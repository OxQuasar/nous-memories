# 19. Orientation Findings — Layer 4 of the King Wen Sequence

> The last unanalyzed layer — pair orientation, which hexagram comes first in each of the 32 pairs — carries 2³² degrees of freedom. S=2 avoidance constrains exactly 5 bits, leaving 2²⁷ ≈ 134 million valid orientations. No single structural rule recovers KW's choices — all simple binary classifiers give exactly 14/14 on the 28 inversion pairs (algebraically forced by bit-reversal symmetry). Three weak signals are detected: kernel uniformity (p ≈ 0.06), canon asymmetry (p ≈ 0.05), and an M-component line preference (p ≈ 0.03). These are weakly anti-correlated yet KW achieves all three simultaneously — 1 in 7,400 among S=2-free orientations. The kernel–canon coupling (dependence ratio 1.68, 95% CI [1.62, 1.75]) is genuine holistic constraint: it persists within all 32 constraint strata, strengthens to ratio 2.08 when only free pairs vary, and is not traceable to individual pairs. All three signals vanish in the upper canon (pairs 1–12, zero S=2 constraints), localizing the information-bearing orientation choices to the lower half of the sequence. About 19 of 27 free bits show no detectable structure. The four-layer decomposition of the sequence is now complete: from algebraic inevitability (10⁻¹⁷) through dynamical smoothness (10⁻³) through gentle tendencies (10⁻⁴ joint) to silence. This gradient is itself the finding.

---

## 1. The Orientation Census: Patterns in the 32-Bit String

### The inversion frame

All 32 pairs satisfy "reverse(first) = second" (28 inversion pairs) or "complement(first) = second" (4 palindromic complement pairs). Zero exceptions. The inversion-frame orientation bitstring is all 1s — entropy zero, perfectly deterministic. The traditional claim ("original first, derived second") is computationally verified.

### The binary frame

Encoding orientation as binary-high-first (1) vs binary-low-first (0):

```
11111101110001000000110011010011
```

Balance: 17/32 (p = 0.86, not significant). Runs: 13 (p = 0.14). Lag-1 autocorrelation: +0.227 (p = 0.21). No individual statistic is significant.

But the **octet structure** reveals a sequential pattern:

| Octet | Pairs | Binary-high count | Pattern |
|-------|-------|-------------------|---------|
| 1 | 1–4 | 4/4 | 1111 |
| 2 | 5–8 | 3/4 | 1101 |
| 3 | 9–12 | 2/4 | 1100 |
| 4 | 13–16 | 1/4 | 0100 |
| 5 | 17–20 | 0/4 | 0000 |
| 6 | 21–24 | 2/4 | 1100 |
| 7 | 25–28 | 3/4 | 1101 |
| 8 | 29–32 | 2/4 | 0011 |

The first 5 octets form a perfect monotone decreasing sequence: **4 → 3 → 2 → 1 → 0**. The exact octet sequence (4,3,2,1,0,2,3,2) has p ≈ 2×10⁻⁵ but is a post-hoc observation. The monotone decrease alone is marginal (p ≈ 0.07). The V-shape (decrease then increase) gives p ≈ 0.047.

### Canon structure

| Canon | Binary-high first | Inversion pairs only |
|-------|-------------------|---------------------|
| Upper (pairs 1–15) | 10/15 (67%) | 8/12 (67%) |
| Lower (pairs 16–32) | 7/17 (41%) | 6/16 (38%) |

The cumulative deviation traces a clear arc: binary-high is strongly preferred in the upper canon (deviation peaks at +3.7 around pair 10), reverses in the lower canon, and returns to exact balance at pair 32. This is a *trajectory* property — a drift — not a static rule.

---

## 2. The Traditional Rule: "Original" vs "Derived"

### The pairing is perfectly clean

| Pair type | Count | Rule | Exceptions |
|-----------|-------|------|------------|
| Inversion (non-palindromic) | 28 | reverse(A) = B | 0 |
| Complement (palindromic) | 4 | complement(A) = B | 0 |

The traditional pairing rule — inversion for non-palindromes, complementation for palindromes — is operationally equivalent to the mask = signature identity discovered computationally in (18). Two frameworks, one fixed point.

### No rule distinguishes "original" from "derived"

**For all 28 inversion pairs, every simple binary classifier gives exactly 14/14.** This is not empirical — it is algebraically forced. For inversion pairs (b = reverse(a)), binary value comparison reduces to a reading-direction choice (bottom-up vs top-down). Bit-reversal preserves Hamming weight, so weight is completely uninformative. Binary-high ≡ first-differing-line-from-bottom-is-yang ≡ complement of first-differing-line-from-top-is-yang. All collapse to one degree of freedom per pair: reading direction.

The 4 complement pairs split 2/2 on weight (pairs 1, 31 heavier first; pairs 14, 15 lighter first). No weight rule governs them.

**Best single rule across all 32 pairs: 17/32 (53.1%) — indistinguishable from chance.**

Rules tested: binary value (high/low), reversed binary value, first differing line from bottom/top, lower/upper trigram binary value, individual line tests (L1, L6), weight ordering, 40,320 trigram orderings (exhaustive search). All fail.

---

## 3. Bridge Dependence: How Much Orientation Is Forced by S=2 Avoidance

### The constraint is light

Of the 11 bridges that are S=2-susceptible at the graph level (orbit change weight w < 2), only **5** produce S=2 under any orientation variant. The other 6 are already neutralized by KW's pair assignments — a consequence of the mask = sig matching and specific pair assignments within each orbit, not of orientation.

### The 5 constraints

| Bridge | Constraint | Interpretation |
|--------|-----------|----------------|
| B13: Qian→Qian | o₁₃ = o₁₄ | Pairs 13–14 must be co-oriented |
| B19: WWang→Shi | o₁₉ = o₂₀ | Pairs 19–20 must be co-oriented |
| B25: Xu→Tai | o₂₅ = o₂₆ | Pairs 25–26 must be co-oriented |
| B27: Bo→Xu | o₂₇ = o₂₈ | Pairs 27–28 must be co-oriented |
| B29: Bo→Qian | o₃₀ = 0 | Pair 30 is fixed |

