# Round 4: Corridors, Mechanism, and the Two Continuity Modes

## Overview

Round 3 discovered the lag-4 periodicity (p = 0.0017) — every second pair tends to share a trigram, creating "corridors" of partial trigram continuity. This round investigates three questions: what mechanism produces the corridors, how do they interact with the 9 preserving bridges, and what is their relationship to complementary coverage. The central finding: **corridors and preserving bridges are independent continuity mechanisms that operate at different scales and have opposite relationships to complementary coverage.**

---

## Task A: Corridor Identification

### Corridors defined

A **corridor** is a maximal chain of hexagram positions p, p+4, p+8, ... that all share the same trigram in the same role (lower or upper). Length ≥ 2.

Nine corridors found:

| Rank | Role | Trigram | Length | Positions | Pairs spanned |
|:---:|:---:|:---:|:---:|---|---|
| 1 | Lower | Earth ☷ | 4 | 8,12,16,20 | P4,P6,P8,P10 |
| 2 | Upper | Earth ☷ | 4 | 7,11,15,19 | P4,P6,P8,P10 |
| 3 | Lower | Heaven ☰ | 3 | 1,5,9 | P1,P3,P5 |
| 4 | Lower | Wind ☴ | 2 | 28,32 | P14,P16 |
| 5 | Lower | Thunder ☳ | 2 | 17,21 | P9,P11 |
| 6 | Lower | Lake ☱ | 2 | 54,58 | P27,P29 |
| 7 | Upper | Mountain ☶ | 2 | 18,22 | P9,P11 |
| 8 | Upper | Wind ☴ | 2 | 53,57 | P27,P29 |
| 9 | Upper | Heaven ☰ | 2 | 6,10 | P3,P5 |

### The Dual Corridor Theorem

The two longest corridors — LO Earth and UP Earth — span the **exact same pairs** (P4,P6,P8,P10). These are not independent structures. The four pairs each have Earth as upper trigram in their first hexagram and Earth as lower trigram in their second hexagram:

| Pair | 1st hex (lo/up) | 2nd hex (lo/up) | Generator |
|:---:|---|---|:---:|
| P4 | Kan/Earth | Earth/Kan | M |
| P6 | Heaven/Earth | Earth/Heaven | OMI |
| P8 | Mountain/Earth | Earth/Thunder | I |
| P10 | Lake/Earth | Earth/Wind | OM |

In each pair, Earth appears in the 1st hex's upper position and the 2nd hex's lower position. The pairing transformation moves Earth from one trigram slot to its complement. The "dual corridor" is a single structural fact: **these four pairs all contain Earth, and they are placed at positions 4,6,8,10 — every other pair in the range.**

This dual structure also appears in shorter form:
- P9,P11: Thunder as 1st_lo + Mountain as 2nd_up (corridor pair)
- P27,P29: Lake as 2nd_lo + Wind as 1st_up (corridor pair)
- P3,P5: Heaven as 1st_lo + Heaven as 2nd_up (corridor pair)

### Corridor pairs: 13 of 32

Pairs participating in at least one corridor: P1, P3, P4, P5, P6, P8, P9, P10, P11, P14, P16, P27, P29.

These 13 corridor pairs are concentrated in the Upper Canon (11 of 13). Only P27 and P29 are in the Lower Canon. The corridor structure is predominantly an Upper Canon phenomenon.

---

## Task B: Corridors and Bridges Are Independent

### Zero overlap

**None of the 9 preserving bridges fall inside any corridor.**

The corridors connect pairs separated by 2 (pairs k and k+2). The preserving bridges connect consecutive pairs (pairs k and k+1). Because the corridors skip every other pair, the bridges that connect adjacent corridor pairs are not "internal" to the corridors — they bridge the gap between a corridor pair and its non-corridor neighbor.

