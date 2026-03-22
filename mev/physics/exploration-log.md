# Physics Phase — Exploration Log

## Iteration 1: Funding Settlement → OI Closure Clustering

### Hypothesis
After negative funding settlements on Binance (every 8h), OI drops cluster in the 0-4h window following settlement more than after neutral/positive settlements. The mechanism: funding cost forces position closures on a predictable schedule.

### What was tested
- 1,137 matched settlements (919 episode + 267 control periods, combined after dedup).
- Binance 8h funding rate aligned with Bybit hourly OI (cross-exchange by design — testing market-wide positioning response to Binance-specific settlement).
- ETH hourly price used for price-conditional analysis.
- Settlements binned by funding rate: deeply negative (<-1bps, n=11), moderately negative (-1bps to 0, n=113), moderately positive (0 to 3bps, n=980), deeply positive (>3bps, n=33).
- OI change computed for 0-4h and 4-8h windows post-settlement.
- Pre-settlement OI change (-2h to 0h) checked for preemptive closing behavior.
- Price-conditional test: does funding sign add signal beyond price direction?

### What was measured
- **Negative vs positive funding, 0-4h OI change:** Neg mean = -0.37%, Pos mean = +0.04%. Welch t p=0.045, Mann-Whitney p=0.053. Marginal.
- **Deeply negative vs deeply positive:** Deep neg mean = -1.35%, Deep pos mean = -0.57%. Mann-Whitney p=0.27. Not significant. n=11 vs n=33.
- **Within deeply negative, 0-4h vs 4-8h:** 0-4h mean = -1.35%, 4-8h mean = +0.08%. Mann-Whitney p=0.16. Suggestive front-loading but not significant.
- **Pre-settlement OI change for deeply negative:** mean = +0.44%. OI was *increasing* before settlement. No preemptive closing.
- **Price-conditional (neg funding + price falling vs pos funding + price falling):** -0.47% vs -0.28%, p=0.34. Funding sign adds no signal beyond price direction.
- **Both extremes show OI drops:** Deeply positive funding (>3bps) also shows -0.57% OI decline in 0-4h. The effect is sign-symmetric, not funding-direction-specific.

### What was found
1. **Price direction dominates OI changes, not funding mechanics.** After conditioning on whether price was falling, funding sign adds no statistically significant information (p=0.34).
2. **Both funding extremes show OI drops.** Deeply negative and deeply positive funding both produce OI declines. This means extreme funding rates are a *measurement* of volatile/imbalanced regimes, not a *cause* of OI closure. Two thermometers, no thermostat.
3. **No preemptive closing.** OI grew +0.44% in the 2h before deeply negative settlements. Two possible explanations remain untested: (a) funding rate farming — shorts enter to capture the payment, growing OI; (b) compositional asymmetry — during rapid drops, voluntary short entry (unbounded) outpaces forced long exit (bounded by position size).
4. **The marginal signal (p≈0.05) in the broad negative-vs-positive comparison disappears under scrutiny.** It's driven by the confound that negative funding co-occurs with falling prices, which independently cause OI declines.

### Structural learning
The funding settlement process is **informationally constrained, not physically constrained**. Settlement times are fixed and known. Funding rates are published in advance. Any timing-based edge would be pure information — and the thesis predicts informational timing gets arbitraged. The negative result is consistent with the core thesis.

This re-categorizes the remaining probes:
- **Informational timing** (known schedule, visible parameters): #1 Funding (tested — negative), #6 Margin call cycles (same structural category — deprioritized).
- **Physical timing** (sequential dependencies, hard constraints): #3 Collateral chain propagation, #5 Validator exit queue, #7 Stablecoin mint/burn.
- **Hybrid**: #2 ETF flows (T+1 settlement is physical, daily flow publication is informational), #4 Liquidity withdrawal (behavioral, not a hard constraint).

### Artifacts
- Script: `memories/mev/physics/funding_oi_clustering.py`
- Results: `memories/mev/physics/funding_oi_results.txt`
- Plots: `memories/mev/physics/funding_oi_clustering.png`, `memories/mev/physics/funding_oi_timeprofile.png`

