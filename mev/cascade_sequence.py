#!/usr/bin/env python3
"""
Protocol Cascade Sequencing

Analyzes temporal ordering of liquidation events across Maker, Compound,
and Aave during stress episodes. Uses block-level timestamps from raw
event logs for sub-daily resolution.
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "cascade_sequence_results.txt"

HIGH_LIQ_PERCENTILE = 90
EPISODE_GAP_DAYS = 14
ACTIVATION_THRESHOLD_USD = 100_000  # $100K minimum to count as "activated"


# ── Data loading ──────────────────────────────────────────────

def load_events() -> pd.DataFrame:
    """Load all raw events into a unified dataframe with UTC timestamps and USD volumes."""
    price_h = pd.read_csv(DATA_DIR / "eth_price_1h.csv")
    price_h["datetime"] = pd.to_datetime(price_h["datetime"], utc=True).dt.floor("h")
    price_h = price_h.set_index("datetime").sort_index()

    frames = []

    # Aave (volume in ETH)
    aave = pd.read_csv(DATA_DIR / "liquidation_events_raw.csv")
    aave["dt"] = pd.to_datetime(aave["timestamp"], unit="s", utc=True)
    aave["hour"] = aave["dt"].dt.floor("h")
    aave = aave.merge(price_h[["price"]].reset_index().rename(columns={"datetime": "hour"}),
                       on="hour", how="left")
    aave["volume_usd"] = aave["collateral_eth"] * aave["price"]
    aave["protocol"] = "aave"
    frames.append(aave[["dt", "timestamp", "volume_usd", "protocol"]])

    # Compound (volume already in USD)
    comp = pd.read_csv(DATA_DIR / "liquidation_compound_raw.csv")
    comp["dt"] = pd.to_datetime(comp["timestamp"], unit="s", utc=True)
    comp["protocol"] = comp["protocol"].map(
        lambda x: "compound_v2" if "v2" in str(x) else "compound_v3")
    # Merge v2+v3 into "compound"
    comp["protocol"] = "compound"
    frames.append(comp[["dt", "timestamp", "volume_usd", "protocol"]])

    # Maker (volume in ETH)
    maker = pd.read_csv(DATA_DIR / "liquidation_maker_raw.csv")
    maker["dt"] = pd.to_datetime(maker["timestamp"], unit="s", utc=True)
    maker["hour"] = maker["dt"].dt.floor("h")
    maker = maker.merge(price_h[["price"]].reset_index().rename(columns={"datetime": "hour"}),
                         on="hour", how="left")
    maker["volume_usd"] = maker["volume_eth"] * maker["price"]
    maker["protocol"] = "maker"
    frames.append(maker[["dt", "timestamp", "volume_usd", "protocol"]])

    events = pd.concat(frames, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    events["date"] = events["dt"].dt.strftime("%Y-%m-%d")
    return events


def load_daily() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["fwd_7d"] = df["price"].shift(-7) / df["price"] - 1
    return df


def build_episodes(daily: pd.DataFrame) -> list[list[int]]:
    """Build episodes from high-liquidation days using 14d gap threshold."""
    nonzero = daily.loc[daily["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)

    high_idx = daily.index[daily["total_usd"] > threshold].tolist()
    if not high_idx:
        return []

    episodes = [[high_idx[0]]]
    for i in high_idx[1:]:
        gap = (daily.loc[i, "date"] - daily.loc[episodes[-1][-1], "date"]).days
        if gap <= EPISODE_GAP_DAYS:
            episodes[-1].append(i)
        else:
            episodes.append([i])
    return episodes, threshold


# ── Section A: Protocol activation ordering ───────────────────

def section_a(events: pd.DataFrame, daily: pd.DataFrame, episodes: list,
              threshold: float, out: list):
    out.append("=" * 60)
    out.append("A. PROTOCOL ACTIVATION ORDERING DURING EPISODES")
    out.append("=" * 60)
    out.append(f"\nData: block-level timestamps for {len(events)} events across 3 protocols")
    out.append(f"Activation threshold: >${ACTIVATION_THRESHOLD_USD/1000:.0f}K daily volume per protocol")
    out.append(f"Episodes: {len(episodes)} (14d gap clustering, high-liq days >P{HIGH_LIQ_PERCENTILE})")

    protocols = ["maker", "compound", "aave"]
    rows = []

    for ep_idx in episodes:
        ep_start = daily.loc[ep_idx[0], "date"]
        ep_end = daily.loc[ep_idx[-1], "date"]
        ep_dates = set(daily.loc[ep_idx, "date"].dt.strftime("%Y-%m-%d"))

        # Get all events in the date range of the episode (inclusive, with 1d buffer)
        ep_events = events[(events["dt"] >= ep_start - pd.Timedelta(days=0)) &
                           (events["dt"] <= ep_end + pd.Timedelta(days=1))]

        # Daily volume per protocol within episode
        daily_proto = ep_events.groupby([ep_events["dt"].dt.strftime("%Y-%m-%d"), "protocol"])["volume_usd"].sum()
        daily_proto = daily_proto.unstack(fill_value=0)

        # First activation day for each protocol
        first_day = {}
        first_timestamp = {}
        for proto in protocols:
            if proto not in daily_proto.columns:
                continue
            active_days = daily_proto.index[daily_proto[proto] > ACTIVATION_THRESHOLD_USD]
            if len(active_days) > 0:
                first_day[proto] = active_days[0]
                # Get exact first event timestamp
                proto_events = ep_events[
                    (ep_events["protocol"] == proto) &
                    (ep_events["dt"].dt.strftime("%Y-%m-%d") == active_days[0])
                ]
                if len(proto_events) > 0:
                    first_timestamp[proto] = proto_events["timestamp"].min()

        row = {
            "start": str(ep_start.date()),
            "size": len(ep_idx),
            "fwd_7d": daily.loc[ep_idx[0], "fwd_7d"],
        }
        for proto in protocols:
            if proto in first_day:
                day_offset = (pd.Timestamp(first_day[proto], tz="UTC") - ep_start).days
                row[f"{proto}_day"] = day_offset
                row[f"{proto}_ts"] = first_timestamp.get(proto, np.nan)
            else:
                row[f"{proto}_day"] = np.nan
                row[f"{proto}_ts"] = np.nan

        rows.append(row)

    ep_df = pd.DataFrame(rows)

    # Report table
    out.append(f"\n  {'Start':<12s} {'Size':>4s}  {'Maker':>6s}  {'Comp':>6s}  {'Aave':>6s}  {'First':>10s}  {'7d Ret':>8s}")
    out.append(f"  {'-'*60}")

    ordering_counts = {}
    for _, r in ep_df.iterrows():
        days = {}
        for p in protocols:
            d = r[f"{p}_day"]
            if not np.isnan(d):
                days[p] = int(d)

        first_proto = min(days, key=days.get) if days else "—"
        day_strs = [f"{r[f'{p}_day']:>5.0f}d" if not np.isnan(r[f"{p}_day"]) else "     —" for p in protocols]
        fwd = f"{r['fwd_7d']*100:>+7.2f}%" if not np.isnan(r["fwd_7d"]) else "     n/a"
        out.append(f"  {r['start']:<12s} {r['size']:>4d}  {''.join(day_strs)}  {first_proto:>10s}  {fwd}")

        if len(days) >= 2:
            ordering = tuple(sorted(days.keys(), key=lambda p: (days[p], protocols.index(p))))
            ordering_counts[ordering] = ordering_counts.get(ordering, 0) + 1

    out.append(f"\n  Protocol activation orderings (multi-protocol episodes):")
    for ordering, count in sorted(ordering_counts.items(), key=lambda x: -x[1]):
        out.append(f"    {' → '.join(ordering)}: {count} episodes")

    # Summary: which protocol activates first most often?
    first_counts = {}
    for _, r in ep_df.iterrows():
        days = {p: r[f"{p}_day"] for p in protocols if not np.isnan(r[f"{p}_day"])}
        if len(days) >= 2:
            first = min(days, key=days.get)
            first_counts[first] = first_counts.get(first, 0) + 1

    out.append(f"\n  First-to-activate (multi-protocol episodes):")
    total = sum(first_counts.values())
    for p in protocols:
        n = first_counts.get(p, 0)
        pct = n / total * 100 if total > 0 else 0
        out.append(f"    {p:>10s}: {n}/{total} ({pct:.1f}%)")

    return ep_df


# ── Section B: Protocol lead/lag statistics ───────────────────

def section_b(events: pd.DataFrame, daily: pd.DataFrame, episodes: list,
              ep_df: pd.DataFrame, out: list):
    out.append("\n" + "=" * 60)
    out.append("B. PROTOCOL LEAD/LAG STATISTICS")
    out.append("=" * 60)

    protocols = ["maker", "compound", "aave"]
    pairs = [("maker", "compound"), ("maker", "aave"), ("compound", "aave")]

    out.append(f"\n  Lag = day(Y first active) - day(X first active). Positive = X leads Y.")
    out.append(f"\n  {'Pair':<22s} {'N':>4s}  {'Med lag':>8s}  {'Mean lag':>9s}  {'X leads':>8s}  {'Same day':>9s}  {'Y leads':>8s}")
    out.append(f"  {'-'*68}")

    for px, py in pairs:
        lags = []
        for _, r in ep_df.iterrows():
            dx, dy = r[f"{px}_day"], r[f"{py}_day"]
            if not np.isnan(dx) and not np.isnan(dy):
                lags.append(int(dy - dx))

        if len(lags) >= 3:
            arr = np.array(lags)
            med = np.median(arr)
            mn = np.mean(arr)
            x_leads = (arr > 0).sum()
            same = (arr == 0).sum()
            y_leads = (arr < 0).sum()
            n = len(arr)
            out.append(f"  {px}→{py:<14s} {n:>4d}  {med:>+7.1f}d  {mn:>+8.2f}d  "
                       f"{x_leads:>4d} ({x_leads/n*100:4.0f}%)  "
                       f"{same:>4d} ({same/n*100:4.0f}%)  "
                       f"{y_leads:>4d} ({y_leads/n*100:4.0f}%)")
        else:
            out.append(f"  {px}→{py:<14s}   <3 episodes with both protocols")

    # Sub-daily resolution: for same-day activations, who fires first by timestamp?
    out.append(f"\n  Sub-daily ordering (same-day activations, using block timestamps):")
    for px, py in pairs:
        x_first = 0
        y_first = 0
        ties = 0
        for _, r in ep_df.iterrows():
            dx, dy = r[f"{px}_day"], r[f"{py}_day"]
            if not np.isnan(dx) and not np.isnan(dy) and dx == dy:
                tsx = r[f"{px}_ts"]
                tsy = r[f"{py}_ts"]
                if not np.isnan(tsx) and not np.isnan(tsy):
                    if tsx < tsy:
                        x_first += 1
                    elif tsy < tsx:
                        y_first += 1
                    else:
                        ties += 1
        total = x_first + y_first + ties
        if total > 0:
            out.append(f"    {px}→{py}: {x_first} {px}-first, {y_first} {py}-first, "
                       f"{ties} ties (of {total} same-day pairs)")
        else:
            out.append(f"    {px}→{py}: no same-day activations")


# ── Section C: Lag structure vs cascade severity ──────────────

def section_c(daily: pd.DataFrame, episodes: list, ep_df: pd.DataFrame, out: list):
    out.append("\n" + "=" * 60)
    out.append("C. LAG STRUCTURE VS CASCADE SEVERITY")
    out.append("=" * 60)

    protocols = ["maker", "compound", "aave"]

    # For each episode, compute max lag between first and last protocol activation
    spread_days = []
    for _, r in ep_df.iterrows():
        days = [r[f"{p}_day"] for p in protocols if not np.isnan(r[f"{p}_day"])]
        if len(days) >= 2:
            spread = max(days) - min(days)
            spread_days.append({
                "start": r["start"],
                "spread": spread,
                "fwd_7d": r["fwd_7d"],
                "n_protocols": len(days),
            })

    if not spread_days:
        out.append("\n  No multi-protocol episodes to analyze")
        return

    sp_df = pd.DataFrame(spread_days)

    # Split: simultaneous (spread ≤ 1d) vs sequential (spread ≥ 2d)
    simul = sp_df[sp_df["spread"] <= 1]
    seqn = sp_df[sp_df["spread"] >= 2]

    out.append(f"\n  Multi-protocol episodes: {len(sp_df)}")
    out.append(f"  Simultaneous (all protocols within 1 day): {len(simul)}")
    out.append(f"  Sequential (≥2 day gap between first and last): {len(seqn)}")

    for label, sub in [("Simultaneous", simul), ("Sequential", seqn)]:
        fwd = sub["fwd_7d"].dropna()
        if len(fwd) > 0:
            out.append(f"\n  {label} (n={len(fwd)}):")
            out.append(f"    7d forward return: median={fwd.median()*100:+.3f}%, mean={fwd.mean()*100:+.3f}%, %neg={100*(fwd<0).mean():.1f}%")
        else:
            out.append(f"\n  {label}: no data")

    s_fwd = simul["fwd_7d"].dropna()
    q_fwd = seqn["fwd_7d"].dropna()
    if len(s_fwd) >= 3 and len(q_fwd) >= 3:
        spread = (s_fwd.median() - q_fwd.median()) * 100
        stat, pval = stats.mannwhitneyu(s_fwd, q_fwd, alternative="two-sided")
        out.append(f"\n  Spread (simul - sequential median): {spread:+.3f}pp")
        out.append(f"  Mann-Whitney: U={stat:.0f}, p={pval:.4f}")
    elif len(s_fwd) >= 1 and len(q_fwd) >= 1:
        out.append(f"\n  Insufficient data for statistical test (n={len(s_fwd)}, {len(q_fwd)})")

    # Detail table
    out.append(f"\n  {'Start':<12s} {'Spread':>7s}  {'#Proto':>6s}  {'7d Ret':>8s}  {'Type'}")
    out.append(f"  {'-'*50}")
    for _, r in sp_df.sort_values("start").iterrows():
        typ = "simul" if r["spread"] <= 1 else "seq"
        fwd_s = f"{r['fwd_7d']*100:>+7.2f}%" if not np.isnan(r["fwd_7d"]) else "     n/a"
        out.append(f"  {r['start']:<12s} {r['spread']:>6.0f}d  {r['n_protocols']:>6d}  {fwd_s}  {typ}")


# ── Section D: Volume share dynamics ──────────────────────────

def section_d(events: pd.DataFrame, daily: pd.DataFrame, episodes: list, out: list):
    out.append("\n" + "=" * 60)
    out.append("D. VOLUME SHARE DYNAMICS WITHIN EPISODES")
    out.append("=" * 60)

    protocols = ["aave", "compound", "maker"]

    # Find the largest episodes by total volume
    ep_info = []
    for ep_idx in episodes:
        ep_start = daily.loc[ep_idx[0], "date"]
        ep_end = daily.loc[ep_idx[-1], "date"]
        total_vol = daily.loc[ep_idx, "total_usd"].sum()
        ep_info.append({
            "indices": ep_idx,
            "start": ep_start,
            "end": ep_end,
            "total_vol": total_vol,
            "size": len(ep_idx),
        })

    # Sort by total volume, take top 5
    ep_info.sort(key=lambda x: -x["total_vol"])
    top_episodes = ep_info[:5]

    out.append(f"\n  Top {len(top_episodes)} episodes by total liquidation volume:")

    for ep in top_episodes:
        start_str = str(ep["start"].date())
        out.append(f"\n  --- Episode starting {start_str} ({ep['size']} high-liq days, ${ep['total_vol']/1e6:.1f}M total) ---")

        # Get daily protocol volumes for this episode
        ep_events = events[
            (events["dt"] >= ep["start"]) &
            (events["dt"] <= ep["end"] + pd.Timedelta(days=1))
        ]

        daily_vol = ep_events.groupby([ep_events["dt"].dt.strftime("%Y-%m-%d"), "protocol"])["volume_usd"].sum()
        daily_vol = daily_vol.unstack(fill_value=0)

        # Ensure all protocol columns exist
        for p in protocols:
            if p not in daily_vol.columns:
                daily_vol[p] = 0

        daily_vol["total"] = daily_vol[protocols].sum(axis=1)
        daily_vol = daily_vol[daily_vol["total"] > 0].sort_index()

        out.append(f"    {'Date':<12s}  {'Aave':>10s}  {'Compound':>10s}  {'Maker':>10s}  {'Total':>10s}  {'Aave%':>6s} {'Comp%':>6s} {'Makr%':>6s}")
        out.append(f"    {'-'*78}")

        for date, row in daily_vol.iterrows():
            t = row["total"]
            pcts = [row[p] / t * 100 if t > 0 else 0 for p in protocols]
            out.append(
                f"    {date:<12s}  ${row['aave']/1e3:>9.0f}K  ${row['compound']/1e3:>9.0f}K  "
                f"${row['maker']/1e3:>9.0f}K  ${t/1e3:>9.0f}K  {pcts[0]:>5.1f}% {pcts[1]:>5.1f}% {pcts[2]:>5.1f}%"
            )

        # Summary: first-half vs second-half share shift
        n_days = len(daily_vol)
        if n_days >= 4:
            half = n_days // 2
            first_half = daily_vol.iloc[:half][protocols].sum()
            second_half = daily_vol.iloc[half:][protocols].sum()
            fh_total = first_half.sum()
            sh_total = second_half.sum()

            out.append(f"\n    Share shift (first half → second half of episode):")
            for p in protocols:
                fh_pct = first_half[p] / fh_total * 100 if fh_total > 0 else 0
                sh_pct = second_half[p] / sh_total * 100 if sh_total > 0 else 0
                out.append(f"      {p:>10s}: {fh_pct:5.1f}% → {sh_pct:5.1f}% ({sh_pct - fh_pct:+.1f}pp)")


# ── Main ──────────────────────────────────────────────────────

def main():
    out = []
    out.append("PROTOCOL CASCADE SEQUENCING")
    out.append("Temporal ordering of liquidations across Maker, Compound, and Aave")
    out.append("Data: block-level event timestamps from raw liquidation logs")
    out.append("")

    print("Loading events...")
    events = load_events()
    daily = load_daily()
    episodes, threshold = build_episodes(daily)

    out.append(f"Total events: {len(events)} (aave: {(events['protocol']=='aave').sum()}, "
               f"compound: {(events['protocol']=='compound').sum()}, "
               f"maker: {(events['protocol']=='maker').sum()})")
    out.append(f"High-liquidation threshold (P{HIGH_LIQ_PERCENTILE}): ${threshold:,.0f}")
    out.append(f"Episodes: {len(episodes)}")

    # Check how many events couldn't get price (NaN volume_usd)
    missing = events["volume_usd"].isna().sum()
    if missing > 0:
        out.append(f"WARNING: {missing} events missing USD conversion (no price match)")
        events = events.dropna(subset=["volume_usd"])

    ep_df = section_a(events, daily, episodes, threshold, out)
    section_b(events, daily, episodes, ep_df, out)
    section_c(daily, episodes, ep_df, out)
    section_d(events, daily, episodes, out)

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
