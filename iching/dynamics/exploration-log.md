# Dynamics Investigation — Exploration Log

## Iteration 1: Semantic Laplacian and Walsh Spectrum (Probe D1)

### Entry Point

Q11–Q15 ask whether the line-change transition graph (Q₆ hypercube) has dynamical structure in the semantic manifold. Prior nulls (R192, R209) established that 五行 edge labels (克/生/比和) carry no semantic information. This iteration tests vertex-level flow structure via the graph Laplacian.

### Method

**Step 1: Walsh spectral decomposition.** Projected 64×1024 centered hex-level BGE-M3 embeddings onto Walsh-Hadamard basis of Q₆. Measured variance fraction per eigenspace (7 groups by Hamming weight). Permutation null: 1000 label shuffles.

**Step 2: Laplacian field analysis.** Computed Lap(h) = mean(neighbor embeddings) − emb(h).
- 2a: ||Lap(h)|| distribution vs permutation null
- 2b: Complement Laplacian anti-parallelism (cosine of Lap(h) and Lap(63−h) for 32 pairs)
- 2c: Algebraic correlates of ||Lap(h)||

All steps repeated in residual space. Cross-model check on E5-large for Step 2b.

Script: `d1_laplacian_walsh.py`

### Results

**Walsh spectrum near-flat with weight-3 enrichment (97.9th %ile).** Weight-1 depleted (4.4th), weight-4 depleted (5.0th). No low-pass or high-pass concentration.

**Complement Laplacian anti-parallelism: fails cross-model.** BGE-M3 raw marginal (5th %ile, mean cosine −0.033). E5-large: 26th %ile. The complement involution is static opposition, not flow opposition.

**No algebraic correlates of Laplacian magnitude.** All p > 0.12.

**Residual anti-smooth at 0th percentile.** The non-algebraic content actively differentiates adjacent hexagrams.

→ R253 (dynamics negative)

### Side finding

The weight-3 enrichment led to the manifold identification (R254–R256), which is a Q1 result, not a dynamics result. Those iterations are recorded in `reversal/exploration-log.md` Phase 9.

---

## Iteration 2: 五行-Labeled Subgraph Spectra (Probe 1)

### Entry Point

Probe 1 from `plan.md` (Q15). Decompose Q₆ into three edge-typed subgraphs by 五行 relation, compute spectra, connectivity, and determine how trigram-level structure lifts to hexagram level. First probe that treats the transition graph as a purely combinatorial object without embeddings.

### Method

Built three 64×64 adjacency matrices from `atlas/transitions.json`, classified by `tiyong_relation` (克/生/比和). Analyzed in four modes: directed (as given), AND-symmetrized (bidirectional edges only), OR-symmetrized (either direction suffices), and at the 8×8 trigram level. Computed eigenvalues, connected components, spectral gaps, and tested whether 64-vertex subgraphs decompose as Cartesian products of 8-vertex trigram subgraphs.

Script: `p1_subgraph_spectra.py`. Results: `p1_results.json`.

### Results

**[measured] The 五行 classification is inherently directed.** Every hexagram sends ALL 6 of its outgoing transitions to the SAME 五行 group. The directed matrix decomposes as A_g = P_g × A_{Q₆}, where P_g is the diagonal projection onto hexagrams with surface relation g. The edge label is determined entirely by the source vertex.

- 132 of 192 undirected Q₆ edges (69%) carry different 五行 types in the two directions
- Antisymmetric norms are 66–82% of symmetric norms — the directed structure carries substantial information
- Pair distribution: (克,生)=64, (克,比和)=44, (比和,生)=24, (克,克)=24, (生,生)=28, (比和,比和)=8
- Vertex counts: 比和=14, 生=24, 克=26 hexagrams (out-degree 6 each → 84, 144, 156 directed edges)

**[measured] Trigram-level spectral radii: 1 (比和), √2 (生), φ (克).**

Trigram 8×8 adjacency eigenvalues:
- 比和: {−1(×2), 0(×4), 1(×2)} — two disjoint K₂ edges
- 生: {−√2(×2), 0(×4), √2(×2)} — two disjoint P₃ paths
- 克: {−φ(×2), −1/φ(×2), 1/φ(×2), φ(×2)} — two disjoint P₄ paths

These are 2cos(π/3), 2cos(π/4), 2cos(π/5) — a Chebyshev sequence with denominators 3, 4, 5. The 五行 partition decomposes the 12 trigram-cube edges into paired paths of consecutive lengths {P₂, P₃, P₄}, exhausting all edges.

**[measured] 克 is the unique universally connected subgraph.**

OR-symmetrized connectivity:
- 比和: 11 components (one 54-vertex + 10 isolates)
- 生: 3 components (one 62-vertex + 2 isolates)
- 克: 1 component (all 64 vertices connected)

