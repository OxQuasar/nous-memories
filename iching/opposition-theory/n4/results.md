# n=4 Exhaustive Opposition Analysis — Results

## 1. Setup

16 four-bit states (0000 through 1111) partitioned into 8 unordered pairs. Total distinct pairings: 16!/(2⁸ × 8!) = **2,027,025**. All enumerated exhaustively.

Four opposition measures computed per pairing:
1. **Opposition strength** — Σ Hamming(a,b) across 8 pairs
2. **Opposition diversity** — Shannon entropy of XOR mask distribution (15 possible masks)
4. **Opposition balance** — weight tilt (mean |Δyang|) and reversal symmetry (pairs preserved under bit-reversal)
5. **Weight complementarity** — Pearson r of yang-counts, canonical ordering a < b

Measure 3 (sequential opposition variety) deferred — requires a sequence ordering, not just a pairing. No canonical n=4 sequence exists.

### Z₂² orbit structure

Group {id, complement, reversal, comp∘rev} acting on {0,...,15}:

| Orbit | Size | States | Weights |
|-------|------|--------|---------|
| 1 | 2 | 0000, 1111 | 0, 4 |
| 2 | 4 | 0001, 0111, 1000, 1110 | 1, 3, 1, 3 |
| 3 | 4 | 0010, 0100, 1011, 1101 | 1, 1, 3, 3 |
| 4 | 2 | 0011, 1100 | 2, 2 |
| 5 | 2 | 0101, 1010 | 2, 2 |
| 6 | 2 | 0110, 1001 | 2, 2 |

**6 orbits total**: 4 of size 2, 2 of size 4. No fixed point under the full group.

**4 palindromes** (reversal-fixed): {0000, 0110, 1001, 1111}, forming 2 complement pairs.
**4 comp∘rev-fixed**: {0011, 0101, 1010, 1100}, the "anti-palindromes."

Both reversal and comp∘rev have fixed points → **neither yields a valid complete pairing**. Only complement (no fixed points at even n) produces a valid pairing from a single operation.

---

## 2. Measure Ranges and Discrimination

| Measure | Range | Unique Values | Mean ± Std | Discriminates? |
|---------|-------|---------------|------------|----------------|
| Strength | [8, 32] | 13 (all even) | 17.07 ± 2.60 | Yes |
| Diversity | [0, 3.0] | 12 | 2.52 ± 0.29 | Yes |
| Weight Tilt | [0.5, 1.5] | 5 | 1.17 ± 0.24 | **Weak** — only 5 levels |
| Reversal Sym | [0, 8] | 8 | 1.11 ± 1.17 | Moderate (skewed: 37% at 0) |
| Weight Corr | [−1, +1] | 126 | +0.27 ± 0.36 | Yes |

**Weight tilt is near-degenerate** at n=4. Five values {0.5, 0.75, 1.0, 1.25, 1.5} with limited spread. This measure may not be fundamental — it provides almost no discrimination between pairings.

The strength distribution is near-Gaussian centered at ~17, with extreme tails: only 1 pairing achieves S=32, only 272 achieve S=8.

---

## 3. The Orthogonality Result

**Pearson r(strength, diversity) = 0.000000000000000** — exactly zero to machine precision.

Strength and diversity are perfectly uncorrelated over the space of all 2,027,025 pairings. This is not a near-miss or a sampling artifact. It is structural.

The same holds at n=3: over all 105 pairings of 8 trigram-states into 4 pairs, r(S, D) = 0 exactly.

### But E[D|S] varies

| S | n | mean D | max D |
|---|---|--------|-------|
| 32 | 1 | 0.00 | 0.00 |
| 30 | 16 | 0.81 | 0.81 |
| 28 | 216 | 1.39 | 1.55 |
| 26 | 2,800 | 1.88 | 2.16 |
| 24 | 21,624 | 2.19 | 2.75 |
| 22 | 105,696 | 2.40 | **3.00** |
| 20 | 316,992 | 2.51 | 3.00 |
| 18 | 566,592 | 2.56 | 3.00 |
| 16 | 585,360 | 2.56 | 3.00 |
| 14 | 327,296 | 2.49 | 3.00 |
| 12 | 90,368 | 2.35 | 2.75 |
| 10 | 9,792 | 2.08 | 2.50 |
| 8 | 272 | 1.36 | 2.00 |

E[D|S] traces an inverted U: lowest at both extremes of S, peaking around S=18. The zero linear correlation means this nonlinear dependence is symmetric — it cancels out in the Pearson inner product. They are uncorrelated but not independent.

