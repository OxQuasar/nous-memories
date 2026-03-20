#!/usr/bin/env python3
"""CAPO Incident Forensics & Oracle Composition Trace.

Task A: Pull March 10 LiquidationCall events, cross-reference with position data.
Task B: Trace CAPO oracle adapter chain for wstETH, weETH, osETH.
"""

import csv
import os
import time
from datetime import datetime, timezone
from dataclasses import dataclass

import requests

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/BNZuV78MYIdQEqymhrHikACnAGe5cTES"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POSITION_CSV = os.path.join(os.path.dirname(__file__), "..", "position", "data", "positions_decomposed.csv")

# Contracts
AAVE_CORE_POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
AAVE_PRIME_POOL = "0x4e033931ad43597d96d6bcc25c280717730b58b1"
AAVE_CORE_ORACLE = "0x54586bE62E3c3580375aE3723C145253060Ca0C2"
LIQ_TOPIC = "0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286"

# The CAPO parameter update was executed at block 24626860
INCIDENT_BLOCK = 24626860
# Scan range: 10 blocks before to 50 blocks after
SCAN_START = INCIDENT_BLOCK - 10
SCAN_END = INCIDENT_BLOCK + 50

# Known token addresses
WSTETH = "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"
WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
WEETH = "0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee"
OSETH = "0xf1c9acdc66974dfb6decb12aa385b9cd01190e38"

# Known CAPO adapters (from core oracle getSourceOfAsset)
CAPO_ADAPTERS = {
    "wstETH": "0xe1d97bf61901b075e9626c8a2340a7de385861ef",
    "weETH": "0x87625393534d5c102cadb66d37201df24cc26d4c",
    "osETH": "0x2b86d519ef34f8adfc9349cdea17c09aa9db60e2",
}

# Incident parameters (from post-mortem)
INCIDENT = {
    "stale_snapshot_ratio": 1.1572,
    "target_snapshot_ratio": 1.2282,
    "max_allowed_ratio": 1.1919,
    "actual_market_ratio": 1.228,
    "depeg_pct": 2.85,
    "execution_tx": "0x32c64151469cf2202cbc9581139c6de7b34dae2012eba9daf49311265dfe5a1e",
    "param_update_tx": "0xfbafeaa8c58dd6d79f88cdf5604bd25760964bc8fc0e834fe381bb1d96d3db95",
    "borrow_cap_tx": "0x34f568b28dbcaf6a8272038ea441cbc864c8608fe044c590f9f03d0dac9cf7f8",
}


# ---------- Helpers ----------

def eth_call(to, data, block="latest"):
    payload = {"jsonrpc": "2.0", "method": "eth_call",
               "params": [{"to": to, "data": "0x" + data}, block], "id": 1}
    resp = requests.post(ALCHEMY_URL, json=payload, timeout=30).json()
    if "error" in resp:
        return None
    raw = resp.get("result", "0x")
    return raw[2:] if raw not in ("0x", None) else None


def eth_get_logs(address, topics, from_block, to_block):
    """Get logs in 10-block chunks (Alchemy free tier limit)."""
    all_logs = []
    block = from_block
    while block <= to_block:
        chunk_end = min(block + 9, to_block)
        payload = {
            "jsonrpc": "2.0", "method": "eth_getLogs",
            "params": [{"address": address, "topics": topics,
                        "fromBlock": hex(block), "toBlock": hex(chunk_end)}],
            "id": 1,
        }
        for attempt in range(3):
            resp = requests.post(ALCHEMY_URL, json=payload, timeout=30).json()
            if "error" not in resp:
                all_logs.extend(resp.get("result", []))
                break
            time.sleep(0.5)
        block = chunk_end + 1
    return all_logs


def get_block_timestamp(block_num):
    payload = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber",
               "params": [hex(block_num), False], "id": 1}
    resp = requests.post(ALCHEMY_URL, json=payload, timeout=30).json()
    if resp.get("result"):
        return int(resp["result"]["timestamp"], 16)
    return 0


def u256(h, s=0):
    return int(h[s * 64:(s + 1) * 64], 16)


def addr_from_topic(topic):
    """Extract address from 32-byte indexed topic."""
    return "0x" + topic[26:].lower()


def keccak256_selector(sig):
    """Compute 4-byte function selector."""
    from Crypto.Hash import keccak
    k = keccak.new(digest_bits=256)
    k.update(sig.encode())
    return k.hexdigest()[:8]


# ---------- Task A: Liquidation Event Collection ----------

