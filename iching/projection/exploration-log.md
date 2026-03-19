# Resolution Investigation — Exploration Log

## Iteration 1: Dark Sector Characterization (Probe 4 / R5)

**Probe:** Characterize the hex-level eigenvalues with no trigram-level ancestor. Determine what symmetries organize them, what dynamics they control, and when they dominate.

**Method:** Full eigensystem of OR-symmetrized 64×64 五行 adjacency matrices. Coherent/dark separation by matching against tensor sums of trigram eigenvalues. Walsh basis decomposition of dark eigenvectors. Symmetry classification under complement (h↔63−h) and trigram swap (upper↔lower). Algebraic identification of dark eigenvalues. Dominance crossover computation.

**Script:** `dark_sector.py` → `dark_sector_results.json`

### Measured: Coherent/Dark Separation

| Type | Coherent | Dark | Coherent Weight | Coherent ρ | Dark ρ |
|------|----------|------|-----------------|------------|--------|
| 比和 | 32 | 32 | 21.1% | 2.000 | 3.661 |
| 生 | 20 | 44 | ≈0% | ≈0 | 4.496 |
| 克 | 20 | 44 | 9.1% | 3.236 | 4.688 |

The coherent eigenvalues for 比和 are {±2} (×4 each) plus 24 zeros. For 克, {±3.236, ±1.236} ≈ {±2φ, ±2/φ} (×1 each) plus zeros matching the "same-magnitude resonance filter" from R272. For 生, all 20 coherent eigenvalues are zero — the tensor product structure predicts only the kernel.

### Measured: 生 Coherent Sector Is Entirely the Kernel

The generation channel has zero non-trivial coherent eigenvalues. Every dynamical mode in the OR-symmetrized 生 subgraph is an interaction effect between upper and lower trigrams. The trigram-level eigenvalues for 生 are {±√2 (×2), 0 (×4)}; the tensor sums include ±2√2, ±√2, and 0, but only the zeros appear in the actual hex spectrum. The same-magnitude modes ±2√2 are destroyed by the fiber coupling.

Coherent content grades: 比和 (21.1%) > 克 (9.1%) > 生 (0%). This ordering inverts the Z₅ distance ordering: 比和 = distance 0, 生 = distance 1, 克 = distance 2. Adjacency on the 5-cycle (生) is more destructive to independent trigram dynamics than opposition (克).

**Untested:** Whether this kernel result holds for the directed 生 matrix (before symmetrization). If it does, the result is topological. If not, the OR-symmetrization is the mechanism.

### Measured: Walsh Basis Distribution of Dark Eigenvectors

Dark eigenvector energy distributed across Walsh weights:

| Weight | 比和 | 生 | 克 | Binomial C(6,w)/64 |
|--------|------|---|---|---------------------|
| 0 | 2.7% | 2.1% | 2.2% | 1.6% |
| 1 | 14.0% | 12.2% | 11.2% | 9.4% |
| 2 | 18.3% | 25.2% | 25.8% | 23.4% |
| 3 | 31.6% | 21.1% | 21.5% | 31.3% |
| 4 | 16.7% | 25.2% | 26.0% | 23.4% |
| 5 | 14.1% | 12.2% | 11.2% | 9.4% |
| 6 | 2.7% | 2.1% | 2.2% | 1.6% |

比和 follows the binomial distribution closely (weight-3 dominant). 生 and 克 shift energy from weight 3 toward weights 2 and 4, producing a "saddle" distribution. No concentration at specific Walsh weights. No correspondence to the weight-3 eigenspace from the semantic manifold (R254–R256).

### Measured: Symmetry Classification

All three OR-symmetrized matrices commute with both complement and trigram swap (||[A,P]|| = 0 verified numerically). The Z₂ × Z₂ symmetry partitions the 64-dimensional space into sectors of dimension 20, 12, 16, 16 (universal, depends only on Q₆ geometry).

All eigenvalues come in ±pairs — a consequence of bipartiteness inherited from Q₆.

生 and 克 eigenvectors decompose cleanly into definite parity sectors (0 mixed states). 比和 has 20 mixed-parity states in the raw eigensystem (degenerate eigenspaces where `eigh` picks arbitrary bases).

