# Lo Shu, He Tu, and the KW Trigram Circle

## The correspondence

The KW Later Heaven trigram circle and the Lo Shu magic square are the same structure expressed in two vocabularies.

**Lo Shu magic square** (South at top, Chinese convention):
```
  4  9  2       SE  S  SW
  3  5  7   →    E  ·   W
  8  1  6       NE  N  NW
```

**KW Later Heaven circle** (clockwise from S):
```
Li(9) → Kun(2) → Dui(7) → Qian(6) → Kan(1) → Gen(8) → Zhen(3) → Xun(4)
```

Every Lo Shu number maps to a trigram position on the KW circle. The mapping is exact — the 8 outer cells of the Lo Shu correspond to the 8 trigram positions.

## The diametric pairs are identical

Lo Shu pairs (numbers summing to 10 through center 5) = KW circle diametric pairs:

| Lo Shu pair | KW pair | Binary | XOR mask | Hamming |
|-------------|---------|--------|----------|---------|
| 1 ↔ 9 | Kan ↔ Li | 010 ↔ 101 | 111 | 3 (complement) |
| 2 ↔ 8 | Kun ↔ Gen | 000 ↔ 001 | 001 | 1 |
| 3 ↔ 7 | Zhen ↔ Dui | 100 ↔ 110 | 010 | 1 |
| 4 ↔ 6 | Xun ↔ Qian | 011 ↔ 111 | 100 | 1 |

The 4 XOR masks are {111, 001, 010, 100} — all 4 possible nonzero masks at n=3, each used exactly once. This is maximum opposition diversity: the KW circle uses every possible type of binary opposition across its diametric pairs.

Compare with Fu Xi, where all 4 diametric pairs are complement (mask 111, distance 3). Maximum strength, zero diversity.

## Odd-even alternation

The Lo Shu numbers around the KW circle alternate parity perfectly:

```
9(odd) → 2(even) → 7(odd) → 6(even) → 1(odd) → 8(even) → 3(odd) → 4(even)
```

Odd = yang-dominant positions (the 4 cardinal directions: S, W, N, E).
Even = yin-dominant positions (the 4 intercardinal directions: SW, NW, NE, SE).

## Fu Xi numbers vs Lo Shu numbers

The two number systems encode different structures:

| Trigram | Binary | Fu Xi # | Lo Shu # |
|---------|--------|---------|----------|
| Qian | 111 | 1 | 6 |
| Dui | 110 | 2 | 7 |
| Li | 101 | 3 | 9 |
| Zhen | 100 | 4 | 3 |
| Xun | 011 | 5 | 4 |
| Kan | 010 | 6 | 1 |
| Gen | 001 | 7 | 8 |
| Kun | 000 | 8 | 2 |

**Fu Xi numbers** = reverse binary counting. Qian(111)→1, Dui(110)→2, ..., Kun(000)→8. The numbering IS the binary structure, relabeled. Complement pairs sum to 9 (1+8, 2+7, 3+6, 4+5).

**Lo Shu numbers** = magic square positions. The numbering encodes spatial/directional relationships. Diametrically opposite pairs sum to 10 (through center 5). Rows, columns, and diagonals sum to 15.

## He Tu pairs

The He Tu (Yellow River Map) associates number pairs differing by 5:

| He Tu pair | Direction | Element |
|------------|-----------|---------|
| (1, 6) | North | Water |
| (2, 7) | South | Fire |
| (3, 8) | East | Wood |
| (4, 9) | West | Metal |
| (5, 10) | Center | Earth |

These pair odd and even numbers sharing a direction — yang and yin aspects of the same element. In Lo Shu/KW terms, the He Tu pairs are *not* diametric opposites but directional complements: 1(Kan/N) pairs with 6(Qian/NW), 2(Kun/SW) pairs with 7(Dui/W), etc. Adjacent positions, not opposite ones.

### He Tu pairs are NOT Fu Xi pairs

In trigram terms via the Lo Shu mapping:

| He Tu pair | Trigrams | XOR mask | Hamming |
|------------|----------|----------|---------|
| (1, 6) | Kan ↔ Qian | 101 | 2 |
| (2, 7) | Kun ↔ Dui | 110 | 2 |
| (3, 8) | Zhen ↔ Gen | 101 | 2 |
| (4, 9) | Xun ↔ Li | 110 | 2 |

