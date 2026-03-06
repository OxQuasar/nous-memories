# Spaceprobe: Characterizing the Underlying Relational Space

## Motivation

The opposition theory investigation revealed that multiple independent coordinate systems — Lo Shu (number-theoretic), binary trigrams (algebraic), five phases (elemental/cyclic), He Tu (directional) — all produce consistent assignments when mapped onto each other. Yet no direct bridge exists between any two of them (Lo Shu numbers don't translate to binary operations; five-phase cycles don't reduce to XOR). They agree only *through* the trigram intermediary.

This convergence without reduction implies an underlying relational space that each system coordinatizes faithfully but partially. The question: what IS that space, stated without reference to any particular coordinate system?

## Prior findings that constrain the space

### At n=3 (trigrams)

- 8 states on a circle with 4 diametric pairs, each with a unique opposition type — all 4 nonzero XOR masks used exactly once (max diversity)
- Lo Shu magic square maps perfectly onto the KW circle: diametric pairs sum to 10, rows/columns/diagonals sum to 15
- Odd-even alternation around the circle (odd=cardinal=yang-dominant, even=intercardinal)
- Element assignments consistent across Lo Shu numbers, trigram binary structure, and five-phase directionality
- He Tu pairs (differ by 5) trace specific 生克 edges: 3 生 + 1 克
- Earth carries the magic constant: {2, 5, 8} sums to 15, Earth=center
- Intra-element binary structure is non-uniform: Wood trigrams are complements (Zhen 100 ↔ Xun 011, distance 3), Metal and Earth trigrams are adjacent (distance 1)
- Flying star path (Lo Shu traversal 5→6→7→...→4) has constant consecutive mask distance of exactly 2, zero variance — maximizes uniformity
- Three pairing systems (Fu Xi, Lo Shu, He Tu) occupy three distinct points in opposition measure space: max strength, max diversity, uniform intermediate

### At n=6 (hexagrams)

- KW pairing is one of exactly 9 structurally coherent pairings under the 384-element mirror-pair symmetry group
- The pairing rule is reversal (flip upside down) wherever possible, complement only for the 8 palindromic hexagrams — preserves yin-yang balance (weight)
- 7 XOR mask types from the 3 mirror-pair operations {O, M, I} and their combinations; KW uses all 7
- Consecutive bridge kernel distance at the 96.6th percentile (corrected from 99.2nd under proper null model) — driven by 8/30 OMI complement transitions. Concentrates entirely in Upper Canon (hex 1-30, 99.84th %ile); Lower Canon is generic
- 16 of 32 orientation bits load-bearing under metric-degradation criteria (corrected from 27/27)
- kac: 2 kernel repeats out of 30 (~75th percentile, corrected from "0th percentile")
- H-subgroup residence: running kernel product inhabits {id, O, MI, OMI} 64.5% of the time (96.7th percentile, independent of f1)
- 32/32 developmental priority — condition precedes consequence in pair ordering
- Algebra↔meaning inverse correlation but jointly exhaustive coverage
- Phase transition from n=4 to n=6: KW-style is mediocre at n=4 (75th percentile) but extreme at n=6 (99.98th percentile strength), driven by 3 mirror pairs unlocking the full Z₂³ signature vocabulary

### Across scales

- n=3 and n=6 use opposite pairing principles: n=3 chose complement (max strength), n=6 chose reversal (weight preservation). Cross-scale divergence unresolved.
- The five-phase layer (生克) is orthogonal to the hexagram pairing layer — they don't interact
- Nuclear trigrams (互卦) carry no independent opposition information; they are a lossy projection of the hexagram level
- The n=3 arrangement is a cosmological/spatial map (Lo Shu); the n=6 sequence is a process ordering (developmental priority, sequential anti-repetition). Different scales serve different functions.

---

## Approach 1: Invariant Catalog

**Method:** Enumerate every property that holds across ALL coordinate systems simultaneously. The intersection of what all systems preserve IS the underlying space, defined by its invariants.

**Steps:**

1. List all known properties in each coordinate system:
   - Binary: Z₂³ group structure, XOR masks, Hamming distances, complement/reversal operations
   - Lo Shu: magic square constraint (sum 15), pair-sum 10, odd-even cross pattern, row/column/diagonal structure
   - Five phases: directed 5-cycle (生/克), element groupings (1/1/2/2/3 partition), directional correspondence
   - He Tu: pair-by-5 structure, inner/outer rings, directional pairing

2. For each property, test whether it has a counterpart in EVERY other system. A property is an invariant only if it manifests in all coordinate systems, possibly in different vocabulary.

3. The properties that survive this filter define the underlying space. Express them in coordinate-free language.

**Expected output:** A minimal set of axioms that any faithful coordinatization must satisfy. Something like: "a space of 8 states with 4 opposition pairs, a cyclic ordering, and a directed interaction structure on 5 equivalence classes."

**Risk:** The intersection might be too thin — just the trivial structure (8 things arranged in a circle with 4 pairs). Or it might be rich enough to be interesting.

---

## Approach 2: Fourth Coordinate System

**Method:** Find additional traditional systems that independently map onto the same 8-state space. Each new system that agrees with the others further constrains what the underlying space can be. The *way* it converges reveals new invariants invisible from the first three systems alone.

**Candidates:**

