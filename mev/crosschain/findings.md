# Cross-Chain Flows — Findings

## 1. Summary

THORChain's directional swap data (19 pools, 1,460 days, hourly resolution for 5 crash windows) was tested for cross-chain flow signals that predict, coincide with, or lag ETH/BTC price movements. All directional flow signals failed — organic flows track persistent user-base composition, not market stress. What the data revealed instead: a precisely measurable arb correction mechanism (ratio ≈ 1.0 at daily resolution, scaling with profit opportunity at hourly resolution) that characterizes crash regimes in real-time but does not predict their onset.

## 2. Original Questions — Answers

### Where does money go during crypto stress events?

**Answer: The same place it always goes.** BTC holders sell BTC on THORChain 88% of all days. ETH holders accumulate ETH 65% of all days. During crashes, the same flows amplify with volume but the direction doesn't change.

| Regime | BTC organic_net mean | ETH organic_net mean |
|--------|---------------------|---------------------|
| BTC crash days | -$551M | +$179M |
| Normal days | -$516M | +$142M |
| BTC rally days | -$594M | +$154M |

BTC selling is slightly stronger on rally days than crash days. The "crash rotation" visible in raw btc_eth_rotation is the persistent user-composition flow amplified by higher volume during any volatile period. Stablecoin flight-to-safety is inverted: ratio is *lower* during crashes (0.028–0.044) than baseline (0.048), because total volume grows faster than stablecoin buying.

**Confidence: High.** Tested across 612 trade-era days, 5 crash episodes, 3 price regimes. Pattern is stable.

### Do cross-chain flow patterns predict, coincide with, or lag price movements?

**Answer: Neither predict nor lead.** Organic flow vs next-day ETH return: r ≈ -0.05. The 7-day momentum signal (Q1→Q5 spread of 2.84%) is a depth-regime artifact — it vanishes when splitting by pool depth (deep pools: flat, no signal; shallow pools: noisy, driven by a few bounce episodes). Organic 7d flow correlates with *past* 7d return (r = -0.133, contrarian buying) but past return has no forward power (r = 0.023).

**Confidence: High.** Multiple specifications tested. The causal pathway is blocked at every step.

### Is there arbitrage opportunity in cross-chain price dislocations during volatility?

**Answer: Dislocations exist but are small and mean-revert within one hour.** Mean absolute dislocation (THORChain vs CEX ETH price) ranges 0.35–0.61% during crash episodes, with max spikes to 4.5–6.1%. Lag-1 autocorrelation is negative or near-zero in 4/5 episodes (mean-reversion). The one persistent episode (Oct 2025, autocorr +0.247) had contested direction — arbs overcorrected to stale prices.

Practical barriers: THORChain ETH swaps take ~10–15 minutes for L1 confirmation. Mean dislocation of 0.5% minus swap fees (~0.3–0.5%) minus execution risk leaves near-zero expected profit. The arb opportunity is already being captured by trade-account bots with low-latency infrastructure.

**Confidence: Medium.** Hourly resolution may miss intra-hour opportunities that 5-min data would reveal. Oct 2025's persistence is untested at finer granularity.

## 3. What the Data Revealed Instead

### The organic/arb mirror

Every organic directional flow is offset by an equal and opposite arb correction. For BTC.BTC in the trade era, correction ratio (trade_net / -organic_net):

- Mean: 1.007, Median: 0.999, Std: 0.228 (filtered to days with |organic_net| > $100M; unfiltered std of 0.574 is inflated by noise on tiny-volume days)
- 1 of 531 qualifying days where arbs joined organic direction (ratio < 0): Jul 2, 2024
- Held through crashes, recoveries, calm markets, and $1.2B criminal laundering

This is the AMM arbitrage mechanism made visible: organic users push the pool price off-market, arbs push it back. The near-perfect 1:1 ratio means THORChain functions as a price-transparent passthrough — organic intent is fully legible from the data, and fully corrected.

### Arb precision scales with profit opportunity

Hourly correction ratio tightness (0.8 ≤ ratio ≤ 1.2) by organic impact size:

| Impact quintile (|organic_net| / depth) | ETH tight % | BTC tight % |
|----------------------------------------|-------------|-------------|
| Q1 (smallest impact) | 14% | 9% |
| Q3 (medium) | 39% | 35% |
| Q5 (largest impact) | 87% | 83% |

