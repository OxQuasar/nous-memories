# Phase B: Partition Comparison, Directed Graphs & Quotient Structure

## Probe 3: Partition Comparison

### Partition definitions

**Wuxing** (H=2.2500 bits): Earth: {Kun, Gen}; Wood: {Zhen, Xun}; Metal: {Dui, Qian}; Water: {Kan}; Fire: {Li}
**Yang count** (H=1.8113 bits): 1yang: {Zhen, Kan, Gen}; 2yang: {Dui, Li, Xun}; 0yang: {Kun}; 3yang: {Qian}
**Basin(TT)** (H=1.5000 bits): Cycle: {Zhen, Dui, Gen, Xun}; Kun: {Kun, Kan}; Qian: {Li, Qian}
**Later Heaven** (H=2.0000 bits): East: {Zhen, Xun}; South: {Kun, Li}; West: {Dui, Qian}; North: {Kan, Gen}
**Complement** (H=2.0000 bits): (0, 7): {Kun, Qian}; (1, 6): {Zhen, Xun}; (2, 5): {Kan, Li}; (3, 4): {Dui, Gen}
**b0+b1 parity** (H=1.0000 bits): p0: {Kun, Dui, Gen, Qian}; p1: {Zhen, Kan, Li, Xun}

### Mutual Information matrix

| | Wuxing | Yang count | Basin(TT) | Later Heaven | Complement | b0+b1 parity |
|---|---:|---:|---:|---:|---:|---:|
| Wuxing | 2.2500 | 1.0613 | 1.0000 | 1.7500 | 1.5000 | 1.0000 |
| Yang count | 1.0613 | 1.8113 | 0.8113 | 1.0613 | 0.8113 | 0.3113 |
| Basin(TT) | 1.0000 | 0.8113 | 1.5000 | 0.7500 | 1.0000 | 0.0000 |
| Later Heaven | 1.7500 | 1.0613 | 0.7500 | 2.0000 | 1.2500 | 0.5000 |
| Complement | 1.5000 | 0.8113 | 1.0000 | 1.2500 | 2.0000 | 1.0000 |
| b0+b1 parity | 1.0000 | 0.3113 | 0.0000 | 0.5000 | 1.0000 | 1.0000 |

### Normalized MI matrix

| | Wuxing | Yang count | Basin(TT) | Later Heaven | Complement | b0+b1 parity |
|---|---:|---:|---:|---:|---:|---:|
| Wuxing | 1.00 | 0.59 | 0.67 | 0.88 | 0.75 | 1.00 |
| Yang count | 0.59 | 1.00 | 0.54 | 0.59 | 0.45 | 0.31 |
| Basin(TT) | 0.67 | 0.54 | 1.00 | 0.50 | 0.67 | 0.00 |
| Later Heaven | 0.88 | 0.59 | 0.50 | 1.00 | 0.62 | 0.50 |
| Complement | 0.75 | 0.45 | 0.67 | 0.62 | 1.00 | 1.00 |
| b0+b1 parity | 1.00 | 0.31 | 0.00 | 0.50 | 1.00 | 1.00 |

### Key observations

**Highest NMI pairs:**

- Wuxing ↔ b0+b1 parity: NMI=1.0000, MI=1.0000 bits
- Complement ↔ b0+b1 parity: NMI=1.0000, MI=1.0000 bits
- Wuxing ↔ Later Heaven: NMI=0.8750, MI=1.7500 bits
- Wuxing ↔ Complement: NMI=0.7500, MI=1.5000 bits
- Wuxing ↔ Basin(TT): NMI=0.6667, MI=1.0000 bits

**Lowest NMI pairs:**

- Yang count ↔ Complement: NMI=0.4479, MI=0.8113 bits
- Yang count ↔ b0+b1 parity: NMI=0.3113, MI=0.3113 bits
- Basin(TT) ↔ b0+b1 parity: NMI=0.0000, MI=0.0000 bits

### Wuxing predictability

H(Wuxing) = 2.2500 bits

| Predictor X | H(Wuxing \| X) | Information gained | % of Wuxing |
|-------------|---------------|-------------------|-------------|
| Later Heaven | 0.5000 | 1.7500 | 77.8% |
| Complement | 0.7500 | 1.5000 | 66.7% |
| Yang count | 1.1887 | 1.0613 | 47.2% |
| Basin(TT) | 1.2500 | 1.0000 | 44.4% |
| b0+b1 parity | 1.2500 | 1.0000 | 44.4% |

### Pair predictors: H(Wuxing | X, Y)

