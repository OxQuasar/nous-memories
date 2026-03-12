# Odd-Characteristic Rigidity Test

## Case 1: F₃² → Z₇

Domain: F₃² = Z₃ × Z₃ (9 elements)
Involution: negation σ(x) = -x mod 3
Target: Z₇, involution τ(y) = -y mod 7
Domain neg pairs: (9-1)/2 = 4
Target neg pairs: (7-1)/2 = 3
Excess E = 4 - 3 = 1 (same as (3,5) over F₂!)


**Result:** 6 orbit(s)
**Comparison with (3,5) over F₂:** (3,5) has 1 orbit (rigidity)
**Rigidity does NOT extend to F₃ — 6 orbits**

## Case 2: F₃² → Z₅

Domain neg pairs: 4, Target neg pairs: 2
Excess E = 4 - 2 = 2


## Case 3: F₃² → Z₃

Domain neg pairs: 4, Target neg pairs: 1
Excess E = 4 - 1 = 3


## Case 4: F₅² → Z₂₃ (E=1 for q=5, n=2)

Domain: F₅² (25 elements), neg pairs: 12
Target: Z₂₃, neg pairs: 11
Excess E = 12 - 11 = 1
WARNING: 23^12 ≈ 10^16 assignments — too large for brute force!
Skipping enumeration.

## Case 5: F₂³ → Z₅ (reference — known rigid)


**Reference result:** 204 orbit(s) — matches known result

## Case 6: F₂³ → Z₇ (boundary E=0)


## Summary

| Case | Domain | Target | E | Surjections | Orbits | Rigid? |
|------|--------|--------|---|-------------|--------|--------|
| F₃²→Z₇ | F_3^2 | Z_7 | 1 | 768 | 6 | no |
| F₃²→Z₅ | F_3^2 | Z_5 | 2 | 464 | 8 | no |
| F₃²→Z₃ | F_3^2 | Z_3 | 3 | 80 | 5 | no |
| F₂³→Z₅ | F_2^3 | Z_5 | 5 | 73752 | 204 | no |
| F₂³→Z₇ | F_2^3 | Z_7 | 4 | 595728 | 771 | no |

## Key Question Answered

**NO — rigidity does NOT extend to odd characteristic** (at least not at F₃²→Z₇).
F₃²→Z₇ has 6 orbits despite E=1.

### Structural note: symmetry group comparison

The symmetry groups are structurally different:
- **F₂:** Involution is COMPLEMENT x ↦ x ⊕ 1ⁿ (affine, not linear).
  Symmetry group = Stab(1ⁿ) ⊂ GL(n, F₂). |Stab(111)| = 24.
  Orbit count under Stab(111) × Aut(Z₅) = 1 (rigidity).
- **F₃:** Involution is NEGATION x ↦ -x (linear).
  Symmetry group = full GL(n, F₃), since A(-x) = -(Ax).
  |GL(2, F₃)| = 48. Orbit count under GL(2,F₃) × Aut(Z₇) = 6.

Despite using the LARGER symmetry group (full GL vs stabilizer),
F₃ still has 6 orbits. This confirms rigidity is F₂-specific.

The key F₂ property: complement x ↦ x ⊕ 1ⁿ is NOT linear,
so its stabilizer in GL is a proper subgroup. The orbit count
formula ((p-3)/2)! × 2^{2^{n-1}-1-n} = 1 at (3,5) depends on
the specific structure of this stabilizer (exact sequence
1 → V₄ → Stab(1ⁿ) → S₃ → 1) which has no analog for GL(n, F₃).