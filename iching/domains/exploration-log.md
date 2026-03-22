# Domains — Exploration Log

## Iteration 1: Q₃ Edge-Coloring Orbit Structure & Inverse Approach

**Question:** The grammar (GMS, valve, complement-Z₅) classifies Q₃ edges as 比和/生/克. How does this classification transform under axis assignment (Aut(Q₃))? How many distinct predictions does the grammar make? Can the typing be recovered from observed edge types alone (inverse approach)?

**Script:** `q3_edge_orbits.py`

### Part 1: Aut(Q₃) Orbit Structure — Measured

- Aut(Q₃) = S₃ ⋉ (Z₂)³, order 48 (6 axis permutations × 8 polarity flips)
- **24 distinct edge-coloring patterns** in the orbit, stabilizer size 2
- Stabilizer = {identity, complement map v→v⊕111}. Complement preserves edge types because type classes {0}, {1,4}, {2,3} are closed under negation.
- **All 24 patterns have identical edge-count distribution: 比和=2, 生=4, 克=6.** No axis assignment changes this ratio.
- **No 生↔克 swap pair exists within the orbit.** The swapped patterns (比和=2, 生=6, 克=4) are valid surjections but not reachable by any Q₃ automorphism. 克-dominance (6/12 edges) is an invariant of the domain-relevant symmetry group.
- **All 24 patterns verified:** 克 subgraph = 2×P₄, 生 subgraph = 2×P₃, 比和 subgraph = 2×K₂.

### Part 2: Full Surjection Landscape — Measured

- 240 complement-equivariant surjective functions F: F₂³ → Z₅
- 192 are shape A ({2,2,2,1,1} fiber partition), 48 are shape B ({4,1,1,1,1})
- **102 distinct edge-coloring patterns** across all 240 functions
- Decomposition by (比和, 生, 克) edge counts:

| Edge counts | Shape A functions | Shape B functions | Distinct colorings | In Aut(Q₃) orbit |
|---|---|---|---|---|
| (2,4,6) | 48 | 24 | 36 | 24 |
| (2,6,4) | 48 | 24 | 36 | 0 |
| (0,4,8) | 48 | 0 | 15 | 0 |
| (0,8,4) | 48 | 0 | 15 | 0 |

- **Aut(Q₃) orbit is NOT exhaustive.** 78 colorings lie outside the orbit. These arise from GL(3,F₂) shearing maps (in Stab(111) but not in Aut(Q₃)) and Z₅ automorphisms that swap 生↔克.
- The Aut(Q₃) orbit = exactly the 24 shape A colorings with (2,4,6). It occupies one geometric locus: shape A with Q₃-adjacent doublet pairs.
- The (0,\*,\*) patterns (30 colorings, all shape A) have doublet pairs at non-adjacent Q₃ positions. These cannot arise from genuine independent binary axes — they require nonlinear axis entanglement (shearing).
- The 生↔克 swap pairs partition perfectly: (2,4,6)↔(2,6,4), (0,4,8)↔(0,8,4). No self-dual patterns.

### Minimal Determining Set — Measured

- Q₃'s 12 edges form 6 complement pairs. Complement edges always carry the same type (equivariance).
- **Minimum 6 edges** (one per complement pair) needed to distinguish all 102 colorings.
- **64 = 2⁶ minimal determining sets**, each a transversal of the 6 complement pairs.
- **Within the 24 Aut(Q₃) colorings only: 5 edges suffice** (192 determining sets of size 5). One complement pair is redundant if the (2,4,6) distribution is already known.

### Structural Implications — Proven from computation

1. **克-dominance is invariant under all axis assignments.** For any domain with 3 independent binary axes, the Z₅ grammar classifies exactly 6/12 single-axis transitions as 克 (destructive), 4/12 as 生 (generative), 2/12 as 比和 (continuation). No axis relabeling or polarity choice changes this.

2. **The constraint is on sequencing, not frequency.** Destructive transitions are the most common type. The GMS forbids consecutive 克→克 steps along each P₄ path, not the occurrence of 克 transitions individually.

3. **The (0,\*,\*) colorings serve as an axis-independence diagnostic.** If observed data produces an edge coloring in the 78-element complement (outside Aut(Q₃)), the domain's axes are not genuinely independent binary oppositions.

4. **The inverse approach requires complete data.** All 6 independent edge observations are needed to uniquely determine the coloring among the 102 possibilities. Reduced to 5 if the domain is known to have genuine binary axes.

### What Remains Untested

- Explicit market regime edge classification under the canonical axis assignment (which specific transitions are 克, 生, 比和 in market terms)
- The two P₄ paths through market regime space and their GMS-forbidden sequences
- Whether market regime transitions are predominantly single-axis (Q₃ edges) — prerequisite M1
- Whether 克→克 bigrams are suppressed in market data — the core GMS test
- Whether the valve (克→生 = 0) holds in market transitions
- TCM 八纲辨证 mapping verification — whether the traditional 五行 assignment matches the canonical typing
- Statistical power: ~30-40 transitions estimated sufficient for GMS detection under non-backtracking null (not verified by simulation)

---

## Iteration 2: Market Regime Predictions & Axis-Type Alignment

**Question:** Under the canonical axis assignment (b₀=trend, b₁=volatility, b₂=liquidity), what specific market transitions are classified as 克/生/比和? What are the GMS-forbidden sequences? What null rate does GMS suppress against?

**Script:** `market_regime_predictions.py`

### Regime Typing — Measured

| Regime | Binary | Trigram | Element |
|--------|--------|---------|---------|
| Quiet decline | 000 | 坤 | 土 |
| Grinding rally | 001 | 震 | 木 |
| Panic/capitulation | 010 | 坎 | 水 |
| Short squeeze | 011 | 兌 | 金 |
| Slow bleed | 100 | 艮 | 土 |
| Healthy bull | 101 | 離 | 火 |
| Correction | 110 | 巽 | 木 |
| Euphoria | 111 | 乾 | 金 |

### Two P₄ 克-Paths — Measured

1. Panic/capitulation(水) →克→ Quiet decline(土) →克→ Grinding rally(木) →克→ Short squeeze(金)
2. Slow bleed(土) →克→ Correction(木) →克→ Euphoria(金) →克→ Healthy bull(火)

Each P₄ alternates volatility and trend flips: vol→trend→vol.

### Axis-Type Alignment — Measured

Each Q₃ axis contributes 4 edges. The type distribution by axis:

| Axis | 克 | 生 | 比和 |
|------|---|---|-----|
| Volatility (b₁) | **4** | 0 | 0 |
| Trend (b₀) | 2 | 2 | 0 |
| Liquidity (b₂) | 0 | 2 | **2** |

