
# Relevant Files

- Market Research Directory: memories/markets
- Henry Arch Doc: memories/arch/henry-arch
- Henry Strategy Doc: memories/arch/henry-strategy.md (Log and Update Trading Strategies Implementation Here)
- Strategy 01 Detailed Log: memories/markets/strategy01/log.md
- Research Next Steps: memories/markets/next-steps.md
- Boundary Study Design: memories/markets/boundary-study.md
- Findings: memories/markets/findings.md
- Grade 16 Script: memories/markets/16_grade_regime.py
- Grade 16 Output: memories/markets/16_grade_regime_output.txt
- C2 Boundary Study: memories/markets/17_c2_boundary_study.py
- C2 Boundary Output: memories/markets/17_c2_boundary_output.txt
- C2 Follow-up: memories/markets/17b_c2_followup.py / 17b_c2_followup_output.txt
- C2 Filter EV: memories/markets/17c_c2_filter_ev.py / 17c_c2_filter_ev_output.txt
- C3 Entry Quality: memories/markets/18_c3_entry_quality.py / 18_c3_entry_quality_output.txt
- Full IS Backtest: memories/markets/19_full_is_backtest_output.txt
- C1 Breakthrough EV: memories/markets/20_c1_breakthrough_ev.py / 20_c1_breakthrough_ev_output.txt
- Strategy Code: ~/henry/callandor/strategy/strategies/regime_cycle.go

# Research Phase Status: DIRECTIONAL TRADING CLOSED

The 2-bit regime model (trend_8h × trend_48h) is a validated state classifier that does NOT produce a tradeable directional strategy. All avenues exhausted:

| Avenue | Result | Evidence |
|--------|--------|----------|
| C3 confirmed entry (v3.0) | Gross negative (−0.555%) | Script 19 |
| C2 exit filter | Real signal, negative EV | Script 17c |
| C3 entry quality | Clean null (24 indicators) | Script 18 |
| C1 breakthrough EV | Logistic at chance at entry | Script 20 |
| C0 shorts (v3.1) | Interaction degraded longs | Strategy log |
| C1 entry (v3.2) | Value trap, −13.38% | Strategy log |
| Longer timescale (24h/96h) | Exit signal collapses (2.8pp gap) | Findings §6 |

**Pivot:** Model value is as risk overlay/state classifier for strategies with independently-sourced edge.

# How to test a new strategy 

1. Create a new strategy file in Henry: callandor/strategy/strategies
2. Launch a Callandor simulator backtest 
    - go run . backtest-strategy -s [strategy_name] -p 1 -m 5 # first week (-p) of 5 months (-m)
        - Do not run more than 8 weeks (m * parallel_runs) at a time due to memory limits. 
    - go run . backtest-strategy -s [strategy_name]  --start 2025-10-01 --end 2025-10-30
        - Can run --start to --end timeframes of max 2 months.
    - **CRITICAL:** Always run full IS period for validation. Partial rotations (-p N) produce biased samples.
3. Add/Change logging capabilites to extract data as needed
4. Go binary is at /snap/go/11103/bin/go (not on default PATH in agent sessions)

Refer to henry/CLAUDE.md for additional guidelines
Log strategy WIP status and new hypotheses into memories/arch/henry-strategy.md
Log detailed notes about strategy into memories/markets/[folder_for_strategy]

# Operational Knowledge

## Backtesting
- `-p N` selects which week within each month (rotation). **WARNING: produces biased samples.** The v3.0 +4.18% was a -p 2 artifact; full IS was -36.76%.
- `-m N` sets months. Each period = 1 month chunk.
- `--start` / `--end` for arbitrary date ranges (no -p/-m needed). **Preferred method.**
- Go binary path: `/snap/go/11103/bin/go` — must be added to PATH in agent sessions.
- Run from `~/henry` (not `~/henry/callandor`) — that's where main.go lives.
- Backtest runtime: ~2 min/period with modules disabled, ~12 min for full IS (7 months).
- Log files: `/tmp/rc{version}_{period}.log` naming convention.

## IsSet() Bug (FIXED)
- `ModuleRequirements.IsSet()` in `strategy/interface.go` returned false when all module booleans were false.
- Fix: also check `IndicatorRetention > 0 || IndicatorWarmupHours > 0`.

## Data Files
- IS data: `memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv` (18.5M rows, per-second)
- Forward data: `memories/markets/data/btc_datalog_2026-02-20_2026-03-13.csv` (1.9M rows, per-second)
- Key columns (0-indexed): timestamp=0, price=2, trend_1h=32, trend_4h=33, trend_8h=34, trend_16h=35, trend_24h=36, trend_48h=37, trend_96h=38
- Trend magnitudes: ~1e-5 (simulator DS30 units). Research uses ~1e-4 (5-min bar units). Factor of 10.

