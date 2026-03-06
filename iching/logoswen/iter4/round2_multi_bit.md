# Round 2: Multi-Bit Interactions — Gradient to Curvature

## Setup

Round 1 established single-bit deltas (gradient). Round 2 probes 2- and 3-bit flips to measure interaction terms (curvature). The key question: is the landscape additive, or do multi-bit interactions change the picture?

KW baseline: **χ² = 2.290**, **asym = +3**, **m = 12/16**, **coupling = 1.906**.

**Interaction term** = actual − expected_additive (where expected_additive = KW + Σ single-bit deltas).

---

## Table 1: Critical Joint Flips

| Experiment | Bits | Pairs | Metric | Actual | Expected | Interaction |
|:-----------|:-----|:------|:-------|-------:|---------:|------------:|
| **1. Improvement cone** | 10+17 | 10,21 | χ² | **0.742** | 0.742 | **0.000** |
| | | | asym | **5** | 5 | **0** |
| | | | m | **12** | 12 | **0** |
| | | | coupling | **1.678** | — | Δ=−0.228 |
| **2. Catastrophic pair** | 13+23 | 15,19+20 | χ² | **12.613** | 10.548 | **+2.065** |
| | | | asym | **2** | 2 | **0** |
| | | | m | **11** | 11 | **0** |
| | | | coupling | **0.121** | — | Δ=−1.785 |
| **3a. Subset** | 9+17 | 9,21 | χ² | **0.742** | 0.742 | **0.000** |
| | | | asym | **3** | 3 | **0** |
| | | | m | **13** | 13 | **0** |
| **3b. Triple** | 9+10+17 | 9,10,21 | χ² | **0.742** | 0.226 | **+0.516** |
| | | | asym | **4** | 4 | **0** |
| | | | m | **13** | 13 | **0** |
| | | | coupling | **1.699** | — | Δ=−0.208 |

### Key findings

**1. Improvement cone is perfectly additive at 2-bit level.** Bits 10+17 produce exactly the sum of their individual effects: χ² drops from 2.290 to 0.742, asymmetry rises to 5. Zero interaction on all three metrics. The improvement is real and cooperative.

**2. Catastrophe is super-additive.** Bits 13+23 produce χ² = 12.613, which is **+2.065 worse than the additive prediction** (10.548). The two catastrophic bits reinforce each other — the destruction is synergistic. Coupling collapses to 0.121 (essentially zero — 93.7% below baseline).

**3. All-three-improving perturbation found.** Bits {9, 10, 17} produce **χ² = 0.742 (↓1.548), asym = 4 (↑1), m = 13 (↑1)**. All three metrics improve simultaneously. This is the first all-improving perturbation in the entire investigation.

**3a. But there's a χ² floor.** The 3-bit flip {9,10,17} gets χ² = 0.742, which equals the 2-bit flip {10,17}. Adding bit 9 should have reduced χ² further to 0.226, but the interaction term is +0.516 — bit 9's χ² improvement is cancelled when combined with bits 10+17. The landscape is additive at 2-bits but develops curvature at 3-bits. χ² = 0.742 appears to be a floor.

**3b. The {9,17} pair is also perfectly additive:** χ² = 0.742, asym = 3, m = 13 — exactly as predicted. The curvature only appears in the 3-way combination {9,10,17}.

---

## Table 2: Improvement Cone Neighborhood (2-bit combos with bits 10, 17)

50 combos tested (25 with anchor=10, 25 with anchor=17). Zero S=2 violations.

### Pure improvement combos (≥1 improve, 0 degrade): **15 of 50**

| Bits | Pairs | Δχ² | Δasym | Δm | Int χ² |
|:-----|:------|----:|------:|---:|-------:|
| 3,10 | 3,10 | −0.516 | 0 | +1 | 0.000 |
| 4,10 | 4,10 | −0.516 | 0 | 0 | 0.000 |
| 5,10 | 5,10 | −0.516 | 0 | +1 | 0.000 |
| 9,10 | 9,10 | −0.516 | 0 | +1 | +0.516 |
| 10,15 | 10,17 | −1.548 | 0 | 0 | 0.000 |
| 10,26 | 10,29+30 | −1.548 | 0 | 0 | 0.000 |
| 0,17 | 0,21 | −0.516 | 0 | 0 | −0.516 |
| 2,17 | 2,21 | −0.516 | 0 | 0 | 0.000 |
| 3,17 | 3,21 | −1.032 | 0 | +1 | 0.000 |
| 4,17 | 4,21 | −1.032 | 0 | 0 | 0.000 |
| 5,17 | 5,21 | −1.032 | 0 | +1 | 0.000 |
| 9,17 | 9,21 | −1.548 | 0 | +1 | 0.000 |
| 11,17 | 11,21 | +0.000 | +2 | 0 | −1.032 |
| 15,17 | 17,21 | −1.032 | 0 | 0 | +1.032 |
| 17,22 | 21,13+14 | −1.032 | +1 | 0 | 0.000 |

### All-three-improving combos: **0**

No 2-bit combo improves all three metrics simultaneously. The asymmetry-improving bits (6, 11, 12, 20, 21) that pair with 10 or 17 all degrade either χ² or m.

### Interaction term statistics (experiment 4)

- **|int_χ²|**: mean 0.382, max 2.065
- **|int_asym|**: mean 0.00, **always exactly zero**
- **|int_m|**: mean 0.00, **always exactly zero**

