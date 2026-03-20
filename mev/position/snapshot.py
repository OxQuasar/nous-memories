"""
Aave v3 Ethereum: Pull all borrower positions, compute health factors & liquidation prices.

Data sources:
  - The Graph (Aave v3 subgraph): user positions & collateral breakdown
  - Aave v3 Pool getUserAccountData (on-chain via multicall): accurate HF & threshold
  - Aave v3 Oracle (on-chain): asset prices
  - Local CSV: ETH/USD reference price
"""

import csv
import sys
import time
from pathlib import Path

import requests
from web3 import Web3

# Force unbuffered output
print = lambda *args, **kwargs: (sys.stdout.write(" ".join(str(a) for a in args) + kwargs.get("end", "\n")), sys.stdout.flush())

# --- Constants ---

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

API_KEY = (SCRIPT_DIR / "graph.txt").read_text().strip()
SUBGRAPH_ID = "Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g"
GRAPH_URL = f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/{SUBGRAPH_ID}"

RPC_URL = (SCRIPT_DIR / "alchemy.txt").read_text().strip()
AAVE_ADDRESSES_PROVIDER = "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e"
MULTICALL3 = "0xcA11bde05977b3631167028862bE2a173976CA11"

ETH_CORRELATED = {"WETH", "stETH", "wstETH", "cbETH", "rETH", "weETH", "osETH", "ETHx", "ezETH", "tETH", "rsETH"}

PAGE_SIZE = 1000
USER_BATCH_SIZE = 100  # for subgraph queries
MULTICALL_BATCH = 100  # for on-chain multicall
QUERY_DELAY = 0.5
RETRY_DELAY = 2.0

# --- Graph helpers ---