**One axis is pure-克 (volatility), one is pure non-克 (liquidity), one is mixed (trend).** This (4/2+2/2+2) partition is structurally invariant across all 24 Aut(Q₃) patterns — it follows from the P₄ path structure. Which physical axis occupies each role depends on the bit assignment.

Under the canonical assignment: every volatility regime change is destructive; no liquidity regime change is destructive. Trend changes are mixed (destructive from 土 and 木 vertices, generative from 水 and 火 vertices).

### 比和 Pairs — Measured

Both 比和 transitions are liquidity flips within same-element pairs:
- Quiet decline(土) ↔ Slow bleed(土): liquidity change within low-vol downtrend
- Short squeeze(金) ↔ Euphoria(金): liquidity change within high-vol uptrend

### GMS-Forbidden Sequences — Measured

4 undirected (8 directed) forbidden 3-step sequences, 2 per P₄ path:

**Path 1 (scarce liquidity face):**
- Panic/capitulation →克(vol)→ Quiet decline →克(trend)→ Grinding rally
- Quiet decline →克(trend)→ Grinding rally →克(vol)→ Short squeeze

**Path 2 (abundant liquidity face):**
- Slow bleed →克(vol)→ Correction →克(trend)→ Euphoria
- Correction →克(trend)→ Euphoria →克(vol)→ Healthy bull

All forbidden sequences involve a volatility flip immediately followed by a trend flip, or vice versa. Liquidity transitions are never part of any forbidden sequence.

### Null P(克→克) — Measured

Under uniform random walk on Q₃ (each of 3 neighbors equally likely). P(克→克) varies by P₄ position: internal vertices (克-degree 2) have higher null rate than endpoints (克-degree 1).

| Vertex | Element | P₄ position | 克-neighbors | P(克→克) |
|--------|---------|-------------|-------------|---------|
| Quiet decline (000) | 土 | internal | 2 of 3 | 0.3333 |
| Grinding rally (001) | 木 | internal | 2 of 3 | 0.3333 |
| Correction (110) | 木 | internal | 2 of 3 | 0.3333 |
| Euphoria (111) | 金 | internal | 2 of 3 | 0.3333 |
| Panic/capitulation (010) | 水 | endpoint | 1 of 3 | 0.2222 |
| Short squeeze (011) | 金 | endpoint | 1 of 3 | 0.2222 |
| Slow bleed (100) | 土 | endpoint | 1 of 3 | 0.2222 |
| Healthy bull (101) | 火 | endpoint | 1 of 3 | 0.2222 |

Average P(克→克) across all vertices: **0.2778**. Under GMS: **0**. Detection at p<0.05 requires ~11 transitions (strict null) or ~30-40 transitions (non-backtracking null).

### 生 as Bridge Type — Observed from structure

生 appears on all three axes (0+2+2 = 4 edges) but dominates none. This diffuse distribution matches the dynamics finding that 生 has the simplest algebraic structure (pure kernel, zero coherent content, R283) and the most context-free interpretive character (8c.2: "creator depletes regardless"). The bridge character at Q₃ edge level is the geometric origin of 生's algebraic simplicity — it connects everything without privileging any axis or direction.

### Structural Implications

1. **Axis-selection criterion.** Before testing GMS, identify which market axis has uniformly disruptive transitions. If volatility fits (all vol flips are empirically "hard"), the canonical assignment is supported. This is cheaper than full GMS testing.

2. **GMS is localized to a 2-axis subspace.** The forbidden sequences involve only volatility and trend flips. Liquidity transitions are never 克 and never participate in forbidden patterns. GMS constrains the vol×trend plane only.

3. **土-element regimes have highest 克 exposure.** Quiet decline and Slow bleed (both 土, low-vol) have 2/3 neighbors connected by 克 edges. These "calm" regimes sit at the interior of the P₄ paths, making them the most constrained by GMS.

### What Remains Untested

- Whether market regime transitions are predominantly single-axis (M1 prerequisite)
- Whether volatility flips are empirically the most uniformly disruptive axis (axis-selection test)
- Whether 克→克 bigrams are suppressed in market data (GMS test)
- Whether the valve holds after 克 transitions
- The same analysis for TCM 八纲辨证 (which axis is pure-克 in the medical domain?)
- Statistical power simulation (the ~30-40 estimate is analytical, not simulated)

---

## Iteration 3: Axis-Type Alignment — Algebraic Proof

**Question:** Why is one axis always pure-克? Is the (4/2+2/2+2) axis-type partition forced by the algebra, and if so, what mechanism produces it?

**Script:** `market_regime_predictions.py` (axis alignment verification section)

### The Doublet Alignment Invariant — Proven

The {2,2,2,1,1} fiber partition has three doublets. In the canonical surjection, two doublets are Q₃-adjacent (Hamming distance 1) and one is a complement pair (Hamming distance 3). Both adjacent doublets always sit on the SAME axis. This is forced: complement equivariance maps each adjacent doublet to the other, requiring both to cross the same face boundary.

**Verified computationally:** All 24 Aut(Q₃) patterns confirm the pure-克 axis is always orthogonal to the doublet alignment axis (24/24).

### Function Census — Measured

Among 192 shape A functions:
- **96 functions** have profile (1,1,3): two adjacent doublets + one complement doublet → 48 in Aut(Q₃) orbit
- **96 functions** have profile (2,2,3): zero adjacent doublets (doublets at Hamming distance 2) → 0 in Aut(Q₃) orbit (these are the shearing extras)

The Aut(Q₃) orbit contains EXACTLY the functions with adjacent doublet pairs.

### Axis-Type Alignment Theorem — Proven

**Theorem.** In any {2,2,2,1,1} complement-equivariant surjection F₂³ → Z₅ with Q₃-adjacent doublets, the three axes have types:
- **Doublet axis:** 2比和 + 2生
- **Pure-克 axis:** 4克
- **Mixed axis:** 2克 + 2生

**Proof.** Doublet values form a negation pair {a, -a} with a ∈ {2,3} (QNR mod 5). Singleton values form {s₁, -s₁} with s₁ ∈ {1,4} (QR mod 5).

*Step 1 (doublet axis):* 2 edges connect doublet pairs (diff=0 → 比和). 2 edges connect singletons to complement-doublet members (diff ∈ {1,4} → 生). Profile: (B,B,S,S).

*Step 2 (remaining axes):* Each gets 2 edges with diff = a ∈ {2,3} → 克. The remaining 2 edges per axis have diffs a+s₁ (one axis) and a-s₁ (other axis).

