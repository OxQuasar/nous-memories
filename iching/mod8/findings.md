# Mod-8 Investigation — Findings

> The 先天 mod-8 divination arithmetic projected onto the F₂³ algebraic structure.
> Questions M1–M5 in `questions.md`. All statistics are exhaustive enumerations.
> **Bit convention A:** b₀ = bottom line, b₂ = top line. The 先天 binary counter uses Convention B (top=MSB); the bit-reversal bridge is documented in §II.

**Epistemological key:**
- **[proven]** — algebraically necessary, follows from definitions
- **[measured]** — exhaustive enumeration

---

## §I. Bit-Layer Decomposition

### Data
- Scripts: `m1_mod8_structure.py`, `m2a_cycle_landscape.py`

### Finding I.1: Maximally differentiated 五行 content across bit-layers

**[measured]** Q₃ has 12 edges, 4 per bit-layer. The canonical 五行 assignment produces maximal type differentiation:

| Layer | Edges | 比和 | 生 | 克 |
|-------|-------|------|-----|-----|
| bit₂ (top) | 4 | 2 | 2 | **0** |
| bit₁ (mid) | 4 | 0 | 0 | **4** |
| bit₀ (bot) | 4 | 0 | 2 | 2 |
| **Total** | **12** | **2** | **4** | **6** |

bit₂ is the unique 克-free layer. bit₁ is pure 克. This is the Chebyshev sequence {P₂, P₃, P₄} from R258, reframed as 五行 content: each bit-layer carries a single path subgraph of the trigram cube, and these paths have lengths 2 (比和), 3 (生), 4 (克).

**[proven] Mechanism for bit₁ = pure 克:** Within each b₀-half, the mid-bit separates elements at Z₅ distance ±2. In b₀=1: b₁ splits Metal{111,011} from {Fire(101), Wood(001)}, both at 克 distance. In b₀=0: b₁ splits {Water(010), Wood(110)} from Earth{000,100}, both at 克 distance.

**[proven] Mechanism for bit₂ = 克-free:** Top-bit flips preserve (b₁,b₀). The paired elements Metal=(1,1) and Earth=(0,0) map to themselves (比和). The singletons Fire=(0,1) and Water=(1,0) share their (b₁,b₀) with Wood, at Z₅ distance 1 = 生.

---

## §II. The Mod-8 Cycle

### Finding II.1: Mod-8 cycle type sequence

**[measured]** The 先天 cycle 1→2→3→4→5→6→7→8→1 produces the 五行 type sequence:

{比和, 克, 生, 比和, 生, 克, 比和, 生}

Counts: 比和=3, 生=3, 克=2. Three 比和 steps at within-element pairs (Metal 1→2, Wood 4→5, Earth 7→8), spacing 3.

### Finding II.2: Q₃ edge selection is entirely 克-free

**[measured]** The mod-8 cycle has 4 Hamming-1 steps (at positions 1→2, 3→4, 5→6, 7→8). All 4 have XOR mask = (1,0,0) — they flip bit₂ exclusively. Their 五行 types: 2 比和, 2 生, **zero 克**.

**[measured]** The 2 克 transitions (steps 2→3 and 6→7) both occur at Hamming distance 2, with XOR = (1,1,0) = bit₂+bit₁. They are NOT Q₃ edges. The 克 enters the cycle exclusively through multi-bit jumps that include the 克-saturated bit₁.

**[proven] Mechanism:** The 先天 ordering sorts b₀ first (positions 1–4 have b₀=1, 5–8 have b₀=0), then b₁ (reversed), then b₂. Single-step increments toggle bit₂ — the fastest-changing bit in this descending binary counter. Since bit₂ is the unique 克-free layer, all single-step Q₃ edges on the mod-8 cycle are 克-free.

### Finding II.3: Complement partial palindrome

**[measured]** T(k) = T(8−k) for k=1,2,3. The first 7 steps form a palindrome {比和, 克, 生, 比和, 生, 克, 比和}. The 8th step (坤→乾 = Earth→Metal = 生) is the wraparound seam — self-paired under complement, unconstrained by any other step.

---

## §III. Q₃ Floor Theorem

