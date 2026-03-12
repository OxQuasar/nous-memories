# Self-Referential Codes with Partial Visibility

## The pattern

A system where:
1. **States = transitions** (self-referential: the object is its own transformation group)
2. **Partial visibility** (a structural ceiling on how much of the state space is accessible at once)
3. **Relational output** (the system produces relations between types, not absolute measurements)
4. **Rigid quotient** (the mapping from combinatorial space to relational space is forced, not chosen)

The I Ching is the unique rigid instance of this pattern at (n,p) = (3,5). The question was whether this architecture appears elsewhere — not as metaphor, but structurally.

---

## RESOLVED: The architecture does not generalize

### Investigation summary (6 iterations, 16 computations)

**"Self-interpreting code" is not a mathematical category.** The properties that make (3,5) special are algebraically isolated through three levels of specificity:

1. **Char = 2 required.** Fixed-point-free involutory translations (the complement involution) exist only in characteristic 2. Odd characteristic (F₃) has 6 orbits at E=1, not 1. The involution is linear (not affine) in odd char, giving fundamentally different orbit geometry.

2. **|F_q| = 2 required.** GL Maximization Theorem: F₂ has the largest symmetry group for any fixed domain size. F₄² → Z₁₃ has 116,488 orbits vs F₂⁴'s 1,042 (ratio = |G| ratio = 112×). The surjection count is field-independent; only the symmetry differs.

3. **(n,p) = (3,5) required.** Orbit formula ((p−3)/2)! × 2^{2^{n-1}−1−n} = 1 only at p=5, n=3.

### Domain comparisons — all negative

| Domain | Match Type | Finding |
|--------|-----------|---------|
| Genetic code (F₄³ → 21 aa) | Architectural only | No equivariance (0/64 wobble is trivial, best non-trivial 2/64). No group target. 6:1 fiber ratio. |
| F₃ (odd char) | No match | 6 orbits at E=1. Linear involution → no analogous orbit structure. |
| F₄ (char 2, |q|>2) | No match | 116K orbits. Smaller stabilizer (12 vs 1344). Free action generic. |
| Design theory | No match | Fiber partition not a GDD. λ-values non-constant. |
| Fano labeling | No match | Complement orthogonal to projective structure. All pairs collinear. |

### What the verbal analogies mean

The candidate domains (markets, biology, neural coding, ecology, immune recognition) share the **architectural** feature of "surjection from combinatorial to relational space." This is trivially universal — every code, hash function, and classification scheme is a surjection. The **specific** algebraic properties (complement equivariance, rigid quotient, cyclic group target, involutory transitions) are F₂-specific.

**Financial markets:** The observer-participation match is the strongest verbal analogy. But markets have continuous dynamics, infinite dimensionality, and no rigidity theorem. The connection is epistemological (both reject passive observation) not algebraic.

**Genetic code:** Both are surjections from combinatorial to functional space. But the genetic code lacks equivariance, group-structured targets, fiber homogeneity, and rigidity. "Frozen accident" not forced uniqueness.

**Quantum mechanics:** Shallow match. QM uses complex Hilbert space; F₂ is finite, discrete, real-valued, non-superposable. The resemblance is epistemological only.

---

## The F₂ information architecture (updated)

The properties below are **F₂-specific and (3,5)-specific**, not instances of a general theory:

**Observer-entanglement.** F₂ self-duality: every element is both state and translation. This is automatic from char = 2 (additive inverse = identity). No analog in F₃ or F₄.

**Complementary projections.** Core and shell are orthogonal — specific to the PG(2,F₂) structure at n=3. No analog at n=4 (PG(3,F₂) has different geometry).

**The 2/5 ceiling.** Extremal within the E=1 family (2/p → 0 as p grows) but trivially forced by smallest p. Not a deep property.

**Rigid quotient.** The conjunction of three arithmetic coincidences: char=2, |F_q|=2, and (3,5). Each level eliminates vast classes of candidates.

---

## New results from the investigation

| Result | Status |
|--------|--------|
| Char-2 uniqueness theorem | Proven |
| GL Maximization Theorem | Proven |
| Surjection count field-independence | Proven |
| Free action ↔ Frame Type 2 at (3,5) | Proven |
| ANF 4-parameter family, a_{ij} = 2a₇ | Proven |
| Surjectivity locus 240/625 | Proven |
| 4D indecomposable representation over Z₅ | Computed |
| Genetic code: no equivariance | Proven (exhaustive) |

---

## Remaining open questions

### Within the (3,5) framework

1. **Dynamics beyond statics.** The 互 shear, P→H cascade, and attractor structure at (3,5) were explored in Phases 1-2. Is there a clean dynamical characterization of why the IC orbit is selected? (The static characterization is complete; the dynamical question remains.)

2. **Information-theoretic optimality.** Is there a channel-theoretic sense in which the IC surjection is optimal? The visibility ceiling is extremal but trivially so. Is there a non-trivial optimality criterion?

3. **The ANF representation.** The 4D indecomposable representation of Stab(111) over Z₅ — does it appear in representation theory tables? Is Stab(111) ≅ 2³⋊S₃ a known group with known Z₅-representations?

### Beyond the (3,5) framework

4. **The (3,5) object in other contexts.** Does the specific decorated Fano plane (PG(2,F₂) with Z₅ compass) appear in finite geometry, coding theory, or design theory under a different name?

5. **Observer-participation formalization.** Can "observer = participant" be formalized information-theoretically without F₂? The strongest domain match (markets) is epistemological, not algebraic. Is there a framework between "verbal analogy" and "algebraic isomorphism" that captures the structural insight?
