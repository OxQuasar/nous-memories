# Bridge-Orientation Findings (Thread C, Round 1)

> **Central question:** How much of the 2³² orientation space is constrained by S=2 avoidance, and how does orientation affect the kernel chain?

> **Key result:** S=2 avoidance constrains exactly **5 bits** of the 32-bit orientation string, leaving 2²⁷ ≈ 134 million valid orientations (3.125% of the total space). The constraint is far weaker than expected — orientation is primarily a free design choice, not a forced structural consequence.

---

## 1. Orientation-Bridge Interaction: The 4-Variant Analysis

Each bridge k (between pair k and pair k+1) depends on which hexagram *exits* pair k and which *enters* pair k+1. There are 4 orientation variants per bridge:

| Variant | Exit hex | Entry hex |
|---------|----------|-----------|
| KW (o_k=0, o_{k+1}=0) | pair[k].b | pair[k+1].a |
| flip_L (o_k=1, o_{k+1}=0) | pair[k].a | pair[k+1].a |
| flip_R (o_k=0, o_{k+1}=1) | pair[k].b | pair[k+1].b |
| flip_LR (o_k=1, o_{k+1}=1) | pair[k].a | pair[k+1].b |

### Verified theorem: Orbit delta is orientation-invariant

All 31 bridges: orbit_Δ is identical across all 4 orientations. ✓

This is expected: both members of a pair share the same orbit (consequence of mask=sig), so the orbit change at each bridge is determined by which pair is on each side, not by which member of that pair occupies the boundary.

**Implication:** The orbit multigraph, its edge weights, and all Eulerian-path level properties are completely independent of orientation. Orientation affects only the "kernel dressing" — the position component of each bridge.

---

## 2. S=2 Susceptibility: Only 5 of 31 Bridges

Of the 11 bridges that are S=2-susceptible at the graph level (orbit change weight w < 2), only **5** produce S=2 under any orientation variant:

| Bridge | Orbit transition | w | S=2 under KW? | Orientations with S=2 |
|--------|-----------------|---|---------------|----------------------|
| B8  | Tai→Zhun    | 1 | No | 0/4 |
| B13 | Qian→Qian   | 0 | No | 2/4 (flip_L, flip_R) |
| B14 | Qian→Shi    | 1 | No | 0/4 |
| B15 | Shi→Zhun    | 1 | No | 0/4 |
| B18 | WWang→WWang | 0 | No | 0/4 |
| B19 | WWang→Shi   | 1 | No | 2/4 (flip_L, flip_R) |
| B22 | WWang→XChu  | 1 | No | 0/4 |
| B25 | Xu→Tai      | 1 | No | 2/4 (flip_L, flip_R) |
| B27 | Bo→Xu       | 1 | No | 2/4 (flip_L, flip_R) |
| B28 | Xu→Bo       | 1 | No | 0/4 |
| B29 | Bo→Qian     | 1 | No | 2/4 (flip_R, flip_LR) |

**Key insight:** 6 of the 11 graph-susceptible bridges are already S=2-immune purely from KW's pair assignment — the specific hexagrams assigned to each pair avoid S=2 regardless of orientation. This is a consequence of the mask=sig matching rule and the specific pair assignments within each orbit, not of orientation.

---

## 3. Exact Constraint Structure

### The 5 orientation constraints

| Bridge | Constraint | Interpretation |
|--------|-----------|----------------|
| B13: Qian→Qian | o₁₃ = o₁₄ | Pairs 13-14 must have EQUAL orientation |
| B19: WWang→Shi | o₁₉ = o₂₀ | Pairs 19-20 must have EQUAL orientation |
| B25: Xu→Tai | o₂₅ = o₂₆ | Pairs 25-26 must have EQUAL orientation |
| B27: Bo→Xu | o₂₇ = o₂₈ | Pairs 27-28 must have EQUAL orientation |
| B29: Bo→Qian | o₃₀ = 0 | Pair 30 MUST keep KW orientation |

### Structure of the constraints

- **4 equality constraints** (B13, B19, B25, B27): adjacent pairs must be co-oriented (both KW or both flipped). Each eliminates 50% of the 2-bit space → 1 bit lost per constraint.
- **1 fixed-value constraint** (B29): pair 30's orientation is completely determined (must be 0). This is different — it forces a specific bit value rather than relating two bits.
- **5 independent constraint components**: pairs {13,14}, {19,20}, {25,26}, {27,28}, {29,30}. No two share a pair index. The constraints factorize completely.

### The count

| Component | Pairs | Valid orientations |
|-----------|-------|-------------------|
| 1 | {13, 14} | 2 of 4 |
| 2 | {19, 20} | 2 of 4 |
| 3 | {25, 26} | 2 of 4 |
| 4 | {27, 28} | 2 of 4 |
| 5 | {29, 30} | 2 of 4 |
| Free | 22 pairs | 2²² |

**Total S=2-free orientations: 2⁵ × 2²² = 2²⁷ = 134,217,728**

**Fraction of 2³²: 1/32 = 3.125%**

**Bits lost: exactly 5.**

This is remarkably clean: S=2 avoidance eliminates exactly 5 bits of the 32-bit orientation string, leaving 27 bits completely free. The constraint is sparse (affects only 10 of 32 pairs) and local (no long-range correlations between constraint components).

---

## 4. Kernel Chain Dependence on Orientation

### Every bridge has an orientation-dependent kernel

All 31 bridges change kernel when orientation changes (31/31 orientation-dependent). Most bridges have 4 distinct kernels across the 4 orientation variants. Three bridges (B13, B18, B30) have only 2 distinct kernels — these are the self-loop bridges (Qian→Qian, WWang→WWang) and the terminal bridge (Qian→Tai).

