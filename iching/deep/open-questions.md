# Open Questions

## Central thread

Structure → incompleteness → curvature → specificity → meaning.

The algebraic characterization is complete at this resolution. Z₂⁶ with shell/core projections, 五行 coordinates, basin convergence, palace walks, 六親 near-bijection. Two divination systems exhaust the hexagram's information through the only two primitive projections available (proven algebraically, confirmed historically). Orthogonality between 納甲 and core is confirmed; leakage at the element level is quantified (~7%, which is 2.5/6.0 = 42% at the bit level, collapsing to near-zero through the 五行 quotient). Temporal curvature is characterized: three sources, one softened by 日辰 to a 1/5 residual (proven as theorem). Two bridges connect algebra to text: 凶×basin (core, p=0.0002) and 吉×生体 (shell, p=0.007, basin-independent). Both encode process not state. Bridge orthogonality is proven at the perturbation level (atlas workflow).

The atlas establishes the coordinate system as informationally complete (zero residual: H(hexagram | full profile) = 0.0 bits). Combined with zero free parameters — now fully proven (R32: the 0.50-bit cosmological choice is forced by conjunction of textual bridge + cycle attractor semantics, 0/32 alternatives viable) — this means: the encoding is complete in both directions, and uniquely determined. The atlas is the terminal structural computation — remaining questions are queries against it, not new constructions.

The atlas further establishes: the {2,2,2,1,1} partition is the single organizing principle from which all structural properties derive; the torus is the frame (epistemology — when you can see what) while the Z₅ diagonal quotient is where meaning lives (ontology — what things signify); and the core is time-independent (orthogonality wall) while the shell is time-modulated.

**The 梅花 atlas extends this:** The 384-state expansion (64 hexagrams × 6 動爻) projects the hexagram space into a directed, depth-stratified evaluation. Two independent information channels (text ↔ present state, arc ↔ trajectory) operate through the same Z₅×Z₅ geometry but with different axes (positional vs relational). The 體/用 cut converts static algebra into directed reading — "temporal" in 梅花 is structural depth rendered as narrative.

---

## 1. Formal H¹ computation

**Status: open, lower priority**

All three curvature sources are quantified (用神 projection: 45/20/35; seasonal ceiling: 2/5→4/5; palace holes: 16:32:16). The qualitative picture is clear and the orthogonality wall limits the interpretive reach of H¹ (the shell-layer presheaf cannot see core-layer dynamics).

A formal computation could test whether curvature varies with basin, palace rank, or 互 depth. But the expected payoff is a numerical refinement of an already-clear structural picture, not a new insight.

**Atlas-informed refinement:** The constraint analysis shows basin ⊥ rank (MI=0.000), which means H¹ cannot vary jointly with basin and rank — they contribute independently. This further limits the degrees of freedom available for curvature variation.

---

## 2. Is the 五行 assignment necessary or arbitrary?

**Status: RESOLVED → R32**

---

## 3. The 納甲 modification

**Status: documented, historical question**

京氏易傳 uses universal upper trigram branch offset +3 (63/63 match). 火珠林 modified to 乾/坤-only, gaining one unique 六親 word (58→59/64). The modification improved 六親 near-injectivity at the cost of one rule exception.

When did this modification occur? Answering requires surveying intermediate texts (唐–宋 dynasty) between 京氏易傳 and modern practice. This is a historical-philological question, not a computational one.

---

## 4. Semantic mapping — text-first characterization

**Status: open, foundational**

All prior semantic work approached from algebra → text: does algebraic position predict textual content? The answer is mostly null (R25: <1% variance, R22: 納音 null, R12: thematic null). But this tested the wrong direction. We never characterized the texts *on their own terms* to discover their intrinsic structure, then compared with algebra.

### What's missing

**The 卦辭 corpus as a semantic object.** 64 short texts describing situations, imagery, judgments. What themes recur? What situations cluster? Is there an intrinsic semantic structure — groups of hexagrams that talk about similar things — independent of any algebraic coordinate?

**The 爻辭 corpus.** 384 line texts. Beyond valence markers (吉/凶/悔/吝), the content is untouched. What do lines at nuclear positions (2-5) talk about vs outer lines (1,6)? Do initial lines (初) share themes across hexagrams? Do top lines (上) share themes? Is there a positional semantic signature?

