
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
- Strategy Code: ~/henry/callandor/strategy/strategies/regime_cycle.go

# How to test a new strategy 

1. Create a new strategy file in Henry: callandor/strategy/strategies
2. Launch a Callandor simulator backtest 
    - go run . backtest-strategy -s [strategy_name] -p 1 -m 5 # first week (-p) of 5 months (-m)
        - Do not run more than 12 weeks (m * parallel_runs) at a time due to memory limits. 
    - go run . backtest-strategy -s [strategy_name]  --start 2025-10-01 --end 2025-10-30
        - Due to chunked loading can run --start to --end timeframes of arbitrary length. (But cannot exceed 5 parallel workers)
3. Add/Change logging capabilites to extract data from runs as needed

Refer to henry/CLAUDE.md for additional guidelines
Log strategy WIP status and new hypotheses into memories/arch/henry-strategy.md
Log detailed notes about strategy into memories/markets/[folder_for_strategy]

# Operational Knowledge

## Backtesting
- `-p N` selects which week within each month (rotation). Use different -p values for independent samples.
- `-m N` sets months. Each period = 1 month chunk. N periods run sequentially.
- `--start` / `--end` for arbitrary date ranges (no -p/-m needed).
- Backtest runtime: ~2 min/period with modules disabled, ~10 min with modules enabled.
- Log files: `/tmp/rc{version}_{period}.log` naming convention.
- Reconciliation: check FuturesPM vs TradeCapture discrepancy. <0.1% is clean. Forward data has a known 2.17% gap (investigate separately).

## IsSet() Bug (FIXED)
- `ModuleRequirements.IsSet()` in `strategy/interface.go` returned false when all module booleans were false.
- Fix: also check `IndicatorRetention > 0 || IndicatorWarmupHours > 0`.
- Impact: 3× backtest speedup (~2 min vs ~50 min per period).

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
- Already applied in regime_cycle.go constants (c2CoefT8h = 3485330.0, etc.)

## Datalog Column Availability for Boundary Studies
- Intermediate trends: trend_4h(33), trend_16h(35), trend_24h(36), trend_96h(38)
- Trend-of-trends: tot_4h(39), tot_8h(40), tot_24h(41) — NOTE: structurally zero during C2 regime
- OLS volatility: ols_vol_4h(45), ols_vol_8h(46), ols_vol_16h(47), ols_vol_24h(48)
- Realized vol: realized_vol_4h(52), realized_vol_8h(53), realized_vol_16h(55), realized_vol_24h(56)
- Volume/CVD: cvd_slope_5m(59), cvd_div_15m(63), vwap_divergence(65)
- Not yet tested: microstructure, order book, large orders, volume profile, Goertzel

# Workflow Lessons

## Strategy Development Process
1. Start with simplest possible version. Measure baseline.
2. Add ONE feature at a time. Run all periods. Compare to baseline.
3. Check for interaction effects: does the new feature degrade existing signals?
4. **Gross-per-trade is the gate metric**, not total PnL. Fee floor = 0.36% at 0.18% RT.
5. If total trade count increases significantly, almost certainly net-negative.

## Model Grading Process
1. Gate 0: trend divergence check (simulator native vs recomputed). Halt if >10%.
2. Topology violations (zero tolerance post-debounce).
3. Episode statistics (count, duration, regime distribution).
4. Jump chain Frobenius distance vs reference.
5. Exit AUC (>0.90 pass, <0.85 fail).
6. Calibration (bimodal check for C1; C2 calibration structurally inapplicable at exits).

## Boundary Study Process (Established in Cycle 1)
1. Define transition type and outcome variable (binary for C2/C1, continuous for C3/C0)
2. Snapshot indicators at transition entry (first bar post-debounce)
3. Compute per-indicator: AUC, Cohen's d, correlation with trend_8h, split-half stability, Bonferroni-corrected p
4. Gate candidates: AUC > 0.60, |r_trend8h| < 0.7, split-half stable
5. Residual analysis: does indicator add info beyond existing logistic model? (bin by P, compute within-bin AUC)
6. If candidates pass all gates: characterize (cross-correlation matrix, continuous vs binary, forward check)
7. Compute filter EV before strategy changes (per-episode PnL × filter accuracy − fee cost)

## Key Insight: Fee Structure as Binding Constraint
The 0.18% round-trip fee creates a hard floor: any trade must generate >0.36% gross to be viable. The regime model produces ~5-7 signals/month. Three attempts to add more signals (C0 shorts, C1 breakthroughs) all failed because they increased trade count 3-4× while diluting gross-per-trade below the fee floor. Future improvements must increase per-trade quality, not trade quantity.

## C2 Episodes Are Too Small for Fee-Bearing Interventions
C2 episode price moves average 0.2-0.6% (both directions). This is in the same range as the 0.36% RT fee. Even with a perfect filter, the expected loss avoided per true positive (~0.62%) minus fees (~0.36%) leaves only ~0.26% per correct filter activation — which is wiped out by false positive costs (recovery missed + fee). **Any strategy modification at C2 that adds round-trips is structurally negative EV.** C2 improvements must be fee-free (e.g., information for position sizing at C3 entry, not mid-hold exits).

## Interaction Effects Are the Dominant Failure Mode
Both v3.1 (shorts) and v3.2 (breakthroughs) degraded the core C3 long signal through entry timing changes — even though both new features had positive gross signals in isolation. Any new feature must be tested with the constraint: "do existing signals degrade?" If longs go from +4.18% to negative, the feature is rejected regardless of its own contribution. Note: C2 exit filters are categorically different (removing part of a hold, not adding entries) and have lower interaction risk — but failed on economics, not interaction.

## Boundary Study Cycle Workflow (What Worked)
- **Targeted hypothesis-driven subset beats full sweep.** 18 indicators (mechanistically motivated) on 185 episodes, not 90+ indicators. Reduces multiple comparisons, faster execution.
- **Independence testing is essential.** Check correlation with ALL regime-defining variables (trend_8h AND trend_48h), not just the primary one. Script 17 only checked trend_8h; 17b had to add trend_48h check.
- **EV calculation before strategy changes.** Script 17c prevented premature implementation of a filter that looked compelling on AUC/split-half but had negative expected value. Always compute the economics.
- **The "lower bound" caveat can be wrong.** The initial framing assumed C0 continuation losses were uncaptured, but the strategy exits at C0 entry = C2 exit. Understand the strategy mechanics before adding caveats.
- **Clean null results are valuable.** Volatility and volume carry zero C2-outcome information — permanently narrows the search space.

# Validated Signals (Not Yet Actionable)

## trend_24h at C2 Entry
- AUC 0.765 for C2→C3 vs C2→C0 (p=3e-6 Bonferroni)
- Independent of trend_8h (r=0.036) and trend_48h (r=0.460)
- Split-half stable (0.77/0.76), forward-consistent (93.8% vs 70.0%)
- Operational: within P>0.80 logistic bin, trend_24h sign → 85.4% vs 44.4% success (OR=7.29)
- Binary signal (sign) for negative values; continuous (magnitude matters, within-AUC 0.680) for positive
- trend_16h carries similar but weaker signal (AUC 0.688, r=0.724 with trend_24h)
- Stack depth (≥2 of {trend_4h, trend_16h, trend_24h} positive): 87% vs 58% success
- **Not actionable as exit filter** due to fee structure (filter EV = -6.45%)
- May become actionable with lower fees, or as input to C3 entry quality scoring
