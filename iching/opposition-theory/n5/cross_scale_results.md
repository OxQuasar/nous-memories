======================================================================
n=5 CROSS-SCALE ANALYSIS
======================================================================

## Fixed Points
  Palindromes (rev-fixed): 8
    00000  w=0  comp=11111
    00100  w=1  comp=11011
    01010  w=2  comp=10101
    01110  w=3  comp=10001
    10001  w=2  comp=01110
    10101  w=3  comp=01010
    11011  w=4  comp=00100
    11111  w=5  comp=00000
  Comp∘rev-fixed: 0
  Complement-fixed: 0

## Z₂² Orbit Structure
  Total orbits: 10
  Size distribution: {2: 4, 4: 6}
    O 0 (size 2): 00000, 11111  weights=[0, 5]
    O 1 (size 4): 00001, 01111, 10000, 11110  weights=[1, 4, 1, 4]
    O 2 (size 4): 00010, 01000, 10111, 11101  weights=[1, 1, 4, 4]
    O 3 (size 4): 00011, 00111, 11000, 11100  weights=[2, 3, 2, 3]
    O 4 (size 2): 00100, 11011  weights=[1, 4]
    O 5 (size 4): 00101, 01011, 10100, 11010  weights=[2, 3, 2, 3]
    O 6 (size 4): 00110, 01100, 10011, 11001  weights=[2, 2, 3, 3]
    O 7 (size 4): 01001, 01101, 10010, 10110  weights=[2, 3, 2, 3]
    O 8 (size 2): 01010, 10101  weights=[2, 3]
    O 9 (size 2): 01110, 10001  weights=[3, 2]

  Size-2 orbits: 4
  Size-4 orbits: 6

## KW-Style Pairing
  Rule: reversal for non-palindromes, complement for palindromes
    00000 ↔ 11111  XOR=11111 dist=5 Δw=5 [comp]
    00001 ↔ 10000  XOR=10001 dist=2 Δw=0 [rev]
    00010 ↔ 01000  XOR=01010 dist=2 Δw=0 [rev]
    00011 ↔ 11000  XOR=11011 dist=4 Δw=0 [rev]
    00100 ↔ 11011  XOR=11111 dist=5 Δw=3 [comp]
    00101 ↔ 10100  XOR=10001 dist=2 Δw=0 [rev]
    00110 ↔ 01100  XOR=01010 dist=2 Δw=0 [rev]
    00111 ↔ 11100  XOR=11011 dist=4 Δw=0 [rev]
    01001 ↔ 10010  XOR=11011 dist=4 Δw=0 [rev]
    01010 ↔ 10101  XOR=11111 dist=5 Δw=1 [comp]
    01011 ↔ 11010  XOR=10001 dist=2 Δw=0 [rev]
    01101 ↔ 10110  XOR=11011 dist=4 Δw=0 [rev]
    01110 ↔ 10001  XOR=11111 dist=5 Δw=1 [comp]
    01111 ↔ 11110  XOR=10001 dist=2 Δw=0 [rev]
    10011 ↔ 11001  XOR=01010 dist=2 Δw=0 [rev]
    10111 ↔ 11101  XOR=01010 dist=2 Δw=0 [rev]

  Measures:
    Strength:    52
    Diversity:   2.000000
    Weight Tilt: 0.6250
    Weight Corr: +0.157895
    Distinct masks: 4
      11111 (dist=5): ×4
      10001 (dist=2): ×4
      01010 (dist=2): ×4
      11011 (dist=4): ×4

  Complement S = 80 (maximum)
  KW-style S = 52 (65.0% of max)
  S cost of weight preservation: 35.0%

## Mirror-Pair Partition Group (Stabilizer in B_5)
  |B_5| = 2^5 × 5! = 3840
  Mirror pairs at n=5: {L1↔L5, L2↔L4}, center L3
  |Stab_B5(KW-style)| = 64 (0.1s)
  Expected structure: permute 2 mirror pairs (S₂) × swap within (Z₂²) × center (Z₂)
                    × flip mirror pair values (Z₂²) × flip center value (Z₂)
  Expected order: 2 × 4 × 2 × 4 × 2 = 128

