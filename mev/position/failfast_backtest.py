"""
Historical position snapshots for fail-fast backtest.

3 episodes + comparison with existing June 2022 data:
  - 2022-11-08 FTX crash (V2, moderate)
  - 2024-04-12 Iran tensions (V3, absorbed)
  - 2024-08-04 Yen carry trade (V3, escalating)
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
DATA_DIR.mkdir(exist_ok=True)

RPC_URL = (SCRIPT_DIR / "alchemy.txt").read_text().strip()
API_KEY = (SCRIPT_DIR / "graph.txt").read_text().strip()

MULTICALL3 = "0xcA11bde05977b3631167028862bE2a173976CA11"

# V2 contracts
V2_LENDING_POOL = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
V2_DATA_PROVIDER = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"
V2_ADDR_PROVIDER = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"
V2_DEPLOY_BLOCK = 11362579

# V3 contracts
V3_ADDR_PROVIDER = "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e"
V3_SUBGRAPH_ID = "Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g"
V3_GRAPH_URL = f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/{V3_SUBGRAPH_ID}"

# Asset classification
ETH_CORRELATED_V2 = {"WETH", "stETH", "wstETH"}
ETH_CORRELATED_V3 = {"WETH", "stETH", "wstETH", "cbETH", "rETH", "weETH", "osETH", "ETHx", "ezETH", "rsETH"}
STABLECOINS_V2 = {"USDC", "USDT", "DAI", "FRAX", "LUSD", "BUSD", "GUSD", "sUSD", "TUSD", "USDP", "FEI", "UST"}
STABLECOINS_V3 = {"USDC", "USDT", "DAI", "FRAX", "GHO", "sDAI", "LUSD", "PYUSD", "crvUSD", "USDe", "sUSDe", "USDS"}

KEY_RESERVES_V2 = {"WETH", "stETH", "wstETH", "USDC", "USDT", "DAI", "FRAX", "LUSD", "BUSD", "GUSD", "sUSD",
                    "TUSD", "USDP", "FEI", "UST", "WBTC", "LINK", "AAVE", "UNI", "CRV", "SNX", "MKR", "ENS", "BAL"}

PHANTOM_THRESHOLD = 0.8
REAL_THRESHOLD = 0.2
MULTICALL_BATCH = 100
RESERVE_BATCH = 500

# --- Episodes ---
EPISODES = {
    "nov2022": {"block": 15921589, "eth_price": 1568.93, "version": "v2",
                "label": "FTX crash", "type": "moderate", "csv": "positions_nov2022.csv"},
    "apr2024": {"block": 19635810, "eth_price": 3510.35, "version": "v3",
                "label": "Iran tensions", "type": "absorbed", "csv": "positions_apr2024.csv"},
    "aug2024": {"block": 20451460, "eth_price": 2903.17, "version": "v3",
                "label": "Yen carry trade", "type": "escalating", "csv": "positions_aug2024.csv"},
}


# --- Shared helpers ---

def try_multicall(w3, calls, block):
    mc_abi = [{"inputs": [{"name": "requireSuccess", "type": "bool"},
                           {"components": [{"name": "target", "type": "address"},
                                           {"name": "callData", "type": "bytes"}],
                            "name": "calls", "type": "tuple[]"}],
               "name": "tryAggregate",
               "outputs": [{"components": [{"name": "success", "type": "bool"},
                                            {"name": "returnData", "type": "bytes"}],
                             "name": "returnData", "type": "tuple[]"}],
               "stateMutability": "view", "type": "function"}]
    mc = w3.eth.contract(address=Web3.to_checksum_address(MULTICALL3), abi=mc_abi)
    for attempt in range(3):
        try:
            return mc.functions.tryAggregate(False, calls).call(block_identifier=block)
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                raise


def classify_position(eth_debt_frac):
    if eth_debt_frac > PHANTOM_THRESHOLD:
        return "phantom"
    elif eth_debt_frac < REAL_THRESHOLD:
        return "real"
    return "mixed"


def compute_liq_price(eth_price, total_col, eth_col, debt, eth_debt, stable_debt, lt, pos_type):
    """Compute liquidation price for ETH-dominant positions."""
    if eth_col <= 0 or lt <= 0:
        return None
    non_eth_col = total_col - eth_col
    if pos_type == "real":
        remaining = debt - non_eth_col * lt
    else:
        fixed_debt = stable_debt
        remaining = fixed_debt - non_eth_col * lt
    if remaining <= 0:
        return 0.0
    return eth_price * remaining / (eth_col * lt)


# ==================================================
# V2 Pipeline
# ==================================================

def run_v2_snapshot(w3, ep):
    block = ep["block"]
    eth_price = ep["eth_price"]
    eth_corr = ETH_CORRELATED_V2
    stables = STABLECOINS_V2

    # Phase A: Reserve info
    print("  Phase A: Reserve info")
    pool_abi = [{"inputs": [], "name": "getReservesList", "outputs": [{"type": "address[]"}],
                 "stateMutability": "view", "type": "function"}]
    pool = w3.eth.contract(address=Web3.to_checksum_address(V2_LENDING_POOL), abi=pool_abi)
    reserves = pool.functions.getReservesList().call(block_identifier=block)

    pdp_abi = [{"inputs": [{"type": "address"}], "name": "getReserveTokensAddresses",
                "outputs": [{"type": "address"}, {"type": "address"}, {"type": "address"}],
                "stateMutability": "view", "type": "function"}]
    pdp = w3.eth.contract(address=Web3.to_checksum_address(V2_DATA_PROVIDER), abi=pdp_abi)
    sym_abi = [{"inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"},
               {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "stateMutability": "view", "type": "function"}]

    reserve_info = []
    debt_tokens = []
    for addr in reserves:
        cs = Web3.to_checksum_address(addr)
        aToken, stableDebt, varDebt = pdp.functions.getReserveTokensAddresses(cs).call(block_identifier=block)
        token = w3.eth.contract(address=cs, abi=sym_abi)
        try:
            symbol = token.functions.symbol().call(block_identifier=block)
            decimals = token.functions.decimals().call(block_identifier=block)
        except Exception:
            symbol, decimals = "UNKNOWN", 18
        reserve_info.append({"address": addr.lower(), "symbol": symbol, "decimals": decimals})
        debt_tokens.append(Web3.to_checksum_address(varDebt))
        debt_tokens.append(Web3.to_checksum_address(stableDebt))
    print(f"    {len(reserve_info)} reserves, {len(debt_tokens)} debt tokens")

    # Phase B: Oracle prices (v2 returns prices in ETH)
    print("  Phase B: Oracle prices")
    prov_abi = [{"inputs": [], "name": "getPriceOracle", "outputs": [{"type": "address"}],
                 "stateMutability": "view", "type": "function"}]
    prov = w3.eth.contract(address=Web3.to_checksum_address(V2_ADDR_PROVIDER), abi=prov_abi)
    oracle_addr = prov.functions.getPriceOracle().call(block_identifier=block)
    oracle_abi = [{"inputs": [{"type": "address[]"}], "name": "getAssetsPrices",
                   "outputs": [{"type": "uint256[]"}], "stateMutability": "view", "type": "function"}]
    oracle = w3.eth.contract(address=Web3.to_checksum_address(oracle_addr), abi=oracle_abi)
    addrs = [Web3.to_checksum_address(r["address"]) for r in reserve_info]
    raw = oracle.functions.getAssetsPrices(addrs).call(block_identifier=block)
    oracle_prices = {r["address"]: (p / 1e18) * eth_price for r, p in zip(reserve_info, raw)}

    # Phase C: Find borrowers
    print("  Phase C: Finding borrowers")
    borrowers = set()
    page_key = None
    while True:
        params = {"fromBlock": hex(V2_DEPLOY_BLOCK), "toBlock": hex(block),
                  "fromAddress": "0x0000000000000000000000000000000000000000",
                  "contractAddresses": debt_tokens, "category": ["erc20"],
                  "maxCount": "0x3e8", "withMetadata": False, "excludeZeroValue": True}
        if page_key:
            params["pageKey"] = page_key
        r = requests.post(RPC_URL, json={"id": 1, "jsonrpc": "2.0",
                          "method": "alchemy_getAssetTransfers", "params": [params]}, timeout=60)
        data = r.json()
        if "error" in data:
            print(f"    Error: {data['error']}")
            break
        for t in data["result"]["transfers"]:
            borrowers.add(t["to"].lower())
        page_key = data["result"].get("pageKey")
        if not page_key:
            break
        time.sleep(0.2)
    print(f"    {len(borrowers)} unique borrowers")

    # Phase D: getUserAccountData
    print("  Phase D: getUserAccountData")
    selector = bytes.fromhex("bf92857c")
    pool_cs = Web3.to_checksum_address(V2_LENDING_POOL)
    addr_list = sorted(borrowers)
    account_data = {}
    for i in range(0, len(addr_list), MULTICALL_BATCH):
        batch = addr_list[i:i + MULTICALL_BATCH]
        calls = [(pool_cs, selector + bytes(12) + bytes.fromhex(a[2:])) for a in batch]
        ret = try_multicall(w3, calls, block)
        for addr, (ok, data) in zip(batch, ret):
            if not ok or len(data) < 192:
                continue
            col_eth = int.from_bytes(data[0:32], "big") / 1e18
            debt_eth = int.from_bytes(data[32:64], "big") / 1e18
            lt = int.from_bytes(data[96:128], "big") / 10000.0
            hf_raw = int.from_bytes(data[160:192], "big")
            hf = hf_raw / 1e18 if hf_raw < 2**255 else float("inf")
            if debt_eth > 1e-10:
                account_data[addr] = {"collateral_usd": col_eth * eth_price, "debt_usd": debt_eth * eth_price,
                                       "liq_threshold": lt, "health_factor": hf}
        if (i // MULTICALL_BATCH + 1) % 50 == 0:
            print(f"    {len(account_data)} active")
    print(f"    {len(account_data)} active borrowers")

    # Phase E: Reserve breakdown
    print("  Phase E: Reserve breakdown")
    active_addrs = sorted(account_data.keys())
    active_reserves = [r for r in reserve_info if oracle_prices.get(r["address"], 0) > 0
                       and r["symbol"] in KEY_RESERVES_V2]
    print(f"    {len(active_reserves)} key reserves for {len(active_addrs)} users")

    pdp_sel = bytes.fromhex("28dd2d01")
    pdp_cs = Web3.to_checksum_address(V2_DATA_PROVIDER)
    for r in active_reserves:
        r["_asset_bytes"] = bytes(12) + bytes.fromhex(r["address"][2:])

    user_bd = {a: {"eth_col": 0.0, "total_col": 0.0, "eth_debt": 0.0, "stable_debt": 0.0,
                    "other_debt": 0.0, "largest": ("", 0.0)} for a in active_addrs}

    users_per_batch = max(1, RESERVE_BATCH // len(active_reserves))
    total_batches = (len(active_addrs) + users_per_batch - 1) // users_per_batch
    for i in range(0, len(active_addrs), users_per_batch):
        ub = active_addrs[i:i + users_per_batch]
        calls, cmap = [], []
        for ui, addr in enumerate(ub):
            ub_bytes = bytes(12) + bytes.fromhex(addr[2:])
            for ri, res in enumerate(active_reserves):
                calls.append((pdp_cs, pdp_sel + res["_asset_bytes"] + ub_bytes))
                cmap.append((ui, ri))
        ret = try_multicall(w3, calls, block)
        for (ui, ri), (ok, d) in zip(cmap, ret):
            if not ok or len(d) < 288:
                continue
            res = active_reserves[ri]
            sym, price, dec = res["symbol"], oracle_prices[res["address"]], res["decimals"]
            abal = int.from_bytes(d[0:32], "big") / (10 ** dec)
            sdebt = int.from_bytes(d[32:64], "big") / (10 ** dec)
            vdebt = int.from_bytes(d[64:96], "big") / (10 ** dec)
            col_en = int.from_bytes(d[256:288], "big") != 0
            info = user_bd[ub[ui]]
            if abal > 0 and col_en:
                cv = abal * price
                info["total_col"] += cv
                if cv > info["largest"][1]:
                    info["largest"] = (sym, cv)
                if sym in eth_corr:
                    info["eth_col"] += cv
            td = (sdebt + vdebt) * price
            if td > 0:
                if sym in eth_corr:
                    info["eth_debt"] += td
                elif sym in stables:
                    info["stable_debt"] += td
                else:
                    info["other_debt"] += td
        if (i // users_per_batch + 1) % 100 == 0 or i // users_per_batch + 1 == total_batches:
            print(f"    Batch {i // users_per_batch + 1}/{total_batches}")
        time.sleep(0.05)

    # Build positions
    return build_positions(account_data, user_bd, eth_price, eth_corr)


# ==================================================
# V3 Pipeline
# ==================================================

def graph_query(query, retries=2):
    for attempt in range(retries + 1):
        try:
            r = requests.post(V3_GRAPH_URL, json={"query": query}, timeout=60)
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                raise RuntimeError(f"GraphQL: {data['errors']}")
            return data["data"]
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
            else:
                raise


def run_v3_snapshot(w3, ep):
    block = ep["block"]
    eth_price = ep["eth_price"]
    eth_corr = ETH_CORRELATED_V3
    stables = STABLECOINS_V3

    # Phase A: Borrowers via subgraph
    print("  Phase A: Fetching borrowers (subgraph)")
    borrowers = []
    cursor = ""
    while True:
        where = f'borrowedReservesCount_gt: 0, id_gt: "{cursor}"' if cursor else "borrowedReservesCount_gt: 0"
        q = f'{{ users(first: 1000, where: {{{where}}}, orderBy: id, block: {{number: {block}}}) {{ id }} }}'
        users = graph_query(q)["users"]
        borrowers.extend(u["id"] for u in users)
        if len(users) < 1000:
            break
        cursor = users[-1]["id"]
        time.sleep(0.3)
    print(f"    {len(borrowers)} borrowers")

    # Phase B: User reserves via subgraph (for collateral/debt breakdown)
    print("  Phase B: User reserves (subgraph)")
    all_urs = []
    batch_size = 100
    for i in range(0, len(borrowers), batch_size):
        batch = borrowers[i:i + batch_size]
        addr_str = ", ".join(f'"{a}"' for a in batch)
        cursor_ur = ""
        while True:
            cf = f', id_gt: "{cursor_ur}"' if cursor_ur else ""
            q = f"""{{ userReserves(first: 1000, where: {{user_in: [{addr_str}]{cf}}}, orderBy: id,
                       block: {{number: {block}}}) {{
                user {{ id }}
                currentATokenBalance currentTotalDebt currentVariableDebt
                usageAsCollateralEnabledOnUser
                reserve {{ symbol decimals underlyingAsset reserveLiquidationThreshold }}
            }} }}"""
            urs = graph_query(q)["userReserves"]
            all_urs.extend(urs)
            if len(urs) < 1000:
                break
            cursor_ur = urs[-1]["id"]
            time.sleep(0.3)
        if (i // batch_size + 1) % 20 == 0:
            print(f"    Batch {i // batch_size + 1}/{(len(borrowers) + batch_size - 1) // batch_size}: {len(all_urs)} reserves")
        time.sleep(0.3)
    print(f"    {len(all_urs)} user reserves")

    # Phase C: Oracle prices (v3 returns USD, 8 decimals)
    print("  Phase C: Oracle prices")
    prov_abi = [{"inputs": [], "name": "getPriceOracle", "outputs": [{"type": "address"}],
                 "stateMutability": "view", "type": "function"},
                {"inputs": [], "name": "getPool", "outputs": [{"type": "address"}],
                 "stateMutability": "view", "type": "function"}]
    prov = w3.eth.contract(address=Web3.to_checksum_address(V3_ADDR_PROVIDER), abi=prov_abi)
    oracle_addr = prov.functions.getPriceOracle().call(block_identifier=block)
    pool_addr = prov.functions.getPool().call(block_identifier=block)

    # Collect unique underlying addresses
    underlying_set = set()
    for ur in all_urs:
        underlying_set.add(ur["reserve"]["underlyingAsset"])
    underlying_list = sorted(underlying_set)

    oracle_abi = [{"inputs": [{"type": "address[]"}], "name": "getAssetsPrices",
                   "outputs": [{"type": "uint256[]"}], "stateMutability": "view", "type": "function"}]
    oracle = w3.eth.contract(address=Web3.to_checksum_address(oracle_addr), abi=oracle_abi)
    cs_list = [Web3.to_checksum_address(a) for a in underlying_list]
    raw_prices = oracle.functions.getAssetsPrices(cs_list).call(block_identifier=block)
    oracle_prices = {a: p / 1e8 for a, p in zip(underlying_list, raw_prices)}

    # Phase D: getUserAccountData via multicall
    print("  Phase D: getUserAccountData")
    selector = bytes.fromhex("bf92857c")
    pool_cs = Web3.to_checksum_address(pool_addr)
    account_data = {}
    for i in range(0, len(borrowers), MULTICALL_BATCH):
        batch = borrowers[i:i + MULTICALL_BATCH]
        calls = [(pool_cs, selector + bytes(12) + bytes.fromhex(a[2:])) for a in batch]
        ret = try_multicall(w3, calls, block)
        for addr, (ok, d) in zip(batch, ret):
            if not ok or len(d) < 192:
                continue
            col = int.from_bytes(d[0:32], "big") / 1e8
            debt = int.from_bytes(d[32:64], "big") / 1e8
            lt = int.from_bytes(d[96:128], "big") / 10000.0
            hf_raw = int.from_bytes(d[160:192], "big")
            hf = hf_raw / 1e18 if hf_raw < 2**255 else float("inf")
            if debt > 0:
                account_data[addr] = {"collateral_usd": col, "debt_usd": debt,
                                       "liq_threshold": lt, "health_factor": hf}
        if (i // MULTICALL_BATCH + 1) % 50 == 0:
            print(f"    {len(account_data)} active")
    print(f"    {len(account_data)} active borrowers")

    # Build user breakdown from subgraph data
    user_bd = {}
    for ur in all_urs:
        uid = ur["user"]["id"]
        if uid not in account_data:
            continue
        if uid not in user_bd:
            user_bd[uid] = {"eth_col": 0.0, "total_col": 0.0, "eth_debt": 0.0, "stable_debt": 0.0,
                             "other_debt": 0.0, "largest": ("", 0.0)}
        res = ur["reserve"]
        sym = res["symbol"]
        dec = int(res["decimals"])
        underlying = res["underlyingAsset"]
        price = oracle_prices.get(underlying, 0.0)
        if price == 0:
            continue

        abal = int(ur["currentATokenBalance"]) / (10 ** dec)
        tdebt = int(ur["currentTotalDebt"]) / (10 ** dec)
        col_en = ur["usageAsCollateralEnabledOnUser"]

        info = user_bd[uid]
        if abal > 0 and col_en:
            cv = abal * price
            info["total_col"] += cv
            if cv > info["largest"][1]:
                info["largest"] = (sym, cv)
            if sym in eth_corr:
                info["eth_col"] += cv

        if tdebt > 0:
            dv = tdebt * price
            if sym in eth_corr:
                info["eth_debt"] += dv
            elif sym in stables:
                info["stable_debt"] += dv
            else:
                info["other_debt"] += dv

    # Ensure all active borrowers have breakdown entries
    for addr in account_data:
        if addr not in user_bd:
            user_bd[addr] = {"eth_col": 0.0, "total_col": 0.0, "eth_debt": 0.0,
                              "stable_debt": 0.0, "other_debt": 0.0, "largest": ("", 0.0)}

    return build_positions(account_data, user_bd, eth_price, eth_corr)


# ==================================================
# Position builder (shared)
# ==================================================

def build_positions(account_data, user_bd, eth_price, eth_corr):
    positions = []
    for addr, acct in account_data.items():
        bd = user_bd.get(addr, {"eth_col": 0, "total_col": 0, "eth_debt": 0,
                                 "stable_debt": 0, "other_debt": 0, "largest": ("", 0)})
        debt = acct["debt_usd"]
        eth_debt_frac = bd["eth_debt"] / debt if debt > 0 else 0
        pos_type = classify_position(eth_debt_frac)
        eth_col = bd["eth_col"]
        total_col = bd["total_col"]
        eth_dom = eth_col > 0.5 * total_col if total_col > 0 else False
        lt = acct["liq_threshold"]

        liq_price = None
        if eth_dom and eth_col > 0 and lt > 0 and pos_type != "phantom":
            liq_price = compute_liq_price(eth_price, total_col, eth_col, debt,
                                           bd["eth_debt"], bd["stable_debt"], lt, pos_type)

        positions.append({
            "user": addr, "collateral_usd": acct["collateral_usd"],
            "eth_collateral_usd": eth_col, "debt_usd": debt,
            "health_factor": acct["health_factor"],
            "liq_price_usd": liq_price if liq_price is not None else "",
            "eth_dominant": eth_dom, "largest_collateral_symbol": bd["largest"][0],
            "eth_debt_usd": bd["eth_debt"], "stable_debt_usd": bd["stable_debt"],
            "eth_debt_fraction": eth_debt_frac, "position_type": pos_type,
        })
    return positions


# ==================================================
# Analysis
# ==================================================

def analyze(positions, eth_price, label):
    """Compute metrics for one episode snapshot."""
    total_col = sum(p["collateral_usd"] for p in positions)
    total_debt = sum(p["debt_usd"] for p in positions)
    eth_dom = [p for p in positions if p["eth_dominant"]]
    real = [p for p in eth_dom if p["position_type"] == "real"]
    phantom = [p for p in eth_dom if p["position_type"] == "phantom"]

    # Real positions with valid liq prices below current
    real_liq = [p for p in real if p["liq_price_usd"] != "" and 0 < float(p["liq_price_usd"]) < eth_price]
    real_liq.sort(key=lambda p: float(p["liq_price_usd"]), reverse=True)

    # Cliff: largest real position
    cliff = max(real_liq, key=lambda p: p["debt_usd"]) if real_liq else None
    cliff_size = cliff["debt_usd"] if cliff else 0
    cliff_liq = float(cliff["liq_price_usd"]) if cliff else 0
    cliff_dist = (eth_price - cliff_liq) / eth_price * 100 if cliff else 0

    # Proximity bands
    bands = {}
    for band in [5, 10, 20, 30, 50]:
        threshold = eth_price * (1 - band / 100)
        in_band = [p for p in real_liq if float(p["liq_price_usd"]) >= threshold]
        bands[band] = sum(p["debt_usd"] for p in in_band)

    # Runway: cumulative real debt between price and cliff
    runway = 0.0
    if cliff:
        runway = sum(p["debt_usd"] for p in real_liq if float(p["liq_price_usd"]) >= cliff_liq)

    # Gradient: real debt per 1% of price in zone between price and cliff
    pct_to_cliff = cliff_dist if cliff_dist > 0 else 1
    gradient = runway / pct_to_cliff if pct_to_cliff > 0 else 0

    # Top 5 real
    top5 = sorted(real_liq, key=lambda p: p["debt_usd"], reverse=True)[:5]

    metrics = {
        "label": label, "eth_price": eth_price,
        "total_borrowers": len(positions), "total_col": total_col, "total_debt": total_debt,
        "eth_dom_count": len(eth_dom), "real_count": len(real), "phantom_count": len(phantom),
        "real_debt": sum(p["debt_usd"] for p in real),
        "phantom_debt": sum(p["debt_usd"] for p in phantom),
        "cliff_size": cliff_size, "cliff_liq": cliff_liq, "cliff_dist": cliff_dist,
        "runway": runway, "gradient": gradient, "bands": bands, "top5": top5,
    }

    print(f"\n  --- {label} (ETH=${eth_price:,.0f}) ---")
    print(f"  Borrowers: {len(positions):,d}  Col: ${total_col:,.0f}  Debt: ${total_debt:,.0f}")
    print(f"  ETH-dom: {len(eth_dom):,d}  Real: {len(real):,d} (${sum(p['debt_usd'] for p in real):,.0f})")
    print(f"  Phantom: {len(phantom):,d} (${sum(p['debt_usd'] for p in phantom):,.0f})")
    print(f"  Cliff: ${cliff_size:,.0f} at ${cliff_liq:,.0f} ({cliff_dist:.0f}% below)")
    print(f"  Runway: ${runway:,.0f}  Gradient: ${gradient:,.0f}/% ")
    for b in [5, 10, 20, 30, 50]:
        print(f"    Real {b:>2d}%: ${bands[b]:>14,.0f}")

    return metrics


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":
    t0 = time.time()

    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 60}))
    assert w3.is_connected()

    fields = ["user", "collateral_usd", "eth_collateral_usd", "debt_usd",
              "health_factor", "liq_price_usd", "eth_dominant", "largest_collateral_symbol",
              "eth_debt_usd", "stable_debt_usd", "eth_debt_fraction", "position_type"]

    all_metrics = []

    for name, ep in EPISODES.items():
        print(f"\n{'='*70}")
        print(f"EPISODE: {ep['label']} ({name}) — block {ep['block']} ETH=${ep['eth_price']:,.2f}")
        print(f"{'='*70}")

        t1 = time.time()
        if ep["version"] == "v2":
            positions = run_v2_snapshot(w3, ep)
        else:
            positions = run_v3_snapshot(w3, ep)

        # Save CSV
        csv_path = DATA_DIR / ep["csv"]
        with open(csv_path, "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=fields)
            wr.writeheader()
            wr.writerows(positions)
        print(f"  Saved {len(positions)} to {csv_path}")

        metrics = analyze(positions, ep["eth_price"], ep["label"])
        metrics["type"] = ep["type"]
        all_metrics.append(metrics)
        print(f"  Completed in {time.time() - t1:.0f}s")

    # Load June 2022 data for comparison
    print(f"\n{'='*70}")
    print("Loading June 2022 reference data")
    print(f"{'='*70}")
    june_path = DATA_DIR / "positions_june2022.csv"
    if june_path.exists():
        with open(june_path) as f:
            june_pos = []
            for row in csv.DictReader(f):
                june_pos.append({
                    "user": row["user"],
                    "collateral_usd": float(row["collateral_usd"]),
                    "eth_collateral_usd": float(row["eth_collateral_usd"]),
                    "debt_usd": float(row["debt_usd"]),
                    "health_factor": float(row["health_factor"]),
                    "liq_price_usd": row["liq_price_usd"] if row["liq_price_usd"] else "",
                    "eth_dominant": row["eth_dominant"] == "True",
                    "largest_collateral_symbol": row["largest_collateral_symbol"],
                    "eth_debt_usd": float(row.get("eth_debt_usd", 0)),
                    "stable_debt_usd": float(row.get("stable_debt_usd", 0)),
                    "eth_debt_fraction": float(row.get("eth_debt_fraction", 0)),
                    "position_type": row.get("position_type", "real"),
                })
        june_metrics = analyze(june_pos, 1788.42, "stETH depeg")
        june_metrics["type"] = "escalating"
        all_metrics.insert(0, june_metrics)

    # Print comparison table
    print(f"\n{'='*70}")
    print("COMPARISON TABLE")
    print(f"{'='*70}")
    hdr = f"{'Episode':<25s} {'Type':<12s} {'ETH':>8s} {'Cliff':>10s} {'Cliff%':>7s} {'Runway':>12s} {'R5%':>10s} {'R10%':>10s} {'R20%':>10s} {'R30%':>10s}"
    print(hdr)
    print("-" * len(hdr))
    for m in all_metrics:
        print(f"{m['label']:<25s} {m['type']:<12s} ${m['eth_price']:>6,.0f} ${m['cliff_size']/1e6:>7.0f}M {m['cliff_dist']:>5.0f}% ${m['runway']/1e6:>9.0f}M ${m['bands'][5]/1e6:>7.1f}M ${m['bands'][10]/1e6:>7.1f}M ${m['bands'][20]/1e6:>7.1f}M ${m['bands'][30]/1e6:>7.1f}M")

    print(f"\nTotal runtime: {time.time() - t0:.0f}s")
