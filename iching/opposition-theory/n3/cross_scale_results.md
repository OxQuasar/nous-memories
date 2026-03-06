======================================================================
n=3 CROSS-SCALE ANALYSIS
======================================================================

## 1. Z₂² Orbit Structure at n=3

  All 8 states:
    000: w=0, rev=000, comp=111, cr=111
    001: w=1, rev=100, comp=110, cr=011
    010: w=1, rev=010, comp=101, cr=101
    011: w=2, rev=110, comp=100, cr=001
    100: w=1, rev=001, comp=011, cr=110
    101: w=2, rev=101, comp=010, cr=010
    110: w=2, rev=011, comp=001, cr=100
    111: w=3, rev=111, comp=000, cr=000

  Orbits under Z₂²:
    O0 (size 2): ['000', '111']  weights: [0, 3]
    O1 (size 4): ['001', '011', '100', '110']  weights: [1, 2, 1, 2]
    O2 (size 2): ['010', '101']  weights: [1, 2]

  Orbit sizes: {2: 2, 4: 1}

  Palindromes (rev-fixed): 4 — ['000', '010', '101', '111']
  Comp∘rev-fixed: 0 — []
  Complement-fixed: 0 — []

  Size-2 orbits: 2
    ['000', '111']  palindrome=True  cr-fixed=False
    ['010', '101']  palindrome=True  cr-fixed=False

  Size-4 orbits: 1
    ['001', '011', '100', '110']

## 2. Can Reversal Produce a Valid Pairing?

  Reversal has 4 fixed points (palindromes).
  Since palindromes map to themselves under reversal,
  reversal alone CANNOT produce a complete pairing.

  Comp∘rev has 0 fixed points.
  No fixed points — comp∘rev can produce a complete pairing.

  Complement has 0 fixed points.
  Complement CAN produce a complete pairing.

## 3. All 105 Pairings Enumerated

  Total pairings: 105 (expected 105)

## 4. Equivariant Pairings

  Equivariant under complement: 25
  Equivariant under reversal: 9
  Equivariant under comp∘rev: 25
  Fully Z₂²-equivariant (all three): 9

  All fully equivariant pairings:
    [000↔010, 001↔011, 100↔110, 101↔111]
      S=4, D=0.0000, total_Δw=4, WC=+1.0000
      masks: {'010': 4}
    [000↔010, 001↔100, 011↔110, 101↔111]
      S=6, D=1.0000, total_Δw=2, WC=+0.8182
      masks: {'010': 2, '101': 2}
    [000↔010, 001↔110, 011↔100, 101↔111]
      S=8, D=1.0000, total_Δw=4, WC=+0.4545
      masks: {'010': 2, '111': 2}
    [000↔101, 001↔011, 010↔111, 100↔110]
      S=6, D=1.0000, total_Δw=6, WC=+0.3333
      masks: {'101': 2, '010': 2}
    [000↔101, 001↔100, 010↔111, 011↔110]
      S=8, D=0.0000, total_Δw=4, WC=+0.0000
      masks: {'101': 4}
    [000↔101, 001↔110, 010↔111, 011↔100]
      S=10, D=1.0000, total_Δw=6, WC=-0.5000
      masks: {'101': 2, '111': 2}
    [000↔111, 001↔011, 010↔101, 100↔110]
      S=8, D=1.0000, total_Δw=6, WC=-1.0000
      masks: {'111': 2, '010': 2}
    [000↔111, 001↔100, 010↔101, 011↔110]
      S=10, D=1.0000, total_Δw=4, WC=-0.5000
      masks: {'111': 2, '101': 2}
    [000↔111, 001↔110, 010↔101, 011↔100]
      S=12, D=0.0000, total_Δw=6, WC=-1.0000
      masks: {'111': 4}

