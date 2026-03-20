"""
Expand liquidation events with Compound v2/v3 + Maker data.
Merge with existing Aave events and rerun concentration ratio test.

Data source: Free public Ethereum RPC (eth_getLogs).
"""

import json
import os
import time
import urllib.request
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# RPCs — try llamarpc first, publicnode as fallback (50k block limit)
RPCS = ["https://eth.llamarpc.com", "https://ethereum-rpc.publicnode.com"]
CHUNK_SIZES = {RPCS[0]: 100_000, RPCS[1]: 50_000}

# --- Contract / event config ---

# Compound v2: LiquidateBorrow across major debt markets, filter for cETH collateral
COMP_V2_TOPIC = "0x298637f684da70674f26509b10f07ec2fbc77a335ab1e7d6215a4b2484d8bb52"
COMP_V2_MARKETS = [
    "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643",  # cDAI
    "0x39AA39c021dfbaE8faC545936693aC917d5E7563",  # cUSDC
    "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9",  # cUSDT
]
CETH_ADDR = "0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5"
# Underlying decimals for repayAmount conversion to USD
COMP_V2_DECIMALS = {
    "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643": 18,  # DAI
    "0x39aa39c021dfbae8fac545936693ac917d5e7563": 6,   # USDC
    "0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9": 6,   # USDT
}

# Compound v3: AbsorbCollateral on Comet USDC market
COMP_V3_COMET = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"
COMP_V3_TOPIC = "0x9850ab1af75177e4a9201c65a2cf7976d5d28e40ef63494b44366f86b2f9412e"
WETH_TOPIC = "0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

# Maker Dog: Bark for ETH-A/B/C ilks
MAKER_DOG = "0x135954d155898D42C90D2a57824C690e0c7BEf1B"
MAKER_TOPIC = "0x85258d09e1e4ef299ff3fc11e74af99563f022d21f3f940db982229dc2a3358c"
ETH_ILKS = {
    "ETH-A": "0x4554482d41000000000000000000000000000000000000000000000000000000",
    "ETH-B": "0x4554482d42000000000000000000000000000000000000000000000000000000",
    "ETH-C": "0x4554482d43000000000000000000000000000000000000000000000000000000",
}

START_BLOCK = 14_000_000  # ~Jan 2022
COMP_V3_START = 15_800_000  # v3 Comet deployed ~Nov 2022

