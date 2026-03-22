# Dynamics — Execution Plan

## Question

How does money flow through the DeFi leverage system during major price moves? Where does it enter, how does it get leveraged, and how does it exit?

The prior phases mapped the static structure (position topology, oracle architecture, DEX depth). This phase measures the system *in motion* — how the structure changes during crashes and bull runs.

## Price Epochs

| Episode | Dates | Move | Type |
|---------|-------|------|------|
| 2022 Bear Leg 1 | Jan 1 → Jun 18 2022 | $3,764 → $983 (−74%) | Crash — Terra/3AC/stETH depeg |
| 2022 Bear Rally | Jun 18 → Aug 13 2022 | $983 → $1,983 (+102%) | Rally — Merge anticipation |
| 2022 Bear Leg 2 | Aug 13 → Nov 21 2022 | $1,983 → $1,112 (−44%) | Crash — FTX collapse |
| 2023 Recovery | Nov 21 2022 → Mar 11 2024 | $1,112 → $4,067 (+266%) | Bull — Shapella, ETF anticipation |
| 2024 Consolidation | Mar 11 → Aug 7 2024 | $4,067 → $2,362 (−42%) | Drawdown — Yen carry unwind |
| 2024 Bull Run | Aug 7 → Dec 16 2024 | $2,362 → $4,025 (+70%) | Bull — post-Yen recovery |
| 2025 Crash | Dec 16 2024 → Apr 8 2025 | $4,025 → $1,465 (−64%) | Crash — largest drawdown in dataset |
| 2025 Recovery | Apr 8 → Aug 22 2025 | $1,465 → $4,820 (+229%) | Bull — strongest recovery |
| 2025 Q4 Chop | Aug 22 → Dec 17 2025 | $4,820 → $2,823 (−41%) | Drawdown — volatile |
| 2026 Crash | Dec 17 2025 → Feb 24 2026 | $3,362 → $1,854 (−45%) | Crash — most recent |
| 2026 Recovery? | Feb 24 → Mar 19 2026 | $1,854 → $2,202 (+19%) | Rally — current |

## Execution

No active steps. All planned steps complete or deferred.

---

## Done

### Step 1: Exchange Flow Pull ✅
Pull CoinMetrics ETH exchange flow data for full 2022-2026 range. Merge with existing price data. Compute net flows, cumulative reserve changes per epoch.

**Result:** Null signal at daily resolution (max |r| < 0.04). Measurement gap: unmeasured flows dominate reserve changes.

**Output:** `data/daily_flows.csv`, `data/epoch_flow_summary.csv`, `data/flow_price_lag.csv`, `data/reserve_price_lag.csv`

### Step 2: Liquidation Event Pull ✅
Pull all Aave v2/v3 LiquidationCall events for the full date range (2022-01 → 2026-03). Decode and enrich with price data.

**Result:** 65,382 events. Phantom: 161 (0.2%). Real: 38,055. Full collateral type breakdown.

**Output:** `data/liquidations_full.csv`

### Step 3: Epoch Position Snapshots ⏸ Deferred
For each of the 11 epochs, take 3 position snapshots (start, mid, end) via subgraph historical queries. Compute real/phantom split, HF distribution, concentration metrics.

**Status:** Aggregate findings sufficient for dynamics picture. Would add HF distribution depth for recharge model quantification.

### Step 4: Protocol TVL + Utilization ✅
Pull Aave TVL, borrow volume, and utilization from DefiLlama and/or subgraph at epoch boundaries.

**Result:** Utilization homeostasis at 38-42%. ETH-borrow denomination artifact identified and corrected.

**Output:** `data/protocol_metrics_daily.csv`, `data/protocol_epoch_summary.csv`

### Step 5: Synthesis ✅
Combine all layers into per-epoch narratives and cross-epoch patterns.

**Output:** `findings.md`, `exploration-log.md`

### Step 6: OI Leading Signal Refinement ✅

Refined the flow phase's OI leading signal across four sub-investigations. Original plan had 6a-6d; 6b and 6d were superseded during investigation by higher-value tests.

**6a. Multi-exchange OI coverage** — Bybit and OKX OI pulled. OI drops are exchange-specific, not market-wide (Binance-Bybit correlation goes negative during stress). Aggregating dilutes signal (enrichment 4.7x → 2.3x). Binance-only is the cleanest single signal. OKX has insufficient history.

**Contract OI validation** — The flow phase's 37h lead / 94% consistency was measured on USD OI (contaminated by price). Contract OI (cleaner metric): 27h lead, 82% consistency, 7.9x enrichment at >3% with ~2 false alarms/year. Contract OI detects "traders closing positions," USD OI detects "price dropping."