**The 象傳 layer.** 64 大象 (hexagram-level images) explicitly describe trigram interaction ("天行健" = heaven moves vigorously for 乾). These are the interpretive layer closest to the shell projection. Do 大象 descriptions correlate with surface 五行 relations? They should — they're literally describing the trigram pair. The question is whether they do so through 五行 language or through independent imagery.

**The 彖傳 layer.** Hexagram commentaries that explicitly discuss trigram relationships. Do they use 生/克 language? Do they reference upper/lower interaction in terms that map to the directed relation (生体 vs 体生用)?

**Cross-text consistency.** Do 卦辭, 彖傳, and 象傳 agree on the same hexagram? Disagreements would reveal where different textual layers encode different aspects — potentially mapping to the shell/core distinction.

**火珠林 domain sections.** The 用神 mapping (30+ domains → 六親 types) has never been extracted or formalized. This is the practitioner's semantic layer — the bridge from human concerns to algebraic positions.

**梅花易數 worked examples.** Shao Yong's actual readings. What reasoning pattern does he follow? Does his interpretation trace the core projection (體→互→變) or does he use shell-level reasoning?

### Approach: text → structure → compare

1. **Characterize the 卦辭 independently.** Cluster the 64 texts by semantic similarity (embeddings exist). Identify the natural groupings. Label the clusters by dominant theme/imagery. This produces a *text-derived* partition of the 64 hexagrams.
2. **Compare text-derived partition against algebraic partitions.** MI between text clusters and (basin, palace, kernel, surface relation, depth relation). If MI > 0 for any algebraic coordinate, the text encodes that coordinate — but discovered bottom-up rather than imposed top-down.
3. **Characterize 爻辭 by line position.** Pool all 初 lines, all 二 lines, ..., all 上 lines. Does each position have a semantic signature? Traditional commentary says yes (初=beginning, 上=excess). Test whether this is in the texts or only in the commentary.
4. **Extract 象傳 trigram language.** The 大象 texts describe trigram-pair interactions in natural language. Parse these into relation categories. Compare with the algebraic surface relation. This is where shell-level algebra should be *most* visible in text.
5. **Extract 彖傳 五行 language.** Search for generation/destruction vocabulary in the commentaries. Map occurrences to the algebraic 生/克 classification. Test agreement.
6. **Formalize the 用神 mapping.** Extract from 火珠林 text: domain → 六親 type → element. Build the complete practitioner's lookup table. Test internal structure (do related domains map to 生克-adjacent types?).

### What this would resolve

- Whether the text corpus has its own semantic structure that algebra partially captures (descriptive) or that algebra is orthogonal to (notational)
- Whether the 象傳/彖傳 explicitly encode 五行 relations — which would date the shell projection's recognition
- Whether the practitioner's 用神 mapping is structured or arbitrary
- Whether line position carries semantic weight independent of algebra — this would be evidence for a third organizing principle beyond shell and core

### Dependencies
- Embeddings exist (synthesis/embeddings.npz) for 卦辭, 爻辭, 大象, 彖傳
- Atlas coordinates exist (atlas/atlas.json) for all 64 hexagrams
- 火珠林 text exists (texts/huozhulin/huozhulin.md) for 用神 extraction
- 梅花易數 text exists (texts/meihuajingshu/) for worked examples

---

## 5. Temporal × semantic interaction

**Status: open, atlas-enabled, lower priority**

The atlas establishes: valence lives on the Z₅ quotient (p=0.75 spatial residual), and temporal coverage varies by season. Uncomputed: does the 凶×basin signal strength change when the basin's dominant element is 旺 (seasonally strong) vs 死 (seasonally weak)?

This requires crossing temporal.json (60 states) with valence_torus.json (per-cell rates). A small computation but potentially revealing: if the signal is purely algebraic (structural position in Z₂⁶), temporal context shouldn't modulate it. If it does modulate, the bridge has a temporal component not captured by the static atlas.

---

## 6. 火珠林 operational atlas

**Status: open, next major atlas**

The 梅花 atlas mapped one of two operational projections. 火珠林 uses the same hexagram space but evaluates through 六親 × 日辰 activation — a time-dependent 五行 overlay with a floating daily reference (日辰), vs 梅花's fixed 體 reference. The two systems make structurally different cuts through the same algebra.

