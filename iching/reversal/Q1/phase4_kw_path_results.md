# Phase 4: King Wen Path Through the Thematic Manifold

Null model: 10000 permutations of 30 interior pairs (pair 0=乾坤, pair 31=既濟未濟 fixed), anti-clustering enforced.

## Test 1: Bridge Smoothness

31 between-pair bridge distances in residual space (cosine).

| Metric | KW | Null μ±σ | %ile | z |
|--------|---:|--------:|-----:|--:|
| mean | 0.97388 | 1.01051±0.02305 | 5.6% | -1.59 |
| median | 0.98243 | 1.00452±0.02637 | 21.6% | -0.84 |
| max | 1.24482 | 1.28560±0.05833 | 27.8% | -0.70 |
| std | 0.11351 | 0.12516±0.01507 | 22.2% | -0.77 |
| lag1_autocorr | -0.32226 | -0.03406±0.17764 | 5.4% | -1.62 |

## Test 2: Path Shape

PCA on 32 pair centroids. Variance explained: 0.117, 0.096, 0.081, 0.069, 0.066

- **Total R² drift**: KW=0.11281, null=0.13904±0.07726, pct=42.6%
- **Max spectral amp**: KW=0.67785, null=0.69526±0.08299, pct=46.9%
- Dominant frequencies: [np.int64(2), np.int64(3), np.int64(15), np.int64(12), np.int64(9)]

## Test 3: Complement Placement

24 reversal pairs with complement mapping.

- Thematic × sequence distance: Pearson r=-0.0704 (p=0.7439), Spearman ρ=-0.0247 (p=0.9088)
- Pearson percentile vs null: 42.8%
- Spearman percentile vs null: 47.2%
- KW mean complement sequence distance: 7.92 (null: 10.32)

## Test 4: 上經/下經 Split

- Within-上經: 1.02277
- Within-下經: 1.02396
- Cross-split: 1.04002
- Split quality: 0.01665, pct=85.8%, z=+1.07
- Cross-split complements: 6/12, pct=56.6%, z=-0.11
