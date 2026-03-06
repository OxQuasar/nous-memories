# The Trigram Relational Space: Invariant Characterization

## 1. The Question

Multiple independent coordinate systems — binary algebra (Z₂³), Lo Shu (number-theoretic), five phases (elemental/cyclic), He Tu (directional pairing) — all produce consistent assignments when mapped onto the 8 trigrams. Yet no direct bridge exists between any two of them: Lo Shu numbers don't translate to XOR operations, five-phase cycles don't reduce to Hamming distances. They agree only *through* the trigram intermediary.

**What is the underlying relational space they all coordinatize?** State it without reference to any particular coordinate system.

---

## 2. The Coordinate Systems and Their Known Properties

### Binary / Z₂³ (Fu Xi)

The 8 trigrams are the elements of the group Z₂³ = {0,1}³. Each trigram is a 3-bit string; yin = 0, yang = 1.

| Trigram | Binary | Yang count | Fu Xi # |
|---------|--------|------------|---------|
| Qian | 111 | 3 | 1 |
| Dui | 110 | 2 | 2 |
| Li | 101 | 2 | 3 |
| Zhen | 100 | 1 | 4 |
| Xun | 011 | 2 | 5 |
| Kan | 010 | 1 | 6 |
| Gen | 001 | 1 | 7 |
| Kun | 000 | 0 | 8 |

The Fu Xi arrangement pairs each trigram with its bitwise complement (XOR 111). All 4 pairs have Hamming distance 3. Fu Xi numbering is reverse binary counting.

### Lo Shu / King Wen Circle

The Lo Shu magic square assigns numbers 1–9 to a 3×3 grid (5 at center). The 8 outer cells map to the 8 trigrams on the KW Later Heaven circle:

```
  4(Xun/SE)   9(Li/S)    2(Kun/SW)
  3(Zhen/E)   5(center)   7(Dui/W)
  8(Gen/NE)   1(Kan/N)    6(Qian/NW)
```

Diametric pairs on the KW circle correspond exactly to pairs summing to 10 through center 5. The KW circle and Lo Shu perimeter are the same ordering. Rows, columns, and diagonals of the Lo Shu sum to 15.

### Five Phases / 五行

The trigrams partition into 5 elements (partition shape 2,2,2,1,1):

| Element | Trigrams | Direction |
|---------|----------|-----------|
| Metal (金) | Qian, Dui | West |
| Wood (木) | Zhen, Xun | East |
| Earth (土) | Kun, Gen | Center/NE-SW |
| Fire (火) | Li | South |
| Water (水) | Kan | North |

The five elements interact through two directed 5-cycles: 生 (generation: Wood→Fire→Earth→Metal→Water→Wood) and 克 (overcoming: Wood→Earth→Water→Fire→Metal→Wood).

### He Tu / 河图

The He Tu pairs numbers differing by 5, associating yang and yin aspects of the same directional element:

| He Tu pair | Trigrams | Element | XOR mask | Hamming |
|------------|----------|---------|----------|---------|
| (1, 6) | Kan ↔ Qian | Water/Metal | 101 | 2 |
| (2, 7) | Kun ↔ Dui | Earth/Metal | 110 | 2 |
| (3, 8) | Zhen ↔ Gen | Wood/Earth | 101 | 2 |
| (4, 9) | Xun ↔ Li | Wood/Fire | 110 | 2 |

All He Tu pairs have Hamming distance exactly 2. The He Tu pairs cross elements with a specific 生克 signature: 3 生 relationships + 1 克.

---

## 3. The Invariant Catalog

Four rounds of computation and evaluation produced a three-tier catalog: coordinate-free invariants, coordinate-dependent properties, and system-specific features.

### Tier 1: Coordinate-free invariants (survive cross-system filtering)

**I1. Three distinguished fixed-point-free involutions.**
Each of the three traditional pairing systems — Fu Xi complement (ι₁), KW/Lo Shu diametric (ι₂), He Tu differ-by-5 (ι₃) — is a fixed-point-free involution on 8 elements, partitioning them into 4 disjoint pairs.

*Status: Theorem.* Each system's opposition rule is computationally verified to be an involution without fixed points.

**I2. The three involutions generate S₄ on a unique block system.**
The group G = ⟨ι₁, ι₂, ι₃⟩ has order 24 and is isomorphic to S₄ (the symmetric group on 4 objects). G acts on the 8 elements through a unique system of imprimitivity: 4 blocks of 2. The blocks are {Kun,Zhen}, {Gen,Dui}, {Kan,Li}, {Xun,Qian}.

