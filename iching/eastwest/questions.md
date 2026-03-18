# East/West: The Number 5 Across Traditions

## Context

The I Ching research program established that Z₅ is forced by the axioms (R102: smallest prime with two independent Hamiltonian cycles). The West independently arrived at 5 through geometry (the pentagram, the golden ratio). Multiple branches of mathematics converge on 5 from independent directions. This folder investigates what connects these convergences.

## The Convergence

| Property | Branch | Why 5 | Tradition |
|----------|--------|-------|-----------|
| Two independent Hamiltonian cycles | Group theory | Smallest prime where stride-1 ≠ ±stride-2 | Chinese (五行 生/克) |
| Golden ratio φ = (1+√5)/2 | Algebra | √5 is the discriminant of x²−x−1 | Greek (Pythagorean) |
| Optimal packing angle 360°/φ² | Number theory | φ has the slowest-converging continued fraction | Biological (phyllotaxis) |
| First non-trivial star polygon {5/2} | Geometry | Smallest n where stride-2 gives a star, not a polygon | Greek/esoteric (pentagram) |
| Rigid surjection F₂³ → Z₅ | Combinatorics | Orbit formula = 1 only at (3,5) | I Ching research |
| Five-fold classification | Cross-cultural | China (五行), India (Mahābhūta), Greek (4+1) | Multiple |

---

## Established Results (R181–R213)

### The Dimension Threshold (R181–R182)
- (2,3) is the unique viable point at n=2. Z₃ supports only 1 Hamiltonian cycle — dual dynamics impossible.
- n=3 is necessary and sufficient for the minimum dual-cycle system (given binary encoding).
- The Greek quaternary system (F₂²) is structurally locked out of dual-cycle dynamics.

### The Cyclotomic Structure (R183–R188)
- Universal trace formula: Shape A trace = 1+2cos(2πj/p); Shape B trace = 3.
- At p=5: Shape A traces are {φ, ψ}. The golden ratio tags the I Ching's partition type.
- W(k=1, ω=0) = φ exactly for the I Ching's surjection.
- All |W|² values at (3,5) lie in Q(√5).
- Pentagon = Cay(Z₅,{±1}) = 生; Pentagram = Cay(Z₅,{±2}) = 克; edge ratio = φ.
- Complement equivariance ↔ Galois conjugation (σ: ζ₅ → ζ₅⁴). Generic to all equivariant Z_p maps.

### Textual Findings (R189–R196)
- KW sequence: strong signal in text embeddings (tuan 99.7%, guaci 92%), zero in binary/algebraic metrics.
- Texts use the five-phase *partition* but not the five-phase *dynamics* (生/克 carry no semantic information).
- hu_cell predicts cross-layer semantic similarity (99.4–99.5%ile). Only cross-layer algebraic predictor. Tier 2.
- R191 retracted (surface cell anti-signal failed cross-model replication).

### Dynamics & Cube-Edge Geometry (R197–R203)
- Full pullback (f-lifted Cayley graphs on F₂³): φ NOT detected. Fiber-size asymmetry breaks clean spectral structure.
- **Cube-edge partition**: A_克 spectrum = {±φ, ±φ, ±1/φ, ±1/φ}. The 克 subgraph of the 3-cube is P₄∪P₄; φ enters via 2cos(kπ/5) where 5 = path length + 1.
- Path-length progression: 比和→P₂, 生→P₃, 克→P₄. Only 克 produces φ.
- The n=3 identity: 2^{n-1}+1 = 2ⁿ−3 = p holds uniquely at n=3. Two independent routes to φ converge only at (3,5).
- Transition balance: 比和:生:克 = 1:2:3 across all 384 line transitions. Bit-stratified by line position.
- E=1 family fiber ratio: 3/(p−3) → 0. Not Fibonacci-related.
- Basin structure trivial: F₂-linear, determined by bits 2,3.

