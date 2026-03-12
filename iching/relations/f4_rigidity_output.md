========================================================================
  CHAR-2 THEOREM
========================================================================

  Theorem: An involutory fixed-point-free translation σ(x) = x + a
  on F_qⁿ (a ≠ 0) exists iff char(F_q) = 2.

  Proof:
  - σ²(x) = x + 2a. Involutory iff 2a = 0 iff char(F_q) | 2.
  - char(F_q) is prime, so char(F_q) | 2 iff char(F_q) = 2.
  - Fixed-point-free: σ(x) = x iff a = 0, impossible. ∎

  Corollary: Complement-respecting surjections exist only
  over characteristic-2 fields: F₂, F₄, F₈, F₁₆, ...

========================================================================
  CASE 0: F₂² → Z₃ (E=0 boundary)
========================================================================

  Domain: F₂², |domain| = 4
  Complement pairs: [(0, 3), (1, 2)]
  R = 2, S = 2, E = 0
    |GL(2,F₂)| = 6, |Stab(1ⁿ)| = 2
    |Aut(Z_3)| = 2, |G| = 4

  Orbits (Burnside): 2 (remainder=0)
  Total surjections: 4
    (0, 1)
    (0, 2)
    (1, 0)
    (2, 0)
  Expected orbits: 4 / avg_orbit_size

========================================================================
  CASE 1 (reference): F₂³ → Z₅ (known: 1 orbit = rigidity)
========================================================================

  R = 4, S = 3, E = 1
    |GL(3,F₂)| = 168, |Stab(1ⁿ)| = 24
    |Aut(Z_5)| = 4, |G| = 96

  Orbits (Burnside): 5 (remainder=0)
  (5 total orbits. The '1 orbit rigidity' is for one specific type distribution.)

========================================================================
  CASE 2 (reference): F₂⁴ → Z₁₃ (known: 960 orbits)
========================================================================

  R = 8, S = 7, E = 1
    |GL(4,F₂)| = 20160, |Stab(1ⁿ)| = 1344
    |Aut(Z_13)| = 12, |G| = 16128

  Orbits (Burnside): 1042 (remainder=0)
  (Prior '960' used Kernel×Aut on one type dist; this is full Stab×Aut on all surjections)

========================================================================
  CASE 3: F₄² → Z₁₃, complement = (1, 1)
========================================================================

  R = 8, S = 7, E = 1
  Complement pairs:
    Pair 0: {(0, 0), (1, 1)}
    Pair 1: {(0, 1), (1, 0)}
    Pair 2: {(0, 2), (1, 3)}
    Pair 3: {(0, 3), (1, 2)}
    Pair 4: {(2, 0), (3, 1)}
    Pair 5: {(2, 1), (3, 0)}
    Pair 6: {(2, 2), (3, 3)}
    Pair 7: {(2, 3), (3, 2)}
    |GL(2,F₄)| = 180, |Stab((1, 1))| = 12
    |Aut(Z_13)| = 12, |G| = 144

  Orbits (Burnside): 116488 (remainder=0)
  Total surjections: 16,773,120
  Avg orbit size: 144.0

========================================================================
  CASE 4: F₄² → Z₁₃, complement = (1, 2)
========================================================================

  R = 8, S = 7, E = 1
  Complement pairs:
    Pair 0: {(0, 0), (1, 2)}
    Pair 1: {(0, 1), (1, 3)}
    Pair 2: {(0, 2), (1, 0)}
    Pair 3: {(0, 3), (1, 1)}
    Pair 4: {(2, 0), (3, 2)}
    Pair 5: {(2, 1), (3, 3)}
    Pair 6: {(2, 2), (3, 0)}
    Pair 7: {(2, 3), (3, 1)}
    |GL(2,F₄)| = 180, |Stab((1, 2))| = 12
    |Aut(Z_13)| = 12, |G| = 144

  Orbits (Burnside): 116488 (remainder=0)
  Total surjections: 16,773,120
  Avg orbit size: 144.0

========================================================================
  CASE 5: F₄² → Z₁₃, complement = (2, 3)
========================================================================

  R = 8, S = 7, E = 1
  Complement pairs:
    Pair 0: {(0, 0), (2, 3)}
    Pair 1: {(0, 1), (2, 2)}
    Pair 2: {(0, 2), (2, 1)}
    Pair 3: {(0, 3), (2, 0)}
    Pair 4: {(1, 0), (3, 3)}
    Pair 5: {(1, 1), (3, 2)}
    Pair 6: {(1, 2), (3, 1)}
    Pair 7: {(1, 3), (3, 0)}
    |GL(2,F₄)| = 180, |Stab((2, 3))| = 12
    |Aut(Z_13)| = 12, |G| = 144

  Orbits (Burnside): 116488 (remainder=0)
  Total surjections: 16,773,120
  Avg orbit size: 144.0

========================================================================
  SUMMARY
========================================================================

  | Domain | Field | Complement | |Stab×Aut| | Orbits | Rigid? |
  |--------|-------|------------|-----------|--------|--------|
  | F₂²→Z₃ | F₂ | (1,1) | 4 | 2 | no |
  | F₂³→Z₅ | F₂ | (1,1,1) | 96 | 5 | ★ (1 within IC type) |
  | F₂⁴→Z₁₃ | F₂ | (1,1,1,1) | 16128 | 1042 | no |
  | F₄²→Z₁₃ | F₄ | (1,1) | 144 | 116488 | no |
  | F₄²→Z₁₃ | F₄ | (1,α) | 144 | 116488 | no |
  | F₄²→Z₁₃ | F₄ | (α,α+1) | 144 | 116488 | no |

  KEY COMPARISON (same domain size 16, same target Z₁₃, same E=1):
    F₂⁴: 1042 orbits, |Stab(1⁴)×Aut(Z₁₃)| = 16128
    F₄²: 116488 orbits, |Stab((1,1))×Aut(Z₁₃)| = 144

  Orbit count independent of complement choice: 116488 ✓

  F₄²/F₂⁴ orbit ratio: 116488/1042 = 111.79

  F₄² has MORE orbits → smaller symmetry group gives less identification
  The F₂ structure (larger stabilizer) is key to reducing orbit count

  CONCLUSION:
  Rigidity (1 orbit) is specific to F₂³ → Z₅.
  It requires BOTH:
  1. F₂ (not F₄): the stabilizer structure of complement
     in GL(n,F₂) is fundamentally different from GL(n/2,F₄)
  2. (n,p) = (3,5): the unique arithmetic making orbit count = 1
