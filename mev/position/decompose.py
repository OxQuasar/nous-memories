"""
Decompose Aave v3 positions by debt type: real vs phantom liquidation walls.

Reads existing positions_current.csv (on-chain HF/threshold), re-fetches
subgraph userReserves for debt breakdown, classifies positions, and
recomputes liquidation prices accounting for ETH-denominated debt cancellation.

Real wall: stablecoin debt + ETH collateral → ETH price drop triggers liquidation
Phantom wall: ETH debt + ETH collateral → both sides drop, no ETH-price liquidation
"""

import csv
import sys
import time
from pathlib import Path

import requests
from web3 import Web3

print = lambda *args, **kwargs: (sys.stdout.write(" ".join(str(a) for a in args) + kwargs.get("end", "\n")), sys.stdout.flush())

# --- Constants ---

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

API_KEY = (SCRIPT_DIR / "graph.txt").read_text().strip()
SUBGRAPH_ID = "Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g"
GRAPH_URL = f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/{SUBGRAPH_ID}"

RPC_URL = (SCRIPT_DIR / "alchemy.txt").read_text().strip()
AAVE_ADDRESSES_PROVIDER = "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e"

ETH_CORRELATED = {"WETH", "stETH", "wstETH", "cbETH", "rETH", "weETH", "osETH", "ETHx", "ezETH", "tETH", "rsETH"}
STABLECOINS = {"USDC", "USDT", "DAI", "FRAX", "GHO", "sDAI", "LUSD", "PYUSD", "crvUSD", "USDe", "sUSDe", "USDS",
               "eUSDe", "RLUSD", "USDG", "USDtb", "mUSD", "EURC", "syrupUSDT"}

# Debt type thresholds
PHANTOM_THRESHOLD = 0.8  # >80% ETH debt = phantom
REAL_THRESHOLD = 0.2     # <20% ETH debt = real

PAGE_SIZE = 1000
USER_BATCH_SIZE = 100
QUERY_DELAY = 0.5
RETRY_DELAY = 2.0

# --- Helpers ---

def graph_query(query: str, retries: int = 3) -> dict:
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
                time.sleep(RETRY_DELAY)
            else:
                raise


def fetch_user_reserves(addresses: list[str]) -> list[dict]:
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


def load_oracle_prices(w3: Web3, reserve_list: list[dict]) -> dict[str, float]:
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


def load_eth_price() -> float:
    csv_path = SCRIPT_DIR.parent / "data" / "eth_price_1h.csv"
    with open(csv_path) as f:
        lines = f.readlines()
    return float(lines[-1].strip().split(",")[2])


def load_positions() -> list[dict]:
    """Load existing positions CSV."""
    positions = {}
    with open(DATA_DIR / "positions_current.csv") as f:
        for row in csv.DictReader(f):
            row["collateral_usd"] = float(row["collateral_usd"])
            row["eth_collateral_usd"] = float(row["eth_collateral_usd"])
            row["debt_usd"] = float(row["debt_usd"])
            row["health_factor"] = float(row["health_factor"])
            row["eth_dominant"] = row["eth_dominant"] == "True"
            positions[row["user"]] = row
    return positions


# --- Main ---

