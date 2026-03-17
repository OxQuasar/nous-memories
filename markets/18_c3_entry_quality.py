"""
Script 18: C3 Entry Quality Study.

Identifies which indicators at C3 entry predict episode quality
(price change, duration). Uses same regime detection as script 17.

Two outcome variables:
  - Continuous: episode price change (%)
  - Binary: duration >= 6h

Adds microstructure indicators and predecessor regime as features.
"""

import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score

# ─── CONFIG ───
DATA_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
OUTPUT_FILE = '/home/quasar/nous/memories/markets/18_c3_entry_quality_output.txt'
SUBSAMPLE = 300  # 1s → 5min

# ─── COLUMN DEFINITIONS ───
CORE_COLS = {
    0: 'timestamp',
    2: 'price',
}

INDICATOR_COLS = {
    # Trends (7)
    32: 'trend_1h',
    33: 'trend_4h',
    34: 'trend_8h',
    35: 'trend_16h',
    36: 'trend_24h',
    37: 'trend_48h',
    38: 'trend_96h',
    # Trend-of-trends (3)
    39: 'tot_4h',
    40: 'tot_8h',
    41: 'tot_24h',
    # Volatility (4)
    46: 'ols_vol_8h',
    53: 'realized_vol_8h',
    48: 'ols_vol_24h',
    56: 'realized_vol_24h',
    # CVD/volume (3)
    59: 'cvd_slope_5m',
    63: 'cvd_div_15m',
    65: 'vwap_divergence',
    # Microstructure (6)
    70: 'ob_total_ratio_1m',
    74: 'ob_total_ratio_5m',
    72: 'spread_bps_1m',
    73: 'depth_asymmetry_10',
    77: 'liquidity_shift_15m',
    78: 'ob_imbalance_slope_5m',
}

ALL_COLS = {**CORE_COLS, **INDICATOR_COLS}
INDICATOR_NAMES = list(INDICATOR_COLS.values())
# 24 data indicators + 1 computed (is_from_c2)
BONFERRONI = len(INDICATOR_NAMES) + 1  # 25

DURATION_THRESHOLD_H = 6.0
BAR_MINUTES = 5


def load_data(path, every=SUBSAMPLE):
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
    """Regime episodes with flicker debounce."""
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

    ep_data = []
    for k in range(len(merged)):
        s, r = merged[k]
        e = merged[k + 1][0] if k + 1 < len(merged) else n
        ep_data.append({'regime': r, 'start': s, 'end': e})

    return pd.DataFrame(ep_data)


def extract_c3_episodes(df, episodes):
    """Extract C3 episodes with entry indicators, price change, duration, predecessor/successor."""
    records = []
    for i in range(len(episodes)):
        if episodes['regime'].iloc[i] != 3:
            continue

        entry_bar = episodes['start'].iloc[i]
        exit_bar = episodes['end'].iloc[i] - 1  # last bar in episode

        # Price change
        p_start = df['price'].iloc[entry_bar]
        p_end = df['price'].iloc[exit_bar]
        pct_change = (p_end - p_start) / p_start * 100

        # Duration in hours
        n_bars = episodes['end'].iloc[i] - entry_bar
        duration_h = n_bars * BAR_MINUTES / 60.0

        # Predecessor regime
        pred_regime = episodes['regime'].iloc[i - 1] if i > 0 else -1
        is_from_c2 = 1 if pred_regime == 2 else 0

        # Successor regime
        succ_regime = episodes['regime'].iloc[i + 1] if i + 1 < len(episodes) else -1

        row = {
            'pct_change': pct_change,
            'duration_h': duration_h,
            'is_long': int(duration_h >= DURATION_THRESHOLD_H),
            'is_from_c2': is_from_c2,
            'pred_regime': pred_regime,
            'succ_regime': succ_regime,
            'entry_bar': entry_bar,
        }
        for col in INDICATOR_NAMES:
            row[col] = df[col].iloc[entry_bar]

        records.append(row)

    return pd.DataFrame(records)


