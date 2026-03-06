# Round 5: Basin Characterization — Results

## KW Reference Profile

| Metric | KW Value | Direction |
|--------|----------|-----------|
| Kernel χ² | 2.290 | Lower = better |
| Canon asymmetry | +3 | Higher = better |
| M-score | 12/16 | Higher = better |
| Kernel autocorrelation | −0.464 | More negative = better |

---

## Critical Correction: KW Is Not a Basin Attractor

Round 4's finding that "forward greedy L1-to-KW-target recovers KW from random starts" was **circular**. The L1-to-KW-target objective uses KW's own metric values as the target. KW is a fixed point of targeting itself — this says nothing about whether KW is discoverable without prior knowledge of KW.

Round 5 tests three **KW-agnostic** criteria — improvement rules that define "better" without referencing KW's specific values — and finds:

**KW is never recovered. Not once. Under any criterion. From any of 200 random starts.**

---

## Test 1: Descent from 200 Random Starts × 3 Criteria

### Three KW-Agnostic Acceptance Criteria

| Criterion | Rule | Character |
|-----------|------|-----------|
| **A** (Pareto) | Accept if no axis worsens and ≥1 improves | Conservative; preserves all gains |
| **B** (Balanced) | Accept if std-normalized sum improves | Weighted by random variability |
| **C** (Worst-axis) | Accept if minimum axis-distance-from-median increases | Focuses on weakest signal |

### Results

| Criterion | KW exact | ≤ Ham 4 | Median Ham | Distinct attractors | Dom-by-KW | Trade-off |
|-----------|----------|---------|------------|---------------------|-----------|-----------|
| A (Pareto) | **0/200** | 0/200 | 12 | 200 | 51 | 149 |
| B (Balanced) | **0/200** | 82/200 | 5 | 10 | 0 | 200 |
| C (Worst-axis) | **0/200** | 3/200 | 11 | 194 | 90 | 110 |

### Criterion A: Pareto Non-Degradation

Every random start finds a different fixed point (200 distinct attractors). The Pareto improvement landscape has no structure — it fragments into 200 islands. 51 of 200 final orientations are dominated by KW; 149 are trade-offs. None dominate KW.

The minimum Hamming distance from KW is 5. The median is 12. Pareto non-degradation is too permissive — it accepts moves that improve any one axis regardless of the magnitude, leading to chaotic drift.

### Criterion B: Balanced Improvement ★

**The most informative criterion.** Only 10 distinct attractors among 200 starts — the landscape has strong basin structure. The Hamming distribution is bimodal:

| Cluster | Hamming range | Count | % | Character |
|---------|---------------|-------|---|-----------|
| Near-KW | 3–5 | 116 | 58% | chi²-improved, kac-relaxed |
| Far-KW | 7–10 | 84 | 42% | Further from KW |

**The dominant attractor** (68/200 = 34%) sits at Hamming 4 from KW (pairs 9, 19, 20, 21):

| Metric | KW | H=4 attractor | Change |
|--------|-----|---------------|--------|
| χ² | 2.290 | 2.806 | Worse (+0.516) |
| asym | +3 | +3 | Equal |
| m | 12 | 13 | Better (+1) |
| kac | −0.464 | −0.581 | Better (−0.117) |
| **Pareto** | — | **trade-off** | — |

This attractor trades 0.5 units of χ² for 0.12 units of kac and +1 m-score. Under balanced normalization, the gains overpower the loss.

**The secondary attractor** (14/200 = 7%) sits at Hamming 3 (pairs 9, 11, 21):

| Metric | KW | H=3 attractor | Change |
|--------|-----|---------------|--------|
| χ² | 2.290 | 0.742 | Better (−1.548) |
| asym | +3 | +4 | Better (+1) |
| m | 12 | 13 | Better (+1) |
| kac | −0.464 | −0.409 | Worse (+0.055) |

This attractor achieves the χ² floor (0.742 — the best reachable by 3-bit perturbation from iter4) while improving asym and m. It sacrifices 12% of kac.