## State Orbits Under Full Stabilizer
  Number of orbits: 3
  Size distribution: {8: 2, 16: 1}
    SO 0 (size  8): weights={0: 1, 1: 1, 2: 2, 3: 2, 4: 1, 5: 1}, states=[00000, 00100, 01010, 01110, 10001, 10101, 11011, 11111]
    SO 1 (size 16): weights={1: 4, 2: 4, 3: 4, 4: 4}, states=[00001, 00010, 00101, 00110, 01000, 01011, 01100, 01111...]
    SO 2 (size  8): weights={2: 4, 3: 4}, states=[00011, 00111, 01001, 01101, 10010, 10110, 11000, 11100]

## Equivariant Pairings Under Full Stabilizer
  Total pair-orbits: 29 (0.0s)
  Valid pair-orbits (no internal overlap): 13
    VPO 0:  4 pairs, S_contrib=  4, WT=1.00, masks=['00100']
    VPO 1:  4 pairs, S_contrib= 16, WT=2.00, masks=['11011']
    VPO 2:  4 pairs, S_contrib= 20, WT=2.50, masks=['11111']
    VPO 3:  8 pairs, S_contrib=  8, WT=1.00, masks=['00100']
    VPO 4:  8 pairs, S_contrib= 16, WT=2.00, masks=['01010', '10001']
    VPO 5:  8 pairs, S_contrib= 24, WT=2.00, masks=['01110', '10101']
    VPO 6:  8 pairs, S_contrib= 16, WT=0.00, masks=['01010', '10001']
    VPO 7:  8 pairs, S_contrib= 24, WT=1.00, masks=['01110', '10101']
    VPO 8:  8 pairs, S_contrib= 32, WT=2.00, masks=['11011']
    VPO 9:  8 pairs, S_contrib= 40, WT=2.00, masks=['11111']
    VPO10:  4 pairs, S_contrib=  4, WT=1.00, masks=['00100']
    VPO11:  4 pairs, S_contrib= 16, WT=0.00, masks=['11011']
    VPO12:  4 pairs, S_contrib= 20, WT=1.00, masks=['11111']

  Equivariant pairings: 63 (0.00s)

  Pairing 1:
    S=16, D=0.000000, WT=1.0000, WC=+1.000000
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 1

  Pairing 2:
    S=24, D=1.500000, WT=1.5000, WC=+0.818182
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 3

  Pairing 3:
    S=32, D=1.500000, WT=1.5000, WC=+0.454545
    Types: {'other': 4, 'cr': 12}
    Distinct masks: 3

  Pairing 4:
    S=24, D=1.500000, WT=0.5000, WC=+0.894737
    Types: {'other': 4, 'rev': 8, 'cr': 4}
    Distinct masks: 3

  Pairing 5:
    S=32, D=1.500000, WT=1.0000, WC=+0.684211
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 3

  Pairing 6:
    S=40, D=1.000000, WT=1.5000, WC=+0.250000
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 2

  Pairing 7:
    S=48, D=1.000000, WT=1.5000, WC=+0.000000
    Types: {'other': 4, 'comp': 8, 'cr': 4}
    Distinct masks: 2

  Pairing 8:
    S=28, D=0.811278, WT=0.7500, WC=+0.915493
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 2

  Pairing 9:
    S=36, D=2.000000, WT=1.2500, WC=+0.600000
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 4

  Pairing 10:
    S=44, D=2.000000, WT=1.2500, WC=+0.309091
    Types: {'other': 4, 'cr': 8, 'rev': 4}
    Distinct masks: 4

  Pairing 11:
    S=36, D=2.000000, WT=0.2500, WC=+0.924051
    Types: {'other': 4, 'rev': 12}
    Distinct masks: 4

  Pairing 12:
    S=44, D=2.000000, WT=0.7500, WC=+0.721519
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 4

  Pairing 13:
    S=52, D=0.811278, WT=1.2500, WC=+0.239437
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 2

  Pairing 14:
    S=60, D=1.500000, WT=1.2500, WC=+0.014085
    Types: {'other': 4, 'comp': 8, 'rev': 4}
    Distinct masks: 3

  Pairing 15:
    S=32, D=0.811278, WT=1.0000, WC=+0.802817
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 2

  Pairing 16:
    S=40, D=2.000000, WT=1.5000, WC=+0.454545
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 4

  Pairing 17:
    S=48, D=2.000000, WT=1.5000, WC=+0.163636
    Types: {'other': 4, 'cr': 8, 'comp': 4}
    Distinct masks: 4

  Pairing 18:
    S=40, D=2.000000, WT=0.5000, WC=+0.822785
    Types: {'other': 4, 'rev': 8, 'comp': 4}
    Distinct masks: 4

  Pairing 19:
    S=48, D=2.000000, WT=1.0000, WC=+0.620253
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 4

  Pairing 20:
    S=56, D=1.500000, WT=1.5000, WC=+0.126761
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 3

  Pairing 21:
    S=64, D=0.811278, WT=1.5000, WC=-0.098592
    Types: {'other': 4, 'comp': 12}
    Distinct masks: 2

  Pairing 22:
    S=28, D=0.811278, WT=1.2500, WC=+0.309091
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 2

  Pairing 23:
    S=36, D=2.000000, WT=1.7500, WC=-0.225806
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 4

  Pairing 24:
    S=44, D=2.000000, WT=1.7500, WC=-0.741935
    Types: {'other': 4, 'cr': 12}
    Distinct masks: 4

  Pairing 25:
    S=36, D=2.000000, WT=0.7500, WC=+0.239437
    Types: {'other': 4, 'rev': 8, 'cr': 4}
    Distinct masks: 4

  Pairing 26:
    S=44, D=2.000000, WT=1.2500, WC=+0.014085
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 4

  Pairing 27:
    S=52, D=0.811278, WT=1.7500, WC=-0.563636
    Types: {'other': 12, 'cr': 4}
    Distinct masks: 2

  Pairing 28:
    S=60, D=1.500000, WT=1.7500, WC=-0.854545
    Types: {'other': 4, 'comp': 8, 'cr': 4}
    Distinct masks: 3

  Pairing 29:
    S=40, D=1.000000, WT=1.0000, WC=+0.250000
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 2

  Pairing 30:
    S=48, D=1.500000, WT=1.5000, WC=-0.272727
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 3

  Pairing 31:
    S=56, D=1.500000, WT=1.5000, WC=-0.636364
    Types: {'other': 4, 'cr': 8, 'rev': 4}
    Distinct masks: 3

  Pairing 32:
    S=48, D=1.500000, WT=0.5000, WC=+0.263158
    Types: {'other': 4, 'rev': 12}
    Distinct masks: 3

  Pairing 33:
    S=56, D=1.500000, WT=1.0000, WC=+0.052632
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 3

  Pairing 34:
    S=64, D=0.000000, WT=1.5000, WC=-0.500000
    Types: {'other': 12, 'rev': 4}
    Distinct masks: 1

  Pairing 35:
    S=72, D=1.000000, WT=1.5000, WC=-0.750000
    Types: {'other': 4, 'comp': 8, 'rev': 4}
    Distinct masks: 2

  Pairing 36:
    S=44, D=1.500000, WT=1.2500, WC=+0.125000
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 3

  Pairing 37:
    S=52, D=2.000000, WT=1.7500, WC=-0.454545
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 4

  Pairing 38:
    S=60, D=2.000000, WT=1.7500, WC=-0.818182
    Types: {'other': 4, 'cr': 8, 'comp': 4}
    Distinct masks: 4

  Pairing 39:
    S=52, D=2.000000, WT=0.7500, WC=+0.157895
    Types: {'other': 4, 'rev': 8, 'comp': 4}
    Distinct masks: 4

  Pairing 40:
    S=60, D=2.000000, WT=1.2500, WC=-0.052632
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 4

  Pairing 41:
    S=68, D=0.811278, WT=1.7500, WC=-0.625000
    Types: {'other': 12, 'comp': 4}
    Distinct masks: 2

  Pairing 42:
    S=76, D=0.811278, WT=1.7500, WC=-0.875000
    Types: {'other': 4, 'comp': 12}
    Distinct masks: 2

  Pairing 43:
    S=32, D=0.811278, WT=1.3750, WC=+0.163636
    Types: {'comp': 4, 'other': 8, 'cr': 4}
    Distinct masks: 2

  Pairing 44:
    S=40, D=2.000000, WT=1.8750, WC=-0.483871
    Types: {'comp': 4, 'other': 8, 'cr': 4}
    Distinct masks: 4

  Pairing 45:
    S=48, D=2.000000, WT=1.8750, WC=-1.000000
    Types: {'comp': 4, 'cr': 12}
    Distinct masks: 4

  Pairing 46:
    S=40, D=2.000000, WT=0.8750, WC=+0.126761
    Types: {'comp': 4, 'rev': 8, 'cr': 4}
    Distinct masks: 4

  Pairing 47:
    S=48, D=2.000000, WT=1.3750, WC=-0.098592
    Types: {'comp': 4, 'other': 8, 'cr': 4}
    Distinct masks: 4

  Pairing 48:
    S=56, D=1.500000, WT=1.8750, WC=-0.709091
    Types: {'comp': 4, 'other': 8, 'cr': 4}
    Distinct masks: 3

  Pairing 49:
    S=64, D=0.811278, WT=1.8750, WC=-1.000000
    Types: {'comp': 12, 'cr': 4}
    Distinct masks: 2

  Pairing 50:
    S=44, D=1.500000, WT=1.1250, WC=+0.125000
    Types: {'comp': 4, 'other': 8, 'rev': 4}
    Distinct masks: 3

  Pairing 51:
    S=52, D=2.000000, WT=1.6250, WC=-0.454545
    Types: {'comp': 4, 'other': 8, 'rev': 4}
    Distinct masks: 4

  Pairing 52:
    S=60, D=2.000000, WT=1.6250, WC=-0.818182
    Types: {'comp': 4, 'cr': 8, 'rev': 4}
    Distinct masks: 4

  Pairing 53: ← KW-STYLE
    S=52, D=2.000000, WT=0.6250, WC=+0.157895
    Types: {'comp': 4, 'rev': 12}
    Distinct masks: 4

  Pairing 54:
    S=60, D=2.000000, WT=1.1250, WC=-0.052632
    Types: {'comp': 4, 'other': 8, 'rev': 4}
    Distinct masks: 4

  Pairing 55:
    S=68, D=0.811278, WT=1.6250, WC=-0.625000
    Types: {'comp': 4, 'other': 8, 'rev': 4}
    Distinct masks: 2

  Pairing 56:
    S=76, D=0.811278, WT=1.6250, WC=-0.875000
    Types: {'comp': 12, 'rev': 4}
    Distinct masks: 2

  Pairing 57:
    S=48, D=1.000000, WT=1.3750, WC=+0.000000
    Types: {'comp': 8, 'other': 8}
    Distinct masks: 2

  Pairing 58:
    S=56, D=1.500000, WT=1.8750, WC=-0.636364
    Types: {'comp': 8, 'other': 8}
    Distinct masks: 3

  Pairing 59:
    S=64, D=1.500000, WT=1.8750, WC=-1.000000
    Types: {'comp': 8, 'cr': 8}
    Distinct masks: 3

  Pairing 60:
    S=56, D=1.500000, WT=0.8750, WC=+0.052632
    Types: {'comp': 8, 'rev': 8}
    Distinct masks: 3

  Pairing 61:
    S=64, D=1.500000, WT=1.3750, WC=-0.157895
    Types: {'comp': 8, 'other': 8}
    Distinct masks: 3

  Pairing 62:
    S=72, D=1.000000, WT=1.8750, WC=-0.750000
    Types: {'comp': 8, 'other': 8}
    Distinct masks: 2

  Pairing 63: ← COMPLEMENT
    S=80, D=0.000000, WT=1.8750, WC=-1.000000
    Types: {'comp': 16}
    Distinct masks: 1

