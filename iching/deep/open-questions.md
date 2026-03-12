# Open Questions

## Central thread

Structure → incompleteness → curvature → specificity → meaning.

The algebraic characterization is complete at this resolution. Z₂⁶ with shell/core projections, 五行 coordinates, basin convergence, palace walks, 六親 near-bijection. Two divination systems exhaust the hexagram's information through the only two primitive projections available (proven algebraically, confirmed historically). Orthogonality between 納甲 and core is confirmed; leakage at the element level is quantified (~7%, which is 2.5/6.0 = 42% at the bit level, collapsing to near-zero through the 五行 quotient). Temporal curvature is characterized: three sources, one softened by 日辰 to a 1/5 residual (proven as theorem). Two bridges connect algebra to text: 凶×basin (core, p=0.0002) and 吉×生体 (shell, p=0.007, basin-independent). Both encode process not state. Bridge orthogonality is proven at the perturbation level (atlas workflow).

The atlas establishes the coordinate system as informationally complete (zero residual: H(hexagram | full profile) = 0.0 bits). Combined with zero free parameters — now fully proven (R32: the 0.50-bit cosmological choice is forced by conjunction of textual bridge + cycle attractor semantics, 0/32 alternatives viable) — this means: the encoding is complete in both directions, and uniquely determined. The atlas is the terminal structural computation — remaining questions are queries against it, not new constructions.

The atlas further establishes: the {2,2,2,1,1} partition is the single organizing principle from which all structural properties derive; the torus is the frame (epistemology — when you can see what) while the Z₅ diagonal quotient is where meaning lives (ontology — what things signify); and the core is time-independent (orthogonality wall) while the shell is time-modulated.

**The 梅花 atlas extends this:** The 384-state expansion (64 hexagrams × 6 動爻) projects the hexagram space into a directed, depth-stratified evaluation. Two independent information channels (text ↔ present state, arc ↔ trajectory) operate through the same Z₅×Z₅ geometry but with different axes (positional vs relational). The 體/用 cut converts static algebra into directed reading — "temporal" in 梅花 is structural depth rendered as narrative.

**The semantic map completes the empirical side:** Bottom-up characterization of all textual layers confirms the residual is thick (89% for 爻辭). The text-algebra interface is bounded: two distributional bridges (marker placement) plus shared positional hierarchy (from the 3+3 factorization). 89% of textual semantic content is orthogonal to algebraic structure. The commentary tradition (小象/彖傳/大象) sees binary structure (Z₂) and positional hierarchy but not the pentadic algebra (Z₅) — the 五行 formalization is a separate layer, not a reading of the earlier tradition.

**The unification program (R43-R59) completes the number-theoretic foundation:** The (n,p) = (3,5) uniqueness is now proven as the **Uniqueness Theorem** — the orbit count of complement-respecting surjections with three-type coexistence equals ((p−3)/2)! × 2^{2^{n−1}−1−n}, which is 1 if and only if (n,p) = (3,5). Two independent arithmetic conditions force this: p = 5 (trivial assignment moduli, the smallest prime with two independent cycles) and n = 3 (trivial orientation moduli, from the Mersenne-type equation 2^{n−1} = n+1 having unique non-degenerate solution n = 3). The selection chain simplifies to 240→192→96→1 under the full symmetry Stab(111) × Aut(Z₅), which acts regularly on Orbit C. The former "0.5-bit" is presentational — it appears only when fixing the 互 kernel line (an external datum), not from any structural freedom. At (4,13), the orbit count is 960 = 5! × 2³ (verified exhaustively), confirming the formula and proving the uniqueness is specific to (3,5). The object is an isolated rigid point in a doubly-exponentially growing moduli space. See unification/synthesis-3.md for the complete account (supersedes synthesis-1.md and synthesis-2.md).

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

**Status: RESOLVED → semantic-map workflow**

Bottom-up characterization of all textual layers completed. Key findings:

1. **Thick residual (89% for 爻辭, ≥64% for 卦辭).** The texts have rich independent structure that algebra cannot predict. The two bridges (凶×basin, 吉×生体) are distributional constraints on marker placement, not determinants of semantic content. No hidden systematic text-algebra alignment was found by exhaustive bottom-up search.

2. **Positional dominance.** The 384 爻辭 organize by line position, not by parent hexagram. k=3 clusters cut across hexagrams (χ²=37.2, p=0.0001). The dominant textual structure is positional — "64 instances of 6 roles" rather than "6 lines per 64 situations."

