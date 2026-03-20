# Links — How External Events Connect to DeFi Liquidation Cascades

## 1. Summary

DeFi liquidation cascades amplify crashes they did not initiate. After controlling for BTC and S&P 500 moves, each 100 liquidation events produce ~100 bps of additional ETH-specific decline, with the first events doing 3× the marginal damage of later ones. The amplification operates on a 5–7 day timescale, doubles in crash regimes, and is responsible for crash days contributing 108% of ETH/BTC's total 4-year decline (calm periods net +7.7%). DeFi leverage does not cause chronic ETH/BTC decay — that is structural/narrative — but it makes every crash worse and prevents full recovery between them.

## 2. The Amplification Mechanism

### Baseline model

Trained on 1,172 non-crash days:

```
ETH_ret = 0.0001 + 0.979·BTC_ret + 0.506·SP_ret    (R² = 0.631)
```

ETH moves nearly 1:1 with BTC and adds ~0.5× S&P sensitivity. Residuals from this model on crash days measure ETH-specific damage beyond what broad market moves explain.

### Liquidation-conditioned residuals

Model residuals bucketed by daily Aave liquidation count (all 1,536 days):

| Liq count | n | Mean residual | Interpretation |
|-----------|---|---------------|----------------|
| 0 | 158 | +0.24% | ETH outperforms |
| 1–10 | 818 | +0.06% | Neutral |
| 11–50 | 352 | +0.01% | Neutral |
| 51–200 | 145 | −0.62% | Amplification begins |
| 201–500 | 36 | −0.74% | Strong amplification |
| 500+ | 27 | −1.96% | Severe amplification |

The gradient is monotonic after controlling for BTC and S&P moves. Days with 500+ liquidations show ~2% daily ETH-specific underperformance — a ~8× ratio and 2.20 percentage point swing from zero-liquidation days.

### Amplification coefficient

Crash-day regressions of model residual on liquidation count:

- **Linear:** δ = −0.12 bps per event (p = 0.008)
- **Log:** δ = −21.6 bps per unit log(1 + liq_count) (p = 0.002, better fit)

The log model's superiority confirms concavity. Bucketed marginal impact:

| Bucket | Marginal impact per event |
|--------|--------------------------|
| First 100–200 | −0.63 bps/event |
| 201–500 | −0.23 bps/event |
| 500+ | −0.22 bps/event |

First-wave liquidations do 3× the per-event damage.

**Important caveat:** The R² of these regressions is low (0.019 linear, 0.026 log) — Aave liquidation count explains only ~2% of residual variance. Aave liquidations are a proxy for total forced selling, not a comprehensive measure. Other channels (DEX selling, CEX liquidations, market maker de-risking) are not captured. The "100 bps per 100 liquidations" figure is Aave-specific; total DeFi-related amplification is likely larger.

### Multi-day cascade timescale

Partial Spearman correlation of liquidation count with ETH/BTC return (controlling for BTC return):

| Window | Spearman r | p-value |
|--------|-----------|---------|
| 1-day | −0.141 | 2.7e-8 |
| 3-day | −0.183 | 4.7e-13 |
| 5-day | −0.224 | 5.8e-19 |
| 7-day | −0.263 | 1.2e-25 |

Correlation nearly doubles from 1-day to 7-day. This is the physical timescale of protocol deleveraging — each day's liquidations add to the ongoing sell pressure, and the cumulative effect is what creates ETH-specific damage at longer horizons.

Cross-correlation at the daily level: liquidation count peaks at lag 0 (r = −0.221), then decays: lag+1 (−0.216), lag+2 (−0.152), lag+3 (−0.108), lag+4 (−0.082), lag+5 (−0.071). This is one-directional decay, not bidirectional — confirming it's the physical deleveraging timeline, not information lag.

## 3. Three Modes of DeFi/Crash Interaction

### Mode 1: Ramp-phase amplification

The first wave of liquidations does maximum damage. By the time liquidation count peaks, the marginal ETH-specific damage is already exhausted.

**2026 weekly pattern:**

| Week | Cumulative residual | Mean liqs/day |
|------|-------------------|---------------|
| W4 (Jan 19) | −9.0% | 24 |
| W5 (Jan 26) | −10.0% | 282 |
| W6 (Feb 2) | +3.5% | 606 |