### Measured: Algebraic Structure

- **比和 dark eigenvalues:** 28/32 identified in Q(√2) or Q(√5). The 4 unidentified are ±3.661 and ±0.773, which are roots of x⁴ − 14x² + 8 = 0 (discriminant involves √41).
- **克 dark eigenvalues:** 10/44 identified in Q(√5). The ±2.303 and ±1.303 values are roots of x⁴ − 7x² + 9 = 0 (discriminant involves √13). 34 eigenvalues unidentified.
- **生 dark eigenvalues:** Only 2/44 identified (±2.0 ∈ Q). 42 eigenvalues have no simple closed form — generic algebraic numbers of degree > 4.

Algebraic complexity gradient: 比和 (simple) > 克 (intermediate) > 生 (generic). The same ordering as coherent content.

### Measured: Dominance Crossover

| Type | Crossover from hex 0 | Average crossover | Never cross (of 64) |
|------|----------------------|-------------------|---------------------|
| 比和 | step 0 | 2.0 | 3 |
| 生 | N/A (isolated vertex) | 0.13 | 2 |
| 克 | step 1 | 0.25 | 0 |

Dark sector dominates from essentially step 0 for all types. For 克, every initial hexagram crosses into dark dominance by step 1. For 生, the coherent sector is trivial — any non-kernel state is 100% dark.

### Discussion Findings

**Partition tightness interpretation (from review discussion):** The dark sector's spectral genericity (Walsh-binomial, no internal structure, immediately dominant) is evidence that the minimal Markov partition is tight *on the constraint axis*: it captures exactly the constraints (GMS, valve, Chebyshev) and nothing more. The dynamics within the constraint manifold are free. This reframes R5 from "what's in the dark sector?" (answer: generic dynamics) to "is the partition tight?" (answer: yes, on the constraint axis). Scope qualifier: this does not address whether 64 states is the minimal encoding of these constraints — only that no spectral constraints are missing.

**Constraint/dynamics orthogonality:** The edge-type axis (五行 typing) defines the constraint manifold. The bit-layer axis (互 as RG) coarse-grains dynamics within it. The coherent/dark decomposition operates on the constraint axis; the RG relevant/irrelevant decomposition operates on the dynamics axis. These are orthogonal (R274), and the dark sector results confirm this spectrally: constraints don't predict dynamics.

**生 irreducibility:** The generation channel's complete kernel result means 生 is maximally irreducible to trigram components. Discussion proposed this arises from adjacency on the Z₅ cycle making the fiber coupling "maximally non-diagonal." The directed matrix test would determine whether this is topological or an artifact of symmetrization.

### Candidate Results

- **R282:** Dark sector genericity = partition tightness on the constraint axis. The 五行 edge-type decomposition captures all spectral constraints; the dark sector is generic (Walsh-binomial, immediately dominant).
- **R283:** 生 coherent sector is entirely the kernel. Generation is maximally irreducible to trigram components. Coherent content grades inversely with Z₅ proximity.
- **R284:** Algebraic complexity hierarchy across types: 比和 (Q(√2), Q(√5), Q(√41)) > 克 (Q(√5), Q(√13)) > 生 (generic).
- **R285:** Constraint/dynamics orthogonality confirmed spectrally, consistent with R274.

### Predictions Generated

1. Directed 生 matrix has trivial coherent sector (topology test for R283)
2. 生 transitions are worst for multi-step information preservation (input to Probe 5)
3. Logistic map at Fibonacci parameter: Q₃ embeddability of the Markov partition is the fastest kill condition (input to Probe 1)

## Iteration 2: Directed 生 Topology Test + Logistic Map Probe (R1 / Probe 1)

### Task A: Directed 生 Matrix Coherent Fraction

**Probe:** Test whether R283 (生 coherent sector = kernel) is topological or an artifact of OR-symmetrization.

**Method:** Compute eigenvalues of the raw directed 64×64 生 adjacency matrix (144 directed edges, non-symmetric). Match against tensor sums of directed trigram-level 生 eigenvalues. Count coherent vs dark.

