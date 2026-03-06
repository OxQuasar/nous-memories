# Threads D+E: Position Trajectory and Weight/Yang Flow — Findings

## Summary

The position trajectory through Z₂³ is structured but only mildly so — no single statistic is individually significant at the 5% level among S=2-free orientations. The weight trajectory is **almost entirely a Layer 3 property**: only 4 of 32 pairs affect weight when orientation flips, and yang drainage (7/8 octets lose yang) has p ≈ 0.50 under complement-pair randomization. The strongest orientation-layer signal discovered is a **single line-pair preference**: among the 16 pairs where L2 ≠ L5, KW places L2=yin first in 12 cases (p = 0.038 one-sided). This reduces to: **KW prefers m=0 (yin at L2) in the first hexagram when the m-axis is asymmetric.** All other positional and weight properties belong to layers above.

---

## Thread D: Position Trajectory

### D1: Full Coverage and Coset Structure

**All 8 positions covered per orbit: YES, always.** This is invariant under orientation — guaranteed because each pair spans 2 distinct positions, and 4 pairs × 2 = 8 = |Z₂³|. Changing orientation only swaps which position is "first" and "second" within each pair; the set of visited positions is unchanged.

**Coset structure:** 5 of 8 orbits (XChu, Shi, WWang, Bo, Xu) have first-hexagram positions forming a coset of a 2-dimensional subgroup of Z₂³. Three orbits (Qian, Zhun, Tai) do not. This matches the earlier Thread A+B finding (5/7 non-trivial orbits). Under random orientation, ~50% of orbits independently form cosets, giving p(≥5) ≈ 0.23 — **not significant**.

### D2: Position Trajectory Autocorrelation

KW's position trajectory (64 steps through Z₂³, encoded as 0-7 integers) has:

| Lag | KW autocorrelation | S=2-free mean | p(≤KW) | p(≥KW) |
|-----|-------------------|---------------|--------|--------|
| 1 | −0.244 | −0.199 | 0.225 | 0.783 |
| 2 | −0.121 | −0.252 | 0.927 | 0.077 |
| 4 | +0.160 | +0.103 | 0.706 | 0.305 |
| 8 | +0.230 | +0.137 | 0.782 | 0.226 |

**No individual lag is significant at 5%.** Lag-2 shows the most suggestive deviation: KW has *less* negative autocorrelation at lag 2 than typical (p = 0.077 for being this un-anticorrelated). This means the position trajectory avoids the common pattern of lag-2 anti-correlation slightly more than random. But it's marginal at best.

### D3: Per-Component Autocorrelation

| Component | Lag | KW | p(≤KW) |
|-----------|-----|-----|--------|
| o (L1) | 1 | −0.175 | 0.317 |
| o (L1) | 2 | −0.032 | 0.981 |
| m (L2) | 1 | −0.016 | 0.808 |
| m (L2) | 2 | −0.097 | 0.362 |
| i (L3) | 1 | −0.111 | 0.569 |
| i (L3) | 2 | +0.032 | 0.773 |

**No per-component autocorrelation is individually significant.** The three position coordinates evolve approximately independently and without strong serial dependence.

### D4: Position-Orbit Cross-Correlation

Lag-0 cross-correlation between position and orbit integer trajectories: **exactly 0.000**. This is algebraically forced: each orbit visits all 8 positions uniformly, so the marginal distribution of positions given any orbit is uniform. Position and orbit are **perfectly uncorrelated** at lag 0.

At non-zero lags:

| Lag | KW cross-corr | Mean | p(≤KW) |
|-----|--------------|------|--------|
| +1 | −0.107 | −0.080 | 0.414 |
| −1 | +0.045 | +0.069 | 0.413 |

**Not significant.** The hidden (position) and visible (orbit) trajectories are essentially independent, confirming the factored-basis decomposition: orbit coordinates and position coordinates live in orthogonal subspaces.