### Finding III.1: Every Q₃ Hamiltonian cycle has 克 ≥ 3

**[measured]** All 6 distinct Q₃ Hamiltonian cycles (up to start vertex and direction). 克 distribution: {3, 3, 4, 4, 5, 5}. Minimum = 3. The mod-8 cycle's 克=2 is unreachable by any Q₃ edge-path.

**[proven] Complete forcing chain:**

1. **Topological partition:** The union of bit₀ and bit₂ edges forms exactly two disjoint 4-cycles: {坤,艮,離,震} (b₁=0 half) and {坎,巽,乾,兌} (b₁=1 half). The b₁ bit is frozen within each component.

2. **Bridge requirement:** Any Q₃ Hamiltonian cycle must include ≥2 bit₁ edges (enter + exit each half). Since bit₁ = pure 克, this gives 克 ≥ 2 from bit₁ alone.

3. **Asymmetric 克 in b₁=1 half:** In the b₁=1 component {坎=Water, 兌=Metal, 乾=Metal, 巽=Wood}, both bit₀ edges are 克 (Water↔Metal and Wood↔Metal). Any Hamiltonian path through this 4-vertex component uses 3 of 4 edges, so at least one bit₀ 克 edge is unavoidable.

4. **Floor = 2 + 1 = 3:** 2 克 from bit₁ bridges + ≥1 克 from b₁=1 component's bit₀ edges.

The b₁=0 half has one avoidable 克 edge (Earth↔Wood) and one 生 edge (Earth↔Fire), so the asymmetry is specific to b₁=1, where the singleton Water forces both bit₀ edges to 克 distance.

---

## §IV. Landscape Context

### Finding IV.1: 克-free bit-layers are generic

**[measured]** Across all 240 complement-respecting surjections F₂³ → Z₅ (involution x ↦ (4−x) mod 5):
- 192/240 (80%) have at least one 克-free bit-layer
- By partition: {2,2,2,1,1} = 168/192 (87.5%), {4,1,1,1,1} = 24/48 (50%)
- Per specific bit-layer: ~30% (by S₃ symmetry of bit positions, each layer equally likely)

The canonical assignment's bit₂ being 克-free, aligned with the 先天 ordering's bit₂ selection, is a **1-in-3 coincidence**.

### Finding IV.2: Pure-克 layers partition-dependent

**[measured]** 120/240 (50%) of surjections have at least one pure-克 layer (all 4 edges in that layer are 克). Per layer: exactly 48 each (perfect S₃ symmetry). By partition: {2,2,2,1,1} = 120/192 (62.5%), **{4,1,1,1,1} = 0/48 (0%)**. The {4,1,1,1,1} partition never produces a pure-克 layer.

### Finding IV.3: Mod-8 cycle's 克=2 is low but not extreme

**[measured]** Among all 2520 distinct 8-cycles on 8 labeled vertices:

| 克 count | Cycles | % | 
|----------|--------|---|
| 0 | 16 | 0.6% |
| 1 | 96 | 3.8% |
| **2** | **384** | **15.2%** |
| 3 | 624 | 24.8% |
| 4 | 668 | 26.5% |
| 5 | 512 | 20.3% |
| 6 | 152 | 6.0% |
| 7 | 64 | 2.5% |
| 8 | 4 | 0.2% |

Mean = 3.714. Mod-8 cycle at **19.7th percentile**. 克=0 is achievable (16 cycles exist).

**[measured]** Among the 48 complement-palindrome cycles (T(k)=T(8−k)): 克 distribution {0:4, 2:14, 3:8, 4:12, 5:4, 6:2, 7:4}. 克=1 never appears (odd parity excluded by palindrome structure). The mod-8 cycle is one of 14 complement-palindrome cycles with 克=2.

### Finding IV.4: Z₈ and Z₅ are fundamentally incompatible

**[measured]** No non-trivial cyclic shift S_k (k≠0) preserves the 五行 type of all 28 trigram pairs. S₄ (complement) is minimally destructive: 12/28 pairs change. The element map is never well-defined for k≠0 — paired elements split under shifting.

---

## §V. 體用 Distribution Under the Date Formula (M3)

### Data
- Script: `m3_tiyong_distribution.py`

