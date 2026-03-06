# 8. Subcube Occupation in the King Wen Sequence

> Every pair is a main diagonal. The 7 mask groups tile the hypercube by diagonals at three scales.

---

## Setup

Each pair lives in a subcube of {0,1}^6 defined by its mask. The mask's 1-bits are the "flip dimensions" (lines that change within the pair). The 0-bits are "fixed dimensions" (lines that don't change). The fixed-dimension values identify *which* subcube the pair occupies.

- **2-flip pairs** (O, M, I): live in 2D faces (squares) of the hypercube. 4 fixed dims → 2^4 = 16 possible faces per group.
- **4-flip pairs** (OM, OI, MI): live in 4D subcubes (tesseracts). 2 fixed dims → 2^2 = 4 possible tesseracts per group.
- **6-flip pairs** (OMI): live in the full 6D cube. No fixed dims.

---

## Finding 1: Every Pair Is a Main Diagonal

Within its subcube, every pair connects two opposite corners — the projected XOR is all 1s.

| Group | Subcube dim | Projected XOR |
|-------|:----------:|:-------------:|
| O, M, I | 2D | 11 |
| OM, OI, MI | 4D | 1111 |
| OMI | 6D | 111111 |

No pair is an edge, face diagonal, or partial flip. Every pair spans the **maximum possible distance** within its subcube. The two hexagrams in each pair are as far apart as their change type allows.

---

## Finding 2: Perfect Balance in Every Half-Space

Every mask group distributes its vertices exactly 50/50 between yin and yang on every dimension:

| Group | Vertices | Per half-space |
|-------|:--------:|:--------------:|
| OMI | 16 | 8 / 8 |
| OM, OI, MI | 8 each | 4 / 4 |
| O, M, I | 8 each | 4 / 4 |

This holds for all 6 dimensions simultaneously. No group favors any line position or polarity. The tiling is isotropic.

---

## Finding 3: 2-Flip Groups Occupy the Same 4 Faces

All three 2-flip groups (O, M, I) occupy faces indexed by the same 4 fixed-line patterns:

| Fixed pattern | Structure |
|:---:|-----------|
| `0000` | all fixed lines yin |
| `0110` | inner mirror pair yang, outer yin |
| `1001` | outer mirror pair yang, inner yin |
| `1111` | all fixed lines yang |

These are the 4 palindromic patterns — the only patterns where each mirror-position pair (L1=L6, L2=L5 or equivalent) has matching values. The inversion constraint forces palindromic fixed lines.

The 4 face keys form a structure: `0000 ↔ 1111` at Hamming distance 4, `0110 ↔ 1001` at Hamming distance 4, and all other pairs at Hamming distance 2. Two complementary pairs of faces, cross-linked at distance 2.

---

## Finding 4: Each Face Is Partitioned Into Two Diagonals

A 2D face (square) has 4 vertices: `{00, 01, 10, 11}`. These form two diagonals: `{01, 10}` and `{00, 11}`.

In every face occupied by a 2-flip group:
- The **2-flip pair** occupies one diagonal: `{01, 10}` or `{10, 01}`
- The **OMI complement pair** occupies the other diagonal: `{00, 11}`

The two missing vertices in every 2-flip face always belong to OMI. The face is perfectly split between a single-generator change (one mirror pair flips) and a full complement change (all lines flip).

This means the 2-flip groups and OMI are **interlocked at the face level**: they jointly tile every occupied 2D face into two perpendicular diagonals.

---

## Finding 5: 4-Flip Groups Occupy Complementary Subcube Pairs

Each 4-flip group occupies exactly 2 of 4 possible 4D subcubes. The two occupied subcubes always have complementary fixed-line values:

| Group | Fixed dims | Subcube keys |
|-------|-----------|:------------:|
| OM | L3, L4 | {00, 11} |
| OI | L2, L5 | {00, 11} |
| MI | L1, L6 | {00, 11} |

The fixed dimensions are **orthogonal** across groups — no two 4-flip groups share any fixed dimension. OM fixes the inner pair, OI fixes the middle pair, MI fixes the outer pair.

The 12 missing vertices in each 4D subcube split evenly:
- 4 belong to the two constituent single-generator groups
- 4 belong to OMI

For example, in OM's subcube [00]: the 12 missing vertices include 4 from O, 4 from M, and 4 from OMI.

---

## Finding 6: The Tiling Structure

The 64 vertices of {0,1}^6 are partitioned into 32 pairs, each a main diagonal of a subcube:

| Scale | Group | Pairs | Vertices | Subcubes used |
|:-----:|-------|:-----:|:--------:|:-------------:|
| 6D | OMI | 8 | 16 | 1 (the full cube) |
| 4D | OM | 4 | 8 | 2 of 4 |
| 4D | OI | 4 | 8 | 2 of 4 |
| 4D | MI | 4 | 8 | 2 of 4 |
| 2D | O | 4 | 8 | 4 of 16 |
| 2D | M | 4 | 8 | 4 of 16 |
| 2D | I | 4 | 8 | 4 of 16 |
| **Total** | | **32** | **64** | |

The tiling has a recursive nesting: every 2D face that a 2-flip group occupies is embedded in a 4D subcube of the corresponding 4-flip group. The OMI group acts as the complement at every level — it fills the opposite diagonal in 2D faces, the remaining vertices in 4D subcubes, and spans the full cube at 6D.

---

## Finding 7: The Three Generators Partition the Fixed-Dimension Space

The three generators O, M, I define three orthogonal 2D subspaces of the hypercube:

| Generator | Flip pair | Fixed by |
|-----------|----------|----------|
| O | L1, L6 | OM, OI (when combined) |
| M | L2, L5 | OM, MI (when combined) |
| I | L3, L4 | OI, MI (when combined) |

Each generator's flip dimensions are the fixed dimensions of the other two 4-flip groups that don't contain it. This is a perfect orthogonal decomposition: {0,1}^6 = O⊗M⊗I, where each factor is a {0,1}^2 corresponding to a mirror-position line pair.

---

## Summary

The King Wen pairing decomposes {0,1}^6 into 32 main diagonals tiling subcubes at three scales:

1. **Every pair is a main diagonal** — maximum distance within its change subspace
2. **Three orthogonal generators** (O, M, I) decompose the cube as {0,1}^2 ⊗ {0,1}^2 ⊗ {0,1}^2
3. **7 groups = all non-empty subsets of {O, M, I}** tile the hypercube with perfect balance
4. **2D faces split into perpendicular diagonals** — one from a single-generator group, one from OMI
5. **OMI is the universal complement** — it fills the opposite diagonal at every scale

The pairing structure is not just a list of 32 related pairs. It is a **complete diagonal tiling of {0,1}^6** built from a tensor product of three 2D mirror-pair factors, with the complement group serving as the dual at every level of the decomposition.
