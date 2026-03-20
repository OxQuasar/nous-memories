# 五行 Structural Analysis — Findings

> **Bit convention A:** b₀ = bottom line, b₂ = top line.

## 1. The 五行 Assignment

The traditional 五行 (Wuxing) system assigns each of the 8 trigrams to one of 5 elements. Using the encoding b₀=bottom line, b₂=top line:

| Element | Trigrams | Bit values | Class size |
|---------|----------|------------|------------|
| Earth 土 | Kun ☷, Gen ☶ | 000, 100 | 2 |
| Metal 金 | Dui ☱, Qian ☰ | 011, 111 | 2 |
| Wood 木 | Zhen ☳, Xun ☴ | 001, 110 | 2 |
| Fire 火 | Li ☲ | 101 | 1 |
| Water 水 | Kan ☵ | 010 | 1 |

The partition has shape {2, 2, 2, 1, 1}. The two singletons — Fire and Water — are mutual complements (010 ⊕ 101 = 111). This assignment is the standard one found across classical Chinese sources; it is not derived here but taken as given and analyzed.

### Complement pairing within 五行

Only Wood has both members of a complement pair in the same class: Zhen(001) ⊕ Xun(110) = 111. Fire and Water are cross-class complements. Earth and Metal pair across classes: Kun(000)↔Qian(111), Dui(011)↔Gen(100).

---

## 2. Geometry on Z₂³

**Status: proven.** All statements in this section follow from the bit encoding and element assignment by direct computation.

### Element classes as geometric objects on the 3-cube

| Type | Elements | Intra-class XOR | Hamming d | Geometric character |
|------|----------|-----------------|-----------|---------------------|
| Edge pair | Earth {000, 100} | 100 | 1 | Differ in bit 2 only |
| Edge pair | Metal {011, 111} | 100 | 1 | Differ in bit 2 only |
| Body diagonal | Wood {001, 110} | 111 | 3 | Complement pair (antipodal) |
| Singleton | Fire {101} | — | — | — |
| Singleton | Water {010} | — | — | — |

Earth and Metal share the same intra-class structure: both are cube edges with XOR mask 100 (bit 2 is the free variable within each). Wood is the body diagonal — the unique element whose class members are a complement pair. Fire(101) and Water(010) are mutual complements that the partition assigns to separate singleton classes.

### 生 and 克 as cube operations

Neither 生 (generation) nor 克 (overcoming) is a geometric operation on the cube. Both are geometrically irregular — they use multiple XOR masks at varying Hamming distances and cannot be expressed as any rotation, reflection, or translation of Z₂³.

The XOR masks used by each cycle:

| Category | Masks | Binary | Count |
|----------|-------|--------|-------|
| 生-exclusive | {3, 4} | {011, 100} | 2 |
| 克-exclusive | {2, 6} | {010, 110} | 2 |
| Shared | {1, 5, 7} | {001, 101, 111} | 3 |

Together: all 7 nonzero masks of Z₂³. The two cycles partition the 7 masks into {2 exclusive + 2 exclusive + 3 shared}.

### The parity separation

The 生-exclusive masks {011, 100} both preserve b₀⊕b₁ parity: XORing any trigram by 011 or 100 does not change the value of b₀⊕b₁. The 克-exclusive masks {010, 110} both break b₀⊕b₁ parity.

The b₀⊕b₁ parity itself cleanly separates element classes:
- Parity 0: {Kun, Dui, Gen, Qian} = Earth ∪ Metal
- Parity 1: {Zhen, Kan, Li, Xun} = Wood ∪ Fire ∪ Water

**生 is parity-respecting; 克 is parity-breaking.** Generation flows within the two cosets defined by this parity; overcoming crosses between them.

### No clean bit projection

五行 cannot be expressed as a function of any single bit or pair of bits. The (b₀, b₁) projection gives: (0,0)→Earth (pure), (1,1)→Metal (pure), but (0,1)→{Water, Wood} and (1,0)→{Wood, Fire} — mixed. Wood's complement structure (XOR=111, all bits toggle) is incompatible with any linear partition.

---

## 3. Element Pairs on Inner Space

**Status: proven.** The inner space has 16 states (4 inner lines of a hexagram). Each state determines a lower nuclear trigram (lines 2-3-4) and an upper nuclear trigram (lines 3-4-5), which share 2 bits. All results follow by enumeration.

### Full cross-tabulation

