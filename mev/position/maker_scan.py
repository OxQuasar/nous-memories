"""
Maker/Sky ETH vault scanner: enumerate all active ETH-collateral vaults,
compute liquidation prices, compare with Aave v3 real wall.

All Maker ETH vaults are "real" by construction — debt is always DAI/USDS,
never ETH. No looping/phantom positions possible.
"""

import csv
import sys
import time
from pathlib import Path

from web3 import Web3

print = lambda *args, **kwargs: (sys.stdout.write(" ".join(str(a) for a in args) + kwargs.get("end", "\n")), sys.stdout.flush())

# --- Constants ---

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
RPC_URL = (SCRIPT_DIR / "alchemy.txt").read_text().strip()

CDP_MANAGER = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
VAT = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B"
SPOT = "0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3"
MULTICALL3 = "0xcA11bde05977b3631167028862bE2a173976CA11"

# ETH-related ilk names
ETH_ILKS = ["ETH-A", "ETH-B", "ETH-C", "WSTETH-A", "WSTETH-B"]

MULTICALL_BATCH = 200


def load_eth_price() -> float:
    csv_path = SCRIPT_DIR.parent / "data" / "eth_price_1h.csv"
    with open(csv_path) as f:
        lines = f.readlines()
    return float(lines[-1].strip().split(",")[2])


def pad_ilk(name: str) -> bytes:
    """Convert ilk name to bytes32."""
    return name.encode().ljust(32, b"\x00")


def get_ilk_params(w3: Web3) -> dict:
    """Get rate accumulator and liquidation ratio for each ETH ilk."""
    vat_abi = [{"inputs": [{"type": "bytes32"}], "name": "ilks", "outputs": [
        {"type": "uint256"}, {"type": "uint256"}, {"type": "uint256"},
        {"type": "uint256"}, {"type": "uint256"}
    ], "stateMutability": "view", "type": "function"}]
    vat = w3.eth.contract(address=Web3.to_checksum_address(VAT), abi=vat_abi)

    spot_abi = [{"inputs": [{"type": "bytes32"}], "name": "ilks", "outputs": [
        {"type": "address"}, {"type": "uint256"}
    ], "stateMutability": "view", "type": "function"}]
    spot = w3.eth.contract(address=Web3.to_checksum_address(SPOT), abi=spot_abi)

    params = {}
    for name in ETH_ILKS:
        ilk = pad_ilk(name)
        Art, rate, spot_val, line, dust = vat.functions.ilks(ilk).call()
        _, mat = spot.functions.ilks(ilk).call()
        params[name] = {
            "rate": rate / 1e27,
            "mat": mat / 1e27,
            "total_art": Art / 1e18,
            "dust": dust / 1e45,
        }
        total_debt = Art / 1e18 * rate / 1e27
        print(f"  {name:>12s}: mat={mat/1e27:.2f} ({mat/1e27*100:.0f}%)  rate={rate/1e27:.6f}  total_debt=${total_debt:>12,.0f}")
    return params