*Step 3 (the split):* (a+s₁)(a-s₁) = a²-s₁² = 4-1 = 3 mod 5. Since (3/5) = -1 (QNR), exactly one of {a+s₁, a-s₁} is QR (生) and the other is QNR (克). So one axis collects 4/4 克, the other gets 2克+2生. ∎

### The Legendre Symbol as Type Selector — Proven

The entire axis-type structure is controlled by the Legendre symbol (·/5):
- Doublet values ∈ QNR = {2,3} → 克 distances → pure-克 axis
- Singleton values ∈ QR = {1,4} → 生 distances → bridge type
- The split: (a²-s₁²/5) = (3/5) = -1, forcing the opposite-type split on the two non-doublet axes

This connects to the R=B result from 8c-ext2.5: both the interpretation symmetry (R=B count = 56) and axis-type purity are manifestations of (3/5) = -1. Two consequences of one number-theoretic fact.

### The Z₅ Automorphism and 生↔克 Swap — Proven

Under Aut(Z₅), the element ×2 maps QNR→QR (swapping {2,3}→{4,1}). This swaps doublet values from 克-class to 生-class, turning the pure-克 axis into a pure-生 axis. This is exactly the 生↔克 swap identified in Iteration 1 — it exits the Aut(Q₃) orbit but stays in the Stab(111)×Aut(Z₅) orbit. The Aut(Q₃) orbit selects QNR-doublets; the full algebraic orbit includes QR-doublets too.

### Structural Implications

1. **The doublet alignment is the fundamental invariant.** The entire axis-type structure (pure-克, mixed, doublet) follows from knowing which axis the two adjacent doublets share.

2. **The mixed axis has EXACTLY 2克+2生.** Not approximately — the product constraint forces a perfect 2-2 split. This is a testable prediction: the non-pure, non-doublet axis should show exactly half destructive transitions.

3. **Axis identification from transition character.** For any domain: find the axis where ALL transitions are disruptive (pure-克) and the axis where NO transitions are disruptive (doublet axis). The third is mixed. No time-series needed — only transition classification.

### Empirical Testing Sequence — Derived from three iterations

- **Step 0:** Verify transitions are predominantly single-axis (M1 prerequisite)
- **Step 1:** Identify the axis where ALL transitions are disruptive → pure-克 axis
- **Step 2:** Identify the axis where NO transitions are disruptive → doublet axis
- **Step 3:** Verify the mixed axis has exactly 2/4 destructive transitions
- **Step 4:** Test GMS (no consecutive 克) on the P₄ paths (pure-克 + mixed axes)

Steps 1-3 require classifying transition character only. Step 4 requires sequential data (~30-40 transitions for detection).

### What Remains Untested

- All empirical steps (0-4) for any domain
- Whether the (4,13) case at Q₄ produces analogous axis-type alignment (structural, not domain-relevant)
- The exact QR/QNR partition structure at general (n,p) and whether it generalizes the axis-type theorem

---

## Synthesis: Three Iterations — Algebra to Prediction

**Starting question:** Does the 五行 grammar (GMS, valve, complement-Z₅) make specific, testable predictions for domains outside its native algebraic habitat?

**Answer:** Yes. The grammar makes ONE structural prediction for any Q₃ domain, invariant under all axis assignments. The prediction has three layers:

1. **Edge-count invariance (Iteration 1).** The 6:4:2 ratio (克:生:比和) is locked. No axis relabeling changes it. 克-dominance is structural, not conventional.

2. **Subgraph invariance (Iterations 1-2).** The 克 edges form 2×P₄ (two disjoint 4-vertex paths), 生 forms 2×P₃, 比和 forms 2×K₂. This determines the GMS-forbidden sequences: consecutive steps along either P₄.

3. **Axis-type alignment (Iteration 3).** One axis is always pure-克, one is never destructive (doublet axis), one is mixed at exactly 2:2. Forced by (3/5) = -1 (Legendre symbol). This is (3,5)-specific — at (4,13), (3/13) = +1 and the mechanism breaks.

**The connection to prior work:** The Legendre symbol (3/5) = -1 controls both the axis-type alignment (this investigation) and the R=B interpretation symmetry count = 56 (8c-ext2.5). Two consequences of one number-theoretic fact. The domains investigation was framed as empirical, but what it found was algebraic — the last layer of structure in the canonical surjection, visible only when projected onto Q₃ adjacency.

**Empirical testing protocol (Steps 0-4) derived:**
- Steps 1-3 (axis identification) require only transition character classification — no time-series, no data infrastructure
- Step 4 (GMS bigram test) requires ~30-40 sequential transitions
- The protocol applies to any Q₃ domain; market regimes are the first concrete target

**What was NOT found:**
- Any empirical data (all results are algebraic/computational)
- Any (4,13) structure (parked as non-domain-relevant)
- Any domain verification (the next phase)

**Scripts:** `q3_edge_orbits.py` (orbit structure, 102-coloring landscape, minimal determining sets), `market_regime_predictions.py` (explicit regime typing, P₄ paths, forbidden sequences, null model, axis-type verification).

---

## Iteration 4: First Empirical Pass — Market Regime Data Pipeline

**Question:** Do BTC market regime transitions, when classified via three binary axes on Q₃, satisfy the prerequisites for grammar testing? Specifically: (a) are transitions predominantly single-axis (M1)? (b) what is the vertex distribution? (c) does the observed edge-type distribution match the theoretical 6:4:2 ratio?

**Script:** `market_regime_data.py`

**Data:** `btc_datalog_2025-07-21_2026-02-20.csv` — 18.6M rows of 1-second BTC data, 7 months. Resampled to 4h bars.

### Data Pipeline — Built

Resampled 1-second data to 4h bars (UTC-aligned). Three binary axes constructed:

| Axis | Field | Rule | Bit |
|------|-------|------|-----|
| Trend (b₀) | `trend_4h` | positive → 1, non-positive → 0 | b₀ |
| Volatility (b₁) | `realized_vol_4h` | above 30-day rolling median → 1, below → 0 | b₁ |
| Liquidity (b₂) | `volume_4h` (sum per bar) | above 7-day rolling median → 1, below → 0 | b₂ |

Note: The planned liquidity proxy `spread_bps_1m` was degenerate — 97% zeros in early data, 100% zeros after September 2025. `volume_since_last` (summed per bar) was substituted as fallback.

### Liquidity Axis Failure — Measured

Volume-as-liquidity-proxy is strongly correlated with volatility after binarization:

| Diagnostic | Value |
|-----------|-------|
| MI(b1_vol, b2_liq) | **0.346 bits** (max = 1.0) |
| Phi correlation | **0.66** |
| Bars where vol=liq | **83.1%** |

Contingency table:
```
         liq=0   liq=1
vol=0     535      96
vol=1     122     537
```

