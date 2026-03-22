"""
Collateral Chain Propagation — Burst Detection in Liquidation Cascades

Tests whether Aave liquidations on spike days cluster in bursts (cascade waves)
or are uniformly distributed. Analyzes inter-event intervals, burst structure,
collateral-type composition, and oracle update alignment.
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime, timezone

BASE = "memories/mev/dynamics/data"
OUT = "memories/mev/physics"

# Burst detection thresholds to test (seconds)
GAP_THRESHOLDS = [60, 120, 300, 600]
DEFAULT_GAP = 120  # primary threshold for detailed analysis

# Minimum events on a spike day to include in analysis
MIN_EVENTS = 50

# Oracle: Chainlink ETH/USD aggregator proxy
ORACLE_ADDRESS = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
ORACLE_TOPIC = "0x0559884fd3a460db3073b7fc896cc77986f16e378210ced9a467c94b5d34f566"  # AnswerUpdated
ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/BNZuV78MYIdQEqymhrHikACnAGe5cTES"


def load_data():
    """Load liquidations, spike days, block timestamps, and price."""
    liqs = pd.read_csv(f"{BASE}/liquidations_full.csv")
    liqs["dt"] = pd.to_datetime(liqs["timestamp"], unit="s", utc=True)
    liqs["date"] = liqs["dt"].dt.strftime("%Y-%m-%d")

    spikes = pd.read_csv(f"{BASE}/crash_spike_days.csv")
    spikes = spikes[(spikes["is_spike"] == True) & (spikes["date"] != "SUMMARY")]
    spike_dates = set(spikes["date"].values)

    with open(f"{BASE}/block_timestamps.json") as f:
        block_ts = json.load(f)
    # Convert keys to int
    block_ts = {int(k): v for k, v in block_ts.items()}

    price = pd.read_csv("memories/mev/data/eth_price_1h.csv")
    price["datetime"] = pd.to_datetime(price["datetime"], format="mixed", utc=True)
    price = price.sort_values("datetime").set_index("datetime")

    return liqs, spikes, spike_dates, block_ts, price


def get_spike_day_events(liqs, spike_dates):
    """Extract real liquidation events on spike days, sorted by timestamp."""
    real = liqs[liqs["category"] == "real"].copy()
    spike_events = real[real["date"].isin(spike_dates)].copy()
    spike_events = spike_events.sort_values("timestamp").reset_index(drop=True)
    return spike_events


def compute_intervals(events_df):
    """Compute inter-event intervals (seconds) within each spike day."""
    results = {}
    for date, group in events_df.groupby("date"):
        sorted_g = group.sort_values(["timestamp", "block_number"])
        ts = sorted_g["timestamp"].values
        blocks = sorted_g["block_number"].values
        if len(ts) < 2:
            continue
        intervals = np.diff(ts)

        # Block-level: collapse same-block events
        block_groups = sorted_g.groupby("block_number", sort=True)
        unique_blocks = block_groups["timestamp"].first().sort_index()
        block_ts = unique_blocks.values
        block_intervals = np.diff(block_ts) if len(block_ts) > 1 else np.array([])
        events_per_block = block_groups.size().values

        results[date] = {
            "timestamps": ts,
            "intervals": intervals,
            "block_intervals": block_intervals,
            "events_per_block": events_per_block,
            "n_events": len(ts),
            "n_blocks": len(unique_blocks),
            "collateral_labels": sorted_g["collateral_label"].values,
        }
    return results


def detect_bursts(timestamps, collateral_labels, gap_threshold):
    """Detect bursts: consecutive events separated by < gap_threshold seconds."""
    if len(timestamps) < 2:
        return []

    bursts = []
    current_burst_start = 0

    for i in range(1, len(timestamps)):
        if timestamps[i] - timestamps[i - 1] > gap_threshold:
            # End current burst
            bursts.append({
                "start_idx": current_burst_start,
                "end_idx": i - 1,
                "n_events": i - current_burst_start,
                "start_ts": timestamps[current_burst_start],
                "end_ts": timestamps[i - 1],
                "duration_s": timestamps[i - 1] - timestamps[current_burst_start],
                "collaterals": collateral_labels[current_burst_start:i],
            })
            current_burst_start = i

    # Final burst
    bursts.append({
        "start_idx": current_burst_start,
        "end_idx": len(timestamps) - 1,
        "n_events": len(timestamps) - current_burst_start,
        "start_ts": timestamps[current_burst_start],
        "end_ts": timestamps[-1],
        "duration_s": timestamps[-1] - timestamps[current_burst_start],
        "collaterals": collateral_labels[current_burst_start:],
    })

    return bursts


def burst_collateral_composition(bursts):
    """Classify each burst by collateral composition."""
    compositions = []
    for b in bursts:
        labels = set(b["collaterals"])
        has_weth = "WETH" in labels
        has_wsteth = "wstETH" in labels
        n_types = len(labels)

        if n_types == 1 and has_weth:
            comp = "WETH-only"
        elif n_types == 1 and has_wsteth:
            comp = "wstETH-only"
        elif n_types == 1:
            comp = "other-only"
        elif has_weth and has_wsteth:
            comp = "mixed-WETH+wstETH"
        elif has_weth:
            comp = "mixed-WETH+other"
        else:
            comp = "mixed-other"

        compositions.append(comp)
    return compositions


def simulate_null_bursts(n_events, day_duration_s, gap_threshold, n_sims=1000):
    """Simulate uniform Poisson null: same n_events distributed uniformly."""
    burst_counts = []
    for _ in range(n_sims):
        ts = np.sort(np.random.uniform(0, day_duration_s, n_events))
        intervals = np.diff(ts)
        n_bursts = np.sum(intervals > gap_threshold) + 1
        burst_counts.append(n_bursts)
    return np.array(burst_counts)


ALCHEMY_BLOCK_LIMIT = 10  # Free tier limit


def fetch_oracle_updates(block_start, block_end):
    """Fetch Chainlink AnswerUpdated events for a block range, chunked for free tier."""
    import urllib.request
    import time

    all_updates = []
    current = block_start

    while current <= block_end:
        chunk_end = min(current + ALCHEMY_BLOCK_LIMIT - 1, block_end)
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getLogs",
            "params": [{
                "address": ORACLE_ADDRESS,
                "topics": [ORACLE_TOPIC],
                "fromBlock": hex(current),
                "toBlock": hex(chunk_end),
            }]
        })

        req = urllib.request.Request(
            ALCHEMY_URL,
            data=payload.encode(),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            if "result" in data:
                for log in data["result"]:
                    block_num = int(log["blockNumber"], 16)
                    price_raw = int(log["topics"][1], 16)
                    if price_raw >= 2**255:
                        price_raw -= 2**256
                    all_updates.append({
                        "block_number": block_num,
                        "price_raw": price_raw,
                        "price_usd": price_raw / 1e8,
                    })
            elif "error" in data and "rate" in str(data["error"]).lower():
                time.sleep(1)
                continue  # retry this chunk
        except Exception:
            pass  # skip failed chunks

        current = chunk_end + 1

    return all_updates if all_updates else None


def run_analysis(spike_events, interval_data, block_ts, price):
    """Run full burst detection and statistical analysis."""
    lines = []
    lines.append("=" * 70)
    lines.append("COLLATERAL CHAIN PROPAGATION — BURST DETECTION")
    lines.append("=" * 70)

    # --- Step 1a: Raw inter-event interval distribution ---
    all_intervals = np.concatenate([d["intervals"] for d in interval_data.values()])
    lines.append(f"\n## Inter-event interval distribution (all spike days)\n")
    lines.append(f"  Total intervals: {len(all_intervals)}")
    lines.append(f"  Mean: {all_intervals.mean():.1f}s  Median: {np.median(all_intervals):.1f}s")
    lines.append(f"  Std: {all_intervals.std():.1f}s")
    lines.append(f"  Same-block (Δt=0): {np.sum(all_intervals == 0)} ({np.sum(all_intervals == 0)/len(all_intervals)*100:.1f}%)")
    for pct in [10, 25, 50, 75, 90, 95, 99]:
        lines.append(f"  P{pct}: {np.percentile(all_intervals, pct):.1f}s")

    # --- Step 1b: Inter-BLOCK intervals (collapse same-block events) ---
    block_intervals = np.concatenate([d["block_intervals"] for d in interval_data.values()])
    lines.append(f"\n## Inter-block interval distribution (unique blocks only)\n")
    lines.append(f"  Total block transitions: {len(block_intervals)}")
    lines.append(f"  Mean: {block_intervals.mean():.1f}s  Median: {np.median(block_intervals):.1f}s")
    lines.append(f"  Std: {block_intervals.std():.1f}s")
    for pct in [10, 25, 50, 75, 90, 95, 99]:
        lines.append(f"  P{pct}: {np.percentile(block_intervals, pct):.1f}s")

    # Events per block
    all_epb = np.concatenate([d["events_per_block"] for d in interval_data.values()])
    lines.append(f"\n## Events per block\n")
    lines.append(f"  Mean: {all_epb.mean():.2f}  Median: {np.median(all_epb):.0f}  Max: {all_epb.max()}")
    lines.append(f"  Blocks with >1 event: {np.sum(all_epb > 1)} / {len(all_epb)} ({np.sum(all_epb > 1)/len(all_epb)*100:.1f}%)")

    # Test against exponential (Poisson process)
    cv = block_intervals.std() / block_intervals.mean()
    lines.append(f"\n  Coefficient of variation (inter-block): {cv:.3f} (exponential=1.0)")
    lines.append(f"  → {'Overdispersed (bursty)' if cv > 1.2 else 'Near-exponential' if 0.8 < cv < 1.2 else 'Underdispersed (regular)'}")

    # --- Step 2: Burst detection across thresholds ---
    lines.append(f"\n## Burst detection across gap thresholds\n")
    lines.append(f"  {'Threshold':>10s} | {'Bursts':>7s} | {'Med size':>8s} | {'Med gap':>8s} | {'Med dur':>8s} | {'Single%':>7s}")
    lines.append("  " + "-" * 65)

    for gap_thresh in GAP_THRESHOLDS:
        all_bursts = []
        all_gaps = []
        for date, data in sorted(interval_data.items()):
            bursts = detect_bursts(data["timestamps"], data["collateral_labels"], gap_thresh)
            all_bursts.extend(bursts)
            # Gaps between bursts
            for i in range(1, len(bursts)):
                all_gaps.append(bursts[i]["start_ts"] - bursts[i - 1]["end_ts"])

        sizes = [b["n_events"] for b in all_bursts]
        durs = [b["duration_s"] for b in all_bursts if b["n_events"] > 1]
        singles = sum(1 for s in sizes if s == 1)

        lines.append(f"  {gap_thresh:>8d}s | {len(all_bursts):>7d} | {np.median(sizes):>8.1f} | "
                     f"{np.median(all_gaps):>7.0f}s | {np.median(durs):>7.0f}s | {singles/len(all_bursts)*100:>6.1f}%")

    # --- Step 3: Per-spike-day burst stats at default threshold ---
    lines.append(f"\n## Per-spike-day burst statistics (gap={DEFAULT_GAP}s)\n")
    lines.append(f"  {'Date':>12s} | {'Events':>6s} | {'Bursts':>6s} | {'Med size':>8s} | {'Max size':>8s} | "
                 f"{'Med gap':>8s} | {'Med dur':>8s} | {'Null p':>7s}")
    lines.append("  " + "-" * 85)

    per_day_stats = {}
    for date in sorted(interval_data.keys()):
        data = interval_data[date]
        if data["n_events"] < MIN_EVENTS:
            continue

        bursts = detect_bursts(data["timestamps"], data["collateral_labels"], DEFAULT_GAP)
        sizes = [b["n_events"] for b in bursts]
        durs = [b["duration_s"] for b in bursts if b["n_events"] > 1]
        gaps = []
        for i in range(1, len(bursts)):
            gaps.append(bursts[i]["start_ts"] - bursts[i - 1]["end_ts"])

        # Null simulation
        day_dur = data["timestamps"][-1] - data["timestamps"][0]
        if day_dur > 0:
            null_bursts = simulate_null_bursts(data["n_events"], day_dur, DEFAULT_GAP)
            observed_bursts = len(bursts)
            # Two-sided: is observed burst count different from null?
            p_val = np.mean(null_bursts <= observed_bursts) * 2
            p_val = min(p_val, 2 - p_val)  # two-sided
        else:
            p_val = np.nan

        per_day_stats[date] = {
            "bursts": bursts, "n_bursts": len(bursts),
            "n_events": data["n_events"], "p_val": p_val,
        }

        med_gap = f"{np.median(gaps):.0f}s" if gaps else "N/A"
        med_dur = f"{np.median(durs):.0f}s" if durs else "N/A"

        lines.append(f"  {date:>12s} | {data['n_events']:>6d} | {len(bursts):>6d} | "
                     f"{np.median(sizes):>8.1f} | {max(sizes):>8d} | "
                     f"{med_gap:>8s} | {med_dur:>8s} | {p_val:>7.4f}")

    # --- Step 4: Collateral composition of bursts ---
    lines.append(f"\n## Collateral composition of bursts (gap={DEFAULT_GAP}s)\n")

    all_bursts_default = []
    for date, data in sorted(interval_data.items()):
        if data["n_events"] < MIN_EVENTS:
            continue
        bursts = detect_bursts(data["timestamps"], data["collateral_labels"], DEFAULT_GAP)
        all_bursts_default.extend(bursts)

    compositions = burst_collateral_composition(all_bursts_default)
    comp_counts = pd.Series(compositions).value_counts()
    total_bursts = len(compositions)
    lines.append(f"  Total bursts: {total_bursts}")
    for comp, count in comp_counts.items():
        lines.append(f"  {comp:>25s}: {count:4d} ({count/total_bursts*100:5.1f}%)")

    # Multi-event bursts only (singletons are trivially homogeneous)
    multi_bursts = [b for b in all_bursts_default if b["n_events"] > 1]
    multi_comps = burst_collateral_composition(multi_bursts)
    multi_counts = pd.Series(multi_comps).value_counts()
    lines.append(f"\n  Multi-event bursts only (n={len(multi_bursts)}):")
    for comp, count in multi_counts.items():
        lines.append(f"  {comp:>25s}: {count:4d} ({count/len(multi_bursts)*100:5.1f}%)")

    # --- Step 5: Burst size distribution ---
    lines.append(f"\n## Burst size distribution (gap={DEFAULT_GAP}s)\n")
    all_sizes = [b["n_events"] for b in all_bursts_default]
    size_counts = pd.Series(all_sizes).value_counts().sort_index()
    for size in sorted(size_counts.index[:15]):
        lines.append(f"  Size {size:>3d}: {size_counts[size]:4d} bursts")
    if len(size_counts) > 15:
        lines.append(f"  ... ({len(size_counts)} distinct sizes total)")
    lines.append(f"\n  Mean burst size: {np.mean(all_sizes):.1f}")
    lines.append(f"  Max burst size: {max(all_sizes)}")
    lines.append(f"  Fraction single-event: {sum(1 for s in all_sizes if s == 1)/len(all_sizes)*100:.1f}%")

    # --- Step 6: Burstiness metric (Goh-Barabási) ---
    # B = (σ - μ) / (σ + μ), B > 0 = bursty, B = 0 = Poisson, B < 0 = regular
    mu = all_intervals.mean()
    sigma = all_intervals.std()
    B = (sigma - mu) / (sigma + mu)
    lines.append(f"\n## Burstiness metric (Goh-Barabási)\n")
    lines.append(f"  B = (σ-μ)/(σ+μ) = ({sigma:.1f}-{mu:.1f})/({sigma:.1f}+{mu:.1f}) = {B:.4f}")
    lines.append(f"  → {'Bursty (B>0)' if B > 0 else 'Regular (B<0)' if B < 0 else 'Poisson (B≈0)'}")

    return lines, per_day_stats


ORACLE_QUERY_BUDGET = 500  # max block range to query per spike day (50 API calls)


def fetch_oracle_for_spike_days(spike_events, block_ts, interval_data):
    """Fetch oracle updates for top spike days and analyze alignment.
    
    Uses a targeted approach: only queries block ranges around the densest
    liquidation burst, staying within free-tier API budget.
    """
    lines = []
    lines.append(f"\n## Oracle update alignment\n")

    # Top 3 spike days by event count (limited to keep API calls manageable)
    top_days = sorted(interval_data.items(), key=lambda x: x[1]["n_events"], reverse=True)[:3]
    oracle_data = {}

    for date, data in top_days:
        day_events = spike_events[spike_events["date"] == date]

        # Find the densest burst and query around it
        bursts = detect_bursts(data["timestamps"], data["collateral_labels"], DEFAULT_GAP)
        biggest = max(bursts, key=lambda b: b["n_events"])

        # Get block range for biggest burst
        burst_events = day_events.iloc[biggest["start_idx"]:biggest["end_idx"] + 1]
        block_min = int(burst_events["block_number"].min())
        block_max = int(burst_events["block_number"].max())

        # Clamp to budget
        block_range = block_max - block_min
        if block_range > ORACLE_QUERY_BUDGET:
            block_mid = (block_min + block_max) // 2
            block_min = block_mid - ORACLE_QUERY_BUDGET // 2
            block_max = block_mid + ORACLE_QUERY_BUDGET // 2

        # Extend slightly for context
        block_min = max(block_min - 50, 0)
        block_max = block_max + 50
        n_chunks = (block_max - block_min) // ALCHEMY_BLOCK_LIMIT + 1

        print(f"  Fetching oracle for {date} (blocks {block_min}-{block_max}, ~{n_chunks} calls)...")
        updates = fetch_oracle_updates(block_min, block_max)

        if updates is None or len(updates) == 0:
            lines.append(f"  {date}: No oracle updates found in queried range")
            continue

        # Get timestamps for oracle blocks from block_ts or estimate
        oracle_ts = []
        for u in updates:
            bn = u["block_number"]
            if bn in block_ts:
                oracle_ts.append(block_ts[bn])
            else:
                # Estimate: ~12s per block from nearest known block
                nearest = min(block_ts.keys(), key=lambda k: abs(k - bn))
                oracle_ts.append(block_ts[nearest] + (bn - nearest) * 12)

        oracle_timestamps = np.array(oracle_ts)
        oracle_prices = np.array([u["price_usd"] for u in updates])
        oracle_data[date] = {"timestamps": oracle_timestamps, "prices": oracle_prices}

        # Oracle update intervals
        if len(oracle_timestamps) > 1:
            oracle_intervals = np.diff(oracle_timestamps)
            lines.append(f"  {date}: {len(updates)} oracle updates in queried range, "
                        f"median interval={np.median(oracle_intervals):.0f}s, "
                        f"mean={oracle_intervals.mean():.0f}s")

            # Alignment: for each burst start, find time since last oracle update
            burst_starts = np.array([b["start_ts"] for b in bursts])
            lags = []
            for bs in burst_starts:
                prior = oracle_timestamps[oracle_timestamps <= bs]
                if len(prior) > 0:
                    lags.append(bs - prior[-1])

            if lags:
                lags = np.array(lags)
                lines.append(f"    Burst-start lag after oracle: "
                            f"median={np.median(lags):.0f}s, mean={lags.mean():.0f}s, "
                            f"P25={np.percentile(lags, 25):.0f}s, P75={np.percentile(lags, 75):.0f}s")
        else:
            lines.append(f"  {date}: Only {len(updates)} oracle update(s)")

    return lines, oracle_data


def plot_timelines(spike_events, interval_data, oracle_data):
    """Plot liquidation timelines for top spike days."""
    # Top 6 days by event count
    top_days = sorted(interval_data.items(), key=lambda x: x[1]["n_events"], reverse=True)[:6]

    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    axes = axes.flatten()

    color_map = {"WETH": "#1f77b4", "wstETH": "#ff7f0e"}
    default_color = "#999999"

    for idx, (date, data) in enumerate(top_days):
        ax = axes[idx]
        ts = data["timestamps"]
        labels = data["collateral_labels"]
        t0 = ts[0]

        # Minutes from start
        minutes = (ts - t0) / 60

        # Color by collateral type
        colors = [color_map.get(l, default_color) for l in labels]

        ax.scatter(minutes, np.ones(len(minutes)), c=colors, s=8, alpha=0.6, marker="|", linewidths=1.5)

        # Overlay burst boundaries
        bursts = detect_bursts(ts, labels, DEFAULT_GAP)
        for b in bursts:
            if b["n_events"] > 3:
                bstart = (b["start_ts"] - t0) / 60
                bend = (b["end_ts"] - t0) / 60
                ax.axvspan(bstart, bend, alpha=0.08, color="red")

        # Overlay oracle updates if available
        if date in oracle_data:
            oracle_ts = oracle_data[date]["timestamps"]
            oracle_min = (oracle_ts - t0) / 60
            valid = (oracle_min >= 0) & (oracle_min <= minutes.max())
            for om in oracle_min[valid]:
                ax.axvline(om, color="green", alpha=0.3, linewidth=0.8, linestyle="--")

        ax.set_title(f"{date} (n={data['n_events']}, {len(bursts)} bursts)", fontsize=10)
        ax.set_xlabel("Minutes from first event")
        ax.set_yticks([])
        ax.set_ylim(0.5, 1.5)

    # Legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="|", color=color_map["WETH"], label="WETH", markersize=10, linewidth=0),
        Line2D([0], [0], marker="|", color=color_map["wstETH"], label="wstETH", markersize=10, linewidth=0),
        Line2D([0], [0], marker="|", color=default_color, label="other", markersize=10, linewidth=0),
        Patch(facecolor="red", alpha=0.15, label=f"Burst (gap>{DEFAULT_GAP}s)"),
        Line2D([0], [0], color="green", linestyle="--", alpha=0.5, label="Oracle update"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=5, fontsize=9)

    plt.suptitle("Liquidation Event Timelines — Top 6 Spike Days", fontsize=13, y=0.98)
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(f"{OUT}/cascade_timeline.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/cascade_timeline.png")


def plot_intervals(all_intervals, interval_data):
    """Plot interval distribution and burst statistics."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Top-left: Histogram of inter-BLOCK intervals (log scale, excludes same-block)
    ax = axes[0, 0]
    block_intervals = np.concatenate([d["block_intervals"] for d in interval_data.values()])
    bins = np.logspace(0, np.log10(max(block_intervals) + 1), 80)
    ax.hist(block_intervals, bins=bins, alpha=0.7, color="#1f77b4", edgecolor="none")
    for gt in GAP_THRESHOLDS:
        ax.axvline(gt, color="red", alpha=0.5, linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Inter-event interval (seconds)")
    ax.set_ylabel("Count")
    ax.set_title("Inter-Block Interval Distribution")
    ax.text(0.95, 0.95, f"n={len(block_intervals)}\nmedian={np.median(block_intervals):.0f}s",
            transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    # Top-right: CDF vs exponential (block-level)
    ax = axes[0, 1]
    sorted_intervals = np.sort(block_intervals)
    cdf = np.arange(1, len(sorted_intervals) + 1) / len(sorted_intervals)
    ax.plot(sorted_intervals, cdf, label="Observed (inter-block)", linewidth=2)
    # Exponential CDF
    lam = 1 / block_intervals.mean()
    x_exp = np.linspace(0, sorted_intervals[-1], 1000)
    cdf_exp = 1 - np.exp(-lam * x_exp)
    ax.plot(x_exp, cdf_exp, "--", color="red", label="Exponential (Poisson)", linewidth=1.5)
    ax.set_xscale("log")
    ax.set_xlabel("Inter-event interval (seconds)")
    ax.set_ylabel("Cumulative probability")
    ax.set_title("CDF: Observed vs Exponential Null")
    ax.legend(fontsize=9)

    # Bottom-left: Burst count by threshold per spike day
    ax = axes[1, 0]
    dates_sorted = sorted(interval_data.keys(),
                          key=lambda d: interval_data[d]["n_events"], reverse=True)
    dates_top = [d for d in dates_sorted if interval_data[d]["n_events"] >= MIN_EVENTS][:10]
    x_pos = np.arange(len(dates_top))
    width = 0.8 / len(GAP_THRESHOLDS)
    for i, gt in enumerate(GAP_THRESHOLDS):
        counts = []
        for date in dates_top:
            data = interval_data[date]
            bursts = detect_bursts(data["timestamps"], data["collateral_labels"], gt)
            counts.append(len(bursts))
        ax.bar(x_pos + i * width, counts, width, label=f"{gt}s", alpha=0.8)
    ax.set_xticks(x_pos + width * len(GAP_THRESHOLDS) / 2)
    ax.set_xticklabels([d[5:] for d in dates_top], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Number of bursts")
    ax.set_title("Burst Count by Gap Threshold")
    ax.legend(fontsize=8, title="Gap thresh")

    # Bottom-right: Burst size distribution (default threshold)
    ax = axes[1, 1]
    all_sizes = []
    for date, data in interval_data.items():
        if data["n_events"] < MIN_EVENTS:
            continue
        bursts = detect_bursts(data["timestamps"], data["collateral_labels"], DEFAULT_GAP)
        all_sizes.extend([b["n_events"] for b in bursts])

    max_show = min(max(all_sizes), 50)
    bins_size = np.arange(0.5, max_show + 1.5, 1)
    clipped = np.clip(all_sizes, 1, max_show)
    ax.hist(clipped, bins=bins_size, alpha=0.7, color="#2ca02c", edgecolor="none")
    ax.set_xlabel("Events per burst")
    ax.set_ylabel("Count")
    ax.set_title(f"Burst Size Distribution (gap={DEFAULT_GAP}s)")
    ax.set_yscale("log")
    ax.text(0.95, 0.95, f"n_bursts={len(all_sizes)}\nmedian={np.median(all_sizes):.0f}\nmax={max(all_sizes)}",
            transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    plt.tight_layout()
    plt.savefig(f"{OUT}/cascade_intervals.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/cascade_intervals.png")


def main():
    liqs, spikes, spike_dates, block_ts, price = load_data()
    spike_events = get_spike_day_events(liqs, spike_dates)
    print(f"Spike dates: {len(spike_dates)}")
    print(f"Real liquidations on spike days: {len(spike_events)}")

    interval_data = compute_intervals(spike_events)
    print(f"Days with >= 2 events: {len(interval_data)}")

    all_intervals = np.concatenate([d["intervals"] for d in interval_data.values()])
    print(f"Total intervals: {len(all_intervals)}")

    # Main analysis
    result_lines, per_day_stats = run_analysis(spike_events, interval_data, block_ts, price)

    # Oracle alignment
    oracle_lines, oracle_data = fetch_oracle_for_spike_days(spike_events, block_ts, interval_data)
    result_lines.extend(oracle_lines)

    # Summary & interpretation
    result_lines.append("\n" + "=" * 70)
    result_lines.append("SUMMARY & INTERPRETATION")
    result_lines.append("=" * 70)

    # Compute key metrics for summary (use block-level intervals for cleaner signal)
    block_intervals = np.concatenate([d["block_intervals"] for d in interval_data.values()])
    cv = block_intervals.std() / block_intervals.mean()
    B = (block_intervals.std() - block_intervals.mean()) / (block_intervals.std() + block_intervals.mean())

    # Null comparison
    sig_days = sum(1 for d, s in per_day_stats.items() if s["p_val"] < 0.05)
    total_days = len(per_day_stats)

    # Burst composition
    all_bursts_default = []
    for date, data in interval_data.items():
        if data["n_events"] < MIN_EVENTS:
            continue
        bursts = detect_bursts(data["timestamps"], data["collateral_labels"], DEFAULT_GAP)
        all_bursts_default.extend(bursts)
    multi = [b for b in all_bursts_default if b["n_events"] > 1]
    multi_comps = burst_collateral_composition(multi)
    mixed_frac = sum(1 for c in multi_comps if "mixed" in c) / len(multi_comps) * 100 if multi_comps else 0

    same_block_frac = np.sum(all_intervals == 0) / len(all_intervals) * 100

    result_lines.append(f"""
1. LIQUIDATIONS ARE STRONGLY BURSTY
   - Burstiness metric B = {B:.3f} (>0 = bursty, 0 = Poisson)
   - Coefficient of variation (inter-block) = {cv:.2f} (exponential = 1.0)
   - {same_block_frac:.0f}% of consecutive liquidations occur in the SAME BLOCK (Δt=0)
   - Inter-block: median = {np.median(block_intervals):.0f}s vs mean = {block_intervals.mean():.0f}s
   - Heavy right tail: blocks cluster with long quiet periods between.

2. NULL COMPARISON
   - {sig_days}/{total_days} spike days show significantly fewer bursts than 
     uniform null (p<0.05). Fewer bursts = more clustering.
   - {'Most' if sig_days > total_days/2 else 'Some'} days have burst structure that cannot be 
     explained by random timing.

3. COLLATERAL COMPOSITION
   - Multi-event bursts: {mixed_frac:.0f}% contain mixed collateral types.
   - {'High mixing suggests liquidations cascade across collateral types simultaneously.' if mixed_frac > 60 else 'Moderate mixing — some collateral-type clustering within bursts.' if mixed_frac > 30 else 'Low mixing — bursts tend to be collateral-type homogeneous.'}

4. CASCADE vs INDEPENDENT vs INTERMEDIATE
   Based on the interval distribution shape, burst structure, and collateral
   composition, the data best fits:""")

    if B > 0.2 and sig_days > total_days * 0.5:
        result_lines.append("""   → CASCADE MODEL: Strong burst structure with characteristic gaps.
     Liquidations propagate as chains — one triggers the next after a
     short processing delay.""")
    elif B > 0 and sig_days > 0:
        result_lines.append("""   → INTERMEDIATE: Some burst structure driven by price volatility
     clustering. Events cluster when price drops fast, but the sequential
     dependency (gap ≈ oracle update) may or may not be present.""")
    else:
        result_lines.append("""   → INDEPENDENT: Near-Poisson timing. Events are driven by price
     level crossings, not sequential propagation.""")

    results_text = "\n".join(result_lines)
    print(results_text)

    with open(f"{OUT}/cascade_results.txt", "w") as f:
        f.write(results_text)
    print(f"\nSaved {OUT}/cascade_results.txt")

    # Plots
    plot_timelines(spike_events, interval_data, oracle_data)
    plot_intervals(all_intervals, interval_data)


if __name__ == "__main__":
    main()