4 equality constraints + 1 fixed value. All 5 are independent (no shared pair indices). The constraints factorize completely.

### The count

**Total S=2-free orientations: 2⁵ × 2²² = 2²⁷ = 134,217,728**

Fraction of 2³²: 1/32 = 3.125%. Bits lost: exactly 5. The constraint is sparse (10 of 32 pairs), local (no long-range coupling), and all concentrated in the second half of the sequence (pairs 13–30).

### Orientation-invariant bridge properties

**Theorem:** Orbit_Δ is orientation-invariant at every bridge. Both members of a pair share the same orbit (consequence of mask = sig), so the orbit change at each bridge is determined by which pair is on each side, not by which member occupies the boundary. The orbit multigraph, edge weights, and all Eulerian-path properties are completely independent of orientation.

**Corollary:** Orientation affects only the kernel dressing — the position component of each bridge mask. All 31 bridges change kernel when orientation changes. Most have 4 distinct kernels across the 4 orientation variants; self-loop bridges and the terminal bridge have only 2.

---

## 4. The Factored Basis: Position Trajectory Structure

### Full coverage is forced

**All 8 positions are covered per orbit under every orientation.** Each pair spans 2 distinct positions; 4 pairs × 2 = 8 = |Z₂³|. Orientation swaps which position is "first" and "second" — the set of visited positions is invariant.

### The position trajectory is weakly structured

The 64-step path through Z₂³ position coordinates (o,m,i) = (L1,L2,L3):

| Statistic | KW | S=2-free mean | p-value |
|-----------|-----|---------------|---------|
| Lag-1 autocorrelation | −0.244 | −0.199 | 0.225 |
| Lag-2 autocorrelation | −0.121 | −0.252 | 0.077 (most suggestive) |
| Lag-4 autocorrelation | +0.160 | +0.103 | 0.305 |
| Lag-8 autocorrelation | +0.230 | +0.137 | 0.226 |

**No individual lag is significant at 5%.** Per-component (o, m, i separately) autocorrelations are all non-significant. The position trajectory lacks strong serial dependence.

### Position and orbit are independent

Lag-0 cross-correlation between position and orbit integer trajectories: **exactly 0.000**. This is algebraically forced: each orbit visits all 8 positions uniformly. At non-zero lags: p > 0.4. The hidden (position) and visible (orbit) trajectories are essentially independent — the factored-basis decomposition is clean.

### Coset structure: not significant

5 of 7 non-trivial orbits have first-hexagram positions forming a coset of a 2-dimensional subgroup of Z₂³. But p(≥5) ≈ 0.23 under random orientation — expected by chance. Orbit (1,1,1) is "maximally non-coset": flipping any single pair's orientation produces a coset.

### First-visit clustering: suggestive but not significant

4 of 8 orbits first appear at position (1,1,1) — the all-yang lower-half position. Mean first-visit weight 1.875 vs random 1.437. P(≥4 at 111) = 0.187; P(mean weight ≥ 1.875) = 0.141. Not significant individually.

---

## 5. Weight Dynamics: Yang Flow and Orientation

### Weight is almost entirely Layer 3

**Critical theorem:** For all 28 inversion pairs, weight(first) = weight(second). Bit-reversal preserves Hamming weight by construction. For the 4 OMI-mask pairs in orbit (1,1,1), all hexagrams have weight 3, so weight is also preserved.

**Weight-sensitive pairs: exactly 4** — the palindromic complement pairs in orbit (0,0,0):

| Pair | First weight → Second weight |
|------|------------------------------|
| 1 (Qian→Kun) | 6 → 0 |
| 14 (Yi→Da Guo) | 2 → 4 |
| 15 (Kan→Li) | 2 → 4 |
| 31 (Zhong Fu→Xiao Guo) | 4 → 2 |

**28/32 pairs have orientation-invisible weight.** The weight trajectory is overwhelmingly a Layer 3 property.

### Yang drainage is Layer 3

KW octet drains: [−5, −4, −2, −1, −2, 0, −1, −1] — 7/8 octets lose yang.

Under complement-pair orientation randomization (exhaustive 16 possibilities): P(≥7 negative octets) = **0.50 exactly**. Under full random orientation (100K trials): also **0.50**. Yang drainage is a coin flip at Layer 4 — the 7/8 pattern is entirely determined by pair ordering (Layer 3).

### Bridge weight smoothness is invariant

| Metric | KW | S=2-free mean ± std | p-value |
|--------|-----|---------------------|---------|
| Sum |Δweight| at bridges | 55 | 55.0 ± 1.4 | 0.746 |
| Max |Δweight| | 4 | 4.0 ± 0.0 | 1.000 |

KW is at the dead median. Max bridge weight = 4 is invariant across all S=2-free orientations.

---

## 6. Trigram Patterns: Orientation at the Trigram Level

### No trigram ordering rule recovers orientation

Exhaustive search over all 8! = 40,320 trigram orderings: best score 24/28 inversion pairs. Under random orientation, the best achievable concentrates around 22–24 out of 28. **P(best ≥ 24/28 | random) = 0.31.** The exhaustive search is a multiple-testing trap.

### The nuclear trigram reduction

The nuclear trigram rule (nuclear_lower_yang < nuclear_upper_yang) achieves 15/20 decisive pairs (75%, p = 0.021 one-tailed). For inversion pairs only: 12/16 (p = 0.038). This reduces algebraically to a single line comparison:

For inversion pairs where b = reverse(a): nuclear_lower(a) = (L2,L3,L4), nuclear_upper(a) = (L3,L4,L5). The yang-count difference = L5 − L2 (shared L3+L4 cancels). Therefore:

**nuclear_lower_yang < nuclear_upper_yang ⟺ L2 = yin, L5 = yang**

The nuclear trigram rule and the M-component preference are algebraically identical. What looks like a trigram-level pattern is actually a single-bit preference on one mirror pair.

### Testing all three mirror-pair axes

