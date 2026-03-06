# Iter7 Trigram Findings: The Intermediate Space

## 1. Executive Summary

Six prior iterations mapped the King Wen sequence from two sides — Z₂⁶ algebra (iters 1–5) and traditional meaning (iter6). Algebra found the 32 orientation bits Pareto-optimal on four axes (p ≈ 10⁻⁵). Meaning found them 32/32 aligned with developmental priority (p ≈ 10⁻⁵). Neither derived the other. The pattern was **complementary coverage**: where algebra constrains most, meaning is weakest, and vice versa. But the mechanism was unnamed.

Iter7 worked in the intermediate space — the trigram layer, where each hexagram's six bits become an inner × outer situational interaction. Five rounds, three sage assessments.

**The central finding:** The trigram layer is not "between" algebra and meaning. It is the space where the hexagram's two natures — as a bit pattern and as a situation — are **the same object under different decompositions**. The mirror-pair decomposition (L1↔L6, L2↔L5, L3↔L4) and the trigram decomposition (L1-L3 | L4-L6) cut the same six lines differently. They are maximally non-aligned at the boundary L3|L4, where every mirror pair straddles and every trigram separates. There is no third thing doing the constraining. The constraint is the hexagram itself — six lines, indivisible, being read two ways.

This non-alignment generates the entire architecture:

- A **selection membrane** at the trigram boundary — the exact geometric condition under which bridge transitions preserve a trigram (the trigram boundary theorem)
- **Two independent continuity modes** — preserving bridges (orientation-dependent, at algebraically flexible positions) and corridors (ordering-dependent, at algebraically rigid positions) — that tile the complementary coverage with zero overlap
- A **permission-selection pattern** repeating at every scale — algebra permits, developmental logic selects

The abstract complementary coverage from iter6 is now *explained*: the sequence has two independently structured construction layers (pair ordering and orientation), each providing trigram continuity where the other is silent.

---

## 2. The Trigram Decomposition: Hexagrams as Trigram Interactions

Each hexagram's six bits decompose into two trigrams:
- **Lower trigram** (L1-L3): the inner condition
- **Upper trigram** (L4-L6): the outer context

With 8 possible trigrams, this places each hexagram in a cell of an 8×8 grid (lower × upper), with each cell occupied exactly once. The eight trigrams:

| Binary | Trigram | Symbol | Image | Family role |
|--------|---------|:------:|-------|-------------|
| 111 | Qian | ☰ | Heaven | Father |
| 000 | Kun | ☷ | Earth | Mother |
| 100 | Zhen | ☳ | Thunder | Eldest Son |
| 010 | Kan | ☵ | Water | Middle Son |
| 001 | Gen | ☶ | Mountain | Youngest Son |
| 011 | Xun | ☴ | Wind | Eldest Daughter |
| 101 | Li | ☲ | Fire | Middle Daughter |
| 110 | Dui | ☱ | Lake | Youngest Daughter |

Every hexagram is a specific pairing of inner condition with outer context. This is the space in which situational meaning operates — where "Fire below Earth" (Ming Yi, Darkening of the Light) means something different from "Earth below Fire" (Jin, Progress), not because the bits differ, but because the inner-outer relationship differs.

**Nuclear trigrams** use the middle four lines: nuclear lower (L2-L4), nuclear upper (L3-L5). They overlap with both primary trigrams — sharing L2,L3 with lower and L4,L5 with upper — creating a hidden dynamic within each hexagram. Only 16 of 64 possible nuclear pairs appear, each exactly 4 times. This contraction is the only known reduction that preserves both trigram and algebraic structure.

---

## 3. The KW Path Through Trigram-Pair Space

The King Wen sequence traces a path visiting each of 64 cells on the 8×8 grid exactly once — a Hamiltonian path. The path alternates between two types of steps:

- **Within-pair steps** (32): forced by algebraic pairing, connecting a pair's two members
- **Bridge steps** (31): free transitions connecting consecutive pairs