Specifically: the Earth corridor spans pairs 4,6,8,10. The bridges between these pairs (B4→B5, B5→B6, ...) connect pairs 4→5, 5→6, 6→7, 7→8, 8→9, 9→10. The corridor-relevant bridges would be B5 (P5→P6), B7 (P7→P8), B9 (P9→P10) — but none of these are preserving bridges (B5 has kernel=I, B7 has kernel=O, B9 has kernel=O).

The preserving bridges are: B3, B6, B11, B12, B13, B18, B26, B27, B30. None connect pairs that are both in the same corridor.

### Two independent continuity mechanisms

| Property | Preserving bridges | Corridors |
|---|---|---|
| Scale | Local (pair k → k+1) | Pair-periodic (pair k → k+2) |
| Count | 9 of 31 | 9 structures, 13 pairs |
| Algebraic condition | kernel = id (no palindromic component) | Pair ordering (which pairs neighbor) |
| What is preserved | One primary trigram (lo or up) | A trigram appearing in the pair's hexagrams |
| Controlled by | Bridge XOR mask (affected by orientation) | Pair ordering (unaffected by orientation) |

These are genuinely independent: different scales, different algebraic determinants, and zero physical overlap.

---

## Task C: The Lag-4 Mechanism

### Pair ordering, not orientation

Three Monte Carlo tests (100,000 trials each) isolate the source:

| Test | KW | Null mean ± σ | p-value | Interpretation |
|---|:---:|:---:|:---:|---|
| Fix pair ordering, randomize orientation | 24 | 20.0 ± 3.7 | 0.213 | Orientation doesn't create lag-4 |
| Randomize pair ordering, keep orientation | 24 | 13.8 ± 4.2 | **0.014** | Pair ordering creates lag-4 |
| Randomize both | 24 | 13.5 ± 4.3 | **0.014** | Same significance as order alone |

**The lag-4 periodicity is entirely a property of which pairs are placed where in the sequence.** Flipping orientations within pairs doesn't destroy it (p = 0.21 — KW indistinguishable from random orientations with the same pair order). Shuffling the pair order does destroy it (p = 0.014).

This is the first property identified that is purely about **pair ordering** rather than **orientation**. All previous findings (kac, χ², M-score, developmental priority) concerned the 32 orientation bits. The corridors are about the 31 inter-pair position choices.

### AA vs BB decomposition

Lag-4 decomposes into AA (1st hex of pair k matches 1st hex of pair k+2) and BB (2nd hex matches 2nd):

| Component | KW | Null mean ± σ | p-value |
|---|:---:|:---:|:---:|
| AA (1st↔1st) | 13 | 6.9 ± 2.3 | **0.010** |
| BB (2nd↔2nd) | 11 | 6.9 ± 2.3 | 0.060 |

AA is more significant than BB. The first hexagrams of every-other-pair are the primary carriers of the periodic signal. Since the "first hexagram" is determined by orientation, this means orientation contributes a secondary enhancement to the pair-ordering-driven periodicity — but the enhancement is not statistically significant on its own (p = 0.21 for orientation randomization).

### The pair-level view

At the pair level, lag-4 = lag-2 (every other pair shares a trigram). The slot-by-slot analysis: pairs k and k+2 match in 24/120 trigram slots (20.0%) vs expected 12.5% under random pair ordering (p = 0.014). The matches are strongly structured:

| Match pattern | Count | Description |
|---|:---:|---|
| 1st_lo ↔ 1st_lo | 4 | Same lower trigram in first hexagrams |
| 1st_up ↔ 1st_up | 9 | Same upper trigram in first hexagrams |
| 2nd_lo ↔ 2nd_lo | 8 | Same lower trigram in second hexagrams |
| 2nd_up ↔ 2nd_up | 3 | Same upper trigram in second hexagrams |

The 1st_up slot is the strongest contributor (9 matches). This aligns with the Earth corridor structure: pairs 4,6,8,10 all have Earth as 1st_up.

---

## Task D: Corridors × Complementary Coverage

### The inverse pattern

