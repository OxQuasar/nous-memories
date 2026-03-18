# I Ching Research — Captain's Log

## Key Files

- Research directory: `memories/iching/directory.md`
- Core texts: `memories/texts/iching/` (yaoci.json, guaci.json, tuan.json, xiangzhuan.json, xugua.json)
- Atlas: `memories/iching/atlas/atlas.json` — hex profiles, `kw_number`, `complement`, `reverse`, `lower_trigram`, `upper_trigram`, `basin`, `palace`, `surface_cell`
- Embeddings: `memories/iching/synthesis/embeddings.npz` (keys: guaci, yaoci, daxiang, tuan; yaoci = 384×1024 BGE-M3)
- Reversal investigation: `memories/iching/reversal/` — main research program
  - `findings.md` — canonical results document (R94–R180)
  - `questions.md` — all questions closed, program summary
  - `exploration-log.md` — iteration-by-iteration log (19 iterations)
  - `resonance-tests.md` — T1/T2/T3 framework (all complete)
  - `Q1/` — computation scripts and cached embeddings (phases 1–8)
  - `Q2/` — axiom investigations including Q2 Proper
  - `Q2T2/`, `Q3/`, `T3/` — investigation phases
- East/West investigation: `memories/iching/eastwest/` — cyclotomic, KW sequence, torus coherence, dynamics, perturbation, cross-architecture replication
  - `findings.md` — canonical results document (R181–R214)
  - `exploration-log.md` — iteration-by-iteration log (12 iterations, R181–R214)
  - `questions.md` — all questions closed
  - Scripts: `cyclotomic_probe.py`, `kw_sequence_probe.py`, `torus_coherence.py`, `differentiation_principle.py`, `hu_cell_validation.py`, `dynamics_probe.py`, `edge_type_decomposition.py`, `perturbation_directions.py`, `sikuroberta_replication.py`, `pair_concordance.py`
- Fibonacci / opposition manifold investigation: `memories/iching/fibo/` — Fibonacci alignment, opposition space probes, cross-layer geometry, independence tests
  - `findings.md` — canonical results document (R215–R237)
  - `questions.md` — Fibonacci open questions 
  - `exploration-log.md` — iteration log (8 iterations: Fibonacci + semantic probes + cross-layer + position-resolved + Hamming-length + unification + d=2/reversal + trigram decomposition)
  - `fibo_probe.py`, `semantic_probes.py`, `artifact_check.py`, `cross_layer_opposition.py`, `position_resolved.py`, `hamming_length.py`, `unification_test.py`, `reversal_and_d2_retest.py`, `trigram_d2_decomposition.py`, `rank_bimodality.py` — computation scripts

## Research Program Status: (237 results, 1 retracted)

### Characterization

The (3,5) structure is the unique rigid formalization of composable polarity with dual evaluation. One contingency: the group axiom. The thematic manifold has ~16 cross-model-stable opposition dimensions within yaoci, irreducibly non-algebraic. The system organizes conceptual space for judgment under uncertainty — mathematical, not physical.

**Epistemic caveat (R225):** The ~16 dimensions are "text-intrinsic" in the cross-model sense (stable across 4 embedding architectures on yaoci). They are NOT demonstrably "concept-intrinsic" — cross-layer comparison (yaoci vs guaci/tuan/daxiang) is confounded by genre differences. Whether the same conceptual oppositions manifest across text layers is untestable within the embedding paradigm.