| v | bits | Lower nuclear | Upper nuclear | Lo elem | Up elem | Relation | Basin |
|---|------|--------------|--------------|---------|---------|----------|-------|
| 0 | 0000 | Kun(000) | Kun(000) | Earth | Earth | 比 | Kun ★ |
| 1 | 0001 | Zhen(001) | Kun(000) | Wood | Earth | 克→ | Kun |
| 2 | 0010 | Kan(010) | Zhen(001) | Water | Wood | 生→ | Cycle |
| 3 | 0011 | Dui(011) | Zhen(001) | Metal | Wood | 克→ | Cycle |
| 4 | 0100 | Gen(100) | Kan(010) | Earth | Water | 克→ | Cycle |
| 5 | 0101 | Li(101) | Kan(010) | Fire | Water | ←克 | Cycle ★ |
| 6 | 0110 | Xun(110) | Dui(011) | Wood | Metal | ←克 | Qian |
| 7 | 0111 | Qian(111) | Dui(011) | Metal | Metal | 比 | Qian |
| 8 | 1000 | Kun(000) | Gen(100) | Earth | Earth | 比 | Kun |
| 9 | 1001 | Zhen(001) | Gen(100) | Wood | Earth | 克→ | Kun |
| 10 | 1010 | Kan(010) | Li(101) | Water | Fire | 克→ | Cycle ★ |
| 11 | 1011 | Dui(011) | Li(101) | Metal | Fire | ←克 | Cycle |
| 12 | 1100 | Gen(100) | Xun(110) | Earth | Wood | ←克 | Cycle |
| 13 | 1101 | Li(101) | Xun(110) | Fire | Wood | ←生 | Cycle |
| 14 | 1110 | Xun(110) | Qian(111) | Wood | Metal | ←克 | Qian |
| 15 | 1111 | Qian(111) | Qian(111) | Metal | Metal | 比 | Qian ★ |

★ = attractor (fixed point of 互 map)

### Realization constraint

Of 25 possible (lower element, upper element) pairs, **12 are realized**, 13 are absent. The overlap constraint (nuclear trigrams share 2 bits) combined with the element assignment determines which pairs can occur.

### Basin-element structure

| Basin | States | Element pairs | Relations present |
|-------|--------|---------------|-------------------|
| Kun | 4 | Earth/Earth, Wood/Earth | 比, 克→ |
| Qian | 4 | Metal/Metal, Wood/Metal | 比, ←克 |
| Cycle | 8 | 8 distinct pairs | 生→, ←生, 克→, ←克 |

**Fixed-point basins** have only 比 (same) and 克 (overcoming) — no 生 (generation). The overlap constraint forces the upper nuclear to be element-pure within each fixed-point basin (Earth for Kun, Metal for Qian). The lower nuclear varies because one free bit (b₁) toggles between two trigrams of different elements.

**Wood as universal intruder:** In the Kun basin, the free bit toggles lower nuclear between Kun(Earth) and Zhen(Wood). In the Qian basin, it toggles between Qian(Metal) and Xun(Wood). Wood has 克 relations with both Earth (Wood克Earth) and Metal (Metal克Wood). Result: **all non-比 convergence at lower nuclear position is 克 — zero 生.**

**Cycle basin** is the only basin where generative (生) relations appear between nuclear elements.

### Convergence relation summary

| Nuclear position | 比 | 生→ | ←生 | 克→ | ←克 |
|------------------|----|-----|-----|-----|-----|
| Lower | 2 | 0 | 0 | 5 | 5 |
| Upper | 6 | 2 | 2 | 1 | 1 |

Lower nuclear convergence is entirely {比, 克}. Upper nuclear convergence is 比-dominated (6/12) with small contributions from all other types.

---

## 4. Partition Comparison

**Status: proven.** All mutual information values are exact (computed over 8 equiprobable trigrams).

### Six partitions compared

| Partition | Shape | H (bits) |
|-----------|-------|----------|
| 五行 | (2,2,2,1,1) | 2.2500 |
| Yang count | (3,3,1,1) | 1.8113 |
| Basin(TT) | (4,2,2) | 1.5000 |
| Later Heaven quadrant | (2,2,2,2) | 2.0000 |
| Complement pair | (2,2,2,2) | 2.0000 |
| b₀⊕b₁ parity | (4,4) | 1.0000 |

### Mutual information matrix

| | Wuxing | Yang | Basin | LH | Compl | Parity |
|---|---:|---:|---:|---:|---:|---:|
| Wuxing | 2.25 | 1.06 | 1.00 | 1.75 | 1.50 | 1.00 |
| Yang | 1.06 | 1.81 | 0.81 | 1.06 | 0.81 | 0.31 |
| Basin | 1.00 | 0.81 | 1.50 | 0.75 | 1.00 | **0.00** |
| LH | 1.75 | 1.06 | 0.75 | 2.00 | 1.25 | 0.50 |
| Compl | 1.50 | 0.81 | 1.00 | 1.25 | 2.00 | 1.00 |
| Parity | 1.00 | 0.31 | **0.00** | 0.50 | 1.00 | 1.00 |

