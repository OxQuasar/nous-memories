# Opposition Theory: Quantifying Oppositeness Across Scales

## Core Observation

The principle of opposites — 0 or 1, and the change between opposing states — is the generative principle of the I Ching. At every scale from n=1 (yin/yang) to n=6 (hexagrams), binary opposition creates structure. The King Wen sequence embeds this principle across multiple axes simultaneously.

The four algebraic axes already measured (χ², asymmetry, M-score, kac) are oppositeness measures, not labeled as such. This document reframes the investigation's findings as a theory of opposition and proposes a scale-by-scale analysis from n=2 through n=6.

---

## The Pairing Rule Across Scales

At each scale n, the 2ⁿ states admit a pairing — a partition into 2ⁿ⁻¹ pairs. The traditional pairing is:

**n=3 (trigrams):** Complement (flip all bits). All four pairs at maximum Hamming distance (3). Heaven/Earth, Thunder/Wind, Water/Fire, Mountain/Lake. The Shuo Gua pairs.

**n=6 (hexagrams):** Reversal (180° rotation) for 28 non-palindromic pairs, complement for 4 palindromic pairs. Algebraically: mask = signature identity (Layer 2).

The two rules look different but are both forms of opposition:
- At n=3, opposition = value inversion (complement). Every yin becomes yang.
- At n=6, opposition = structural inversion (reversal). Inner becomes outer, each trigram is mirrored. For palindromic trigrams, structural inversion collapses to value inversion.

The 180° rotation at n=6 is a compound opposition: swap inner/outer trigrams + reverse each trigram internally. From the trigram frame, this is positional opposition composed with the n=3 reversal operation (which, at n=3, was the *rejected* pairing in favor of complement). The hexagram pairing rule absorbs the trigram-level reversal as a component of a larger opposition.

---

## Five Oppositeness Measures

### 1. Opposition Strength (global)

Total Hamming distance across all pairs: Σ w(aᵢ ⊕ bᵢ).

Measures the raw amount of opposition the pairing embeds. Complement saturates this (every bit flips in every pair). At n=3, the traditional pairing maximizes opposition strength — all four pairs at distance 3, total = 12 = maximum.

At n=6, mask = signature identity fixes opposition strength by orbit. Signature (1,1,1) orbits contribute distance 6 per pair (full opposition), signature (1,0,0) orbits contribute distance 2 (minimal opposition). The total is determined by orbit structure, not freely optimized.

**Key constraint:** At n=3, maximum opposition strength and algebraic self-consistency are compatible. At n=6, they diverge — the tradition chose algebraic identity (mask = signature) over maximizing raw oppositeness. Note: this is not a strength-diversity trade-off (the two are orthogonal) but a choice between algebraic equivariance and combinatorial freedom. Among random pairings, KW achieves 99.98th percentile strength; among equivariant pairings, KW is the unique strength-maximizer within the weight-preserving (all-reversal) subfamily — see Phase 2 below.

### 2. Opposition Diversity

Entropy of the XOR mask distribution across pairs.

Measures how many types of opposition the system uses. At n=3 it's trivial — one mask type (111) for all four pairs. At n=6, this is essentially kernel uniformity (χ²): are the generator types {id, O, M, I, OM, OI, MI, OMI} evenly distributed across bridges?

Higher diversity = the system employs varied forms of opposition rather than repeating one type.

### 3. Sequential Opposition Variety

Autocorrelation of consecutive opposition types across the sequence.

This is kac (kernel autocorrelation). Consecutive bridges almost never repeat the same kernel dressing. The system demands that each transition opposes in a *different way* from its predecessor. Anti-repetition of opposition type.

### 4. Opposition Balance

Directional preferences within the opposition structure.

This is M-score (L2=yin preference within pairs) and asymmetry (canon-level ordering preference). These measure whether the oppositions tilt systematically — whether condition→consequence has a directional signature.

### 5. Weight Complementarity

Correlation of yang-count between pair members.

