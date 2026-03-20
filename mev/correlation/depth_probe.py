#!/usr/bin/env python3
"""DEX Liquidity Depth Probe for LST Tokens.

Measures how much selling (in USD) produces 1%, 2%, 5% depeg from fair rate.
Uses Paraswap aggregator API for real cross-DEX depth (routes through Uniswap,
Curve, Balancer, etc. simultaneously) and Alchemy RPC for on-chain fair rates.
"""

import csv
import json
import os
import sys
import time
from dataclasses import dataclass, field

import requests

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/BNZuV78MYIdQEqymhrHikACnAGe5cTES"
PARASWAP_URL = "https://apiv5.paraswap.io/prices"

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

# Sell amounts in ETH-equivalent terms
SELL_AMOUNTS_ETH = [10, 50, 100, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000]

PARASWAP_DELAY = 1.1  # seconds between requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@dataclass
class Token:
    symbol: str
    address: str
    decimals: int = 18


TOKENS = [
    Token("weETH", "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee"),
    Token("osETH", "0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38"),
    Token("rsETH", "0xA1290d69c65A6Fe4DF752f95823fae25cB99e5A7"),
    Token("wstETH", "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"),
    Token("rETH", "0xae78736Cd615f374D3085123A210448E74Fc6393"),
    Token("cbETH", "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704"),
    Token("ETHx", "0xA35b1B31Ce002FBF2058D22F30f95D405200A15b"),
]

# Phantom exposure per token (from position topology investigation)
PHANTOM_EXPOSURE = {
    "weETH": 230_000_000,
    "osETH": 332_000_000,
    "rsETH": 880_000_000,
    "wstETH": 1_700_000_000,
    "rETH": 200_000_000,
    "cbETH": 150_000_000,
    "ETHx": 100_000_000,
}