**The path jumps.** 54 of 63 transitions change both trigrams. Only 9 of 31 bridges preserve one trigram (5 lower, 4 upper). No within-pair transition preserves any trigram — this is algebraically forced (the cross-trigram theorem).

**Row and column coverage** follows the traditional canon structure: Heaven ☰ and Earth ☷ dominate the first half (mean position ~18–20 vs expected 32.5, z ≈ −2.2); the "children" trigrams (Thunder, Mountain, Wind, Lake) dominate the second half.

**The lag-4 periodicity** (p = 0.0017): every second pair tends to share a trigram in corresponding positions. This creates corridors — extended regions of partial trigram continuity, most prominently Earth spanning positions 7–20 and Heaven spanning positions 1–9.

---

## 4. Mirror Pairs vs Trigram Split: Two Decompositions of Z₂⁶

The hexagram's six bits admit two natural decompositions:

| Property | Mirror-pair split | Trigram split |
|----------|:-:|:-:|
| Grouping | (L1,L6), (L2,L5), (L3,L4) | (L1,L2,L3) \| (L4,L5,L6) |
| Principle | Palindromic symmetry | Positional (inner/outer) |
| Boundary | Each pair straddles L3\|L4 | Separated at L3\|L4 |
| What it sees | Orbit structure, algebraic properties | Situational interaction, meaning |

These two cuts are **maximally non-aligned**: every mirror pair has one member on each side of the trigram boundary. This is the structural root of the entire investigation.

**The cross-trigram theorem** (Round 1): every non-identity mirror-pair generator (O, M, I, and all combinations) changes bits in both the lower and upper trigram. Consequence: no KW pair can share a trigram. Pair partners always occupy different rows AND different columns of the 8×8 grid — full situational inversion.

**M's symmetric uniqueness** (Round 1): among the three single generators, M is the only one that flips the *same* position in both trigrams (position 1, the middle/ruler bit). O flips position 0↔2 across the boundary; I flips position 2↔0. Only M acts symmetrically.

This is why M-component = nuclear trigram rule. L2 − L5 literally *is* the yang count difference between nuclear trigrams. The translation is not by analogy — it is identity. M's unique symmetric action on the ruler line is the geometric reason this component carries meaning most transparently among all algebraic signals.

**O's nuclear invisibility** (Round 1): O flips only L1 and L6 (outermost lines), which lie outside the nuclear window (L2-L5). The four O-generator pairs are the only within-pair transitions that preserve the hidden dynamic.

---

## 5. Algebraic Properties in Trigram Terms

### The kernel = id theorem (Round 2)

The kernel dressing of a bridge XOR mask is its palindromic component — the generators whose mirror pairs are both active. Each such generator straddles the trigram boundary (one member in L1-L3, one in L4-L6). Therefore:

**A bridge can preserve a trigram only if its kernel dressing is id** — no palindromic component. Any active kernel generator forces both trigrams to change.

Of 31 bridges: 15 have kernel = id (candidates for preservation). 16 have kernel ≠ id (both trigrams necessarily change).

### The trigram boundary theorem (Round 5)

Complete characterization: an id-kernel bridge preserves a trigram **if and only if** all its XOR 1-bits fall on one side of the trigram boundary.

Two-level geometric gate at the L3|L4 membrane:
- **Level 1** (kernel = id): no mirror pair flips both members → no symmetric straddling
- **Level 2** (one-sided XOR): remaining unpaired bits all on one side → no asymmetric straddling

This is exact — not statistical, not approximate. It classifies all 31 bridges into three groups:

| Condition | Count | Character |
|-----------|:-----:|-----------|
| kernel = id AND one-sided | 9 | **Preserving** |
| kernel = id AND split | 6 | **Near-preserving** (min_dist = 1) |
| kernel ≠ id | 16 | **Both change** (min_dist ≥ 1) |

The gradient from preserving to non-preserving is smooth — no structural cliff.

