# Toward a Theory of Prime-Heterogeneous Rigid Structures

## Status: Framework Achieved

The original document (deep/toward-unification.md) identified five gaps that a unifying framework
would need to address. The PG(2,2) unification program (6 iterations, 17 proven results) has
resolved or clarified each gap. This document updates the assessment.

---

## The Five Gaps: Updated

### Gap 1: Prime-Indexed Constraints → RESOLVED

**Original:** No formalism where constraint type varies with prime index.

**Resolution:** PG(2,2) provides the formalism. The three lines through complement (H, P, Q) are
prime-indexed constraint carriers:

| Line | Functional | Prime pair | Constraint type |
|------|-----------|-----------|----------------|
| P = ker(b₀⊕b₁) | 五行 parity | {2,5} | Algebraic (complement = negation on Z₅) |
| Q = ker(b₀⊕b₂) | Palindromic | {2,3} | Combinatorial (which bit positions agree) |
| H = ker(b₁⊕b₂) | 互 kernel | {3,5} | Geometric (positional depth × relational dynamics) |

The prime index is not an external annotation — it emerges from the Fano geometry. Each line's
defining functional constrains different bit-position pairs, naturally selecting which prime
pairing it mediates.

The P+Q+H = 8 theorem (proved: no complement-antipodal step-XOR = OMI, so each step hits
exactly one of {P,Q,H}) shows the three prime-indexed constraints partition the transition space.

### Gap 2: Heterogeneous Gluing → RESOLVED (as feature, not bug)

**Original:** No notion of morphism subsuming algebraic, combinatorial, and geometric types.

**Resolution:** The heterogeneity is forced, not accidental. Each prime contributes a different
kind of mathematical substance:
- Prime 2: polarity (F₂ linear algebra)
- Prime 3: dimension/position (index sets, hierarchies)
- Prime 5: relation/dynamics (cyclic ordering)

The gluings between each pair are necessarily of the type appropriate to those two kinds:
- {2,5}: algebraic (complement = negation — the only involution compatible with both)
- {2,3}: combinatorial (bit-position hierarchy — which bits are erased first under 互)
- {3,5}: geometric (compass arrangement — oriented embedding of Z₅ into a circle)

A framework that homogenized the gluings would be false to the mathematics. The correct
framework *explains* the heterogeneity rather than eliminating it.

### Gap 3: Finite Rigidity Criterion → RESOLVED

**Original:** No analog of the Hasse principle for finite structures.

**Resolution:** F₂-transversality + one compass.

The rigidity decomposes into two mechanisms:
1. **F₂-transversality:** Linear constraints over F₂ reduce configuration spaces by codimension
   counting. At each stage, the constraint locus has the expected dimension (no unexpected
   intersections). This handles 7 of the 11 constraint steps.

2. **One compass:** The three non-linear constraints (Z₅ monotonicity, complement symmetry,
   FPF involutions) are all resolved by the single geometric datum of the 後天 compass
   arrangement. The compass is itself uniquely forced by the triple junction of {2,3,5}.

The rigidity criterion is: **the prime-indexed constraints are transverse over F₂, and the
non-linear residual is resolved by the compass datum.** The system has exactly 0.5 bits of
genuine freedom (the choice of which through-OMI line carries the same-element pair).

### Gap 4: Dynamics on Rigid Structures → RESOLVED

**Original:** No framework for endomorphisms respecting multi-prime structure.

**Resolution:** 互 in the factored basis.

The 互 (nuclear) transform, expressed in the product Fano geometry PG(2,2) × PG(2,2), is:
```
Position: o'=m, m'=i, i'=i⊕ī    (shift + one shear)
Orbit:    ō'=m̄, m̄'=ī, ī'=ī      (independent shift + project)
```

This is the minimal departure from a product map — one additive coupling term (ī leaks into i).
The entire attractor structure follows:
- Rank sequence 6→4→2 (coordinates killed outside-in)
- Bifurcation on ī: fixed points (ī=0, frame pair) vs 2-cycle (ī=1, Q-pair)
- Attractors Fano-aligned: {坤,乾} at origin orbit, {坎,離} at complement orbit

The P→H parity rotation under 互 (P-functional of nuclear = H-functional of original)
creates the 生/克 cross-rotation mechanism, explaining the quantitative 克 amplification
(20/13 ≈ 1.538×).

### Gap 5: Statistical Gluing → PARTIALLY ADDRESSED

**Original:** No framework mixing proven constraints with statistical evidence.

**Status:** The PG(2,2) framework is purely algebraic — it handles the 17 proven results and the
4 structural interpretations. The statistical bridge (吉×生体, p=0.007) identified in the
atlas program enters the unification only through the 0.5-bit resolution: R32 uses the textual
bridge conjunction to force the cosmological choice.

Within the Fano framework, the 0.5-bit is genuine (all four candidates are algebraically
isomorphic). The statistical bridge provides the external datum that selects among them. This
is consistent with the framework's architecture: algebraic constraints handle everything they
can, and the irreducible residual (0.5 bits) is resolved by the one piece of data the algebra
cannot see.

The deeper question — whether statistical evidence and algebraic proof can be made formally
commensurable — remains open. The hexagram system provides a clean test case: one mixed-epistemic
derivation (R32) where both types of evidence are needed.

---

## The Framework: PG(2,2) Decorated with One Compass

### Statement

The algebraic structure of the hexagram system is determined by:
1. **PG(2,2) × PG(2,2)**: Product Fano geometry with three distinguished lines through
   complement and one shear coupling the factors
2. **One compass**: Z₅ circular ordering (後天 arrangement)
3. **One choice (0.5 bits)**: Which through-OMI line carries the same-element pair

### What it explains (17 proven results)
See synthesis.md for the complete enumeration.

### What remains outside
- King Wen ordering (combinatorial — probed and confirmed null, Z < 1.5σ)
- Textual/semantic content (interpretive, not mathematical)
- Statistical gluing (mixed-epistemic, partially addressed through R32)

### The predictive test
先天 was not used to build the framework. When tested, it emerged as a corollary:
the unique complement-antipodal Hamiltonian cycle in Family H with b₀ constancy =
maximal yin/yang separation. This independent confirmation distinguishes a theory
from a description.

---

## Relationship to toward-unification.md Concrete Next Steps

The original document proposed five concrete steps. Status:

1. **"Formalize the prime-indexed constraint structure as a category"** → Achieved through
   PG(2,2). The three lines through complement are the prime-indexed constraint carriers.
   The hexagram system is not a terminal object in a category but a unique fixed point of
   F₂-transverse constraints.

2. **"Compute the obstruction"** → The obstruction is characterized: 0.5 bits. The analog
   of the Brauer-Manin obstruction is the symmetry of OMI on PG(2,2) — both candidate
   Wood pairs have XOR = OMI, making them indistinguishable to any OMI-symmetric constraint.

3. **"Test on other systems"** → Not attempted. The 24-cell, Monster group, and error-correcting
   codes remain candidate test cases. This is the most promising future direction for the
   mathematical framework (not the hexagram system specifically).

4. **"Engage F₁ theorists"** → The PG(2,2) framework provides a concrete finite-field analog
   that F₁ theory should be able to express. Whether any F₁ formalism naturally decomposes
   PG(2,2) by prime-indexed constraints is an open question.

5. **"Formalize statistical gluing"** → Open. The framework handles the algebraic part but
   defers to R32's conjunction argument for the 0.5-bit. A formal mixed-epistemic category
   remains unbuilt.
