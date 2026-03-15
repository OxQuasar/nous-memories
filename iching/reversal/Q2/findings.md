# Q2 Test 1: Alternative Axiom Systems — Findings

## Central Question

Is the (3,5) object special among all possible change-modeling systems, or only within complement-respecting binary surjections?

## Answer

**The complement axiom's algebraic form (negation equivariance) is the unique possibility within the framing. (3,5) is the unique rigid point. The structure is necessary given the framing; the framing is coherent but not itself necessary.**

---

## Three-Layer Architecture

### Layer 1: Negation is the unique equivariance type (THEOREM)

**Theorem (Negation Uniqueness).** Let f: F₂ⁿ → Z_p be a surjection with p > 2^{n−1} (singleton-forcing regime). If f(x⊕v) = α·f(x) for all x and some fixed nonzero v ∈ F₂ⁿ and α ∈ Aut(Z_p), then α = p−1 (i.e., α = −1, negation).

*Proof.* Applying the equivariance condition twice: f(x) = f(x⊕v⊕v) = α·f(x⊕v) = α²·f(x). So (α²−1)·f(x) ≡ 0 mod p for all x.
- If α² ≢ 1 mod p: f(x) = 0 for all x. Not surjective.
- If α² ≡ 1 mod p: solutions are α = 1 and α = −1 (p prime).
- For α = 1: f is constant on cosets of ⟨v⟩, giving at most 2^{n−1} distinct values. Since p > 2^{n−1}, f cannot be surjective.
- Only α = −1 remains. ∎

**Corollary.** Translation equivariance f(x⊕v) = f(x) + c is impossible for odd prime p: applying twice gives 2c ≡ 0, so c = 0, reducing to the α = 1 case.

**Corollary (Unique axis).** In the singleton-forcing regime, each equivariant surjection is equivariant w.r.t. exactly one nonzero vector. (Double equivariance w.r.t. v₁ and v₂ would give f constant on cosets of ⟨v₁⊕v₂⟩, contradicting surjectivity for p > 2^{n−1}.)

### Layer 2: Axis is a (2ⁿ−1)-fold GL-equivalent choice (THEOREM)

**Theorem (1/(2ⁿ−1) Cross-Section).** GL(n,F₂) acts transitively on the 2ⁿ−1 nonzero vectors of F₂ⁿ. If f is equivariant w.r.t. v, then f∘g⁻¹ is equivariant w.r.t. g(v). The equivariant surjections form a GL-invariant subset, and fixing any axis v selects exactly 1/(2ⁿ−1) of them.

At (3,5): 1,680 equivariant surjections, 240 per axis, fraction = 1/7.

### Layer 3: Rigidity at (3,5) (PRIOR THEOREM)

Within the complement-respecting cross-section, the orbit formula ((p−3)/2)! × 2^{2^{n−1}−1−n} equals 1 iff (n,p) = (3,5). This is the uniqueness theorem from the prior research (synthesis-3, §IV).

---

## The Unrestricted Landscape

### Orbit counts without complement equivariance

| (n,p) | |surjections| | |GL×Aut| | orbits | equivariant orbits |
|-------|-------------|---------|--------|--------------------|
| (2,3) | 36 | 12 | 5 | — |
| (3,3) | 5,796 | 336 | 63 | 6 |
| (3,5) | 126,000 | 672 | **245** | 5 |
| (3,7) | 141,120 | 1,008 | 142 | 2 |
| (4,3) | 42,850,116 | 40,320 | 3,149 | — |
| (4,5) | 131,542,866,000 | 80,640 | 1,863,977 | — |

**(3,5) has the most orbits among n=3 cases.** Without equivariance, it is the *least* rigid parameter point. Its specialness emerges only when equivariance is imposed.

### Equivariance fraction across n=3

