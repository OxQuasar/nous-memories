# Transformation Graph and Palace Structure

## Task 1: Single-Change Graph on Z₂⁶

### Relation changes by line position

Lines 1-3 change lower trigram (体). Lines 4-6 change upper trigram (用).

  Line 1 (b0, 体(lower)):
    Element changes: 64/64 (100%)
    Basin changes: 0/64 (0%)
    Relation preserved: 0/64 (0%)
  Line 2 (b1, 体(lower)):
    Element changes: 64/64 (100%)
    Basin changes: 0/64 (0%)
    Relation preserved: 0/64 (0%)
  Line 3 (b2, 体(lower)):
    Element changes: 32/64 (50%)
    Basin changes: 64/64 (100%)
    Relation preserved: 32/64 (50%)
  Line 4 (b3, 用(upper)):
    Element changes: 64/64 (100%)
    Basin changes: 64/64 (100%)
    Relation preserved: 0/64 (0%)
  Line 5 (b4, 用(upper)):
    Element changes: 64/64 (100%)
    Basin changes: 0/64 (0%)
    Relation preserved: 0/64 (0%)
  Line 6 (b5, 用(upper)):
    Element changes: 32/64 (50%)
    Basin changes: 0/64 (0%)
    Relation preserved: 32/64 (50%)

### Basin-changing lines

  Line 1 (b0): 0/64 basin changes
  Line 2 (b1): 0/64 basin changes
  Line 3 (b2): 64/64 basin changes
  Line 4 (b3): 64/64 basin changes
  Line 5 (b4): 0/64 basin changes
  Line 6 (b5): 0/64 basin changes
  → Only lines 3 and 4 (b₂, b₃ = interface bits) change basins

### Element transition matrix (all line changes)

   from\to    Wood    Fire   Earth   Metal   Water
  ------------------------------------------------
      Wood       0      16      32      32      16
      Fire      16       0      16      16       0
     Earth      32      16      32       0      16
     Metal      32      16       0      32      16
     Water      16       0      16      16       0

## Task 2: Palace Structure (京房八宮)

Total unique hexagrams: 64 (partition verified: True)

### All 8 palaces

Masks (cumulative XOR from root):
  本宮  : 000000 (none)
  一世  : 000001 (b0)
  二世  : 000011 (b0, b1)
  三世  : 000111 (b0, b1, b2)
  四世  : 001111 (b0, b1, b2, b3)
  五世  : 011111 (b0, b1, b2, b3, b4)
  游魂  : 010111 (b0, b1, b2, b4)
  歸魂  : 010000 (b4)

### 坤宮 (Earth)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 000000    2          Kun   坤/  坤  Earth  Earth     比和    Kun  6
    一世 000001   24           Fu   震/  坤   Wood  Earth    体克用    Kun  1
    二世 000011   19          Lin   兌/  坤  Metal  Earth     生体    Kun  2
    三世 000111   11          Tai   乾/  坤  Metal  Earth     生体  KanLi  3
    四世 001111   34    Da Zhuang   乾/  震  Metal   Wood    体克用   Qian  4
    五世 011111   43         Guai   乾/  兌  Metal  Metal     比和   Qian  5
    游魂 010111    5           Xu   乾/  坎  Metal  Water    体生用  KanLi  4
    歸魂 010000    8           Bi   坤/  坎  Earth  Water    体克用    Kun  3

### 震宮 (Wood)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 001001   51         Zhen   震/  震   Wood   Wood     比和  KanLi  6
    一世 001000   16           Yu   坤/  震  Earth   Wood     克体  KanLi  1
    二世 001010   40          Xie   坎/  震  Water   Wood    体生用  KanLi  2
    三世 001110   32         Heng   巽/  震   Wood   Wood     比和   Qian  3
    四世 000110   46        Sheng   巽/  坤   Wood  Earth    体克用  KanLi  4
    五世 010110   48         Jing   巽/  坎   Wood  Water     生体  KanLi  5
    游魂 011110   28       Da Guo   巽/  兌   Wood  Metal     克体   Qian  4
    歸魂 011001   17          Sui   震/  兌   Wood  Metal     克体  KanLi  3

### 坎宮 (Water)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 010010   29          Kan   坎/  坎  Water  Water     比和    Kun  6
    一世 010011   60          Jie   兌/  坎  Metal  Water    体生用    Kun  1
    二世 010001    3         Zhun   震/  坎   Wood  Water     生体    Kun  2
    三世 010101   63        Ji Ji   離/  坎   Fire  Water     克体  KanLi  3
    四世 011101   49           Ge   離/  兌   Fire  Metal    体克用   Qian  4
    五世 001101   55         Feng   離/  震   Fire   Wood     生体   Qian  5
    游魂 000101   36      Ming Yi   離/  坤   Fire  Earth    体生用  KanLi  4
    歸魂 000010    7          Shi   坎/  坤  Water  Earth     克体    Kun  3

