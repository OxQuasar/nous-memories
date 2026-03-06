# Thread F: Trigram Orientation + Thread C Extended — Findings

> **Central question (F):** Do trigram-level patterns in the King Wen sequence encode orientation preferences? Can a trigram-based rule recover which hexagram comes first in each pair?

> **Central question (C extended):** Among the 2²⁷ S=2-free orientations, what properties distinguish KW's specific choice?

> **Key results:**
> 1. **No trigram ordering rule recovers KW orientation** (best 24/28 after optimizing over all 40320 orderings; p = 0.31 corrected for multiple testing)
> 2. **The M-component (L2,L5) shows a marginal asymmetry**: among 16 decisive pairs, KW's first hexagram has L2=yin, L5=yang 12 times (p = 0.038 uncorrected; p ≈ 0.06 among S=2-free; p ≈ 0.22 corrected for testing all 3 components)
> 3. **Nuclear trigrams reduce to the M-component rule**: nuclear_lower < nuclear_upper ⟺ L5 > L2
> 4. **Multi-property filtering**: combining kernel uniformity, OMI contrast, canon asymmetry, and trigram bridge preservation reduces to 1/50,000 samples matching KW (joint p ≈ 0.00002)
> 5. **Canon asymmetry is a genuine Layer 4 signal**: P(asymmetry ≥ KW) = 0.048 among S=2-free orientations

---

## 1. Trigram Configuration Under Inversion (Thread F, §1)

### Verified: the reversal relationship

For all 28 inversion pairs (b = reverse(a)):
- lower_b = reverse(upper_a) ✓ (28/28)
- upper_b = reverse(lower_a) ✓ (28/28)

For 4 complement pairs (b = complement(a)):
- lower_b = complement(lower_a) ✓
- upper_b = complement(upper_a) ✓

### Consequence for orientation

Flipping an inversion pair's orientation doesn't just swap the hexagram — it performs a non-trivial operation on the trigram structure:
- (lower_a, upper_a) ↔ (reverse(upper_a), reverse(lower_a))

This is NOT simply swapping upper and lower. It also reverses each trigram. This means trigram-level patterns are sensitive to orientation in a structured way: the reversal operation couples the upper/lower trigram swap with an internal trigram reversal.

---

## 2. Trigram Balance (Thread F, §2)

**Each of the 8 trigrams appears exactly 8 times as lower and 8 times as upper across all 64 hexagrams.** This is a forced property — it holds for any permutation of 64 hexagrams (since the 64 hexagrams are exactly the 8×8 grid of (lower, upper) trigram combinations).

**Every (lower, upper) trigram pair appears exactly once in the 64 hexagrams.** This is also forced — a consequence of having all 64 distinct hexagrams.

---

## 3. Trigram Position Preferences (Thread F, §3)

Within each pair, the "first" hexagram's trigram profile vs the "second":

### Lower trigram in first hexagram

| Trigram | 1st hex | 2nd hex | Ratio |
|---------|---------|---------|-------|
| Thunder | 6 | 2 | 0.75 |
| Mountain | 5 | 3 | 0.625 |
| Fire | 5 | 3 | 0.625 |
| Heaven | 5 | 3 | 0.625 |
| Water | 4 | 4 | 0.50 |
| Earth | 3 | 5 | 0.375 |
| Lake | 3 | 5 | 0.375 |
| Wind | 1 | 7 | 0.125 |

### Upper trigram in first hexagram

| Trigram | 1st hex | 2nd hex | Ratio |
|---------|---------|---------|-------|
| Wind | 6 | 2 | 0.75 |
| Lake | 6 | 2 | 0.75 |
| Water | 5 | 3 | 0.625 |
| Earth | 4 | 4 | 0.50 |
| Heaven | 4 | 4 | 0.50 |
| Mountain | 3 | 5 | 0.375 |
| Thunder | 2 | 6 | 0.25 |
| Fire | 2 | 6 | 0.25 |

### Pattern