def format_duration_histogram(durations):
    """Duration histogram in specified bins."""
    bins = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 12), (12, 24), (24, float('inf'))]
    labels = ['0-2h', '2-4h', '4-6h', '6-8h', '8-12h', '12-24h', '24h+']
    lines = []
    for (lo, hi), label in zip(bins, labels):
        count = ((durations >= lo) & (durations < hi)).sum()
        pct = count / len(durations) * 100
        bar = '█' * int(pct / 2)
        lines.append(f"    {label:>6s}: {count:>4d} ({pct:5.1f}%) {bar}")
    return lines


def block1_episode_stats(c3_df):
    """Block 1: Episode Statistics."""
    lines = []
    n = len(c3_df)
    n_c2 = c3_df['is_from_c2'].sum()
    n_c1 = n - n_c2

    lines.append("=" * 100)
    lines.append("  BLOCK 1: C3 Episode Statistics")
    lines.append("=" * 100)
    lines.append(f"  Total C3 episodes: {n}")
    lines.append(f"  From C2 (predecessor): {n_c2} ({n_c2/n:.1%})")
    lines.append(f"  From C1 (predecessor): {n_c1} ({n_c1/n:.1%})")
    lines.append("")

    # Duration distribution
    dur = c3_df['duration_h']
    lines.append("  Duration (hours):")
    lines.append(f"    min={dur.min():.1f}  Q1={dur.quantile(0.25):.1f}  median={dur.quantile(0.5):.1f}  "
                 f"Q3={dur.quantile(0.75):.1f}  max={dur.max():.1f}  mean={dur.mean():.1f}")
    lines.append(f"    Fraction ≥ {DURATION_THRESHOLD_H}h: {(dur >= DURATION_THRESHOLD_H).mean():.1%}")
    lines.append("")
    lines.append("  Duration histogram:")
    lines.extend(format_duration_histogram(dur.values))
    lines.append("")

    # Price change distribution
    pc = c3_df['pct_change']
    lines.append("  Price change (%):")
    lines.append(f"    min={pc.min():.2f}  Q1={pc.quantile(0.25):.2f}  median={pc.quantile(0.5):.2f}  "
                 f"Q3={pc.quantile(0.75):.2f}  max={pc.max():.2f}  mean={pc.mean():.2f}")
    lines.append("")

    # Price change by duration bucket
    short = c3_df[c3_df['duration_h'] < DURATION_THRESHOLD_H]['pct_change']
    long = c3_df[c3_df['duration_h'] >= DURATION_THRESHOLD_H]['pct_change']
    lines.append(f"  Price change by duration:")
    lines.append(f"    < {DURATION_THRESHOLD_H}h (n={len(short)}): mean={short.mean():.2f}%  median={short.median():.2f}%")
    lines.append(f"    ≥ {DURATION_THRESHOLD_H}h (n={len(long)}):  mean={long.mean():.2f}%  median={long.median():.2f}%")
    lines.append("")

    return lines


def block2_price_change_correlation(c3_df):
    """Block 2: Spearman correlation with episode price change."""
    lines = []
    lines.append("=" * 100)
    lines.append("  BLOCK 2: Correlation with Episode Price Change (Spearman)")
    lines.append(f"  Bonferroni factor: {BONFERRONI}")
    lines.append("=" * 100)

    all_indicators = INDICATOR_NAMES + ['is_from_c2']
    y = c3_df['pct_change'].values

    results = []
    for ind in all_indicators:
        x = c3_df[ind].values.astype(float)
        valid = ~np.isnan(x) & ~np.isnan(y)
        x_v, y_v = x[valid], y[valid]
        n_avail = len(x_v)

        if n_avail < 10:
            continue

        # Skip constant inputs (e.g. tot_* in C3 regime)
        if np.std(x_v) == 0:
            continue

        rho, p_raw = stats.spearmanr(x_v, y_v)
        if np.isnan(rho):
            continue
        p_corr = min(p_raw * BONFERRONI, 1.0)
        flag = '***' if n_avail < 150 else ''

        results.append({
            'indicator': ind,
            'rho': rho,
            'abs_rho': abs(rho),
            'p_raw': p_raw,
            'p_corr': p_corr,
            'n': n_avail,
            'flag': flag,
        })

    res_df = pd.DataFrame(results).sort_values('abs_rho', ascending=False).reset_index(drop=True)

    hdr = f"  {'Rank':>4s} | {'Indicator':<24s} | {'ρ':>7s} | {'p_raw':>10s} | {'p_corr':>10s} | {'n':>5s}"
    sep = "  " + "-" * (len(hdr) - 2)
    lines.append(hdr)
    lines.append(sep)

    for rank, (_, row) in enumerate(res_df.iterrows(), 1):
        flag = ' (n<150)' if row['flag'] else ''
        lines.append(f"  {rank:>4d} | {row['indicator']:<24s} | {row['rho']:>+7.4f} | "
                     f"{row['p_raw']:>10.2e} | {row['p_corr']:>10.2e} | {row['n']:>5d}{flag}")

    lines.append("")
    return lines, res_df


