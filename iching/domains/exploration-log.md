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