### Key relationships

**Best single predictor of 五行:** Later Heaven (H(W|LH) = 0.50 bits, 77.8% captured). East=Wood and West=Metal are exact matches. The 0.50-bit residual comes from Earth being split across South(Kun) and North(Gen).

**Perfect pair predictors** (H(W|X,Y) = 0): Yang count + Complement; Basin + Later Heaven; Later Heaven + Complement; Later Heaven + Parity. 五行 is fully determined by any of these pairs.

**Complete orthogonality:** Basin(TT) ⊥ b₀⊕b₁ parity (MI = 0.000). Basin depends on (b₂, b₀) homogeneity; parity depends on b₀⊕b₁. They share b₀ but use it in structurally independent ways.

**Parity is a function of 五行:** NMI(Wuxing, parity) = 1.000. Every element class has a unique parity value. Parity 0 = {Earth, Metal}; parity 1 = {Wood, Fire, Water}.

---

## 5. Directed Graphs in Bit Space

**Status: proven.** Enumeration over all ordered pairs.

### Five-phase graphs on 8 trigrams

The 5 relation types partition the complete digraph K₈ (56 directed edges, excluding self-loops):

| Relation | Edge count | Character |
|----------|-----------|-----------|
| 比 (same element) | 6 | Intra-class |
| 生→ (generates) | 12 | Forward generation |
| ←生 (generated by) | 12 | Reverse generation |
| 克→ (overcomes) | 13 | Forward overcoming |
| ←克 (overcome by) | 13 | Reverse overcoming |

Total: 6 + 12 + 12 + 13 + 13 = 56 ✓

The asymmetry (12 生 vs 13 克 edges) arises from class sizes: 克 has one more singleton→singleton edge (Water克Fire) than 生 does, because Water→Fire is an overcoming relation while Fire→Earth is a generating relation.

### Five-phase relations along 互 convergence edges

Of the 16 inner states, 14 have non-self 互 edges (the 4 attractors map to themselves with 2 being self-identical). Along these 14 convergence edges:

| Statistic | Value |
|-----------|-------|
| 克 on ≥1 nuclear position | 12/14 (86%) |
| 生 on ≥1 nuclear position | 4/14 (29%) |
| Same relation on both positions | 4/14 (29%) |

**By basin:**
- Kun (3 edges): {(克→,比)×2, (比,比)×1}
- Qian (3 edges): {(←克,比)×2, (比,比)×1}
- Cycle (8 edges): all 8 distinct, mixing all relation types

Kun and Qian are symmetric: Kun convergence overcomes at lower nuclear (Wood克→Earth→attractor); Qian convergence is overcome at lower nuclear (Wood←克Metal→attractor). Both have upper nuclear identity (比).

### Anti-correlation of 生 and 克 across positions

The dominant combined relation types across all 240 ordered pairs on inner space are (←克, 生→) and (克→, ←生) at 14 each. **When one nuclear trigram is being overcome, the other tends to be generating.** 克 and 生 are anti-correlated across the two nuclear positions.

---

## 6. Quotient Structure: Algebraic or Cosmological?

### Symmetry group

**Status: proven** (enumeration over GL(3,F₂) and Aff(3,F₂)).

- |GL(3,F₂)| = 168 invertible linear maps
- **Linear symmetries preserving 五行 (named classes):** 1 (identity only)
- **Affine symmetries preserving 五行:** 2 (identity + translation by 100)

The sole non-trivial symmetry is x → x ⊕ 100, which swaps Kun↔Gen (within Earth) and Dui↔Qian (within Metal). This is the same bit-2 degree of freedom that makes Earth and Metal edge pairs.

**Unlabeled partition automorphisms** (allowing class relabeling): |Aut| = 8, rank 29/420 among all {2,2,2,1,1} partitions (above median of 6).

### Impossibility results

**Status: proven** (exhaustive enumeration of all relevant algebraic structures on Z₂³).

| Construction | Can produce 五行? | Reason |
|---|---|---|
| Subgroup quotient Z₂³/H | **No** | Quotients have equal-size classes; 五行 has {2,2,2,1,1} |
| Kernel of linear map | **No** | Preimages are cosets of equal size |
| Orbit of any Aff(3,F₂) element | **No** | Shape {1,1,2,2,2} not among the 8 realized orbit shapes |
| 2 Boolean functions | **No** | 2 bits give at most 4 classes; 五行 has 5 |
| 3 linear (affine) functions | **No** | Only 1 non-trivial linear function is constant on all 5 classes |
| Any number of symmetric functions | **No** | Popcount classes cross-cut 五行 |
| 3 arbitrary Boolean functions | **Yes** | Minimum sufficient |

