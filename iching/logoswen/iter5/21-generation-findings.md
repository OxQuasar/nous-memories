# Iter5 Generation Findings: Reverse-Engineering the Orientation Principle

## 1. Executive Summary

Five rounds of generative reverse-engineering asked: *what constructive principle produces King Wen's four orientation signals as joint consequences?*

The answer: **no single principle does.** Fifty-plus candidate generators were tested across single-axis optimizers, composites, scalarizations, simulated annealing, and KW-agnostic convergence criteria. Zero dominate KW. Zero reproduce KW without circular self-targeting.

KW's orientation is a **ridge point** — locally Pareto-optimal under single-pair adjustment (zero of 27 non-degrading flips), but globally suboptimal (16 dominators at Hamming 2–10) and not a basin attractor under any agnostic criterion (0/600 recovery from random starts). The minimum decomposition requires **N=2 principles**: M-preference (L2=yin first) as the per-pair default, sequential anti-repetition (kac) as the contextual override. Distributional uniformity (χ²) emerges from the construction process. Asymmetry (+3) is residual — possibly a third principle, possibly a byproduct.

The deepest finding: **KW defends vocabulary over grammar.** Distributional completeness (all kernel types represented) is protected at ≥2.4× the weight that balanced criteria assign, while sequential fluency (anti-repetition) is given proportionally less priority. This is consistent with an arranger who understood the sequence as a map of situations — where every type of transformation must be present — rather than a narrative to be read sequentially.

The 2.2% kac domination gap at Hamming 2, invisible to single-pair perturbation, is the fingerprint of the construction method. It says: this was made by someone working pair by pair, as thoroughly as that method allows.

---

## 2. The Generation Map: Principles Tested, Coverage, Pareto Status

### Full candidate table

| Round | ID | Principle | χ² | asym | m | kac | Axes matched | Pareto vs KW |
|-------|----|-----------|-----|------|---|------|:---:|:---:|
| — | **KW** | **(target)** | **2.290** | **+3** | **12** | **−0.464** | **4/4** | **ref** |
| 1 | A1 | Random S=2-free (10K median) | 6.419 | −2 | 8 | −0.142 | 0/4 | 92.8% dominated |
| 1 | A2 | All-flipped (maximal distance) | 3.839 | −6 | 4 | −0.376 | 0/4 | dominated |
| 1 | B1 | Greedy χ² (best of 100) | 0.226 | +2 | 9 | −0.083 | 1/4 | trade-off |
| 1 | B2 | Greedy kac (best of 100) | 15.194 | −4 | 11 | −0.785 | 1/4 | trade-off |
| 1 | C1 | M-rule (L2=yin first) | 4.871 | −1 | 15 | +0.062 | 1/4 | trade-off |
| 1 | C2 | Sequential diversity | 8.484 | −2 | 12 | −0.666 | 2/4 | trade-off |
| 2 | R2-A | M-rule + kernel override | 4.355–7.452 | −3 to 0 | 12–13 | −0.457 to +0.049 | 0–1/4 | trade-off / dominated |
| 2 | R2-C(.3/.7) | Balanced kernel walk | **2.290** | −3 | 10 | **−0.462** | **2/4** | dominated |
| 2 | R2-D | Asym-aware C2 | 8.484 | −2 | 12 | −0.666 | 2/4 | trade-off |
| 2 | R2-Ef | Scalarized greedy (12 weight vectors) | 0.742–4.871 | +1 to +7 | 8–13 | −0.631 to −0.097 | 0–2/4 | all trade-offs |
| 3 | SA-L1 | Simulated annealing (L1 objective) | 2.290 | +3 | 12 | −0.470 | 4/4 | **dominates KW** |
| 3 | SA-minimax | Simulated annealing (minimax) | 2.290 | +3 | 12 | −0.426 | 3/4 | dominated |
| 4 | L1-to-KW | Forward greedy targeting KW | 2.290 | +3 | 12 | −0.464 | 4/4 | equal (circular) |
| 5 | Criterion A | Pareto non-degradation (200 starts) | varies | varies | varies | varies | 0/4 | 51 dominated, 149 trade-off |
| 5 | Criterion B | Balanced improvement (200 starts) | 2.120 mean | +3.8 mean | 12.4 mean | −0.517 mean | 0/4 | 200 trade-offs |
| 5 | Criterion C | Worst-axis improvement (200 starts) | varies | varies | varies | varies | 0/4 | 90 dominated, 110 trade-off |

