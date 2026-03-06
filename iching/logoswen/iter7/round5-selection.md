# Round 5: The Selection Principle — What Separates the 9 from the 6

## Overview

The kernel = id theorem (Round 2) established that trigram preservation at a bridge *requires* kernel dressing = id. But 15 bridges have kernel = id and only 9 preserve. This round characterizes the 6 non-preserving id-kernel bridges exhaustively to identify the second-order selection principle. The central finding: **the selection is geometric, not statistical — an id-kernel bridge preserves if and only if all its XOR 1-bits fall on one side of the trigram boundary.** This is an exact theorem, completing the characterization of trigram preservation.

---

## Task A: The 6 Non-Preserving Id-Kernel Bridges

### Full characterization

| B# | Exit hex | Entry hex | XOR mask | H | lo_d | up_d | Orbit Δ | Near-preserves |
|:--:|----------|-----------|:--------:|:-:|:----:|:----:|---------|:-:|
| B1 | Kun ☷☷ (000000) | Zhun ☳☵ (100010) | 100010 | 2 | 1 | 1 | L1+L5 | lower (1 bit) |
| B8 | Yu ☷☳ (000100) | Sui ☳☱ (100110) | 100010 | 2 | 1 | 1 | L1+L5 | lower (1 bit) |
| B10 | Guan ☷☴ (000011) | Shi He ☳☲ (100101) | 100110 | 3 | 1 | 2 | L1+L5+L4 | lower (1 bit) |
| B22 | Gou ☴☰ (011111) | Cui ☷☱ (000110) | 011001 | 3 | 2 | 1 | L6+L2+L3 | upper (1 bit) |
| B24 | Jing ☴☵ (011010) | Ge ☲☱ (101110) | 110100 | 3 | 2 | 1 | L1+L2+L4 | upper (1 bit) |
| B31 | Xiao Guo ☶☳ (001100) | Ji Ji ☲☵ (101010) | 100110 | 3 | 1 | 2 | L1+L5+L4 | lower (1 bit) |

All 6 are near-preserving: one trigram is distance 1 from preservation, meaning a single bit prevents full trigram continuity. The other trigram is distance 1–2.

### Comparison with the 9 preserving bridges

| Property | 9 Preserving | 6 Non-preserving |
|----------|:---:|:---:|
| Mean Hamming | 2.1 | 2.7 |
| lo_dist range | {0, 2} | {1, 2} |
| up_dist range | {0, 1, 2, 3} | {1, 2} |
| XOR patterns | 6 distinct | 4 distinct |
| Repeated deltas | L1+L3 ×2, L2+L3 ×2, L6+L5+L4 ×2 | L1+L5 ×2, L1+L5+L4 ×2 |

---

## Task B: The Bit-Distribution Theorem

### The exact separator

For each id-kernel bridge, the XOR mask has no palindromic component (by definition — kernel = id means no mirror pair flips both members). Every 1-bit is "unpaired." The critical question: are these unpaired bits all on one side of the trigram boundary, or do they straddle it?

**Result: Perfect separation.**

| Bridge | XOR mask | Lower bits | Upper bits | Distribution | Status |
|:------:|:--------:|:---:|:---:|:---:|:---:|
| B3 | 000111 | — | L4,L5,L6 | ALL UPPER | **PRESERVES** lower |
| B6 | 101000 | L1,L3 | — | ALL LOWER | **PRESERVES** upper |
| B11 | 101000 | L1,L3 | — | ALL LOWER | **PRESERVES** upper |
| B12 | 000111 | — | L4,L5,L6 | ALL UPPER | **PRESERVES** lower |
| B13 | 011000 | L2,L3 | — | ALL LOWER | **PRESERVES** upper |
| B18 | 000011 | — | L5,L6 | ALL UPPER | **PRESERVES** lower |
| B26 | 000010 | — | L5 | ALL UPPER | **PRESERVES** lower |
| B27 | 011000 | L2,L3 | — | ALL LOWER | **PRESERVES** upper |
| B30 | 000001 | — | L6 | ALL UPPER | **PRESERVES** lower |
| B1 | 100010 | L1 | L5 | SPLIT 1+1 | near-preserving |
| B8 | 100010 | L1 | L5 | SPLIT 1+1 | near-preserving |
| B10 | 100110 | L1 | L4,L5 | SPLIT 1+2 | near-preserving |
| B22 | 011001 | L2,L3 | L6 | SPLIT 2+1 | near-preserving |
| B24 | 110100 | L1,L2 | L4 | SPLIT 2+1 | near-preserving |
| B31 | 100110 | L1 | L4,L5 | SPLIT 1+2 | near-preserving |

