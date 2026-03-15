# Q1 Phase 3: Complement Depth Analysis — Results

## Question

The complement involution is characterized at three levels (algebraic, statistical, geometric). Two threads remain:
1. The 4 complement pairs that are NOT anti-correlated — are they algebraically special?
2. Can opposition strength be predicted from algebraic properties?
3. Is the antipodal map decomposable into shared axes, or truly 32-independent?

---

## Part A: The 4 Exceptions

Four complement pairs have non-negative residual cosine similarity:

| Pair | Similarity | Basin | Surface | Rank | Reverse? |
|------|-----------|-------|---------|------|----------|
| 升 ↔ 无妄 | +0.073 | Cycle+Cycle | 体克用+克体 | 4 | No |
| 革 ↔ 蒙 | +0.032 | Kun+Qian | 体克用+克体 | 4 | No |
| 師 ↔ 同人 | +0.011 | Kun+Qian | 体克用+克体 | 7 | No |
| 泰 ↔ 否 | +0.007 | Cycle+Cycle | 体生用+生体 | 3 | Yes |

**No shared algebraic property distinguishes the exceptions.**
- Basin: 2 same, 2 different
- Surface relation: none identical (3 share the same type of non-identity, 1 differs)
- Reverse pair: only 泰↔否
- Shared trigram: only 泰↔否
- Rank: 3, 4, 4, 7 — no concentration
- All have depth 2, but so do 24/32 pairs

The strongest structural predictor of anti-correlation is `shared_any_tri` (pairs sharing a trigram through upper↔lower matching are MORE anti-correlated, mean −0.384 vs −0.175, p = 0.082). But this goes the *wrong* direction — shared trigrams predict stronger opposition, not weaker. The 4 exceptions are not structurally special; they are the weak tail of a continuous distribution.

---

## Part B: Predicting Opposition Strength

### Univariate Correlations

| Feature | r | p |
|---------|---|---|
| Hamming weight (lighter) | −0.169 | 0.354 |
| KW number distance | +0.108 | 0.555 |
| Rank | +0.234 | 0.198 |
| Depth | +0.190 | 0.299 |
| Same basin | −0.170 | 0.352 |
| Is reverse pair | +0.007 | 0.969 |

No predictor reaches significance (all p > 0.19).

### Multivariate Regression

R² = 0.093 with 4 predictors (Hamming weight, KW distance, same basin, is reverse). Essentially zero explanatory power.

### By Basin Type

- Cycle+Cycle (n=16): mean = −0.229
- Kun+Qian (n=16): mean = −0.174
- Not significant (p = 0.207)

### By Hamming Weight

- hw=0 (乾↔坤): −0.273 (n=1)
- hw=1: −0.151 (n=6)
- hw=2: −0.181 (n=15)
- hw=3: −0.254 (n=10)
- No monotonic trend. Maximum bitflip (hw=0, hw=3) pairs are most anti-correlated, but this is not significant with n=32.

**Conclusion:** Opposition strength is algebraically opaque. No structural feature of a complement pair predicts how strongly the texts oppose thematically.

---

## Part C: Antipodal Map Characterization

### Cross-Pair Axis Generalization

For each of the 32 pair-difference axes, test whether it separates OTHER complement pairs (above chance = 0.500):

| Space | Mean separation | t-test | Interpretation |
|-------|----------------|--------|----------------|
| Residual | 0.444 | t=−6.89, p<0.0001 | Below chance (artifact of residual constraints) |
| Raw | 0.484 | t=−1.38, p=0.177 | At chance (axes are independent) |

In raw embedding space, each pair's opposition axis carries zero information about other pairs. The below-chance result in residual space is an artifact: regression constrains centroids to sum to ~0 within groups, creating spurious anti-alignment.

### Dimensionality

| Measure | Value |
|---------|-------|
| PCs for 50% | 8 |
| PCs for 80% | 15 |
| PCs for 90% | 19 |
| Participation ratio | 18.4 (of 31 possible) |
| Mean pairwise cosine | −0.032 |

The 32 difference vectors are nearly orthogonal and span ~18 effective dimensions. This confirms Phase 2: complement opposition is a high-dimensional antipodal map, not a low-dimensional reflection.

### What This Means

The complement involution acts on the thematic manifold as a **context-dependent antipodal map**: each hexagram opposes its complement along its own unique direction. There is no "complement axis" in the singular — there are 32 independent opposition directions. The map is:
- Not decomposable into shared components
- Not predictable from algebra
- Not reducible to a small number of semantic dimensions

---

## Part D: Multi-Level Synthesis

| Level | Source | Finding | Implication |
|-------|--------|---------|-------------|
| Algebraic forcing | T1, R85 | α = −1 is unique equivariant involution | Complement is the only possible structural choice |
| Cross-cultural | T2, R98 | Ifá independently discovered complement pairing | Complement is cognitively natural |
| Statistical | Q1, R112 | Mean cosine = −0.201 (p < 1e-6) | Texts composed with opposite themes |
| Geometric | Q1, R123 | ~18 effective dimensions, axes orthogonal | Each pair opposes in its own direction |
| Exceptions | Q1 Phase 3 | 4 pairs not anti-correlated, no shared property | Continuous distribution, no structural boundary |
| Prediction | Q1 Phase 3 | R² = 0.093 — algebra cannot predict strength | Opposition strength lives in the textual layer |
| Goldilocks | R108 | (3,5) is unique rigid point at complement boundary | Complement selects the only tractable cross-section |

The complement involution is simultaneously:
- **Algebraically FORCED** — the only equivariant option
- **Cognitively NATURAL** — independently discovered
- **Textually PERVASIVE** — 88% of pairs anti-correlated
- **Geometrically RICH** — 18-dimensional antipodal map
- **Algebraically OPAQUE** — opposition strength is unpredictable

This is the deepest bridge between algebra and text in the I Ching: the complement is the only algebraic operation that reaches into the thematic manifold, but once there, it acts with a richness that algebra cannot describe.

---

## New Results

| # | Result | Status |
|---|--------|--------|
| R130 | 4 non-anti-correlated complement pairs share no algebraic property | Measured |
| R131 | No algebraic feature predicts opposition strength (R² = 0.093) | Measured |
| R132 | Cross-pair axes do not generalize (raw separation = 0.484, p = 0.18) | Measured |
| R133 | Participation ratio of complement axes = 18.4 (of 31 possible) | Measured |
| R134 | shared_any_tri predicts STRONGER opposition (r = −0.384 vs −0.175, p = 0.082) | Measured |

---

## Computation

`Q1/phase3_complement_depth.py` — Full analysis script (Parts A–D)
