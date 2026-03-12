#!/usr/bin/env python3
"""Phase 4: Regime-Conditioned Returns & Duration Analysis.

Analyzes predictive content of Basis A 8-state regime labels:
- Part 1: Duration analysis per macro-regime
- Part 2: Exit destination with confidence intervals
- Part 3: Price returns conditioned on regime
- Part 4: Cross-basis contingency (Basis A × Basis D)
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent / "datalog_2025-07-21_2026-02-20.csv"
OUTPUT_DIR = Path(__file__).parent
DOWNSAMPLE_MS = 300_000

NEEDED_COLS = [
    "timestamp", "price",
    "trend_1h", "trend_8h", "trend_48h",     # Basis A
    "tot_8h", "realized_vol_8h",              # Basis D
]

N_STATES = 8
N_MACRO = 4
N_SUBPERIODS = 3

# Basis A macro-regimes: cluster = b₂*2 + b₁ (slow bits)
STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
MACRO_LABELS = ["C0 bear", "C1 reversal", "C2 pullback", "C3 bull"]
MACRO_MEMBERS = {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7]}

# Basis D complement-pair clusters
COMPLEMENT_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]
STATE_TO_CPAIR = {}
for idx, (a, b) in enumerate(COMPLEMENT_PAIRS):
    STATE_TO_CPAIR[a] = idx
    STATE_TO_CPAIR[b] = idx
CPAIR_LABELS = ["P0", "P1", "P2", "P3"]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def wilson_ci(count, n, z=1.96):
    """Wilson score confidence interval for a proportion."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = count / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    spread = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return p, max(0, center - spread), min(1, center + spread)


def pct_str(vals, percentiles=(25, 50, 75)):
    """Format percentile summary."""
    pcts = np.percentile(vals, percentiles)
    return f"mean={np.mean(vals):.1f}  p25={pcts[0]:.1f}  median={pcts[1]:.1f}  p75={pcts[2]:.1f}  max={np.max(vals):.0f}"


def extract_episodes(macro_states, states_8, prices):
    """Extract regime episodes from macro-state sequence.

    Returns list of dicts:
      {macro, duration, entry_sub, exit_sub, exit_dest, entry_price, exit_price,
       start_idx, end_idx, truncated}
    """
    n = len(macro_states)
    episodes = []
    i = 0
    while i < n:
        macro = macro_states[i]
        start = i
        while i < n and macro_states[i] == macro:
            i += 1
        end = i - 1  # last bar in this regime

        truncated = (start == 0) or (end == n - 1)
        exit_dest = macro_states[i] if i < n else -1

        episodes.append({
            "macro": macro,
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
        })
    return episodes


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
    print(f"  Rows: {len(df)}")
    return df


# ═══════════════════════════════════════════════════════════════════════════
#  PART 1: Duration Analysis
# ═══════════════════════════════════════════════════════════════════════════

def part1_duration(episodes):
    print(f"\n{'=' * 70}")
    print("  PART 1: Regime Duration Analysis")
    print(f"{'=' * 70}")

    # Exclude truncated episodes
    clean = [e for e in episodes if not e["truncated"]]
    print(f"  Total episodes: {len(episodes)} ({len(episodes) - len(clean)} truncated, excluded)")
    print(f"  Clean episodes: {len(clean)}")

    for m in range(N_MACRO):
        eps = [e for e in clean if e["macro"] == m]
        if not eps:
            continue
        members = MACRO_MEMBERS[m]
        durs = np.array([e["duration"] for e in eps])

        print(f"\n--- {MACRO_LABELS[m]} ({len(eps)} episodes) ---")

        # 1. Overall duration
        print(f"  Duration (bars): {pct_str(durs)}")
        print(f"  Duration (hours): mean={np.mean(durs)*5/60:.1f}h  median={np.median(durs)*5/60:.1f}h")

        # 2. Duration by exit destination
        print(f"\n  Duration by exit destination:")
        for dest in range(N_MACRO):
            if dest == m:
                continue
            dest_eps = [e for e in eps if e["exit_dest"] == dest]
            if not dest_eps:
                continue
            d = np.array([e["duration"] for e in dest_eps])
            print(f"    → {MACRO_LABELS[dest]} (n={len(dest_eps)}): {pct_str(d)}")

        # 3. Duration by last sub-state
        print(f"\n  Duration by last sub-state (exit bar):")
        for sub in members:
            sub_eps = [e for e in eps if e["exit_sub"] == sub]
            if not sub_eps:
                continue
            d = np.array([e["duration"] for e in sub_eps])
            print(f"    S{sub} (n={len(sub_eps)}): {pct_str(d)}")


