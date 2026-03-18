# East/West Exploration Log

## Iteration 1: The Cyclotomic Probe (Q3, Q5)

### What was tested

Three parallel computations investigating whether the golden ratio (φ) and the 五行 dual-cycle structure are connected through the cyclotomic field Q(ζ₅), plus a dimensional analysis of the Greek quaternary system.

**Computation A: (n,p) Rigidity Landscape**
- Enumerated complement-equivariant surjections F₂ⁿ → Z_p for n=2,3,4,5 across all viable primes
- Computed orbit counts under Stab(1ⁿ) × Aut(Z_p)
- Checked dual-cycle viability (≥2 independent Hamiltonian cycles on Z_p)

**Computation B: Walsh Spectra**
- Computed Walsh-Hadamard transforms W_{f,k}(ω) = Σ ζ_p^{k·f(x)} · (-1)^{⟨ω,x⟩} for all complement-equivariant surjections
- At (3,5): all 240 surjections. At (3,3) and (3,7): boundary primes. At (4,13): comparison
- Extracted spectral invariants: |W|² multisets, algebraic fields, partition dependence

**Computation C: Character Lift Geometry**
- Constructed v ∈ C⁸ via v_x = ζ₅^{f(x)} for the I Ching's surjection
- Verified complement equivariance ↔ Galois conjugation (σ: ζ₅ → ζ₅⁴)
- Computed Galois traces, norms, inner products, σ-eigenspace decomposition
- Compared with (4,13)

### What was found

**A: Rigidity Landscape**

| n | p | E | #surj | #orbits | dual? |
|---|---|---|-------|---------|-------|
| 2 | 3 | 0 | 4 | 2 | ✗ |
| 3 | 3 | 2 | 64 | 6 | ✗ |
| 3 | 5 | 1 | 240 | 5 | ✓ |
| 3 | 7 | 0 | 192 | 2 | ✓ |
| 4 | 3–13 | 1–6 | 6K–16.8M | — | varies |

- (2,3) is the only viable point at n=2. Z₃ has stride-2 ≡ stride-(−1), so 生 and 克 collapse. **The Greek dimension forces relational degeneracy.**
- (3,5) has 5 orbits: [96, 48, 48, 24, 24]. Three orbits with partition (2,2,2,1,1), two with (4,1,1,1,1). Consistent with synthesis-3 selection chain: 240 → 192 (Shape A) → 96 (Orbit C) → 1 orbit.
- n=3 is necessary and sufficient for the minimum dual-cycle system: p≥5 requires 2^{n-1} ≥ 3.

**B: Walsh Spectra**

- 5 orbits → 2 distinct spectral signatures (one per partition type). Partition determines spectrum, not orbit.
- All |W|² values at (3,5) lie in Q(√5) = Q(φ). Values expressible as (a + b√5)/2.
- At (3,3): |W|² values rational. At (3,7): values in Q(cos 2π/7) — no √5.
- W(k=1, ω=0) = φ exactly for the I Ching surjection. This is a multiplicity-dependent fact: Σ ζ₅^{f(x)} = 2·1 + 2ζ₅ + ζ₅² + ζ₅³ + 2ζ₅⁴ = 1 + (ζ₅ + ζ₅⁴) = 1 + 1/φ = φ.

**C: Character Lift Geometry**

- Complement equivariance becomes Galois conjugation: v_{x⊕7} = σ(v_x) where σ: ζ₅ → ζ₅⁴. Generic to ALL equivariant Z₅ maps.
- Galois traces per complement pair: {2, 1/φ, −φ} = {2cos(2πk/5)} for k=0,1,2.
- **Key finding — Galois trace sum distinguishes partition types:**
  - Shape A, shared pair {1,4}: Σ Tr = φ
  - Shape A, shared pair {2,3}: Σ Tr = ψ (Galois conjugate)
  - Shape B: Σ Tr = 3 (rational)
  - Under Aut(Z₅), the two Shape A cases are conjugate. **φ tags three-type coexistence.**
- Sesquilinear inner product ⟨v, σ(v)⟩ = ψ = (1−√5)/2 for the I Ching surjection.
- σ-eigenspace decomposition: ||v⁺||²/||v||² ≈ 0.461 = (17−√5)/32. Arithmetic consequence of multiplicities, no structural content.
- At (4,13): traces are 2cos(2πk/13) — no golden ratio. φ-structure is p=5-specific.

### What it means

**Q5 closed: "address, not cause."** The golden ratio and 五行 dual cycles are two faces of the 5th cyclotomic field Q(ζ₅). The connection is real but not deep:
1. **p=5-specific**: Q(ζ₅) contains Q(√5), so |W|² ∈ Q(√5). Other primes lack √5.
2. **Partition-specific**: φ marks Shape A (three-type coexistence); Shape B gives rational traces.
3. **Orientation-specific**: Which of φ, ψ depends on shared negation pair. Aut(Z₅) equates them.

The rigidity conditions ((p−3)/2)! = 1 and 2^{n-1} = n+1) are counting arguments — they do not reformulate in field-theoretic terms. Q(ζ₅) is where the structure *lives*, not what *causes* the structure.

**Q3 partially answered.** The Greek quaternary system (F₂²) forces p≤3, where dual cycles are impossible. The trigram (n=3) is the minimum dimension for relational richness. This is a mathematical fact, not cultural accident: the Western starting dimension structurally prevented 五行-type dynamics.

### Script
`memories/iching/eastwest/cyclotomic_probe.py` — Computations A, B, C.

---

## Iteration 2: Trace Generalization and Cayley Graphs (Q2, Q3, Q5 closure)

### What was tested

**Computation D: Universal Trace Formula**
- Derived and verified the Galois trace sum ΣTr across the entire E=1 family (n, p=2ⁿ−3)
- Checked whether the Shape A / Shape B discrimination generalizes beyond p=5

**Computation E: Pentagon/Pentagram as Cayley Graphs**
- Identified pentagon = Cay(Z₅, {±1}) = 生 cycle, pentagram = Cay(Z₅, {±2}) = 克 cycle
- Computed edge ratios across primes
- Verified adjacency spectrum = Galois traces

### What was found

**D: Universal Trace Formula**

For the E=1 family (n, p = 2ⁿ−3):

| Shape | ΣTr formula | Proof |
|-------|-------------|-------|
| Shape B (m₀=2) | **3** (universal) | 2·2 + Σ_{k=1}^{(p-1)/2} 2cos(2πk/p) = 4 + (−1) = 3 |
| Shape A (class j doubled) | **1 + 2cos(2πj/p)** | One trace counted twice, sum identity |

At (3,5): Shape A → {φ, ψ} — the golden ratio pair. At (4,13): six algebraic numbers in Q(cos(2π/13)), degree 6. The discrimination generalizes; the φ-structure does not.

**E: Pentagon/Pentagram Cayley Graphs**

- Pentagon = Cay(Z₅, {±1}) = 生 cycle. Pentagram = Cay(Z₅, {±2}) = 克 cycle.
- Edge ratio pentagram/pentagon = 2cos(π/5) = φ exactly. p=5-specific.
- Both have adjacency spectrum {2, 1/φ, 1/φ, −φ, −φ} — isospectral.
- The adjacency eigenvalues ARE the Galois traces: λⱼ = Tr(ζ₅^j) = 2cos(2πj/5).

### What it means

**The Cayley graph framing is presentation, not content.** The identification Cayley eigenvalues = Galois traces = 2cos(2πk/p) is definitional at every step.