**What a 火珠林 atlas would map:**
- 384-state table with 六親 evaluations per line position
- 用神 activation rules (which line "leads" the reading, by domain)
- 日辰 × state interaction (how daily element cycles modulate readings)
- The contrast with 梅花: fixed reference (體) vs floating reference (日辰)
- Whether 火珠林's 4/5 ceiling (via 日辰) produces a structurally different arc space than 梅花's 2/5 ceiling

**Dependency:** 火珠林 text extraction (partial in sy-divination.md), atlas.json, temporal.json.

---

## Resolved

### R1. Do the dropped 京氏 layers carry independent information?
**No.** H(all 5 fields | palace, rank) = 0.0000 bits. 火珠林's compression was lossless. (jingshiyizhuan workflow)

### R2. Does the full 京氏 temporal system resolve the 2/5 ceiling?
**No.** Finer notation repackages the same pentacyclic structure. Breaking the ceiling requires information orthogonal to 五行. (jingshiyizhuan workflow)

### R3. Are the astronomical assignments algebraically determined?
**Yes.** Each is a cyclic quotient of the palace walk: Q∈Z₃, planets∈Z₅, mansions∈Z₂₈, 建始∈Z₆₀. Zero design freedom in stepping; only palace base values are free. (jingshiyizhuan workflow)

### R4. Original vs modified 納甲 rule
**Discovery:** 京氏易傳 uses universal upper trigram branch offset +3 (63/63 match). 火珠林 modified to 乾/坤-only, gaining one unique 六親 word (58→59/64). Likely deliberate optimization. **Historical sub-question promoted to §3 above.** (jingshiyizhuan/findings.md §3)

### R5. Only two hexagram-reading methods exist
**Confirmed algebraically and historically.** Shell (3+3 trigram split) and core (1+4+1 nuclear overlap) are the only two primitive projections on the 3+3 factorization of Z₂⁶. Chinese sources independently classify hexagram divination into exactly 六爻/納甲法 and 梅花易數 — no third method. (huozhulin/findings.md, closure theorem)

### R6. The decisive test — text ↔ algebra
**MIXED — two bridges.** The oldest textual layers partially encode algebraic structure through two narrow channels: 凶×basin (core, p=0.0002) and 吉×生体 (shell, p=0.007, basin-independent). Both encode process not state. Deeper constructs (kernel, palace, I-component on embeddings) are null. Four definitive nulls bound the bridges: embedding-space (p>0.4), thematic content (p>0.07), KW between-pair ordering (p=0.76), 序卦 narratives (p>0.25). (synthesis Probes 1, 7, 8, 9)

### R7. Does 日辰 break the 2/5 ceiling?
**Yes — proven as theorem.** Maximum rises from 2/5 to 4/5. The excluded element alternates between 休 (exhausted source) and 死 (conquered object). 囚 (opposition) is always representable. 梅花 inherits 2/5. Pipeline asymmetry: 梅花 curves domain, 火珠林 curves codomain. Orthogonality wall untouched. (synthesis Probe 4)

### R8. Contextual obstruction × 凶
**NULL — predicted by orthogonality.** F_total = 12 conservation law. n_zero determined by missing-type count (16:32:16). Shell-layer measures cannot see core-layer 凶 signal — confirmed as algebraically orthogonal projections. (synthesis Probe 2)

### R9. 用神 mapping structure
**STRUCTURED — by 生克 cycle.** Auxiliary = 生-preimage (σ⁻¹). 忌神 = 克-preimage. 兄弟 (self) excluded as reference frame with 0 domains. 官鬼+妻財 = 15/22 = 68% of all domains. Structural space symmetric (2/5 suppression, 1/5 日辰-克, uniform across types). ALL asymmetry enters through 用神 projection's domain weighting (8:7:4:3:0). Gen palace darkest (missing 妻財+官鬼 = 68% of domains unreadable). Triad diagnostic: 45.3% full, 19.9% blind, 34.8% degraded. 兄弟's absence benign (0 domains). (synthesis Probe 3)

