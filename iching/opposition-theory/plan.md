# Opposition Theory — Study Plan

## Current State

### Completed work:

**Shao Yong reference** — Full documentation of xiantian system, Huangji Jingshi, Meihua Yishu. Key structural principle: bifurcation generates everything, binary counting IS temporal order.

**King Wen studies** (15 studies + 8 LOGOS iterations) — 4 layers (pairing, matching, ordering, orientation), 4 axes (χ², asymmetry, M-score, kac), 27 bits all load-bearing, Pareto-optimal at Hamming-1. Algebra and meaning inversely correlated but jointly exhaustive. 32/32 developmental priority. 22 theorems.

**Opposition theory draft** — Reframes existing findings as 5 opposition measures. Compares Fu Xi vs KW at n=3 and n=6. Identifies self-similarity of opposition across levels.

**Phase 1 complete** — Exhaustive n=4 analysis (2,027,025 pairings). Three major revisions to the theory. See `n4-analysis.md`.

**Phase 2 complete** — KW's full symmetry group identified (mirror-pair partition group, order 384 in B₆). Under this symmetry, exactly 9 equivariant pairings exist; KW is the unique weight-preserving one (WT=0.375 vs ≥1.125). Cross-scale analysis at n=3,4,5,6 confirms weight-preservation is structurally productive at n≥5. See `phase2/equivariant_analysis.md`, `n6/full_stabilizer_results.md`, `n5/cross_scale_results.md`.

**Phase 3 complete** — Nuclear trigrams are a projection, not an independent structural level. The 互卦 map is a lossy 4:1 compression (64→16) that erases the outer pair and doubles the inner pair. Phase 3's main contribution: depth-function separation (outer=weight buffer, inner=opposition core) decomposes Phase 2's invariant into spatially localized mechanisms. See `phase3/nuclear_trigram_analysis.md`.

---

## Phase 1 Results (Complete)

### Three revisions forced by data:

**1. Orthogonality replaces trade-off.** S↔D correlation is exactly 0.000 at n=3 and n=4, ~0 at n=6. Strength and diversity are independent axes, not in tension. Constraint only at boundaries (lens-shaped feasible region).

**2. Algebraic purity, not diversity maximization.** KW restricts to the 2^k−1 signature masks and distributes nearly uniformly within that vocabulary. 95% of algebraic ceiling at n=4, 98% at n=6. ~~Correct characterization: *maximize strength subject to Z₂²-equivariance*.~~ Superseded by Phase 2 — see below.

**3. Phase transition at n=4→n=6.** KW-style is mediocre at n=4 (dominated by 23,632 pairings) but extreme at n=6 (99.98th percentile strength among random pairings). Mechanism: 2 mirror pairs at n=4 → reversal too uniform; 3 mirror pairs at n=6 → full Z₂³ signature vocabulary unlocked.

### Measure reduction:

Original 5 measures → 3 effective pairing dimensions + 1 sequence dimension + 1 discrete constraint:
- **Strength (S)** — Σ Hamming distance across pairs
- **Diversity (D)** — entropy of XOR mask distribution (orthogonal to S in full space, anti-correlated under equivariance)
- **Weight correlation** — Pearson r of yang-counts between pair members (weight tilt is derivative, r=−0.61/−0.73)
- **Sequential variety (kac)** — only measurable with a tradition-supplied sequence
- **Equivariance** — discrete constraint (Z₂²), not continuous measure. 0.006% of pairings at n=4, ~0% at n=6

### Framework elimination:

- **Option A (Pareto):** Validated as descriptive tool, limited at n=6 (sampling only)
- **Option B (Weighted functional):** **Eliminated.** S↔D orthogonality means no linear functional captures both
- **Option C (Information-theoretic):** **Superseded.** Max-entropy does NOT select KW (Phase 2). See revised characterization below.

---

## Phase 2 Results (Complete)

### Equivariant landscape:

**Structural decomposition.** The equivariant pairing problem factors into 3 independent components:
- 4 palindrome orbits (size 2): 25 configurations
- 4 comp_rev-fixed orbits (size 2): 25 configurations
- 12 size-4 orbits: ~2.5 billion configurations
- **Total: ~1.57 × 10¹² equivariant pairings** (verified: 3 × 3 × 13 = 117 at n=4)

### Questions resolved:

**Q1 (Formalize the constraint): RESOLVED.** The equivariant space decomposes by orbit type. Each size-4 orbit offers 3 intra-orbit choices (comp, rev, cr) plus inter-orbit linkings. The per-orbit identity S_rev + S_cr = S_comp = 2N holds universally.