## 5. Weight Preservation Analysis

  Total |Δw| across all pairings:
    Range: [2, 6]
    Δw=2: 9 pairings
    Δw=4: 72 pairings
    Δw=6: 24 pairings

  Pairings with total Δw = 0 (perfect weight preservation): 0
  NO weight-preserving pairing exists at n=3!

  Weight distribution: {0: 1, 1: 3, 2: 3, 3: 1}
  For Δw=0, each pair must have equal weight.
  w=0: 1 state (odd count — cannot pair among themselves)
  w=3: 1 state (odd count — cannot pair among themselves)
  Since w=0 and w=3 each have 1 state, they MUST pair with
  different-weight partners. Perfect weight preservation is impossible.

  Minimum Δw pairings (total_Δw = 2): 9
    [000(w=0)↔001(w=1), 010(w=1)↔100(w=1), 011(w=2)↔101(w=2), 110(w=2)↔111(w=3)]
      S=6, D=1.0000, eq_all=False
    [000(w=0)↔001(w=1), 010(w=1)↔100(w=1), 011(w=2)↔110(w=2), 101(w=2)↔111(w=3)]
      S=6, D=2.0000, eq_all=False
    [000(w=0)↔001(w=1), 010(w=1)↔100(w=1), 011(w=2)↔111(w=3), 101(w=2)↔110(w=2)]
      S=6, D=2.0000, eq_all=False
    [000(w=0)↔010(w=1), 001(w=1)↔100(w=1), 011(w=2)↔101(w=2), 110(w=2)↔111(w=3)]
      S=6, D=2.0000, eq_all=False
    [000(w=0)↔010(w=1), 001(w=1)↔100(w=1), 011(w=2)↔110(w=2), 101(w=2)↔111(w=3)]
      S=6, D=1.0000, eq_all=True
    [000(w=0)↔010(w=1), 001(w=1)↔100(w=1), 011(w=2)↔111(w=3), 101(w=2)↔110(w=2)]
      S=6, D=2.0000, eq_all=False
    [000(w=0)↔100(w=1), 001(w=1)↔010(w=1), 011(w=2)↔101(w=2), 110(w=2)↔111(w=3)]
      S=6, D=2.0000, eq_all=False
    [000(w=0)↔100(w=1), 001(w=1)↔010(w=1), 011(w=2)↔110(w=2), 101(w=2)↔111(w=3)]
      S=6, D=2.0000, eq_all=False
    [000(w=0)↔100(w=1), 001(w=1)↔010(w=1), 011(w=2)↔111(w=3), 101(w=2)↔110(w=2)]
      S=6, D=1.0000, eq_all=False

## 6. Equivariance + Weight Preservation

  Min total_Δw among equivariant pairings: 2
  Equivariant pairings achieving min Δw: 1
    [000↔010, 001↔100, 011↔110, 101↔111]
      S=6, D=1.0000, total_Δw=2

  Complement pairing is fully equivariant: True
    S=12, total_Δw=6

## 7. Cross-Scale Consistency Check

  THE UNIFIED PRINCIPLE:
    Maximize weight preservation, subject to equivariance.
    Within that, maximize strength.

  AT n=6:
    - 12 size-4 orbits: reversal (weight-preserving) is available → use it
    - 8 size-2 orbits: forced to complement (weight disruption unavoidable
      for palindrome orbits, zero for cr-fixed orbits)
    - Among all-reversal: KW uniquely maximizes S
    → KW is the unique solution

  AT n=3:
    - NO weight-preserving pairing exists at all
      (w=0 and w=3 have odd counts → forced cross-weight pairing)
    - Weight preservation is vacuously maximized by any pairing
    - Among equivariant pairings: 9 exist
    - Min Δw among equivariant: 2
    - Max S at min Δw among equivariant: 6
    - Number achieving both: 1
    - Is complement the unique such pairing? False

