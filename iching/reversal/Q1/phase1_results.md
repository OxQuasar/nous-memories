# Q1 Phase 1: Residual Extraction and Intrinsic Structure — Results

## Method

384 yaoci (line text) embeddings (BGE-M3, 1024-dim) regressed against all known algebraic coordinates (line position, basin, surface relation, palace, palace element, rank, depth, i_component, inner_val, hu_depth, shi, ying). Residuals extracted and analyzed for intrinsic structure.

---

## 1. Variance Decomposition

### Hierarchical table

| Predictor set | R² | Notes |
|---|---|---|
| Position only (6 levels) | 1.7% | Line position 1-6 |
| Algebra only (categoricals + numeric) | 9.2% | Basin, surface relation, palace, etc. |
| Position + algebra (joint) | 11.0% | Overlap: 0.0% (nearly additive) |
| **RESIDUAL (89.0%)** | — | **The object of Q1** |

### Deeper decomposition of the residual

| Component | R² of raw embeddings | Notes |
|---|---|---|
| Hex identity (64 dummies) | 26.0% | Each hexagram's texts have a thematic signature |
| Position + algebra + hex (full) | 27.7% | Ceiling with all hex-level + position info |
| Ultimate residual | 72.3% | Within-hexagram, within-position variation |

### Key decomposition insight

| Layer | R² (cumulative) | What it captures |
|---|---|---|
| Algebra | 9.2% | Basin/palace/surface — 五行-derived coordinates |
| Hex identity beyond algebra | +16.8% = 26.0% | Per-hexagram thematic identity NOT predicted by algebra |
| Position | +1.7% = 27.7% | Line position adds little beyond hex identity |
| Within-hex residual | 72.3% | Per-line variation within each hexagram |

**The 89% residual (from algebra + position) decomposes into:**
- **16.8%**: Hex-specific thematic identity (algebra can't see it, but it's per-hexagram)
- **72.3%**: True within-hexagram, per-line variation (the irreducible residual)

---

## 2. Cluster Analysis

### Raw embeddings (baseline)

| Method | Result |
|---|---|
| Best k-means | k=4, silhouette=0.076 |
| DBSCAN | 0 clusters (384 noise) |
| K-means/Ward ARI | 0.206 (unstable) |
| PCA 90% | 51 components |

### Residual embeddings (the 89%)

| Method | Result |
|---|---|
| Best k-means | k=4, silhouette=0.070 |
| DBSCAN | 0 clusters (384 noise) |
| K-means/Ward ARI | 0.403 (moderate) |
| PCA 90% | 51 components |

### Silhouette sweep (k=2..10)

| k | Raw | Residual |
|---|---|---|
| 2 | 0.071 | 0.070 |
| 3 | 0.075 | 0.066 |
| 4 | 0.076 | 0.068 |
| 5 | 0.063 | 0.064 |
| 6 | 0.059 | 0.067 |

**All silhouette scores < 0.08.** DBSCAN fails at all eps values (1.0–4.0). The residual has NO discrete cluster structure. It is a smooth, diffuse distribution — not a collection of separated groups.

---

## 3. Intra-hexagram Coherence (the key positive finding)

After removing ALL algebraic coordinates, nearest-neighbor analysis on the residual:

| Coordinate | Observed rate | Expected (baseline) | Enrichment ratio |
|---|---|---|---|
| **Same hexagram** | **0.082** | **0.013** | **6.26×** |
| Same position | 0.152 | 0.164 | 0.92× |
| Same basin | 0.390 | 0.373 | 1.04× |
| Same palace | 0.158 | 0.123 | 1.29× |
| Same palace element | 0.263 | 0.217 | 1.21× |
| Same surface relation | 0.234 | 0.199 | 1.18× |

**Position is cleanly removed** (ratio 0.92 — correctly regressed out). **Hexagram identity is preserved at 6.26×** — the dominant residual structure.

Within-hex vs between-hex pairwise cosine similarity on residual:
- Within-hex: mean = 0.031 (960 pairs)
- Between-hex: mean = -0.003 (72,576 pairs)
- Mann-Whitney p < 1e-6, Cohen's d = 0.24

**The 89% residual retains per-hexagram thematic identity that no algebraic coordinate captures.**

---

## 4. Complement Anti-Correlation (surprise finding)

Mean cosine similarity between hexagram centroids in residual space:

| Pair type | Mean similarity | Count |
|---|---|---|
| **Complement pairs** | **−0.201** | 32 |
| Reverse pairs | −0.086 | 28 |
| All pairs | −0.016 | 2016 |

Mann-Whitney (complement < all): p < 1e-6.

**Complement hexagram texts are semantically OPPOSITE in the residual.** This signal is NOT captured by the algebraic regression (which includes basin, palace, etc. but not complement explicitly).

Most extreme complement pairs:
| Pair | Similarity |
|---|---|
| 恆 Heng ↔ 益 Yi | −0.615 |
| 咸 Xian ↔ 損 Sun | −0.497 |
| 既濟 Ji Ji ↔ 未濟 Wei Ji | −0.430 |
| 萃 Cui ↔ 大畜 Da Chu | −0.422 |

Least anti-correlated:
| Pair | Similarity |
|---|---|
| 升 Sheng ↔ 无妄 Wu Wang | +0.073 |
| 革 Ge ↔ 蒙 Meng | +0.032 |
| 師 Shi ↔ 同人 Tong Ren | +0.011 |

Adding raw 6-bit binary vectors to the regression reduces complement anti-correlation from −0.201 to −0.134. The anti-correlation is partially binary-structural, partially textual.

### Complement pair variance decomposition

Complement PAIR identity (32 groups of 12 yaoci) explains **7.5%** of the algebra-residual variance. Hex identity explains **18.8%** of the same residual. So complement pairs account for 7.5/18.8 = 40% of hex-level residual structure — the rest is per-hex identity beyond pair membership.

---

## 5. Algebraic Independence of Residual Clusters

χ² tests: does any algebraic coordinate predict residual k-means labels (k=4)?

| Coordinate | χ² | p-value | Cramér's V | Significant? |
|---|---|---|---|---|
| i_component | 0.54 | 0.461 | 0.038 | No |
| surface_relation | 3.01 | 0.557 | 0.089 | No |
| basin | 0.80 | 0.670 | 0.046 | No |
| palace_element | 2.27 | 0.687 | 0.077 | No |
| palace | 3.91 | 0.790 | 0.101 | No |
| depth | 0.24 | 0.888 | 0.025 | No |
| line_pos | 1.47 | 0.917 | 0.062 | No |
| rank | 2.13 | 0.952 | 0.075 | No |

**No algebraic coordinate predicts residual cluster membership.** The regression successfully removed all algebraic signal. (Compare: raw clusters show significant line_pos and i_component.)

---

## 6. Summary and Interpretation

### The residual is diffuse but NOT unstructured

The 89% residual has:
- **No cluster structure** — silhouette < 0.08, DBSCAN fails, embedding space is a smooth cloud
- **Strong intra-hexagram coherence** — 6.26× nearest-neighbor enrichment, p < 1e-6
- **Complement anti-correlation** — complement hexagram texts are semantically opposite (−0.20)
- **No algebraic leakage** — no coordinate predicts residual cluster membership

### The architecture of meaning

```
Embedding variance (100%)
├── Algebraic coordinates (9.2%) — basin, palace, surface relation, etc.
├── Hex identity beyond algebra (16.8%) — per-hexagram thematic signature
├── Position (1.7%) — line position effect
└── Within-hex residual (72.3%) — per-line variation, the true irreducible
```

### What the 89% IS

The residual is not noise, not clusters, not algebra. It is a **smooth thematic manifold** where each hexagram occupies a distinct region, and complement hexagrams are at opposite poles. The organizing principle is hexagram identity — but not the identity captured by algebraic coordinates. Each hexagram has a thematic essence (imagery, situation, narrative arc) that the algebra cannot predict but the texts consistently express.

The prior work's finding that "89% is text-intrinsic" is refined: ~17% is text-intrinsic but hex-coherent (each hexagram has its own thematic world), and ~72% is within-hexagram variation (line-to-line narrative diversity).

### Connection to Q3

The complement anti-correlation suggests the texts were composed with awareness of complement structure — complement hexagrams tell "opposite stories." This bridges Q1 (what's in the residual) to Q3 (how practitioners navigate the textual layer): the complement axis provides a coordinate for navigating the thematic manifold.

---

## Computation

- Script: `Q1/phase1_residual_structure.py`
- Data: `synthesis/embeddings.npz` (yaoci), `atlas/atlas.json`
- All results reproducible with fixed random seed (42)