### D5: First-Visit Position Clustering

KW first-visit positions (the position of the first hexagram when each orbit first appears):

| Orbit | First-visit pos | Weight |
|-------|----------------|--------|
| Qian | 111 | 3 |
| Xu | 111 | 3 |
| XChu | 111 | 3 |
| Tai | 111 | 3 |
| Zhun | 100 | 1 |
| Shi | 010 | 1 |
| WWang | 100 | 1 |
| Bo | 000 | 0 |

4 of 8 orbits enter at position (1,1,1) — the all-yang position in the lower half. Mean first-visit position weight = 1.875 (random mean: 1.437). Both statistics are suggestive but not significant:

- P(≥4 first-visits at 111) = 0.187
- P(mean weight ≥ 1.875) = 0.141

**KW shows a mild preference for entering orbits at high-position coordinates, but it's not statistically significant as an isolated finding.**

### D6: Within-Pair Position Transitions

Within-pair position changes match orbit signatures perfectly for all 28 inversion pairs (Δpos = sig). The 4 complement pairs (orbit (0,0,0)) show Δpos = (1,1,1) = OMI ≠ (0,0,0) = sig — as expected, since complement pairs flip all 6 bits.

Bridge kernel dressings (iter2 convention: kernel = (mask[5], mask[4], mask[3]) = upper-half XOR):

| Kernel | Count |
|--------|-------|
| id | 4 |
| O | 6 |
| M | 3 |
| I | 2 |
| OM | 4 |
| OI | 4 |
| MI | 4 |
| OMI | 4 |

The O-dominance (6/31) and I-rarity (2/31) are inherited from Layer 3 (pair ordering), not Layer 4. These match the iter2 findings exactly (chi² = 2.29, 7th percentile).

---

## Thread E: Weight and Yang Flow

### E1: Weight Is Almost Entirely Layer 3

**Critical theorem:** For all 28 inversion pairs, weight(first) = weight(second). Reversal preserves Hamming weight by construction. For the 4 OMI-mask pairs in orbit (1,1,1), all hexagrams have weight 3, so weight is also preserved.

**Weight-sensitive pairs: exactly 4** — the palindromic complement pairs in orbit (0,0,0):

| Pair | First wt | Second wt | Δ |
|------|----------|-----------|---|
| 1 (Qian→Kun) | 6 | 0 | −6 |
| 14 (Yi→Da Guo) | 2 | 4 | +2 |
| 15 (Kan→Li) | 2 | 4 | +2 |
| 31 (Zhong Fu→Xiao Guo) | 4 | 2 | −2 |

**Implication: 28/32 pairs have orientation-invisible weight.** The weight trajectory is overwhelmingly a Layer 3 (pair ordering) property. Only the 4 complement pairs' orientations affect weight at all.

### E2: Complement Pair Weight Pattern

KW pattern: pairs 1 and 31 place heavier first; pairs 14 and 15 place lighter first. This is a 2-heavier/2-lighter split with no obvious rule. The pattern correlates with position — bookend pairs (1,31) go heavy→light; interior pairs near the canon break (14,15) go light→heavy — but with only 4 data points, this is anecdotal.

**S=2 constraint overlap:** Pairs 14, 15, and 31 are in S=2 constraint groups. Pair 1 is unconstrained. So 3 of 4 complement-pair orientations are constrained by S=2 avoidance. Among the 16 possible complement-pair orientations:

- All produce 6 or 7 negative octets
- KW has 7 negative octets (8 of 16 orientations share this)
- Bridge smoothness varies from 51 to 57 (KW = 55, near median)
- Monotone quartets vary from 12 to 13 (KW = 12, half of orientations share this)

**No complement-pair metric distinguishes KW.** The complement-pair orientation is not optimized for any weight-level property.

### E3: Yang Drainage Is Layer 3

KW octet drains: [−5, −4, −2, −1, −2, 0, −1, −1] — 7/8 octets lose yang.

