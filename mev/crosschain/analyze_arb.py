#!/usr/bin/env python3
"""Analyze arb correction mechanics using daily and hourly THORChain data."""

import sys
import numpy as np
import pandas as pd

DATA_DIR = "memories/mev/crosschain/data"
ETH_PRICE_1H = "memories/mev/data/eth_price_1h.csv"

ORGANIC_NET_THRESHOLD = 1e6

CRASH_EPISODES = {
    "aug2024":    ("2024-08-01", "2024-08-15"),
    "dec2024":    ("2024-12-11", "2024-12-25"),
    "oct2025":    ("2025-10-06", "2025-10-20"),
    "nov2025":    ("2025-11-17", "2025-12-01"),
    "janfeb2026": ("2026-01-14", "2026-01-28"),
}

# Peak stress days within each episode (for slip comparison)
CRASH_PEAKS = {
    "aug2024":    ("2024-08-04", "2024-08-07"),
    "dec2024":    ("2024-12-14", "2024-12-18"),
    "oct2025":    ("2025-10-10", "2025-10-14"),
    "nov2025":    ("2025-11-21", "2025-11-26"),
    "janfeb2026": ("2026-01-19", "2026-01-24"),
}


def load_daily():
    flow = pd.read_csv(f"{DATA_DIR}/flow_metrics.csv")
    # anomaly column: NaN means no anomaly — normalize to empty string
    flow["anomaly"] = flow["anomaly"].fillna("")

    # Load ETH daily price for returns — columns: date, timestamp, price
    eth_daily = pd.read_csv("memories/mev/data/eth_price.csv")
    eth_daily = eth_daily.rename(columns={"price": "eth_price"})
    eth_daily["date"] = pd.to_datetime(eth_daily["date"]).dt.strftime("%Y-%m-%d")
    eth_daily["eth_return"] = eth_daily["eth_price"].pct_change()
    eth_daily["abs_return"] = eth_daily["eth_return"].abs()
    return flow, eth_daily


def load_hourly():
    swaps = pd.read_csv(f"{DATA_DIR}/hourly_swaps.csv")
    depths = pd.read_csv(f"{DATA_DIR}/hourly_depths.csv")
    eth_1h = pd.read_csv(ETH_PRICE_1H)
    return swaps, depths, eth_1h


# ── Analysis 1: Slip as stress indicator (daily) ──

