======================================================================
EQUIVARIANT LANDSCAPE UNDER FULL 384-ELEMENT STABILIZER
======================================================================

Building stabilizer...
  |Stab| = 384 (1.5s)

## Step 1: State Orbits Under 384-Element Group

  Number of orbits: 4
  Size distribution: {8: 2, 24: 2}
  O 0 (size  8): weights={0: 1, 2: 3, 4: 3, 6: 1}, states=[000000, 001100, 010010, 011110, 100001, 101101, 110011, 111111]
  O 1 (size 24): weights={1: 6, 3: 12, 5: 6}, states=[000001, 000010, 000100, 001000, 001101, 001110, 010000, 010011...]
  O 2 (size 24): weights={2: 12, 4: 12}, states=[000011, 000101, 000110, 001001, 001010, 001111, 010001, 010100...]
  O 3 (size  8): weights={3: 8}, states=[000111, 001011, 010101, 011001, 100110, 101010, 110100, 111000]

  Comparison with Z₂² (4 elements):
    Z₂² orbits: 20 (sizes: {2: 8, 4: 12})
    Full stabilizer orbits: 4 (sizes: {8: 2, 24: 2})

## Step 2: Pair Orbits Under 384-Element Group

  Total pair-orbits: 36 (0.0s)
  Size distribution: {4: 2, 12: 10, 24: 4, 48: 4, 64: 1, 96: 14, 192: 1}
  Valid (no internal overlap): 8 / 36
  Valid pair-orbit sizes: {4: 2, 12: 6}
    PO 0:   4 pairs,   8 states, S_contrib= 24, masks=['111111']
    PO 1:  12 pairs,  24 states, S_contrib= 48, masks=['011110', '101101', '110011']
    PO 2:  12 pairs,  24 states, S_contrib= 24, masks=['001100', '010010', '100001']
    PO 3:  12 pairs,  24 states, S_contrib= 72, masks=['111111']
    PO 4:  12 pairs,  24 states, S_contrib= 24, masks=['001100', '010010', '100001']
    PO 5:  12 pairs,  24 states, S_contrib= 48, masks=['011110', '101101', '110011']
    PO 6:  12 pairs,  24 states, S_contrib= 72, masks=['111111']
    PO 7:   4 pairs,   8 states, S_contrib= 24, masks=['111111']

## Step 3: Enumerate Equivariant Pairings

  Solutions found: 9 (0.00s)
  Distinct pairings: 9

## Step 4: Measures for Each Equivariant Pairing

  Pairing 1:
    S=120, D=2.750000, WT=1.8750, WC=-1.000000
    Pair-orbits used: [0, 7, 1, 4]
    Pair types: {'comp': 8, 'cr': 24}
    Distinct masks: 7
      111111 (dist=6): ×8
      011110 (dist=4): ×4
      101101 (dist=4): ×4
      001100 (dist=2): ×4
      110011 (dist=4): ×4
      010010 (dist=2): ×4
      100001 (dist=2): ×4

  Pairing 2:
    S=144, D=2.000000, WT=1.1250, WC=-0.400000
    Pair-orbits used: [0, 7, 1, 5]
    Pair types: {'comp': 8, 'cr': 12, 'rev': 12}
    Distinct masks: 4
      111111 (dist=6): ×8
      011110 (dist=4): ×8
      101101 (dist=4): ×8
      110011 (dist=4): ×8

  Pairing 3:
    S=168, D=1.548795, WT=1.8750, WC=-1.000000
    Pair-orbits used: [0, 7, 1, 6]
    Pair types: {'comp': 20, 'cr': 12}
    Distinct masks: 4
      111111 (dist=6): ×20
      011110 (dist=4): ×4
      101101 (dist=4): ×4
      110011 (dist=4): ×4

  Pairing 4:
    S=96, D=2.000000, WT=1.1250, WC=+0.200000
    Pair-orbits used: [0, 7, 2, 4]
    Pair types: {'comp': 8, 'rev': 12, 'cr': 12}
    Distinct masks: 4
      111111 (dist=6): ×8
      100001 (dist=2): ×8
      010010 (dist=2): ×8
      001100 (dist=2): ×8

  Pairing 5: ← KW
    S=120, D=2.750000, WT=0.3750, WC=+0.515789
    Pair-orbits used: [0, 7, 2, 5]
    Pair types: {'comp': 8, 'rev': 24}
    Distinct masks: 7
      111111 (dist=6): ×8
      100001 (dist=2): ×4
      010010 (dist=2): ×4
      110011 (dist=4): ×4
      001100 (dist=2): ×4
      101101 (dist=4): ×4
      011110 (dist=4): ×4

  Pairing 6:
    S=144, D=1.548795, WT=1.1250, WC=+0.043478
    Pair-orbits used: [0, 7, 2, 6]
    Pair types: {'comp': 20, 'rev': 12}
    Distinct masks: 4
      111111 (dist=6): ×20
      100001 (dist=2): ×4
      010010 (dist=2): ×4
      001100 (dist=2): ×4

  Pairing 7:
    S=144, D=1.548795, WT=1.8750, WC=-1.000000
    Pair-orbits used: [0, 7, 3, 4]
    Pair types: {'comp': 20, 'cr': 12}
    Distinct masks: 4
      111111 (dist=6): ×20
      001100 (dist=2): ×4
      010010 (dist=2): ×4
      100001 (dist=2): ×4

  Pairing 8:
    S=168, D=1.548795, WT=1.1250, WC=-0.448276
    Pair-orbits used: [0, 7, 3, 5]
    Pair types: {'comp': 20, 'rev': 12}
    Distinct masks: 4
      111111 (dist=6): ×20
      110011 (dist=4): ×4
      101101 (dist=4): ×4
      011110 (dist=4): ×4

  Pairing 9: ← COMPLEMENT
    S=192, D=0.000000, WT=1.8750, WC=-1.000000
    Pair-orbits used: [0, 7, 3, 6]
    Pair types: {'comp': 32}
    Distinct masks: 1
      111111 (dist=6): ×32

## Verification
  Pairing 1: equivariant under all 384 elements: True
  Pairing 2: equivariant under all 384 elements: True
  Pairing 3: equivariant under all 384 elements: True
  Pairing 4: equivariant under all 384 elements: True
  Pairing 5: equivariant under all 384 elements: True
  Pairing 6: equivariant under all 384 elements: True
  Pairing 7: equivariant under all 384 elements: True
  Pairing 8: equivariant under all 384 elements: True
  Pairing 9: equivariant under all 384 elements: True

======================================================================
SUMMARY
======================================================================

  State orbits under full stabilizer: 4
  Pair-orbits (valid): 8
  Equivariant pairings: 9

  9 pairings respect the full mirror-pair symmetry.
  The lexicographic characterization retains its role within this smaller space.
