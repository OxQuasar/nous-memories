"""
Liquidation Walls: Pull ETH liquidation map from DefiLlama,
build price-bucketed histogram, identify major walls.

Data source: DefiLlama frontend (SSR data from /liquidations/eth).
No historical data available from this source — current snapshot only.
"""

import json
import os
import re
import urllib.request
from datetime import datetime, timezone

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

LIQUIDATIONS_URL = "https://defillama.com/liquidations/eth"
BINS_FILE = os.path.join(DATA_DIR, "liquidation_bins.csv")
TOP_POS_FILE = os.path.join(DATA_DIR, "liquidation_top_positions.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "liquidation_walls_results.txt")

# Aggregate nearby bins into clusters
CLUSTER_RANGE_USD = 200  # cluster bins within $200 of each other


def fetch_liquidation_data() -> dict:
    """Scrape DefiLlama liquidations page SSR data."""
    req = urllib.request.Request(LIQUIDATIONS_URL, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    match = re.search(r"__NEXT_DATA__[^{]*({.+?})</script>", html)
    if not match:
        raise RuntimeError("Could not find __NEXT_DATA__ in page")

    nd = json.loads(match.group(1))
    return nd["props"]["pageProps"]["data"]


def build_bin_table(data: dict) -> pd.DataFrame:
    """Convert bin data into a price-indexed DataFrame."""
    bin_size = data["binSize"]
    current_price = data["currentPrice"]
    n_bins = data["totalBins"]

    rows = []
    # Aggregate across all chains
    all_chains = data["chartDataBins"]["chains"]
    for bin_idx in range(n_bins):
        price_low = bin_idx * bin_size
        price_mid = (bin_idx + 0.5) * bin_size
        total_usd = 0
        total_native = 0
        for chain_data in all_chains.values():
            b = chain_data["bins"].get(str(bin_idx), {})
            total_usd += b.get("usd", 0)
            total_native += b.get("native", 0)
        rows.append({
            "bin": bin_idx,
            "price_low": price_low,
            "price_mid": price_mid,
            "price_high": price_low + bin_size,
            "usd": total_usd,
            "native_eth": total_native,
        })

    df = pd.DataFrame(rows)
    df["pct_from_current"] = (df["price_mid"] - current_price) / current_price * 100
    return df


def build_protocol_breakdown(data: dict) -> pd.DataFrame:
    """Per-protocol aggregate liquidation data."""
    tl = data["totalLiquidables"]["protocols"]
    dp = data["dangerousPositionsAmounts"]["protocols"]
    rows = []
    for proto in tl:
        rows.append({
            "protocol": proto,
            "total_liquidable_usd": tl.get(proto, 0),
            "dangerous_usd": dp.get(proto, 0),
        })
    df = pd.DataFrame(rows).sort_values("total_liquidable_usd", ascending=False)
    return df


def find_walls(bins_df: pd.DataFrame, current_price: float, n: int = 10) -> list[str]:
    """Identify top N price levels with most concentrated liquidations below current price."""
    below = bins_df[bins_df["price_mid"] < current_price].copy()
    below = below.sort_values("usd", ascending=False).head(n)

    lines = []
    lines.append(f"  {'Price Range':>22s}  {'Liquidatable':>14s}  {'ETH Amount':>12s}  {'Drop Required':>14s}")
    for _, row in below.iterrows():
        lines.append(
            f"  ${row['price_low']:>8,.0f}-${row['price_high']:>7,.0f}"
            f"  ${row['usd']/1e6:>11.1f}M"
            f"  {row['native_eth']:>10,.0f}"
            f"  {row['pct_from_current']:>12.1f}%"
        )
    return lines


def top_positions_table(data: dict, n: int = 15) -> tuple[list[str], pd.DataFrame]:
    """Format top individual positions."""
    positions = data.get("topPositions", [])
    if not positions:
        return ["  No position data available."], pd.DataFrame()

    rows = []
    for p in positions[:n]:
        rows.append({
            "liq_price": p.get("liqPrice", 0),
            "collateral_value_usd": p.get("collateralValue", 0),
            "collateral_eth": p.get("collateralAmount", 0),
            "protocol": p.get("protocol", ""),
            "chain": p.get("chain", ""),
            "address": p.get("displayName", ""),
        })
    df = pd.DataFrame(rows)

    current_price = data["currentPrice"]
    df["pct_from_current"] = (df["liq_price"] - current_price) / current_price * 100

    lines = []
    lines.append(f"  {'Liq Price':>10s}  {'Collateral':>12s}  {'ETH':>10s}  {'Drop %':>8s}  {'Protocol':>10s}  Address")
    for _, r in df.iterrows():
        lines.append(
            f"  ${r['liq_price']:>9,.0f}"
            f"  ${r['collateral_value_usd']/1e6:>9.1f}M"
            f"  {r['collateral_eth']:>9,.0f}"
            f"  {r['pct_from_current']:>7.1f}%"
            f"  {r['protocol']:>10s}"
            f"  {r['address']}"
        )

    return lines, df


def cumulative_liquidation_at_drops(bins_df: pd.DataFrame, current_price: float) -> list[str]:
    """What total liquidation volume hits at various % drops from current price."""
    lines = []
    for drop_pct in [5, 10, 15, 20, 25, 30, 40, 50, 60, 75]:
        threshold = current_price * (1 - drop_pct / 100)
        mask = bins_df["price_mid"] >= threshold
        total = bins_df.loc[~mask, "usd"].sum()
        lines.append(f"  {drop_pct:>3d}% drop (→${threshold:>7,.0f}):  ${total/1e6:>10.1f}M cumulative liquidations")
    return lines


def analyze(data: dict) -> str:
    """Full analysis, return summary text."""
    lines = []
    ts = datetime.fromtimestamp(data["time"], tz=timezone.utc)
    current_price = data["currentPrice"]

    lines.append(f"Snapshot time: {ts.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"Current ETH price: ${current_price:,.2f}")
    lines.append(f"Total liquidatable: ${data['totalLiquidable']/1e6:,.1f}M")
    lines.append(f"Dangerous positions (near liquidation): ${data['dangerousPositionsAmount']/1e6:,.1f}M")
    lines.append(f"Bad debt: ${data['badDebts']/1e6:,.1f}M")
    lines.append(f"Total tracked positions: {data.get('totalPositions', 'N/A')}")
    lines.append(f"Bin size: ${data['binSize']:,.2f}")
    lines.append("")

    # Protocol breakdown
    proto_df = build_protocol_breakdown(data)
    lines.append("=== PROTOCOL BREAKDOWN ===")
    lines.append(f"  {'Protocol':>20s}  {'Total Liquidatable':>18s}  {'Dangerous':>14s}")
    for _, r in proto_df.iterrows():
        if r["total_liquidable_usd"] < 100_000:
            continue
        lines.append(
            f"  {r['protocol']:>20s}"
            f"  ${r['total_liquidable_usd']/1e6:>15.1f}M"
            f"  ${r['dangerous_usd']/1e6:>11.1f}M"
        )
    lines.append("")

    # Build bins
    bins_df = build_bin_table(data)

    # Top walls
    lines.append("=== TOP 10 LIQUIDATION WALLS (largest bins below current price) ===")
    lines.extend(find_walls(bins_df, current_price))
    lines.append("")

    # Cumulative at various drops
    lines.append("=== CUMULATIVE LIQUIDATION AT PRICE DROPS ===")
    lines.extend(cumulative_liquidation_at_drops(bins_df, current_price))
    lines.append("")

    # Top individual positions
    lines.append("=== TOP 15 INDIVIDUAL POSITIONS ===")
    pos_lines, pos_df = top_positions_table(data)
    lines.extend(pos_lines)
    lines.append("")

    # Verdict
    lines.append("=== VERDICT ===")
    lines.append("Data access: DefiLlama SSR page data — current snapshot only, no historical.")
    lines.append("  → Can build current liquidation map but CANNOT backtest cascade behavior.")
    lines.append("  → Historical liquidation events would need Dune (API key) or Aave subgraph (Graph API key).")
    lines.append("")

    # Key observations
    below = bins_df[bins_df["price_mid"] < current_price]
    biggest = below.nlargest(3, "usd")
    lines.append("Key observations:")
    for _, row in biggest.iterrows():
        lines.append(
            f"  • ${row['usd']/1e6:.0f}M wall at ${row['price_low']:,.0f}-${row['price_high']:,.0f}"
            f" ({row['pct_from_current']:.0f}% below current)"
        )

    total_below_10pct = below[below["pct_from_current"] >= -10]["usd"].sum()
    total_below_25pct = below[below["pct_from_current"] >= -25]["usd"].sum()
    lines.append(f"  • Within 10% drop: ${total_below_10pct/1e6:.0f}M liquidatable")
    lines.append(f"  • Within 25% drop: ${total_below_25pct/1e6:.0f}M liquidatable")
    lines.append("")
    lines.append("Signal usability: MONITOR-ONLY (no backtest possible from free data)")
    lines.append("  The liquidation map shows WHERE cascades could happen.")
    lines.append("  Without historical data, we cannot test IF they actually cascade or absorb.")

    return "\n".join(lines)


def main():
    print("Fetching liquidation data from DefiLlama...")
    data = fetch_liquidation_data()
    print(f"  Current price: ${data['currentPrice']:,.2f}")
    print(f"  Total liquidatable: ${data['totalLiquidable']/1e6:,.1f}M")
    print(f"  Positions tracked: {data.get('totalPositions', 'N/A')}")
    print()

    # Save bin data
    bins_df = build_bin_table(data)
    bins_df.to_csv(BINS_FILE, index=False)
    print(f"Bins saved → {BINS_FILE}")

    # Save top positions
    positions = data.get("topPositions", [])
    if positions:
        pos_df = pd.DataFrame(positions)
        pos_df.to_csv(TOP_POS_FILE, index=False)
        print(f"Top positions saved → {TOP_POS_FILE}")
    print()

    # Run analysis
    summary = analyze(data)
    print(summary)

    with open(RESULTS_FILE, "w") as f:
        f.write(summary + "\n")
    print(f"\nResults saved → {RESULTS_FILE}")


if __name__ == "__main__":
    main()
