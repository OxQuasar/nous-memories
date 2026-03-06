# Mask-Signature Identity Analysis

## Executive Summary

The mask-signature identity (mask = sig for sig ≠ 0, mask = OMI for sig = 0) is the deepest structural choice in the King Wen sequence (p ≈ 10⁻¹⁷). This analysis asks: is it the unique "natural" uniform matching rule, or one of several valid choices?

**Core findings:**

1. **Even-Hamming is universal, not distinctive** — ALL Z₂³ masks have even weight. Every uniform matching produces even pair Hamming distances. What IS unique to mask=sig: the Hamming distance equals 2 × weight(sig) for every orbit.

2. **S=2 absence is matching-independent** — Among all 27 complementary assignments (the structurally motivated subset), the S=2 absence rate varies only from 2.28% to 2.84% (CV = 0.06). KW's specific mask=sig assignment ranks 26th of 27 — it does NOT optimize for S=2 avoidance. The S=2 absence depends on the **ordering**, not the matching.

3. **The mask-signature identity is the unique identity permutation** — Among the 729 weight-preserving assignments, exactly 27 satisfy the complementary pairing property (mask(x) ⊕ mask(x⊕OMI) = OMI). These 27 correspond to the 3³ permutations of {O, M, I} across the three complementary orbit pairs. KW is the unique assignment where each single-generator orbit uses the generator that **matches its own signature** — the identity permutation.

4. **Conditional S=2 probability: 2.43%** — Given KW's matching and Eulerian path, random orderings produce S=2 absence only 2.43% of the time. KW's exact S-distribution {0:15, 1:15, 3:1} occurs in 0.088% of random orderings.

---

## Investigation 1: Even-Hamming Exclusivity

### All Z₂³ Masks Have Even Weight

| Mask | 6-bit form | Weight |
|------|-----------|--------|
| O | (1,0,0,0,0,1) | 2 |
| M | (0,1,0,0,1,0) | 2 |
| I | (0,0,1,1,0,0) | 2 |
| OM | (1,1,0,0,1,1) | 4 |
| OI | (1,0,1,1,0,1) | 4 |
| MI | (0,1,1,1,1,0) | 4 |
| OMI | (1,1,1,1,1,1) | 6 |

**Theorem.** Every element of ⟨O,M,I⟩ has even weight. Each atomic generator flips exactly one mirror-pair (2 bits). The XOR of any combination preserves parity. Weight = 2 × |active generators|.

**Consequence:** Even-Hamming pair distances are a **universal property** of orbit-consistent pairing, not a distinguishing feature of mask=sig. Any of the 7⁸ uniform matching assignments produces only even pair Hamming distances.

### What IS Unique: The H = 2×|sig| Correspondence

Under mask=sig:

| Orbit type | sig weight | Mask | Pair H |
|-----------|-----------|------|--------|
| Single-gen (O, M, I) | 1 | sig | 2 |
| Double-gen (OM, OI, MI) | 2 | sig | 4 |
| Triple (Qian, Tai) | 0, 3 | OMI | 6 |

Under OTHER assignments this correspondence breaks: e.g., using mask O for orbit Zhun(110) gives H=2 instead of the structural H=4.

### Assignments Preserving the Hamming Profile

729 of 5,764,801 uniform assignments produce the same Hamming distance profile as KW (H=6 for Qian/Tai, H=2 for single-gen, H=4 for double-gen). These are exactly:

- Qian: forced to OMI (only weight-6 mask)
- Tai: forced to OMI (only weight-6 mask)  
- Single-gen orbits {Bo, Shi, XChu}: any of {O, M, I} → 3³ = 27 choices
- Double-gen orbits {WWang, Xu, Zhun}: any of {OM, OI, MI} → 3³ = 27 choices

Total: 1 × 27 × 27 × 1 = 729.

---

## Investigation 2: Cross-Orbit Bridge Properties Under Different Matchings

### Bridge S=2 Susceptibility

Of the 31 KW bridges, only **11** can ever produce S=2 (the other 20 are structurally S=2-free regardless of hexagram choice):

| Bridge | Transition | S=2 fraction (over all 64 hex pairs) |
|--------|-----------|--------------------------------------|
| B8 | Tai→Zhun | 16/64 = 25.0% |
| B13 | Qian→Qian | 24/64 = 37.5% |
| B14 | Qian→Shi | 16/64 = 25.0% |
| B15 | Shi→Zhun | 16/64 = 25.0% |
| B18 | WWang→WWang | 24/64 = 37.5% |
| B19 | WWang→Shi | 16/64 = 25.0% |
| B22 | WWang→XChu | 16/64 = 25.0% |
| B25 | Xu→Tai | 16/64 = 25.0% |
| B27 | Bo→Xu | 16/64 = 25.0% |
| B28 | Xu→Bo | 16/64 = 25.0% |
| B29 | Bo→Qian | 16/64 = 25.0% |

