# Dynamics Investigation — Findings

> Entry point: the I Ching as a representational map to the dynamics of situational change.
> Questions Q11–Q15 in `questions.md`.

## Results

### R253: Dynamical Flow Hypothesis — Negative

**[measured]** Walsh spectral decomposition of hex-level embeddings on Q₆ is near-flat. Three deviations: weight-1 depleted (4.4th %ile), weight-4 depleted (5.0th %ile), weight-3 enriched (97.9th %ile).

**[measured]** Complement Laplacian anti-parallelism: BGE-M3 raw marginal (5th %ile, mean cosine −0.033), E5-large fails cross-model replication (26th %ile). No algebraic property predicts Laplacian magnitude (all p > 0.12). No semantic flow structure on the transition graph.

**[measured]** 克/生/比和 classification null at vertex level (extending edge-level nulls R192, R209).

Script: `d1_laplacian_walsh.py`

### R257: 五行 Edge Classification Is a Vertex Property

**[measured]** Every hexagram sends ALL 6 outgoing transitions to the SAME 五行 group. The directed matrix decomposes as A_g = P_g × A_{Q₆}, where P_g is the diagonal projection onto hexagrams with surface relation g. The edge label is determined entirely by the source vertex, not the transition.

132 of 192 undirected Q₆ edges (69%) carry different types in each direction. Vertex counts: 比和=14, 生=24, 克=26.

Script: `p1_subgraph_spectra.py`

### R258: Chebyshev Spectral Sequence

**[measured]** Trigram-level spectral radii: 比和 = 1, 生 = √2, 克 = φ. These are 2cos(π/3), 2cos(π/4), 2cos(π/5) — a Chebyshev sequence with denominators 3, 4, 5. The 五行 partition decomposes the 12 trigram-cube edges into paired paths of consecutive lengths {P₂, P₃, P₄}, exhausting all edges with no overlap.

Script: `p1_subgraph_spectra.py`

### R259: 克 Universal Connectivity, Inverse Spectral Gap

**[measured]** 克 is the unique universally connected 五行 subgraph (OR-symmetrized: 1 component, all 64 vertices). 比和 has 11 components (10 isolates), 生 has 3 components (2 isolates).

**[measured]** Spectral gaps inversely ordered: 比和 (2.0) >> 生 (0.951) >> 克 (0.288). 克 connects everything but mixes slowest.

Script: `p1_subgraph_spectra.py`

### R260: Fiber Bundle Structure (Non-Product Lift)

**[measured]** The 64-vertex 五行 subgraphs are NOT Cartesian products of the 8-vertex trigram subgraphs. Max spectral deviations: 比和=2.0, 生=1.41, 克=2.24. The edge labeling depends on the interaction of BOTH trigrams (surface relation = 体-用 comparison).

Script: `p1_subgraph_spectra.py`

### R261: 互 Map — Hinge Collapse and Mean-Isometry

**[measured]** hu²(h) = 21·b₂ + 42·b₃. The 互 map collapses 6 bits to 2 (lines 3,4 — the inter-trigram boundary) in exactly 2 steps. Basins perfectly balanced (16 each). Preimage perfectly regular (in-degree = 4).

**[measured]** Mean-isometry at every Hamming distance: d(hu(x),hu(y))/d(x,y) = 1.0000. Forced by bit weights [0,1,2,2,1,0], mean = 1.0. Variance decreases monotonically: σ=0.82 at d=1 (neighbors scrambled), σ=0 at d=6 (complements perfectly preserved).

Script: `p2_hu_dynamics.py`

### R262: 克→生 One-Way Valve Under 互

**[measured]** 五行 transition matrix under 互:

| src\dst | 比和 | 生 | 克 |
|---------|------|-----|-----|
| 比和 | 6 | 4 | 4 |
| 生 | 2 | 4 | 18 |
| 克 | 8 | 0 | 18 |

克→生 = 0. Strict one-way flow: 生 →→ 克 ⇄ 比和 with no return from 克 to 生.

**[measured]** Basin × 五行 completely independent (p=0.98). The 互 map is geometrically type-blind (basin structure) but elementally directional (type-space flow). The valve is an interaction effect: (bit compression) × (element assignment). Neither factor alone creates directionality.

**[measured]** The valve is contingent: only 1 of 6 unlabeled partitions (from valid surjections) has a zero cell. Causal chain: element assignment → bit constraint on 互 image → type imbalance (≤2 targets of one type) → zero cell → one-way valve.

Scripts: `p2_hu_dynamics.py`, `p3_composed_dynamics.py`

