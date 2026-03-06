# Phase 4: 生克 (Shēng-Kè) Foundation Data

Five-phase (五行) analysis of the KW pairing and trigram→element mapping.
Encoding: L1=bit0 (bottom) … L6=bit5 (top). Trigrams as 3-bit integers.

## 0. Traditional Mapping

### Trigram → Element

| Trigram | Binary | Element | Element (ZH) |
|---------|--------|---------|-------------|
| Kun ☷ | 000 | Earth | 土 |
| Gen ☶ | 001 | Earth | 土 |
| Kan ☵ | 010 | Water | 水 |
| Xun ☴ | 011 | Wood | 木 |
| Zhen ☳ | 100 | Wood | 木 |
| Li ☲ | 101 | Fire | 火 |
| Dui ☱ | 110 | Metal | 金 |
| Qian ☰ | 111 | Metal | 金 |

### Five-phase cycles

**生 (generation):** Wood → Fire → Earth → Metal → Water → Wood
**克 (overcoming):** Wood → Earth → Water → Fire → Metal → Wood

### Element → Trigrams

| Element | Trigrams | Count |
|---------|----------|-------|
| Wood (木) | Xun ☴ (011), Zhen ☳ (100) | 2 |
| Fire (火) | Li ☲ (101) | 1 |
| Earth (土) | Kun ☷ (000), Gen ☶ (001) | 2 |
| Metal (金) | Dui ☱ (110), Qian ☰ (111) | 2 |
| Water (水) | Kan ☵ (010) | 1 |

## Q1: 体/用 as Scale Bridge

384 states = 64 hexagrams × 6 moving lines.
Moving in lower → lower=用, upper=体. Moving in upper → upper=用, lower=体.

### 1.1 Hamming Distance Distribution (体 vs 用)

| Hamming d | Count | Fraction | Baseline (all 8×8) |
|-----------|-------|----------|-------------------|
| 0 | 48 | 0.1250 | 0.1250 |
| 1 | 144 | 0.3750 | 0.3750 |
| 2 | 144 | 0.3750 | 0.3750 |
| 3 | 48 | 0.1250 | 0.1250 |

**Mean Hamming (体/用):** 1.5000
**Mean Hamming (baseline all pairs):** 1.5000
**Bias:** neutral

### 1.2 XOR Mask Distribution (体 ⊕ 用)

| XOR mask | Count | Fraction | Hamming |
|----------|-------|----------|---------|
| 000 | 48 | 0.1250 | 0 |
| 001 | 48 | 0.1250 | 1 |
| 010 | 48 | 0.1250 | 1 |
| 011 | 48 | 0.1250 | 2 |
| 100 | 48 | 0.1250 | 1 |
| 101 | 48 | 0.1250 | 2 |
| 110 | 48 | 0.1250 | 2 |
| 111 | 48 | 0.1250 | 3 |

### 1.3 Cross-Tabulation: KW Signature × Hamming Distance

KW signature (o,m,i) for the hexagram's KW pair; Hamming = distance between 体 and 用 trigrams.

| Signature | d=0 | d=1 | d=2 | d=3 | Total | Mean d |
|-----------|-----|-----|-----|-----|-------|--------|
| (0, 0, 1) | 0 | 48 | 0 | 0 | 48 | 1.00 |
| (0, 1, 0) | 0 | 24 | 0 | 24 | 48 | 2.00 |
| (0, 1, 1) | 0 | 0 | 48 | 0 | 48 | 2.00 |
| (1, 0, 0) | 0 | 48 | 0 | 0 | 48 | 1.00 |
| (1, 0, 1) | 24 | 0 | 24 | 0 | 48 | 1.00 |
| (1, 1, 0) | 0 | 0 | 48 | 0 | 48 | 2.00 |
| (1, 1, 1) | 24 | 24 | 24 | 24 | 96 | 1.50 |

### 1.4 Cross-Tabulation: KW Signature × Five-Phase Relation

| Signature | 比和 | 生体 | 克体 | 体生用 | 体克用 |
|-----------|---|---|---|---|---|
| (0, 0, 1) | 12 | 12 | 6 | 12 | 6 |
| (0, 1, 0) | 12 | 6 | 12 | 6 | 12 |
| (0, 1, 1) | 0 | 12 | 12 | 12 | 12 |
| (1, 0, 0) | 12 | 12 | 6 | 12 | 6 |
| (1, 0, 1) | 24 | 12 | 0 | 12 | 0 |
| (1, 1, 0) | 0 | 12 | 12 | 12 | 12 |
| (1, 1, 1) | 24 | 6 | 30 | 6 | 30 |