**Theorem (S-bound):** max_S at a bridge = 3 − w(orbit_change).

| w(orbit_change) | max_S | S=2 possible? | KW bridges with this w |
|-----------------|-------|---------------|----------------------|
| 0 (self-loop) | 3 | YES | 2 |
| 1 (single-component) | 2 | YES | 9 |
| 2 (double-component) | 1 | **NO** | 14 |
| 3 (OMI) | 0 | **NO** | 6 |

**Proof:** Each orbit-change bit means one mirror-pair has XOR=1 (exactly one line in the pair flips). Such a pair contributes 0 to S (which counts pairs where BOTH lines flip). If w(orbit_change) = k, then k mirror-pairs are "used" for the orbit change, leaving at most 3−k pairs that could both-flip. **QED.**

**Consequence:** 20 of 31 KW bridges are **structurally S=2-immune**. S=2 avoidance requires correct hexagram placement at only 11 bridges — the 2 self-loops and 9 weight-1 orbit changes. This makes S=2 absence far more achievable than the naive estimate suggests.

### Marginal Uniformity at Bridges

**Verified (100,000 samples):** With random pair assignment and random orientation, each hexagram in an orbit appears at each bridge position with probability exactly 1/8. The marginal distribution is uniform regardless of which uniform matching is used.

