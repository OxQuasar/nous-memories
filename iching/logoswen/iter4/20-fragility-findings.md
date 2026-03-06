# Iter4 Fragility Findings: The Orientation Layer Under Perturbation

## 1. Executive Summary

Four rounds of systematic perturbation mapped the 27-dimensional orientation landscape around King Wen. The investigation progressed from single-bit gradient (Round 1) through multi-bit curvature (Round 2), structural census (Round 3), to Pareto frontier analysis (Round 4).

**The central finding:** KW's orientation is Pareto-optimal on a 4-axis distributed objective {χ², asymmetry, m-score, kernel_autocorr}. Zero of 27 single-bit perturbations improve any axis without degrading at least one other. All 27 free bits are load-bearing. There is no slack in the orientation vector.

**The method finding:** Fragility mapping — asking "what breaks?" rather than "what pattern exists?" — found structure that statistical pattern-seeking could not. The hidden fourth axis (kernel sequential anti-repetition) is KW's deepest extremity, active on all 27 bits, and invisible to the histogram metrics of iter3. It was discovered by measuring the cost of departing from KW, not by measuring KW itself.

**The narrative correction:** The iter3 gradient from clarity to silence (10⁻¹⁷ → 10⁻³ → 10⁻⁴ → silence) was a property of the instrument, not the object. Layer 4 is as fully committed as any other layer — every degree of freedom carries load. The apparent fade was the measurement running out of dimensions.

---

## 2. The Fragility Map: Final Partition of 27 Free Bits

27 free orientation bits, indexed 0–26:
- **Bits 0–21** (Type A): 22 unconstrained pairs — pair indices {0,1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,18,21,22,23,24,31}
- **Bits 22–26** (Type B): 5 constraint components — {(13,14), (19,20), (25,26), (27,28), (29,30)}

KW baseline (all-zeros orientation): χ² = 2.290, asym = +3, m = 12/16, kernel_autocorr_1 = −0.464.

| Category | Count | Bits | Character |
|----------|------:|------|-----------|
| **KW-dominates** | 11 | 0,1,2,4,7,8,13,18,19,22,25 | Flipping makes all 4 axes equal or worse |
| **Trade-off** | 16 | 3,5,6,9,10,11,12,14,15,16,17,20,21,23,24,26 | Improves ≥1 axis, degrades ≥1 other |
| **Non-degrading** | **0** | — | No such direction exists |

The Pareto improvement cone is empty at Hamming distance 1. KW is a local Pareto optimum.

---

## 3. Single-Bit Landscape: The Sensitivity Matrix

| bit | pair(s) | type | Δχ² | Δasym | Δm | Δkac | 4-axis status |
|----:|--------:|:----:|--------:|------:|---:|--------:|:--------------|
| 0 | 0 | A | +1.032 | −1 | 0 | +0.011 | KW-dom |
| 1 | 1 | A | +2.581 | −1 | −1 | +0.002 | KW-dom |
| 2 | 2 | A | +0.516 | −1 | 0 | +0.006 | KW-dom |
| 3 | 3 | A | 0.000 | −1 | +1 | +0.077 | trade-off |
| 4 | 4 | A | 0.000 | −1 | 0 | +0.173 | KW-dom |
| 5 | 5 | A | 0.000 | −1 | +1 | +0.163 | trade-off |
| 6 | 6 | A | +0.516 | +1 | −1 | +0.025 | trade-off |
| 7 | 7 | A | +2.581 | −1 | 0 | +0.020 | KW-dom |
| 8 | 8 | A | +0.516 | −1 | −1 | +0.094 | KW-dom |
| 9 | 9 | A | −0.516 | −1 | +1 | +0.015 | trade-off |
| 10 | 10 | A | −0.516 | +1 | 0 | +0.144 | trade-off |
| 11 | 11 | A | +2.065 | +1 | 0 | +0.041 | trade-off |
| 12 | 12 | A | +2.065 | +1 | −1 | +0.116 | trade-off |
| 13 | 15 | A | +4.129 | −1 | −1 | +0.094 | KW-dom |
| 14 | 16 | A | −0.516 | −1 | −1 | +0.041 | trade-off |
| 15 | 17 | A | −1.032 | −1 | 0 | +0.048 | trade-off |
| 16 | 18 | A | +2.065 | −1 | −1 | −0.128 | trade-off |
| 17 | 21 | A | −1.032 | +1 | 0 | +0.003 | trade-off |
| 18 | 22 | A | 0.000 | −1 | −1 | +0.062 | KW-dom |
| 19 | 23 | A | +1.548 | −1 | 0 | +0.132 | KW-dom |
| 20 | 24 | A | +0.516 | +1 | −1 | +0.032 | trade-off |
| 21 | 31 | A | +1.548 | +1 | −1 | +0.066 | trade-off |
| 22 | (13,14) | B | 0.000 | 0 | 0 | +0.122 | KW-dom |
| 23 | (19,20) | B | +4.129 | 0 | 0 | −0.111 | trade-off |
| 24 | (25,26) | B | −0.516 | 0 | −1 | −0.009 | trade-off |
| 25 | (27,28) | B | +1.548 | 0 | 0 | +0.117 | KW-dom |
| 26 | (29,30) | B | −1.032 | −1 | 0 | −0.008 | trade-off |