Damage concentrates in W4–W5 (ramp), while W6 (peak liquidations at 606/day) shows *positive* residual — the system is already reversing. The −0.63 bps/event for the first 100–200 events vs −0.22 for 500+ is the quantitative basis.

### Mode 2: Recovery suppression

Ongoing deleveraging prevents ETH from participating in BTC and S&P bounces.

**April 2025:** Actual ETH return was +2.1%, but the model predicted +14.6% (BTC +10.6%, S&P recovering). Residual: −12.5%. Mean 205 liquidations/day — the system was still unwinding even as markets recovered. This mode can persist for weeks to months.

### Mode 3: Exhaustion reversal

Once forced selling completes, ETH bounces disproportionately. Requires a clean break where no new selling pressure enters.

**Terra July 2022:** +31.2% cumulative residual recovery, from a trough of −27.2%. Liquidations dropped to 62/day (from 145–196 in May–June). The system exhausted its sellable collateral.

### When permanent damage occurs

When crashes chain faster than Mode 3 can complete, recovery windows never open. The Yen carry crash (Aug 2024) showed only +2.9% within-window recovery, then transitioned directly into the 2025 rotation that became the worst crash in the dataset. Post-Yen-carry 60-day residual was −13.5% — the only crash with continued deterioration after its window ended.

This crash-chaining mechanism — not a continuous process — is why crash days account for 108% of ETH/BTC's 4-year decline while calm days net +7.7%.

## 4. Crash-by-Crash

| Crash | Catalyst | VIX peak | ETH drawdown | ETH/BTC mult | Cum residual | Worst 7d | Mean liqs/day |
|-------|----------|----------|-------------|-------------|-------------|---------|--------------|
| Terra/3AC | crypto-native → macro | 34.8 | −66.6% | 1.28× | +4.8% | −14.0% | 134 |
| FTX | crypto-native | 26.1 | −32.6% | 1.26× | −3.1% | −6.0% | 19 |
| Yen carry | macro | 38.6 | −33.3% | 1.59× | −16.7% | −12.6% | 105 |
| 2025 crash | rotation → macro | 52.3 | −60.2% | 2.14× | −54.5% | −17.5% | 118 |
| 2026 crash | crypto-native | 21.8 | −44.9% | 1.27× | −13.5% | −13.8% | 126 |

**Aggregate by catalyst type:**
- Macro-origin (Terra, Yen, 2025): 244 days, −66.4% cumulative residual, −0.27%/day, 122 liqs/day average
- Crypto-native (FTX, 2026): 120 days, −16.6% cumulative residual, −0.14%/day, 72 liqs/day average

Macro crashes produce ~2× daily amplification rate and ~4× cumulative damage vs crypto-native.

### Per-crash narratives

**Terra/3AC (May–Jul 2022):** UST collapse triggered the cascade, but the concurrent Fed rate-hiking cycle (VIX 34.8 — higher than FTX or 2026) prevented the broader market from absorbing the shock, making this a hybrid crypto-native/macro event. May: −16.3% cumulative residual with 145 liqs/day. June: −10.0% residual, 196 liqs/day (cascade continues). July: +31.2% residual recovery, 62 liqs/day (exhaustion reversal). The aggregate +4.8% cumulative residual is misleading — it nets severe amplification against a large recovery. Worst single day: May 26, −7.9% residual with 325 liquidations.

**FTX (Nov–Dec 2022):** CEX insolvency caused mild DeFi response. Only 19 liqs/day average — the damage was mostly on centralized venues. ETH tracked BTC closely (1.26× drawdown multiple, lowest in dataset). Cumulative residual −3.1% — smallest amplification.

**Yen carry (Jul–Aug 2024):** Macro-origin. USD/JPY unwound → global equities sold → ETH cascade. Initial shock preceded liquidations: Jul 25 showed −5.1% residual with only 27 liquidations. Aug 4: 389 liquidations as cascade fires. Only +2.9% within-window recovery. Post-window 60-day residual: −13.5% — this crash transitioned directly into the conditions that triggered 2025.

