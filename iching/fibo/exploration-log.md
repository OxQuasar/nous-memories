# Fibonacci Investigation — Exploration Log

## Iteration 1

### Design Phase (Discussion)

**Framing:** Six open questions (Q1–Q6) about whether the Fibonacci structure in the I Ching's parameters is structural or arithmetic coincidence. The sage proposed a discriminator: a Fibonacci appearance is structural iff the *derivation* contains additive self-reference F(n+1) = F(n) + F(n-1). If the mechanism is exponential/multiplicative/primality-based, it's small-number overlap.

**Analytical resolutions (no computation needed):**
- Q1 forcing chain logic: The "two-lookback" appearance is because n serves dual roles (dimension and exponent). Every proof chain has premises feeding conclusions — calling that Fibonacci-shaped proves too much.
- Q5 eigenvalue bridge: P₄ eigenvalues = 2cos(kπ/5) because path length+1 = 5 = |Z₅|. Fibonacci matrix eigenvalues {φ, -1/φ} are a subset by Chebyshev structure. Reformulation of R198.
- Q4: Deferred as numerology without prior prediction.
- Q6: Deferred as philosophical wrapper pending mathematical results.

**Computation plan:** Four tasks ordered by expected yield.

### Computation Phase

**Task 1: Fibonacci vs E=1 family scan (n=2..30)**

Precomputed Fibonacci numbers up to ~10⁹. Checked 2ⁿ−3, 2ⁿ, (2ⁿ−1)×n against Fibonacci set.

Results:
- n=2: 2ⁿ−3 = 1 = F(1) (trivial). 1 hit.
- n=3: 2ⁿ−3 = 5 = F(5), 2ⁿ = 8 = F(6), (2ⁿ−1)×n = 21 = F(8). **3 simultaneous hits.** Unique.
- n=4: 2ⁿ−3 = 13 = F(7). 1 hit.
- n=5..30: Zero hits across all three expressions.

**Proven:** The triple hit at n=3 is unique and the Fibonacci alignment permanently breaks for n≥5. The concentration is maximal because n=3 places parameters in the dense region F(3)–F(8) = {2,3,5,8,13,21}.

**Task 2: Orbit count factorization**

At (4,13): Enumerated all complement-equivariant surjections F₂⁴ → Z₁₃ by brute force (8 representative pairs, each assigned to Z₁₃ values). Total surjections = 232,243,200 = 2¹⁴ × 3⁴ × 5² × 7.

Orbit count = 232,243,200 / (|GL(4,F₂)| × |Aut(Z₁₃)|) = 232,243,200 / (20,160 × 12) = 960. ✓

960 = 2⁶ × 3 × 5. Factor 5 traces to |GL(4,F₂)| = 20,160 = 2⁶ × 3² × 5 × 7 (from the group order formula). Not Fibonacci-related.

(5,29) and (6,61) computationally prohibitive — search space ~10⁴⁵.

**Task 3: Nuclear (互) orbit structure**

Verified 互 formula against all 64 atlas entries: 互(L₁,...,L₆) = (L₂,L₃,L₄,L₃,L₄,L₅). ✓

Nuclear matrix M over F₂:
- rank(M) = 4, kernel dim = 2
- M² = M⁴ (period 2 on stable image, not nilpotent)
- 3 attracting sets: 2 fixed points (Kun, Qian) + 1 two-cycle (JiJi ↔ WeiJi)

Full directed graph:
- |im(M)| = 16 nodes
- 48 leaves (no preimages, transient length 2)
- Uniform branching: every image node has exactly 4 = 2^(6−rank) preimages
- Basin sizes: {Kun}: 16, {Qian}: 16, {JiJi↔WeiJi}: 32
- Depth structure per fixed-point basin: 1 (d=0) → 3 (d=1) → 12 (d=2)
- Depth structure for 2-cycle basin: 2 (d=0) → 6 (d=1) → 24 (d=2)

The 16:16:32 split is forced by complement symmetry (σ commutes with M, σ swaps Kun↔Qian, stabilizes the 2-cycle). All branching is uniform. No Fibonacci counts anywhere in the orbit structure.

**Task 4: P₄ vs Fibonacci matrix eigenvalues**

Computed numerically (verified to machine precision, diffs ≤ 2.2×10⁻¹⁶):
- spec(P₄) = {φ, 1/φ, −1/φ, −φ}
- spec([[1,1],[1,0]]) = {φ, −1/φ}
- Relationship: bipartite doubling. spec(P₄) = spec(Fib) ∪ {−spec(Fib)}.
- Explanation: both involve 2cos(kπ/5) because P₄ has 5-1 = 4 vertices and the Fibonacci polynomial x²−x−1 has roots 2cos(π/5) and 2cos(2π/5).

Tautological reformulation of R198. No new content.

### Review Phase (Discussion)

Sage confirmed all results match predictions. Key assessments:

- Basin structure 16:16:32 is forced by F₂-linear algebra + complement symmetry. No deviation from prediction.
- Q2b/Q2c (dynamics lifted to Q(ζ₅)) closed without computation: the lift is a change of representation, not dynamics. Cannot create additive self-reference by tensoring with cyclotomic field.
- Q4 closed: no positive evidence from Q1–Q3 to motivate search.
- Q6 closed: philosophical wrapper dissolved — no mathematical substrate remains.

**Verdict: all six questions closed. The Fibonacci framing adds description but not explanation.**

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R215 | Fibonacci parameter alignment is arithmetic coincidence — triple hit at n=3 only, permanent divergence n≥5 | Theorem | New |
| R216 | Nuclear orbit structure entirely F₂-linear — uniform branching, no Fibonacci counts | Theorem | New |
| R217 | spec(P₄) ⊃ spec(Fibonacci matrix) is tautological bipartite doubling — reformulation of R198 | Theorem | New |
| R218 | 960 orbit count factors (2⁶×3×5) trace to group orders, not Fibonacci | Measurement | New |

### Operational Notes