def block3_duration_separation(c3_df):
    """Block 3: Separation by duration >= threshold (AUC, Cohen's d)."""
    lines = []
    lines.append("=" * 100)
    lines.append(f"  BLOCK 3: Separation by Duration ≥ {DURATION_THRESHOLD_H}h (Binary)")
    lines.append(f"  Bonferroni factor: {BONFERRONI}")
    lines.append("=" * 100)

    all_indicators = INDICATOR_NAMES + ['is_from_c2']
    y = c3_df['is_long'].values

    n_long = y.sum()
    n_short = len(y) - n_long
    lines.append(f"  Long (≥{DURATION_THRESHOLD_H}h): {n_long}   Short (<{DURATION_THRESHOLD_H}h): {n_short}")
    lines.append("")

    results = []
    for ind in all_indicators:
        x = c3_df[ind].values.astype(float)
        valid = ~np.isnan(x)
        x_v, y_v = x[valid], y[valid]
        n_avail = len(x_v)

        if n_avail < 10 or y_v.sum() < 3 or (len(y_v) - y_v.sum()) < 3:
            continue

        x_pos = x_v[y_v == 1]
        x_neg = x_v[y_v == 0]
        u_stat, p_raw = stats.mannwhitneyu(x_pos, x_neg, alternative='two-sided')
        auc = u_stat / (len(x_pos) * len(x_neg))
        auc_dist = abs(auc - 0.5)

        pooled_std = x_v.std(ddof=1)
        cohens_d = (x_pos.mean() - x_neg.mean()) / pooled_std if pooled_std > 0 else 0.0

        p_corr = min(p_raw * BONFERRONI, 1.0)
        flag = '***' if n_avail < 150 else ''

        results.append({
            'indicator': ind,
            'auc': auc,
            'auc_dist': auc_dist,
            'cohens_d': cohens_d,
            'p_raw': p_raw,
            'p_corr': p_corr,
            'n': n_avail,
            'flag': flag,
        })

    res_df = pd.DataFrame(results).sort_values('auc_dist', ascending=False).reset_index(drop=True)

    hdr = f"  {'Rank':>4s} | {'Indicator':<24s} | {'AUC':>6s} | {'Cohen_d':>8s} | {'p_raw':>10s} | {'p_corr':>10s} | {'n':>5s}"
    sep = "  " + "-" * (len(hdr) - 2)
    lines.append(hdr)
    lines.append(sep)

    for rank, (_, row) in enumerate(res_df.iterrows(), 1):
        flag = ' (n<150)' if row['flag'] else ''
        lines.append(f"  {rank:>4d} | {row['indicator']:<24s} | {row['auc']:>6.3f} | {row['cohens_d']:>+8.3f} | "
                     f"{row['p_raw']:>10.2e} | {row['p_corr']:>10.2e} | {row['n']:>5d}{flag}")

    lines.append("")
    return lines, res_df


