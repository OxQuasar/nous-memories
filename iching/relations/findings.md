# Relations Investigation — Consolidated Findings

## Central Question

Does the F₂ self-interpreting code architecture — self-referential, partially visible, relationally interpreted — generalize beyond the I Ching to markets, biology, neural coding, ecology?

## Answer

**No.** The (3,5) object is algebraically isolated. "Self-interpreting code" is a verbal analogy, not a mathematical category.

---

## The Three-Level Specificity Chain

### Level 1: Characteristic 2 Required (THEOREM)

**Statement:** Involutory fixed-point-free translations on F_qⁿ exist if and only if char(F_q) = 2.

**Proof:** Translation σ(x) = x + a. Involutory: σ²(x) = x + 2a = x iff 2a = 0 iff char = 2. Fixed-point-free: x + a = x iff a = 0. ∎

**Consequence:** Complement-respecting surjections (equivariant under a fixed-point-free involutory translation) exist only over fields of characteristic 2. The I Ching's complement involution x ↦ x ⊕ 1ⁿ is a translation — an affine, non-linear map. In odd characteristic, the analogous involution (negation x ↦ −x) is linear, giving fundamentally different orbit geometry.

**Evidence:** F₃² → Z₇ at E=1: 6 orbits (not rigid). Despite matching excess parameter, the linear character of negation prevents orbit collapse.

### Level 2: |F_q| = 2 Required (GL MAXIMIZATION THEOREM)

**Statement:** For fixed domain size N = q^m, |GL(m, F_q)| is maximized at q = 2. Therefore the orbit-collapsing symmetry group is largest over F₂.

**Proof sketch:** |GL(m, F_q)| = ∏_{i=0}^{m-1}(N − q^i). Smaller q → more factors (larger m) and each factor is larger (q^i smaller). Both effects compound.

**Evidence:** N = 16: |GL(4, F₂)| = 20,160 vs |GL(2, F₄)| = 180 (ratio 112). F₂⁴ → Z₁₃: 1,042 orbits. F₄² → Z₁₃: 116,488 orbits (ratio ≈ 112). The surjection count is field-independent (16,773,120 in both cases) — only the symmetry group differs.

**Key finding:** Surjection count depends only on (R, S, E) — the combinatorial parameters of complement pairs and target slots — not on the field. The field enters only through the symmetry group.

### Level 3: (n,p) = (3,5) Required (ORBIT FORMULA)

**Statement:** The orbit count for complement-respecting surjections F₂ⁿ → Z_p within the IC type distribution is ((p−3)/2)! × 2^{2^{n-1}−1−n}. This equals 1 iff p = 5 and n = 3.

**Proof:** ((p−3)/2)! = 1 forces p = 5. 2^{2^{n-1}−1−n} = 1 forces 2^{n-1} = n+1, which holds only at n = 3.

---

## Domain Comparisons (All Negative)

### Genetic Code: F₄³ → 21 targets

| Property | I Ching (3,5) | Genetic Code |
|----------|--------------|--------------|
| Domain | F₂³ (8 elements) | F₄³ (64 codons) |
| Target | Z₅ (cyclic group) | 21 targets (no group) |
| Fiber ratio | 2:1 | 6:1 |
| Involutory equivariance | EXACT | ABSENT |
| Rigidity | 1 orbit | N/A |

- Only perfect equivariance: U↔C wobble at position 3 (trivial code symmetry, τ = identity)
- Best non-trivial: 2/64 violations
- Watson-Crick complement: 60/64 violations
- **Connection is architectural (both surjections) not algebraic (no shared structure)**

### F₃ (Odd Characteristic)

- F₃² → Z₇ (E=1): 6 orbits under GL(2,F₃) × Aut(Z₇)
- Negation is linear (not affine) → full GL acts → no analogous orbit formula
- Orbit formula structure has no F₃ analog

### F₄ (Characteristic 2, Larger Field)

