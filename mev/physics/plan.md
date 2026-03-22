# Physics — Market Processes with Inherent Latency

## Premise

The contract OI signal (27h lead, p=0.035) works because it measures a physical process — positions unwinding through a leverage hierarchy — that takes time regardless of information speed. Markets are fast at pricing information but slow at moving atoms. Anywhere a process involves moving real assets, institutional decision-making, queue-based processing, or periodic settlement, there is latency that cannot be arbitraged away.

This investigation maps and measures these physical processes in crypto and TradFi markets.

## Status

| # | Process | Status | Result |
|---|---------|--------|--------|
| 1 | Funding Rate → Position Closure | **Tested — Negative** | Informational timing, arbitraged away. Price dominates, funding adds nothing. Both extremes show OI drops (volatile regime symptom, not cause). |
| 2 | ETF Flow → Market Impact Lag | **Tested — Pattern observed** | Outflows accompany multi-day clusters, terminal days show flow reversal. n=14 spike days, n=3 clusters. Not statistically significant. Acts as cascade-type classifier, not predictor. |
| 3 | Collateral Chain Propagation | **Tested — Positive** | Not a sequential cascade. Oracle-gated threshold batching: 67% same-block, B=0.77, ~7.6 min inter-burst gap. Mega-bursts up to 377 events. 78% collateral-homogeneous. |
| 3b | Self-Reinforcement (follow-up) | **Tested — Inconclusive** | Hourly price resolution insufficient. Confound between self-reinforcement, liquidity thinning, and velocity clustering cannot be separated. Best estimate: second-order positive feedback. |
| 4 | Liquidity Withdrawal Dynamics | **Deprioritized** | Behavioral, not hard physical. Partially addressed by Phase 6 (8-27% LP depth loss). |
| 5 | Validator Exit Queue | **Deprioritized** | Weeks-to-months timescale, too slow for crash dynamics. |
| 6 | Margin Call Cycles | **Deprioritized** | Same structural category as #1 (informational timing). Expected negative result. |
| 7 | Stablecoin Mint/Burn Latency | **Deprioritized** | Indirect connection to crash mechanics. |
| 8 | Cross-Venue Arb Settlement | **Not tested** | Partially measured in Phase 6 (1h THORChain mean-reversion). |

## Key Structural Learning