### R263: Hinge Lines Destroy Equilibria

**[measured]** Composed maps F_k(h) = hu(flip(h, k)):

| Line | Type | Attractors | Basins |
|------|------|-----------|--------|
| 1, 6 | outer | 2 fixed + 1 two-cycle | 4 (32,32,16,16) |
| 2, 5 | middle | 2 fixed + 1 two-cycle | 4 (32,32,16,16) |
| **3, 4** | **hinge** | **single 4-cycle** | **1 (all 64)** |

Hinge lines (3,4 — the inter-trigram boundary) destroy all equilibria: no fixed points, no 2-cycles. Every hexagram flows to a single global 4-cycle.

**[measured]** F₃/F₄ asymmetry: F₃ cycle alternates 生/比和 (excludes 克). F₄ cycle is pure 克 (excludes 生 and 比和). The two sides of the inter-trigram boundary are dynamically inequivalent.

**[measured]** The 克→生 block breaks under composition: only pure 互 (F₁ = F₆ = hu) preserves the zero cell. Lines 2–5 produce nonzero 克→生 counts.

Script: `p3_composed_dynamics.py`

### R264: 12-State Absorbing Class

**[measured]** The random-line-then-互 Markov chain converges in 3 steps to 12 absorbing states, uniform 1/12 each. The absorbing set = {a ⊕ v : a ∈ {0, 21, 42, 63}, v ∈ {0, e₁, e₆}} — the 互 attractor thickened by single outer-bit flips. Composition: 比和=4 (33%), 生=2 (17%), 克=6 (50%).

Script: `p3_composed_dynamics.py`

### R265: Fibonacci Machine at Trigram Level

**[measured]** Trigram-level closed walk counts (even n, verified n=1..20):

| Type | Form | Growth |
|------|------|--------|
| 克 | 4·L_n (Lucas numbers) | φ^n |
| 生 | 4·2^(n/2) | (√2)^n |
| 比和 | 4 (constant) | 1 |

The 克 trigram subgraph is a Fibonacci machine: walk counts satisfy the Fibonacci recurrence exactly, forced by P₄'s eigenvalues {±φ, ±1/φ}.

Script: `p45_symbolic_transfer.py`

### R266: Fibonacci Does Not Lift; φ Survives in Coherent Sector

**[measured]** Hexagram-level 克 walks do NOT satisfy a Fibonacci recurrence. The fiber bundle structure introduces a degree-46 recurrence.

**[measured]** φ survives explicitly: eigenvalues ±2φ and ±2/φ (multiplicity 1 each) in the hexagram 克 OR-symmetrized spectrum. These are the "aligned" trigram modes (both trigrams in the same P₄ eigenstate). The "misaligned" mode ±√5 = ±(φ + 1/φ) is absent — destroyed by the fiber bundle coupling. The non-product interaction preserves coherent modes while destroying incoherent ones.

Script: `p45_symbolic_transfer.py`

### R267: Stage-vs-Drama Decomposition

**[measured]** Across 6 alternative element assignments:

- **Entropy** follows group SIZE (stage-level): the 26-element group always has the highest entropy (~1.545), regardless of which 五行 type it carries.
- **Spectral gap** follows 五行 LABEL (derived stage): ordering 生 > 克 > 比和 holds for ALL 6 assignments, invariant under element permutation. This is forced by the unique surjection F₂³ → Z₅ constraining 生↔P₃ and 克↔P₄ invariantly.

**Classification:**
- **Stage** (forced by algebra): entropy-by-size, bipartiteness, Chebyshev sequence, mean-isometry, stationary = proportional, no forbidden two-step words
- **Derived stage** (forced by unique surjection × Z₅ cycle): spectral gap ordering 生 > 克 > 比和, path assignment 生↔P₃ / 克↔P₄
- **Drama** (contingent on traditional assignment): zero cell / one-way valve (1/6 of partitions), F₃/F₄ asymmetry type content, specific flow direction
- **Interaction** (bit compression × element assignment): valve mechanism, coherent φ survival

Script: `p45_symbolic_transfer.py`

### R268: Null-Space Architecture of Weight-3

**[measured]** Q₆'s null space = weight-3 Walsh eigenspace (dim 20). The three 五行 OR-symmetrized subgraphs carve weight-3 into:
- 5-dim triple null (invisible to ALL three types)
- 15-dim visible complement (in range of at least one type)
- Common range of all three subgraphs: 3-dim, weight-{1,5} modes

Script: `p7_dimension.py`

