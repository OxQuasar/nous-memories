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

---

## Iteration 8: Golden Mean Shift Identification (Probe A — Fingerprint Investigation)

### Entry Point

Probe A from the fingerprint investigation (`plan.md`). The 克 trigram subgraph has topological entropy log φ, same as the golden mean shift (GMS — the simplest non-trivial shift of finite type, defined by forbidding "11"). R265 established that 克 trigram walk counts are exactly 4×Lucas numbers. This iteration asks: what is the precise structural relationship between P₄ walks and the golden mean shift?

### Method

**Part 1 (Trigram topology):** Printed the explicit graph (vertices, edges, components) for each trigram subgraph. Confirmed the 2×P₂, 2×P₃, 2×P₄ decomposition and identified which trigrams sit on which path.

**Part 2 (Forbidden words):** Treated walks on each trigram subgraph as vertex shifts. Enumerated forbidden 2-letter words (= non-edges). Tested whether any additional forbidden words of length 3+ exist beyond those implied by length-2 (= are these 1-step SFTs?).

**Part 3 (GMS comparison):** Compared P₄ to the GMS across five dimensions:
- 3a: Periodic orbit counts tr(A^n) for both systems
- 3b: Zeta function factorization det(I - zA)
- 3c: Higher block presentations of GMS vs P₄
- 3d: Edge shift comparison
- 3e: Bipartite square root — A² restricted to bipartition classes

**Part 4 (Hexagram-level entropy decomposition):** Decomposed hex-level 克 topological entropy into coherent (φ-related eigenvalues) and incoherent sectors.

Script: `probeA_golden_mean.py`. Results: `probeA_results.json`.

### Results — Part 1: Trigram Subgraph Topology

**[confirmed] All three subgraphs are exactly as predicted:**

| Group | Edges | Components | Topology |
|-------|-------|------------|----------|
| 比和  | 2     | 6 (4 isolated) | 2×P₂: Kun☷—Dui☱, Gen☶—Qian☰ |
| 生    | 4     | 4 (2 isolated) | 2×P₃: Zhen☳—Li☲—Dui☱, Gen☶—Kan☵—Xun☴ |
| 克    | 6     | 2              | 2×P₄: Kan☵—Kun☷—Zhen☳—Gen☶, Dui☱—Xun☴—Qian☰—Li☲ |

克 uses all 8 vertices with no isolates — the only fully connected subgraph.

### Results — Part 2: Forbidden Words

**[measured] All trigram subgraphs are 1-step SFTs.** No additional forbidden words exist beyond the forbidden 2-letter words (non-edges). The symbolic dynamics is fully determined by the adjacency structure.

| System | Vertices | Forbidden 2-words | Self-loops |
|--------|----------|-------------------|------------|
| P₄ (abstract) | 4 | 10 | 0 |
| 2×P₄ (克) | 8 | 52 | 0 |
| 2×P₂ (比和) | 8 | 60 | 0 |
| 2×P₃ (生) | 8 | 56 | 0 |
| GMS | 2 | 1 ("11") | 1 |

Key structural contrast: GMS has a self-loop; P₄ has none. This is the source of the bipartite/non-bipartite difference.

### Results — Part 3: GMS Comparison

**[measured] P₄ and GMS are NOT topologically conjugate.** Periodic orbit counts differ: GMS tr(M^n) = L_n (Lucas numbers for all n); P₄ tr(A^n) = 2L_n for even n, 0 for odd n (bipartite). Different trace sequences → different periodic orbit structure → not conjugate.

**[measured] Zeta function factorization — the central structural result.**

det(I - zA_{P₄}) = 1 - 3z² + z⁴ = (1 - z - z²)(1 + z - z²)

- **(1 - z - z²)** is exactly the GMS zeta denominator
- **(1 + z - z²)** is the "anti-GMS" (z → −z parity twist)
- Therefore: **ζ_{P₄}(z) = ζ_{GMS}(z) × ζ_{anti-GMS}(z)**

The GMS zeta function is an exact factor of the P₄ zeta function. This is an instance of the Artin formalism for Z₂-covers: for any bipartite graph (= Z₂-cover of its quotient), ζ factors as ζ_{base} × L(z,χ) where χ is the sign character.

**[measured] Higher block presentations do not match.** GMS[2] (2-block recoding) has spectrum {φ, -1/φ, 0} — 3 eigenvalues. P₄ has spectrum {±φ, ±1/φ} — 4 eigenvalues. Not a block recoding relationship.