*Status: Theorem.* Verified by exhaustive group closure (all 40,320 elements of S₈ checked). The group has trivial center, derived subgroup A₄, abelianization Z₂. The block action is faithful.

**I3. Internal group hierarchy: V₄ ◁ S₄.**
ι₂ and ι₃ commute (ι₂∘ι₃ has order 2), generating a Klein four-group V₄ = {id, ι₂, ι₃, ι₂∘ι₃}. Adding ι₁ extends V₄ to the full S₄. The fourth element τ = ι₂∘ι₃ is itself a fixed-point-free involution whose 4 pairs are exactly the 4 blocks.

V₄ is a normal subgroup of G. The quotient G/V₄ ≅ S₃.

*Status: Theorem.* Direct computation of products and closure.

**I4. Generator conjugacy-class separation.**
ι₁ and ι₂ lie in the same conjugacy class within G (class C₂, containing 6 elements — they act as transpositions on blocks while also swapping within certain blocks). ι₃ lies in a different conjugacy class (class C₄, containing 3 elements — it permutes blocks without any within-block swapping).

This means ι₃ (He Tu) is structurally non-interchangeable with ι₁ and ι₂. It is the only generator that acts purely at the block level, preserving the internal structure of every pair.

*Status: Theorem.* Conjugacy class computation within G.

**I5. Pair overlap pattern.**
|pairs(ι₁) ∩ pairs(ι₂)| = 1 (the shared pair is {Kan, Li}).
|pairs(ι₁) ∩ pairs(ι₃)| = 0.
|pairs(ι₂) ∩ pairs(ι₃)| = 0.

The shared pair {Kan, Li} constitutes one of the four blocks. This block is distinguished: it is the unique block that appears as a pair in more than one generator.

*Status: Theorem.* Direct computation of pair sets.

**I6. Product-order fingerprint.**
The pairwise products of generators have orders:
- ord(ι₁ ∘ ι₂) = 3 (cycle structure: two 3-cycles + two fixed points on blocks)
- ord(ι₁ ∘ ι₃) = 4 (cycle structure: two 4-cycles)
- ord(ι₂ ∘ ι₃) = 2 (the fourth involution τ)

The unordered multiset {2, 3, 4} of product orders is a coordinate-free fingerprint of how the three generators sit inside S₄.

*Status: Theorem.* Direct computation.

**I7. Polarity partition (with Axiom 3).**
The 8 elements admit a balanced partition P₊/P₋ (4 elements each) with the following properties:
- P₊ = {Kan, Zhen, Dui, Li} (Lo Shu odd / cardinal directions / KW even positions)
- P₋ = {Kun, Gen, Qian, Xun} (Lo Shu even / intercardinal / KW odd positions)
- This partition does NOT coincide with binary weight parity (yang-count ≥ 2 vs ≤ 1). Binary weight gives {Qian, Dui, Li, Xun} as yang-dominant, swapping {Kan, Zhen} ↔ {Qian, Xun}.
- The shared pair {Kan, Li} lies entirely within P₊.

The polarity partition is external to the involution structure — it cannot be derived from ι₁, ι₂, ι₃ alone. It requires the number system (Lo Shu), the spatial system (directions), or an explicit orientation axiom.

*Status: Observation (the partition exists and is consistent across Lo Shu, directional, and KW-positional systems). The claim that it is irreducible to the involution structure is a theorem (Aut from involutions alone is Z₂, not trivial).*

### Tier 2: Coordinate-dependent properties (require Z₂³ labeling)

**D1. Hamming profile stratification.**
Under the standard binary encoding, the three involutions produce three distinct Hamming profiles:
- ι₁ (Fu Xi): all pairs at distance 3, profile (3,3,3,3). Maximum strength, zero diversity.
- ι₂ (KW): distances (3,1,1,1), using all 4 nonzero XOR masks. Maximum diversity.
- ι₃ (He Tu): all pairs at distance 2, profile (2,2,2,2). Uniform intermediate.

*Status: Observation, coordinate-dependent.* The profiles are properties of the involutions composed with a specific Z₂³ isomorphism. A different isomorphism between the trigram set and the cube would produce different profiles for the same abstract involutions. However, the null model shows this specific profile triple is rare (p = 3.84 × 10⁻⁴ among all triples of FPF involutions on Z₂³), providing evidence that the Z₂³ coordinatization is non-trivially chosen.

