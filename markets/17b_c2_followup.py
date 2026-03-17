"""
Script 17b: C2 Boundary Follow-up Analyses.

Five analyses on C2 episode data:
1. Cross-correlation matrix (trend_8h/16h/24h/48h)
2. Operational split in P>0.80 logistic bin (trend_24h/16h sign)
3. Continuous vs binary (magnitude AUC within sign groups)
4. Forward data check
5. Trend stack depth (trend_4h/16h/24h sign composite)
"""

import numpy as np
import pandas as pd
from scipy import stats

# ─── CONFIG ───
IS_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
FWD_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2026-02-20_2026-03-13.csv'
OUTPUT_FILE = '/home/quasar/nous/memories/markets/17b_c2_followup_output.txt'
SUBSAMPLE = 300  # 1s → 5min

SCALE_FACTOR = 10.0
C2_COEFS_SIM = (5.209, 1477.0 * SCALE_FACTOR, 348533.0 * SCALE_FACTOR)

# Columns needed (0-indexed)
COLS = {
    0: 'timestamp', 2: 'price',
    32: 'trend_1h', 33: 'trend_4h', 34: 'trend_8h',
    35: 'trend_16h', 36: 'trend_24h', 37: 'trend_48h',
}
TREND_COLS = ['trend_8h', 'trend_16h', 'trend_24h', 'trend_48h']
SNAPSHOT_COLS = ['trend_1h', 'trend_4h', 'trend_8h', 'trend_16h', 'trend_24h', 'trend_48h']


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def load_data(path):
    col_indices = sorted(COLS.keys())
    col_names = [COLS[i] for i in col_indices]
    df = pd.read_csv(path, usecols=col_indices, names=col_names, header=0)
    return df.iloc[::SUBSAMPLE].reset_index(drop=True)


def assign_regime(df):
    b8 = (df['trend_8h'] >= 0).astype(int)
    b48 = (df['trend_48h'] >= 0).astype(int)
    df['regime'] = b8 + 2 * b48
    return df


def detect_episodes(df):
    regime = df['regime'].values
    n = len(regime)

    changes = np.where(np.diff(regime) != 0)[0] + 1
    starts = np.concatenate([[0], changes])
    ends = np.concatenate([changes, [n]])
    raw_regimes = regime[starts]
    raw_durations = ends - starts

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


def extract_c2_episodes(df, episodes):
    records = []
    for i in range(len(episodes)):
        if episodes['regime'].iloc[i] != 2:
            continue
        if i + 1 >= len(episodes):
            continue
        next_regime = episodes['regime'].iloc[i + 1]
        if next_regime == 3:
            outcome = 1
        elif next_regime == 0:
            outcome = 0
        else:
            continue

        entry_bar = episodes['start'].iloc[i]
        row = {'outcome': outcome}
        for col in SNAPSHOT_COLS:
            row[col] = df[col].iloc[entry_bar]
        records.append(row)

    return pd.DataFrame(records)


def p_bull(c2_df):
    """Logistic P(bull) from existing model."""
    b0, b1, b8 = C2_COEFS_SIM
    logit = b0 + b1 * c2_df['trend_1h'].values + b8 * c2_df['trend_8h'].values
    return sigmoid(logit)


def safe_auc(x, y):
    """Mann-Whitney AUC, returns NaN if insufficient data."""
    x_pos, x_neg = x[y == 1], x[y == 0]
    if len(x_pos) < 3 or len(x_neg) < 3:
        return np.nan
    u, _ = stats.mannwhitneyu(x_pos, x_neg, alternative='two-sided')
    return u / (len(x_pos) * len(x_neg))


# ═══════════════════════════════════════════════════════════════
# Analysis functions
# ═══════════════════════════════════════════════════════════════

