"""
Full Aave v2/v3 LiquidationCall event pull — all collateral types.
Classifies events as phantom/real/other for dynamics analysis.
"""

import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# --- RPC endpoints ---
RPC_URL = "https://ethereum-rpc.publicnode.com"
CHUNK_SIZE = 50_000

# --- Contracts ---
POOLS = [
    ("v2", "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", 14_000_000),
    ("v3", "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2", 16_300_000),
]

LIQUIDATION_TOPIC = "0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286"

# --- Token metadata ---
TOKENS = {
    # ETH and LSTs
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": ("WETH", 18),
    "0xae7ab96520de3a18e5e111b5eaab095312d7fe84": ("stETH", 18),
    "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0": ("wstETH", 18),
    "0xae78736cd615f374d3085123a210448e74fc6393": ("rETH", 18),
    "0xbe9895146f7af43049ca1c1ae358b0541ea49704": ("cbETH", 18),
    "0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee": ("weETH", 18),
    # Stablecoins
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": ("USDC", 6),
    "0xdac17f958d2ee523a2206206994597c13d831ec7": ("USDT", 6),
    "0x6b175474e89094c44da98b954eedeac495271d0f": ("DAI", 18),
    "0x40d16fc0246ad3160ccc09b8d0d3a2cd28ae6c2f": ("GHO", 18),
    "0x4fabb145d64652a948d72533023f6e7a623c7c53": ("BUSD", 18),
    "0x056fd409e1d7a124bd7017459dfea2f387b6d5cd": ("GUSD", 2),
    "0x0000000000085d4780b73119b644ae5ecd22b376": ("TUSD", 18),
    "0x57ab1ec28d129707052df4df418d58a2d46d5f51": ("sUSD", 18),
    "0x8e870d67f660d95d5be530380d0ec0bd388289e1": ("USDP", 18),
    "0x853d955acef822db058eb8505911ed77f175b99e": ("FRAX", 18),
    "0x6c3ea9036406852006290770bedfcaba0e23a0e8": ("PYUSD", 6),
    # Other major tokens
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": ("WBTC", 8),
    "0x514910771af9ca656af840dff83e8264ecf986ca": ("LINK", 18),
    "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9": ("AAVE", 18),
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": ("UNI", 18),
    "0xba100000625a3754423978a60c9317c58a424e3d": ("BAL", 18),
    "0xd533a949740bb3306d119cc777fa900ba034cd52": ("CRV", 18),
    "0x0f5d2fb29fb7d3cfee444a200298f468908cc942": ("MANA", 18),
    "0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c": ("ENJ", 18),
    "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2": ("MKR", 18),
    "0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f": ("SNX", 18),
}

LST_TOKENS = {"stETH", "wstETH", "rETH", "cbETH", "weETH"}
STABLE_TOKENS = {"USDC", "USDT", "DAI", "GHO", "BUSD", "GUSD", "TUSD", "sUSD", "USDP", "FRAX", "PYUSD"}
ETH_LIKE = {"WETH"} | LST_TOKENS

RATE_LIMIT_S = 0.3
RAW_FILE = DATA_DIR / "liquidations_raw.csv"
OUTPUT_FILE = DATA_DIR / "liquidations_full.csv"
CHECKPOINT_FILE = DATA_DIR / "liquidation_checkpoint.json"
TS_CACHE_FILE = DATA_DIR / "block_timestamps.json"

RAW_COLS = [
    "block_number", "tx_hash", "pool", "log_index",
    "collateral_asset", "debt_asset", "user",
    "debt_to_cover_raw", "liquidated_collateral_raw",
    "liquidator", "receive_atoken",
]


def token_info(addr: str) -> tuple[str, int]:
    info = TOKENS.get(addr.lower())
    if info:
        return info
    return (addr[:6] + ".." + addr[-4:], 18)


def classify(collateral_label: str, debt_label: str) -> str:
    if collateral_label in LST_TOKENS and debt_label == "WETH":
        return "phantom"
    if collateral_label in ETH_LIKE and debt_label in STABLE_TOKENS:
        return "real"
    return "other"


