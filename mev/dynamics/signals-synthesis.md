# Dynamics — Signals Synthesis

## Signals Tested

### Ranked by Strength

| # | Signal | Lead Time | Strength | Verdict |
|---|--------|-----------|----------|---------|
| 1 | **Contract OI >3% as escalation predictor** | +27h median | Strong | Fisher's p=0.0345 — all 7/7 episodes with contract-OI drops escalated. 7.9x enrichment, ~2 false alarms/year. Detects "traders are closing positions" (not just "price is dropping"). Resolves flow phase iteration 15 failure. |
| 2 | **3-tier mechanism classification** | Contemporaneous | Strong | Kruskal-Wallis p=0.007 on peak liquidation. Forced cascade ($122M), voluntary de-risking ($35M), mild ($7M). Classifies mechanism, not outcome. |
| 3 | **Liquidation spike concentration** | Contemporaneous | Strong | 3 days = 45-89% of epoch volume. Not predictive, but defines the shape of cascade events. Consistent across all 6 crash epochs. |
| 4 | **User turnover between crashes** | Structural (months) | Strong | 5-57% overlap depending on rebuild time. Robust across 5 crash pairs. Measures system reload state. |
| 5 | **Crash/recovery asymmetry** | Structural | Strong | 9-203× by real liquidation volume. Consistent across all crash→recovery pairs except FTX anomaly. |
| 6 | **Phantom wall crash immunity** | Structural | Strong (negative) | 139 organic liquidations in 4.2 years across 6 crash epochs. Mechanism confirmed via CAPO oracle architecture. Strongest negative finding in the phase. |
| 7 | **Pre-crash borrow × crash depth** | Structural (months) | Weak-moderate | r=0.47 (n=6). Directionally correct. Best single aggregate predictor but not reliable with small sample. Confounded by crash type. |
| 8 | **Utilization as leverage ceiling** | Structural | Moderate | 38-42% homeostasis post-2022. Rate controller constrains leverage buildup. Not directly predictive but sets bounds on stored energy. |
| 9 | **Crash taxonomy (endo/exo)** | Requires catalyst knowledge | Conjectured | n=1 exogenous (2024 Yen carry). Pattern is mechanistically intuitive but untested beyond one case. |

### Refined in Step 6

| Signal | Original (Flow Phase) | Refined (Dynamics Step 6) | Change |
|--------|-----------------------|---------------------------|--------|
| OI lead time | 37h (USD OI) | 27h (contract OI) | -10h; cleaner metric removes price contamination |
| OI consistency | 94% (16/17) | 82% (14/17) | Lower but on genuine position closures, not price artifact |
| OI enrichment at >3% | 3.9x (USD) | 7.9x (contract) | 2× better; fewer signals but much higher precision |
| OI false alarms/year | ~20 (USD at >3%) | ~2 (contract at >3%) | 10× fewer false alarms |
| OI as escalation predictor | p=0.515 (USD) | p=0.0345 (contract) | From "doesn't predict" to "significantly predicts" |
| Multi-exchange benefit | Not tested | None — dilutes signal | Binance-only is cleanest. OI drops are exchange-specific. |
| Forced vs voluntary | Not decomposed | 3-tier via funding rate | Funding rate <-0.01% identifies forced cascades (4/17 episodes) |

### Noise (no signal found)

| Signal | What was tested | Result | Don't revisit because |
|--------|----------------|--------|----------------------|
| Daily net exchange flow → price | Cross-correlation lags -5 to +5, 1,538 days | Max \|r\| = 0.036 | CoinMetrics flow methodology captures minority of actual balance movements. Measurement gap is structural, not resolvable with different aggregation. |
| Daily reserve change → price | Cross-correlation lags -5 to +5, 1,538 days | Max \|r\| = 0.044 | Even direct balance observation (bypassing flow measurement) shows no signal. The unmeasured component also doesn't carry signal. |
| Within-epoch flow-price correlation | Pearson correlation per epoch, 11 epochs | Max \|r\| = 0.17 | Weak even within regimes. No epoch shows dominant flow-price relationship. |
| ETH-denominated borrow change during crashes | Appeared to show leverage increasing | Denomination artifact | Mechanical price effect: ETH-equivalent of constant USD debt doubles when price halves. USD borrow change is the truthful measure. Residual negative in 5/6 crashes. |
| stETH event count as composition signal | 44% of real events in 2025_q4_chop | Dust artifact | 2,538 events = 11.1 stETH total ($33K). Median 0.002 stETH ($6). Noise from dust farming, not structural signal. |
| Multi-exchange OI aggregation | Bybit + Binance aggregate vs Binance-only | Dilutes signal | Enrichment drops from 4.7x to 2.3x. OI drops are exchange-specific (correlation goes negative during stress). Cross-exchange cascade essentially simultaneous when both fire (1.5h median). |
| Velocity profile as forced/voluntary discriminant | 30m concentration for 7 contract-OI episodes | Directionally correct, n too small | Tier 1 median 69% vs Tier 2 15%, but exceptions exist (ep 9 gradual despite forced, ep 16 sharp despite voluntary). Two orthogonal axes, not one clean discriminant. |