# ═══════════════════════════════════════════════════════════════════════════
#  PART 2: Exit Destination with Confidence
# ═══════════════════════════════════════════════════════════════════════════

def part2_exit_analysis(episodes, macro_states, states_8):
    print(f"\n{'=' * 70}")
    print("  PART 2: Exit Destination Analysis with Confidence")
    print(f"{'=' * 70}")

    clean = [e for e in episodes if not e["truncated"]]

    for m in range(N_MACRO):
        eps = [e for e in clean if e["macro"] == m]
        if not eps:
            continue
        members = MACRO_MEMBERS[m]
        dests = [d for d in range(N_MACRO) if d != m]
        dest_labels = [MACRO_LABELS[d] for d in dests]

        print(f"\n--- {MACRO_LABELS[m]} ---")
        print(f"  Exit probability by last sub-state (95% Wilson CI):")

        header = f"  {'Sub':>4}  {'n':>5}  " + "  ".join(f"{MACRO_LABELS[d]:>20}" for d in dests)
        print(header)

        for sub in members:
            sub_eps = [e for e in eps if e["exit_sub"] == sub]
            n = len(sub_eps)
            if n == 0:
                print(f"  S{sub:>3}  {'N/A':>5}")
                continue
            cells = []
            for d in dests:
                count = sum(1 for e in sub_eps if e["exit_dest"] == d)
                p, lo, hi = wilson_ci(count, n)
                cells.append(f"{p:.3f} [{lo:.3f},{hi:.3f}]")
            print(f"  S{sub:>3}  {n:>5}  " + "  ".join(f"{c:>20}" for c in cells))

    # C2 subperiod stability
    print(f"\n--- C2 Pullback: Subperiod Stability of Exit Splits ---")
    c2_eps = [e for e in clean if e["macro"] == 2]
    n_total = len(c2_eps)
    splits = np.array_split(range(len(c2_eps)), N_SUBPERIODS)

    for k in range(N_SUBPERIODS):
        sub_indices = splits[k]
        sub_eps = [c2_eps[i] for i in sub_indices]
        print(f"\n  Subperiod {k + 1} ({len(sub_eps)} C2 episodes):")
        for sub in MACRO_MEMBERS[2]:
            sub_sub = [e for e in sub_eps if e["exit_sub"] == sub]
            n = len(sub_sub)
            if n == 0:
                print(f"    S{sub}: no exits")
                continue
            to_bear = sum(1 for e in sub_sub if e["exit_dest"] == 0)
            to_bull = sum(1 for e in sub_sub if e["exit_dest"] == 3)
            to_other = n - to_bear - to_bull
            p_bear, _, _ = wilson_ci(to_bear, n)
            p_bull, _, _ = wilson_ci(to_bull, n)
            print(f"    S{sub} (n={n}): → bear={p_bear:.3f} ({to_bear})  "
                  f"→ bull={p_bull:.3f} ({to_bull})  → other={to_other}")


# ═══════════════════════════════════════════════════════════════════════════
#  PART 3: Price Returns
# ═══════════════════════════════════════════════════════════════════════════

def part3_returns(episodes):
    print(f"\n{'=' * 70}")
    print("  PART 3: Price Returns Conditioned on Regime")
    print(f"{'=' * 70}")

    clean = [e for e in episodes if not e["truncated"]]

    for m in range(N_MACRO):
        eps = [e for e in clean if e["macro"] == m]
        if not eps:
            continue
        members = MACRO_MEMBERS[m]
        dests = [d for d in range(N_MACRO) if d != m]

        rets = np.array([e["log_return"] for e in eps])
        durs = np.array([e["duration"] for e in eps])

        print(f"\n--- {MACRO_LABELS[m]} ({len(eps)} episodes) ---")
        print(f"  Log return: mean={np.mean(rets)*100:.4f}%  median={np.median(rets)*100:.4f}%  "
              f"std={np.std(rets)*100:.4f}%  skew={float(pd.Series(rets).skew()):.3f}")
        mean_dur = np.mean(durs)
        print(f"  Return per bar: {np.mean(rets)/mean_dur*100:.6f}%  "
              f"(regime velocity: {np.mean(rets)/mean_dur*100*12:.4f}%/hr)")

        # By exit destination
        print(f"\n  Returns by exit destination:")
        for d in dests:
            dest_eps = [e for e in eps if e["exit_dest"] == d]
            if not dest_eps:
                continue
            dr = np.array([e["log_return"] for e in dest_eps])
            dd = np.array([e["duration"] for e in dest_eps])
            print(f"    → {MACRO_LABELS[d]} (n={len(dest_eps)}): "
                  f"mean={np.mean(dr)*100:.4f}%  median={np.median(dr)*100:.4f}%  "
                  f"std={np.std(dr)*100:.4f}%  ret/bar={np.mean(dr)/np.mean(dd)*100:.6f}%")

        # For C2 specifically: by last sub-state
        if m == 2:
            print(f"\n  C2 returns by last sub-state:")
            for sub in members:
                sub_eps = [e for e in eps if e["exit_sub"] == sub]
                if not sub_eps:
                    continue
                sr = np.array([e["log_return"] for e in sub_eps])
                sd = np.array([e["duration"] for e in sub_eps])
                print(f"    S{sub} (n={len(sub_eps)}): "
                      f"mean={np.mean(sr)*100:.4f}%  median={np.median(sr)*100:.4f}%  "
                      f"std={np.std(sr)*100:.4f}%  mean_dur={np.mean(sd):.1f}bars  "
                      f"ret/bar={np.mean(sr)/np.mean(sd)*100:.6f}%")
                # Further split by destination
                for d in dests:
                    dd_eps = [e for e in sub_eps if e["exit_dest"] == d]
                    if not dd_eps:
                        continue
                    ddr = np.array([e["log_return"] for e in dd_eps])
                    ddd = np.array([e["duration"] for e in dd_eps])
                    print(f"      → {MACRO_LABELS[d]} (n={len(dd_eps)}): "
                          f"mean={np.mean(ddr)*100:.4f}%  dur={np.mean(ddd):.1f}bars")