---

## Iteration 2: Collateral Chain Propagation — Burst Detection

### Hypothesis
Within spike days, Aave liquidations cluster in bursts with gaps (propagation waves) rather than distributing uniformly. If cascade = chain (liquidation A → price impact → liquidation B), expect sequential bursts with gaps reflecting execution latency. If cascade = independent, expect uniform/Poisson distribution proportional to price decline rate.

### What was tested
- 11,331 real liquidation events across 22 spike days (from 65,382 total Aave liquidation events, filtered to `category='real'` and spike day dates).
- Inter-event interval distribution computed at both event level and block level.
- Burst detection using gap thresholds (60s, 120s, 300s, 600s). Primary analysis at 120s.
- Statistical test: observed burst count vs uniform null (1,000 simulations per spike day).
- Collateral-type composition of bursts (WETH, wstETH, other).
- Burstiness metrics: Goh-Barabási B, coefficient of variation.
- Oracle update alignment attempted via Alchemy RPC (Chainlink ETH/USD AnswerUpdated events).

### What was measured
- **Same-block liquidations:** 7,528 of 11,309 intervals (66.6%) have Δt=0. Multiple positions liquidated in the same block.
- **Inter-block intervals:** Median 36s, mean 418s, std 1,828s. Coefficient of variation = 4.37 (exponential = 1.0). Extreme overdispersion.
- **Events per block:** Mean 2.98, median 1, max 35. 49.2% of blocks have >1 liquidation event.
- **Burstiness:** B = 0.77 (raw events), B = 0.63 (block-level). Both strongly bursty, far from Poisson.
- **Burst detection (120s threshold):** 1,114 bursts across all spike days. Median inter-burst gap: 456s (7.6 min). Median burst duration: 60s. 40.7% single-event bursts.
- **Null comparison:** 21/21 spike days with ≥50 events reject uniform null at p < 0.001.
- **Max burst sizes:** 377 (2024-08-05), 324 (2025-02-03), 281 (2025-04-07). Mega-bursts contain ~25-50% of a day's total events.
- **Collateral composition (multi-event bursts):** 77.6% WETH-only, 19.1% WETH+wstETH, 3.2% WETH+other, 0.2% mixed-other.
- **Oracle alignment:** Inconclusive. Alchemy free-tier block range limits (10 blocks/query) prevented fetching Chainlink AnswerUpdated events for spike day block ranges.

### What was found
1. **Liquidations are strongly bursty, not sequential chains.** The dominant pattern is simultaneous liquidation (same block), not A→B→C propagation. 67% of consecutive liquidations have zero time gap.
2. **The mechanism is oracle-gated batching, not cascade propagation.** Oracle price update → all positions crossing health factor threshold get liquidated simultaneously → quiet period → next oracle update → next batch. The "propagation delay" is the oracle update interval (~5-8 min during volatility), not execution time.
3. **Bursts are collateral-type homogeneous.** 78% single-type (WETH). Driven by a single price feed triggering multiple positions at similar health factors. wstETH positions join when the wstETH oracle also updates (19% mixed WETH+wstETH bursts).
4. **Characteristic inter-burst gap (~7.6 min) consistent with Chainlink volatility update cadence.** Chainlink ETH/USD updates on ~0.5-1% deviation threshold during volatility. The gap structure suggests bursts are gated by discrete oracle price steps.
5. **Mega-bursts reflect position density clustering.** Up to 377 positions liquidated in a single burst means hundreds of positions had health factors crossing 1.0 within one oracle deviation step (~0.5-1% price move). This is extreme positional herding.

### Conceptual reframe: threshold batch process, not cascade
The term "cascade" implies sequential propagation (A causes B). The data shows a **threshold batch process**: continuous price decline is quantized by oracle deviation thresholds into discrete batch liquidation events. The objects of interest are:
- The **position density map** (how many positions cluster at each price level)
- The **oracle step size** (the quantization resolution)
- Not propagation speed or execution latency

