# Round 2: Composite Generators — Results

## KW Reference Profile

| Metric | KW Value | Direction |
|--------|----------|-----------|
| Kernel χ² | 2.290 | Lower = better |
| Canon asymmetry | +3 | Higher = better |
| M-score | 12/16 | Higher = better |
| Kernel autocorrelation | −0.464 | More negative = better |

---

## R2-A: Face-Flow Composite (M-rule + kernel-repeat override)

Start from M-rule (C1), override at positions where bridge kernel Hamming distance to previous is below threshold.

| Variant | Threshold | Overrides | χ² | asym | m | kac | Ham | Pareto |
|---------|-----------|-----------|-----|------|---|------|-----|--------|
| R2-A1 | exact repeat (h<1) | 6/32 | 4.355 | 0 | 13 | +0.049 | 9 | trade-off |
| R2-A2 | h<2 | 7/32 | 7.452 | −3 | 12 | −0.457 | 14 | dominated-by-kw |
| R2-A3 | h<3 | 5/32 | 4.355 | −1 | 15 | −0.294 | 10 | trade-off |

**R2-A2** is dominated by KW on all 4 axes — the strongest kernel-repeat threshold (h<2) overrides too aggressively and produces an orientation worse than KW everywhere.

**R2-A1** gains m=13 (better) but kac collapses to +0.049 (positive — worse than random).

**R2-A3** has the fewest overrides (5) and achieves m=15 but kac=−0.294 (still much worse than KW).

**Conclusion:** Face-flow composites fail because starting from the M-rule puts the orientation in a region of space where the kernel chain is already disrupted. Overriding a few positions cannot recover sequential diversity.

---

## R2-C: Balanced Kernel Walk

Sequential processing with composite score: `score = w_seq × hamming_from_prev + w_dist × kernel_deficit`.

| Weights (seq, dist) | Label | χ² | asym | m | kac | Ham | Pareto |
|---------------------|-------|-----|------|---|------|-----|--------|
| (1.0, 0.0) | pure sequential | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |
| (0.7, 0.3) | seq-heavy | 7.452 | −2 | 11 | −0.653 | 15 | trade-off |
| (0.5, 0.5) | equal | 7.452 | −2 | 12 | −0.485 | 13 | trade-off |
| (0.3, 0.7) | dist-heavy | **2.290** | −3 | 10 | −0.462 | 12 | dominated-by-kw |
| (0.0, 1.0) | pure distributional | 3.323 | **+3** | 11 | −0.371 | 8 | dominated-by-kw |

**R2-C (dist-heavy, 0.3/0.7)** hits KW's exact χ²=2.290 and near-exact kac=−0.462 (vs KW's −0.464). But it collapses asym to −3 (vs +3) and m to 10 (vs 12). Dominated by KW.

**R2-C (pure distributional)** matches KW's asym=+3 exactly but loses on all other axes.

**R2-C (equal, 0.5/0.5)** achieves kac=−0.485 (slightly better than KW) but at χ²=7.452 cost.

**Observation:** As the distributional weight increases from 0→1, χ² improves (8.5→3.3) while kac degrades (−0.67→−0.37). The transition is smooth. KW's operating point (χ²=2.3, kac=−0.46) falls at roughly w_dist≈0.7, but asymmetry and m-score collapse at that weight.

**Kernel distributions:**

| Variant | id | O | M | I | OM | OI | MI | OMI |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| KW | 4 | 4 | 5 | 3 | 4 | 3 | 4 | 4 |
| pure seq | 6 | 7 | 3 | 2 | 3 | 1 | 6 | 3 |
| dist-heavy | 5 | 5 | 5 | 3 | 2 | 3 | 4 | 4 |
| pure dist | 5 | 5 | 5 | 2 | 4 | 2 | 5 | 3 |

KW's kernel distribution (range 3–5, max deviation from expected 3.875) is notably more uniform than either endpoint.

---

## R2-D: Asymmetry-Aware Sequential Diversity

C2 (sequential diversity) with asymmetry-aware tie-breaking: prefer binary-high-first in upper canon; three variants for lower canon preference.

| Variant | Lower pref | χ² | asym | m | kac | Ham | Pareto |
|---------|-----------|-----|------|---|------|-----|--------|
| upper-high/lower-low | low | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |
| upper-high/lower-neutral | none | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |
| upper-high/lower-high | high | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |

**All three variants produce identical orientations.** The asymmetry tie-breaking is never reached — the primary criterion (Hamming distance from previous kernel) and secondary criterion (least-seen kernel count) always resolve ties before the tertiary (asymmetry preference) fires.

**Implication:** In C2's sequential diversity framework, orientation choices are fully determined by kernel-chain properties. There is no room for asymmetry preferences to enter as tie-breaks. To inject asymmetry, it would need to be a competing primary criterion, not a subordinate one.

---

## R2-E: Multi-Objective Greedy Scalarization

Greedy hill-climb on weighted sum of normalized axes. 50 starts per weight vector, 10 weight vectors.

