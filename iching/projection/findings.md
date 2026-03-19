# Resolution Phase — Findings

> Phase 8: What is it projecting?

## Central Finding

The I Ching is not projecting an external dynamical system. It is the unique canonical classification of single-step changes in a 6-bit binary system under complement symmetry and five-phase typing. The "minimal Markov partition" interpretation from Phase 7 refines to: the minimal system *on which* the constraint class {GMS + complement + Z₅} can be written — not a partition *of* some external target, but the stage itself.

## Results

### R282: Partition Tightness on the Constraint Axis

The dark sector (eigenvalues with no trigram-level ancestor) is spectrally generic: Walsh-binomial weight distribution, no internal structure, immediately dominant from step 0. This is evidence that the 五行 edge-type decomposition captures all spectral constraints — nothing is missing. The dynamics within the constraint manifold are free.

Scope qualifier: tightness here means no spectral constraints are absent. It does not address whether 64 states is the minimal state count for encoding these constraints (though that is answered separately: 6 bits is forced by {≥3 bits for Z₅ surjection} × {2 subsystems for interaction typing} × {complement symmetry}).

### R283: 生 Coherent Sector Is the Kernel (Topological)

The generation channel has zero non-trivial coherent eigenvalues — every dynamical mode is an interaction effect between upper and lower trigrams. Confirmed topological: the directed (unsymmetrized) 生 matrix also has a trivial coherent sector (24 coherent eigenvalues, all zero). The kernel result is about how generation organizes Q₆, not about symmetrization.

Coherent content grades inversely with Z₅ proximity: 比和 (21.1%, distance 0) > 克 (9.1%, distance 2) > 生 (0%, distance 1). Adjacency on the 5-cycle is more destructive to independent trigram dynamics than opposition.

Unexpected: the directed 生 matrix has all-real eigenvalues (64/64) despite being non-symmetric, implying similarity to a symmetric matrix.

### R284: Algebraic Complexity Hierarchy

Dark sector algebraic structure varies by type:
- **比和:** 28/32 dark eigenvalues in Q(√2) or Q(√5). Remaining 4 are roots of x⁴ − 14x² + 8 (discriminant involves √41).
- **克:** 10/44 in Q(√5). Two pairs are roots of x⁴ − 7x² + 9 (discriminant involves √13). 34 unidentified.
- **生:** 2/44 in Q. 42 are generic algebraic numbers of degree > 4.

Gradient: simpler relation → simpler dark sector → more tractable dynamics. Proper factorization of characteristic polynomials over Q would sharpen this.

### R285: Constraint/Dynamics Orthogonality Confirmed Spectrally

The edge-type axis (五行 typing) defines the constraint manifold. The bit-layer axis (互 as RG) coarse-grains dynamics within it. The coherent/dark decomposition operates on the constraint axis; the RG relevant/irrelevant decomposition operates on the dynamics axis. These are orthogonal (consistent with R274). Dark sector dominance confirms: constraints don't predict dynamics.

### R286: Not the Markov Partition of Any 1D Map

Absolute structural obstruction: continuous 1D maps produce transition matrices where each row is a contiguous block of 1s (interval graphs). Q₃ is not an interval graph. No reordering can fix this. Rules out all 1D maps at all parameters with all partitions.

### R287: Constraint-on-Transitions vs Constraint-on-States

Two routes to realize the GMS:
- **Fibonacci route (logistic map):** State space = set of legal sequences. Only GMS-allowed states exist. Cell count grows as Fibonacci. Constraint on which states exist.
- **Hypercube route (I Ching):** State space = full binary cube (all 2⁶ = 64 states). GMS constraint lives on edges (transition typing as 克), not vertices. All states exist; constraint on how you move between them.

This explains three dark sector properties simultaneously: existence (over-complete embedding), genericity (excess has no reason for structure), dominance (64 ≫ 13 GMS-legal 6-sequences).

The spectral overlap persists at the constraint level: both systems share forbidden-"11", entropy log(φ), and algebraic field Q(φ). The geometries diverge: interval graph vs hypercube.

### R288: Single-Step Classification (R1 Closure)

The I Ching is the unique canonical classification of single-step Q₆ transitions under complement-Z₅ axioms. Information content is concentrated in the single-step regime. The classification is unique (uniqueness theorem), not "maximally informative" — there are no competitors.

Evidence:
1. Not the Markov partition of any 1D map (R286)
2. Full transition graph IS Q₆ — typing classifies but doesn't constrain
3. Type info decorrelates in 1–2 steps (single-step, not trajectory-level)
4. Dark sector generic — no external system's signature
5. Directed single-step subgraphs are the informative regime — matching traditional practice

The "minimal Markov partition" refines to: minimal system on which {GMS + complement + Z₅} can be written.

### R289: Composability Decorrelation

Mutual information half-lives: 生 ~1.1 steps, 克 ~1.4, 比和 ~1.8. Ordering matches coherent content gradient (more dark = faster decorrelation). Mixing time on full graph: 5 steps. Spectral gap = 1/6 (Q₆ geometry). Lazy chain τ ≈ 2.4 steps for all types.

Stationary distribution: 比和 = 0.219, 生 = 0.375, 克 = 0.406 (proportional to vertex type counts 14:24:26).

Directed type-restricted subgraphs show dramatically different behavior: entropy at step 5 is 0.06–0.24 bits (vs max 1.58 for symmetric). The 体用 directionality creates absorbing-like structures. The architecture is informative in the directed single-step regime — the regime traditional practice uses.

### R290: 互 Preserves 1/3 of Transitions

互(b₀b₁b₂b₃b₄b₅) = b₁b₂b₃b₂b₃b₄. Only middle-line bit-flips (b₁, b₄) produce single-bit-flip transitions in the 互 image. Outer lines vanish; boundary lines double. Exactly 2/6 = 1/3 preserved, type-independently. Pure Q₆ geometry × 互 bit structure. 互 does not commute with transitions (||[A,H]||_F = 25.3). 互 has 2 fixed points.

### R291: 生 Parity Balance Forced by Uniqueness Theorem

The {2,2,2,1,1} element partition has two singleton elements (Water, Fire) at Z₅ distance 2 (克 relation), forced by complement-Z₅ structure. Parity imbalance arises only from singleton×singleton pairs:
- 比和: 8 even / 6 odd (Water×Water + Fire×Fire → extra even)
- 克: 12 even / 14 odd (Water×Fire + Fire×Water → extra odd)
- 生: 12 even / 12 odd (no singleton×singleton pairs → exact balance)

生's exact convergence to stationary (no bipartite residual) is downstream of the uniqueness theorem.

## Phase Consistency Check

R282–R291 checked against all prior phases (1–7): consistent. The algebra is the typing; the text is the content within the frame. Grammar ≠ vocabulary. The three-level null (R192/R209/R253) reads as confirmation: edge properties (typing) and vertex properties (text) are generically independent on graphs without strong vertex-edge coupling. The ~11% correlation is the shared complement symmetry.

## Scripts

| Script | Output | Probe |
|--------|--------|-------|
| `dark_sector.py` | `dark_sector_results.json` | Probe 4 (R5) |
| `logistic_map.py` | `logistic_map_results.json` | Probe 1 (R1) |
| `composability.py` | `composability_results.json` | Probe 5 (R6) |