### 兌宮 (Metal)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 011011   58          Dui   兌/  兌  Metal  Metal     比和  KanLi  6
    一世 011010   47          Kun   坎/  兌  Water  Metal     生体  KanLi  1
    二世 011000   45          Cui   坤/  兌  Earth  Metal    体生用  KanLi  2
    三世 011100   31         Xian   艮/  兌  Earth  Metal    体生用   Qian  3
    四世 010100   39         Jian   艮/  坎  Earth  Water    体克用  KanLi  4
    五世 000100   15         Qian   艮/  坤  Earth  Earth     比和  KanLi  5
    游魂 001100   62     Xiao Guo   艮/  震  Earth   Wood     克体   Qian  4
    歸魂 001011   54      Gui Mei   兌/  震  Metal   Wood    体克用  KanLi  3

### 艮宮 (Earth)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 100100   52          Gen   艮/  艮  Earth  Earth     比和  KanLi  6
    一世 100101   22           Bi   離/  艮   Fire  Earth    体生用  KanLi  1
    二世 100111   26       Da Chu   乾/  艮  Metal  Earth     生体  KanLi  2
    三世 100011   41          Sun   兌/  艮  Metal  Earth     生体    Kun  3
    四世 101011   38          Kui   兌/  離  Metal   Fire     克体  KanLi  4
    五世 111011   10           Lu   兌/  乾  Metal  Metal     比和  KanLi  5
    游魂 110011   61     Zhong Fu   兌/  巽  Metal   Wood    体克用    Kun  4
    歸魂 110100   53         Jian   艮/  巽  Earth   Wood     克体  KanLi  3

### 離宮 (Fire)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 101101   30           Li   離/  離   Fire   Fire     比和   Qian  6
    一世 101100   56           Lu   艮/  離  Earth   Fire     生体   Qian  1
    二世 101110   50         Ding   巽/  離   Wood   Fire    体生用   Qian  2
    三世 101010   64       Wei Ji   坎/  離  Water   Fire    体克用  KanLi  3
    四世 100010    4         Meng   坎/  艮  Water  Earth     克体    Kun  4
    五世 110010   59         Huan   坎/  巽  Water   Wood    体生用    Kun  5
    游魂 111010    6         Song   坎/  乾  Water  Metal     生体  KanLi  4
    歸魂 111101   13     Tong Ren   離/  乾   Fire  Metal    体克用   Qian  3

### 巽宮 (Wood)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 110110   57          Xun   巽/  巽   Wood   Wood     比和  KanLi  6
    一世 110111    9     Xiao Chu   乾/  巽  Metal   Wood    体克用  KanLi  1
    二世 110101   37      Jia Ren   離/  巽   Fire   Wood     生体  KanLi  2
    三世 110001   42           Yi   震/  巽   Wood   Wood     比和    Kun  3
    四世 111001   25      Wu Wang   震/  乾   Wood  Metal     克体  KanLi  4
    五世 101001   21       Shi He   震/  離   Wood   Fire    体生用  KanLi  5
    游魂 100001   27           Yi   震/  艮   Wood  Earth    体克用    Kun  4
    歸魂 100110   18           Gu   巽/  艮   Wood  Earth    体克用  KanLi  3

### 乾宮 (Metal)
  Rank     Hex  KW#         Name  Lo/ Up   Lo_E   Up_E    Rel  Basin  世
  --------------------------------------------------------------------------------
    本宮 111111    1         Qian   乾/  乾  Metal  Metal     比和   Qian  6
    一世 111110   44          Gou   巽/  乾   Wood  Metal     克体   Qian  1
    二世 111100   33          Dun   艮/  乾  Earth  Metal    体生用   Qian  2
    三世 111000   12           Pi   坤/  乾  Earth  Metal    体生用  KanLi  3
    四世 110000   20         Guan   坤/  巽  Earth   Wood     克体    Kun  4
    五世 100000   23           Bo   坤/  艮  Earth  Earth     比和    Kun  5
    游魂 101000   35          Jin   坤/  離  Earth   Fire     生体  KanLi  4
    歸魂 101111   14       Da You   乾/  離  Metal   Fire     克体   Qian  3

## Task 3: Palace Coordinate Projections

