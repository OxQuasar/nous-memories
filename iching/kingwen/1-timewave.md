# 1. Timewave Zero — Construction and Reproduction

> Reverse-engineering the McKenna/Kelley/Watkins timewave from the King Wen sequence.

---

## Background

Terence and Dennis McKenna (1975, *The Invisible Landscape*) extracted a waveform from the King Wen sequence of the I Ching and claimed it was fractal, self-similar, and mapped the ebb and flow of "novelty" in time. The grand claims are dismissed. The mathematical construction underneath is real and reproducible.

The construction has three stages: extract transition data from the King Wen sequence, build a 384-point wave via three-scale resonance, then make it fractal via self-similar expansion.

---

## Stage 1: First-Order Differences

The King Wen sequence orders 64 hexagrams (each a 6-bit binary string). The first-order difference `h[k]` is the Hamming distance between hexagram `k` and hexagram `k+1` — how many lines change.

```
h[] = [6, 2, 4, 4, 4, 3, 2, 4, 2, 4, 6, 2, 2, 4, 2, 2,
       6, 3, 4, 3, 2, 2, 2, 3, 4, 2, 6, 2, 6, 3, 2, 3,
       4, 4, 4, 2, 4, 6, 4, 3, 2, 4, 2, 3, 4, 3, 2, 3,
       4, 4, 4, 1, 6, 2, 2, 3, 4, 3, 2, 1, 6, 3, 6, 3]
```

64 values, range [1, 6]. Wraps circularly: h[64] = h[0] = 3 (hexagram 64 back to hexagram 1).

---

## Stage 2: 384-Point Number Set

### Why 384?

64 hexagrams × 6 lines = 384 line-positions. The expansion reads the same 64-element `h[]` signal through three lenses at different zoom levels simultaneously:

| Scale | Name | Reads h[] as | Cycle length | Cycles across 384 | Weight |
|-------|------|-------------|--------------|-------------------|--------|
| Yao (line) | finest | `h[k]` | 64 | 6 | ×1 |
| Trigram | medium | `h[k/3]` | 192 | 2 | ×3 |
| Hexagram | coarsest | `h[k/6]` | 384 | 1 | ×6 |

Division is C-style integer truncation (toward zero), so `h[k/3]` is sample-and-hold — `k=0,1,2` all read `h[0]`, `k=3,4,5` all read `h[1]`, etc. Each scale is a piecewise-constant version of `h[]`, stretched by 3× or 6×. Weights compensate for the slower sampling.

### The formula

Each point `w[k]` for `k = 0..383`:

```
w[k] = |angular(k)| + |linear(k)|
```

### Linear term — level (0th order): how large are the transitions here?

```
linear(k) = (9 - h[-k] - h[k-1])
          + 3 * (9 - h[-k/3] - h[k/3-1])
          + 6 * (9 - h[-k/6] - h[k/6-1])
```

Reads the raw transition intensity at the current position and its **antipodal point** on the 64-element ring (`k + (-k) = 64 mod 64`). No differencing — just the values, subtracted from 9. Bigger transitions at this position → smaller linear term.

The constant 9 is unmotivated. Max possible `h[-k] + h[k-1]` is 12 (both at 6), min is 0. The value 9 biases the term positive for average transition intensities (~3.3 each, giving `9 - 3.3 - 3.3 ≈ 2.4`).

### Angular term — slope (1st order): how are the transitions changing here?

```
angular(k) = sign1 * (h[k-1] - h[k-2] + h[-k] - h[1-k])              # yao
           + 3 * sign3 * (h[k/3-1] - h[k/3-2] + h[-k/3] - h[1-k/3])  # trigram
           + 6 * sign6 * (h[k/6-1] - h[k/6-2] + h[-k/6] - h[1-k/6])  # hexagram
```

First derivative of the transition intensity. `h[k-1] - h[k-2]` is the forward slope (how transitions changed approaching this point). `h[-k] - h[1-k]` is the slope at the antipodal point. The angular term measures whether transitions are *increasing or decreasing* at this position and its opposite on the ring.

All `h[]` indices are mod 64 (circular).

### Antipodal pairing

Both terms pair each position with its diametrically opposite point on the 64-element ring:

```
position k  ←→  position -k mod 64    (k + (-k) ≡ 0 mod 64)
```

For example, position 10 pairs with position 54. The wave at each point reflects the combined state of that position and its mirror.

### The half-twist (sign modulation)

```
sign1 = (-1)^|floor((k-1)/32)|     flips every 32 steps (half of yao cycle)
sign3 = (-1)^|floor((k-3)/96)|     flips every 96 steps (half of trigram cycle)
sign6 = (-1)^|floor((k-6)/192)|    flips every 192 steps (half of hexagram cycle)
```

Each sign flips at the midpoint of its scale's cycle. Effect: the angular contribution is folded in half — first half adds normally, second half subtracts. It's as if each circular reading of `h[]` is cut at the halfway point and folded onto itself with opposite sign.

