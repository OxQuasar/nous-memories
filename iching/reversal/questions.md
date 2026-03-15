# Reversal: Looking Inward

The research program has moved outward from (3,5) — larger parameter spaces, more orbits, isolation proofs. 77 results characterize what the object *is*. None address what it *does*, what generates its axioms, or what lives in the 89% the algebra can't see.

Three questions for the inward direction.

---

## Q1: The Residual as Primary Object

**Status:** Phases 1-5 complete (39 results, R112–R150). The 89% residual is a smooth ~20-dimensional manifold with complement antipodality. No clusters, no algebraic predictors of similarity. The complement involution is a high-dimensional antipodal map — each pair opposes along its own unique axis. Phase 4 (image vocabulary analysis) proved the opposition is **lexically invisible** (Jaccard p=0.897). Phase 5 (syntactic frame analysis) confirmed the **quadruple dissociation**: algebra, vocabulary, 象, and syntactic frames all produce r ≈ 0 against embedding geometry. The residual is sub-syntactic, compositional, and non-decomposable. See `Q1/phase1_results.md` through `Q1/phase5_results.md`.

The semantic-map workflow tested 384 爻辭 for algebraic signal and found 89% residual. It never studied the residual itself.

**Question:** What is the internal structure of the 爻辭 when treated as a corpus on its own terms — not as data points to test for algebraic signal, but as a system of situational descriptions with its own logic?

**What to look for:**
- Image-clusters: recurring animals, landscapes, body parts, social roles, actions. Do they form a vocabulary with combinatorial rules?
- Positional grammar: texts organize by line position (known). But what's the *content* doing at each position? Is there a systematic shift in imagery type as position changes (e.g., outer lines → social/visible situations, inner lines → internal/hidden ones)?
- Intra-hexagram narrative: do the 6 lines within a hexagram tell a story? Is there a grammar of situational escalation or transformation across positions?
- Cross-hexagram patterns: which hexagrams share imagery? Does imagery clustering align with any coordinate the algebra *doesn't* use?

**Method:** NLP/semantic analysis on the 384 line statements. Cluster by imagery, not by algebra. Extract the structural skeleton of the textual layer and compare it against all known algebraic coordinates. The interesting finding would be structure that's *orthogonal* to everything already measured — evidence that the 89% has its own organizing principle.

**Data:** `texts/yaoci.json` (384 line texts), `atlas/atlas.json` (algebraic coordinates for null-model comparison).

**Why it matters:** The texts are the original object. The algebra is a skeleton discovered inside them. The 89% is not noise — it's the body. Understanding its structure is the most direct way of looking inward.

### Phase 4: The KW Path Through the Residual

The KW ordering is the one authored element — R61 proved no algebraic metric discriminates it. The 序卦傳 provides narrative justifications. Previous analysis (kw-final) tested algebraic coordinates and found nothing. But it never had the thematic manifold.

Now there's a coordinate system for the textual layer. The KW sequence traces a path through the ~20-dimensional thematic space. That path has never been examined.

**What to check:**

1. **Path smoothness:** Is the KW sequence a smooth walk through the thematic manifold? Measure consecutive thematic distances. Compare to random orderings under the correct null model (the one kw-final established). If the sequence is narratively coherent, adjacent hexagrams should be closer in thematic space than chance.

2. **Path structure:** Does the trajectory have shape — spiral, oscillation, linear progression, something else? The 序卦傳 describes a developmental arc. Does the thematic embedding confirm it?

3. **Complement placement tension:** Complement pairs are maximally distant in thematic space (R112, R123) but usually adjacent in the KW sequence. That tension — thematic opposites placed close together — might be the design principle. Measure the relationship between thematic distance and sequence distance for complement pairs vs non-complement pairs.

4. **The narrative grammar:** If the path is smooth, what drives the transitions? Do consecutive hexagrams share imagery, develop a theme, or systematically contrast? Does the 序卦傳's stated logic match the thematic manifold's geometry?