AND-symmetrized connectivity (bidirectional edges only):
- 比和: 58 components (two 4-cliques + 56 isolates)
- 生: 42 components (two 12-vertex + 40 isolates)
- 克: 44 components (two 9-vertex + four 2-vertex + 38 isolates)

**[measured] Spectral gaps inversely ordered to connectivity.**

AND-symmetrized spectral gaps (λ₁ − λ₂):
- 比和: 2.0 (fastest mixing within its small clusters)
- 生: 0.951
- 克: 0.288 (slowest mixing despite universal reach)

**[measured] Tensor product test fails.** The 64-vertex subgraph spectra do NOT equal Cartesian products of the 8-vertex trigram spectra for any type. Max deviations: 比和=2.0, 生=1.41, 克=2.24. The hexagram-level edge labeling depends on the interaction of BOTH trigrams (the surface relation), not just the changing trigram. The structure is a fiber bundle, not a product.

### Structural observations from discussion

**Weak-tie topology.** The combination of connectivity and spectral gap data produces three regimes: 比和 = small closed clusters (strong ties), 生 = near-global bridges (moderate ties), 克 = universal slow connector (weak ties). 克 connects everything but mixes slowest — a random walk on 克 takes ~7× longer to equilibrate than on the full graph.

**KAM/irrationality ordering.** The spectral radii 1, √2, φ are also ordered by continued-fraction irrationality: 1=[1] (rational), √2=[1;2,2,...] (moderate), φ=[1;1,1,...] (maximal). In KAM theory, maximally irrational frequency ratios correspond to the most robust tori. This maps 克 to maximal stability. However, this ordering is contingent on the specific element assignment (which 五行 type gets which path length), not forced by algebra. Record as structural, not designed.

**生-free attractor.** The 互 attractor {0, 21, 42, 63} has vertex types {比和, 克, 克, 比和} — no 生. Analysis: the 互 map's fixed points {000000, 111111} are identical-trigram hexagrams → necessarily 比和. Its 2-cycle {010101, 101010} is the maximally alternating pair (Kan☵/Li☲), which the element assignment maps to Water/Fire → 克. This is doubly contingent: the 互 map selects the alternating pair (structural), and the element assignment makes it 克 (contingent). 生's absence from the attractor is specific to this assignment — other complement pairs would produce 生 or 比和 endpoints.

---

## Iteration 3: 互 Map Dynamics + Real-Eigenvalue Null Test (Probe 2)

### Entry Point

Probe 2 from `plan.md` (Q15). Analyze the 互 (nuclear) map as a discrete dynamical system on 64 states. Cross-tabulate with 五行 vertex type to test whether the fiber bundle structure (Probe 1) and 互 dynamics are aligned or orthogonal. Also resolve the open question from Probe 1: are the real eigenvalues of directed matrices specific to the 五行 partition or generic?

### Method

Built the 64→64 functional graph from `atlas.json` (hu_hex field). Computed full orbit structure, basin membership, preimage distribution, contraction analysis (mean Hamming distance ratio at each starting distance, broken down by 五行 type), basin × 五行 cross-tabulation, 五行 transition matrix under 互, and Hamming distance to attractor by type.

For the null test: generated 1000 random partitions of 64 vertices into groups of sizes {14, 24, 26}, built P_random × A_{Q₆} for each, and checked whether all eigenvalues were real.

Script: `p2_hu_dynamics.py`. Results: `p2_results.json`.

### Results

**[measured] hu² is determined by two bits.** hu²(h) = 21·b₂ + 42·b₃, where b₂, b₃ are bits 2,3 (lines 3,4 — the inter-trigram boundary). The 互 map collapses 6 bits to 2 in exactly 2 steps. Transient distribution: {depth 0: 4, depth 1: 12, depth 2: 48}. 75% of hexagrams need exactly 2 steps.

**[measured] Basins perfectly balanced.** 16 hexagrams per basin. Preimage perfectly regular: in-degree = 4 for all 16 image elements, in-degree = 0 for the other 48.

**[measured] Mean-isometry at every Hamming distance.** Mean contraction ratio d(hu(x),hu(y))/d(x,y) = 1.0000 exactly at every starting distance d=1,...,6. This is algebraically forced: the hu map uses source bits with weights [0,1,2,2,1,0], mean weight = 6/6 = 1.0. By linearity, expected output distance equals input distance.

Variance decreases monotonically with distance: σ=0.82 at d=1 (neighbors scrambled), σ=0 at d=6 (complement pairs perfectly preserved). The 互 map is maximally faithful to complements and maximally noisy at the neighbor scale.

**[measured] Contraction is type-blind.** All 五行 type pairs (克-克, 生-生, 比和-比和, mixed) have mean ratio = 1.0000. The mean-isometry holds uniformly across types.

