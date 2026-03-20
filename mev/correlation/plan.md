# Correlation-Cascade Investigation — Plan

## Premise

The position topology investigation (6 iterations, `../position/`) found that DeFi's near-price liquidation wall is >99.99% phantom — ETH-loop strategies (wstETH collateral / WETH debt) whose health factor depends on the LST/ETH exchange rate, not ETH/USD price. $5.6B of phantom positions sit at HF 1.03-1.05.

The market hasn't become less fragile. It shifted what it's fragile to: from ETH/USD price-cascade (2022) to staking-derivative depeg-cascade (2026). This investigation characterizes that vulnerability.

## Question

**What depeg magnitude in LST/ETH triggers cascade activation for the $5.6B phantom wall?**

Sub-questions:
1. How much LST selling breaks each token's peg? (DEX liquidity depth)
2. How far have LST pegs actually moved during historical stress? (depeg magnitude)
3. Do Chainlink oracles update fast enough to trigger liquidations during rapid depeg? (oracle lag)
4. Does a depeg in one LST spread to others? (contagion across tiers)

## Conjectured LST Fragility Hierarchy

| Tier | Tokens | DEX Liquidity | Depeg Threshold | Phantom Exposure | Cascade Role |
|------|--------|---------------|-----------------|------------------|--------------|
| 3 | osETH, tETH, ETHx | Thin | Low (1-2%?) | ~$300M | Early warning — cracks first |
| 2 | weETH | Medium | Medium (3-5%?) | ~$1.5B | Amplifier — large exposure, moderate resilience |
| 1 | wstETH | Deep (Curve/Balancer) | High (5-7%?) | ~$1.4B | Systemic — only cracks in severe stress |

Hypothesis: cascade propagates upward through tiers. Tier 3 cracks → selling pressure → Tier 2 weakens → if severe enough → Tier 1 breaks → full phantom wall activation.

## Execution

### Step 1: DEX Liquidity Depth per LST
Map the on-chain liquidity available for each LST token. For each: how much selling (in USD) produces a 1%, 2%, 5% depeg from fair value?

**Data sources:**
- DEX pool reserves: Curve, Balancer, Uniswap v3 (concentrated liquidity ranges)
- DefiLlama liquidity endpoint (if available for LST tokens)
- Direct pool contract queries via Alchemy RPC

**Tokens to scan:** wstETH, weETH, osETH, rsETH, ETHx, cbETH, rETH

**Output:** `data/lst_liquidity.csv` — token, pool, TVL, depth at 1%/2%/5% depeg

### Step 2: Historical Depeg Magnitudes
How far has each LST's peg actually moved during past stress events?

**Data sources:**
- DEX price history: Uniswap/Curve pool price feeds via subgraphs or DefiLlama
- stETH/ETH during Jun 2022 (known: ~7% depeg). Others during same period?
- Any depeg events during Aug 2024 (Yen carry), Feb 2025 crash, other episodes

**Key dates to check:** Jun 2022, Nov 2022, Aug 2024, Feb 2025 (overlap with position topology episodes)

**Output:** `data/lst_depeg_history.csv` — token, date, max depeg %, duration, concurrent ETH drawdown

### Step 3: Oracle Lag Analysis
Chainlink oracles have heartbeat intervals and deviation thresholds. During rapid depeg, does the oracle update fast enough for Aave to trigger liquidations, or does arb restore the peg before the oracle moves?

**Data sources:**
- Chainlink oracle contracts: `latestRoundData()` at historical blocks during depeg events
- Compare oracle price vs DEX spot price during depeg windows
- Aave oracle wrapper contracts (may use different feeds for different LSTs)

**Questions:**
- What is the heartbeat for each LST oracle? (1h? 24h?)
- What deviation threshold triggers an update? (0.5%? 1%?)
- During the Jun 2022 stETH depeg, did the oracle lag behind DEX price? By how much?

**Output:** `data/oracle_lag.csv` — token, oracle address, heartbeat, deviation threshold, lag during stress events

### Step 4: Phantom Wall Activation Thresholds
Combine Steps 1-3 to compute: for the $5.6B phantom wall, what depeg magnitude activates each tier?

**Method:**
- From Step 1: liquidity depth tells us how much selling produces X% depeg
- From position data (already collected): phantom positions per LST with their HF
- Compute: at X% depeg, which phantom positions reach HF < 1?
- Account for oracle lag (Step 3): if oracle only updates at 1% deviation, positions at HF 1.005 won't be liquidated until depeg exceeds ~1%

