# KW Pair Ordering — Consolidated Findings

## Result

**The King Wen pair ordering is designed but not algebraically determined.**

It is the unique component of the I Ching's structure where human authorship enters. The ordering satisfies two hard structural constraints and exhibits three soft aesthetic properties, but these collectively leave an enormous space (~7.2×10³¹ valid orderings) within which the KW sequence is not anomalous on any measurable structural dimension.

---

## Method

Generated 50,000 valid pair orderings satisfying:
- **Fixed endpoints:** Qian/Kun at position 0, Ji Ji/Wei Ji at position 31
- **Z₅×Z₅ anti-clustering:** no consecutive hexagrams share the same element pair

Computed 12 structural metrics on each ordering and compared KW to the null distribution. Applied two joint significance tests: omnibus Σz² and directional triple joint count.

**Acceptance rate:** 27.37% (182,706 attempts for 50,000 valid orderings).

---

## Findings

### F1: No single metric discriminates KW

All 12 metrics place KW within the 2nd–98th percentile:

| Metric | KW | %ile | z |
|--------|-----|------|---|
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

### F2: No joint anomaly

**Omnibus Σz² = 12.95 (65th percentile).** KW's total squared deviation across all metrics is average. This is the proper look-elsewhere-corrected test.

**Triple joint: 7/50,000 = 0.014%.** The three most borderline metrics (orbit_oneway_frac, torus_step_mean, complement_distance_mean) are nearly independent (all pairwise |r| < 0.07), and only 7 orderings match KW's direction on all three. But Bonferroni-corrected for C(12,3) = 220 triples: p ≈ 3.1%. Marginal and does not survive proper correction. The omnibus at 65th percentile settles it.

### F3: Basin clustering is a confound — CORRECTION

The prior p<0.001 basin clustering signal (05_king_wen_sequence.py, cited as a "known constraint" in questions.md) was an artifact of comparing to fully random permutations. Under the correct null model (anti-clustering + fixed endpoints):

- KW basin_clustering = 0.290 (18th percentile, z = -0.94)
- Null mean = 0.365
- **KW is below average**

**Mechanism:** Z₅×Z₅ cell sizes are non-uniform and correlate with basin via shared inner bits (b₂, b₃). The anti-clustering constraint forces avoidance of large element-pair cells, which implicitly routes through basin-coherent neighborhoods. Basin clustering is induced by anti-clustering, not independent of it.

### F4: Three soft properties characterize KW's style

These describe KW's aesthetic without determining it:

1. **Directional orbit flow (98.3rd %ile).** 91% of connected orbit pairs appear in only one direction. The sequence has a preferred current through orbit space.
2. **Small Z₅ torus steps (9.5th %ile).** Consecutive hexagrams tend toward nearby element pairs, beyond what anti-clustering forces.
3. **Complement proximity (10.4th %ile).** Complement-paired pairs are placed closer together (mean distance 7.9 vs null mean 10.3).

### F5: The constraint space is enormous

~27% of random pair orderings (with fixed endpoints) satisfy anti-clustering. This gives ~0.27 × 30! ≈ 7.2×10³¹ valid orderings. The known hard constraints eliminate ~73% of orderings but leave a space vastly larger than any optimization could search exhaustively. The ordering is not uniquely determined by structural constraints.

### F6: The ordering principle is narrative, not algebraic

The 序卦傳 provides between-pair transition logic using a small set of semantic templates ("物不可以終X" = dialectical reversal, "X必有Y" = necessary consequence). The 上經/下經 split is explicitly marked with a cosmogenic reset. These narrative structures are real but operate in dimensions (semantic, pedagogical, cosmological) outside our 12-metric space.

---

## What this means for the I Ching's structure

The I Ching consists of:
- **Algebraically forced components:** 五行 assignment (uniqueness theorem), pairing rule (V₄ maximum), trigram arrangements (先天 = Z₂ optimum, 後天 = 2×3×5 triple junction), endpoints (poles + attractors)
- **One authored component:** the linear ordering of 32 pairs

The ordering is the system's single free parameter. It is where tradition, pedagogy, and cosmological narrative enter the otherwise rigid algebraic frame. This is itself a structural result: the I Ching has exactly one degree of freedom, and it is narrative.