### 1.5 KW Partner 体/用 Complementarity

For each KW pair (a,b) at same moving line: what is rel(a) vs rel(b)?

| rel(a) | rel(b) | Count |
|--------|--------|-------|
| 比和 | 比和 | 24 |
| 体克用 | 克体 | 21 |
| 克体 | 体克用 | 21 |
| 克体 | 生体 | 12 |
| 体克用 | 体生用 | 12 |
| 体生用 | 体克用 | 12 |
| 生体 | 克体 | 12 |
| 生体 | 生体 | 12 |
| 体生用 | 体生用 | 12 |
| 生体 | 体生用 | 9 |
| 体生用 | 生体 | 9 |
| 比和 | 体克用 | 6 |
| 比和 | 克体 | 6 |
| 克体 | 比和 | 6 |
| 体克用 | 比和 | 6 |
| 体生用 | 比和 | 3 |
| 生体 | 比和 | 3 |
| 比和 | 生体 | 3 |
| 比和 | 体生用 | 3 |

**Same relation:** 48/192 = 0.2500
**Different relation:** 144/192 = 0.7500

**Key patterns (top 10):**

| rel(a) | rel(b) | Count | Complementary? |
|--------|--------|-------|----------------|
| 比和 | 比和 | 24 | ✗ |
| 体克用 | 克体 | 21 | ✓ |
| 克体 | 体克用 | 21 | ✓ |
| 克体 | 生体 | 12 | ✓ |
| 体克用 | 体生用 | 12 | ✓ |
| 体生用 | 体克用 | 12 | ✓ |
| 生体 | 克体 | 12 | ✓ |
| 生体 | 生体 | 12 | ✗ |
| 体生用 | 体生用 | 12 | ✗ |
| 生体 | 体生用 | 9 | ✓ |

## Q2: 生克 in Hamming/Mask Terms

### 2.1 Intra-Element Structure

Trigrams the tradition treats as 'same element' (比和).

| Element | Trig A | Trig B | XOR | Hamming |
|---------|--------|--------|-----|---------|
| Wood | Xun ☴ (011) | Zhen ☳ (100) | 111 | 3 |
| Fire | Li ☲ (101) | (singleton) | — | — |
| Earth | Kun ☷ (000) | Gen ☶ (001) | 001 | 1 |
| Metal | Dui ☱ (110) | Qian ☰ (111) | 001 | 1 |
| Water | Kan ☵ (010) | (singleton) | — | — |

### 2.2 生 (Generation) Relationship Structure

All trigram pairs where element(src) generates element(tgt).

| Edge | Src trig | Tgt trig | XOR | Hamming |
|------|----------|----------|-----|---------|
| Wood→Fire | Xun ☴ (011) | Li ☲ (101) | 110 | 2 |
| Wood→Fire | Zhen ☳ (100) | Li ☲ (101) | 001 | 1 |
| Fire→Earth | Li ☲ (101) | Kun ☷ (000) | 101 | 2 |
| Fire→Earth | Li ☲ (101) | Gen ☶ (001) | 100 | 1 |
| Earth→Metal | Kun ☷ (000) | Dui ☱ (110) | 110 | 2 |
| Earth→Metal | Kun ☷ (000) | Qian ☰ (111) | 111 | 3 |
| Earth→Metal | Gen ☶ (001) | Dui ☱ (110) | 111 | 3 |
| Earth→Metal | Gen ☶ (001) | Qian ☰ (111) | 110 | 2 |
| Metal→Water | Dui ☱ (110) | Kan ☵ (010) | 100 | 1 |
| Metal→Water | Qian ☰ (111) | Kan ☵ (010) | 101 | 2 |
| Water→Wood | Kan ☵ (010) | Xun ☴ (011) | 001 | 1 |
| Water→Wood | Kan ☵ (010) | Zhen ☳ (100) | 110 | 2 |

**生 Hamming distribution:** {1: 4, 2: 6, 3: 2}
**生 mean Hamming:** 1.8333

### 2.3 克 (Overcoming) Relationship Structure

All trigram pairs where element(src) overcomes element(tgt).

