# Round 3: Is OMI Dominance the Whole Story? — Results

## Summary: OMI dominance is mostly f1 by another name, but subgroup bias and front-loading are NOT.

### 1. OMI dominance conditioned on f1

| Metric | Value |
|--------|-------|
| Pearson r(f1, OMI count) | **0.651** |
| KW OMI=8 unconditional percentile | 99.2% |
| KW OMI=8 conditional on f1≥1.70 | **93.6%** |
| Mean OMI at f1∈[1.7,1.8) | 5.57 ± 1.52 |

**f1 and OMI count are strongly correlated (r=0.65).** This is expected — OMI deltas contribute 3.0 to the distance sum, while the mean over all deltas is ~1.5, so OMI deltas are the primary driver of high f1.

Conditioned on f1≥1.70, KW's OMI count of 8 drops from the 99th to the **93.6th percentile**. Still elevated but far less extreme — much of the OMI signal was carried by f1. The conditional OMI distribution shows KW is about 1.3σ above the conditional mean (8 vs 5.94 ± 1.67).

Conversely, conditioned on OMI≥8, KW's f1 is at the **55.7th percentile** — completely unremarkable. Once you fix the OMI count, f1 carries no additional information.

**Verdict: OMI count and f1 are near-equivalent signals. OMI count is the *mechanism* of high f1, not an independent constraint. f1 is a summary of OMI dominance.**

### 2. Subgroup bias IS an independent signal

| Metric | KW | Null mean ± std | Percentile |
|--------|-----|-----------------|-----------|
| {id,O,MI,OMI} residence (random start) | 0.645 | 0.500 ± 0.088 | **97.2%** |
| {id,O,MI,OMI} residence (fixed start M) | 0.645 | 0.484 ± 0.089 | **98.1%** |

The null here uses the **same delta distribution** as KW but in random order. The subgroup bias (64.5% residence in {id,O,MI,OMI}) is NOT mechanically entailed by the delta distribution. Even with the same delta counts, random orderings produce ~50% residence. KW's ordering of deltas specifically keeps the running product inside this subgroup.

This is a genuine independent structural property — the **order** of deltas matters, not just their counts.

### 3. OMI spacing: front-loaded

| Spacing metric | KW | Null mean ± std | Percentile |
|----------------|-----|-----------------|-----------|
| First-half OMI count (of 8 total) | 6 | 4.00 ± 1.22 | **98.3%** |
| Gap variance | 7.96 | 6.50 ± 4.55 | 72.5% |
| Max gap | 8 | 8.07 ± 2.42 | 62.7% |
| Min gap | 1 | 1.09 ± 0.29 | 91.6% |

**The OMI deltas are concentrated in the first half of the sequence** (6 of 8, at the 98.3rd percentile). Positions [4, 6, 8, 10, 11, 13] form a dense cluster in positions 4-13 (pairs 9-28 in KW numbers), with only 2 OMIs in the second half (at positions 21 and 29).

Gap pattern: [2, 2, 2, 1, 2, 8, 8] — extremely regular in the cluster (gaps of 2), then two large gaps. This is front-loading, not uniform spacing.

The OMI transitions connect specific pair ranges: the dense cluster bridges pairs 9-32 (KW hexagrams 17-64's first third), and the two isolated OMIs are at pairs 22-23 (hex 43-48) and the final pair 30-31 (hex 61-64).

### 4. Delta autocorrelation: unremarkable

All delta sequence autocorrelation measures are within normal range:
- Lag-1 component correlations: O=0.03, M=-0.17, I=0.03 (mean -0.04)
- Lag-1 Hamming: KW=1.448 (41.8th percentile)
- Number of runs: KW=27 (72.2nd percentile)
- Max run: 2 (66.9th percentile)
- Delta-delta MI (corrected): 0.531 bits (not tested against null, but the raw value with 26 nonzero cells in the transition matrix is heavily biased)

No significant sequential structure in the deltas beyond what's captured by the distribution and the subgroup bias.

### 5. Global path properties

| Property | Value |
|----------|-------|
| Total delta product (δ₁⊕...⊕δ₃₀) | I = (0,0,1) |
| = k₁ ⊕ k₃₁ | M ⊕ MI = I ✓ |
| First-half delta product | O |
| Second-half delta product | OI |
| Total kernel product (k₁⊕...⊕k₃₁) | M |
| First-half kernel product (k₁..k₁₆) | OM |
| Second-half kernel product (k₁₇..k₃₁) | O |

**Reversal symmetry confirmed**: reversing the pair sequence produces exactly the reversed kernel sequence and the same delta distribution. The delta sequence reversed equals the delta sequence of the reversed pair ordering. This is a structural identity of the bridge construction, not a property of KW specifically.

Half-sequence kernel products: OM and O. Their XOR is M (the total product). No obvious symmetry between halves — they're distinct elements.

### 6. Joint constraint tightness

| Constraint set | Fraction of 1M trials |
|---------------|----------------------|
| f1 ≥ 1.70 | 11.54% |
| OMI ≥ 8 | 2.57% |
| Repeats ≤ 2 | 24.57% |
| Types = 8 | 87.08% |
| f1 ∧ OMI | 1.96% |
| f1 ∧ OMI ∧ Rep | 0.94% |
| **All four** | **0.85%** |
| f1≥1.75 ∧ OMI≥8 ∧ Rep≤2 ∧ Types=8 | 0.76% |
| f1∈[1.75,1.80] ∧ all | 0.20% |

**The known constraints jointly eliminate ~99.2% of the random search space.** About 1 in 500 random orderings satisfies all four constraints at KW's exact levels. This is significant but not extreme — roughly comparable to the OMI dominance signal alone (99.2nd percentile).

The f1 and OMI constraints are highly redundant (f1∧OMI = 1.96% vs f1 alone = 11.5%, OMI alone = 2.57%). The "repeats ≤ 2" constraint adds genuine independent filtering (from 1.96% to 0.94%).

## What the three rounds establish

1. **f1 is the primary metric**, and OMI dominance is its mechanism (r=0.65). These are one signal, not two.

2. **The transition "grammar" (MI) is an artifact** of small-sample bias + f1-correlated elevation. No independent sequential structure at the kernel level.

3. **Two genuinely independent signals remain after deflation:**
   - **Subgroup bias**: running product spends 64.5% in {id,O,MI,OMI} (97-98th percentile even controlling for delta distribution). This is about the *ordering* of transitions, not their counts.
   - **OMI front-loading**: 6/8 OMI deltas in the first half (98.3rd percentile). The maximum-change transitions are concentrated early in the sequence.

4. **Joint constraint tightness**: All known properties together eliminate ~99.2% of random space. About 1 in 120 random orderings matches KW on all measured criteria. Non-trivial but not remotely unique — a large ensemble of orderings shares these properties.
