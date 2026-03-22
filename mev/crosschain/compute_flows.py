#!/usr/bin/env python3
"""Compute directional flow metrics from THORChain swap/depth data."""

import sys
import numpy as np
import pandas as pd

DATA_DIR = "memories/mev/crosschain/data"

# --- Era and anomaly classification ---

ERA_BOUNDARIES = [
    ("2024-06-01", "synth"),
    ("2024-07-01", "transition"),
    (None, "trade"),
]

ANOMALY_RANGES = [
    ("2025-01-24", "2025-01-26", "thorfi_pause"),
    ("2025-02-22", "2025-03-05", "bybit"),
]

STABLECOIN_POOLS = [
    "ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48",
    "ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7",
    "ETH.DAI-0X6B175474E89094C44DA98B954EEDEAC495271D0F",
]

CRASH_EPISODES = [
    ("Aug 2024", "2024-08-01", "2024-08-12"),
    ("Dec 2024", "2024-12-09", "2024-12-22"),
    ("Oct 2025", "2025-10-06", "2025-10-18"),
    ("Nov 2025", "2025-11-15", "2025-12-01"),
    ("Jan-Feb 2026", "2026-01-07", "2026-02-10"),
]

ORGANIC_NET_THRESHOLD = 1e6  # min |organic_net| for correction_ratio


def classify_era(date: str) -> str:
    for boundary, era in ERA_BOUNDARIES:
        if boundary is None or date < boundary:
            return era
    return ERA_BOUNDARIES[-1][1]


def classify_anomaly(date: str) -> str:
    for start, end, label in ANOMALY_RANGES:
        if start <= date <= end:
            return label
    return ""


def compute_per_pool(swaps: pd.DataFrame, depths: pd.DataFrame) -> pd.DataFrame:
    """Compute per-pool per-day flow metrics."""
    df = swaps.copy()

    # Core directional flows
    df["organic_net"] = df["toAssetVolumeUSD"] - df["toRuneVolumeUSD"]
    df["trade_net"] = df["toTradeVolumeUSD"] - df["fromTradeVolumeUSD"]
    df["synth_net"] = df["synthMintVolumeUSD"] - df["synthRedeemVolumeUSD"]
    df["secured_net"] = df["toSecuredVolumeUSD"] - df["fromSecuredVolumeUSD"]

    # Arb share
    trade_total = df["fromTradeVolumeUSD"] + df["toTradeVolumeUSD"]
    df["arb_share"] = np.where(df["totalVolumeUSD"] > 0, trade_total / df["totalVolumeUSD"], np.nan)

    # Correction ratio: trade_net / -organic_net (how much arb corrects organic flow)
    df["correction_ratio"] = np.where(
        np.abs(df["organic_net"]) >= ORGANIC_NET_THRESHOLD,
        df["trade_net"] / -df["organic_net"],
        np.nan,
    )

    # Era and anomaly
    df["era"] = df["date"].map(classify_era)
    df["anomaly"] = df["date"].map(classify_anomaly)

    # Join depth data for major pools
    depth_cols = depths[["pool", "date", "assetDepth", "assetPriceUSD"]].copy()
    depth_cols["pool_depth_usd"] = depth_cols["assetDepth"] * depth_cols["assetPriceUSD"] / 1e8 * 2
    depth_cols = depth_cols[["pool", "date", "pool_depth_usd"]]

    df = df.merge(depth_cols, on=["pool", "date"], how="left")

    df["depth_norm_organic"] = np.where(
        df["pool_depth_usd"] > 0, df["organic_net"] / df["pool_depth_usd"], np.nan
    )
    df["depth_norm_volume"] = np.where(
        df["pool_depth_usd"] > 0, df["totalVolumeUSD"] / df["pool_depth_usd"], np.nan
    )

    return df


