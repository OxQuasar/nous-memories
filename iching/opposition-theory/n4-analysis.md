# Phase 1 Capstone: Opposition Across Scales

## 1. The n=4 State Space

### States and symmetry group

16 four-bit states {0000, ..., 1111}. The symmetry group Z₂² = {id, complement, reversal, comp∘rev} acts on these states, where reversal swaps positions L1↔L4 and L2↔L3, and complement flips all bits.

### Orbits

6 orbits: 4 of size 2, 2 of size 4.

| Orbit | Size | States | Yang-weights |
|-------|------|--------|--------------|
| 1 | 2 | 0000, 1111 | 0, 4 |
| 2 | 4 | 0001, 0111, 1000, 1110 | 1, 3, 1, 3 |
| 3 | 4 | 0010, 0100, 1011, 1101 | 1, 1, 3, 3 |
| 4 | 2 | 0011, 1100 | 2, 2 |
| 5 | 2 | 0101, 1010 | 2, 2 |
| 6 | 2 | 0110, 1001 | 2, 2 |

### Fixed points

- **4 palindromes** (reversal-fixed): {0000, 0110, 1001, 1111}. Form 2 complement pairs.
- **4 anti-palindromes** (comp∘rev-fixed): {0011, 0101, 1010, 1100}. Form 2 complement pairs.
- **0 complement-fixed** (none at even n — complement has no fixed points when all bits flip).

Both reversal and comp∘rev have 4 fixed points each. Neither yields a valid complete pairing alone. Only complement produces a valid pairing from a single group element.

This fixed-point constraint is specific to even n. At odd n (n=3), complement also has no fixed points, and the palindrome count differs. The even/odd structural distinction determines which operations can serve as pairing generators.

---

## 2. Pairing Enumeration

### Search space

A pairing = a partition of 16 states into 8 unordered pairs. Total: 16!/(2⁸ × 8!) = **2,027,025** distinct pairings. All enumerated exhaustively.

### Measures computed

Four of five opposition measures are computable at n=4:

| # | Measure | Definition | Computable? |
|---|---------|------------|-------------|
| 1 | **Strength** | Σ Hamming(a,b) across 8 pairs | ✓ |
| 2 | **Diversity** | Shannon entropy of XOR mask distribution | ✓ |
| 3 | **Sequential variety** | Autocorrelation of consecutive opposition types | ✗ — requires a sequence |
| 4 | **Weight tilt** | Mean |Δ yang-count| across pairs | ✓ |
| 5 | **Weight correlation** | Pearson r of yang-counts between pair members | ✓ |

Measure 3 (sequential variety / kac) is inapplicable: it requires a canonical ordering of states into a sequence, and no such ordering exists at n=4. This measure is intrinsically *sequence-dependent*, not *pairing-intrinsic*. It becomes measurable only where a tradition supplies a sequence (n=3 circular arrangements, n=6 King Wen).

---

## 3. Each Measure at n=4

### Strength

| Property | Value |
|----------|-------|
| Range | [8, 32], all even |
| Distinct values | 13 |
| Mean ± std | 17.07 ± 2.60 |
| Distribution shape | Near-Gaussian, extreme tails |

The unique maximum S=32 belongs to a single pairing: complement (all 8 pairs at Hamming distance 4). The minimum S=8 is achieved by 272 pairings. Strength is a powerful discriminator — 13 levels across 2M pairings.

### Diversity

| Property | Value |
|----------|-------|
| Range | [0.0, 3.0] |
| Distinct values | 12 |
| Mean ± std | 2.52 ± 0.29 |
| Theoretical max | log₂(8) = 3.0 (all 8 masks distinct) |

Maximum diversity (D=3.0, all 8 pairs with distinct XOR masks) is achieved by 167,040 pairings (8.24%). Zero diversity (single mask type) is achieved by complement alone. Good discriminator.

### Weight tilt

| Property | Value |
|----------|-------|
| Range | [0.5, 1.5] |
| Distinct values | **5** |
| Values | {0.50, 0.75, 1.00, 1.25, 1.50} |

**Near-degenerate.** Only 5 levels across 2M pairings. The degeneracy is structural: at n=4, the possible yang-count differences between paired states are drawn from a small set, so the mean absolute difference has very few achievable values. Weight tilt provides almost no discrimination.

At n=6, weight tilt improves (continuous range [0.375, 1.875]) but remains strongly coupled to weight correlation (r = −0.73). This raises the question: is weight tilt a derivative of weight correlation rather than an independent axis?

### Weight correlation

