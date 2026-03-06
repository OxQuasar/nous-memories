# Study 2: Ring Structure and Multi-Scale Dynamics in the King Wen Sequence

> Taking the timewave construction as directional intuition, test whether its core assumptions hold empirically in the sequence itself.

---

## Motivation

The timewave construction makes five implicit claims about the King Wen sequence:

1. The sequence has **ring structure** — antipodal positions are coupled
2. **Bidirectional reading** (forward + antipodal) captures more than forward-only
3. **Multi-scale decomposition** at three fixed octaves (×1, ×3, ×6) extracts real structure
4. **Level + slope** (0th + 1st order) together capture more than either alone
5. The resulting wave is **self-similar** across scales

None of these were tested by the McKennas. The timewave was built on these assumptions and mapped to history. We test the assumptions against their own source data.

---

## Phase 1: Antipodal Coupling

The timewave pairs each position `k` with position `-k mod 64`. Is this coupling real?

**Tests:**

- Compute correlation between `h[k]` and `h[64-k]` across all positions. Is it significant?
- Monte Carlo: generate 10,000 random permutations of the 64 h-values. For each, compute the same antipodal correlation. Where does King Wen fall in the distribution?
- Sweep all possible pairing offsets `d = 1..63`: for each, compute correlation between `h[k]` and `h[(k+d) mod 64]`. Is `d = 32` (diametric/antipodal) actually the strongest coupling, or does some other offset dominate?
- Partial correlation: after controlling for the global mean, does antipodal coupling survive?

**Null hypothesis:** Antipodal positions are no more coupled than any other pairing. King Wen's structure is sequential, not ring-like.

---

## Phase 2: Bidirectional vs Unidirectional

The timewave reads forward slope and antipodal slope simultaneously. Does this capture more information?

**Tests:**

