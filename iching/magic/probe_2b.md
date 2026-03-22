# Probe 2b: Palace Rank Structure, Zero Cells, and Z₅ Sum Distribution

## Executive Summary

**Part 1 — Zero Cells:** All 4 zero cells in the 6×5 grid are **structurally hard** — no trigram in the 納甲 system can produce them. Metal is impossible at L1, L2, L4 (positions 1 in both lower and upper trigrams). Wood is impossible at L6 (position 3 in upper trigram). This traces to the 天干/地支 branch assignments.

**Part 2 — Rank Structure:** Rank 6 (游魂) has the highest element diversity: 4/8 hexagrams have all 5 elements (vs 0–2 for other ranks), average 4.5 distinct elements. Rank 3 (三世) has the lowest: zero all-5 hexagrams, all have exactly 4. The all-5 condition requires lower and upper trigram non-Earth pairs to be disjoint. The 4 possible non-Earth pairs form an F₂² lattice; disjointness = XOR=11 condition.

**Part 3 — Z₅ Sum:** The non-uniform mod-5 distribution {0:12, 1:6, 2:24, 3:2, 4:20} is **exactly predicted** by convolution of trigram-level Z₅ sums. Each trigram has sum ∈ {3, 6, 9} (all ≡ 0 mod 3). The sole lower/upper asymmetry is 坤: sum=3 as lower (stem 乙), sum=9 as upper (stem 癸). All other trigrams have identical sums in both positions.

---

## Part 1: Zero Cells and 納甲 Branch Structure

### 1a. Lower trigram 納甲 assignments (L1, L2, L3):

Stem  Trigram   L1 branch   L1 elem   L2 branch   L2 elem   L3 branch   L3 elem
--------------------------------------------------------------------------------
   丁       兌           巳      Fire           卯      Wood           丑     Earth
   丙       艮           辰     Earth           午      Fire           申     Metal
   乙       坤           未     Earth           巳      Fire           卯      Wood
   己       離           卯      Wood           丑     Earth           亥     Water
   庚       震           子     Water           寅      Wood           辰     Earth
   戊       坎           寅      Wood           辰     Earth           午      Fire
   甲       乾           子     Water           寅      Wood           辰     Earth
   辛       巽           丑     Earth           亥     Water           酉     Metal

### 1b. Upper trigram 納甲 assignments (L4, L5, L6):

Stem  Trigram   L4 branch   L4 elem   L5 branch   L5 elem   L6 branch   L6 elem
--------------------------------------------------------------------------------
   丁       兌           巳      Fire           卯      Wood           丑     Earth
   丙       艮           辰     Earth           午      Fire           申     Metal
   壬       乾           午      Fire           申     Metal           戌     Earth
   己       離           卯      Wood           丑     Earth           亥     Water
   庚       震           子     Water           寅      Wood           辰     Earth
   戊       坎           寅      Wood           辰     Earth           午      Fire
   癸       坤           丑     Earth           亥     Water           酉     Metal
   辛       巽           丑     Earth           亥     Water           酉     Metal

### 1c. Possible elements at each position:

L1: possible = ['Earth', 'Fire', 'Water', 'Wood'], IMPOSSIBLE = ['Metal']
L2: possible = ['Earth', 'Fire', 'Water', 'Wood'], IMPOSSIBLE = ['Metal']
L3: possible = ['Earth', 'Fire', 'Metal', 'Water', 'Wood'], IMPOSSIBLE = ∅
L4: possible = ['Earth', 'Fire', 'Water', 'Wood'], IMPOSSIBLE = ['Metal']
L5: possible = ['Earth', 'Fire', 'Metal', 'Water', 'Wood'], IMPOSSIBLE = ∅
L6: possible = ['Earth', 'Fire', 'Metal', 'Water'], IMPOSSIBLE = ['Wood']

### 1d. Zero cell analysis:

Zero cells in the 6×5 grid:
  (L1, Metal): count=0 — HARD (no trigram produces this)
  (L2, Metal): count=0 — HARD (no trigram produces this)
  (L4, Metal): count=0 — HARD (no trigram produces this)
  (L6, Wood): count=0 — HARD (no trigram produces this)

### 1e. Structural possibility matrix:

How many of the 8 trigrams produce each (position, element) pair:
       Wood   Fire  Earth  Metal  Water
L1        2      1      3      0      2  ←Metal impossible
L2        3      2      2      0      1  ←Metal impossible
L3        1      1      3      2      1
L4        2      2      3      0      1  ←Metal impossible
L5        2      1      2      1      2
L6        0      1      3      3      1  ←Wood impossible

