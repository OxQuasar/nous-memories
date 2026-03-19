# DeFi Signals Exploration Plan

## Goal

Test whether on-chain DeFi metrics produce actionable leading signals for ETH price direction. Fast, broad exploration — kill or pursue each signal within a day.

## Baseline

**ETH daily price**: 1,297 days from 2022-01-01 to 2026-03-18. Saved at `signals/data/eth_price.csv`. Pulled from DefiLlama coins API (no auth). Covers full cycle: 2022 crash, bear bottom, recovery, recent pullback.

Script: `signals/eth_price.py`

## Method

Each realm = one script = one question. Pull data, compute correlation with ETH price, check for lead/lag. A signal "works" if it moves before price with enough consistency and lead time to be actionable. Concurrent correlation is interesting but not tradeable. Lagging is useless.

Tools: Python, pandas, numpy. DefiLlama API as primary source (free, no auth). Dune/subgraphs for on-chain granularity when needed.

## Realms

### 1. Stablecoin Supply (first)
- **Data**: DAI + GHO + USDS total supply over time
- **Source**: DefiLlama stablecoins API (`/stablecoins`, `/stablecoincharts`)
- **Question**: Does stablecoin mint rate predict ETH direction? Supply expansion = leverage expansion.
- **Why first**: Cleanest mechanical relationship to leverage. Ready-made time series from DefiLlama. Lowest friction.

### 2. Lending Utilization
- **Data**: Aave/Morpho aggregate borrowing utilization
- **Source**: DefiLlama protocol TVL (`/protocol/{name}`) or yields API
- **Question**: Does utilization rate lead, lag, or coincide with price moves?
- **Why second**: Direct leverage gauge. Available from DefiLlama.

### 3. stETH/ETH Spread
- **Data**: Historical stETH/ETH price ratio
- **Source**: DefiLlama or CoinGecko price for stETH
- **Question**: Does spread widening predict broader selloffs? What's the lead time?
- **Why third**: Simple price ratio, easy pull. Known stress indicator.

### 4. TVL Token-Terms vs USD-Terms Divergence
- **Data**: DeFi TVL in ETH vs TVL in USD for major protocols
- **Source**: DefiLlama TVL API
- **Question**: Does real-inflow-adjusted TVL give a cleaner signal than raw TVL?
- **Why fourth**: Derived metric from existing data. Separates real deposit flows from price effects.

### 5. Bridge Flows
- **Data**: Net flows between chains
- **Source**: DefiLlama bridges API (`/bridges`)
- **Question**: Does capital rotation signal regime changes?
- **Why fifth**: Available but noisier. Explore after cleaner signals.

### 6. Liquidation Walls
- **Data**: Current Aave position distribution, liquidation price thresholds
- **Source**: Aave subgraph or Dune queries
- **Question**: Where are clustered liquidation thresholds? How much forced selling sits at each level?
- **Why last**: Hardest data access. Most value if earlier signals validate the thesis.

## Output Per Realm

- Correlation coefficient (Pearson) between signal and ETH price
- Cross-correlation at various lags (signal leads price by N days)
- Rate-of-change correlation (signal delta vs price delta)
- Plain text verdict: lead, lag, concurrent, or noise

## Status

| Realm | Status | Verdict |
|-------|--------|---------|
| Baseline (ETH price) | ✅ Done | 1,297 daily prices |
| 1. Stablecoin supply | Next | — |
| 2. Lending utilization | — | — |
| 3. stETH/ETH spread | — | — |
| 4. TVL divergence | — | — |
| 5. Bridge flows | — | — |
| 6. Liquidation walls | — | — |