- Forward-only feature for position `k`: `h[k-1] - h[k-2]` (local slope)
- Bidirectional feature: `(h[k-1] - h[k-2]) + (h[-k] - h[1-k])` (timewave's angular term at yao scale)
- Prediction target: `h[k]` (the next transition)
- Mutual information: `MI(forward, h[k])` vs `MI(bidirectional, h[k])` — does the antipodal term add predictive value beyond the forward term?
- Regression: predict `h[k]` from forward-only features vs forward + antipodal features. Compare R² and residual structure.
- Control: repeat with random pairing offsets instead of antipodal. Does the improvement (if any) depend specifically on the antipodal relationship, or does any backward reading help?

**Null hypothesis:** The antipodal slope adds no predictive information about the next transition.

---

## Phase 3: Multi-Scale Decomposition

The timewave uses three scales at fixed ratios (1, 3, 6). Are these ratios justified?

**Tests:**

- Decompose the timewave construction into its three scale contributions independently:
  - Yao-only wave (384 points, just the ×1 scale)
  - Trigram-only wave (384 points, just the ×3 scale)
  - Hexagram-only wave (384 points, just the ×6 scale)
- For each: compute entropy, autocorrelation structure, and spectral content. Which carries the most structured signal?
- Sweep alternative scale ratios: replace (1, 3, 6) with (1, 2, 4), (1, 4, 16), (1, 2, 3), etc. For each combination, generate the 384-point wave and measure structure (autocorrelation energy, spectral concentration, entropy). Are (1, 3, 6) locally optimal?
- FFT of the raw `h[]` sequence: identify natural resonant frequencies. Do they align with periods 64, 192, 384 (the cycle lengths of the three scales)?
- Proper wavelet decomposition (Haar or Daubechies) of `h[]` at equivalent scales — how much signal does sample-and-hold lose compared to real wavelets?

**Null hypothesis:** The ratios (1, 3, 6) are arbitrary. Other ratios produce equally structured or more structured waves.

---

## Phase 4: Level + Slope Interaction

The timewave sums `|angular| + |linear|`. Is this combination meaningful?

**Tests:**

- Correlation between angular and linear terms across all 384 positions. If highly correlated, one is redundant.
- Compare combination methods:
  - `|a| + |b|` (timewave original)
  - `a + b` (signed sum)
  - `a² + b²` (energy)
  - Keep as separate 2D features
- For each method: measure entropy, autocorrelation structure, spectral concentration of the resulting wave. Which produces the most structured output?
- The constant 9: sweep from 0 to 12 in the linear term `(C - h[-k] - h[k-1])`. For each value, measure wave structure. Is 9 special, or does 6 (the true midpoint of [0,12]) or some other value produce a more structured wave?
- Information decomposition: how much of `w[k]`'s variance comes from the linear term vs the angular term vs their interaction?

**Null hypothesis:** The absolute value sum is arbitrary. Signed combination or separate features carry equal or more information.

---

## Phase 5: Self-Similarity

The fractal expansion tiles the 384-point wave at powers of 64. Does the King Wen sequence have intrinsic self-similarity?

**Tests:**

- Autocorrelation of the 384-point Kelley wave at lags 64, 128, 192, 256, 320 — are there peaks at multiples of 64 indicating repeating structure at that scale?
- Fractal dimension estimation: box-counting or Higuchi method on the 384-point wave. Is it genuinely fractal, or is the self-similarity imposed by the expansion rather than inherent?
- Scaling factor sweep: apply the fractal expansion `f(x)` with wave factors 2, 4, 8, 16, 32, 64, 128, 256. For each, compute the fractal dimension and self-similarity metrics of the resulting wave. Is 64 special (matching 64 hexagrams) or does the expansion work equally well at any factor?
- Cross-scale mutual information: for the fractal wave, compute MI between `f(x)` sampled at scale `s` and `f(x)` sampled at scale `64*s`. Does zooming in/out actually reveal correlated patterns?
- Compare against fractal expansion of random 384-point waves (same value distribution, random order). Does the King Wen wave exhibit more self-similarity than chance?

**Null hypothesis:** The self-similarity is an artifact of the fractal expansion (which imposes self-similarity on any input) rather than a property of the King Wen sequence.

---

## Execution

All tests in Python, extending `analysis.py` and `timewave.py`. Each phase produces:

- Test statistic with p-value against null (Monte Carlo with 10,000 random permutations of the King Wen sequence)
- Effect size (how much better than random, not just whether it's significant)
- Visualization where useful

Phases are independent and can run in parallel.

---

## Success Criteria

For each of the five timewave assumptions, one of three outcomes:

| Outcome | Meaning |
|---------|---------|
| **Confirmed** | The assumption holds with statistical significance (p < 0.01) and meaningful effect size in the King Wen sequence |
| **Rejected** | The assumption doesn't hold — King Wen is indistinguishable from random on this axis |
| **Partially confirmed** | The assumption holds in modified form (e.g., coupling exists but at a different offset than antipodal, or different scale ratios outperform (1,3,6)) |

The partial confirmations are the most interesting — they point to real structure that the timewave construction approximated but didn't nail precisely.

---

## Results

### Phase 1: Antipodal Coupling — REJECTED

Antipodal correlation (d=32) is r=0.103, ranking 27th out of 63 possible offsets. Monte Carlo p=0.58 — indistinguishable from random.

The strongest coupling is at offsets d=28 and d=36 (r=0.294), not the diametric position. Adjacent correlation (d=1) is r=-0.262 — consecutive hexagrams are weakly anti-correlated (high transition followed by low transition), which is a real sequential property. But the ring/antipodal structure the timewave assumes does not exist.

**Verdict:** The timewave's pairing of each position with its diametric opposite is arbitrary. The King Wen sequence has sequential structure (adjacent anti-correlation), not ring structure.

### Phase 2: Bidirectional vs Unidirectional — INCONCLUSIVE

Single-variable correlation with next transition: forward-only r=-0.199, bidirectional r=-0.302. The bidirectional reading improves R² from 0.039 to 0.091. But multi-feature regression (forward + antipodal as separate features) gives negative R² — overfitting on 64 samples.

Antipodal offset ranks 25th out of 63 for predictive value. The improvement from bidirectional reading is not specific to the antipodal relationship — many offsets produce similar gains.

Regression weights (forward=-0.158, antipodal=-0.147) are nearly equal, suggesting the improvement comes from any second feature reducing noise, not from a meaningful antipodal signal.

**Verdict:** Adding a second reading angle helps slightly, but there's nothing special about the antipodal angle. The bidirectional principle is weakly useful; the specific pairing is not.

### Phase 3: Multi-Scale Decomposition — PARTIALLY CONFIRMED (wrong ratios)

The timewave's ratios (1,3,6) rank **9th out of 12** combinations tested on combined structure score (autocorrelation energy + spectral concentration):

| Ratios | Score |
|--------|-------|
| (1,8,32) | 13.80 |
| (1,4,16) | 8.42 |
| (2,6,12) | 5.74 |
| (1,6,12) | 5.70 |
| (1,3,9) | 4.31 |
| ... | ... |
| **(1,3,6)** | **2.32** |
| (1,2,4) | 2.03 |
| (1,2,3) | 1.18 |

The principle of multi-scale decomposition is sound — combining scales always outperforms single-scale. But the timewave chose suboptimal ratios. Wider separation between scales (1,8,32) captures far more structure. The raw h[] sequence has a dominant period of 2.0 hexagrams, which doesn't naturally align with the (1,3,6) cycle structure.

Individual scale comparison: hexagram-only (×6) has the highest autocorrelation energy (2.07), followed by trigram (1.10), then yao (0.64). The coarsest scale carries the most structured signal.

**Verdict:** Multi-scale decomposition works. The specific ratios (1,3,6) are suboptimal — wider scale separation captures more structure.

### Phase 4: Level + Slope Interaction — PARTIALLY CONFIRMED (wrong parameters)

Angular and linear terms are perfectly uncorrelated (r=0.000) — they capture genuinely orthogonal information. This is a real property: level and slope measure independent aspects of the transition structure.

Variance decomposition of `w[k] = |a| + |b|`:
- |angular| (slope): 40.9% of variance
- |linear| (level): 65.3% of variance
- Covariance: -6.2%

However, the combination method is suboptimal. Structure scores by method:

| Method | Score |
|--------|-------|
| \|b\| only (linear) | 1.80 |
| a² + b² (energy) | 1.63 |
| \|a\| + \|b\| (original) | 1.44 |
| a + b (signed) | 1.36 |
| \|a\| only (angular) | 1.09 |

Linear alone produces a more structured wave than the combined timewave formula. The angular term adds noise when combined via absolute-value sum.

The constant 9 in the linear term ranks 8th out of 13 values. Constants 0-5 produce more structured waves — smaller constants make the linear term more sensitive to the actual h-values rather than being dominated by the constant.

**Verdict:** Level and slope are genuinely independent signals. But the timewave's specific combination (|a| + |b| with C=9) is worse than using the linear term alone. The independent information exists; the construction fails to exploit it properly.

### Phase 5: Self-Similarity — REJECTED

No significant autocorrelation at multiples of 64. The six 64-element segments of the wave have a mean off-diagonal correlation of -0.056 (z=-1.72, p=0.97). King Wen's wave is slightly *less* self-similar than random.

Segment correlation matrix reveals structure that is antipodal rather than self-similar: segments 0 and 3 correlate (+0.45), segments 1 and 4 correlate (+0.60), but these pairs are anti-correlated with each other. This is a half-period oscillation, not fractal self-similarity.

Scaling factor sweep shows near-zero mean pairwise correlation at all split sizes except 192 (two halves, r=+0.41), which reflects the half-twist's fold structure.

**Verdict:** The 384-point wave has no intrinsic self-similarity at any scale. The fractal expansion imposes self-similarity mechanically rather than revealing a property of the King Wen sequence. The observed structure is oscillatory (half-period), not fractal.

---

## Summary

| Assumption | Verdict | Key Finding |
|-----------|---------|-------------|
| Antipodal coupling | **Rejected** | r=0.10, rank 27/63, p=0.58. No ring structure. |
| Bidirectional reading | **Inconclusive** | Weak improvement, not specific to antipodal offset. |
| Multi-scale (1,3,6) | **Partially confirmed** | Multi-scale works; (1,3,6) ranks 9th of 12. Wider separation is better. |
| Level + slope | **Partially confirmed** | Independent signals (r=0.00); but linear alone outperforms the combination. |
| Self-similarity | **Rejected** | No intrinsic fractal structure. z=-1.72, p=0.97. |

**What the timewave got right:** Multi-scale decomposition extracts real structure from the King Wen transition sequence, and level/slope capture independent information.

**What it got wrong:** The specific parameters (antipodal pairing, ratios 1:3:6, constant 9, absolute-value combination) are all suboptimal. The fractal self-similarity is imposed, not discovered. The construction works mechanically but its parameter choices are not justified by the data it claims to derive from.

**What's actually in the data:** The King Wen sequence has sequential structure (adjacent anti-correlation), coarse-scale dominance (hexagram-level patterns carry the most signal), and a half-period oscillatory pattern in the 384-point wave. These are real properties — but they point toward different analytical tools than the timewave construction used.