def graph_query(query: str, retries: int = 1) -> dict:
    for attempt in range(retries + 1):
        try:
            r = requests.post(GRAPH_URL, json={"query": query}, timeout=60)
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                raise RuntimeError(f"GraphQL errors: {data['errors']}")
            return data["data"]
        except Exception as e:
            if attempt < retries:
                print(f"  Query failed ({e}), retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                raise


def fetch_all_borrowers() -> list[str]:
    """Paginate through all borrower addresses."""
    borrowers = []
    cursor = ""
    page = 0
    while True:
        where = f'borrowedReservesCount_gt: 0, id_gt: "{cursor}"' if cursor else "borrowedReservesCount_gt: 0"
        q = f'{{ users(first: {PAGE_SIZE}, where: {{{where}}}, orderBy: id) {{ id }} }}'
        users = graph_query(q)["users"]
        borrowers.extend(u["id"] for u in users)
        page += 1
        if page % 5 == 0:
            print(f"  Fetched {len(borrowers)} borrowers so far...")
        if len(users) < PAGE_SIZE:
            break
        cursor = users[-1]["id"]
        time.sleep(QUERY_DELAY)
    return borrowers


def fetch_user_reserves(addresses: list[str]) -> list[dict]:
    """Fetch userReserves for a batch of addresses."""
    all_reserves = []
    addr_str = ", ".join(f'"{a}"' for a in addresses)
    cursor = ""
    while True:
        cursor_filter = f', id_gt: "{cursor}"' if cursor else ""
        q = f"""{{
  userReserves(first: {PAGE_SIZE}, where: {{user_in: [{addr_str}]{cursor_filter}}}, orderBy: id) {{
    id
    user {{ id }}
    currentATokenBalance
    currentTotalDebt
    usageAsCollateralEnabledOnUser
    reserve {{ symbol decimals underlyingAsset }}
  }}
}}"""
        reserves = graph_query(q)["userReserves"]
        all_reserves.extend(reserves)
        if len(reserves) < PAGE_SIZE:
            break
        cursor = reserves[-1]["id"]
        time.sleep(QUERY_DELAY)
    return all_reserves


# --- On-chain ---

def get_pool_address(w3: Web3) -> str:
    abi = [{"inputs": [], "name": "getPool", "outputs": [{"type": "address"}],
            "stateMutability": "view", "type": "function"}]
    provider = w3.eth.contract(address=Web3.to_checksum_address(AAVE_ADDRESSES_PROVIDER), abi=abi)
    return provider.functions.getPool().call()


def load_oracle_prices(w3: Web3, reserve_list: list[dict]) -> dict[str, float]:
    """Query Aave v3 oracle for all asset prices. Returns {underlying_address: price_usd}."""
    abi_provider = [{"inputs": [], "name": "getPriceOracle", "outputs": [{"type": "address"}],
                     "stateMutability": "view", "type": "function"}]
    provider = w3.eth.contract(address=Web3.to_checksum_address(AAVE_ADDRESSES_PROVIDER), abi=abi_provider)
    oracle_addr = provider.functions.getPriceOracle().call()

    abi_oracle = [{"inputs": [{"type": "address[]"}], "name": "getAssetsPrices",
                   "outputs": [{"type": "uint256[]"}], "stateMutability": "view", "type": "function"}]
    oracle = w3.eth.contract(address=oracle_addr, abi=abi_oracle)

    addr_map = {}
    for r in reserve_list:
        addr = r["underlyingAsset"]
        addr_map[Web3.to_checksum_address(addr)] = addr

    checksum_addrs = list(addr_map.keys())
    raw_prices = oracle.functions.getAssetsPrices(checksum_addrs).call()
    return {addr_map[cs]: raw / 1e8 for cs, raw in zip(checksum_addrs, raw_prices)}


def batch_get_account_data(w3: Web3, pool_addr: str, addresses: list[str]) -> dict[str, dict]:
    """Use Multicall3 to batch getUserAccountData for all addresses.
    Returns {addr: {collateral_usd, debt_usd, liq_threshold, health_factor}}."""

    # ABI encode getUserAccountData(address) call
    pool_abi = [{"inputs": [{"type": "address"}], "name": "getUserAccountData",
                 "outputs": [{"type": "uint256"}, {"type": "uint256"}, {"type": "uint256"},
                            {"type": "uint256"}, {"type": "uint256"}, {"type": "uint256"}],
                 "stateMutability": "view", "type": "function"}]
    pool = w3.eth.contract(address=Web3.to_checksum_address(pool_addr), abi=pool_abi)

    multicall_abi = [{"inputs": [{"components": [{"name": "target", "type": "address"},
                                                  {"name": "callData", "type": "bytes"}],
                                   "name": "calls", "type": "tuple[]"}],
                      "name": "aggregate",
                      "outputs": [{"name": "blockNumber", "type": "uint256"},
                                  {"name": "returnData", "type": "bytes[]"}],
                      "stateMutability": "view", "type": "function"}]
    multicall = w3.eth.contract(address=Web3.to_checksum_address(MULTICALL3), abi=multicall_abi)

    # Pre-encode all calldata (same function selector, just different address arg)
    selector = bytes.fromhex("bf92857c")  # getUserAccountData(address) selector
    pool_cs = Web3.to_checksum_address(pool_addr)

    results = {}
    total_batches = (len(addresses) + MULTICALL_BATCH - 1) // MULTICALL_BATCH

    for i in range(0, len(addresses), MULTICALL_BATCH):
        batch = addresses[i:i + MULTICALL_BATCH]
        calls = []
        for addr in batch:
            # ABI encode: selector + address padded to 32 bytes
            calldata = selector + bytes(12) + bytes.fromhex(addr[2:] if addr.startswith("0x") else addr)
            calls.append((pool_cs, calldata))

        for attempt in range(3):
            try:
                _, return_data = multicall.functions.aggregate(calls).call()
                break
            except Exception as e:
                if attempt < 2:
                    print(f"  Multicall batch failed ({e}), retrying...")
                    time.sleep(2)
                else:
                    raise

        for addr, data in zip(batch, return_data):
            decoded = w3.codec.decode(
                ["uint256", "uint256", "uint256", "uint256", "uint256", "uint256"],
                data
            )
            collateral = decoded[0] / 1e8
            debt = decoded[1] / 1e8
            threshold = decoded[3] / 10000.0
            hf = decoded[5] / 1e18 if decoded[5] < 2**255 else float("inf")

            results[addr] = {
                "collateral_usd": collateral,
                "debt_usd": debt,
                "liq_threshold": threshold,
                "health_factor": hf,
            }

        batch_num = i // MULTICALL_BATCH + 1
        if batch_num % 10 == 0 or batch_num == total_batches:
            print(f"  Multicall batch {batch_num}/{total_batches}")

    return results


def load_eth_price() -> float:
    csv_path = SCRIPT_DIR.parent / "data" / "eth_price_1h.csv"
    with open(csv_path) as f:
        lines = f.readlines()
    return float(lines[-1].strip().split(",")[2])


# --- Position computation ---

def compute_positions(
    account_data: dict[str, dict],
    user_reserves_raw: list[dict],
    prices: dict[str, float],
    eth_price: float,
) -> list[dict]:
    """Combine on-chain account data with subgraph collateral breakdown."""
    # Group reserves by user for collateral breakdown
    user_collateral: dict[str, dict] = {}  # user -> {eth_col_usd, total_col_usd, largest_symbol}
    for ur in user_reserves_raw:
        uid = ur["user"]["id"]
        if uid not in user_collateral:
            user_collateral[uid] = {"eth_col_usd": 0.0, "total_col_usd": 0.0,
                                     "largest": ("", 0.0)}

        res = ur["reserve"]
        symbol = res["symbol"]
        decimals = int(res["decimals"])
        underlying = res["underlyingAsset"]
        price_usd = prices.get(underlying, 0.0)

        atoken_bal = int(ur["currentATokenBalance"]) / (10 ** decimals)
        collateral_enabled = ur["usageAsCollateralEnabledOnUser"]

        if atoken_bal > 0 and collateral_enabled:
            col_val = atoken_bal * price_usd
            info = user_collateral[uid]
            info["total_col_usd"] += col_val
            if col_val > info["largest"][1]:
                info["largest"] = (symbol, col_val)
            if symbol in ETH_CORRELATED:
                info["eth_col_usd"] += col_val

    positions = []
    for user, acct in account_data.items():
        if acct["debt_usd"] == 0:
            continue

        col_info = user_collateral.get(user, {"eth_col_usd": 0, "total_col_usd": 0, "largest": ("", 0)})
        eth_col_usd = col_info["eth_col_usd"]
        total_col = col_info["total_col_usd"]
        eth_dominant = eth_col_usd > 0.5 * total_col if total_col > 0 else False

        # Liquidation price for ETH-dominant positions
        # On-chain gives us the effective weighted threshold already
        # HF = weighted_threshold_sum / debt, so weighted_threshold_sum = HF * debt
        # Split into: eth_threshold_contribution + non_eth_threshold_contribution
        # Assume threshold applies uniformly (acct["liq_threshold"] is weighted average)
        # eth_threshold_contribution ≈ eth_col_usd * liq_threshold
        # non_eth_threshold_contribution ≈ (total_col - eth_col_usd) * liq_threshold
        # At liquidation (ETH drops by factor k):
        # non_eth_threshold_contrib + eth_col_usd * k * liq_threshold = debt
        # k = (debt - non_eth_col * liq_threshold) / (eth_col_usd * liq_threshold)
        liq_price_usd = None
        if eth_dominant and eth_col_usd > 0:
            lt = acct["liq_threshold"]
            non_eth_col = total_col - eth_col_usd
            remaining_debt = acct["debt_usd"] - non_eth_col * lt
            if remaining_debt > 0 and lt > 0:
                k = remaining_debt / (eth_col_usd * lt)
                liq_price_usd = eth_price * k
            else:
                liq_price_usd = 0.0

        positions.append({
            "user": user,
            "collateral_usd": acct["collateral_usd"],
            "eth_collateral_usd": eth_col_usd,
            "debt_usd": acct["debt_usd"],
            "health_factor": acct["health_factor"],
            "liq_price_usd": liq_price_usd if liq_price_usd is not None else "",
            "eth_dominant": eth_dominant,
            "largest_collateral_symbol": col_info["largest"][0],
        })

    return positions


# --- Main ---

if __name__ == "__main__":
    t0 = time.time()

    eth_price_ref = load_eth_price()
    print(f"ETH reference price: ${eth_price_ref:.2f}")

    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 60}))
    assert w3.is_connected(), "RPC connection failed"
    print(f"Connected to Ethereum, block {w3.eth.block_number}")

    pool_addr = get_pool_address(w3)
    print(f"Aave v3 Pool: {pool_addr}")

    # Phase A: Reserves & oracle prices
    print("\n--- Phase A: Loading reserves & oracle prices ---")
    q = '{ reserves(first: 100, orderBy: symbol) { symbol decimals underlyingAsset } }'
    reserves_data = graph_query(q)["reserves"]
    print(f"  {len(reserves_data)} reserves found")

    prices = load_oracle_prices(w3, reserves_data)
    print(f"  {sum(1 for p in prices.values() if p > 0)}/{len(prices)} with non-zero oracle price")

    # Phase B: Borrowers
    print("\n--- Phase B: Fetching borrowers ---")
    borrowers = fetch_all_borrowers()
    print(f"  Total borrowers: {len(borrowers)}")

    # Phase C: On-chain account data via multicall
    print("\n--- Phase C: On-chain getUserAccountData (multicall) ---")
    account_data = batch_get_account_data(w3, pool_addr, borrowers)
    print(f"  Got account data for {len(account_data)} users")

    # Phase D: Subgraph user reserves (for collateral breakdown)
    print("\n--- Phase D: Fetching user reserves (subgraph) ---")
    all_user_reserves = []
    total_batches = (len(borrowers) + USER_BATCH_SIZE - 1) // USER_BATCH_SIZE
    for i in range(0, len(borrowers), USER_BATCH_SIZE):
        batch = borrowers[i:i + USER_BATCH_SIZE]
        all_user_reserves.extend(fetch_user_reserves(batch))
        batch_num = i // USER_BATCH_SIZE + 1
        if batch_num % 10 == 0 or batch_num == total_batches:
            print(f"  Batch {batch_num}/{total_batches}: {len(all_user_reserves)} reserves so far")
        time.sleep(QUERY_DELAY)
    print(f"  Total user reserves fetched: {len(all_user_reserves)}")

    # Phase E: Compute positions
    print("\n--- Phase E: Computing positions ---")
    positions = compute_positions(account_data, all_user_reserves, prices, eth_price_ref)

    # Save CSV
    output_path = DATA_DIR / "positions_current.csv"
    fields = ["user", "collateral_usd", "eth_collateral_usd", "debt_usd",
              "health_factor", "liq_price_usd", "eth_dominant", "largest_collateral_symbol"]
    with open(output_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(positions)
    print(f"\n  Saved {len(positions)} positions to {output_path}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total_collateral = sum(p["collateral_usd"] for p in positions)
    total_debt = sum(p["debt_usd"] for p in positions)
    eth_dominant_pos = [p for p in positions if p["eth_dominant"]]
    eth_dom_collateral = sum(p["collateral_usd"] for p in eth_dominant_pos)
    eth_dom_debt = sum(p["debt_usd"] for p in eth_dominant_pos)

    print(f"Total borrowers found:       {len(borrowers)}")
    print(f"Positions with debt:         {len(positions)}")
    print(f"Total collateral USD:        ${total_collateral:,.0f}")
    print(f"Total debt USD:              ${total_debt:,.0f}")
    print(f"ETH-dominant positions:      {len(eth_dominant_pos)} "
          f"(${eth_dom_collateral:,.0f} collateral, ${eth_dom_debt:,.0f} debt)")

    # HF distribution
    hf_ranges = [(1.0, "< 1.0"), (1.1, "< 1.1"), (1.25, "< 1.25"), (1.5, "< 1.5"), (2.0, "< 2.0")]
    print(f"\nHealth factor distribution:")
    for thresh, label in hf_ranges:
        count = sum(1 for p in positions if p["health_factor"] < thresh)
        debt = sum(p["debt_usd"] for p in positions if p["health_factor"] < thresh)
        print(f"  HF {label:>6s}:  {count:>5d} positions  ${debt:>15,.0f} debt")

    # Liquidation price distribution
    eth_liq = [p for p in eth_dominant_pos if p["liq_price_usd"] != "" and p["liq_price_usd"] is not None]
    above_current = 0
    above_current_debt = 0.0
    within = {5: [0, 0.0], 10: [0, 0.0], 20: [0, 0.0], 30: [0, 0.0], 50: [0, 0.0]}
    for p in eth_liq:
        lp = float(p["liq_price_usd"])
        if lp >= eth_price_ref:
            above_current += 1
            above_current_debt += p["debt_usd"]
            continue
        pct_below = (eth_price_ref - lp) / eth_price_ref * 100
        for threshold in within:
            if pct_below <= threshold:
                within[threshold][0] += 1
                within[threshold][1] += p["debt_usd"]

    print(f"\nETH reference price: ${eth_price_ref:.2f}")
    print(f"Already liquidatable (liq > current): {above_current} positions, ${above_current_debt:,.0f} debt")
    for t in sorted(within):
        c, v = within[t]
        print(f"  Liq price within {t:>2d}% below:  {c:>5d} positions  ${v:>15,.0f} debt")

    # Top 10
    top10 = sorted(positions, key=lambda p: p["collateral_usd"], reverse=True)[:10]
    print(f"\nTop 10 positions by collateral:")
    print(f"  {'User':>42s} {'Collateral':>14s} {'Debt':>14s} {'HF':>8s} {'LiqPrice':>10s} {'Coll':>8s}")
    for p in top10:
        lp = f"${p['liq_price_usd']:,.0f}" if p['liq_price_usd'] != "" else "N/A"
        print(f"  {p['user']:>42s} ${p['collateral_usd']:>12,.0f} ${p['debt_usd']:>12,.0f} "
              f"{p['health_factor']:>8.3f} {lp:>10s} {p['largest_collateral_symbol']:>8s}")

    # Compare
    print(f"\n--- Comparison with DefiLlama liquidation_bins ---")
    print(f"DefiLlama total liquidatable:  $2,160,362,375 (all protocols, stale, ETH~$3782)")
    print(f"Our Aave v3 total debt:        ${total_debt:,.0f}")
    print(f"Our Aave v3 total collateral:  ${total_collateral:,.0f}")

    print(f"\nCompleted in {time.time() - t0:.1f}s")