### Structural Blind Spots

| Blind spot | Evidence | Implication |
|-----------|----------|-------------|
| Lending stress bypassing perp layer | Episode 10: -20.2% 7d return, $44M peak liq, no contract OI drop, no negative funding. ETH-specific rotation without perp market participation. | Contract OI cannot detect events where lending stress comes from direct price decline without perp position closure. 1/17 episodes in 2024-2026 sample. |
| Control sample fragility | 3 control months, ~2 drops at >3% threshold | Enrichment ratio rank ordering (Binance > aggregate) is robust but absolute magnitudes are fragile. |

## Composite Signal: What Could Be Constructed

The individual signals combine into a **system state assessment + early warning framework**:

### Early Warning: Contract OI Monitor
- **Input:** Binance ETHUSDT contract-denominated OI (`sum_open_interest`), hourly
- **Trigger:** >3% hourly drop in contract OI
- **What it means:** Perp traders are actually closing positions (not just price declining). 100% of episodes where this fires escalated. Median 27h lead before lending liquidation peak.
- **Precision:** 7.9x enrichment over background rate. ~2 false alarms/year at >3% threshold.
- **Severity indicator:** If concurrent funding rate <-0.01%, classified as forced cascade (Tier 1, median $122M peak liquidation). If funding rate normal, voluntary de-risking (Tier 2, median $35M).
- **Blind spot:** Lending stress from direct price decline without perp participation (episode 10 type). ~6% of episodes.

### Stored Energy Estimate
- **Input:** Total Aave borrowed (USD) from DefiLlama, updated daily
- **Signal:** Higher borrow = more stored liquidation energy
- **Weakness:** r=0.47 with crash outcomes. Doesn't account for HF distribution (concentrated near threshold vs spread across safe levels). Would improve with position-level HF data (deferred Step 3).

### Recharge State
- **Input:** Time since last major liquidation episode + price change since last episode
- **Signal:** Longer rebuild + bigger rally = more fresh leverage with new participants. Systems that recently crashed (< 60 days) have depleted liquidation supply.
- **Qualitative support:** FTX (56-day rebuild) → $12M. Yen carry (475-day rebuild) → $302M. 

### Fragility Indicator (speculative, not yet tested)
- **Input:** wstETH share of real-position collateral (from subgraph or protocol analytics)
- **Signal:** Higher wstETH share → fewer but larger positions → potentially more concentrated liquidation events when they occur
- **Status:** Observed pattern (wstETH users are 13.5× larger, more spike-concentrated), but not yet tested as predictor

### Utilization Bound
- **Input:** Aave utilization rate
- **Signal:** >42% → system near structural ceiling, rate controller will resist further leverage buildup. <35% → room for significant leverage accumulation.
- **Strength:** Consistently observed post-2022. One exception: 2022_bear_1 broke to 31%.

## What's Next

### Option A: Deeper investigation (Step 3 position snapshots)
- **What:** HF distribution at epoch boundaries via subgraph queries (~33 queries for 11 epochs × 3 points)
- **Why:** Would convert recharge model from qualitative (r=0.47) to potentially quantitative. HF tail concentration might predict liquidation intensity better than aggregate borrow.
- **Cost:** ~33 subgraph queries, reusing position phase scanner
- **Expected return:** Moderate. The aggregate picture is established. Snapshots would refine specific questions (2024 anomaly decomposition, HF distribution shapes, phantom lifecycle timing).

### Option B: Real-time pipeline
- **What:** Monitor current system state using the signals identified
- **Components:** Binance contract OI hourly monitor, funding rate tracker, daily DefiLlama borrow pull, time-since-last-crash tracker, utilization monitor
- **Why:** The dynamics findings describe how the system behaves. A pipeline would track *where we are now* in the recharge cycle and fire alerts when contract OI drops >3%.
- **Status:** The monitoring system from the flow phase already tracks liquidation episodes. Adding contract OI, funding rate, borrow level, and utilization would complete the state picture.

### Option C: Pivot to different research direction
- **What:** The dynamics phase answered the "how does money flow" question. The remaining open threads (phantom lifecycle, 2024 anomaly, HF distributions) are refinements, not new questions.
- **Possible pivots:** Liquidator ecosystem analysis (who extracts value from stress events), cross-protocol cascade modeling (Aave → Compound → Maker ordering), or real-time oracle risk monitoring (extending the CAPO findings).

### Recommendation
Option B is the highest-return next step. The dynamics findings are structural and won't change much with more data. A real-time state tracker incorporating the contract OI early warning signal (27h lead, 7.9x enrichment) alongside recharge state and utilization would make the findings operationally useful. The contract OI monitor is the most actionable single signal discovered across all phases.
