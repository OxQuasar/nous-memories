# 先天/後天 Arrangements: Mathematical Analysis

## Part 0: Arrangement Verification & Correction

### CORRECTION: 先天 arrangement
The task specified (S→SW→W→NW→N→NE→E→SE):
  乾,兌,離,震,坤,巽,坎,艮
This has 巽 and 艮 SWAPPED in the lower half and uses clockwise direction.
It violates 說卦傳: 山澤通氣 requires 艮↔兌 diametrically opposed,
but task places 兌(SW)↔艮(SE) at 90° apart.

Correct 先天 (counterclockwise S→SE→E→NE→N→NW→W→SW):
  乾,兌,離,震,坤,艮,坎,巽
  Shao Yong values: 7,6,5,4,0,1,2,3 (upper descends, lower ascends)

### Corrected 先天八卦
    N: 坤 (000) — Earth
   NE: 震 (001) — Wood
    E: 離 (101) — Fire
   SE: 兌 (011) — Metal
    S: 乾 (111) — Metal
   SW: 巽 (110) — Wood
    W: 坎 (010) — Water
   NW: 艮 (100) — Earth

  Complement pair verification:
    坤(N) ↔ 乾(S): 180° ✓
    震(NE) ↔ 巽(SW): 180° ✓
    坎(W) ↔ 離(E): 180° ✓
    兌(SE) ↔ 艮(NW): 180° ✓

### 後天八卦
    N: 坎 (010) — Water
   NE: 艮 (100) — Earth
    E: 震 (001) — Wood
   SE: 巽 (110) — Wood
    S: 離 (101) — Fire
   SW: 坤 (000) — Earth
    W: 兌 (011) — Metal
   NW: 乾 (111) — Metal

  先天 cardinal-aligned: False
  後天 cardinal-aligned: True

## Part 1: Enumeration

Total cardinal-aligned: 96
後天 index: 43

## Part 2: Scoring

### 先天 Scores
  complement_diameter:  4/4
  reversal_reflection:  2/2
  v4_isometry:          1/3
    complement: ✓ ('rot', 4)
    reversal: ✗
    comp∘rev: ✗
  Z₂ composite:        6/6
  sheng_min_spread:     720°
  sheng_monotone:       False
  ke_angular_variance:  5994.0
  best_repr: [('震', 45), ('離', 90), ('坤', 0), ('乾', 180), ('坎', 270)]

### 後天 Scores
  complement_diameter:  1/4
  reversal_reflection:  0/2
  v4_isometry:          0/3
    complement: ✗
    reversal: ✗
    comp∘rev: ✗
  Z₂ composite:        1/6
  sheng_min_spread:     360°
  sheng_monotone:       True
  ke_angular_variance:  1134.0
  best_repr: [('震', 90), ('離', 180), ('坤', 225), ('兌', 270), ('坎', 0)]

### Metric Distributions (96 cardinal-aligned)

  complement_diameter:
    1: 64 ← 後天
    2: 32

  reversal_reflection:
    0: 56 ← 後天
    1: 32
    2: 8

  v4_isometry:
    0: 88 ← 後天
    1: 8

  sheng_min_spread:
    360: 56 ← 後天
    720: 40

  sheng_monotone:
    False: 40
    True: 56 ← 後天

  ke_angular_variance:
    1134.0: 56 ← 後天
    4374.0: 8
    7614.0: 32

## Part 3: What Uniquely Selects 後天?

### Progressive filtering
  Start: 96
  + 生 cycle monotone: 56 remain (後天: ✓)
  + element pairs adjacent or opposed: 8 remain (後天: ✓)
  + Wood/Metal adjacent, Earth opposed: 8 remain (後天: ✓)
  + cardinal yin/yang balance (1,1,2,2): 2 remain (後天: ✓)
  + sons (震坎艮) at N/NE/E: 1 remain (後天: ✓)

  Surviving arrangements:
    後天: 坎, 艮, 震, 巽, 離, 坤, 兌, 乾