| | KW-dom | Trade-off | S2 | Clear | Suggestive |
|---|:---:|:---:|:---:|:---:|:---:|
| In corridor (13 pairs) | 6 (46%) | 4 (31%) | 3 (23%) | 7 (54%) | 6 (46%) |
| Outside corridor (19 pairs) | 5 (26%) | 11 (58%) | 3 (16%) | 14 (74%) | 5 (26%) |

**Corridor pairs are more algebraically rigid (46% KW-dom vs 26%) and less meaning-transparent (54% Clear vs 74%).** This is the **opposite** of the preserving-bridge pattern, where preserving bridges cluster at trade-off (algebraically flexible) pairs with lower Clear rates.

### The two continuity modes and complementary coverage

| Continuity mechanism | Where it appears | Algebraic character | Meaning character |
|---|---|---|---|
| Preserving bridges | Trade-off pairs (67%) | Algebra allows latitude → trigram continuity fills the gap | Bridges at confidence transitions |
| Corridors | KW-dom pairs (46%) | Algebra is rigid → corridors provide structural framework | Less meaning-transparent |

The two continuity mechanisms *partition* the complementary coverage:
- Where **algebra is flexible** (trade-off pairs): preserving bridges provide local trigram continuity, and meaning is strong
- Where **algebra is rigid** (KW-dom pairs): corridors provide periodic trigram continuity, and meaning is weaker

This is co-projection seen from a new angle. The algebraic framework (pair ordering, orbit structure) creates the corridors. The semantic space (developmental logic) creates the bridge continuity. Each operates where the other is weakest. The trigram layer is where they divide labor.

---

## Task E: The Trigram Pair-Type Structure

### Three pair types

Each pair uses 2, 3, or 4 unique trigrams across its two hexagrams:

| Unique trigrams | Count | Composition |
|:---:|:---:|---|
| 2 | 10 | Both hexagrams use the same complementary trigram pair |
| 3 | 16 | One palindromic + one non-palindromic trigram in 1st hex |
| 4 | 6 | Both non-palindromic trigrams in 1st hex → 4 trigrams total |

This is controlled by the **palindrome status** of the trigrams:
- **Palindromic trigrams** (reverse = self): Heaven (111), Earth (000), Fire (101), Water (010)
- **Non-palindromic trigrams** (reverse ≠ self): Thunder (100) ↔ Mountain (001), Wind (011) ↔ Lake (110)

For inversion pairs (28 of 32), the second hexagram's lower = reverse(first's upper) and vice versa. If both trigrams are palindromic, reversal doesn't change them → 2 unique trigrams. If one is non-palindromic, reversal changes it → 3 unique. If both are non-palindromic, reversal may produce the same pair (when both are from the same reversal pair, e.g., Thunder/Thunder → Mountain/Mountain → 2 unique) or different trigrams → 4 unique.

### The all-children hexagram

All six 4-trigram pairs use **exactly the same four trigrams**: {Thunder, Mountain, Wind, Lake} — the four "children" trigrams. These are the 4 non-palindromic trigrams. The "parent" (Heaven, Earth) and "middle" (Fire, Water) trigrams are palindromic and never appear in 4-trigram pairs.

This is a structural consequence: 4-trigram pairs require both members to involve non-palindromic trigrams that reverse into different trigrams. The only non-palindromic trigrams are the four children. So 4-trigram pairs are always "all-children" pairs.

### Corridor membership by pair type

| Pair type | In corridor | Total | Rate |
|:---:|:---:|:---:|:---:|
| 2-trigram | 5 | 10 | 50% |
| 3-trigram | 4 | 16 | 25% |
| 4-trigram | 4 | 6 | 67% |

The 4-trigram (all-children) pairs have the highest corridor participation rate. This seems counterintuitive — pairs with *more* unique trigrams should share *less* with neighbors. But the all-children pairs all share the same 4 trigrams ({Zhen, Gen, Xun, Dui}), so any two of them automatically share. The pair ordering places several of these near each other (P9, P14, P16 in the upper canon; P27, P31 in the lower canon), creating corridors.