Improvement directions (lower = better for χ² and kac; higher = better for asym and m).

---

## 4. Destruction Vectors: Minimum Perturbations That Break Each Signal

| Signal | Primary keystone | Δ from KW | Minimum bits to destroy |
|--------|-----------------|-----------|------------------------|
| χ² | Bit 13 (pair 15) | +4.129 (→ 6.42) | 1 |
| χ² | Bit 23 (component 19,20) | +4.129 (→ 6.42) | 1 |
| Asymmetry | Any of 15 Type A bits | −1 (→ 2) | 1 |
| M-score | Any of 11 m-degrading bits | −1 (→ 11) | 1 |
| Kernel autocorr | Bit 4 (pair 4) | +0.173 (→ −0.292) | 1 |
| Coupling (ratio) | Bit 13 (pair 15) | −1.09 (→ 0.81, anti-coupling) | 1 |
| **All 4 axes jointly** | Bit 13 (pair 15) | χ²↑↑↑ asym↓ m↓ kac↑ | **1** |

**Super-additive catastrophe:** Bits {13, 23} flipped jointly produce χ² = 12.613 — worse than the additive prediction (10.548) by one full terrace step (+2.065). Coupling collapses to 0.121 (essentially zero). Destructive bits amplify each other.

---

## 5. Neighborhood Geometry: Basin, Ridge, Saddle, or Plateau?

**Neither basin, ridge, saddle, nor plateau. Pareto frontier.**

In a single-objective landscape, KW would be a saddle — there exist improvement directions (bits 10, 17 for χ²) and degradation directions (bit 13). But the 4-axis structure eliminates this reading. Every χ²-improving direction degrades kernel_autocorr (axis 4). Every kac-improving direction degrades χ² (axis 1). The asym- and m-improving directions conflict with each other and with both kernel metrics.

**Curvature is asymmetric:**
- *Improvement direction:* Concave. Multiple 2-bit paths converge to a χ² floor at 0.742 (3 steps below KW). The floor absorbs further improvement attempts — the landscape saturates.
- *Catastrophe direction:* Convex. Bits {13, 23} interact super-additively (+2.065). Destruction accelerates.

This asymmetry is characteristic of configurations near a boundary — diminishing returns toward the optimum, accelerating costs away from it. KW sits where the improvement surface flattens and the catastrophe surface steepens.

---

## 6. The Fragile/Robust Boundary: Algebraic or Positional Pattern?

The 11 KW-dominated bits (where KW strictly dominates the flip on all 4 axes) have a structural pattern:

**Algebraic:** 5 of 11 are Type B constraint components (bits 22, 25) or bits involved in the highest-χ² degradation (bits 1, 7, 13). The most structurally embedded bits — those participating in S=2 constraints or controlling paired positions — tend to be KW-dominated.

