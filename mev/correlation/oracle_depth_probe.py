#!/usr/bin/env python3
"""Chainlink feed analysis + stETH/eETH DEX depth + oracle feed identification.

A. Chainlink stETH/ETH feed: pull last 20 rounds, compute update frequency
B. stETH→WETH and eETH→WETH DEX depth via Paraswap
C. weETH/osETH CAPO oracle feed identification
"""

import csv
import os
import time
from datetime import datetime, timezone

import requests

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/BNZuV78MYIdQEqymhrHikACnAGe5cTES"
PARASWAP_URL = "https://apiv5.paraswap.io/prices"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
STETH = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
EETH = "0x35fA164735182de50811E8e2E824cFb9B6118ac2"

CHAINLINK_STETH_ETH_PROXY = "0x86392dC19c0b719886221c78AB11eb8Cf5c52812"

SELL_AMOUNTS_ETH = [10, 50, 100, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000]
PARASWAP_DELAY = 1.1

# CAPO adapters (from Step 2)
CAPO_ADAPTERS = {
    "wstETH": "0xe1d97bf61901b075e9626c8a2340a7de385861ef",
    "weETH": "0x87625393534d5c102cadb66d37201df24cc26d4c",
    "osETH": "0x2b86d519ef34f8adfc9349cdea17c09aa9db60e2",
}


# ---------- Helpers ----------

def keccak_selector(sig: str) -> str:
    from Crypto.Hash import keccak
    k = keccak.new(digest_bits=256)
    k.update(sig.encode())
    return k.hexdigest()[:8]


def eth_call(to: str, data: str) -> str | None:
    payload = {"jsonrpc": "2.0", "method": "eth_call",
               "params": [{"to": to, "data": "0x" + data}, "latest"], "id": 1}
    resp = requests.post(ALCHEMY_URL, json=payload, timeout=30).json()
    if "error" in resp:
        return None
    raw = resp.get("result", "0x")
    return raw[2:] if raw not in ("0x", None) else None


def u256(h: str, slot: int = 0) -> int:
    return int(h[slot * 64:(slot + 1) * 64], 16)


def addr_from(h: str, slot: int = 0) -> str:
    return "0x" + h[slot * 64 + 24:(slot + 1) * 64]


def get_eth_price_usd() -> float:
    result = eth_call("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", "feaf968c")
    if result:
        return u256(result, 1) / 1e8
    return 2000.0


def paraswap_quote(src, dst, amount_wei, src_dec=18, dst_dec=18):
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
            return None
        except Exception as e:
            print(f"    Paraswap error: {e}")
            if attempt < 2:
                time.sleep(2)
    return None


def extract_route_dexes(route):
    dex_names = set()
    for path in route.get("bestRoute", []):
        for swap in path.get("swaps", []):
            for ex in swap.get("swapExchanges", []):
                dex_names.add(ex.get("exchange", "?"))
    return "+".join(sorted(dex_names)) if dex_names else "unknown"


# ---------- Task A: Chainlink stETH/ETH rounds ----------

