# V₄ Symmetry Group on Z₂⁶

## Verification: V₄ = {id, comp, rev, comp∘rev}

Checking group axioms on all 64 hexagrams:
  comp² = id ✓
  rev² = id ✓
  (comp∘rev)² = id ✓
  comp∘rev = rev∘comp ✓ (V₄ is abelian)

## Task 1: Fixed Points and Orbits

Fixed points of complement: 0
Fixed points of reversal: 8
  000000 = #2 Kun (坤/坤)
  001100 = #62 Xiao Guo (艮/震)
  010010 = #29 Kan (坎/坎)
  011110 = #28 Da Guo (巽/兌)
  100001 = #27 Yi (震/艮)
  101101 = #30 Li (離/離)
  110011 = #61 Zhong Fu (兌/巽)
  111111 = #1 Qian (乾/乾)
Fixed points of comp∘rev: 8
  000111 = #11 Tai (乾/坤)
  001011 = #54 Gui Mei (兌/震)
  010101 = #63 Ji Ji (離/坎)
  011001 = #17 Sui (震/兌)
  100110 = #18 Gu (巽/艮)
  101010 = #64 Wei Ji (坎/離)
  110100 = #53 Jian (艮/巽)
  111000 = #12 Pi (坤/乾)

Total V₄ orbits: 20
Orbit size distribution: {2: 8, 4: 12}
  Size 1: 0 (fixed by all three involutions)
  Size 2: 8 (fixed by one involution)
  Size 4: 12 (generic)

### All V₄ orbits

#### Size-2 orbits (8 total)

  1. #2 Kun, #1 Qian
     000000, 111111 | stab={rev}
  2. #11 Tai, #12 Pi
     000111, 111000 | stab={c∘r}
  3. #54 Gui Mei, #53 Jian
     001011, 110100 | stab={c∘r}
  4. #62 Xiao Guo, #61 Zhong Fu
     001100, 110011 | stab={rev}
  5. #29 Kan, #30 Li
     010010, 101101 | stab={rev}
  6. #63 Ji Ji, #64 Wei Ji
     010101, 101010 | stab={c∘r}
  7. #17 Sui, #18 Gu
     011001, 100110 | stab={c∘r}
  8. #28 Da Guo, #27 Yi
     011110, 100001 | stab={rev}

#### Size-4 orbits (12 total)

  1. #24 Fu, #43 Guai, #23 Bo, #44 Gou
     000001, 011111, 100000, 111110
  2. #7 Shi, #8 Bi, #14 Da You, #13 Tong Ren
     000010, 010000, 101111, 111101
  3. #19 Lin, #34 Da Zhuang, #20 Guan, #33 Dun
     000011, 001111, 110000, 111100
  4. #15 Qian, #16 Yu, #9 Xiao Chu, #10 Lu
     000100, 001000, 110111, 111011
  5. #36 Ming Yi, #5 Xu, #35 Jin, #6 Song
     000101, 010111, 101000, 111010
  6. #46 Sheng, #45 Cui, #26 Da Chu, #25 Wu Wang
     000110, 011000, 100111, 111001
  7. #51 Zhen, #58 Dui, #52 Gen, #57 Xun
     001001, 011011, 100100, 110110
  8. #40 Xie, #39 Jian, #38 Kui, #37 Jia Ren
     001010, 010100, 101011, 110101
  9. #55 Feng, #60 Jie, #56 Lu, #59 Huan
     001101, 010011, 101100, 110010
  10. #32 Heng, #31 Xian, #41 Sun, #42 Yi
     001110, 011100, 100011, 110001
  11. #3 Zhun, #49 Ge, #4 Meng, #50 Ding
     010001, 011101, 100010, 101110
  12. #48 Jing, #47 Kun, #22 Bi, #21 Shi He
     010110, 011010, 100101, 101001

### Size-4 orbit detail