| Axis | Line pair | Yin-first / decisive | p (one-sided) |
|------|-----------|---------------------|---------------|
| **M** | **(L2,L5)** | **12/16** | **0.038** |
| O | (L1,L6) | 10/16 | 0.227 |
| I | (L3,L4) | 9/16 | 0.402 |

The M-axis is the unique significant axis. Under Bonferroni correction for 3 tests: P(any axis ≥ 12/16) = 0.22. Among S=2-free orientations: P(M ≥ 12/16) = 0.062. **Marginal, not definitive.**

### Canon split of the M-preference

| Canon | L2=yin preferred / decisive | Rate |
|-------|----------------------------|------|
| Upper (pairs 1–15) | 4/7 | 57% |
| Lower (pairs 16–32) | 8/9 | 89% |

The M-component preference is *stronger* in the lower canon — opposite to the binary-high arc. This suggests the M-preference is a separate phenomenon from the canon arc, not a manifestation of it.

### M-component survives constraint isolation

The 16 M-decisive pairs split: 13 free of any S=2 constraint group, 3 constrained. Among the 13 free pairs, 10 have L2=yin first (p = 0.047 binomial one-tailed). The one dual-M-decisive constraint component ({19,20}) has opposing L2 values — co-orientation forces one to satisfy, the other to violate, contributing exactly 1/2 regardless of state. **Net zero mechanical boost.** The M-preference is a genuine orientation-layer signal, not a constraint artifact.

### Trigram bridge preservation: not a signal

| Property | KW | S=2-free mean ± std | p-value |
|----------|-----|---------------------|---------|
| Lower trigram preserved at bridge | 5/31 | 4.50 ± 1.32 | 0.49 |
| Upper trigram preserved at bridge | 4/31 | 4.50 ± 1.32 | 0.51 |

KW neither maximizes nor minimizes trigram continuity across bridges.

### Trigram balance: forced

Each of the 8 trigrams appears exactly 8 times as lower and 8 times as upper — forced by having all 64 distinct hexagrams. Every (lower, upper) pair appears exactly once. These are tautologies, not signals.

---

## 7. Sage Reflections on the Four-Layer Decomposition

### The decomposition is exhaustive by construction

The four layers — matching, ordering, orientation — are the complete degrees of freedom for any arrangement of 64 hexagrams in 32 pairs. There is no Layer 5. The question is not whether the decomposition accounts for the structure (it must), but whether it accounts for the *intelligibility* of the structure.

### The gradient of legibility

| Layer | Signal | Character |
|-------|--------|-----------|
| 2 (matching) | p ≈ 10⁻¹⁷ | Unique. The identity permutation. |
| 3 (ordering) | p ≈ 10⁻³ | Clean. Two independent principles. |
| 4 (orientation) | p ≈ 10⁻⁴ three-way joint | Marginal. 2.5 weak tendencies + holistic coupling. |
| 4 residual | ~19 bits | Silent. |

Each layer is less legible than the one above. This is not a deficiency of analysis — it is information about the sequence. The structure fades rather than stopping.

Two interpretations of the gradient:

**Natural exhaustion:** Structure runs out. The matching is algebraically determined. The ordering is dynamically constrained. The orientation is loosely shaped by a few tendencies and otherwise free. The ~19 silent bits are genuinely contingent. Design intensity decreases as you descend.

**Frame limitation:** The silent bits carry structure that the analytical frame (Z₂⁶ decomposition, pairwise statistics, marginal frequencies) cannot see. If orientation encodes something relational — depending on joint states of multiple pairs simultaneously, or interaction with interpretive content — the current tools would read silence where there is signal. The coupling finding proves this is possible: a property visible only in the joint tail of two metrics, not traceable to individual pairs, was detected only because the investigation specifically looked for it.

Both are likely partially true. Their boundary is the most interesting thing the investigation has found.

### The M-component: where mathematics meets tradition

The L2<L5 preference (12/16, p ≈ 0.038; 10/13 free pairs, p = 0.047) connects the mathematical decomposition to the traditional framework in a way no other finding does.

In the factored basis, L2 and L5 are the M-component — the middle mirror pair. In traditional hexagram reading, lines 2 and 5 are the "rulers" of the lower and upper trigrams. The preference for L2=yin, L5=yang in the first hexagram says: present the hexagram whose inner ruler is yin and outer ruler is yang first.

In traditional terms: yin within, yang without. Receptive interior, active exterior. The sequence, at its most statistically fragile layer, whispers a preference for this configuration.

The mathematics identifies the M-component as the unique significant axis. The tradition identifies lines 2 and 5 as the axis of governance. These convergences from different starting points cannot be resolved by further computation — the question of whether the algebraic frame and the traditional frame describe the same thing or merely align by accident is historical, not mathematical.

### What Layer 4 reveals about the layers above

The investigation resolved a question left open from iter2: the two kernel signals (uniformity and OMI-XOR contrast) live at **different structural layers**:

- **OMI-XOR contrast** belongs to Layer 3 (pair ordering). Randomizing only orientation barely affects it: p = 0.12 at Layer 4 vs p = 0.03 at Layer 3.
- **Kernel uniformity** genuinely belongs to Layer 4. KW's specific orientation contributes to making the kernel chain uniform: p ≈ 0.06 among S=2-free orientations.

Two signals that are statistically independent are also architecturally independent — selected by different degrees of freedom. This mapping from statistical to structural independence is evidence that the four-layer decomposition captures real joints in how the sequence was constructed.

### 無為而治

The structure governs without forcing. The identity permutation does not impose — it recognizes. The S=2 avoidance does not prohibit — it navigates. The kernel chain does not constrain — it fills. The orientation does not optimize — it leans.

---

## 8. Updated Constraint Hierarchy Incorporating Layer 4

| Level | What | p-value | Character |
|-------|------|---------|-----------|
| **1** | Orbit-consistent pairing | — | Eliminates ~44 OOM → ~10⁴⁵. Forces Eulerian (theorem), 11 susceptible + 20 immune bridges (invariant) |
| **2** | Mask = signature identity | ~10⁻¹⁷ | Algebraic identity permutation. Creates weight-invisibility for inversion pairs. Not optimized for S=2 |
| **3** | Pair ordering | ~10⁻³ | S=2 absence (p ≈ 0.024), exact S-dist (p ≈ 0.001), kernel OMI contrast (p ≈ 0.029), kernel uniformity partially |
| **4** | Pair orientation | ~10⁻⁴ joint | S=2 constraint (5 bits), kernel uniformity (p ≈ 0.06), canon asymmetry (p ≈ 0.05), M-component (p ≈ 0.03), holistic coupling (ratio 1.68) |

