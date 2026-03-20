#!/usr/bin/env python3
"""
Exchange Inflow/Outflow Around Liquidation Episodes

Tests whether CEX exchange flows distinguish escalating (mixed) from
non-escalating (distributed-only) episodes, and absorbed (FP) from
cascading (TP) distributed days.

Data source: CoinMetrics Community API (free, no key).
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import requests
import sys

DATA_DIR = Path(__file__).parent / "data"
FLOWS_CSV = DATA_DIR / "exchange_flows.csv"
RESULTS_FILE = DATA_DIR / "exchange_flow_results.txt"

HIGH_LIQ_PERCENTILE = 90
CONC_PERCENTILE = 97
FORWARD_HORIZON = 7
EPISODE_GAP_DAYS = 14

COINMETRICS_URL = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
METRICS = "FlowInExNtv,FlowOutExNtv,FlowInExUSD,FlowOutExUSD,SplyExNtv"
ZSCORE_WINDOW = 30


# ── Data fetching ─────────────────────────────────────────────

def fetch_exchange_flows() -> pd.DataFrame:
    """Fetch daily ETH exchange flows from CoinMetrics Community API."""
    if FLOWS_CSV.exists():
        df = pd.read_csv(FLOWS_CSV)
        df["date"] = pd.to_datetime(df["date"])
        print(f"Loaded cached exchange flows: {len(df)} rows")
        return df

    print("Fetching exchange flows from CoinMetrics...")
    all_data = []
    url = COINMETRICS_URL
    params = {
        "assets": "eth",
        "metrics": METRICS,
        "frequency": "1d",
        "start_time": "2022-01-01",
        "end_time": "2026-03-19",
        "page_size": 10000,
    }

    while True:
        r = requests.get(url, params=params, timeout=60)
        if r.status_code != 200:
            print(f"API error: {r.status_code} {r.text[:500]}")
            sys.exit(1)

        resp = r.json()
        all_data.extend(resp["data"])

        if "next_page_url" not in resp:
            break
        url = resp["next_page_url"]
        params = {}  # next_page_url includes all params

    print(f"Fetched {len(all_data)} daily records")

    rows = []
    for entry in all_data:
        rows.append({
            "date": entry["time"][:10],
            "flow_in_ntv": float(entry["FlowInExNtv"]),
            "flow_out_ntv": float(entry["FlowOutExNtv"]),
            "flow_in_usd": float(entry["FlowInExUSD"]),
            "flow_out_usd": float(entry["FlowOutExUSD"]),
            "sply_ex_ntv": float(entry["SplyExNtv"]),
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv(FLOWS_CSV, index=False)
    print(f"Saved to {FLOWS_CSV}")
    return df


# ── Shared classification logic ───────────────────────────────

def load_liquidations() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["price"].shift(-FORWARD_HORIZON) / df["price"] - 1
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


# ── Derived metrics ───────────────────────────────────────────

def compute_flow_metrics(flows: pd.DataFrame) -> pd.DataFrame:
    """Add net flow, z-score, and reserve change columns."""
    df = flows.copy().sort_values("date").reset_index(drop=True)
    df["net_flow_usd"] = df["flow_in_usd"] - df["flow_out_usd"]
    df["net_flow_ntv"] = df["flow_in_ntv"] - df["flow_out_ntv"]
    df["reserve_delta"] = df["sply_ex_ntv"].diff()

    # Rolling 30d z-score of net flow
    roll = df["net_flow_usd"].rolling(ZSCORE_WINDOW, min_periods=10)
    df["net_flow_zscore"] = (df["net_flow_usd"] - roll.mean()) / roll.std()

    return df


def get_window_zscore(flow_df: pd.DataFrame, start: pd.Timestamp,
                      end: pd.Timestamp) -> float:
    """Mean net flow z-score for a date range."""
    mask = (flow_df["date"] >= start) & (flow_df["date"] <= end)
    vals = flow_df.loc[mask, "net_flow_zscore"].dropna()
    return vals.mean() if len(vals) > 0 else np.nan


# ── Tests ─────────────────────────────────────────────────────

def test1_episode_flow_signature(high: pd.DataFrame, episodes: list,
                                 flow_df: pd.DataFrame, out: list):
    """Flow signature around episodes: pre/during/post, split by type."""
    out.append("=" * 60)
    out.append("TEST 1: FLOW SIGNATURE AROUND EPISODES (±7d)")
    out.append("=" * 60)

    regimes = high["regime"].values
    records = []

    for ep in episodes:
        ep_regimes = set(regimes[ep])
        has_c = "concentrated" in ep_regimes
        has_d = "distributed" in ep_regimes

        if has_c and has_d:
            ep_type = "escalating"
        elif has_d:
            ep_type = "non-escalating"
        else:
            ep_type = "pure-concentrated"

        ep_start = high.iloc[ep[0]]["date"]
        ep_end = high.iloc[ep[-1]]["date"]

        pre_z = get_window_zscore(flow_df, ep_start - pd.Timedelta(days=7),
                                  ep_start - pd.Timedelta(days=1))
        during_z = get_window_zscore(flow_df, ep_start, ep_end)
        post_z = get_window_zscore(flow_df, ep_end + pd.Timedelta(days=1),
                                   ep_end + pd.Timedelta(days=7))

        # Also raw net flow
        mask_during = (flow_df["date"] >= ep_start) & (flow_df["date"] <= ep_end)
        mean_net = flow_df.loc[mask_during, "net_flow_usd"].mean()

        records.append({
            "start": ep_start,
            "end": ep_end,
            "size": len(ep),
            "type": ep_type,
            "pre_z": pre_z,
            "during_z": during_z,
            "post_z": post_z,
            "mean_net_usd": mean_net,
        })

    edf = pd.DataFrame(records)

    # Per-episode table
    out.append(f"\n  {'Start':<12s} {'Size':>4s} {'Type':<16s} "
               f"{'Pre Z':>7s} {'Dur Z':>7s} {'Post Z':>7s} {'Net USD/d':>14s}")
    out.append(f"  {'-'*70}")

    for _, r in edf.sort_values("start").iterrows():
        pz = f"{r['pre_z']:+.2f}" if not np.isnan(r["pre_z"]) else "n/a"
        dz = f"{r['during_z']:+.2f}" if not np.isnan(r["during_z"]) else "n/a"
        oz = f"{r['post_z']:+.2f}" if not np.isnan(r["post_z"]) else "n/a"
        net = f"${r['mean_net_usd']/1e6:+.1f}M" if not np.isnan(r["mean_net_usd"]) else "n/a"
        out.append(f"  {str(r['start'].date()):<12s} {r['size']:>4d} {r['type']:<16s} "
                   f"{pz:>7s} {dz:>7s} {oz:>7s} {net:>14s}")

    # Group comparison
    out.append(f"\n  --- Group medians ---")
    out.append(f"  {'Type':<18s} {'n':>3s} {'Pre Z':>8s} {'Dur Z':>8s} {'Post Z':>8s} "
               f"{'Net USD/d':>12s}")
    out.append(f"  {'-'*55}")

    for ep_type in ["escalating", "non-escalating", "pure-concentrated"]:
        sub = edf[edf["type"] == ep_type]
        if len(sub) == 0:
            continue
        pz = sub["pre_z"].median()
        dz = sub["during_z"].median()
        oz = sub["post_z"].median()
        net = sub["mean_net_usd"].median()
        out.append(f"  {ep_type:<18s} {len(sub):>3d} {pz:>+8.2f} {dz:>+8.2f} {oz:>+8.2f} "
                   f"${net/1e6:>+10.1f}M")

    # Mann-Whitney: escalating vs non-escalating during-episode z-score
    esc = edf.loc[edf["type"] == "escalating", "during_z"].dropna()
    non = edf.loc[edf["type"] == "non-escalating", "during_z"].dropna()

    out.append(f"\n  --- Escalating vs Non-escalating (during-episode z-score) ---")
    out.append(f"  Escalating:     n={len(esc)}, median={esc.median():+.2f}")
    out.append(f"  Non-escalating: n={len(non)}, median={non.median():+.2f}")
    if len(esc) >= 3 and len(non) >= 3:
        stat, pval = stats.mannwhitneyu(esc, non, alternative="two-sided")
        out.append(f"  Mann-Whitney U={stat:.0f}, p={pval:.4f}")

    # Also test pre-episode
    esc_pre = edf.loc[edf["type"] == "escalating", "pre_z"].dropna()
    non_pre = edf.loc[edf["type"] == "non-escalating", "pre_z"].dropna()
    out.append(f"\n  --- Escalating vs Non-escalating (pre-episode z-score) ---")
    out.append(f"  Escalating:     n={len(esc_pre)}, median={esc_pre.median():+.2f}")
    out.append(f"  Non-escalating: n={len(non_pre)}, median={non_pre.median():+.2f}")
    if len(esc_pre) >= 3 and len(non_pre) >= 3:
        stat, pval = stats.mannwhitneyu(esc_pre, non_pre, alternative="two-sided")
        out.append(f"  Mann-Whitney U={stat:.0f}, p={pval:.4f}")

    return edf


def test2_distributed_tp_vs_fp(dist: pd.DataFrame, flow_df: pd.DataFrame, out: list):
    """Net flow z-score on TP vs FP distributed days."""
    out.append("")
    out.append("=" * 60)
    out.append("TEST 2: FLOW ON DISTRIBUTED DAYS — TP vs FP")
    out.append("=" * 60)

    merged = dist.merge(flow_df[["date", "net_flow_usd", "net_flow_zscore",
                                  "net_flow_ntv"]], on="date", how="left")
    valid = merged.dropna(subset=["net_flow_zscore", "fwd_7d"])

    out.append(f"\n  Distributed days with flow data: {len(valid)} / {len(dist)}")

    tp = valid[valid["fwd_7d"] < 0]
    fp = valid[valid["fwd_7d"] >= 0]

    out.append(f"\n  Net flow z-score on event day:")
    for label, sub in [("True positive (decline)", tp), ("False positive (no decline)", fp)]:
        z = sub["net_flow_zscore"]
        net = sub["net_flow_usd"]
        out.append(f"    {label}:")
        out.append(f"      n={len(z)}, z-score median={z.median():+.2f}, mean={z.mean():+.2f}")
        out.append(f"      Net flow median=${net.median()/1e6:+.1f}M, mean=${net.mean()/1e6:+.1f}M")

    tp_z = tp["net_flow_zscore"]
    fp_z = fp["net_flow_zscore"]
    if len(tp_z) >= 3 and len(fp_z) >= 3:
        stat, pval = stats.mannwhitneyu(tp_z, fp_z, alternative="two-sided")
        out.append(f"\n  Mann-Whitney (z-score): U={stat:.0f}, p={pval:.4f}")

    # Correlation
    if len(valid) >= 5:
        r, p = stats.spearmanr(valid["net_flow_zscore"], valid["fwd_7d"])
        out.append(f"  Spearman (z-score vs fwd_7d): r={r:.3f}, p={p:.4f}")

    # Also test raw net flow
    tp_net = tp["net_flow_usd"]
    fp_net = fp["net_flow_usd"]
    if len(tp_net) >= 3 and len(fp_net) >= 3:
        stat, pval = stats.mannwhitneyu(tp_net, fp_net, alternative="two-sided")
        out.append(f"  Mann-Whitney (raw net USD): U={stat:.0f}, p={pval:.4f}")


def test3_absorption_signature(edf: pd.DataFrame, out: list):
    """Non-escalating should show more net inflows (absorption) than escalating."""
    out.append("")
    out.append("=" * 60)
    out.append("TEST 3: ABSORPTION SIGNATURE — NET INFLOW COMPARISON")
    out.append("=" * 60)

    out.append(f"\n  Prediction: non-escalating (absorbed) episodes should show")
    out.append(f"  elevated net inflows (positive = buyers absorbing) vs escalating.")

    esc = edf[edf["type"] == "escalating"]
    non = edf[edf["type"] == "non-escalating"]

    out.append(f"\n  During-episode mean net flow (USD/day):")
    out.append(f"    Escalating:     n={len(esc)}, median=${esc['mean_net_usd'].median()/1e6:+.1f}M")
    out.append(f"    Non-escalating: n={len(non)}, median=${non['mean_net_usd'].median()/1e6:+.1f}M")

    esc_v = esc["mean_net_usd"].dropna()
    non_v = non["mean_net_usd"].dropna()
    if len(esc_v) >= 3 and len(non_v) >= 3:
        stat, pval = stats.mannwhitneyu(esc_v, non_v, alternative="two-sided")
        out.append(f"    Mann-Whitney U={stat:.0f}, p={pval:.4f}")

    # Direction check
    if esc_v.median() > non_v.median():
        out.append(f"\n  → Escalating episodes show HIGHER net inflows (more selling to exchanges)")
        out.append(f"  → Consistent with: exchange selling pressure precedes/accompanies cascades")
    elif non_v.median() > esc_v.median():
        out.append(f"\n  → Non-escalating episodes show HIGHER net inflows")
        out.append(f"  → Opposite of absorption prediction — non-escalating has more exchange selling")
    else:
        out.append(f"\n  → No clear directional difference")


def test4_flow_timing_vs_spike(high: pd.DataFrame, episodes: list,
                                flow_df: pd.DataFrame, out: list):
    """For escalating episodes, when does peak net inflow occur relative to concentrated spike?"""
    out.append("")
    out.append("=" * 60)
    out.append("TEST 4: FLOW TIMING RELATIVE TO CONCENTRATED SPIKE")
    out.append("=" * 60)

    regimes = high["regime"].values
    records = []

    for ep in episodes:
        ep_regimes = regimes[ep]
        r_set = set(ep_regimes)
        if not ("concentrated" in r_set and "distributed" in r_set):
            continue  # only mixed/escalating

        ep_start = high.iloc[ep[0]]["date"]
        ep_end = high.iloc[ep[-1]]["date"]

        # First concentrated day
        first_conc_pos = next(i for i, r in enumerate(ep_regimes) if r == "concentrated")
        first_conc_date = high.iloc[ep[first_conc_pos]]["date"]

        # Flow data in extended window around episode
        window_start = ep_start - pd.Timedelta(days=3)
        window_end = ep_end + pd.Timedelta(days=3)
        mask = (flow_df["date"] >= window_start) & (flow_df["date"] <= window_end)
        window_flows = flow_df[mask].copy()

        if len(window_flows) == 0:
            continue

        # Peak net inflow day (most positive = most selling pressure to exchanges)
        peak_idx = window_flows["net_flow_usd"].idxmax()
        peak_date = window_flows.loc[peak_idx, "date"]
        peak_net = window_flows.loc[peak_idx, "net_flow_usd"]

        gap = (peak_date - first_conc_date) / np.timedelta64(1, "D")

        records.append({
            "ep_start": ep_start,
            "first_conc": first_conc_date,
            "peak_flow_date": peak_date,
            "peak_net_usd": peak_net,
            "gap_to_conc": gap,  # negative = peak before conc, positive = after
        })

    rdf = pd.DataFrame(records)

    out.append(f"\n  Escalating episodes analyzed: {len(rdf)}")
    out.append(f"\n  Peak net inflow day relative to first concentrated spike:")

    out.append(f"\n  {'Ep Start':<12s} {'1st Conc':>12s} {'Peak Flow':>12s} "
               f"{'Gap':>6s} {'Peak Net':>12s}")
    out.append(f"  {'-'*58}")

    for _, r in rdf.sort_values("ep_start").iterrows():
        gap_s = f"{r['gap_to_conc']:+.0f}d"
        out.append(f"  {str(r['ep_start'].date()):<12s} {str(r['first_conc'].date()):>12s} "
                   f"{str(r['peak_flow_date'].date()):>12s} {gap_s:>6s} "
                   f"${r['peak_net_usd']/1e6:>+10.1f}M")

    if len(rdf) > 0:
        gaps = rdf["gap_to_conc"]
        n_before = (gaps < 0).sum()
        n_same = (gaps == 0).sum()
        n_after = (gaps > 0).sum()
        med_gap = gaps.median()

        out.append(f"\n  Peak flow timing:")
        out.append(f"    Before conc spike: {n_before}")
        out.append(f"    Same day:          {n_same}")
        out.append(f"    After conc spike:  {n_after}")
        out.append(f"    Median gap: {med_gap:+.1f} days")

        if n_before > n_after:
            out.append(f"  → Peak exchange inflow tends to PRECEDE concentrated spike")
        elif n_after > n_before:
            out.append(f"  → Peak exchange inflow tends to FOLLOW concentrated spike")
        else:
            out.append(f"  → No clear temporal pattern")


# ── Main ──────────────────────────────────────────────────────

def main():
    out = []
    out.append("EXCHANGE INFLOW/OUTFLOW AROUND LIQUIDATION EPISODES")
    out.append("Source: CoinMetrics Community API | Asset: ETH")
    out.append("Classification: M1-P97 | Episodes: 14d gap clustering")
    out.append("")

    # Load data
    flows_raw = fetch_exchange_flows()
    flow_df = compute_flow_metrics(flows_raw)

    df = load_liquidations()
    df["regime"] = classify_m1p97(df)

    all_high = df[df["regime"].isin(["concentrated", "distributed"])].copy()
    high = all_high.reset_index(drop=True)
    episodes = build_episodes(high)
    dist = df[df["regime"] == "distributed"].copy()

    # Summary stats
    out.append(f"Flow data: {flow_df['date'].min().date()} to {flow_df['date'].max().date()} "
               f"({len(flow_df)} days)")
    out.append(f"Mean daily net flow: ${flow_df['net_flow_usd'].mean()/1e6:.1f}M")
    out.append(f"Median daily net flow: ${flow_df['net_flow_usd'].median()/1e6:.1f}M")
    out.append(f"Z-score range: [{flow_df['net_flow_zscore'].min():.2f}, "
               f"{flow_df['net_flow_zscore'].max():.2f}]")
    out.append(f"Positive net flow = net inflow to exchanges = selling pressure")
    out.append("")

    edf = test1_episode_flow_signature(high, episodes, flow_df, out)
    test2_distributed_tp_vs_fp(dist, flow_df, out)
    test3_absorption_signature(edf, out)
    test4_flow_timing_vs_spike(high, episodes, flow_df, out)

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
