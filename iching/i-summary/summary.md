# I Ching Research Summary

## What was found

The I Ching's algebraic structure is the unique complement-respecting surjection F₂³ → Z₅ with three-type coexistence. Unique by theorem: Orbits(n,p) = ((p−3)/2)! × 2^{2^{n-1}−1−n} = 1 iff (n,p) = (3,5). An isolated rigid point in a doubly-exponentially growing moduli space.

The concrete realization is PG(2,F₂) decorated with one compass. The 0.5-bit "cosmological choice" is presentational — under full symmetry Stab(111) × Aut(Z₅), there is exactly 1 orbit. The binary choice appears only when fixing the 互 kernel line H. The ANF parameter space (Z₅⁴) decomposes as the trivial ⊕ standard representation of S₄ over GF(5), with Aut(Z₅) acting as pure scalar multiplication.

The texts and the algebra are independent systems sharing a narrow interface: one strong core bridge (basin × 凶, R²=23%) and a diffuse shell contact zone ({吉, 利} × {surface_relation, rank, palace_element}, R²≈6-10%), with 89% residual. The coupling is marker-specific: 凶 (danger) responds to both algebraic projections independently; 吉 and 利 (fortune, advantage) respond to shell only; 7 of 11 markers are algebraically uncoupled. 凶's dual coupling is NOT prevalence-driven (power simulation: monotonically increasing, no sweet spot at 13.5%). The commentary tradition sees primes 2 and 3 but not 5.

Two operational atlases exhaust the algebraic interpretive surface. Shell (火珠林) and core (梅花) are the only two primitive projections on Z₂⁶ (R5). Their temporal channels are proven orthogonal (MI=0). The representational substrate ({4,2,2,2,2} branch element distribution) constrains the system more than its design choices do.

The (3,5) object is algebraically isolated. "Self-interpreting code" is not a mathematical category — the architecture doesn't generalize. Isolation proven through three levels: char=2 (theorem), |F_q|=2 (GL Maximization), (n,p)=(3,5) (orbit formula). All cross-domain comparisons (genetic code, F₃, F₄) are clean negatives.

The nuclear shear has rank(M^k) = max(2, 2n−2k) for all n ≥ 2 — proven by block triangularization of M = [S E; E S] via σ = p ⊕ q coordinates. The all-ones vector 𝟏 is a fixed point of T = S+E, preventing nilpotency and creating the 4-element attractor {坤坤, 既濟, 未濟, 乾乾} at n=3.

At (4,13), the first non-trivial moduli space: 960 orbits classified by Hamming syndrome structure. The orientation code is the [7,4,3] Hamming code, but the Type-0 fiber constraint creates a "stuck bit" defect that pairs syndromes, yielding 960 = 4 × (96 + 3×48) — not 8×120. The 4-fold classification is canonical under GL(3,F₂).

The 彖傳 is a systematic anomaly detector on binary structure: 剛/柔 ratio is perfectly monotonic inverse to basin yang-content (Kun 2.14 > Cycle 1.50 > Qian 1.25).

213 results (1 retracted) across 11 workflows. See reversal/ and eastwest/ for R94–R214. Original 77 results proven or verified across 10 workflows (atlas, atlas-mh, atlas-hzl, deep, unification phases 1–3, semantic-map, kw-final, relations, i-summary). Zero contradictions.

---

## Established results (full list in deep/open-questions.md)

### The uniqueness theorem (unification phase 3)

