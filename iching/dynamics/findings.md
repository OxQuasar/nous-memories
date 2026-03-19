# Dynamics Investigation — Findings

> Entry point: the I Ching as a representational map to the dynamics of situational change.
> Questions Q11–Q15 in `questions.md`.

## Results

### R253: Dynamical Flow Hypothesis — Negative

**[measured]** Walsh spectral decomposition of hex-level embeddings on Q₆ is near-flat. Three deviations: weight-1 depleted (4.4th %ile), weight-4 depleted (5.0th %ile), weight-3 enriched (97.9th %ile).

**[measured]** Complement Laplacian anti-parallelism: BGE-M3 raw marginal (5th %ile, mean cosine −0.033), E5-large fails cross-model replication (26th %ile). No algebraic property predicts Laplacian magnitude (all p > 0.12). No semantic flow structure on the transition graph.

**[measured]** 克/生/比和 classification null at vertex level (extending edge-level nulls R192, R209).

Script: `d1_laplacian_walsh.py`

## Results Moved to reversal/

R254 (weight-3 eigenspace identification), R255 (dimensional pressure), R256 (Krawtchouk unification) are manifold characterization results. They answer "what is the ~16-dim thematic manifold?" — a reversal/Q1 question. Relocated to `reversal/findings.md` Phase 9.

Scripts moved to `reversal/Q1/phase9_weight3_verification.py`, `reversal/Q1/phase9_krawtchouk_unification.py`

## What R253 Tested and What It Didn't

**Tested:** Whether the semantic manifold has flow structure on the line-change graph (Laplacian divergence, complement anti-parallelism, algebraic correlates of flow). One specific operationalization of "the I Ching models dynamics."

**Not tested:**
- Inverse methods: inferring dynamical properties from the transition graph structure (Koopman operator, SINDy, symbolic regression)
- Symbolic dynamics: whether the 64-state transition graph matches any known dynamical system's symbolic coding
- Abstract graph topology: bifurcation structure, basin topology, attractor characterization of the transition graph itself (not through embeddings)
- External comparison: actual situational dynamics data vs I Ching structure
- The broader hypothesis that the I Ching discretizes a space of dynamics in a non-flow sense