**Q2 historical framing:** The Greeks studied the pentagram's *geometry* (edge ratios, self-similarity, φ as proportion). The Chinese studied Z₅'s *algebra* (生/克 as relational dynamics). These are the spectral structure and the adjacency structure of the same Cayley graph. The Greeks had the eigenvalues; the Chinese had the adjacency matrix. Neither tradition computed both.

### Script
`memories/iching/eastwest/cyclotomic_probe.py` — Computations D, E added.

---

## Iteration 3: King Wen Sequence Analysis

### What was tested

Three analyses of the King Wen (KW) ordering of 64 hexagrams, testing whether it carries structural information in binary, algebraic, or semantic dimensions.

### What was found

**Hamming Distance — no inter-pair signal** (32.6%ile). **Five-Phase Torus — no signal** (61.4%ile). **Text Embeddings — semantic smoothness detected**: tuan (99.7%) > guaci (92%) > yaoci (80%) > daxiang (76%). Binary and torus show zero inter-pair signal.

### What it means

**The KW ordering is structured in meaning-space, not in algebraic space.** Authorial confound (layer gradient correlates with discursive freedom) is not separable.

### Script
`memories/iching/eastwest/kw_sequence_probe.py`

---

## Iteration 4: Five-Phase Torus — Static Thematic Structure

### What was tested

Four analyses testing whether the five-phase torus cells carry static thematic coherence, and whether 生/克 relational dynamics predict semantic similarity.

### What was found

**Within-cell anti-signal in guaci (3.5%ile).** **Five-phase relations — no signal.** **Torus cell-pair identity captures real tuan variance** (99%ile, ~10.5% uplift) but only at fine-grained level, not through distance or relation type.

### What it means

**The texts use the five-phase partition, not the five-phase dynamics.** 生, 克, 比和 carry no semantic information.

### Script
`memories/iching/eastwest/torus_coherence.py`

---

## Iteration 5: Systematic Differentiation Test

### What was tested

Tested 12+ structural groupings across two text layers (guaci, tuan) to determine if "texts differentiate where structure groups" is a universal principle.

### What was found

**Not universal.** Only 2 of 24 grouping×layer combinations show anti-signal (surface_cell and surface_relation in guaci only).

**hu_cell (互卦 element pair) is the only cross-layer consistent predictor.** Cohesion signal in both guaci (99.4%ile) and tuan (99.5%ile). **Trigram identity predicts tuan only (99.9%ile), not guaci** — reflects commentarial practice.

### Script
`memories/iching/eastwest/differentiation_principle.py`

---

## Iteration 6: Cross-Model Validation of hu_cell (R194)

### What was tested

Cross-model validation of hu_cell semantic coherence using BGE-M3, E5-large, and LaBSE. Cached cross-model embeddings are yaoci-only (384×1024 per model), aggregated to hex level (mean of 6 lines).

### What was found

| Model | hu_cell pctile | hu_cell Δ | Status |
|-------|---------------|-----------|--------|
| **BGE-M3 (guaci)** | **99.4%** | **+0.015** | PASS |
| **BGE-M3 (tuan)** | **99.4%** | **+0.008** | PASS |
| BGE-M3 (yaoci) | 82.5% | +0.002 | FAIL |
| E5-large (yaoci) | 89.0% | +0.001 | FAIL |
| LaBSE (yaoci) | 86.5% | +0.006 | FAIL |

**Direction replicates** (positive in 5/5 models, all >80th percentile). **Magnitude doesn't reach threshold** in yaoci-aggregated models (82–89%). The yaoci aggregation compresses variance severely (σ drops from 0.08 to 0.008–0.035), making the test underpowered.

**surface_cell anti-signal does NOT replicate** — null in all yaoci models and in tuan. The guaci anti-signal was layer-specific.

### What it means

**hu_cell: stays Tier 2.** Direction is consistent but the cross-model test was underpowered due to yaoci aggregation. Would need guaci/tuan embeddings from E5-large and LaBSE for a fair test — not worth the investment given the small effect size (Δ = 0.008–0.015).

**R191 retracted.** Surface cell anti-signal does not replicate across models or layers.

### Script
`memories/iching/eastwest/hu_cell_validation.py`

---

## Iteration 7: φ in the Dynamics — Five Threads

### What was tested

Five computations probing whether φ appears in the *dynamics* of the I Ching system, testing a gap identified after the prior 6 iterations (which only examined statics — spectra, traces, partition tagging).

**Thread 2A: Full Pullback Spectra.** The surjection f = [2,2,4,0,0,1,3,3] (trigram → Z₅) lifts the pentagon (生) and pentagram (克) Cayley graphs from Z₅ to F₂³. Built 8×8 adjacency matrices for both pullbacks (x~y iff f(y)−f(x) ≡ ±1 or ±2 mod 5, regardless of Hamming distance). Also built the 5×5 quotient matrices Q = P·D where D = diag(2,1,2,2,1) encodes fiber sizes.

**Thread 2B: Cube-Edge Partition Spectra.** Partitioned the 12 edges of the 3-cube by Z₅ distance between their endpoint elements: 生 (d=±1), 克 (d=±2), 比和 (d=0). Built three 8×8 sub-adjacency matrices. Checked whether φ appears as eigenvalue of any.

**Thread 5: E=1 Family Partitions.** For n=3..8 where p = 2ⁿ−3 is prime, computed fiber partition structure. Tested whether the 3/2 doubleton/singleton ratio at (3,5) is Fibonacci-related or coincidental.

**Thread 3: Transition Balance.** Enumerated all 384 single-line hexagram transitions, classifying each by the Z₅ relation change on the affected trigram.

**Thread 4: Basin Structure.** Computed the 互 (hugua) iteration for all 64 hexagrams. Verified analytical prediction that the map is F₂-linear and everything is determined by bits 2,3 after 2 steps.

### What was found

**Thread 2A — Full pullback: φ NOT detected (proven).**

| Graph | Edges | Eigenvalues (8×8) | φ? |
|-------|-------|-------------------|-----|
| 生-pullback | 12 | {3.103, 1.146, 0.732, 0, 0, 0, −2.249, −2.732} | NO |
| 克-pullback | 13 | {3.297, 1.0, 0.787, 0, 0, 0, −2.0, −3.084} | NO |

The 5×5 quotient eigenvalues embed exactly in the 8×8 spectra, with 3 zero fiber-only eigenvalues. The fiber-size asymmetry D = diag(2,1,2,2,1) breaks any clean φ structure. The 生 and 克 pullbacks are NOT isomorphic (12 vs 13 edges) — the fiber size mismatch under α: k→2k on Z₅ prevents any bijection.

**Thread 2B — Cube-edge partition: φ DETECTED in A_克 (proven).**

| Subgraph | Edges | Structure | Eigenvalues | φ? |
|----------|-------|-----------|-------------|-----|
| A_比和 | 2 | P₂ ∪ P₂ ∪ 4·isolated | {±1, ±1, 0⁴} | NO |
| A_生 | 4 | P₃ ∪ P₃ ∪ 2·isolated | {±√2, ±√2, 0⁴} | NO |
| **A_克** | **6** | **P₄ ∪ P₄** | **{±φ, ±φ, ±1/φ, ±1/φ}** | **YES** |

Partition verified: A_生 + A_克 + A_比和 = A_cube with cube spectrum {3,1³,−1³,−3}.

The 6 克 edges form two disjoint 4-vertex paths:
- Path 1: 010—000—100—110 (Water→Earth→Wood→Metal)
- Path 2: 001—011—111—101 (Earth→Wood→Metal→Fire)

