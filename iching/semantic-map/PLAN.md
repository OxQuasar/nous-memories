# Semantic Mapping — Text-First Characterization

## Why This Matters

All prior semantic work tested algebra → text: does this algebraic partition predict textual content? Eleven null results. Two narrow bridges (凶×basin p=0.0002, 吉×生体 p=0.007). These bridges are the only empirical glue connecting the algebraic structure to the corpus.

The unification program depends on knowing how thick this glue is. Is it two point contacts (thin, possibly accidental), a systematic partial alignment (formalizable as a noisy functor), or total orthogonality plus coincidences (not formalizable)? This question can only be answered by reversing the direction: text → structure → compare with algebra.

**The temporal separation argument.** The 卦辭/爻辭 predate the algebraic formalization by ~700 years (Zhou dynasty texts, Han dynasty systematization). If the texts have intrinsic structure that aligns with algebra, the algebra is descriptive (modeling something real). If they don't, the algebra is notational (imposed framework). Either outcome changes what the unification framework needs to explain.

## What exists

**Embeddings:** BGE-M3 (1024-dim, Chinese-native). Already computed for 卦辭 (64), 爻辭 (384), 大象 (64), 彖傳 (64). Stored in `synthesis/embeddings.npz`.

**Texts available but not embedded:** 小象 (384 entries, in xiangzhuan.json), 序卦 (64, in xugua.json — may be in npz), 說卦/雜卦/繫辭 (not available as structured JSON).

**Null results (carry over, do not retest):**
- Basin, palace, I-component, kernel → 卦辭 embedding: all p > 0.4
- Surface relation → 爻辭 embedding: <1% variance explained
- 納音 names → 爻辭 content: null beyond element
- 序卦 narrative → algebraic transitions: null
- hu_relation → 吉: null (p=0.731)

**Code:** `spaceprobe/kwprobe/17_semantic_embeddings.py` (embedding generator), `synthesis/01_decisive_test.py` (clustering tests), `atlas/12_semantic_screens.py` (thematic screens).

---

## The Approach: Bottom-Up

Every prior probe asked: "given this algebraic partition, do the texts cluster accordingly?" That's top-down. This mapping asks: "what structure do the texts have on their own terms, and where does it happen to align with algebra?"

Three layers, each independent:

### Layer 1: Intrinsic text structure (no algebra)
### Layer 2: Algebraic comparison (where do they touch?)
### Layer 3: Commentary analysis (what does the interpretive tradition see?)

---

## I. Intrinsic Text Structure

### I.1 卦辭 clustering (64 texts)

Embed all 64 卦辭. Cluster without any algebraic reference (k-means, hierarchical, DBSCAN — try multiple, report stable clusters). Characterize each cluster: what themes, imagery, vocabulary, situations define it?

**Questions:**
1. How many natural clusters exist? Is the corpus semantically homogeneous (1-2 clusters = flat) or structured (4-8 clusters = rich taxonomy)?
2. What are the cluster boundaries? Thematic (war/agriculture/marriage)? Tonal (warning/encouragement/neutral)? Situational (crisis/stability/transition)?
3. Do any clusters correspond to known textual categories (e.g., the received groupings of "auspicious" hexagrams)?

### I.2 爻辭 clustering (384 texts)

Same approach, larger corpus. The 384 line texts are more formulaic (short, often share stock phrases like 無咎, 悔亡, 利涉大川). Two sub-analyses:

**I.2a. By line position.** Pool all 初爻 (64 texts), all 二爻, etc. Does each position have a semantic signature? The deep workflow proved line positions encode the algebraic hierarchy (outer core / interface / shell, p<0.001 for valence). Do they also encode thematic content? Initial lines about beginnings, fifth lines about authority, top lines about excess?

**I.2b. Full 384 clustering.** Cluster all 384 爻辭. Compare cluster membership with: (a) line position, (b) hexagram membership, (c) stock phrase presence. Is the dominant structure positional (lines cluster by position) or hexagrammatic (lines cluster by parent hexagram) or phrasal (lines cluster by formulaic content)?

### I.3 Stock phrase extraction

