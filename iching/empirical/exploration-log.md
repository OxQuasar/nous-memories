# Empirical Probes — Exploration Log

---

## Iteration 1: Probe 8a — Internal Consistency of 10 Worked Examples

**Script:** `probe_8a.py`
**Results:** `probe_8a_results.md`
**Source:** 梅花易數 vol1, lines 176–237

### What was tested

All 10 worked examples from 梅花易數 vol1 were mechanically verified against the stated algorithm. Five checks per example:

1. **Arithmetic:** Do input numbers mod 8 / mod 6 produce the claimed upper/lower trigram numbers and moving line? (Including 0→max convention: remainder 0 → 8 for trigrams, 6 for lines.)
2. **Hexagram identity:** Does composing the computed trigrams produce the named hexagram?
3. **互卦:** Does computing nuclear trigrams match the text's claimed 互?
4. **變卦:** Does flipping the moving line produce the named changed hexagram?
5. **體用 assignment:** Does moving-line position → 体/用 match the text?

Implementation used `cycle_algebra.py` infrastructure (trigram elements, `hugua()`, `biangua()`, `five_phase_relation()`) with a new 先天→binary mapping layer: {1:乾=111, 2:兌=011, 3:離=101, 4:震=001, 5:巽=110, 6:坎=010, 7:艮=100, 8:坤=000}.

### What was found

**[measured] 10/10 fully consistent.** Every example passes all 5 checks. Zero discrepancies between the text's stated computations and the algorithm's output.

**Two algorithm families, one pipeline:**
- Examples 1–5 (先天): input is numerical (date/time, sound counts, stroke counts, character tones). Upper/lower trigram numbers computed from arithmetic, then mod 8 → trigram, mod 6 → line.
- Examples 6–10 (後天): input is observational (person type, animal, object). Trigrams assigned from symbolic category + direction. Trigram numbers + time → mod 6 → line only.

Both feed into identical compose/flip/interpret mechanics downstream.

### Derived findings from review discussion

**Finding 8a.1: Parity wall scope refinement**

**[proven]** The 192/384 parity constraint (Finding IV.1 in atlas-mh) applies specifically to the **date formula** (year+month+day+hour), where S = total determines both lower trigram (S mod 8) and moving line (S mod 6), locking their parities. Other 先天 methods (sound counting, stroke counting, tone mapping) use independent sums for upper, lower, and moving-line totals, breaking the parity lock.

Verified: Examples 1–2 (date formula) both satisfy parity match. Examples 3 and 5 (sound, strokes — classified as 先天 by the text) violate parity. The text's own examples demonstrate that "先天" is broader than "date formula."

**Finding 8a.2: Six zeros = kernel of 五行 map on even-parity fiber**

**[proven]** The 6 stable_neutral states (all-比和 relation vector) are:
- 坤(000000) line 6, 乾(111111) line 6
- 剥(100000) lines 3 and 6, 夬(011111) lines 3 and 6

These are the **RG attractor (坤, 乾) plus their immediate predecessors (剥, 夬)** from the dynamics findings. The mechanism is algebraic:

1. All-比和 at 本 requires both trigrams = same element → only Earth (坤,艮) and Metal (乾,兌) have paired trigrams
2. All-比和 at 變 requires the flipped trigram to stay in the same element → Hamming-1 within an element pair
3. Earth pair (坤↔艮) and Metal pair (乾↔兌) differ at bit 2 only → bit 2 of a trigram = line 3 (lower) or line 6 (upper)
4. Bit 2 is free because within the even-parity fiber (b₀⊕b₁=0, shared by Earth and Metal), b₂ is the kernel of the 五行 map

The grammar's diagnostic-silence points (五行 produces zero discrimination) are identical to the dynamics' RG attractor + predecessors.

**Finding 8a.3: Adversarial-first ordering hypothesis**

**[measured, N=10]** The worked examples present the relation vector in a consistent order: adversarial signals first, amelioration last. Example 1: "兑金为体，离火克之。互中巽木，复三起离火，则克体之卦气盛...幸变为艮土，兑金得生" — threat chain first, then closing counterpoint. Not selection of a single signal, but exhaustive reporting with adversarial priority.

**Finding 8a.4: Selection rule decomposition**

**[measured, N=10]** The practitioner's interpretive process separates into two operations:
1. **Position selection** (which component of the relation vector to weight): inferrable from the vector alone — scan for the most adversarial signal. This is mechanizable.
2. **Semantic interpretation** (what the signal means concretely): requires the question content and trigram imagery (象). Not mechanizable from the algebra alone.

This maps to the extractability boundary in Finding V.5. Example 9: 本卦 relation is 体克用 (favorable), but the text highlights 互's 离火克体 (adversarial) — worst-case scanning selects the adversarial position.

**Finding 8a.5: Three-channel architecture observation**

**[measured, N=10]** The worked examples invoke three information channels:

| Channel | Source | Type | Examples |
|---|---|---|---|
| 五行 arc | 体/用 生克 relation vector | Computed from state | All 10 |
| 爻辭 text | Line statement | Computed from state | Ex 6–10 (後天) |
| Hexagram name | 卦名 as Chinese word | Assigned (historical) | Ex 4 (升=ascending), Ex 10 (睽=estrangement, 損=damage) |

**Revised by 8c:** The naming channel is informal practitioner lore (0/17 domain templates reference hexagram names). The formal system has two channels, not three.

**Finding 8a.6: 比和 saturation escape**

**[measured]** Example 5 (西林寺) is one of the 6 stable_neutral states (hex 32, line 3). All positions = Earth → 五行 grammar produces zero discrimination. The text escapes to yin/yang binary analysis ("群阴剥阳" — counting yin/yang lines). This is a **fallthrough** from Z₅ typing to Z₂ counting — not an exit from formalism, but a descent to finer-grained formalism when the coarse grammar saturates.

The fallthrough trigger (all-比和 vector) is formally detectable. The Z₂ counting is mechanical. But applying the result ("群阴 in a temple is bad") requires semantic context.

Comparison: 火珠林 has an analogous diagnostic-silence condition (用神 absent → seek 伏神), but escapes laterally (visible → hidden variable) rather than vertically (Z₅ → Z₂). Different escape architectures reflect different primary grammars.

**Finding 8a.7: 象 reinforcement pattern**

**[measured, N=10]** In all 10 examples, trigram imagery (象) reinforces (never contradicts) the 五行 signal. The 象 layer functions as a translation layer — converting algebraic results into concrete predictions — not as an independent information source. The 10 examples are likely curated pedagogically; contradiction cases, if they exist, may appear in advanced vol3 cases.

The 象 invocations sort into 5 formalizability categories:
- A (trigram→thing, casting): fully formalizable via 万物属类 table
- B (trigram→attribute, interpretation): formalizable via 说卦传 table
- C (element composition): semi-formalizable (table + physical reasoning)
- D (hexagram name as word): catalogable but not mechanizable
- E (爻辞 resonance/coincidence): not formalizable

