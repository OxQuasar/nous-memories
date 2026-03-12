========================================================================
  THE FIBER PARTITION AS A COMBINATORIAL DESIGN
========================================================================

  ====================================================================
  1. IC FIBER PARTITION
  ====================================================================

  Block 0 (Wood): ['001(震)', '110(巽)'] (size 2)
  Block 1 (Fire): ['101(離)'] (size 1)
  Block 2 (Earth): ['000(坤)', '100(艮)'] (size 2)
  Block 3 (Metal): ['011(兌)', '111(乾)'] (size 2)
  Block 4 (Water): ['010(坎)'] (size 1)

  Complement pair structure:
    {000, 111}: f = (2, 3), blocks (Earth, Metal)
    {001, 110}: f = (0, 0), blocks (Wood, Wood)
    {010, 101}: f = (4, 1), blocks (Water, Fire)
    {011, 100}: f = (3, 2), blocks (Metal, Earth)

  ====================================================================
  2. BLOCK INCIDENCE ON FANO LINES
  ====================================================================

  Blocks restricted to PG(2,F₂):
    Block 0 (Wood): ['001(震)', '110(巽)'] (size 2)
    Block 1 (Fire): ['101(離)'] (size 1)
    Block 2 (Earth): ['100(艮)'] (size 1)
    Block 3 (Metal): ['011(兌)', '111(乾)'] (size 2)
    Block 4 (Water): ['010(坎)'] (size 1)

  Block pair intersection matrix (# Fano lines touching both blocks):
                Wood    Fire   Earth   Metal   Water
        Wood       5       2       2       3       2
        Fire       2       3       1       2       1
       Earth       2       1       3       1       1
       Metal       3       2       1       5       2
       Water       2       1       1       2       3

  Lines through each block:
    Wood (|block|=2): 5 lines
    Fire (|block|=1): 3 lines
    Earth (|block|=1): 3 lines
    Metal (|block|=2): 5 lines
    Water (|block|=1): 3 lines

  Colors per Fano line:
    ['001', '010', '011']: 3 colors: ['Wood', 'Metal', 'Water']
    ['001', '100', '101']: 3 colors: ['Wood', 'Fire', 'Earth']
    ['001', '110', '111']: 2 colors: ['Wood', 'Metal']
    ['010', '100', '110']: 3 colors: ['Wood', 'Earth', 'Water']
    ['010', '101', '111']: 3 colors: ['Fire', 'Metal', 'Water']
    ['011', '100', '111']: 2 colors: ['Earth', 'Metal']
    ['011', '101', '110']: 3 colors: ['Wood', 'Fire', 'Metal']

  ====================================================================
  3. GROUP-DIVISIBLE DESIGN CHECK
  ====================================================================

  A GDD requires:
  - Groups (here: complement pairs)
  - Blocks (here: fibers of f)
  - Each pair of points from different groups appears in exactly λ blocks

  λ-values for cross-group pairs: {0: 22, 1: 2}
  λ is not constant → NOT a GDD in the strict sense

  Within-group pair coverage:
    Group ['000', '111']: λ = 0
    Group ['001', '110']: λ = 1
    Group ['010', '101']: λ = 0
    Group ['011', '100']: λ = 0

  ====================================================================
  4. CROSS-ORBIT COMPARISON
  ====================================================================

  Orbit 0 (size 96, shape [2, 2, 2, 1, 1]) ★:
    GDD: no (λ dist: {0: 22, 1: 2})
    Colors/line: {2: 2, 3: 5}
    Same-color pairs on Fano lines: 2/21

  Orbit 1 (size 48, shape [2, 2, 2, 1, 1]):
    GDD: no (λ dist: {0: 22, 1: 2})
    Colors/line: {2: 2, 3: 5}
    Same-color pairs on Fano lines: 2/21

  Orbit 2 (size 48, shape [2, 2, 2, 1, 1]):
    GDD: no (λ dist: {0: 22, 1: 2})
    Colors/line: {2: 3, 3: 4}
    Same-color pairs on Fano lines: 3/21

  Orbit 3 (size 24, shape [4, 1, 1, 1, 1]):
    GDD: no (λ dist: {0: 20, 1: 4})
    Colors/line: {1: 1, 3: 6}
    Same-color pairs on Fano lines: 3/21

  Orbit 4 (size 24, shape [4, 1, 1, 1, 1]):
    GDD: no (λ dist: {0: 20, 1: 4})
    Colors/line: {2: 6, 3: 1}
    Same-color pairs on Fano lines: 6/21

  ====================================================================
  5. COMPLEMENTARY BALANCE
  ====================================================================

  For each Z₅ value k, consider block_k ∪ block_{-k mod 5}:
  These are the 'complement-related' blocks.

  Block 0 (self-neg): ['001', '110'] (size 2)
  Blocks 1∪4: ['010', '101'] (size 2)
  Blocks 2∪3: ['000', '011', '100', '111'] (size 4)

  Complement constraint: f(~x) = -f(x) means
  block_k and block_{-k} are complement-related.
  {x, ~x} always maps to {k, -k}.
  For k=0: both to 0. For k≠0: one to k, one to -k.
