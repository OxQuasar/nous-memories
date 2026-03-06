# 3. Phase 1b/2b: Non-Linear Structure Detection in Backward Reading

> Replacing correlation-based tests with information-theoretic and structural tests.

---

## Motivation

Phase 1 and 2 used Pearson correlation and linear regression to test antipodal coupling and bidirectional prediction. These assume linear relationships. The King Wen sequence may have nonlinear, ordinal, or structural coupling that correlation misses entirely.

This phase re-tests the same questions with tools that make no linearity assumption.

---

## Tests

### Test 1: Non-Parametric Mutual Information

Mutual information measures how much knowing one variable reduces uncertainty about another, with no assumptions about the form of the relationship — linear, quadratic, threshold, anything.

64 positions on a ring. At each position `k`, a transition intensity `h[k]`. Pick an offset `d`. You have 64 pairs: `(h[k], h[(k+d) mod 64])`. Bin the h-values into categories (low/mid/high), build the joint frequency table, compute:

```
MI = sum over cells:  P(i,j) × log2( P(i,j) / (P(i) × P(j)) )
```

If the two variables are independent, `P(i,j) = P(i) × P(j)`, MI = 0. If one determines the other, MI equals the entropy. MI catches any nonlinear coupling that correlation would miss — if `h[k] = 2` always pairs with `h[(k+d)] = 6` regardless of the functional form, MI detects it.

- Sweep all offsets d=1..63, not just antipodal
- Compare against MI from 10,000 random permutations
- Whichever offset produces the highest MI has the most structured pairing on the ring

### Test 2: Contingency Table (Chi-Squared)

Same question as MI but framed as a hypothesis test with a known null distribution. Bin h-values into {low (1-2), mid (3-4), high (5-6)}. Build a 3×3 contingency table of `(h[k], h[(k+d) mod 64])`. Compute expected counts under independence:

```
expected[i,j] = (row_i_total × col_j_total) / grand_total
chi² = sum over cells: (observed - expected)² / expected
```

For a 3×3 table, df=4. chi² > 13.28 rejects independence at p<0.01. MI gives magnitude (bits of shared information); chi-squared gives a direct significance threshold. Together they answer: is the coupling real, and how strong is it?

- Sweep all offsets — which has the most structured joint distribution?

### Test 3: Compressibility (Lempel-Ziv)

Lempel-Ziv complexity counts distinct phrases in a greedy parse — each new phrase is the shortest substring not previously seen. Example: `1,2,1,2,3` parses as `[1][2][1,2][3]` — 4 phrases.

Concatenate h[] with its reverse and compute LZ complexity of the 128-length sequence. The ratio (concat / forward) tells you:

- **≈ 1.0**: reverse is completely redundant — every phrase was already in the forward pass. The backward reading contains no new information.
- **≈ 2.0**: reverse is completely independent — just as many new phrases. No structural relationship between directions.
- **Between**: partial redundancy — some structural overlap.

This doesn't test any specific coupling like "position k relates to position -k." It asks the broader question: does the sequence as a whole contain patterns shared between forward and backward readings? Any internal symmetry — at any offset — makes the reverse partially compressible given the forward, dropping the ratio below 2.

- Compare against random permutations for significance

### Test 4: Permutation Entropy and Shared Ordinal Patterns

Permutation entropy ignores actual values and looks only at rank order — the shape of local patterns.

Slide a window of length `n` (order) across the sequence. At each position, record the rank ordering of values in the window. For order 3, window `(4, 2, 6)` has rank pattern `(1, 0, 2)` — second is smallest, first is middle, third is largest. Order 3 has 3! = 6 possible patterns. Order 4 has 4! = 24.

```
PE = -sum over patterns: P(pattern) × log2(P(pattern))
```

Maximum PE = log2(n!) — all patterns equally likely, no ordinal structure. Lower PE = ordinal regularity. This captures patterns in the *dynamics* (up-up-down vs up-down-up) that pairwise MI and chi-squared cannot see.