**2025 crash (Jan–Apr 2025):** The worst crash in the dataset. Started as ETH-specific rotation in January: BTC +8.5%, ETH −2.1%, VIX 16.7 — model predicted +11.5%, actual +0.3%. January residual: −11.2% with only 18 liqs/day. Not DeFi, not macro, not identifiable in any measured variable. February: liquidation cascade fires (120 liqs/day, −18.4% residual). March: macro stress joins (VIX rising to 21.6, −12.4% residual). April: recovery suppression — market rising but ETH trails by 12.5% with 205 liqs/day. Worst single day: Apr 6, −7.15% residual with 1,705 liquidations.

**2026 crash (Jan–Feb 2026):** Crypto-native selloff. VIX peaked at 21.8 (below the 30 macro threshold). Demonstrates the ramp-phase pattern clearly: W4 damage (−9.0% residual, 24 liqs/day) → W5 cascade (−10.0%, 282 liqs/day) → W6 exhaustion (+3.5%, 606 liqs/day). Peak liquidation day (Feb 5, 1,978 events) saw BTC fall more than ETH — the cascade was already dissipating.

## 5. Correlation Regimes

### VIX regime drives ETH/S&P coupling

ETH/S&P 500 30-day rolling correlation bucketed by VIX level:

| VIX quartile | Range | ETH/S&P corr | Rolling std |
|---|---|---|---|
| Q1 | 11.9–14.9 | 0.228 | 0.238 |
| Q2 | 14.9–17.8 | 0.284 | 0.167 |
| Q3 | 17.8–22.0 | 0.431 | 0.225 |
| Q4 | 22.1–52.3 | 0.512 | 0.127 |

Monotonic in both level and stability. At high VIX, ETH/S&P coupling is both stronger (+0.51) and more predictable (std 0.13). At low VIX, crypto partially decouples from equities and the relationship is unstable.

### Rate regime (time-confounded)

Fed funds rate vs ETH/S&P correlation:

| Regime | Fed funds | ETH/S&P corr | Period |
|---|---|---|---|
| Near-zero | <0.5% | 0.550 | Jan–Apr 2022 |
| Hiking | 0.5–3% | 0.524 | May–Sep 2022 |
| High | 3–4.5% | 0.435 | Oct 2022–Mar 2026 |
| Very-high | 4.5%+ | 0.276 | Feb 2023–Nov 2024 |

Each rate regime maps to a specific time period. The monotonic pattern (higher rates → lower coupling) could equally reflect market maturation, BTC ETF effects, or rate-environment effects. Cannot disentangle with this data. Lower confidence than the VIX finding.

### Rolling ETH/S&P dynamics

- Mean: +0.379, range: −0.383 to +0.839
- Days with negative correlation: 62/1,507 (4.1%)
- Longest negative streak: 37 days (Nov–Dec 2023), coinciding with BTC ETF anticipation rally — crypto-specific catalyst decoupled ETH from equities temporarily

### Borrow growth null (definitive)

Spearman correlation between calm-period ETH/BTC daily return and 30-day borrow growth:

| Period | Spearman r | p-value | n |
|---|---|---|---|
| All calm | +0.007 | 0.81 | 1,145 |
| Pre-2024 | +0.004 | 0.92 | 547 |
| Post-2024 | +0.000 | 1.00 | 598 |
| Lagged 1–30d | max |r| = 0.034 | all p > 0.25 | — |

DeFi leverage rebuilding does not explain calm-period ETH/BTC decline. The chronic ETH/BTC decay (0.079 → 0.031 over 4 years) is market-structural, not DeFi-mechanical.

## 6. Causal Ordering

### Aave liquidation cascades are never the first mover

Across all five crashes, the primary catalyst was external to Aave lending liquidation cascades. Note: DeFi broadly defined did initiate Terra/3AC — the UST algorithmic stablecoin was a DeFi mechanism. The claim here is specifically that Aave-style lending liquidation cascades are a second-order amplifier, not an initiating cause:

| Crash | Primary catalyst | DeFi role | Evidence |
|---|---|---|---|
| Terra/3AC | UST algorithmic stablecoin collapse | Amplifier | Liquidation cascade follows stETH depeg |
| FTX | CEX insolvency | Mild amplifier | Only 19 liqs/day — damage on centralized venues |
| Yen carry | USD/JPY unwind → global equity selloff | Amplifier | Jul 25: −5.1% residual with 27 liqs (shock precedes cascade) |
| 2025 | ETH-specific rotation (Jan), then macro (Mar–Apr) | Amplifier (Feb–Apr) | Jan: 18 liqs/day, −11.2% residual. Feb: 120 liqs/day |
| 2026 | Crypto-wide selloff | Amplifier | W4 damage precedes W5–W6 liquidation peak |

