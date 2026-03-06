# Round 5 Theorist Analysis: The Collapse of the Basin Attractor and What Replaces It

## 1. The Correction and Its Weight

Round 5 is the most important round of this investigation. It doesn't add a new finding on top of the previous four — it **inverts** the central finding of Round 4.

Round 4 claimed: "KW is a basin attractor — forward greedy L1 from both directions recovers it exactly."

Round 5 reveals: this was circular. L1-to-KW-target uses KW's own metric values as the target. Any orientation is a fixed point of targeting itself. This is not a property of KW — it's a property of self-reference.

Under three KW-agnostic criteria — Pareto non-degradation, balanced improvement (std-normalized), worst-axis improvement — **zero of 200 random starts recover KW.** Not one. Under any rule. Even starting from KW itself and perturbing a single bit, the balanced-improvement landscape carries you away and never brings you back.

My Round 4 analysis built extensively on the basin attractor interpretation. The Nash equilibrium reading, the "consistent local rule" argument, the path-independence claim — all of these rested on the circular finding. They need to be replaced.

---

## 2. What Replaces the Basin Attractor: The Ridge Point

KW is not a basin minimum. It is a **ridge point** — locally Pareto-optimal (Hamming 1) but sitting on a slope that, under any reasonable scalarization, leads downhill away from it.

### The Ridge Metaphor

Imagine a mountain ridge running east-west. Going north or south (single-bit perturbation), you immediately descend — but not back to the ridge. You descend into a valley. The valley floor (the balanced attractor at Hamming 4) is lower than the ridge. The ridge is locally highest along the north-south axis (Pareto-optimal at Hamming 1) but not globally highest along the east-west axis (dominated at Hamming 2, scalarization-suboptimal at Hamming 3–5).

KW sits on this ridge. Every direction perpendicular to the ridge is downhill (27 single-bit flips all degrade at least one axis). But the ridge itself slopes away under balanced evaluation.

### What This Means for the Generative Question