**Resonance verdict: T1+, T2−, T3−.** Mathematically special given the framing; culturally specific (assembled once); empirically ungrounded (doesn't map onto physical dynamics).

**Opposition manifold terminal characterization (R215–R237):** Three mutually independent organizational principles in the ~16-dim opposition space: text length (~1 dim, vocabulary-accessible), d=1 differentiation (vocabulary-inaccessible), d=6 complement opposition (vocabulary-inaccessible). One coupling at d=2 (ρ ≈ −0.30, distributed across trigram components). Non-decomposability confirmed across five independent factoring axes (R167, R170, R210, R220, R236). Embedding methodology at resolution limit.

### Result Map

| Investigation | Results | Key Finding |
|---|---|---|
| Q2 T1: Axiom systems | R73–R93 | (3,5) forced given framing; framing is tightest window |
| Q2 T2: Cross-cultural | R94–R111 | Binary converges; dual-cycle surjection unique to China |
| Q1 Phases 1-7: Residual | R112–R166 | ~16-dim text-intrinsic opposition space, algebraically opaque |
| Q3: Judgment boundary | R140–R150 | 5 operations, 3 phases, designed specification gap |
| Q1 Phase 8: Directions | R167–R170 | Trigram decomposition negative; directions text-intrinsic (ρ=0.88) |
| Q2 Proper: Forcing chain | R171–R175 | Minimum |S|=6; gap at group axiom; irreducible |
| T3: Climate asymmetry | R176–R180 | {4,2,2,2,2} cardinality appears; structural prediction 0/83 |
| East/West: Cyclotomic | R181–R188 | φ and dual cycles share Q(ζ₅) — "address with conditional resonance" |
| East/West: Text/Sequence | R189–R196 | KW ordering is semantic not algebraic. 生/克 invisible in texts |
| East/West: φ in dynamics | R197–R209 | φ in cube-edge partition (克=P₄∪P₄). No bridge to text at any resolution |
| Perturbation directions | R210–R211 | d=1 directions full-rank (hexagram-specific). Partial bit-position alignment |
| Cross-architecture replication | R212–R213 | Tier 1b confirmed on SikuRoBERTa. ~85% geometry text-intrinsic, ~15% architecture-dependent |
| Q4 closure | R214 | φ in 5-fold systems trivially affirmative (arithmetic); Route B in nature negative (no known instantiation) |
| Fibonacci alignment + Opposition manifold | R215–R218 | Arithmetic coincidence — triple hit at n=3 only, no Fibonacci in dynamics or orbit counts |
| Semantic probes | R219–R223 | Text length aligns with opposition (1 of ~16 dims). Opposition is vocabulary-diffuse, not vocabulary-opaque |
| Cross-layer geometry | R224–R227 | Opposition geometry is layer-specific. Guaci↔tuan coupled (commentary). Yaoci disconnected (genre confound) |
| Position-resolved opposition | R228–R231 | L1 least opposed. d=1 differentiation flat (holistic). 升↔无妄 bimodal at L3/L5 (pair-specific) |
| Hamming-length independence | R232–R234 | R159 and R219 completely independent. Hamming V-shape is residual-space only. Text length has zero mediation |
| Unification test | R235 | d=1 and d=6 independent — two separate organizing principles |
| d=2 coupling + reversal | R236–R237 | d=2 anti-coupling confirmed (distributed, non-decomposable). Reversal non-significant |
| Trigram decomposition | R236 update | d=2 coupling distributed across trigram components. Non-decomposability confirmed |

### Non-Decomposability Inventory

The thematic manifold resists decomposition at every resolution tested:

| Resolution | Test | Result |
|---|---|---|
| d=1 direction (R210) | Line perturbation mean directions | Rank ~5.4/6, hexagram-specific |
| d=1 magnitude (R209) | 五行 edge type predicts anti-correlation? | Null (controlled for line position) |
| d=1 by bit position (R229) | Differentiation varies by which line flips? | No — flat across all 6 positions |
| d=6 direction (R167) | Complement opposition factors through trigrams? | No |
| d=6 by position (R228) | Opposition varies by line position? | Mildly — L1 least opposed, range ~6.7% |
| All algebraic (R170) | Any grouping predicts direction? | No |
| Partial structure (R211) | Bit-position signature in relative cosines | Within > cross (5/5 sources), layer-stratified |
| Vocabulary probes (R219–R220) | 8 lexical axes tested against opposition | Text length captures ~1 dim; 7 content probes weak/null |
| Text length × Hamming (R232–R233) | Does text length mediate the Hamming V-shape? | No — zero mediation, orthogonal dimensions |
| Cross-layer (R225) | Opposition geometry shared across text layers? | Not testable (genre confound) |
| d=2 coupling (R236) | Trigram sub-component predicts d=2 anti-coupling? | No (distributed, 0/4 individually) |

### Complement Involution: Nine Levels

Forced → Natural → Pervasive → Rich → Opaque → Lexically Invisible → Non-Decomposable → Compositional → Text-Intrinsic

**Update (R219–R222):** The "Lexically Invisible" level is refined: the opposition is not vocabulary-opaque but vocabulary-*diffuse*. Text length captures ~1 dimension of opposition (5–11% R², cross-model). Content vocabulary (吉凶, 往來, social, temporal) shows diffuse weak alignment (7.5× enrichment over chance) but no single content axis reaches cross-model significance. The sole persistent exception (升↔无妄, R158) is lexically unremarkable (R222). Overall: ~1/16 of opposition is mechanically capturable; ~15/16 remains lexically inaccessible.

**Update (R225–R226):** The "Text-Intrinsic" level needs qualification: cross-model stable within yaoci, but not demonstrably cross-layer stable. The 升↔无妄 anomaly is layer-dependent (rank 29/32 in guaci, 17/32 in yaoci).

**Update (R228, R231):** The "Compositional" level gains new detail: opposition is mostly holistic across positions (R228, range ~6.7%), with L1 (initial line) consistently least opposed. But individual pairs can have strongly bimodal positional profiles (R231: 升↔无妄 opposed at L3/L5, concordant at L1/L2/L4/L6). The pair-specific bimodality is cross-model consistent.

## Epistemic Tier System

- **Tier 1 (theorems):** R85, R75, R87, R102, R108, R171–R174, R181–R187, R197–R205, R207–R208, R215–R217. Mathematical proofs.
- **Tier 1b (text-intrinsic):** R156–R159, R161–R163, R167–R170, R212, R213 (pair ranking). Cross-model validated across BGE-M3/E5-large/LaBSE/SikuRoBERTa (4 architecturally distinct models). R213 quantifies: ~85% of opposition geometry is cross-architecture invariant. **Caveat (R225):** "text-intrinsic" means cross-model within yaoci, not cross-layer.
- **Tier 2 (measurements):** R151, R164–R166, R176–R179, R189–R190, R192–R196, R206, R209–R211, R213 (angular structure), R218, R219–R237. Method-dependent.
- **Tier 3 (interpretations):** R175, R180, R188, R214-Q4b. Revisable.
- **Retracted:** R191 (surface cell anti-signal — failed cross-model replication).

### Vulnerability
All Tier 1b findings depend on transformer-based neural network embeddings. Four models agree across distinct training data (multilingual web / classical Chinese 四库全书), training objectives (contrastive similarity / masked LM), architectures (BERT-base / various larger encoders), and embedding methods (mean-pooled hidden states / fine-tuned sentence pooling). R213 quantifies the boundary: pair-level opposition ranking is cross-architecture invariant (profile ρ = 0.80–0.83), while fine-grained angular structure is ~85% recoverable with ~15% architecture-dependent (correlating with training-data cultural salience, not text content). The remaining vulnerability is that all are transformer-based. A non-neural approach would be a different research program.

**Additional vulnerability (R225):** Cross-model stability within a text layer does not imply cross-layer stability. The ~16 opposition dimensions may be properties of the yaoci text type (formulaic line texts), not of the hexagram concepts. Genre differences between text layers (line texts vs paragraphs) confound cross-layer comparison in embedding space.

### Algebraic R² Two-Band Structure
The "80/20" language comes from the judgment tradition's self-description. Empirical split:
- **10.8–11.0%** across 3 multilingual sentence-transformers (remarkably tight 0.2pp band — model-invariant within class)
- **13.2%** on SikuRoBERTa (classical-Chinese BERT — domain sensitivity, not artifact)

The tight multilingual band is itself a finding. The 2pp elevation on domain-matched model suggests multilingual models partially miss vocabulary patterns correlated with algebraic coordinates. The tradition overestimates its algorithmic coverage regardless (~80% claimed vs ~87–89% measured).

### Two Routes to φ (iterations 7–9)

φ appears at (3,5) through two structurally independent mechanisms:

1. **Route A (cyclotomic):** Q(ζ₅)⁺ = Q(√5) forces Walsh spectra and Galois traces into Q(φ). Top-down, unconditional (all 240 surjections).
2. **Route B (combinatorial):** The 克 edges of the 3-cube form P₄ ∪ P₄, with eigenvalues 2cos(kπ/5) = {φ, 1/φ, −1/φ, −φ}. Bottom-up, conditional (96/240 surjections, determined by Jacobian type).

The two routes converge because 2^{n-1}+1 = 2ⁿ−3 = p has the unique solution n=3. At (4,13) the path denominator would be 9 ≠ 13 and φ disappears.

**No bridge from Route B to text — tested at three resolutions:**

| Resolution | Test | Result |
|---|---|---|
| Torus cell (R192) | 生/克/比和 semantic information | Null |
| Nuclear hex (R206) | hu_cell × Jacobian coupling | p = 0.996 |
| Cube edge (R209) | 克 vs 生 d=1 transitions, controlled for line position | p > 0.2, inconsistent sign |

**Final verdict on R188:** "Address with conditional resonance" — fully characterized, no bridge to text, investigation closed.

### Fibonacci Alignment (iteration 1)

The I Ching's parameters {2,3,5,8} are consecutive Fibonacci numbers F(3)–F(6). Investigation tested whether this is structural (additive self-reference in the derivation) or coincidental (small-number overlap).

### Semantic Probe Vectors (iteration 2)

8 vocabulary-based probes tested against the complement opposition space across 4 models × 2 text layers.

**Verdict: opposition is vocabulary-diffuse, not vocabulary-opaque.** Text length is the only cross-model significant probe (p<.001 in 4/4 yaoci models + guaci, R² = 5–11%). It is not a centroid geometry artifact (ρ ≈ 0 between length and distance-to-mean). Content probes (吉凶, 利, 往來, 貞, social, temporal, negation) show diffuse enrichment (15/40 at p<.05, expected 2.0) but no single content axis reaches cross-model significance. Negation is absorbed by text length in yaoci; marginal independent guaci signal (p=.01 residualized).

**升↔无妄** is lexically unremarkable — the R158 anomaly is not vocabulary-accessible.

**Guaci text-length asymmetry** is complement-specific (p=.008); yaoci is not (p=.32). The complement involution correlates with judgment verbosity but not line-text verbosity.

### Cross-Layer Opposition Geometry (iteration 3)

Compared complement opposition structure across 4 text layers (yaoci, guaci, tuan, daxiang) using BGE-M3 embeddings.

**Verdict: opposition geometry is layer-specific, not demonstrably concept-intrinsic.** Guaci↔tuan are strongly coupled (profile ρ = 0.576, p<.001) — expected given commentary relationship. Tuan↔daxiang show weak coupling (ρ_diff = 0.15, p=.001). All yaoci comparisons are null — but this is a genre artifact (line-averaging vs whole-text embedding), not evidence of different opposition structure.

**Key limitation identified:** Cross-layer comparison is confounded by genre differences between text types. The "concept-intrinsic opposition" hypothesis is neither confirmed nor refuted — it's untestable with current embedding methodology. This is a methodological boundary.

**升↔无妄 is layer-dependent:** Rank 29/32 in guaci (least opposed) but 17/32 in yaoci (median). The R158 anomaly may originate in the judgment layer.

**Guaci complement length asymmetry** is idiosyncratic — uncorrelated with KW ordering (p=1.0) and valence (ρ=0.02). Dominated by 坤↔乾 (Δ=32 characters).

### Position-Resolved Opposition (iteration 4)

Tested whether complement opposition and d=1 differentiation vary by line position, across 4 models.

**Opposition is mostly holistic with mild L1 attenuation (R228).** L1 (initial line) is consistently the least opposed position across all 4 models. Range = ~6.7% of mean. No cross-model consensus on which position is MOST opposed.

**d=1 differentiation is flat across bit positions (R229).** Flipping any of the 6 bits produces statistically indistinguishable thematic shifts. Extends R162's holistic composition finding to the bit-position decomposition.

**Opposition and differentiation are independent (R230).** The positional profile of complement opposition does NOT correlate with the positional profile of d=1 differentiation (ρ ≈ 0). Where texts oppose most is unrelated to where structural changes produce the largest shifts.

**升↔无妄 has pair-specific bimodal opposition at L3/L5 (R231).** Strongly opposed at L3 and L5 (ranks 1-6/32), concordant at L1/L2/L4/L6 (ranks 20-32/32). Rank variance = 2nd of 32 pairs (128.7 vs median 68.8). Cross-model consistent (above 75th percentile in 4/4 models). Other high-variance pairs (泰↔否, 恒↔益, 復↔姤) have different positional signatures — bimodality is pair-specific, not a shared pattern.

### Hamming-Length Independence (iteration 5)

Tested whether text length (R219) mediates the Hamming V-shape (R159). Two-stage design: Stage A tests text-length difference across Hamming distances (no embeddings); Stage B tests partial correlation controlling for text length (4 models).

**Text-length difference is flat across Hamming distance (R232).** Yaoci ρ = −0.007, p = .76. No V-shape. Text length does not track Hamming distance at all.

**R159 is completely independent of text length (R233).** Partial correlation reduces r by < 1% across all 4 models. The Hamming anti-correlation and the text-length opposition axis share zero variance.

**The Hamming V-shape is a residual-space phenomenon (R234).** Raw embeddings show flat distance ratios (1.001:1.002:1.019). Residual embeddings (after removing ~11% algebraic signal) show the V-shape (1.055:0.971:1.183). The algebraic component is positively correlated with Hamming proximity, masking the thematic anti-correlation in raw space.

**Structural implication:** The opposition manifold has at least two independent design principles: (1) text length (~1 dim, vocabulary-accessible, Hamming-independent) and (2) Hamming anti-correlation (~15 dims, vocabulary-inaccessible, residual-space). These don't interact.

## Operational Notes

### Infrastructure
- Python venv: `/home/quasar/nous/.venv/`
- GPU: Quadro P5000, 17GB VRAM. CUDA available.
- `sentence-transformers` 5.2.3, `FlagEmbedding` 1.3.5, `transformers` 5.2.0 installed.
- Phase 1 functions (`load_data`, `build_design_matrix`, `extract_residuals`) are the reusable foundation — import from `phase1_residual_structure.py`
- Cached cross-model embeddings in `Q1/embeddings_{bge-m3,e5-large,labse,sikuroberta}.npz`

### Atlas Structure
- Hex indices 0-63 (binary value). Atlas keys are string versions.
- `kw_number`: 1-indexed King Wen position
- `complement`: hex index of bit-complement
- `reverse`: hex index of reversal (top-to-bottom flip)
- `lower_trigram.element` / `upper_trigram.element`: 五行 elements
- `surface_cell`: [lower_element, upper_element]

### Bit Convention Warning
- Atlas uses **big-endian** trigram bits: trigram string "001" = index 1 in atlas
- dynamics_probe uses **little-endian** (index = value): F_MAP index 1 corresponds to atlas trigram bit-reverse(1)=4
- Mapping: atlas hex bit k (line k+1) = dp trigram bit (2−k%3) within each trigram
- Line 1 (hex bit 0) = dp bit 2 = 生+克; Line 2 (hex bit 1) = dp bit 1 = pure 克; Line 3 (hex bit 2) = dp bit 0 = 比和+生

### KW Pair Structure
- 32 pairs: sort by kw_number, take consecutive pairs
- 4 palindrome (self-reverse, paired with complement): 乾↔坤, 頤↔大過, 坎↔離, 中孚↔小過
- 4 anti-palindrome (reverse=complement): 泰↔否, 隨↔蠱, 漸↔歸妹, 既濟↔未濟
- 24 pure reversal

### Null Model for KW Analysis
- Fix endpoints (pair 0 = 乾坤, pair 31 = 既濟未濟)
- Permute 30 interior pairs
- Anti-clustering: bridge element pairs must differ
- ~27% acceptance rate
- 10K permutations sufficient

### Working Style Observations
- The sage's structural decompositions consistently improved analysis design
- Surprise findings (R159 Hamming anti-correlation) emerged from routine validation — always examine intermediate results
- Cross-model validation should be standard for any embedding-based finding
- The sage correctly identified when investigations reached diminishing returns
- n=32 constraint on complement pairs limits all direction-based analyses — design tests with zero free parameters
- Residual-space artifacts are real — always verify direction findings on raw centroids (Phase 8e lesson)
- The "numerically positive, structurally negative" distinction (T3) is a useful template: cardinality match ≠ structural match
- Q2 Proper showed that enumeration at small parameters can resolve philosophical questions computationally — the |S|=6 solution was not anticipated
- R191 retraction demonstrates: single-model, single-layer findings are fragile. Always cross-validate before building on measurement results
- Authorial confound (tuan > guaci > yaoci pattern) recurs across multiple analyses — treat layer-stratified signals with skepticism
- "Addresses without structures" pattern recurs at multiple levels — the system uses mathematical scaffolding without using the scaffolding's internal dynamics
- The sage correctly predicted 4/5 thread outcomes in iteration 7 — the one surprise (φ in cube-edge partition) came from the computation the sage identified as the strongest test
- When the sage says "this is the only well-posed question," listen — it was also the only one that produced a non-trivial finding
- Sagemegistus's independent assessment identified the complement symmetry of P₄ (analytically resolved as generic) and the Jacobian connection (computationally productive — led to R205)
- The hu_cell bridge hypothesis (Route B ↔ R194) was definitively killed — a useful negative that prevents future false trails
- The sage's confound identification (五行 type entangled with line position) saved the R159 decomposition from a false positive — the uncontrolled comparison showed 比和 > 克 > 生, but the controlled test (Pass 2) was null
- Three-resolution null strategy (R192/R206/R209) is the strongest possible negative within the embedding paradigm — no further Route B → text tests are warranted
- The naive mean displacement is identically zero by symmetry (h→h⊕mask is a bijection) — always check symmetry before computing
- Perturbation rank ~5.4 (not rank 1-2 as predicted) demonstrates: the thematic manifold's non-decomposability extends to the d=1 perturbation geometry. The holistic composition (R162) is confirmed from the directional side
- The within > cross pattern (R211) is weak but consistent — and its layer stratification (tuan strongest) recapitulates R195, suggesting it reflects commentarial practice rather than deep text structure
- The sage's anisotropy analysis for BERT mean-pooling was exactly right: relative comparisons with permutation nulls are robust to uniform compression. Always check embedding quality diagnostics before comparing across architectures
- Genre proximity to target corpus matters more than architecture type for cross-model agreement (LaBSE on Bible translations agrees less than SikuRoBERTa on classical Chinese)
- The R² two-band finding (10.8–11.0% multilingual / 13.2% domain-matched) emerged from what was designed as a replication test — always examine what changes alongside what replicates
- The sage predicted pair-level ρ ≈ 0.55–0.65; actual was 0.74–0.75. The text signal constrains opposition directions more tightly than expected across architectures — the invariant core is larger than anticipated. Predictions that are wrong in the informative direction are still valuable calibration
- R213's three-level gradient (profile > Procrustes > direction) is the cleanest decomposition of "text-intrinsic" from binary to quantitative: ~85% recoverable geometry, ~15% architecture-dependent, with the dependent fraction correlating with training-data cultural salience
- The Fibonacci discriminator (mechanism vs output) resolved most questions analytically before computation — establishing the right test saves computation cycles. The sage's prediction accuracy for the Fibonacci investigation was 4/4.
- Top-down probe testing (test named directions) works at n=32 where bottom-up factor analysis (interpret unnamed PCs) fails. At n ≈ p, PCs are noise eigenvectors; but projecting onto pre-specified directions has 1 free parameter per test.
- The most mechanical probe (text length) produced the strongest finding. Content vocabulary probes were diffusely weak. This suggests the opposition space's vocabulary-accessible component is at the level of discourse structure (verbosity, elaboration) rather than content categories.
- Always check for confounds before recording probe results: negation's univariate significance (p<.05 in 4/4) was entirely mediated by text length in yaoci.
- The yaoci/guaci split on complement text-length asymmetry (p=.32 vs p=.008) connects to the authorial confound: judgments may have been composed with complement awareness, line texts less so.
- Cross-layer comparison within single-model embeddings is confounded by genre differences between text types. Line-averaging (yaoci) produces fundamentally different geometry from whole-text embedding (guaci/tuan/daxiang). Cross-layer ≠ cross-concept.
- "Text-intrinsic" (cross-model within one layer) ≠ "concept-intrinsic" (cross-layer across genres). The previous program conflated these. R225 identifies the boundary.
- Procrustes R² without a task-relevant permutation null is uninterpretable. The random-subspace baseline (k/d) is too loose; the right null permutes the correspondence (hexagram labels) while preserving per-layer geometry.
- The guaci↔tuan coupling (ρ = 0.576) is the textual relationship (commentary on judgment) dressed as a structural finding. Not everything statistically significant is scientifically informative.
- Rank marginals are uniform by construction — proposed "marginal corrections" on rank matrices are mathematically trivial (no-ops). Always verify a correction is non-trivial before implementing.
- The opposition/differentiation independence (R230) is a clean structural result: the hexagram system separates what each position says about opposition from how sensitive the whole hexagram is to perturbation at each position.
- Pair-specific positional signatures (R231: each high-variance pair has its own unique profile) suggest the opposition manifold has pair-level microstructure that is not captured by any position-level or trigram-level decomposition.
- The Spearman ρ shortcut (testing overall correlation before computing bin-by-bin profiles) saved computation: ρ ≈ 0 immediately resolved the mediation question.
- R159 requires residual embeddings — the algebraic ~11% creates positive Hamming-correlated similarity that exactly counteracts the thematic anti-correlation. This raw/residual distinction was invisible in the original measurement but is methodologically critical for interpretation.
- The < 1% partial correlation reduction is the cleanest possible mediation null. When testing whether two findings share a mechanism, partial correlation is definitive if the proposed mediator is measured directly (text length) rather than latent.
- Line-level and centroid-level residualization commute (both linear). R² inflation at centroid level (35% vs 11%) absorbs within-hexagram variance, not cross-hexagram signal. Always check commutativity before assuming granularity changes affect results.
- A null result under distorted residuals is conservative — noisy residuals bias correlations toward zero. R235 is robust precisely because it's null.
- The d=2 > d=1 asymmetry may partly reflect measurement precision: 15 neighbors (d=2) vs 6 (d=1) gives lower-variance per-hexagram estimates. The magnitude comparison isn't apples-to-apples.
- Reversal's p ≈ 0.1 is a hard ceiling: n=24 with effect size ~0.05 would need ~100 pairs for 80% power. The I Ching has exactly 24.
- The distributed signature (no component significant, aggregate significant) in R236 is the same non-decomposability seen at every resolution. The manifold's resistance to factoring is its defining characteristic.
