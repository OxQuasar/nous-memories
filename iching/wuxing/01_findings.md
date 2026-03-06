# Phase A: Trigram Cube Geometry & Inner Space Element Mapping

## Probe 1: Element Classes on Z₂³

### 1a. Geometric Character of Element Classes

| Element | Trigrams | Values | Size | XOR mask | Hamming | Geometry |
|---------|----------|--------|------|----------|---------|----------|
| Wood 木 | Zhen(001), Xun(110) | 001,110 | 2 | 111 | 3 | body diagonal |
| Fire 火 | Li(101) | 101 | 1 | — | — | singleton |
| Earth 土 | Kun(000), Gen(100) | 000,100 | 2 | 100 | 1 | edge |
| Metal 金 | Dui(011), Qian(111) | 011,111 | 2 | 100 | 1 | edge |
| Water 水 | Kan(010) | 010 | 1 | — | — | singleton |

**Observations:**
- Metal(111,011) and Earth(000,100): both edge pairs, XOR=100 (differ only in bit 2)
- Wood(001,110): complement pair, XOR=111, d=3 (body diagonal)
- Fire(101) and Water(010): singletons, mutual complements (XOR=111, d=3)
- **Metal and Earth share the same XOR mask (100)** — bit 2 is the free variable within both

### Complement Pairing within 五行

| Trigram | Value | Complement | Comp value | Same element? |
|--------|-------|------------|------------|---------------|
| Kun ☷ | 000 | Qian ☰ | 111 | ✗ — Earth vs Metal |
| Zhen ☳ | 001 | Xun ☴ | 110 | ✓ — both Wood |
| Kan ☵ | 010 | Li ☲ | 101 | ✗ — Water vs Fire |
| Dui ☱ | 011 | Gen ☶ | 100 | ✗ — Metal vs Earth |
| Gen ☶ | 100 | Dui ☱ | 011 | ✗ — Earth vs Metal |
| Li ☲ | 101 | Kan ☵ | 010 | ✗ — Fire vs Water |
| Xun ☴ | 110 | Zhen ☳ | 001 | ✓ — both Wood |
| Qian ☰ | 111 | Kun ☷ | 000 | ✗ — Metal vs Earth |

Only Wood has intra-class complement pairing. Fire↔Water are cross-class complements.

### 1b. 生 and 克 Cycles on the Cube

#### 生 (generation): Wood→Fire→Earth→Metal→Water→Wood