**D2. XOR mask coverage (slot decomposition).**
Under the standard binary encoding:
- ι₂ (KW) masks: {001, 010, 100, 111} = {e₁, e₂, e₃, e₁+e₂+e₃} — a basis of Z₂³ plus the all-ones vector.
- ι₃ (He Tu) masks: {101, 110} = {e₁+e₃, e₁+e₂} — 2-sums involving the first basis vector.
- Together they use 6 of 7 nonzero elements of Z₂³. The missing mask is 011 = e₂+e₃ — the unique 2-sum not involving e₁.

*Status: Observation, coordinate-dependent.* Requires not just *a* Z₂³ labeling but the traditional one. The structure is sensitive to which bit is L1, L2, L3.

**D3. Statistical rarity of the Hamming triple.**
The Hamming profile triple {(3,3,3,3), (2,2,2,2), (1,1,1,3)} occurs in only 72 of 187,460 possible triples of FPF involutions on Z₂³ (p = 3.84 × 10⁻⁴). Under a pairwise-disjointness constraint, p = 0 — no fully disjoint triple achieves this profile. The traditional system achieves it by sharing exactly one pair (Li↔Kan between ι₁ and ι₂).

*Status: Observation, coordinate-dependent.* The entire null model is defined inside Z₂³. It characterizes the coordinatization, not the abstract space.

### Tier 3: System-specific features

**S1. Central element.** Lo Shu 5 / Five-Phase Earth. Present in Lo Shu and Five-Phase systems, absent from binary algebra. Earth carries the magic constant: {2, 5, 8} sum to 15.

**S2. Five-phase partition.** The (2,2,2,1,1) partition into elements with directed 生/克 cycles. The partition shape has no binary analog. The traditional element assignment maximizes partition cleanness (top 13.3% of 50,400 valid surjections).

**S3. Magic square constraint.** Lo Shu rows/columns/diagonals sum to 15. This is a property of the number labeling, not the abstract structure.

**S4. Flying star path regularity.** The Lo Shu traversal (5→6→7→8→9→1→2→3→4) has constant consecutive mask distance of exactly 2 — zero variance. This maximizes uniformity of transition character.

---

## 4. Coordinate-Free Axioms for the Underlying Space

**Theorem.** The following two axioms on three fixed-point-free involutions on an 8-element set determine a unique structure up to isomorphism:

**Axiom 1 (Overlap).** Three fixed-point-free involutions ι₁, ι₂, ι₃ on an 8-element set S satisfy:
- |pairs(ι₁) ∩ pairs(ι₂)| = 1
- |pairs(ι₁) ∩ pairs(ι₃)| = 0
- |pairs(ι₂) ∩ pairs(ι₃)| = 0

**Axiom 2 (Commutation).** ι₂ ∘ ι₃ has order 2.

**Everything else follows:**
- G = ⟨ι₁, ι₂, ι₃⟩ ≅ S₄ (order 24)
- G acts on a unique block system of 4 blocks of 2
- The blocks are the pairs of τ = ι₂ ∘ ι₃
- Product orders: ord(ι₁∘ι₂) = 3, ord(ι₁∘ι₃) = 4
- ι₃ lies in the normal V₄ of S₄; ι₁ and ι₂ do not
- The derived subgroup is A₄; the abelianization is Z₂
- Aut = Z₂ (the non-trivial automorphism is τ itself)

*Proof method: Exhaustive enumeration.* All 105 fixed-point-free involutions on {0,...,7} were generated. All C(105,3) = 187,460 ordered triples were tested against both axioms. Survivors were classified up to S₈-conjugacy. Result: exactly one isomorphism class.

*Axiom independence:* Neither axiom is derivable from the other. Removing Axiom 1 admits overlap patterns other than (1,0,0). Removing Axiom 2 admits products ι₂∘ι₃ of order 4, doubling the solution count.

**Optional Axiom 3 (Orientation).** S admits a balanced partition P₊/P₋ (|P₊| = |P₋| = 4) such that the unique shared pair of ι₁ and ι₂ lies entirely within P₊.

With Axiom 3: Aut = {id}. The structure is fully rigid — every element is uniquely determined.

---

## 5. Uniqueness