| X | Y | H(Wuxing \| X,Y) | Residual % |
|---|---|-----------------|------------|
| Yang count | Complement | 0.0000 | 0.0% |
| Basin(TT) | Later Heaven | 0.0000 | 0.0% |
| Later Heaven | Complement | 0.0000 | 0.0% |
| Later Heaven | b0+b1 parity | 0.0000 | 0.0% |
| Yang count | Later Heaven | 0.2500 | 11.1% |
| Basin(TT) | Complement | 0.2500 | 11.1% |
| Basin(TT) | b0+b1 parity | 0.2500 | 11.1% |
| Yang count | Basin(TT) | 0.5000 | 22.2% |
| Yang count | b0+b1 parity | 0.5000 | 22.2% |
| Complement | b0+b1 parity | 0.7500 | 33.3% |

**Best single predictor leaves 0.5000 bits (22.2% of Wuxing)**

**Best pair predictor leaves 0.0000 bits (0.0% of Wuxing)**

→ Wuxing is fully captured by the best pair of other partitions.

## Probe 4: Directed Graphs

### 4a. Five-phase graphs on Z₂³ (8 trigrams)

| Relation | Edges | In-degree range | Out-degree range |
|----------|-------|-----------------|------------------|
| 比 (same) | 6 | 1–1 | 1–1 |
| 生→ (gen_fwd) | 12 | 1–2 | 1–2 |
| ←生 (gen_rev) | 12 | 1–2 | 1–2 |
| 克→ (over_fwd) | 13 | 1–2 | 1–2 |
| ←克 (over_rev) | 13 | 1–2 | 1–2 |

**Total:** 56 edges = 8×7 = 56 ✓ (complete digraph minus self-loops)

**生 (gen_fwd) degree by trigram:**

| Trigram | Element | Out-degree | In-degree |
|---------|---------|------------|-----------|
| Kun ☷ | Earth | 2 | 1 |
| Zhen ☳ | Wood | 1 | 1 |
| Kan ☵ | Water | 2 | 2 |
| Dui ☱ | Metal | 1 | 2 |
| Gen ☶ | Earth | 2 | 1 |
| Li ☲ | Fire | 2 | 2 |
| Xun ☴ | Wood | 1 | 1 |
| Qian ☰ | Metal | 1 | 2 |

**克 (over_fwd) degree by trigram:**

| Trigram | Element | Out-degree | In-degree |
|---------|---------|------------|-----------|
| Kun ☷ | Earth | 1 | 2 |
| Zhen ☳ | Wood | 2 | 2 |
| Kan ☵ | Water | 1 | 2 |
| Dui ☱ | Metal | 2 | 1 |
| Gen ☶ | Earth | 1 | 2 |
| Li ☲ | Fire | 2 | 1 |
| Xun ☴ | Wood | 2 | 2 |
| Qian ☰ | Metal | 2 | 1 |

### 4b. Five-phase on 16-node inner space

#### Combined relation distribution (all ordered pairs)

| Lower rel | Upper rel | Count |
|-----------|-----------|-------|
| ←克 | 生→ | 14 |
| 克→ | ←生 | 14 |
| ←生 | ←克 | 13 |
| 生→ | 克→ | 13 |
| 生→ | ←克 | 12 |
| ←生 | 克→ | 12 |
| 生→ | 生→ | 12 |
| ←生 | ←生 | 12 |
| ←克 | 比 | 11 |
| 克→ | 比 | 11 |
| ←克 | ←克 | 10 |
| 克→ | 克→ | 10 |
| 克→ | ←克 | 9 |
| ←克 | 克→ | 9 |
| 比 | 克→ | 8 |

#### Hugua edges: five-phase classification

Total hugua edges (non-self): 14

| Lower rel | Upper rel | Count | Basin |
|-----------|-----------|-------|-------|
| 克→ | 比 | 1→0 | Kun |
| 克→ | ←生 | 2→5 | Cycle |
| ←克 | ←生 | 3→5 | Cycle |
| 克→ | 克→ | 4→10 | Cycle |
| ←克 | 克→ | 5→10 | Cycle |
| ←克 | 比 | 6→15 | Qian |
| 比 | 比 | 7→15 | Qian |
| 比 | 比 | 8→0 | Kun |
| 克→ | 比 | 9→0 | Kun |
| 克→ | ←克 | 10→5 | Cycle |
| ←克 | ←克 | 11→5 | Cycle |
| 克→ | 生→ | 12→10 | Cycle |
| ←克 | 生→ | 13→10 | Cycle |
| ←克 | 比 | 14→15 | Qian |

**Hugua edges with 生 on at least one position:** 4/14

**Hugua edges with 克 on at least one position:** 12/14

**Hugua edges with SAME relation on both positions:** 4/14

#### Hugua edge relations by basin

