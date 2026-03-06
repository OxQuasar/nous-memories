# 6. Line-Level Analysis of the King Wen Sequence

> Track each of the 6 line positions as independent binary signals through the sequence.

---

## Representation

The 64×6 binary matrix M: rows are hexagrams in King Wen order, columns are line positions (L1=bottom to L6=top). Each column is a binary signal of length 64 — the yin/yang state of that line position as you walk the sequence.

---

## Finding 1: Perfect Independence Between Lines

All six line signals are **exactly uncorrelated** (Pearson r = 0.000 for every pair). Each line position is a completely independent binary signal. No line predicts any other line's state at the same position in the sequence.

This is a non-trivial property of the King Wen ordering. Any permutation of 64 hexagrams uses each vertex once, but most orderings would introduce spurious correlations between line signals. King Wen maintains exact orthogonality.

---

## Finding 2: Pairing Structure Is 87.5% Inversion

For adjacent pairs (odd→even hexagram), testing whether L_k of hex[n] equals L_(7-k) of hex[n+1]:

- **168/192 bits match (87.5%)**
- Each line shows identical stats: 28/32 mirror matches

The 12.5% non-matches are the 4 palindromic hexagrams (whose bit pattern reads the same reversed) — for these, the King Wen pair is the complement instead. The pairing rule is: **inversion when possible, complement when inversion is identity**.

---

## Finding 3: No Forbidden 5-Bit Transitions

Lines changed per step:

| Lines changed | Count | Hamming distance |
|:---:|:---:|:---:|
| 1 | 2 | 1 |
| 2 | 20 | 2 |
| 3 | 13 | 3 |
| 4 | 19 | 4 |
| 5 | **0** | 5 |
| 6 | 9 | 6 |

The sequence **never changes exactly 5 lines** in a single step. Every other count appears. This is the same even-Hamming preference seen in the hypercube analysis, but now sharper: 5-bit transitions are completely absent, not just rare.

The 9 full-complement transitions (all 6 lines flip) are the palindromic pair transitions. The 2 single-line transitions are the only edge-walks on the hypercube.

---

## Finding 4: Mirror-Position Lines Co-Change

Co-change ratios (actual vs expected under independence):

| Pair | Ratio | Relationship |
|------|-------|-------------|
| L1-L6 | **1.34** | outer mirror |
| L3-L4 | **1.32** | inner mirror |
| L2-L5 | **1.29** | middle mirror |
| L3-L5 | 0.82 | cross-position |
| L1-L5 | 0.92 | cross-position |

The three mirror pairs (L1↔L6, L2↔L5, L3↔L4) consistently co-change more than expected. Cross-position pairs co-change less. This is the inversion structure manifested as temporal correlation: when a hexagram changes to its inversion, the mirror-position lines must flip together.

---

## Finding 5: Run Lengths Are Random

No line has significantly more or fewer switches than a random permutation of 32 yin + 32 yang:

| Line | Switches | Random mean | z-score | p |
|------|----------|------------|---------|---|
| L1 | 37 | 32.0 | +1.26 | 0.92 |
| L2 | 32 | 32.0 | -0.01 | 0.55 |
| L3 | 35 | 31.9 | +0.77 | 0.81 |
| L4 | 34 | 31.9 | +0.52 | 0.74 |
| L5 | 35 | 32.0 | +0.75 | 0.81 |
| L6 | 38 | 32.0 | +1.51 | 0.95 |

The line signals show no unusual persistence or anti-persistence. The structure is in *which* lines change together, not in *how long* they stay in one state.

---

## Finding 6: Lag-1 Negative, Lag-4 Positive

Mean autocorrelation across all six lines:

| Lag | Autocorrelation |
|-----|----------------|
| 1 | **-0.115** |
| 2 | -0.021 |
| 3 | -0.031 |
| 4 | **+0.125** |
| 8 | -0.031 |
| 16 | +0.052 |
| 32 | +0.062 |

**Lag-1 is negative**: consecutive hexagrams tend to have opposite line values (the inversion pairing).

**Lag-4 is positive**: hexagrams 4 apart tend to share line values. This is the pair-of-pairs structure — the first pair and the second pair in a group of four hexagrams tend to have similar line configurations.

---

## Finding 7: Period 2 and Period 4 Dominate

FFT of line signals shows dominant power at periods 2.0 and 4.0 across all lines. Line 5 has the strongest period-2 signal (power=100). Line 6 has a strong period-2.9 signal.

The period-2 peak is the pairing structure: every 2 hexagrams form an inversion pair. The period-4 peak is the pair-of-pairs grouping. These spectral signatures are consistent across all six lines — the pairing imposes a shared rhythmic structure on all line positions simultaneously.

Cross-spectral coherence peaks:
- L1-L6, L5-L6, L1-L5: period 4.0 — the outer/upper lines share a period-4 rhythm
- L3-L4: period 21.3 — the inner lines share a longer-period oscillation
- L3-L5: period 16.0 — another long-period coupling

---

## Finding 8: Most Common Change Patterns

| Pattern | Count | Structure |
|---------|-------|-----------|
| (L1,L2,L3,L4,L5,L6) | 9 | full complement |
| (L3,L4) | 5 | inner pair only |
| (L1,L2,L5,L6) | 4 | outer+middle, skip inner |
| (L1,L3,L4,L6) | 4 | outer+inner, skip middle |
| (L2,L5) | 4 | middle pair only |
| (L1,L6) | 4 | outer pair only |
| (L2,L3,L4,L5) | 4 | middle+inner, skip outer |

The dominant patterns are **mirror-symmetric**: lines change in complementary pairs (L1+L6, L2+L5, L3+L4). The most common non-trivial patterns are one mirror pair changing alone, or two mirror pairs changing while the third stays fixed. The sequence evolves by toggling structurally symmetric line groups.

---

## Finding 9: Line Signals at Key Offsets

**Offset 19** (the coupling offset): inner lines L3 and L4 match at 56.2%, outer lines match at only 43.8%. The coupling at offset 19 is slightly concentrated in the inner line positions.

**Offset 32** (antipodal): lines L5 and L6 match at 62.5%, while L3 and L4 match at only 43.8%. The antipodal relationship, such as it is, lives in the upper lines.

All match rates are modest (43-63%), confirming that offset structure is primarily in transition intensities, not in raw line states.

---

## Summary

The King Wen sequence maintains six perfectly independent binary signals. The structure is not in the individual signals (which are statistically random in their run lengths) but in how they **change together**:

1. **Mirror-position co-change** — lines at positions k and 7-k flip together more than expected
2. **No 5-bit transitions** — the sequence avoids changing exactly 5 of 6 lines
3. **Period-2/period-4 rhythm** — the pairing structure imposes a shared spectral signature
4. **Symmetric change patterns** — lines toggle in structurally complementary groups

The organizing principle is the inversion operation: the sequence evolves by applying approximate bit-reversal at each step, creating coordinated motion across mirror-position lines while keeping each line's marginal distribution perfectly balanced and uncorrelated.
