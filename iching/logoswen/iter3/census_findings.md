# Threads A+B: Orientation Census & Traditional Rule — Findings

## Summary

The 32-bit orientation layer of the King Wen sequence exhibits one perfectly clean structural property (the inversion/complement rule), an exact algebraic identity linking several candidate rules, and no single rule that distinguishes "first" from "second" beyond chance for inversion pairs. The orientation appears to carry approximately 28 free bits — 4 bits are fixed by the complement-pair convention, and the remaining 28 (for inversion pairs) show 14/14 balance under every simple binary classifier.

---

## 1. The Inversion Frame (Thread A core finding)

**Result: All 32 pairs satisfy "reverse(first) = second" or "complement(first) = second" with zero exceptions.**

| Pair type | Count | Rule |
|-----------|-------|------|
| Inversion (non-palindromic) | 28 | reverse(A) = B |
| Complement (palindromic) | 4 | complement(A) = B |

The inversion frame orientation bitstring is `11111111111111111111111111111111` — all 1s. The "first" hexagram in every pair is the "original": reading its lines bottom-to-top defines the standard presentation, and the "second" is obtained by transformation (reversal or complement).

This is the traditional claim, now verified computationally. It carries no information (entropy = 0) because it's perfectly deterministic.

**Complement pairs** (all in orbit (0,0,0)):
- Pair 1: Qian (111111) → Kun (000000) — heavier first  
- Pair 14: Yi (100001) → Da Guo (011110) — lighter first
- Pair 15: Kan (010010) → Li (101101) — lighter first
- Pair 31: Zhong Fu (110011) → Xiao Guo (001100) — heavier first

The complement pairs split 2/2 on weight — no weight rule governs them.

---

## 2. The 14/14 Algebraic Identity (Thread B core finding)

**For all 28 inversion pairs, every simple binary rule gives exactly 14/14.**

This is not coincidence — it's algebraically forced. For inversion pairs (b = reverse(a)):

- `to_int(a)` uses weights (2⁵, 2⁴, 2³, 2², 2¹, 2⁰) applied to (L1, L2, L3, L4, L5, L6)
- `to_int(b)` uses the same weights applied to (L6, L5, L4, L3, L2, L1), which equals `to_int_reversed(a)`
- So `to_int(a) > to_int(b)` iff the MSB-first reading exceeds the LSB-first reading

This is equivalent to:
- **binary_high** ≡ **first_diff_bottom_yang** (first asymmetric line pair from bottom has bottom line yang)
- **revbin_high** ≡ **first_diff_top_yang** (complement of above)
- These two are exact complements: if one gives 14/14, the other gives 14/14

Weight is completely uninformative for inversion pairs because bit-reversal preserves Hamming weight (same bits, different order, same count).

**Best single structural rule across all 32 pairs: 17/32 (53.1%)** — statistically indistinguishable from chance.

Rules tested (all at 14/28 for inversion pairs):
- Binary value (high/low)
- Reversed binary value  
- First differing line from bottom/top
- Lower/upper trigram binary value
- Individual line tests (L1, L6)

---

## 3. The Binary Frame (Thread A)

The binary orientation string (1 = first hex has higher binary value):

```
11111101110001000000110011010011
```

**Statistics:**
- Balance: 17/32 (p = 0.86, not significant)
- Runs: 13 (expected ≈ 16.5, p = 0.14, not significant)  
- Lag-1 autocorrelation: +0.227 (p = 0.21, not significant)
- Lag-4 autocorrelation: +0.291 (highest, suggestive)

**Octet structure:**

| Octet | Pairs | Binary-high count | Pattern |
|-------|-------|-------------------|---------|
| 1 | 1-4 | 4/4 | 1111 |
| 2 | 5-8 | 3/4 | 1101 |
| 3 | 9-12 | 2/4 | 1100 |
| 4 | 13-16 | 1/4 | 0100 |
| 5 | 17-20 | 0/4 | 0000 |
| 6 | 21-24 | 2/4 | 1100 |
| 7 | 25-28 | 3/4 | 1101 |
| 8 | 29-32 | 2/4 | 0011 |

The first 5 octets form a perfect monotone decreasing sequence: **4 → 3 → 2 → 1 → 0**.

Monte Carlo (100K trials):
- Exact octet sequence (4,3,2,1,0,2,3,2): p ≈ 0.00002
- First 5 octets monotone decreasing: p ≈ 0.067
- V-shape (decrease then increase): p ≈ 0.047

The exact octet sequence is highly unlikely (p ≈ 2×10⁻⁵), but this is likely an artifact of testing a specific observation — the monotone decrease alone is marginally significant. The octet pattern is visually striking but not individually compelling after multiple-comparison correction.

