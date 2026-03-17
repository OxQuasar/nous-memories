# I Ching Research — Directory

## Program Overview

An investigation of the I Ching's algebraic structure, producing 77 results across 10 workflows. Central finding: the 五行 assignment is a complement-respecting surjection F₂³ → Z₅ — the unique rigid point in an infinite family. The orbit formula Orbits(n,p) = ((p−3)/2)! × 2^{2^{n−1}−1−n} equals 1 if and only if (n,p) = (3,5).

---

## Core Workflows (definitive)

### `deep/`
**The foundational exploration.** 9 iterations tracing from two axioms (binary substrate + two independent cycles) to the complete parameter derivation. Establishes: why 5 elements (smallest prime with two independent cycles), why 3 lines (dimensional forcing theorem), why this assignment (zero free parameters), why these compass arrangements (先天 = Z₂ optimum, 後天 = {2,3,5} triple junction), KW pairing uniqueness (basin-preservation maximum).
- `exploration-log.md` — iteration-by-iteration record (R32–R42)
- `open-questions.md` — complete results inventory (R1–R72)
- `number-structure.md` — the {2, 3, 5} prime architecture

### `unification/`
**The uniqueness theorem.** Three phases: (1) PG(2,F₂) framework — the Fano plane decorated with one compass, (2) (n,p) landscape — singleton-forcing, E=1 family, selection chain, (3) the uniqueness proof — orbit formula, Reed-Muller connection, 0.5-bit is presentational.
- `unification.md` — primary document, Phase 3 status
- `synthesis-3.md` — definitive account (519 lines, 15 theorems T1–T15, supersedes synthesis-1/2)
- `synthesis-2.md` — Phase 2 account (landscape, eigenstructure)
- `synthesis-1.md` — Phase 1 account (PG(2,F₂), 17 results)
- `phase1-unification.md` — the (3,5) framework + I Ching mapping

### `semantic-map/`
**Text-algebra interface.** Bottom-up analysis of all textual layers. 89% of text is algebraically independent. Two bridges survive position control (CMH): 凶×basin (core, OR=4.25) and 吉×生体 (shell, OR=2.19). Commentary layers are non-algebraic: 大象 imagistic, 彖傳 binary-structural (Z₂), 小象 positional. Three historical registers map to three primes.
- `findings.md` — complete findings

### `relations/`
**Isolation proof.** Cross-domain investigation proving the (3,5) object doesn't generalize. Three-level specificity chain: char=2 required (theorem), |F_q|=2 required (GL Maximization), (n,p)=(3,5) required (orbit formula). All comparisons negative: genetic code (no equivariance), F₃/F₄ (many orbits), design theory (dead end). "Self-interpreting code" closed as verbal analogy.
- `findings.md` — complete findings (R62–R68)

### `kw-final/`
**King Wen pair ordering.** Monte Carlo (50K orderings) under correct null model shows no metric discriminates KW. R41 corrected (basin clustering was artifact of wrong null). The ordering is **designed but not algebraically determined** — the unique point of human authorship. Principle is narrative (序卦傳), not algebraic.
- `findings.md` — complete findings (R61)

### `i-summary/`
**Final investigation + master summary.** Resolves Q4 (three-tier coupling, not just two bridges), Q5 (彖傳 anomaly detection), Q8 (no name in existing mathematics — definitive negative). Proves nuclear rank formula for all n ≥ 2. Characterizes (4,13) moduli space via Hamming syndrome structure.
- `summary.md` — master summary of entire research program
- `exploration-log.md` — iteration record (R69–R72)
- `findings.md` — complete findings
- `work/` — computation scripts and proof documents
- `work/proof_nuclear_rank.md` — formal proof of rank(M^k) = max(2, 2n−2k)

### `reversal/`
**The inward turn.** 87 results (R94–R180) across 19 iterations, reversing the program's direction: from analyzing the object to inhabiting it. Four investigations, all closed.

**Q1 — The Residual (R112–R170):** The 89% of text that algebra can't see is a smooth ~16-dimensional thematic manifold, cross-model validated (BGE-M3, E5-large, LaBSE). No clusters. The complement involution is the sole organizing principle — an antipodal map where each pair opposes along its own unique axis. Quadruple dissociation: algebra, vocabulary, 象 categories, and syntactic frames all return null against embedding geometry. The residual is sub-syntactic and non-decomposable. Near-neighbor differentiation and holistic composition produce a V-shaped Hamming spectrum. All algebraic groupings (Fano lines, 五行, basins, trigram decomposition) null against opposition direction.