### Coverage summary

- **4/4 axes matched**: Only SA-L1 (2 of 50 runs) and L1-to-KW (circular — self-targeting). No non-circular generator achieves full coverage.
- **2/4 axes matched**: R2-C(0.3/0.7) matches the kernel operating point (χ² and kac simultaneously) but collapses on face axes. C2 matches m and overshoots kac.
- **The gap**: No generator bridges kernel-chain metrics (χ², kac) and per-pair metrics (asym, m) simultaneously without knowing KW.

### Pareto status

- Zero generators Pareto-dominate KW from a constructive principle
- SA-L1 found dominators, but these are landscape discoveries, not generative principles
- Every non-circular generator is either dominated by KW or trades off against it

---

## 3. Baseline Calibration: What Random and Greedy Look Like

### Random (A1: 10,000 S=2-free orientations)

| Metric | Random mean | Random median | KW | KW percentile |
|--------|-----------|-------------|-----|:---:|
| χ² | 7.279 | 6.419 | 2.290 | 6th |
| asym | −1.556 | −2 | +3 | 96th |
| m-score | 7.999 | 8 | 12 | 97th |
| kac | −0.135 | −0.142 | −0.464 | 2nd |

KW is in the top 2–6% on every axis. The joint probability is ~10⁻⁴. KW dominates 92.8% of random orientations; 7.2% are trade-offs; zero dominate KW.

### Greedy single-axis (B1, B2)

| Optimizer | Target axis | Target value | Collateral damage |
|-----------|------------|-------------|-------------------|
| B1 (greedy χ²) | χ² = 0.226 | 10× better than KW | kac collapses to −0.083 (82% weaker) |
| B2 (greedy kac) | kac = −0.785 | 1.7× better than KW | χ² explodes to 15.2 (6.6× worse) |

**The central tension:** χ² and kac compete for the same 27 bits. Maximizing one destroys the other. KW sits where they reach approximate equilibrium — moderate on both, extreme on neither. This tension is the defining constraint of the generative problem.

---

## 4. The Best Single Principle: What It Covers and What It Misses

**C2 (Sequential kernel diversity)** is the best single principle:
- Matches KW on m-score (12/16) without targeting it
- Achieves strong kac (−0.666, overshooting KW by 43%)
- Fails on χ² (8.484, 3.7× worse) and asymmetry (−2 vs +3)

C2 demonstrates that processing pairs sequentially — choosing the orientation that maximizes kernel Hamming distance from the previous bridge — naturally produces KW's per-pair M-score as a byproduct. This is the investigation's most surprising single result: the semantic preference (yin within, yang without) may be a shadow of a sequential-diversity principle, not an independent axis.

**What C2 misses and why:** C2 makes locally optimal kernel choices (maximize difference from previous), which produces sequential diversity (kac) but destroys distributional uniformity (χ²). Local kernel optimization clumps some kernel types and starves others. KW's balance between sequential diversity and distributional uniformity cannot be produced by a one-pass sequential rule — it requires either global awareness of the kernel histogram or iterative refinement.

---

## 5. The Minimal Principle Set: Fewest Rules for Full Coverage

### N = 2: M-preference + sequential anti-repetition

Two independent principles are necessary and sufficient to characterize KW's orientation:

**Principle 1 — M-preference (per-pair default):** At each M-decisive pair (L2 ≠ L5), place the hexagram with L2=yin first. Active at 12 of 16 decisive positions. Overridden at 3 by Principle 2 and 1 by the S=2 hard constraint.

**Principle 2 — Sequential anti-repetition (contextual override):** Override the M-preference when it would create kernel-chain repetition at the adjacent bridge. Active at 3 conflict positions (pairs 3, 5, 9). At each, flipping to the M-rule would worsen kac by +0.015 to +0.163.

