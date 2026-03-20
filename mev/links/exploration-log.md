# Links — Exploration Log

## Iteration 1: TradFi Data Pull + Initial Crash Analysis

### What was built
- `pull_tradfi.py` — pulls 7 yfinance tickers (S&P 500, VIX, USD/JPY, DXY, 10Y yield, gold, BTC) and 3 FRED series (fed funds, yield spread, CPI), merges with existing ETH daily price
- `data/tradfi_daily.csv` — 1539 rows, 2022-01-01 → 2026-03-19, 12 data columns + date index
- 2 NaN rows (Jan 1-2 2022, before markets opened), otherwise fully populated via forward-fill
- ETH prices verified exact match against source `../data/eth_price.csv` (6 spot checks across range)

### What was measured

**Crash epoch drawdowns (peak-to-trough within window):**

| Crash | ETH | BTC | S&P | ETH/BTC mult | VIX peak |
|-------|-----|-----|-----|-------------|----------|
| Terra/3AC (May-Jul 2022) | -66.6% | -52.1% | -14.7% | 1.28x | 34.8 |
| FTX (Nov-Dec 2022) | -32.6% | -25.8% | -8.8% | 1.26x | 26.1 |
| Yen carry (Jul-Aug 2024) | -33.3% | -20.9% | -8.5% | 1.59x | 38.6 |
| 2025 crash (Jan-Apr 2025) | -60.2% | -28.1% | -18.9% | 2.14x | 52.3 |
| 2026 crash (Jan-Feb 2026) | -44.9% | -35.3% | -2.6% | 1.27x | 21.8 |

**Liquidation intensity vs ETH/BTC underperformance (monotonic gradient):**

| Liq bucket | n | ETH/BTC daily mean | ETH excess vs BTC |
|---|---|---|---|
| None/low | 797 | +0.095% | +0.093% |
| Moderate | 588 | -0.001% | +0.014% |
| High | 77 | -0.439% | -0.410% |
| Very high | 61 | -1.080% | -1.018% |
| Extreme | 16 | -2.202% | -2.140% |

Spearman(liq_count, ETH/BTC return): r=-0.145, p=1.2e-8. Survives BTC-return control: partial r=-0.141, p=2.7e-8.

**Multi-day cumulative pressure (partial correlation controlling for BTC return):**

| Window | Spearman r | p-value |
|--------|-----------|---------|
| 1-day | -0.141 | 2.7e-8 |
| 3-day | -0.183 | 4.7e-13 |
| 5-day | -0.224 | 5.8e-19 |
| 7-day | -0.263 | 1.2e-25 |

Correlation nearly doubles from 1-day to 7-day. The ETH-specific liquidation pressure separates from broad crypto moves at longer horizons.

**Crash/calm decomposition of ETH/BTC decline:**

Total ETH/BTC log return: -0.937 (-60.8%)
- Crash days (364 days): -1.012 log return (-63.6%), 108.0% of total decline
- Calm days (1175 days): +0.075 log return (+7.7%), -8.0% of total decline
- 2025 crash alone: -0.626 log return (-46.5%), 66.8% of entire 4-year decline

**Inter-crash ETH/BTC recovery:**
- Terra trough → FTX start: +6.9%
- FTX trough → Yen carry start: -25.8% (continued declining in calm)
- Yen carry trough → 2025 start: -20.4% (continued declining in calm)
- 2025 trough → 2026 start: +77.0% (bounce from extreme oversold)

**2025 crash monthly breakdown:**
- Jan: ETH -2.1%, BTC +8.5%, ETH/BTC -9.7%, VIX avg 16.7
- Feb: ETH -29.2%, BTC -16.2%, ETH/BTC -15.6%, VIX avg 16.8
- Mar: ETH -17.2%, BTC -4.0%, ETH/BTC -13.7%, VIX avg 21.6
- Apr: ETH -5.9%, BTC +10.6%, ETH/BTC -14.9%, VIX avg 32.5

The 2025 crash started as ETH-specific rotation (Jan: BTC up, ETH down, VIX calm) before becoming macro-entangled (Mar-Apr: VIX spikes, S&P drops).

