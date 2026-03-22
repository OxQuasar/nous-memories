# Probe 3: The 5×5 Element-Pair Torus

## Executive Summary

**Grid populations:** Verified Pop(i,j) = fiber(i) × fiber(j). The matrix has exactly 3 distinct values: {1, 2, 4}. Symmetric (pop = pop^T). Anti-diagonal totals (by relation type): {14, 12, 13, 13, 12}.

**⚡ The Siamese magic square decomposes via 生 and 克 strides.** M[i,j] = 5A[i,j] + B[i,j] + 1 where:
- A[i,j] = (i + j + 3) mod 5 — the Z₅ Cayley addition table (= 五行 relation, shifted by 3)
- B[i,j] = (i + 2j + 1) mod 5 — mixed: row stride 1 (生), column stride 2 (克)

Each 五行 relation type gets exactly one "tier" of 5 consecutive magic numbers: 克→{1-5}, 被克→{6-10}, 被生→{11-15}, 同→{16-20}, 生→{21-25}.

**⚡ Magic mod 5 is a Latin square** and an affine map on Z₅: M mod 5 = (i + 2j + 2) mod 5. Row stride = 1 (生), column stride = 2 (克). Both fundamental 五行 strides are embedded.

**He Tu additive grid has constant anti-diagonal sums (= 110)** — but this is a structural tautology (any additive grid f(i)+g(j) has this property on cyclic anti-diagonals).

**Center cell (Earth, Earth)** contains 4 hexagrams: the two 本宮 hexagrams (坤坤, 艮艮) and two rank-5 hexagrams (坤艮, 艮坤). Magic value = 13 (the median).

**Lo Shu element sums** are {Wood=7, Fire=9, Earth=10, Metal=13, Water=1} — no obvious magic property, but Metal=13 echoes the center magic value.

---

## Setup: 5×5 Grid Populations

Rows = lower trigram surjection element, Columns = upper trigram surjection element.

 Lower\Upper    Wo    Fi    Ea    Me    Wa  | Row
--------------------------------------------------
        Wood     4     2     4     4     2  | 16
        Fire     2     1     2     2     1  | 8
       Earth     4     2     4     4     2  | 16
       Metal     4     2     4     4     2  | 16
       Water     2     1     2     2     1  | 8
--------------------------------------------------
     Col sum    16     8    16    16     8  | 64

Fiber sizes: {'Wood': 2, 'Fire': 1, 'Earth': 2, 'Metal': 2, 'Water': 1}
Expected pop(i,j) = fiber(i) × fiber(j):
 Lower\Upper    Wo    Fi    Ea    Me    Wa  | Row
        Wood     4     2     4     4     2  | 16
        Fire     2     1     2     2     1  | 8
       Earth     4     2     4     4     2  | 16
       Metal     4     2     4     4     2  | 16
       Water     2     1     2     2     1  | 8

Actual = Expected: True

### Anti-diagonal populations (relation types):

Relation (i+j) mod 5 = distance in 生 cycle.

  d=0 兄弟(同)       : cells=[(0, 0), (1, 4), (2, 3), (3, 2), (4, 1)], pops=[np.int64(4), np.int64(1), np.int64(4), np.int64(4), np.int64(1)], total=14
  d=1 子孫(生)       : cells=[(0, 1), (1, 0), (2, 4), (3, 3), (4, 2)], pops=[np.int64(2), np.int64(2), np.int64(2), np.int64(4), np.int64(2)], total=12
  d=2 妻財(克)       : cells=[(0, 2), (1, 1), (2, 0), (3, 4), (4, 3)], pops=[np.int64(4), np.int64(1), np.int64(4), np.int64(2), np.int64(2)], total=13
  d=3 官鬼(被克)      : cells=[(0, 3), (1, 2), (2, 1), (3, 0), (4, 4)], pops=[np.int64(4), np.int64(2), np.int64(2), np.int64(4), np.int64(1)], total=13
  d=4 父母(被生)      : cells=[(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)], pops=[np.int64(2), np.int64(2), np.int64(4), np.int64(2), np.int64(2)], total=12