This connects to Phase 3's CAPO finding (49 liquidations in 84 seconds from one oracle misprice) — same mechanism, different trigger. Both are batch processes triggered by discrete oracle events.

### Connection to prior phases
- The **5-7 day cascade timescale** (Phase 4) is not a chain of individual liquidations. It is repeated oracle-gated batch events across days, with the multi-day structure reflecting the time for price to grind through successive clusters of liquidation prices.
- The **27h OI signal** (Phase 1) likely measures the buildup of vulnerable positions, not cascade propagation. OI contraction in perps precedes DeFi liquidations because CEX deleveraging is continuous (instant liquidations) while DeFi deleveraging is quantized (oracle-gated). The 27h gap may be the behavioral lag between perp closure (fast, continuous) and DeFi liquidation (slow, oracle-gated).
- **Phase 2's wall proximity** finding should predict mega-burst sizes: position density at a given price level determines how many liquidations fire when the oracle steps to that level.

### Artifacts
- Script: `memories/mev/physics/collateral_cascade.py`
- Results: `memories/mev/physics/cascade_results.txt`
- Plots: `memories/mev/physics/cascade_timeline.png`, `memories/mev/physics/cascade_intervals.png`

---

## Iteration 3: Self-Reinforcement Test — Burst Acceleration

### Hypothesis
If liquidation batch selling creates meaningful price impact, observed inter-burst gaps should be shorter than what external price velocity alone predicts. The ratio of observed/expected gap measures the self-reinforcement strength.

### What was tested
- 1,045 valid inter-burst gaps across 21 spike days (filtered for price velocity > 0.1%/h to exclude flat periods).
- Expected gap computed as: oracle deviation threshold (D) / local price velocity. Tested at D=0.5% and D=1.0%.
- Price velocity estimated from hourly ETH price data via linear interpolation at gap midpoints.
- Ratio = observed_gap / expected_gap. Ratio < 1 implies self-reinforcement.
- Intra-day acceleration: Spearman rank correlation between gap sequence number and ratio within each spike day.
- Liquidation volume: total collateral seized per spike day in ETH-equivalent terms (WETH direct + wstETH × 1.15).

### What was measured
- **Observed/expected ratio (D=0.5%):** Median = 0.39, mean = 0.98. Wilcoxon p ≈ 0 (W=84,464). One-sample t on log(ratio): t=-23.1, p ≈ 0.
- **Observed/expected ratio (D=1.0%):** Median = 0.19, mean = 0.49. Wilcoxon p ≈ 0.
- **Intra-day acceleration:** 13/21 days show negative Spearman ρ (ratio decreasing = acceleration). 4 days significant at p<0.01: 2022-05-11 (ρ=-0.45), 2025-03-10 (ρ=-0.69), 2025-11-04 (ρ=-0.51), 2026-01-31 (ρ=-0.39). Mean ρ across days = -0.088.
- **Strongest intra-day case:** 2025-03-10 — ratio drops from 0.53 (first half) to 0.07 (second half), a 7x acceleration.
- **Liquidation volume totals:** 422,652 ETH ($918M) across all spike days. Largest single day: 2024-08-05 = 80,849 ETH ($200M). 2025-11-04: wstETH seized (10,630) exceeds WETH (4,933) — wstETH now dominates late-2025 liquidations.
- **Volume context:** $200M forced sell on heaviest day against ~$5-15B daily CEX volume = 1-4% of daily volume. Concentrated in burst windows (2-3 hours), becomes 8-40% of volume in those windows.

### What was found — and what was not resolved

**The headline ratio (0.39) does not confirm self-reinforcement.** The resolution confound is severe: hourly price data averages velocity across the full hour, but crash activity is concentrated in specific hours where velocity is much higher. If a 10% daily drop is concentrated in 4-6 hours, true velocity during active hours is 5-6x the hourly average. Correcting for this would push ratios from 0.39 up to ~2.0-2.4, potentially flipping the sign entirely. The ratio < 1 partially (or fully) reflects temporal concentration of crashes, not liquidation-driven acceleration.