## Simulator Trend Computation
- trend_8h: DS30 subsampling → 960 OLS points over 8h (vs 96 points in 5-min research)
- trend_48h: DS300 subsampling → 576 OLS points (matches research)
- trend_1h: DS10 subsampling → 360 OLS points (vs 12 in research)
- `NormalizedTrendAndVolatility` in calcs.go: OLS slope / mean price → fractional rate per bar

## 10× Scale Factor
- Simulator trends are 10× smaller than research convention (DS30 vs 5-min bars)
- Regime detection: immune (sign-based)
- Logistic coefficients: multiply feature coefs by 10, intercept unchanged
- Already applied in regime_cycle.go constants

## Datalog Column Availability
- Intermediate trends: trend_4h(33), trend_16h(35), trend_24h(36), trend_96h(38)
- Trend-of-trends: tot_4h(39), tot_8h(40), tot_24h(41) — structurally zero during C2/C3 regimes
- OLS volatility: ols_vol_4h(45), ols_vol_8h(46), ols_vol_16h(47), ols_vol_24h(48)
- Realized vol: realized_vol_4h(52), realized_vol_8h(53), realized_vol_16h(55), realized_vol_24h(56)
- Volume/CVD: cvd_slope_5m(59), cvd_div_15m(63), vwap_divergence(65)
- Microstructure: ob_total_ratio_1m(70), spread_bps_1m(72), depth_asymmetry_10(73), ob_total_ratio_5m(74), liquidity_shift_15m(77), ob_imbalance_slope_5m(78)

# Key Findings & Meta-Insights

## Entry-Bar Prediction is Structurally Impossible (with trend-family indicators)
Scripts 18, 19, 20 all converge: at any regime entry, the defining trend variable has *just* crossed its threshold — magnitude is minimal and uninformative about what follows. Logistic models work at exits because the trend has developed magnitude by then. This pre-closes ALL future proposals to predict episode quality from entry-bar snapshots of OLS trends, vol, CVD, or microstructure. Entry-time prediction requires a fundamentally different information source.

## Fee Structure as Binding Constraint
0.18% RT fee creates a hard floor: any trade must generate >0.36% gross. But the base strategy has negative gross (-0.555%). Even zero-fee wouldn't make this profitable (gross is negative).

## C2 Episodes Are Too Small for Fee-Bearing Interventions
C2 price moves average 0.2-0.6% (both directions). Even perfect filters net ~0.26% after fees — wiped out by false positive costs.

## Sample Bias from -p Rotations
The -p N flag selects specific weeks within months. v3.0 showed +4.18% on -p 2 but -36.76% on full period. **Never validate on partial rotations.** Always use --start/--end for full period.

## Validated Signals (Not Actionable for Trading)
- **trend_24h at C2 entry:** AUC 0.765 (p=3e-6), independent of trend_8h/trend_48h, split-half stable. Real signal, but C2 moves ≈ fee cost → negative EV as exit filter.
- **Duration ≥6h separates good/bad C3 episodes:** sub-6h mean=-0.49%, ≥6h mean=+0.41%. But not predictable at entry.

# Workflow Lessons

## Strategy Development Process
1. **Always validate on full IS period first.** Partial samples are biased.
2. Gross-per-trade is the gate metric, not total PnL.
3. If total trade count increases significantly, almost certainly net-negative.
4. Check interaction effects: does the new feature degrade existing signals?

## Boundary Study Process
1. Define transition type and outcome variable
2. Snapshot indicators at transition entry (first bar post-debounce)
3. Compute per-indicator: AUC, Cohen's d, correlation with trend_8h, split-half stability, Bonferroni-corrected p
4. Gate candidates: AUC > 0.60, |r_trend8h| < 0.7, split-half stable
5. Residual analysis + EV computation before ANY strategy changes
6. Clean null results are valuable — permanently narrows search space

## Key Insight: State Identification ≠ Tradeable Edge
The regime model correctly identifies 4 market states with validated topology and high exit AUCs. But knowing you're in a bull regime doesn't mean you can profit from it — the confirmation lag means forward returns from confirmed states ≈ 0. The model's value is classificatory, not predictive of forward returns.

## Interaction Effects Are the Dominant Failure Mode
v3.1 (shorts) and v3.2 (breakthroughs) both degraded core signal through entry timing changes, even though features had positive signals in isolation.

## Confirmation-Based Entry Failure Mechanism
Backward-looking trend indicators confirm state *after* the move that created it. By the time both trend_8h AND trend_48h are positive (C3 confirmed), the move is already priced in. Residual forward return ≈ 0 or negative.
