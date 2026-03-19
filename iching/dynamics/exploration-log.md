# Dynamics Investigation — Exploration Log

## Iteration 1: Semantic Laplacian and Walsh Spectrum (Probe D1)

### Entry Point

Q11–Q15 ask whether the line-change transition graph (Q₆ hypercube) has dynamical structure in the semantic manifold. Prior nulls (R192, R209) established that 五行 edge labels (克/生/比和) carry no semantic information. This iteration tests vertex-level flow structure via the graph Laplacian.

### Method

**Step 1: Walsh spectral decomposition.** Projected 64×1024 centered hex-level BGE-M3 embeddings onto Walsh-Hadamard basis of Q₆. Measured variance fraction per eigenspace (7 groups by Hamming weight). Permutation null: 1000 label shuffles.

**Step 2: Laplacian field analysis.** Computed Lap(h) = mean(neighbor embeddings) − emb(h).
- 2a: ||Lap(h)|| distribution vs permutation null
- 2b: Complement Laplacian anti-parallelism (cosine of Lap(h) and Lap(63−h) for 32 pairs)
- 2c: Algebraic correlates of ||Lap(h)||

All steps repeated in residual space. Cross-model check on E5-large for Step 2b.

Script: `d1_laplacian_walsh.py`

### Results

**Walsh spectrum near-flat with weight-3 enrichment (97.9th %ile).** Weight-1 depleted (4.4th), weight-4 depleted (5.0th). No low-pass or high-pass concentration.

**Complement Laplacian anti-parallelism: fails cross-model.** BGE-M3 raw marginal (5th %ile, mean cosine −0.033). E5-large: 26th %ile. The complement involution is static opposition, not flow opposition.

**No algebraic correlates of Laplacian magnitude.** All p > 0.12.

**Residual anti-smooth at 0th percentile.** The non-algebraic content actively differentiates adjacent hexagrams.

→ R253 (dynamics negative)

### Side finding

The weight-3 enrichment led to the manifold identification (R254–R256), which is a Q1 result, not a dynamics result. Those iterations are recorded in `reversal/exploration-log.md` Phase 9.

---

## What Has Been Tested vs What Hasn't

**Tested:** Semantic Laplacian flow — whether the thematic manifold has sources/sinks/flow on the transition graph. One operationalization of "the I Ching models dynamics." Result: negative.

**Not tested (see questions.md):**
- Inverse methods (Koopman, SINDy, symbolic regression)
- Symbolic dynamics / shift spaces
- Abstract transition graph topology (without embeddings)
- External comparison to actual situational dynamics
- Literature survey on dynamical systems with 64-state codings
- φ at stability boundaries (KAM connection)
- Bifurcation frequency ratios vs 1:2:3
