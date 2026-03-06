# Kernel Independence Findings (Round 3)

## Question

The kernel chain shows two properties: (1) near-uniform frequency (chi² = 2.29, 7th percentile) and (2) OMI-dominated consecutive XORs (26.7% vs 12.5% expected). Are these one signal or two?

## Answer

**Two independent signals.** The correlation is r = −0.035 (essentially zero). The conditional p-values are nearly identical to the marginals. The joint probability matches the product of marginals within noise.

---

## Method

50,000 random completions on KW's Eulerian path with KW's matching. For each:
- chi² of kernel frequency from uniform (31 kernels across 8 generators)
- OMI-XOR fraction (count of OMI in 30 consecutive kernel XORs)
- Mean XOR Hamming weight (average distance between consecutive kernels)

---

## Key Results

### 1. Marginal P-Values (50K samples)

| Metric | KW value | Sample mean ± std | P-value | Direction |
|--------|----------|-------------------|---------|-----------|
| Chi² (uniformity) | 2.29 | 7.08 ± 3.74 | **0.068** | lower = more uniform |
| OMI-XOR fraction | 0.267 (8/30) | 0.126 ± 0.061 | **0.029** | higher = more contrastive |
| Mean XOR weight | 1.77 | 1.50 ± 0.16 | **0.058** | higher = more distant |

All three are marginal to significant. KW's kernel chain is simultaneously more uniform, more contrastive, and more distant than random — three different ways of saying the same thing? No:

### 2. Correlation Analysis

| Pair | Pearson r | Interpretation |
|------|-----------|----------------|
| chi² vs OMI-XOR | **−0.035** | Essentially zero |
| chi² vs mean XOR weight | **−0.165** | Weak negative (uniform → slightly higher mean weight) |
| OMI-XOR vs mean XOR weight | **+0.655** | Strong positive (OMI fraction drives mean weight) |

The chi²–OMI correlation is negligible. Uniform chains do NOT preferentially produce OMI XORs.

OMI fraction and mean XOR weight are strongly correlated (r = 0.65) — they're essentially the same signal, since OMI (weight 3) is the heaviest possible XOR.

### 3. Conditional Analysis

**Conditioning on chi² ≤ 2.29 (the ~7% most uniform):**

| Metric | Conditional | Unconditional |
|--------|-------------|---------------|
| Mean OMI fraction | 0.130 | 0.126 |
| P(OMI ≥ KW) | **3.08%** | 2.93% |

Virtually identical. Knowing a chain is uniform tells you nothing about its OMI XOR pattern.

**Conditioning on OMI ≥ 0.267 (the ~3% most OMI-rich):**

| Metric | Conditional | Unconditional |
|--------|-------------|---------------|
| Mean chi² | 7.07 | 7.08 |
| P(chi² ≤ KW) | **7.16%** | 6.82% |

Again virtually identical. OMI-rich chains are no more uniform than typical.

### 4. Joint P-Value

| Quantity | Value |
|----------|-------|
| P(chi² ≤ KW AND OMI ≥ KW) | **0.00210** (105/50,000) |
| Expected if independent | 0.00200 (= 0.068 × 0.029) |
| Ratio observed/independent | **1.05** |

The ratio is 1.05 — essentially 1.0. The joint probability is the product of marginals. **The signals are independent.**

Triple joint: P(chi² ≤ KW AND OMI ≥ KW AND xw ≥ KW) = **0.00156** (78/50,000). This combines all three kernel chain properties.

### 5. Decile Analysis

Chi² decile vs OMI fraction — completely flat:

| Decile | Chi² range | Mean OMI | P(OMI ≥ KW) |
|--------|-----------|----------|-------------|
| D1 (most uniform) | [0.2, 2.8] | 0.130 | 3.0% |
| D5 (median) | [5.4, 6.4] | 0.127 | 3.0% |
| D10 (least uniform) | [12.1, 34.8] | 0.122 | 3.2% |

No trend. The OMI-XOR rate is independent of kernel uniformity across the entire range.

### 6. XOR Weight Distribution

The random baseline XOR distribution is perfectly uniform over Z₂³ (each element appears 12.5%). This means the XOR weight distribution follows the binomial weighting of Z₂³:

| Weight | Elements | KW /30 | Random /30 | Excess |
|--------|----------|--------|-----------|--------|
| 0 (id) | 1 | **2** (6.7%) | 3.8 (12.6%) | −1.8 |
| 1 (O,M,I) | 3 | **11** (36.7%) | 11.2 (37.4%) | −0.2 |
| 2 (OM,OI,MI) | 3 | **9** (30.0%) | 11.2 (37.4%) | −2.2 |
| 3 (OMI) | 1 | **8** (26.7%) | 3.8 (12.6%) | **+4.2** |

KW has a massive excess at weight 3 (OMI) and corresponding deficit at weights 0 and 2. The mean XOR weight is 1.77 vs 1.50 expected — a 0.27 shift toward heavier (more different) consecutive kernels.

The weight-1 count (11/30) is exactly at the expected value. The redistribution is specifically: weight 0 and 2 → weight 3. KW doesn't just avoid repeats — it concentrates the "savings" specifically into full complements.

---

## Conclusion

The KW kernel chain has **two independent design principles**:

1. **Uniform marginal frequency** (p = 0.068): Each of the 8 generators appears approximately equally often. This is a distributional property — how many of each generator, regardless of order.

2. **Maximal consecutive contrast** (p = 0.029): Consecutive kernel dressings tend to be maximally different (OMI XOR). This is a sequential property — the order in which generators appear.

These are genuinely independent (r = −0.035). Neither explains the other. The joint probability is **p ≈ 0.002** — roughly 1 in 500 random completions achieve both simultaneously.

Together with the kernel XOR weight analysis, the design principle can be stated precisely: **distribute generators uniformly, and when stepping between consecutive bridges, prefer the full complement (flip all three generator bits) over any partial change.**

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `kernel_independence.py` | Joint analysis of chi² vs OMI-XOR (50K samples) | ✓ Complete |