# Files
COMP_RAW_FILE = os.path.join(DATA_DIR, "liquidation_compound_raw.csv")
MAKER_RAW_FILE = os.path.join(DATA_DIR, "liquidation_maker_raw.csv")
AAVE_RAW_FILE = os.path.join(DATA_DIR, "liquidation_events_raw.csv")
ETH_PRICE_FILE = os.path.join(DATA_DIR, "eth_price.csv")
COMBINED_FILE = os.path.join(DATA_DIR, "liquidation_events_combined.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "liquidation_expand_results.txt")

CONCENTRATION_THRESHOLD = 0.5
TRAILING_WINDOW = 7


def rpc_call(method: str, params: list, retries: int = 3) -> dict:
    """JSON-RPC call with retries across RPCs."""
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    for attempt in range(retries):
        rpc = RPCS[min(attempt, len(RPCS) - 1)]
        req = urllib.request.Request(rpc, data=payload, headers={
            "Content-Type": "application/json", "User-Agent": "signals/0.1",
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
    return int(rpc_call("eth_blockNumber", [])["result"], 16)


def get_chunk_size() -> int:
    """Test which RPC is available and return its chunk size."""
    for rpc, chunk in CHUNK_SIZES.items():
        try:
            payload = json.dumps({"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}).encode()
            req = urllib.request.Request(rpc, data=payload, headers={
                "Content-Type": "application/json", "User-Agent": "signals/0.1"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                json.loads(resp.read())
            return chunk
        except Exception:
            continue
    return 50_000  # safe default


def pull_logs(address: str | list[str], topics: list, start: int, end: int, label: str,
              resume_file: str = None, resume_key: str = None) -> list[dict]:
    """Generic log puller with resume support."""
    cursor = start
    chunk = get_chunk_size()

    # Resume
    if resume_file and os.path.exists(resume_file) and resume_key:
        existing = pd.read_csv(resume_file)
        subset = existing[existing["source"] == resume_key] if "source" in existing.columns else existing
        if len(subset) > 0:
            last_block = int(subset["block_number"].max())
            if last_block >= cursor:
                cursor = last_block + 1
                print(f"  [{label}] resuming from block {cursor} ({len(subset)} existing)")

    all_logs = []
    params_base = {"topics": topics}
    if isinstance(address, list):
        params_base["address"] = address
    else:
        params_base["address"] = address

    while cursor <= end:
        to_block = min(cursor + chunk - 1, end)
        pct = (cursor - start) / max(end - start, 1) * 100
        print(f"  [{label}] {pct:5.1f}% block {cursor}..{to_block}", end=" ", flush=True)

        try:
            params = {**params_base, "fromBlock": hex(cursor), "toBlock": hex(to_block)}
            data = rpc_call("eth_getLogs", [params])
        except Exception as e:
            if chunk > 10_000:
                chunk = chunk // 2
                print(f"reducing chunk to {chunk}")
                continue
            raise

        logs = data["result"]
        print(f"{len(logs)} events")
        all_logs.extend(logs)
        cursor = to_block + 1
        time.sleep(0.3)

    return all_logs


# --- Compound v2 ---

def pull_compound_v2(end_block: int) -> pd.DataFrame:
    """Pull Compound v2 LiquidateBorrow events with cETH collateral."""
    print("Pulling Compound v2 events...")
    rows = []

    for market in COMP_V2_MARKETS:
        market_lower = market.lower()
        decimals = COMP_V2_DECIMALS[market_lower]
        logs = pull_logs(market, [COMP_V2_TOPIC], START_BLOCK, end_block,
                         f"comp-v2-{market[:8]}", COMP_RAW_FILE, f"comp_v2_{market_lower}")

        for log in logs:
            d = log["data"][2:]
            collateral = ("0x" + d[3*64+24:4*64]).lower()
            if collateral != CETH_ADDR:
                continue

            block_num = int(log["blockNumber"], 16)
            ts_hex = log.get("blockTimestamp")
            ts = int(ts_hex, 16) if ts_hex else 0

            repay_raw = int(d[2*64:3*64], 16)
            repay_usd = repay_raw / 10**decimals  # stablecoins ≈ $1

            rows.append({
                "block_number": block_num,
                "timestamp": ts,
                "volume_usd": repay_usd,
                "tx_hash": log["transactionHash"],
                "source": f"comp_v2_{market_lower}",
                "protocol": "compound_v2",
            })

    df = pd.DataFrame(rows)
    if len(df) > 0:
        df = df.drop_duplicates(subset=["tx_hash", "block_number"]).sort_values("block_number")
    return df


# --- Compound v3 ---

def pull_compound_v3(end_block: int) -> pd.DataFrame:
    """Pull Compound v3 AbsorbCollateral events for WETH."""
    print("Pulling Compound v3 events...")
    # AbsorbCollateral: topics = [sig, absorber(indexed), borrower(indexed), asset(indexed)]
    # Filter asset = WETH via topic3
    logs = pull_logs(COMP_V3_COMET, [COMP_V3_TOPIC, None, None, WETH_TOPIC],
                     COMP_V3_START, end_block, "comp-v3", COMP_RAW_FILE, "comp_v3")

    rows = []
    for log in logs:
        block_num = int(log["blockNumber"], 16)
        ts_hex = log.get("blockTimestamp")
        ts = int(ts_hex, 16) if ts_hex else 0

        d = log["data"][2:]
        # data: [collateralAbsorbed (18 dec), usdValue (8 dec — Comet price scale)]
        usd_value = int(d[64:128], 16) / 1e8

        rows.append({
            "block_number": block_num,
            "timestamp": ts,
            "volume_usd": usd_value,
            "tx_hash": log["transactionHash"],
            "source": "comp_v3",
            "protocol": "compound_v3",
        })

    df = pd.DataFrame(rows)
    if len(df) > 0:
        df = df.drop_duplicates(subset=["tx_hash", "block_number"]).sort_values("block_number")
    return df


# --- Maker ---

def pull_maker(end_block: int) -> pd.DataFrame:
    """Pull Maker Dog Bark events for ETH ilks."""
    print("Pulling Maker events...")
    rows = []

    for ilk_name, ilk_topic in ETH_ILKS.items():
        logs = pull_logs(MAKER_DOG, [MAKER_TOPIC, ilk_topic], START_BLOCK, end_block,
                         f"maker-{ilk_name}", MAKER_RAW_FILE, f"maker_{ilk_name}")

        for log in logs:
            block_num = int(log["blockNumber"], 16)
            ts_hex = log.get("blockTimestamp")
            ts = int(ts_hex, 16) if ts_hex else 0

            d = log["data"][2:]
            ink_raw = int(d[0:64], 16)  # WAD, 18 decimals = ETH amount
            ink_eth = ink_raw / 1e18

            rows.append({
                "block_number": block_num,
                "timestamp": ts,
                "volume_eth": ink_eth,
                "tx_hash": log["transactionHash"],
                "source": f"maker_{ilk_name}",
                "protocol": "maker",
            })

    df = pd.DataFrame(rows)
    if len(df) > 0:
        df = df.drop_duplicates(subset=["tx_hash", "block_number"]).sort_values("block_number")
    return df


# --- Merge & Analyze ---

def fill_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing timestamps via linear interpolation from known ones."""
    has_ts = df[df["timestamp"] > 0]
    if len(has_ts) < 2:
        return df
    coeffs = np.polyfit(has_ts["block_number"].values, has_ts["timestamp"].values, 1)
    missing = df["timestamp"] == 0
    if missing.any():
        df.loc[missing, "timestamp"] = np.polyval(coeffs, df.loc[missing, "block_number"].values).astype(int)
    return df


def build_combined(comp_v2: pd.DataFrame, comp_v3: pd.DataFrame, maker: pd.DataFrame) -> pd.DataFrame:
    """Merge all protocols with existing Aave data into daily series."""
    eth_price = pd.read_csv(ETH_PRICE_FILE)
    eth_price["date"] = eth_price["date"].astype(str)

    # Load existing Aave raw
    aave_raw = pd.read_csv(AAVE_RAW_FILE)
    aave_raw = fill_timestamps(aave_raw)
    aave_raw["date"] = pd.to_datetime(aave_raw["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
    aave_raw = aave_raw.merge(eth_price[["date", "price"]], on="date", how="left")
    aave_raw["price"] = aave_raw["price"].ffill()
    aave_raw["volume_usd"] = aave_raw["collateral_eth"] * aave_raw["price"]
    aave_daily = aave_raw.groupby("date").agg(
        aave_usd=("volume_usd", "sum"),
        aave_count=("volume_usd", "count"),
    ).reset_index()

    # Compound v2 daily
    if len(comp_v2) > 0:
        comp_v2 = fill_timestamps(comp_v2)
        comp_v2["date"] = pd.to_datetime(comp_v2["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
        comp_v2_daily = comp_v2.groupby("date").agg(
            comp_v2_usd=("volume_usd", "sum"),
            comp_v2_count=("volume_usd", "count"),
        ).reset_index()
    else:
        comp_v2_daily = pd.DataFrame(columns=["date", "comp_v2_usd", "comp_v2_count"])

    # Compound v3 daily
    if len(comp_v3) > 0:
        comp_v3 = fill_timestamps(comp_v3)
        comp_v3["date"] = pd.to_datetime(comp_v3["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
        comp_v3_daily = comp_v3.groupby("date").agg(
            comp_v3_usd=("volume_usd", "sum"),
            comp_v3_count=("volume_usd", "count"),
        ).reset_index()
    else:
        comp_v3_daily = pd.DataFrame(columns=["date", "comp_v3_usd", "comp_v3_count"])

    # Maker daily — needs ETH price for USD conversion
    if len(maker) > 0:
        maker = fill_timestamps(maker)
        maker["date"] = pd.to_datetime(maker["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
        maker = maker.merge(eth_price[["date", "price"]], on="date", how="left")
        maker["price"] = maker["price"].ffill()
        maker["volume_usd"] = maker["volume_eth"] * maker["price"]
        maker_daily = maker.groupby("date").agg(
            maker_usd=("volume_usd", "sum"),
            maker_count=("volume_usd", "count"),
        ).reset_index()
    else:
        maker_daily = pd.DataFrame(columns=["date", "maker_usd", "maker_count"])

    # Merge all
    all_dates = pd.date_range("2022-01-01", pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d"), freq="D")
    combined = pd.DataFrame({"date": all_dates.strftime("%Y-%m-%d")})
    for src_df in [aave_daily, comp_v2_daily, comp_v3_daily, maker_daily]:
        if len(src_df) > 0:
            combined = combined.merge(src_df, on="date", how="left")
    combined = combined.fillna(0)

    # Total
    usd_cols = [c for c in combined.columns if c.endswith("_usd")]
    count_cols = [c for c in combined.columns if c.endswith("_count")]
    combined["total_usd"] = combined[usd_cols].sum(axis=1)
    combined["total_count"] = combined[count_cols].sum(axis=1)

    # Add ETH price
    combined = combined.merge(eth_price[["date", "price"]], on="date", how="left")
    combined["price"] = combined["price"].ffill().bfill()

    combined.to_csv(COMBINED_FILE, index=False)
    print(f"Combined daily: {len(combined)} days → {COMBINED_FILE}")
    return combined


def concentration_test(df: pd.DataFrame, label: str) -> list[str]:
    """Run concentration ratio test on a daily liquidation series."""
    lines = []
    df = df.copy().sort_values("date").reset_index(drop=True)

    # Forward returns
    for h in [1, 3, 7, 14]:
        df[f"fwd_{h}d"] = df["price"].shift(-h) / df["price"] - 1

    # Trailing 7d volume and concentration ratio
    df["trailing_7d"] = df["total_usd"].rolling(TRAILING_WINDOW, min_periods=1).sum()
    df["conc_ratio"] = df["total_usd"] / df["trailing_7d"].replace(0, np.nan)

    # Percentile thresholds (active days only)
    active = df[df["total_usd"] > 0]["total_usd"]
    if len(active) < 50:
        lines.append(f"  [{label}] Insufficient active days ({len(active)})")
        return lines

    p90 = np.percentile(active, 90)
    lines.append(f"  [{label}] 90th pctl threshold: ${p90/1e6:.2f}M, active days: {len(active)}")

    high = df[(df["total_usd"] >= p90) & df["conc_ratio"].notna()]
    conc = high[high["conc_ratio"] > CONCENTRATION_THRESHOLD]
    dist = high[high["conc_ratio"] <= CONCENTRATION_THRESHOLD]

    lines.append(f"  [{label}] High-liq days: {len(high)} (concentrated: {len(conc)}, distributed: {len(dist)})")
    lines.append("")

    for group_label, subset in [("Concentrated", conc), ("Distributed", dist)]:
        if len(subset) < 3:
            lines.append(f"  {group_label}: too few days ({len(subset)})")
            continue
        lines.append(f"  {group_label} (n={len(subset)}):")
        lines.append(f"  {'Horizon':>10s}  {'Mean':>8s}  {'Median':>8s}  {'% Neg':>8s}")
        for h in [1, 3, 7, 14]:
            vals = subset[f"fwd_{h}d"].dropna()
            if len(vals) == 0:
                continue
            lines.append(
                f"  {h:>8d}d  {vals.mean():+8.3%}  {vals.median():+8.3%}"
                f"  {100*(vals < 0).mean():7.1f}%"
            )
        lines.append("")

    # Significance test
    c7 = conc["fwd_7d"].dropna()
    d7 = dist["fwd_7d"].dropna()
    if len(c7) >= 5 and len(d7) >= 5:
        u_stat, p_val = stats.mannwhitneyu(c7, d7, alternative="two-sided")
        lines.append(f"  [{label}] 7d return Mann-Whitney: U={u_stat:.0f}, p={p_val:.4f}")
        lines.append(f"  [{label}] Concentrated 7d median: {c7.median():+.3%}, Distributed 7d median: {d7.median():+.3%}")
        diff = c7.median() - d7.median()
        lines.append(f"  [{label}] Spread: {diff:+.3%}")
    lines.append("")

    return lines


def main():
    end_block = get_current_block()
    print(f"Current block: {end_block}")
    print()

    # Pull new data
    comp_v2 = pull_compound_v2(end_block)
    print(f"  Compound v2: {len(comp_v2)} events")
    if len(comp_v2) > 0:
        # Save raw for resume
        comp_v2.to_csv(COMP_RAW_FILE, index=False)
    print()

    comp_v3 = pull_compound_v3(end_block)
    print(f"  Compound v3: {len(comp_v3)} events")
    if len(comp_v3) > 0:
        existing = pd.read_csv(COMP_RAW_FILE) if os.path.exists(COMP_RAW_FILE) else pd.DataFrame()
        pd.concat([existing, comp_v3]).to_csv(COMP_RAW_FILE, index=False)
    print()

    maker = pull_maker(end_block)
    print(f"  Maker: {len(maker)} events")
    if len(maker) > 0:
        maker.to_csv(MAKER_RAW_FILE, index=False)
    print()

    # Build combined
    print("Building combined daily series...")
    combined = build_combined(comp_v2, comp_v3, maker)
    print()

    # Summary stats
    lines = []
    lines.append("=== DATA SUMMARY ===")
    for col in [c for c in combined.columns if c.endswith("_usd") and c != "total_usd"]:
        proto = col.replace("_usd", "")
        total = combined[col].sum()
        days_active = (combined[col] > 0).sum()
        lines.append(f"  {proto:>12s}: ${total/1e6:>8.1f}M total, {days_active:>5d} active days")
    total = combined["total_usd"].sum()
    days_active = (combined["total_usd"] > 0).sum()
    lines.append(f"  {'COMBINED':>12s}: ${total/1e6:>8.1f}M total, {days_active:>5d} active days")
    lines.append("")

    # Aave-only baseline (reproduce old results)
    lines.append("=== CONCENTRATION RATIO TEST: AAVE ONLY (baseline) ===")
    aave_only = combined[["date", "aave_usd", "price"]].copy()
    aave_only = aave_only.rename(columns={"aave_usd": "total_usd"})
    lines.extend(concentration_test(aave_only, "Aave-only"))

    # Combined
    lines.append("=== CONCENTRATION RATIO TEST: ALL PROTOCOLS (expanded) ===")
    lines.extend(concentration_test(combined, "Combined"))

    # Verdict
    lines.append("=== VERDICT ===")

    # Run combined test and extract key numbers
    df = combined.copy().sort_values("date").reset_index(drop=True)
    for h in [7]:
        df[f"fwd_{h}d"] = df["price"].shift(-h) / df["price"] - 1
    df["trailing_7d"] = df["total_usd"].rolling(TRAILING_WINDOW, min_periods=1).sum()
    df["conc_ratio"] = df["total_usd"] / df["trailing_7d"].replace(0, np.nan)
    active = df[df["total_usd"] > 0]["total_usd"]
    p90 = np.percentile(active, 90)
    high = df[(df["total_usd"] >= p90) & df["conc_ratio"].notna()]
    conc = high[high["conc_ratio"] > CONCENTRATION_THRESHOLD]
    dist = high[high["conc_ratio"] <= CONCENTRATION_THRESHOLD]
    c7 = conc["fwd_7d"].dropna()
    d7 = dist["fwd_7d"].dropna()

    if len(c7) >= 5 and len(d7) >= 5:
        _, p_val = stats.mannwhitneyu(c7, d7, alternative="two-sided")
        lines.append(f"  Combined sample: concentrated n={len(c7)}, distributed n={len(d7)}")
        lines.append(f"  Concentrated 7d median: {c7.median():+.3%}")
        lines.append(f"  Distributed 7d median: {d7.median():+.3%}")
        lines.append(f"  Mann-Whitney p = {p_val:.4f}")
        if p_val < 0.05:
            lines.append(f"  → SIGNIFICANT at 5%. Concentration ratio classifies cascade vs absorption.")
        elif p_val < 0.10:
            lines.append(f"  → MARGINAL (p < 0.10). Promising but not conclusive.")
        else:
            lines.append(f"  → NOT SIGNIFICANT. More data or different threshold needed.")

    summary = "\n".join(lines)
    print(summary)

    with open(RESULTS_FILE, "w") as f:
        f.write(summary + "\n")
    print(f"\nResults saved → {RESULTS_FILE}")


if __name__ == "__main__":
    main()