def compute_cross_pool(flow: pd.DataFrame) -> pd.DataFrame:
    """Compute cross-pool daily aggregates."""
    dates = sorted(flow["date"].unique())
    rows = []

    for date in dates:
        day = flow[flow["date"] == date]

        btc_organic = day.loc[day["pool"] == "BTC.BTC", "organic_net"].sum()
        eth_organic = day.loc[day["pool"] == "ETH.ETH", "organic_net"].sum()

        stable_buy = day.loc[day["pool"].isin(STABLECOIN_POOLS), "toAssetVolumeUSD"].sum()
        total_vol = day["totalVolumeUSD"].sum()

        # Herfindahl: concentration index
        pool_vols = day.loc[day["totalVolumeUSD"] > 0, "totalVolumeUSD"]
        if total_vol > 0 and len(pool_vols) > 0:
            shares = pool_vols / total_vol
            hhi = (shares ** 2).sum()
        else:
            hhi = np.nan

        rows.append({
            "date": date,
            "btc_organic_net": btc_organic,
            "eth_organic_net": eth_organic,
            "stable_buy_volume": stable_buy,
            "total_volume": total_vol,
            "flight_to_safety": stable_buy / total_vol if total_vol > 0 else np.nan,
            "btc_eth_rotation": btc_organic - eth_organic,
            "herfindahl": hhi,
            "era": classify_era(date),
            "anomaly": classify_anomaly(date),
        })

    return pd.DataFrame(rows)


def validate(flow: pd.DataFrame, cross: pd.DataFrame):
    """Print summary stats."""
    print(f"\n=== VALIDATION ===", file=sys.stderr)
    print(f"flow_metrics.csv: {len(flow)} rows ({flow['pool'].nunique()} pools, {flow['date'].nunique()} days)", file=sys.stderr)
    print(f"cross_pool_daily.csv: {len(cross)} rows", file=sys.stderr)

    # Correction ratio stats for BTC.BTC in trade era, excluding anomalies
    btc_trade = flow[
        (flow["pool"] == "BTC.BTC")
        & (flow["era"] == "trade")
        & (flow["anomaly"] == "")
    ]["correction_ratio"].dropna()
    print(f"\nBTC.BTC correction_ratio (trade era, no anomaly): n={len(btc_trade)}", file=sys.stderr)
    print(f"  mean={btc_trade.mean():.3f}  median={btc_trade.median():.3f}  std={btc_trade.std():.3f}", file=sys.stderr)

    # Crash episode rotation totals
    print(f"\nbtc_eth_rotation totals by crash episode:", file=sys.stderr)
    for name, start, end in CRASH_EPISODES:
        mask = (cross["date"] >= start) & (cross["date"] <= end)
        total = cross.loc[mask, "btc_eth_rotation"].sum()
        days = mask.sum()
        print(f"  {name:20s} [{start} → {end}]: {total:>15,.0f}  ({days} days)", file=sys.stderr)


if __name__ == "__main__":
    print("Loading data...", file=sys.stderr)
    swaps = pd.read_csv(f"{DATA_DIR}/swaps_daily.csv")
    depths = pd.read_csv(f"{DATA_DIR}/depths_daily.csv")

    print("Computing per-pool metrics...", file=sys.stderr)
    flow = compute_per_pool(swaps, depths)

    print("Computing cross-pool metrics...", file=sys.stderr)
    cross = compute_cross_pool(flow)

    # Save
    flow_cols = [
        "pool", "date", "startTime", "endTime",
        "totalVolumeUSD", "totalCount", "totalFees", "averageSlip", "runePriceUSD",
        "toAssetVolumeUSD", "toAssetCount", "toRuneVolumeUSD", "toRuneCount",
        "fromTradeVolumeUSD", "toTradeVolumeUSD", "fromTradeCount", "toTradeCount",
        "fromSecuredVolumeUSD", "toSecuredVolumeUSD",
        "synthMintVolumeUSD", "synthRedeemVolumeUSD",
        "organic_net", "trade_net", "synth_net", "secured_net",
        "arb_share", "correction_ratio",
        "pool_depth_usd", "depth_norm_organic", "depth_norm_volume",
        "era", "anomaly",
    ]
    flow[flow_cols].to_csv(f"{DATA_DIR}/flow_metrics.csv", index=False)
    print(f"Wrote {DATA_DIR}/flow_metrics.csv", file=sys.stderr)

    cross.to_csv(f"{DATA_DIR}/cross_pool_daily.csv", index=False)
    print(f"Wrote {DATA_DIR}/cross_pool_daily.csv", file=sys.stderr)

    validate(flow, cross)
