# Domains — Findings

## Overview

7 iterations across Iterations 1–3 (algebraic groundwork) and Iterations 4–7 (empirical market test), plus 3 iterations on D1 (TCM 八纲辨证). The investigation asked: does the Z₅ grammar (GMS, valve, axis-type partition) make testable predictions for domains outside its native algebraic habitat? Algebraic results (D3) established the predictions; the market test (D4) was the first empirical evaluation; the TCM study (D1) was the second.

---

## D3: Structural Invariance Results (Iterations 1–3)

### D3-R1: Edge-count invariance

Under any axis assignment (all 48 elements of Aut(Q₃) = S₃ ⋉ (Z₂)³), the edge-type distribution is always 比和=2, 生=4, 克=6. 50% of single-axis transitions are 克-typed. 24 distinct patterns, stabilizer = {id, complement}. Subgraph structure: 克 = 2×P₄, 生 = 2×P₃, 比和 = 2×K₂.

### D3-R2: Full surjection landscape

102 distinct edge-coloring patterns from 240 complement-equivariant surjective functions F₂³ → Z₅. The Aut(Q₃) orbit contains exactly 24 of these (the ones with Q₃-adjacent doublet pairs). The (0,\*,\*) patterns (30 colorings) serve as an axis-independence diagnostic: they require nonlinear axis entanglement.

### D3-R3: Minimal determining set

6 edges (one per complement pair) necessary and sufficient to identify any coloring among the 102. Within Aut(Q₃), 5 suffice.

### D3-R4: Axis-Type Alignment Theorem

In any {2,2,2,1,1} complement-equivariant surjection F₂³ → Z₅ with Q₃-adjacent doublets, the three axes have types: **doublet** (2比和+2生, never destructive), **pure-克** (4克, always destructive), **mixed** (2克+2生, exactly half destructive). Forced by the Legendre symbol (3/5) = -1. The (4/2+2/2+2) partition is specific to p=5.

### D3-R5: Empirical testing protocol

Steps 0–4 derived from D3-R1 through D3-R4. Step 0 (M1 prerequisite), Steps 1–3 (axis-type identification from transition character), Step 4 (GMS bigram test on P₄ paths).

---

## D4: Market Regime Test (Iterations 4–7)

### Data

BTC 1-second datalog, 2025-07-21 to 2026-02-20 (18.6M rows, 7 months). Resampled to 1h bars (5,160 bars) and 4h bars (1,290 bars). Three binary axes: trend (`trend_4h`), volatility (`realized_vol_4h`), order book bias (`ob100_ratio_1m`).

### D4-R1: Axis independence achieved

The original liquidity proxy (`spread_bps_1m`) was degenerate (>97% zeros). Volume-as-liquidity had MI=0.346 with volatility, collapsing Q₃ to Q₂ (83% of bars on one face). Six order book fields screened; `ob100_ratio_1m` selected: MI=0.0025, vertex entropy 2.995/3.0, min vertex count 143.

An independence–stability tradeoff was discovered: the most independent fields (ob_imbalance_slope, liquidity_shift) oscillate too fast for Q₃ edge structure (M1≈0.46). `ob100_ratio_1m` changes on a timescale compatible with trend and volatility.

### D4-R2: Q₃ adjacency is empirically real

M1 = 0.789 at 1h (79% of non-self transitions are single-axis). M1 increases monotonically from 0.44 (8h) to 0.79 (1h), confirming that multi-axis jumps at longer bars are sequential single-axis flips resolved at shorter timescales. Near-uniform vertex distribution (11–15% per vertex).

### D4-R3: Z₅ axis-type partition does not manifest

Edge-level partition test on all 12 Q₃ edges, 2,065 traversals at 1h. Two observables: regime persistence at destination, volatility ratio (next/current bar).

**Level 1 (partition existence):** Persistence FAILS (max/median ratio 1.52, threshold 2.0). Vol ratio PASSES (2.32) but is confounded — vol-axis flips mechanically change vol.

**Level 2 (canonical assignment):** FAILS. Volatility axis has LARGEST within-axis range (predicted uniform). Trend axis has SMALLEST (predicted bimodal). Opposite of prediction.

**Within-axis type comparisons** — the decisive test controlling for axis identity:
- Trend axis (2克 vs 2生): persistence p=0.226, |log(vol_ratio)| p=0.444
- Liquidity axis (2比和 vs 2生): persistence p=0.853, |log(vol_ratio)| p=0.411

All four comparisons non-significant (all p>0.2). η²(axis)/η²(type) = 2.4–3.0×. Axis identity dominates.

### D4-R4: 克→克 is enhanced, not suppressed (GMS falsified)

GMS bigram test on 2,065 Q₃ edges (1h bars). Two framings (temporal adjacency and Q₃ walk), three null models (independence, vertex-conditional, permutation).

克→克 is 42–46% above independence null. p=1.0000 in permutation tests (observed higher than all 10,000 shuffles). The enhancement is fully explained by graph topology: vertex-conditional null gives ratio 1.014.

75 of 222 克→克 bigrams fall on the P₄ paths the GMS specifically forbids. All 8 directed forbidden triples observed.