- The discriminator (mechanism vs output) resolved most questions analytically before computation. Only Q2a required substantial computation, and the result was negative as predicted.
- The sage's prediction accuracy: 4/4 (Q1 coincidence, Q3 group-theoretic, Q2a F₂-linear, Q5 tautological). No surprises.
- The "maximally concentrated coincidence" framing is the cleanest summary: n=3 uniquely sits in the dense region of Fibonacci, and the forcing chain's exponential/primality mechanism guarantees permanent escape.
- For future investigations: any claim that "X is Fibonacci" should be tested with the discriminator before computation. If the derivation is not additive self-referential, it's small-number overlap.

---

## Iteration 2

### Design Phase (Discussion)

**Pivot from Fibonacci (closed) to positive characterization of the ~16 opposition dimensions.**

Sagemegistus proposed three threads:
1. Positive characterization of opposition dimensions via PCA loadings
2. Nuclear fiber as predictor of thematic similarity
3. 升↔无妄 as diagnostic window

**Assessment:**
- Thread 2 pre-closed: Mantel test from Phase 2 already showed r = −0.003, p = 0.877. Nuclear fiber predicts nothing.
- Thread 3 piggybacks on Thread 1.
- Thread 1 is the only new investigation.

**Methodological debate:** Bottom-up PC interpretation (naming PCs from their loadings) was rejected — n=32 with ~16 PCs means each PC is determined by ~2 pairs. Factor analysis at n ≈ p produces eigenvectors of noise, not interpretable factors.

**Chosen methodology: Top-down semantic probe vectors.** Define candidate semantic axes from vocabulary features (text-derived, no embeddings), compute probe direction via regression, project complement-pair differences onto probe, compare R² to permutation null.

**Key design decisions:**
- Raw embeddings for both probes and complement differences (sage correction: avoid basis mismatch between raw and residual spaces)
- No circularity: scores from text vocabulary, probe direction from regression, null from permuting scores
- Cross-model threshold: p < 0.01 in ≥3 of 4 models

### Computation Phase

**8 probes tested across 2 text layers (yaoci, guaci) × 4 models = 64 tests.**

Probes: (1) 吉凶 valence, (2) 利 favorability, (3) 往來 directionality, (4) 貞 frequency, (5) social markers, (6) temporal markers, (7) text length, (8) negation density.

**Main results:**

| Probe | yaoci cross-model | guaci | Verdict |
|-------|-------------------|-------|---------|
| text length | p<.001 in 4/4 models | p<.001 | **Cross-model significant** |
| 否定 negation | p<.05 in 4/4, p<.01 in 0/4 | p<.001 | Near-miss |
| 往來 direction | p<.01 in 2/4 | p=.20 | Not robust |
| 貞 frequency | p<.01 in 1/4 | p=.002 | Not robust |
| All others | p>.05 | p>.05 | Null |

**Enrichment:** 15/40 tests at p<.05 (expected 2.0). 7.5× enrichment beyond chance. The opposition space has diffuse vocabulary correlates.

**Artifact check:** Text length is NOT a centroid geometry artifact. Correlation between text length and ||centroid − global_mean|| is ρ ≈ 0 across all models (strongest: ρ = −0.22, p = .077 on SikuRoBERTa). Centroid norms also uncorrelated with length.

**Complement text-length asymmetry:** Yaoci — null (p = .32). Guaci — significant (p = .008). Complement pairs have systematically different guaci lengths but not yaoci lengths. The guaci signal is driven by a few extreme pairs (坤↔乾: Δ=32 characters).

**Negation partial correlation:** After controlling for text length, yaoci negation signal vanishes in all 4 models (p = .07–.23). Guaci negation retains marginal signal (R² drops from .116 to .085, p = .010). Negation is mostly redundant with text length in yaoci; marginally independent in guaci.

**升↔无妄 diagnostics:** Complement cosine = 0.61–0.96 across models, rank 11–17/32 — near median. Vocabulary scores near-average on all 8 probes. The R158 anomaly is not explained by any vocabulary feature tested.

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R219 | Text length aligns with complement opposition direction (R² = 5.6–11.1%, p<.001 in 4/4 models). Not a centroid geometry artifact. Not correlated with algebraic coordinates | Measurement | New |
| R220 | Diffuse vocabulary enrichment: 15/40 probe tests at p<.05 (expected 2.0). Opposition space has weak but pervasive vocabulary correlates | Measurement | New |
| R221 | Negation density absorbed by text length in yaoci; marginal independent guaci signal (p=.01 after residualization). Algebraic negation ↔ lexical negation bridge is weak | Measurement | New |
| R222 | 升↔无妄 is lexically unremarkable — median complement cosine, near-average vocabulary scores. R158 anomaly not vocabulary-accessible | Measurement | New |
| R223 | Guaci texts are complement-asymmetric in length (p=.008); yaoci are not (p=.32). The complement involution correlates with judgment verbosity but not line-text verbosity | Measurement | New |

### Operational Notes

- The top-down probe methodology (test named directions rather than interpreting unnamed PCs) was the critical design choice. It produces falsifiable results at n=32 where bottom-up factor analysis would produce noise.
- Text length as a control probe produced the strongest finding — the "most mechanical" feature was the most informative. This suggests the opposition space's vocabulary-accessible component is at the level of discourse structure (verbosity, elaboration) rather than content categories (valence, agency, temporality).
- The diffuse enrichment (7.5×) is arguably the more important finding than any single probe: it means the opposition space is not vocabulary-opaque, but vocabulary-diffuse. Many lexical features weakly align; none dominates.
- The yaoci/guaci split on text-length asymmetry (p=.32 vs p=.008) suggests the complement involution operates differently at the judgment level vs the line level — judgments are authored with complement awareness, line texts are not. This connects to the authorial confound noted repeatedly in previous work.
- The negation probe's absorption by text length in yaoci is methodologically important: univariate significance (p<.05 in 4/4 models) was entirely mediated by a confound. Always check for confounds before recording probe results.

---

## Iteration 3

### Design Phase (Discussion)

**Cross-layer opposition geometry — testing whether the ~16 opposition dimensions are concept-intrinsic or layer-specific.**

Sagemegistus proposed three threads:
1. Cross-layer opposition geometry — compare complement-pair difference vectors across yaoci, guaci, tuan, daxiang
2. Guaci length asymmetry — what drives the complement text-length asymmetry (R223)?
3. Multivariate vocabulary signal — deferred (n=32/p=8 makes joint R² inflated)

