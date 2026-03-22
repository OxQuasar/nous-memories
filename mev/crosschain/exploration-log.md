# Cross-Chain Flows — Exploration Log

## Iteration 1: Data Pull + Structure Discovery

### What was done

**Step 1: Full data pull completed.** Script at `pull_data.py`, data in `data/`.

| File | Rows | Coverage |
|------|------|----------|
| `swaps_daily.csv` | 27,740 | 19 pools × 1,460 days (2022-03-22 → 2026-03-20) |
| `depths_daily.csv` | 5,840 | 4 major pools × 1,460 days |
| `tvl_daily.csv` | 1,460 | Aggregate TVL, same range |

96 API calls, ~2 minutes. All pools have exactly 1,460 rows. Sanity-checked against plan's initial observations for Aug 2024 crash — all figures match.

**Pool coverage varies significantly.** Core pools (BTC, ETH, stablecoins, DOGE, LTC, AVAX, ATOM, BCH) have 1,200-1,455 active days. SOL.SOL has only 17 active days (started Feb 25, 2026). XRP.XRP has 287 (started Jun 2025). TRON pools have 166 (started Oct 2025). BSC.BNB started Sep 2023.

### What was found

#### Volume decomposition is exact

`totalVolumeUSD = organic + trade + synth + secured` with zero residual across all rows, where:
- organic = toAssetVolumeUSD + toRuneVolumeUSD
- trade = fromTradeVolumeUSD + toTradeVolumeUSD
- synth = synthMintVolumeUSD + synthRedeemVolumeUSD
- secured = fromSecuredVolumeUSD + toSecuredVolumeUSD

This means the plan's original `arb_share = (fromTrade + toTrade) / total` is correct but captures only one channel. The four channels each have directional axes:

| Signal | Definition | Meaning |
|--------|-----------|---------|
| organic_net | toAssetVolumeUSD - toRuneVolumeUSD | Non-arb directional intent |
| trade_net | toTradeVolumeUSD - fromTradeVolumeUSD | CEX-DEX gap direction (arb) |
| synth_net | synthMintVolumeUSD - synthRedeemVolumeUSD | Synthetic asset creation/destruction |
| secured_net | toSecuredVolumeUSD - fromSecuredVolumeUSD | L1 secured swap direction |

#### Three structural eras in the data

Measured on BTC.BTC monthly channel shares:

| Era | Dates | Organic % | Trade % | Synth % |
|-----|-------|-----------|---------|---------|
| Synth-dominant | Mar 2022 – May 2024 | 10-55% | 0% | 45-93% |
| Transition | June 2024 | 37% | 32% | 31% |
| Trade-dominant | Jul 2024 – present | 20-50% | 50-79% | ~0% |

The structural break at June 2024 is sharp — synth drops from 75% to 3% in one month while trade appears at 66%. This is a protocol-level change (trade accounts replacing synth accounts), not a market behavior shift.

#### The organic/arb mirror

For BTC.BTC in the trade era (Jul 2024+), across 545 days with |organic_net| > $100M:

- Correction ratio (trade_net / -organic_net): mean 1.008, median 1.000, std 0.241
- Only 2 days where arbs joined organic direction (ratio < 0): Jan 25 2025 and Jul 2 2024
- Only 6 days where arbs overshot >2x

The organic/arb mirror means: when organic users sell BTC on THORChain, arbs buy the same amount back (correcting the AMM price to CEX). The near-perfect 1:1 ratio held across crashes, recoveries, normal markets, and even criminal laundering events.

During Aug 2024 crash (measured values):
```
BTC.BTC Aug 3: organic=-1,415M, arb=+1,514M (residual +99M)
BTC.BTC Aug 5: organic=-595M,   arb=+709M   (residual +114M)
ETH.ETH Aug 3: organic=+792M,   arb=-748M   (residual +44M)
ETH.ETH Aug 5: organic=+343M,   arb=-362M   (residual -19M)
```

#### Two protocol anomaly windows identified

