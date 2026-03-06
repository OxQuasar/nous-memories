# Round 1: Single-Bit Perturbation Baseline

## Setup

27 free orientation bits, indexed 0–26:
- **Bits 0–21** (Type A): 22 unconstrained pairs — pair indices {0,1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,18,21,22,23,24,31}
- **Bits 22–26** (Type B): 5 constraint components — {(13,14), (19,20), (25,26), (27,28), (29,30)}

All components are equality-constrained (o_k = o_{k+1}) except component (29,30) which is constrained to {(0,0), (1,0)}.

KW baseline (all zeros orientation): **χ² = 2.290**, **asym = +3**, **m_score = 12/16**.

"Improve" means: χ² decreases (more uniform), asym increases (stronger upper-canon bias), m_score increases (more L2=yin preference).

---

## Table 1: Single-Bit Metric Profiles

| bit | pair(s) | type | χ² | Δχ² | asym | Δasym | m_sc | Δm | #imp | #deg |
|----:|--------:|:----:|-------:|--------:|-----:|------:|-----:|---:|-----:|-----:|
| 0 | 0 | A | 3.323 | +1.032 | 2 | -1 | 12 | 0 | 0 | 2 |
| 1 | 1 | A | 4.871 | +2.581 | 2 | -1 | 11 | -1 | 0 | 3 |
| 2 | 2 | A | 2.806 | +0.516 | 2 | -1 | 12 | 0 | 0 | 2 |
| 3 | 3 | A | 2.290 | 0.000 | 2 | -1 | 13 | +1 | 1 | 1 |
| 4 | 4 | A | 2.290 | 0.000 | 2 | -1 | 12 | 0 | 0 | 1 |
| 5 | 5 | A | 2.290 | 0.000 | 2 | -1 | 13 | +1 | 1 | 1 |
| 6 | 6 | A | 2.806 | +0.516 | 4 | +1 | 11 | -1 | 1 | 2 |
| 7 | 7 | A | 4.871 | +2.581 | 2 | -1 | 12 | 0 | 0 | 2 |
| 8 | 8 | A | 2.806 | +0.516 | 2 | -1 | 11 | -1 | 0 | 3 |
| 9 | 9 | A | 1.774 | -0.516 | 2 | -1 | 13 | +1 | 2 | 1 |
| 10 | 10 | A | 1.774 | -0.516 | 4 | +1 | 12 | 0 | 2 | 0 |
| 11 | 11 | A | 4.355 | +2.065 | 4 | +1 | 12 | 0 | 1 | 1 |
| 12 | 12 | A | 4.355 | +2.065 | 4 | +1 | 11 | -1 | 1 | 2 |
| 13 | 15 | A | 6.419 | +4.129 | 2 | -1 | 11 | -1 | 0 | 3 |
| 14 | 16 | A | 1.774 | -0.516 | 2 | -1 | 11 | -1 | 1 | 2 |
| 15 | 17 | A | 1.258 | -1.032 | 2 | -1 | 12 | 0 | 1 | 1 |
| 16 | 18 | A | 4.355 | +2.065 | 2 | -1 | 11 | -1 | 0 | 3 |
| 17 | 21 | A | 1.258 | -1.032 | 4 | +1 | 12 | 0 | 2 | 0 |
| 18 | 22 | A | 2.290 | 0.000 | 2 | -1 | 11 | -1 | 0 | 2 |
| 19 | 23 | A | 3.839 | +1.548 | 2 | -1 | 12 | 0 | 0 | 2 |
| 20 | 24 | A | 2.806 | +0.516 | 4 | +1 | 11 | -1 | 1 | 2 |
| 21 | 31 | A | 3.839 | +1.548 | 4 | +1 | 11 | -1 | 1 | 2 |
| 22 | 13,14 | B | 2.290 | 0.000 | 3 | 0 | 12 | 0 | 0 | 0 |
| 23 | 19,20 | B | 6.419 | +4.129 | 3 | 0 | 12 | 0 | 0 | 1 |
| 24 | 25,26 | B | 1.774 | -0.516 | 3 | 0 | 11 | -1 | 1 | 1 |
| 25 | 27,28 | B | 3.839 | +1.548 | 3 | 0 | 12 | 0 | 0 | 1 |
| 26 | 29,30 | B | 1.258 | -1.032 | 2 | -1 | 12 | 0 | 1 | 1 |

### Key observations (factual only)

