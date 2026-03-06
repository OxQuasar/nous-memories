# 7. Mask Group Analysis of the King Wen Sequence

> The 32 pairs use 7 internal masks. What structure exists within and between these groups?

---

## Finding 1: Every Group Contains All 8 Trigrams Exactly Once << THIS >>

Each mask group's hexagrams collectively use all 8 possible upper trigrams exactly once and all 8 possible lower trigrams exactly once. This holds for every group — the 8-pair complement group (16 hexagrams, 2 of each trigram) and every 4-pair group (8 hexagrams, 1 of each trigram).

The mask groups are **complete trigram sets**. No trigram is overrepresented or missing in any group. This means each change type (mask) draws from the full vocabulary of trigrams, never specializing.

---

## Finding 2: Weight Is Always Preserved

For non-complement pairs (masks with 2 or 4 flips), both hexagrams always have **identical weight** (number of yang lines). |A-B| = 0 for all 24 non-complement pairs.

This is a necessary consequence of inversion: reversing bit order doesn't change the count of 1s. The complement pairs have A+B = 6 (always sums to 6). Across all groups, mean A+B = 6.0 exactly.

---

## Finding 3: Fixed Lines Are Mirror-Symmetric

For non-complement pairs, the lines that don't flip (fixed lines) must satisfy the inversion constraint: if line k is fixed, then line (7-k) must also be fixed at the same value (since inversion maps k↔7-k).

**4-flip groups** (2 fixed lines — a mirror pair):
- Only patterns `00` and `11` appear — both fixed lines are either both yin or both yang
- Each pattern appears exactly 2 times per group
- Coverage: 2/4 possible patterns

**2-flip groups** (4 fixed lines — two mirror pairs):
- Only 4 patterns appear: `0000`, `0110`, `1001`, `1111`
- These are exactly the 4 palindromic patterns (L1=L6, L2=L5 for inner; similarly for others)
- Each pattern appears exactly 1 time per group
- Coverage: 4/16 possible patterns

The fixed-line patterns enumerate every way to assign values to the mirror-position pairs. The constraint is not "any combination of fixed values" but specifically "mirror-symmetric combinations."

---

## Finding 4: The Mask Algebra (Moving lines)

The 7 masks decompose into three atomic mirror-pair operations:

| Atom | Lines | Notation |
|------|-------|----------|
| Outer | L1, L6 | **O** |
| Middle | L2, L5 | **M** |
| Inner | L3, L4 | **I** |

Every mask is a combination of these atoms:

| Mask | Atoms | Flips |
|------|-------|:-----:|
| `100001` | O | 2 |
| `010010` | M | 2 |
| `001100` | I | 2 |
| `110011` | O+M | 4 |
| `101101` | O+I | 4 |
| `011110` | M+I | 4 |
| `111111` | O+M+I | 6 |

The masks form a Boolean lattice on {O, M, I}:
- 3 singletons (2-flip)
- 3 pairs (4-flip)
- 1 triple (6-flip, complement)

Each singleton mask is the complement of a pair mask: O ↔ M+I, M ↔ O+I, I ↔ O+M. The XOR distance between masks equals 2× the number of atoms that differ.

---

## Finding 5: Subcube Occupation

Each mask group occupies subcubes of the hypercube determined by its fixed-line values:

| Group | Subcube dim | Subcubes occupied | Vertices per subcube |
|-------|:----------:|:-----------------:|:-------------------:|
| O+M+I (complement) | 6 | 1/1 | 16/64 |
| O+M, O+I, M+I (4-flip) | 4 | 2/4 | 4/16 |
| O, M, I (2-flip) | 2 | 4/16 | 2/4 |

The 4-flip groups each occupy exactly 2 of 4 possible 4D subcubes — the two palindromic subcubes (fixed pair both yin, or both yang). The 2-flip groups occupy 4 of 16 possible 2D subcubes — the 4 doubly-palindromic subcubes.

In total: 16 + 3×8 + 3×8 = 64 hexagrams. Every hexagram belongs to exactly one mask group. The groups partition the hypercube.

---

## Finding 6: Transition Structure Between Groups

The sequence transitions between mask groups follow a pattern:

| Transition | Count | Notes |
|-----------|:-----:|-------|
| complement → complement | 2 | self-loops |
| 4-flip → 4-flip | 4 | especially O+M → O+I (3x) |
| 2-flip → complement | 3 | |
| complement → 2-flip | 3 | |
| 2-flip → 2-flip | 3 | especially M → I (2x) |
| 4-flip → 2-flip | 4 | |
| 2-flip → 4-flip | 4 | |

No single transition dominates. The sequence moves fairly freely between all mask types, with a slight tendency to alternate flip counts (2→6→2 or 2→4→2) rather than staying at the same level.

---

## Finding 7: Sequence Positions

**Complement pairs** (positions 1, 6, 9, 14, 15, 27, 31, 32) bookend the sequence (pairs 1 and 32) and cluster at the boundary between canons (14, 15). They appear at irregular intervals.

**Outer+middle pairs** (positions 2, 10, 17, 25) are the most regular — gaps of 8, 7, 8. Nearly periodic with period ~8.

**Outer+inner** (3, 18, 26, 29) and **middle+inner** (13, 19, 20, 23) cluster in the second half.

**The 2-flip groups** scatter throughout without obvious periodicity.

---

## Summary

The pair structure reveals a clean algebraic organization:

1. **Three atomic operations** — O (outer), M (middle), I (inner) mirror-pair flips
2. **7 masks = all non-empty subsets** of {O, M, I} — a complete Boolean lattice
3. **Every group is a complete trigram set** — no change type is biased toward particular trigrams
4. **Fixed lines obey mirror symmetry** — constrained to palindromic patterns
5. **Weight is invariant** — inversion preserves yang count; complement pairs sum to 6
6. **Groups partition the hypercube** into subcubes of dimension 2, 4, and 6

The King Wen pairs don't just alternate between states — they systematically exercise every combination of the three independent change axes, with each combination drawing evenly from the full trigram vocabulary. The structure is a **complete Boolean algebra of change** built on three mirror-symmetric generators.

## The Sequence

   1. OMI    乾  - 坤 
   2. OM     屯  - 蒙
   3. OI     需  - 訟
   4. M      師  - 比
   5. I      小畜- 履 
   6. OMI    泰  - 否
   7. M      同人- 大有                                                            
   8. I      謙  - 豫
   9. OMI    隨  - 蠱
  10. OM     臨  - 觀
  11. I      噬嗑- 賁
  12. O      剝  - 復
  13. MI     無妄- 大畜
  14. OMI    頤 - 大過
  15. OMI    坎 - 離
  16. M      咸 - 恆
  17. OM     遯 - 大壯
  18. OI     晉 - 明夷
  19. MI     家人- 睽
  20. MI     蹇 -  解
  21. M      損 -  益 
  22. O      夬 -  姤
  23. MI     萃 -  升
  24. I      困 -  井
  25. OM     革 -  鼎
  26. OI     震 -  艮
  27. OMI    漸 - 歸妹
  28. O      豐 - 旅 
  29. OI     巽 - 兌
  30. O      渙 - 節
  31. OMI    中孚-小過
  32. OMI    既濟-未濟


OMI  OM  OI  M  I  OMI  M  I  OMI  OM  I  O  MI  OMI  OMI  M  OM  OI  MI  MI  M  O  MI  I  OM  OI  OMI  O  OI  O  OMI  OMI