| Property | Value |
|----------|-------|
| Range | [−1.0, +1.0] |
| Distinct values | 126 |
| Mean ± std | +0.27 ± 0.36 |

The most discriminating measure at n=4. The extreme values belong to named pairings: r = −1.0 (complement, unique) and r ≈ +0.07 (KW-style). Continuous distribution with no degeneracy.

### Effective dimensionality

The 5-measure framework reduces to **3 effective pairing dimensions** at n=4:

1. **Strength** — well-defined, independent
2. **Diversity** — well-defined, independent, orthogonal to everything
3. **Weight structure** — weight correlation is the primary axis; weight tilt is a near-degenerate derivative

Plus **1 sequence-dependent dimension** (sequential variety / kac) that only activates when an ordering is imposed.

---

## 4. The Pareto Frontier

### Inter-measure correlations

| Pair | Pearson r | Note |
|------|-----------|------|
| **S ↔ D** | **0.000** | Exactly zero to machine precision |
| S ↔ Weight Tilt | +0.313 | Moderate |
| **S ↔ Weight Corr** | **−0.611** | Strong: high-strength ↔ weight anti-correlation |
| **D ↔ Weight Tilt** | **0.000** | Exactly zero |
| D ↔ Weight Corr | +0.004 | Negligible |
| Weight Tilt ↔ Weight Corr | −0.607 | Strong: these two are nearly redundant |

**Two exact zeros.** Diversity is uncorrelated with both strength and weight tilt to machine precision. Diversity is also negligibly correlated with weight correlation (+0.004). Diversity is orthogonal to every other measure — it appears to capture a structurally independent dimension of pairing geometry.

The S ↔ Weight Corr coupling (r = −0.61) is the strongest inter-measure relationship: pairings with high strength necessarily anti-correlate weights (complement-like behavior), while low-strength pairings pair similar weights.

### The feasible region

The S×D space is **lens-shaped**:

| Strength | Max D | Min D | Count |
|----------|-------|-------|-------|
| 32 | 0.00 | 0.00 | 1 |
| 30 | 0.81 | 0.81 | 16 |
| 28 | 1.55 | 0.81 | 216 |
| 26 | 2.16 | 0.81 | 2,800 |
| 24 | 2.75 | 0.00 | 21,624 |
| 22 | 3.00 | 0.81 | 105,696 |
| 20 | 3.00 | 0.81 | 316,992 |
| 18 | 3.00 | 0.81 | 566,592 |
| 16 | 3.00 | 0.00 | 585,360 |
| 14 | 3.00 | 0.81 | 327,296 |
| 12 | 2.75 | 0.81 | 90,368 |
| 10 | 2.50 | 0.81 | 9,792 |
| 8 | 2.00 | 0.00 | 272 |

Boundary constraints are **symmetric**: both high and low strength cap achievable diversity. Full diversity (D=3.0) is freely achievable only in the interior (S ∈ [14, 22]). The bulk of pairings cluster around S ≈ 16–18.

### The 2D Pareto staircase

Maximizing both S and D simultaneously yields a 6-point frontier:

| S | D | Count on frontier |
|---|---|-------------------|
| 32 | 0.000 | 1 |
| 30 | 0.811 | 16 |
| 28 | 1.549 | 96 |
| 26 | 2.156 | 768 |
| 24 | 2.750 | 672 |
| 22 | 3.000 | 1,536 |

Total: 3,089 pairings on the 2D frontier (0.15% of all). Each step trades 2 strength for 0.4–0.8 diversity. The frontier IS the upper-right boundary of the feasible lens.

---

## 5. Named Pairings

### Complement

Pair each state with its bitwise complement. The analog of Shao Yong / Fu Xi at every scale.

| Measure | Value | Position |
|---------|-------|----------|
| Strength | 32 | Maximum (unique) |
| Diversity | 0.000 | Minimum |
| Weight Tilt | 1.500 | Maximum |
| Weight Corr | −1.000 | Extreme negative |
| Equivariant | under all of Z₂² | |
| Pareto (2D, 3D, 5D) | ✓ all | |

Complement is the extreme of concentrated opposition. One mask type (1111), repeated 8 times. Maximum strength because every bit differs in every pair. On every Pareto frontier. The single pairing that uniquely achieves S=32.

### KW-style (reversal + complement fallback for palindromes)

The n=4 analog of the King Wen hexagram pairing rule: pair non-palindromes by reversal, palindromes by complement.

