# 9. Generator Sequence and Hypercube Geometry

> Does the order in which change types appear relate to the geometric structure of the subcubes they occupy?

---

## Setup

Each of the 32 pairs has a change type from the Boolean lattice {O, M, I}. The sequence of these types defines a path through the lattice. Simultaneously, each pair occupies a subcube of {0,1}^6 identified by its fixed-line values. The question: does the abstract path (lattice) relate to the concrete path (hypercube)?

Generator sequence:

```
 1. OMI   乾坤        17. OM    遯大壯
 2. OM    屯蒙        18. OI    晉明夷
 3. OI    需訟        19. MI    家人睽
 4. M     師比        20. MI    蹇解
 5. I     小畜履      21. M     損益
 6. OMI   泰否        22. O     夬姤
 7. M     同人大有    23. MI    萃升
 8. I     謙豫        24. I     困井
 9. OMI   隨蠱        25. OM    革鼎
10. OM    臨觀        26. OI    震艮
11. I     噬嗑賁      27. OMI   漸歸妹
12. O     剝復        28. O     豐旅
13. MI    無妄大畜    29. OI    巽兌
14. OMI   頤大過      30. O     渙節
15. OMI   坎離        31. OMI   中孚小過
16. M     咸恆        32. OMI   既濟未濟
```

---

## Finding 1: Three Independent Binary Signals

Each generator (O, M, I) is active in exactly 20/32 pairs (62.5%). All pairwise correlations are r = -0.067 — effectively zero.

This mirrors the line-level finding: the six lines are independent binary signals at the hexagram level, and the three generators are independent binary signals at the pair level. Independence is preserved across scales.

---

## Finding 2: The Sequence Diversifies Change Types

The path through the Boolean lattice takes larger steps than random:

| Lattice step | Count | Meaning |
|:---:|:---:|---------|
| 0 | 3 | same type repeated |
| 1 | 9 | one generator added or removed |
| 2 | 14 | two generators change (swap) |
| 3 | 5 | all three generators change |

Mean step: 1.68. Random permutations average 1.45 ± 0.14 (p = 0.066). The sequence tends to change which generators are active rather than repeating the same change type. It maximizes diversity in the type of change applied.

The 3 zero-step transitions (same type repeated) are: pairs 14→15 (OMI→OMI), pairs 19→20 (MI→MI), pairs 31→32 (OMI→OMI). Two of these are at the very end of the sequence.

---

## Finding 3: Center Distance Tracks Generator Changes

| Metric pair | Correlation |
|------------|:-----------:|
| Lattice distance ↔ Center distance | **r = +0.50** |
| Bridge Hamming ↔ Center distance | r = +0.44 |
| Lattice distance ↔ Bridge Hamming | r = -0.02 |

When the generator type changes, the pair center moves in the hypercube. But the actual bridge Hamming distance (how many bits flip between the exit hexagram of one pair and the entry hexagram of the next) is completely uncorrelated with the generator change.

The abstract structure (Boolean lattice path) and the concrete structure (vertex-to-vertex path) are **decoupled**. The lattice determines *where* in the hypercube you are (center), but not *how* you get there (bridge). The bridges are genuinely free — they don't follow the lattice.

---

## Finding 4: 4-Flip Groups Traverse Subcubes Symmetrically

Each 4-flip group visits its two complementary subcubes in a structured order:

| Group | Positions | Subcube keys | Pattern |
|-------|-----------|:------------:|---------|
| OM | 2, 10, 17, 25 | 00, 00, 11, 11 | first half → complement |
| MI | 13, 19, 20, 23 | 11, 11, 00, 00 | mirror of OM |
| OI | 3, 18, 26, 29 | 11, 00, 00, 11 | cross pattern |

OM and MI mirror each other — OM starts in the 00-subcube and moves to 11; MI starts in 11 and moves to 00. OI crosses: 11→00→00→11.

---

## Finding 5: 2-Flip Groups Share a Subcube Ordering

All three 2-flip groups visit the same 4 palindromic subcube keys, but in related orders:

| Group | Positions | Subcube key weights |
|-------|-----------|:-------------------:|
| O | 12, 22, 28, 30 | 0, 4, 2, 2 |
| M | 4, 7, 16, 21 | 0, 4, 2, 2 |
| I | 5, 8, 11, 24 | 4, 0, 2, 2 |

O and M visit subcubes in identical weight order: empty (0000) → full (1111) → mixed (0110) → mixed (1001). I visits them in complement order: full → empty → mixed → mixed.

---

## Finding 6: Period-8 Structure in Subcube Weight

Assigning each pair a "subcube weight" (sum of fixed-key values, with OMI = 3 as virtual center):

```
3 0 2 0 4 3 4 0 | 3 0 2 0 2 3 3 2 | 2 0 2 0 2 4 0 2 | 2 0 3 2 2 2 3 3
```

Autocorrelation peaks at lag 8 (r = +0.459) — the path revisits similar hypercube regions every 8 pairs (quarter of the sequence). This is consistent with the 4-flip groups' 2+2 subcube split and the overall period-4 structure in the hexagram sequence.

---

## Finding 7: Generator Autocorrelation Structure

Each generator has distinct temporal dynamics:

| Generator | lag 1 | lag 3 | lag 16 | Character |
|-----------|:-----:|:-----:|:------:|-----------|
| O | +0.07 | +0.33 | **+0.47** | slow — repeats state at half-sequence |
| M | -0.20 | -0.20 | -0.07 | alternating — tends to flip each step |
| I | **-0.33** | -0.07 | -0.33 | strongly alternating — anti-persists |

O is the most persistent generator — if it's active, it tends to stay active. I is the most volatile — it switches on and off rapidly. M is intermediate. This creates a hierarchy of change rates: outer lines change slowly, inner lines change fast.

---

## Finding 8: Path Hamming Budget

| Component | Total Hamming | Share |
|-----------|:------------:|:-----:|
| Intra-pair (diagonals) | 120 | 56.9% |
| Bridges (free) | 91 | 43.1% |
| **Total** | **211** | |

More than half the path's total movement is the structured inversion/complement within pairs. The bridges — the actual ordering choices — account for less than half. The sequence is majority-determined by its pairing structure; the ordering freedom is secondary.

---

## Summary

The generator sequence and hypercube geometry are related but decoupled:

1. **Generators are independent and balanced** — three uncorrelated binary signals, each at 62.5%
2. **The sequence diversifies** — larger lattice steps than random (p = 0.066), avoids repeating change types
3. **Lattice position → hypercube position** — changing generators moves the center (r = +0.50)
4. **Lattice position ↛ bridge path** — bridge Hamming is uncorrelated with generator change (r = -0.02)
5. **4-flip groups cross their subcubes symmetrically** — OM/MI mirror, OI crosses
6. **Period-8 structure** — subcube weight repeats every 8 pairs
7. **O is slow, I is fast** — the three generators have different persistence, creating a hierarchy of change rates
8. **57% of the path is structural** — the diagonals dominate; bridges are the minority

The King Wen sequence operates on two levels simultaneously: a structured diagonal tiling (the pairing) and a diversifying walk through the Boolean lattice of change types (the ordering). The pairing determines where you are; the ordering determines what kind of change happens next. They share a center-of-mass but not a path.
