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

### Step 6: OI Leading Signal Refinement

The flow phase established that Binance ETHUSDT open interest drops (>4% hourly) precede Aave lending liquidation peaks by a corrected median of 37 hours, with 94% consistency (16/17 episodes) and 10.9% median further price decline after signal fires. Current limitations: Binance-only, OI proxy includes voluntary closures, 30% precision at 3% threshold (~5 false alarms/year at 4%).

**6a. Multi-exchange OI coverage**

Binance OI is one exchange. Test whether aggregating OI across exchanges (Bybit, OKX, Deribit) produces a cleaner signal. Binance 5-min OI snapshots are available via their data archive. Other exchanges: check Bybit public API (`/v5/market/open-interest`), OKX (`/api/v5/public/open-interest`), Deribit (`/public/get_book_summary_by_currency`).

- Pull multi-exchange OI for the same 17 episodes (2024+)
- Compare single-exchange vs aggregate OI signal: does aggregate reduce false positives?
- Test whether one exchange consistently leads others (exchange-level cascade ordering)

**6b. Crash-type conditioned signal quality**

Links phase showed macro crashes produce 2× daily amplification and 4× cumulative damage vs crypto-native. Does the OI signal behave differently?

- Split the 17 episodes by crash catalyst type (macro vs crypto-native vs rotation)
- Compare lead time, precision, and price-decline-after-signal across types
- Test: does the OI signal fire earlier for macro crashes (cross-market transmission) vs crypto-native (direct leverage)
- Interaction: OI signal + VIX level. Does high VIX + OI drop have higher precision than OI drop alone?

**6c. Voluntary vs forced closure decomposition**

The core proxy weakness: OI drops include voluntary de-risking. Two approaches:

1. **Funding rate diagnostic.** During forced liquidations, funding rate should spike (longs liquidated → forced selling → price drops → negative funding). During voluntary closures, funding rate may not spike. Cross-reference OI drops with concurrent funding rate changes. Binance funding rate is available at 8h intervals via API.

2. **OI drop velocity profile.** Forced liquidation cascades should produce sharper, more concentrated OI drops (cascade dynamics). Voluntary de-risking should produce more gradual OI decline. Compare the 5-min OI profile shape of true positive episodes vs false positive episodes.

**6d. Signal conjunction test**

The flow phase proposed but never tested the three-layer conjunction: utilization (pre-condition) → perp OI (early warning) → magnitude (classification). Test it now with full dynamics data:

- Define trigger: Aave utilization >40% AND OI drop >4% in same 48h window
- Compare precision vs OI-only: does the utilization pre-condition filter reduce false positives?
- Add VIX conditioning from links phase: utilization >40% AND OI drop >4% AND VIX >22
- Report precision, recall, and lead time for each conjunction variant

**Output:** `data/oi_signal_refined.csv`, findings integrated into exploration log

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
| 7 | OI signal refinement | Open | Multi-exchange, crash-type conditioning, voluntary/forced decomposition, conjunction test. |

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