Orbit       h    comp     rev     c∘r        Name_h    Name_comp     Name_rev      Name_cr
--------------------------------------------------------------------------------------------------------------
    1 000001 111110 100000 011111            Fu          Gou           Bo         Guai
    2 000010 111101 010000 101111           Shi     Tong Ren           Bi       Da You
    3 000011 111100 110000 001111           Lin          Dun         Guan    Da Zhuang
    4 000100 111011 001000 110111          Qian           Lu           Yu     Xiao Chu
    5 000101 111010 101000 010111       Ming Yi         Song          Jin           Xu
    6 000110 111001 011000 100111         Sheng      Wu Wang          Cui       Da Chu
    7 001001 110110 100100 011011          Zhen          Xun          Gen          Dui
    8 001010 110101 010100 101011           Xie      Jia Ren         Jian          Kui
    9 001101 110010 101100 010011          Feng         Huan           Lu          Jie
   10 001110 110001 011100 100011          Heng           Yi         Xian          Sun
   11 010001 101110 100010 011101          Zhun         Ding         Meng           Ge
   12 010110 101001 011010 100101          Jing       Shi He          Kun           Bi

## Task 2: V₄ Action on Coordinate Systems

### 2a: V₄ action on elements

Complement on trigrams → elements:
  坤(Earth) → 乾(Metal)
  震(Wood) → 巽(Wood)
  坎(Water) → 離(Fire)
  兌(Metal) → 艮(Earth)
  艮(Earth) → 兌(Metal)
  離(Fire) → 坎(Water)
  巽(Wood) → 震(Wood)
  乾(Metal) → 坤(Earth)
  Fiber-preserving: True
  Induced Z₅ permutation: {'Earth': 'Metal', 'Wood': 'Wood', 'Water': 'Fire', 'Metal': 'Earth', 'Fire': 'Water'}
  Is negation (-x mod 5): True

Reversal on trigrams → elements:
  坤(Earth) → 坤(Earth)
  震(Wood) → 艮(Earth)
  坎(Water) → 坎(Water)
  兌(Metal) → 巽(Wood)
  艮(Earth) → 震(Wood)
  離(Fire) → 離(Fire)
  巽(Wood) → 兌(Metal)
  乾(Metal) → 乾(Metal)
  Fiber-preserving: False
  Fiber map (showing multi-valued):
    Earth → {'Earth', 'Wood'}
    Fire → {'Fire'}
    Metal → {'Metal', 'Wood'}
    Water → {'Water'}
    Wood → {'Metal', 'Earth'}

Comp∘Rev on trigrams → elements:
  坤(Earth) → 乾(Metal)
  震(Wood) → 兌(Metal)
  坎(Water) → 離(Fire)
  兌(Metal) → 震(Wood)
  艮(Earth) → 巽(Wood)
  離(Fire) → 坎(Water)
  巽(Wood) → 艮(Earth)
  乾(Metal) → 坤(Earth)
  Fiber-preserving: False
  Fiber map:
    Earth → {'Metal', 'Wood'}
    Fire → {'Water'}
    Metal → {'Earth', 'Wood'}
    Water → {'Fire'}
    Wood → {'Metal', 'Earth'}

### 2b: V₄ action on directed relations

  complement:
    体克用 → {'克体'}
    体生用 → {'生体'}
    克体 → {'体克用'}
    比和 → {'比和'}
    生体 → {'体生用'}
    Well-defined on relations: True

  reversal:
    体克用 ⇒ {'比和', '体生用', '体克用', '克体'}
    体生用 ⇒ {'体生用', '生体', '比和', '体克用'}
    克体 ⇒ {'生体', '比和', '克体', '体克用'}
    比和 ⇒ {'比和', '克体', '体生用', '体克用', '生体'}
    生体 ⇒ {'生体', '克体', '体生用', '比和'}
    Well-defined on relations: False

  comp∘rev:
    体克用 ⇒ {'比和', '生体', '体克用', '克体'}
    体生用 ⇒ {'生体', '克体', '体生用', '比和'}
    克体 ⇒ {'克体', '体生用', '比和', '体克用'}
    比和 ⇒ {'比和', '体生用', '克体', '体克用', '生体'}
    生体 ⇒ {'体生用', '生体', '比和', '体克用'}
    Well-defined on relations: False

### 2c: V₄ action on basins

  complement:
    Kun → {'Qian'}
    KanLi → {'KanLi'}
    Qian → {'Kun'}
    Preserves basins: False

  reversal:
    Kun → {'Kun'}
    KanLi → {'KanLi'}
    Qian → {'Qian'}
    Preserves basins: True

  comp∘rev:
    Kun → {'Qian'}
    KanLi → {'KanLi'}
    Qian → {'Kun'}
    Preserves basins: False