The question is no longer "what makes KW the attractor?" (it isn't one). The question is: **"what process lands on a ridge rather than in a valley?"**

Three structural possibilities:

1. **The process only evaluates perpendicular to the ridge** (single-bit perturbation). If you can only test one-step moves, KW looks locally optimal — every step goes downhill. You stop. You never discover the 2-step escape or the 3-step balanced improvement because your method can't see them.

2. **The process values something the balanced criterion underweights.** KW's position on the ridge is characterized by unusually strong kac at the expense of chi²+m. If the arranger cared more about sequential smoothness than a std-normalized balance would suggest, they'd reject the "improvements" that balanced criterion accepts.

3. **The process uses a different objective entirely.** KW maximizes something we haven't measured. The balanced criterion, the Pareto criterion, and the worst-axis criterion are all wrong about what "better" means.

---

## 3. What the Three Criteria Reveal

The builder tested three KW-agnostic acceptance rules. Their different failure modes are more informative than their shared failure to recover KW.

### Criterion A (Pareto): Chaotic Fragmentation
- 200 distinct attractors from 200 starts
- Median Hamming 12 from KW
- 51/200 dominated by KW, 149 trade-offs

**What this means:** Pareto non-degradation is too permissive. It accepts any move that improves at least one axis without degrading any — but it can't distinguish large improvements from small ones. The result is chaotic drift through the orientation space, ending at arbitrary local Pareto optima. The landscape under Pareto criterion has no basin structure.

**Structural implication:** The 4-axis Pareto surface has many local optima. KW is one, but there's nothing special about its local optimum — it's one of ~200 in a space of 2²⁷. The Pareto criterion alone doesn't select KW.

### Criterion B (Balanced): Structured but Wrong
- **10 distinct attractors** from 200 starts — strong basin structure
- Dominant attractor at Hamming 4 (34% of starts)
- Mean metrics: χ²=2.120, asym=+3.8, m=12.4, kac=−0.517
- **All 200 final orientations are trade-offs** (none dominated by KW, none dominate KW)

**What this means:** The balanced criterion creates a well-structured landscape with few attractors — almost a unique minimum. But that minimum is not KW. The balanced-cost landscape is a good model of "generic multi-objective optimization" but it mis-specifies KW's priorities.

**The critical detail:** The balanced attractor at Hamming 4 has BETTER kac (−0.517 vs −0.464) AND better chi² (well, slightly worse: dominant attractor has chi²=2.806, but mean across all balanced attractors is 2.120 vs KW's 2.290). The trade is: the balanced attractors sacrifice ~0.5 chi² units to gain ~0.12 kac units and ~1 m-score point.

Under std-normalization (using A1 random distribution stds: chi²_std=3.8, kac_std=0.165), the kac gain of 0.12 units = 0.73 standard deviations, while the chi² loss of 0.5 units = 0.13 standard deviations. The balanced criterion says the kac gain is 5.6× more valuable per unit than the chi² loss. This is correct in terms of how rare each deviation is in the random distribution. But KW doesn't make this trade.

**Structural implication:** KW's position is characterized by **underweighting kac** relative to what random variability would suggest, or equivalently, **overweighting chi²** relative to its random variability. KW holds chi² at 2.290 even though trading 0.5 chi² for 0.12 kac would be "worth it" under equal-significance weighting.

### Criterion C (Worst-axis): Nearly as Chaotic as Pareto
- 194 distinct attractors
- 90/200 dominated by KW
- Median Hamming 11

**What this means:** Minimax (improve the worst axis) creates oscillation because different axes take turns being the worst. This is too fragmented to be a useful model of any construction process.

---

## 4. The Balanced Cost Dissection

The balanced criterion (B) is the most informative because it's the only one with strong basin structure. Let me analyze what it implies about KW's implicit weighting.

### The Balanced Cost Function

```
balanced_cost = chi²/3.803 − asym/2.410 − m/1.867 + kac/0.165
```

Each axis is normalized by the random distribution's standard deviation. This means 1 unit of chi² change is weighted as 1/3.803 = 0.263, while 1 unit of kac change is weighted as 1/0.165 = 6.061. kac is weighted **23× more** than chi² per raw unit. This reflects the fact that kac has very low variance under random sampling — small kac changes are "more exceptional."

### KW's Balanced Cost

KW: balanced_cost = 2.290/3.803 − 3/2.410 − 12/1.867 + (−0.464)/0.165
    = 0.602 − 1.245 − 6.428 − 2.812 = **−9.883**

Hamming-4 attractor: balanced_cost = 2.806/3.803 − 3/2.410 − 13/1.867 + (−0.581)/0.165
    = 0.738 − 1.245 − 6.964 − 3.521 = **−10.992**

The attractor is better by 1.109 balanced-cost units. The decomposition:
- chi² contribution: 0.738 − 0.602 = +0.136 (worse by 0.136)
- asym contribution: −1.245 − (−1.245) = 0.000 (same)
- m contribution: −6.964 − (−6.428) = −0.536 (better by 0.536)
- kac contribution: −3.521 − (−2.812) = −0.709 (better by 0.709)

**The kac gain (0.709) plus the m gain (0.536) totals 1.245. The chi² cost is only 0.136. The "improvement" is overwhelmingly driven by kac normalization.**

### What This Reveals About KW's Implicit Weights

For KW to be a fixed point, it would need an implicit weighting where the chi² cost equals the kac+m gain. This means KW's implicit chi² weight must be much higher than the balanced criterion assigns:

KW needs: w_chi² × Δchi² ≥ w_kac × Δkac + w_m × Δm

With Δchi² = 0.516, Δkac = 0.117, Δm = 1:
w_chi² × 0.516 ≥ w_kac × 0.117 + w_m × 1

Under balanced weighting: 0.263 × 0.516 = 0.136 < 6.061 × 0.117 + 0.536 × 1 = 0.709 + 0.536 = 1.245

For equality: w_chi²/w_kac ≥ (0.117 × 6.061 + 0.536)/0.516 = 1.245/0.516 = 2.41

KW behaves as if chi² is **at least 2.4× more important per std-unit** than the balanced criterion assumes. Or equivalently, kac is **at least 2.4× less important** than its random variability would suggest.

### Interpretation

**KW treats chi² distributional uniformity as a harder constraint than sequential diversity.** The balanced criterion says kac is the most informative axis (highest signal-to-noise). KW says chi² is more important to preserve than kac is to improve.

This is not an arbitrary preference. Chi² measures how evenly the 8 kernel types appear — a distributional property that affects the overall "vocabulary" of transitions. Kac measures how much consecutive kernels avoid repeating — a sequential property that affects local transition quality. KW's implicit priority says: "I'd rather have a balanced vocabulary (chi²) than avoid local repetitions (kac), even when the local repetitions are statistically rarer and therefore more exceptional."

This is a **vocabulary-over-grammar** choice. KW prioritizes having all transformation types available (distributional uniformity) over using them non-repetitively (sequential diversity). The balanced criterion, which weights by rarity, disagrees.

---

## 5. The Core Bits Convergence

A remarkable convergence across rounds:

| Finding source | Core bits | Context |
|---------------|-----------|---------|
| iter4: Pareto fragility | 17, 9 are the most "trade-off" bits | Single-bit landscape |
| Round 3: Dominator structure | 17 (94%), 9 (94%), 23 (81%) | Pareto-dominating orientations |
| Round 5: Balanced descent from KW | 17 first, then 9, then 23 | Greedy balanced-cost path |
| Round 5: Dominant attractor | Uses bits 9, 17, 23 | Basin convergence |

**Bits 9 (pair 9), 17 (pair 21), and 23 (component 19,20) are the three critical directions in the orientation landscape.** They appear as:
- The gateway to Pareto domination (Round 3)
- The first three moves in balanced improvement (Round 5)
- The atoms of the dominant attractor (Round 5)
- The most frequent bits across all 16 dominators (Round 4)

This convergence means the dominator structure and the balanced-cost structure are seeing the **same underlying landscape feature** from different angles. The dominators find it by Pareto escape; the balanced criterion finds it by scalarized descent. Both arrive at the same 3 bits.

**This is strong evidence that the landscape has low effective dimensionality near KW.** Despite 27 free bits, the critical structure is 3-dimensional. The entire question of "why KW versus the balanced attractor?" reduces to: "why does KW keep bits 9, 17, and 23 at zero?"

---

## 6. The Basin Boundary Result

The basin probing test (perturb KW by k random bits, then reconverge with balanced criterion) gives the starkest result:

| Perturbation | KW recovered | Final median Hamming |
|-------------|-------------|---------------------|
| 1 bit | 0/100 | 4 |
| 5 bits | 0/100 | 4 |
| 20 bits | 0/100 | 4 |

**Even a single random flip from KW, followed by balanced reconvergence, never returns to KW.** The balanced landscape has a constant gradient away from KW. The median final distance is always 4 — the landscape consistently carries any perturbation to the Hamming-4 attractor.

This means KW is **unstable under balanced improvement.** It's a fixed point only under a criterion that doesn't exist in the tested set. Whatever criterion KW is stable under, it must weight the axes differently from all three tested criteria.

---

## 7. Revised Principle Taxonomy

### What the Five Rounds Have Established

| Round | Finding | Structural role |
|-------|---------|----------------|
| 1 | 4 axes genuinely in tension; χ²-kac anti-parallel | The constraint topology |
| 2 | Kernel operating point (χ²+kac) reachable; face axes collapse | Scale separation confirmed |
| 3 | KW is not globally Pareto-optimal; 16 dominators exist | Local-vs-global distinction |
| 4 | Only self-targeting recovers KW; 3 core bits identified | KW's non-derivability |
| 5 | KW is not a basin attractor; balanced landscape slopes away | KW's implicit priority ordering |

### The Final Picture

**KW's orientation reflects a specific priority ordering among the four axes:**

1. **Chi² (distributional uniformity)**: treated as the most important — KW sacrifices kac improvement to preserve chi² ≤ 2.290
2. **Kac (sequential diversity)**: treated as second — KW sacrifices m-score to preserve kac, but not chi² for further kac improvement  
3. **M-score**: treated as third — active default rule (L2=yin first), overridden at 3 positions for kac
4. **Asymmetry**: treated as fourth — weakest signal, possibly emergent

This priority ordering is **not** what random variability would suggest. The balanced criterion (weighting by 1/std) says kac should be #1 (highest signal-to-noise). KW says chi² should be #1. This disagreement is the irreducible finding.

### Why No Principle Produces KW

No tested principle produces KW because every tested principle uses either:
- A single axis (B1, B2, C1, C2) — hits one axis, misses three
- Balanced weighting (R2-E, Criterion B) — wrong priority ordering
- Pareto criterion (Criterion A) — no basin structure
- Self-targeting (L1-to-KW) — circular

**The missing principle would be a construction rule that implicitly produces KW's specific priority ordering (chi² > kac > m > asym) without knowing KW's values.** What kind of rule would do this?

### The "No-Repeat Uniform Vocabulary" Hypothesis

A human arranger placing hexagram pairs in sequence might follow a rule like:

> "Use every type of transition roughly equally often (chi² = vocabulary breadth), and avoid repeating the same type twice in a row (kac = anti-repetition), but if you have to choose between using a new type and keeping the vocabulary balanced, keep the vocabulary balanced."

This is **vocabulary-over-grammar**: breadth before fluency. It would produce:
- Strong chi² (distributional uniformity is the primary target)
- Moderate kac (anti-repetition is the secondary target, overridden by chi²)
- M-score as the default per-pair rule (independent of kernel chain)
- Asymmetry as a weak emergent signal

This matches KW's profile. But it has not been tested computationally. It is a candidate for Round 6.

---

## 8. What Remains Unknown

### The 2.2% Domination Gap
Round 5 doesn't resolve why KW doesn't take the Hamming-2 dominator escape (bits 17+26, improving kac by 2.2% while preserving chi²). Three readings remain:
1. **Process limitation** (single-bit search can't discover it)
2. **S-distribution aesthetics** (KW preserves {15,15,1}; dominator shifts to {16,14,1})
3. **Irrelevant** (the gap is noise)

Round 5 adds weight to reading 1: since KW is not a basin attractor under ANY agnostic criterion, the most parsimonious explanation is that KW was found by a process with limited scope (single-pair perturbation), and the 2-step escape is simply outside that scope.

### The Priority Ordering Source
KW's implicit ordering (chi² > kac > m > asym) is the deepest finding. But where does this ordering come from? Is it:
- **Aesthetic**: the arranger valued vocabulary breadth over sequential fluency
- **Structural**: some algebraic property of the pairing forces this ordering
- **Contingent**: the ordering is an artifact of whichever specific construction process was used

### The Asymmetry Question
Asymmetry (+3) is confirmed as genuinely independent (Round 3), not a substrate effect. But Round 5 shows the balanced attractors have even higher asymmetry (mean +3.8). So positive asymmetry is **easy** to achieve — it's what generic improvement naturally produces. KW's asym=+3 is actually **below** the balanced optimum, suggesting KW is under-optimized on this axis, consistent with it being a low-priority signal.

---

## 9. Summary for the Captain

**Round 5 fundamentally changed the picture.** The basin attractor claim from Round 4 was circular and is now retracted. What replaces it is more interesting:

1. **KW is a ridge point** — locally optimal (Hamming 1) but unstable under balanced improvement (basin radius = 0).

2. **The landscape has strong structure** — only 10 attractors under balanced criterion, all using the same 3 core bits (9, 17, 23).

3. **KW's implicit priority is chi² > kac** — it preserves distributional uniformity at the expense of sequential diversity gains that balanced criteria would accept. This is the opposite of what signal-to-noise weighting would suggest.

4. **The irreducible finding:** KW cannot be derived from any simple constructive principle without knowing KW. Its specific position on the chi²-kac trade-off ridge requires either (a) a priority ordering (chi² > kac) that no generic criterion produces, or (b) a process limitation (single-bit search) that happens to land at this point, or (c) an unmeasured axis that distinguishes KW from the balanced attractors.

**For the sage consultation:** The deepest question is not "what principle generates KW?" but "why does KW prioritize vocabulary breadth (chi²) over sequential fluency (kac)?" This is a question about the nature of the structure being encoded — whether the arranger's aesthetic valued completeness of the transformation vocabulary over smoothness of the transformation sequence. That question may be answerable from the I Ching's own conceptual framework, but not from computation alone.