def analysis_1_cross_correlation(c2_df):
    """Spearman cross-correlation matrix at C2 entry."""
    lines = []
    lines.append("=" * 80)
    lines.append("  Analysis 1: Cross-Correlation Matrix (Spearman, C2 entry snapshots)")
    lines.append("=" * 80)
    lines.append(f"  Episodes: {len(c2_df)}")
    lines.append("")

    data = c2_df[TREND_COLS].values
    n = len(TREND_COLS)
    corr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            corr[i, j], _ = stats.spearmanr(data[:, i], data[:, j])

    # Print matrix
    hdr = "              " + "  ".join(f"{c:>12s}" for c in TREND_COLS)
    lines.append(hdr)
    for i, name in enumerate(TREND_COLS):
        vals = "  ".join(f"{corr[i, j]:>+12.3f}" for j in range(n))
        lines.append(f"  {name:>12s}{vals}")

    lines.append("")
    lines.append("  Key pairs:")
    pairs = [
        ('trend_24h', 'trend_48h', 0.7, "reduces to trend_48h magnitude"),
        ('trend_24h', 'trend_16h', 0.8, "same signal"),
        ('trend_24h', 'trend_8h', 0.7, "redundant with regime variable"),
        ('trend_16h', 'trend_8h', 0.7, "redundant with regime variable"),
    ]
    for a, b, thresh, meaning in pairs:
        ia, ib = TREND_COLS.index(a), TREND_COLS.index(b)
        r = corr[ia, ib]
        flag = f"⚠ |r|>{thresh}" if abs(r) > thresh else "✓ independent"
        lines.append(f"    {a} vs {b}: r={r:+.3f}  {flag}  ({meaning if abs(r) > thresh else 'distinct signals'})")

    return lines


def analysis_2_operational_split(c2_df):
    """Operational split in P>0.80 logistic bin by trend sign."""
    lines = []
    lines.append("")
    lines.append("=" * 80)
    lines.append("  Analysis 2: Operational Split in P>0.80 Logistic Bin")
    lines.append("=" * 80)

    pb = p_bull(c2_df)
    mask_high = pb > 0.80
    high = c2_df[mask_high].copy()
    y_high = high['outcome'].values

    lines.append(f"  Total C2 episodes: {len(c2_df)}")
    lines.append(f"  P>0.80 episodes: {mask_high.sum()}")
    lines.append(f"  P>0.80 base rate: {y_high.mean():.1%}")
    lines.append("")

    for trend_col in ['trend_24h', 'trend_16h']:
        pos_mask = high[trend_col].values > 0
        neg_mask = ~pos_mask

        n_pos, n_neg = pos_mask.sum(), neg_mask.sum()
        s_pos = y_high[pos_mask].sum() if n_pos > 0 else 0
        s_neg = y_high[neg_mask].sum() if n_neg > 0 else 0
        r_pos = s_pos / n_pos if n_pos > 0 else float('nan')
        r_neg = s_neg / n_neg if n_neg > 0 else float('nan')

        lines.append(f"  ── Split by {trend_col} sign ──")
        lines.append(f"    {trend_col} > 0:  n={n_pos:>4d}  success={s_pos:>4d}  rate={r_pos:.1%}")
        lines.append(f"    {trend_col} ≤ 0:  n={n_neg:>4d}  success={s_neg:>4d}  rate={r_neg:.1%}")

        # Fisher exact test
        table = np.array([[s_pos, n_pos - s_pos],
                          [s_neg, n_neg - s_neg]])
        if table.min() >= 0 and n_pos > 0 and n_neg > 0:
            odds, p_val = stats.fisher_exact(table)
            lines.append(f"    Fisher exact: OR={odds:.2f}, p={p_val:.4f}")
        else:
            lines.append(f"    Fisher exact: insufficient data")
        lines.append("")

    return lines


def analysis_3_continuous_vs_binary(c2_df):
    """Within trend_24h sign groups, does magnitude matter?"""
    lines = []
    lines.append("=" * 80)
    lines.append("  Analysis 3: Continuous vs Binary (trend_24h magnitude within sign groups)")
    lines.append("=" * 80)
    lines.append("")

    y = c2_df['outcome'].values
    t24 = c2_df['trend_24h'].values

    for label, mask in [("trend_24h > 0", t24 > 0), ("trend_24h ≤ 0", t24 <= 0)]:
        x_sub = t24[mask]
        y_sub = y[mask]
        n = len(x_sub)
        n_pos = y_sub.sum()
        n_neg = n - n_pos

        auc = safe_auc(np.abs(x_sub), y_sub)

        lines.append(f"  ── {label} ──")
        lines.append(f"    n={n} (C3={n_pos}, C0={n_neg})")
        if np.isnan(auc):
            lines.append(f"    AUC of |trend_24h|: N/A (insufficient classes)")
        else:
            verdict = "magnitude matters" if auc > 0.60 else "sign is sufficient" if auc < 0.55 else "marginal"
            lines.append(f"    AUC of |trend_24h|: {auc:.3f} → {verdict}")
        lines.append("")

    return lines