The eigenvalues of P₄ are {2cos(kπ/5) : k=1,2,3,4} = {φ, 1/φ, −1/φ, −φ}. The 5 in the denominator comes from 4+1 (Sturm-Liouville boundary condition on the path), NOT directly from Z₅.

**Remarkable progression:** Path lengths increase with Z₅ distance. The denominators are 3, 4, 5 — and only 5 produces φ.

**Thread 5 — E=1 family: Fibonacci ratio is coincidence (proven).**

| n | p | Shape A ratio (doubles/singles) |
|---|---|---------------------------------|
| 3 | 5 | 3/2 = 1.5 |
| 4 | 13 | 3/10 = 0.3 |
| 5 | 29 | 3/26 ≈ 0.115 |
| 6 | 61 | 3/58 ≈ 0.052 |

General formula: 3/(p−3) → 0. The 3/2 at (3,5) is NOT φ (1.618...) and is not special.

**Thread 3 — Transition balance: 生:克 = 2:3 (proven).**

Total: 比和=64, 生=128, 克=192. Ratio 生:克 = 2:3 exactly. No φ involvement.

Per-line breakdown: bit 0 flips produce ONLY 比和+生 (no 克). Bit 1 flips produce ONLY 克 (no 生 or 比和). Bit 2 flips produce 生+克 (no 比和). Perfect lower/upper symmetry.

**Thread 4 — Basin structure: trivially uniform (proven).**

3 attractors: fixed points {000000, 111111}, 2-cycle {010101 ↔ 101010}. Basin sizes: 16/32/16. Depth distribution: {0:4, 1:12, 2:48}. All determined by bits 2,3 of the hexagram. The hugua map is F₂-linear; H² collapses to a 2-bit space. No structural content.

### What it means

**The key surprise is Thread 2B.** φ appears in the cube-edge partition — a structure where neither the 3-cube nor the five-phase coloring individually contains √5. The φ enters through a combinatorial route (P₄ path eigenvalues) independent of the cyclotomic route (character lift, Walsh spectra) found in iterations 1–2.

**Two independent routes to φ at (3,5):**
- **Route A (cyclotomic, iterations 1–2):** Q(ζ₅)⁺ = Q(√5), so traces, Walsh spectra, and character-lift values land in Q(φ). Top-down: the number field forces φ. Unconditional — holds for all 240 surjections.
- **Route B (combinatorial, this iteration):** The 克 edges of the 3-cube decompose into P₄ paths, whose eigenvalues are 2cos(kπ/5). Bottom-up: binary geometry produces φ. Conditional — holds for the I Ching's specific surjection.

**The n=3 identity:** The eigenvalue denominator 4+1=5 comes from |V(P₄)|+1 = 2^{n-1}+1. For this to equal p = 2ⁿ−3: solving 2^{n-1}+1 = 2ⁿ−3 gives 2^{n-1} = 4, so **n=3 is the unique solution.** The two routes converge only at (3,5) because only there does the path-length boundary condition (n+1) equal the cyclotomic degree (p).

**Updated verdict: "Address with conditional resonance."** Prior verdict was "address, not cause." The new finding adds a second, structurally independent route to φ that was not anticipated. The resonance is richer than expected, but remains (3,5)-specific and conditional on the surjection.

### Script
`memories/iching/eastwest/dynamics_probe.py` — Computations 1–5.

---

## Iteration 8: Orbit Universality, Jacobian, and hu_cell Bridge

### What was tested

Five computations resolving the open questions from iteration 7: orbit universality of the P₄ decomposition, the Jacobian characterization of φ-resonance, the nuclear map connection, and the (4,13) geometric control.

**Computation 6: Full Orbit Taxonomy.** For all 240 complement-equivariant surjections at (3,5), classified into orbits under Stab(111) × Aut(Z₅), built cube-edge partition subgraphs, and classified each by connected component structure.

**Computation 7: Jacobian Types.** For each surjection, computed the "discrete Jacobian" — the set of Z₅ distance types induced by each bit direction. Classified all 240 surjections by their Jacobian type multiset.

**Computation 8: Nuclear Map × Jacobian Coincidence.** Tested whether "the nuclear map duplicates the pure-克 bit" is structurally forced or coincidental.

**Computation 9: hu_cell Bridge Test.** Tested whether hexagrams with 克-connected surface trigrams cluster within hu_cell groups — bridging Route B (φ) to the textual finding (R194).

**Computation 10: (4,13) Cube-Edge Geometry.** Computed the 克 subgraph structure on the 4-cube for a Shape A surjection at (4,13), confirming R200 geometrically.

### What was found

**Computation 6 — Orbit taxonomy: φ is NOT orbit-specific, but IS conditional.**

| Statistic | Value |
|-----------|-------|
| φ in 克 | 48/240 (20%) |
| φ in 生 | 48/240 (20%) |
| φ in neither | 144/240 (60%) |
| φ in both | 0/240 (mutual exclusion) |

The 生/克 roles are perfectly interchangeable — every structure that appears in 克 also appears in 生 with the same count. 8 distinct (生, 克, 比和) structure triples exist:

| 生 structure | 克 structure | 比和 | Count |
|---|---|---|---|
| P₄+P₄ | P₃+P₃+2I | P₂+P₂+4I | 48 |
| P₃+P₃+2I | **P₄+P₄** | P₂+P₂+4I | **48** |
| K₁,₃+K₁,₃ | P₃+P₃+2I | P₂+P₂+4I | 24 |
| P₃+P₃+2I | K₁,₃+K₁,₃ | P₂+P₂+4I | 24 |
| C₄+C₄ | P₂×4 | 8I | 24 |
| P₃+P₃+2I | G₈(8e) | 8I | 24 |
| P₂×4 | C₄+C₄ | 8I | 24 |
| G₈(8e) | P₃+P₃+2I | 8I | 24 |

Per-orbit: Orbits of size 24 (Shape B) have NO φ. Orbits of sizes 48 and 96 (Shape A) each have exactly 1/4 of their members with 克=P₄+P₄ and 1/4 with 生=P₄+P₄. The I Ching is in the size-96 orbit.

**Computation 7 — Jacobian characterization: φ ↔ pure-克 direction (proven).**

All 48 surjections with 克=P₄+P₄ share the **same Jacobian type**: {{比和,生}, {克}, {生,克}}. Having a pure-克 direction at a standard basis vector is necessary and sufficient for P₄+P₄ in 克. The I Ching's Jacobian: bit 0 = {比和,生}, bit 1 = {克} (pure), bit 2 = {生,克}.

8 distinct Jacobian types exist across all 240, perfectly correlated with the 8 structure triples.

**Computation 8 — Nuclear coincidence: NO structural coupling.**

120/240 surjections have a pure-克 direction at a standard basis bit, distributed perfectly uniformly: 48 at each of bits 0, 1, 2. The nuclear map's preference for bit 1 has no structural relationship to the Jacobian — the coincidence in the I Ching is 1-in-3.

Direction distribution across all 7 nonzero F₂³ vectors: exactly 48 surjections per direction (but 0 for the all-ones vector 111, which is fixed by Stab(111)).

**Computation 9 — hu_cell bridge: definitively dead (p = 0.996).**

12/64 hexagrams (18.75%) have 克-connected surface trigrams. The distribution across 12 hu_cell groups shows zero structure — permutation test p-value = 0.996. hu_cell carries no information about surface 克-connectivity. The hypothesized bridge from Route B (φ) to the textual finding (R194) does not exist.

**Computation 10 — (4,13) geometry: φ absent, sparse structure confirmed.**