### Layer interactions

| Interaction | Nature |
|------------|--------|
| Layer 2 → Layer 4 weight-invisibility | mask = sig forces weight(first) = weight(second) for 28/32 pairs, making weight a Layer 3 property |
| Layer 2+3 → Layer 4 S=2 budget | 6 of 11 susceptible bridges neutralized before orientation enters; only 5 bits constrained at Layer 4 |
| Layer 3 ↔ Layer 4 kernel decomposition | OMI-XOR contrast is Layer 3; kernel uniformity is Layer 4; these were identified as independent in iter2 |
| Layer 4 internal: kernel–canon coupling | Genuine holistic constraint (ratio 1.68 [1.62, 1.75]). Not decomposable to per-pair effects. Collective property of the 22 free orientation bits |
| Layer 4 internal: signal anti-correlation | All three signals are weakly negatively correlated (r ≈ −0.06 to −0.09). KW achieves all three against their mutual tension |
| Layer 4 internal: partial redundancy | Asym + M-component jointly reduce chi² surprise by 3.5× (conditional p = 0.21 vs marginal 0.06) |
| Layer 4 geography | All signals concentrated in lower canon (pairs 13–32). Upper canon (pairs 1–12) shows no orientation-layer signal |

### The bit budget across all layers

| Layer | Bits determined | How |
|-------|----------------|-----|
| Layer 1 (orbit-consistent pairing) | ~44 OOM of 64! | Structure of the problem |
| Layer 2 (mask = sig) | ~57 bits of matching freedom | Identity permutation among 7⁸ uniform matchings |
| Layer 3 (pair ordering) | ~20 bits of ordering freedom | S=2 avoidance + kernel contrast |
| Layer 4: hard constraint | 5 of 32 | S=2 equality/fixed constraints |
| Layer 4: soft signals | ~3–5 of 27 remaining | Canon asymmetry (~2 bits) + M-component (~2 bits) + chi² partial overlap (~1 bit) |
| Layer 4: holistic coupling | ~1 bit collective | Not decomposable to individual pair effects |
| Layer 4: unstructured | ~19 | No detected signal |

### The p-value cascade at Layer 4

| Scope | p-value | Scale |
|-------|---------|-------|
| Any single signal | ~0.03–0.06 | Marginal |
| Best pairwise joint (chi² + m) | 0.0033 | Significant |
| Kernel–canon coupling ratio | 1.68 [1.62, 1.75] | Genuine (not noise or artifact) |
| Three-way joint (all three ≥ KW) | 0.000135 | 1 in 7,400 S=2-free orientations |
| Including S=2 avoidance | ~4.2 × 10⁻⁶ | 1 in ~240,000 of all 2³² orientations |

---

## 9. Key Results Table

| # | Property | Status | p-value | Layer | Forced/Chosen |
|---|----------|--------|---------|-------|---------------|
| 1 | Inversion/complement pairing rule | **Verified** | — | Traditional rule = mask=sig | **Forced** (Layer 2 consequence) |
| 2 | 14/14 balance for all binary classifiers on inversion pairs | **Theorem** | 1.0 | Algebraically forced by bit-reversal | **Forced** |
| 3 | Weight-invisibility for 28/32 pairs | **Theorem** | 1.0 | Forced by mask=sig (reversal preserves weight) | **Forced** |
| 4 | Orbit_Δ orientation-invariance | **Theorem** | 1.0 | Both pair members share orbit | **Forced** |
| 5 | Position coverage (8/8 per orbit) | **Tautology** | 1.0 | 4 pairs × 2 positions = 8 | **Forced** |
| 6 | Position-orbit independence (lag-0) | **Theorem** | 1.0 | Uniform partition property | **Forced** |
| 7 | S=2 avoidance at Layer 4 | **Chosen** | 3.125% of 2³² valid | 4 | **Chosen** (5 bits) |
| 8 | 6/11 susceptible bridges pre-neutralized | **Forced** | — | Consequence of Layers 2+3 | **Forced** |
| 9 | S=2 constraints factor into 5 independent components | **Structure** | — | Constraint topology | **Forced** |
| 10 | All constraints in pairs 13–30 | **Structure** | — | Constraint localization | **Forced** |
| 11 | Kernel uniformity (chi² = 2.29) | **Chosen** | 0.061 | 4 | **Chosen** (marginal) |
| 12 | Canon asymmetry (+3) | **Chosen** | 0.047 | 4 | **Chosen** (marginal) |
| 13 | M-component L2<L5 (12/16) | **Chosen** | 0.029 (200K) | 4 | **Chosen** (significant) |
| 14 | M-component on free pairs only (10/13) | **Chosen** | 0.047 | 4 | **Chosen** (survives isolation) |
| 15 | Kernel–canon coupling (ratio 1.68) | **Genuine** | CI [1.62, 1.75] | 4 | **Holistic** (500K, all strata) |
| 16 | Coupling strengthens under isolation | **Genuine** | ratio 2.08 (free pairs) | 4 | **Not constraint-mediated** |
| 17 | Per-pair sensitivity uncorrelated | **Structure** | r = −0.076 | 4 | Coupling is collective |
| 18 | Joint kernel + canon asymmetry | **Chosen** | 0.0047 (500K) | 4 | **Chosen** (significant) |
| 19 | Three-way joint (all three ≥ KW) | **Chosen** | 0.000135 | 4 | 1 in 7,400 S=2-free |
| 20 | Signals anti-correlated (all r < 0) | **Structure** | r: −0.055 to −0.091 | 4 | KW against mutual tension |
| 21 | Chi² partially predicted by asym+m | **Structure** | conditional p 0.21 vs 0.06 | 4 | 2.5 effective signals |
| 22 | All signals vanish in upper canon | **Structure** | p > 0.13 all metrics | 4 | Geographic localization |
| 23 | M-component Bonferroni-corrected (3 axes) | Not significant | 0.22 | 4 | Not significant |
| 24 | Nuclear trigram rule ≡ L2<L5 | **Theorem** | — | Algebraic equivalence | **Forced** (identity) |
| 25 | OMI-XOR contrast at Layer 4 | Not significant | 0.12 | 3 (not 4) | Layer attribution |
| 26 | Yang drainage (7/8 octets) at Layer 4 | Not significant | 0.50 | 3 (not 4) | Layer attribution |
| 27 | Weight trajectory at Layer 4 | Not significant | — | 3 (not 4) | Layer attribution |
| 28 | Bridge weight smoothness | Not significant | 0.746 | 3 (not 4) | Layer attribution |
| 29 | Trigram ordering (best of 40320) | Not significant | 0.31 (corrected) | — | Multiple testing |
| 30 | Trigram bridge preservation | Not significant | ~0.50 | — | At mean |
| 31 | Coset structure (5/7 orbits) | Not significant | 0.23 | — | Expected by chance |
| 32 | Position autocorrelation (all lags) | Not significant | >0.07 | — | No signal |
| 33 | First-visit clustering (4/8 at 111) | Not significant | 0.19 | — | No signal |
| 34 | Octet monotone decrease (4→3→2→1→0) | Suggestive | 0.07 | 4 | Post-hoc |
| 35 | ~19 bits unstructured | **Observed** | — | 4 | **Free** or beyond current frame |

