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

---

## Iteration 13 — False Positive Anatomy of Distributed Days

**Date:** 2026-03-19

### What was tested

What distinguishes the ~32% of distributed liquidation days (M1-P97) where 7d forward return is positive (the signal fails). Six candidate traits were tested for separation power between true positives (51 days, 7d return < 0) and false positives (24 days, 7d return ≥ 0).

- **Script:** `memories/mev/false_positive_anatomy.py`
- **Data:** `memories/mev/data/false_positive_results.txt`
- **Dataset:** Same `liquidation_events_combined.csv`, 75 distributed days under M1-P97 classification with forward return data

### What was measured

**Test 1 — Position within episode:**
FP median position 0.50, TP median 0.40. Mann-Whitney p=0.316. Not significant — false positive distributed days do not cluster at distinct episode positions.

**Test 2 — Trailing drawdown magnitude:**
Trailing 7d: FP median -10.15%, TP median -7.97%, p=0.514. Trailing 14d: FP median -9.47%, TP median -9.01%, p=0.977. Not significant — prior drawdown depth does not distinguish FP from TP.

**Test 3 — Volume percentile rank within 180d window:**
FP median 93.55 pctl, TP median 91.79 pctl, p=0.261. Spearman r=0.096, p=0.411 (percentile vs forward return). Not significant — position within the P90-P97 band does not predict outcome. No gradient.

**Test 4 — Utilization APY (2023-02+, n=51):**
FP median APY 4.57%, TP median 3.95%, p=0.296. Not significant as a group comparison. Marginal Spearman r=0.245, p=0.083 — higher APY weakly associated with worse signal (more false positives). Low APY (<median 4.15%): 72% hit rate. High APY: 65.4%.

**Test 5 — Prior episode recency:**
FP median 7 days since prior high-liq day, TP median 4 days, p=0.411. Not significant.

**Test 6 — OI confirmation (2024-03+, n=50):**
Best individual predictor. FP max OI drop median -3.92%, TP median -4.86%, p=0.081. With >3% OI drop present: 70.7% hit rate (n=41). Without: 55.6% hit rate (n=9).

**Combined filters (2024-03+ period, n=50):**

| Filter | n | %neg | Median fwd 7d |
|---|---|---|---|
| No filter (baseline) | 50 | 68.0% | -1.55% |
| OI drop >3% | 41 | 70.7% | -3.31% |
| Bear (trail 30d ≤ 0) | 36 | 69.4% | -3.83% |
| OI drop + bear | 31 | 71.0% | -3.31% |
| OI drop + extreme trail (<-15%) | 6 | 100% | -6.44% |

**2026-01-20 episode detail:** First day (Jan 20) was false positive: +2.6% fwd, moderate drawdown (-11.9% trail 7d), APY 3.67%, OI drop -4.29%. After the concentrated spike on Jan 31 ($72.7M, 100th percentile), subsequent distributed days (Feb 1-4) were all true positives with deeper drawdowns and lower APY.

### What these results mean

**The ~32% false positive rate is largely irreducible within on-chain lending features.** No single trait meets the separation threshold (≥60%/≤30% prevalence split). The 97th percentile threshold is already doing most of the classification work available in this data domain. The remaining false positives depend on factors outside on-chain lending data.

**OI confirmation is the best marginal filter** but the improvement is modest (68% → 71%). The reframe: distributed events *with* perp OI confirmation represent cross-leverage-tier cascade (systematic stress); those *without* may be lending-only (idiosyncratic, e.g., single whale liquidation). This connects to the position heterogeneity principle — cross-tier confirmation identifies when the stress involves multiple leverage layers.

**Utilization APY direction is counterintuitive within distributed days.** Higher APY weakly predicts worse signal quality. Interpretation: high APY + distributed classification means the day is moderate-sized in a high-activity environment — closer to market noise that happened to cross the P90 threshold. The 180d trailing window adapts to regime shifts slower than utilization moves.

### Architecture reframe from review

The review discussion produced a reframe of the three-layer monitoring architecture:

**Prior framing:** Three independent layers — utilization classifies regime, OI provides early warning, magnitude classifies resolution. Each contributes to accuracy.