# ═══════════════════════════════════════════════════════════════════════════
#  PART 4: Cross-Basis Contingency
# ═══════════════════════════════════════════════════════════════════════════

def part4_contingency(macro_states, cpair_states):
    print(f"\n{'=' * 70}")
    print("  PART 4: Cross-Basis Contingency (Basis A × Basis D)")
    print(f"{'=' * 70}")

    n = len(macro_states)
    table = np.zeros((N_MACRO, 4))
    for i in range(n):
        table[macro_states[i], cpair_states[i]] += 1
    table_pct = table / n * 100

    print(f"\n  Contingency table (% of all bars):")
    header = f"  {'':>15}" + "".join(f"{CPAIR_LABELS[j]:>10}" for j in range(4)) + f"{'Total':>10}"
    print(header)
    for m in range(N_MACRO):
        row = f"  {MACRO_LABELS[m]:>15}" + "".join(f"{table_pct[m, j]:>9.2f}%" for j in range(4))
        row += f"{table_pct[m].sum():>9.2f}%"
        print(row)
    col_sums = table_pct.sum(axis=0)
    total_row = f"  {'Total':>15}" + "".join(f"{col_sums[j]:>9.2f}%" for j in range(4)) + f"{col_sums.sum():>9.2f}%"
    print(total_row)

    # Conditional: P(Basis D | Basis A)
    print(f"\n  P(Basis D cluster | Basis A regime):")
    header2 = f"  {'':>15}" + "".join(f"{CPAIR_LABELS[j]:>10}" for j in range(4))
    print(header2)
    for m in range(N_MACRO):
        row_sum = table[m].sum()
        if row_sum == 0:
            continue
        cond = table[m] / row_sum * 100
        print(f"  {MACRO_LABELS[m]:>15}" + "".join(f"{cond[j]:>9.2f}%" for j in range(4)))


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()

    # Basis A states
    features_a = ["trend_1h", "trend_8h", "trend_48h"]
    mask = df[features_a].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    states_8 = ((bdf["trend_48h"] > 0).astype(int) * 4
                + (bdf["trend_8h"] > 0).astype(int) * 2
                + (bdf["trend_1h"] > 0).astype(int)).values
    macro_states = np.array([STATE_TO_MACRO[s] for s in states_8])
    prices = bdf["price"].values

    print(f"  Working rows: {len(bdf)}")
    print(f"  Price range: {prices.min():.0f} → {prices.max():.0f}")

    # Extract episodes
    episodes = extract_episodes(macro_states, states_8, prices)
    print(f"  Total regime episodes: {len(episodes)}")

    part1_duration(episodes)
    part2_exit_analysis(episodes, macro_states, states_8)
    part3_returns(episodes)

    # Basis D states for contingency
    features_d = ["tot_8h", "trend_8h", "realized_vol_8h"]
    mask_d = bdf[features_d].notna().all(axis=1)
    vol_median = bdf["realized_vol_8h"].median()
    states_d = ((bdf["realized_vol_8h"] > vol_median).astype(int) * 4
                + (bdf["trend_8h"] > 0).astype(int) * 2
                + (bdf["tot_8h"] > 0).astype(int)).values
    cpair_states = np.array([STATE_TO_CPAIR[s] for s in states_d])
    part4_contingency(macro_states, cpair_states)

    print(f"\n{'=' * 70}")
    print("  Phase 4 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
