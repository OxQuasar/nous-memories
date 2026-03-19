# Empirical Investigation — Plan

## The Core Test

Apply the 五行 grammar to real transition data and check whether it predicts anything. The grammar: three transition types (continuation/generation/destruction), a forbidden bigram (no consecutive destruction), and a one-way valve (destruction → generation blocked). If these constraints hold in data the grammar wasn't fitted to, it's capturing real structure.

## The Mapping Problem

The grammar requires:
1. A system with discrete states (or discretizable continuous states)
2. A cyclic classification of states into ≥5 types
3. A rule assigning transitions to {continuation, generation, destruction} based on the type-distance between source and target states

The classification must be defined *before* looking at transition data. If we choose the classification after seeing the data, we're fitting, not predicting.

**Two strategies:**

**Strategy A (strong):** Use a domain where a natural 5-category classification already exists independently of the I Ching. Apply the grammar mechanically and test.

**Strategy B (weak but broader):** Use multiple candidate classifications per domain. Test each. Report which (if any) produce significant constraint structure. Correct for multiple comparisons.

Strategy A is the real test. Strategy B is exploratory.

---

## Probe 1: Ecological Succession (E1, E2, E3)

**Why first:** Ecology has a natural state classification, high transition counts, and publicly available data.

**States:** Ecosystem regimes (e.g. clear lake / turbid lake, forest / grassland / shrubland, coral-dominated / algae-dominated reef).

**Five-type classification (Strategy A):** Use standard ecological functional types. One natural mapping:
- 水 Water → aquatic/wetland regimes
- 木 Wood → forest/growth regimes  
- 火 Fire → disturbance/high-energy regimes
- 土 Earth → stable/climax regimes
- 金 Metal → degraded/mineral-dominated regimes

**Data source:** Regime Shifts Database (RSDB, Stockholm Resilience Centre). Contains ~30 regime shift types with documented transitions, drivers, and feedbacks.

**Steps:**
1. Extract all documented regime transitions from RSDB
2. Classify source and target regimes into 5 types using the ecological mapping
3. Compute transition type for each (比和/生/克) based on cycle distance
4. Count bigram frequencies across sequential transitions within the same system
5. Test E2: is 克-克 suppressed vs null? (permutation test, 10K shuffles)
6. Test E3: is 克→生 suppressed vs null?
7. Test E1: do 克 transitions have different duration/reversibility than 生 transitions?

**Null model:** Shuffle transition type labels within each system, preserving marginal frequencies and system identity.

**Sample size needed:** ≥100 transitions for bigram statistics to have power. RSDB may be too small; supplement with ERSE (Ecological Regime Shift Evidence) database if needed.

## Probe 2: Political Regime Transitions (E1, E2, E3, E4)

**Why second:** Long time series, well-classified, thousands of transitions.

**States:** Political regime types from Polity IV / V-Dem.

**Five-type classification (Strategy A):** Use standard regime categories:
- Full autocracy → 金
- Partial autocracy → 水
- Anocracy (mixed) → 土
- Partial democracy → 木
- Full democracy → 火

This mapping is debatable — that's the point. Run with it, then test robustness under all 120 permutations of the 5-type assignment. If the constraint holds for only one or two permutations, it's specific. If it holds for many, it's generic to the cycle structure.

**Data source:** Polity V (Center for Systemic Peace). ~170 countries, 1800–present. Annual regime scores.

**Steps:**
1. Discretize Polity scores into 5 categories
2. Extract all year-to-year transitions where the category changes
3. Classify each transition as 比和/生/克
4. Compute bigram frequencies across all countries
5. Test E2, E3 as in Probe 1
6. Test E4: compare results across regions (E4 asks whether the grammar is system-independent)

**Null model:** Shuffle transitions within each country's time series. Also: compare to a Markov chain fitted to the marginal transition matrix.

**Robustness:** Run all 120 permutations of the 5-type assignment. Report the distribution of E2/E3 p-values across permutations.

## Probe 3: Market Regime Transitions (E1, E2, E6)

**Why third:** High-frequency data, good for testing E6 (single-step vs multi-step).

**States:** Market regimes classified by hidden Markov model or volatility clustering.

**Five-type classification (Strategy B):** No natural 5-category classification exists in finance. Use HMM with 5 states fitted to volatility/return data. The states emerge from data, then test whether the grammar's constraints apply to transitions between them.

**Data source:** S&P 500 daily returns, 1950–present. ~18K trading days.

**Steps:**
1. Fit 5-state HMM to daily returns (or use existing regime classification from literature)
2. Extract regime transition sequence
3. For each of the 120 possible cycle orderings of the 5 HMM states, compute 五行 transition types
4. For each ordering, test E2 and E3
5. Test E6: compute mutual information between transition type at step t and step t+k for k=1,2,3,4,5. Check for decorrelation at k≈2 (matching R288)

**Null model:** Shuffle regime labels. Also: compare to baseline HMM transition probabilities.

**This probe is Strategy B** — the classification is not given a priori. Correction for 120 comparisons is mandatory.

## Probe 4: Cross-Domain Comparison (E4)

**After Probes 1–3:** Compare results across ecology, politics, and markets.

**Questions:**
- Do the same constraints (克-克 suppression, valve) appear across domains?
- If so, at similar effect sizes?
- Does the "best" cycle ordering vary by domain, or is one ordering consistently best?

If one cycle ordering works across all three domains, that's strong evidence for a universal grammar. If different domains need different orderings, the grammar is domain-specific and the universality claim fails.

## Probe 5: Coarse-Graining Test (E5)

**Requires:** A system observable at multiple resolutions. Markets are the best candidate (tick/minute/hour/day/week).

**Steps:**
1. Classify transitions at the finest resolution (tick or minute)
2. Coarse-grain to the next resolution (hour or day)
3. Classify transitions at the coarse resolution
4. Compare: does the grammar's classification agree across scales?

If the grammar is scale-invariant, transition types at the fine scale should aggregate consistently to the same types at the coarse scale. If not, the grammar is resolution-dependent.

---

## Priority Order

1. **Probe 2 (political)** — largest dataset, cleanest state boundaries, most transitions, best for statistical power. Start here.
2. **Probe 1 (ecological)** — most natural 5-type mapping, but smaller sample size
3. **Probe 3 (market)** — highest frequency for E6, but Strategy B (no natural mapping)
4. **Probe 4 (cross-domain)** — depends on Probes 1–3
5. **Probe 5 (coarse-graining)** — requires multi-resolution data, most technically demanding

## What Would Change Our Understanding

- **E2 positive across domains:** The GMS constraint is a real feature of multi-regime transitions. The grammar captures something about how destructive change works.
- **E2 negative everywhere:** The forbidden-pattern constraint is specific to the algebraic structure, not to nature. The I Ching's grammar is self-consistent but not empirically descriptive.
- **E3 positive (valve holds):** Destruction genuinely requires a cooling-off period before generation. This would be the most surprising and practically significant finding.
- **E4 positive (cross-domain):** The grammar is universal — domain-independent structure of transitions. This would validate the traditional claim at the level of transition grammar (not content).
- **E6 matches R288:** Single-step prediction outperforms multi-step, confirming the system is designed for immediate assessment, not trajectory forecasting.