**Revised framing:** Utilization is **attention routing**, not accuracy filtering. It determines which type of event to expect (distributed vs concentrated), but does not improve classification accuracy within the distributed class. The operational architecture is hierarchical: utilization sets the prior → OI confirms cross-tier involvement → magnitude classifies resolution. Layers 2 and 3 are the active components; Layer 1 is context.

This demotes the conjunction test (#4 on the open list) — if utilization doesn't improve distributed accuracy, testing the three-layer conjunction is less valuable than originally estimated.

### What was measured vs conjectured

**Measured:**
- 75 distributed days: 51 TP (68%), 24 FP (32%)
- Six traits tested: episode position (p=0.316), trailing drawdown (p=0.514/0.977), volume percentile (p=0.261), utilization APY (p=0.296), prior episode recency (p=0.411), OI confirmation (p=0.081)
- No single trait cleanly separates FP from TP
- OI confirmation is best marginal filter: 68% → 71% hit rate
- Extreme combined filter (OI drop + trail <-15%): 6/6 decline, but n too small to trust
- 2026-01-20 episode: pre-concentrated day was FP, post-concentrated days were all TP

**Conjectured:**
- The ~32% FP rate is structurally expected for non-climactic volume signals, consistent with ~60-70% hit rates for comparable patterns in traditional microstructure
- The irreducibility boundary drawn is the information limit of on-chain lending data for this signal — improvement requires a different data class (exchange flows, options IV, direct perp liquidations)
- Utilization's role is attention routing (which classifier to weight), not accuracy filtering
- Post-concentrated distributed days may have higher TP rates than pre-concentrated ones (concentrated spike as cascade confirmation, not resolution) — the episode arc hypothesis

### What was not tested

- **Episode arc effect:** Whether distributed days *following* a concentrated spike within the same episode have different hit rates than distributed days *preceding* one. Prediction: post-concentrated distributed should have higher TP rate (the concentrated spike confirms the cascade, remaining distributed flow is mechanical late-deleveraging of near-threshold positions). The 2026-01-20 episode is consistent with this but n=1. Testable with existing data across the 12 mixed episodes.
- **Exchange flow absorption signal:** Whether CEX net inflows distinguish absorbed (FP) from cascading (TP) distributed events. If off-chain liquidity is the absorption mechanism, it should be visible in exchange flow data. Testable with CoinMetrics community data.
- **Options IV timing:** Whether Deribit IV spikes before, during, or after the perp OI drop — determines whether the information lives in a faster layer.
- **Utilization-conditioned magnitude threshold:** Adjusting the P90 gate for APY regime to reduce false triggers in high-utilization environments. Low priority — marginal effect size (p=0.083).

---

## Iteration 14 — Episode Arc Probe: Pre vs Post Concentrated Distributed Days

**Date:** 2026-03-19

### What was tested

Whether distributed days occurring *before* vs *after* the first concentrated spike within mixed episodes (M1-P97) have different hit rates. Pre-registered prediction: post-concentrated distributed should have higher TP rate (concentrated spike = cascade confirmation, remaining flow is mechanical late-deleveraging). 13 mixed episodes, 53 distributed days within them, plus 22 distributed days in non-mixed episodes.

- **Script:** `memories/mev/false_positive_anatomy.py` (extended)
- **Data:** `memories/mev/data/episode_arc_results.txt`
- **Dataset:** Same `liquidation_events_combined.csv`, M1-P97 classification, 14-day gap episode clustering

### What was measured

| Group | n | %decline | Median fwd_7d |
|---|---|---|---|
| All distributed (M1-P97) | 75 | 68.0% | -3.31% |
| Pre-concentrated (mixed eps) | 26 | 80.8% | -7.48% |
| Post-concentrated (mixed eps) | 27 | 70.4% | -4.70% |
| Non-mixed episodes | 22 | 50.0% | +0.34% |

Mann-Whitney pre vs post: U=272, p=0.163. Not significant at these sample sizes.

Trailing drawdown context: pre-concentrated median trail_7d = -5.86%, post-concentrated median trail_7d = -13.81%. Pre-concentrated days have moderate prior drawdowns; post-concentrated have deep ones (the spike itself caused the drawdown). Yet pre-concentrated predicts better — ruling out mean-reversion as the driver.

### The prediction was wrong — and why

The pre-registered prediction (post-concentrated > pre-concentrated TP rate) was wrong. Pre-concentrated is stronger: 80.8% vs 70.4%.

The error was treating the concentrated spike as an information event ("confirms the cascade is real") when it's primarily a physical event ("clears the most extreme positions from the book"). After clearing, the remaining position field is less stressed, so distributed flow has less predictive content. Pre-spike distributed flow is running in a hot feedback loop (maximum stress, positions accumulating near thresholds); post-spike is running in a cooler one (most extreme positions already cleared).

General principle: in systems with feedback (price → liquidation → more price decline), an event's *effect on the feedback loop* matters more than its *informational content*. The concentrated spike breaks the feedback loop by clearing extreme positions.

### The structural finding: non-mixed episode distributed days are noise

**Distributed days in episodes that never produce a concentrated spike have a 50.0% hit rate and median fwd_7d of +0.34%.** Essentially coin-flip — no signal.

The 68% overall hit rate for all distributed days is a blend of two populations:
- Escalating episodes (mixed, containing concentrated spikes): ~76% hit rate (53 days)
- Non-escalating episodes (never reach concentrated): ~50% hit rate (22 days)

Back-calculation confirms: 0.7 × 0.76 + 0.3 × 0.50 ≈ 68%, matching the observed overall rate.

**The distributed signal's value comes from being part of an episode that will escalate to a concentrated spike, not from distributed flow per se.** The "irreducible 32% FP rate" from iteration 13 is not irreducible — it's a mixture of two populations with different base rates. The problem is classifying which population you're in at the time of the distributed day.

### Measurement concern: forward-window contamination

Many pre-concentrated distributed days have the first concentrated spike within their 7-day forward return window. The 80.8% hit rate may partly measure "the concentrated spike is coming and it causes decline" rather than "distributed flow independently predicts decline." The claim that pre-concentrated is the strongest sub-signal requires checking how many pre-concentrated days have the concentrated spike inside the 7d window, and what the hit rate is for the subset where the gap exceeds 7 days.

The non-mixed episode finding (50% = noise) is unaffected by this concern.

### What was measured vs conjectured

**Measured:**
- Pre-concentrated distributed: n=26, 80.8% decline, median -7.48%
- Post-concentrated distributed: n=27, 70.4% decline, median -4.70%
- Non-mixed episode distributed: n=22, 50.0% decline, median +0.34%
- Pre vs post Mann-Whitney p=0.163
- Pre-concentrated trailing drawdown shallower than post (-5.86% vs -13.81%), yet forward returns worse — not mean-reversion
- Mixture decomposition: 0.7 × 0.76 + 0.3 × 0.50 ≈ 68%, consistent with observed overall rate

**Conjectured:**
- The concentrated spike's primary effect is physical (clears positions, breaks feedback loop), not informational (confirms cascade)
- The 80.8% pre-concentrated rate is likely inflated by forward-window contamination — some fraction of the decline is caused by the concentrated spike itself falling within the 7d return measurement
- Non-escalating episodes are events where lending stress was moderate enough that the market absorbed it without cascading — the 50% rate is the consequence, not an artifact
- OI confirmation at episode onset may predict escalation (episode reaches concentrated), not just improve day-level hit rate — this would reframe OI from marginal day-level filter (+3pp) to episode-level classifier

### What was not tested

- **Forward-window contamination check:** Among pre-concentrated days, how many have the first concentrated spike within 7 days? What is the hit rate for the subset where the gap exceeds 7 days? Determines whether pre-concentrated distributed flow has independent predictive content or is mechanically contaminated.
- **OI as escalation predictor:** For each episode beginning with distributed days, does a >3% OI drop within ±48h of episode onset predict whether the episode will subsequently produce a concentrated spike? Episode-level binary classification. Small n (~10-12 episodes in OI data period).
- **Exchange flow absorption signal:** Whether CEX net inflows distinguish escalating from non-escalating episodes. The non-mixed/50% finding predicts that non-escalating episodes should show evidence of off-chain absorption (elevated inflows).

---

## Iteration 15 — Forward-Window Contamination Check + OI Escalation Predictor

**Date:** 2026-03-19

### What was tested

Two follow-up tests from the episode arc probe (iteration 14): (A) whether the pre-concentrated 80.8% hit rate is an artifact of forward-window contamination (concentrated spike falling inside the 7d return measurement), and (B) whether OI drops at episode onset predict whether the episode will escalate to produce a concentrated spike.

- **Script:** `memories/mev/false_positive_anatomy.py` (extended)
- **Data:** `memories/mev/data/arc_followup_results.txt`
- **Dataset:** Same `liquidation_events_combined.csv` + `binance_oi_episodes.csv`

### What was measured

**Test A — Forward-window contamination:**

Of 26 pre-concentrated distributed days, 21 have the first concentrated spike within their 7-day forward return window (gap ≤7 days). Only 5 have clean forward windows (gap >7 days).

| Group | n | %decline | Median fwd_7d |
|---|---|---|---|
| Contaminated (spike ≤7d away) | 21 | 90.5% | -10.65% |
| Clean (spike >7d away) | 5 | 40.0% | +1.45% |
| Non-mixed baseline | 22 | 50.0% | +0.34% |

The clean subset (40%) is indistinguishable from the non-mixed baseline (50%). The pre-concentrated signal is almost entirely explained by the concentrated spike's price impact falling inside the measurement window. No independent predictive content detectable.

**Test B — OI as episode escalation predictor:**

Among 17 episodes with OI data (2024-03+), 15 had a >3% hourly OI drop near episode onset. The threshold fires for nearly every episode regardless of escalation.

| | Escalated | Not escalated | Total |
|--|-----------|---------------|-------|
| OI drop >3% | 9 | 6 | 15 |
| No OI drop | 2 | 0 | 2 |

Fisher's exact p=0.515. No magnitude separation either — non-escalating episodes show OI drops of -3.2% to -6.8%, fully overlapping the escalating range.

### What these results mean

**The pre-concentrated signal is a measurement artifact.** The 80.8% hit rate from iteration 14 was driven by the concentrated spike itself falling within the 7d forward return window. Distributed flow before a concentrated spike does not independently predict decline — it co-occurs with the spike, and the spike drives the measured return.

**OI does not predict episode escalation.** The >3% hourly OI drop fires for 15 of 17 episodes, both escalating and non-escalating. The cross-tier cascade framing from iteration 13 (OI confirmation = systematic stress) was analytically elegant but not supported as an operational classifier. The iteration 13 finding of 68→71% hit rate improvement with OI was likely noise.

### Revised decomposition of the distributed signal

The 68% overall hit rate for distributed days is an honest forecast (the correct base rate for a monitoring system) but the causal interpretation must be revised:

| Group | n | %decline | Status |
|---|---|---|---|
| Pre-concentrated (contaminated) | 21 | 90.5% | Artifact — spike drives return |
| Pre-concentrated (clean) | 5 | 40.0% | No signal (n too small, consistent with baseline) |
| Post-concentrated | 27 | 70.4% | **Clean signal** — no contamination |
| Non-mixed episodes | 22 | 50.0% | **Noise** — coin-flip |

**Post-concentrated distributed (70.4%, n=27) is the only clean sub-signal above baseline.** It's uncontaminated because the concentrated spike is behind it, not ahead. Mechanically: the spike clears extreme positions but leaves near-threshold positions that continue unwinding — aftershock prediction after the earthquake.

**Non-mixed episode distributed days (50%) are noise.** Moderate lending stress that the market absorbed without cascading.

### Revised interpretation of the magnitude classifier

The magnitude classifier's contribution is narrower than originally framed:

1. **Concentrated spike itself** — capitulation marker, positive forward return (+2.36% median). This finding is unaffected by the contamination analysis.
2. **Post-spike distributed flow** — aftershock prediction. After a concentrated spike, distributed flow signals 70% chance of further decline as near-threshold positions continue unwinding.
3. **Stand-alone distributed flow** (no episode context) — at or near baseline. Not an independent predictor of price direction.

The original claim "distributed events predict further declines with 68% hit rate" is correct as a statistical fact but misleading as a causal claim. The revised claim: "distributed flow is episode-context-dependent — meaningful after a concentrated spike (aftershock, 70%), noise without one (50%)."

The 68% remains the honest base rate for a monitoring system because the forward-window contamination is part of the natural data-generating process — in real-time, a distributed day that's actually pre-concentrated *will* see the spike within 7 days, so the 90% contaminated rate is the real outcome.

### Progressive sharpening across iterations 13-15

| Iteration | Claim | Status after probing |
|---|---|---|
| 13 | 32% FP rate is irreducible within lending features | Revised — it's two populations, not irreducible noise |
| 14 | Pre-concentrated distributed is strongest sub-signal (81%) | Refuted — forward-window artifact |
| 14 | Non-mixed episodes are noise (50%) | Confirmed — robust, no contamination concern |
| 14 | Post-concentrated is the feedback-loop-cooling aftershock | Confirmed — 70.4%, clean measurement |
| 13 | OI confirmation improves hit rate 68→71% | Weakened — OI fires for nearly everything, improvement likely noise |
| 15 | OI predicts episode escalation | Refuted — Fisher's p=0.515, threshold too common |

### What was measured vs conjectured

**Measured:**
- 21/26 pre-concentrated days have concentrated spike within 7d forward window
- Clean pre-concentrated subset (n=5): 40% hit rate, indistinguishable from 50% baseline
- OI escalation predictor: 15/17 episodes have >3% OI drop regardless of escalation, Fisher's p=0.515
- Post-concentrated distributed (n=27, 70.4%) confirmed as only clean sub-signal above baseline

**Conjectured:**
- The 68% overall rate is an honest forecast but mechanistically driven by proximity to concentrated spikes, not by distributed flow independently predicting decline
- The iteration 13 OI finding (68→71%) was likely noise given OI fires for nearly every episode
- Escalation prediction may require position-level monitoring (price proximity to large liquidation thresholds) rather than aggregate flow metrics — a different analytical mode than the statistical program conducted here
- The statistical probing of the distributed signal has reached natural diminishing returns — further refinement within the same data domain is unlikely to produce new findings

### What was not tested

- **Liquidation wall proximity as escalation predictor:** Whether price proximity to large lending liquidation thresholds at episode onset predicts escalation. The most structurally grounded candidate — the concentrated spike literally is a large position getting liquidated. But requires position-level snapshot data and faces dynamic management challenges (collateral top-ups, partial repayments). Different analytical mode from aggregate flow statistics.
- **Exchange flow absorption signal:** Whether CEX net inflows distinguish escalating from non-escalating episodes. Still testable with CoinMetrics data.
- **Post-concentrated distributed — further characterization:** Whether the 70.4% hit rate varies by distance from the concentrated spike, episode severity, or market regime. n=27 limits subdivision.

---

## Iteration 16 — Exchange Inflow/Outflow Around Liquidation Episodes

**Date:** 2026-03-19

### What was tested

Whether daily CEX exchange flows (CoinMetrics Community API, free tier) distinguish escalating from non-escalating liquidation episodes, and whether they separate true positive from false positive distributed days. Four tests designed around specific predictions from the episode arc findings.

- **Script:** `memories/mev/exchange_flows.py`
- **Data:** `memories/mev/data/exchange_flows.csv` (raw), `memories/mev/data/exchange_flow_results.txt`
- **Source:** CoinMetrics Community API, ETH metrics: FlowInExNtv/USD, FlowOutExNtv/USD, SplyExNtv. 1,538 daily observations, 2022-01-01 to 2026-03-18.
- **Derived metrics:** Net flow (USD) = inflow − outflow (positive = selling pressure). Rolling 30d z-score.

### What was measured

**Test 1 — Flow signature around episodes (±7d window):**
Escalating (mixed) episodes: median during-episode z-score = +0.09 (n=13). Non-escalating (distributed-only): median = +0.09 (n=11). Mann-Whitney p=0.954. Pre-episode z-scores: escalating +0.08, non-escalating -0.07, p=0.297. No separation in any window.

**Test 2 — Distributed TP vs FP flow:**
TP distributed days: median z-score +0.31 (n=51). FP distributed days: median +0.25 (n=24). Mann-Whitney p=0.755. Spearman r=0.057, p=0.630. Raw net USD also fails (p=0.590). Zero discriminating power.

**Test 3 — Absorption signature:**
Prediction: non-escalating (absorbed) episodes should show elevated net inflows (buyers absorbing stress). Result: escalating episodes median net flow -$2.2M/day, non-escalating -$15.5M/day. Mann-Whitney p=0.817. Weak wrong-direction trend. The absorption-via-exchange-buying hypothesis is not supported.

**Test 4 — Flow timing relative to concentrated spike:**
Peak daily net inflow relative to first concentrated spike: before in 7/13 episodes, after in 6/13. Median gap: -2.0 days. Essentially coin flip. No reliable timing relationship.

### What these results mean

**Daily exchange flow data adds no signal to the liquidation classification system.** All four tests are null — not marginal, not directional, but genuinely flat. Exchange flows do not distinguish escalating from non-escalating episodes, do not separate TP from FP distributed days, do not confirm the absorption hypothesis, and do not provide timing information around concentrated spikes.

### Why flow data fails on the escalation question

The escalation question — "will this moderate stress event hit a large concentrated position?" — is a **topology question**, not a flow question. It depends on where large lending positions sit relative to current price and whether price declines far enough to reach them. No aggregate flow metric captures position topology. Flow data measures the *consequences* of escalation (more selling, more exchange activity) and cannot predict escalation because consequences only become visible once escalation is already underway.

This explains the consistent null results across three data domains tested against the escalation prediction:
- On-chain lending features (iteration 13): six traits tested, none separate FP from TP
- OI/perp data (iteration 15): doesn't predict escalation at episode level (fires for 15/17 episodes)
- Exchange flows (this iteration): no signal at all

All three are flow-based or aggregate metrics. The only structurally grounded escalation predictor — liquidation wall proximity (price distance to large position thresholds) — is position-level data, a different analytical class.

### Operational conclusion

The 68% base rate for distributed days is what the monitoring system gets. The 50/70 decomposition (non-escalating = noise, post-concentrated = aftershock) is analytically informative — it explains why the system works when it works and fails when it fails — but it is not operationally accessible without the concentrated spike as a classifier.

The monitoring system's core output is the binary classification: "was today's liquidation spike capitulation (concentrated, positive forward return) or continuation (distributed, 68% negative)?" The post-concentrated aftershock signal (70%) provides marginally higher confidence after a capitulation event has already occurred but the operational delta is small (+2pp over baseline).

### What was measured vs conjectured

**Measured:**
- Four tests, all null: episode-level flow signature (p=0.954), TP/FP flow (p=0.755), absorption signature (p=0.817), flow timing (7/13 before, 6/13 after)
- Daily exchange flows provide zero discriminating power for the liquidation classification system
- Both escalating and non-escalating episodes show weak net outflows during stress

**Conjectured:**
- The escalation question is a topology question (position locations), not a flow question (aggregate activity) — explains why all flow-based tests fail
- Daily resolution being too coarse is the less likely explanation — Tests 1-3 show no directional lean that finer granularity could amplify
- The absorption mechanism (if it exists) may be structurally invisible to on-chain flow data — could operate through derivatives settlement, internal exchange transfers, or OTC desks

### What was not tested

- **Hourly exchange flow data:** Requires CoinMetrics Pro (paid). Could rescue Test 4 (flow timing) but unlikely to rescue Tests 1-3 given the absence of directional signal at daily level.
- **Per-exchange breakdown:** Whether specific exchanges (Binance, Coinbase) show different flow signatures during stress events. Requires CoinMetrics Pro.
- **Liquidation wall proximity as escalation predictor:** Parked as a different analytical mode (position-level monitoring vs aggregate flow statistics).

---

## Iteration 17 — Options IV Timing Probe (Deribit DVOL)

**Date:** 2026-03-19

### What was tested

Whether ETH implied volatility (Deribit DVOL index) spikes before, during, or after concentrated lending liquidation spikes. The position heterogeneity principle predicted options (effective 10-100x via delta) should react before perps (5-50x). Three tests: IV level around concentrated spikes, IV timing relative to concentrated spikes, and IV timing relative to OI drops.

- **Script:** `memories/mev/iv_timing.py`
- **Data:** `memories/mev/data/eth_iv_history.csv` (raw), `memories/mev/data/iv_timing_results.txt`
- **Source:** Deribit public API (`get_volatility_index_data`), no auth required. ETH DVOL daily, 2022-01-01 to 2026-03-19, 1,539 observations. DVOL range: 30.7–153.9, median 68.4.

### What was measured

**Test 1 — IV level around concentrated spikes:**
IV rises on 84.2% of concentrated days (baseline 43.8%). Median DVOL change (spike day vs 7d prior): +4.4 on concentrated days vs -0.6 baseline. Mann-Whitney p≈0.0000. Strong contemporaneous relationship — but both IV and liquidations respond to the same price crash. Not new information.

**Test 2 — IV timing relative to concentrated spike:**
Peak IV within ±7d of first concentrated spike across 13 escalating episodes: before spike in 1, same day in 5, after in 7. Median gap: +1.0 days. **IV peaks after the concentrated spike, not before.** The options market reacts to the cascade, not anticipates it.

**Test 3 — IV vs OI timing (2024-03+ episodes, n=11):**
IV peak vs OI trough: IV leads in 3, same day in 4, IV lags in 4. Median gap: 0.0 days. IV and OI are roughly co-temporal. IV does not provide earlier information than OI. Both tend to peak/trough slightly after the concentrated spike (median +1.0d for both).

### What these results mean

**IV does not provide early warning.** The original plan question was: "Does Deribit IV spike before, during, or after the perp OI drop? Is the vol expansion already priced?" Answer: during/after. Not priced ahead. This closes the "faster layer" hypothesis — options are not a faster signal than perps despite higher effective leverage.

**The information sequence is:** lending stress → OI drop ≈ IV spike → resolution. Neither derivative market provides warning that precedes the on-chain lending signal itself.

### Refinement of the position heterogeneity principle

The principle predicted options should react before perps due to higher effective leverage. This prediction failed. The explanation: **the principle applies to forced position closures, not to market pricing responses.**

- **Perp OI drops** are position events — forced liquidations closing positions. Governed by leverage thresholds.
- **IV changes** are pricing responses — market makers adjusting via delta hedging in response to realized volatility. Governed by pricing mechanisms, not leverage thresholds.

The principle's domain: temporal ordering in *forced liquidation cascades* scales with the leverage gap between position types. It does not extend to pricing mechanisms (IV, spreads, funding rates) which have their own timing dynamics independent of leverage structure.

This boundary condition prevents misapplication: without it, one would predict options should lead everything and waste time testing it. With it, one knows to only look for leverage-gap ordering among forced position events across tiers.

### Observation: post-capitulation vol-selling window

IV peaks ~1 day after the concentrated spike, while concentrated spikes tend to have positive forward returns (+2.36% median). This means IV is elevated and likely to revert precisely when the directional outlook turns favorable. This is a potential vol-selling window — but it uses the concentrated spike (from lending data) as the trigger, not IV as the signal. A trading implementation observation, not a new signal finding.

### What was measured vs conjectured

**Measured:**
- IV rises on 84.2% of concentrated days, median change +4.4 vs -0.6 baseline (p≈0.0000)
- Peak IV lags concentrated spike by median +1.0 days (1 before, 5 same day, 7 after)
- IV peak and OI trough are co-temporal (median gap 0.0 days)
- IV does not provide earlier information than OI

**Conjectured:**
- The position heterogeneity principle applies to forced closures only, not to market pricing responses — this explains why options don't lead despite higher effective leverage
- The vol-selling window (elevated IV + positive forward return post-spike) is a potential trading implementation detail, not tested as a strategy
- The information sequence (lending → OI ≈ IV → resolution) suggests the on-chain lending signal is the primary source, with derivative markets responding to rather than anticipating the cascade
