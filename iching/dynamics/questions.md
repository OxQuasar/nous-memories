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

These rule out one operationalization: semantic Laplacian flow. They do not address the broader hypothesis.

## Open Questions

### Q11: Is the I Ching a discretization of a dynamical phase space?

The 64 hexagrams partition some space. Line changes are transitions. The question: does the partition and transition structure correspond to anything in dynamical systems theory?

**Two approaches:**

1. **Forward (pattern matching):** Survey symbolic dynamics for 64-symbol or 6-bit systems. Check whether known dynamical systems have transition graphs resembling the I Ching's structure. Risk: susceptible to "no exact match" closure.

2. **Inverse (data-driven):** Treat the I Ching structure as data. Work backward to infer properties of whatever dynamical system it might discretize. Methods: Koopman operator analysis, SINDy, symbolic regression on the transition graph. More powerful because it doesn't require guessing the target system.

### Q12: Do transition type frequencies tell us anything about dynamics?

The 1:2:3 ratio (比和:生:克) is a strong structural claim — 50% of transitions are 克 (destructive/transformative). In dynamical systems: what's the generic ratio of continuation to bifurcation in parameterized families? Is 克-dominance realistic, or does it require special conditions?

### Q13: Why would φ appear in a system that models dynamics?

φ governs the boundary between stability and chaos in KAM theory (golden-mean torus most stable). φ appears in the I Ching's 克 eigenstructure (P₄, basis-dependent). If the system models dynamics, φ's presence in the destruction channel might not be presentational — it might reflect that the system is optimized for representing dynamics near stability boundaries.

Three independent routes to investigate:
- KAM theory: role of φ in stability boundaries of Hamiltonian systems
- Z₅ representation: cos(2π/5) = (φ−1)/2 forces φ into five-fold symmetric dynamics
- P₄ spectral: do the eigenvalues {φ, 1/φ, −1/φ, −φ} have dynamical interpretation (cascade, resonance)?

### Q14: What would "the I Ching models dynamics" mean formally?

Not a Markov chain (no flow structure). Not a specific dynamical system (too generic). The testable version: the I Ching's structure (transition graph, 克/生/比和 classification, thematic manifold) has properties that are *generic* to a class of dynamical systems. The transition graph would be a symbolic coding, and the thematic manifold would encode the effective dimensionality of the dynamics.

The ~16 dimensions of the manifold are a quantitative measurement. If the system discretizes a lower-dimensional attractor, what attractor dimension would produce ~16 effective dimensions after discretization onto a 6-cube?

### Q15: Can the transition graph be analyzed as an abstract dynamical object?

Independent of embeddings. The 64-node graph with 384 directed edges, each labeled 克/生/比和, is a combinatorial object. What are its graph-theoretic properties relevant to dynamics?
- Spectral gap of the full transition matrix (not just the 克 subgraph)
- Basin structure under iterated application of different transition types
- Cycle structure and attractor topology
- Comparison to known symbolic dynamics (shifts of finite type, sofic shifts)

## Methods Not Yet Used

The prior investigation relied almost entirely on embedding analysis (project onto embeddings, test against permutation null, cross-model validate). The dynamics questions call for different methods:

- **Symbolic dynamics / ergodic theory** — analyzing the transition graph as a shift space
- **Inverse problems** — inferring dynamical properties from the transition structure
- **Literature survey** — what does dynamical systems theory say about 64-state symbolic codings, φ at stability boundaries, bifurcation frequency ratios?
- **Abstract graph theory** — spectral and topological properties of the transition graph without embeddings
- **External data** — comparing I Ching structure to actual dynamics (decision-making, organizational change, situational assessment)