| Weights (χ², asym, m, kac) | χ² | asym | m | kac | Ham | Pareto |
|----------------------------|-----|------|---|------|-----|--------|
| (0.25, 0.25, 0.25, 0.25) | 0.226 | +7 | 7 | +0.175 | 16 | trade-off |
| (0.50, 0.00, 0.00, 0.50) | 1.258 | 0 | 12 | +0.568 | 17 | trade-off |
| (0.00, 0.50, 0.50, 0.00) | 11.581 | +10 | 8 | −0.231 | 11 | trade-off |
| (0.40, 0.10, 0.10, 0.40) | 0.742 | +3 | 9 | +0.525 | 12 | trade-off |
| (0.10, 0.40, 0.40, 0.10) | 1.774 | +9 | 9 | −0.057 | 8 | trade-off |
| (0.27, 0.02, 0.04, 0.68) | 1.258 | +1 | 11 | +0.568 | 16 | trade-off |
| (0.35, 0.53, 0.07, 0.05) | 1.258 | +9 | 8 | −0.262 | 8 | trade-off |
| (0.14, 0.29, 0.26, 0.31) | 2.290 | +9 | 7 | +0.111 | 14 | trade-off |
| (0.43, 0.25, 0.15, 0.18) | 0.226 | +7 | 7 | +0.175 | 16 | trade-off |
| (0.50, 0.09, 0.13, 0.29) | 0.226 | +5 | 8 | +0.232 | 16 | trade-off |

**Zero Pareto dominance of KW.** All 10 weight vectors produce trade-offs.

**Critical finding: kac is always positive (or weakly negative) in optimized orientations.** Even weights (0.50, 0.00, 0.00, 0.50) — putting half the weight on kac itself — produce kac=+0.568. The greedy optimizer, when it improves χ² and kac jointly, ends up in a region where kac is destroyed.

**Why:** The scalarized objective normalizes kac by dividing by KW_KAC (−0.464). Since KW_KAC is negative, minimizing `val/KW_KAC` means *maximizing* val (making it more positive). The normalization inverts the kac direction.

**R2-E w=(0.40,0.10,0.10,0.40)** achieves χ²=0.742, asym=+3 (matching KW), m=9 — but kac=+0.525. The χ²-asym achievement comes at total kac collapse.

**R2-E w=(0.14,0.29,0.26,0.31)** achieves χ²=2.290 (matching KW), asym=+9, m=7, kac=+0.111.

---

## Summary Table: All Round 2 Generators vs KW

| Generator | χ² | asym | m | kac | Ham | Pareto |
|-----------|-----|------|---|------|-----|--------|
| **KW** | **2.290** | **+3** | **12** | **−0.464** | **0** | reference |
| R2-A1 (M+override h<1) | 4.355 | 0 | 13 | +0.049 | 9 | trade-off |
| R2-A2 (M+override h<2) | 7.452 | −3 | 12 | −0.457 | 14 | dominated |
| R2-A3 (M+override h<3) | 4.355 | −1 | 15 | −0.294 | 10 | trade-off |
| R2-C (1.0/0.0) seq | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |
| R2-C (0.7/0.3) | 7.452 | −2 | 11 | −0.653 | 15 | trade-off |
| R2-C (0.5/0.5) | 7.452 | −2 | 12 | −0.485 | 13 | trade-off |
| R2-C (0.3/0.7) | 2.290 | −3 | 10 | −0.462 | 12 | dominated |
| R2-C (0.0/1.0) dist | 3.323 | +3 | 11 | −0.371 | 8 | dominated |
| R2-D (all 3 variants) | 8.484 | −2 | 12 | −0.666 | 13 | trade-off |
| R2-E (equal) | 0.226 | +7 | 7 | +0.175 | 16 | trade-off |
| R2-E (chi²+kac) | 1.258 | 0 | 12 | +0.568 | 17 | trade-off |
| R2-E (asym+m) | 11.581 | +10 | 8 | −0.231 | 11 | trade-off |
| R2-E (chi²+kac heavy) | 0.742 | +3 | 9 | +0.525 | 12 | trade-off |
| R2-E (asym+m heavy) | 1.774 | +9 | 9 | −0.057 | 8 | trade-off |

---

## Key Findings

1. **Zero generators dominate KW.** 21 distinct candidates tested; 3 dominated by KW, 18 trade-offs, 0 dominate.

2. **R2-D is vacuous.** Asymmetry tie-breaking never fires in sequential diversity framework. C2's kernel-chain choices fully determine orientation with no room for soft preferences.

3. **R2-C maps the χ²-kac trade-off.** As distributional weight increases, χ² improves and kac degrades monotonically. KW's operating point falls at w_dist≈0.7 for the kernel metrics, but asymmetry and m-score require a mechanism outside the kernel-chain framework.

4. **R2-E reveals the normalization bug.** The kac normalization (dividing by negative KW_KAC) inverts the optimization direction. All R2-E results have positive kac — they're optimizing kac in the wrong direction. This needs fixing for Round 3.

5. **Face-flow hybrid (R2-A) fails at the root.** Starting from M-rule orientation puts you in a kernel-chain-hostile region. Patching with overrides can't recover; the starting point determines the trajectory.

6. **The persistent gap.** Achieving both χ²≈2.3 AND kac≈−0.46 AND asym=+3 AND m=12 remains impossible for all tested principles. The closest approaches hit 2-3 axes and miss the others.