**Escalation predictor** — Contract OI >3% predicts episode escalation: Fisher's p=0.0345. All 7/7 episodes with contract-OI drops escalated vs 4/10 without. Resolves the flow phase iteration 15 failure (p=0.515 on USD OI).

**6c. Voluntary vs forced decomposition** — 3-tier structure: Tier 1 (forced: OI drop + negative funding, 4 eps, $122M median peak liq), Tier 2 (voluntary: OI drop + normal funding, 3 eps, $35M), Tier 3 (mild: no OI drop, 10 eps, $7M). Kruskal-Wallis p=0.007 on peak liquidation. Velocity profiles directionally confirm (Tier 1 median 69% 30m concentration vs Tier 2 15%) but n too small for significance.

**6b/6d superseded.** 6b (crash-type conditioning) absorbed into 3-tier analysis — no clean pattern by crash type. 6d (conjunction test) replaced by escalation predictor — contract OI >3% alone achieves the filtering that conjunction was designed for; utilization homeostasis at 38-42% makes it a non-discriminating gate.

**Key insight:** The 3-tier structure classifies mechanism (how stress propagates), not outcome (how far price falls). Outcome = mechanism × leverage state × macro context. Episode 10 (-20.2% fwd return, no OI drop) defines the structural blind spot: lending stress from direct price decline without perp participation.

**Output:** `multi_exchange_oi.py`, `contract_oi_validation.py`, `escalation_test.py`, `data/6a_results.txt`, `data/contract_oi_results.txt`, `data/escalation_results.txt`, `data/bybit_oi_*.csv`, `data/okx_oi_*.csv`, `data/binance_funding_*.csv`

---

## Key Questions

| # | Question | Status | Finding |
|---|----------|--------|---------|
| 1 | Leverage build/unwind asymmetry | ✅ Answered | Crash/recovery asymmetry 9-203× by liquidation volume. Unwind in hours (3 days = 45-89% of volume), rebuild over months. |
| 2 | Phantom position lifecycle | Partially answered | Phantom positions don't liquidate during crashes (139 organic events in 4.2 years). Open/close dynamics require snapshot time series — deferred. |
| 3 | Liquidation composition shift | ✅ Answered | No shift toward phantom liquidations (0.2%). Real collateral shifting: wstETH 0% (2022) → 56% (2025). Distinct user population, larger positions. |
| 4 | Exchange flow as leading indicator | ✅ Answered: No | Max |r| < 0.04 at all lags. Measurement gap makes data fundamentally incomplete. |
| 5 | Post-crash topology | Partially answered | User turnover 5-57%. Full topology requires deferred Step 3. |
| 6 | 2026 crash specifically | ✅ Answered | $5.6B phantom wall survived. $1.42B whale survived. $193M real liquidations, 87% in top 3 days. |
| 7 | OI signal refinement | ✅ Answered | Contract OI (not USD OI) is the correct metric. 27h lead, 7.9x enrichment, ~2 false alarms/year. Predicts escalation (p=0.0345). 3-tier mechanism classification (forced/voluntary/mild) validated at p=0.007. Exchange-specific, not market-wide. Structural blind spot: events where lending stress bypasses perp layer (1/17 episodes). |

## Infrastructure

All existing:
- Alchemy RPC (`../position/alchemy.txt`) — LiquidationCall events, historical state
- The Graph (`../position/graph.txt`) — position snapshots at historical blocks
- CoinMetrics community CSV — exchange flows (free, no key)
- DefiLlama API — protocol TVL (free)
- ETH price data (`../data/eth_price.csv`)
- Binance API — 5-min OI snapshots, 8h funding rate (free, no key for public endpoints)
- Bybit/OKX public APIs — OI data (free)

## Connection to Prior Work

| Phase | What it produced | What this phase uses |
|-------|-----------------|---------------------|
| Flow (17 iterations) | Liquidation episode classification. 37h OI lead signal. Position heterogeneity principle. | Episode dates, OI signal baseline, perp_lead.py scripts |
| Position (6 iterations) | Real/phantom decomposition. Snapshot methodology. | Scanner scripts, position classification logic |
| Correlation (4 iterations) | Oracle architecture. DEX depth. CAPO risk. March 10 forensics. | Phantom position inventory, whale addresses |
| Links (4 iterations) | Amplification model. VIX regime coupling. Crash taxonomy by catalyst. | Crash type classification, VIX thresholds for conjunction test |
| **Dynamics** (this) | How the system behaves in motion across full bull/bear cycles. | — |
