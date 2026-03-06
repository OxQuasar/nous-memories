# Phase 4: 生克 Modal Complementarity

## Summary

The 生克 (Shēng-Kè) system was hypothesized to bridge concentrated opposition at n=3 and distributed opposition at n=6 via the 体/用 projection. This hypothesis is refuted: the 体/用 split samples trigram pairs uniformly (theorem), and the algebraic property of generating Z₂³ from cycle masks is universal across all valid surjections (100%). The replacement finding is **modal complementarity**: the traditional trigram→element assignment maximally differentiates the two fundamental interaction modes (生 and 克) in the XOR mask space. This partition cleanness property places the traditional mapping in the top 13.3% of 50,400 valid assignments — not inevitable, but non-trivially constrained.

---

## 1. 体/用 Projection (Q1)

The 体/用 split projects each hexagram (n=6) into two directed trigrams (n=3): the trigram containing the moving line becomes 用 (dynamic), the other becomes 体 (static reference). This creates 384 states (64 hexagrams × 6 moving lines).

**Theorem (uniform sampling).** Every ordered trigram pair (a, b) appears exactly 6 times across the 384 states. Each hexagram contributes 3 copies of (upper, lower) and 3 copies of (lower, upper) — one for each moving line in the respective trigram. Over all 64 hexagrams, this covers all 64 ordered pairs uniformly.

**Consequence.** The Hamming distance distribution between 体 and 用 is *identically* the baseline distribution of all 8×8 trigram pairs. Mean Hamming = 1.5000 for both. The projection introduces no bias toward opposition or similarity.

**Resolved: negative.** The scale bridge, if any, is not in the projection mechanism. The 体/用 split is a structurally neutral sampling device — it faithfully represents the full diversity of trigram relationships, neither concentrating nor distributing opposition. Whatever the five-phase evaluation layer does, it operates on a perfectly representative input.

---

## 2. 生克 in XOR Mask Terms (Q2)

The traditional mapping assigns 8 trigrams to 5 elements with partition shape (2,2,2,1,1): three elements receive two trigrams (Metal={111,110}, Wood={100,011}, Earth={001,000}) and two receive one (Fire={101}, Water={010}).

### Intra-element structure

| Element | Trigrams | XOR | Hamming |
|---------|----------|-----|---------|
| Metal | Qian (111), Dui (110) | 001 | 1 |
| Wood | Zhen (100), Xun (011) | 111 | 3 |
| Earth | Gen (001), Kun (000) | 001 | 1 |

Metal and Earth pair trigrams at minimum Hamming distance (d=1, single-bit flip). Wood is the anomaly: Zhen and Xun are **complements** (d=3, all bits differ). The tradition groups maximally distant trigrams as "same."

### Cycle masks (traditional mapping)

| Cycle | XOR masks produced | Count |
|-------|-------------------|-------|
| 生 (generation) | {001, 100, 101, 110, 111} | 5 of 7 |
| 克 (overcoming) | {010, 011, 100, 101, 111} | 5 of 7 |
| 生 ∪ 克 | all 7 nonzero masks | 7 of 7 |

Both cycles independently generate the full group Z₂³ under XOR closure.

### Z₂³ generation is universal (null model result)

All 50,400 valid surjections (8 trigrams → 5 elements, partition 2,2,2,1,1) were enumerated and scored. **Every single one generates Z₂³ on both cycles.** The rate is 100% for 生, 100% for 克, 100% for both.

This is a consequence of the partition shape: with 5 directed edges connecting groups of 1-2 trigrams each, at least 5 distinct nonzero XOR masks are produced. Since 5 vectors in a 3-dimensional vector space over GF(2) always contain a spanning set, generation is guaranteed. **Z₂³ generation is a theorem of the partition geometry, not a property of the traditional assignment.**

### Partition cleanness IS the distinctive property

The masks exclusive to each cycle tell the real story:

| Category | Masks |
|----------|-------|
| 生-only | {001, 110} |
| 克-only | {010, 011} |
| Shared | {100, 101, 111} |

**Partition cleanness** = (exclusive masks) / (total distinct masks) = 4/7 = 0.5714.

This is the **maximum** achievable value. Among all 50,400 surjections, only 6,720 (13.3%) achieve this maximum. The traditional mapping sits at the **100th percentile** — no surjection exceeds it.

The exclusive masks define how the two modes **differ**: 生 produces transformations {001, 110} that 克 never does, and vice versa. Maximum cleanness means maximum differentiation between generation and overcoming in the trigram transformation space.

### 克 edge-variance anomaly

The 克 cycle's per-edge Hamming variance is at the **96.2nd percentile** among surjections. This is driven by the Water→Fire edge (Kan 010 → Li 101), the only singleton-to-singleton edge in the 克 cycle. It forces Hamming distance 3 (complement), creating a single outlier edge among four edges at d=1.5.

**Resolved: genuine structure found.** The traditional mapping maximally differentiates 生 and 克 transformation modes. The distinctive property is modal complementarity, not algebraic generation scope.

---

## 3. Sequential Opposition in the Evaluation Circuit (Q3)

The 本卦→互卦→变卦 circuit evaluates three related hexagrams against 体 using five-phase relationships. For each of the 384 (hexagram, moving_line) states, the triple (rel_本, rel_互, rel_变) was computed.

### Anti-repetition pattern

| # unique relations | Count | Fraction |
|-------------------|-------|----------|
| 1 (all same) | 20 | 5.2% |
| 2 (one repeat) | 200 | 52.1% |
| 3 (all different) | 164 | 42.7% |

The three viewpoints **usually disagree** (94.8% have at least one change). All-different triples occur at nearly the maximum rate achievable given 5 possible relations and 3 slots.

### 互卦 amplification theorem

**Theorem (verified exhaustively).** For every hexagram x and every line position k ∈ {0,…,5}, the Hamming distance between 互卦(x) and 互卦(x ⊕ 2^k) depends only on k, not on x:

| Layer | Lines | 互卦 Hamming response |
|-------|-------|----------------------|
| Outer | L1 (bit 0), L6 (bit 5) | 0 — erased |
| Middle | L2 (bit 1), L5 (bit 4) | 1 — preserved |
| Inner | L3 (bit 2), L4 (bit 3) | 2 — doubled |

This follows directly from the 互卦 definition picking bits {1,2,3,2,3,4}: bits 2 and 3 each appear twice in the output (amplification), bits 1 and 4 once (preservation), bits 0 and 5 never (erasure). The amplification factor per depth layer is: O→0, M→1, I→2.

### Step transition rates

| Transition | Change rate |
|------------|------------|
| 本卦 → 互卦 | 71.9% |
| 互卦 → 变卦 | 77.1% |
| 本卦 → 变卦 | 83.3% |

The circuit's non-redundancy is geometrically arranged: 互卦 erases the outer shell and amplifies the inner core; 变卦 flips exactly one line. The three views are structurally constructed to minimize overlap.

**Resolved.** The evaluation circuit produces non-redundant information by geometric construction.

---

## 4. Depth Separation Meets 体/用 (Q4)

Q1's negative result (uniform projection) means the 体/用 split does not preferentially select depth layers. The outer/middle/inner functional separation from Phase 3 operates at the hexagram level but does not interact with the 体/用 assignment — because the assignment depends only on which trigram contains the moving line, not on the line's depth position within the hexagram.

**Collapsed into Q1 and Q5.** No independent content.

---

## 5. Shell-Only Opposition Under 生克 (Q5)

Phase 3 identified 4 KW pairs with signature (1,0,0) — opposition entirely in the outer shell (L1, L6), invisible to the nuclear projection. These pairs have identical upper and lower trigrams up to L1/L6 perturbation.

### Agreement rates

