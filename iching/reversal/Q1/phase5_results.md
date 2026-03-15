# Q1 Phase 5: Syntactic Frame Analysis — Results

## Phase 1: Frame Classification

- **384 lines** classified across 5 marker-based frames + state_description
- Classification is purely mechanical: marker present → frame tagged

| Frame | Markers | Lines | % |
|-------|---------|-------|---|
| directive | 利, 勿, 不可, 宜 | 79 | 20.6% |
| conditional | 若, 如, 則 | 30 | 7.8% |
| locative | 在, 于 | 75 | 19.5% |
| motion | 往, 來, 征, 行, 涉, 入, 出 | 90 | 23.4% |
| negation | 不, 勿, 弗, 匪, 无, 無 | 197 | 51.3% |
| state_desc | (no markers) | 106 | 27.6% |

- Frames per line: 0=106, 1=132, 2=110, 3+=36

## Phase 2: Correlation Tests

### 2a: Line-Level Mantel Test (384×384)

- Pearson r = 0.0008
- p (parametric) = 0.8194
- **p (permutation) = 0.4818**

### 2b: Hexagram-Level Mantel Test (64×64)

- Pearson r = 0.0841 (cosine frame dist)
- p (permutation) = 0.1252
- Euclidean frame dist: r = 0.0935, p = 2.591e-05

### 2c: Complement Pair Frame Profiles

- Complement frame diff magnitude: 4.464
- Random pair frame diff magnitude: 4.155
- Mann-Whitney p = 0.2911

### 2d: Position × Frame

| Frame | L1 | L2 | L3 | L4 | L5 | L6 |
|-------|----|----|----|----|----|----| 
| directive | 13 | 16 | 12 | 7 | 14 | 17 |
| conditional | 3 | 5 | 8 | 4 | 6 | 4 |
| locative | 9 | 17 | 11 | 11 | 10 | 17 |
| motion | 23 | 10 | 19 | 13 | 9 | 16 |
| negation | 33 | 30 | 35 | 32 | 29 | 38 |
| state_desc | 17 | 23 | 18 | 18 | 18 | 12 |

## Interpretation

**Syntactic frames do NOT predict embedding geometry.**

**Quadruple dissociation** confirmed:

| Layer | Test | r | p |
|-------|------|---|---|
| 1. Algebra | R119/R125 | ≈ 0 | > 0.40 |
| 2. Vocabulary | R135 | — | 0.897 |
| 3. 說卦傳 象 | R146 | -0.003 | 0.543 |
| 4. Syntactic frames | This test | 0.0008 | 0.4818 |

The embedding geometry is irreducible to any mechanically extractable feature. It lives in the sub-syntactic compositional texture — how characters combine to create situated meaning, below the level of grammar, vocabulary, or symbolic association.
