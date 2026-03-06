# Round 3: Anatomy, Annealing, and the Domination Discovery

## KW Reference Profile

| Metric | KW Value | Direction |
|--------|----------|-----------|
| Kernel χ² | 2.290 | Lower = better |
| Canon asymmetry | +3 | Higher = better |
| M-score | 12/16 | Higher = better |
| Kernel autocorrelation | −0.464 | More negative = better |

---

## The Headline: KW Is Not Pareto-Optimal

Simulated annealing and exhaustive enumeration discovered **12 orientations that Pareto-dominate KW** — matching or exceeding KW on all 4 axes.

The minimal dominator requires only **2 free-bit flips** (Hamming distance 2 from KW):

| Property | KW | Dominator (2-flip) |
|----------|----|--------------------|
| Orientation | `00000000000000000000000000000000` | `00000000000000000000010000000100` |
| χ² | 2.290 | 2.290 (equal) |
| asym | +3 | +3 (equal) |
| m_score | 12/16 | 12/16 (equal) |
| kac | −0.464 | **−0.474** (better) |
| Hamming from KW | — | 2 |

The two flips: **pair 21 (Lin/Guan)** + **component (29,30)**.

The strongest dominator flips 6 free bits and achieves kac=−0.513 (10.4% better than KW).

### What This Means

The iter4 finding that "zero of 27 single-bit flips improve any axis without degrading another" remains true. But **2-bit combinations can escape the single-bit Pareto barrier.** KW is a local Pareto optimum at Hamming distance 1, but not at distance 2.

The escape mechanism is **chi² epistasis**: each of the two flips individually improves chi² by ~1.0, but together the improvements exactly cancel (+2.065 epistatic interaction). Meanwhile their kac improvements are additive. The result: a 2-flip move that is chi²-neutral, asym-neutral, m-neutral, and kac-improving.

---

## Priority 1: Anatomy of the Hamming-4 Neighbor

The R2-Ef "m dominant" orientation (Hamming 4 from KW) differs at pairs {9, 10, 11, 21}.

### Per-Bit Effects

| Pair | M-dec | Δχ² | Δasym | Δm | Δkac | Pareto | Kernel Effect |
|------|-------|-----|-------|-----|------|--------|---------------|
| 9 | Y | −0.516 | −1 | +1 | +0.015 | trade-off | B8:O→M, B9:MI→OI |
| 10 | N | −0.516 | +1 | 0 | +0.144 | trade-off | B9:MI→M, B10:id→I |
| 11 | N | +2.065 | +1 | 0 | +0.041 | trade-off | B10:id→O, B11:OMI→MI |
| 21 | N | −1.032 | +1 | 0 | +0.003 | trade-off | B20:OI→I, B21:O→id |

### Additivity Test

| | Δχ² | Δasym | Δm | Δkac |
|---|-----|-------|-----|------|
| Additive prediction | +0.000 | +2 | +1 | +0.203 |
| Actual combined | **−1.548** | +2 | +1 | +0.158 |
| Epistasis | **−1.548** | 0 | 0 | −0.045 |

**Strong chi² epistasis.** The 4-bit combination achieves 1.548 better chi² than the additive prediction. Asym and m-score are perfectly additive. kac shows mild epistasis (−0.045).

### Interpretation

Only 1 of 4 bits is M-decisive; only 1 improves m-score. But ALL 4 worsen kac. KW keeps these bits at 0 primarily to preserve kac, not to maximize m-score. The m-dominant orientation trades kac for chi² (epistatic chi² improvement) and a small m-score gain.

---

## Priority 2: Simulated Annealing

### Design

Two objectives targeting KW's exact profile:
- **Minimax**: minimize max(|metric − KW|/scale) across 4 axes
- **L1**: minimize sum(|metric − KW|/scale) across 4 axes

50 runs each, 100K steps, geometric cooling (T₀=1.0, α=0.999).

### Results

| Objective | Best cost | χ² | asym | m | kac | Ham | Pareto |
|-----------|-----------|-----|------|---|------|-----|--------|
| Minimax | 0.082 | 2.290 | +3 | 12 | −0.426 | 8 | dominated-by-kw |
| **L1** | **0.011** | **2.290** | **+3** | **12** | **−0.470** | **10** | **dominates-kw** |

### Minimax (50 runs)

- 0 dominate KW, 41 dominated by KW, 9 trade-offs
- Best matches KW on 3 axes but kac=−0.426 (worse)
- Mean Hamming from KW: 9.2

### L1 (50 runs)

