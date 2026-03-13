# Next Steps: Regime Model Development

## Current State

Discovery (11 phases) + OOS validation (Phase 12) + production refit (Phase 13) complete.

- 4-regime directed cycle: **OOS-validated** on 2 years of BTC 2023-2024 (2,947 episodes)
- All topological invariants confirmed: K=4, structural zeros, complement symmetry (JSD 0.007)
- Exit prediction: **cross-domain AUC 0.957 (C2), 0.980 (C1)** — top tier
- Returns confirmed: C1 breakthrough +1.08% OOS vs +1.09% IS, asymmetry ratio 3.95
- Production coefficients fitted on raw-scale OOS data (Phase 13)
- Regime detection refined: **2-bit macro (trend_8h × trend_48h)**, not 3-bit trigram

---

## Resolved Questions

### ~~OOS Validation~~
**RESOLVED — TOP TIER PASS (Phase 12).**

| Criterion | Result | Status |
|-----------|--------|--------|
| K=4 topology | K=4, gap=0.151 | ✓ |
| Structural zeros | Identical pattern | ✓ |
| Complement symmetry | JSD = 0.007 | ✓ |
| C2 AUC > 0.85 | 0.957 | ✓ TOP TIER |
| C1 AUC > 0.85 | 0.980 | ✓ TOP TIER |

### ~~Coefficient Refit~~
**RESOLVED (Phase 13).** Production coefficients in raw OLS slope units. See findings.md §11.

### ~~C1 Thin-n~~
**RESOLVED.** 155 breakthroughs in OOS (was 43 IS). Return +1.08% confirmed.

### ~~Binary vs Continuous~~
**RESOLVED.** Binary signal environment-dependent. Continuous trend_8h model stable. Binary is discovery tool only.

### ~~3-bit vs 2-bit Regime Detection~~
**RESOLVED (Phase 13).** On raw-scale data, trend_1h flips every ~55 minutes, creating ~21K noisy micro-episodes. The macro regime is medium × slow alignment (trend_8h × trend_48h = 2-bit). This gives ~2,950 episodes at ~5.9h mean duration — matching IS perfectly. trend_1h enters only as a logistic predictor at exit, not as a regime determinant.

---

## 1. Forward Validation (Next Priority)

Python batch script on post-Feb 2026 BTC data. No dashboard, no real-time — just grade the model.

### What it does
1. Compute OLS trends (1h, 8h, 48h) on 5-min bars
2. Detect regime transitions from 2-bit macro (trend_8h sign × trend_48h sign)
3. At each transition, record: regime, trend_1h, trend_8h, logistic P(favorable), actual outcome
4. After the run, grade against rubric

### Production model

**Trend computation:** OLS slope of rolling window of period duration, divided by mean price in window → fractional rate per bar. See `data/download_btc.py`.

**C2 Pullback Exit:**
```
P(bull) = σ(5.209 + 1477 × trend_1h + 348533 × trend_8h)
Decision boundary: trend_8h ≈ −0.000015
```

**C1 Reversal Exit:**
```
P(bt) = σ(−4.890 + 3138 × trend_1h + 421505 × trend_8h)
Decision boundary: trend_8h ≈ +0.000012
```

### Grading rubric

| Grade | Criteria |
|-------|----------|
| A | Zero topology violations, calibration within ±10pp per bin, decision boundary stable |
| B | ≤2 topology violations, calibration within ±15pp, boundary shifted but direction correct |
| C | Topology holds but exit signal degraded (AUC <0.80 or calibration off >20pp) |
| F | Topology violations >5%, or K≠4 on live data |

A or B → proceed to simulator integration for live trading. C → regime tracking only. F → stop.

### Minimum data
30 days (~150 episodes, ~40 C2 exits, ~40 C1 exits). Enough for topology, marginal for calibration. 90 days would be solid.

---

## 2. Simulator Integration (If Grade A/B) 

Once forward validation passes, integrate the regime model into the existing trading simulator. The simulator handles per-second data ingestion and order execution — the regime model feeds it conviction signals at regime transitions (~5 per day).

---

## 3. Multi-Asset Validation (Deferred)

### 3a. Crypto (ETH, SOL)
Same market microstructure, different assets. Tests whether the regime cycle is a property of crypto markets or BTC specifically.

**Key question:** Do transition probabilities match BTC, or just topology? Topology match with different probabilities is still a win — framework portable, parameters asset-specific.

**Data needed:** ETH/SOL 5-min OHLCV, 6+ months. Can use `data/download_btc.py` adapted for other symbols.

### 3b. Traditional markets (SPY, QQQ) (Deferred)
Different microstructure (market hours, no 24/7 trading). Tests whether complement symmetry and directed cycle survive session boundaries.

**Expectation:** Topology likely holds. Complement symmetry may weaken (volatility asymmetry stronger in equities). Time-invariance will likely break (session open/close effects).

---

## 4. Contingent Next Steps

### 4a. HMM (if 2-bit regime tracking fails operationally)
Motivated only if operational prototype reveals:
- Systematic boundary flickering at trend_8h ≈ 0 or trend_48h ≈ 0
- Detection latency vs a continuous model
- Smooth transition zones that the binary model misclassifies

### 4b. IS Normalization Recovery
If the IS data normalization recipe can be recovered, enables:
- Direct threshold comparison (was the bifurcation boundary invariant?)
- Combined IS+OOS logistic fit for maximum sample size
- Not blocking — OOS-only refit is sufficient for deployment

---

## Priority Order

1. **Forward validation** → Python batch on post-Feb 2026 data, grade against rubric
2. **Simulator integration** → if grade A/B, wire regime signals into trading simulator
3. **Multi-asset** → when data available, confirms portability

Item 1 needs post-Feb 2026 BTC data (download with `data/download_btc.py`). Item 2 gates on item 1. Item 3 is independent.
