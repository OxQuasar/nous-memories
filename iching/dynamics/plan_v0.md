# Dynamics Investigation — Implementation Plan

## Constraint

No embedding analysis. These questions need different methods: abstract graph theory, spectral analysis of combinatorial objects, literature survey, and symbolic dynamics. Every probe below works with the transition graph as a combinatorial object or with external literature.

## Available Data

- `atlas/atlas.json` — 64 hexagram profiles (binary, trigrams, elements, hu_hex, palace, basin, depth)
- `atlas/transitions.json` — 384 transitions (source, line, destination, tiyong_relation, basin/palace crossing)

## Structural Facts

- The full transition graph is Q₆ (6-cube): 64 vertices, 384 directed edges (192 undirected), each vertex degree 6
- Edges are labeled by 五行 relation between 体 (stationary) and 用 (moving) trigrams
- On the trigram cube (F₂³): 比和 = 2 edges (P₂+P₂+4I), 生 = 4 edges (P₃+P₃+2I), 克 = 6 edges (P₄∪P₄)
- Trigram-level ratio 1:2:3; hexagram-level counts 84:144:156
- The 互 (nuclear) map h → hu(h) is a separate deterministic 64→64 map with 4-element attractor {0, 21, 42, 63}

---

## Probe 1: 五行-labeled subgraph spectra (Q15)

**What:** Build the three 64×64 adjacency matrices A_克, A_生, A_比和 from transitions.json. Compute their spectra.

**Why:** The full Q₆ adjacency has known spectrum (eigenvalues 6−2k with multiplicity C(6,k)). The 五行 labeling decomposes this into three subgraphs. Their spectra tell us about mixing, connectivity, and periodicity of walks restricted to each transition type.

**Compute:**
1. Build A_克, A_生, A_比和 as symmetric 64×64 matrices from transitions.json (collapse directed to undirected)
2. Verify A_克 + A_生 + A_比和 = A_{Q₆}
3. Eigenvalues and multiplicities of each
4. Connected components of each subgraph
5. Spectral gap of each (relates to mixing time)
6. Check: does A_克 on the 64-vertex graph decompose as a tensor product reflecting the trigram-level P₄∪P₄? What's the relationship between the 8-vertex trigram spectrum {±φ, ±1/φ} and the 64-vertex spectrum?

**Expected output:** Three spectra + component structure + verification of how trigram-level structure lifts to hexagram level.

---

## Probe 2: 互 map dynamics (Q15)

**What:** Analyze the 互 (nuclear) map as a discrete dynamical system.

**Why:** The 互 map is the only deterministic dynamics the I Ching has — every hexagram maps to exactly one nuclear hexagram. This is a concrete dynamical system on 64 states with known attractor. Its structure is the most direct test of whether the I Ching encodes dynamical principles.

**Compute:**
1. Build the 64→64 map from atlas.json (hu_hex field)
2. Full orbit structure: for each hexagram, compute the trajectory h, hu(h), hu²(h), ... until attractor
3. Transient lengths for all 64 states
4. Basin sizes and boundaries (which states lead to which attractor elements)
5. Preimage structure: for each state, how many states map to it? (in-degree of the functional graph)
6. Is the functional graph a tree-with-cycles? What's its structure class?
7. Lyapunov-like analysis: does the map contract distances? Compute mean Hamming distance d(hu(x), hu(y)) / d(x,y) averaged over pairs at each distance
8. Compare basin boundaries to algebraic features (bits 2,3 per R203, palace, 五行 type)

**Expected output:** Complete orbit diagram, basin structure, contraction analysis.

---

## Probe 3: Composed dynamics (Q15/Q11)

**What:** Analyze what happens when line-change transitions compose with the 互 map or with each other.

**Why:** A single line change is one step on Q₆. But the I Ching's operational use involves sequences: a hexagram changes (line flip), then the result is read, then potentially the nuclear hexagram is consulted. The composition of these operations creates richer dynamics than either alone.

**Compute:**
1. For each of the 384 transitions (h, line) → h', compute hu(h') — the nuclear hexagram of the changed hexagram
2. Build the 384-edge directed graph of h → hu(flip(h, line)). What's its structure?
3. Iterate: from each starting hexagram, what happens under repeated apply-random-line-then-hu? Run as a Markov chain, compute stationary distribution
4. Compare the stationary distribution to uniform — are some hexagrams more "reachable" than others?
5. Separate by 五行 type: what happens under 克-only transitions composed with 互? 生-only? 比和-only?
6. Check for absorbing states, periodic orbits, transient structure in each composed system

**Expected output:** Composed transition structures, Markov stationary distributions, comparison across 五行 types.

---

## Probe 4: Symbolic dynamics characterization (Q11/Q14)

**What:** Treat the 五行-labeled transition graph as a shift space and compute its dynamical invariants.

**Why:** Symbolic dynamics is the standard framework for discretized dynamics. If the I Ching is a symbolic coding of some continuous system, its shift space properties (entropy, forbidden words, sofic structure) would constrain what that system could be.