**THORFi lending/savers pause (Jan 24, 2025):** Node operators voted to suspend THORFi programs due to $200M insolvency risk. RUNE dropped ~30%. This explains the arb correction ratio anomaly on Jan 24 (ratio 2.65x) and Jan 25 (ratio -0.15x) — the RUNE crash shifted pool prices, creating abnormal arb dynamics. Not a market signal.

**Bybit hack laundering (Feb 22 – Mar 3, 2025):** $1.4B in ETH stolen from Bybit on Feb 21 by Lazarus Group. $1.2B laundered through THORChain by swapping ETH → BTC over 10 days. In the data: BTC.BTC organic_net = +$106B, ETH.ETH organic_net = -$107B. These flows show up as "organic" (not trade accounts) but are criminal laundering, not market behavior. Volume hit 772x daily pool turnover on Mar 2 (vs ~50x normal). Arb correction held at ratio ≈ 1.00 throughout. Volume dropped sharply on Mar 4 ($3.5B), normalized by Mar 6.

#### Correction ratio variance classifies crash types

Measured across five clean episodes:

| Episode | Correction Ratio 7d Std | Character |
|---------|------------------------|-----------|
| Aug 2024 | 0.152 | Sharp V, tight arb, unidirectional selling |
| Nov 2025 | 0.057 | Smooth decline, organic reversal at bottom |
| Jan-Feb 2026 | 0.245 | Deep crash, tight arb |
| Dec 2024 | 0.435 | Arb oscillation |
| Oct 2025 | 0.513 | Contested direction, most oscillation |

Low std = directional conviction (market agrees on direction). High std = contested (arbs overshoot/undershoot). This is a descriptor of ongoing crash character, not a predictor of crash onset.

#### Pool depth declining 70-90%

| Pool | Apr 2024 (peak) | Mar 2026 (now) | Decline |
|------|----------------|----------------|---------|
| BTC.BTC | 1,240 BTC ($87M) | 197 BTC ($14M) | -84% |
| ETH.ETH | 13,377 ETH ($47M) | 2,534 ETH ($5M) | -81% |

Decline is in native asset terms (not just USD), indicating LP withdrawal not just price decline. Member counts fell ~17% (BTC) and ~22% (ETH). THORFi insolvency and Bybit laundering event likely accelerated LP exit.

This means: same dollar volume creates ~6x more price impact now vs early 2024. Flow magnitudes are incomparable across time without depth normalization.

## Iteration 2: Flow Metrics + Signal Triage

### What was done

**Step 2: Flow metrics computed.** Script at `compute_flows.py`, outputs in `data/`.

| File | Rows | Content |
|------|------|---------|
| `flow_metrics.csv` | 27,740 | Per-pool per-day: organic_net, trade_net, synth_net, secured_net, arb_share, correction_ratio, pool_depth_usd, depth_norm_organic, depth_norm_volume, era, anomaly flags |
| `cross_pool_daily.csv` | 1,460 | Daily cross-pool: btc/eth organic_net, flight_to_safety, btc_eth_rotation, herfindahl, era, anomaly |

Validation confirmed: correction ratio for BTC.BTC in trade era (excluding anomalies) = mean 1.006, median 1.000. btc_eth_rotation is large-negative during all 5 crash episodes.

**Step 3: Flow-price correlation largely resolved during review discussions.** The planned lead/lag tests were addressed through targeted analysis rather than exhaustive computation. Key results below.

### What was found

#### BTC→ETH rotation is a persistent baseline, not a crash signal

BTC.BTC organic_net is negative on 88.4% of all days in the trade era. ETH.ETH organic_net is positive on 64.8% of days. This pattern is persistent regardless of price direction.

Measured by BTC return tercile:

| Regime | BTC organic_net mean | ETH organic_net mean |
|--------|---------------------|---------------------|
| BTC crash days | -551M | +179M |
| Normal days | -516M | +142M |
| BTC rally days | -594M | +154M |

BTC selling is slightly STRONGER on rally days than crash days. The "crash rotation" observed in 4/5 episodes is the same persistent user-composition flow (BTC holders converting to other assets via THORChain), amplified by higher volume during volatile periods in either direction. The btc_eth_rotation metric captures THORChain user base behavior, not market stress response.

