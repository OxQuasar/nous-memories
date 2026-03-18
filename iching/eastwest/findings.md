# East/West: Complete Findings

> 12 iterations investigating whether the golden ratio (φ) and 五行 dual cycles share a deep connection.
> 34 results (R181–R214, one retracted).

---

## Overall Synthesis

The I Ching carries φ. Not incidentally, not just through the cyclotomic field — it's wired into the destruction cycle's geometry on the binary cube.

Two independent routes produce φ at (3,5). Route A is cyclotomic (top-down, generic to all 240 surjections). Route B is combinatorial (bottom-up, specific to 96/240 surjections including the I Ching's). The two routes converge uniquely at n=3 via the identity 2^{n−1}+1 = 2ⁿ−3, which has exactly one solution. The I Ching sits at the unique point where both routes produce φ simultaneously.

The structural parameters are four consecutive Fibonacci numbers: 2, 3, 5, 8 = F(3)–F(6). Each is derived independently through the forcing chain, but the numerical output satisfies the Fibonacci recurrence: 2+3=5, 3+5=8, 5+8=13. The next Fibonacci number F(7)=13 is precisely where rigidity breaks (960 orbits). φ = lim F(n+1)/F(n) is both the limit of the sequence that generates the parameters and an eigenvalue inside the structure itself.

Three layers of structure:

**The algebra** carries φ through the 克 cycle. The 6 克 edges on the trigram cube form two P₄ paths with eigenvalues {φ, 1/φ, −1/φ, −φ}. The 生 cycle does not carry φ (4 edges, P₃, no golden ratio eigenvalue). Destruction is geometrically richer than generation.

**The texts** do not see the dynamics. The 五行 relational labels (生/克/比和) carry no semantic information (R192). The 11% algebraic variance is static (grouping), not dynamic (relating). The texts use the partition without the cycles. The bridge between φ and textual meaning has not been found.

**The cross-cultural picture** is precise. The Greek system (n=2, F₂²) is structurally locked out of dual-cycle dynamics — Z₃ has only one Hamiltonian cycle. The pentagram is the 克 Cayley graph Cay(Z₅,{±2}), with edge ratio φ. The Greeks studied its spectral structure (geometry, proportions). The Chinese studied its adjacency structure (生/克 dynamics). Same graph, different readings, neither tradition computed both.

**What remains open:** The connection between φ, the I Ching, and natural systems may be at the level of *process* rather than *classification*. The T3 test asked "does nature have five phases?" (No.) The unasked question: "do the I Ching and nature share the same deep structure — self-referential sequential change — with φ as its signature?" The Fibonacci recurrence (next = current + previous) describes both natural growth and the I Ching's forcing chain. φ is the eigenvalue of both. Whether this is coincidence at small numbers or a structural identity is the open thread. See `fibo/questions.md`.

---

## Detailed Findings

---

### The Dimension Threshold (R181–R182)

Binary encoding + dual cycles requires dimension n ≥ 3.

| n | Max viable p | Rigid point | Dual cycles? | Tradition |
|---|-------------|-------------|--------------|-----------|
| 2 | p ≤ 3 | (2,3) | ✗ — stride-2 ≡ stride-(−1) on Z₃ | Greek (hot/cold × wet/dry) |
| 3 | p ≤ 7 | (3,5) | ✓ — stride-1 ≠ stride-2 on Z₅ | Chinese (trigrams → 五行) |

The Greek quaternary system (F₂², 4 elements from 2 binary qualities) structurally prevents dual-cycle dynamics: the only odd prime p ≤ 3 has a single Hamiltonian cycle. To get two independent cycles, you need p ≥ 5, which requires 2^{n-1} ≥ 3, so n ≥ 3.

**Limitation:** This proves that n=2 forecloses dual cycles *given binary encoding*. Five-element systems without binary substrate are mathematically possible (and existed historically). The theorem constrains the conjunction: binary encoding + complement equivariance + dual cycles → n ≥ 3.

---

### The Cyclotomic Structure (R183–R187)

### Universal Trace Formula (R183)

For the E=1 family (n, p = 2ⁿ−3), the Galois trace sum ΣTr of the character-lifted surjection distinguishes partition types:

| Partition type | ΣTr | Proof |
|---------------|-----|-------|
| Shape B (degenerate, m₀ = 2) | **3** (universal, rational) | Root-of-unity sum identity |
| Shape A (three-type coexistence, class j doubled) | **1 + 2cos(2πj/p)** (irrational) | One trace counted twice |

### Golden Ratio Tags Shape A (R184)

At p = 5: Shape A trace sums are {φ, ψ} — the golden ratio and its conjugate. Shape B gives 3. Under Aut(Z₅), φ ↔ ψ, so the distinction is between irrational (Shape A) and rational (Shape B). At p = 13: Shape A gives six algebraic numbers in Q(cos(2π/13)), degree 6. The partition discrimination generalizes; the φ-structure is p=5-specific.

### Walsh Spectra (R185)

All |W|² values at (3,5) lie in Q(√5). At (3,3): rational. At (3,7): Q(cos 2π/7). The golden ratio's appearance tracks the cyclotomic field, not the rigidity.

### Complement ↔ Galois Conjugation (R186)

Complement equivariance f(x⊕1ⁿ) = −f(x) becomes, under the character lift χ∘f, the Galois automorphism σ: ζ₅ → ζ₅⁴. This is generic to ALL complement-equivariant maps to Z_p — it holds by definition of the character, not by any special property of the I Ching's surjection.

### Pentagon = 生, Pentagram = 克 (R187)

The regular pentagon is the Cayley graph Cay(Z₅, {±1}) — the 生 (generation) cycle. The regular pentagram is Cay(Z₅, {±2}) — the 克 (destruction) cycle. Edge ratio pentagram/pentagon = 2cos(π/5) = φ. Both have adjacency spectrum {2, 1/φ, 1/φ, −φ, −φ} (isospectral, graph-isomorphic via α: k→2k).

The Cayley graph framing is presentation, not content — the identification Cayley eigenvalues = Galois traces = 2cos(2πk/p) is definitional at every step. But it provides the cleanest formulation of Q2: the Greeks studied the pentagram's *spectral structure* (edge ratios, geometric proportions, φ). The Chinese studied Z₅'s *adjacency structure* (生/克 as relational dynamics). Same graph, different readings. Neither tradition computed both.

---

### Textual Findings (R189–R196)

### King Wen Ordering: Semantic, Not Algebraic (R189–R190)

The KW sequence carries structure in text-semantic space but NOT in binary or algebraic space:

| Dimension | Inter-pair signal | Evidence |
|-----------|------------------|----------|
| Binary (Hamming distance) | None | 32.6th percentile vs null |
| Five-phase torus | None | 61.4th percentile vs null |
| Text embeddings (tuan) | **Strong** | 99.7th percentile |
| Text embeddings (guaci) | Moderate | 92.0th percentile |

Layer gradient (tuan > guaci > yaoci > daxiang) correlates with discursive freedom, not traditional dating. Authorial confound is not separable: later commentators may have amplified intrinsic thematic structure.

### Texts Use the Partition, Not the Dynamics (R192)

The five-phase relation labels (生/克/比和) carry no semantic information in either text layer. The surjection f: F₂³ → Z₅ groups hexagrams into torus cells; the relational dynamics that define Z₅ as a cycle algebra are invisible in textual similarity.

This sharpens the 89/11 split (R157): the ~11% algebraic variance is *static* (grouping, labeling) not *dynamic* (relating, transforming). The feature that makes 五行 mathematically special — the dual Hamiltonian cycles, the unique rigidity — is exactly the feature absent from the texts.

### No Universal Differentiation Principle (R196)

Systematic test of 12+ structural groupings across two text layers: only 2 of 24 grouping×layer combinations show anti-signal (surface_cell and surface_relation in guaci only). The claim that "texts differentiate where structure groups" is local, not general. R191 (surface cell anti-signal) retracted after failing cross-model replication.

### hu_cell: Unresolved (R194)

The nuclear hexagram's element cell (互卦) predicts semantic similarity in guaci (99.4%ile) and tuan (99.5%ile) — the only cross-layer consistent algebraic predictor. Direction positive in 5/5 models (82–99th percentile), but yaoci-aggregated tests are underpowered due to variance compression. Stays Tier 2 pending hex-level cross-model validation (low priority given small effect size Δ = 0.008–0.015).

---

### φ in Dynamics (R197–R209)

### Two Routes to φ

**Route A (cyclotomic, unconditional):** Q(ζ₅)⁺ = Q(√5) forces Walsh spectra and Galois traces into Q(φ). Top-down — holds for all 240 complement-equivariant surjections.

**Route B (combinatorial, conditional):** The 克 edges of the 3-cube form P₄ ∪ P₄, with eigenvalues 2cos(kπ/5) = {φ, 1/φ, −1/φ, −φ}. Bottom-up — holds for 96/240 surjections (determined by Jacobian type R205). The I Ching's surjection is in this 2/5 subset.

**Convergence identity:** 2^{n-1}+1 = 2^n−3 = p has the unique solution n=3. At (4,13) the path denominator is 9 ≠ 13 and φ disappears (R207).

### Orbit Characterization (R204–R208)

96/240 surjections have φ in one cycle type: 48 in 克, 48 in 生. Perfect mirror symmetry. φ ↔ Jacobian multiset {{比和,生},{克},{生,克}} with a pure direction at a standard basis vector (necessary and sufficient). 8 distinct structure triples exist. Nuclear map × Jacobian: no coupling.

### No Bridge to Text (R192, R206, R209)

| Resolution | Test | Result |
|---|---|---|
| Torus cell (R192) | 生/克/比和 semantic information | Null |
| Nuclear hex (R206) | hu_cell × Jacobian coupling | p = 0.996 |
| Cube edge (R209) | 克 vs 生 d=1 transitions, controlled for line position | p > 0.2, inconsistent sign |

Route B is algebraically real and has no detectable textual correlate at any resolution tested.

---

### Perturbation Directions (R210–R211)

Single-line perturbation directions are hexagram-specific (rank ~5.4/6, no dominant axis). Within-pair cosines (same bit position, different trigram) consistently exceed cross-pair (5/5 sources), layer-stratified: tuan (+0.27) > guaci (+0.12) > yaoci (+0.03–0.06). The algebraically special bit (bit 1, pure 克) shows the strongest tuan alignment (+0.32) but is textually most opaque in the primary layer (guaci −0.01).

---

### Cross-Architecture Replication (R212–R213)

### Aggregate Replication (R212)

All Tier 1b findings replicate on SikuRoBERTa, a classical-Chinese BERT model architecturally distinct from the three prior multilingual sentence-transformers (different training data, objective, architecture, embedding method).

| Finding | SikuRoBERTa | Prior (3 models) | Replicated? |
|---------|-------------|-------------------|-------------|
| R156: complement mean cosine | −0.162 (p=0.0001, 27/32) | ≈ −0.19 (28–29/32) | ✓ |
| R157: algebraic R² | 13.2% | 10.8–11.0% | ✓ (elevated) |
| R159: Hamming V-shape | d=1 (1.055) > d=2 (1.040) > d=3 (0.991) | V-shape confirmed | ✓ |

### Two-Band R² Structure

The tight 10.8–11.0% across multilingual models measures "algebraic variance accessible through multilingual embeddings." SikuRoBERTa's 13.2% measures "algebraic variance accessible through classical-Chinese-native embeddings." Both bands are findings: the multilingual invariance, and the domain-sensitivity elevation.

### Pair-Level Concordance (R213)

The complement opposition decomposes into two components:

| Level | Metric | SikuRoBERTa range | Prior range |
|-------|--------|-------------------|-------------|
| Which pairs oppose? | Profile ρ (32-element) | 0.80–0.83 | 0.82–0.96 |
| How much geometry aligns? | Procrustes R² (k=20) | 0.83–0.86 | 0.85–0.95 |
| Which directions? | Direction ρ (32×32) | 0.74–0.75 | 0.76–0.88 |

**Model-invariant core:** The pair ranking (which pairs oppose most/least) is text-intrinsic (profile ρ = 0.80–0.83 across architectures).

**Architecture-sensitive periphery:** The fine-grained angular directions are ~85% recoverable via Procrustes alignment, with ~15% architecture-dependent. The ~16 opposition dimensions decompose into ~13-14 cross-architecture invariant dimensions plus ~2-3 architecture-dependent dimensions.

Largest discrepancies (Kan↔Li showing stronger opposition in SikuRoBERTa, Jian↔Kui showing weaker) correlate with cultural salience in training corpora — a training-data confound, not a text property.

### Cross-Model ρ Clusters by Genre, Not Architecture

| Pair | ρ (full matrix) |
|------|---|
| bge-m3 ↔ e5-large | 0.868 |
| bge-m3 ↔ sikuroberta | 0.679 |
| e5-large ↔ sikuroberta | 0.703 |
| bge-m3 ↔ labse | 0.633 |
| e5-large ↔ labse | 0.535 |
| labse ↔ sikuroberta | 0.461 |

Genre proximity to the target corpus matters more than training objective for structural agreement.

---

## Complete Result Table

| # | Finding | Tier |
|---|---------|------|
| R181 | (2,3) is the unique viable point at n=2; Z₃ supports only 1 Hamiltonian cycle → no dual dynamics | Theorem |
| R182 | n=3 is necessary and sufficient for the minimum dual-cycle system (given binary encoding) | Theorem |
| R183 | Shape A trace sum = 1+2cos(2πj/p); Shape B trace sum = 3. Universal for E=1 family | Theorem |
| R184 | At (3,5): Shape A trace sum ∈ {φ,ψ}, tagging three-type coexistence with golden-ratio arithmetic. p=5-specific | Theorem |
| R185 | |W|² ∈ Q(√5) at p=5, Q at p=3, Q(cos 2π/7) at p=7. φ-connection tracks cyclotomic field, not rigidity | Theorem |
| R186 | Complement equivariance ↔ Galois conjugation on Q(ζ₅): generic to all equivariant Z_p maps | Theorem |
| R187 | Pentagon = Cay(Z₅,{±1}) = 生; Pentagram = Cay(Z₅,{±2}) = 克; edge ratio = φ = 2cos(π/5) | Theorem |
| R188 | Q5 closed: Q(ζ₅) is shared address of φ and dual cycles, not shared cause. "Address with conditional resonance" | Interpretation |
| R189 | KW semantic smoothness is layer-stratified: tuan (99.7%) > guaci (92%) > yaoci (80%) > daxiang (76%). Binary and torus show no inter-pair signal | Measurement |
| R190 | Layer gradient correlates with discursive freedom, not traditional dating. Authorial confound not separable | Measurement |
| R191 | ~~Surface cell anti-signal~~ **RETRACTED** — does not replicate across models or layers | — |
| R192 | Five-phase relation labels (生/克/比和) carry no semantic information in either text layer | Measurement |
| R193 | Torus cell-pair identity captures real tuan variance (99%ile, ~10.5% uplift) but not through distance or relation type | Measurement |
| R194 | hu_cell predicts semantic similarity in guaci (99.4%) and tuan (99.5%); direction positive 5/5 models, yaoci inconclusive. Tier 2 | Measurement |
| R195 | Trigram identity predicts tuan (99.9%ile) but not guaci — layer-dependent, commentarial practice | Measurement |
| R196 | Systematic differentiation test: 2/24 anti-signal. No universal differentiation principle | Measurement |
| R197 | Full pullback (f-lifted Cayley graphs on F₂³): φ NOT detected. 生/克 pullbacks non-isomorphic (12 vs 13 edges) | Theorem |
| R198 | Cube-edge partition: A_克 spectrum = {±φ, ±φ, ±1/φ, ±1/φ}. 克 subgraph = P₄ ∪ P₄; φ via 2cos(kπ/5) | Theorem |
| R199 | Path-length progression: 比和→P₂, 生→P₃, 克→P₄. Only 克 produces φ | Theorem |
| R200 | The n=3 identity: 2^{n-1}+1 = 2ⁿ−3 = p uniquely at n=3. Two routes to φ converge only at (3,5) | Theorem |
| R201 | Transition balance: 比和:生:克 = 1:2:3 across all 384 line transitions. Bit-stratified | Theorem |
| R202 | E=1 family fiber ratio: 3/(p−3) → 0. Not Fibonacci-related | Theorem |
| R203 | Basin structure trivial: F₂-linear, determined by bits 2,3 | Theorem |
| R204 | 96/240 surjections (2/5) have φ in one cycle type. 48 克 + 48 生, mutual exclusion | Theorem |
| R205 | φ ↔ Jacobian multiset {{比和,生},{克},{生,克}} with pure direction. Necessary and sufficient | Theorem |
| R206 | Nuclear map × Jacobian: no coupling. hu_cell bridge dead (p=0.996) | Measurement |
| R207 | (4,13): 克 = P₂⁴ + 8I. φ absent — fibers too thin | Theorem |
| R208 | 8 structure triples at (3,5), perfect 生↔克 mirror. 比和 = P₂+P₂+4I or 8I | Theorem |
| R209 | d=1 anti-correlation not structured by 五行 edge type. Controlled test p > 0.2, inconsistent sign | Measurement |
| R210 | Perturbation directions hexagram-specific. Rank ~5.4/6, σ₁/σ₂ ≈ 1.15. 0/30 significance | Measurement |
| R211 | Within-pair > cross-pair perturbation cosines (5/5 sources). Layer-stratified: tuan > guaci > yaoci | Measurement |
| R212 | Cross-architecture replication: R156/R157/R159 replicate on SikuRoBERTa. Four-model consensus confirms "text-intrinsic." R² two-band: 10.8–11.0% (multilingual) / 13.2% (domain-matched) | Tier 1b |
| R213 | Pair-level concordance: complement opposition = model-invariant core (profile ρ 0.80–0.83) + architecture-sensitive periphery (direction ρ 0.74–0.75). ~85% geometry recoverable (Procrustes R² 0.83–0.86 at k=20). ~13-14 invariant + ~2-3 architecture-dependent dimensions | Tier 1b (ranking) / Tier 2 (angular) |

---

## Epistemic Tiers

**Tier 1 (theorems):** R181–R187, R197–R205, R207–R208. Provable from definitions and arithmetic.

**Tier 1b (text-intrinsic, cross-model validated):** R156–R159, R161–R163, R167–R170, R212, R213 (pair ranking component). Validated across 4 architecturally distinct models (BGE-M3, E5-large, LaBSE, SikuRoBERTa). Remaining vulnerability: all are transformer-based neural networks. R213 quantifies: ~85% of opposition geometry is cross-architecture invariant; ~15% is architecture-dependent (correlates with training-data cultural salience).

**Tier 2 (measurements):** R189, R190, R192–R196, R206, R209–R211, R213 (angular structure component). Method-dependent.

**Tier 3 (interpretations):** R188, R214-Q4b. Best reading of evidence, revisable.

**Retracted:** R191.

---

## Scripts

| Script | Computations |
|--------|-------------|
| `cyclotomic_probe.py` | Rigidity landscape, Walsh spectra, character lift, trace formula, Cayley graphs |
| `kw_sequence_probe.py` | KW Hamming distance, torus trajectory, text embedding trajectory |
| `torus_coherence.py` | Within-cell similarity, five-phase relations, torus distance, variance decomposition |
| `differentiation_principle.py` | Systematic grouping test across 12+ structural features |
| `hu_cell_validation.py` | Cross-model validation of hu_cell |
| `dynamics_probe.py` | Pullback spectra, cube-edge partition, orbit taxonomy, Jacobian, (4,13) geometry |
| `edge_type_decomposition.py` | R159 decomposition by 五行 edge type, cross-model |
| `perturbation_directions.py` | SVD rank, cosine similarity, within-pair analysis |
| `sikuroberta_replication.py` | Cross-architecture replication of R156/R157/R159 |
| `pair_concordance.py` | Pair-level direction concordance, Procrustes alignment, profile concordance |
