# Open Questions — Computation Results

## Q4: Exhaustive Bridge Scan

### Setup
99 (coordinate × marker) pairs tested across 384 yaoci records.
- 9 algebraic coordinates (4 core, 5 shell projection)
- 11 markers (≥5 occurrences; 利貞 and 利涉大川 dropped as too rare)
- Tests: raw chi²/Fisher → CMH position-controlled → bridge-controlled

### Results: The bridge landscape is NOT isolated to two pairs

**Bonferroni survivors (p < 5.05×10⁻⁴): exactly 2 pairs**

| Pair | CMH p | CMH OR | Bridge p |
|------|-------|--------|----------|
| basin × 凶 | 4.08×10⁻⁵ | 0.24 (Cycle basin) | 1.41×10⁻⁴ |
| i_component × 凶 | 4.08×10⁻⁵ | 4.25 (component 0) | 1.41×10⁻⁴ |

These two are the same signal: i_component is a binary re-encoding of basin (Cycle basin = i_component 0). The identical CMH p-values confirm this.

**CMH-significant at p < 0.05: 12 pairs total**

Core projection (3 pairs, all driven by 凶):
1. basin × 凶: p=4.08×10⁻⁵, OR=0.24 at Cycle basin ← **PRIMARY BRIDGE**
2. i_component × 凶: p=4.08×10⁻⁵ (same signal as #1)
3. hu_relation × 凶: p=2.85×10⁻³, OR=2.67 at 比和 — marginally survives bridge control (p=0.037)

Shell projection (9 pairs, broader signal):
4. rank × 咎: p=6.72×10⁻³, OR=8.11 at rank 7
5. rank × 吉: p=7.86×10⁻³, OR=2.42 at rank 2
6. shi × 吉: p=7.86×10⁻³, OR=2.42 at shi=2 (same signal as #5: rank 2 ↔ shi line 2)
7. **surface_relation × 吉**: p=1.70×10⁻², OR=0.45 at 克体 ← **SECONDARY BRIDGE** (but note: best level is 克体, not 生体!)
8. rank × 利: p=2.00×10⁻², OR=2.55 at rank 2
9. shi × 利: p=2.00×10⁻², (same signal as #8)
10. surface_relation × 悔: p=4.35×10⁻², OR=3.62 at 体克用
11. palace_element × 利: p=4.62×10⁻², OR=1.94 at Metal
12. surface_relation × 无咎: p=4.68×10⁻², OR=1.84 at 克体

**All 12 pairs survive bridge control** — none are absorbed by the cross-projection bridge.

### Key Findings

**F1: Core projection is clean — one bridge dominates.**
Basin × 凶 is the only Bonferroni-surviving core signal. The hu_relation × 凶 signal (比和 ↔ 凶) is secondary and barely survives bridge control (p=0.037). This makes sense: 比和 in nuclear structure correlates with basin membership (both reflect inner-trigram similarity).

**F2: Shell projection is richer than predicted — NOT a single bridge.**
The prediction was "surface_relation × 吉 (生体) alone." Reality: at least 4 independent shell signals survive position control, driven by different coordinates and markers:
- rank/shi at level 2 → 吉 and 利 (rank-2 hexagrams are associated with favorable markers)
- surface_relation → 吉 (but best contrast is 克体 LOW, not 生体 HIGH)
- rank 7 → 咎 (highest rank hexagrams attract blame markers)
- palace_element Metal → 利

**F3: SURPRISE — The surface_relation×吉 bridge is not exactly 生体→吉.**
The CMH pairwise breakdown for surface_relation × 吉:
- 克体: CMH p=0.017, OR=0.446 ← strongest (克体 SUPPRESSES 吉)
- 生体: CMH p=0.032, OR=1.875 (生体 elevates 吉, but weaker)
- 比和: CMH p=0.083, OR=0.574 (not significant)

The bridge is better described as "克体 suppresses 吉" than "生体 promotes 吉." The original finding (F7 in semantic-map findings) reported 生体 as the driver — this scan shows the contrast is really driven by 克体's low rate.

**F4: Rank 2 is a significant shell-side signal independent of surface_relation.**
Rank 2 (三世卦, third-generation palace member) shows OR=2.42 for 吉 and OR=2.55 for 利, surviving both position and basin bridge controls. This is NOT absorbed by the surface_relation bridge — it represents an additional channel.

**F5: Multiple-testing caveat.** 
After Bonferroni, only 2 pairs survive (both basin × 凶 in different encodings). All shell signals are p=0.007–0.047, significant nominally but not after strict correction. The shell projection has weak, distributed associations rather than one clean bridge.

### Raw numbers for primary bridges

**Basin × 凶 (core, Bonferroni-significant):**
| Basin | N lines | 凶 count | 凶 rate |
|-------|---------|----------|--------|
| Kun | 96 | 20 | 20.8% |
| Cycle | 192 | 12 | 6.2% |
| Qian | 96 | 20 | 20.8% |

Cycle basin has one-third the 凶 rate of Kun/Qian basins (6.2% vs 20.8%). This is the strongest text-algebra bridge in the entire system.

**Surface relation × 吉 (shell, nominal significance):**
| Relation | N lines | 吉 count | 吉 rate |
|----------|---------|----------|--------|
| 生体 | 72 | 30 | 41.7% |
| 体克用 | 78 | 29 | 37.2% |
| 体生用 | 72 | 25 | 34.7% |
| 比和 | 84 | 19 | 22.6% |
| 克体 | 78 | 15 | 19.2% |

生体 has the highest rate (41.7%), 克体 the lowest (19.2%). The CMH flagged 克体 as best contrast because the binary split "克体 vs rest" (19.2% vs ~34%) is more extreme than "生体 vs rest" (41.7% vs ~28%). Both describe the same gradient.

**Rank × 吉 (shell, nominal significance):**
| Rank | N lines | 吉 count | 吉 rate |
|------|---------|----------|--------|
| 0 | 48 | 9 | 18.8% |
| 1 | 48 | 10 | 20.8% |
| **2** | **48** | **23** | **47.9%** |
| 3 | 48 | 16 | 33.3% |
| 4 | 48 | 14 | 29.2% |
| 5 | 48 | 13 | 27.1% |
| 6 | 48 | 17 | 35.4% |
| 7 | 48 | 16 | 33.3% |

Rank 2 (三世卦) is a striking outlier: 47.9% 吉 vs ~30.7% overall.

---

## Q8: Decorated Fano Plane — Three Computations

### Part A: Representation Decomposition

**Result: ρ₄ ≅ trivial ⊕ standard (1 + 3 decomposition)**

The 4D representation of Stab(111) ≅ S₄ on GF(5)⁴ = {(a₁,a₂,a₄,a₇)} decomposes as:

| Irrep | Multiplicity | Dimension | Contribution |
|-------|-------------|-----------|-------------|
| trivial | 1 | 1 | 1 |
| sign | 0 | 1 | 0 |
| standard | 1 | 3 | 3 |
| sgn⊗std | 0 | 3 | 0 |
| V₂(2D) | 0 | 2 | 0 |
| **Total** | | | **4** ✓ |

Character verified: [4, 2, 0, 1, 0] matching classes (), (12), (12)(34), (123), (1234).

**The trivial subrepresentation** is the 1D space fixed by all of S₄. This corresponds to the "overall scaling" parameter — related to the complement eigenvalue.

**The standard representation** is the familiar 3D irrep of S₄ (permutation representation minus trivial). This is the space where the three coordinate parameters (a₁,a₂,a₄) act "like permutations of three things."

**Block structure:** The representation is NOT upper-triangular — a₇ mixes with (a₁,a₂,a₄). The trivial+standard decomposition is an abstract isomorphism, not a visible block structure in the (a₁,a₂,a₄,a₇) basis.

**Aut(Z₅) acts as pure scalar multiplication.** τ ∈ {1,2,3,4} sends (a₁,a₂,a₄,a₇) → τ·(a₁,a₂,a₄,a₇). This confirms the Stab(111) and Aut(Z₅) actions commute in the simplest possible way.

### Part B: Differential Uniformity

**Differential uniformity δ_f = 4.**

Derivative spectrum by direction:

| Direction a | Spectrum (Δ=0,1,2,3,4) | max | Type |
|-------------|----------------------|-----|------|
| 001 | (0,2,2,2,2) | 2 | **Flat** |
| 010 | (0,0,4,4,0) | 4 | Two-value |
| 011 | (0,4,0,0,4) | 4 | Two-value |
| 100 | (4,2,0,0,2) | 4 | Three-value with zero-peak |
| 101 | (0,2,2,2,2) | 2 | **Flat** |
| 110 | (0,0,4,4,0) | 4 | Two-value |
| 111 | (2,2,1,1,2) | 2 | **Near-flat (eigenvalue direction)** |

**Key patterns:**
- Three flat/near-flat directions: {001, 101, 111}. These have max = 2 (optimal for 8→5 maps).
- The flat directions 001, 101 are weight-1 and weight-2 vectors. Together with 111 (weight-3), they span the "diagonal" subspace {x : popcount(x) is odd} — but this isn't quite right; 001⊕101 = 100, not 111.
- Actually: {001, 101} = a Fano line. And 111 is the complement fixpoint. The flat directions are structurally special.

**Complement eigenvalue D₁₁₁f = 3f: VERIFIED for all 8 inputs.**

This means f(x⊕111) = f(x) + 3f(x) = 4f(x) = -f(x) mod 5. This is exactly the complement constraint: f(x̄) = -f(x) mod 5.

**Only the direction a=111 has eigenvalue structure.** No other direction satisfies D_a f = c·f for any constant c.

### Part C: Type-Assignment Reduction

**At (3,5): complete invariant = type assignment, 1 orbit**

The 3 non-frame complement pairs receive types {0, 1, 2} — one of each:
- {001, 110} → both Wood → type 0 (identical fibers)
- {010, 101} → Water/Fire → type 1 (singleton fibers)
- {011, 100} → Metal/Earth → type 2 (shared double-fibers)

GL(2,F₂) ≅ S₃ acts transitively on the 6 possible type assignments → 1 orbit.
RM(1,2) has dimension 3 = number of non-frame pairs → orientation fully absorbed.
**Type assignment is the complete invariant. The (3,5) object has NO residual decoration.**

**At (4,13): genuine decoration emerges**

- 7 non-frame complement pairs
- RM(1,3) has dimension 4 < 7
- Orientation orbits: 2^(7-4) = 8

**The (3,5) case is the unique point where orientation is fully absorbed.**

For all n ≥ 4: dim RM(1, n-1) = n < 2^(n-1) - 1, so residual decoration survives. The number of orientation orbits grows exponentially: 2^(2^(n-1) - 1 - n).

This is a sharp characterization: the (3,5) object sits at the exact boundary where RM codes can absorb all orientation freedom. One step higher and the object acquires genuine decoration that symmetry cannot eliminate.

---

## Shell Depth: Logistic Regression Model Comparison

### Setup
Logistic regressions predicting 吉 and 凶 from nested sets of algebraic coordinates. 384 yaoci records. McFadden pseudo-R² and likelihood ratio tests.

### Results for 吉 (prevalence 118/384 = 30.7%)

| Model | k | McFadden R² | AIC | Description |
|-------|---|------------|-----|-------------|
| M0 | 6 | 0.0574 | 458.6 | Position only |
| M1 | 8 | 0.0619 | 460.4 | Position + basin |
| M2 | 10 | 0.0887 | 451.8 | Position + surface_relation |
| M3 | 13 | 0.0874 | 458.4 | Position + rank |
| M4 | 21 | 0.1138 | 461.9 | Position + all shell |
| M5 | 23 | 0.1162 | 464.7 | Position + basin + all shell |

**Key finding: Basin adds NOTHING for 吉.** M0→M1 (add basin): LR=2.13, p=0.344, not significant. M4→M5 (add basin to shell): LR=1.15, p=0.562, not significant. Basin is irrelevant for predicting 吉.

**Shell coordinates matter collectively.** M0→M4 (add all shell): LR=26.7, p=0.031. Surface_relation alone (ΔR²=+0.031) and rank alone (ΔR²=+0.030) contribute nearly equally. Combined shell ΔR²=+0.056 — less than additive, suggesting partial overlap.

**Only one coefficient survives in the full model:** line_position=2 (trad. line 3, inner trigram top), β=−1.57, OR=0.21, p=0.003. No shell coordinate achieves individual significance at p<0.05 in the full model — the shell signal is distributed, not concentrated.

### Results for 凶 (prevalence 52/384 = 13.5%)

| Model | k | McFadden R² | AIC | Description |
|-------|---|------------|-----|-------------|
| M0 | 6 | 0.0654 | 296.6 | Position only |
| M1 | 8 | 0.1287 | 281.4 | Position + basin |
| M2 | 10 | 0.0950 | 295.6 | Position + surface_relation |
| M3 | 13 | 0.1039 | 298.9 | Position + rank |
| M4 | 21 | 0.1827 | 290.9 | Position + all shell |
| M5 | 23 | 0.2263 | 281.6 | Position + basin + all shell |

**Basin dominates 凶 prediction.** M0→M1: LR=19.3, p=6.5×10⁻⁵. Basin alone (ΔR²=+0.063) exceeds any single shell coordinate. In the full model, basin=Qian (OR=4.36, p=0.002) and basin=Kun (OR=3.80, p=0.005) are the strongest predictors.

**Shell adds significant incremental signal.** M1→M5 (shell given basin): LR=29.7, p=0.013. And basin adds to shell: M4→M5: LR=13.3, p=0.001. The projections carry **independent** information for 凶.

**Full model achieves R²=0.226** — substantial for this kind of data. Significant coefficients: basin=Qian/Kun, palace_element=Water, surface_relation=体生用/生体 (both suppress 凶).

### The Asymmetry

| | 吉 | 凶 |
|---|---|---|
| Basin ΔR² | +0.005 (NS) | **+0.063** (p<10⁻⁴) |
| Surface_relation ΔR² | **+0.031** (p=0.005) | +0.030 (p=0.06) |
| Rank ΔR² | **+0.030** (p=0.048) | +0.039 (p=0.11) |
| Combined shell ΔR² | **+0.056** (p=0.031) | +0.117 (p=0.002) |
| Full model R² | 0.116 | **0.226** |

**凶 is more predictable than 吉.** Basin is a strong predictor for 凶 but irrelevant for 吉. Shell coordinates contribute to both but are individually weak. The full model explains twice as much variance for 凶 (22.6%) as for 吉 (11.6%).

### Interaction Test

Rank × surface_relation interaction could not be tested (singular matrix): rank-2 hexagrams only have surface_relations {生体, 体生用}, never {克体, 比和, 体克用}. This is a structural confound — rank and surface_relation are partially entangled through the palace system.

Within rank-2 hexagrams, comparing the two available surface relations:
- 生体: 54.2% 吉 (13/24) vs 体生用: 41.7% 吉 (10/24)
- Neither subsample significantly differs from the same surface_relation at other ranks (Fisher p=0.14 and p=0.44).

**The rank-2 effect and surface_relation effect cannot be fully disentangled** because they share structural zeros in their cross-tabulation.

---

## Flat-Direction Uniformity (15 × 16 partition)

### Setup
For each of the 240 complement-equivariant surjections F₂³ → Z₅, compute which of the 7 nonzero directions in F₂³ are "flat" (max derivative count ≤ 2, optimal diffusion).

### Result: Exactly 15 patterns, each containing exactly 16 surjections

| # | Pattern type | Count | Flat dirs | Stab size |
|---|-------------|-------|-----------|-----------|
| 3 | 4-flat (complementary pairs) | 3 × 16 = 48 | 4 | 8 |
| 12 | 3-flat (including 111) | 12 × 16 = 192 | 3 | 2 |

**Total: 15 patterns × 16 surjections = 240.** The partition is perfectly uniform.

### Two orbits under Stab(111)

The 15 patterns form **2 orbits** under Stab(111) ≅ S₄:

**Orbit A (3 patterns, 48 surjections):** Patterns with 4 flat directions, none including 111. The three patterns are:
- {001, 010, 101, 110} — the 4 "mixed" directions (complement pairs of Fano lines)
- {001, 011, 100, 110}
- {010, 011, 100, 101}

Each has stabilizer of order 8 (a copy of D₄ inside S₄).

**Orbit B (12 patterns, 192 surjections):** Patterns with 3 flat directions, always including 111 (the complement direction). The IC pattern {001, 101, 111} belongs here.

Each has stabilizer of order 2 (generated by the identity and one involution).

**Orbit-stabilizer theorem verified:** 3 × 8 = 12 × 2 = 24 = |S₄|. ✓

### Aut(Z₅) preserves flat-direction patterns

Scaling f by τ ∈ {1,2,3,4} does not change which directions are flat. This is expected: scaling values preserves the distribution shape over Z₅.

### Surjection orbits

Under the full group Stab(111) × Aut(Z₅) (order 96): **5 orbits** (sizes 96, 48, 48, 24, 24). The IC orbit has size 96 and spans all 12 patterns in Orbit B.

Under Stab(111) alone (order 24): **17 orbits**. The Aut(Z₅) action merges groups of orbits.

### IC pattern {001, 101, 111} — detail

The 16 surjections sharing the IC pattern all have fiber type {2,2,2,1,1} — two elements with double fibers, two with single fibers, confirming this is the IC orbit's type class.

**Stabilizer of the IC pattern:** order 2, generated by the identity and the matrix that swaps bit 2 (i.e., the involution fixing bits 0,1 and complementing bit 2). In terms of the Fano plane, this is the unique involution that fixes the Fano line {001, 101} (where 001 ⊕ 101 = 100).

**Structural characterization:** The IC flat directions {001, 101, 111} form a set where:
- 001 and 101 lie on a common Fano line ({001, 100, 101})
- 111 is the complement direction (eigenvalue direction)
- They do NOT form a Fano line (001 ⊕ 101 = 100 ≠ 111)

Three Fano lines pass through pairs of these directions, each containing exactly 2/3 flat directions. The flat set is "almost a line" — two points on a line plus the complement point.

---

## Marker Coupling Profiles

### Setup
For each marker with ≥8 occurrences (11 markers total), fit logistic regressions:
- Model 0: position only (baseline)
- Model A: position + basin (core projection)
- Model B: position + shell (surface_relation + rank + palace_element)
- Model C: position + basin + shell (full)

For sparse markers (<15 occurrences: 悔, 亨, 咎), the shell model is reduced to surface_relation only (full shell has 21 parameters, too many for 8-13 events).

### Coupling profile table

| Marker | N | Valence | ΔR²_core | ΔR²_shell | ΔR²_total | Core p | Shell p | Type |
|--------|---|---------|----------|-----------|-----------|--------|---------|------|
| 吉 | 118 | positive | +0.005 | +0.056 | +0.059 | 0.344 | **0.031** | Shell-only |
| 无咎 | 84 | positive | +0.007 | +0.046 | +0.060 | 0.223 | 0.230 | None |
| 貞 | 71 | neutral | +0.005 | +0.043 | +0.046 | 0.414 | 0.385 | None |
| 凶 | 52 | negative | **+0.063** | **+0.117** | **+0.161** | **6.5×10⁻⁵** | **0.002** | **Dual** |
| 利 | 51 | positive | +0.006 | +0.098 | +0.108 | 0.437 | **0.013** | Shell-only |
| 厲 | 26 | negative | +0.030 | +0.050 | +0.092 | 0.058 | 0.853 | None† |
| 吝 | 20 | negative | +0.002 | +0.079 | +0.081 | 0.845 | 0.646 | None† |
| 悔亡 | 18 | neutral | +0.016 | +0.071 | — | 0.308 | 0.804 | None† |
| 悔 | 13 | negative | — | +0.059 | — | — | 0.152 | None‡ |
| 亨 | 8 | positive | +0.028 | +0.068 | +0.089 | 0.341 | 0.260 | None‡ |
| 咎 | 8 | negative | +0.074 | +0.130 | +0.205 | 0.057 | **0.038** | Shell-only‡ |

† Full shell model may be unreliable (events/parameters ≈ 1.0)
‡ Sparse marker — reduced shell model (surface_relation only)

### Key findings

**F6: 凶 is the ONLY dual-coupled marker.**
凶 is the only marker with significant associations to BOTH core (basin, p=6.5×10⁻⁵) and shell (p=0.002) projections. Moreover, core and shell carry independent information: core-given-shell p=0.001, shell-given-core p=0.013. Overlap is modest (+0.020), confirming the two projections capture distinct aspects of 凶 placement.

**F7: No marker is Core-only.**
Not a single marker reaches significance on core projection alone. Basin coupling is exclusive to 凶 — all other markers have p>0.05 for the basin model.

**F8: Shell-only markers are 吉, 利, and (marginally) 咎.**
These markers show significant shell coupling but no core coupling. 利 has the strongest pure shell signal (ΔR²=+0.098, p=0.013). 吉 follows (ΔR²=+0.056, p=0.031). Both are "favorable" markers — shell coordinates help predict where positive assessments appear.

**F9: Most markers show NO algebraic coupling.**
7 of 11 markers (无咎, 貞, 厲, 吝, 悔亡, 悔, 亨) have no significant association with either projection after position control. These markers are placed by textual/contextual logic, not algebraic structure.

**F10: 厲 nearly reaches core significance (p=0.058).**
厲 (danger/severity) is the closest to a second core-coupled marker, with ΔR²_core = +0.030. Combined with shell, it reaches ΔR²_total = +0.092 — but neither projection alone is significant. This is suggestive but underpowered.

### Hypothesis test: negative vs positive core coupling

**Hypothesis:** Negative/warning markers (凶, 咎, 厲, 悔, 吝) are more core-coupled than positive/affirmative markers (吉, 利, 亨, 无咎).

| | Positive (4) | Negative (5) |
|--|--|--|
| Mean ΔR²_core | 0.011 | 0.034 |
| Mean ΔR²_shell | 0.067 | 0.087 |

Negative markers show 3× higher mean core coupling (+0.034 vs +0.011). But:
- **Permutation test p = 0.186** — not significant at α=0.05.
- The effect is driven almost entirely by 凶 (ΔR²_core=0.063) and 咎 (0.074). Remove either and the difference vanishes.
- Shell coupling does not differ significantly between valence groups (p=0.169).

**Conclusion:** The trend exists but is not significant with only 9 markers. The hypothesis that negative markers are more algebraically constrained is **suggestive but unconfirmed** — it rests on 凶 being an extreme outlier rather than a systematic valence effect.

### Coupling landscape

The 2D scatter (ΔR²_core, ΔR²_shell) reveals:
- **凶 is an outlier** — high on both axes, far from all other markers
- **咎 is similar but sparse** — high core and shell but only 8 occurrences
- **利 is a pure shell marker** — low core, high shell
- **The majority cluster near the origin** — low coupling on both axes

This is NOT the predicted pattern of "negative=core, positive=shell." Instead: **凶 alone occupies dual space**, positive markers cluster in shell-only or none, and most negative markers show no significant coupling at all.

---

## Synthesis

1. **The "exactly one bridge per projection" prediction is PARTIALLY confirmed.** Core projection has exactly one bridge (basin × 凶), clean and Bonferroni-significant. Shell projection has a diffuse constellation of weak signals, not a single clean bridge. The surface_relation × 吉 signal exists but is weaker and surrounded by other shell signals (rank, palace_element) of comparable strength.

2. **凶 is more algebraically constrained than 吉.** Logistic regression confirms the asymmetry: the full model explains 22.6% of 凶 variance vs 11.6% of 吉 variance. Basin alone accounts for 6.3% of 凶 variance (p<10⁻⁴) but only 0.5% of 吉 (NS). 凶 placement respects algebraic structure; 吉 placement is more textually autonomous.

3. **Shell coordinates are weakly additive.** Surface_relation and rank each contribute ~3% ΔR² for 吉, but combined shell gives only 5.6% (not 6%). Rank and surface_relation are partially confounded through the palace system — rank-2 hexagrams can only have surface_relations {生体, 体生用}, never {克体, 比和, 体克用}. This structural entanglement prevents clean disentanglement of shell-side signals.

4. **The 240 surjections partition into 15 × 16 by flat-direction pattern.** This is a clean combinatorial fact: every pattern contains exactly 16 surjections. The patterns form 2 orbits under Stab(111): 3 patterns with 4 flat directions (none including 111) and 12 patterns with 3 flat directions (all including 111). The IC pattern belongs to the larger orbit.

5. **The representation decomposition ρ₄ ≅ trivial ⊕ standard** provides clean mathematical vocabulary: the surjection space splits into a 1D "scale" (trivial) and a 3D "shape" (standard S₄ representation). The 5 orbits of surjections correspond to points in GF(5)⁴ modulo this group action.

6. **The differential uniformity δ_f = 4** and the eigenvalue D₁₁₁f = 3f = -f (complement constraint as eigenvalue) place the IC surjection in the vocabulary of cross-characteristic cryptographic functions. The complement direction 111 is the unique eigenvalue direction — and it always belongs to the flat set (for all 192 surjections in the IC-type orbit).

7. **The (3,5) type-assignment is a complete invariant** because RM(1,2) exactly fills the orientation space. This is the combinatorial reason for the single orbit in the IC type class: there is simply no room for decoration.

8. **凶 is uniquely dual-coupled; no other marker has core coupling.** The marker coupling landscape is sparse and asymmetric: 凶 alone bridges both projections, positive markers weakly couple to shell, and most markers (~64%) show no algebraic coupling at all. The hypothesis that negative markers are systematically more core-coupled is suggestive (3× higher mean) but not significant (p=0.19) — it rests on 凶 being an extreme outlier rather than a category-level effect.

---

## Status

Both Q4 and Q8 are **resolved**. See `exploration-log.md` for the full iteration history, interpretive synthesis, and new questions generated.

**Q4 resolution:** Three-tier coupling (凶 dual-coupled R²=23%, 吉/利 shell-only R²≈6-10%, 7/11 markers uncoupled). The "two bridges" count is upper-bounded by R5 (2 projections). The bound is saturated asymmetrically: one clean core bridge + one diffuse shell contact zone.

**Q8 resolution:** Definitive negative. The object (complement-equivariant surjection F₂³ → Z₅) falls in a cross-characteristic gap between GBF and finite geometry communities, and its decoration is unique at (3,5), eliminating classification need. Best mathematical description: trivial ⊕ standard of S₄ over GF(5).