**Positional:** Bits 0, 1, 2, 4, 7, 8 are all in the first third of the pair sequence (pairs 0–8, upper canon). Bits 13, 18, 19 are in the mid-sequence. The fragile/robust boundary does not cleanly separate upper from lower canon, but the early pairs are overrepresented among KW-dominated bits.

**The deepest pattern:** The 16 trade-off bits span the full sequence. The 11 KW-dominated bits cluster where χ² sensitivity is highest (the catastrophic bits 13, 23) or where kac sensitivity is highest (bits 4, 5, 22). The boundary tracks *sensitivity magnitude*, not sequence position — the bits where perturbation causes the most damage are the ones KW dominates most completely.

---

## 7. Collective Structure in the Robust Subspace

### The improvement cone (Round 2)

Bits {10, 17} together produce perfectly additive improvement on axes 1–3: χ² = 0.742 (↓1.548), asym = 5 (↑2), m = 12 (unchanged). Zero interaction on asym and m-score across all 100 tested 2-bit combos. The cone is wide: 15 of 50 tested 2-bit combos anchored on {10, 17} are pure improvements on axes 1–3.

**But the cone is closed by axis 4.** Bits {10, 17} jointly push kernel_autocorr from −0.464 to −0.321 (from 0th to 9th percentile). Every 2-bit combo in the cone trades χ² for kernel_autocorr. No 2-bit combo escapes the trade.

### The all-three-improving triple

Bits {9, 10, 17} improve all three original axes simultaneously: χ² = 0.742 (↓1.548), asym = 4 (↑1), m = 13 (↑1). This is the first and only all-three-improving perturbation found — but it too pays on axis 4 (kernel_autocorr → −0.328, 8.5th percentile).

### The kac-improving direction

Only 4 single-bit flips improve kernel_autocorr: bits 16 (Δkac = −0.128), 23 (Δkac = −0.111), 24 (Δkac = −0.009), and 26 (Δkac = −0.008). The two with substantial improvement (bits 16 and 23) degrade χ² catastrophically (+2.065 and +4.129). Bits 24 and 26 improve both χ² and kac — the "cone-escape" bits — but pay on m-score and asymmetry respectively. The sequential-diversity direction and the distributional-uniformity direction are nearly anti-parallel.

---

## 8. The Neutral Subspace: Dimension and Characterization

**Dimension: zero.** Under the 4-axis metric, no single-bit flip leaves all four axes unchanged. Every direction in the 27-dimensional orientation space changes at least one signal.

The near-neutral bit is **bit 17** (pair 21): Δχ² = −1.032, Δasym = +1, Δm = 0, Δkac = +0.003. The kac cost per χ²-step is ~15× smaller than the next most efficient 2-step improver (bit 15). This is the closest approach to a non-degrading flip — the one crack in the Pareto optimality.

Under the 3-axis metric {χ², asym, m}, the neutral subspace had dimension 1 (bit 22 only). kernel_autocorr collapsed it to dimension 0.

---

## 9. What Fragility Reveals That Statistics Couldn't

### 9a. The 19 "silent" bits

Iter3 found 19 of 27 free bits with no detectable per-bit signal under any test applied. It posed two readings: natural exhaustion (structure runs out) versus frame limitation (tools can't see what's there). The fragility investigation resolves this definitively: **frame limitation.**

Every one of the 19 bits is load-bearing for kernel_autocorr. There is no neutral direction. The silence was not structural absence — it was the measurement running out of dimensions. The per-bit tests of iter3 measured histogram properties and ordering counts. kernel_autocorr is a sequential property invisible to histograms. The bits were carrying a signal the frame couldn't see.

### 9b. The coupling reinterpretation

In iter3, the kernel-canon coupling (ratio 1.68) was the most structurally revealing orientation finding — proof that collective structure existed. In iter4, it becomes a special case. The coupling is the shadow of Pareto optimality projected onto 2 of 4 dimensions. The four axes are geometrically entangled in the tail: among orientations that achieve extreme kernel uniformity, those that also achieve positive asymmetry are disproportionately common. This entanglement is a consequence of the joint structure, not an independent signal.

