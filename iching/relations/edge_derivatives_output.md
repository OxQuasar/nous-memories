========================================================================
  EDGE DERIVATIVE PROFILE
========================================================================

  5 orbits, sizes: [96, 48, 48, 24, 24]

  ====================================================================
  I CHING DERIVATIVE TABLE
  ====================================================================

  f = [2, 0, 4, 3, 2, 1, 0, 3]
      x  f(x)   d(x,001) d(x,010) d(x,100)   s(x) w(x)
  ----------------------------------------------------
    000     2          3        2        0      2    4   坤(Earth)
    001     0          2        3        1      3    5   震(Wood)
    010     4          4        3        1      3    4   坎(Water)
    011     3          1        2        0      2    3   兌(Metal)
    100     2          4        3        0      2    3   艮(Earth)
    101     1          1        2        4      3    4   離(Fire)
    110     0          3        2        4      3    5   巽(Wood)
    111     3          2        3        0      2    4   乾(Metal)

  Derivative distribution: {0: 4, 1: 4, 2: 6, 3: 6, 4: 4}
  Average Boolean sensitivity: 2.500
  Total weighted sensitivity: 32

  Complement antisymmetry check: d(x,m) + d(x⊕m, m) ≡ 0 mod 5
  ✓ All pass

  ====================================================================
  DERIVATIVE COMPARISON ACROSS ALL ORBITS
  ====================================================================

  Orbit  Size           Shape                Deriv Dist Avg s(x)    W  IC Dinv
  ---------------------------------------------------------------------------
      0    96 [2, 2, 2, 1, 1] {0: 4, 1: 6, 2: 4, 3: 4, 4: 6}    2.500   28   ★  (4)
      1    48 [2, 2, 2, 1, 1]  {1: 8, 2: 4, 3: 4, 4: 8}    3.000   32      (4)
      2    48 [2, 2, 2, 1, 1] {0: 4, 1: 4, 2: 6, 3: 6, 4: 4}    2.500   32      (4)
      3    24 [4, 1, 1, 1, 1] {0: 4, 1: 6, 2: 4, 3: 4, 4: 6}    2.500   28      (2)
      4    24 [4, 1, 1, 1, 1] {0: 4, 1: 4, 2: 6, 3: 6, 4: 4}    2.500   32      (2)

  Dinv = derivative distribution is orbit-invariant (same for all elements)

  ====================================================================
  DERIVATIVE TABLES FOR ORBIT REPRESENTATIVES
  ====================================================================

  ─── Orbit 0 (I Ching) ───
  f = [1, 0, 1, 2, 3, 4, 0, 4], shape = [2, 2, 2, 1, 1]
      x  f(x)   d(001) d(010) d(100)   s(x)
    000     1        4      0      2      2
    001     0        1      2      4      3
    010     1        1      0      4      2
    011     2        4      3      2      3
    100     3        1      2      3      3
    101     4        4      0      1      2
    110     0        4      3      1      3
    111     4        1      0      3      2
  Dist: {0: 4, 1: 6, 2: 4, 3: 4, 4: 6}, W=28

  ─── Orbit 1  ───
  f = [0, 1, 1, 2, 3, 4, 4, 0], shape = [2, 2, 2, 1, 1]
      x  f(x)   d(001) d(010) d(100)   s(x)
    000     0        1      1      3      3
    001     1        4      1      3      3
    010     1        1      4      3      3
    011     2        4      4      3      3
    100     3        1      1      2      3
    101     4        4      1      2      3
    110     4        1      4      2      3
    111     0        4      4      2      3
  Dist: {1: 8, 2: 4, 3: 4, 4: 8}, W=32

  ─── Orbit 2  ───
  f = [1, 0, 2, 2, 3, 3, 0, 4], shape = [2, 2, 2, 1, 1]
      x  f(x)   d(001) d(010) d(100)   s(x)
    000     1        4      1      2      3
    001     0        1      2      3      3
    010     2        0      4      3      2
    011     2        0      3      2      2
    100     3        0      2      3      2
    101     3        0      1      2      2
    110     0        4      3      2      3
    111     4        1      4      3      3
  Dist: {0: 4, 1: 4, 2: 6, 3: 6, 4: 4}, W=32

  ─── Orbit 3  ───
  f = [0, 0, 1, 2, 3, 4, 0, 0], shape = [4, 1, 1, 1, 1]
      x  f(x)   d(001) d(010) d(100)   s(x)
    000     0        0      1      3      2
    001     0        0      2      4      2
    010     1        1      4      4      3
    011     2        4      3      3      3
    100     3        1      2      2      3
    101     4        4      1      1      3
    110     0        0      3      1      2
    111     0        0      4      2      2
  Dist: {0: 4, 1: 6, 2: 4, 3: 4, 4: 6}, W=28

  ─── Orbit 4  ───
  f = [1, 0, 0, 2, 3, 0, 0, 4], shape = [4, 1, 1, 1, 1]
      x  f(x)   d(001) d(010) d(100)   s(x)
    000     1        4      4      2      3
    001     0        1      2      0      2
    010     0        2      1      0      2
    011     2        3      3      2      3
    100     3        2      2      3      3
    101     0        3      4      0      2
    110     0        4      3      0      2
    111     4        1      1      3      3
  Dist: {0: 4, 1: 4, 2: 6, 3: 6, 4: 4}, W=32

  ====================================================================
  ORBIT-LEVEL AGGREGATE ANALYSIS
  ====================================================================

  NOTE: Derivative distribution varies within orbits (not orbit-invariant).
  Computing ORBIT-AVERAGED statistics.

  Orbit 0 (size 96, shape [2, 2, 2, 1, 1]) ★:
    Avg derivative dist: {0:2.0, 1:5.5, 2:5.5, 3:5.5, 4:5.5}
    Avg weighted sensitivity: 33.00
    W distribution: {28: 24, 32: 48, 40: 24}

  Orbit 1 (size 48, shape [2, 2, 2, 1, 1]):
    Avg derivative dist: {0:2.0, 1:5.5, 2:5.5, 3:5.5, 4:5.5}
    Avg weighted sensitivity: 33.00
    W distribution: {28: 12, 32: 24, 40: 12}

  Orbit 2 (size 48, shape [2, 2, 2, 1, 1]):
    Avg derivative dist: {0:2.0, 1:5.5, 2:5.5, 3:5.5, 4:5.5}
    Avg weighted sensitivity: 33.00
    W distribution: {28: 12, 32: 24, 40: 12}

  Orbit 3 (size 24, shape [4, 1, 1, 1, 1]):
    Avg derivative dist: {0:4.0, 1:5.0, 2:5.0, 3:5.0, 4:5.0}
    Avg weighted sensitivity: 30.00
    W distribution: {28: 12, 32: 12}

  Orbit 4 (size 24, shape [4, 1, 1, 1, 1]):
    Avg derivative dist: {0:4.0, 1:5.0, 2:5.0, 3:5.0, 4:5.0}
    Avg weighted sensitivity: 30.00
    W distribution: {28: 12, 32: 12}

  ====================================================================
  ANALYSIS
  ====================================================================

  KEY FINDINGS:

  1. Derivative distribution is NOT orbit-invariant.
     Within each orbit, different surjections have different
     derivative distributions. This is because the Stab(111)
     action permutes vertices but the mask directions are fixed.

  2. ORBIT-AVERAGED derivative distribution distinguishes
     Shape A from Shape B:
     - Shape A (orbits 0,1,2): avg {0:2.0, 1:5.5, 2:5.5, 3:5.5, 4:5.5}
     - Shape B (orbits 3,4):   avg {0:4.0, 1:5.0, 2:5.0, 3:5.0, 4:5.0}
     Shape B has more zero derivatives (4 vs 2) — consistent
     with its larger fiber ({4,1,1,1,1} has more local degeneracy).

  3. Average derivative distribution does NOT distinguish
     the IC orbit from other Shape A orbits.
     All three Shape A orbits have identical averages.

  4. Weighted sensitivity W distribution:
     - Shape A orbits: {28:24, 32:48, 40:24} — avg 33.0
     - Shape B orbits: {28:12, 32:12} — avg 30.0
     The proportions scale with orbit size but the values
     are the same within each shape.

  5. The I Ching's SPECIFIC surjection has:
     - Derivative dist: {0: 4, 1: 4, 2: 6, 3: 6, 4: 4}
     - W = 32
     - This is the {0:4, 1:4, 2:6, 3:6, 4:4} type,
       one of 4 types in the IC orbit (24 surjections each).

  CONCLUSION: Derivative statistics separate fiber shapes but
  do NOT distinguish the IC orbit from other Shape A orbits.
  The IC orbit's uniqueness lies in its algebraic property:
  it is the ONLY orbit with FREE action (|orbit| = |G| = 96).
