# MEV Signals Exploration Log

## Iteration 1 — Stablecoin Supply (Realm 1)

**Date:** 2026-03-19

### What was tested

Combined DeFi-native stablecoin supply (DAI + GHO + USDS) as a leading indicator for ETH price direction.

- **Data source:** DefiLlama stablecoins API. IDs: DAI=5, GHO=118, USDS (Sky Dollar)=209.
- **Period:** 2022-01-01 to 2026-03-18, daily granularity.
- **Script:** `memories/mev/stablecoin_supply.py`
- **Data saved:** `memories/mev/data/stablecoin_supply.csv`

### What was measured

| Stablecoin | Peak cross-corr (r) | Lag (days) | Classification |
|---|---|---|---|
| DAI | +0.229 | -1 | Concurrent |
| GHO | -0.061 | +27 | Noise |
| USDS | -0.134 | +28 | Noise (only 541 days, spurious) |
| **Combined** | **-0.124** | **-8** | **Lag** |

### Structural observations (conjectured)

- Reflexive loop doesn't close: minted stablecoins disperse rather than feeding back into spot demand.
- Expansion is voluntary/multi-path; contraction is forced/single-path.

---

## Iteration 2 — stETH/ETH Spread (Realm 3)

**Date:** 2026-03-19

### What was tested

stETH/ETH ratio as stress indicator. Segmented pre/post Shanghai (April 2023). Discount-only.

- **Script:** `memories/mev/steth_spread.py`
- **Data saved:** `memories/mev/data/steth_spread.csv`

### What was measured

| Period | Peak r | Lag | Classification |
|---|---|---|---|
| Pre-Shanghai | -0.375 | -1 | Concurrent |
| Post-Shanghai | 0.08 | — | Noise |

Pre-Shanghai conditional: -4.3% mean 14d returns, 67.5% hit rate. Post-Shanghai: coin-flip. Signal arbitraged away by redemption infrastructure.

---

## Iteration 3 — Liquidation Walls (Realm 6)

**Date:** 2026-03-19

### What was tested

Current ETH-collateralized liquidation threshold map.

- **Script:** `memories/mev/liquidation_walls.py`
- **Data saved:** `memories/mev/data/liquidation_walls.csv`, `memories/mev/data/liquidation_top_positions.csv`

### What was measured

- $2.16B total liquidatable. Walls at $1,300-$1,600 (60%+ below current ~$3,783).
- Two whale positions dominate: $213M Compound, $201M Maker — 94% of value.
- Current regime: not fragile.

---

## Iteration 4 — Historical Liquidation Events & Cascade Dynamics (Realm 6 continued)

**Date:** 2026-03-19

### What was tested

Historical Aave v2+v3 liquidation events: do spikes predict further drops (cascade) or recovery (absorption)?

- **Data source:** Free public RPC, on-chain `LiquidationCall` logs.
- **Period:** Jan 2022 → Mar 2026, 1,524 days, 27,702 events, $1.19B.
- **Script:** `memories/mev/liquidation_events.py`
- **Data saved:** `memories/mev/data/liquidation_events.csv`

### What was measured

| Threshold | # Days | 7d fwd return | Baseline | Direction |
|---|---|---|---|---|
| 90th pctl ($0.9M+) | 111 | -1.76% | +0.34% | Mild cascade |
| 95th pctl ($3.7M+) | 56 | +0.72% | +0.34% | Inverts — absorption |

Bimodal: moderate spikes → cascade; extreme spikes → capitulation/bounce. Clustering: lag-1 autocorrelation +0.145, gone by lag 2.

---

## Iteration 5 — Volatility Signal & Concentration Ratio

**Date:** 2026-03-19

### What was tested

A. Do high-liquidation days predict elevated forward return variance? B. Does temporal shape of liquidation flow (concentrated vs distributed) classify cascade vs absorption?

- **Script:** `memories/mev/volatility_signal.py`
- **Data saved:** `memories/mev/data/volatility_signal.csv`

### What was measured

**A. Volatility regime:** 1d absolute returns: quiet 2.36% → extreme 4.62% (~2x, monotonic). Log-volume → 7d realized vol: r=0.235. Real but modest.

**B. Concentration ratio (Aave-only baseline):**

| Group | N | 7d Median Return | % Negative |
|---|---|---|---|
| Concentrated (>50% of trailing 7d) | 72 | +0.19% | ~50% |
| Distributed (≤50%) | 39 | -3.44% | 64% |

Mann-Whitney p=0.177. Effect size: 3.6pp.

---

## Iteration 6 — Multi-Protocol Expansion & Concentration Ratio Retest

**Date:** 2026-03-19

### What was tested

Expanded liquidation event dataset by adding Compound v2, Compound v3, and Maker (Dog/Bark) ETH-collateral liquidations. Retested concentration ratio on combined data.

- **Data source:** Same free public RPC approach. Additional contracts:
  - Compound v2: cDAI (`0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643`), cUSDC (`0x39AA39c021dfbaE8faC545936693aC917d5E7563`), cUSDT (`0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9`) — filtered for cETH collateral seizures
  - Compound v3 Comet USDC (`0xc3d688B66703497DAA19211EEdff47f25384cdc3`) — `AbsorbCollateral` events, WETH asset
  - Maker Dog (`0x135954d155898D42C90D2a57824C690e0c7BEf1B`) — `Bark` events, ETH-A/B/C ilks