def analyze_slip(flow, eth_daily):
    print("\n" + "=" * 60, file=sys.stderr)
    print("ANALYSIS 1: Slip as stress indicator", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    results = []

    for pool in ["BTC.BTC", "ETH.ETH"]:
        pf = flow[(flow["pool"] == pool) & (flow["era"] == "trade") & (flow["anomaly"] == "")].copy()
        pf = pf.merge(eth_daily[["date", "abs_return"]], on="date", how="left")

        # Slip vs turnover correlation
        valid = pf.dropna(subset=["averageSlip", "depth_norm_volume"])
        valid = valid[valid["depth_norm_volume"] > 0]
        if len(valid) > 10:
            corr_turnover = valid["averageSlip"].corr(valid["depth_norm_volume"])
            print(f"\n{pool} (trade era, n={len(valid)}):", file=sys.stderr)
            print(f"  Slip vs turnover corr: {corr_turnover:.3f}", file=sys.stderr)

        # Slip vs abs_return: lead/lag
        valid2 = pf.dropna(subset=["averageSlip", "abs_return"]).copy()
        valid2 = valid2.sort_values("date").reset_index(drop=True)
        if len(valid2) > 10:
            slip = valid2["averageSlip"]
            ret = valid2["abs_return"]
            corr_lag_m1 = slip.corr(ret.shift(1))   # slip(t) vs return(t-1)
            corr_lag_0 = slip.corr(ret)              # slip(t) vs return(t)
            corr_lag_p1 = slip.corr(ret.shift(-1))   # slip(t) vs return(t+1)
            print(f"  Slip vs |return|: lag-1={corr_lag_m1:.3f}, lag0={corr_lag_0:.3f}, lag+1={corr_lag_p1:.3f}", file=sys.stderr)

        # Per-episode slip
        baseline_slip = pf["averageSlip"].median()
        print(f"  Baseline median slip: {baseline_slip:.2f} bps", file=sys.stderr)

        for ep_name, (start, end) in CRASH_PEAKS.items():
            ep_data = pf[(pf["date"] >= start) & (pf["date"] <= end)]
            if len(ep_data) > 0:
                ep_slip = ep_data["averageSlip"].mean()
                ratio = ep_slip / baseline_slip if baseline_slip > 0 else np.nan
                print(f"  {ep_name:15s}: mean slip={ep_slip:.2f} bps ({ratio:.1f}x baseline)", file=sys.stderr)
                results.append({
                    "pool": pool, "episode": ep_name, "metric": "slip",
                    "crash_value": ep_slip, "baseline_value": baseline_slip,
                    "ratio": ratio,
                })

    return results


# ── Analysis 2: Price dislocation (hourly) ──

def analyze_dislocation(h_depths, eth_1h):
    print("\n" + "=" * 60, file=sys.stderr)
    print("ANALYSIS 2: Price dislocation (hourly)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    # Build CEX price lookup: round timestamp to nearest hour
    eth_1h = eth_1h.copy()
    eth_1h["hour_ts"] = (eth_1h["timestamp"] // 3600) * 3600
    # Deduplicate — keep closest to round hour
    eth_1h["offset"] = (eth_1h["timestamp"] % 3600).abs()
    eth_1h = eth_1h.sort_values("offset").drop_duplicates(subset=["hour_ts"], keep="first")
    cex_lookup = eth_1h.set_index("hour_ts")["price"].to_dict()

    # Filter to ETH.ETH depths
    eth_depths = h_depths[h_depths["pool"] == "ETH.ETH"].copy()
    eth_depths["startTime"] = eth_depths["startTime"].astype(int)
    eth_depths["tc_price"] = eth_depths["assetPriceUSD"].astype(float)
    eth_depths["cex_price"] = eth_depths["startTime"].map(cex_lookup)
    eth_depths = eth_depths.dropna(subset=["cex_price", "tc_price"])
    eth_depths = eth_depths[eth_depths["tc_price"] > 0]
    eth_depths["dislocation_pct"] = (eth_depths["tc_price"] - eth_depths["cex_price"]) / eth_depths["cex_price"] * 100
    eth_depths["abs_dislocation"] = eth_depths["dislocation_pct"].abs()

    results = []

    # Sample rows for validation
    print("\nSample dislocation rows (Aug 2024 peak):", file=sys.stderr)
    aug = eth_depths[eth_depths["episode"] == "aug2024"].sort_values("startTime")
    aug_peak = aug[(aug["datetime"] >= "2024-08-04") & (aug["datetime"] <= "2024-08-06")]
    if len(aug_peak) > 0:
        sample = aug_peak.head(8)
        for _, row in sample.iterrows():
            print(f"  {row['datetime']}  TC=${row['tc_price']:.2f}  CEX=${row['cex_price']:.2f}  disl={row['dislocation_pct']:+.3f}%", file=sys.stderr)

    # Per-episode stats
    print("\nDislocation stats per episode:", file=sys.stderr)
    for ep in CRASH_EPISODES:
        ep_data = eth_depths[eth_depths["episode"] == ep]
        if len(ep_data) < 2:
            print(f"  {ep:15s}: insufficient data", file=sys.stderr)
            continue

        mean_abs = ep_data["abs_dislocation"].mean()
        max_abs = ep_data["abs_dislocation"].max()
        autocorr = ep_data["dislocation_pct"].autocorr(lag=1)

        # Turnover quartile split (need to join with hourly swaps)
        # We'll compute this from the dislocation data's own variation
        # Use abs_dislocation as proxy for stress
        q75 = ep_data["abs_dislocation"].quantile(0.75)
        high_stress = ep_data[ep_data["abs_dislocation"] >= q75]["abs_dislocation"].mean()
        low_stress = ep_data[ep_data["abs_dislocation"] < q75]["abs_dislocation"].mean()

        print(f"  {ep:15s}: mean|disl|={mean_abs:.4f}%  max|disl|={max_abs:.4f}%  autocorr(1h)={autocorr:.3f}  high_q={high_stress:.4f}% low_q={low_stress:.4f}%", file=sys.stderr)

        results.append({
            "pool": "ETH.ETH", "episode": ep, "metric": "dislocation",
            "mean_abs_dislocation": mean_abs,
            "max_abs_dislocation": max_abs,
            "dislocation_autocorr_1h": autocorr,
        })

    return results, eth_depths


# ── Analysis 3: Hourly correction dynamics ──

def analyze_corrections(h_swaps):
    print("\n" + "=" * 60, file=sys.stderr)
    print("ANALYSIS 3: Hourly correction dynamics", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    results = []

    for pool in ["BTC.BTC", "ETH.ETH"]:
        pf = h_swaps[h_swaps["pool"] == pool].copy()
        pf["organic_net"] = pf["toAssetVolumeUSD"] - pf["toRuneVolumeUSD"]
        pf["trade_net"] = pf["toTradeVolumeUSD"] - pf["fromTradeVolumeUSD"]
        pf["correction_ratio"] = np.where(
            np.abs(pf["organic_net"]) >= ORGANIC_NET_THRESHOLD,
            pf["trade_net"] / -pf["organic_net"],
            np.nan,
        )

        print(f"\n{pool} hourly correction ratios:", file=sys.stderr)
        for ep in CRASH_EPISODES:
            ep_data = pf[pf["episode"] == ep]
            cr = ep_data["correction_ratio"].dropna()
            if len(cr) < 2:
                print(f"  {ep:15s}: insufficient data (n={len(cr)})", file=sys.stderr)
                continue

            tight = ((cr >= 0.8) & (cr <= 1.2)).mean()
            print(f"  {ep:15s}: n={len(cr):3d}  mean={cr.mean():.3f}  std={cr.std():.3f}  tight(0.8-1.2)={tight:.1%}", file=sys.stderr)

            # Peak stress vs calm: split by volume quartile
            ep_with_vol = ep_data.dropna(subset=["correction_ratio"]).copy()
            if len(ep_with_vol) > 10:
                q75 = ep_with_vol["totalVolumeUSD"].quantile(0.75)
                high_vol = ep_with_vol[ep_with_vol["totalVolumeUSD"] >= q75]["correction_ratio"]
                low_vol = ep_with_vol[ep_with_vol["totalVolumeUSD"] < q75]["correction_ratio"]
                tight_high = ((high_vol >= 0.8) & (high_vol <= 1.2)).mean()
                tight_low = ((low_vol >= 0.8) & (low_vol <= 1.2)).mean()
                print(f"               tight correction: high-vol hours={tight_high:.1%}  low-vol hours={tight_low:.1%}", file=sys.stderr)

            results.append({
                "pool": pool, "episode": ep, "metric": "correction",
                "pct_tight_correction": tight,
                "mean_correction": cr.mean(),
                "std_correction": cr.std(),
            })

    return results


# ── Analysis 4: Depth impact during crashes ──

def analyze_depth_impact(h_depths):
    print("\n" + "=" * 60, file=sys.stderr)
    print("ANALYSIS 4: Depth impact during crashes", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    results = []

    for pool in ["BTC.BTC", "ETH.ETH"]:
        pf = h_depths[h_depths["pool"] == pool].copy()
        pf["assetDepth"] = pf["assetDepth"].astype(float)
        pf["assetPriceUSD"] = pf["assetPriceUSD"].astype(float)
        pf["depth_usd"] = pf["assetDepth"] * pf["assetPriceUSD"] / 1e8 * 2
        pf = pf.sort_values("startTime")

        print(f"\n{pool} depth changes during crashes:", file=sys.stderr)
        for ep, (start, end) in CRASH_EPISODES.items():
            ep_data = pf[pf["episode"] == ep]
            if len(ep_data) < 24:
                print(f"  {ep:15s}: insufficient data", file=sys.stderr)
                continue

            # Pre-crash: first 24h. Peak stress: use CRASH_PEAKS
            first_24h = ep_data.head(24)["depth_usd"].mean()
            last_24h = ep_data.tail(24)["depth_usd"].mean()

            peak_start, peak_end = CRASH_PEAKS[ep]
            peak_data = ep_data[(ep_data["datetime"] >= peak_start) & (ep_data["datetime"] < peak_end + " 24:00")]
            peak_depth = peak_data["depth_usd"].mean() if len(peak_data) > 0 else np.nan

            depth_change_pct = (last_24h - first_24h) / first_24h * 100 if first_24h > 0 else np.nan
            min_depth = ep_data["depth_usd"].min()
            max_depth = ep_data["depth_usd"].max()
            drawdown = (min_depth - max_depth) / max_depth * 100 if max_depth > 0 else np.nan

            print(f"  {ep:15s}: pre=${first_24h/1e6:.1f}M → post=${last_24h/1e6:.1f}M ({depth_change_pct:+.1f}%)  drawdown={drawdown:+.1f}%  peak_stress=${peak_depth/1e6:.1f}M", file=sys.stderr)

            results.append({
                "pool": pool, "episode": ep, "metric": "depth",
                "depth_loss_pct": depth_change_pct,
                "depth_drawdown_pct": drawdown,
            })

    return results


# ── Combine and save ──

def save_results(slip_results, disl_results, corr_results, depth_results):
    """Save arb_analysis.csv — one row per (pool, episode) with key metrics."""
    # Build lookup dicts keyed by (pool, episode)
    rows = {}
    for r in slip_results:
        key = (r["pool"], r["episode"])
        rows.setdefault(key, {"pool": r["pool"], "episode": r["episode"]})
        rows[key]["mean_slip"] = r["crash_value"]
        rows[key]["baseline_slip"] = r["baseline_value"]

    for r in disl_results:
        key = (r["pool"], r["episode"])
        rows.setdefault(key, {"pool": r["pool"], "episode": r["episode"]})
        rows[key]["mean_abs_dislocation"] = r["mean_abs_dislocation"]
        rows[key]["max_abs_dislocation"] = r["max_abs_dislocation"]
        rows[key]["dislocation_autocorr_1h"] = r["dislocation_autocorr_1h"]

    for r in corr_results:
        key = (r["pool"], r["episode"])
        rows.setdefault(key, {"pool": r["pool"], "episode": r["episode"]})
        rows[key]["pct_tight_correction"] = r["pct_tight_correction"]

    for r in depth_results:
        key = (r["pool"], r["episode"])
        rows.setdefault(key, {"pool": r["pool"], "episode": r["episode"]})
        rows[key]["depth_loss_pct"] = r["depth_loss_pct"]

    df = pd.DataFrame(list(rows.values()))
    cols = ["pool", "episode", "mean_slip", "baseline_slip",
            "mean_abs_dislocation", "max_abs_dislocation", "dislocation_autocorr_1h",
            "pct_tight_correction", "depth_loss_pct"]
    for c in cols:
        if c not in df.columns:
            df[c] = np.nan
    df = df[cols].sort_values(["pool", "episode"])
    df.to_csv(f"{DATA_DIR}/arb_analysis.csv", index=False)
    print(f"\nWrote {DATA_DIR}/arb_analysis.csv ({len(df)} rows)", file=sys.stderr)


if __name__ == "__main__":
    print("Loading data...", file=sys.stderr)
    flow, eth_daily = load_daily()
    h_swaps, h_depths, eth_1h = load_hourly()

    slip_results = analyze_slip(flow, eth_daily)
    disl_results, _ = analyze_dislocation(h_depths, eth_1h)
    corr_results = analyze_corrections(h_swaps)
    depth_results = analyze_depth_impact(h_depths)

    save_results(slip_results, disl_results, corr_results, depth_results)
