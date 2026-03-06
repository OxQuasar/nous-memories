# Phase 2: Equivariant Pairing Landscape

## The Central Question

Does "maximize entropy of mask distribution subject to Z₂²-equivariance" uniquely pick out King Wen (KW)? 

**Answer: No.** ~18% of equivariant pairings dominate KW on both strength and diversity. KW is not on the S×D Pareto frontier of the equivariant family. But KW IS uniquely characterized by a different principle — see §6.

---

## 1. Structural Decomposition

The Z₂²-equivariant pairing problem decomposes into three independent subproblems:

| Component | n=4 | n=6 |
|-----------|-----|-----|
| Palindrome orbits (size 2) | 2 → 3 configs | 4 → 25 configs |
| Comp-rev-fixed orbits (size 2) | 2 → 3 configs | 4 → 25 configs |
| Size-4 orbits | 2 → 13 configs | 12 → 2,513,795,337 configs |
| **Total equivariant pairings** | **3 × 3 × 13 = 117** | **25 × 25 × 2.5B ≈ 1.57 × 10¹²** |

**Key insight: these three groups are fully independent.** No equivariant pairing can cross-pair between groups. The proof:
- Size-4 ↔ Size-2: applying reversal creates contradictions (would require a ∈ size-4 to equal rev(a), violating orbit size)
- Palindrome ↔ CR-fixed: reversal acts as identity on palindromes but as complement on CR-fixed states → incompatible constraints

### Per-orbit choices

**Size-2 orbits {a, comp(a)}**: Self-match (pair a↔comp(a), 1 way) or inter-pair with another size-2 orbit of the same type (2 linkings per pair).

**Size-4 orbits {x, comp(x), rev(x), comp_rev(x)}**: Three intra-orbit options (all equivariant):
- **comp**: x↔comp(x), rev(x)↔comp_rev(x). S = 12, mask = 111111
- **rev**: x↔rev(x), comp(x)↔comp_rev(x). S ∈ {4, 8}, mask = palindromic
- **cr**: x↔comp_rev(x), comp(x)↔rev(x). S ∈ {4, 8}, mask = palindromic complement

Plus 4 inter-orbit linkings per pair of size-4 orbits.

### Structural identity: S_rev + S_cr = S_comp = 12 per orbit

For every size-4 orbit, the three intra-orbit strengths satisfy:
```
S_comp = 12       (always)
S_rev + S_cr = 12 (always)
S_rev ∈ {4, 8}    (orbit-dependent)
```

This means all-rev and all-cr have identical total S from size-4 orbits (both = 72), and produce the same set of masks (the 6 non-trivial palindromes). The complement of a reversal mask is a comp-rev mask, and the set of palindromic masks is self-complementary.

---

## 2. n=4 Equivariant Landscape

**117 equivariant pairings.** Key findings:

| S | D | Count | Notes |
|---|---|-------|-------|
| 32 | 0.00 | 1 | Complement (unique S-maximizer) |
| 28 | 0.81 | 8 | |
| 24 | 1.00–1.50 | 28 | KW at S=24, D=1.50 |
| 20 | 0.81–2.00 | 48 | |
| 16 | 0.00–2.00 | 32 | |

**108 of 117 have inter-orbit pairing** — the per-orbit product (9) vastly undercounts.

KW is on the S×D Pareto frontier at n=4: (S=24, D=1.50) is Pareto-optimal. But it's one of 16 pairings at that point.

---

## 3. n=6 Equivariant Landscape (500K sample)

**~1.57 trillion equivariant pairings.** Sampled uniformly.

### Measure distributions

| Measure | Range | Mean ± Std | KW value | KW percentile |
|---------|-------|-----------|----------|---------------|
| Strength | [56, 192] | 111.3 ± 12.9 | 120 | 79.7% |
| Diversity | [0, 4.0] | 3.32 ± 0.30 | 2.75 | 4.3% |
| Weight Tilt | [0.125, 1.875] | 1.32 ± 0.28 | 0.375 | 0.09% |
| Weight Corr | [−1.0, +0.92] | +0.006 ± 0.33 | +0.516 | 94.7% |

### Critical comparison: equivariant vs random

| | Equivariant | Random |
|---|---|---|
| S mean | 111.3 | 97.5 |
| S range | [56, 192] | [70, 126] |
| D mean | 3.32 | 4.54 |
| D range | [0, 4.0] | [3.78, 5.0] |

Equivariance pushes strength UP and diversity DOWN compared to random pairings. The constraint concentrates opposition into structured patterns.

### S↔D correlation

**Within the equivariant set: r(S,D) = −0.334.** This is a genuine trade-off — unlike the full pairing space where S and D are orthogonal (r ≈ 0). Equivariance creates a negative coupling between strength and diversity that doesn't exist in general.

### KW position

- **Not on the S×D Pareto frontier.** 
- **~18% of equivariant pairings dominate KW on both S and D.**
- KW has moderate strength (80th percentile) and low diversity (4th percentile).
- KW has near-minimum weight tilt (0.09th percentile) and high weight correlation (95th percentile).

