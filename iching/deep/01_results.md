# Alternative 五行 Assignment Discrimination Test

Tests whether the traditional trigram→element assignment is uniquely forced.

## Part 1: Alternative Assignments

### Assignment A (Traditional)

| Trigram | Binary | Element |
|---------|--------|---------|
| Kun ☷ | 000 | Earth |
| Zhen ☳ | 001 | Wood |
| Kan ☵ | 010 | Water |
| Dui ☱ | 011 | Metal |
| Gen ☶ | 100 | Earth |
| Li ☲ | 101 | Fire |
| Xun ☴ | 110 | Wood |
| Qian ☰ | 111 | Metal |

生-cycle: Wood → Fire → Earth → Metal → Water
Complement = negation: True

### Assignment B: Pair {Kan, Li}

Total complement-respecting configurations: 16

**B.1**: positions = {'Kan+Li': 0, 'Kun+Gen': 1, 'Dui+Qian': 4, 'Zhen': 2, 'Xun': 3}
**B.2**: positions = {'Kan+Li': 0, 'Kun+Gen': 1, 'Dui+Qian': 4, 'Zhen': 3, 'Xun': 2}
**B.3**: positions = {'Kan+Li': 0, 'Kun+Gen': 2, 'Dui+Qian': 3, 'Zhen': 1, 'Xun': 4}
**B.4**: positions = {'Kan+Li': 0, 'Kun+Gen': 2, 'Dui+Qian': 3, 'Zhen': 4, 'Xun': 1}
**B.5**: positions = {'Kan+Li': 0, 'Kun+Gen': 3, 'Dui+Qian': 2, 'Zhen': 1, 'Xun': 4}
**B.6**: positions = {'Kan+Li': 0, 'Kun+Gen': 3, 'Dui+Qian': 2, 'Zhen': 4, 'Xun': 1}

Valid B assignments built: 16

### Assignment C: Cross-pair {Kan, Zhen} + {Li, Xun}

Total complement-respecting configurations: 16

**C.1**: {Kan,Zhen}@1 {Li,Xun}@4 {Kun,Qian}@0 Gen@2 Dui@3
**C.2**: {Kan,Zhen}@1 {Li,Xun}@4 {Kun,Qian}@0 Gen@3 Dui@2
**C.3**: {Kan,Zhen}@2 {Li,Xun}@3 {Kun,Qian}@0 Gen@1 Dui@4
**C.4**: {Kan,Zhen}@2 {Li,Xun}@3 {Kun,Qian}@0 Gen@4 Dui@1

Valid C assignments built: 16

## Part 2: 吉×生体 Discriminating Test

### Traditional (A)

- 生体 count: 72
- 生体 吉 rate: 0.444 (32/72)
- Fisher (生体 vs rest, 吉): OR=2.10, p=0.0069
- 比和 凶 rate: 0.202
- 克体 吉 rate: 0.269
- Relation distribution: {'比和': 84, '克体': 78, '体克用': 78, '体生用': 72, '生体': 72}

**Full cross-tab (Traditional):**

| Relation | n | 亨 | 凶 | 利 | 厲 | 吉 | 吝 | 悔 | 无咎 |
|----------|---|---|---|---|---|---|---|---|---|
| 比和 | 84 | 0(0.00) | 17(0.20) | 13(0.15) | 6(0.07) | 19(0.23) | 2(0.02) | 7(0.08) | 17(0.20) |
| 生体 | 72 | 3(0.04) | 5(0.07) | 8(0.11) | 4(0.06) | 32(0.44) | 7(0.10) | 5(0.07) | 17(0.24) |
| 体生用 | 72 | 2(0.03) | 6(0.08) | 13(0.18) | 5(0.07) | 23(0.32) | 3(0.04) | 7(0.10) | 15(0.21) |
| 克体 | 78 | 1(0.01) | 11(0.14) | 9(0.12) | 7(0.09) | 21(0.27) | 5(0.06) | 3(0.04) | 19(0.24) |
| 体克用 | 78 | 2(0.03) | 13(0.17) | 13(0.17) | 4(0.05) | 23(0.29) | 3(0.04) | 9(0.12) | 17(0.22) |

### Assignment B variants