- **Script:** `memories/mev/liquidation_expand.py`
- **Data saved:** `memories/mev/data/liquidation_events_combined.csv`

### What was measured

**Data expansion:**

| Protocol | Events | Volume | Active Days |
|---|---|---|---|
| Aave v2+v3 | 27,702 | $1,192M | 1,110 |
| Compound v2 | 7,459 | $312M | 565 |
| Compound v3 | 747 | $208M | 150 |
| Maker (ETH-A/B/C) | 329 | $312M | 103 |
| **Combined** | **36,237** | **$2,024M** | **1,168** |

+31% volume, but only +2 distributed-class days (39→41). Protocols liquidate on the same days — correlated events.

**Concentration ratio — before vs after:**

| Metric | Aave Only | Combined |
|---|---|---|
| High-liq days (>90th pctl) | 111 | 117 |
| Concentrated / Distributed | 72 / 39 | 76 / 41 |
| Concentrated 7d median | +0.19% | +0.19% |
| Distributed 7d median | -3.44% | -3.48% |
| Spread | 3.63pp | 3.67pp |
| Distributed % negative | 64% | 70.7% |
| **Mann-Whitney p** | **0.177** | **0.076** |

### What these results mean

**The signal survived expansion.** Effect direction consistent, spread stable at ~3.7pp, p improved from 0.177 to 0.076. The distributed group (multi-day liquidation bleed) shows -3.48% median 7d returns with 70.7% negative hit rate. The concentrated group (single-day capitulation spike) shows essentially flat forward returns.

**Correlated events limit further L1 expansion.** Adding more L1 protocols adds volume to existing high-liquidation days rather than creating new ones. Diminishing returns on sample size from this approach.

### What is measured vs conjectured

**Measured:**
- 36,237 liquidation events across 4 protocols, $2.02B total
- Concentration ratio effect: 3.67pp spread, p=0.076, stable across Aave-only → combined
- Distributed events: n=41, median -3.48%, 70.7% negative
- Effect survived out-of-sample protocol expansion without dilution

**Conjectured:**
- Concentrated spikes = overhang clearing (absorption). Distributed = ongoing fragility (cascade). Mechanistic explanation for the measured split.
- Signal is arbitrage-resistant because it reads temporal structure, not just volume.
- Signal would reach conventional significance with ~2-3x more distributed events.

### Characterized signal properties