The 克 subgraph of the 4-cube (for a Shape A surjection) has only 4 edges, forming P₂+P₂+P₂+P₂+8I. Eigenvalues: {±1⁴, 0⁸}. Eigenvalue denominator 3 ≠ 13. The fibers at (4,13) are too thin (10 singletons out of 13 elements) for extended paths. The P₄ structure at (3,5) requires the three doubleton fibers of Shape A to create "bridge" edges — a geometry that doesn't scale.

### What it means

**The φ-resonance characterization is now complete.** The Jacobian multiset {{比和,生}, {克}, {生,克}} is the necessary and sufficient condition for φ in one cycle type (R205). Which cycle type carries φ depends on which label (生 or 克) aligns with the pure direction — this is labeling-dependent. The 96/240 (2/5) resonant surjections are distributed uniformly across the three Shape A orbits.

**The complement symmetry on the P₄ paths** (analyzed in discussion, not computed) is generically forced: complement equivariance preserves Z₅ distance and is fixed-point-free on F₂³, so it must swap the two P₄ components and reverse orientation. This is R186 restated in graph language — no new content.

**The hu_cell bridge is dead.** The nuclear map's bit-duplication architecture and the surjection's Jacobian structure are structurally independent. hu_cell's textual predictive power (R194) has no connection to Route B's φ-resonance.

**The investigation has reached natural closure.** All original threads and all follow-up threads are resolved. The verdict "address with conditional resonance" is fully characterized:
- Route A (cyclotomic): unconditional, all 240 surjections, field-theoretic
- Route B (combinatorial): conditional (96/240), Jacobian-determined, Sturm-Liouville
- Convergence: unique at n=3 via the identity 2^{n-1}+1 = p
- No bridge to textual content

### Script
`memories/iching/eastwest/dynamics_probe.py` — Computations 6–10 added.

---

## Iteration 9: Edge-Type Decomposition of R159

### What was tested

The sharpest remaining test for a bridge between Route B (φ in 克 subgraph) and the textual manifold. R159 (Tier 1b, cross-model validated) established that hexagram pairs at Hamming distance 1 are MORE thematically distant than expected. This d=1 anti-correlation operates at exactly the structural resolution where Route B's φ lives — the 12 edges of the 3-cube. The question: does the 五行 type of a d=1 transition predict the strength of the thematic anti-correlation?

**Critical confound identified:** 五行 type and line position are almost perfectly entangled by the Jacobian. Lines 2,5 produce only 克 transitions; lines 3,6 produce only 比和+生. Only lines 1,4 have both 生 and 克 transitions (16 of each per line), providing a controlled comparison.

**Bit convention note:** The dynamics_probe used little-endian trigram indices; the atlas uses big-endian. In the atlas convention: hex bit 0 (line 1) corresponds to dp trigram bit 2 (生+克), hex bit 1 (line 2) to dp bit 1 (pure 克), hex bit 2 (line 3) to dp bit 0 (比和+生).

**Pass 1: Line-position decomposition.** For each of the 6 line positions, collected the 32 d=1 hexagram pairs and computed mean residual cosine distance. Cross-model (BGE-M3, E5-large, LaBSE).

**Pass 2: Controlled 五行 test.** Within lines 1 and 4 only (where both 生 and 克 occur), split 64 pairs into 32 克-pairs and 32 生-pairs. Permutation test (10K shuffles) for difference in mean thematic distance.

**Pass 3: Full 五行 decomposition.** All 192 pairs classified by 五行 type (比和=32, 生=64, 克=96). Means reported with the caveat of line-position confound.

### What was found

**Pass 1 — Line-position decomposition: no consistent gradient.**

| Model | L1 | L2 | L3 | L4 | L5 | L6 |
|-------|----|----|----|----|----|----|
| bge-m3 | 1.096 | 1.025 | 1.042 | 1.073 | 1.120 | 1.073 |
| e5-large | 1.092 | 1.043 | 1.025 | 1.079 | 1.130 | 1.071 |
| labse | 1.105 | 1.009 | 1.093 | 1.032 | 1.061 | 1.079 |

The ordering of line means changes across models. L5 tends high and L2 tends low in BGE-M3 and E5-large (both pure-克 lines), but LaBSE reverses this. No robust line-position signal. R164's "inner lines carry more thematic weight" does not manifest as a d=1 anti-correlation gradient.

**Pass 2 — Controlled test (lines 1,4: 克 vs 生): NULL.**

| Model | 克 mean (n=32) | 生 mean (n=32) | Δ(克−生) | p-value |
|-------|---------------|---------------|----------|---------|
| bge-m3 | 1.078 | 1.091 | −0.014 | 0.70 |
| e5-large | 1.086 | 1.085 | +0.001 | 0.98 |
| labse | 1.096 | 1.041 | +0.055 | 0.23 |

Sign inconsistent across models (BGE-M3 negative, others positive). No model reaches significance. The 克 vs 生 distinction produces no detectable thematic difference when line position is controlled.

**Pass 3 — Full 五行 decomposition (confounded): apparent gradient is artifact.**

| Model | 比和 (n=32) | 生 (n=64) | 克 (n=96) |
|-------|----------|----------|----------|
| bge-m3 | 1.114 | 1.046 | 1.074 |
| e5-large | 1.109 | 1.036 | 1.086 |
| labse | 1.152 | 1.030 | 1.056 |

The pattern 比和 > 克 > 生 is consistent across all 3 models but entirely explained by the line-position confound: 比和 appears only at lines 3,6; the Pass 2 controlled test shows the within-position comparison is null.

### What it means

**The bridge from Route B to text is dead at the cube-edge resolution.** This is the third independent null at the third structural resolution:

| Resolution | Test | Result |
|---|---|---|
| Torus cell (R192) | 生/克/比和 semantic information | Null |
| Nuclear hex (R206) | hu_cell × Jacobian coupling | p = 0.996 |
| Cube edge (R209) | 克 vs 生 at controlled line position | p > 0.2, inconsistent sign |

Route B (φ in 克 subgraph) is algebraically real and combinatorially interesting. It has no detectable connection to the textual manifold. This confirms the program's central finding: **the system uses addresses without using the structures at those addresses.**

### Script
`memories/iching/eastwest/edge_type_decomposition.py`

---

## Result Table (R181–R211)

