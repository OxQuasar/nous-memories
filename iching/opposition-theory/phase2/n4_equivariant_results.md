======================================================================
PHASE 2: n=4 EQUIVARIANT PAIRING ANALYSIS
======================================================================

Orbits (6):
  O0: size 2 — 0000, 1111
  O1: size 4 — 0001, 0111, 1000, 1110
  O2: size 4 — 0010, 0100, 1011, 1101
  O3: size 2 — 0011, 1100
  O4: size 2 — 0101, 1010
  O5: size 2 — 0110, 1001

  Size-2 orbits: 4
  Size-4 orbits: 2

Enumerating all pairings...
  Total: 2,027,025 (3.3s)

Filtering for full Z₂²-equivariance...
  Found: 117 (5.8s)

======================================================================
Q1: INTRA-ORBIT vs INTER-ORBIT PAIRING
======================================================================

  Pairings with inter-orbit pairs: 108 / 117
  Max inter-orbit pairs in any pairing: 8

  Inter-orbit pairing IS possible among equivariant pairings.
  This explains why count (117) exceeds per-orbit product (9).

  Examples of inter-orbit equivariant pairings:

  Pairing (inter=8):
    0000 ↔ 0110  [INTER]  type=none
    0001 ↔ 0010  [INTER]  type=none
    0011 ↔ 0101  [INTER]  type=none
    0100 ↔ 1000  [INTER]  type=none
    0111 ↔ 1011  [INTER]  type=none
    1001 ↔ 1111  [INTER]  type=none
    1010 ↔ 1100  [INTER]  type=none
    1101 ↔ 1110  [INTER]  type=none

  Pairing (inter=8):
    0000 ↔ 0110  [INTER]  type=none
    0001 ↔ 0010  [INTER]  type=none
    0011 ↔ 1010  [INTER]  type=none
    0100 ↔ 1000  [INTER]  type=none
    0101 ↔ 1100  [INTER]  type=none
    0111 ↔ 1011  [INTER]  type=none
    1001 ↔ 1111  [INTER]  type=none
    1101 ↔ 1110  [INTER]  type=none

  Pairing (inter=6):
    0000 ↔ 0110  [INTER]  type=none
    0001 ↔ 0010  [INTER]  type=none
    0011 ↔ 1100  [intra]  type=comp+rev
    0100 ↔ 1000  [INTER]  type=none
    0101 ↔ 1010  [intra]  type=comp+rev
    0111 ↔ 1011  [INTER]  type=none
    1001 ↔ 1111  [INTER]  type=none
    1101 ↔ 1110  [INTER]  type=none

======================================================================
ORBIT PAIRING PATTERNS
======================================================================

  Distinct orbit-level pairing patterns: 8
    count=36: 4 intra-orbit + 4 inter-orbit pairs
    count=18: 6 intra-orbit + 2 inter-orbit pairs
    count=18: 6 intra-orbit + 2 inter-orbit pairs
    count=16: 0 intra-orbit + 8 inter-orbit pairs
    count=9: 8 intra-orbit + 0 inter-orbit pairs
    count=8: 2 intra-orbit + 6 inter-orbit pairs
    count=8: 2 intra-orbit + 6 inter-orbit pairs
    count=4: 4 intra-orbit + 4 inter-orbit pairs

======================================================================
Q2: MEASURES FOR ALL EQUIVARIANT PAIRINGS
======================================================================

  Strength distribution:
    S=16:  32 pairings
    S=20:  48 pairings
    S=24:  28 pairings
    S=28:   8 pairings
    S=32:   1 pairings

  Diversity distribution:
    D=0.000000:   3 pairings
    D=0.811278:  24 pairings
    D=1.000000:  18 pairings
    D=1.500000:  48 pairings
    D=2.000000:  24 pairings

  S × D cross-tabulation:
       S           D  count
      16    0.000000      2
      16    0.811278      8
      16    1.000000      6
      16    1.500000      8
      16    2.000000      8
      20    0.811278      8
      20    1.500000     24
      20    2.000000     16
      24    1.000000     12
      24    1.500000     16
      28    0.811278      8
      32    0.000000      1

