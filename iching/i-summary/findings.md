# I Ching Open Questions Investigation — Complete Findings

## Investigation Overview

Three iterations across two sessions (2026-03-13, 2026-03-14), investigating six open questions from the I Ching structural research corpus. Six questions resolved, one conjecture upgraded to theorem. 77 total results across 10 workflows, zero contradictions.

---

## Results Summary

| # | Result | Evidence Tier | Status |
|---|--------|--------------|--------|
| R69 | Hamming syndrome structure at (4,13): [7,4,3] code + Type-0 defect → 4×240 | Exhaustive verification | Verified |
| R69a | Biased orbit 48×3 split + type-distribution rotation under GL(3,F₂) | Exhaustive verification (3 configs) | Verified |
| R70 | 凶 dual-coupling not prevalence-driven | Statistical simulation (6000 reps) | Measured |
| R71 | Nuclear rank formula: rank(M^k) = max(2, 2n−2k) for all n ≥ 2 | Algebraic proof + computational verification (n=2..10) | **Theorem** |
| R72 | 彖傳 剛/柔 anomaly detection: perfect monotonic across basins | Exhaustive text count | Measured |

---

## R69: Hamming Syndrome Structure at (4,13)

### Statement

At (n=4, p=13), the 960 orbits of complement-equivariant surjections (within a fixed type distribution, under Stab(1⁴) × Aut(Z₁₃)) are classified by the [7,4,3] Hamming code with a Type-0 defect:

**960 = 4 × (96 + 3 × 48) = 4 × 240**

### Structure

The 7 non-Frame complement pairs form PG(2,F₂) = the Fano plane. The kernel flip patterns (under the pair-fixing subgroup of Stab(1⁴)) generate the first-order Reed-Muller code RM(1,3) ⊂ (Z₂)⁷, which IS the [7,4,3] Hamming code. The Fano-plane labeling of complement pairs is the Hamming parity-check matrix H (3×7, columns = nonzero vectors of F₂³).

The Hamming syndrome s = Hv ∈ F₂³ classifies orientation vectors v ∈ (Z₂)⁷ into 8 cosets. However, the expected 8×120 product decomposition fails because:

1. **Type-0 defect:** The Type-0 pair (both representatives map to 0) creates a "stuck bit" — when a kernel element flips this pair algebraically, the orientation doesn't actually change (0 = −0). Half the kernel preserves syndromes; half shifts by ⊕(H·e_j) where j is the Type-0 column. This pairs syndromes: e.g., {0,1}, {2,3}, {4,5}, {6,7} when Type-0 is at Fano point 001.

2. **Aut(Z₁₃) coset hopping:** Non-negation automorphisms (α = 2, 3, ...) permute values within negation pairs in assignment-dependent ways. Each orbit visits exactly 3 of the 4 Z₂ cosets, leaving one "missing pair."

### Classification table

| Missing Z₂ pair | Uniform orbits | Biased orbits (3 sub-classes of 48) | Total |
|-----------------|---------------|-------------------------------------|-------|
| {s, s⊕d} class 1 | 96 | 48 + 48 + 48 | 240 |
| {s, s⊕d} class 2 | 96 | 48 + 48 + 48 | 240 |
| {s, s⊕d} class 3 | 96 | 48 + 48 + 48 | 240 |
| {s, s⊕d} class 4 | 96 | 48 + 48 + 48 | 240 |

Where d = H·e_j (the syndrome of the Type-0 Fano point).

- **Uniform orbits** (384 total): 16 surjections per syndrome across 6 present syndromes.
- **Biased orbits** (576 total): (8, 8, 8, 8, 32, 32) — one Z₂ pair 4× overrepresented. The overrepresented pair is always a Z₂ pair, and the 144 biased orbits per class split 48×3 among the three non-missing Z₂ pairs (Z₃-symmetric).

### Universality

Verified across 3 type distributions (Type-0 at Fano points 001, 011, 100):
- The Z₂ pairing rotates with the Type-0 Fano point as predicted by H·e_j
- The 4×240 structure is preserved in all cases
- The 96/144 uniform/biased split is preserved in all cases
- The structure is canonical under GL(3,F₂), which acts transitively on Fano points

### Significance

The three-way interaction of code structure (Hamming ⊂ (Z₂)⁷), fiber-type constraint (stuck bit at Type-0), and cross-characteristic symmetry (Aut(Z₁₃)) is genuinely novel — it doesn't arise in classical coding theory where domain and codomain share a characteristic.

At (3,5), the same Type-0 defect exists but is masked: RM(1,2) fills the entire orientation space (Z₂)³, so the defect cannot create observable structure. This is a quantitative refinement of rigidity: the code fills the space *even after accounting for the stuck bit*.

---

## R70: 凶 Dual-Coupling is Not Prevalence-Driven

### Statement

