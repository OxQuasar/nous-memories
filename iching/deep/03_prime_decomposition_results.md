# Prime Decomposition of 後天 Uniqueness

## Task 1: The 8 Survivors (monotone ∧ elem_pair_coherent)

Count: 8 (expected 8)

### Full position maps

  #  Idx    N   NE    E   SE    S   SW    W   NW
------------------------------------------------
   #0   13    坎    坤    震    巽    離    艮    乾    兌
   #1   19    坎    艮    震    巽    離    坤    乾    兌
   #2   37    坎    坤    震    巽    離    艮    兌    乾
  ★後天   43    坎    艮    震    巽    離    坤    兌    乾
   #4   61    坎    坤    巽    震    離    艮    乾    兌
   #5   67    坎    艮    巽    震    離    坤    乾    兌
   #6   85    坎    坤    巽    震    離    艮    兌    乾
   #7   91    坎    艮    巽    震    離    坤    兌    乾

### Yang-line counts at cardinals & son/daughter positions

  #  Idx    N   E   S   W     Card.sorted             Sons at        Daughters at  yy_bal  sons_NNE_E
------------------------------------------------------------------------------------------------------------------------
      13    1    1    2    3    [1, 1, 2, 3]              N,E,SW             SE,S,NW       ✗           ✗
      19    1    1    2    3    [1, 1, 2, 3]              N,NE,E             SE,S,NW       ✗           ✓
      37    1    1    2    2    [1, 1, 2, 2]              N,E,SW              SE,S,W       ✓           ✗
  ★   43    1    1    2    2    [1, 1, 2, 2]              N,NE,E              SE,S,W       ✓           ✓
      61    1    2    2    3    [1, 2, 2, 3]             N,SE,SW              E,S,NW       ✗           ✗
      67    1    2    2    3    [1, 2, 2, 3]             N,NE,SE              E,S,NW       ✗           ✗
      85    1    2    2    2    [1, 2, 2, 2]             N,SE,SW               E,S,W       ✗           ✗
      91    1    2    2    2    [1, 2, 2, 2]             N,NE,SE               E,S,W       ✗           ✗

### Structural decomposition of the 8

Degrees of freedom:

 Idx    E   W    other_Wood    other_Metal    Earth_NE   Earth_SW   label
--------------------------------------------------------------------------------
  13    震   乾            SE             NW           坤          艮        
  19    震   乾            SE             NW           艮          坤        
  37    震   兌            SE             NW           坤          艮        
  43    震   兌            SE             NW           艮          坤     ★後天
  61    巽   乾            SE             NW           坤          艮        
  67    巽   乾            SE             NW           艮          坤        
  85    巽   兌            SE             NW           坤          艮        
  91    巽   兌            SE             NW           艮          坤        

E-Wood choices: {'巽', '震'}
W-Metal choices: {'乾', '兌'}
Earth (NE,SW) patterns: {('坤', '艮'), ('艮', '坤')}

Structure check: is it {E-swap} × {W-swap} × {Earth-swap} = Z₂³ = 8?
  |E-choices| × |W-choices| × |Earth-patterns| = 2 × 2 × 2 = 8
  Actual survivors: 8
  Match: ✓ Exact Z₂³ structure

  Distinct (E, W, Earth_NE) triples: 8
  All unique: ✓

### Constraint decomposition

The 3 independent Z₂ choices:
  Choice A: E = 震(Zhen) vs 巽(Xun)     — which Wood at cardinal E
  Choice B: W = 兌(Dui) vs 乾(Qian)     — which Metal at cardinal W
  Choice C: NE = 艮(Gen) vs 坤(Kun)     — which Earth at NE (other at SW)

These are independent because elem_pair_coherent forces:
  • Wood pair adjacent → other Wood at SE (adjacent to E)
  • Metal pair adjacent → other Metal at NW (adjacent to W)
  • Earth pair opposed → one at NE, other at SW