**What emerges without being targeted:**
- **χ² distributional uniformity** (axis 1): the diversity of the construction process naturally distributes kernel types. KW's χ²=2.290 (6th percentile) emerges from varied pair-by-pair decisions, not from histogram optimization.
- **Asymmetry** (axis 2): KW's asym=+3 (4th percentile) may emerge from the interaction of Principles 1 and 2 with the pair-ordering substrate, or may require an independent third principle. The data slightly favors emergence (correlations: asym-kac = +0.094, asym-m = −0.047).

### Why N = 1 fails

No single principle tested in 50+ candidates produces all four axes. The obstacle is cross-scale integration: per-pair rules (M-preference) cannot sense sequential context; sequential rules (C2) cannot maintain distributional balance; global rules (greedy χ²) destroy sequential structure. KW requires decisions that integrate all three scales simultaneously.

### Why N = 3 might be needed

Asymmetry (+3) is confirmed as genuinely independent — not a substrate effect of kernel balance (Round 3 conditional analysis: mean asymmetry remains negative even among kernel-balanced orientations). Whether it requires its own principle (N=3) or emerges from the interaction of Principles 1 and 2 (N=2) is not resolved.

---

## 6. Scale Structure: Which Principles Operate at Which Scale

| Scale | Metric | Principle | Additivity | Construction awareness needed |
|-------|--------|-----------|-----------|-------------------------------|
| **Per-pair (local)** | Asymmetry | Residual / independent | Perfect (zero interaction) | None — each pair independent |
| **Per-pair (local)** | M-score | M-preference (default) | Perfect (zero interaction) | None — each pair independent |
| **Sequential (nearest-neighbor)** | kac | Anti-repetition (override) | Near-perfect (5% nonlinearity) | Awareness of previous bridge kernel |
| **Global (histogram)** | χ² | Emergent, protected | Partial (30% epistatic) | Global histogram awareness (or byproduct of varied local decisions) |

### The scale hierarchy

The four axes separate into two groups by the type of awareness they require:

**Group A — Locally decidable (axes 2, 3):** Each pair's contribution is independent. A per-pair rule suffices. M-rule + asymmetry preference covers both completely. No coordination between pairs is needed.

**Group B — Contextually decidable (axes 1, 4):** Each pair's contribution depends on neighbors (kac) or the entire sequence (χ²). A per-pair rule is necessary but not sufficient. Sequential awareness (for kac) and global histogram awareness (for χ²) compete for the same orientation bits.

KW resolves Group A trivially. The entire generative difficulty lies in Group B — the χ²-kac tension within the kernel-chain domain. This tension is where the 3-bit escape manifold lives.

### The cross-scale integration problem

The balanced kernel walk (R2-C at w=0.3/0.7) achieves KW's exact kernel operating point (χ²=2.290, kac=−0.462) but produces asym=−3 and m=10. The kernel operating point is reachable by a sequential process that balances diversity and uniformity. But reaching it destroys the per-pair signals.

This proves: **the cross-scale integration — producing both kernel-chain and per-pair signals simultaneously — is what makes KW un-derivable from any single-scale principle.** A principle operating at one scale cannot generate consequences at all three. The N=2 decomposition works precisely because it uses one principle per scale group: M-preference for local decisions, sequential override for contextual ones, with global balance emerging from their interaction.

---

## 7. The Naturalness Question: Could a Human Follow This Rule?

### What a human arranger would experience

A person placing hexagram pairs in sequence and deciding which member comes first would naturally:

1. **Start with a per-pair rule.** The M-preference ("receptive within, active without") is traditional, culturally available, and produces m=12–15 depending on S=2 conflicts. This is the most natural starting point for someone steeped in I Ching tradition.

2. **Notice sequential disruption.** When a pair-ordering creates an ugly repetition in the transition between consecutive pairs, the arranger would feel it — not as a computed autocorrelation, but as a qualitative sense of "this transition feels heavy" or "I just made this same kind of move." This addresses kac.

