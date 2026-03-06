# Round 1 Theorist Analysis: What the Baselines Reveal

## 1. The Core Result

**No generator dominates KW. None even ties on all 4 axes.** This is the headline. Among 10,000 random orientations, 100 χ²-optimized, 100 kac-optimized, and 3 targeted constructions — zero Pareto-dominate KW. The Pareto improvement cone is empty not just at Hamming distance 1 (iter4's finding), but across the entire orientation space as explored by these strategies.

This doesn't prove KW is globally Pareto-optimal — only that it's extremely hard to beat. But the pattern of *how* each generator fails is far more informative than the fact that it fails.

---

## 2. Principle Taxonomy

### Type A: Null calibration
| Generator | Logic | Result |
|-----------|-------|--------|
| A1 (random) | Uniform over S=2-free orientations | KW dominates 92.8%; 0 dominate KW |
| A2 (all-flipped) | Maximal distance from KW | Dominated by KW on all 4 axes |

### Type B: Single-axis optimizers
| Generator | Target | Target result | Collateral damage |
|-----------|--------|---------------|-------------------|
| B1 (greedy χ²) | χ² → min | 0.226 (10× better than KW) | kac collapses to −0.083 (from −0.464) |
| B2 (greedy kac) | kac → min | −0.785 (1.7× better than KW) | χ² explodes to 15.2 (from 2.3) |

### Type C: Principle-based constructors
| Generator | Principle | Design intent | Result |
|-----------|-----------|---------------|--------|
| C1 (M-rule) | L2=yin first | Maximize axis 3 (m_score) | m=15 but kac=+0.062 (positive!) |
| C2 (sequential diversity) | Max kernel Hamming from previous | Maximize axis 4 (kac) | kac=−0.666 but χ²=8.484 |

---

## 3. The Axis-Principle Map

### What controls what

| Axis | Controlled by | Indifferent to | Anti-correlated with |
|------|--------------|----------------|---------------------|
| χ² (kernel uniformity) | Global histogram balance | M-rule, polarity | Sequential diversity (kac) |
| asym (canon asymmetry) | Which-half preference | Kernel optimization | Flipping polarity (A2: −6) |
| m_score (M-component) | Per-pair L2/L5 decision | Kernel optimization | S=2 fixes that override local rule |
| kac (kernel autocorrelation) | Sequential transition variety | M-rule, polarity | Distributional uniformity (χ²) |

### The critical tension: χ² vs kac

This is the most informative finding. The two kernel-chain metrics are **nearly anti-parallel**:

- B1 (optimize χ²): achieves χ²=0.226 but kac collapses to −0.083
- B2 (optimize kac): achieves kac=−0.785 but χ² explodes to 15.2
- C2 (structural kac heuristic): kac=−0.666 but χ²=8.484

**Why they conflict:** Kernel χ² measures how evenly the 8 kernel types are distributed in aggregate (a histogram property). Kernel autocorrelation measures how much consecutive kernels avoid repeating (a sequential property). To minimize χ², you want each kernel type to appear ~3.875 times — this is a *counting* constraint. To minimize kac, you want consecutive kernels to be as different as possible — this is a *sequencing* constraint. 

A uniform distribution over 31 bridges with 8 types means ~4 of each. But to make consecutive ones maximally different, you'd want to cycle through types in a structured pattern — which tends to produce some types more and others less, depending on the graph constraints. C2's kernel distribution confirms this: {id:6, O:7, M:3, I:2, OM:3, OI:1, MI:6, OMI:3}. The sequential-diversity principle creates distributional *non*-uniformity.

**KW's resolution:** χ²=2.290 and kac=−0.464 — moderately good on both, extreme on neither. This is the signature of a trade-off, not an optimization. KW sits where the two goals reach approximate equilibrium.

### The face axes (asym, m_score) are decoupled from the flow axes

Neither B1 nor B2 (kernel optimizers) substantially affects asymmetry or m_score. B1's asym distribution (mean −1.14) is barely shifted from A1's (mean −1.56). B2's m_score distribution (mean 8.7) is barely shifted from A1's (mean 8.0). The kernel-chain metrics and the within-pair metrics live in nearly orthogonal subspaces.

**Implication:** A principle that addresses χ² and kac jointly would not automatically produce asym or m_score. The face axes need their own mechanism.

### The M-rule is a specialist

C1 maximizes m_score to 15/16 (near-perfect) but destroys kac entirely (flips it to *positive* +0.062). The M-rule orients pairs based on a per-pair property (L2 value) with no regard for what happens at the boundary between pairs. This is precisely why it kills the sequential signal — it makes orientation decisions that are locally "right" (per-pair face) but sequentially catastrophic.

KW's m_score of 12/16 suggests the M-preference is active but **overridden** at 4 of the 16 decisive positions. The 4 exceptions are where satisfying the M-rule would conflict with the kernel-chain constraints. This is the first hint of a hierarchical principle: a local per-pair rule subject to global sequential overrides.

---

## 4. Scale Separation Confirmed

The generators reveal three distinct scales of control:

| Scale | Property | Mechanism | Generators that succeed |
|-------|----------|-----------|------------------------|
| **Per-pair (local)** | m_score, asym | Which member comes first | C1 (m_score only) |
| **Sequential (nearest-neighbor)** | kac | Adjacent kernel diversity | C2 (kac only) |
| **Global (histogram)** | χ² | Aggregate kernel distribution | B1 (χ² only) |

No generator tested operates at multiple scales simultaneously. Each achieves its target scale and fails at others. This explains why no generator dominates KW: KW's profile requires simultaneous optimization across all three scales.

---

## 5. The Gap Analysis

### What's missing from every candidate

**The face-flow bridge.** No principle tested connects the per-pair orientation decision (which member first?) to the sequential-chain property (how do consecutive bridges relate?). The M-rule (C1) makes local decisions blind to sequence. The diversity rule (C2) makes sequential decisions blind to face properties. KW somehow integrates both.

**The χ²-kac balance.** C2 (sequential diversity) gets kac much better than random (−0.666 vs median −0.142) but pays heavily on χ² (8.484 vs median 6.419 — actually *worse* than random). No principle produces the combination of moderate χ² and strong kac simultaneously.

**Positive asymmetry.** Every generator except B1's population (which gets asym=+2 in one lucky case) defaults to negative asymmetry. The random mean is −1.56. This means positive asymmetry is *rare* — it requires a specific structural preference for binary-high-first in the upper half relative to the lower half. No principle tested targets this.

### The shape of the missing principle

The missing principle must:
1. Make per-pair orientation decisions (addressing axes 2 and 3)
2. While being aware of the sequential context (addressing axis 4)
3. In a way that produces distributional uniformity as a side effect (addressing axis 1)
4. With an upper-canon / lower-canon asymmetry (addressing axis 2 specifically)

Property (3) is the hardest. Distributional uniformity is usually an optimization target, not a side effect. The one scenario where it arises naturally is when a process visits all options with roughly equal frequency — i.e., a process that is *varied without trying to be uniform*. This is different from optimization. It's more like: a process with enough internal diversity that histogram uniformity is emergent.

---

## 6. Refinement Proposals for Round 2

### Proposal R2-A: Face-flow composite
Orient by M-rule (L2=yin first) as default, then override at positions where this would create a kernel repeat or near-repeat. Test different override thresholds: override when kernel would be identical to previous, when Hamming distance to previous < 2, etc. This directly addresses the missing face-flow bridge.

### Proposal R2-B: Weighted multi-objective
Instead of greedy on one axis, use a scalarized objective: minimize w₁·χ² + w₂·kac (+ possibly w₃·(16−m) + w₄·(max_asym − asym)). Sweep the weight vector to map the Pareto frontier computationally. This tells us what KW's implicit weight vector is — where on the trade-off surface it sits.

### Proposal R2-C: Balanced kernel walk
Rather than maximizing sequential diversity (C2), construct the kernel chain to be a de Bruijn–like sequence — one that is both sequentially varied AND distributionally uniform. Use a constraint satisfaction approach: find an orientation that produces a kernel sequence with no consecutive repeats AND χ² below some threshold.

### Proposal R2-D: Asymmetry-aware variant of C2
Run C2 (sequential diversity) but with a secondary criterion: when choosing between two orientations with equal kernel-Hamming score, prefer the one that makes the pair binary-high-first if in the upper canon. This tests whether asymmetry can be folded in "for free."

### Proposal R2-E: KW's 4 exceptions to M-rule
Identify the 4 pairs where KW deviates from the M-rule. Examine what these overrides achieve on the kernel chain. This may reveal the override logic directly — what sequential property KW is preserving when it sacrifices the M-preference.

---

## 7. The Current Best

**No single generator is "best" — they are incomparable.** But the most instructive comparison for next-round design:

| Generator | Coverage | Most informative failure |
|-----------|----------|------------------------|
| C2 | kac ✓, m = KW | χ² destroyed (8.5 vs 2.3) |
| C1 | m ✓✓ | kac destroyed (+0.06 vs −0.46) |
| B1 (best) | χ² ✓✓ | kac destroyed (−0.08 vs −0.46) |

**C2 is the most promising starting point** because:
1. It matches KW on m_score (12/16) without trying — the sequential diversity heuristic accidentally preserves the M-preference to exactly KW's level
2. It achieves strong kac (−0.666 vs KW's −0.464) — overshoot on this axis
3. Its failure mode (χ² explosion) has a clear mechanism (sequential structure creates distributional non-uniformity)
4. It can potentially be modified to dampen the χ² cost without destroying the kac benefit

The path from C2 to KW requires: (a) reducing χ² from 8.5 to 2.3, (b) improving asymmetry from −2 to +3, (c) relaxing kac from −0.666 to −0.464 (accepting worse sequential diversity in exchange for better distributional uniformity). This is a specific, measurable three-axis adjustment, and the direction of each adjustment is known.

---

## 8. Deeper Structural Observation

### The polarity result (A2)

The all-flipped orientation is dominated by KW on every axis. This is not obvious. Flipping all bits should invert asymmetry (it does: +3 → −6) and flip m_score (it does: 12 → 4). But it also degrades χ² (2.290 → 3.839) and kac (−0.464 → −0.376). 

The kernel-chain metrics *should* be somewhat polarity-insensitive — they depend on the XOR between consecutive hexagrams, and flipping both members of every pair changes the bridge masks in a specific way. That the degradation occurs means KW's specific polarity choices interact constructively with the pair ordering to produce better kernel statistics than the mirror image does. **KW's orientation is not just "which end is up" — it cooperates with the fixed ordering to create the kernel chain.**

### The Hamming distance pattern

All generators land at Hamming distance 13–15 from KW (except A2 at 31 and A1 at ~16). This is a striking convergence. KW sits roughly at the center of the S=2-free orientation space (Hamming ~16 from random = random distance between two random points in {0,1}^32). The optimized generators don't cluster near KW — they're roughly equidistant, each pulled to a different region of orientation space by its target axis.

**Implication:** KW is not near any single-axis optimum. It occupies a distinctive region of orientation space — roughly equidistant from the χ² minimum, the kac minimum, and the m-score maximum. This is geometric evidence for balanced multi-objective placement.

---

## 9. Summary for the Captain

**Round 1 establishes:** The four axes are genuinely in tension. No single principle dominates. The critical structural gap is the face-flow bridge — connecting per-pair orientation decisions to sequential kernel-chain properties. C2 (sequential diversity) is the most promising starting point because it accidentally preserves m_score while achieving strong kac, but it needs modification to address χ² and asymmetry.

**The question for Round 2:** Can a composite principle — one that makes per-pair decisions while maintaining sequential awareness — produce KW's balanced profile? The most productive tests would combine the M-rule (face) with sequential diversity (flow) and measure where the combination lands on the 4-axis surface.