### Finding V.1: Per-shift undirected type distribution

**[measured]** For each cyclic shift S_h (h = 0..7), the 8 (upper, lower) pairs where lower = S_h(upper):

| Shift | 比和 | 生 | 克 | 克% |
|-------|------|----|----|-----|
| 0 | 8 | 0 | 0 | 0% |
| 1 | 3 | 3 | 2 | 25% |
| 2 | 0 | 4 | 4 | 50% |
| 3 | 0 | 3 | 5 | 62.5% |
| 4 | 0 | 4 | 4 | 50% |
| 5 | 0 | 3 | 5 | 62.5% |
| 6 | 0 | 4 | 4 | 50% |
| 7 | 3 | 3 | 2 | 25% |

**[proven] Mirror symmetry:** S_h and S_{8-h} produce identical undirected type distributions (pair reversal: undirected type is symmetric). For directed relations, S_h and S_{8-h} have transposed distributions (克体 ↔ 体克用, 生体 ↔ 体生用).

### Finding V.2: Unweighted shift average = null (algebraically necessary)

**[proven]** Cycling through all 8 shifts generates every ordered pair (upper, lower) exactly once across 64 total pairs (8 shifts × 8 uppers). The unweighted type distribution therefore equals the null: 比和 = 14/64 = 21.88%, 生 = 24/64 = 37.50%, 克 = 26/64 = 40.62%.

### Finding V.3: 比和 concentration at shifts {0, 1, 7}

**[proven]** 比和 requires same-element trigrams. Paired elements occupy adjacent 先天 positions: {乾,兌}=Metal at (1,2), {震,巽}=Wood at (4,5), {艮,坤}=Earth at (7,8). Non-identity 比和 requires shift ±1, reaching the same-element neighbor. Singletons Fire(3) and Water(6) produce 比和 only with themselves (shift 0).

### Finding V.4: Hour-weighted ergodic deviation

**[measured]** The 12 地支 hours map non-uniformly to shifts: shifts 1–4 get weight 2 (hours H and H+8 collapse), shifts 0,5,6,7 get weight 1. The 克-enriched shifts 2,3,4 are doubly weighted:

| Type | Actual (hour-weighted) | Null | Δ |
|------|------------------------|------|---|
| 比和 | 17.71% | 21.88% | −4.17% |
| 生 | 39.58% | 37.50% | +2.08% |
| 克 | 42.71% | 40.62% | +2.08% |

### Finding V.5: Shift 2 bit-layer partition

**[proven]** The 8 pairs under shift 2 split into two maximally differentiated populations:
- 4 pairs with XOR = 010 (pure bit₁): all 克
- 4 pairs with XOR = 011 (bit₁⊕bit₀): all 生

The 50% 克 at shift 2 is two perfectly typed populations from distinct bit-layer compositions.

### Finding V.6: Mod-8/mod-6 gcd=2 coupling

**[proven]** Moving line m = S mod 6, where S = Y+M+D+H and lower_raw = S mod 8. Since gcd(8,6) = 2:
- Even lower_raw → m ∈ {2, 4, 6} → P(upper = 体) = 1/3
- Odd lower_raw → m ∈ {1, 3, 5} → P(upper = 体) = 2/3

For any shift, 4 of 8 uppers give each parity, so average P(upper = 体) = 1/2. But each specific (upper, shift) pair has a deterministic 2:1 bias.

### Finding V.7: Directed ergodic favorability

**[measured]** Directed ergodic average (hour-weighted, with moving-line 体 probability):

| Relation | Actual | Null | Δ |
|----------|--------|------|---|
| 比和 | 17.71% | 21.88% | −4.17% |
| 生体 | 19.79% | 18.75% | +1.04% |
| 体生用 | 19.79% | 18.75% | +1.04% |
| 体克用 | 20.83% | 20.31% | +0.52% |
| 克体 | 21.88% | 20.31% | +1.56% |

Favorable (比和 + 生体 + 体克用) = 58.33% vs null 60.94% (Δ = −2.60%). The date formula is slightly more adversarial than random chance.

---

## §VI. Grammar Survival at Hexagram Level (M4)

### Data
- Script: `m4_grammar_survival.py`

