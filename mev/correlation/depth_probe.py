#!/usr/bin/env python3
"""DEX Liquidity Depth Probe for LST Tokens.

Simulates sells of increasing sizes through Uniswap V3 pools to measure
how much selling pressure produces 1%, 2%, 5% depeg from fair exchange rate.
Uses raw eth_call via Alchemy RPC — no web3.py dependency.
"""

import csv
import json
import os
import struct
import sys
from dataclasses import dataclass

import requests

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/BNZuV78MYIdQEqymhrHikACnAGe5cTES"

# Contracts
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
UNISWAP_V3_FACTORY = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
UNISWAP_V3_QUOTER_V2 = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"

# Curve pools (stETH-based)
CURVE_STETH_POOL = "0xDC24316b9AE028F1497c275EB9192a3Ea0f67022"
STETH = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"

# Fee tiers to scan
UNISWAP_FEE_TIERS = [100, 500, 3000, 10000]

# Sell amounts in USD
SELL_AMOUNTS_USD = [100_000, 500_000, 1_000_000, 5_000_000, 10_000_000,
                    25_000_000, 50_000_000, 100_000_000, 250_000_000, 500_000_000]

# Tiny amount for fair rate (0.01 ETH worth — small enough to not move the price)
FAIR_RATE_AMOUNT_ETH = 0.01

@dataclass
class Token:
    symbol: str
    address: str
    decimals: int = 18
    # For wstETH: wraps stETH, so fair rate comes from stEthPerToken()
    is_wsteth: bool = False


