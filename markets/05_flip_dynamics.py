#!/usr/bin/env python3
"""Phase 5: Intra-Episode Flip Dynamics (C2 Pullback + C1 Reversal).

Studies how the fast bit (trend_1h) flips within regime episodes and
whether those flips are actionable trading triggers.
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

CONFIRM_BARS = 3          # bars to confirm a flip
RETURN_HORIZONS = [5, 10, 20, 50]


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


def extract_episodes(macro_states, states_8, prices):
    """Extract regime episodes (reused from Phase 4)."""
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


# ─── Flip Extraction ────────────────────────────────────────────────────────

def find_flips(states_8, prices, start_idx, end_idx, from_state, to_state):
    """Find all from_state→to_state transitions within [start_idx, end_idx].

    Returns list of dicts: {bar_idx, price, is_confirmed, hold_length}
    - bar_idx: index of the bar where to_state first appears
    - is_confirmed: whether the state stays as to_state for ≥CONFIRM_BARS bars
    - hold_length: how many consecutive bars in to_state after the flip
    """
    flips = []
    i = start_idx + 1  # can't flip at the very first bar
    while i <= end_idx:
        if states_8[i] == to_state and states_8[i - 1] == from_state:
            flip_bar = i
            # Count consecutive bars in to_state
            hold = 0
            j = i
            while j <= end_idx and states_8[j] == to_state:
                hold += 1
                j += 1
            is_confirmed = hold >= CONFIRM_BARS
            flips.append({
                "bar_idx": flip_bar,
                "price": prices[flip_bar],
                "is_confirmed": is_confirmed,
                "hold_length": hold,
            })
            i = j  # skip past this run
        else:
            i += 1
    return flips


def cumulative_returns(prices, flip_bar, episode_end, horizons):
    """Compute log returns at specified horizons after flip_bar."""
    p0 = prices[flip_bar]
    results = {}
    for h in horizons:
        target = min(flip_bar + h, episode_end)
        actual_h = target - flip_bar
        ret = np.log(prices[target] / p0) if p0 > 0 else 0
        results[h] = (ret, actual_h, target <= episode_end)
    return results


# ═══════════════════════════════════════════════════════════════════════════
#  PART 1: C2 Pullback Flip Analysis
# ═══════════════════════════════════════════════════════════════════════════

def part1_c2_flips(episodes, states_8, prices, macro_states):
    print(f"\n{'=' * 70}")
    print("  PART 1: Intra-Episode Flip Analysis — C2 Pullback")
    print(f"{'=' * 70}")

    clean_c2 = [e for e in episodes if e["macro"] == 2 and not e["truncated"]]
    print(f"  C2 episodes (non-truncated): {len(clean_c2)}")

    # ── 1a: Entry State Distribution ─────────────────────────────────────
    print(f"\n--- 1a. Entry State Distribution ---")
    entry_s4 = [e for e in clean_c2 if e["entry_sub"] == 4]
    entry_s5 = [e for e in clean_c2 if e["entry_sub"] == 5]
    print(f"  Enter as S4 (trend_1h↓): {len(entry_s4)} ({len(entry_s4)/len(clean_c2)*100:.1f}%)")
    print(f"  Enter as S5 (trend_1h↑): {len(entry_s5)} ({len(entry_s5)/len(clean_c2)*100:.1f}%)")

    # Entry state → exit destination
    print(f"\n  Entry state → exit destination:")
    for entry_sub, label, group in [(4, "S4", entry_s4), (5, "S5", entry_s5)]:
        if not group:
            continue
        to_bear = sum(1 for e in group if e["exit_dest"] == 0)
        to_bull = sum(1 for e in group if e["exit_dest"] == 3)
        n = len(group)
        durs = np.array([e["duration"] for e in group])
        print(f"    {label} entry (n={n}): → bear={to_bear/n:.3f}  → bull={to_bull/n:.3f}  "
              f"mean_dur={np.mean(durs):.1f} bars")

    # ── 1b: Flip Count Per Episode ───────────────────────────────────────
    print(f"\n--- 1b. Flip Count Per Episode ---")
    flip_counts = []
    unflip_counts = []
    for e in clean_c2:
        s = states_8[e["start_idx"]:e["end_idx"] + 1]
        flips = sum(1 for i in range(len(s) - 1) if s[i] == 4 and s[i + 1] == 5)
        unflips = sum(1 for i in range(len(s) - 1) if s[i] == 5 and s[i + 1] == 4)
        flip_counts.append(flips)
        unflip_counts.append(unflips)
    flip_counts = np.array(flip_counts)
    unflip_counts = np.array(unflip_counts)

    print(f"  S4→S5 flips:  mean={np.mean(flip_counts):.2f}  median={np.median(flip_counts):.0f}  "
          f"min={np.min(flip_counts)}  max={np.max(flip_counts)}")
    print(f"  S5→S4 unflips: mean={np.mean(unflip_counts):.2f}  median={np.median(unflip_counts):.0f}  "
          f"min={np.min(unflip_counts)}  max={np.max(unflip_counts)}")

    zero_flip = np.sum(flip_counts == 0)
    print(f"  Episodes with 0 flips: {zero_flip} ({zero_flip/len(clean_c2)*100:.1f}%) — entered as S5, never went to S4")

    # Split by exit destination
    print(f"\n  Flip count by exit destination:")
    for dest, label in [(0, "bear"), (3, "bull")]:
        dest_idx = [i for i, e in enumerate(clean_c2) if e["exit_dest"] == dest]
        if not dest_idx:
            continue
        fc = flip_counts[dest_idx]
        print(f"    → {label} (n={len(dest_idx)}): mean={np.mean(fc):.2f}  median={np.median(fc):.0f}")

    # ── 1c: Return Profile Relative to Flips ─────────────────────────────
    print(f"\n--- 1c. Return Profile: S4→S5 Flips ---")

    all_flips = []
    for e in clean_c2:
        flips = find_flips(states_8, prices, e["start_idx"], e["end_idx"], 4, 5)
        for f in flips:
            f["episode_end"] = e["end_idx"]
            f["exit_dest"] = e["exit_dest"]
        all_flips.extend(flips)

    holds = [f for f in all_flips if f["is_confirmed"]]
    chatters = [f for f in all_flips if not f["is_confirmed"]]
    print(f"  Total S4→S5 flips: {len(all_flips)}")
    print(f"  Holds (≥{CONFIRM_BARS} bars): {len(holds)} ({len(holds)/max(1,len(all_flips))*100:.1f}%)")
    print(f"  Chatters (<{CONFIRM_BARS} bars): {len(chatters)} ({len(chatters)/max(1,len(all_flips))*100:.1f}%)")

    # Cumulative returns
    print(f"\n  Cumulative return profile after flip:")
    header = f"  {'Bars':>6}  {'Holds':>14} (n={len(holds)})  {'Chatters':>14} (n={len(chatters)})  {'All':>14} (n={len(all_flips)})"
    print(header)

    for h in RETURN_HORIZONS:
        for group, label in [(holds, "holds"), (chatters, "chatters"), (all_flips, "all")]:
            rets = []
            for f in group:
                cr = cumulative_returns(prices, f["bar_idx"], f["episode_end"], [h])
                rets.append(cr[h][0])
            if label == "holds":
                h_ret = np.mean(rets) * 100 if rets else 0
                h_str = f"{h_ret:+.4f}%"
            elif label == "chatters":
                c_ret = np.mean(rets) * 100 if rets else 0
                c_str = f"{c_ret:+.4f}%"
            else:
                a_ret = np.mean(rets) * 100 if rets else 0
                a_str = f"{a_ret:+.4f}%"
        print(f"  {'+' + str(h):>6}  {h_str:>20}  {c_str:>20}  {a_str:>20}")

    # ── 1d: Return at the FINAL Flip ─────────────────────────────────────
    print(f"\n--- 1d. Return at FINAL S4→S5 Flip ---")
    print(f"  (For episodes exiting C2 in state S5)")

    s5_exit_eps = [e for e in clean_c2 if e["exit_sub"] == 5]
    print(f"  S5-exit episodes: {len(s5_exit_eps)}")

    final_flip_data = []
    for e in s5_exit_eps:
        flips = find_flips(states_8, prices, e["start_idx"], e["end_idx"], 4, 5)
        if not flips:
            # Entered as S5, never went to S4 — no flip to analyze
            continue
        last_flip = flips[-1]
        ret_after = np.log(prices[e["end_idx"]] / last_flip["price"]) if last_flip["price"] > 0 else 0
        ret_before = np.log(last_flip["price"] / prices[e["start_idx"]]) if prices[e["start_idx"]] > 0 else 0
        total_ret = e["log_return"]
        bars_after = e["end_idx"] - last_flip["bar_idx"]
        final_flip_data.append({
            "ret_after": ret_after,
            "ret_before": ret_before,
            "total_ret": total_ret,
            "bars_after": bars_after,
            "exit_dest": e["exit_dest"],
        })

    no_flip = len(s5_exit_eps) - len(final_flip_data)
    print(f"  Episodes with ≥1 flip: {len(final_flip_data)}  (no flip: {no_flip})")

    if final_flip_data:
        ret_after = np.array([d["ret_after"] for d in final_flip_data])
        ret_before = np.array([d["ret_before"] for d in final_flip_data])
        total_ret = np.array([d["total_ret"] for d in final_flip_data])
        bars_after = np.array([d["bars_after"] for d in final_flip_data])

        # Fraction of return after final flip
        # Only meaningful where total_ret != 0
        nonzero = total_ret != 0
        if nonzero.sum() > 0:
            frac_after = ret_after[nonzero] / total_ret[nonzero]
            print(f"\n  Return breakdown (n={len(final_flip_data)}):")
            print(f"    Return before final flip: mean={np.mean(ret_before)*100:+.4f}%  "
                  f"median={np.median(ret_before)*100:+.4f}%")
            print(f"    Return after final flip:  mean={np.mean(ret_after)*100:+.4f}%  "
                  f"median={np.median(ret_after)*100:+.4f}%")
            print(f"    Total episode return:     mean={np.mean(total_ret)*100:+.4f}%  "
                  f"median={np.median(total_ret)*100:+.4f}%")
            print(f"    Bars from final flip to exit: mean={np.mean(bars_after):.1f}  "
                  f"median={np.median(bars_after):.0f}")

        # By exit destination
        print(f"\n  Final flip returns by exit destination:")
        for dest, label in [(0, "bear"), (3, "bull")]:
            dff = [d for d in final_flip_data if d["exit_dest"] == dest]
            if not dff:
                continue
            ra = np.array([d["ret_after"] for d in dff])
            ba = np.array([d["bars_after"] for d in dff])
            print(f"    → {label} (n={len(dff)}): ret_after={np.mean(ra)*100:+.4f}%  "
                  f"bars_after={np.mean(ba):.1f}")

    # ── 1e: Confirmed-Flip Trading Simulation ────────────────────────────
    print(f"\n--- 1e. Confirmed-Flip Trading Simulation ---")
    print(f"  Rule: enter long when S4→S5 persists ≥{CONFIRM_BARS} bars.")
    print(f"  Exit: next S5→S4 reversal OR C2 regime exit (whichever first).")

    trades = []
    for e in clean_c2:
        flips = find_flips(states_8, prices, e["start_idx"], e["end_idx"], 4, 5)
        for f in flips:
            if not f["is_confirmed"]:
                continue
            entry_bar = f["bar_idx"] + CONFIRM_BARS - 1  # confirmation bar
            if entry_bar > e["end_idx"]:
                continue
            entry_price = prices[entry_bar]

            # Find exit: next S5→S4 reversal or episode end
            exit_bar = entry_bar
            j = entry_bar + 1
            while j <= e["end_idx"]:
                if states_8[j] == 4 and states_8[j - 1] == 5:
                    exit_bar = j - 1  # last S5 bar before reversal
                    break
                j += 1
            else:
                exit_bar = e["end_idx"]  # held through episode exit

            exit_price = prices[exit_bar]
            ret = np.log(exit_price / entry_price) if entry_price > 0 else 0
            trades.append({
                "entry_bar": entry_bar,
                "exit_bar": exit_bar,
                "ret": ret,
                "duration": exit_bar - entry_bar,
                "exit_dest": e["exit_dest"],
                "held_to_exit": exit_bar == e["end_idx"],
            })

    print(f"\n  Total confirmed-flip trades: {len(trades)}")

    if trades:
        rets = np.array([t["ret"] for t in trades])
        durs = np.array([t["duration"] for t in trades])
        wins = rets > 0
        losses = rets < 0

        print(f"  Mean return: {np.mean(rets)*100:+.4f}%")
        print(f"  Median return: {np.median(rets)*100:+.4f}%")
        print(f"  Std: {np.std(rets)*100:.4f}%")
        print(f"  Win rate: {np.mean(wins)*100:.1f}% ({wins.sum()}/{len(trades)})")
        if wins.sum() > 0:
            print(f"  Mean win: {np.mean(rets[wins])*100:+.4f}%")
        if losses.sum() > 0:
            print(f"  Mean loss: {np.mean(rets[losses])*100:+.4f}%")
        print(f"  Mean duration: {np.mean(durs):.1f} bars ({np.mean(durs)*5/60:.1f}h)")
        held = sum(1 for t in trades if t["held_to_exit"])
        print(f"  Held to regime exit: {held}/{len(trades)} ({held/len(trades)*100:.1f}%)")

        # Return per bar (a simple measure of edge quality)
        ret_per_bar = np.mean(rets) / max(1, np.mean(durs))
        print(f"  Return per bar: {ret_per_bar*100:.6f}%  ({ret_per_bar*100*12:.4f}%/hr)")


# ═══════════════════════════════════════════════════════════════════════════
#  PART 2: C1 Reversal (Lighter Treatment)
# ═══════════════════════════════════════════════════════════════════════════

def part2_c1_flips(episodes, states_8, prices):
    print(f"\n{'=' * 70}")
    print("  PART 2: C1 Reversal — Flip Dynamics (Lighter)")
    print(f"{'=' * 70}")

    clean_c1 = [e for e in episodes if e["macro"] == 1 and not e["truncated"]]
    print(f"  C1 episodes (non-truncated): {len(clean_c1)}")

    # ── 2a: Entry State + Flip Count ─────────────────────────────────────
    print(f"\n--- 2a. Entry State & Flip Count ---")
    entry_s2 = sum(1 for e in clean_c1 if e["entry_sub"] == 2)
    entry_s3 = sum(1 for e in clean_c1 if e["entry_sub"] == 3)
    print(f"  Enter as S2 (trend_1h↓): {entry_s2} ({entry_s2/len(clean_c1)*100:.1f}%)")
    print(f"  Enter as S3 (trend_1h↑): {entry_s3} ({entry_s3/len(clean_c1)*100:.1f}%)")

    flip_counts = []
    for e in clean_c1:
        s = states_8[e["start_idx"]:e["end_idx"] + 1]
        flips = sum(1 for i in range(len(s) - 1) if s[i] == 2 and s[i + 1] == 3)
        flip_counts.append(flips)
    flip_counts = np.array(flip_counts)

    print(f"  S2→S3 flips: mean={np.mean(flip_counts):.2f}  median={np.median(flip_counts):.0f}  "
          f"min={np.min(flip_counts)}  max={np.max(flip_counts)}")

    # By exit destination
    print(f"\n  Flip count by exit destination:")
    for dest, label in [(0, "bear"), (3, "bull")]:
        dest_idx = [i for i, e in enumerate(clean_c1) if e["exit_dest"] == dest]
        if not dest_idx:
            continue
        fc = flip_counts[dest_idx]
        print(f"    → {label} (n={len(dest_idx)}): mean={np.mean(fc):.2f}  median={np.median(fc):.0f}")

    # ── 2b: Return at Final Flip ─────────────────────────────────────────
    print(f"\n--- 2b. Return at FINAL S2→S3 Flip ---")
    print(f"  (For S3-exit episodes going to bull)")

    s3_bull = [e for e in clean_c1 if e["exit_sub"] == 3 and e["exit_dest"] == 3]
    print(f"  S3-exit → bull episodes: {len(s3_bull)}")

    final_flip_rets = []
    for e in s3_bull:
        flips = find_flips(states_8, prices, e["start_idx"], e["end_idx"], 2, 3)
        if not flips:
            continue
        last_flip = flips[-1]
        ret_after = np.log(prices[e["end_idx"]] / last_flip["price"]) if last_flip["price"] > 0 else 0
        bars_after = e["end_idx"] - last_flip["bar_idx"]
        final_flip_rets.append({"ret_after": ret_after, "bars_after": bars_after, "total": e["log_return"]})

    if final_flip_rets:
        ra = np.array([d["ret_after"] for d in final_flip_rets])
        ba = np.array([d["bars_after"] for d in final_flip_rets])
        tr = np.array([d["total"] for d in final_flip_rets])
        print(f"  With flips: {len(final_flip_rets)}")
        print(f"    Return after final flip: mean={np.mean(ra)*100:+.4f}%  median={np.median(ra)*100:+.4f}%")
        print(f"    Total episode return:    mean={np.mean(tr)*100:+.4f}%  median={np.median(tr)*100:+.4f}%")
        print(f"    Bars after final flip:   mean={np.mean(ba):.1f}")

    # ── 2c: Confirmed-Flip Returns ───────────────────────────────────────
    print(f"\n--- 2c. Confirmed S2→S3 Flip Return Profile ---")

    all_flips = []
    for e in clean_c1:
        flips = find_flips(states_8, prices, e["start_idx"], e["end_idx"], 2, 3)
        for f in flips:
            f["episode_end"] = e["end_idx"]
        all_flips.extend(flips)

    holds = [f for f in all_flips if f["is_confirmed"]]
    chatters = [f for f in all_flips if not f["is_confirmed"]]
    print(f"  Total S2→S3 flips: {len(all_flips)}")
    print(f"  Holds (≥{CONFIRM_BARS} bars): {len(holds)} ({len(holds)/max(1,len(all_flips))*100:.1f}%)")
    print(f"  Chatters: {len(chatters)} ({len(chatters)/max(1,len(all_flips))*100:.1f}%)")

    print(f"\n  Cumulative return profile:")
    header = f"  {'Bars':>6}  {'Holds':>14} (n={len(holds)})  {'Chatters':>14} (n={len(chatters)})"
    print(header)

    for h in RETURN_HORIZONS:
        for group, label in [(holds, "holds"), (chatters, "chatters")]:
            rets = []
            for f in group:
                cr = cumulative_returns(prices, f["bar_idx"], f["episode_end"], [h])
                rets.append(cr[h][0])
            if label == "holds":
                h_str = f"{np.mean(rets)*100:+.4f}%" if rets else "N/A"
            else:
                c_str = f"{np.mean(rets)*100:+.4f}%" if rets else "N/A"
        print(f"  {'+' + str(h):>6}  {h_str:>20}  {c_str:>20}")


# ─── Main ────────────────────────────────────────────────────────────────────

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

    print(f"  Working rows: {len(bdf)}, price range: {prices.min():.0f}–{prices.max():.0f}")

    episodes = extract_episodes(macro_states, states_8, prices)
    print(f"  Total episodes: {len(episodes)}")

    part1_c2_flips(episodes, states_8, prices, macro_states)
    part2_c1_flips(episodes, states_8, prices)

    print(f"\n{'=' * 70}")
    print("  Phase 5 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