def analysis_4_forward(fwd_path):
    """Forward data check."""
    lines = []
    lines.append("=" * 80)
    lines.append("  Analysis 4: Forward Data Check (Feb 20 – Mar 13, 2026)")
    lines.append("=" * 80)

    df = load_data(fwd_path)
    lines.append(f"  Loaded: {len(df)} bars (5-min), price {df['price'].min():.0f}–{df['price'].max():.0f}")

    assign_regime(df)
    episodes = detect_episodes(df)
    lines.append(f"  Episodes: {len(episodes)}")

    c2_df = extract_c2_episodes(df, episodes)
    n_total = len(c2_df)
    if n_total == 0:
        lines.append("  No C2 episodes with outcomes in forward period.")
        return lines

    n_success = c2_df['outcome'].sum()
    n_fail = n_total - n_success
    lines.append(f"  C2 episodes: {n_total} ({n_success} →C3, {n_fail} →C0)")
    lines.append(f"  Base rate: {n_success/n_total:.1%}")
    lines.append("")

    # trend_24h sign distribution
    t24_pos = (c2_df['trend_24h'] > 0).sum()
    t24_neg = n_total - t24_pos
    lines.append(f"  trend_24h sign: {t24_pos} positive, {t24_neg} non-positive")

    # Success rate by sign
    y = c2_df['outcome'].values
    t24 = c2_df['trend_24h'].values

    for label, mask in [("trend_24h > 0", t24 > 0), ("trend_24h ≤ 0", t24 <= 0)]:
        n = mask.sum()
        if n == 0:
            lines.append(f"    {label}: n=0")
            continue
        s = y[mask].sum()
        lines.append(f"    {label}: n={n}, success={s}, rate={s/n:.1%}")

    lines.append("")
    lines.append("  (Small n — directional confirmation only, not validation)")

    return lines


def analysis_5_stack_depth(c2_df):
    """Trend stack depth: count of positive intermediate trends."""
    lines = []
    lines.append("")
    lines.append("=" * 80)
    lines.append("  Analysis 5: Trend Stack Depth")
    lines.append("  stack_depth = count of {trend_4h > 0, trend_16h > 0, trend_24h > 0}")
    lines.append("=" * 80)
    lines.append("")

    depth = ((c2_df['trend_4h'] > 0).astype(int)
             + (c2_df['trend_16h'] > 0).astype(int)
             + (c2_df['trend_24h'] > 0).astype(int))
    y = c2_df['outcome'].values

    lines.append(f"  {'Depth':>5s}  {'n':>5s}  {'C3':>5s}  {'C0':>5s}  {'Rate':>7s}")
    lines.append(f"  {'-'*35}")

    for d in range(4):
        mask = depth == d
        n = mask.sum()
        if n == 0:
            lines.append(f"  {d:>5d}  {0:>5d}  {'-':>5s}  {'-':>5s}  {'-':>7s}")
            continue
        s = y[mask].sum()
        f = n - s
        rate = s / n
        lines.append(f"  {d:>5d}  {n:>5d}  {s:>5d}  {f:>5d}  {rate:>7.1%}")

    # Monotonicity check
    rates = []
    for d in range(4):
        mask = depth == d
        n = mask.sum()
        if n > 0:
            rates.append(y[mask].mean())
        else:
            rates.append(np.nan)

    valid_rates = [r for r in rates if not np.isnan(r)]
    if len(valid_rates) >= 3:
        monotone = all(a <= b for a, b in zip(valid_rates, valid_rates[1:]))
        lines.append(f"\n  Monotonic increase: {'Yes' if monotone else 'No'}")
        lines.append(f"  Rate range: {min(valid_rates):.1%} → {max(valid_rates):.1%}")

    return lines


def main():
    print("Loading IS data...", flush=True)
    df = load_data(IS_FILE)
    assign_regime(df)
    episodes = detect_episodes(df)
    c2_df = extract_c2_episodes(df, episodes)
    print(f"  {len(c2_df)} C2 episodes ({c2_df['outcome'].sum()} →C3, {len(c2_df) - c2_df['outcome'].sum()} →C0)")

    all_lines = []

    all_lines.extend(analysis_1_cross_correlation(c2_df))
    all_lines.extend(analysis_2_operational_split(c2_df))
    all_lines.extend(analysis_3_continuous_vs_binary(c2_df))
    all_lines.extend(analysis_4_forward(FWD_FILE))
    all_lines.extend(analysis_5_stack_depth(c2_df))

    all_lines.append("")
    all_lines.append("=" * 80)

    output = '\n'.join(all_lines)
    print(output)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)
    print(f"\nOutput saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