**Kun** (3 edges):
  - (克→, 比): 2
  - (比, 比): 1

**Cycle** (8 edges):
  - (克→, ←生): 1
  - (←克, ←生): 1
  - (克→, 克→): 1
  - (←克, 克→): 1
  - (克→, ←克): 1
  - (←克, ←克): 1
  - (克→, 生→): 1
  - (←克, 生→): 1

**Qian** (3 edges):
  - (←克, 比): 2
  - (比, 比): 1

## Probe 5: Quotient Structure

### 5a. Symmetry group

|GL(3,F₂)| = 168

**Linear symmetries preserving Wuxing:** 1

**Affine symmetries preserving Wuxing:** 2

Linear symmetries (matrices A where A preserves each element class):

```
  [1 0 0]
  [0 1 0]
  [0 0 1]
```
  Action: identity

Additional affine symmetries (Ax+b with b≠0):

- b=100: 000→100, 001→001, 010→010, 011→111, 100→000, 101→101, 110→110, 111→011

*Note: these count symmetries preserving each **named** element class (Earth→Earth, Metal→Metal, etc.). The unlabeled partition automorphism group (allowing class permutation) is larger — see §5d.*

### 5b. Algebraic decomposition

H(Wuxing) = 2.2500 bits

**Decomposition hierarchy:**

1. b₀⊕b₁ parity → H(Wuxing | parity) = 1.2500
   - Information from parity: 1.0000 bits
2. + b₀ within parity → H(Wuxing | parity, b₀) = 0.5000
   - Additional from b₀: 0.7500 bits
3. Residual (cosmological): 0.5000 bits

**Algebraic bits:** 1.7500
**Cosmological bits:** 0.5000

### 5c. The non-linear residual

Parity-0 coset: {000, 011, 100, 111} → complement pairs: [(0, 7), (3, 4)]
  Wuxing: {000=Earth, 011=Metal, 100=Earth, 111=Metal}
  Within this coset, b₀ cleanly separates Earth(b₀=0) from Metal(b₀=1).

Parity-1 coset: {001, 010, 101, 110} → complement pairs: [(1, 6), (2, 5)]
  Wuxing: {001=Wood, 010=Water, 101=Fire, 110=Wood}
  Complement pairs in coset: 2
  Traditional choice: keep pair (1, 6) together → Wood
  Alternative: keep pair (2, 5) together → would merge Water+Fire
  **This is 1 binary choice** — the sole cosmological input to Wuxing.

**Information accounting:**
- H(Wuxing) = 2.2500 bits
- Algebraic (linear features): 1.7500 bits
- Cosmological (1 binary choice): 0.5000 bits
- Sum: 2.2500 bits ✓

### 5d. Ranking among all (2,2,2,1,1) partitions

Total partitions with shape (2,2,2,1,1): **420**

Traditional Wuxing = partition #157

- **MI with Yang count:** 1.0613 (rank 217/420, top 51.7%)
- **MI with Basin(TT):** 1.0000 (rank 73/420, top 17.4%)
- **MI with Later Heaven:** 1.7500 (rank 5/420, top 1.2%)
- **Total MI (sum):** 3.8113 (rank 40/420, top 9.5%)

**Affine automorphism group order:**
- Traditional Wuxing: |Aut| = 8
- Range across all partitions: 6–48
- Mean: 9.6, Median: 6
- Wuxing rank by |Aut|: 29/420 (higher = more symmetric)

#### Top 10 partitions by total MI

| Rank | MI(Yang) | MI(Basin) | MI(LH) | Total | |Aut| | Is Wuxing? |
|------|----------|-----------|--------|-------|-------|------------|
| 1 | 1.5613 | 1.5000 | 1.2500 | 4.3113 | 8 |  |
| 2 | 1.5613 | 1.2500 | 1.5000 | 4.3113 | 48 |  |
| 3 | 1.3113 | 1.0000 | 2.0000 | 4.3113 | 6 |  |
| 4 | 1.5613 | 1.0000 | 1.7500 | 4.3113 | 8 |  |
| 5 | 1.5613 | 1.5000 | 1.2500 | 4.3113 | 8 |  |
| 6 | 1.5613 | 1.0000 | 1.7500 | 4.3113 | 8 |  |
| 7 | 1.3113 | 1.0000 | 2.0000 | 4.3113 | 6 |  |
| 8 | 1.3113 | 1.2500 | 1.7500 | 4.3113 | 6 |  |
| 9 | 1.5613 | 1.2500 | 1.5000 | 4.3113 | 6 |  |
| 10 | 1.5613 | 1.0000 | 1.5000 | 4.0613 | 6 |  |