**Result: R283 is topological.** The directed 生 matrix has 24 coherent eigenvalues, all zero. Every non-zero eigenvalue is dark. The kernel result is about how the 生 relation organizes Q₆, not about the symmetrization procedure.

| Property | OR-symmetrized | Directed |
|----------|---------------|----------|
| Coherent eigenvalues | 20 (all zero) | 24 (all zero) |
| Dark eigenvalues | 44 | 40 |
| Dark spectral weight | 100% | 100% |
| Spectral radius | 4.496 | 2.799 |

Unexpected observation: the directed 生 matrix has all-real eigenvalues (64/64), despite being non-symmetric. This implies the matrix is similar to a symmetric matrix, possibly via a diagonal similarity related to detailed balance.

### Task B: Logistic Map at GMS Parameter (Probe 1 / R1)

**Probe:** Does the logistic map at the GMS parameter produce a Markov partition matching the I Ching's 64-state transition structure?

**Method:** Computed transition graphs of x → rx(1−x) at r = 1+√5 ≈ 3.236 for partitions of 2, 4, 8, 16 equal intervals. Tested Q₃ embeddability of the 8-cell transition graph. Computed natural Markov partition using critical point iterates. Compared spectral structure.

**Script:** `logistic_map.py` → `logistic_map_results.json`

### Proven: The I Ching Is Not the Markov Partition of Any 1D Map

**Structural impossibility (absolute obstruction):** Continuous 1D maps produce transition matrices where each row is a contiguous block of 1s (because f maps intervals to connected intervals). Such transition graphs are interval graphs. Q₃ is not an interval graph — it has rows like [0,1,1,0,1,0,0,0] (Hamming-1 neighbors are non-contiguous). No reordering of cells can fix this. This rules out all 1D maps at all parameters with all partitions.

### Measured: Q₃ Embeddability Failure

The logistic map at r = 1+√5 with 8 equal intervals gives:
- Logistic degree sequence: [2, 3, 3, 3, 4, 4, 4, 5] — non-uniform
- Q₃ degree sequence: [3, 3, 3, 3, 3, 3, 3, 3] — uniform
- Logistic edges: 14 (symmetrized) vs Q₃ edges: 12
- Logistic transition matrix: asymmetric; Q₃ adjacency: symmetric
- Q₃ embeddability: FALSE

### Measured: Natural Markov Partition Cell Counts

The critical-point-based Markov partition (dynamically natural boundaries at critical point iterates) gives:
- 2-bit resolution: 3 cells (boundaries at {0, 0.191, 0.5, 0.809})
- 3-bit resolution: 5 cells (boundaries at {0, 0.063, 0.191, 0.5, 0.809, 0.937})

Cell counts: 2, 3, 5, 8... — Fibonacci numbers, not powers of 2. This is a direct consequence of the GMS constraint: the number of legal words of length n in the GMS grows as F(n+2).

### Measured: Spectral Comparison

| Property | Logistic (8 cells) | I Ching 克 (trigram) |
|----------|-------------------|---------------------|
| Spectral radius | 2.000 | 1.618 (φ) |
| Nonzero eigenvalues | {2, −φ, 1, 1/φ} | {±φ, ±1/φ} |
| Field | Q(φ) | Q(φ) |

Both spectra live in Q(φ). The overlap: φ and 1/φ appear in both. The GMS connection is real at the constraint level — shared forbidden-"11" pattern, shared entropy log(φ), shared algebraic field Q(φ). But the geometries diverge: interval graph vs hypercube graph.

### Discussion Finding: Constraint-on-Transitions vs Constraint-on-States (R287)

The logistic map and the I Ching realize the GMS in fundamentally different ways:

- **Fibonacci route (logistic map):** The state space IS the set of legal sequences. Only GMS-allowed states exist as cells. Cell count grows as Fibonacci. The constraint is on which states exist.

- **Hypercube route (I Ching):** The state space is the FULL binary cube (all 2⁶ = 64 states). The GMS constraint lives on edges (transition typing as 克), not on vertices. All states exist; the constraint is on how you move between them.

This explains three dark sector properties simultaneously:
1. **Existence:** The 64-vertex hypercube is larger than the GMS needs (~13 GMS-legal 6-sequences). The excess provides the dark sector.
2. **Genericity:** The excess has no reason to carry specific structure.
3. **Dominance:** The excess is large (64 ≫ 13).