**χ² sensitivity:**
- 3 bits leave χ² unchanged: bits 3 (pair 3), 4 (pair 4), 5 (pair 5) — all Δχ² = 0.000.
- 2 additional zeros: bit 18 (pair 22), bit 22 (component 13,14).
- Worst degradation: bits 13 (pair 15) and 23 (component 19,20) — both Δχ² = +4.129.
- Best improvement: bits 15 (pair 17) and 17 (pair 21) — both Δχ² = -1.032. Also bit 26 (component 29,30) = -1.032.
- Quantized: Δχ² values are multiples of ±0.516 (= 1/expected = 8/31 squared/scaled).

**Asymmetry sensitivity:**
- 5 constraint components (bits 22–25) leave asymmetry unchanged (Δasym = 0), except bit 26 (component 29,30, Δasym = -1).
- Among unconstrained pairs: 7 improve asym (+1), 15 degrade (-1). None neutral.
- The 7 asym-improving flips are pairs: 6, 10, 11, 12, 21, 24, 31.

**M-score sensitivity:**
- 13 flips leave m_score unchanged (Δm = 0). These are the non-M-decisive pairs plus some constraint components.
- 3 flips improve m_score (+1): bits 3, 5, 9 (pairs 3, 5, 9).
- 11 flips degrade m_score (-1). The M-score is asymmetrically fragile: 11 ways to break it vs 3 ways to improve it.

**No flip improves all 3 metrics simultaneously.** Only 2 flips improve ≥1 metric with 0 degradation:
- **Bit 10 (pair 10)**: χ² improves (-0.516), asym improves (+1), m neutral. Pure improvement on 2/3.
- **Bit 17 (pair 21)**: χ² improves (-1.032), asym improves (+1), m neutral. Pure improvement on 2/3.

---

## Table 2: Conditional Coupling Estimates

Baseline coupling ratio (unconditional 20K): **1.906** (P(χ²≤KW)=0.0612, P(asym≥KW)=0.0462, P(joint)=0.00540).

| bit | P(χ²≤KW) | P(as≥KW) | P(joint) | ratio | Δratio |
|----:|----------:|---------:|---------:|------:|-------:|
| 0 | 0.0646 | 0.0268 | 0.00400 | 2.304 | +0.398 |
| 1 | 0.0418 | 0.0278 | 0.00190 | 1.635 | -0.271 |
| 2 | 0.0443 | 0.0278 | 0.00175 | 1.424 | -0.483 |
| 3 | 0.0723 | 0.0261 | 0.00360 | 1.908 | +0.002 |
| 4 | 0.0707 | 0.0238 | 0.00400 | 2.379 | +0.473 |
| 5 | 0.0485 | 0.0264 | 0.00325 | 2.538 | +0.632 |
| 6 | 0.0805 | 0.0679 | 0.00640 | 1.169 | -0.737 |
| 7 | 0.0621 | 0.0263 | 0.00245 | 1.498 | -0.408 |
| 8 | 0.0514 | 0.0245 | 0.00285 | 2.259 | +0.352 |
| 9 | 0.0614 | 0.0260 | 0.00315 | 1.977 | +0.071 |
| 10 | 0.0733 | 0.0666 | 0.00840 | 1.720 | -0.187 |
| 11 | 0.0585 | 0.0699 | 0.00795 | 1.941 | +0.035 |
| 12 | 0.0529 | 0.0669 | 0.00590 | 1.668 | -0.238 |
| 13 | 0.0309 | 0.0259 | 0.00065 | 0.814 | -1.092 |
| 14 | 0.0544 | 0.0268 | 0.00205 | 1.407 | -0.499 |
| 15 | 0.0541 | 0.0255 | 0.00290 | 2.108 | +0.202 |
| 16 | 0.0458 | 0.0267 | 0.00245 | 2.000 | +0.094 |
| 17 | 0.0649 | 0.0680 | 0.00795 | 1.803 | -0.103 |
| 18 | 0.0706 | 0.0265 | 0.00265 | 1.419 | -0.487 |
| 19 | 0.0747 | 0.0261 | 0.00250 | 1.285 | -0.622 |
| 20 | 0.0714 | 0.0643 | 0.00650 | 1.417 | -0.489 |
| 21 | 0.0546 | 0.0678 | 0.00635 | 1.718 | -0.188 |
| 22 | 0.0535 | 0.0479 | 0.00335 | 1.306 | -0.600 |
| 23 | 0.0357 | 0.0483 | 0.00195 | 1.134 | -0.773 |
| 24 | 0.0643 | 0.0459 | 0.00580 | 1.965 | +0.059 |
| 25 | 0.0516 | 0.0510 | 0.00385 | 1.463 | -0.443 |
| 26 | 0.0660 | 0.0267 | 0.00335 | 1.900 | -0.007 |