### Theorem (Trigram Preservation — Complete Characterization)

A bridge in the KW sequence preserves a trigram **if and only if**:
1. Its kernel dressing is id (no palindromic component), **AND**
2. All XOR 1-bits fall on one side of the trigram boundary (all in L1–L3 or all in L4–L6).

Equivalently: the orbit delta uses lines from only one trigram half.

This gives the three-level classification:

| Condition | Count | Character |
|-----------|:-----:|-----------|
| kernel = id AND one-sided | 9 | **Preserving** (one trigram unchanged) |
| kernel = id AND split | 6 | **Near-preserving** (min_dist = 1) |
| kernel ≠ id | 16 | **Both change** (min_dist ≥ 1) |

This is a structural theorem, not a statistical pattern. It holds exactly for all 31 bridges.

### Why this works

For id-kernel bridges, the XOR mask has no palindromic component — each 1-bit stands alone, with its mirror partner at 0. These unpaired bits are the only things that change between exit and entry hexagrams.

If all 1-bits are in positions 0–2 (L1–L3): the lower trigram changes, the upper trigram is untouched → upper preserved.

If all 1-bits are in positions 3–5 (L4–L6): the upper trigram changes, the lower trigram is untouched → lower preserved.

If 1-bits are on *both* sides: both trigrams change → near-preserving.

The geometric insight: **the trigram boundary (L3|L4) is the selection membrane.** The kernel = id condition ensures no bit-pair straddles this membrane symmetrically. The one-sidedness condition ensures the remaining asymmetric bits don't straddle it either. Preservation requires *total* non-straddling: neither symmetric (kernel) nor asymmetric (orbit delta) changes cross the boundary.

---

## Task C: The Theoretical Landscape

### How many id-kernel XOR patterns exist?

Each of the 3 mirror pairs (L1↔L6, L2↔L5, L3↔L4) can contribute:
- 0 bits (pair inactive)
- 1 bit on the lower side (L1, L2, or L3)
- 1 bit on the upper side (L6, L5, or L4)

This gives 3³ = 27 patterns, minus the zero pattern = **26 nonzero id-kernel XOR masks**.

Of these 26:
- **14 are one-sided** (all bits in L1–L3 or all in L4–L6): 2 × (2³ − 1) = 14
- **12 are split** (bits on both sides): 26 − 14 = 12

Wait — let me recount. The one-sided patterns: all bits lower means each active pair chooses lower, all bits upper means each active pair chooses upper. For "all lower": each pair is either inactive (0) or lower (L). That's 2³ − 1 = 7 patterns with at least one active. Similarly 7 for "all upper." Total one-sided = 14.

But the script output says 14 preserving / 12 non-preserving. Let me verify: 26 − 14 = 12. Yes.

**Preserving fraction by Hamming weight:**

| Hamming | Total patterns | One-sided | Fraction |
|:-------:|:-:|:-:|:-:|
| 1 | 6 | 6 | 100% |
| 2 | 12 | 6 | 50% |
| 3 | 8 | 2 | 25% |

At H=1 (single bit flip), preservation is guaranteed — a single bit is always on one side. At H=2, it's a coin flip. At H=3, only 2 of 8 patterns are one-sided (all-lower: L1+L2+L3, or all-upper: L4+L5+L6). The probability of preservation decreases sharply with Hamming distance.

### KW's id-kernel bridges vs the theoretical base rate

KW has 15 id-kernel bridges with 9 preserving = **60%**. The theoretical base rate of one-sided patterns is 14/26 = **54%**. KW is slightly above base rate but not significantly so. The count of 9 was already shown (Round 2) to be statistically unremarkable against random pair orderings.

**Conclusion: KW does not over-select for preservation among its id-kernel bridges.** The 9/6 split is close to what geometry alone predicts. The significance of the 9 preserving bridges lies in their *content* (which trigrams, which meanings) not their *count*.

---

## Task D: The Spoiler Bits