### Discussion Finding: R1 Reframed

The original question: "What is it projecting?" The logistic map probe rules out all 1D maps. The remaining question is sharper: is the I Ching an abstract minimal arena for the constraint class {GMS + complement symmetry + Z₅ typing}, or does a specific multi-dimensional binary system with coupled 3-bit blocks exist as its referent?

The arena interpretation is consistent with Phase 5's conclusion (judgment instrument, not physics model). An abstract arena for assessment would have: all states present (any situation assessable), constraints on transitions (how situations relate), generic dynamics within constraints (content is free). This matches the measured dark sector properties.

If a specific referent exists, it must be a system with: (1) two coupled 3-bit subsystems, (2) single-bit transition dynamics, (3) state-dependent coupling between subsystems. This eliminates standard spin models (where interaction is between adjacent sites, not blocks).

### Candidate Results

- **R283 confirmed topological** (directed matrix test passes — the 生 kernel is not a symmetrization artifact)
- **R286:** The I Ching is not the Markov partition of any 1D map. Q₃ is not an interval graph. Absolute obstruction.
- **R287:** Constraint-on-transitions (hypercube, all states exist, GMS on edges) vs constraint-on-states (Fibonacci, only legal states exist). The dark sector is the spectral content of the over-complete embedding.
- **R1 reframed:** "What is it projecting?" → "Is it an abstract arena or does a specific coupled-3-bit system exist as referent?"

### What Remains

- Probe 5 (composability): 生 predicted worst for multi-step information preservation. Arena interpretation predicts rapid convergence to stationary distribution (no long-range structure).
- Probes 2–3 (timescale survey, regime transition data): lower priority, empirical.
- Proper factorization of characteristic polynomials over Q (sharpen R284): lower priority.
- Directed 生 real-eigenvalue mechanism (detailed balance?): low priority, doesn't change R283.

## Iteration 3: Composability Probe (Probe 5 / R6)

**Probe:** Test whether the I Ching's transition structure preserves information across multiple steps, and how this varies by transition type.

**Method:** n-step type flow matrices, per-type mutual information decay, eigenvalue composition, 互 interaction with transitions, information entropy evolution, arena diagnostic (autocorrelation decay), directed vs symmetric subgraph comparison.

**Script:** `composability.py` → `composability_results.json`

### Measured: Type Information Destroyed in 1–2 Steps

The full transition graph IS Q₆ — every single-bit-flip is a valid transition regardless of 五行 type. The type labels classify edges but do not restrict connectivity. Walk dynamics on the full graph are purely Q₆.

| Step | TV distance from stationary | Type info remaining |
|------|---------------------------|---------------------|
| 0 | 0.781 | 100% |
| 1 | 0.118 | ~15% |
| 3 | 0.017 | ~2% |
| 5 | 0.006 | <1% (mixed) |
| 10+ | 0.004 | Bipartite residual only |

Mixing time: 5 steps. Stationary distribution: 比和=0.219, 生=0.375, 克=0.406 (proportional to vertex type counts 14:24:26).

Persistent residual TV ≈ 0.0045 from bipartite parity: Q₆ is period-2, and 比和 (8 even / 6 odd) and 克 (12 even / 14 odd) have unequal parity splits. 生 (12 even / 12 odd) is parity-balanced and converges exactly.

### Measured: Dark Sector Prediction Confirmed

Mutual information half-lives by type:

| Type | MI(1) | MI(2) | MI(4) | Half-life | Dark % (Probe 4) |
|------|-------|-------|-------|-----------|-------------------|
| 比和 | 0.604 | 0.240 | 0.095 | ~1.8 steps | 79% |
| 克 | 0.450 | 0.128 | 0.023 | ~1.4 steps | 91% |
| 生 | 0.359 | 0.093 | 0.014 | ~1.1 steps | 100% |

生 decorrelates fastest (MI drops 97% in 4 steps), 比和 slowest (84% drop). Ordering matches coherent content gradient from Probe 4: more dark = faster decorrelation.

### Measured: 互 Preserves Exactly 1/3 of Transitions