def eth_call(to: str, data: str) -> str | None:
    """eth_call, returns hex without 0x prefix, or None on error."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": to, "data": "0x" + data}, "latest"],
        "id": 1,
    }
    resp = requests.post(ALCHEMY_URL, json=payload, timeout=30)
    result = resp.json()
    if "error" in result:
        return None
    raw = result.get("result", "0x")
    if raw == "0x" or raw is None:
        return None
    return raw[2:]


def get_eth_price_usd() -> float:
    """Get ETH/USD from Chainlink."""
    result = eth_call("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", "feaf968c")
    if result:
        answer = int(result[64:128], 16)  # slot 1 of latestRoundData
        return answer / 1e8
    return 2000.0


def paraswap_quote(src: str, dst: str, amount_wei: int, src_dec: int = 18, dst_dec: int = 18) -> dict | None:
    """Get aggregated quote from Paraswap."""
    params = {
        "srcToken": src, "destToken": dst,
        "amount": str(amount_wei),
        "srcDecimals": str(src_dec), "destDecimals": str(dst_dec),
        "side": "SELL", "network": "1",
    }
    for attempt in range(3):
        try:
            resp = requests.get(PARASWAP_URL, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if "priceRoute" in data:
                    return data["priceRoute"]
                return None
            if resp.status_code == 429:
                time.sleep(3 * (attempt + 1))
                continue
            # Other error — check if it's "ESTIMATED_LOSS_GREATER_THAN_MAX_IMPACT" (too large)
            try:
                err = resp.json().get("error", "")
                if "ESTIMATED_LOSS" in str(err) or "No routes" in str(err) or "liquidity" in str(err).lower():
                    return None
            except:
                pass
            return None
        except Exception as e:
            print(f"    Paraswap error: {e}")
            if attempt < 2:
                time.sleep(2)
    return None


def get_fair_rate(token: Token) -> float | None:
    """Get fair exchange rate (ETH per 1 token) using a tiny Paraswap quote."""
    amount = 10 ** token.decimals  # 1 token
    time.sleep(PARASWAP_DELAY)
    route = paraswap_quote(token.address, WETH, amount, token.decimals, 18)
    if route:
        dest = int(route["destAmount"])
        return dest / 1e18
    return None


def extract_route_dexes(route: dict) -> str:
    """Extract DEX names from Paraswap route."""
    dex_names = set()
    for path in route.get("bestRoute", []):
        for swap in path.get("swaps", []):
            for ex in swap.get("swapExchanges", []):
                dex_names.add(ex.get("exchange", "?"))
    return "+".join(sorted(dex_names)) if dex_names else "unknown"


def _do_quote(token: Token, fair_rate: float, eth_price: float, sell_eth: float) -> dict:
    """Execute a single quote and return a row dict."""
    token_amount = sell_eth / fair_rate
    amount_wei = int(token_amount * 10**token.decimals)
    sell_usd = sell_eth * eth_price

    time.sleep(PARASWAP_DELAY)
    route = paraswap_quote(token.address, WETH, amount_wei, token.decimals, 18)

    if route is None:
        return {
            "token": token.symbol,
            "sell_eth_equiv": sell_eth,
            "sell_usd": int(sell_usd),
            "sell_tokens": f"{token_amount:.2f}",
            "fair_rate": f"{fair_rate:.8f}",
            "effective_rate": "N/A",
            "depeg_pct": "N/A",
            "eth_received": "N/A",
            "dex_route": "N/A",
        }

    dest_eth = int(route["destAmount"]) / 1e18
    src_tokens = int(route["srcAmount"]) / 10**token.decimals
    eff_rate = dest_eth / src_tokens if src_tokens > 0 else 0
    depeg = (fair_rate - eff_rate) / fair_rate * 100
    dexes = extract_route_dexes(route)

    return {
        "token": token.symbol,
        "sell_eth_equiv": sell_eth,
        "sell_usd": int(sell_usd),
        "sell_tokens": f"{src_tokens:.2f}",
        "fair_rate": f"{fair_rate:.8f}",
        "effective_rate": f"{eff_rate:.8f}",
        "depeg_pct": f"{depeg:.4f}",
        "eth_received": f"{dest_eth:.4f}",
        "dex_route": dexes,
    }


def _log_row(row: dict):
    """Print a single probe result."""
    sell_eth = row["sell_eth_equiv"]
    sell_usd = float(row["sell_usd"])
    if row["depeg_pct"] == "N/A":
        print(f"  {sell_eth:>8.0f} ETH (${sell_usd/1e6:>6.1f}M): NO ROUTE")
    else:
        print(f"  {sell_eth:>8.0f} ETH (${sell_usd/1e6:>6.1f}M): "
              f"rate={float(row['effective_rate']):.6f} depeg={float(row['depeg_pct']):>7.3f}% "
              f"ETH_out={float(row['eth_received']):>10.2f}  [{row['dex_route']}]")


def probe_token(token: Token, eth_price: float) -> list[dict]:
    """Probe liquidity depth using Paraswap aggregator with adaptive refinement."""
    print(f"\n{'='*60}")
    print(f"Probing {token.symbol}")
    print(f"{'='*60}")

    fair_rate = get_fair_rate(token)
    if fair_rate is None:
        print(f"  Could not get fair rate, skipping")
        return []

    token_price_usd = fair_rate * eth_price
    print(f"  Fair rate: {fair_rate:.6f} ETH/{token.symbol}  (${token_price_usd:.2f})")

    rows = []
    last_success_eth = None

    # Phase 1: sweep the standard amounts
    for sell_eth in SELL_AMOUNTS_ETH:
        row = _do_quote(token, fair_rate, eth_price, sell_eth)
        _log_row(row)
        rows.append(row)

        if row["depeg_pct"] != "N/A":
            last_success_eth = sell_eth

    # Phase 2: if we hit NO ROUTE, refine between last_success and first_failure
    # Use bisection to find the boundary and fill in intermediate points
    if last_success_eth is not None:
        first_fail_eth = None
        for sell_eth in SELL_AMOUNTS_ETH:
            if sell_eth > last_success_eth:
                first_fail_eth = sell_eth
                break

        if first_fail_eth is not None:
            print(f"  --- Refining between {last_success_eth} and {first_fail_eth} ETH ---")
            # Test intermediate points: bisect 3 times
            lo, hi = last_success_eth, first_fail_eth
            refinement_points = set()
            for _ in range(4):
                mid = (lo + hi) / 2
                mid = round(mid)
                if mid in refinement_points or mid == lo or mid == hi:
                    break
                refinement_points.add(mid)
                row = _do_quote(token, fair_rate, eth_price, mid)
                _log_row(row)
                rows.append(row)
                if row["depeg_pct"] != "N/A":
                    lo = mid
                else:
                    hi = mid

            # Also test a few more points around the boundary
            for frac in [0.6, 0.7, 0.8, 0.9]:
                pt = round(last_success_eth + frac * (first_fail_eth - last_success_eth))
                if pt not in refinement_points and pt != last_success_eth and pt != first_fail_eth:
                    refinement_points.add(pt)
                    row = _do_quote(token, fair_rate, eth_price, pt)
                    _log_row(row)
                    rows.append(row)

    # Sort rows by sell amount for output
    rows.sort(key=lambda r: float(r["sell_eth_equiv"]))
    return rows


def interpolate_threshold(rows: list[dict], target_depeg: float) -> float | None:
    """Find USD sell amount producing target depeg%. Returns None if unreachable."""
    points = [(float(r["sell_usd"]), float(r["depeg_pct"]))
              for r in rows if r["depeg_pct"] != "N/A"]
    if not points:
        return None
    points.sort()

    # Target below first point — interpolate from origin
    if points[0][1] >= target_depeg:
        usd1, dep1 = points[0]
        return target_depeg / dep1 * usd1 if dep1 > 0 else None

    # Target above last point
    if points[-1][1] < target_depeg:
        return None

    # Bracket search
    for i in range(len(points) - 1):
        u0, d0 = points[i]
        u1, d1 = points[i + 1]
        if d0 <= target_depeg <= d1:
            if d1 == d0:
                return u0
            return u0 + (target_depeg - d0) / (d1 - d0) * (u1 - u0)

    return None


def build_summary(all_rows: dict[str, list[dict]], eth_price: float) -> list[dict]:
    """Build summary per token."""
    summary = []
    for token in TOKENS:
        rows = all_rows.get(token.symbol, [])
        phantom = PHANTOM_EXPOSURE.get(token.symbol, 0)

        if not rows or all(r["eth_received"] == "N/A" for r in rows):
            summary.append({
                "token": token.symbol,
                "fair_rate": rows[0]["fair_rate"] if rows else "N/A",
                "max_eth_out": "N/A",
                "max_capacity_usd": "N/A",
                "usd_to_1pct": "N/A",
                "usd_to_2pct": "N/A",
                "usd_to_5pct": "N/A",
                "phantom_usd": f"{phantom/1e6:.0f}M",
                "cascade_ratio": "N/A",
            })
            continue

        max_eth = max(float(r["eth_received"]) for r in rows if r["eth_received"] != "N/A")

        usd_1 = interpolate_threshold(rows, 1.0)
        usd_2 = interpolate_threshold(rows, 2.0)
        usd_5 = interpolate_threshold(rows, 5.0)
        cascade = phantom / usd_2 if usd_2 and usd_2 > 0 else None

        def fmt_usd(v):
            return f"${v/1e6:.1f}M" if v else ">MAX"

        summary.append({
            "token": token.symbol,
            "fair_rate": rows[0]["fair_rate"],
            "max_eth_out": f"{max_eth:.0f}",
            "max_capacity_usd": f"${max_eth * eth_price / 1e6:.1f}M",
            "usd_to_1pct": fmt_usd(usd_1),
            "usd_to_2pct": fmt_usd(usd_2),
            "usd_to_5pct": fmt_usd(usd_5),
            "phantom_usd": f"{phantom/1e6:.0f}M",
            "cascade_ratio": f"{cascade:.1f}x" if cascade else "N/A",
        })

    return summary


def main():
    print("LST DEX Liquidity Depth Probe (Aggregated via Paraswap)")
    print("=" * 60)

    eth_price = get_eth_price_usd()
    print(f"ETH price: ${eth_price:.2f}")
    print(f"Sell amounts (ETH): {SELL_AMOUNTS_ETH}")
    print(f"Sell amounts (USD): {[f'${x*eth_price/1e6:.1f}M' for x in SELL_AMOUNTS_ETH]}")

    all_rows = {}
    flat_rows = []
    for token in TOKENS:
        rows = probe_token(token, eth_price)
        all_rows[token.symbol] = rows
        flat_rows.extend(rows)

    # Write detailed results
    os.makedirs(DATA_DIR, exist_ok=True)
    detail_path = os.path.join(DATA_DIR, "lst_liquidity_depth.csv")
    fields = ["token", "sell_eth_equiv", "sell_usd", "sell_tokens",
              "fair_rate", "effective_rate", "depeg_pct", "eth_received", "dex_route"]
    with open(detail_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(flat_rows)
    print(f"\nDetailed: {detail_path} ({len(flat_rows)} rows)")

    # Build and write summary
    summary = build_summary(all_rows, eth_price)
    summary_path = os.path.join(DATA_DIR, "lst_depth_summary.csv")
    summary_fields = ["token", "fair_rate", "max_eth_out", "max_capacity_usd",
                      "usd_to_1pct", "usd_to_2pct", "usd_to_5pct",
                      "phantom_usd", "cascade_ratio"]
    with open(summary_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    print(f"Summary: {summary_path}")

    # Print summary table
    print(f"\n{'='*95}")
    print("LIQUIDITY DEPTH SUMMARY — Aggregated across all DEX pools")
    print(f"{'='*95}")
    print(f"{'Token':<8} {'DEX Cap':>12} {'→1% depeg':>12} {'→2% depeg':>12} "
          f"{'→5% depeg':>12} {'Phantom':>10} {'Cascade@2%':>12}")
    print("-" * 95)
    for s in summary:
        print(f"{s['token']:<8} {s['max_capacity_usd']:>12} {s['usd_to_1pct']:>12} "
              f"{s['usd_to_2pct']:>12} {s['usd_to_5pct']:>12} "
              f"{s['phantom_usd']:>10} {s['cascade_ratio']:>12}")

    return summary


if __name__ == "__main__":
    main()