### Key observations (factual only)

**Coupling-increasing flips** (Δratio > +0.3): bits 0, 4, 5, 8 (pairs 0, 4, 5, 8).
- Bit 5 (pair 5) has the strongest increase: ratio = 2.538, Δ = +0.632.

**Coupling-destroying flips** (Δratio < -0.5): bits 2, 6, 13, 19, 22, 23 (pairs 2, 6, 15, 23, component 13/14, component 19/20).
- Bit 13 (pair 15) is the most coupling-destructive: ratio = 0.814, Δ = -1.092 (drops below 1.0 — anti-coupling).
- Bit 23 (component 19,20) is second: ratio = 1.134, Δ = -0.773.

**Near-transparent flips** (|Δratio| < 0.1): bits 3, 9, 11, 16, 24, 26 (pairs 3, 9, 11, 18, component 25/26, component 29/30).

Note: 20K samples per condition yields ~5-10% relative precision on the ratio. Values with |Δratio| < ~0.3 are within noise.

---

## Table 3: Summary Classification

| bit | pair(s) | type | classification |
|----:|--------:|:----:|:---------------|
| 0 | 0 | A | degrades_at_least_one |
| 1 | 1 | A | degrades_at_least_one |
| 2 | 2 | A | degrades_at_least_one |
| 3 | 3 | A | mixed |
| 4 | 4 | A | degrades_at_least_one |
| 5 | 5 | A | mixed |
| 6 | 6 | A | mixed |
| 7 | 7 | A | degrades_at_least_one |
| 8 | 8 | A | degrades_at_least_one |
| 9 | 9 | A | mixed |
| 10 | 10 | A | **improves_at_least_one** |
| 11 | 11 | A | mixed |
| 12 | 12 | A | mixed |
| 13 | 15 | A | degrades_at_least_one |
| 14 | 16 | A | mixed |
| 15 | 17 | A | mixed |
| 16 | 18 | A | degrades_at_least_one |
| 17 | 21 | A | **improves_at_least_one** |
| 18 | 22 | A | degrades_at_least_one |
| 19 | 23 | A | degrades_at_least_one |
| 20 | 24 | A | mixed |
| 21 | 31 | A | mixed |
| 22 | 13,14 | B | **neutral** |
| 23 | 19,20 | B | degrades_at_least_one |
| 24 | 25,26 | B | mixed |
| 25 | 27,28 | B | degrades_at_least_one |
| 26 | 29,30 | B | mixed |

**Counts:**
- degrades_at_least_one: 12 (44%)
- mixed: 12 (44%)
- improves_at_least_one: 2 (7%)
- neutral: 1 (4%)

---

## Structural Notes

1. **Asymmetry is the most fragile signal.** 22 of 27 flips degrade it. Only 7 Type A flips improve it, and 0 Type B flips change it at all (except bit 26). This means asymmetry depends on nearly the entire free-pair orientation — most bits contribute to it, and KW's choice is near-optimal.

2. **χ² has variable sensitivity.** 5 bits are transparent (Δ = 0), while the extremes span from -1.032 to +4.129. The degradation range is asymmetric — much easier to worsen uniformity than improve it.

3. **M-score changes are sparse.** Only 13 of 27 flips change it (the M-decisive pairs). This is expected — only pairs where L2 ≠ L5 can change the M-score.

4. **Component (13,14) is perfectly invisible** — flipping it changes nothing across all three metrics. This is the only fully neutral bit.

5. **Two pure-improvement bits exist**: pair 10 and pair 21. Both improve χ² and asymmetry without touching M-score. These are candidates for "KW chose sub-optimally here" or "these bits serve a purpose not captured by these three metrics."

6. **Coupling is most fragile to bit 13 (pair 15)**. Flipping pair 15 drops the coupling ratio below 1.0, meaning the χ²–asymmetry correlation actually inverts. Pair 15 is also the worst single-bit χ² degradation (Δ = +4.129). This bit appears to be a structural keystone for the coupling phenomenon.

---

## Data Files

- `round1_data.json` — complete raw data (27 metric profiles, 27 coupling estimates, classifications, KW baseline)
- `single_bit_fragility.py` — computation script (reproducible, seed-fixed)