**[measured] Basin × 五行 completely independent.** Chi-square = 1.11, p = 0.98. The 互 map's basin structure is orthogonal to the 五行 vertex coloring.

| Basin | 比和 | 生 | 克 | Total |
|-------|------|-----|-----|-------|
| 0 | 4 | 5 | 7 | 16 |
| 21 | 3 | 7 | 6 | 16 |
| 42 | 3 | 7 | 6 | 16 |
| 63 | 4 | 5 | 7 | 16 |

**[measured] 克→生 = 0 under 互: strict one-way valve.**

| src\dst | 比和 | 生 | 克 |
|---------|------|-----|-----|
| 比和 | 6 | 4 | 4 |
| 生 | 2 | 4 | 18 |
| 克 | 8 | 0 | 18 |

No 克 hexagram maps to a 生 hexagram under 互. The flow in 五行 type-space is directional: 生 →→ 克 ⇄ 比和, with no return from 克 to 生. 75% of 生 hexagrams map to 克; 69% of 克 hexagrams stay 克.

**Mechanism (from discussion):** Only 2 of 16 middle-bit patterns produce 生 output. The element assignment prevents any 克 input from having those specific middle-bit patterns. This is contingent on the element assignment — a different valid surjection F₂³ → Z₅ could produce a different zero cell or no zero cell.

**[measured] 生 hexagrams are slightly farther from attractors.** Mean distance to nearest attractor: 比和=1.43, 克=1.38, 生=1.67. No 生 hexagram sits at distance 0 from any attractor.

**[measured] Real eigenvalues of P_g × A_{Q₆} are generic.** 1000/1000 random partitions of sizes {14,24,26} produced all-real eigenvalues for all 3 directed matrices. All 6 alternative element assignments also give all-real eigenvalues. This is a structural property of Q₆ + diagonal projections, not specific to 五行. The Probe 1 observation carries no information about the element assignment.

### Structural characterization from discussion

**The 互 map is a geometric isometry that is simultaneously an elemental rectifier.** It preserves mean Hamming distance at every scale (geometric), is basin-blind to 五行 type (p=0.98), yet creates a strict one-way valve in 五行 type-space (克→生 = 0). These are orthogonal properties of the same map.

**The valve is an interaction effect.** Bit compression alone doesn't create directionality (the map is type-blind geometrically). The element assignment alone doesn't create directionality (basins are type-independent). The valve emerges from (bit compression) × (element assignment) together. The existence of a valve may be structural (any valid assignment might produce one), but the specific direction (生 drains) is contingent on the traditional assignment.

**The hinge interpretation.** hu² collapses to bits 2,3 — lines 3,4, the inter-trigram boundary. These are the only bits that appear in both nuclear trigrams. Iterated nuclear extraction preserves only the coupling between upper and lower trigrams, discarding everything else.

---

## Iteration 4: Composed Dynamics + Alternative Assignments (Probe 3)

### Entry Point

Probe 3 from `plan.md` (Q15/Q11). Analyze what happens when line-change transitions compose with the 互 map. Test the hinge prediction: bits 2,3 (lines 3,4) should have privileged status in composed dynamics. Also compute full 3×3 互 transition matrices for all alternative element assignments to determine whether the zero cell is generic or specific.

### Method

**Part A:** Tested 12 labeled element assignments (6 unlabeled partitions × 2 label swaps). For each, computed the 64-hexagram surface relations and the 3×3 五行 transition matrix under 互.

**Part B:** For each of 6 line positions, defined F_k(h) = hu(flip(h, k)). Built the composed adjacency, tested single-step distributions (targets, entropy) for each line, ran the random-line-then-互 Markov chain (stationary distribution, spectral gap, absorbing structure), computed 五行 flow under composition (overall and per-line), and analyzed full orbit structure (fixed points, cycles, basins, transients) for each F_k.

Script: `p3_composed_dynamics.py`. Results: `p3_results.json`.

### Results — Part A

**[measured] The zero cell is NOT generic: only 1 of 6 unlabeled partitions has one.** Of 12 labeled assignments, exactly 2 have a zero cell — and they are the same unlabeled partition with 生/克 labels swapped:
- Assignment 6 (sizes 14/26/24): 生→克 = 0
- Assignment 7 = ACTUAL (sizes 14/24/26): 克→生 = 0

The zero always blocks the 26-element group from reaching the 24-element group. The other 5 unlabeled partitions have no zero cell. The traditional element assignment's partition is structurally special among valid surjections (1/6 probability).

### Results — Part B

**[measured] Every composed map lands on the same 16-element 互 image.** The line flip does not expand the reachable set. Each hexagram reaches exactly 5 distinct targets (2 of 6 lines are "dead" — produce same output as 互 alone).