### Element pair trajectory (lo_elem, up_elem) by rank

      Palace         R0         R1         R2         R3         R4         R5         R6         R7
  ------------------------------------------------------------------------------------------
           坤      Ea/Ea      Wo/Ea      Me/Ea      Me/Ea      Me/Wo      Me/Me      Me/Wa      Ea/Wa
           震      Wo/Wo      Ea/Wo      Wa/Wo      Wo/Wo      Wo/Ea      Wo/Wa      Wo/Me      Wo/Me
           坎      Wa/Wa      Me/Wa      Wo/Wa      Fi/Wa      Fi/Me      Fi/Wo      Fi/Ea      Wa/Ea
           兌      Me/Me      Wa/Me      Ea/Me      Ea/Me      Ea/Wa      Ea/Ea      Ea/Wo      Me/Wo
           艮      Ea/Ea      Fi/Ea      Me/Ea      Me/Ea      Me/Fi      Me/Me      Me/Wo      Ea/Wo
           離      Fi/Fi      Ea/Fi      Wo/Fi      Wa/Fi      Wa/Ea      Wa/Wo      Wa/Me      Fi/Me
           巽      Wo/Wo      Me/Wo      Fi/Wo      Wo/Wo      Wo/Me      Wo/Fi      Wo/Ea      Wo/Ea
           乾      Me/Me      Wo/Me      Ea/Me      Ea/Me      Ea/Wo      Ea/Ea      Ea/Fi      Me/Fi

### Relation trajectory by rank

      Palace     R0     R1     R2     R3     R4     R5     R6     R7
  -----------------------------------------------------------------
           坤     比和     体克     生体     生体     体克     比和     体生     体克
           震     比和     克体     体生     比和     体克     生体     克体     克体
           坎     比和     体生     生体     克体     体克     生体     体生     克体
           兌     比和     生体     体生     体生     体克     比和     克体     体克
           艮     比和     体生     生体     生体     克体     比和     体克     克体
           離     比和     生体     体生     体克     克体     体生     生体     体克
           巽     比和     体克     生体     比和     克体     体生     体克     体克
           乾     比和     克体     体生     体生     克体     比和     生体     克体

  Distinct relation trajectories: 8

### Basin trajectory by rank

      Palace     R0     R1     R2     R3     R4     R5     R6     R7
  -----------------------------------------------------------------
           坤    Kun    Kun    Kun    Kan    Qia    Qia    Kan    Kun
           震    Kan    Kan    Kan    Qia    Kan    Kan    Qia    Kan
           坎    Kun    Kun    Kun    Kan    Qia    Qia    Kan    Kun
           兌    Kan    Kan    Kan    Qia    Kan    Kan    Qia    Kan
           艮    Kan    Kan    Kan    Kun    Kan    Kan    Kun    Kan
           離    Qia    Qia    Qia    Kan    Kun    Kun    Kan    Qia
           巽    Kan    Kan    Kan    Kun    Kan    Kan    Kun    Kan
           乾    Qia    Qia    Qia    Kan    Kun    Kun    Kan    Qia

  Distinct basin trajectories: 4

### V₄ orbit membership

      Palace  V₄ orbit IDs of 8 members
  ------------------------------------------------------------
           坤  [0, 1, 3, 7, 3, 1, 5, 2]
           震  [8, 4, 9, 13, 6, 17, 19, 18]
           坎  [15, 12, 14, 16, 14, 12, 5, 2]
           兌  [8, 17, 6, 13, 9, 4, 11, 10]
           艮  [8, 17, 6, 13, 9, 4, 11, 10]
           離  [15, 12, 14, 16, 14, 12, 5, 2]
           巽  [8, 4, 9, 13, 6, 17, 19, 18]
           乾  [0, 1, 3, 7, 3, 1, 5, 2]

  坤宮: 6 distinct V₄ orbits (of 8 members)
  震宮: 8 distinct V₄ orbits (of 8 members)
  坎宮: 6 distinct V₄ orbits (of 8 members)
  兌宮: 8 distinct V₄ orbits (of 8 members)
  艮宮: 8 distinct V₄ orbits (of 8 members)
  離宮: 6 distinct V₄ orbits (of 8 members)
  巽宮: 8 distinct V₄ orbits (of 8 members)
  乾宮: 6 distinct V₄ orbits (of 8 members)