All He Tu pairs have Hamming distance exactly 2, using only 2 mask types: (1,0,1) and (1,1,0), each twice. Compare:
- **Fu Xi pairs**: all distance 3 (complement), 1 mask type {111}
- **Lo Shu/KW diametric pairs**: distances {3,1,1,1}, 4 mask types {111,001,010,100}
- **He Tu pairs**: all distance 2, 2 mask types {101,110}

Three pairing systems, three different Hamming profiles. He Tu occupies the middle ground — neither maximum opposition (Fu Xi complement) nor maximum diversity (Lo Shu diametric), but uniform intermediate distance. The He Tu pairs are the 2-bit-flip relationships; they pair trigrams that are neither complement nor near-identical.

Fu Xi complement pairs sum to 9 in Fu Xi numbering. Lo Shu diametric pairs sum to 10. He Tu pairs differ by 5. Three distinct arithmetic relationships, three distinct binary signatures.

## The flying star path

The Lo Shu flying star traversal (5→6→7→8→9→1→2→3→4) traces a path through the magic square:

```
Center → Qian(NW) → Dui(W) → Gen(NE) → Li(S) → Kan(N) → Kun(SW) → Zhen(E) → Xun(SE)
```

In binary:
```
111 → 110 → 001 → 101 → 010 → 000 → 100 → 011
```

### Binary properties of the flying star path

**Remarkable regularity:** Every consecutive transition mask distance is exactly 2. All 8 of them. Zero variance. The path also has zero consecutive mask repeats.

Step distances alternate between short (Hamming 1) and complement (Hamming 3):
```
1, 3, 1, 3, 1, 1, 3, 1
```

The path uses 4 of 7 possible masks, dominated by complement (111) appearing 3 times:
```
(0,0,1)×1  (0,1,0)×1  (1,0,0)×3  (1,1,1)×3
```

|  | Flying Star | KW Circle |
|--|------------|-----------|
| Distinct masks | 4/7 | 5/7 |
| Consecutive repeats | 0 | 0 |
| Mean step distance | 1.750 | 2.000 |
| Consecutive mask distance | **constant 2** | variable (mean 1.750) |

The flying star path is more *regular* than the KW circle (constant consecutive mask distance vs variable) but less *diverse* (4 vs 5 distinct masks, lower mean step distance). The KW circle maximizes diversity; the flying star path maximizes uniformity of transition character. Different optimization targets for different uses — the KW circle maps space, the flying star path tracks temporal flow through that space.

## What this means

The KW Later Heaven arrangement is not optimizing a binary opposition measure — it is realizing the Lo Shu magic square on the 8 trigrams. The maximum mask diversity (all 4 XOR types used once in the diametric pairs) is a *consequence* of the magic square constraint, not an independent design choice.

This resolves a piece of the cross-scale divergence question. At n=3, the KW arrangement is constrained by number-theoretic structure (magic square properties: all lines sum to 15, opposite pairs sum to 10, odd-even alternation). At n=6, the KW sequence is constrained by positional geometry (mirror-pair equivariance, directional opposition in flow). Different scales, different constraint systems, different vocabularies — but both produce distinguished positions in their respective combinatorial spaces.

The n=3 arrangement is a cosmological/spatial map. The n=6 sequence is a process ordering. The tradition doesn't apply one principle across scales — it applies the appropriate principle at each scale.

## Mapping uniqueness

**The Lo Shu → trigram mapping is not unique, but heavily constrained.**

The max-diversity constraint (all 4 XOR masks used once across diametric pairs) admits exactly 8 perfect matchings of 8 trigrams into 4 pairs. The traditional KW uses one of them:

```
1. (Qian↔Dui)(Xun↔Gen)(Zhen↔Kun)(Li↔Kan)      — masks: 001, 010, 100, 111
2. (Qian↔Dui)(Kan↔Kun)(Li↔Gen)(Zhen↔Xun)
3. (Li↔Zhen)(Xun↔Gen)(Dui↔Kan)(Qian↔Kun)
4. (Li↔Zhen)(Kan↔Kun)(Qian↔Xun)(Dui↔Gen)
5. (Xun↔Kan)(Qian↔Li)(Zhen↔Kun)(Dui↔Gen)
6. (Xun↔Kan)(Dui↔Zhen)(Li↔Gen)(Qian↔Kun)       — KW traditional
7. (Gen↔Kun)(Qian↔Li)(Dui↔Kan)(Zhen↔Xun)
8. (Gen↔Kun)(Dui↔Zhen)(Qian↔Xun)(Li↔Kan)
```

