#!/usr/bin/env python3
"""
Episode Arc Probe — Pre vs Post Concentrated Distributed Days

Within mixed episodes (M1-P97), split distributed days into those
occurring before vs after the first concentrated spike. Compare hit rates.

Directional probe on small n — report counts and rates.
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "episode_arc_results.txt"

HIGH_LIQ_PERCENTILE = 90
CONC_PERCENTILE = 97
FORWARD_HORIZON = 7
EPISODE_GAP_DAYS = 14


# ── Shared classification logic (same as false_positive_anatomy.py) ──

def load_liquidations() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["price"].shift(-FORWARD_HORIZON) / df["price"] - 1
    df["trail_7d"] = df["price"] / df["price"].shift(7) - 1
    return df


def classify_m1p97(df: pd.DataFrame) -> pd.Series:
    nonzero = df.loc[df["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)
    is_high = df["total_usd"] > threshold

    vol = df["total_usd"].values
    n = len(vol)
    pctl = np.full(n, np.nan)
    for i in range(n):
        start = max(0, i - 179)
        window = vol[start:i + 1]
        nz = window[window > 0]
        if len(nz) >= 10:
            pctl[i] = stats.percentileofscore(nz, vol[i], kind="rank")

    regime = pd.Series("normal", index=df.index)
    valid_high = is_high & ~np.isnan(pctl)
    regime[valid_high & (pctl >= CONC_PERCENTILE)] = "concentrated"
    regime[valid_high & (pctl < CONC_PERCENTILE)] = "distributed"
    return regime


def build_episodes(high: pd.DataFrame) -> list[list[int]]:
    high = high.reset_index(drop=True)
    dates = high["date"].values
    episodes = [[0]]
    for i in range(1, len(dates)):
        gap = (dates[i] - dates[episodes[-1][-1]]) / np.timedelta64(1, "D")
        if gap <= EPISODE_GAP_DAYS:
            episodes[-1].append(i)
        else:
            episodes.append([i])
    return episodes


# ── Arc analysis ──────────────────────────────────────────────

def main():
    out = []
    out.append("EPISODE ARC PROBE — PRE vs POST CONCENTRATED DISTRIBUTED DAYS")
    out.append("Classification: M1-P97 (180d window, ≥97th pctl → concentrated)")
    out.append("Episodes: 14-day gap clustering")
    out.append("")

    df = load_liquidations()
    df["regime"] = classify_m1p97(df)

    all_high = df[df["regime"].isin(["concentrated", "distributed"])].copy()
    high = all_high.reset_index(drop=True)
    episodes = build_episodes(high)

    regimes = high["regime"].values

    # Identify mixed episodes
    mixed = []
    for ep in episodes:
        r = set(regimes[ep])
        if "concentrated" in r and "distributed" in r:
            mixed.append(ep)

    out.append(f"Total episodes: {len(episodes)}")
    out.append(f"Mixed episodes (both types): {len(mixed)}")
    out.append(f"Total high-liq days in mixed episodes: {sum(len(e) for e in mixed)}")

    # Split distributed days within each mixed episode
    pre_rows = []
    post_rows = []
    ep_details = []

    for ep in mixed:
        ep_data = high.iloc[ep]
        dates = ep_data["date"].values
        ep_regimes = ep_data["regime"].values

        # First concentrated day
        conc_indices = [i for i, r in enumerate(ep_regimes) if r == "concentrated"]
        first_conc_pos = conc_indices[0]
        first_conc_date = dates[first_conc_pos]

        ep_pre = []
        ep_post = []

        for j, (idx, row) in enumerate(zip(ep, ep_data.itertuples())):
            if ep_regimes[j] != "distributed":
                continue
            if j < first_conc_pos:
                pre_rows.append(high.iloc[idx])
                ep_pre.append(high.iloc[idx])
            else:
                post_rows.append(high.iloc[idx])
                ep_post.append(high.iloc[idx])

        ep_details.append({
            "start": str(pd.Timestamp(dates[0]).date()),
            "size": len(ep),
            "first_conc": str(pd.Timestamp(first_conc_date).date()),
            "n_pre": len(ep_pre),
            "n_post": len(ep_post),
            "pre_fwd": [r["fwd_7d"] for r in ep_pre if not np.isnan(r["fwd_7d"])],
            "post_fwd": [r["fwd_7d"] for r in ep_post if not np.isnan(r["fwd_7d"])],
        })

    pre_df = pd.DataFrame(pre_rows) if pre_rows else pd.DataFrame()
    post_df = pd.DataFrame(post_rows) if post_rows else pd.DataFrame()

    # ── Group comparison ──────────────────────────────────────
    out.append("")
    out.append("=" * 60)
    out.append("PRE vs POST CONCENTRATED: DISTRIBUTED DAY OUTCOMES")
    out.append("=" * 60)

    pre_fwd = pre_df["fwd_7d"].dropna() if len(pre_df) > 0 else pd.Series(dtype=float)
    post_fwd = post_df["fwd_7d"].dropna() if len(post_df) > 0 else pd.Series(dtype=float)

    for label, s in [("Pre-concentrated distributed", pre_fwd),
                     ("Post-concentrated distributed", post_fwd)]:
        if len(s) > 0:
            neg = (s < 0).sum()
            out.append(f"\n  {label}:")
            out.append(f"    n={len(s)}, decline={neg} ({100*neg/len(s):.1f}%), "
                       f"no-decline={len(s)-neg} ({100*(len(s)-neg)/len(s):.1f}%)")
            out.append(f"    Median fwd_7d: {s.median()*100:+.2f}%")
            out.append(f"    Mean fwd_7d:   {s.mean()*100:+.2f}%")
        else:
            out.append(f"\n  {label}: n=0")

    if len(pre_fwd) >= 3 and len(post_fwd) >= 3:
        stat, pval = stats.mannwhitneyu(pre_fwd, post_fwd, alternative="two-sided")
        out.append(f"\n  Mann-Whitney U={stat:.0f}, p={pval:.4f}")
    elif len(pre_fwd) > 0 and len(post_fwd) > 0:
        out.append(f"\n  Sample too small for Mann-Whitney (pre={len(pre_fwd)}, post={len(post_fwd)})")

    # Also report trailing drawdown context
    out.append("")
    out.append("=" * 60)
    out.append("TRAILING DRAWDOWN CONTEXT")
    out.append("=" * 60)

    pre_trail = pre_df["trail_7d"].dropna() if len(pre_df) > 0 else pd.Series(dtype=float)
    post_trail = post_df["trail_7d"].dropna() if len(post_df) > 0 else pd.Series(dtype=float)

    for label, s in [("Pre-concentrated", pre_trail), ("Post-concentrated", post_trail)]:
        if len(s) > 0:
            out.append(f"  {label}: n={len(s)}, median trail_7d={s.median()*100:+.2f}%, "
                       f"mean={s.mean()*100:+.2f}%")

    out.append("  (Post-concentrated days likely have deeper prior drawdowns — "
               "the concentrated spike itself causes drawdown)")

    # ── Non-mixed distributed days ────────────────────────────
    out.append("")
    out.append("=" * 60)
    out.append("DISTRIBUTED DAYS OUTSIDE MIXED EPISODES")
    out.append("=" * 60)

    # Find distributed days NOT in any mixed episode
    mixed_indices = set()
    for ep in mixed:
        mixed_indices.update(ep)

    non_mixed_dist = []
    for ep in episodes:
        r = set(regimes[ep])
        if "concentrated" in r and "distributed" in r:
            continue  # skip mixed
        for idx in ep:
            if regimes[idx] == "distributed":
                non_mixed_dist.append(high.iloc[idx])

    nm_df = pd.DataFrame(non_mixed_dist) if non_mixed_dist else pd.DataFrame()
    nm_fwd = nm_df["fwd_7d"].dropna() if len(nm_df) > 0 else pd.Series(dtype=float)

    if len(nm_fwd) > 0:
        neg = (nm_fwd < 0).sum()
        out.append(f"\n  Distributed days in pure-distributed or single-day episodes:")
        out.append(f"    n={len(nm_fwd)}, decline={neg} ({100*neg/len(nm_fwd):.1f}%), "
                   f"median fwd_7d={nm_fwd.median()*100:+.2f}%")

    # Summary table
    out.append("")
    out.append("=" * 60)
    out.append("SUMMARY COMPARISON")
    out.append("=" * 60)

    out.append(f"\n  {'Group':<35s} {'n':>4s} {'%decline':>9s} {'Med fwd7d':>10s}")
    out.append(f"  {'-'*60}")
    for label, s in [
        ("All distributed (M1-P97)", pd.concat([pre_fwd, post_fwd, nm_fwd])),
        ("Pre-concentrated (mixed eps)", pre_fwd),
        ("Post-concentrated (mixed eps)", post_fwd),
        ("Non-mixed episodes", nm_fwd),
    ]:
        if len(s) > 0:
            neg = 100 * (s < 0).mean()
            med = s.median() * 100
            out.append(f"  {label:<35s} {len(s):>4d} {neg:>8.1f}% {med:>+9.2f}%")

    # ── Per-episode detail ────────────────────────────────────
    out.append("")
    out.append("=" * 60)
    out.append("PER-EPISODE DETAIL (mixed episodes)")
    out.append("=" * 60)

    out.append(f"\n  {'Start':<12s} {'Size':>4s} {'1st Conc':>12s} "
               f"{'Pre-D':>5s} {'Post-D':>6s} {'Pre fwd7d':>20s} {'Post fwd7d':>20s}")
    out.append(f"  {'-'*90}")

    for d in ep_details:
        pre_str = ", ".join(f"{v*100:+.1f}%" for v in d["pre_fwd"]) if d["pre_fwd"] else "—"
        post_str = ", ".join(f"{v*100:+.1f}%" for v in d["post_fwd"]) if d["post_fwd"] else "—"
        out.append(f"  {d['start']:<12s} {d['size']:>4d} {d['first_conc']:>12s} "
                   f"{d['n_pre']:>5d} {d['n_post']:>6d} {pre_str:>20s} {post_str:>20s}")

    # ── All distributed days in mixed episodes with arc label ─
    out.append("")
    out.append("=" * 60)
    out.append("ALL DISTRIBUTED DAYS IN MIXED EPISODES")
    out.append("=" * 60)

    out.append(f"\n  {'Date':<12s} {'Arc':>6s} {'Regime':<14s} {'LiqUSD':>12s} "
               f"{'Trail7d':>8s} {'Fwd7d':>8s} {'Price':>8s}")
    out.append(f"  {'-'*75}")

    for ep in mixed:
        ep_data = high.iloc[ep]
        ep_regimes = ep_data["regime"].values
        conc_indices = [i for i, r in enumerate(ep_regimes) if r == "concentrated"]
        first_conc_pos = conc_indices[0]

        for j, idx in enumerate(ep):
            row = high.iloc[idx]
            if row["regime"] != "distributed":
                # Show concentrated days as context
                arc = "CONC"
            elif j < first_conc_pos:
                arc = "PRE"
            else:
                arc = "POST"

            t7 = row.get("trail_7d", np.nan)
            f7 = row.get("fwd_7d", np.nan)
            t7_s = f"{t7*100:+.1f}%" if not np.isnan(t7) else "n/a"
            f7_s = f"{f7*100:+.1f}%" if not np.isnan(f7) else "n/a"

            out.append(f"  {str(row['date'].date()):<12s} {arc:>6s} {row['regime']:<14s} "
                       f"${row['total_usd']:>11,.0f} {t7_s:>8s} {f7_s:>8s} ${row['price']:>7,.0f}")
        out.append("")  # blank line between episodes

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