- **The object is the unique complement-respecting surjection F₂³ → Z₅ with three-type coexistence**, equipped with the involutory nuclear shear on F₂⁶. Uniqueness is a theorem: Stab(111) × Aut(Z₅) acts regularly on the 96 Orbit-C surjections → 1 orbit.
- **Two independent arithmetic conditions:** p = 5 (trivial assignment moduli: (p−3)/2)! = 1) and n = 3 (RM(1,2) fills orientation space: 2^{n-1} = n+1). Both necessary, jointly sufficient.
- **The 0.5-bit is presentational.** 1 orbit under full symmetry, 2 orbits only when H fixed. No cosmological choice.
- **Isolated rigid point.** (4,13): 960 orbits. (5,29): ~6.4×10¹². The moduli space grows doubly-exponentially.
- **The object has no name in existing mathematics.** Cross-characteristic gap (F₂ domain, Z₅ codomain) falls between GBF and finite geometry communities. Uniqueness at (3,5) eliminates classification need. Tested and excluded: association scheme, coherent configuration, GDD, Fano labeling, Walsh spectrum framework. The best mathematical description is: trivial ⊕ standard of S₄ over GF(5).
- **Three equivalent mathematical descriptions:** (1) PG(2,F₂) with type assignment on lines through 111 (unique up to S₃); (2) surjectivity locus within trivial ⊕ standard representation of S₄ × Z₄ on GF(5)⁴; (3) cross-characteristic function F₂³ → Z₅ with unique eigenvalue direction D_{111}f = 3f and δ_f = 4.
- **Flat-direction partition:** 15 patterns in 2 S₄-orbits (3 complete-pair + 12 selective+complement), each with exactly 16 surjections. Complement flatness ⟺ three-type fiber shape {2,2,2,1,1}. Clean but derivative of fiber shape.

### The (4,13) moduli space (i-summary)

- **960 orbits classified by Hamming syndrome.** The orientation code at (4,13) is the [7,4,3] Hamming code — the kernel flip patterns are codewords. The Fano-plane labeling of complement pairs IS the parity-check matrix.
- **Type-0 defect halves classification.** The Type-0 pair (both reps map to 0) creates a "stuck bit" that desynchronizes the kernel action from the Hamming structure. Effective flips have syndrome ∈ {0, H·e_j} instead of just {0}, pairing syndrome classes. 960 = 4 × 240, not 8 × 120.
- **Within each class: 96 uniform + 144 biased.** Biased orbits split 48×3 among non-missing Z₂ pairs (Z₃-symmetric). The classification rotates with the Type-0 Fano point (verified across 3 type distributions) and is canonical under GL(3,F₂).
- **At (3,5), the defect is masked by rigidity:** RM(1,2) fills the orientation space entirely, so the Type-0 defect has no room to manifest. This is a quantitative refinement of why (3,5) is rigid.

### The nuclear rank theorem (i-summary)

- **rank(M^k) = max(2, 2n−2k) for all n ≥ 2.** PROVEN by block triangularization. In the factored basis, M = [S E; E S] where S is a nilpotent shift and E is a rank-1 innermost coupling. The change of basis σ = p ⊕ q yields block upper-triangular M' = [T E; 0 T], where T = S+E has a fixed point 𝟏.
- **Key lemma (orthogonal support):** The off-diagonal coupling Φ_k annihilates ker(T^k) because ker(T^k) is supported on outer levels while E only passes the innermost component. Weaker than im(Φ_k) ⊆ im(T^k) (which is false), but sufficient.
- **Rank drops by exactly 2 per iteration** (one from position, one from orbit), stabilizing at rank 2 after n−1 steps. Stable image = F₂² = 4-element alternating-bit attractor.

### The structure (atlas + deep + unification phases 1–2)

- **Zero residual:** 13 五行 coordinates jointly identify every hexagram uniquely. H(hexagram | full profile) = 0.0 bits.
- **{2,2,2,1,1} partition** forced by pigeonhole at (3,5). Two singletons (Water/Fire) = 互 cycle attractors.
- **Selection chain 240→192→96→16→4→2** (complete, each step classified as theorem or structural choice).
- **The torus is the frame, the Z₅ quotient is the picture.** Valence lives on the Z₅ diagonal — relation type, not position (R21).
- **Three-tier text-algebra coupling:** 凶 dual-coupled (core+shell, R²=22.6%), 吉/利 shell-only (R²≈6-10%), 7/11 markers uncoupled (~64%). Basin × 凶 is the sole Bonferroni-surviving bridge (CMH p = 4.1×10⁻⁵). Shell contact is diffuse across multiple coordinates. ~89% of text variance is algebraically independent.
- **凶's dual coupling is genuine, not prevalence-driven.** Power simulation (6000 reps across 6 prevalences) shows monotonically increasing dual-detection power. At 凶's prevalence (13.5%), dual power is only 22% — yet it was detected, while higher-prevalence markers (吉 at 31%) show no dual coupling. "Why 凶?" is semantic, not statistical.
- **Only two reading methods exist:** Shell (3+3 = 火珠林) and core (1+4+1 = 梅花). The only two primitive projections on Z₂⁶ (R5).

