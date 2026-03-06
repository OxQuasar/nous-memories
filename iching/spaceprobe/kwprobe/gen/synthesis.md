# KW Generative Investigation: Final Synthesis

## Question

Given the 32 fixed pairs (by reversal/complement) of the King Wen sequence, what principle determines their ordering? Can the 31 inter-pair bridge choices be derived from a generative rule simpler than the sequence itself?

## Method

Six rounds of systematic algebraic probing, testing reconstruction of the 31 bridge choices from algebraic features of the hexagrams. Each round built on prior findings, guided by sage evaluation and captain coordination.

| Round | Approach | Key test |
|-------|----------|----------|
| 1 | Pair graph + greedy 互 | Can 互-continuity reconstruct KW? |
| 2 | Sub-optimal bridge discriminants | What features predict KW's choice at 17 non-互-optimal bridges? |
| 3 | Hierarchical basin + 互 | Does basin schedule + local 互 optimization generate KW? |
| 4 | Kernel independence + scoring walk | Is H-kernel redundant with basin? Can combined scoring reconstruct? |
| 5 | Global structure (bipartite, 互-graph, skeleton) | Does the sequence have a global geometry that determines local choices? |
| 6 | Null models + anomaly analysis | Which findings survive proper baselines? |

## What Holds Up

### Constraint profile (the skeleton)

