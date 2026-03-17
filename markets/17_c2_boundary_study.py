"""
Script 17: C2 Boundary Indicator Study.

Identifies which indicators carry information about C2 pullback outcomes
(→C3 bull vs →C0 bear) beyond what trend_8h already provides.

Uses regime detection from 16_grade_regime.py (sign-based 2-bit, flicker debounce).
Snapshots indicators at C2 ENTRY (first bar post-debounce).
"""

import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score

# ─── CONFIG ───
DATA_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
OUTPUT_FILE = '/home/quasar/nous/memories/markets/17_c2_boundary_output.txt'
SUBSAMPLE = 300  # 1s → 5min

# Logistic model coefficients (simulator units, from 16_grade_regime.py)
SCALE_FACTOR = 10.0
C2_COEFS_SIM = (5.209, 1477.0 * SCALE_FACTOR, 348533.0 * SCALE_FACTOR)

# ─── COLUMN DEFINITIONS ───
# Core columns (always loaded)
CORE_COLS = {
    0: 'timestamp',
    2: 'price',
    32: 'trend_1h',
    34: 'trend_8h',
    37: 'trend_48h',
}

# Indicator columns to study
INDICATOR_COLS = {
    # Group 1: Intermediate trends
    33: 'trend_4h',
    35: 'trend_16h',
    36: 'trend_24h',
    38: 'trend_96h',
    # Group 2: Trend-of-trends
    39: 'tot_4h',
    40: 'tot_8h',
    41: 'tot_24h',
    # Group 3: Volatility (OLS)
    45: 'ols_vol_4h',
    46: 'ols_vol_8h',
    47: 'ols_vol_16h',
    48: 'ols_vol_24h',
    # Group 3: Volatility (realized)
    52: 'realized_vol_4h',
    53: 'realized_vol_8h',
    55: 'realized_vol_16h',
    56: 'realized_vol_24h',
    # Group 4: Volume/CVD
    59: 'cvd_slope_5m',
    63: 'cvd_div_15m',
    65: 'vwap_divergence',
}

ALL_COLS = {**CORE_COLS, **INDICATOR_COLS}
INDICATOR_NAMES = list(INDICATOR_COLS.values())
N_INDICATORS = len(INDICATOR_NAMES)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def load_data(path, every=SUBSAMPLE):
    """Load needed columns, subsample to 5-min."""
    col_indices = sorted(ALL_COLS.keys())
    col_names = [ALL_COLS[i] for i in col_indices]
    df = pd.read_csv(path, usecols=col_indices, names=col_names, header=0)
    df = df.iloc[::every].reset_index(drop=True)
    return df


def assign_regime(df):
    """2-bit regime: sign(trend_8h) × sign(trend_48h). Zero = positive."""
    b8 = (df['trend_8h'] >= 0).astype(int)
    b48 = (df['trend_48h'] >= 0).astype(int)
    df['regime'] = b8 + 2 * b48
    return df


def detect_episodes(df):
    """Regime episodes with flicker debounce (from 16_grade_regime.py)."""
    regime = df['regime'].values
    n = len(regime)

    changes = np.where(np.diff(regime) != 0)[0] + 1
    starts = np.concatenate([[0], changes])
    ends = np.concatenate([changes, [n]])
    raw_regimes = regime[starts]
    raw_durations = ends - starts

    # Flicker debounce: absorb 1-bar A→B→A back into A
    kept_idx = list(range(len(starts)))
    changed = True
    while changed:
        changed = False
        new_kept = []
        i = 0
        while i < len(kept_idx):
            idx = kept_idx[i]
            if (raw_durations[idx] == 1
                    and i > 0 and i < len(kept_idx) - 1):
                prev_r = raw_regimes[kept_idx[i - 1]]
                next_r = raw_regimes[kept_idx[i + 1]]
                if prev_r == next_r:
                    changed = True
                    i += 1
                    continue
            new_kept.append(idx)
            i += 1
        kept_idx = new_kept

    # Merge consecutive same-regime
    merged = []
    for idx in kept_idx:
        r = raw_regimes[idx]
        if merged and merged[-1][1] == r:
            continue
        merged.append((starts[idx], r))

    # Build episode list
    ep_data = []
    for k in range(len(merged)):
        s, r = merged[k]
        e = merged[k + 1][0] if k + 1 < len(merged) else n
        ep_data.append({'regime': r, 'start': s, 'end': e})

    return pd.DataFrame(ep_data)