## Task 4: 世 Line Position

    Rank   世 line  Claimed  Match
  -----------------------------------
      本宮        6        6      ✓
      一世        1        1      ✓
      二世        2        2      ✓
      三世        3        3      ✓
      四世        4        4      ✓
      五世        5        5      ✓
      游魂        4        4      ✓
      歸魂        3        3      ✓

  世 pattern: 6,1,2,3,4,5,4,3
  → Ascends through lines 1-5, then retraces: 4→3
  → 游魂 returns to 世=4 (interface), 歸魂 to 世=3 (interface)
  → 本宮 世=6 (top line = palace invariant bit b₅)

## Task 5: Palace Walk Algebra

### Bit-flip sequence

Masks as cumulative XOR from root:
  R0→R0: mask=000000, step XOR=000000, flip=none
  R1→R1: mask=000001, step XOR=000001, flip=[0]
  R2→R2: mask=000011, step XOR=000010, flip=[1]
  R3→R3: mask=000111, step XOR=000100, flip=[2]
  R4→R4: mask=001111, step XOR=001000, flip=[3]
  R5→R5: mask=011111, step XOR=010000, flip=[4]
  R6→R6: mask=010111, step XOR=001000, flip=[3]
  R7→R7: mask=010000, step XOR=000111, flip=[0, 1, 2]

  Sequential flips: b₀, b₁, b₂, b₃, b₄, b₃(un-flip), b₀b₁b₂(un-flip)
  → Drill in from outer to interface, continue to shell,
    partial retract (un-flip b₃), then bulk retract lower trigram

### Basin visitation by palace

  坤宮: visits 3 basins — ['Kun', 'Kun', 'Kun', 'KanLi', 'Qian', 'Qian', 'KanLi', 'Kun']
  震宮: visits 2 basins — ['KanLi', 'KanLi', 'KanLi', 'Qian', 'KanLi', 'KanLi', 'Qian', 'KanLi']
  坎宮: visits 3 basins — ['Kun', 'Kun', 'Kun', 'KanLi', 'Qian', 'Qian', 'KanLi', 'Kun']
  兌宮: visits 2 basins — ['KanLi', 'KanLi', 'KanLi', 'Qian', 'KanLi', 'KanLi', 'Qian', 'KanLi']
  艮宮: visits 2 basins — ['KanLi', 'KanLi', 'KanLi', 'Kun', 'KanLi', 'KanLi', 'Kun', 'KanLi']
  離宮: visits 3 basins — ['Qian', 'Qian', 'Qian', 'KanLi', 'Kun', 'Kun', 'KanLi', 'Qian']
  巽宮: visits 2 basins — ['KanLi', 'KanLi', 'KanLi', 'Kun', 'KanLi', 'KanLi', 'Kun', 'KanLi']
  乾宮: visits 3 basins — ['Qian', 'Qian', 'Qian', 'KanLi', 'Kun', 'Kun', 'KanLi', 'Qian']

  Palaces visiting 3 basins: 4 (坤, 坎, 離, 乾)
  Palaces visiting 2 basins: 4 (震, 兌, 艮, 巽)
  (KanLi-rooted palaces stay within KanLi + one other)

### Complement action on palaces

  Same palace under complement: 0/64
  Different palace: 64/64

  Palace → complement palace mapping:
    Dui ☱           → Gen ☶
    Gen ☶           → Dui ☱
    Kan ☵           → Li ☲
    Kun ☷           → Qian ☰
    Li ☲            → Kan ☵
    Qian ☰          → Kun ☷
    Xun ☴           → Zhen ☳
    Zhen ☳          → Xun ☴

### Reversal action on palaces

  Same palace under reversal: 8/64

  Palace → reversal palace mapping:
    Dui ☱           → Dui ☱, Gen ☶, Xun ☴, Zhen ☳
    Gen ☶           → Dui ☱, Gen ☶, Xun ☴, Zhen ☳
    Kan ☵           → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Kun ☷           → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Li ☲            → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Qian ☰          → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Xun ☴           → Dui ☱, Gen ☶, Xun ☴, Zhen ☳
    Zhen ☳          → Dui ☱, Gen ☶, Xun ☴, Zhen ☳

### Comp∘Rev action on palaces

  Palace → comp∘rev palace mapping:
    Dui ☱           → Dui ☱, Gen ☶, Xun ☴, Zhen ☳
    Gen ☶           → Dui ☱, Gen ☶, Xun ☴, Zhen ☳
    Kan ☵           → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Kun ☷           → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Li ☲            → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Qian ☰          → Kan ☵, Kun ☷, Li ☲, Qian ☰
    Xun ☴           → Dui ☱, Gen ☶, Xun ☴, Zhen ☳
    Zhen ☳          → Dui ☱, Gen ☶, Xun ☴, Zhen ☳