**Asymmetry and M-score are perfectly additive in all 50 tested 2-bit combos.** The only metric with nonzero interaction terms is χ². This is a structural finding — asym and m each depend on independent per-pair properties that don't interact, while χ² depends on bridge kernels that are shared between adjacent pairs.

### Cone widening

Bit 17 (pair 21) generates a much wider improvement cone than bit 10 (pair 10):
- **Bit 10 anchor**: 6 pure-improvement partners (bits 3,4,5,9,15,26)
- **Bit 17 anchor**: 9 pure-improvement partners (bits 0,2,3,4,5,9,11,15,22)

The improvement cone is wider around bit 17. Several partners (3,4,5,9,15) appear with both anchors.

---

## Table 3: Random Hessian (50 random 2-bit combos, excluding bits 10,17)

50 pairs sampled from the 25 non-cone bits. Zero S=2 violations.

### Interaction term distribution

**χ² interaction terms:**
- 52% of combos have exactly zero interaction (perfectly additive)
- Mean |int_χ²| = 0.490
- Values observed: {−2.065, −1.548, −1.032, −0.516, 0.000, +0.516, +1.032} — all multiples of 0.516

**Asymmetry and M-score: always exactly zero interaction.** Confirmed across all 50 random combos — these metrics are strictly additive in 2-bit space.

### Nonlinearity coefficient (|interaction| / |Σ individual deltas|) for χ²

| Statistic | Value |
|:----------|------:|
| Mean | 0.406 |
| Median | 0.254 |
| Std | 0.535 |
| Min | 0.000 |
| Max | 2.000 |
| Fraction < 0.1 (near-additive) | 43.5% |
| Fraction > 0.5 (strongly epistatic) | 30.4% |

**Interpretation:** χ² interactions are a mix. ~44% of random 2-bit combos are near-additive (|nl| < 0.1), but ~30% show strong epistasis (|nl| > 0.5). The landscape is **neither purely additive nor strongly epistatic** — it's intermediate, with interaction strength depending on which specific bits are combined.

Notable: nonlinearity coefficient can exceed 1.0 (interaction larger than the sum of individual effects). Several combos show nl = 2.0, meaning the interaction fully doubles the individual sum. These are pairs where the individual effects partially cancel but the interaction reverses the cancellation.

---

## Table 4: Nonlinearity Summary (all 100 valid 2-bit combos)

| Metric | Mean int. | Mean |int.| | Max |int.| | Fraction zero | Additive? |
|:-------|----------:|----------:|----------:|--------------:|:----------|
| χ² | −0.036 | 0.490 | 2.065 | 52.0% | **Partially** |
| Asymmetry | 0.00 | 0.00 | 0 | 100.0% | **Perfectly** |
| M-score | 0.00 | 0.00 | 0 | 100.0% | **Perfectly** |

### Why χ² has interactions but asym and m don't

**Asymmetry** depends on binary ordering within each pair independently. Flipping pair k changes the ordering of pair k only. Two flips at different pairs can't interact because they affect disjoint pairs.

**M-score** depends on which hexagram is first in each M-decisive pair. Same argument — per-pair property, no cross-pair interaction.

**χ²** depends on bridge kernels, and bridge k depends on the exit hex of pair k and entry hex of pair k+1. One might expect only adjacent pairs to interact. But the data refutes this: of the 48 nonzero χ² interactions in the 100 combos, **only 3 involve adjacent pairs** (distance 1). The remaining 45 have pair distances ranging from 2 to 29. The interactions are **long-range** — changing the orientation of pair 0 can alter the χ² interaction with pair 29.

This means χ² interactions are not mediated by shared bridges. Instead they arise from the global uniformity constraint: each pair flip changes which kernel appears at 1–2 bridges, and two distant flips can reinforce or cancel in how they perturb the 8-category histogram. The interaction is through the **global count vector**, not through local bridge adjacency.

---

## Structural Notes

1. **The improvement cone is real.** Bits 10+17 produce χ² = 0.742 (vs KW's 2.290), asym = 5 (vs 3), m = 12 (unchanged). This is a 67.6% reduction in χ² and a 67% increase in asymmetry. The improvement is perfectly additive at the 2-bit level.

2. **All-three-improving exists at 3 bits: {9, 10, 17}.** χ² improves by 1.548, asym improves by 1, m improves by 1. However, the χ² improvement is capped at 0.742 (not the additive prediction of 0.226) — there's a +0.516 interaction at the 3-bit level.

3. **Coupling modestly weakens in the improvement direction.** Bits 10+17 drop coupling from 1.906 to 1.678 (Δ = −0.228). Bits 9+10+17 drop it to 1.699 (Δ = −0.208). The coupling reduction is real but modest — coupling survives the improvement.

4. **Catastrophic destruction is super-additive.** Bits 13+23 push χ² to 12.613 (5.5× KW), which is worse than the additive prediction by one full step (+2.065). Coupling collapses to 0.121 — complete destruction. The catastrophic bits are not independent; they amplify each other.

5. **χ² = 0.742 is likely a landscape floor.** Three different combinations ({10,17}, {9,17}, {9,10,17}) all produce χ² = 0.742 despite different additive predictions. This suggests 0.742 is the minimum achievable χ² in the few-bit neighborhood around KW.

6. **The landscape has a strict structural hierarchy:** Asym and m are always additive (no interactions), χ² sometimes has interactions (mediated by adjacent-pair bridges). This means the single-bit gradient is perfectly reliable for asym and m, but only approximately reliable for χ².

---

## Data Files

- `round2_data.json` — complete raw data (6 experiments, 100 2-bit combos)
- `multi_bit_fragility.py` — computation script (reproducible)