### R269: Triple-Null Projection Test — Negative

**[measured]** The semantic manifold does NOT avoid the 5 triple-null directions:

| Model | f_invisible | Expected | Percentile |
|-------|-------------|----------|-----------|
| BGE-M3 | 0.2445 | 0.2500 | 35.5th |
| E5-large | 0.2413 | 0.2500 | 25.3rd |
| SikuRoBERTa | 0.2854 | 0.2500 | 96.8th |

The manifold distributes variance uniformly across visible/invisible directions. The 五行 transition structure and the semantic manifold are independently organized within weight-3. Three-level null: vertex (R192/R209/R253), flow (R253), spectral (this result).

The complement involution is a shared constraint (symmetry of Q₆), not a bridge: it constrains text (antisymmetric → weight-3) and graph (null at weight-3) independently.

Script: `p8_triple_null_test.py`

## Results Moved to reversal/

R254 (weight-3 eigenspace identification), R255 (dimensional pressure), R256 (Krawtchouk unification) are manifold characterization results. Relocated to `reversal/findings.md` Phase 9.

## Question Status

| Question | Status | Finding |
|----------|--------|---------|
| Q11 (discretization) | Partial | Rich internal structure characterized; no external matching done |
| Q12 (frequencies) | Open | 1:2:3 is forced by algebra; comparison to bifurcation data untested |
| Q13 (φ) | Characterized | Chebyshev sequence from P₄, coherent survival through fiber bundle, KAM ordering contingent on assignment |
| Q14 (formal meaning) | Negative for 五行 | Internal dynamics (valve, hinge, Fibonacci) are disconnected from text at all three tested levels |
| Q15 (abstract analysis) | Complete | Comprehensive spectral, topological, and dynamical characterization of the transition graph |

### Fingerprint Questions (F1–F7)

| Question | Status | Finding |
|----------|--------|---------|
| F1 (Chebyshev) | Characterized | Forced by {P₂,P₃,P₄} which requires complement-Z₅ reflection gate (R277–R279) |
| F2 (Fibonacci) | Characterized | P₄ = bipartite double cover of GMS; walk counts = 4×Lucas (R270) |
| F3 (irreversibility) | Absorbed | Valve at Tier 4 of forcing chain; 10/20 assignments have it (R281) |
| F4 (contraction) | Characterized | 互 = block-spin RG, d=2, b=2, 2 bits/step (R273) |
| F5 (coherent sector) | Characterized | Same-magnitude resonance filter; coherent sector subdominant (R272) |
| F6 (combined signature) | Answered | Two perpendicular structures: edge-type (Hamiltonian) ⊥ bit-layer (RG) |
| F7 (互 = RG?) | Confirmed | Block-spin RG on bit-layer axis; does NOT descend to GMS (R273–R274) |

## What Remains Untested

- External matching: does the transition structure correspond to any known dynamical system? (Q11)
- Bifurcation frequency comparison: 1:2:3 vs real dynamical systems (Q12)
- Non-五行 graph dynamics: Q₆ structure connecting to text independently of the 五行 overlay (only Laplacian tested; other operationalizations possible)
- External data: actual situational dynamics vs I Ching transition structure
- Hex-level zeta factorization: what symmetry group organizes the 60 incoherent eigenvalues? (the "dark sector")
- Aut(Q₃) orbits on the 10 valve assignments: does it reduce the irreducible drama at Tier 5?
- The complement-Z₅ reflection condition generalized: is there a theorem in finite group theory for when a Z₂ involution on a set is a Z_n isometry?

## Fingerprint Investigation Results (Probe A)

### R270: P₄ = Bipartite Double Cover of the Golden Mean Shift

**[measured]** The zeta function of P₄ factors exactly:

det(I - zA_{P₄}) = (1 - z - z²)(1 + z - z²) = ζ⁻¹_GMS(z) × ζ⁻¹_anti-GMS(z)

The first factor is the GMS zeta denominator; the second is its parity twist (z → −z). This is the Artin factorization for the Z₂-cover P₄ → GMS.

**[measured]** Bipartite square root confirmation: A²_{P₄}|_odd = M²_GMS = [[2,1],[1,1]] (exact matrix equality). A²|_even = [[1,1],[1,2]] = (M²_GMS)^T. Both sectors have spectrum {φ², 1/φ²}.

**[measured]** P₄ and GMS are NOT topologically conjugate (different periodic orbit counts: P₄ has 2L_n even/0 odd; GMS has L_n all n). P₄ is the bipartite double cover, with the folding map as a topological factor map.