### Finding VI.1: GMS fails at undirected level

**[measured]** 24/88 consecutive-hour pairs (27.3%) have consecutive 克 — a decisive GMS violation. Every upper trigram has at least 1 violation:

| Upper | Element | Consecutive 克 | / 11 |
|-------|---------|----------------|------|
| 坤(0) | Earth | 2 | 11 |
| 乾(1) | Metal | 4 | 11 |
| 兌(2) | Metal | 4 | 11 |
| 離(3) | Fire | 1 | 11 |
| 震(4) | Wood | 4 | 11 |
| 巽(5) | Wood | 5 | 11 |
| 坎(6) | Water | 2 | 11 |
| 艮(7) | Earth | 2 | 11 |

### Finding VI.2: Mod-6 coupling provides zero directed protection

**[measured]** All 24 undirected 克-克 pairs admit consecutive 克体-克体 under at least one moving-line assignment. The mod-6 coupling is not a grammatical filter. P(克体-克体) per 克-克 pair ranges from 0.2222 to 0.4444.

### Finding VI.3: Valve fails

**[measured]** 克→生 = 10/37 克-outgoing transitions (27.0%). The valve is thoroughly violated.

### Finding VI.4: 克-clustering from sequential sampling

**[measured]** 克→克 = 24 vs null expectation 16.1 — 49% enrichment. 克→生 = 10 vs null 14.9 — suppressed ~33%.

**[proven] Mechanism:** The 12-hour sequence visits shifts 1→2→3→4→5→6→7→0→1→2→3→4. Shifts 2–6 form a contiguous 克-heavy block (50–62.5% 克, 0% 比和). The grammar requires Q₃-edge locality (single bit-flips); the calendar navigates via Z₈ cyclic shifts (multi-bit jumps). The 克-clustering is autocorrelation from sequential sampling of a spatially structured distribution — a Z₈ property, not a shadow of Q₃ grammar.

---

## §VII. Topology in Empirical Data (M5)

### Data
- Script: `m5_topology_in_data.py`
- Sources: BTC-USD daily returns 2015–2025 (N=4016), Gaussian i.i.d., AR(1) ρ=0.3, GARCH(1,1) (each N=4000)
- Discretization: 8 quantile bins → 先天 position → F₂³ vector

### Finding VII.1: Bit-layer grammar is tautological

**[proven]** The bit-layer 克 percentages for Hamming-1 transitions hold identically across all data sources:

| Source | bit₀ 克% | bit₁ 克% | bit₂ 克% |
|--------|---------|---------|---------|
| Grammar prediction | 50% | 100% | 0% |
| BTC | 39.3% | 100.0% | 0.0% |
| Gaussian | 50.3% | 100.0% | 0.0% |
| AR(1) | 50.1% | 100.0% | 0.0% |
| GARCH | 44.8% | 100.0% | 0.0% |

bit₁=100% and bit₂=0% are exact for all sources. This is a property of the WUXING_MAP (every bit₁ edge connects elements at Z₅ distance 2; every bit₂ edge at distance 0 or 1), not of any data being mapped. Observing bit-layer structure in data mapped through this functor cannot count as evidence about the data itself.

### Finding VII.2: GMS and valve fail empirically

**[measured]** No data source shows GMS suppression or valve suppression:

| Source | GMS ratio | Valve (克→生%) |
|--------|-----------|----------------|
| BTC | 1.12x | 36.2% |
| Gaussian | 1.06x | 34.2% |
| AR(1) | 1.00x | 29.6% |
| GARCH | 1.05x | 36.9% |

### Finding VII.3: No Q₃-edge preference in any data source

**[measured]** Hamming-1 transition fractions:

| Source | H=1 actual | H=1 shuffled | H=1 null (37.5%) | Δ from null |
|--------|-----------|-------------|------------------|-------------|
| BTC | 34.8% | 38.5% | 37.5% | −2.7% |
| Gaussian | 37.0% | 37.2% | 37.5% | −0.5% |
| AR(1) | 40.3% | 38.1% | 37.5% | +2.8% |
| GARCH | 36.3% | 36.6% | 37.5% | −1.2% |