**Why this matters:** This connects the one authored element (KW ordering) to the one non-algebraic structure (residual manifold). The algebra couldn't see the sequence's logic because it was the wrong lens. The thematic manifold might be the right one. If the KW path is coherent in thematic space, it would explain what the sequence *is* — a curated walk through the space of human situations, organized by narrative rather than algebra, but legible in the residual's coordinates.

---

## Q2: The Axioms from Below

**Status:** Test 1 complete (21 results, R73–R93). Q2 proper not started.

### Test 1 Result (Complete)

Q2 Test 1 asked: is (3,5) special among ALL change-modeling systems? Answer: **the structure is necessary given the framing; the framing is coherent but not itself necessary.**

Three key theorems:
1. **Negation Uniqueness (R85):** For p > 2^{n−1}, α = −1 is the only automorphism admitting equivariant surjections. The complement axiom's algebraic form is forced.
2. **1/(2ⁿ−1) Cross-Section (R75):** The complement axiom selects a fixed fraction of each GL-orbit. The direction is a choice; all directions are GL-equivalent.
3. **Singleton-Forcing Phase Transition (R87):** The boundary p = 2^{n−1} separates degenerate (local symmetry, no rigidity) from rigid (unique axes, orbit collapse possible).

Without complement equivariance, (3,5) is the LEAST rigid n=3 parameter point (245 orbits, maximum). The complement axiom locates pre-existing GL-invariant structure (a thin 1.33% equivariant subset) rather than creating new structure.

### The Contingency Locus

The question of necessity now reduces to three axioms:
1. **Binary states with polarity** — F₂ⁿ domain with complement involution
2. **Relational codomain** — prime cyclic group Z_p as target
3. **Completeness** — surjectivity (every phase realized)

Given these, the negation-uniqueness theorem forces the complement form, the two-cycle theorem forces p=5, the dimensional forcing theorem gives n=3, and the orbit formula gives uniqueness.

### Q2 Proper (Not Started)

**Question:** What is the minimal mathematical structure capable of representing *situated change* — and does it converge on binary + two cycles, or is that one possibility among several?

**What "situated change" requires (candidate axioms):**
- **Distinguishable states** — a finite set, discreteness
- **Polarity** — each state has a complement/opposite (involution)
- **Transformation** — states can change into other states (dynamics)
- **Evaluation** — transitions can be assessed as favorable/unfavorable (a relational structure on the space of changes)

**What to investigate:**
- Does requiring both polarity (involution) and evaluation (relational codomain) force the binary → Z₅ structure, or are there other solutions?
- Is "two independent cycles" the unique way to get a non-trivial evaluation with polarity? Or can one cycle suffice? Three?
- Information-theoretic angle: what's the minimum entropy system that supports both reversible states and irreversible evaluations?
- Category-theoretic angle: is there a universal property that characterizes the (3,5) object — a functor it represents, a limit it satisfies?

**Why it matters:** The current derivation runs backward: I Ching → axioms → parameters. If the axioms can be derived forward from the concept of change itself, then the I Ching's structure isn't just unique — it's *necessary*. If they can't, then the axioms are contingent and the investigation has found the structure of a particular artifact, not of change as such.

**Connection to Test 1:** Test 1 showed that *within* the framing, everything is forced. Q2 proper asks whether the framing itself is forced. This is primarily a philosophical/theoretical question, not a computational one.

---

## Q3: The Judgment Boundary

**Status:** Characterized (11 results, R140–R150). Five judgment operations (analogy, integration, external, weighting, exception) form a closed, system-invariant repertoire. Three-phase sequence (read → assess → anchor) mirrors the tradition's own 訣 ordering. The system explicitly formalizes its own specification gap: 真/形色 magnitude distinction (R142), 推數又須明理 principle (R143). Quadruple dissociation confirmed: algebra, vocabulary, 象, and syntactic frames all produce r ≈ 0 against embedding geometry (R149). The 89% residual is sub-syntactic and non-decomposable. 象 provides a coordinate grid; embedding geometry describes the terrain. See `Q3/`, `Q1/phase5_*`.

