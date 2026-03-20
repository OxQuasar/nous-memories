# Dynamics — Signals Synthesis

## Signals Tested

### Ranked by Strength

| # | Signal | Lead Time | Strength | Verdict |
|---|--------|-----------|----------|---------|
| 1 | **Liquidation spike concentration** | Contemporaneous | Strong | 3 days = 45-89% of epoch volume. Not predictive, but defines the shape of cascade events. Consistent across all 6 crash epochs. |
| 2 | **User turnover between crashes** | Structural (months) | Strong | 5-57% overlap depending on rebuild time. Robust across 5 crash pairs. Measures system reload state. |
| 3 | **Crash/recovery asymmetry** | Structural | Strong | 9-203× by real liquidation volume. Consistent across all crash→recovery pairs except FTX anomaly. |
| 4 | **Phantom wall crash immunity** | Structural | Strong (negative) | 139 organic liquidations in 4.2 years across 6 crash epochs. Mechanism confirmed via CAPO oracle architecture. Strongest negative finding in the phase. |
| 5 | **Pre-crash borrow × crash depth** | Structural (months) | Weak-moderate | r=0.47 (n=6). Directionally correct. Best single aggregate predictor but not reliable with small sample. Confounded by crash type. |
| 6 | **Utilization as leverage ceiling** | Structural | Moderate | 38-42% homeostasis post-2022. Rate controller constrains leverage buildup. Not directly predictive but sets bounds on stored energy. |
| 7 | **Crash taxonomy (endo/exo)** | Requires catalyst knowledge | Conjectured | n=1 exogenous (2024 Yen carry). Pattern is mechanically intuitive but untested beyond one case. |

### Noise (no signal found)

| Signal | What was tested | Result | Don't revisit because |
|--------|----------------|--------|----------------------|
| Daily net exchange flow → price | Cross-correlation lags -5 to +5, 1,538 days | Max \|r\| = 0.036 | CoinMetrics flow methodology captures minority of actual balance movements. Measurement gap is structural, not resolvable with different aggregation. |
| Daily reserve change → price | Cross-correlation lags -5 to +5, 1,538 days | Max \|r\| = 0.044 | Even direct balance observation (bypassing flow measurement) shows no signal. The unmeasured component also doesn't carry signal. |
| Within-epoch flow-price correlation | Pearson correlation per epoch, 11 epochs | Max \|r\| = 0.17 | Weak even within regimes. No epoch shows dominant flow-price relationship. |
| ETH-denominated borrow change during crashes | Appeared to show leverage increasing | Denomination artifact | Mechanical price effect: ETH-equivalent of constant USD debt doubles when price halves. USD borrow change is the truthful measure. Residual negative in 5/6 crashes. |
| stETH event count as composition signal | 44% of real events in 2025_q4_chop | Dust artifact | 2,538 events = 11.1 stETH total ($33K). Median 0.002 stETH ($6). Noise from dust farming, not structural signal. |

## Composite Signal: What Could Be Constructed

The individual signals don't combine into a clean predictive composite, but they define a **system state assessment framework**:

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
- **Components:** Daily DefiLlama borrow pull, time-since-last-crash tracker, utilization monitor
- **Why:** The dynamics findings describe how the system behaves. A pipeline would track *where we are now* in the recharge cycle.
- **Status:** The monitoring system from the flow phase already tracks liquidation episodes. Adding borrow level and utilization from DefiLlama would complete the state picture.

### Option C: Pivot to different research direction
- **What:** The dynamics phase answered the "how does money flow" question. The remaining open threads (phantom lifecycle, 2024 anomaly, HF distributions) are refinements, not new questions.
- **Possible pivots:** Liquidator ecosystem analysis (who extracts value from stress events), cross-protocol cascade modeling (Aave → Compound → Maker ordering), or real-time oracle risk monitoring (extending the CAPO findings).

### Recommendation
Option B is the highest-return next step. The dynamics findings are structural and won't change much with more data. A real-time state tracker that says "system is X% recharged, utilization at Y%, borrow at $Z" would make the findings operationally useful. Option A (snapshots) is worth doing if a specific question demands it, but not as a broad multi-epoch pull.