互(b₀b₁b₂b₃b₄b₅) = b₁b₂b₃b₂b₃b₄. Effect on bit-flips:

| Bit flip | Effect on 互 | Hamming distance | Preserved? |
|----------|-------------|------------------|------------|
| b₀ (outer lower) | Lost | 0 | No (same vertex) |
| b₁ (middle lower) | 1-to-1 | 1 | **Yes** |
| b₂ (boundary lower) | Doubled → bits 1,3 | 2 | No |
| b₃ (boundary upper) | Doubled → bits 2,4 | 2 | No |
| b₄ (middle upper) | 1-to-1 | 1 | **Yes** |
| b₅ (outer upper) | Lost | 0 | No (same vertex) |

Exactly 2/6 = 1/3 of transitions preserved. Result is **type-independent** (same 1/3 fraction for 比和, 生, 克). Pure Q₆ geometry × 互 bit structure.

互 does not commute with transitions: ||[A, H]||_F = 25.3. 互 has 2 fixed points.

### Measured: Directed vs Symmetric Subgraph Divergence

Walking within a single type's subgraph (restricted dynamics):

| Type | Directed H(5) | Symmetric H(5) | Max entropy |
|------|--------------|----------------|-------------|
| 比和 | 0.06 | 1.55 | 1.58 |
| 克 | 0.11 | 1.48 | 1.58 |
| 生 | 0.24 | 1.37 | 1.58 |

Directed subgraphs trap information: the 体用 directionality creates absorbing-like structures. Symmetric subgraphs dissipate normally. The divergence is dramatic — two orders of magnitude in entropy.

### Measured: Arena Diagnostic

Lazy chain autocorrelation decay times (removes bipartite oscillation):

| Type | Decay time τ | Stationary π |
|------|-------------|-------------|
| 比和 | 2.39 | 0.219 |
| 生 | 2.41 | 0.375 |
| 克 | 2.32 | 0.406 |

Spectral gap = 1/6 (from Q₆ geometry). All types decorrelate in τ ≈ 2.4 lazy steps. **Verdict: rapid decorrelation.**

### Discussion Finding: 生 Parity Balance Forced by Uniqueness Theorem (R291)

The {2,2,2,1,1} element partition gives two singleton elements (Water = trigram 2, Fire = trigram 5) and three doublet elements. Each doublet has one even-parity and one odd-parity trigram, producing balanced hexagram parity for any pair involving a doublet.

Parity imbalance arises only from singleton×singleton pairs. The two singleton elements are at Z₅ distance 2 (克 relation) — forced by the complement-Z₅ structure. Therefore:
- 比和: Water×Water + Fire×Fire = 2 extra even hexagrams → 8/6 split
- 克: Water×Fire + Fire×Water = 2 extra odd hexagrams → 12/14 split
- 生: No singleton×singleton pairs → exact 12/12 balance

生's exact convergence (no bipartite residual) is downstream of the uniqueness theorem.

### Discussion Finding: R1 Closed — Not Projecting an External System (R288)

The I Ching is the unique canonical classification of single-step changes in a 6-bit binary system under complement-Z₅ axioms. It is not projecting an external dynamical system.

Evidence:
1. Not the Markov partition of any 1D map (R286, structural impossibility)
2. The full transition graph IS Q₆ — the typing classifies edges but doesn't constrain the graph
3. Type information decorrelates in 1–2 steps — the classification is single-step, not trajectory-level
4. Dark sector is generic — no external system's signature
5. Directed single-step subgraphs are the regime where the architecture is informative — matching traditional practice

The "minimal Markov partition" interpretation from Phase 7 refines to: the I Ching is the minimal system on which the constraint class {GMS + complement + Z₅} can be written. Not a minimal partition *of* some external target, but a minimal stage *for* these constraints.

Consistency check against all prior phases (1–7): consistent. The algebra is the typing; the text is the content within the frame. Grammar ≠ vocabulary.

### Discussion Finding: Q2 Connection

Q2 (reversal) asked whether composability is forced. The composability results show: multi-step type composition is not structurally supported (rapid decorrelation). Composability in the algebraic sense (group axiom) is not needed because the system is designed for single-step assessment. The forcing chain's one contingent step (the valve) operates at the single-step level.