Under random complement-pair orientations (exhaustive 16 possibilities):
- P(≥7 negative octets) = **0.50**

Under full random orientation (100K trials):
- P(≥7 negative octets) = **0.50**

**Yang drainage is EXACTLY a coin flip at Layer 4.** The 7/8 drainage pattern is entirely a Layer 3 property (pair ordering determines which weight pairs are in which octets). Orientation can only flip the 4 complement pairs, and even then the drainage count is equally split between 6 and 7 negative octets.

### E4: Bridge Weight Smoothness

KW bridge weight smoothness (sum of |Δweight| at bridges): 55.

| Metric | KW | Mean | Std | p(≤KW) |
|--------|-----|------|-----|--------|
| Sum \|Δweight\| | 55 | 55.0 | 1.4 | 0.746 |
| Max \|Δweight\| | 4 | 4.0 | 0.0 | 1.000 |

**KW is at the dead median.** Bridge weight smoothness is not affected by orientation (beyond the tiny complement-pair effect). Max bridge weight = 4 is invariant across all S=2-free orientations.

### E5: The L2 < L5 Rule (Nuclear Trigram Discovery)

The trigram analysis (Thread F) found that the "nuclear lower more yang" rule achieves 24/28 on inversion pairs. This reduces algebraically to a single line comparison:

**For inversion pairs where b = reverse(a):**
- nuclear_lower(a) = (L2, L3, L4), nuclear_lower(b) = (L5, L4, L3)
- The sum difference = L2 − L5 (shared L3+L4 cancels)
- So the rule reduces to: **L2 < L5 in the first hexagram**

Testing all three line-pair axes:

| Line pair | Axis | Yin-first | Yang-first | Tied | Best/decisive | p (one-sided) |
|-----------|------|-----------|------------|------|---------------|---------------|
| L1 vs L6 | o | 6 | 10 | 12 | 10/16 | 0.227 |
| **L2 vs L5** | **m** | **12** | **4** | **12** | **12/16** | **0.038** |
| L3 vs L4 | i | 7 | 9 | 12 | 9/16 | 0.402 |

**The m-axis is the unique significant signal.** Among the 16 pairs where L2 ≠ L5 (the m-axis is asymmetric), KW places the hexagram with L2=yin first in 12 of 16 cases (75%, p = 0.038 one-sided).

In position-coordinate language: **when the orbit has m̄=1 (M-asymmetric), KW prefers the hexagram with m=0 (L2=yin) as "first."**

**Significance under S=2-free null:**
- P(best nuclear rule ≥ 24/28) among S=2-free orientations = **0.030**
- But this is the best of 10 tested rules → Bonferroni correction → p ≈ 0.30
- Testing the L2<L5 rule specifically (post-hoc, but with algebraic motivation): p = 0.038

**Assessment:** The L2<L5 preference is the strongest single signal found in orientation. It's marginally significant by itself but loses significance under multiple-testing correction. It is, however, the only positional axis with any detectable preference, and its algebraic cleanness (single line-pair, single coordinate) argues against it being noise.

### E6: Nuclear Rule Exceptions

The 4 pairs where the L2<L5 rule fails (first hex has L2=yang, L5=yin):

| Pair | First hex | Orbit | L2 | L5 |
|------|-----------|-------|----|----|
| 4 (Shi) | 010000 | Shi | 1 | 0 |
| 6 (Tai) | 111000 | Tai | 1 | 0 |
| 10 (Lin) | 110000 | Zhun | 1 | 0 |
| 21 (Sun) | 110001 | Shi | 1 | 0 |

