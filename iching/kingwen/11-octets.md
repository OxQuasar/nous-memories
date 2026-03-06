#  11. Octet-Level Analysis of the King Wen Sequence

> Groups of 4 consecutive pairs (8 hexagrams). 8 octets total. What structure exists at this coarsest sequential scale?

---

## Composition

Each octet contains four consecutive pairs with their generator types.

```
O1  OMI→OM→OI→M     乾坤 屯蒙 需訟 師比
O2  I→OMI→M→I        小畜履 泰否 同人大有 謙豫
O3  OMI→OM→I→O       隨蠱 臨觀 噬嗑賁 剝復
O4  MI→OMI→OMI→M     無妄大畜 頤大過 坎離 咸恆
O5  OM→OI→MI→MI      遯大壯 晉明夷 家人睽 蹇解
O6  M→O→MI→I         損益 夬姤 萃升 困井
O7  OM→OI→OMI→O      革鼎 震艮 漸歸妹 豐旅
O8  OI→O→OMI→OMI     巽兌 渙節 中孚小過 既濟未濟
```

---

## Finding 1: Every Octet Covers All 6 Lines

Union mask is `111111` for all 8 octets. Four pairs is sufficient to guarantee that every line position is changed at least once, regardless of which generators appear.

Intersection masks vary: most are `000000` (no line is changed by every pair), but O4 intersects on `010010` (M lines) and O7, O8 intersect on `100001` (O lines) — reflecting their "always active" generators.

---

## Finding 2: All Octets Span the Full Hypercube

Every octet's 8 vertices vary across all 6 dimensions — no octet is confined to a subcube. The 8 hexagrams always spread across the full {0,1}^6, never collapsing into a 3-cube or smaller subspace.

Mean pairwise Hamming distances range from 2.79 (O3, tightest cluster) to 3.36 (O4, most dispersed). The theoretical maximum for 8 random vertices is 3.0, so octets cluster near the expected spread.

---

## Finding 3: Generator Lock-In Across the Sequence

The "always active" generator per octet reveals a structural drift:

| Octet | Always Active | Vocabulary |
|-------|:---:|---|
| O1 | ∅ | OMI, OM, OI, M |
| O2 | ∅ | I, OMI, M |
| O3 | ∅ | OMI, OM, I, O |
| O4 | **M** | MI, OMI, M |
| O5 | ∅ | OM, OI, MI |
| O6 | ∅ | M, O, MI, I |
| O7 | **O** | OM, OI, OMI, O |
| O8 | **O** | OI, O, OMI |

The first half (O1–O3) has no universal generator — maximum diversity. O4 locks M (middle lines always change). O7 and O8 lock O (outer lines always change). The sequence progressively constrains which lines participate.

---

## Finding 4: O7 Has Perfect Generator Parity

The XOR of all 4 generator bit-patterns within each octet:

```
O1: OM    O2: OI    O3: O     O4: I
O5: MI    O6: O     O7: 0     O8: I
```

O7 is the only octet where XOR = 0 — its generators (OM, OI, OMI, O) cancel perfectly. Every generator bit appears an even number of times. This makes O7 the most internally balanced octet in the sequence.

---

## Finding 5: Trigram Coverage Is Incomplete

No octet achieves full 8-trigram coverage in either upper or lower position. Best is 6/8 (O4, O5, O6). This contrasts with the mask-group analysis where every group contains all 8 trigrams exactly once — sequential grouping doesn't inherit that property.

The early octets (O1–O3) are especially constrained, using only 4–5 of 8 trigrams. Coverage improves toward the middle of the sequence.

---

## Finding 6: O4–O5 Are the Closest Mirror Pair

Comparing O_k with O_{9-k} (first half vs second half reversed):

| Mirror Pair | Center Distance | Shared Generators | Weight Sums |
|:-----------:|:---:|:---:|:---:|
| O1 ↔ O8 | 0.306 | OMI, OI | 20 + 26 = 46 |
| O2 ↔ O7 | 0.433 | OMI | 28 + 24 = 52 |
| O3 ↔ O6 | 0.866 | O, I | 18 + 26 = 44 |
| O4 ↔ O5 | **0.177** | MI | 26 + 24 = 50 |

O4–O5 (the central pair, splitting the sequence at hexagram 32/33) are geometrically closest in the hypercube. O3–O6 are the most distant — the boundaries between the first/second quarters and third/fourth quarters are structurally dissimilar.

No mirror pair sums to the balanced weight of 48. The canons are not weight-symmetric at the octet level.

---

## Finding 7: Weight Trajectories Drift Downward

7 of 8 octets have non-positive net weight change (yang drains within each octet):

```
O1: 6→1  Δ=-5    O5: 4→2  Δ=-2
O2: 5→1  Δ=-4    O6: 3→3  Δ= 0
O3: 3→1  Δ=-2    O7: 4→3  Δ=-1
O4: 4→3  Δ=-1    O8: 4→3  Δ=-1
```

O1 has the most dramatic drop (6→1, from Qian/pure yang to Bi/mostly yin). O6 is the only neutral octet. The downward drift is strongest in the first canon (O1–O4) with total Δ=-12, while the second canon (O5–O8) drifts only Δ=-4.

---

## Summary

At the octet level:

1. **Complete line coverage** — every octet touches all 6 lines, guaranteed by 4 diverse generators
2. **Full-dimensional spread** — 8 vertices always span all 6 dimensions, never collapsing to a subcube
3. **Progressive generator lock-in** — early octets are maximally diverse; later ones lock O or M as always-active
4. **O7's perfect parity** — the only octet where generator XOR = 0 (all bits cancel)
5. **Incomplete trigram coverage** — sequential grouping doesn't achieve the all-8-trigrams property of mask groups
6. **Central mirror symmetry** — O4↔O5 are the closest mirror pair, the sequence's geometric midpoint
7. **Yang drainage** — 7/8 octets lose yang; the first canon drains 3× faster than the second

The octet is the scale at which the sequence's directional character becomes visible: a progressive movement from yang-heavy to yin-heavy, with structural constraints tightening as the sequence proceeds.