| # | Finding | Tier |
|---|---------|------|
| R181 | (2,3) is the unique viable point at n=2; Z₃ supports only 1 Hamiltonian cycle → no dual dynamics | Theorem |
| R182 | n=3 is necessary and sufficient for the minimum dual-cycle system | Theorem |
| R183 | Shape A trace sum = 1+2cos(2πj/p); Shape B trace sum = 3. Universal for E=1 family | Theorem |
| R184 | At (3,5): Shape A trace sum ∈ {φ,ψ}, tagging three-type coexistence with golden-ratio arithmetic. p=5-specific | Theorem |
| R185 | |W|² ∈ Q(√5) at p=5, Q at p=3, Q(cos 2π/7) at p=7. φ-connection tracks cyclotomic field, not rigidity | Theorem |
| R186 | Complement equivariance ↔ Galois conjugation on Q(ζ₅): generic to all equivariant Z_p maps | Theorem |
| R187 | Pentagon = Cay(Z₅,{±1}) = 生; Pentagram = Cay(Z₅,{±2}) = 克; edge ratio = φ = 2cos(π/5) | Theorem |
| R188 | Q(ζ₅) is shared address of φ and dual cycles, not shared cause. Final: "address with conditional resonance" | Interpretation |
| R189 | KW semantic smoothness is layer-stratified: tuan (99.7%) > guaci (92%) > yaoci (80%) > daxiang (76%). Binary and torus show no inter-pair signal | Measurement |
| R190 | Layer gradient correlates with discursive freedom, not traditional dating. Authorial confound not separable | Measurement |
| R191 | ~~Surface cell anti-signal~~ **RETRACTED** — does not replicate across models or layers | — |
| R192 | Five-phase relation labels (生/克/比和) carry no semantic information in either text layer | Measurement |
| R193 | Torus cell-pair identity captures real tuan variance (99%ile, ~10.5% uplift) but not through distance or relation type | Measurement |
| R194 | hu_cell predicts semantic similarity in guaci (99.4%) and tuan (99.5%); direction positive 5/5 models, yaoci inconclusive. Tier 2 | Measurement |
| R195 | Trigram identity predicts tuan (99.9%ile) but not guaci — layer-dependent, commentarial practice | Measurement |
| R196 | Systematic differentiation test: 2/24 anti-signal. No universal differentiation principle | Measurement |
| R197 | Full pullback (f-lifted Cayley graphs on F₂³): φ NOT detected. 生/克 pullbacks are non-isomorphic (12 vs 13 edges). Quotient eigenvalues embed with 3 zero fiber-only eigenvalues | Theorem |
| R198 | Cube-edge partition: A_克 spectrum = {±φ, ±φ, ±1/φ, ±1/φ}. The 克 subgraph of the 3-cube is P₄ ∪ P₄; φ enters via 2cos(kπ/5) where 5 = path length + 1 | Theorem |
| R199 | Path-length progression: 比和→P₂ (cos kπ/3), 生→P₃ (cos kπ/4), 克→P₄ (cos kπ/5). Only 克 produces φ | Theorem |
| R200 | The n=3 identity: 2^{n-1}+1 = 2ⁿ−3 = p holds uniquely at n=3. Two independent routes to φ (cyclotomic + combinatorial) converge only at (3,5) | Theorem |
| R201 | Transition balance: 比和:生:克 = 1:2:3 across all 384 hexagram line transitions. Bit-stratified by line position | Theorem |
| R202 | E=1 family fiber ratio: 3/(p−3) → 0. The 3/2 ratio at (3,5) is not Fibonacci-related | Theorem |
| R203 | Basin structure is trivial: F₂-linear map, determined by bits 2,3, depths {0:4, 1:12, 2:48} | Theorem |
| R204 | 96/240 surjections (2/5) have φ in one cycle type. 48 克 + 48 生, mutual exclusion. Perfect 生↔克 mirror symmetry | Theorem |
| R205 | φ ↔ Jacobian multiset {{比和,生},{克},{生,克}} with pure direction at basis vector. Necessary and sufficient | Theorem |
| R206 | Nuclear map × Jacobian: no structural coupling. hu_cell bridge dead (p=0.996). Pure-克 direction uniform across all 6 non-111 F₂³ vectors | Measurement |
| R207 | (4,13): 克 = P₂⁴ + 8I. Denominator 3 ≠ 13. φ absent — fibers too thin for extended paths | Theorem |
| R208 | Full taxonomy: 8 structure triples at (3,5), perfect 生↔克 mirror symmetry. 比和 = P₂+P₂+4I or 8I | Theorem |
| R209 | d=1 thematic anti-correlation (R159) not structured by 五行 edge type. Controlled test at lines 1,4: p > 0.2, inconsistent sign across 3 models. Route B → text bridge dead at cube-edge resolution | Measurement |
| R210 | Single-line perturbation directions are hexagram-specific. No consistent mean direction at any line position (0/30 significance tests). 6×D displacement matrix has effective rank ~5.4/6, σ₁/σ₂ ≈ 1.15. Cross-model validated (5/5 sources) | Measurement |
| R211 | Within-pair perturbation cosines (same bit position, different trigram) consistently exceed cross-pair cosines (5/5 sources, Δ = +0.06 to +0.31). Layer-stratified: tuan (+0.27) > guaci (+0.12) > yaoci (+0.03–0.06). Consistent with R195. Note: bit 1 (the pure-克 direction, algebraically special per R205) shows guaci −0.01 / tuan +0.32 — the algebraically special bit position is textually most opaque in the primary layer | Measurement |

## Question Status

| Question | Status | Key Results |
|----------|--------|-------------|
| Q1 (unified theory of 5-ness) | **Closed (negative)** | No cyclotomic unification. φ and dual cycles are independent consequences of 5's arithmetic |
| Q2 (pentagon vs algebra) | **Closed** | R187: same Cayley graph, different readings (spectral vs adjacency) |
| Q3 (why West stopped at geometry) | **Closed** | R181–R182: n=2 → p≤3 → dual cycles impossible |
| Q4 (φ in natural systems) | **Open** | Untouched. Empirical, outside scope |
| Q5 (cyclotomic connection) | **Closed** | R183–R188: "address with conditional resonance." Two independent routes to φ converge at (3,5) only |
| Q1/Q5 reopened (φ in dynamics) | **Closed** | R197–R209: φ in cube-edge partition. No bridge to text at any resolution. Fully characterized |

| Perturbation directions | **Closed** | R210–R211: rank ~5.4 (hexagram-specific). Partial bit-position alignment in relative cosines (layer-stratified). Non-decomposability confirmed at d=1 |

## Scripts

| Script | Computations |
|--------|-------------|
| `cyclotomic_probe.py` | A–E: rigidity, Walsh spectra, character lift, trace formula, Cayley graphs |
| `kw_sequence_probe.py` | KW Hamming, torus trajectory, text embedding trajectory |
| `torus_coherence.py` | Within-cell similarity, five-phase relations, torus distance, variance decomposition |
| `differentiation_principle.py` | Systematic grouping test across 12+ features |
| `hu_cell_validation.py` | Cross-model validation of hu_cell |
| `dynamics_probe.py` | Pullback spectra, cube-edge partition, E=1 family, transition balance, basin structure, orbit taxonomy, Jacobian types, nuclear coincidence, hu_cell bridge, (4,13) geometry |
| `edge_type_decomposition.py` | R159 decomposition by line position and 五行 edge type, cross-model validated |
| `perturbation_directions.py` | Mean displacement norms, SVD rank, cosine similarity matrix, within-pair analysis, cross-model validation |
---

## Iteration 10: Perturbation Direction Decomposition

### What was tested

Whether single-line perturbations push hexagrams in CONSISTENT DIRECTIONS in embedding space, and whether different line positions push in DIFFERENT directions. All prior d=1 tests measured magnitude (how far does a perturbation push). This tests direction (which way does it push in the ~16-dimensional thematic space).

**Critical correction:** The naive mean displacement Σ_h [embed(h⊕mask) − embed(h)] is identically zero by symmetry (h→h⊕mask is a bijection). The computation uses canonical 32-pair displacements: for each line position, group the 64 hexagrams into 32 pairs {h₀, h₁} where h₀ has bit=0 and h₁ has bit=1, compute embed(h₁) − embed(h₀).

Five embedding sources: BGE-M3 guaci (64×1024), BGE-M3 tuan (64×1024), BGE-M3 yaoci centroids (64×1024), E5-large yaoci centroids (64×1024), LaBSE yaoci centroids (64×768). All raw embeddings (not residuals).

**Computation 1+2: Mean displacement norms + significance.** For each line position and source, computed the mean of 32 displacement vectors and its norm. Permutation test (10K shuffles) for significance.

**Computation 3: SVD of the 6×D mean displacement matrix.** The singular value spectrum directly measures how many independent perturbation directions exist: rank 1 = single axis, rank 3 = bit-position-specific, rank 6 = all independent.