Arbs are rational profit-seekers. Large organic flows create large price dislocations, which create large arb profit, which attracts precise correction. Small flows create noise-level dislocations that arbs ignore.

### The shallower-pool paradox

Pool depth declined 70–90% from peak (BTC: 1,240 → 197 BTC, ETH: 13,377 → 2,534 ETH). Counterintuitively, shallower pools show *tighter* correction and *smaller* dislocations:

| Pool depth regime | Mean |dislocation| | Tight correction % |
|-------------------|---------------------|---------------------|
| Deep (~$60M) | 0.58% | 26% |
| Shallow (~$16M) | 0.35–0.52% | 57–63% |

Mechanism: same dollar volume in a shallower pool creates a larger price dislocation → larger arb profit → tighter correction → smaller residual dislocation. Depth decline makes correction *better*, not worse — until some threshold where arb capital itself becomes limiting (not yet observed).

### Two crash regimes: clear-direction vs contested

BTC-ETH hourly return correlation cleanly separates crash behavior:

| Episode | BTC-ETH corr | Correction std | Dislocation autocorr | Character |
|---------|-------------|---------------|---------------------|-----------|
| Aug 2024 | 0.880 | 0.152 | -0.135 | Clear direction, tight arb |
| Dec 2024 | 0.826 | 0.435 | +0.003 | Clear direction |
| Jan-Feb 2026 | 0.830 | 0.245 | +0.075 | Clear direction |
| Nov 2025 | 0.456 | 0.057 | -0.077 | Intermediate |
| Oct 2025 | 0.369 | 0.513 | +0.247 | Contested, oscillatory |

**Clear-direction** (corr > 0.8): Market agrees on direction. Arbs correct efficiently. Dislocations mean-revert within one hour.

**Contested** (corr < 0.5): BTC and ETH price targets move independently. Arbs correct to where the price *was*, not where it *is*. Overcorrections create new dislocations in the opposite direction. Dislocations persist across hours.

This is a real-time crash-type classifier, not a predictor. It describes the ongoing character of a crash — whether the market has consensus or not.

## 4. Dead Signals

| Signal | Test | Kill metric |
|--------|------|-------------|
| BTC→ETH rotation as crash predictor | Mean organic_net by BTC return tercile | Direction-indifferent: -$594M (rally) vs -$551M (crash) |
| Single-day flow → next-day price | Correlation | r ≈ -0.05 |
| 7-day flow momentum | Quintile analysis split by depth | Vanishes when depth-conditioned; deep pools flat |
| Flight-to-safety ratio | Crash vs baseline comparison | Inverted: 0.028–0.044 (crash) vs 0.048 (baseline) |
| Herfindahl concentration | Crash vs baseline | Range 0.191–0.240 vs baseline 0.226; no separation |
| Slip as stress indicator | Correlation with turnover and |return| | r = -0.01 to -0.16; governed by fee tiers not market stress |

## 5. Protocol Events as Data Contaminants

**THORFi lending/savers pause (Jan 24–26, 2025).** Node operators voted to suspend THORFi programs due to ~$200M insolvency risk. RUNE dropped ~30%. Correction ratio spiked to 2.65x (Jan 24) and went negative -0.15x (Jan 25) — the RUNE price crash shifted pool equilibria, creating abnormal arb dynamics unrelated to BTC/ETH market conditions. Flagged as `anomaly = 'thorfi_pause'` in flow_metrics.csv.

**Bybit hack laundering (Feb 22 – Mar 5, 2025).** $1.4B ETH stolen from Bybit by Lazarus Group. ~$1.2B laundered through THORChain (ETH → BTC) over 10 days. In the data: BTC.BTC organic_net = +$106B, ETH.ETH organic_net = -$107B over the window. These flows are classified as "organic" (not trade accounts) but represent criminal laundering, not market behavior. Volume hit 772x daily pool turnover (vs ~50x normal). Arb correction held at ratio ≈ 1.00 throughout — the mechanism is flow-agnostic. Flagged as `anomaly = 'bybit'`.

Both events contaminate any analysis that treats organic flows as market sentiment. The anomaly flags must be applied to exclude these windows.

## 6. Data Limitations