### The geometry (unification phase 1)

- **PG(2,F₂):** Three lines through complement (H, P, Q) carry the three coprime pairings. P+Q+H = 8 theorem.
- **互 is a shear:** One term (ī leaks into i) creates all dynamical richness. Rank 6→4→2. P→H parity rotation → 克 amplification 1.538×.
- **KW pairing = orbit class** (theorem). 先天 = Fano triangle walk, unique via b₀ constancy (predictive test).
- **Eigenstructure:** Spectral gap 0.71, stationary π(同+克+被克) = 89%. Zero stride-2→stride-1 flow. P-coset alignment exact: F(同)=1, F(克)=1/13.

### The landscape (unification phase 2)

- **Singleton-forcing ⟺ p > 2^{n−1}** (theorem, 27 cases verified).
- **(3,5) unique by triple resonance:** singleton-forcing ∧ three-type-possible ∧ n=3.
- **Hexagram Z₅ = pullback** of trigram f×f (no new data at hexagram level).
- **E=1 family** (3,5), (4,13), (5,29), (6,61): uniform structure, only (3,5) rigid.

### The isolation (relations)

- **"Self-interpreting code" is not a mathematical category.** Verbal analogy only. The architecture doesn't generalize.
- **Three-level specificity chain proven:**
  - Char = 2 required: fixed-point-free involutory translations exist only in char 2.
  - |F_q| = 2 required: GL Maximization Theorem — F₂ has largest symmetry group for any domain size (gap grows super-exponentially: 112× at N=16, >10⁹× at N=256).
  - (n,p) = (3,5) required: orbit formula = 1 only here.
- **Surjection count is field-independent:** depends on (R,S,E), not field. F₂⁴ and F₄² → Z₁₃ both have 16,773,120 surjections. Only symmetry differs.
- **Five-orbit decomposition at (3,5):** [96, 48, 48, 24, 24]. IC orbit = unique free orbit (Frame Type 2, τ-fixing theorem). Free action is generic at larger parameters.
- **ANF parametrization:** 4 free parameters (a₁,a₂,a₄,a₇) ∈ Z₅⁴. All degree-2 coefficients = 2a₇. Surjectivity locus 240/625.
- **Genetic code:** exhaustive test (210K pairs). No involutory equivariance. Connection architectural only.
- **All domain comparisons negative:** F₃ (6 orbits), F₄ (116K orbits), genetic code (no equivariance), design theory (dead end), Fano labeling (dead end).

### The 彖傳 (i-summary)

- **Systematic anomaly detector on binary structure.** 剛/柔 ratio is perfectly monotonic inverse to basin yang-content: Kun (2.14) > Cycle (1.50) > Qian (1.25). The commentary highlights what's structurally unusual — yang in yin-dominant hexagrams, yin in yang-dominant ones.

### The 梅花 atlas (384 states)

- **8 arc types** with perfect symmetry (rescued/betrayed 56/56, improving/deteriorating 52/52).
- **先天 parity wall:** 192/384 reachable, biased toward favorable arcs (OR=5.23).
- **体互 adversarial:** 63% 克-dominant. Informationally calibrated.
- **Two independent channels:** Text (爻辭, present state) vs arc (體/用 trajectory).
- **18 domains, one engine.** Domain selects semantic binding + imagery overlay.

### The 火珠林 atlas (64 profiles × temporal context × 31 domains)