**Computation 4+5: 6×6 cosine similarity matrix + within-pair cosines.** The cosine between mean displacements for lines i and j measures whether those line positions push in similar directions. Within-pair cosines (L1↔L4, L2↔L5, L3↔L6) test whether same-bit-position lines in different trigrams perturb similarly.

**Computation 6: Angular diversity null model.** Bootstrap test for whether the 6 directions are more or less diverse than expected under resampling noise.

### What was found

**Computation 1+2 — Mean displacements: NOT significant (0/30 tests).**

All p-values > 0.3 across all 6 lines × 5 sources. The ratio ‖mean‖/mean(‖individual‖) ≈ 0.17, consistent with √(1/32) ≈ 0.18 expected for random unit vectors. Individual perturbation displacements are large (‖δ‖ ≈ 0.3–0.9) but point in near-random directions, so the mean collapses. No line position has a consistent perturbation direction.

**Computation 3 — SVD: effective rank ~5.4/6.**

| Source | σ₁/σ₂ | Participation Ratio |
|--------|--------|-------------------|
| bge-m3 guaci | 1.25 | 5.14 |
| bge-m3 tuan | 1.17 | 5.26 |
| bge-m3 yaoci | 1.04 | 5.54 |
| e5-large yaoci | 1.06 | 5.69 |
| labse yaoci | 1.23 | 5.37 |

Mean participation ratio = 5.40. Mean σ₁/σ₂ = 1.15. The 6 mean displacement vectors are nearly equi-normed and nearly independent — they span all 6 available dimensions almost uniformly. No dominant perturbation axis exists.

**Computation 4+5 — Cosine structure: within-pair > cross-pair (consistently).**

Within-pair cosines (same bit position, different trigram):

| Source | bit 0 (L1↔L4) | bit 1 (L2↔L5) | bit 2 (L3↔L6) | Mean within | Mean cross | Δ |
|--------|---------|---------|---------|-------------|------------|-------|
| bge-m3 guaci | +0.18 | −0.01 | +0.20 | +0.12 | +0.07 | +0.06 |
| bge-m3 tuan | +0.24 | +0.32 | +0.25 | +0.27 | −0.04 | +0.31 |
| bge-m3 yaoci | +0.09 | +0.16 | −0.10 | +0.05 | −0.07 | +0.12 |
| e5-large yaoci | +0.13 | +0.13 | −0.07 | +0.06 | −0.06 | +0.12 |
| labse yaoci | +0.04 | +0.16 | −0.11 | +0.03 | −0.04 | +0.07 |

Within > cross in ALL 5 sources. Tuan shows the strongest effect (within = +0.27 vs cross = −0.04, Δ = +0.31). Bits 0 and 1 are consistently positive; bit 2 is inconsistent across models.

**Computation 6 — Angular diversity: not significant (0/5 sources).**

The 6 directions are diverse (nearly orthogonal) but this diversity is expected from 6 vectors in high-dimensional space — no evidence of extra diversity or extra alignment beyond sampling noise.

### What it means

**The perturbation geometry is predominantly hexagram-specific.** No individual line position has a consistent mean perturbation direction (R210). The 6×D mean displacement matrix has effective rank ~5.4, meaning all 6 line-perturbations push in nearly independent directions. There is no dominant "differentiation axis" — the R159 anti-correlation is not directionally coherent.

**But bit-position identity partially determines perturbation direction (R211).** Same-bit-position perturbations (e.g., flipping line 2 vs flipping line 5 — both change the middle line of their respective trigram) produce more similar displacements than cross-position perturbations. This is a RELATIVE alignment effect, not an absolute direction. The layer stratification (tuan > guaci > yaoci) is consistent with R195: tuan commentarial practice more explicitly encodes trigram-line-position semantics.

**Non-decomposability inventory is now complete:**
- d=1 (R210): perturbation directions full-rank, hexagram-specific
- d=6 (R167): complement opposition doesn't factor through trigrams
- All algebraic groupings (R170): no labels sort directions
- Partial structure: bit-position signature in relative alignment (R211), strongest in commentarial layer

### Script
`memories/iching/eastwest/perturbation_directions.py`

---

## Iteration 11: Cross-Architecture Replication (SikuRoBERTa)

### What was tested

Whether the three Tier 1b findings (R156 complement anti-correlation, R157 algebraic R², R159 Hamming V-shape) — previously validated across three multilingual sentence-transformers (BGE-M3, E5-large, LaBSE) — replicate on SikuRoBERTa, a classical-Chinese BERT model architecturally distinct from all prior models.

**Why this matters:** The acknowledged vulnerability of all Tier 1b findings was that the three validating models share architectural assumptions: all are multilingual sentence-transformers fine-tuned on similarity tasks. SikuRoBERTa breaks that shared assumption on four axes:
- **Training data:** Classical Chinese corpus (四库全书) vs multilingual web
- **Training objective:** Masked language model vs contrastive similarity
- **Architecture:** BERT-base (12 layers, 768 dims) vs various larger encoders (1024 dims)
- **Embedding method:** Mean-pooled last hidden layer (excluding [CLS]/[SEP]) vs fine-tuned sentence pooling

**Methodological consideration:** Raw BERT mean-pooling produces anisotropic embeddings (cosine similarities compressed toward 1.0). This affects absolute magnitudes but NOT relative comparisons. All three tests use permutation-based nulls, so the signal-to-null ratio is preserved under uniform compression. An effective-dimensionality diagnostic (participation ratio) was run to confirm the embeddings are not degenerate.

**Procedure:**
1. Extract 384 yaoci embeddings via SikuRoBERTa last hidden layer, mean-pooled, L2-normalized → (384, 768)
2. Compute participation ratio of covariance matrix (adequacy diagnostic)
3. Replicate R156: complement-pair residual cosines (32 pairs, 10K permutations)
4. Replicate R157: OLS regression R² with full design matrix
5. Replicate R159: Hamming distance spectrum of pairwise residual cosine distances
6. Cross-model Spearman ρ on 64×64 distance matrices

### What was found

**Diagnostic: adequate embedding quality.**

| Metric | SikuRoBERTa | BGE-M3 (baseline) |
|--------|-------------|-------------------|
| Participation ratio | 50.0 | 65.9 |
| Mean pairwise cosine | 0.654 | — |
| σ₁/σ₂ | 1.37 | 1.26 |

PR = 50 — exactly at the pre-specified adequacy threshold. Mean pairwise cosine 0.654 (far from 0.95 degeneracy marker). No whitening needed. Slightly more concentrated than BGE-M3 but not degenerate.

**R156 (complement anti-correlation): REPLICATED.**

| Metric | SikuRoBERTa | Prior (3 models) |
|--------|-------------|------------------|
| Mean residual cosine | −0.162 | ≈ −0.19 |
| Negative pairs | 27/32 | 28–29/32 |
| p-value | 0.0001 | < 0.001 |

Direction and significance preserved. Slightly weaker magnitude (−0.162 vs −0.19) and one fewer negative pair.

**R157 (algebraic R²): REPLICATED (with notable elevation).**

| Metric | SikuRoBERTa | Prior (3 models) |
|--------|-------------|------------------|
| R² | 13.2% | 10.8–11.0% |

Within the [5%, 15%] replication window. The 2pp elevation above the tight multilingual band is interpreted as domain sensitivity: SikuRoBERTa's classical Chinese training better represents the vocabulary patterns that correlate with algebraic coordinates.

**R159 (Hamming V-shape): REPLICATED.**

| d | SikuRoBERTa | Pattern |
|---|-------------|---------|
| 1 | 1.055 | ← highest (non-complement) |
| 2 | 1.040 | |
| 3 | 0.991 | |
| 4 | 1.015 | |
| 5 | 0.976 | |
| 6 | 1.162 | ← complement spike |