| Pair | XOR mask | Distance | Type |
|------|----------|----------|------|
| 0000 ↔ 1111 | 1111 | 4 | complement (palindrome) |
| 0110 ↔ 1001 | 1111 | 4 | complement (palindrome) |
| 0011 ↔ 1100 | 1111 | 4 | complement (comp∘rev-fixed) |
| 0101 ↔ 1010 | 1111 | 4 | complement (comp∘rev-fixed) |
| 0001 ↔ 1000 | 1001 | 2 | reversal |
| 0010 ↔ 0100 | 0110 | 2 | reversal |
| 0111 ↔ 1110 | 1001 | 2 | reversal |
| 1011 ↔ 1101 | 0110 | 2 | reversal |

| Measure | Value | Position |
|---------|-------|----------|
| Strength | 24 | 75th percentile |
| Diversity | 1.500 | 3 mask types: {1111, 1001, 0110} |
| Weight Tilt | 0.500 | **Minimum** |
| Weight Corr | +0.067 | Near zero |
| Equivariant | under all of Z₂² | |
| Pareto (2D, 3D, 5D) | ✗ all | Dominated by 23,632 pairings |

The KW-style pairing is fully Z₂²-equivariant (one of only 117 such pairings, 0.006% of all). But it is **not on any Pareto frontier**. The structural limitation: at n=4, every reversal pair has Hamming distance exactly 2, contributing only 2 mask types (1001 and 0110). At S=24, the maximum achievable diversity is 2.75 — KW-style reaches only 1.50.

The 4 comp∘rev-fixed states (0011, 0101, 1010, 1100) "accidentally" pair by complement under the KW rule, because reversing them yields their complement. This gives mask 1111 a count of 2 (palindrome complement pairs) + 2 (accidental complement pairs from comp∘rev-fixed) = 4, while the reversal masks (1001, 0110) each get 2.

### Invalid single-operation pairings

- **Reversal**: 4 palindromes are self-reversal → not a complete pairing
- **Comp∘rev**: 4 anti-palindromes are self-images → not a complete pairing

### Equivariance counts

| Equivariant under | Count | % of 2,027,025 |
|-------------------|-------|-----------------|
| complement | 5,937 | 0.29% |
| reversal | 993 | 0.05% |
| comp∘rev | 993 | 0.05% |
| **all three (full Z₂²)** | **117** | **0.006%** |

Both complement and KW-style are among the 117 fully equivariant pairings.

---

## 6. The S↔D Orthogonality

### The finding

| Scale | r(S, D) | Method | Pairings |
|-------|---------|--------|----------|
| n=3 | 0.000 (exact) | Exhaustive | 105 |
| n=4 | 0.000 (exact) | Exhaustive | 2,027,025 |
| n=6 | −0.002 (≈ 0) | 100K sample | (sampling error ~0.003) |

Strength and diversity are **exactly uncorrelated** at n=3 and n=4, and consistent with zero at n=6. This is the central structural finding of Phase 1.

### Not independence — orthogonality with nonlinear dependence

E[D|S] traces an inverted U: diversity is constrained at both extremes of strength and peaks in the interior (S ≈ 16–18 at n=4). The conditional variance of D given S is also non-constant. They are linearly uncorrelated but *not* independent.

The zero linear correlation arises because the nonlinear dependence is symmetric: the inverted-U shape cancels exactly in the Pearson inner product. Strength depends on mask *weights* (Hamming distances); diversity depends on mask *multiplicities* (how many pairs share each mask type). Under the symmetry of the uniform distribution over perfect matchings, these two functions are orthogonal in the L² sense.

### What this refutes and what it establishes

**Refuted:** The original hypothesis that strength and diversity trade off globally. No such trade-off exists. They are free to vary independently.

**Established:** The constraint is purely at the boundaries. At extreme strength (S ≥ 24 at n=4), the feasible diversity ceiling drops. At extreme low strength (S ≤ 10), it also drops. In the large interior, both can be jointly maximized. The correct geometric picture is a lens-shaped feasible region, not an anti-correlated axis.

### Diversity's universal orthogonality

Diversity is also exactly uncorrelated with weight tilt at n=4 (r = 0.000), and negligibly correlated with weight correlation (+0.004) and reversal symmetry (−0.025). At n=6, diversity correlates with nothing: r(D, WT) = −0.003, r(D, WC) = +0.005.

Diversity appears to measure a structurally independent axis of pairing geometry — something like the combinatorial topology of the matching, orthogonal to all weight-based and symmetry-based properties.

---

## 7. The Phase Transition: n=4 → n=6

### KW shifts from dominated to extreme