- **Shell ⊥ core confirmed at temporal level:** MI(日辰 activation, 互 chain) = 0. Constructive proof: 13 branch-sharing hexagram groups with universally different 互 values.
- **{4,2,2,2,2} cascade:** Earth at 4/12 branch positions (substrate constraint, not design choice) propagates through all layers: Earth universality (never missing), anti-resonance (fc=0 iff missing 生 pair), 官鬼 target deficit (Fire/Metal scarcity), 納音 overrepresentation.
- **Anti-resonance theorem:** fc=0 ⟺ hexagram's 2 missing 六親 types form a 生 pair in element space. 10/320 states (3.1%). 6 immune hexagrams (all Fire/Metal 克 pair).
- **Perfect balance theorem:** Every hexagram has exactly 6 沖, 6 合, 6 墓 across 12 日辰. Discrimination is in the temporal pattern, not the count.
- **游魂 = universal completeness (8/8):** Maximizes visible-hidden element divergence. Two modes: direct spanning (4 palaces) and root rescue (4 palaces).
- **用神 7-step protocol:** SELECT → VISIBILITY → STRENGTH → 日辰 → MOVEMENT → NETWORK → JUDGE. Each step maps to a specific data file. Algorithmic through step 6; judgment at step 7.
- **31 domains → 8 clusters + 5 exceptions.** 妻財+官鬼 = 80% of 用神 coverage. 5 special protocols classified by 2D taxonomy (layer × mode) with zero residual.
- **Tangent vector (梅花) vs local observable (火珠林).** 梅花 computes a trajectory; 火珠林 evaluates a state. The modal 火珠林 outcome (靜卦, 17.8%) has no transformation at all.
- **Three-layer architecture genuine:** 天干/地支/納音 are independent information channels, asymmetrically activated. 地支 = all domains; 天干 = 3 contexts; 納音 = 3 domains.

### The texts (semantic map)

- **89% residual thickness.** Texts organize by position, not algebra.
- **小象 encodes 3-layer hierarchy:** χ²=125, p=5×10⁻²⁶. Zero algebraic signal after position control.
- **Commentary is non-algebraic:** 大象 imagistic, 彖傳 binary-structural (Z₂), 小象 positional only.
- **Three historical registers see three primes:** 爻辭 → positions, 小象/彖傳 → Z₂, 五行 → Z₅.

### The thematic manifold (reversal investigation, R94–R180)

> Full details: `reversal/findings.md` (87 results across 19 iterations)

- **~16-dimensional text-intrinsic opposition space.** The 89% residual is a smooth manifold with the complement involution as sole organizing principle. Cross-model validated (BGE-M3, E5-large, LaBSE). Algebraic R² = 10.8–11.0% (model-invariant).
- **Non-decomposable.** Quadruple dissociation: algebra, vocabulary, 象 categories, and syntactic frames all null against embedding geometry. Trigram decomposition null. All algebraic groupings null against opposition direction.
- **Forcing chain gap.** One irreducible gap at composability (group axiom). Without it, |S|=6 suffices. With it, (3,5) forced.
- **Judgment boundary.** Five operations, three phases, designed specification gap. Resonance T1+/T2−/T3−.

### East/West: φ and 五行 across traditions (R181–R214)

> Full details: `eastwest/findings.md` (33 results across 12 iterations)

- **"Address with conditional resonance, no bridge to text."** Two independent routes to φ at (3,5): Route A (cyclotomic, unconditional) and Route B (combinatorial, conditional on 96/240 surjections). Convergence unique at n=3 via identity 2^{n-1}+1 = 2^n−3.
- **Dimension threshold:** n=2 → p≤3 → dual cycles impossible. Greek system structurally locked out. Pentagon (生) and pentagram (克) are the same Cayley graph read differently.
- **No bridge to text at any resolution tested.** Five-phase dynamics (生/克) invisible in text embeddings. Route B (φ in 克 subgraph) has no textual correlate.
- **Cross-architecture replication (R212–R213).** Tier 1b findings replicate on SikuRoBERTa (classical-Chinese BERT). R² two-band: 10.8–11.0% (multilingual) / 13.2% (domain-matched). Opposition geometry is ~85% text-intrinsic, ~15% architecture-dependent (correlating with training-data cultural salience). Four-model consensus across distinct training data, objectives, architectures, and embedding methods.

### Epistemic tiers (full program)

- **Tier 1 (theorems):** R85, R75, R87, R102, R108, R171–R174, R181–R187, R197–R205, R207–R208.
- **Tier 1b (text-intrinsic, 4-model validated):** R156–R159, R161–R163, R167–R170, R212, R213.
- **Tier 2 (measurements):** R151, R164–R166, R176–R179, R189–R196, R206, R209–R211.
- **Tier 3 (interpretations):** R175, R180, R188.
- **Retracted:** R191.