The lower trigram shows a rough yang-weight preference: high-yang trigrams (Thunder=1, Fire=2, Heaven=3) tend to appear as lower trigram in the first hexagram. Wind (yang count 2) is a dramatic exception — almost never lower in the first hex.

The upper trigram shows roughly the reverse: Wind and Lake dominate the upper position of the first hexagram; Thunder and Fire avoid it.

This is consistent with the inversion structure: if the first hex has Thunder as lower, the second has reverse(Thunder) = Thunder as upper. But the asymmetry between first and second is the orientation choice.

---

## 4. Nuclear Trigram Rule (Thread F, §7 — Key Finding)

### The rule

**Among decisive pairs (where nuclear lower yang ≠ nuclear upper yang), the first hexagram has LESS nuclear lower yang than nuclear upper yang in 15/20 cases (75%, p = 0.021 one-tailed).**

For inversion pairs only: 12/16 decisive (p = 0.038).

### Algebraic reduction

The nuclear lower trigram is (L2,L3,L4). The nuclear upper is (L3,L4,L5). Their yang-count difference = L5 - L2. So:

**nuclear_lower_yang < nuclear_upper_yang ⟺ L2 = 0, L5 = 1**

The nuclear trigram rule is equivalent to: **KW's first hexagram tends to have L2=yin, L5=yang**.

### Component analysis

Testing all three mirror-pair components for first-hex preference:

| Component | Line pair | Decisive pairs | First hex preference | Score | p-value |
|-----------|-----------|----------------|---------------------|-------|---------|
| **M** | **(L2,L5)** | **16** | **L2=yin, L5=yang** | **12/16** | **0.038** |
| O | (L1,L6) | 16 | L1=yang, L6=yin | 10/16 | 0.227 |
| I | (L3,L4) | 16 | L3=yang, L4=yin | 9/16 | 0.402 |

The M-component is the strongest of the three, but under multiple testing correction (3 components tested): P(any component ≥ 12/16) = 0.22 (simulation). Among S=2-free orientations specifically: P(M ≥ 12/16) = 0.062. **Marginal, not definitive.** The first hexagram tends to have the middle line pair in (yin, yang) order — L2=0, L5=1 — but this could be chance.

### Canon split

| Canon | L2=yin preferred | Decisive | Rate |
|-------|-----------------|----------|------|
| Upper (pairs 1-15) | 4 | 7 | 57% |
| Lower (pairs 16-32) | 8 | 9 | 89% |

The M-component preference is *stronger* in the lower canon — opposite to the binary-high arc from Thread A. This suggests the M-preference is a separate phenomenon, not a manifestation of the same canon arc.

### Interpretation

The M-component corresponds to the middle position pair (lines 2 and 5). In the factored basis, L2⊕L5 is the M-component of the orbit signature. KW's orientation preference for L2=yin means: among hexagrams whose middle pair is asymmetric (L2≠L5), the first hexagram tends to have the yin line in the lower position.

---

## 5. Trigram Ordering Search (Thread F, §11)

### Exhaustive search over all 8! = 40,320 orderings

**Best lower-trigram ordering score: 24/28 inversion pairs**

Ordering (highest → lowest): Thunder, Fire, Mountain, Heaven, Water, Wind, Lake, Earth

4 exceptions: pairs 12, 18, 21, 23.

### Multiple-testing correction

**P(best ordering ≥ 24/28 | random orientation) = 0.31** (10,000 simulations)

Under random orientation, the best achievable score from all 40,320 orderings concentrates around 22-24 out of 28. KW's 24/28 is completely typical.

**Conclusion: No trigram ordering rule recovers KW's orientation.** The exhaustive search is a multiple-testing trap — with 40,320 hypotheses, even random data yields high scores.

---

## 6. Trigram Transitions at Bridges (Thread F, §9)

| Property | KW | S=2-free mean ± std | p-value |
|----------|-----|---------------------|---------|
| Lower trigram preserved at bridge | 5/31 | 4.50 ± 1.32 | 0.49 (two-sided) |
| Upper trigram preserved at bridge | 4/31 | 4.50 ± 1.32 | 0.51 (two-sided) |

