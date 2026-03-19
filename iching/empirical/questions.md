# Empirical Investigation — Questions

> The theoretical structure is complete. The I Ching provides a grammar: three transition types (continuation/generation/destruction) with a forbidden-pattern constraint and a one-way valve. Does this grammar produce useful predictions when applied to real systems?

## E1: Does the Three-Type Classification Predict Transition Character?

Take any system with identifiable states and observable transitions. Classify the transitions using the 五行 grammar:
- **Continuation** (比和): transition between states of the same type
- **Generation** (生): transition between adjacent types in a cycle
- **Destruction** (克): transition between non-adjacent types

Does the classification correlate with observable properties of the transition — its smoothness, duration, reversibility, or cost?

The prediction from the algebra: generation transitions should be smoother/cheaper than destruction transitions. Continuation should be the most stable. If the classification carries no information about the transition's character, the grammar has no predictive power.

## E2: Does the Forbidden-Pattern Constraint Hold?

The GMS constraint says: consecutive destruction is forbidden without an intervening non-destructive step. In formal terms, no 克-克 bigram.

Take systems with time-series of classified transitions. Count bigram frequencies. Is 克-克 suppressed relative to a null model (random transitions with the same marginal frequencies)?

This is the most falsifiable prediction. If consecutive destructive transitions occur at base rate, the constraint doesn't apply. If they're suppressed, the grammar captures something real about how destructive change works.

## E3: Does the Valve Hold?

The valve (R262): destruction never directly produces generation (克→生 = 0 in the directed subgraph). Destruction must pass through continuation before generation can resume.

In a classified time-series: after a destructive transition, does the system always pass through a neutral/continuation phase before a generative transition occurs? Or can destruction immediately flip to generation?

This is testable independently of E2. The valve is a directed constraint — it's about the ordering of transition types, not just their co-occurrence.

## E4: Is the Grammar System-Independent?

The strongest claim: the three-type classification with GMS constraint works across domains. The same grammar should apply to ecological succession, market regimes, political transitions, and physiological states — because the grammar is about the abstract structure of transitions, not the specific content.

Test by applying E1–E3 across multiple domains. If the constraint holds in ecology but not finance, the grammar is domain-specific. If it holds across domains, it's capturing something about how multi-state systems transition in general.

## E5: Does Coarse-Graining Preserve the Grammar?

The 互 map (RG) coarse-grains 64 states → 16 → 4. Does the three-type classification survive coarse-graining? If you observe a system at high resolution and classify transitions, then observe the same system at low resolution, do the classifications agree?

This tests whether the grammar is scale-invariant — whether it describes the same transition structure at different levels of detail. If coarse-graining destroys the classification, the grammar only works at one resolution.

## E6: Does Single-Step Outperform Multi-Step?

Phase 8 found that type information decorrelates in 1–2 steps (R288). The grammar should be predictive for the *next* transition but not for transitions 3+ steps ahead.

Test: given a current state and transition type, how well does the grammar predict the type of the next transition vs the transition after that? If prediction accuracy drops sharply after 1 step, the theory is confirmed. If it persists, Phase 8's composability result needs revisiting.

## Methodology Notes

- The mapping from empirical categories to 五行 types is the critical step and the main source of bias. Multiple independent mappings should be tested.
- The null model for E2/E3 must account for marginal transition frequencies — the question is whether bigram suppression exceeds what base rates predict.
- Domain selection should prioritize systems with clear state boundaries and high transition counts. Political regime data (Polity IV) and ecological regime shifts are strongest candidates.
- The grammar should be tested blind — classify transitions first, check predictions second. Not the reverse.