### D4-R5: Market regime walk is memoryless

Vertex-conditional null ratio 1.014 means: a first-order Markov chain on Q₃ vertices with empirical per-vertex transition rates fully accounts for edge-type sequencing. No second-order structure. No edge-type memory. The simplest possible model for regime transitions on Q₃ — current vertex → vertex-dependent probabilities → next vertex.

### D4-R6: Root cause — S₃ symmetry breaking

The Z₅ typing assumes S₃ symmetry across Q₃ axes — it treats all axes as interchangeable, assigning type based on algebraic distance. The three market axes (trend, volatility, order book bias) have maximally asymmetric physical character: different dimensions, different timescales, different dynamics. Axis identity (which physical axis changed) explains behavioral variance; algebraic type does not.

---

## D1: TCM 八纲辨证 Test (Closed)

### Investigation

Examined whether TCM's 八纲辨证 (Eight Principles Pattern Identification) provides a natural Q₃ test bed for the Z₅ grammar. The three candidate binary axes: 寒/热 (cold/hot), 虚/实 (deficiency/excess), 表/里 (exterior/interior). Sources: 黃帝內經 (素問 chs. 5, 28, 29, 31, 32; 靈樞 chs. 73, 77), 傷寒論, and secondary 梅花易數 medical domain.

### D1-R1: Axis correlation — common 陰/陽 factor

All three axes are subdivisions of the single 陰/陽 meta-axis. 表=陽, 热=陽, 实=陽; 里=陰, 寒=陰, 虚=陰. This is not a statistical correlation — it is definitional in the source texts (素問 ch.5: "陽勝則熱，陰勝則寒"; ch.29: "陽者主外，陰者主內"; ch.28: "邪氣盛則實" = yang excess).

**Consequence:** Strong diagonal clustering in the Q₃ cube. The 热-实-表 vertex and 寒-虚-里 vertex are default attractors. The cube does not fill uniformly — it hollows into a near-degenerate structure dominated by two opposite corners.

### D1-R2: 表/里 sequentiality

The 表/里 axis is not a binary state variable but a disease-depth gradient. The 熱論 (素問 ch.31) models 傷寒 as progressing through six channels over six days: 太陽→陽明→少陽→太陰→少陰→厥陰. The treatment boundary is at day 3: "未滿三日者，可汗而已；滿三日者，可泄而已" (sweat before day 3, purge after). The 傷寒論 confirms this is the dominant clinical model, with "转属" (transfer) transitions being the primary disease dynamics.

**Consequence:** 表 and 里 are not interchangeable binary states like the bits of a Q₃ vertex. They are ordered stages of progression. A patient does not oscillate between 表 and 里 — disease moves inward. This violates the Q₃ requirement of bidirectional transitions on all axes.

### D1-R3: No classical mapping exists

No text in the 黃帝內經, 傷寒論, or 梅花易數 assigns 八纲 poles to trigram bits. The only 內經 chapter connecting trigrams to medicine (靈樞 ch.77, 九宮八風) maps trigrams to organs via wind direction — a cosmological framework, not a diagnostic one. The 梅花 medical domain uses Z₅ (生克) for prognosis but does not map 八纲 axes to trigram lines.

**Consequence:** Constructing a 八纲 → trigram mapping would be an invention with researcher degrees of freedom, not a discovery of existing structure. Any positive result would be contaminated by the freedom in choosing which axis maps to which bit position.

### D1-R4: Dimensional mismatch — clinical structure is 2×3, not 2³

The 傷寒論's 六經 model organizes disease channels as a two-level tree: 陰/陽 at the top, then three subdivisions within each. Three 陽 channels (太陽, 陽明, 少陽) subdivide 表; three 陰 channels (太陰, 少陰, 厥陰) subdivide 里. This is Z₂ × Z₃ = 6 channels, not Z₂³ = 8 vertices. The native clinical architecture has the wrong combinatorial dimension for Q₃.

**Consequence:** The 八纲 framework (which frames the clinical material as 2³) is a later systematization imposed on a structure that is natively 2×3. The mismatch is detectable: six channels pair into three 表裏 pairs, each resolved during specific 地支 time windows. No arrangement of three binary axes can naturally produce this 2×3 structure — it would require one axis to have three values, not two.

### D1 verdict: CLOSED

Four structural failures:
1. Common factor (陰/陽) → diagonal clustering, not uniform Q₃ occupation
2. Sequentiality of 表/里 → unidirectional progression, not bidirectional switching
3. No classical mapping → construction artifacts
4. Dimensional mismatch → native structure is 2×3, not 2³

---

## Cross-Domain Synthesis

### What D4 and D1 tell us together

D4 (market regimes): Q₃ adjacency is real, but Z₅ typing adds nothing. Cause: maximally asymmetric axes (different physical dimensions).

D1 (TCM 八纲): The axes share a common factor and are hierarchically nested. Cause: all three are subdivisions of one meta-axis (陰/陽).

These are complementary failures. D4 axes are too different from each other. D1 axes are too similar to each other (all reducible to one underlying variable). The Z₅ grammar requires axes that are **independent but equivalent** — different enough to vary freely, similar enough to be interchangeable.