| Property | n=4 | n=6 |
|----------|-----|-----|
| Strength | 24 (75th %ile) | 120 (**99.98th** %ile) |
| Diversity | 1.50 (interior) | 2.750 (**0th** %ile — below all 100K random) |
| Weight Tilt | 0.50 (minimum) | 0.375 (**0th** %ile — below all random) |
| Weight Corr | +0.07 (near zero) | +0.516 (**97.65th** %ile) |
| Pareto frontier | ✗ dominated by 23,632 | N/A (but extreme on S axis) |
| Z₂²-equivariant | Yes (1 of 117) | Yes (0 of 10K random) |

At n=4, KW-style is mediocre. At n=6, it is extreme on every axis and outside the random distribution on most. The same pairing rule — reversal for non-palindromes, complement for palindromes — produces qualitatively different results at the two scales.

### The mechanism: reversal expressiveness

At n=4: **2 mirror pairs** (L1↔L4, L2↔L3). Reversal can vary along 2 binary axes → 3 possible nonzero signature masks. But all reversal pairs are locked at Hamming distance 2 and contribute only 2 of 3 mask types. The signature space is barely expressible.

At n=6: **3 mirror pairs** (L1↔L6, L2↔L5, L3↔L4). Reversal varies along 3 binary axes → 7 possible nonzero signature masks. Reversal pairs span distances {2, 4, 6} and contribute all 7 mask types. The Z₂³ signature group is fully expressible for the first time.

The transition is qualitative, not gradual. With 2 mirror pairs, the KW rule is structurally cramped — reversal is too uniform to generate either high strength or high mask diversity. With 3 mirror pairs, the same rule accesses the full algebraic repertoire.

### The algebraic diversity ceiling

KW's diversity, when measured against the maximum achievable using only signature masks (the "algebraic ceiling"), is near-optimal at every scale:

| Scale | k (mirror pairs) | Algebraic ceiling | KW diversity | % of ceiling |
|-------|-------------------|-------------------|--------------|--------------|
| n=4 | 2 | log₂3 ≈ 1.585 | 1.500 | 95% |
| n=6 | 3 | log₂7 ≈ 2.807 | 2.750 | 98% |

The combinatorial ceiling (all pairs with distinct masks) is log₂(8) = 3.0 at n=4 and log₂(32) = 5.0 at n=6. Against these, KW's diversity looks low (1.50 of 3.0 at n=4, 2.75 of 5.0 at n=6). But the gap is entirely due to algebraic restriction: KW uses only the 2^k − 1 signature masks, not all 2^n − 1 possible masks. Within that restricted vocabulary, it uses nearly every type at nearly equal frequency. "Low diversity" in the combinatorial sense is "high purity" in the algebraic sense.

The deviation from the ceiling comes entirely from the 111111/1111 mask getting double weight: palindrome complement pairs and comp∘rev-fixed "accidental" complement pairs both produce this mask. At n=6, this gives the 111111 mask count 8 instead of 4, accounting for the gap from log₂7.

---

## 8. Implications for the Opposition Theory Framework

### Three revisions forced by the data

**1. Orthogonality replaces trade-off.** The original framing predicted a global trade-off between opposition strength and diversity. The data show exact orthogonality at n=3 and n=4, confirmed at n=6. Strength and diversity are independent degrees of freedom with boundary constraints at extremes, not ends of a tension.

**2. Algebraic purity replaces diversity maximization.** KW does not maximize combinatorial diversity. It maximizes *algebraically structured* opposition: using exactly the masks generated by the mirror-pair signature group, with near-uniform distribution, and no others. The 56 unused masks at n=6 are excluded as a class by the equivariance constraint, not rejected individually. The correct characterization of KW is: **maximize opposition strength subject to Z₂²-equivariance.**

**3. Equivariance IS the mask constraint.** Z₂²-equivariance (the pairing respects the orbit structure) and the algebraic mask constraint (mask = orbit signature) are the same property expressed differently. They collapse into a single structural requirement. At n=6, this property is shared by 0 of 10K random pairings — it is astronomically rare.

### Measure reduction

The original 5 measures reduce to a more parsimonious set:

- **3 pairing-intrinsic dimensions**: strength, diversity, weight structure (correlation). Weight tilt is near-degenerate at n=4 (5 values) and strongly coupled to weight correlation at both n=4 (r = −0.61) and n=6 (r = −0.73) — it is a derivative, not an independent axis.
- **1 sequence-dependent dimension**: sequential variety (kac). Only measurable when a tradition supplies an ordering. Not a property of the pairing itself.
- **1 structural property**: equivariance. Not a continuous measure but a discrete constraint that partitions the pairing space into algebraically structured vs unconstrained.