def block4_independence_stability(c3_df, b2_df, b3_df):
    """Block 4: Independence & stability checks for significant indicators."""
    lines = []
    lines.append("=" * 100)
    lines.append("  BLOCK 4: Independence & Stability Checks")
    lines.append("  (Indicators with p_corr < 0.05 in Block 2 or Block 3)")
    lines.append("=" * 100)

    # Collect significant indicators
    sig_b2 = set(b2_df[b2_df['p_corr'] < 0.05]['indicator'].tolist()) if len(b2_df) > 0 else set()
    sig_b3 = set(b3_df[b3_df['p_corr'] < 0.05]['indicator'].tolist()) if len(b3_df) > 0 else set()
    sig_all = sig_b2 | sig_b3

    if not sig_all:
        lines.append("  No indicators reached p_corr < 0.05 in either block.")
        lines.append("")
        return lines

    t8h_mag = np.abs(c3_df['trend_8h'].values)
    t48h_mag = np.abs(c3_df['trend_48h'].values)

    for ind in sorted(sig_all):
        in_b2 = ind in sig_b2
        in_b3 = ind in sig_b3
        if in_b2 and in_b3:
            signal_type = "both"
        elif in_b2:
            signal_type = "entry quality signal"
        else:
            signal_type = "duration filter candidate"

        lines.append(f"\n  ── {ind} ({signal_type}) ──")

        x = c3_df[ind].values.astype(float)
        valid = ~np.isnan(x)
        x_v = x[valid]

        # Correlation with trend magnitudes
        r_t8h, _ = stats.spearmanr(x_v, t8h_mag[valid])
        r_t48h, _ = stats.spearmanr(x_v, t48h_mag[valid])
        lines.append(f"    Spearman with |trend_8h|:  {r_t8h:+.4f}")
        lines.append(f"    Spearman with |trend_48h|: {r_t48h:+.4f}")

        # Split-half stability
        mid = len(c3_df) // 2
        for metric_name, block_type in [('ρ (price change)', 'b2'), ('AUC (duration)', 'b3')]:
            if block_type == 'b2' and not in_b2:
                continue
            if block_type == 'b3' and not in_b3:
                continue

            halves = []
            for half_label, slc in [('H1', slice(0, mid)), ('H2', slice(mid, None))]:
                x_h = c3_df[ind].iloc[slc].values.astype(float)
                valid_h = ~np.isnan(x_h)

                if block_type == 'b2':
                    y_h = c3_df['pct_change'].iloc[slc].values
                    v = valid_h & ~np.isnan(y_h)
                    if v.sum() < 10:
                        halves.append((half_label, np.nan))
                        continue
                    rho_h, _ = stats.spearmanr(x_h[v], y_h[v])
                    halves.append((half_label, rho_h))
                else:
                    y_h = c3_df['is_long'].iloc[slc].values
                    v = valid_h
                    x_hv, y_hv = x_h[v], y_h[v]
                    if len(x_hv) < 10 or y_hv.sum() < 2 or (len(y_hv) - y_hv.sum()) < 2:
                        halves.append((half_label, np.nan))
                        continue
                    x_pos = x_hv[y_hv == 1]
                    x_neg = x_hv[y_hv == 0]
                    u, _ = stats.mannwhitneyu(x_pos, x_neg, alternative='two-sided')
                    auc_h = u / (len(x_pos) * len(x_neg))
                    halves.append((half_label, auc_h))

            v1, v2 = halves[0][1], halves[1][1]
            v1_s = f"{v1:.4f}" if not np.isnan(v1) else "N/A"
            v2_s = f"{v2:.4f}" if not np.isnan(v2) else "N/A"
            lines.append(f"    Split-half {metric_name}: H1={v1_s}  H2={v2_s}")

    lines.append("")
    return lines


