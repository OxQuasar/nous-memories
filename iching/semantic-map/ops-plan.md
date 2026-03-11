# Semantic Map — Operational Plan

## Goal

Bottom-up semantic characterization of I Ching textual layers. Key deliverable: **residual thickness** — the fraction of intrinsic text structure that is independent of algebraic coordinates. Operationalized as MI(intrinsic clusters, full algebraic profile) / H(clusters).

## Design Decisions (from plan discussion)

1. **I.3 before I.2** — stock phrase extraction unlocks meaningful 爻辭 clustering
2. **爻辭 diagnostic-first** — cluster raw 384 embeddings before stripping; result determines downstream weight
3. **Three parallel tracks** from start: (A) stock phrases → 爻辭, (B) 卦辭 clustering, (C) commentary extraction
4. **Layer ordering constraint** applies to algebraic comparison (Layer 2), not data extraction
5. **小象 embedding gated** on I.2 diagnostic — if 15-char 爻辭 embeddings collapse to valence, 12-char 小象 will be worse
6. **Commentary parsing: regex + manual** — no NLP; classical Chinese vocabulary is closed and small
7. **Residual thickness: MI-based** — avoids circularity of "removing" algebraic signal
8. **I.4 (imagery taxonomy) deferred** — lowest priority, unlikely to shift residual thickness
9. **BGE-M3 caveat** — thick residual = lower bound; thin residual carries asterisk

## Dependency Graph

```
S1 (stock phrases) ──→ S5 (爻辭 full) ──→ S7 (algebraic comparison) ──→ S11 (residual thickness)
                                                                                    ↓
S3 (爻辭 diagnostic) ─→ S5                                                    S12 (synthesis)
                     ─→ S6 (小象 gate) ──→ S10 (小象 clustering)                    ↑
                                                                          S8 (大象 bridge) ─┘
S2 (卦辭 clustering) ──→ S7                                               S9 (彖傳 analysis) ┘
                                                                          S10 ─────────────┘
S4 (commentary regex) ──→ S8 (大象 bridge test)
                      ──→ S9 (彖傳 structural)
                      ──→ S10 (小象 positional)
```

Three independent start tracks: {S1, S3} (Track A), {S2} (Track B), {S4} (Track C).

## Segments

### Segment 1: Foundation Extraction (iterations 1-4)

**S1: Stock phrase extraction** [I.3]
- Input: `memories/texts/iching/yaoci.json` (384 line texts)
- Extract all valence markers: 吉, 凶, 悔, 吝, 咎, 厲, 亨, 利, 貞, 無咎, 悔亡, 元亨, 利貞, 利涉大川
- Build 384×N binary presence matrix
- Co-occurrence matrix + PCA → latent dimensionality of marker system
- Positional bias: marker × line position (1-6) contingency table
- Output: `stock_phrases.json` (per-line markers, co-occurrence, PCA components)

**S2: 卦辭 clustering** [I.1]
- Input: `synthesis/embeddings.npz` → guaci (64×1024)
- Multiple algorithms: k-means (k=2..10), hierarchical (ward, complete, average), DBSCAN (sweep ε)
- Stability: compare cluster assignments across methods, report stable clusters
- Silhouette scores for optimal k
- Characterize each stable cluster: which hexagrams, what themes (manual inspection of member texts)
- Output: `guaci_clusters.json` (assignments, centroids, silhouette, stability report)

**S3: 爻辭 diagnostic** [I.2-diag]
- Input: `synthesis/embeddings.npz` → yaoci (384×1024)
- Quick k-means (k=3,5,8), inspect top-3 clusters manually
- Test: do clusters separate by valence markers (吉-dominant, 凶-dominant, 無咎-dominant)?
- Metric: χ² of marker × cluster assignment
- Decision output: {formulaic_dominated: bool, valence_separation_strength: float}
- If formulaic: stripped clustering (S5) becomes essential
- If NOT formulaic: embeddings see past stock phrases, stripped comparison is secondary

