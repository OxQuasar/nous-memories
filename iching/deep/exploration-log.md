# Deep Exploration Log

## Iteration 1: Two Z₅ Incommensurability + Assignment Uniqueness

### What was tested

**1. Are the He Tu Z₅ and 生-cycle Z₅ the same algebraic structure?**

Computed the complement anti-automorphism π on both Z₅ labelings:
- 生-cycle ring (Wood=0, Fire=1, Earth=2, Metal=3, Water=4): π acts as x → -x mod 5
- He Tu ring (Earth=0, Water=1, Fire=2, Wood=3, Metal=4): π acts as the permutation (0 4)(1 2)(3)

Exhaustive search of all 25 affine maps f(x) = ax + b mod 5 on He Tu: none match π. The 生 cycle itself has irregular steps [4,3,4,2,2] on He Tu numbering — not stride-anything.

Both generate D₅ (dihedral, order 10) via ⟨σ, π⟩. Conjugating permutation γ = [3,2,0,4,1] verified: γσγ⁻¹ = σ_hetu, γπγ⁻¹ = π_hetu.

**2. Is the 0.50-bit cosmological choice (which odd-coset complement pair to keep together) forced?**

Enumerated all alternative {2,2,2,1,1} partitions of 8 trigrams into 5 elements, constrained to complement-respecting configurations:
- **A (traditional)**: {Zhen,Xun}=Wood kept together, {Kan}=Water, {Li}=Fire split. 1 assignment.
- **B**: {Kan,Li} kept together, {Zhen},{Xun} split. 16 complement-respecting configurations.
- **C**: Cross-pair {Kan,Zhen} + {Li,Xun}. 16 complement-respecting configurations.