def scan_vaults(w3: Web3, ilk_params: dict) -> list[dict]:
    """Enumerate all CDPs, filter to active ETH vaults, read collateral & debt."""
    mgr_cs = Web3.to_checksum_address(CDP_MANAGER)
    vat_cs = Web3.to_checksum_address(VAT)
    mc_cs = Web3.to_checksum_address(MULTICALL3)

    # Get total CDP count
    cdpi_abi = [{"inputs": [], "name": "cdpi", "outputs": [{"type": "uint256"}],
                 "stateMutability": "view", "type": "function"}]
    mgr = w3.eth.contract(address=mgr_cs, abi=cdpi_abi)
    total_cdps = mgr.functions.cdpi().call()
    print(f"  Total CDPs: {total_cdps}")

    # Function selectors
    ilks_sel = bytes.fromhex("2c2cb9fd")  # CdpManager.ilks(uint256)
    urns_sel = bytes.fromhex("2726b073")  # CdpManager.urns(uint256)

    multicall_abi = [{"inputs": [{"name": "requireSuccess", "type": "bool"},
                                  {"components": [{"name": "target", "type": "address"},
                                                  {"name": "callData", "type": "bytes"}],
                                   "name": "calls", "type": "tuple[]"}],
                      "name": "tryAggregate",
                      "outputs": [{"components": [{"name": "success", "type": "bool"},
                                                   {"name": "returnData", "type": "bytes"}],
                                    "name": "returnData", "type": "tuple[]"}],
                      "stateMutability": "view", "type": "function"}]
    multicall = w3.eth.contract(address=mc_cs, abi=multicall_abi)

    eth_ilk_bytes = {pad_ilk(name) for name in ETH_ILKS}

    # Phase 1: Batch read ilks and urns for all CDPs
    print("  Phase 1: Reading CDP ilks and urns...")
    cdp_info = {}  # cdp_id -> (ilk_name, urn_addr)
    total_batches = (total_cdps + MULTICALL_BATCH - 1) // MULTICALL_BATCH

    for batch_start in range(1, total_cdps + 1, MULTICALL_BATCH):
        batch_end = min(batch_start + MULTICALL_BATCH, total_cdps + 1)
        batch_ids = list(range(batch_start, batch_end))

        calls = []
        for cdp_id in batch_ids:
            id_bytes = cdp_id.to_bytes(32, "big")
            calls.append((mgr_cs, ilks_sel + id_bytes))
            calls.append((mgr_cs, urns_sel + id_bytes))

        for attempt in range(3):
            try:
                results = multicall.functions.tryAggregate(False, calls).call()
                break
            except Exception as e:
                if attempt < 2:
                    print(f"    Multicall failed ({e}), retrying...")
                    time.sleep(2)
                else:
                    raise

        for j, cdp_id in enumerate(batch_ids):
            ilk_ok, ilk_data = results[j * 2]
            urn_ok, urn_data = results[j * 2 + 1]
            if not (ilk_ok and urn_ok):
                continue

            ilk_raw = ilk_data[:32]
            urn_addr = "0x" + urn_data[-20:].hex()

            if ilk_raw in eth_ilk_bytes:
                ilk_name = ilk_raw.decode().rstrip("\x00")
                cdp_info[cdp_id] = (ilk_name, urn_addr)

        batch_num = (batch_start - 1) // MULTICALL_BATCH + 1
        if batch_num % 10 == 0 or batch_num == total_batches:
            print(f"    Batch {batch_num}/{total_batches}: {len(cdp_info)} ETH CDPs found")

    print(f"  Found {len(cdp_info)} ETH-related CDPs")

    # Phase 2: Batch read Vat.urns(ilk, urn) for ETH CDPs
    print("  Phase 2: Reading vault state (ink, art)...")
    vat_urns_sel = bytes.fromhex("2424be5c")  # Vat.urns(bytes32,address)

    cdp_list = list(cdp_info.items())
    vaults = []
    total_batches2 = (len(cdp_list) + MULTICALL_BATCH - 1) // MULTICALL_BATCH

    for i in range(0, len(cdp_list), MULTICALL_BATCH):
        batch = cdp_list[i:i + MULTICALL_BATCH]
        calls = []
        for cdp_id, (ilk_name, urn_addr) in batch:
            ilk_bytes = pad_ilk(ilk_name)
            urn_bytes = bytes(12) + bytes.fromhex(urn_addr[2:])
            calls.append((vat_cs, vat_urns_sel + ilk_bytes + urn_bytes))

        for attempt in range(3):
            try:
                results = multicall.functions.tryAggregate(False, calls).call()
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise

        for j, (cdp_id, (ilk_name, urn_addr)) in enumerate(batch):
            ok, data = results[j]
            if not ok or len(data) < 64:
                continue
            ink = int.from_bytes(data[:32], "big") / 1e18
            art = int.from_bytes(data[32:64], "big") / 1e18

            if art > 0 and ink > 0:
                params = ilk_params[ilk_name]
                debt_dai = art * params["rate"]
                liq_price = debt_dai * params["mat"] / ink
                vaults.append({
                    "cdp_id": cdp_id,
                    "ilk": ilk_name,
                    "ink_eth": ink,
                    "art": art,
                    "debt_dai": debt_dai,
                    "liq_price": liq_price,
                    "mat": params["mat"],
                })

        batch_num = i // MULTICALL_BATCH + 1
        if batch_num % 5 == 0 or batch_num == total_batches2:
            print(f"    Batch {batch_num}/{total_batches2}: {len(vaults)} active vaults")

    return vaults


# --- Main ---