def rpc_call(method: str, params: list, retries: int = 4) -> dict:
    for attempt in range(retries):
        try:
            resp = requests.post(RPC_URL, json={
                "jsonrpc": "2.0", "method": method, "params": params, "id": 1
            }, timeout=60)
            if resp.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"    rate limited, wait {wait}s")
                time.sleep(wait)
                continue
            data = resp.json()
            if "error" in data:
                if attempt < retries - 1:
                    time.sleep(2 ** (attempt + 1))
                    continue
                raise RuntimeError(f"RPC error: {data['error']}")
            return data
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise
    raise RuntimeError(f"RPC failed after {retries} retries")


def get_current_block() -> int:
    data = rpc_call("eth_blockNumber", [])
    return int(data["result"], 16)


def addr_from_topic(topic: str) -> str:
    return "0x" + topic[-40:].lower()


def u256(hex_data: str, slot: int) -> int:
    return int(hex_data[slot * 64:(slot + 1) * 64], 16)


def decode_event(log: dict, pool: str) -> dict:
    topics = log["topics"]
    data_hex = log["data"][2:]
    return {
        "block_number": int(log["blockNumber"], 16),
        "tx_hash": log["transactionHash"],
        "pool": pool,
        "log_index": int(log.get("logIndex", "0x0"), 16),
        "collateral_asset": addr_from_topic(topics[1]),
        "debt_asset": addr_from_topic(topics[2]),
        "user": addr_from_topic(topics[3]),
        "debt_to_cover_raw": str(u256(data_hex, 0)),
        "liquidated_collateral_raw": str(u256(data_hex, 1)),
        "liquidator": "0x" + data_hex[128 + 24:192].lower(),
        "receive_atoken": u256(data_hex, 3) != 0,
    }


def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text())
    return {}


def save_checkpoint(cp: dict):
    CHECKPOINT_FILE.write_text(json.dumps(cp))


def pull_events(pool: str, address: str, start_block: int, end_block: int,
                writer, checkpoint: dict) -> int:
    cursor = checkpoint.get(pool, start_block)
    if cursor > start_block:
        print(f"  [{pool}] resuming from block {cursor:,}")

    total = 0
    chunk = CHUNK_SIZE

    while cursor <= end_block:
        to_block = min(cursor + chunk - 1, end_block)
        pct = (cursor - start_block) / max(end_block - start_block, 1) * 100
        print(f"  [{pool}] {pct:5.1f}% block {cursor:,}..{to_block:,}", end=" ", flush=True)

        try:
            data = rpc_call("eth_getLogs", [{
                "address": address,
                "topics": [LIQUIDATION_TOPIC],
                "fromBlock": hex(cursor),
                "toBlock": hex(to_block),
            }])
        except Exception as e:
            if chunk > 5_000:
                chunk //= 2
                print(f"  chunk→{chunk}")
                continue
            raise

        logs = data["result"]
        for log in logs:
            row = decode_event(log, pool)
            writer.writerow(row)

        count = len(logs)
        total += count
        print(f"→ {count} events (total: {total})")

        cursor = to_block + 1
        checkpoint[pool] = cursor
        save_checkpoint(checkpoint)
        time.sleep(RATE_LIMIT_S)

    return total


def fetch_block_timestamps(blocks: set[int]) -> dict[int, int]:
    """Interpolate timestamps from cached reference points + a few new fetches."""
    import numpy as np

    # Load cached timestamps
    ts_map = {}
    if TS_CACHE_FILE.exists():
        cached = json.loads(TS_CACHE_FILE.read_text())
        ts_map = {int(k): v for k, v in cached.items()}

    # Fetch a few reference points at boundaries if cache is sparse
    ref_blocks = sorted(blocks)
    # Pick ~20 evenly spaced reference blocks to validate
    indices = np.linspace(0, len(ref_blocks) - 1, min(20, len(ref_blocks)), dtype=int)
    to_fetch = [ref_blocks[i] for i in indices if ref_blocks[i] not in ts_map]

    if to_fetch:
        print(f"\nFetching {len(to_fetch)} reference timestamps...")
        for block in to_fetch:
            try:
                data = rpc_call("eth_getBlockByNumber", [hex(block), False])
                ts_map[block] = int(data["result"]["timestamp"], 16)
            except Exception:
                pass
            time.sleep(0.15)
        TS_CACHE_FILE.write_text(json.dumps({str(k): v for k, v in ts_map.items()}))

    # Build interpolation model from all known points
    known = sorted((b, t) for b, t in ts_map.items() if t > 0)
    print(f"\nTimestamps: {len(known)} reference points, {len(blocks)} blocks to map")

    if len(known) >= 2:
        kb = np.array([k[0] for k in known])
        kt = np.array([k[1] for k in known])
        # Use linear interpolation (block time is ~12s, very regular)
        result = {}
        all_blocks = np.array(sorted(blocks))
        interp_ts = np.interp(all_blocks, kb, kt).astype(int)
        for b, t in zip(all_blocks, interp_ts):
            result[int(b)] = int(t)
        return result

    return ts_map