**Liquidation peaks vs price action on specific dates:**
- 2025-01-13 (192 liqs): ETH -3.5%, BTC +0.0%, S&P +0.2% — pure ETH-specific
- 2025-04-06 (1705 liqs): ETH -13.3%, BTC -6.3%, VIX 45.3 — macro-entangled
- 2026-01-31 (1293 liqs): ETH -10.2%, BTC -6.5%, VIX 17.4 — crypto-specific
- 2026-02-05 (1978 liqs): ETH -11.1%, BTC -14.1%, VIX 21.8 — BTC fell more than ETH on this peak liquidation day

### Observations (not yet tested)

- **Crash type classification:** Low VIX + low ETH/BTC mult (≈1.3x) = crypto-native (FTX, 2026). High VIX + high ETH/BTC mult (≈2x+) = macro-entangled (Yen carry, 2025). Terra sits between (crypto origin + macro backdrop).
- **Ratchet structure:** Crashes destroy ETH/BTC, calm periods partially recover, net is permanent decline. But the 2023-2024 calm-period decline (-25.8% post-FTX, -20.4% post-Yen carry) suggests non-DeFi factors also drive ETH/BTC down between crashes.
- **DeFi as amplification mechanism:** The monotonic liquidation-intensity gradient and multi-day cumulative pressure pattern are consistent with DeFi liquidation cascades creating ETH-specific sell pressure. But this has not yet been tested against Aave borrow levels or separated from the structural ETH/BTC decline trend.
- **2023-2024 calm decline competing explanations:** (a) structural rotation from BTC ETF narrative/institutional reweighting, exogenous to DeFi; (b) DeFi leverage rebuilding creates slow ETH supply pressure even without crashes. These predict different correlations with Aave borrow growth rates — testable with existing dynamics phase data.
- **ETH/BTC structural decline (0.079 → 0.031):** Whether this is DeFi-mechanical (repeated liquidation ratchet) or market-structural (BTC gaining institutional allocation) remains untested. The two mechanisms aren't mutually exclusive.

### Open questions for next iterations

- Do ETH/TradFi correlations change structurally across crash vs calm periods?
- Does Aave borrow level explain the 2023-2024 calm-period ETH/BTC decline?
- At what VIX level does ETH/S&P correlation regime shift?
- Does the ETH/BTC drawdown multiple correlate with total liquidation volume per crash?
- What is the transmission lag from macro event → ETH price → DeFi liquidation spike?
- THORChain cross-chain flow data: does flow direction differ by crash catalyst type?

## Iteration 2: Correlation Analysis

### What was built
- `correlations.py` — 5 analyses: full-period correlation matrix, 30-day rolling correlations, regime-split (crash vs calm), lead/lag cross-correlation, calm-period borrow growth test
- `data/correlation_matrix.csv` — 15×15 Pearson correlation matrix (returns + levels + DeFi variables)
- `data/rolling_correlations.csv` — 1538 rows, 10 rolling correlation series (30-day window)

### What was measured

**Full-period Pearson correlations with ETH daily return:**
- BTC return: +0.822
- S&P 500 return: +0.425
- VIX change: -0.361
- Liquidation count: -0.221
- DXY return: -0.129
- Everything else: |r| < 0.10

**Full-period Pearson correlations with ETH/BTC daily return:**
- S&P 500 return: +0.234
- VIX change: -0.202
- Liquidation count: -0.138
- Borrow change 30d: +0.039 (≈ zero)
- Total borrowed: +0.009 (≈ zero)

**Rolling ETH/S&P 30-day correlation:**
- Mean: +0.379, std: 0.220
- Range: -0.383 to +0.839
- Days with negative correlation: 62/1507 (4.1%)
- Longest negative streak: 37 days (Nov–Dec 2023, ETF anticipation rally)

**Regime-split correlations (crash n=364, calm n=1174):**

| Pair | Crash r | Calm r | Δ |
|------|---------|--------|---|
| ETH ret vs S&P ret | +0.492 | +0.376 | +0.116 |
| ETH ret vs BTC ret | +0.881 | +0.786 | +0.095 |
| ETH ret vs liq_count | -0.287 | -0.144 | -0.143 |
| ETH/BTC ret vs S&P ret | +0.315 | +0.187 | +0.128 |
| ETH/BTC ret vs liq_count | -0.167 | -0.110 | -0.058 |
| ETH/BTC ret vs total_borrowed | -0.078 | +0.038 | -0.116 |

Crash regime doubles the liquidation correlation impact and raises ETH/S&P coupling. Total_borrowed flips sign under stress (negative in crashes, near-zero in calm).

