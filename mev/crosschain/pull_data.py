#!/usr/bin/env python3
"""Pull daily swap, depth, and TVL history from THORChain Midgard API."""

import csv
import os
import sys
import time
from datetime import datetime, timezone

import requests

BASE_URL = "https://midgard.ninerealms.com/v2"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DELAY = 0.7  # seconds between API calls

# Pagination windows (each returns up to 400 days)
PAGE_STARTS = [1646092800, 1680652800, 1715126400, 1749686400]

POOLS_ALL = [
    "BTC.BTC", "ETH.ETH",
    "ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48",
    "ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7",
    "BCH.BCH", "BSC.BNB",
    "BSC.USDT-0X55D398326F99059FF775485246999027B3197955",
    "BASE.USDC-0X833589FCD6EDB6E08F4C7C32D4F71B54BDA02913",
    "DOGE.DOGE",
    "ETH.DAI-0X6B175474E89094C44DA98B954EEDEAC495271D0F",
    "AVAX.AVAX",
    "AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E",
    "LTC.LTC", "XRP.XRP", "GAIA.ATOM", "SOL.SOL", "TRON.TRX",
    "TRON.USDT-TR7NHQJEKQXGTCI8Q8ZY4PL8OTSZGJLJ6T",
    "ETH.WBTC-0X2260FAC5E5542A773AA44FBCFEDF7C193BC2C599",
]

POOLS_MAJOR = [
    "BTC.BTC", "ETH.ETH",
    "ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48",
    "ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7",
]

SWAP_FIELDS = [
    "pool", "date", "startTime", "endTime",
    "totalVolumeUSD", "totalCount", "totalFees", "averageSlip", "runePriceUSD",
    "toAssetVolumeUSD", "toAssetCount", "toRuneVolumeUSD", "toRuneCount",
    "fromTradeVolumeUSD", "toTradeVolumeUSD", "fromTradeCount", "toTradeCount",
    "fromSecuredVolumeUSD", "toSecuredVolumeUSD",
    "synthMintVolumeUSD", "synthRedeemVolumeUSD",
]

DEPTH_FIELDS = [
    "pool", "date", "startTime", "endTime",
    "assetDepth", "runeDepth", "assetPriceUSD", "liquidityUnits", "membersCount",
    "synthSupply", "synthUnits",
]

TVL_FIELDS = [
    "date", "startTime", "endTime",
    "totalValuePooled", "runePriceUSD",
]

call_count = 0


def api_get(url: str, params: dict) -> dict:
    """GET with delay and retry."""
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


def ts_to_date(ts: str) -> str:
    return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")


def safe_float(v: str) -> str:
    """Convert API string to float string, handling NaN."""
    if v in ("NaN", "", None):
        return ""
    return v