BTC shows Hamming-1 *depletion*, the opposite of Q₃-edge preference. AR(1) shows slight enrichment from generic autocorrelation, not Q₃-specific structure.

### Finding VII.4: BTC excess complement transitions

**[measured]** BTC: 16.4% Hamming-3 (complement) transitions vs 12.5% null (+3.9%). This reflects known financial tail reversion (extreme returns followed by opposite-extreme returns), not Q₃ structure. The complement pairs in 先天 ordering are biased toward 生 (Metal↔Earth), producing BTC's 克-depletion (34.5% vs 40.6% null).

### Finding VII.5: R286-R287 obstruction

**[proven]** Q₃ is not an interval graph. Scalar time series are 1-dimensional. No 1-dimensional ordering of 8 states can reproduce Q₃ adjacency. The dimensional mismatch is topological — Q₃ has 3 independent binary dimensions. Q₃-edge preference would require the discretization to be a Gray code, which encodes adjacency by construction rather than discovering it.

---

## Summary

### The structural theorem

**Q₃ and Z₈ share vertices but are topologically incommensurable for grammar transport.**

The grammar (GMS, valve, forcing chain) is an intrinsic property of the Q₃ edge-coloring under the complement-Z₅ surjection. The divination (mod-8 calendar, quantile discretization) operates on Z₈ cyclic structure. The 先天 permutation bijects vertices but cannot transport edge constraints — it is a bijection, not a homomorphism.

| | Q₃ (algebraic) | Z₈ (calendrical) |
|---|---|---|
| Topology | Hypercube edges | Cyclic adjacency |
| 克 at edges | 50% (dominant) | 0% at Q₃ edges, 25% overall |
| Grammar | GMS, valve, forcing chain | None (free) |
| 克 at hexagram level | N/A | 42.71% |
| Temporal constraints | Forbidden patterns (GMS) | Autocorrelation only |
| Favorability structure | N/A | Parity wall (OR=5.23) |
| Empirical footprint | Tautological (functor property) | Data-dependent |

### Three categories of finding

**Mechanism (proven):**
- Bit-layer decomposition: bit₂=克-free, bit₁=pure 克. Traced to Z₅ distance structure. (§I)
- Q₃ floor forcing chain: 克 ≥ 3 for any Q₃ Hamiltonian cycle. (§III)
- Ergodic null: unweighted shift average = null distribution exactly. (§V.2)
- Mod-8/mod-6 gcd=2 coupling: even/odd lower_raw determines 体 assignment bias. (§V.6)
- Grammar failure mechanism: Z₈ cyclic shifts ≠ Q₃ single-bit transitions. (§VI.4)
- R286-R287 obstruction: Q₃ is not an interval graph → scalar discretization cannot access Q₃ adjacency. (§VII.5)
- Bit-layer tautology: 五行 typing of Q₃ edges is a functor property, not a data property. (§VII.1)

**Measured (exhaustive or empirical):**
- Hour-weighting produces +2.08% 克-enrichment, −2.6% favorability vs null. (§V.4, §V.7)
- GMS violation rate 27.3%, valve non-zero (10/37), at hexagram level under calendar formula. (§VI.1–3)
- 克-clustering 49% enriched over i.i.d. from sequential shift sampling. (§VI.4)
- No Q₃-edge preference in BTC, Gaussian, AR(1), or GARCH data. (§VII.3)
- BTC excess complement transitions (16.4% vs 12.5% null) = known financial tail reversion. (§VII.4)

**Structural constraint (proven):**
- Q₃ floor: 克 ≥ 3 topologically forced for any Q₃ edge-path. (§III)
- Z₈/Z₅ incompatibility: no cyclic shift preserves 五行 pair types. (§IV.4)
- Topological separation is total: vertex bijection ≠ edge homomorphism. (§I–§VII)

### Connection to broader investigation

The mod-8 investigation confirms the I Ching's algebraic structure (Q₃ grammar, complement-Z₅ forcing, φ-orbit) as a purely mathematical object — a property of the unique canonical edge-typing of Q₃ under complement-Z₅ axioms. The divination's operational structure (体用, parity wall, arc types) is an independent Z₈ arithmetic system that shares the same vertex set but has no access to the edge grammar.

