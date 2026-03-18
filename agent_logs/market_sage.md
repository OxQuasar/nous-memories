
# Relevant Files

- Market Research Directory: memories/markets
- Henry Strategy Doc: memories/arch/henry-strategy.md
- Strategy 01 Log: memories/markets/strategy01/log.md
- Research Findings: memories/markets/findings.md
- Next Steps: memories/markets/next-steps.md
- Boundary Study Design: memories/markets/boundary-study.md
- Strategy Code: ~/henry/callandor/strategy/strategies/regime_cycle.go
- IS Data: memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv
- Forward Data: memories/markets/data/btc_datalog_2026-02-20_2026-03-13.csv

### Scripts (in memories/markets/)
- 17_c2_boundary_study.py / 17_c2_boundary_output.txt — C2 indicator ranking
- 17b_c2_followup.py / 17b_c2_followup_output.txt — correlation, operational splits, forward check
- 17c_c2_filter_ev.py / 17c_c2_filter_ev_output.txt — C2 filter EV analysis
- 18_c3_entry_quality.py / 18_c3_entry_quality_output.txt — C3 entry quality null (24 indicators)
- 19_full_is_backtest.py / 19_full_is_backtest_output.txt — full IS backtest (v3.0 invalidated)
- 20_c1_breakthrough_ev.py / 20_c1_breakthrough_ev_output.txt — C1 logistic at chance at entry

### Column Indices (0-indexed, for boundary study scripts)
- 0: timestamp, 2: price
- 32-38: trend_{1,4,8,16,24,48,96}h
- 39-41: tot_{4,8,24}h
- 45-48: ols_vol_{4,8,16,24}h, 52-56: realized_vol_{4,8,16,24}h
- 59: cvd_slope_5m, 63: cvd_div_15m, 65: vwap_divergence

# Current State — Directional Trading CLOSED

All directional trading avenues for the 2-bit regime model have been systematically tested and closed (7 avenues, 4 scripts, 4 strategy versions). The model is a **validated state classifier** (K=4 topology, AUC 0.957+, cross-asset) that does not produce a tradeable directional strategy. Its value is in state classification for use as infrastructure — risk labeling, position sizing — for strategies that source their edge elsewhere.

# Governing Constraints

## Fee Floor
0.18% round-trip (0.045% per side × 2× leverage × 2 sides). Minimum viable trade: ~0.36% gross. **Every feature that increases trade count without proportionally increasing gross-per-trade is value-destructive.**

## No Gross Edge
Full IS backtest (50 trades): gross/trade = −0.555% (95% CI: [−2.47%, +1.36%], p=0.563). The problem is not fees eating the edge — there is no edge. The strategy loses money before fees.

## Entry-Bar Prediction Is Structurally Impossible (Trend-Family Indicators)
Scripts 18, 19, 20 converge: **backward-looking trend indicators at regime entry contain no forward-predictive information about episode quality.** At any regime entry, the defining trend variable has just crossed its threshold — magnitude is minimal and uninformative. Logistic models work at exits (AUC 0.96+) because by exit time the trend has developed magnitude. This generalizes across ALL regime boundaries. Any entry-time prediction requires a fundamentally different information source, not a different indicator in the same family (OLS trends, vol, CVD, microstructure all null).

## Confirmation-Based Entry Failure
By the time trend_8h AND trend_48h both confirm positive (C3), the move that made them positive has already happened. You enter after confirmation and capture the residual forward return, which is empirically zero or negative. This is a fundamental limitation of confirmation-based trend following at this timescale.

## C2 Episode Scale vs Fee Scale
C2 episode price moves average 0.2–0.6%. Fee per filter activation: 0.36%. C2 episodes are too small for fee-bearing interventions.

## 10× Scale Factor
Simulator DS30 trends are 10× smaller than research 5-min convention. Regime detection immune (sign-based). Logistic coefficients: multiply feature coefs by 10, intercept unchanged.

# Strategy Development Lessons (4 iterations)

## v2.1 → v3.0: Stop Loss Timescale Matching
3% stop fires during indicator lag. 8% stop = insurance only, never triggered.

## v3.1: Shorts — Interaction Effects
Short signal real (+14.89% gross). Flip mechanism changed long entry timing → longs degraded. **New entry types interact systemically.**

## v3.2: C1 Breakthrough — Value Trap
0.5/1.0 exposure split structurally loses vs full 1.0 C3 capture. **Trade count increases are destructive.**

## v3.0 Full IS: Sample Artifact Discovery
Prior +4.18% baseline (23 trades, −p 2 rotation) was biased sample. Full IS: −36.76% (50 trades). **−p rotations select specific weeks → always use --start/--end for unbiased backtests.**

## Exit Type Decomposition (Full IS, 50 trades)
- XC1 exits: 18 trades, 56% WR, +37.62% — driven by 3 outlier wins (+24.67%, +20.89%, +10.26%)
- XC0 exits: 31 trades, 32% WR, −58.19% — the dominant loss mechanism
- 1 stop-out: −16.19%
- Temporal instability: first half −38.80%, second half +2.04%