### 2d: V₄ action on 互

  complement commutes with 互: True
  reversal commutes with 互: True
  comp∘rev commutes with 互: True

## Task 3: V₄ and the Element System (Detailed)

### Reversal fiber analysis

Reversal on trigrams:
  Fixed: 坤(000→000,Earth), 坎(010→010,Water), 離(101→101,Fire), 乾(111→111,Metal)
  Swapped: 震(001)↔艮(100): Wood↔Earth
           巽(110)↔兌(011): Wood↔Metal

Element-level effect:
  Water → Water (fixed, singleton)
  Fire → Fire (fixed, singleton)
  Earth → {Earth, Wood} (Gen stays Earth, Kun stays Earth, but Zhen(Wood)→Gen(Earth))
  Metal → {Metal, Wood} (Qian stays Metal, Dui stays Metal, but Xun(Wood)→Dui(Metal))
  Wood → {Earth, Metal} (Zhen→Gen=Earth, Xun→Dui=Metal)

Reversal is NOT fiber-preserving. Wood splits into Earth and Metal.
But it IS fiber-preserving on the SINGLETON elements (Fire, Water).
The singletons are the injection points of the Z₂→Z₅ map —
reversal respects them because they have no fiber ambiguity.

### Reversal on hexagrams: upper/lower swap

For hexagram h with lower=L, upper=U:
  rev(h) has lower=rev_trig(U), upper=rev_trig(L)
  This swaps upper↔lower AND reverses trigram bits.

  Verified: rev(lo,up) = (rev_trig(up), rev_trig(lo)) for all 64: True

### Reversal effect on directed relation

If lo_elem and up_elem are both singletons (Fire or Water),
reversal preserves both elements → relation is determined by
swapping upper↔lower → relation inverts (生体↔体生用, 克体↔体克用, 比和→比和).

  Reversal inverts relation: 24/64
  (Expected if reversal = perfect upper/lower swap: 64/64)

  Failures (reversal ≠ simple relation inversion):
    000001 (Wood/Earth → 体克用) → rev (Earth/Earth → 比和), expected 克体
    000011 (Metal/Earth → 生体) → rev (Earth/Wood → 克体), expected 体生用
    000100 (Earth/Earth → 比和) → rev (Earth/Wood → 克体), expected 比和
    000110 (Wood/Earth → 体克用) → rev (Earth/Metal → 体生用), expected 克体
    001000 (Earth/Wood → 克体) → rev (Earth/Earth → 比和), expected 体克用
    001010 (Water/Wood → 体生用) → rev (Earth/Water → 体克用), expected 生体
    001100 (Earth/Wood → 克体) → rev (Earth/Wood → 克体), expected 体克用
    001101 (Fire/Wood → 生体) → rev (Earth/Fire → 生体), expected 体生用
    001110 (Wood/Wood → 比和) → rev (Earth/Metal → 体生用), expected 比和
    001111 (Metal/Wood → 体克用) → rev (Earth/Metal → 体生用), expected 克体
    010001 (Wood/Water → 生体) → rev (Water/Earth → 克体), expected 体生用
    010011 (Metal/Water → 体生用) → rev (Water/Wood → 体生用), expected 生体
    010100 (Earth/Water → 体克用) → rev (Water/Wood → 体生用), expected 克体
    010110 (Wood/Water → 生体) → rev (Water/Metal → 生体), expected 体生用
    011000 (Earth/Metal → 体生用) → rev (Wood/Earth → 体克用), expected 生体
    011010 (Water/Metal → 生体) → rev (Wood/Water → 生体), expected 体生用
    011100 (Earth/Metal → 体生用) → rev (Wood/Wood → 比和), expected 生体
    011101 (Fire/Metal → 体克用) → rev (Wood/Fire → 体生用), expected 克体
    011110 (Wood/Metal → 克体) → rev (Wood/Metal → 克体), expected 体克用
    011111 (Metal/Metal → 比和) → rev (Wood/Metal → 克体), expected 比和
    100000 (Earth/Earth → 比和) → rev (Wood/Earth → 体克用), expected 比和
    100001 (Wood/Earth → 体克用) → rev (Wood/Earth → 体克用), expected 克体
    100010 (Water/Earth → 克体) → rev (Wood/Water → 生体), expected 体克用
    100011 (Metal/Earth → 生体) → rev (Wood/Wood → 比和), expected 体生用
    100101 (Fire/Earth → 体生用) → rev (Wood/Fire → 体生用), expected 生体
    100111 (Metal/Earth → 生体) → rev (Wood/Metal → 克体), expected 体生用
    101001 (Wood/Fire → 体生用) → rev (Fire/Earth → 体生用), expected 生体
    101011 (Metal/Fire → 克体) → rev (Fire/Wood → 生体), expected 体克用
    101100 (Earth/Fire → 生体) → rev (Fire/Wood → 生体), expected 体生用
    101110 (Wood/Fire → 体生用) → rev (Fire/Metal → 体克用), expected 生体
    110000 (Earth/Wood → 克体) → rev (Metal/Earth → 生体), expected 体克用
    110001 (Wood/Wood → 比和) → rev (Metal/Earth → 生体), expected 比和
    110010 (Water/Wood → 体生用) → rev (Metal/Water → 体生用), expected 生体
    110011 (Metal/Wood → 体克用) → rev (Metal/Wood → 体克用), expected 克体
    110101 (Fire/Wood → 生体) → rev (Metal/Fire → 克体), expected 体生用
    110111 (Metal/Wood → 体克用) → rev (Metal/Metal → 比和), expected 克体
    111001 (Wood/Metal → 克体) → rev (Metal/Earth → 生体), expected 体克用
    111011 (Metal/Metal → 比和) → rev (Metal/Wood → 体克用), expected 比和
    111100 (Earth/Metal → 体生用) → rev (Metal/Wood → 体克用), expected 生体
    111110 (Wood/Metal → 克体) → rev (Metal/Metal → 比和), expected 体克用