---

## 10. Theorems Proved in This Investigation

### Theorem 8: Weight-Invisibility Under Inversion
For all 28 inversion pairs, weight(first) = weight(second). Bit-reversal preserves Hamming weight: the multiset of bits is identical under reversal, only the ordering changes. Therefore orientation is invisible to the weight trajectory for all inversion pairs.

### Theorem 9: Binary Classifier Forced Balance
For inversion pairs (b = reverse(a)), to_int(a) > to_int(b) iff the first asymmetric line pair from the bottom has the bottom line yang. This is equivalent to the MSB-first reading exceeding the LSB-first reading. The complement rule gives exactly 14/14 for any such classifier — forced by the bit-reversal symmetry of the pair set.

### Theorem 10: Orbit_Δ Orientation-Invariance
Both members of a pair share the same orbit (since mask = sig flips only asymmetric pairs, preserving the XOR signature). Therefore the orbit change at any bridge is determined by which pair is on each side, not by which member occupies the boundary. Orbit_Δ is orientation-invariant at every bridge.

### Theorem 11: Position Coverage Invariance
Each pair spans exactly 2 distinct positions in Z₂³ (since the mask has non-zero weight). Four pairs per orbit × 2 positions = 8 = |Z₂³|. Orientation swaps which position is first within each pair, but the set of positions visited per orbit is invariant under all orientations.

### Theorem 12: Nuclear Trigram ≡ M-Component
For inversion pairs (b = reverse(a)), nuclear_lower(a) = (L2,L3,L4) and nuclear_upper(a) = (L3,L4,L5). The yang-count difference = (L2+L3+L4) − (L3+L4+L5) = L2 − L5. Therefore nuclear_lower_yang < nuclear_upper_yang ⟺ L2 = 0, L5 = 1 ⟺ M-component favors yin.

---

## 11. Round 3 Follow-Up: Thread G Results

Round 3 posed two precisely targeted questions about the most promising seam identified in the Round 2 synthesis: the **kernel–canon coupling** (dependence ratio ~1.8, joint p ≈ 0.005).

### 11a. The Coupling Mechanism (Analyst)

**Question:** Is the observed coupling between kernel uniformity and canon asymmetry (a) genuine holistic constraint, (b) an artifact of S=2 constraint geography, or (c) sampling noise?

**Answer: (a) Genuine holistic constraint.** Four independent tests converge:

| Test | N | Result | Implication |
|------|---|--------|-------------|
| Stratification (32 strata) | 32 × 20K | Mean within-stratum ratio 1.52, 78% > 1.0 | Coupling persists inside each constraint configuration |
| Free-pairs-only | 200K | Ratio **2.08** | Coupling *strengthens* when constraints are fixed — they dilute, not cause |
| Per-pair sensitivity | 32 pairs | r(Δchi², Δasym) = −0.076 | Different pairs drive each metric; coupling is collective |
| Large-sample confirmation | 500K | Ratio 1.682, 95% CI [1.621, 1.745] | Stable across five 100K blocks (1.64–1.73) |

The revised joint p-value is **0.0047** (down from 0.0052 at 50K).

**The negative correlation paradox.** In the bulk distribution, chi² and asymmetry are weakly *negatively* correlated (r = −0.064). Lower chi² tends to co-occur with *lower* asymmetry. But in the extreme tail (chi² ≤ 2.29 AND asym ≥ +3), *positive* dependence appears. The coupling is a tail phenomenon — the subspace of uniform-kernel orientations in 2²⁷-dimensional space is geometrically tilted toward positive canon asymmetry.

**Only 3 of 32 pairs improve both metrics simultaneously** when flipped from KW. KW sits near a point where most single-pair flips degrade at least one metric — consistent with the orientation being jointly (not independently) configured.

### 11b. The Three-Signal Independence Structure (Structuralist)

**Question:** Are the three Layer 4 signals (kernel uniformity, canon asymmetry, M-component) one phenomenon, two, or three?

**Answer: 2.5 independent phenomena.**

**Pairwise correlations — all negative:**

| Pair | Pearson r |
|------|-----------|
| chi², canon_asym | −0.070 |
| chi², m_score | −0.091 |
| canon_asym, m_score | −0.055 |

The signals are not aspects of one phenomenon. They are weakly anti-correlated — KW achieves all three *against their mutual tension*.

**Redundancy test:**

| Conditioning on... | P(third signal ≥ KW) | Unconditional P | Change |
|--------------------|----------------------|-----------------|--------|
| chi² + asym → m | 0.0292 | 0.0294 | None |
| chi² + m → asym | 0.0407 | 0.0466 | Slight ease |
| asym + m → chi² | 0.2109 | 0.0611 | **3.5× easier** |