**Lead/lag cross-correlation (ETH return vs others, ±5 days):**
- All TradFi variables peak at lag=0. No daily lead/lag detected — transmission is sub-daily.
- Liquidation count: peak at lag=0 (-0.221), then persists at lag+1 (-0.216), lag+2 (-0.152), lag+3 (-0.108), lag+4 (-0.082), lag+5 (-0.071). One-directional 5-day decay — the physical timescale of protocol deleveraging, not information lag.

**VIX regime → ETH/S&P coupling (monotonic):**

| VIX quartile | Range | ETH/S&P corr | Rolling std |
|---|---|---|---|
| Q1 | 11.9–14.9 | 0.228 | 0.238 |
| Q2 | 14.9–17.8 | 0.284 | 0.167 |
| Q3 | 17.8–22.0 | 0.431 | 0.225 |
| Q4 | 22.1–52.3 | 0.512 | 0.127 |

High VIX = high coupling, both stronger and more stable.

**Rate regime → ETH/S&P coupling (monotonic but time-confounded):**

| Regime | Fed funds | ETH/S&P corr | Period |
|---|---|---|---|
| Near-zero | <0.5% | 0.550 | Jan–Apr 2022 only |
| Hiking | 0.5–3% | 0.524 | May–Sep 2022 |
| High | 3–4.5% | 0.435 | Oct 2022–Mar 2026 |
| Very-high | 4.5%+ | 0.276 | Feb 2023–Nov 2024 |

Each rate regime maps to a specific time period. Cannot separate rate effects from period effects. Lower weight than VIX finding.

**Borrow growth vs calm-period ETH/BTC (definitive null):**
- All calm periods: Spearman r=+0.007, p=0.81
- Pre-2024 calm: r=+0.004, p=0.92
- Post-2024 calm: r=+0.000, p=1.00
- All lags 1–30 days: nothing (max |r| = 0.034)

DeFi leverage rebuilding does not explain calm-period ETH/BTC decline.

**Yield spread vs total_borrowed:**
- Levels: r=0.762, p=1.7e-292
- Daily changes: r=-0.030, p=0.24
Co-symptoms of the same macro regime (expanding risk appetite), not operationally connected at any frequency.

**Pre-crash ETH/S&P decoupling:**

| Crash | 30d pre-crash ETH/S&P corr |
|---|---|
| Terra/3AC | +0.622 |
| FTX | +0.397 |
| Yen carry | +0.025 (decoupled) |
| 2025 | +0.348 |
| 2026 | +0.382 |

Only Yen carry preceded by true decoupling. But Yen carry is the only macro-origin crash — n=1 of 1 eligible cases. Crypto was selling off (ETH -14.4% in one week of early July) while S&P rose, front-running macro stress by 3-4 weeks.

### Observations updated from iteration 1

- **"DeFi as chronic drag" rejected.** Borrow growth null is definitive across all calm periods, time splits, and lags. The 2023-2024 ETH/BTC decline is market-structural (BTC ETF, institutional rotation), not DeFi-mechanical. This resolves the competing explanations from iteration 1 in favor of structural rotation.
- **"DeFi as acute amplifier" supported.** Liquidation intensity correlates monotonically with ETH-specific damage. Effect doubles during crash periods. Persists for ~5 days per cascade (protocol deleveraging timescale). Survives BTC return controls.
- **Framing update:** "Acute amplifier with weak recovery" is more precise than "ratchet." Crashes destroy ETH/BTC acutely, calm recovers only +7.7% of what crashes destroy. The permanent damage is real but comes from asymmetric recovery, not a continuous mechanism.

### Open questions carried forward

- Does the ETH/BTC drawdown multiple correlate with total liquidation volume per crash? (testable in Step 3+5)
- How many basis points of extra ETH decline per liquidation event? (Step 5 amplification quantification)
- Does the amplification mechanism differ between macro-origin and crypto-native crashes? (expected: yes, based on ETH/BTC mult divergence)
- Pre-crash ETH/S&P decoupling as early warning for macro-origin crashes — hypothesis preserved, n=1 of 1 eligible
- THORChain cross-chain flow direction during crashes — not yet pulled, lower priority

## Iteration 3: Crash Amplification Analysis (Steps 3+5 merged)