**Trigram bridge preservation is completely typical.** KW neither maximizes nor minimizes trigram continuity across bridges. This is not surprising — bridge trigram behavior is primarily a Layer 3 (pair ordering) property, with orientation contributing only minor adjustments.

---

## 7. Canon-Split Trigram Patterns (Thread F, §12)

### Upper canon (pairs 1-15): first hex lower trigrams

Thunder dominates (5 occurrences), Heaven is strong (4). Wind absent (0). Earth minimal (1).

### Lower canon (pairs 16-32): first hex lower trigrams

Mountain and Fire dominate (4 each). Thunder drops to 1. More balanced overall.

### Upper canon: first hex upper trigrams

Earth dominates (4). Heaven and Water present (3 each). Thunder absent (0).

### Lower canon: first hex upper trigrams

Wind and Lake dominate (5 each). Earth absent (0).

This reversal — Thunder→lower in the upper canon, absent from lower; Wind→upper in the lower canon, absent from upper — mirrors the binary-high canon arc but in trigram terms.

---

## 8. Thread C Extended: Valid Orientation Subspace (§1-2)

### Structure recap

- 2³² total orientations
- 2²⁷ = 134,217,728 S=2-free orientations (3.125%)
- 5 independent constraints: 4 equality constraints + 1 fixed value
- 22 completely free pairs, 10 pairs in 5 constrained components

### Comprehensive property comparison (50K S=2-free samples)

| Metric | KW | S=2-free mean ± std | Percentile |
|--------|-----|---------------------|------------|
| Kernel chi² (uniformity) | 2.29 | 7.33 ± 3.82 | 6th (p = 0.061) |
| OMI-XOR fraction | 0.267 | 0.167 ± 0.069 | 88th (p = 0.119) |
| Canon asymmetry | +3 | -1.51 ± 2.41 | 95th (p = 0.048) |
| Mean bridge Hamming | 2.94 | 2.84 ± 0.13 | 83rd (not significant) |
| Lower bridge preservation | 5/31 | 4.50 ± 1.32 | 78th |
| Upper bridge preservation | 4/31 | 4.50 ± 1.32 | 51st |
| Upper canon binary-high | 10/15 | 7.51 ± 1.81 | 95th |
| Lower canon binary-high | 7/17 | 9.01 ± 1.59 | 17th |

### Key finding: canon asymmetry is a real signal

KW's orientation produces a canon asymmetry of +3 (upper canon has 3 more binary-high-first pairs than lower canon). Among S=2-free orientations:
- Mean asymmetry: -1.51 (negative because S=2 constraints are all in the lower canon, pairs 13-30)
- P(asymmetry ≥ +3) = **0.048** (significant at 5% level)
- P(|asymmetry| ≥ 3) = 0.389 (not significant if testing for any direction)

The significance is one-directional: KW's upper canon specifically favors binary-high. The S=2 constraints shift the mean negative (because constrained pairs are in the lower half), making KW's positive direction even more unusual.

---

## 9. Thread C Extended: Joint Analysis (§4, §7)

### Independence of signals

| Pair | Correlation | Independent? |
|------|------------|-------------|
| chi² vs canon_asym | r = -0.068 | Yes (weak) |
| chi² vs OMI-XOR | r = 0.037 | Yes |

### Multi-property filtering

| Conditions | Survivors (of 50K) | Fraction |
|-----------|-------------------|----------|
| chi² ≤ KW | 3,037 | 6.07% |
| + OMI ≥ KW | 262 | 0.52% |
| + asymmetry ≥ KW | 10 | 0.02% |
| + lower bridge ≥ KW | 5 | 0.01% |
| + upper bridge ≤ KW | 1 | 0.002% |

**Only 1 of 50,000 S=2-free orientations matches KW on all 5 properties simultaneously.**

