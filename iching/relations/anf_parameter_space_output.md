========================================================================
  GROUP ACTION ON ANF PARAMETER SPACE Z₅⁴
========================================================================

  |Stab(111)| = 24

  ====================================================================
  PART A: FULL 4×4 REPRESENTATION ON (a₁, a₂, a₄, a₇)
  ====================================================================

  The standard action: (A,α)·f = x ↦ α·f(A⁻¹x).
  For α=1, this means g(x) = f(A⁻¹x), so g = f∘A⁻¹.
  We compute the 4×4 matrix R_A such that
  params(f∘A⁻¹) = R_A · params(f).

  Homomorphism R_{AB} = R_A · R_B: ✓
  Kernel: 1 elements
  Distinct R_A: 24 (|Stab|/|ker| = 24)

  Block structure analysis:
  (a₁,a₂,a₄) independent of a₇ column: ✗
  a₇ depends on (a₁,a₂,a₄): yes
  a₇→a₇ diagonal values: [1, 4]

  Sample R_A matrices:
    A = [001,010,100]:
      [0, 0, 1, 0]
      [0, 1, 0, 0]
      [1, 0, 0, 0]
      [0, 0, 0, 1]

    A = [111,010,100]:
      [0, 0, 1, 0]
      [0, 1, 1, 2]
      [1, 0, 1, 2]
      [0, 0, 4, 4]

    A = [001,100,010]:
      [0, 0, 1, 0]
      [1, 0, 0, 0]
      [0, 1, 0, 0]
      [0, 0, 0, 1]

    A = [111,100,010]:
      [0, 0, 1, 0]
      [1, 0, 1, 2]
      [0, 1, 1, 2]
      [0, 0, 4, 4]

    A = [010,001,100]:
      [0, 1, 0, 0]
      [0, 0, 1, 0]
      [1, 0, 0, 0]
      [0, 0, 0, 1]

    A = [111,001,100]:
      [0, 1, 0, 0]
      [0, 1, 1, 2]
      [1, 1, 0, 2]
      [0, 4, 0, 4]

    ... (18 more)

  a₇ invariant under Stab(111): ✗
  18 elements change a₇:
    A = [100,010,111]: a₇ row = [0, 0, 4, 4]
    A = [100,001,111]: a₇ row = [0, 4, 0, 4]
    A = [100,111,010]: a₇ row = [0, 0, 4, 4]
    A = [100,111,001]: a₇ row = [0, 4, 0, 4]
    ... (14 more)

  Upper-left 3×3 block (action on (a₁,a₂,a₄)):

  ====================================================================
  PART B: AUT(Z₅) ACTION
  ====================================================================

  τ_k: f ↦ kf acts as scalar multiplication on ALL params.
  (a₁,a₂,a₄,a₇) → (ka₁,ka₂,ka₄,ka₇)

  ====================================================================
  PART C: ORBIT DECOMPOSITION IN Z₅⁴
  ====================================================================

  Total surjective param points: 240

  Orbits in Z₅⁴: 5, sizes [96, 48, 48, 24, 24]

  Orbit 0 (size 96, ref orbit #0, shape [2, 2, 2, 1, 1]) ★ IC:
    a₇ distribution: {0: 24, 1: 18, 2: 18, 3: 18, 4: 18}
    Rep: params=(0, 1, 2, 3), f=[3, 3, 4, 0, 0, 1, 2, 2]
  Orbit 1 (size 48, ref orbit #2, shape [2, 2, 2, 1, 1]):
    a₇ distribution: {0: 12, 1: 9, 2: 9, 3: 9, 4: 9}
    Rep: params=(1, 1, 2, 0), f=[3, 4, 4, 0, 0, 1, 1, 2]
  Orbit 2 (size 48, ref orbit #1, shape [2, 2, 2, 1, 1]):
    a₇ distribution: {0: 12, 1: 9, 2: 9, 3: 9, 4: 9}
    Rep: params=(1, 1, 2, 3), f=[0, 1, 1, 3, 2, 4, 4, 0]
  Orbit 3 (size 24, ref orbit #3, shape [4, 1, 1, 1, 1]):
    a₇ distribution: {1: 6, 2: 6, 3: 6, 4: 6}
    Rep: params=(0, 1, 2, 1), f=[0, 0, 1, 3, 2, 4, 0, 0]
  Orbit 4 (size 24, ref orbit #4, shape [4, 1, 1, 1, 1]):
    a₇ distribution: {1: 6, 2: 6, 3: 6, 4: 6}
    Rep: params=(1, 1, 3, 1), f=[4, 0, 0, 3, 2, 0, 0, 1]

  ====================================================================
  PART D: STRATA BY a₇
  ====================================================================

  a₇=0: 48 points, orbit breakdown: {0: 24, 1: 12, 2: 12}
  a₇=1: 48 points, orbit breakdown: {0: 18, 1: 9, 2: 9, 3: 6, 4: 6}
  a₇=2: 48 points, orbit breakdown: {0: 18, 1: 9, 2: 9, 3: 6, 4: 6}
  a₇=3: 48 points, orbit breakdown: {0: 18, 1: 9, 2: 9, 3: 6, 4: 6}
  a₇=4: 48 points, orbit breakdown: {0: 18, 1: 9, 2: 9, 3: 6, 4: 6}

  ====================================================================
  TASK 16: SURJECTIVITY LOCUS
  ====================================================================

  f(x) as affine function of (a₁,a₂,a₄,a₇):

    f(000) =          2a₁ + 2a₂ + 2a₄ + 4a₇ ✓   [~111: f(~000) = 2]
    f(001) =          3a₁ + 2a₂ + 2a₄ + 4a₇ ✓   [~110: f(~001) = 0]
    f(010) =          2a₁ + 3a₂ + 2a₄ + 4a₇ ✓   [~101: f(~010) = 4]
    f(011) =           3a₁ + 3a₂ + 2a₄ + a₇ ✓   [~100: f(~011) = 4]
    f(100) =          2a₁ + 2a₂ + 3a₄ + 4a₇ ✓   [~011: f(~100) = 1]
    f(101) =           3a₁ + 2a₂ + 3a₄ + a₇ ✓   [~010: f(~101) = 1]
    f(110) =           2a₁ + 3a₂ + 3a₄ + a₇ ✓   [~001: f(~110) = 0]
    f(111) =           3a₁ + 3a₂ + 3a₄ + a₇ ✓   [~000: f(~111) = 3]

  'Misses k' locus in Z₅⁴:
    Misses 0: 256/625 params
    Misses 1: 81/625 params
    Misses 2: 81/625 params
    Misses 3: 81/625 params
    Misses 4: 81/625 params

  Complement symmetry of miss loci:
    miss(1) = miss(4): ✓ identical
    miss(2) = miss(3): ✓ identical

  Surjective: 240/625 (should = 240)
  Non-surjective range sizes: {1: 1, 2: 32, 3: 128, 4: 224}

  Stab(111)-orbits (no Aut): 17, sizes [24, 24, 24, 24, 24, 12, 12, 12, 12, 12, 12, 12, 12, 6, 6, 6, 6]
    Orbit 0 (size 24, shape [4, 1, 1, 1, 1]): a₇ dist = {1: 6, 2: 6, 3: 6, 4: 6}
    Orbit 1 (size 24, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 6, 1: 6, 2: 6, 3: 6}
    Orbit 2 (size 24, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 6, 1: 6, 3: 6, 4: 6}
    Orbit 3 (size 24, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 6, 1: 6, 2: 6, 4: 6}
    Orbit 4 (size 24, shape [2, 2, 2, 1, 1]) ★: a₇ dist = {0: 6, 2: 6, 3: 6, 4: 6}
    Orbit 5 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 3: 3, 4: 6}
    Orbit 6 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 1: 6, 3: 3}
    Orbit 7 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 2: 3, 4: 6}
    Orbit 8 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 1: 3, 3: 6}
    Orbit 9 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 3: 6, 4: 3}
    Orbit 10 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 1: 3, 2: 6}
    Orbit 11 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 2: 6, 4: 3}
    Orbit 12 (size 12, shape [2, 2, 2, 1, 1]): a₇ dist = {0: 3, 1: 6, 2: 3}
    Orbit 13 (size 6, shape [4, 1, 1, 1, 1]): a₇ dist = {1: 3, 3: 3}
    Orbit 14 (size 6, shape [4, 1, 1, 1, 1]): a₇ dist = {1: 3, 2: 3}
    Orbit 15 (size 6, shape [4, 1, 1, 1, 1]): a₇ dist = {2: 3, 4: 3}
    Orbit 16 (size 6, shape [4, 1, 1, 1, 1]): a₇ dist = {3: 3, 4: 3}