---

## Open questions

### About the I Ching specifically

**Q1: 火珠林 operational atlas.** RESOLVED → atlas-hzl workflow. See atlas-hzl/findings.md.

**Q2: KW sequence ordering.** RESOLVED → kw-final workflow. The pair ordering is **designed but not algebraically determined** — the unique point of human authorship. See kw-final/findings.md.

**Q3: 納甲 modification history.** When did the 京氏易傳 → 火珠林 rule change occur? Historical-philological.

### About the texts

**Q4: Why exactly two bridges?** RESOLVED → open-questions + i-summary workflows. Three-tier coupling (凶 dual, 吉/利 shell-only, 7/11 uncoupled). See i-summary/exploration-log.md.

**Q5: 彖傳 as systematic anomaly detector.** RESOLVED → i-summary workflow. 剛/柔 perfectly monotonic inverse to basin yang-content across all three basins.

**Q6: 說卦傳 attributes.** Non-compass attributes (animals, body parts) untested for algebraic signal.

### About the algebra

**Q8: The decorated Fano plane in existing mathematics.** RESOLVED (negative) → open-questions workflow. No name exists. Cross-characteristic gap + uniqueness → nothing to classify.

**Q9: Nuclear rank formula.** RESOLVED → i-summary workflow. PROVEN for all n ≥ 2: rank(M^k) = max(2, 2n−2k). See i-summary/work/proof_nuclear_rank.md.

**NQ4: The (4,13) decorated object.** RESOLVED → i-summary workflow. 960 = 4 × (96 + 3×48) via Hamming + Type-0 defect. Canonical under GL(3,F₂).

### Remaining open

**NQ1: 凶's dual-coupling.** RESOLVED — not prevalence-driven. "Why 凶?" is semantic.

**NQ2: 利's stronger shell coupling.** 利 (ΔR²_shell=0.098) > 吉 (0.056). Does the conditional/unconditional distinction in their semantics map to coupling strength? LOW PRIORITY — interpretive.

**NQ3: Rank-2 × 吉 signal.** p=0.008 nominal, not Bonferroni-surviving. Needs independent corpus validation. MEDIUM PRIORITY.

**NQ5: Cross-characteristic GBF as a new function class.** Complement-equivariant surjections F₂ⁿ → Z_p. Deprioritized as completism — the object's isolation at (3,5) means the class has exactly one interesting point.

**Q7: Incommensurability as mechanism.** The 2/5 visibility ceiling is trivially forced by smallest p. Unfalsifiable as stated.

---

## Document map

| Folder | Contents |
|--------|----------|
| `unification/unification.md` | Primary document: Phase 3 complete. The uniqueness theorem + all supporting questions resolved. |
| `unification/synthesis-3.md` | Definitive account (519 lines, 15 theorems, supersedes synthesis-1/2). |
| `unification/synthesis-2.md` | Phase 2 account (landscape, selection chain, eigenstructure). |
| `unification/synthesis-1.md` | Phase 1 account (PG(2,F₂) framework, 17 results). |
| `unification/phase1-unification.md` | The (3,5) framework + I Ching mapping. |
| `deep/` | Deep exploration: 9 iterations, derivation tree, open-questions.md (R1–R72). |
| `deep/number-structure.md` | The 2, 3, 5 prime architecture. |
| `atlas/` | Static 五行 atlas: 64 profiles, torus, transformations, constraints. |
| `atlas-mh/` | 梅花 operational atlas: 384 states, arcs, torus flow, channels, timing. |
| `atlas-hzl/` | 火珠林 operational atlas: 64 profiles × temporal × 31 domains, network reading. |
| `semantic-map/` | Text-algebra interface: 89% residual, two bridges, three registers. |
| `kw-final/` | KW pair ordering investigation: Monte Carlo (50K), joint analysis, R41 correction. |
| `relations/` | Cross-domain investigation: 6 iterations, 16 computations. R62–R68. |
| `open-questions/` | Q4 and Q8 resolution: exhaustive bridge scan, marker coupling profiles. |
| `i-summary/` | This file + exploration log + computation scripts (R69–R72, nuclear rank proof). |
| `i-summary/work/` | All computation scripts and output files for this investigation. |
