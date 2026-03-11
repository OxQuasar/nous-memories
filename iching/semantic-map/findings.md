# Semantic Map — Findings

> Bottom-up semantic characterization of I Ching textual layers.
> All statistics are exhaustive over the relevant corpus. p-values from permutation tests or exact tests.
> Embedding model: BGE-M3 (1024-dim, Chinese-native). Caveat: all embedding results are projections through a modern multilingual model trained predominantly on contemporary Chinese.

---

## I. Intrinsic Text Structure

### F1: 卦辭 embedding space is diffuse — no discrete clusters [S2, measured]

Silhouette scores: 0.058 (k=2) → 0.032 (k=8). DBSCAN finds 1 cluster. Cross-method stability: kmeans↔ward ARI=0.51, all other pairs ≤0.05.

The 64 judgment texts form no discrete clusters in BGE-M3 space. The corpus is semantically continuous — diffusely distributed with no strong groupings.

### F2: 爻辭 embeddings capture situational content, not formulaic valence [S3, measured]

`formulaic_dominated = False`. Prediction accuracy of cluster membership from valence markers: 47.4% at k=3 (baseline 45.6% — essentially random). No significant χ² for any marker × cluster assignment.

All three k=3 clusters show nearly identical marker distributions (吉: 27-34%, 無咎: 18-24%, 凶: 12-15%). Stripping markers removes only 3.3% of embedding variance (ARI=0.82 raw vs stripped). BGE-M3 embeddings separate on situational/imagistic content, not stock phrases.

### F3: 爻辭 dominant structure is POSITIONAL [S5, measured]

k=3 clusters: position × cluster χ²=37.2, p=0.0001. Only 3/64 hexagrams have all 6 lines in the same cluster — clusters cut across hexagrams.

| Cluster | Size | Position bias | Distinctive vocabulary |
|---------|------|---------------|----------------------|
| 0 | 175 | Peaks at L3 | 厲吉, 有悔, 居貞 — cautionary |
| 1 | 95 | Peaks at L2,L5 | 利用, 有孚, 中行 — central/proper |
| 2 | 114 | Peaks at L1 | 乘馬, 婚媾, 往蹇 — situational |

**Dominant structure: positional (not hexagrammatic, not thematic).** The 384 texts organize by WHERE they sit (line position), not by WHICH hexagram they belong to.

### F4: Marker system has 8 latent dimensions, 3 families [S1, measured]

PCA: 8 components for 90% variance. PC1: 吉(+) vs 無咎(−). Not a simple good/bad axis.

Three marker families:
- **Enabling/neutral:** {無咎, 亨, 利}
- **Favorable outcomes:** {悔亡, 吉, 貞}
- **Unfavorable/cautionary:** {凶, 悔, 吝, 咎, 厲}

Positional bias (significant):
- 吉: peaks at L2,L5 (central), trough at L3. χ²=17.1, p=0.004
- 凶: peaks at L3,L6 (extreme), trough at L5. χ²=17.2, p=0.004
- No other marker reaches significance.

元亨 and 元亨利貞 never appear in 爻辭 — exclusively 卦辭 vocabulary.

### F5: Positional signatures confirm algebraic hierarchy pairing [S5, measured]

PERMANOVA: position explains significant embedding variance (pseudo-F=1.34, p=0.001).

Centroid cosine distances between position pairs:
- L2↔L5 = 0.013 (closest — shared "central" role)
- L3↔L5 = 0.028 (most distant — maximum semantic contrast)
- Hierarchy pairs ({1,6}, {2,5}, {3,4}) mean distance: 0.016 vs non-hierarchy: 0.017

The algebraic hierarchy grouping ({1,6} outer, {2,5} interface, {3,4} core) has slightly tighter within-group centroid distances than cross-group, consistent with the hierarchy organizing semantic content.

---

## II. Algebraic Comparison

### F6: Residual thickness is HIGH — texts are largely independent of algebra [S7, measured]

| Corpus | Algebraic R² | Residual | Note |
|--------|-------------|----------|------|
| 卦辭 (64) | ≤0.36 (joint) | **≥0.64** | No individual coordinate significant; joint R² inflated by overfitting (38 PCA components, 5 predictors, 64 obs). True algebraic R² likely 15-25%. |
| 爻辭 (384) | 0.11 (joint) | **0.89** | More trustworthy (139 PCA components, 384 obs). All individual coordinates significant at p=0.001 but each explains <3%. |

