# Sequence Layer Characterization

## 1. The problem: characterize the KW ordering

The King Wen sequence places 64 hexagrams in a specific order. The hexagrams are already organized into 32 pairs (by the KW pairing rule: reversal where possible, complement for palindromes). The sequence layer determines two things: (a) which pair goes in which position, and (b) which member of each pair comes first (the orientation bit).

The pairing layer was fully characterized: two axioms on three fixed-point-free involutions determine a unique structure at n=3; at n=6, mirror-pair geometry yields exactly 9 equivariant pairings, and KW is the unique weight-tilt minimizer. Can the sequence layer be similarly characterized — by axioms, a generating rule, or a tight constraint set?

**Answer after five computational rounds: no.** The sequence layer yields a structural *signature* (properties that distinguish the ordering) but not a *characterization* (axioms that determine it). This is an honest difference in the layers' susceptibility to algebraic analysis.

---

## 2. The search space

The 32 KW pairs are fixed. The ordering is determined by:

- **Pair permutation**: 32! ≈ 2.6 × 10³⁵ possible orderings (fixing pair 0 at position 0 gives 31! ≈ 8.2 × 10³³)
- **Orientation bits**: for each pair, which member comes first. 4 pairs consist of two palindromes paired by complement — both orientations produce different bridges, so all 32 pairs carry an orientation degree of freedom. Total: 2³² ≈ 4.3 × 10⁹

Combined search space: ~31! × 2³² ≈ 3.5 × 10⁴³. Under the correct null model (randomize both permutation and orientation), this is the space against which KW's properties are measured.

In practice, Monte Carlo sampling (1M trials of random permutation + random orientation) provides the null distributions. The properties tested are functions of the **bridge kernel sequence** — the sequence of 31 XOR masks connecting consecutive pairs, projected onto their palindromic (mirror-pair) component in Z₂³.

---

## 3. The known extreme properties (after deflation)

The earlier synthesis reported inflated figures. Five rounds of computation with correct null models produced these corrected values:

| Property | KW value | Earlier claim | Corrected percentile |
|----------|----------|---------------|---------------------|
| Mean consecutive kernel distance (f1) | 1.767 | 99.2nd %ile | **96.6th** |
| Kernel repeats (kac) | 2/30 | 0th %ile (no repeats) | **~75th** |
| Load-bearing orientation bits | 16/32 | 27/27 | **16/32** |
| Distinct kernel types | 8/8 | — | 87% baseline (weak) |
| Transition grammar (MI) | 1.33 bits raw | Significant | **Artifact** (0.43σ after bias correction) |
| OMI (complement) delta count | 8/30 | — | **99.2nd** unconditional, **93.6th** conditional on f1 |
| H-subgroup residence | 20/31 = 64.5% | — | **96.7th** |

**Two signals survive honest testing.** Everything else is either derivative (OMI ≈ f1, r = 0.65), weak (repeats, types), or artifactual (transition grammar).

---

## 4. Angles explored and results

### Round 1: Computational ground truth
Established baseline metrics, kernel word, transition matrix, running product path. Key corrections: 16 (not 27) load-bearing bits; 96.6th (not 99.2nd) percentile for f1; 2 kernel repeats exist.

### Round 2: Testing the grammar claim
The transition mutual information of 1.33 bits is a small-sample bias artifact. Miller-Madow correction removes 0.41 bits. After correction, KW is 0.43σ above the shuffle null — unremarkable. The "grammar" is dead. However, OMI dominance in transition deltas (8/30 at 99.2nd %ile) emerged as the sharpest single-metric signal.

### Round 3: Is OMI dominance independent of f1?
No — r(f1, OMI) = 0.65. Conditioned on f1 ≥ 1.70, OMI count drops to 93.6th %ile. Conditioned on OMI ≥ 8, f1 is at 55.7th %ile. They are one signal. However, subgroup residence (97.2nd %ile even controlling for delta distribution) and OMI front-loading (98.3rd %ile for first-half count) emerged as independent properties. Joint constraint tightness: ~1 in 120 (four constraints).

