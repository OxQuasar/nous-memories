"""
Protocol metrics: Aave TVL + borrow data from DefiLlama.
Epoch summaries, recharge model test, utilization dynamics.
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
MEV_DATA = Path(__file__).parent.parent / "data"

EPOCHS = [
    ("2022_bear_1",        "2022-01-01", "2022-06-18", "crash"),
    ("2022_rally",         "2022-06-18", "2022-08-13", "bull"),
    ("2022_bear_2",        "2022-08-13", "2022-11-21", "crash"),
    ("2023_recovery",      "2022-11-21", "2024-03-11", "bull"),
    ("2024_consolidation", "2024-03-11", "2024-08-07", "crash"),
    ("2024_bull",          "2024-08-07", "2024-12-16", "bull"),
    ("2025_crash",         "2024-12-16", "2025-04-08", "crash"),
    ("2025_recovery",      "2025-04-08", "2025-08-22", "bull"),
    ("2025_q4_chop",       "2025-08-22", "2025-12-17", "crash"),
    ("2026_crash",         "2025-12-17", "2026-02-24", "crash"),
    ("2026_recovery",      "2026-02-24", "2026-03-19", "bull"),
]

CRASH_EPOCHS = [e[0] for e in EPOCHS if e[3] == "crash"]


def fetch_defillama(protocol: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch TVL and borrowed data for a protocol from DefiLlama."""
    print(f"  Fetching {protocol}...")
    resp = requests.get(f"https://api.llama.fi/protocol/{protocol}", timeout=60)
    resp.raise_for_status()
    data = resp.json()

    chain_tvls = data.get("chainTvls", {})

    def extract(key):
        entries = chain_tvls.get(key, {}).get("tvl", [])
        if not entries:
            return pd.DataFrame(columns=["date", "value"])
        rows = [{"date": datetime.fromtimestamp(e["date"], tz=timezone.utc).strftime("%Y-%m-%d"),
                 "value": e["totalLiquidityUSD"]} for e in entries]
        df = pd.DataFrame(rows)
        # DefiLlama can have duplicate dates — keep last
        return df.drop_duplicates(subset="date", keep="last")

    tvl = extract("Ethereum")
    borrowed = extract("Ethereum-borrowed")
    return tvl, borrowed


def pull_protocol_data() -> pd.DataFrame:
    """Pull v2 + v3 data and merge into daily time series."""
    v2_tvl, v2_bor = fetch_defillama("aave-v2")
    v3_tvl, v3_bor = fetch_defillama("aave-v3")

    # Rename columns
    v2_tvl = v2_tvl.rename(columns={"value": "v2_tvl"})
    v2_bor = v2_bor.rename(columns={"value": "v2_borrowed"})
    v3_tvl = v3_tvl.rename(columns={"value": "v3_tvl"})
    v3_bor = v3_bor.rename(columns={"value": "v3_borrowed"})

    # Merge all on date
    df = v2_tvl.merge(v2_bor, on="date", how="outer")
    df = df.merge(v3_tvl, on="date", how="outer")
    df = df.merge(v3_bor, on="date", how="outer")
    df = df.fillna(0)
    df = df.sort_values("date").reset_index(drop=True)

    # Filter to 2022-01-01 onwards
    df = df[df["date"] >= "2022-01-01"].reset_index(drop=True)

    df["total_tvl"] = df["v2_tvl"] + df["v3_tvl"]
    df["total_borrowed"] = df["v2_borrowed"] + df["v3_borrowed"]

    return df


def merge_price(df: pd.DataFrame) -> pd.DataFrame:
    """Merge with daily ETH price, compute derived metrics."""
    prices = pd.read_csv(MEV_DATA / "eth_price.csv")
    prices["date"] = prices["date"].astype(str)
    prices = prices[["date", "price"]]

    df = df.merge(prices, on="date", how="left")
    df["price"] = df["price"].ffill().bfill()
    df.rename(columns={"price": "eth_price"}, inplace=True)

    df["borrowed_eth"] = df["total_borrowed"] / df["eth_price"]
    supply = df["total_tvl"] + df["total_borrowed"]
    df["utilization_rate"] = np.where(supply > 0, df["total_borrowed"] / supply, 0)

    return df