The system lives on a Q₂ face: 83% of bars occupy the 4 regimes where vol and liquidity agree (0,1,6,7). The 4 regimes where vol and liquidity disagree (2,3,4,5) are rare transients (17% combined). The three axes are not independent — the first requirement for a testable Q₃ domain is not met with volume as the liquidity proxy.

### Alternative Liquidity Proxies — Measured

The datalog contains order book fields with full coverage and low vol correlation:

| Field | Non-zero% | Corr with vol |
|-------|-----------|---------------|
| `ob_total_ratio_1m` | 100% | -0.154 |
| `ob100_ratio_1m` | 100% | -0.036 |
| `depth_asymmetry_10` | 100% | -0.095 |
| `ob_total_ratio_5m` | 100% | -0.156 |
| `liquidity_shift_15m` | 99.3% | 0.014 |
| `ob_imbalance_slope_5m` | 99.3% | 0.006 |

Compare: `volume_since_last` has raw correlation 0.130 with vol, but after binarization by rolling median the mutual information is 0.346 bits. Order book fields (especially `ob100_ratio_1m` at -0.036 and `liquidity_shift_15m` at 0.014) may achieve genuine independence after binarization.

### M1 Prerequisite (Single-Axis Fraction) — Measured

| Metric | Value |
|--------|-------|
| Total 4h bars | 1,290 |
| Transitions | 1,289 |
| Self-loops | 374 (29.0%) |
| Q₃ edges (single-axis) | 525 (40.7%) |
| Multi-axis jumps | 390 (30.3%) |
| — Hamming 2 | 273 |
| — Hamming 3 | 117 |
| **M1 (Q₃ edges / non-self)** | **0.574** |

M1 = 57.4% is above the random baseline (~43% if transitions were uniformly distributed across all 7 non-self neighbors) but below the ~70% threshold that would indicate strong Q₃ adjacency preference. The 30% multi-axis fraction suggests the 4h timescale does not fully resolve sequential single-axis flips — shorter bars may increase M1 by resolving multi-axis jumps into sequential single-axis steps.

### Vertex Distribution — Measured

| Vertex | Bits | Trigram | Regime | Count | % |
|--------|------|---------|--------|-------|---|
| 0 | 000 | 坤 | Quiet decline | 276 | 21.4% |
| 1 | 001 | 震 | Grinding rally | 259 | 20.1% |
| 2 | 010 | 坎 | Panic/capitulation | 64 | 5.0% |
| 3 | 011 | 兌 | Short squeeze | 58 | 4.5% |
| 4 | 100 | 艮 | Slow bleed | 43 | 3.3% |
| 5 | 101 | 離 | Healthy bull | 53 | 4.1% |
| 6 | 110 | 巽 | Correction | 284 | 22.0% |
| 7 | 111 | 乾 | Euphoria | 253 | 19.6% |

Bimodal: the 4 dominant regimes (0,1,6,7 = 83%) are exactly the Q₂ face where vol=liq. This is a direct consequence of the vol-liquidity axis correlation.

### Edge-Type Distribution — Measured

Among 525 Q₃ edges:

| Type | Count | % | Theoretical (from algebra) |
|------|-------|---|---------------------------|
| 比和 | 40 | 7.6% | 16.7% (2/12) |
| 生 | 79 | 15.0% | 33.3% (4/12) |
| 克 | 406 | 77.3% | 50.0% (6/12) |

克 at 77.3% vs theoretical 50% — this is a traffic concentration artifact, not a grammar effect. Under the canonical assignment, the two 克-typed trend edges (000↔001 and 110↔111) connect the four dominant regimes. The two 生-typed trend edges (010↔011 and 100↔101) connect the four rare regimes. Since trend flips account for 70% of all single-axis transitions and the dominant regimes sit on 克-typed trend edges, 克 is mechanically inflated by the bimodal vertex distribution.

### Axis Flip Distribution — Measured

Among 525 Q₃ edges:

| Axis | Count | % |
|------|-------|---|
| Trend | 369 | 70.3% |
| Volatility | 67 | 12.8% |
| Liquidity | 89 | 17.0% |

Trend is by far the fastest axis at 4h resolution. Volatility and liquidity change on slower timescales relative to the bar size.

### Disruption Measure Confound — Identified

|return_next_bar| cannot be used as the "disruption" measure for the axis-type alignment test (Steps 1-3). A trend flip mechanically produces a large |return| — that's what trend reversal is by definition. Using |return_next_bar| would bias toward finding trend as the pure-克 axis regardless of the grammar, measuring axis identity rather than edge character.

Alternative disruption measures identified that avoid this confound:
- **Regime persistence** (bars until next state change): 克 = destabilizing (short dwell in destination), 生 = sustaining (long dwell). No directional bias.
- **Volatility ratio** (realized_vol of next bar / current bar): captures whether the transition amplifies or dampens volatility, regardless of direction.

### Test Design for Axis-Type Alignment — Designed (not yet run)

Two-level test:
- **Level 1:** Does a {4, 2+2, 2+2} partition exist across the three axes? For each axis, compute per-edge mean of the observable (4 edges per axis). One axis should have minimal within-axis variance (uniform), one maximal (bimodal), one intermediate. This tests the theorem's structural prediction without assuming which axis maps where.
- **Level 2:** Does the partition match the canonical assignment (vol = pure-克, liquidity = doublet, trend = mixed)?

Level 1 is the important structural test. Level 2 is specific to the Z₅ typing.

### What Remains Untested

- Whether order book liquidity proxies achieve axis independence (MI < 0.1 required)
- M1 as a function of bar size (timescale sweep at 1h, 2h, 4h, 8h, daily)
- Edge-level disruption test (regime persistence + vol ratio per edge, {4,2+2,2+2} partition)
- GMS bigram test (parked until axis independence and timescale are resolved)
- Valve test (parked)
- All axis permutation tests
- Out-of-sample validation (Feb-Mar 2026 data)
- Longer history (2023-2024 1m data)

**Scripts:** `market_regime_data.py` (data pipeline). **Output:** `market_4h_bars.csv` (1290 bars), `market_transitions.csv` (1289 transitions).

---

## Iteration 5: Axis Independence Fix, Timescale Sweep, Hamming-3 Characterization

**Question:** (a) Can order book fields replace volume-as-liquidity to achieve axis independence? (b) How does M1 vary with bar size? (c) What are the Hamming-3 transitions?

**Scripts:** `market_regime_diagnostics.py` (all three tasks), `market_regime_data.py` (updated pipeline)

### Task 1: Liquidity Axis Candidate Screening — Measured

