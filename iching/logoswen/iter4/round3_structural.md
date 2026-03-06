# Round 3: Structural Census — What Does the Improvement Cone Cost?

## Setup

80 structural properties computed for each orientation, across 5 categories:
- **Trigram transitions** (chi², distinct count, self-transitions)
- **Line autocorrelation & FFT** (per-line memory, spectral energy, dominant frequency)
- **Hamming distances** (within-pair, bridge, consecutive)
- **Pair-internal symmetry** (complement, inversion, palindrome counts, ordering)
- **Sequence patterns** (trigram runs/boundaries, weight distribution, positional balance)

**Calibration:** 200 random S=2-free orientations establish the null distribution. A property is **significant** if the flipped value falls at ≤5th or ≥95th percentile.

**25 properties are orientation-invariant** (identical for all S=2-free orientations): trigram uniformity, line-pair correlations, pair Hamming statistics, complement/inversion/palindrome counts, line balance, weight mean/std, half-yang counts. These reflect the pair structure, not the orientation.

**55 properties are variable.** Of these, **6 are extreme in KW** (≤5th or ≥95th percentile).

---

## KW Extremities (before any flips)

Properties where KW is already extreme among S=2-free orientations:

| Property | KW | Pctile | Random μ | Random σ |
|:---------|---:|-------:|---------:|---------:|
| **kernel_autocorr_1** | **−0.464** | **0.0%** | −0.110 | 0.167 |
| line_0_autocorr_sum | 0.605 | 5.0% | 0.977 | 0.235 |
| line_0_fft_energy | 530 | 95.5% | 518.2 | 8.62 |
| upper_first_larger | 10 | 98.0% | 7.48 | 1.63 |
| line_4_fft_energy | 562 | 99.5% | 520.3 | 11.76 |
| line_4_dominant_freq | 32 | 100.0% | 21.9 | 5.97 |

**kernel_autocorr_1 = −0.464** is the most extreme: more negative than any of the 200 random orientations. This means KW's bridge kernel chain has maximal **anti-autocorrelation** — consecutive bridges almost always have *different* kernel dressings. This is distinct from χ² uniformity (which measures the histogram, not the sequence order). KW optimizes both the *distribution* and the *sequential ordering* of kernels.

**upper_first_larger = 10** (98th percentile) is the already-known asymmetry signal.

**line_4** and **line_0** have extreme FFT properties — specific spectral signatures in lines 1 and 5 (in traditional numbering) that are unusually strong.

---

## Experiment 1: bits {10,17} — Improvement Cone

23 of 80 properties change. 6 reach significance.

### Significant changes (new signals not redundant with χ²/asym/m)

| Property | KW | Flip | Δ | Flip pctile | Direction |
|:---------|---:|-----:|--:|------------:|:----------|
| **total_line_autocorr** | 4.568 | 4.004 | −0.564 | **2.0%** | worse (extreme low) |
| **kernel_boundaries** | 28 | 29 | +1 | **98.5%** | worse (extreme high) |
| upper_tri_trans_distinct | 28 | 29 | +1 | 96.0% | mild extreme |
| line_0_dominant_freq | 16 | 31 | +15 | 97.0% | changed |
| upper_first_larger | 10 → 11 | — | +1 | 99.5% | (redundant with asym) |
| line_0_autocorr_sum | 0.605 → 0.602 | — | −0.003 | 4.5% | (already extreme) |

### Key finding: **kernel_autocorr_1 relaxes**

| | KW | Flip | Pctile |
|---|---:|-----:|-------:|
| kernel_autocorr_1 | −0.464 | −0.321 | 0.0% → 9.0% |

The flip pushes kernel anti-autocorrelation from the absolute extreme (0th percentile) toward the bulk, though it remains fairly low (9th percentile). This is the clearest structural cost: **the improvement cone trades kernel sequential diversity for kernel distributional uniformity**.

### Key finding: **total_line_autocorr drops to extreme low**