**Pool depth declined 70–90%.** BTC pool went from 1,240 BTC ($87M) to 197 BTC ($14M). ETH: 13,377 ($47M) to 2,534 ($5M). THORChain is increasingly a passthrough, not a liquidity venue. Same dollar flow creates ~6x more price impact now vs early 2024. Flow magnitudes are incomparable across time without depth normalization. When depth_norm_organic exceeds ~150x, the pool is a passthrough and the metric saturates.

**"Organic" label is behavioral, not intentional.** It captures all non-trade-account, non-synth, non-secured swaps — including criminal laundering (Bybit), whale portfolio rebalancing, and genuine market stress response, without distinction.

**Structural break at June 2024.** Synth-dominant era (Mar 2022 – May 2024) → trade-dominant era (Jul 2024+). Synth share dropped from 75% to 3% in one month as trade accounts replaced synth accounts. Cross-epoch analysis requires separate treatment. Only the trade era (21 months) has clean organic/arb decomposition.

**Only 5 clean crash episodes in the trade era.** Aug 2024, Dec 2024, Oct 2025, Nov 2025, Jan-Feb 2026. Small sample for crash-type classification. Two protocol anomaly windows (THORFi, Bybit) further reduce usable data.

**Hourly resolution may be too coarse.** THORChain swaps settle in minutes. The mean-reversion of dislocations within one hour could contain exploitable sub-hour structure that this analysis did not capture.

## 7. Connection to Prior Work

| Prior Phase | Finding | Cross-chain addition |
|-------------|---------|---------------------|
| Flow (Phase 1) | OI drops >4% precede lending liquidation by 37h, ~30% precision | THORChain organic flow carries no forward information (r ≈ 0). Cannot improve OI signal precision — the two data sources measure different things (CEX positioning vs cross-chain user-base behavior) |
| Position (Phase 2) | Real/phantom decomposition, position heterogeneity principle | Arb correction mechanism is a parallel instance of the heterogeneity principle: organic users and arb bots are distinct populations with ~10x+ leverage gap in information speed. The 1:1 correction emerges from this gap |
| Dynamics (Phase 4) | Recharge cycle, crash taxonomy, temporal concentration | The two crash regimes (clear-direction vs contested) map onto the dynamics crash taxonomy. Contested crashes (Oct 2025) may correspond to non-standard crash types where the market hasn't established directional consensus |
| Links (Phase 5) | VIX drives ETH/S&P coupling; macro crashes produce 2x amplification | BTC-ETH hourly correlation during crashes (0.37–0.88) is a crypto-internal analog of the ETH/S&P coupling. High VIX → high cross-asset correlation → cleaner arb correction. The Oct 2025 contested regime (low correlation) may correspond to crypto-native events where macro correlation doesn't apply |

**What this phase adds to crash anatomy:** The arb correction mechanism provides a real-time lens on crash character — whether the market has directional consensus or not. It cannot predict crashes, but it can characterize their type — clear-direction vs contested — as they unfold, observable within hours of crash onset via BTC-ETH hourly return correlation and correction ratio variance. This does not require waiting for liquidation data or OI changes.

## 8. Data Inventory

### Scripts
| File | Purpose |
|------|---------|
| `pull_data.py` | Daily swap/depth/TVL pull from Midgard API (96 calls) |
| `pull_hourly.py` | Hourly swap/depth pull for 5 crash windows (30 calls) |
| `compute_flows.py` | Per-pool and cross-pool daily flow metrics |
| `analyze_arb.py` | Slip, dislocation, correction, depth analysis |

### Data files (`data/`)
| File | Rows | Description |
|------|------|-------------|
| `swaps_daily.csv` | 27,740 | 19 pools × 1,460 days, all swap volume fields |
| `depths_daily.csv` | 5,840 | 4 major pools × 1,460 days, pool depth and price |
| `tvl_daily.csv` | 1,460 | Aggregate THORChain TVL |
| `flow_metrics.csv` | 27,740 | Per-pool daily: organic/trade/synth/secured nets, arb_share, correction_ratio, depth_norm, era, anomaly |
| `cross_pool_daily.csv` | 1,460 | Daily cross-pool: BTC/ETH organic_net, flight_to_safety, btc_eth_rotation, herfindahl |
| `hourly_swaps.csv` | 5,040 | 3 pools × 5 episodes × 336 hours |
| `hourly_depths.csv` | 5,040 | Same structure, pool depth and price per hour |
| `arb_analysis.csv` | 10 | 2 pools × 5 episodes: slip, dislocation, correction, depth metrics |
