"""
ETF Flows and Inter-Day Cascade Structure

Tests whether ETF outflows act as an exogenous force that pushes price into
the next position cluster, causing spike days to extend into multi-day events.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

BASE = "memories/mev/dynamics/data"
OUT = "memories/mev/physics"

# ETF launch dates
BTC_ETF_LAUNCH = "2024-01-11"
ETH_ETF_LAUNCH = "2024-07-23"

# Spike day proximity threshold for classification
CLUSTER_PROXIMITY_DAYS = 7


def load_data():
    """Load ETF flows, spike days, and price data."""
    etf = pd.read_csv(f"{OUT}/data/etf_daily_flows.csv", parse_dates=["date"])
    etf = etf.sort_values("date").set_index("date")

    spikes = pd.read_csv(f"{BASE}/crash_spike_days.csv")
    spikes = spikes[(spikes["is_spike"] == True) & (spikes["date"] != "SUMMARY")].copy()
    spikes["date"] = pd.to_datetime(spikes["date"])
    spikes = spikes.sort_values("date").reset_index(drop=True)

    price = pd.read_csv("memories/mev/data/eth_price_1h.csv")
    price["datetime"] = pd.to_datetime(price["datetime"], format="mixed", utc=True)
    price = price.sort_values("datetime")
    # Daily price (use last observation per day)
    price["date"] = price["datetime"].dt.date
    daily_price = price.groupby("date")["price"].last()
    daily_price.index = pd.to_datetime(daily_price.index)

    return etf, spikes, daily_price


def classify_spike_days(spikes):
    """Classify spike days as cluster-initiating, terminal, or isolated."""
    dates = spikes["date"].values
    n = len(dates)
    classes = []

    for i in range(n):
        d = dates[i]
        has_prior = any(0 < (d - dates[j]) / np.timedelta64(1, 'D') <= CLUSTER_PROXIMITY_DAYS
                       for j in range(i))
        has_next = any(0 < (dates[j] - d) / np.timedelta64(1, 'D') <= CLUSTER_PROXIMITY_DAYS
                      for j in range(i + 1, n))

        if has_prior and has_next:
            classes.append("mid-cluster")
        elif has_next and not has_prior:
            classes.append("cluster-initiating")
        elif has_prior and not has_next:
            classes.append("terminal")
        else:
            classes.append("isolated")

    spikes["spike_class"] = classes
    return spikes


def get_trading_day_window(etf_index, target_date, window):
    """Get trading days within a window around target_date.
    
    Returns a dict mapping offset → (date, flow) where offset is in trading days.
    """
    # Find nearest trading day to target_date (or before for weekends)
    all_dates = etf_index
    mask = all_dates <= target_date
    if mask.any():
        anchor = all_dates[mask][-1]
    else:
        return {}

    anchor_idx = all_dates.get_loc(anchor)
    result = {}
    for offset in range(window[0], window[1] + 1):
        idx = anchor_idx + offset
        if 0 <= idx < len(all_dates):
            result[offset] = all_dates[idx]
    return result


def compute_event_study(etf, spikes, flow_col, window=(-5, 5)):
    """Compute ETF flows around spike days by classification."""
    results = []

    for _, spike in spikes.iterrows():
        target = spike["date"]
        spike_class = spike["spike_class"]

        # Get trading day window
        td_window = get_trading_day_window(etf.index, target, window)
        if not td_window:
            continue

        for offset, td in td_window.items():
            if td in etf.index:
                flow = etf.loc[td, flow_col]
                if pd.notna(flow):
                    results.append({
                        "spike_date": target,
                        "spike_class": spike_class,
                        "offset": offset,
                        "trading_date": td,
                        "flow": flow,
                        "epoch": spike["epoch"],
                    })

    return pd.DataFrame(results)


def compute_cumulative_flows(etf, spikes, flow_col):
    """Compute cumulative pre/post flows for each spike day."""
    records = []
    for _, spike in spikes.iterrows():
        target = spike["date"]
        td_window = get_trading_day_window(etf.index, target, (-5, 5))
        if not td_window:
            continue

        pre_3d = 0
        post_3d = 0
        for offset, td in td_window.items():
            if td in etf.index:
                flow = etf.loc[td, flow_col]
                if pd.notna(flow):
                    if -3 <= offset < 0:
                        pre_3d += flow
                    elif 0 < offset <= 3:
                        post_3d += flow

        # Day-of flow
        day_of = 0
        if 0 in td_window and td_window[0] in etf.index:
            v = etf.loc[td_window[0], flow_col]
            if pd.notna(v):
                day_of = v

        records.append({
            "date": target,
            "epoch": spike["epoch"],
            "spike_class": spike["spike_class"],
            "events": spike["events"],
            "price_return": spike["price_return_1d"],
            "volume_usd": spike["volume_usd"],
            f"pre_3d_{flow_col}": pre_3d,
            f"day_of_{flow_col}": day_of,
            f"post_3d_{flow_col}": post_3d,
        })

    return pd.DataFrame(records)


def run_analysis(etf, spikes, daily_price):
    """Main analysis."""
    lines = []
    lines.append("=" * 70)
    lines.append("ETF FLOWS AND INTER-DAY CASCADE STRUCTURE")
    lines.append("=" * 70)

    # Filter to spike days with ETF coverage
    spikes_etf = spikes[spikes["date"] >= BTC_ETF_LAUNCH].copy()
    lines.append(f"\n## Coverage\n")
    lines.append(f"  Spike days total: {len(spikes)}")
    lines.append(f"  Spike days with BTC ETF coverage (≥{BTC_ETF_LAUNCH}): {len(spikes_etf)}")
    spikes_eth_etf = spikes[spikes["date"] >= ETH_ETF_LAUNCH]
    lines.append(f"  Spike days with ETH ETF coverage (≥{ETH_ETF_LAUNCH}): {len(spikes_eth_etf)}")

    # Classification
    lines.append(f"\n## Spike day classification\n")
    for _, row in spikes_etf.iterrows():
        lines.append(f"  {row['date'].strftime('%Y-%m-%d')} [{row['epoch']:>20s}] "
                     f"{row['spike_class']:>20s}  events={row['events']:>5.0f}  "
                     f"return={row['price_return_1d']*100:>+6.1f}%")

    class_counts = spikes_etf["spike_class"].value_counts()
    for cls, cnt in class_counts.items():
        lines.append(f"  {cls}: {cnt}")

    # --- Event study: BTC ETF flows ---
    lines.append(f"\n## Event study: BTC ETF flows around spike days\n")
    es_btc = compute_event_study(etf, spikes_etf, "btc_flow_usd_m")

    if len(es_btc) > 0:
        # Average flow by offset and class
        lines.append(f"  Offset | {'All':>8s} | {'Initiating':>11s} | {'Terminal':>9s} | {'Isolated':>9s}")
        lines.append("  " + "-" * 60)
        for offset in range(-5, 6):
            vals = {}
            for cls in ["all", "cluster-initiating", "terminal", "isolated"]:
                if cls == "all":
                    sub = es_btc[es_btc["offset"] == offset]["flow"]
                else:
                    sub = es_btc[(es_btc["offset"] == offset) & (es_btc["spike_class"] == cls)]["flow"]
                vals[cls] = sub.mean() if len(sub) > 0 else np.nan

            lines.append(f"  {offset:>+3d}    | {vals['all']:>+8.1f} | {vals.get('cluster-initiating', np.nan):>+11.1f} | "
                        f"{vals.get('terminal', np.nan):>+9.1f} | {vals.get('isolated', np.nan):>+9.1f}")

    # --- Cumulative flows ---
    cum_btc = compute_cumulative_flows(etf, spikes_etf, "btc_flow_usd_m")

    if len(cum_btc) > 0:
        lines.append(f"\n## Cumulative BTC ETF flows per spike day\n")
        lines.append(f"  {'Date':>12s} | {'Class':>20s} | {'Pre-3d':>8s} | {'Day-of':>8s} | {'Post-3d':>8s} | "
                     f"{'Events':>6s} | {'Return':>8s}")
        lines.append("  " + "-" * 90)
        for _, row in cum_btc.iterrows():
            lines.append(f"  {row['date'].strftime('%Y-%m-%d'):>12s} | {row['spike_class']:>20s} | "
                        f"{row['pre_3d_btc_flow_usd_m']:>+8.1f} | {row['day_of_btc_flow_usd_m']:>+8.1f} | "
                        f"{row['post_3d_btc_flow_usd_m']:>+8.1f} | {row['events']:>6.0f} | "
                        f"{row['price_return']*100:>+7.1f}%")

    # --- ETH ETF flows (where available) ---
    spikes_eth = spikes_etf[spikes_etf["date"] >= ETH_ETF_LAUNCH].copy()
    if len(spikes_eth) > 0:
        cum_eth = compute_cumulative_flows(etf, spikes_eth, "eth_flow_usd_m")
        if len(cum_eth) > 0:
            lines.append(f"\n## Cumulative ETH ETF flows per spike day\n")
            lines.append(f"  {'Date':>12s} | {'Pre-3d':>8s} | {'Day-of':>8s} | {'Post-3d':>8s} | "
                         f"{'Events':>6s} | {'Return':>8s}")
            lines.append("  " + "-" * 65)
            for _, row in cum_eth.iterrows():
                lines.append(f"  {row['date'].strftime('%Y-%m-%d'):>12s} | "
                            f"{row['pre_3d_eth_flow_usd_m']:>+8.1f} | {row['day_of_eth_flow_usd_m']:>+8.1f} | "
                            f"{row['post_3d_eth_flow_usd_m']:>+8.1f} | {row['events']:>6.0f} | "
                            f"{row['price_return']*100:>+7.1f}%")

    # --- January 2025 mystery ---
    lines.append(f"\n## January 2025 check\n")
    jan_2025 = etf.loc["2025-01-01":"2025-01-31"]
    if len(jan_2025) > 0:
        btc_jan = jan_2025["btc_flow_usd_m"].sum()
        eth_jan = jan_2025["eth_flow_usd_m"].sum()
        lines.append(f"  BTC ETF total flow Jan 2025: {btc_jan:+.1f}M")
        lines.append(f"  ETH ETF total flow Jan 2025: {eth_jan:+.1f}M")
        # Weekly breakdown
        jan_2025_weekly = jan_2025.resample("W").sum()
        lines.append(f"\n  Weekly breakdown:")
        for dt, row in jan_2025_weekly.iterrows():
            lines.append(f"    Week ending {dt.strftime('%Y-%m-%d')}: BTC={row['btc_flow_usd_m']:+.1f}M, "
                        f"ETH={row['eth_flow_usd_m']:+.1f}M")

    # --- Predictive tests ---
    lines.append(f"\n## Predictive tests\n")

    if len(cum_btc) > 3:
        # Correlation: pre-3d BTC flow vs spike severity
        valid = cum_btc.dropna(subset=["pre_3d_btc_flow_usd_m"])
        if len(valid) > 5:
            rho_events, p_events = stats.spearmanr(valid["pre_3d_btc_flow_usd_m"], valid["events"])
            rho_return, p_return = stats.spearmanr(valid["pre_3d_btc_flow_usd_m"], valid["price_return"])
            lines.append(f"  Pre-3d BTC flow vs liquidation count: ρ={rho_events:+.3f}, p={p_events:.4f}")
            lines.append(f"  Pre-3d BTC flow vs price return: ρ={rho_return:+.3f}, p={p_return:.4f}")

            # Does pre-flow predict cluster continuation?
            has_next = cum_btc["spike_class"].isin(["cluster-initiating", "mid-cluster"])
            if has_next.sum() > 2 and (~has_next).sum() > 2:
                flow_cont = cum_btc.loc[has_next, "pre_3d_btc_flow_usd_m"].dropna()
                flow_term = cum_btc.loc[~has_next, "pre_3d_btc_flow_usd_m"].dropna()
                if len(flow_cont) > 2 and len(flow_term) > 2:
                    u, p = stats.mannwhitneyu(flow_cont, flow_term, alternative="less")
                    lines.append(f"\n  Pre-3d BTC flow: continued cluster vs terminal/isolated:")
                    lines.append(f"    Continued: mean={flow_cont.mean():+.1f}M (n={len(flow_cont)})")
                    lines.append(f"    Terminal/isolated: mean={flow_term.mean():+.1f}M (n={len(flow_term)})")
                    lines.append(f"    Mann-Whitney (continued < terminal): U={u:.0f}, p={p:.4f}")

    return lines, cum_btc, spikes_etf


def plot_event_study(etf, spikes_etf):
    """Event study plot: cumulative ETF flow around spike days by class."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax_idx, (flow_col, title, launch) in enumerate([
        ("btc_flow_usd_m", "BTC ETF", BTC_ETF_LAUNCH),
        ("eth_flow_usd_m", "ETH ETF", ETH_ETF_LAUNCH),
    ]):
        ax = axes[ax_idx]
        spikes_sub = spikes_etf[spikes_etf["date"] >= launch]
        es = compute_event_study(etf, spikes_sub, flow_col)

        if len(es) == 0:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
            continue

        colors = {"cluster-initiating": "#d62728", "terminal": "#1f77b4",
                  "isolated": "#2ca02c", "mid-cluster": "#ff7f0e"}

        for cls in ["cluster-initiating", "terminal", "isolated", "mid-cluster"]:
            sub = es[es["spike_class"] == cls]
            if len(sub) == 0:
                continue
            # Average cumulative flow
            offsets = range(-5, 6)
            cum_flow = []
            running = 0
            for off in offsets:
                vals = sub[sub["offset"] == off]["flow"]
                running += vals.mean() if len(vals) > 0 else 0
                cum_flow.append(running)

            n_days = sub["spike_date"].nunique()
            ax.plot(list(offsets), cum_flow, marker="o", markersize=4,
                   label=f"{cls} (n={n_days})", color=colors.get(cls, "gray"), linewidth=2)

        ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
        ax.axhline(0, color="gray", linestyle=":", alpha=0.3)
        ax.set_xlabel("Trading days relative to spike")
        ax.set_ylabel("Cumulative net flow ($M)")
        ax.set_title(f"{title} Flows Around Spike Days")
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUT}/etf_event_study.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/etf_event_study.png")