def extract_c2_episodes(df, episodes):
    """Extract C2 episodes with outcomes and indicator snapshots at entry.

    Returns DataFrame with one row per C2 episode:
    - outcome: 1 = C3 (success), 0 = C0 (failure)
    - indicator values at entry bar
    """
    records = []
    for i in range(len(episodes)):
        if episodes['regime'].iloc[i] != 2:
            continue
        # Need next episode for outcome
        if i + 1 >= len(episodes):
            continue
        next_regime = episodes['regime'].iloc[i + 1]
        # C2 can only go to C3 (success) or C0 (failure)
        if next_regime == 3:
            outcome = 1
        elif next_regime == 0:
            outcome = 0
        else:
            continue  # guard

        entry_bar = episodes['start'].iloc[i]
        row = {'outcome': outcome}
        for col in INDICATOR_NAMES:
            row[col] = df[col].iloc[entry_bar]
        # Also grab core columns for logistic model
        row['trend_1h'] = df['trend_1h'].iloc[entry_bar]
        row['trend_8h'] = df['trend_8h'].iloc[entry_bar]
        records.append(row)

    return pd.DataFrame(records)


def compute_indicator_stats(c2_df):
    """Compute AUC, effect size, correlation, stability, p-value for each indicator."""
    y = c2_df['outcome'].values
    n1 = y.sum()       # C3 (success)
    n0 = len(y) - n1   # C0 (failure)
    t8h = c2_df['trend_8h'].values

    results = []
    for ind in INDICATOR_NAMES:
        x = c2_df[ind].values
        valid = ~np.isnan(x)
        x_v, y_v, t8h_v = x[valid], y[valid], t8h[valid]

        if len(x_v) < 10 or y_v.sum() < 3 or (len(y_v) - y_v.sum()) < 3:
            continue

        # a) AUC (Mann-Whitney)
        x_pos = x_v[y_v == 1]
        x_neg = x_v[y_v == 0]
        u_stat, p_raw = stats.mannwhitneyu(x_pos, x_neg, alternative='two-sided')
        auc = u_stat / (len(x_pos) * len(x_neg))
        direction = '+' if auc >= 0.5 else '-'
        auc_abs = max(auc, 1 - auc)

        # b) Effect size
        rank_biserial = 2 * auc - 1
        pooled_std = x_v.std(ddof=1)
        if pooled_std > 0:
            cohens_d = (x_pos.mean() - x_neg.mean()) / pooled_std
        else:
            cohens_d = 0.0

        # c) Correlation with trend_8h
        r_t8h, _ = stats.spearmanr(x_v, t8h_v)

        # d) Split-half stability
        mid = len(x_v) // 2
        auc_halves = []
        for half_x, half_y in [(x_v[:mid], y_v[:mid]), (x_v[mid:], y_v[mid:])]:
            if half_y.sum() < 2 or (len(half_y) - half_y.sum()) < 2:
                auc_halves.append(np.nan)
                continue
            h_pos = half_x[half_y == 1]
            h_neg = half_x[half_y == 0]
            h_u, _ = stats.mannwhitneyu(h_pos, h_neg, alternative='two-sided')
            auc_halves.append(h_u / (len(h_pos) * len(h_neg)))

        half1, half2 = auc_halves
        # Stable = same direction (both > 0.5 or both < 0.5)
        if np.isnan(half1) or np.isnan(half2):
            stable = 'N/A'
        elif (half1 >= 0.5) == (half2 >= 0.5):
            stable = 'Y'
        else:
            stable = 'N'

        # e) p-value with Bonferroni
        p_corr = min(p_raw * N_INDICATORS, 1.0)

        results.append({
            'indicator': ind,
            'auc': auc,
            'auc_abs': auc_abs,
            'direction': direction,
            'cohens_d': cohens_d,
            'r_t8h': r_t8h,
            'half1': half1,
            'half2': half2,
            'stable': stable,
            'p_raw': p_raw,
            'p_corr': p_corr,
        })

    return pd.DataFrame(results).sort_values('auc_abs', ascending=False).reset_index(drop=True)


