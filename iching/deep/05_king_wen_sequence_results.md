# King Wen Sequence Analysis

## Task 1: King Wen Sequence Encoding

Verified: KW is a permutation of 0-63 (all 64 hexagrams)

 KW#         Name     Bin  Dec  Lo  Up   Lo_E   Up_E
------------------------------------------------------------
   1         Qian 111111   63   乾   乾  Metal  Metal
   2          Kun 000000    0   坤   坤  Earth  Earth
   3         Zhun 010001   17   震   坎   Wood  Water
   4         Meng 100010   34   坎   艮  Water  Earth
   5           Xu 010111   23   乾   坎  Metal  Water
  29          Kan 010010   18   坎   坎  Water  Water
  30           Li 101101   45   離   離   Fire   Fire
  63        Ji Ji 010101   21   離   坎   Fire  Water
  64       Wei Ji 101010   42   坎   離  Water   Fire

## Task 2: Pairing Structure

Pair type distribution (32 pairs):
  both: 4
  complement: 4
  neither: 0
  reversal: 24
  Palindromes (self-reversing): 4

Traditional claim: pairs are reversal-pairs except palindromes → complement
  Reversal pairs (incl. both): 28
  Complement-only pairs: 4
  Complement-only pairs are palindromes?
    #1/2 (Qian/Kun): palindrome=True
    #27/28 (Yi/Da Guo): palindrome=True
    #29/30 (Kan/Li): palindrome=True
    #61/62 (Zhong Fu/Xiao Guo): palindrome=True

### All 32 pairs
Pair  #a-#b        Name_a       Name_b         Type Palindrome
----------------------------------------------------------------------
   1   1-2           Qian          Kun   complement          ✓
   2   3-4           Zhun         Meng     reversal           
   3   5-6             Xu         Song     reversal           
   4   7-8            Shi           Bi     reversal           
   5   9-10      Xiao Chu           Lu     reversal           
   6  11-12           Tai           Pi         both           
   7  13-14      Tong Ren       Da You     reversal           
   8  15-16          Qian           Yu     reversal           
   9  17-18           Sui           Gu         both           
  10  19-20           Lin         Guan     reversal           
  11  21-22        Shi He           Bi     reversal           
  12  23-24            Bo           Fu     reversal           
  13  25-26       Wu Wang       Da Chu     reversal           
  14  27-28            Yi       Da Guo   complement          ✓
  15  29-30           Kan           Li   complement          ✓
  16  31-32          Xian         Heng     reversal           
  17  33-34           Dun    Da Zhuang     reversal           
  18  35-36           Jin      Ming Yi     reversal           
  19  37-38       Jia Ren          Kui     reversal           
  20  39-40          Jian          Xie     reversal           
  21  41-42           Sun           Yi     reversal           
  22  43-44          Guai          Gou     reversal           
  23  45-46           Cui        Sheng     reversal           
  24  47-48           Kun         Jing     reversal           
  25  49-50            Ge         Ding     reversal           
  26  51-52          Zhen          Gen     reversal           
  27  53-54          Jian      Gui Mei         both           
  28  55-56          Feng           Lu     reversal           
  29  57-58           Xun          Dui     reversal           
  30  59-60          Huan          Jie     reversal           
  31  61-62      Zhong Fu     Xiao Guo   complement          ✓
  32  63-64         Ji Ji       Wei Ji         both           

## Task 3: Full Coordinate Projection

 KW       Name     Bin   Lo_E   Up_E    Rel  Basin   SY Comp