d=1 > d=2 > d=3. V-shape preserved.

**Cross-model correlation: moderate agreement.**

| Pair | Spearman ρ |
|------|-----------|
| bge-m3 ↔ e5-large | 0.868 |
| bge-m3 ↔ sikuroberta | 0.679 |
| e5-large ↔ sikuroberta | 0.703 |
| bge-m3 ↔ labse | 0.633 |
| e5-large ↔ labse | 0.535 |
| labse ↔ sikuroberta | 0.461 |

SikuRoBERTa correlates more strongly with BGE-M3/E5-large than LaBSE does with either. The ρ matrix clusters by genre proximity to classical Chinese, not by architecture type.

### What it means

**All three Tier 1b findings replicate.** Four-model consensus across distinct training data, objectives, architectures, and embedding methods confirms "text-intrinsic" classification. The remaining vulnerability narrows to: all models are transformer-based neural networks. Breaking that would require non-neural approaches (classical NLP, topic models, manual annotation) — a different research program.

**R² two-band structure (proven):** The tight 10.8–11.0% band across multilingual models was measuring "algebraic variance accessible through multilingual embeddings of classical Chinese." SikuRoBERTa's 13.2% measures "algebraic variance accessible through classical-Chinese-native embeddings." The extra 2pp is vocabulary signal multilingual models partially miss. R157 should be reported as two bands: 10.8–11.0% (multilingual) and 13.2% (domain-matched). The tight multilingual band is itself a finding (model-invariance within that class).

**Genre proximity > architecture type (observed).** The cross-model ρ matrix reveals that LaBSE (trained on parallel Bible translations) agrees LESS with SikuRoBERTa (classical Chinese literary corpus) than BGE-M3/E5-large do. Genre proximity to the target corpus matters more than training objective (contrastive vs masked LM) for structural agreement.

### Script
`memories/iching/eastwest/sikuroberta_replication.py`

---

## Iteration 12: Pair-Level Concordance (R213)

### What was tested

Whether SikuRoBERTa agrees with prior models on WHICH specific complement pairs oppose most strongly and in WHICH directions. R212 tested aggregate replication (mean anti-correlation, total R², Hamming spectrum). This tests pair-level resolution — the finest grain at which "text-intrinsic" can be verified.

**Methodology (matching phase 8b exactly):**
1. Computed residual centroids for all 4 models (algebraic signal regressed out via OLS)
2. Built 32 complement-pair unit difference vectors per model
3. Direction concordance: Spearman ρ on 32×32 cosine similarity matrices of unit difference vectors
4. Procrustes alignment: PCA-reduce to k dimensions, orthogonal Procrustes rotation, R² at k=5,8,10,15,20
5. Profile concordance: Spearman ρ on 32-element vectors of complement-pair residual cosines

### What was found

**Direction concordance (32×32 cosine matrices):**

|  | bge-m3 | e5-large | labse | sikuroberta |
|--|--------|----------|-------|-------------|
| bge-m3 | — | 0.884 | 0.779 | 0.750 |
| e5-large | | — | 0.763 | 0.743 |
| labse | | | — | 0.735 |
| sikuroberta | | | | — |

SikuRoBERTa ρ range: 0.735–0.750. Prior minimum: LaBSE↔E5 = 0.763. Gap: 0.03 below prior minimum.

**Procrustes R² at k=20:**

| Pair | R² |
|------|-----|
| bge↔e5 | 0.949 |
| bge↔labse | 0.873 |
| bge↔siku | 0.859 |
| e5↔labse | 0.849 |
| e5↔siku | 0.854 |
| labse↔siku | 0.832 |

~85% of complement-pair opposition geometry recoverable across architectures.

**Profile concordance (which pairs oppose most/least):**

|  | bge-m3 | e5-large | labse | sikuroberta |
|--|--------|----------|-------|-------------|
| bge-m3 | — | 0.961 | 0.863 | 0.830 |
| e5-large | | — | 0.821 | 0.833 |
| labse | | | — | 0.800 |
| sikuroberta | | | | — |

SikuRoBERTa ρ range: 0.800–0.833. Passes the 0.78 threshold.

**Three-level gradient:**

| Level | Metric | SikuRoBERTa range | Prior range |
|-------|--------|-------------------|-------------|
| Which pairs oppose? | Profile ρ | 0.80–0.83 | 0.82–0.96 |
| How much geometry aligns? | Procrustes R² (k=20) | 0.83–0.86 | 0.85–0.95 |
| Which directions? | Direction ρ | 0.74–0.75 | 0.76–0.88 |

**Largest pair-level discrepancies:**

| Pair | SikuRoBERTa cos | Multilingual cos | Note |
|------|-----------------|------------------|------|
| 蹇↔睽 | −0.061 | −0.245 | Siku sees much less opposition |
| 坎↔離 | −0.235 | −0.110 | Siku sees much more opposition |
| 解↔旅 | −0.292 | −0.219 | Moderate difference |

坎↔離 (Kan↔Li, Water↔Fire) is the canonical complement pair in the tradition. SikuRoBERTa, trained on 四库全书 with extensive commentarial literature, sees stronger Kan/Li opposition — a training-data confound, not a text property. This illustrates the mechanism: the architecture-dependent fraction correlates with cultural salience in training corpora.

### What it means

**The complement opposition has a two-component structure:** a model-invariant core (pair ranking, ρ = 0.80–0.83) and an architecture-sensitive periphery (angular direction, ρ = 0.74–0.75). The ~16 opposition dimensions decompose into ~13-14 cross-architecture invariant dimensions plus ~2-3 architecture-dependent dimensions.

"Text-intrinsic" is confirmed for the pair-level opposition ranking. The full high-dimensional angular structure is ~85% text-intrinsic, ~15% architecture-dependent. The architecture-dependent fraction correlates with training-data cultural emphasis (e.g., Kan↔Li amplification in classical Chinese corpora), not with text content.

The sage predicted ρ ≈ 0.55–0.65; actual was 0.74–0.75. The text signal constrains opposition directions more tightly than expected even across fundamentally different architectures — itself the strongest evidence for "text-intrinsic."

### Script
`memories/iching/eastwest/pair_concordance.py`

---

## Result Table (R181–R213)