### S×D Pareto frontier (from sample)

| S | D | Samples |
|---|---|---------|
| 192 | 0.00 | (unseen — complement) |
| 168 | 2.50 | 1 |
| 160 | 2.91 | 1 |
| 156 | 3.38 | 1 |
| 152 | 3.58 | 1 |
| 148 | 3.70 | 2 |
| 144 | 3.75 | 2 |
| 140 | 3.88 | 1 |
| 132 | 4.00 | 2 |

KW (S=120, D=2.75) is far from this frontier.

---

## 4. The All-Reversal Subfamily

KW belongs to a special subfamily: **all size-4 orbits use reversal, all size-2 orbits self-match.**

This subfamily has exactly **625 members** (25 pal configs × 25 cr configs, with size-4 choices fixed to all-rev).

### All-rev S×D Pareto frontier

| S | D | Count | Notes |
|---|---|-------|-------|
| 120 | 2.750 | **1** | **KW (unique)** |
| 116 | 2.781 | 12 | |

**KW uniquely maximizes S within the all-rev subfamily.** It's on the 2-point Pareto frontier.

### Why all-rev has fixed S=72 from size-4 orbits

Each size-4 orbit contributes S_rev ∈ {4, 8}. The sum across all 12 orbits:
```
S_big_rev = 4+4+8+4+8+8+8+8+4+4+8+4 = 72
```

For KW (all self-match for size-2): S_pal = 24, S_cr = 24, S_big = 72 → total S = 120.

Any inter-pairing of palindrome orbits reduces S_pal < 24 (self-match gives maximum distance 6 per pair). Similarly for CR orbits. So KW uniquely achieves S=120 within the all-rev family.

---

## 5. What KW Uniquely Optimizes

KW is NOT the S-maximizer, D-maximizer, or S×D Pareto-optimizer among all equivariant pairings. But it IS characterized by:

### The reversal priority principle

**KW is the unique equivariant pairing that:**
1. Uses reversal for every orbit where reversal is a distinct option (all 12 size-4 orbits)
2. Falls back to complement (the only size-2 self-match) where reversal has fixed points (all 8 size-2 orbits)

This is a **lexicographic optimization**: maximize reversal usage first, then maximize strength within that constraint.

### Why reversal is "preferred"

Among the three intra-orbit operations:
- **Reversal** preserves yang-count (weight). This is its unique algebraic property.
- **Complement** anti-preserves weight: w(comp(x)) = N − w(x)
- **Comp-rev** also anti-preserves weight: w(cr(x)) = N − w(x)

KW is the equivariant pairing that **maximally preserves the weight (yang-count) of each hexagram while pairing it with a structurally distinct partner.**

### The mask structure

All-reversal produces exactly 6 masks (the 6 non-trivial palindromes), each appearing with equal multiplicity (4 pairs each). With the size-2 complement pairs adding 8 copies of mask 111111, the total distribution is:
```
111111: 8 pairs (from forced palindrome/CR-fixed complements)
6 palindromic masks: 4 pairs each (from reversal of size-4 orbits)
Total: 8 + 24 = 32 pairs, 7 distinct masks
```

This is the "maximally uniform reversal-compatible mask distribution."

---

## 6. Summary of Characterization Results

| Question | Answer |
|----------|--------|
| Does max-entropy equivariance select KW? | **No.** ~18% of equivariant pairings beat KW on both S and D. |
| Is KW on the equivariant S×D Pareto frontier? | **No.** Not at n=6 (yes at n=4). |
| What does KW uniquely optimize? | **Maximum reversal usage** within equivariance. |
| Is complement unique S-maximizer? | **Yes**, at both n=4 (S=32, unique) and n=6 (S=192, unique). |
| Does the S↔D trade-off exist within equivariant set? | **Yes** (r = −0.33), unlike the full space (r = 0). |
| How many equivariant pairings at n=6? | **~1.57 × 10¹²** (decomposed as 25 × 25 × 2.5B). |

### The correct characterization of KW

KW is not defined by an entropy optimization. It is defined by a **structural priority rule**:

> **Use reversal wherever the group action permits; fall back to complement where reversal has fixed points.**

This makes KW the unique equivariant pairing that maximally preserves the intrinsic weight (yang-count) of each state while providing non-trivial spatial opposition (bit-reversal swaps positions).

The I Ching pairing is not "maximum entropy subject to symmetry." It is "maximum spatial opposition subject to weight preservation and symmetry."

---

## Files

| File | Description |
|------|-------------|
| `n4_equivariant.py` | n=4 analysis: enumerate 117, compute measures, characterize |
| `n6_equivariant.py` | n=6 analysis: structural decomposition + 500K sample |
| `n4_equivariant_results.md` | Raw n=4 output |
| `n6_equivariant_results.md` | Raw n=6 output |
| `n6_eq_sample.npz` | 500K sample measure data |
| `equivariant_analysis.md` | This synthesis document |
