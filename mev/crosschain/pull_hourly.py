#!/usr/bin/env python3
"""Pull hourly swap and depth data for crash windows from THORChain Midgard API."""

import csv
import os
import sys
import time
from datetime import datetime, timezone

import requests

BASE_URL = "https://midgard.ninerealms.com/v2"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DELAY = 0.7

POOLS = [
    "BTC.BTC",
    "ETH.ETH",
    "ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48",
]

# (label, from_ts, count) — 14 days = 336 hours, fits in one call (max 400)
CRASH_WINDOWS = [
    ("aug2024",    1722470400, 336),  # Aug 1-15 2024
    ("dec2024",    1733875200, 336),  # Dec 11-25 2024
    ("oct2025",    1759708800, 336),  # Oct 6-20 2025
    ("nov2025",    1763337600, 336),  # Nov 17 - Dec 1 2025
    ("janfeb2026", 1768348800, 336),  # Jan 14-28 2026
]

SWAP_FIELDS = [
    "pool", "episode", "datetime", "startTime", "endTime",
    "totalVolumeUSD", "totalCount", "totalFees", "averageSlip", "runePriceUSD",
    "toAssetVolumeUSD", "toAssetCount", "toRuneVolumeUSD", "toRuneCount",
    "fromTradeVolumeUSD", "toTradeVolumeUSD", "fromTradeCount", "toTradeCount",
    "fromSecuredVolumeUSD", "toSecuredVolumeUSD",
    "synthMintVolumeUSD", "synthRedeemVolumeUSD",
]

DEPTH_FIELDS = [
    "pool", "episode", "datetime", "startTime", "endTime",
    "assetDepth", "runeDepth", "assetPriceUSD", "liquidityUnits", "membersCount",
    "synthSupply", "synthUnits",
]

call_count = 0


def api_get(url, params):
    global call_count
    for attempt in range(3):
        time.sleep(DELAY)
        call_count += 1
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"  retry {attempt+1}/3: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed after 3 retries: {url} {params}")


def ts_to_dt(ts):
    return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d %H:%M")


def safe(v):
    if v in ("NaN", "", None):
        return ""
    return v


def pull_hourly_swaps():
    path = os.path.join(DATA_DIR, "hourly_swaps.csv")
    seen = set()
    rows = []

    for label, from_ts, count in CRASH_WINDOWS:
        for pool in POOLS:
            print(f"[hourly swaps] {label} {pool}", file=sys.stderr)
            data = api_get(f"{BASE_URL}/history/swaps", {
                "pool": pool, "interval": "hour", "from": from_ts, "count": count,
            })
            for iv in data.get("intervals", []):
                key = (pool, iv["startTime"])
                if key in seen:
                    continue
                seen.add(key)
                row = {"pool": pool, "episode": label, "datetime": ts_to_dt(iv["startTime"])}
                for f in SWAP_FIELDS:
                    if f in ("pool", "episode", "datetime"):
                        continue
                    row[f] = safe(iv.get(f, ""))
                rows.append(row)

    rows.sort(key=lambda r: (r["pool"], r["startTime"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SWAP_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"[hourly swaps] wrote {len(rows)} rows", file=sys.stderr)
    return rows


def pull_hourly_depths():
    path = os.path.join(DATA_DIR, "hourly_depths.csv")
    seen = set()
    rows = []

    for label, from_ts, count in CRASH_WINDOWS:
        for pool in POOLS:
            print(f"[hourly depths] {label} {pool}", file=sys.stderr)
            data = api_get(f"{BASE_URL}/history/depths/{pool}", {
                "interval": "hour", "from": from_ts, "count": count,
            })
            for iv in data.get("intervals", []):
                key = (pool, iv["startTime"])
                if key in seen:
                    continue
                seen.add(key)
                row = {"pool": pool, "episode": label, "datetime": ts_to_dt(iv["startTime"])}
                for f in DEPTH_FIELDS:
                    if f in ("pool", "episode", "datetime"):
                        continue
                    row[f] = safe(iv.get(f, ""))
                rows.append(row)

    rows.sort(key=lambda r: (r["pool"], r["startTime"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=DEPTH_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"[hourly depths] wrote {len(rows)} rows", file=sys.stderr)
    return rows


def validate(swap_rows, depth_rows):
    print("\n=== HOURLY VALIDATION ===\n", file=sys.stderr)
    from collections import Counter
    sc = Counter((r["pool"], r["episode"]) for r in swap_rows)
    dc = Counter((r["pool"], r["episode"]) for r in depth_rows)
    print("Swaps per (pool, episode):", file=sys.stderr)
    for key in sorted(sc):
        print(f"  {key[0]:60s} {key[1]:15s} {sc[key]:4d} rows", file=sys.stderr)
    print(f"\nDepths per (pool, episode):", file=sys.stderr)
    for key in sorted(dc):
        print(f"  {key[0]:60s} {key[1]:15s} {dc[key]:4d} rows", file=sys.stderr)
    print(f"\nTotal: {len(swap_rows)} swap rows, {len(depth_rows)} depth rows", file=sys.stderr)
    print(f"API calls: {call_count}", file=sys.stderr)


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    swap_rows = pull_hourly_swaps()
    depth_rows = pull_hourly_depths()
    validate(swap_rows, depth_rows)
