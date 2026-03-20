# Empirical Probes — Findings

> Empirical workflow on the 梅花易數 operational system and related algebraic structures. Eight iterations, eight probes (8a, 8c, 8c-ext, 8c-ext2, 8b-parse, 8b-test, 8e, 7a). See `exploration-log.md` for full iteration details.

---

## Overview

The 梅花易數 was tested as an operational system — not for predictive validity (bounded by data resolution), but for internal structural consistency and algebraic properties. The text's algorithm, decision rules, and arc classification were extracted, formalized, and tested against the Phase 1–8 algebraic framework. The 皇極經世 event chronicle was parsed and tested for event-character correlation with the 五行 cycle. The 納甲 branch-element system was tested for complement-Z₅ consistency. The algebraic kernel states were tested for anomalous position in the semantic manifold and anomalous 爻辞 valence.

**Central finding:** The complement-Z₅ involution — the same algebraic structure that generates the valve constraint at the dynamics level (Phase 7) — also generates the rescued=betrayed arc symmetry at the interpretation level. The 梅花 system's operational grammar has a single free parameter (the valence of 体克用), and varying it degrades both the system's symmetry and its favorability simultaneously and monotonically. The competition template (10/17 domains) is the unique structural optimum.

**Boundary finding:** Complement-Z₅ holds at the trigram-element level (梅花) but fails at the line-element level (火珠林 納甲). The boundary is at the Z₁₂→Z₅ projection — non-uniform 地支→五行 fibers break pointwise consistency while preserving global orbit-sum invariance.

**Cross-level finding:** The 4 algebraic kernel hexagrams (Earth/Metal pairs where bit-flip geometry preserves element identity) are completely depleted of standalone 吉 in the 爻辞 texts (0/24 vs 106/360, p=0.0006). No other valence marker is anomalous. The effect is a threshold at the 變卦 level — 2 additional hexagrams sharing main+互=比和 but lacking any 變=比和 lines have baseline 吉 rates. The algebra's diagnostic-silence points coincide with the texts' affirmation-absence points — a cross-temporal correspondence between a ~1000 BCE text and a ~1000 CE algebraic framework.

---

## Findings

### From Probe 8a: Algorithm Verification

**8a.1 [measured]** 10/10 worked examples are internally consistent. Every example passes all 5 mechanical checks (arithmetic, hexagram identity, 互, 變, 体用 assignment).

**8a.2 [proven]** The 192/384 parity constraint applies specifically to the date formula (year+month+day+hour). Other 先天 methods (sound, strokes, tones) use independent sums, breaking the parity lock. "先天" is broader than "date formula."

**8a.3 [proven]** The 6 stable_neutral states (all-比和 relation vector) are the kernel of the 五行 map on the even-parity fiber. They coincide with the RG attractor (坤, 乾) + predecessors (剥, 夬) from the dynamics findings. Mechanism: only Earth and Metal have Hamming-1 trigram pairs, differing at bit 2 only (= lines 3/6), which is the kernel of the 五行 map within the even-parity fiber.

**8a.4 [measured, N=10]** The practitioner's interpretive process separates into position selection (mechanizable — scan for adversarial minimum) and semantic interpretation (requires question content + 象 imagery). Maps to Finding V.5's extractability boundary.

**8a.5 [measured]** When 五行 grammar saturates (all-比和), the text escapes to Z₂ counting ("群阴剥阳"). Fallthrough from Z₅ typing to Z₂ counting — vertical descent in formalism, not exit from it. 火珠林's analogous escape is lateral (visible → 伏神).

**8a.6 [measured, N=10]** 象 imagery always reinforces (never contradicts) the 五行 signal in the pedagogical examples. The 象 layer functions as translation vocabulary, not independent information source.

### From Probe 8c: Decision Grammar

**8c.1 [measured]** The 18-domain decision table has a **4+1 invariant structure.** Four relations have domain-invariant valence:

| Relation | Valence | Invariant across 17 体用 domains |
|---|---|---|
| 用克体 | always - | ✓ |
| 体生用 | always - | ✓ |
| 用生体 | always + | ✓ |
| 比和 | always + | ✓ |
| **体克用** | **domain-dependent** | **✗** |

