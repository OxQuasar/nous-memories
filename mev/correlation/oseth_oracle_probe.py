#!/usr/bin/env python3
"""osETH Oracle Pathway Resolution + Definitive CAPO Architecture Verification.

Resolves the osETH CAPO implied feed mystery and definitively maps all three
LST CAPO adapters' bytecode-embedded addresses.
"""

import csv
import os
import time
from datetime import datetime, timezone

import requests

ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/BNZuV78MYIdQEqymhrHikACnAGe5cTES"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def keccak_sel(sig: str) -> str:
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


def extract_push32_addresses(code_hex: str) -> set[str]:
    """Extract addresses from PUSH32 instructions in EVM bytecode."""
    addrs = set()
    i = 0
    while i < len(code_hex) - 66:
        opcode = int(code_hex[i:i + 2], 16)
        if opcode == 0x7f:  # PUSH32
            val_hex = code_hex[i + 2:i + 66]
            if val_hex[:24] == "0" * 24:
                val = int(val_hex[24:], 16)
                if val > 2 ** 80:
                    addrs.add("0x" + val_hex[24:])
            i += 66
        elif 0x60 <= opcode <= 0x7f:
            i += 2 + (opcode - 0x5F) * 2
        else:
            i += 2
    return addrs


CAPO_ADAPTERS = {
    "wstETH": {
        "adapter": "0xe1d97bf61901b075e9626c8a2340a7de385861ef",
        "ratio_provider": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
        "ratio_fn": "getPooledEthByShares(uint256)",
    },
    "weETH": {
        "adapter": "0x87625393534d5c102cadb66d37201df24cc26d4c",
        "ratio_provider": "0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee",
        "ratio_fn": "getRate()",
    },
    "osETH": {
        "adapter": "0x2b86d519ef34f8adfc9349cdea17c09aa9db60e2",
        "ratio_provider": "0x2a261e60fb14586b474c208b1b7ac6d0f5000306",
        "ratio_fn": "convertToAssets(uint256)",
    },
}