**S4: Commentary regex extraction** [III.1 + III.2 + III.3-regex]
- Input: `memories/texts/iching/xiangzhuan.json` (大象 + 小象), 彖傳 text
- **III.1 大象:** Extract (upper_trigram_image, lower_trigram_image, spatial_relation, moral_action) from each of 64 entries. Trigram image vocab: {天,地,雷,風,水,火,山,澤}. Classify relation type: spatial/dynamic/functional.
- **III.2 彖傳:** Extract occurrences of structural vocabulary {剛,柔,上,下,中,正,位,得,失,應,乘,承} from each of 64 entries. Tag with hexagram + line reference where identifiable. Flag 中 for disambiguation (positional vs metaphorical).
- **III.3 小象 vocab:** Extract structural vocabulary {位,中,正,當,應,上下,剛,柔,失位,得位,不當位} from each of 384 entries. Build 384×N feature matrix. Cross-tab with line position (1-6).
- Output: `daxiang_relations.json`, `tuanzhuan_structure.json`, `xiaoxiang_vocab.json`

### Segment 2: Core Clustering (iterations 5-8)

**S5: 爻辭 full analysis** [I.2a + I.2b] — depends on S1, S3
- **I.2a Positional signatures:** Pool all 初爻 (64 texts), all 二爻, etc. Compute centroid per position. Pairwise distances between position centroids. Test: do positions separate? PERMANOVA on position × embedding. Cross-reference with stock phrase positional bias from S1.
- **I.2b Stripped clustering:** Remove valence marker substrings from all 384 texts. Re-embed stripped texts via BGE-M3 (new embeddings needed). Cluster stripped embeddings. Compare with raw clusters from S3. What structure remains after removing the formulaic vocabulary?
- Key question: is dominant structure positional (by line), hexagrammatic (by parent), or phrasal (by formula)?
- Output: `yaoci_clusters.json` (raw + stripped assignments, positional signatures, dominance analysis)

**S6: 小象 embedding gate** — depends on S3
- If S3 shows raw 爻辭 embeddings are NOT valence-collapsed → embed 小象 (384 texts via BGE-M3)
- If S3 shows valence collapse → skip 小象 embedding, rely on regex features from S4 only
- Decision recorded in ops-plan findings

### Segment 3: Algebraic Comparison + Commentary Tests (iterations 9-16)

**S7: Layer 2 algebraic comparison** [II.1 + II.2] — depends on S2, S5
- Load algebraic coordinates from `atlas/atlas.json`: basin, depth, palace, Z₅ surface relation, Z₅×Z₅ surface cell, I-component, kernel
- Cross-tab intrinsic 卦辭 clusters (from S2) × each algebraic partition. χ² or Fisher, Bonferroni correction.
- Cross-tab intrinsic 爻辭 clusters (from S5) × algebraic coordinates (mapped to 384 states via hexagram membership). Add line position as covariate.
- For any significant alignment: measure overlap %, compute MI, check survival after controlling for known bridges (凶×basin, 吉×生体)
- Output: `algebra_comparison.json`

**S8: Commentary bridge test** [大象 imagistic vs 生克] — depends on S4
- From S4's daxiang_relations.json: classify each trigram interaction as:
  - (a) imagistic (天行健 = "heaven moves vigorously" — concrete image)
  - (b) relational/生克 (Wood 克 Earth — element interaction)
  - (c) spatial (thunder below mountain — positional)
- Compare described relation with algebraic surface relation (生/克/比和) for each hexagram
- χ² test: does 大象 relation type predict algebraic surface relation?
- Hypothesis test: 大象 uses imagistic language, NOT 生克 language
- Output: findings in `daxiang_bridge.json`

**S9: 彖傳 structural language analysis** — depends on S4
- From S4's tuanzhuan_structure.json:
  - Frequency of each structural term across 64 entries
  - 剛柔 references × actual yang/yin values at referenced positions
  - 中 references × line 2/5 membership
  - 得位/失位 × yang-in-odd / yin-in-even position
  - 應 references × 1↔4, 2↔5, 3↔6 line pairs
- Cross-tab structural language categories × algebraic partitions (basin, I-component, depth)
- Question: is 彖傳 structural language a precursor to 五行 classification?
- Output: `tuanzhuan_analysis.json`

