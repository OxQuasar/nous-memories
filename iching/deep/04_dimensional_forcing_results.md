# Dimensional Forcing: Why 3 Lines?

## Task 1: Dimensional Forcing Theorem (n=1..8)

For Z₂ⁿ with complement=negation partitions into Z₅:
  2^(n-1) complement pairs distributed as (k₀, k₁, k₂)
  Fiber sizes: |Wood|=2k₀, |Fire|=|Water|=k₁, |Earth|=|Metal|=k₂
  Surjective: k₀≥1, k₁≥1, k₂≥1
  Singleton: min(k₁,k₂)=1

  n  2^(n-1)  surj shapes   w/ singl   w/o singl  ALL singl?  min fiber
---------------------------------------------------------------------------
  1        1            0          0           0          no          0
  2        2            0          0           0          no          0
  3        4            3          3           0         YES          1 ←←←
  4        8           21         11          10          no          1
  5       16          105         27          78          no          1
  6       32          465         59         406          no          1
  7       64         1953        123        1830          no          1
  8      128         8001        251        7750          no          1

Dimensions where ALL surjective partitions have singletons: [3]

★ CONFIRMED: n=3 is the UNIQUE dimension (among 1..8) where every
  surjective complement=negation partition Z₂ⁿ → Z₅ has singleton fibers.

### Why n=3 is forced

For n=3: 2^(n-1) = 4 complement pairs
  k₀ + k₁ + k₂ = 4, all ≥ 1
  Surjective partition shapes:
    (1,1,2) → fibers [2, 1, 1, 2, 2] singleton ✓
    (1,2,1) → fibers [2, 2, 2, 1, 1] singleton ✓
    (2,1,1) → fibers [4, 1, 1, 1, 1] singleton ✓

  With k₀+k₁+k₂=4 and all ≥ 1: max(k₁,k₂) ≤ 4-1-1 = 2
  If min(k₁,k₂) ≥ 2, then k₁+k₂ ≥ 4, so k₀ ≤ 0 → contradiction.
  Therefore min(k₁,k₂) = 1 always. QED.

### Why n=4 breaks

For n=4: 2^(n-1) = 8 complement pairs
  First partition without singletons:
    (1,2,5) → fibers [2, 2, 2, 5, 5]
    (1,3,4) → fibers [2, 3, 3, 4, 4]
    (1,4,3) → fibers [2, 4, 4, 3, 3]

  (k₁=2, k₂=2) is possible because k₀=8-2-2=4 ≥ 1. No singletons.

### Why n=2 fails (different reason)

For n=2: 2^(n-1) = 2 complement pairs
  k₀+k₁+k₂ = 2 with all ≥ 1 → impossible (need ≥ 3)
  NO surjective partitions exist. The Z₂/Z₅ bridge cannot be built.

### Boundary analysis

  n=1: 1 pair, cannot reach 3 destinations → no surjection
  n=2: 2 pairs, need 3 destinations → still impossible
  n=3: 4 pairs, 3 destinations → surjection forced to have singletons ★
  n=4: 8 pairs, 3 destinations → room for non-singleton partitions
  n≥4: always have non-singleton partitions (slack grows)

## Task 2: Concrete Assignments for n=3

Complement pairs in Z₂³: [(0, 7), (1, 6), (2, 5), (3, 4)]
  = {(000,111), (001,110), (010,101), (011,100)}

### Partition shapes and concrete assignment counts

       Shape                Fibers   Pair combos  Orientations   Total    Type
--------------------------------------------------------------------------------
  (1,1,2)       [2, 1, 1, 2, 2]            12             8      96     B/C
  (1,2,1)       [2, 2, 2, 1, 1]            12             8      96     B/C
  (2,1,1)       [4, 1, 1, 1, 1]            12             4      48       A

  Total concrete assignments: 240

### Direct enumeration verification

  Direct enumeration: 240 valid assignments
  Matches combinatorial count: True

  Fiber shape distribution:
    (2, 2, 2, 1, 1): 192 assignments (has singleton ✓)
    (4, 1, 1, 1, 1): 48 assignments (has singleton ✓)

  ALL assignments have singletons: True

### Traditional assignment identification

  Traditional assignment satisfies complement=negation: True
  Traditional fiber shape: (2, 2, 2, 1, 1)
  Traditional assignment is type: B/C (2,2,2,1,1)

  Traditional pair destinations:
    (000,111): 2,3 → Earth/Metal split (type 2)
    (001,110): both→Wood (type 0)
    (010,101): 4,1 → Fire/Water split (type 1)
    (011,100): 3,2 → Earth/Metal split (type 2)

## Task 3: n=4 Partition Space