def pull_chainlink_rounds():
    """Pull last 20 rounds from Chainlink stETH/ETH feed via proxy."""
    print("=" * 60)
    print("TASK A: Chainlink stETH/ETH Feed Analysis")
    print("=" * 60)

    sel_grd = keccak_selector("getRoundData(uint80)")

    # Get latest round ID from proxy
    r = eth_call(CHAINLINK_STETH_ETH_PROXY, "feaf968c")  # latestRoundData
    if not r:
        print("  ERROR: Cannot read latestRoundData from proxy")
        return []

    latest_round_id = u256(r, 0)
    # Decode: phaseId = roundId >> 64, aggregatorRoundId = roundId & mask
    phase_id = latest_round_id >> 64
    agg_round = latest_round_id & ((1 << 64) - 1)
    phase_base = phase_id << 64
    print(f"  Latest roundId: {latest_round_id} (phase={phase_id}, round={agg_round})")

    # Get aggregator address
    r_agg = eth_call(CHAINLINK_STETH_ETH_PROXY, keccak_selector("aggregator()"))
    if r_agg:
        agg_addr = addr_from(r_agg)
        print(f"  Aggregator: {agg_addr}")

    rounds = []
    for i in range(20):
        rid = phase_base + agg_round - i
        data = sel_grd + hex(rid)[2:].zfill(64)
        r = eth_call(CHAINLINK_STETH_ETH_PROXY, data)
        if r and len(r) >= 320:
            answer = u256(r, 1)
            started = u256(r, 2)
            updated = u256(r, 3)
            if updated > 0 and answer > 0:
                rounds.append({
                    "round": agg_round - i,
                    "answer": answer / 1e18,
                    "updated_at": updated,
                    "updated_utc": datetime.fromtimestamp(updated, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                })

    # Compute gaps and deviations
    for i in range(len(rounds) - 1):
        gap = rounds[i]["updated_at"] - rounds[i + 1]["updated_at"]
        dev = abs(rounds[i]["answer"] - rounds[i + 1]["answer"]) / rounds[i + 1]["answer"] * 100
        rounds[i]["gap_seconds"] = gap
        rounds[i]["gap_hours"] = gap / 3600
        rounds[i]["deviation_pct"] = dev
    if rounds:
        rounds[-1]["gap_seconds"] = 0
        rounds[-1]["gap_hours"] = 0
        rounds[-1]["deviation_pct"] = 0

    # Print
    print(f"\n  Last 20 rounds:")
    print(f"  {'Round':<8} {'Answer':<14} {'Updated (UTC)':<22} {'Gap (h)':<10} {'Dev (%)':<10}")
    print(f"  {'-'*68}")
    for rd in rounds:
        gap = f"{rd.get('gap_hours', 0):.1f}h" if rd.get('gap_hours', 0) > 0 else "-"
        dev = f"{rd.get('deviation_pct', 0):.4f}%" if rd.get('deviation_pct', 0) > 0 else "-"
        print(f"  {rd['round']:<8} {rd['answer']:<14.10f} {rd['updated_utc']:<22} {gap:<10} {dev:<10}")

    # Summary stats
    gaps = [rd["gap_seconds"] for rd in rounds if rd.get("gap_seconds", 0) > 0]
    devs = [rd["deviation_pct"] for rd in rounds if rd.get("deviation_pct", 0) > 0]
    answers = [rd["answer"] for rd in rounds]
    if gaps:
        avg_gap = sum(gaps) / len(gaps)
        max_gap = max(gaps)
        min_gap = min(gaps)
        print(f"\n  Update frequency: avg={avg_gap/3600:.1f}h, min={min_gap/3600:.1f}h, max={max_gap/3600:.1f}h")
    if devs:
        avg_dev = sum(devs) / len(devs)
        max_dev = max(devs)
        print(f"  Price deviation: avg={avg_dev:.4f}%, max={max_dev:.4f}%")
    if answers:
        answer_range = max(answers) - min(answers)
        print(f"  Answer range: {min(answers):.10f} to {max(answers):.10f} (spread={answer_range/min(answers)*100:.4f}%)")

    return rounds


# ---------- Task B: stETH and eETH DEX depth probes ----------

def probe_depth(token_name, token_addr, eth_price):
    """Probe sell depth for a token against WETH via Paraswap."""
    print(f"\n{'='*60}")
    print(f"Probing {token_name} ({token_addr[:12]}...) → WETH depth")
    print(f"{'='*60}")

    # Get fair rate from tiny quote
    amount_1 = 10 ** 18  # 1 token
    time.sleep(PARASWAP_DELAY)
    route = paraswap_quote(token_addr, WETH, amount_1)
    if not route:
        print(f"  Cannot get fair rate for {token_name}")
        return []
    fair_rate = int(route["destAmount"]) / 1e18
    print(f"  Fair rate: {fair_rate:.8f} ETH/{token_name} (${fair_rate * eth_price:.2f})")

    rows = []
    last_success_eth = None

    # Phase 1: sweep standard amounts
    for sell_eth in SELL_AMOUNTS_ETH:
        token_amount = sell_eth / fair_rate
        amount_wei = int(token_amount * 1e18)
        sell_usd = sell_eth * eth_price

        time.sleep(PARASWAP_DELAY)
        route = paraswap_quote(token_addr, WETH, amount_wei)

        if route is None:
            print(f"  {sell_eth:>8} ETH (${sell_usd / 1e6:>6.1f}M): NO ROUTE")
            rows.append(_make_row(token_name, sell_eth, sell_usd, token_amount, fair_rate))
            continue

        row = _parse_route(token_name, sell_eth, sell_usd, fair_rate, route)
        _print_row(row)
        rows.append(row)
        last_success_eth = sell_eth

    # Phase 2: refine between last success and first failure
    if last_success_eth is not None:
        first_fail_eth = None
        for sell_eth in SELL_AMOUNTS_ETH:
            if sell_eth > last_success_eth:
                first_fail_eth = sell_eth
                break

        if first_fail_eth is not None:
            print(f"  --- Refining between {last_success_eth} and {first_fail_eth} ETH ---")
            lo, hi = last_success_eth, first_fail_eth
            tested = set()
            for _ in range(4):
                mid = round((lo + hi) / 2)
                if mid in tested or mid == lo or mid == hi:
                    break
                tested.add(mid)
                token_amount = mid / fair_rate
                amount_wei = int(token_amount * 1e18)
                sell_usd = mid * eth_price

                time.sleep(PARASWAP_DELAY)
                route = paraswap_quote(token_addr, WETH, amount_wei)
                if route is None:
                    print(f"  {mid:>8} ETH (${sell_usd / 1e6:>6.1f}M): NO ROUTE")
                    rows.append(_make_row(token_name, mid, sell_usd, token_amount, fair_rate))
                    hi = mid
                else:
                    row = _parse_route(token_name, mid, sell_usd, fair_rate, route)
                    _print_row(row)
                    rows.append(row)
                    lo = mid

            # Fill in a few more points around the boundary
            for frac in [0.6, 0.7, 0.8, 0.9]:
                pt = round(last_success_eth + frac * (first_fail_eth - last_success_eth))
                if pt not in tested and pt != last_success_eth and pt != first_fail_eth:
                    tested.add(pt)
                    token_amount = pt / fair_rate
                    amount_wei = int(token_amount * 1e18)
                    sell_usd = pt * eth_price
                    time.sleep(PARASWAP_DELAY)
                    route = paraswap_quote(token_addr, WETH, amount_wei)
                    if route is None:
                        print(f"  {pt:>8} ETH (${sell_usd / 1e6:>6.1f}M): NO ROUTE")
                        rows.append(_make_row(token_name, pt, sell_usd, token_amount, fair_rate))
                    else:
                        row = _parse_route(token_name, pt, sell_usd, fair_rate, route)
                        _print_row(row)
                        rows.append(row)

    rows.sort(key=lambda r: float(r["sell_eth_equiv"]))
    return rows


def _make_row(token, sell_eth, sell_usd, sell_tokens, fair_rate):
    return {
        "token": token, "sell_eth_equiv": sell_eth, "sell_usd": int(sell_usd),
        "sell_tokens": f"{sell_tokens:.2f}", "fair_rate": f"{fair_rate:.8f}",
        "effective_rate": "N/A", "depeg_pct": "N/A", "eth_received": "N/A",
        "dex_route": "N/A",
    }


def _parse_route(token, sell_eth, sell_usd, fair_rate, route):
    dest_eth = int(route["destAmount"]) / 1e18
    src_tokens = int(route["srcAmount"]) / 1e18
    eff_rate = dest_eth / src_tokens if src_tokens > 0 else 0
    depeg = (fair_rate - eff_rate) / fair_rate * 100
    dexes = extract_route_dexes(route)
    return {
        "token": token, "sell_eth_equiv": sell_eth, "sell_usd": int(sell_usd),
        "sell_tokens": f"{src_tokens:.2f}", "fair_rate": f"{fair_rate:.8f}",
        "effective_rate": f"{eff_rate:.8f}", "depeg_pct": f"{depeg:.4f}",
        "eth_received": f"{dest_eth:.4f}", "dex_route": dexes,
    }


def _print_row(row):
    sell_eth = row["sell_eth_equiv"]
    sell_usd = float(row["sell_usd"])
    eff = float(row["effective_rate"])
    dep = float(row["depeg_pct"])
    eth_out = float(row["eth_received"])
    print(f"  {sell_eth:>8} ETH (${sell_usd / 1e6:>6.1f}M): "
          f"rate={eff:.6f} depeg={dep:>7.3f}% ETH_out={eth_out:>10.2f}  [{row['dex_route']}]")


def interpolate_threshold(rows, target_depeg):
    points = [(float(r["sell_usd"]), float(r["depeg_pct"]))
              for r in rows if r["depeg_pct"] != "N/A"]
    if not points:
        return None
    points.sort()
    if points[0][1] >= target_depeg:
        return target_depeg / points[0][1] * points[0][0] if points[0][1] > 0 else None
    if points[-1][1] < target_depeg:
        return None
    for i in range(len(points) - 1):
        u0, d0 = points[i]
        u1, d1 = points[i + 1]
        if d0 <= target_depeg <= d1:
            if d1 == d0:
                return u0
            return u0 + (target_depeg - d0) / (d1 - d0) * (u1 - u0)
    return None


# ---------- Task C: CAPO feed identification ----------

def identify_capo_feeds():
    """Identify sub-feeds for each CAPO adapter by price decomposition."""
    print(f"\n{'='*60}")
    print("TASK C: CAPO Oracle Feed Identification")
    print(f"{'='*60}")

    sel_rp = keccak_selector("RATIO_PROVIDER()")
    sel_sr = keccak_selector("getSnapshotRatio()")
    sel_st = keccak_selector("getSnapshotTimestamp()")
    sel_ic = keccak_selector("isCapped()")
    sel_la = "50d25bcd"  # latestAnswer
    sel_mg = keccak_selector("getMaxRatioGrowthPerSecond()")
    sel_md = keccak_selector("MINIMUM_SNAPSHOT_DELAY()")

    eth_price = get_eth_price_usd()
    results = []

    for name, adapter in CAPO_ADAPTERS.items():
        print(f"\n  --- {name} ---")
        row = {"token": name, "adapter": adapter}

        # latestAnswer (USD price, 8 decimals)
        r = eth_call(adapter, sel_la)
        usd_price = u256(r) / 1e8 if r else 0
        row["usd_price"] = usd_price
        print(f"  Aave USD price: ${usd_price:.2f}")

        # RATIO_PROVIDER
        r = eth_call(adapter, sel_rp)
        ratio_prov = addr_from(r) if r else "N/A"
        row["ratio_provider"] = ratio_prov
        print(f"  Ratio provider: {ratio_prov}")

        # snapshotRatio / isCapped
        r = eth_call(adapter, sel_sr)
        snap_ratio = u256(r) / 1e18 if r else 0
        row["snapshot_ratio"] = snap_ratio

        r = eth_call(adapter, sel_ic)
        is_capped = bool(u256(r)) if r else False
        row["is_capped"] = is_capped

        # snapshotTimestamp
        r = eth_call(adapter, sel_st)
        snap_ts = u256(r) if r else 0
        row["snapshot_timestamp"] = datetime.fromtimestamp(snap_ts, tz=timezone.utc).strftime(
            "%Y-%m-%d") if snap_ts else "N/A"

        # maxGrowthPerSecond
        r = eth_call(adapter, sel_mg)
        row["max_growth_per_sec"] = u256(r) if r else 0

        # MINIMUM_SNAPSHOT_DELAY
        r = eth_call(adapter, sel_md)
        row["min_delay_days"] = u256(r) / 86400 if r else 0

        # Get actual on-chain ratio from provider
        actual_ratio = 0
        for fn in ["stEthPerToken()", "getRate()"]:
            r = eth_call(ratio_prov, keccak_selector(fn))
            if r and u256(r) > 0:
                actual_ratio = u256(r) / 1e18
                row["actual_ratio"] = actual_ratio
                row["ratio_fn"] = fn
                print(f"  Actual ratio ({fn}): {actual_ratio:.8f}")
                break

        # Decompose: USD_price = ratio × market_feed_ETH × ETH/USD
        # Solve for market_feed_ETH = USD_price / (ratio × ETH/USD)
        effective_ratio = actual_ratio if not is_capped and actual_ratio > 0 else snap_ratio
        if effective_ratio > 0 and eth_price > 0:
            implied_market_feed = usd_price / (effective_ratio * eth_price)
            row["implied_market_feed"] = implied_market_feed
            print(f"  Implied market feed: {implied_market_feed:.8f} (should be ~1.0 for X/ETH)")
            if abs(implied_market_feed - 1.0) < 0.01:
                print(f"  → Market feed is ~1.0, suggesting direct ETH/USD pricing (no separate X/ETH feed)")
                row["feed_structure"] = "ratio × ETH/USD"
            else:
                print(f"  → Market feed deviates from 1.0, suggesting an intermediate X/ETH Chainlink feed")
                row["feed_structure"] = "ratio × X/ETH × ETH/USD"

        results.append(row)

    # Check known Chainlink feeds
    print(f"\n  --- Known Chainlink feeds ---")
    feeds = {
        "stETH/ETH": CHAINLINK_STETH_ETH_PROXY,
    }
    for feed_name, feed_addr in feeds.items():
        r = eth_call(feed_addr, "feaf968c")  # latestRoundData
        if r:
            answer = u256(r, 1)
            updated = u256(r, 3)
            dec_r = eth_call(feed_addr, "313ce567")
            dec = u256(dec_r) if dec_r else 18
            print(f"  {feed_name} ({feed_addr[:12]}...): {answer / 10**dec:.8f} "
                  f"(updated {datetime.fromtimestamp(updated, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')})")

    return results


# ---------- Main ----------

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    eth_price = get_eth_price_usd()
    print(f"ETH price: ${eth_price:.2f}\n")

    # Task A: Chainlink rounds
    rounds = pull_chainlink_rounds()
    if rounds:
        path = os.path.join(DATA_DIR, "chainlink_steth_eth_rounds.csv")
        fields = ["round", "answer", "updated_utc", "gap_seconds", "gap_hours", "deviation_pct"]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rounds)
        print(f"\n  Saved: {path}")

    # Task B: stETH and eETH depth probes
    all_depth_rows = {}
    for token_name, token_addr in [("stETH", STETH), ("eETH", EETH)]:
        rows = probe_depth(token_name, token_addr, eth_price)
        all_depth_rows[token_name] = rows

        csv_name = f"{token_name.lower()}_depth.csv"
        path = os.path.join(DATA_DIR, csv_name)
        fields = ["token", "sell_eth_equiv", "sell_usd", "sell_tokens", "fair_rate",
                  "effective_rate", "depeg_pct", "eth_received", "dex_route"]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"  Saved: {path}")

    # Depth comparison summary
    print(f"\n{'='*60}")
    print("DEPTH COMPARISON: Oracle-Facing Layer")
    print(f"{'='*60}")
    for token_name, rows in all_depth_rows.items():
        numeric = [r for r in rows if r["eth_received"] != "N/A"]
        if numeric:
            max_eth = max(float(r["eth_received"]) for r in numeric)
            max_sell = max(float(r["sell_eth_equiv"]) for r in numeric)
            for target in [0.5, 1.0, 2.0]:
                threshold = interpolate_threshold(rows, target)
                thr_str = f"${threshold / 1e6:.1f}M" if threshold else ">MAX"
                print(f"  {token_name}: {target}% depeg at {thr_str}")
            print(f"  {token_name}: max DEX capacity ~{max_eth:.0f} ETH (${max_eth * eth_price / 1e6:.1f}M)")
        else:
            print(f"  {token_name}: no successful quotes")

    # Task C: Oracle feed identification
    feed_results = identify_capo_feeds()
    if feed_results:
        path = os.path.join(DATA_DIR, "oracle_feeds.csv")
        all_keys = set()
        for r in feed_results:
            all_keys.update(r.keys())
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=sorted(all_keys))
            w.writeheader()
            w.writerows(feed_results)
        print(f"\n  Saved: {path}")

    return rounds, all_depth_rows, feed_results


if __name__ == "__main__":
    main()
