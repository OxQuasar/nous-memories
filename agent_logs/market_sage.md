
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

### Boundary Study Scripts (Phase 17)
- 17_c2_boundary_study.py / 17_c2_boundary_output.txt — indicator ranking
- 17b_c2_followup.py / 17b_c2_followup_output.txt — correlation, operational splits, forward check
- 17c_c2_filter_ev.py / 17c_c2_filter_ev_output.txt — filter EV analysis

### Column Indices (0-indexed, for boundary study scripts)
- 0: timestamp, 2: price
- 32: trend_1h, 33: trend_4h, 34: trend_8h, 35: trend_16h, 36: trend_24h, 37: trend_48h, 38: trend_96h
- 39: tot_4h, 40: tot_8h, 41: tot_24h
- 45-48: ols_vol_{4,8,16,24}h, 52-56: realized_vol_{4,8,16,24}h
- 59: cvd_slope_5m, 63: cvd_div_15m, 65: vwap_divergence

# Governing Constraints

## Fee Floor
0.18% round-trip (0.045% per side × 2× leverage × 2 sides). Minimum viable trade: ~0.36% gross. 5-7 signals/month. **Every feature that increases trade count without proportionally increasing gross-per-trade is value-destructive.**

## C2 Episode Scale vs Fee Scale
C2 episode price moves average 0.2–0.6%. Fee per filter activation: 0.36%. **C2 episodes are too small for fee-bearing interventions.** Any strategy modification that adds trades within C2 is structurally negative. This is a general constraint, not specific to any indicator.

## 10× Scale Factor
Simulator DS30 trends are 10× smaller than research 5-min convention. Regime detection immune (sign-based). Logistic coefficients: multiply feature coefs by 10, intercept unchanged.

## Logistic Model Scope
Exit scoring validated at exits only. P(bull) > threshold is monotonically equivalent to trend_8h > constant. Logistic wrapping adds no information for binary decisions — use the underlying variable directly.

# Strategy Development Lessons (4 iterations)

## v2.1 → v3.0: Stop Loss Timescale Matching
3% stop fires during indicator lag. 8% stop = insurance only, never triggered. Net swing: +9.77%.

## v3.1: Shorts — Interaction Effects from New Entry Types
Short signal real (+14.89% gross). Flip mechanism changed long entry timing → longs degraded -11.37% (was +4.18%). **New entry types interact systemically.**

## v3.2: C1 Breakthrough — Value Trap
0.5/1.0 exposure split structurally loses vs full 1.0 C3 capture. 72 trades × 0.18% = 12.96% fee drag. **Trade count increases are destructive.**

## Phase 17 C2 Filter: Signal Real, Not Actionable
trend_24h separates C2 outcomes (AUC 0.765, p=3e-6) but C2 price moves are too small relative to fees. Filter EV: -6.45%. **Exit filters that add trades are subject to the same fee constraint as entry features.** The distinction between "adding entries" and "adding exits" doesn't change the fee math.

### Interaction Risk Taxonomy (from Phase 17 review)
- **New entry types** (v3.1 shorts, v3.2 C1 entries): HIGH interaction risk — create new trade populations that change existing trade timing.
- **Exit filters on existing positions** (C2 filter): LOW interaction risk — removes part of a hold, re-entry uses existing mechanism. Cost is quantifiable per-episode, not systemic.
- This distinction matters for evaluating future proposals.

## Exit Type Decomposition
- XC1 exits (Reversal): 10 trades, 70% WR, +38.16% — the entire edge
- XC0 exits (Bear): 13 trades, 23% WR, -33.98% — the entire cost

# Validated Signals

## trend_24h at C2 Entry (Phase 17, HIGH confidence)
- AUC: 0.765 (Bonferroni-corrected p = 3e-6)
- Split-half: 0.77/0.76 (unusually stable)
- Cohen's d: 0.815 (large effect)
- Independence: r_trend8h = 0.036, r_trend48h = 0.460, r_trend16h = 0.724
- Mechanism: measures how far negative signal has propagated up timescale hierarchy. Positive = shallow pullback (8h turned, deeper structure intact). Negative = deeper erosion.
- Operational split in P>0.80 bin: trend_24h > 0 → 85.4% success (n=123); trend_24h ≤ 0 → 44.4% success (n=36). OR=7.29, Fisher p<0.0001.
- Signal is primarily binary (sign sufficient for negative group, magnitude adds AUC 0.680 within positive group).
- Forward data directionally consistent (93.8% vs 70.0%, n=26).
- **Not actionable as C2 exit filter** at current fee structure. Filed for future use.