| Constraint | Evidence | Bits eliminated |
|------------|----------|-----------------|
| Basin clustering | 0th percentile vs random | 43 of 118 |
| H-kernel preference | Independent from basin (51% vs 45%); 12/14 at multi-option bridges | +14 (to 2^60) |
| Chiastic symmetry | IV1 Kun-heavy (4○/1●), IV2 Qian-heavy (2○/5●); p=0.026 | descriptive |
| Attractor framing | Fixed points open (#1-2), limit cycle closes (#63-64); p ≈ 5×10⁻⁷ | fixes 2 of 32 positions |
| KanLi mediation | 90% of cross-basin transitions route through center basin | descriptive |
| 互 continuity | 12.7th percentile total weight | subordinate to pair numbering |

These are genuine structural properties, not artifacts. They establish what any theory of the KW ordering must respect.

### Structural findings

**Basin crossing is the dominant discriminant.** At the 17 bridges where KW's choice is not 互-optimal, basin-crossing correctly predicts KW's choice in 14/17 cases (p=0.0002). KW pays 互-cost specifically to cross between basins.

**H-kernel carries independent information.** Only 51% of basin-crossing options are H-kernel. KW preferentially selects H-kernel transitions: 12/14 at bridges with multiple basin-crossing options. Basin-crossing and H-kernel are partially independent constraints.

**The bipartite structure IS basin structure.** At d≤1, the pair graph splits into polar (Kun+Qian, 16 pairs) vs center (KanLi, 16 pairs). This adds no information beyond the basin sequence — all basin-consistent orderings produce exactly the same component-switching pattern.

**互-graph coverage is typical.** KW's 29/31 distinct edges sits at the 79th percentile. 100% of random orderings visit all 16 互 values. The near-Hamiltonian property is an artifact of graph density.

**The cost gradient is a depletion artifact.** KW's first-half vs second-half 互 gradient is at the 25th percentile vs random — within normal range. Early bridges appear sub-optimal because the available pool is richer, not because KW systematically invests early.

## What Does Not Hold Up

### No generative principle found

Best reconstruction: **7/31 transitions (23%)** from scoring rule α=1, β=1 (basin-crossing + H-kernel). This ceiling held across 124+ parameter configurations including:
- Pure 互 greedy (3/31)
- Basin-constrained 互 greedy (5/31)
- Basin-crossing bonus with varied weights (7/31 max)
- H-kernel bonus (7/31 max)
- Hexagram distance bonus (4/31)
- Combined grid search over (α, γ, β) (7/31 max)

### No algebraic sorting criterion predicts pair numbering

| Property | Spearman ρ with position | p-value |
|----------|-------------------------|---------|
| Mean yang count | 0.083 | 0.65 |
| Distance from Qian | -0.083 | 0.65 |
| Entry-互 value | 0.081 | 0.66 |
| Lower trigram | -0.045 | 0.81 |
| Upper trigram | 0.111 | 0.55 |
| Basin type | 0.050 | 0.79 |

The pair numbering is not a monotonic sort on any tested structural property.

## The Decisive Datum: Run 13

The single most informative finding. Run 13 (pairs 17-18-19: Jin/Ming Yi → Jia Ren/Kui → Jian/Xie) is the only basin run with ≥3 pairs, providing the only non-trivial test of within-run ordering.

| Ordering | Total 互 weight | Rank |
|----------|----------------|------|
| Jia Ren→Jin→Jian | 2 | **minimum** |
| Jian→Jin→Jia Ren | 2 | **minimum** |
| **Jin→Jia Ren→Jian (KW)** | **7** | **maximum** |
| Jin→Jian→Jia Ren | 7 | maximum |
| Jia Ren→Jian→Jin | 7 | maximum |
| Jian→Jia Ren→Jin | 7 | maximum |

KW follows ascending pair-number order (17→18→19), achieving the **worst** possible 互 weight. All seven 2-pair runs also follow ascending pair-number order, but there the constraint is trivially compatible with 互 (symmetric weights). Run 13 is where they conflict, and **pair numbering wins decisively**.

**Implication:** Whatever determines pair numbering is the primary ordering principle. 互 continuity is a consequence that emerges when it doesn't conflict — not a design criterion.

## Verdict Against Generative Criteria

1. **Simpler than the sequence?** No. The best algebraic description (basin schedule + H-kernel scoring) requires specifying parameters and still leaves 2^60 ≈ 10^18 orderings. It is a partial compression, not a generator.

2. **Sufficient to reconstruct?** No. 7/31 = 23%. The remaining 77% requires information this framework does not contain.

3. **Natural to the I Ching?** Partially. Basin structure and H-kernel are native to 互 — they are structural consequences of operations the tradition itself defined. But they describe constraints, not a production rule.

## Conclusion

**The ordering principle is semantic with algebraic consequences.**

The sequence of hexagram meanings follows a narrative/philosophical logic that determines pair numbering. This semantic ordering produces notable algebraic signatures (basin clustering at 0th percentile, 互 continuity at 12.7th percentile, H-kernel preference, chiastic symmetry) because semantic categories correlate with binary structure. The algebraic properties are **real but emergent** — they arise from the semantic ordering, not the reverse.

The algebraic approach found the **skeleton**: the structural constraints the sequence respects. The **flesh** — the specific ordering within those constraints — lives in a semantic domain that algebraic probing can bound but cannot enter.

## What Would Change This Conclusion

An algebraic rule reconstructing >20/31 transitions would indicate the semantic ordering itself follows algebraic logic not yet identified. At 7/31 after exhaustive search, this possibility has diminishing returns but cannot be excluded.

## Suggested Next Investigation

Formalize the **Xugua (序卦) commentary** — the traditional text giving explicit reasons for each hexagram's position. If the Xugua's rationale, when formalized, predicts the algebraic signatures found here, that would close the circle:

```
meaning → formalized meaning → predicted algebra → verified algebra
```

This would be a semantic investigation, not an algebraic probe — a different paradigm from the one completed here.

## Scripts

| Script | Content |
|--------|---------|
| `gen/01_pair_graph.py` | Pair graph, greedy 互 walk, threshold analysis, random baselines |
| `gen/02_bridge_discriminant.py` | Sub-optimal bridge feature analysis, discrimination power |
| `gen/03_hierarchical_test.py` | Basin schedule + local 互 reconstruction, within-run optimality |
| `gen/04_kernel_and_walk.py` | Kernel independence, cost gradient, transition-walk scoring |
| `gen/05_global_structure.py` | Bipartite traversal, 互-graph walk, skeleton intervals |
| `gen/06_null_model_and_anomaly.py` | Null models, Run 13 anomaly, algebraic sorting tests |