**[measured] Bipartite square root — confirmed.** P₄ bipartition: even={0,2}, odd={1,3}.
- A²|_odd = M²_GMS = [[2,1],[1,1]] (exact matrix equality)
- A²|_even = [[1,1],[1,2]] (transpose of M²_GMS)
- Both have spectrum {φ², 1/φ²} — identical to M²_GMS

**P₄ is the bipartite double cover of the golden mean shift.** The folding map (collapsing bipartition classes) is a topological factor map from P₄ to GMS. The zeta function factorization encodes this: P₄ dynamics decompose into GMS (even parity) × anti-GMS (odd parity).

### Results — Part 4: Hexagram-Level Entropy Decomposition

**[measured] Coherent sector accounts for 76% of entropy but does not dominate the spectral radius.**

| Sector | ρ | h_top | Fraction of total |
|--------|---|-------|-------------------|
| Total (64×64) | 4.6885 | 1.5451 | 100% |
| Coherent (±2φ, ±2/φ) | 3.2361 = 2φ | 1.1744 = log(2)+log(φ) | 76.0% |
| Incoherent (other 60 eigs) | 4.6885 | 1.5451 | dominant |

The spectral radius is dominated by incoherent modes (ρ_incoherent = 4.69 > ρ_coherent = 3.24). Long-time hex-level dynamics are NOT controlled by the GMS structure.

**[measured] Tensor eigenvalue survival is selective.** Of 9 distinct tensor eigenvalue types (sums λ_i + λ_j from trigram P₄ spectrum), only 5 survive into the hex spectrum: ±2φ, ±2/φ, 0. The destroyed eigenvalues are ±√5 = ±(φ+1/φ) and ±1 = ±(φ-1/φ) — exactly the cross-magnitude modes where the two trigrams resonate at different eigenvalue magnitudes.

### Discussion findings

**The hierarchy {trivial, full, GMS} is algebraically forced (sage).** The unique surjection F₂³ → Z₅ forces edge partition {2,4,6} → paths {P₂, P₃, P₄}. Each P_n is a bipartite double cover:
- 比和 (P₂) → trivial fixed point (single vertex with self-loop, ρ=1)
- 生 (P₃) → full 2-shift (everything allowed, ρ=2)
- 克 (P₄) → golden mean shift (forbids "11", ρ=φ)

The Chebyshev sequence {1, √2, φ} = {√1, √2, √(φ²)} are square roots of the base shift spectral radii. This is stage-level: no freedom in which hierarchy appears.

**Same-magnitude resonance filter (sage).** The fiber bundle coupling at the hex level preserves tensor eigenvalues where both trigrams resonate at the same magnitude (φ+φ=2φ, 1/φ+1/φ=2/φ) and destroys cross-magnitude modes (φ+1/φ=√5). The destroyed √5 = tr(M_GMS) — the hex level cannot linearly access the trace of the underlying GMS matrix. This filter is unique to 克: 生 has only one nonzero magnitude (√2), so there's nothing to filter; 比和 is trivially magnitude-matched.

**The zeta factorization parallels number theory (sage).** The factorization ζ_{P₄} = ζ_{GMS} × L(z,χ) parallels ζ_{Q(√5)}(s) = ζ(s) × L(s, (5/·)) in algebraic number theory. The anti-GMS factor is the L-function of the Z₂-covering. This is standard Artin formalism for graph zeta functions (Stark-Terras, Bartholdi), but specific here because the base is the GMS — a dynamical object rather than a symmetric graph.

### New results

→ R270: P₄ = bipartite double cover of the GMS. ζ_{P₄} = ζ_{GMS} × ζ_{anti-GMS}. Confirmed by zeta factorization and bipartite square root (A²|_odd = M²_GMS exactly).

→ R271: The hierarchy {trivial, full, GMS} is algebraically forced. The unique surjection F₂³ → Z₅ forces {P₂, P₃, P₄}, which are bipartite double covers of the only three SFTs that arise. Stage-level.

→ R272: Same-magnitude resonance filter at hex level. The 五行 coupling preserves same-magnitude tensor modes (±2φ, ±2/φ) and destroys cross-magnitude modes (±√5, ±1). The destroyed √5 = tr(M_GMS). This filter is non-trivial only for 克 (two distinct eigenvalue magnitudes).