3. **小象 vocabulary encodes the algebraic 3-layer hierarchy (χ²=125, p=5×10⁻²⁶).** Three vocabulary groups {上+下+初, 中, 位+當} map to the three algebraic layers {outer, interface, core}. Both tradition and algebra read the same hierarchy forced by the 3+3 factorization — not convergent recognition but two descriptions of one structural fact.

4. **Commentary layers are non-algebraic.** 大象: imagistic (no 五行 vocabulary). 彖傳: binary-structural (Z₂, not Z₅). 小象: positional (no algebraic signal beyond position). The 五行 formalization is a separate layer imposed later.

5. **Both bridges survive position control (CMH).** 凶×basin: OR=4.25, p=0.00002 after stratifying by position. 吉×生体: OR=2.19, p=0.004. The two bridges are genuinely independent of position — three layers of text-algebra contact: position, basin (core), 体用 (shell).

**Sub-questions resolved:**
- The text corpus has its own semantic structure that algebra is largely orthogonal to (thick residual)
- The 象傳/彖傳 do NOT encode 五行 relations — they use independent imagery (大象) and binary structural vocabulary (彖傳)
- Line position carries semantic weight independent of algebra — it IS the dominant organizing principle of the text corpus
- I.4 imagery taxonomy deferred — unlikely to shift residual thickness

**Full findings:** `semantic-map/findings.md`

---

## 5. Temporal × semantic interaction

**Status: open, atlas-enabled, lower priority**

The atlas establishes: valence lives on the Z₅ quotient (p=0.75 spatial residual), and temporal coverage varies by season. Uncomputed: does the 凶×basin signal strength change when the basin's dominant element is 旺 (seasonally strong) vs 死 (seasonally weak)?

This requires crossing temporal.json (60 states) with valence_torus.json (per-cell rates). A small computation but potentially revealing: if the signal is purely algebraic (structural position in Z₂⁶), temporal context shouldn't modulate it. If it does modulate, the bridge has a temporal component not captured by the static atlas.

---

## 6. 火珠林 operational atlas

**Status: RESOLVED → atlas-hzl workflow**

See atlas-hzl/findings.md for complete results. Summary: 11 data files, 13 scripts, 6 sections (static profiles, seasonal activation, 日辰 layer, 動爻 layer, network reading, domain bindings). Key structural results: shell⊥core confirmed at temporal level (MI=0), anti-resonance theorem (fc=0 iff missing pair forms 生 pair), {4,2,2,2,2} cascade across all layers, 游魂 universal 飛伏 completeness, 用神 evaluation protocol formalized as 7-step algorithm. 31 domains extracted (26 standard + 5 special), classified by 2D taxonomy (layer × mode).

---

## 7. Three-register temporal architecture

**Status: new, from semantic map**

The semantic map revealed three historical layers operating in three different registers:

| Layer | Period | Register | What it sees |
|-------|--------|----------|-------------|
| 爻辭 | ~9th c. BC | Situational/imagistic | Positions, processes |
| 小象/彖傳 | ~5th-3rd c. BC | Binary-structural | Yang/yin, centrality, correspondence |
| 五行 formalization | ~1st c. BC | Pentadic-algebraic | Elements, basins, surface relations |

These registers suggestively map to the three primes of PG(2,2): prime 2 (binary polarity), prime 3 (positional hierarchy), prime 5 (cyclic dynamics). The commentary tradition sees primes 2 and 3 but not prime 5. The 五行 formalization sees prime 5.

**Open question:** Is the register → prime mapping coincidence or structure? Would need historical analysis of when specific structural concepts first appear in the commentary tradition to test whether the temporal sequence follows the prime ordering.

**Epistemic status:** Pattern observation (suggestive), not measured.

---

## 8. 彖傳 as anomaly detector

**Status: new, from semantic map**

The 彖傳 comments on what is noteworthy/unusual, not what is dominant. Kun basin (predominantly yin) has the highest 剛/柔 ratio (2.14) — more 剛 references where 剛 is rare. This is the same information-theoretic stance as the depth gradient: information concentrates at boundaries (depth-1 peak in 凶, not at attractors).

