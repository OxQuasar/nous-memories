# Thread G Directive — The Kernel–Canon Coupling

## The Seam

Among all findings from Rounds 1–2, one demands deeper investigation: the **positive dependence between kernel uniformity and canon asymmetry** at the orientation layer.

### Why this seam, not others

The investigation produced three kinds of results:

1. **Clean nulls** — weight dynamics, yang drainage, trigram ordering, position autocorrelation, bridge smoothness. These are settled. No further investigation warranted.

2. **Clean theorems** — 14/14 forced balance, weight-invisibility, orbit_Δ invariance, nuclear ≡ M-component. These are proved. Nothing to investigate.

3. **Marginal signals** — kernel uniformity (p ≈ 0.06), canon asymmetry (p ≈ 0.05), M-component (p ≈ 0.04 uncorrected). Each is individually at the boundary of significance.

The coupling between the first two marginal signals is the anomaly. If they were independent, their joint probability would be 0.061 × 0.048 = 0.0029. The observed joint is 0.0052, giving a dependence ratio of 1.79. This means orientations that produce uniform kernel chains are ~80% more likely than chance to also produce positive canon asymmetry (upper canon favoring binary-high).

**Why is this surprising?** Kernel uniformity is a property of the 31 bridge masks — how evenly the 8 generators are distributed across bridges. Canon asymmetry is a property of the 32-bit orientation string — whether more binary-high-first pairs appear in the upper vs lower half. These live in different spaces: one is about bridge dressing, the other about reading direction. There is no obvious mechanism linking them.

**What would explain it?** Either:
- (a) A hidden structural variable constrains both simultaneously — some property of the pair/bridge geometry that forces uniform kernels and positive canon asymmetry to co-occur
- (b) The coupling is an artifact of the S=2 constraint structure (all 5 constraints are in pairs 13–30, the lower half, which mechanically affects canon asymmetry)
- (c) The coupling is a sampling artifact at the current sample size (50K)

Distinguishing (a) from (b) from (c) is the most informative thing we can do. If (a), we've found a holistic principle operating on the ~20 "silent" bits. If (b), the coupling is explained and the two signals reduce to one effective signal. If (c), the joint p ≈ 0.005 weakens.

---

## Investigations

### For the Analyst

**Investigation: Anatomize the kernel–canon coupling mechanism.**

**Method:**

1. **Stratify by S=2 constraint pattern.** The 5 S=2 constraints each have 2 valid states (equal-0 or equal-1 for equality constraints; only 0 for the fixed constraint). This gives 2⁴ = 16 constraint configurations. Within each configuration, compute the conditional correlation between kernel chi² and canon asymmetry. If the coupling vanishes within strata, it's explained by the constraint structure. If it persists, it's a genuine orientation-level phenomenon.

2. **Bridge-by-bridge contribution mapping.** Kernel chi² is a function of all 31 bridge kernels. Canon asymmetry is a function of the 32 orientation bits. For each of the 31 bridges, compute: how much does flipping the orientation of the pair(s) that influence this bridge change kernel chi² vs canon asymmetry? Build a "sensitivity map" — which bridges contribute most to the coupling?

3. **The S=2 constraint geography hypothesis.** All 5 S=2 constraints are in pairs 13–30 (lower canon). The S=2 constraints force co-orientation of adjacent pairs, which mechanically biases canon asymmetry (co-oriented pairs in the lower half push the asymmetry in one direction). At the same time, co-orientation affects the kernel at the constrained bridges. Test: among the 2²² completely free orientations (holding the 5 constrained components fixed at KW's values), what is the kernel–canon correlation? If it drops to zero, the coupling is entirely mediated by the constraint structure.

4. **Large-sample confirmation.** Increase to 500K S=2-free samples. Re-estimate the joint probability and dependence ratio with tighter confidence intervals. Current estimate: ratio = 1.79, but with 259 joint events in 50K samples, the standard error on the ratio is substantial.

**Expected output:** A clear determination of whether the coupling is (a) a genuine holistic constraint, (b) an artifact of S=2 constraint geography, or (c) a sampling fluctuation. If (a), characterize the mechanism. If (b), quantify how much of the joint p ≈ 0.005 is explained by the constraint structure vs genuine independence.

**Deliverable:** `logoswen/iter3/coupling_analysis.md`

---

### For the Structuralist

**Investigation: The M-component preference — is it independent of the coupling, or part of it?**

**Method:**

1. **Three-way joint analysis.** Compute the joint distribution of (kernel chi², canon asymmetry, M-component score) across 200K+ S=2-free orientations. The current analysis tested M-component marginally (p ≈ 0.06 among S=2-free) and the kernel–canon joint (p ≈ 0.005). But we don't know: does conditioning on kernel uniformity AND canon asymmetry affect the M-component score? If the ~259 orientations that match KW's kernel+canon profile also tend to have high M-component scores, the three signals may be one phenomenon.

2. **M-component and the S=2 constraints.** Three of the 5 S=2 constraint groups ({19,20}, {25,26}, {27,28}) involve pairs where L2 ≠ L5 (the M-axis is decisive). The co-orientation constraint at these bridges forces adjacent pairs to share orientation — which means if one pair satisfies L2<L5, the co-oriented pair is also forced to satisfy it (or violate it). This could mechanically boost the M-component score. Test: among pairs NOT in any S=2 constraint group, what is the M-component score? If it drops to 50%, the M-preference is an artifact of the constraint structure.

3. **Canon-split of all three signals.** Compute kernel chi², canon asymmetry, and M-component score separately for upper-canon bridges/pairs and lower-canon bridges/pairs. The upper canon (pairs 1–12, bridges 1–11) has zero S=2 constraints. If all three signals are present in the upper canon alone (where S=2 plays no role), the signals are genuinely orientation-layer phenomena, not constraint artifacts.

4. **Conditional independence test.** Given the S=2 constraint configuration, are the three signals (kernel uniformity, canon asymmetry, M-component) pairwise independent? Compute partial correlations controlling for constraint configuration. This directly tests whether the constraint structure mediates the coupling or whether the signals have independent sources.

**Expected output:** Whether the three Layer 4 signals are one phenomenon, two, or three. Whether the S=2 constraint geography explains any of them. A clean attribution: which part of p ≈ 0.005 is constraint-mediated, which is genuinely chosen.

**Deliverable:** `logoswen/iter3/three_signal_analysis.md`