Each non-preserving id-kernel bridge nearly preserves one trigram — a single "spoiler bit" on the wrong side prevents it. What are these spoiler bits?

| B# | Spoiler bit | Position in trigram | Near-preserves |
|:--:|:-----------:|:-------------------:|:-:|
| B1 | L1 | bottom (position 0) | lower |
| B8 | L1 | bottom (position 0) | lower |
| B10 | L1 | bottom (position 0) | lower |
| B22 | L6 | top (position 2) | upper |
| B24 | L4 | bottom (position 0) | upper |
| B31 | L1 | bottom (position 0) | lower |

**5 of 6 spoiler bits are at position 0** (the bottom of their respective trigram). The middle position (L2/L5, the ruler line) never appears as a spoiler.

This connects to the mirror-pair structure. The spoiler bits are:
- L1 (4 cases): the O-generator's lower member
- L4 (1 case): the I-generator's upper member
- L6 (1 case): the O-generator's upper member

The O mirror pair (L1↔L6) is involved in 5 of 6 spoilers. The M mirror pair (L2↔L5) is never a spoiler. This is consistent with M's special status: M acts on the ruler line symmetrically, and its contribution is the strongest orientation signal (the nuclear trigram rule). The M-pair's symmetry means it either flips both bits (kernel ≠ id) or neither — it never contributes a "stray" bit on the wrong side.

### The L1+L5 pattern

Three bridges (B1, B8, B31) share the orbit delta L1+L5 or its extension L1+L5+L4. This pattern — L1 on the lower side, L5 on the upper side — corresponds to the O-pair contributing L1 and the M-pair contributing L5. These are bits from *different* mirror pairs that happen to land on *different* sides of the trigram boundary.

B1 and B8 have the identical XOR mask (100010) and identical orbit delta (L1+L5). They represent the same structural situation at different positions in the sequence:
- B1: Kun (☷☷) → Zhun (☳☵) — Earth/Earth transitioning to Thunder/Water
- B8: Yu (☷☳) → Sui (☳☱) — Earth/Thunder transitioning to Thunder/Lake