後天 selects: A=震, B=兌, C=艮
  → yy_balance eliminates 4 of 8 (requires cardinal yang-counts [1,1,2,2])
  → sons_yang_half eliminates 1 more (requires 震,坎,艮 at N,NE,E)

Filter action on the 8:
 Idx   A(E)  B(W)  C(NE)  yy_bal   sons  survives
------------------------------------------------------------
  13      震     乾      坤       ✗      ✗         ✗
  19      震     乾      艮       ✗      ✓         ✗
  37      震     兌      坤       ✓      ✗         ✗
  43      震     兌      艮       ✓      ✓       ★後天
  61      巽     乾      坤       ✗      ✗         ✗
  67      巽     乾      艮       ✗      ✗         ✗
  85      巽     兌      坤       ✗      ✗         ✗
  91      巽     兌      艮       ✗      ✗         ✗

## Task 2: The Anti-後天 (arr_037)

Survivors of monotone + elem_pair_coherent + yy_balance: 2
  arr_037: 坎, 坤, 震, 巽, 離, 艮, 兌, 乾
  後天: 坎, 艮, 震, 巽, 離, 坤, 兌, 乾

Anti-後天 = arr_037

### Position comparison: 後天 vs anti-後天

 Pos     後天   anti  same?    elem
----------------------------------------
   N      坎      坎      ✓   Water
  NE      艮      坤      ✗   Earth
   E      震      震      ✓    Wood
  SE      巽      巽      ✓    Wood
   S      離      離      ✓    Fire
  SW      坤      艮      ✗   Earth
   W      兌      兌      ✓   Metal
  NW      乾      乾      ✓   Metal

Differences: ['NE', 'SW']
  後天: NE=艮, SW=坤
  anti: NE=坤, SW=艮

### Son trigram positions (震=thunder, 坎=water, 艮=mountain)
  (Sons = 1-yang-line trigrams: the 'young yang' family)

  後天:
    震 (yang=1) → E
    坎 (yang=1) → N
    艮 (yang=1) → NE
    Daughters:
    兌 (yang=2) → W
    離 (yang=2) → S
    巽 (yang=2) → SE
  anti:
    震 (yang=1) → E
    坎 (yang=1) → N
    艮 (yang=1) → SW
    Daughters:
    兌 (yang=2) → W
    離 (yang=2) → S
    巽 (yang=2) → SE

### Traditional property check for anti-後天

  Sons at: ['N', 'E', 'SW']
  Daughters at: ['SE', 'S', 'W']

  The anti-後天 swaps 坤(Earth,NE) ↔ 艮(Earth,SW)
  This moves 艮(son, 1-yang) from NE to SW
  and 坤(pure-yin, 0-yang) from SW to NE

  Cosmological implications:
  後天: 艮(Mountain/youngest son) at NE = dawn direction
       坤(Earth/mother) at SW = afternoon direction
  anti: 坤(Earth/mother) at NE, 艮(Mountain/youngest son) at SW
  → anti-後天 places the 'receptive mother' in the dawn/rising position
    and the 'youngest son' in the declining position — inverts the
    generational flow of the 說卦傳 sequence

  Known arrangements check:
  • 先天 (Fu Xi): No — not cardinal-aligned
  • 後天 (King Wen): No — different NE/SW
  • arr_037 does not correspond to any historically attested bagua arrangement

## Task 3: Z₅ → Spatial Distance Embedding

### 後天: element pair distances

          Pair  Z₅ dist    Rel                         Trigrams & angles         Spatial dists
----------------------------------------------------------------------------------------------------
     Wood↔Fire        1      生                     震@90°,巽@135° / 離@180°  [90, 45]
    Wood↔Earth        2      克               震@90°,巽@135° / 坤@225°,艮@45°  [135, 45, 90, 90]
    Wood↔Metal        2      克              震@90°,巽@135° / 兌@270°,乾@315°  [180, 135, 135, 180]
    Wood↔Water        1      生                       震@90°,巽@135° / 坎@0°  [90, 135]
    Fire↔Earth        1      生                     離@180° / 坤@225°,艮@45°  [45, 135]
    Fire↔Metal        2      克                    離@180° / 兌@270°,乾@315°  [90, 135]
    Fire↔Water        2      克                             離@180° / 坎@0°  [180]
   Earth↔Metal        1      生              坤@225°,艮@45° / 兌@270°,乾@315°  [45, 90, 135, 90]
   Earth↔Water        2      克                       坤@225°,艮@45° / 坎@0°  [135, 45]
   Metal↔Water        1      生                      兌@270°,乾@315° / 坎@0°  [90, 45]