The 梅花 divination system's practical structure — the parity wall favorability (OR=5.23), the ti_hu adversarial bias (63%), the layered inversion pattern — operates entirely within Z₈ arithmetic. These are real structural properties of the divination algorithm, but they derive from mod-8 parity constraints, not from Q₃ grammar.

---

## §VIII. Z₅ Geometry of the 先天 Cycle

### Finding VIII.1: The 先天 cycle is a retrograde palindrome on Z₅

**[measured]** The 先天 positions 1–8 project to Z₅ as:

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|----------|---|---|---|---|---|---|---|---|
| Trigram | 乾 | 兌 | 離 | 震 | 巽 | 坎 | 艮 | 坤 |
| Element | 金 | 金 | 火 | 木 | 木 | 水 | 土 | 土 |
| Z₅ | 3 | 3 | 1 | 0 | 0 | 4 | 2 | 2 |

The undirected Z₅ distance sequence from any center element is palindromic. Centered on 木(0):

```
克  克  生  [比和 比和]  生  克  克
金  金  火    木    木    水  土  土
 3   3   1    0    0     4   2   2
```

### Finding VIII.2: All non-trivial steps are retrograde on the 生 cycle

**[measured]** The consecutive-step Z₅ relationships:

| Step | From → To | Z₅ relation | Direction on 生 cycle |
|------|-----------|-------------|----------------------|
| 1→2 | 金→金 | 比和 | — |
| 2→3 | 金→火 | 火克金 | **retrograde** (next overcomes previous) |
| 3→4 | 火→木 | 木生火 | **retrograde** (next is parent of previous) |
| 4→5 | 木→木 | 比和 | — |
| 5→6 | 木→水 | 水生木 | **retrograde** (next is parent of previous) |
| 6→7 | 水→土 | 土克水 | **retrograde** (next overcomes previous) |
| 7→8 | 土→土 | 比和 | — |
| 8→1 | 土→金 | 土生金 | **forward** (previous generates next) |

Seven steps retrograde. One step forward (the seam, 土→金 = 坤→乾 = Earth→Heaven). The cycle unwinds against the 生 direction, then one generative step resets it.

The relationship-type palindrome:
```
比和, 克↓, 生↓, 比和, 生↓, 克↓, 比和, 生↑
                                       ^^^^ seam
```

### Finding VIII.3: 木 is the palindrome center AND the 互 kernel element

**[proven]** 木 is special in six independent structural ways:

1. **先天 cycle:** Palindrome center. Flanked symmetrically by 生 (火↔水) and 克 (金↔土). Equal relational pressure from both temporal directions. No other element has this property on the 先天 cycle.

2. **先天 ordering:** Straddles the b₀ boundary. 震(001) is position 4 (last b₀=1), 巽(110) is position 5 (first b₀=0). 木 is the yin/yang hinge of the primary sort.

3. **互 algebra (synthesis-1, Part IV):** The 木 pair {震,巽} lies on the Fano line H — the 互 kernel. 互 projection preserves 木. The 互 attractors carry 木. This is the 0.5-bit freedom: the tradition chose H=Wood (互 kernel = element-preserving direction) over the alternative H=Water/Fire.

4. **Complement closure (probe5):** 木 is the unique element closed under complement. 震↔巽 are complements (XOR=111, Hamming distance 3), and both are 木. Every other element maps to a different element under complement (金↔土, 火↔水). 木 is the fixed point of the complement permutation on Z₅.

5. **Cycle conjugation (wuxing/summary_findings):** The complement permutation maps the 生 cycle to its inverse (the 克 cycle), with 木 as the fixed point. 木 is the hinge where the direction of causation reverses. It bridges 生 and 克 because it sits at the pivot of the anti-automorphism. Without 木 as a single element, convergence under 互 would be frictionless — 木 creates the necessary 克 friction at every convergence step.

6. **He Tu compass (opposition-theory/loshu.md):** 木 = East, occupying Lo Shu positions 3 and 4 (震 and 巽). On the He Tu, 木 participates in two cross-element pairs: (3,8) = 震↔艮 = Wood克Earth, and (4,9) = 巽↔離 = Wood生Fire. 木 is the only element whose He Tu pairs include the sole 克 relationship among the four pairs (the other three are all 生). 木 is also the starting point of both the 生 cycle (木→火→土→金→水) and the 克 cycle (木→土→水→火→金) in their traditional enumeration — the generative origin in the spatial/compass representation, paralleling its role as palindrome center in the temporal/先天 representation.