Individual 爻辭 PERMANOVA:
- Line position: R²=0.018, p=0.001
- Basin: R²=0.007, p=0.001
- Surface relation: R²=0.014, p=0.001
- Palace: R²=0.024, p=0.001

**The thick residual.** 89% of 爻辭 embedding variance is text-intrinsic — algebra cannot predict what the texts SAY. The two known bridges operate through marker placement frequencies (distributional), not through semantic content (thematic).

### F7: Both bridges survive position control — genuinely independent channels [CMH tests, measured]

The hypothesis that the two bridges might reduce to a single positional contact was tested by Cochran-Mantel-Haenszel analysis, stratifying by line position:

| Bridge | CMH statistic | p (position-controlled) | MH common OR | Raw OR |
|--------|--------------|------------------------|--------------|--------|
| 凶×basin | 18.11 | 0.000021 | 4.25 | 3.95 |
| 吉×生体 | 8.24 | 0.0041 | 2.19 | 2.10 |

**Both bridges survive position control.** Basin predicts 凶 independently of position (effect slightly STRONGER within strata: MH OR=4.25 > raw OR=3.95). 生体 predicts 吉 independently of position (effect unchanged: MH OR=2.19 ≈ raw OR=2.10).

The text-algebra interface has three independent layers:
1. **Position** → organizes text content (F3) and marker placement (F4)
2. **Basin** → independently constrains 凶 placement (core projection)
3. **体用 relation** → independently constrains 吉 placement (shell projection)

---

## III. Commentary Analysis

### F8: 小象 vocabulary encodes the algebraic 3-layer hierarchy [S4, measured]

Individual term positional bias (all p < 10⁻⁴):

| Term | L1 | L2 | L3 | L4 | L5 | L6 | χ² | p |
|------|----|----|----|----|----|----|-----|---|
| 中 | 0 | 24 | 0 | 3 | 23 | 1 | 80.2 | 7.7×10⁻¹⁶ |
| 位 | 0 | 0 | 10 | 11 | 12 | 0 | 33.4 | 3.2×10⁻⁶ |
| 正 | 6 | 3 | 1 | 0 | 14 | 3 | 28.8 | 2.6×10⁻⁵ |
| 上 | 1 | 2 | 5 | 5 | 5 | 17 | 28.3 | 3.2×10⁻⁵ |
| 當 | 0 | 0 | 11 | 9 | 7 | 1 | 26.0 | 8.9×10⁻⁵ |

Including 初 (concentrated at L1, 6/8) and 下 (concentrated at L1, 6/16), vocabulary terms partition into three groups matching the algebraic hierarchy:

| Algebraic layer | Lines | Vocabulary | Hits |
|---|---|---|---|
| Outer | {1, 6} | 上+下+初 | 33 |
| Interface | {2, 5} | 中 | 47 |
| Core | {3, 4} | 位+當 | 44 |

Reduced 3×3 table: χ² = 124.9, p = 4.9×10⁻²⁶. The tradition uses distinct vocabulary for each algebraic layer.

The alignment is not convergent recognition of separate things — it is two descriptions of one structural fact: the hierarchy forced by the 3+3 factorization. Lines 2,5 are literal centers of their respective trigrams (→ 中). Lines 3,4 are the boundary between trigrams (→ 位/當). Lines 1,6 are physical extremes (→ 初/上/下). The algebra formalizes the same hierarchy through the nuclear transform (互 reads bits b₁-b₄, making lines 3,4 informationally densest and lines 1,6 invisible). Both the tradition and the algebra read the hexagram format itself.

### F9: 小象 has no algebraic signal beyond position [S10, measured]

Vocabulary clusters are strongly position-dependent (silhouette 0.63 at k=6). After controlling for position:
- Basin residual: R²=0.033, p=0.088 — NOT significant
- Embedding clusters show no overlap with vocabulary clusters (ARI≈0)

The 小象 sees positions, not the algebraic coordinates that happen to be computable from those positions.

### F10: 大象 operates in imagistic register, not 生克 [S8, measured]