def block5_trade_crosscheck(c3_df, episodes):
    """Block 5: Trade-level cross-check. C3↔C2 chains until exit to C0/C1."""
    lines = []
    lines.append("=" * 100)
    lines.append("  BLOCK 5: Trade-Level Cross-Check (informational)")
    lines.append("  Consecutive C3↔C2 chains until exit to C0 or C1")
    lines.append("=" * 100)

    # Build trades: start from C3, follow C3→C2→C3→... until non-C2/C3
    ep_regimes = episodes['regime'].values
    n_ep = len(episodes)
    used = set()
    trades = []

    for i in range(n_ep):
        if i in used or ep_regimes[i] != 3:
            continue

        # Start a trade chain
        chain = [i]
        used.add(i)
        j = i + 1
        while j < n_ep:
            r = ep_regimes[j]
            if r in (2, 3):
                chain.append(j)
                used.add(j)
                j += 1
            else:
                break

        # Determine exit: what comes after the chain
        exit_idx = j
        if exit_idx < n_ep:
            exit_regime = ep_regimes[exit_idx]
            if exit_regime == 1:
                exit_label = 'XC1'
            elif exit_regime == 0:
                exit_label = 'XC0'
            else:
                exit_label = f'X{exit_regime}'
        else:
            exit_label = 'end'

        # Entry bar = first bar of first C3 in chain
        entry_bar = episodes['start'].iloc[chain[0]]
        # C3 episodes in this chain
        c3_indices_in_chain = [k for k in chain if ep_regimes[k] == 3]

        trades.append({
            'entry_bar': entry_bar,
            'exit_label': exit_label,
            'n_c3_episodes': len(c3_indices_in_chain),
            'chain_len': len(chain),
        })

    trades_df = pd.DataFrame(trades)
    n_trades = len(trades_df)

    # Count by exit label
    exit_counts = trades_df['exit_label'].value_counts()
    lines.append(f"  Total trades: {n_trades}")
    for label, count in exit_counts.items():
        lines.append(f"    {label}: {count}")
    lines.append("")

    # Map C3 episodes to their trade's exit label
    # Re-do: for each C3 episode in c3_df, find which trade it belongs to
    # We use entry_bar matching
    c3_entry_bars = c3_df['entry_bar'].values

    # Build map: episode start → trade info
    ep_to_trade = {}
    for i in range(n_ep):
        if i in used or ep_regimes[i] != 3:
            pass  # already handled above... need different approach

    # Simpler: re-walk and tag each C3 episode
    trade_labels = {}  # entry_bar → exit_label
    for i in range(n_ep):
        if ep_regimes[i] != 3:
            continue
        # Walk forward from this episode to find chain exit
        j = i + 1
        while j < n_ep and ep_regimes[j] in (2, 3):
            j += 1
        if j < n_ep:
            exit_r = ep_regimes[j]
            exit_label = 'XC1' if exit_r == 1 else ('XC0' if exit_r == 0 else f'X{exit_r}')
        else:
            exit_label = 'end'
        trade_labels[episodes['start'].iloc[i]] = exit_label

    c3_df_copy = c3_df.copy()
    c3_df_copy['trade_exit'] = c3_df_copy['entry_bar'].map(trade_labels)

    # Filter to XC0 vs XC1
    xc0_mask = c3_df_copy['trade_exit'] == 'XC0'
    xc1_mask = c3_df_copy['trade_exit'] == 'XC1'
    n_xc0 = xc0_mask.sum()
    n_xc1 = xc1_mask.sum()

    lines.append(f"  C3 episodes with XC0 exit: {n_xc0}")
    lines.append(f"  C3 episodes with XC1 exit: {n_xc1}")
    lines.append(f"  n≈{n_trades}, informational only, not used for ranking")
    lines.append("")

    if n_xc0 >= 5 and n_xc1 >= 5:
        # Test top indicators at trade level using FIRST C3 entry only
        # Filter to first C3 per trade
        first_c3_bars = set()
        for i in range(n_ep):
            if ep_regimes[i] != 3:
                continue
            # Is this the first C3 in its chain? Check if predecessor is not C2/C3
            if i == 0 or ep_regimes[i - 1] not in (2, 3):
                first_c3_bars.add(episodes['start'].iloc[i])

        first_mask = c3_df_copy['entry_bar'].isin(first_c3_bars)
        trade_df = c3_df_copy[first_mask & (xc0_mask | xc1_mask)].copy()
        trade_df['outcome'] = (trade_df['trade_exit'] == 'XC1').astype(int)

        n_t = len(trade_df)
        lines.append(f"  First-C3-per-trade subset: {n_t} trades")

        if n_t >= 15 and trade_df['outcome'].sum() >= 3 and (n_t - trade_df['outcome'].sum()) >= 3:
            y_t = trade_df['outcome'].values
            all_indicators = INDICATOR_NAMES + ['is_from_c2']

            trade_results = []
            for ind in all_indicators:
                x = trade_df[ind].values.astype(float)
                valid = ~np.isnan(x)
                x_v, y_v = x[valid], y_t[valid]
                if len(x_v) < 10 or y_v.sum() < 2 or (len(y_v) - y_v.sum()) < 2:
                    continue
                x_pos = x_v[y_v == 1]
                x_neg = x_v[y_v == 0]
                u, p = stats.mannwhitneyu(x_pos, x_neg, alternative='two-sided')
                auc = u / (len(x_pos) * len(x_neg))
                trade_results.append({
                    'indicator': ind,
                    'auc': auc,
                    'auc_dist': abs(auc - 0.5),
                    'p_raw': p,
                    'n': len(x_v),
                })

            if trade_results:
                tr_df = pd.DataFrame(trade_results).sort_values('auc_dist', ascending=False).reset_index(drop=True)
                hdr = f"  {'Rank':>4s} | {'Indicator':<24s} | {'AUC':>6s} | {'p_raw':>10s} | {'n':>5s}"
                sep_line = "  " + "-" * (len(hdr) - 2)
                lines.append(hdr)
                lines.append(sep_line)
                for rank, (_, row) in enumerate(tr_df.head(10).iterrows(), 1):
                    lines.append(f"  {rank:>4d} | {row['indicator']:<24s} | {row['auc']:>6.3f} | "
                                 f"{row['p_raw']:>10.2e} | {row['n']:>5d}")
        else:
            lines.append("  Insufficient trades for AUC analysis.")
    else:
        lines.append("  Insufficient XC0/XC1 trades for comparison.")

    lines.append("")
    return lines


