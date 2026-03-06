# Round 1: Baseline Generators — Results

## KW Reference Profile

| Metric | KW Value | Direction |
|--------|----------|-----------|
| Kernel χ² | 2.290 | Lower = better |
| Canon asymmetry | +3 | Higher = better |
| M-score | 12/16 | Higher = better |
| Kernel autocorrelation | −0.464 | More negative = better |

---

## A1: Random S=2-Free Orientation (10,000 samples)

### Distribution

| Metric | Mean | Std | Min | P5 | P50 | P95 | Max | KW | KW %ile |
|--------|------|-----|-----|-----|-----|-----|-----|-----|---------|
| chi² | 7.279 | 3.803 | 0.226 | 2.290 | 6.419 | 14.677 | 28.097 | 2.290 | 6.3% |
| asym | −1.556 | 2.410 | −11 | −5 | −2 | +2 | +7 | +3 | 4.4% |
| m_score | 7.999 | 1.867 | 2 | 5 | 8 | 11 | 15 | 12 | 2.9% |
| kac | −0.135 | 0.165 | −0.688 | −0.395 | −0.142 | +0.147 | +0.516 | −0.464 | 1.9% |

### Pareto Comparison to KW

| Relationship | Count | % |
|-------------|-------|---|
| Dominate KW | 0 | 0.00% |
| Dominated by KW | 9,276 | 92.76% |
| Trade-off | 724 | 7.24% |
| Equal | 0 | 0.00% |

---

## A2: All-Flipped Orientation

All-32-flipped violates S=2 at bridge 29. Used 27-free-bits-flipped variant (S=2-compliant).

| Property | Value |
|----------|-------|
| Orientation | `11111111111111111111111111111101` |
| Hamming from KW | 31 |
| chi² | 3.839 |
| asym | −6 |
| m_score | 4/16 |
| kac | −0.376 |
| Per-axis | chi²:worse, asym:worse, m_score:worse, kac:worse |
| **Pareto** | **dominated-by-kw** |

---

## B1: Greedy χ² Minimizer (100 random starts)

### Distribution (post-optimization)

| Metric | Mean | Std | Min | P5 | P50 | P95 | Max | KW | KW %ile |
|--------|------|-----|-----|-----|-----|-----|-----|-----|---------|
| chi² | 0.711 | 0.341 | 0.226 | 0.226 | 0.742 | 1.258 | 1.774 | 2.290 | 100% |
| asym | −1.140 | 2.035 | −6 | −4 | −1 | +2 | +4 | +3 | 4.0% |
| m_score | 8.470 | 2.234 | 2 | 5 | 8 | 12 | 15 | 12 | 9.0% |
| kac | −0.114 | 0.144 | −0.463 | −0.341 | −0.096 | +0.099 | +0.243 | −0.464 | 0.0% |

### Best χ² Orientation

| Property | Value |
|----------|-------|
| Orientation | `10000011101101100000010101111100` |
| Hamming from KW | 15 |
| chi² | 0.226 |
| asym | +2 |
| m_score | 9/16 |
| kac | −0.083 |
| Per-axis | chi²:better, asym:worse, m_score:worse, kac:worse |
| **Pareto** | **trade-off** |

### Pareto Summary

| Relationship | Count |
|-------------|-------|
| Dominate KW | 0 |
| Dominated by KW | 0 |
| Trade-off | 100 |
| Equal | 0 |

---

## B2: Greedy kac Minimizer (100 random starts)

### Distribution (post-optimization)

| Metric | Mean | Std | Min | P5 | P50 | P95 | Max | KW | KW %ile |
|--------|------|-----|-----|-----|-----|-----|-----|-----|---------|
| chi² | 8.974 | 3.358 | 2.806 | 3.323 | 9.000 | 15.194 | 15.710 | 2.290 | 0.0% |
| asym | −2.050 | 2.037 | −6 | −5 | −2 | +2 | +3 | +3 | 2.0% |
| m_score | 8.700 | 1.962 | 4 | 5 | 9 | 12 | 12 | 12 | 7.0% |
| kac | −0.706 | 0.046 | −0.785 | −0.769 | −0.709 | −0.631 | −0.577 | −0.464 | 100% |

### Best kac Orientation

| Property | Value |
|----------|-------|
| Orientation | `00110101000000001111110001111100` |
| Hamming from KW | 15 |
| chi² | 15.194 |
| asym | −4 |
| m_score | 11/16 |
| kac | −0.785 |
| Per-axis | chi²:worse, asym:worse, m_score:worse, kac:better |
| **Pareto** | **trade-off** |

### Pareto Summary

| Relationship | Count |
|-------------|-------|
| Dominate KW | 0 |
| Dominated by KW | 0 |
| Trade-off | 100 |
| Equal | 0 |

---

## C1: M-Component Rule

Rule: orient each pair so L2=yin comes first (M-decisive pairs); binary-high-first for M-indecisive pairs.

Raw orientation violates S=2 at bridges {13, 19, 27}. Fixed by flipping 3 bits.

| Property | Value |
|----------|-------|
| Raw orientation | `00010100011100100100100100001100` |
| Final orientation | `00010100011101100101100100011100` |
| Hamming from KW | 14 |
| chi² | 4.871 |
| asym | −1 |
| m_score | 15/16 |
| kac | +0.062 |
| Per-axis | chi²:worse, asym:worse, m_score:better, kac:worse |
| **Pareto** | **trade-off** |

---

## C2: Sequential Kernel Diversity

Rule: process pairs in order, choose orientation maximizing kernel Hamming distance from previous bridge; tie-break by least-seen kernel.

| Property | Value |
|----------|-------|
| Orientation | `00010101000100001111110000011100` |
| Hamming from KW | 13 |
| chi² | 8.484 |
| asym | −2 |
| m_score | 12/16 |
| kac | −0.666 |
| Per-axis | chi²:worse, asym:worse, m_score:equal, kac:better |
| **Pareto** | **trade-off** |

Kernel distribution: id=6, O=7, M=3, I=2, OM=3, OI=1, MI=6, OMI=3

---

## Summary Table

| Generator | χ² | asym | m_score | kac | Hamming | Pareto vs KW |
|-----------|-----|------|---------|------|---------|--------------|
| **KW** | **2.290** | **+3** | **12** | **−0.464** | **0** | reference |
| A1 (median) | 6.419 | −2 | 8 | −0.142 | ~16 | (distribution) |
| A2 | 3.839 | −6 | 4 | −0.376 | 31 | dominated-by-kw |
| B1 (best) | 0.226 | +2 | 9 | −0.083 | 15 | trade-off |
| B2 (best) | 15.194 | −4 | 11 | −0.785 | 15 | trade-off |
| C1 | 4.871 | −1 | 15 | +0.062 | 14 | trade-off |
| C2 | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |
