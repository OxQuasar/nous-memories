======================================================================
TASK A: S↔D ANTI-CORRELATION UNDER EQUIVARIANCE
======================================================================

## A1. Strength Identity: S_rev + S_cr = S_comp

                                               Orbit S_comp S_rev S_cr  Sum  Check
  -------------------------------------------------- ------ ----- ---- ---- ------
            ['000001', '011111', '100000', '111110']     12     4    8   12      ✓
            ['000010', '010000', '101111', '111101']     12     4    8   12      ✓
            ['000011', '001111', '110000', '111100']     12     8    4   12      ✓
            ['000100', '001000', '110111', '111011']     12     4    8   12      ✓
            ['000101', '010111', '101000', '111010']     12     8    4   12      ✓
            ['000110', '011000', '100111', '111001']     12     8    4   12      ✓
            ['001001', '011011', '100100', '110110']     12     8    4   12      ✓
            ['001010', '010100', '101011', '110101']     12     8    4   12      ✓
            ['001101', '010011', '101100', '110010']     12     4    8   12      ✓
            ['001110', '011100', '100011', '110001']     12     4    8   12      ✓
            ['010001', '011101', '100010', '101110']     12     8    4   12      ✓
            ['010110', '011010', '100101', '101001']     12     4    8   12      ✓

  Identity holds for all 12 orbits: True
  S_comp = 12 for all orbits (= 2×N = 2×6 = 12)

  Proof: Let m = x ⊕ rev(x) (the reversal mask, a palindrome).
    S_rev = 2 × popcount(m)
    mask_cr = x ⊕ comp_rev(x) = x ⊕ comp(rev(x)) = (x ⊕ rev(x)) ⊕ 111111 = comp(m)
    S_cr = 2 × popcount(comp(m)) = 2 × (N − popcount(m))
    S_rev + S_cr = 2N = S_comp  ∎

## A2. Mask Structure Per Orbit

  Each intra-orbit choice produces a deterministic mask (2 copies).
  comp: always 111111
  rev: x ⊕ rev(x) = palindromic mask (the mirror-pair signature)
  cr: comp(rev mask) = complementary palindromic mask

  Orbit mask_comp mask_rev  mask_cr   rev is comp(cr)?
     0   111111   100001   011110                  ✓
     1   111111   010010   101101                  ✓
     2   111111   110011   001100                  ✓
     3   111111   001100   110011                  ✓
     4   111111   101101   010010                  ✓
     5   111111   011110   100001                  ✓
     6   111111   101101   010010                  ✓
     7   111111   011110   100001                  ✓
     8   111111   100001   011110                  ✓
     9   111111   010010   101101                  ✓
    10   111111   110011   001100                  ✓
    11   111111   001100   110011                  ✓

  Observation: mask_rev and mask_cr are always complementary.
  The 6 palindromic masks form 3 complementary pairs:
    001100 ↔ 110011
    010010 ↔ 101101
    011110 ↔ 100001

## A3. Why Equivariance Creates S↔D Anti-Correlation

  In the FULL pairing space:
    - S depends on Hamming weights of XOR masks
    - D depends on entropy of mask distribution (multiplicity)
    - These are orthogonal: knowing S tells you nothing about D (r = 0)

  Under EQUIVARIANCE:
    - Each size-4 orbit contributes exactly 2 pairs
    - The choice is from {comp, rev, cr}
    - comp: S=12 (max), mask=111111 (shared across all orbits)
    - rev/cr: S<12, mask=palindromic (distinct per orbit)

  THE COUPLING: choosing comp for an orbit contributes max S
  but adds to the 111111 pile (reducing diversity).
  Choosing rev/cr contributes less S but a distinct mask (increasing diversity).
  Since mask identity is tied to the operation, S and mask-type are coupled per orbit.
  Summing over orbits: more comp choices → higher S, lower D.
  This creates the negative correlation r(S,D) ≈ −0.33.

## A4. Analytic Structure

  For the 12 size-4 orbits with intra-orbit matching only:
  Let c_i ∈ {comp, rev, cr} be the choice for orbit i.
  S_big = Σᵢ S(c_i)
  mask_counts = multiset of masks from all choices
  D = H(mask_counts / 32)

  S(comp) = 12 always, S(rev) and S(cr) vary by orbit.
  Masks:
    comp → 111111 (same for all orbits)
    rev → orbit-specific palindrome (6 distinct values)
    cr → complement of the rev palindrome (6 distinct values)

  Rev masks by orbit:
    001100: orbits [3, 11] (count=2)
    010010: orbits [1, 9] (count=2)
    011110: orbits [5, 7] (count=2)
    100001: orbits [0, 8] (count=2)
    101101: orbits [4, 6] (count=2)
    110011: orbits [2, 10] (count=2)

  Each palindromic mask appears in exactly 2 orbits for rev,
  and 2 orbits for cr (its complement mask).
  Total: 6 distinct masks × 2 orbits = 12 orbit-mask slots = 12 orbits ✓

  Per-orbit S-vs-mask contribution:
  Choice  S contribution                    Mask effect
    comp        12 (max)          adds 2 to 111111 pile
     rev          4 or 8  adds 2 to distinct palindrome
      cr          8 or 4  adds 2 to distinct palindrome