### kac, χ², and the trigram layer

The four algebraic axes (kac, χ², M-score, asymmetry) operate on the orientation bits. The trigram layer interacts with them through the kernel dressing: bridge kernel dressings carry the palindromic structure that kac measures (kernel anti-correlation). The 9 preserving bridges, having kernel = id, contribute zero palindromic information to kac. The sequential structure of kac is carried entirely by the 16 non-id-kernel bridges and the 6 near-preserving ones.

### Within-pair geometry

**Theorem:** lo_dist = up_dist for all 32 pairs. Each mirror-pair generator contributes one bit change to each trigram. Within-pair geometry is entirely determined by the orbit algebra:

| Active generators | Grid distance | Count |
|:-:|:-:|:-:|
| 1 (O, M, or I) | 2 | 12 |
| 2 (OM, OI, MI) | 4 | 12 |
| 3 (OMI) or 0 (complement) | 6 | 8 |

Bridge geometry is free — distances span {1, 2, 3, 4, 6} with r = −0.354 between lower and upper Hamming distances (moderate trade-off: when one trigram changes more, the other changes less).

---

## 6. Meaning Properties in Trigram Terms

### Developmental priority as trigram narrative

Iter6 established that KW's orientation encodes developmental priority: condition → consequence. At preserving bridges, this manifests as a specific trigram narrative:

- **Lower preserved** (5 bridges): "The inner state endures while the outer situation transforms." Inner continuity across external change.
- **Upper preserved** (4 bridges): "The outer context endures while the inner state transforms." Contextual stability across internal change.

These are not overlaid interpretations. They are the structural consequence of which trigram persists.

### The 9 preserving bridges: developmental grammar

| B# | Preserved | Trigram | Narrative arc |
|:--:|:-:|:-:|---|
| B3 | Lower | Water ☵ | Inner danger persists; outer shifts force→yielding → Army |
| B6 | Upper | Heaven ☰ | Outer vastness persists; inner awakens receptivity→clarity → Fellowship |
| B11 | Upper | Mountain ☶ | Outer form persists; inner substance drains → Splitting Apart |
| B12 | Lower | Thunder ☳ | Inner impulse persists; outer expands receptivity→creative → Innocence |
| B13 | Upper | Mountain ☶ | Outer containment persists; inner shifts creative→impulse → Nourishment |
| B18 | Lower | Fire ☲ | Inner clarity persists; outer transforms suppression→gentle order → Family |
| B26 | Lower | Mountain ☶ | Inner stillness persists; outer unfolds stillness→gradual → Development |
| B27 | Upper | Thunder ☳ | Outer movement persists; inner deepens joy→clarity → Abundance |
| B30 | Lower | Lake ☱ | Inner joy persists; outer gentles danger→influence → Inner Truth |

**Xugua correspondence:** 7 of 9 clear alignment, 2 of 9 suggestive, 0 contradictions. The traditional pair-to-pair narrative matches the trigram-continuity story.

**Mountain** appears 3 times (p = 0.044 vs random orderings). Earth and Wind never appear as preserved trigrams.

### The B11-B12-B13 cluster

Three consecutive preserving bridges — a sustained developmental arc through Splitting Apart → Return → Innocence → Accumulation → Nourishment. Mountain persists as the outer context through B11-B13 while the inner state transforms from vitality through dissolution to directed impulse. This is the longest streak of trigram continuity in the sequence.

---

## 7. The Trigram Bridge: Where Algebra Meets Meaning

### The three translation points

These are not correspondences between separate facts. They are the same fact in two languages.

**1. Kernel silence = preservation permission.** The palindromic component of the XOR mask is literally the part that straddles the trigram boundary. "No palindromic component" (algebra) *is* "permission to preserve a trigram" (meaning). One condition, two vocabularies.

**2. M-component = nuclear trigram rule.** L2 − L5 is literally the yang count difference between nuclear trigrams. "L2 = yin first" (algebra) *is* "the hidden dynamic is receptive below, active above" (trigram tradition). Verified at all 16 M-decisive pairs.

