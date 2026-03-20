# Position Topology — Execution Plan

## Infrastructure

| Resource | Endpoint | Verified |
|---|---|---|
| Alchemy RPC | `alchemy.txt` | ✅ Block 24,693,844 |
| The Graph (Aave v3 Ethereum) | `graph.txt`, subgraph `Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g` | ✅ Position data + historical block queries |
| ETH price data | `../data/eth_price.csv` (daily + hourly, 2022-01 → 2026-03) | ✅ From flow phase |
| Episode dates | `../data/liquidation_events_combined.csv` (27 episodes) | ✅ From flow phase |

Key discovery: The Graph supports `block: {number: N}` parameter on all queries. We can get position snapshots at any historical block without an archive node. This collapses Phase 1 and Phase 2 into a single pipeline.

## Subgraph Schema (relevant fields)

**UserReserve**: `user.id`, `currentATokenBalance`, `currentTotalDebt`, `currentVariableDebt`, `usageAsCollateralEnabledOnUser`, `reserve.symbol`, `reserve.decimals`, `reserve.reserveLiquidationThreshold`, `reserve.price.priceInEth`, `reserve.baseLTVasCollateral`, `reserve.underlyingAsset`

**Reserve**: `symbol`, `decimals`, `reserveLiquidationThreshold`, `baseLTVasCollateral`, `price.priceInEth`, `liquidityIndex`, `variableBorrowIndex`

Pagination: max 1000 per query, use `id_gt` cursor. ~1000+ active borrowers currently.

## Liquidation Price Math

For a single-collateral, single-debt position:

```
Health Factor = (collateral_USD * liquidation_threshold) / debt_USD

HF < 1 → liquidatable

Liquidation price of ETH = (debt_USD * current_ETH_price) / (collateral_ETH * liquidation_threshold * current_ETH_price)

Simplified for ETH-collateral, stablecoin-debt:
  liq_price = debt_USD / (collateral_ETH * liquidation_threshold)
```

Multi-collateral positions: sum weighted collateral across all reserves, sum all debt. Compute aggregate HF. Liquidation triggers when aggregate HF < 1, but the ETH liquidation price depends on how much of the collateral is ETH-correlated.

Simplification for v1: focus on positions where ETH (or WETH/wstETH/stETH) is the dominant collateral asset. These are the positions whose liquidation prices move with ETH price. Stablecoin-collateral positions don't create ETH liquidation walls.

## Execution

### Step 1: Current Snapshot (`snapshot.py`)
Pull all active Aave v3 borrowers at current block. For each:
- Fetch all userReserves with debt > 0
- Fetch all userReserves with collateral > 0 and usageAsCollateralEnabled
- Compute liquidation price using reserve parameters and oracle prices
- Filter to ETH-correlated collateral positions

Output: `../data/positions_current.csv` — `user, collateral_symbol, collateral_usd, debt_usd, health_factor, liq_price_usd, protocol`

Validation: compare total liquidatable value and distribution against DefiLlama's stale snapshot ($2.16B total, $53.52M within -20%).

Estimated queries: ~10 pages × 1000 users = ~10 queries for users, + ~10 for reserves/prices. Well within free tier.

### Step 2: Density Map (`density.py`)
From snapshot CSV, compute the liquidation density map:
- Bucket liquidation prices into $50 bins
- For each bin: count of positions, total collateral USD, largest single position
- Identify walls (bins where single position > $50M or total > $200M)
- Compute proximity metrics: distance from current price to nearest wall, total liquidatable within 5%/10%/20%

Output: `../data/density_current.csv` + visualization data. This is the "liquidation heatmap."

### Step 3: Historical Snapshots (`historical.py`)
For each of the 27 episode start dates from `liquidation_events_combined.csv`:
1. Convert date → Ethereum block number (Alchemy `eth_getBlockByNumber` or Etherscan API)
2. Query Aave v3 subgraph at that block: `users(block: {number: N})`
3. Compute liquidation density map at that block
4. Record: wall proximity, total liquidatable within 5%/10%/20%, largest wall size + distance

Output: `../data/positions_historical.csv` — one row per episode with topology metrics at onset.

Query budget: 27 episodes × ~15 queries each = ~400 queries. Well within 100K/month free tier.

### Step 4: Backtest (`backtest.py`)
Merge historical topology metrics with episode outcomes (escalated vs absorbed, from flow phase data):
- Test: does wall proximity at episode onset predict escalation?
- Binary classification: near wall (within 10%) → predict escalation. Far wall → predict absorption.
- Measure: accuracy, precision, recall vs flow-phase baseline (32% FP rate)
- Test wall size threshold: does $100M+ wall within 10% predict differently than $50M?
- Test single-whale vs distributed wall: one position > 50% of wall vs many small positions

Output: `../data/backtest_results.csv` + `findings.md`

### Step 5: Wall Dynamics (if Step 4 validates)
For 3-5 episodes where we have clear wall proximity:
- Take daily snapshots during the episode (days 1-7)
- Track: did the wall move? Did whales top up collateral? Did partial liquidations shrink it?
- Quantify wall stability over the episode window

This answers open question #1 from the thesis.

## Query Patterns

```graphql
# All borrowers (paginated)
{
  users(first: 1000, where: {borrowedReservesCount_gt: 0, id_gt: $cursor}, orderBy: id) {
    id
    borrowedReservesCount
  }
}

# Full position data for a batch of users
{
  userReserves(first: 1000, where: {user_in: [$addresses], currentTotalDebt_gt: "0"}) {
    user { id }
    currentATokenBalance
    currentTotalDebt
    usageAsCollateralEnabledOnUser
    reserve {
      symbol
      decimals
      underlyingAsset
      reserveLiquidationThreshold
      baseLTVasCollateral
      price { priceInEth }
    }
  }
}

# Historical (add block parameter)
{
  userReserves(first: 1000, where: {...}, block: {number: 18000000}) { ... }
}
```

## Risks

1. **Subgraph balance staleness.** `currentATokenBalance` and `currentTotalDebt` reflect values at last indexing, not query time. Interest accrual creates drift. For positions held for months, this could be 1-5% off. Acceptable for wall detection (we care about $50M+ clusters, not exact amounts).

2. **Multi-collateral complexity.** Users with ETH + WBTC + stETH as collateral have a blended liquidation price. First pass: treat each collateral asset independently. Refinement: compute weighted liquidation price per user.

3. **E-mode positions.** Aave v3 E-mode allows higher LTV for correlated assets (e.g., ETH/stETH). These positions have different liquidation thresholds than standard mode. Must check E-mode category per user.

4. **Oracle price divergence.** Aave uses Chainlink oracles which can deviate from market price during volatility. Liquidation prices should be computed against Aave's oracle price, not market price.

5. **Protocol coverage gap.** Starting with Aave v3 only (~80% of lending). Compound v3 and Maker/Spark add the remaining 20%. Can extend in Step 3 if Aave-only results are promising but noisy.

## Success Criteria

- Step 1 produces a snapshot that roughly matches DefiLlama ($2B+ total, identifiable walls)
- Step 4 shows wall proximity at episode onset has higher predictive power than any flow-phase signal (>70% accuracy on escalation prediction, vs 50-76% flow-phase range)
- Or: Step 4 shows no relationship, in which case the thesis is wrong and we document why

## Scope Control

Start with Aave v3 Ethereum only. Do not add Compound/Maker/multi-chain until Step 4 results justify it. Each additional protocol is a separate engineering effort that should be motivated by a specific gap in the Aave-only results.