| (n,p) | Total surj | Equivariant | Fraction | Eq orbits / Total | Multi-vector? |
|-------|-----------|------------|----------|-------------------|---------------|
| (3,3) | 5,796 | 364 | 6.28% | 6 / 63 | Yes (84 with 2 vectors) |
| (3,5) | 126,000 | 1,680 | 1.33% | 5 / 245 | No (exactly 1 each) |
| (3,7) | 141,120 | 1,344 | 0.95% | 2 / 142 | No (exactly 1 each) |

The equivariant fraction decreases with p. Only at (3,3) [non-singleton-forcing] do multi-vector equivariances occur.

### Scaling equivariance at (3,5) — all α ∈ Aut(Z₅)

| α mod 5 | Order | #Surjections | Reason if 0 |
|---------|-------|-------------|-------------|
| 1 | 1 | 0 | p > 2^{n−1}, non-surjective |
| 2 | 4 | 0 | α² ≠ 1, forces f ≡ 0 |
| 3 | 4 | 0 | α² ≠ 1, forces f ≡ 0 |
| 4 (=−1) | 2 | 1,680 | **Unique survivor** |

---

## The Singleton-Forcing Boundary

### Phase transition at p = 2^{n−1}

| Property | Below (p ≤ 2^{n−1}), e.g. (3,3) | Above (p > 2^{n−1}), e.g. (3,5) |
|----------|----------------------------------|----------------------------------|
| Equivariant fraction | 6.28% | 1.33% |
| Max equivariance axes | 2 (+ 1 periodicity) | 1 |
| Identity equivariance (α=1) | possible (252 surjections) | impossible |
| Most rigid sub-class | 2 orbits (double-equi) | **1 orbit** (Orbit C) |
| Smallest orbit size | 14 (|stab| = 24) | 168 (|stab| = 4) |

**Local symmetry and global uniqueness are in tension.** Below the boundary, individual surjections are more symmetric (larger stabilizers, more equivariance axes), but orbits are too small for global rigidity. Above the boundary, surjections are less symmetric individually, but the balance of freedom and constraint at (3,5) uniquely produces 1-orbit rigidity.

### Double-equivariance structure at (3,3)

The 84 double-equivariant surjections each have a "trident" of 3 distinguished vectors:
- v₁, v₂: negation axes, f(x⊕vᵢ) = −f(x)
- v₃ = v₁⊕v₂: periodicity axis, f(x⊕v₃) = f(x)

All 21 vector pairs appear equally (4 surjections each). All 84 have partition (4,2,2). They span 2 orbits (sizes 42 each) — no rigidity.

---

## Complement-Orbit Concentration

The 240 complement-respecting surjections at (3,5) land in exactly 5 of the 245 GL-orbits:

| GL-orbit size | Comp-resp members | Density | Stab×Aut stabilizer |
|--------------|------------------|---------|---------------------|
| 672 | 96 | 1/7 | order 1 (free action) |
| 336 | 48 | 1/7 | order 2 |
| 336 | 48 | 1/7 | order 2 |
| 168 | 24 | 1/7 | order 4 |
| 168 | 24 | 1/7 | order 4 |

The 1/7 density is uniform and group-theoretically forced. The 5 GL-orbits correspond exactly to the 5 Stab(111)×Aut(Z₅) orbits (no merging under full GL).

### Fiber partition analysis at (3,5)

| Partition | #Surjections | #Orbits | Equivariant? |
|-----------|-------------|---------|-------------|
| (3,2,1,1,1) | 67,200 | 130 | Never |
| (2,2,2,1,1) | 50,400 | 98 | 1,344 of 50,400 (2.7%) |
| (4,1,1,1,1) | 8,400 | 17 | 336 of 8,400 (4.0%) |

Partition {2,2,2,1,1} does NOT force equivariance. Equivariance requires value-alignment (complement pairs → negation pairs), not just fiber shape.

---

## Interpretation

### What is forced vs. what is chosen