**Both attractors use the two core dominator bits (free bits 9 and 17 = pairs 9 and 21).** These are the same bits that appear in 93.8% of the 16 known KW-dominators. The balanced-improvement landscape and the dominator landscape share the same critical directions.

### Criterion C: Worst-Axis Improvement

Nearly as fragmented as Pareto (194 distinct attractors). The minimax criterion creates many local optima because different axes become the worst at different points, creating oscillation. 90/200 final orientations are dominated by KW.

One run reaches Hamming 1 from KW (pair 29 flipped): χ²=1.258, asym=2, m=12, kac=−0.473. This is a trade-off (chi2 better, asym worse, kac better).

### Final Metric Distributions

| Criterion | Mean χ² | Mean asym | Mean m | Mean kac |
|-----------|---------|-----------|--------|----------|
| KW | 2.290 | +3 | 12 | −0.464 |
| A (Pareto) | 3.165 | +2.2 | 9.4 | −0.351 |
| B (Balanced) | **2.120** | **+3.8** | **12.4** | **−0.517** |
| C (Worst-axis) | 2.048 | +1.4 | 10.7 | −0.359 |

Criterion B's attractors are closest to KW in character: moderate chi², positive asymmetry, strong m-score, strong kac. But the mean kac (−0.517) is BETTER than KW's (−0.464), and the mean chi² (2.120) is also better. The balanced-improvement landscape consistently finds orientations that improve on KW's profile.

---

## Test 2: Basin Boundary Probing

Starting from KW, randomly flip 1–20 free bits, then reconverge using Criterion B.

| Walk length | KW recovered | ≤ Ham 4 | Median Ham |
|-------------|-------------|---------|------------|
| 1 | 0/100 | 94/100 | 4 |
| 2 | 0/100 | 92/100 | 4 |
| 3 | 0/100 | 86/100 | 4 |
| 4 | 0/100 | 89/100 | 4 |
| 5 | 0/100 | 78/100 | 4 |
| 8 | 0/100 | 71/100 | 4 |
| 12 | 0/100 | 60/100 | 4 |
| 16 | 0/100 | 60/100 | 4 |
| 20 | 0/100 | 54/100 | 4 |

**KW is never recovered** — not even after a single random flip. The Criterion B landscape has a consistent gradient away from KW toward the Hamming-4 attractor.

The median final Hamming distance is **always 4**, regardless of walk length. This means:
- Even 1-bit perturbations from KW don't reconverge to KW — they slide to the H≈4 attractor
- Even 20-bit perturbations (massive disruption) reconverge to within Hamming 4 of KW (54% of the time)

**The basin boundary is at KW itself.** KW is on the boundary, not inside the basin. The basin belongs to the Hamming-3-to-5 attractors.

---

## The Greedy Balanced-Cost Path from KW

Starting from KW and greedily flipping the bit that most improves balanced cost:

| Step | Bit flipped | Pair(s) | Ham | χ² | asym | m | kac | Cost |
|------|-------------|---------|-----|-----|------|---|------|------|
| 0 | — | — | 0 | 2.290 | +3 | 12 | −0.464 | −9.884 |
| 1 | Free bit 17 | Pair 21 | 1 | 1.258 | +4 | 12 | −0.461 | −10.552 |
| 2 | Free bit 9 | Pair 9 | 2 | 0.742 | +3 | 13 | −0.447 | −10.720 |
| 3 | Free bit 23 | (19,20) | 4 | 2.806 | +3 | 13 | −0.581 | −10.991 |

**The first move flips pair 21** — the same pair that is the most frequent dominator bit (93.8%). The greedy path uses all three core dominator bits (17, 9, 23) in its first three steps.

Step 1 is remarkable: flipping pair 21 alone improves chi² by 1.032, asym by 1, and worsens kac by only 0.003. This is the bit 17 anomaly from iter4 — the ~15× most efficient trade. Under balanced normalization, it's a clear improvement.

Step 3 (component 19,20) adds chi² (+2.064) but gains kac (−0.134). The chi² cost is large, but the kac gain is worth 14× more in std-normalized terms.

---

## What the Attractor Landscape Reveals

### 1. KW is not a basin attractor — it's a saddle