体克用 has three modes: competition (+, 10 domains), manifestation (+~, 5 domains), nurture (-, 2 domains).

**8c.2 [proven]** The 4+1 structure reflects a 五行 grammar asymmetry: 生 is self-referential (creator depletes regardless of recipient → context-free valence), 克 is other-referential (destroyer's welfare depends on target → context-dependent valence). Maps to the dynamics valve: context-dependent 克 cannot directly produce context-free 生.

**8c.3 [measured + conjectured]** The interpretation system operates as a 4-layer override hierarchy with decreasing formalizability and activation frequency:

| Layer | Formalizability | Frequency |
|---|---|---|
| L1: Base 5-relation template | Fully mechanical | Always |
| L2: Domain-specific 体克用 mode | Fully mechanical | 7/17 domains |
| L3: 十應/三要 external omens | Requires perception | When omens present |
| L4: 体用 abandonment / Z₂ fallthrough | Requires structural judgment | 6/384 states |

**8c.4 [measured]** Adversarial-first ordering (hypothesized from 8a worked examples) is REFUTED for domain templates. Templates use 体's-agency-first ordering. Adversarial-first was a feature of narrative exposition, not template structure.

**8c.5 [measured]** 0/17 体用 domains reference hexagram names. The naming channel is practitioner lore, not system architecture. Two formal channels (五行 arc + 爻辞 text), not three.

**8c.6 [measured]** 天時占 (weather) is a structurally different system: frequency model (counting trigram occurrences) vs relational model (evaluating 五行 relations). The only domain using what the dynamics findings would call "spectral" analysis.

**8c.7 [measured]** 象 tables function as vocabulary (lexicon for translating algebra into predictions), not protocol (deterministic lookup). 0/10 worked examples use the 8-trigram outcome tables. All 象 invocations trace to the 万物属類 table.

### From Probe 8c-ext: Arc Symmetry Under Domain Templates

**8c-ext.1 [proven]** Rescued = Betrayed symmetry (R=B) is INVARIANT under all valence templates. This is a theorem of the complement involution σ: hex → 63-hex, which induces -id on Z₅ and sign-flips all 4 relation-vector positions simultaneously (verified 384/384).

**8c-ext.2 [measured]** Improving = Deteriorating symmetry (I=D) holds only under competition. Breaks under manifestation (I=30, D=78), nurture (I=12, D=86), and nurture-full (I=40, D=56).

**8c-ext.3 [measured]** Favorable→unfavorable flow is one-directional under manifestation (33→0) and nurture (69→0). Competition template is the unique favorable maximum. Exception: nurture-full (生產) partially recovers (68→40) via 体生用 inversion.

**8c-ext.4 [proven]** All 6 stable_neutral states survive under every template. The grammar's diagnostic-silence points are absolute.

**8c-ext.5 [measured]** Arc reclassification scales with template distance: 32% (manifestation), 47% (nurture), 72% (nurture-full). Under nurture: zero stable_favorable states remain.

### From Probe 8c-ext2: Symmetry Theorem

**8c-ext2.1 [proven empirically, 16 alphabets]** Three-tier symmetry theorem:

| Symmetry | Condition | Mechanism |
|---|---|---|
| R=B | Any positive (a, b) | σ negates all signs → rescued↔betrayed bijection |
| I=D | Symmetric alphabet: V(r) = -V(σ(r)) | Sign-negation preserved → improving↔deteriorating balanced |
| Stable_neutral invariance | Any alphabet | All-比和 → all-zero under any weighting |

**8c-ext2.2 [proven empirically]** I=D holds for all symmetric alphabets. Two I=D counts: 34 (a=b, exact negation) and 52 (a≠b, compensated balance). The 18-state gap represents valence-tied boundary states.

**8c-ext2.3 [measured]** Breaking boundary: I=D fails when V(体克用) ≤ 0 (sign-negation failure) or when partial valence degeneracy occurs (V(体克用) = V(生体)). The manifestation template (体克用=0) is exactly at the breaking boundary.

**8c-ext2.4 [proven]** Competition template is simultaneously the maximum-symmetry point (R=B + I=D) and maximum-favorability point. Domain specialization degrades both simultaneously. Forced by the 4+1 structure: 体克用 is the only modifiable relation, and any reduction of its positivity crosses the sign-negation boundary.

**8c-ext2.5 [measured]** R = B = 56 for all symmetric alphabets. The count decomposes as 2 × 28 (upper/lower symmetry), with inner 28 from Z₅ quadratic residue structure × trigram bit-flip geometry × {2,2,2,1,1} partition.

**8c-ext2.6 [proven]** The complement-Z₅ involution unifies three levels:

| Level | Phenomenon |
|---|---|
| Dynamics (Phase 7) | Valve constraint (克→生 = 0) |
| Interpretation (this workflow) | R=B invariance |
| Combinatorics (this workflow) | R=B count = 56 via Z₅ QR structure |

### From Probe 8b: 皇極經世 Event Chronicle

**8b.1 [measured]** 1111 events extracted from 1320 year entries (84.2% coverage) across ~400 BCE to ~960 CE. 天干 distribution perfectly uniform (132/stem). Selection bias precondition passed: blank years uniformly distributed across 10 stems (χ²=7.70, p=0.56) and 5 elements (χ²=3.61, p=0.46).

**8b.2 [proven]** The 天干→五行 mapping on consecutive years produces only 比和 and 生, never 克. The 天干 cycle IS the 五行 生 cycle encoded in time. Consequence: E2 (克→克 suppression) and E3 (valve: 克→生=0) are structurally untestable at year-level resolution.

**8b.3 [measured]** All statistical tests return null:

| Test | χ² | df | p | Cramér's V |
|---|---:|---:|--:|---:|
| Event character × 5 elements | 1.96 | 4 | 0.74 | 0.064 |
| Event character × 10 stems | 4.05 | 9 | 0.91 | 0.092 |
| Stem-branch 五行 relation (八字) | 3.91 | 4 | 0.42 | 0.091 |

Effect size bound: with N=477, any association < Cramér's V=0.064.

**8b.4 [measured]** 120-permutation control: all 120 permutations of the 5 elements produce identical χ² values. The canonical 五行 ordering is not special because no ordering is special. Event character is completely independent of position in the 10-year stem cycle.

**8b.5 [proven]** Z₅ orbit invariance: the 12/60 relation uniformity (each of 5 stem-branch 五行 relations appears exactly 12 times in the 60-year cycle) is forced by Z₅ cyclic structure, independent of 地支→五行 distribution. Proof: summing n_{σ_R(E)} over a complete Z₅ orbit gives Σn_i regardless of the distribution {n_i}. The sexagenary cycle is a universal 五行 balance instrument — not by design, but by group theory.

**8b.6 [measured]** Approach B (month-level date resolution) blocked: only 10/1111 entries (0.9%) mention specific months.

### From Probe 8e: 納甲 Under Complement-Z₅

**8e.1 [proven]** Complement-Z₅ (σ = -id on Z₅) holds at the trigram-element level but FAILS at the 納甲 branch-element level. σ produces 4 different Z₅ shifts {0, 1, 3, 4} across the 4 complement pairs. Only 2/32 hexagram complement pairs have a uniform 6-line Z₅ shift.

**8e.2 [proven]** Root cause: the Z₁₂ → Z₅ projection via 地支→五行 has non-uniform fibers (Earth=4, others=2). Arithmetic progressions in Z₁₂ (branch ring) become non-arithmetic in Z₅ (element ring) after projection. Different starting points produce different Z₅ step patterns.

**8e.3 [measured]** 艮↔兌 is the unique fully consistent complement pair (standard 納甲). This is a numerical coincidence of starting offsets — verified by showing that pairs summing to 9 in Z₁₂ do not generally have constant Z₅ diffs.

**8e.4 [proven]** 24 alternative TRIGRAM_BRANCH_START tables achieve full complement consistency. None includes the historical values (乾=0, 震=0 not in the consistent set {1,2,3,4}). The system was not designed for complement consistency at the branch level.

**8e.5 [measured]** The corrected 京氏 rule (universal +3 upper offset) makes complement consistency worse (3/8 → 2/8 consistent half-configurations). The modern 火珠林 modification is closer to complement consistency than the original.

**8e.6 [proven]** The 納甲 map is not a group homomorphism from Z₈×Z₃ → Z₅. It is a composition of an affine step in Z₁₂ (branch ring) followed by the non-linear 地支→五行 projection. Line elements are NOT the trigram element repeated — each trigram's 3 line elements span 2–3 distinct 五行 elements.

### From Probe 7a: Kernel Hexagrams in the Semantic Manifold

**7a.1 [measured]** The 4 kernel hexagrams (h=0 坤|坤, h=31 乾|兌, h=32 坤|艮, h=63 乾|乾) are individually closer to the semantic center than average (z=−1.52 in residual space) but NOT mutually clustered (permutation p=0.455). They are semantically generic but thematically dispersed — consistent with "neutral/undifferentiated" rather than "similar."

**7a.2 [measured]** Standalone 吉 is completely absent from the 4 kernel hexagrams:

| Marker | Kernel (N=24) | Other (N=360) | Fisher p |
|---|---|---|---|
| Standalone 吉 (not 元吉) | 0/24 (0.000) | 106/360 (0.294) | **0.0006** |
| 元吉 (superlative) | 1/24 (0.042) | 11/360 (0.031) | 0.54 |
| 利 (conditional) | 4/24 (0.167) | 52/360 (0.144) | 0.76 |
| 无咎 (neutral) | 6/24 (0.250) | 78/360 (0.217) | 0.80 |
| 凶 (negative) | 5/24 (0.208) | 47/360 (0.131) | 0.35 |

The effect is specific to standalone 吉. Every other valence marker (positive, negative, neutral) is at baseline rates.

**7a.3 [measured]** The 吉 depletion requires the full kernel condition, not just same-element. Three-level stratification of the 14 same-element hexagrams:

| Group | N hex | N lines | Standalone 吉 | Rate |
|---|---|---|---|---|
| Kernel (Earth/Metal, has 變=比和 lines) | 4 | 24 | 0 | 0.000 |
| Extended (Wood, main+互=比和 but no 變=比和) | 2 | 12 | 2 | 0.167 |
| Same-element only (main=比和, 互≠比和) | 8 | 48 | 12 | 0.250 |
| Different-element (baseline) | 50 | 300 | 92 | 0.307 |

The effect is a threshold at the 變卦 level. The 2 Wood hexagrams (h=14 恒, h=49 益) share main+互=比和 with the kernel but have baseline 吉 rates because no single-line change stays in Wood (震↔巽 differ at all 3 bits). The discriminant is whether the hexagram contains any line reaching full diagnostic silence — which requires Earth or Metal element pairs (the only elements with Hamming-1 same-element trigram pairs, from Finding 8a.3).

**7a.4 [measured]** The kernel's single 吉 occurrence is 坤 L5 (黃裳元吉), which is 元吉 (superlative form), not standalone 吉. The texts withhold the standard unconditional positive marker while allowing conditional markers (利), superlative markers (元吉), and all negative/neutral markers at normal rates.

---

## Synthesis

### What was established

The 梅花易數's operational grammar is internally consistent (10/10 examples), structurally clean (4+1 invariant structure with a single free parameter), and algebraically connected to the dynamics findings (complement-Z₅ unification). The system was designed as a judgment instrument with a precise extractability gradient: fully mechanical at L1+L2 (covering all states across all domains), requiring perception at L3, requiring structural judgment only at the 6 kernel states (L4).

The complement-Z₅ involution σ is the deepest shared invariant. At the dynamics level it generates the valve (克→生=0). At the interpretation level it generates R=B invariance. At the combinatorial level it fixes the R=B count at 56 through the Z₅ quadratic residue structure. At the temporal level, Z₅ orbit-sum invariance forces automatic relation uniformity in any cycle-based system. This confirms that the 梅花 operational system and the Phase 7 dynamics decomposition are not independent descriptions — they are two views of the same algebraic structure.

The competition template (体克用 = favorable, 10/17 domains) is the unique structural optimum: maximum symmetry (both R=B and I=D) and maximum favorability. Domain specialization monotonically degrades both properties. The tradition's anxiety about nurture domains (飲食, 生產 — zero stable_favorable states) is structurally justified.

### The complement-Z₅ boundary

Complement-Z₅ marks a clean structural boundary between 梅花 and 火珠林:

| Property | 梅花 (trigram level) | 火珠林 (line level) |
|----------|---------------------|---------------------|
| Element assignment | 8→5 surjection | 48→5 via Z₁₂ projection |
| Complement-Z₅ | σ = -id (universal) | σ → {0,1,3,4} (pair-dependent) |
| Algebraic structure | Group homomorphism | Affine + non-linear projection |
| Resolution | Global (complete orbits) | Local (3-element windows) |

The 地支→五行 fiber map ({4,2,2,2,2}) is irrelevant to global properties (8b: orbit-sum invariance holds for any distribution) but causal for local properties (8e: pointwise consistency fails because of Earth's oversized fiber). Systems working above the Z₁₂→Z₅ projection (梅花: trigram elements) inherit complement-Z₅. Systems working below it (火珠林: branch elements) do not.

### The 89%/11% boundary and its kernel exception

The Phase 3 finding (11% algebraic, 89% text-independent) was measured at the text level. At the operational level, the 4-layer hierarchy shows why: L1+L2 use only the 五行 relation vector (algebraic channel). L3+ uses 象 imagery and 爻辞 text (textual channel). These are parallel channels converging at the output — the algebra provides valence, the text provides vocabulary. The 89% independence is exactly what this parallel architecture predicts.

The kernel 吉-depletion (7a.2) is a local exception to this global independence. The algebraic channel goes to zero at the kernel (all-比和 = no signal). The textual channel independently withholds standalone 吉 at the same states (0/24, p=0.0006). The channels are independent in the interior (360 non-kernel lines) but correlate at the origin (24 kernel lines). This is consistent with orthogonal dimensions sharing a boundary condition — both channels detect the same structural property (undifferentiation) from different directions.

The effect is a threshold, not a gradient (7a.3). The 2 Wood hexagrams with main+互=比和 but no 變=比和 lines have baseline 吉 rates (0.167 vs 0.307). The discriminant is the bit-flip geometry from Finding 8a.3: only Earth and Metal have Hamming-1 same-element trigram pairs (via bit 2), which creates lines where a single change preserves full element identity across all layers. The 吉-depletion marks the boundary where the algebra achieves complete diagnostic silence — and the texts respond with complete affirmation silence.

The correspondence is cross-temporal: the 爻辞 texts (~1000 BCE) predate the formal 五行 framework (~300 BCE) and the 梅花 algebraic analysis (~1000 CE) by centuries. The algebraic kernel condition — total self-relation across all layers — picks out hexagrams whose texts independently encode the same condition through 吉-withdrawal.

### Data resolution boundary

The 皇極經世 event catalogue (1111 events, year-level) returns null across all tests (p=0.42–0.91). The grammar requires relational input (体 + 用) at temporal resolution finer than year-level. The 梅花 date formula demands hour-level input. Only 0.9% of chronicle entries mention specific months. A source with full date resolution (year+month+day+hour) would enable the relational test.

---

## Open Questions (generated by this workflow)

Ranked by structural yield:

**Q-天時.** Is 天時's frequency model (counting trigram occurrences) equivalent to spectral projection in the dynamics decomposition? Trigram indicators are specific Walsh functions — does 天時 use the same modes that carry the 五行 information?

**Q-complexity.** 比和 is algebraically most complex (dynamics) but interpretively simplest (always neutral). Is interpretive simplicity forced by algebraic diversity (wide range → heterogeneous → no consistent signal)?

**Q-extractability.** Can the 4-layer hierarchy produce a finer decomposition of the 89% residual? L1+L2 are fully mechanical — what fraction of interpretive output can they generate?

**Q-34/52.** What are the 36 boundary states (18 improving + 18 deteriorating under a≠b, 36 stable under a=b)? Do they have a combinatorial characterization?

**Q-factoring.** The 納甲 complement diff patterns factor as 8 lower × 4 upper (not 8×8). The asymmetry comes from 乾/坤 position-dependence. Does this factoring interact with 八宮 palace structure?

**Q-卦辭.** Does the 吉 depletion extend from 爻辭 (line statements) to 卦辭 (hexagram-level judgments)?