**[measured] Single-step hinge prediction: NULL.** All 6 lines produce identical output distributions: 16 targets, exactly 4 hexagrams per target, entropy = 4.0 bits. No hinge/outer distinction at this level.

**[measured] Orbit-level hinge prediction: CONFIRMED.** The hinge distinction is qualitative:

| Line | Type | Fixed pts | 2-cycles | Attractor | Basins |
|------|------|-----------|----------|-----------|--------|
| 1 | outer | {0, 63} | {21,42} | 2 fixed + 1 two-cycle | 4 basins (32,32,16,16) |
| 2 | outer | {1, 62} | {20,43} | 2 fixed + 1 two-cycle | 4 basins (32,32,16,16) |
| **3** | **hinge** | **none** | **none** | **single 4-cycle** | **1 basin (all 64)** |
| **4** | **hinge** | **none** | **none** | **single 4-cycle** | **1 basin (all 64)** |
| 5 | outer | {31, 32} | {10,53} | 2 fixed + 1 two-cycle | 4 basins (32,32,16,16) |
| 6 | outer | {0, 63} | {21,42} | 2 fixed + 1 two-cycle | 4 basins (32,32,16,16) |

Hinge lines (3,4) destroy all equilibria — no fixed points, no 2-cycles. They produce a single global 4-cycle that captures ALL 64 hexagrams. Outer lines preserve the 互 attractor structure (2 fixed points + 1 two-cycle, 4 basins).

**Structural explanation:** F₁ = F₆ = hu (bits 0,5 have weight 0 in 互, so flipping them has no effect). F₂ and F₅ shift which bit occupies the boundary but preserve attractor character. F₃ and F₄ flip WITHIN the boundary bits (the only information 互 preserves), destabilizing everything.

**[measured] The F₃/F₄ asymmetry: two flavors of instability.**
- F₃ (line 3, top of lower trigram): 4-cycle 10(生)→31(比和)→53(生)→32(比和) — alternating 生/比和, excludes 克
- F₄ (line 4, bottom of upper trigram): 4-cycle 1(克)→20(克)→62(克)→43(克) — pure 克, excludes 生 and 比和

The two hinge positions are dynamically inequivalent. Line 3 (lower→用, upper→体) produces oscillation between generation and harmony. Line 4 (upper→用, lower→体) produces locked opposition.

**[measured] 克→生 block BREAKS under composition.** The pure-互 zero cell (克→生 = 0) does not survive line-flip composition in aggregate (16 of 384 composed transitions are 克→生). Per-line: lines 1 and 6 preserve the block (they equal hu); lines 2–5 produce nonzero 克→生 counts.

Per-line zero cells vary:
- Lines 1, 6: 克→生 = 0 (same as pure 互)
- Line 2: 比和→生 = 0
- Line 3: 生→生 = 0
- Line 4: no zero cell
- Line 5: 比和→生 = 0

**[measured] Markov chain (random-line-then-互) converges to 12 absorbing states.** Spectral gap = 1/3, mixing time = 3 steps. Stationary distribution uniform over the 12 absorbing states (1/12 each).

The 12 absorbing states = {a ⊕ v : a ∈ {0, 21, 42, 63}, v ∈ {0, e₁, e₆}} — the 互 attractor thickened by single outer-bit flips. The 4 excluded image elements are the double outer-bit flips (both lines 1 and 6 flipped simultaneously).

Stationary 五行 composition: 比和 = 33.3% (4 states), 生 = 16.7% (2 states), 克 = 50.0% (6 states). 生 is depleted to half its size-proportional share.

### Structural observations from discussion

**Stage vs drama framing.** Across Probes 1–3, a consistent pattern: the algebra creates the stage (Q₆ structure, 互 map, path partition, 1:2:3 ratio), while the element assignment creates the drama (which types flow where, which zero cells exist, which cycles are 克-locked vs oscillating). Every "interesting" finding about 五行 dynamics is contingent on the assignment, not forced by the algebra.

**The inter-trigram boundary has two dynamically inequivalent sides.** The 互 map treats lines 3 and 4 symmetrically (both contribute equally to both nuclear trigrams), but composed dynamics (F₃ vs F₄) breaks this symmetry through the 体/用 distinction. This positional asymmetry is a property of the hexagram structure made visible through composition.

**The absorbing set as tolerance neighborhood.** The 12-state Markov absorbing class is the 互 attractor plus single outer-bit deviations. The composed system preserves hinge information plus one bit of outer context, but not two simultaneous outer-bit flips.

### What was not tested