def epoch_boundary_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Extract values at epoch boundaries."""
    rows = []
    for name, start, end, regime in EPOCHS:
        # Find nearest date to start/end
        start_rows = df[df["date"] >= start].head(1)
        end_rows = df[df["date"] < end].tail(1)
        if start_rows.empty or end_rows.empty:
            continue

        s = start_rows.iloc[0]
        e = end_rows.iloc[0]

        borrowed_change = (e["total_borrowed"] - s["total_borrowed"]) / s["total_borrowed"] if s["total_borrowed"] > 0 else np.nan
        tvl_change = (e["total_tvl"] - s["total_tvl"]) / s["total_tvl"] if s["total_tvl"] > 0 else np.nan

        rows.append({
            "epoch": name,
            "regime": regime,
            "tvl_start": s["total_tvl"],
            "tvl_end": e["total_tvl"],
            "tvl_change_pct": tvl_change,
            "borrowed_start": s["total_borrowed"],
            "borrowed_end": e["total_borrowed"],
            "borrowed_change_pct": borrowed_change,
            "borrowed_eth_start": s["borrowed_eth"],
            "borrowed_eth_end": e["borrowed_eth"],
            "utilization_start": s["utilization_rate"],
            "utilization_end": e["utilization_rate"],
            "eth_price_start": s["eth_price"],
            "eth_price_end": e["eth_price"],
        })

    return pd.DataFrame(rows)


def test_recharge_model(epoch_summary: pd.DataFrame):
    """Test: does pre-crash borrowed correlate with liquidation volume?"""
    # Load liquidation summary
    liq = pd.read_csv(DATA_DIR / "epoch_liquidation_summary.csv")
    liq_real = liq[(liq["category_filter"] == "real")].copy()
    liq_real = liq_real[["epoch", "total_liquidation_usd", "event_count"]]

    crash = epoch_summary[epoch_summary["regime"] == "crash"].copy()
    merged = crash.merge(liq_real, on="epoch", how="inner")

    print("\n" + "=" * 90)
    print("RECHARGE MODEL TEST — Pre-crash leverage vs liquidation volume")
    print("=" * 90)
    print(f"\n{'Epoch':<22s} {'Borrowed $':>14s} {'Borrowed ETH':>14s} {'Liq Vol $':>14s} {'Events':>7s} {'Util':>6s}")
    for _, r in merged.iterrows():
        print(f"{r['epoch']:<22s} ${r['borrowed_start']:>13,.0f} {r['borrowed_eth_start']:>13,.0f} "
              f"${r['total_liquidation_usd']:>13,.0f} {r['event_count']:>7,.0f} {r['utilization_start']:>5.1%}")

    # Correlations
    if len(merged) >= 3:
        corr_usd = merged["borrowed_start"].corr(merged["total_liquidation_usd"])
        corr_eth = merged["borrowed_eth_start"].corr(merged["total_liquidation_usd"])
        corr_util = merged["utilization_start"].corr(merged["total_liquidation_usd"])
        corr_bor_change = merged["borrowed_change_pct"].corr(merged["total_liquidation_usd"])

        print(f"\nCorrelations (n={len(merged)} crash epochs):")
        print(f"  borrowed_start (USD) vs liq_volume:    r = {corr_usd:.3f}")
        print(f"  borrowed_start (ETH) vs liq_volume:    r = {corr_eth:.3f}")
        print(f"  utilization_start    vs liq_volume:    r = {corr_util:.3f}")
        print(f"  borrowed_change_pct  vs liq_volume:    r = {corr_bor_change:.3f}")

        if corr_usd > 0.7:
            print("  → STRONG: Pre-crash leverage level predicts liquidation volume")
        elif corr_usd > 0.4:
            print("  → MODERATE: Some signal from pre-crash leverage")
        else:
            print("  → WEAK: Pre-crash leverage alone doesn't predict liquidation volume")

        # Also test borrowed_eth to remove price-level confound
        if corr_eth > corr_usd + 0.05:
            print("  → ETH-denominated measure is stronger (price-level confound removed)")
        elif corr_usd > corr_eth + 0.05:
            print("  → USD-denominated measure is stronger (USD volume matters)")

    # Also test deleveraging magnitude
    print(f"\nDeleveraging during crashes:")
    for _, r in merged.iterrows():
        print(f"  {r['epoch']:<22s} borrowed Δ = {r['borrowed_change_pct']:>7.1%}  "
              f"tvl Δ = {r['tvl_change_pct']:>7.1%}  "
              f"util: {r['utilization_start']:.1%} → {r['utilization_end']:.1%}")


def print_utilization_dynamics(epoch_summary: pd.DataFrame):
    print("\n" + "=" * 90)
    print("UTILIZATION RATE DYNAMICS")
    print("=" * 90)
    print(f"\n{'Epoch':<22s} {'Regime':>7s} {'Util Start':>10s} {'Util End':>10s} {'Δ Util':>10s} {'TVL Δ%':>8s} {'Bor Δ%':>8s}")
    for _, r in epoch_summary.iterrows():
        delta = r["utilization_end"] - r["utilization_start"]
        print(f"{r['epoch']:<22s} {r['regime']:>7s} {r['utilization_start']:>9.1%} "
              f"{r['utilization_end']:>9.1%} {delta*100:>+8.1f}pp  "
              f"{r['tvl_change_pct']:>+7.1%} {r['borrowed_change_pct']:>+7.1%}")

    # Summarize patterns
    crashes = epoch_summary[epoch_summary["regime"] == "crash"]
    bulls = epoch_summary[epoch_summary["regime"] == "bull"]

    crash_util_delta = crashes["utilization_end"].values - crashes["utilization_start"].values
    bull_util_delta = bulls["utilization_end"].values - bulls["utilization_start"].values

    print(f"\nAvg utilization change — crashes: {crash_util_delta.mean():+.1%}")
    print(f"Avg utilization change — bulls:   {bull_util_delta.mean():+.1%}")


def main():
    print("Pulling protocol data from DefiLlama...")
    daily = pull_protocol_data()
    daily = merge_price(daily)
    daily.to_csv(DATA_DIR / "protocol_metrics_daily.csv", index=False)
    print(f"Daily metrics: {len(daily)} rows, {daily['date'].min()} to {daily['date'].max()}")

    # Quick sanity
    print(f"\nLatest values:")
    last = daily.iloc[-1]
    print(f"  Total TVL: ${last['total_tvl']:,.0f}")
    print(f"  Total Borrowed: ${last['total_borrowed']:,.0f}")
    print(f"  Utilization: {last['utilization_rate']:.1%}")
    print(f"  Borrowed ETH: {last['borrowed_eth']:,.0f}")

    # Epoch summary
    epoch_sum = epoch_boundary_summary(daily)
    epoch_sum.to_csv(DATA_DIR / "protocol_epoch_summary.csv", index=False)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 220)
    print("\n" + "=" * 90)
    print("PROTOCOL METRICS — EPOCH BOUNDARY SUMMARY")
    print("=" * 90)
    pd.set_option("display.float_format", lambda x: f"{x:,.0f}" if abs(x) > 100 else f"{x:.3f}")
    cols = ["epoch", "regime", "tvl_start", "tvl_end", "borrowed_start", "borrowed_end",
            "borrowed_change_pct", "borrowed_eth_start", "borrowed_eth_end",
            "utilization_start", "utilization_end"]
    print(epoch_sum[cols].to_string(index=False))

    # Recharge model test
    test_recharge_model(epoch_sum)

    # Utilization dynamics
    print_utilization_dynamics(epoch_sum)


if __name__ == "__main__":
    main()