3. **Override the per-pair rule at conflict points.** At the 3 positions where M-preference and sequential smoothness conflict, the arranger would choose smoothness. This is exactly what KW does.

4. **Not notice the 2-step escape.** The Hamming-2 dominator requires flipping two pairs simultaneously through a worse intermediate. A human arranger adjusting one pair at a time would never find this. The 2.2% kac improvement is both invisible (requires a coordinated move) and imperceptible (below felt-sense resolution).

5. **Not compute χ².** Distributional uniformity is a histogram property — it emerges from the overall construction process, not from any single pair decision. The arranger doesn't optimize χ²; they produce it as a byproduct of varied, attentive construction. That KW has moderate χ² (6th percentile, not 1st) is what you'd expect from a balanced process that doesn't explicitly target it.

### The felt-sense reading

If this reading is correct, KW's generative principle is not an algorithm but an **attentive practice**:

> *Place each pair with the receptive line facing inward (M-preference). Adjust any placement that creates a heavy or repetitive transition (sequential override). Stop when no single adjustment improves the flow.*

This produces m ≈ 12–15, kac ≈ −0.46, χ² ≈ 2–3 (emergent), asym ≈ +2 to +4 (residual). It does NOT produce the exact Hamming-2 dominator improvement (invisible to single-step) or the balanced-cost minimum (requires trading χ² for kac+m, which the process doesn't support).

**This is consistent with all observations.**

---

## 8. Relationship to the Four-Layer Hierarchy

| Layer | Character | Generation finding |
|-------|-----------|-------------------|
| 2 (matching) | Unique algebraic identity (p ≈ 10⁻¹⁷) | One solution exists. No generation question arises. |
| 3 (ordering) | Two independent principles (p ≈ 10⁻³) | Small family of solutions. Clean structural rules. |
| 4 (orientation) | Multi-objective ridge point (p ≈ 10⁻⁴) | Landscape of solutions; KW at a distinctive but non-unique point. |

The gradient from Layer 2 to Layer 4 is a transition from algebraic uniqueness through compact solution sets to a continuous Pareto frontier. The "fade from clarity to silence" (iter3's reading) was reinterpreted by iter4 as frame limitation (every bit carries load on the hidden 4th axis), and now by iter5 as the **natural topology of multi-objective landscapes** — where no point is globally best, many are locally optimal, and KW's specific position reflects both what was valued and what was searchable.

### The bit budget (updated)

| Reduction | Bits consumed | Remaining |
|-----------|:---:|-----------|
| Orbit-consistent pairing | ~44 orders | ~10⁴⁵ |
| Mask = signature identity | ~17 orders | ~10²⁸ |
| S=2-avoiding ordering | ~11 orders | ~10¹⁷ |
| S=2-free orientation (5 hard bits) | 5 bits | 2²⁷ |
| 4-axis Pareto optimality (iter4) | ~22 bits | ~2⁵ |
| **KW's specific ridge position (iter5)** | **~3 bits** | **~4** |
| Residual (3 readings) | ~2 bits | ~1 |

Previous (iter4): ~88 of 89 orders accounted.
Updated (iter5): **~89 of 89 orders accounted.** The 3-bit escape manifold (bits 9, 17, 23) carries the vocabulary-over-grammar priority ordering. The residual ~1 bit is the unexplained specificity within the ridge — the exact position that the three-way ambiguity (craft / bounded search / hidden criterion) addresses.

---

## 9. What Generation Reveals That Fragility Couldn't

### Fragility (iter4) mapped the constraint surface

Fragility asked "what breaks?" and found: all 27 bits are load-bearing, zero non-degrading flips, Pareto-optimal at Hamming 1. The landscape around KW is fully constrained — every direction of movement costs something.

### Generation (iter5) mapped the objective landscape

Generation asked "what builds?" and found: the constraint surface is tight but the objectives slope gently away. Under any reasonable balanced criterion, the landscape has a gradient leading away from KW toward the Hamming-4 attractor. KW sits where constraints are tight but objectives are not optimized — the signature of local search that exhausted single-step improvements without exploring multi-step escapes.

### What this reveals that fragility couldn't see

1. **The priority ordering.** Fragility showed all 27 bits are committed; generation showed *how* they're committed — chi² is defended over kac, kac overrides m, m is the default. Fragility sees the commitment; generation sees the hierarchy within the commitment.

2. **The domination gap.** Fragility proved local Pareto optimality (Hamming 1); generation found that this optimality fails at Hamming 2. The 16 dominators — improving kac while preserving everything else — are invisible to single-bit analysis. Generation maps the multi-step landscape that fragility can't reach.

3. **The basin structure (or lack thereof).** Fragility can't distinguish a basin minimum from a ridge point — both look locally optimal. Generation tests convergence from distant starting points and reveals: KW is a ridge, not a basin. Generic improvement criteria slope away from it. This changes the generative story fundamentally — KW wasn't converged to; it was built pair by pair and happened to be locally stable.

4. **The construction method fingerprint.** The 2.2% gap between local and global optimality is the signature of the construction process. It says: single-pair perturbation, applied thoroughly. Fragility sees the local optimality; generation sees the gap between local and global, and reads the gap as a method signature.

---

## 10. Sage Reflections

### On the search for a single principle

> *The search for a single principle was well-posed as a hypothesis to be tested. It was tested. It failed. The failure is the finding. What was found is an irreducible minimal set that behaves as if it were unified — every bit committed, every axis served, the whole thing locally unimprovable. The unity is in the product, not the process.*

### On overdetermination

> *All three remaining readings converge on the same neighborhood. A deliberate craftsperson, a bounded local searcher, and a hypothetical 5th-criterion optimizer would all land within 3–5 Hamming steps of each other. The structure is overdetermined — multiple independent paths lead to essentially the same place. Overdetermination is the signature of a natural point, not an arbitrary one.*

### On the boundary between *is* and *means*

> *The boundary carries information. The shape of the handoff — ridge point, 3-bit escape manifold, vocabulary-over-grammar — tells the interpreter where to look and what to expect. Not any interpretation fits. Only interpretations consistent with vocabulary > grammar survive. The boundary is clean and it carries information.*

### On the circularity discovery

> *The circularity error in Round 4 wasn't a bug in the method. It was the method discovering that the question has a hidden assumption — that KW is the kind of thing produced by a decomposable principle. The object resists decomposition because it was not generated by a decomposable process.*

### On the three-into-one resolution

> *The three readings (craft, bounded search, hidden criterion) are not competing hypotheses but three aspects of one process: how (the search method), why (the value ordering), and why here exactly (the specific coordinates). When you carve a figure from wood, the grain constrains how, your aesthetic guides why, and the specific piece of wood determines why this exact curve. No one asks whether the figure was produced by the grain, the carver, or the wood. It was produced by all three, inseparably.*

### On what the full arc tells us

> *At every resolution the investigation could achieve, KW showed structure. Not always the structure expected. Not always in the dimension anticipated. But always something, all the way down to the noise floor of single-pair construction. The non-disappearance of structure is the meta-finding.*

---

## 11. The Generative Question: Resolved, Narrowed, or Deepened?

### Resolved

The following are definitively settled:

- **No single-axis principle produces KW.** χ² and kac are anti-parallel; face and flow are orthogonal. Five independent single-axis tests confirm this.
- **No weighted combination produces KW.** Twenty-one scalarizations tested, including corrected normalization. All produce trade-offs, none produce KW.
- **KW is not globally Pareto-optimal.** Sixteen dominators exist at Hamming 2–10. The escape mechanism is χ² epistasis.
- **KW is not a basin attractor.** Zero of 600 KW-agnostic descents recover it. Basin radius = 0.
- **The minimum principle count is N=2.** M-preference + sequential anti-repetition, with χ² emergent and asymmetry residual.
- **The construction method was single-pair perturbation.** The 2.2% domination gap at Hamming 2 is the fingerprint.

### Narrowed

The generative question has been narrowed from "what principle?" to "why this specific priority ordering?":

- **Why vocabulary over grammar?** Why does KW defend distributional completeness at ≥2.4× the balanced weight? The answer appears to be: because the sequence is a map, and maps require vocabulary. But this is interpretive, not computational.
- **Why 3 override positions and not 4 or 2?** Pairs 3, 5, and 9 are the M-rule exceptions. Their specific selection (rather than other M-decisive pairs) may reflect the sequential context at those positions or may reflect semantic content computation cannot access.

### Deepened

The investigation discovered that the generative question has a deeper form than originally posed:

- The original question assumed KW was **produced by a principle.** The finding is that KW was produced by **a process** — iterative, multi-scale, simultaneously attentive to local semantics and global flow. The process converges to a specific ridge point because of the topology of the landscape, not because of a rule.
- The gap between algorithm and understanding — "the algorithm is the understanding; the understanding is not an algorithm" — is not a limitation of the investigation but a structural feature of the object. KW encodes understanding in a form that resists algorithmic decomposition because the understanding that produced it was not algorithmic.
- The question "what principle generates KW?" is answered by: "the principle is mutual accommodation under multi-scale attention, applied through single-pair adjustment until locally stable." This is a genuine answer — but it is a characterization of a process, not a specification of an algorithm. Whether that distinction matters depends on what you want the answer for.

---

## 12. Key Results Table

| Finding | Round | Character | Significance |
|---------|-------|-----------|-------------|
| χ²–kac anti-parallelism | 1 | Structural | The central tension; no single-axis solution exists |
| C2 matches KW's m-score (12/16) | 1 | Structural | M-preference may be a shadow of sequential diversity |
| KW dominates 92.8% of random | 1 | Statistical | KW is exceptional but not extreme on any single axis |
| Balanced kernel walk matches χ²+kac | 2 | Structural | Kernel operating point reachable; face signals collapse |
| Asymmetry tie-breaking is vacuous | 2 | Structural | Kernel choices fully determine orientation; no soft preferences |
| Scalarized greedy nearest at Hamming 4 | 2 | Structural | The m–kac trade-off is the residual tension |
| **KW not globally Pareto-optimal** | 3 | Geometric | **16 dominators (Hamming 2–10); 3 core bits (9, 17, 23)** |
| M-rule exceptions protect kac | 3 | Structural | Hierarchy confirmed: kac overrides m at conflict positions |
| Asymmetry is genuinely independent | 3 | Statistical | Not a substrate effect of kernel balance |
| Chi² epistasis enables domination | 3, 4 | Algebraic | Two χ²-improving bits cancel; kac improvements add |
| Only self-targeting recovers KW | 4 | Structural | KW is non-derivable from any simple constructive principle |
| **Round 4 basin attractor was circular** | 5 | Methodological | **The most important single correction** |
| **KW not a basin attractor** | 5 | Geometric | **0/600 agnostic recovery; basin radius = 0** |
| Balanced criterion has 10 attractors | 5 | Geometric | Landscape has strong structure; KW is not among attractors |
| **Vocabulary-over-grammar priority** | 5 | Structural | **Chi² defended at ≥2.4× balanced weight over kac** |
| 3-bit escape manifold | 3–5 | Geometric | 24 bits locked; bits 9, 17, 23 carry the entire question |
| Construction method = single-pair | 3–5 | Methodological | 2.2% gap is the fingerprint of pair-by-pair adjustment |
| Three-way ambiguity is irreducible | 5 | Epistemological | Craft / bounded search / hidden criterion — computationally indistinguishable |
| **Overdetermination** | sage | Structural | Multiple paths converge on KW's neighborhood — natural point |

---

*The investigation's deepest finding is negative in form and positive in content: no algorithm generates KW, but the absence of an algorithm is itself the characterization. KW is the specific configuration where multiple incompatible pressures reach mutual accommodation — a natural point in a multi-objective landscape, arrived at by attentive practice rather than by rule. The computational description is complete. What lies beyond it — whether the algebraic properties are the substance of the design or shadows of a semantic structure — is a question for a different kind of inquiry.*