### The 2025 January mystery

January 2025 produced −11.2% cumulative residual with only 18 liquidations/day. The model predicted ETH should have risen 11.5% (BTC +8.5%, S&P flat). Something sold ETH specifically while BTC rallied, VIX was calm at 16.7, and DeFi had minimal liquidation activity. This is the initial trigger for the worst crash in the dataset and is not explained by any variable in our model. Candidates: institutional rebalancing from ETH to BTC, ETH narrative deterioration (L2 fragmentation, Solana competition). Not tested.

### Transmission timescales

- **Macro → crypto price:** Sub-daily. All TradFi variables peak at lag 0 in daily cross-correlation. The S&P/VIX/DXY signals reach ETH within the same trading day.
- **Price drop → DeFi cascade:** 1–7 days. Liquidation count cross-correlation persists from lag 0 (r = −0.221) through lag+5 (r = −0.071). The partial correlation strengthening from 1-day (r = −0.141) to 7-day (r = −0.263) confirms multi-day accumulation.
- **Cascade exhaustion → recovery:** Variable. Terra: ~30 days (May damage → July reversal). 2025: 60+ days post-window for +18% recovery. Yen carry: no recovery — chained into next crash.

## 7. Connection to Prior Phases

**Flow phase** established that perpetual funding rate leads Aave lending liquidations by ~37 hours. This phase confirms the broader pattern: external catalysts → price action → DeFi response, with DeFi operating on a multi-day (5–7 day) timescale for the full cascade. The 37h perp→lending lead fits within the first day of the 1–7 day cascade window measured here.

**Position phase** decomposed Aave collateral into real and phantom components and mapped conditional liquidation fuel by price level. This phase quantifies what happens when that fuel ignites: ~100 bps of extra ETH decline per 100 liquidation events, concave, with first events doing 3× marginal damage. The position phase's ETH-denominated collateral concentration explains *why* liquidations create ETH-specific sell pressure that the amplification model captures as negative residuals.

**Correlation phase** documented the CAPO oracle architecture and the March 10 incident. Oracle design determines *which* positions become liquidatable at a given price level — a confound not separated in this phase's amplification model. The measured δ coefficient aggregates both market-risk liquidations and oracle-design-driven liquidations.

**Dynamics phase** established the recharge cycle (borrow rebuilds → crash depletes → rebuild) and crash/recovery asymmetry. This phase adds the external dimension: the recharge cycle's crash phase is triggered by external catalysts (never DeFi-internal), amplified by DeFi mechanics, and resolved by exhaustion. The dynamics phase's finding that recovery takes 2–4× longer than collapse maps to Mode 2 (recovery suppression) identified here.

## 8. Open Questions

**2025 January rotation trigger.** The −11.2% residual with 18 liqs/day is the largest unexplained signal in the dataset. Identifying the cause would explain what initiated the worst crash episode. Institutional flow data (not available in our dataset) would be needed.

**Recovery completeness determinants.** Terra's +32.1% within-crash reversal vs other crashes' 2–5% is a 6–16× outlier. What determines whether Mode 3 (exhaustion reversal) produces full recovery? Candidates: crash depth, subsequent market direction, time before next crash. Not systematically tested.

**Oracle architecture as amplification confound.** The amplification coefficient aggregates market-driven and oracle-design-driven liquidations. Separating these would require matching each liquidation event to the oracle price path that triggered it — data exists from the Correlation phase but was not joined here.

**Cross-chain flow direction.** THORChain swap data would reveal whether crashes show flight-to-stables, BTC rotation, or total exit. Different flow directions would distinguish panic (stables) from rebalancing (BTC rotation). Not pulled.

**Pre-crash decoupling as early warning.** ETH/S&P correlation was near-zero (0.025) before the Yen carry crash — the only macro-origin crash preceded by true decoupling. n = 1 of 1 eligible cases. Requires more macro-origin events to test.

**Sub-daily transmission.** All TradFi variables peak at lag 0 at daily resolution. Hourly data would measure whether VIX spikes lead ETH drops by hours, or whether the transmission is truly simultaneous across global markets.