#### Daily flow does not predict next-day price (confirmed)

Organic flow vs next-day ETH return: r ≈ -0.05. Depth-normalized flow: r ≈ -0.04. Organic contrarian buying (buying into falling market): 46% hit rate, mean +0.39% — indistinguishable from noise.

#### Multi-day ETH momentum signal is a depth-regime artifact

The 7-day rolling organic_net quintile analysis initially showed a monotonic contrarian pattern (Q1 heaviest selling → +1.85% forward 7d return, Q5 heaviest buying → -0.99%, spread 2.84%). However, splitting by pool depth:

| Depth Regime | Q1 (sell) fwd 7d | Q5 (buy) fwd 7d | Pattern |
|-------------|-----------------|-----------------|---------|
| Deep pool (>$41M median) | -2.17% | -1.95% | Flat. No signal. |
| Shallow pool (<$17M median) | +6.39% | +1.02% | Noisy, driven by bounce episodes |

The full-sample monotonicity was an artifact of mixing two depth regimes with different return distributions. The shallow-pool Q1 result is driven by a few extreme bounce episodes from oversold conditions on thin liquidity.

Additionally: organic 7d flow correlates with past 7d ETH return at r=-0.133 (contrarian dip-buying behavior). But past 7d return does not predict forward return (r=0.023). The causal pathway is blocked: organic flow tracks recent price (contrarian), but recent price has no forward predictive power.

#### Flight-to-safety ratio is weak or inverted

Flight_to_safety (stablecoin buy volume / total volume) is LOWER during crashes than baseline:

| Period | Flight-to-safety ratio |
|--------|----------------------|
| Baseline (trade era) | 0.048 |
| Aug 2024 crash | 0.044 |
| Dec 2024 crash | 0.033 |
| Jan-Feb 2026 crash | 0.028 |

Stablecoin buying volume grows more slowly than total volume during stress. Stablecoin organic_net is also inconsistent: Aug/Dec 2024 showed net USDT accumulation (+$3.5B, +$4.5B), but Nov 2025 and Jan-Feb 2026 showed net USDC selling. The flight-to-safety concept does not hold consistently in this data.

#### Herfindahl concentration does not distinguish crashes

Baseline mean: 0.226. Crash episodes range 0.191–0.240. Volume rises across all pools roughly proportionally during stress — there is no concentration into fewer pools.

#### Depth normalization breaks down for very shallow pools

ETH.ETH depth_norm_organic reaches +146 during Jan-Feb 2026 (pool at $5M depth with $700M+ daily flow). When daily turnover exceeds ~150-200x, the depth normalization metric becomes unreliable — the pool is functioning as a passthrough, not a liquidity venue. This corresponds to depth < ~$10M at current volume levels.

### Signal triage summary

**Dead (tested, no signal):**
- BTC→ETH rotation as crash signal (persistent baseline, price-direction-indifferent)
- Single-day flow → next-day price prediction (r ≈ 0)
- Multi-day ETH flow momentum predictor (depth-regime artifact)
- Flight-to-safety ratio (inverted during crashes)
- Herfindahl concentration (no crash discrimination)

**Alive (tested, robust):**
- Arb correction mechanism: ratio ≈ 1.0 ± 0.05, mechanically grounded, survived every test including criminal laundering
- Correction ratio variance as real-time crash-type classifier (low std = directional conviction, high std = contested)

**Untested (deferred to Steps 4-5):**
- Slip dynamics as liquidity stress indicator (averageSlip field available but unanalyzed)
- Price dislocation persistence: THORChain pool price vs CEX price, how long dislocations last
- Correction lag timing at hourly resolution
- Whether shallow pools show larger/longer dislocations (the depth decline may make this more measurable)
- Arb economics: estimated profit from correction activity

## Iteration 3: Arb Mechanics + Hourly Dynamics

### What was done

**Steps 4+5a combined: Hourly data pull + arb mechanism analysis.** Scripts at `pull_hourly.py` and `analyze_arb.py`.