For reversal pairs: weight is preserved (both members have the same yang count). Opposition changes structure without changing weight. For complement pairs: weight is maximally anti-correlated (w + w' = n). Opposition inverts value directly.

At n=3, the traditional (complement) pairing gives perfect weight anti-correlation. At n=6, only 4 of 32 pairs show weight anti-correlation; the other 28 have zero weight difference. The weight axis of opposition is mostly silent at n=6 — structure carries the opposition instead.

---

## Scale Analysis: Where Opposition Becomes Costly

### n=2: 4 states, 1 mirror pair

Reversal and complement produce the same pairing. Opposition is trivially free — no tension between any measure.

### n=3: 8 states, 1 mirror pair + center line

Reversal and complement diverge on non-palindromic states. Tradition chose complement (maximum opposition strength). Opposition diversity is trivial (one mask type). No trade-off yet — maximum opposition and algebraic coherence coexist.

The palindromes (Heaven, Earth, Water, Fire) are self-symmetric under reversal but not under complement. The non-palindromes (Thunder, Mountain, Wind, Lake) separate the two operations. Tradition pairs Thunder/Wind and Mountain/Lake (complement), not Thunder/Mountain and Wind/Lake (reversal). Nature-opposition over positional-mirror.

### n=4: 16 states, 2 mirror pairs (L1↔L4, L2↔L3), Z₂²

Exhaustive analysis: all 2,027,025 pairings enumerated, 4 measures computed. Full details in `n4/results.md`.

**Structure:** 6 orbits under Z₂² (4 of size 2, 2 of size 4). 4 palindromes, 4 comp∘rev-fixed states. Both reversal and comp∘rev have fixed points — neither yields a valid complete pairing alone. Only complement produces a valid pairing from a single operation.

**Strength ↔ Diversity: exactly uncorrelated.** Pearson r = 0 to machine precision, across all 2,027,025 pairings. Same holds at n=3 (r = 0 across 105 pairings). The predicted "trade-off" between concentration and distribution does not manifest as a global anti-correlation — the measures are orthogonal degrees of freedom.

**Boundary constraint, not trade-off.** The maximum achievable diversity is capped at extreme strength: D_max = 0 at S=32, rising through D_max = 2.75 at S=24, reaching the theoretical maximum D = 3.0 = log₂8 at S ≤ 22. The feasible region in S×D space is lens-shaped. The 2D Pareto frontier is a 6-point staircase along the upper-right boundary of this lens.

**Complement pairing:** uniquely maximizes strength (S=32, only 1 of 2M pairings). Zero diversity. Perfect weight anti-correlation (r = −1). On every Pareto frontier. The extreme of concentrated opposition.

**KW-style (reversal + complement for palindromes):** S=24, D=1.5, only 3 mask types. Not on any Pareto frontier — dominated by 23,632 pairings. Fully Z₂²-equivariant (one of only 117 such pairings). The structural problem: n=4 reversal pairs all have Hamming distance exactly 2 and contribute only 2 mask types. Reversal at n=4 is too uniform to generate diversity.

**Weight tilt partially degenerate** — only 5 distinct values across 2M pairings. Not a useful independent measure at this scale.

### n=6: 64 states, 3 mirror pairs (L1↔L6, L2↔L5, L3↔L4), Z₂²

100K random pairings sampled; exact measures for KW and Shao Yong. Full details in `n6/results.md`.

**Structure:** 20 orbits under Z₂² (8 of size 2, 12 of size 4). 8 palindromes, 8 anti-palindromes (comp∘rev-fixed). Same constraint as n=4: only complement yields a valid complete pairing from a single operation.

**KW pairing is extreme on every axis among random pairings.** Strength 120 (99.98th percentile of random), diversity 2.750 (below the minimum of 100K random pairings), weight tilt 0.375 (below random minimum), weight correlation +0.516 (97.65th percentile). Fully Z₂²-equivariant — a property shared by 0 of 10K random samples. Among equivariant pairings, KW is at the 80th percentile for S and 4th percentile for D — not extreme, but uniquely characterized by weight-preservation priority (see Phase 2).

**The 7-mask structure.** KW uses exactly the 7 nonzero elements of Z₂³ (the mirror-pair signature group): {100001, 010010, 001100, 110011, 101101, 011110, 111111}. Distribution: [8,4,4,4,4,4,4]. Mask = orbit signature. This is the algebraic self-consistency identified in the KW studies — each pair's XOR mask is determined by which mirror pairs (O, M, I) differ between the two hexagrams.

**S↔D orthogonality holds.** r(S,D) = −0.002 from 100K sample (sampling error ~0.003). The structural orthogonality observed at n=3 and n=4 persists at n=6.

**Phase transition from n=4.** KW goes from dominated (n=4: 75th percentile strength among all pairings, not on any Pareto frontier) to extreme (n=6: 99.98th percentile strength among random pairings). The mechanism: at n=4, reversal pairs have fixed distance 2 and only 2 mask types. At n=6, reversal pairs span distances {2, 4, 6} and generate all 7 signature mask types. The Z₂³ signature group is only fully expressible at n ≥ 6 (where there are 3 independent mirror pairs).

**Algebraic diversity ceiling.** KW's diversity of 2.750 looks low against the random floor of 3.78 (combinatorial space admits 63 mask types). But measured against the algebraic ceiling — the maximum entropy using only signature masks — it's near-optimal. The ceiling is log₂7 ≈ 2.807 (all 7 masks equally used); KW achieves 2.750 (98% of ceiling). The deviation is entirely from the 111111 mask getting 8 pairs instead of 4, because 4 non-palindromic reversal pairs accidentally coincide with complement pairs (the comp∘rev-fixed states).

**The four measured axes** (χ², asymmetry, M-score, kac) from the KW studies quantify opposition properties within the *orientation and ordering* degrees of freedom — the choices made after the pairing is fixed. The pairing itself is what the present analysis characterizes.

--------------------------------------------------------------------------------------------------------

## Fu Xi vs King Wen at n=3: Concentrated vs Distributed Opposition

The two traditional trigram arrangements encode the same 8 states but organize opposition differently.

### Diametric pairings (opposite positions on the circle)

**Fu Xi pairs** (all complement):

| Pair | Binary | XOR | Distance |
|------|--------|-----|----------|
| Heaven / Earth | 111 / 000 | 111 | 3 |
| Thunder / Wind | 100 / 011 | 111 | 3 |
| Water / Fire | 010 / 101 | 111 | 3 |
| Mountain / Lake | 001 / 110 | 111 | 3 |

**KW pairs** (opposite positions on Later Heaven circle):

| Pair | Binary | XOR | Distance |
|------|--------|-----|----------|
| Li / Kan | 101 / 010 | 111 | 3 |
| Kun / Gen | 000 / 001 | 001 | 1 |
| Dui / Zhen | 110 / 100 | 010 | 1 |
| Qian / Xun | 111 / 011 | 100 | 1 |

| Measure | Fu Xi | KW |
|---------|-------|----|
| Opposition strength (Σ dist) | 12 (maximum) | 6 (half) |
| Opposition diversity (distinct masks) | 1 of 4 possible | 4 of 4 (maximum) |
| Sequential variety (mask repetition) | zero (all identical) | perfect (all distinct) |
| Weight complementarity (correlation) | r = −1 (perfect anti-corr.) | r ≈ +0.66 (positive corr.) |
| Weight difference | 3, 1, 1, 1 (mean 1.5) | 1, 1, 1, 1 (uniform) |

Fu Xi saturates opposition strength but has zero diversity — one opposition type repeated four times. KW halves the strength but maximizes diversity — four distinct mask types, no repetition. The choice between concentrated and distributed opposition is already visible at n=3. These are independent structural choices, not ends of a trade-off — the n=4 exhaustive analysis confirms S and D are exactly uncorrelated (r = 0 to machine precision).

### Sequential transitions (around the circle)

**Fu Xi** clockwise from top: Qian(111), Dui(110), Li(101), Zhen(100), Kun(000), Xun(011), Kan(010), Gen(001)

This is binary counting: 7, 6, 5, 4, 0, 3, 2, 1. Each hemisphere descends. Algebraically structured.

**KW** clockwise from S: Li(101), Kun(000), Dui(110), Qian(111), Kan(010), Gen(001), Zhen(100), Xun(011)

Seasonal/functional cycle. No arithmetic pattern.

| Step | Fu Xi transition | dist | KW transition | dist |
|------|-----------------|------|---------------|------|
| 1→2 | 111→110 = 001 | 1 | 101→000 = 101 | 2 |
| 2→3 | 110→101 = 011 | 2 | 000→110 = 110 | 2 |
| 3→4 | 101→100 = 001 | 1 | 110→111 = 001 | 1 |
| 4→5 | 100→000 = 100 | 1 | 111→010 = 101 | 2 |
| 5→6 | 000→011 = 011 | 2 | 010→001 = 011 | 2 |
| 6→7 | 011→010 = 001 | 1 | 001→100 = 101 | 2 |
| 7→8 | 010→001 = 011 | 2 | 100→011 = 111 | 3 |
| 8→1 | 001→111 = 110 | 2 | 011→101 = 110 | 2 |

| Measure | Fu Xi | KW |
|---------|-------|----|
| Mean distance | 1.5 | 2.0 |
| Distance range | [1, 2] | [1, 3] |
| Distinct masks | 4 of 7 | 5 of 7 |
| Dominant mask | 001 (3×) | 101 (3×) |
| Max-distance transition | none | 1 (Zhen→Xun = 111, complement) |
| Consecutive mask repeats | 0 | 0 |

### The structural principle

Fu Xi concentrates opposition into the diameters (complement pairs across the circle) and keeps sequential transitions smooth — low average distance, repetitive masks, binary-counting regularity. Opposition is stored, not expressed in flow.

KW distributes opposition throughout the sequence — higher average distance between neighbors, more mask variety, one full complement transition (Zhen→Xun, distance 3) embedded in the sequential flow. Opposition is woven into the process.

**Fu Xi separates opposition from flow. KW weaves opposition into flow.**

This is the same principle visible at n=6: the KW hexagram sequence sacrifices concentrated opposition (it doesn't maximize within-pair Hamming distance) for distributed opposition (kernel diversity χ², sequential anti-repetition kac). The n=3 trigram arrangements already encode this divergence.

---

## Shao Yong vs King Wen at n=6: The Same Divergence, Amplified

The Shao Yong (先天) circular arrangement of 64 hexagrams is the direct n=6 analog of the Fu Xi trigram circle. Qian (111111) at top, Kun (000000) at bottom. Right semicircle counts down in binary (63→32), left semicircle counts up (0→31). Diametrically opposite hexagrams are always complements (XOR = 111111).

### Diametric pairings

**Shao Yong pairs:** All 32 are complement. Every pair at maximum Hamming distance (6). One mask type (111111).

**KW pairs:** 28 reversal + 4 complement. Hamming distance varies by orbit signature — distance = 2 × (number of asymmetric mirror pairs in the orbit). Signature (1,0,0) → distance 2, signature (1,1,0) → distance 4, signature (1,1,1) → distance 6. Mixed mask types distributed across 8 kernel dressings.

### Sequential transitions

**Shao Yong:** Binary counting. Each step increments or decrements by 1 in binary representation. Average Hamming distance between consecutive hexagrams ≈ 2. Both semicircle seams are smooth: 32(100000) → 0(000000) = distance 1, 31(011111) → 63(111111) = distance 1. No jarring transitions anywhere. Algebraically structured, minimal sequential opposition.

**KW:** 64 hexagrams in a linear sequence with pair structure (each pair adjacent). Bridge transitions have S-distribution {S=0: 15, S=1: 15, S=3: 1} and Hamming distances governed by H = w(sig_change) + 2S. Within-pair transitions have S-distribution {S=1: 12, S=2: 12, S=3: 8}. Higher average sequential distance, varied transition types, kernel anti-repetition (kac at 0th percentile).

### Comparison

| Measure | Shao Yong | KW |
|---------|-----------|-----|
| Opposition strength (pairs) | 192 (maximum, all complement) | 120 (7 signature mask types) |
| Opposition diversity (pairs) | 0.000 (1 mask, zero entropy) | 2.750 (7 masks, 98% of algebraic ceiling) |
| Sequential smoothness | high (binary counting, mean ≈ 2) | lower (varied bridges, higher mean) |
| Sequential variety | low (repetitive transition types) | high (kac anti-repetition) |
| Weight complementarity | r = −1 (all pairs anti-correlated) | r = +0.52 (reversal preserves weight) |

### The amplified divergence

At n=3, the divergence between Fu Xi and KW was visible but constrained — only 4 pairs, limited room for diversity. At n=6, the divergence amplifies across every measure:

- **Pairing opposition:** Shao Yong holds all 32 pairs at maximum distance (S=192). KW uses algebraic equivariance (mask = orbit signature), which distributes pairs across three distance levels (2, 4, 6) with S=120 — still 99.98th percentile among random pairings, but 62.5% of the complement maximum. The constraint is not a cost paid for diversity; S and D are orthogonal. The constraint is algebraic coherence: the pairing respects the Z₂² orbit structure.

- **Sequential opposition:** Shao Yong's binary counting produces minimal, repetitive transitions — the flow is smooth but monotonous. KW's four orientation axes (χ², asymmetry, M-score, kac) specifically quantify how it distributes opposition into the sequential structure. These axes don't exist for Shao Yong because it has no orientation or ordering freedom — the arrangement is fully determined by binary counting.

- **Structural depth:** Shao Yong is a single principle (binary counting) producing a single arrangement. KW has four layers (pairing, matching, ordering, orientation) each carrying distinct opposition properties, with two frames (algebraic and semantic) providing complementary coverage. The opposition is not just distributed across the sequence — it's distributed across structural layers.

**The same principle at both scales:** Shao Yong/Fu Xi maximizes opposition strength through complement pairing — all opposition of one type. KW maximizes opposition strength subject to algebraic equivariance — opposition channeled through every mask the signature group provides, and only those masks. The divergence is not a trade-off between strength and diversity but a choice between algebraic purity and combinatorial freedom.

---

## The Self-Similarity of Opposition

The opposition principle is self-similar across levels of description:

- **Within pairs:** two states in developmental complementarity (condition → consequence)
- **Between pairs:** transitions use diverse opposition types without repetition (χ², kac)
- **Across the sequence:** two analytical frames (algebra, meaning) in complementary coverage
- **Across scales:** the pairing rule at n=3 (complement) is absorbed as a component of the pairing rule at n=6 (reversal = swap + complement-at-trigram-level)

Opposition generates opposition at every level. The tradition resolves this self-similarity through algebraic equivariance: at each scale, the pairing respects the symmetry group, channeling opposition through every available algebraic type while excluding non-algebraic masks entirely.

---

## Phase 1 Reframing: Algebraic Purity, Not Trade-Off

The n=4 exhaustive analysis and n=6 sampling force a revision of the original framing.

**What the draft predicted:** Strength and diversity trade off — you sacrifice one for the other. The KW design principle is "distribute opposition into flow."

**What the data show:** Strength and diversity are orthogonal (r = 0, exact at n=3 and n=4, confirmed at n=6). There is no global trade-off. Instead:

1. **Lens-shaped feasible region.** In S×D space, boundary constraints at extreme strength cap diversity, and vice versa. But in the interior, both are freely achievable. The "trade-off" is a boundary phenomenon at extremes, not a global anti-correlation.

2. **KW doesn't maximize diversity.** It maximizes *algebraically structured* opposition — using exactly the masks generated by the mirror-pair signature group, with near-uniform distribution across those masks. KW's diversity of 2.75 is below the random floor (3.78 at n=6), but it's 98% of the algebraic ceiling (log₂7 ≈ 2.807).

3. **"Low diversity" = "high purity."** KW uses all 7 signature masks and no others. Measured against the full combinatorial space (63 possible masks), this looks restricted. Measured against the algebraic grammar, it's near-maximal. The 56 unused masks are not rejected one by one — they are excluded as a class by the equivariance constraint.

4. **Equivariance IS the 7-mask constraint.** Z₂²-equivariance (the pairing respects the orbit structure of {id, reversal, complement, comp∘rev}) and the algebraic mask constraint (mask = orbit signature) are the same property expressed differently. At n=6, this property is shared by 0 of 10K random pairings — it is astronomically rare.

---

## Phase 2: KW as Weight-Preserving Mirror-Pair Pairing

### The mirror-pair partition group

The N line positions of an n-line figure decompose into ⌊N/2⌋ mirror pairs plus a center (if N is odd). At n=6: {L1↔L6, L2↔L5, L3↔L4}. The subgroup of B_N (signed permutations of N coordinates) preserving this partition — permuting pairs among themselves, swapping positions within pairs, and independently flipping values at each pair — is a natural geometric group defined by positional structure alone.

At n=6, this group has order 384 = (Z₂ ≀ S₃) × (Z₂)³, generated by 6 elements: 3 mirror-pair swaps and 3 mirror-pair value flips.

**Theorem.** The mirror-pair partition group is exactly the stabilizer of the KW pairing in B₆. That is, a bitwise operation preserves the KW pairing if and only if it preserves the mirror-pair partition. (Verified computationally: all 46,080 elements of B₆ checked.)

### 9 equivariant pairings

Under the full 384-element group, the 64 states collapse into **4 orbits**: two of size 8 and two of size 24. Only **8 pair-orbits** are internally consistent (no state overlap). The two size-8 orbits are forced (one pair-orbit each), leaving a 3×3 = **9 equivariant pairings**.

| Pairing | S | D | WT | Character |
|---------|---|---|------|-----------|
| Complement | 192 | 0.00 | 1.875 | All-complement. Max S. |
| KW | 120 | 2.75 | **0.375** | All-reversal for size-24 orbits. **Min WT.** |
| KW's mirror | 120 | 2.75 | 1.875 | All-comp∘rev for size-24 orbits. Same S, D as KW. |
| 6 others | 96–168 | 1.55–2.00 | 1.125–1.875 | Mixed operation choices. |

**KW is the unique minimum-weight-tilt pairing** (WT=0.375 vs ≥1.125 for all others). No tiebreaking needed.

### KW = the unique weight-preserving one

The yang-count (popcount) of a hexagram is its most fundamental scalar property — the balance of yin and yang. Reversal swaps spatial position (inner↔outer) while preserving this balance. Complement inverts the balance entirely (w → N−w). Comp∘rev does both.

Among the 9 mirror-pair-symmetric pairings, KW is uniquely characterized by: **pair each hexagram with a structurally distinct partner (spatial inversion) that shares its yin-yang balance.** Where spatial inversion has fixed points (palindromes), fall back to value inversion (complement), accepting the weight disruption as unavoidable.

The 7-mask structure, the near-maximal algebraic diversity (D=2.75 vs ceiling log₂7≈2.81), and the 99.98th percentile strength among random pairings are all *consequences* of this weight-preservation principle, not the principle itself.

*Caveat:* This characterization uniquely identifies KW as a selection criterion. Whether it also describes the historical design logic — whether weight preservation was a conscious priority — is a separate question. The characterization describes the *structural position* KW occupies, not necessarily the *path* by which it was constructed.

### Discovery path: Z₂² analysis

The 384-element characterization was reached through a longer analysis using the 4-element subgroup Z₂² = {id, complement, reversal, comp∘rev}. The key intermediate results:

**Structural decomposition.** Under Z₂², the equivariant pairing problem factors into three independent subproblems (4 palindrome orbits × 4 cr-fixed orbits × 12 size-4 orbits), yielding ~1.57 × 10¹² equivariant pairings — an enormous space that collapses to 9 under the full stabilizer.

**Per-orbit strength identity.** For every size-4 orbit: **S_rev + S_cr = S_comp = 2N**. This follows from the decomposition of the 6-bit XOR mask space into palindromic and anti-palindromic subspaces under the reversal involution. Reversal's mask is confined to the palindromic subspace (popcount = popcount(m)), comp∘rev's mask to the anti-palindromic subspace (popcount = N − popcount(m)), and complement spans the full space (popcount = N). The identity is the additivity of Hamming weight over these disjoint subspaces.

**S↔D anti-correlation under equivariance.** In the full pairing space, S and D are orthogonal (r ≈ 0). Under equivariance, r(S,D) = −0.334. The mechanism: each orbit's operation choice determines both its S contribution and its mask identity. Complement gives maximum S but a shared mask (111111); reversal/comp-rev give lower S but orbit-specific palindromic masks. This per-orbit S↔mask binding creates negative correlation at the global level.

**Falsification of entropy-maximization.** KW is NOT the strength-maximizer among equivariant pairings (complement is, at S=192). KW is NOT on the equivariant S×D Pareto frontier (~18% of Z₂²-equivariant pairings dominate KW on both). The correct characterization is weight preservation, not entropy or strength maximization.

### Unification: Weight Preservation = Algebraic Purity = Reversal Priority

Phase 1's "algebraic purity" framing (KW uses only signature masks, near-uniformly distributed) and Phase 2's "weight preservation" framing (KW uses reversal wherever possible) are three descriptions of one structural fact:

1. **Weight preservation** (choose reversal) is the *mechanism*
2. **Algebraic mask diversity** (all 7 signature masks) is the *consequence* — reversal's XOR mask IS the orbit signature (x ⊕ rev(x) = the palindromic mask encoding which mirror pairs differ)
3. **Reversal priority** is the *operational rule* — the decision procedure that generates both

The algebraic ceiling shortfall (D = 2.75 vs log₂7 ≈ 2.81) arises because the 111111 mask gets 8 copies (from forced complement at palindrome orbits) instead of 4 — a structural necessity, not a design choice.

### Cross-scale analysis

KW-style pairings (reversal for non-palindromes, complement for palindromes) exist at every n ≥ 3. Their structural position varies:

| n | States | Size-4 orbits | |Stab| | Eq. pairings | KW S/S_max | KW S %ile | KW WT (min?) |
|---|--------|---------------|--------|--------------|------------|-----------|-------------|
| 3 | 8 | 1 | — | 9 | 83% | ~99% | 1.00 (no) |
| 4 | 16 | 2 | — | 117 | 75% | ~75% | — |
| 5 | 32 | 6 | 64 | 63 | 65% | 99.7% | 0.63 (no†) |
| 6 | 64 | 12 | 384 | 9 | 63% | 99.98% | 0.38 (yes) |

†At n=5, an equivariant pairing with WT=0.25 exists (using inter-orbit reversal pairings), but it has S=36 vs KW-style's S=52. KW-style is the max-S among low-WT pairings, consistent with the lexicographic principle. ‡At n=5, |Stab|=64 = (Z₂ ≀ S₂) × (Z₂)³: the center position (L3) has no permutation freedom (always fixed under mirror-pair-preserving permutations), so the group is 8 permutations × 8 flips, not 128 as a naive count might suggest.

The tradition chose the tightest pairing compatible with each scale's geometry. At n=3, the mirror-pair structure is too sparse (1 pair) to distinguish reversal from complement — both are geometrically valid, and complement is stronger. At n ≥ 5, the richer mirror-pair geometry (2+ pairs) distinguishes the operations completely, and reversal preserves the structural information that geometry encodes. The n=3 divergence is not a failure of the weight-preservation principle; it's a consequence of the principle having no traction at that scale.

**Phase 2 conclusion.** KW is the unique weight-preserving pairing among the 9 invariants of the hexagram's mirror-pair geometry. This is a computationally verified, falsifiable characterization.

---

## Phase 3: Depth-Function Decomposition

### The question

Phase 2 characterized *what* KW preserves (weight) and *why* it's unique (among 9 mirror-pair-symmetric pairings). Phase 3 asked: does this invariant have internal spatial structure? Specifically: do nuclear trigrams (L2-L3-L4, L3-L4-L5) — which straddle the L3|L4 boundary between trigram and mirror-pair geometry — carry independent opposition information?

### The answer: No independent information, but a structural decomposition

Nuclear trigrams are a strict projection of hexagram-level structure. The 互卦 map (nuclear hexagram extraction) is a lossy 4:1 compression (64 → 16 hexagrams) that erases the outer pair (L1, L6) and doubles the inner pair (L3, L4). Every nuclear-level opposition property reduces to the hexagram-level signature with the O-component erased. The 7 signature masks collapse to 3 nonzero masks + identity under 互卦.

The I Ching's opposition structure is **two-level, not three-level**: the full hexagram and shell trigrams are the operative layers. Nuclear trigrams are a derived view.

### Depth-function separation

Phase 3's positive contribution: weight preservation is not uniformly distributed across the hexagram. The 6 line positions separate into three depth layers with distinct functional roles under KW:

| Layer | Lines | Mirror pair | Function |
|-------|-------|-------------|----------|
| Outer | L1, L6 | O | **Weight buffer.** Erased by 互卦. Absorbs weight disruption from complement pairs. |
| Middle | L2, L5 | M | **Bridge.** Each belongs to exactly one nuclear trigram. Preserved by 互卦. |
| Inner | L3, L4 | I | **Opposition core.** Both belong to BOTH nuclear trigrams. Doubled by 互卦. |

Evidence: weight preservation degrades monotonically with depth projection:

| Level | Mean |Δw| (all 32 pairs) | Mean |Δw| (28 reversal) | Weight correlation r |
|-------|-------------------------|------------------------|---------------------|
| Full hexagram | 0.375 | 0.000 | +0.516 |
| Nuclear trigram | 0.750 | 0.571 | +0.277 |
| Standard trigram | 1.125 | 1.071 | +0.024 |

Nuclear trigrams are more weight-stable than standard trigrams (0.57 vs 1.07 for reversal pairs) because the shared inner pair dampens weight redistribution. The outer pair absorbs the remaining disruption.

### Commutativity classification

The 互卦 projection partitions KW pairs by opposition depth:

- **Depth-penetrating** (28 pairs, signatures with M or I component): opposition survives nuclear projection. 互卦 commutes with KW.
- **Shell-only** (4 pairs, signature (1,0,0)): opposition lives entirely in the outer pair. 互卦 erases it — the pair collapses to identity.

The 8 hexagrams (4 pairs) where 互卦 fails to commute with KW are exactly those crossing the **palindrome phase boundary**: non-palindromic hexagrams whose nuclear core (L2-L5) is palindromic (L2=L5 and L3=L4). The two paths through the commutativity diagram apply different branches of the KW rule (reversal vs complement), producing different results.

This reveals the KW rule's two-branch structure is not merely a "fallback" — it classifies opposition by depth: shell-only versus core-penetrating.

### Connection to Phase 2

Phase 2 showed *that* weight is preserved. Phase 3 shows *where*: the outer lines carry the quantitative balance while the inner lines carry the qualitative opposition. Weight preservation is peripherally concentrated, not uniformly distributed.

The 互卦 convergence structure (64 → 16 → 4, converging to {000000, 010101, 101010, 111111} in exactly 2 steps) is observed but uninterpreted.

---

## Phase 4: 生克 Modal Complementarity

### The question

Phases 1-3 operate purely in binary structure — the only inputs are bit strings and their symmetries. Phase 4 asks: what happens when the traditional five-phase (五行) layer is introduced? The 生克 system maps 8 trigrams onto 5 elements and defines directed evaluation cycles (生 generation, 克 overcoming). The 体/用 split projects each hexagram into a directed pair of trigrams. Does this system bridge the n=3/n=6 opposition scales, or is it a separate layer?

### The answer: No scale bridge, but modal complementarity

The 体/用 projection is structurally neutral — every ordered trigram pair appears exactly 6 times across the 384 (hexagram × moving_line) states. The projection introduces no bias toward opposition or similarity. This is a theorem of the combinatorial structure, independent of any mapping.

The algebraic property of Z₂³ generation (both 生 and 克 cycle masks generating the full group under XOR closure) is universal — 100% of 50,400 valid surjections (8 trigrams → 5 elements, partition 2,2,2,1,1) achieve it on both cycles. This is a property of the partition geometry, not the traditional assignment.

**What IS distinctive:** the traditional mapping achieves maximum **partition cleanness** — the greatest possible differentiation between which XOR masks are exclusive to 生 vs exclusive to 克. The exclusive masks are: 生-only {001, 110}, 克-only {010, 011}, shared {100, 101, 111}. Cleanness = 4/7 = maximum. Only 13.3% of surjections achieve this value (100th percentile).

### The 互卦 amplification gradient

**Theorem.** Flipping line k in a hexagram changes the 互卦 by a deterministic amount depending only on the line's depth layer:
- Outer (L1, L6): Hamming change = 0 (erased)
- Middle (L2, L5): Hamming change = 1 (preserved)
- Inner (L3, L4): Hamming change = 2 (amplified)

This follows from the 互卦 picking bits {1,2,3,2,3,4}: inner bits appear twice (amplified), middle bits once (preserved), outer bits never (erased). This extends Phase 3's depth-function separation into a quantitative perturbation-sensitivity hierarchy.

### The evaluation circuit

The 本卦→互卦→变卦 circuit produces three five-phase evaluations per state. These are geometrically non-redundant: all three evaluations differ in 42.7% of states, all agree in only 5.2%. The step-by-step change rates (72%, 77%, 83%) confirm that each stage provides substantially new information.

### Shell-only pairs under 生克

Phase 3's 4 shell-only KW pairs (signature (1,0,0)) show 50% five-phase agreement between partners vs 21.4% for depth-penetrating pairs (2.33× ratio). This is structurally explained: L1/L6 perturbations often preserve the trigram→element assignment. But n=4 is too small for statistical conclusions.

### The combinatorial landscape

50,400 valid surjections were exhaustively enumerated and scored:

| Metric | Traditional | Percentile | Verdict |
|--------|-------------|------------|---------|
| Z₂³ generation (both) | Yes | 100% (universal) | Generic — not distinctive |
| Partition cleanness | 4/7 (max) | 100% (top 13.3%) | **Distinctive** |
| 克 edge-mean variance | 0.36 | 96.2% | Extreme — singleton edge anomaly |
| 生−克 Hamming asymmetry | +0.218 | 76.9% | Moderate |
| Partner agreement | 25.0% | 41.4% | Unremarkable |

### Connection to earlier phases

Phase 2 showed KW is the unique weight-preserving pairing among 9 mirror-pair-symmetric pairings. Phase 4 shows the traditional trigram→element assignment is among the top 13.3% of assignments maximizing modal complementarity among 50,400 valid surjections. Both are selection principles: the tradition's choices occupy distinguished positions in well-defined, exhaustively enumerable combinatorial spaces. Neither was inevitable; both are non-trivially constrained.

The two principles operate at different levels — the hexagram pairing (Phase 2) is purely binary, while the element assignment (Phase 4) introduces a non-binary mapping layer. Phase 4's main epistemic contribution is the sharp separation: combinatorial theorems (uniform sampling, Z₂³ universality, 互卦 amplification) hold regardless of the mapping, while the distinctive properties (partition cleanness, edge variance) depend entirely on the traditional assignment.

---

## Open Questions

1. ~~**S↔D orthogonality.**~~ Resolved (Phase 1): holds at n=3 (exact), n=4 (exact), n=6 (sampled r = −0.002). Under equivariance, r(S,D) = −0.334 — the per-orbit S↔mask coupling creates an anti-correlation that doesn't exist in the full space. Resolved (Phase 2): mechanism identified.

2. ~~**Is KW the unique strength-maximizer among equivariant pairings?**~~ Resolved (Phase 2): No. Complement is the unique S-maximizer (S=192). KW is the unique S-maximizer among *weight-preserving* equivariant pairings (S=120). The characterization is lexicographic: weight preservation >> strength >> equivariance.

3. **Cross-scale divergence.** The weight-preservation principle holds at n ≥ 5 (KW-style is extreme at both n=5 and n=6) but NOT at n=3, where tradition chose complement (strength >> weight preservation). The n=5 data shows the transition is not a sharp n=6 threshold — KW-style already occupies the 99.7th percentile at n=5. Phase 4 showed the 体/用 projection is neutral and the 生克 layer operates orthogonally to the hexagram-level pairing rule. The two scales may genuinely reflect distinct design logics.

4. Does the complementary coverage (algebra ↔ meaning inverse correlation) have a precursor at n=3 or n=4?

5. ~~**Nuclear trigram boundary.**~~ Resolved (Phase 3): The L3|L4 membrane does not carry independent opposition information. Every nuclear-level property is derivable from the hexagram-level signature by erasing the O-component. The structural contribution is the depth-function separation (outer=buffer, inner=core), which decomposes Phase 2's invariant into spatially localized mechanisms.

6. ~~**Equivariance as prior vs consequence.**~~ Resolved: The mirror-pair partition group — the subgroup of B₆ preserving the decomposition {L1↔L6, L2↔L5, L3↔L4} — has order 384 and is characterized independently of any pairing. The theorem that this group equals KW's stabilizer in B₆ means KW's equivariance is a *consequence* of mirror-pair invariance, not an independently imposed constraint. Under this full symmetry, exactly **9 equivariant pairings** exist (vs ~1.57 trillion under Z₂²). KW is the unique weight-minimizing one among these 9. The characterization collapses from "lexicographic over 1.57T" to "weight-preserving among 9." The Z₂² used throughout Phase 2 was a convenient subgroup of index 96 — sufficient to derive the rule but far from the tightest constraint.

7. ~~**Scale-bridging via 生克.**~~ Resolved (Phase 4): Refuted. The 体/用 projection is structurally neutral (uniform sampling theorem). Z₂³ generation is universal. The traditional mapping's distinctive property is modal complementarity (partition cleanness at 100th percentile, top 13.3%), not scale bridging.

8. **Max-cleanness elite structure.** What structural features do the ~6,700 max-partition-cleanness assignments share? Is the traditional one further distinguished within this elite set?

9. **The Wood anomaly.** Zhen (100) and Xun (011) are complements (d=3) — the only intra-element pair at maximum Hamming distance. All other dual-trigram elements pair at d=1. Connection to 克 edge-variance?