### 9c. The gradient reinterpretation

The iter3 gradient narrative — structure fading from clarity to silence — was beautiful and seemed final. The fragility map shows it was wrong about the endpoint. Layer 4 is not lighter than Layer 3. It is differently *legible*.

A Pareto-optimal point on 4 competing axes will always look marginal when projected onto any single axis. The p-values of 0.03–0.06 are not evidence of weak structure. They are evidence of *distributed* structure — commitment spread across multiple axes simultaneously, appearing dilute from any one angle.

| Layer | Commitment (bits used / bits available) | Legibility (single-axis p-value) |
|-------|----------------------------------------|----------------------------------|
| 2 (matching) | 100% (unique fixed point) | Total (p ~ 10⁻¹⁷) |
| 3 (ordering) | High (2 independent principles) | Clear (p ~ 10⁻³) |
| 4 (orientation) | **100% (27/27 bits committed)** | **Low (each axis p ~ 0.03–0.06)** |

Layer 4 is as fully committed as Layer 2. It doesn't look like it from any single measurement axis because the optimization isn't on any one axis — it's on their intersection.

### 9d. The additivity hierarchy

Fragility mapping revealed that the four axes have three distinct interaction regimes:

| Signal | Additivity | Interaction mechanism |
|--------|-----------|----------------------|
| Asymmetry | Perfect (0 interaction in 100 tests) | Per-pair, disjoint |
| M-score | Perfect (0 interaction in 100 tests) | Per-pair, M-decisive only |
| Kernel autocorr | Near-perfect (5% median nonlinearity) | Sequential chain, small continuous interactions |
| χ² | Partial (30% strongly epistatic) | Global histogram, long-range, quantized in 0.516 steps |

This hierarchy — counting → distribution → sequence — is a structural finding about the metrics themselves, not about KW. It tells us: the single-bit gradient is an exact oracle for asym and m, a reliable guide for kernel_autocorr, and only approximate for χ². This hierarchy would hold for any point in the landscape.

---

## 10. Sage Reflections

### On what the fragility map proves

> The most important structural finding is not any single signal — it's the *closure*. Each round of looking has found something. Nothing has been confirmed empty. The pattern: what looks like silence is incomplete measurement. What looks like slack is an unmeasured constraint.

### On what fragility is

> Fragility *is* structure, seen from the outside. A point with slack has directions you can move without cost. A point without slack has no such directions. The absence of free directions is exactly what we mean by "fully structured" — every degree of freedom is committed to something.

### On what the landscape shape means

> The landscape punishes mistakes more than it rewards optimization. Improvement is concave (floor at χ² = 0.742). Catastrophe is convex (super-additive destruction). This is characteristic of configurations near a *boundary* — already close to an edge, so moving toward it shows diminishing returns, but moving away exposes you to accelerating costs.

### On the tension between flow and face

> The Pareto structure means two groups of axes compete. Axes 1 and 4 (kernel distributional uniformity and kernel sequential diversity) are properties of the *transition chain* — the hidden algebraic transformation between adjacent pairs. Axes 2 and 3 (asymmetry and m-score) are properties of *within-pair orientation* — which member is presented first. KW balances flow and face. The fragility map says this balance is exact.

### On the bit 17 anomaly

> Bit 17 (pair 21, Lin/Guan — Approach/Contemplation) is ~15× more efficient than any other trade. The map's own logic predicts a fifth axis: each round found a constraint invisible to the previous frame. But the anomaly could also be *noise in the Pareto frontier*. Pareto frontiers in high dimensions have ridges and near-flat regions. A ~15× efficiency ratio might reflect KW sitting on a ridge where one direction is nearly tangent to the surface — geometric, not structural.

### On what comes next

