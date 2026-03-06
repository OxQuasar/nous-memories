# Fragility Map — Final (Iter4, Rounds 1–4)

## Conclusion

**KW's orientation is Pareto-optimal on the 4-axis distributed objective {χ², asymmetry, m-score, kernel_autocorr}.** Zero of 27 single-bit perturbations improve any axis without degrading at least one other. All 27 free bits are load-bearing. There is no slack in the orientation vector.

Weight-ordering balance is a conservation consequence of complement-pair algebra, not an independent optimization target. The effective optimization landscape is 4-dimensional.

---

## The Four Axes

| Axis | Signal | KW | Extremity | Active bits | Additivity |
|------|--------|---:|-----------|--------:|------------|
| 1 | Kernel χ² (distributional uniformity) | 2.290 | p ≈ 0.06 | 22 | Partial (quantized, epistatic) |
| 2 | Canon asymmetry (upper-first ordering) | +3 | p ≈ 0.05 | 22 | Perfect (zero interaction) |
| 3 | M-score (L2=yin preference) | 12/16 | p ≈ 0.03 | 14 | Perfect (zero interaction) |
| 4 | **Kernel autocorrelation** | **−0.464** | **0th pctile** | **27** | Near-perfect (5% median error) |

Inverse relationship between structural reach and legibility: the most constraining signal (kernel_autocorr, all 27 bits) was the last discovered and the hardest to detect.

---

## The Pareto Proof

### Single-bit classification on all 4 axes

| Category | Count | Bits |
|----------|------:|------|
| **KW-dominates** | 11 | 0, 1, 2, 4, 7, 8, 13, 18, 19, 22, 25 |
| **Trade-off** | 16 | 3, 5, 6, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 23, 24, 26 |
| **Non-degrading** | **0** | — |

**Zero non-degrading flips.** The Pareto improvement cone is empty at Hamming distance 1.

### How each apparent escape is closed

| Direction | Apparent improvement | Closed by |
|-----------|---------------------|-----------|
| Bits 10, 17 | χ²↓ asym↑ (iter3 "pure improvement") | kac↑ (axis 4) |
| Bits 24, 26 | χ²↓ kac↓ (2D cone-escape on {χ², kac}) | m↓ or asym↓ (axes 2, 3) |
| Bits 16, 23 | kac↓ (strongest kac-improving directions) | χ²↑↑ (axis 1) |
| Bit 9 | χ²↓ m↑ | asym↓, kac↑ (axes 2, 4) |

Every low-dimensional escape is closed by the remaining axes. This is the geometric fingerprint of a point on a high-dimensional Pareto frontier.

### Multi-bit confirmation

All 16 tested 2-bit improvement combos from Round 2 are trade-offs on {χ², kac}. The single-bit cone-escape property (bits 24, 26) does not survive pairing with improvement bits. The landscape is convex toward KW.

---

## The Landscape

### Curvature

- *Improvement:* Concave. χ² floor at 0.742 (3 steps below KW). Multiple 2-bit paths converge there. 3-bit combinations saturate.
- *Catastrophe:* Convex. Bits {13, 23} interact by +2.065 (super-additive). Coupling collapses to 0.121. Destruction accelerates.

### Additivity hierarchy

| Signal | Additivity | Mechanism |
|--------|-----------|-----------|
| Asymmetry | Perfect | Per-pair, disjoint |
| M-score | Perfect | Per-pair, M-decisive only |
| Kernel autocorr | Near-perfect | Sequential chain, small continuous interactions |
| χ² | Partial | Global histogram, long-range, quantized in 0.516 |

Hierarchy: counting → distribution → sequence. Each level inherits more structure from the generative mechanism.

### Key structural features

- **Primary keystone:** Bit 13 (pair 15) — worst χ² (+4.13), worst coupling (→0.81), degrades 3/4 axes
- **Silent destroyers:** Bits 4, 22, 25 — degrade kac while leaving χ² unchanged; invisible to histogram metrics
- **Most efficient trade:** Bit 17 (pair 21) — Δχ² = −1.032 at Δkac = +0.003; ~15× more efficient than any other
- **Steepest trade:** Bit 16 (pair 18) — Δkac = −0.128 at Δχ² = +2.065; maximum kac gain at maximum χ² cost
- **Weight-ordering:** 2-bit subspace (bits 0, 22). Conservation law, not optimization target. KW at dead center.