Six fields screened as b₂ replacements, binarized by 7-day rolling median, compared on MI(b1_vol, b2) and vertex uniformity:

| Field | MI | φ | agree% | min vertex | entropy | M1 |
|-------|------|-------|--------|------------|---------|------|
| ob_imbalance_slope_5m | 0.0003 | +0.019 | 50.9% | 77 | 2.850 | 0.462 |
| liquidity_shift_15m | 0.0015 | +0.045 | 52.2% | 67 | 2.825 | 0.470 |
| **ob100_ratio_1m** | **0.0025** | **-0.059** | **47.1%** | **143** | **2.995** | **0.592** |
| ob_total_ratio_1m | 0.0061 | -0.092 | 45.4% | 110 | 2.956 | 0.660 |
| depth_asymmetry_10 | 0.1113 | -0.388 | 30.6% | 78 | 2.877 | 0.571 |
| volume_since_last | 0.3458 | +0.663 | 83.1% | 43 | 2.652 | 0.574 |

#### Independence–Stability Tradeoff — Discovered

The two most independent fields (ob_imbalance_slope_5m, liquidity_shift_15m — MI≈0) oscillate too fast, producing M1≈0.46 (barely above the 0.43 random baseline). High independence but no Q₃ edge structure — these axes flip on a faster timescale than trend and volatility, generating multi-axis noise.

`ob100_ratio_1m` is the sweet spot: MI=0.0025 (essentially zero), entropy=2.995 (max=3.0), minimum vertex count=143, M1=0.592. It changes on a timescale compatible with the other two axes.

#### What is `ob100_ratio_1m`?

Bid-to-ask depth ratio at top 100 price levels of the order book, averaged over 1-minute windows. This measures **order book directional bias** (buyer support vs seller pressure), not "liquidity" in the traditional sense (market depth or trading cost). The physical interpretation of b₂ has shifted from "scarce/abundant liquidity" to "sell-heavy/buy-heavy order book."

#### Selected: `ob100_ratio_1m` as new b₂

Pipeline updated. All subsequent CSVs use this axis.

### Updated Vertex Distribution — Measured

With `ob100_ratio_1m` as b₂:

| Vertex | Bits | Trigram | Regime | Count | % |
|--------|------|---------|--------|-------|---|
| 0 | 000 | 坤 | Quiet decline | 143 | 11.1% |
| 1 | 001 | 震 | Grinding rally | 151 | 11.7% |
| 2 | 010 | 坎 | Panic/capitulation | 190 | 14.7% |
| 3 | 011 | 兌 | Short squeeze | 156 | 12.1% |
| 4 | 100 | 艮 | Slow bleed | 176 | 13.6% |
| 5 | 101 | 離 | Healthy bull | 161 | 12.5% |
| 6 | 110 | 巽 | Correction | 158 | 12.2% |
| 7 | 111 | 乾 | Euphoria | 155 | 12.0% |

Near-uniform: all vertices between 11.1% and 14.7%. Entropy 2.995 of 3.0 max. The Q₂ collapse is fully resolved — all 8 regimes are well-populated.

Note: regime labels ("Quiet decline," "Panic," etc.) were defined when b₂ was "liquidity." With b₂ now measuring order book bias, the labels need reinterpretation (e.g., vertex 4 = "Slow bleed" is now "down, low vol, buy-heavy book" — more like "supported decline").

### Updated Edge-Type Distribution — Measured

Among 593 Q₃ edges (up from 525 with volume):

| Type | Count | % | Theoretical (6:4:2) |
|------|-------|---|---------------------|
| 比和 | 85 | 14.3% | 16.7% |
| 生 | 256 | 43.2% | 33.3% |
| 克 | 252 | 42.5% | 50.0% |

The 77.3% 克-dominance from Iteration 4 was entirely a traffic concentration artifact from correlated axes. With independent axes, 生 and 克 are nearly equal at ~43% each.

Per-edge traffic intensity: each 生 edge carries (256/4)/(252/6) = 64.0/42.0 = 1.52× more traffic than each 克 edge. The system preferentially uses 生-typed transitions. This excess is ~5σ above the uniform-traffic expectation. Whether this reflects a genuine type-level preference (生 = path of least resistance) or vertex-frequency effects requires per-edge analysis (not yet done).

### Updated Axis Flip Distribution — Measured

| Axis | Count | % |
|------|-------|---|
| Trend | 299 | 50.4% |
| Volatility | 118 | 19.9% |
| Liquidity (ob100) | 176 | 29.7% |

Much more balanced than Iteration 4 (was 70:13:17). Trend is still the fastest axis but no longer dominant.

### Updated M1 — Measured

M1 = 0.5918 (593 Q₃ edges out of 1002 non-self transitions). Slightly improved from 0.574 with volume. 408 multi-axis jumps remain (31.6% of all transitions).

### Task 2: Timescale Sweep — Measured

Using the old volume-based axes (to isolate timescale from axis choice):

| Period | Bars | Self% | M1 | H3% |
|--------|------|-------|------|-----|
| 1h | 5,160 | 54.3% | **0.791** | 0.9% |
| 2h | 2,580 | 39.7% | 0.686 | 3.2% |
| 4h | 1,290 | 29.0% | 0.574 | 9.1% |
| 8h | 645 | 21.9% | 0.445 | 15.4% |
| 12h | 430 | 19.3% | 0.457 | 13.5% |
| 24h | 215 | 20.1% | 0.544 | 6.5% |

M1 increases monotonically from 8h (0.445) to 1h (0.791), confirming that shorter bars resolve multi-axis jumps into sequential single-axis steps. H3 (all-axis flips) drops from 9.1% at 4h to 0.9% at 1h.

At 1h, nearly 80% of actual regime changes are single-axis (Q₃ edges). This suggests 1h is closer to the natural timescale for single-axis transitions, though this needs re-verification with `ob100_ratio_1m` since the tradeoff may differ (ob100 might oscillate faster at 1h).

### Task 3: Hamming-3 Characterization — Measured

(Using old volume-based 4h pipeline)

117 Hamming-3 transitions. These are exclusively complement pairs (all 3 bits flip):

| Pair | Count | % |
|------|-------|---|
| 001 (Grinding rally) ↔ 110 (Correction) | 67 | 57.3% |
| 000 (Quiet decline) ↔ 111 (Euphoria) | 50 | 42.7% |

Both pairs connect the dominant Q₂ face regimes (0,1,6,7). No significant difference in |return_next_bar| across transition types (mean ~0.56-0.64% for all). Mild temporal clustering (15 consecutive pairs, one run of 3), distributed across all months.

