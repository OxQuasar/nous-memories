# Q1 Phase 2: Geometry of the Thematic Manifold — Results

## Method

64 hex centroids computed from residual embeddings (Phase 1: algebra + position regressed out). Analyzed via PCA, complement pair-difference vectors, structural similarity tests, and intra-hexagram trajectory analysis. Where noted, tests re-run on raw embeddings to avoid regression artifacts.

---

## Part A: Principal Axes of Hex-Thematic Space

PCA on 64 hex centroids in residual space:

| PC | Variance % | Cumulative % |
|---|---|---|
| PC1 | 7.3% | 7.3% |
| PC2 | 6.6% | 13.9% |
| PC3 | 5.2% | 19.1% |
| PC4 | 5.2% | 24.3% |
| PC5 | 4.6% | 28.8% |
| PC6–10 | 3.5–4.3% each | 48.1% |

**Components for 80%: 21. Components for 90%: 21.**

The hex-thematic space is HIGH-DIMENSIONAL — no dominant axis. PC1 explains only 7.3%, and variance drops gradually (no elbow). This is not a space with a few meaningful directions; it's a roughly isotropic cloud with ~20 effective dimensions.

### Correlation with known coordinates

Only one PC shows any correlation with any atlas coordinate above |r| = 0.25:

| PC | Coordinate | r | p |
|---|---|---|---|
| PC3 | bit_5 | −0.253 | 0.044 |

**The thematic manifold is genuinely novel.** Its principal axes do not align with basin, palace, surface relation, King Wen number, trigram values, Hamming weight, depth, rank, or any other known coordinate. The 16.8% of variance carried by hex identity (Phase 1, R118) lives in a space orthogonal to the algebra.

---

## Part B: Complement Axis Analysis

### Structure of complement opposition

32 complement pair-difference vectors (centroid_A − centroid_B):

| Metric | Value |
|---|---|
| Mean pairwise cosine of diff vectors | −0.032 |
| Std | 0.142 |
| Range | [−0.473, +0.435] |

**Complement opposition is MULTI-DIMENSIONAL.** Difference vectors are nearly orthogonal (mean cosine ≈ 0). Each complement pair opposes in its OWN semantic direction — there is no single "opposition axis."

PCA on the 32 difference vectors:

| PC | Variance % | Cumulative % |
|---|---|---|
| PC1 | 10.8% | 10.8% |
| PC2 | 8.2% | 19.0% |
| PC3 | 7.5% | 26.5% |
| PC10 | 4.2% | 63.9% |
| 90% at | — | PC19 |

**19 components for 90%** — the complement opposition is distributed across the full dimensionality of the manifold.

### Complement consistency

Despite multi-dimensionality, complement anti-correlation is robust:
- 28/32 complement pairs are negatively correlated in residual space
- 4 weakly positive exceptions: 升↔无妄 (+0.073), 革↔蒙 (+0.032), 師↔同人 (+0.011), 泰↔否 (+0.007)
- Mean: −0.201 (confirms Phase 1, R112)

**Interpretation:** "Complement hexagrams have opposite themes" is correct, but "opposite" means something different for each pair. 恆/益 oppose along one semantic axis (−0.615), 咸/損 along another (−0.497). The complement involution acts on a high-dimensional thematic space, not a single polarity.

---

## Part C: Beyond Complement — What Else Organizes the Manifold?

### Structural predictors of semantic similarity (RAW embeddings)

Testing on RAW hex centroids (not residuals, to avoid regression artifacts):

| Predictor | Mantel r | p |
|---|---|---|
| Hamming weight proximity | −0.094 | <0.001 |
| Same basin | −0.073 | 0.001 |
| Same surface relation | +0.026 | 0.244 |
| KW adjacency (Xugua) | +0.024 | 0.280 |
| Hamming proximity | −0.019 | 0.399 |
| Any shared trigram | +0.010 | 0.656 |
| Same lower trigram | −0.009 | 0.672 |
| Reverse pair | +0.009 | 0.691 |
| Same palace | −0.006 | 0.803 |
| Same upper trigram | +0.005 | 0.811 |
| Same nuclear hexagram | −0.003 | 0.877 |
| KW number proximity | +0.003 | 0.887 |
| Same i_component | +0.011 | 0.620 |