**Theorem.** Under Axioms 1–2, there is exactly one isomorphism class of triples (ι₁, ι₂, ι₃) on 8 elements. The automorphism group of the structure is Z₂, generated by the derived involution τ = ι₂∘ι₃.

**With Axiom 3:** The automorphism group is trivial. The structure is rigid.

**Symmetry breakdown by data layer:**

| Data included | Aut order | Group |
|--------------|-----------|-------|
| Hamming metric only (cube) | 48 | Aut(Z₂³) |
| + Involution memberships | 2 | Z₂ |
| + Five-phase assignments | 1 | {id} |
| + Z₂³ Hamming data | 1 | {id} |

Both the five-phase layer and the Z₂³ layer independently break the last Z₂ symmetry. They break the *same* symmetry: the non-trivial automorphism τ = ι₂∘ι₃ is non-affine on Z₂³ (so it's ruled out by the binary structure) and it disrupts the 生/克 cycle assignments (so it's ruled out by the five-phase structure). Both layers carry the same one bit of orientation information.

---

## 6. Extension to n=6

*(Full analysis in [q3-cross-scale.md](q3-cross-scale.md).)*

The n=3 characterization does not directly extend to n=6. The two scales share a common algebraic skeleton but diverge in their pairing logic due to parity.

### The n=6 group structure

The three basic involutions on 64 hexagrams — complement (σ₁), reversal (σ₂), comp∘rev (σ₃) — all commute, generating only V₄ (trivially forced at any bit length). The structurally interesting group is **G₃₈₄ = (Z₂ ≀ S₃) × Z₂³** (order 384), generated by three layers:

1. **Mirror-pair XOR masks** T = ⟨O, M, I⟩ ≅ Z₂³: flip values within each of the 3 mirror pairs {L1,L6}, {L2,L5}, {L3,L4}. Note: O ⊕ M ⊕ I = complement.
2. **Within-pair position swaps** ≅ Z₂³: exchange positions within each mirror pair.
3. **Pair permutations** ≅ S₃: permute the 3 mirror pairs as units.

Layers 1 and 2 commute, giving the kernel K = T × ⟨swaps⟩ ≅ Z₂⁶ (order 64, normal). The short exact sequence: 1 → K ≅ Z₂⁶ → G₃₈₄ → S₃ → 1.

### The block system and 9 pairings

T acts freely on 64 hexagrams, producing 8 orbits of size 8 indexed by the **mirror-pair residual** φ(h) = (L1⊕L6, L2⊕L5, L3⊕L4) ∈ Z₂³. S₃ merges these by Hamming weight into 4 macro-orbits:

| Macro-orbit | Size | Residual weight | Pairing |
|-------------|------|-----------------|---------|
| A (palindromes) | 8 | 0 | Forced (complement) |
| B (anti-palindromes) | 8 | 3 | Forced (complement) |
| C | 24 | 1 | 3 choices |
| D | 24 | 2 | 3 choices |

Total equivariant pairings: 1 × 1 × 3 × 3 = **9**. KW is pairing #1 (rev/rev): the unique minimizer of weight tilt (WT = 0.375, threefold gap to next-best 1.125).

### KW ∉ G₃₈₄

The KW pairing (reversal where possible, complement for palindromes) is NOT a group element — verified computationally. It applies σ₂ on 48 hexagrams and σ₁ on 16, selecting between operations based on palindromicity. The three pure involutions σ₁, σ₂, σ₃ are all in G₃₈₄, but none is the KW pairing. KW is equivariant *under* G₃₈₄ without being *in* it.

### Cross-scale comparison

| | n=3 | n=6 |
|---|---|---|
| Translation group T | Z₂³ (regular rep on 8) | Z₂³ (index-8 subgroup of Z₂⁶) |
| Quotient action | S₃ (within S₄ on 4 blocks) | S₃ (on 8 T-orbits → 4 macro-orbits) |
| Equivariant pairings | 9 | 9 |
| Traditional pairing | Complement (ι₁) — **in group** | KW hybrid — **not in group** |
| Selection criterion | Max strength (S) | Min weight tilt (WT) |

The 3² = 9 count arises at both scales from the same mechanism: 2 free components × 3 involution choices. The divergence is forced by parity: at odd n, complement is simultaneously FPF, a group element, and strongest — no tradeoff exists. At even n, parity creates palindromic fixed points, forcing a choice between algebraic purity and weight preservation that the tradition resolves in favor of weight preservation.

### Structural argument for n=6