## Part 3a: Standard 5×5 Magic Square Placement

Standard magic square:
   17   24    1    8   15
   23    5    7   14   16
    4    6   13   20   22
   10   12   19   21    3
   11   18   25    2    9
Magic constant = 65

### Identity placement (algebraic Z₅ order on both axes):

Magic value at each element-pair cell:
 Lower\Upper    Wo    Fi    Ea    Me    Wa
        Wood    17    24     1     8    15
        Fire    23     5     7    14    16
       Earth     4     6    13    20    22
       Metal    10    12    19    21     3
       Water    11    18    25     2     9

### Weighted magic sums by relation type (identity placement):

  d=0 兄弟(同)       : magic_sum= 90, pop-weighted= 258
  d=1 子孫(生)       : magic_sum=115, pop-weighted= 272
  d=2 妻財(克)       : magic_sum= 15, pop-weighted=  35
  d=3 官鬼(被克)      : magic_sum= 40, pop-weighted= 107
  d=4 父母(被生)      : magic_sum= 65, pop-weighted= 156

### Exhaustive search over row/column permutations:

Total placements: 14400
Correlation with cell population:
  Mean: 0.0000
  Std: 0.0529
  Max: 0.1076 at rows=(1, 3, 0, 2, 4), cols=(3, 2, 4, 0, 1)
  Min: -0.1076 at rows=(3, 1, 2, 4, 0), cols=(0, 3, 1, 4, 2)
  Identity placement: -0.0196

### Best-correlated placement:

Row permutation: ['Fire', 'Metal', 'Wood', 'Earth', 'Water']
Col permutation: ['Metal', 'Earth', 'Water', 'Wood', 'Fire']
 Lower\Upper    Wo    Fi    Ea    Me    Wa
        Wood    14     7    16    23     5
        Fire    21    19     3    10    12
       Earth     8     1    15    17    24
       Metal    20    13    22     4     6
       Water     2    25     9    11    18

Pop-weighted sums for best placement by relation:
  d=0 兄弟(同)       : weighted= 249
  d=1 子孫(生)       : weighted= 138
  d=2 妻財(克)       : weighted= 149
  d=3 官鬼(被克)      : weighted= 198
  d=4 父母(被生)      : weighted= 120

### Worst-correlated placement:

Row permutation: ['Metal', 'Fire', 'Earth', 'Water', 'Wood']
Col permutation: ['Wood', 'Metal', 'Fire', 'Water', 'Earth']
Correlation: -0.1076

### Are relation-type magic sums ever constant?

For each placement, compute the 5 relation-type magic sums.
Check if any placement makes them all equal (= 65, since total = 325).

  FOUND: rows=(0, 1, 2, 3, 4), cols=(0, 2, 4, 1, 3), sums=[np.int64(65), np.int64(65), np.int64(65), np.int64(65), np.int64(65)]
  FOUND: rows=(0, 1, 2, 3, 4), cols=(0, 4, 3, 2, 1), sums=[np.int64(65), np.int64(65), np.int64(65), np.int64(65), np.int64(65)]
  FOUND: rows=(0, 1, 2, 3, 4), cols=(1, 0, 4, 3, 2), sums=[np.int64(65), np.int64(65), np.int64(65), np.int64(65), np.int64(65)]

Total placements with constant relation sums: 200/14400

### ⚡ Magic square decomposition via 生/克 strides

The Siamese 5×5 decomposes as M[i,j] = 5·A[i,j] + B[i,j] + 1, where A and B are
orthogonal Latin squares:

  A[i,j] = (i + j + 3) mod 5  — the Z₅ Cayley table (= 五行 relation index + 3)
  B[i,j] = (i + 2j + 1) mod 5  — row stride 1 (生), column stride 2 (克)

A sorts by 五行 relation type. B distributes within each tier using the 克 stride.