All 4 exceptions have L2=yang, L5=yin. Three of the four first hexagrams have the lower trigram pattern "x1xxxx" — yang at L2. These are concentrated in the first half of the sequence (3 in upper canon, 1 in lower). The lower-canon correction (from Thread A's canon arc finding) partially explains this: the upper canon favors binary-high (which correlates with L2=yang), working against the L2<L5 rule.

---

## Structural Summary

### What Belongs to Which Layer

| Property | Layer | Evidence |
|----------|-------|---------|
| Yang drainage (7/8 octets) | **Layer 3** | p = 0.50 under Layer 4 randomization |
| Weight trajectory (64 values) | **Layer 3** | 28/32 pairs are weight-orientation-invisible |
| Bridge weight smoothness | **Layer 3** | Invariant (mean=55, max=4) across orientations |
| Complement pair weight pattern | **Layer 4** | 4 bits, 3 constrained by S=2; no optimized metric |
| Position coverage (8/8 per orbit) | **Forced** | Invariant under all orientations (tautology) |
| Position-orbit independence | **Forced** | Algebraically forced by uniform orbit partition |
| Coset structure (5/8 orbits) | Not significant | p ≈ 0.23 |
| L2 < L5 preference | **Layer 4** | 12/16 decisive (p = 0.038); m-axis specific |
| Position autocorrelation | Not significant | All lags p > 0.07 |
| First-visit position clustering | Not significant | p ≈ 0.14 for mean weight |

### The L2<L5 Rule: The Only Layer 4 Candidate

Among all properties tested:
- **Weight properties**: entirely Layer 3 (or Layer 2 for the matching rule)
- **Position coverage**: invariant (tautology)
- **Autocorrelation**: not significant
- **Coset structure**: not significant
- **First-visit clustering**: not significant
- **L2 < L5**: marginally significant (p = 0.038), algebraically clean

The L2<L5 rule has a natural interpretation in the factored basis: **when the m-axis is tensioned (asymmetric), present the yin-m-position hexagram first.** This is the only axis-specific orientation preference detected. The o-axis and i-axis show no significant preference.

### Connection to the Canon Arc

Thread A found that binary-high is preferred in the upper canon (67%) and binary-low in the lower canon (37.5%). Binary-high for inversion pairs corresponds to the first differing line (from bottom) being yang. The L2<L5 rule is a different axis: it operates on the m-axis (L2,L5) rather than the first-differing-line (which can be any axis).

The canon arc and L2<L5 rule are **partially overlapping but distinct signals**. Three of the four L2<L5 exceptions are in the upper canon, where the binary-high preference (opposing L2<L5) is strongest. The lower canon, where binary-high preference weakens, is where L2<L5 dominates most cleanly.

### Summary Assessment

**Orientation is loosely constrained (2²⁷ valid) and carries at most one marginally significant signal.** The L2<L5 preference (12/16, p = 0.038) is the strongest candidate for a Layer 4 design principle. Weight, yang flow, and position trajectory structure are all Layer 3 properties — orientation is invisible to them.

The nuclear trigram score of 24/28 (85.7%) is algebraically equivalent to L2<L5 at 12/16 decisive plus 12 ties — visually impressive but statistically modest. KW's orientation at Layer 4 is either:
1. Weakly structured by the L2<L5 preference (with ~4 exceptions), or
2. Genuinely free, with L2<L5 as a statistical fluctuation (p = 0.038 < 0.05 but post-hoc)

The investigation cannot distinguish these two with the available data. The L2<L5 rule's algebraic cleanness (single axis, single coordinate, simple statement) is the main argument for option 1. The multiple-testing concern and small sample (16 decisive pairs) is the main argument for option 2.

---

## Scripts

| Script | Purpose | Key output |
|--------|---------|------------|
| `thread_de_dynamics.py` | Full position trajectory + weight analysis | Position/orbit coverage, yang drainage, weight trajectory |
| `thread_de_deep.py` | Significance testing (50K S=2-free samples) | Autocorrelation p-values, L2<L5 significance, bridge smoothness |
| `trigram_orientation.py` | Trigram rules + nuclear discovery | Nuclear lower yang rule 24/28 → reduces to L2<L5 |