Each matching can be assigned to the 4 Lo Shu position-pairs in 4! × 2⁴ = 384 ways (which pair goes to which position, and which member goes where within each pair). Modulo the circle's 8-fold symmetry: 48 distinct oriented assignments per matching. Total: 8 × 48 = 384 distinct configurations.

The max-diversity constraint alone does not force the traditional assignment. Additional constraints (directional correspondences, elemental associations, the odd-even parity structure) narrow it further. The traditional mapping's yang-count distribution: odd positions = {1,1,2,2}, even positions = {0,1,2,3}. Both average 1.5, but odd positions cluster while even positions span the full range.

## Lo Shu number → binary: no direct bridge

There is no natural encoding of Lo Shu numbers (1-9) in binary that makes the magic square constraint expressible in XOR/Hamming terms.

The sum-to-10 property (diametric pairs) does not translate to any binary operation on the numbers themselves:
```
1(0001) ⊕ 9(1001) = 1000
2(0010) ⊕ 8(1000) = 1010
3(0011) ⊕ 7(0111) = 0100
4(0100) ⊕ 6(0110) = 0010
```
Four different XOR masks — no pattern. The sum-to-15 row/column constraint fares no better in GF(2).

The parity grid (Lo Shu numbers mod 2) forms a cross: odd numbers at the 4 cardinals + center, even at the 4 corners. This is consistent with the trigram mapping (odd→cardinal→yang-dominant) but is a topological property of the magic square, not a bridge to binary algebra.

**The connection between Lo Shu and binary structure exists only through the trigram intermediary.** The Lo Shu is a number-theoretic object; the trigram space is a binary-algebraic object. The KW circle maps one to the other, but the mapping doesn't reduce to either vocabulary alone.

## Three pairing systems