## A5. Verification from Sample

  r(S, D) from 500K equivariant sample: -0.334287

  S-conditional D (from sample):
    S= 68: n=   163, D_mean=3.3076, D_std=0.2787
    S= 72: n=   528, D_mean=3.3336, D_std=0.2880
    S= 76: n=  1390, D_mean=3.3878, D_std=0.2941
    S= 80: n=  3188, D_mean=3.4040, D_std=0.2883
    S= 84: n=  6716, D_mean=3.4156, D_std=0.2870
    S= 88: n= 12413, D_mean=3.4274, D_std=0.2816
    S= 92: n= 20708, D_mean=3.4318, D_std=0.2764
    S= 96: n= 31207, D_mean=3.4260, D_std=0.2731
    S=100: n= 42448, D_mean=3.4175, D_std=0.2725
    S=104: n= 52439, D_mean=3.4004, D_std=0.2724
    S=108: n= 59590, D_mean=3.3820, D_std=0.2720
    S=112: n= 61100, D_mean=3.3530, D_std=0.2731
    S=116: n= 57127, D_mean=3.3189, D_std=0.2774
    S=120: n= 49234, D_mean=3.2789, D_std=0.2807
    S=124: n= 37956, D_mean=3.2288, D_std=0.2864
    S=128: n= 26858, D_mean=3.1724, D_std=0.2943
    S=132: n= 17399, D_mean=3.1134, D_std=0.2989
    S=136: n= 10079, D_mean=3.0336, D_std=0.3050
    S=140: n=  5348, D_mean=2.9569, D_std=0.3054
    S=144: n=  2378, D_mean=2.8550, D_std=0.3176
    S=148: n=  1063, D_mean=2.7550, D_std=0.3237
    S=152: n=   424, D_mean=2.6486, D_std=0.3399
    S=156: n=   127, D_mean=2.4956, D_std=0.3227

## A6. Why r(S,D) = 0 in the Full Space

  In the full space of pairings (no equivariance constraint):
  - Any state can pair with any other state
  - The mask a⊕b can be ANY nonzero value (63 possible)
  - The Hamming weight of the mask (determining S contribution)
    and the mask identity (determining D contribution)
    are independently choosable across different pairs
  
  Under equivariance:
  - Each orbit's mask is FIXED by the operation choice
  - The operation determines BOTH the mask identity AND its weight
  - Specifically: comp always gives mask=111111 (weight 6)
    while rev/cr give orbit-specific masks (weight < 6)
  
  This is the coupling: in the full space, two pairs can have
  the same Hamming distance but different masks (e.g., 110100 and 101010
  both have distance 3). Under equivariance, the mask is deterministic
  given the orbit and operation — no freedom to decouple S from mask identity.
  
  The equivariance constraint BINDS the per-orbit S contribution to
  the per-orbit mask contribution, creating the anti-correlation.

======================================================================
TASK B: WEIGHT PRESERVATION EQUIVALENCE
======================================================================

## B1. Weight Change Per Operation

  Algebraic prediction:
    rev: w(rev(x)) = w(x) → Δw = 0 always
    comp: w(comp(x)) = N − w(x) → Δw = |2w(x) − N|
    cr: w(comp_rev(x)) = N − w(x) → Δw = |2w(x) − N|

  Orbit        x w(x)  Δw_comp  Δw_rev  Δw_cr   rev=0? comp=cr?
     0   000001    1   [4, 4]  [0, 0] [4, 4]        ✓        ✓
     1   000010    1   [4, 4]  [0, 0] [4, 4]        ✓        ✓
     2   000011    2   [2, 2]  [0, 0] [2, 2]        ✓        ✓
     3   000100    1   [4, 4]  [0, 0] [4, 4]        ✓        ✓
     4   000101    2   [2, 2]  [0, 0] [2, 2]        ✓        ✓
     5   000110    2   [2, 2]  [0, 0] [2, 2]        ✓        ✓
     6   001001    2   [2, 2]  [0, 0] [2, 2]        ✓        ✓
     7   001010    2   [2, 2]  [0, 0] [2, 2]        ✓        ✓
     8   001101    3   [0, 0]  [0, 0] [0, 0]        ✓        ✓
     9   001110    3   [0, 0]  [0, 0] [0, 0]        ✓        ✓
    10   010001    2   [2, 2]  [0, 0] [2, 2]        ✓        ✓
    11   010110    3   [0, 0]  [0, 0] [0, 0]        ✓        ✓

  Reversal preserves weight for ALL orbits: True
  Comp and CR have identical Δw for ALL orbits: True

  Conclusion: REVERSAL IS THE UNIQUE WEIGHT-PRESERVING INTRA-ORBIT OPERATION.