def plot_severity(cum_btc):
    """Scatter: pre-spike flow vs severity."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    if len(cum_btc) < 3:
        plt.savefig(f"{OUT}/etf_severity.png", dpi=150)
        plt.close()
        return

    colors = {"cluster-initiating": "#d62728", "terminal": "#1f77b4",
              "isolated": "#2ca02c", "mid-cluster": "#ff7f0e"}

    # Left: Flow vs events
    ax = axes[0]
    for cls in cum_btc["spike_class"].unique():
        sub = cum_btc[cum_btc["spike_class"] == cls]
        ax.scatter(sub["pre_3d_btc_flow_usd_m"], sub["events"],
                  s=40, alpha=0.7, color=colors.get(cls, "gray"), label=cls)
    ax.set_xlabel("Pre-3d BTC ETF flow ($M)")
    ax.set_ylabel("Liquidation events")
    ax.set_title("Pre-Spike BTC Flow vs Liquidation Count")
    ax.legend(fontsize=8)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.3)

    # Right: Flow vs return
    ax = axes[1]
    for cls in cum_btc["spike_class"].unique():
        sub = cum_btc[cum_btc["spike_class"] == cls]
        ax.scatter(sub["pre_3d_btc_flow_usd_m"], sub["price_return"] * 100,
                  s=40, alpha=0.7, color=colors.get(cls, "gray"), label=cls)
    ax.set_xlabel("Pre-3d BTC ETF flow ($M)")
    ax.set_ylabel("1-day ETH price return (%)")
    ax.set_title("Pre-Spike BTC Flow vs Price Return")
    ax.legend(fontsize=8)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.3)
    ax.axhline(0, color="gray", linestyle=":", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/etf_severity.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/etf_severity.png")


def plot_timeline(etf, spikes_etf, daily_price):
    """Timeline plot for major crash epochs."""
    epochs_to_plot = ["2025_crash", "2026_crash", "2025_q4_chop"]
    fig, axes = plt.subplots(len(epochs_to_plot), 1, figsize=(16, 5 * len(epochs_to_plot)))
    if len(epochs_to_plot) == 1:
        axes = [axes]

    for idx, epoch in enumerate(epochs_to_plot):
        ax = axes[idx]
        ep_spikes = spikes_etf[spikes_etf["epoch"] == epoch]
        if len(ep_spikes) == 0:
            ax.text(0.5, 0.5, f"No spike days in {epoch}", ha="center", va="center",
                   transform=ax.transAxes)
            continue

        # Date range: 2 weeks before first spike to 1 week after last
        date_start = ep_spikes["date"].min() - pd.Timedelta(days=14)
        date_end = ep_spikes["date"].max() + pd.Timedelta(days=7)

        # ETF flows in range
        etf_range = etf.loc[date_start:date_end]
        if len(etf_range) == 0:
            continue

        # BTC flows as bars
        btc = etf_range["btc_flow_usd_m"].fillna(0)
        colors = ["#d62728" if v < 0 else "#2ca02c" for v in btc.values]
        ax.bar(btc.index, btc.values, color=colors, alpha=0.6, width=0.8, label="BTC ETF flow")

        # ETH flows as bars (offset)
        if "eth_flow_usd_m" in etf_range.columns:
            eth = etf_range["eth_flow_usd_m"].fillna(0)
            eth_colors = ["#ff6666" if v < 0 else "#66cc66" for v in eth.values]
            ax.bar(eth.index + pd.Timedelta(hours=12), eth.values, color=eth_colors,
                  alpha=0.4, width=0.6, label="ETH ETF flow")

        # Mark spike days
        for _, spike in ep_spikes.iterrows():
            ax.axvline(spike["date"], color="black", linewidth=2, alpha=0.7, linestyle="-")

        # Price on secondary axis
        ax2 = ax.twinx()
        price_range = daily_price.loc[date_start:date_end]
        if len(price_range) > 0:
            ax2.plot(price_range.index, price_range.values, "b-", linewidth=1.5, alpha=0.6, label="ETH price")
            ax2.set_ylabel("ETH price ($)", color="blue")
            ax2.tick_params(axis="y", labelcolor="blue")

        ax.set_title(f"{epoch}: ETF Flows + Spike Days (vertical lines)")
        ax.set_ylabel("Daily net flow ($M)")
        ax.legend(loc="upper left", fontsize=8)
        ax.axhline(0, color="gray", linestyle=":", alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{OUT}/etf_timeline.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/etf_timeline.png")


def main():
    etf, spikes, daily_price = load_data()
    spikes = classify_spike_days(spikes)
    print(f"Spike days classified: {spikes['spike_class'].value_counts().to_dict()}")

    result_lines, cum_btc, spikes_etf = run_analysis(etf, spikes, daily_price)

    # Write summary interpretation
    result_lines.append("\n" + "=" * 70)
    result_lines.append("SUMMARY & INTERPRETATION")
    result_lines.append("=" * 70)

    results_text = "\n".join(result_lines)
    print(results_text)

    with open(f"{OUT}/etf_results.txt", "w") as f:
        f.write(results_text)
    print(f"\nSaved {OUT}/etf_results.txt")

    # Plots
    plot_event_study(etf, spikes_etf)
    plot_severity(cum_btc)
    plot_timeline(etf, spikes_etf, daily_price)


if __name__ == "__main__":
    main()