| Edge | Src trig | Tgt trig | XOR | Hamming |
|------|----------|----------|-----|---------|
| Wood→Earth | Xun ☴ (011) | Kun ☷ (000) | 011 | 2 |
| Wood→Earth | Xun ☴ (011) | Gen ☶ (001) | 010 | 1 |
| Wood→Earth | Zhen ☳ (100) | Kun ☷ (000) | 100 | 1 |
| Wood→Earth | Zhen ☳ (100) | Gen ☶ (001) | 101 | 2 |
| Earth→Water | Kun ☷ (000) | Kan ☵ (010) | 010 | 1 |
| Earth→Water | Gen ☶ (001) | Kan ☵ (010) | 011 | 2 |
| Water→Fire | Kan ☵ (010) | Li ☲ (101) | 111 | 3 |
| Fire→Metal | Li ☲ (101) | Dui ☱ (110) | 011 | 2 |
| Fire→Metal | Li ☲ (101) | Qian ☰ (111) | 010 | 1 |
| Metal→Wood | Dui ☱ (110) | Xun ☴ (011) | 101 | 2 |
| Metal→Wood | Dui ☱ (110) | Zhen ☳ (100) | 010 | 1 |
| Metal→Wood | Qian ☰ (111) | Xun ☴ (011) | 100 | 1 |
| Metal→Wood | Qian ☰ (111) | Zhen ☳ (100) | 011 | 2 |

**克 Hamming distribution:** {1: 6, 2: 6, 3: 1}
**克 mean Hamming:** 1.6154

### 2.4 Full 8×8 Trigram Interaction Matrix

体 (rows) × 用 (columns). Cell = Hamming distance / relation initial.

|  体\用  | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|--------|----|----|----|----|----|----|----|----|
| 000 | d0H | d1H | d1F | d2X | d1X | d2A | d2D | d3D |
| 001 | d1H | d0H | d2F | d1X | d2X | d1A | d3D | d2D |
| 010 | d1X | d2X | d0H | d1D | d2D | d3F | d1A | d2A |
| 011 | d2F | d1F | d1A | d0H | d3H | d2D | d2X | d1X |
| 100 | d1F | d2F | d2A | d3H | d0H | d1D | d1X | d2X |
| 101 | d2D | d1D | d3X | d2A | d1A | d0H | d2F | d1F |
| 110 | d2A | d3A | d1D | d2F | d1F | d2X | d0H | d1H |
| 111 | d3A | d2A | d2D | d1F | d2F | d1X | d1H | d0H |

Legend: d=Hamming distance, H=比和(harmonious), A=生体(auspicious), X=克体(harmful), D=体生用(draining), F=体克用(favorable)

### 2.5 Hamming Distance by Five-Phase Relationship

Excluding self-pairs (a=b). How does each relationship distribute over Hamming distances?

| Relation | d=0 | d=1 | d=2 | d=3 | Total | Mean d |
|----------|-----|-----|-----|-----|-------|--------|
| 比和 | 0 | 4 | 0 | 2 | 6 | 1.6667 |
| 生体 | 0 | 4 | 6 | 2 | 12 | 1.8333 |
| 克体 | 0 | 6 | 6 | 1 | 13 | 1.6154 |
| 体生用 | 0 | 4 | 6 | 2 | 12 | 1.8333 |
| 体克用 | 0 | 6 | 6 | 1 | 13 | 1.6154 |

**Key finding:** Do 生 and 克 differ systematically in Hamming profile?

- 生 (generation): mean d = 1.8333
- 克 (overcoming): mean d = 1.6154
- **Result:** Differ by 0.2179 — 生 is more distant.

## Q6: Five-Phase Cycle as Combinatorial Object

### Enumeration

Total valid surjections (8 trigrams → 5 elements, partition 2,2,2,1,1): **50400**

Traditional assignment found at index: 18371

### Traditional Assignment Scores

| Metric | 生 (generation) | 克 (overcoming) | Overall |
|--------|-----------------|-----------------|---------|
| Mean Hamming | 1.8333 | 1.6154 | — |
| Complement fraction (d=3) | 0.1667 | 0.0769 | — |
| Intra-element Hamming | — | — | 1.6667 |
| Edge pair count | 12 | 13 | — |

### Ranking Among All 50400 Assignments

| Metric | Traditional value | Percentile | Interpretation |
|--------|-------------------|------------|----------------|
| 生 mean Hamming | 1.8333 | 77.4% | moderate |
| 克 mean Hamming | 1.6154 | 34.3% | average |
| 生 complement frac | 0.1667 | 75.2% | moderate |
| 克 complement frac | 0.0769 | 25.7% | average |
| Intra-element Hamming | 1.6667 | 64.8% | average |