---

## Resolved Questions

### Why doesn't KW take the "free improvement" on 3 metrics?

**Resolved.** It's not free. Every χ²-improving direction degrades kernel_autocorr. The 3-metric improvement cone (bits 10, 17) trades distributional uniformity for sequential diversity. KW preserves its unprecedented sequential anti-repetition (0th percentile) at the cost of 2 χ² steps.

### Why does bit 22 modulate coupling despite metric neutrality?

**Resolved.** Bit 22 degrades kernel_autocorr by 0.122 and changes 38 of 80 structural properties, pushing 6 to absolute extremes (all yang-balance related). Its "neutrality" was an artifact of the 3-metric frame. On 4 axes, it is actively load-bearing.

### Are any bits truly free?

**No.** kernel_autocorr has nonzero sensitivity to all 27 bits. There is no direction in the 27-dimensional space where KW can move without cost.

### What were the 19 "silent" bits carrying?

**kernel_autocorr.** Every silent bit is load-bearing for axis 4. The silence was frame limitation — the histogram metrics couldn't see sequential ordering.

---

## The Residual

**Bit 17 (pair 21, Lin/Guan)** achieves Δχ² = −1.032 at Δkac = +0.003 — ~15× more efficient than the next best trade. Two readings:

1. **Precision:** KW resolves at 0.6% of the kac range.
2. **Hidden signal:** Bit 17 pays on a 5th axis not yet measured. Structurally consistent with the pattern (each round found a constraint invisible to the previous frame).

The sage notes a third possibility: the anomaly may be geometric (a ridge on the Pareto frontier where one direction is nearly tangent to the surface) rather than structural (evidence of a missing axis). The fragility map cannot distinguish these.

---

## The Corrected Narrative

| Layer | Commitment | Legibility |
|-------|-----------|-----------|
| 2 (matching) | 100% (unique) | 10⁻¹⁷ |
| 3 (ordering) | High (2 principles) | 10⁻³ |
| 4 (orientation) | **100% (27/27 committed)** | **0.03–0.06 per axis** |

The gradient from clarity to silence was a property of the instrument, not the object. Layer 4's low per-axis legibility is not weak structure — it is *distributed* structure. A Pareto-optimal point on 4 competing axes will always appear marginal from any single projection.

The structure doesn't fade. It changes character: from algebraic uniqueness (Layer 2) to dynamical smoothness (Layer 3) to **multi-objective balance** (Layer 4). Each form of structure is less legible but equally committed.

---

## Bit Budget

| Reduction | Bits consumed | Remaining |
|-----------|:---:|-----------|
| Pairing (orbit-consistent) | ~44 orders | ~10⁴⁵ |
| Matching (identity) | ~17 orders | ~10²⁸ |
| Ordering (S=2 avoidance) | ~11 orders | ~10¹⁷ |
| Orientation hard constraints | 5 bits | 2²⁷ |
| **4-axis Pareto optimality** | **~22 bits** | **~32** |
| Bit 17 residual | ~0–1 bits | 16–32 |

Previous (iter3): ~66/89 orders accounted, ~19 bits unresolved.
Updated (iter4): **~88/89 orders accounted.** The 19 bits carry kernel_autocorr.

---

## Data Files

| Round | Findings | Data | Script |
|-------|----------|------|--------|
| 1 (gradient) | round1_single_bit.md | round1_data.json | single_bit_fragility.py |
| 2 (curvature) | round2_multi_bit.md | round2_data.json | multi_bit_fragility.py |
| 3 (structural census) | round3_structural.md | round3_data.json | structural_census.py |
| 4 (Pareto) | — | round4_data.json | pareto_analysis.py |
| Capstone | 22-fragility-findings.md | — | — |
| Map | fragility-map.md | — | — |
