# Phase 4 Round 2: Sequential and Algebraic Structure

## A. Directed Cycle Profiles

### 生 (generation) cycle — per-edge detail

**Wood → Fire** (n=2 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Xun ☴ (011) | Li ☲ (101) | 110 | 2 |
| Zhen ☳ (100) | Li ☲ (101) | 001 | 1 |

**Fire → Earth** (n=2 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Li ☲ (101) | Kun ☷ (000) | 101 | 2 |
| Li ☲ (101) | Gen ☶ (001) | 100 | 1 |

**Earth → Metal** (n=4 pairs, mean d=2.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Kun ☷ (000) | Dui ☱ (110) | 110 | 2 |
| Kun ☷ (000) | Qian ☰ (111) | 111 | 3 |
| Gen ☶ (001) | Dui ☱ (110) | 111 | 3 |
| Gen ☶ (001) | Qian ☰ (111) | 110 | 2 |

**Metal → Water** (n=2 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Dui ☱ (110) | Kan ☵ (010) | 100 | 1 |
| Qian ☰ (111) | Kan ☵ (010) | 101 | 2 |

**Water → Wood** (n=2 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Kan ☵ (010) | Xun ☴ (011) | 001 | 1 |
| Kan ☵ (010) | Zhen ☳ (100) | 110 | 2 |

**生 overall:** mean d = 1.8333, variance of edge means = 0.1600
**Edge means:** ['1.50', '1.50', '2.50', '1.50', '1.50']

### 克 (overcoming) cycle — per-edge detail

**Wood → Earth** (n=4 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Xun ☴ (011) | Kun ☷ (000) | 011 | 2 |
| Xun ☴ (011) | Gen ☶ (001) | 010 | 1 |
| Zhen ☳ (100) | Kun ☷ (000) | 100 | 1 |
| Zhen ☳ (100) | Gen ☶ (001) | 101 | 2 |

**Earth → Water** (n=2 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Kun ☷ (000) | Kan ☵ (010) | 010 | 1 |
| Gen ☶ (001) | Kan ☵ (010) | 011 | 2 |

**Water → Fire** (n=1 pairs, mean d=3.00)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Kan ☵ (010) | Li ☲ (101) | 111 | 3 |

**Fire → Metal** (n=2 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Li ☲ (101) | Dui ☱ (110) | 011 | 2 |
| Li ☲ (101) | Qian ☰ (111) | 010 | 1 |

**Metal → Wood** (n=4 pairs, mean d=1.50)

| Source | Target | XOR | Hamming |
|--------|--------|-----|---------|
| Dui ☱ (110) | Xun ☴ (011) | 101 | 2 |
| Dui ☱ (110) | Zhen ☳ (100) | 010 | 1 |
| Qian ☰ (111) | Xun ☴ (011) | 100 | 1 |
| Qian ☰ (111) | Zhen ☳ (100) | 011 | 2 |

**克 overall:** mean d = 1.6154, variance of edge means = 0.3600
**Edge means:** ['1.50', '1.50', '3.00', '1.50', '1.50']

### Asymmetry statistic (生 − 克 mean Hamming)

**Traditional value:** 0.2179

**Distribution (n=50400):** min=-0.8590, max=0.8590, mean=-0.0000, std=0.3206
**Traditional percentile:** 76.9%

```
  -0.869 to -0.782 | ██ 360
  -0.782 to -0.695 | ███████ 960
  -0.695 to -0.608 | ███████ 960
  -0.608 to -0.521 | ███ 480
  -0.521 to -0.434 | █████ 720
  -0.434 to -0.348 | ███████████████████████ 3000
  -0.348 to -0.261 | ████████████████████████████████ 4200
  -0.261 to -0.174 | █████████████████████████████████████ 4920
  -0.174 to -0.087 | ████████████████████████ 3120
  -0.087 to +0.000 | ██████████████████████████████████████████████████ 6480
  +0.000 to +0.087 | ██████████████████████████████████████████████████ 6480
  +0.087 to +0.174 | ████████████████████████ 3120
  +0.174 to +0.261 | █████████████████████████████████████ 4920 ◄ TRAD
  +0.261 to +0.348 | ████████████████████████████████ 4200
  +0.348 to +0.434 | ███████████████████████ 3000
  +0.434 to +0.521 | █████ 720
  +0.521 to +0.608 | ███ 480
  +0.608 to +0.695 | ███████ 960
  +0.695 to +0.782 | ███████ 960
  +0.782 to +0.869 | ██ 360
```

### Per-edge variance of Hamming distances

| Metric | Traditional | Mean | Std | Percentile |
|--------|-------------|------|-----|------------|
| 生 edge-mean variance | 0.1600 | 0.1646 | 0.1064 | 62.9% |
| 克 edge-mean variance | 0.3600 | 0.1646 | 0.1064 | 96.2% |

## B. XOR Mask Algebra

### 生 cycle masks

**Masks:** {001, 100, 101, 110, 111}
**Count:** 5 of 7 nonzero masks
**XOR-closure:** {000, 001, 010, 011, 100, 101, 110, 111}
**Closure size:** 8 (= Z₂³)
**Generates full Z₂³?** True

### 克 cycle masks

**Masks:** {010, 011, 100, 101, 111}
**Count:** 5 of 7 nonzero masks
**XOR-closure:** {000, 001, 010, 011, 100, 101, 110, 111}
**Closure size:** 8 (= Z₂³)
**Generates full Z₂³?** True

### Mask overlap

| Category | Masks | Count |
|----------|-------|-------|
| 生 only | {001, 110} | 2 |
| 克 only | {010, 011} | 2 |
| Both | {100, 101, 111} | 3 |
| Neither | {} | 0 |

### Comparison with n=3 KW vocabulary

The n=3 KW pairing (complement) uses a single mask: {111}.
- 生 edges include mask 111: **True**
- 克 edges include mask 111: **True**

The n=3 KW-style pairing (reversal for the size-4 orbit) would use masks {001, 110}.
- 生 ∩ KW-style: {001, 110}
- 克 ∩ KW-style: {}

## C. Partner Agreement Null Model

**Traditional agreement rate:** 0.2500 (= 48/192)
**Distribution:** min=0.1562, max=0.5938, mean=0.3001, std=0.0896
**Traditional percentile:** 41.4%

```
  0.151-0.174 | ██ 480
  0.174-0.196 | ███████████████████ 3840
  0.196-0.218 |  0
  0.218-0.241 | ██████████████████████████████████ 6960
  0.241-0.263 | ███████████████████████████████████████████████ 9600 ◄ TRAD
  0.263-0.285 | ██████████████████████████████████████████████████ 10080
  0.285-0.308 |  0
  0.308-0.330 | ██████████████████████ 4560
  0.330-0.353 | █████████████████████ 4320
  0.353-0.375 |  0
  0.375-0.397 | ███████████████████ 3840
  0.397-0.420 | ███████████ 2400
  0.420-0.442 | █ 240
  0.442-0.464 |  0
  0.464-0.487 | ██ 480
  0.487-0.509 | █ 240
  0.509-0.532 | ███████████████ 3120
  0.532-0.554 |  0
  0.554-0.576 |  0
  0.576-0.599 | █ 240
```

## D. Shell-Only Pairs Under 生克

### Shell-only pairs (signature (1,0,0))

These 4 KW pairs differ only at L1 and L6 — identical nuclear cores.

**000001 ↔ 100000**

| Line | 体(a) | 用(a) | rel(a) | 体(b) | 用(b) | rel(b) | Agree? |
|------|-------|-------|--------|-------|-------|--------|--------|
| 1 | 000 | 001 | 比和 | 100 | 000 | 体克用 | ✗ |
| 2 | 000 | 001 | 比和 | 100 | 000 | 体克用 | ✗ |
| 3 | 000 | 001 | 比和 | 100 | 000 | 体克用 | ✗ |
| 4 | 001 | 000 | 比和 | 000 | 100 | 克体 | ✗ |
| 5 | 001 | 000 | 比和 | 000 | 100 | 克体 | ✗ |
| 6 | 001 | 000 | 比和 | 000 | 100 | 克体 | ✗ |

**001101 ↔ 101100**

| Line | 体(a) | 用(a) | rel(a) | 体(b) | 用(b) | rel(b) | Agree? |
|------|-------|-------|--------|-------|-------|--------|--------|
| 1 | 001 | 101 | 生体 | 101 | 100 | 生体 | ✓ |
| 2 | 001 | 101 | 生体 | 101 | 100 | 生体 | ✓ |
| 3 | 001 | 101 | 生体 | 101 | 100 | 生体 | ✓ |
| 4 | 101 | 001 | 体生用 | 100 | 101 | 体生用 | ✓ |
| 5 | 101 | 001 | 体生用 | 100 | 101 | 体生用 | ✓ |
| 6 | 101 | 001 | 体生用 | 100 | 101 | 体生用 | ✓ |

**010011 ↔ 110010**

| Line | 体(a) | 用(a) | rel(a) | 体(b) | 用(b) | rel(b) | Agree? |
|------|-------|-------|--------|-------|-------|--------|--------|
| 1 | 010 | 011 | 体生用 | 110 | 010 | 体生用 | ✓ |
| 2 | 010 | 011 | 体生用 | 110 | 010 | 体生用 | ✓ |
| 3 | 010 | 011 | 体生用 | 110 | 010 | 体生用 | ✓ |
| 4 | 011 | 010 | 生体 | 010 | 110 | 生体 | ✓ |
| 5 | 011 | 010 | 生体 | 010 | 110 | 生体 | ✓ |
| 6 | 011 | 010 | 生体 | 010 | 110 | 生体 | ✓ |

**011111 ↔ 111110**

| Line | 体(a) | 用(a) | rel(a) | 体(b) | 用(b) | rel(b) | Agree? |
|------|-------|-------|--------|-------|-------|--------|--------|
| 1 | 011 | 111 | 克体 | 111 | 110 | 比和 | ✗ |
| 2 | 011 | 111 | 克体 | 111 | 110 | 比和 | ✗ |
| 3 | 011 | 111 | 克体 | 111 | 110 | 比和 | ✗ |
| 4 | 111 | 011 | 体克用 | 110 | 111 | 比和 | ✗ |
| 5 | 111 | 011 | 体克用 | 110 | 111 | 比和 | ✗ |
| 6 | 111 | 011 | 体克用 | 110 | 111 | 比和 | ✗ |

### Agreement rate comparison

| Category | Agree | Total | Rate |
|----------|-------|-------|------|
| Shell-only (4 pairs) | 12 | 24 | 0.5000 |
| Depth-penetrating (28 pairs) | 36 | 168 | 0.2143 |
| All (32 pairs) | 48 | 192 | 0.2500 |

**Shell-only / Depth ratio:** 2.33×
Shell-only pairs show **substantially more agreement** — as expected,
since their trigrams are nearly identical (only L1/L6 differ).

## E. 变卦 Opposition Map

### 本卦 → 变卦 opposition type

Flipping one line always gives Hamming distance 1 at the hexagram level.

| Hex-level relation | Count | Fraction |
|-------------------|-------|----------|
| other | 384 | 1.0000 |

### 互卦(本) vs 互卦(变) opposition type

How does flipping one line propagate through the 互卦 map?

| 互卦-level relation | Count | Fraction |
|-------------------|-------|----------|
| other | 256 | 0.6667 |
| identity | 128 | 0.3333 |

| 互卦 Hamming | Count | Fraction |
|-------------|-------|----------|
| 0 | 128 | 0.3333 |
| 1 | 128 | 0.3333 |
| 2 | 128 | 0.3333 |

### Line position → 互卦 Hamming

Which moving lines are visible to the 互卦 map?

| Moving line | 互卦 Hamming | Visible? |
|------------|-------------|----------|
| L1 (bit 0) | 0 | no (erased) |
| L2 (bit 1) | 1 | yes |
| L3 (bit 2) | 2 | yes |
| L4 (bit 3) | 2 | yes |
| L5 (bit 4) | 1 | yes |
| L6 (bit 5) | 0 | no (erased) |

### 本卦→互卦→变卦 evaluation circuit

For each (hexagram, moving_line) state, the triple of five-phase relations:

1. **本卦:** 体/用 relation of the original hexagram
2. **互卦:** 体/用 relation using nuclear trigrams (体 position inherited)
3. **变卦:** 体/用 relation of the changed hexagram

### Repetition pattern

| # unique relations | Count | Fraction |
|-------------------|-------|----------|
| 1 (=all same) | 20 | 0.0521 |
| 2 (=one repeat) | 200 | 0.5208 |
| 3 (=all different) | 164 | 0.4271 |

### Most common triples (top 20)

| 本卦 | 互卦 | 变卦 | Count |
|------|------|------|-------|
| 比和 | 比和 | 体克用 | 11 |
| 比和 | 比和 | 克体 | 11 |
| 体生用 | 克体 | 克体 | 11 |
| 生体 | 体克用 | 体克用 | 11 |
| 体生用 | 克体 | 体生用 | 9 |
| 生体 | 体克用 | 生体 | 9 |
| 比和 | 比和 | 比和 | 8 |
| 体克用 | 比和 | 比和 | 8 |
| 克体 | 比和 | 比和 | 8 |
| 克体 | 体克用 | 体生用 | 7 |
| 克体 | 体克用 | 比和 | 7 |
| 体克用 | 克体 | 生体 | 7 |
| 体克用 | 克体 | 比和 | 7 |
| 生体 | 体克用 | 克体 | 7 |
| 生体 | 体克用 | 体生用 | 7 |
| 体生用 | 克体 | 生体 | 7 |
| 体生用 | 克体 | 体克用 | 7 |
| 体克用 | 体克用 | 比和 | 7 |
| 克体 | 克体 | 比和 | 7 |
| 克体 | 比和 | 体生用 | 6 |

### Anti-repetition summary

- **All three same:** 20/384 = 0.0521
- **All three different:** 164/384 = 0.4271
- **One repeated:** 200/384 = 0.5208

### Step-by-step transition rates

| Transition | Changes | Rate |
|------------|---------|------|
| 本卦 → 互卦 | 276/384 | 0.7188 |
| 互卦 → 变卦 | 296/384 | 0.7708 |
| 本卦 → 变卦 | 320/384 | 0.8333 |

## Structural Analysis

### Key finding 1: Asymmetry is moderately unusual

The traditional 生−克 asymmetry (0.2179) sits at percentile 76.9%.
生 connects more distant trigrams than 克. Among 50,400 random assignments,
this is a **moderate outlier** — the directional difference is not random.

### Key finding 2: XOR masks span nearly all of Z₂³

生 uses 5 masks, 克 uses 5 masks.
Together they cover 7 of 7 nonzero masks.
生's masks alone generate the full group Z₂³ under XOR.

克's masks alone generate the full group Z₂³ under XOR.

### Key finding 3: Shell-only pairs and agreement

Shell-only agreement: 0.5000, depth-penetrating: 0.2143.
Shell-only pairs are more stable under 生克 evaluation — changing only L1/L6
often preserves the 体/用 five-phase relationship.

### Key finding 4: 互卦 erases L1/L6 flips

Flipping L1 or L6 produces **zero** change in the 互卦 —
the nuclear map is completely blind to outer-shell perturbations.
This directly connects to the shell-only pair stability above.

### Key finding 5: Evaluation circuit diversity

All-same: 5.2%, all-different: 42.7%, one-repeat: 52.1%.
The 本→互→变 circuit produces **substantial diversity** in five-phase evaluations —
the three viewpoints usually disagree, providing non-redundant information.