n=6 is the minimum even length where the constraint space is tight. At n=4 (2 mirror pairs), 117 equivariant pairings exist — too many for unique selection. At n=6 (3 mirror pairs), S₃ creates the precise 4-macro-orbit structure yielding 9 pairings with a unique WT-minimizer. The threshold is 3 mirror pairs — the minimum for S₃ to act non-trivially on the residual Z₂³.

---

## 7. What the Characterization Explains

### Why the coordinate systems agree

The coordinate systems agree because the underlying structure is almost rigid (Aut = Z₂). Once the single orientation bit is fixed, every element is uniquely determined by its relational fingerprint — its pattern of memberships across the three involutions plus its polarity class. Any faithful coordinatization must land on the same rigid structure.

Concretely:
- The Lo Shu magic square constraint (sum-to-15, sum-to-10) is *consistent with* the involution structure but does not generate it. The Lo Shu labels the structure with numbers that happen to satisfy additional arithmetic constraints.
- The five-phase directed cycles (生/克) provide the orientation bit that breaks the Z₂ ambiguity. They also introduce the (2,2,2,1,1) partition — a finer structure than the involutions alone provide — but this is compatible with, not derivable from, the involution axioms.
- The binary algebra (Z₂³) provides both a metric (Hamming) and a group structure (XOR). The metric characterizes *how* each involution pairs elements — but this is information about the coordinatization, not the abstract space.

### Why no direct bridge exists between systems

The systems coordinatize orthogonal aspects of the same rigid object. Lo Shu captures number-theoretic structure (sums, differences). Binary captures algebraic structure (group operations, Hamming metric). Five phases capture directed interaction structure (生/克 cycles). He Tu captures the "clean" involution — the one that acts on blocks without internal disruption.

These are genuinely different projections, like longitude, latitude, and altitude describe the same point without being reducible to each other. The distance correlations confirm this: among the 28 pairwise trigram relations, only Hamming↔FuXi arc (ρ = 0.654, tautological — Fu Xi *is* binary counting) and KW arc↔HeTu (ρ = 0.525) are significant. All other cross-system distance correlations are non-significant.

---

## 8. What the Characterization Doesn't Explain

### Honest boundaries

1. **Why this particular S₄.** The axioms uniquely determine the structure, but they don't explain *why* these axioms rather than others. The overlap pattern (1,0,0) and the commutation condition are sufficient constraints — but are they natural, or artifacts of the decomposition into three named systems?

2. **The missing mask.** The nonzero element e₂+e₃ = 011 of Z₂³ is the only one not used by any involution pair at n=3. Whether this gap is a structural consequence of the S₄ action (forced by the block system), or carries additional meaning, is unknown. (At n=6, KW uses all 7 nonzero mirror-pair masks — the mask vocabulary is saturated.)

3. **The polarity partition's origin.** The partition P₊/P₋ is consistent across three independent systems (Lo Shu odd, cardinal directions, KW even positions) but cannot be derived from the involution structure. Why these three systems independently produce the same partition is unexplained. (Q4 confirmed no additional traditional system provides an independent path to P₊/P₋.)

4. **Referential status.** The characterization says *what* the structure is (a rigid combinatorial object) but not *what it is for*. The tradition treats these 8 states as isomorphic to relational patterns in events. Whether that isomorphism has empirical content is outside this analysis.

5. **HeTu's privileged role.** ι₃ (He Tu) is the only generator in the normal V₄, acting purely at the block level. This is a mathematical fact with possible interpretive significance (He Tu as the most "primordial" or structurally conservative pairing), but that significance has not been tested.

---

## 9. Implications for Approaches 2 and 3

### Approach 2: Fourth Coordinate System

*(Completed in [q4-coordinate-systems.md](q4-coordinate-systems.md).)* Additional traditional systems (天干, 地支 六冲/六合/三合) are compatible with the S₄ block structure but carry no independent structural information beyond the element/direction assignments. The polarity partition P₊/P₋ is not independently recoverable without routing through compass geometry.

### Approach 3: Operational Probe via Divination

The characterization provides a coordinate-free framework for analyzing the Meihua evaluation circuit (本→互→变):
- Each step of the circuit can be described as a transformation within the S₄ structure.
- The 体/用 projection samples every ordered trigram pair exactly 6 times (uniform sampling theorem — proved in Phase 4 of the opposition theory).
- The five-phase evaluation at each step is a readout of how the current state sits relative to the (2,2,2,1,1) partition.