### Kernel chain statistics: KW vs random S=2-free orientations

100,000 uniformly sampled S=2-free orientations:

| Metric | KW | S=2-free mean ± std | p-value |
|--------|-----|---------------------|---------|
| chi² (uniformity) | 2.29 | 7.32 ± 3.80 | 0.061 (5th percentile) |
| OMI-XOR fraction | 0.267 | 0.167 ± 0.069 | 0.118 |
| Mean XOR weight | 1.767 | 1.550 ± 0.161 | 0.112 |
| Generators used | 8/8 | 7.86 (86% use all 8) | — |

### Comparison: conditioning on S=2-free vs unconditional

| Metric | S=2-free mean | All orientations mean | Difference |
|--------|--------------|----------------------|------------|
| chi² (uniformity) | 7.32 | 7.06 | +0.26 |
| OMI-XOR fraction | 0.167 | 0.167 | ≈0 |

| p-value | S=2-free null | All orientations null |
|---------|--------------|----------------------|
| P(chi² ≤ KW) | 0.061 | 0.068 |
| P(OMI ≥ KW) | 0.118 | 0.122 |

**The S=2 constraint has negligible effect on kernel statistics.** The p-values barely shift between the S=2-free and unconditional null models. This makes sense: only 5 of 31 bridges are constrained, and the constraints operate on pairs (equality of orientation bits), not on specific kernel values.

### Joint probability

P(chi² ≤ 2.29 AND OMI ≥ 0.267 | S=2-free) = 0.0049 (487/100,000)

If independent: 0.061 × 0.118 = 0.0072. Ratio: 0.68 — slight negative dependence. The joint probability is lower than the iter2 value (0.002) because the null model here randomizes only orientation, not pair-ordering — a much smaller space.

### Key realization: OMI-XOR signal is from pair-ordering, not orientation

The iter2 analysis found OMI-XOR fraction p ≈ 0.029 when randomizing both pair-ordering AND orientation. Here, randomizing only orientation gives p ≈ 0.12. The OMI dominance signal comes primarily from **which pairs are assigned to which orbit slots** (Layer 3), not from **which hexagram comes first within each pair** (Layer 4).

---

## 5. Weight-5 Bridge Equivalence

Among S=2-free orientations, weight-5 bridges never appear (0/50,000 samples). This confirms: for KW's specific pair assignments, S=2-free ↔ weight-5-free at the orientation level.

However, across all 31 × 4 = 124 (bridge, orientation) combinations:
- S=2 AND weight-5: 8 cases
- S=2 but NOT weight-5: 2 cases (both at self-loop bridges where H=4 can give S=2)
- weight-5 but NOT S=2: 0 cases

So weight-5 → S≥2, but S=2 does not require weight-5. The self-loop bridges (w=0) can achieve S=2 at weight 4.

---

## 6. Hamming Weight Distribution

KW's orientation is uniquely weight-5-free among the 4 global flip variants:

| Variant | Weight distribution | Weight-5? |
|---------|-------------------|-----------|
| KW | {1:2, 2:8, 3:13, 4:7, 6:1} | No |
| flip_all_L | {1:4, 2:7, 3:8, 4:9, 5:3} | Yes |
| flip_all_R | {1:3, 2:7, 3:8, 4:9, 5:4} | Yes |
| flip_all_LR | {1:1, 2:6, 3:13, 4:9, 5:1, 6:1} | Yes |

---

## 7. Structural Summary

### The constraint hierarchy at Layer 4

| Property | Bits affected | Character |
|----------|--------------|-----------|
| S=2 avoidance | 5 of 32 | 4 equality constraints + 1 fixed value |
| Kernel uniformity | ~27 free bits remaining | KW at 5th percentile (p ≈ 0.06) |
| OMI-XOR dominance | ~27 free bits remaining | p ≈ 0.12 (not significant at this layer) |

### The 5-bit constraint is unexpectedly light

Prior expectation (from the S-bound theorem): 11 susceptible bridges, each with P(S=2) ≈ 25-37.5%, independence would give P(all avoid) ≈ 2.5-3%. But this reasoning applies to *random hexagrams at each bridge*, not to orientation flips within fixed pairs.

The actual constraint is cleaner: KW's pair assignments already eliminate S=2 at 6 of 11 susceptible bridges. At the remaining 5, the constraint is a simple equality (or fixed-value) on adjacent orientation bits. The constraint decomposes into 5 independent binary components with no inter-component coupling.

### What orientation chooses

With 2²⁷ valid orientations (all S=2-free), orientation is overwhelmingly a free design choice. The kernel uniformity signal (p ≈ 0.06) persists — KW's kernel chain is more uniform than ~94% of S=2-free orientations. But the OMI-XOR signal weakens to non-significant (p ≈ 0.12), confirming it belongs primarily to the pair-ordering layer.

The effective Layer 4 question becomes: **Among 2²⁷ ≈ 134M S=2-free orientations, did KW choose for kernel uniformity?** The p-value (0.06) is marginal but consistent with the iter2 finding. Orientation contributes to kernel uniformity but does not drive OMI contrast.

---

## Scripts

| Script | Purpose | Key output |
|--------|---------|------------|
| `bridge_orientation.py` | Per-bridge 4-variant analysis | 5 S=2-susceptible bridges identified |
| `orientation_enumeration.py` | Exact S=2-free count + constraint structure | 2²⁷ valid, 5 bits lost |
| `kernel_orientation_deep.py` | Joint kernel statistics + independence | chi² p=0.06, OMI p=0.12, joint p=0.005 |