Under any reasonable KW-agnostic improvement criterion, the landscape slopes away from KW. The "basin of attraction" found in Round 4 was an artifact of self-targeting (L1 to KW's own values). KW sits at a saddle point where:

- Moving in the {9, 17, 23} direction improves balanced cost (chi²↓ + kac↓ > chi²↑)
- Moving in other directions worsens cost
- No single direction is Pareto-dominant (confirmed in iter4)

### 2. The landscape has two attractor families

The 10 distinct Criterion-B attractors cluster into two families:

| Family | Representative | Ham from KW | Character |
|--------|---------------|-------------|-----------|
| **Chi²-focused** | Pairs {9, 11, 21} | 3 | chi²→0.742, kac slightly worse |
| **kac-focused** | Pairs {9, 19, 20, 21} | 4 | kac→−0.581, chi² slightly worse |

Both families share the core bits (9 and 17/pair 21). They diverge on whether to prioritize chi² reduction (via bit 11) or kac improvement (via component 23). The stochastic bit-selection order determines which family a descent run reaches.

### 3. KW's kac extremity is the anomaly

Under balanced-cost improvement, every attractor has worse kac than its other metrics would suggest. KW stands out precisely because it has *anomalously strong kac relative to its chi²*. The balanced attractors achieve better chi² than KW (mean 2.120 vs 2.290) but better kac too (mean −0.517 vs −0.464).

KW preserves kac at the expense of chi². The balanced criterion says this trade is suboptimal — you can get both better by flipping the right bits. But the Pareto structure says you can't get both better *simultaneously* with single-bit moves (iter4). The 2-step escape via chi² epistasis is the only route, and KW doesn't take it.

### 4. The dominator bits are the balanced-improvement directions

Bits 9, 17, and 23 — the core of the dominator structure — are also the first three moves in balanced-cost greedy descent from KW. The dominators (which improve kac while holding chi²/asym/m constant) and the balanced-cost attractors (which improve everything via trade-offs) share the same critical directions in orientation space.

### 5. Basin boundary at Hamming 0

The reconvergence test shows that even a 1-bit perturbation from KW doesn't reconverge to KW. The "basin" has zero radius. KW is the unique point in its neighborhood that maintains its specific kac-chi² balance. Move one step in any direction and the balanced-cost landscape carries you to a different optimum.

---

## The Revised Picture

| Round | Claim | Status after Round 5 |
|-------|-------|---------------------|
| R4-P5 | "KW is a basin attractor" | **Circular.** Only under self-targeting. |
| R4-P5 | "Forward greedy L1 recovers KW" | **True but trivial.** Any point is recovered by targeting itself. |
| R3 | "12 dominators exist (Hamming 2-8)" | **Confirmed.** They share the same bits as the balanced attractors. |
| R3 | "KW is not globally Pareto-optimal" | **Confirmed and strengthened.** KW is locally Pareto-optimal (1-bit) but suboptimal under any reasonable scalarization. |

### KW's Character

KW is **not** a basin attractor. It is a **ridge point** — a configuration that is:

1. **Locally Pareto-optimal** at Hamming distance 1 (no non-degrading single flips)
2. **Pareto-dominated** at Hamming distance 2 (the 16 dominators improve kac without cost)
3. **Scalarization-suboptimal** under balanced criteria (greedy descent moves away immediately)
4. **Structurally distinctive** in that it maintains a specific kac-chi² balance that no generic criterion reproduces

KW's uniqueness is not that it sits at a basin minimum, but that it sits at a **specific point on a ridge** where kac is prioritized over chi². Under the balanced criterion, the rational move is to trade kac for chi²+m gains. KW doesn't make this trade. Either:

1. The arranger valued kac more than balanced cost suggests (sequential anti-repetition was prioritized over distributional uniformity)
2. The arranger used single-bit perturbation and couldn't discover the 2-step escape
3. An unmeasured 5th criterion holds KW at this point

---

## Data Files

| File | Contents |
|------|----------|
| round5_basin.py | Test 1 (200 starts × 3 criteria) + Test 2 (basin boundary) |
| round5_data.json | All convergence data, final orientations, statistics |
| round5_results.md | This document |