**Open question:** Is this anomaly-detection stance systematic across the 彖傳, or just an artifact of the 剛/柔 count? Would need fine-grained analysis: for each hexagram, does the 彖傳 preferentially comment on the structurally unusual lines?

**Epistemic status:** Single observation (measured), generalization (conjectured).

---

## 9. General rank formula for 互_n

**Status: conjectured, from unification Phase 3**

For the nuclear extraction 互_n on F₂^{2n}: rank(M^k) = max(2, 2n−2k). Convergence to rank-2 stable image in n−1 steps. Same 4-element attractor at all n: {all-0, all-1, alt-A, alt-B}.

Verified at n=3 (rank 6→4→2→2) and n=4 (rank 8→6→4→2→2). General proof would follow from the factored-basis structure (shift + shear / shift + projection), which is established for general n but the rank computation is verified only at n=3,4. (unification/transitivity_probe.py)

---

## 10. Is the residual group action free for all (n, p)?

**Status: conjectured, from unification Phase 3**

The action of (F₂)^{n-1} × Aut(Z_p) on within-type-distribution surjections is free at both (3,5) and (4,13). If free in general, the orbit count formula Orbits = ((p−3)/2)! × 2^{2^{n−1}−1−n} is exact. Freeness at (3,5) follows from regularity (|group| = |set| = 16). Freeness at (4,13) verified exhaustively (all 960 orbits have size 96). General proof not attempted. (unification/within_type_orbits.py)

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

**Updated by semantic map:** Both bridges survive position control (CMH: 凶×basin p=0.00002, 吉×生体 p=0.004). Residual thickness confirmed thick (89%). Commentary layers non-algebraic. (semantic-map/findings.md)

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

**Updated by semantic map:** Survives position control (CMH OR=2.19, p=0.004). Effect unchanged by stratification — genuinely independent of line position. (semantic-map/findings.md F7)

### R12. 凶 content at depth boundary
**NULL — distributional not thematic.** Depth-1 hexagrams carry more 凶 (19.4% vs 12.8%), but 凶 text content doesn't systematically differ by depth. No word category reaches significance (best: threshold p=0.069). (synthesis Probe 7)

**Confirmed by semantic map:** 89% of 爻辭 embedding variance is text-intrinsic. The bridges are distributional (WHERE markers appear), not thematic (WHAT texts say). (semantic-map/findings.md F6)

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

### R33. Why 5 elements (deep)
**FORCED BY NUMBER THEORY.** Two independent non-degenerate cycles on Z_k require: stride-1 and stride-2 generate the full group (k prime), and stride-2 ≠ stride-1 or its inverse (fails for k=2,3). The smallest viable prime is k=5. (deep/number-structure.md, deep/04_dimensional_forcing.py)

### R34. Why 3 lines per trigram (deep)
**FORCED BY PIGEONHOLE.** Dimensional forcing theorem: n=3 is the unique dimension where every surjective complement=negation partition Z₂ⁿ → Z₅ has singleton fibers. For n≤2, surjection impossible. For n≥4, singleton-free surjections exist. The singleton bridge (Fire/Water injection points) is structurally guaranteed if and only if n=3. (deep/04_dimensional_forcing.py)

### R35. Why 6 lines per hexagram (deep)
**FORCED BY 互 DYNAMICS.** n=3 (6 lines) is the largest dimension where 互² = identity on all eventual cycles. At n=4 (8 lines), 3-cycles appear, breaking the 2-cycle attractor structure. (deep/04_dimensional_forcing.py)

### R36. 先天 arrangement uniquely forced (deep)
**UNIQUE Z₂ OPTIMUM.** Z₂ composite score 6/6 (complement_diameter=4/4, reversal_reflection=2/2). Maximum achievable by any cardinal-aligned arrangement is 3/6. Gap of 3 proves Z₂ geometric coherence and He Tu element alignment are fundamentally incompatible. (deep/02_arrangements.py)

### R37. 後天 arrangement uniquely forced (deep)
**UNIQUE 2×3×5 TRIPLE JUNCTION.** Among 96 cardinal-aligned arrangements: prime-5 constraints (monotone + elem_pair_coherent) → 8 survivors (exact Z₂³ product, Z₅-orthogonal); prime-2 (yy_balance) → 2; prime-3 (sons_yang_half) → 1 = 後天. Minimal uniqueness set verified. (deep/02_arrangements.py, deep/03_prime_decomposition.py)