### Candidate Results

- **R288:** The I Ching is the unique canonical classification of single-step Q₆ transitions under complement-Z₅ axioms. Information content concentrated in single-step regime. R1 closed.
- **R289:** Composability decorrelation confirms dark sector predictions. MI half-lives: 生 ~1.1, 克 ~1.4, 比和 ~1.8.
- **R290:** 互 preserves exactly 1/3 of transitions, type-independently. Only middle-line bit-flips survive.
- **R291:** 生 bipartite parity balance forced by uniqueness theorem. Singleton elements at Z₅ distance 2 → no singleton×singleton pairs in 生.

### Status

Theoretical arc of the resolution phase is complete:
- R1 (what is it projecting?): closed — not projecting anything external
- R5 (dark sector): closed — generic, partition tight on constraint axis
- R6 (composability): closed — single-step regime, rapid decorrelation

Remaining probes (2–3) are empirical questions about whether natural systems exhibit these constraints. Different investigation, different methods. The theoretical question is answered.

## Final Synthesis

### The Arc

The phase started with: "If the I Ching is a minimal Markov partition, what is it projecting?" It ended with: "Nothing external. It is the minimal stage on which the constraint class can be written."

Three iterations traced a narrowing path:
1. **Dark sector characterization** established that the 60/64 dark eigenvalues are spectrally generic (partition tight on constraint axis), that generation is maximally irreducible to components (生 = pure kernel, topological), and that constraint/dynamics axes are orthogonal.
2. **Logistic map probe** proved the I Ching is not the Markov partition of any 1D map (Q₃ is not an interval graph), and revealed the constraint-on-transitions vs constraint-on-states distinction — two incompatible architectures for realizing the same GMS constraint.
3. **Composability probe** showed type information decorrelates in 1–2 steps, confirmed dark sector predictions quantitatively, and identified the directed single-step regime as where the architecture is informative.

### What Changed from Phase 7

Phase 7 framed the I Ching as "the smallest Markov partition that simultaneously captures a nontrivial spectral hierarchy, a forbidden-pattern constraint, and an inversion symmetry." This assumed a projection target — some class of external systems being approximated.

This phase eliminated the projection interpretation. The full transition graph IS Q₆ — the typing classifies edges but doesn't constrain the graph. The dark sector is generic — no external system's signature. The classification is single-step — trajectories carry no type information beyond step 1–2.

The refined interpretation: the I Ching is the unique canonical typing of Q₆ transitions under complement-Z₅ axioms. Not a projection of something, but the one and only way to assign meaning to hypercube transitions under these axioms. The constraint class {GMS + complement + Z₅} coexists only here (uniqueness theorem). The text provides content within this frame; the algebra provides the frame. They are independent because they operate on different aspects (edges vs vertices) of the same graph.

### Connection to Prior Phases

| Phase | Finding | How this phase connects |
|-------|---------|------------------------|
| 1 (what is it) | Unique rigid surjection F₂³ → Z₅ | = uniqueness of the edge typing |
| 2 (why unique) | (3,5) is the sole solution | = why Q₆ is the only stage |
| 3 (where stops) | 11% algebraic, 89% residual | = algebra is edge typing, text is vertex content |
| 4 (inside boundary) | ~16-dim thematic manifold | = vertex content organized by complement only |
| 5 (what it's for) | Judgment instrument | = single-step assessment, not trajectory prediction |
| 6 (wider connections) | φ through Route B | = intrinsic to the P₄ edge coloring on Q₃ |
| 7 (what it represents) | Minimal Markov partition | → refined to: minimal stage for constraint class |

### Running Results

R282–R291 (10 results). Total across investigation: ~291 results across 8 phases.

### Open Questions

**Refinements:** Z₅ proximity inversion mechanism (R283), algebraic discriminants (R284), directed subgraph trapping (R289). Computable but don't change the structural picture.

**New direction:** Shift spaces as hypercube edge colorings — general theory of embedding shift constraints in Q_n. Connects to coding theory and algebraic graph theory. A different investigation.

**Empirical:** Timescale ratios in natural systems (R2), regime transition statistics (R3). Different methods, different investigation.