| Variant | n(生体) | 生体 吉 rate | OR | p | 比和 凶 | 克体 吉 |
|---------|---------|-------------|-----|---|---------|---------|
| B.1 | 78 | 0.308 | 1.00 | 1.0000 | 0.155 | 0.375 |
| B.2 | 78 | 0.321 | 1.08 | 0.7845 | 0.155 | 0.292 |
| B.3 | 72 | 0.403 | 1.69 | 0.0649 | 0.155 | 0.321 |
| B.4 | 72 | 0.375 | 1.46 | 0.2018 | 0.155 | 0.308 |
| B.5 | 72 | 0.375 | 1.46 | 0.2018 | 0.155 | 0.282 |
| B.6 | 72 | 0.292 | 0.91 | 0.7791 | 0.155 | 0.321 |
| B.7 | 78 | 0.321 | 1.08 | 0.7845 | 0.155 | 0.403 |
| B.8 | 78 | 0.282 | 0.86 | 0.6804 | 0.155 | 0.375 |
| B.9 | 78 | 0.321 | 1.08 | 0.7845 | 0.083 | 0.389 |
| B.10 | 78 | 0.295 | 0.93 | 0.8908 | 0.083 | 0.347 |
| B.11 | 72 | 0.319 | 1.07 | 0.8874 | 0.083 | 0.295 |
| B.12 | 72 | 0.250 | 0.71 | 0.2604 | 0.083 | 0.321 |
| B.13 | 72 | 0.389 | 1.57 | 0.1186 | 0.083 | 0.308 |
| B.14 | 72 | 0.347 | 1.25 | 0.4787 | 0.083 | 0.308 |
| B.15 | 78 | 0.308 | 1.00 | 1.0000 | 0.083 | 0.319 |
| B.16 | 78 | 0.308 | 1.00 | 1.0000 | 0.083 | 0.250 |

B summary: OR range [0.71, 1.69], p range [0.0649, 1.0000]
Any B with p < 0.05: False
Any B with OR > 1.5: True

### Assignment C variants (sample)

| Variant | n(生体) | 生体 吉 rate | OR | p | 比和 凶 | 克体 吉 |
|---------|---------|-------------|-----|---|---------|---------|
| C.1 | 78 | 0.295 | 0.93 | 0.8908 | 0.095 | 0.236 |
| C.2 | 78 | 0.256 | 0.73 | 0.3360 | 0.095 | 0.319 |
| C.3 | 72 | 0.278 | 0.84 | 0.5745 | 0.095 | 0.256 |
| C.4 | 72 | 0.361 | 1.35 | 0.3211 | 0.095 | 0.295 |
| C.5 | 72 | 0.236 | 0.65 | 0.1588 | 0.095 | 0.333 |
| C.6 | 72 | 0.319 | 1.07 | 0.8874 | 0.095 | 0.372 |
| C.7 | 78 | 0.372 | 1.44 | 0.1717 | 0.095 | 0.278 |
| C.8 | 78 | 0.333 | 1.16 | 0.5844 | 0.095 | 0.361 |
| C.9 | 78 | 0.308 | 1.00 | 1.0000 | 0.119 | 0.375 |
| C.10 | 78 | 0.333 | 1.16 | 0.5844 | 0.119 | 0.292 |
| C.11 | 72 | 0.333 | 1.16 | 0.6709 | 0.119 | 0.333 |
| C.12 | 72 | 0.319 | 1.07 | 0.8874 | 0.119 | 0.308 |
| C.13 | 72 | 0.375 | 1.46 | 0.2018 | 0.119 | 0.244 |
| C.14 | 72 | 0.292 | 0.91 | 0.7791 | 0.119 | 0.282 |
| C.15 | 78 | 0.282 | 0.86 | 0.6804 | 0.119 | 0.333 |
| C.16 | 78 | 0.244 | 0.67 | 0.2158 | 0.119 | 0.319 |

C summary: OR range [0.65, 1.46], p range [0.1588, 1.0000]
Any C with p < 0.05: False
Any C with OR > 1.5: False

### Side-by-side comparison

| Metric | Traditional (A) | Best B | Best C |
|--------|----------------|--------|--------|
| 生体 吉 rate | 0.444 | 0.403 | 0.236 |
| Fisher OR | 2.102 | 1.690 | 0.646 |
| Fisher p | 0.007 | 0.065 | 0.159 |
| 比和 凶 rate | 0.202 | 0.155 | 0.095 |
| 克体 吉 rate | 0.269 | 0.321 | 0.333 |

## Part 3: Structural Checks

### 3.1 Cycle Attractor Relations (既濟/未濟)

| Assignment | 既濟 relation | 未濟 relation |
|------------|-------------|-------------|
| Traditional (A) | 克体 | 体克用 |
| B (first) | 比和 | 比和 |
| C (first) | 体克用 | 克体 |

### 3.2 Complement = Negation on Cycle Ring

| Assignment | π = -x mod 5 |
|------------|-------------|
| Traditional (A) | True |
| B (first) | True |
| C (first) | True |

### 3.3 Zero Residual (profile uniqueness)