This suggests the opposition space for pairings is effectively 3-dimensional (S, D, weight structure), with equivariance as a discrete structural constraint that drastically narrows the feasible region.

### What complement and KW-style each optimize

**Complement (Shao Yong/Fu Xi):** Maximizes strength. Zero diversity. Perfect weight anti-correlation. On every Pareto frontier. The degenerate extreme — one operation, one mask, maximum force.

**KW-style:** Maximizes strength subject to equivariance, using reversal as the primary operation. Near-maximal algebraic diversity. Near-zero weight tilt (reversal preserves yang-count). Not Pareto-optimal at n=4 (reversal is too uniform), but extreme at n=6 (reversal spans the full signature space). The design principle only realizes its potential at the hexagram scale.

---

## 9. Revised Predictions (Confirmed at n=6)

Phase 1 generated predictions about n=6 based on the n=4 structural analysis. These were subsequently confirmed by the n=6 computation:

| Prediction | n=6 Result |
|------------|------------|
| S↔D orthogonality persists | r = −0.002 ✓ |
| KW shifts from dominated to extreme | 99.98th percentile strength ✓ |
| Reversal generates diverse masks at n=6 | 7 distinct masks (all signature types) ✓ |
| Equivariance becomes rarer at larger n | 0 of 10K random pairings ✓ |
| KW near algebraic diversity ceiling | 98% of log₂7 ✓ |

The one finding that was *not* predicted: KW falls **below the random floor** on diversity and weight tilt. It isn't just at the low end of the distribution — it's outside it entirely. This is the signature of algebraic purity: no random pairing restricts itself to 7 of 63 possible masks, because equivariance is a zero-probability event at this scale.

---

## 10. Phase 2 Recommendations

### Framework selection

The three candidate frameworks from the plan are now differentially supported:

**Option A (Pareto):** Validated at n=4 as a descriptive tool. The 6-point staircase cleanly characterizes the S×D frontier. But at n=6, exhaustive enumeration is impossible, limiting the Pareto approach to sampling. And the key insight — algebraic purity — is not naturally expressed in Pareto terms.

**Option B (Weighted functional):** **Eliminated.** The exact orthogonality of S and D means no single linear functional Σλᵢfᵢ captures both. Any weighted combination will be indifferent to diversity (or to strength), because the two contribute zero covariance.

**Option C (Information-theoretic):** **Favored.** "Maximize entropy within the signature-mask constraint" naturally captures the algebraic ceiling result. KW achieves 98% of log₂7 — this is entropy maximization subject to algebraic restrictions on the mask vocabulary. The information-theoretic frame explains both *what* KW does (near-maximal entropy over signature masks) and *why* diversity appears low (the vocabulary is algebraically restricted).

### Next computational question

**Is KW the unique strength-maximizer among equivariant pairings?** The 117 fully Z₂²-equivariant pairings at n=4 are already identified. Among equivariant pairings that use reversal as the primary operation (i.e., pair non-palindromes by reversal), is complement-fallback for palindromes the unique strength-maximizing completion? If so, the KW pairing rule is fully characterized: *the strength-maximizing reversal-based equivariant pairing.*

This is tractable at n=4 and, if the equivariant pairings at n=6 can be enumerated, potentially at n=6 as well.

### Downstream phases (unchanged)

- **Phase 3 (Nuclear trigrams):** The L3|L4 boundary question is independent of the framework revision. Can proceed in parallel.
- **Phase 4 (生克 synthesis):** Requires the framework to stabilize. Wait for Option C formalization.

---

## Files

| Location | Contents |
|----------|----------|
| `n4/enumerate.py` | Exhaustive enumeration, 4 measures → `measures.npz`, `meta.json` |
| `n4/structure.py` | Z₂² orbits, fixed points, equivariance → `structure.md` |
| `n4/pareto.py` | Pareto frontiers, scatter plots → PNGs |
| `n4/results.md` | Full n=4 results |
| `n4/measures.npz` | 2,027,025 × 5 compressed measure arrays |
| `n6/compute.py` | KW + Shao Yong measures, 100K random sample |
| `n6/results.md` | Full n=6 results |
| `n6/sample_measures.npz` | 100K random pairing measures |
| `n6/summary.json` | Named pairing measures + correlations |
| `opposition-theory.md` | Living theory document (updated with all findings) |
| `plan.md` | Original study plan (Phase 1 now complete) |