KW's total line autocorrelation (sum of absolute autocorrelation across all 6 lines, lags 1–8) is 4.568 — a middling 20.5th percentile. The {10,17} flip drops it to 4.004 — the 2.0th percentile. The line patterns become unusually memoryless. This is driven by lines 2 and 3 (inner lines), whose autocorrelation drops by ~0.25 each.

### Unchanged (notable)

- Bridge Hamming distances: unchanged
- Bridge S-values: unchanged
- Pair symmetry counts: unchanged (all invariant)
- Weight distribution: unchanged
- Positional balance (yang): unchanged

---

## Experiment 2: bits {9,10,17} — All-Three-Improving

27 of 80 properties change. 7 reach significance.

### Additional costs beyond {10,17}

| Property | KW | {10,17} | {9,10,17} | Pctile |
|:---------|---:|--------:|----------:|-------:|
| total_fft_energy | 3168 | 3168 | **3200** | **98.5%** |
| line_4_fft_energy | 562 | 562 | **584** | **99.5%** |
| line_1_fft_energy | 530 | 530 | **544** | **97.5%** |
| line_4_fft_peak | 10.0 | 10.0 | **12.0** | **99.5%** |
| line_1_dominant_freq | 18 | 18 | **32** | **100.0%** |

Adding bit 9 (pair 9, Lin/Guan) introduces **FFT-domain costs** not present in {10,17} alone. The spectral energy of lines 1 and 4 (the palindrome-paired outer lines L2 and L5 in traditional numbering) increases to extreme levels. Total FFT energy reaches 98.5th percentile.

This is significant because **lines 1 and 4 are exactly the M-component lines** (L2 and L5). Bit 9 improves m-score by making more first-hexagrams have L2=yin — but this creates an extreme spectral signature in those same lines.

### kernel_autocorr_1 relaxation (same as {10,17})

kernel_autocorr_1: −0.464 → −0.328 (8.5th percentile). The cost is comparable.

---

## Experiment 3: bit 22 — Coupling-Only (Component 13,14)

38 of 80 properties change — the **most changes of any experiment**. 12 reach significance.

### This bit is NOT structurally invisible

Despite changing zero of the three standard metrics (χ², asym, m), bit 22 produces:

| Property | KW | Flip | Flip pctile |
|:---------|---:|-----:|------------:|
| **yang_balance** | 4 | **12** | **100.0%** |
| **pos_yang_imbalance** | 4 | **12** | **100.0%** |
| **first_hex_total_yang** | 98 | **102** | **100.0%** |
| **weight_ordering_bias** | 0 | **4** | **100.0%** |
| **n_first_heavier** | 2 | **4** | **100.0%** |
| **weight_autocorr_1** | 0.063 | **0.085** | **100.0%** |
| line_3_fft_energy | 520 | **512** | **1.0%** |
| line_0_fft_peak | 7.616 | **7.071** | **1.5%** |
| upper_tri_boundaries | 59 | 60 | 95.5% |
| lower_tri_trans_distinct | 28 | 29 | 98.0% |

**Six properties are pushed to the absolute extreme** (100th percentile) — more extreme than any of the 200 random orientations. This is remarkable for a bit that appeared neutral on our three metrics.

The pattern: flipping component (13,14) creates a **strong yang-balance asymmetry**. The first hexagram in each pair becomes systematically heavier (more yang lines) relative to the second. This is a per-pair **weight ordering** signal — distinct from the binary-value ordering that asymmetry measures, and distinct from the L2 value that m-score measures.

**This resolves the puzzle of why bit 22 modulates coupling despite metric-neutrality.** The coupling between χ² and asymmetry operates through the full orientation structure. Bit 22 changes the *weight balance* of the sequence, which alters how random orientations in its neighborhood distribute across the χ²–asymmetry space, without changing either metric for the specific KW orientation.

---

## Experiment 4: bit 13 — Keystone Control (Pair 15)

26 of 80 properties change. Only 2 reach significance.