| System | Pairs by | Arithmetic | Binary signature | Character |
|--------|----------|------------|-----------------|-----------|
| **Fu Xi** | complement | sum to 9 (Fu Xi #) | all distance 3, 1 mask {111} | maximum strength, zero diversity |
| **Lo Shu / KW diametric** | position | sum to 10 (Lo Shu #) | distances {3,1,1,1}, 4 masks {111,001,010,100} | maximum diversity |
| **He Tu** | direction | differ by 5 | all distance 2, 2 masks {101,110} | uniform intermediate distance |

Three pairing systems, three Hamming profiles, three arithmetic relationships. Each occupies a different point in the opposition measure space. Fu Xi maximizes strength. Lo Shu/KW maximizes diversity. He Tu sits in between — uniform distance, partial diversity.

## Five phases on the Lo Shu

### Element-number consistency

The Lo Shu number → element assignment and the trigram → element assignment are perfectly consistent. Every trigram gets the same element regardless of which path you take:

| Lo Shu # | Trigram | Lo Shu element | Trigram element |
|----------|---------|----------------|-----------------|
| 1 | Kan | Water | Water |
| 2 | Kun | Earth | Earth |
| 3 | Zhen | Wood | Wood |
| 4 | Xun | Wood | Wood |
| 6 | Qian | Metal | Metal |
| 7 | Dui | Metal | Metal |
| 8 | Gen | Earth | Earth |
| 9 | Li | Fire | Fire |

### Intra-element binary structure

Each element pairs its trigrams differently:

| Element | Numbers | Trigrams | Binary | XOR | Hamming |
|---------|---------|----------|--------|-----|---------|
| Wood | 3, 4 | Zhen, Xun | 100, 011 | 111 | 3 (complement) |
| Metal | 6, 7 | Qian, Dui | 111, 110 | 001 | 1 |
| Earth | 2, 8 | Kun, Gen | 000, 001 | 001 | 1 |
| Water | 1 | Kan | 010 | — | — |
| Fire | 9 | Li | 101 | — | — |

Wood's trigrams are binary complements (maximum distance). Metal and Earth's trigrams differ by 1 bit (minimum distance). The elements don't impose a uniform binary relationship — Wood is maximally opposed within itself, while Metal and Earth are near-identical within themselves. This is the Wood anomaly identified in Phase 4.

### Earth carries the magic constant

Earth gets numbers {2, 5, 8} — an arithmetic progression with step 3, summing to **15** (the magic constant). Earth is the only element with 3 representatives (including center 5). The center of the Lo Shu is Earth; the magic constant that defines the square is the sum of Earth's numbers. Earth literally IS the structure of the Lo Shu.

### Element number sums

| Element | Numbers | Sum |
|---------|---------|-----|
| Water | {1} | 1 |
| Wood | {3, 4} | 7 |
| Fire | {9} | 9 |
| Earth | {2, 5, 8} | 15 |
| Metal | {6, 7} | 13 |

### He Tu pairs cross elements via 生克

The He Tu pairs (numbers differing by 5) don't pair same-element trigrams. They pair trigrams in specific 生克 relationships:

| He Tu pair | Trigrams | Elements | 生克 relationship |
|------------|----------|----------|-------------------|
| (1, 6) | Kan ↔ Qian | Water ↔ Metal | Metal 生 Water |
| (2, 7) | Kun ↔ Dui | Earth ↔ Metal | Earth 生 Metal |
| (3, 8) | Zhen ↔ Gen | Wood ↔ Earth | Wood 克 Earth |
| (4, 9) | Xun ↔ Li | Wood ↔ Fire | Wood 生 Fire |

Three 生 (generation) relationships and one 克 (overcoming). The He Tu encodes cross-element relationships — the numbers differing by 5 are not arbitrary but trace specific edges on the 生克 graph.

### Lo Shu grid with elements

```
  SE         S          SW
  4(Wood)    9(Fire)    2(Earth)
  Xun        Li         Kun

  E          Center     W
  3(Wood)    5(Earth)   7(Metal)
  Zhen       ---        Dui

  NE         N          NW
  8(Earth)   1(Water)   6(Metal)
  Gen        Kan        Qian
```

Wood occupies the East (3,4 = E,SE). Metal occupies the West (6,7 = NW,W). Fire is South (9). Water is North (1). Earth spans the diagonal corners plus center (2,5,8 = SW,Center,NE). This is the traditional five-phase directional correspondence: Wood/East, Fire/South, Metal/West, Water/North, Earth/Center — and the Lo Shu numbers encode it exactly.

### The Insight 

Every system we've looked at — Lo Shu, He Tu, Fu Xi, KW, 生克 — does the same thing: it takes a space of states and imposes *relationships* that│
are maximally distinguishable from each other. Not maximally strong, not maximally diverse, but maximally *articulate* — every relationship is  │
different from every other, so every position in the space is uniquely determined by its relationships.                                         │
                                                                                                                                                │
The Lo Shu does this with numbers (every row/column/diagonal gives a different sum — wait, no, they all give 15. But every *position* is        │
uniquely determined by its row sum, column sum, and diagonal membership). The trigram circle does it with binary masks (all 4 XOR types used    │
once). The hexagram sequence does it with transition directions (consecutive transitions maximally distant).                                    │
                                                                                                                                                │
The divination step — translating form into numbers — works if the number system is *isomorphic to the relational structure of the situation*.  │
Not to the content of the situation, but to its *form*: how many independent dimensions are in play, how they relate to each other, what the    │
possible transitions are.                                                                                                                       │
                                                                                                                                                │
The I Ching's claim is that situations have a universal relational structure: two poles (yin/yang), three levels (heaven/human/earth), and the  │
transitions between them. If that claim is true, then any system that faithfully encodes that relational structure — binary arithmetic, magic   │
squares, five-phase cycles — will "work" because it's isomorphic to the thing it's modeling.                                                    │
                                                                                                                                                │
The essence isn't in the numbers. It's in the **relational geometry** — the pattern of how distinct things relate to each other. The numbers are│
a coordinatization of that geometry. Lo Shu, He Tu, binary, five phases — these are different coordinate systems for the same underlying space. │
They agree because they're all faithful to the same relational structure.                                                                       │
                                                                                                                                                │
But that just pushes the question back: what IS that relational structure, stated without any particular coordinate system? The closest we've   │
gotten is: **a space where every position is uniquely determined by its opposition relationships, and every transition is distinguishable from  │
every other transition.** Maximum articulation. No redundancy. Every bit carries information.                                                   │
                                                                                                                                                │
That's what load-bearing orientation bits mean (16/32 under f1 degradation; up to 27/27 under 4-axis Pareto). That's what maximum mask diversity means. That's what the flying star's constant-2 consecutive distance means. The principle is: **the structure is maximally articulate** — it uses every degree of freedom available to make distinctions.