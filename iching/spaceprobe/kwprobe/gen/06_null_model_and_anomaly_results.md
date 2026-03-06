# Null Model Tests + Anomaly Analysis + Synthesis

## Part 1: 互-Graph Walk Null Model

KW's inter-pair walk traverses the 16-vertex 互-value graph with 31 transitions. How unusual are its graph properties vs random pair orderings?

### Results

| Metric | KW | Random mean | Random std | KW percentile |
|--------|-----|-----------|-----------|---------------|
| Distinct edges (out of 31) | 29 | 28.6 | 1.1 | 79.1% |
| Vertices visited (out of 16) | 16 | 16.0 | 0.0 | 100.0% |
| Max edge reuse | 2 | 1.8 | 0.4 | 79.1% (lower=better) |
| All 16 vertices visited | Yes | — | — | 100.0% of random do |

### Distinct edges distribution (random)

| Distinct edges | Count | Cumulative % |
|---------------|-------|-------------|
| 23 | 4 | 0.0% |
| 24 | 97 | 0.1% |
| 25 | 695 | 0.8% |
| 26 | 3354 | 4.2% |
| 27 | 12171 | 16.3% |
| 28 | 27242 | 43.6% |
| 29 ◄ KW | 35493 | 79.1% |
| 30 | 20944 | 100.0% |

**KW's 29 distinct edges is at the 79th percentile** — within normal range for random orderings. The apparent near-Hamiltonian property is not unusual; most random orderings also achieve high edge diversity because the 16-vertex graph has enough edges to accommodate 31 transitions without much repetition.

Visiting all 16 互 values is common (100.0% of random orderings do so). Full 互-space coverage is not a distinguishing feature of KW.

## Part 2: The 3-Pair Anomaly (Run 13)

Run 13 contains pairs 17 (Jin/Ming Yi), 18 (Jia Ren/Kui), 19 (Jian/Xie) — all KanLi ◎. KW places them in ascending pair-number order (17→18→19), which gives 互 weight 7. The minimum achievable is 2. Only 2/6 orderings achieve the minimum; 4/6 (including KW) tie at the **maximum** weight 7.

### 2a. All 6 orderings

| Ordering | Bridge 1 | Bridge 2 | d_互 | Kernels | Phases | Total |
|----------|----------|----------|------|---------|--------|-------|
| Jia Ren→Jin→Jian | Jia Ren→Jin | Jin→Jian | 1+1=2 | OM, OM | 体生用, 克体 | 2 |
| Jian→Jin→Jia Ren | Jian→Jin | Jin→Jia Ren | 1+1=2 | OM, OM | 比和, 生体 | 2 |
| Jin→Jia Ren→Jian **◄ KW** | Jin→Jia Ren | Jia Ren→Jian | 1+6=7 | OM, id | 生体, 生体 | 7 |
| Jin→Jian→Jia Ren | Jin→Jian | Jian→Jia Ren | 1+6=7 | OM, id | 克体, 生体 | 7 |
| Jia Ren→Jian→Jin | Jia Ren→Jian | Jian→Jin | 6+1=7 | id, OM | 生体, 比和 | 7 |
| Jian→Jia Ren→Jin | Jian→Jia Ren | Jia Ren→Jin | 6+1=7 | id, OM | 生体, 体生用 | 7 |

### 2b. Hexagram number ordering

KW's order (17→18→19) is **ascending pair-number order** (hex #35/36 → #37/38 → #39/40).

Of the 6 orderings, ascending pair-number order achieves total 互 = 7 (the maximum). 2/6 orderings achieve the minimum (2); 4/6 tie at the maximum (7). 
The pair-number ordering actively **conflicts** with 互 optimization in this run.

### 2c. Cross-check: 2-pair runs

| Run start | Pairs | Ascending? | KW d_互 | Reverse d_互 | KW optimal? |
|-----------|-------|------------|---------|-------------|-------------|
| 4 | Xiao Chu→Tai | ✓ | 5 | 5 | ✓ |
| 7 | Qian→Sui | ✓ | 1 | 1 | ✓ |
| 13 | Yi→Kan | ✓ | 4 | 4 | ✓ |
| 15 | Xian→Dun | ✓ | 2 | 2 | ✓ |
| 22 | Cui→Kun | ✓ | 5 | 5 | ✓ |
| 25 | Zhen→Jian | ✓ | 1 | 1 | ✓ |
| 29 | Huan→Zhong Fu | ✓ | 0 | 6 | ✓ |

All 7 two-pair runs follow ascending pair-number order. Of those, 7/7 are also 互-optimal (the two orderings often give identical weight).

