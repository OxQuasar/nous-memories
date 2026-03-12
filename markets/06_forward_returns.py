#!/usr/bin/env python3
"""Phase 6: Forward-Looking Returns — Does the exit sub-state of the
previous regime predict returns/duration in the next regime?
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent / "datalog_2025-07-21_2026-02-20.csv"
OUTPUT_DIR = Path(__file__).parent
DOWNSAMPLE_MS = 300_000

NEEDED_COLS = ["timestamp", "price", "trend_1h", "trend_8h", "trend_48h"]

STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
MACRO_LABELS = ["C0 bear", "C1 reversal", "C2 pullback", "C3 bull"]
N_MACRO = 4


# ─── Helpers ─────────────────────────────────────────────────────────────────

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


def extract_episodes(macro_states, states_8, prices):
    n = len(macro_states)
    episodes = []
    i = 0
    while i < n:
        macro = macro_states[i]
        start = i
        while i < n and macro_states[i] == macro:
            i += 1
        end = i - 1
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


def ret_stats(eps_list, label=""):
    """Print return/duration statistics for a list of episodes."""
    if not eps_list:
        print(f"    {label}: n=0")
        return
    rets = np.array([e["log_return"] for e in eps_list])
    durs = np.array([e["duration"] for e in eps_list])
    print(f"    {label} (n={len(eps_list)}): "
          f"ret mean={np.mean(rets)*100:+.4f}%  median={np.median(rets)*100:+.4f}%  "
          f"std={np.std(rets)*100:.4f}%  "
          f"dur mean={np.mean(durs):.0f}bars ({np.mean(durs)*5/60:.1f}h)")


# ─── Analysis ────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()

    features = ["trend_1h", "trend_8h", "trend_48h"]
    mask = df[features].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    states_8 = ((bdf["trend_48h"] > 0).astype(int) * 4
                + (bdf["trend_8h"] > 0).astype(int) * 2
                + (bdf["trend_1h"] > 0).astype(int)).values
    macro_states = np.array([STATE_TO_MACRO[s] for s in states_8])
    prices = bdf["price"].values

    episodes = extract_episodes(macro_states, states_8, prices)
    clean = [e for e in episodes if not e["truncated"]]
    print(f"  Clean episodes: {len(clean)}")

    # Build linked list: for each episode, record the prior episode's exit info
    linked = []
    for i in range(1, len(clean)):
        prev = clean[i - 1]
        curr = clean[i]
        # Ensure adjacency (prev.end_idx + 1 == curr.start_idx)
        if prev["end_idx"] + 1 != curr["start_idx"]:
            continue
        linked.append({
            **curr,
            "src_macro": prev["macro"],
            "src_exit_sub": prev["exit_sub"],
        })

    print(f"  Linked episode pairs: {len(linked)}")

    # ═══════════════════════════════════════════════════════════════════
    #  A. C2 → C3 (pullback resolving to bull)
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("  A. C3 Bull Episodes — By Entry Source")
    print(f"{'=' * 70}")

    c3_from_c2_s5 = [e for e in linked if e["macro"] == 3 and e["src_macro"] == 2 and e["src_exit_sub"] == 5]
    c3_from_c2_s4 = [e for e in linked if e["macro"] == 3 and e["src_macro"] == 2 and e["src_exit_sub"] == 4]
    c3_from_c1 = [e for e in linked if e["macro"] == 3 and e["src_macro"] == 1]
    c3_all = [e for e in linked if e["macro"] == 3]

    ret_stats(c3_from_c2_s5, "C2-S5 → C3 (confirmed pullback)")
    ret_stats(c3_from_c2_s4, "C2-S4 → C3 (uncertain pullback)")
    ret_stats(c3_from_c1,    "C1    → C3 (reversal breakthrough)")
    ret_stats(c3_all,        "All C3 episodes")

    # ═══════════════════════════════════════════════════════════════════
    #  B. C2 → C0 (pullback failing to bear)
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("  B. C0 Bear Episodes — By Entry Source")
    print(f"{'=' * 70}")

    c0_from_c2_s4 = [e for e in linked if e["macro"] == 0 and e["src_macro"] == 2 and e["src_exit_sub"] == 4]
    c0_from_c2_s5 = [e for e in linked if e["macro"] == 0 and e["src_macro"] == 2 and e["src_exit_sub"] == 5]
    c0_from_c3 = [e for e in linked if e["macro"] == 0 and e["src_macro"] == 3]
    c0_from_c1 = [e for e in linked if e["macro"] == 0 and e["src_macro"] == 1]
    c0_all = [e for e in linked if e["macro"] == 0]

    ret_stats(c0_from_c2_s4, "C2-S4 → C0 (failed pullback, uncertain)")
    ret_stats(c0_from_c2_s5, "C2-S5 → C0 (failed pullback, was confirmed)")
    ret_stats(c0_from_c1,    "C1    → C0 (reversal failure)")
    ret_stats(c0_from_c3,    "C3    → C0 (bull → bear, rare)")
    ret_stats(c0_all,        "All C0 episodes")

    # ═══════════════════════════════════════════════════════════════════
    #  C. All Transitions Summary
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("  C. All Transitions Summary (n ≥ 5)")
    print(f"{'=' * 70}")

    print(f"\n  {'Source':>15} {'ExitSub':>8} {'→':>2} {'Dest':>15} {'n':>5} "
          f"{'MeanRet':>10} {'MedRet':>10} {'MeanDur':>10}")
    print(f"  {'-'*15} {'-'*8} {'-'*2} {'-'*15} {'-'*5} {'-'*10} {'-'*10} {'-'*10}")

    # Group by (src_macro, src_exit_sub, macro)
    groups = {}
    for e in linked:
        key = (e["src_macro"], e["src_exit_sub"], e["macro"])
        groups.setdefault(key, []).append(e)

    for (src_m, src_sub, dest_m), eps in sorted(groups.items()):
        if len(eps) < 5:
            continue
        rets = np.array([e["log_return"] for e in eps])
        durs = np.array([e["duration"] for e in eps])
        print(f"  {MACRO_LABELS[src_m]:>15} S{src_sub:>6} → {MACRO_LABELS[dest_m]:>15} "
              f"{len(eps):>5} {np.mean(rets)*100:>+9.4f}% {np.median(rets)*100:>+9.4f}% "
              f"{np.mean(durs):>9.0f}b")

    # ═══════════════════════════════════════════════════════════════════
    #  D. Zero-Flip C2 Episodes
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("  D. Zero-Flip C2 Episodes (entered S5, never went to S4)")
    print(f"{'=' * 70}")

    c2_clean = [e for e in clean if e["macro"] == 2]
    zero_flip = []
    for e in c2_clean:
        s = states_8[e["start_idx"]:e["end_idx"] + 1]
        has_s4 = np.any(s == 4)
        if not has_s4 and e["entry_sub"] == 5:
            zero_flip.append(e)

    if zero_flip:
        to_bull = sum(1 for e in zero_flip if e["exit_dest"] == 3)
        to_bear = sum(1 for e in zero_flip if e["exit_dest"] == 0)
        rets = np.array([e["log_return"] for e in zero_flip])
        durs = np.array([e["duration"] for e in zero_flip])
        print(f"  n={len(zero_flip)}: → bull={to_bull} ({to_bull/len(zero_flip)*100:.0f}%)  "
              f"→ bear={to_bear} ({to_bear/len(zero_flip)*100:.0f}%)")
        print(f"  Mean return: {np.mean(rets)*100:+.4f}%  Mean duration: {np.mean(durs):.1f} bars ({np.mean(durs)*5/60:.1f}h)")
    else:
        print("  None found.")

    print(f"\n{'=' * 70}")
    print("  Phase 6 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
