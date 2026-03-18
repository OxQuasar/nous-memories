"""
Script 20: C1 Breakthrough EV Computation.

Final check: does the existing C1 logistic model identify a high-confidence
breakthrough bin where full-size anticipatory entry clears fees?

C1 entry is structurally different from C3: anticipatory (trend_8h positive,
trend_48h still negative, betting 48h follows) vs confirmatory.

Uses regime detection from scripts 17/18 (sign-based 2-bit, flicker debounce).
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score

# ─── CONFIG ───
DATA_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
OUTPUT_FILE = '/home/quasar/nous/memories/markets/20_c1_breakthrough_ev_output.txt'
SUBSAMPLE = 300  # 1s → 5min
FEE_RT = 0.18  # Round-trip fee %

# C1 logistic coefficients (simulator units — datalog trends are ~1e-5)
# Research: P(bt) = σ(−4.890 + 3138 × trend_1h + 421505 × trend_8h)
# Simulator trends are 10× smaller → multiply feature coefficients by 10
SCALE_FACTOR = 10.0
C1_INTERCEPT = -4.890
C1_COEF_T1H = 3138.0 * SCALE_FACTOR    # = 31380
C1_COEF_T8H = 421505.0 * SCALE_FACTOR  # = 4215050

# ─── COLUMN DEFINITIONS ───
CORE_COLS = {
    0: 'timestamp',
    2: 'price',
    32: 'trend_1h',
    34: 'trend_8h',
    37: 'trend_48h',
}

ALL_COLS = {**CORE_COLS}


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


def extract_c1_episodes(df, episodes):
    """Extract C1 episodes with logistic score, outcome, and price change."""
    records = []
    for i in range(len(episodes)):
        if episodes['regime'].iloc[i] != 1:  # C1 = reversal
            continue
        if i + 1 >= len(episodes):
            continue

        next_regime = episodes['regime'].iloc[i + 1]
        # C1 can go to C3 (breakthrough) or C0 (failure)
        if next_regime == 3:
            outcome = 1  # breakthrough
        elif next_regime == 0:
            outcome = 0  # failure
        else:
            continue  # guard

        entry_bar = episodes['start'].iloc[i]
        exit_bar = episodes['end'].iloc[i] - 1  # last bar of episode

        entry_price = df['price'].iloc[entry_bar]
        exit_price = df['price'].iloc[exit_bar]
        pct_change = (exit_price - entry_price) / entry_price * 100

        duration_bars = episodes['end'].iloc[i] - entry_bar
        duration_hours = duration_bars * 5 / 60  # 5-min bars

        t1h = df['trend_1h'].iloc[entry_bar]
        t8h = df['trend_8h'].iloc[entry_bar]

        # Logistic P(breakthrough) — simulator-scale coefficients
        logit = C1_INTERCEPT + C1_COEF_T1H * t1h + C1_COEF_T8H * t8h
        p_bt = sigmoid(logit)

        records.append({
            'outcome': outcome,
            'p_bt': p_bt,
            'pct_change': pct_change,
            'duration_h': duration_hours,
            'trend_1h': t1h,
            'trend_8h': t8h,
        })

    return pd.DataFrame(records)


def format_output(c1_df):
    """Format all output blocks."""
    lines = []
    n = len(c1_df)
    y = c1_df['outcome'].values
    n_bt = int(y.sum())
    n_fail = n - n_bt
    pct = c1_df['pct_change'].values
    dur = c1_df['duration_h'].values
    p_bt = c1_df['p_bt'].values

    bt_pct = pct[y == 1]
    fail_pct = pct[y == 0]
    bt_dur = dur[y == 1]
    fail_dur = dur[y == 0]

    # ── BLOCK 1 ──
    lines.append("=" * 100)
    lines.append("  Script 20: C1 Breakthrough EV Computation")
    lines.append("  Data: IS period Jul 2025 - Feb 2026")
    lines.append("=" * 100)
    lines.append("")
    lines.append("  BLOCK 1: C1 Episode Statistics")
    lines.append("-" * 100)
    lines.append(f"  Total C1 episodes: {n}")
    lines.append(f"  Breakthroughs (→C3): {n_bt} ({n_bt/n:.1%})")
    lines.append(f"  Failures (→C0):      {n_fail} ({n_fail/n:.1%})")
    lines.append("")
    lines.append(f"  Duration (hours):")
    lines.append(f"    All:          min={dur.min():.1f}  Q1={np.percentile(dur, 25):.1f}  "
                 f"median={np.median(dur):.1f}  Q3={np.percentile(dur, 75):.1f}  "
                 f"max={dur.max():.1f}  mean={dur.mean():.1f}")
    lines.append(f"    Breakthroughs: mean={bt_dur.mean():.1f}h  median={np.median(bt_dur):.1f}h  (n={n_bt})")
    lines.append(f"    Failures:      mean={fail_dur.mean():.1f}h  median={np.median(fail_dur):.1f}h  (n={n_fail})")
    lines.append("")
    lines.append(f"  Price change during C1 episode (%):")
    lines.append(f"    Breakthroughs: mean={bt_pct.mean():.3f}%  median={np.median(bt_pct):.3f}%  "
                 f"std={bt_pct.std():.3f}%")
    lines.append(f"    Failures:      mean={fail_pct.mean():.3f}%  median={np.median(fail_pct):.3f}%  "
                 f"std={fail_pct.std():.3f}%")
    lines.append(f"    Unconditional: mean={pct.mean():.3f}%")
    lines.append("")

    # ── BLOCK 2 ──
    lines.append("  BLOCK 2: Logistic Model Calibration Check")
    lines.append("-" * 100)

    # AUC
    try:
        auc = roc_auc_score(y, p_bt)
        lines.append(f"  Overall AUC: {auc:.3f}")
    except Exception:
        auc = float('nan')
        lines.append(f"  Overall AUC: N/A")
    lines.append("")

    # P(bt) distribution
    lines.append(f"  P(bt) distribution:")
    lines.append(f"    min={p_bt.min():.4f}  Q1={np.percentile(p_bt, 25):.4f}  "
                 f"median={np.median(p_bt):.4f}  Q3={np.percentile(p_bt, 75):.4f}  "
                 f"max={p_bt.max():.4f}")
    lines.append("")

    # Decile bins
    bin_edges = np.arange(0, 1.1, 0.1)
    lines.append(f"  {'Bin':<12s}  {'n':>5s}  {'BT rate':>8s}  {'Mean ΔP%':>9s}  {'BT mean':>9s}  {'Fail mean':>10s}")
    lines.append(f"  {'-'*65}")

    for j in range(len(bin_edges) - 1):
        lo, hi = bin_edges[j], bin_edges[j + 1]
        if j == len(bin_edges) - 2:
            mask = (p_bt >= lo) & (p_bt <= hi)
        else:
            mask = (p_bt >= lo) & (p_bt < hi)
        n_bin = mask.sum()
        if n_bin == 0:
            lines.append(f"  [{lo:.1f}, {hi:.1f})  {0:>5d}  {'—':>8s}  {'—':>9s}  {'—':>9s}  {'—':>10s}")
            continue
        bt_rate = y[mask].mean()
        mean_pct = pct[mask].mean()
        bt_mask = mask & (y == 1)
        fail_mask = mask & (y == 0)
        bt_mean = pct[bt_mask].mean() if bt_mask.sum() > 0 else float('nan')
        fail_mean = pct[fail_mask].mean() if fail_mask.sum() > 0 else float('nan')
        bt_str = f"{bt_mean:>+9.3f}" if not np.isnan(bt_mean) else f"{'—':>9s}"
        fail_str = f"{fail_mean:>+10.3f}" if not np.isnan(fail_mean) else f"{'—':>10s}"
        lines.append(f"  [{lo:.1f}, {hi:.1f})  {n_bin:>5d}  {bt_rate:>8.1%}  {mean_pct:>+9.3f}  {bt_str}  {fail_str}")

    lines.append("")

    # ── BLOCK 3 ──
    lines.append("  BLOCK 3: EV Computation by Confidence Threshold")
    lines.append("-" * 100)
    lines.append(f"  Fee: {FEE_RT:.2f}% round-trip")
    lines.append(f"  EV = (bt_rate × mean_bt_move) + ((1 - bt_rate) × mean_fail_move) - {FEE_RT}%")
    lines.append("")

    data_months = 7.0  # Jul 2025 - Feb 2026 ≈ 7 months

    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    lines.append(f"  {'Threshold':>9s}  {'n':>5s}  {'BT rate':>8s}  {'BT move':>8s}  "
                 f"{'Fail move':>9s}  {'EV':>8s}  {'EV>0?':>5s}  {'trades/mo':>9s}")
    lines.append(f"  {'-'*75}")

    for thr in thresholds:
        mask = p_bt >= thr
        n_thr = mask.sum()
        if n_thr < 3:
            lines.append(f"  P>{thr:.1f}      {n_thr:>5d}  {'—':>8s}  {'—':>8s}  {'—':>9s}  {'—':>8s}  {'—':>5s}  {'—':>9s}")
            continue
        bt_rate = y[mask].mean()
        bt_mask = mask & (y == 1)
        fail_mask = mask & (y == 0)
        mean_bt = pct[bt_mask].mean() if bt_mask.sum() > 0 else 0.0
        mean_fail = pct[fail_mask].mean() if fail_mask.sum() > 0 else 0.0
        ev = bt_rate * mean_bt + (1 - bt_rate) * mean_fail - FEE_RT
        positive = 'YES' if ev > 0 else 'NO'
        trades_per_month = n_thr / data_months

        lines.append(f"  P>{thr:.1f}      {n_thr:>5d}  {bt_rate:>8.1%}  {mean_bt:>+8.3f}  "
                     f"{mean_fail:>+9.3f}  {ev:>+8.3f}  {positive:>5s}  {trades_per_month:>9.1f}")

    lines.append("")

    # Baseline
    bt_rate_all = y.mean()
    ev_all = bt_rate_all * bt_pct.mean() + (1 - bt_rate_all) * fail_pct.mean() - FEE_RT
    lines.append(f"  Baseline (all C1): n={n}, BT rate={bt_rate_all:.1%}, "
                 f"BT move={bt_pct.mean():+.3f}%, Fail move={fail_pct.mean():+.3f}%, "
                 f"EV={ev_all:+.3f}%")
    lines.append("")

    # ── BLOCK 4 ──
    lines.append("  BLOCK 4: Practical Assessment")
    lines.append("-" * 100)

    # Find best threshold with n >= 5
    best_ev = -999
    best_thr = None
    for thr in thresholds:
        mask = p_bt >= thr
        n_thr = mask.sum()
        if n_thr < 5:
            continue
        bt_rate = y[mask].mean()
        bt_mask = mask & (y == 1)
        fail_mask = mask & (y == 0)
        mean_bt = pct[bt_mask].mean() if bt_mask.sum() > 0 else 0.0
        mean_fail = pct[fail_mask].mean() if fail_mask.sum() > 0 else 0.0
        ev = bt_rate * mean_bt + (1 - bt_rate) * mean_fail - FEE_RT
        if ev > best_ev:
            best_ev = ev
            best_thr = thr

    any_positive = best_ev > 0

    if any_positive:
        mask = p_bt >= best_thr
        n_best = mask.sum()
        bt_rate_best = y[mask].mean()
        lines.append(f"  POSITIVE EV FOUND at P>{best_thr:.1f}")
        lines.append(f"    n={n_best} trades, BT rate={bt_rate_best:.1%}, EV={best_ev:+.3f}%/trade")
        lines.append(f"    Expected: {n_best/data_months:.1f} trades/month")
        lines.append(f"    Expected monthly EV: {n_best/data_months * best_ev:+.3f}%")
        lines.append("")
        lines.append("  CAVEATS:")
        lines.append("    - This measures C1 episode price change only (entry at C1 start, exit at C1 end)")
        lines.append("    - Does NOT include potential C3 continuation")
        lines.append("    - In-sample: logistic was fit on OOS 2023-2024 data, tested here on IS 2025-2026")
        lines.append("    - v3.2 used P>0.50 with 0.5 exposure and produced -13.38% — but that had")
        lines.append("      interaction effects with the long logic. This evaluates C1 trades in isolation.")
        lines.append("    - Small n in high-confidence bins: results are noisy")
    else:
        lines.append("  NO POSITIVE EV at any threshold (n>=5).")
        if best_thr is not None:
            lines.append(f"  Best threshold: P>{best_thr:.1f} with EV={best_ev:+.3f}%")
        lines.append("")
        lines.append("  The C1 breakthrough logistic model classifies outcomes but the")
        lines.append("  price moves during C1 episodes do not generate positive EV")
        lines.append("  even in the highest-confidence bins.")

    lines.append("")

    # Key insight
    lines.append("  COMPARISON TO v3.2")
    lines.append("  v3.2 entered C1 at 0.5 exposure when P(bt)>0.50: -13.38% over 16 weeks")
    lines.append("  That failure had two causes:")
    lines.append("    1. Interaction: 0.5 exposure in C1 degraded subsequent C3 capture")
    lines.append("    2. Fee drag: 72 C1 trades x 0.18% = 12.96% in fees alone")
    lines.append("  This script evaluates C1 in ISOLATION (no interaction) and at FULL SIZE")
    lines.append(f"  Result: {'Positive' if any_positive else 'Negative'} EV in isolation")
    lines.append("")

    lines.append("=" * 100)
    lines.append("  VERDICT")
    lines.append("=" * 100)
    if any_positive:
        lines.append("  C1 anticipatory entry shows positive EV in isolation at high confidence.")
        lines.append("  However, small n in high-confidence bins means this needs validation.")
        lines.append("  Next step: verify in simulator as a standalone trade type.")
    else:
        lines.append("  C1 anticipatory entry has NO POSITIVE EV even in isolation.")
        lines.append("  The regime model is a validated state classifier that does not produce")
        lines.append("  a tradeable directional strategy at current fees and timescales.")
        lines.append("  Its value is in state classification (risk labeling, sizing) not trade generation.")
    lines.append("")
    lines.append("=" * 100)

    return '\n'.join(lines)


def main():
    print("Loading data...", flush=True)
    df = load_data(DATA_FILE)
    print(f"  {len(df)} bars (5-min), price {df['price'].min():.0f}-{df['price'].max():.0f}")

    print("Assigning regimes...", flush=True)
    assign_regime(df)
    episodes = detect_episodes(df)
    print(f"  {len(episodes)} episodes detected")

    print("Extracting C1 episodes...", flush=True)
    c1_df = extract_c1_episodes(df, episodes)
    n_total = len(c1_df)
    n_bt = int(c1_df['outcome'].sum())
    print(f"  {n_total} C1 episodes ({n_bt} breakthroughs, {n_total - n_bt} failures)")

    output = format_output(c1_df)
    print(output)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)
    print(f"\nOutput saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