**[measured]** The palindrome's mirror structure maps exactly onto the {2,2,2,1,1} partition:

| Position on palindrome | Element | Multiplicity | Z₅ distance from 木 | Type |
|----------------------|---------|-------------|---------------------|------|
| Outer edges (1,2) | 金 | 2 (paired) | 2 (克) | b₀=1 side |
| Inner (3) | 火 | 1 (singleton) | 1 (生) | b₀=1 side |
| **Center (4,5)** | **木** | **2 (paired)** | **0 (比和)** | **hinge** |
| Inner (6) | 水 | 1 (singleton) | 1 (生) | b₀=0 side |
| Outer edges (7,8) | 土 | 2 (paired) | 2 (克) | b₀=0 side |

金↔土: both paired, both at 克 distance. 火↔水: both singleton, both at 生 distance. The {2,2,2,1,1} partition is laid out as a symmetric (paired-克, singleton-生, [center], singleton-生, paired-克) pattern.

### Finding VIII.4: The generative seam is at the calendar wrap-around

**[measured]** The single forward 生 step (土→金, position 8→1, 坤→乾) is the cycle's wrap-around — the transition from last to first. In the calendar:
- **Hourly cycle:** 未時→申時 (hour 8→9, ~1–3 PM → 3–5 PM)
- **地支 yearly cycle:** 未年→申年 (Goat→Monkey)

The most symbolically loaded transition in the system (坤→乾, Earth→Heaven) is the only one flowing in the natural generative direction.

### Finding VIII.5: Z₅ operates in period-8 cycles incommensurate with the calendar

**[measured]** The Z₅ relational structure has period 8 (from mod-8 arithmetic). The calendar periods are 10 (天干), 12 (地支), 60 (甲子). Since gcd(8,60)=4 and lcm(8,60)=120, the Z₅ pattern and the calendar never fully synchronize. The system operates on three independent clocks:
- Z₈ — mod-8 arithmetic (period 8)
- Z₅ — relational quality (period 8, via 先天 projection)
- Z₁₂ × Z₁₀ — the calendar (period 60)

Each projection loses information. The 60-year cycle has structure the Z₅ reading cannot see.

### Finding VIII.6: 木 as multi-layer convergence point

**[measured]** Six structural properties converge on 木 across independent layers:

| # | Property | Layer | Why 木 is unique |
|---|----------|-------|-----------------|
| 1 | Palindrome center | 先天→Z₅ projection | Equal 生 and 克 pressure from both temporal directions |
| 2 | b₀ yin/yang hinge | 先天 binary counter | Straddles positions 4–5, the primary sort boundary |
| 3 | 互 kernel (Fano line H) | F₂³ linear algebra | Fixed under coarse-graining; the 0.5-bit freedom |
| 4 | Complement-closed | Q₃ automorphism | Only element where σ(木)=木; fixed point of Z₅ anti-automorphism |
| 5 | Cycle conjugator | Z₅ 生/克 algebra | 生 cycle reverses to 克 cycle at 木; creates necessary friction |
| 6 | He Tu generative origin | Compass/spatial | Starting point of both 生 and 克 cycles; only element with a 克 He Tu pair |

These properties come from different mathematical structures (cyclic arithmetic, binary ordering, Fano geometry, group automorphisms, Z₅ cycle algebra, compass geometry). Their convergence on a single element is either a design principle or a consequence of a constraint not yet identified.

**[open question — M6]:** Is the convergence forced? Complement closure (4) forces {震,巽} to be paired. Placing this pair on the 互 kernel (3) is the 0.5-bit choice. Does that choice force palindrome centrality (1) and b₀ hinge position (2) on the 先天 cycle, or are those independent alignments?

---

## §IX. 先天 vs 後天: Retrograde and Prograde on Z₅

### Finding IX.1: The two arrangements are temporal inverses on the 生 cycle