In both cases: the bottom line L1 flips (0→1, Earth→Thunder in the lower trigram) while L5 flips (changing the upper trigram's middle position). The near-preserved lower trigram is Kun → Zhen (Earth → Thunder), differing only at L1.

---

## Task E: Nuclear Trigrams at the 15 Id-Kernel Bridges

### Nuclear preservation comparison

| | Nuc. lower pres. | Nuc. upper pres. | Both | Neither |
|---|:---:|:---:|:---:|:---:|
| 9 preserving | 3/9 (33%) | 1/9 (11%) | 1/9 (B30) | 6/9 |
| 6 non-preserving | 2/6 (33%) | 0/6 | 0/6 | 4/6 |

The rates of nuclear preservation are similar between the two groups. The key distinction is at the top: **only preserving bridges achieve both-nuclear preservation** (B30, the Jie→Zhong Fu transition with maximum continuity). Non-preserving bridges never preserve nuclear upper.

### The nuclear preservation mechanism

Nuclear lower uses L2,L3,L4 (bits 1,2,3). Nuclear upper uses L3,L4,L5 (bits 2,3,4). For nuclear preservation, the relevant bits must all be 0 in the XOR mask.

The bridges that preserve nuclear lower:
- B1 (near), B8 (near): XOR=100010. Bits 1,2,3 are all 0. ✓
- B18 (pres), B26 (pres): XOR=000011, 000010. Bits 1,2,3 are all 0. ✓
- B30 (pres): XOR=000001. Bits 1,2,3,4 are all 0. ✓ (also preserves nuclear upper)

**Notable:** B1 and B8, despite being non-preserving at the primary trigram level, *do* preserve nuclear lower. Their spoiler bit (L1) is outside the nuclear window. So these bridges have a hidden continuity that doesn't appear at the primary trigram level — the inner dynamic persists even as the outer trigram frame shifts.

The 2 non-preserving bridges with nuclear lower preservation (B1, B8) both have the L1+L5 orbit delta. L1 is outside the nuclear lower window (L2–L4) and L5 is outside the nuclear lower window. The XOR bits only touch the outermost layers (L1, L5), leaving the nuclear core untouched.

---

## Task F: Counterfactual Analysis — Could the 6 Be Made Preserving?

For each non-preserving id-kernel bridge, we test: what if the orientation of the exit pair or entry pair were flipped?

| B# | Flip exit | Flip entry | Flip both | Constraint |
|:--:|:---------:|:----------:|:---------:|:----------:|
| B1 | no (ker=I) | no (ker=id, split) | no (ker=I) | Both free |
| B8 | no (ker=I) | no (ker=I) | no (ker=id, split) | Both free |
| B10 | no (ker=id, split) | no (ker=id, split) | no (ker=id, split) | Both free |
| B22 | **YES** (ker=id, one-sided) | **YES** (ker=id, one-sided) | no (ker=id, split) | Both free |
| B24 | **YES** (ker=id, one-sided) | **YES** (ker=id, one-sided) | no (ker=id, split) | Both free |
| B31 | no (ker=id, split) | no (ker=id, split) | no (same mask) | P31 S2-fixed |

### Three classes of non-preservation

**1. Structurally locked (B1, B8):** Flipping either adjacent pair destroys the id-kernel condition (introduces I-component). These bridges *cannot* be made preserving by any single orientation flip. The pair generators on either side of the bridge (id↔OM for B1, I↔OMI for B8) conspire to prevent it.

**2. Orientation-determined (B22, B24):** Flipping *either* adjacent pair produces preservation. These bridges could have been preserving under different orientation choices. The current non-preservation is a genuine orientation selection — and both adjacent pairs are free (not S2-constrained). The current orientation was *chosen* to not preserve here.

**3. Partially locked (B10, B31):** Flipping either pair keeps kernel = id but the distribution remains split. For B31, P31 is also S2-fixed. These bridges are locked by the specific pair content, not just orientation.

### The significance of B22 and B24

B22 and B24 are the key diagnostic cases. Both are free (no S2 constraint on either adjacent pair), and flipping either pair would produce preservation. The fact that KW's orientation *chooses* non-preservation here means developmental priority (the known orientation-selecting principle) does not optimize for trigram preservation at these positions.

What pairs are adjacent?
- B22: P22 (Guai/Gou) → P23 (Cui/Sheng). Fragility: KW-dom → KW-dom. Confidence: Clear → Clear.
- B24: P24 (Kun/Jing) → P25 (Ge/Ding). Fragility: trade-off → trade-off. Confidence: Suggestive → Clear.

B22 sits between two KW-dom pairs (algebra dominant). B24 sits between two trade-off pairs. There is no single fragility profile that characterizes the "chosen non-preservation" cases.

### Counterfactual for the 9 preserving bridges

| B# | Flip exit → | Flip entry → | Adjacent constraints |
|:--:|:----------:|:------------:|:---:|
| B3 | LOST (id, split) | LOST (id, split) | free, free |
| B6 | LOST (ker=M) | LOST (ker=M) | free, free |
| B11 | LOST (id, split) | LOST (id, split) | free, free |
| B12 | LOST (id, split) | LOST (id, split) | free, free |
| B13 | pres (id, one-sided) | LOST (ker=O) | free, S2 |
| B18 | LOST (ker=I) | LOST (ker=I) | free, free |
| B26 | LOST (ker=OI) | LOST (ker=OI) | free, S2 |
| B27 | LOST (ker=O) | LOST (ker=O) | S2, free |
| B30 | pres (id, one-sided) | LOST (ker=MI) | free, S2 |

**7 of 9 preserving bridges are fragile:** flipping either adjacent pair destroys preservation. 2 of 9 (B13, B30) survive one specific flip — and in both cases, the surviving flip is the one that *doesn't* touch the S2-constrained pair (the S2 pair can't flip anyway, so preservation survives the one available flip by coincidence).

This asymmetry is important: **preservation is easy to destroy, hard to create.** The 9 preserving bridges are delicately positioned — the right pair content at the right orientation. The 6 non-preserving bridges include 2 that could easily have been preserving (B22, B24) and 4 that are structurally locked out.

---

## Task G: Adjacent Pair Properties

### Fragility comparison

| | KW-dom | Trade-off | S2 |
|---|:---:|:---:|:---:|
| Preserving adj. pairs (18) | 2 (11%) | 12 (67%) | 4 (22%) |
| Non-preserving adj. pairs (12) | 7 (58%) | 4 (33%) | 1 (8%) |