Relation types: spatial 37 (58%), functional 14 (22%), dynamic 13 (20%).

- Zero 五行 relational terms (金/土/相生/相克/五行) in moral/action portions
- 水/火/木 appear only as nature images (天與水違行, 地中生木), not elemental theory
- Relation type × surface relation: χ²=15.16, p=0.056 (marginal)
- Trigram image match rate: 78% (50/64); mismatches use secondary images (雲=水, 泉=水, 電=火, 木=風)

**比和 fraction by relation type:** dynamic 46.2%, functional 35.7%, spatial 8.1%. Same-element pairs get dynamic descriptions (天行健) rather than spatial ones — no spatial contrast to describe when trigrams are identical.

The 大象 describes trigram interaction through concrete imagery, not through elemental dynamics. The 五行 framework is a separate formalization layer.

### F11: 彖傳 tracks binary structure, not algebraic coordinates [S9, measured]

**Accuracy of structural references:**
- 中 references: 100% accurate (always at L2/L5; 剛中=16, 柔中=5, all correct)
- 剛/柔 with line reference: 13/23 correct (57%) — regex matching is approximate
- 應 references: 55% of line pairs are actually "responding" vs 47% baseline — weak tracking

**Cross-tab with algebraic coordinates — all null:**
- 剛/柔 ratio × basin: H=1.13, p=0.57
- Structural density × I-component: U=531, p=0.80
- 往/來 × surface_relation: H=2.53, p=0.64

The 彖傳 has a vocabulary for binary structure (yang/yin, position, correspondence) but NOT for the 五行 superstructure. It operates in the binary (Z₂) register, not the pentadic (Z₅) register.

**Anomaly detection pattern:** Kun basin has the HIGHEST 剛/柔 ratio (2.14 — more 剛 references in the predominantly yin basin). The 彖傳 comments on what's noteworthy/unusual, not what's dominant. This is anomaly detection, not category assignment. The same information-theoretic stance as the depth gradient: information concentrates at boundaries (depth-1 peak in 凶, not at attractors).

---

## IV. Integration Tests

### IV.1 The 700-year test

**Answer: The algebra and texts share a narrow interface — two bridges plus position — but are otherwise independent systems.**

The algebra is partially descriptive: it captures the positional hierarchy that the texts encode (F3, F5, F8). But it is not generative: it does not determine semantic content (F6: 89% residual). The two bridges (凶×basin, 吉×生体) are genuine but narrow — distributional constraints on WHERE markers appear, not determinants of WHAT texts SAY.

The pre-algebraic tradition (爻辭 ~9th c. BC, 小象/彖傳 ~5th-3rd c. BC) sees binary structure (yang/yin, position, correspondence) but not the 五行 superstructure (elements, basins, surface relations) that came with Han dynasty formalization. The 五行 framework is descriptive of patterns in the texts but was not read from the texts — it was an independent mathematical framework that happens to capture two distributional regularities (凶 placement, 吉 placement) in the pre-existing corpus.

### IV.2 The commentary bridge test

**Answer: The commentary tradition does NOT mediate between text and 五行 algebra.**

- 大象: imagistic (F10) — no 五行 vocabulary
- 彖傳: binary-structural (F11) — sees Z₂ (yang/yin), not Z₅ (elements)
- 小象: positional (F8, F9) — sees line hierarchy but not algebraic coordinates beyond position

All three commentary layers operate in non-algebraic registers. The 五行 formalization is a separate layer — not a reading of the earlier tradition but an independent mathematical framework imposed later.

### IV.3 The residual thickness test

**Answer: THICK residual.**

| Measure | Value | Interpretation |
|---------|-------|----------------|
| 卦辭 algebraic R² | ≤0.36 (likely 0.15-0.25) | Most embedding variance is text-intrinsic |
| 爻辭 algebraic R² | 0.11 | 89% of embedding variance is text-intrinsic |
| 凶×basin (position-controlled) | OR=4.25, p=0.00002 | Genuine, not positional artifact |
| 吉×生体 (position-controlled) | OR=2.19, p=0.004 | Genuine, not positional artifact |

The system has two genuinely independent layers (algebraic + textual), touching at narrow bridges. The bridges are distributional (marker placement frequencies), not thematic (what texts say). The 11 prior null results (embeddings × all algebraic partitions, all p>0.4) are confirmed and explained: the texts' semantic content is orthogonal to algebraic structure.