However, this is a post-hoc selection of properties — the individual p-values (0.06, 0.12, 0.05, 0.49, 0.51) include two that are near-null (bridge preservation). The genuine signals are:
- Kernel uniformity: p ≈ 0.06 (marginal)
- Canon asymmetry: p ≈ 0.05 (marginal)
- Joint (chi² + asym): p ≈ 0.005

### Joint kernel + canon asymmetry

P(chi² ≤ KW AND asymmetry ≥ KW) = 0.0052 (259/50,000)

If independent: 0.061 × 0.048 = 0.0029. Ratio: 1.79 — **positive dependence**. Orientations that produce uniform kernel chains also tend to have positive canon asymmetry. This is unexpected and suggests a structural coupling between kernel uniformity and binary-high preference in the upper canon.

---

## 10. Summary: What Orientation Encodes

### Layer 4 signals (genuinely orientation-dependent)

| Signal | p-value | Character |
|--------|---------|-----------|
| S=2 avoidance | 5 bits constrained | Hard constraint (binary) |
| Kernel uniformity | p ≈ 0.06 | Soft preference (distributional) |
| Canon asymmetry | p ≈ 0.05 | Sequential preference (upper vs lower canon) |
| M-component (L2,L5) preference | p ≈ 0.04 uncorrected; ~0.06 S=2-free; ~0.22 corrected | Marginal component preference |
| Joint kernel + canon asymmetry | p ≈ 0.005 | Two correlated marginal signals |

### Layer 4 non-signals (not orientation-dependent)

| Property | Why not a signal |
|----------|-----------------|
| Trigram ordering | p = 0.31 (multiple testing corrected) |
| Trigram bridge preservation | KW = mean (p ≈ 0.5) |
| OMI-XOR contrast | Belongs to Layer 3 (p = 0.12 at Layer 4 vs 0.03 at Layer 3) |
| Trigram (lower,upper) uniqueness | Forced (all 64 pairs appear exactly once) |
| Trigram balance | Forced (each trigram appears 8× as lower and 8× as upper) |

### The M-component ↔ nuclear trigram connection

The nuclear trigram rule and the M-component preference are algebraically identical:

**nuclear_lower_yang < nuclear_upper_yang ⟺ L2=yin, L5=yang ⟺ M-component of first hex favors (0,1)**

This is a reading direction preference for the middle mirror pair. It says: among hexagrams with an asymmetric middle pair (L2≠L5), KW tends to place the one with L2=yin first. This is a coordinate-level selection principle operating on a single component of the factored basis.

### What remains unexplained

The 27 free bits decompose roughly as:
- 5 bits: S=2 constraint (binary, hard)
- ~3-4 bits: kernel uniformity + canon asymmetry (soft, jointly p ≈ 0.005)
- ~1-2 bits: M-component preference (marginal, p ≈ 0.06 among S=2-free)
- ~20 bits: no detected signal

About 60-70% of the orientation freedom shows no detectable structure. This could mean:
1. The remaining bits are genuinely free (no design principle)
2. The signal exists but requires a different analytical frame
3. The interaction effects (how bits combine) carry the structure, not individual bits

### The strongest Layer 4 result

The joint kernel-uniformity + canon-asymmetry signal (p ≈ 0.005) is the most compelling Layer 4 finding. These two properties are weakly positively correlated (r = -0.07 with chi², meaning low chi² correlates with high asymmetry), suggesting a structural coupling. The multi-property filter (1/50K) is suggestive but includes post-hoc criteria — the pre-registered signals (kernel from iter2, canon asymmetry from Thread A) give the honest joint p ≈ 0.005.

---

## Scripts

| Script | Purpose | Key output |
|--------|---------|------------|
| `trigram_orientation.py` | Trigram trajectories, nuclear trigrams, ordering search | M-component p=0.038, ordering p=0.31 corrected |
| `thread_c_extended.py` | Multi-property analysis across 50K S=2-free samples | Joint p=0.005, multi-filter → 1/50K |
