# Round 4: Algebraic Investigation — Results

## Summary: H = {id, O, MI, OMI} is uniquely distinguished, subgroup bias lives in the Upper Canon, and H-optimization is NOT equivalent to f1.

### 1. H characterization: the M-I lock

H = {id, O, MI, OMI} has a clean algebraic characterization: **z ∈ H iff the M-bit equals the I-bit**. In hexagram terms, the middle mirror pair (L2,L5) and inner mirror pair (L3,L4) are "locked" — they always flip together or not at all. The outer mirror pair (L1,L6) is free.

KW running product is M-I locked at 20/31 positions (96.7th percentile vs random orderings, null mean 15.5 ± 2.7).

The non-locked positions form 5 clusters: B1, B7, B14, B16-17, B20, B24-25, B29-31. These are the positions where the running product has M ≠ I.

### 2. Bridge kernel H-membership

18/31 bridge kernels are themselves in H (87.8th percentile, null mean 15.3 ± 2.8). This is mildly elevated but not extreme. The H-membership of bridge kernels is evenly split between canons (9 each).

**Key structural finding from pair-pair analysis**: For any adjacent pair-pair, there are exactly 0, 2, or 4 orientations (out of 4) that produce an H-kernel. **Never 1 or 3.** The distribution is:
- 0/4 H-options: 12.9% of pair-pairs
- 2/4 H-options: 75.8%
- 4/4 H-options: 11.3%

This is because H is a subgroup — its complement is a coset. The XOR mask's kernel membership depends on the XOR of the orientation-induced bit flips, and these come in pairs (flipping one pair's orientation toggles between H and non-H).

**7 of 31 KW bridges have H-kernel forced** (all 4 orientations → H). These correspond to specific pair-pair adjacencies where the hexagram structure makes H-membership inevitable: bridges 12, 13, 19, 22, 27, 30, 31.

Bridge 14 (hex 28→29) is special: it has **0 H-options** — no orientation can produce an H-kernel there. Only 2 distinct kernel types available (both non-H).

### 3. Greedy H-maximization: NOT equivalent to f1

| Metric | Greedy H-max | KW |
|--------|-------------|-----|
| H-residence | 0.990 ± 0.024 | 0.645 |
| f1 | **2.876 ± 0.073** | 1.767 |
| OMI count | 27.5 ± 1.5 | 8 |
| Repeats | 0.33 ± 0.50 | 2 |
| Types | **3.51 ± 0.89** | **8** |

**Greedy H-maximization produces much higher f1 than KW** (2.88 vs 1.77) — but at the cost of kernel diversity (3.5 types vs 8). Within greedy results, H-residence and f1 are uncorrelated (r = 0.006).

This is decisive: **H-residence and f1 are independent objectives**, not two views of the same signal. Maximizing one does not reproduce the other. KW is NOT near the H-residence maximum (0.645 vs achievable 0.99), suggesting KW trades H-residence against diversity.

The greedy algorithm reveals that near-perfect H-residence is achievable (>99%) with any starting pair, but this requires using only ~3.5 kernel types — almost mono-thematic bridges. KW's use of all 8 types actively fights H-residence.

### 4. All seven order-4 subgroups

| Subgroup | KW res | KW/31 | Null mean | Percentile |
|----------|--------|-------|-----------|------------|
| {I, M, MI, id} | 0.548 | 17/31 | 0.499 | 76.7% |
| {I, O, OI, id} | 0.452 | 14/31 | 0.500 | 35.9% |
| {I, OM, OMI, id} | 0.516 | 16/31 | 0.499 | 64.4% |
| {M, O, OM, id} | 0.484 | 15/31 | 0.499 | 50.2% |
| {M, OI, OMI, id} | 0.548 | 17/31 | 0.500 | 76.8% |
| **{MI, O, OMI, id}** | **0.645** | **20/31** | **0.499** | **96.7%** |
| {MI, OI, OM, id} | 0.581 | 18/31 | 0.500 | 86.1% |

**{id, O, MI, OMI} is uniquely the most biased subgroup.** It's the only one above the 95th percentile. The next closest is {MI, OI, OM, id} at 86.1%. The gap is ~10 percentile points — clear separation.

This confirms the outer mirror pair is the distinguished axis. The subgroup that locks M and I together (treating the inner hexagram core as a unit) is the one KW's running product preferentially inhabits.

### 5. Bridge kernel pair-pair structure

Every adjacent pair-pair has either 0, 2, or 4 H-kernel orientations (never odd). This is forced by H being an index-2 subgroup of Z₂³.

Of the 31 KW bridges:
- 7 are **H-forced** (all orientations produce H-kernel)
- 1 is **H-forbidden** (no orientation produces H-kernel) — bridge 14, hex 28→29
- 23 have **2 of 4 orientations** producing H-kernel

For the 23 with a choice, KW chose the H-producing orientation in 11 cases and the non-H orientation in 12 cases. This is essentially random — the orientation choices don't systematically favor H-kernels. The subgroup bias in the running product must therefore come from the **ordering** of pairs, not the orientation choices.

### 6. Two-canon structure — the decisive finding

| Metric | Upper Canon (B1-B14) | Lower Canon (B16-B31) | Full |
|--------|---------------------|----------------------|------|
| f1 (internal) | **2.154** | 1.467 | 1.767 |
| OMI deltas | **5/13** | 2/15 | 8/30 |
| H-kernel count | 9/14 (64%) | 9/16 (56%) | 18/31 |
| H-residence (reset) | **0.786** (11/14) | 0.500 (8/16) | 0.645 |
| H-residence (continuing) | — | 0.500 (8/16) | — |

**The subgroup bias is entirely in the Upper Canon.** The lower canon has exactly 50% H-residence — pure chance. The upper canon has 78.6%, driving the overall 64.5%.

**OMI deltas are also concentrated in the upper canon** (5/13 = 38.5% vs 2/15 = 13.3%). This aligns with the earlier finding of OMI front-loading (Round 3).

**f1 diverges sharply between canons**: Upper = 2.15 (extreme), Lower = 1.47 (below overall random mean of 1.49). The upper canon is doing the heavy lifting on every metric.

Cross-canon bridge kernel: OM (not in H). The transition between canons breaks the M-I lock.

## Structural picture

The King Wen sequence has a **two-phase architecture**:

1. **Upper Canon (hex 1-30)**: High-opposition phase. f1 = 2.15, H-residence 79%, OMI-heavy. The cumulative transformation keeps the middle and inner mirror pairs locked. Maximum change between bridges.

2. **Lower Canon (hex 31-64)**: Diversifying phase. f1 = 1.47 (below random mean), H-residence 50% (random), few OMI transitions. Greater kernel diversity — the lower canon uses more varied bridge types, avoiding the H-subgroup dominance.

The overall KW properties (f1 = 1.77, H-residence 64.5%, 8 kernel types) are an **average of two very different halves**, not a uniform optimization. The "high f1" and "subgroup bias" are upper canon properties. The "all 8 kernel types" and "diversity" are lower canon properties.

This resolves the tension between high f1 and kernel diversity: they're in different halves. KW isn't trading them off in a single optimization — it's doing them sequentially.