## Part 2: Rank Structure and All-5-Element Hexagrams

### 2a. The 16 all-5-element hexagrams by rank:

| Hex | Name | Palace | Rank | Rank Name | Element Profile |
|-----|------|--------|------|-----------|-----------------|
|  0 | Kun          | Kun ☷    | 0 | 本宮 | E→F→W→E→W→M |
| 63 | Qian         | Qian ☰   | 0 | 本宮 | W→W→E→F→M→E |
| 37 | Bi           | Gen ☶    | 1 | 一世 | W→E→W→E→F→M |
| 44 | Lu           | Li ☲     | 1 | 一世 | E→F→M→W→E→W |
| 39 | Da Chu       | Gen ☶    | 2 | 二世 | W→W→E→E→F→M |
|  3 | Lin          | Kun ☷    | 2 | 二世 | F→W→E→E→W→M |
| 48 | Guan         | Qian ☰   | 4 | 四世 | E→F→W→E→W→M |
| 57 | Wu Wang      | Xun ☴    | 4 | 四世 | W→W→E→F→M→E |
| 50 | Huan         | Li ☲     | 5 | 五世 | W→E→F→E→W→M |
| 22 | Jing         | Zhen ☳   | 5 | 五世 | E→W→M→W→E→F |
| 12 | Xiao Guo     | Dui ☱    | 6 | 游魂 | E→F→M→W→W→E |
| 51 | Zhong Fu     | Gen ☶    | 6 | 游魂 | F→W→E→E→W→M |
| 33 | Yi           | Xun ☴    | 6 | 游魂 | W→W→E→E→F→M |
| 30 | Da Guo       | Zhen ☳   | 6 | 游魂 | E→W→M→F→W→E |
|  2 | Shi          | Kan ☵    | 7 | 歸魂 | W→E→F→E→W→M |
| 61 | Tong Ren     | Li ☲     | 7 | 歸魂 | W→E→W→F→M→E |

### 2b. All-5-element count by rank:

| Rank | Name | All-5 count | Out of 8 |
|------|------|-------------|----------|
| 0 | 本宮 | 2 | 8 |
| 1 | 一世 | 2 | 8 |
| 2 | 二世 | 2 | 8 |
| 3 | 三世 | 0 | 8 |
| 4 | 四世 | 2 | 8 |
| 5 | 五世 | 2 | 8 |
| 6 | 游魂 | 4 | 8 |
| 7 | 歸魂 | 2 | 8 |

### 2c. Average distinct elements per rank:

| Rank | Name | Avg distinct | Min | Max | All-5 count |
|------|------|-------------|-----|-----|-------------|
| 0 | 本宮 | 3.500 | 3 | 5 | 2 |
| 1 | 一世 | 4.000 | 3 | 5 | 2 |
| 2 | 二世 | 4.000 | 3 | 5 | 2 |
| 3 | 三世 | 4.000 | 4 | 4 | 0 |
| 4 | 四世 | 4.000 | 3 | 5 | 2 |
| 5 | 五世 | 4.000 | 3 | 5 | 2 |
| 6 | 游魂 | 4.500 | 4 | 5 | 4 |
| 7 | 歸魂 | 4.000 | 3 | 5 | 2 |

### 2d. Distinct elements by palace × rank:

Palace       elem   R0  R1  R2  R3  R4  R5  R6  R7  | Avg
---------------------------------------------------------------------------
Dui ☱        Metal   3   3   3   4   4   4   5   4  | 3.75
Gen ☶        Earth   3   5   5   4   4   4   5   4  | 4.25
Kan ☵        Water   3   3   4   4   4   3   4   5  | 3.75
Kun ☷        Earth   5   4   5   4   3   4   4   3  | 4.00
Li ☲         Fire    3   5   4   4   4   5   4   5  | 4.25
Qian ☰       Metal   5   4   3   4   5   4   4   3  | 4.00
Xun ☴        Wood    3   4   4   4   5   3   5   4  | 4.00
Zhen ☳       Wood    3   4   4   4   3   5   5   4  | 4.00

### 2e. Element multiplicity distribution by rank:

For each rank, how many hexagrams have each element count (0, 1, or 2):

**Rank 0 (本宮):**
  Wood  : 0×=2, 1×=2, 2×=4
  Fire  : 0×=3, 1×=2, 2×=3
  Earth : 2×=8
  Metal : 0×=4, 1×=2, 2×=2
  Water : 0×=3, 1×=2, 2×=3

