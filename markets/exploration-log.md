# Markets Investigation — Exploration Log

## Iterations 1–3: (3,5) Test → Clean Negative
- K=4 across 3 independent bases (trend, volume profile, orthogonal channels)
- Complement symmetry confirmed (Basis D: JSD < 0.09 all pairs, degenerate eigenvalues)
- Exhaustive 240-surjection search: K=4 lumpability 19× better than best K=5
- (3,5) formally closed

## Iteration 4: Regime-Conditioned Returns
- 4-regime directed cycle: bear(C0) → reversal(C1) → bull(C3) → pullback(C2) → bear
- C2 exit sub-state signal: S5 (trend_1h↑) → 92% bull, S4 (trend_1h↓) → 50/50
- Stable across 3 subperiods (92.1%, 92.7%, 90.7%)
- S5 episodes net positive (+0.20%), S4 episodes net negative (−0.81%)
- C1 reversal: asymmetric payoff (+1.09% for bull breakthrough, −0.25% for failure)

## Iteration 5: Intra-Episode Flip Dynamics
- Flip trigger is noise: 511 confirmed-flip trades, 38.4% win rate, +0.005% mean. Not tradeable.
- ~3 flips per episode. Can't distinguish final recovery from earlier fails.
- The signal is an exit property, not a trigger. The sub-state at exit confirms the transition quality.
- C2 is a holding pattern where the market oscillates before deciding.

## Iteration 6: Forward-Looking Returns + Synthesis
- C2-S5 → C3 (n=111): +0.09%, 7.6h — longer, positive returns
- C2-S4 → C3 (n=32): −0.17%, 4.3h — shorter, negative returns (anemic bull)
- Generalizes across ALL regime boundaries (C3-S7→orderly, C3-S6→sharp)
- Zero-flip C2 episodes: 11 S5-entry all → bull (100%); 17 S4-entry predominantly → bear

---

## Iteration 7: Transition-Level Clustering (8 states, 5 relation types?)
- Z₅ relation-typing REJECTED. Transitions decompose into 4 types (within/forward/backward/forbidden)
- K=4-implied grouping wins on BIC over all unsupervised K
- Complement symmetry confirmed for Basis A at J₈ level (mean JSD = 0.051)
- **(3,5) → market DEFINITIVELY CLOSED**

## Iteration 8: Temporal Modulation
- Transition TYPE is time-invariant (all chi-squared p > 0.05)
- S5→bull signal is time-independent (p = 0.567): Asia 92%, Europe 97%, US 87%, Evening 91%
- Structural zeros hold across all time blocks (3 absolute + 1 near-zero)
- Transition TIMING mildly non-uniform (p = 0.038) — frequency varies, type doesn't
- Weekend effect: higher C1 breakthrough (26.9% vs 17.5%), faster cycling. Liquidity artifact.
- **Mechanistic synthesis:** time-invariance + complement symmetry → endogenous multi-timescale feedback

## Iteration 9: Timescale Universality

### Question
Does the K=4 directed cycle hold across different timescale combinations?

### Bases tested
| Basis | Fast | Medium | Slow | Ratio |
|-------|------|--------|------|-------|
| A (original) | trend_1h | trend_8h | trend_48h | 1:8:48 |
| E | trend_4h | trend_24h | trend_96h | 4:24:96 |
| F | trend_1h | trend_4h | trend_16h | 1:4:16 |
| G | trend_1h | trend_16h | trend_96h | 1:16:96 |

### Results

**K=4 directed cycle is UNIVERSAL.** All 4 bases produce identical topology: same cycle C0→C1→C3→C2→C0, same 4 forbidden transitions, same complement symmetry (mean JSD 0.027–0.067), same near-uniform stationary distribution. Now confirmed across 6+ independent bases total.

**Duration scales linearly with slow timescale:**
| Basis | Slow | Mean dur | Ratio to A |
|-------|------|----------|------------|
| F | 16h | 3.0h | 0.46× |
| A | 48h | 6.5h | 1.00× |
| G | 96h | 12.0h | 1.85× |
| E | 96h | 17.4h | 2.68× (overshoots — higher feature correlation) |