| Property | KW | Flip | Flip pctile |
|:---------|---:|-----:|------------:|
| kernel_longest_run | 2 | **3** | **98.0%** |
| kernel_autocorr_1 | −0.464 | **−0.370** | **4.5%** |

The keystone flip has **few structural side effects** beyond the already-measured metric catastrophe. Its damage is concentrated in the kernel domain (χ² and kernel autocorrelation), not in trigram transitions, line patterns, or weight balance. The structural census confirms that bit 13's destruction is well-captured by the existing metrics — it is primarily a χ²-domain keystone, not a multi-domain keystone.

---

## Cross-Experiment Summary

### Properties changed vs unchanged

| Experiment | Changed | Significant | New extreme | Existing extremes relaxed |
|:-----------|--------:|------------:|------------:|-------------------------:|
| {10,17} | 23 | 6 | 3 (autocorr, boundaries, freq) | 1 (kernel_autocorr) |
| {9,10,17} | 27 | 7 | 5 (FFT energy/peak, freq) | 1 (kernel_autocorr) |
| bit 22 | **38** | **12** | **6** (yang balance family) | 1 (kernel_autocorr) |
| bit 13 | 26 | 2 | 1 (kernel_longest_run) | 0 |

### The structural costs of the improvement cone

Two distinct costs identified:

**Cost 1: Kernel sequential diversity (kernel_autocorr_1).** KW achieves −0.464 (0th percentile). The improvement cone relaxes this to −0.32 (9th percentile). This is the most robust finding — every experiment relaxes it, and KW's value is unprecedented in the random sample. **KW appears to optimize not just kernel uniformity but kernel sequential anti-repetition.** The improvement cone trades sequential diversity for distributional uniformity.

**Cost 2: Line autocorrelation collapse (total_line_autocorr).** {10,17} pushes total line autocorrelation to the 2nd percentile. The line patterns become unusually memoryless — each line's value at position n becomes nearly independent of position n−1. This is not obviously desirable; it may indicate loss of structural coherence between adjacent hexagrams at the individual-line level.

**Cost 3 (only for {9,10,17}): M-line spectral excess.** Adding bit 9 creates extreme FFT energy in lines 1 and 4 — exactly the M-component lines. This is a side effect of manipulating the M-decisive pairs.

### The hidden signal of bit 22

Bit 22 (component 13,14) is the most structurally impactful flip despite being metric-neutral. It creates unprecedented yang-balance asymmetry (first hexagram systematically heavier). This is a **fourth type of ordering signal** not captured by binary-value ordering (asymmetry) or L2-value ordering (m-score). It represents **weight ordering** — the relationship between the total yang content of paired hexagrams.

KW's bit 22 setting produces near-zero weight ordering bias (0.0), placing the sequence at the 47.5th percentile — dead center. Flipping it creates extreme bias (100th percentile). KW's choice preserves weight-ordering neutrality.

---

## What Explains KW's Refusal of the Improvement Cone?

The strongest candidate: **kernel sequential anti-repetition (kernel_autocorr_1)**. 

KW achieves a value more extreme than any random orientation in a 200-sample pool — a property invisible to the χ² metric. The improvement cone weakens it. If KW optimizes a combined objective that includes both kernel distributional uniformity *and* kernel sequential diversity, then the cone's χ² improvement comes at the cost of this sequential objective.

The total_line_autocorr finding adds a secondary cost but is less compelling — KW is not extreme on this property, so pushing it to 2nd percentile might not reflect a deliberate KW optimization.

The FFT costs of {9,10,17} are concentrated in the M-component lines and are a predictable side effect, not a deep structural cost.

**Bottom line:** The cone is not free. It buys χ² improvement at the price of kernel sequential diversity. Whether this trade matters depends on whether the sequencing of kernels (not just their distribution) carries structural significance.

---

## Data Files

- `round3_data.json` — full census data (KW properties, calibration statistics, 4 experiment results)
- `structural_census.py` — computation script (80 properties, 200-sample calibration)