**Rank 1 (一世):**
  Wood  : 0×=1, 1×=4, 2×=3
  Fire  : 0×=2, 1×=4, 2×=2
  Earth : 2×=8
  Metal : 0×=3, 1×=4, 2×=1
  Water : 0×=2, 1×=4, 2×=2

**Rank 2 (二世):**
  Wood  : 0×=1, 1×=4, 2×=3
  Fire  : 0×=2, 1×=4, 2×=2
  Earth : 2×=8
  Metal : 0×=3, 1×=4, 2×=1
  Water : 0×=2, 1×=4, 2×=2

**Rank 3 (三世):**
  Wood  : 1×=6, 2×=2
  Fire  : 0×=3, 1×=2, 2×=3
  Earth : 2×=8
  Metal : 0×=2, 1×=6
  Water : 0×=3, 1×=2, 2×=3

**Rank 4 (四世):**
  Wood  : 0×=1, 1×=4, 2×=3
  Fire  : 0×=2, 1×=4, 2×=2
  Earth : 2×=8
  Metal : 0×=3, 1×=4, 2×=1
  Water : 0×=2, 1×=4, 2×=2

**Rank 5 (五世):**
  Wood  : 0×=1, 1×=4, 2×=3
  Fire  : 0×=2, 1×=4, 2×=2
  Earth : 2×=8
  Metal : 0×=3, 1×=4, 2×=1
  Water : 0×=2, 1×=4, 2×=2

**Rank 6 (游魂):**
  Wood  : 1×=6, 2×=2
  Fire  : 0×=1, 1×=6, 2×=1
  Earth : 2×=8
  Metal : 0×=2, 1×=6
  Water : 0×=1, 1×=6, 2×=1

**Rank 7 (歸魂):**
  Wood  : 0×=2, 1×=2, 2×=4
  Fire  : 0×=1, 1×=6, 2×=1
  Earth : 2×=8
  Metal : 0×=4, 1×=2, 2×=2
  Water : 0×=1, 1×=6, 2×=1

### 2f. ⚡ Structural explanation for all-5-element condition

Every trigram contributes exactly 1 Earth + 2 non-Earth elements to its 3 lines.
The 4 possible non-Earth pairs across all trigrams are:
  {Wood, Fire}, {Wood, Water}, {Metal, Fire}, {Metal, Water}

These form a Boolean lattice F₂²:
  (Wood present?, Fire present?) → {W,F}=(1,1), {W,Wa}=(1,0), {M,F}=(0,1), {M,Wa}=(0,0)

All-5-element condition: lower pair ∩ upper pair = ∅ ⟺ they differ on BOTH coordinates.
I.e., the disjointness is exactly XOR = (1,1) in the F₂² lattice.

The 2 complementary pairings correspond to:
  {Wood,Fire} ↔ {Metal,Water} — Z₅ negation pairs ({0,1} ↔ {3,4})
  {Wood,Water} ↔ {Metal,Fire} — Z₅ 克-stride pairs ({0,4} ↔ {1,3})