-----------------------------------------------------------------
  1       Qian 111111  Metal  Metal     比和   Qian   14    2
  2        Kun 000000  Earth  Earth     比和    Kun    0    1
  3       Zhun 010001   Wood  Water     生体    Kun    6   50
  4       Meng 100010  Water  Earth     克体    Kun    3   49
  5         Xu 010111  Metal  Water    体生用  KanLi    9   35
  6       Song 111010  Water  Metal     生体  KanLi    9   36
  7        Shi 000010  Water  Earth     克体    Kun    2   13
  8         Bi 010000  Earth  Water    体克用    Kun    2   14
  9   Xiao Chu 110111  Metal   Wood    体克用  KanLi   10   16
 10         Lu 111011  Metal  Metal     比和  KanLi   13   15
 11        Tai 000111  Metal  Earth     生体  KanLi    7   12
 12         Pi 111000  Earth  Metal    体生用  KanLi    7   11
 13   Tong Ren 111101   Fire  Metal    体克用   Qian   12    7
 14     Da You 101111  Metal   Fire     克体   Qian   12    8
 15       Qian 000100  Earth  Earth     比和  KanLi    1   10
 16         Yu 001000  Earth   Wood     克体  KanLi    4    9
 17        Sui 011001   Wood  Metal     克体  KanLi   10   18
 18         Gu 100110   Wood  Earth    体克用  KanLi    4   17
 19        Lin 000011  Metal  Earth     生体    Kun    6   33
 20       Guan 110000  Earth   Wood     克体    Kun    3   34
 21     Shi He 101001   Wood   Fire    体生用  KanLi    9   48
 22         Bi 100101   Fire  Earth    体生用  KanLi    6   47
 23         Bo 100000  Earth  Earth     比和    Kun    1   43
 24         Fu 000001   Wood  Earth    体克用    Kun    4   44
 25    Wu Wang 111001   Wood  Metal     克体  KanLi   11   46
 26     Da Chu 100111  Metal  Earth     生体  KanLi    8   45
 27         Yi 100001   Wood  Earth    体克用    Kun    5   28
 28     Da Guo 011110   Wood  Metal     克体   Qian    9   27
 29        Kan 010010  Water  Water     比和    Kun    4   30
 30         Li 101101   Fire   Fire     比和   Qian   10   29
 31       Xian 011100  Earth  Metal    体生用   Qian    7   41
 32       Heng 001110   Wood   Wood     比和   Qian    7   42
 33        Dun 111100  Earth  Metal    体生用   Qian    8   19
 34  Da Zhuang 001111  Metal   Wood    体克用   Qian   11   20
 35        Jin 101000  Earth   Fire     生体  KanLi    5    5
 36    Ming Yi 000101   Fire  Earth    体生用  KanLi    5    6
 37    Jia Ren 110101   Fire   Wood     生体  KanLi    8   40
 38        Kui 101011  Metal   Fire     克体  KanLi   11   39
 39       Jian 010100  Earth  Water    体克用  KanLi    3   38
 40        Xie 001010  Water   Wood    体生用  KanLi    6   37
 41        Sun 100011  Metal  Earth     生体    Kun    7   31
 42         Yi 110001   Wood   Wood     比和    Kun    7   32
 43       Guai 011111  Metal  Metal     比和   Qian   13   23
 44        Gou 111110   Wood  Metal     克体   Qian   10   24
 45        Cui 011000  Earth  Metal    体生用  KanLi    6   26
 46      Sheng 000110   Wood  Earth    体克用  KanLi    3   25
 47        Kun 011010  Water  Metal     生体  KanLi    8   22
 48       Jing 010110   Wood  Water     生体  KanLi    5   21
 49         Ge 011101   Fire  Metal    体克用   Qian   11    4
 50       Ding 101110   Wood   Fire    体生用   Qian    8    3
 51       Zhen 001001   Wood   Wood     比和  KanLi    8   57
 52        Gen 100100  Earth  Earth     比和  KanLi    2   58
 53       Jian 110100  Earth   Wood     克体  KanLi    4   54
 54    Gui Mei 001011  Metal   Wood    体克用  KanLi   10   53
 55       Feng 001101   Fire   Wood     生体   Qian    9   59
 56         Lu 101100  Earth   Fire     生体   Qian    6   60
 57        Xun 110110   Wood   Wood     比和  KanLi    6   51
 58        Dui 011011  Metal  Metal     比和  KanLi   12   52
 59       Huan 110010  Water   Wood    体生用    Kun    5   55
 60        Jie 010011  Metal  Water    体生用    Kun    8   56
 61   Zhong Fu 110011  Metal   Wood    体克用    Kun    9   62
 62   Xiao Guo 001100  Earth   Wood     克体   Qian    5   61
 63      Ji Ji 010101   Fire  Water     克体  KanLi    7   64
 64     Wei Ji 101010  Water   Fire    体克用  KanLi    7   63

## Task 4: Sequential Structure

### 4a: Hamming distance between consecutive hexagrams

  Mean consecutive Hamming distance: 3.349
  Distribution: {1: 2, 2: 20, 3: 13, 4: 19, 6: 9}
  Null mean: 3.049
  p-value (KW ≤ null): 0.9815
  Not significant

### 4b: Z₅×Z₅ torus path

  Distinct cells visited: 25/25
  Visit distribution: {1: 4, 2: 12, 4: 9}
  Mean torus step (|Δlo|+|Δup| on Z₅): 2.444
  Null mean torus step: 2.413
  p-value: 0.6178
  Not significant