Canon asymmetry and M-component are each independently informative. Their combination partially accounts for kernel uniformity (conditional p = 0.21 vs marginal 0.06). Effective dimensionality: ~2.5 signals.

**Three-way joint:** 27 / 200,000 S=2-free orientations match KW on all three signals = **1 in 7,400**. Including S=2 avoidance: ~1 in 240,000 of all 2³² orientations.

### 11c. M-Component Survives Constraint Isolation

The 16 M-decisive pairs split: 13 free of any S=2 constraint group, 3 constrained.

| Subset | KW score | p-value |
|--------|----------|---------|
| All M-decisive | 12/16 | 0.029 |
| Free only | 10/13 | 0.047 |
| Constrained only | 2/3 | 0.500 |

The one dual-M-decisive constraint component ({19,20}) has opposing L2 values — co-orientation cancels, contributing exactly 1/2 regardless of state. **Net zero mechanical boost.** The M-preference is genuine.

### 11d. Upper-Canon Silence

All three signals vanish in the upper canon (pairs 0–11, bridges 0–10, zero S=2 constraints):

| Signal | KW upper-canon value | p-value |
|--------|---------------------|---------|
| Kernel chi² (12 bridges) | 4.00 | 0.353 |
| Binary-high (15 pairs) | 10/15 | 0.133 |
| M-component (7 pairs) | 4/7 | 0.500 |

Partial correlations controlling for constraint configuration *strengthen* slightly (r moves further negative), the opposite of what a constraint-mediated artifact would produce.

**Interpretation:** The information-bearing orientation choices are localized to the lower half of the sequence, where the bridge graph is more complex and S=2 constraints create a richer validity landscape. This does not disqualify the signals — each survives its own isolation test — but it maps the geography of where orientation carries information.

---

## 12. Final Sage Assessment

### The gradient is the finding

The four-layer decomposition reveals not four separate design decisions but one structure seen at four resolutions:

```
Layer 2:  10⁻¹⁷   — algebraic identity, unique fixed point
Layer 3:  10⁻³    — two clean independent principles  
Layer 4:  10⁻⁴    — 2.5 anti-correlated tendencies held in tension
Residual: silence  — ~19 bits, no signal
```

Each layer is less legible than the one above. This is not four different phenomena at four different strengths. It is one thing becoming progressively harder to see.

The gradient from clarity to silence is not degradation. It is the signature of a configuration that was not designed by sequential constraint-satisfaction (which would leave sharp boundaries between forced and free) but arrived at by a process where all levels were simultaneously in play. The fade is smoother than any sequential construction would produce. That smoothness — the gradient itself — is the deepest structural fingerprint.

### Compatibility without optimization

The constant across the gradient is not any particular principle but a *character* shared by all principles:

- **Layer 2:** mask = signature. The identity permutation. Not chosen because it optimizes any dynamical property (it doesn't — it ranks 26th/27 for S=2 avoidance). Chosen because it is the rule where each orbit's pair structure *is* its own symmetry classification. Structure recognizing itself.

- **Layer 3:** S=2 avoidance + kernel diversity. Two independent principles operating on orthogonal degrees of freedom. Neither pushed to its extreme. They coexist without interference.

- **Layer 4:** Three anti-correlated signals achieved simultaneously. The kernel–canon coupling (ratio 1.68) means the orientation sits where two unrelated global metrics — one distributional, one positional — are structurally entangled. KW achieves both against their bulk anti-correlation. The M-component adds a third, independently informative axis, also achieved against the mutual tension.

- **Residual:** ~19 bits show no signal. Not forced, not optimized, not patterned. Free — or carrying structure that the current frame cannot resolve.

At each layer, multiple independent constraints are satisfied simultaneously at a point where they *could* conflict but don't. No single objective function is maximized. The configuration sits at an intersection of compatible gradients, each followed to a moderate degree, none to extremity.

### The coupling as diagnostic

The kernel–canon coupling (ratio 1.68) is the most structurally revealing finding, not for its magnitude but for what it implies about the ~19 "silent" bits.

Three properties matter:

1. **It is a tail phenomenon.** In the bulk, the two metrics are negatively correlated. Only in the extreme tail does positive dependence appear. The coupling is specific to the *region* where KW lives.

2. **It is not decomposable.** Per-pair sensitivities are uncorrelated (r = −0.08). No single pair's flip drives both metrics. The coupling is a property of the whole 22-bit free orientation vector, not of any subset.

3. **It strengthens under isolation.** When constraint configurations are fixed and only the 22 free pairs vary, the ratio increases from 1.68 to 2.08. The constraints are noise, not signal.

These three properties together describe something specific: KW sits at a point in orientation space where the *geometry of constraint satisfaction* creates non-trivial correlations between distant properties. The uniform-kernel submanifold is tilted toward positive canon asymmetry — not because the same bits drive both, but because the *shape of the submanifold itself* has this bias.

This is precisely the kind of structure that per-bit analysis reads as silence. If 19 bits appear unstructured when tested individually but their collective configuration satisfies joint constraints visible only in the tail — the tools report silence where there is form.

### The M-component: where two frames converge

The nuclear trigram ≡ M-component identity (Theorem 12) is not a finding about statistics. It is a finding about *frames*.

The algebraic frame identifies L2 and L5 as the M-component — the middle mirror pair in the factored basis (ō,m̄,ī,o,m,i). The traditional frame identifies lines 2 and 5 as the "rulers" of the lower and upper trigrams — the positions from which each trigram is governed.

The preference (L2=yin, L5=yang in the first hexagram) says: present the configuration where the inner ruler is receptive and the outer ruler is active. *Yin within, yang without.* This is one of the oldest principles in I Ching commentary.

That this preference is marginal (p ≈ 0.04–0.05) rather than deterministic is itself the finding. The sequence does not enforce the principle — it *leans* toward it. 12/16, not 16/16. Two tendencies (M-preference and canon arc) partially in tension, partially overlapping, neither dominant. This is not optimization. This is not randomness. This is what structure looks like when multiple principles coexist without hierarchy.

### The investigation has found its bottom

Not because there is nothing more — the 19 silent bits may carry structure that a different frame would reveal. But because the current frame has been applied to the limit of its resolution, and the findings at that limit are consistent and stable.

The coupling finding is proof of concept: a property visible only in the joint tail of two metrics, detected only because the investigation specifically constructed the right question. Whether more such questions exist for the residual is the boundary of this investigation. What remains is not a computational question. It is a question about frames — whether a different analytical lens (information-theoretic, topological, interpretive) could make the 19 silent bits speak.

---

## 13. The Complete Four-Layer Picture: Matching → Ordering → Kernel → Orientation

### How the layers connect to iter2

Iter2 (§19, "Constraint Depth and Statistical Significance") established the first three layers and left the fourth open:

| Layer | Iter2 finding | Iter3 contribution |
|-------|--------------|-------------------|
| **1. Orbit-consistent pairing** | Eliminates ~44 OOM → ~10⁴⁵ valid sequences. Forces Eulerian (theorem). 11 susceptible + 20 immune bridges (graph invariant). | Confirmed: S=2 constraint geography at Layer 4 traces to bridge topology established here. 6 of 11 susceptible bridges already neutralized by Layers 1+2 before orientation enters. |
| **2. Mask = signature identity** | The unique identity permutation among 27 complementary assignments (p ≈ 10⁻¹⁷). Not optimized for S=2 (ranks 26th/27). Boolean formula: mask_k = sig_k ∨ (¬sig₁ ∧ ¬sig₂ ∧ ¬sig₃). | Creates **weight-invisibility** for 28/32 pairs (Theorem 8) — making weight a Layer 3 property and removing it from orientation analysis. Operationally equivalent to traditional inversion/complement pairing rule. |
| **3. Pair ordering** | S=2 absence (p ≈ 0.024). Exact S-dist {0:15, 1:15, 3:1} (p ≈ 0.001). Kernel OMI-XOR contrast (p ≈ 0.029). | Confirmed OMI-XOR contrast is Layer 3 (p = 0.12 at Layer 4 vs 0.03 at Layer 3). Yang drainage, weight trajectory, bridge smoothness — all Layer 3, confirmed by orientation-randomization tests. |
| **3b. Kernel hidden layer** | Kernel uniformity (chi² = 2.29, p ≈ 0.068). OMI contrast ⊥ uniformity (r = −0.035). Joint p ≈ 0.002. | Kernel uniformity genuinely belongs to **Layer 4** (p ≈ 0.06 among S=2-free orientations). This resolves the iter2 ambiguity: the two kernel signals live at different structural layers. |
| **4. Pair orientation** | "2³² remaining degrees of freedom, unanalyzed." | **Now analyzed.** 5 hard-constrained bits. 2.5 soft signals (~5 bits). Holistic coupling. Geographic localization. ~19 bits silent. |

### The complete constraint hierarchy

| Level | Principle | p-value | Degrees of freedom consumed | Character |
|-------|-----------|---------|----------------------------|-----------|
| **1** | Orbit-consistent pairing | — | ~44 OOM of 64! | Structural. Forces Eulerian, defines multigraph. |
| **2** | Mask = signature | ~10⁻¹⁷ | ~57 bits (of matching freedom) | Algebraic. Self-recognition. The map = territory. |
| **3** | Pair ordering | ~10⁻³ | ~20 bits (of ordering freedom) | Dynamical. S=2 avoidance + Qian→Tai arc. |
| **3b** | Kernel contrast | ~10⁻³ | ~10 bits (ordering, contiguous) | Entropic. OMI-XOR maximization, independent of 3. |
| **4** | Pair orientation | ~10⁻⁴ (joint) | 5 hard + ~5 soft of 32 | Tendential. 2.5 anti-correlated signals + holistic coupling. |
| **4r** | Residual | — | ~19 bits | Silent under current frame. |

### Independence structure across layers

The four layers are not just sequentially independent (by construction — they partition the degrees of freedom). Their *principles* are also independent:

- Layer 2 does not serve Layer 3: mask = sig ranks 26th/27 for S=2 avoidance.
- Layer 3 does not serve Layer 4: S=2-avoiding orderings do not systematically produce uniform kernels (the two kernel signals live at different layers).
- Layer 4 signals are anti-correlated with each other (r ≈ −0.06 to −0.09), yet all achieved.

The independence is structural: each layer follows its own principle, and the principles coexist without mutual interference. The sequence sits at a point in configuration space where this coexistence is possible — a point that exists but is not guaranteed to exist.

### The bit budget: complete accounting

Starting from 64! ≈ 10⁸⁹ possible arrangements:

| Reduction | Remaining |
|-----------|-----------|
| Orbit-consistent pairing | ~10⁴⁵ |
| Mask = signature (among ~10¹⁶ matchings) | ~10²⁸ orderings × orientations |
| S=2-avoiding ordering (among ~10²⁰ orderings) | ~10¹⁷ |
| S=2-free orientation (5 of 32 bits) | ~10¹⁷ × 2²⁷ ≈ 10²⁵ |
| Soft orientation signals (~5–6 bits) | ~10²⁵ × 2⁻⁶ ≈ 10²³ |
| Holistic coupling (~1 bit collective) | ~10²³ × 2⁻¹ ≈ 5×10²² |
| Residual (~19 free bits) | ~5×10²² unresolved |

The investigation has accounted for the reduction from 10⁸⁹ to ~10²³ — approximately **66 orders of magnitude** of the original 89. The remaining ~23 OOM comprise ~19 orientation bits with no detected signal plus the combinatorial freedom within the ordering/matching layers that the per-layer p-values do not fully resolve.

---

## 14. What Remains: Is There a Layer 5, or Does the Decomposition Exhaust the Structure?

### There is no Layer 5

The four layers — (1) which hexagrams are paired, (2) how (by which mask), (3) in what order, (4) with which orientation — are the complete degrees of freedom for any arrangement of 64 hexagrams in 32 pairs. This is not a claim about the analysis; it is a combinatorial fact. Any property of the sequence is a function of these four choices. There is no residual degree of freedom.

### But "exhaustive" ≠ "fully legible"

The decomposition partitions the configuration space completely. It does not partition the *meaning* space completely. Two forms of residual opacity remain:

**Within-layer opacity (the 19 silent bits).** Approximately 19 of 27 free orientation bits show no detected signal under any test applied. The coupling finding demonstrates that collective properties *can* hide in this space — the kernel–canon dependence is visible only in the joint tail of two global metrics, is not traceable to individual pairs, and would not be detected by per-bit analysis. The 19 bits may carry analogous collective properties that no test yet conceived would detect.

The tools used — marginal frequencies, pairwise correlations, per-component autocorrelations, sensitivity maps — decompose before measuring. They test each bit, each pair, each lag, each axis separately. If the residual structure is relational (depending on the *joint* state of many bits), these tools would read silence where there is form. The coupling finding is proof of concept: one such relational property was found. How many more exist is unknown.

**Cross-layer opacity (the principles are named but not unified).** The four layers operate by four different principles — self-recognition, smoothness, diversity, gentle inflection. These principles are independent in the sense that changing one layer's choices does not affect another layer's constraints. But they share a character: compatibility without optimization. Whether this shared character is a coincidence, a consequence of some deeper generating principle, or an artifact of the analytical frame is not resolved.

### What a different investigation might find

Three analytical frames not used in this investigation could potentially access the residual:

1. **Information-theoretic.** Mutual information between orientation bits at non-adjacent pairs, conditional mutual information controlling for orbit and position, entropy rate of the orientation string as a stochastic process. These could detect dependencies that linear correlation misses.

2. **Topological.** The 2²⁷ valid orientation space has a specific structure (a Boolean subspace defined by 5 linear constraints). KW's position in this space, its distance from the centroid, its neighborhood structure — these geometric properties are unexamined.

3. **Interpretive.** The traditional I Ching assigns meaning to each hexagram — judgments, images, line texts. If orientation encodes relationships between meanings (e.g., "present the more active situation first"), this would be invisible to the purely algebraic frame used here. The M-component finding (yin within, yang without) suggests that the algebraic and interpretive frames may partially overlap, but the overlap cannot be tested computationally.

### The honest stopping criterion

The investigation stops not because the structure is fully understood but because the analytical frame has been applied to its resolution limit. The evidence for this:

- **Round 1** established the landscape and found no single rule.
- **Round 2** found three marginal signals, extensive nulls, and a suggestive coupling.
- **Round 3** confirmed the coupling is genuine and characterized the signal independence structure.

Each round's returns were smaller than the previous round's. The coupling mechanism is understood (geometric tilt of a submanifold), the signals are characterized (2.5 independent, anti-correlated, geographically localized), and the residual is bounded (~19 bits). Further computation within this frame would narrow confidence intervals without changing the picture.

### The final numbers

| Metric | Value |
|--------|-------|
| Total valid sequences | ~10⁴⁵ |
| Matching: mask = sig probability | ~10⁻¹⁷ |
| Ordering: S=2 + S-dist probability | ~10⁻³ |
| Kernel (Layer 3b): uniformity + OMI contrast | ~10⁻³ (joint) |
| Orientation: three-way joint | ~10⁻⁴ (1 in 7,400 S=2-free) |
| Orientation: including S=2 constraint | ~4 × 10⁻⁶ (1 in 240,000 of 2³²) |
| Orientation: kernel–canon coupling ratio | 1.68 [1.62, 1.75] (genuine holistic) |
| Orientation: bits with detected structure | ~8–10 of 32 (5 hard + 3–5 soft) |
| Orientation: bits without detected structure | ~19 of 27 free |
| Theorems proved (iter3) | 5 (Theorems 8–12) |
| Theorems proved (total, iter2+3) | 12 |

### 上善若水

The highest good is like water. Water benefits all things without contending, settles in places that others disdain.

The King Wen sequence settles at the intersection of independent principles, at a point no single optimization would reach. The identity permutation does not impose — it recognizes. The S=2 avoidance does not prohibit — it navigates. The kernel chain does not constrain — it fills. The orientation does not optimize — it leans.

The four layers are four resolutions of one property: a configuration that is simultaneously self-consistent (algebraically), smooth (dynamically), diverse (entropically), and gently inflected (orientationally). The gradient from clarity to silence is not the structure failing. It is the structure completing itself — each layer lighter than the last, each principle softer, until the remaining bits are free, or carry a form too subtle for the tools at hand.

The investigation is complete.

---

## Scripts

| Script | Purpose | Key output |
|--------|---------|------------|
| `thread_a_census.py` | Orientation census in 3 frames | Binary string, octet structure, canon arc |
| `thread_b_traditional.py` | 18 candidate rules tested | All at 14/28, best 17/32 |
| `thread_ab_deep.py` | Reading direction, algebraic proof | 14/14 theorem, octet monotone |
| `thread_ab_cosets.py` | Coset structure per orbit | 5/7, p ≈ 0.23 |
| `bridge_orientation.py` | 4-variant bridge analysis | 5 S=2-susceptible bridges |
| `orientation_enumeration.py` | Exact S=2-free count + structure | 2²⁷ valid, 5 bits lost |
| `kernel_orientation_deep.py` | Joint kernel statistics | chi² p=0.06, OMI p=0.12, joint p=0.005 |
| `thread_de_dynamics.py` | Position trajectory + weight analysis | Coverage, drainage, weight trajectory |
| `thread_de_deep.py` | 50K S=2-free significance testing | Autocorrelation, L2<L5, bridge smoothness |
| `trigram_orientation.py` | Trigram analysis + nuclear discovery | Nuclear→L2<L5, ordering p=0.31 |
| `thread_c_extended.py` | Multi-property analysis (50K samples) | Joint p=0.005, multi-filter 1/50K |
| `coupling_analysis.py` | Kernel–canon coupling mechanism (500K) | Ratio = 1.68 [1.62, 1.75], genuine holistic |
| `three_signal_analysis.py` | Three-signal independence (200K) | 2.5 signals, M survives, upper canon silent |