- **2 dominate KW**, 34 dominated by KW, 14 trade-offs
- Best matches KW on 3 axes with kac=−0.470 (better by 1.1%)
- Mean Hamming from KW: 9.6
- Mutual Hamming distances among top 10: mean 8.1 (spread, not clustered)

### Why L1 Succeeds and Minimax Doesn't

Minimax penalizes the worst axis equally regardless of direction. When kac is slightly better than KW, minimax doesn't reward it — it focuses on whichever axis deviates most. L1 rewards improvement on kac even while maintaining equality on other axes. The asymmetry means L1 can exploit the kac improvement direction that minimax ignores.

---

## Priority 3: Asymmetry as Substrate Effect

### Conditional Analysis (10,000 random S=2-free orientations)

| Condition | N | Mean asym | Interpretation |
|-----------|---|-----------|---------------|
| Unconditional | 10,000 | −1.556 | Negative baseline |
| χ² < 3.0 | 997 (10.0%) | −0.868 | Less negative, still negative |
| kac < −0.3 | 1,547 (15.5%) | −1.993 | More negative |
| χ² < 3.0 AND kac < −0.3 | 107 (1.1%) | −1.421 | Still negative |
| m ≥ 10 | 2,113 (21.1%) | −1.670 | Roughly baseline |

### Correlation Matrix

| | chi² | asym | m | kac |
|---|------|------|---|-----|
| chi² | — | −0.077 | −0.079 | −0.091 |
| asym | | — | −0.047 | +0.094 |
| m | | | — | +0.035 |
| kac | | | | — |

### Verdict

**Asymmetry is NOT a substrate effect.** Conditioning on kernel balance (χ² < 3.0) shifts mean asymmetry from −1.556 to −0.868, but it remains firmly negative. KW's +3 is still exceptional even among kernel-balanced orientations. Positive asymmetry requires an independent mechanism.

The weak positive correlation between asym and kac (+0.094) and between m and kac (+0.035) suggests slight coupling but nowhere near enough to explain KW's profile as a single-axis side effect.

---

## Priority 4: KW's M-Rule Exceptions

### The 4 Exceptions

KW follows the M-rule (L2=yin first) at 12 of 16 M-decisive pairs. The 4 exceptions:

| Pair | L2(a) | L5(a) | Δχ² if flipped to M-rule | Δasym | Δm | Δkac | Can flip? |
|------|-------|-------|--------------------------|-------|-----|------|-----------|
| 3 | 1 | 0 | 0.000 | −1 | +1 | **+0.077** | Yes |
| 5 | 1 | 0 | 0.000 | −1 | +1 | **+0.163** | Yes |
| 9 | 1 | 0 | −0.516 | −1 | +1 | **+0.015** | Yes |
| 20 | 1 | 0 | — | — | — | — | **No (S=2)** |

### Pattern

