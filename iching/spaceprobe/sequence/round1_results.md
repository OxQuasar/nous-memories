# Round 1: Computational Ground Truth — Results

## Key findings that correct or refine the synthesis

### 1. Orientation bits: 16 load-bearing, not 27

The synthesis claimed "all 27 orientation bits load-bearing." The actual count is **16 / 32** under the criterion: flipping degrades f1 (mean consecutive kernel distance), increases repeats, or reduces distinct kernel types. 16 pairs are inert to orientation flips.

The discrepancy likely stems from different criteria. Our test: single-bit flip degrades at least one of {f1, repeats, f2}. The previous analysis may have used Pareto-optimality across a wider set of objectives, or a stricter definition counting pairs that affect ANY bridge (even if net metrics don't change, the specific bridge sequence changes). Under a "bridge-sequence changes at all" criterion, more pairs would be load-bearing since swapping any non-self-reverse pair changes its exit hexagram, affecting both adjacent bridges.

**Non-load-bearing pairs** include all 3 complement pairs where both members are palindromes (pairs 0, 14, 30 — hexagrams (1,2), (29,30), (61,62)), plus pair 13 (27,28) which IS load-bearing (Δf1 = -0.2). The 4th palindrome complement pair IS sensitive.

### 2. KW percentile: 96.6%, not 99.2%

f1 (mean consecutive kernel distance) = 1.767, at the **96.6th percentile** among 1M random trials (random pair permutation + random orientation). The synthesis figure of 99.2% likely came from the earlier kernel_distances.py which:
- Used 6-bit dressing distances (×2 scaling but same ordering)
- Used only 10,000 trials
- Shuffled pair ORDER but kept orientations FIXED (KW orientations preserved)

Our test is stricter: we randomize BOTH permutation and orientation, which is the correct null model for assessing how special KW is. Under this model, KW is still extreme (~97th percentile) but not as extreme as previously reported.

### 3. KW is Pareto-dominated

On the (f1, f2) Pareto plane:
- **3.0% of random trials dominate KW** (better on both f1 and f2 simultaneously)
- Maximum f1 found: 2.267 (KW = 1.767, ratio 0.78)
- f2 = 8 (all kernel types) is common: 87% of random trials achieve it

KW is not on the Pareto frontier for these two objectives alone. This means either:
1. The KW ordering optimizes additional objectives we haven't measured
2. f1 and f2 aren't the right objectives — the real constraint is more specific
3. KW balances multiple constraints, landing near but not on any single frontier

### 4. The kernel word

```
M OM OMI O OMI id OI M O MI id OMI id I OM OM O OM OMI OI OI O MI I O M id MI OI O MI
```

31 symbols over an 8-symbol alphabet. Key properties:

| Property | Value |
|----------|-------|
| Distinct types | 8/8 |
| Shannon entropy | 2.946 bits (98.2% of max) |
| Most common | O (6 times) |
| Least common | I (2 times) |
| Self-transitions | 2/30 (OM→OM at B15→B16, OI→OI at B20→B21) |
| Longest run | 2 |
| Mean consec. distance | 1.767 (3-bit) |

### 5. Algebraic structure

**Running product** visits all 8 elements of Z₂³. Element visit counts: id(6), MI(6), OMI(5), O(3), M(3), OM(3), OI(3), I(2). Heavily biased toward id and MI.

**Total product** (XOR of all 31 kernels): **M** = (0,1,0). Not the identity. This means the sequence is not "balanced" in the Z₂³ sense — the kernel contributions don't cancel out.

**Subgroup generation**: Full Z₂³ generated after just 3 bridges. The first 3 kernels {M, OM, OMI} already span the entire group. This is fast but not exceptional — 3 random elements of Z₂³ span the full group with probability (1-1)(1-1/2)(1-1/4) = ... well, the first element is nonzero (7/8 chance), the second not in the span of the first (6/8), the third not in the 4-element subgroup (4/8). So P(3 generators suffice) ≈ 7/8 × 6/8 × 4/8 = 168/512 ≈ 32.8%. Not rare, but not guaranteed.

### 6. Transition graph

Conditional entropy H(k_{n+1} | k_n) = 1.609 bits (unconditional: 2.940 bits). Mutual information I = 1.331 bits. This is substantial — knowing the current kernel tells you a lot about the next one. The transition structure is far from uniform random.

Key transition patterns:
- O → MI happens 3 times (most frequent single transition)
- OMI → id happens 2 times
- Several kernel types have strong "successor preferences"

### 7. Constraint satisfaction

KW does NOT satisfy "no consecutive kernel repeat" universally — it has 2 repeats (OM→OM, OI→OI). However:
- 28/30 transitions are non-repeating (90.7th percentile)
- Only 1.76% of random trials achieve ALL 30 non-repeating

The "d≥2" constraint is even harder: KW satisfies it for 17/30 (82.4th percentile), and 0 of 100,000 random trials satisfy it for all 30.

### 8. Pair sensitivity details

Most sensitive pairs (flipping causes largest f1 decrease):
1. **Pair 8 (hex 17,18 — Sui/Gu)**: Δf1 = -0.200, +2 repeats
2. **Pair 13 (hex 27,28 — Yi/Da Guo)**: Δf1 = -0.200, +2 repeats  
3. **Pair 31 (hex 63,64 — Ji Ji/Wei Ji)**: Δf1 = -0.100, +1 repeat

The terminal pair (63,64) being third-most-sensitive is notable — "After Completion / Before Completion" closing the sequence matters structurally.

## Implications for next round

1. **The "27 load-bearing" claim needs refinement.** Under metric-degradation criteria, it's 16. The claim may have used a different (perhaps correct) definition we should recover.

2. **KW is not f1-optimal.** At 96.6th percentile with 3% domination rate, the sequence is clearly non-random but also clearly not maximizing f1 alone. What else is it doing?

3. **The transition structure has high mutual information** (1.33 bits). This suggests the kernel sequence isn't just "diverse" — it has a specific grammar. Characterizing this grammar is a natural next step.

4. **Two repeats exist.** The "0th percentile kac" claim from the synthesis needs re-examination. It may have referred to a different metric (kac = kernel auto-correlation?) rather than literal zero repeats.

5. **The total product being M (not id)** means there's a net asymmetry. If the sequence were traversed cyclically (pair 32 connecting back to pair 1), the last bridge would need to contribute M to close the loop. Is there structure in this closure?