**Wood → Fire** (2 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Zhen(001) | Li(101) | 100 | 1 | edge |
| Xun(110) | Li(101) | 011 | 2 | face diagonal |

**Fire → Earth** (2 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Li(101) | Kun(000) | 101 | 2 | face diagonal |
| Li(101) | Gen(100) | 001 | 1 | edge |

**Earth → Metal** (4 pairs, mean d=2.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Kun(000) | Dui(011) | 011 | 2 | face diagonal |
| Kun(000) | Qian(111) | 111 | 3 | body diagonal |
| Gen(100) | Dui(011) | 111 | 3 | body diagonal |
| Gen(100) | Qian(111) | 011 | 2 | face diagonal |

**Metal → Water** (2 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Dui(011) | Kan(010) | 001 | 1 | edge |
| Qian(111) | Kan(010) | 101 | 2 | face diagonal |

**Water → Wood** (2 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Kan(010) | Zhen(001) | 011 | 2 | face diagonal |
| Kan(010) | Xun(110) | 100 | 1 | edge |

**生 (generation) summary:**
- Overall mean Hamming: 1.8333
- XOR masks used: {001, 011, 100, 101, 111}
- Edge means: [1.50, 1.50, 2.50, 1.50, 1.50]

#### 克 (overcoming): Wood→Earth→Water→Fire→Metal→Wood

**Wood → Earth** (4 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Zhen(001) | Kun(000) | 001 | 1 | edge |
| Zhen(001) | Gen(100) | 101 | 2 | face diagonal |
| Xun(110) | Kun(000) | 110 | 2 | face diagonal |
| Xun(110) | Gen(100) | 010 | 1 | edge |

**Earth → Water** (2 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Kun(000) | Kan(010) | 010 | 1 | edge |
| Gen(100) | Kan(010) | 110 | 2 | face diagonal |

**Water → Fire** (1 pair, mean d=3.00)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Kan(010) | Li(101) | 111 | 3 | body diagonal |

**Fire → Metal** (2 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Li(101) | Dui(011) | 110 | 2 | face diagonal |
| Li(101) | Qian(111) | 010 | 1 | edge |

**Metal → Wood** (4 pairs, mean d=1.50)

| Source | Target | XOR | d | Geometry |
|--------|--------|-----|---|----------|
| Dui(011) | Zhen(001) | 010 | 1 | edge |
| Dui(011) | Xun(110) | 101 | 2 | face diagonal |
| Qian(111) | Zhen(001) | 110 | 2 | face diagonal |
| Qian(111) | Xun(110) | 001 | 1 | edge |

**克 (overcoming) summary:**
- Overall mean Hamming: 1.6154
- XOR masks used: {001, 010, 101, 110, 111}
- Edge means: [1.50, 1.50, 3.00, 1.50, 1.50]

#### Geometric Character of Cycles

- 生 XOR vocabulary: {001, 011, 100, 101, 111} (5 masks)
- 克 XOR vocabulary: {001, 010, 101, 110, 111} (5 masks)
- Shared: {001, 101, 111}
- 生 only: {011, 100}
- 克 only: {010, 110}

**Is 生 a rotation of the cube?** No — a rotation would use a single XOR mask (or composition of fixed symmetry operations). 生 uses multiple XOR masks and visits vertices at varying Hamming distances. It is **geometrically irregular**.

**Is 克 a rotation?** Same verdict — geometrically irregular.

Neither cycle traces a Hamiltonian path on the cube graph. The element→trigram fan-out (2 trigrams per 2-member element) breaks any single-path interpretation.

### 1c. Bit-2 Partition Hypothesis

#### Trigrams tabulated by (b₀, b₁) and b₂

| (b₀,b₁) | b₂=0 | b₂=1 |
|----------|------|------|
| (0, 0) | Kun=Earth | Gen=Earth |
| (0, 1) | Kan=Water | Xun=Wood |
| (1, 0) | Zhen=Wood | Li=Fire |
| (1, 1) | Dui=Metal | Qian=Metal |

#### Does (b₀, b₁) determine element?

- (b₀,b₁)=(0, 0): elements = {'Earth'} → ✓ pure
- (b₀,b₁)=(0, 1): elements = {'Wood', 'Water'} → ✗ mixed: {'Wood', 'Water'}
- (b₀,b₁)=(1, 0): elements = {'Wood', 'Fire'} → ✗ mixed: {'Wood', 'Fire'}
- (b₀,b₁)=(1, 1): elements = {'Metal'} → ✓ pure

**(b₀, b₁) does NOT cleanly partition elements.**

#### Partition by (b₀, b₁)

| (b₀,b₁) | Elements | Trigrams |
|----------|----------|----------|
| (0, 0) | Earth | Kun, Gen |
| (0, 1) | Water, Wood | Kan, Xun |
| (1, 0) | Fire, Wood | Zhen, Li |
| (1, 1) | Metal | Dui, Qian |

#### Refined bit-2 analysis

Within Metal: Qian(111) vs Dui(011) — differ in b₂ only ✓
Within Earth: Kun(000) vs Gen(100) — differ in b₂ only ✓
Within Wood: Zhen(001) vs Xun(110) — differ in ALL bits ✗
Fire(101): b₂=1, b₁=0, b₀=1
Water(010): b₂=0, b₁=1, b₀=0

**Conclusion:** Bit 2 is the *intra-class* degree of freedom for Metal and Earth. It is NOT a clean partition axis. The 五行 map cannot be expressed as a function of any single-bit or two-bit projection. Wood's complement structure (XOR=111) requires all 3 bits, which is incompatible with any linear partition.

## Probe 2: 五行 on the 16-Node Inner Space

### 2a. Element Pairs for All 16 Inner States

| v | bits | Lower nuc | Upper nuc | Lo elem | Up elem | Pair relation | Basin | Depth |
|---|------|-----------|-----------|---------|---------|---------------|-------|-------|
|  0 | 0000 |   Kun(000) |   Kun(000) |  Earth |  Earth |    比 |   Kun | 0 ★ |
|  1 | 0001 |  Zhen(001) |   Kun(000) |   Wood |  Earth |   克→ |   Kun | 1 |
|  2 | 0010 |   Kan(010) |  Zhen(001) |  Water |   Wood |   生→ | Cycle | 1 |
|  3 | 0011 |   Dui(011) |  Zhen(001) |  Metal |   Wood |   克→ | Cycle | 1 |
|  4 | 0100 |   Gen(100) |   Kan(010) |  Earth |  Water |   克→ | Cycle | 1 |
|  5 | 0101 |    Li(101) |   Kan(010) |   Fire |  Water |   ←克 | Cycle | 0 ★ |
|  6 | 0110 |   Xun(110) |   Dui(011) |   Wood |  Metal |   ←克 |  Qian | 1 |
|  7 | 0111 |  Qian(111) |   Dui(011) |  Metal |  Metal |    比 |  Qian | 1 |
|  8 | 1000 |   Kun(000) |   Gen(100) |  Earth |  Earth |    比 |   Kun | 1 |
|  9 | 1001 |  Zhen(001) |   Gen(100) |   Wood |  Earth |   克→ |   Kun | 1 |
| 10 | 1010 |   Kan(010) |    Li(101) |  Water |   Fire |   克→ | Cycle | 0 ★ |
| 11 | 1011 |   Dui(011) |    Li(101) |  Metal |   Fire |   ←克 | Cycle | 1 |
| 12 | 1100 |   Gen(100) |   Xun(110) |  Earth |   Wood |   ←克 | Cycle | 1 |
| 13 | 1101 |    Li(101) |   Xun(110) |   Fire |   Wood |   ←生 | Cycle | 1 |
| 14 | 1110 |   Xun(110) |  Qian(111) |   Wood |  Metal |   ←克 |  Qian | 1 |
| 15 | 1111 |  Qian(111) |  Qian(111) |  Metal |  Metal |    比 |  Qian | 0 ★ |

### 2b. Element Pairs × Basin Cross-Tabulation

**Realized element pairs:** 12 of 25 possible

| Basin | # States | Element pairs (lo/up) |
|-------|----------|-----------------------|
| Kun | 4 | Earth/Earth, Wood/Earth |
| Cycle | 8 | Earth/Water, Earth/Wood, Fire/Water, Fire/Wood, Metal/Fire, Metal/Wood, Water/Fire, Water/Wood |
| Qian | 4 | Metal/Metal, Wood/Metal |

**Absent element pairs (13):**

  Earth/Fire, Earth/Metal, Fire/Earth, Fire/Fire, Fire/Metal
  Metal/Earth, Metal/Water, Water/Earth, Water/Metal, Water/Water
  Wood/Fire, Wood/Water, Wood/Wood

### 2c. Analysis

#### Five-phase relation between nuclear trigrams, by basin

| Basin | 比 | 生→ | ←生 | 克→ | ←克 |
|-------|----|-----|-----|-----|-----|
| Kun | 2 | 0 | 0 | 2 | 0 |
| Cycle | 0 | 1 | 1 | 3 | 3 |
| Qian | 2 | 0 | 0 | 0 | 2 |

#### Fixed-point basin constraint

In fixed-point basins, the interface bits (b₂,b₃) are identical (both 0 or both 1).

**Kun basin** (interface=(0, 0)):
  - Upper nuclear = (b₂,b₃,b₄) with b₂=b₃=0: upper trigram ∈ {Gen, Kun}
  - Upper elements: {'Earth'} → always same element = **Earth**
  - Lower nuclear = (b₁,b₂,b₃) with b₂=b₃=0: lower trigram ∈ {Kun, Zhen}
  - Lower elements: {'Earth', 'Wood'}

**Qian basin** (interface=(1, 1)):
  - Upper nuclear = (b₂,b₃,b₄) with b₂=b₃=1: upper trigram ∈ {Dui, Qian}
  - Upper elements: {'Metal'} → always same element = **Metal**
  - Lower nuclear = (b₁,b₂,b₃) with b₂=b₃=1: lower trigram ∈ {Qian, Xun}
  - Lower elements: {'Metal', 'Wood'}

**Verdict:** Upper nuclear is element-pure within fixed-point basins — forced by the overlap constraint. Lower nuclear varies (1 free bit toggles between 2 trigrams with potentially different elements).

**Cycle basin:** 8 states, relations present: {生→, ←生, 克→, ←克}

### 2d. Attractor Element Flow

#### Attractor 0 (Kun/Kun): Earth/Earth [Kun basin]

| Feeder | bits | Lo elem | Up elem | Lo→Attr rel | Up→Attr rel | Chain |
|--------|------|---------|---------|-------------|-------------|-------|
|  1 | 0001 |   Wood |  Earth |    克→ |     比 | 1→0 |
|  8 | 1000 |  Earth |  Earth |     比 |     比 | 8→0 |
|  9 | 1001 |   Wood |  Earth |    克→ |     比 | 9→0 |

#### Attractor 5 (Li/Kan): Fire/Water [Cycle basin]

| Feeder | bits | Lo elem | Up elem | Lo→Attr rel | Up→Attr rel | Chain |
|--------|------|---------|---------|-------------|-------------|-------|
|  2 | 0010 |  Water |   Wood |    克→ |    ←生 | 2→5 |
|  3 | 0011 |  Metal |   Wood |    ←克 |    ←生 | 3→5 |
| 11 | 1011 |  Metal |   Fire |    ←克 |    ←克 | 11→5 |

#### Attractor 10 (Kan/Li): Water/Fire [Cycle basin]

| Feeder | bits | Lo elem | Up elem | Lo→Attr rel | Up→Attr rel | Chain |
|--------|------|---------|---------|-------------|-------------|-------|
|  4 | 0100 |  Earth |  Water |    克→ |    克→ | 4→10 |
| 12 | 1100 |  Earth |   Wood |    克→ |    生→ | 12→10 |
| 13 | 1101 |   Fire |   Wood |    ←克 |    生→ | 13→10 |

#### Attractor 15 (Qian/Qian): Metal/Metal [Qian basin]

| Feeder | bits | Lo elem | Up elem | Lo→Attr rel | Up→Attr rel | Chain |
|--------|------|---------|---------|-------------|-------------|-------|
|  6 | 0110 |   Wood |  Metal |    ←克 |     比 | 6→15 |
|  7 | 0111 |  Metal |  Metal |     比 |     比 | 7→15 |
| 14 | 1110 |   Wood |  Metal |    ←克 |     比 | 14→15 |

#### Convergence relation summary

| Position | 比 | 生→ | ←生 | 克→ | ←克 | Total |
|----------|----|-----|-----|-----|-----|-------|
| Lower | 2 | 0 | 0 | 5 | 5 | 12 |
| Upper | 6 | 2 | 2 | 1 | 1 | 12 |

## Structural vs Cosmological Summary

### Algebraically necessary (given any 8→5 map with sizes 2,2,2,1,1)

- Only 16 of 64 trigram-pairs are reachable as nuclear pairs (overlap constraint)
- Fixed-point basins force upper nuclear element purity (interface bits shared)
- Each basin has exactly 4 inner states (Kun/Qian) or 8 (Cycle)
- The 1:3:12 depth ratio holds for any content of those slots

### Requires the specific traditional element assignment

- Metal and Earth share XOR mask 100 (bit 2 free) — depends on Qian↔Dui, Kun↔Gen grouping
- Wood is the only complement pair — depends on Zhen↔Xun assignment
- Fire and Water as mutual complements — depends on Li and Kan being singletons
- The specific element pairs that appear in each basin
- The distribution of 生/克/比 relations along convergence edges

### Unexpected patterns

- 12 of 25 element pairs realized → 13 absent
- Upper nuclear is always 比和 in fixed-point basins (forced by overlap + traditional assignment)
- All 5 relation types appear in Cycle basin only
- The bit-2 axis is shared by Metal AND Earth — the two elements whose trigram pairs are cube edges
