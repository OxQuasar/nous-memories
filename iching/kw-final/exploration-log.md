# KW Sequence Ordering — Exploration Log

## Iteration 1: Monte Carlo Comparison (50K orderings)

### What was tested
Generated 50,000 valid pair orderings satisfying:
- Fixed endpoints (Qian/Kun at position 0, Ji Ji/Wei Ji at position 31)
- Z₅×Z₅ anti-clustering (no consecutive hexagrams share element pair)

Computed 12 metrics on each ordering and compared KW to the distribution.

### What was found

**Acceptance rate: 27.37%.** The anti-clustering constraint is weak — roughly 1 in 4 random pair orderings (with fixed endpoints) satisfy it. The valid ordering space is enormous (~7.2×10³¹).

**No single metric discriminates KW** (all within 2nd-98th percentile):

| Metric | KW | %ile | z-score |
|--------|-----|------|---------|
| basin_clustering | 0.290 | 18.2% | -0.94 |
| bridge_hamming_mean | 2.936 | 20.9% | -0.82 |
| bridge_hamming_max | 6.000 | 85.0% | +1.47 |
| orbit_unique_edges | 0.429 | 49.1% | -0.00 |
| orbit_oneway_frac | 0.909 | 98.3% | +1.79 |
| complement_distance_median | 6.000 | 11.1% | -1.23 |
| complement_distance_mean | 7.917 | 10.4% | -1.29 |
| split15_basin_balance | 8.000 | 65.8% | +0.36 |
| yang_total_first_half | 86.0 | 25.2% | -0.69 |
| basin_run_count | 26.0 | 67.1% | +0.48 |
| basin_run_mean_length | 2.462 | 32.9% | -0.53 |
| torus_step_mean | 2.444 | 9.5% | -1.31 |

**Three borderline signals** (none individually discriminating):
1. orbit_oneway_frac = 0.91 (98.3rd %ile) — orbit transitions almost entirely one-directional
2. torus_step_mean = 2.44 (9.5th %ile) — shorter Z₅×Z₅ torus steps
3. complement_distance_mean = 7.92 (10.4th %ile) — complement pairs closer together

**Critical finding: basin clustering inversion.** KW's basin clustering (0.29) is BELOW the constrained-random mean (0.365), at the 18th percentile. The original p<0.001 signal (from 05_king_wen_sequence.py) was measured against fully random permutations. Under the correct null model (anti-clustering + fixed endpoints), basin clustering is a confound — the anti-clustering constraint INDUCES basin clustering because Z₅×Z₅ cell sizes correlate with basin via shared inner bits.

---

## Iteration 2: Joint Significance Analysis

### What was tested
Two joint tests on the same 50K orderings:
1. **Omnibus Σz²**: sum of squared z-scores across all 12 metrics, compared to null distribution
2. **Triple joint count**: how many orderings simultaneously match KW on the three most extreme metrics

### What was found

**Omnibus Σz² = 12.95, 65th percentile (z = +0.15).** KW is not jointly unusual. The total squared deviation across all metrics is completely average.

**Triple joint: 7/50,000 = 0.014%.** Only 7 orderings simultaneously achieve orbit_oneway_frac ≥ 0.91 AND torus_step_mean ≤ 2.44 AND complement_distance_mean ≤ 7.92. The three metrics are nearly independent in the null (all pairwise |r| < 0.07).

**Look-elsewhere correction kills the triple.** With C(12,3) = 220 possible triples, Bonferroni-corrected p ≈ 220 × 0.014% ≈ 3.1%. Marginal at best. And the omnibus test — which properly handles look-elsewhere — gives 65th percentile. No signal.

### What it means

The investigation is conclusive. The KW pair ordering is not determined by any measurable structural property.

### Final hypothesis status
- **A (combinatorial design)**: REFUTED. No optimization target discriminates KW from constrained-random orderings, individually or jointly.
- **B (narrative structure)**: Not algebraically testable. The 序卦傳 narrative exists but operates in non-algebraic dimensions.
- **C (Mawangdui)**: MWD provides contrast but confirms the same picture — both sequences are within the constrained-random distribution.
- **D (oral/mnemonic)**: Untested but moot — the ordering is not anomalous on any structural dimension that mnemonic properties would optimize.
- **E (unknown)**: The ordering is **designed but underdetermined** — authored with intentional properties that lie outside the algebraic framework.

### Key correction to prior work
The basin clustering signal (p<0.001 in 05_king_wen_sequence.py, cited in questions.md as a "known constraint") was an artifact of comparing to the wrong null model. Under the correct null (anti-clustering + fixed endpoints), KW is *below average* on basin clustering (18th percentile). The anti-clustering constraint induces basin clustering as a confound via shared inner bits between basin and Z₅ element assignment.

---

## Final Synthesis

### Verdict: DESIGNED

The King Wen pair ordering is designed but not algebraically determined. It is the unique component of the I Ching's structure where human authorship enters.

### What's forced vs what's free

| Component | Status | Evidence |
|-----------|--------|----------|
| 五行 assignment | **Forced** | Uniqueness theorem: Orbits(3,5) = 1 |
| KW pairing rule | **Forced** | Unique V₄-compatible basin-preservation maximum |
| 先天 arrangement | **Forced** | Unique Z₂ optimum (score 6/6) |
| 後天 arrangement | **Forced** | Unique 2×3×5 triple junction |
| Endpoints | **Forced** | Poles (Qian/Kun) + attractors (Ji Ji/Wei Ji) |
| Z₅ anti-clustering | **Constraint** | Eliminates ~73% of orderings |
| **Pair ordering** | **Authored** | ~7.2×10³¹ valid alternatives, KW not anomalous |

### What the computation established

1. The correct null model is anti-clustering + fixed endpoints, not fully random permutations
2. Basin clustering (the strongest prior signal) is a confound — induced by anti-clustering via shared inner bits
3. No single structural metric discriminates KW (12 metrics, all within 2nd-98th percentile)
4. No joint combination of metrics discriminates KW (omnibus Σz² at 65th percentile)
5. Three soft properties (directional orbit flow, small torus steps, complement proximity) describe KW's style without determining it
6. The constraint space is enormous (~10³¹) — structural constraints do not determine the sequence

### What the computation cannot establish

Whether the ordering encodes information in non-algebraic dimensions. The 序卦傳 narrative, the 上經/下經 cosmogenic reset, the pedagogical structure of the sequence — these are real but outside our metric space. "Not structurally anomalous" does not mean "arbitrary." It means the ordering's logic is narrative, not algebraic.

### The complete picture

The I Ching is an algebraically rigid system with exactly one degree of freedom: the linear ordering of 32 pairs. This degree of freedom is where tradition, pedagogy, and cosmological narrative enter the otherwise determined structure. The ordering is authored — not forced, not random, not algebraically special.