- The Wood-exclusion mechanism: whether the traditional assignment is the only one where the 互 image excludes a single element entirely (testable explanation for the 1/6 valve)
- Symbolic dynamics / shift space properties of walks on the 五行 subgraphs (→ Probe 4)
- Transfer matrix walk growth, topological entropy, and φ role (→ Probe 5)
- Entropy comparison across all 6 alternative partitions (stage vs drama test for continuous invariants)
- Bifurcation frequency comparison to known dynamical systems (→ Probe 6)

---

## Iteration 5: Symbolic Dynamics, Transfer Matrices, and Stage-vs-Drama Test (Probes 4+5)

### Entry Point

Probes 4 and 5 from `plan.md` (Q11/Q13/Q14/Q15), combined. Characterize the symbolic dynamics of 五行-labeled walks, verify the Fibonacci/Lucas structure of 克 walks at the trigram level, test whether it lifts to the hexagram level, and resolve the stage-vs-drama question: which dynamical properties are forced by the algebra vs contingent on the element assignment?

Also: test the Wood-exclusion mechanism for the zero cell (minority hypothesis).

### Method

**Part 1 (Symbolic dynamics):** Built the 3×3×3 tensor of two-step type transitions (all 2304 length-2 paths). Computed the 3×3 type Markov transition matrix, its eigenvalues, and stationary distribution. Computed topological entropy h_top = log(ρ(A)) for each subgraph in three modes (OR-symmetrized, AND-symmetrized, directed). Computed closed walk counts tr(A^n) for n=1..20.

**Part 2 (Transfer matrices):** Verified exact closed-form identities for trigram-level walk counts. Computed hexagram-level walk counts and tested for recurrence structure. Extracted characteristic polynomial of A_克^{OR} and identified φ eigenvalues.

**Part 3 (Stage vs drama):** For all 6 unlabeled alternative assignments, built OR-symmetrized subgraphs, computed spectral radii, entropies, and spectral gaps. Tested whether entropy and gap orderings are invariant across assignments.

**Part 4 (Wood exclusion):** For each assignment, computed element distribution in the 互 image and correlated with zero-cell existence.

Script: `p45_symbolic_transfer.py`. Results: `p45_results.json`.

### Results — Part 1: Symbolic Dynamics

**[measured] No forbidden two-step type sequences.** All 27 possible (g₁, g₂, g₃) triples have nonzero counts across the 2304 length-2 paths. The 五行-labeled transition graph is a full shift at length 2. No forbidden words exist at this scale.

**[measured] Stationary distribution = size-proportional, exactly.** The 3×3 type Markov chain has stationary distribution (14/64, 24/64, 26/64), matching the type frequencies exactly. This is forced by Q₆ being 6-regular: in any regular graph, the random walk's stationary distribution is uniform over vertices, so projection onto any partition gives proportional weights. Not a finding about 五行.

Eigenvalues of the type Markov matrix: {1.0, −0.181, 0.068}. Fast mixing (gap ≈ 0.82).

**[measured] Topological entropy hierarchy flips between symmetrization modes.**

| Subgraph | 比和 | 生 | 克 | Q₆ |
|----------|------|-----|-----|------|
| OR-sym | 1.298 | 1.503 | **1.545** | 1.792 |
| AND-sym | 0.693 | **1.029** | 0.828 | — |
| Directed | 0.693 | **1.029** | 0.828 | — |

OR: 克 > 生 > 比和. AND/directed: 生 > 克 > 比和. The AND and directed modes have identical spectral radii because the symmetric part of P_g × A_{Q₆} equals A_g^{AND}.

**[measured] All subgraphs are bipartite.** N_n = 0 for all odd n across all three subgraphs and Q₆. The even/odd weight partition (bit parity) is respected by all 五行 edges. Forced by Q₆ structure (every edge flips exactly one bit).

### Results — Part 2: Transfer Matrices and φ

**[measured] Trigram-level closed walk counts — exact closed forms verified for n=1..20.**

| Type | Closed walks (even n) | Growth rate | Form |
|------|----------------------|-------------|------|
| 克 | 4·L_n (Lucas numbers) | φ^n | Fibonacci recurrence |
| 生 | 4·2^(n/2) | (√2)^n | Exponential doubling |
| 比和 | 4 (constant) | 1 | No growth |

The 克 trigram subgraph is a Fibonacci machine: its closed walk counts are exactly 4× Lucas numbers {4, 12, 28, 72, 188, 492, 1288, ...}. These satisfy the Fibonacci recurrence L_{n+2} = L_{n+1} + L_n, forced by P₄'s eigenvalues {±φ, ±1/φ}.

**[measured] Fibonacci structure does NOT lift to the hexagram level.** The hexagram-level 克 walk ratio N_{n+2}/N_n converges slowly to ρ² ≈ 21.98 (squared spectral radius) via a degree-46 polynomial recurrence, not a clean Fibonacci/Lucas recurrence. The fiber bundle structure (non-product lift) destroys the trigram-level algebraic cleanness.

