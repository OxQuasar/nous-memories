# I Ching as a Map to Dynamical Space

## Entry Point

The investigation has characterized the I Ching's internal structure: algebraic skeleton (unique rigid surjection), geometric interface (φ, P₄, 1:2:3 transitions), and thematic manifold (89%, ~16 dimensions, weight-3 Walsh eigenspace). But the I Ching is *representational* — it models change-as-experienced. The text maps structure onto the dynamics of situations. The question is whether this map preserves structure.

## The Four Spaces

1. **Algebraic** — combinatorial skeleton (orbit-invariant, unique)
2. **Geometric** — dynamic interface (basis-dependent, φ, transition structure)
3. **Semantic** — thematic manifold (text, 89% independent of algebra, weight-3 Walsh eigenspace)
4. **Experiential/Dynamical** — the actual territory of situational change

Spaces 1-3 are the I Ching (source side). Space 4 is what it represents (target side). The investigation has characterized 1, 2, and 3. It has not looked at 4.

## Prior Evidence

- Semantic flow on the transition graph is negative (R253 — Laplacian anti-parallelism fails cross-model)
- 五行 transition types (克/生/比和) carry no semantic information (R192, R209, R253)
- The thematic manifold is the weight-3 Walsh eigenspace, not a dynamical structure (R254-R256, in reversal/)
- The 五行 decoration of the transition graph and the semantic manifold are independently organized at three levels: vertex, flow, spectral (R253, R269)

## Questions

### Q11: Is the I Ching a discretization of a dynamical phase space?

**Status: partial.** Rich internal structure characterized (R257–R268). No external matching done.

The 64 hexagrams partition some space. Line changes are transitions. The transition graph has been characterized internally: Chebyshev spectral sequence, Fibonacci walk growth, fiber bundle structure, one-way valve under 互, hinge line dynamics. The structural fingerprint is precise enough to compare against known dynamical systems.

**Untested:** Forward matching (survey symbolic dynamics for systems with this fingerprint) and inverse methods (infer dynamical properties from the transition structure).

### Q12: Do transition type frequencies tell us anything about dynamics?

**Status: open.** The 1:2:3 ratio (比和:生:克) is forced by the unique surjection F₂³ → Z₅ (stage-level property). Entropy follows group size, not 五行 label. The ratio is algebraically determined, not a free parameter.

**Untested:** Comparison to bifurcation frequency ratios in real dynamical systems. The structural fingerprint (weak-tie topology: 比和=local clusters, 生=near-global bridges, 克=universal slow connector) is precise enough for comparison but hasn't been matched to external data.

### Q13: Why would φ appear in a system that models dynamics?

**Status: characterized.** φ appears as 2cos(π/5) in the Chebyshev sequence (R258), as the spectral radius of the P₄ path graph in the 克 trigram subgraph (R265), and survives the hexagram lift only in the coherent sector as eigenvalues ±2φ and ±2/φ (R266). The KAM/irrationality ordering (比和=rational, 生=moderate, 克=maximally irrational) is contingent on the element assignment, not forced by algebra (R267).

Three routes investigated:
- **KAM theory:** The ordering maps 克 to maximal stability (the golden-mean torus). Contingent on assignment.
- **Z₅ representation:** cos(2π/5) = (φ−1)/2 forces φ into Z₅ cycle structure. This is stage-level.
- **P₄ spectral:** The 克 trigram subgraph is a Fibonacci machine. Walk counts = 4·Lₙ exactly. The fiber bundle lift preserves φ only in aligned modes.

**Not addressed:** Whether φ's dynamical role (KAM stability) functionally relates to the I Ching's modeling of change, or is an algebraic coincidence of the (3,5) parameter pair.

### Q14: What would "the I Ching models dynamics" mean formally?

**Status: negative for 五行 pathway.** The internal dynamics (valve, hinge, Fibonacci) are disconnected from the text at all three tested levels — vertex (R192/R209/R253), flow (R253), spectral (R269). The 五行 decoration creates real dynamical structure on Q₆, but this structure does not interact with the semantic manifold.

The bare Q₆ graph connects to text through the complement involution (shared symmetry), but this is a constraint, not a bridge. The complement involution constrains the text to weight-3 (antisymmetric) and constrains Q₆'s null space to be weight-3. These are parallel responses to the same substrate symmetry.

**Untested:** Non-五行 operationalizations of "the graph models dynamics" — the Laplacian test (R253) is only one approach. Other graph-text interfaces besides 五行 labeling have not been tested.

### Q15: Can the transition graph be analyzed as an abstract dynamical object?

**Status: complete.** Comprehensive spectral, topological, and dynamical characterization across 7 iterations (R257–R269). Key results:

- 五行 type is a vertex property, not edge property (R257)
- Chebyshev spectral sequence {1, √2, φ} (R258)
- 克 = unique universal connector with slowest mixing (R259)
- Fiber bundle, not product (R260)
- 互 collapses to hinge bits in 2 steps, mean-isometric (R261)
- 克→生 one-way valve, contingent on 1/6 partition (R262)
- Hinge lines destroy equilibria, F₃/F₄ asymmetry (R263)
- 12-state absorbing class = attractor ⊕ {0, e₁, e₆} (R264)
- Fibonacci machine at trigram level, coherent φ survival (R265, R266)
- Stage/drama decomposition separating forced vs contingent (R267)
- Null-space architecture: 5 invisible + 15 visible weight-3 modes (R268)
- Triple-null projection test negative (R269)

## Methods Not Yet Used

- **Literature survey** — comparing the structural fingerprint to known dynamical system classifications
- **External data** — comparing I Ching structure to actual situational dynamics
- **Inverse methods** — inferring target-space properties from the transition structure
- **Non-五行 graph dynamics** — testing graph-text connections without the 五行 labeling layer