### What was built
- `amplification.py` — 6-part analysis: baseline OLS model, crash-day residuals, liquidation-conditioned residuals, amplification quantification, per-crash breakdown by catalyst type, per-crash worst-day timelines
- `data/crash_residuals.csv` — 364 rows, per-crash-day: date, crash label, ETH/BTC/S&P returns, predicted, residual, liq_count

### What was measured

**Baseline model (trained on 1172 non-crash days):**
ETH_ret = 0.0001 + 0.979·BTC_ret + 0.506·SP_ret, R²=0.631. ETH moves ~1:1 with BTC plus ~0.5x S&P sensitivity on non-crash days.

**Liquidation-conditioned model residuals (all days, not just crashes):**

| Liq bucket | n | Mean residual |
|---|---|---|
| 0 | 158 | +0.24% |
| 1-10 | 818 | +0.06% |
| 11-50 | 352 | +0.01% |
| 51-200 | 145 | -0.62% |
| 201-500 | 36 | -0.74% |
| 500+ | 27 | -1.96% |

Monotonic after controlling for BTC and S&P moves. 500+ liquidation days show ~2% daily ETH-specific underperformance.

**Amplification coefficient:**
- Linear: δ = -0.12 bps per liquidation event (p=0.008, R²=0.019)
- Log: δ = -21.6 bps per unit log-liq (p=0.002, R²=0.026)
- Concave: first 100-200 liquidations do -0.63 bps/event, 201-500 do -0.23 bps/event, 500+ do -0.22 bps/event. First wave does 3x damage per event.

**Per-crash cumulative residuals:**

| Crash | Days | Cum residual | Trough | Within-crash recovery | 60d post-crash |
|---|---|---|---|---|---|
| Terra/3AC | 92 | +4.8% | -27.2% | +32.1% | +2.2% |
| FTX | 61 | -3.1% | -8.6% | +5.5% | -4.5% |
| Yen carry | 32 | -16.7% | -19.7% | +2.9% | -13.5% |
| 2025 crash | 120 | -54.5% | -56.8% | +2.3% | +18.0% |
| 2026 crash | 59 | -13.5% | -17.5% | +4.0% | +7.4% |

**By catalyst type:**
- Macro (Terra, Yen carry, 2025): 244 days, -66.4% cumulative residual, -0.27%/day mean
- Crypto-native (FTX, 2026): 120 days, -16.6% cumulative residual, -0.14%/day mean

Macro crashes produce ~2x daily amplification and ~4x total cumulative damage vs crypto-native.

**Per-crash δ significance:** Only 2025 reaches significance individually (p=0.008). Others: Terra p=0.13, FTX p=0.07, Yen carry p=0.84, 2026 p=0.89. Expected given n=32 to n=120 per crash. Mechanism is clear in aggregate and bucketed analysis.

**Terra/3AC sub-period decomposition:**
- May: -16.3% cumulative residual (crash phase, 145 avg liqs/day)
- June: -10.0% cumulative residual (continued cascade, 196 avg liqs/day)
- July: +31.2% cumulative residual (oversold bounce/reversal, 62 avg liqs/day)
- Aggregate +4.8% entirely from July recovery exceeding May-June damage

**2025 crash monthly residuals:**
- Jan: -11.2% residual, only 18 liqs/day. Model predicted +11.5% (BTC +8.5%), actual +0.3%. Pure non-DeFi ETH-specific rotation.
- Feb: -18.4% residual, 120 liqs/day. Liquidation cascade fires.
- Mar: -12.4% residual, 134 liqs/day. Macro stress joins (VIX rising).
- Apr: -12.5% residual, 205 liqs/day. Peak liquidations during *rising* market (+2.1% actual vs +14.6% predicted). Recovery suppression.

**2026 weekly pattern — damage peaks before liquidation peaks:**
- W4 (Jan 19): -9.0% residual, 24 liqs/day — damage starting
- W5 (Jan 26): -10.0% residual, 282 liqs/day — cascade fires
- W6 (Feb 2): +3.5% residual, 606 liqs/day — peak liquidations, exhaustion/reversal

**Worst 7-day residual windows per crash:**
- Terra: -14.0% (ending May 27)
- FTX: -6.0% (ending Nov 20)
- Yen carry: -12.6% (ending Aug 9)
- 2025: -17.5% (ending Feb 7)
- 2026: -13.8% (ending Feb 4)

### Structural findings

**Three modes of DeFi/crash interaction (verified):**