**BGE-M3 caveat:** Thick residual = lower bound on actual thickness (the model may miss text structure that would make the residual thicker). Thin residual would carry an asterisk (the model might impose similarity not present in classical Chinese). Since the residual IS thick, the finding is robust: even a modern model that might flatten classical Chinese distinctions sees 89% independence.

---

## V. Implications for Unification

### Gap 5 (Statistical Gluing) is thinner than feared

The PG(2,2) unification framework identified Gap 5 — the difficulty of mixing statistical evidence with algebraic proof — as partially addressed but open. The semantic map clarifies the scope of this gap:

The statistical bridge operates through a very specific, narrow channel: marker placement frequencies correlate with algebraic coordinates, but 89% of the texts' semantic substance floats free. The 0.5-bit cosmological choice that R32 resolves through 吉×生体 is the entire bridge to the textual tradition — there is no hidden systematic alignment waiting to be discovered.

The gluing is thin but genuine. It is thin because the texts have rich independent structure (thick residual). It is genuine because both bridges survive position control (F7) and neither is reducible to the other (they operate through different algebraic projections: core vs shell).

### The temporal architecture

Three historical layers, three different registers:

| Layer | Period | Register | What it sees |
|-------|--------|----------|-------------|
| 爻辭 | ~9th c. BC | Situational/imagistic | Positions, processes (凶=stasis, 吉=flow) |
| 小象/彖傳 | ~5th-3rd c. BC | Binary-structural | Yang/yin, centrality, correspondence |
| 五行 formalization | ~1st c. BC | Pentadic-algebraic | Elements, basins, surface relations |

Each layer sees the hexagram through its own vocabulary. The algebraic layer (五行) captures two distributional patterns in the earliest layer (爻辭) — but these patterns concern marker placement, not semantic content. The commentary layers (小象/彖傳) bridge temporally but not algebraically: they see the binary structure that the algebra formalizes but use different vocabulary and different conceptual frameworks.

*Remark: The three registers suggestively map to the three primes of PG(2,2) — prime 2 (binary polarity), prime 3 (positional hierarchy), prime 5 (cyclic dynamics). The commentary tradition sees primes 2 and 3 but not prime 5. This is a pattern observation, not a proven correspondence.*

### What the texts encode independently

The 89% residual is not noise — it is structured situational/imagistic content that organizes by line position. The texts encode:
1. A positional hierarchy (central/extreme, with 吉 at center and 凶 at extremes)
2. Situational imagery (horses, marriages, journeys, conflicts) that varies by position type
3. Navigational vocabulary (enabling/cautionary/favorable markers with 8-dimensional latent structure)

This content exists independently of — and 700 years prior to — the algebraic formalization. The algebra describes the container (Z₂⁶ with its projections and hierarchies); the texts describe the contained (situations, processes, outcomes). They touch at two narrow distributional bridges but are otherwise separate systems describing the same 64×6 state space from different angles.

---

## Epistemic Status

| Category | Claims | Status |
|----------|--------|--------|
| **Measured** | Residual thickness (64%/89%); both bridges survive position control (CMH); 卦辭 diffuse; 爻辭 positional dominance; marker 8-dim/3-family structure; 小象 3-layer vocabulary (χ²=125); 大象 imagistic register; 彖傳 binary-structural; all commentary × algebra nulls | Exhaustive computation or exact/permutation test |
| **Structural interpretation** | "Texts encode process, algebra encodes structure"; "五行 is a second translation layer"; "彖傳 does anomaly detection"; "bridges are distributional, not thematic"; "three historical layers, three registers" | Pattern descriptions of measured facts — interpretive framing |
| **Caveats** | 卦辭 joint R² inflated by overfitting; BGE-M3 projection may flatten classical Chinese distinctions; 小象 surface_relation residual (R²=0.061) not permutation-tested | Known limitations, flagged |

---

*Scripts: `01_stock_phrases.py` through `09_xiaoxiang.py`*
*Data: `data/` directory (13 JSON files)*
*Cross-references: synthesis/findings.md, mh-atlas/findings.md, deep/exploration-log.md, unification/toward-unification.md*