## Random Sample (50,000 pairings)
  Sampling time: 5.4s

  Sample statistics:
    Strength: mean=41.3088, std=4.2205, range=[26.0000, 58.0000]
    Diversity: mean=3.5349, std=0.1957, range=[2.4363, 4.0000]
    Weight Tilt: mean=1.2700, std=0.1884, range=[0.3750, 1.8750]
    Weight Corr: mean=0.2225, std=0.2489, range=[-0.7992, 0.9155]

  KW-style percentiles:
    Strength       : KW=   52.0000  percentile=99.66%
    Diversity      : KW=    2.0000  percentile=0.00%
    Weight Tilt    : KW=    0.6250  percentile=0.13%
    Weight Corr    : KW=    0.1579  percentile=37.78%

  Complement percentiles:
    Strength       : Comp=   80.0000  percentile=100.00%
    Diversity      : Comp=    0.0000  percentile=0.00%
    Weight Tilt    : Comp=    1.8750  percentile=100.00%

## Cross-Scale Comparison
    n States |S₂ orbs| |Stab| #Eq pairings KW S%max KW S%ile  KW WT
    3      8         3      ?            9    83.3%     ~99%   1.00
    4     16         6      ?          117      75%     ~75%      ?
    5     32        10     64           63    65.0%   99.66%   0.62
    6     64        20    384            9    62.5%   99.98%   0.38