### The working hypothesis was wrong as stated

The opposition theory draft predicted a "trade-off" between strength and diversity. The data show **no global trade-off** — they are orthogonal degrees of freedom. The constraint is purely a **boundary phenomenon**: at the extremes of strength (S ≥ 24 or S ≤ 10), the maximum achievable diversity is capped. In the interior (10 < S < 24), full diversity D = 3.0 is freely achievable.

---

## 4. The Boundary (Feasible Region)

The feasible region in S × D space is lens-shaped:

| Strength | Max Diversity | Min Diversity |
|----------|--------------|---------------|
| 32 | 0.00 | 0.00 |
| 30 | 0.81 | 0.81 |
| 28 | 1.55 | 0.81 |
| 26 | 2.16 | 0.81 |
| 24 | 2.75 | 0.00 |
| 22 | 3.00 | 0.81 |
| 20 | 3.00 | 0.81 |
| 18 | 3.00 | 0.81 |
| 16 | 3.00 | 0.00 |
| 14 | 3.00 | 0.81 |
| 12 | 2.75 | 0.81 |
| 10 | 2.50 | 0.81 |
| 8 | 2.00 | 0.00 |

Both extremes of strength constrain diversity. The theoretical maximum diversity D = log₂(8) = 3.0 (all 8 masks distinct) is achieved by **167,040 pairings** (8.24%) across strength levels 14–22.

The **2D Pareto frontier** (maximize both S and D) has exactly 6 profile points:

| S | D | Count |
|---|---|-------|
| 32 | 0.000 | 1 |
| 30 | 0.811 | 16 |
| 28 | 1.549 | 96 |
| 26 | 2.156 | 768 |
| 24 | 2.750 | 672 |
| 22 | 3.000 | 1,536 |

This staircase IS the upper-right boundary of the lens. It starts at the complement pairing (S=32, D=0) and ends at the maximum-diversity region (S=22, D=3.0). Each step loses 2 strength to gain ~0.4–0.8 diversity.

---

## 5. Named Pairings

### Complement pairing

Pair each state with its bitwise complement. All 8 pairs at Hamming distance 4, single mask 1111.

| Measure | Value | Rank |
|---------|-------|------|
| Strength | **32** | **Maximum** (unique — only pairing at S=32) |
| Diversity | 0.000 | Minimum (1 mask type) |
| Weight Tilt | 1.500 | Maximum |
| Reversal Sym | 8/8 | Maximum |
| Weight Corr | **−1.000** | Extreme negative |
| 2D Pareto | ✓ | |
| 3D Pareto | ✓ | |
| 5D Pareto | ✓ | |

Equivariant under all of Z₂². Sits on every Pareto frontier tested.

### KW-style (reversal for non-palindromes, complement for palindromes)

The n=4 analog of the King Wen hexagram pairing rule.

| Pair | XOR | Dist | Type |
|------|-----|------|------|
| 0000 ↔ 1111 | 1111 | 4 | complement (palindrome) |
| 0110 ↔ 1001 | 1111 | 4 | complement (palindrome) |
| 0011 ↔ 1100 | 1111 | 4 | complement (comp∘rev-fixed) |
| 0101 ↔ 1010 | 1111 | 4 | complement (comp∘rev-fixed) |
| 0001 ↔ 1000 | 1001 | 2 | reversal |
| 0010 ↔ 0100 | 0110 | 2 | reversal |
| 0111 ↔ 1110 | 1001 | 2 | reversal |
| 1011 ↔ 1101 | 0110 | 2 | reversal |

| Measure | Value | Rank |
|---------|-------|------|
| Strength | 24 | 75th percentile |
| Diversity | 1.500 | 3 mask types (1111, 1001, 0110) |
| Weight Tilt | **0.500** | **Minimum** (reversal preserves weight) |
| Reversal Sym | 8/8 | Maximum |
| Weight Corr | +0.067 | Near zero |
| 2D Pareto | ✗ | Dominated by 23,632 pairings |
| 3D Pareto | ✗ | |
| 5D Pareto | ✗ | |

Also equivariant under all of Z₂². **Not on any Pareto frontier.** At S=24, maximum achievable diversity is 2.75 — KW-style reaches only 1.50.

The problem: at n=4, reversal pairs have Hamming distance exactly 2 (the inner and outer bits swap but the middle two are preserved by the palindrome structure of reversal). This is structurally weak — it costs 8 strength per reversal pair compared to complement, and contributes only 2 distinct mask types (1001, 0110). The n=4 reversal pairs are too uniform to generate diversity.