def main():
    print("Loading data...", flush=True)
    df = load_data(DATA_FILE)
    print(f"  {len(df)} bars (5-min), price {df['price'].min():.0f}–{df['price'].max():.0f}")

    print("Assigning regimes...", flush=True)
    assign_regime(df)
    episodes = detect_episodes(df)
    print(f"  {len(episodes)} episodes detected")

    # Regime counts
    for r in [0, 1, 2, 3]:
        n = (episodes['regime'] == r).sum()
        print(f"    C{r}: {n} episodes")

    print("Extracting C3 episodes...", flush=True)
    c3_df = extract_c3_episodes(df, episodes)
    print(f"  {len(c3_df)} C3 episodes extracted")

    # Build output
    all_lines = []

    all_lines.append("")
    all_lines.append("  Script 18: C3 Entry Quality Study")
    all_lines.append(f"  Data: {len(df)} bars, {len(episodes)} episodes, {len(c3_df)} C3 episodes")
    all_lines.append("")

    # Block 1
    print("Block 1: Episode statistics...", flush=True)
    all_lines.extend(block1_episode_stats(c3_df))

    # Block 2
    print("Block 2: Price change correlation...", flush=True)
    b2_lines, b2_df = block2_price_change_correlation(c3_df)
    all_lines.extend(b2_lines)

    # Block 3
    print("Block 3: Duration separation...", flush=True)
    b3_lines, b3_df = block3_duration_separation(c3_df)
    all_lines.extend(b3_lines)

    # Block 4
    print("Block 4: Independence & stability...", flush=True)
    b4_lines = block4_independence_stability(c3_df, b2_df, b3_df)
    all_lines.extend(b4_lines)

    # Block 5
    print("Block 5: Trade-level cross-check...", flush=True)
    b5_lines = block5_trade_crosscheck(c3_df, episodes)
    all_lines.extend(b5_lines)

    output = '\n'.join(all_lines)
    print(output)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)
    print(f"\nOutput saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
