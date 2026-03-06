# Round 4: Dominator Investigation — Results

## KW Reference Profile

| Metric | KW Value | Direction |
|--------|----------|-----------|
| Kernel χ² | 2.290 | Lower = better |
| Canon asymmetry | +3 | Higher = better |
| M-score | 12/16 | Higher = better |
| Kernel autocorrelation | −0.464 | More negative = better |

---

## P1: All 12 Dominators Independently Validated

All 12 dominating orientations from Round 3 were recomputed from scratch:

| # | Ham | χ² | asym | m | kac | S2-free | Dominates | Status |
|---|-----|-----|------|---|------|---------|-----------|--------|
| 1 | 2 | 2.290 | +3 | 12 | −0.474 | ✓ | ✓ | VALID |
| 2 | 4 | 1.774 | +3 | 12 | −0.474 | ✓ | ✓ | VALID |
| 3 | 6 | 1.258 | +3 | 12 | −0.547 | ✓ | ✓ | VALID |
| 4 | 6 | 2.290 | +3 | 12 | −0.513 | ✓ | ✓ | VALID |
| 5 | 6 | 2.290 | +3 | 12 | −0.539 | ✓ | ✓ | VALID |
| 6 | 6 | 1.774 | +3 | 12 | −0.475 | ✓ | ✓ | VALID |
| 7 | 7 | 2.290 | +4 | 12 | −0.518 | ✓ | ✓ | VALID |
| 8 | 6 | 2.290 | +3 | 12 | −0.524 | ✓ | ✓ | VALID |
| 9 | 6 | 2.290 | +3 | 12 | −0.525 | ✓ | ✓ | VALID |
| 10 | 6 | 1.774 | +3 | 12 | −0.477 | ✓ | ✓ | VALID |
| 11 | 8 | 2.290 | +3 | 12 | −0.534 | ✓ | ✓ | VALID |
| 12 | 8 | 2.290 | +3 | 12 | −0.532 | ✓ | ✓ | VALID |

**12/12 confirmed.** Independent recomputation from raw orientation vectors matches stored metrics exactly.

---

## P2: Semantic Analysis of the Hamming-2 Dominator

### What Gets Swapped

The dominator flips two free bits:
- **Bit 17 → Pair 21**: Swaps #43 Guai (Breakthrough, 111110) ↔ #44 Gou (Coming to Meet, 011111)
- **Bit 26 → Component (29,30)**: Swaps #59 Huan (Dispersion, 010011) ↔ #60 Jie (Limitation, 110010) at pair 29

Pair 30 (#61 Zhong Fu / #62 Xiao Guo) is unchanged — it's part of the constrained component but the valid alternate state only requires flipping pair 29.

### Bridge Changes

Only 4 of 31 bridges change:

| Bridge | KW kernel | Dom kernel |
|--------|-----------|------------|
| 20 | OI | I |
| 21 | O | id |
| 28 | OI | I |
| 29 | O | id |

**Pattern: OI→I and O→id at both locations.** The same kernel transformation occurs at both flip sites. This is not coincidental — both pairs have similar algebraic structure relative to their neighbors.

### Kernel Distribution Shift

| Kernel | KW | Dom | Δ |
|--------|-----|-----|---|
| id | 4 | 6 | +2 |
| O | 6 | 4 | −2 |
| I | 2 | 4 | +2 |
| OI | 4 | 2 | −2 |
| (others) | — | — | 0 |

χ² is preserved because the distribution shifts are symmetric: two types gain +2, two types lose −2. The net imbalance cancels. This is the **chi² epistasis mechanism**: each flip individually changes the histogram, but together the changes are complementary.

### kac Improvement Mechanism

KW has adjacent kernel pairs (OI, O) at bridges 20-21 and 28-29. The dominator replaces these with (I, id). 

In the kernel autocorrelation metric, consecutive kernel similarity is penalized. OI and O share 2 of 3 kernel bits (Hamming distance 1). I and id share 2 of 3 kernel bits (also Hamming distance 1). But the *context* differs: the surrounding bridges create different autocorrelation contributions. The net effect is a modest kac improvement of 0.010 (from −0.464 to −0.474).

### Asymmetry Preservation

| Pair | Canon | KW binary-high-first | Dom binary-high-first |
|------|-------|---------------------|-----------------------|
| 21 | lower | True | False |
| 29 | lower | False | True |
| 30 | lower | True | True |

The two swaps cancel in the asymmetry calculation: one changes from high-first to low-first, the other from low-first to high-first. Both are in the lower canon, so asymmetry (upper − lower) is preserved at +3.

### M-Score Preservation

None of the affected pairs (21, 29, 30) are M-decisive (L2 = L5 in all three). So the M-rule is unaffected.

---

## P3: Structural Preservation Check

### Properties Compared Across All Dominators

| Property | KW | Dom #1 (H=2) | Preserved across all 12? |
|----------|-----|------------|--------------------------|
| Max S-value | 3 | 3 | **No** — only #1 and #6 preserve S=3 |
| S-distribution | {0:15, 1:15, 3:1} | {0:16, 1:14, 3:1} | **No** — varies |
| Binary-high-first | 17 | 17 | **No** — varies (15–19) |
| Kernel repeats | 2 | 1 | **No** — varies (1–4) |
| Max kernel run | 2 | 2 | **Yes** — all preserve max run ≤2 |
| kac lag-2 | +0.196 | +0.101 | No — varies widely |
| Total weight | 192 | 192 | **Yes** (algebraic invariant) |

### Key Finding: S=3 Bridge

KW has a unique S=3 bridge (the bridge where all three mirror-pair flips coincide). Most dominators eliminate this feature. Only 2 of the original 12 preserve it.

The Hamming-2 dominator preserves the S=3 bridge and preserves the max kernel run length (≤2). It changes the S-distribution slightly (one S=0 gains at the expense of one S=1) and reduces kernel repeats from 2 to 1.

### Hamming-2 Dominator Structural Detail

| Metric | KW | Ham-2 Dominator | Change |
|--------|-----|-----------------|--------|
| Kernel repeats | 2 | 1 | Fewer repeats (better) |
| Kernel Hamming chain sum | 53 | 51 | Lower sequential variety |
| kac lag-1 | −0.464 | −0.474 | Better (more anti-correlated) |
| kac lag-2 | +0.196 | +0.101 | Significantly lower |
| Max kernel run | 2 | 2 | Same |
| S-distribution | {0:15, 1:15, 3:1} | {0:16, 1:14, 3:1} | Minor shift |

**The Hamming-2 dominator is structurally very close to KW.** It reduces sequential repetition (kernel repeats 2→1, kac lag-2 halved). The structural cost is small: one S-value shifts from 1 to 0, and the kernel Hamming chain sum drops by 2.

---

## P4: Extended Search — All Dominators up to Hamming ≤8

### Search Statistics

| Hamming | Orientations checked | New dominators | Total |
|---------|---------------------|----------------|-------|
| ≤6 | 397,593 | 12 | 12 |
| 7 | 888,030 | 1 | 13 |
| 8 | 2,220,075 | 3 | 16 |
| **Total** | **3,505,698** | **16** | **16** |

### New Dominators (Hamming 7-8)

| Bits flipped | Ham | χ² | asym | m | kac |
|-------------|-----|-----|------|---|------|
| {9,10,11,15,16,17,23} | 8 | 1.774 | +3 | 12 | −0.525 |
| {0,9,11,17,20,23,26} | 8 | 2.290 | +3 | 12 | −0.481 |
| {9,10,11,16,17,23,26} | 8 | 1.774 | +3 | 12 | −0.472 |
| {2,3,9,10,11,12,23,24} | 10 | 2.290 | +3 | 12 | −0.470 |

Note: The last entry at Hamming 10 was found because it involves 8 free bits (some of which are Type B components affecting 2 pairs each).

### Hamming Distribution

| Hamming from KW | Count |
|-----------------|-------|
| 2 | 1 |
| 4 | 1 |
| 6 | 7 |
| 7 | 1 |
| 8 | 5 |
| 10 | 1 |

### Bit Frequency (Updated)

| Bit | Pair(s) | Frequency | % |
|-----|---------|-----------|---|
| **17** | [21] | **15/16** | 93.8% |
| **9** | [9] | **15/16** | 93.8% |
| **23** | (19,20) | **13/16** | 81.2% |
| 11 | [11] | 8/16 | 50.0% |
| 10 | [10] | 6/16 | 37.5% |
| 16 | [18] | 5/16 | 31.2% |
| 26 | (29,30) | 5/16 | 31.2% |
| 24 | (25,26) | 5/16 | 31.2% |
| 15 | [17] | 5/16 | 31.2% |

**Update:** Bit 17 is no longer in ALL dominators — the Hamming-10 dominator at bits {2,3,9,10,11,12,23,24} excludes it. But it remains in 15/16 (93.8%).

### kac Range Across All Dominators

- Best (most negative): −0.547 (Hamming 6, bits {9,17,23,24})
- Worst: −0.470 (Hamming 10, bits {2,3,9,10,11,12,23,24})
- Median: −0.516
- KW: −0.464
- **Max improvement over KW: 17.8%**

---

## P5: Sequential Construction Hypothesis

### Test 1: Forward Greedy Targeting KW Profile

Processing pairs 0→31, choosing each orientation to minimize L1 distance from KW's exact metrics (looking ahead with remaining pairs at default).

**Result: Recovers KW exactly (Hamming 0).** The L1-to-KW-target greedy algorithm, when given KW's profile as the target, produces KW. This means KW is a fixed point of forward greedy L1 descent.

### Test 2: M-Rule Default + kac-Aware Override

Default: M-rule (L2=yin first). Override when the alternative improves kac by >0.01.

**Result:** 11 overrides (3 S=2-forced, 8 kac-driven).
- Orientation: `00000000000000000010000000000100` (Hamming 2 from KW)
- Metrics: χ²=2.290, asym=+1, m=11, kac=−0.608
- **Pareto: trade-off** (worse on asym and m, better on kac)

This is **the Hamming-2 dominator's orientation!** The M-rule+kac-override process produces the exact same orientation as the minimal dominator, but with a different metric profile because the overrides go beyond what's needed for domination (8 overrides instead of 2).

Wait — the orientation `00000000000000000010000000000100` has bits flipped at pairs 18 and 29. That's actually different from the Hamming-2 dominator (pairs 21 and 29). The similar Hamming distance is coincidental.

### Test 3: Single-Objective Forward Greedy

| Objective | χ² | asym | m | kac | Ham | Pareto |
|-----------|-----|------|---|------|-----|--------|
| kac only | 2.290 | +2 | 11 | −0.617 | 3 | trade-off |
| χ² only | 0.742 | +1 | 13 | −0.399 | 2 | trade-off |
| **L1 to KW** | **2.290** | **+3** | **12** | **−0.464** | **0** | **equal (= KW)** |
| kac weighted | 0.742 | +3 | 13 | −0.447 | 2 | trade-off |
| balanced | 0.742 | +5 | 12 | −0.321 | 2 | trade-off |

**The only objective that recovers KW is the L1-to-KW-target.** No simple single-axis or balanced-weight objective produces KW. This means KW is not the output of any simple greedy forward rule — it's the fixed point of targeting itself.

### Test 4: Reverse Greedy (Pairs 31→0)

| Objective | χ² | asym | m | kac | Ham | Pareto |
|-----------|-----|------|---|------|-----|--------|
| kac only | 4.355 | 0 | 10 | −0.647 | 5 | trade-off |
| **L1 to KW** | **2.290** | **+3** | **12** | **−0.464** | **0** | **equal (= KW)** |

**L1-to-KW also recovers KW in reverse.** KW is a fixed point of greedy L1 descent from both directions. This is evidence that KW occupies a unique local basin under the L1 metric.

### Test 5: Can Single-Bit Descent Reach KW from the Dominator?

Starting from the Hamming-2 dominator (L1 cost 0.021):

**No single-bit flip from the dominator reduces L1 cost.** The only available single-bit moves either increase L1 (move away from KW metrics) or are blocked by S=2 constraints. The dominator sits in a different basin under single-bit L1 descent.

Flipping bit 17 back (toward KW) actually increases L1 cost dramatically to 0.802 — because the chi² epistasis works in reverse: the individual flip worsens chi² by 1.032, which the kac gain of 0.003 cannot compensate for.

**The dominator and KW are in separate basins of the single-bit L1 landscape.** Neither can reach the other by greedy descent.

---

## Bonus: 5th Axis Hypothesis

### Kernel Autocorrelation Lag-2

KW has kac_lag2 = +0.196. Among the 16 dominators:
- 11/16 have *lower* (better?) kac_lag2 than KW
- 3/16 have *higher* kac_lag2 than KW

If kac_lag2 were a 5th axis (lower = better, matching the lag-1 pattern), the dominators would still dominate KW on it — they improve on lag-2 as well. So **kac_lag2 does not explain KW's choice** to stay at its current position.

### Kernel Run Lengths

All 12 original dominators preserve KW's max kernel run length of 2. No dominator creates runs of 3 or more consecutive identical kernels. This property is preserved.

### S-Distribution Shift

KW has {S=0: 15, S=1: 15, S=3: 1} — a notably symmetric distribution with a single S=3 outlier. Most dominators break this symmetry. Only 2 of 16 preserve the S=3 bridge.

**This is the strongest candidate for a 5th axis.** The S=3 bridge at position 15 (the boundary between upper and lower canon) is a distinctive structural feature. Most dominators eliminate it. If preserving the S-distribution or the S=3 bridge were a design criterion, it would explain why KW rejects most dominating orientations.

However, the Hamming-2 dominator *does* preserve the S=3 bridge. So even this criterion doesn't fully explain KW's choice.

---

## Summary of Key Findings

1. **All 12 dominators validated.** 16 total found up to Hamming 8.

2. **The Hamming-2 dominator is remarkably well-behaved.** It preserves S=3, max kernel run, asymmetry, m-score, and binary-high-first count. It only differs from KW on 4 of 31 bridges, all via the same OI→I / O→id kernel transformation. It improves kac by 2.2%.

3. **No single-objective greedy produces KW.** Only the L1-to-KW-target objective (targeting KW's own profile) recovers it. KW is a fixed point of self-targeting, not the output of any simple optimization.

4. **KW and the dominators occupy separate basins.** Single-bit descent cannot reach one from the other. The chi² epistasis that enables domination also creates a barrier: approaching KW from a dominator requires passing through a chi²-worsened intermediate.

5. **No clear 5th axis found.** kac_lag2, kernel run length, and weight balance do not explain KW's preference for its current position over the dominators. The S-distribution shift is the strongest candidate but is not sufficient (the Hamming-2 dominator preserves it).

6. **The forward greedy L1-to-KW process is path-independent.** Both forward (0→31) and reverse (31→0) processing recover KW exactly. KW is a robust fixed point under L1 targeting.

---

## Interpretation

The dominator discovery does *not* mean KW is "wrong" or sub-optimal. It means:

1. **The 4-axis metric is incomplete.** KW is locally Pareto-optimal at Hamming distance 1 (iter4) but not at distance 2. The 2-step escape uses chi² epistasis — a nonlinear interaction the arranger couldn't detect with single-pair perturbations.

2. **The domination gap is tiny.** The Hamming-2 dominator improves kac by only 0.010 (2.2%). This is within the noise floor of any felt-sense construction process. A human arranger could not distinguish kac=−0.464 from kac=−0.474.

3. **KW is a basin attractor.** It's the fixed point of forward greedy L1 descent — no matter which direction you process pairs, the same orientation emerges. This is a strong structural property: KW is the only orientation that is simultaneously the greedy-best choice at every pair position given the rest.

4. **The structural near-equivalence of KW and the Hamming-2 dominator** (same 4 bridges change, same kernel transformation at both sites, same macro-structure preserved) suggests they're *two versions of the same design* — the dominator is what you'd get if you continued polishing after reaching KW.

---

## Data Files

| File | Contents |
|------|----------|
| round4_analysis.py | All P1–P5 + bonus analysis |
| round4_data.json | Aggregated results from all priorities |
| round4_dominators_extended.json | All 16 dominators with metadata (up to Hamming 8) |