**[measured] φ survives explicitly in the hexagram 克 spectrum.** The OR-symmetrized 克 subgraph has eigenvalues ±2φ ≈ ±3.236 and ±2/φ ≈ ±1.236 (multiplicity 1 each). These are exactly the trigram P₄ eigenvalues doubled (2×{±φ, ±1/φ}), representing the "pure product" modes where both trigrams are in the same eigenstate.

The "mixed" product eigenvalue ±(φ + 1/φ) = ±√5 does NOT appear — it is destroyed by the fiber bundle coupling. The non-product interaction preserves aligned trigram modes while destroying misaligned ones. φ survives the lift only in the coherent sector.

### Results — Part 3: Stage vs Drama

**[measured] Entropy ordering follows group SIZE (stage-level).** Across all 6 alternative assignments, the 26-element group always has the highest entropy (~1.545), the 24-element group is second (~1.503), the 14-element group is last (~1.298). When 生 and 克 swap group sizes between assignment classes, their entropies swap correspondingly.

**[measured] Spectral gap ordering follows 五行 LABEL (derived stage property).** The ordering 生 > 克 > 比和 holds for ALL 6 assignments, regardless of whether 生 has 24 or 26 vertices.

- Class A (4 assignments, 生=24 vertices): gaps 比和=0.425, 生=0.882, 克=0.724
- Class B (2 assignments, 生=26 vertices): gaps 比和=0.425, 生=0.967, 克=0.641

The gap tracks the 五行 label, not the size. This is because the unique surjection F₂³ → Z₅ forces 生↔P₃ and 克↔P₄ invariantly (P₃ has a larger spectral gap than P₄), and this assignment is preserved under element permutation due to the complement-respecting rigidity of the surjection. The gap ordering is a theorem about the unique surjection interacting with the Z₅ cycle structure, not a contingent property of the element assignment.

### Results — Part 4: Wood Exclusion / Minority Hypothesis

**[measured] The minority hypothesis for the zero cell is confirmed.** A zero cell in the 互 transition matrix appears if and only if one type has ≤ 2 hexagrams in the 16-element 互 image.

| Assignment | Image distribution (比和:生:克) | Zero cell |
|------------|-------------------------------|-----------|
| 1 | 4:6:6 | none |
| 2 | 4:5:7 | none |
| 3 | 4:5:7 | none |
| 4 | 4:6:6 | none |
| 5 | 4:8:4 | none |
| **6 (actual)** | **4:10:2** | **克→生 = 0** |

Only the traditional assignment produces the extreme imbalance (10:2 between the two non-比和 types) needed for a zero cell. The complete causal chain: element assignment → bit constraint on 互 image → type imbalance (≤2 targets of one type) → zero cell in transition matrix → one-way valve.

### Structural synthesis from discussion

**Stage vs drama decomposition (complete):**
- **Stage** (forced by algebra): entropy-by-size, bipartiteness, Chebyshev sequence, mean-isometry, stationary = proportional, no forbidden two-step words
- **Derived stage** (forced by unique surjection × Z₅ cycle): spectral gap ordering 生 > 克 > 比和, path assignment 生↔P₃ / 克↔P₄
- **Drama** (contingent on traditional assignment): zero cell and one-way valve (1/6 of partitions), F₃/F₄ asymmetry's specific type content, specific flow direction (生 drains to 克)
- **Interaction** (bit compression × element assignment): the valve mechanism, coherent φ survival through fiber bundle

**The coherent sector:** φ survives the non-product lift from trigram to hexagram only in the aligned modes (2φ, 2/φ). The misaligned mode (√5 = φ + 1/φ) is destroyed by the fiber bundle coupling. The fiber bundle selects for trigram coherence.

### What was not tested

- Spectral dimension from return probabilities (→ Probe 7)
- Comparison to ~16-dim semantic manifold via discretization bounds
- Literature comparison of the structural fingerprint to known dynamical regime classifications (→ Probe 6)
- External data comparison (actual situational dynamics vs I Ching structure)

---

## Iteration 6: Spectral Dimension + Null Space Architecture (Probe 7)

### Entry Point

Probe 7 from `plan.md` (Q14). Compute spectral dimension of the 五行 subgraphs, compare dimensional measures to the ~16-dim semantic manifold (R254-R256), and synthesize the dimensional picture across all probes.

### Method

Computed return probabilities P(n) = tr(A^n)/(N·ρ^n) for even n=2..40 across all subgraphs. Attempted spectral dimension fitting (log-log regression). Computed ranks, nullities, and null space intersections of the three OR-symmetrized 五行 subgraphs. Decomposed the triple null and common range in terms of Walsh weight.

Script: `p7_dimension.py`. Results: `p7_results.json`.