**The boundary is sharp:** one non-linear Boolean function is both necessary and sufficient (given the 2 linear functions b₀⊕b₁ and b₀).

### The three-layer decomposition

**Status: proven** (constructive verification — reconstructed partition matches traditional assignment for all 8 trigrams).

H(五行) = 2.2500 bits, decomposing as:

| Layer | Feature | Information | Cumulative | Type |
|-------|---------|------------|------------|------|
| 1 | b₀⊕b₁ parity | 1.0000 bits | 1.0000 | Algebraic (linear) |
| 2 | b₀ within parity-0 coset | 0.7500 bits | 1.7500 | Algebraic (linear) |
| 3 | Complement pair choice in parity-1 coset | 0.5000 bits | 2.2500 | Cosmological |

**Layer 1** separates {Earth, Metal} from {Wood, Fire, Water}. This is a linear functional on Z₂³.

**Layer 2** separates Earth from Metal within the even coset. Also linear.

**Layer 3** is the sole non-algebraic input. The odd-parity coset {001, 010, 101, 110} contains exactly 2 complement pairs: {Zhen(001), Xun(110)} and {Kan(010), Li(101)}. 五行 keeps {Zhen, Xun} together (= Wood) and splits {Kan, Li} into singletons (Water, Fire). The alternative — keeping {Kan, Li} and splitting {Zhen, Xun} — is algebraically indistinguishable.

### The alternative partition

**Status: proven** (computed and compared).

The "anti-五行" (opposite Layer-3 choice) loses on every metric:

| Metric | Traditional | Alternative |
|--------|------------|-------------|
| MI(Later Heaven) | 1.7500 | 1.5000 |
| MI(Basin) | 1.0000 | 0.7500 |
| LH quadrant pairs kept | 2/4 | 1/4 |

Traditional 五行 keeps East (Zhen+Xun = Wood) and West (Dui+Qian = Metal) — the two quadrants where compass pairing coincides with element identity.

### Ranking among all {2,2,2,1,1} partitions

**Status: proven** (exhaustive enumeration of all 420 partitions).

| MI(LH) value | Count | Cumulative |
|-------------|-------|-----------|
| 2.0000 | 4 | 4 |
| **1.7500** | **24** | **28 ← 五行** |
| 1.5000 | 120 | 148 |
| 1.2500 | 272 | 420 |

五行 ranks #5 (top 1.2%) for Later Heaven alignment. The 4 partitions that rank higher all keep 3 of 4 LH quadrant pairs, but every one includes {Kun(000), Li(101)} as a pair — mixing Earth and Fire. These have maximum compass alignment but no coherent elemental interpretation.

**五行 is the most Later-Heaven-aligned partition that respects elemental identity.**

---

## 7. Relationship to I-Component Correlation

**Status: the mechanism is proven; the statistical correlation (χ²=2209) is measured.**

The I-component at the hexagram level was found to predict 生/克 relations between nuclear trigrams (χ²=2209, measured in prior work). The mechanism is now fully explained:

1. **The I-component IS b₀⊕b₁ parity** at the trigram level. This is Layer 1 of the 五行 decomposition.

2. **Layer 1 separates the XOR mask vocabularies of 生 and 克.** The 生-exclusive masks {011, 100} preserve this parity; the 克-exclusive masks {010, 110} break it.

3. Therefore, when two trigrams are connected by a 生 edge, the transition preserves b₀⊕b₁ parity. When connected by a 克 edge, the transition tends to break it.

4. At the hexagram level, the I-component aggregates this parity information over both trigram positions, producing the observed statistical correlation.

The correlation is not an independent finding — it is Layer 1 doing what Layer 1 does. The deeper patterns (克-dominated convergence in fixed-point basins, 生 confined to the Cycle, Wood as universal intruder, anti-correlation of 克/生 across nuclear positions) all follow from how this parity interacts with the overlap constraint of nuclear trigrams.

---

## 8. Conclusion: What 五行 IS, Structurally

### What it is not

五行 is not a quotient of Z₂³ by any subgroup. It is not the kernel or cokernel of any linear map. It is not an orbit of any element of Aff(3,F₂). It is not derivable from yang count or any symmetric function. Its class sizes {2,2,2,1,1} are structurally incompatible with all equal-partition mechanisms that Z₂³'s linear algebra offers.