Values assigned to each relation type (anti-diagonal d = (i+j) mod 5):
  d=2 妻財(克):   tier 0 → {1, 2, 3, 4, 5}    sum = 15
  d=3 官鬼(被克):  tier 1 → {6, 7, 8, 9, 10}   sum = 40
  d=4 父母(被生):  tier 2 → {11, 12, 13, 14, 15} sum = 65
  d=0 兄弟(同):   tier 3 → {16, 17, 18, 19, 20} sum = 90
  d=1 子孫(生):   tier 4 → {21, 22, 23, 24, 25} sum = 115

The tier ordering (shifted by 3): 克 gets lowest, 生 gets highest.
The center value 13 sits at relation type 被生, tier 2 — the exact median.

---

## Part 3b: Mod-5 Residue Pattern

Magic square mod 5:
   2   4   1   3   0
   3   0   2   4   1
   4   1   3   0   2
   0   2   4   1   3
   1   3   0   2   4

Is Latin square: True

Z₅ addition table (i+j mod 5):
   0   1   2   3   4
   1   2   3   4   0
   2   3   4   0   1
   3   4   0   1   2
   4   0   1   2   3

### Is magic mod 5 an affine transform of Z₅ addition?

Looking for σ, τ, c such that magic_mod5[i,j] = (σ(i) + τ(j) + c) mod 5.

  FOUND: σ=(0, 1, 2, 3, 4), τ=(2, 4, 1, 3, 0), c=0
  i.e., magic_mod5[i,j] = (σ(i) + τ(j) + 0) mod 5
  σ(i) = 1i + 0 mod 5 (affine)
  τ(j) = 2j + 2 mod 5 (affine)

Z₅ multiplication table (i×j mod 5):
   0   0   0   0   0
   0   1   2   3   4
   0   2   4   1   3
   0   3   1   4   2
   0   4   3   2   1

Magic mod 5 == Addition table: False
Magic mod 5 == Multiplication table: False

### Row-by-row analysis of magic mod 5:

  Row 0: [np.int64(2), np.int64(4), np.int64(1), np.int64(3), np.int64(0)], successive diffs mod 5: [np.int64(2), np.int64(2), np.int64(2), np.int64(2), np.int64(2)]
  Row 1: [np.int64(3), np.int64(0), np.int64(2), np.int64(4), np.int64(1)], successive diffs mod 5: [np.int64(2), np.int64(2), np.int64(2), np.int64(2), np.int64(2)]
  Row 2: [np.int64(4), np.int64(1), np.int64(3), np.int64(0), np.int64(2)], successive diffs mod 5: [np.int64(2), np.int64(2), np.int64(2), np.int64(2), np.int64(2)]
  Row 3: [np.int64(0), np.int64(2), np.int64(4), np.int64(1), np.int64(3)], successive diffs mod 5: [np.int64(2), np.int64(2), np.int64(2), np.int64(2), np.int64(2)]
  Row 4: [np.int64(1), np.int64(3), np.int64(0), np.int64(2), np.int64(4)], successive diffs mod 5: [np.int64(2), np.int64(2), np.int64(2), np.int64(2), np.int64(2)]

  Col 0: [np.int64(2), np.int64(3), np.int64(4), np.int64(0), np.int64(1)], successive diffs mod 5: [np.int64(1), np.int64(1), np.int64(1), np.int64(1), np.int64(1)]
  Col 1: [np.int64(4), np.int64(0), np.int64(1), np.int64(2), np.int64(3)], successive diffs mod 5: [np.int64(1), np.int64(1), np.int64(1), np.int64(1), np.int64(1)]
  Col 2: [np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(0)], successive diffs mod 5: [np.int64(1), np.int64(1), np.int64(1), np.int64(1), np.int64(1)]
  Col 3: [np.int64(3), np.int64(4), np.int64(0), np.int64(1), np.int64(2)], successive diffs mod 5: [np.int64(1), np.int64(1), np.int64(1), np.int64(1), np.int64(1)]
  Col 4: [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4)], successive diffs mod 5: [np.int64(1), np.int64(1), np.int64(1), np.int64(1), np.int64(1)]