### Round 4: Algebraic investigation
The subgroup H = {id, O, MI, OMI} is uniquely distinguished among all 7 order-4 subgroups (next closest: 86.1th %ile). Algebraic characterization: z ∈ H iff M-bit = I-bit (the "M-I lock" — middle and inner mirror pairs flip together). The bias comes from pair *ordering*, not orientation choices. Greedy H-maximization produces f1 = 2.88 but only 3.5 kernel types — H-residence and f1 are genuinely independent objectives. **Critical finding: the two-canon asymmetry.** Upper Canon f1 = 2.154 (99.84th), H-residence = 11/14 (99.42nd). Lower Canon: dead center on everything.

### Round 5: Joint constraints and Lower Canon
f1 and H-residence are uncorrelated (r = −0.001). Joint constraint: ~0.86% (1 in 116). Five constraints together: ~0.083% (1 in 1,200). Upper Canon is doubly extreme at ~1 in 10,000. Lower Canon tested for: weight smoothness (53rd %ile), trigram continuity (72nd %ile), raw Hamming distance (49th %ile). All generic. The Lower Canon is structurally silent at this resolution.

---

## 5. The characterization (best candidate)

No axiomatic characterization was found. The best available description:

**The KW ordering is a two-phase sequence. The first phase (Upper Canon, hex 1–30) simultaneously maximizes consecutive kernel opposition (f1) and constrains the cumulative transformation path to the M-I locked subgroup H = {id, O, MI, OMI} of Z₂³. The second phase (Lower Canon, hex 31–64) releases all kernel-level constraints.**

The two properties of the Upper Canon:
1. **High f1**: each bridge kernel is as different as possible from the previous, driven by OMI (complement) transitions
2. **H-residence**: the running product of kernels stays within the subgroup where the middle and inner mirror pairs are locked — the inner hexagram core (lines 2–5) is treated as a unit while the outer boundary (lines 1, 6) is free

These are independent (r = −0.001) and jointly extreme (~1 in 10,000 for the Upper Canon segment).

The cross-canon bridge (hex 30→31, kernel = OM, not in H) explicitly breaks the M-I lock.

---

## 6. Selectivity: how many orderings satisfy it

| Constraint set | Survival rate |
|---|---|
| f1 ≥ 1.70 alone | 11.5% |
| H-residence ≥ 20/31 alone | 7.1% |
| f1 ∧ H-residence (the two real constraints) | **0.86%** (~1 in 116) |
| + repeats ≤ 2 | 0.51% |
| + all 8 kernel types | 0.46% |
| + OMI ≥ 8 | **0.083%** (~1 in 1,200) |

**Honest tightness: ~1 in 116** on the two independent constraints. The 1-in-1,200 figure packages two real constraints with three that are either weak or redundant with f1. Roughly 8,600 orderings per million share KW's distinguishing properties.

For comparison: the pairing layer narrows to 1 of 9 algebraically, then 1 of 1 with weight-tilt. The sequence layer is orders of magnitude less constrained.

For the Upper Canon alone: the joint probability of f1 ≥ 2.15 and H-residence ≥ 11/14 is ~1 in 10,000. The structure concentrates here.

---

## 7. KW vs Fu Xi through the characterization lens