# Validated Signals

## trend_24h at C2 Entry (Phase 17, HIGH confidence)
- AUC: 0.765 (Bonferroni-corrected p = 3e-6), split-half: 0.77/0.76
- Cohen's d: 0.815 (large effect)
- Independence: r_trend8h = 0.036, r_trend48h = 0.460
- Mechanism: measures how far negative signal has propagated up timescale hierarchy
- Operational split: trend_24h > 0 → 85.4% success (n=123); ≤ 0 → 44.4% (n=36)
- Forward-consistent (93.8% vs 70.0%, n=26)
- **Not actionable as C2 exit filter** at current fees (EV = −6.45%)

## Confirmed Nulls (HIGH confidence)

### At C2 Entry (Script 17)
- Volatility (OLS + realized, all timescales): AUC 0.50–0.54
- Volume/CVD: AUC 0.50–0.56
- Trend-of-trends: structurally zero during C2 regime
- trend_96h: AUC 0.512, unstable

### At C3 Entry (Script 18)
- All 24 indicators null after Bonferroni (n=189 episodes)
- Microstructure (ob_total_ratio, spread_bps, depth_asymmetry, liquidity_shift, ob_imbalance_slope): uniformly AUC ≈ 0.50
- All trends (4h–96h): |ρ| < 0.19 with price change
- Predecessor regime (C2 vs C1): AUC=0.581, not significant
- Best suggestive: realized_vol_24h (ρ=−0.20, p_corr=0.14), trend_1h for duration (AUC=0.623, p_corr=0.085)

### At C1 Entry (Script 20)
- C1 logistic: AUC=0.533 at entry (chance level). 187/204 episodes at P(bt) < 0.10
- Logistic is an exit-time tool; cannot be repurposed for entry prediction

### Duration: Real Effect, Not Predictable
- Sub-6h C3 episodes: mean −0.49%; ≥6h: mean +0.41%
- No entry-bar indicator predicts duration
- C3 quality is exogenously determined during the episode, not at entry

# Research Process Lessons

## Boundary Study Methodology
1. Snapshot at first bar after debounced transition
2. Univariate AUC ranking with Bonferroni correction
3. Independence gate: correlation with ALL regime-defining variables
4. Split-half stability
5. Residual AUC within logistic model bins
6. Per-episode EV before any strategy changes
7. Filter cost (fees × activations) vs filter benefit

## Pattern: When to Stop a Line
- Signal confirmed real → operationalization → EV negative → file and move on
- Clean nulls permanently close search directions
- "Real signal, not actionable" is a valid research outcome

## Pattern: Interaction Risk Assessment
- New entry types → HIGH risk (v3.1, v3.2)
- Modifications to existing holds → LOW risk (quantifiable per-episode)
- Trade count increase >50% → almost certainly negative

## Pattern: Sample Artifact Detection
- −p rotation backtests select biased week subsets
- Always validate with full period (--start/--end)
- Temporal stability check (first half vs second half) should be standard
- The temporal instability IS a finding — a real edge shouldn't concentrate in one calendar half

## Pattern: Outcome Variable Must Match Analysis Unit
- Trade-level labels (XC1/XC0) at n=23 → insufficient for AUC ranking
- Episode-level outcomes at n=189 → statistically adequate
- When episodes chain within trades, trade labels create correlated episode labels → inflated p-values

## Pattern: Distinguish Duration Filter from Entry Quality Signal
- An indicator that predicts duration but not price change is a duration filter, not an entry quality signal
- These map to different backlog items and different actionable levers

# Key Insights

## Debouncing
5-minute debounce eliminates per-second flicker. Without: ~194 trades/month. With: ~7/month.

## State Identification ≠ Tradeable Edge
The regime model correctly labels states (topology validated, exit AUCs high, cross-asset). But confirmed states don't predict positive forward returns. The model is a state classifier, not a signal source.

## Logistic Model Scope
Exit scoring validated at exits only. At entry, the defining variable has just crossed threshold → logistic correctly reports "no information." Models designed for exit-time measurement cannot be repurposed for entry-time prediction.

## Longer Timescale (24h/96h) Pre-Closed
Basis G exit signal gap = 2.8pp (vs 42.6pp for 8h/48h). The exit AUC that makes the model useful requires the 1:8 fast-to-medium ratio.

# Standing Concerns

1. **Forward reconciliation discrepancy**: 2.17% gap between FuturesPM and TradeCapture on forward data. Not investigated.
2. **Pivot track is undefined**: The regime model's value as infrastructure (risk overlay, sizing) is asserted but unprototyped. The first concrete test would be: apply regime labels to an independently-edged strategy and measure improvement. No such strategy currently exists in the pipeline.
3. **C0 shorts remain uninvestigated in isolation**: v3.1 shorts failed due to interaction (flip mechanism), not because the short signal was wrong (+27.06% from 6h+ shorts). Isolated evaluation would face the same entry-bar prediction problem, but the mechanism is different (shorting in confirmed bear, not entering confirmed bull). Low priority given overall closure.
