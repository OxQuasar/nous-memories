"""
Pull historical Aave v2/v3 WETH-collateral liquidation events from on-chain logs.
Aggregate daily, test cascade vs absorption behavior.

Data source: Free public Ethereum RPC (eth_getLogs on Aave Pool contracts).
"""

import json
import os
import time
import urllib.request
from datetime import datetime, timezone

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

RPC_URL = "https://eth.llamarpc.com"
FALLBACK_RPC = "https://ethereum-rpc.publicnode.com"

# Aave contracts
AAVE_V2_POOL = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
AAVE_V3_POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"

# LiquidationCall event signature
LIQUIDATION_TOPIC = "0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286"
# WETH as topic1 (collateral asset, indexed, zero-padded to 32 bytes)
WETH_TOPIC = "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

# Block ranges
V2_START_BLOCK = 14_000_000  # ~Jan 2022
V3_START_BLOCK = 16_300_000  # ~Jan 2023 (v3 deployment)
CHUNK_SIZE = 100_000  # llamarpc allows 100k
FALLBACK_CHUNK = 50_000  # publicnode limit

WETH_DECIMALS = 18
RAW_EVENTS_FILE = os.path.join(DATA_DIR, "liquidation_events_raw.csv")
DAILY_FILE = os.path.join(DATA_DIR, "liquidation_events.csv")
ETH_PRICE_FILE = os.path.join(DATA_DIR, "eth_price.csv")
ETH_PRICE_1H_FILE = os.path.join(DATA_DIR, "eth_price_1h.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "liquidation_events_results.txt")


def rpc_call(method: str, params: list, rpc: str = RPC_URL, retries: int = 3) -> dict:
    """Make JSON-RPC call with retries and fallback."""
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    for attempt in range(retries):
        url = rpc if attempt < retries - 1 else FALLBACK_RPC
        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": "application/json",
            "User-Agent": "signals/0.1",
        })
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read())
            if "error" in data:
                raise RuntimeError(f"RPC error: {data['error']}")
            return data
        except Exception as e:
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"    retry {attempt+1} in {wait}s ({e})")
                time.sleep(wait)
            else:
                raise


def get_current_block() -> int:
    data = rpc_call("eth_blockNumber", [])
    return int(data["result"], 16)


def pull_events(contract: str, start_block: int, end_block: int, label: str) -> list[dict]:
    """Pull all WETH-collateral liquidation events for a contract."""
    all_events = []
    cursor = start_block

    # Resume from existing raw file
    if os.path.exists(RAW_EVENTS_FILE):
        existing = pd.read_csv(RAW_EVENTS_FILE)
        contract_events = existing[existing["contract"] == contract]
        if len(contract_events) > 0:
            last_block = int(contract_events["block_number"].max())
            if last_block > cursor:
                cursor = last_block + 1
                print(f"  [{label}] resuming from block {cursor} ({len(contract_events)} existing events)")

    chunk = CHUNK_SIZE
    while cursor < end_block:
        to_block = min(cursor + chunk - 1, end_block)
        pct = (cursor - start_block) / max(end_block - start_block, 1) * 100
        print(f"  [{label}] {pct:5.1f}% block {cursor}..{to_block}", end=" ", flush=True)

        try:
            data = rpc_call("eth_getLogs", [{
                "address": contract,
                "topics": [LIQUIDATION_TOPIC, WETH_TOPIC],
                "fromBlock": hex(cursor),
                "toBlock": hex(to_block),
            }])
        except Exception as e:
            # If chunk too large, halve it
            if chunk > 10_000:
                chunk = chunk // 2
                print(f"reducing chunk to {chunk}")
                continue
            raise

        logs = data["result"]
        for log in logs:
            block_num = int(log["blockNumber"], 16)
            ts_hex = log.get("blockTimestamp")
            ts = int(ts_hex, 16) if ts_hex else 0

            # Decode liquidatedCollateralAmount from data (bytes 32-64)
            data_hex = log["data"][2:]
            liq_collateral_raw = int(data_hex[64:128], 16)
            liq_collateral_eth = liq_collateral_raw / 10**WETH_DECIMALS

            all_events.append({
                "block_number": block_num,
                "timestamp": ts,
                "collateral_eth": liq_collateral_eth,
                "tx_hash": log["transactionHash"],
                "contract": contract,
            })

        print(f"{len(logs)} events")
        cursor = to_block + 1
        time.sleep(0.3)

    return all_events