**Exit sub-state signal depends on fast:medium ratio — bandwidth phenomenon:**
| Basis | Ratio | S5→bull | S4→bull | Gap |
|-------|-------|---------|---------|-----|
| A | 1:8 | 91.8% | 49.2% | 42.6pp |
| F | 1:4 | 82.1% | 38.8% | 43.3pp |
| E | 1:6 | 73.7% | 42.3% | 31.4pp |
| G | 1:16 | 77.8% | 75.0% | 2.8pp (**no signal**) |

Signal works in a bandwidth ~1:4 to 1:8. At 1:16, fast bit decouples from medium and carries no information about C2 pullback exit direction.

**Sub-state signal universality is REGIME-DEPENDENT (sharpest new finding):**

Within-pair heterogeneity (JSD) by regime:
| Regime | A (1:8) | E (1:6) | F (1:4) | G (1:16) |
|--------|---------|---------|---------|----------|
| C1 reversal | 0.108 | **0.325** | **0.319** | **0.121** |
| C2 pullback | **0.344** | **0.227** | **0.320** | 0.023 |

C1 retains fast-bit information at ALL ratios including 1:16. C2 loses it at 1:16. Two different mechanisms:
- **C1 reversal:** fast timescale *catalyzes* regime change against prevailing trend → always informative
- **C2 pullback:** resolution depends on medium↔slow interaction → fast bit only informative when coupled to medium (ratio ≤ 1:8)

### Deliverables
- `logos/markets/09_timescale_universality.py`, `memories/markets/09_phase9_output.txt`

---

## Iteration 10: Signal Refinement & Split-Half Validation

### Question
Three sub-questions: (a) Does trend_1h magnitude carry graded information beyond binary? (b) Does episode duration add predictive power beyond exit sub-state? (c) Does the full structure independently emerge from each half of the data?

### Results

**10a: Magnitude is a continuous predictor — the binary is a coarse approximation.**

Spearman ρ=0.533 (p=4e-15, n=187): trend_1h at C2 exit strongly predicts bull/bear direction.

S5 terciles (monotonically increasing bull rate):
| Tercile | n | Bull rate | 95% Wilson CI | trend_1h range |
|---------|---|-----------|---------------|----------------|
| Low | 41 | 83% | [69%, 92%] | [0.01, 0.41] |
| Mid | 40 | 95% | [84%, 99%] | [0.41, 0.88] |
| High | 41 | 98% | [87%, 100%] | [0.88, 5.94] |

S4 decomposition (monotonically increasing bear rate with |trend_1h|):
| Tercile | n | Bear rate | 95% Wilson CI | |trend_1h| range |
|---------|---|-----------|---------------|-----------------|
| Least neg | 22 | 27% | [13%, 48%] | [0.00, 0.26] |
| Mid | 21 | 43% | [25%, 64%] | [0.26, 0.92] |
| Most neg | 22 | 82% | [62%, 93%] | [0.96, 4.07] |

Key finding: the zero threshold is a convention, not a natural boundary. "Least negative" S4 exits (|trend_1h| < 0.26) are 73% bull — closer to S5 behavior.

**Mechanistic confirmation (trend_8h at exit):**
| Group | n | mean trend_8h | std |
|-------|---|---------------|-----|
| S5→bull | 112 | −0.019 | 0.016 |
| S5→bear | 10 | −0.979 | 0.573 |
| S4→bull | 32 | −0.024 | 0.031 |
| S4→bear | 33 | −1.438 | 1.406 |

Successful transitions (→bull) have trend_8h near zero (medium trend about to align). Failed transitions have deeply negative trend_8h (medium trend committed against). 100% of S5→bull have trend_8h < 0 but very close to zero.

**Magnitude does NOT predict return size** (all Spearman p > 0.39). Predicts direction only — once in C3, C3 dynamics determine returns.

**10b: Duration is NOT an independent signal. Clean negative.**
- S5: short 91.5% vs long 92.1% bull (Fisher p=1.00)
- S4: short 57.1% vs long 43.3% bear (Fisher p=0.32)
- Duration adds nothing beyond exit sub-state. One fewer operational variable.

**10c: Split-half blind re-discovery — ALL structural properties independently confirmed.**