## Part 3c: Center Cell (Earth, Earth)

Cell (Earth, Earth): 4 hexagrams

| Hex | Name | Binary | Palace | Rank | Lower trig | Upper trig |
|-----|------|--------|--------|------|------------|------------|
|  0 | Kun          | 000000 | Kun ☷    | 0 (本宮) | 坤 | 坤 |
|  4 | Qian         | 000100 | Dui ☱    | 5 (五世) | 艮 | 坤 |
| 32 | Bo           | 100000 | Qian ☰   | 5 (五世) | 坤 | 艮 |
| 36 | Gen          | 100100 | Gen ☶    | 0 (本宮) | 艮 | 艮 |

Earth-mapping trigrams: 坤 (000) and 艮 (100)
So (Earth,Earth) cell = hexagrams with lower ∈ {坤,艮} AND upper ∈ {坤,艮}
Possible combos: 坤坤, 坤艮, 艮坤, 艮艮 = 4 hexagrams

### Properties:

**h0 (Kun):** 坤/坤
  Element profile: E→F→W→E→W→M, Z₅ sum=12
  六親 profile: 兄弟→父母→官鬼→兄弟→妻財→子孫
  Palace: Kun ☷ (rank 0)

**h4 (Qian):** 艮/坤
  Element profile: E→F→M→E→W→M, Z₅ sum=15
  六親 profile: 父母→官鬼→兄弟→父母→子孫→兄弟
  Palace: Dui ☱ (rank 5)

**h32 (Bo):** 坤/艮
  Element profile: E→F→W→E→F→M, Z₅ sum=9
  六親 profile: 父母→官鬼→妻財→父母→官鬼→兄弟
  Palace: Qian ☰ (rank 5)

**h36 (Gen):** 艮/艮
  Element profile: E→F→M→E→F→M, Z₅ sum=12
  六親 profile: 兄弟→父母→子孫→兄弟→父母→子孫
  Palace: Gen ☶ (rank 0)

Magic square value at (2,2) = 13
This is the center of the 5×5 magic square (value 13 = (25+1)/2).

## Part 3d: Lo Shu Pullback via Surjection

### Test 1: Fiber partition verification

Fiber sizes: Wood=2, Fire=1, Earth=2, Metal=2, Water=1
Partition: [2, 2, 2, 1, 1] = [2, 2, 2, 1, 1]
Pop(i,j) = fiber(i) × fiber(j): verified = True

Population matrix (actual):
      Wood:  4   2   4   4   2
      Fire:  2   1   2   2   1
     Earth:  4   2   4   4   2
     Metal:  4   2   4   4   2
     Water:  2   1   2   2   1
  Unique values: [np.int64(1), np.int64(2), np.int64(4)]

### Test 2: Lo Shu → element-level sums

Lo Shu trigram placement:
  巽(4) 離(9) 坤(2)
  震(3)  [5]  兌(7)
  艮(8) 坎(1) 乾(6)

Element-level Lo Shu sums (sum of fiber trigram values):
  Wood: 7 (fiber size 2)
  Fire: 9 (fiber size 1)
  Earth: 10 (fiber size 2)
  Metal: 13 (fiber size 2)
  Water: 1 (fiber size 1)
  Total: 40 (= 45 - 5 = 40, center excluded)

Relations to known constants:
  Element sums: [7, 9, 10, 13, 1]
  Sum = 40
  Pairwise sums (consecutive in Z₅): [16, 19, 23, 14, 8]

### Lo Shu element sums placed on 5×5 grid:

Each cell (i,j) gets value = elem_loshu_sum(i) + elem_loshu_sum(j):
 Lower\Upper    Wo    Fi    Ea    Me    Wa
        Wood    14    16    17    20     8
        Fire    16    18    19    22    10
       Earth    17    19    20    23    11
       Metal    20    22    23    26    14
       Water     8    10    11    14     2

