# Q2 Proper: Computational Formalization of Situated Change

## Question

Is (F₂³, Z₅) the *minimum* implementation of 'polarity + dual evaluation',
or merely the minimum *group-theoretic* one?

## Setup

Axioms for (S, σ, R, φ):
1. S finite, |S| ≥ 2 (distinguishable states)
2. σ: S → S fixed-point-free involution (polarity)
3. R = Z_p with p ≥ 5 (dual evaluation — minimum for ≥2 independent cycles)
4. φ: S → R surjection with φ(σ(s)) = −φ(s) mod p (equivariant evaluation)

## Key Results

### R171: Minimum |S| is 6, not 8

The axioms force |R| = 5 (minimum prime with 2 independent Hamiltonian
cycles) and |S| ≥ p + 1 = 6. At |S| = 6:
- 3 σ-orbits map bijectively to 3 value classes ({0}, {1,4}, {2,3})
- Solutions exist for ALL 15 FPF involutions — no group structure needed
- Essentially unique (up to relabeling): the bijection is forced

### R172: Group structure is not forced by the axioms

At every |S| ≥ 6 (even), equivariant surjections to Z₅ exist for ANY
FPF involution on S — regardless of whether S carries group structure.
All FPF involutions on n elements are isomorphic as abstract (S, σ) pairs
(just 'n/2 disjoint 2-cycles'). Group structure is additional data, not
derivable from the axioms.

### R173: The group axiom forces F₂ᵏ, which forces |S| = 8

If we add a fifth axiom — S is a group with σ as translation — then:
- Negation Uniqueness (R85): σ must be complement in char-2 → S = F₂ᵏ
- |F₂¹| = 2, |F₂²| = 4 both too small (need ≥ 6) → k ≥ 3 → |S| ≥ 8
- At k = 3: rigidity theorem gives exactly 5 GL-orbits of surjections
- At k ≥ 4: orbit explosion (168 at k=4) → no rigidity
- ∴ F₂³ is the unique rigid group solution

### R174: The forcing chain has exactly one gap

```
Polarity          → σ FPF involution  → |S| even
Dual evaluation   → |R| ≥ 5           → R = Z₅ (minimum prime)
Equivariance      → |S| ≥ 6           → minimum: |S| = 6
        ↓
  [GAP: why must S be a group?]
        ↓
Group structure   → S = F₂ᵏ           → k ≥ 3 → |S| = 8
Rigidity theorem  → k = 3 uniquely     → (3,5) is the answer
```

The gap is between 'set with involution' and 'group with translation'.
Axioms 1-4 leave |S| = 6 as the minimum. The group axiom is what lifts
the minimum to |S| = 8 and engages the rigidity machinery.

### R175: The gap is irreducible

Four candidate fifth axioms were examined:

1. **Composability**: states can be combined (s₁ ⊕ s₂ ∈ S). Restates
   the group axiom directly.

2. **Line independence**: each state decomposes into n independent
   binary positions. Restates the F₂ⁿ structure directly.

3. **Self-referentiality**: the system can model its own evaluation.
   Either too vague to formalize, or when formalized as "the evaluation
   must be structurally unique" (rigidity), it restates the conclusion.

4. **Transition completeness**: every pair of states connected by
   single-step change. On F₂ⁿ this is Hamming-1; on a generic set it's
   just K_n — doesn't force group structure.

No candidate closes the gap without smuggling in the answer. The group
structure (composability) is the deepest contingency: the creative
insight that makes rigidity possible, not derivable from situated change.

## Minimum Solution Landscape

| |S| | p | Orbits | Classes | Class-surjections | Group? |
|-----|---|--------|---------|-------------------|--------|
| 6 | 5 | 3 | 3 | 6 (bijection) | Not required |
| 8 | 5 | 4 | 3 | 36 | F₂³ → 5 GL-orbits |
| 10 | 5 | 5 | 3 | 150 | Not F₂ᵏ |
| 8 | 7 | 4 | 4 | 24 | F₂³ possible |
| 12 | 7 | 6 | 4 | 1560 | Not minimal |
| 12 | 11 | 6 | 6 | 720 | Not minimal |
| 14 | 13 | 7 | 7 | 5040 | Not minimal |

## Interpretation

The I Ching's structure is NOT the minimum implementation of
'polarity + dual evaluation'. A 6-element set suffices. What makes
(F₂³, Z₅) special is that it's the minimum RIGID implementation —
and rigidity requires composability (group structure), which is not
derivable from the concept of change.

The forcing chain: polarity + dual evaluation + equivariance →
minimum |S| = 6. Group structure → minimum |S| = 8 on F₂³. Rigidity
→ (3,5) uniquely. The group axiom is the one contingency — the
creative act that engages the machinery. This aligns with T2: binary
encoding converges cross-culturally, but assembling it into a group
with equivariant surjection was done once.