if __name__ == "__main__":
    t0 = time.time()

    eth_price = load_eth_price()
    print(f"ETH reference price: ${eth_price:.2f}")

    # Load existing positions (on-chain HF/collateral/debt already computed)
    print("\n--- Loading existing positions ---")
    positions = load_positions()
    print(f"  {len(positions)} positions loaded")

    # Get oracle prices for debt valuation
    print("\n--- Loading oracle prices ---")
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 60}))
    q = '{ reserves(first: 100, orderBy: symbol) { symbol decimals underlyingAsset } }'
    reserves_data = graph_query(q)["reserves"]
    prices = load_oracle_prices(w3, reserves_data)
    print(f"  {sum(1 for p in prices.values() if p > 0)}/{len(prices)} with non-zero price")

    # Fetch subgraph userReserves for debt breakdown
    print("\n--- Fetching user reserves (subgraph) ---")
    all_addrs = list(positions.keys())
    all_user_reserves = []
    total_batches = (len(all_addrs) + USER_BATCH_SIZE - 1) // USER_BATCH_SIZE
    for i in range(0, len(all_addrs), USER_BATCH_SIZE):
        batch = all_addrs[i:i + USER_BATCH_SIZE]
        all_user_reserves.extend(fetch_user_reserves(batch))
        batch_num = i // USER_BATCH_SIZE + 1
        if batch_num % 20 == 0 or batch_num == total_batches:
            print(f"  Batch {batch_num}/{total_batches}: {len(all_user_reserves)} reserves")
        time.sleep(QUERY_DELAY)
    print(f"  Total: {len(all_user_reserves)} reserves fetched")

    # Compute per-user debt and collateral breakdown
    print("\n--- Computing debt/collateral breakdown ---")
    user_breakdown: dict[str, dict] = {}
    for ur in all_user_reserves:
        uid = ur["user"]["id"]
        if uid not in user_breakdown:
            user_breakdown[uid] = {
                "eth_debt_usd": 0.0, "stable_debt_usd": 0.0, "other_debt_usd": 0.0,
                "eth_col_usd": 0.0, "total_col_usd": 0.0, "largest": ("", 0.0),
            }

        res = ur["reserve"]
        symbol = res["symbol"]
        decimals = int(res["decimals"])
        underlying = res["underlyingAsset"]
        price_usd = prices.get(underlying, 0.0)

        total_debt = int(ur["currentTotalDebt"]) / (10 ** decimals)
        atoken_bal = int(ur["currentATokenBalance"]) / (10 ** decimals)
        collateral_enabled = ur["usageAsCollateralEnabledOnUser"]

        info = user_breakdown[uid]

        # Debt side
        if total_debt > 0:
            debt_val = total_debt * price_usd
            if symbol in ETH_CORRELATED:
                info["eth_debt_usd"] += debt_val
            elif symbol in STABLECOINS:
                info["stable_debt_usd"] += debt_val
            else:
                info["other_debt_usd"] += debt_val

        # Collateral side (refresh from subgraph for consistency)
        if atoken_bal > 0 and collateral_enabled:
            col_val = atoken_bal * price_usd
            info["total_col_usd"] += col_val
            if col_val > info["largest"][1]:
                info["largest"] = (symbol, col_val)
            if symbol in ETH_CORRELATED:
                info["eth_col_usd"] += col_val

    # Merge and classify
    print("--- Classifying positions ---")
    enriched = []
    for user, pos in positions.items():
        bd = user_breakdown.get(user, {
            "eth_debt_usd": 0, "stable_debt_usd": 0, "other_debt_usd": 0,
            "eth_col_usd": 0, "total_col_usd": 0, "largest": ("", 0),
        })

        total_debt = pos["debt_usd"]
        eth_debt = bd["eth_debt_usd"]
        stable_debt = bd["stable_debt_usd"]
        other_debt = bd["other_debt_usd"]
        eth_debt_frac = eth_debt / total_debt if total_debt > 0 else 0.0

        # Position type
        if eth_debt_frac > PHANTOM_THRESHOLD:
            pos_type = "phantom"
        elif eth_debt_frac < REAL_THRESHOLD:
            pos_type = "real"
        else:
            pos_type = "mixed"

        eth_col_usd = bd["eth_col_usd"]
        total_col = bd["total_col_usd"]
        eth_dominant = eth_col_usd > 0.5 * total_col if total_col > 0 else False

        # Derive liq_threshold from on-chain HF
        # HF = (collateral * weighted_threshold) / debt → lt = HF * debt / collateral
        lt = (pos["health_factor"] * total_debt / pos["collateral_usd"]
              if pos["collateral_usd"] > 0 else 0.0)

        # Recompute liquidation price based on position type
        liq_price = None
        if eth_dominant and eth_col_usd > 0 and lt > 0:
            non_eth_col = total_col - eth_col_usd
            if pos_type == "real":
                # All debt is fixed USD — original formula
                remaining = total_debt - non_eth_col * lt
                if remaining > 0:
                    liq_price = eth_price * remaining / (eth_col_usd * lt)
                else:
                    liq_price = 0.0
            elif pos_type == "mixed":
                # Only stablecoin + other debt is fixed; ETH debt cancels
                fixed_debt = stable_debt + other_debt
                remaining = fixed_debt - non_eth_col * lt
                if remaining > 0:
                    liq_price = eth_price * remaining / (eth_col_usd * lt)
                else:
                    liq_price = 0.0
            # phantom: no meaningful ETH/USD liq price

        enriched.append({
            "user": user,
            "collateral_usd": pos["collateral_usd"],
            "eth_collateral_usd": eth_col_usd,
            "debt_usd": total_debt,
            "health_factor": pos["health_factor"],
            "liq_price_usd": liq_price if liq_price is not None else "",
            "eth_dominant": eth_dominant,
            "largest_collateral_symbol": bd["largest"][0],
            "eth_debt_usd": eth_debt,
            "stable_debt_usd": stable_debt,
            "eth_debt_fraction": eth_debt_frac,
            "position_type": pos_type,
        })

    # Save enriched CSV
    output_path = DATA_DIR / "positions_decomposed.csv"
    fields = ["user", "collateral_usd", "eth_collateral_usd", "debt_usd",
              "health_factor", "liq_price_usd", "eth_dominant", "largest_collateral_symbol",
              "eth_debt_usd", "stable_debt_usd", "eth_debt_fraction", "position_type"]
    with open(output_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(enriched)
    print(f"\n  Saved {len(enriched)} positions to {output_path}")

    # --- Analysis ---
    print("\n" + "=" * 70)
    print("DECOMPOSED WALL ANALYSIS")
    print("=" * 70)

    eth_dom = [p for p in enriched if p["eth_dominant"]]
    real = [p for p in eth_dom if p["position_type"] == "real"]
    phantom = [p for p in eth_dom if p["position_type"] == "phantom"]
    mixed = [p for p in eth_dom if p["position_type"] == "mixed"]

    print(f"\nETH-dominant positions: {len(eth_dom)}")
    print(f"  Real (stablecoin debt):     {len(real):>6d}  debt ${sum(p['debt_usd'] for p in real):>15,.0f}")
    print(f"  Phantom (ETH debt):         {len(phantom):>6d}  debt ${sum(p['debt_usd'] for p in phantom):>15,.0f}")
    print(f"  Mixed:                      {len(mixed):>6d}  debt ${sum(p['debt_usd'] for p in mixed):>15,.0f}")

    # Wall composition by proximity band
    bands = [5, 10, 20, 30, 50]
    print(f"\nWall composition by proximity band:")
    print(f"  {'Band':>6s} {'Real Pos':>10s} {'Real Debt':>16s} {'Phantom Pos':>12s} {'Phantom Debt':>16s} {'Mixed Pos':>10s} {'Mixed Debt':>16s} {'Real %':>8s}")

    for band in bands:
        real_in = [p for p in real if p["liq_price_usd"] != "" and
                   0 <= (eth_price - float(p["liq_price_usd"])) / eth_price <= band / 100]
        phantom_in = [p for p in phantom]  # phantom has no liq_price, use old data to estimate
        mixed_in = [p for p in mixed if p["liq_price_usd"] != "" and
                    0 <= (eth_price - float(p["liq_price_usd"])) / eth_price <= band / 100]

        # For phantom positions, estimate proximity using original (naive) liq price from CSV
        phantom_in_band = []
        for p in phantom:
            # Back-compute the "naive" liq price (as if all debt were fixed USD)
            if p["eth_collateral_usd"] > 0:
                lt_est = p["health_factor"] * p["debt_usd"] / p["collateral_usd"] if p["collateral_usd"] > 0 else 0
                if lt_est > 0:
                    non_eth = p["collateral_usd"] - p["eth_collateral_usd"]  # approx
                    rem = p["debt_usd"] - non_eth * lt_est
                    if rem > 0:
                        naive_liq = eth_price * rem / (p["eth_collateral_usd"] * lt_est)
                        pct_below = (eth_price - naive_liq) / eth_price
                        if 0 <= pct_below <= band / 100:
                            phantom_in_band.append(p)

        r_debt = sum(p["debt_usd"] for p in real_in)
        p_debt = sum(p["debt_usd"] for p in phantom_in_band)
        m_debt = sum(p["debt_usd"] for p in mixed_in)
        total = r_debt + p_debt + m_debt
        real_pct = r_debt / total * 100 if total > 0 else 0

        print(f"  {band:>5d}% {len(real_in):>10d} ${r_debt:>14,.0f} {len(phantom_in_band):>12d} ${p_debt:>14,.0f} {len(mixed_in):>10d} ${m_debt:>14,.0f} {real_pct:>7.1f}%")

    # Top 10 REAL positions
    real_with_liq = [p for p in real if p["liq_price_usd"] != "" and float(p["liq_price_usd"]) < eth_price]
    real_with_liq.sort(key=lambda p: p["debt_usd"], reverse=True)
    print(f"\nTop 10 REAL positions (stablecoin debt, ETH collateral):")
    print(f"  {'User':>42s} {'Collateral':>14s} {'Debt':>14s} {'HF':>8s} {'LiqPrice':>10s} {'Type':>8s} {'Coll':>8s}")
    for p in real_with_liq[:10]:
        lp = f"${float(p['liq_price_usd']):,.0f}"
        print(f"  {p['user']:>42s} ${p['collateral_usd']:>12,.0f} ${p['debt_usd']:>12,.0f} "
              f"{p['health_factor']:>8.3f} {lp:>10s} {p['position_type']:>8s} {p['largest_collateral_symbol']:>8s}")

    # Top 10 PHANTOM positions
    print(f"\nTop 10 PHANTOM positions (ETH debt + ETH collateral):")
    phantom_sorted = sorted(phantom, key=lambda p: p["debt_usd"], reverse=True)
    print(f"  {'User':>42s} {'Collateral':>14s} {'Debt':>14s} {'HF':>8s} {'ETH Debt%':>10s} {'Coll':>8s}")
    for p in phantom_sorted[:10]:
        print(f"  {p['user']:>42s} ${p['collateral_usd']:>12,.0f} ${p['debt_usd']:>12,.0f} "
              f"{p['health_factor']:>8.3f} {p['eth_debt_fraction']:>9.1%} {p['largest_collateral_symbol']:>8s}")

    print(f"\nCompleted in {time.time() - t0:.1f}s")
