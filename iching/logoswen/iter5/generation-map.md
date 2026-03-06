# Generation Map — Iter5 (Final)

## The Question

*What principle — applied during sequence construction — produces all four orientation signals as joint consequences?*

## The Answer

**No single constructive principle produces KW. No algorithm reproduces it without already knowing the target. KW is a ridge point — locally optimal under single-pair adjustment, sitting at a specific balance between distributional completeness and sequential fluency that no generic criterion selects.**

The minimum decomposition requires N=2 principles (M-preference + sequential anti-repetition), with distributional uniformity emergent and asymmetry residual. The 2.2% domination gap at Hamming 2 reflects the resolution limit of single-pair perturbation, not a structural flaw.

The investigation's deepest finding: **KW prioritizes vocabulary breadth (all kernel types represented) over sequential fluency (avoiding repetition) — a vocabulary-over-grammar choice that no balanced criterion reproduces.** This is consistent with an arranger who understood the sequence as a *map of situations* rather than a *narrative to be read sequentially*.

## KW Target Profile

| Axis | Metric | KW Value | Scale | Construction role |
|------|--------|----------|-------|-------------------|
| 1 | Kernel χ² | 2.290 | Global (histogram) | Protected; emergent not targeted |
| 2 | Canon asymmetry | +3 | Per-pair (local) | Residual; weakest signal |
| 3 | M-score | 12/16 | Per-pair (local) | Default rule; overridden at 3+1 positions |
| 4 | Kernel autocorrelation | −0.464 | Sequential | Override criterion; kac > m at conflicts |

## Construction Hierarchy (Final)

| Priority | Constraint | Type | Mechanism |
|----------|-----------|------|-----------|
| 0 | S=2 avoidance | Hard structural | 5 bits forced; 1 M-exception forced |
| 1 | Distributional uniformity (χ²) | Emergent, protected | Not targeted but preserved over kac+m trades |
| 2 | Sequential anti-repetition (kac) | Primary soft override | Overrides M-rule at 3 conflict positions |
| 3 | M-preference (L2=yin first) | Secondary soft default | Active at 12/16 decisive positions |
| 4 | Asymmetry (upper-high-first) | Tertiary / residual | Possibly emergent from above |

## Landscape Characterization

| Property | Value | Evidence |
|----------|-------|----------|
| Local Pareto optimality (H=1) | Yes | 0/27 single-bit flips non-degrading (iter4) |
| Global Pareto optimality (H≥2) | **No** | 16 dominators (H=2–10), best kac=−0.547 |
| Basin attractor | **No** | 0/600 agnostic descents recover KW (R5) |
| Basin radius | **0** | Even 1-bit perturbation never reconverges (R5) |
| Effective dimensionality | **3 bits** | Bits 9, 17, 23 define the escape manifold |
| Domination gap | 2.2% kac | Hamming-2 dominator: bits {17, 26} |
| KW character | **Ridge point** | Locally optimal in 24D; on gentle slope in 3D |

## What 50+ Generators Proved

| What was tested | What was eliminated |
|-----------------|-------------------|
| Single-axis optimizers (6) | Single-objective optimization |
| Composites, hybrids, scalarizations (21) | Linear decomposition / weighted combination |
| Simulated annealing (100 runs) | Global Pareto optimality |
| Forward/reverse greedy targeting KW | Self-targeting (circular — any point is its own fixed point) |
| 3 KW-agnostic criteria × 200 starts | Basin attractor hypothesis |

**Zero generators dominate KW. Zero non-circular generators reproduce KW.**

## The Three Remaining Readings

The data cannot distinguish between:

| Reading | KW is... | Stopped because... |
|---------|----------|-------------------|
| A (Intentional craft) | Product of deliberate multi-scale balance | The arranger *chose* this point |
| B (Bounded rationality) | Product of simple local rule iterated to convergence | Single-pair search can't see the escape |
| C (Structural constraint) | Held by an unmeasured 5th criterion | We haven't found what distinguishes it |

All three are consistent with all observations. Disambiguation requires evidence computation cannot provide.

The sage's resolution: these are not competing hypotheses but **three aspects of one process** — how (the search method), why (the value ordering), why here exactly (the specific coordinates). They were never separate.

## The Sage's Resolution

> *KW's orientation is the fingerprint of someone who understood what they were making. The specific trade-offs — what was protected, what was sacrificed, what was left to emerge — are consistent with an arranger who grasped that the sequence needed to represent the complete space of transformation, not just provide a smooth reading experience.*

> *The generative difficulty IS the structure. KW's orientation is the specific configuration where multiple incompatible pressures reach mutual accommodation. Accommodation is not a principle you can write as an algorithm. It is a process you converge to.*

> *Asking "what principle generates the orientation?" is like asking "what principle generates the shadow?" The shadow is real, measurable, characterizable — but it's cast by a three-dimensional object, and no analysis of shadows alone can recover the third dimension.*

## Complete Round Log

| Round | What was tested | Key finding | What died |
|-------|----------------|-------------|-----------|
| 1 | 6 baseline generators | χ²–kac anti-parallel; face–flow orthogonal; C2 matches m=12 | Single-axis optimization |
| 2 | 21 composites + scalarizations | χ²–kac trade-off mapped; face-flow bridge unachievable; kac normalization bug caught | Weighted combination |
| 3 | Anatomy + annealing + Pareto search | **KW not globally Pareto-optimal** — 16 dominators; M-exceptions protect kac; asymmetry independent | Global optimality |
| 4 | Dominator investigation + greedy construction | 3 core bits (9, 17, 23); L1-to-KW recovers KW (circular); hierarchy established | *(False positive: basin attractor)* |
| 5 | 3 KW-agnostic criteria × 200 starts + basin probing | **KW not a basin attractor** — 0/600 recovery; basin radius = 0; vocabulary-over-grammar | Basin attractor hypothesis |

## Data Files

| Round | Results | Data | Scripts |
|-------|---------|------|---------|
| 1 | round1_results.md, round1_analysis.md | round1_data.json | round1_baselines.py |
| 2 | round2_results.md | round2_data.json, round2_verify_data.json, round2e_fixed_data.json | round2_generators.py, verify_c2_c1.py, round2e_fixed.py |
| 3 | round3_results.md | round3_data.json, round3_sa_data.json, round3_dominators.json | round3_anatomy.py, round3_annealing.py |
| 4 | round4_results.md, round4_analysis.md | round4_data.json, round4_dominators_extended.json | round4_analysis.py |
| 5 | round5_results.md, round5_analysis.md, round5_final_analysis.md | round5_data.json | round5_basin.py |
| — | generation-map.md | — | infra.py |
| Capstone | 23-generation-findings.md | — | — |