This means: for a **single** bridge, the S distribution is matching-independent. But correlations across bridges (hexagram used at bridge k constrains what's available at bridge k+1 within the same orbit) create weak matching dependence in the joint distribution.

### S=2 Absence Across Different Matchings

**Large-sample comparison (50,000 samples each):**

| Matching | S=2 absent | S=0 % | S=1 % | S=2 % | S=3 % |
|----------|-----------|-------|-------|-------|-------|
| **KW (mask=sig)** | **2.34%** | 49.2 | 40.3 | 9.9 | 0.5 |
| All-O | 1.91% | 49.2 | 39.2 | 10.5 | 1.1 |
| All-OMI | 1.80% | 49.3 | 40.2 | 10.5 | — |
| All-M | 1.87% | 49.2 | 39.3 | 10.5 | 1.1 |
| Reverse-KW | 1.74% | 49.2 | 39.8 | 10.5 | 0.5 |

**Key observation:** S=0 is nearly identical (49.2%) across all matchings — this is a structural invariant. S=1 and S=2 trade off slightly: mask=sig has lower S=2 (9.9% vs ~10.5%) and higher S=1 (40.3% vs ~39.2%). This small shift pushes the S=2 absence rate from ~1.8% to ~2.3%.

### The 27 Complementary Assignments

Among the 729 weight-preserving assignments, exactly 27 satisfy the complementary pairing property f(x) ⊕ f(x⊕OMI) = OMI. These are parameterized by the independent choice of {O, M, I} for each of the three weight-1 orbits {Bo, Shi, XChu}, with the weight-2 partner forced.

**S=2 absence rates (20,000 samples each):**

| Rank | Bo→ | Shi→ | XChu→ | S=2 absent | Note |
|------|-----|------|-------|-----------|------|
| 1 | I | M | M | 2.84% | |
| 2 | O | I | O | 2.81% | |
| 3 | I | M | I | 2.76% | |
| ... | | | | | |
| 14 | M | O | M | 2.54% | |
| ... | | | | | |
| 26 | **O** | **M** | **I** | **2.30%** | **← KW** |
| 27 | O | M | O | 2.28% | |

**KW ranks 26th of 27** — nearly the worst for S=2 absence among complementary assignments.

But: the total range is only 2.28%–2.84% (std = 0.14%, CV = 0.06). The matching has a **negligible effect** on S=2 avoidance. The ~2.3% rate is a property of the **Eulerian path** and the **ordering**, not the matching.

**Conclusion:** The mask-signature identity is NOT chosen to optimize S=2 absence. It is chosen for algebraic reasons (identity permutation, generator-orbit correspondence) — the S=2 avoidance comes from the ordering layer.

---

## Investigation 3: The Complement Rule — Algebraic Characterization

### The Map f: Z₂³ → Z₂³ \ {0}

The mask assignment defines a surjection f from 8 orbits to 7 non-identity generators:

```
f(sig) = sig,       if sig ≠ (0,0,0)
f(sig) = (1,1,1),   if sig = (0,0,0)
```

### Boolean Formula

**mask_k = sig_k ∨ (¬sig₁ ∧ ¬sig₂ ∧ ¬sig₃)**

"Flip the kth line pair if it's asymmetric, OR if ALL pairs are symmetric."

### Properties of f

1. **NOT a group homomorphism** — f(0) = (1,1,1) ≠ 0
2. **NOT a bijection** — f collapses {(0,0,0), (1,1,1)} → (1,1,1)
3. **Kernel of non-injectivity = {Qian, Tai}** — the Eulerian endpoints
4. **Surjective** onto Z₂³ \ {0}

### The OMI-Complementary Pairing

The OMI involution pairs orbits: {x, x⊕(1,1,1)}

| Orbit pair | Masks | XOR of masks |
|-----------|-------|-------------|
| Qian(000) ↔ Tai(111) | OMI, OMI | id (collapsed) |
| Bo(100) ↔ WWang(011) | O, MI | OMI (complementary) |
| Shi(010) ↔ Xu(101) | M, OI | OMI (complementary) |
| XChu(001) ↔ Zhun(110) | I, OM | OMI (complementary) |

**Theorem.** f(x) ⊕ f(x ⊕ OMI) = OMI for all x ∉ {(0,0,0), (1,1,1)}, and = id for x ∈ {(0,0,0), (1,1,1)}.

The three non-collapsed orbit pairs have masks that are **exact complements** — they XOR to OMI. This means: across each OMI-paired orbit pair, the two masks together activate every generator exactly once. The pairing achieves **complete generator coverage** across each complementary pair.

### Why OMI for Qian?

Among the 7 non-identity generators, OMI is the **unique** mask that:
1. Treats all 3 generators equally (no symmetry-breaking in the maximally symmetric orbit)
2. Has the same weight-class as Tai's forced mask (both are OMI)
3. Makes the Eulerian endpoints share the same matching rule
4. Maximizes the Hamming distance within pairs (H=6)

Any other choice for Qian would privilege one generator over another in the orbit where all three generators have equal standing — a structural inconsistency.

### The Identity Permutation

The 27 complementary assignments differ by a permutation of {O, M, I} across the three complementary orbit pairs. Specifically, each of the three single-generator orbits {Bo(100), Shi(010), XChu(001)} independently chooses one of {O, M, I}.

KW is the unique assignment where:
- Bo(100) → O (the generator whose bit pattern matches the orbit signature)
- Shi(010) → M (the generator whose bit pattern matches the orbit signature)
- XChu(001) → I (the generator whose bit pattern matches the orbit signature)

This is the **identity permutation**: each orbit uses the generator that IS its own symmetry structure. The mask doesn't just respect the orbit — it IS the orbit.

### Operational Interpretation

Under mask=sig, the pair partner of hexagram h is obtained by:
- **Swapping** each asymmetric line pair (where l_i ≠ l_j → flip both)
- **Preserving** each symmetric line pair (where l_i = l_j → leave alone)

The partner is the **reflection of h across its own symmetry plane** — the unique hexagram in the orbit that corrects exactly the asymmetries while preserving all agreements.

For Qian (all symmetric): the "reflection" has no plane to reflect across (all lines agree), so the rule flips everything — the partner is the complement.

---

## Investigation 4: Conditional S=2 Probability

### Setup

Fix KW's Eulerian orbit path AND KW's matching (mask=sig). Sample 50,000 random orderings (random pair slot assignment + random pair orientation within each orbit).

### Results

| Property | Value | KW actual |
|----------|-------|-----------|
| S=2 absent | **2.43%** | YES |
| Weight-5 absent | 7.35% | YES |
| \|S=0 − S=1\| ≤ 1 | 21.59% | YES (= 0) |
| Exact KW S-dist {0:15, 1:15, 3:1} | **0.088%** | YES |

### S Distribution (aggregate over 1.55M bridges)

| S | Count | % | KW actual |
|---|-------|---|-----------|
| 0 | 763,571 | 49.3% | 15/31 = 48.4% |
| 1 | 623,837 | 40.3% | 15/31 = 48.4% |
| 2 | 154,175 | 9.9% | 0/31 = 0% |
| 3 | 8,417 | 0.5% | 1/31 = 3.2% |

### Disentangling Path vs Matching vs Ordering Effects

| Condition | S=2 absent rate |
|-----------|----------------|
| Random orbit ordering + random matching (B2 baseline) | **1.22%** |
| Random orbit ordering + KW matching (mask=sig) | **0.99%** |
| KW Eulerian path + KW matching + random ordering | **2.43%** |
| Random Eulerian path + KW matching + random ordering | **~2.5%** (mean) |

**UPDATE (see path_selection_findings.md):** The orbit-change weight profile is a graph invariant — ALL Eulerian paths have exactly 11 susceptible + 20 immune bridges. The difference between the B2 baseline (~1.2%) and the Eulerian path analysis (~2.5%) is because B2 uses **random orbit orderings** (which are NOT valid Eulerian paths and have different S=2 susceptibility profiles), while the Eulerian path analysis respects the actual multigraph constraint.

Within valid Eulerian paths, the S=2 absence rate varies modestly (CV = 0.27, range 0.6%–4.6%). KW's path is unremarkable at the 42nd percentile.

The matching effect is weak: mask=sig shifts ~0.5% of bridge mass from S=2 to S=1 compared to most other matchings, but this has negligible practical impact on S=2 absence rates.

### Key Answers

**Open Question 1:** Given KW's matching (mask=sig) and KW's Eulerian path, the probability of S=2 absence under random ordering is **2.43%** (1 in 41).

**KW's exact S-distribution {0:15, 1:15, 3:1}** occurs in **0.088% = 1/1136** of random orderings — a 1-in-1000 event even after fixing both the matching and Eulerian path.

---

## The Constraint Hierarchy (Updated)

### Level 0: The space
- 64 hexagrams ∈ {0,1}⁶, 8 orbits of 8 hexagrams each

### Level 1: Orbit-consistent pairing
- **Forces:** Eulerian bridge walk, even pair Hamming distances, orbit visit uniformity
- **Eliminates:** ~44 orders of magnitude (to ~10⁴⁵)

### Level 2: Uniform matching per orbit (p ≈ 4 × 10⁻¹⁰)
- Within this: mask=sig identity (p ≈ 10⁻¹⁷ among all matchings)
- The 729 weight-preserving assignments (p ≈ 1.3 × 10⁻⁴ among uniform)
- The 27 complementary assignments (p ≈ 4.7 × 10⁻⁶ among uniform)
- The identity permutation (p ≈ 1.7 × 10⁻⁷ among uniform)
- **NOT motivated by S=2 optimization** — KW ranks 26th/27 complementary assignments
- **Motivated by:** algebraic identity (mask IS the orbit signature), generator-orbit correspondence, maximal structural self-consistency

### ~~Level 2b~~ (ELIMINATED — see path_selection_findings.md)
- The orbit-change weight profile (20 immune, 11 susceptible) is a **graph invariant**
- ALL 150,955,488 Eulerian paths have the identical weight profile
- The Eulerian path does NOT affect the S=2-susceptible bridge count
- S=2 absence rate varies modestly with path (CV=0.27), KW is at 42nd percentile (unremarkable)

### Level 3: Pair ordering (S=2 absence: p ≈ 0.025 conditional on Level 2)
- Under independence: P(all 11 avoid S=2) ≈ 2.93%
- Actual with correlations: ~2.5% (weak negative correlation)
- KW's exact S-dist {0:15, 1:15, 3:1}: p ≈ 0.001
- The 15/15 S=0/S=1 balance: p ≈ 0.22 conditional on S=2 absence

### Level 4: Pair orientation
- 2³² ≈ 4 × 10⁹ remaining degrees of freedom

---

## Key Theorems

### Theorem 1: Even-Hamming Universality
Every element of ⟨O,M,I⟩ ⊂ Z₂⁶ has even Hamming weight. Therefore every orbit-consistent pairing produces even pair Hamming distances.

### Theorem 2: Marginal Bridge Uniformity
Under random pair assignment and random orientation, the hexagram at any bridge position is uniformly distributed over the 8 hexagrams of the relevant orbit, regardless of which uniform matching is used. The per-bridge S distribution is matching-independent.

### Theorem 3: Complementary Assignment Structure
Among the 729 weight-preserving uniform assignments, exactly 27 satisfy the complementary pairing property. These are parameterized by 3 independent choices from {O,M,I} — one for each of the three complementary orbit pairs {Bo↔WWang, Shi↔Xu, XChu↔Zhun}. The weight-2 partner's mask is forced by the complementarity constraint. KW is the unique assignment where each choice is the identity (the generator matching the orbit's own signature).

### Theorem 4: S-Bound at Bridges
The maximum S value at a bridge is 3 − w(orbit_change), where w is the Hamming weight of the orbit signature change. S=2 is impossible at any bridge with w(orbit_change) ≥ 2. In KW's Eulerian path, 20 of 31 bridges have w ≥ 2 and are structurally S=2-immune. S=2 avoidance depends only on the 11 susceptible bridges.

### Theorem 5: Mask-Signature as Identity Permutation
The mask-signature rule is the unique uniform matching assignment satisfying ALL of:
1. Weight-preserving: H(pair) = 2 × weight(sig)
2. Complementary: paired orbits have complementary masks
3. Identity: each single-generator orbit uses its own generator

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `identity_analysis.py` | Investigations 1–4 (main analysis) | ✓ Complete |
| `identity_analysis_deep.py` | Deep follow-up: bridge susceptibility, 27 complementary assignments | ✓ Complete |