### What it is

**五行 is a maximally compass-aligned partition of Z₂³, constrained to respect elemental identity, built from two linear features plus one non-linear cosmological binary choice.**

The algebraic skeleton (78%, 1.75 bits) determines:
- The parity split between stable elements {Earth, Metal} and dynamic elements {Wood, Fire, Water}
- The resolution of Earth vs Metal within the stable class
- The separation of 生-exclusive from 克-exclusive XOR masks
- The element-pure upper nuclear constraint in fixed-point basins
- The basin orthogonality (Basin ⊥ parity)

The cosmological input (22%, 0.50 bits) determines:
- Which complement pair in the dynamic coset stays together (Wood) vs splits (Fire, Water)
- This choice is resolved by Later Heaven compass alignment
- It cannot be derived from any linear, symmetric, or orbit-based construction on Z₂³

### Epistemic status

| Category | Claims | Status |
|----------|--------|--------|
| **Proven** | Three-layer decomposition; impossibility results; parity/XOR separation; inner-space realization; MI matrix; ranking among 420 partitions; convergence relation distribution | Exact computation over finite structures |
| **Measured** | I-component χ²=2209 correlation with 生/克 | Statistical measurement over King Wen sequence |
| **Structural interpretation** | "生 is harmonious / 克 is confrontational" as parity preservation/violation; "convergence strips, generation persists in the Cycle" | Pattern descriptions of proven facts — the interpretive framing is suggested, not proven |

The algebra and the cosmology compose without interference. The cosmological degree of freedom operates in the exact subspace the algebra leaves undetermined. Neither overrides the other. They are orthogonal inputs to a common partition.

---

## 9. Interpretive Notes: 五行 as Dynamic Character in 互 Space

### What 五行 coordinates represent in the reduction

Each node in the 16-node inner space carries an element pair (lower nuclear, upper nuclear). This pair is the qualitative readout of what remains after the 互 projection strips surface information. It encodes three things:

**The quality of the destination.** The attractors have specific element signatures: Kun=Earth/Earth, Qian=Metal/Metal (both 比和 — equilibrium), JiJi↔WeiJi=Fire/Water↔Water/Fire (mutual 克 — perpetual conflict). Fixed points are rest. The 2-cycle is irresolution.

**The friction of convergence.** Along every non-trivial convergence edge, Wood intrudes via the overlap's free bit. It creates 克 at every step toward a fixed point. The element pair at a given node tells you what destruction the next 互 step involves.

**Whether generation is possible.** 生 appears only in the Cycle basin — the basin that never resolves to a fixed point. The fixed-point basins have zero 生 along convergence. Generation and resolution are mutually exclusive.

### No generative attractor

All attractors are either static equilibrium (比和) or perpetual conflict (克↔克). No attractor has 生. Generation exists only in transit within the Cycle basin — the dynamic between nodes still converging toward the oscillation. Once you arrive, generation stops. The destination of all generative flow is conflict.

Every path through the system takes one of two forms:
- **Convergence through destruction to rest** (fixed-point basins: 克→比)
- **Generation on the way to permanent conflict** (cycle basin: 生→克↔克)

Creation is a process, never a destination.

### Wood as necessary asymmetry

Wood is structurally unique: the only complement pair in the dynamic coset, its members (Zhen=001, Xun=110) span the full cube. It intrudes into both fixed-point basins via the overlap's free bit, creating 克 where there would otherwise be only 比和. Without Wood, convergence would be frictionless — same element all the way down, static, dead. Wood is what makes convergence cost something.

Wood also holds the 生 cycle together as its hinge (Wood→Fire→Earth→Metal→Water→Wood). The cosmological choice to keep {Zhen,Xun} as one element (rather than splitting them like {Kan,Li}) preserves this bridge. The system needs Wood whole to have both generative cycling and destructive convergence.

### The beginning of generation

Generation cannot begin at the attractor (that's 克 or 比). It cannot begin at the inner core (that's where convergence terminates). It begins at the surface — the full 6-bit hexagram before any reduction. The outer bits (b₀,b₅) are the most generative: most transient, most information-rich, first to be stripped.

The 梅花 method reads the same structure temporally: 用 (now) → 互 (middle) → 變 (end). The generative relationships at the 用 level — the surface — are what's happening. By the 互 level, you see hidden structure. At the attractor, you see what cannot change.

Generation begins where information is richest and most perishable. Reduction is the process of watching generation give way to convergence give way to what remains. The beginning of generation is the question. The attractor is the answer. The answer has no generation in it.
