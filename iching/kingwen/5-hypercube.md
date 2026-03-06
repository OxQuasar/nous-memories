# 5. Hypercube Geometry of the King Wen Sequence

> Each hexagram is a vertex of {0,1}^6. The King Wen sequence is a path through all 64 vertices. What does the structure we found in transition intensities mean in this geometric space?

---

## Representation

Each hexagram maps to a 6-bit binary string — a vertex of the 6-dimensional hypercube. The King Wen sequence defines a walk through all 64 vertices. Two vertices are "close" if they differ in few bits (low Hamming distance). The hypercube has natural symmetries: bit flips (complementation), bit reversal (inversion/flipping the hexagram upside-down), and bit permutations.

---

## Finding 1: Hamiltonian Path with Perfect Balance

The King Wen sequence visits all 64 vertices exactly once — it is a Hamiltonian path through {0,1}^6.

The centroid of the path is exactly [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]. Every line position is yang in exactly 32 of the 64 hexagrams. This is perfect dimensional balance — the sequence uses every bit equally. Quarters of the sequence (1-16, 17-32, 33-48, 49-64) deviate slightly from balance, but the full sequence is exact.

This is a non-trivial constraint. A random permutation of 64 hexagrams is always a Hamiltonian path (it's just a reordering of all vertices), and always has a balanced centroid (since every vertex appears once). The interesting question is not *that* it's balanced, but *how* it traverses the space.

---

## Finding 2: Step Size Distribution — Not Edge-Walking

The path does not walk along hypercube edges (single-bit flips). Step sizes:

| Hamming distance | Steps | Expected (random) |
|-----------------|-------|--------------------|
| 1 | 2 | ~6 |
| 2 | 20 | ~15 |
| 3 | 14 | ~20 |
| 4 | 19 | ~15 |
| 5 | 0 | ~6 |
| 6 | 9 | ~1 |

The sequence over-represents 2-bit and 4-bit jumps and massively over-represents 6-bit jumps (full complements — all bits flip). It under-represents 1-bit, 3-bit, and 5-bit jumps. The 9 complement transitions (Hamming 6) are the paired hexagrams where one is the bitwise negation of the other.

The even-Hamming preference means the path tends to preserve parity — consecutive hexagrams usually have the same number of yang lines (mod 2), or flip to the exact opposite.

---

## Finding 3: Adjacent Steps ≈ Bit Reversal (Inversion)

The strongest geometric pattern in the sequence. For adjacent hexagrams (offset 1), testing whether each target bit can be predicted from a source bit:

| Target bit | Best source | Match | Operation |
|-----------|------------|-------|-----------|
| 1 | bit 6 | 65.6% | copy |
| 2 | bit 5 | 78.1% | copy |
| 3 | bit 4 | 71.9% | copy |
| 4 | bit 3 | 68.8% | copy |
| 5 | bit 2 | 62.5% | copy |
| 6 | bit 1 | 71.9% | copy |

This is the inversion operation — reading the hexagram upside-down (bit k ↔ bit 7-k). Overall accuracy: 69.8%. The King Wen sequence approximately alternates inversions, confirming the known pairing structure: hexagrams 1-2 are inversions, 3-4 are inversions, etc. When inversion produces the same hexagram (palindromic bits), the pair is complements instead.

No other offset comes close to this level of geometric regularity.

---

## Finding 4: Offset 19 Is Not Geometric

The offset-19 coupling (significant in transition intensities at p<0.01 on chi-squared) does not correspond to a geometric relationship in the hypercube.

- Mean Hamming distance for offset-19 pairs: 3.06 (rank 27/63 by closeness)
- No consistent XOR mask — the most common XOR pattern appears in only 4/64 pairs
- Per-bit differences are near-uniform (28-36 out of 64 pairs differ on each bit)
- Best permutation+XOR assignment: 57.8% accuracy (near chance)

The offset-19 structure lives entirely in the transition intensity domain. Positions 19 apart have correlated *changes* (Hamming distances between consecutive hexagrams), but the hexagrams themselves are not geometrically related.

---

## Finding 5: Offset 27 Is Not a Hypercube Automorphism

The ring symmetry at rotation 27 (significant at p=0.009 in phase1b) does not correspond to a hypercube symmetry.

- Best XOR mask: 001111 (4 flips), matching only 5/64 positions
- Monte Carlo: random gets 4.01±0.79 matches, p=0.22
- Best permutation+XOR assignment: 59.4% accuracy

Like offset 19, the rotation-27 symmetry is a property of how transition intensities are arranged around the ring, not a geometric property of the hexagrams as hypercube vertices.

---

## Finding 6: Trigram Trajectories

The upper and lower trigrams trace independent paths through their respective 3-cubes (8 vertices each). Both paths visit all 8 trigrams multiple times with short run lengths (mean ~1.7 steps before switching trigram).

Upper trigram: 60 runs across 64 steps — almost every step changes the upper trigram.
Lower trigram: 59 runs — same pattern.

The path through the full 6-cube decomposes into two nearly-independent paths through 3-cubes, with no long residence in any trigram subcube. The sequence is maximally exploratory at the trigram level.

---

## Finding 7: Forward vs Backward Path

The backward path traverses the same 64 vertices in reverse order. Since the transition intensity h[k] = Hamming(v[k], v[k+1]), the backward sequence is simply h[] reversed.

### Rotation 27: Exact Match Significance

At rotation 27, the forward and backward transition sequences have **36/64 exact matches** — over half the step sizes are identical. Monte Carlo: random permutations average 16.3 exact matches. **p < 0.0001**.

This is the same ring symmetry from phase1b (edit distance 28/64, p=0.009), now measured as exact position-by-position Hamming distance matches. Within ±1 tolerance: 42/64 positions match.

The correlation between forward and rotated-backward transitions at rotation 27 is r=0.186 — modest in linear terms, but the exact-match count shows the relationship is discrete rather than continuous. The sequences don't scale together; they *coincide* at specific positions.

### Correlation Peak Is Elsewhere

The best *correlation* between forward and rotated-backward transitions is at rotation 37 (r=0.344), not 27. Rotation 27 ranks lower on correlation because the relationship isn't linear — it's a discrete matching pattern that correlation underweights.

This explains why phase1b's correlation-based tests (Study 2) missed the ring symmetry that the edit-distance test found. The forward-backward relationship is structural (same/different), not proportional (scales together).

### Trigram Trajectories Have Their Own Symmetry Axes

Upper trigram trajectory: best forward-backward match at rotation 35 (18/64 positions, p=0.044).
Lower trigram trajectory: best match at rotation 30 (18/64, p=0.046).

Both marginally significant, but at different rotations than the transition intensity axis (27). The three levels of structure — transition intensity, upper trigram, lower trigram — each have independent symmetry axes on the ring.

### Curvature Is Identical

Forward and backward paths have identical curvature distributions (mean 3.06 bits of direction change per step). This is trivially true — reversing a path doesn't change how sharply it turns, only the direction. Best curvature correlation at rotation 58.

---

## Summary

| Question | Answer |
|----------|--------|
| Is King Wen a Hamiltonian path? | Yes, with perfect dimensional balance |
| Does it walk edges? | No — prefers 2-bit and 4-bit jumps, with 9 complement transitions (6-bit) |
| Geometric pattern in adjacent steps? | Bit reversal (inversion) at 69.8% — the pairing structure |
| Offset 19 in hypercube? | Not geometric — coupling is in transition intensities only |
| Offset 27 in hypercube? | Not geometric — ring symmetry is in transition intensities only |
| Trigram structure? | Nearly independent upper/lower trajectories, maximally exploratory |
| Forward vs backward? | 36/64 exact step-size matches at rotation 27 (p<0.0001). Discrete, not linear. |
| Trigram symmetry axes? | Upper at rotation 35, lower at rotation 30 — independent of transition axis 27 |

**Three independent structural layers:**

1. **Vertex geometry** — the pairing structure (adjacent inversions, even-Hamming preference)
2. **Transition intensities** — ring properties (offset 19 coupling, rotation 27 symmetry, 36/64 exact matches forward↔backward)
3. **Trigram trajectories** — their own symmetry axes (upper=35, lower=30), marginally significant

These layers are orthogonal. The hypercube geometry is about *what* the hexagrams are. The transition intensities are about *how much they change*. The trigram trajectories are about *which structural component* changes. Each has its own symmetry, at its own rotation.