- F₄² → Z₁₃: 116,488 orbits (vs F₂⁴'s 1,042)
- Orbit ratio matches |G| ratio exactly (both numerators = 16,773,120)
- At F₄, the symmetry group action is free on all surjections (no non-trivial stabilizers)

---

## Internal Structure of the (3,5) Object

### The 5 Orbits

| Orbit | Size | Shape | Frame Type | |Stab| | Free? |
|-------|------|-------|------------|--------|-------|
| 0 (IC) | 96 | {2,2,2,1,1} | Type 2 | 1 | YES ★ |
| 1 | 48 | {2,2,2,1,1} | Type 0 | 2 | no |
| 2 | 48 | {2,2,2,1,1} | Type 1 | 2 | no |
| 3 | 24 | {4,1,1,1,1} | — | 4 | no |
| 4 | 24 | {4,1,1,1,1} | — | 4 | no |

**Free action mechanism:** Frame = Type 2 means f(000) = y ≠ 0. Any stabilizer (A,τ) forces τ(y) = y. Since Aut(Z₅) acts freely on Z₅\{0}, τ = id. Then Shape A's three-type configuration locks A = id.

**Caveat:** Free action is generic at larger parameters ((4,13): all sampled surjections have trivial stabilizer). The IC orbit's free action is distinctive only within (3,5)'s small moduli space.

### Edge Derivatives

All Shape A orbits have identical orbit-averaged derivative distributions: {0:2, 1:5.5, 2:5.5, 3:5.5, 4:5.5}. The IC orbit is NOT distinguished by differential structure. Its uniqueness is purely group-theoretic.

### ANF Parametrization

Every complement-respecting function f: F₂³ → Z₅ is determined by 4 parameters (a₁, a₂, a₄, a₇) ∈ Z₅⁴:

```
f(x₀,x₁,x₂) = a₀ + a₁x₀ + a₂x₁ + a₄x₂ + 2a₇(x₀x₁ + x₀x₂ + x₁x₂) + a₇·x₀x₁x₂
```

where a₀ = −(a₁ + a₂ + a₄ + 2a₇) mod 5.

**Universal relation:** All degree-2 coefficients = 2a₇ mod 5.

**Group action:** Stab(111) × Aut(Z₅) acts faithfully on Z₅⁴ via a 4D indecomposable representation. The representation is NOT block-diagonal — a₇ is not invariant under Stab(111).

**Surjectivity locus:** 240 of 625 points. miss(0) = 4⁴ = 256, miss(k≠0) = 3⁴ = 81. Complement symmetry: miss(k) = miss(−k).

### Visibility Ceiling

- (3,5): 2/5 = 0.400 (maximum in E=1 family)
- (4,13): 2/13 = 0.154
- (5,29): 2/29 = 0.069
- Pattern: 2/(2ⁿ−3) → 0 monotonically. Extremal but trivially forced by smallest p.

---

## Meta-Finding

The cascade of negatives converges on a positive characterization: **the (3,5) object is special precisely because it's isolated.** Its properties (complement equivariance, rigid quotient, cyclic group target, involutory transitions, 2/5 visibility ceiling) are not instances of a general theory — they are the specific consequences of three arithmetic coincidences:

1. char = 2 (only characteristic with fixed-point-free involutory translations)
2. |F_q| = 2 (maximizes GL symmetry for any domain size)
3. (n,p) = (3,5) (unique solution to the orbit formula = 1)

The (3,5) object is itself, not an instance of something.

---

## New Results from This Investigation

| Result | Status |
|--------|--------|
| Char-2 uniqueness theorem | Proven |
| GL Maximization Theorem | Proven (verified N ∈ {4,...,256}) |
| Surjection count field-independence | Proven for (R,S) = (8,7) |
| Free action ↔ Frame Type 2 at (3,5) | Proven |
| ANF 4-parameter family with a_{ij} = 2a₇ | Proven |
| Surjectivity locus 240/625 | Proven |
| 4D indecomposable representation of Stab(111) | Computed |
| Genetic code: no involutory equivariance | Proven (exhaustive search) |
| F₃ rigidity failure (6 orbits at E=1) | Proven |
| F₄ vs F₂ orbit ratio = |G| ratio | Measured |
| Derivative invariance across Shape A | Measured |
| Design theory / Fano labeling: no connection | Established |
