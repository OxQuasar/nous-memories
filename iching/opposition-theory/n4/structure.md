======================================================================
n=4 STRUCTURAL ANALYSIS
======================================================================

## Z₂² Orbit Structure

Group: {id, complement, reversal, comp∘rev} acting on {0,...,15}
Total orbits: 6
Orbit sizes: {2: 4, 4: 2}

All orbits:
  Orbit  1 (size 2): 0000, 1111  weights: [0, 4]
  Orbit  2 (size 4): 0001, 0111, 1000, 1110  weights: [1, 3, 1, 3]
  Orbit  3 (size 4): 0010, 0100, 1011, 1101  weights: [1, 1, 3, 3]
  Orbit  4 (size 2): 0011, 1100  weights: [2, 2]
  Orbit  5 (size 2): 0101, 1010  weights: [2, 2]
  Orbit  6 (size 2): 0110, 1001  weights: [2, 2]

## Fixed Points

Palindromes (reversal-fixed): 4
  0000  (weight 0, complement = 1111)
  0110  (weight 2, complement = 1001)
  1001  (weight 2, complement = 0110)
  1111  (weight 4, complement = 0000)

Complement-fixed: 0
  (none — complement has no fixed points at even n)

Comp∘rev-fixed: 4
  0011
  0101
  1010
  1100

## Palindrome Analysis

Palindromes at n=4 have form L1 L2 L2 L1 (L2↔L3 and L1↔L4 match).
So 2² = 4 palindromes. They form 2 complement pairs:
  0000 ↔ 1111  (dist 4)
  0110 ↔ 1001  (dist 4)

Non-palindromes: 12 states forming 6 reversal pairs

## Named Pairings

### Complement
  Pairs:
    0000 ↔ 1111  XOR=1111 dist=4 Δw=4
    0001 ↔ 1110  XOR=1111 dist=4 Δw=2
    0010 ↔ 1101  XOR=1111 dist=4 Δw=2
    0011 ↔ 1100  XOR=1111 dist=4 Δw=0
    0100 ↔ 1011  XOR=1111 dist=4 Δw=2
    0101 ↔ 1010  XOR=1111 dist=4 Δw=0
    0110 ↔ 1001  XOR=1111 dist=4 Δw=0
    0111 ↔ 1000  XOR=1111 dist=4 Δw=2
  Measures:
    Strength:          32
    Diversity:         0.000000
    Weight Tilt:       1.5000
    Reversal Symmetry: 8/8
    Weight Correlation:-1.000000
    Mask distribution: {'1111': 8}

### Reversal
  INVALID — 4 palindromes are fixed under reversal (0000, 0110, 1001, 1111)

### Comp∘Rev
  INVALID — 4 anti-palindromes are fixed under comp∘rev (0011, 0101, 1010, 1100)

### KW-style (rev + comp for palindromes)
  Pairs:
    0000 ↔ 1111  XOR=1111 dist=4 Δw=4
    0001 ↔ 1000  XOR=1001 dist=2 Δw=0
    0010 ↔ 0100  XOR=0110 dist=2 Δw=0
    0011 ↔ 1100  XOR=1111 dist=4 Δw=0
    0101 ↔ 1010  XOR=1111 dist=4 Δw=0
    0110 ↔ 1001  XOR=1111 dist=4 Δw=0
    0111 ↔ 1110  XOR=1001 dist=2 Δw=0
    1011 ↔ 1101  XOR=0110 dist=2 Δw=0
  Measures:
    Strength:          24
    Diversity:         1.500000
    Weight Tilt:       0.5000
    Reversal Symmetry: 8/8
    Weight Correlation:+0.066667
    Mask distribution: {'0110': 2, '1001': 2, '1111': 4}

## Equivariance of Named Pairings

A pairing is equivariant under g if applying g to both members of every
pair produces another pair in the same pairing.

  Complement:
    equivariant under complement: True
    equivariant under reversal: True
    equivariant under comp∘rev: True

  KW-style (rev + comp for palindromes):
    equivariant under complement: True
    equivariant under reversal: True
    equivariant under comp∘rev: True

## Relationships Between Named Pairings
  KW-style == Complement? False

## Equivariant Pairing Counts

Counting pairings equivariant under each group element requires
checking all 2,027,025 pairings. Running enumeration...
  Enumeration: 3.5s

  Equivariant counts (out of 2,027,025):
    under complement:  5,937
    under   reversal:    993
    under   comp∘rev:    993
    under all three:     117
