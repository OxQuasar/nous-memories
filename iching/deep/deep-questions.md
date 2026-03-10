# Deep Questions

Questions beyond the atlas resolution. Structural, philosophical, possibly unanswerable with current tools.

Status tracking: **RESOLVED** = computationally answered with proof/exhaustive computation. **OPEN** = well-characterized but not computationally resolvable.

---

## 1. Is there a coordinate-free space underneath? [OPEN]

We have multiple coordinate systems describing the same 64 objects:
- Z₂⁶ (binary lines — combinatorial identity)
- Z₅×Z₅ (element pairs — relational surface)
- Z₅ quotient (directed relations — meaning)
- Lo Shu 3×3 (positional geometry with mod-5 conservation)
- Palace walks (8 orbits under iterated bit-flip)
- 互 convergence (3 basins, depth layers)

Usually multiple charts imply an intrinsic manifold. The instinct: there's a coordinate-free object all of these are projections of.

### The obstruction

**There can't be a standard algebraic one.** F₂ and Z₅ are coprime. Any abelian group that's simultaneously an F₂-module and a Z₅-module decomposes as their direct product — and Z₂⁶ has no Z₅-subquotient as a group. The trigram→element map is not a homomorphism. It cannot be. There is no algebraic arrow connecting the binary and pentadic structures.

The two number systems coexist on the same 64-point set but cannot be unified into a single algebraic structure.

### Three possibilities

**A. The relational web.** The 64 hexagrams with their full incidence structure: 互 chains, 變 fan, complement pairs, reverse pairs, palace membership, basin convergence, element assignment, seasonal access. No coordinates — just the relation pattern. Every coordinate system is a different reading of this web. The web is the invariant; the coordinates are perspectives.

**B. Something categorical.** The hexagram as a functor from the category of contexts (seasons × questions × methods) to relational structures. Different coordinate systems correspond to different evaluations of the functor. The coordinate-free object is the functor itself. But category theory provides language, not content.

**C. There is no underlying space.** The system is fundamentally the *tension* between two incommensurable structures meeting on a shared finite set. 64 points are the meeting ground. The structures imposed on them — Boolean (Z₂⁶) and cyclic (Z₅) — are algebraically incompatible. The productive content lives in the interference pattern, not in either structure alone.

Evidence for C is now overwhelming: the dimensional forcing theorem (§3) shows that n=3 is the unique dimension where the bridge is forced to create singletons. The bridge MUST be lossy (fibers, not bijection) because coprime group orders prevent homomorphism. Yet the singletons at Fire/Water create injection points where both systems agree — and these are exactly the 互 cycle attractors. The interference pattern is not an accident; it's the mechanism.

### Status: OPEN

This question is well-posed but interpretive. The computational program mapped all four incommensurabilities (§4), proved the bridge structure (§3, §5), and derived every parameter (derivation.md). What remains is whether "the interference pattern IS the structure" (option C) constitutes a satisfactory mathematical answer or merely describes one. This is a question about mathematical ontology, not computation.

---

## 2. Why do the two Z₅ structures agree? [RESOLVED]

**Resolution: They don't agree on operations — only on the partition. Connected through 後天, not algebra.**

The arithmetic Z₅ (He Tu, counting numbers mod 5) and the structural Z₅ (trigram binary geometry → {2,2,2,1,1} partition) produce the same 5 elements through different mechanisms.

The R32 computation (deep/01_assignment_test.py) proved:

- **The two Z₅ structures are genuinely incommensurable.** Both generate D₅ under ⟨σ, π⟩, but complement π is affine (-x mod 5) on the 生-cycle ring and non-affine on the He Tu ring. Exhaustive search of all 25 affine maps confirms no match.
- The conjugation γ = [3,2,0,4,1] is not affine — a pure permutation with no algebraic structure.
- γ does NOT preserve Z₅ cyclic distance: d(0,3)=2 but d(γ(0),γ(3))=d(3,4)=1. Incommensurable as metric spaces too.
- The He Tu Z₅ is spatial (compass directions). The 生-cycle Z₅ is relational (dynamics). Connected through the 後天 compass arrangement (a conventional bridge, not a forced one).

**References:** 01_assignment_test.py (Finding 1), exploration-log.md (Iteration 1)

---

## 3. What is the 3×5 grid? [RESOLVED]

**Resolution: Null discriminative power for the middle coordinate.**

The Z₅ × Z₅ × Z₅ projection (lower_element × hu_relation × upper_element): 43/125 cells realized, 82 forbidden. But hu_relation adds NO textual discriminative power: χ² p=0.731 for 吉 across 5 hu_relation categories.

The nuclear relation (互) constrains which cells are structurally occupied but carries no independent semantic signal. Meaning lives on the Z₅ quotient (directed relation), not on finer coordinates.

**References:** 01_assignment_test.py (Finding 4), exploration-log.md (Iteration 1)

---

## 4. Is incommensurability the mechanism? [OPEN]

The deep exploration mapped four nested incommensurabilities:

| Layer | Gap | Bridge | Status |
|---|---|---|---|
| Z₂ vs Z₅ | Binary vs pentadic | Complement (unique cross-framework involution) | Bridged |
| He Tu Z₅ vs 生-cycle Z₅ | Spatial vs dynamic | 後天 compass (triple junction, not algebra) | Connected |
| 先天 vs 後天 | Z₂ optimum vs 2×3×5 junction | τ: order-4, complement-bridging, fiber-breaking | Mapped |
| Shell vs Core | Identity vs convergence | None (orthogonality wall) | Unbridged |

The computational evidence is complete: every parameter derives from the tension between incommensurable structures. The question is whether this observation is a *fact about the system* or the *explanation of the system*.

### Status: OPEN

Well-characterized but not computationally resolvable. The claim "the system works through gaps rather than unifications" is an interpretive statement about the relationship between mathematical structure and function. The four incommensurabilities are proven; their role as mechanism is a philosophical position.

---

## 5. Complement as universal connector [RESOLVED]

**Resolution: Complement is the unique involution that simultaneously respects both number systems, and its properties force the dimensional constraint.**

Complement (XOR with all-ones) acts as:
- **In Z₂**: Bit-flip involution on all bits simultaneously
- **In Z₅**: The anti-automorphism π = -x mod 5 (negation on the 生-cycle ring)
- **In 先天**: Rotation by π (180°) — all 4 complement pairs diametrically opposed
- **In τ**: Maps cycle 1 ↔ cycle 2 (the two 4-cycles of τ = H ∘ X⁻¹)
- **In dimensional forcing**: The constraint f(x̄) = -f(x) mod 5 is what creates the 3-destination structure on complement pairs, which forces singletons at n=3

Complement is the ONLY involution that transfers cleanly between Z₂ and Z₅. Every other transformation (互, 變, seasonal access, 生克) is native to one framework and degraded in the other. Complement threads through all four incommensurability layers.

**References:** 01_assignment_test.py (complement=negation), 02_arrangements.py (先天 complement geometry), 03_prime_decomposition.py (τ complement-bridging), 04_dimensional_forcing.py (complement in dimensional constraint)

---

## 6. The 後天 arrangement as mathematical object [RESOLVED]

**Resolution: The 後天 is the unique arrangement satisfying three constraints corresponding to primes 2, 3, and 5. It is the unique triple junction of all three structural primes.**

Among 96 cardinal-aligned arrangements, the 後天 is uniquely determined by:

| Stage | Constraint | Prime | Survivors | What it determines |
|---|---|---|---|---|
| 0 | Cardinal alignment (He Tu) | — | 96 | Fixed frame |
| 1 | 生-monotonicity + element pair coherence | 5 | 8 | Which elements go where (Z₅ fiber geometry) |
| 2 | Cardinal yin/yang balance [1,1,2,2] | 2 | 2 | Polarity at cardinal positions |
| 3 | Sons (震坎艮 = Z₂³ standard basis) at N/NE/E | 3 | 1 | Line-position ordering on compass |

The 8 survivors after stage 1 form an exact Z₂³ = 2×2×2 product:
- Choice A: which Wood at E (震 vs 巽)
- Choice B: which Metal at W (兌 vs 乾)
- Choice C: which Earth at NE (艮 vs 坤)

**Z₅ metrics are identical across all 8 survivors** — the residual Z₂³ is orthogonal to Z₅. Primes 2 and 3 resolve degrees of freedom that prime 5 cannot see.

The sole competitor (arr_037, "anti-後天") differs only at NE/SW (艮↔坤 swapped), inverting the generational flow. It is not historically attested.

**先天 comparison:** 先天 is the unique Z₂ champion (complement_diameter=4/4, Z₂ composite=6/6). It CANNOT be cardinal-aligned — Z₂ optimality requires sacrificing Z₅ alignment entirely. The gap (6 vs max 3) proves the fundamental incompatibility.

**τ = H ∘ X⁻¹:** Two 4-cycles (坤→坎→兌→巽)(震→艮→乾→離), order 4. Complement maps cycle 1 ↔ cycle 2. Fiber-breaking, non-geometric. Cross-cuts all structure because it translates between genuinely incommensurable embeddings.

**References:** 02_arrangements.py, 03_prime_decomposition.py, exploration-log.md (Iterations 2-3)

---

## 7. The 說卦傳 sequence [OPEN]

The 說卦傳 describes the 後天 arrangement as a temporal/seasonal sequence: "帝出乎震" (the sovereign emerges from 震/East/Spring), proceeding clockwise through the year. This is the textual source for the arrangement's intercardinal positions.

The deep exploration proved the 後天 is mathematically forced by three structural constraints (§6), but the 說卦傳 provides an independent, non-mathematical rationale grounded in seasonal observation and cosmological narrative.

### What we don't know

1. Does the 說卦傳 sequence encode mathematical structure not captured by the compass metrics? (The sequential ordering was found algebraically random, p=0.76, in the atlas.)
2. Is there a formal relationship between the narrative structure ("emerges from 震, works in 離, receives from 坤...") and the prime-3 constraint (sons at N/NE/E)?
3. Historical: when did the 後天 arrangement crystallize? Is there textual evidence of alternative arrangements being considered and rejected?

### Status: OPEN

Requires Chinese textual analysis and historical philology — a different methodology from computational structural analysis. The computational program provides the *that* (the 後天 is forced by three primes), but the 說卦傳 may provide the *why* in culturally grounded terms.
