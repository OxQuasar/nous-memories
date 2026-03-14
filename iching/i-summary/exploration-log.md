# Open Questions Exploration Log

## Session: 2026-03-14

### Questions Investigated (Iteration 6 — final)
- **C1-C2:** Formal proof of nuclear rank sequence for all n ≥ 2

---

## C1-C2: Nuclear Rank Sequence — PROVEN

### What was tested

Attempted to upgrade the nuclear rank formula from "verified at n=3,4,5,6" to "proven for all n ≥ 2." The approach: express the nuclear shear matrix M in a factored basis, block-triangularize, and prove the rank formula algebraically.

### What was found

**PROVEN for all n ≥ 2.** Five-step proof, each step verified computationally at n=2,...,10:

**Step 1 — Factored basis decomposition.** In the basis {p₀,...,p_{n-1}, q₀,...,q_{n-1}} where p_j = L_{j+1} (lower, bottom-to-top) and q_j = L_{2n-j} (upper, top-to-bottom), the nuclear matrix has symmetric block form:
```
M = [S  E]    S = superdiagonal shift, E = e_{n-1}·e_{n-1}^T
    [E  S]
```

**Step 2 — Block triangularization.** The involutory change of basis σ = p ⊕ q gives:
```
M' = [T  E]    where T = S + E = "shift + stay"
     [0  T]
```

**Step 3 — rank(T^k) = max(1, n−k).** T has a fixed point: T^{n-1}(e_{n-1}) = 𝟏 (all-ones), and T(𝟏) = 𝟏. This prevents nilpotency. ker(T^k) = span{e₀,...,e_{min(k,n-1)-1}} (outermost coordinates killed by outward shift).

**Step 4 — Key lemma: Φ_k · ker(T^k) = {0}.** The off-diagonal coupling Φ_k = Σ T^l · E · T^{k-1-l} annihilates the kernel of T^k. Mechanism: ker(T^k) is supported on outer levels; the rank-1 gate E = e_{n-1}·e_{n-1}^T only passes the innermost component. Outer levels never reach the inner gate — "orthogonal support."

NOTE: The natural first attempt (im(Φ_k) ⊆ im(T^k)) is FALSE. The correct statement is weaker but sufficient: Φ_k vanishes on ker(T^k).