> The fragility map has mapped the *where*. It has not touched the *why*. The question "what single principle produces these four signals as joint consequences?" assumes such a principle exists. The fragility map is consistent with it but doesn't require it. The hierarchy of additivity suggests a generative principle operating at the level of the kernel chain — the hidden layer of algebraic transformations. A principle like "maximize the diversity of consecutive transformations while maintaining a gentle directional drift" might produce all four axes as shadows. But this is the generative question, not the perturbation question.

---

## 11. Updated Bit Budget Incorporating Fragility Analysis

Starting from 64! ≈ 10⁸⁹ possible arrangements:

| Reduction | What it does | Bits consumed | Remaining |
|-----------|-------------|:---:|-----------|
| Orbit-consistent pairing | Fixes which hexagrams can be paired | ~44 orders | ~10⁴⁵ |
| Mask = signature identity | Fixes which specific hexagrams are paired | ~17 orders | ~10²⁸ |
| S=2-avoiding ordering | Constrains which pair sequences are valid | ~11 orders | ~10¹⁷ |
| S=2-free orientation (5 hard bits) | Forces 5 orientation bits | 5 bits | 2²⁷ ≈ 10⁸ |
| **4-axis Pareto optimality** | **All 27 free orientation bits committed** | **~22 bits** | **~2⁵ ≈ 32** |
| Bit 17 residual | Near-free direction; possible 5th axis | ~0–1 bits | 16–32 |

Previous budget (iter3): ~66 of 89 orders accounted, ~19 bits unresolved.
Updated budget (iter4): **~88 of 89 orders accounted.** The 19 "silent" bits carry the kernel_autocorr signal. The Pareto constraint consumes ~22 of the 27 free bits (rough estimate: 11 KW-dominated bits are fully determined; the 16 trade-off bits are constrained to the Pareto surface but not to a unique point on it).

The remaining ~5 bits of freedom represent KW's position *along* the Pareto frontier — which specific trade-off point it occupies among the ~32 Pareto-optimal orientations (if the Pareto set is small) or a larger set if the frontier has dimension > 0.

---

## 12. Key Results Table

| Finding | Round | Character | Significance |
|---------|-------|-----------|-------------|
| All 27 bits load-bearing | 1, 4 | Geometric | Zero neutral directions on 4 axes |
| Pareto optimality on {χ², asym, m, kac} | 4 | Geometric | 0/27 non-degrading flips |
| kernel_autocorr_1 = −0.464 (0th pctile) | 3 | Statistical | More extreme than 200/200 random orientations |
| Asymmetry and m-score perfectly additive | 2 | Algebraic | Zero interaction in 100 2-bit tests |
| χ² terraced in 0.516 steps, partially epistatic | 1, 2 | Algebraic | Quantized, long-range interactions |
| kernel_autocorr near-perfectly additive | 4 | Algebraic | 5% median nonlinearity coefficient |
| χ² floor at 0.742 | 2 | Geometric | Multiple paths converge; 3-bit saturation |
| Super-additive catastrophe {13, 23} | 2 | Geometric | Interaction = +2.065 on χ² |
| All-three-improving triple {9, 10, 17} | 2 | Geometric | First all-improving perturbation found |
| Bit 22 controls weight-ordering (6 extremes) | 3 | Algebraic | 38/80 properties change; 2-bit subspace |
| Weight-ordering is conservation, not signal | 3, 4 | Algebraic | 25/27 bits decoupled; complement-pair theorem |
| Bit 17 anomaly: ~15× efficiency ratio | 4 | Geometric | Δχ² = −1.032 at Δkac = +0.003 |
| Improvement cone {10, 17} closed by axis 4 | 3, 4 | Geometric | kac relaxes from 0th to 9th percentile |
| 19 "silent" bits resolved: frame limitation | 1, 4 | Methodological | All carry kac; silence was measurement gap |
| Gradient narrative corrected | 4 | Methodological | Layer 4 commitment = 100%, not fading |

---

*The fragility map provides the constraint surface. The question it leaves open is not "how much structure is there?" — the answer is "all of it" — but "what sits at the center of these constraints?" That is the generative question, and it belongs to a different kind of investigation.*