n=4: 2^3 = 8 complement pairs
  Surjective partition shapes: 21
  With singletons: 11
  Without singletons: 10
  Fraction with singletons: 11/21 = 0.524

  All surjective shapes:
         Shape                     Fibers  Singleton?  Min fiber
  -----------------------------------------------------------------
  ( 1, 1, 6)            [6, 6, 2, 1, 1]           ✓          1
  ( 1, 2, 5)            [5, 5, 2, 2, 2]           ✗          2
  ( 1, 3, 4)            [4, 4, 3, 3, 2]           ✗          2
  ( 1, 4, 3)            [4, 4, 3, 3, 2]           ✗          2
  ( 1, 5, 2)            [5, 5, 2, 2, 2]           ✗          2
  ( 1, 6, 1)            [6, 6, 2, 1, 1]           ✓          1
  ( 2, 1, 5)            [5, 5, 4, 1, 1]           ✓          1
  ( 2, 2, 4)            [4, 4, 4, 2, 2]           ✗          2
  ( 2, 3, 3)            [4, 3, 3, 3, 3]           ✗          3
  ( 2, 4, 2)            [4, 4, 4, 2, 2]           ✗          2
  ( 2, 5, 1)            [5, 5, 4, 1, 1]           ✓          1
  ( 3, 1, 4)            [6, 4, 4, 1, 1]           ✓          1
  ( 3, 2, 3)            [6, 3, 3, 2, 2]           ✗          2
  ( 3, 3, 2)            [6, 3, 3, 2, 2]           ✗          2
  ( 3, 4, 1)            [6, 4, 4, 1, 1]           ✓          1
  ( 4, 1, 3)            [8, 3, 3, 1, 1]           ✓          1
  ( 4, 2, 2)            [8, 2, 2, 2, 2]           ✗          2
  ( 4, 3, 1)            [8, 3, 3, 1, 1]           ✓          1
  ( 5, 1, 2)           [10, 2, 2, 1, 1]           ✓          1
  ( 5, 2, 1)           [10, 2, 2, 1, 1]           ✓          1
  ( 6, 1, 1)           [12, 1, 1, 1, 1]           ✓          1

  Concrete assignment counts by shape:
    (1,1,6) [[6, 6, 2, 1, 1]]: C(8,1)×C(7,1) × 2^7 = 7168
    (1,2,5) [[5, 5, 2, 2, 2]]: C(8,1)×C(7,2) × 2^7 = 21504
    (1,3,4) [[4, 4, 3, 3, 2]]: C(8,1)×C(7,3) × 2^7 = 35840
    (1,4,3) [[4, 4, 3, 3, 2]]: C(8,1)×C(7,4) × 2^7 = 35840
    (1,5,2) [[5, 5, 2, 2, 2]]: C(8,1)×C(7,5) × 2^7 = 21504
    (1,6,1) [[6, 6, 2, 1, 1]]: C(8,1)×C(7,6) × 2^7 = 7168
    (2,1,5) [[5, 5, 4, 1, 1]]: C(8,2)×C(6,1) × 2^6 = 10752
    (2,2,4) [[4, 4, 4, 2, 2]]: C(8,2)×C(6,2) × 2^6 = 26880
    (2,3,3) [[4, 3, 3, 3, 3]]: C(8,2)×C(6,3) × 2^6 = 35840
    (2,4,2) [[4, 4, 4, 2, 2]]: C(8,2)×C(6,4) × 2^6 = 26880
    (2,5,1) [[5, 5, 4, 1, 1]]: C(8,2)×C(6,5) × 2^6 = 10752
    (3,1,4) [[6, 4, 4, 1, 1]]: C(8,3)×C(5,1) × 2^5 = 8960
    (3,2,3) [[6, 3, 3, 2, 2]]: C(8,3)×C(5,2) × 2^5 = 17920
    (3,3,2) [[6, 3, 3, 2, 2]]: C(8,3)×C(5,3) × 2^5 = 17920
    (3,4,1) [[6, 4, 4, 1, 1]]: C(8,3)×C(5,4) × 2^5 = 8960
    (4,1,3) [[8, 3, 3, 1, 1]]: C(8,4)×C(4,1) × 2^4 = 4480
    (4,2,2) [[8, 2, 2, 2, 2]]: C(8,4)×C(4,2) × 2^4 = 6720
    (4,3,1) [[8, 3, 3, 1, 1]]: C(8,4)×C(4,3) × 2^4 = 4480
    (5,1,2) [[10, 2, 2, 1, 1]]: C(8,5)×C(3,1) × 2^3 = 1344
    (5,2,1) [[10, 2, 2, 1, 1]]: C(8,5)×C(3,2) × 2^3 = 1344
    (6,1,1) [[12, 1, 1, 1, 1]]: C(8,6)×C(2,1) × 2^2 = 224
  Total concrete assignments for n=4: 312480

  Minimum fiber size across all surjective partitions: 1

## Task 4: Theorem Statement

**Theorem (Dimensional Forcing).** Let f: Z₂ⁿ → Z₅ be a surjection
satisfying f(x̄) = -f(x) mod 5 for all x ∈ Z₂ⁿ (where x̄ = x ⊕ 1ⁿ).
Then:
  (a) Such f exists if and only if n ≥ 3.
  (b) For n = 3, every such f has at least two singleton fibers.
  (c) For n ≥ 4, there exist such f with no singleton fibers.