### What was not tested

- Does 互 respect the bipartite parity of the 克 subgraph? (bridge to Probe B)
- Hex-level zeta factorization — what symmetry group organizes the 64 eigenvalues?
- Incoherent eigenvector characterization — where do the dominant non-GMS modes concentrate?
- The same-magnitude filter for 生 and 比和 at the hex level (expected trivially satisfied)
- 互 as formal renormalization: semigroup, entropy monotonicity, fixed-point structure (Probe B)
- Chebyshev spacing genericity: is {P₂, P₃, P₄} the only consecutive path triple that fits Q₃? (Probe C)

---

## Iteration 9: 互 as Renormalization (Probe B — Fingerprint Investigation)

### Entry Point

Probe B from the fingerprint investigation (`plan.md`), entered via the bridge question from Probe A: does the 互 map respect the bipartite parity of the 克 subgraph? If so, 互 descends to the GMS quotient and is a renormalization on the golden mean shift. Also: formal RG properties (semigroup, entropy monotonicity, conserved quantities, fixed-point linearization) and the bit-weight kernel [0,1,2,2,1,0] as decimation scheme.

### Method

**Part 1 (Parity descent):** For each hexagram, computed the bipartite parity class of its lower and upper trigrams within the two P₄ components of the 克 subgraph. Built the 4×4 parity transition matrix under 互: (pL_in, pU_in) → (pL_out, pU_out).

**Part 2 (Formal RG):**
- 2a: Iterated the semigroup {hu, hu², hu³, ...}. Counted distinct maps.
- 2b: Computed Shannon entropy of the pushforward distribution under iterated hu, starting from uniform on 64 states. Also computed entropy of the 3-state 五行 type marginal.
- 2c: Tested conserved quantities: popcount, Walsh coefficients (all 64), mean Hamming distance.
- 2d: Linearized hu and hu² near each fixed point {0, 21, 42, 63}. Classified perturbations as relevant (grow) or irrelevant (shrink).

**Part 3 (Bit-weight kernel):**
- 3a: Characterized 互 as bit routing σ = [1,2,3,2,3,4] rather than arithmetic.
- 3b: Computed the routing matrix R and its powers R², R³.
- 3c: Verified the conveyor belt structure: outer→middle→hinge with hinge swap.

Script: `probeB_renormalization.py`. Results: `probeB_results.json`.

### Results — Part 1: Parity Descent

**[measured] 互 maximally scrambles P₄ bipartite parity.** The 4×4 parity transition matrix is perfectly uniform: every input parity class (pL, pU) maps to every output class with exactly 4/16 = 25% probability. No parity is preserved, swapped, or correlated in any way.

**Mechanism:** 互 shifts the trigram window inward by 1 bit. The output lower trigram L' = [b₁, b₂, b₃] mixes bits from both the original lower and upper trigrams. Since parity depends on element identity (position in the P₄ graph), the 1-bit shift generically scrambles parity.