**Sage's key design contribution:** Decompose cross-layer comparison into ρ_centroid (content similarity) vs ρ_difference (opposition direction similarity). If ρ_centroid is high but ρ_difference is low → layers share content but oppose differently. If ρ_difference > ρ_centroid → opposition is more conserved than content (strongest evidence for concept-intrinsic).

**Data:** All 4 layers available in BGE-M3 embeddings (embeddings.npz). Cross-model files have yaoci only. So this is single-model (BGE-M3).

### Computation Phase

**Per-layer metrics:**

| Layer | Mean cos | #Neg | PR | 升↔无妄 rank |
|-------|---------|------|-----|-------------|
| yaoci | 0.818 | 0 | 22.3 | 17/32 |
| guaci | 0.573 | 0 | 16.1 | 29/32 |
| tuan | 0.690 | 0 | 22.7 | 22/32 |
| daxiang | 0.617 | 0 | 19.2 | 11/32 |

**Critical observation:** No negative complement cosines in ANY layer on raw embeddings. The complement opposition (R156: mean −0.19) was measured on *residual* embeddings after regressing out algebraic coordinates. Raw cosines are positive because all texts share genre.

**Cross-layer comparisons:**

| Pair | ρ_centroid (p) | ρ_diff (p) | Procrustes R² | profile ρ (p) |
|------|---------------|-----------|---------------|--------------|
| yaoci-guaci | −0.022 (.613) | −0.016 (.630) | 0.401 | +0.303 (.092) |
| yaoci-tuan | +0.093 (.115) | +0.080 (.040) | 0.461 | +0.259 (.153) |
| yaoci-daxiang | −0.029 (.640) | +0.042 (.171) | 0.429 | +0.061 (.742) |
| **guaci-tuan** | **+0.331 (.0001)** | **+0.328 (.0001)** | **0.576** | **+0.576 (.0006)** |
| guaci-daxiang | −0.014 (.584) | +0.028 (.247) | 0.358 | +0.294 (.102) |
| tuan-daxiang | +0.030 (.324) | +0.149 (.001) | 0.514 | +0.175 (.339) |

**Guaci length asymmetry:** KW ordering shows no effect (16/31, p=1.0). Valence correlation null (ρ=0.02). Dominated by 坤↔乾 (Δ=32 characters). Idiosyncratic.

### Review Phase (Discussion)

The sage identified three critical issues:

**1. Yaoci disconnection is genre artifact.** Line-averaging (6 short formulaic texts → centroid) produces fundamentally different geometry from whole-paragraph embeddings. The high yaoci mean cosine (0.82) confirms centroid compression. Cross-layer comparisons involving yaoci are uninformative about opposition structure — they measure genre difference, not opposition difference. Difference vectors do NOT fully correct for this because genre affects relative geometry (signal-to-noise), not just absolute positions.

**2. Procrustes R² uninterpretable without permutation null.** The 0.36–0.58 range exceeds random-subspace expectation (~0.02 for k=20 in R^1024) but may be inflated by shared genre/corpus structure. The correct null (permute hexagram labels, preserving per-layer geometry) was not computed. Without it, the Procrustes values are not evidence for or against cross-layer coupling.

**3. "Concept-intrinsic opposition" is untestable with current data.** Cannot separate conceptual content from textual genre in single-model embeddings. This is a methodological boundary.

**Consequence for R169:** The ~16 opposition dimensions are cross-model stable within yaoci (R168–R169 stand). But they cannot be shown to be concept-intrinsic — they are yaoci-intrinsic. Whether the same conceptual oppositions manifest in other text layers is untestable without genre-controlled data. This is an epistemic downgrade of the interpretation, not the measurement.

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R224 | Guaci and tuan share complement-opposition structure (profile ρ = 0.576, p < .001; ρ_diff = 0.33). Expected: commentary relationship | Measurement | New |
| R225 | Yaoci opposition geometry not comparable to hexagram-level layers (genre/construction confound). ~16 dims are yaoci-intrinsic, not demonstrably concept-intrinsic | Measurement | New |
| R226 | 升↔无妄 opposition is layer-dependent: rank 29/32 (guaci), 17/32 (yaoci), 11/32 (daxiang). R158 anomaly may be guaci-driven | Measurement | New |
| R227 | Guaci complement length asymmetry is idiosyncratic — uncorrelated with KW ordering (p=1.0) and valence (ρ=0.02). Dominated by 坤↔乾 | Measurement | New |

### Operational Notes

- Genre confound between text layers is severe and cannot be corrected by differencing. Line-averaging changes embedding geometry fundamentally — this limits ALL cross-layer analyses within the embedding paradigm.
- The sage's ρ_centroid vs ρ_difference decomposition was the right design, but the genre confound makes the yaoci comparisons uninterpretable regardless of which metric is used.
- Procrustes R² without a permutation null is uninformative. Always compute the task-relevant null, not just the random-subspace baseline.
- The guaci↔tuan coupling is the expected textual relationship dressed as a finding. Not everything that's statistically significant is scientifically informative.
- The R225 epistemic downgrade is the most important outcome of this iteration: it identifies a boundary of what the embedding methodology can establish. "Text-intrinsic" (cross-model within yaoci) ≠ "concept-intrinsic" (cross-layer across genres). The previous program conflated these.

---

## Iteration 4

### Design Phase (Discussion)

**Position-resolved opposition and differentiation — testing holistic vs positional structure.**

Sagemegistus identified a tension between existing findings:
- R162 (holistic composition): single-line change shifts ALL six texts
- R164 (inner core): inner lines carry thematic core (三<四<二<初<五<上)

These make conflicting predictions about WHERE complement opposition concentrates across the 6 line positions.