*Proof.*
  There are 2^(n-1) complement pairs. Each pair maps to one of 3
  destination types: self-conjugate (0), or one of two split types (1,2).
  Let (k₀,k₁,k₂) be the counts. Surjectivity requires k₀,k₁,k₂ ≥ 1.

  (a) k₀+k₁+k₂ = 2^(n-1) ≥ 3 iff n ≥ 3. For n≤2, 2^(n-1) ≤ 2 < 3.

  (b) For n=3: k₀+k₁+k₂ = 4 with all ≥ 1.
      Suppose min(k₁,k₂) ≥ 2. Then k₁+k₂ ≥ 4, so k₀ ≤ 0. Contradiction.
      Therefore min(k₁,k₂) = 1, giving fiber size 1 (a singleton).
      The paired element with k=1 produces two singleton fibers (at
      positions i and 5-i in Z₅).

  (c) For n=4: (k₀,k₁,k₂) = (4,2,2) gives all fibers ≥ 2. □

**Corollary.** The Z₂/Z₅ bridge — the existence of an injective point
in the quotient map f: Z₂ⁿ → Z₅ with complement=negation — is
structurally guaranteed if and only if n = 3.

**Interpretation.** The trigram having 3 lines is not a design choice
but a structural necessity: it is the unique dimension where the
Z₂-Z₅ bridge is forced to create singleton fibers, which are the
injection points that make the quotient map invertible on two fibers.

## Task 5: Hexagram Dimension (互 Convergence)

For 2n-line figures (Z₂^{2n}), the 互 analog extracts inner lines
and repackages them. We test convergence for n=2,3,4.

### n=3: Standard 互 (6-line hexagrams)

  Total hexagrams: 64
  Fixed points of 互: 2
    Values: [0, 63]
    As upper/lower trigrams:
      000000 = (000/000)
      111111 = (111/111)

  Convergence depth distribution (steps to reach cycle):
    depth 0: 4 hexagrams
    depth 1: 12 hexagrams
    depth 2: 48 hexagrams

  Maximum convergence depth: 2
  Cycle length distribution:
    cycle length 1: 32 hexagrams
    cycle length 2: 32 hexagrams

### n=2: 4-line figures (Z₂⁴)

  For 4-line figures, 互 extracts inner 2 lines (lines 2,3)
  and must form a new 4-line figure. Following the pattern:
    lower 'digram' = lines 2,3 → new lines 1,2
    upper 'digram' = lines 2,3 → new lines 3,4
  This means 互(h) = inner | (inner << 2) where inner = (h>>1) & 0b11

  Total 4-line figures: 16
  Fixed points: 2 → [0, 15]
    As binary: ['0000', '1111']
  Convergence depths: {0: 4, 1: 12}
  Max depth: 1

### n=4: 8-line figures (Z₂⁸)

  For 8-line figures, 互 extracts inner 6 lines (lines 2-7)
  Lower 4-gram = lines 2,3,4,5 → bits 0-3
  Upper 4-gram = lines 3,4,5,6 → bits 4-7
  But this gives an 8-line figure only if we treat
  lines 2-5 as lower half and lines 3-6 as upper half.

  Total 8-line figures: 256
  Fixed points: 2
  Convergence depths: {0: 8, 1: 56, 2: 192}
  Max depth: 2
  Cycle lengths: {1: 64, 3: 192}

### Comparison: 互 convergence by dimension

  n  2n lines   |Z₂^{2n}|  Fixed pts  Max depth       Cycle lens
-----------------------------------------------------------------
  2         4          16          2          1     {1: 8, 2: 8}
  3         6          64          2          2   {1: 32, 2: 32}
  4         8         256          2          2  {1: 64, 3: 192}

### Is n=3 distinguished for 互 convergence?

  n=2 (4 lines): all converge to fixed points? False
  n=3 (6 lines): all converge to fixed points? False
  n=4 (8 lines): all converge to fixed points? False


  Max cycle length by dimension:
    n=2: max cycle = 2 → all cycles divide 2: ✓
    n=3: max cycle = 2 → all cycles divide 2: ✓
    n=4: max cycle = 3 → all cycles divide 2: ✗

  ★ n=3 is the largest n where 互² is the identity on eventual cycles.
    At n=4, 互 introduces 3-cycles — a qualitative change in dynamics.

  n=2: 2/16 = 0.125 fixed point ratio
  n=3: 2/64 = 0.031 fixed point ratio
  n=4: 2/256 = 0.008 fixed point ratio

## Summary

### Dimensional forcing: n=3 is uniquely forced
  • n ≤ 2: No surjective complement=negation partition exists
  • n = 3: Every surjection has singletons (pigeonhole on 4 pairs)
  • n ≥ 4: Non-singleton surjections exist (enough slack)
  → The 3-line trigram is the unique bridge dimension

### Concrete count for n=3
  Total valid assignments: 240
  Fiber shapes: {(4, 1, 1, 1, 1): 48, (2, 2, 2, 1, 1): 192}
  ALL have singletons: True

### 互 convergence
  n=2 (4 lines): max cycle 2, max depth 1, 2 fixed pts
  n=3 (6 lines): max cycle 2, max depth 2, 2 fixed pts
  n=4 (8 lines): max cycle 3, max depth 2, 2 fixed pts
  → n=4 introduces 3-cycles: 互² ≠ identity on eventual cycle
