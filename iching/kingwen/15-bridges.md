# 15. Bridge Analysis of the King Wen Sequence

> Pairing hexagrams offset by one (2-3, 4-5, 6-7, ...) instead of the standard pairs (1-2, 3-4, 5-6, ...). These bridge transitions carry the "real" structural change — the movement between orbits.

---

## Finding 1: Bridges Break the Generator Algebra

29 of 31 bridge masks cannot be expressed as any combination of O, M, I. The mirror-pair generator structure that governs standard pairs is completely absent at bridges.

| Property | Standard Pairs | Bridges |
|----------|:-:|:-:|
| Generator-expressible masks | 32/32 (100%) | 2/31 (6%) |
| Unique masks | 7/32 | 23/31 |
| Hamming distances | 2, 4, 6 (even only) | 1, 2, 3, 4, 6 (odd allowed) |
| Mean Hamming | 3.75 | 2.94 |
| Mirror-pair structure | Always | Never (except B14, B19) |

The two bridges that DO use standard generators are B14 (I, the canon boundary) and B19 (OMI) — and these are the only two self-transitions (same orbit). When a bridge stays within an orbit, it uses the generator algebra. When it crosses orbits, it breaks it.

---

## Finding 2: Bridges Are Closer in Hamming Distance

Bridge transitions average 2.94 bits of change vs 3.75 for standard pairs. The distribution peaks at Hamming 3 (13/31) and includes single-bit changes (2/31) — impossible for standard pairs.

The sequence makes *smaller* moves between pairs than within them. Intra-pair change is large and structured (generator-governed). Inter-pair change is small and unconstrained (free movement). The narrative steps are gentler than the algebraic ones.

---

## Finding 3: Orbit Transition Matrix Is Sparse and Asymmetric

The 8 orbits connect via bridges in a directed graph:

```
         →1    →5    →4    →8    →7    →3    →2    →6
  1:Qian  [1]    .     1     .     .     .     1     1
  5:XChu   .     .     .     .     1     .     1    [2]
  4:Shi    .     2     .     .     1     .     1     .
  8:WWang  1     1     1    [1]    .     .     .     .
  7:Bo     1     .     .     2     .     1     .     .
  3:Xu     .     .     1     1     1     .     .     1
  2:Zhun   .     1     .     .     .     3     .     .
  6:Tai    .     .     1     .     1     .     1     .
```

Of 56 possible directed edges (excluding self-loops), only 20 are used (36%). The graph is sparse — most orbit-to-orbit transitions never occur.

---

## Finding 4: Transitions Are Almost Entirely One-Way

Of 22 connected orbit pairs, only 2 are symmetric:
- **Orbit 5 (XChu) ↔ Orbit 2 (Zhun)**: 1 each direction
- **Orbit 7 (Bo) ↔ Orbit 3 (Xu)**: 1 each direction

The remaining 18 connections are unidirectional. The sequence has a preferred flow direction through orbit space.

Strongest one-way channels:
- **Orbit 2 → Orbit 3** (Zhun→Xu): 3 bridges, 0 reverse. The OM→OI transition is a dominant current.
- **Orbit 5 → Orbit 6** (XChu→Tai): 2 bridges, 0 reverse.
- **Orbit 4 → Orbit 5** (Shi→XChu): 2 bridges, 0 reverse.
- **Orbit 7 → Orbit 8** (Bo→WWang): 2 bridges, 0 reverse.

---

## Finding 5: Self-Transitions Mark Structural Boundaries

Only 2 self-transitions exist:
- **B14**: Orbit 1 (0,0,0) → Orbit 1. The canon boundary (Da Guo→Kan, hexagrams 28→29). Mask = I (the only bridge using a single generator).
- **B19**: Orbit 8 (0,1,1) → Orbit 8. Mid-lower-canon (Kui→Jian, hexagrams 38→39). Mask = OMI (complement).

Both use generator masks. Both are structural "resting points" — moments where the sequence pauses in the same orbit across a bridge. Everywhere else, the bridge crosses into a new structural world.

---

## Finding 6: Orbit Degree Is Nearly Uniform

| Orbit | Out | In | Self | Total |
|:---:|:---:|:---:|:---:|:---:|
| 1 (Qian) | 4 | 3 | 1 | 7 |
| 2 (Zhun) | 4 | 4 | 0 | 8 |
| 3 (Xu) | 4 | 4 | 0 | 8 |
| 4 (Shi) | 4 | 4 | 0 | 8 |
| 5 (XChu) | 4 | 4 | 0 | 8 |
| 6 (Tai) | 3 | 4 | 0 | 7 |
| 7 (Bo) | 4 | 4 | 0 | 8 |
| 8 (WWang) | 4 | 4 | 1 | 8 |

Every orbit participates equally (3-4 connections in each direction). The asymmetry is in direction, not in degree. No orbit is a dead end or a sink — the graph is well-connected despite its sparsity.

---

## Finding 7: Two Separate Algebras at Two Scales

The bridge analysis confirms the two-level architecture:

**Within orbits (standard pairs):** Change operates through 3 mirror-pair generators. All masks are generator-expressible. Hamming distances are even. The algebra is Z₂³.

**Between orbits (bridges):** Change operates outside the generator algebra. 29/31 masks are not generator-expressible. Hamming distances include odd values. The bit-level change is unconstrained.

**At the orbit level:** Both standard pairs and bridges produce the same signature transition distribution: mi (7×), omi (6×), om (5×), i (4×), m (3×), oi (2×), o (2×), id (2×). The orbit-level dynamics are invariant to which pairing you use.

The generator algebra governs intra-orbit structure. The orbit transition graph governs inter-orbit flow. These are two separate systems operating at different scales, connected only through the signature.

---

## Summary

1. **Bridges break the generator algebra** — 29/31 masks are non-standard, using odd Hamming distances and asymmetric bit patterns
2. **Bridges are gentler** — mean Hamming 2.94 vs 3.75 for standard pairs; narrative steps are smaller than algebraic ones
3. **The transition graph is sparse** — only 36% of possible directed edges are used
4. **Flow is directional** — 18 of 20 connections are one-way; the sequence has a preferred current through orbit space
5. **Self-transitions mark boundaries** — only at the canon break and mid-lower-canon, using generator masks
6. **Degree is uniform** — every orbit is equally connected; asymmetry is in direction, not participation
7. **Two algebras, two scales** — generators govern within-orbit structure; a separate directed graph governs between-orbit flow; both produce the same orbit-level transition distribution