**3. Complementary coverage = two continuity modes.** The abstract pattern from iter6 — where algebra is rigid, meaning is weaker — now has a concrete mechanism: two different structural features provide trigram continuity at the two kinds of positions through two different degrees of freedom.

### The membrane

The trigram boundary (L3|L4) is where the two decompositions interact. Mirror pairs straddle it. Trigrams are separated by it. The trigram boundary theorem locates exactly how the two readings constrain each other: preservation requires zero straddling — neither symmetric (kernel) nor asymmetric (orbit delta) — across the membrane.

This is a geometric fact about Z₂⁶ that has meaning-level consequences because the two decompositions correspond to the hexagram's two natures.

---

## 8. Meaning-Space Geometry: Distances, Paths, Structure

### The two geometric regimes

| Property | Within-pair (32 steps) | Bridge (31 steps) |
|---|---|---|
| Grid distances | {2, 4, 6} only | {1, 2, 3, 4, 6} |
| lo_dist vs up_dist | **Always equal** (forced) | Free, r = −0.354 |
| Asymmetry | Zero | Moderate trade-off |
| Determined by | Orbit structure entirely | Free variable |

Within-pair geometry is entirely algebraic — distances fixed, symmetry perfect. Bridge geometry is where freedom lives — distances span the full range, lower and upper trade off.

The path alternates between these two regimes: a forced, symmetric algebraic step, then a free, asymmetric meaning step. This rhythm — constraint then freedom, constraint then freedom — is the micro-structure of the sequence's construction.

### The corridors

Nine corridors of lag-4 trigram continuity:

| Corridor | Trigram | Positions | Pairs | Region |
|---|---|---|---|---|
| Earth (lower) | ☷ | 8,12,16,20 | P4,P6,P8,P10 | Upper Canon core |
| Earth (upper) | ☷ | 7,11,15,19 | P4,P6,P8,P10 | Upper Canon core |
| Heaven (lower) | ☰ | 1,5,9 | P1,P3,P5 | Opening |
| Heaven (upper) | ☰ | 6,10 | P3,P5 | Opening |
| Thunder (lower) | ☳ | 17,21 | P9,P11 | Upper Canon late |
| Mountain (upper) | ☶ | 18,22 | P9,P11 | Upper Canon late |
| Wind (lower) | ☴ | 28,32 | P14,P16 | Canon boundary |
| Lake (lower) | ☱ | 54,58 | P27,P29 | Lower Canon late |
| Wind (upper) | ☴ | 53,57 | P27,P29 | Lower Canon late |

**Dual corridor theorem:** the two longest corridors (LO Earth and UP Earth) span the exact same pairs — a single structural fact viewed from complementary trigram slots. The pairing transformation moves Earth between lower and upper positions within each pair.

The Earth corridor (positions 7–20) binds together the hexagrams of collective life — Army, Holding Together, Peace, Standstill, Modesty, Enthusiasm, Approach, Contemplation — under the persistent quality of receptive ground. The Heaven corridor (positions 1–9) tracks creative impulse through its first encounters with limitation and society.

---

## 9. The Complementary Coverage Mechanism

Iter6 observed the pattern: where algebra constrains most, meaning is weakest, and vice versa. Iter7 identified the mechanism.

**Two independent continuity modes** provide trigram structure at complementary positions:

| Mode | Scale | Source degree of freedom | Where it appears |
|---|---|---|---|
| **Preserving bridges** | Local (pair→pair) | Orientation (32 bits) | Trade-off pairs (67%) |
| **Corridors** | Periodic (every 2nd pair) | Pair ordering (31 choices) | KW-dom pairs (46%) |

Zero overlap between them. Each provides structure where the other frame is weakest:

- **Where algebra is rigid** (KW-dom pairs): pair ordering creates macro-scale trigram scaffolding. The corridors carry structural continuity. Meaning confidence is lower here (54% Clear vs 74% outside corridors).
- **Where algebra allows latitude** (trade-off pairs): orientation choices create local trigram continuity. The preserving bridges carry developmental narrative. Meaning confidence is higher here.

The two modes operate through genuinely independent degrees of freedom. Randomizing orientation preserves corridor structure (p = 0.21). Shuffling pair order preserves bridge preservation statistics (p = 0.23). Each mode is structurally invisible to the other's randomization.

This is complementary coverage explained as mechanism, not merely observed as pattern.

---

## 10. Nuclear Trigrams: The Hidden Dynamic

The nuclear trigrams (L2-L4, L3-L5) form a contracted space: 64 hexagrams → 16 nuclear pair types, each appearing exactly 4 times.

**Nuclear lower yang − nuclear upper yang = L2 − L5** (Theorem 12, iter3; verified iter7). This is the M-component — the strongest orientation signal — expressed in trigram language. The nuclear trigram rule ("inner nuclear has less yang than outer") *is* the M-rule ("L2 = yin first"), because L2 is literally a line of the nuclear lower and L5 is literally a line of the nuclear upper.

**O's nuclear invisibility:** O flips only L1 and L6, which lie outside the nuclear window. The four O-generator pairs preserve both nuclear trigrams. At bridges, nuclear preservation adds continuity depth:

| Tier | Bridges | Primary preserved | Nuclear preserved |
|---|---|---|---|
| 1 | B3, B6, B11, B12, B13, B27 | One primary | Neither nuclear |
| 2 | B18, B26 | Primary lower | Nuclear lower (Water in both) |
| 3 | B30 | Primary lower | **Both** nuclear (Thunder + Mountain) |

B30 (Jie → Zhong Fu) is the maximal continuity point: inner joy (Lake), hidden impulse (Thunder), and hidden restraint (Mountain) all persist. Only L6 changes.

Two non-preserving id-kernel bridges (B1, B8) also preserve nuclear lower despite failing primary preservation — their spoiler bit (L1) lies outside the nuclear window. These have hidden continuity invisible at the primary trigram level.

---

## 11. Sage Reflections

Three sage consultations shaped the investigation. Their key contributions:

**The non-separation thesis.** The trigram layer is not "between" algebra and meaning. The two decompositions were never separate. They are two ways of reading one object. The "bridge" or "joint" language is useful but obscures this: there is no third thing connecting two separate structures. The constraint is constitutive, not imposed.

**Permission-selection as framing, not finding.** The pattern appears at every scale because it's the structure of the question being asked. Any constrained combinatorial object will show "algebra permits, something selects." The insight is real but risks tautology if treated as discovery rather than framing. The genuine content is in *which* permissions exist and *which* selections are made.

**The 9/15 rate is geometrically expected.** Round 5 showed: 14/26 theoretical id-kernel XOR patterns are one-sided (54%); KW's 9/15 (60%) is close to base rate. The significance is in *which* bridges preserve and *where*, not in *how many*. This is a strength — the count isn't over-fitted.

**B22 and B24 as diagnostic.** These bridges had preservation available and the sequence rejected it — confirming that developmental priority and trigram preservation are genuinely independent peer principles, not a hierarchy where one overrides the other. They sometimes align, sometimes conflict.

---

## 12. What the Trigram Layer Reveals About the Nature of the Sequence

### The King Wen sequence has two construction layers

1. **Pair ordering** (31 choices): which pairs are neighbors. Carries corridor structure, lag-4 periodicity (p = 0.0017), macro-scale thematic arcs. First identified structural property of pair ordering, distinct from all orientation-level findings.

2. **Orientation** (32 choices): which member comes first. Carries kac, χ², M-score, asymmetry, developmental priority, bridge preservation.

These interact — corridors cluster at KW-dom positions, bridges cluster at trade-off positions — but are not reducible to each other. Randomizing one preserves the other's signal.

