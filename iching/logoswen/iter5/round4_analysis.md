# Rounds 3–4 Theorist Analysis: What the Dominators Reveal

## 1. The Central Discovery and Its Implications

**KW is not globally Pareto-optimal, but it is a basin attractor.** These two facts together are more informative than either alone. They reframe the entire generation question.

The old question was: "What principle produces a Pareto-optimal orientation?" The new question is: "What construction process converges to KW's specific basin rather than a dominator basin?"

This is a sharper, more tractable question. It transforms the investigation from an optimization problem (find the right objective) to a dynamical systems problem (characterize the basin of attraction).

---

## 2. What the Dominators' Structure Reveals

### 2a. The Dominator Anatomy

16 dominators were found up to Hamming ≤8. Their bit composition tells a precise story:

| Core bit | Pair(s) | Frequency | Single-bit profile | Role in domination |
|----------|---------|-----------|-------------------|-------------------|
| **17** | 21 (Lin/Guan) | 15/16 | Δχ²=−1.032, Δkac=+0.003 | Gateway: near-zero kac cost enables epistatic pairing |
| **9** | 9 (Xiao Chu/Lü) | 15/16 | Δχ²=−0.516, Δkac=+0.015 | χ² donor: provides chi² improvement for cancellation |
| **23** | (19,20) component | 13/16 | Δχ²=+4.129, Δkac=−0.111 | kac engine: strongest kac improvement, massive χ² cost |

**The dominator recipe is:**
1. Start with bit 17 (near-free gateway)
2. Add bit 9 or another χ²-improving bit (provides χ² credit)
3. Add bit 23 (converts χ² credit to kac improvement via epistatic cancellation)

This is a three-ingredient cooperative mechanism. No single ingredient works alone:
- Bit 17 alone: tiny kac cost, but no kac benefit
- Bit 9 alone: improves χ² but worsens kac
- Bit 23 alone: catastrophically worsens χ² (×1.8) while improving kac
- Bits {9, 23} together: χ² changes partially cancel; kac improvements add
- Bits {17, 26} together: simplest escape — both have small Δkac that happen to combine additively while χ² changes cancel exactly

### 2b. The Epistasis Mechanism

The key insight: **χ² is quantized in steps of 0.516 and epistatically coupled.** Individual bits move χ² by integer multiples of 0.516. But combinations can cancel. The cancellation is not random — it occurs when two bits push the kernel histogram in complementary directions: one shifts {id, O} ↔ {I, OI} and the other reverses the shift.

For the Hamming-2 dominator: both flips perform the same kernel transformation (OI→I, O→id) at different sequence positions. The histogram changes are {id+2, O−2, I+2, OI−2} — two types gain, two types lose by the same amount. The χ² contributions are symmetric, producing exact cancellation.

This is a **resonance** in the kernel histogram space. It requires:
1. Two sequence positions with similar algebraic neighborhood structure
2. Orientation flips that produce the same kernel transformation at both positions
3. The resulting histogram changes being complementary (one up where the other is down)

### 2c. The kac Improvement Mechanism

Unlike χ², which requires careful epistatic cancellation, **kac improvements are nearly additive** (5% median nonlinearity from iter4). Each bit's kac contribution is largely independent. The dominators improve kac simply by accumulating multiple small improvements.

This asymmetry — χ² requires coordination, kac is additive — is why single-bit greedy can't escape. Each individual bit worsens kac (for KW-dominated bits) or worsens χ² (for the kac-improving bits 16, 23). The only escape route is a cooperative move that simultaneously handles both metrics.

---

## 3. The Basin Attractor Finding

### 3a. What "Fixed Point of Self-Targeting" Means

Round 4's most striking result: forward greedy L1 descent, targeting KW's exact metric profile, recovers KW from both processing directions (0→31 and 31→0). No other single-objective or balanced-weight greedy recovers KW.

**This means KW is not the output of any simple optimization.** It's the unique orientation where every individual pair's choice is simultaneously the locally optimal one given all other pairs' choices. This is a Nash equilibrium reading: no player (pair) wants to unilaterally deviate.