1. **Ramp-phase amplification:** First 100-200 liquidations per day do maximum marginal damage (-0.63 bps/event). Operates on 5-7 day timescale. The damage is done during the liquidation ramp, not at the peak. 2026 W4-W5 show -19% cumulative residual while W6 (peak liqs) shows +3.5%.

2. **Recovery suppression:** Ongoing deleveraging prevents ETH from participating in BTC+S&P bounces. April 2025: prices rising (+2.1% ETH), but model residual is -12.5% because the system is still unwinding with 205 liqs/day. This mode can persist for weeks/months.

3. **Exhaustion reversal:** Once forced selling completes, ETH bounces disproportionately. Terra July: +31.2% residual recovery from -27.2% trough. Requires a clean break — a period where no new selling pressure enters.

**Permanent damage comes from crash-chaining:** When crashes chain faster than mode 3 can complete (Yen carry → 2025 rotation → 2025 cascade), recovery windows never open and amplification damage accumulates permanently. This is the structural mechanism behind crash days = 108% of long-term ETH/BTC decline.

**Causal ordering — DeFi is never the first mover:**
- Terra: UST collapse (primary) → DeFi cascade (amplifier)
- FTX: CEX insolvency (primary) → mild DeFi response (amplifier, small)
- Yen carry: Macro unwind (primary) → DeFi cascade (amplifier)
- 2025: ETH-specific rotation in Jan (primary, not DeFi) → DeFi cascade Feb-Apr (amplifier) → macro stress joins Mar-Apr (tertiary)
- 2026: Crypto-wide selloff (primary) → DeFi cascade (amplifier)

In all five crashes, DeFi amplifies a primary catalyst it did not create.

### Open questions

- **2025 January rotation cause:** -11.2% residual with 18 liqs/day. Something sold ETH specifically while BTC rallied. Not DeFi, not macro, not correlation-regime driven (VIX=16.7). Candidates: institutional rebalancing out of ETH into BTC, ETH narrative weakness (L2 fragmentation, Solana competition). This is the trigger for the worst crash in the dataset.
- **Recovery completeness:** Terra's +32.1% within-crash reversal is an outlier. Other crashes show only 2-5% within-window recovery. Does the recovery timescale depend on crash depth, duration, or subsequent market conditions? 2025 shows +18% recovery in 60 days post-crash — substantial but still leaves -36.5% unreversed.
- **Yen carry post-crash anomaly:** -13.5% residual in 60 days *after* the crash ended. Only crash with negative post-window residual. Possibly because it transitioned directly into the ETH-specific rotation that became the 2025 crash — the system never got a clean break.
- **THORChain cross-chain flow direction during crashes** — not yet pulled, would add directional color (flight-to-stables vs BTC rotation vs exit)
- **Pre-crash ETH/S&P decoupling** — preserved as hypothesis, n=1 of 1 eligible macro-origin cases

## Iteration 4: Findings Synthesis + Review Corrections

### What was built
- `findings.md` — 8-section synthesis document covering all Links phase results

### Review corrections applied
1. Section 2: "80× swing" corrected to "~8× ratio and 2.20 percentage point swing"
2. Section 2: Added R² caveat (0.019–0.026) — Aave liquidation count explains ~2% of residual variance, is a proxy for total forced selling, total DeFi amplification likely larger
3. Section 4 Terra narrative: Added note that concurrent Fed rate-hiking cycle (VIX 34.8) prevented broader market from absorbing the shock — hybrid crypto-native/macro classification
4. Section 6: Header changed from "DeFi is never the first mover" to "Aave liquidation cascades are never the first mover." Added note that DeFi broadly (UST stablecoin) did initiate Terra — claim is specifically about lending liquidation cascades as second-order amplifier

### Status
Core plan questions answered:
- "Does DeFi amplify or dampen crashes?" — Amplifies, quantified with three-mode framework
- "What's the transmission path?" — Sub-daily macro→crypto, 5-7 day DeFi cascade timescale, Aave lending cascades never initiate
- "What connects external events to DeFi cascades?" — VIX determines coupling regime (monotonic), crash-chaining prevents recovery

Remaining plan items not executed:
- Step 1b (THORChain data pull) — supplementary, core questions answered without it
- Step 4 (regime analysis details) — VIX regime finding from Step 2 already answers core regime question, rate regime is time-confounded