**Intra-day acceleration (4 significant cases) is more robust but ambiguous.** The hourly velocity bias is roughly constant within a spike day's active hours, so relative acceleration (ratio decreasing over the day) is less affected by the confound. However, the same pattern is equally consistent with:
- (a) Self-reinforcement: liquidation selling → price impact → faster oracle triggers
- (b) Liquidity thinning: LP withdrawal over the course of the crash (Phase 6: 8-27% depth loss) → same selling volume produces larger price impact later

These two mechanisms produce identical observables at available resolution. Distinguishing them requires minute-level price data.

**The liquidation volume numbers are the most useful concrete output.** 422,652 ETH / $918M total. The wstETH composition shift (absent pre-2024, dominant by late 2025) matches Phase 4's finding and has structural implications: wstETH liquidations route through a less liquid market (wstETH/ETH DEX pool), potentially producing more price impact per unit sold.

### Identified boundary
The self-reinforcement question cannot be cleanly resolved with hourly price data. Minute-level price data would allow computing velocity at the same timescale as burst gaps, eliminating the temporal averaging confound. The CAPO natural experiment (Phase 3: 49 liquidations from oracle error, not price movement) is the closest available instrument for causal estimation, but n=1.

**Best estimate from converging evidence:** The system has some positive feedback (Phase 5: non-zero effect), it's probably second-order (1-4% of daily volume concentrated in bursts), and the precise multiplier remains unmeasured.

### Artifacts
- Script: `memories/mev/physics/self_reinforcement.py`
- Results: `memories/mev/physics/reinforcement_results.txt`
- Plots: `memories/mev/physics/reinforcement_scatter.png`, `memories/mev/physics/reinforcement_intraday.png`, `memories/mev/physics/liquidation_volume.png`

---

## Iteration 4: ETF Flows and Inter-Day Cascade Structure

### Hypothesis
ETF outflows act as an exogenous force that pushes price into successive position clusters, determining whether a spike day is isolated or extends into a multi-day deleveraging event. The T+1 settlement lag creates physical selling pressure on the day after redemption filing.

### What was tested
- 14 spike days with BTC ETF coverage (2024-01-11 onward), 14 with ETH ETF coverage (2024-07-23 onward).
- Daily BTC and ETH ETF net flows pulled from SoSoValue (565 trading days, Jan 2024 – Mar 2026).
- Spike days classified: isolated (6), cluster-initiating (3), terminal (3), mid-cluster (2). Classification based on ±7 day proximity.
- Event study: average BTC/ETH ETF flows at each trading-day offset [-5, +5] around spike days, split by classification.
- Cumulative pre-3d, day-of, and post-3d flows per spike day.
- January 2025 mystery check: total and weekly ETF flows during Jan 2025.
- Predictive tests: Spearman correlation of pre-3d flow vs liquidation count/return; Mann-Whitney comparing continued-cluster vs terminal/isolated pre-flows.

### What was measured
- **Average BTC ETF flow on day -1 before spikes:** -$304M. Day 0: -$225M. 12/14 spike days show negative BTC flows in [-1, 0] window.
- **Cluster-initiating days:** Day -1 flow averages -$595M (2x the overall average).
- **Terminal days:** Flow reversal — day-of average +$167M (inflows begin at capitulation).
- **Multi-day cluster persistence:**
  - 2025_q4_chop (Nov 16→20→21): BTC pre -$621M, during -$552M, terminal reversal.
  - 2026_crash (Jan 31→Feb 5→6): BTC pre -$985M, mid -$434M, terminal +$371M.