Pulled hourly swap and depth data for 5 crash episodes × 3 pools (BTC.BTC, ETH.ETH, ETH.USDC) × 14-day windows:

| File | Rows | Content |
|------|------|---------|
| `hourly_swaps.csv` | 5,040 | 3 pools × 5 episodes × 336 hours |
| `hourly_depths.csv` | 5,040 | Same structure, pool depth and price per hour |
| `arb_analysis.csv` | 10 | 2 pools × 5 episodes, key metrics per episode |

Computed hourly TC-vs-CEX price dislocation for ETH.ETH using `eth_price_1h.csv` as CEX reference. Analyzed correction ratio tightness, slip, and depth drawdown at hourly resolution.

### What was found

#### Slip is not a useful stress indicator

`averageSlip` clusters around THORChain fee tiers (10 and 25 basis points) rather than reflecting market stress. Measured correlations:

| Relationship | BTC.BTC | ETH.ETH |
|-------------|---------|---------|
| slip vs turnover (depth_norm_volume) | -0.16 | -0.01 |
| slip vs absolute daily return | -0.03 | -0.05 |

Slip is governed by protocol fee structure, not market conditions. Dead signal.

#### Arb precision scales with profit opportunity (measured, both pools)

Hourly correction ratio tightness (0.8 ≤ ratio ≤ 1.2) by organic impact quintile (|organic_net| / pool_depth):

| Impact quintile | ETH.ETH tight % | BTC.BTC tight % |
|----------------|-----------------|-----------------|
| Q1 (lowest) | 14% | 9% |
| Q2 | 27% | 21% |
| Q3 | 39% | 35% |
| Q4 | 66% | 56% |
| Q5 (highest) | 87% | 83% |

Same pattern by pool depth quintile: shallowest pools (Q1, ~$15M) → 52-65% tight. Deepest (Q5, ~$65-140M) → 22-24% tight.

The mechanism: larger organic flow relative to pool depth creates a larger price dislocation, which creates a larger arb profit opportunity, which attracts more precise arb correction. Arbs are rational profit-seekers — they correct big dislocations precisely and ignore small ones.

Corollary: THORChain's declining pool depth (from $87M to $14M for BTC) paradoxically improves correction tightness by making each organic swap create a larger, more profitable-to-correct dislocation.

#### Price dislocations: mean-revert within 1 hour in 4/5 episodes

ETH.ETH price dislocation (THORChain pool price vs CEX price) across crash episodes:

| Episode | Mean Depth | Mean |Dislocation| | P90 |Dislocation| | Lag-1 Autocorrelation |
|---------|-----------|-------------------|-------------------|-----------------------|
| Aug 2024 | $39M | 0.61% | 1.40% | -0.135 (mean-reverting) |
| Dec 2024 | $63M | 0.58% | 1.22% | +0.009 (uncorrelated) |
| Oct 2025 | $23M | 0.54% | 1.14% | +0.247 (persistent) |
| Nov 2025 | $16M | 0.52% | 1.16% | -0.077 (mean-reverting) |
| Jan-Feb 2026 | $16M | 0.35% | 0.71% | +0.075 (weakly persistent) |

Counterintuitive finding: shallower pools do NOT show larger dislocations. Mean dislocation actually decreases with declining depth (0.61% at $39M → 0.35% at $16M). This is consistent with the arb-precision finding: shallower pools attract tighter arb correction, which reduces dislocation size despite higher price impact per swap.

#### Oct 2025 is uniquely oscillatory

Oct 2025 is the only episode with persistent positive dislocation autocorrelation at both lag-1 (+0.247) and lag-2 (+0.223). All other episodes show near-zero or negative lag-1 (mean-reversion). This aligns with the other Oct 2025 outlier measurements:

| Metric | Oct 2025 | Other episodes |
|--------|----------|---------------|
| Correction ratio 7d std | 0.513 | 0.057–0.435 |
| Dislocation lag-1 autocorr | +0.247 | -0.135 to +0.075 |
| BTC-ETH hourly return corr | 0.369 | 0.456–0.880 |
| BTC/ETH rotation | Both selling | BTC sell + ETH buy (4/4) |