**S10: 小象 positional clustering** — depends on S4, S6
- From S4's xiaoxiang_vocab.json: cluster 384 entries by structural vocabulary features
- Cross-tab vocabulary clusters × line position (1-6) × algebraic hierarchy (outer core/interface/shell)
- If S6 approved embedding: cluster embeddings too, compare with vocabulary-based clustering
- Key question: does 小象 see the line hierarchy that the deep workflow proved 爻辭 encode?
- Output: `xiaoxiang_clusters.json`

### Segment 4: Integration (iterations 17-22)

**S11: Residual thickness measurement** — depends on S7
- Compute MI(intrinsic cluster assignment, full algebraic profile) for both 卦辭 and 爻辭
- Full algebraic profile = joint variable of (basin, depth, palace, surface_relation, I-component, kernel)
- Normalized: MI / H(clusters) = fraction of text structure that's algebraic
- Threshold: <10% = thick residual, >30% = thin residual
- Characterize what's in the residual: the purely textual structure algebra can't see
- Output: `residual_thickness.json`

**S12: Integration tests + findings synthesis** — depends on S8, S9, S10, S11
- **700-year test:** Do Zhou-era texts have intrinsic structure matching Han-era algebra? Answer: quantitative (MI fraction from S11)
- **Commentary bridge test:** Do Han-era commentaries mediate between text and algebra? Answer: from S8 (大象) and S9 (彖傳)
- **Residual thickness test:** After all algebraic signal, how much remains? Answer: from S11
- Synthesize into unified findings document
- Output: `findings.md`

### Segment 5: Cleanup + I.4 if bandwidth (iterations 23-24)

- Review all outputs for consistency
- I.4 imagery taxonomy if time permits (lowest priority)
- Final findings document revision

## Iteration Budget

| Segment | Steps | Iterations | Notes |
|---------|-------|-----------|-------|
| 1: Foundation | S1, S2, S3, S4 | 1-4 | Parallel tracks, S1 is prerequisite |
| 2: Core clustering | S5, S6 | 5-8 | S5 may need re-embedding (compute) |
| 3: Comparison + commentary | S7, S8, S9, S10 | 9-16 | Largest segment, most analysis |
| 4: Integration | S11, S12 | 17-22 | Synthesis + writing |
| 5: Cleanup | Review + optional I.4 | 23-24 | Buffer |

## Caveats

- **BGE-M3 projection:** All embedding results are "as seen by BGE-M3" — a modern multilingual model projecting classical Chinese. Thick residual = lower bound on actual thickness. Thin residual needs caution.
- **11 prior nulls carried over:** Do not retest basin/palace/I-component/kernel → 卦辭 embedding, surface relation → 爻辭, 納音 → 爻辭, 序卦 → algebra, hu_relation → 吉. All confirmed null.
- **Two confirmed bridges carried over:** 凶×basin (p=0.0002), 吉×生体 (p=0.007). Control for these when testing new alignments.

## File Layout

```
memories/iching/semantic-map/
├── ops-plan.md          # This file
├── PLAN.md              # Original research plan
├── scripts/
│   ├── 01_stock_phrases.py     # S1
│   ├── 02_guaci_clusters.py    # S2
│   ├── 03_yaoci_diagnostic.py  # S3
│   ├── 04_commentary_regex.py  # S4
│   ├── 05_yaoci_full.py        # S5
│   ├── 06_algebra_compare.py   # S7
│   ├── 07_daxiang_bridge.py    # S8
│   ├── 08_tuanzhuan.py         # S9
│   ├── 09_xiaoxiang.py         # S10
│   ├── 10_residual.py          # S11
│   └── utils.py                # Shared loaders, embedding helpers
├── data/
│   ├── stock_phrases.json
│   ├── guaci_clusters.json
│   ├── yaoci_clusters.json
│   ├── daxiang_relations.json
│   ├── tuanzhuan_structure.json
│   ├── xiaoxiang_vocab.json
│   ├── xiaoxiang_clusters.json
│   ├── algebra_comparison.json
│   ├── daxiang_bridge.json
│   ├── tuanzhuan_analysis.json
│   └── residual_thickness.json
└── findings.md
```
