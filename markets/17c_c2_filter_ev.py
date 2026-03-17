"""
Script 17c: C2 Exit Filter Expected Value.

Computes the EV of filtering C2 episodes based on trend_24h sign
and stack_depth, using actual price changes during C2 episodes.
"""

import numpy as np
import pandas as pd
from scipy import stats

# ─── CONFIG ───
IS_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
OUTPUT_FILE = '/home/quasar/nous/memories/markets/17c_c2_filter_ev_output.txt'
SUBSAMPLE = 300  # 1s → 5min
FEE_RT_PCT = 0.36  # round-trip fee per filtered episode

# Columns needed (0-indexed)
COLS = {
    0: 'timestamp', 2: 'price',
    32: 'trend_1h', 33: 'trend_4h', 34: 'trend_8h',
    35: 'trend_16h', 36: 'trend_24h', 37: 'trend_48h',
}
SNAPSHOT_COLS = ['trend_1h', 'trend_4h', 'trend_8h', 'trend_16h', 'trend_24h', 'trend_48h']


# ─── DATA LOADING / REGIME DETECTION (from 17/17b) ───

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


def extract_c2_episodes_with_price(df, episodes):
    """Extract C2 episodes with entry/exit prices and indicator snapshots."""
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
        exit_bar = episodes['start'].iloc[i + 1]
        entry_price = df['price'].iloc[entry_bar]
        exit_price = df['price'].iloc[exit_bar]
        pct_change = (exit_price - entry_price) / entry_price * 100

        row = {
            'outcome': outcome,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'pct_change': pct_change,
        }
        for col in SNAPSHOT_COLS:
            row[col] = df[col].iloc[entry_bar]

        # Derived: stack depth
        row['stack_depth'] = int(row['trend_4h'] > 0) + int(row['trend_16h'] > 0) + int(row['trend_24h'] > 0)

        records.append(row)

    return pd.DataFrame(records)


# ─── FILTER EV COMPUTATION ───

def compute_filter_ev(c2_df, filter_mask, filter_name):
    """Compute EV for a filter that exits at C2 entry when filter_mask is True.

    Returns (lines, ev_total) for output formatting and comparison.
    """
    lines = []
    y = c2_df['outcome'].values
    pct = c2_df['pct_change'].values

    filtered = c2_df[filter_mask]
    kept = c2_df[~filter_mask]

    # Group A: filtered + C0 (losses caught)
    grp_a = filtered[filtered['outcome'] == 0]
    # Group B: filtered + C3 (false positives — missed recoveries)
    grp_b = filtered[filtered['outcome'] == 1]
    # Group C: not filtered (kept)
    grp_c = kept

    n_filtered = len(filtered)
    n_a, n_b, n_c = len(grp_a), len(grp_b), len(grp_c)

    lines.append(f"  Filter: {filter_name}")
    lines.append(f"  Filtered: {n_filtered} episodes | Kept: {len(kept)} episodes")
    lines.append("")

    # Group A: losses avoided
    a_pct = grp_a['pct_change'].values
    loss_avoided = np.abs(a_pct).sum() if n_a > 0 else 0.0
    lines.append(f"  Group A — Losses caught ({filter_name}, outcome=C0):")
    lines.append(f"    Count: {n_a}")
    if n_a > 0:
        lines.append(f"    Mean decline: {a_pct.mean():+.3f}%")
        lines.append(f"    Median decline: {np.median(a_pct):+.3f}%")
        lines.append(f"    Total |decline| avoided: {loss_avoided:.3f}%")
    lines.append("")

    # Group B: missed recoveries
    b_pct = grp_b['pct_change'].values
    recovery_missed = b_pct.sum() if n_b > 0 else 0.0
    lines.append(f"  Group B — False positives ({filter_name}, outcome=C3):")
    lines.append(f"    Count: {n_b}")
    if n_b > 0:
        lines.append(f"    Mean C2 gain: {b_pct.mean():+.3f}%")
        lines.append(f"    Median C2 gain: {np.median(b_pct):+.3f}%")
        lines.append(f"    Total recovery missed: {recovery_missed:.3f}%")
    lines.append("")

    # Group C: baseline (unfiltered)
    c_pct = grp_c['pct_change'].values
    lines.append(f"  Group C — Kept episodes (not filtered):")
    lines.append(f"    Count: {n_c} (C3={grp_c['outcome'].sum()}, C0={n_c - grp_c['outcome'].sum()})")
    if n_c > 0:
        lines.append(f"    Mean change: {c_pct.mean():+.3f}%")
        lines.append(f"    Total change: {c_pct.sum():+.3f}%")
    lines.append("")

    # EV calculation
    fee_cost = n_filtered * FEE_RT_PCT
    filter_ev = loss_avoided - recovery_missed - fee_cost

    lines.append(f"  ── Expected Value ──")
    lines.append(f"    Loss avoided (A):       +{loss_avoided:.3f}%")
    lines.append(f"    Recovery missed (B):     -{recovery_missed:.3f}%")
    lines.append(f"    Fee cost ({n_filtered} × {FEE_RT_PCT}%): -{fee_cost:.3f}%")
    lines.append(f"    ─────────────────────────────────")
    lines.append(f"    Filter EV (total):       {filter_ev:+.3f}%")
    if n_filtered > 0:
        lines.append(f"    Filter EV (per filtered): {filter_ev / n_filtered:+.3f}%")
    lines.append("")

    # Comparison: hold all vs filter
    hold_all_pnl = pct.sum()
    filter_pnl = hold_all_pnl + filter_ev  # add back avoided losses, subtract missed gains + fees
    lines.append(f"  ── Comparison ──")
    lines.append(f"    Hold all C2 total PnL:   {hold_all_pnl:+.3f}%")
    lines.append(f"    Filter bad C2 total PnL: {filter_pnl:+.3f}%")
    lines.append(f"    Improvement:             {filter_ev:+.3f}%")

    return lines, filter_ev