The unique dual-coupling of 凶 (danger marker) to both core (basin) and shell (surface_relation, rank, palace_element) algebraic coordinates cannot be explained by its prevalence (13.5% = 52/384 yaoci). The dual-detection power curve is monotonically increasing — higher prevalence always means more power.

### Evidence

Power simulation: 384-row datasets, 1000 replicates × 6 prevalences, with effect sizes matching observed ΔR²_core ≈ 0.063 and ΔR²_shell ≈ 0.117.

| Prevalence π | Core Power | Shell Power | Dual Power |
|-------------|-----------|------------|-----------|
| 0.050 | 0.257 | 0.239 | 0.069 |
| 0.100 | 0.433 | 0.337 | 0.163 |
| **0.135** | **0.510** | **0.443** | **0.223** |
| 0.200 | 0.655 | 0.594 | 0.391 |
| 0.300 | 0.770 | 0.718 | 0.558 |
| 0.500 | 0.806 | 0.821 | 0.661 |

At 凶's prevalence (13.5%), dual-detection power is only 22%. The fact that 凶's dual coupling was detected at all — while 吉 at 30.7% prevalence (58% dual power) shows NO dual coupling — means 凶's effect size is genuinely larger on the core projection. "Why 凶?" is answered semantically: danger is more algebraically constrained than fortune.

---

## R71: Nuclear Rank Theorem

### Statement

**Theorem.** For all n ≥ 2, let M be the 2n×2n nuclear extraction matrix over F₂. Then:

rank(M^k) = max(2, 2n − 2k) for all k ≥ 1.

### Proof (5 steps)

**Step 1 — Factored basis.** In the basis {p₀,...,p_{n-1}, q₀,...,q_{n-1}} where p_j = L_{j+1} (lower, bottom-to-top) and q_j = L_{2n-j} (upper, top-to-bottom):
```
M = [S  E]    S = n×n superdiagonal shift, E = e_{n-1}·e_{n-1}^T
    [E  S]
```
Verified n = 2,...,8.

**Step 2 — Block triangularization.** Q = [I 0; I I] is involutory over F₂. M' = QMQ = [T E; 0 T] where T = S + E. Verified n = 2,...,8.

**Step 3 — rank(T^k) = max(1, n−k).** By induction: T^k(e_{n-1}) = Σ_{i=max(0,n-1-k)}^{n-1} e_i. At k = n−1: T^{n-1}(e_{n-1}) = 𝟏 (all-ones), a fixed point. ker(T^k) = span{e₀,...,e_{min(k,n-1)-1}}. Verified n = 2,...,8 with explicit kernel basis checks.

**Step 4 — Key lemma: Φ_k · ker(T^k) = {0}.** For M'^k = [T^k Φ_k; 0 T^k], the off-diagonal Φ_k = Σ_{l=0}^{k-1} T^l·E·T^{k-1-l} annihilates ker(T^k). Proof: For e_j ∈ ker(T^k), the factor T^{k-1-l}(e_j) is either 0 or e_{j-k+1+l} with j-k+1+l < n-1. Since E = e_{n-1}·e_{n-1}^T only passes the (n-1)-th component, E·e_{j-k+1+l} = 0. Every term vanishes. Verified n = 2,...,8 for all k.

NOTE: The natural first attempt im(Φ_k) ⊆ im(T^k) is FALSE. The correct and sufficient claim is that Φ_k vanishes on ker(T^k).

**Step 5 — Rank formula.** ker(M'^k) = {(x,y) : T^k·y = 0, T^k·x + Φ_k·y = 0}. By Step 4: y ∈ ker(T^k) ⟹ Φ_k·y = 0 ⟹ T^k·x = 0. Hence ker(M'^k) = ker(T^k) × ker(T^k).

