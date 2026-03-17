# Boundary Study: Indicator Profiles at Regime Transitions

## Goal

Map which indicators carry information at which regime boundaries. Pure analysis — no strategy changes until the map is clear.

## Setup

**Regime detection:** 2-bit from sign(trend_8h) × sign(trend_48h), 5-min debounce.
**Data:** BTC IS datalog (Jul 2025 – Feb 2026), 779 episodes.
**Transition moment:** First bar where debounced regime changes.

At every transition, snapshot all indicators. Split by outcome. Test for separation.

## Transitions to Study

| Transition | n (IS) | Outcome split | Strategic question |
|------------|--------|---------------|--------------------|
| →C2 (pullback entry) | 185 | →C3 (81%) vs →C0 (19%) | Can we detect bad pullbacks early? |
| →C1 (reversal entry) | 204 | →C3 (22%) vs →C0 (78%) | Can we detect breakthroughs early? |
| →C3 (bull entry) | 189 | Duration / exit PnL | Can we time entry quality within C3? |
| →C0 (bear entry) | 201 | Duration / whether next C1 breaks through | Can we characterize bear severity? |

Priority: →C2 outcome (directly targets the main loss mechanism), then →C3 entry quality.

## Indicator Groups

### Trend channels (7)
`trend_1h, trend_4h, trend_8h, trend_16h, trend_24h, trend_48h, trend_96h`

Already know: trend_8h and trend_48h define the regime boundary (by construction at zero). The question is what the *other* trends look like — especially trend_4h (between the two regime bits), trend_16h/trend_24h (between 8h and 48h), and trend_96h (slower context).

### Trend-of-trends (5)
`tot_4h, tot_8h, tot_24h, tot_48h, tot_96h`

Rate of change of trend. tot_8h at a C2 entry tells you whether the 8h trend is *accelerating* through zero (sharp reversal) or *decelerating* near zero (lingering pullback). Hypothesis: accelerating-through C2s revert more reliably.

### OLS volatility (7)
`ols_vol_1h, ols_vol_4h, ols_vol_8h, ols_vol_16h, ols_vol_24h, ols_vol_48h, ols_vol_96h`

Residual dispersion around OLS trend. High vol at boundary = noisy transition, low vol = clean. Hypothesis: clean transitions (low vol_8h) resolve more predictably.

### Realized volatility (8)
`realized_vol_1h, realized_vol_4h, realized_vol_8h, realized_vol_12h, realized_vol_16h, realized_vol_24h, realized_vol_48h, realized_vol_96h`

Standard price volatility. Different from OLS vol (which measures residual around trend). Hypothesis: vol regime interacts with trend regime — high realized vol pullbacks more likely to collapse.

### Volume / order flow (12)
`volume_since_last, vd_since_last, cvd_slope_5m, cvd_slope_15m, cvd_accel, cvd_div_5m, cvd_div_15m, cvd_div_1h, vwap_divergence, vwap_div_slope_5m, vol_intensity_ratio, vol_velocity_1m`

Volume confirmation / divergence at transitions. CVD divergence at C2 entry: is volume confirming the pullback (sellers) or diverging (buyers on dip)? VWAP divergence: price below/above session VWAP at transition.

### Microstructure (12)
`ob_total_ratio_1s/1m/5m, ob100_ratio_1m, spread_bps_1s/1m/5m, spread_expansion, depth_asymmetry_10, liquidity_shift_15m, ob_imbalance_slope_5m, bid_absorption_1m, ask_absorption_1m`

Order book state at transition. Spread expansion = liquidity withdrawal. Depth asymmetry = directional pressure. Absorption = large orders being filled. These are fast signals — may not carry multi-hour information, but could qualify entry timing.

### Large orders (6)
`big_bid_sigma, big_bid_distance, big_bid_size, big_ask_sigma, big_ask_distance, big_ask_size, large_cluster_buy_volume, large_cluster_sell_volume`

Institutional footprint at transitions. Hypothesis: large bid clusters near price at C2 entry = support = more likely to revert to C3.

### Volume profile (24)
`vp{12h,24h,48h,96h}_{poc_dist, vah_dist, val_dist, vahe_dist, vale_dist, width}`

Price position relative to value area at transition. POC distance = how far from highest-volume price. VAH/VAL distance = position within value area. Width = how wide the value area is (consolidation vs trending). Hypothesis: pullbacks near POC revert, pullbacks at value area edge break.

### Goertzel / cyclical (6)
`goertzel_8h_mag/phase, goertzel_12h_mag/phase, goertzel_24h_mag/phase`

Spectral magnitude at key periods. High goertzel_8h_mag at C2 entry = strong 8h cycle = more likely periodic pullback (reverts). Low mag = trend break not cycle.

### Short-term price (3)
`price_trend_5m, price_trend_15m, price_accel`

Instantaneous price momentum at transition. Direction price is moving in the moment of regime change.

### Regime label
`tris_last_regime` — Trismegistus regime label. Possibly redundant with trend regime, but may carry independent information.

## Method

For each transition type:

### 1. Snapshot extraction
At every regime transition bar, record all indicator values. Also record outcome (next regime, episode duration, price change during episode).

### 2. Univariate separation
For binary outcomes (C2→C3 vs C2→C0):
- Mann-Whitney U per indicator (nonparametric, no distribution assumptions)
- AUC per indicator (same test, more interpretable scale)
- Effect size (Cohen's d or rank-biserial correlation)

Rank all indicators by AUC. Anything above 0.60 is potentially informative.

### 3. Correlation structure
Cluster the informative indicators. Many will be correlated (trend_4h ~ trend_8h, ols_vol_8h ~ realized_vol_8h). Identify independent information axes.

### 4. Conditional profiles
For the top indicators: plot distribution conditioned on outcome. Are they bimodal (clean separator) or shifted (marginal information)?

### 5. Interaction with existing model
The logistic exit scoring already uses trend_1h + trend_8h. Do additional indicators carry information *beyond* what the logistic already captures? Residual analysis: compute logistic P(bull), bin by decile, within each bin check if new indicator further separates outcomes.

## Output

A ranked table per transition type:

| Indicator | AUC | Effect size | Correlated with | Independent? | Residual AUC |
|-----------|-----|-------------|-----------------|--------------|--------------|

Plus conditional distribution plots for top candidates.

## What constitutes actionable

An indicator is actionable if:
1. AUC > 0.60 at a transition boundary
2. Carries information independent of trend_8h (residual AUC > 0.55)
3. Separation is robust across time (split-half stable)
4. Has a plausible mechanism (not just noise fit)

Results feed into strategy decisions but don't prescribe them. The fee constraint (0.18% RT, >0.36% gross/trade) still governs — any indicator that adds trades must clear this bar.