======================================================================
Q3: UNIQUENESS ANALYSIS
======================================================================

  KW-style found in equivariant set: True
    S=24, D=1.5, WT=0.5, WC=0.066667
  Complement found in equivariant set: True
    S=32, D=0.0, WT=1.5, WC=-1.0

  Max S among equivariant: 32
    Count at max S: 1
    Is complement the unique S-maximizer? True

  Second-highest S: 28
    Count: 8
    KW among them: False

  Max D at each S level (equivariant only):
    S=32: max D = 0.000000, min D = 0.000000, n=1
    S=28: max D = 0.811278, min D = 0.811278, n=8
    S=24: max D = 1.500000, min D = 1.000000, n=28
    S=20: max D = 2.000000, min D = 0.811278, n=48
    S=16: max D = 2.000000, min D = 0.000000, n=32

  2D Pareto frontier (max S, max D) within equivariant set:
    S=32, D=0.000000 ← COMP
    S=28, D=0.811278
    S=28, D=0.811278
    S=28, D=0.811278
    S=28, D=0.811278
    S=28, D=0.811278
    S=28, D=0.811278
    S=28, D=0.811278
    S=28, D=0.811278
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000 ← KW
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=24, D=1.500000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000
    S=20, D=2.000000

======================================================================
Q4: STRUCTURAL CLASSIFICATION
======================================================================

  Distinct pair-type signatures: 28
    n= 16: none:8
    n=  8: comp+rev:2, none:6
    n=  8: comp_rev:2, none:4, rev:2
    n=  8: comp:2, comp_rev:2, none:4
    n=  8: comp:2, none:4, rev:2
    n=  8: comp+comp_rev:2, none:6
    n=  4: comp+rev:2, comp_rev:2, none:2, rev:2
    n=  4: comp_rev:4, none:4
    n=  4: comp:2, comp+rev:2, comp_rev:2, none:2
    n=  4: none:4, rev:4
    n=  4: comp:2, comp+rev:2, none:2, rev:2
    n=  4: comp:4, none:4
    n=  4: comp+comp_rev:2, comp+rev:2, none:4
    n=  4: comp+comp_rev:2, comp_rev:2, none:2, rev:2
    n=  4: comp:2, comp+comp_rev:2, comp_rev:2, none:2
    n=  4: comp:2, comp+comp_rev:2, none:2, rev:2
    n=  2: comp+rev:2, comp_rev:4, none:2
    n=  2: comp+rev:2, none:2, rev:4
    n=  2: comp:4, comp+rev:2, none:2
    n=  2: comp+comp_rev:2, comp+rev:2, comp_rev:2, rev:2
    n=  2: comp+comp_rev:2, comp_rev:4, none:2
    n=  2: comp:2, comp+comp_rev:2, comp+rev:2, comp_rev:2
    n=  2: comp+comp_rev:2, none:2, rev:4
    n=  2: comp:2, comp+comp_rev:2, comp+rev:2, rev:2
    n=  2: comp:4, comp+comp_rev:2, none:2
    n=  1: comp+comp_rev:2, comp+rev:2, comp_rev:4
    n=  1: comp+comp_rev:2, comp+rev:2, rev:4
    n=  1: comp:4, comp+comp_rev:2, comp+rev:2

======================================================================
ANALYSIS: SIZE-2 ORBIT PAIRING FREEDOM
======================================================================

  Size-2 orbits contain states from the complement-pair relationship.
  But equivariant cross-pairing between size-2 orbits is possible
  when reversal maps one orbit to another.

  Size-2 orbit reversal relationships:
    ['0000', '1111'] → rev:['0000', '1111'], cr:['0000', '1111']
    ['0011', '1100'] → rev:['0011', '1100'], cr:['0011', '1100']
    ['0101', '1010'] → rev:['0101', '1010'], cr:['0101', '1010']
    ['0110', '1001'] → rev:['0110', '1001'], cr:['0110', '1001']

  Group action on size-2 orbits:
    ['0000', '1111']: rev→['0000', '1111'], comp→['0000', '1111'], cr→['0000', '1111']
    ['0011', '1100']: rev→['0011', '1100'], comp→['0011', '1100'], cr→['0011', '1100']
    ['0101', '1010']: rev→['0101', '1010'], comp→['0101', '1010'], cr→['0101', '1010']
    ['0110', '1001']: rev→['0110', '1001'], comp→['0110', '1001'], cr→['0110', '1001']

======================================================================
SUMMARY
======================================================================

  Total Z₂²-equivariant pairings at n=4: 117
  Inter-orbit pairing possible: Yes
  Unique S-maximizer (complement): True
  KW: S=24, D=1.5
  KW S-rank among equivariant: 10/117
  KW D-rank among equivariant: 25/117
  Pareto frontier size: 41