def build_output():
    """Read raw events, add timestamps and labels, write final CSV."""
    import pandas as pd
    import numpy as np

    raw = pd.read_csv(RAW_FILE, dtype={"debt_to_cover_raw": str, "liquidated_collateral_raw": str})
    print(f"\nRaw events: {len(raw):,}")

    unique_blocks = set(raw["block_number"].unique())
    ts_map = fetch_block_timestamps(unique_blocks)

    rows = []
    for _, r in raw.iterrows():
        block = int(r["block_number"])
        coll_label, coll_dec = token_info(r["collateral_asset"])
        debt_label, debt_dec = token_info(r["debt_asset"])

        rows.append({
            "block_number": block,
            "timestamp": ts_map.get(block, 0),
            "tx_hash": r["tx_hash"],
            "pool": r["pool"],
            "user": r["user"],
            "collateral_asset": r["collateral_asset"],
            "collateral_label": coll_label,
            "collateral_amount": int(r["liquidated_collateral_raw"]) / (10 ** coll_dec),
            "collateral_decimals": coll_dec,
            "debt_asset": r["debt_asset"],
            "debt_label": debt_label,
            "debt_amount": int(r["debt_to_cover_raw"]) / (10 ** debt_dec),
            "debt_decimals": debt_dec,
            "liquidator": r["liquidator"],
            "receive_atoken": r["receive_atoken"],
            "category": classify(coll_label, debt_label),
        })

    out = pd.DataFrame(rows).sort_values("block_number").reset_index(drop=True)
    out.to_csv(OUTPUT_FILE, index=False)
    print(f"Output: {len(out):,} events → {OUTPUT_FILE}")
    return out


def print_summary(df):
    print("\n" + "=" * 60)
    print("LIQUIDATION PULL SUMMARY")
    print("=" * 60)

    print(f"\nTotal events: {len(df):,}")
    print(f"  v2: {(df['pool'] == 'v2').sum():,}")
    print(f"  v3: {(df['pool'] == 'v3').sum():,}")

    print(f"\nBy category:")
    for cat in ["real", "phantom", "other"]:
        n = (df["category"] == cat).sum()
        print(f"  {cat:10s}: {n:6,} ({n / len(df) * 100:.1f}%)")

    print(f"\nTop collateral assets:")
    for label, count in df["collateral_label"].value_counts().head(10).items():
        print(f"  {label:10s}: {count:6,} ({count / len(df) * 100:.1f}%)")

    print(f"\nTop debt assets:")
    for label, count in df["debt_label"].value_counts().head(10).items():
        print(f"  {label:10s}: {count:6,} ({count / len(df) * 100:.1f}%)")

    if "timestamp" in df.columns and df["timestamp"].max() > 0:
        t_min = datetime.fromtimestamp(df["timestamp"].min(), tz=timezone.utc)
        t_max = datetime.fromtimestamp(df["timestamp"].max(), tz=timezone.utc)
        print(f"\nDate range: {t_min:%Y-%m-%d} to {t_max:%Y-%m-%d}")

    print(f"Unique liquidated users: {df['user'].nunique():,}")
    print(f"Unique liquidators: {df['liquidator'].nunique():,}")


def main():
    checkpoint = load_checkpoint()
    current_block = get_current_block()
    print(f"Current block: {current_block:,}")

    # Phase 1: Pull raw events
    raw_exists = RAW_FILE.exists() and os.path.getsize(RAW_FILE) > 0
    with open(RAW_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RAW_COLS)
        if not raw_exists:
            writer.writeheader()
        total = 0
        for pool, address, start_block in POOLS:
            count = pull_events(pool, address, start_block, current_block, writer, checkpoint)
            total += count
    print(f"\nNew events pulled: {total:,}")

    # Phase 2: Enrich and output
    df = build_output()
    print_summary(df)


if __name__ == "__main__":
    main()