Script: `probeA_golden_mean.py`

### R271: The {Trivial, Full, GMS} Hierarchy Is Algebraically Forced

**[proven]** The unique surjection F₂³ → Z₅ forces the edge partition {2, 4, 6} on Q₃'s 12 edges, giving paths {P₂, P₃, P₄}. Each P_n is a bipartite double cover:

| 五行 type | Path | Base shift | ρ_base | ρ_cover = √(ρ_base²) |
|-----------|------|-----------|--------|----------------------|
| 比和 | P₂ | Trivial (fixed point) | 1 | 1 |
| 生 | P₃ | Full 2-shift | 2 | √2 |
| 克 | P₄ | Golden mean shift | φ | φ |

The Chebyshev sequence {1, √2, φ} = {2cos(π/3), 2cos(π/4), 2cos(π/5)} is the cover spectral radii. The hierarchy {trivial, full, GMS} exhausts the three simplest SFTs on binary alphabet — forced by the algebraic constraint, not selected from among alternatives. Stage-level.

Script: `probeA_golden_mean.py`

### R272: Same-Magnitude Resonance Filter at Hexagram Level

**[measured]** The fiber bundle coupling at the hexagram level selectively preserves tensor eigenvalues where both trigrams resonate at the same eigenvalue magnitude, and destroys cross-magnitude modes:

| Tensor eigenvalue | Form | Magnitude match | Survives hex? |
|-------------------|------|-----------------|---------------|
| ±2φ | φ+φ | ✓ same | ✓ |
| ±2/φ | 1/φ+1/φ | ✓ same | ✓ |
| 0 | φ+(-φ), etc. | — | ✓ |
| ±√5 | φ+1/φ | ✗ cross | ✗ destroyed |
| ±1 | φ-1/φ | ✗ cross | ✗ destroyed |

The destroyed √5 = tr(M_GMS): the hex level cannot linearly access the trace of the underlying GMS matrix. This filter is non-trivial only for 克 (the only subgraph with two distinct nonzero eigenvalue magnitudes).

**[measured]** Coherent sector (±2φ, ±2/φ) accounts for 76% of hex-level topological entropy but does NOT dominate the spectral radius (ρ_coherent = 2φ ≈ 3.24 < ρ_total = 4.69). Long-time hex-level dynamics are controlled by incoherent modes with no trigram-level analog.

Script: `probeA_golden_mean.py`

## Fingerprint Investigation Results (Probe B)

### R273: 互 Is a Block-Spin RG (Scale Factor 2, d=2)

**[measured]** The 互 map is a conveyor belt RG on the bit-layer structure:
- 3 layers of 2 bits: outer {0,5}, middle {1,4}, hinge {2,3}
- Each step shifts information inward by one layer: outer→middle→hinge
- Hinge bits swap under hu: (b₂,b₃) → (b₃,b₂). hu² = identity on hinge.
- Entropy loss: exactly 2 bits/step for 2 steps (6→4→2 bits). Matches d·log₂(b) = 2·1 = 2.
- Semigroup: {hu, hu², hu²=hu⁴=...}. hu² is idempotent (the RG terminates at the IR fixed point).
- Image sizes: 64→16→4 (factor 4 reduction per step).

Stage-level: the routing σ = [1,2,3,2,3,4] is defined by nuclear trigram construction, independent of 五行.

Script: `probeB_renormalization.py`

### R274: Edge-Type and Bit-Layer Axes Are Orthogonal

**[measured]** 互 maximally scrambles P₄ bipartite parity. The 4×4 parity transition matrix (pL_in, pU_in) → (pL_out, pU_out) is perfectly uniform: every cell = 4/16 = 25%.

The edge-type axis (五行 → P₂/P₃/P₄ → shift spaces) and the bit-layer axis (互 → conveyor belt → hinge attractor) are complementary decompositions of Q₆. One classifies transitions by kind; the other classifies structure by depth. 互 does not descend to the GMS quotient.

Script: `probeB_renormalization.py`

### R275: Universal Relevant/Irrelevant Decomposition

**[measured]** At every fixed point {0, 21, 42, 63}:
- 2 relevant directions: hinge bits {2, 3} — perturbations grow under hu²
- 4 irrelevant directions: outer+middle bits {0, 1, 4, 5} — perturbations die under hu²

Phases classified by hinge parity: {0, 63} fixed (b₂=b₃, swap-invariant), {21, 42} period-2 (b₂≠b₃, exchanged by swap).

Script: `probeB_renormalization.py`

### R276: Walsh Mode Breaking Pattern