**Q2 — The Axioms (R73–R111, R171–R175):** The forcing chain has exactly one gap: composability (the group axiom). Without it, a bare 6-element set suffices. With it, F₂³ and (3,5) are forced. The gap is irreducible. Cross-culturally: binary converges (≥3 traditions), five-fold partially converges (China/India), dual-cycle surjection is unique to China.

**Q3 — The Judgment Boundary (R140–R150):** Five judgment operations (analogy 40%, integration 19%, external 19%, weighting 17.5%, exception 5%), invariant across 梅花 and 火珠林. Three-phase sequence: read → assess → anchor. The system explicitly formalizes its own specification gap.

**Resonance Test 3 (R176–R180):** {4,2,2,2,2} appears in climate data but structural predictions fail (0/83 cities). The structure is mathematical, not physical. T1+/T2−/T3−.

- `findings.md` — complete findings (87 results, all tiers)
- `exploration-log.md` — 19 iterations
- `questions.md` — open/closed question tracker
- `resonance-tests.md` — resonance test specifications
- `Q1/` — residual analysis (8 phases, cached embeddings, scripts)
- `Q2/` — axiom forcing chain (enumeration, proofs)
- `Q2T2/` — cross-cultural convergence (Ifá counterfactual, branching landscape)
- `Q3/` — judgment boundary (worked examples, 象 space analysis)
- `T3/` — climate cycle test

### `usage.md`
**The system as judgment instrument.** Synthesis of the reversal findings into a functional account: the I Ching as an instrument for judgment under uncertainty, not a model of physics. Covers the interface architecture (calendar → assessment vocabulary → judgment), the {4,2,2,2,2} cascade as interface property, the algorithm-judgment boundary, the five practitioner operations, and the three-layer summary (algebra constrains, interface translates, text provides terrain, practitioner navigates).

---

## Operational Atlases

### `atlas/`
**Static 五行 atlas.** 64 hexagram profiles with all algebraic coordinates. Informational completeness: H(hexagram | full profile) = 0.0 bits. The {2,2,2,1,1} partition, torus geometry, constraint structure.
- `atlas.json` — 64 hexagram profiles (primary data file, referenced by all workflows)
- `transitions.json` — 互/變/palace transformation data
- `constraints.json` — constraint structure

### `atlas-mh/`
**梅花 (Meihua) operational atlas.** 384 states (64 hexagrams × 6 moving lines). Core projection (1+4+1). 8 arc types with perfect symmetry. 先天 parity wall (192/384 reachable). 体互 adversarial (63% 克-dominant). Two independent channels: text (present state) vs arc (trajectory). 18 domains, one engine.
- `findings.md` — complete findings
- `mh_states.json` — 384 state profiles
- `mh_arcs.json` — arc/transition data

### `atlas-hzl/`
**火珠林 (Huozhulin) operational atlas.** Shell projection (3+3). 64 profiles × 5 seasons × 12 日辰 × 31 domains. Central finding: the {4,2,2,2,2} branch element distribution (substrate constraint, not design) cascades through every layer — Earth universality, anti-resonance theorem, 官鬼 deficit, 納音 overrepresentation. Shell ⊥ core proven at temporal level (MI=0). 用神 7-step protocol formalized. 31 domains → 8 clusters + 5 exceptions (2D taxonomy, zero residual). 梅花 computes a tangent vector; 火珠林 evaluates a local observable.
- `findings.md` — complete findings (largest single document)
- `ops-plan.md` — operational plan
- `hzl_profiles.json` — 64 static profiles
- `hzl_seasonal.json` — 320 seasonal states
- `hzl_richen.json` — 768 日辰 interactions
- `hzl_dongyao.json` — 384 transformations
- `hzl_domains.json` — 31 domain bindings
- `hzl_*.json` — additional data files (network, topology, diagnostics, protocols)

---

## Earlier Investigations (superseded but historically significant)

### `kingwen/`
**KW sequence analysis (15 studies).** The first systematic investigation of the King Wen ordering as a path through Z₂⁶. Established: perfect dimensional balance, even-Hamming preference, forward-backward ring symmetry, developmental priority in pair orientation. Superseded by `kw-final/` for the ordering question; structural results absorbed into `deep/`.
- `1-timewave.md` through `15-bridges.md` — sequential study documents
- `14-synthesis.md` — synthesis of studies 1–10