The key question: is there a coordinate-free quantity conserved or systematically transformed along the evaluation path? The current analysis found that the circuit produces non-redundant readings 94.8% of the time (all three evaluations differ in 42.7% of states, all agree in only 5.2%), but did not identify a conserved quantity.

---

## 10. Open Questions

1. **Axiom unification.** Can the two axioms (overlap pattern + commutation) be derived from a single geometric or algebraic principle? The compression from five axioms to two was achieved; compression to one was not attempted.

2. ~~**The missing mask in Z₂³.**~~ **Resolved.** The absence of mask 011 from the three generators is NOT forced by the axioms. Exhaustive enumeration of all 7,560 valid triples shows: 82.7% use mask 011, 20% use all 7 masks with nothing missing, and each mask has roughly equal probability (~500 triples) of being the one omitted. The missing mask is a coincidence of the specific realization, not a structural necessity. Furthermore, the full S₄ group generated by the traditional triple DOES use mask 011 (9 of 24 elements) — it is absent only from the generators, not from the group they generate.

3. ~~**n=6 triple-involution analysis.**~~ **Resolved (Q3).** The n=3 characterization does not have a direct analog at n=6. The three basic involutions generate only V₄ (trivially forced). The structural analog is the 384-element mirror-pair group G₃₈₄ with S₃ quotient, yielding 9 equivariant pairings. See [q3-cross-scale.md](q3-cross-scale.md).

4. ~~**Additional coordinate systems.**~~ **Resolved (Q4).** No additional traditional system tested produces a new involution or an independent determination of P₊/P₋. The two-axiom characterization remains minimal and complete. See [q4-coordinate-systems.md](q4-coordinate-systems.md).

5. **The polarity partition as a consequence.** Is there a deeper structural principle from which the P₊/P₋ partition follows, making Axiom 3 derivable rather than postulated? (Q4 showed it is irreducibly spatial in the traditional systems.)

6. ~~**Cross-scale bridge.**~~ **Partially resolved (Q3).** The divergence is an irreducible geometric fork forced by parity: at n=3, no tradeoff exists between strength, group membership, and weight preservation. At n=6, parity creates palindromic fixed points that force a choice. The shared structure is the 3² = 9 counting mechanism; the selection criteria diverge. See [q3-cross-scale.md](q3-cross-scale.md).

7. **Wood anomaly.** Zhen (100) and Xun (011) are the only intra-element pair that are also binary complements (Hamming distance 3). All other dual-trigram elements pair at distance 1. Does this connect to the 克 edge variance (96.2nd percentile) in the five-phase assignment?

---

## Summary

The underlying relational space of the I Ching trigram system is characterized by two axioms on three fixed-point-free involutions:

> **An 8-element set with three distinguished involutions, two of which commute, the third sharing exactly one pair with one of them and none with the other.**

This determines a unique structure (up to one binary orientation choice) isomorphic to S₄ acting faithfully on 4 blocks of 2 elements each. The structure is almost rigid: Aut = Z₂ from the involution data alone; full rigidity requires a polarity partition that both the algebraic (Z₂³) and elemental (五行) layers independently provide.

The coordinate systems are faithful but partial views of this rigid object. They agree not because they are reducible to each other, but because the object they all describe admits at most two self-maps. The algebraic layer (Z₂³) is not merely a coordinate system — it carries exactly one essential bit of information (orientation) beyond what the involution structure provides. Everything else in Z₂³ (Hamming distances, slot decomposition) is coordinatization-specific.

At n=6, the analogous structure is G₃₈₄ = (Z₂ ≀ S₃) × Z₂³, which constrains the pairing space from ~10¹⁷ to exactly 9 equivariant pairings. The KW pairing is the unique weight-tilt minimizer among these 9, but lies outside the group — a sentence composed from the group's vocabulary that isn't itself a word. The cross-scale divergence (complement at n=3, reversal-hybrid at n=6) is forced by parity, and n=6 is the minimum even length where the constraint space is tight enough for unique selection.

The strongest claim the evidence supports: *the trigram relational space is a determinate mathematical object, uniquely characterized by elementary combinatorial axioms, that admits multiple faithful coordinatizations which agree by structural necessity rather than by convention or coincidence. The hexagram pairing space is a constrained extension of this object, with the KW pairing occupying a unique position defined by the conjunction of group-theoretic constraint and weight preservation.*