These four measurements are different faces of the same state: the market lacked directional consensus. Low BTC-ETH correlation means the price target for each pool moved independently. Arbs correcting to where the price WAS (not where it IS) created overcorrections, which generated new dislocations in the opposite direction (the oscillation). High correction ratio variance is the daily expression of this hourly oscillation.

#### BTC-ETH hourly return correlation separates crash regimes

Measured across all 5 episodes:

| Episode | BTC-ETH Hourly Return Corr | Correction Quality |
|---------|---------------------------|-------------------|
| Aug 2024 | 0.880 | Clean, mean-reverting |
| Dec 2024 | 0.826 | Clean |
| Jan-Feb 2026 | 0.830 | Clean |
| Nov 2025 | 0.456 | Intermediate |
| Oct 2025 | 0.369 | Oscillatory, persistent dislocations |

When BTC and ETH move together (corr > 0.8), the price target is unambiguous and arbs correct efficiently. When correlation breaks down (corr < 0.5), each pool's target moves independently, arbs correct to stale prices, and dislocations persist.

#### High-volume hours have tighter correction than low-volume hours

Across all episodes and both pools, splitting hours by volume median:

- High-volume hours: 39-57% tight correction (BTC), 42-62% (ETH)
- Low-volume hours: 24-48% tight correction (BTC), 26-57% (ETH)

Arb bots are more active (and more precise) during high-activity periods.

#### LP withdrawal during crashes: 8-27% depth loss per episode

Pool depth (assetDepth) drawdown measured peak-to-trough within each crash episode:

| Episode | BTC depth loss | ETH depth loss |
|---------|---------------|----------------|
| Aug 2024 | -34% | -27% |
| Oct 2025 | -35% | -8% |
| Jan-Feb 2026 | -12% | -11% |

LPs withdraw during stress, reducing available liquidity. Aug 2024 and Oct 2025 saw the largest drawdowns. This LP exit amplifies the depth decline trend identified in Iteration 1.

### What remains untested

- 5-min resolution data for Oct 2025 to pin down the oscillation period (is it 15-20 min or 2-3 hours?)
- Whether BTC-ETH hourly correlation can be measured in real-time as a regime classifier (rolling 24h window)
- Cross-chain arb execution timing: can the oscillation windows in contested episodes be exploited given ~10-15 min ETH swap latency?
- The correction mechanism in the synth era (pre-June 2024): did synth_net play the corrective role that trade_net plays now?
- Whether other pools (DOGE, AVAX, etc.) show the same arb-precision-vs-impact relationship

## Iteration 4: Synthesis + Corrections

### What was done

**Step 6: Synthesis written.** `findings.md` produced covering all 8 sections: summary, original question answers, mechanism findings, dead signals, protocol events, data limitations, connection to prior work, data inventory.

**Review corrections applied:**
1. Correction ratio stats in findings.md updated to use |organic_net| > $100M filter (mean 1.007, median 0.999, std 0.228, 1 of 531 days with ratio < 0) instead of unfiltered (std 0.574, inflated by noise on tiny-volume days).
2. Comparative speed claim ("faster than other signals") softened to capability statement ("can characterize their type as they unfold") — the speed comparison was unmeasured.

### What was found

No new empirical findings. The synthesis confirmed internal consistency across all three prior iterations. The two corrections addressed a statistical reporting choice (filtered vs unfiltered) and an unsupported comparative claim.

### What remains untested

- 5-min resolution data for Oct 2025 to pin down the oscillation period
- Whether BTC-ETH hourly correlation can be measured in real-time as a regime classifier (rolling 24h window)
- Cross-chain arb execution timing: can the oscillation windows in contested episodes be exploited given ~10-15 min ETH swap latency?
- The correction mechanism in the synth era (pre-June 2024): did synth_net play the corrective role that trade_net plays now?
- Whether other pools (DOGE, AVAX, etc.) show the same arb-precision-vs-impact relationship
- Speed of crash-type classification via BTC-ETH correlation vs alternative real-time indicators (VIX intraday, OI changes, price momentum)