if __name__ == "__main__":
    t0 = time.time()

    eth_price = load_eth_price()
    print(f"ETH reference price: ${eth_price:.2f}")

    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 60}))
    assert w3.is_connected()
    print(f"Connected to Ethereum, block {w3.eth.block_number}")

    # Get ilk parameters
    print("\n--- Ilk parameters ---")
    ilk_params = get_ilk_params(w3)

    # Scan all vaults
    print("\n--- Scanning vaults ---")
    vaults = scan_vaults(w3, ilk_params)

    # Save CSV
    output_path = DATA_DIR / "maker_vaults.csv"
    fields = ["cdp_id", "ilk", "ink_eth", "debt_dai", "liq_price", "mat"]
    with open(output_path, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(vaults)
    print(f"\n  Saved {len(vaults)} vaults to {output_path}")

    # --- Analysis ---
    print("\n" + "=" * 70)
    print("MAKER ETH VAULT ANALYSIS")
    print("=" * 70)

    # Per-ilk summary
    print("\nPer-ilk summary:")
    print(f"  {'Ilk':>12s} {'Vaults':>8s} {'Collateral ETH':>16s} {'Collateral USD':>16s} {'Debt DAI':>16s}")
    for name in ETH_ILKS:
        ilk_vaults = [v for v in vaults if v["ilk"] == name]
        if ilk_vaults:
            total_ink = sum(v["ink_eth"] for v in ilk_vaults)
            total_debt = sum(v["debt_dai"] for v in ilk_vaults)
            col_usd = total_ink * eth_price
            print(f"  {name:>12s} {len(ilk_vaults):>8d} {total_ink:>16,.1f} ${col_usd:>14,.0f} ${total_debt:>14,.0f}")

    total_ink = sum(v["ink_eth"] for v in vaults)
    total_debt = sum(v["debt_dai"] for v in vaults)
    print(f"  {'TOTAL':>12s} {len(vaults):>8d} {total_ink:>16,.1f} ${total_ink * eth_price:>14,.0f} ${total_debt:>14,.0f}")

    # Liquidation price distribution
    print(f"\nLiquidation price distribution (ETH ref: ${eth_price:.2f}):")
    bands = [5, 10, 20, 30, 50]
    for band in bands:
        threshold = eth_price * (1 - band / 100)
        in_band = [v for v in vaults if v["liq_price"] >= threshold and v["liq_price"] < eth_price]
        debt = sum(v["debt_dai"] for v in in_band)
        col = sum(v["ink_eth"] for v in in_band) * eth_price
        print(f"  Within {band:>2d}% below: {len(in_band):>5d} vaults  ${debt:>14,.0f} debt  ${col:>14,.0f} collateral")

    # Cumulative from below
    print(f"\nCumulative within band:")
    for band in bands:
        threshold = eth_price * (1 - band / 100)
        in_band = [v for v in vaults if v["liq_price"] >= threshold]
        debt = sum(v["debt_dai"] for v in in_band)
        print(f"  Liq price >= ${threshold:>8,.0f} ({band:>2d}% below): {len(in_band):>5d} vaults  ${debt:>14,.0f} debt")

    # Top 15 density bins ($50 wide)
    print(f"\nTop 15 liquidation price bins ($50 wide):")
    bin_width = 50
    bins = {}
    for v in vaults:
        b = int(v["liq_price"] / bin_width) * bin_width
        if b not in bins:
            bins[b] = {"count": 0, "debt": 0.0, "collateral_eth": 0.0}
        bins[b]["count"] += 1
        bins[b]["debt"] += v["debt_dai"]
        bins[b]["collateral_eth"] += v["ink_eth"]

    top_bins = sorted(bins.items(), key=lambda x: x[1]["debt"], reverse=True)[:15]
    print(f"  {'Price Range':>16s} {'Vaults':>8s} {'Debt DAI':>16s} {'Coll ETH':>14s} {'Pct Below':>10s}")
    for price, info in sorted(top_bins, key=lambda x: -x[0]):
        pct = (eth_price - price) / eth_price * 100
        print(f"  ${price:>5,.0f}-${price+bin_width:>5,.0f} {info['count']:>8d} ${info['debt']:>14,.0f} {info['collateral_eth']:>13,.1f} {pct:>9.1f}%")

    # Top 10 vaults
    top10 = sorted(vaults, key=lambda v: v["debt_dai"], reverse=True)[:10]
    print(f"\nTop 10 vaults by debt:")
    print(f"  {'CDP':>8s} {'Ilk':>10s} {'Coll ETH':>14s} {'Coll USD':>14s} {'Debt DAI':>14s} {'LiqPrice':>10s} {'Pct Below':>10s}")
    for v in top10:
        pct = (eth_price - v["liq_price"]) / eth_price * 100
        print(f"  {v['cdp_id']:>8d} {v['ilk']:>10s} {v['ink_eth']:>13,.1f} ${v['ink_eth']*eth_price:>12,.0f} ${v['debt_dai']:>12,.0f} ${v['liq_price']:>8,.0f} {pct:>9.1f}%")

    # Load Aave decomposed data for comparison
    print(f"\n--- Comparison: Maker vs Aave v3 Real Wall ---")
    aave_real = {}
    try:
        with open(DATA_DIR / "positions_decomposed.csv") as f:
            for row in csv.DictReader(f):
                if row["position_type"] == "real" and row["eth_dominant"] == "True" and row["liq_price_usd"]:
                    lp = float(row["liq_price_usd"])
                    if 0 < lp < eth_price:
                        for band in bands:
                            threshold = eth_price * (1 - band / 100)
                            if lp >= threshold:
                                aave_real.setdefault(band, {"count": 0, "debt": 0.0})
                                aave_real[band]["count"] += 1
                                aave_real[band]["debt"] += float(row["debt_usd"])
    except FileNotFoundError:
        print("  (Aave decomposed data not found)")

    print(f"  {'Band':>6s} {'Aave Real Debt':>16s} {'Maker Debt':>16s} {'Combined':>16s} {'Maker %':>8s}")
    for band in bands:
        threshold = eth_price * (1 - band / 100)
        maker_in = [v for v in vaults if v["liq_price"] >= threshold and v["liq_price"] < eth_price]
        maker_debt = sum(v["debt_dai"] for v in maker_in)
        aave_info = aave_real.get(band, {"count": 0, "debt": 0.0})
        combined = aave_info["debt"] + maker_debt
        maker_pct = maker_debt / combined * 100 if combined > 0 else 0
        print(f"  {band:>5d}% ${aave_info['debt']:>14,.0f} ${maker_debt:>14,.0f} ${combined:>14,.0f} {maker_pct:>7.1f}%")

    print(f"\nCompleted in {time.time() - t0:.1f}s")