- Compute ordinal patterns for forward and backward reading separately
- **Shared patterns**: same local shapes exist regardless of direction
- **Unique patterns**: appear in only one direction — asymmetric dynamics
- **Forbidden patterns**: never appear in either direction — hard structural constraints of the sequence
- Combined PE vs single-direction PE: does the backward reading add ordinal information?

### Test 5: Ring Symmetry

A ring-symmetric sequence reads approximately the same forward and backward, once you find the right rotation.

Reverse h[] to get h_rev[]. Rotate h_rev by every offset `r = 0..63`. Measure edit distance (positions where `h[k] ≠ h_rev[(k+r) mod 64]`) at each rotation. The rotation that minimizes edit distance is the axis of symmetry.

Without rotation, h[] vs h_rev[] has distance 56/64 — looks maximally asymmetric. But a hidden rotational mirror symmetry would only appear at the right rotation. Think physically: fold the ring along an axis. Positions on opposite sides of the fold should mirror each other's transition values.

- Find the best rotation and its edit distance
- Compare against 10,000 random permutations — is King Wen closer to ring-symmetric than chance?

### Test 6: Transfer Entropy

Transfer entropy measures whether a source sequence reduces uncertainty about the next step of a target sequence, beyond what the target's own history provides.

```
TE(source → target) = H(target_future | target_past) - H(target_future | target_past, source_past)
```

If TE > 0, the source carries predictive information about the target's future that the target's own past doesn't contain. This is the proper information-theoretic test for "does the backward reading carry independent predictive information?"

- TE from the offset-d reading to the forward reading, for each offset d=1..63
- Compare TE at antipodal vs all other offsets
- Compare against random permutations for significance

### Test 7: KNN Nonlinear Prediction

K-nearest-neighbor makes no assumptions about functional form. To predict h[k], find the 5 positions whose features are most similar (Euclidean distance), average their targets.

- **Forward-only features:** `(h[k-1], h[k-2])` — 2D feature space
- **Forward + antipodal:** `(h[k-1], h[k-2], h[-k], h[1-k])` — 4D feature space

Leave-one-out cross-validation: hold out each position, train on 63, predict the held-out one. If the antipodal reading contains useful information, adding it should reduce error. If it's noise, the extra dimensions hurt — KNN suffers from the curse of dimensionality, where irrelevant features inflate distances and make "nearest" neighbors less meaningful.

- Compare forward-only vs forward+antipodal MSE
- Sweep offset d=1..63 — is there any distance where a second reading genuinely helps nonlinear prediction?

---

## Execution

Single Python script (`phase1b.py`). Each test produces a statistic, a null distribution from Monte Carlo (10,000 permutations), and a p-value. All offsets d=1..63 are swept where applicable.

---

## Results

### Test 1: Non-Parametric MI — ANTIPODAL NOT SPECIAL

Antipodal MI = 0.072 bits, ranking 9th out of 63 offsets. p=0.42 against random. The strongest MI is at offsets d=19 and d=45 (0.191 bits) — which are each other's complements (19 + 45 = 64). Antipodal coupling has no privileged role even under nonlinear measurement.

### Test 2: Chi-Squared — OFFSET 19/45 IS THE REAL COUPLING

Offsets d=19 and d=45 are the only pair reaching significance (chi²=13.85, p<0.01). Antipodal (d=32) ranks 9th with chi²=6.33 (not significant). The King Wen sequence has a real coupling — but it's at offset 19, not 32. This means positions separated by 19 hexagrams share a structured joint distribution of transition intensities.

### Test 3: Compressibility — NEAR-SIGNIFICANT REDUNDANCY (p=0.078)

LZ ratio = 1.545 (concatenating the reverse adds only 54.5% complexity, not 100%). Random permutations average 1.637. King Wen is more compressible than 92.2% of random permutations when concatenated with its reverse. Near-significant at p=0.078.

