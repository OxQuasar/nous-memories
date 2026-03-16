# Phase 8: Dimensionality Reduction of Opposition Directions

Tests whether trigram structure decomposes the directions of thematic opposition between complement pairs.

## 8a: Trigram Additive Model (Cross-Model)

| Model | Full R² | Lower R² | Upper R² | p-value | Within cos | Across cos | Interact p |
|-------|---------|----------|----------|---------|------------|------------|------------|
| bge-m3 | 0.1751 | 0.0663 | 0.0743 | 0.9997 | -0.2006 | -0.0262 | 0.9999 |
| e5-large | 0.1685 | 0.0631 | 0.0704 | 1.0000 | -0.1870 | -0.0268 | 1.0000 |
| labse | 0.1961 | 0.0853 | 0.0762 | 0.9240 | -0.1844 | -0.0268 | 0.9996 |

### Per-trigram-pair vector norms (BGE-M3)

| Pair | α (lower) | β (upper) |
|------|-----------|-----------|
| KunQian | 0.1013 | 0.0996 |
| ZhenXun | 0.0955 | 0.1154 |
| KanLi | 0.1195 | 0.1353 |
| DuiGen | 0.1212 | 0.1122 |

## 8b: Cross-Model Consensus

Best k: 20
Consensus participation ratio: 16.09

### Direction concordance (Spearman ρ)

- bge-m3 ↔ e5-large: ρ=+0.8842 (p=0.000000)
- bge-m3 ↔ labse: ρ=+0.7792 (p=0.000000)
- e5-large ↔ labse: ρ=+0.7626 (p=0.000000)

### Procrustes R²

| k | bge-m3↔e5-large | bge-m3↔labse | e5-large↔labse |
|---|---:|---:|---:|
| 5 | 0.6277 | 0.5683 | 0.4136 |
| 8 | 0.8610 | 0.6877 | 0.6671 |
| 10 | 0.7505 | 0.6338 | 0.6548 |
| 15 | 0.8799 | 0.7762 | 0.7274 |
| 20 | 0.9488 | 0.8725 | 0.8494 |

## 8c: Trigram Decomposition on Consensus

Full R²: 0.1836 (p=0.9913)
Lower R²: 0.0722
Upper R²: 0.0773
Interaction: within=-0.1842, across=-0.0263, p=0.9994

## 8d: Algebraic Groupings

| Representation | Grouping | Within cos | Between cos | Gap | p |
|----------------|----------|------------|-------------|-----|---|
| bge-m3 | basin | -0.0329 | -0.0309 | -0.0021 | 0.5459  |
| bge-m3 | fano_lower | -0.0667 | -0.0217 | -0.0449 | 0.9989  |
| bge-m3 | fano_upper | -0.0580 | -0.0243 | -0.0337 | 0.9873  |
| bge-m3 | wuxing_lower | -0.0679 | -0.0232 | -0.0446 | 0.9983  |
| bge-m3 | wuxing_upper | -0.0580 | -0.0243 | -0.0337 | 0.9886  |
| consensus | basin | -0.0349 | -0.0281 | -0.0069 | 0.6566  |
| consensus | fano_lower | -0.0586 | -0.0234 | -0.0352 | 0.9712  |
| consensus | fano_upper | -0.0528 | -0.0251 | -0.0277 | 0.9357  |
| consensus | wuxing_lower | -0.0631 | -0.0238 | -0.0394 | 0.9840  |
| consensus | wuxing_upper | -0.0528 | -0.0251 | -0.0277 | 0.9343  |

## Key Findings

### Trigram structure does NOT organize opposition direction

The additive trigram model (8 one-hot indicators, rank 7) explains R²≈0.18 of
opposition direction variance — but this is BELOW the null expectation of R²≈0.225.
With 7 effective predictors and 32 observations, random labels explain ~7/31≈22.6%
by chance. All p-values are ≥0.92. The trigram decomposition is definitively negative
across all 3 models and on consensus.

### No algebraic grouping organizes opposition direction

All grouping tests (五行, Fano line, basin) show NEGATIVE gaps in residual space:
within-group pairs are MORE dissimilar than between-group pairs.

**8e verification:** This anti-clustering is an artifact of residual-space projection.
On RAW (pre-regression) centroids, all gaps are near zero or slightly positive:

| Grouping | RAW gap | RAW p | RES gap | RES p |
|----------|---------|-------|---------|-------|
| Lower trigram pair | +0.020 | 0.046 | −0.045 | 0.999 |
| Upper trigram pair | +0.000 | 0.468 | −0.034 | 0.987 |
| 五行 lower | −0.001 | 0.489 | −0.045 | 0.998 |
| 五行 upper | +0.000 | 0.464 | −0.034 | 0.988 |
| Basin | +0.005 | 0.256 | −0.002 | 0.545 |

The algebraic regression removes trigram-correlated components, forcing residual
difference vectors into the orthogonal complement — which mechanically produces
negative gaps for any grouping correlated with the regressed features.

The lower trigram pair type on raw centroids shows a borderline signal (p=0.046,
gap=+0.020), but the effect is tiny (within cos=+0.012, between cos=−0.009)
and would not survive multiple-comparison correction.

### But opposition directions are highly text-intrinsic

Cross-model direction concordance is strong (ρ=0.78–0.88, p≈0). Procrustes alignment
at k=20 yields R²=0.85–0.95 between model pairs. The opposition directions are real
properties of the text, not model artifacts — they're just not organized by trigram algebra.

### Consensus concentrates slightly

Consensus participation ratio (16.1) is slightly below per-model values (~18.4),
suggesting ~2 dimensions of the opposition space are model-specific noise.

### Interaction structure absent

Within-cell residual cosines are more negative than across-cell (gap≈−0.17, p≈1.0),
confirming no interaction between upper and lower trigram pair types. The additive model
is sufficient (and insufficient — both additive and interaction effects are absent).