## Task 6: Palace Element vs 体 (Lower Trigram) Trajectory

### 体-element trajectory through 8 generations

      Palace P_elem      R0      R1      R2      R3      R4      R5      R6      R7
  ---------------------------------------------------------------------------
           坤    Ear     Ea*     Wo      Me      Me      Me      Me      Me      Ea*
           震    Woo     Wo*     Ea      Wa      Wo*     Wo*     Wo*     Wo*     Wo*
           坎    Wat     Wa*     Me      Wo      Fi      Fi      Fi      Fi      Wa*
           兌    Met     Me*     Wa      Ea      Ea      Ea      Ea      Ea      Me*
           艮    Ear     Ea*     Fi      Me      Me      Me      Me      Me      Ea*
           離    Fir     Fi*     Ea      Wo      Wa      Wa      Wa      Wa      Fi*
           巽    Woo     Wo*     Me      Fi      Wo*     Wo*     Wo*     Wo*     Wo*
           乾    Met     Me*     Wo      Ea      Ea      Ea      Ea      Ea      Me*

  (* = matches palace element)

### 体 = palace element by rank

    本宮: 8/8 palaces have 体=palace_element
    一世: 0/8 palaces have 体=palace_element
    二世: 0/8 palaces have 体=palace_element
    三世: 2/8 palaces have 体=palace_element
    四世: 2/8 palaces have 体=palace_element
    五世: 2/8 palaces have 体=palace_element
    游魂: 2/8 palaces have 体=palace_element
    歸魂: 8/8 palaces have 体=palace_element

  Pattern: 8/8 → decrease → 8/8 (歸魂 restores lower trigram)

  歸魂 restores lower trigram to palace root: 8/8

### 用-element trajectory through 8 generations

      Palace P_elem      R0      R1      R2      R3      R4      R5      R6      R7
  ---------------------------------------------------------------------------
           坤    Ear     Ea*     Ea*     Ea*     Ea*     Wo      Me      Wa      Wa 
           震    Woo     Wo*     Wo*     Wo*     Wo*     Ea      Wa      Me      Me 
           坎    Wat     Wa*     Wa*     Wa*     Wa*     Me      Wo      Ea      Ea 
           兌    Met     Me*     Me*     Me*     Me*     Wa      Ea      Wo      Wo 
           艮    Ear     Ea*     Ea*     Ea*     Ea*     Fi      Me      Wo      Wo 
           離    Fir     Fi*     Fi*     Fi*     Fi*     Ea      Wo      Me      Me 
           巽    Woo     Wo*     Wo*     Wo*     Wo*     Me      Fi      Ea      Ea 
           乾    Met     Me*     Me*     Me*     Me*     Wo      Ea      Fi      Fi 

  用=palace_element by rank:
      本宮: 8/8
      一世: 8/8
      二世: 8/8
      三世: 8/8
      四世: 0/8
      五世: 0/8
      游魂: 0/8
      歸魂: 0/8

## Summary

### Single-change graph
  • Lines 1-3 (lower trigram) change 体 element; lines 4-6 change 用
  • Only lines 3 and 4 (interface bits b₂, b₃) change basins
  • Lines 1,2,4,5: ALWAYS change element (100%)
    Lines 3,6: change element 50% (these are the top bit of each trigram)
    → b₂ and b₅ determine which element-pair within a fiber

### Palace structure
  • 8 palaces × 8 ranks = 64 (verified partition)
  • 世 pattern: [6, 1, 2, 3, 4, 5, 4, 3] (ascend 6,1-5, retrace 4,3)
  • b₅ (line 6) never flipped → palace invariant
  • Palaces visiting 3 basins: 4; visiting 2: 4
  • 歸魂 restores lower trigram: 8/8

### V₄ × palace interaction
  • Complement: 0/64 same-palace (crosses most boundaries)
  • Reversal: 8/64 same-palace
  • Comp∘Rev: 24/64 same-palace

### Palace walk as onion traversal
  R0(本宮) → R1(outer) → R2(shell) → R3(interface) →
  R4(full core) → R5(all inner) → R6(partial retract) → R7(shell only)
  The walk drills inward then partially retracts.
  Basin changes occur exactly at ranks 3 and 6 (interface bit toggles).

### 体/用 element trajectories
  • 体 (lower): departs from palace element at R1, fully changed by R3,
    restored at R7 (歸魂)
  • 用 (upper): preserved through R0-R3 (lines 4-6 not yet flipped),
    departs at R4, partially restored at R6 (游魂)
  • The palace walk systematically explores all element combinations
    reachable from the root, then returns the 体 to its origin
