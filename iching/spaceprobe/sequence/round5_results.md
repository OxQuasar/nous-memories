# Round 5: Two Targeted Tests — Results

## Summary: f1 and H-residence are uncorrelated (independent signals), the Upper Canon is extreme on BOTH, the Lower Canon is structurally unremarkable, and trigram-reverse proximity is the strongest new signal.

### 1. Joint constraint tightness

**f1 and H-residence are uncorrelated**: r = -0.001. This is the cleanest possible result — they carry completely independent information. The joint constraint is almost exactly the product of the marginals (ratio 1.06).

| Constraint set | Trials satisfying (of 1M) | Fraction |
|---------------|--------------------------|----------|
| f1 ≥ 1.70 | 115,358 | 11.54% |
| H-res ≥ 20/31 | 70,951 | 7.10% |
| f1 ∧ H-res | 8,642 | **0.86%** |
| + Rep≤2 | 5,067 | 0.51% |
| + Types=8 | 4,646 | 0.46% |
| + OMI≥8 | 830 | **0.083%** |

The 5-constraint survival rate (0.083%) means about 1 in 1,200 random orderings satisfies all known constraints at KW's levels. Adding H-residence to the mix tightens things by ~10× compared to the 4-constraint set from Round 3 (0.85%).

### Upper Canon is doubly extreme

| Metric | KW Upper | Null mean ± std | Percentile |
|--------|----------|-----------------|------------|
| f1 | 2.154 | 1.494 ± 0.241 | **99.84%** |
| H-residence | 11/14 (0.786) | 7.0 ± 1.9 | **99.42%** |

The Upper Canon is simultaneously at the 99.8th percentile for f1 and the 99.4th percentile for H-residence. Both metrics are independent (r ≈ 0), so the Upper Canon being extreme on both is the product — roughly 1 in 10,000 for the upper canon alone.

### Lower Canon is structurally generic

| Metric | KW Lower | Null mean ± std | Percentile |
|--------|----------|-----------------|------------|
| f1 | 1.467 | 1.494 ± 0.224 | **51.2%** |
| H-residence | 8/16 (0.500) | 8.0 ± 2.0 | **60.2%** |

Both perfectly unremarkable. The Lower Canon is indistinguishable from random on kernel-level metrics.

### 2. What does the Lower Canon optimize?

**Answer: nothing measurable at the hexagram level either.**

| Metric | Upper Canon KW | Upper pctile | Lower Canon KW | Lower pctile |
|--------|---------------|-------------|---------------|-------------|
| Trigram continuity | 0.357 | **92.7%** | 0.250 | 71.6% |
| Weight smoothness (|Δw|) | 2.286 | **99.9% (HIGH)** | 1.375 | 52.8% |
| Raw Hamming distance | 2.857 | 32.3% | 3.000 | 49.2% |

The **Upper Canon has anti-smooth weight transitions** — |Δweight| = 2.29 is at the 99.9th percentile (large weight jumps). This aligns with high f1 — the upper canon is maximally disruptive at every level.

The **Lower Canon is dead center** on all metrics. Weight smoothness, trigram continuity, raw Hamming distance — all within 1σ of random. Whatever the Lower Canon encodes, it's not detectable by any of these hex-level metrics.

The Upper Canon has slightly elevated trigram continuity (92.7th percentile) — consecutive bridges more often preserve a trigram. This seems paradoxical with the high f1 (kernel opposition) but makes sense: you can change the kernel maximally while keeping one trigram fixed if the other trigram does all the changing.

**Trigram distribution**: The two canons have different trigram compositions. Upper Canon over-represents Heaven, Earth, Mountain (6 each); Lower Canon over-represents Thunder, Lake, Wind, Fire. Lower trigram entropy is slightly higher (2.84 vs 2.80), but neither is extreme.

### 3. Trigram-level bridge transitions

| Pattern | All 31 | Upper 14 | Lower 16 |
|---------|--------|----------|----------|
| Neither changes | 0 | 0 | 0 |
| Lower trigram only | 4 | 3 | 1 |
| Upper trigram only | 5 | 2 | 3 |
| Both change | 22 | 9 | 12 |

**Zero bridges preserve both trigrams.** Every bridge changes at least one trigram. This is somewhat unusual for the Lower Canon (25th percentile for "both change" count — i.e., KW has fewer "both change" bridges than typical), but not extreme.

Key pattern in single-trigram bridges: when only the lower trigram changes, the kernel is **always id** (3 of 4 cases in upper canon, 1 in lower). When only the upper trigram changes, the kernel is more varied (OMI, OM, M, O). This makes sense: a lower-trigram-only change means bits 1-3 change but bits 4-6 don't, which projects to specific kernel positions.

### 4. Trigram-reverse proximity — a strong new signal

**6 of 28 trigram-reverse pairs are adjacent** in the KW sequence (distance 1). This is at the **100th percentile** — null mean is 0.87 ± 0.93. No random ordering in 100,000 trials matched 6 adjacent trigram-reverse pairs.

| Window k | KW pairs within k | Null mean | Percentile |
|----------|-------------------|-----------|------------|
| 1 | **6** | 0.87 | **100.0%** |
| 2 | 6 | 1.73 | **99.9%** |
| 4 | 6 | 3.42 | 95.2% |
| 8 | 9 | 6.62 | 89.8% |
| 16 | 16 | 12.33 | 94.7% |

The adjacent trigram-reverse pairs are:
- Hex 5 (Xu) ↔ 6 (Song): Water/Heaven ↔ Heaven/Water
- Hex 7 (Shi) ↔ 8 (Bi): Water/Earth ↔ Earth/Water
- Hex 11 (Tai) ↔ 12 (Pi): Heaven/Earth ↔ Earth/Heaven
- Hex 13 (Tong Ren) ↔ 14 (Da You): Fire/Heaven ↔ Heaven/Fire
- Hex 35 (Jin) ↔ 36 (Ming Yi): Earth/Fire ↔ Fire/Earth
- Hex 63 (Ji Ji) ↔ 64 (Wei Ji): Fire/Water ↔ Water/Fire

These are all hexagram **pairs within the same KW pair** — they're consecutive because KW pairs them together. This isn't about the sequence ordering; it's about the **pairing rule**: KW pairs trigram-reverses when the two hexagrams aren't related by bit-reversal (which would make the trigram reversal redundant with hexagram reversal).

Actually, 5 of these 6 are in the Upper Canon (hex 5-14, 35-36), and the last is the terminal pair (63-64). The remaining 22 trigram-reverse pairs are more distant.

At window k=16, KW still has 16/28 pairs within range (94.7th percentile), showing trigram-reverse pairing extends beyond just the immediate pairs.

## Key conclusions

1. **f1 and H-residence are genuinely independent** (r = -0.001). The 5-constraint survival rate is 0.083% — about 1 in 1,200.

2. **The Upper Canon is extreme on both axes** (99.8% f1, 99.4% H-res) — roughly 1 in 10,000 on the joint metric.

3. **The Lower Canon optimizes nothing measurable.** It's structurally generic at both the kernel and hexagram levels.

4. **Trigram-reverse adjacency is the strongest non-kernel signal** (100th percentile). It's primarily a pairing-rule property, not a sequencing property — KW pairs trigram-reverses together.

5. **The two-canon asymmetry is not a dual optimization.** The Upper Canon carries all the kernel-level structure; the Lower Canon doesn't compensate with a different kind of structure. It's simply less constrained.