### Systematic uniqueness search (all filter combinations)

  Minimal constraint sets that UNIQUELY select 後天:
    ★ elem_pair_coherent ∧ yy_balance ∧ sons_yang_half
    ★ WM_adj_E_opp ∧ yy_balance ∧ sons_yang_half

  Near-unique (2-3 survivors):
    elem_pair_coherent ∧ sons_yang_half: ['arr_019', '後天']
    WM_adj_E_opp ∧ sons_yang_half: ['arr_019', '後天']
    monotone ∧ elem_pair_coherent ∧ yy_balance: ['arr_037', '後天']
    monotone ∧ elem_pair_coherent ∧ sons_yang_half: ['arr_019', '後天']
    monotone ∧ WM_adj_E_opp ∧ yy_balance: ['arr_037', '後天']
    monotone ∧ WM_adj_E_opp ∧ sons_yang_half: ['arr_019', '後天']
    monotone ∧ yy_balance ∧ sons_yang_half: ['後天', 'arr_045']
    cd≥1 ∧ elem_pair_coherent ∧ sons_yang_half: ['arr_019', '後天']
    cd≥1 ∧ WM_adj_E_opp ∧ sons_yang_half: ['arr_019', '後天']
    elem_pair_coherent ∧ WM_adj_E_opp ∧ sons_yang_half: ['arr_019', '後天']

### Individual filter sizes
  monotone: 56/96 (後天: ✓)
  cd≥1: 96/96 (後天: ✓)
  cd≥2: 32/96 (後天: ✗)
  rr≥1: 40/96 (後天: ✗)
  elem_pair_coherent: 16/96 (後天: ✓)
  WM_adj_E_opp: 16/96 (後天: ✓)
  all_pairs_adj: 0/96 (後天: ✗)
  yy_balance: 24/96 (後天: ✓)
  sons_yang_half: 12/96 (後天: ✓)

### 後天 vs nearest alternatives (differ by ≤2 positions)

  後天: 坎, 艮, 震, 巽, 離, 坤, 兌, 乾

  arr_019: differs at ['W', 'NW']
    坎, 艮, 震, 巽, 離, 坤, 乾, 兌
    cd=1, rr=0, ke_var=1134.0
  arr_029: differs at ['NE', 'SE']
    坎, 巽, 震, 艮, 離, 坤, 兌, 乾
    cd=1, rr=0, ke_var=1134.0
  arr_030: differs at ['NE', 'NW']
    坎, 乾, 震, 巽, 離, 坤, 兌, 艮
    cd=2, rr=0, ke_var=1134.0
  arr_037: differs at ['NE', 'SW']
    坎, 坤, 震, 巽, 離, 艮, 兌, 乾
    cd=1, rr=0, ke_var=1134.0
  arr_045: differs at ['SE', 'NW']
    坎, 艮, 震, 乾, 離, 坤, 兌, 巽
    cd=1, rr=0, ke_var=1134.0
  arr_091: differs at ['E', 'SE']
    坎, 艮, 巽, 震, 離, 坤, 兌, 乾
    cd=1, rr=1, ke_var=1134.0

## Part 4: Pareto Frontier

Pareto frontier (maximize Z₂ composite, Z₅ composite):
  Z₂=6, Z₅=-419.9 — 先天
  Z₂=3, Z₅=78.7 — arr_005
  Z₂=3, Z₅=78.7 — arr_009
  Z₂=3, Z₅=78.7 — arr_048
  Z₂=3, Z₅=78.7 — arr_055
  Z₂=3, Z₅=78.7 — arr_072
  Z₂=3, Z₅=78.7 — arr_073
  Z₂=3, Z₅=78.7 — arr_075
  Z₂=3, Z₅=78.7 — arr_078
  Z₂=3, Z₅=78.7 — arr_079
  Z₂=3, Z₅=78.7 — arr_082
  Z₂=3, Z₅=78.7 — arr_083
  Z₂=3, Z₅=78.7 — arr_085
  Z₂=3, Z₅=78.7 — arr_093

先天: Z₂=6, Z₅=-419.9
後天: Z₂=1, Z₅=78.7

Max Z₂ among cardinal-aligned = 3
  24 arrangement(s) at this level

先天 Z₂ = 6 vs cardinal-aligned max = 3
  → 先天 EXCEEDS all cardinal-aligned by 3
  → UNIQUE Z₂ champion (no cardinal-aligned arrangement can match)

Max Z₅ among cardinal-aligned = 78.7: 56 arrangement(s)
後天 Z₅ = 78.7: TIED for max