TOKENS = [
    Token("weETH", "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee"),
    Token("osETH", "0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38"),
    Token("rsETH", "0xA1290d69c65A6Fe4DF752f95823fae25cB99e5A7"),
    Token("wstETH", "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0", is_wsteth=True),
    Token("rETH", "0xae78736Cd615f374D3085123A210448E74Fc6393"),
    Token("cbETH", "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704"),
    Token("ETHx", "0xA35b1B31Ce002FBF2058D22F30f95D405200A15b"),
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# ---------- ABI encoding helpers ----------

def encode_address(addr: str) -> str:
    """Encode address as 32-byte hex (left-padded)."""
    return addr.lower().replace("0x", "").zfill(64)

def encode_uint256(val: int) -> str:
    """Encode uint256 as 32-byte hex."""
    return hex(val)[2:].zfill(64)

def encode_uint24(val: int) -> str:
    """Encode uint24 as 32-byte hex (left-padded)."""
    return hex(val)[2:].zfill(64)

def encode_uint160(val: int) -> str:
    """Encode uint160 as 32-byte hex."""
    return hex(val)[2:].zfill(64)

def decode_uint256(hex_str: str, slot: int = 0) -> int:
    """Decode uint256 from hex string at 32-byte slot index."""
    start = slot * 64  # each slot = 32 bytes = 64 hex chars
    return int(hex_str[start:start + 64], 16)

def function_selector(sig: str) -> str:
    """Compute 4-byte function selector from signature."""
    import hashlib
    return hashlib.sha3_256(sig.encode()).hexdigest()[:8]  # Wrong hash!

# Use keccak256 instead
def keccak256(data: bytes) -> bytes:
    """Keccak-256 hash."""
    from hashlib import sha3_256
    # Python's sha3_256 is NOT keccak256. We need to use a workaround.
    # Actually, Python 3.6+ hashlib has sha3_256 which is SHA-3, not Keccak.
    # For EVM, we need Keccak-256. Let's compute manually or use pysha3.
    # Simpler: hardcode the selectors we need.
    raise NotImplementedError("Use hardcoded selectors")

# Hardcoded function selectors (keccak256 of signature, first 4 bytes)
# getPool(address,address,uint24) => 0x1698ee82
SEL_GET_POOL = "1698ee82"
# quoteExactInputSingle((address,address,uint256,uint24,uint160)) => 0xc6a5026a
SEL_QUOTE_EXACT_INPUT_SINGLE = "c6a5026a"
# stEthPerToken() => 0x035faf82
SEL_ST_ETH_PER_TOKEN = "035faf82"
# get_dy(int128,int128,uint256) => 0x5e0d443f
SEL_GET_DY = "5e0d443f"
# decimals() => 0x313ce567
SEL_DECIMALS = "313ce567"


def eth_call(to: str, data: str, block: str = "latest") -> str | None:
    """Make an eth_call and return the result hex string (without 0x prefix).
    Returns None if the call reverts."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": to, "data": "0x" + data}, block],
        "id": 1,
    }
    resp = requests.post(ALCHEMY_URL, json=payload, timeout=30)
    result = resp.json()
    if "error" in result:
        return None
    raw = result.get("result", "0x")
    if raw == "0x" or raw is None:
        return None
    return raw[2:]  # strip 0x


def eth_call_batch(calls: list[tuple[str, str]], block: str = "latest") -> list[str | None]:
    """Batch eth_call. Each call is (to, data). Returns list of results."""
    payload = []
    for i, (to, data) in enumerate(calls):
        payload.append({
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{"to": to, "data": "0x" + data}, block],
            "id": i,
        })
    resp = requests.post(ALCHEMY_URL, json=payload, timeout=60)
    results_raw = resp.json()
    # Sort by id to maintain order
    if isinstance(results_raw, list):
        results_raw.sort(key=lambda x: x.get("id", 0))
    else:
        results_raw = [results_raw]

    results = []
    for r in results_raw:
        if "error" in r:
            results.append(None)
        else:
            raw = r.get("result", "0x")
            if raw == "0x" or raw is None:
                results.append(None)
            else:
                results.append(raw[2:])
    return results


def get_eth_price_usd() -> float:
    """Get current ETH price in USD from the price CSV or a simple RPC call."""
    # Use Chainlink ETH/USD feed: 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
    # latestRoundData() => 0xfeaf968c
    result = eth_call("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", "feaf968c")
    if result:
        # Returns (roundId, answer, startedAt, updatedAt, answeredInRound)
        # answer is at offset 1 (32 bytes each), 8 decimals
        answer = decode_uint256(result, slot=1)
        return answer / 1e8
    # Fallback
    return 2000.0


# ---------- Pool Discovery ----------

def discover_uniswap_pools(token: Token) -> list[tuple[str, int]]:
    """Find Uniswap V3 pools for token/WETH at all fee tiers.
    Returns list of (pool_address, fee_tier)."""
    pools = []
    # Batch all fee tier queries
    calls = []
    for fee in UNISWAP_FEE_TIERS:
        data = SEL_GET_POOL + encode_address(token.address) + encode_address(WETH) + encode_uint24(fee)
        calls.append((UNISWAP_V3_FACTORY, data))

    results = eth_call_batch(calls)
    for i, result in enumerate(results):
        if result:
            addr_int = decode_uint256(result, slot=0)
            if addr_int != 0:
                addr = "0x" + hex(addr_int)[2:].zfill(40)
                pools.append((addr, UNISWAP_FEE_TIERS[i]))
                print(f"  Found Uniswap V3 pool: {addr} fee={UNISWAP_FEE_TIERS[i]}")

    return pools


# ---------- Quote Simulation ----------

def quote_uniswap_v3(token_in: str, token_out: str, amount_in: int, fee: int) -> int | None:
    """Quote a swap via Uniswap V3 QuoterV2.
    Returns amount out, or None if insufficient liquidity."""
    # quoteExactInputSingle takes a struct:
    # (address tokenIn, address tokenOut, uint256 amountIn, uint24 fee, uint160 sqrtPriceLimitX96)
    # Encode as tuple: offset pointer (0x20) then the fields
    # Actually for QuoterV2, the param is a struct passed directly (no offset for single struct).
    # The ABI encoding of a single tuple param:
    data = (SEL_QUOTE_EXACT_INPUT_SINGLE +
            encode_address(token_in) +
            encode_address(token_out) +
            encode_uint256(amount_in) +
            encode_uint24(fee) +
            encode_uint160(0))  # sqrtPriceLimitX96 = 0

    result = eth_call(UNISWAP_V3_QUOTER_V2, data)
    if result and len(result) >= 64:
        amount_out = decode_uint256(result, slot=0)
        return amount_out
    return None


def get_fair_rate_uniswap(token: Token, pool_fee: int) -> float | None:
    """Get fair exchange rate by quoting a tiny amount.
    Returns LST/ETH rate (how much ETH per 1 LST)."""
    # Quote selling a tiny amount of the LST for WETH
    tiny_amount = int(FAIR_RATE_AMOUNT_ETH * 10**token.decimals)
    amount_out = quote_uniswap_v3(token.address, WETH, tiny_amount, pool_fee)
    if amount_out is None or amount_out == 0:
        return None
    return amount_out / tiny_amount  # ETH per LST (in raw units, but decimals cancel if both 18)


def get_wsteth_fair_rate() -> float | None:
    """Get wstETH fair rate from the contract: stEthPerToken()."""
    result = eth_call("0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0", SEL_ST_ETH_PER_TOKEN)
    if result:
        val = decode_uint256(result, slot=0)
        return val / 1e18
    return None


# ---------- Main Probe ----------

def probe_token(token: Token, eth_price: float) -> list[dict]:
    """Probe liquidity depth for a single token. Returns list of result rows."""
    print(f"\n{'='*60}")
    print(f"Probing {token.symbol} ({token.address})")
    print(f"{'='*60}")

    pools = discover_uniswap_pools(token)
    if not pools:
        print(f"  No Uniswap V3 pools found for {token.symbol}")
        return []

    rows = []

    for pool_addr, fee in pools:
        print(f"\n  Pool: {pool_addr} (fee={fee})")

        # Get fair rate
        fair_rate = get_fair_rate_uniswap(token, fee)
        if fair_rate is None:
            print(f"    Could not determine fair rate, skipping")
            continue

        # For wstETH, also check the contract rate
        if token.is_wsteth:
            contract_rate = get_wsteth_fair_rate()
            if contract_rate:
                print(f"    wstETH contract rate: {contract_rate:.6f} stETH/wstETH")
                print(f"    wstETH market rate:   {fair_rate:.6f} ETH/wstETH")

        print(f"    Fair rate: {fair_rate:.6f} ETH per {token.symbol}")

        # Probe each sell amount
        for sell_usd in SELL_AMOUNTS_USD:
            # Convert USD to token amount
            # token price in USD ≈ fair_rate * eth_price (since fair_rate is ETH per token)
            token_price_usd = fair_rate * eth_price
            token_amount = int((sell_usd / token_price_usd) * 10**token.decimals)

            amount_out = quote_uniswap_v3(token.address, WETH, token_amount, fee)

            if amount_out is None:
                print(f"    ${sell_usd/1e6:.1f}M: INSUFFICIENT LIQUIDITY")
                rows.append({
                    "token": token.symbol,
                    "sell_amount_usd": sell_usd,
                    "pool_type": f"uniswap_v3_{fee}",
                    "pool_address": pool_addr,
                    "fair_rate": f"{fair_rate:.8f}",
                    "effective_rate": "N/A",
                    "depeg_pct": "N/A",
                    "eth_received": "N/A",
                })
                continue

            effective_rate = (amount_out / 1e18) / (token_amount / 10**token.decimals)
            depeg_pct = (fair_rate - effective_rate) / fair_rate * 100
            eth_received = amount_out / 1e18

            print(f"    ${sell_usd/1e6:.1f}M: rate={effective_rate:.6f} depeg={depeg_pct:.3f}% "
                  f"ETH_out={eth_received:.2f}")

            rows.append({
                "token": token.symbol,
                "sell_amount_usd": sell_usd,
                "pool_type": f"uniswap_v3_{fee}",
                "pool_address": pool_addr,
                "fair_rate": f"{fair_rate:.8f}",
                "effective_rate": f"{effective_rate:.8f}",
                "depeg_pct": f"{depeg_pct:.4f}",
                "eth_received": f"{eth_received:.4f}",
            })

    return rows


def interpolate_threshold(rows: list[dict], target_depeg: float) -> float | None:
    """Interpolate to find USD sell amount that produces target_depeg%.
    Returns USD amount or None if not reachable."""
    # Filter to numeric rows, sorted by sell amount
    points = []
    for r in rows:
        if r["depeg_pct"] == "N/A":
            continue
        points.append((float(r["sell_amount_usd"]), float(r["depeg_pct"])))

    if not points:
        return None

    points.sort()

    # If target is below minimum observed depeg, extrapolate linearly from first two points
    if points[0][1] >= target_depeg:
        if len(points) >= 2:
            # Linear interp between 0,0 and first point
            usd0, dep0 = 0, 0
            usd1, dep1 = points[0]
            if dep1 - dep0 == 0:
                return None
            return usd0 + (target_depeg - dep0) / (dep1 - dep0) * (usd1 - usd0)
        return None

    # If target exceeds max observed and last row was a successful quote
    if points[-1][1] < target_depeg:
        # Check if there are N/A rows (insufficient liquidity) above
        max_successful_usd = points[-1][0]
        has_insufficient = any(r["depeg_pct"] == "N/A" and float(r["sell_amount_usd"]) > max_successful_usd
                              for r in rows)
        if has_insufficient:
            # Pool runs out before reaching target — return the last successful + marker
            return None  # Cannot reach this depeg, pool is exhausted
        # Extrapolate (less reliable)
        if len(points) >= 2:
            usd0, dep0 = points[-2]
            usd1, dep1 = points[-1]
            if dep1 - dep0 == 0:
                return None
            val = usd0 + (target_depeg - dep0) / (dep1 - dep0) * (usd1 - usd0)
            return val
        return None

    # Interpolate between bracketing points
    for i in range(len(points) - 1):
        usd0, dep0 = points[i]
        usd1, dep1 = points[i + 1]
        if dep0 <= target_depeg <= dep1:
            if dep1 - dep0 == 0:
                return usd0
            frac = (target_depeg - dep0) / (dep1 - dep0)
            return usd0 + frac * (usd1 - usd0)

    return None


# Phantom exposure by token (from position topology investigation)
PHANTOM_EXPOSURE = {
    "weETH": 230_000_000,   # $230M at <1% depeg
    "osETH": 332_000_000,   # $332M at 2-3%
    "rsETH": 880_000_000,   # $880M across 2-5%
    "wstETH": 1_700_000_000, # $1.7B
    "rETH": 200_000_000,    # estimate
    "cbETH": 150_000_000,   # estimate
    "ETHx": 100_000_000,    # estimate
}


def build_summary(all_rows: list[dict]) -> list[dict]:
    """Build summary table with depeg thresholds per token."""
    # Group rows by token + pool (use the pool with deepest liquidity)
    from collections import defaultdict
    by_token_pool = defaultdict(list)
    for r in all_rows:
        key = (r["token"], r["pool_type"], r["pool_address"])
        by_token_pool[key].append(r)

    # For each token, pick the pool that can absorb the most before depeg
    # (i.e., the one where the largest sell amount still has a quote)
    best_pool = {}
    for (token, pool_type, pool_addr), rows in by_token_pool.items():
        successful = [r for r in rows if r["depeg_pct"] != "N/A"]
        max_usd = max((float(r["sell_amount_usd"]) for r in successful), default=0)
        if token not in best_pool or max_usd > best_pool[token][0]:
            best_pool[token] = (max_usd, pool_type, pool_addr, rows)

    summary = []
    for token_sym in [t.symbol for t in TOKENS]:
        if token_sym not in best_pool:
            continue
        _, pool_type, pool_addr, rows = best_pool[token_sym]

        usd_1pct = interpolate_threshold(rows, 1.0)
        usd_2pct = interpolate_threshold(rows, 2.0)
        usd_5pct = interpolate_threshold(rows, 5.0)

        phantom = PHANTOM_EXPOSURE.get(token_sym, 0)

        # Cascade ratio at 2% depeg
        cascade_2pct = phantom / usd_2pct if usd_2pct and usd_2pct > 0 else None

        summary.append({
            "token": token_sym,
            "best_pool": f"{pool_type} ({pool_addr[:10]}...)",
            "usd_to_1pct_depeg": f"{usd_1pct/1e6:.1f}M" if usd_1pct else "EXHAUSTED",
            "usd_to_2pct_depeg": f"{usd_2pct/1e6:.1f}M" if usd_2pct else "EXHAUSTED",
            "usd_to_5pct_depeg": f"{usd_5pct/1e6:.1f}M" if usd_5pct else "EXHAUSTED",
            "phantom_exposure": f"{phantom/1e6:.0f}M",
            "cascade_ratio": f"{cascade_2pct:.1f}x" if cascade_2pct else "N/A",
        })

    return summary


def main():
    print("LST DEX Liquidity Depth Probe")
    print("=" * 60)

    # Get ETH price
    eth_price = get_eth_price_usd()
    print(f"ETH price: ${eth_price:.2f}")

    all_rows = []
    for token in TOKENS:
        rows = probe_token(token, eth_price)
        all_rows.extend(rows)

    # Write detailed results
    detail_path = os.path.join(DATA_DIR, "lst_liquidity_depth.csv")
    fields = ["token", "sell_amount_usd", "pool_type", "pool_address",
              "fair_rate", "effective_rate", "depeg_pct", "eth_received"]
    with open(detail_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nDetailed results: {detail_path} ({len(all_rows)} rows)")

    # Build and write summary
    summary = build_summary(all_rows)
    summary_path = os.path.join(DATA_DIR, "lst_depth_summary.csv")
    summary_fields = ["token", "best_pool", "usd_to_1pct_depeg", "usd_to_2pct_depeg",
                      "usd_to_5pct_depeg", "phantom_exposure", "cascade_ratio"]
    with open(summary_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary)
    print(f"Summary: {summary_path}")

    # Print summary table
    print(f"\n{'='*80}")
    print("LIQUIDITY DEPTH SUMMARY")
    print(f"{'='*80}")
    print(f"{'Token':<8} {'1% depeg':>12} {'2% depeg':>12} {'5% depeg':>12} {'Phantom':>10} {'Cascade':>10}")
    print("-" * 80)
    for s in summary:
        print(f"{s['token']:<8} {s['usd_to_1pct_depeg']:>12} {s['usd_to_2pct_depeg']:>12} "
              f"{s['usd_to_5pct_depeg']:>12} {s['phantom_exposure']:>10} {s['cascade_ratio']:>10}")


if __name__ == "__main__":
    main()
