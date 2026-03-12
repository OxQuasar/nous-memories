========================================================================
  Z₅ LABELING ON THE FANO PLANE
========================================================================

  f = [2, 0, 4, 3, 2, 1, 0, 3]
  PG(2,F₂): 7 points (nonzero F₂³), 7 lines

  ====================================================================
  1. Z₅ TRIPLES ON FANO LINES
  ====================================================================

  {001(震), 010(坎), 011(兌)}
    Values: (0, 4, 3), Sum mod 5 = 2
    Elements: ('Wood', 'Water', 'Metal')
    Diffs: (4, 3, 4)

  {001(震), 100(艮), 101(離)}
    Values: (0, 2, 1), Sum mod 5 = 3
    Elements: ('Wood', 'Earth', 'Fire')
    Diffs: (2, 1, 4)

  {001(震), 110(巽), 111(乾)}
    Values: (0, 0, 3), Sum mod 5 = 3
    Elements: ('Wood', 'Wood', 'Metal')
    Diffs: (0, 3, 3)

  {010(坎), 100(艮), 110(巽)}
    Values: (4, 2, 0), Sum mod 5 = 1
    Elements: ('Water', 'Earth', 'Wood')
    Diffs: (3, 1, 3)

  {010(坎), 101(離), 111(乾)}
    Values: (4, 1, 3), Sum mod 5 = 3
    Elements: ('Water', 'Fire', 'Metal')
    Diffs: (2, 4, 2)

  {011(兌), 100(艮), 111(乾)}
    Values: (3, 2, 3), Sum mod 5 = 3
    Elements: ('Metal', 'Earth', 'Metal')
    Diffs: (4, 0, 1)

  {011(兌), 101(離), 110(巽)}
    Values: (3, 1, 0), Sum mod 5 = 4
    Elements: ('Metal', 'Fire', 'Wood')
    Diffs: (3, 2, 4)

  ====================================================================
  2. LINE SUM DISTRIBUTION
  ====================================================================

  Line sums: [2, 3, 3, 1, 3, 3, 4]
  Distribution: {1: 1, 2: 1, 3: 4, 4: 1}

  Monochromatic lines: 0
  Bichromatic lines: 2
    {001(震), 110(巽), 111(乾)}: (0, 0, 3) → {0: 2, 3: 1}
    {011(兌), 100(艮), 111(乾)}: (3, 2, 3) → {3: 2, 2: 1}
  Trichromatic lines: 5

  ====================================================================
  3. COLLINEAR VS NON-COLLINEAR DIFFERENCES
  ====================================================================

  Collinear pairs (7 lines × 3 pairs = 21): 21
  Non-collinear pairs (21 total - 21 collinear = 0)...
  Total pairs: 21
  Collinear: 21
  Non-collinear: 0

  ★ Every pair of points in PG(2,F₂) is collinear!
  (This is a property of PG(2,F₂): every pair lies on exactly 1 line)

  Unsigned difference distribution (|d| = min(d, 5-d)):
    |d| = 0: 2 pairs
    |d| = 1: 9 pairs
    |d| = 2: 10 pairs

  Signed difference distribution:
    d = 0: 2 pairs (same element)
    d = 1: 3 pairs (generation ±1)
    d = 2: 4 pairs (overcoming ±2)
    d = 3: 6 pairs (overcoming ±2)
    d = 4: 6 pairs (generation ±1)

  ====================================================================
  4. 五行 RELATION ON FANO LINES
  ====================================================================

  Z₅ differences encode 五行 relations:
  d = ±1 (mod 5): generation (相生)
  d = ±2 (mod 5): overcoming (相克)
  d = 0: same element (同)

  {001(震), 010(坎), 011(兌)}
    震→坎: d=4 (gen), 震→兌: d=3 (over), 坎→兌: d=4 (gen)
    Relation profile: ('gen', 'over', 'gen')

  {001(震), 100(艮), 101(離)}
    震→艮: d=2 (over), 震→離: d=1 (gen), 艮→離: d=4 (gen)
    Relation profile: ('over', 'gen', 'gen')

  {001(震), 110(巽), 111(乾)}
    震→巽: d=0 (same), 震→乾: d=3 (over), 巽→乾: d=3 (over)
    Relation profile: ('same', 'over', 'over')

  {010(坎), 100(艮), 110(巽)}
    坎→艮: d=3 (over), 坎→巽: d=1 (gen), 艮→巽: d=3 (over)
    Relation profile: ('over', 'gen', 'over')

  {010(坎), 101(離), 111(乾)}
    坎→離: d=2 (over), 坎→乾: d=4 (gen), 離→乾: d=2 (over)
    Relation profile: ('over', 'gen', 'over')

  {011(兌), 100(艮), 111(乾)}
    兌→艮: d=4 (gen), 兌→乾: d=0 (same), 艮→乾: d=1 (gen)
    Relation profile: ('gen', 'same', 'gen')

  {011(兌), 101(離), 110(巽)}
    兌→離: d=3 (over), 兌→巽: d=2 (over), 離→巽: d=4 (gen)
    Relation profile: ('over', 'over', 'gen')

  ====================================================================
  5. CROSS-ORBIT LINE SUM COMPARISON
  ====================================================================

  Orbit 0 (size 96, shape [2, 2, 2, 1, 1]) ★:
    Rep line sums: (1, 2, 3, 4, 4, 4, 4)
    Line sum multiset orbit-invariant: no (4 types)
    Distinct diff profiles: 96

  Orbit 1 (size 48, shape [2, 2, 2, 1, 1]):
    Rep line sums: (0, 0, 0, 0, 3, 3, 4)
    Line sum multiset orbit-invariant: no (4 types)
    Distinct diff profiles: 48

  Orbit 2 (size 48, shape [2, 2, 2, 1, 1]):
    Rep line sums: (0, 0, 1, 4, 4, 4, 4)
    Line sum multiset orbit-invariant: no (4 types)
    Distinct diff profiles: 48

  Orbit 3 (size 24, shape [4, 1, 1, 1, 1]):
    Rep line sums: (0, 0, 0, 1, 2, 3, 4)
    Line sum multiset orbit-invariant: ✓
    Distinct diff profiles: 24

  Orbit 4 (size 24, shape [4, 1, 1, 1, 1]):
    Rep line sums: (2, 2, 3, 3, 4, 4, 4)
    Line sum multiset orbit-invariant: no (4 types)
    Distinct diff profiles: 24

  ====================================================================
  6. STRUCTURAL ANALYSIS OF LINE SUMS
  ====================================================================

  IC surjection line sums:
    Line ['001', '010', '011']: sum=2 (no complement line in PG)
    Line ['001', '100', '101']: sum=3 (no complement line in PG)
    Line ['001', '110', '111']: sum=3 (no complement line in PG)
    Line ['010', '100', '110']: sum=1 (no complement line in PG)
    Line ['010', '101', '111']: sum=3 (no complement line in PG)
    Line ['011', '100', '111']: sum=3 (no complement line in PG)
    Line ['011', '101', '110']: sum=4 (no complement line in PG)

  Complement action on Fano lines:
    ['001', '010', '011'] → ['100', '101', '110']: NOT a Fano line
    ['001', '100', '101'] → ['010', '011', '110']: NOT a Fano line
    ['001', '110', '111'] → ['000', '001', '110']: NOT a Fano line
    ['010', '100', '110'] → ['001', '011', '101']: NOT a Fano line
    ['010', '101', '111'] → ['000', '010', '101']: NOT a Fano line
    ['011', '100', '111'] → ['000', '011', '100']: NOT a Fano line
    ['011', '101', '110'] → ['001', '010', '100']: NOT a Fano line

  Note: complement of a nonzero point can be 000 (not in PG).
  E.g., complement(111) = 000. So complement does NOT
  preserve PG(2,F₂) as a set.
