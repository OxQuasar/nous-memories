# Line Text Valuations and the Binary Hierarchy

Total records: 384
Valence distribution: {'neutral': 118, 'positive': 148, 'mixed': 41, 'negative': 77}

Marker frequencies: {'吉': 118, '凶': 52, '无咎': 85, '悔': 26, '吝': 20, '厲': 26, '亨': 8}

## Task 2: Valuation by Line Position

  Line    N    吉     吉%    凶     凶%    无咎    悔    吝    厲  Pos  Neg  Mix  Neu
  -------------------------------------------------------------------------------------
     1   64   20  31.2%    9  14.1%    22    3    3    4   32   13    6   13
     2   64   27  42.2%    6   9.4%    11    3    1    1   31    8    3   22
     3   64    6   9.4%   13  20.3%    11    5    8   10    7   23   10   24
     4   64   19  29.7%    4   6.2%    19    6    4    3   28   10    7   19
     5   64   29  45.3%    3   4.7%     9    5    1    4   30    5    8   21
     6   64   17  26.6%   17  26.6%    13    4    3    4   20   18    7   19

  χ² test (吉 × line position): χ²=24.615, p=0.0002, dof=5
  χ² test (凶 × line position): χ²=19.930, p=0.0013, dof=5
  χ² test (valence × line position): χ²=43.864, p=0.0001, dof=15

## Task 3: Valuation by Algebraic Role

  Outer core (lines 1,2,5): always change element, never change basin
  Interface (lines 3,4): change basin (b₂, b₃)
  Shell (line 6): palace invariant (b₅), intra-fiber discriminator

          Role     N    吉      吉%    凶      凶%  Pos  Neg  Mix  Neu
  ----------------------------------------------------------------------
    outer_core   192   76   39.6%   18    9.4%   93   26   17   56
     interface   128   25   19.5%   17   13.3%   35   33   17   43
         shell    64   17   26.6%   17   26.6%   20   18    7   19

  χ² test (吉 × algebraic role): χ²=15.133, p=0.0005, dof=2
  χ² test (凶 × algebraic role): χ²=12.122, p=0.0023, dof=2

## Task 4: Valuation by 体/用 Position

  体 (lines [1, 2, 3]): N=192, 吉=53(27.6%), 凶=28(14.6%), 无咎=44, pos=70, neg=44
  用 (lines [4, 5, 6]): N=192, 吉=65(33.9%), 凶=24(12.5%), 无咎=41, pos=78, neg=33

  Fisher exact (吉: 体 vs 用): OR=0.745, p=0.2236
  Fisher exact (凶: 体 vs 用): OR=1.195, p=0.6549

## Task 5: Valuation by Element Relation

### Average rates by relation

  Relation     N    吉      吉%    凶      凶%    无咎    悔    吝    厲
  -----------------------------------------------------------------
        比和    84   19   22.6%   17   20.2%    17    7    2    6
        生体    72   30   41.7%    6    8.3%    13    5    5    6
       体生用    72   25   34.7%    5    6.9%    19    5    5    3
        克体    78   15   19.2%   13   16.7%    24    3    5    5
       体克用    78   29   37.2%   11   14.1%    12    6    3    6

### Interaction: 吉 rate by relation × line position

  Relation     L1     L2     L3     L4     L5     L6  {'Total':>6}
  -------------------------------------------------------
        比和    29%    43%     7%     7%    36%    14%   22.6%
        生体    33%    33%    17%    42%    75%    50%   41.7%
       体生用    17%    58%    25%    42%    50%    17%   34.7%
        克体    23%    31%     0%     8%    31%    23%   19.2%
       体克用    54%    46%     0%    54%    38%    31%   37.2%

### Interaction: 凶 rate by relation × line position

  Relation     L1     L2     L3     L4     L5     L6  {'Total':>6}
  -------------------------------------------------------
        比和    21%     7%    36%     7%     7%    43%   20.2%
        生体     0%    17%     8%     0%     8%    17%    8.3%
       体生用     0%    17%     0%     8%     0%    17%    6.9%
        克体    31%     0%    31%    15%     8%    15%   16.7%
       体克用    15%     8%    23%     0%     0%    38%   14.1%

  χ² test (吉 × relation × line, full 30-cell): χ²=58.579, p=0.0009, dof=29

## Task 6: 世 Line Valuation

  世 lines: 64 records (1 per hexagram)
    吉: 16 (25.0%)
    凶: 9 (14.1%)
    无咎: 15 (23.4%)

  Non-世 lines: 320 records
    吉: 102 (31.9%)
    凶: 43 (13.4%)
    无咎: 70 (21.9%)

  Fisher exact (吉: 世 vs non-世): OR=0.712, p=0.3023
  Fisher exact (凶: 世 vs non-世): OR=1.054, p=0.8434

### 世 line valuation by position

   世 line    N    吉      吉%    凶      凶%    无咎
  ---------------------------------------------
        1    8    3   37.5%    2   25.0%     1
        2    8    5   62.5%    0    0.0%     1
        3   16    0    0.0%    4   25.0%     2
        4   16    6   37.5%    0    0.0%     6
        5    8    1   12.5%    0    0.0%     3
        6    8    1   12.5%    3   37.5%     2

### 世 vs non-世 at same line position

  Line   世_N     世_吉%  Non世_N    Non世_吉%   p(Fisher)
  -------------------------------------------------------
     1     8    37.5%      56      30.4%      0.6970
     2     8    62.5%      56      39.3%      0.2657
     3    16     0.0%      48      12.5%      0.3231
     4    16    37.5%      48      27.1%      0.5302
     5     8    12.5%      56      50.0%      0.0627
     6     8    12.5%      56      28.6%      0.6701

## Additional: Line 5 as Ruler Position

Traditionally, line 5 is the 'ruler' (君位) — the central yang position.

  Line 5: 吉=29/64 (45.3%)
  Others: 吉=89/320 (27.8%)
  Fisher exact: OR=2.151, p=0.0074

  Line 5: 凶=3/64 (4.7%)
  Others: 凶=49/320 (15.3%)
  Fisher exact: OR=0.272, p=0.0260

## Additional: Lines 3 and 6 — Transition Positions

Lines 3 (top of lower trigram) and 6 (top of upper trigram) are
traditionally considered transition/ending positions.

  Line 3: 吉=6(9.4%), 凶=13(20.3%)
    vs others: 吉 p=0.0000, 凶 p=0.1072
  Line 6: 吉=17(26.6%), 凶=17(26.6%)
    vs others: 吉 p=0.4619, 凶 p=0.0021

## Summary

### Line position hierarchy in text
  吉 × line position: χ²=24.615, p=0.0002
  凶 × line position: χ²=19.930, p=0.0013
  → Significant variation in 吉 across lines
  → Significant variation in 凶 across lines

### Algebraic role
  吉 × role: χ²=15.133, p=0.0005
  → Roles differ in 吉 rate

### 体/用
  吉: 体 vs 用: OR=0.745, p=0.2236
  凶: 体 vs 用: OR=1.195, p=0.6549

### 世 line
  吉: 世 vs non-世: OR=0.712, p=0.3023
  凶: 世 vs non-世: OR=1.054, p=0.8434