### Orbit Characterization (R204–R208)
- 96/240 surjections (2/5) have φ in one cycle type. Perfect 生↔克 mirror symmetry.
- φ ↔ Jacobian multiset {{比和,生},{克},{生,克}} with pure direction at basis vector. Necessary and sufficient.
- Nuclear map × Jacobian: no structural coupling. Pure-克 direction uniform across all 6 non-111 directions.
- (4,13): 克 = P₂⁴ + 8I. φ absent — fibers too thin for extended paths.

### Bridge Tests (R206, R209–R211)
- hu_cell bridge dead (p = 0.996). No connection between nuclear Jacobian and surface 克-connectivity.
- d=1 thematic anti-correlation (R159) not structured by 五行 edge type. Controlled test p > 0.2, inconsistent sign.
- Perturbation directions are hexagram-specific: 0/30 significance tests, effective rank ~5.4/6.
- Within-pair cosines (same bit, different trigram) consistently exceed cross-pair (5/5 sources). Layer-stratified: tuan > guaci > yaoci.

### Cross-Architecture Replication (R212–R213)
- Tier 1b findings (R156, R157, R159) replicate on SikuRoBERTa (classical-Chinese BERT, architecturally distinct from prior 3 models).
- Complement mean cosine = −0.162 (p=0.0001, 27/32 negative). R² = 13.2% (elevated from 10.8–11.0% multilingual band). Hamming V-shape preserved.
- R² two-band structure: 10.8–11.0% (multilingual sentence-transformers) / 13.2% (domain-matched BERT). Domain sensitivity, not artifact.
- Cross-model ρ = 0.46–0.70. Clusters by genre proximity, not architecture type.
- Pair-level concordance (R213): complement opposition decomposes into model-invariant core (profile ρ = 0.80–0.83) and architecture-sensitive periphery (direction ρ = 0.74–0.75). ~85% geometry recoverable via Procrustes (R² = 0.83–0.86 at k=20). ~13-14 invariant + ~2-3 architecture-dependent dimensions.
- Four-model consensus confirms "text-intrinsic" for pair ranking. Remaining vulnerability: all transformer-based.

---

## Questions — Final Status

| Question | Status | Key Results |
|----------|--------|-------------|
| Q1 (unified theory of 5-ness) | **Closed (negative)** | No cyclotomic unification. φ and dual cycles are independent consequences of 5's arithmetic |
| Q2 (pentagon vs algebra) | **Closed** | R187: same Cayley graph, different readings (spectral vs adjacency) |
| Q3 (why West stopped at geometry) | **Closed** | R181–R182: n=2 → p≤3 → dual cycles impossible |
| Q4 (φ in natural systems) | **Open (out of scope)** | Untouched. Empirical, outside this investigation |
| Q5 (cyclotomic connection) | **Closed** | R183–R188: "address with conditional resonance." Two independent routes to φ converge at (3,5) only |
| Q1/Q5 reopened (φ in dynamics) | **Closed** | R197–R209: φ found in cube-edge partition (P₄∪P₄ in 克 subgraph). Fully characterized: 96/240 surjections, Jacobian-determined (R205). No bridge to text at any resolution (R206, R209) |
| Perturbation directions | **Closed** | R210–R211: rank ~5.4 (hexagram-specific). Partial bit-position alignment in relative cosines (layer-stratified, tuan strongest). Non-decomposability confirmed at d=1 |
| Tier 1b vulnerability | **Closed** | R212–R213: cross-architecture replication + pair-level concordance. ~85% geometry text-intrinsic, ~15% architecture-dependent. Vulnerability narrowed to "all transformer-based" |

---

## References

- `eastwest/findings.md` — complete findings document (R181–R213)
- `eastwest/exploration-log.md` — 11-iteration investigation log (R181–R213)
- `iching/unification/synthesis-3.md` — uniqueness theorem, orbit formula
- `iching/reversal/findings.md` — cross-cultural convergence, forcing chain (R94–R180)
- `iching/deep/number-structure.md` — the {2,3,5} prime architecture