## Task 4: V₄ and the KW Sequence

  complement preserves KW pairing: True
    Fixed pairs: 8/32
    Cycle structure on pairs: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
  reversal preserves KW pairing: True
    Fixed pairs: 32/32
    Cycle structure on pairs: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  comp∘rev preserves KW pairing: True
    Fixed pairs: 8/32
    Cycle structure on pairs: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]

### V₄ orbits on KW pairs

Total V₄ orbits on KW pairs: 20
Pair orbit sizes: {1: 8, 2: 12}

  1. P1(Qian/Kun)
  2. P2(Zhun/Meng), P25(Ge/Ding)
  3. P3(Xu/Song), P18(Jin/Ming Yi)
  4. P4(Shi/Bi), P7(Tong Ren/Da You)
  5. P5(Xiao Chu/Lu), P8(Qian/Yu)
  6. P6(Tai/Pi)
  7. P9(Sui/Gu)
  8. P10(Lin/Guan), P17(Dun/Da Zhuang)
  9. P11(Shi He/Bi), P24(Kun/Jing)
  10. P12(Bo/Fu), P22(Guai/Gou)
  11. P13(Wu Wang/Da Chu), P23(Cui/Sheng)
  12. P14(Yi/Da Guo)
  13. P15(Kan/Li)
  14. P16(Xian/Heng), P21(Sun/Yi)
  15. P19(Jia Ren/Kui), P20(Jian/Xie)
  16. P26(Zhen/Gen), P29(Xun/Dui)
  17. P27(Jian/Gui Mei)
  18. P28(Feng/Lu), P30(Huan/Jie)
  19. P31(Zhong Fu/Xiao Guo)
  20. P32(Ji Ji/Wei Ji)

## Task 5: V₄ Orbits and 上經/下經

Hexagram orbit locations:
  Entirely in 上經: 7
  Entirely in 下經: 7
  Split across both: 6

Pair orbit locations:
  Entirely in 上經: 7
  Entirely in 下經: 7
  Split: 6

### Split pair orbits (connecting 上經 ↔ 下經)

  P2[上](Zhun/Meng), P25[下](Ge/Ding)
  P3[上](Xu/Song), P18[下](Jin/Ming Yi)
  P10[上](Lin/Guan), P17[下](Dun/Da Zhuang)
  P11[上](Shi He/Bi), P24[下](Kun/Jing)
  P12[上](Bo/Fu), P22[下](Guai/Gou)
  P13[上](Wu Wang/Da Chu), P23[下](Cui/Sheng)