**[measured]** The 先天 (Fu Xi / Before Heaven) and 後天 (King Wen / After Heaven) trigram cycles projected onto Z₅:

**先天:** 金→金→火→木→木→水→土→土
**後天:** 火→土→金→金→水→土→木→木

| | 先天 | 後天 |
|---|---|---|
| Forward 生 | 1 (seam only) | **4** |
| Retro 生 | 2 | 0 |
| Retro 克 | 2 | 2 |
| 比和 | 3 | 2 |
| **Non-trivial direction** | **4/5 retrograde** | **4/6 prograde** |

先天 runs backward on the 生 cycle (4/5 non-trivial steps retrograde). 後天 runs forward (4/6 prograde). "Before Heaven" unwinds toward origins. "After Heaven" follows the generative direction.

### Finding IX.2: The 克 relationships are invariant across both arrangements

**[measured]** Both cycles contain exactly 2 retrograde 克 steps and 0 forward 克 steps. The two 克 relationships are:
- 土克水 (Earth overcomes Water) — step 6 in 先天, step 5 in 後天
- X克Y at the metal/fire or wood/earth boundary — step 2 in 先天 (火克金), step 6 in 後天 (木克土)

The destructive relationships are preserved. The difference between 先天 and 後天 is entirely in the direction of the 生 (generative) steps. 先天 runs 生 backward (child→parent). 後天 runs 生 forward (parent→child). Destruction is the same in both frames.

### Finding IX.3: 後天 has one contiguous 克 break

**[measured]** The 後天 Z₅ step sequence:

```
FORWARD 生, FORWARD 生, 比和, FORWARD 生, RETRO 克, RETRO 克, 比和, FORWARD 生
火→土       土→金       金→金  金→水       水→土       土→木       木→木  木→火
```

The generative flow runs forward for 4 steps (火→土→金→金→水), hits a wall (two consecutive retrograde 克 steps: 水→土→木), then resumes forward (木→木→火). The 克 break is contiguous — a single interruption in the generative flow.

Compare 先天:
```
比和, RETRO 克, RETRO 生, 比和, RETRO 生, RETRO 克, 比和, FORWARD 生
金→金  金→火      火→木      木→木  木→水      水→土      土→土  土→金
```

先天 alternates: 比和 and retrograde steps interleave throughout. The single forward step is the seam (坤→乾). No contiguous generative run longer than 1.

### Finding IX.4: 木 is the pivot in both arrangements

**[measured]** In 先天: 木 is the palindrome center (positions 4–5). The retrograde flow is symmetric around 木.

In 後天: 木 is the re-entry point after the 克 break. Step 6 lands on 木 (土→木, the second 克). Step 7 rests (木→木, 比和). Step 8 departs from 木 (木→火, resuming forward 生). 木 is where the generative flow restarts after destruction.

| Role | 先天 | 後天 |
|------|------|------|
| 木 as... | Still point (palindrome center) | Restart point (post-克 re-entry) |
| What surrounds 木 | Symmetric retrograde pressure | Destruction before, generation after |
| 木→火 step | Retrograde (火 is 木's child, but runs backward) | Forward (木 generates 火) |

In 先天, 木 is at rest — everything flows around it. In 後天, 木 is at the turning point — destruction ends and generation resumes.

### Interpretation

The 先天/後天 pair encodes two complementary temporal orientations:
- **先天** (pre-manifest): time runs toward origins. The generative chain unwinds. Each moment points back to its source. One creative burst (坤→乾) resets.
- **後天** (manifest): time runs toward consequences. The generative chain builds forward. Two destructive breaks (水→土→木) punctuate the flow, and 木 restarts it.

The tradition places 先天 as the pattern "before heaven" — the template, the potential. 後天 is "after heaven" — the operational, the actual. The Z₅ projection makes this precise: 先天 is retrograde (toward cause), 後天 is prograde (toward effect). Both share the same destructive structure; they differ only in which direction generation flows.

---

### What remains at the boundary

One question sits at the edge of this investigation: is there a natural system with 3-dimensional binary structure (not scalar discretization) where Q₃ adjacency is intrinsic and the grammar would apply to actual state transitions? This is the question of whether the grammar has any physical instantiation beyond the mathematical object itself.
