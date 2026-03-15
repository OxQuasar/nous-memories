# Next Steps: Regime Model Development

## Current State — Research Complete (15 phases)

4-regime directed cycle validated across BTC (IS + 2yr OOS + 21-day forward crash) and ETH (7.5 months). BTC production coefficients transfer cross-asset (AUC 0.994/0.998 on ETH). Research phase is done. Remaining work is engineering + forward time accumulation.

### Production Model

**Regime detection:** 2-bit macro (sign of trend_8h × sign of trend_48h)

| Macro | trend_8h | trend_48h | Regime |
|-------|----------|-----------|--------|
| 0 | − | − | Bear |
| 1 | + | − | Reversal |
| 2 | − | + | Pullback |
| 3 | + | + | Bull |

**Trend computation:** OLS slope of rolling window of period duration, divided by mean price → fractional rate per bar (~1e-5 magnitude). Simulator uses `NormalizedTrendAndVolatility` in `~/henry/callandor/calcs.go`.

**Exit scoring (Phase 13, fit on BTC OOS 2023-2024):**
```
C2 Pullback: P(bull) = σ(5.209 + 1477 × trend_1h + 348533 × trend_8h)
C1 Reversal: P(bt)   = σ(−4.890 + 3138 × trend_1h + 421505 × trend_8h)
```
Decision boundaries: C2 at trend_8h ≈ −0.000015, C1 at trend_8h ≈ +0.000012.

---

## TODO

### 1. Production Scoring

The model labels regimes and scores exits — it does not generate trading signals. Three metrics track whether it's working on live data:

**Metric 1: Topology violations (count)**
Count forbidden transitions: C0→C3, C3→C0, C1→C2, C2→C1. Expected: 0. Multiple violations in a short window = topology breaking.

**Metric 2: Exit AUC (rolling)**
At every C2 and C1 exit, record (trend_1h, trend_8h, P(favorable), actual outcome). Compute rolling AUC over trailing 100 exits.

| AUC | Status |
|-----|--------|
| > 0.90 | Working |
| 0.85–0.90 | Monitor |
| 0.80–0.85 | Investigate |
| < 0.80 | Stop using exit scores |

**Metric 3: Calibration (binned)**
Bin predictions: <0.10, 0.10–0.50, 0.50–0.90, >0.90. Model is bimodal — >95% should fall in extreme bins, actuals within ±10pp of predicted.

**When to refit:** AUC < 0.85 on rolling 100, or calibration drifts >15pp in extreme bins. Refit on most recent 6 months. Topology (2-bit) should never need changing.

### 2. Simulator Integration

Wire regime labels and exit scores into the trading simulator. The simulator handles per-second data ingestion — the regime model feeds it regime state and exit scores at transitions (~5 per day).

### 3. Forward Calibration

Accumulate 30+ days of live data for calibration-level validation (150+ episodes, ~40 C2 and C1 exits each). Phase 14 confirmed topology on 21 days (n=74) but that's below minimum for exit score validation.

### 4. Additional Assets (Deferred)

**PENGU:** Tests boundary invariance across different vol profiles. C2 boundary was near-invariant BTC↔ETH (3% difference) but both have similar fractional vol.

**Traditional markets (SPY, QQQ):** Different microstructure (market hours, gaps). Topology likely holds. Complement symmetry may weaken (volatility asymmetry). Time-invariance will likely break (session effects).

### 5. Failure Clustering (Deferred)

Do high-confidence C2 failures (1-3% at P>0.9) cluster in time? Operational risk characterization for position sizing.

### 6. HMM (Contingent)

Only if operational use reveals systematic boundary flickering at trend_8h ≈ 0 or trend_48h ≈ 0 that degrades regime labeling.

---

## DONE

### OOS Validation (Phase 12) — TOP TIER PASS
K=4 (gap=0.151), identical structural zeros, complement symmetry (JSD=0.007), cross-domain AUC 0.957 (C2) / 0.980 (C1). 2,947 episodes on BTC 2023-2024.

### Coefficient Refit (Phase 13)
Production coefficients in price-normalized units. Fit on BTC OOS 2023-2024.

### C1 Thin-n (Phase 12)
155 breakthroughs in OOS (was 43 IS). Return +1.08% confirmed. Asymmetry ratio 3.95.

### Binary vs Continuous (Phase 11)
Binary S5/S4 signal environment-dependent (gap collapsed 42.6pp → 14.1pp OOS). Continuous trend_8h model stable. Binary deprecated.

### 3-bit vs 2-bit Regime Detection (Phase 13)
trend_1h flips every ~55 minutes on raw data, creating noisy micro-episodes. Macro regime is trend_8h × trend_48h (2-bit). trend_1h enters only as logistic predictor at exit.

### Forward Topology (Phase 14) — PASS
K=4, structural zeros, directed cycle confirmed on 21-day BTC crash (n=74). Below minimum for exit score validation.

### ETH Cross-Asset (Phases 14-15) — CONFIRMED
860 episodes. All 4 hierarchy rungs pass. BTC→ETH coefficient transfer AUC 0.994 (C2) / 0.998 (C1) — outperforms ETH's own fit. Asymmetry ratio 3.87. C2 boundary near-invariant (−1.44e-5 vs −1.49e-5). C1 boundary asset-specific (2.3× different, use as binary go/no-go only).

### Ambiguous Zone (Phase 15) — CLOSED
3-4 episodes in [0.2, 0.8] range on both assets. Bimodal separation confirmed. AUC is mechanical state-reading of clean bifurcation.

### IS Normalization (Phase 13 + simulator fix)
Simulator now uses `NormalizedTrendAndVolatility` for price trends (slope / mean price → fractional rate), matching `download_btc.py`. IS datalog regenerated with consistent units.