### What remains untested from 8a

- Reachability constraints of non-date 先天 methods (stroke, sound, tone) — each may have its own partition of the 384-state space with its own arc biases
- Whether the 6 stable_neutral states have special spectral properties in the dynamics framework

---

## Iteration 2: Probe 8c — 18-Domain Decision Table

**Script:** `probe_8c.py`
**Results:** `probe_8c_results.md`
**Source:** 梅花易數 vol2, lines 44–99 (18 domains), lines 22–41 (base template + 8-trigram tables), lines 145–180 (十應)

### What was tested

1. Extracted all 18 domain decision rules into a structured table
2. Tested 4 hypotheses: template uniformity (H1), adversarial-first ordering (H2), hexagram-name channel presence (H3), subsystem identification (H4)
3. Cross-referenced the 10 worked examples from 8a against vol2's 8-trigram outcome tables and 象 mapping tables

### What was found

**Finding 8c.1: 4+1 invariant structure**

**[measured]** 4 of the 5 relations have domain-invariant valence across all 17 体用-based domains:

| Relation | Valence | Invariant? |
|---|---|---|
| 用克体 | always negative | ✓ (17/17) |
| 体生用 | always negative | ✓ (17/17) |
| 用生体 | always positive | ✓ (17/17) |
| 比和 | always positive | ✓ (17/17) |
| 体克用 | domain-dependent | ✗ |

Only 体克用 admits domain-dependent interpretation. It has three modes:

| Mode | 体克用 valence | 用's semantic role | Domains (N) |
|---|---|---|---|
| Competition | + (favorable) | Adversary/obstacle to overcome | 人事,家宅,屋舍,求財,交易,出行,謁見,疾病,官訟,墳墓 (10) |
| Manifestation | +~ (delayed positive) | Goal/event that must come to you | 婚姻,求謀,求名,行人,失物 (5) |
| Nurture | - (unfavorable) | Resource/entity to receive/protect | 生產,飲食 (2) |

The +~ mode is a genuine third valence: outcome is positive but mechanism is self-defeating (overpowering what needs to come to you delays its arrival). Domain 6 (生產) additionally inverts 体生用 from - to + (mother nourishing child = good), making it the only domain with two inversions.

**Finding 8c.2: 生/克 interpretive asymmetry**

**[proven]** The 4+1 structure has a structural explanation in the 五行 grammar itself:

- **生 is self-referential:** The creator always depletes regardless of recipient. 体生用 = energy drain regardless of what 用 represents. Context-free valence.
- **克 is other-referential:** The destroyer's welfare depends on what's destroyed. 体克用 = good if 用 is a threat, bad if 用 is a resource. Context-dependent valence.

This asymmetry maps to the dynamics valve (克→生=0): the context-dependent relation (克) cannot directly produce the context-free relation (生). The valve separates the "needs context" from the "needs no context" regime in the 五行 grammar.

**Finding 8c.3: Override hierarchy (4 layers)**

**[measured + conjectured]** The 梅花 interpretive system operates as nested overrides with decreasing formalizability and decreasing activation frequency:

| Layer | Description | Formalizability | Frequency |
|---|---|---|---|
| L1 | Base template: 5-relation → valence | Fully mechanical | Always |
| L2 | Domain semantics: 体克用 mode shift | Fully mechanical | 7/17 domains |
| L3 | 十應/三要: external omens invert apparent valence | Requires perception | When omens present |
| L4 | 体用 abandonment / Z₂ fallthrough | Requires structural judgment | 6/384 states or edge cases |

The frequency × formalizability tradeoff is the real structure: the system spends most of its time in the most mechanical layer and falls to less mechanical layers only when the situation demands it.

**Finding 8c.4: Adversarial-first ordering REFUTED for templates**

**[measured]** The hypothesis from 8a.3 (adversarial-first ordering) does NOT hold for the domain templates. 11/17 domains use standard order (体克用 first = 体's agency first). Only 1/17 (人事) leads with 用克体 (adversarial-first). 2/17 (婚姻, 飲食) lead with 用生体 (best-case-first).

The adversarial-first pattern in the 8a worked examples was a feature of *narrative exposition*, not of *template structure*. Templates present relations in a fixed structural order prioritizing 体's agency.

**Finding 8c.5: Hexagram-name channel confined to practitioner lore**

**[measured]** 0/17 体用-based domain templates reference hexagram names as interpretive inputs. Only 天時占 (domain 1, which bypasses 体用 entirely) names specific hexagrams. The naming channel observed in 8a.5 is informal practitioner improvisation, not documented system architecture.

The formal system has two channels (五行 arc + 爻辞 text), not three.

**Finding 8c.6: 天時 as structurally different system**

**[measured]** Domain 1 (天時/weather) is not a deviation from the 体用 template — it is a **completely different grammar**. It counts trigram *occurrences* across 本/互/变 (a frequency model: "離多主晴，坎多主雨"), whereas all other 17 domains evaluate trigram *relations* (a graph model: "体克用 → favorable"). It also references specific hexagram names and seasonal modifiers.

This is the only domain that uses what the dynamics findings would call the "spectral" approach (how many of each trigram type?) rather than the "relational" approach (what is the 五行 relation between 体 and 用?).

**Finding 8c.7: 象 table as vocabulary, not protocol**

**[measured]** 0/10 worked examples use the detailed 8-trigram 生体/克体 outcome tables from vol2 (lines 25–41). All 14 象 invocations across the 10 examples trace to entries in the vol1 八卦万物属類 table. The practitioner uses the trigram image tables as a *lexicon* for translating algebraic outputs into concrete predictions — not as a deterministic lookup.

This confirms Finding V.5's extractability boundary: the algebra narrows the possibility space, the practitioner selects from the vocabulary.

**Finding 8c.8: Subsystem count revision**

**[measured]** 11/18 domains have rules beyond the base 5-relation template (vs. atlas-mh's count of 7). Additional subsystem domains not previously identified: 人事占 (references 8-trigram tables), 求名占 (timing + career danger rules), 求財占 (gain/loss timing rules). 7/18 domains are pure templates: 家宅, 屋舍, 求謀, 交易, 謁見, 官訟, 墳墓.

---

## Iteration 3: Probe 8c-ext — Arc Symmetry Under Three 体克用 Modes

**Script:** `probe_8c_ext.py`
**Results:** `probe_8c_ext_results.md`

### What was tested

Reclassified all 384 梅花 states under 4 valence templates (competition, manifestation, nurture, nurture-full) to test whether the atlas-mh arc symmetries (rescued=betrayed, improving=deteriorating) are universal or template-specific.

Valence templates tested:

| Relation | Competition | Manifestation | Nurture | Nurture-full |
|---|---|---|---|---|
| 生体 | +2 | +2 | +2 | +2 |
| 体克用 | +1 | 0 | -1 | -1 |
| 比和 | 0 | 0 | 0 | 0 |
| 体生用 | -1 | -1 | -1 | +1 |
| 克体 | -2 | -2 | -2 | -2 |

### What was found

**Finding 8c-ext.1: Rescued = Betrayed symmetry is INVARIANT**

**[proven]** R=B holds under all 4 templates: (56/56, 30/30, 48/48, 64/64). This is a theorem of the complement involution σ: hex → 63-hex, which induces -id on Z₅ (the five-phase cycle inversion). σ sign-flips all 4 relation-vector positions simultaneously (verified 384/384). This pairs every rescued state with a betrayed state regardless of valence assignment, because the pairing operates on the relations themselves, not their valence images.

The complement-Z₅ structure that generates the valve constraint at the dynamics level also generates the R=B invariance at the interpretation level — same algebraic fact, two manifestations.

**Finding 8c-ext.2: Improving = Deteriorating symmetry BREAKS**

**[measured]** I=D holds only under competition (52=52). Breaks under all three alternative templates:

| Template | Improving | Deteriorating | I=D? |
|---|---|---|---|
| Competition | 52 | 52 | ✓ |
| Manifestation | 30 | 78 | ✗ (deteriorating +48) |
| Nurture | 12 | 86 | ✗ (deteriorating +74) |
| Nurture-full | 40 | 56 | ✗ (deteriorating +16) |

**Mechanism:** I=D requires the valence alphabet to be symmetric around zero. Competition has {+2,+1,0,-1,-2} (symmetric). Manifestation has {+2,0,0,-1,-2} (negative-heavy). Nurture has {+2,0,-1,-1,-2} (even more negative-heavy). When the alphabet loses symmetry, more trajectories end negative than positive.

**Resolved in iteration 4:** I=D is a theorem of all symmetric valence alphabets, not specific to the competition weights. See 8c-ext2 below.

**Finding 8c-ext.3: Competition template is the unique favorable maximum**

**[measured]** Favorable→unfavorable flow is one-directional under manifestation and nurture:

| Template | Fav→Unfav | Unfav→Fav |
|---|---|---|
| Manifestation | 33 | 0 |
| Nurture | 69 | 0 |
| Nurture-full | 68 | 40 |

Under manifestation and nurture, NO state gains favorable status — the flow is strictly from favorable to unfavorable. The competition template represents the maximum possible favorable count. Domain specialization can only narrow the favorable space.

**Exception:** Nurture-full (生產) partially reverses this: 40 states recover favorable status because 体生用 inversion (from - to +) adds positive valence back. This is the only domain where "giving energy to 用" is good (mother nourishing child), and correspondingly the only domain where unfavorable states can become favorable.

**Finding 8c-ext.4: Stable neutral states are template-invariant**

**[proven]** All 6 stable_neutral states survive under every template. Their all-比和 vectors always map to all-zero valence regardless of 体克用 mode. The grammar's diagnostic-silence points are absolute.

**Finding 8c-ext.5: Scale of arc reclassification**

**[measured]** Impact increases with template distance from competition:

| Template | States reclassified | % of 384 |
|---|---|---|
| Manifestation | 122 | 32% |
| Nurture | 180 | 47% |
| Nurture-full | 278 | 72% |

The atlas-mh arc classification is substantially domain-dependent. It represents the competition-mode reading; nearly half the state space reclassifies under nurture semantics.

**Finding 8c-ext.6: Structural pessimism under domain specialization**

**[measured]** Arc type distributions shift toward unfavorable under all non-competition templates:

| Arc type | Competition | Manifestation | Nurture | Nurture-full |
|---|---|---|---|---|
| stable_favorable | 47 | 39 | 0 | 2 |
| stable_unfavorable | 48 | 117 | 129 | 61 |

Under nurture: **zero** stable_favorable states remain. Every state that was stably favorable under competition has been reclassified. The nurture domains (飲食, 生產) see a state space where no configuration is unconditionally good — consistent with the tradition's framing of these domains as requiring delicate balance rather than forceful action.

---

## Iteration 4: Probe 8c-ext2 — I=D Under Arbitrary Symmetric Alphabets

**Script:** `probe_8c_ext2.py`
**Results:** `probe_8c_ext2_results.md`

### What was tested

Resolved the open question from 8c-ext.2: does I=D hold for all symmetric valence alphabets, or only for the specific competition weights?

A "symmetric alphabet" is parameterized by (a, b) where a, b > 0:
- V(生体) = +a, V(克体) = -a, V(体克用) = +b, V(体生用) = -b, V(比和) = 0

Tested: 16 (a,b) pairs, perturbation of V(体克用) from -2 to +2, and complement involution analysis.

### What was found

**Finding 8c-ext2.1: Three-tier symmetry theorem**

**[proven empirically, 16 alphabets tested]** The arc symmetries form a three-tier hierarchy:

| Symmetry | Condition | Mechanism |
|---|---|---|
| **R=B** | Any positive (a, b) — no symmetry required | σ negates all signs → rescued↔betrayed bijection |
| **I=D** | Symmetric alphabet: V(r) = -V(σ(r)) for all r | σ preserves sign-negation → improving↔deteriorating balanced |
| **Stable_neutral invariance** | Any alphabet | All-比和 → all-zero under any weighting |

R=B is strictly more robust than I=D. R=B depends only on the sign of valences (which σ always flips for any positive a, b). I=D additionally requires that the valence alphabet preserves sign-negation under σ, which holds iff V(体克用) > 0 and V(体生用) < 0 (the symmetric configuration).

**Finding 8c-ext2.2: I=D is a theorem of symmetric alphabets, not a numerical accident**

**[proven empirically]** I=D holds for all 16 tested (a, b) pairs with a, b > 0. Two distinct I=D counts observed:
- **a = b:** I = D = 34 (σ is exact negation → trivial bijection)
- **a ≠ b:** I = D = 52 (σ negates signs but not magnitudes → compensated balance)

No other count values observed. The 18-state difference (52 - 34 = 18 per side) represents states that under equal weights have tied ben/bian valences (classified as stable) but under unequal weights have untied valences (classified as improving or deteriorating).

**Finding 8c-ext2.3: Breaking conditions are precise**

**[measured]** Perturbation of V(体克用) with other values fixed at {V(生体)=+2, V(克体)=-2, V(体生用)=-1, V(比和)=0}:

| V(体克用) | I=D? | R=B? | Mechanism |
|---|---|---|---|
| ≤ 0 | ✗ | ✓ | Sign-negation fails: 体克用 ≤ 0 but σ(体克用) = 克体 = -2 < 0 → both non-positive |
| +0.5 to +1.5 | ✓ | ✓ | Sign-negation preserved |
| +2.0 | ✗ | ✓ | Partial valence degeneracy: 体克用 = 生体 = +2 creates asymmetric magnitude collision |

The breaking boundary at V(体克用) = 0 is exactly where domain specialization (manifestation mode) places it. The I=D breaking under domain specialization is not a side effect — it's structurally forced by the sign-negation failure.

**Finding 8c-ext2.4: Competition template as unique structural optimum**

**[proven]** The competition template is simultaneously:
1. **Maximum symmetry:** both R=B and I=D hold
2. **Maximum favorability:** most favorable states of any template
3. **Unique symmetric point:** the only domain template where the valence alphabet is symmetric (体克用 > 0)

Domain specialization degrades both symmetry and favorability simultaneously and monotonically. This is forced by the 4+1 structure: 体克用 is the only relation available for domain modification, and any reduction of its positivity crosses the sign-negation boundary.

**Finding 8c-ext2.5: R=B count = 56 is absolutely invariant**

**[measured]** R = B = 56 for every symmetric alphabet tested. The count is determined by the complement involution's action on the state space, not by the valence weights. The 56 decomposes as 2 × 28 (upper/lower 体 symmetry), with inner 28 arising from the interplay of Z₅ rescue conditions, trigram bit-flip geometry, and the {2,2,2,1,1} element partition.

The partition into rescued/betrayed states is ultimately a consequence of the quadratic residue structure of Z₅*: the 五行 relations partition into QR = {1,4} (生) and NR = {2,3} (克), and the complement involution maps QR↔NR via negation, guaranteeing R↔B pairing.

**Finding 8c-ext2.6: Complement-Z₅ unifies dynamics and interpretation**

**[proven]** The complement involution σ: hex → 63-hex inducing -id on Z₅ generates three phenomena at three different levels:

| Level | Phenomenon | Mechanism |
|---|---|---|
| Dynamics | Valve constraint (克→生 = 0) | σ partitions Z₅* into {生, 克} cosets; sequential transitions within a coset are constrained |
| Interpretation | R=B invariance | σ pairs every rescued state with a betrayed state via sign-negation |
| Combinatorics | R=B count = 56 | Z₅ QR structure × bit-flip geometry × element partition |

Same algebraic fact, three manifestations. The complement-Z₅ structure is the deepest shared invariant across the 梅花 system's operational and interpretive layers.

### Data limitation: 8b/8d blocked

**[noted]** Probes 8b (皇極經世 event catalogue × 梅花 algorithm) and 8d (seasonal modulation) are blocked by a date-resolution mismatch. The 梅花 date formula requires year + month + day + hour. The 皇極經世 records events at year-level resolution only (with rare month annotations). Without full dates, the hexagram cannot be computed.

This is a data availability limitation, not a closed question. A source with full date resolution for historical events would enable the test.

---

## What remains untested

**Structural:**
- Reachability constraints of non-date 先天 methods (stroke, sound, tone) — each may have its own partition of the 384-state space with its own arc biases
- Whether the 6 stable_neutral states have special spectral properties in the dynamics framework
- Formal proof that I=D holds for ALL symmetric alphabets (empirically confirmed for 16 pairs; analytic proof pending)

**Textual:**
- Does 象 ever contradict 五行 in vol3 or vol5 advanced cases?
- The 十應 inversion principle (L3 overrides): can these be systematically extracted and formalized?
- 天時's frequency model: formal comparison with spectral decomposition from dynamics findings

**Empirical (blocked by data):**
- 8b: Testing arc classification against historical events with full date resolution
- 8d: Whether seasonal modulation (衰旺) improves predictive discrimination beyond base 生克

---

## Final Synthesis (2026-03-19)

Four iterations. Probes 8a, 8c, 8c-ext, 8c-ext2. See `findings.md` for the organized findings and `questions.md` for open questions (E7a–E11).

### Arc of the workflow

Started with mechanical verification (8a: does the algorithm work?) → extracted the decision grammar (8c: what are the rules?) → tested structural invariances (8c-ext: do symmetries survive domain specialization?) → proved the symmetry theorem (8c-ext2: when do symmetries hold in general?). Each iteration opened the next through questions that emerged in review.

### What connected

The complement-Z₅ involution σ — the same algebraic structure that generates the valve constraint at the dynamics level (Phase 7, R279) — generates the rescued=betrayed invariance at the interpretation level. This was not anticipated. The workflow was designed to test internal consistency (8a) and extract decision rules (8c). The unification with the dynamics findings emerged from testing whether arc symmetries survive domain revaluation.

The 生/克 interpretive asymmetry (8c.2) maps directly onto the dynamics valve: 生 is context-free at both levels, 克 is context-dependent at both levels, and the valve (克→生=0) is the boundary between them. This connects the Phase 7 dynamics to the Phase 5 judgment instrument interpretation.

The 6 stable_neutral states bridge dynamics (RG attractor + predecessors), algebra (kernel of 五行 map on even-parity fiber), and interpretation (points where the entire system goes silent). These are the investigation's first candidates for states that are special at all three levels simultaneously — a potential local exception to the three-level null.

### What didn't connect

The empirical prediction test (8b: does the arc classification predict historical event outcomes?) was blocked by date resolution in the 皇極經世. The hexagram-name channel (8a.5) turned out to be practitioner lore, not system architecture (8c.5). The adversarial-first ordering hypothesis (8a.3) was refuted at the template level (8c.4).

### What the workflow generated

Seven new questions (E7a–E11), ranked by the synthesis discussion. The strongest: E7a (6-zeros as semantic outliers — computable, could locally break the three-level null) and E8 (complement-Z₅ in 火珠林 — natural trunk extension, harder than it looks because σ cross-maps palaces).

### Structural position

This workflow completes the first pass of the empirical investigation framework laid out in `plan.md`. The 梅花 system is internally consistent, structurally clean, and algebraically continuous with the theoretical findings. The main open empirical question (does the grammar predict real-world transition outcomes?) remains blocked by data availability. The main open structural questions (E7a, E8, E9) are computable from existing infrastructure.

---

## Iteration 5: Probe 8b-A — Parsing 皇極經世 Event Chronicle + Structural Constraint Discovery

**Script:** `probe_8b_parse.py`
**Data:** `hjjs_events.json`
**Source:** 皇極經世書 vol 6 (`texts/huangjijingshi/6-hj.txt`), lines 17–3137

### What was tested

Parsed the entire 皇極經世 vol 6 event chronicle — the year-by-year historical record from the Warring States period (~400 BCE) through the Five Dynasties (~960 CE). The parser extracts (天干, 地支, event text) tuples from 1320 sexagenary year entries across 44 thirty-year blocks.

Before building the event classifier, tested two preconditions:
1. Whether the parsing is structurally sound (edge cases, corruption)
2. Whether blank-year distribution reveals editorial selection bias by cycle position

Also analyzed the transition structure to determine which of the planned statistical tests (E2, E3) are feasible with this data.

### What was found

**[measured] Parsing: 1111 events extracted from 1320 year entries (84.2% coverage).**

The parser uses a concatenate-then-scan approach: all body text is joined, then the 60-year 天干地支 cycle is followed sequentially with lookahead recovery (window=10) for corrupted markers. Two data quality issues identified:
- One corrupted character at line 577 (`申寅` instead of `甲寅`) — recovered by lookahead, one blank entry inserted
- One section (lines 1949–1993) with systematic 地支 +2 shift — ~10 entries potentially misassigned by one 60-year cycle

天干 distribution is perfectly uniform: all 10 stems get exactly 132 entries (1320/10). Events-with-text distribution is flat (105–118 per stem).

**[measured] Selection bias channel: clear.** Blank years are uniformly distributed across the 10-year stem cycle (χ²=7.70, df=9, p=0.56) and the 5 五行 elements (χ²=3.61, df=4, p=0.46). Event density is even flatter (χ²=1.45, df=9, p=0.998 by stems; χ²=0.68, df=4, p=0.95 by elements). No detectable editorial filtering by cycle position. This does not rule out content-level bias (choosing which details to record within a given year), but the coarsest structural selection channel is level.

**[proven] The 天干→五行 mapping on consecutive years produces only 比和 and 生. Never 克.**

The 天干 cycle encodes paired elements: 甲乙=木, 丙丁=火, 戊己=土, 庚辛=金, 壬癸=水. Every consecutive stem pair is either same-element (比和: 甲→乙, 丙→丁, ...) or parent→child (生: 乙→丙, 丁→戊, ...). Verified empirically across 1110 consecutive-event transitions: 53.1% 生, 44.1% 比和, 2.4% 克 (the 27 克 transitions arise only from 3+ year gaps where blank years intervene; 88.2% of consecutive events are exactly 1 year apart).

**Consequence: E2 (克→克 suppression) and E3 (valve: 克→生=0) are structurally untestable with this data.** With ~27 克 transitions total, the expected number of 克→克 bigrams under the null is <1. The tests have zero statistical power.

This is a design feature of the 天干 cycle, not a data limitation. The cycle IS the 生 cycle encoded in time — it structurally forbids 克 at the year-to-year level. The grammar's transition constraints (E2, E3) operate at finer temporal resolution (the full date formula produces 体 and 用 from different temporal components: year+month+day+hour).

### Structural insight from review discussion: prediction gap

The 梅花 grammar is relational — it requires two elements (体 and 用) to generate a 五行 relation and thus a prediction. A single year's 天干 gives one element. There is no relational prediction from a single label.

The testable hypothesis with this data is weaker: **does event character correlate with position in the 天干/五行 cycle?** This tests whether the 天干→五行 assignment carries non-random information about historical event patterns — a different claim than "does the grammar predict event character."

A refinement identified in review: each sexagenary year carries TWO elements — 天干→五行 and 地支→五行 (子=水, 丑=土, 寅=木, ...). Together they produce a 五行 relation per year (e.g., 甲子 = 木+水 → 水生木). This gives a relational prediction from the year label alone, closer to what the grammar computes. However, this tests the 八字 (Four Pillars) tradition's year-pillar interpretation, not the 梅花 date formula. The theoretical provenance needs to be named explicitly.

### Agreed test sequence for next iteration

1. Build verb-based event classifier (year-level, blind to cycle position)
2. Enumerate all 60 sexagenary pairs → classify stem-branch 五行 relations → check for confounds with historical timeline
3. Run event_character × 5 elements (χ² + effect size confidence interval)
4. Run 120-permutation control (is the canonical 五行 ordering special among all cyclic orderings?)
5. Run stem-branch relational test (event_character × 五行 relation type) — with explicit notation of 八字 provenance

Expected outcome: null. Informative either way — null bounds the grammar's resolution boundary (requires finer temporal input than year-level to generate predictions); signal opens a fork (either validates the 八字 year-pillar interpretation or reveals editorial pattern).

### What remains untested from 8b

- Event classification and all statistical tests (steps 1–5 above)
- Whether volumes 4–5 provide additional parseable event data (vol 4 is tabular format with sparse events; vol 5 covers legendary/early historical period with narrative events)
- 8b Approach B (events with month-level date resolution) — requires identifying entries in vols 4–6 that mention specific months
- Seasonal modulation (8d) — depends on 8b results

---

## Iteration 6: Probe 8b-A — Event Classification + Statistical Tests + Z₅ Orbit Proof

**Script:** `probe_8b_test.py`
**Results:** `probe_8b_test_results.md`
**Data:** `hjjs_events.json` (1320 entries from iteration 5)

### What was tested

Built a verb-based event classifier for the 1111 event entries, then ran five statistical tests for association between event character and position in the 天干/五行 cycle.

**Classifier:** Keyword matching on verb types. Unfavorable: 伐敗殺弑陷滅亂寇叛篡誅攻破戰圍廢死 (17 verbs). Favorable: 平封㑹會和冊朝降 + phrases 稱帝/稱王. Neutral succession markers (卒崩薨繼嗣踐位) excluded. Year-level classification: unfavorable if only unfavorable verbs present, favorable if only favorable, mixed if both, neutral if neither.

**Classifier noise identified:** 平 has ~25% false positive rate from place names (平城, 平陸, 長平), person names (陳平), and era names (河平). Of 163 "favorable" entries, 46 are classified favorable ONLY because of 平. Sensitivity analysis: removing 平 entirely yields N=496 testable entries, and the null result strengthens (χ²=1.47, p=0.83 vs χ²=1.96, p=0.74 with 平). Classifier noise is uniformly distributed across cycle positions, so the null is robust.

### What was found

**[measured] Classification distribution:** 314 unfavorable (23.8%), 163 favorable (12.3%), 292 mixed (22.1%), 342 neutral (25.9%), 209 blank (15.8%). Testable (favorable + unfavorable only): N=477, with 65.8% unfavorable, 34.2% favorable. The 2:1 unfavorable skew reflects the chronicle's focus on conflicts and political upheaval.

**[measured] All four statistical tests return null.**

| Test | χ² | df | p | Cramér's V |
|------|---:|---:|--:|----------:|
| Event character × 5 elements | 1.96 | 4 | 0.74 | 0.064 |
| Event character × 10 stems | 4.05 | 9 | 0.91 | 0.092 |
| Stem-branch 五行 relation (八字) | 3.91 | 4 | 0.42 | 0.091 |
| Sensitivity (without 平) | 1.47 | 4 | 0.83 | 0.054 |

Effect size bound: with N=477, any association between event character and cycle position is smaller than Cramér's V=0.064 (95% level).

**[measured] 120-permutation control:** All 120 permutations of the 5 elements produce identical χ² values. The canonical 五行 ordering is not special because no ordering is special — event character is completely independent of how elements are assigned to the 10-year stem cycle. Monte Carlo test (10,000 random 5-group partitions) confirms: p=0.75.

**[proven] Z₅ orbit invariance: the 12/60 relation uniformity is forced by cyclic structure, independent of element distribution.**

Each of the 5 stem-branch 五行 relations (比和, 干生支, 支生干, 干克支, 支克干) appears exactly 12 times among the 60 sexagenary pairs. Initially attributed to the {4,2,2,2,2} 地支 element distribution (土 doubled). Testing revealed this holds for ANY distribution — including all 6 branches assigned to a single element.

Proof: for relation type R with corresponding Z₅ permutation σ_R, stem element E contributes n_{σ_R(E)} to the count (where n_i is the number of branches with element i). Summing over all 5 elements: Σ_E n_{σ_R(E)} = Σ_i n_i = total_branches. The sum is permutation-invariant because it runs over a complete Z₅ orbit. With 6 branches per parity half, each relation gets 6+6=12.

This means the sexagenary cycle is a universal 五行 balance instrument — not by design, but because the Z₅ cyclic structure of 生/克 makes balance automatic. The {4,2,2,2,2} distribution (土 doubled) was chosen for cosmological/seasonal reasons, not balance constraints.

**[measured] Approach B feasibility: blocked.** Only 10 entries (0.9%) mention specific months. N far too low for statistical testing.

### Structural insights from review discussion

**Prediction gap confirmed.** The 梅花 grammar is relational — it requires two elements (体 and 用) to generate a 五行 relation and thus a prediction. A single year's 天干 gives one element; even the full sexagenary pair's stem-branch relation (tested as 八字 year-pillar interpretation) returns null. The grammar's resolution boundary sits below year-level temporal input.

**Four-level Z₅ symmetry table.** The orbit invariance proof adds a fourth level to the complement-Z₅ unification:

| Level | Phenomenon | Mechanism |
|-------|-----------|-----------|
| Dynamics (Phase 7) | Valve constraint (克→生=0) | Z₅ complement reflection |
| Interpretation (8c-ext) | R=B invariance | Z₅ complement → sign-flip bijection |
| Combinatorics (8c-ext2) | R=B count = 56 | Z₅ quadratic residue structure |
| Temporal (8b) | 12/60 relation uniformity | Z₅ orbit sum invariance |

The temporal level is the weakest (trivially forced by group theory), but it completes the pattern: Z₅ symmetry propagates automatically wherever the 五行 cycle appears.

### What remains untested

- Probe 8e: 納甲 system as Z₁₂→Z₅ mapping (independent of 8b, next in execution order)
- Whether the classifier's place-name noise affects any downstream analysis (it doesn't affect the null, but the raw counts are soft)
- Volumes 4–5 event data (different format, likely lower yield)
- Seasonal modulation (8d) — structurally blocked by 8b null (no year-level signal to modulate)

---

## Iteration 7: Probe 8e — 納甲 System Under Complement-Z₅

**Script:** `probe_8e_najia.py`
**Results:** `probe_8e_results.md`
**Source:** 納甲 table from `huozhulin/01_najia_map.py` (originally 京氏易傳); complement-Z₅ framework from `dynamics/probeC2_complement_z5.py`

### What was tested

The 納甲 system assigns a 天干地支 pair (and thus a 五行 element) to each of 384 line positions (64 hexagrams × 6 lines). The system factors through trigrams: each line's assignment depends only on its trigram, position within the trigram (1–3), and whether it sits in the lower or upper half. The question: does the complement involution σ (hex → 63-hex, flipping all bits) induce a consistent Z₅ transformation on the 納甲 element assignments, as it does on the trigram-level elements?

Also tested: the corrected 京氏 original rule (universal +3 upper branch offset, discovered in the jingshiyizhuan workflow) vs the standard 火珠林 rule. Whether alternative TRIGRAM_BRANCH_START tables could achieve complement consistency. The algebraic structure of 納甲 as a map.

### What was found

**[proven] Complement-Z₅ holds at the trigram-element level but FAILS at the 納甲 branch-element level.**

At the trigram level, σ induces -id on Z₅ for all 4 complement pairs: 乾(金)↔坤(土), 震(木)↔巽(木), 坎(水)↔離(火), 艮(土)↔兌(金). This is the known result from Phase 8 dynamics.

At the 納甲 branch-element level, σ produces 4 different Z₅ shifts {0, 1, 3, 4} across the 4 complement pairs. Of 8 half-complement configurations (4 pairs × lower/upper): 3 are consistent under standard 納甲 (乾↔坤 upper, 艮↔兌 both positions), 5 are inconsistent. At the hexagram level: only 2/32 complement pairs have a uniform 6-line Z₅ shift.

**[proven] Root cause: the Z₁₂ → Z₅ projection via 地支→五行 has non-uniform fibers.**

地支→五行 maps 12 branches to 5 elements with fiber sizes {4,2,2,2,2} (Earth has 4 branches: 丑辰未戌; others have 2 each). 納甲 assigns branches as arithmetic progressions in Z₁₂ (stepping by ±2). These progressions become non-arithmetic in Z₅ after projection through the non-uniform fiber map. Different starting points produce different Z₅ step patterns, so shifting the start (as complement does) changes the pattern rather than uniformly translating it.

This connects to 8b: in the sexagenary cycle analysis, Z₅ orbit-sum invariance holds regardless of fiber sizes (global property). Here, pointwise consistency across 3-element windows fails because of fiber sizes (local property). The same {4,2,2,2,2} distribution is irrelevant globally but causal locally.

**[measured] 艮↔兌 is the unique fully consistent complement pair. This is coincidental.**

艮 (yang, start at branch index 4) samples {辰,午,申} → Z₅ [2,1,3]. 兌 (yin, start at branch index 5) samples {巳,卯,丑} → Z₅ [1,0,2]. The pairwise diffs are all 4 mod 5. Verified that this does not follow from the sum-to-9 property of these branch index pairs: other pairs summing to 9 give diffs {1,2,3,4}, not uniformly 4. The consistency arises from the specific 3-element window landing on branches where the non-linear projection happens to be locally linear.

**[proven] 24 alternative TRIGRAM_BRANCH_START tables achieve full complement consistency. None includes historical values.**

Of the 36 possible (yang_start, yin_start) pairs per complement pair, exactly 4 produce consistent Z₅ diffs. The historical starting points for 乾 and 震 are both 0, which is not among the complement-consistent options {1,2,3,4}. The system was not designed for complement consistency at the branch level.

**[measured] The corrected 京氏 rule (universal +3 upper offset) makes complement consistency WORSE.**

Standard 納甲: 3/8 half-configurations consistent. Corrected 京氏: 2/8 (breaks 艮↔兌 upper). The modern 火珠林 modification is closer to complement consistency than the original, though neither achieves it.

**[proven] The 納甲 map is not a group homomorphism.**

Best linear fit from Z₈ × Z₃ → Z₅ matches only 9/24 cells (37.5%). The map is a composition of an affine step in Z₁₂ (branch ring) followed by the non-linear 地支→五行 projection to Z₅. The non-linearity is entirely in the projection layer.

**[proven] 納甲 line elements are NOT the trigram element repeated.** Each trigram's 3 line elements span 2–3 distinct elements. No trigram has all 3 branch elements matching its trigram-level element. The branch layer carries independent 五行 information relative to the trigram layer.

### Structural insight from review discussion

**Clean structural boundary between 梅花 and 火珠林:**

| Property | 梅花 (trigram level) | 火珠林 (line level) |
|----------|---------------------|---------------------|
| Element assignment | 8→5 surjection | 48→5 via Z₁₂ projection |
| Complement-Z₅ | σ = -id (universal) | σ produces {0,1,3,4} (pair-dependent) |
| Algebraic structure | Group homomorphism | Affine + non-linear projection |
| Resolution | Global (complete orbits) | Local (3-element windows) |

The boundary is at the Z₁₂→Z₅ projection. Systems that work above this projection (梅花: trigram elements) inherit complement-Z₅ automatically. Systems that work below it (火珠林: branch elements) do not. The non-uniform Earth fiber ({4,2,2,2,2}) is the mechanism that breaks the projection's linearity.

**Closes Q-火珠林 from findings.md.** The complement-Z₅ involution does not generate analogous symmetries in the 火珠林 atlas. σ cross-maps palaces and changes 六親 assignments non-uniformly because the underlying line elements don't transform uniformly under σ.

### What remains untested

- Whether the 32 unique diff patterns (8 lower × 4 upper) have further combinatorial structure
- Whether the 2 fully consistent hexagram pairs (艮|坤↔兌|乾, 兌|兌↔艮|艮) have special status in the 火珠林 atlas (palace position, 六親 words)
- The factoring asymmetry (8 lower × 4 upper, not 8×8) — attributed to 乾/坤 position-dependence, but could have deeper origin

---

## Iteration 8: Probe 7a — Kernel Hexagrams in the Semantic Manifold

**Script:** `probe_7a_kernel.py`
**Results:** `probe_7a_results.md`
**Data:** BGE-M3 embeddings from `reversal/Q1/embeddings_bge-m3.npz` (384×1024), atlas from `atlas/atlas.json`, 爻辞 texts from `texts/iching/yaoci.json`

### What was tested

The 6 stable_neutral (hex, line) pairs — at 4 kernel hexagrams: h=0 (坤|坤, Earth), h=31 (乾|兌, Metal), h=32 (坤|艮, Earth), h=63 (乾|乾, Metal) — were tested for anomalous position in the semantic embedding manifold (Phase 4) and for anomalous 爻辞 valence markers.

Six tests: (1) centroid distance from global mean, (2) inter-kernel pairwise distance, (3) nearest neighbors, (4) PCA projection, (5) line-level embedding analysis, (6) valence marker anomaly across the full traditional gradation.

### What was found

**[measured] Geometric: center-ward but not clustered.**

Kernel hexagram centroids are individually closer to the semantic center than average (z=−1.52 in residual space, z=−0.58 in raw). The effect strengthens after algebraic regression, indicating the text-level semantic neutrality is independent of algebraic properties. However, the 4 kernel hexagrams are NOT mutually clustered (permutation test p=0.455) and do not appear in each other's nearest-neighbor lists. They are individually generic but thematically dispersed — consistent with "semantically neutral" rather than "semantically similar."

**[measured] Valence: standalone 吉 completely absent from kernel hexagrams (p=0.0006).**

| Marker | Kernel (N=24) | Other (N=360) | Fisher p |
|---|---|---|---|
| Standalone 吉 (not 元吉) | 0/24 (0.000) | 106/360 (0.294) | 0.0006 |
| 元吉 (superlative) | 1/24 (0.042) | 11/360 (0.031) | 0.54 |
| 利 (conditional positive) | 4/24 (0.167) | 52/360 (0.144) | 0.76 |
| 无咎 (neutral-cleared) | 6/24 (0.250) | 78/360 (0.217) | 0.80 |
| 凶 (strongly negative) | 5/24 (0.208) | 47/360 (0.131) | 0.35 |
| 悔 (mildly negative) | 2/24 (0.083) | 29/360 (0.081) | 1.00 |
| 吝 (regret) | 0/24 (0.000) | 20/360 (0.056) | 0.63 |

The effect is specific to standalone 吉 — the standard unconditional positive marker. Every other valence marker (positive, negative, neutral) is at baseline rates. The kernel's only 吉 occurrence is in 坤 L5 (黃裳元吉), which is 元吉 (superlative form), not standalone 吉. The texts specifically withhold the standard affirmation while allowing conditional markers (利), superlative markers (元吉), and all negative/neutral markers at normal rates.

**[measured] The 吉 depletion is specific to the kernel, not to same-element hexagrams.**

Confound check: the 14 hexagrams with upper=lower trigram element include the 4 kernel hexagrams plus 10 others. The 10 same-element non-kernel hexagrams have 吉 rate = 0.300, almost identical to the different-element baseline (0.330, Fisher p=0.76). The depletion is NOT a property of same-element hexagrams generally. It requires the full kernel condition: main + 互卦 both all-比和. Fisher: kernel vs same-element-not-kernel, p=0.010.

### Structural insights from review discussion

**Absence mirrors absence.** The grammar's characterization of kernel states is diagnostic silence — the 五行 relation vector is all-比和, producing zero signal. Not negative signal, zero signal. The texts mirror this by withdrawing the positive marker (吉) rather than adding negative ones (凶). Where the algebra produces no differentiation, the texts produce no affirmation.

**Marker specificity.** The effect is confined to standalone 吉 — the most common unconditional positive. Conditional positives (利), superlatives (元吉), and all negative/neutral markers are unaffected. This mirrors the distinction between "bad" and "undifferentiated" — the kernel states are not adverse, they're unaffirmable.

**Local exception to the 89%/11% global null.** The algebraic (11%) and textual (89%) channels are globally independent (Phase 3). This finding is a local exception at the algebraic origin: the channels correlate at the kernel while remaining independent in the interior. Consistent with orthogonal dimensions sharing a boundary condition — both channels go to zero at the same point. The channels detect the same structural boundary from different directions.

**Cross-temporal correspondence.** The 爻辭 texts predate the formal 五行 analysis by ~1800 years. The algebraic kernel (a classification from the 梅花 operational grammar) picks out hexagrams whose original texts independently encode the same structural condition through a different mechanism (吉 withdrawal). The correspondence is not designed — it's convergent.

### What remains untested

- Whether the 吉 depletion extends to hexagram-level 辭 (卦辭, the hexagram-level judgments, not just 爻辭 line statements)
- Whether the effect holds across multiple embedding models (tested on BGE-M3 only for geometric; valence is model-independent)
- Whether the 6 stable_neutral lines (a subset of the 24 kernel lines) show stronger depletion than the other 18 kernel lines (0/6 吉 vs 1/18 吉 — too small for statistical test)
- Gradient analysis: do hexagrams with partial 比和 (e.g., main=比和 but 互≠比和) show intermediate 吉 rates?

---

## Iteration 8 Addendum: Q-gradient — Threshold vs Gradient in 吉 Depletion

**Computed during gate review, no separate script.**

### What was tested

The kernel condition for 吉 depletion was refined. There are 6 hexagrams with main + 互 both 比和 (not 4 as initially stated): h=0 坤|坤, h=14 巽|震, h=31 乾|兌, h=32 坤|艮, h=49 震|巽, h=63 乾|乾. The extra 2 (h=14, h=49) are Wood|Wood pairs. The 4-hexagram subset tested in probe 7a (h=0,31,32,63) are Earth/Metal pairs.

The question: is the 吉 depletion a gradient (proportional to diagnostic-silence depth) or a threshold (requiring full silence)?

### What was found

**[measured] The effect is a threshold, not a gradient.**

| Group | N hex | N lines | Standalone 吉 | Rate |
|---|---|---|---|---|
| kernel4 (Earth/Metal, has 變=比和 lines) | 4 | 24 | 0 | 0.000 |
| extra2 (Wood, no 變=比和 lines) | 2 | 12 | 2 | 0.167 |
| same-elem non-kernel | 8 | 48 | 12 | 0.250 |
| different-elem | 50 | 300 | 92 | 0.307 |

The 2 Wood hexagrams (h=14 恒, h=49 益) have baseline 吉 rates despite sharing main+互=比和 with the kernel4. The discriminant is whether the hexagram contains ANY line reaching full diagnostic silence (main + 互 + 變 all 比和). This requires Earth or Metal element pairs — the only elements with Hamming-1 same-element trigram pairs (via bit 2 flip: 坤↔艮, 兌↔乾). Wood trigrams (震↔巽) differ at all 3 bits, so no single-line change stays in Wood.

**[proven] The kernel4 = Earth/Metal same-element pairs from Finding 8a.3.** The mechanism identified in 8a.3 (only Earth and Metal have Hamming-1 same-element pairs at bit 2) is the same mechanism that generates the 吉-depleted set. The kernel states where the 梅花 grammar goes silent are EXACTLY the states where the bit-flip geometry keeps the element constant.

**Corrected kernel condition:** The 吉-depleted set is the 4 hexagrams {0,31,32,63} = Earth/Metal pairs where at least one moving line produces a 變卦 with same-element upper and lower trigrams. The condition "main + 互 both 比和" is necessary but not sufficient — it gives 6 hexagrams, of which only 4 are 吉-depleted. The 變卦 condition (at least some lines reach full silence) is the true threshold.

---

## Final Synthesis

Eight iterations, eight probes. The workflow produced three structural layers of findings, a set of bounded nulls, and better questions than it started with.

### Three structural layers

**Layer 1: Internal consistency and Z₅ unification.** The 梅花 system's operational grammar is internally consistent (10/10 examples), has a 4+1 invariant structure with a single free parameter (体克用 valence), and connects to the dynamics framework through complement-Z₅. The competition template is the unique structural optimum — maximum symmetry and maximum favorability simultaneously. The complement-Z₅ involution generates effects at five levels:

| Level | Phenomenon | Mechanism |
|-------|-----------|-----------|
| Dynamics (Phase 7) | Valve constraint (克→生=0) | Z₅ complement reflection |
| Interpretation (8c-ext) | R=B invariance | Z₅ complement → sign-flip bijection |
| Combinatorics (8c-ext2) | R=B count = 56 | Z₅ quadratic residue structure |
| Temporal (8b) | 12/60 relation uniformity | Z₅ orbit sum invariance |
| Text-algebra convergence (7a) | Kernel 吉-depletion | Bit-flip geometry → diagnostic silence |

**Layer 2: The 梅花/火珠林 boundary.** The Z₁₂→Z₅ projection (地支→五行) is where complement-Z₅ breaks. Above this projection (trigram level, 梅花), complement symmetry holds universally. Below it (line level, 火珠林 納甲), the non-uniform fiber structure ({4,2,2,2,2}, Earth oversized) creates position-dependent Z₅ shifts. The same fiber distribution is irrelevant to global orbit sums (8b: relation uniformity is automatic) but causal for local window consistency (8e: pointwise complement consistency fails). This is a single structural fact about the projection layer, not two independent findings.

**Layer 3: Cross-temporal convergence at the kernel.** The 4 hexagrams where the 梅花 algebra achieves complete diagnostic silence (all-比和 across main, 互, and at least one 變) are the same hexagrams where the 爻辞 texts (~1000 BCE) withdraw the standard unconditional positive marker 吉 (0/24, p=0.0006). The effect is:
- Specific to standalone 吉 — conditional markers (利), superlative markers (元吉), and all negative/neutral markers are at baseline rates
- A threshold at the 變卦 level — the 2 Wood hexagrams with main+互=比和 but no 變=比和 lines have baseline 吉 rates (0.167)
- Traceable to the bit-flip geometry from 8a.3: only Earth and Metal trigram pairs have Hamming-1 same-element pairs, creating the possibility of element-preserving single-line changes

The thematic account (these hexagrams have cautious content for thematic reasons) is weakened by the threshold structure: h=14 恒 (constancy) and h=49 益 (increase) have equally strong thematic content but normal 吉 rates, and they differ from the kernel precisely at the bit-flip geometry condition.

### What was not established

1. **No external predictive validity.** The grammar is internally consistent and externally unvalidated at any temporal resolution testable with available data. The 8b null (p=0.42–0.91) bounds the grammar's possible year-level effect to below Cramér's V=0.064.

2. **The cross-temporal correspondence (7a) could be convergent recognition or coincidence.** The p-value (0.0006) controls for random chance but not for unknown confounds at N=4 hexagrams.

3. **The 梅花/火珠林 boundary is structural, not evaluative.** Whether trigram-level complement-Z₅ (梅花) is "more correct" than line-level non-complement (火珠林) is an interpretive question the workflow does not adjudicate.

### Open questions, ranked by structural yield

**Q-天時.** Is 天時's frequency model (counting trigram occurrences) equivalent to spectral projection in the dynamics decomposition? The most structurally interesting open question — could unify 8c.6's "structurally different system" with the main framework.

**Q-complexity.** 比和 is algebraically most complex (dynamics) but interpretively simplest (always neutral). The deepest conceptual question — why does algebraic diversity force interpretive simplicity?

**Q-卦辭.** Does the 吉 depletion extend from 爻辭 (line statements) to 卦辭 (hexagram-level judgments)? The quickest computation — would strengthen or bound the 7a finding.

**Q-extractability.** Can L1+L2 of the 4-layer hierarchy decompose the 89% textual residual further?

**Q-34/52.** What are the 36 boundary states (18 improving + 18 deteriorating under a≠b)?

**Q-factoring.** Does the 納甲 8×4 factoring interact with 八宮 palace structure?