rank(M'^k) = 2n − 2·min(k, n−1) = max(2, 2n − 2k). ∎

Verified by explicit rank computation at n = 2,...,10.

### Corollaries

1. **Uniform rank drop:** Each iteration kills exactly 2 dimensions (one position, one orbit), regardless of n.
2. **Stabilization:** rank = 2 for all k ≥ n−1. Stable image = F₂² ⊂ F₂^{2n}.
3. **Attractor:** The stable image {0, p_{n-1}, q_{n-1}, p_{n-1}+q_{n-1}} = alternating-bit vectors. At n=3: {坤坤, 既濟, 未濟, 乾乾}.
4. **Anti-nilpotency:** T = S+E has fixed point 𝟏. Without the rank-1 coupling E, the pure shift S is nilpotent (S^n = 0) → rank → 0. The innermost shear prevents collapse.
5. **σ-coordinate independence:** σ_j = p_j ⊕ q_j evolves as Tσ, converging to 𝟏. All levels eventually carry the sum-parity of the innermost pair.

---

## R72: 彖傳 Anomaly Detection

### Statement

The 彖傳's 剛/柔 (firm/yielding) usage ratio is perfectly monotonic inverse to basin yang-content:

| Basin | n_hex | 剛 | 柔 | 剛/柔 ratio | Yang % |
|-------|-------|-----|-----|------------|--------|
| Kun | 16 | 15 | 7 | **2.14** | 33.3% |
| Cycle | 32 | 30 | 20 | 1.50 | 50.0% |
| Qian | 16 | 15 | 12 | **1.25** | 66.7% |

The 彖傳 systematically comments on what's structurally unusual: yang in yin-dominant hexagrams, yin in yang-dominant ones. This identifies the 彖傳 as an **anomaly detector operating on the binary (Z₂) structure**, consistent with the semantic-map finding that the 彖傳 sees Z₂ but not Z₅.

### Caveat

Raw numbers are small (60 剛, 39 柔 across 64 hexagrams). The perfect monotonic ordering across 3 non-overlapping basins is noteworthy but not statistically proven at conventional significance thresholds.

---

## Evidence Quality Assessment

### Tier 1 — Theorems (proven for all parameters)
- R55: Uniqueness at (3,5) — orbit formula = 1
- R57: RM fills orientation space iff n = 3
- R63: Char-2 uniqueness
- R64: GL Maximization at q = 2
- **R71: Nuclear rank formula** — rank(M^k) = max(2, 2n−2k) ∀n ≥ 2

### Tier 2 — Exhaustive verifications (all cases at specific parameters)
- **R69/R69a: Hamming syndrome at (4,13)** — all 92,160 surjections, 3 type distributions
- R56: Regular action at (3,5) — all 96 surjections
- R66: Five-orbit decomposition at (3,5) — all 240 surjections

### Tier 3 — Measured effects (statistical, finite sample)
- **R70: 凶 not prevalence-driven** — 6000 simulated replicates, clean monotonic curve
- **R72: 彖傳 anomaly detection** — 99 data points, perfect monotonic ordering
- Bridge structure (凶 dual, 吉/利 shell-only) — one Bonferroni-surviving, several sub-threshold

Tier 3 is where honest caveats belong. The algebra (Tiers 1-2) is invulnerable. The text-algebra interface (Tier 3) is measured, not proven.

---

## Questions Resolved

| Q# | Question | Status | Key Finding |
|----|----------|--------|-------------|
| Q4 | Why exactly two bridges? | **Resolved** | Structurally bounded (R5), empirically saturated, semantically asymmetric. Three-tier coupling: 凶 dual, 吉/利 shell-only, 7/11 uncoupled. |
| Q8 | Decorated Fano plane? | **Resolved (negative)** | No name. Cross-characteristic gap + uniqueness → nothing to classify. Best description: trivial ⊕ standard of S₄ over GF(5). |
| NQ1 | 凶 prevalence-driven? | **Resolved** | NOT prevalence-driven. Power monotonically increasing. "Why 凶?" is semantic. |
| NQ4 | (4,13) decorated object | **Resolved** | Hamming [7,4,3] + Type-0 defect → 960 = 4×(96+3×48). Canonical under GL(3,F₂). |
| C1-C2 | Nuclear rank formula | **Proven** | rank(M^k) = max(2, 2n−2k) for all n ≥ 2. Block triangularization + orthogonal support lemma. |
| Q5 | 彖傳 anomaly detection | **Resolved** | 剛/柔 perfectly monotonic inverse to yang-content across all basins. |

## Remaining Open Questions

| Q# | Question | Priority | Blocker |
|----|----------|----------|---------|
| NQ3 | Rank-2 × 吉 signal (p=0.008, not Bonferroni) | Medium | Needs independent corpus |
| NQ2 | 利 > 吉 shell coupling | Low | Interpretive (philology) |
| Q6 | 說卦傳 non-compass attributes | Low | Testable but low-value |
| Q3 | 納甲 modification history | Low | Historical-philological |
| Q7 | Visibility ceiling as feature | Dropped | Unfalsifiable (2/5 = arithmetic) |
| NQ5 | Cross-characteristic GBF class | Dropped | Completism (one interesting point) |

---

## Files

| File | Contents |
|------|----------|
| `work/nq4_hamming_syndrome.py` | Initial Hamming syndrome computation |
| `work/nq4_deeper.py` | Deeper syndrome analysis |
| `work/nq4_followup.py` | Follow-up: within-orbit syndrome distributions |
| `work/nq4_thread1_biased.py` | Biased orbit internal geometry (48×3 split) |
| `work/nq4_thread2_typedep.py` | Type-distribution dependence (3 configs) |
| `work/nq1_prevalence_power.py` | Prevalence power simulation |
| `work/c1c2_nuclear_rank.py` | Initial nuclear rank verification (n=3..6) |
| `work/c1c2_proof_v2.py` | Complete proof verification (n=2..10) |
| `work/proof_nuclear_rank.md` | Formal proof document |
| `work/q5_tuanzhuan_anomaly.py` | 彖傳 anomaly detection check |
| `exploration-log.md` | Full iteration-by-iteration record |
| `summary.md` | Updated research summary |