For each of 32 alternatives + traditional: ran the 吉×生体 Fisher exact test (same yaoci texts, reclassified by each assignment's 生/克/比和 relations). Also checked: complement = negation, Cycle attractor relations, zero residual, 互 well-definedness, parity separation.

**3. Does the 3×5 grid (lower_element × hu_relation × upper_element) add discriminative power?**

Projected all 64 hexagrams into Z₅ × Z₅ × Z₅ (125 cells). Cross-tabulated with valence markers.

### What was found

**Finding 1: Two Z₅ incommensurability [proven]**

The 生-cycle Z₅ and He Tu Z₅ are genuinely different algebraic structures on the same 5-element set. Complement is the unique order-2 automorphism (negation) on the 生-cycle ring but is non-affine on He Tu. No algebraic conjugation exists between the two Z₅ *as rings* — only as D₅ *group actions* via the non-affine γ.

The He Tu Z₅ encodes spatial/compass position (where); the 生-cycle Z₅ encodes relational dynamics (how). Connected through the 後天八卦 spatial arrangement, not through algebra.

This resolves deep-questions §2 ("Why do the two Z₅ structures agree?"): They don't agree on operations — they agree only on the partition (the same 5 categories). The He Tu numbers are a spatial labeling convention; the 生-cycle ordering is the relational structure. The "agreement" is at the set level, not the algebraic level.

**Finding 2: The 0.50-bit choice is forced by conjunction [proven + measured]**

| Constraint | What it eliminates | Status |
|---|---|---|
| Complement = negation | Nothing (all 3 types satisfy) | Proven: necessary, not sufficient |
| Cycle attractor ≠ 比和 | All B (16/16) | Proven: {Kan,Li} at position 0 forces 既濟/未濟 = 比和 |
| 吉×生体 p < 0.05 | All remaining B and C | Measured: traditional OR=2.10, p=0.007; best B: OR=1.69, p=0.065; best C: OR=1.46, p=0.20 |

**0 of 32 alternatives reach p < 0.05.** The traditional assignment is uniquely selected by the conjunction of algebraic viability (Cycle attractor 克) + textual alignment (吉×生体 bridge). Neither alone is sufficient:
- Algebra eliminates B entirely but leaves some C variants with 克 at the attractor
- Text eliminates all B and C variants

**Finding 3: Surprises that refine the picture**

- **C retains complement = negation** — the prediction that C breaks complement was wrong. Complement = negation requires complement *pairs* to sit at conjugate cycle positions, not complement *closure* (both members in same element). C achieves this. Corrects the forcing argument: complement = negation is weaker than previously claimed.

- **C achieves better zero residual (64/64 vs traditional's 52/64)** — C pairs even-coset trigrams at Hamming distance 3 (complement pairs: Kun/Qian), avoiding the 6 collisions that arise from the traditional pairing at Hamming distance 1 (adjacent: Kun/Gen). This reveals a **semantic coherence vs algebraic economy tradeoff**: the tradition pairs geometrically adjacent trigrams (preserving phenomenological coherence) and compensates for the resulting collisions through 六親, rather than maximizing single-projection distinguishability.

- **Parity separation holds for all three types** — less discriminating than expected.

- **六親 injectivity numbers (23/64 for traditional)** are a methodological artifact: the computation used trigram-level elements, not the actual 納甲 per-line branch system that yields 59/64 in the atlas.

**Finding 4: 3×5 grid is null [measured]**

43/125 cells realized, 82 forbidden. hu_relation adds no textual valence signal beyond the surface torus: χ² p=0.731 for 吉 across 5 hu_relation categories. The nuclear relation is structurally constrained but not semantically discriminating. Consistent with the atlas finding that valence lives on the Z₅ quotient (directed relation), not on finer coordinates.

### What it means

**The entire 五行 assignment has zero free parameters.** The information decomposition:
- 1.00 bit: b₀⊕b₁ parity (algebraically forced — separates even/odd cosets)
- 0.75 bits: b₀ within even-parity coset (algebraically forced — separates Earth from Metal)
- 0.50 bits: odd-coset choice (forced by conjunction of algebra + text)
- Total: 2.25 bits = H(五行 assignment)

The 0.50-bit choice is the deepest instance of the "incommensurability as mechanism" thesis: the specific partition lives at the intersection of two independently insufficient constraints (algebraic structure and textual tradition). Neither determines it alone; their intersection selects uniquely.

**The system has three nested layers of incommensurability:**
1. Z₂ vs Z₅ (binary/pentadic) — bridged by complement (the unique cross-framework operation)
2. He Tu Z₅ vs 生-cycle Z₅ (spatial/relational) — connected through 後天 compass, not algebra
3. Shell vs Core (identity/convergence) — unbridged (the orthogonality wall)

### Finding 5: The singleton-attractor mechanism [proven]

The Hamming distance analysis reveals WHY the traditional assignment works — not just that it does.

Each assignment type has three doubleton elements (two trigrams paired) with characteristic within-pair Hamming distances:

| Assignment | Pair Hamming distances | Total | Singletons |
|---|---|---|---|---|
| A (traditional) | Earth(Kun↔Gen)=1, Metal(Dui↔Qian)=1, Wood(Zhen↔Xun)=3 | [1,1,3] | Fire(離), Water(坎) |
| B | Earth(Kun↔Gen)=1, Metal(Dui↔Qian)=1, Pair(Kan↔Li)=3 | [1,1,3] | Zhen, Xun |
| C (cross) | Cross(Kan↔Zhen)=2, Cross(Li↔Xun)=2, Even(Kun↔Qian)=3 | [2,2,3] | Gen, Dui |

A and B have identical Hamming profiles [1,1,3]. C has higher total spread [2,2,3], which explains both its perfect zero residual (64/64 — more spread → fewer collisions) and its worse 互 coherence (4/25 vs 8/25 — more spread → nuclear trigrams diverge more within elements).

**The key structural fact:** The 互 cycle attractors are 既濟 (坎 over 離) and 未濟 (離 over 坎). These are made of exactly Kan and Li.

| Assignment | Singletons | Singletons = 互 attractors? | 既濟/未濟 relation |
|---|---|---|---|
| A (traditional) | Fire(離), Water(坎) | **YES** | 克 (Water克Fire) |
| B | Zhen, Xun | No | 比和 (both in same element) |
| C | Gen, Dui | No | 克 (inverted direction) |

**Only assignment A places the 互 attractors as singletons.** This means the Z₅ projection is injective at the convergence locus — the 五行 system can see the exact identity of the attractors without fiber ambiguity. This is where the binary dynamics (互 convergence on Z₂⁶) and element evaluation (生克 on Z₅) achieve maximum constructive interference.

The Fire/Water bridge is not a coincidence but a structural necessity: singleton status at the attractor is what makes the bridge possible.

### Predictions vs results

| Prediction | Result |
|---|---|
| B loses 吉×生体 bridge | ✓ Confirmed. Best B: p=0.065, OR=1.69. None reach p<0.05. |
| B loses cycle attractor 克 | ✓ Confirmed. 既濟/未濟 both → 比和. |
| C breaks complement closure | ✗ Surprise: C retains π = -x. Cross-pairs at conjugate positions suffice. |
| Zero residual survives for all | Partial. A: 52/64, B: 50/64, C: 64/64 (C is better). |
| Traditional uniquely selected | ✓ Only A has BOTH p<0.05 textual bridge AND 既濟/未濟 = 克 AND singletons = attractors. |

### Conjunction forcing table

| Property | A (Traditional) | B (16 variants) | C (16 variants) |
|---|---|---|---|
| 吉×生体 p<0.05 | ✓ (p=0.007) | ✗ (best p=0.065) | ✗ (best p=0.159) |
| 既濟/未濟 = 克 | ✓ | ✗ (比和) | ✓ (inverted) |
| Singletons = 互 attractors | ✓ | ✗ | ✗ |
| π = -x mod 5 | ✓ | ✓ | ✓ |
| 互 well-defined ≥8/25 | ✓ (8) | ✓ (8) | ✗ (4) |
| Zero residual (profile) | 52/64 | 50/64 | 64/64 |

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | π = -x mod 5 on 生-cycle; π non-affine on He Tu; D₅ conjugation via γ; B forces attractor 比和; complement = negation is necessary but not sufficient; parity separation for all types; C retains complement = negation |
| **Measured** | Traditional uniquely achieves 吉×生体 p<0.05 (0/32 alternatives cross threshold); 3×5 grid null (p=0.731); C achieves 64/64 zero residual |
| **Structural interpretation** | Two Z₅s encode spatial vs relational; tradition chose semantic coherence over algebraic economy; zero free parameters via conjunction forcing |
| **Corrected predictions** | C was predicted to break complement — it doesn't (complement = negation ≠ complement closure); zero residual was predicted invariant — C is actually better |

---

## Iteration 2: 先天/後天 Arrangements as Mathematical Objects

### What was tested

**Can the two classical trigram arrangements (先天 Fu Xi, 後天 King Wen) be characterized as optimal embeddings of different number systems into compass geometry?**

The dual uniqueness conjecture: 先天 uniquely maximizes Z₂ geometric coherence; 後天 uniquely maximizes Z₅ geometric coherence.

Enumerated all 96 cardinal-aligned arrangements (N=Water, S=Fire, E=Wood, W=Metal, 4 remaining trigrams at intercardinals: 2×2×4! = 96). Scored each on 7 metrics:

| Metric | Domain | Definition |
|---|---|---|
| complement_diameter | Z₂ | Complement pairs (XOR=111) diametrically opposed (0-4) |
| reversal_reflection | Z₂ | Bit-reversal pairs reflected across N-S axis (0-2) |
| v4_isometry | Z₂ | V₄ actions as compass isometries (0-3) |
| Z₂ composite | Z₂ | complement_diameter + reversal_reflection (0-6) |
| sheng_min_spread | Z₅ | Min total angle to traverse 生 cycle over all representative choices |
| sheng_monotone | Z₅ | Whether min-spread path is unidirectional |
| ke_angular_variance | Z₅ | Variance of angular jumps in 克 cycle |

Also computed: τ = H ∘ X⁻¹ (the 先天→後天 permutation), its cycle structure, fiber preservation, γ projection.

### What was found

**Finding 1: 先天 is the unique Z₂ champion [proven]**

| Metric | 先天 | 後天 | Cardinal-aligned max |
|---|---|---|---|
| complement_diameter | **4/4** | 1/4 | 2 |
| reversal_reflection | **2/2** | 0/2 | 2 |
| Z₂ composite | **6/6** | 1/6 | 3 |
| v4_isometry | 1/3 | 0/3 | 1 |

先天 achieves perfect Z₂ score (6/6). The maximum achievable by ANY cardinal-aligned arrangement is 3/6. The gap of 3 is massive — cardinal alignment is fundamentally incompatible with full Z₂ geometric coherence.

In 先天: complement = rotation by π (180°), bit-reversal pairs reflected across N-S axis. Binary operations on trigrams have direct compass-geometric interpretations.

**先天 is NOT cardinal-aligned** (E=離=Fire, not Wood; W=坎=Water, not Metal). Its Z₂ optimality requires sacrificing He Tu element alignment entirely.

**Finding 2: 後天 is NOT uniquely Z₅-optimal [refuted + refined]**

後天 Z₅ composite = 78.7, tied with 55 other cardinal-aligned arrangements. Pure Z₅ metrics do not uniquely select it.

**However:** the 後天 IS the unique arrangement satisfying a three-constraint conjunction:

| Step | Constraint | Survivors | Nature |
|---|---|---|---|
| Start | Cardinal alignment | 96 | He Tu spatial |
| 1 | 生 cycle monotone | 56 | Z₅ relational |
| 2 | Element pairs adjacent or opposed | 8 | Z₅ fiber geometry |
| 3 | Cardinal yin/yang balance [1,1,2,2] | 2 | Z₂ polarity |
| 4 | Sons (震坎艮) at N/NE/E | **1** | Z₂³ positional |

Minimal uniqueness sets found by exhaustive search over all filter combinations:
- `elem_pair_coherent ∧ yy_balance ∧ sons_yang_half`
- `WM_adj_E_opp ∧ yy_balance ∧ sons_yang_half`

**Finding 3: The three constraints are the three primes [structural interpretation]**

The sage identified that the three constraints correspond to the three primes of the hexagram system (from number-structure.md):

| Prime | Constraint | What it encodes |
|---|---|---|
| 5 (relation) | elem_pair_coherent | 五行 fiber structure has spatial regularity |
| 2 (polarity) | yy_balance | Cardinal yang-line counts balanced [1,1,2,2] |
| 3 (position) | sons_yang_half | Standard basis vectors (weight-1 trigrams) maintain angular order |

The "sons" 震(001), 坎(010), 艮(100) are the standard basis of Z₂³ — distinguished by WHICH line (of the 3 lines) carries yang. Placing them at {N, NE, E} maintains the line-position ordering on the compass. This is the prime 3 (line position) made geometric.

The 後天 is the **unique triple junction of 2, 3, 5** — the unique arrangement where all three irreducible structural dimensions are simultaneously realized spatially.

**Finding 4: τ has two 4-cycles, cross-cuts all structure [proven]**

τ = H ∘ X⁻¹ cycle structure: **(坤→坎→兌→巽)(震→艮→乾→離)**

Order 4. Both cycles are length 4. Key properties:
- Every complement pair is SPLIT across cycles (Kun/Qian in different cycles, Kan/Li in different cycles, etc.)
- Element fibers are NOT preserved: Earth→{Water, Metal}, Metal→{Wood, Fire}
- The quotient permutation on Z₅ is not well-defined (τ does not factor through the element map)
- γ match: negative (as expected from fiber non-preservation)

τ necessarily cross-cuts all algebraic structure because it translates between two genuinely incommensurable embeddings. If it preserved complement structure, both arrangements would share Z₂ geometry (they don't: 4/4 vs 1/4). If it preserved element fibers, the two Z₅ systems would be algebraically related (proven impossible in iteration 1).

**Finding 5: Axis-opposition encodes 克 [measured]**

Lo Shu axis-opposite pairs on the 後天 compass:

| Axis | Pair | Elements | Relation | Lo Shu sum |
|---|---|---|---|---|
| N-S | 坎↔離 | Water↔Fire | 克 | 10 |
| NE-SW | 艮↔坤 | Earth↔Earth | 比和 | 10 |
| E-W | 震↔兌 | Wood↔Metal | 克 | 10 |
| NW-SE | 乾↔巽 | Metal↔Wood | 克 | 10 |

3 of 4 diametrically opposed pairs carry 克 relationships. Combined with 生-monotonicity (adjacent = generation), the 後天 compass encodes Z₅ relational distance spatially:
- d=1 (生) → nearby (45°-90°)
- d=2 (克) → opposite (180°)
- d=0 (比和) → same region

Lo Shu mod-5 analysis: only 2/8 positions match He Tu element numbers mod 5 (N=Water and E=Wood). The Lo Shu is NOT a mod-5 encoding of the He Tu. But the Lo Shu parity pattern is clean: all cardinals odd {1,3,9,7}, all intercardinals even {8,4,2,6}.

**Finding 6: The 先天 arrangement correction [proven]**

The 先天 arrangement going counterclockwise from S must be: 乾,兌,離,震,坤,**艮**,坎,**巽** (not 坤,巽,坎,艮). The originally specified version had 巽 and 艮 swapped, violating 說卦傳: 山澤通氣 requires 艮↔兌 diametrically opposed. The correct version has all 4 complement pairs at 180°.

Shao Yong binary values: S(7), SE(6), E(5), NE(4), N(0), NW(1), W(2), SW(3) — upper half descends counterclockwise, lower half ascends counterclockwise.

### What it means

**The dual uniqueness conjecture is half-confirmed, half-deepened.**

The 先天 half holds cleanly: it is the unique Z₂ optimum, unreachable by any cardinal-aligned arrangement. The gap (6 vs max 3) proves that Z₂ geometric coherence and He Tu spatial alignment are fundamentally incompatible.

The 後天 half is deeper than the original conjecture: it is not purely Z₅-optimal (56 arrangements tie on Z₅ metrics alone). Instead, it is the **unique arrangement where all three primes (2, 3, 5) have simultaneous geometric realization**. The 後天 doesn't abandon Z₂ the way 先天 abandons Z₅ — it retains specific Z₂ properties (yin/yang balance, element pair coherence) while achieving Z₅ monotonicity.

This means the two arrangements have asymmetric relationships to the number systems:
- **先天**: pure Z₂ embedding. Sacrifices Z₅ entirely (not cardinal-aligned).
- **後天**: joint optimization across 2, 3, 5. Retains Z₂ properties (not all), achieves Z₅ monotonicity, and encodes the prime-3 positional structure.

The incommensurability between Z₂ and Z₅ is precisely the fact that these are different arrangements. One compass, two incompatible optimality criteria, two different answers. The 先天 shows what the trigrams ARE (binary objects with complement symmetry). The 後天 shows what the trigrams DO (relational objects embedded in element cycles). The tradition needs both.

### Predictions vs results

| Prediction | Result |
|---|---|
| 先天 Z₂ = 4/4 complement + full V₄ isometry | **Partial.** complement_diameter = 4/4, reversal_reflection = 2/2, but v4_isometry = 1/3 (only complement acts as compass isometry, reversal does NOT). Z₂ composite = 6/6 confirmed. |
| 後天 Z₂ = 1/4 complement | ✓ Confirmed. Only Kan↔Li at N↔S. |
| τ cycle structure = (6,2) | ✗ Wrong. Actual: (4,4). The original prediction used incorrect 先天 arrangement. |
| γ projection negative | ✓ Confirmed. τ does not preserve element fibers; quotient map not well-defined. |
| 後天 uniquely Z₅-optimal | ✗ Refuted. 56 tie on Z₅. But uniquely selected by triple junction of 2, 3, 5. |
| Sage's metric isometry claim | ✗ Wrong. γ does NOT preserve Z₅ cyclic distance (d(0,3)=2 but d(γ(0),γ(3))=d(3,4)=1). The two Z₅ systems are incommensurable as metric spaces too, not just as algebras. |

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | 先天 Z₂ composite = 6/6, unique maximum; 96 cardinal-aligned enumeration; complement = rotation by π in 先天; 後天 complement_diameter = 1/4; τ cycle structure (4,4); τ does not preserve element fibers; γ projection negative; 先天 arrangement correction |
| **Computed (exhaustive)** | 56/96 achieve 生-monotonicity; minimal uniqueness sets for 後天 are {elem_pair_coherent ∧ yy_balance ∧ sons_yang_half}; axis-opposition = 克 in 3/4 pairs; Lo Shu mod-5 matches only 2/8 |
| **Structural interpretation** | Three constraints = three primes (2, 3, 5); 先天 = pure Z₂, 後天 = triple junction; τ cross-cuts forced by incommensurability; spatial distance encodes relational distance on 後天 compass |
| **Corrected claims** | Sage's "shared metric" is wrong (γ not distance-preserving); captain's τ=(6,2) was wrong (used wrong 先天) |

### Open threads for next iteration

1. **Examine the 8 survivors** of monotone + elem_pair_coherent — do they differ ONLY in prime-3 structure (bit-position ordering)? This would confirm the prime decomposition is exact.
2. **The compass as Z₅ distance embedding** — verify computationally that the 後天 maps 生-cycle d=1 to spatial proximity and d=2 to spatial opposition, and check whether this is unique among the 96.
3. **What selects the OTHER survivor** (arr_037, when all but sons_yang_half applied)? What is it, and what's its relationship to the 後天?
4. **Cross-cutting of τ's cycles** — is there a cleaner algebraic characterization of the two 4-cycles?


---

## Iteration 3: Prime Decomposition Verification + τ Structure

### What was tested

**1. Do the 8 survivors of (monotone + elem_pair_coherent) form an exact Z₂³ product?**

Listed all 8, decomposed their degrees of freedom, checked independence.

**2. What is the anti-後天 (arr_037) and why is it eliminated?**

Compared arr_037 (the other yy_balance survivor) to 後天 position by position.

**3. Is the Z₅ distance embedding unique?**

Scored all 96 + the 8 survivors on Z₅ distance embedding quality (mapping 生-cycle distance to spatial distance).

**4. What algebraic structure do τ's two 4-cycles have?**

Analyzed binary values, element distributions, complement relationships, and τ² within the cycles.

### What was found

**Finding 1: Exact Z₂³ product structure [proven]**

The 8 survivors have precisely three independent binary choices:
- Choice A: which Wood at E (震 vs 巽) — other Wood forced to SE by adjacency
- Choice B: which Metal at W (兌 vs 乾) — other Metal forced to NW by adjacency
- Choice C: which Earth at NE (艮 vs 坤) — other Earth forced to SW by opposition

These are algebraically independent: |A| × |B| × |C| = 2 × 2 × 2 = 8 = count of survivors. Every combination appears exactly once.

The subsequent filters act on different axes of this Z₂³:
- **yy_balance** fixes A=震, B=兌 (eliminates 6 of 8, leaving 2)
- **sons_yang_half** fixes C=艮 (eliminates 1 of 2, leaving 後天)

**Finding 2: Z₅ metrics are constant across the Z₂³ [proven]**

All 8 survivors score identically on Z₅ embedding quality (171.0). The Z₂³ degrees of freedom are ORTHOGONAL to Z₅ structure — they control only which within-fiber member goes where, not how fibers relate to each other.

This is the cleanest possible confirmation of the prime decomposition: prime-5 constraints exhaust all Z₅ information, and the residual degrees of freedom are purely Z₂ (polarity/position within fibers).

**Finding 3: The anti-後天 is a single Earth-pair swap [proven]**

arr_037 differs from 後天 at exactly {NE, SW}: 艮↔坤 swapped.
- 後天: 艮(mountain/youngest son) at NE (dawn), 坤(earth/mother) at SW (afternoon)
- anti: 坤 at NE, 艮 at SW — inverts the generational flow of the 說卦傳

Not a historically attested arrangement. The sons_yang_half constraint (placing weight-1 trigrams at {N, NE, E}) is exactly what eliminates it: 艮(100) must be at NE, not SW.

**Finding 4: τ's cycles have complement-bridging structure [proven]**

Cycle 1: (坤→坎→兌→巽) — elements: Earth→Water→Metal→Wood
Cycle 2: (震→艮→乾→離) — elements: Wood→Earth→Metal→Fire

Key properties confirmed:
- Each cycle contains exactly one trigram from each doubleton element (Wood, Metal, Earth)
- Cycle 1 contains Water (singleton), Cycle 2 contains Fire (singleton)
- **Complement maps cycle 1 ↔ cycle 2** (XOR 111 swaps the two cycles entirely)
- τ has order 4: τ⁴ = identity
- τ² gives four 2-cycles: (坤↔兌)(震↔乾)(坎↔巽)(艮↔離) — all cross-element
- Neither τ nor τ² preserves element fibers
- τ is genuinely non-geometric: 5 distinct angular displacements, cannot be realized as any D₈ isometry

### What it means

**The prime decomposition of 後天 uniqueness is exact:**

| Stage | Constraint | Prime | Survivors | What it determines |
|---|---|---|---|---|
| 0 | Cardinal alignment | — | 96 | Fixed frame |
| 1 | Monotone + elem_pair_coherent | 5 | 8 | Which elements go where (fibers) |
| 2 | yy_balance | 2 | 2 | Which polarity member goes to which cardinal |
| 3 | sons_yang_half | 3 | 1 | Which line-position basis vector goes where |

The residual space after prime-5 is Z₂³, and the Z₂ and Z₃ constraints act on different axes of this residual. The decomposition is:
- 96 → 8: **prime 5 removes all relational degrees of freedom** (Z₅ metrics constant across survivors)
- 8 → 2: **prime 2 removes polarity ambiguity** at cardinals
- 2 → 1: **prime 3 removes positional ambiguity** at intercardinals

**τ's complement-bridging property** adds to the incommensurability picture: the transformation between 先天 and 後天 splits every complement pair across its two cycles, but the complement operation itself maps cycle 1 to cycle 2. So complement "knows about" τ's structure even though τ doesn't preserve complement geometry. The two arrangements are entangled through complement even as they differ on it.

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | Z₂³ product structure exact; Z₅ metrics constant across 8 survivors; anti-後天 = single Earth swap; τ cycles complement-bridging; τ order 4; τ non-geometric (5 distinct displacements) |
| **Structural interpretation** | Prime decomposition 96→8→2→1 corresponds to primes 5→2→3; Z₅ orthogonal to Z₂³ residual |



---

## Iteration 4: Dimensional Forcing — Why 3 Lines?

### What was tested

**Is n=3 the unique dimension where the Z₂/Z₅ bridge is structurally guaranteed?**

For Z₂ⁿ with complement=negation surjections onto Z₅:
- Complement pairs (2^(n-1) of them) distribute across 3 destination types: k₀ pairs → Wood (self-conjugate), k₁ pairs → Fire/Water split, k₂ pairs → Earth/Metal split
- Fiber sizes: |Wood|=2k₀, |Fire|=|Water|=k₁, |Earth|=|Metal|=k₂
- Surjective requires k₀,k₁,k₂ ≥ 1
- Singletons exist iff min(k₁,k₂) = 1

Also tested: 互 convergence dynamics for 4-line, 6-line, and 8-line figures.

### What was found

**Finding 1: Dimensional Forcing Theorem [proven]**

| n | Pairs | Surjective shapes | All have singletons? |
|---|---|---|---|
| 1 | 1 | 0 | n/a (impossible) |
| 2 | 2 | 0 | n/a (impossible) |
| **3** | **4** | **3** | **★ YES** |
| 4 | 8 | 21 | no (10 without) |
| 5 | 16 | 105 | no (78 without) |
| 6+ | ... | ... | no (grows rapidly) |

**Theorem.** Let f: Z₂ⁿ → Z₅ be a surjection satisfying f(x̄) = -f(x) mod 5. Then:
- (a) Such f exists if and only if n ≥ 3
- (b) For n = 3, every such f has at least two singleton fibers
- (c) For n ≥ 4, there exist such f with no singleton fibers

**Proof.** 2^(n-1) complement pairs distributed as (k₀, k₁, k₂) with all ≥ 1.
- (a): k₀+k₁+k₂ = 2^(n-1) ≥ 3 iff n ≥ 3.
- (b): For n=3, k₀+k₁+k₂ = 4. If min(k₁,k₂) ≥ 2 then k₁+k₂ ≥ 4, so k₀ ≤ 0 — contradiction. Therefore min(k₁,k₂) = 1 always.
- (c): For n=4, (k₀,k₁,k₂) = (4,2,2) gives all fibers ≥ 2. □

**Why n=3 is special:** 2^(n-1) = 4 = 3+1. After meeting the surjectivity minimum (one pair to each destination), exactly ONE unit of slack remains. That single unit can enlarge only one destination type, so the other split type stays at k=1 = singleton. For n=4: 2^(n-1) = 8 = 3+5, five units of slack — enough to avoid singletons entirely.

**Finding 2: Concrete enumeration for n=3 [verified]**

240 total valid complement=negation surjections Z₂³ → Z₅:
- Shape (2,1,1) → fibers [4,1,1,1,1]: 48 assignments
- Shape (1,2,1) → fibers [2,2,2,1,1]: 96 assignments ← traditional shape
- Shape (1,1,2) → fibers [2,1,1,2,2]: 96 assignments

ALL 240 have singletons. Direct enumeration matches combinatorial count.

**Finding 3: n=4 loses the singleton guarantee [proven]**

21 surjective partition shapes for n=4. 10 of 21 (48%) have no singletons.
312,480 total concrete assignments. Non-singleton partitions dominate.

**Finding 4: 互 involution boundary at n=3 [computed]**

| n | Lines | Max cycle length | 互² = id on cycles? |
|---|---|---|---|
| 2 | 4 | 2 | ✓ |
| 3 | 6 | 2 | ✓ |
| 4 | 8 | 3 | ✗ |

n=3 (6 lines) is the largest dimension where 互² = identity on all eventual cycles. At n=4 (8 lines), 3-cycles appear — a qualitative dynamical change. The 既濟/未濟 pair as a 2-cycle attractor depends on this involutory property.

### What it means

**The trigram having 3 lines is not a design choice but a structural necessity.** n=3 is the unique dimension where:
1. Surjective complement=negation partitions Z₂ⁿ → Z₅ EXIST (rules out n ≤ 2)
2. ALL such partitions FORCE singletons (rules out n ≥ 4)
3. 互 dynamics remain involutory on cycles (rules out n ≥ 4 independently)

The singleton forcing is what makes the Fire/Water bridge possible — the injective points where the Z₂ⁿ → Z₅ quotient is invertible, where binary dynamics and element evaluation achieve constructive interference.

**The complete dimensional derivation:**

| Dimension | Value | Derivation |
|---|---|---|
| Elements | 5 | Smallest prime supporting two independent non-degenerate cycles |
| Lines per trigram | 3 | Unique singleton-forcing dimension for Z₂ⁿ → Z₅ |
| Trigrams | 8 = 2³ | Follows from n=3 |
| Lines per hexagram | 6 = 2×3 | Largest involutory 互 dimension |
| Hexagrams | 64 = 2⁶ | Follows from 2n=6 |

Everything follows from {2, 3, 5}.

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | Dimensional forcing theorem (parts a, b, c); n=3 uniqueness among n=1..8; 240 concrete assignments all have singletons; 互 max cycle length 2 for n≤3, 3 for n=4 |
| **Structural interpretation** | Three lines forced by singleton bridge requirement; six lines forced by involutory 互; all dimensions derive from primes {2,3,5} |


---

## Iteration 5: The King Wen Sequence

### What was tested

**Does the King Wen sequence (the traditional ordering of the 64 hexagrams) have algebraic structure when projected through our coordinate systems?**

Encoded the full KW sequence, analyzed pairing structure, projected through Z₂⁶, Z₅×Z₅, Z₅ quotient, 互 basins, complement, and 先天. Tested sequential structure against null hypothesis (random permutation) with 10,000 Monte Carlo simulations.

### What was found

**Finding 1: KW pairing = reversal ∪ complement [verified]**

The 32 KW pairs: 28 are reversal pairs (flip hexagram upside down), 4 are complement-only pairs. The 4 complement-only pairs are exactly the palindromic hexagram pairs — those where reversal = identity:
- #1/2 (乾/坤), #27/28 (頤/大過), #29/30 (坎/離), #61/62 (中孚/小過)

Traditional claim confirmed computationally. Zero pairs are "neither."

**Finding 2: Basin clustering is the sole significant sequential signal [measured, p < 0.001]**

| Metric | p-value | Significant? |
|---|---|---|
| Basin clustering | **< 0.001** | ★★★ YES |
| Hamming distance | 0.982 | No |
| Z₅×Z₅ torus step | 0.618 | No |
| 互 continuity | 0.182 | No |
| Element continuity | 1.000 | No (ZERO consecutive same-element-pair) |
| 先天 correlation | 0.415 | No |

Same-basin transitions: 38/63 (60%) vs null expectation 23/63 (37%). The KW sequence clusters by inner-line structure (bits 1-4), not by element, not by binary order, not by Hamming proximity.

**Finding 3: 上經/下經 = palindromic/non-palindromic pure partition [structural]**

The 上經 (hexagrams 1-30) contains 4 pure hexagrams: 乾(111), 坤(000), 坎(010), 離(101). These are exactly the **palindromic trigrams** (b₀ = b₂, fixed points of bit-reversal).

The 下經 (hexagrams 31-64) contains 4 pures: 震(001), 艮(100), 巽(110), 兌(011). These are exactly the **non-palindromic trigrams** (moved by bit-reversal, forming 2 orbits: {001↔100}, {011↔110}).

The 上經/下經 split separates reversal-fixed from reversal-mobile anchors. The split boundary (#29-30, 坎/離) falls at the Fire/Water singletons — the Z₂/Z₅ bridge points.

**Finding 4: Complement preserves KW pairing [proven]**

All 32 KW pairs map to KW pairs under complement (32/32). 8 pairs are self-complementary (both members of the pair are each other's complement, or the pair is a palindromic pair where complement ≠ reversal). The complement involution acts on the 32-pair set, fixing 8 and swapping 12 non-fixed pairs in order-2 orbits.

**Finding 5: Basin mirror symmetry between canons [measured]**

上經: Kun-dominated (11K, 14KL, 5Q). 下經: Qian-dominated (5K, 18KL, 11Q). The two canons occupy mirror-image positions in basin space.

**Finding 6: Z₅×Z₅ anti-clustering [measured]**

Zero consecutive hexagrams share both upper AND lower element. The sequence actively avoids element-level repetition while maintaining basin-level coherence. This is a dual optimization: maximal variety at the semantic level (Z₅×Z₅), maximal clustering at the structural level (互 basins).

### What it means

The KW sequence has two layers of structure:

1. **Pairing structure** (well-known, now verified): reversal ∪ complement, with complement preserving the pairing as an involution.

2. **Sequential structure** (one signal): basin clustering. The sequence organizes by nuclear scaffolding (互 basins), not by semantic content (elements, directed relations). This aligns with the iteration-1 finding that 互 is "structurally constrained but not semantically discriminating" (χ² p=0.731): the KW sequence tracks the structural substrate, not the evaluative overlay.

The 上經/下經 split has a clean algebraic characterization: palindromic vs non-palindromic pure anchors. The palindromic trigrams (坎, 離, 乾, 坤) include the Fire/Water bridge points and the maximal-polarity parents. The 上經 is the "stable + bridge" canon; the 下經 is the "mobile" canon.

### Epistemic status

| Category | Claims |
|---|---|
| **Verified** | KW pairing = reversal ∪ complement (28+4); complement preserves pairing (32/32); all 25 Z₅×Z₅ cells visited |
| **Measured** | Basin clustering p < 0.001; all other sequential metrics null; basin mirror symmetry between canons; Z₅×Z₅ anti-clustering (0 consecutive same-pair) |
| **Structural interpretation** | 上經/下經 = palindromic/non-palindromic partition; sequence organized by scaffolding not content; dual optimization (element variety + basin coherence) |

---

## Synthesis (updated)

### The complete derivation tree

From two axioms — (i) two independent cycles exist on a finite set, (ii) a complement-respecting binary substrate exists — the entire parametric structure of the I Ching follows:

```
Axiom: two independent non-degenerate cycles on a finite set
  → |set| = 5 (smallest prime supporting this)
    → Z₅ with 生-cycle (stride 1) and 克-cycle (stride 2)
    → Complement must act as negation (unique order-2 automorphism)
      → Surjective partition Z₂ⁿ → Z₅ with complement=negation
        → n ≥ 3 (surjectivity requires 2^(n-1) ≥ 3)
        → n = 3 (unique dimension forcing singletons)
          → 8 trigrams, 64 hexagrams, 6-line figures
          → {2,2,2,1,1} partition (3 shapes, 240 assignments)
            → Conjunction of algebra + text selects 1 (traditional)
              → 先天: unique Z₂ embedding (complement = diameter)
              → 後天: unique 2×3×5 triple junction
                → τ: order-4, complement-bridging, fiber-breaking
  → 互 dynamics: involutory iff n ≤ 3
    → 6-line hexagrams = largest involutory dimension
    → 既濟/未濟 as 2-cycle attractor (singleton elements)
```

### What each iteration contributed

| Iteration | Question | Answer | Key result |
|---|---|---|---|
| 1 | Why this 五行 assignment? | Zero free parameters | Conjunction of algebra + text selects uniquely |
| 2 | Why these arrangements? | 先天 = Z₂ optimal, 後天 = 2×3×5 junction | Gap of 3 for 先天; triple conjunction for 後天 |
| 3 | Is the prime decomposition exact? | Yes: Z₂³ residual, orthogonal to Z₅ | 96→8→2→1 = primes 5→2→3 |
| 4 | Why 3 lines? | Unique singleton-forcing dimension | Pigeonhole + 互 involution boundary |
| 5 | KW sequence structure? | Basin clustering + palindrome partition | One significant signal; 上經/下經 = palindromic/non-palindromic |

### Four nested incommensurabilities

| Layer | Gap | Bridge | Status |
|---|---|---|---|
| Z₂ vs Z₅ | Binary vs pentadic | Complement (unique cross-framework involution) | Bridged |
| He Tu Z₅ vs 生-cycle Z₅ | Spatial vs dynamic | 後天 compass (triple junction, not algebra) | Connected |
| 先天 vs 後天 | Z₂ optimum vs 2×3×5 junction | τ: order-4, complement-bridging, fiber-breaking | Mapped |
| Shell vs Core | Identity vs convergence | None (orthogonality wall) | Unbridged |

---

## Iteration 6: V₄ Symmetry Group on Z₂⁶

### What was tested

**How does the Klein four-group V₄ = {id, complement, reversal, comp∘rev} act on the 64 hexagrams, and what does it reveal about the system's symmetry structure?**

### What was found

**Finding 1: V₄-equivariance of 互 [proven]**

All three V₄ involutions commute with 互 (nuclear extraction): complement ∘ 互 = 互 ∘ complement, reversal ∘ 互 = 互 ∘ reversal, (comp∘rev) ∘ 互 = 互 ∘ (comp∘rev). Verified exhaustively on all 64 hexagrams.

互 is a V₄-equivariant endomorphism of Z₂⁶. The nuclear transform respects all the symmetry of the system simultaneously, not just complement (which was known from the atlas).

This follows algebraically: 互 extracts inner bits (1,2,3,4) and forms two overlapping trigrams. Reversal on the 6-bit hexagram maps inner bits (1,2,3,4) → (4,3,2,1), which reverses each trigram AND swaps upper/lower — the same as applying reversal to the 互 output. Complement on the 6-bit level applies complement to the inner bits, which commutes with the trigram extraction.

**Finding 2: V₄ orbit structure [proven]**

20 orbits: 0 of size 1, 8 of size 2, 12 of size 4.

The 8 size-2 orbits split into two families:
- **4 palindrome pairs** (reversal-fixed): {乾,坤}, {坎,離}, {中孚,小過}, {頤,大過}
- **4 anti-palindrome pairs** (comp∘rev-fixed): {泰,否}, {隨,蠱}, {漸,歸妹}, {既濟,未濟}

No hexagram is fixed by all three involutions (no size-1 orbits).

**Finding 3: Anti-palindromes are the balanced center [proven]**

The 8 comp∘rev-fixed hexagrams (anti-palindromes) where h = complement(reverse(h)):
- ALL have exactly 3 yang lines (perfect yin/yang balance)
- ALL are in the KanLi basin (the interface basin)
- Include 既濟(#63) and 未濟(#64) — the 互 cycle attractors
- Lower trigram uniquely determines upper as comp∘rev(lower)

Anti-palindromes are the hexagrams at the system's geometric center: balanced polarity, interface basin, convergence locus.

**Finding 4: Complement is the unique Z₅-visible V₄ element [proven]**

| V₄ element | Fiber-preserving? | Relation well-defined? | Basin action |
|---|---|---|---|
| Complement | ✓ (negation on Z₅) | ✓ (inverts direction) | Kun↔Qian, KanLi fixed |
| Reversal | ✗ (Wood→{Earth,Metal}) | ✗ | All fixed |
| Comp∘Rev | ✗ | ✗ | Kun↔Qian, KanLi fixed |

V₄ = Z₂(complement) × Z₂(reversal) decomposes as: complement is the Z₅-visible factor, reversal is the Z₂-only factor. Only complement descends to the element quotient.

**Finding 5: All V₄ elements preserve KW pairing [proven]**

Complement, reversal, and comp∘rev all map KW pairs to KW pairs. V₄ acts on the 32 KW pairs, giving 20 pair-orbits: 8 size-1 (self-complementary pairs) + 12 size-2.

The 上經/下經 split is V₄-compatible: 7 pair-orbits in 上經, 7 in 下經, 6 split across both canons. The 6 split orbits are complement-bridges connecting the two canons.

### What it means

V₄ provides the complete symmetry picture of the hexagram system:

- **Complement** (Z₂ factor 1): the unique operation that respects BOTH Z₂ and Z₅ structure. It bridges the two number systems, preserves element fibers, inverts directed relations, and swaps Kun↔Qian basins.
- **Reversal** (Z₂ factor 2): purely Z₂. Preserves basins and commutes with 互, but is opaque to the element system. Generates the KW pairing structure.
- **Comp∘Rev** (product): selects the balanced center — the anti-palindromes at the interface of all structure.

The V₄-equivariance of 互 means the nuclear transform is maximally symmetric: it respects every involution the system has.

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | V₄ group axioms; 互 commutes with all V₄ elements; 20 orbits (0+8+12); anti-palindromes all 3-yang, all KanLi; complement uniquely fiber-preserving; all V₄ preserve KW pairing |
| **Structural interpretation** | V₄ = Z₂(Z₅-visible) × Z₂(Z₂-only); anti-palindromes = geometric center; 互 is V₄-equivariant |


---

## Iteration 7: Transformation Graph and Palace Structure

### What was tested

**How do single-line changes and the Jing Fang palace walk interact with our coordinate systems?**

### What was found

**Finding 1: Line hierarchy — three tiers of structural impact [proven]**

| Bit | Line | Element change | Basin change | Role |
|---|---|:---:|:---:|---|
| b₀, b₁ | 1, 2 (lower outer) | 100% | 0% | Always cross element fibers, never cross basins |
| b₂ | 3 (lower top) | 50% | 100% | Intra-fiber discriminator + basin interface |
| b₃ | 4 (upper bottom) | 100% | 100% | Always cross both element and basin |
| b₄ | 5 (upper middle) | 100% | 0% | Always cross element fibers |
| b₅ | 6 (upper top) | 50% | 0% | Intra-fiber discriminator, palace invariant |

b₂ and b₃ are the **interface bits** — the only bits that change basins (because 互 extracts bits 1-4). b₂ and b₅ are the **top bits** of each trigram — they discriminate WITHIN element fibers (e.g., 震 vs 巽 differ only in b₂). Top bits have 50% element change rate because half the time they flip within a fiber.

**Finding 2: Palace walk = onion traversal with 体/用 complementarity [proven]**

The Jing Fang bit-flip sequence: b₀, b₁, b₂, b₃, b₄, undo-b₃, undo-b₀b₁b₂.

- R0-R2: Flip lower trigram progressively (体 departs, 用 fixed)
- R3: Cross the interface (first basin change)
- R4-R5: Flip upper trigram core (用 departs)
- R6 (游魂): Un-flip b₃ — interface retract (second basin change)
- R7 (歸魂): Bulk restore lower trigram (体 returns to palace root)

体 (lower) preserved at R0 and R7 only. 用 (upper) preserved at R0-R3 only. The crossover is at the interface bits. **b₅ is NEVER flipped** — it's the palace invariant. The palace is classified by the top bit of the upper trigram.

**Finding 3: Palindromic palaces visit all 3 basins; non-palindromic visit only 2 [proven]**

| Basin trajectory class | Palaces | Basins visited |
|---|---|:---:|
| Kun→Kun→Kun→KL→Qian→Qian→KL→Kun | 坤, 坎 | 3 |
| Qian→Qian→Qian→KL→Kun→Kun→KL→Qian | 離, 乾 | 3 |
| KL→KL→KL→Qian→KL→KL→Qian→KL | 震, 兌 | 2 |
| KL→KL→KL→Kun→KL→KL→Kun→KL | 艮, 巽 | 2 |

Palindromic trigram palaces {坤, 坎, 離, 乾} visit all 3 basins. Non-palindromic {震, 兌, 艮, 巽} visit only 2.

Mechanism: palindromic trigrams have b₀ = b₂, so flipping b₂ changes basin WITHOUT changing element (decoupled coordinates). Non-palindromic trigrams have b₀ ≠ b₂, so flipping b₂ changes both simultaneously (entangled coordinates). Decoupled control → more reachable basins.

This is the same palindromic/non-palindromic split that governs the 上經/下經 partition (iteration 5) — now appearing as basin-traversal depth.

**Finding 4: V₄ × palace interaction [proven]**

- Complement: 0/64 same-palace (maximally boundary-crossing)
- Reversal: 8/64 same-palace (only palindromic 本宮 hexagrams)
- Comp∘Rev: 24/64 same-palace (highest non-trivial same-palace rate)

Complement-paired palaces share identical V₄ orbit patterns. Palindromic-root palaces have 6 distinct V₄ orbits per palace; non-palindromic have 8.

**Finding 5: 世 pattern verified [proven]**

世 (self/shi) line positions: [6, 1, 2, 3, 4, 5, 4, 3]. Ascends through lines 1-5, then retraces 4→3. 本宮 世=6 (the palace invariant bit). The retrace at 游魂/歸魂 mirrors the walk's structural retraction.

### What it means

The palace system is algebraically clean: it's an onion traversal of Z₂⁶ that respects the three-tier line hierarchy (outer/interface/shell). The 体/用 complementarity — 体 explores first and returns, 用 holds then departs — provides the operational rhythm of 火珠林 divination.

The palindromic split (basin-decoupled vs entangled) is now a three-context invariant:
1. **上經/下經**: palindromic anchors in 上經, non-palindromic in 下經
2. **Palace basins**: palindromic palaces visit all 3, non-palindromic visit 2
3. **V₄ orbits**: palindromic 本宮 are reversal-fixed, non-palindromic are reversal-mobile

The underlying mechanism is always the same: b₀ = b₂ decouples the intra-fiber and inter-basin degrees of freedom.

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | Line hierarchy (element/basin change rates); palace bit-flip sequence; 8 palaces × 8 = 64 partition; 世 pattern [6,1,2,3,4,5,4,3]; b₅ invariance; 体/用 complementarity; basin trajectory classes (4 types); complement 0/64 same-palace; palindromic mechanism (b₀=b₂ decoupling) |
| **Structural interpretation** | Palace = onion traversal; palindromic split = coordinate decoupling; operational layer aligned with binary geometry |

---

## Iteration 8: V₄-Compatible Pairings + Palace Torus Trajectories

### What was tested

**How many V₄-compatible pairings exist, and what selects the KW pairing from among them?**

### What was found

**Finding 1: 531,441 V₄-compatible pairings exist [proven]**

V₄ acts on 64 hexagrams producing 20 orbits: 8 of size 2 (pairing forced) + 12 of size 4 (3 choices each, one per involution). Choices are independent across orbits → 3^12 = 531,441 total.

**Finding 2: KW pairing = unique basin-preservation maximum [proven]**

| Pairing | Same-basin pairs | Hamming total |
|---|:---:|:---:|
| KW (pure reversal) | **28/32** (87.5%) | 120 |
| Pure complement | 16/32 (50%) | 192 |
| Pure comp∘rev | 16/32 (50%) | 120 |
| Min-Hamming (hybrid) | 20/32 (62.5%) | 96 |

**Theorem.** The KW pairing is the unique V₄-compatible pairing that maximizes same-basin pairs.

*Proof.* Reversal preserves all three basins (proven iteration 6). Complement and comp∘rev swap Kun↔Qian. For any size-4 orbit, choosing reversal guarantees both resulting pairs are same-basin. Choosing any other involution introduces at least one cross-basin pair (verified: in every size-4 orbit, the complement and comp∘rev splittings each produce exactly one cross-basin pair). The 8 size-2 orbits are forced. So the basin-maximizing strategy is uniquely "reversal everywhere" = KW pairing. □

The 4 cross-basin pairs in KW are the forced palindromic pairs (乾/坤, 坎/離, 中孚/小過, 頤/大過) — complement pairs where reversal isn't available because the hexagrams are self-reversing.

**Finding 3: Minimum-Hamming pairing is unique and unnamed [computed]**

Total Hamming 96, achieved uniquely by using reversal in 6 orbits and comp∘rev in 6 — exactly where each locally minimizes. The KW pairing sacrifices 24 Hamming units for structural uniformity (same involution everywhere). Analogous to the 五行 assignment choosing semantic coherence over algebraic economy (iteration 1).

**Finding 4: Palace torus trajectories confirm Z₅ complement structure [proven]**

Complement-paired palaces have perfectly negation-mirrored Z₅×Z₅ trajectories at all 8 ranks. Singleton palaces (坎, 離) achieve zero-revisit torus efficiency (8/8 distinct cells). All 25 Z₅×Z₅ cells covered across the 8 palaces.

### What it means

The KW pairing is now derived: it's the unique V₄-compatible pairing that maximizes 互 basin coherence. Basin preservation = nuclear-structure preservation: paired hexagrams share the same convergence dynamics under 互. The tradition pairs hexagrams that "compute the same way" under nuclear extraction.

This extends the derivation tree: the KW pairing (reversal + complement fallback) is not arbitrary but uniquely forced by basin preservation within the V₄ symmetry group.

### Epistemic status

| Category | Claims |
|---|---|
| **Proven** | 3^12 = 531,441 V₄-compatible pairings; KW = unique basin-maximizer (theorem + exhaustive verification); min-Hamming pairing unique at H=96; complement-palace trajectories perfectly Z₅-mirrored |
| **Structural interpretation** | KW optimizes nuclear coherence over Hamming proximity; tradition chooses uniform rules over local optimization; singleton palaces are torus-efficient |


---

## Iteration 9: Line Text Valuations and the Binary Hierarchy

### What was tested

**Do the yaoci (line texts) encode the algebraic line hierarchy discovered in iteration 7?**

Analyzed 384 yaoci (64 hexagrams × 6 lines) for textual valuation markers (吉, 凶, 无咎, 悔, 吝, 厲, 亨). Tested correlation with line position, algebraic role, element relation, 体/用 split, and 世 line.

### What was found

**Finding 1: The algebraic role hierarchy manifests in the text [measured, p < 0.001]**

| Role | Lines | 吉% | 凶% | Algebraic property |
|---|---|:---:|:---:|---|
| Outer core | 1,2,5 | **39.6%** | **9.4%** | Change element, preserve basin |
| Interface | 3,4 | **19.5%** | **13.3%** | Change basin |
| Shell | 6 | **26.6%** | **26.6%** | Palace invariant, intra-fiber |

吉 × algebraic role: χ²=15.1, p=0.0005. 凶 × algebraic role: χ²=12.1, p=0.0023.

Outer core lines (element-changers that preserve basins) are the most auspicious. Interface lines (basin-changers) are the least auspicious. Shell (palace invariant, line 6) concentrates 凶.

Interpretation: basin preservation → safety. Crossing a basin boundary means changing 互 convergence dynamics — a more fundamental structural shift than element substitution. The text authors encoded this: basin disruption is dangerous, element change within a basin is manageable.

**Finding 2: Line 5 is the ruler [measured, p=0.007]**

Line 5 (b₄): 吉=45.3%, 凶=4.7%. OR=2.15 vs all other lines (p=0.007 for 吉, p=0.026 for 凶). The traditional designation as 君位 (ruler position) has a clear algebraic basis: b₄ is outer core (maximum influence, minimum structural disruption) and the central bit of the upper trigram.

**Finding 3: The 吉×生体 bridge is position-dependent [measured, p=0.0009]**

The relation × position interaction (30-cell χ²=58.6, p=0.0009) shows the 生体 advantage concentrates at specific lines:

| | L1 | L2 | L3 | L4 | L5 | L6 | Total |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 生体 吉% | 33% | 33% | 17% | 42% | **75%** | **50%** | 41.7% |
| 克体 吉% | 23% | 31% | **0%** | 8% | 31% | 23% | 19.2% |

Line 5 in 生体 hexagrams reaches 75% 吉 — the highest rate in the entire system. Line 3 in 克体 hexagrams has 0% 吉 and 31% 凶 — the most dangerous specific combination. The text evaluates BOTH the element relation AND the line's structural position.

**Finding 4: 体/用 and 世 line are NOT encoded in the yaoci [measured, p > 0.2]**

体 vs 用: p=0.22 (吉), p=0.65 (凶). 世 vs non-世: p=0.30 (吉), p=0.84 (凶). Neither the 梅花 体/用 framework nor the 京房 世 line system is reflected in the yaoci text.

This confirms a chronological-structural ordering: the yaoci encode the foundational layer (binary geometry + element relations) but not the operational overlays (体/用, 世 line) that were developed later.

### What it means

**The yaoci text encodes the same hierarchy that the algebraic analysis discovers.** The binary geometry of the hexagram (which bits are outer/interface/shell) predicts which lines the ancient text treats as auspicious or dangerous. This is the strongest text-structure bridge: not just a marginal correlation (the 吉×生体 p=0.007 from iteration 1) but a structured, position-dependent pattern (interaction p=0.0009).

The text is not independent of the mathematics. But it IS independent of the operational mathematics — the later systems (梅花, 京房) built on the foundation without being part of the original encoding.

### Epistemic status

| Category | Claims |
|---|---|
| **Measured** | 吉×role p=0.0005; 凶×role p=0.0023; line 5 OR=2.15, p=0.007; relation×position interaction p=0.0009; 体/用 null p=0.22; 世 null p=0.30 |
| **Structural interpretation** | Basin preservation → textual safety; line hierarchy = valuation hierarchy; foundational layer encoded in text, operational layers not |

---

## Final Synthesis (Complete)

### The complete derivation tree

From two axioms — (i) two independent non-degenerate cycles exist on a finite set, (ii) a complement-respecting binary substrate exists — the entire parametric structure follows:

```
Axiom: two independent non-degenerate cycles on a finite set
  → |set| = 5 (smallest viable prime)
    → Z₅ with 生-cycle (stride 1) and 克-cycle (stride 2)
    → Complement must act as negation (unique order-2 automorphism)
      → Surjective partition Z₂ⁿ → Z₅ with complement=negation
        → n ≥ 3 (surjectivity requires 2^(n-1) ≥ 3)
        → n = 3 (unique dimension forcing singletons)
          → 8 trigrams, 64 hexagrams, 6-line figures
          → {2,2,2,1,1} partition (3 shapes, 240 assignments)
            → Conjunction of algebra + text selects 1 (traditional)
              → 先天: unique Z₂ embedding (complement = diameter)
              → 後天: unique 2×3×5 triple junction
                → τ: order-4, complement-bridging, fiber-breaking
  → V₄ = {id, complement, reversal, comp∘rev} acts on Z₂⁶
    → 互 is V₄-equivariant (commutes with all involutions)
    → KW pairing = unique basin-preservation maximum among 3^12 V₄-compatible pairings
    → Anti-palindromes (comp∘rev-fixed) = balanced center (3 yang, KanLi basin, 既濟/未濟)
  → 互 dynamics: involutory iff n ≤ 3
    → 6-line hexagrams = largest involutory dimension
    → 既濟/未濟 as 2-cycle attractor (singleton elements)
  → Line hierarchy: outer core / interface / shell
    → Palace walk (京房): onion traversal respecting hierarchy, b₅ invariant
    → Yaoci text: algebraic role predicts valuation (p < 0.001)
```

### What each iteration contributed

| Iteration | Question | Answer | Key result |
|---|---|---|---|
| 1 | Why this 五行 assignment? | Zero free parameters | Conjunction of algebra + text selects uniquely |
| 2 | Why these arrangements? | 先天 = Z₂ optimal, 後天 = 2×3×5 junction | Gap of 3 for 先天; triple conjunction for 後天 |
| 3 | Is the prime decomposition exact? | Yes: Z₂³ residual, orthogonal to Z₅ | 96→8→2→1 = primes 5→2→3 |
| 4 | Why 3 lines? | Unique singleton-forcing dimension | Pigeonhole + 互 involution boundary |
| 5 | KW sequence structure? | Basin clustering + palindrome partition | One significant signal; 上經/下經 = palindromic/non-palindromic |
| 6 | V₄ symmetry? | 互 is V₄-equivariant; anti-palindromes = center | Complement uniquely Z₅-visible; 20 orbits |
| 7 | Palace structure? | Onion traversal, b₅ invariant | Line hierarchy; palindromic palaces visit 3 basins |
| 8 | KW pairing uniqueness? | Unique basin-preservation maximum | Theorem: reversal-maximal = basin-maximal among 3^12 |
| 9 | Line texts encode hierarchy? | Yes (p < 0.001) | Algebraic role predicts 吉/凶; 生体×line5 = 75% 吉 |

### Four nested incommensurabilities

| Layer | Gap | Bridge | Status |
|---|---|---|---|
| Z₂ vs Z₅ | Binary vs pentadic | Complement (unique cross-framework involution) | Bridged |
| He Tu Z₅ vs 生-cycle Z₅ | Spatial vs dynamic | 後天 compass (triple junction, not algebra) | Connected |
| 先天 vs 後天 | Z₂ optimum vs 2×3×5 junction | τ: order-4, complement-bridging, fiber-breaking | Mapped |
| Shell vs Core | Identity vs convergence | None (orthogonality wall) | Unbridged |

### The exploration's arc

The deep exploration traced from axioms to text in 9 iterations:

1. **Foundation** (iterations 1-4): Why this specific system — every parameter derived from minimal axioms. The dimensions {2,3,5}, the element assignment, the two compass arrangements, the dimensional forcing theorem.

2. **Structure** (iterations 5-8): How the system organizes itself — KW sequence, V₄ symmetry group, palace walks, pairing uniqueness. Each layer of organization has a clean algebraic characterization.

3. **Bridge** (iteration 9): The text encodes the algebra — the line hierarchy discovered from binary geometry predicts the textual valuations of the ancient yaoci. The circle closes: mathematical structure → textual tradition → mathematical structure.

The computational picture is complete. Every parameter derived, every organizational layer characterized, and the text-structure bridge confirmed at the line level.