### R38. KW pairing uniquely forced (deep)
**UNIQUE BASIN-PRESERVATION MAXIMUM.** Among 3^12 = 531,441 V₄-compatible pairings, the KW pairing (reversal + complement fallback for palindromes) uniquely maximizes same-basin pairs (28/32). Theorem: reversal preserves all basins; complement and comp∘rev swap Kun↔Qian. (deep/08_pairing_torus.py)

### R39. V₄-equivariance of 互 (deep)
**PROVEN.** All three V₄ involutions (complement, reversal, comp∘rev) commute with the nuclear transform 互. 20 V₄ orbits on 64 hexagrams: 8 size-2 (4 palindrome pairs + 4 anti-palindrome pairs) + 12 size-4. (deep/06_v4_symmetry.py)

### R40. Line hierarchy encoded in yaoci (deep)
**MEASURED — p < 0.001.** Algebraic role (outer core / interface / shell) predicts 吉/凶 rates: 吉 × role χ²=15.1, p=0.0005. Line 5 ruler effect OR=2.15, p=0.007. 生体 × line 5 = 75% 吉 (system peak). 体/用 and 世 line are NOT encoded (p > 0.2) — operational overlays absent from ancient text. (deep/09_line_valuations.py)

**Extended by semantic map:** Positional hierarchy is the dominant organizing principle of the entire 爻辭 corpus (not just valence markers). k=3 embedding clusters separate by position (χ²=37.2, p=0.0001). L2↔L5 closest centroid pair (cosine=0.013). 小象 vocabulary independently confirms the same 3-layer hierarchy (χ²=125, p=5×10⁻²⁶). (semantic-map/findings.md F3, F5, F8)

### R41. KW sequence basin clustering (deep)
**MEASURED — p < 0.001.** Same-basin transitions: 60% vs 37% expected. 上經/下經 = palindromic/non-palindromic pure partition. All other sequential metrics null (Hamming, element continuity, 先天 correlation). (deep/05_king_wen_sequence.py)

### R42. Two Z₅ incommensurability (deep)
**PROVEN.** The 生-cycle Z₅ and He Tu Z₅ are incommensurable as algebras (non-affine conjugation γ) and as metric spaces (γ not distance-preserving). Connected through 後天 compass arrangement, not through algebraic structure. (deep/01_assignment_test.py)