**[measured]** 互 preserves 61/64 Walsh coefficients under pushforward. The 3 broken modes {001010, 010100, 011110} have weights {2, 2, 4}, form a closed group under XOR, and detect the middle↔hinge rearrangement. No connection to the weight-3 triple null (R268) — the broken modes and the invisible modes live in different weight subspaces.

Script: `probeB_renormalization.py`

## Fingerprint Investigation Results (Probe C)

### R277: The Forcing Gap — Z₅ Forces Edge Counts, Not Topology

**[measured]** All 120 complement-respecting Z₅ assignments produce the edge-count multiset {2, 4, 6}. Algebraically forced by Z₅'s distance structure.

**[measured]** Only 40 of 120 Z₅ assignments (33%) produce the 2×{P₂, P₃, P₄} paired-path topology. The other 80 produce mixed-size path unions (e.g., P₂+P₆ fragments). Of the 40 with paired paths, 20 have 克→2×P₄ and 20 have 克→2×P₃.

**R271 revised:** The three-tier forcing chain:
- Tier 1 (Stage): Z₅ → {2,4,6} edges (120/120)
- Tier 2 (Intermediate): additional constraint → 2×{P₂,P₃,P₄} (40/120 = 1/3)
- Tier 3 (Automatic): paired consecutive paths → Chebyshev → {trivial, full, GMS}

The hierarchy {trivial, full, GMS} is NOT purely stage-level. It requires an intermediate constraint (hypothesized: complement-Z₅ compatibility). The 1/3 fraction measures the restrictiveness of this constraint.

4,200 total {2,4,6} path-union partitions of Q₃ exist across 31 topology types. The 2×{P₂,P₃,P₄} topology accounts for 120 of these (2.9%).

Script: `probeC_chebyshev.py`

### R278: Unique Consecutive Path Triple

**[proven]** {P₂, P₃, P₄} is the unique consecutive path triple fitting Q₃ as doubled paths. The constraint 2×[(n-1)+n+(n+1)] = 12 forces n=2 uniquely. Other triples either exceed Q₃'s vertex count or require incompatible edge-count distributions.

Script: `probeC_chebyshev.py`

## Fingerprint Investigation Results (Probe C2)

### R279: Complement-Z₅ Reflection Is the Exact Gate

**[measured]** The 40/120 Z₅ assignments producing 2×{P₂,P₃,P₄} topology are exactly those where the complement involution t→7−t induces a Z₅ isometry on element labels. Perfect contingency: 40 matches, 0 exceptions in either direction.

**[proven]** All 40 isometries are reflections (a→c−a mod 5), never rotations. Forced: complement has order 2, and D₅'s only order-2 elements are the 5 reflections. Each reflection axis appears in exactly 8 assignments (4 with 克→P₄, 4 with 克→P₃).

The structural content: the yin-yang symmetry (complement involution) must be coherent with the five-phase cycles (Z₅). The fraction 1/3 = 40/120 measures the restrictiveness of this coherence condition.

Script: `probeC2_complement_z5.py`

### R280: φ-Orbit Structure

**[measured]** The Z₅ automorphism φ: a→2a (mod 5, order 4) organizes the 40 complement-compatible assignments into exactly 10 orbits of size 4. Within each orbit, topology alternates: 克→P₄ → 克→P₃ → 克→P₄ → 克→P₃.

φ is a bijection between the 20 克→P₄ and 20 克→P₃ assignments (both directions verified). φ² (= negation, a→−a mod 5) preserves topology. The 克→P₄ vs 克→P₃ selection is the Z₂ choice "which Z₅ distance carries the prohibition."

Script: `probeC2_complement_z5.py`

### R281: Complete Forcing Chain

**[measured]** The traditional 五行 assignment is located by a 5-tier forcing chain:

| Tier | Count | Gate | Type |
|------|------:|------|------|
| 1. Z₅ surjections | 120 | F₂³ → Z₅ complement-respecting | Stage |
| 2. Complement = Z₅ reflection | 40 | Yin-yang ↔ five-phase coherence | Intermediate |
| 3. 克→P₄ | 20 | φ-orbit alternation | Z₂ selection |
| 4. Valve (克→生=0) | 10 | Irreversibility | Drama |
| 5. Traditional | 1 | Specific trigram-element pairing | Naming |

Tiers 1–3 are algebraic. Tier 4 is the irreversibility selection (half of Tier 3 assignments have the one-way valve). Tier 5 is the irreducible content of the specific cosmological associations.

Script: `probeC2_complement_z5.py`