| Category | Pairs | Agree | Total | Rate |
|----------|-------|-------|-------|------|
| Shell-only (1,0,0) | 4 | 12 | 24 | 50.0% |
| Depth-penetrating | 28 | 36 | 168 | 21.4% |
| All | 32 | 48 | 192 | 25.0% |

Shell-only pairs show **2.33× higher agreement** — when two hexagrams differ only at L1/L6, the 体/用 five-phase evaluation is more likely to agree. This follows from the structure: since L1/L6 affect only the outer bits of each trigram, the trigram→element mapping often assigns the same element to the perturbed and unperturbed trigrams (specifically, when the intra-element Hamming is 1, as for Metal and Earth).

The overall agreement rate (25.0%) sits at the **41.4th percentile** among surjections — unremarkable.

### Detailed pattern

Of the 4 shell-only pairs: 2 show perfect agreement (all 6 lines agree) and 2 show zero agreement. The split depends on whether the perturbed trigrams fall within the same element:
- 001101↔101100 and 010011↔110010: trigram changes stay within the same element → full agreement
- 000001↔100000 and 011111↔111110: trigram changes cross element boundaries → full disagreement

**Suggestive but underpowered.** n=4 pairs is insufficient for statistical conclusions. The pattern is structurally explained but too small to be a standalone finding.

---

## 6. Five-Phase Cycle as Combinatorial Object (Q6)

### Enumeration

50,400 valid surjections from 8 trigrams to 5 elements with partition shape (2,2,2,1,1) were exhaustively enumerated and scored on multiple metrics.

### Results

| Metric | Traditional value | Percentile | Status |
|--------|-------------------|------------|--------|
| 生 generates Z₂³ | Yes | 100.0% (universal) | Generic |
| 克 generates Z₂³ | Yes | 100.0% (universal) | Generic |
| Both generate Z₂³ | Yes | 100.0% (universal) | Generic |
| Partition cleanness | 0.5714 (max) | 100.0% (top 13.3%) | **Distinctive** |
| 克 edge-mean variance | 0.3600 | 96.2% | **Extreme** |
| 生−克 Hamming asymmetry | +0.218 | 76.9% | Moderate |
| 生 mask count | 5 (min) | 16.7% | Low but not extreme |
| Edge autocorrelation | −0.300 | 67.4% | Average |
| Intra-element Hamming | 1.667 | 65.4% | Average |

### What the traditional assignment optimizes

The traditional mapping is distinguished not by algebraic scope (which is universal) but by **modal complementarity**: the maximum possible differentiation between what 生-edges and 克-edges do in trigram transformation space.

Generation (生) and overcoming (克) are the two fundamental interaction modes of the five-phase system. The traditional trigram→element assignment arranges trigrams so that these two modes use maximally non-overlapping XOR masks. This is not a generic property — 86.7% of assignments achieve less differentiation.

**Resolved.** The traditional assignment is distinguished by modal complementarity, not algebraic scope.

---

## 7. Revised Scale-Bridge Assessment

### Original thesis
The 生克 system bridges n=3 concentrated opposition and n=6 distributed opposition — the 体/用 projection embeds concentrated n=3 evaluation within the distributed n=6 framework.

### Refutation
The 体/用 projection is structurally neutral (uniform sampling theorem). Z₂³ generation is universal (null model). There is no scale-bridging mechanism in the projection or the algebraic structure.

### Replacement finding: modal complementarity
The traditional trigram→element mapping maximally differentiates the two fundamental five-phase interaction modes (生 and 克) in the XOR mask space. This is a **selection principle on the mapping**, not a structural property of the binary system.

### Connection to earlier phases

| Phase | Finding | Type |
|-------|---------|------|
| Phase 2 | KW is the unique weight-preserving pairing among 9 mirror-pair-symmetric pairings | Selection from finite combinatorial space |
| Phase 4 | Traditional element assignment is among the top 13.3% maximizing modal complementarity among 50,400 valid surjections | Selection from finite combinatorial space |

