# Phase 4: 爻辭 Image Vocabulary Analysis — Results

## Phase 1: Image Vocabulary

- **Total distinct tokens:** 692
- **Total occurrences:** 1745
- **Lines with zero tokens:** 7 / 384
- **Per-line density:** mean=4.54, std=2.90
- **Zipf's law fit:** slope=-0.701, R²=0.9235

### Category Distribution

| Category | Distinct | Frequency | % of Total |
|----------|----------|-----------|------------|
| animals | 16 | 55 | 3.2% |
| landscape | 21 | 60 | 3.4% |
| body | 22 | 57 | 3.3% |
| social_roles | 28 | 157 | 9.0% |
| actions | 31 | 154 | 8.8% |
| objects | 18 | 63 | 3.6% |
| natural | 6 | 25 | 1.4% |
| qualities | 13 | 45 | 2.6% |
| states | 537 | 1129 | 64.7% |

## Phase 4: Complement Grounding

### 4a: Vocabulary Contrast

| Measure | Complement pairs | Random pairs |
|---------|-----------------|--------------|
| Mean Jaccard distance | 0.9664 | 0.9734 |
| Std | 0.0447 | 0.0267 |
| Mann-Whitney U | 31328 | p=0.8968 |

Complement pairs are **less distant** in vocabulary than random pairs.

### 4b: Category-level Opposition PCA

- PCs for 80% variance: **3**
- PCs for 90% variance: **5**
- Total categories: 9

| PC | Variance % | Cumulative % | Top loadings |
|----|-----------|-------------|-------------|
| PC1 | 56.9 | 56.9 | states(+0.897), actions(-0.333), landscape(-0.181) |
| PC2 | 12.8 | 69.7 | social_roles(+0.745), body(-0.556), objects(-0.195) |
| PC3 | 10.7 | 80.4 | actions(+0.802), objects(-0.404), landscape(-0.208) |
| PC4 | 7.2 | 87.6 | landscape(+0.458), qualities(-0.452), body(-0.413) |
| PC5 | 4.6 | 92.2 | qualities(+0.557), body(-0.475), objects(+0.445) |

### Dimensionality Comparison

- Token-level category opposition: 5 PCs for 90% variance (out of 9 categories)
- Embedding-level complement structure: 18 PCs (R133)
- The 9-category vocabulary decomposition is a coarse projection of the full 1024-dim embedding space

## Phase 2: Positional Distribution

| Category | L1 | L2 | L3 | L4 | L5 | L6 |
|----------|----|----|----|----|----|----|
| animals | 9 | 8 | 8 | 10 | 11 | 9 |
| landscape | 5 | 8 | 8 | 13 | 9 | 17 |
| body | 11 | 7 | 12 | 10 | 4 | 13 |
| social_roles | 14 | 32 | 32 | 17 | 33 | 29 |
| actions | 32 | 18 | 37 | 25 | 16 | 26 |
| objects | 13 | 11 | 11 | 12 | 6 | 10 |
| natural | 3 | 5 | 5 | 4 | 5 | 3 |
| qualities | 8 | 11 | 7 | 6 | 7 | 6 |
| states | 147 | 187 | 210 | 177 | 202 | 206 |

**Position-biased categories** (χ² goodness-of-fit, p < 0.05):

- **social_roles**: χ²=13.56, p=0.01866
- **actions**: χ²=12.52, p=0.02832
- **states**: χ²=14.92, p=0.01072

### 說卦傳 Trigram-Animal Alignment

No significant associations found (all p > 0.05). The 說卦傳 animal-trigram assignments are not reflected in the 爻辭 text distribution.

## Phase 3: Co-occurrence

- Tokens with freq ≥ 3: 209
- Results reported in stdout (115 significant pairs at p < 0.01)