## 8. Structural Comparison Across Scales

  Scale decomposition:
  
  n=3: 4 orbits (2 size-2, 0 size-4)
    - ALL orbits are size-2 (palindrome or cr-fixed)
    - No size-4 orbits exist → no reversal/comp/cr choice at all
    - Every orbit is forced to self-match (complement)
    - The principle "use reversal for size-4 orbits" is vacuously satisfied
    
  n=4: 6 orbits (4 size-2, 2 size-4)
    - 2 size-4 orbits admit the rev/comp/cr choice
    - KW-style: reversal for both → S=24 (unique S-max in all-rev)
    
  n=6: 20 orbits (8 size-2, 12 size-4)  
    - 12 size-4 orbits admit the rev/comp/cr choice
    - KW: reversal for all 12 → S=120 (unique S-max in all-rev)

  n=3: 3 orbits (2 size-2, 1 size-4), 4 palindromes, 0 cr-fixed

  n=4: 6 orbits (4 size-2, 2 size-4), 4 palindromes, 4 cr-fixed

  n=5: 10 orbits (4 size-2, 6 size-4), 8 palindromes, 0 cr-fixed

  n=6: 20 orbits (8 size-2, 12 size-4), 8 palindromes, 8 cr-fixed

  PATTERN: At odd n (3, 5), there are NO comp∘rev-fixed points
  (because comp_rev(x)=x means rev(x)=comp(x), requiring w(x)=N-w(x),
  so w=N/2 which is impossible at odd N).
  
  At even n (4, 6), comp∘rev-fixed points exist (w = N/2 is achievable).
  
  At n=3: 4 palindromes, 0 cr-fixed → 2 palindrome orbits, 0 cr-fixed orbits.
  All 4 remaining states form 1 size-4 orbit.
  Wait — let me recount...

  n=3 recount:
    Palindromes: ['000', '010', '101', '111'] (4 states)
    CR-fixed: [] (0 states)
    Size-2 orbits: 2
    Size-4 orbits: 1
      ['001', '011', '100', '110']
        comp: 001↔110, 011↔100  S=6, Δw=[1,1], masks=[111,111]
        rev: 001↔100, 011↔110  S=4, Δw=[0,0], masks=[101,101]
        cr: 001↔011, 100↔110  S=2, Δw=[1,1], masks=[010,010]

======================================================================
SUMMARY
======================================================================

  1. n=3 has 3 orbits: 2 size-2, 1 size-4
  2. 4 palindromes, 0 cr-fixed points
  3. Perfect weight preservation is impossible at n=3
     (odd weight classes w=0,w=3 have 1 state each)
  4. Fully equivariant pairings: 9
  5. Complement is one of the fully equivariant pairings

  6. n=3 HAS a size-4 orbit: the non-palindromic states
     Within this orbit, reversal gives Δw=0 (weight-preserving)
     Complement gives Δw>0
     The principle 'use reversal for size-4 orbits' IS applicable
     But the size-2 orbits force complement (which contributes Δw>0)

     'KW-style' at n=3 (rev for size-4, comp for size-2):
       000↔111  Δw=3
       001↔100  Δw=0
       010↔101  Δw=1
       011↔110  Δw=0
       S=10, D=1.0000, total_Δw=4
       Equivariant: True
       Equivariant under comp: True
       Equivariant under rev: True
       Equivariant under cr: True

     Complement pairing at n=3:
       000↔111  Δw=3
       001↔110  Δw=1
       010↔101  Δw=1
       011↔100  Δw=1
       S=12, D=0.0000, total_Δw=6
       Equivariant: True

     THE CROSS-SCALE TEST:
     At n=3, the 'KW-style' (rev for size-4, comp for size-2)
     and the 'complement' (comp for everything) are DIFFERENT pairings.
     Tradition chose COMPLEMENT, not KW-style.
     Is complement consistent with the weight-preservation principle?

     KW-style total Δw: 4
     Complement total Δw: 6

     KW-style has LESS weight disruption than complement!
     But tradition chose complement anyway.
     This means the n=3 tradition does NOT follow the weight-preservation principle.
     However: is KW-style equivariant?