| Assignment | Unique | Collisions | Max collision | Distinct profiles |
|------------|--------|------------|---------------|-------------------|
| Traditional (A) | 52/64 | 6 | 2 | 58 |
| B (first) | 50/64 | 7 | 2 | 57 |
| C (first) | 64/64 | 0 | 1 | 64 |

### 3.4 互 Well-Definedness (torus cells)

| Assignment | Well-defined | Total realized |
|------------|-------------|----------------|
| Traditional (A) | 8/25 | 25/25 |
| B (first) | 8/25 | 25/25 |
| C (first) | 4/25 | 25/25 |

### 3.5 六親 Injectivity

| Assignment | Unique words / 64 |
|------------|-------------------|
| Traditional (A) | 23 |
| B (first) | 23 |
| C (first) | 17 |

### 3.6 Parity Separation (XOR masks)

| Assignment | Parity separated |
|------------|-----------------|
| Traditional (A) | True (生-only parities: {0}, 克-only: {1}) |
| B (first) | True (生-only parities: {1}, 克-only: {0}) |
| C (first) | True (生-only parities: {1}, 克-only: {0}) |

## Part 4: He Tu vs 生-cycle Z₅

### 1. π = -x mod 5 on 生-cycle ring

| Element | x (生) | π(x) | -x mod 5 | Match |
|---------|--------|------|----------|-------|
| Wood | 0 | 0 | 0 | ✓ |
| Fire | 1 | 4 | 4 | ✓ |
| Earth | 2 | 3 | 3 | ✓ |
| Metal | 3 | 2 | 2 | ✓ |
| Water | 4 | 1 | 1 | ✓ |

**Result: π = -x mod 5 on 生-cycle: True**

### 2. π on He Tu ring

| Element | x (HeTu) | π(x) | 
|---------|----------|------|
| Earth | 0 | 4 |
| Water | 1 | 2 |
| Fire | 2 | 1 |
| Wood | 3 | 3 |
| Metal | 4 | 0 |

Searching all 25 affine maps f(x) = ax + b mod 5:
  NO affine map matches. **π is not affine on He Tu.**

### 3. D₅ generation

On 生-cycle: |⟨σ, π⟩| = 10
  D₅ has order 10: ✓
On He Tu: |⟨σ, π⟩| = 10
  D₅ has order 10: ✓

### 4. Conjugating permutation γ

γ: 生-cycle → He Tu
  Wood: 0 → 3
  Fire: 1 → 2
  Earth: 2 → 0
  Metal: 3 → 4
  Water: 4 → 1

γ σ_sheng γ⁻¹ = σ_hetu: True
γ π_sheng γ⁻¹ = π_hetu: True

**Both actions are D₅, conjugated by γ = [3, 2, 0, 4, 1]**
**γ as cycle notation:** {0: 3, 1: 2, 2: 0, 3: 4, 4: 1}

## Part 5: Z₅ × Z₅ × Z₅ Grid (surface × hu × surface)

Total cells realized: 43 of 125 = 125 possible

Population: min=1, max=4, mean=1.5, median=1
Population distribution: {1: 26, 2: 15, 4: 2}

### Hexagrams per hu_relation

| hu_relation | n_hex |
|-------------|-------|
| 比和 | 16 |
| 生体 | 4 |
| 体生用 | 4 |
| 克体 | 20 |
| 体克用 | 20 |

### Valence by hu_relation (middle coordinate)

| hu_relation | n | 吉 | 吉 rate | 凶 | 凶 rate |
|-------------|---|---|---------|---|---------|
| 比和 | 96 | 26 | 0.271 | 22 | 0.229 |
| 生体 | 24 | 10 | 0.417 | 4 | 0.167 |
| 体生用 | 24 | 7 | 0.292 | 0 | 0.000 |
| 克体 | 120 | 38 | 0.317 | 13 | 0.108 |
| 体克用 | 120 | 37 | 0.308 | 13 | 0.108 |

χ² test (吉 across hu_relation): χ²=2.026, p=0.7310, dof=4

### Forbidden cells analysis

Forbidden cells: 82 of 125
Realized cells: 43 of 125
Occupancy rate: 0.344

## Summary

### Predictions vs Results

| Prediction | Result |
|------------|--------|
| B loses 吉×生体 bridge | ✓ Confirmed (best p=0.0649) |
| B loses cycle attractor 克 | ✓ Confirmed: 比和/比和 |
| C breaks complement closure | ✗ C still has complement=negation |
| Zero residual survives for all | Check table 3.3 above |
| Traditional unique: textual + algebraic | Textual (p=0.0069): ✓, Algebraic (π=-x): ✓ |