**Informational vs Physical timing:** Processes with known schedules and visible parameters (#1 Funding, #6 Margin calls) produce no exploitable timing. Processes with hard sequential dependencies (#3 Collateral chain) or physical settlement constraints (#2 ETF flows) show measurable structure.

**"Cascade" → "Threshold batch process":** The data overturns the cascade metaphor. Liquidations are not sequential chains (A→B→C). They are simultaneous batch events triggered by discrete oracle price updates. The relevant objects are position density distribution and oracle step size, not propagation speed.

## Known Physical Processes

### 1. Funding Rate → Position Closure Clustering

Binance perp funding settles every 8 hours. Deeply negative funding at settlement creates an 8-hour decision window — traders absorb the cost or close before the next settlement. Position closures may cluster in the hours following negative funding settlements.

**Testable now.** Existing data: Binance 8h funding rate (dynamics phase, 919 episode records + 267 control), 5-min OI snapshots. Test whether contract OI drops cluster in the 0-4h window after negative funding settlements vs other times.

### 2. ETF Flow → Market Impact Lag

BTC and ETH ETF creations/redemptions are T+1 settlement. Daily flow data is published after market close. Large outflows represent institutional decisions that execute over hours-to-days: decision → approval → broker instruction → redemption → settlement → market sale of underlying.

**Data:** ETF flow data is public daily. BTC ETFs since Jan 2024, ETH ETFs since Jul 2024. Pull from public sources (e.g., SoSoValue, BitMEX Research, or SEC filings).

**Key test:** Do large ETF outflow days predict next-day or next-week crypto returns? Does the 2025 January mystery (-11.2% ETH residual, 18 liqs/day) coincide with ETH ETF outflows?

### 3. Collateral Chain Propagation

When Aave liquidates a position, the seized collateral is sold. If that sale depresses the price enough to trigger the next liquidation, there's a measurable propagation delay (block confirmation + liquidator execution + DEX routing). The dynamics phase measured the aggregate 5-7 day cascade timescale. The per-link propagation time within a single cascade day is unmeasured.

**Testable with existing data.** The 65,382 liquidation events have block numbers. Within spike days, measure the inter-liquidation interval distribution. Is it random, or do liquidations cluster in bursts with gaps (propagation waves)?

### 4. Liquidity Withdrawal Dynamics

Market makers and LPs withdraw liquidity during stress. THORChain showed 8-27% depth loss per crash episode. CEX order books thin similarly. The withdrawal is progressive, not instantaneous — some participants withdraw at first sign of stress, others wait.

**Data:** THORChain hourly depths exist (crosschain phase). CEX order book snapshots are harder — Kaiko, Tardis.dev have historical data but are paid. Binance provides current depth but not historical.

**Key question:** Does the rate of liquidity withdrawal predict cascade severity? Early fast withdrawal = worse cascade, or does early withdrawal actually *prevent* cascades by making the remaining book more resilient (thinner but with committed LPs)?

### 5. Validator Exit Queue

ETH validator exits process through a rate-limited queue. When many validators want to exit simultaneously, the queue grows and creates a backlog of ETH that will hit the market in the future (days to weeks). Queue length is on-chain and real-time.

**Data:** Beacon chain API, or services like beaconcha.in. Queue length over time, correlated with ETH price and staking yield.

**Key test:** Does exit queue growth precede ETH selling pressure? Or is it a lagging indicator (validators exit after price already dropped)?

### 6. Margin Call Cycles

Traditional prime brokers issue margin calls on institutional schedules (typically morning, banking hours). Crypto-native funds with TradFi lenders face forced selling during banking hours, creating predictable intraday windows.

**Data:** Hard to measure directly. Proxy: does crypto selling volume cluster in specific hours (9-11am ET, corresponding to US margin call windows)? Testable with hourly price data already available.

### 7. Stablecoin Mint/Burn Latency

USDT minting requires fiat settlement (banking hours, wire transfers). USDC minting via Circle is faster but still not instant. Large mints represent capital entering crypto; large burns represent exits. The time between the decision to enter/exit and the actual on-chain mint/burn creates latency.

**Data:** On-chain mint/burn events for USDT and USDC are public (Transfer events from zero address). Glassnode, Nansen, or direct event logs.

**Key test:** Do large stablecoin mints/burns lead price? What's the typical lag between a mint event and price impact?

### 8. Cross-Venue Arbitrage Settlement

Arbitraging between CEX and DeFi requires: detect opportunity → submit transaction → wait for confirmation → settle. On Ethereum L1 this is ~12 seconds per block but can be minutes during congestion. Cross-chain (THORChain) takes 10-15 minutes. During fast moves, the settlement time creates a window where prices diverge.

**Partially measured.** THORChain dislocations mean-revert within 1 hour in 4/5 episodes. CEX-to-DeFi arb settlement time unmeasured.

### 9+ Captain's Discretion

Follow leads which were generated in this investigation. 


## Approach

This is exploratory. The processes above are starting points, not a checklist. The investigation should:

1. Pick the most testable process (existing data, clear hypothesis)
2. Measure it
3. Follow leads — if funding settlement clustering exists, what does that imply about the next link in the chain?
4. Kill processes that don't show measurable latency
5. For processes with confirmed latency, estimate the information content: does knowing the process state improve prediction beyond what price alone tells you?

The goal is to map which physical processes create exploitable time windows and which are already arbitraged despite their latency.

## Data Available

| Data | Location | Coverage |
|------|----------|----------|
| Binance 5-min OI | dynamics phase cache | 17 episodes, 2024-2026 |
| Binance 8h funding rate | `dynamics/data/binance_funding_episodes.csv` | 17 episodes + 3 control months |
| Aave liquidation events | `dynamics/data/liquidations_full.csv` | 65,382 events, 2022-2026, with block numbers |
| THORChain hourly depths | `crosschain/data/hourly_depths.csv` | 5 crash windows, 3 pools |
| ETH hourly price | `data/eth_price_1h.csv` | 36,734 rows, 2022-2026 |
| TradFi daily | `links/data/tradfi_daily.csv` | S&P, VIX, USD/JPY, DXY, yields, 2022-2026 |
| BTC/ETH ETF daily flows | `physics/data/etf_daily_flows.csv` | 565 trading days, Jan 2024 – Mar 2026 |

## Data to Pull

| Data | Source | Cost | Status |
|------|--------|------|--------|
| BTC/ETH ETF daily flows | SoSoValue, public CSV | Free | **Pulled** — 565 rows |
| ETH validator exit queue history | Beacon chain API / beaconcha.in | Free | Not pulled (deprioritized) |
| Stablecoin mint/burn events | Alchemy RPC (event logs) | Free (existing key) | Not pulled (deprioritized) |
| Hourly crypto volume by exchange | CoinGecko API or similar | Free tier may suffice | Not pulled |
| CEX order book depth history | Kaiko / Tardis.dev | Paid — evaluate if needed | Not pulled |
| Minute-level ETH price | Binance 1-min klines (free API) | Free | Not pulled (would resolve self-reinforcement question) |
| Chainlink oracle events | Alchemy archive RPC | Free/Paid | Not pulled (would confirm oracle-gating directly) |

## Connection to Prior Work

This phase sits on top of everything. Each prior phase identified a temporal structure:

| Phase | Temporal finding | Physical process | Physics phase connection |
|-------|-----------------|------------------|------------------------|
| Flow | 37h perp→lending lead (revised to 27h on contract OI) | Leverage tier propagation | 27h gap = behavioral lag between continuous CEX deleveraging and oracle-gated DeFi liquidation |
| Position | Conditional severity at wall proximity | Static topology, no time dimension | Position density at each price level determines batch size per oracle step |
| Correlation | 84-second CAPO cascade (March 10) | Oracle update → liquidation bot response | Same oracle-gated batch mechanism, different trigger |
| Dynamics | 5-7 day cascade timescale, 3 spike days = 45-89% of volume | Aggregate deleveraging | Repeated oracle-gated batching across days; multi-day structure from external pressure (ETF flows) + position cluster topology |
| Links | Sub-daily macro→crypto, DeFi amplification on 5-7 day timescale | Cross-market transmission | Second-order positive feedback (~100bps/100 liqs) within oracle-gated batches |
| Crosschain | 1-hour dislocation mean-reversion, 8-27% LP withdrawal per crash | Arb settlement, LP behavioral response | Liquidity thinning amplifies later batches; dislocation timescale reflects cross-venue arb settlement |
| **Physics** (this) | Oracle-gated threshold batching, ETF flow cascade classification | Crash lifecycle model | Connective tissue linking all prior findings |