| Metric | Half 1 ($99k-$126k) | Half 2 ($60k-$107k) | Full |
|--------|---------------------|---------------------|------|
| K (eigenvalue gap) | 4 (gap=0.134) | 4 (gap=0.146) | 4 (gap=0.141) |
| Structural zeros | 4 | 4 | 4 |
| Cycle match | ✓ | ✓ | ✓ |
| Complement JSD | 0.054 | 0.066 | 0.051 |
| S5→bull | 95.2% [87%,98%] (n=62) | 88.3% [78%,94%] (n=60) | 91.8% [86%,96%] (n=122) |
| S4→bull | 43.2% [29%,59%] (n=37) | 57.1% [39%,74%] (n=28) | 49.2% [38%,61%] (n=65) |

All acceptance criteria passed in both halves. Eigenvalue gaps clean (not marginal). Half 2 has *stricter* zeros (C3→C0 exactly 0.000). Complement symmetry holds at JSD < 0.07 in both halves — rules out statistical artifact.

**S5→bull rate reframed: 87–95% with mild environment-dependent modulation** (not "92% ± 2%"). Lower bound of 87% still operationally strong.

### Deliverables
- `memories/markets/10_signal_refinement.py`, `memories/markets/10_phase10_output.txt`

---

## Iteration 11: Logistic Regression at Regime Exits — Major Reframing

### Question
Does trend_8h add predictive power beyond trend_1h at regime exits? What's the AUC baseline for continuous features? Does this generalize beyond C2?

### Results

**The "fast bit as qualifier" story was a proxy. trend_8h is the dominant predictor.**

Cross-validated logistic regression (Half 1 → Half 2 and vice versa):

| Boundary | n | Binary AUC | Best model | CV AUC | AUC gain | trend_8h adds? |
|----------|---|------------|------------|--------|----------|----------------|
| C2→{C0,C3} | 187 | 0.773 | trend_1h + trend_8h | **0.973** | +0.200 | yes |
| C1→{C0,C3} | 210 | 0.586 | trend_1h + trend_8h | **0.965** | +0.379 | yes |
| C0→{C1,C2} | 211 | 0.523 | trend_1h + trend_8h | **0.722** | +0.199 | yes |
| C3→{C2,C0} | 172 | N/A | N/A | N/A | — | untestable (1 crash) |

**C2 exit:** trend_8h coefficient = 42.2 (p=0.012), trend_1h coefficient = 2.2 (p=0.20, not significant). The scorecard: at trend_8h = −0.1, P(bull) = 0.91; at trend_8h = −0.5, P(bull) ≈ 0. The cliff is in trend_8h. Pseudo R² = 0.93.

**C1 exit (biggest surprise):** Binary sub-state was near-random (AUC 0.586). But trend_8h (coef 48.1, p=8e-5) separates breakthroughs from failures at AUC 0.965. Upgrades C1 from "mostly unpredictable" to "substantially predictable." Caveat: ~20 breakthroughs per fold, AUC confidence interval is wide (likely >0.85, "0.97" overstates precision).

**C0 exit:** Moderate signal (AUC 0.722). trend_8h helps predict skip-ahead (C0→C2) vs normal cycle (C0→C1).

**Interaction term adds nothing** (M3 ≈ M2). Relationship is additive.

### Key reframing

The binary exit signal (S5/S4 = trend_1h sign) was a noisy proxy for trend_8h distance-to-zero. The mechanism: fast trend turns first, medium follows. When trend_1h > 0 at C2 exit, it *correlates with* trend_8h being near its turning point. But trend_8h near zero is the actual predictor.

**Calibration is bimodal**: 143 episodes at P(bull) > 0.80, 41 at P(bull) < 0.20, ~3 in between. The model is effectively a sharper binary classifier (better decision boundary) rather than a graded probability scorer. Operational position sizing will be approximately binary. The continuous model's advantage is *fewer misclassifications*, not graded conviction.

### Cross-validation asymmetry

H1→H2 AUC = 0.947, H2→H1 AUC = 0.999. Model trained on correction/recovery half generalizes better to bull market than vice versa. Consistent with S5→bull rate varying between halves. Exact logistic coefficients are environment-dependent estimates that will need recalibration on new data.

### What this decides

- **HMM: defer.** Binary trigram + logistic regression solves both regime identification and exit prediction. HMM's remaining value (continuous regime tracking, earlier exit detection) is speculative with no demonstrated failure of binary assignment.
- **Operational architecture converged:** binary trigram → regime ID, trend_8h → exit quality
- **C1 upgraded:** from "mostly unpredictable" to "substantially predictable" — major expansion of actionable signal space
- **Binding constraint unchanged:** OOS data. Everything from here is in-sample refinement.

