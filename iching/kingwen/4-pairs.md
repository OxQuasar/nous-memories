# 4. Pair-Level Analysis of the King Wen Sequence

> Treat each adjacent pair of hexagrams as a unit. 32 pairs, each an inversion or complement. What structure exists between them?

---

## Representation

Each pair (hex[2k], hex[2k+1]) is characterized by:
- **Internal mask**: XOR of the two hexagrams — which lines flip within the pair
- **Center**: midpoint (a+b)/2 in R^6 — where the pair sits in the hypercube
- **Bridge**: the transition from one pair's exit to the next pair's entry

---

## Finding 1: Only 7 Mask Types (Moving Lines)

The 32 pairs use exactly 7 internal XOR patterns:

| Mask | Flips | Count | Lines that flip |
|------|:-----:|:-----:|-----------------|
| 111111 | 6 | 8 | all lines (complement) |
| 110011 | 4 | 4 | L1, L2, L5, L6 (outer + middle) |
| 101101 | 4 | 4 | L1, L3, L4, L6 (outer + inner) |
| 011110 | 4 | 4 | L2, L3, L4, L5 (middle + inner) |
| 010010 | 2 | 4 | L2, L5 (middle only) |
| 001100 | 2 | 4 | L3, L4 (inner only) |
| 100001 | 2 | 4 | L1, L6 (outer only) |

The complement mask appears 8 times. Each of the other 6 masks appears exactly 4 times. 8 + 6×4 = 32.

Every line flips in exactly 20/32 pairs (62.5%) — perfect per-line balance.

---

## Finding 2: Masks Form Complementary Pairs

The 6 non-complement masks pair into three complementary sets:

| 2-flip mask | 4-flip mask | Structure |
|:-----------:|:-----------:|-----------|
| `100001` | `011110` | outer ↔ middle+inner |
| `010010` | `101101` | middle ↔ outer+inner |
| `001100` | `110011` | inner ↔ outer+middle |

Each 2-flip mask is the bitwise complement of a 4-flip mask. Each appears exactly 4 times. The three mirror-position pairs (L1↔L6, L2↔L5, L3↔L4) are the atomic units — every mask is a combination of these pairs. The complement mask activates all three; the 4-flip masks activate two; the 2-flip masks activate one.

The flip count distribution is:
- 2 lines: 12 pairs (3 mask types × 4)
- 4 lines: 12 pairs (3 mask types × 4)
- 6 lines: 8 pairs (1 mask type × 8)

---

## Finding 3: Bridges Are Free

Intra-pair transitions follow the 7 rigid masks. Inter-pair bridges are the opposite — nearly all unique.

|  | Intra-pair | Bridge |
|--|-----------|--------|
| Unique masks | 7/32 | 23/31 |
| Mean Hamming | 3.75 | 2.94 |
| Inversions | ~24/32 | 0/31 |
| Complements | 8/32 | 1/31 |

Bridges are lighter (fewer bits flip), more diverse, and structurally unconstrained. The pair-internal transition is determined by the pairing rule (inversion or complement). The bridge is where the King Wen sequence exercises its ordering freedom.

Bridge per-line flip frequency is uneven (L2: 12/31, L6: 18/31), unlike the perfect 20/32 balance of intra-pair flips. The bridges don't maintain the same symmetry as the pairs themselves.

---

## Finding 4: Eight Complement Pairs at the Hypercube Center

The 8 complement pairs (mask 111111) have their center at exactly [½, ½, ½, ½, ½, ½] — the geometric center of the hypercube. These pairs straddle the origin: their two hexagrams are maximally opposite, so their midpoint is perfectly centered.

The other 24 pairs are displaced from center. Their centers take values from {0, 0.5, 1} per dimension: 0 means both hexagrams have yin at that line, 1 means both have yang, 0.5 means they differ.

Center equivalence classes (pairs with identical centers):

| Center | Pairs | Mask |
|--------|-------|------|
| ½½½½½½ | 1, 6, 9, 14, 15, 27, 31, 32 | 111111 |
| ½½00½½ | 2, 10 | 110011 |
| ½1½½1½ | 3, 29 | 101101 |
| 1½½½½1 | 13, 19 | 011110 |
| ½½11½½ | 17, 25 | 110011 |
| ½0½½0½ | 18, 26 | 101101 |
| 0½½½½0 | 20, 23 | 011110 |

Pairs with the same mask can have different centers (they flip the same lines but start from different positions). Pairs with the same center necessarily have the same mask.

---

## Finding 5: Both Canons Use All 7 Masks

The Upper Canon (pairs 1-15) and Lower Canon (pairs 16-32) share all 7 mask types. Zero masks are exclusive to either half.

| | 2-flip | 4-flip | 6-flip |
|--|:------:|:------:|:------:|
| Upper Canon | 6 | 4 | 5 |
| Lower Canon | 6 | 8 | 3 |

The Lower Canon has more 4-flip pairs and fewer complements, but uses the same vocabulary. The change mechanisms are universal; their frequency shifts between halves.

---

## Finding 6: Consecutive Pairs Tend to Change Mask Type

Mask Hamming distance between consecutive pairs (how different their internal masks are):

| Mask distance | Count |
|:---:|:---:|
| 0 (same mask) | 3 |
| 2 | 9 |
| 4 | 14 |
| 6 (opposite mask) | 5 |

Mean: 3.35 (random: 2.90 ± 0.28, p=0.04 one-tail). Consecutive pairs tend to have *more different* masks than random — the sequence avoids repeating the same type of change. It diversifies which lines participate from one pair to the next.

Mean Jaccard overlap between consecutive pair masks: 0.37. About a third of the flipping lines carry over from one pair to the next; two-thirds are new.

---

## Finding 7: Pair Offset Structure

At the pair level (32 units on a ring), center distance is minimized at offsets 8 and 24 (mean distance 0.827). These are each other's complements (8 + 24 = 32), suggesting a quarter-period structure: pairs separated by 8 positions tend to occupy similar regions of the hypercube.

Mask matches peak at offsets 6 and 26 (7/32 matches each — also complements). Pairs separated by 6 tend to use the same internal mask.

---

## Summary

The 32 pairs have a precise combinatorial structure:

1. **7 mask types** — complement (×8) plus 3 complementary pairs of 2-flip/4-flip masks (×4 each)
2. **Mirror-position pairs are the atoms** — every mask is built from {L1↔L6, L2↔L5, L3↔L4} toggling as units
3. **Intra-pair is rigid, inter-pair is free** — the pairing determines the internal mask; the bridges between pairs carry the sequence's ordering choices
4. **Complement pairs anchor the center** — 8 pairs sit at the hypercube midpoint, the other 24 are displaced
5. **Consecutive pairs diversify** — the sequence avoids repeating mask types, rotating which lines participate in change
6. **Both halves use the same vocabulary** — all 7 masks appear in both canons

The pair structure is a **7-letter alphabet of change types**, each built from combinations of the three mirror-position line pairs. The sequence spells out a path through this alphabet that maximizes diversity between consecutive letters.
