# Open Questions

## Central thread

Structure → incompleteness → curvature → specificity → meaning.

The algebraic characterization is complete at this resolution. Z₂⁶ with shell/core projections, 五行 coordinates, basin convergence, palace walks, 六親 near-bijection. Two divination systems exhaust the hexagram's information through the only two primitive projections available (proven algebraically, confirmed historically). Orthogonality between 納甲 and core is confirmed; leakage at the element level is quantified (~7%, which is 2.5/6.0 = 42% at the bit level, collapsing to near-zero through the 五行 quotient). Temporal curvature is characterized: three sources, one softened by 日辰 to a 1/5 residual (proven as theorem). Two bridges connect algebra to text: 凶×basin (core) and 吉×生体 (shell), both encoding process not state. Bridge orthogonality is proven at the perturbation level (atlas workflow).

The atlas establishes the coordinate system as informationally complete (zero residual: H(hexagram | full profile) = 0.0 bits). Combined with zero free parameters, this means: the encoding is complete in both directions, and uniquely determined. The atlas is the terminal structural computation — remaining questions are queries against it, not new constructions.

The atlas further establishes: the {2,2,2,1,1} partition is the single organizing principle from which all structural properties derive; the torus is the frame (epistemology — when you can see what) while the Z₅ diagonal quotient is where meaning lives (ontology — what things signify); and the core is time-independent (orthogonality wall) while the shell is time-modulated.

---

## 1. Formal H¹ computation

**Status: open, lower priority**

All three curvature sources are quantified (用神 projection: 45/20/35; seasonal ceiling: 2/5→4/5; palace holes: 16:32:16). The qualitative picture is clear and the orthogonality wall limits the interpretive reach of H¹ (the shell-layer presheaf cannot see core-layer dynamics).

A formal computation could test whether curvature varies with basin, palace rank, or 互 depth. But the expected payoff is a numerical refinement of an already-clear structural picture, not a new insight.

**Atlas-informed refinement:** The constraint analysis shows basin ⊥ rank (MI=0.000), which means H¹ cannot vary jointly with basin and rank — they contribute independently. This further limits the degrees of freedom available for curvature variation.

---

## 2. Is the 五行 assignment necessary or arbitrary?

**Status: open, computable**

The atlas proves every structural property traces to the specific {2,2,2,1,1} partition of 8 trigrams into 5 elements. The wuxing workflow decomposed this assignment into 1.75 bits algebraic + 0.50 bits cosmological:

**What's forced (1.75 bits):**
- Parity bit (b₀⊕b₁, 1.00 bit): splits even-parity {Kun,Gen,Dui,Qian} from odd-parity {Kan,Xun,Zhen,Li}
- Bit b₀ within even class (0.75 bit): separates Earth{Kun,Gen} from Metal{Dui,Qian}

**What's chosen (0.50 bits):**
Within odd-parity {Kan,Li,Zhen,Xun}, which form 2 complement pairs: {Kan,Li} and {Zhen,Xun}. Tradition keeps {Zhen,Xun}=Wood together, splits {Kan,Li} into Fire/Water singletons. The alternative: keep {Kan,Li} together, split {Zhen,Xun}. Only 3 possible choices (which complement pair to keep).

**The question:** Is the 0.50-bit cosmological choice forced by a structural criterion?

**Computable test — 3 candidate assignments:**

The even-parity partition is forced. Only the odd-parity coset has freedom. The 3 alternatives:

| Choice | Kept pair | Split pair | Traditional? |
|--------|-----------|------------|-------------|
| A | {Zhen,Xun}=Wood | {Kan}=Water, {Li}=Fire | Yes |
| B | {Kan,Li}=? | {Zhen}=?, {Xun}=? | No |
| C | One from each: {Kan,Zhen}, {Li,Xun} or similar | — | No (breaks complement structure) |

For each of the 3 (or enumerate all valid alternatives), run the full atlas machinery and measure:

1. **Zero-residual property** — does the full 五行 profile still uniquely identify all 64 hexagrams? If only the traditional assignment achieves zero residual, it's forced.
2. **六親 injectivity** — traditional gets 59/64 unique 六親 words. Do alternatives score higher or lower?
3. **凶×basin correlation** — the p=0.0002 bridge. Does it survive under alternative assignments, or is it an artifact of this specific partition?
4. **吉×生体 correlation** — p=0.007. Same test.
5. **Complement closure** — Wood is the *only* element closed under complement (Zhen↔Xun are complements). Requiring exactly one complement-closed element: does this uniquely force the partition?
6. **Anti-phase breathing** — does 生/克 alternation at nuclear transitions hold for alternative assignments?
7. **互 well-definedness on Z₅×Z₅** — the atlas found 17/25 cells multi-valued. Does an alternative assignment improve or worsen this?
8. **Perturbation onion** — does the 4-layer structure survive?

**The complement closure test is the fastest discriminator.** On Z₂³, complement pairs are: (Kun,Qian), (Gen,Dui), (Kan,Li), (Zhen,Xun). Parity + b₀ already separate Kun/Qian and Gen/Dui into different elements. Within the odd coset, only {Zhen,Xun} and {Kan,Li} are complement pairs. Only 3 cases to check (keep Zhen+Xun, keep Kan+Li, keep neither).

If the traditional assignment uniquely maximizes across these metrics — or uniquely satisfies a subset — then the 0.50 cosmological bits are forced, and the entire 五行 assignment is necessary with zero free parameters.

**Known partial evidence:**
- Later Heaven coherence: traditional partition ranks #5 of 420 possible {2,2,2,1,1} partitions (wuxing/03). But this is partially circular (Later Heaven is itself tradition).
- Wood's Hamming-3 distance (Zhen↔Xun are antipodal on Z₂³) is the root cause of 互 non-well-definedness on the torus. Alternative pair {Kan,Li} has Hamming distance 2. Would keeping {Kan,Li} together reduce torus indeterminacy?

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
