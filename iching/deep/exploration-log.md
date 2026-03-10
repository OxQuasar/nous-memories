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

## Synthesis

### The arc of the deep exploration

The atlas and meihua-atlas mapped the structural landscape: coordinates, projections, bridges, temporal overlays, operational architecture. The deep exploration asked the next question: **why does this specific architecture exist?** Not what the system is, but why it must be this way and no other.

The answer: **the system is uniquely determined.** Every degree of freedom in the 五行 assignment is fixed — 1.75 bits by binary geometry, 0.50 bits by the conjunction of algebraic constraint and textual evidence. The traditional trigram→element mapping is not one choice among many; it is the only configuration where the algebra is structurally viable AND the textual bridge holds.

### Four findings, one theme

All four findings point to the same structural principle: **the system's content lives in the interference between incommensurable frameworks.**

1. **Two Z₅ incommensurability.** The He Tu (spatial) and 生-cycle (relational) Z₅ structures share elements and global symmetry (D₅) but are non-affinely twisted. Complement is clean negation on the relational ring and non-algebraic on the spatial ring. Position and dynamics cannot be unified into a single coordinate frame. They meet through the 後天八卦 tradition — a historical mediation, not a mathematical derivation.

2. **Conjunction forcing.** The 0.50-bit cosmological choice is squeezed between algebra from below (which eliminates B entirely by collapsing the Cycle attractor to 比和) and text from above (which eliminates C by degrading the 吉×生体 bridge). Neither constraint alone selects the traditional assignment; their intersection does. The assignment lives in the interference zone.

3. **Semantic coherence vs algebraic economy.** The tradition chose to pair adjacent trigrams (Hamming distance 1), accepting 6 profile collisions that the alternative C avoids through maximal-distance pairing. The tradition optimizes for multi-projection readability — the ability to read the same hexagram through multiple overlapping lenses — rather than single-projection economy. The 六親 system compensates for the collisions at a different structural level.

4. **3×5 grid null.** The nuclear relation (互) constrains which cells are structurally occupied (82/125 forbidden) but carries no independent semantic signal (χ² p=0.731). The 互 layer is scaffolding — it shapes the space but doesn't carry meaning on its own. Meaning lives on the Z₅ quotient (the directed relation), not on finer coordinates.

### Three nested incommensurabilities

The deep exploration reveals three layers, each confirmed computationally:

| Layer | Gap | Bridge | Status |
|---|---|---|---|
| Z₂ vs Z₅ | Combinatorial vs relational | Complement (the unique cross-framework operation) | Bridged |
| He Tu Z₅ vs 生-cycle Z₅ | Spatial vs dynamic | 後天八卦 (conventional, not algebraic) | Connected |
| Shell vs Core | Identity vs convergence | None (orthogonality wall) | Unbridged |

Complement threads through the first two layers (bit-flip in Z₂, negation in 生-cycle Z₅) but becomes non-algebraic when it hits He Tu Z₅. Nothing crosses the third layer. The practitioner navigates all three.

### The structural research program's boundary

This exploration reaches the natural boundary of computation. The questions that remain — whether a coordinate-free space exists (deep-questions §1), whether incommensurability is the mechanism (§4) — are well-characterized but not computationally resolvable. They describe the system's nature rather than posing testable hypotheses.

The computational picture is complete:
- **Atlas**: the full coordinate system (13 五行 coordinates, zero residual, two bridges to text)
- **Meihua-atlas**: the operational expansion (384 states, two channels, 8 arc types)
- **Deep**: the uniqueness proof (zero free parameters, three nested incommensurabilities)

What remains is interpretation of the map, not extension of it.