| Property | Value |
|---|---|
| Signal | Liquidation concentration ratio (today's volume / trailing 7d total) |
| Trigger | Daily liquidation volume > 90th percentile of all days |
| Classification | Concentrated (ratio > 0.5) vs Distributed (ratio ≤ 0.5) |
| Distributed outcome | Median -3.48% 7d return, 70.7% negative |
| Concentrated outcome | Median +0.19% 7d return, ~50% negative |
| Effect size | 3.67pp median spread |
| Statistical significance | p=0.076 (Mann-Whitney), borderline |
| Frequency | ~41 distributed events in 1,524 days ≈ 10/year |
| Computable in real-time | Yes — monitor on-chain liquidation events, compute ratio daily |
| Data source | Free public RPC, no API keys needed |

### What was not tested

- **L2 liquidation events** (Aave on Arbitrum, Base, Optimism). Would test universality of mechanism across chains with different gas dynamics and user bases. Same code, different RPC endpoints.
- **Utilization → liquidation regime link.** Does high lending utilization predict distributed (cascade-type) liquidation patterns? Would connect Realm 2 to Realm 6 causally: utilization as precondition for cascade mode.
- **IV/options data.** Whether market already prices vol expansion on liquidation days.
- **Vol × concentration interaction.** Whether distributed events show higher forward vol than concentrated.
- **Sharpe/tradeability.** Whether -3.48% median at 71% hit rate, ~10x/year is tradeable after costs.

### Thesis evolution

| Stage | Thesis formulation |
|---|---|
| Original | "On-chain leverage data predicts ETH price direction" |
| After Realm 1 | Expansion signals lag — loop doesn't close |
| After Realm 3 | Contraction signals get arbitraged — infrastructure adapts |
| After Realm 6 | Liquidation map is legible but snapshot-only |
| After Realm 6b | Liquidation outcomes are bimodal (cascade vs absorption) |
| After volatility test | Vol signal real but modest; concentration ratio classifies modes |
| **Current** | **"The temporal structure of liquidation flow classifies system mode — fragility resolving vs deepening." Characterized signal: concentration ratio, p=0.076, ~3.7pp effect, ~10 events/year.** |

### Decision point — two doors forward

**Door 1: L2 universality test.** Same code, different RPCs. Tests whether mechanism is about leverage topology universally or Ethereum-L1-specific. Characterization question.

**Door 2: Utilization → liquidation regime.** Does high utilization predict distributed liquidation patterns? Builds a two-step causal chain: high utilization → distributed liquidations → further downside. Connects parked Realm 2 to the primary finding. More interesting because it extends the strongest result rather than replicating it.

### Parked

- Realms 4 (TVL divergence), 5 (bridge flows) — no clear connection to primary finding
- USDT/USDC supply (capital inflow signal — different mechanism entirely)
- Options/IV overlay, Sharpe analysis — premature until signal further characterized

---

## Iteration 7 — Utilization → Liquidation Regime Link (Plan Item A)

**Date:** 2026-03-19

### What was tested

Whether high lending utilization (proxied by Aave v3 stablecoin supply APY) predicts distributed vs concentrated liquidation patterns. The hypothesis: high utilization → more leveraged positions → distributed (cascade-type) liquidations when a shock hits.

- **Data source:** DefiLlama yields API (`/chart/{pool_id}`) for Aave v3 Ethereum pools: USDC, USDT, DAI, WETH. Daily `apyBase` and `tvlUsd`.
- **Period:** Feb 2023 → Mar 2026 (~1,100 days). Aave v2 is not in DefiLlama yields, so 2022 data is not covered.
- **Leverage proxy:** TVL-weighted stablecoin APY across USDC + USDT + DAI (`stable_apy_weighted`).
- **Script:** `memories/mev/utilization_signal.py`
- **Data saved:** `memories/mev/data/utilization_apy.csv`, `memories/mev/data/utilization_results.txt`

### What was measured

**Test A (pre-event APY comparison):** For each high-liquidation day in the overlap period, computed mean `stable_apy_weighted` over the 7 days before the event. Compared between concentrated and distributed groups.

| Group | Pre-event 7d mean APY (median) |
|---|---|
| Concentrated | 4.81% |
| Distributed | 3.69% |
| Mann-Whitney p | 0.0011 |

**Result is the inverse of hypothesis.** Concentrated events are preceded by *higher* APY (higher utilization), not lower.

**Test B (quartile conditional):** Bucketed all days by `stable_apy_weighted` quartile. Within each, computed fraction of high-liquidation events that are distributed:

| Quartile | APY range | % distributed |
|---|---|---|
| Q1 (lowest) | <2.73% | 64% |
| Q2 | 2.73–4.13% | 35% |
| Q3 | 4.13–5.53% | 27% |
| Q4 (highest) | >5.53% | 12% |
| Fisher's exact (Q1 vs Q4) | | p=0.0013 |

Perfectly monotonic gradient: low utilization → more distributed events; high utilization → more concentrated events.

**Test C (temporal lead/lag):** Cross-correlation between `stable_apy_weighted` and daily liquidation volume at lags -14d to +14d. All correlations near zero (|r| < 0.05). APY *level* correlates with classification, but APY does not dynamically precede or follow liquidation events.

### What this suggests and what it doesn't

The inverse result has a plausible mechanism: high utilization = crowded positions at similar thresholds + active liquidator infrastructure → shocks clear in a single concentrated burst. Low utilization = sparse positions + fewer liquidators → liquidations trickle over days.

However, the review discussion identified that this result is likely a **regime confound**, not a causal relationship:

### Vulnerabilities identified in review

**1. Regime confound.** Stablecoin APY moves in regime-scale waves (months of low, months of high). Low APY periods likely overlap with bear markets / low liquidity. High APY periods overlap with bull / high-activity periods. The finding may reduce to: "liquidation events during bear markets produce worse forward returns" — true but trivial. APY is acting as a regime proxy, not a causal driver.

**2. Effective degrees of freedom.** The ~100 high-liquidation days in the overlap period are not independent observations. They cluster into approximately 5-8 distinct stress episodes, each spanning days/weeks within a single APY regime. Mann-Whitney and Fisher tests assume independence. With block-correlated data, p=0.0011 could inflate by an order of magnitude or more. The perfect monotonic gradient is actually the fingerprint of a slow-moving confound sorting observations, not independent evidence.

**3. Denominator contamination in the primary finding itself.** The concentration ratio (today's volume / trailing 7d total) has a trailing 7d denominator that is mechanically regime-biased. In a bear market with sustained stress, the trailing 7d total is already elevated, making it harder for any single day to exceed 50% — this mechanically biases toward "distributed" classification precisely when forward returns are negative (because bear markets persist). In a bull market with quiet prior days, the trailing 7d is low, making it easy to cross 50% — mechanically biased toward "concentrated."

Concrete example: an identical $60M liquidation day. In a bear context with $260M trailing 7d → ratio = 23%, classified "distributed." In a bull context with $90M trailing 7d → ratio = 67%, classified "concentrated." The same event gets different labels purely from regime context. The entire signal chain (bear → inflated denominator → "distributed" → negative forward returns) can run through regime momentum without any structural mechanism being invoked.

**This means the regime confound concern applies to the primary finding (concentration ratio, Iteration 5-6), not just the utilization extension.**

### What was measured vs conjectured

**Measured:**
- Aave v3 stablecoin APY data for USDC/USDT/DAI, Feb 2023 → Mar 2026
- Inverse relationship: higher pre-event APY predicts concentrated (not distributed) events, p=0.0011
- Monotonic Q1→Q4 gradient in distributed fraction: 64% → 35% → 27% → 12%
- No temporal lead/lag structure in cross-correlations

**Conjectured:**
- The inverse relationship is a regime confound rather than a causal mechanism
- The primary finding's trailing 7d denominator is regime-contaminated
- ~5-8 independent episodes rather than ~100 independent observations, making p-values unreliable

### What was not tested

- Whether the concentration ratio survives regime-invariant reclassification (alternative denominators that normalize out regime)
- Whether the concentrated/distributed distinction predicts forward returns within the same market regime (trailing 30d return as control)
- The effective number of independent episodes (clustering analysis)
- Whether the forward return spread is stable across a range of classification thresholds or dependent on a single cut

---

## Iteration 8 — Regime-Invariance Stress Test of Concentration Ratio

**Date:** 2026-03-19

### What was tested

Whether the concentration ratio's forward return spread (Iterations 5-6) survives when the classification method is changed to remove the trailing 7d denominator's regime contamination (identified in Iteration 7 review). Two alternative classification methods were tested alongside the original, plus within-regime controls and episode clustering.

- **Script:** `memories/mev/regime_test.py`
- **Data:** `memories/mev/data/regime_test_results.txt`
- **Dataset:** `liquidation_events_combined.csv`, full period Jan 2022 → Mar 2026, 117 high-liquidation days (>P90 of non-zero days, threshold $1.05M)

### What was measured

**A. Alternative classification methods:**

| Method | How it classifies | Conc n | Dist n | Spread | p-value |
|---|---|---|---|---|---|
| Original (7d sum >50%) | Shape: is today dominant in its 7d window? | 76 | 41 | +3.674pp | 0.0761 |
| M1-P95 (180d window ≥95th) | Magnitude: is today extreme vs 6-month history? | 56 | 57 | +4.545pp | 0.0100 |
| M1-P97 (180d window ≥97th) | Magnitude: is today very extreme vs 6-month history? | 38 | 75 | +5.672pp | 0.0027 |
| M2-Peak (today/max(prior 6d) >2.0) | Shape: is today a dominant spike vs recent days? | 65 | 52 | +2.431pp | 0.3727 |

M1 (magnitude-based, regime-invariant) strengthens the signal. M2 (shape-based, regime-invariant) does not reach significance.

**Classification overlap with original:**
- M1-P95: 66.7% of original distributed → new distributed, 58.1% of original concentrated → new concentrated. Moderate overlap — methods are measuring partly different things.
- M1-P97: 84.6% of original distributed → new distributed, 43.2% of original concentrated → new concentrated. High overlap on distributed side, substantial reclassification of concentrated days.
- M2-Peak: 100% of original distributed → new distributed, 85.5% of original concentrated → new concentrated. M2 is a strict superset — all original distributed days are M2-distributed, plus 11 original concentrated days.

**B. Threshold stability (M1, 180d window):**

Spread is positive from 85th through 99th percentile. p-values drop from 0.085 (91st) through 0.003 (97th), rise back at 99th (small n). Effect visible across a range, not threshold-dependent.

| Pctl | n conc | n dist | Spread | p-value |
|---|---|---|---|---|
| 91st | 87 | 26 | +2.482pp | 0.0850 |
| 93rd | 72 | 41 | +2.155pp | 0.0269 |
| 95th | 56 | 57 | +4.545pp | 0.0100 |
| 97th | 38 | 75 | +5.672pp | 0.0027 |

**C. Within-regime control (trailing 30d ETH return):**

Bear market (30d ret ≤ 0) — spread survives strongly:
- M1-P95: +6.224pp, p=0.0015 (concentrated: n=48, median +1.23%; distributed: n=38, median -4.99%)
- M1-P97: +7.207pp, p=0.0012 (concentrated: n=33, median +2.27%; distributed: n=53, median -4.94%)
- Original: +5.379pp, p=0.0772

Bull market (30d ret > 0) — insufficient distributed events to test (n=5 for original, n=5 for M1-P97). Consistent with structural interpretation: bull-market shocks tend to produce concentrated spikes.

**D. Episode clustering (14d gap):**
- 117 high-liquidation days → 27 independent episodes
- Episode sizes: min=1, max=17, median=4
- Zero pure-distributed episodes. All 12 episodes containing distributed days also contain concentrated days. 15 episodes are pure concentrated.
- Episode-level test (dominant classification, first-day 7d return): concentrated n=21 median -0.47%, distributed n=6 median -16.78%. Spread: +16.311pp, p=0.031.
- The 6 distributed-dominant episodes: Jan 2022 (-21.4%), Apr 2022 (-1.5%), May 2022 (-28.6%), Feb 2025 (-20.2%), Mar 2025 (-13.3%), Jan 2026 (+2.6%).

### Key reframing from review

**The signal is magnitude-based, not shape-based.** The original thesis framed the concentration ratio as reading "temporal structure" — spike vs sequence, fragility resolving vs deepening. The M1 vs M2 comparison shows this is wrong:
- M2 (peak ratio) directly tests temporal shape (is today a dominant spike in its local window?) and fails (p=0.37).
- M1 (180d percentile) tests absolute magnitude (is today extreme by historical standards?) and succeeds (p=0.003).

The original concentration ratio conflated both dimensions. M1 strips to pure magnitude, M2 strips to pure shape. Magnitude is what predicts forward returns.

Revised claim: **"Extremely large liquidation days (97th+ percentile of 180d) tend to mark capitulation with positive forward returns; moderately large liquidation days (90th-97th percentile) tend to precede further declines."** This is a known microstructure pattern (climactic volume) measured with on-chain precision.

### What was measured vs conjectured

**Measured:**
- 180d-window percentile classification produces wider spread (5.7pp vs 3.7pp) and stronger significance (p=0.003 vs p=0.076) than original
- Spread survives within bear markets: +7.2pp, p=0.001 (M1-P97)
- Shape-based classification (M2-Peak) does not reach significance (p=0.37)
- 27 independent episodes; episode-level spread +16.3pp, p=0.031
- Zero pure-distributed episodes — concentrated and distributed days co-occur within stress events

**Conjectured:**
- The signal is magnitude-based (climactic volume) rather than shape-based (temporal structure of liquidation flow)
- This may reduce to a known microstructure pattern re-measured on-chain, rather than a novel DeFi-specific structural signal
- On-chain data's full transparency means no information asymmetry — measurement precision alone may not constitute edge

### What was not tested

- **Within-episode position:** Are concentrated days (M1) systematically later within episodes than distributed days? If yes, the spread may reflect position-in-crash (climax near the end) rather than structural classification.
- **Trailing 7d return control:** Do distributed days within bear markets have worse trailing 7d returns than concentrated days? If momentum/mean-reversion explains the spread, the signal reduces further.
- **Protocol cascade sequencing (Plan item C):** Temporal ordering of liquidations across protocols — architecturally determined, regime-invariant, and not yet tested.
- **Whether the magnitude pattern is DeFi-specific or generic:** Comparison to traditional-market climactic volume behavior.

---

## Iteration 9 — Discriminant Tests: Within-Episode Position & Momentum Control

**Date:** 2026-03-19

### What was tested

Two tests designed to determine whether the magnitude signal (M1-P97, Iteration 8) reflects genuine structural content or reduces to known artifacts: (1) within-episode position (are concentrated days just episode climax days near the end of crashes?), and (2) trailing 7d return control (does momentum/mean-reversion explain the forward return spread?).

- **Script:** `memories/mev/regime_test.py` (extended with sections E, F)
- **Data:** `memories/mev/data/regime_test_results.txt` (sections E, F appended)

### What was measured

**Test E — Within-episode position (M1-P97, mixed episodes):**

13 mixed episodes (containing both concentrated and distributed days under M1-P97):
- Concentrated days: n=35, mean normalized position = 0.621, median = 0.750
- Distributed days: n=53, mean normalized position = 0.420, median = 0.400
- Mann-Whitney p=0.006

Concentrated days cluster significantly later in episodes. Position-in-crash contributes to the forward return spread — days near the end of a crash mechanically have less remaining downside.

**Test F — Trailing 7d return control (M1-P97, bear market):**

Within bear-market high-liquidation days (trailing 30d return ≤ 0), n=86 (33 concentrated, 53 distributed):

| Metric | Concentrated | Distributed | Spread |
|---|---|---|---|
| Trailing 7d return (median) | -13.20% | -10.11% | — |
| Forward 7d return (median) | +2.27% | -4.94% | +7.21pp |
| Excess forward return (fwd − trail, median) | +16.28% | +5.38% | +10.91pp |
| Excess return Mann-Whitney p | | | 0.0003 |

Concentrated days have *deeper* prior 7d drawdowns than distributed days (p=0.066). Yet their forward returns are better. The excess return spread (forward minus trailing) is +10.9pp at p=0.0003.

### What these results mean together

**Position-in-crash (Test E) contributes but does not explain the spread.** Concentrated days tend to be later in episodes, which mechanically improves their forward returns. However:

**The signal is not mean-reversion (Test F).** If the spread were mean-reversion, days with deeper prior drawdowns should bounce more, and the excess return (forward minus trailing) would be similar between groups. Instead, concentrated days have deeper prior drawdowns AND disproportionately better excess returns. The magnitude classification captures something beyond trailing momentum.

**Conclusion:** The magnitude signal (M1-P97) is a validated empirical pattern. Extremely large liquidation days (≥97th percentile of 180d) predict better 7d forward returns than moderately large ones, with a ~5-7pp spread that survives regime controls, momentum controls, position-in-episode effects, and threshold variation.

### Review consensus on signal status

The review discussion reached consensus on three points:

**1. The magnitude signal is real.** Tests E and F close the "is this real" question. No remaining confounds identified that could overturn the finding.

**2. The magnitude signal is not a trading edge.** On-chain liquidation events are fully public, trivially indexable, and monitored by every serious DeFi participant. The classification (is today ≥97th pctl of 180d?) requires no information processing advantage. Zero information asymmetry. The signal is validated as a descriptive tool for monitoring system stress, not as a source of trading edge.

**3. The structural edge hypothesis now lives in the architectural layer.** The investigations most likely to reveal genuinely novel, non-reducible signals are those testing architectural properties of the multi-protocol leverage system:
- Protocol cascade sequencing (Plan C): Do different collateral ratios and liquidation thresholds produce a measurable, predictable ordering of liquidation events across protocols? Does the lag structure between protocols correlate with cascade severity?
- Perp leading edge (Plan D): Does the cross-venue leverage hierarchy (higher-leverage perps → lower-leverage lending) create temporal structure?
- These require non-trivial synthesis across multiple data sources, which is a higher information-processing bar than anything tested so far.

### What was measured vs conjectured

**Measured:**
- Concentrated days (M1-P97) cluster later in episodes: mean position 0.62 vs 0.42, p=0.006
- Concentrated days have deeper trailing 7d drawdowns: median -13.2% vs -10.1%, p=0.066
- Excess forward return spread persists: +10.9pp, p=0.0003
- Signal is not mean-reversion: deeper prior drawdowns + better forward returns = disproportionate bounce

**Conjectured:**
- The magnitude signal reduces to a known climactic volume pattern (observed in traditional markets for decades) re-measured on-chain with higher precision
- On-chain measurement precision alone does not constitute trading edge due to zero information asymmetry
- Architectural features (protocol ordering, cross-venue timing) may provide genuine edge because they require non-trivial multi-source synthesis

### What was not tested

- **Protocol cascade sequencing (Plan C):** Whether Maker/Compound liquidations systematically precede Aave, and whether the lag structure correlates with cascade severity. Data exists — zero cost.
- **Perp liquidation as leading edge (Plan D):** Whether perpetual DEX liquidations precede lending protocol liquidations. Requires new data (Hyperliquid API).
- **Whether the magnitude pattern is DeFi-specific or generic:** Direct comparison to traditional-market climactic volume behavior.

---

## Iteration 10 — Protocol Cascade Sequencing (Plan Item C)

**Date:** 2026-03-19

### What was tested

Whether different lending protocols (Maker, Compound, Aave) liquidate in a predictable, architecturally-determined order during stress events. The hypothesis: higher collateral ratios (Maker 150%) should trigger liquidations earlier in a price decline than lower ratios (Aave with variable/e-mode), creating a measurable lag that could serve as an early warning signal.

- **Script:** `memories/mev/cascade_sequence.py`
- **Data:** `memories/mev/data/cascade_sequence_results.txt`
- **Dataset:** Block-level event timestamps from raw liquidation logs (`liquidation_events_raw.csv`, `liquidation_compound_raw.csv`, `liquidation_maker_raw.csv`), 38,116 events across 3 protocols. Same 27 episodes from Iteration 8.

### What was measured

**A. Protocol activation ordering:**

| First to activate | Episodes | % |
|---|---|---|
| Aave | 11/23 | 48% |
| Compound | 7/23 | 30% |
| Maker | 5/23 | 22% |

No consistent cascade sequence. Aave fires first most often despite having the most flexible collateral ratios. Sub-daily (block-level) resolution confirms: when protocols activate on the same day, Aave fires first vs Compound 67% of the time (6/9) and vs Maker 80% (4/5).

**The structural hypothesis is refuted.** Ordering is volume-proportional (Aave has ~80% of lending volume), not architecturally determined by collateral ratios.

**B. Protocol lag statistics:**

| Pair | N | Median lag | X leads Y | Same day | Y leads X |
|---|---|---|---|---|---|
| Maker→Aave | 20 | -3.5d | 0% | 25% | 75% (Aave leads) |
| Compound→Aave | 20 | -1.0d | 0% | 45% | 55% (Aave leads) |
| Maker→Compound | 19 | 0d | 11% | 53% | 37% |

Aave leads both Maker and Compound in the majority of episodes. Maker never leads Aave (0/20 episodes). The ordering is the inverse of the collateral-ratio prediction.

**C. Simultaneous vs sequential activation:**

| Type | N | Median 7d return | % negative |
|---|---|---|---|
| Simultaneous (all protocols within 1d) | 8 | +0.26% | 50% |
| Sequential (≥2d spread) | 15 | -4.35% | 80% |
| Spread | | +4.61pp | |
| Mann-Whitney p | | 0.24 | |

Directionally consistent with the magnitude classifier (simultaneous ≈ capitulation, sequential ≈ continuation), but not significant. This is the same distributed/concentrated distinction measured from the protocol dimension rather than the volume dimension — not independent information.

**D. Volume share dynamics within episodes:**

Volume share shifts are inconsistent across episodes:
- May 2022: Aave early (62%) → Compound late (54%)
- Jan 2022: Compound early (67%) → Aave late (54%)
- Aug 2024: Compound early (75%) → Aave late (79%)
- Mar 2025: Aave early (87%) → Maker late (61%)

No universal pattern of protocol-level volume migration within episodes.

### Why the structural hypothesis failed

Collateral ratios set the threshold at which a position liquidates, but the timing of when that threshold is hit depends on the position's specific entry price and LTV, not just the protocol's minimum ratio. Aave has the most positions distributed across the widest range of entry prices, so it has positions at every price level and fires first almost by definition. The architectural logic assumed positions cluster near protocol minimums — they don't.

### Emergent finding: position heterogeneity dominates protocol parameters

Across the investigation, every structural hypothesis testing whether DeFi protocol parameters (collateral ratios, utilization rates, protocol architecture) create predictive temporal structure has failed for the same reason: **position heterogeneity within protocols dominates protocol-level structural parameters.**

The pattern across refutations:
- **Utilization (Iteration 7):** APY as regime proxy, not causal driver. User behavior (borrowing patterns) varies independently of protocol parameters.
- **Temporal shape (Iteration 8):** Shape-based classification (M2-Peak) fails; only magnitude succeeds. The temporal pattern of liquidation flow is determined by position distribution, not by protocol architecture.
- **Protocol cascade (Iteration 10):** Ordering is volume-proportional, not determined by collateral ratios. Positions span the full price range within each protocol.

The leverage topology is transparent at the protocol level, but the positions within that topology are distributed in ways that blur the structural edges. You can see Maker's 150% collateral ratio, but you can't predict when Maker liquidations will fire relative to Aave because user positions span the full price range.

### What was measured vs conjectured

**Measured:**
- Aave activates first in 48% of multi-protocol episodes; Maker never leads Aave (0/20)
- Sub-daily: Aave fires first in 67-80% of same-day activations
- Simultaneous vs sequential: +4.6pp spread, p=0.24 (not significant)
- Volume share dynamics are inconsistent across episodes

**Conjectured:**
- Ordering is volume-proportional rather than architecturally determined
- Position heterogeneity within protocols is the common failure mode for all structural hypotheses tested
- The simultaneous/sequential distinction is redundant with the magnitude classifier, not an independent signal

### What was not tested

- **Perp → lending temporal lead (Plan D):** Cross-venue leverage hierarchy (5-50x perps vs 1.5-3x lending) has a qualitatively wider leverage gap than cross-protocol (Maker vs Aave). This is the last structural test where the gap might be large enough to overcome position heterogeneity. Requires Hyperliquid API data — feasibility check needed before committing to full analysis (Hyperliquid launched late 2023, ~2 years overlap, ~15 of 27 episodes).
- **Cross-collateral contagion (Plan E):** Whether multi-collateral distributed events predict worse outcomes than ETH-only events.

---

## Iteration 11 — Perp → Lending Temporal Lead (Plan Item D)

**Date:** 2026-03-19

### What was tested

Whether perpetual futures liquidation activity precedes lending protocol liquidation activity during stress episodes. The hypothesis: higher-leverage instruments (perps at 5-50x) should liquidate before lower-leverage instruments (lending at 1.5-3x) because they hit thresholds at smaller price moves. This is the cross-venue leverage hierarchy test — structurally different from Plan C (cross-protocol within lending) which failed because the leverage gap between lending protocols was too narrow.

- **Script:** `memories/mev/perp_lead.py`
- **Data:** `memories/mev/data/perp_lead_results.txt`, `memories/mev/data/binance_oi_episodes.csv`

### Data feasibility (Phase 1)

Direct historical perp liquidation data is not freely available:
- Hyperliquid: stats API returns 403, no public liquidation history endpoint
- Coinglass: all liquidation endpoints require API key
- Binance: removed public forceOrders endpoint; no liquidationSnapshot in data archive

**Proxy used:** Binance ETHUSDT 5-minute open interest (OI) snapshots, available Dec 2021 → present. Large negative hourly OI changes during stress episodes are mechanically driven by forced position closures (liquidations). Threshold: >3% hourly OI drop. 92,157 rows of 5-min data fetched for the 17 episodes from 2024 onward (7,697 hourly data points).

**Limitation:** OI changes include voluntary closures. During severe stress, forced closures dominate, but the proxy is noisy for milder events.

### What was measured (Phase 2)

**A. Episode alignment:** For each of 17 lending liquidation episodes (2024+), identified the first significant OI drop (>3% hourly) within ±48h of the lending peak day. Lending reference: midnight UTC of peak liquidation day.

**B. Lead/lag statistics:**

| Metric | Value |
|---|---|
| Episodes with perp OI drop preceding lending peak | 16/17 (94%) |
| Median lead time | 23 hours |
| Mean lead time | 24.4 hours |
| P10 lead | 7 hours |
| P25 lead | 9 hours |
| P75 lead | 44 hours |
| Only lending-leads episode | 2025-01-07 (lag = -1h, essentially simultaneous) |

**C. Lag vs severity:**
- Spearman correlation (lag vs 7d return): r=+0.33, p=0.20 — not significant
- Simultaneous episodes (|lag| < 12h, n=7): median 7d return = -4.35%
- Perps-lead episodes (>12h, n=10): median 7d return = -0.34%

### Structural finding

The leverage hierarchy creates measurable temporal structure: perp OI drops precede lending liquidation peaks by a median of 23 hours with 94% consistency. This is the structural signal that Plan C (protocol cascade within lending) failed to find. The leverage gap between perps (5-50x) and lending (1.5-3x) is wide enough to produce consistent ordering, whereas the Maker-Aave gap (both 1.5-3x effective) was not.

This confirms the position-heterogeneity finding from Iteration 10: structural parameters only create temporal ordering when the parameter gap is large enough to dominate position diversity.

### Vulnerabilities identified in review

**1. False positive rate is unknown (existential concern).** The >3% hourly OI drop threshold and ±48h search window may produce high recall but low precision. A 48h window contains 96 hourly observations. If >3% OI drops occur frequently during volatile markets, finding one before any lending spike could approach base rate. The control test: count all >3% hourly OI drops in the full dataset, and compute what fraction fall within 48h before a lending episode.

**2. Reference point inflates lead time.** Lending reference is midnight of peak day. Actual lending liquidations happen during the day. If peak lending events cluster around noon-6pm UTC, the true lead is 12-18h shorter. A 23h median could compress to 5-11h. Block-level lending timestamps exist and could provide a tighter reference.

**3. Voluntary vs forced closures.** OI drops during moderate events may be predominantly voluntary de-risking (traders closing positions as price falls), not forced liquidations. If so, the "lead" is behavioral (sophisticated traders react faster) rather than mechanical (leverage hierarchy). A diagnostic: compute the ETH price at the OI drop time vs at the lending peak hour. If the OI drop happens at -5% from recent highs and lending peaks at -15%, there's genuine warning content (the further decline hasn't happened yet). If both happen at similar price levels, the OI drop is faster measurement of the same event.

**4. Information asymmetry.** Even if the lead is real, OI data is public (Binance publishes it). The signal doesn't rely on private information — it relies on synthesizing OI movement with lending liquidation wall maps.

### What was measured vs conjectured

**Measured:**
- Perp OI drops precede lending peaks in 16/17 episodes (94%), median 23h
- Simultaneous episodes have worse 7d returns (-4.35%) than perps-lead episodes (-0.34%)
- No significant correlation between lag magnitude and episode severity (p=0.20)

**Conjectured:**
- The lead time is inflated by the midnight reference point; true lead may be 5-11h
- The false positive rate may be high, making the 94% consistency less meaningful than it appears
- The signal's practical value is as a confirmation input within a monitoring system, not standalone edge
- The leverage hierarchy (perps → lending) creates real temporal structure, but this is the structural finding, not a trading signal

### What was not tested

- **False positive rate control:** How many >3% OI drops occur outside of lending episodes? What is the precision of the signal?
- **Price-level diagnostic:** ETH price at OI drop vs at lending peak — determines whether the lead provides genuine warning content or is just faster measurement of the same event
- **Corrected lead time:** Using block-level lending timestamps instead of midnight reference

---

## Iteration 12 — Perp Lead Discriminant Tests: False Positive Rate & Price Diagnostic

**Date:** 2026-03-19

### What was tested

Two discriminant tests to resolve the key vulnerabilities identified in Iteration 11: (1) false positive rate of the >3% OI drop signal, and (2) price-level diagnostic + corrected lead time using block-level lending timestamps.

- **Script:** `memories/mev/perp_lead.py` (extended with sections G, H)
- **Data:** `memories/mev/data/perp_lead_results.txt` (sections G, H appended)
- **Additional data:** Binance OI for 3 control months (2024-09, 2024-11, 2025-07) with no lending episodes

### What was measured

**Test G — False positive rate:**

| Threshold | Episode drops/day | Control drops/day | Enrichment | Est. false alarms/year |
|---|---|---|---|---|
| >1% | 1.36 | 0.60 | 2.3x | ~219 |
| >2% | 0.48 | 0.18 | 2.6x | ~66 |
| >3% | 0.21 | 0.05 | 3.9x | ~20 |
| >4% | 0.10 | 0.01 | 6.8x | ~5 |
| >5% | 0.05 | 0.01 | 5.9x | ~3 |

At the 3% threshold: ~30% precision (~20 false alarms/year vs ~8 true episodes). At 4%: enrichment jumps to 6.8x with ~5 false alarms/year. The 4% threshold is the operational sweet spot.

**Test H — Corrected lead time + price diagnostic:**

Using block-level lending timestamps to identify the actual hour of peak lending liquidation volume (replacing the midnight reference):

| Metric | Original (midnight ref) | Corrected (actual peak hour) |
|---|---|---|
| Median lead | 23h | 37h |
| Mean lead | 24.4h | 37.3h |
| Perps lead | 16/17 (94%) | 16/17 (94%) |

The midnight reference **understated** the lead, not overstated it. Lending liquidation peaks cluster in the afternoon/evening UTC, so the actual peak is later than midnight, extending the lead.

**Price-level diagnostic:**

| Metric | Value |
|---|---|
| Median price decline (OI drop → lending peak) | -10.9% |
| Mean price decline | -8.7% |
| Episodes with further decline after OI drop | 15/17 (88%) |

When the OI drop fires, ETH is typically 10.9% higher than it will be at the lending peak. This is genuine early warning — further decline is still coming. Not faster measurement of the same event.

Per-episode detail shows the price gap is substantial in most cases: -15.1% (Mar 2024), -11.5% (Apr 2024), -16.8% (Aug 2024), -12.5% (Dec 2024), -11.6% (Mar 2025, Sep 2025), -14.5% (Jan 2026). Two episodes show minimal gap: -0.7% (Aug 2024 late) and +3.5% (Nov 2024 — the one case where the OI drop was likely noise).

### What these results mean

**The perp → lending lead is validated as genuine early warning.** Three concerns from Iteration 11 are resolved:
1. False positive rate is manageable at the 4% threshold (~5 false alarms/year, 6.8x enrichment)
2. Corrected lead time is 37h (longer than original 23h estimate, not shorter)
3. Price diagnostic confirms 10.9% further decline after OI drop — genuine warning content, not same-event measurement

### Final review consensus

The review discussion reached consensus on:

1. **The magnitude classifier IS the climactic volume pattern** measured on-chain with higher precision than traditional volume data allows. Drop the "may reduce to" hedge. The pattern itself is not novel; the measurement precision is the DeFi-specific contribution.

2. **Three findings to carry forward:**
   - **Position heterogeneity principle:** The most generalizable finding. Temporal ordering in liquidation cascades scales with the leverage gap between position types. Explains why intra-lending protocol structure doesn't produce signals, and predicts where signals will exist (wide leverage gaps).
   - **Perp → lending lead (37h, 10.9% further decline):** The one genuinely novel structural finding. Not a standalone trading signal (precision issues) but provides information beyond simpler inputs.
   - **Three-layer monitoring architecture:** Utilization (pre-condition) → perp OI (early warning) → magnitude (classification). Each layer stress-tested individually. The conjunction hasn't been tested as a system.

3. **Investigation conclusion:** The on-chain leverage topology is legible, the mechanical relationships are real, and the leverage hierarchy creates measurable temporal structure when the leverage gap is wide enough. The findings constitute a fragility monitoring system, not a trading edge. No single signal provides information asymmetry on fully public data; value is in the synthesis.

### What was measured vs conjectured

**Measured:**
- False positive rate: 3.9x enrichment at 3%, 6.8x at 4%, ~5 false alarms/year at 4% threshold
- Corrected lead time: 37h median (increased from 23h after fixing midnight reference)
- Price decline OI drop → lending peak: -10.9% median, 88% of episodes
- The OI signal fires at a meaningfully higher price than where lending liquidations peak

**Conjectured:**
- The magnitude classifier is the climactic volume pattern, not a novel DeFi-specific mechanism
- The perp → lending lead's value is as a confirmation input within a monitoring system, not standalone edge
- The conjunction of all three layers (utilization + perp OI + magnitude) may produce better precision than any single signal, but this has not been tested