======================================================================
SUMMARY
======================================================================

  n=5 orbit structure: 4 size-2 + 6 size-4 orbits
  Mirror-pair stabilizer: |Stab| = 64
  Equivariant pairings: 63
  KW-style: S=52, WT=0.6250, S-percentile=99.66%

  n=5 looks like n=6: KW-style is extreme → transition before n=6


============================================================
n=5 STABILIZER DIAGNOSTIC
============================================================

Mirror pairs: {L1↔L5} = {pos0↔pos4}, {L2↔L4} = {pos1↔pos3}
Center: L3 = pos2

Testing 6 expected generators:

  ✓ swap within pair 1: L1↔L5
    perm=(4, 1, 2, 3, 0), flip=00000, preserves KW: True
  ✓ swap within pair 2: L2↔L4
    perm=(0, 3, 2, 1, 4), flip=00000, preserves KW: True
  ✓ permute pairs: {L1,L5}↔{L2,L4}
    perm=(1, 0, 2, 4, 3), flip=00000, preserves KW: True
  ✓ flip pair 1 values: complement at {L1,L5}
    perm=(0, 1, 2, 3, 4), flip=10001, preserves KW: True
  ✓ flip pair 2 values: complement at {L2,L4}
    perm=(0, 1, 2, 3, 4), flip=01010, preserves KW: True
  ✓ flip center value: complement at L3
    perm=(0, 1, 2, 3, 4), flip=00100, preserves KW: True

  6/7 generators preserve KW

## Group Structure Explanation
  Permutation part: Z₂ ≀ S₂ = (Z₂)² ⋊ S₂ = order 8
    (swap within pair 1) × (swap within pair 2) × (permute pairs)
  Flip part: (Z₂)³ = order 8
    (flip pair 1) × (flip pair 2) × (flip center)
  Total: 8 × 8 = 64

  The initial expectation of 128 double-counted: there is no
  independent 'center permutation' generator — the center position
  is always fixed by any mirror-pair-preserving permutation.
  |Stab| = 64 is the correct expected order, matching computation.

  Group generated by all 7 generators: 64 elements
  Of these, 64 preserve KW