Both are selection principles that pick structurally distinctive members from well-defined combinatorial spaces. Neither was inevitable; both are non-trivially constrained. The parallel is methodological: the tradition's choices at both the hexagram-pairing level and the trigram→element level can be characterized as occupying distinguished positions in enumerable spaces, even though the specific optimization criteria differ (weight preservation vs modal complementarity).

---

## 8. Epistemic Status

### Combinatorial theorems (from binary structure alone)
- 体/用 uniform sampling: every ordered trigram pair appears exactly 6 times across 384 states
- Z₂³ generation universality: all (2,2,2,1,1) surjections generate Z₂³ on both cycles
- 互卦 amplification gradient: O→0, M→1, I→2 (deterministic per line position)
- 本→互→变 non-redundancy: geometric construction minimizes overlap between the three views

### Mapping-dependent observations (percentile ranks among surjections)
- Partition cleanness: 100th percentile (top 13.3%) — **strongest signal**
- 克 edge-variance: 96.2nd percentile — structurally driven by singleton→singleton edge
- 生−克 Hamming asymmetry: 76.9th percentile — moderate
- Partner agreement: 41.4th percentile — unremarkable
- Edge autocorrelation: 67.4th percentile — unremarkable

### Unresolved
Whether partition cleanness has a deeper structural explanation or is an irreducible property of the traditional assignment. The 6,720 max-cleanness assignments have not been further analyzed.

---

## 9. Payloads

What Phase 4 contributes to the overall theory:

1. **Scale-bridging is not the mechanism** — modal complementarity is. The 生克 system does not bridge n=3 and n=6 opposition; it imposes a maximally differentiated evaluation framework on the (structurally neutral) 体/用 projection.

2. **The traditional trigram→element assignment is non-trivially constrained** (top 13.3% on partition cleanness). This parallels Phase 2's finding that KW is the unique weight-preserving pairing among 9 candidates.

3. **The 互卦 amplification gradient is a theorem** linking depth layers to perturbation sensitivity: outer lines are invisible, inner lines are amplified. This extends Phase 3's depth-function separation into a quantitative sensitivity hierarchy.

4. **The evaluation circuit (本→互→变) is geometrically non-redundant.** The three evaluation stages are constructed to provide maximally diverse five-phase readings (all-different in 42.7% of states, all-same in only 5.2%).

---

## 10. Open Questions

1. **Max-cleanness elite structure.** What structural features do the ~6,700 max-cleanness assignments share? Is the traditional one further distinguished within this elite set? (E.g., by intra-element Hamming, edge-variance profile, or some other metric.)

2. **Directed mask sequences.** Does the ordered sequence of masks around each cycle carry additional structure beyond what partition cleanness captures? The autocorrelation test was uninformative, but more refined sequence statistics might reveal structure.

3. **The Wood anomaly.** Zhen (100) and Xun (011) are complements (d=3) — the only intra-element pair at maximum distance. Does this connect to the 克 edge-variance signal (the Water→Fire singleton edge is also at d=3)?

4. **Cross-scale divergence (Q3 from Phase 2).** Does the modal complementarity finding illuminate why n=3 uses complement while n=6 uses reversal? The 体/用 projection is neutral, so the five-phase layer operates independently of the hexagram-level pairing rule. The two scales may genuinely reflect distinct design logics, with 生克 operating orthogonally to both.

---

## Files

| File | Description |
|------|-------------|
| `shengke_foundation.py` | Round 1: 体/用 projection, element mapping, surjection enumeration |
| `foundation_results.md` | Round 1 results |
| `cycle_algebra.py` | Round 2: XOR mask algebra, partner agreement, 变卦 circuit |
| `cycle_algebra_results.md` | Round 2 results |
| `generation_test.py` | Round 3: Z₂³ null model, partition cleanness, directed profiles |
| `generation_test_results.md` | Round 3 results |
| `shengke_analysis.md` | This document — Phase 4 capstone |