The reverse reading is partially redundant with the forward reading — the sequence has structural symmetry that makes reading backward capture overlapping information. This doesn't mean the backward reading is useless, but it's not independent.

### Test 4: Ordinal Patterns — SHARED STRUCTURE, ONE FORBIDDEN

Order 3: all 6 possible patterns appear in both directions. No forbidden patterns. Permutation entropy is high (~0.95 normalized) — the sequence is close to maximally complex at this order.

Order 4: 21 of 24 patterns appear in each direction. 19 are shared, 2 are unique to each direction, and 1 pattern is forbidden in both. The shared forbidden pattern is a structural constraint of the King Wen sequence visible from either direction.

Combined permutation entropy (0.923) is higher than either direction alone (0.900, 0.908), confirming the backward reading adds some ordinal information.

### Test 5: Ring Symmetry — SIGNIFICANT (p=0.009)

The most striking result. Best ring symmetry at rotation 27: only 28/64 positions differ between h[] and its rotated reverse (random: 35.9 ± 2.4). p=0.009 — **statistically significant at p < 0.01**.

The King Wen sequence has genuine ring symmetry, but the axis of symmetry is at rotation 27, not at the diametric position (32). If you rotate the reversed sequence by 27 positions, nearly half the transition values align. The timewave was right that ring structure exists — but wrong about where the axis is.

### Test 6: Transfer Entropy — ADJACENT DOMINATES, ANTIPODAL NULL

d=1 (adjacent) has TE=1.34 bits, massively dominant. Antipodal TE=0.14 bits, rank 27/63, p=0.49. The strongest predictive transfer comes from the immediately preceding position, not from any distant coupling.

Interesting secondary offsets: d=20 (0.33 bits) and d=27 (0.26 bits). Offset 27 echoes the ring symmetry axis from Test 5.

### Test 7: KNN Prediction — ANTIPODAL DOESN'T HELP

Forward+antipodal features produce *worse* MSE than forward-only (2.136 vs 2.102). Adding the antipodal reading hurts KNN prediction — it adds noise.

But: offset d=63 (the *adjacent reverse* — essentially h[k+1]) gives MSE=0.335, a massive improvement. This is trivially expected (nearby values are informative). Non-trivial standouts: d=38 and d=47 both beat baseline.

---

## Summary

| Test | Antipodal (d=32) | Best offset | Real finding |
|------|-----------------|-------------|--------------|
| MI | rank 9, p=0.42 | d=19/45 (0.19 bits) | Coupling exists at offset 19, not 32 |
| Chi-squared | rank 9, not sig. | d=19/45 (p<0.01) | Only significant coupling is at offset 19 |
| Compressibility | — | — | Reverse is partially redundant (ratio 1.55, p=0.08) |
| Ordinal patterns | — | — | 1 shared forbidden pattern at order 4 |
| Ring symmetry | — | rotation 27 (p=0.009) | Genuine ring symmetry at rotation 27, not 32 |
| Transfer entropy | rank 27, p=0.49 | d=1 (1.34 bits) | Adjacent dominates; d=27 is secondary |
| KNN prediction | rank 10, hurts | d=63 (trivial) | Antipodal adds noise to prediction |

**Key findings:**

1. **Ring symmetry is real** (p=0.009) but the axis is at rotation 27, not the diametric position 32. The timewave picked the wrong axis.

2. **Offset 19/45 is the real coupling**, significant on chi-squared. This is 19 hexagrams apart — roughly 30% of the ring, not 50%. The coupling might relate to the Upper Canon / Lower Canon split (hexagrams 1-30 vs 31-64).

3. **The reverse reading is partially redundant** (LZ compression ratio 1.55), confirming structural symmetry but suggesting the backward reading doesn't add as much independent information as the timewave assumes.

4. **Adjacent positions dominate prediction** (TE d=1 = 1.34 bits). The sequence is fundamentally sequential, with a secondary ring structure. The timewave inverted the hierarchy — it weighted the ring structure as primary and the sequential structure as secondary.