**The pattern:** KW follows ascending pair-number order at every multi-pair run. This is trivially compatible with 互 optimization for 2-pair runs (where weights are often symmetric), but directly conflicts in the 3-pair run. Number ordering is the stronger constraint; 互 continuity is sacrificed when they conflict.

## Part 3: The 'Number Ordering' Hypothesis

Is there a structural property that correlates with pair position?

### Rank correlations with pair position

| Property | Spearman ρ | p-value | Significant? |
|----------|-----------|---------|-------------|
| Mean yang count | 0.0830 | 0.6517 | no |
| Mean distance from Qian (63) | -0.0830 | 0.6517 | no |
| Entry-互 value | 0.0813 | 0.6581 | no |
| Lower trigram | -0.0445 | 0.8091 | no |
| Upper trigram | 0.1110 | 0.5454 | no |
| Basin (0=Kun, 1=KanLi, 2=Qian) | 0.0497 | 0.7870 | no |

No significant monotonic correlation between pair position and any tested structural property. The pair numbering does not follow a simple sorting criterion.

## Part 4: Synthesis — What Has the Algebraic Approach Achieved?

### Constraint profile

| Stage | Constraint | Bits eliminated | Remaining space | Best reconstruction |
|-------|-----------|----------------|----------------|-------------------|
| Baseline | None | 0 | 2^117.7 (32!) | ~1/31 random |
| Round 1 | Orientation significance | — | fixed | — |
| Round 2 | Basin-crossing + H-kernel (identified) | — | — | — |
| Round 3 | Basin schedule | 43 | 2^75 | 5/31 |
| Round 4 | Score α=1,β=1 (basin cross + H-kernel) | 57 | 2^60 | 7/31 |
| Round 5 | Global geometry (bipartite, skeleton) | (descriptive) | — | — |
| Round 6 | Null model tests | — | — | 29/31 distinct (n.s.) |

### What we found

1. **Basin structure is real and extreme.** KW's basin clustering is at the 0th percentile. Basin determines the d≤1 bipartite partition (polar vs center). Basin-crossing is the primary discriminant at sub-optimal bridges (14/17).

2. **H-kernel is independently significant.** Not redundant with basin-crossing (only 51% of crossers are H-kernel). KW preferentially selects H-kernel transitions at 12/14 multi-option basin-crossing bridges.

3. **Chiastic interval structure.** Skeleton pairs divide the sequence into a Kun-dominant first half and Qian-dominant second half, with KanLi as constant mediator. The mid-sequence hinge (pairs 13-14) is a pole-inversion gate.

4. **互-graph coverage is typical.** 29/31 distinct edges is within normal range (79th percentile). The apparent near-Hamiltonian property is an artifact of graph density.

5. **Number ordering overrides 互 optimization.** Within multi-pair basin runs, KW follows ascending pair-number order even when this achieves 互-maximum (worst). In Run 13, KW's order is one of 4/6 orderings that tie at the worst weight. The pair numbering is the stronger constraint.

### What we did not find

1. **No generative principle.** No algebraic scoring function reconstructs more than 7/31 transitions (23%). The Kolmogorov complexity of the sequence exceeds what any tested algebraic rule can compress.

2. **No explanation for specific pair numbering.** Why is Jin pair 17 and not pair 25? No tested structural property (yang count, trigram value, 互 value, basin) produces a monotonic ordering that matches KW.

3. **No single-feature generator.** The ordering emerges from the interaction of multiple constraints (basin, kernel, skeleton, numbering) none of which alone determines the sequence.

### The honest conclusion

The algebraic approach has identified **what KW respects** but not **what generates it**.

The evidence points to a **semantic ordering with algebraic consequences**:

- The sequence of hexagram *meanings* (Qian→Zhun→Xu→Shi→...) follows a narrative/philosophical logic that determines pair numbering.

- This semantic ordering happens to produce notable algebraic signatures (basin clustering at 0th percentile, 互 continuity at 12.7th percentile, H-kernel preference, chiastic structure) because the semantic categories (heaven, earth, water, fire, etc.) correlate with algebraic structure.

- The algebraic properties are **emergent consequences** of a semantic generator, not the generator itself.


**The strongest evidence for this view:** Run 13. When ascending pair-number order (= semantic sequence) conflicts with 互 optimization, semantics wins decisively. 互 continuity is a byproduct, not a design criterion.


**What would change this conclusion:** Finding an algebraic rule that reconstructs >20/31 transitions. This would suggest the semantic ordering itself follows an algebraic logic we haven't yet identified. At 7/31, the algebraic approach has reached diminishing returns.