### Results

**[measured] Spectral dimension fitting is meaningless for finite graphs.** Return probabilities converge to 2/N (bipartite limit) rather than decaying as n^{-d_s/2}. Fitted values (~1.0–1.5) reflect convergence rates. Q₆ fits to d_s=0.87, far below its actual dimension 6. Discarded as an approach.

**[measured] Rank hierarchy: 克(46) > 生(44) = Q₆(44) > 比和(26).**

克 has MORE independent spectral modes than Q₆ itself (46 vs 44). OR-symmetrization adds edges from both directions, creating 2 extra modes. 比和 has rank 26, leaving 38 null dimensions — more than half the space is invisible to 比和.

**[measured] Q₆'s null space is exactly the weight-3 Walsh eigenspace (dim 20).** Q₆ eigenvalue 0 has multiplicity C(6,3) = 20. This is the same space where the semantic manifold lives (R254-R256). The thematic manifold occupies precisely the modes that the transition graph annihilates.

**[measured] Null space intersection architecture.**

| | 比和 | 生 | 克 | Q₆ |
|---|---|---|---|---|
| 比和 | 38 | 7 | 5 | 14 |
| 生 | 7 | 20 | 5 | 10 |
| 克 | 5 | 5 | 18 | 9 |
| Q₆ | 14 | 10 | 9 | 20 |

- Triple null (intersection of all three): dim = 5, fully contained in Q₆'s null space (weight-3)
- This partitions the 20-dim weight-3 space into: 5 universally invisible dimensions + 15 differentially visible dimensions (visible to at least one 五行 type)

**[measured] Common range of all three subgraphs: dim = 3.** Composed of weight-{1,5} Walsh modes (complement-paired eigenspaces of Q₆, eigenvalues ±4). These are the only directions that ALL three 五行 types propagate.

**[measured] Full 64-dim decomposition:** 3 universal modes (weight-{1,5}) + 5 universally invisible modes (triple null, in weight-3) + 56 differentially visible modes.

**[measured] 互 dimensional reduction: 64 → 16 → 4 states (6 → 4 → 2 bits).** The bit-layer structure [0,1,2,2,1,0] organizes as three concentric pairs: outer (bits 0,5, discarded immediately), middle (bits 1,4, survive one step), hinge (bits 2,3, survive to attractor).

### Key observation from discussion

**The 15 ≈ ~16 near-match.** The semantic manifold has ~16 effective dimensions (R254-R256). The weight-3 space partitions into 5 triple-null directions (invisible to all transition types) + 15 visible directions (visible to at least one type). If the semantic manifold concentrates its variance in the 15 visible directions (avoiding the 5 triple-null directions), this would be the first spectral-level bridge between the transition structure and the text — operating at a different level than the vertex-level nulls (R192, R209, R253).

**The text-in-null-space property is forced by the complement involution.** The complement involution structures both the text (R254-R256) and the graph (complements at Hamming distance 6). Weight-3 is the natural spectral scale for opposition structure. The significance is methodological (enables spectral decomposition of the text-graph interface) rather than independently substantive.

### What was not tested

- Triple-null projection test: does the semantic manifold avoid the 5 universally invisible weight-3 directions?
- Cross-model validation of the triple-null test (E5-large, SikuRoBERTa)
- Literature comparison of the structural fingerprint (Probe 6)
- External data comparison

---

## Iteration 7: Triple-Null Projection Test (Probe 8)

### Entry Point

The highest-value test remaining from the Probe 7 discussion. The weight-3 Walsh eigenspace (dim 20) partitions into 5 triple-null directions (invisible to ALL three 五行 OR-symmetrized subgraphs) + 15 visible directions (in the range of at least one subgraph). The semantic manifold has ~16 effective dimensions in weight-3. Question: does the manifold avoid the 5 invisible directions, concentrating in the 15 visible ones?

### Method

Built the three OR-symmetrized 64×64 五行 adjacency matrices. Computed null spaces via SVD. Found the triple intersection (5-dim, verified fully within weight-3, max residual 3.89e-16). Split weight-3 into V_invisible (5-dim triple null) and V_visible (15-dim complement). Loaded cached hex-level embeddings for BGE-M3, E5-large, and SikuRoBERTa. Projected centered embeddings onto weight-3, then partitioned variance between V_invisible and V_visible. Permutation null: 10,000 hexagram-label shuffles.

Script: `p8_triple_null_test.py`. Results: `p8_results.json`.

### Results

**[measured] The semantic manifold does NOT avoid the triple-null directions. Cleanly null across models.**

| Model | f_invisible | Expected | Percentile | Verdict |
|-------|-------------|----------|-----------|---------|
| BGE-M3 | 0.2445 | 0.2500 | 35.5th | Null |
| E5-large | 0.2413 | 0.2500 | 25.3rd | Null |
| SikuRoBERTa | 0.2854 | 0.2500 | 96.8th | Anti-aligned |