## Task 6: Comp∘Rev — The Third Involution

### Fixed points of comp∘rev

comp∘rev(h) = h requires: b₅=1-b₀, b₄=1-b₁, b₃=1-b₂
Three free bits (b₀,b₁,b₂) → 8 fixed points

 Binary  KW#         Name  Lo  Up   Lo_E   Up_E    Rel  Basin Yang
---------------------------------------------------------------------------
000111   11          Tai   乾   坤  Metal  Earth     生体  KanLi    3
001011   54      Gui Mei   兌   震  Metal   Wood    体克用  KanLi    3
010101   63        Ji Ji   離   坎   Fire  Water     克体  KanLi    3
011001   17          Sui   震   兌   Wood  Metal     克体  KanLi    3
100110   18           Gu   巽   艮   Wood  Earth    体克用  KanLi    3
101010   64       Wei Ji   坎   離  Water   Fire    体克用  KanLi    3
110100   53         Jian   艮   巽  Earth   Wood     克体  KanLi    3
111000   12           Pi   坤   乾  Earth  Metal    体生用  KanLi    3

Yang line counts: [3, 3, 3, 3, 3, 3, 3, 3]
  All have exactly 3 yang lines: True

Total hexagrams with 3 yang lines: 20
Of which, comp∘rev-fixed: 8
Fraction: 8/20

Relations among cr-fixed: {'生体': 1, '体克用': 3, '克体': 3, '体生用': 1}

Basins among cr-fixed: {'KanLi': 8}

### Structural characterization

comp∘rev fixed means: the hexagram read backwards with all lines flipped
equals itself. This is an 'anti-palindrome' — a figure that is its own
complement-reversal.

Binary structure of comp∘rev-fixed hexagrams:
  b₀b₁b₂ | b₃b₄b₅ where b₃=1-b₂, b₄=1-b₁, b₅=1-b₀
  → lower trigram determines upper trigram as comp∘rev(lower)

  000111: lo=111(乾), up=000(坤), comp∘rev(lo)=000(坤), up == comp∘rev(lo): True
  001011: lo=011(兌), up=001(震), comp∘rev(lo)=001(震), up == comp∘rev(lo): True
  010101: lo=101(離), up=010(坎), comp∘rev(lo)=010(坎), up == comp∘rev(lo): True
  011001: lo=001(震), up=011(兌), comp∘rev(lo)=011(兌), up == comp∘rev(lo): True
  100110: lo=110(巽), up=100(艮), comp∘rev(lo)=100(艮), up == comp∘rev(lo): True
  101010: lo=010(坎), up=101(離), comp∘rev(lo)=101(離), up == comp∘rev(lo): True
  110100: lo=100(艮), up=110(巽), comp∘rev(lo)=110(巽), up == comp∘rev(lo): True
  111000: lo=000(坤), up=111(乾), comp∘rev(lo)=111(乾), up == comp∘rev(lo): True

### Traditional significance

  既濟 (#63) in cr-fixed: True
  未濟 (#64) in cr-fixed: True

  KW pairs containing cr-fixed hexagrams: [6, 9, 27, 32]

## Summary

### V₄ orbit structure
  20 orbits total: 0 size-1, 8 size-2, 12 size-4
  Fixed points: comp=0, rev=8 (palindromes), comp∘rev=8 (anti-palindromes)

### Fiber preservation
  Complement: preserves element fibers ✓ (acts as -x mod 5 on Z₅)
  Reversal: does NOT preserve fibers (Wood → {Earth, Metal})
  Comp∘Rev: does NOT preserve fibers
  → Only complement descends to Z₅. Reversal is purely Z₂.

### Directed relation action
  Complement: well-defined on relations
  Reversal: inverts relation direction for 24/64 hexagrams

### KW sequence compatibility
  All three involutions preserve KW pairing: ✓
  V₄ orbits on KW pairs: 20
  Pair orbits split: {'上經': 7, '下經': 7, 'split': 6}

### Anti-palindromes (comp∘rev-fixed)
  8 hexagrams where h = complement(reverse(h))
  All have exactly 3 yang lines (balanced yin/yang)
  Include 既濟 and 未濟 (the 互 cycle attractors)
  Lower trigram uniquely determines upper as comp∘rev(lower)