| Element | Status | Mechanism |
|---------|--------|-----------|
| Binary substrate (F₂ⁿ) | Choice (axiom) | "States are binary combinations" |
| Equivariance requirement | Choice (axiom) | "Each state has an opposite" |
| Surjectivity | Choice (axiom) | "Every phase must be realized" |
| Negation (α = −1) | **Forced** | Unique equivariance type for p > 2^{n−1} |
| Complement axis (v = 111) | (2ⁿ−1)-fold choice | All GL-equivalent |
| p = 5 (two cycles) | **Forced** | Unique prime with (p−3)/2 = 1 independent cycles |
| n = 3 | **Forced** | Unique dimension with 2^{n−1} = n+1 |
| The I Ching's specific map | **Forced** | 1 orbit (Orbit C) |

### The contingency locus

The I Ching's structure is necessary given three axioms:
1. **Binary states** with polarity (F₂ⁿ domain with a complement involution)
2. **Relational codomain** (prime cyclic group Z_p as target)
3. **Completeness** (surjectivity — every phase realized)

Given these, the negation-uniqueness theorem forces the complement form, the two-cycle theorem forces p=5, the dimensional forcing theorem gives n=3, and the orbit formula gives uniqueness. The chain is fully determined.

The question "is the resonance necessary or contingent?" reduces to: **are these three axioms the right formalization of "situated change"?** This is Q2 proper from the reversal questions — a philosophical question, not a computational one.

---

## Results Inventory (21 results)

| # | Result | Status |
|---|--------|--------|
| R73 | Two-cycle uniqueness: independent cycles on Z_p = (p−3)/2, two cycles ↔ p=5 | Theorem |
| R74 | (3,5) unrestricted orbit count = 245, maximum among n=3 cases | Measured |
| R75 | Complement-respecting surjections occupy exactly 1/7 of each GL-orbit they touch | Theorem |
| R76 | 5 Stab-orbits map to 5 distinct GL-orbits (no merging under full GL) | Measured |
| R77 | GL stabilizer of comp-resp surjection = Stab×Aut stabilizer | Measured |
| R78 | E=0 orbit formula at (3,7): 2 orbits from residual assignment classes | Proven |
| R79 | p=7 complement-respecting orbits: 2 at (3,7), 610 at (4,7) | Measured |
| R80 | Equivariant surjections form GL-invariant 1.33% subset, 5 of 245 orbits | Measured |
| R81 | Each equivariant surjection has exactly 1 axis (at p > 2^{n−1}) | Measured |
| R82 | Partition {2,2,2,1,1} does not force equivariance (97.3% lack it) | Measured |
| R83 | Orbit non-monotonicity unexplained by partition diversity | Measured |
| R84 | Complement axiom locates pre-existing GL-invariant structure | Interpretation |
| R85 | Negation-uniqueness: α = −1 is unique equivariance for p > 2^{n−1} | Theorem |
| R86 | Translation equivariance: provably empty for odd prime targets | Theorem |
| R87 | Double equivariance ↔ non-singleton-forcing regime (p ≤ 2^{n−1}) | Theorem |
| R88 | Equivariance table: (3,3) 6.28%, (3,5) 1.33%, (3,7) 0.95% | Measured |
| R89 | Equivariant fraction decreases with p at fixed n | Measured |
| R90 | (3,3) double-equi: triple signature (2 negation + 1 periodicity axis) | Measured + Proven |
| R91 | 84 double-equivariant surjections span 2 orbits — no rigidity below boundary | Measured |
| R92 | Identity equivariance exists only below singleton-forcing boundary | Measured + Proven |
| R93 | All 21 vector pairs appear equally in double-equivariant class | Measured |

## Computation Files
- `phase1_p7_orbits.py` — p=7 complement-respecting orbit enumeration
- `phase2_unrestricted_orbits.py` — Unrestricted orbit landscape + complement analysis
- `phase3_internal_structure.py` — Internal GL-orbit structure
- `phase4_equivariance_landscape.py` — Equivariance across all automorphisms
- `phase5_p3_anomaly.py` — (3,3) double-equivariance structure