def pull_all_events() -> pd.DataFrame:
    """Pull from both Aave v2 and v3."""
    current_block = get_current_block()
    print(f"Current block: {current_block}")

    events = []
    events.extend(pull_events(AAVE_V2_POOL, V2_START_BLOCK, current_block, "v2"))
    events.extend(pull_events(AAVE_V3_POOL, V3_START_BLOCK, current_block, "v3"))

    df = pd.DataFrame(events)
    if len(df) == 0:
        return df

    # Merge with any existing data
    if os.path.exists(RAW_EVENTS_FILE):
        existing = pd.read_csv(RAW_EVENTS_FILE)
        df = pd.concat([existing, df], ignore_index=True)

    df = df.drop_duplicates(subset=["tx_hash", "block_number"]).sort_values("block_number")
    df.to_csv(RAW_EVENTS_FILE, index=False)
    print(f"Raw events: {len(df)} → {RAW_EVENTS_FILE}")
    return df


def fill_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing timestamps using block number interpolation."""
    has_ts = df[df["timestamp"] > 0]
    if len(has_ts) == 0:
        return df

    # Simple linear interpolation: timestamp ~ block_number
    from numpy.polynomial import polynomial as P
    coeffs = np.polyfit(has_ts["block_number"].values, has_ts["timestamp"].values, 1)
    missing = df["timestamp"] == 0
    if missing.any():
        df.loc[missing, "timestamp"] = np.polyval(coeffs, df.loc[missing, "block_number"].values).astype(int)
    return df


def build_daily(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to daily liquidation volumes, merge with ETH price."""
    df = raw_df.copy()
    df = fill_timestamps(df)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%d")

    daily = df.groupby("date").agg(
        event_count=("collateral_eth", "count"),
        total_eth=("collateral_eth", "sum"),
    ).reset_index()

    # Merge with ETH price for USD conversion
    eth_price = pd.read_csv(ETH_PRICE_FILE)
    eth_price["date"] = eth_price["date"].astype(str)
    daily = daily.merge(eth_price[["date", "price"]], on="date", how="left")
    daily["price"] = daily["price"].ffill()
    daily["total_usd"] = daily["total_eth"] * daily["price"]

    # Fill missing days with 0
    all_dates = pd.date_range(daily["date"].min(), daily["date"].max(), freq="D")
    full = pd.DataFrame({"date": all_dates.strftime("%Y-%m-%d")})
    daily = full.merge(daily, on="date", how="left").fillna(0)

    # Re-merge price for days with no liquidations
    daily = daily.drop(columns=["price"], errors="ignore")
    daily = daily.merge(eth_price[["date", "price"]], on="date", how="left")
    daily["price"] = daily["price"].ffill().bfill()

    daily.to_csv(DAILY_FILE, index=False)
    print(f"Daily aggregated: {len(daily)} days → {DAILY_FILE}")
    return daily