### `opposition-theory/`
**Opposition hypothesis (4 phases).** Tested whether the I Ching optimizes a unified opposition measure. The hypothesis was wrong — but led to the 9-pairing theorem (only 9 structurally coherent pairings exist under mirror-pair geometry, KW uses reversal). Lo Shu / He Tu / Fu Xi occupy distinct points in opposition space. Results fed into `spaceprobe/`.
- `synthesis.md` — final synthesis
- `phase4-shengke.md` — five-phase layer analysis
- `loshu.md` — Lo Shu magic square connection

### `spaceprobe/`
**Trigram relational space.** Answered "what IS the 8-state structure?" — an 8-element set with three distinguished fixed-point-free involutions satisfying two axioms. Multiple coordinate systems (Fu Xi, Lo Shu/KW, He Tu) are faithful representations without being reducible to each other. Established the convergence-without-reduction principle.
- `synthesis.md` — final synthesis
- `doubles.md`, `invariants.md` — structural analysis
- `sequence-characterization.md` — sequence properties

### `attractors/`
**互 attractor analysis.** Defines the three-layer onion (outer/shell/interface), proves 互 peels exactly one layer per application, characterizes the 4-element attractor {坤坤, 既濟, 未濟, 乾乾}. Basin as exact 互 invariant. Results absorbed into `unification/`.
- `findings.md` — complete findings

### `wuxing/`
**五行 structural analysis (3 phases).** Initial characterization of the trigram→element assignment as geometry on Z₂³. The {2,2,2,1,1} partition, complement pairing structure, Fire/Water singletons as mutual complements. Results absorbed into `deep/` and `atlas/`.
- `summary_findings.md` — summary
- `01-03_findings.md` — phase findings

### `jingshiyizhuan/`
**京氏易傳 source text analysis.** Extracted and characterized the five layers 火珠林 dropped from the original Han dynasty system (氣候分數, 五星, 二十八宿, 建始, 積算). Central finding: all five are deterministic functions of (palace, rank) — H(fields | palace, rank) = 0.0 bits — 火珠林's compression was lossless. Discovered the universal 納甲 offset rule (+3 for upper trigrams, exception-free).
- `findings.md` — unified findings
- `01-04_findings.md` — phase findings

### `huozhulin/`
**火珠林 preliminary.** Initial 納甲 map, palace kernel, 六親 algebra. Superseded by `atlas-hzl/`.

### `synthesis/`
**Early cross-workflow synthesis.** Probe-based investigation (7 probes) establishing the two-bridge structure, two-projection theorem, and structured incompleteness principle. Results absorbed into `semantic-map/` and `unification/`. Data files still referenced by later workflows.
- `findings.md` — synthesis findings
- `probe1-7_results.md` — individual probe results

### `logoswen/`
**KW sequence investigation (LOGOS-driven).** Frame-walking analysis, algebraic decomposition. Superseded by `kw-final/`.
- `synthesis-0.md`, `synthesis-1.md` — synthesis documents

### `kwmapper/`
**KW mapping + divination examples.** Practical divination worked examples using the structural framework.
- `synthesis.md` — synthesis
- `sy_divination_examples.md` — worked examples

---

## Source Texts

Original Chinese source texts in `memories/texts/`. See `texts/directory.md` for full listing.

---

## Navigation

| Question | Go to |
|----------|-------|
| What is the central result? | `unification/synthesis-3.md` |
| Full results inventory (R1–R180) | `deep/open-questions.md` (R1–R72), `reversal/findings.md` (R94–R180) |
| Master summary | `i-summary/summary.md` |
| How was it derived? | `deep/exploration-log.md` |
| What do the texts say? | `semantic-map/findings.md` |
| Why is it isolated? | `relations/findings.md` |
| How does 火珠林 work? | `atlas-hzl/findings.md` |
| How does 梅花 work? | `atlas-mh/findings.md` |
| What about the KW ordering? | `kw-final/findings.md` |
| The {2,3,5} prime architecture | `deep/number-structure.md` |
| Nuclear rank proof | `i-summary/work/proof_nuclear_rank.md` |
| What's in the 89% residual? | `reversal/findings.md` § Q1 |
| What are the axioms? | `reversal/findings.md` § Q2 |
| How does judgment work? | `reversal/findings.md` § Q3 |
| What is the system *for*? | `usage.md` |
| Cross-cultural comparison | `reversal/findings.md` § Q2 Test 2 |
| Source texts directory | `../texts/directory.md` |