### Domain criterion — three conditions

For the Z₅ grammar to be testable in any domain:

1. **S₃ symmetry.** Three axes of similar physical character, similar dynamics, similar timescale. (D4 lesson — market axes are different dimensions.)

2. **Axis independence.** No common factor that creates diagonal clustering. Each axis must vary freely while the others remain fixed. (D1 lesson — 陰/陽 meta-axis creates correlation.)

3. **Axis parallelism.** All axes must be genuine binary state variables, not hierarchically nested or sequentially ordered. No axis should represent a one-way progression. (D1 lesson — 表/里 is sequential; 六經 is 2×3, not 2³.)

### Grammar decomposability

The 梅花 medical domain uses Z₅ (五行 生克) extensively for medical content — pharmacology, spirit diagnosis, prognosis — without requiring Q₃ structure. The hexagram generation system (Q₃) is the delivery mechanism; Z₅ is the interpretive grammar. These are algebraically separable: Q₃ could exist without Z₅ (a hypercube with no edge typing), and Z₅ could exist without Q₃ (element relations without a three-bit substrate).

**Epistemological caveat:** The tradition's parallel usage of Z₅ and Z₂ frameworks (刺熱論's 天干/五行 temporal system vs 傷寒論's 地支/陰陽 temporal system) reflects historical layering — different medical schools developing different explanatory frameworks — not a deliberate decomposition of mathematical structures. The algebraic separability is real; whether Z₅ has autonomous empirical content outside the I Ching's abstract Q₃ is unknown.

### Interpretive shift: uniqueness classification vs natural law

The uniqueness theorem (synthesis-3) proves the 五行 assignment is the unique complement-respecting surjection F₂³ → Z₅. Uniqueness theorems classify — they establish that a particular mathematical object is the only one of its kind under given axioms. They do not predict that the classified pattern will appear in physical systems.

D4 and D1 together are evidence that the grammar may be specific to the abstract trigram space where it was derived. Each domain fails for a *different* structural reason, and the failure reasons are complementary (too different / too similar). The three-condition criterion is so restrictive that it may be satisfiable only in the abstract algebraic habitat — not because no domain has been found yet, but because the conditions define a narrow window that real-world domains systematically miss from opposite directions.

This shifts the research orientation from "search for external validation" toward "characterize the grammar's nature as a mathematical object." The grammar's content may be its uniqueness — that it is the only way to type Q₃ edges under complement-Z₅ axioms — not its transferability to physical systems.

### Implications for remaining domains

**D1 (TCM 八纲辨证):** Closed. Four structural failures (common factor, sequentiality, no mapping, dimensional mismatch).

**D2 (Quantum 3-qubit):** Unchanged — algebraically exact, likely physically empty.

**Other Q₃ domains:** The three-condition criterion is now extremely restrictive. Any candidate must have three binary axes that are (a) physically similar, (b) statistically independent, and (c) genuinely parallel (bidirectional switching, no hierarchy). No obvious remaining candidates.

**Z₅-only domains (new thread):** The 刺熱論 (素問 ch.32) claims organ diseases worsen on 克-element days — a direct Z₅ prediction without Q₃ structure. The test is Z₅-as-edge-typing (2×5 contingency: does the pairwise 克 relation between organ element and day element predict symptom direction?), not Z₅-as-group (spectral periodicity). Currently lacks available data — no existing dataset combines daily symptom tracking with TCM organ classification at sufficient scale.

### Methodological lessons

1. **Front-load axis independence screening.** Verify MI(axis_i, axis_j) < 0.1 before building transition analysis. The volume-as-liquidity failure (MI=0.346) cost one iteration.

2. **Use vertex-conditional null, not independence null.** On Q₃, the graph topology creates edge-type clustering via vertex neighborhoods. Naive null models overestimate the significance of type-level patterns.

3. **Partition test before GMS.** The partition test (η²≈0) identifies the mechanism (S₃ breaking); the GMS test alone only shows the outcome. Both are needed but partition is more informative.

4. **Timescale is a parameter, not a choice.** M1 varies from 0.44 (8h) to 0.79 (1h). The "right" timescale is the one where single-axis transitions dominate — shorter bars resolve multi-axis jumps.

5. **Check for common factors before assuming independence.** Axes that share a meta-variable (like 陰/陽 subsuming all three 八纲 axes) will show correlated occupation even if pairwise MI is moderate. The structural test is: can each axis flip independently while the others are held fixed?

6. **Verify bidirectionality.** If transitions on an axis are predominantly one-directional (表→里 but rarely 里→表), that axis does not participate in Q₃ walk dynamics. Check both transition directions empirically.

---

## Open Questions

- D2.1–D2.4: Quantum measurement typing (parked, expected empty)
- Whether Z₅ alone (decoupled from Q₃) has empirical content — the 刺熱論 disease timing is a candidate test (currently no data)
- Whether any Q₃-compatible domain exists, given the three-condition criterion
- Whether the grammar is fundamentally specific to the I Ching's abstract trigram space — Z₅ as a typological classification of static configurations, not a dynamical law