## Confirmed Nulls at C2 Entry (Phase 17, HIGH confidence)
- **Volatility** (OLS and realized, all timescales): AUC 0.50–0.54. Zero separation.
- **Volume/CVD** (cvd_slope_5m, cvd_div_15m, vwap_divergence): AUC 0.50–0.56. Zero separation.
- **Trend-of-trends** (tot_4h, tot_8h, tot_24h): Structurally zero during C2 regime. Cannot be used at C2 entry.
- **trend_96h**: AUC 0.512, not stable across halves.

These nulls permanently narrow the search space for C2-related improvements.

# Research Process Lessons

## Boundary Study Methodology (established Phase 17)
1. Define snapshot timing matching production (first bar after debounced transition)
2. Univariate AUC ranking with Bonferroni correction
3. Independence gate: correlation with ALL regime-defining variables (not just trend_8h — the Phase 17 script initially missed trend_48h)
4. Split-half stability (AUC direction must agree)
5. Residual AUC within logistic model bins
6. Compute per-episode EV before any strategy changes
7. Compare filter cost (fees × activations) against filter benefit (loss avoided - recovery missed)

## Pattern: When to Stop a Line
- Signal confirmed real → attempt operationalization → EV negative → file and move on
- Don't force actionability where the math says no
- Clean nulls are valuable — they permanently close search directions
- A complete cycle that produces "real signal, not actionable" is a success

## Pattern: Interaction Risk Assessment
Before any strategy change, classify it:
- Does it add new entry types? → HIGH risk (v3.1, v3.2 precedent)
- Does it modify existing holds? → LOW risk (quantifiable per-episode cost)
- Does it change trade count by >50%? → Almost certainly negative (fee constraint)

## Pattern: Regime Model Has No Hysteresis
A trade that survives a bad C2 (44.4% recovery) isn't weakened by having survived it. State resets to C3. Mid-trade pullback quality doesn't predict eventual trade outcome. Don't pursue trade-level analyses conditioned on C2 quality — sample size collapses and mechanism doesn't support it.

# Key Insights

## Debouncing
5-minute debounce eliminates per-second flicker. Without: ~194 trades/month (all losers). With: ~7/month (research-aligned).

## Regime Model as State Labeler, Not Timing Tool
Labels states correctly but doesn't say when to enter within a regime. Entry timing is the unsolved problem.

## Complement Symmetry and Shorts
C0 shorts mirror C3 longs (+27.06% from 6h+ shorts). Requires: isolated execution, no flip mechanism, context gating.

# Forward Monitoring

1. **Topology violations**: count forbidden transitions. Expected: 0.
2. **Exit AUC (rolling 100)**: >0.90 working, 0.85-0.90 monitor, <0.80 stop.
3. **Ambiguous zone**: [0.10-0.50) bin population and accuracy.
4. **Forward reconciliation discrepancy**: 2.17% on forward data. Investigate separately.

## When to Refit
AUC < 0.85 on rolling 100 exits. Refit on most recent 6 months. Topology (2-bit) should never need changing.

# Standing Concerns

1. **Document drift**: log.md and next-steps.md have divergent sequencing for next steps. Reconcile after this cycle.
2. **Base rate was misestimated**: boundary-study.md cited 81/19 split; actual was 77.3/22.7 (143/42). Future planning should use measured numbers.
3. **Improvement axis narrowing**: C2 exit filters are out. C0 shorts are out (interaction). C1 breakthroughs are out (value trap). The remaining axes are: →C3 entry quality (next cycle) and isolated C0 shorts (deferred, requires architectural change). If →C3 entry quality also hits the fee wall, the strategy may be at its structural ceiling for this fee regime.