The preserving/non-preserving split is strongly correlated with fragility:
- **Preserving bridges cluster at trade-off pairs** (67% vs 33%)
- **Non-preserving bridges cluster at KW-dom pairs** (58% vs 11%)

This extends the Round 4 finding. The trade-off pairs are where algebra is flexible and meaning is strong — and this is exactly where preservation occurs. The KW-dom pairs are where algebra is rigid — and this is where preservation fails (even when algebraically permitted).

### Meaning confidence comparison

| | Clear | Suggestive |
|---|:---:|:---:|
| Preserving adj. pairs (18) | 10 (56%) | 8 (44%) |
| Non-preserving adj. pairs (12) | 9 (75%) | 3 (25%) |

Non-preserving id-kernel bridges are adjacent to *more* Clear pairs (75% vs 56%). This is consistent with the KW-dom clustering: KW-dom pairs tend to have Clear confidence (the algebraic signal is already carrying meaning).

---

## Summary: The Selection Principle

### The complete theorem

**Trigram preservation at a KW bridge occurs if and only if:**
1. The bridge XOR mask has no palindromic component (kernel = id)
2. The bridge XOR mask's 1-bits all fall on one side of the trigram boundary

This is a two-level geometric gate:
- Level 1 (kernel): Do any mirror pairs flip symmetrically? If yes → both trigrams change.
- Level 2 (sidedness): Are the remaining asymmetric flips confined to one half? If yes → the other half's trigram is preserved.

### What the 6 non-preserving cases reveal

The 6 split into three structural classes:

| Class | Bridges | Character | Can become preserving? |
|-------|---------|-----------|:---:|
| Structurally locked | B1, B8 | L1+L5 delta; flip either pair → kernel ≠ id | No |
| Orientation-selected | B22, B24 | Both free; flip either pair → preserves | Yes (rejected) |
| Content-locked | B10, B31 | Flip either → still split; one partially S2-locked | No |

The structurally locked cases (B1, B8) are interesting: they have the XOR mask 100010, involving the O-pair's L1 and the M-pair's L5. These two bits, from different mirror pairs, happen to land on different sides of the boundary. But both bridges preserve nuclear lower trigrams — their "damage" is superficial (outermost lines only).

The orientation-selected cases (B22, B24) are the most diagnostic: here, preservation was *possible* and *rejected*. The developmental priority principle chose orientations that sacrifice trigram preservation at these positions. This confirms that developmental priority does not always align with trigram continuity — they are genuinely independent ordering principles that sometimes conflict.

### The spoiler bit pattern

5 of 6 spoiler bits are at position 0 (the bottom of the trigram — L1 or L4). The ruler line (position 1 — L2 or L5) never appears as a spoiler. The M mirror pair, which controls the ruler lines, never contributes a stray bit that disrupts preservation. Only O and I do.

This connects to M's unique symmetry (Round 1): M flips the same position in both trigrams, so its asymmetric contribution is always balanced. O and I cross positions (0↔2), creating the possibility of a single bit leaking across the boundary.

### The big picture

The selection principle is geometric: **the trigram boundary acts as a membrane, and preservation requires all changes to be on one side.** This is a structural consequence of the hexagram being decomposed two different ways:
- Mirror pairs: L1↔L6, L2↔L5, L3↔L4 (straddling the boundary)
- Trigrams: L1-L3 | L4-L6 (separated by the boundary)

The kernel = id condition ensures that no mirror pair straddles the boundary *symmetrically* (both members flipping). The one-sidedness condition ensures that no mirror pair straddles it *asymmetrically* (one member on each side). Together: zero straddling in any form → preservation.

The two-level gate echoes the permission-selection architecture identified across all rounds:
- **Permission** (kernel = id): algebraic — no palindromic structure
- **Selection** (one-sidedness): geometric — all changes confined to one trigram half

Whether a given bridge satisfies both conditions depends on both pair ordering and orientation. The count of 9/15 (60%) is close to the theoretical base rate (54%), meaning KW does not systematically over-select for preservation. But the *positions* where preservation occurs (trade-off pairs, meaning-rich transitions) and where it's rejected (KW-dom pairs, algebraically rigid positions) reveal the complementary coverage architecture.

---

## Data Files

| File | Contents |
|------|----------|
| `selection_analysis.py` | Complete computation script (915 lines) |
| `round5-selection.md` | This document |
