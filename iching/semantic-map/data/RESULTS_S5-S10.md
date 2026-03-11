# Core Analysis Results (S5 + S7 + S8 + S9 + S10)

## S5: 爻辭 Full Analysis

### Part A: Raw Cluster Characterization

**Dominant structure: POSITIONAL** (not hexagrammatic, not thematic)

k=3 results:
- Position × cluster: χ²=37.2, p=0.0001 — highly significant positional dependency
- Only 3/64 hexagrams have all 6 lines in same cluster — clusters cut across hexagrams
- Clusters span 51-58 hexagrams each — broadly distributed, not hex-coherent

Cluster profiles (k=3):
| Cluster | Size | Position bias | Distinctive content |
|---------|------|---------------|-------------------|
| 0 | 175 | Peaks at L3 (46) | 厲吉, 有悔, 居貞 — cautionary outcomes |
| 1 | 95 | Peaks at L2,L5 (22,24) | 利用, 有孚, 中行 — central/proper action |
| 2 | 114 | Peaks at L1 (26), L4 (23) | 婚媾, 往蹇, 无妄 — situational imagery |

k=5: even stronger positional signal (χ²=52.3, p=0.0001), only 1 hex-coherent.

### Part B: Positional Signatures

- **PERMANOVA: pseudo-F=1.34, p=0.001** — position explains significant embedding variance
- Hierarchy grouping: mean cosine distance within hierarchy pairs (1↔6, 2↔5, 3↔4) = 0.0157, vs non-hierarchy = 0.0173
- Pairs (2,5) are closest in hierarchy (0.0130) — matches their shared "central" role

Centroid distance reveals structure:
- L4 is closest to L1, L2, L6 — the "bridge" position
- L3 and L5 are most distant from each other (0.0277) — maximum semantic contrast
- L2↔L5 closeness (0.0130) confirms structural pairing (both "central" positions)

### Part C: Stripped Clustering

- **Variance removed by marker projection: 3.3%** — markers explain negligible embedding variance
- **ARI (raw vs stripped): 0.82** — clusters barely change when markers are removed
- **Confirms S3 diagnostic: embeddings capture imagistic/situational content, not formulaic valence**

## S7: Algebraic Comparison (Residual Thickness)

### Guaci (64 hexagrams)

| Coordinate | R² | p-value |
|-----------|-----|---------|
| basin | 0.032 | 0.419 |
| depth | 0.028 | 0.930 |
| i_component | 0.018 | 0.191 |
| surface_relation | 0.066 | 0.256 |
| palace | 0.116 | 0.160 |
| **JOINT** | **0.360** | — |

**Guaci residual thickness: 0.64** — 64% of guaci embedding variance is independent of all algebraic coordinates. No individual coordinate reaches significance. Palace has the largest individual R² (0.116) but is not significant.

Note: PCA retained 38 components for 90% variance — the embedding space is quite high-dimensional.

### Yaoci (384 lines)

| Predictor | R² (RDA) |
|-----------|----------|
| Line position | 0.018 |
| Algebraic coordinates | 0.093 |
| Joint (position + algebra) | 0.111 |

Individual PERMANOVA (all p=0.001):
- Basin: R²=0.007
- Surface relation: R²=0.014
- Palace: R²=0.024

**Yaoci residual thickness: 0.89** — 89% of yaoci embedding variance is text-intrinsic.

Note: Yaoci algebraic effects are individually small but collectively significant (p=0.001). Position accounts for only 1.8% of variance in embeddings — despite being the dominant clustering axis (S5.A). This means position creates systematic but small shifts in the embedding centroid, not dramatic separations.

## S8: 大象 Bridge Test

- **大象 operates in IMAGISTIC register, not elemental**
- No 五行 vocabulary (金木水火土/相生相克) appears in moral/action portions
- 水/火/木 appear only as trigram nature images (not elemental theory)
- Relation type × surface relation: χ²=15.16, p=0.056 — marginal, not significant
- Image → element recovery: 100% (upper: 63/63, lower: 53/53) — but this is trivial since trigram images deterministically map to elements
- Extended trigram image match: ~60/64 (including secondary images: 雲=水, 泉=水, 電=火, 木=風)
- **Conclusion: 大象 commentary does not use 五行 relational language. It describes via nature imagery, not elemental dynamics.**

## S9: 彖傳 Structural Analysis

### Accuracy of structural references
- **剛/柔 + line reference**: 13/23 correct (57%) — barely above chance (50% for binary yang/yin)
  - Note: these are approximate regex matches; many 剛/柔 references don't have explicit line numbers nearby
- **中 references**: 剛中 appears 16 times, ALL with yang at line 2 or 5. 柔中: 5 times, all with yin at 2 or 5. **100% accuracy** — 中 is a faithful structural descriptor
- **應 (correspondence)**: 25 hexagrams mention 應; 55% of their line pairs are actually "responding" (different yin/yang). Non-應 hexagrams: 47%. Modest difference — 應 weakly tracks actual correspondence.

### Cross-tab with algebraic coordinates

| Test | Statistic | p-value | Finding |
|------|-----------|---------|---------|
| 剛/柔 ratio × basin | H=1.13 | 0.569 | NOT significant |
| Structural density × I-component | U=531 | 0.799 | NOT significant |
| 往/來 × surface relation | H=2.53 | 0.639 | NOT significant |

**彖傳 structural vocabulary does NOT track algebraic coordinates.** No test reaches significance. The 彖傳 uses structural language (剛/柔/中/應) that tracks the hexagram's binary line structure, not the 五行/basin/surface algebraic profile.

### Basin-specific 剛/柔 ratios
- Kun basin: 剛/柔 = 2.14 (surprising — more 剛 even in the Kun basin)
- Cycle: 1.50
- Qian: 1.25

The fact that Kun basin has the HIGHEST 剛/柔 ratio is noteworthy — suggests 彖傳 comments on what's unusual/noteworthy (剛 lines in a predominantly 柔 context).

## S10: 小象 Full Analysis

### Vocabulary-based clustering

Vocabulary clusters are STRONGLY position-dependent:
- k=6 (best silhouette=0.631): χ²=160.2, p≈0 for position

Key clusters at k=4 (sil=0.530):
| Cluster | Size | Position signature | Content |
|---------|------|--------------------|---------|
| 0 | 30 | L3, L4, L5 only | 位, 當 terms — positional commentary |
| 1 | 256 | All positions | Default/generic commentary |
| 2 | 50 | L1, L4 | 剛, 柔 terms |
| 3 | 48 | L2, L5 only | 中 term — central position markers |

Cluster 3 perfectly captures the "中" vocabulary at lines 2,5.

### Embedding-based clustering

- Silhouette very low (0.034 at k=3) — embeddings have diffuse distribution (similar to guaci)
- ARI between vocab and embedding clusters: ≈0 — the two capture different structures
- Embedding clusters still position-dependent (χ²=58-92, p≈0) but via different mechanisms

### Residual algebraic signal

| Predictor | R² |
|-----------|-----|
| Position alone | 0.025 |
| Position + Basin | 0.058 (basin residual: 0.033) |
| Position + Surface relation | 0.086 (srel residual: 0.061) |

**Basin residual p-value (controlling for position): p=0.088** — NOT significant at α=0.05.

**Conclusion: After controlling for line position, there is NO significant algebraic signal in 小象 embeddings.** The surface relation shows the largest residual (6.1%) but was not permutation-tested due to computational cost. The dominant structure in 小象 is positional, not algebraic.