**Q2 (Uniqueness): RESOLVED.** Max-entropy does NOT uniquely select KW. ~18% of equivariant pairings dominate KW on both S and D. KW is not on the equivariant S×D Pareto frontier at n=6. However:

**KW = argmax S, subject to max weight preservation, subject to Z₂²-equivariance.**

This is a lexicographic optimization:
1. FIRST: maximize weight preservation → use reversal for all 12 size-4 orbits (unique weight-preserving operation; the "all-reversal subfamily" of 625 pairings)
2. THEN: maximize strength → self-match (complement) for all 8 size-2 orbits (uniquely maximizes S within all-reversal)

Reversal is the unique weight-preserving intra-orbit operation because w(rev(x)) = w(x) while w(comp(x)) = w(cr(x)) = N − w(x).

**Q4 (Conditional entropy): SUPERSEDED.** The entropy-maximization framing is wrong. KW does not maximize D — it sits at the 4th percentile of D among equivariant pairings. The correct characterization is weight-preservation priority, not entropy maximization.

### S↔D anti-correlation under equivariance:

In the full pairing space, r(S,D) = 0 (exact). Under equivariance, r(S,D) = −0.334 (from 500K sample).

**Mechanism:** Each size-4 orbit's operation choice determines both its S contribution and its mask. Complement gives S=12 (max) but mask=111111 (shared, reduces D). Reversal/comp-rev give S<12 but orbit-specific masks (increases D). This per-orbit S↔mask coupling doesn't exist in the full space (where mask identity and weight are freely independent).

### Remaining open questions:

**Q3 (Cross-scale divergence): OPEN.** Weight-preservation holds at n≥5 (KW-style at 99.7th percentile for n=5, 99.98th for n=6) but NOT at n=3 (tradition chose complement). n=5 data (63 equivariant pairings, |Stab|=64) shows the transition is gradual, not a sharp n=6 threshold. n=4 is the outlier (KW-style mediocre at 75th percentile). The n=3 divergence remains genuinely open: either a deeper principle generates both choices, or the trigram and hexagram traditions reflect distinct design logics.

At n=3, the mirror-pair structure is too sparse (1 pair) to distinguish reversal from complement — both are geometrically valid, and complement is stronger. At n≥5, the richer geometry (2+ pairs) distinguishes the operations, and reversal preserves the structural information geometry encodes.

**Q5 (Sequential variety integration):** kac (the 4th axis) is sequence-dependent. Can it be expressed as conditional entropy of consecutive bridge kernels? Integration with the pairing characterization remains open.

**Q6 (Equivariance as prior): RESOLVED.** The mirror-pair partition group — the subgroup of B₆ preserving {L1↔L6, L2↔L5, L3↔L4} — has order 384, is characterized independently of any pairing, and equals KW's stabilizer in B₆ (theorem, verified computationally). Under this full symmetry, exactly 9 equivariant pairings exist. KW is the unique weight-preserving one (WT=0.375 vs ≥1.125). Characterization: "weight-preserving among 9 mirror-pair-symmetric pairings."

---

## Phase 3 Results (Complete)

### Three questions asked, all resolved:

**Does the trigram boundary carry its own opposition signature?** No. The L3|L4 boundary is geometrically special (unique split mirror pair appearing in both nuclear trigrams) but informationally derivative. Every nuclear-level opposition property reduces to the hexagram-level signature with the O-component erased.

**How does nuclear trigram opposition relate to the effective measures?** Nuclear trigrams are a strict projection of hexagram-level structure. The 7 signature masks reduce to 3 nonzero + identity under 互卦. No new opposition measures emerge.

**Is there opposition information at the boundary that neither decomposition captures alone?** No. The nuclear level is a convergence operator (64→16→4), not a self-similarity operator. The 互卦 test found no self-similarity.

### Positive findings:

**1. Depth-function separation.** The 6 lines separate into three functional layers under KW:
- Outer (L1, L6): weight buffer — carries quantitative preservation
- Middle (L2, L5): bridge — one member per nuclear trigram
- Inner (L3, L4): opposition core — both members in both nuclear trigrams

This decomposes Phase 2's weight-preservation invariant into spatially localized mechanisms.

**2. Commutativity classification.** 互卦 partitions KW pairs into:
- Shell-only opposition (4 pairs, signature (1,0,0)): opposition invisible to nuclear level
- Depth-penetrating opposition (28 pairs): opposition preserved through projection

