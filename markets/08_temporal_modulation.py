#!/usr/bin/env python3
"""Phase 8: Temporal Modulation of Regime Transition Probabilities.

Tests whether the 4-regime directed cycle varies systematically by
time-of-day or day-of-week. If transitions are time-invariant, regime
dynamics are a market-structural property, not a calendar artifact.

Basis A: trend_1h × trend_8h × trend_48h → 8 states S0–S7.
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path("/home/quasar/nous/memories/markets/datalog_2025-07-21_2026-02-20.csv")
OUTPUT_DIR = Path("/home/quasar/nous/memories/markets")
DOWNSAMPLE_MS = 300_000

NEEDED_COLS = ["timestamp", "price", "trend_1h", "trend_8h", "trend_48h"]

STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
MACRO_LABELS = ["C0 bear", "C1 reversal", "C2 pullback", "C3 bull"]
N_MACRO = 4

# Trading session blocks (6h each, UTC)
BLOCK_LABELS = ["Asia (00-05)", "Europe (06-11)", "US (12-17)", "Evening (18-23)"]
N_BLOCKS = 4
DOW_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ─── Data Loading ────────────────────────────────────────────────────────────

def load_and_downsample():
    print("Loading and downsampling to 5-minute bars...")
    chunks = []
    for chunk in pd.read_csv(DATA_PATH, usecols=NEEDED_COLS, chunksize=500_000):
        chunk["bar"] = chunk["timestamp"] // DOWNSAMPLE_MS
        chunks.append(chunk.groupby("bar").last().reset_index())
    df = pd.concat(chunks, ignore_index=True)
    df = df.groupby("bar").last().reset_index()
    df = df.sort_values("bar").reset_index(drop=True)
    # Derive temporal columns from timestamp (ms → UTC)
    dt = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df["utc_hour"] = dt.dt.hour
    df["dow"] = dt.dt.dayofweek  # Mon=0, Sun=6
    df["block"] = df["utc_hour"] // 6  # 0=Asia, 1=Europe, 2=US, 3=Evening
    print(f"  Rows: {len(df)}")
    return df


# ─── Helpers ─────────────────────────────────────────────────────────────────

def compute_states(df):
    mask = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    states_8 = ((bdf["trend_48h"] > 0).astype(int) * 4
                + (bdf["trend_8h"] > 0).astype(int) * 2
                + (bdf["trend_1h"] > 0).astype(int)).values
    macro = np.array([STATE_TO_MACRO[s] for s in states_8])
    return bdf, states_8, macro


def jump_chain_from_counts(count_matrix):
    """Row-normalized jump chain (diagonal zeroed)."""
    J = count_matrix.astype(float).copy()
    np.fill_diagonal(J, 0)
    row_sums = J.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return J / row_sums


def extract_episodes(macro_states, states_8, prices, extra_cols=None):
    """Extract regime episodes. extra_cols: dict of name → array, sampled at episode boundaries."""
    n = len(macro_states)
    episodes = []
    i = 0
    while i < n:
        macro_val = macro_states[i]
        start = i
        while i < n and macro_states[i] == macro_val:
            i += 1
        end = i - 1
        truncated = (start == 0) or (end == n - 1)
        exit_dest = macro_states[i] if i < n else -1
        ep = {
            "macro": macro_val,
            "duration": end - start + 1,
            "entry_sub": states_8[start],
            "exit_sub": states_8[end],
            "exit_dest": exit_dest,
            "entry_price": prices[start],
            "exit_price": prices[end],
            "log_return": np.log(prices[end] / prices[start]) if prices[start] > 0 else 0,
            "start_idx": start,
            "end_idx": end,
            "truncated": truncated,
        }
        if extra_cols:
            for name, arr in extra_cols.items():
                ep[f"exit_{name}"] = arr[end]
                ep[f"start_{name}"] = arr[start]
        episodes.append(ep)
    return episodes


def format_matrix(M, labels, decimals=3):
    w = max(len(l) for l in labels)
    header = " " * (w + 2) + "".join(f"{l:>{w+2}}" for l in labels)
    lines = [header]
    for i, l in enumerate(labels):
        row = f"{l:<{w+2}}" + "".join(f"{M[i,j]:>{w+2}.{decimals}f}" for j in range(M.shape[1]))
        lines.append(row)
    return "\n".join(lines)


def wilson_ci(count, n, z=1.96):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = count / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    spread = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return p, max(0, center - spread), min(1, center + spread)


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 1: Time-Tagged Transitions
# ═══════════════════════════════════════════════════════════════════════════

def step1_tagged_transitions(bdf, states_8, macro, episodes):
    print("\n" + "=" * 70)
    print("  STEP 1: Time-Tagged Transitions")
    print("=" * 70)

    clean = [e for e in episodes if not e["truncated"]]
    print(f"  Total episodes: {len(episodes)}, clean: {len(clean)}")

    # Each transition = end of one episode / start of next
    # Tag by temporal info at the transition bar (first bar of new regime)
    transitions = []
    for e in clean:
        if e["exit_dest"] < 0:
            continue
        # The transition bar is end_idx + 1 (first bar of next regime)
        trans_idx = e["end_idx"] + 1
        if trans_idx >= len(bdf):
            continue
        transitions.append({
            "src": e["macro"],
            "dst": e["exit_dest"],
            "exit_sub": e["exit_sub"],
            "utc_hour": bdf["utc_hour"].iloc[trans_idx],
            "dow": bdf["dow"].iloc[trans_idx],
            "block": bdf["block"].iloc[trans_idx],
            "duration": e["duration"],
            "log_return": e["log_return"],
        })

    print(f"  Tagged transitions: {len(transitions)}")

    # Distribution by block
    print(f"\n  Transitions by time block:")
    for b in range(N_BLOCKS):
        n = sum(1 for t in transitions if t["block"] == b)
        print(f"    {BLOCK_LABELS[b]}: {n} ({n/len(transitions)*100:.1f}%)")

    # Distribution by DOW
    print(f"\n  Transitions by day of week:")
    for d in range(7):
        n = sum(1 for t in transitions if t["dow"] == d)
        print(f"    {DOW_LABELS[d]}: {n} ({n/len(transitions)*100:.1f}%)")

    # Distribution by hour (24h histogram)
    print(f"\n  Transitions by UTC hour:")
    hour_counts = np.zeros(24, dtype=int)
    for t in transitions:
        hour_counts[t["utc_hour"]] += 1
    for h in range(24):
        bar = "█" * (hour_counts[h] // 2)
        print(f"    {h:02d}:00  {hour_counts[h]:>4}  {bar}")

    return transitions


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 2: Hourly Modulation of J₄
# ═══════════════════════════════════════════════════════════════════════════

def step2_hourly_j4(transitions):
    print("\n" + "=" * 70)
    print("  STEP 2: J₄ by Time Block")
    print("=" * 70)

    # Global J₄ from transitions
    global_counts = np.zeros((N_MACRO, N_MACRO))
    for t in transitions:
        global_counts[t["src"], t["dst"]] += 1
    J_global = jump_chain_from_counts(global_counts)

    clabels = [f"C{i}" for i in range(N_MACRO)]
    print(f"\n--- Global J₄ (from {len(transitions)} transitions) ---")
    print(format_matrix(J_global, clabels))

    # Per-block J₄
    block_Js = []
    block_counts = []
    for b in range(N_BLOCKS):
        bc = np.zeros((N_MACRO, N_MACRO))
        for t in transitions:
            if t["block"] == b:
                bc[t["src"], t["dst"]] += 1
        J_b = jump_chain_from_counts(bc)
        block_Js.append(J_b)
        block_counts.append(bc)

        print(f"\n--- J₄ Block {b}: {BLOCK_LABELS[b]} (n={int(bc.sum())}) ---")
        print(format_matrix(J_b, clabels))

        frob = np.linalg.norm(J_b - J_global, "fro")
        print(f"  ‖J₄_block - J₄_global‖_F = {frob:.4f}")

    # Structural zeros check
    print(f"\n--- Structural Zero Persistence ---")
    # Forbidden: C0→C3, C1→C2, C2→C1, C3→C0
    forbidden = [(0, 3), (1, 2), (2, 1), (3, 0)]
    for src, dst in forbidden:
        vals = [block_counts[b][src, dst] for b in range(N_BLOCKS)]
        total = sum(vals)
        print(f"  C{src}→C{dst}: total={total}  by block: {vals}  "
              f"{'ZERO HOLDS' if total <= 3 else 'BROKEN (n=' + str(total) + ')'}")

    # Chi-squared test per non-forbidden transition
    print(f"\n--- Chi-Squared Tests: Transition Rate × Block Independence ---")
    print(f"  H₀: transition probability is independent of time block")
    print(f"  {'Transition':>12}  {'χ²':>8}  {'p-value':>10}  {'Result':>20}")

    non_forbidden = [(i, j) for i in range(N_MACRO) for j in range(N_MACRO)
                     if i != j and (i, j) not in forbidden]

    any_significant = False
    for src, dst in non_forbidden:
        # Contingency table: rows = blocks, cols = [this transition, other transitions from src]
        table = np.zeros((N_BLOCKS, 2))
        for b in range(N_BLOCKS):
            this_count = block_counts[b][src, dst]
            other_count = sum(block_counts[b][src, d] for d in range(N_MACRO) if d != src and d != dst)
            table[b] = [this_count, other_count]

        # Skip if any row is all zeros or table is degenerate
        if table.sum() < 10 or np.any(table.sum(axis=1) == 0):
            print(f"  C{src}→C{dst}:  {'N/A':>8}  {'N/A':>10}  insufficient data")
            continue

        try:
            chi2, p, dof, expected = chi2_contingency(table)
            sig = "SIGNIFICANT *" if p < 0.05 else "not significant"
            if p < 0.05:
                any_significant = True
            print(f"  C{src}→C{dst}:  {chi2:>8.3f}  {p:>10.4f}  {sig}")
        except ValueError:
            print(f"  C{src}→C{dst}:  {'N/A':>8}  {'N/A':>10}  degenerate")

    if not any_significant:
        print(f"\n  → No transition shows significant time-block dependence (all p > 0.05)")
    else:
        print(f"\n  → Some transitions show significant time-block modulation")

    return J_global, block_Js, block_counts


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 3: Exit Sub-State Signal by Time Block
# ═══════════════════════════════════════════════════════════════════════════

def step3_exit_substate_by_block(transitions):
    print("\n" + "=" * 70)
    print("  STEP 3: C2 Exit Sub-State Signal by Time Block")
    print("=" * 70)

    # C2 exits: src=2
    c2_exits = [t for t in transitions if t["src"] == 2]
    print(f"  Total C2 exits: {len(c2_exits)}")

    # Check if we have enough data per block
    block_n = [sum(1 for t in c2_exits if t["block"] == b) for b in range(N_BLOCKS)]
    use_2blocks = any(n < 15 for n in block_n)

    if use_2blocks:
        print(f"  Block counts: {block_n} — some < 15, using 2 blocks instead")
        block_defs = [(0, [0, 1], "00-11 UTC"), (1, [2, 3], "12-23 UTC")]
    else:
        print(f"  Block counts: {block_n} — using 4 blocks")
        block_defs = [(b, [b], BLOCK_LABELS[b]) for b in range(N_BLOCKS)]

    # S5 and S4 exit rates by block
    print(f"\n  {'Block':>20}  {'Sub':>4}  {'n':>5}  {'→Bull':>6}  {'→Bear':>6}  "
          f"{'Bull%':>7}  {'95% CI':>18}")

    for block_id, block_vals, block_label in block_defs:
        for sub in [5, 4]:
            subset = [t for t in c2_exits if t["block"] in block_vals and t["exit_sub"] == sub]
            n = len(subset)
            if n == 0:
                print(f"  {block_label:>20}   S{sub}  {n:>5}  {'—':>6}  {'—':>6}  {'—':>7}  {'—':>18}")
                continue
            to_bull = sum(1 for t in subset if t["dst"] == 3)
            to_bear = sum(1 for t in subset if t["dst"] == 0)
            p, lo, hi = wilson_ci(to_bull, n)
            print(f"  {block_label:>20}   S{sub}  {n:>5}  {to_bull:>6}  {to_bear:>6}  "
                  f"{p*100:>6.1f}%  [{lo*100:.1f}%, {hi*100:.1f}%]")

    # Global reference
    print(f"\n  Global reference:")
    for sub in [5, 4]:
        subset = [t for t in c2_exits if t["exit_sub"] == sub]
        n = len(subset)
        to_bull = sum(1 for t in subset if t["dst"] == 3)
        p, lo, hi = wilson_ci(to_bull, n)
        print(f"  {'Global':>20}   S{sub}  {n:>5}  {to_bull:>6}  "
              f"{'':>6}  {p*100:>6.1f}%  [{lo*100:.1f}%, {hi*100:.1f}%]")

    # Chi-squared: S5→bull rate independent of block?
    print(f"\n  Chi-squared: S5→bull rate × block independence")
    s5_exits = [t for t in c2_exits if t["exit_sub"] == 5]
    table = np.zeros((len(block_defs), 2))
    for bi, (_, block_vals, _) in enumerate(block_defs):
        subset = [t for t in s5_exits if t["block"] in block_vals]
        to_bull = sum(1 for t in subset if t["dst"] == 3)
        to_bear = len(subset) - to_bull
        table[bi] = [to_bull, to_bear]

    if table.sum() >= 10 and np.all(table.sum(axis=1) > 0):
        try:
            chi2, p, dof, _ = chi2_contingency(table)
            print(f"    χ²={chi2:.3f}, p={p:.4f} — {'SIGNIFICANT' if p < 0.05 else 'not significant'}")
        except ValueError:
            print(f"    Degenerate table")
    else:
        print(f"    Insufficient data")

    # Also test S4
    print(f"\n  Chi-squared: S4→bull rate × block independence")
    s4_exits = [t for t in c2_exits if t["exit_sub"] == 4]
    table = np.zeros((len(block_defs), 2))
    for bi, (_, block_vals, _) in enumerate(block_defs):
        subset = [t for t in s4_exits if t["block"] in block_vals]
        to_bull = sum(1 for t in subset if t["dst"] == 3)
        to_bear = len(subset) - to_bull
        table[bi] = [to_bull, to_bear]

    if table.sum() >= 10 and np.all(table.sum(axis=1) > 0):
        try:
            chi2, p, dof, _ = chi2_contingency(table)
            print(f"    χ²={chi2:.3f}, p={p:.4f} — {'SIGNIFICANT' if p < 0.05 else 'not significant'}")
        except ValueError:
            print(f"    Degenerate table")
    else:
        print(f"    Insufficient data")


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 4: Day-of-Week Effects
# ═══════════════════════════════════════════════════════════════════════════

def step4_dow(transitions):
    print("\n" + "=" * 70)
    print("  STEP 4: Day-of-Week Effects")
    print("=" * 70)

    # Weekday vs Weekend J₄
    for label, dow_set in [("Weekday (Mon-Fri)", {0, 1, 2, 3, 4}), ("Weekend (Sat-Sun)", {5, 6})]:
        counts = np.zeros((N_MACRO, N_MACRO))
        for t in transitions:
            if t["dow"] in dow_set:
                counts[t["src"], t["dst"]] += 1
        J = jump_chain_from_counts(counts)
        clabels = [f"C{i}" for i in range(N_MACRO)]
        print(f"\n--- J₄ {label} (n={int(counts.sum())}) ---")
        print(format_matrix(J, clabels))

    # Frobenius distance weekday vs weekend
    wd_counts = np.zeros((N_MACRO, N_MACRO))
    we_counts = np.zeros((N_MACRO, N_MACRO))
    for t in transitions:
        if t["dow"] < 5:
            wd_counts[t["src"], t["dst"]] += 1
        else:
            we_counts[t["src"], t["dst"]] += 1
    J_wd = jump_chain_from_counts(wd_counts)
    J_we = jump_chain_from_counts(we_counts)
    frob = np.linalg.norm(J_wd - J_we, "fro")
    print(f"\n  ‖J₄_weekday - J₄_weekend‖_F = {frob:.4f}")

    # Duration by DOW
    print(f"\n--- Mean Episode Duration by Day of Week (bars × 5min) ---")
    print(f"  {'DOW':>5}  {'Transitions':>12}  {'Mean Dur (bars)':>16}  {'Mean Dur (h)':>13}")
    for d in range(7):
        subset = [t for t in transitions if t["dow"] == d]
        if not subset:
            print(f"  {DOW_LABELS[d]:>5}  {0:>12}  {'—':>16}  {'—':>13}")
            continue
        durs = [t["duration"] for t in subset]
        mean_d = np.mean(durs)
        print(f"  {DOW_LABELS[d]:>5}  {len(subset):>12}  {mean_d:>16.1f}  {mean_d*5/60:>13.1f}")

    # Transition rate by DOW — transitions per bar
    print(f"\n--- Transition Rate by Day of Week ---")
    # We need total bars per DOW for this — approximate from transition counts
    # Actually we can compute from the transition durations
    for d in range(7):
        subset = [t for t in transitions if t["dow"] == d]
        n_trans = len(subset)
        total_bars = sum(t["duration"] for t in subset)
        rate = n_trans / total_bars if total_bars > 0 else 0
        print(f"  {DOW_LABELS[d]:>5}: {n_trans} transitions, {total_bars} bars in source regimes, "
              f"rate = {rate:.4f} trans/bar ({1/rate:.0f} bars/trans)" if rate > 0 else
              f"  {DOW_LABELS[d]:>5}: {n_trans} transitions")


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 5: Regime Duration by Starting Hour
# ═══════════════════════════════════════════════════════════════════════════

def step5_duration_by_start_hour(transitions, episodes, bdf):
    print("\n" + "=" * 70)
    print("  STEP 5: Regime Duration by Starting Hour")
    print("=" * 70)

    clean = [e for e in episodes if not e["truncated"]]

    # Tag episodes with start hour
    for e in clean:
        e["start_hour"] = bdf["utc_hour"].iloc[e["start_idx"]]
        e["start_block"] = bdf["block"].iloc[e["start_idx"]]

    # Mean duration by start block, per regime
    print(f"\n--- Mean Duration (hours) by Start Block ---")
    print(f"  {'Block':>20}  {'C0 bear':>10}  {'C1 rev':>10}  {'C2 pull':>10}  {'C3 bull':>10}  {'All':>10}")
    for b in range(N_BLOCKS):
        vals = []
        for m in range(N_MACRO):
            subset = [e for e in clean if e["start_block"] == b and e["macro"] == m]
            if subset:
                mean_h = np.mean([e["duration"] for e in subset]) * 5 / 60
                vals.append(f"{mean_h:>10.1f}")
            else:
                vals.append(f"{'—':>10}")
        all_subset = [e for e in clean if e["start_block"] == b]
        all_mean = np.mean([e["duration"] for e in all_subset]) * 5 / 60 if all_subset else 0
        print(f"  {BLOCK_LABELS[b]:>20}  {'  '.join(vals)}  {all_mean:>10.1f}")

    # Transition hour histogram — when do regime changes happen?
    print(f"\n--- Transition Hour Histogram (preferred times for regime changes) ---")
    hour_counts = np.zeros(24, dtype=int)
    for t in transitions:
        hour_counts[t["utc_hour"]] += 1
    mean_per_hour = hour_counts.mean()
    for h in range(24):
        dev = (hour_counts[h] - mean_per_hour) / mean_per_hour * 100
        bar = "█" * max(0, int(hour_counts[h] / 2))
        flag = " ▲" if dev > 20 else " ▼" if dev < -20 else ""
        print(f"    {h:02d}:00  {hour_counts[h]:>4}  ({dev:>+6.1f}%)  {bar}{flag}")

    # Chi-squared: are transitions uniformly distributed across hours?
    print(f"\n  Chi-squared: uniform distribution of transitions across 4 blocks")
    block_counts = np.array([sum(1 for t in transitions if t["block"] == b) for b in range(N_BLOCKS)])
    expected = np.full(N_BLOCKS, len(transitions) / N_BLOCKS)
    chi2 = np.sum((block_counts - expected) ** 2 / expected)
    from scipy.stats import chi2 as chi2_dist
    p = 1 - chi2_dist.cdf(chi2, df=N_BLOCKS - 1)
    print(f"    Block counts: {block_counts}")
    print(f"    Expected (uniform): {expected[0]:.1f}")
    print(f"    χ²={chi2:.3f}, p={p:.4f} — {'SIGNIFICANT' if p < 0.05 else 'not significant'}")


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 6: Summary
# ═══════════════════════════════════════════════════════════════════════════

def step6_summary(transitions, block_Js, J_global):
    print("\n" + "=" * 70)
    print("  STEP 6: Summary")
    print("=" * 70)

    # Frobenius norms
    frobs = [np.linalg.norm(block_Js[b] - J_global, "fro") for b in range(N_BLOCKS)]
    print(f"\n  Frobenius distance from global J₄:")
    for b in range(N_BLOCKS):
        print(f"    {BLOCK_LABELS[b]}: {frobs[b]:.4f}")
    print(f"    Mean: {np.mean(frobs):.4f}, Max: {np.max(frobs):.4f}")

    # Compare to subperiod stability from Phase 2 (those were 0.03–0.12)
    print(f"\n  Context: Phase 2 subperiod stability Frobenius norms were 0.03–0.12")
    max_frob = np.max(frobs)
    if max_frob < 0.12:
        print(f"  → Time-block variation ({max_frob:.4f}) is WITHIN subperiod variation range")
        print(f"  → No evidence of systematic temporal modulation")
    else:
        print(f"  → Time-block variation ({max_frob:.4f}) EXCEEDS subperiod variation range")
        print(f"  → Possible systematic temporal modulation")

    # Key transition comparison across blocks
    print(f"\n  Key transition probabilities by block:")
    key_trans = [(0, 1, "C0→C1"), (1, 0, "C1→C0"), (1, 3, "C1→C3"),
                 (2, 3, "C2→C3"), (2, 0, "C2→C0"), (3, 2, "C3→C2")]
    print(f"  {'Trans':>8}  {'Global':>8}  " +
          "  ".join(f"{BLOCK_LABELS[b]:>15}" for b in range(N_BLOCKS)))
    for src, dst, label in key_trans:
        global_p = J_global[src, dst]
        block_ps = [block_Js[b][src, dst] for b in range(N_BLOCKS)]
        block_strs = "  ".join(f"{p:>15.3f}" for p in block_ps)
        print(f"  {label:>8}  {global_p:>8.3f}  {block_strs}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()
    bdf, states_8, macro = compute_states(df)
    prices = bdf["price"].values

    episodes = extract_episodes(macro, states_8, prices,
                                extra_cols={"block": bdf["block"].values,
                                            "utc_hour": bdf["utc_hour"].values,
                                            "dow": bdf["dow"].values})

    # Step 1
    transitions = step1_tagged_transitions(bdf, states_8, macro, episodes)

    # Step 2
    J_global, block_Js, block_counts = step2_hourly_j4(transitions)

    # Step 3
    step3_exit_substate_by_block(transitions)

    # Step 4
    step4_dow(transitions)

    # Step 5
    step5_duration_by_start_hour(transitions, episodes, bdf)

    # Step 6
    step6_summary(transitions, block_Js, J_global)

    print(f"\n{'=' * 70}")
    print("  Phase 8 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