### Invalid operations

- **Reversal**: 4 palindromes are fixed → not a valid complete pairing
- **Comp∘rev**: 4 anti-palindromes are fixed → not a valid complete pairing

### Equivariance counts

Of 2,027,025 pairings:
- 5,937 equivariant under complement (0.29%)
- 993 equivariant under reversal (0.05%)
- 993 equivariant under comp∘rev (0.05%)
- **117 equivariant under all three** (0.006%)

Both named pairings are in the 117.

---

## 6. Inter-Measure Correlations

| Pair | Pearson r |
|------|-----------|
| **Strength ↔ Diversity** | **0.000** |
| Strength ↔ Weight Tilt | +0.313 |
| **Strength ↔ Weight Corr** | **−0.611** |
| **Diversity ↔ Weight Tilt** | **0.000** |
| Diversity ↔ Reversal Sym | −0.025 |
| Diversity ↔ Weight Corr | +0.004 |
| Weight Tilt ↔ Reversal Sym | −0.135 |
| Weight Tilt ↔ Weight Corr | −0.607 |
| Reversal Sym ↔ Weight Corr | −0.036 |

Two exact zeros: S↔D and D↔WT. Diversity is nearly orthogonal to everything — it correlates meaningfully with nothing. Strength and weight correlation are strongly coupled (r = −0.61): high-strength pairings necessarily anti-correlate weights (complement-like), low-strength pairings pair similar weights.

---

## 7. Implications for Opposition Theory

### The concentration-distribution framing needs refinement

The theory predicted that strength and diversity would *trade off*. They don't — they're orthogonal. The correct statement: **strength and diversity are independent degrees of freedom, subject to boundary constraints at extremes.** The "trade-off" is a boundary phenomenon, not a global anti-correlation.

This holds at both n=3 (confirmed: r = 0 exactly over 105 pairings) and n=4 (r = 0 over 2,027,025 pairings). The orthogonality appears structural and scale-invariant.

### Complement pairing is Pareto-optimal but cornered

Complement uniquely maximizes strength (S = 32 = 4 × 8, every pair at max distance). It's on every Pareto frontier. But it sits in a corner: zero diversity, maximum weight tilt, perfect weight anti-correlation. It is the extreme of concentration — one opposition type, repeated uniformly.

### The KW-style pairing is equivariant but suboptimal

KW-style is fully Z₂²-equivariant (a strong symmetry property — only 117 pairings share it). But it's not on any Pareto frontier. The n=4 reversal pairs are too structurally uniform: all have distance 2, using only 2 mask types. The mixing of complement and reversal at n=4 produces 3 mask types — far from the 8-type maximum.

### Why n=4 may not predict n=6

At n=4, reversal pairs have fixed Hamming distance 2 (the two mirror positions swap, the other two stay). At n=6, reversal pairs span distances {2, 4, 6} depending on orbit signature. This means n=6 reversal pairs carry **variable** opposition strength and contribute **diverse** masks — exactly what n=4 reversal pairs fail to do.

The KW principle (reversal where possible, complement for palindromes) may only become Pareto-competitive at scales where reversal produces diverse opposition. At n=4, it doesn't. At n=6, it does — and this is precisely where the King Wen sequence lives.

### Open question: why is S↔D exactly zero?

The exact orthogonality of strength and diversity across all pairings, at both n=3 and n=4, demands explanation. This is not a symmetry argument alone (the distribution of S is not symmetric). It may reflect a deeper combinatorial identity in the structure of XOR masks over perfect matchings.

---

## Files

| File | Description |
|------|-------------|
| `enumerate.py` | Enumeration + measures → `measures.npz`, `meta.json` |
| `structure.py` | Z₂² orbits, fixed points, equivariance → `structure.md` |
| `pareto.py` | Pareto frontiers + scatter plots → PNGs |
| `measures.npz` | 2,027,025 × 5 compressed measure arrays |
| `meta.json` | Named pairing indices, pairs, invalid pairing notes |
| `structure.md` | Full structural analysis output |
| `strength_vs_diversity.png` | S×D scatter with Pareto frontier and named pairings |
| `strength_vs_weight_corr.png` | S×WC scatter |
| `density_strength_diversity.png` | Hexbin density in S×D space |
| `diversity_vs_weight_corr.png` | D×WC scatter |
| `strength_vs_rev_sym.png` | S×RS scatter |