The two modern models distribute weight-3 variance uniformly across visible/invisible directions (f_invisible ≈ 25% = 5/20), indistinguishable from random label assignment. SikuRoBERTa puts slightly MORE variance in invisible directions (28.5%, p ≈ 0.03), suggesting mild anti-alignment if anything.

**[measured] The 15 ≈ ~16 near-match is coincidence.** The manifold's ~16 effective dimensions are unrelated to the 15 visible directions. The two structures coexist in weight-3 but are independently organized.

**[measured] Per-dimension breakdown shows no preferential alignment.** The most invisible Walsh directions have f_invisible = 0.625 (partially invisible), not 1.0 — the triple null is a rotated subspace, not spanned by individual Walsh basis vectors. The 4 most invisible directions correspond to "block" weight-3 patterns ({000111}, {011100}, {111000}, {100011}). Overlap between lowest-variance Walsh directions and most-invisible directions: 3/5 (p ≈ 0.14, not significant).

**[measured] Full triple null (all weights): also null.** Total-variance fractions in the 5-dim triple null: BGE-M3 = 8.22%, E5-large = 7.90%, SikuRoBERTa = 8.98% (expected 7.81% = 5/64). Consistent with uniform.

### Synthesis: Three levels of null

This probe completes a three-level test of whether the 五行 transition structure connects to the semantic manifold:

1. **Vertex level** (R192, R209, R253): 五行 type carries no semantic signal
2. **Flow level** (R253): Laplacian divergence on Q₆ has no semantic structure
3. **Spectral level** (this probe): visible/invisible mode partition has no semantic correlate

All null. The 五行 decomposition and the semantic manifold are independently organized on the same lattice.

### Structural conclusion from discussion

**The complement involution is a shared constraint, not a bridge.** σ(h) = 63−h is a symmetry of Q₆ that constrains both text (antisymmetric → weight-3 concentration) and graph (null at weight-3). These are parallel responses to the same substrate symmetry, not causally connected. The text fills weight-3 because it's the largest antisymmetric eigenspace; the graph is null at weight-3 because of Q₆'s eigenvalue structure. The text-in-null-space property is a corollary, not evidence of interaction.

### What was not tested

- External matching: does the I Ching's transition structure correspond to any known dynamical system? (Q11, literature)
- Bifurcation frequency comparison: does 1:2:3 match real dynamical systems? (Q12, literature + external data)
- Non-五行 transition dynamics: does the Q₆ graph structure connect to text INDEPENDENTLY of 五行? (Partially addressed by Laplacian null, but only one operationalization tested)

---

## Final Synthesis

### Central finding

The I Ching's transition graph (Q₆ decorated by 五行 type and composed with the 互 map) has rich internal dynamical structure — Fibonacci machines, one-way valves, hinge attractors, fiber bundles with coherent sectors — that is completely disconnected from the semantic content of the text.

The bare graph (Q₆ without 五行 decoration) connects to the text through the complement involution, which is a shared symmetry of the substrate. The decorated graph does not. The disconnection is between the 五行 decoration and the text, not between the substrate and the text.

### The stage/drama decomposition

The investigation's deepest structural contribution: a clean separation between what the algebra forces and what the element assignment contributes, discovered by systematic testing across 6 alternative assignments.

- **Stage** (forced): entropy-by-size, bipartiteness, Chebyshev sequence, mean-isometry, stationary = proportional, no forbidden two-step words
- **Derived stage** (forced by unique surjection × Z₅ cycle): spectral gap ordering 生 > 克 > 比和, path assignment 生↔P₃ / 克↔P₄
- **Drama** (contingent on traditional assignment): zero cell and one-way valve (1/6 probability), F₃/F₄ asymmetry type content, specific flow direction (生 drains to 克)
- **Interaction** (bit compression × element assignment): the valve mechanism, coherent φ survival through fiber bundle

### Three-level null

The 五行 transition structure and the semantic manifold are independently organized on Q₆:
1. **Vertex level** (R192, R209, R253): 五行 type carries no semantic signal
2. **Flow level** (R253): graph Laplacian has no semantic structure
3. **Spectral level** (R269): visible/invisible mode partition within weight-3 has no semantic correlate

The complement involution is a shared constraint (symmetry of Q₆), not a bridge between them.

### What remains

- Q11: external matching of the structural fingerprint (Chebyshev, Fibonacci, 1:2:3, weak-tie topology) against known dynamical systems
- Q12: bifurcation frequency comparison (1:2:3 ratio vs real dynamical systems)
- Non-五行 graph dynamics (other operationalizations beyond Laplacian)
- External data comparison
