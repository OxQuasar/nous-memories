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

## 1. Operational Prototype (Next Priority)

### Components
1. **Regime tracker:** Sign of trend_8h × sign of trend_48h → 2-bit macro regime (bear/reversal/pullback/bull)
2. **Exit monitor:** At regime transition, read trend_1h and trend_8h → logistic model → P(favorable exit)
3. **Dashboard:** Current regime, time in regime, trend_8h level, exit probability

### Architecture
- Input: live 5-min BTC price → compute OLS trend at 1h, 8h, 48h rolling windows
- State: 2-bit macro regime from trend_8h sign × trend_48h sign
- Transition: detected when either trend_8h or trend_48h crosses zero
- Output: regime label + exit quality when transition occurs

### Production model

**Trend computation:** OLS slope of rolling window of period duration, divided by mean price in window → fractional rate per bar. E.g., trend_8h = OLS slope through last 96 5-min bars, normalized. See `data/download_btc.py` for implementation.

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

### What the prototype tests
- Does the 2-bit regime tracker produce clean transitions in live data?
- Does trend_8h zero-crossing reliably mark transition events?
- Any boundary flickering that would motivate HMM?
- Forward validation: do exit predictions match outcomes?

---

## 2. Live Forward Test (Post-Feb 2026 BTC)

True forward OOS on data not available during any analysis phase. Even 30 days (~150 episodes) is informative.

**This is running implicitly once the prototype is built.** The prototype generates live validation data.

Key metrics to track:
- Regime sequence: does it follow the directed cycle?
- Structural zero violations: any forbidden transitions?
- Exit prediction accuracy: binned P(bull) vs actual at C2 and C1
- trend_8h decision boundary: stable near zero?

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

1. **Operational prototype** → live regime tracking + exit signal (can build now)
2. **Live forward test** → runs automatically once prototype deployed
3. **Multi-asset** → when data available, confirms portability

Item 1 can proceed immediately. Item 2 is implicit. Item 3 is blocked on data acquisition.
