"""
Historical Aave v2 position snapshot at June 10, 2022 (block 14935369).

Approach:
  1. Get all v2 reserve debt tokens at historical block
  2. Scan debtToken mint events via alchemy_getAssetTransfers to find borrowers
  3. Multicall getUserAccountData at historical block for accurate HF
  4. Scan userReserveData for collateral/debt breakdown (asset-level)
  5. Classify real vs phantom, compute liquidation prices
"""

import csv
import sys
import time
from pathlib import Path

import requests
from web3 import Web3

print = lambda *args, **kwargs: (sys.stdout.write(" ".join(str(a) for a in args) + kwargs.get("end", "\n")), sys.stdout.flush())

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

RPC_URL = (SCRIPT_DIR / "alchemy.txt").read_text().strip()

# Aave v2 contracts
LENDING_POOL_V2 = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
PROTOCOL_DATA_PROVIDER = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"
PRICE_ORACLE_V2 = "0xA50ba011c48153De246E5192C8f9258A2ba79Ca9"
MULTICALL3 = "0xcA11bde05977b3631167028862bE2a173976CA11"

# June 10, 2022 00:00 UTC
TARGET_BLOCK = 14935369
V2_DEPLOY_BLOCK = 11362579

ETH_CORRELATED_2022 = {"WETH", "stETH", "wstETH"}
STABLECOINS_2022 = {"USDC", "USDT", "DAI", "FRAX", "LUSD", "BUSD", "GUSD", "sUSD", "TUSD", "USDP", "FEI", "UST"}

PHANTOM_THRESHOLD = 0.8
REAL_THRESHOLD = 0.2
MULTICALL_BATCH = 100
RESERVE_BATCH = 500  # larger batch for per-reserve multicalls

# Only query reserves that matter for classification. Covers >99% of TVL.
KEY_RESERVES_2022 = {
    "WETH", "stETH", "wstETH",  # ETH-correlated
    "USDC", "USDT", "DAI", "FRAX", "LUSD", "BUSD", "GUSD", "sUSD", "TUSD", "USDP", "FEI", "UST",  # stablecoins
    "WBTC", "LINK", "AAVE", "UNI", "CRV", "SNX", "MKR", "ENS", "BAL",  # major alts
}


def load_eth_price_at_date() -> float:
    """Get ETH/USD price closest to June 10, 2022 00:00 UTC."""
    csv_path = SCRIPT_DIR.parent / "data" / "eth_price_1h.csv"
    target_ts = 1654819200
    best_price = 0.0
    best_diff = float("inf")
    with open(csv_path) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split(",")
            ts = int(parts[1])
            diff = abs(ts - target_ts)
            if diff < best_diff:
                best_diff = diff
                best_price = float(parts[2])
            if ts > target_ts + 7200:
                break
    return best_price


def get_reserve_info(w3: Web3) -> list[dict]:
    """Get all v2 reserves and their token addresses at historical block."""
    pool_abi = [{"inputs": [], "name": "getReservesList", "outputs": [{"type": "address[]"}],
                 "stateMutability": "view", "type": "function"}]
    pool = w3.eth.contract(address=Web3.to_checksum_address(LENDING_POOL_V2), abi=pool_abi)
    reserves = pool.functions.getReservesList().call(block_identifier=TARGET_BLOCK)

    pdp_abi = [{"inputs": [{"type": "address"}], "name": "getReserveTokensAddresses",
                "outputs": [{"type": "address"}, {"type": "address"}, {"type": "address"}],
                "stateMutability": "view", "type": "function"}]
    pdp = w3.eth.contract(address=Web3.to_checksum_address(PROTOCOL_DATA_PROVIDER), abi=pdp_abi)

    # ERC20 symbol ABI
    sym_abi = [{"inputs": [], "name": "symbol", "outputs": [{"type": "string"}],
                "stateMutability": "view", "type": "function"},
               {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}],
                "stateMutability": "view", "type": "function"}]

    info = []
    for addr in reserves:
        cs = Web3.to_checksum_address(addr)
        aToken, stableDebt, varDebt = pdp.functions.getReserveTokensAddresses(cs).call(block_identifier=TARGET_BLOCK)
        token = w3.eth.contract(address=cs, abi=sym_abi)
        try:
            symbol = token.functions.symbol().call(block_identifier=TARGET_BLOCK)
            decimals = token.functions.decimals().call(block_identifier=TARGET_BLOCK)
        except Exception:
            symbol = "UNKNOWN"
            decimals = 18
        info.append({
            "address": addr.lower(),
            "symbol": symbol,
            "decimals": decimals,
            "aToken": aToken.lower(),
            "stableDebtToken": stableDebt.lower(),
            "variableDebtToken": varDebt.lower(),
        })
    return info