Both operational atlases terminate at a boundary between algorithm and judgment. 梅花 ends at "interpret the arc." 火珠林 ends at step 7 of the 用神 protocol: "judge." The 飛伏 system explicitly marks an 80/20 interface — algorithmic inside, practitioner inference outside.

**Question:** What is the structure of judgment at the algorithm-practitioner boundary? Not to algorithmize it, but to characterize what kind of cognitive operation it is.

**What to look for:**
- **Typology of judgment moves.** The source texts contain worked examples. When practitioners cross the 80/20 boundary, do they perform a small number of distinct operations (analogy, weighting, narrative construction, exception handling), or is it genuinely open-ended?
- **The semantic bridge in practice.** The two measured bridges (凶×basin, 吉×生体) are statistical. When a practitioner reads a hexagram, how do algebraic coordinates and textual imagery actually combine? Is the practitioner doing implicit Bayesian updating, pattern matching, or something else?
- **Domain-dependence of judgment.** 火珠林 has 31 domains. The 5 "special protocol" domains (疾病, 天時, 射覆, 來情, 姓字) break the standard framework. Does judgment also change character across domains, or is there a universal judgment operation applied to domain-specific inputs?
- **The role of the 89%.** If the textual residual has its own structure (Q1), does judgment operate *within* that structure? Is the practitioner navigating the textual layer using the algebraic skeleton as a map?

**Method:** Extract worked examples from source texts (火珠林, 梅花 traditions). Classify the interpretive moves at each judgment point. Look for recurring patterns — not to formalize them into an algorithm, but to characterize the *type* of operation.

**Data:** Source texts in `texts/`, operational protocols in `atlas-hzl/hzl_yongshen_protocol.json`, domain bindings in `atlas-hzl/hzl_domains.json`, 飛伏 diagnostics in `atlas-hzl/hzl_feifu_diagnostic.json`.

**Why it matters:** The research program has been ontological — characterizing what the object *is*. The judgment boundary is where the object becomes operational — where structure meets use. Understanding this boundary is the most direct way of understanding what the system *does*, not what it *is*. The 80/20 split suggests the system was *designed* with this boundary in mind — algorithm and judgment are complementary, not hierarchical.

---

## Relations Between the Three Questions

Q1 (residual) and Q3 (judgment) meet at the practitioner: the 89% is the medium through which judgment operates. If Q1 finds structure in the residual, Q3 asks how practitioners navigate that structure.

Q2 (axioms) and Q1 (residual) meet at the question of necessity: if the axioms are necessary (Q2), then the 89% residual is the space of freedom *within* a necessary skeleton. If the axioms are contingent, the residual might contain the actual organizing principle that the algebra is a shadow of.

Q2 (axioms) and Q3 (judgment) meet at the concept of change: Q2 asks what change *requires* formally; Q3 asks what change *looks like* operationally. If they converge — if the minimal formal structure of change maps onto the structure of practical judgment — that would be the strongest possible evidence for the "inward" thesis.

All three reverse the program's direction: from analyzing the object to inhabiting it.

**Current status:** Q2 Tests 1-2 complete. Q1 Phases 1-5 complete (39 results, R112–R150). Q3 characterized (11 results, R140–R150). Q2 proper not started. The complement involution has been characterized at all seven levels (forced/natural/pervasive/rich/opaque/lexically invisible/non-decomposable). The judgment boundary has definite structure: five operations, three phases, designed specification gap, grid/terrain decomposition. Quadruple dissociation (algebra/vocabulary/象/syntactic frames) confirms the 89% residual is sub-syntactic, compositional, and non-decomposable. 150 total results across the full research program.