### R10. S₄ × 五行 involutions
**COMPLEMENT IS ANTI-AUTOMORPHISM.** π∘σ∘π⁻¹ = σ⁻¹, where π = (Earth↔Metal)(Fire↔Water)(Wood). Complement reverses 生 to 克, preserves 比/生/克 category (0% hexagram-level disruption), preserves b₀⊕b₁ parity universally. Semantic gap (reverse 0.720 > complement 0.680 > rev∘comp 0.673) tracks concrete visual identity, not abstract relational structure. Wood = fixed point of anti-automorphism. MI correction: 0.750 bits lost under complement pairing = within-pair element identity (Layer 2). As function, complement preserves ALL 五行 information (MI=2.250). (synthesis Probe 5)

### R11. Shell bridge (體/用 × valence)
**POSITIVE — 吉×生体 is genuine.** 生体 (用 nourishes 體) carries 44.4% 吉 vs 27.6% baseline (Fisher p=0.007, OR=2.10). Signal is basin-independent (same direction and magnitude in all three basins). 比和→凶 trend is confounded with basin and underpowered. The 梅花 tradition partially recovered 生体→吉 but distorted through symmetrization. (synthesis Probes 8, basin-controlled test)

### R12. 凶 content at depth boundary
**NULL — distributional not thematic.** Depth-1 hexagrams carry more 凶 (19.4% vs 12.8%), but 凶 text content doesn't systematically differ by depth. No word category reaches significance (best: threshold p=0.069). (synthesis Probe 7)

### R13. KW sequence algebraic structure
**NULL beyond pairing.** Between-pair ordering is algebraically random (p=0.76). Five-phase relations at chance. (synthesis Probe 6)

### R14. 序卦 narrative × algebraic transitions
**NULL.** All four cross-tabulations non-significant (all p>0.25). (synthesis Probe 9)

### R15. 五行 coordinate completeness (atlas)
**COMPLETE — zero residual.** H(hexagram | full 五行 profile) = 0.0 bits. The 13 coordinates jointly identify every hexagram uniquely. The coordinate system is informationally equivalent to Z₂⁶. Five minimal identifying pairs found. The bit-5 residual (6 non-singleton pairs, all XOR=32) is the exact gap between the 五行 projection and Z₂⁶, recovered by 六親. (atlas workflow)

### R16. Bridge orthogonality at perturbation level (atlas)
**PROVEN.** 體/用 distribution identical between boundary states (flip b₂/b₃) and non-boundary states. The two bridges do not interact through the 變 fan. Perturbation-level independence proven algebraically, not just measured statistically. (atlas workflow)

### R17. Perturbation onion structure (atlas)
**PROVEN — 4 layers (upgrades 3-layer model).** The 互 coordinate breaks the shell layer's symmetry: Outer (L1,L6) / Shell-outer (L5, 50% hu_cell preserved) / Shell-inner (L2, 0% preserved) / Interface (L3,L4, 0% preserved + 0% basin). L2/L5 asymmetry: b₁=LSB always crosses elements, b₄=MSB preserves for parity-0 coset {Earth,Metal}. (atlas workflow)

### R18. Forbidden cross-projection constraints (atlas)
**PROVEN.** Surface 克 excludes nuclear 生 (6/25 surface×hu relation pairs forbidden). hu_relation × basin: 7/15 forbidden (比和 only in FP basins, 生 only in Cycle). surface_cell × hu_cell: 252/300 forbidden. Same parity mechanism at both projection levels — one finding, two projections. Process-level constraint algebra exists. (atlas workflow)

### R19. Palace walk basin crossover = 游魂/歸魂 (atlas)
**PROVEN.** Basin flips at ranks 3 and 6 where mask b₂⊕b₃=1. Pattern: [0,0,0,1,0,0,1,0]. Traditional names track the return journey (游魂 = re-crossing at rank 6, 歸魂 = arrival at rank 7). 3 Z₅ equivalence classes (partition by parity coset), 2 abstract basin patterns (FP-rooted vs Cycle-rooted). (atlas workflow)

### R20. Torus structure and limitations (atlas)
**CHARACTERIZED.** Z₅×Z₅ is a lossy projection with variable resolution (4:2:1 population gradient). 互 not well-defined on it (17/25 cells, exact criterion: lower singleton + upper non-Wood). Complement is clean; reversal is not (6/28 selection rule). 2-cycle attractor isolated. The torus is the frame (epistemology — when is what visible), not the picture (ontology — that lives on the Z₅ quotient). Its geometry is essential for the seasonal diagonal sweep with wraparound; nowhere else. (atlas workflow)