### Orientation is now fully characterized; pair ordering is not

The orientation bits have both an algebraic account (Pareto-optimal on four axes, locally unimprovable) and a meaning account (32/32 developmental priority). These two accounts exhibit complementary coverage that the trigram layer explains mechanistically.

The pair ordering has a structural account (corridors, lag-4) but **no meaning account**. Why these specific pairs are neighbors — what developmental logic governs pair sequencing — is the largest remaining unmapped degree of freedom. The Xugua (序卦傳) addresses pair-to-pair transitions directly and has not been systematically compared to corridor structure.

### The generative question remains open

Permission-selection operates at every identified scale. Algebra permits; something selects. "Developmental priority" names the selecting principle at the orientation level. At the pair-ordering level and at the bridge-selection level, the selecting principle is unnamed. The trigram investigation mapped the *shape* of selection — where it operates, what it permits, what it chooses — without identifying the principle itself beyond orientation.

The sage's assessment: the generative question is real but premature. You name the selecting principle by watching it operate across enough instances, not by theorizing in advance. Pair ordering is the natural next domain.

---

## 13. Key Results Table

| Finding | Round | Type | Significance |
|---|---|---|---|
| Cross-trigram theorem | 1 | Exact | All generators straddle boundary; no pair shares a trigram |
| M's symmetric uniqueness | 1 | Exact | M flips same position (ruler) in both trigrams |
| O's nuclear invisibility | 1 | Exact | O flips only lines outside nuclear window |
| Nuclear contraction 64→16 | 1 | Exact | 16 nuclear types, each appearing 4× |
| Kernel = id theorem | 2 | Exact | Preservation → kernel dressing = id |
| 9/31 preserving bridges | 2 | Observed | p = 0.23 vs random pair orderings (not significant in count) |
| Mountain overrepresentation | 2 | Marginal | 3×, p = 0.044 (borderline after correction) |
| 7/9 Xugua correspondence | 2 | Assessed | 7 clear, 2 suggestive, 0 contradictions |
| Bridges at trade-off pairs | 2 | Observed | 67% trade-off vs 41% base rate |
| Lag-4 periodicity | 3 | Significant | p = 0.0017 (3.3σ) |
| Within-pair lo_dist = up_dist | 3 | Exact | Forced by mirror-pair structure |
| Corridors: pair-ordering property | 4 | Significant | Destroyed by pair shuffle (p = 0.014), survives orientation shuffle (p = 0.21) |
| Two continuity modes | 4 | Structural | Zero overlap; complementary coverage tiled |
| Trigram boundary theorem | 5 | Exact | Preservation ≡ (kernel = id) ∧ (one-sided XOR) |
| Spoiler bits at position 0 | 5 | Observed | 5/6 at bottom; ruler line never spoils |
| B22, B24: preservation rejected | 5 | Diagnostic | Peer independence of developmental priority and preservation |
| B30: maximal continuity | 2,5 | Observed | Only bridge preserving all three layers (primary + both nuclear) |

---

## Data Files

| File | Contents |
|------|----------|
| `trigram_decompose.py` | Round 1: full trigram decomposition, 8×8 grid, path statistics |
| `round1-trigram-map.md` | Round 1: complete substrate map |
| `bridge_trigrams.py` | Round 2: bridge trigram analysis, statistical tests |
| `round2-bridges.md` | Round 2: preserving bridges, continuity gradient, Xugua correspondence |
| `path_geometry.py` | Round 3: lag-4 periodicity, return times, step distances |
| `round3-path-geometry.md` | Round 3: path geometry findings |
| `round4_corridors.py` | Round 4: corridor identification, mechanism tests |
| `round4-corridors.md` | Round 4: corridors, two continuity modes |
| `selection_analysis.py` | Round 5: trigram boundary theorem, counterfactual analysis |
| `round5-selection.md` | Round 5: selection principle, three bridge classes |
| `trigram-map.md` | Living document: final integrated map |