---

## 4. Canon Structure

**Upper canon** (pairs 1-15): 10/15 binary-high first (67%)  
**Lower canon** (pairs 16-32): 7/17 binary-high first (41%)

For inversion pairs only:
- Upper (excluding complement pairs 1, 14, 15): 8/12 binary-high (67%)
- Lower (excluding complement pair 31): 6/16 binary-high (38%)

The cumulative deviation shows a clear arc: binary-high is strongly preferred in the upper canon (deviation peaks at +3.7 around pair 10), then reverses in the lower canon, returning to exact balance at pair 32.

**Interpretation:** In the upper canon, the "bottom-to-top reading gives the larger number" direction is preferred. In the lower canon, it reverses. This could reflect the traditional "ascending/descending" thematic arc.

---

## 5. Position Coordinates & Coset Structure

In the factored basis, each hexagram has orbit coordinates (ō,m̄,ī) and position coordinates (o,m,i) = (L1, L2, L3).

**Key identity:** For inversion pairs, the position difference pos_a ⊕ pos_b equals the orbit signature. This is the mask = sig identity expressed in position space. For complement pairs (all in orbit (0,0,0)), the position difference is (1,1,1) ≠ (0,0,0) = sig.

**Coset structure:** In 5 of 7 non-trivial orbits, the 4 first-hexagram positions form a coset of a 2-dimensional subgroup of Z₂³:

| Orbit | Pairs | Coset? | Subgroup |
|-------|-------|--------|----------|
| (0,0,0) | 1,14,15,31 | No | (complement pairs, structurally different) |
| (0,0,1) | 5,8,11,24 | **Yes** | {MI, OI, OM} |
| (0,1,0) | 4,7,16,21 | **Yes** | {MI, O, OMI} |
| (0,1,1) | 13,19,20,23 | **Yes** | {I, O, OI} |
| (1,0,0) | 12,22,28,30 | **Yes** | {M, OI, OMI} |
| (1,0,1) | 3,18,26,29 | **Yes** | {MI, O, OMI} |
| (1,1,0) | 2,10,17,25 | No | General position (6 distinct XORs) |
| (1,1,1) | 6,9,27,32 | No | General position (but 1 flip away from coset) |

Monte Carlo: p(coset) ≈ 0.50 per orbit independently, so 5/7 gives p(≥5) ≈ 0.23. **Not statistically significant** — this level of coset structure is expected by chance.

Orbit (1,1,1) is interesting: flipping any single pair's orientation produces a coset (all 4 single-flip alternatives yield cosets with different subgroups). This means KW's orientation in orbit (1,1,1) is "maximally non-coset" — the unique 4-element subset of Z₂³ that avoids all coset structures.

---

## 6. Key Conclusions

### What's determined:
1. **The pairing rule is perfectly clean:** 28 inversion + 4 complement, no exceptions.
2. **"Original first" is the universal convention:** reverse(first) = second, or complement(first) = second.
3. **Weight cannot distinguish orientation for inversion pairs** (forced equality by symmetry).
4. **The binary/first-diff rules all collapse to one degree of freedom** per inversion pair: the choice of reading direction (bottom-up vs top-down).

### What's not determined by any single rule:
5. **No structural rule exceeds 53% on all 32 pairs** (17/32 best, with 15 exceptions).
6. **All simple rules give exactly 50% on inversion pairs** (14/28, algebraically forced).
7. **Complement pairs split 2/2 on weight**, ruling out a uniform weight rule.

### What's suggestive but not conclusive:
8. **Upper canon favors binary-high** (67%), **lower canon favors binary-low** (62%).
9. **First 5 octets monotone decrease** (4→3→2→1→0, p ≈ 0.07).
10. **Coset structure in 5/7 orbits** (p ≈ 0.23, not significant).

### Implication for Thread C:
The orientation carries approximately 28 genuinely free bits (the 4 complement pairs are in orbit (0,0,0) and constrained by the complement convention). The question for Thread C is: how many of these 28 bits are forced by S=2 avoidance at bridges? If the answer is "most of them," then the apparent randomness of orientation is actually tight constraint. If "few," then orientation is a genuine design choice with ~28 bits of freedom and no simple rule.

---

## Scripts

- `thread_a_census.py`: Builds all orientation frames, computes statistics, Monte Carlo
- `thread_b_traditional.py`: Verifies pairing rule, tests 18 candidate structural rules
- `thread_ab_deep.py`: Reading direction analysis, octet patterns, information content
- `thread_ab_cosets.py`: Coset structure analysis in position coordinates per orbit