**Consequence:** The GMS and anti-GMS sectors (from Probe A's zeta factorization) are fully coupled by 互. The 互 map does NOT act as renormalization on the golden mean shift. It acts on a different structural axis.

### Results — Part 2: Formal RG Properties

**[measured] Semigroup: {hu, hu², hu²} with hu² idempotent.**
- 3 distinct maps total. hu⁴ = hu², hu⁵ = hu³, alternating thereafter.
- Image sizes: hu: 64→16, hu²: 64→4, hu³: 64→4 (same 4 fixed points).
- hu² ∘ hu² = hu² (idempotent — the RG "terminates" at the IR fixed point).

**[measured] Entropy decreases monotonically: exactly −2 bits/step.**

| Step | Support | H(state) bits | H(type) bits |
|------|---------|---------------|--------------|
| 0 | 64 | 6.000 | 1.538 |
| 1 | 16 | 4.000 | 1.299 |
| 2 | 4 | 2.000 | 1.000 |
| 3+ | 4 | 2.000 | 1.000 |

Final type distribution: 比和=32, 克=32. 生 is completely eliminated — consistent with the one-way valve (R262).

**[measured] 61/64 Walsh coefficients preserved.** The 3 broken modes are {001010, 010100, 011110} — weights {2, 2, 4}. These form a closed group under XOR and detect exactly the middle↔hinge rearrangement. The 3 modes go from 0→64 under the pushforward, concentrating mass onto the attractor subspace. No connection to the weight-3 triple null (R268).

**[measured] Universal relevant/irrelevant decomposition at all 4 fixed points.**
- Relevant: bits 2, 3 (hinge pair) — perturbations grow under hu²
- Irrelevant: bits 0, 1, 4, 5 (outer + middle) — perturbations die under hu²
- Identical at every fixed point {0, 21, 42, 63}

**[measured] Phase classification by hinge parity:** {0, 63} are true fixed points (b₂ = b₃, swap-invariant). {21, 42} are period-2 (b₂ ≠ b₃, exchanged by the hinge swap hu|_hinge = swap(b₂, b₃)).

### Results — Part 3: Bit-Weight Kernel

**[measured] 互 is bit routing, not arithmetic.** output[i] = input[σ(i)] where σ = [1,2,3,2,3,4]. The "weights" [0,1,2,2,1,0] are multiplicity counts (how many output positions each input bit feeds), not filter coefficients.

**[measured] Routing matrix R has rank 4 → 2 under iteration.** R: rank 4 (6→4 effective reduction). R²: rank 2 (only bits 2,3 survive). R³ = R^∞: rank 2 (stable). Column sums: R=[0,1,2,2,1,0], R²=[0,0,3,3,0,0].

**[measured] 3-level conveyor belt with swap, verified for all 64 hexagrams:**
- outer_out = middle_in ✓ (layer shifts inward)
- middle_out = hinge_in ✓ (layer shifts inward)
- hinge_out = swap(hinge_in) ✓ (b₂, b₃ swap positions)

### Discussion findings

**互 is a block-spin RG at scale factor 2 on a 2-dimensional system (sage).** The hexagram has 6 bits organized as 3 layers of 2 (one per trigram): outer {0,5}, middle {1,4}, hinge {2,3}. 互 discards 1 layer per step. Entropy loss = d·log₂(b) = 2·log₂(2) = 2 bits/step, matching the standard formula where d=2 (upper/lower trigram dimensions) and b=2 (halving resolution). Stage-level — forced by the 2×3 geometry.

**Edge-type and bit-layer are complementary decompositions (sage).** The edge-type axis (五行 → GMS/shift spaces) classifies transitions by *kind*. The bit-layer axis (互 → conveyor belt) classifies structure by *depth*. "Kind of change" and "depth of change" are independent variables. The maximal parity scrambling is the proof of this independence. In standard RG terms: the GMS is a feature of the "Hamiltonian"; 互 is the RG transformation acting on Hamiltonian space. That they decouple is the normal RG relationship.

**The 3 broken Walsh modes have no connection to the triple null (sage).** Weights {2, 2, 4} vs weight-3 for the triple null. The Walsh modes broken by 互 and the modes invisible to 五行 live in different weight subspaces. Another axis of orthogonality.

**The conveyor belt is stage-level (sage).** The routing σ = [1,2,3,2,3,4] is defined by 互's construction (nuclear trigrams), which is pure combinatorics, no 五行 input. What changes across assignments: which 五行 type is eliminated at the attractor (drama, 1/6 contingent).

### New results

→ R273: 互 is a block-spin RG at scale factor 2 on a 2-dimensional system. Entropy loss = d·log₂(b) = 2 bits/step. Conveyor belt terminates in 2 steps. Semigroup {hu, hu², hu²} with hu² idempotent. Stage-level.

→ R274: 互 maximally scrambles P₄ bipartite parity (uniform 4×4 transition matrix). The edge-type axis (五行 → GMS) and the bit-layer axis (互 → conveyor belt) are orthogonal decompositions of Q₆.

→ R275: Universal relevant/irrelevant decomposition. 2 relevant (hinge bits 2,3) + 4 irrelevant (outer+middle) at every fixed point. Phases classified by hinge parity.

→ R276: 互 preserves 61/64 Walsh coefficients. The 3 broken modes {001010, 010100, 011110} (weights {2,2,4}) detect the middle↔hinge rearrangement. No connection to the weight-3 triple null.

### What was not tested

- Chebyshev spacing genericity: is {P₂, P₃, P₄} the unique partition of Q₃'s 12 edges into consecutive paths? (Probe C)
- Probe D: characterization of all 6 assignments' irreversibility properties
- Probe E (synthesis): reframed as "what does the perpendicular pair {edge-type, bit-layer} correspond to?"
- Hex-level zeta factorization: what symmetry group organizes the 64 eigenvalues?
- Incoherent eigenvector characterization: where do the dominant non-GMS modes concentrate?

---

## Iteration 10: Chebyshev Spacing Genericity (Probe C — Fingerprint Investigation)

### Entry Point

Probe C from the fingerprint investigation (`plan.md`). R271 claimed the hierarchy {trivial, full, GMS} is "algebraically forced" by the unique surjection F₂³ → Z₅. This iteration tests: is the 2×{P₂, P₃, P₄} topology actually forced, or does it require additional constraints?

### Method

**Part 1 (Edge partition enumeration):** Enumerated all 3-colorings of Q₃'s 12 edges with color-class sizes {2,4,6} such that each color class is a union of vertex-disjoint paths. Classified by topology type.

**Part 2 (Spectral radii):** For each valid partition, computed spectral radii of the three color classes. Identified which partitions produce the Chebyshev sequence {1, √2, φ}.

**Part 3 (Z₅ forcing):** For all 120 complement-respecting Z₅ assignments, computed the induced edge partition and classified its topology. Tested whether {2,4,6} edge counts and 2×{P₂,P₃,P₄} topology are forced.

**Part 4 (Consecutive triples):** Checked which consecutive path triples {P_n, P_{n+1}, P_{n+2}} can tile Q₃ as doubled paths.

Script: `probeC_chebyshev.py`. Results: `probeC_results.json`.

### Results — Part 1: Edge Partition Enumeration

**[measured] 4,200 valid {2,4,6} path-union partitions exist** across 31 distinct topology types. Of these, **120 produce 2×{P₂, P₃, P₄}** — the specific topology observed in the 五行 partition. The actual 五行 partition is one of these 120.

The most common topology type (480 partitions) is {2×P₂ | P₂+P₂+P₃ | P₂+P₆}. The target 2×{P₂,P₃,P₄} topology is only the 13th most common (120/4200 = 2.9%).

### Results — Part 2: Spectral Radii

**[measured] All 120 partitions with 2×{P₂,P₃,P₄} topology have identical spectra:** the Chebyshev sequence {1, √2, φ}. This is automatic — P_n's spectrum depends only on length.

The Chebyshev sequence appears in 312 of 4,200 total partitions (including non-2×{P₂,P₃,P₄} topologies that share the same spectral radii). 25 distinct spectral sequences arise across all valid partitions.

### Results — Part 3: The Forcing Gap

**[measured] {2,4,6} edge counts are forced by Z₅ (120/120).** All complement-respecting Z₅ assignments produce this multiset. Algebraic.

**[measured] 2×{P₂,P₃,P₄} topology is NOT forced by Z₅ alone.** Only 40 of 120 Z₅ assignments (33%) produce paired-path topology. The other 80 produce mixed-size path unions (e.g., P₂+P₆ fragments). Of the 40 that produce 2×{P₂,P₃,P₄}, exactly 20 have 克→2×P₄ and 20 have 克→2×P₃ (the 生/克 swap).

**This refines R271:** The original claim that "the unique surjection F₂³→Z₅ forces {P₂,P₃,P₄}" is too strong. Z₅ forces edge counts but not path topology.

### Results — Part 4: Consecutive Triples

**[measured] {P₂, P₃, P₄} is the unique consecutive triple** fitting Q₃. The constraint: 2×(P_n + P_{n+1} + P_{n+2}) has (n-1)+(n)+(n+1) = 3n edges per copy, ×2 = 6n edges total. For Q₃: 6n = 12 → n = 2. The only solution is {P₂, P₃, P₄}. Other triples like 2×{P₃,P₃,P₃} require equal edge counts (4,4,4), incompatible with {2,4,6}.

### Discussion findings

**Three-tier forcing chain (captain + sage):**
- **Tier 1 (Stage):** Z₅ surjection → {2,4,6} edges. 120/120. Algebraic.
- **Tier 2 (Intermediate constraint):** additional condition → 2×{P₂,P₃,P₄} topology. 40/120 = 1/3.
- **Tier 3 (Automatic):** paired consecutive paths → Chebyshev {1,√2,φ} → {trivial, full, GMS}.

**Complement-Z₅ compatibility hypothesis (sage).** The 40 that produce clean paired paths may be exactly the assignments where the complement involution induces a Z₅ isometry on the elements. Sanity-checked on the traditional assignment: complement maps (Earth,Metal,Water,Wood,Fire) via a → 1−a mod 5, which is a Z₅ reflection (isometry). ✓ on 1 data point. Full verification across all 120 assignments is the next computation.

**The 20/20 split (sage).** The Z₅ automorphism a → 2a mod 5 swaps distance-1 (生) and distance-2 (克), creating a Z₂ symmetry within the 40. Each assignment with 克→2×P₄ has a partner with 克→2×P₃. Choosing which distance type gets the GMS is a Z₂ selection within the already-constrained 1/3.

### New results

→ R277: Z₅ forces {2,4,6} edge counts (120/120) but NOT the 2×{P₂,P₃,P₄} topology (40/120 = 1/3). R271 revised: the Chebyshev hierarchy requires an intermediate constraint beyond the bare surjection.

→ R278: {P₂, P₃, P₄} is the unique consecutive path triple fitting Q₃ as doubled paths. Given the topology, the Chebyshev sequence and shift-space hierarchy are automatic.

### What was not tested

- Complement-Z₅ compatibility: does it exactly characterize the 40? (sage hypothesis, next computation)
- The 20/20 split: verify Z₅ automorphism a→2a pairs the two halves
- Probe E (synthesis): material now sufficient to attempt
- Hex-level zeta factorization, incoherent modes (deferred)

---

## Iteration 11: Complement-Z₅ Compatibility Verification (Probe C2 — Fingerprint Investigation)

### Entry Point

The sage hypothesized (Iteration 10) that the 40/120 Z₅ assignments producing 2×{P₂,P₃,P₄} are exactly those where the complement involution t→7−t induces a Z₅ isometry on element labels. This iteration tests that hypothesis and characterizes the full algebraic structure.

### Method

**Part 1 (Isometry test):** For each of 120 complement-respecting Z₅ assignments, computed the permutation of elements induced by complement. Tested whether it's a Z₅ isometry (member of dihedral group D₅). Built the 2×2 contingency table against paired-path topology.

**Part 2 (Isometry types):** Classified each of the 40 (predicted) isometry-compatible assignments by reflection axis. Checked the rotation/reflection split.

**Part 3 (φ-orbit structure):** Applied the Z₅ automorphism φ: a→2a (mod 5) to all 40 assignments. Computed orbit structure, size, and topology alternation.

**Part 4 (Forcing chain completion):** Counted assignments at each tier: 120→40→20→10→1. Connected valve condition (克→生=0) to the forcing chain.

Script: `probeC2_complement_z5.py`. Results: `probeC2_results.json`.

### Results — Part 1: The Central Hypothesis

**[measured] CONFIRMED with zero exceptions.**

|  | Z₅ isometry | NOT isometry | Total |
|--|:-----------:|:------------:|:-----:|
| 2×{P₂,P₃,P₄} | **40** | **0** | 40 |
| NOT 2×{P₂,P₃,P₄} | **0** | **80** | 80 |
| Total | 40 | 80 | 120 |

The complement-Z₅ isometry condition is both necessary and sufficient for the paired-path topology.

### Results — Part 2: Only Reflections

**[measured] All 40 isometries are reflections (a → c−a mod 5), never rotations.** This is forced: complement is order 2, and D₅'s only order-2 elements are the 5 reflections (rotations have order 1 or 5). Each of the 5 reflection axes appears in exactly 8 assignments, with a 4/4 split between 克→P₄ and 克→P₃ within each axis.

### Results — Part 3: φ-Orbit Structure

**[measured] The Z₅ automorphism φ: a→2a (mod 5) has order 4.** All 40 assignments organize into exactly 10 orbits of size 4. Within each orbit, topology alternates: 克→P₄ → 克→P₃ → 克→P₄ → 克→P₃. φ is a bijection between the 20 克→P₄ and 20 克→P₃ assignments (confirmed both directions). φ² (= negation: a→−a mod 5) preserves topology (40/40).

### Results — Part 4: The Complete Forcing Chain

**[measured]** 

| Tier | Count | Gate | Algebraic content |
|------|------:|------|-------------------|
| Z₅ surjections | 120 | — | F₂³ → Z₅ complement-respecting |
| Complement = Z₅ reflection | 40 | ÷3 | Yin-yang coherent with five-phase cycles |
| 克→P₄ (not P₃) | 20 | ÷2 | φ-orbit alternation |
| Valve (克→生=0) | 10 | ÷2 | Irreversibility selection |
| Traditional | 1 | ÷10 | Specific trigram-element pairing |

**[measured] The valve discriminator:** Of the 20 assignments with 克→2×P₄, exactly 10 have the one-way valve (克→生=0 under 互). The symmetric result holds: among the 20 with 克→P₃, exactly 10 have the swapped valve (生→克=0).

### Discussion findings

**The ÷3 at Tier 2 (sage).** The factor 3 = 120/40 is not a simple group index. It measures the "probability of global coherence": 4 complement pairs must each satisfy the same Z₅ reflection. There are 5 possible reflections, each accommodating 8 of the 120 assignments. The remaining 80 have complement pairs on inconsistent reflection axes.

**The 10→1 is irreducible drama (sage).** The 10 assignments sharing all four gates (complement-Z₅ reflection, 克→P₄, valve) differ in: (a) which of the 5 reflection axes is used (each contributes 2 valve assignments), and (b) which specific trigrams get which elements within complement pairs. This is where the I Ching's specific cosmological associations enter — Kun=Earth, Qian=Metal, etc. It's the naming.

**Probe D absorbed into the forcing chain (captain).** The valve appears at Tier 4 (10/20). The question "why choose irreversibility?" reduces to "why Tier 4?" — interpretive, not computational.

**Probe E synthesis (sage).** The answer to "what system is this?": two perpendicular structures on Q₆, each with distinct algebraic origin:
1. **Edge-type** (五行 → Z₅ → shift spaces): the Hamiltonian. Gated by complement-Z₅ compatibility.
2. **Bit-layer** (互 → conveyor belt): the RG transformation. Stage-level, no gate.

Connected by a compatibility condition (complement-Z₅ reflection) that gates access to the clean mathematics (GMS, Chebyshev, φ). Orthogonal by R274.

### New results

→ R279: Complement-Z₅ reflection is the exact gate to the Chebyshev hierarchy. 40/120, zero exceptions. Necessary and sufficient. Only reflections occur (forced: complement is order 2 → D₅ involutions → reflections). 5 axes × 8 assignments = 40.

→ R280: φ-orbit structure. The Z₅ automorphism a→2a (order 4) organizes the 40 into 10 orbits of 4, with topology alternating P₄/P₃. φ² preserves topology. The 克→P₄ vs 克→P₃ selection is the Z₂ choice "which Z₅ distance carries the prohibition."

→ R281: Complete forcing chain 120→40→20→10→1. Tiers 1–3 algebraic (Z₅, complement-Z₅ reflection, φ-orbit). Tier 4 = irreversibility (valve). Tier 5 = naming (specific trigram-element pairing).

### What was not tested

- Aut(Q₃) orbits on the 10 valve assignments: does it reduce the irreducible drama?
- Hex-level zeta factorization: what symmetry group organizes the 64 eigenvalues?
- Incoherent eigenvector characterization: where do the dominant non-GMS modes concentrate?
- The specific reflection axis of the traditional assignment: does it have distinguished properties?

---

## Final Synthesis (Fingerprint Investigation, Iterations 8–11)

### What system is this?

Not one system. Two perpendicular structures on Q₆, each with a distinct algebraic origin:

**Structure 1 — Edge-type axis (the Hamiltonian):**
A Z₅ surjection from Q₃ to the 5-cycle, constrained to be complement-coherent (Z₅ reflection), produces three subgraphs that are bipartite double covers of {trivial shift, full shift, golden mean shift}. The Chebyshev spectral sequence {1, √2, φ} is automatic. At the hexagram level, the coherent sector preserves φ via a same-magnitude resonance filter. The incoherent modes (born from the fiber bundle coupling) dominate the spectral radius.

**Structure 2 — Bit-layer axis (the RG transformation):**
The 互 map is a block-spin RG at scale factor 2 on the 2-dimensional trigram system. It strips one layer per step (2 bits/step), converging in 2 steps to a 4-state hinge attractor. Universal relevant/irrelevant decomposition. Preserves 61/64 Walsh modes.

**Relationship:** Orthogonal (R274). The GMS is a property of the Hamiltonian; 互 is the RG transformation. They share the complement involution as a common symmetry but otherwise do not interact. Their only contact point (type elimination at the attractor) is contingent.

### The forcing chain

The traditional 五行 assignment is located by a 5-tier forcing chain (R281):

| Tier | Count | Gate | Type |
|------|------:|------|------|
| 1. Z₅ surjections | 120 | F₂³ → Z₅ complement-respecting | Stage |
| 2. Complement = Z₅ reflection | 40 | Yin-yang ↔ five-phase coherence | Intermediate |
| 3. 克→P₄ | 20 | φ-orbit alternation | Z₂ selection |
| 4. Valve (克→生=0) | 10 | Irreversibility | Drama |
| 5. Traditional | 1 | Specific trigram-element pairing | Naming |

Tiers 1–3 are algebraic. By Tier 3, the mathematics is locked — GMS, Chebyshev, shift space hierarchy all follow automatically. Tier 4 is the irreversibility selection. Tier 5 is the irreducible content of the specific cosmological associations.

### What the investigation found about its own limits

1. **The coherent sector is subdominant.** The GMS, Chebyshev, and φ structures live in a sector that accounts for 76% of hex-level topological entropy but does not control the spectral radius (ρ_coherent = 2φ ≈ 3.24 < ρ_total = 4.69). The mathematics we understand is the skeleton, not the flesh. The 60 incoherent eigenvalues — born from the fiber bundle coupling with no trigram-level ancestor — dominate long-time hex-level dynamics and are uncharacterized.

2. **The category-level semantic match is forced.** 比和 (sameness) → fixed point, 生 (production) → full shift, 克 (constraint) → GMS. This looks like a correspondence between names and mathematical content. But the three 五行 types are defined by Z₅ distance (0, 1, 2 — a constraint ordering), and the three shift spaces are ordered by the same axis (more constraint → lower entropy). There is only one order-preserving map. The match is tautological, not informative.

3. **The triple null holds.** Everything found about the transition structure (R270–R281) is disconnected from the semantic content of the text (R269). The 五行 decoration and the semantic manifold are independently organized on Q₆.

4. **The structure is the shadow of the architecture.** The I Ching's mathematical structure is overwhelmingly forced by its architectural choices (binary encoding, trigram pairing, five-phase classification, complement symmetry). The traditional element assignment contributes very little — it selects among 10 equivalent realizations of the same abstract pattern. The object is not a deep encoding of dynamics; it is a tight algebraic design where the mathematical content is entailed by the premises.

### Results produced (R270–R281)

| Result | Content | Probe |
|--------|---------|-------|
| R270 | P₄ = bipartite double cover of GMS; ζ_{P₄} = ζ_{GMS} × ζ_{anti-GMS} | A |
| R271 | Hierarchy {trivial, full, GMS} — revised by R277 | A→C |
| R272 | Same-magnitude resonance filter (±2φ, ±2/φ survive; ±√5, ±1 destroyed) | A |
| R273 | 互 = block-spin RG (d=2, b=2, 2 bits/step, hu² idempotent) | B |
| R274 | Edge-type ⊥ bit-layer orthogonality (maximal parity scrambling) | B |
| R275 | Universal relevant/irrelevant decomposition (2 relevant + 4 irrelevant at every fixed point) | B |
| R276 | 61/64 Walsh modes preserved; 3 broken detect middle↔hinge swap | B |
| R277 | Z₅ forces {2,4,6} edges (120/120) but NOT topology (40/120 = 1/3) | C |
| R278 | {P₂, P₃, P₄} unique consecutive path triple for Q₃ | C |
| R279 | Complement-Z₅ reflection = exact gate to Chebyshev hierarchy (40/120, zero exceptions) | C2 |
| R280 | φ-orbit structure (10 orbits of 4, alternating P₄/P₃; φ² preserves topology) | C2 |
| R281 | Complete forcing chain 120→40→20→10→1 | C2 |

### What remains open

- **The dark sector:** hex-level zeta factorization would reveal whether the 60 incoherent eigenvalues organize into a small number of irreducible sectors or fragment. This is the most concrete deferred computation.
- **Aut(Q₃) on the 10:** would determine whether Q₃'s 48 automorphisms collapse some of the 10 valve assignments, reducing the irreducible drama.
- **The compatibility condition generalized:** the complement-Z₅ reflection gate (a Z₂ involution being a Z_n isometry) may have a theorem in finite group theory that characterizes when this is possible, generalizing beyond the I Ching.
- **Perpendicularity in other systems:** is the Hamiltonian ⊥ RG decoupling generic to systems with type classification and coarse-graining, or specific to the I Ching's construction?