## B2. Size-2 Orbit Weight Changes (Forced Pairings)

  Palindrome orbits (self-match = complement):
    000000 ↔ 111111: w=0,6, Δw=6
    001100 ↔ 110011: w=2,4, Δw=2
    010010 ↔ 101101: w=2,4, Δw=2
    011110 ↔ 100001: w=4,2, Δw=2
    Total Δw from pal: 12

  Comp-rev-fixed orbits (self-match = complement):
    000111 ↔ 111000: w=3,3, Δw=0
    001011 ↔ 110100: w=3,3, Δw=0
    010101 ↔ 101010: w=3,3, Δw=0
    011001 ↔ 100110: w=3,3, Δw=0
    Total Δw from cr-fixed: 0

  Size-2 orbits are FORCED to use complement.
  For palindrome orbits: Δw = |2w(p) − N| (nonzero unless w = N/2)
  For cr-fixed orbits: w(x) + w(comp(x)) = N, but x and comp(x)
    are the two elements. Here comp_rev(x)=x means rev(x)=comp(x),
    so w(rev(x))=w(x) and w(comp(x))=N−w(x).
    But wait: cr-fixed states have comp_rev(x)=x, meaning the orbit
    is {x, comp(x)} where rev(x) = comp(x).
    So w(x) = w(rev(x)) = w(comp(x)) = N − w(x) → w(x) = N/2.
    ALL cr-fixed states have weight N/2 = 3. Δw = 0 for cr-fixed orbits!

  Verification: True

## B3. The Lexicographic Characterization

  THEOREM: Among Z₂²-equivariant pairings of n=6 states:
  
  (1) Reversal is the UNIQUE weight-preserving intra-orbit operation
      for size-4 orbits (complement and comp-rev both break weight).
      
  (2) Size-2 orbits are forced to use complement (no alternative).
      Palindrome size-2 orbits have Δw > 0 (unavoidable).
      CR-fixed size-2 orbits have Δw = 0 (all states have weight N/2).
      
  (3) "Maximize weight preservation" = "use reversal for all size-4 orbits"
      = the all-reversal subfamily (625 pairings).
      
  (4) Within the all-reversal subfamily, KW is the UNIQUE strength-maximizer
      (S = 120, achieved only by all-self-match for size-2 orbits).
      
  Therefore:
  
      KW = argmax S  subject to  max weight preservation  subject to  Z₂²-equivariance
      
  Equivalently, KW is the unique solution to the lexicographic optimization:
      
      FIRST: maximize weight preservation (reversal for all size-4 orbits)
      THEN: maximize strength (self-match for all size-2 orbits)

## B4. KW Uniqueness in All-Reversal Subfamily

  S_big_rev (fixed for all-rev): 72
  Max S_pal (all self-match): 24
  Max S_cr (all self-match): 24
  Max total S in all-rev: 120
  KW S: 120
  Match: True

  Why self-match maximizes S for size-2 orbits:
  Self-match pairs a↔comp(a) at distance N = 6.
  Any inter-orbit pair a↔c has distance < N (since a ≠ comp(c) in general).
  Complement is the UNIQUE distance-maximizing partner for any state.
  Therefore self-match uniquely maximizes S for size-2 orbits. ∎

## Summary

  ┌─────────────────────────────────────────────────────────────────────┐
  │ STRUCTURAL IDENTITY                                                │
  │                                                                    │
  │ For every size-4 orbit:  S_rev + S_cr = S_comp = 2N              │
  │                                                                    │
  │ Proof: mask_rev = m (palindrome), mask_cr = comp(m)               │
  │        S_rev = 2·popcount(m), S_cr = 2·(N − popcount(m))         │
  │        Sum = 2N = S_comp  ∎                                       │
  ├─────────────────────────────────────────────────────────────────────┤
  │ COUPLING MECHANISM                                                 │
  │                                                                    │
  │ comp → S=12, mask=111111 (shared)  → high S, low D               │
  │ rev  → S<12, mask=palindrome (distinct) → low S, high D          │
  │ cr   → S<12, mask=palindrome (distinct) → low S, high D          │
  │                                                                    │
  │ Under equivariance, S and mask-identity are coupled per orbit.    │
  │ This creates r(S,D) ≈ −0.33.                                     │
  │                                                                    │
  │ In the full space, S and mask-identity are independent → r = 0.   │
  ├─────────────────────────────────────────────────────────────────────┤
  │ WEIGHT PRESERVATION                                                │
  │                                                                    │
  │ Reversal is the UNIQUE weight-preserving operation among           │
  │ {comp, rev, cr} for size-4 orbits.                                │
  │                                                                    │
  │ "Max weight preservation" = "all-reversal" = 625 pairings         │
  ├─────────────────────────────────────────────────────────────────────┤
  │ KW CHARACTERIZATION                                                │
  │                                                                    │
  │ KW = argmax S,  subject to  max weight preservation,              │
  │                 subject to  Z₂²-equivariance                      │
  │                                                                    │
  │ Unique solution. Lexicographic: weight pres. >> strength.          │
  └─────────────────────────────────────────────────────────────────────┘