def find_borrowers(reserve_info: list[dict]) -> set[str]:
    """Find all addresses that ever borrowed via debt token mints.
    
    Scan all debt tokens in a single alchemy_getAssetTransfers call per page
    by batching contract addresses.
    """
    all_debt_tokens = []
    for r in reserve_info:
        all_debt_tokens.append(Web3.to_checksum_address(r["variableDebtToken"]))
        all_debt_tokens.append(Web3.to_checksum_address(r["stableDebtToken"]))

    borrowers = set()
    page_key = None
    total_transfers = 0
    pages = 0

    while True:
        params = {
            "fromBlock": hex(V2_DEPLOY_BLOCK),
            "toBlock": hex(TARGET_BLOCK),
            "fromAddress": "0x0000000000000000000000000000000000000000",
            "contractAddresses": all_debt_tokens,
            "category": ["erc20"],
            "maxCount": "0x3e8",
            "withMetadata": False,
            "excludeZeroValue": True,
        }
        if page_key:
            params["pageKey"] = page_key

        for attempt in range(3):
            try:
                r = requests.post(RPC_URL, json={
                    "id": 1, "jsonrpc": "2.0",
                    "method": "alchemy_getAssetTransfers",
                    "params": [params]
                }, timeout=60)
                data = r.json()
                if "error" not in data:
                    break
            except Exception:
                pass
            time.sleep(2)
        else:
            if "error" in data:
                print(f"    Error: {data['error']}")
                break

        transfers = data["result"]["transfers"]
        for t in transfers:
            borrowers.add(t["to"].lower())

        total_transfers += len(transfers)
        pages += 1
        if pages % 20 == 0:
            print(f"    Page {pages}: {total_transfers} transfers, {len(borrowers)} unique borrowers")

        page_key = data["result"].get("pageKey")
        if not page_key:
            break
        time.sleep(0.2)

    print(f"    Total: {pages} pages, {total_transfers} transfers, {len(borrowers)} unique borrowers")
    return borrowers


def batch_get_account_data(w3: Web3, addresses: list[str]) -> dict[str, dict]:
    """Multicall getUserAccountData at historical block."""
    mc_abi = [{"inputs": [{"name": "requireSuccess", "type": "bool"},
                           {"components": [{"name": "target", "type": "address"},
                                           {"name": "callData", "type": "bytes"}],
                            "name": "calls", "type": "tuple[]"}],
               "name": "tryAggregate",
               "outputs": [{"components": [{"name": "success", "type": "bool"},
                                            {"name": "returnData", "type": "bytes"}],
                             "name": "returnData", "type": "tuple[]"}],
               "stateMutability": "view", "type": "function"}]
    multicall = w3.eth.contract(address=Web3.to_checksum_address(MULTICALL3), abi=mc_abi)

    selector = bytes.fromhex("bf92857c")  # getUserAccountData(address)
    pool_cs = Web3.to_checksum_address(LENDING_POOL_V2)

    eth_price = load_eth_price_at_date()
    results = {}
    total_batches = (len(addresses) + MULTICALL_BATCH - 1) // MULTICALL_BATCH

    for i in range(0, len(addresses), MULTICALL_BATCH):
        batch = addresses[i:i + MULTICALL_BATCH]
        calls = []
        for addr in batch:
            calldata = selector + bytes(12) + bytes.fromhex(addr[2:] if addr.startswith("0x") else addr)
            calls.append((pool_cs, calldata))

        for attempt in range(3):
            try:
                ret = multicall.functions.tryAggregate(False, calls).call(block_identifier=TARGET_BLOCK)
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise

        for addr, (ok, data) in zip(batch, ret):
            if not ok or len(data) < 192:
                continue
            # v2 returns values in ETH (18 decimals), not USD
            col_eth = int.from_bytes(data[0:32], "big") / 1e18
            debt_eth = int.from_bytes(data[32:64], "big") / 1e18
            lt = int.from_bytes(data[96:128], "big") / 10000.0
            hf_raw = int.from_bytes(data[160:192], "big")
            hf = hf_raw / 1e18 if hf_raw < 2**255 else float("inf")

            if debt_eth > 1e-10:
                results[addr] = {
                    "collateral_usd": col_eth * eth_price,
                    "debt_usd": debt_eth * eth_price,
                    "liq_threshold": lt,
                    "health_factor": hf,
                }

        batch_num = i // MULTICALL_BATCH + 1
        if batch_num % 20 == 0 or batch_num == total_batches:
            print(f"    Batch {batch_num}/{total_batches}: {len(results)} active borrowers")

    return results