**3. Palindrome phase boundary.** 8 hexagrams (4 KW pairs) cross the palindrome threshold under 互卦. These are exactly the non-palindromic hexagrams whose nuclear core is palindromic (L2=L5, L3=L4). The two paths through the commutativity diagram use different branches of the KW rule, producing different results.

**4. Weight degradation at depth.** Mean |Δw| = 0.375 (hexagram) → 0.750 (nuclear) → 1.125 (trigram). The outer pair buffers weight; removing it degrades the invariant.

### Payloads carried to Phase 4:

1. Depth-function separation constrains 体/用 analysis
2. Shell-only vs depth-penetrating opposition classification
3. Weight preservation is peripherally concentrated — outer lines stabilize balance

---

## Phase 4 Results (Complete)

### Core thesis tested and refuted:

The hypothesis that 生克 bridges n=3 concentrated opposition and n=6 distributed opposition was tested computationally. The 体/用 projection is structurally neutral (uniform sampling theorem), and Z₂³ generation from cycle masks is universal across all 50,400 valid surjections. No scale-bridging mechanism exists.

### Replacement finding — modal complementarity:

The traditional trigram→element mapping maximally differentiates the two fundamental interaction modes (生 and 克) in the XOR mask space. 生-only masks: {001, 110}; 克-only masks: {010, 011}; shared: {100, 101, 111}. This "partition cleanness" of 4/7 is the maximum achievable, placing the traditional mapping at the 100th percentile (top 13.3% of surjections achieve this value).

### Six questions resolved:

**Q1 (体/用 as scale bridge): NEGATIVE.** The 体/用 split samples all ordered trigram pairs exactly 6 times each (theorem). No bias toward opposition or similarity. The projection is structurally neutral.

**Q2 (生克 in mask terms): RESOLVED.** Both cycles use 5 of 7 nonzero masks and generate Z₂³ — but this is universal (100% of surjections). The distinctive property is partition cleanness (100th percentile).

**Q3 (Evaluation circuit): RESOLVED.** 本→互→变 produces all-different five-phase evaluations in 42.7% of states, all-same in only 5.2%. Non-redundancy is geometric: 互卦 erases outer/amplifies inner, 变卦 flips one line. The 互卦 amplification gradient O→0, M→1, I→2 is a theorem.

**Q4 (Depth meets 体/用): COLLAPSED.** Q1's negative result (uniform projection) means no depth-体/用 interaction. Collapsed into Q1 and Q5.

**Q5 (Shell-only under 生克): SUGGESTIVE.** Shell-only pairs (signature (1,0,0)) show 50% agreement vs 21.4% for depth-penetrating (2.33× ratio). Structurally explained but n=4 pairs is insufficient for statistical conclusions.

**Q6 (Combinatorial object): RESOLVED.** 50,400 surjections enumerated. Z₂³ generation universal. Traditional assignment distinguished by partition cleanness (100th pct), 克 edge-variance (96.2nd pct), and 生−克 asymmetry (76.9th pct).

### Payloads:

1. Scale-bridging is not the mechanism — modal complementarity is
2. Traditional assignment non-trivially constrained (top 13.3% on partition cleanness)
3. 互卦 amplification gradient: O→0, M→1, I→2 (theorem)
4. Evaluation circuit geometrically non-redundant

See `phase4/shengke_analysis.md`.

---

## Open Questions (Across All Phases)

1. **Cross-scale divergence (Q3).** Phase 4 showed the 体/用 projection is neutral and the 生克 layer operates orthogonally to the hexagram-level pairing rule. The divergence between n=3 complement and n≥5 reversal remains genuinely open. The two scales may reflect distinct design logics.

2. **Algebra ↔ meaning complementarity.** Does the complementary coverage (algebra ↔ meaning inverse correlation from KW studies) have a precursor at n=3 or n=4?

3. **互卦 convergence.** The iteration 64→16→4 converges to {000000, 010101, 101010, 111111}. Observed but uninterpreted.

4. **Max-cleanness elite structure.** What structural features do the ~6,700 max-partition-cleanness assignments share? Is the traditional one further distinguished within this elite set?

5. **The Wood anomaly.** Zhen (100) and Xun (011) are complements (d=3) — the only intra-element pair at maximum distance. All other dual-trigram elements pair at d=1. Does this connect to the 克 edge-variance signal?
