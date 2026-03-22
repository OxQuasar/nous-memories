"""
Self-Reinforcement Test — Intra-Day Burst Acceleration

Tests whether liquidation batch selling creates enough price impact to
accelerate subsequent batches beyond what external price velocity alone
would predict.

Reuses burst detection from collateral_cascade.py.
"""

import json
import sys
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Reuse from cascade module
sys.path.insert(0, "memories/mev/physics")
from collateral_cascade import (
    load_data, get_spike_day_events, compute_intervals, detect_bursts,
    DEFAULT_GAP, MIN_EVENTS, BASE, OUT
)

# Oracle deviation thresholds to test (%)
DEVIATION_THRESHOLDS = [0.5, 1.0]
PRIMARY_DEVIATION = 0.5

# Minimum price velocity to include a gap (filter flat periods)
MIN_PRICE_VELOCITY_PCT_PER_S = 0.1 / 3600  # 0.1% per hour

# wstETH/ETH approximate ratio
WSTETH_ETH_RATIO = 1.15


class PriceInterpolator:
    """Linear interpolator + local velocity from hourly price data."""

    def __init__(self, price_df):
        # Convert datetime index to unix seconds
        raw = price_df.index.astype(np.int64)
        # Auto-detect resolution:
        #   nanoseconds: ~1.64e18 for 2022 epoch → divide by 10^9
        #   microseconds: ~1.64e15 for 2022 epoch → divide by 10^6
        if raw[0] > 1e17:
            self.ts = (raw // 10**9).values
        elif raw[0] > 1e14:
            self.ts = (raw // 10**6).values
        else:
            self.ts = raw.values
        self.prices = price_df["price"].values

    def price_at(self, t):
        """Interpolate price at unix timestamp t."""
        idx = np.searchsorted(self.ts, t)
        if idx == 0:
            return self.prices[0]
        if idx >= len(self.ts):
            return self.prices[-1]
        t0, t1 = self.ts[idx - 1], self.ts[idx]
        p0, p1 = self.prices[idx - 1], self.prices[idx]
        if t1 == t0:
            return p0
        frac = (t - t0) / (t1 - t0)
        return p0 + frac * (p1 - p0)

    def velocity_at(self, t):
        """Compute local price velocity (%/second) using the hourly bracket.
        
        Uses the two hourly data points that bracket timestamp t.
        This gives the best velocity estimate at our data resolution.
        """
        idx = np.searchsorted(self.ts, t)
        if idx == 0 or idx >= len(self.ts):
            return 0.0
        t0, t1 = self.ts[idx - 1], self.ts[idx]
        p0, p1 = self.prices[idx - 1], self.prices[idx]
        dt = t1 - t0
        if dt == 0 or p0 == 0:
            return 0.0
        return abs((p1 - p0) / p0) * 100 / dt  # %/second


def compute_gap_metrics(interval_data, price_interp):
    """For each inter-burst gap, compute observed gap, price velocity, and expected gap.
    
    Price velocity is taken from the hourly bracket surrounding the gap midpoint,
    since our price data is hourly and gap-endpoint interpolation gives near-zero
    velocity for sub-hour gaps.
    """
    records = []

    for date, data in sorted(interval_data.items()):
        if data["n_events"] < MIN_EVENTS:
            continue

        bursts = detect_bursts(data["timestamps"], data["collateral_labels"], DEFAULT_GAP)
        if len(bursts) < 2:
            continue

        for i in range(1, len(bursts)):
            prev_burst = bursts[i - 1]
            curr_burst = bursts[i]

            gap_start = prev_burst["end_ts"]
            gap_end = curr_burst["start_ts"]
            observed_gap = gap_end - gap_start

            if observed_gap <= 0:
                continue

            midpoint_ts = (gap_start + gap_end) / 2

            # Use hourly-bracket velocity at the gap midpoint
            price_velocity = price_interp.velocity_at(midpoint_ts)
            p_start = price_interp.price_at(gap_start)
            p_end = price_interp.price_at(gap_end)
            price_change_pct = abs((p_end - p_start) / p_start) * 100 if p_start > 0 else 0

            # Compute expected gap for each deviation threshold
            expected_gaps = {}
            for D in DEVIATION_THRESHOLDS:
                if price_velocity > MIN_PRICE_VELOCITY_PCT_PER_S:
                    expected_gaps[D] = D / price_velocity
                else:
                    expected_gaps[D] = np.nan

            records.append({
                "date": date,
                "gap_idx": i - 1,
                "gap_start_ts": gap_start,
                "gap_end_ts": gap_end,
                "midpoint_ts": midpoint_ts,
                "observed_gap": observed_gap,
                "price_start": p_start,
                "price_end": p_end,
                "price_change_pct": price_change_pct,
                "price_velocity": price_velocity,
                "prev_burst_size": prev_burst["n_events"],
                "curr_burst_size": curr_burst["n_events"],
                **{f"expected_gap_{D}": v for D, v in expected_gaps.items()},
            })

    return pd.DataFrame(records)


def compute_liq_volume(spike_events, spikes_df):
    """Compute ETH-equivalent liquidation volume per spike day."""
    records = []
    for date, group in spike_events.groupby("date"):
        weth = group[group["collateral_label"] == "WETH"]["collateral_amount"].sum()
        wsteth = group[group["collateral_label"] == "wstETH"]["collateral_amount"].sum()
        eth_total = weth + wsteth * WSTETH_ETH_RATIO

        spike_row = spikes_df[spikes_df["date"] == date]
        eth_price = spike_row["eth_price"].values[0] if len(spike_row) > 0 else np.nan
        price_return = spike_row["price_return_1d"].values[0] if len(spike_row) > 0 else np.nan
        usd_total = eth_total * eth_price if not np.isnan(eth_price) else np.nan

        records.append({
            "date": date,
            "n_events": len(group),
            "weth_seized": weth,
            "wsteth_seized": wsteth,
            "eth_equivalent": eth_total,
            "usd_equivalent": usd_total,
            "eth_price": eth_price,
            "price_return_1d": price_return,
        })

    return pd.DataFrame(records).sort_values("date")


def run_analysis(gaps_df):
    """Statistical analysis of observed vs expected gaps."""
    lines = []
    lines.append("=" * 70)
    lines.append("SELF-REINFORCEMENT TEST — BURST ACCELERATION")
    lines.append("=" * 70)

    for D in DEVIATION_THRESHOLDS:
        col_exp = f"expected_gap_{D}"
        valid = gaps_df.dropna(subset=[col_exp]).copy()
        if len(valid) == 0:
            lines.append(f"\n## Deviation threshold D = {D}%\n")
            lines.append(f"  No valid gaps at this threshold.")
            continue

        valid["ratio"] = valid["observed_gap"] / valid[col_exp]
        # Filter extreme ratios (artifacts of near-zero velocity at boundary)
        valid = valid[(valid["ratio"] > 0.001) & (valid["ratio"] < 1000)]
        valid["log_ratio"] = np.log(valid["ratio"])

        lines.append(f"\n## Deviation threshold D = {D}%\n")
        lines.append(f"  Valid gaps (price velocity > {MIN_PRICE_VELOCITY_PCT_PER_S*3600:.1f}%/h): {len(valid)}")
        lines.append(f"  Observed gap:  median={np.median(valid['observed_gap']):.0f}s, "
                     f"mean={valid['observed_gap'].mean():.0f}s")
        lines.append(f"  Expected gap:  median={np.median(valid[col_exp]):.0f}s, "
                     f"mean={valid[col_exp].mean():.0f}s")

        lines.append(f"\n  Ratio (observed/expected):")
        lines.append(f"    Median: {np.median(valid['ratio']):.3f}")
        lines.append(f"    Mean:   {valid['ratio'].mean():.3f}")
        for pct in [10, 25, 50, 75, 90]:
            lines.append(f"    P{pct}: {np.percentile(valid['ratio'], pct):.3f}")

        # Statistical tests
        if len(valid) > 10:
            w_stat, w_p = stats.wilcoxon(valid["log_ratio"], alternative="two-sided")
            lines.append(f"\n  Wilcoxon signed-rank on log(obs/exp) vs 0:")
            lines.append(f"    W={w_stat:.0f}, p={w_p:.6f}")
            lines.append(f"    median log(ratio) = {np.median(valid['log_ratio']):.4f}")

            t_stat, t_p = stats.ttest_1samp(valid["log_ratio"], 0)
            lines.append(f"  One-sample t-test on log(obs/exp) vs 0:")
            lines.append(f"    t={t_stat:.3f}, p={t_p:.6f}")
            lines.append(f"    mean log(ratio) = {valid['log_ratio'].mean():.4f}")

            if np.median(valid["ratio"]) < 1:
                lines.append(f"  → Ratio < 1: SELF-REINFORCEMENT detected "
                             f"(gaps shorter than price-velocity-alone predicts)")
            elif np.median(valid["ratio"]) > 1:
                lines.append(f"  → Ratio > 1: gaps LONGER than expected "
                             f"(no self-reinforcement)")
            else:
                lines.append(f"  → Ratio ≈ 1: passive system")

    return lines


def run_intraday_analysis(gaps_df):
    """Check whether self-reinforcement strengthens over the course of a spike day."""
    lines = []
    lines.append(f"\n## Intra-day acceleration (D={PRIMARY_DEVIATION}%)\n")

    col_exp = f"expected_gap_{PRIMARY_DEVIATION}"
    valid = gaps_df.dropna(subset=[col_exp]).copy()
    valid["ratio"] = valid["observed_gap"] / valid[col_exp]

    # Per spike day: correlation between gap sequence number and ratio
    lines.append(f"  {'Date':>12s} | {'Gaps':>5s} | {'Rho':>6s} | {'p':>8s} | {'1st half':>9s} | {'2nd half':>9s} | {'Trend':>8s}")
    lines.append("  " + "-" * 75)

    all_rhos = []
    for date, group in valid.groupby("date"):
        if len(group) < 10:
            continue

        rho, p_val = stats.spearmanr(group["gap_idx"], group["ratio"])
        all_rhos.append(rho)

        mid = len(group) // 2
        first_half = group.iloc[:mid]["ratio"].median()
        second_half = group.iloc[mid:]["ratio"].median()

        trend = "↓ accel" if second_half < first_half * 0.8 else "↑ decel" if second_half > first_half * 1.2 else "→ flat"

        lines.append(f"  {date:>12s} | {len(group):>5d} | {rho:>+6.3f} | {p_val:>8.4f} | "
                     f"{first_half:>9.3f} | {second_half:>9.3f} | {trend:>8s}")

    if all_rhos:
        lines.append(f"\n  Mean Spearman ρ across days: {np.mean(all_rhos):+.3f}")
        lines.append(f"  Days with ρ < 0 (acceleration): {sum(1 for r in all_rhos if r < 0)}/{len(all_rhos)}")

    return lines


def run_volume_analysis(vol_df):
    """Summarize liquidation volume."""
    lines = []
    lines.append(f"\n## Liquidation volume per spike day (ETH-equivalent)\n")
    lines.append(f"  {'Date':>12s} | {'Events':>6s} | {'WETH':>10s} | {'wstETH':>10s} | {'ETH eq':>10s} | "
                 f"{'USD eq':>14s} | {'Price':>8s} | {'Return':>8s}")
    lines.append("  " + "-" * 95)

    for _, row in vol_df.iterrows():
        lines.append(f"  {row['date']:>12s} | {row['n_events']:>6.0f} | {row['weth_seized']:>10.1f} | "
                     f"{row['wsteth_seized']:>10.1f} | {row['eth_equivalent']:>10.1f} | "
                     f"${row['usd_equivalent']:>12,.0f} | ${row['eth_price']:>7.0f} | "
                     f"{row['price_return_1d']*100:>+7.1f}%")

    lines.append(f"\n  Total ETH-equivalent seized: {vol_df['eth_equivalent'].sum():,.1f} ETH")
    lines.append(f"  Total USD-equivalent seized: ${vol_df['usd_equivalent'].sum():,.0f}")

    return lines


def plot_scatter(gaps_df):
    """Observed vs expected gap scatter plot."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for idx, D in enumerate(DEVIATION_THRESHOLDS):
        ax = axes[idx]
        col_exp = f"expected_gap_{D}"
        valid = gaps_df.dropna(subset=[col_exp])

        # Color by epoch (date prefix)
        dates = valid["date"].unique()
        cmap = plt.cm.tab10
        date_colors = {d: cmap(i % 10) for i, d in enumerate(sorted(dates))}

        for date in sorted(dates):
            sub = valid[valid["date"] == date]
            ax.scatter(sub[col_exp], sub["observed_gap"],
                      s=12, alpha=0.5, color=date_colors[date], label=date[:7])

        # Diagonal line
        lims = [max(ax.get_xlim()[0], ax.get_ylim()[0], 10),
                min(ax.get_xlim()[1], ax.get_ylim()[1])]
        ax.plot([1, 1e6], [1, 1e6], "k--", alpha=0.3, linewidth=1)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Expected gap (s)")
        ax.set_ylabel("Observed gap (s)")
        ax.set_title(f"Observed vs Expected (D={D}%)")

        ratio = valid["observed_gap"] / valid[col_exp]
        ax.text(0.05, 0.95, f"median ratio={np.median(ratio):.2f}\nn={len(valid)}",
                transform=ax.transAxes, va="top", fontsize=9,
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    # Deduplicate legend
    handles, labels = axes[0].get_legend_handles_labels()
    seen = set()
    unique = [(h, l) for h, l in zip(handles, labels) if l not in seen and not seen.add(l)]
    if unique and len(unique) <= 12:
        fig.legend(*zip(*unique), loc="lower center", ncol=min(6, len(unique)), fontsize=7)

    plt.suptitle("Self-Reinforcement: Observed vs Expected Inter-Burst Gap", fontsize=12)
    plt.tight_layout(rect=[0, 0.06, 1, 0.95])
    plt.savefig(f"{OUT}/reinforcement_scatter.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/reinforcement_scatter.png")


def plot_intraday(gaps_df):
    """Plot ratio over time within spike days."""
    col_exp = f"expected_gap_{PRIMARY_DEVIATION}"
    valid = gaps_df.dropna(subset=[col_exp]).copy()
    valid["ratio"] = valid["observed_gap"] / valid[col_exp]

    # Top 6 days by gap count
    day_counts = valid.groupby("date").size().sort_values(ascending=False)
    top_days = [d for d in day_counts.index if day_counts[d] >= 10][:6]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for idx, date in enumerate(top_days):
        ax = axes[idx]
        sub = valid[valid["date"] == date].sort_values("gap_idx")

        ax.scatter(sub["gap_idx"], sub["ratio"], s=20, alpha=0.6, c="#1f77b4")
        ax.axhline(1.0, color="red", linestyle="--", alpha=0.5, label="ratio=1 (passive)")

        # Trend line
        if len(sub) > 5:
            z = np.polyfit(sub["gap_idx"], sub["ratio"], 1)
            x_fit = np.linspace(sub["gap_idx"].min(), sub["gap_idx"].max(), 50)
            ax.plot(x_fit, np.polyval(z, x_fit), "k-", alpha=0.4, linewidth=1.5)

            rho, p_val = stats.spearmanr(sub["gap_idx"], sub["ratio"])
            ax.text(0.95, 0.95, f"ρ={rho:+.2f}\np={p_val:.3f}",
                    transform=ax.transAxes, ha="right", va="top", fontsize=8,
                    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

        ax.set_title(f"{date} (n={len(sub)})", fontsize=10)
        ax.set_xlabel("Gap sequence #")
        ax.set_ylabel("Observed / Expected gap")
        ax.set_ylim(0, min(ax.get_ylim()[1], 10))

    for idx in range(len(top_days), 6):
        axes[idx].set_visible(False)

    plt.suptitle(f"Intra-Day Burst Acceleration (D={PRIMARY_DEVIATION}%)", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"{OUT}/reinforcement_intraday.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/reinforcement_intraday.png")


def plot_volume(vol_df):
    """Bar chart of liquidation volume and price decline per spike day."""
    fig, ax1 = plt.subplots(figsize=(14, 6))

    dates = vol_df["date"].values
    x = np.arange(len(dates))
    eth_eq = vol_df["eth_equivalent"].values
    returns = vol_df["price_return_1d"].values * 100

    bars = ax1.bar(x, eth_eq, color="#1f77b4", alpha=0.7, label="ETH seized")
    ax1.set_ylabel("ETH-equivalent collateral seized", color="#1f77b4")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")
    ax1.set_xticks(x)
    ax1.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(x, returns, "ro-", markersize=5, linewidth=1.5, label="Price return", alpha=0.8)
    ax2.axhline(0, color="gray", linestyle="--", alpha=0.3)
    ax2.set_ylabel("1-day price return (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

    plt.title("Liquidation Volume vs Price Decline — Spike Days")
    plt.tight_layout()
    plt.savefig(f"{OUT}/liquidation_volume.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/liquidation_volume.png")


def main():
    liqs, spikes_df, spike_dates, block_ts, price = load_data()
    spike_events = get_spike_day_events(liqs, spike_dates)
    interval_data = compute_intervals(spike_events)

    print(f"Spike days with >= {MIN_EVENTS} events: "
          f"{sum(1 for d in interval_data.values() if d['n_events'] >= MIN_EVENTS)}")

    # Build price interpolator
    price_interp = PriceInterpolator(price)

    # Step 1-3: Gap metrics
    gaps_df = compute_gap_metrics(interval_data, price_interp)
    print(f"Total inter-burst gaps: {len(gaps_df)}")

    # Step 5: Liquidation volume
    vol_df = compute_liq_volume(spike_events, spikes_df)

    # Analysis
    result_lines = run_analysis(gaps_df)
    result_lines.extend(run_intraday_analysis(gaps_df))
    result_lines.extend(run_volume_analysis(vol_df))

    # Summary
    result_lines.append("\n" + "=" * 70)
    result_lines.append("SUMMARY & INTERPRETATION")
    result_lines.append("=" * 70)

    results_text = "\n".join(result_lines)
    print(results_text)

    with open(f"{OUT}/reinforcement_results.txt", "w") as f:
        f.write(results_text)
    print(f"\nSaved {OUT}/reinforcement_results.txt")

    # Plots
    plot_scatter(gaps_df)
    plot_intraday(gaps_df)
    plot_volume(vol_df)


if __name__ == "__main__":
    main()