Hamming-3 transitions are not exotic events — they are the vol-liquidity co-movement artifact: vol and liquidity flip together (because they're correlated), plus trend flips, producing apparent all-axis jumps. With the new independent axis (ob100_ratio_1m), these should largely resolve into proper Q₃ edge sequences.

### What Remains Untested

- Timescale sweep with `ob100_ratio_1m` (does MI stay < 0.1 at 1h? does M1 improve?)
- Edge-level partition test: regime persistence + vol ratio per edge, {4,2+2,2+2} axis structure
- Per-edge traffic analysis (is the 生-excess uniform across all 4 生 edges or concentrated?)
- GMS bigram test (parked)
- Valve test (parked)
- Out-of-sample validation (Feb-Mar 2026 data)
- Longer history (2023-2024 1m data)

**Scripts:** `market_regime_diagnostics.py` (screening, sweep, H3 analysis), `market_regime_data.py` (pipeline, updated to use `ob100_ratio_1m`). **Output:** `market_4h_bars.csv` (1290 bars, updated), `market_transitions.csv` (1289 transitions, updated).

---

## Iteration 6: Edge-Level Partition Test — First Genuine Grammar Test

**Question:** Does the Z₅ axis-type partition ({4, 2+2, 2+2}) manifest as measurable differences in transition character across the three market axes?

**Script:** `market_partition_test.py`

### Task 1: Timescale Verification with `ob100_ratio_1m` — Measured

| Period | Bars | MI(b1,b2) | M1 | Q₃ edges |
|--------|------|-----------|------|----------|
| **1h** | 5,160 | 0.0025 | **0.7885** | **2,065** |
| 2h | 2,580 | 0.0021 | 0.6734 | 1,140 |
| 4h | 1,290 | 0.0025 | 0.5918 | 593 |

MI is stable at 0.0025 across all timescales — `ob100_ratio_1m` does NOT degrade at shorter bars. M1 = 0.79 at 1h (79% of non-self transitions are single-axis), with 2,065 Q₃ edges — 3.5× the sample size of 4h.

**Selected: 1h bars** for the partition test.

### Task 2: Edge-Level Partition Test — Measured

Two observables computed for each of the 12 Q₃ edges at 1h resolution (n=2,065 Q₃ edges total):

**Observable 1: Regime persistence** — bars at destination vertex before any axis changes. Grammar predicts: 克 = low (destabilizing), 生 = high (sustaining).

**Observable 2: Volatility ratio** — realized_vol at destination / origin. Grammar predicts: 克 = high (disruptive), 生 = low (settling).

#### Per-Edge Data

| Edge | Axis | Type | Traffic | Persistence±SE | Vol ratio±SE |
|------|------|------|---------|----------------|--------------|
| 000↔001 | trend | 克 | 169 | 2.21±0.12 | 0.999±0.010 |
| 010↔011 | trend | 生 | 197 | 2.00±0.10 | 1.005±0.017 |
| 100↔101 | trend | 生 | 205 | 2.42±0.12 | 1.003±0.009 |
| 110↔111 | trend | 克 | 171 | 1.95±0.09 | 0.977±0.012 |
| 000↔010 | vol | 克 | 46 | 2.59±0.36 | 1.145±0.062 |
| 001↔011 | vol | 克 | 58 | 1.88±0.16 | 0.984±0.036 |
| 100↔110 | vol | 克 | 66 | 2.24±0.27 | 1.134±0.038 |
| 101↔111 | vol | 克 | 58 | 1.91±0.21 | 1.122±0.051 |
| 000↔100 | liq | 比和 | 240 | 1.75±0.09 | 1.014±0.010 |
| 001↔101 | liq | 生 | 234 | 1.66±0.07 | 0.985±0.008 |
| 010↔110 | liq | 生 | 338 | 1.94±0.08 | 1.055±0.012 |
| 011↔111 | liq | 比和 | 283 | 1.86±0.07 | 1.003±0.009 |

#### Traffic Distribution by Type

| Type | Edges | Total traffic | Per-edge mean |
|------|-------|---------------|---------------|
| 比和 | 2 | 523 | 262 |
| 生 | 4 | 974 | 244 |
| 克 | 6 | 568 | 95 |

生 edges carry 47% of all Q₃ traffic despite being 33% of edges (4/12). 克 edges carry only 28% despite being 50% of edges (6/12). This reflects axis-level transition rates: liquidity axis flips most frequently (2生+2比和 edges, 274/edge), trend is intermediate (2克+2生, 186/edge), volatility is rarest (4克, 57/edge).

#### Level 1 Test: {4, 2+2, 2+2} Partition

**Persistence — within-axis range:**

| Axis | Types | Edge means | Range |
|------|-------|------------|-------|
| volatility | [克,克,克,克] | [2.59, 1.88, 2.24, 1.91] | **0.708** |
| trend | [克,生,生,克] | [2.21, 2.00, 2.42, 1.95] | 0.466 |
| liquidity | [比和,生,生,比和] | [1.75, 1.66, 1.94, 1.86] | 0.283 |

max/median = 0.708/0.466 = **1.52 → FAIL** (threshold 2.0)

**Volatility ratio — within-axis range:**

| Axis | Types | Edge means | Range |
|------|-------|------------|-------|
| volatility | [克,克,克,克] | [1.145, 0.984, 1.134, 1.122] | **0.161** |
| liquidity | [比和,生,生,比和] | [1.014, 0.985, 1.055, 1.003] | 0.070 |
| trend | [克,生,生,克] | [0.999, 1.005, 1.003, 0.977] | 0.028 |

max/median = 0.161/0.070 = **2.32 → PASS** (threshold 2.0)

**But the vol ratio pass is confounded:** volatility-axis edges mechanically produce extreme vol ratios because flipping the vol bit IS a volatility regime change. Directed analysis confirms: low→high vol transitions average vol_ratio ≈ 1.35, high→low ≈ 0.83. This is axis identity, not Z₅ type.

#### Level 2 Test: Canonical Assignment

Both observables show **volatility** as the axis with largest range. The canonical prediction was **trend** (mixed axis). **Level 2: MISMATCH** on both observables.

#### Within-Axis Type Comparisons — The Decisive Test

Controlling for axis identity by comparing edges of different Z₅ types within the same axis:

**Trend axis (2 克 edges vs 2 生 edges):**

| Type | n | Persistence | |log(vol_ratio)| |
|------|---|-------------|-----------------|
| 克 | 340 | 2.08±0.07 | 0.107±0.006 |
| 生 | 402 | 2.21±0.08 | 0.113±0.006 |
| t-test p | | **0.226** | **0.444** |

**Liquidity axis (2 比和 edges vs 2 生 edges):**

| Type | n | Persistence | |log(vol_ratio)| |
|------|---|-------------|-----------------|
| 比和 | 523 | 1.81±0.06 | 0.102±0.004 |
| 生 | 572 | 1.83±0.05 | 0.107±0.005 |
| t-test p | | **0.853** | **0.411** |

**All four within-axis comparisons are non-significant (all p > 0.2).** The Z₅ edge type has no detectable effect on either observable when axis identity is controlled.

#### Effect Size: Axis vs Type

| Observable | η²(type) | η²(axis) | Ratio |
|------------|----------|----------|-------|
| Persistence | 0.0055 | 0.0132 | **2.4×** |
| |log(vol_ratio)| | 0.0305 | 0.0924 | **3.0×** |

Which axis flips explains 2.4–3.0× more behavioral variance than the Z₅ edge type. Both η² values are small (<10%), but the relative comparison is consistent: axis identity dominates.

#### Pooled Type Means

| Type | Persistence | Vol ratio | n |
|------|------------|-----------|---|
| 比和 | 1.81±0.06 | 1.008±0.007 | 523 |
| 生 | 1.99±0.05 | 1.017±0.006 | 974 |
| 克 | 2.10±0.07 | 1.031±0.011 | 568 |

Persistence ordering is **reversed** from the grammar's prediction: 克 destinations are the MOST persistent (2.10), not least. This reversal is an axis confound — all vol-axis edges are 克-typed, and vol transitions are rare but stable once achieved.

### Structural Interpretation

The Z₅ axis-type partition does not manifest as measurable transition character differences in market regimes. The test was well-powered: n=340–572 per within-axis comparison, sufficient to detect 0.3σ effects at 80% power.

**Why:** The Z₅ typing assumes S₃ symmetry across the three Q₃ axes — it treats all axes as interchangeable, assigning type based on algebraic distance rather than physical identity. But the three market axes (trend, volatility, order book bias) have maximally asymmetric physical character: different dimensions, different timescales, different dynamics. The S₃ symmetry is maximally broken by the physics. Axis identity (which physical axis changed) dominates over algebraic type (what Z₅ distance the transition has).

**Domain criterion identified:** For the axis-type partition to be testable, a domain needs approximate S₃ symmetry — three axes of similar kind, timescale, and measurement character. Market axes fail this criterion.

### What Remains Untested

- GMS bigram test (克→克 suppression) — logically independent from the partition test, but the negative partition result lowers the prior substantially
- D1 (TCM 八纲辨证) — three clinical binary axes with potentially better S₃ symmetry
- All axis permutation tests (moot given the negative partition result)
- Out-of-sample and longer-history robustness (moot for same reason)

**Scripts:** `market_partition_test.py`. **Data used:** 1h bars from `btc_datalog_2025-07-21_2026-02-20.csv` with axes: trend (`trend_4h`), volatility (`realized_vol_4h`), order book bias (`ob100_ratio_1m`).

---

## Iteration 7: GMS Bigram Test — 克→克 Suppression

**Question:** Are consecutive 克-typed Q₃ transitions suppressed, as the GMS (generative-mutual-suppression) rule predicts?

**Script:** `market_gms_test.py`

### Method

Two framings tested on 2,065 Q₃ edges from 5,160 1h bars (axes: trend, volatility, ob100_ratio_1m):

- **Framing A (strict temporal adjacency):** Only count 克→克 when two consecutive bars both undergo Q₃-edge transitions. Self-loops and multi-axis jumps break the pair.
- **Framing B (Q₃ walk):** Extract the Q₃-edge-only sequence (skip self-loops and multi-axis jumps). Count consecutive 克→克 in this walk.

Three null models:
- **Null A (independence):** P(克)² × n_pairs
- **Null B (vertex-conditional):** Empirical P(next edge is 克 | at vertex v), summed over all observed 克 arrivals
- **Null C (permutation):** Shuffle edge-type labels among the 2,065 Q₃ edges, 10,000 iterations

### Results — Measured

**Framing A (temporal adjacency):**

| Metric | Value |
|--------|-------|
| Adjacent Q₃-edge pairs | 843 |
| 克→克 observed | 93 |
| Expected (independence) | 63.8 |
| Observed/expected ratio | **1.458** |
| Permutation p-value | **1.0000** (all 10k shuffles had fewer) |

**Framing B (Q₃ walk):**

| Metric | Value |
|--------|-------|
| Walk length | 2,065 steps |
| Consecutive pairs | 2,064 |
| 克→克 observed | 222 |
| Expected (independence) | 156.2 |
| Expected (vertex-conditional) | 219.0 |
| Observed/expected ratio (indep) | **1.422** |
| Observed/expected ratio (vertex) | **1.014** |
| Permutation p-value | **1.0000** (all 10k shuffles had fewer) |

**Full bigram tables (Framing B, Q₃ walk):**

|  | →比和 | →生 | →克 |
|--|-------|-----|-----|
| 比和→ | 238 | 140 | 145 |
| 生→ | 153 | 619 | 201 |
| 克→ | 132 | 214 | 222 |

**Result: 克→克 is ENHANCED, not suppressed.** The observed count is 42–46% above the independence baseline in both framings, and p=1.0000 in both permutation tests (observed is higher than all 10,000 shuffled counts). This is the opposite of the GMS prediction.

### Vertex-Conditional Explanation

P(next Q₃ edge is 克 | at vertex v):

| Vertex | P(克) | Position |
|--------|-------|----------|
| 000 Quiet decline | 0.485 | P₄ interior |
| 001 Grinding rally | 0.475 | P₄ interior |
| 110 Correction | 0.383 | P₄ interior |
| 111 Euphoria | 0.456 | P₄ interior |
| 010 Panic/capitulation | 0.062 | P₄ endpoint |
| 011 Short squeeze | 0.148 | P₄ endpoint |
| 100 Slow bleed | 0.152 | P₄ endpoint |
| 101 Healthy bull | 0.105 | P₄ endpoint |

The four P₄-interior vertices (000, 001, 110, 111) have P(克) ≈ 0.38–0.49 — close to half. The four P₄-endpoint vertices have P(克) ≈ 0.06–0.15 — very low. Since 克 edges connect P₄-interior vertices to each other, landing at one after a 克 step puts you where the next step is also likely 克. The enhancement is fully explained by graph topology (Null B ratio = 1.014).

### P₄ Path Analysis

| Category | Count | % of 克→克 |
|----------|-------|-----------|
| On P₄ (GMS-forbidden) | 75 | 33.8% |
| Off P₄ | 147 | 66.2% |

75 specifically forbidden 3-step sequences were observed. These include all 8 forbidden directed triples. The P₄ paths are heavily trafficked, not avoided.

Off-P₄ 克→克 consists primarily of backtracking (e.g., 000→001→000 = trend flip, trend flip-back) — the same 克-typed trend edge traversed twice in a row.

### Structural Interpretation

The GMS prediction is decisively falsified. 克→克 is positively correlated in market regime transitions, and the correlation is entirely explained by graph topology: 克 edges cluster on one face of Q₃ (connecting the 4 high-traffic vertices), so the random walk naturally produces 克→克 runs through traffic concentration.

This completes the D4 investigation. The Z₅ grammar fails all empirical tests:
- D4.1 (M1 prerequisite): **PASS** — Q₃ adjacency is real
- D4.2 (axis-type partition): **FAIL** — Z₅ type has no behavioral effect
- D4.3 (GMS 克→克 suppression): **FAIL** — 克→克 is enhanced, not suppressed
- D4.4 (valve): **FAIL** (by implication from D4.3)
- D4.5 (axis assignment): **MOOT** (no signal to assign)

The positive finding: Q₃ as a graph framework for market regime transitions has empirical validity (M1=0.79). But the Z₅ typing layered on top adds nothing. Axis identity dominates algebraic type.

**Scripts:** `market_gms_test.py`. **Data used:** 1h bars from same datalog, same axes as Iteration 6.

### Memoryless Q₃ Walk — Positive Finding

The vertex-conditional null ratio of 1.014 means: a first-order Markov chain on the 8 Q₃ vertices, with empirical per-vertex transition rates, fully accounts for the observed sequential statistics of edge types. Knowing the type of the last transition (克/生/比和) adds zero predictive power beyond knowing the current vertex.

This is the simplest possible model for regime transitions on Q₃: current state → vertex-dependent transition probabilities → next state. No hidden states, no higher-order dependencies, no edge-type memory.

The GMS constraint requires second-order edge-type memory — the system must "remember" that the last transition was 克 and avoid making the next one also 克. A memoryless walk has no such memory. The memorylessness is not just consistent with the GMS failure — it IS the mechanism.

### Connection to Mod-8

The mod-8 investigation concluded: the grammar is typological, not dynamical. It classifies static relational configurations, not temporal sequences. The D4 investigation confirms this from a new angle: temporal sequences of market regime transitions are memoryless with respect to Z₅ type, exactly as predicted by a non-dynamical grammar. The negative GMS result is consistent with the investigation's prior understanding — a positive result would have been the surprise.

### D4 Summary — Three-Level Finding Hierarchy

**Level 1 (positive, general):** Q₃ adjacency is empirically real for market regimes. Three genuinely independent binary axes (trend, volatility, order book bias) produce 8 well-populated regimes with near-uniform vertex coverage (entropy 2.995/3.0). M1 = 0.79 at 1h — market regime changes proceed primarily one axis at a time.

**Level 2 (positive, specific):** Market regime transitions are well-modeled as a memoryless walk on Q₃ with vertex-dependent transition rates. The vertex-conditional null explains 克→克 clustering to within 1.4%. No structure beyond the graph and the per-vertex rates.

**Level 3 (negative):** Z₅ typing adds nothing to the Q₃ framework. No behavioral differentiation by edge type (all within-axis p > 0.2, η² ≈ 0). No sequential constraint (克→克 enhanced 1.42×, not suppressed). No valve. Axis identity (which physical axis changed) explains 2.4–3.0× more behavioral variance than Z₅ type.

**Root cause:** The Z₅ typing assumes S₃ symmetry across Q₃ axes — it treats all axes as interchangeable. The three market axes (trend, volatility, order book bias) have maximally asymmetric physical character: different dimensions, different timescales, different dynamics. The S₃ symmetry is maximally broken by the physics.

### Implications for Other Domains

**D1 (TCM 八纲辨证):** The memoryless Markov null is now the baseline. A positive GMS result in TCM would need to show 克→克 suppression below what vertex-conditional rates predict — genuine second-order structure. TCM's three diagnostic axes (cold/hot, deficiency/excess, exterior/interior) may have better S₃ symmetry (all are clinical binary assessments of the same system, measured by similar methods, operating on similar timescales).

**Domain criterion sharpened:** For the Z₅ grammar to be testable in any domain, two conditions must hold: (a) three genuinely independent binary axes with approximate S₃ symmetry, and (b) transition dynamics that exhibit second-order edge-type structure beyond what a memoryless walk produces.

---

## D4 Final Synthesis (Iterations 1–7)

**Starting question:** Does the Z₅ grammar make testable, falsifiable predictions for Q₃ domains outside the I Ching's native algebraic space?

**What was established algebraically (Iterations 1–3):**
- The edge-type distribution {比和=2, 生=4, 克=6} is invariant under all 48 Q₃ automorphisms (D3-R1)
- 102 distinct colorings exist; 24 in the Aut(Q₃) orbit; the (0,\*,\*) patterns diagnose axis non-independence (D3-R2)
- The axis-type partition {pure-克, mixed, doublet} = {4, 2+2, 2+2} is forced by (3/5)=-1 (D3-R4)
- A concrete 5-step testing protocol was derived (D3-R5)

**What was established empirically (Iterations 4–7):**
- Q₃ adjacency is empirically real for BTC market regimes: M1=0.79 at 1h (D4-R2)
- Three genuinely independent binary axes can be constructed using order book data: MI=0.0025, vertex entropy 2.995/3.0 (D4-R1)
- The Z₅ axis-type partition does not manifest: η²(type)≈0, all within-axis p>0.2 (D4-R3)
- GMS is falsified: 克→克 enhanced 1.42×, not suppressed; vertex-conditional null explains to within 1.4% (D4-R4)
- Market regime walk is memoryless with respect to edge type (D4-R5)
- Root cause: S₃ symmetry breaking by maximally asymmetric physical axes (D4-R6)

**What was NOT established:**
- Whether the grammar works in any domain with better S₃ symmetry (D1/TCM is untested)
- Whether the grammar's typological nature precludes all temporal/dynamical tests, or only those on axes with broken S₃ symmetry
- Whether there exist domains where second-order edge-type structure (beyond memoryless walk) is present

**Connection to broader investigation:**
The D4 negative confirms the mod-8 conclusion (grammar is typological, not dynamical) from an independent empirical angle. The "typological not dynamical" finding now has convergent support from: (a) the mod-8 structural analysis showing 先天 divination operates on Z₈ not Q₃, (b) the D4 empirical test showing temporal sequences are memoryless with respect to Z₅ type.

**Scripts:** `q3_edge_orbits.py`, `market_regime_predictions.py`, `market_regime_data.py`, `market_regime_diagnostics.py`, `market_partition_test.py`, `market_gms_test.py`

**Findings document:** `findings.md`