### R21. Valence per Z₅×Z₅ cell (atlas)
**NULL spatial structure.** Both bridges replicated at torus level (core: χ²=17.44, p=0.0002; shell: Fisher p=0.033). Spatial residual: χ²=19.0, p=0.75. Valence is a function of the Z₅ quotient (directed relation), not Z₅×Z₅ position. The 25 cells collapse to 5 relation types; no cell-level information survives beyond the relation. (atlas workflow)

### R22. 納音 semantic probe (atlas)
**NULL beyond element.** KW H=57.67, p<0.0001 at 納音 name level, entirely explained by element grouping. 劍鋒金 doesn't predict sharp imagery; 海中金 doesn't predict water imagery. The finest-grained 五行 coordinate carries no semantic weight. (atlas workflow)

### R23. Temporal overlay on torus (atlas)
**COMPUTED.** Seasonal shadow: 2×2 active block sweeping diagonally with period 5. 日辰: quadratic amplification (active cells = n²). 60 states pre-computed in temporal.json. Fire/Water both active in 16/60 states. 1/5 residual stripe = ceiling theorem made geometric. 梅花 formula near-uniform (χ²=10.7), calendar application biased (χ²=481.8) — two different objects. (atlas workflow)

### R24. Tradition's interpolation (atlas)
**SYSTEMATIC DISTORTION.** Tradition symmetrizes directional signals: 生体→吉 confirmed (OR≈2.1), but 体生用 is weaker (34.7% vs 41.7%). 比和 contradicted — tradition reads state (harmony), texts encode process (convergence → danger, highest 凶 rate). 体克用 contradicted — high 吉 (37.2%), not 凶. Single principle: receiving > giving (inward flow → 吉). The tradition collapsed direction into category and lost the signal. (atlas workflow)

### R25. Thematic content by surface relation (atlas)
**NULL at semantic level.** Surface relation explains <1% of embedding variance despite statistical significance (KW p=0.0004, high power from ~73k comparisons). Confirms synthesis finding — trigram-pair identity drives similarity, not thematic content. (atlas workflow)