def decode_liquidation_log(log):
    """Decode a LiquidationCall event log."""
    collateral = addr_from_topic(log["topics"][1])
    debt_asset = addr_from_topic(log["topics"][2])
    user = addr_from_topic(log["topics"][3])

    data = log["data"][2:]
    debt_to_cover = u256(data, 0)
    liq_collateral_amount = u256(data, 1)
    liquidator = "0x" + data[128 + 24:192]

    block_num = int(log["blockNumber"], 16)
    tx_hash = log["transactionHash"]

    return {
        "block": block_num,
        "tx_hash": tx_hash,
        "user": user,
        "collateral_asset": collateral,
        "collateral_amount": liq_collateral_amount / 1e18,
        "debt_asset": debt_asset,
        "debt_amount": debt_to_cover / 1e18,
        "liquidator": liquidator,
    }


def collect_liquidations():
    """Collect all LiquidationCall events from both Core and Prime pools."""
    print("Scanning for LiquidationCall events...")
    print(f"  Block range: {SCAN_START} to {SCAN_END}")

    events = []
    for pool_name, pool_addr in [("Core", AAVE_CORE_POOL), ("Prime", AAVE_PRIME_POOL)]:
        logs = eth_get_logs(pool_addr, [LIQ_TOPIC], SCAN_START, SCAN_END)
        print(f"  {pool_name} pool ({pool_addr[:10]}...): {len(logs)} events")
        for log in logs:
            ev = decode_liquidation_log(log)
            ev["pool"] = pool_name
            events.append(ev)

    # Get block timestamps
    block_timestamps = {}
    for ev in events:
        if ev["block"] not in block_timestamps:
            block_timestamps[ev["block"]] = get_block_timestamp(ev["block"])

    for ev in events:
        ts = block_timestamps[ev["block"]]
        ev["timestamp"] = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Sort by block
    events.sort(key=lambda e: (e["block"], e["pool"]))
    return events


def summarize_liquidations(events):
    """Print and return summary statistics."""
    users = {}
    total_collateral = 0.0
    total_debt = 0.0

    for ev in events:
        user = ev["user"]
        if user not in users:
            users[user] = {"collateral": 0.0, "debt": 0.0, "events": 0, "pool": ev["pool"]}
        users[user]["collateral"] += ev["collateral_amount"]
        users[user]["debt"] += ev["debt_amount"]
        users[user]["events"] += 1
        total_collateral += ev["collateral_amount"]
        total_debt += ev["debt_amount"]

    # Liquidator stats
    liquidators = {}
    for ev in events:
        liq = ev["liquidator"]
        if liq not in liquidators:
            liquidators[liq] = {"collateral": 0.0, "debt": 0.0, "events": 0}
        liquidators[liq]["collateral"] += ev["collateral_amount"]
        liquidators[liq]["debt"] += ev["debt_amount"]
        liquidators[liq]["events"] += 1

    print(f"\n--- Liquidation Summary ---")
    print(f"Total events: {len(events)}")
    print(f"Unique users liquidated: {len(users)}")
    print(f"Total wstETH seized: {total_collateral:.2f}")
    print(f"Total WETH debt repaid: {total_debt:.2f}")

    # ETH price at incident
    eth_price = 2136.0  # approximate from our data
    print(f"Approximate USD value: ${total_collateral * 1.229 * eth_price / 1e6:.2f}M")

    print(f"\nTop liquidated users:")
    sorted_users = sorted(users.items(), key=lambda x: x[1]["collateral"], reverse=True)
    for user, data in sorted_users[:10]:
        print(f"  {user}: {data['collateral']:.2f} wstETH ({data['events']} events, {data['pool']})")

    print(f"\nLiquidators:")
    sorted_liquidators = sorted(liquidators.items(), key=lambda x: x[1]["collateral"], reverse=True)
    for liq, data in sorted_liquidators[:5]:
        bonus_eth = data["collateral"] * 1.229 - data["debt"]  # rough: collateral_value - debt
        print(f"  {liq}: seized {data['collateral']:.2f} wstETH, repaid {data['debt']:.2f} WETH ({data['events']} events)")

    return users


# ---------- Cross-reference with position data ----------