Row sums: [np.int64(75), np.int64(85), np.int64(90), np.int64(105), np.int64(45)]
Col sums: [np.int64(75), np.int64(85), np.int64(90), np.int64(105), np.int64(45)]

Population-weighted total: 1120

### Test 3: He Tu element numbers on 5×5 grid

He Tu pair sums: {'Wood': 11, 'Fire': 9, 'Earth': 15, 'Metal': 13, 'Water': 7}

Additive He Tu grid (row_sum + col_sum):
 Lower\Upper    Wo    Fi    Ea    Me    Wa
        Wood    22    20    26    24    18
        Fire    20    18    24    22    16
       Earth    26    24    30    28    22
       Metal    24    22    28    26    20
       Water    18    16    22    20    14

Row sums: [np.int64(110), np.int64(100), np.int64(130), np.int64(120), np.int64(90)]
Col sums: [np.int64(110), np.int64(100), np.int64(130), np.int64(120), np.int64(90)]

He Tu grid anti-diagonal sums (by relation type):
  d=0 兄弟(同)       : sum=110, pop-weighted= 344
  d=1 子孫(生)       : sum=110, pop-weighted= 272
  d=2 妻財(克)       : sum=110, pop-weighted= 306
  d=3 官鬼(被克)      : sum=110, pop-weighted= 302
  d=4 父母(被生)      : sum=110, pop-weighted= 280

**NOTE:** The constant anti-diagonal sum (= 110 = 2 × 55) is a structural tautology.
For ANY additive grid f(i) + g(j) on cyclic anti-diagonals (i+j) mod n:
  Σ_r (f(r) + g((d-r) mod n)) = Σ f + Σ g = constant.
The He Tu pair sums happen to be {7, 9, 11, 13, 15} with Σ = 55, giving 2×55 = 110.
The pop-weighted sums ARE non-constant — these reflect genuine structure.

Multiplicative He Tu grid (row_sum × col_sum):
 Lower\Upper    Wo    Fi    Ea    Me    Wa
        Wood   121    99   165   143    77
        Fire    99    81   135   117    63
       Earth   165   135   225   195   105
       Metal   143   117   195   169    91
       Water    77    63   105    91    49

### He Tu pair sums on anti-diagonals:

  d=0: values=[22, 16, 28, 28, 16], sum=110
  d=1: values=[20, 20, 22, 26, 22], sum=110
  d=2: values=[26, 18, 26, 20, 20], sum=110
  d=3: values=[24, 24, 24, 24, 14], sum=110
  d=4: values=[18, 22, 30, 22, 18], sum=110

## Additional Observations

### Population matrix symmetry:

Symmetric (pop = pop^T): True

### Population per anti-diagonal (relation type):

  d=0 兄弟(同)       : pops=[np.int64(4), np.int64(1), np.int64(4), np.int64(4), np.int64(1)], total=14
  d=1 子孫(生)       : pops=[np.int64(2), np.int64(2), np.int64(2), np.int64(4), np.int64(2)], total=12
  d=2 妻財(克)       : pops=[np.int64(4), np.int64(1), np.int64(4), np.int64(2), np.int64(2)], total=13
  d=3 官鬼(被克)      : pops=[np.int64(4), np.int64(2), np.int64(2), np.int64(4), np.int64(1)], total=13
  d=4 父母(被生)      : pops=[np.int64(2), np.int64(2), np.int64(4), np.int64(2), np.int64(2)], total=12

### Analytical population per anti-diagonal:

  d=0: Σ fiber(r)×fiber((d-r) mod 5) = 14
  d=1: Σ fiber(r)×fiber((d-r) mod 5) = 12
  d=2: Σ fiber(r)×fiber((d-r) mod 5) = 13
  d=3: Σ fiber(r)×fiber((d-r) mod 5) = 13
  d=4: Σ fiber(r)×fiber((d-r) mod 5) = 12

### Magic square anti-diagonal sums (identity placement):

  d=0: sum=90
  d=1: sum=115
  d=2: sum=15
  d=3: sum=40
  d=4: sum=65
  Total: 325
  Constant at 65? False