### Distribution Summaries

**生 mean Hamming:** min=1.3077, max=2.1667, mean=1.7143, std=0.1684, traditional=1.8333
**克 mean Hamming:** min=1.3077, max=2.1667, mean=1.7143, std=0.1684, traditional=1.6154
**生 complement fraction:** min=0.0000, max=0.3333, mean=0.1429, std=0.0842, traditional=0.1667
**克 complement fraction:** min=0.0000, max=0.3333, mean=0.1429, std=0.0842, traditional=0.0769
**Intra-element mean Hamming:** min=1.0000, max=3.0000, mean=1.7143, std=0.4302, traditional=1.6667

### Histogram: 生 Mean Hamming Distance

```
   1.30- 1.34 | ████ 840
   1.34- 1.39 | ███ 720
   1.39- 1.43 | ███ 720
   1.43- 1.47 | ███████ 1320
   1.47- 1.52 | █████████████ 2520
   1.52- 1.56 | ███████████████ 2880
   1.56- 1.61 | ██████████████████ 3360
   1.61- 1.65 | ██████████████████████████ 4920
   1.65- 1.69 | █████████████████████████████████████████████████ 9120
   1.69- 1.74 |  0
   1.74- 1.78 | ██████████████████████████████████████████████████ 9240
   1.78- 1.83 |  0
   1.83- 1.87 | ███████████████████████████████████ 6480 ◄ TRAD
   1.87- 1.91 |  0
   1.91- 1.96 | █████████████████████████ 4800
   1.96- 2.00 | ███████ 1440
   2.00- 2.04 |  0
   2.04- 2.09 | ███████ 1440
   2.09- 2.13 |  0
   2.13- 2.18 | ███ 600
```

### Histogram: 克 Mean Hamming Distance

```
   1.30- 1.34 | ████ 840
   1.34- 1.39 | ███ 720
   1.39- 1.43 | ███ 720
   1.43- 1.47 | ███████ 1320
   1.47- 1.52 | █████████████ 2520
   1.52- 1.56 | ███████████████ 2880
   1.56- 1.61 | ██████████████████ 3360
   1.61- 1.65 | ██████████████████████████ 4920 ◄ TRAD
   1.65- 1.69 | █████████████████████████████████████████████████ 9120
   1.69- 1.74 |  0
   1.74- 1.78 | ██████████████████████████████████████████████████ 9240
   1.78- 1.83 |  0
   1.83- 1.87 | ███████████████████████████████████ 6480
   1.87- 1.91 |  0
   1.91- 1.96 | █████████████████████████ 4800
   1.96- 2.00 | ███████ 1440
   2.00- 2.04 |  0
   2.04- 2.09 | ███████ 1440
   2.09- 2.13 |  0
   2.13- 2.18 | ███ 600
```

## Structural Analysis

### Observation 1: 体/用 Hamming is EXACTLY the baseline (theorem)

The 体/用 Hamming distribution is identical to the baseline 8×8 distribution.
This is not empirical — it is a structural theorem: each hexagram contributes 3 copies
of (upper, lower) and 3 copies of (lower, upper), so over all 64 hexagrams, every ordered
trigram pair (a, b) appears exactly 6 times. The 体/用 decomposition samples ALL trigram
pairs uniformly. The five-phase evaluation layer operates on a perfectly representative
sample — no bias toward opposition or similarity.

### Observation 2: Intra-element Hamming structure

- Metal: 110 ⊕ 111 = 001, d=1
- Wood: 011 ⊕ 100 = 111, d=3
- Earth: 000 ⊕ 001 = 001, d=1

Metal and Earth pair trigrams at d=1 (minimal perturbation); Wood pairs at d=3 (complement).
Traditional intra-element mean Hamming = 1.6667.

### Observation 3: 生 vs 克 Hamming profiles

生 mean: 1.8333, 克 mean: 1.6154
Difference: 0.2179.
生 edges connect more Hamming-distant trigrams than 克 edges.

### Observation 4: Traditional assignment ranking

Among 50400 valid assignments:
- 生 Hamming: percentile 77.4%
- 克 Hamming: percentile 34.3%
- 生 complement frac: percentile 75.2%
- 克 complement frac: percentile 25.7%
- Intra-element Hamming: percentile 64.8%

The traditional assignment is **moderately unusual** on some metrics —
not random but not maximally extreme either.