def residual_analysis(c2_df, stats_df):
    """For indicators passing all gates, compute residual AUC within logistic bins."""
    # Gates: AUC_abs > 0.60, |r_t8h| < 0.7, stable = Y
    candidates = stats_df[
        (stats_df['auc_abs'] > 0.60) &
        (stats_df['r_t8h'].abs() < 0.7) &
        (stats_df['stable'] == 'Y')
    ]

    if len(candidates) == 0:
        return None, candidates

    # Compute logistic probability
    b0, b1, b8 = C2_COEFS_SIM
    logit = b0 + b1 * c2_df['trend_1h'].values + b8 * c2_df['trend_8h'].values
    p_bull = sigmoid(logit)
    y = c2_df['outcome'].values

    # Bin edges
    bins = [('P<0.20', p_bull < 0.20),
            ('0.20≤P≤0.80', (p_bull >= 0.20) & (p_bull <= 0.80)),
            ('P>0.80', p_bull > 0.80)]

    residual_results = []
    for _, row in candidates.iterrows():
        ind = row['indicator']
        x = c2_df[ind].values
        valid = ~np.isnan(x)

        ind_res = {'indicator': ind, 'bins': []}
        any_residual = False

        for bin_label, mask in bins:
            m = mask & valid
            n_bin = m.sum()
            y_bin = y[m]
            x_bin = x[m]

            if n_bin < 10 or y_bin.sum() < 2 or (n_bin - y_bin.sum()) < 2:
                ind_res['bins'].append((bin_label, n_bin, np.nan))
                continue

            x_pos = x_bin[y_bin == 1]
            x_neg = x_bin[y_bin == 0]
            u, _ = stats.mannwhitneyu(x_pos, x_neg, alternative='two-sided')
            residual_auc = u / (len(x_pos) * len(x_neg))
            residual_auc_abs = max(residual_auc, 1 - residual_auc)
            if residual_auc_abs > 0.55:
                any_residual = True
            ind_res['bins'].append((bin_label, n_bin, residual_auc))

        ind_res['independent'] = any_residual
        residual_results.append(ind_res)

    return residual_results, candidates