1. **天干 (Heavenly Stems):** 10 stems, traditionally paired with the 5 elements (2 per element). They form a 10-cycle used in calendar systems. The stems have yin/yang polarity. If they map onto the trigram space consistently, the 10→8 reduction and its kernel would reveal structure.

2. **地支 (Earthly Branches):** 12 branches (the zodiac animals), each with element and yin/yang assignment. Used in 四柱 (Four Pillars) alongside stems. The 12→8 mapping and its structure.

3. **二十八宿 (28 Lunar Mansions):** 28 star groupings divided into 4 directional quadrants of 7 each. Each quadrant maps to an element and a guardian beast. The 28→8 reduction through the directional/elemental layer.

4. **二十四节气 (24 Solar Terms):** 24 divisions of the solar year, grouped by season and element. The temporal cycle mapped onto the spatial framework.

5. **九宫 (Nine Palaces):** The Lo Shu grid interpreted as 9 spatial sectors with temporal dynamics (Flying Stars). The 9th position (center/Earth/5) may carry the structure's fixed point.

**Steps:**

1. Select the most tractable candidate (likely 天干 — smallest, most directly connected to five phases)
2. Map it onto the trigram space via traditional correspondences
3. Compute its binary/XOR properties
4. Check which invariants from Approach 1 it preserves
5. Identify new constraints it introduces

**Expected output:** New invariants that weren't visible from the first three systems. Possibly a tighter characterization of the underlying space.

**Risk:** The traditional correspondences may be inconsistent or many-to-one in ways that destroy structure. The mapping may require interpretive choices that undermine the result.

---

## Approach 3: Operational Probe via Divination

**Method:** The Meihua divination system IS a traversal of this space. It takes input (time/perception), maps to coordinates, and traces a path (本卦→互卦→变卦). If the underlying space is real, the traversal should have structural properties independent of which coordinate system describes it.

**Steps:**

1. Take a concrete Meihua reading (from sy-divination.md or construct one)
2. Express the complete evaluation in all available coordinate systems:
   - Binary: hexagram as {0,1}⁶, trigrams as {0,1}³, XOR masks along the path
   - Lo Shu: trigrams as numbers, arithmetic relationships along the path
   - Five phases: elements, 生克 evaluations at each step
   - He Tu: number pairs, directional relationships

3. At each step of the evaluation path (本→互→变), record:
   - The transition in each coordinate system
   - Which properties are preserved vs changed
   - The relationship to 体 in each vocabulary

4. Identify what is INVARIANT across all coordinate descriptions of the same reading:
   - Does the 生克 verdict correspond to a specific binary transition type?
   - Does the Lo Shu arithmetic predict the five-phase evaluation?
   - Is there a quantity that is conserved along the evaluation path in all systems?

5. Repeat for multiple readings covering different hexagram regions to check generality.

**Expected output:** Either a coordinate-free description of what a divination reading "does" to the underlying space (a traversal with specific invariant properties), or evidence that the coordinate systems diverge operationally (different systems give incommensurable descriptions of the same reading).

**Risk:** This is the most speculative approach. The divination system may mix structural and interpretive elements in ways that can't be cleanly separated. The "invariant" may turn out to be the five-phase verdict itself, which would be circular.

---

## Sequencing

**Approach 1 first.** It's the most constrained and least speculative. It uses only data we already have. If the invariant catalog is rich, it directly answers the question. If it's thin, it tells us the space is simpler than the coordinate systems suggest.

**Approach 2 if Approach 1 produces a candidate characterization.** A fourth coordinate system can validate or falsify the proposed invariants. Pick the candidate that's most likely to introduce NEW constraints.

**Approach 3 last, or in parallel with 2.** It's the highest-risk, highest-reward path. It's also the one closest to the tradition's own claim about what the system does.

---

## Key distinction: isomorphism vs coordinate-free

The convergence of multiple systems doesn't require a coordinate-free underlying space. It only requires that structure-preserving maps (isomorphisms) exist between systems and that these maps are compatible (the triangle Lo Shu → trigrams → five phases commutes).

Two possible answers:

**A. The trigrams ARE the universal object.** Z₂³ is the canonical space. Lo Shu, He Tu, five phases are different labelings of the same 8 objects. The convergence is trivially explained: they're all decorating the same structure. The "underlying space" is just binary trigrams, and there's nothing deeper.

**B. There is a space richer than any single coordinate system.** Some properties are visible from Lo Shu but not from binary, or from five phases but not from Lo Shu. The convergence is non-trivial because each system captures a different *aspect* of something none of them fully represents.

The test: are there properties of the space that are visible from one coordinate system but NOT expressible in another? If yes → B (the space is richer). If every property in every system translates to binary → A (Z₂³ is the whole story).

Q4 from the Lo Shu study showed no direct Lo Shu→binary bridge. This is ambiguous — it could mean the Lo Shu sees something binary doesn't (evidence for B), or it could mean the Lo Shu is just an opaque encoding of binary that adds nothing structural (evidence for A).

The spaceprobe must resolve this fork.

## The question, restated

Multiple coordinate systems converge on the same 8-state relational structure without being reducible to each other. What are the minimal axioms of a space that admits all of these as faithful coordinatizations? And does that axiomatic space have properties that explain why the tradition treats it as isomorphic to the relational structure of events?

Or, more sharply: is the underlying space just Z₂³ with decorations, or is it something richer that Z₂³ only partially captures?