### R26. 梅花 torus flow — 互 as vector field on Z₅×Z₅
**COMPUTED — maximally multi-valued.** 梅花 torus (體,用 axes) has only 2/25 well-defined cells (vs atlas's 8/25). Population follows {2,2,2,1,1} partition (24:12:6 gradient). Wood,Wood reaches 6 互 targets (maximum). The 梅花 torus is a finer-grained but less deterministic view of the same geometry — the line-level expansion (64→384) amplifies multi-valuedness. (mh-atlas workflow)

### R27. 梅花 arc classification
**COMPUTED — 8 arc types, symmetric with basin dependence.** rescued/betrayed = 56/56, improving/deteriorating = 52/52. Cycle basin concentrates in mixed (76.1%). Mixed has lowest 凶 (7.5%). ti_hu 克-dominance (63%) = perturbation onion L2/L5 at interpretation level. 互 amplifier confirmed (OR=1.96, p=0.007). 183/625 relation vectors realized (29.3%). (mh-atlas workflow)

### R28. 梅花 two-channel architecture
**CONFIRMED — text ↔ arc are independent channels.** 爻辭 encode present state (ben_relation), 體/用 arc encodes trajectory (本→互→變). 先天 drops text channel; 後天 uses both. Parity wall (192/384 reachable by 先天) biases arc channel (stable_favorable OR=5.23, p=0.0002) but NOT text channel (吉/凶 balanced). The system expects channel disagreement and provides resolution protocol. (mh-atlas workflow)

### R29. 比和 discrepancy at 梅花 level
**PARTIALLY RESOLVED.** 比和-at-本 凶 elevation (20.2% vs 11.7%) persists within each basin (Kun 29.2%/18.1%, Qian 25.0%/19.4%, Cycle 11.1%/5.1%). Not purely basin confound. 比和-at-本 locked to improving/deteriorating/neutral/mixed (no rescued/betrayed from valence=0). Tradition's "百事順遂" scoped to 体用 only, not full arc. Small within-basin samples prevent definitive statistical closure. (mh-atlas workflow)

### R30. 梅花 18 domain structure
**ONE ENGINE, 18 SKINS.** All 17 體/用 domains use identical 5-relation evaluation. No domain modifies the 生克 logic. Domain-specific content enters through: (1) semantic binding (what 體/用 represent), (2) trigram imagery, (3) optional sub-systems (present in 3 domains: 婚姻 appearance types, 生產 gender counting, 疾病 3 sub-systems). Six structural clusters: self-vs-other (3), self-vs-asset (4), self-vs-endeavor (4), body-vs-condition (2), self-vs-dwelling (3), self-vs-absent (1). The 18 are explicitly exemplars ("占者以類而推之可也"), not exhaustive. 天時 sole exception (committee reading, no 體/用). (mh-atlas workflow, verified against vol 2 text)

### R31. 先天 parity wall
**PROVEN — 192/384 reachable.** The 先天 formula has a hard parity constraint: total determines both lower trigram and line position, coupling their parities. Even total → even lower trigram + odd lines only; odd total → odd lower trigram + even lines only. Every hexagram reaches exactly 3 of 6 lines. The unreachable half is arc-biased: stable_favorable vs stable_unfavorable OR=5.23 (p=0.0002), but text-channel valence (吉/凶) is balanced across both halves. 先天 and 後天 operate in structurally complementary state spaces — 後天 is not redundant but necessary for full 384-state coverage. (mh-atlas workflow)

### R32. 五行 assignment is necessary — zero free parameters
**PROVEN BY CONJUNCTION FORCING.** The 0.50-bit cosmological choice (which odd-coset complement pair to keep together) is uniquely determined by the conjunction of two independent criteria. Tested all 32 complement-respecting alternative assignments (16 type-B "pair {Kan,Li}", 16 type-C "cross-pair {Kan,Zhen}+{Li,Xun}"):

1. **吉×生体 textual bridge:** Traditional A achieves OR=2.10, p=0.007 (32/72 = 44.4% 吉 in 生体). Best alternative: B.3 at OR=1.69, p=0.065 (marginal). **0 of 32 alternatives reach p<0.05.** The traditional assignment is the unique one where the textual bridge is statistically significant.

2. **既濟/未濟 cycle attractor semantics:** Traditional A: 既濟=克体, 未濟=体克用 (Water/Fire 克 tension). Assignment B: both → 比和 (pairing {Kan,Li} collapses the completion/incompletion dialectic to identity). Assignment C: 体克用/克体 (克 preserved but inverted direction).

No single criterion eliminates all alternatives:
| Property | A (Traditional) | B (16 variants) | C (16 variants) |
|----------|----------------|-----------------|-----------------|
| 吉×生体 p<0.05 | ✓ (p=0.007) | ✗ (best p=0.065) | ✗ (best p=0.159) |
| 既濟/未濟 = 克 | ✓ | ✗ (比和) | ✓ (inverted) |
| π = -x mod 5 | ✓ | ✓ | ✓ |
| Parity separation | ✓ | ✓ | ✓ |
| 互 well-defined ≥8/25 | ✓ (8) | ✓ (8) | ✗ (4) |

But the **conjunction** of textual bridge + cycle attractor semantics uniquely selects A. **The entire 五行 assignment has zero free parameters: 1.75 bits algebraic + 0.50 bits forced by conjunction.**

**Surprises:**
- C retains complement=negation (predicted to break — wrong; cross-pairs at conjugate positions suffice).
- C achieves PERFECT zero residual (64/64 unique profiles vs A's 52/64) but at the cost of halved 互 well-definedness (4/25 vs 8/25). C trades global uniqueness for local coherence — the wrong tradeoff for a divination system.
- B collapses {Kan,Li} Hamming-3 distance into one element, destroying the Fire/Water bridge — the exact locus where Z₂ and Z₅ optimally coincide.

**The singleton-attractor mechanism:** Only assignment A places the 互 cycle attractors (既濟/未濟 = Kan/Li) as singletons. This makes Z₅ injective at the convergence locus — where depth flow terminates, element identity is unambiguous. B pairs them (fiber=2, ambiguous), C makes different trigrams singletons (Gen/Dui, not the attractors). The Fire/Water bridge exists because the singletons ARE the attractors. (deep/01_assignment_test.py, deep/exploration-log.md)