| # | Finding | Tier |
|---|---------|------|
| R181 | (2,3) is the unique viable point at n=2; Z₃ supports only 1 Hamiltonian cycle → no dual dynamics | Theorem |
| R182 | n=3 is necessary and sufficient for the minimum dual-cycle system | Theorem |
| R183 | Shape A trace sum = 1+2cos(2πj/p); Shape B trace sum = 3. Universal for E=1 family | Theorem |
| R184 | At (3,5): Shape A trace sum ∈ {φ,ψ}, tagging three-type coexistence with golden-ratio arithmetic. p=5-specific | Theorem |
| R185 | |W|² ∈ Q(√5) at p=5, Q at p=3, Q(cos 2π/7) at p=7. φ-connection tracks cyclotomic field, not rigidity | Theorem |
| R186 | Complement equivariance ↔ Galois conjugation on Q(ζ₅): generic to all equivariant Z_p maps | Theorem |
| R187 | Pentagon = Cay(Z₅,{±1}) = 生; Pentagram = Cay(Z₅,{±2}) = 克; edge ratio = φ = 2cos(π/5) | Theorem |
| R188 | Q(ζ₅) is shared address of φ and dual cycles, not shared cause. Final: "address with conditional resonance" | Interpretation |
| R189 | KW semantic smoothness is layer-stratified: tuan (99.7%) > guaci (92%) > yaoci (80%) > daxiang (76%). Binary and torus show no inter-pair signal | Measurement |
| R190 | Layer gradient correlates with discursive freedom, not traditional dating. Authorial confound not separable | Measurement |
| R191 | ~~Surface cell anti-signal~~ **RETRACTED** — does not replicate across models or layers | — |
| R192 | Five-phase relation labels (生/克/比和) carry no semantic information in either text layer | Measurement |
| R193 | Torus cell-pair identity captures real tuan variance (99%ile, ~10.5% uplift) but not through distance or relation type | Measurement |
| R194 | hu_cell predicts semantic similarity in guaci (99.4%) and tuan (99.5%); direction positive 5/5 models, yaoci inconclusive. Tier 2 | Measurement |
| R195 | Trigram identity predicts tuan (99.9%ile) but not guaci — layer-dependent, commentarial practice | Measurement |
| R196 | Systematic differentiation test: 2/24 anti-signal. No universal differentiation principle | Measurement |
| R197 | Full pullback (f-lifted Cayley graphs on F₂³): φ NOT detected. 生/克 pullbacks are non-isomorphic (12 vs 13 edges). Quotient eigenvalues embed with 3 zero fiber-only eigenvalues | Theorem |
| R198 | Cube-edge partition: A_克 spectrum = {±φ, ±φ, ±1/φ, ±1/φ}. The 克 subgraph of the 3-cube is P₄ ∪ P₄; φ enters via 2cos(kπ/5) where 5 = path length + 1 | Theorem |
| R199 | Path-length progression: 比和→P₂ (cos kπ/3), 生→P₃ (cos kπ/4), 克→P₄ (cos kπ/5). Only 克 produces φ | Theorem |
| R200 | The n=3 identity: 2^{n-1}+1 = 2ⁿ−3 = p holds uniquely at n=3. Two independent routes to φ (cyclotomic + combinatorial) converge only at (3,5) | Theorem |
| R201 | Transition balance: 比和:生:克 = 1:2:3 across all 384 hexagram line transitions. Bit-stratified by line position | Theorem |
| R202 | E=1 family fiber ratio: 3/(p−3) → 0. The 3/2 ratio at (3,5) is not Fibonacci-related | Theorem |
| R203 | Basin structure is trivial: F₂-linear map, determined by bits 2,3, depths {0:4, 1:12, 2:48} | Theorem |
| R204 | 96/240 surjections (2/5) have φ in one cycle type. 48 克 + 48 生, mutual exclusion. Perfect 生↔克 mirror symmetry | Theorem |
| R205 | φ ↔ Jacobian multiset {{比和,生},{克},{生,克}} with pure direction at basis vector. Necessary and sufficient | Theorem |
| R206 | Nuclear map × Jacobian: no structural coupling. hu_cell bridge dead (p=0.996). Pure-克 direction uniform across all 6 non-111 F₂³ vectors | Measurement |
| R207 | (4,13): 克 = P₂⁴ + 8I. Denominator 3 ≠ 13. φ absent — fibers too thin for extended paths | Theorem |
| R208 | Full taxonomy: 8 structure triples at (3,5), perfect 生↔克 mirror symmetry. 比和 = P₂+P₂+4I or 8I | Theorem |
| R209 | d=1 thematic anti-correlation (R159) not structured by 五行 edge type. Controlled test at lines 1,4: p > 0.2, inconsistent sign across 3 models. Route B → text bridge dead at cube-edge resolution | Measurement |
| R210 | Single-line perturbation directions are hexagram-specific. No consistent mean direction at any line position (0/30 significance tests). 6×D displacement matrix has effective rank ~5.4/6, σ₁/σ₂ ≈ 1.15. Cross-model validated (5/5 sources) | Measurement |
| R211 | Within-pair perturbation cosines (same bit position, different trigram) consistently exceed cross-pair cosines (5/5 sources, Δ = +0.06 to +0.31). Layer-stratified: tuan (+0.27) > guaci (+0.12) > yaoci (+0.03–0.06). Bit 1 (pure-克, algebraically special) shows guaci −0.01 / tuan +0.32 — algebraically special bit is textually most opaque in primary layer | Measurement |
| R212 | Tier 1b cross-architecture replication: R156, R157, R159 all replicate on SikuRoBERTa (classical-Chinese BERT). Complement mean cosine = −0.162 (p=0.0001, 27/32 negative). R² = 13.2% (elevated from 10.8–11.0% multilingual band — domain sensitivity). Hamming V-shape preserved. Cross-model ρ = 0.46–0.70. Four-model consensus confirms "text-intrinsic" | Tier 1b |
| R213 | Pair-level concordance: complement opposition decomposes into model-invariant core (profile ρ = 0.80–0.83) and architecture-sensitive periphery (direction ρ = 0.74–0.75). Procrustes R² = 0.83–0.86 at k=20 (~85% geometry recoverable). ~13-14 cross-architecture invariant dimensions + ~2-3 architecture-dependent. Largest discrepancies (Kan↔Li, Jian↔Kui) correlate with training-data cultural salience | Tier 1b (pair ranking) / Tier 2 (angular structure) |

## Question Status

| Question | Status | Key Results |
|----------|--------|-------------|
| Q1 (unified theory of 5-ness) | **Closed (negative)** | No cyclotomic unification. φ and dual cycles are independent consequences of 5's arithmetic |
| Q2 (pentagon vs algebra) | **Closed** | R187: same Cayley graph, different readings (spectral vs adjacency) |
| Q3 (why West stopped at geometry) | **Closed** | R181–R182: n=2 → p≤3 → dual cycles impossible |
| Q4 (φ in natural systems) | **Open** | Untouched. Empirical, outside scope |
| Q5 (cyclotomic connection) | **Closed** | R183–R188: "address with conditional resonance." Two independent routes to φ converge at (3,5) only |
| Q1/Q5 reopened (φ in dynamics) | **Closed** | R197–R209: φ in cube-edge partition. No bridge to text at any resolution. Fully characterized |
| Perturbation directions | **Closed** | R210–R211: rank ~5.4 (hexagram-specific). Non-decomposability confirmed at d=1 |
| Tier 1b vulnerability | **Closed** | R212–R213: cross-architecture replication + pair-level concordance. ~85% geometry text-intrinsic, ~15% architecture-dependent |

## Scripts

| Script | Computations |
|--------|-------------|
| `cyclotomic_probe.py` | A–E: rigidity, Walsh spectra, character lift, trace formula, Cayley graphs |
| `kw_sequence_probe.py` | KW Hamming, torus trajectory, text embedding trajectory |
| `torus_coherence.py` | Within-cell similarity, five-phase relations, torus distance, variance decomposition |
| `differentiation_principle.py` | Systematic grouping test across 12+ features |
| `hu_cell_validation.py` | Cross-model validation of hu_cell |
| `dynamics_probe.py` | Pullback spectra, cube-edge partition, E=1 family, transition balance, basin structure, orbit taxonomy, Jacobian types, nuclear coincidence, hu_cell bridge, (4,13) geometry |
| `edge_type_decomposition.py` | R159 decomposition by line position and 五行 edge type, cross-model validated |
| `perturbation_directions.py` | Mean displacement norms, SVD rank, cosine similarity matrix, within-pair analysis, cross-model validation |
| `sikuroberta_replication.py` | Cross-architecture replication of R156/R157/R159 on classical-Chinese BERT |
| `pair_concordance.py` | Pair-level direction concordance, Procrustes alignment, profile concordance across 4 models |
