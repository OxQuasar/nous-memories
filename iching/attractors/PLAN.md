# Attractor Probe — 互 as Dimensional Reduction

## Status: COMPLETE

All core probes (01-07) finished. Results in `findings.md`.
Probe 08 (ordering comparison) assessed as low-value — attractor framing already established (p≈5×10⁻⁷).

## Key Result

互 is a linear map M: F₂⁶ → F₂⁶ with minimal polynomial x²(x+1)².
Inner map formula: (i₀,i₁,i₂,i₃) → (i₁,i₂,i₁,i₂).
Three-layer onion: outer(b₀,b₅) → shell(b₁,b₄) → interface(b₂,b₃).
Each 互 step peels one layer. Interface bits are the sole survivors.

## Speculations Resolved

- S1 (生 cycle): Refuted — bit-algebraic, not elemental
- S2 (rank 4, kernel = outer): Confirmed — inner rank is 2
- S3 (depth ~ complexity): Weakened — 75% at depth-2, uniform across basins
- S4 (feeder trees = 五行): Derivative — forced by overlap constraint
- S5 (京房 = fiber): Refuted — palaces orthogonal to convergence

## Execution Log

```
Phase A (structural):
  01_functional_graph.py    — 64-node graph, perfect balance, depth {0:4, 1:12, 2:48}
  02_information_cascade.py — F₂ algebra, min poly x²(x+1)², eigenspaces
  03_inner_orbits.py        — 16-node inner space, formula, feeder geometry

Phase B (overlays):
  04_trigram_projection.py  — trigram pairs, overlap constraint, 京房 test (S5 refuted)
  05_kw_depth_walk.py       — depth profile, 1:3:12 uniformity, central clustering
  07_convergence_fivephase.py — attractor elements, 比和 forcing, S1/S4 resolved

Skipped:
  06 — merged into 02 (spectral = F₂ matrix analysis)
  08 — low marginal value (attractor framing already quantified)
```