The 爻辭 use a limited vocabulary of outcome markers: 吉, 凶, 悔, 吝, 咎, 厲, 亨, 利, 貞. Extract all instances. Build the co-occurrence matrix: which markers appear together? Which are mutually exclusive?

**Questions:**
1. Is there a latent dimensionality to the marker system? (PCA on the co-occurrence matrix)
2. Do markers cluster into families (e.g., {吉, 亨, 利} vs {凶, 厲, 咎})?
3. Are some markers positionally biased (e.g., 咎 predominantly at line 3)?

### I.4 Imagery taxonomy

Extract concrete imagery: animals (龍, 馬, 鹿, 豕, 魚), natural features (川, 山, 冰, 雷), human situations (婚姻, 師, 寇). Build a taxonomy of image types. Map which hexagrams use which imagery.

**Question:** Is the imagery randomly distributed, or does it cluster? If it clusters, do the clusters have any algebraic correlate?

---

## II. Algebraic Comparison

Only after Layer 1 produces intrinsic clusters. Do NOT use algebraic partitions to guide clustering.

### II.1 Cluster × algebra cross-tabulation

For each intrinsic cluster from I.1/I.2, compute overlap with every algebraic partition:
- Basin (Kun/Qian/Cycle)
- Depth (0/1/2)
- Palace (8 palaces)
- Z₅ surface relation (5 diagonals)
- Z₅×Z₅ surface cell (25 cells)
- I-component (0/1)
- Kernel (8 types)

Use χ² or Fisher exact test for each. Bonferroni correction for multiple comparisons.

**Expected:** Most will be null (prior work). The question is whether bottom-up clusters reveal alignments that top-down partitions missed — alignments invisible when you start from the algebra because they don't respect any single algebraic coordinate.

### II.2 Partial alignment characterization

For any significant alignment found:
- How much of the cluster is explained by the algebraic partition? (% overlap, mutual information)
- Is the alignment with a single algebraic coordinate or a conjunction?
- Does the alignment survive after controlling for the two known bridges (凶×basin, 吉×生体)?

### II.3 The residual

After removing all algebraic signal: what's left? Characterize the purely textual structure that algebra can't see. This residual IS the text's independent contribution — the semantic content that exists prior to and independent of the algebraic formalization.

**For unification:** The residual's size determines whether statistical gluing is thin (small residual = most text structure IS algebraic) or thick (large residual = texts have their own world).

---

## III. Commentary Analysis

The commentaries (象傳, 彖傳) are the tradition's own semantic mapping — Han-era scholars relating the texts to trigram structure. They bridge the temporal gap between Zhou texts and Han algebra.

### III.1 大象 trigram relation extraction

Each of the 64 大象 names both trigrams and describes their interaction. Parse systematically:

1. Which trigrams are mentioned? (Verify they match the hexagram's actual trigrams)
2. What relation is described? Categorize: spatial (above/below), dynamic (generates/overcomes), functional (illuminates/nourishes/obstructs)
3. Does the described relation map to the algebraic surface relation (生/克/比和)?

**Hypothesis:** 大象 uses spatial/imagistic language, not 生克 language. If confirmed, the commentary tradition sees trigram relations through imagery (thunder below mountain = restraint) not through elements (Wood below Earth = 克). The 五行 formalization would then be a second translation layer, not a direct reading of the text.

### III.2 彖傳 structural language

The 彖傳 explicitly discusses hexagram structure (剛柔, 上下, 中正). Extract:

1. **剛柔 (firm/yielding)** references — which lines, which positions? Compare with the yang/yin values.
2. **上下 (above/below)** references — trigram interaction? Line position? Both?
3. **中 (center)** references — line 2 and 5? Something else?
4. **得位/失位 (proper/improper position)** — yang in odd positions, yin in even? How systematic?
5. **應 (correspondence)** — lines 1↔4, 2↔5, 3↔6? How often mentioned, does it predict content?

**Question:** Is the 彖傳's structural language a precursor to 五行 classification? Do 剛柔 and 上下 partition the hexagrams in ways that align with basin, I-component, or surface relation?

### III.3 小象 line-level commentary (384 entries)

Never analyzed. Each 小象 comments on one line of one hexagram. Embed all 384, cluster, and cross-reference with:
- Line position (1-6)
- The algebraic hierarchy (outer core / interface / shell)
- The corresponding 爻辭's valence markers

**Question:** Does 小象 see the line hierarchy that the deep workflow proved the 爻辭 encode? The 小象 is explicitly interpretive — it explains why each line says what it says. If the explanations cluster by algebraic position, the tradition implicitly recognized the hierarchy before formalizing it.

---

## IV. Integration Tests

### IV.1 The 700-year test

Do Zhou-era texts (卦辭, 爻辭) have intrinsic structure that matches Han-era algebra (五行, 納甲, 宮)?

- If yes → the algebra discovered pre-existing structure. The unification framework must account for a real correspondence.
- If no → the algebra imposed structure. The statistical bridges (凶×basin, 吉×生体) are thin coincidences. The unification framework's "statistical gluing" gap is smaller than feared.

### IV.2 The commentary bridge test

Do Han-era commentaries (象傳, 彖傳) use structural language that mediates between text and algebra?

- If 彖傳's 剛柔/上下 categories align with binary coordinates (I-component, depth) → the commentaries translate between textual imagery and algebraic structure
- If 大象's trigram interactions use imagistic language unrelated to 生克 → the 五行 layer is a separate formalization, not a reading of the earlier tradition

### IV.3 The residual thickness test

After all algebraic signal is removed from the texts, how much intrinsic structure remains?

- Thick residual (texts have rich independent structure) → the system has two genuinely independent layers (algebraic + textual), touching at narrow bridges
- Thin residual (most text structure is algebraic) → the system is more unified than current evidence suggests, and the 11 null results were asking the wrong questions

---

## V. Outputs

### Data files

- `text_clusters.json` — intrinsic clustering of 卦辭 and 爻辭 (cluster assignments, centroids, silhouette scores)
- `stock_phrases.json` — extracted markers, co-occurrence matrix, PCA components
- `imagery_taxonomy.json` — concrete imagery extracted, hexagram assignments, cluster cross-reference
- `daxiang_relations.json` — parsed 大象 trigram interactions, relation categories
- `tuanzhuan_structure.json` — extracted structural language (剛柔, 上下, 中, 得位, 應)
- `xiaoxiang_clusters.json` — 小象 embeddings and clustering
- `algebra_comparison.json` — cross-tabulation of intrinsic clusters × algebraic partitions

### Findings

- `findings.md` — per-section results, the three integration tests, residual characterization

### What carries over (no recomputation)

- All embeddings in `synthesis/embeddings.npz` (卦辭, 爻辭, 大象, 彖傳)
- All null results (11 tests, listed above)
- Both confirmed bridges (凶×basin, 吉×生体)
- All algebraic coordinates from atlas.json

### What's new

- Bottom-up clustering (Layer 1) — never attempted
- 小象 analysis (III.3) — never embedded
- Commentary structural language extraction (III.1, III.2) — never parsed systematically
- The integration tests (IV) — the questions that matter for unification

---

## Estimated Scope

**Computation:** Medium. Embedding generation is fast (BGE-M3 inference). Clustering is standard. The cross-tabulation is combinatorial but small (64 or 384 objects × ~15 algebraic coordinates). Main cost is running multiple clustering algorithms to find stable structure.

**Text extraction:** Medium-heavy. 大象 and 彖傳 parsing requires Chinese NLP — extracting trigram references, relation words, structural vocabulary from classical Chinese text. Semi-automated: regex + manual verification.

**小象 embedding:** Light. 384 texts already in JSON. Embed via existing infrastructure, cluster, cross-reference.

**Total:** 2-3 iterations of a compute workflow. The heaviest lift is the commentary parsing (III.1, III.2), which requires careful text processing.

---

## Dependency on Unification

This mapping feeds the unification program at three points:

1. **Residual thickness** → determines whether "statistical gluing" is a real gap or a thin appendage
2. **Commentary bridge** → determines whether the tradition itself saw a mediating structure between text and algebra
3. **700-year alignment** → determines whether the algebraic formalization discovered or invented structure

These are the three things the unification framework needs to know before it can formalize the text-algebra relationship. Without them, the framework is designing a bridge without knowing the distance between the banks.