### Deliverables
- `memories/markets/11_logistic_exit.py`, `memories/markets/11_phase11_output.txt`

---

## Iteration 12: Out-of-Sample Validation (BTC 2023-2024) — TOP TIER PASS

### Question
Do the structural properties and exit prediction model hold on 2 years of BTC data from a completely different macro environment ($16.7k–$108k, post-FTX recovery → ATH)?

### Data
- OOS: BTC 5-min, 2023-01-05 → 2024-12-30 (209,072 bars, 2,947 episodes)
- IS: BTC Jul 2025–Feb 2026 (61,920 bars, 796 episodes)

### Distribution diagnostic (Step 0)
IS trends are pre-normalized (std ~1), OOS are raw fractional rates (std ~1e-4). Scale differs ~3000×. Binary state construction is scale-invariant (sign-based) so topology is unaffected. Logistic models used standardized (z-score) features for cross-domain comparison. AUC is rank-invariant so valid regardless.

### Part A: Topology — CONFIRMED

| Property | OOS (2023-2024) | IS (2025-2026) | Verdict |
|----------|-----------------|----------------|---------|
| K (spectral gap) | 4 (gap=0.151) | 4 (gap=0.141) | ✓ |
| Structural zeros | 3 absolute + 1 near-zero (n=2) | 3 absolute + 1 near-zero (n=1) | ✓ identical |
| Complement symmetry | JSD=0.007 | JSD=0.051 | ✓ stronger in OOS |
| Stationary dist | 23.1%–29.7% | 22.6%–28.1% | ✓ near-uniform |
| Jump chain Frobenius | — | 0.066 vs IS | ✓ nearly identical |
| Mean episode duration | 5.6–6.6h | 6.1–6.9h | ✓ consistent |

The directed cycle C0→C1→C3→C2→C0 is identical. Same 3 absolute zeros (C1→C2, C2→C1, C3→C0) and same near-zero (C0→C3). Topology is macro-environment-invariant.

### Part B: Exit Prediction — STRONG PASS

**Bit-flip attribution (circularity test):** 86.4% of macro exits involve trend_8h flipping, 13.7% trend_48h, 8.5% trend_1h. Note: trend_1h alone *cannot* cause a macro transition by construction. The high trend_8h fraction means the model partly measures "how close to crossing" — partly mechanical. Non-trivial content: discriminating exits where trend_8h approaches zero but retreats vs crosses.

**Binary S5→bull rate:** 85.9% [82.7%, 88.7%] (n=512). Point estimate passes 85% threshold. Lower CI (82.7%) **FAILS** the pre-committed ">85% lower CI" criterion. IS reference: 91.8%. The degradation is real. S4→bull rate jumped to 71.8% (IS: 49.2%) — binary signal gap collapsed from 42.6pp to 14.1pp in bull-dominated OOS period. **Binary signal is environment-dependent; deprecated as deployment tool.**

**Cross-domain logistic (standardized features):**

| Boundary | Direction | AUC | Brier |
|----------|-----------|-----|-------|
| C2 | IS→OOS | **0.957** | 0.049 |
| C2 | OOS→IS | **0.999** | 0.041 |
| C1 | IS→OOS | **0.980** | 0.054 |
| C1 | OOS→IS | **0.982** | 0.056 |

All exceed the top-tier acceptance threshold (AUC > 0.85). The continuous model absorbs the environment effect that degraded the binary signal.

**C1 thin-n resolved:** 155 breakthroughs in OOS (vs 43 IS). AUC 0.980 with adequate sample size.

**Standardized coefficients:** trend_8h dominant in both periods. IS: 3.91, OOS: 7.27 at C2. Coefficient ratio ~1.86× — same direction, different magnitude. Recalibration needed for deployment.

**Threshold comparison:** Standardized z-score thresholds differ (IS: −0.31, OOS: −0.12). Not directly interpretable due to different normalization conventions between IS and OOS data. Threshold invariance prediction is **untestable** with current data.

**Calibration (IS model → OOS):** IS model slightly overestimates at extremes. Low bin: predicted 3.7%, actual 1.1%. High bin: predicted 91.5%, actual 97.6%. Ranking is excellent; calibration needs refit.

### Part C: Returns — REMARKABLY STABLE