def format_output(c2_df, stats_df, residual_results, candidates):
    """Format all output."""
    lines = []
    y = c2_df['outcome'].values
    n_total = len(y)
    n_success = y.sum()
    n_fail = n_total - n_success

    lines.append("=" * 110)
    lines.append("  C2 Boundary Study: Indicator Ranking")
    lines.append("=" * 110)
    lines.append(f"  Episodes: {n_total} total ({n_success} C2→C3 success, {n_fail} C2→C0 failure)")
    lines.append(f"  Base rate: {n_success/n_total:.1%} success")
    lines.append(f"  Indicators tested: {N_INDICATORS}")
    lines.append(f"  Bonferroni correction factor: {N_INDICATORS}")
    lines.append("")

    # Main table
    hdr = (f"{'Rank':>4s} | {'Indicator':<20s} | {'AUC':>5s} | {'Dir':>3s} | {'Cohen_d':>7s} | "
           f"{'r_t8h':>6s} | {'Half1':>5s} | {'Half2':>5s} | {'Stbl':>4s} | "
           f"{'p_raw':>9s} | {'p_corr':>9s} | {'Indep':>5s}")
    sep = "-" * len(hdr)
    lines.append(hdr)
    lines.append(sep)

    # Build independence map
    indep_map = {}
    if residual_results:
        for r in residual_results:
            indep_map[r['indicator']] = 'Y' if r['independent'] else 'N'

    for rank, (_, row) in enumerate(stats_df.iterrows(), 1):
        ind = row['indicator']
        indep = indep_map.get(ind, '-')

        # Flag high correlation
        dep_flag = 'dep' if abs(row['r_t8h']) >= 0.7 else indep

        h1 = f"{row['half1']:.2f}" if not np.isnan(row['half1']) else '  N/A'
        h2 = f"{row['half2']:.2f}" if not np.isnan(row['half2']) else '  N/A'

        line = (f"{rank:>4d} | {ind:<20s} | {row['auc_abs']:.3f} | {row['direction']:>3s} | "
                f"{row['cohens_d']:>+7.3f} | {row['r_t8h']:>+6.3f} | {h1:>5s} | {h2:>5s} | "
                f"{row['stable']:>4s} | {row['p_raw']:>9.2e} | {row['p_corr']:>9.2e} | {dep_flag:>5s}")
        lines.append(line)

    # Conditional distribution for passing indicators
    # Note structural zeros
    lines.append("")
    lines.append("  Note: tot_4h/tot_8h/tot_24h are structurally zero during C2 regime")
    lines.append("  (trend-of-trend computation produces constant values given regime sign constraints)")

    if residual_results:
        lines.append("")
        lines.append("=" * 110)
        lines.append("  Residual Analysis: Indicators Passing All Gates")
        lines.append("  Gates: AUC_abs > 0.60, |r_t8h| < 0.7, split-half stable")
        lines.append("=" * 110)

        for res in residual_results:
            ind = res['indicator']
            x = c2_df[ind].values
            y_vals = c2_df['outcome'].values
            valid = ~np.isnan(x)
            x_v, y_v = x[valid], y_vals[valid]

            x_pos = x_v[y_v == 1]
            x_neg = x_v[y_v == 0]

            lines.append(f"\n  ── {ind} ──")
            lines.append(f"    C3 group (success): mean={np.mean(x_pos):.6e} ± {np.std(x_pos):.6e}  (n={len(x_pos)})")
            lines.append(f"    C0 group (failure): mean={np.mean(x_neg):.6e} ± {np.std(x_neg):.6e}  (n={len(x_neg)})")
            lines.append("")
            lines.append(f"    {'Bin':<14s}  {'n':>5s}  {'Residual AUC':>12s}  {'Verdict':>8s}")
            lines.append(f"    {'-'*50}")

            for bin_label, n_bin, r_auc in res['bins']:
                if np.isnan(r_auc):
                    lines.append(f"    {bin_label:<14s}  {n_bin:>5d}  {'N/A':>12s}  {'':>8s}")
                else:
                    r_abs = max(r_auc, 1 - r_auc)
                    verdict = '✓ info' if r_abs > 0.55 else '– none'
                    lines.append(f"    {bin_label:<14s}  {n_bin:>5d}  {r_auc:>12.3f}  {verdict:>8s}")

            overall = 'INDEPENDENT' if res['independent'] else 'redundant'
            lines.append(f"    → {overall}")
    else:
        lines.append("")
        lines.append("  No indicators passed all gates (AUC>0.60, |r_t8h|<0.7, stable).")

    lines.append("")
    lines.append("=" * 110)
    return '\n'.join(lines)


def main():
    print("Loading data...", flush=True)
    df = load_data(DATA_FILE)
    print(f"  {len(df)} bars (5-min), price {df['price'].min():.0f}–{df['price'].max():.0f}")

    print("Assigning regimes...", flush=True)
    assign_regime(df)
    episodes = detect_episodes(df)
    print(f"  {len(episodes)} episodes detected")

    print("Extracting C2 episodes...", flush=True)
    c2_df = extract_c2_episodes(df, episodes)
    n_total = len(c2_df)
    n_success = c2_df['outcome'].sum()
    print(f"  {n_total} C2 episodes ({n_success} →C3, {n_total - n_success} →C0)")

    print("Computing indicator statistics...", flush=True)
    stats_df = compute_indicator_stats(c2_df)

    print("Running residual analysis...", flush=True)
    residual_results, candidates = residual_analysis(c2_df, stats_df)

    output = format_output(c2_df, stats_df, residual_results, candidates)
    print(output)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)
    print(f"\nOutput saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