But Nash equilibria can be suboptimal (the Prisoner's Dilemma analogy). KW is a coordination equilibrium where each pair's choice makes sense given the others, but a coordinated multi-pair deviation could improve the collective outcome. This is exactly what the dominators are — coordinated deviations that no single pair would choose.

### 3b. Path Independence is the Key Structural Feature

That forward and reverse processing both recover KW is remarkable. It means KW is not an artifact of processing order. Whichever direction you sweep through the pairs, making the locally best choice at each step, you arrive at the same orientation.

This is strong evidence for a **consistent local rule**. A human arranger, making pair-by-pair decisions in any order, would converge to KW if they were optimizing the same implicit objective at each step. The rule doesn't depend on the order you apply it — it depends on the orientation state of the whole configuration, evaluated locally at each pair.

### 3c. The Basin Separation Is Topological

KW and the Hamming-2 dominator cannot reach each other via single-bit descent. This is because the χ² epistasis that enables domination also creates a barrier. To move from KW to the dominator:
- Flip bit 17 first: χ² drops by 1.032 (improvement), but the intermediate state has kac=−0.461 (very slight worsening). The L1 distance to KW's profile *increases* because χ² moves away from KW's value.
- Flip bit 26 next: this completes the domination, but the first flip made the intermediate look *worse* by the L1 metric targeting KW.

The barrier is metric-structural: the intermediate state looks worse than both the starting point and the destination. This is a saddle in the single-bit landscape.

---

## 4. Scale Separation: Fully Confirmed and Extended

### 4a. Updated Scale Map

| Scale | Metric | Additivity | Dominator behavior | Construction implication |
|-------|--------|-----------|-------------------|------------------------|
| **Per-pair (local)** | asym | Perfect | Exactly preserved (all 16 have asym≥3) | Local choice, no coordination needed |
| **Per-pair (local)** | m_score | Perfect | Exactly preserved (all 16 have m=12) | Local choice, no coordination needed |
| **Sequential (nearest-neighbor)** | kac | Near-perfect | Additive improvement across flips | Sequential awareness suffices |
| **Global (histogram)** | χ² | Epistatic | Requires coordinated cancellation | Global awareness needed |

**The dominator mechanism operates at the boundary between scales.** The local axes (asym, m_score) are automatically preserved because the dominator bits don't affect M-decisive pairs or asymmetry balance. The sequential axis (kac) improves additively. Only the global axis (χ²) requires the cooperative cancellation mechanism.

### 4b. Hierarchy Implication

The dominators reveal that the four axes separate into two groups by the type of construction awareness they require:

**Group A: Locally decidable** (axes 2 and 3)
- Each pair's contribution is independent
- A per-pair rule suffices
- M-rule + asymmetry preference = complete

**Group B: Contextually decidable** (axes 1 and 4)
- Each pair's contribution depends on neighbors (kac) or the whole sequence (χ²)
- A per-pair rule is necessary but not sufficient
- Sequential awareness (kac) and global histogram awareness (χ²) compete

KW resolves Group A trivially (M-rule covers m_score; asymmetry preference covers asym). The entire generative difficulty lies in Group B: the χ²-kac tension.

---

## 5. The Gap Analysis: What's Left

### 5a. The M-Rule Exception Pattern — Now Fully Explained

Round 3 showed that KW's 4 M-rule exceptions all protect kac:
- Pairs 3, 5, 9: flipping to M-rule would worsen kac by +0.015 to +0.163
- Pair 20: forced by S=2 constraint

But Round 4's M-rule+kac-override test went further: with an override threshold of Δkac > 0.01, the algorithm overrides at 8 positions (not just 4), producing Hamming distance 2 from KW but with worse asym and m_score.

**The M-rule is not the primary generative rule.** It's a secondary preference that is active only when it doesn't conflict with the primary constraint (kac preservation). KW's construction hierarchy is:
1. S=2 constraint (hard, structural)
2. kac-preservation (primary soft, sequential)
3. M-preference (secondary soft, per-pair)
4. Asymmetry preference (tertiary soft, per-pair with half-sequence awareness)

But this hierarchy cannot be the full story, because applying rules 1–3 alone (with kac override threshold 0.01) produces an orientation that deviates from KW on asym and m. The rules are not independent — they interact.

### 5b. What No Generator Has Reproduced

Across 4 rounds, ~50 distinct generators have been tested. None produces KW's full 4-axis profile. The closest approaches:

| Generator | Axes matched | Missing | Why |
|-----------|-------------|---------|-----|
| R2-C (0.3/0.7) | χ², kac (≈) | asym, m | Kernel-chain optimization ignores face |
| R2-Ef strong kernel | asym (≈), kac (≈) | χ², m | Scalarization can't balance 4 axes |
| SA-L1 targeting KW | all 4 exactly | — | Circular: uses KW as target |
| Forward greedy L1-to-KW | all 4 exactly | — | Circular: uses KW as target |

**The only generators that reproduce KW are those that use KW itself as the target.** This is the deepest finding. It means KW is not derivable from any simple constructive principle we've tested — it's a fixed point that can only be characterized self-referentially.

### 5c. The 2.2% Gap

The Hamming-2 dominator improves kac by 0.010 (2.2%). Is this gap meaningful?

**Arguments it's noise:**
- The kac difference is within the noise floor of any felt-sense construction
- A human arranger couldn't distinguish kac=−0.464 from kac=−0.474
- The S-distribution shifts slightly ({0:15, 1:15, 3:1} → {0:16, 1:14, 3:1})

**Arguments it's structural:**
- The dominator requires a 2-step cooperative move invisible to single-pair perturbation
- KW's S-distribution {0:15, 1:15, 3:1} is more symmetric than the dominator's {0:16, 1:14, 3:1}
- Most dominators (14/16) eliminate the S=3 bridge at position 15 — only KW and 2 dominators preserve it

The strongest candidate for why KW stays at its position: **S-distribution aesthetics.** The {15, 15, 1} split is visually symmetric (equal counts of S=0 and S=1, with one exceptional S=3). The dominator breaks this symmetry to {16, 14, 1}. If the arranger valued the aesthetic balance of transition types, they would prefer KW's position.

But this is speculative. The data cannot distinguish between "KW's position reflects a 5th criterion" and "KW's position reflects the limits of single-pair perturbation as a construction method."

---

## 6. The Nature of the Object

### 6a. Three Possible Readings

**Reading 1: KW is the output of a consistent local rule, period.**
The basin attractor finding supports this. KW is the Nash equilibrium of a game where each pair chooses its orientation to optimize a multi-axis objective given all other pairs' choices. The "generative principle" is the implicit objective function at each pair. The dominators represent coordinated deviations that the arranger's local process couldn't discover.

**Reading 2: KW is one of ~32 equally valid configurations on the Pareto frontier.**
The bit budget analysis (iter4) estimated ~2⁵ = 32 orientations on the Pareto surface. KW is one; the dominators are some of the others. The specific selection among these ~32 is contingent — determined by the arranger's starting point and process, not by structural principle. The 19 "residual" bits from iter3 are the navigational choices within this narrow frontier.

**Reading 3: KW reflects a principle we haven't measured.**
The S-distribution, the S=3 bridge at the upper/lower canon boundary, or some other structural feature is an unmeasured axis that distinguishes KW from the dominators. Each round has discovered a new axis (iter4: kac; now: S-distribution?). The pattern may continue.

### 6b. Which Reading the Evidence Favors

**Reading 1 is the most parsimonious.** It explains:
- Why KW is recoverable from both processing directions (consistent local rule)
- Why the dominators exist but are basin-separated (local rule has blind spots at cooperative scales)
- Why no simple generator reproduces KW (the rule is implicit, not a named optimization target)
- Why the domination gap is small (2.2% — the resolution limit of local construction)

Readings 2 and 3 are not excluded but require additional assumptions.

---

## 7. Refinement Proposals for Round 5

### Proposal R5-A: Basin Topology Mapping
Trace all single-bit descent paths from each of the 16 dominators. Do they all converge to KW, or do some converge to other attractors? If there's a single universal attractor (KW), the basin attractor finding is maximally strong. If there are multiple attractors, the landscape has more structure than we know.

### Proposal R5-B: Two-Step Escape Classification
Enumerate all C(27,2) = 351 two-bit combinations from KW. For each, compute all 4 metrics. Classify each into: dominates KW, dominated by KW, trade-off. This completes the Hamming-2 neighborhood exhaustively and tells us whether the single dominator at Hamming 2 is unique or one of several.

### Proposal R5-C: S-Distribution as 5th Axis
Add S-distribution symmetry as a 5th metric. Specifically: define S_sym = |count(S=0) − count(S=1)|. KW has S_sym = 0 (perfect symmetry). Recompute the Pareto analysis with this 5th axis. Does it eliminate any dominators? If it eliminates all but KW, we've found the missing criterion.

### Proposal R5-D: Reverse-Engineer the Implicit Objective
Given that L1-to-KW greedy recovers KW, the "objective" is the L1 distance to KW's profile. But this is circular. Instead: search for the simplest function f(χ², asym, m, kac) such that greedy forward optimization of f recovers KW. Test candidates:
- f = χ² − α·asym − β·m + kac (linear)
- f = max(χ²/c₁, −asym/c₂, −m/c₃, kac/c₄) (minimax)
- f = χ² + kac (ignore face axes)
- f = w₁χ² + w₂kac subject to asym ≥ 3, m ≥ 12 (constrained)

If any of these recover KW without using KW's values explicitly, that function *is* the generative principle.

### Proposal R5-E: Construction Process Simulation
Simulate a human-like construction process:
1. Start with default orientation (all zeros)
2. Repeatedly sample a random pair, try flipping it
3. Accept if the flip improves some implicit criterion; reject otherwise
4. Run for many iterations
5. Vary the criterion and see which converges to KW

This tests whether a stochastic Metropolis-like process (more humanly plausible than greedy) can reach KW from a random start, and what acceptance criterion is needed.

---

## 8. The Current Best Understanding

### The Generative Story (Revised)

KW's orientation was not produced by optimizing a single explicit metric. It was produced by a consistent local process — something like:

> For each pair, choose the orientation that "feels best" given the current state of all other pairs. Iterate until stable.

The "feels best" criterion integrates:
1. **M-preference** (yin within, yang without — L2=yin first): the dominant per-pair rule, active at 12/16 decisive positions
2. **Sequential smoothness** (kernel diversity, anti-repetition): the override rule that reverses the M-preference at 3 positions where it would create kernel-chain clumping
3. **Asymmetry awareness** (upper-high-first preference): a weak directional preference concentrated in the lower canon
4. **Distributional balance** (kernel histogram uniformity): an emergent property, not directly targeted, arising from the interaction of the above three

The process is self-consistent: applying it from any starting point converges to the same orientation. But it has a blind spot at the 2-step cooperative scale — it can't discover that flipping two specific pairs simultaneously would improve kac by 2.2% while preserving everything else.

### What This Means for "the Principle"

**N = 2 load-bearing principles, plus 1 emergent constraint.**

1. **M-preference** (per-pair, local): determines ~12 of 16 decisive pair orientations
2. **Sequential anti-repetition** (nearest-neighbor, contextual): overrides M-preference at 3–4 positions; determines the remaining ~11 non-decisive pair orientations
3. **Distributional uniformity** (global, emergent): not a separate principle but a consequence of (2) when moderated by (1)

Asymmetry (+3) is the weakest signal and may be a by-product of (1) and (2) rather than an independent principle. But this hypothesis hasn't been tested.

### Parsimony Score

**N = 2** is the current minimum principle count. This is better than N = 4 (one per axis) but worse than N = 1. Whether N = 1 is achievable depends on whether proposals R5-D or R5-E can find a single implicit objective that recovers KW. The self-targeting finding (L1-to-KW = KW) proves such an objective *exists* but hasn't identified it in non-circular terms.

---

## 9. Summary for the Captain

**Rounds 3–4 established:**
1. KW is not globally Pareto-optimal — 16 dominators exist, closest at Hamming 2
2. The domination mechanism is χ² epistatic cancellation + additive kac improvement
3. KW IS a basin attractor — forward greedy L1 from both directions recovers it exactly
4. Basin separation is real — KW and dominators can't reach each other via single-bit descent
5. The construction hierarchy is: S=2 constraint → kac-preservation → M-preference → asymmetry awareness
6. No non-circular generator reproduces KW — only self-targeting works

**The question for Round 5:** Can we identify the implicit objective function that makes KW the unique attractor? This is the final step toward the generative principle. If found, it completes the investigation. If not found, the finding itself (KW is a self-consistent equilibrium of multiple simultaneous principles, with no simpler characterization) is the answer.

**The most promising tests:** R5-D (reverse-engineer the objective) and R5-C (S-distribution as 5th axis). These attack the problem from opposite directions — one seeks the rule, the other seeks the missing measurement.