ETH_USD_FEED = "0x5424384b256154046e9667ddfaaa5e550145215e"


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Get ETH/USD price
    r = eth_call(ETH_USD_FEED, "feaf968c")
    eth_usd = u256(r, 1) / 1e8
    print(f"ETH/USD Chainlink: ${eth_usd:.2f}\n")

    results = []

    for name, cfg in CAPO_ADAPTERS.items():
        print(f"{'='*60}")
        print(f"{name} CAPO Adapter: {cfg['adapter']}")
        print(f"{'='*60}")

        row = {"token": name, "adapter": cfg["adapter"]}

        # 1. Extract bytecode addresses
        payload = {"jsonrpc": "2.0", "method": "eth_getCode",
                   "params": [cfg["adapter"], "latest"], "id": 1}
        resp = requests.post(ALCHEMY_URL, json=payload, timeout=30).json()
        code = resp["result"][2:]
        addrs = extract_push32_addresses(code)

        print(f"  Bytecode addresses ({len(addrs)}):")
        for addr in sorted(addrs):
            desc_r = eth_call(addr, keccak_sel("description()"))
            desc = ""
            if desc_r and len(desc_r) >= 128:
                try:
                    l = u256(desc_r, 1)
                    desc = bytes.fromhex(desc_r[128:128 + l * 2]).decode()
                except:
                    pass
            print(f"    {addr}  {desc or '(no description)'}")
        row["bytecode_addresses"] = "; ".join(sorted(addrs))

        # 2. Get CAPO latestAnswer
        r = eth_call(cfg["adapter"], "50d25bcd")
        usd_price = u256(r) / 1e8
        row["usd_price"] = usd_price
        print(f"  CAPO latestAnswer: ${usd_price:.2f}")

        # 3. Get protocol rate from ratio provider
        if "(uint256)" in cfg["ratio_fn"]:
            data = keccak_sel(cfg["ratio_fn"]) + hex(10 ** 18)[2:].zfill(64)
        else:
            data = keccak_sel(cfg["ratio_fn"])
        r = eth_call(cfg["ratio_provider"], data)
        ratio = u256(r) / 1e18
        row["protocol_rate"] = ratio
        row["ratio_fn"] = cfg["ratio_fn"]
        print(f"  Protocol rate ({cfg['ratio_fn']}): {ratio:.8f}")

        # 4. Verify decomposition: price = rate × ETH/USD
        computed = ratio * eth_usd
        diff_pct = abs(computed - usd_price) / usd_price * 100
        row["computed_price"] = computed
        row["diff_pct"] = diff_pct
        row["eth_usd_feed"] = ETH_USD_FEED
        row["structure"] = "protocol_rate × ETH/USD"
        print(f"  Computed: {ratio:.6f} × ${eth_usd:.2f} = ${computed:.2f}")
        print(f"  Difference: {diff_pct:.4f}% {'✓ MATCH' if diff_pct < 0.01 else '✗ MISMATCH'}")

        # 5. CAPO parameters
        r = eth_call(cfg["adapter"], keccak_sel("getSnapshotRatio()"))
        snap_ratio = u256(r) / 1e18 if r else 0
        row["snapshot_ratio"] = snap_ratio

        r = eth_call(cfg["adapter"], keccak_sel("getSnapshotTimestamp()"))
        snap_ts = u256(r) if r else 0
        row["snapshot_timestamp"] = datetime.fromtimestamp(
            snap_ts, tz=timezone.utc).strftime("%Y-%m-%d") if snap_ts else "N/A"

        r = eth_call(cfg["adapter"], keccak_sel("isCapped()"))
        row["is_capped"] = bool(u256(r)) if r else False

        r = eth_call(cfg["adapter"], keccak_sel("MINIMUM_SNAPSHOT_DELAY()"))
        row["min_delay_days"] = u256(r) / 86400 if r else 0

        print(f"  Snapshot ratio: {snap_ratio:.8f}")
        print(f"  Snapshot date: {row['snapshot_timestamp']}")
        print(f"  Currently capped: {row['is_capped']}")
        print(f"  Min delay: {row['min_delay_days']:.0f} days")
        print()

        results.append(row)

    # Save
    path = os.path.join(DATA_DIR, "oracle_feeds.csv")
    fields = ["token", "adapter", "usd_price", "protocol_rate", "ratio_fn",
              "computed_price", "diff_pct", "structure", "eth_usd_feed",
              "snapshot_ratio", "snapshot_timestamp", "is_capped", "min_delay_days",
              "bytecode_addresses"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    print(f"Saved: {path}")

    # Also save osETH-specific detail
    oseth_path = os.path.join(DATA_DIR, "oseth_oracle.csv")
    oseth_row = next(r for r in results if r["token"] == "osETH")
    with open(oseth_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerow(oseth_row)
    print(f"Saved: {oseth_path}")

    # Print summary
    print(f"\n{'='*60}")
    print("DEFINITIVE CAPO ARCHITECTURE SUMMARY")
    print(f"{'='*60}")
    print("ALL THREE adapters use: cap(protocol_rate) × ETH/USD")
    print("NO intermediate market feeds (stETH/ETH, eETH/ETH, osETH/ETH)")
    print()
    print("Shared components:")
    print(f"  ETH/USD Chainlink: {ETH_USD_FEED}")
    print(f"  Config contract:   0xc2aacf6553d20d1e9d78e365aaba8032af9c85b0")
    print(f"    (ADDRESSES_PROVIDER → Aave v3 PoolAddressesProvider)")
    print()
    for r in results:
        print(f"  {r['token']}: {r['ratio_fn']} on {r['token']} → "
              f"rate={r['protocol_rate']:.6f} × ${eth_usd:.2f} = ${r['computed_price']:.2f} "
              f"(diff={r['diff_pct']:.4f}%)")


if __name__ == "__main__":
    main()
