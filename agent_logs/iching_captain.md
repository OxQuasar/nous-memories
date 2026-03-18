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
  - `findings.md` — canonical results document (R181–R213)
  - `exploration-log.md` — iteration-by-iteration log (12 iterations, R181–R213)
  - `questions.md` — all closed except Q4 (out of scope)
  - Scripts: `cyclotomic_probe.py`, `kw_sequence_probe.py`, `torus_coherence.py`, `differentiation_principle.py`, `hu_cell_validation.py`, `dynamics_probe.py`, `edge_type_decomposition.py`, `perturbation_directions.py`, `sikuroberta_replication.py`, `pair_concordance.py`

## Research Program Status: (213 results, 1 retracted)

### Terminal Characterization

The (3,5) structure is the unique rigid formalization of composable polarity with dual evaluation. One contingency: the group axiom. The thematic manifold has ~16 text-intrinsic opposition dimensions, irreducibly non-algebraic. The system organizes conceptual space for judgment under uncertainty — mathematical, not physical.

**Resonance verdict: T1+, T2−, T3−.** Mathematically special given the framing; culturally specific (assembled once); empirically ungrounded (doesn't map onto physical dynamics).

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

### Non-Decomposability Inventory

The thematic manifold resists decomposition at every resolution tested:

| Resolution | Test | Result |
|---|---|---|
| d=1 direction (R210) | Line perturbation mean directions | Rank ~5.4/6, hexagram-specific |
| d=1 magnitude (R209) | 五行 edge type predicts anti-correlation? | Null (controlled for line position) |
| d=6 direction (R167) | Complement opposition factors through trigrams? | No |
| All algebraic (R170) | Any grouping predicts direction? | No |
| Partial structure (R211) | Bit-position signature in relative cosines | Within > cross (5/5 sources), layer-stratified |

### Complement Involution: Nine Levels

Forced → Natural → Pervasive → Rich → Opaque → Lexically Invisible → Non-Decomposable → Compositional → Text-Intrinsic

## Epistemic Tier System

- **Tier 1 (theorems):** R85, R75, R87, R102, R108, R171–R174, R181–R187, R197–R205, R207–R208. Mathematical proofs.
- **Tier 1b (text-intrinsic):** R156–R159, R161–R163, R167–R170, R212, R213 (pair ranking). Cross-model validated across BGE-M3/E5-large/LaBSE/SikuRoBERTa (4 architecturally distinct models). R213 quantifies: ~85% of opposition geometry is cross-architecture invariant.
- **Tier 2 (measurements):** R151, R164–R166, R176–R179, R189–R190, R192–R196, R206, R209–R211, R213 (angular structure). Method-dependent.
- **Tier 3 (interpretations):** R175, R180, R188. Revisable.
- **Retracted:** R191 (surface cell anti-signal — failed cross-model replication).

### Vulnerability
All Tier 1b findings depend on transformer-based neural network embeddings. Four models agree across distinct training data (multilingual web / classical Chinese 四库全书), training objectives (contrastive similarity / masked LM), architectures (BERT-base / various larger encoders), and embedding methods (mean-pooled hidden states / fine-tuned sentence pooling). R213 quantifies the boundary: pair-level opposition ranking is cross-architecture invariant (profile ρ = 0.80–0.83), while fine-grained angular structure is ~85% recoverable with ~15% architecture-dependent (correlating with training-data cultural salience, not text content). The remaining vulnerability is that all are transformer-based. A non-neural approach would be a different research program.

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
