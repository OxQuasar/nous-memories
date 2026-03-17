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

## Research Program Status: (180 results)

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

### Complement Involution: Nine Levels

Forced → Natural → Pervasive → Rich → Opaque → Lexically Invisible → Non-Decomposable → Compositional → Text-Intrinsic

## Epistemic Tier System

- **Tier 1 (theorems):** R85, R75, R87, R102, R108, R171–R174. Mathematical proofs.
- **Tier 1b (text-intrinsic):** R156–R159, R161–R163, R167–R170. Cross-model validated across BGE-M3/E5-large/LaBSE.
- **Tier 2 (measurements):** R151, R164–R166, R176–R179. Method-dependent.
- **Tier 3 (interpretations):** R175, R180. Revisable.

### Vulnerability
All Tier 1b findings depend on transformer-based multilingual embeddings. Three models agree, but they share architectural assumptions. A radically different embedding approach (classical-Chinese-only, non-neural) could produce different results. Noted, not fixable within current paradigm.

### 80/20 vs 89/11
The "80/20" language comes from the judgment tradition's self-description. Empirical split is 89/11 — algebra explains 10.8–11.0% (model-invariant). The tradition overestimates its own algorithmic coverage.

## Operational Notes

### Infrastructure
- Python venv: `/home/quasar/nous/.venv/`
- GPU: Quadro P5000, 17GB VRAM. CUDA available.
- `sentence-transformers` 5.2.3, `FlagEmbedding` 1.3.5 installed.
- Phase 1 functions (`load_data`, `build_design_matrix`, `extract_residuals`) are the reusable foundation — import from `phase1_residual_structure.py`
- Cached cross-model embeddings in `Q1/embeddings_{bge-m3,e5-large,labse}.npz`

### Atlas Structure
- Hex indices 0-63 (binary value). Atlas keys are string versions.
- `kw_number`: 1-indexed King Wen position
- `complement`: hex index of bit-complement
- `reverse`: hex index of reversal (top-to-bottom flip)
- `lower_trigram.element` / `upper_trigram.element`: 五行 elements
- `surface_cell`: [lower_element, upper_element]

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