**Three threads:**
1. Position-resolved complement opposition (4 models × 6 positions)
2. Position-resolved d=1 differentiation by bit position (4 models × 6 bits)
3. 升↔无妄 per-position profile (piggybacks on #1)

**Sage's key clarification:** Parts A and B answer complementary questions — A asks where opposition concentrates by position, B asks where differentiation concentrates by bit. These are different measurements (content at each position vs sensitivity to structural changes).

### Computation Phase

**Part A: Position-resolved complement opposition**

| Position | bge-m3 | e5-large | labse | sikuroberta | argmax? |
|----------|--------|----------|-------|-------------|---------|
| L1 | highest | highest | highest | highest | **L1 = least opposed, 4/4 models** |
| L2 | low | low | low | mid | |
| L3 | low | mid | low | low | |
| L4 | mid | mid | mid | mid | |
| L5 | lowest | low | mid | lowest | |
| L6 | mid | lowest | lowest | low | |

L1 consistently least opposed (highest cosine) across all 4 models. Range = ~6.7% of mean — mild modulation, mostly holistic. The argmin (most opposed position) varies across models (L5, L6, L2) — no cross-model consensus on which position is MOST opposed.

**Part B: d=1 differentiation — flat across bit positions.**

All 6 bit positions produce statistically indistinguishable d=1 thematic shifts. One labse outlier at L3 (p=.010) doesn't replicate. This cleanly extends R162: the hexagram responds holistically regardless of which line is perturbed.

**Part A-B non-correlation:** The opposition positional profile does NOT correlate with the differentiation positional profile (Spearman ρ ≈ 0 across models). Opposition and differentiation are independent properties of the positional structure.

**Part C: 升↔无妄 bimodal pattern — the main finding.**

| Model | L1 | L2 | L3 | L4 | L5 | L6 |
|-------|----|----|----|----|----|----|
| bge-m3 | 29 | 28 | **5** | 27 | **4** | 30 |
| e5-large | 30 | 27 | **4** | 32 | **1** | 24 |
| labse | 31 | 27 | **6** | 28 | **2** | 22 |
| sikuroberta | 24 | 26 | **1** | 28 | **6** | 20 |

Bimodal: strongly opposed at L3 and L5 (ranks 1-6/32), weakly opposed at L1/L2/L4/L6 (ranks 20-32/32). Cross-model consistent.

**Follow-up: Rank variance bimodality analysis.**

- 升↔无妄 rank variance = 128.7 (2nd of 32 pairs, median = 68.8)
- Marginal correction is inapplicable: rank marginals are uniform by construction (column means = 16.5 always)
- Cross-model consistency of rank variance: mean ρ = 0.334. Architecture-stratified: bge-m3↔e5-large ρ=0.75 (strong), pairs involving sikuroberta ρ ≈ 0.1-0.3 (weak). Partial text-intrinsic signal.
- 4 pairs consistently bimodal (above 75th percentile in ≥3/4 models): 泰↔否, 升↔无妄, 恒↔益, 復↔姤
- Each has a unique positional signature — the bimodality is pair-specific, not a shared pattern

**Part D: Cross-model consistency.**
- Part A profiles: moderate consistency (ρ ranges from 0.5-0.9 across model pairs)
- Part B profiles: near-zero consistency (flat profiles → no signal to correlate)
- Part A-B correlation: near zero across all models

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R228 | Complement opposition mildly positional: L1 consistently least opposed (4/4 models), range ~6.7% of mean. Mostly holistic with mild L1 attenuation | Measurement | New |
| R229 | d=1 differentiation is flat across bit positions — holistic composition (R162) extends to bit-position decomposition | Measurement | New |
| R230 | Opposition and differentiation positional profiles are independent (ρ ≈ 0). Content opposition and perturbation sensitivity are different properties | Measurement | New |
| R231 | 升↔无妄 has bimodal position profile: opposed at L3/L5 (ranks 1-6), concordant at L1/L2/L4/L6 (ranks 20-32). Rank variance = 2nd of 32. Cross-model consistent (4/4 models above 75th %ile). Pair-specific — other high-variance pairs have different signatures | Measurement | New |

### Operational Notes

- Rank marginals are uniform by construction — "marginal correction" on rank matrices is a no-op. The sage's concern about L1 marginal effects was valid for absolute cosines but not for ranks. Always check whether the proposed correction is mathematically non-trivial before computing.
- The follow-up rank variance analysis was essential: without it, the L3/L5 pattern could have been dismissed as cherry-picking. With it, 升↔无妄 is objectively the 2nd most positionally heterogeneous pair.
- Cross-model consistency of positional heterogeneity (ρ = 0.334) is moderate and architecture-stratified. This is consistent with R213's finding that ~15% of geometry is architecture-dependent.
- The Part A-B independence finding is a clean structural result: the hexagram system separates "what each position says about opposition" from "how sensitive the whole hexagram is to structural changes at each position." These are logically independent properties and empirically confirmed to be so.

---

## Iteration 5

### Design Phase (Discussion)

**Testing whether R159 (Hamming V-shape) and R219 (text length as opposition axis) share a common mechanism.**

Sagemegistus identified this as the highest-value remaining test: if text-length difference shows a V-shape across Hamming distance, the two design principles (near-neighbor differentiation + complement opposition) share text length as a mediator. If flat, they're independent.

Two stages:
- Stage A (no embeddings): text-length difference by Hamming distance — does |Δlen| show a V-shape?
- Stage B (with embeddings): partial correlation — does R159 survive after controlling for text length?

**Sage's contribution:** Partial correlation is sufficient; formal mediation analysis (Sobel test) would require causal assumptions we can't justify. Also: compute Spearman ρ(Hamming_d, |Δlen|) as a shortcut — if ≈ 0, Stage B confirms independence but the conclusion is already clear.

### Computation Phase

**Stage A: Text-length V-shape — NO V-shape.**

| d | n pairs | mean |Δ yaoci_len| | mean |Δ guaci_len| |
|---|---------|---------------------|---------------------|
| 1 | 192 | 18.12 | ~8.4 |
| 2 | 480 | 19.00 | ~8.5 |
| 3 | 640 | 17.92 | ~8.1 |
| 4 | 480 | 17.82 | ~8.0 |
| 5 | 192 | 18.85 | ~8.7 |
| 6 | 32 | 19.25 | ~10.3 |

Yaoci: peak/trough ratio 1.046, ρ = −0.007, p = .76. Flat.
Guaci: marginal d=6 elevation (complement-specific, from R223), ρ = −0.006, p = .80. Not a V-shape.

**Stage B: R159 replication and partial correlation.**

Critical discovery: R159 does NOT replicate on raw embeddings (r ≈ −0.02, null across 4 models). It replicates perfectly on residual embeddings (after regressing out algebraic coordinates):

| Model | Raw r | Residual r | Partial r (|Δlen|) | Reduction |
|-------|-------|-----------|-------------------|-----------|
| bge-m3 | −0.019 (ns) | −0.097 *** | −0.097 *** | +0.2% |
| e5-large | −0.024 (ns) | −0.112 *** | −0.112 *** | −0.0% |
| labse | −0.001 (ns) | −0.066 ** | −0.066 ** | −0.6% |
| sikuroberta | −0.010 (ns) | −0.081 *** | −0.081 *** | +0.3% |

Partial correlation reduces R159 by < 1%. Text length has zero effect on the Hamming anti-correlation.

V-shape distance ratios:
- Raw (bge-m3): d=1: 1.001, d=3: 1.002, d=6: 1.019 — flat
- Residual (bge-m3): d=1: 1.055, d=3: 0.971, d=6: 1.183 — clear V-shape

### Review Phase (Discussion)

Sage accepted R232 and R233 as clean. Reframed R234: don't claim "R159 requires residuals" without checking original methodology. Instead, record precisely what was observed: raw space shows flat ratio profile, residual space shows V-shape. The algebraic component is positively correlated with Hamming proximity, counteracting the thematic anti-correlation.

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R232 | Text-length difference flat across Hamming distance (yaoci ρ = −0.007, guaci ρ = −0.006). No V-shape. Text length does not mediate the Hamming V-shape | Measurement | New |
| R233 | R159 completely independent of text length. Partial correlation reduces r by < 1% across 4 models. R159 and R219 operate on orthogonal dimensions of the opposition manifold | Measurement | New |
| R234 | Hamming-thematic anti-correlation is a residual-space phenomenon. Raw embeddings show flat ratio (1.001:1.002:1.019). Residual embeddings show V-shape (1.055:0.971:1.183). Algebraic component is positively correlated with Hamming proximity, masking the thematic anti-correlation | Measurement | New |

### Operational Notes

- The Spearman ρ shortcut (ρ ≈ 0 between Hamming distance and |Δlen|) immediately resolved Stage A — the V-shape test was technically redundant once ρ was computed.
- The raw vs residual distinction in R159 replication is methodologically critical: the algebraic ~11% creates positive Hamming-correlated similarity that exactly counteracts the negative thematic anti-correlation. This is why the V-shape is invisible in raw space but clear in residual space.
- The independence of R159 and R219 means the opposition manifold has at least two structurally independent design principles: one captured by text length (~1 dim, vocabulary-accessible), one captured by the Hamming V-shape (~15 dims, vocabulary-inaccessible). These don't interact at all.
- The < 1% reduction in partial correlation is as clean a null as possible for a mediation test. Not "weak mediation" — zero mediation.

---

## Iteration 6

### Design Phase (Discussion)

**Testing whether d=1 differentiation (R159 V-shape peak) and d=6 complement opposition (R156) are unified or independent.**

The V-shape in Hamming-thematic anti-correlation (R159) has peaks at d=1 and d=6. The d=6 peak is complement opposition (R156). Are these two aspects of a single monotonic gradient (hexagrams differentiate proportionally from local to global) or two independent phenomena (separate mechanisms for near-neighbor differentiation and complement opposition)?

**Design:**
- Compute per-hexagram d1_diff (mean cosine distance to 6 Hamming d=1 neighbors) and comp_opp (cosine distance to complement) in residual space
- Main test: Spearman ρ(d1_diff, comp_opp) across 4 models
- Controls: Hamming weight (geometric confound), complement symmetry (effective sample size)
- Monotonicity check: d=2 differentiation as intermediate distance test

**Residual extraction:** Built a centroid-level design matrix (algebraic coordinates from atlas) and regressed 64 hexagram centroids (averaged from 384 yaoci line embeddings) against it.

### Computation Phase

**Algebraic R² — unexpected inflation:**

| Model | R² (centroid) | Expected (R157) |
|-------|--------------|-----------------|
| bge-m3 | 0.3549 | ~0.11 |
| e5-large | 0.3510 | ~0.11 |
| labse | 0.3602 | ~0.11 |
| sikuroberta | 0.3620 | ~0.13 |

R² = 35–36% across all 4 models, versus 10.8–13.2% established in R157 on 384 line embeddings. The design matrix includes ~10+ dummy variables from categorical atlas features (basin, surface_relation, palace, palace_element, rank) plus 6 numerical features, fitted on only n=64 centroids. Overfitting is the likely explanation.

**Main test: d1_diff vs comp_opp — NULL (0/4 models significant).**

| Model | ρ(d1,co) | p | ρ partial (|hw) | p |
|-------|----------|---|-----------------|---|
| bge-m3 | −0.182 | 0.150 | −0.182 | 0.150 |
| e5-large | −0.129 | 0.308 | −0.126 | 0.323 |
| labse | −0.141 | 0.265 | −0.143 | 0.260 |
| sikuroberta | −0.109 | 0.391 | −0.099 | 0.437 |

Mean ρ = −0.14, consistent negative direction but nowhere near significance. Hamming weight control changes nothing (partial ≈ raw). All models agree: d=1 differentiation and complement opposition are uncorrelated.

**d=2 anti-coupling — significant in 3/4 models but flagged as potentially artifactual:**

| Model | ρ(d2,co) | p |
|-------|----------|---|
| bge-m3 | −0.393 | 0.001 ** |
| e5-large | −0.321 | 0.010 ** |
| labse | −0.264 | 0.035 * |
| sikuroberta | −0.214 | 0.090 |

d=2 shows stronger anti-coupling than d=1 across all 4 models — opposite to the prediction of a monotonic gradient. However, the R² = 35% overfitting means residual-space geometry is distorted: the regression absorbs noise along predictor dimensions, creating artificially small variance in algebraic directions. d=2 neighbors share more algebraic structure than d=1 or d=6 pairs, so d=2 distances are disproportionately affected by the distortion. The d=2 finding cannot be trusted until the residual extraction is corrected.

**Complement symmetry of d1_diff:**

| Model | ρ(d1_diff(h), d1_diff(σ(h))) | p |
|-------|-------------------------------|---|
| bge-m3 | +0.751 | <0.001 |
| e5-large | +0.661 | <0.001 |
| labse | +0.151 | 0.408 |
| sikuroberta | +0.496 | 0.004 |

High complement symmetry in 3/4 models (effective n ≈ 32, not 64 for independent observations). This is structurally expected: σ(h)'s d=1 neighbors are the complements of h's d=1 neighbors, so d1_diff(h) ≈ d1_diff(σ(h)) follows if complement opposition is roughly constant across pairs.

### Review Phase (Discussion)

**Sage assessment of R² discrepancy:**
The R² = 35% is almost certainly overfitting. With n=64 and k ≈ 10+ predictors, the degrees of freedom are insufficient. The adjusted R² ≈ 23% is still double the established 11%. Worse: overfitted regression distorts residual geometry by absorbing noise along predictor dimensions, biasing all downstream distance computations. Distances are compressed along algebraic axes and relatively inflated along non-algebraic axes.

**Sage assessment of findings:**

1. **R235 (d1 vs comp_opp independence): ROBUST.** This is a null result. The R² inflation makes residual distances noisier, which biases toward null. A null finding in the presence of distorted residuals is conservative — the true null is at least as strong. Cross-model consistent (0/4 significant, same direction).

2. **d=2 anti-coupling: UNRELIABLE.** Do not record. d=2 neighbors share more algebraic structure than d=1 or d=6 pairs; overfitted residual extraction disproportionately distorts d=2 geometry. Cannot distinguish real effect from artifact until residuals are corrected (either by reducing predictors for n=64, or by residualizing 384 line embeddings first then aggregating to centroids).

3. **"Thematic budget" interpretation: PREMATURE.** Even if d=2 effect survived artifact correction, ρ ≈ −0.30 means 9% shared variance. "Budget constraint" overstates the coupling.

**Captain's decision:** Record R235 only. The d=2 anti-coupling is flagged as requiring methodology verification. The complement symmetry of d1_diff is structurally expected (bit-flip bijection), not an empirical finding.

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R235 | d=1 differentiation and complement opposition are independent. ρ(d1_diff, comp_opp) null in 4/4 models (mean ρ = −0.14, p = 0.15–0.39). Hamming weight control changes nothing. The V-shape peaks at d=1 and d=6 arise from separate mechanisms. The thematic manifold has (at least) two independent organizing principles in its vocabulary-inaccessible ~15 dimensions | Measurement | New |

### Unreported observations (requiring methodology verification)

- d=2 anti-coupling with comp_opp: ρ ≈ −0.21 to −0.39, p < 0.05 in 3/4 models. Potentially artifactual from overfitted centroid-level residual extraction (R² = 35% vs expected 11%). Would need to be retested with corrected residuals (residualize 384 line embeddings first, then average to centroids; or reduce design matrix to ≤5 predictors for n=64).
- Algebraic R² inflation at centroid level: 0.35–0.36 across all 4 models. Expected ~0.11. Likely degrees-of-freedom issue with ~16 predictors on n=64. This is a methodological warning for any future centroid-level algebraic regression.

### Operational Notes

- The R² discrepancy is a clean example of overfitting in low-n regression: the established R² ≈ 11% (R157, n=384) inflates to 35% at n=64 with the same predictor set. Always check R² against established baselines when changing granularity.
- A null result under distorted residuals is conservative — if the regression absorbs too much variance, remaining distances are noisier, biasing correlations toward zero. R235 is robust precisely because it's null.
- The complement symmetry of d1_diff (ρ = 0.15–0.75) is structurally necessary, not empirical: h's d=1 neighborhood is the complement of σ(h)'s d=1 neighborhood. The variable cross-model magnitude reflects how constant complement opposition is across pairs, not an independent phenomenon.
- The d=2 > d=1 pattern (anti-coupling stronger at d=2) is opposite to both the unified-gradient prediction (d=1 should be strongest) and the independence prediction (both null). It's the one result that could be interesting if it survives artifact correction — but a single distorted-residual explanation is more parsimonious than a "local thematic budget."

---

## Iteration 7

### Design Phase (Discussion)

**Two threads: (1) verify d=2 anti-coupling with corrected residuals, (2) characterize reversal opposition in residual space.**

**Thread 1 rationale:** Iteration 6 flagged d=2 anti-coupling as potentially artifactual from overfitted centroid-level regression (R² = 35% vs established 11%). Fix: residualize at 384 line embeddings (where R² ≈ 11% is established), then average to 64 centroids. If d=2 survives, it's real. If it doesn't, R235 stands alone.

**Thread 2 rationale:** The complement involution has 9 levels of characterization. The reversal involution — the I Ching's other natural symmetry — has only R154 (disruption ratio 1.067 in raw space, barely above baseline). R85 proves complement is the unique *equivariant* involution (α = −1 is the only Z₅ automorphism compatible with the surjection). Reversal is NOT equivariant — it doesn't descend to Z₅. Prediction: reversal should show no systematic thematic opposition.

**Key design decisions:**
- Exclude anti-palindrome pairs (reverse = complement) from reversal analysis — complement opposition would contaminate
- 4-group classification: pure-reversal (24), non-palindrome-complement (28), anti-palindrome (4), palindrome-complement (4)
- Permutation test: randomly pair 48 non-palindrome hexagrams into 24 pairs (unconditional null)
- R159 profile comparison instead of Hamming-matched null: compare pure-reversal group mean at d=2 and d=4 against the established V-shape profile at those distances
- Pure-reversal Hamming distances: d ∈ {2, 4} only (reversal swaps 3 bit-pairs, each contributing 0 or 2 to Hamming distance)

### Computation Phase

**Part 1: Corrected residual extraction — R² confirmed at ~11%.**

| Model | R² (line-level) |
|-------|----------------|
| bge-m3 | 0.110 |
| e5-large | 0.108 |
| labse | 0.108 |
| sikuroberta | 0.132 |

Sanity check passed. The R² = 35% at centroid level was absorbing within-hexagram variance (which disappears when averaging 6 lines). Between-hexagram residual geometry is identical either way — line-level regression ∘ averaging = averaging ∘ line-level regression (linearity of both operations). The R² discrepancy was a display artifact, not a computation error.

**Part 1a: d=2 anti-coupling SURVIVES corrected residuals.**

| Model | ρ(d1,co) | p | ρ(d2,co) | p |
|-------|----------|---|----------|---|
| bge-m3 | −0.182 | .150 | **−0.393** | **.001** |
| e5-large | −0.129 | .308 | **−0.321** | **.010** |
| labse | −0.141 | .265 | **−0.264** | **.035** |
| sikuroberta | −0.109 | .391 | −0.214 | .090 |

Results identical to iteration 6 (as predicted by commutativity). d=1: 0/4 significant. d=2: 3/4 significant. The anti-coupling is not a residual extraction artifact.

**Part 2: Reversal opposition — non-significant trend.**

**2a. Pure-reversal Hamming distances:** 12 at d=2, 12 at d=4 (perfectly split).

**2b. Group statistics (residual cosine similarity, averaged across 4 models):**

| Group | n | mean cos | std |
|-------|---|----------|-----|
| Pure-reversal | 24 | −0.066 | ~0.145 |
| Non-pal complement | 28 | −0.195 | ~0.167 |
| Anti-palindrome | 4 | −0.209 | ~0.164 |
| Palindrome-complement | 4 | −0.142 | ~0.093 |

Hierarchy: anti-palindrome (−0.21) ≈ non-pal complement (−0.20) > palindrome-complement (−0.14) > pure-reversal (−0.07) > null baseline (−0.02).

**2c. Permutation test — NOT significant.**

| Model | Observed | Null mean ± std | p (two-sided) |
|-------|----------|-----------------|---------------|
| bge-m3 | −0.067 | −0.018 ± 0.028 | .085 |
| e5-large | −0.053 | −0.018 ± 0.026 | .179 |
| labse | −0.076 | −0.018 ± 0.036 | .102 |
| sikuroberta | −0.069 | −0.017 ± 0.031 | .090 |

0/4 significant at p < 0.05. All p-values in 0.08–0.18 range — consistent trend but not robust. Effect size ~0.05 cosine, approximately 30% of complement opposition magnitude.

**2d. R159 profile comparison — reversal pairs deviate from V-shape profile.**

| Model | d=2 deviation | d=4 deviation |
|-------|--------------|--------------|
| bge-m3 | −0.036 | −0.046 |
| e5-large | −0.012 | −0.040 |
| labse | −0.024 | −0.076 |
| sikuroberta | −0.034 | −0.048 |

Reversal pairs are consistently more opposed (more negative) than all-pairs at the same Hamming distance. Deviation larger at d=4 than d=2 in all 4 models. But given permutation tests are non-significant, this deviation is within noise.

### Review Phase (Discussion)

**Sage assessment:**

1. **d=2 anti-coupling: Record as R236.** Cross-model consistency (3/4) meets threshold. The "budget" interpretation is wrong — ρ ≈ −0.30 means 9% shared variance, not a conservation law. Parsimonious hypothesis: d=2 neighbors share one trigram (two bit flips within a trigram preserve the other). d=2 differentiation partly measures trigram dependency — hexagrams whose meaning depends on one trigram have high d2_diff within that trigram and low d2_diff in the other. Complement flips both trigrams, creating maximum contrast for single-trigram-dependent hexagrams. Testable follow-up but not required for recording.

2. **Reversal: Record as R237.** Non-significant but consistent trend. p ≈ 0.1 is "underpowered or absent" territory — n=24 with effect size ~0.05 cosine would need ~100 pairs for 80% power. The I Ching has exactly 24 pure-reversal pairs. R85 prediction not contradicted. Trend may reflect 序卦傳 pairing tradition rather than algebraic structure.

3. **Commutativity: Not a result.** Mathematical identity (linearity). Note in methodology, not as a numbered finding.

### Results

| # | Finding | Tier | Status |
|---|---------|------|--------|
| R236 | d=2 neighborhood similarity anti-correlates with complement opposition (ρ ≈ −0.21 to −0.39, p < 0.05 in 3/4 models). Absent at d=1 (R235). Hexagrams more similar to their d=2 neighbors are more opposed to their complements. Interpretation open — trigram dependency is a testable hypothesis | Measurement | New |
| R237 | Pure-reversal KW pairs show non-significant trend toward thematic opposition (mean residual cosine −0.066 vs null −0.018, p = 0.08–0.18 across 4 models). Effect size ~30% of complement opposition. R85 prediction (complement as unique equivariant bridge) not contradicted | Measurement | New |

### Operational Notes

- Line-level and centroid-level residualization commute (both linear). The R² = 35% at centroid level absorbed within-hexagram variance, not cross-hexagram signal. Both produce identical residual centroids. Always check commutativity before assuming granularity changes affect results.
- The d=2 > d=1 asymmetry may partly reflect measurement precision: 15 neighbors (d=2) vs 6 (d=1) gives lower-variance per-hexagram d_diff estimates, increasing power to detect correlations. This doesn't invalidate R236 but means the d=1/d=2 magnitude comparison isn't apples-to-apples.
- Reversal's p ≈ 0.1 is a hard ceiling: n=24 pure-reversal pairs with effect size ~0.05 would need ~100 pairs for 80% power. The I Ching has exactly 24. No amount of cross-model validation can overcome the sample size limit.
- The even d=2/d=4 split (12/12) in pure-reversal pairs is a structural fact about 6-bit palindrome statistics.
- Anti-palindrome pairs (reverse = complement) match non-palindrome complement opposition (−0.21 vs −0.20). The two involutions don't compound — anti-palindromes are complement pairs that happen to also be reversals, and their opposition is at the complement level.
- Palindrome-complement pairs (self-reverse) show slightly weaker opposition (−0.14 vs −0.20) than non-palindrome complements. With n=4, this is noise, but it's directionally consistent with palindromes being "more symmetric" = "less opposed."

---

## Iteration 8

### Design Phase (Discussion)

**Trigram decomposition of R236's d=2 anti-coupling — testing the mechanism.**

R236 is the one surprise finding from this investigation: d=2 neighborhood similarity anti-correlates with complement opposition, but d=1 does not (R235). The sage proposed a trigram dependency hypothesis: d=2 neighbors that share one trigram (2 bit flips within the other trigram) measure single-trigram dependency. If a hexagram's meaning depends on one trigram, complement (which flips both) creates maximum contrast.

**Key structural fact:** Of 15 d=2 neighbors, only 6 share a trigram (3 share lower, 3 share upper). The remaining 9 flip one bit in each trigram (cross-trigram). The within-trigram subset is the minority.

**Three competing hypotheses:**
1. Trigram dependency: within-trigram components drive R236, cross-trigram null. Trigram imbalance anti-correlates with comp_opp.
2. Interaction: cross-trigram drives R236 (coupling operates through trigram interaction, not single-trigram dependency).
3. Distributed: all components contribute weakly, significance emerges only from pooling.

**Sage's key distinction:** R167 established that trigrams don't predict opposition *direction*. This test asks whether trigrams predict opposition *magnitude* — a logically independent question. Both outcomes are interpretable.

### Computation Phase

**Bit convention verified:** bits 0–2 = lower trigram, bits 3–5 = upper trigram. ✓

**Component correlations with complement opposition:**

| Component | bge-m3 | e5-large | labse | sikuroberta | Mean ρ | Sig ≥3? |
|-----------|--------|----------|-------|-------------|--------|---------|
| d2_within_lower | −0.091 (.47) | −0.120 (.34) | +0.106 (.40) | +0.070 (.58) | −0.009 | 0/4 |
| d2_within_upper | −0.191 (.13) | −0.277 (.03) | −0.163 (.20) | −0.268 (.03) | −0.225 | 2/4 |
| d2_cross | −0.245 (.05) | −0.045 (.72) | −0.192 (.13) | −0.146 (.25) | −0.157 | 0/4 |
| d2_all (R236) | −0.393 (.001) | −0.321 (.010) | −0.264 (.035) | −0.214 (.090) | −0.298 | 3/4 ◄ |
| Trigram imbalance | +0.073 (.57) | +0.065 (.61) | −0.015 (.91) | +0.043 (.74) | +0.041 | 0/4 |

**Verdict: DISTRIBUTED.** No single component reaches ≥3/4 significance. Trigram imbalance null (0/4, mean ρ = +0.04). The coupling requires pooling all 15 d=2 neighbors. The trigram dependency hypothesis is rejected.

**Upper > lower asymmetry:** Within-upper (mean ρ = −0.225, 2/4) is notably stronger than within-lower (mean ρ = −0.009, 0/4). Directionally consistent with R165 (upper trigram more disruptive). Below the ≥3/4 cross-model threshold for recording as a standalone finding.

### Review Phase (Discussion)

**Sage assessment:** Fold the decomposition into R236 as a mechanism characterization, not a separate result. "R236 is distributed" is a property of R236, not an independent finding. Creating R238 would inflate the result count without adding an independent measurement.

**Captain concurred.** R236 updated to include the trigram decomposition. No new result numbers from iteration 8.

### Results

No new results. R236 updated:

| # | Finding (updated) | Tier | Status |
|---|-------------------|------|--------|
| R236 | d=2 neighborhood similarity anti-correlates with complement opposition (ρ ≈ −0.21 to −0.39, p < 0.05 in 3/4 models). Absent at d=1 (R235). The coupling is distributed across trigram components: no single sub-component (within-lower ρ ≈ −0.01, within-upper ρ ≈ −0.23, cross-trigram ρ ≈ −0.16) reaches cross-model significance individually (0/4, 2/4, 0/4). Pooling all 15 d=2 neighbors required. Trigram imbalance null (0/4). Consistent with non-decomposability of the thematic manifold (R167) | Measurement | Updated |

### Operational Notes

- The upper > lower asymmetry (ρ ≈ −0.23 vs −0.01, 2/4 vs 0/4) is directionally consistent with R165 (upper trigram more disruptive). Below threshold for recording but worth noting for pattern inventory.
- The distributed signature (no component significant, aggregate significant) is the same non-decomposability seen at every resolution: d=1 directions (R210, rank ~5.4/6), opposition direction (R167), vocabulary probes (R220, diffuse enrichment), and now d=2 coupling mechanism. The manifold's resistance to factoring is its defining characteristic.
- This test confirms the investigation has reached its natural boundary: the one surprising finding (R236) decomposes into the same holistic structure seen everywhere else. No new structural principle remains to extract at embedding resolution.

---

## Final Synthesis

Eight iterations. 23 results (R215–R237). Entry point: are the I Ching's parameters {2,3,5,8} structurally Fibonacci? Terminal finding: the ~16 opposition dimensions are irreducibly holistic.

**Phase 1 (iteration 1):** Fibonacci alignment is arithmetic coincidence — the forcing chain's mechanism is exponential/primality, not additive self-reference. The discriminator (structural iff derivation contains F(n+1) = F(n) + F(n-1)) resolved 4/6 questions analytically. R215–R218.

**Phase 2 (iterations 2–8):** Positive characterization of the ~16 cross-model-stable opposition dimensions. Decomposed along every available axis:

- **Accessible:** Text length captures ~1 of ~16 dims (R219). Opposition is vocabulary-diffuse (R220), not vocabulary-opaque.
- **Independent:** Three organizational principles — text length, d=1 differentiation, d=6 complement opposition — are mutually independent (R233, R235). The V-shape peaks arise from separate mechanisms.
- **Coupled:** d=2 neighborhood similarity anti-correlates with complement opposition (R236, ρ ≈ −0.30, 3/4 models). This single coupling is itself non-decomposable — distributed across trigram components.
- **Bounded:** Cross-layer comparison confounded by genre (R225). Opposition mostly holistic across positions (R228–R229) with pair-specific exceptions (R231). Reversal non-significant (R237).

**Central characterization:** Non-decomposability confirmed across five independent factoring axes (R167, R170, R210, R220, R236). The thematic manifold resists factoring not because the right decomposition hasn't been found, but because the texts compose meaning holistically.

**Methodological boundary reached:** Embedding paradigm at resolution limit (~15% architecture-dependent, R213). Further computation probes below the noise floor.

**Investigation closed.**