### R43. (n,p) singleton-forcing landscape (unification)
**PROVEN.** Singleton forcing in complement-respecting surjections Z₂ⁿ → Z_p occurs iff p > 2^(n-1). The family is infinite (Bertrand's postulate guarantees primes in every window). Verified exhaustively for 27 (n,p) cases across n ∈ {3,4,5,6}. (unification/np_landscape.py)

### R44. (3,5) uniqueness — triple resonance (unification)
**PROVEN (Phase 2); SUPERSEDED BY R55 (Phase 3).** Phase 2 established (3,5) as the unique (n,p) satisfying singleton forcing + three-type partition + Fano geometry. Phase 3 proved the stronger result: (3,5) is the unique rigid point where the orbit count = 1, from two independent arithmetic conditions (R55). The triple resonance is a corollary. (unification/np_landscape.py, unification/synthesis-3.md §IV)

### R45. Shape count formula (unification)
**PROVEN.** In the singleton-forcing regime, # partition shapes = Σ_{k=0}^{E} p(k), where E = 2^(n-1) − (p+1)/2 is the excess and p(k) is the integer partition function. Verified for all 16 forcing cases. Generating function: (1/(1-x)) × Π_{k≥1} 1/(1-x^k). (unification/np_landscape.py)

### R46. Surjection count ratio at E=1 (unification)
**PROVEN.** At E=1 (p = 2^n − 3), the ratio of spread to concentrated surjections is exactly N_A/N_B = p − 1. Verified at (3,5): 192/48 = 4; (4,13): 12:1; (5,29): 28:1; (6,61): 60:1. (unification/orbit_c_nuclear.py)

### R47. Selection chain (unification)
**PROVEN — updated by Phase 3.** Under full symmetry Stab(111) × Aut(Z₅), the selection chain is 240→192→96→**1**. The intermediate steps 96→16→4→2 from Phase 2 were artifacts of prematurely fixing the 互 kernel line H and the Aut(Z₅) quotient. At the abstract level, Orbit C is a single orbit (regular action, stabilizer trivial). The "0.5-bit" is presentational: it appears only when fixing H, breaking S₃→Z₂. (unification/cc_identity.py, unification/synthesis-3.md §III)

### R48. Hexagram Z₅ Reduction (unification)
**PROVEN.** All hexagram-level 五行 quantities (relation type d, 互 transition, complement action) are determined by the trigram-level surjection f and the F₂-linear (lower, upper) decomposition. The hexagram level adds no additional Z₅ data. d(h) = f(upper) − f(lower) mod 5. (unification/hexagram_wuxing.py)

### R49. Complement theorem on hexagrams (unification)
**PROVEN.** d(~h) = −d(h) mod 5. Complement maps 同→同, 生↔被生, 克↔被克. Follows directly from f(~x) = −f(x). Reversal does NOT descend to Z₅: d(h̄) = −d(h) in only 24/64 cases (reversal splits doubleton fibers). (unification/hexagram_wuxing.py)

### R50. 互 transition eigenstructure (unification)
**VERIFIED.** The 5×5 Markov transition matrix T[d→d'] has spectrum {1, 1/6, −1/13, (157 ± i√75815)/1092}. Spectral gap 1 − √(23/273) ≈ 0.71. Stationary distribution π = (28/87, 8/145, 247/870, 247/870, 8/145) concentrates 89% on {同,克,被克}. Antisymmetric block is upper triangular: zero flow from stride-2 to stride-1 (克 never produces 生 under 互). Mixing in 3-5 iterations confirms cascade depth. (unification/eigenstructure.py)

### R51. Exact P-coset alignment formula (unification)
**PROVEN.** Each Z₅ fiber is P-homogeneous: {Wood, Fire, Water} all P-odd; {Earth, Metal} all P-even. The P-even fraction F(d) is an exact convolution: F(同)=1, F(生)=F(被生)=2/3, F(克)=F(被克)=1/13. Not an approximation — deterministic from fiber partition {2,2,2,1,1} and P-parity structure. (unification/eigenstructure.py)

### R52. 0.5-bit — presentational, not structural (unification)
**RESOLVED — PRESENTATIONAL.** *Updated from Phase 2 characterization.* Phase 2 identified the 0.5-bit as an irreducible boundary between algebra and cosmology. Phase 3 proved this wrong: under the full symmetry Stab(111) × Aut(Z₅), all 96 Orbit-C surjections form 1 orbit (regular action). The 0.5-bit appears ONLY when fixing the 互 kernel line H (an external datum), which breaks Stab(111) ≅ S₄ down to Stab(H)∩Stab(111) ≅ D₄. Under D₄ × Aut(Z₅): 2 orbits on the 16 IC+Alt type pair. The "cosmological choice" is a coordinate choice, not a structural one. (unification/cc_identity.py, unification/synthesis-3.md §III)

### R53. CC/AS hypothesis closed (unification Phase 3)
**NEGATIVE.** The Z₅-difference relation on F₂³ does NOT produce an association scheme (375/378 intersection matrix pairs non-commuting). The coherent closure has 28 classes = the orbit partition of the fiber automorphism group (Z₂)³. This is the generic answer for ANY function with fiber shape {2,2,2,1,1}, not specific to the 五行 map. (unification/cc_identity.py)

### R54. Walsh-Hadamard spectrum automatic (unification Phase 3)
**CHARACTERIZED.** W_f(ω) lives in Q(√5). W(000) = −1/φ (negative reciprocal of golden ratio). Real for even-weight ω, imaginary for odd-weight ω (complement equivariance). Spectral power: P-line 60%, Q-line 37%, H-line 3%. All determined by fiber sizes + singleton placement + ζ₅ arithmetic — NOT by f's detailed structure. At (n,p), the field would be Q(cos 2π/p) by the same mechanism. (unification/cc_identity.py)

### R55. Uniqueness Theorem (unification Phase 3)
**PROVEN — the central result.** Among all (n,p) with p = 2ⁿ−3 (E=1 family), the orbit count of Orbit-C surjections within a fixed type distribution under (F₂)^{n−1} × Aut(Z_p) is:

> **Orbits(n,p) = ((p−3)/2)! × 2^{2^{n−1}−1−n}**

This equals 1 if and only if (n,p) = (3,5).

Two independent conditions:
1. ((p−3)/2)! = 1 ⟺ p = 5 (smallest prime with two independent cycles)
2. 2^{2^{n−1}−1−n} = 1 ⟺ 2^{n−1} = n+1 ⟺ n = 3 (unique RM-filling dimension)

Verified: (3,5) → 1 orbit; (4,13) → 960 = 5!×2³; (5,29) → ~6.4×10¹². (unification/within_type_orbits.py, unification/synthesis-3.md §IV)

### R56. Orbit C regularity (unification Phase 3)
**PROVEN.** Stab(111) × Aut(Z₅) acts regularly (free + transitive) on the 96 Orbit-C surjections at (3,5). Proof: S₃ transitive on 6 type patterns × V₄ × Aut(Z₅) regular on 16 within-pattern surjections. 6 × 16 = 96, stabilizer trivial. (unification/transitivity_probe.py, unification/synthesis-3.md §III)

### R57. Reed-Muller code fills orientation space iff n=3 (unification Phase 3)
**PROVEN.** The kernel swap patterns in Stab(1ⁿ) generate the first-order Reed-Muller code RM(1,n−1) inside (Z₂)^{2^{n−1}−1}. The orientation quotient has 2^{2^{n−1}−1−n} cosets. This equals 1 iff dim(RM) = dim(orientation space), i.e., n = 2^{n−1}−1, i.e., 2^{n−1} = n+1. Solutions: n=1 (degenerate), n=3 (unique non-degenerate). At n=4: RM(1,3) has dimension 4 inside (Z₂)⁷ → 8 orientation orbits. (unification/within_type_orbits.py, unification/synthesis-3.md §VI)

### R58. Type-distribution transitivity generalizes (unification Phase 3)
**PROVEN at (3,5) and (4,13).** The Orbit-C-analog type distributions form 1 orbit under Stab(1ⁿ) at both (3,5) (6 distributions, 1 orbit) and (4,13) (42 distributions, 1 orbit). The 7 non-Frame pairs at n=4 form PG(2,F₂) = Fano plane; GL(3,F₂) acts as its full automorphism group. Conjectured to hold for all n ≥ 3 (follows from 2-transitivity of GL(n−1,F₂) on PG(n−2,F₂)). (unification/transitivity_probe.py, unification/synthesis-3.md §II)

### R59. 互 transition matrix: type-invariant at (3,5), complete invariant at (4,13) (unification Phase 3)
**VERIFIED.** At (3,5), all 16 surjections within a type distribution produce the SAME 5×5 transition matrix T. At (4,13), every surjection produces a DISTINCT 13×13 T (verified for first 200 surjections: 200 distinct T matrices). The transition from constant to distinguishing occurs because p×p matrix resolution (25 vs 169 entries) exceeds the moduli at (4,13) but not at (3,5). (unification/within_type_orbits.py)

### R60. 火珠林 operational atlas (atlas-hzl)
**COMPLETE.** The shell projection operationalized across 6 sections:
- §I: 64 static profiles with 納甲/六親/飛伏/納音/卦身. 世/應 asymmetry (妻財+官鬼=59% at 世). 游魂=universal completeness (8/8). Earth universality proven by pigeonhole.
- §II: 320 seasonal states (64×5). 2/5 ceiling confirmed. Anti-resonance: fc=0 ⟺ missing pair is a 生 pair (10/320 states). 6 immune hexagrams (all Fire/Metal missing克 pair).
- §III: 768 日辰 interactions. Perfect balance theorem (6/6/6 per hexagram). Shell⊥core MI=0 (constructive proof: 13 branch-sharing groups with different 互). 旬空 uniform (1.00 void lines/state). Three-layer architecture documented (天干/地支/納音).
- §IV: 384 transformations. All 25 化爻 types realized. 官鬼 target deficit (55/384=14.3%, root cause: {4,2,2,2,2}). Basin crossing binary by line (L3/L4=100%, others=0%).
- §V: 飛伏 diagnostic table (9 cases, 財/鬼 only = 80% coverage by design). 獨發 patterns (兄弟=zero positive domains). 用神 7-step protocol formalized with data file mapping.
- §VI: 31 domains → 8 structural clusters + 5 special protocols classified by 2D taxonomy (layer×mode). 卦身 conditional sixth variable (41% on-line).
Central synthesis: tangent vector (梅花) vs local observable (火珠林). Two systems exhaust the hexagram's information through orthogonal temporal channels. (atlas-hzl/findings.md)