def analyze(daily: pd.DataFrame) -> str:
    """Run cascade vs absorption analysis."""
    lines = []
    lines.append(f"Data: {daily['date'].iloc[0]} to {daily['date'].iloc[-1]} ({len(daily)} days)")
    lines.append(f"Total liquidation events: {daily['event_count'].sum():.0f}")
    lines.append(f"Total ETH liquidated: {daily['total_eth'].sum():,.0f} ETH")
    lines.append(f"Total USD liquidated: ${daily['total_usd'].sum()/1e6:,.1f}M")
    lines.append(f"Days with liquidations: {(daily['event_count'] > 0).sum()} / {len(daily)}")
    lines.append("")

    # Forward returns
    for horizon in [1, 3, 7, 14]:
        daily[f"fwd_{horizon}d"] = daily["price"].shift(-horizon) / daily["price"] - 1

    # Unconditional baseline
    lines.append("=== UNCONDITIONAL BASELINE ===")
    for horizon in [1, 3, 7, 14]:
        col = f"fwd_{horizon}d"
        vals = daily[col].dropna()
        lines.append(
            f"  {horizon:>2d}d: mean={vals.mean():+.3%}, median={vals.median():+.3%},"
            f" %neg={100*(vals < 0).mean():.1f}%"
        )
    lines.append("")

    # A. Cascade vs absorption at various thresholds
    active_days = daily[daily["total_usd"] > 0]
    if len(active_days) < 20:
        lines.append("Insufficient liquidation data for threshold analysis.")
        return "\n".join(lines)

    lines.append("=== A. CASCADE vs ABSORPTION TEST ===")
    lines.append("(Forward ETH returns after high-liquidation days)")
    lines.append("")

    for pct_label, pct in [("75th", 75), ("90th", 90), ("95th", 95), ("99th", 99)]:
        threshold = np.percentile(active_days["total_usd"], pct)
        spike_days = daily[daily["total_usd"] >= threshold]
        if len(spike_days) < 3:
            continue

        lines.append(f"  {pct_label} percentile: ≥${threshold/1e6:.1f}M ({len(spike_days)} days)")
        lines.append(f"  {'Horizon':>10s}  {'Mean':>8s}  {'Median':>8s}  {'% Neg':>8s}  {'Count':>6s}")
        for horizon in [1, 3, 7, 14]:
            col = f"fwd_{horizon}d"
            vals = spike_days[col].dropna()
            if len(vals) == 0:
                continue
            lines.append(
                f"  {horizon:>8d}d  {vals.mean():+8.3%}  {vals.median():+8.3%}"
                f"  {100*(vals < 0).mean():7.1f}%  {len(vals):>6d}"
            )
        lines.append("")

    # B. Clustering test
    lines.append("=== B. LIQUIDATION CLUSTERING ===")
    lines.append("(Autocorrelation of daily liquidation volume)")
    active_vol = daily["total_usd"].values
    mean_vol = active_vol.mean()
    var_vol = active_vol.var()
    if var_vol > 0:
        for lag in range(1, 8):
            n = len(active_vol)
            autocorr = np.sum((active_vol[:n-lag] - mean_vol) * (active_vol[lag:] - mean_vol)) / (n * var_vol)
            lines.append(f"  lag {lag}d: autocorr = {autocorr:+.3f}")
    lines.append("")

    # C. Top liquidation days
    lines.append("=== C. TOP 15 LIQUIDATION DAYS ===")
    top = daily.nlargest(15, "total_usd")
    lines.append(f"  {'Date':>12s}  {'Volume':>12s}  {'Events':>8s}  {'ETH Price':>10s}  {'7d Fwd':>8s}")
    for _, row in top.iterrows():
        fwd = f"{row['fwd_7d']:+.2%}" if pd.notna(row["fwd_7d"]) else "N/A"
        lines.append(
            f"  {row['date']:>12s}  ${row['total_usd']/1e6:>9.1f}M"
            f"  {row['event_count']:>8.0f}"
            f"  ${row['price']:>9,.0f}"
            f"  {fwd:>8s}"
        )
    lines.append("")

    # D. Overall verdict
    lines.append("=== VERDICT ===")

    # Use 90th percentile as the key threshold
    threshold_90 = np.percentile(active_days["total_usd"], 90)
    spikes = daily[daily["total_usd"] >= threshold_90]
    if len(spikes) > 0:
        fwd_7d = spikes["fwd_7d"].dropna()
        baseline_7d = daily["fwd_7d"].dropna()
        spike_mean = fwd_7d.mean()
        base_mean = baseline_7d.mean()
        spike_neg = (fwd_7d < 0).mean()
        base_neg = (baseline_7d < 0).mean()

        if spike_mean < base_mean and spike_neg > base_neg + 0.05:
            verdict = "CASCADE"
            desc = "High liquidation days are followed by worse-than-average returns → cascading behavior"
        elif spike_mean > base_mean and spike_neg < base_neg - 0.05:
            verdict = "ABSORPTION"
            desc = "High liquidation days are followed by better-than-average returns → clearing/bounce behavior"
        else:
            verdict = "MIXED"
            desc = "No clear directional signal from liquidation spikes"

        lines.append(f"  Signal: {verdict}")
        lines.append(f"  {desc}")
        lines.append(f"  Spike 7d mean: {spike_mean:+.3%} vs baseline 7d mean: {base_mean:+.3%}")
        lines.append(f"  Spike 7d %neg: {spike_neg:.1%} vs baseline 7d %neg: {base_neg:.1%}")

    return "\n".join(lines)


def main():
    print("=== DATA ACCESS EXPLORATION ===")
    print()
    print("Option A (DefiLlama liquidations API): FAILED — 500 error on all endpoints")
    print("Option B (Aave subgraph/The Graph): FAILED — hosted service deprecated, decentralized requires API key")
    print("Option C (Dune Analytics): FAILED — requires API key (401)")
    print("Option D (On-chain event logs via free RPC): SUCCESS ✓")
    print("  → Using eth.llamarpc.com (free, 100k block range)")
    print("  → Pulling Aave v2+v3 LiquidationCall events for WETH collateral")
    print()

    print("Pulling liquidation events from on-chain logs...")
    raw_df = pull_all_events()

    if len(raw_df) == 0:
        print("No events found!")
        return

    print(f"\nTotal raw events: {len(raw_df)}")
    print()

    print("Building daily aggregation...")
    daily = build_daily(raw_df)
    print()

    print("Analyzing cascade vs absorption...")
    summary = analyze(daily)
    print()
    print(summary)

    with open(RESULTS_FILE, "w") as f:
        f.write("=== DATA ACCESS RESULTS ===\n")
        f.write("Option A (DefiLlama liquidations API): FAILED — 500 error\n")
        f.write("Option B (Aave subgraph/The Graph): FAILED — deprecated / requires API key\n")
        f.write("Option C (Dune Analytics): FAILED — requires API key\n")
        f.write("Option D (On-chain event logs via free RPC): SUCCESS\n\n")
        f.write(summary + "\n")
    print(f"\nResults saved → {RESULTS_FILE}")


if __name__ == "__main__":
    main()