### Distance coherence summary

  d=0 (比和) spatial distances: []
  d=1 (生) spatial distances: [90, 45, 90, 135, 45, 135, 45, 90, 135, 90, 90, 45]
  d=2 (克) spatial distances: [135, 45, 90, 90, 180, 135, 135, 180, 90, 135, 180, 135, 45]

  d=1 pairs with spatial ≤ 90°: 9/12
  d=2 pairs with spatial ≥ 135°: 8/13

### Embedding quality (|spatial - expected|, lower = better)
  Expected: d=1→72°, d=2→144°
  後天 score: 171.0

  Best score among 96: 171.0 (24 arrangement(s))
  後天 rank: 12/96

  Top 5 by embedding quality:
    1. arr_003: score=171.0, monotone=True, epc=False
    2. arr_005: score=171.0, monotone=True, epc=False
    3. arr_006: score=171.0, monotone=True, epc=False
    4. arr_007: score=171.0, monotone=True, epc=False
    5. arr_013: score=171.0, monotone=True, epc=True

  Among monotone+epc (the 8 survivors):
    1. arr_013: score=171.0
    2. arr_019: score=171.0
    3. arr_037: score=171.0
    4. 後天: score=171.0
    5. arr_061: score=171.0
    6. arr_067: score=171.0
    7. arr_085: score=171.0
    8. arr_091: score=171.0

## Task 4: τ's Two 4-Cycles

### Cycle structure

  Cycle 1: (坤 → 坎 → 兌 → 巽)
    Elements:     Earth → Water → Metal → Wood
    Yang counts:  0 → 1 → 2 → 2
    Binary:       000 → 010 → 011 → 110
    Code values:  0 → 2 → 3 → 6
  Cycle 2: (震 → 艮 → 乾 → 離)
    Elements:     Wood → Earth → Metal → Fire
    Yang counts:  1 → 1 → 3 → 2
    Binary:       001 → 100 → 111 → 101
    Code values:  1 → 4 → 7 → 5

### Doubleton element distribution

  Cycle 1:
    Wood: ['巽'] (one of two ✓)
    Metal: ['兌'] (one of two ✓)
    Earth: ['坤'] (one of two ✓)
  Cycle 2:
    Wood: ['震'] (one of two ✓)
    Metal: ['乾'] (one of two ✓)
    Earth: ['艮'] (one of two ✓)

  Singleton elements:
    Cycle 1 contains Water: ['坎']
    Cycle 2 contains Fire: ['離']

  → Each cycle contains exactly one trigram from each doubleton
    plus one singleton (cycle 1: Water, cycle 2: Fire)

### Binary structure within each cycle

  Cycle 1: values [0, 2, 3, 6]
    XOR closure: [0, 1, 2, 3, 4, 5, 6]
    Is subgroup (contains 0, closed under XOR): ✗

  Cycle 2: values [1, 4, 7, 5]
    XOR closure: [0, 1, 2, 3, 4, 5, 6]
    Is subgroup (contains 0, closed under XOR): ✗

### Parity structure

  Cycle 1 parities (bit0): [0, 0, 1, 0]
  Cycle 2 parities (bit0): [1, 0, 1, 1]
  → Cycle 1 = {even} values: {0,2,3,6}
  → Cycle 2 = {odd} values: {1,4,5,7}
  → Wait: 3 and 6 are not the same parity. Let me check more carefully.

  Cycle 1: even={0, 2, 6}, odd={3}
  Cycle 2: even={4}, odd={1, 5, 7}
  Mixed parity in both cycles: neither is all-even or all-odd