Fu Xi (Shao Yong's binary counting order) and KW sit at opposite extremes of the same combinatorial space:

| Property | Fu Xi | KW (Upper Canon) | KW (Lower Canon) |
|----------|-------|-------------------|-------------------|
| Kernel distance | Constant (d=2), zero variance | High (f1=2.15), max variance | Generic (f1=1.47) |
| Kernel types | 2 (OM, OMI only) | All 8 | All 8 |
| OMI deltas | Alternating mechanically | Clustered, front-loaded | Sparse |
| Design logic | Systematic enumeration | Maximum opposition | Unknown |
| Generated by rule? | Yes (binary counting) | No known rule | No known rule |

Fu Xi is maximally smooth — smallest possible steps, minimal direction change, zero kernel variance. KW's Upper Canon is maximally rough — largest possible kernel jumps, all types used, complement-dominated. They represent **enumeration vs process** — two opposite answers to "how should you traverse the hexagram space?"

The Lower Canon is closer to random than to either extreme, which is itself a structural statement.

---

## 8. Connection to pairing and involution characterizations

The sequence investigation operates on the bridge kernel sequence — a derivative of the *ordering* that the pairing characterization cannot access. The relationship between layers:

**The pairing layer** determines *what* is paired (which hexagram goes with which). Fully characterized: 3² = 9 equivariant pairings under G₃₈₄, KW uniquely selected by weight-tilt minimization. This holds across both canons.

**The sequence layer** determines *where* each pair sits and *which member leads*. Not characterized. The two layers are structurally orthogonal — pairing properties (weight-tilt, mask vocabulary) say nothing about ordering properties (f1, subgroup residence), and vice versa.

The bridge kernel lives in the same Z₂³ that indexes the mirror-pair XOR masks from the pairing characterization. The subgroup H = {id, O, MI, OMI} is one of seven order-4 subgroups of that Z₂³. It corresponds to transformations where the M and I operations are locked — algebraically, the same "inner core as unit" structure that appears in the mirror-pair decomposition. This is the one point of contact between layers: the algebraic vocabulary is shared, even though the constraints are independent.

The involution characterization at n=3 (two axioms → S₄ on 4 blocks of 2) operates at a different scale entirely. The sequence layer is a property of the n=6 structure that has no n=3 analog (trigrams have no traditional sequential ordering with comparable structure).

---

## 9. What remains unexplained

1. **The generative gap.** No rule, algorithm, or axiomatic system produces the KW ordering. The constraints filter (~1 in 116) but do not generate. The pairing layer found its generator (three involutions + two axioms → unique structure). The sequence layer has not.

2. **The Lower Canon.** ~~Structurally silent.~~ **Resolved (lead 2):** The Lower Canon is organized by developmental priority, not kernel metrics. 72% of algebraic dominator violations target Lower Canon pairs, concentrated on Clear-confidence developmental pairs. The Lower Canon's algebraic genericity is not absence of structure but presence of a different kind: semantic ordering that defends against algebraic domination. See `lead2/findings.md`.

3. **Why H = {id, O, MI, OMI}?** The M-I lock (inner core as unit, outer boundary free) is uniquely distinguished among all 7 order-4 subgroups, but its connection to hexagram interpretation — if any — is unexplored. Does it relate to the trigram boundary (lines 3-4 being the junction between lower and upper trigrams)?

4. **Selection effect.** Does the Upper Canon's hexagram content (containing Heaven/Earth, Water/Fire, the "elemental" pairs) inherently support higher f1 and H-residence? Untested: the maximum achievable metrics over all 15! orderings of those specific pairs, compared to random 15-pair sets drawn from the 32.

5. **Why the 上经/下经 division at hex 30?** The investigation found that all measurable sequential structure lives in the shorter first half. Whether this is cause (the division exists to mark the boundary between structured and unstructured) or effect (the structure was concentrated in what became the Upper Canon for other reasons) is unknown.

---

## 10. Implications for active leads 2–4

### Lead 2: Developmental priority and algebra↔meaning complementarity — RESOLVED
The per-canon analysis confirmed: developmental priority is the Lower Canon's organizing principle. 72% of dominator violations target the Lower Canon; meaning clarity is 71% Clear there vs 60% in the Upper Canon. The algebra↔meaning inverse correlation replicates within each canon. Two canons, two organizing principles (algebra and meaning), jointly preventing algebraic domination. See `lead2/findings.md`.

### Lead 3: Operational probe via divination
The Meihua evaluation circuit (本→互→变) operates through trigram projections and five-phase assignments — neither of which showed structure in the sequence investigation. However, the investigation tested only *transition* properties between consecutive pairs. The divination probe tests *functional* properties (what happens when the structure is used as designed). The M-I lock's characterization (inner core as unit) is suggestive for 互卦 analysis, since the nuclear hexagram erases the outer pair and doubles the inner — exactly the pair that H treats as free vs locked.

### Lead 4: Flying star as third sequential logic
The investigation established KW as "maximally rough" and Fu Xi as "maximally smooth" at the kernel level. Flying star (Lo Shu traversal) has constant consecutive mask distance of exactly 2 — zero variance, like Fu Xi, but at a different distance. Three sequential logics, three points in the kernel-distance design space: Fu Xi at d=2 (smooth, low), KW Upper Canon at d≈2.15 mean with high variance (rough, high), flying star at d=2 (smooth, intermediate). The characterization framework developed here (f1, H-residence, kernel type distribution) could be applied directly to the flying star sequence at n=6 to complete the three-way comparison.