def load_positions():
    """Load decomposed position data."""
    positions = {}
    with open(POSITION_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = row["user"].lower()
            positions[user] = row
    return positions


def cross_reference(liquidated_users, positions):
    """Cross-reference liquidated users with our position snapshot."""
    print("\n--- Position Cross-Reference ---")

    matches = []
    for user, liq_data in liquidated_users.items():
        user_lower = user.lower()
        if user_lower in positions:
            pos = positions[user_lower]
            matches.append({
                "user": user,
                "liq_collateral_wsteth": liq_data["collateral"],
                "liq_debt_weth": liq_data["debt"],
                "liq_pool": liq_data["pool"],
                "snapshot_collateral_usd": float(pos["collateral_usd"]),
                "snapshot_debt_usd": float(pos["debt_usd"]),
                "snapshot_hf": float(pos["health_factor"]) if pos["health_factor"] else 0,
                "snapshot_type": pos["position_type"],
                "snapshot_largest_collateral": pos["largest_collateral_symbol"],
            })

    print(f"Liquidated users found in our snapshot: {len(matches)} / {len(liquidated_users)}")

    if matches:
        matches.sort(key=lambda m: m["snapshot_collateral_usd"], reverse=True)
        for m in matches[:10]:
            print(f"  {m['user'][:12]}... HF={m['snapshot_hf']:.4f} "
                  f"col=${m['snapshot_collateral_usd']/1e6:.2f}M "
                  f"type={m['snapshot_type']} collateral={m['snapshot_largest_collateral']}")

    # Check mega-whales that SURVIVED
    print("\n--- Mega-whale survival analysis ---")
    mega_positions = []
    for user, pos in positions.items():
        col = float(pos["collateral_usd"])
        if col > 100_000_000 and pos["position_type"] == "phantom":
            symbol = pos["largest_collateral_symbol"]
            if symbol in ("wstETH", "weETH"):
                hf = float(pos["health_factor"]) if pos["health_factor"] else 0
                mega_positions.append({
                    "user": user,
                    "collateral_usd": col,
                    "health_factor": hf,
                    "collateral_symbol": symbol,
                    "survived": user not in {u.lower() for u in liquidated_users},
                })

    mega_positions.sort(key=lambda p: p["collateral_usd"], reverse=True)
    for p in mega_positions[:10]:
        # How much depeg would catch this position?
        # HF = 1 when depeg = (HF - 1) / HF * 100 (rough for E-Mode)
        # More precisely: HF_after = HF_before * (1 - depeg_fraction)
        # Liquidation when HF_after < 1: depeg > (HF - 1) / HF
        if p["health_factor"] > 1:
            depeg_to_liq = (p["health_factor"] - 1) / p["health_factor"] * 100
        else:
            depeg_to_liq = 0
        status = "SURVIVED" if p["survived"] else "LIQUIDATED"
        print(f"  {p['user'][:12]}... ${p['collateral_usd']/1e9:.2f}B "
              f"HF={p['health_factor']:.4f} {p['collateral_symbol']} "
              f"→ {depeg_to_liq:.2f}% depeg to liquidate [{status}]")

    return matches


# ---------- Task B: Oracle Composition Trace ----------

def trace_oracle(token_name, adapter_addr, token_addr):
    """Trace CAPO oracle composition for a token."""
    print(f"\n=== {token_name} Oracle Composition ===")
    print(f"CAPO adapter: {adapter_addr}")

    sel = {
        "RATIO_PROVIDER": keccak256_selector("RATIO_PROVIDER()"),
        "MINIMUM_SNAPSHOT_DELAY": keccak256_selector("MINIMUM_SNAPSHOT_DELAY()"),
        "getMaxRatioGrowthPerSecond": keccak256_selector("getMaxRatioGrowthPerSecond()"),
        "getSnapshotRatio": keccak256_selector("getSnapshotRatio()"),
        "getSnapshotTimestamp": keccak256_selector("getSnapshotTimestamp()"),
        "isCapped": keccak256_selector("isCapped()"),
        "latestAnswer": "50d25bcd",
        "decimals": "313ce567",
        "description": "7284e416",
    }

    result = {}
    result["token"] = token_name
    result["adapter"] = adapter_addr

    # Description
    r = eth_call(adapter_addr, sel["description"])
    if r:
        try:
            length = u256(r, 1)
            text = bytes.fromhex(r[128:128 + length * 2]).decode("utf-8")
            result["description"] = text
            print(f"  Description: {text}")
        except:
            pass

    # latestAnswer
    r = eth_call(adapter_addr, sel["latestAnswer"])
    if r:
        price = u256(r)
        result["latest_price_usd"] = price / 1e8
        print(f"  Current price: ${price / 1e8:.2f}")

    # RATIO_PROVIDER
    r = eth_call(adapter_addr, sel["RATIO_PROVIDER"])
    if r:
        prov = "0x" + r[24:64]
        result["ratio_provider"] = prov
        print(f"  Ratio provider: {prov}")

    # MINIMUM_SNAPSHOT_DELAY
    r = eth_call(adapter_addr, sel["MINIMUM_SNAPSHOT_DELAY"])
    if r:
        delay = u256(r)
        result["min_snapshot_delay_days"] = delay / 86400
        print(f"  Snapshot delay: {delay}s ({delay / 86400:.0f} days)")

    # getMaxRatioGrowthPerSecond
    r = eth_call(adapter_addr, sel["getMaxRatioGrowthPerSecond"])
    if r:
        rate = u256(r)
        result["max_growth_per_sec"] = rate
        print(f"  Max growth/sec: {rate}")

    # getSnapshotRatio
    r = eth_call(adapter_addr, sel["getSnapshotRatio"])
    if r:
        ratio = u256(r) / 1e18
        result["snapshot_ratio"] = ratio
        print(f"  Snapshot ratio: {ratio:.8f}")

    # getSnapshotTimestamp
    r = eth_call(adapter_addr, sel["getSnapshotTimestamp"])
    if r:
        ts = u256(r)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        result["snapshot_timestamp"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(f"  Snapshot timestamp: {dt}")

    # isCapped
    r = eth_call(adapter_addr, sel["isCapped"])
    if r:
        capped = bool(u256(r))
        result["is_capped"] = capped
        print(f"  Currently capped: {capped}")

    # Get Chainlink stETH/ETH feed info
    if token_name == "wstETH":
        chainlink_feed = "0x86392dC19c0b719886221c78AB11eb8Cf5c52812"
        r = eth_call(chainlink_feed, "feaf968c")  # latestRoundData
        if r:
            answer = u256(r, 1)
            updated = u256(r, 3)
            dt = datetime.fromtimestamp(updated, tz=timezone.utc)
            result["chainlink_steth_eth"] = answer / 1e18
            result["chainlink_updated"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            print(f"  Chainlink stETH/ETH: {answer / 1e18:.8f} (updated {dt})")

    return result


# ---------- Main ----------

def main():
    print("=" * 70)
    print("CAPO INCIDENT FORENSICS & ORACLE COMPOSITION TRACE")
    print("=" * 70)
    print(f"Incident: March 10, 2026 11:46 UTC")
    print(f"CAPO reported wstETH rate: ~{INCIDENT['max_allowed_ratio']}")
    print(f"Actual market rate: ~{INCIDENT['actual_market_ratio']}")
    print(f"Undervaluation: ~{INCIDENT['depeg_pct']}%")

    os.makedirs(DATA_DIR, exist_ok=True)

    # Task A: Collect liquidation events
    print("\n" + "=" * 70)
    print("TASK A: LIQUIDATION EVENT COLLECTION")
    print("=" * 70)

    events = collect_liquidations()
    users = summarize_liquidations(events)

    # Save liquidation events CSV
    liq_path = os.path.join(DATA_DIR, "capo_liquidations_mar10.csv")
    fields = ["block", "timestamp", "pool", "user", "collateral_asset",
              "collateral_amount", "debt_asset", "debt_amount", "liquidator", "tx_hash"]
    with open(liq_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(events)
    print(f"\nSaved: {liq_path} ({len(events)} rows)")

    # Cross-reference with position data
    if os.path.exists(POSITION_CSV):
        positions = load_positions()
        matches = cross_reference(users, positions)

        overlap_path = os.path.join(DATA_DIR, "capo_position_overlap.csv")
        if matches:
            with open(overlap_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=matches[0].keys())
                writer.writeheader()
                writer.writerows(matches)
            print(f"Saved: {overlap_path}")
    else:
        print(f"\nPosition data not found at {POSITION_CSV}")

    # Task B: Oracle Composition Trace
    print("\n" + "=" * 70)
    print("TASK B: ORACLE COMPOSITION TRACE")
    print("=" * 70)

    oracle_results = []
    tokens = {
        "wstETH": WSTETH,
        "weETH": WEETH,
        "osETH": OSETH,
    }
    for name, addr in tokens.items():
        if name in CAPO_ADAPTERS:
            result = trace_oracle(name, CAPO_ADAPTERS[name], addr)
            oracle_results.append(result)

    # Save oracle composition CSV
    oracle_path = os.path.join(DATA_DIR, "oracle_composition.csv")
    if oracle_results:
        all_keys = set()
        for r in oracle_results:
            all_keys.update(r.keys())
        with open(oracle_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(oracle_results)
        print(f"\nSaved: {oracle_path}")

    return events, oracle_results


if __name__ == "__main__":
    main()