**Why 游魂 (rank 6) is maximal:** At rank 6, the lower trigram retains its rank-5 identity
(= the palace's 克-partner) while the upper trigram flips to a new trigram. This maximizes
the chance that lower and upper non-Earth pairs are complementary. The rank-6 upper trigram
is structurally distant from the lower, promoting diversity.

**Why 三世 (rank 3) has zero all-5:** At rank 3, the lower trigram has been fully replaced
(3 flips) while the upper remains the palace trigram. The lower replacement tends to share
non-Earth elements with the upper, reducing diversity to exactly 4 for all 8 palaces.

---

## Part 3: Z₅ Sum Distribution

### 3a. Z₅ sum mod 5 × palace element:

 Palace elem  ≡0  ≡1  ≡2  ≡3  ≡4  | Total
--------------------------------------------------
        Wood   5   0   6   2   3  | 16 (2 palaces)
        Fire   1   0   4   0   3  | 8 (1 palace)
       Earth   3   1   7   0   5  | 16 (2 palaces)
       Metal   2   3   5   0   6  | 16 (2 palaces)
       Water   1   2   2   0   3  | 8 (1 palace)
       Total  12   6  24   2  20  | 64

### 3b. Z₅ sum mod 5 × palace rank:

        Rank  ≡0  ≡1  ≡2  ≡3  ≡4  | Total
--------------------------------------------------
0       本宮   0   2   5   1   0  | 8
1       一世   3   2   2   0   1  | 8
2       二世   2   1   3   0   2  | 8
3       三世   3   0   0   0   5  | 8
4       四世   0   0   3   1   4  | 8
5       五世   1   0   4   0   3  | 8
6       游魂   1   0   4   0   3  | 8
7       歸魂   2   1   3   0   2  | 8

### 3c. (Lower trigram Z₅ sum, Upper trigram Z₅ sum) cross-tab:

 Lower\Upper    3    6    9  | Total
----------------------------------------
           3    6   12    6  | 24
           6    8   16    8  | 32
           9    2    4    2  | 8

Total hexagram Z₅ sum = lower + upper:
  sum= 6:  6 hexagrams  compositions: 3+3(×6)
  sum= 9: 20 hexagrams  compositions: 3+6(×12), 6+3(×8)
  sum=12: 24 hexagrams  compositions: 3+9(×6), 6+6(×16), 9+3(×2)
  sum=15: 12 hexagrams  compositions: 6+9(×8), 9+6(×4)
  sum=18:  2 hexagrams  compositions: 9+9(×2)

### 3d. Per-trigram Z₅ sums:

**Lower trigrams (stem → trigram → branches → elements → Z₅ sum):**

  丁 (兌): ('Fire', 'Wood', 'Earth') → Z₅=[1, 0, 2] → sum=3 (surjection elem=Metal, Z₅=3)
  丙 (艮): ('Earth', 'Fire', 'Metal') → Z₅=[2, 1, 3] → sum=6 (surjection elem=Earth, Z₅=2)
  乙 (坤): ('Earth', 'Fire', 'Wood') → Z₅=[2, 1, 0] → sum=3 (surjection elem=Earth, Z₅=2)
  己 (離): ('Wood', 'Earth', 'Water') → Z₅=[0, 2, 4] → sum=6 (surjection elem=Fire, Z₅=1)
  庚 (震): ('Water', 'Wood', 'Earth') → Z₅=[4, 0, 2] → sum=6 (surjection elem=Wood, Z₅=0)
  戊 (坎): ('Wood', 'Earth', 'Fire') → Z₅=[0, 2, 1] → sum=3 (surjection elem=Water, Z₅=4)
  甲 (乾): ('Water', 'Wood', 'Earth') → Z₅=[4, 0, 2] → sum=6 (surjection elem=Metal, Z₅=3)
  辛 (巽): ('Earth', 'Water', 'Metal') → Z₅=[2, 4, 3] → sum=9 (surjection elem=Wood, Z₅=0)

**Upper trigrams (stem → trigram → branches → elements → Z₅ sum):**

  丁 (兌): ('Fire', 'Wood', 'Earth') → Z₅=[1, 0, 2] → sum=3 (surjection elem=Metal, Z₅=3)
  丙 (艮): ('Earth', 'Fire', 'Metal') → Z₅=[2, 1, 3] → sum=6 (surjection elem=Earth, Z₅=2)
  壬 (乾): ('Fire', 'Metal', 'Earth') → Z₅=[1, 3, 2] → sum=6 (surjection elem=Metal, Z₅=3)
  己 (離): ('Wood', 'Earth', 'Water') → Z₅=[0, 2, 4] → sum=6 (surjection elem=Fire, Z₅=1)
  庚 (震): ('Water', 'Wood', 'Earth') → Z₅=[4, 0, 2] → sum=6 (surjection elem=Wood, Z₅=0)
  戊 (坎): ('Wood', 'Earth', 'Fire') → Z₅=[0, 2, 1] → sum=3 (surjection elem=Water, Z₅=4)
  癸 (坤): ('Earth', 'Water', 'Metal') → Z₅=[2, 4, 3] → sum=9 (surjection elem=Earth, Z₅=2)
  辛 (巽): ('Earth', 'Water', 'Metal') → Z₅=[2, 4, 3] → sum=9 (surjection elem=Wood, Z₅=0)

**Trigram Z₅ sum vs surjection element:**

| Trigram | Surj elem | Z₅(surj) | Lower sum | Upper sum |
|---------|-----------|----------|-----------|-----------|
| 乾 | Metal | 3 | 6 | 6 |
| 坤 | Earth | 2 | 3 | 9 |
| 震 | Wood  | 0 | 6 | 6 |
| 巽 | Wood  | 0 | 9 | 9 |
| 坎 | Water | 4 | 3 | 3 |
| 離 | Fire  | 1 | 6 | 6 |
| 艮 | Earth | 2 | 6 | 6 |
| 兌 | Metal | 3 | 3 | 3 |

### 3e. Verification: hexagram Z₅ sum determined by trigram pair

Mismatches between predicted (from stems) and actual Z₅ sum: 0/64

### 3f. Explaining the mod-5 distribution:

Lower trigram Z₅ sum distribution (across 64 hexagrams):
  sum=3: 24 hexagrams
  sum=6: 32 hexagrams
  sum=9: 8 hexagrams

Upper trigram Z₅ sum distribution (across 64 hexagrams):
  sum=3: 16 hexagrams
  sum=6: 32 hexagrams
  sum=9: 16 hexagrams

Lower: {3: 3, 6: 4, 9: 1} trigrams per sum value
Upper: {3: 2, 6: 4, 9: 2} trigrams per sum value

**Predicted hex sum distribution from trigram-level convolution:**
(Each of 8 lower trigrams × each of 8 upper trigrams = 64 pairs)

  sum= 6: predicted= 6, actual= 6 ✓
  sum= 9: predicted=20, actual=20 ✓
  sum=12: predicted=24, actual=24 ✓
  sum=15: predicted=12, actual=12 ✓
  sum=18: predicted= 2, actual= 2 ✓

**Predicted mod-5 distribution:**
  ≡0 mod 5: predicted=12, actual=12
  ≡1 mod 5: predicted= 6, actual= 6
  ≡2 mod 5: predicted=24, actual=24
  ≡3 mod 5: predicted= 2, actual= 2
  ≡4 mod 5: predicted=20, actual=20

### 3g. Root cause of non-uniform mod-5 distribution:

Trigram Z₅ sums (lower position):
  丁 (兌): sum=3, mod 5 = 3
  丙 (艮): sum=6, mod 5 = 1
  乙 (坤): sum=3, mod 5 = 3
  己 (離): sum=6, mod 5 = 1
  庚 (震): sum=6, mod 5 = 1
  戊 (坎): sum=3, mod 5 = 3
  甲 (乾): sum=6, mod 5 = 1
  辛 (巽): sum=9, mod 5 = 4

Trigram Z₅ sums (upper position):
  丁 (兌): sum=3, mod 5 = 3
  丙 (艮): sum=6, mod 5 = 1
  壬 (乾): sum=6, mod 5 = 1
  己 (離): sum=6, mod 5 = 1
  庚 (震): sum=6, mod 5 = 1
  戊 (坎): sum=3, mod 5 = 3
  癸 (坤): sum=9, mod 5 = 4
  辛 (巽): sum=9, mod 5 = 4

Lower trigram sum mod 5 distribution (across 8 trigrams): {1: 4, 3: 3, 4: 1}
Upper trigram sum mod 5 distribution (across 8 trigrams): {1: 4, 3: 2, 4: 2}

Hex sum mod 5 = convolution of trigram mod-5 distributions:
  ≡0 mod 5: 12 (from 64 = 8×8 pairs)
  ≡1 mod 5: 6 (from 64 = 8×8 pairs)
  ≡2 mod 5: 24 (from 64 = 8×8 pairs)
  ≡3 mod 5: 2 (from 64 = 8×8 pairs)
  ≡4 mod 5: 20 (from 64 = 8×8 pairs)

### 3h. ⚡ 坤 is the sole source of lower/upper asymmetry

Trigram Z₅ sums in lower vs upper position:

| Trigram | Surj elem | Lower sum | Upper sum | Same? |
|---------|-----------|-----------|-----------|-------|
| 乾 | Metal | 6 | 6 | ✓ |
| 坤 | Earth | 3 | 9 | ✗ DIFFERENT |
| 震 | Wood | 6 | 6 | ✓ |
| 巽 | Wood | 9 | 9 | ✓ |
| 坎 | Water | 3 | 3 | ✓ |
| 離 | Fire | 6 | 6 | ✓ |
| 艮 | Earth | 6 | 6 | ✓ |
| 兌 | Metal | 3 | 3 | ✓ |

Only 坤 has different Z₅ sums in lower vs upper position.
This is because 納甲 assigns different stems: 乙 (lower) → (Earth, Fire, Wood) = sum 3,
vs 癸 (upper) → (Earth, Water, Metal) = sum 9.

坤's lower elements {Earth, Fire, Wood} = {2, 1, 0} ← the "low" Z₅ triple (sum 3)
坤's upper elements {Earth, Water, Metal} = {2, 4, 3} ← the "high" Z₅ triple (sum 9)
These are Z₅-complementary: {0,1,2} ↔ {2,3,4}, sharing only Earth(2).

The lower/upper trigram sum distributions differ ONLY because of 坤:
  Lower: {3: 3 trigrams, 6: 4, 9: 1}  (坤 contributes 3)
  Upper: {3: 2 trigrams, 6: 4, 9: 2}  (坤 contributes 9)

If 坤 had the same sum in both positions, the distribution would be symmetric.