def pull_swaps():
    """Pull swap history for all pools."""
    path = os.path.join(DATA_DIR, "swaps_daily.csv")
    seen = set()  # (pool, startTime) dedup
    rows = []

    for i, pool in enumerate(POOLS_ALL):
        print(f"[swaps] {i+1}/{len(POOLS_ALL)} {pool}", file=sys.stderr)
        for page_start in PAGE_STARTS:
            data = api_get(f"{BASE_URL}/history/swaps", {
                "pool": pool, "interval": "day",
                "from": page_start, "count": 400,
            })
            for iv in data.get("intervals", []):
                key = (pool, iv["startTime"])
                if key in seen:
                    continue
                seen.add(key)
                row = {"pool": pool, "date": ts_to_date(iv["startTime"])}
                for f in SWAP_FIELDS:
                    if f in ("pool", "date"):
                        continue
                    row[f] = safe_float(iv.get(f, ""))
                rows.append(row)

    rows.sort(key=lambda r: (r["pool"], r["startTime"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SWAP_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"[swaps] wrote {len(rows)} rows to {path}", file=sys.stderr)
    return rows


def pull_depths():
    """Pull depth history for major pools."""
    path = os.path.join(DATA_DIR, "depths_daily.csv")
    seen = set()
    rows = []

    for i, pool in enumerate(POOLS_MAJOR):
        print(f"[depths] {i+1}/{len(POOLS_MAJOR)} {pool}", file=sys.stderr)
        for page_start in PAGE_STARTS:
            data = api_get(f"{BASE_URL}/history/depths/{pool}", {
                "interval": "day", "from": page_start, "count": 400,
            })
            for iv in data.get("intervals", []):
                key = (pool, iv["startTime"])
                if key in seen:
                    continue
                seen.add(key)
                row = {"pool": pool, "date": ts_to_date(iv["startTime"])}
                for f in DEPTH_FIELDS:
                    if f in ("pool", "date"):
                        continue
                    row[f] = safe_float(iv.get(f, ""))
                rows.append(row)

    rows.sort(key=lambda r: (r["pool"], r["startTime"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=DEPTH_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"[depths] wrote {len(rows)} rows to {path}", file=sys.stderr)
    return rows


def pull_tvl():
    """Pull aggregate TVL history."""
    path = os.path.join(DATA_DIR, "tvl_daily.csv")
    seen = set()
    rows = []

    print("[tvl] pulling aggregate TVL", file=sys.stderr)
    for page_start in PAGE_STARTS:
        data = api_get(f"{BASE_URL}/history/tvl", {
            "interval": "day", "from": page_start, "count": 400,
        })
        for iv in data.get("intervals", []):
            key = iv["startTime"]
            if key in seen:
                continue
            seen.add(key)
            row = {
                "date": ts_to_date(iv["startTime"]),
                "startTime": iv["startTime"],
                "endTime": iv["endTime"],
                "totalValuePooled": safe_float(iv.get("totalValuePooled", "")),
                "runePriceUSD": safe_float(iv.get("runePriceUSD", "")),
            }
            rows.append(row)

    rows.sort(key=lambda r: r["startTime"])
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TVL_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"[tvl] wrote {len(rows)} rows to {path}", file=sys.stderr)
    return rows


def validate(swap_rows, depth_rows, tvl_rows):
    """Print summary stats."""
    print("\n=== VALIDATION ===\n")

    # Swaps per pool
    from collections import defaultdict
    pool_stats = defaultdict(lambda: {"count": 0, "min_date": "9999", "max_date": "0000"})
    for r in swap_rows:
        s = pool_stats[r["pool"]]
        s["count"] += 1
        if r["date"] < s["min_date"]:
            s["min_date"] = r["date"]
        if r["date"] > s["max_date"]:
            s["max_date"] = r["date"]

    print("SWAPS by pool:")
    for pool in POOLS_ALL:
        s = pool_stats[pool]
        flag = " ⚠️" if s["count"] < 100 else ""
        print(f"  {pool:60s} {s['count']:5d} rows  [{s['min_date']} → {s['max_date']}]{flag}")
    print(f"  TOTAL: {len(swap_rows)} rows\n")

    # Depths per pool
    pool_stats2 = defaultdict(lambda: {"count": 0, "min_date": "9999", "max_date": "0000"})
    for r in depth_rows:
        s = pool_stats2[r["pool"]]
        s["count"] += 1
        if r["date"] < s["min_date"]:
            s["min_date"] = r["date"]
        if r["date"] > s["max_date"]:
            s["max_date"] = r["date"]

    print("DEPTHS by pool:")
    for pool in POOLS_MAJOR:
        s = pool_stats2[pool]
        flag = " ⚠️" if s["count"] < 100 else ""
        print(f"  {pool:60s} {s['count']:5d} rows  [{s['min_date']} → {s['max_date']}]{flag}")
    print(f"  TOTAL: {len(depth_rows)} rows\n")

    print(f"TVL: {len(tvl_rows)} rows", end="")
    if tvl_rows:
        print(f"  [{tvl_rows[0]['date']} → {tvl_rows[-1]['date']}]")
    else:
        print()

    print(f"\nTotal API calls: {call_count}")


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    swap_rows = pull_swaps()
    depth_rows = pull_depths()
    tvl_rows = pull_tvl()
    validate(swap_rows, depth_rows, tvl_rows)