---

## Task F: Corridor Meaning

### The Earth Corridor (Pairs 4,6,8,10; Positions 7-20)

Hexagrams: Shi (Army), Bi (Holding Together), Tai (Peace), Pi (Standstill), Qian/Modesty, Yu (Enthusiasm), Lin (Approach), Guan (Contemplation).

The developmental arc: from collective mobilization (Army) through the cycle of social flourishing and decline (Peace → Standstill) to the deepening of contemplative wisdom (Modesty → Contemplation). **Earth as the persistent element** is semantically precise: these hexagrams describe the collective ground — social organization, governance, approach to power — all rooted in Earth's quality of receptive holding.

The skipped pairs in between (P5: Xiao Chu/Lü, P7: Tong Ren/Da You, P9: Sui/Gu) concern individual conduct within the collective: personal restraint, fellowship, following/decay. The Earth corridor provides the *ground* while the intervening pairs describe *what happens on that ground*.

### The Heaven Corridor (Pairs 1,3,5; Positions 1,5,9)

Hexagrams: Qian (Creative), Xu (Waiting), Xiao Chu (Small Taming).

The opening sequence: pure creative force (Qian), then meeting the first obstacle (Xu/Waiting involves Heaven below Water), then the first social formation (Small Taming involves Heaven below Wind). **Heaven as the persistent element** tracks the creative impulse through its first encounters with limitation and society.

### The Thunder/Mountain Corridor (Pairs 9,11; Positions 17-22)

Two overlapping corridors: LO Thunder (Sui, Shi He) and UP Mountain (Gu, Bi/Grace). These pairs share the same hexagrams: Following/Decay and Biting Through/Grace. The persistent elements are movement (Thunder below) and stillness (Mountain above) — the dynamic of applying force from below against the constraint of form above.

---

## Summary

### Four findings

**1. The lag-4 periodicity is a pair-ordering property.** It is not produced by orientation choices. Shuffling pair order destroys it (p = 0.014); randomizing orientation within pairs preserves it (p = 0.21). This is the first identified structural property of the KW pair ordering itself, as opposed to the orientation bits.

**2. Corridors and preserving bridges are independent.** Zero overlap. Different scales (pair k→k+2 vs k→k+1), different algebraic determinants (pair ordering vs kernel dressing), different relationships to complementary coverage. They are two distinct continuity mechanisms.

**3. The two continuity modes partition complementary coverage.** Preserving bridges appear at algebraically flexible (trade-off) positions where meaning is strong. Corridors appear at algebraically rigid (KW-dom) positions where meaning is weaker. Each mechanism provides trigram continuity where the other frame (algebra for bridges, meaning for corridors) is less constrained.

**4. The dual corridor structure.** The two longest corridors (LO Earth, UP Earth) are a single structure: the same 4 pairs viewed from complementary trigram slots. This generalizes: corridors track pairs that *contain* a specific trigram, and the pairing transformation moves that trigram between lower and upper slots within each pair.

### Connection to co-projection

The corridor finding extends the co-projection picture. Previously: algebra and meaning each account for the 32 orientation bits from complementary directions. Now: the *pair ordering* (a different degree of freedom from orientation) creates trigram corridors that themselves split along the complementary coverage boundary. The algebraic side of the sequence creates periodic trigram structure at KW-dom positions; the semantic side creates local trigram continuity at trade-off positions. The trigram layer is where these two modes of structure-making become visible as distinct mechanisms.

This suggests that what was called "the single structure casting both shadows" has at least two independent construction layers: pair ordering (corridors) and orientation choice (bridges + kac + M-score + developmental priority). The corridor structure is a third face of the unnamed object — neither algebraic (it's about pair ordering, not orbits) nor semantic (it's about trigram statistics, not developmental logic), but structural in a way that partitions the algebra-meaning complementarity.

---

## Data Files

| File | Contents |
|------|----------|
| `round4_corridors.py` | Complete computation script |
| `round4-corridors.md` | This document |