def get_user_reserve_breakdown(w3: Web3, addresses: list[str], reserve_info: list[dict],
                                oracle_prices: dict[str, float]) -> dict[str, dict]:
    """Get per-asset collateral and debt for each user via multicall at historical block.
    
    Only queries reserves with non-zero oracle prices (material reserves).
    Processes in user-batches: for each batch of users, query all reserves at once.
    """
    mc_abi = [{"inputs": [{"name": "requireSuccess", "type": "bool"},
                           {"components": [{"name": "target", "type": "address"},
                                           {"name": "callData", "type": "bytes"}],
                            "name": "calls", "type": "tuple[]"}],
               "name": "tryAggregate",
               "outputs": [{"components": [{"name": "success", "type": "bool"},
                                            {"name": "returnData", "type": "bytes"}],
                             "name": "returnData", "type": "tuple[]"}],
               "stateMutability": "view", "type": "function"}]
    multicall = w3.eth.contract(address=Web3.to_checksum_address(MULTICALL3), abi=mc_abi)

    selector = bytes.fromhex("28dd2d01")  # getUserReserveData(address,address)
    pdp_cs = Web3.to_checksum_address(PROTOCOL_DATA_PROVIDER)

    # Filter to key reserves with prices
    active_reserves = [r for r in reserve_info
                       if oracle_prices.get(r["address"], 0) > 0
                       and r["symbol"] in KEY_RESERVES_2022]
    print(f"    Querying {len(active_reserves)} key reserves: {[r['symbol'] for r in active_reserves]}")

    # Pre-compute asset bytes
    for r in active_reserves:
        r["_asset_bytes"] = bytes(12) + bytes.fromhex(r["address"][2:])

    user_data = {addr: {
        "eth_col_usd": 0.0, "total_col_usd": 0.0,
        "eth_debt_usd": 0.0, "stable_debt_usd": 0.0, "other_debt_usd": 0.0,
        "largest": ("", 0.0),
    } for addr in addresses}

    # Process in user batches, all reserves per batch
    users_per_batch = max(1, RESERVE_BATCH // len(active_reserves))
    total_batches = (len(addresses) + users_per_batch - 1) // users_per_batch

    for i in range(0, len(addresses), users_per_batch):
        user_batch = addresses[i:i + users_per_batch]
        calls = []
        call_map = []  # (user_idx, reserve_idx)

        for u_idx, addr in enumerate(user_batch):
            user_bytes = bytes(12) + bytes.fromhex(addr[2:])
            for r_idx, res in enumerate(active_reserves):
                calls.append((pdp_cs, selector + res["_asset_bytes"] + user_bytes))
                call_map.append((u_idx, r_idx))

        for attempt in range(3):
            try:
                ret = multicall.functions.tryAggregate(False, calls).call(block_identifier=TARGET_BLOCK)
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise

        for (u_idx, r_idx), (ok, data) in zip(call_map, ret):
            if not ok or len(data) < 288:
                continue
            res = active_reserves[r_idx]
            symbol = res["symbol"]
            price = oracle_prices[res["address"]]
            decimals = res["decimals"]

            atoken_bal = int.from_bytes(data[0:32], "big") / (10 ** decimals)
            stable_debt = int.from_bytes(data[32:64], "big") / (10 ** decimals)
            var_debt = int.from_bytes(data[64:96], "big") / (10 ** decimals)
            col_enabled = int.from_bytes(data[256:288], "big") != 0

            addr = user_batch[u_idx]
            info = user_data[addr]

            if atoken_bal > 0 and col_enabled:
                col_val = atoken_bal * price
                info["total_col_usd"] += col_val
                if col_val > info["largest"][1]:
                    info["largest"] = (symbol, col_val)
                if symbol in ETH_CORRELATED_2022:
                    info["eth_col_usd"] += col_val

            total_debt_val = (stable_debt + var_debt) * price
            if total_debt_val > 0:
                if symbol in ETH_CORRELATED_2022:
                    info["eth_debt_usd"] += total_debt_val
                elif symbol in STABLECOINS_2022:
                    info["stable_debt_usd"] += total_debt_val
                else:
                    info["other_debt_usd"] += total_debt_val

        batch_num = i // users_per_batch + 1
        if batch_num % 50 == 0 or batch_num == total_batches:
            print(f"    Batch {batch_num}/{total_batches}")
        time.sleep(0.1)

    return user_data


def get_oracle_prices(w3: Web3, reserve_info: list[dict]) -> dict[str, float]:
    """Get Aave v2 oracle prices at historical block."""
    oracle_abi = [{"inputs": [{"type": "address[]"}], "name": "getAssetsPrices",
                   "outputs": [{"type": "uint256[]"}], "stateMutability": "view", "type": "function"}]
    oracle = w3.eth.contract(address=Web3.to_checksum_address(PRICE_ORACLE_V2), abi=oracle_abi)

    addrs = [Web3.to_checksum_address(r["address"]) for r in reserve_info]
    raw = oracle.functions.getAssetsPrices(addrs).call(block_identifier=TARGET_BLOCK)

    # v2 oracle returns prices in ETH (WAD, 18 decimals)
    # Need to convert to USD using ETH price
    eth_price = load_eth_price_at_date()
    prices = {}
    for r, p in zip(reserve_info, raw):
        price_eth = p / 1e18
        prices[r["address"]] = price_eth * eth_price
    return prices


# --- Main ---

if __name__ == "__main__":
    t0 = time.time()

    eth_price = load_eth_price_at_date()
    print(f"ETH price at June 10, 2022: ${eth_price:.2f}")

    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 60}))
    assert w3.is_connected()
    block = w3.eth.get_block(TARGET_BLOCK)
    print(f"Target block {TARGET_BLOCK}, timestamp {block.timestamp}")

    # Phase A: Reserve info
    print("\n--- Phase A: Reserve info at historical block ---")
    reserve_info = get_reserve_info(w3)
    print(f"  {len(reserve_info)} reserves")
    for r in reserve_info[:5]:
        print(f"    {r['symbol']:>10s}  dec={r['decimals']}")

    # Phase B: Oracle prices
    print("\n--- Phase B: Oracle prices ---")
    oracle_prices = get_oracle_prices(w3, reserve_info)
    for r in reserve_info:
        p = oracle_prices.get(r["address"], 0)
        if p > 0:
            print(f"    {r['symbol']:>10s}: ${p:>12,.2f}")

    # Phase C: Find all borrowers
    print("\n--- Phase C: Finding borrowers via debt token mints ---")
    borrowers = find_borrowers(reserve_info)
    print(f"  Found {len(borrowers)} unique borrower addresses")

    # Phase D: Get account data
    print("\n--- Phase D: getUserAccountData at block {TARGET_BLOCK} ---")
    addr_list = sorted(borrowers)
    account_data = batch_get_account_data(w3, addr_list)
    print(f"  {len(account_data)} active borrowers with debt > 0")

    # Phase E: Asset-level breakdown
    print("\n--- Phase E: Per-asset reserve breakdown ---")
    active_addrs = sorted(account_data.keys())
    user_breakdown = get_user_reserve_breakdown(w3, active_addrs, reserve_info, oracle_prices)

    # Phase F: Classify and compute
    print("\n--- Phase F: Classification ---")
    positions = []
    for addr, acct in account_data.items():
        bd = user_breakdown.get(addr, {
            "eth_col_usd": 0, "total_col_usd": 0, "eth_debt_usd": 0,
            "stable_debt_usd": 0, "other_debt_usd": 0, "largest": ("", 0),
        })

        total_debt = acct["debt_usd"]
        eth_debt_frac = bd["eth_debt_usd"] / total_debt if total_debt > 0 else 0

        if eth_debt_frac > PHANTOM_THRESHOLD:
            pos_type = "phantom"
        elif eth_debt_frac < REAL_THRESHOLD:
            pos_type = "real"
        else:
            pos_type = "mixed"

        eth_col = bd["eth_col_usd"]
        total_col = bd["total_col_usd"]
        eth_dominant = eth_col > 0.5 * total_col if total_col > 0 else False
        lt = acct["liq_threshold"]

        liq_price = None
        if eth_dominant and eth_col > 0 and lt > 0:
            non_eth_col = total_col - eth_col
            if pos_type == "real":
                remaining = total_debt - non_eth_col * lt
                if remaining > 0:
                    liq_price = eth_price * remaining / (eth_col * lt)
                else:
                    liq_price = 0.0
            elif pos_type == "mixed":
                fixed_debt = bd["stable_debt_usd"] + bd["other_debt_usd"]
                remaining = fixed_debt - non_eth_col * lt
                if remaining > 0:
                    liq_price = eth_price * remaining / (eth_col * lt)
                else:
                    liq_price = 0.0

        positions.append({
            "user": addr,
            "collateral_usd": acct["collateral_usd"],
            "eth_collateral_usd": eth_col,
            "debt_usd": total_debt,
            "health_factor": acct["health_factor"],
            "liq_price_usd": liq_price if liq_price is not None else "",
            "eth_dominant": eth_dominant,
            "largest_collateral_symbol": bd["largest"][0],
            "eth_debt_usd": bd["eth_debt_usd"],
            "stable_debt_usd": bd["stable_debt_usd"],
            "eth_debt_fraction": eth_debt_frac,
            "position_type": pos_type,
        })

    # Save CSV
    output_path = DATA_DIR / "positions_june2022.csv"
    fields = ["user", "collateral_usd", "eth_collateral_usd", "debt_usd",
              "health_factor", "liq_price_usd", "eth_dominant", "largest_collateral_symbol",
              "eth_debt_usd", "stable_debt_usd", "eth_debt_fraction", "position_type"]
    with open(output_path, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader()
        wr.writerows(positions)
    print(f"\n  Saved {len(positions)} positions to {output_path}")

    # --- Analysis ---
    print("\n" + "=" * 70)
    print(f"AAVE V2 SNAPSHOT — JUNE 10, 2022 (ETH ~${eth_price:.0f})")
    print("=" * 70)

    total_col = sum(p["collateral_usd"] for p in positions)
    total_debt = sum(p["debt_usd"] for p in positions)
    eth_dom = [p for p in positions if p["eth_dominant"]]

    print(f"\nTotal borrowers: {len(positions)}")
    print(f"Total collateral: ${total_col:,.0f}")
    print(f"Total debt: ${total_debt:,.0f}")
    print(f"ETH-dominant: {len(eth_dom)} positions, ${sum(p['debt_usd'] for p in eth_dom):,.0f} debt")

    # Decomposition
    real = [p for p in eth_dom if p["position_type"] == "real"]
    phantom = [p for p in eth_dom if p["position_type"] == "phantom"]
    mixed = [p for p in eth_dom if p["position_type"] == "mixed"]

    print(f"\nETH-dominant decomposition:")
    print(f"  Real:    {len(real):>6d}  debt ${sum(p['debt_usd'] for p in real):>15,.0f}")
    print(f"  Phantom: {len(phantom):>6d}  debt ${sum(p['debt_usd'] for p in phantom):>15,.0f}")
    print(f"  Mixed:   {len(mixed):>6d}  debt ${sum(p['debt_usd'] for p in mixed):>15,.0f}")

    # Real wall by band
    bands = [5, 10, 20, 30, 50]
    print(f"\nReal wall by proximity band (ETH=${eth_price:.0f}):")
    print(f"  {'Band':>6s} {'Positions':>10s} {'Debt':>16s}")
    for band in bands:
        in_band = [p for p in real if p["liq_price_usd"] != "" and
                   0 <= (eth_price - float(p["liq_price_usd"])) / eth_price <= band / 100]
        debt = sum(p["debt_usd"] for p in in_band)
        print(f"  {band:>5d}% {len(in_band):>10d} ${debt:>14,.0f}")

    # Top 10 real
    real_sorted = sorted([p for p in real if p["liq_price_usd"] != "" and float(p["liq_price_usd"]) < eth_price],
                         key=lambda p: p["debt_usd"], reverse=True)
    print(f"\nTop 10 REAL positions:")
    print(f"  {'User':>42s} {'Collateral':>14s} {'Debt':>14s} {'HF':>8s} {'LiqPrice':>10s} {'Coll':>8s}")
    for p in real_sorted[:10]:
        lp = f"${float(p['liq_price_usd']):,.0f}" if p["liq_price_usd"] != "" else "N/A"
        print(f"  {p['user']:>42s} ${p['collateral_usd']:>12,.0f} ${p['debt_usd']:>12,.0f} "
              f"{p['health_factor']:>8.3f} {lp:>10s} {p['largest_collateral_symbol']:>8s}")

    # Compare with current snapshot
    print(f"\n--- Comparison: June 2022 vs March 2026 ---")
    print(f"  {'Metric':>30s} {'Jun 2022':>16s} {'Mar 2026':>16s}")
    print(f"  {'ETH price':>30s} ${eth_price:>14,.0f} ${'2,202':>13s}")
    print(f"  {'Total borrowers':>30s} {len(positions):>16,d} {'29,311':>16s}")
    print(f"  {'Total collateral':>30s} ${total_col:>14,.0f} ${'22,562,723,239':>13s}")
    print(f"  {'Total debt':>30s} ${total_debt:>14,.0f} ${'13,175,482,196':>13s}")

    print(f"\nCompleted in {time.time() - t0:.1f}s")