**Output:** `data/activation_thresholds.csv` — token, depeg %, positions activated, debt activated, collateral at risk

### Step 5: Transaction-Level Cascade Replay
Replay historical cascades at the transaction level to characterize real-time cascade dynamics. The position phase measured topology statically (snapshots at episode onset). This step measures what happens once the first liquidation fires.

**Method:**
- Pull all `LiquidationCall` events from Aave (v2/v3) and Compound during the 4 escalating episodes (Jan 2022, Jun 2022, Aug 2024, Feb 2025) + 2 absorbed episodes for comparison (FTX Nov 2022, Aug 2023)
- Sequence by block/timestamp: collateral seized, debt repaid, collateral asset, price at that block
- Measure per episode:
  - Liquidation rate: events per block, per minute, per hour
  - Cumulative selling pressure: total collateral dumped over time
  - Price impact: ETH price change per $X of liquidation selling
  - Tipping point: at what liquidation density ($/min) does the cascade become self-sustaining vs peter out?
  - Time structure: does it accelerate, plateau, or come in waves?
- Compare escalating vs absorbed: same metrics, different outcomes. What's the measurable difference at the transaction level?

**Data sources:**
- Aave v2/v3 Pool contract `LiquidationCall` events (topic: `0xe413a321...`). Indexed by Alchemy `eth_getLogs` with block range filters.
- Compound `AbsorbCollateral` / `LiquidateAbsorb` events
- ETH price at each liquidation block (from on-chain oracle or existing price data)

**Output:** `data/cascade_replay_{episode}.csv` — block, timestamp, user, collateral_asset, collateral_seized_usd, debt_repaid_usd, eth_price, cumulative_selling, liquidation_rate. Plus `data/cascade_dynamics.csv` — per-episode summary with tipping point, peak rate, total duration, self-sustaining threshold.

### Step 6: Contagion Dynamics
Does a depeg in one LST spread to others?

**Mechanisms to test:**
- Direct: Tier 3 liquidation dumps osETH → DEX selling → osETH/ETH drops further. Does this selling pressure leak into weETH or wstETH pools?
- Indirect: Market panic — seeing one LST crack causes selling of others
- Structural: Some positions use multiple LSTs as collateral. One LST depegging weakens the whole position.

**Data sources:**
- Cross-LST correlation during historical stress events (from Step 2 data)
- Shared pool exposure (e.g., Balancer pools with multiple LSTs)
- Multi-LST collateral positions from existing Aave snapshot data

**Output:** `findings.md` — contagion pathways, correlation measurements, cascade propagation model

## Infrastructure

Reuses existing infrastructure from position phase:
- Alchemy RPC (`../position/alchemy.txt`) — pool queries, oracle queries, historical state
- The Graph (`../position/graph.txt`) — Aave v3 position data (phantom positions already characterized)
- ETH price data (`../data/eth_price.csv`)
- Position snapshots (`../position/data/positions_*.csv`) — phantom positions with HF, collateral type, debt type

New infrastructure needed:
- DEX subgraphs (Uniswap v3, Curve, Balancer) or direct pool queries for liquidity depth
- Chainlink oracle contract ABIs for `latestRoundData()` historical queries

## Scope Control

Start with Step 1 (liquidity depth) — it's the most tractable and immediately answers "how much selling breaks the peg." If Tier 3 LSTs can be depegged with <$50M of selling and $300M of phantom positions sit behind that threshold, the cascade risk is quantifiable and the investigation proceeds. If all LSTs require >$500M to depeg 2%, the wall is effectively unreachable and the investigation can stop early.

## Connection to Prior Work

| Phase | What it produced | What this phase uses |
|-------|-----------------|---------------------|
| Flow (17 iterations) | Monitoring system: regime → early warning → classification. Identified escalation prediction as unsolved. | Episode dates, liquidation event data |
| Position (6 iterations) | Real/phantom decomposition. Conditional fuel map. Cascade mechanics (progressive + cliff). Risk rotation finding. | Phantom position inventory ($5.6B, per-LST breakdown, HF distribution) |
| **Correlation** (this) | Depeg activation thresholds. Transaction-level cascade dynamics. Contagion model. Complete phantom-wall risk characterization. | — |