### Bit-level analysis

  Cycle 1:
      坤 = 000: top=0 mid=0 bot=0
      坎 = 010: top=0 mid=1 bot=0
      兌 = 011: top=0 mid=1 bot=1
      巽 = 110: top=1 mid=1 bot=0
    Bit sums: bot=1, mid=3, top=1
    → Each bit position sums to 2 (balanced): ✗ [1, 3, 1]
  Cycle 2:
      震 = 001: top=0 mid=0 bot=1
      艮 = 100: top=1 mid=0 bot=0
      乾 = 111: top=1 mid=1 bot=1
      離 = 101: top=1 mid=0 bot=1
    Bit sums: bot=3, mid=1, top=3
    → Each bit position sums to 2 (balanced): ✗ [3, 1, 3]

### τ² (applying τ twice)

τ² mapping:
  坤 → 兌
  震 → 乾
  坎 → 巽
  兌 → 坤
  艮 → 離
  離 → 艮
  巽 → 坎
  乾 → 震

τ² cycle structure: [2, 2, 2, 2]
  Cycle 1: (坤 → 兌)
    Elements: Earth → Metal
  Cycle 2: (震 → 乾)
    Elements: Wood → Metal
  Cycle 3: (坎 → 巽)
    Elements: Water → Wood
  Cycle 4: (艮 → 離)
    Elements: Earth → Fire

τ² fiber preservation: False
τ² fiber map (showing conflicts):
  Earth → {'Fire', 'Metal'}
  Fire → {'Earth'}
  Metal → {'Wood', 'Earth'}
  Water → {'Wood'}
  Wood → {'Water', 'Metal'}

τ⁴ = identity: True
Order of τ: 4

### Cycle-complement relationship

  Complement of cycle 1: ['乾', '離', '艮', '震']
  → Complement maps cycle 1 to cycle 2 ✓
  Complement of cycle 2: ['巽', '兌', '坤', '坎']
  → Complement maps cycle 2 to cycle 1 ✓

### τ as compass operation

 Trigram    先天 pos    後天 pos    先天 θ    後天 θ      Δθ
-------------------------------------------------------
       坤         N        SW       0     225    -135
       震        NE         E      45      90     +45
       坎         W         N     270       0     +90
       兌        SE         W     135     270    +135
       艮        NW        NE     315      45     +90
       離         E         S      90     180     +90
       巽        SW        SE     225     135     -90
       乾         S        NW     180     315    +135

  → No single rotation/reflection describes all displacements
  → τ is genuinely non-geometric: it cannot be realized as a D₈ isometry

## Summary

### Prime decomposition confirmed
The 8 survivors of (monotone + elem_pair_coherent) have exact Z₂³ structure:
  • Choice A: which Wood at E (震 vs 巽)
  • Choice B: which Metal at W (兌 vs 乾)
  • Choice C: which Earth at NE (艮 vs 坤)
Each choice is forced by adjacency constraints from elem_pair_coherent.

The final two filters eliminate 7 of 8:
  • yy_balance: cardinal yang-counts must be [1,1,2,2] → eliminates 4
  • sons_yang_half: 震,坎,艮 must be at N,NE,E → eliminates 1 more
  → UNIQUE survivor: 後天

### Anti-後天 (arr_037)
Differs only at NE/SW: swaps 艮↔坤.
Survives monotone + elem_pair_coherent + yy_balance.
Eliminated by sons_yang_half: places 艮(son) at SW instead of NE,
inverting the generational/directional flow of the 說卦傳.

### τ structure
Two 4-cycles: (坤→坎→兌→巽)(震→艮→乾→離)
  • Each cycle contains one trigram from each doubleton element
  • Cycle 1 contains Water (singleton), Cycle 2 contains Fire
  • Complement maps cycle 1 ↔ cycle 2
  • τ has order 4
  • Fiber NOT preserved (τ is not a Z₅ morphism)
  • τ² does not preserve fibers