# ─── MAIN ───

def main():
    print("Loading IS data...", flush=True)
    df = load_data(IS_FILE)
    assign_regime(df)
    episodes = detect_episodes(df)
    c2_df = extract_c2_episodes_with_price(df, episodes)
    n_total = len(c2_df)
    n_success = c2_df['outcome'].sum()
    print(f"  {n_total} C2 episodes ({n_success} →C3, {n_total - n_success} →C0)")

    out = []

    # ── Per-episode table for filtered population (trend_24h ≤ 0) ──
    out.append("=" * 100)
    out.append("  C2 Filter EV Study")
    out.append("=" * 100)
    out.append(f"  IS data: {n_total} C2 episodes ({n_success} →C3, {n_total - n_success} →C0)")
    out.append(f"  Fee assumption: {FEE_RT_PCT}% per round-trip")
    out.append("")

    filtered_pop = c2_df[c2_df['trend_24h'] <= 0].copy()
    out.append("─" * 100)
    out.append("  Per-Episode Detail: trend_24h ≤ 0 (filtered population)")
    out.append("─" * 100)
    out.append(f"  {'#':>3s}  {'Entry':>8s}  {'Exit':>8s}  {'Chg%':>7s}  {'t24h':>12s}  {'Outcome':>8s}")
    out.append(f"  {'─'*55}")

    for idx, (_, row) in enumerate(filtered_pop.iterrows(), 1):
        label = 'C3' if row['outcome'] == 1 else 'C0'
        out.append(f"  {idx:>3d}  {row['entry_price']:>8.0f}  {row['exit_price']:>8.0f}  "
                   f"{row['pct_change']:>+7.3f}  {row['trend_24h']:>12.2e}  {label:>8s}")

    out.append("")

    # ── Filter 1: trend_24h ≤ 0 ──
    out.append("=" * 100)
    out.append("  FILTER 1: trend_24h ≤ 0")
    out.append("=" * 100)
    mask_t24 = c2_df['trend_24h'] <= 0
    lines_t24, ev_t24 = compute_filter_ev(c2_df, mask_t24, "trend_24h ≤ 0")
    out.extend(lines_t24)

    # ── Filter 2: stack_depth < 2 ──
    out.append("")
    out.append("=" * 100)
    out.append("  FILTER 2: stack_depth < 2")
    out.append("  stack_depth = count of {trend_4h > 0, trend_16h > 0, trend_24h > 0}")
    out.append("=" * 100)
    mask_stack = c2_df['stack_depth'] < 2
    lines_stack, ev_stack = compute_filter_ev(c2_df, mask_stack, "stack_depth < 2")
    out.extend(lines_stack)

    # ── Filter comparison ──
    out.append("")
    out.append("=" * 100)
    out.append("  FILTER COMPARISON")
    out.append("=" * 100)
    out.append(f"  trend_24h ≤ 0:   EV = {ev_t24:+.3f}%  (filters {mask_t24.sum()} episodes)")
    out.append(f"  stack_depth < 2: EV = {ev_stack:+.3f}%  (filters {mask_stack.sum()} episodes)")
    winner = "trend_24h ≤ 0" if ev_t24 > ev_stack else "stack_depth < 2"
    out.append(f"  Winner: {winner}")

    out.append("")
    out.append("  NOTE: C2-only price change is a lower bound on total loss avoided —")
    out.append("  C0 continuation losses not included. For C2→C0 failures, the strategy")
    out.append("  continues losing through C0 until C0→C1 reversal detection.")

    out.append("")
    out.append("=" * 100)

    output = '\n'.join(out)
    print(output)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)
    print(f"\nOutput saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