This is the most controversial step — McKenna never justified it beyond vague references to "preserving geometric properties." Removing it produces the Watkins variant. Watkins' objection: the fold point being at exactly the midpoint is unmotivated, and the k-dependent sign modulation doesn't preserve local geometric information during the collapse.

### Putting it together

`w[k] = |angular(k)| + |linear(k)|`

The absolute values collapse sign — you get a magnitude of:
- **How much is happening here** (linear: transition level at position + antipode)
- **How much is shifting here** (angular: transition slope at position + antipode)

Summed across three scales, each reading the same `h[]` data at different zoom levels.

### Number set variants

| Name | Half-twist | Origin |
|------|-----------|--------|
| Kelley (TW1) | yes | Original 1974 FORTRAN by Royce Kelley & Leon Taylor |
| Watkins (TW2) | no | Peter Meyer's 1994 correction — algorithm as described without the twist |
| Sheliak (TW3) | variant | John Sheliak's vector algebra formalization |
| Huang Ti (TW4) | no | Alternative sequence ordering |

All produce 384 values in the range [0, ~84].

---

## Stage 3: Fractal Self-Similar Expansion

The 384-point wave is made fractal by summing self-similar copies at every power of 64:

```
f(x) = (1/64^3) * [ coarse(x) + fine(x) ]
```

**Coarse scales** (zooming out):
```
coarse(x) = sum over i where x >= 64^i:  64^i * v(x / 64^i)
```

**Fine scales** (zooming in):
```
fine(x) = sum over i from 1:  v(x * 64^i) / 64^i
```

Where `v(y)` linearly interpolates into the 384-point array, wrapping modularly.

The effect: the same 384-point wave pattern appears at every temporal scale. A pattern visible over 384 days repeats (scaled) over 384 * 64 days, 384 * 64^2 days, etc. The wave is self-similar by construction.

---

## Reproduction Results

Our Python reproduction (`timewave.py`) validates against the known number sets:

| Set | Match |
|-----|-------|
| Watkins (no half-twist) | **384/384 exact** |
| Kelley (with half-twist) | **383/384** (1 discrepancy at index 119, likely original FORTRAN rounding) |

### Kelley number set statistics

```
Length: 384
Range:  [0, 79]
Mean:   36.39
Std:    14.61
Median: 37.0
```

### Wave shape

The 384-point wave starts near zero (novelty/change), rises through several peaks, and falls back. The peaks correspond to regions where the King Wen sequence's transition structure (Hamming distances, trigram changes) concentrates.

---

## What the Construction Actually Does

Strip away the mysticism. The construction is:

1. **Measure transition intensity** in the King Wen sequence (Hamming distances between consecutive hexagrams)

2. **Multi-scale decomposition** — read those transitions at three temporal resolutions (line, trigram, hexagram), analogous to wavelet decomposition at fixed octaves

3. **Combine forward and backward slopes** — the angular term compares the transition entering a point with the transition leaving it, at each scale

4. **Make it fractal** — tile the 384-point result at every power-of-64 scale, creating self-similarity

The output is a wave where:
- **Low values** = high rate of change in the King Wen transition structure ("novelty")
- **High values** = low rate of change ("habit" / stasis)

---

## Critique (Watkins Objection)

Matthew Watkins identified the core mathematical problem: the half-twist (sign modulation) is k-dependent, meaning the collapse from three scales into one doesn't preserve local geometric information. The specific sign-flip pattern has no stated justification. Removing it (Watkins variant) produces a different wave.

More fundamentally: the choice of wave factor 64, the three specific resonance scales (1, 3, 6), and the angular/linear decomposition are all asserted without derivation. The construction works mechanically but the parameter choices are unmotivated.

---

## Relevance to Morpheus

The timewave construction is interesting not as prophecy but as precedent: someone looked at the King Wen transition structure and found multi-scale patterns. Our analysis confirms the sequence has real mathematical structure (higher-than-random Hamming distances, spectral periodicity, forbidden trigram transitions, zero repeated subsequences).

The connection to Axis 5 (transition encoding): the timewave's `h[]` array is literally our Hamming distance sequence from `analysis.py`. The McKennas' intuition — that the transition grammar of states contains predictive information — is what Axis 5 tests empirically on BTC data. The difference: we test against market reality rather than mapping to historical narrative.

---

## Files

- `sequence.py` — King Wen sequence data, trigram decomposition
- `analysis.py` — Seven numerical analyses of the sequence
- `timewave.py` — Reproduction of the McKenna/Kelley/Watkins construction
- `timewave.md` — This document

## Sources

- McKenna & McKenna, *The Invisible Landscape* (1975)
- [kl4yfd/timewave_z3r0](https://github.com/kl4yfd/timewave_z3r0) — C implementation (public domain)
- [blasut/Timewave-Zero-JS](https://github.com/blasut/Timewave-Zero-JS) — JavaScript port
- [Watkins Objection](https://www.fourmilab.ch/rpkp/autopsy.html) — mathematical critique
- [Four Number Sets](https://www.fractal-timewave.com/articles/four_number_sets.htm) — variant history