Z₂ × Z₅ cross-tabulation:
    Z₂ |  -436.1  -419.9  -403.7    78.7
  ----------------------------------------
     6 |       ·       1       ·       ·
     3 |      10       ·       1      13
     2 |      12       ·       2      18
     1 |      10       ·       5      25

## Part 4.5: τ = H ∘ X⁻¹

τ mapping (先天 position → 後天 trigram at that position):
  坤 (Earth) → 坎 (Water)
  震 ( Wood) → 艮 (Earth)
  坎 (Water) → 兌 (Metal)
  兌 (Metal) → 巽 ( Wood)
  艮 (Earth) → 乾 (Metal)
  離 ( Fire) → 震 ( Wood)
  巽 ( Wood) → 坤 (Earth)
  乾 (Metal) → 離 ( Fire)

Cycle structure: (坤→坎→兌→巽) (震→艮→乾→離)
Cycle lengths: [4, 4]

Fiber preserved: False
Fiber map (not well-defined — showing conflicts):
  Earth → {'Water', 'Metal'}
  Fire → {'Wood'}
  Metal → {'Wood', 'Fire'}
  Water → {'Metal'}
  Wood → {'Earth'}

γ reference: {'Wood': 'Metal', 'Fire': 'Earth', 'Earth': 'Wood', 'Metal': 'Water', 'Water': 'Fire'}
γ match: False

## Part 5: Lo Shu Analysis

 Pos Trig   Elem  LS  HT LS%5 HT%5  Mod5
   N   坎  Water   1   1    1    1     ✓
  NE   艮  Earth   8   5    3    0     ✗
   E   震   Wood   3   3    3    3     ✓
  SE   巽   Wood   4   3    4    3     ✗
   S   離   Fire   9   2    4    2     ✗
  SW   坤  Earth   2   5    2    0     ✗
   W   兌  Metal   7   4    2    4     ✗
  NW   乾  Metal   6   4    1    4     ✗

Mod-5 matches: 2/8

He Tu pair membership (inner/outer = n, n+5):
  N: LS=1, Water pair=(1, 6), ✓
  NE: LS=8, Earth pair=(5, 10), ✗
  E: LS=3, Wood pair=(3, 8), ✓
  SE: LS=4, Wood pair=(3, 8), ✗
  S: LS=9, Fire pair=(2, 7), ✗
  SW: LS=2, Earth pair=(5, 10), ✗
  W: LS=7, Metal pair=(4, 9), ✗
  NW: LS=6, Metal pair=(4, 9), ✗

He Tu pair matches: 2/8

Lo Shu parity pattern:
  Cardinals (N,E,S,W): all ODD in Lo Shu → {1,3,9,7}
  Intercardinals: all EVEN → {8,4,2,6}
  Cardinals all odd: True
  Intercardinals all even: True

Lo Shu axis-opposite pairs and 五行 relationships:
  S(離,Fire,9) ↔ N(坎,Water,1): sum=10, rel=Water克Fire
  SW(坤,Earth,2) ↔ NE(艮,Earth,8): sum=10, rel=比和
  W(兌,Metal,7) ↔ E(震,Wood,3): sum=10, rel=Metal克Wood
  NW(乾,Metal,6) ↔ SE(巽,Wood,4): sum=10, rel=Metal克Wood
  → All axis-opposite pairs sum to 10 (magic square property)
  → Paired elements: Fire↔Water (克), Earth↔Earth (比和), Metal↔Wood (克×2)

## Summary of Key Findings

### 先天 (Corrected)
  complement_diameter = 4/4 (ALL pairs at 180°)
  reversal_reflection = 2/2
  v4_isometry = 1/3
  Z₂ composite = 6/6

### 後天
  complement_diameter = 1/4
  sheng_monotone = True
  sheng_min_spread = 360°
  ke_angular_variance = 1134.0

先天 on Pareto frontier: True
後天 on Pareto frontier: False

### Dual Uniqueness Conjecture
  先天 Z₂ = 6 vs cardinal-aligned max = 3
  → 先天 is UNIQUE Z₂ champion (exceeds all 96 cardinal-aligned)
  後天 Z₅ = 78.7 (cardinal-aligned max = 78.7)
  → 後天 IS among Z₅ maximizers (56 tied)
  → 後天 uniquely selected by: element_pair_coherent ∧ yy_balance ∧ sons_yang_half