**Compute:**
1. The 五行-labeled transition graph defines allowed transitions. For each pair of types (e.g., 克→克, 克→生, etc.), count how many two-step paths exist through each intermediate state
2. Build the 3×3 transition count matrix between 五行 types (how many 克-edges lead to states with 克-edges, etc.)
3. Compute the topological entropy of walks on each subgraph: log(spectral_radius(A)) / step
4. Compute the topological entropy of the full labeled system
5. Compare these entropies to known symbolic dynamics: full shift on 6 symbols (log 6), golden mean shift (log φ), Fibonacci shift, etc.
6. Check: is any subgraph a shift of finite type? What are the forbidden words (pairs of consecutive transition types that can't occur)?

**Expected output:** Entropy values, forbidden word structure, comparison to known systems.

---

## Probe 5: Transfer matrix and φ (Q13)

**What:** Analyze the role of φ in the 克 subgraph's dynamical properties using transfer matrix methods.

**Why:** φ enters via P₄∪P₄ on the trigram cube. Transfer matrices for path graphs have eigenvalues involving cos(kπ/(n+1)), which for P₄ gives cos(π/5) = φ/2 and cos(2π/5) = (φ−1)/2. The question: does this have dynamical content (Fibonacci quasiperiodicity, renormalization fixed point) or is it purely spectral?

**Compute:**
1. The transfer matrix T_克 for the 克 subgraph on the trigram cube (8×8). This governs the number of 克-walks of length n between trigrams
2. Compute T_克^n for n = 1..20. How does the walk count grow? The growth rate is set by the spectral radius, which involves φ
3. Compare: T_生^n and T_比和^n growth rates. What algebraic numbers govern 生 and 比和?
4. On the 64-vertex level: the 克 walk structure. Does the P₄ eigenstructure create quasiperiodic behavior in walk counts? (Fibonacci-like recurrences)
5. The Zeta function of the 克 subgraph: Z(t) = exp(Σ N_n t^n / n) where N_n = tr(A_克^n). Compute and factor. φ should appear explicitly

**Expected output:** Walk count growth rates with algebraic numbers identified, comparison across types, zeta function.

---

## Probe 6: Bifurcation frequency comparison (Q12)

**What:** Literature survey + computation on bifurcation frequencies in generic dynamical systems, compared to the 1:2:3 ratio.

**Why:** The 比和:生:克 = 1:2:3 edge ratio on the trigram cube is a structural fact. If 比和 ≈ continuation, 生 ≈ smooth change, 克 ≈ bifurcation/disruption, then 50% 克 is a strong claim about how often transformative transitions occur. Is this realistic?

**Literature search:**
1. In generic 1-parameter families of dynamical systems, what fraction of parameter space corresponds to bifurcations vs stable behavior?
2. In the logistic map r ∈ [0,4]: what fraction is periodic windows vs chaos? (known to be ~0.86 chaos / ~0.14 periodic by Lyapunov measure)
3. In Hamiltonian systems: what fraction of phase space is KAM tori vs chaotic sea for typical perturbation strengths?
4. Arnol'd's problem on bifurcation density: any known results on the measure of bifurcation sets in parameterized families?

**Compute (if literature provides a comparison frame):**
1. For the logistic map: measure of different dynamical regimes as a function of r
2. For the standard map: fraction of phase space occupied by different orbit types as a function of kick strength

**Expected output:** Comparison of 1:2:3 to actual bifurcation frequency data from known systems. Does 克-dominance match any known regime?

---

## Probe 7: Dimension and discretization (Q14)

**What:** What constraints does the transition graph structure place on the dimension of a continuous system it could represent?

**Why:** The ~16-dimensional thematic manifold is a measurement. If the I Ching discretizes a dynamical system, the relationship between the number of symbols (64 = 2⁶), the transition structure, and the attractor dimension is constrained by embedding theorems and information-theoretic bounds.

**Compute:**
1. Information-theoretic: 64 states encode log₂(64) = 6 bits. A d-dimensional attractor discretized into 64 cells has resolution ~ 64^(1/d) per dimension. For d = 3, 4, 5, 6: what resolution?
2. Takens embedding: to embed a d-dimensional attractor, need 2d+1 delay coordinates. With 6 binary coordinates, this bounds d ≤ 2.5. But the I Ching's 6 bits aren't delay coordinates — they're structural (upper/lower trigram × 3 lines each)
3. The 互 map contracts to a 4-element attractor. By R203, basins are determined by bits 2,3 — effectively 2 bits, giving 4 basins. The 互 map reduces 6 dimensions to 2. What does this mean for the dynamics?
4. Graph-theoretic dimension estimates: compute the spectral dimension of each 五行 subgraph (from the scaling of return probability P(t) ~ t^{-d_s/2})
5. Compare spectral dimensions to the ~16-dim manifold measurement — are they consistent?

**Expected output:** Dimension bounds from multiple methods, consistency check.

---

## Probe 8+: Captain's Discretion

Follow high value threads opened.


## What Counts as Progress

- **Positive:** A spectral or structural property of the transition graph that matches a known class of dynamical systems. Or: dimension estimates from graph theory consistent with the ~16-dim manifold via a known discretization relationship.
- **Negative:** The transition graph is structurally generic (indistinguishable from random labeled hypercube). Or: dimension estimates inconsistent with any reasonable dynamical interpretation.
- **Reframing:** The graph has structure but it doesn't match "dynamics" — it matches something else (coding theory, combinatorial design, game theory).
- **All of these are results.** None of them close the investigation.