### 4c: Directed relation sequence

  Relation distribution: {'体克用': 13, '体生用': 12, '克体': 13, '比和': 14, '生体': 12}
  Number of relation-runs: 52
  Mean run length: 1.23
  Max run length: 2

### 4d: Shao Yong (先天) correlation

  Pearson correlation (KW# vs SY sum): 0.0634
  Weak/none

### 4e: Basin transitions

  Basin distribution: {-1: 16, 0: 32, 1: 16}
    Kun(-1): 16, KanLi(0): 32, Qian(1): 16
  Basin transition matrix:
     from\to    Kun  KanLi   Qian
         Kun      8      4      4
       KanLi      6     22      3
        Qian      2      6      8

  Same-basin consecutive: 38/63 = 0.603
  Null mean same-basin: 23.0/63
  p-value (KW ≥ null): 0.0000
  ★ SIGNIFICANT

## Task 5: Odd vs Even (Upper/Lower Triangle)

### Odd (1,3,...,63)

  Lower trigrams: {'坤': 3, '震': 6, '坎': 4, '兌': 3, '艮': 5, '離': 5, '巽': 1, '乾': 5}
  Upper trigrams: {'坤': 4, '震': 2, '坎': 5, '兌': 6, '艮': 3, '離': 2, '巽': 6, '乾': 4}
  Lower elements: {'Earth': 8, 'Fire': 5, 'Metal': 8, 'Water': 4, 'Wood': 7}
  Upper elements: {'Earth': 7, 'Fire': 2, 'Metal': 10, 'Water': 5, 'Wood': 8}
  Relations: {'体克用': 6, '体生用': 6, '克体': 5, '比和': 7, '生体': 8}
  Basins: Kun=9, KanLi=16, Qian=7

### Even (2,4,...,64)

  Lower trigrams: {'坤': 5, '震': 2, '坎': 4, '兌': 5, '艮': 3, '離': 3, '巽': 7, '乾': 3}
  Upper trigrams: {'坤': 4, '震': 6, '坎': 3, '兌': 2, '艮': 5, '離': 6, '巽': 2, '乾': 4}
  Lower elements: {'Earth': 8, 'Fire': 3, 'Metal': 8, 'Water': 4, 'Wood': 9}
  Upper elements: {'Earth': 9, 'Fire': 6, 'Metal': 6, 'Water': 3, 'Wood': 8}
  Relations: {'体克用': 7, '体生用': 6, '克体': 8, '比和': 7, '生体': 4}
  Basins: Kun=7, KanLi=16, Qian=9

## Task 6: Specific Hypotheses

### Hypothesis A: Z₅×Z₅ torus coverage

  Cells visited: 25/25
  Complete coverage

  Torus grid (count of hexagrams per cell):
             Wood   Fire  Earth  Metal  Water
      Wood      4      2      4      4      2
      Fire      2      1      2      2      1
     Earth      4      2      4      4      2
     Metal      4      2      4      4      2
     Water      2      1      2      2      1

### Hypothesis B: Consecutive pair 互 relationships

  Pairs with same 互: 4/32
  Pairs where 互(a)=b or 互(b)=a: 1/32
  Consecutive hexagrams with same 互: 5/63
  Null mean consecutive same-互: 3.0
  p-value: 0.1816
  Not significant

### Hypothesis C: KW number ↔ 先天 (Shao Yong) correlation

  Pearson r(KW_index, SY_hex_number): 0.1038
  Spearman ρ: 0.1038, p=0.4146
  Not significant

### Hypothesis D: 上經 (1-30) vs 下經 (31-64)

  上經 (1-30):
    Relations: {'体克用': 6, '体生用': 4, '克体': 8, '比和': 7, '生体': 5}
    Basins: Kun=11, KanLi=14, Qian=5
    Mean yang lines: 2.87
    Mean SY sum: 6.70
    Pure hexagrams (lo=up): 4
  下經 (31-64):
    Relations: {'体克用': 7, '体生用': 8, '克体': 5, '比和': 7, '生体': 7}
    Basins: Kun=5, KanLi=18, Qian=11
    Mean yang lines: 3.12
    Mean SY sum: 7.26
    Pure hexagrams (lo=up): 4

  上經: 30 hexagrams (15 pairs)
  下經: 34 hexagrams (17 pairs)

  Pure hexagrams in 上經: 4
    #1 Qian (乾/乾)
    #2 Kun (坤/坤)
    #29 Kan (坎/坎)
    #30 Li (離/離)
  Pure hexagrams in 下經: 4
    #51 Zhen (震/震)
    #52 Gen (艮/艮)
    #57 Xun (巽/巽)
    #58 Dui (兌/兌)

### Additional: Element pair transition structure

  Consecutive pairs with same lower element: 11/63
  Consecutive pairs with same upper element: 10/63
  Consecutive pairs with both same: 0/63
  Null mean both-same: 2.1
  p-value: 1.0000
  Not significant

### Complement × pairing structure

  ★ KW pairs whose complements form a KW pair: 32/32
  → Complement PRESERVES the KW pairing structure perfectly

  Complement pair map (KW pair → complement pair):
    Pair 2 (Zhun...) ↔ Pair 25 (Ge...)
    Pair 3 (Xu...) ↔ Pair 18 (Jin...)
    Pair 4 (Shi...) ↔ Pair 7 (Tong Ren...)
    Pair 5 (Xiao Chu...) ↔ Pair 8 (Qian...)
    Pair 10 (Lin...) ↔ Pair 17 (Dun...)
    Pair 11 (Shi He...) ↔ Pair 24 (Kun...)
    Pair 12 (Bo...) ↔ Pair 22 (Guai...)
    Pair 13 (Wu Wang...) ↔ Pair 23 (Cui...)
    Pair 16 (Xian...) ↔ Pair 21 (Sun...)
    Pair 19 (Jia Ren...) ↔ Pair 20 (Jian...)
    Pair 26 (Zhen...) ↔ Pair 29 (Xun...)
    Pair 28 (Feng...) ↔ Pair 30 (Huan...)
  Self-complementary pairs: [1, 6, 9, 14, 15, 27, 31, 32]

  Self-complementary pair structure:
    Pair 1: Qian/Kun (111111/000000), comp=(000000/111111)
    Pair 6: Tai/Pi (000111/111000), comp=(111000/000111)
    Pair 9: Sui/Gu (011001/100110), comp=(100110/011001)
    Pair 14: Yi/Da Guo (100001/011110), comp=(011110/100001)
    Pair 15: Kan/Li (010010/101101), comp=(101101/010010)
    Pair 27: Jian/Gui Mei (110100/001011), comp=(001011/110100)
    Pair 31: Zhong Fu/Xiao Guo (110011/001100), comp=(001100/110011)
    Pair 32: Ji Ji/Wei Ji (010101/101010), comp=(101010/010101)

### Basin run structure

  上經: QKKK..KK....QQ....KK..KK..KQKQ
  下經: QQQQ......KKQQ....QQ....QQ..KKKQ..
  (K=Kun basin, .=KanLi, Q=Qian)

  Number of runs: 26 (63 transitions → 26 blocks)
  Runs: Q×1 K×3 .×2 K×2 .×4 Q×2 .×4 K×2 .×2 K×2 .×2 K×1 Q×1 K×1 Q×5 .×6 K×2 Q×2 .×4 Q×2 .×4 Q×2 .×2 K×3 Q×1 .×2

## Summary of Findings

### Pairing structure
  28 reversal pairs, 4 complement-only pairs
  Traditional claim (reversal except palindromes → complement): CONFIRMED

### Sequential structure significance
  Hamming distance: p=0.9815 (not significant)
  Torus step size: p=0.6178 (not significant)
  Basin clustering: p=0.0000 ★★★
  互 continuity: p=0.1816 (not significant)
  Element continuity: p=1.0000 (not significant)
  先天 correlation: ρ=0.1038, p=0.4146 (not significant)

### Key structural properties
  ★ Complement preserves KW pairing: 32/32 pairs map to pairs
  ★ Basin clustering: p<0.001 (38/63 same-basin transitions vs null ~23)
  ★ Zero consecutive same-element-pair hexagrams (anti-clustering at Z₅×Z₅)
  ★ 上經 contains 4 pure hexagrams: 乾坤坎離 (Metal,Earth,Water,Fire)
    下經 contains 4 pure hexagrams: 震艮巽兌 (Wood,Earth,Wood,Metal)
    → 上經 = singleton-element pures + Earth; 下經 = doubleton-element pures
  ★ 30+34 split: 上經 ends at Kan/Li (the Fire/Water bridge)

### 上經 vs 下經
  上經: 4 pure hexagrams, 下經: 4
  30 + 34 split (not 32 + 32)
  上經: Kun-basin dominated (11 Kun, 14 KanLi, 5 Qian)
  下經: Qian-basin dominated (5 Kun, 18 KanLi, 11 Qian)
  → The two canons occupy different basin territories
