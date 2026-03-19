# I Ching Research — Directory

~269 results across 20 workflows. See `trajectory.md` for the investigation arc.

Central finding: the 五行 assignment is the unique rigid complement-respecting surjection F₂³ → Z₅. The thematic manifold has ~16 text-intrinsic opposition dimensions, identified as the weight-3 Walsh eigenspace of Q₆.

---

## Core Workflows

### `deep/`
Parameter derivation from two axioms. R1–R42.
- `open-questions.md` — results inventory (R1–R72)
- `number-structure.md` — {2, 3, 5} prime architecture

### `unification/`
Uniqueness theorem: orbit formula = 1 iff (3,5). R43–R68.
- `synthesis-3.md` — definitive account (T1–T15)

### `semantic-map/`
Text-algebra interface. 89% independent. Two bridges survive position control. R in `findings.md`.

### `relations/`
Isolation proof: char=2, |F_q|=2, (3,5) all required. R62–R68.

### `kw-final/`
KW ordering is designed, not algebraically forced. R61.

### `i-summary/`
Nuclear rank proof, (4,13) moduli space. R69–R72.
- `summary.md` — master summary through R77

### `reversal/`
90 results (R94–R180, R254–R256). The inward turn.
- **Q1:** ~16-dim thematic manifold, complement involution as sole organizing principle, quadruple dissociation. Phase 9: weight-3 Walsh eigenspace identification (R254–R256)
- **Q2:** Forcing chain gap at composability (group axiom). Cross-cultural: binary converges, dual-cycle surjection unique to China
- **Q3:** Five judgment operations, algorithm-judgment boundary
- **T3:** {4,2,2,2,2} in climate but structural predictions fail. T1+/T2−/T3−
- `Q1/` — cached embeddings (`embeddings_{bge-m3,e5-large,labse,sikuroberta}.npz`), scripts

### `eastwest/`
φ and dual cycles across traditions. R181–R214 (1 retracted).
Two routes to φ at (3,5): cyclotomic (unconditional) and combinatorial (P₄∪P₄, conditional). No bridge to text at any resolution. Cross-architecture replication on SikuRoBERTa confirms ~85% text-intrinsic geometry.

### `fibo/`
Fibonacci alignment, φ ubiquity, interface layer. R215–R252.
Three φ mechanisms: CF extremality, Z₅ representation theory, small-number density. I Ching shares Z₅ mechanism with quasicrystals. Presentational package (φ + 1:2:3 + P₄) is the interface architecture.

### `dynamics/`
R253, R257–R269. Transition graph dynamics: complete internal characterization, disconnected from text.
- **Q₆ decomposed by 五行:** Chebyshev sequence {1, √2, φ}, fiber bundle structure, Fibonacci machine at trigram level, coherent φ survival (±2φ, ±2/φ)
- **互 dynamics:** hinge collapse (hu²→2 bits), one-way valve 克→生=0 (contingent, 1/6 partitions), hinge lines destroy equilibria, F₃/F₄ asymmetry, 12-state absorbing class
- **Stage/drama decomposition:** entropy follows size (stage), spectral gap follows label (derived stage), valve is drama, coherent sector is interaction
- **Three-level null:** vertex (R192/R209/R253), flow (R253), spectral (R269) — 五行 decoration and semantic manifold are independently organized. Complement involution is shared constraint, not bridge.
- `findings.md` — R253, R257–R269
- `questions.md` — Q11–Q15 with status (Q15 complete, Q13 characterized, Q14 negative for 五行, Q11/Q12 open for external matching)
- `exploration-log.md` — 7 iterations + final synthesis
- Scripts: `p1_subgraph_spectra.py`, `p2_hu_dynamics.py`, `p3_composed_dynamics.py`, `p45_symbolic_transfer.py`, `p7_dimension.py`, `p8_triple_null_test.py`

### `usage.md`
The system as judgment instrument. Three-layer summary.

---

## Operational Atlases

### `atlas/`
64 hexagram profiles. `atlas.json` referenced by all workflows. Also `transitions.json`, `constraints.json`.

### `atlas-mh/`
梅花 atlas. 384 states. Core projection, 8 arc types, 体互 adversarial (63% 克-dominant).

### `atlas-hzl/`
火珠林 atlas. {4,2,2,2,2} cascade, shell ⊥ core, 用神 protocol, 31 domains → 8 clusters.

---

## Earlier Investigations

`kingwen/` — KW as path through Z₂⁶ (15 studies). Superseded by `kw-final/`.
`opposition-theory/` — 9-pairing theorem. Fed into `spaceprobe/`.
`spaceprobe/` — Trigram relational space, convergence-without-reduction.
`attractors/` — 互 three-layer onion, 4-element attractor. Absorbed into `unification/`.
`wuxing/` — {2,2,2,1,1} partition. Absorbed into `deep/`.
`jingshiyizhuan/` — 京氏易傳: 5 dropped layers all deterministic, compression lossless.
`huozhulin/` — Preliminary. Superseded by `atlas-hzl/`.
`synthesis/` — Early probes. Absorbed into `semantic-map/` and `unification/`.
`logoswen/` — KW investigation. Superseded by `kw-final/`.
`kwmapper/` — Worked divination examples.

---

## Navigation

| Question | Go to |
|----------|-------|
| Central result | `unification/synthesis-3.md` |
| Full results | `deep/open-questions.md`, `reversal/findings.md`, `eastwest/findings.md`, `fibo/findings.md`, `dynamics/findings.md` |
| Texts analysis | `semantic-map/findings.md` |
| Isolation proof | `relations/findings.md` |
| 火珠林 | `atlas-hzl/findings.md` |
| 梅花 | `atlas-mh/findings.md` |
| The 89% residual | `reversal/findings.md` § Q1 |
| Axioms & forcing | `reversal/findings.md` § Q2 |
| φ & Fibonacci | `fibo/findings.md` |
| Dynamics | `dynamics/findings.md` |
| Source texts | `../texts/directory.md` |