**No structural feature meaningfully predicts hex semantic similarity.** The two weakly significant predictors (Hamming weight, basin) are both NEGATIVE — meaning hexagrams that share these features are slightly LESS similar, not more. |r| < 0.10 everywhere.

**The thematic manifold is orthogonal to all known algebraic and structural coordinates.** This is the strongest version of the "89% is text-intrinsic" finding: not only does algebra fail to predict what the texts say, but no structural feature at all — not trigrams, not KW order, not nuclear hexagrams, not Xugua sequence — predicts which hexagrams are thematically similar.

---

## Part D: Intra-Hexagram Narrative Structure

### Universal narrative arc: ABSENT

Testing on RAW embeddings (position was already removed from residuals):

| Metric | Value |
|---|---|
| Mean trajectory linearity R² | 0.196 |
| Expected (random) | 0.200 |
| PC1 of mean trajectory vs position | ρ = −0.029, p = 0.957 |
| Shared trajectory variance | 2.4% of within-hex variance |

**No universal narrative arc.** Mean trajectory linearity equals the random expectation. The shared positional pattern explains only 2.4% of within-hex variation — 97.6% is hexagram-specific. Each hexagram tells its own story; there is no common 6-line template.

### Mean trajectory magnitudes

Distance of mean positional deviation from hex centroid:

| Position | Magnitude |
|---|---|
| L1 | 0.0900 |
| L2 | 0.0834 |
| L3 | **0.1067** |
| L4 | 0.0717 |
| L5 | 0.0973 |
| L6 | 0.0796 |

**L3 is the most distinctive position** (largest deviation from centroid). L4 is the least distinctive. This matches the known role of L3 as the "crisis" position (prior work: L3 peaks for 凶, troughs for 吉).

### Position-pair deviations from baseline

Off-diagonal mean cosine similarity ≈ −0.200 (expected from centering). Deviations from this baseline reveal structural patterns:

| Pair | Deviation | Note |
|---|---|---|
| L2↔L4 | **+0.040** | Most similar pair (inner positions of lower/upper trigrams) |
| L1↔L6 | **+0.034** | Boundary positions share themes |
| L1↔L3 | +0.019 | Lower trigram coherence |
| L4↔L6 | **−0.029** | Most dissimilar pair |
| L2↔L5 | −0.008 | Classical pair, but not notably similar |
| L4↔L5 | −0.011 | Adjacent but dissimilar |

**Classical position pairs (L1↔L4, L2↔L5, L3↔L6) are NOT preferentially similar.** Mean classical: −0.203, mean non-classical: −0.196. The classical "correspondence" theory is not reflected in textual similarity.

Instead, the strongest textual similarities are:
- **L2↔L4**: +0.040 above baseline — the "inner" positions (L2 of lower trigram, L1 of upper trigram). Both are positions of entry/approach.
- **L1↔L6**: +0.034 above baseline — the boundary positions. Both deal with beginnings/endings.

---

## Summary

### The architecture of the thematic manifold

1. **High-dimensional** (~20 effective dimensions, no dominant axis)
2. **Orthogonal to all known coordinates** (no structural feature predicts similarity)
3. **Complement-antipodal** (28/32 pairs anti-correlated, but each along its own axis)
4. **No universal narrative arc** (2.4% shared trajectory, 97.6% hex-specific)
5. **L3 is the most distinctive position** (largest deviation from centroid)
6. **L2↔L4 is the strongest position pair** (inner trigram positions share themes)

### What organizes the manifold?

Not algebra. Not trigrams. Not KW order. Not nuclear hexagrams. The organizing principle is **hexagram identity itself** — each hexagram occupies a distinct region of the thematic manifold, and the distances between hexagrams are not predictable from any structural feature we can measure. The 16.8% hex-thematic layer (R118) is a genuine emergent property of the textual corpus, not a shadow of the algebraic skeleton.

The one structural principle that DOES operate in this space is the **complement involution** — but it operates multi-dimensionally, not along a single axis. Each complement pair has its own opposition direction. The complement involution acts as a **thematic antipodal map** on a high-dimensional manifold.

---

## Computation

- Script: `Q1/phase2_manifold_geometry.py`
- Data: `synthesis/embeddings.npz`, `atlas/atlas.json`
- All results reproducible with fixed random seed (42)