At all 3 non-constrained exceptions, flipping to the M-rule would:
- Improve m-score by +1 (as expected — that's what the M-rule does)
- **Worsen kac** (by +0.015 to +0.163)
- Worsen asymmetry by −1

**KW consistently protects kac over M-preference.** At every M-decisive pair where the M-rule and kac conflict, KW chooses kac. The 4th exception (pair 20) is structurally forced by the S=2 constraint.

This directly answers the Round 1 question: "Why does KW have m=12 instead of m=15?" Because 3 of the 4 M-rule violations protect kac, and 1 is structurally forced. The M-rule is the default; kac-preservation is the override.

---

## The Domination Discovery: Full Analysis

### All 12 Dominating Orientations

| # | Free bits flipped | Hamming | χ² | asym | m | kac |
|---|-------------------|---------|-----|------|---|------|
| 1 | {17, 26} | 2 | 2.290 | +3 | 12 | −0.474 |
| 2 | {9, 10, 16, 17} | 4 | 1.774 | +3 | 12 | −0.474 |
| 3 | {9, 17, 23, 24} | 6 | 1.258 | +3 | 12 | −0.547 |
| 4 | {0, 6, 9, 17, 23} | 6 | 2.290 | +3 | 12 | −0.513 |
| 5 | {6, 9, 15, 17, 23} | 6 | 2.290 | +3 | 12 | −0.539 |
| 6 | {9, 10, 16, 17, 23} | 6 | 1.774 | +3 | 12 | −0.475 |
| 7 | {9, 11, 17, 23, 24} | 7 | 2.290 | +4 | 12 | −0.519 |
| 8 | {9, 15, 17, 20, 23} | 6 | 2.290 | +3 | 12 | −0.524 |
| 9 | {9, 15, 17, 21, 23} | 6 | 2.290 | +3 | 12 | −0.525 |
| 10 | {9, 10, 11, 16, 17, 26} | 6 | 1.774 | +3 | 12 | −0.477 |
| 11 | {9, 11, 15, 17, 23, 24} | 8 | 2.290 | +3 | 12 | −0.534 |
| 12 | {9, 11, 17, 23, 24, 26} | 8 | 2.290 | +3 | 12 | −0.532 |

### Free Bit Frequency Across Dominators

| Free bit | Pair(s) | Frequency | Note |
|----------|---------|-----------|------|
| **17** | 21 (Lin/Guan) | **12/12** | **Necessary for domination** |
| **9** | 9 | **11/12** | Nearly necessary |
| 23 | (19,20) component | 9/12 | Common |
| 24 | (25,26) component | 4/12 | |
| 15 | 17 | 4/12 | |
| 11 | 11 | 4/12 | |
| Others | various | 1–3/12 | |

### The Bit 17 (Pair 21) Anomaly — Resolved

In iter4, bit 17 was flagged as anomalous: it achieved Δχ²=−1.032 at Δkac=+0.003, a ~15× better efficiency ratio than any other bit. The iter4 analysis posed two readings:

1. KW resolves at 0.6% of the kac range (precision)
2. Bit 17 pays on a 5th axis not yet measured

**Neither reading is correct.** Bit 17 is the gateway to Pareto domination. It appears in **every** dominating orientation. Its near-zero kac cost makes it the one bit that can be flipped without significant kac degradation — and when combined with bit 26 (which also has small kac cost), the chi² epistasis creates a zero-cost escape from the single-bit Pareto barrier.

The anomaly was not precision or a hidden axis. It was a **structural ridge** on the Pareto frontier — a near-tangent direction that, when extended to 2 dimensions, exits the Pareto-optimal set entirely.

### Mechanism: Chi² Epistasis

| Component | Δχ² (single) | Δχ² (combined) | Epistasis |
|-----------|-------------|----------------|-----------|
| Bit 17 alone | −1.032 | — | — |
| Bit 26 alone | −1.032 | — | — |
| Additive prediction | −2.065 | — | — |
| Actual (17+26) | — | **0.000** | **+2.065** |

The chi² metric is quantized in steps of 0.516 and partially epistatic (iter4 finding). Two individually chi²-improving bits can exactly cancel when combined, if they push the same kernel types in opposite directions. This epistasis is the mechanism enabling domination: kac improves additively while chi² cancels epistatically.

---

## Summary of Findings

1. **KW is NOT globally Pareto-optimal.** 12 orientations dominate it, the closest at Hamming distance 2. All match KW on axes 1–3 and strictly beat it on axis 4 (kac).

2. **Bit 17 (pair 21, Lin/Guan) is the key.** It appears in all 12 dominators. The iter4 anomaly (15× efficiency ratio) was the signal of a structural ridge on the Pareto frontier.

3. **The escape mechanism is chi² epistasis.** Bits that individually improve chi² can cancel when combined, producing a chi²-neutral kac-improving move.

4. **KW's M-rule exceptions protect kac.** At all 3 non-constrained M-decisive pairs where KW deviates from the M-rule, following the M-rule would worsen kac.

5. **Asymmetry is genuinely independent.** It is not a substrate effect of kernel balance or sequential diversity. It requires its own mechanism.

6. **The generative hierarchy refines to:** M-rule as default → kac-preservation overrides at specific positions → but with a residual gap (KW doesn't take the 2-bit kac improvement that exists).

---

## Open Question: Why Doesn't KW Take the 2-Bit Improvement?

KW could improve kac from −0.464 to −0.474 by flipping just 2 bits (pair 21 + component 29,30). Why doesn't it?

Three hypotheses:
1. **5th axis.** These 2 bits pay on an unmeasured axis. (Consistent with iter4's per-round pattern of discovering new constraints.)
2. **Process limitation.** The arranger's construction process couldn't detect a 2-step cooperative improvement — single-bit perturbations showed no improvement (consistent with the single-bit Pareto barrier).
3. **Not meaningful.** The kac difference (−0.464 vs −0.474) is 2.2% and may fall within the noise floor of whatever principle generated the orientation.

---

## Data Files

| File | Contents |
|------|----------|
| round3_anatomy.py | Priorities 1, 3, 4 implementation |
| round3_annealing.py | Priority 2 (SA) implementation |
| round3_data.json | Combined results from all priorities |
| round3_sa_data.json | Full SA run data (50 runs × 2 objectives) |
| round3_dominators.json | All 12 dominating orientations with metadata |