**Step 5 — Rank formula.** ker(M'^k) = ker(T^k) × ker(T^k), so:
```
rank(M^k) = 2n − 2·dim(ker(T^k)) = 2·max(1, n−k) = max(2, 2n−2k)  ∎
```

### What it means

This is the first general-n theorem in the corpus about the nuclear shear. Key corollaries:

1. **Uniform rank drop of 2 per iteration** — one bit killed from position, one from orbit — regardless of n.
2. **Stabilization at rank 2 after n−1 steps.** The stable image F₂² consists of the alternating-bit vectors (at n=3: {坤坤, 既濟, 未濟, 乾乾}).
3. **The all-ones fixed point** of T prevents nilpotency. Without the innermost coupling E, the pure shift S would be nilpotent (rank → 0). The shear i ↔ ī creates the persistent attractor.
4. **The σ = p ⊕ q coordinate** (measuring position-orbit agreement) evolves independently as T, converging to 𝟏: all levels eventually carry the sum-parity of the innermost pair.

### Status: PROVEN (theorem-level, all n ≥ 2)

Files: `c1c2_proof_v2.py` (verification n=2..10), `proof_nuclear_rank.md` (formal proof document)

---

## Session: 2026-03-13 (continued)

### Questions Investigated (Iterations 4-5)
- **NQ4:** Hamming syndrome structure at (4,13) — the decorated object
- **NQ1:** Is 凶's dual-coupling prevalence-driven?
- **C1-C2:** Nuclear rank sequence at n=5,6
- **Q5:** 彖傳 as systematic anomaly detector

---

## NQ4: Hamming Syndrome Structure at (4,13) [PRIMARY]

### What was tested

At (n=4, p=13): 7 non-Frame complement pairs form PG(2,F₂) = the Fano plane. The kernel flip patterns generate RM(1,3) ⊂ (Z₂)⁷. Identification: this is the [7,4,3] Hamming code. The Fano-plane labeling of complement pairs IS the parity-check matrix H (3×7, columns = nonzero vectors of F₂³).

**Prediction:** The 8 Hamming syndrome classes classify the 960 orbits into 8 groups of 120 (orientation × assignment product decomposition).

**Computation:** Enumerated all 92,160 surjections within one type distribution, computed orientation vectors, Hamming syndromes, and grouped by full orbits under Kernel × Aut(Z₁₃).

### What was found

**VERIFIED:**
- The kernel flip patterns ARE Hamming codewords — all 8 have syndrome 0.
- The Hamming parity-check matrix H correctly classifies orientation vectors into 8 syndrome classes.
- Syndrome distribution over all 92,160 surjections is perfectly uniform: 11,520 per syndrome (12.5% each).
- 64 of 128 possible orientation vectors are realized (constrained by Type-0 pair → v[0] = 0 always).
- 8 distinct orientation vectors per syndrome class.

**SURPRISE — THE 8 × 120 PRODUCT FAILS:**
- Each of the 960 full orbits visits exactly **6 of 8 syndromes**, not 1.
- The missing 2 syndromes always form a Z₂ pair: {0,1}, {2,3}, {4,5}, or {6,7}.
- Missing-pair distribution is perfectly symmetric: 240 orbits per class.
- Correct factorization: **960 = 4 × 240**, not 8 × 120.

### Mechanism: Type-0 Defect

**PROVEN:** The kernel flip patterns are Hamming codewords in the raw F₂⁷ theory. But the Type-0 pair (pair 1, assigned value 0) creates a "stuck bit": when a kernel element with λ(1)=1 acts, the raw flip has flip[0]=1, but f(14) = −f(1) = −0 = 0, so the orientation at position 0 doesn't actually flip. The *effective* flip differs from the raw flip at position 0 (forced to 0).

Since H·e₀ = (1,0,0) = syndrome 1, the effective flip has syndrome 0 or 1 (not just 0). Half the kernel (λ(1) = 0) preserves syndromes; half (λ(1) = 1) shifts by ⊕1. This creates the Z₂ pairing: {0,1}, {2,3}, {4,5}, {6,7}.

**Negation (α = 12)** flips all non-Type-0 positions → flip pattern (0,1,1,1,1,1,1) → syndrome shift ⊕1. Same shift as the kernel desynchronization, so negation doesn't reach new cosets.

**Higher Aut(Z₁₃) elements** (α = 2, 3, ...) permute values within negation pairs in assignment-dependent ways. Each orbit visits exactly 3 of the 4 Z₂ cosets, leaving one missing.

### Within-orbit syndrome distributions

Two sub-types exist within each missing-pair class:

| Sub-type | Count per class | Syndrome distribution |
|----------|----------------|----------------------|
| Uniform | 96 orbits | 16 surjections per syndrome |
| Biased | 144 orbits | (8, 8, 8, 8, 32, 32) per syndrome |
| **Total** | **240 orbits** | |

### Thread 1: Biased orbit internal geometry (RESOLVED)

**Q1: Do overrepresented syndromes form Z₂ pairs?** Yes — 576/576 (100%).

**Q2: Do the 144 biased orbits split 48×3?** Yes — perfect 48×3 for all 4 classes.

| Missing pair | Uniform | Biased | Over=(0,1) | Over=(2,3) | Over=(4,5) | Over=(6,7) |
|-------------|---------|--------|------------|------------|------------|------------|
| {0,1} | 96 | 144 | — | 48 | 48 | 48 |
| {2,3} | 96 | 144 | 48 | — | 48 | 48 |
| {4,5} | 96 | 144 | 48 | 48 | — | 48 |
| {6,7} | 96 | 144 | 48 | 48 | 48 | — |

Complete classification: **960 = 4 × [96 + 3 × 48] = 4 × 240 = 384 + 576**

**Q3: Does 96/144 correlate with shared negation pair?** No — both types use all 6 frame value pairs. Distinction is intrinsic to the Aut(Z₁₃) action.

**Q4: Kernel vs Aut decomposition within orbits:**
- Kernel generates syndrome orbits of size 2: {s, s⊕1}
- Uniform: Aut distributes 2/12 per syndrome (perfectly even)
- Biased: Aut concentrates 4/12 at overrepresented syndromes (vs 1/12 at others)

### Thread 2: Type-distribution dependence (RESOLVED)

| Config | Type-0 pair | Fano point | Predicted shift | Actual Z₂ pairing | Match? |
|--------|------------|------------|----------------|-------------------|--------|
| Original | pair 1 | 001 | ⊕1 | {0,1},{2,3},{4,5},{6,7} | ✓ |
| Config 2 | pair 3 | 011 | ⊕3 | {0,3},{1,2},{4,7},{5,6} | ✓ |
| Config 3 | pair 4 | 100 | ⊕4 | {0,4},{1,5},{2,6},{3,7} | ✓ |

The syndrome pairing is canonically determined by the Type-0 Fano point: shift = H·e_j. Since GL(3,F₂) acts transitively on Fano points, the 4-fold structure is universal up to this symmetry.

### What it means

The Hamming code IS the correct object at (4,13), but the Type-0 constraint creates a defect that halves its distinguishing power from 8-fold to 4-fold.

**Key insight:** At (3,5), the same Type-0 defect exists but has no room to manifest — RM(1,2) already fills the orientation space entirely. At (4,13), the 3-dimensional gap (7−4=3) provides room for the defect to create structure. This is a quantitative refinement of why (3,5) is rigid.

**The three-way interaction is genuinely novel:** Code structure (Hamming ⊂ (Z₂)⁷) × fiber-type constraint (stuck bit) × codomain symmetry (Aut(Z₁₃)). This doesn't arise in classical coding theory where domain and codomain share a characteristic.

### Status: RESOLVED

---

## NQ1: Prevalence Power Simulation

### What was tested

Simulated 384-row datasets for prevalences π ∈ {0.05, 0.10, 0.135, 0.20, 0.30, 0.50}, with core ΔR²≈0.063 and shell ΔR²≈0.117, 1000 replicates each.

### What was found

| Prevalence π | Core Power | Shell Power | Dual Power |
|-------------|-----------|------------|-----------|
| 0.050 | 0.257 | 0.239 | 0.069 |
| 0.100 | 0.433 | 0.337 | 0.163 |
| **0.135** | **0.510** | **0.443** | **0.223** |
| 0.200 | 0.655 | 0.594 | 0.391 |
| 0.300 | 0.770 | 0.718 | 0.558 |
| 0.500 | 0.806 | 0.821 | **0.661** |

**13.5% is NOT a sweet spot.** Power monotonically increases. 凶's dual-coupling at only 22% power (while 吉 at 31% prevalence with much higher power shows no dual coupling) means the effect is large and genuine.

### Status: RESOLVED — "Why 凶?" is semantic, not statistical.

---

## C1-C2: Nuclear Rank Sequence (initial verification)

Verified rank(M^k) = max(2, 2n−2k) at n=3,4,5,6. Stable image = F₂² = 4 alternating-bit elements at all tested n. (Later upgraded to full proof — see Session 2026-03-14 above.)

---

## Q5: 彖傳 Anomaly Detection

| Basin | n_hex | 剛 | 柔 | 剛/柔 ratio | Yang % |
|-------|-------|-----|-----|------------|--------|
| Kun | 16 | 15 | 7 | **2.14** | 33.3% |
| Cycle | 32 | 30 | 20 | 1.50 | 50.0% |
| Qian | 16 | 15 | 12 | **1.25** | 66.7% |

**✓ PERFECT MONOTONIC: Kun > Cycle > Qian**, inverse to yang-content. The 彖傳 is an anomaly detector operating on binary (Z₂) structure — it highlights what's structurally unusual.

### Status: RESOLVED (measured, not proven — small sample)

---

## Session: 2026-03-13 (prior iterations)

### Questions Investigated
- **Q4:** Why exactly two text-algebra bridges? (from open-questions.md)
- **Q8:** Does the Z₅-decorated Fano plane appear in existing mathematics? (from open-questions.md)

---

## Q4: Why Exactly Two Bridges?

### What was tested

**Iteration 1: Exhaustive bridge scan** — 99 (algebraic coordinate × text marker) pairs across all 384 yaoci, with CMH position-control and bridge-control.

**Iteration 2: Logistic regression model comparison** — Nested logistic regressions predicting each marker from position, core, and shell.

**Iteration 3: Full marker coupling profiles** — All 11 markers classified by coupling type.

### What was found

**Three-tier coupling structure:**
1. **凶 → core + shell** (dual-coupled, R² = 22.6%). Only marker responding to both projections.
2. **吉, 利 → shell only** (R² ≈ 6-10%). Track relational context, blind to inner structure.
3. **7/11 markers → uncoupled** (~64%). Placement is textual/contextual only.

Basin × 凶 is the sole Bonferroni-surviving bridge (CMH p = 4.1×10⁻⁵). ~89% of text variance is algebraically independent. Valence hypothesis (negative markers → core) NOT significant (p = 0.186); effect is 凶-specific.

### Status: RESOLVED

---

## Q8: The Decorated Fano Plane in Existing Mathematics

### What was found

**No name exists.** Cross-characteristic gap (F₂ → Z₅) + uniqueness at (3,5) → nothing to classify → no name needed. Best description: trivial ⊕ standard of S₄ over GF(5). Flat-direction partition (15 = C(3,2)×5) is derivative of fiber shape.

### Status: RESOLVED (definitive negative)

---

## Final Combined Status

| Q# | Question | Status | Key Finding |
|----|----------|--------|-------------|
| Q4 | Why exactly two bridges? | **Resolved** | Three-tier coupling: 凶 dual, 吉/利 shell-only, 7/11 uncoupled |
| Q8 | Decorated Fano plane? | **Resolved (negative)** | No name; cross-characteristic gap |
| NQ1 | 凶 prevalence-driven? | **Resolved** | NOT prevalence-driven; power monotonically increasing |
| NQ4 | (4,13) decorated object | **Resolved** | Hamming [7,4,3] + Type-0 defect → 960 = 4×(96+3×48). Universal under GL(3,F₂). |
| C1-C2 | Nuclear rank formula | **Proven** | rank(M^k) = max(2, 2n−2k) for all n ≥ 2. Formal proof via block triangularization. |
| Q5 | 彖傳 anomaly detection | **Resolved** | Perfect monotonic across all basins |

## All New Results (this investigation)

| # | Result | Status |
|---|--------|--------|
| R69 | Hamming syndrome at (4,13): [7,4,3] code + Type-0 defect → 4×240 | Verified (exhaustive) |
| R69a | Biased orbit 48×3 split + type-distribution rotation | Verified (exhaustive, 3 configs) |
| R70 | 凶 dual-coupling not prevalence-driven | Measured (simulation, 6000 reps) |
| R71 | Nuclear rank sequence: PROVEN for all n ≥ 2 | **Theorem** |
| R72 | 彖傳 剛/柔 anomaly detection confirmed | Measured (exhaustive count) |

---

## Final Synthesis

### What the investigation accomplished

Three iterations resolved six open questions and upgraded one conjecture (C1-C2) to a theorem. The investigation touched three domains: pure algebra (nuclear rank proof), cross-characteristic coding theory (Hamming syndrome at (4,13)), and text-algebra interface (凶 prevalence, 彖傳 anomaly detection).

### Evidence tiers

The corpus now has three clean evidence tiers:

**Tier 1 — Theorems** (5 results, proven for all parameters): R55 (uniqueness), R57 (RM filling), R63 (char-2), R64 (GL maximization), R71 (nuclear rank). These are closed — no further computation can strengthen them.

**Tier 2 — Exhaustive verifications** (R56, R66, R69/R69a): All cases checked at specific parameters. As strong as finite computation allows.

**Tier 3 — Measured effects** (R70, R72, bridge structure): Statistical, finite sample. The algebra is invulnerable; the text-algebra interface is measured, not proven. The weakest links are exactly where the object touches human authorship.

### The three-tier evidence structure mirrors the three-tier coupling structure

- Tier 1 (theorems) = the algebraic core — facts about F₂, Z₅, and their interaction
- Tier 2 (verifications) = the first non-trivial decoration — complete at specific parameters
- Tier 3 (measurements) = the text-algebra interface — real but fragile

### What remains open

Nothing that internal computation can resolve. The remaining questions are either interpretive (NQ2: 利 > 吉 semantics), require external data (NQ3: rank-2 × 吉 in independent corpus), or are deprioritized (NQ5: completism, Q7: unfalsifiable). The investigation has reached its natural boundary.

### Key insight from the (4,13) analysis

The Type-0 defect mechanism — where the Hamming code's classifying power is halved by a fiber-type constraint — provides a quantitative refinement of why (3,5) is rigid. Rigidity at (3,5) is not just "the code fills the space" but "the code fills the space even after accounting for the stuck bit." This three-way interaction of code structure, fiber constraint, and cross-characteristic symmetry is genuinely novel.

### Key insight from the nuclear rank proof

The orthogonal support lemma — ker(T^k) is supported on outer levels, E filters only the innermost — is the structural explanation for why the rank formula works. The natural but false approach (im(Φ_k) ⊆ im(T^k)) was corrected to the weaker but sufficient claim (Φ_k vanishes on ker(T^k)). The all-ones fixed point 𝟏 of T = S+E is the mechanism preventing nilpotency — the innermost coupling creates the persistent attractor.