- **ETH ETF amplification:** 2025-11-04: -$418M ETH ETF pre-3d + -$219M day-of. Nov 16-21 cluster: cumulative ETH outflows -$550M pre.
- **January 2025:** BTC ETF +$5,256M inflow, ETH ETF +$102M inflow. NOT ETF-driven. Brief ETH outflow -$187M in week of Jan 5-12 while BTC received +$313M = BTC-dominance rotation.
- **Predictive tests:** Pre-3d BTC flow vs liquidation count: ρ=+0.30, p=0.30. Pre-3d flow vs cluster continuation: U=23, p=0.55. Not significant (n too small).

### What was found
1. **ETF outflows consistently precede and accompany spike days.** 12/14 spike days show negative BTC flows in the [-1, 0] window. Cluster-initiating days have 2x stronger pre-outflows.
2. **Outflows persist through multi-day clusters.** The three clusters with ETF data all show sustained outflows across multiple days, with reversal at the terminal day.
3. **Terminal days show flow reversal.** Inflows begin at capitulation bottom — consistent with "selling pressure exhaustion" as the termination mechanism.
4. **ETH ETF outflows compound BTC-driven risk-off.** Worst clusters have simultaneous BTC + ETH outflows.
5. **January 2025 mystery partially resolved.** The -11.2% ETH residual was NOT ETF-driven (flows were strongly positive). The drawdown was CEX/perp-driven or macro repositioning through non-ETF channels. Brief ETH→BTC rotation visible in week of Jan 5-12.
6. **Predictive power not confirmed at n=14.** Patterns are visible in the event study but cannot achieve statistical significance.
7. **ETF outflows are necessary but not sufficient for cluster extension.** Isolated spike days with large negative pre-flows (2025-02-28: -$2,147M; 2025-03-10: -$582M; 2025-11-04: -$867M) did not produce multi-day clusters. The model predicts extension requires *both* external pressure (ETF outflows) *and* sufficient position density at the next price level (Phase 2 fuel map).
8. **Two counter-examples are purely endogenous events.** 2025-02-03 (+$999M pre-3d) and 2025-10-10 (+$1,514M pre-3d) are isolated spike days during net-positive ETF flow periods — DeFi-specific triggers without institutional selling pressure.

### Artifacts
- Script: `memories/mev/physics/etf_flows.py`
- Data: `memories/mev/physics/data/etf_daily_flows.csv` (565 rows, Jan 2024 – Mar 2026)
- Results: `memories/mev/physics/etf_results.txt`
- Plots: `memories/mev/physics/etf_event_study.png`, `memories/mev/physics/etf_severity.png`, `memories/mev/physics/etf_timeline.png`

---

## Phase Consolidation: Crash Lifecycle Model

This phase tested 4 probes across the 8 physical processes identified in the plan. The core output is not a set of individual timing signals but a **mechanistic model of the crash lifecycle** that connects findings from all prior phases.

### The model

**Stage 1 — Trigger.** External (macro shock → ETF redemption wave) or endogenous (position breach, oracle event). ETF-accompanied triggers produce multi-day events; non-ETF triggers produce isolated events.

**Stage 2 — Within-day execution.** Oracle-gated threshold batching. Continuous price decline is quantized by Chainlink oracle deviation thresholds (~0.5-1%) into discrete batch liquidation events. Each oracle update triggers simultaneous liquidation of all positions crossing health factor 1.0 at that price (67% same-block). Batch size determined by position density at that price level (Phase 2 topology). Characteristic inter-burst gap: ~7.6 minutes during volatility. Bursts are collateral-type homogeneous (78% WETH-only).

**Stage 3 — Within-day feedback.** Some positive feedback exists (Phase 5: ~100bps extra decline per 100 liquidations). Magnitude uncertain — hourly price data insufficient to separate self-reinforcement from velocity clustering and liquidity thinning. Best estimate: second-order effect, 1-4% of daily volume concentrated in bursts.

**Stage 4 — Inter-day extension.** Determined by whether external selling pressure (ETF settlement, continued macro stress) pushes price to the next position cluster. Multi-day extension requires *both* external pressure *and* sufficient position density at the next level. ETF outflows persist through clusters (3-5 trading days), which aligns with Phase 4's 5-7 day cascade timescale.