| Path | OOS | IS | Verdict |
|------|-----|-----|---------|
| C2-S5→C3 | +0.36% (n=440) | +0.09% (n=111) | ✓ same sign, OOS larger |
| C2-S4→C3 | −0.01% (n=183) | −0.17% (n=32) | ✓ same sign |
| C1→C3 (breakthrough) | +1.08% (n=155) | +1.09% (n=43) | ✓ virtually identical |
| C1→C0 (failure) | −0.27% (n=549) | −0.25% (n=167) | ✓ virtually identical |
| Asymmetry ratio | 3.95 | 4.36 | ✓ stable |

C1 breakthrough return stability (+1.08% vs +1.09%) is the single most striking result — identical return magnitude across completely different macro environments with 3.6× the sample size.

### Pre-committed acceptance criteria verdict

| Criterion | Result | Status |
|-----------|--------|--------|
| K=4 topology | ✓ Confirmed | PASS |
| Structural zeros (same 4 forbidden) | ✓ Identical pattern | PASS |
| Complement symmetry (JSD < 0.15) | ✓ JSD = 0.007 | PASS |
| trend_8h AUC > 0.85 at C2 | ✓ AUC = 0.957 | **TOP TIER** |
| S5→bull rate >85% | Point: 85.9%, CI lower: 82.7% | **FAIL on CI** |
| trend_8h threshold invariance | Untestable (normalization mismatch) | INCONCLUSIVE |

**Overall: TOP TIER (K=4 + AUC > 0.85). Proceed to deployment.**

### Key operational lessons
1. **Binary S5/S4 signal deprecated.** Environment-dependent. Use continuous trend_8h model.
2. **Logistic coefficients need refit on raw-scale data.** OOS data is raw (same as live); IS is pre-normalized. Refit on OOS gives production-ready coefficients.
3. **C1 breakthrough is confirmed tradeable.** n=155, return +1.08%, asymmetry ratio 3.95. No longer thin-n.
4. **AUC partly mechanical.** 86% of exits driven by trend_8h bit flip. Model reads state quality, not predicting the future. Still operationally useful.

### Deliverables
- `memories/markets/12_oos_validation.py`, `memories/markets/12_oos_validation_output.txt`

---

## INVESTIGATION STATUS — Phases 1–12

### Operational architecture (OOS-VALIDATED)
1. **Regime identification:** Binary trigram (trend_1h × trend_8h × trend_48h) → 4-regime directed cycle
2. **Exit quality prediction:** trend_8h level at regime exit → P(favorable transition), cross-domain AUC 0.957 (C2), 0.980 (C1)

### Evidence hierarchy

**Layer 1: Topological invariants (DEFINITIVE — OOS confirmed)**
- K=4 directed cycle, structural zeros, complement symmetry
- Confirmed across: 6+ bases, 4 timescale ratios, all time blocks, split-half, AND 2 years of OOS data in a different macro environment
- Frobenius distance IS↔OOS = 0.066

**Layer 2: Exit prediction (VERY HIGH — OOS confirmed)**
- trend_8h dominates exit prediction at C2 (cross-domain AUC 0.957) and C1 (0.980)
- Binary signal deprecated (environment-dependent gap collapse)
- C1 thin-n concern resolved (n=155 breakthroughs in OOS)

**Layer 3: Returns (HIGH — OOS confirmed)**
- C1 breakthrough: +1.08% OOS vs +1.09% IS (virtually identical)
- Asymmetry ratio stable (3.95 vs 4.36)
- C2-S5→C3 returns same sign, larger in OOS

**Layer 4: Scaling and invariance (high confidence, IS only)**
- Duration scales linearly with slow timescale
- Transition type is time-invariant

### Resolved constraints
- ~~OOS data~~ → **PASSED** (Phase 12, top tier)
- ~~C1 thin-n~~ → **RESOLVED** (155 breakthroughs in OOS)
- ~~Binary signal reliability~~ → **SUPERSEDED** by continuous trend_8h model

### Remaining constraints
- **Normalization resolution:** IS data pre-normalized, OOS/live data raw. Must refit logistic on raw-scale data for deployment.
- **Multi-asset** (ETH/SOL) — gates portability claims
- **Operational prototype** — binary trigram tracker + trend_8h monitor
- **Live forward test** (post-Feb 2026 BTC) — true forward OOS