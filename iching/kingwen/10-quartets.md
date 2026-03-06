# 10. Quartet-Level Analysis of the King Wen Sequence

> Groups of 2 consecutive pairs (4 hexagrams). 16 quartets. What structure exists at this scale?

---

## Composition

Each quartet contains two consecutive pairs with their generator types. The generator change (ΔGEN) shows which generators switch between the two pairs.

```
Q1  OMI→OM   ΔI    乾坤 屯蒙          Q9  OM→OI   ΔMI   遯大壯 晉明夷
Q2  OI→M     ΔOMI  需訟 師比         Q10  MI→MI   =     家人睽 蹇解
Q3  I→OMI    ΔOM   小畜履 泰否       Q11  M→O     ΔOM   損益 夬姤
Q4  M→I      ΔMI   同人大有 謙豫     Q12  MI→I    ΔM    萃升 困井
Q5  OMI→OM   ΔI    隨蠱 臨觀         Q13  OM→OI   ΔMI   革鼎 震艮
Q6  I→O      ΔOI   噬嗑賁 剝復       Q14  OMI→O   ΔMI   漸歸妹 豐旅
Q7  MI→OMI   ΔO    無妄大畜 頤大過   Q15  OI→O    ΔI    巽兌 渙節
Q8  OMI→M    ΔOI   坎離 咸恆         Q16  OMI→OMI =     中孚小過 既濟未濟
```

---

## Finding 1: Quartet Centers Collapse Into 7 Equivalence Classes

16 quartets share only 7 distinct center positions:

| Center | Quartets | Count |
|--------|----------|:-----:|
| [0.50, 0.50, 0.25, 0.25, 0.50, 0.50] | Q1, Q5 | 2 |
| [0.50, 0.25, 0.75, 0.75, 0.25, 0.50] | **Q4, Q9, Q13, Q14** | 4 |
| [0.75, 0.75, 0.50, 0.50, 0.75, 0.75] | Q3, Q11 | 2 |
| [0.50, 0.50, 0.50, 0.50, 0.50, 0.50] | Q10, Q16 | 2 |
| others | Q2, Q6, Q7, Q8, Q12, Q15 | 1 each |

Four quartets (Q4, Q9, Q13, Q14) share the exact same center — all with the pattern [½, ¼, ¾, ¾, ¼, ½]. This center has mirror symmetry (dim 1=dim 6, dim 2=dim 5, dim 3=dim 4) and is biased toward yang on inner lines, yin on middle lines.

Q10 and Q16 sit at the perfect center [½, ½, ½, ½, ½, ½]. Q10 is MI→MI (same generator repeated) and Q16 is OMI→OMI (the sequence's final quartet).

---

## Finding 2: Weight Trajectories Are Step Functions

Within each quartet, the yang count follows the pattern **W, W, W', W'** — constant within each pair, then stepping to a new value at the bridge:

```
Q1:  6→0→2→2    Q9:  4→4→2→2
Q2:  4→4→1→1    Q10: 4→4→2→2
Q3:  5→5→3→3    Q11: 3→3→5→5
Q4:  5→5→1→1    Q12: 2→2→3→3
Q5:  3→3→2→2    Q13: 4→4→2→2
Q6:  3→3→1→1    Q14: 3→3→3→3
Q7:  4→4→2→4    Q15: 4→4→3→3
Q8:  2→4→3→3    Q16: 4→2→3→3
```

13/16 quartets follow W,W,W',W' exactly. The exceptions (Q7, Q8, Q16) involve complement pairs where the weight can flip. Weight changes happen at bridges, not within pairs — confirming that the bridge is where actual structural movement occurs.

Most quartets decrease in weight (10/16 have W' < W). The sequence tends to drift from yang-heavy to yin-heavy within each quartet.

---

## Finding 3: Seven Parallelogram Quartets

7 of 16 quartets form **parallelograms** in the hypercube — opposite sides have equal Hamming distance:

| Quartet | Pairs | Side lengths | Structure |
|---------|-------|:----------:|-----------|
| Q4 | M→I | 2, 4 | small intra-pair, large bridge |
| Q6 | I→O | 2, 2 | all edges equal (rhombus) |
| Q9 | OM→OI | 4, 2 | |
| Q10 | MI→MI | 4, 2 | same generator, diff subcubes |
| Q11 | M→O | 2, 4 | |
| Q13 | OM→OI | 4, 2 | repeats Q9's structure |
| Q16 | OMI→OMI | 6, 3 | largest parallelogram |

The parallelograms arise when the bridge transition has the same geometric relationship as the cross-pair diagonal. Q6 (I→O) is the tightest: all 6 pairwise distances are 2 — a rhombus confined to 4 dimensions.

---

## Finding 4: Complementary vs Overlapping Change

The Jaccard overlap between a quartet's two pair masks reveals two distinct types:

**Zero overlap (J=0.00)** — Q2, Q4, Q6, Q11: the two pairs change completely different lines.
- Q4: M→I changes L2,L5 then L3,L4 — all 4 middle/inner lines touched, outer untouched
- Q6: I→O changes L3,L4 then L1,L6 — inner then outer, middle untouched
- These quartets achieve **maximum line coverage** relative to their pair sizes

**Full overlap (J=1.00)** — Q10, Q16: both pairs change the exact same lines.
- Q10: MI→MI — same mask repeated
- Q16: OMI→OMI — both complements

**Intermediate** — the rest have 2-4 shared lines between masks.

Union mask is 111111 (all lines) for 10/16 quartets — the quartet level almost always touches every line, even when individual pairs only change 2 or 4.

---

## Finding 5: Offset 4 Is the Natural Quartet Period

Quartet centers are closest at offset 4 (mean distance 0.601) and its complement offset 12. This is one-quarter of the 16-quartet ring, confirming the period-4 structure seen in line spectral analysis.

The quartet sequence has a natural 4-fold periodicity in the hypercube: Q_k tends to revisit Q_{k+4}'s neighborhood.

---

## Finding 6: No Mirror Symmetry Between Canons

Comparing Q_k with Q_{17-k} (first half vs second half reversed): no generator pair matches, no reversed matches. The two halves of the quartet sequence are structurally independent — there is no palindromic or mirror organization at this level.

---

## Summary

At the quartet level:

1. **Centers collapse** — 16 quartets → 7 positions, with 4 quartets sharing one center
2. **Weight is a step function** — constant within pairs, stepping at bridges
3. **Parallelogram structure** — 7/16 quartets form parallelograms in the hypercube
4. **Complementary change types** — some quartets change disjoint lines (J=0), maximizing coverage
5. **Period-4 offset** — the natural periodicity of quartets in the hypercube
6. **Union masks are mostly complete** — 10/16 quartets touch all 6 lines

The quartet is where the sequence achieves full line coverage: individual pairs change 2-6 lines, but pairs of pairs almost always touch all 6. The pairing provides inversion within a subcube; the quartet provides coverage across subcubes.