**Stage 5 — Termination.** Flow reversal (ETF inflows begin) + position cluster exhaustion (insufficient density to sustain spike days). Terminal spike days show positive ETF flows on day-of or post-3d.

### How this connects prior phases

| Prior Phase | Finding | Physics Mechanism |
|------------|---------|-------------------|
| Phase 1 (Flow) | 27h OI → liquidation lead | CEX deleveraging is continuous; DeFi deleveraging is oracle-gated. The 27h gap is the behavioral lag between fast perp closure and slow on-chain liquidation. |
| Phase 2 (Position) | Wall proximity predicts severity | Position density at each price level determines batch size when oracle steps to that level. |
| Phase 3 (Correlation) | CAPO 84-second cascade | Same oracle-gated batch mechanism, different trigger (misprice vs real decline). |
| Phase 4 (Dynamics) | 5-7 day cascade, 3 spike days = 45-89% | Repeated oracle-gated batching across days. Multi-day structure from external pressure (ETF flows) pushing price through successive position clusters. |
| Phase 5 (Links) | DeFi amplifies crashes ~100bps/100 liqs | Second-order positive feedback within the batch process. Measurably non-zero but not the primary driver. |
| Phase 6 (Crosschain) | 8-27% LP withdrawal, 1h dislocation mean-reversion | Liquidity thinning amplifies later batches within a spike day. Dislocation mean-reversion timescale (~1h) reflects cross-venue arb settlement. |

### What was not tested
- **#4 Liquidity withdrawal dynamics:** Behavioral, not hard physical constraint. Partially addressed by Phase 6's LP withdrawal finding.
- **#5 Validator exit queue:** Rate-limited physical process but operates on weeks-to-months timescale — too slow for crash dynamics.
- **#6 Margin call cycles:** Informationally constrained (predictable banking hours). Same structural category as funding settlements (probe #1). Deprioritized after probe #1 negative result.
- **#7 Stablecoin mint/burn latency:** Physical process (fiat settlement) but connects to crashes only indirectly through stablecoin demand.

### Identified boundaries
- Self-reinforcement magnitude: cannot resolve with hourly price data. Requires minute-level price or a natural experiment.
- ETF causal direction: cannot determine whether outflows cause declines or co-respond to macro signals. n=14 spike days, n=3 clusters.
- Oracle alignment: burst gaps are consistent with Chainlink update cadence but direct confirmation requires archive RPC access.
- The model produces regime classifiers (ETF flow sign classifies cascade type), not event predictors.

### All artifacts
| File | Description |
|------|-------------|
| `physics/funding_oi_clustering.py` | Probe #1: funding → OI analysis |
| `physics/funding_oi_results.txt` | Probe #1 results |
| `physics/collateral_cascade.py` | Probe #3: burst detection |
| `physics/cascade_results.txt` | Probe #3 results |
| `physics/self_reinforcement.py` | Probe #3b: self-reinforcement test |
| `physics/reinforcement_results.txt` | Probe #3b results |
| `physics/etf_flows.py` | Probe #2: ETF flow analysis |
| `physics/etf_results.txt` | Probe #2 results |
| `physics/data/etf_daily_flows.csv` | ETF daily flow data (Jan 2024 – Mar 2026) |
| `physics/funding_oi_clustering.png` | Probe #1 box plots |
| `physics/funding_oi_timeprofile.png` | Probe #1 time profiles |
| `physics/cascade_timeline.png` | Probe #3 spike day timelines |
| `physics/cascade_intervals.png` | Probe #3 interval distributions |
| `physics/reinforcement_scatter.png` | Probe #3b observed vs expected scatter |
| `physics/reinforcement_intraday.png` | Probe #3b intra-day acceleration |
| `physics/liquidation_volume.png` | Probe #3b liquidation volume per spike day |
| `physics/etf_event_study.png` | Probe #2 event study |
| `physics/etf_severity.png` | Probe #2 flow vs severity scatter |
| `physics/etf_timeline.png` | Probe #2 epoch timelines |
