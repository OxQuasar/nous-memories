# Mod-8 Investigation — Exploration Log

> Structural relationship between the 先天 mod-8 divination arithmetic and the F₂³ algebraic structure.
> Questions M1–M5 in `questions.md`.

---

## Iteration 1: Foundation — Bit-Layer Decomposition and Mod-8 Cycle

**Script:** `m1_mod8_structure.py`

### What was tested

Seven computations addressing M1 (五行 partition in mod-8) and M2 (cyclic shift invariance):

1. Foundation table: 8 trigrams with 先天 position, F₂³ vector, 五行 element, complement partner
2. Bit-layer 五行 decomposition: all 12 Q₃ edges classified by which bit they flip and their 五行 type
3. Mod-8 cycle type sequence: 五行 types of all 8 consecutive transitions in the 先天 ordering
4. Gray code comparison: 五行 types of the standard reflected Gray code cycle on Q₃
5. All Q₃ Hamiltonian cycles: exhaustive enumeration (6 distinct cycles), 五行 type counts for each
6. Cyclic shift analysis: for each shift k=0..7, how many of the 28 trigram pairs change 五行 type
7. Complement-respecting surjection landscape: all 240 valid surjections F₂³ → Z₅, bit-layer 五行 decomposition for each

### What was found

**[measured] Bit-layer decomposition — maximally differentiated 五行 content.**

| Layer | 比和 | 生 | 克 |
|-------|------|-----|-----|
| bit₂ (top) | 2 | 2 | **0** |
| bit₁ (mid) | 0 | 0 | **4** |
| bit₀ (bot) | 0 | 2 | 2 |

bit₂ is the unique 克-free layer. bit₁ is pure 克 — every mid-bit flip produces 克.

**[proven] Mechanism for bit₁ = pure 克:** Within each b₀-half, the mid-bit separates elements at Z₅ distance ±2. In b₀=1: b₁ splits Metal{111,011} from {Fire(101), Wood(001)}, both at 克 distance. In b₀=0: b₁ splits {Water(010), Wood(110)} from Earth{000,100}, both at 克 distance.

**[proven] Mechanism for bit₂ = 克-free:** Top-bit flips preserve (b₁,b₀). Metal and Earth are defined by (b₁,b₀) = (1,1) and (0,0) — mapping to themselves (比和). Fire and Water share their (b₁,b₀) with Wood: Fire(0,1)↔Wood(0,1) and Water(1,0)↔Wood(1,0), both Z₅ distance 1 = 生.

**[measured] Mod-8 cycle type sequence: {比和, 克, 生, 比和, 生, 克, 比和, 生}.**

Counts: 比和=3, 生=3, 克=2. The three 比和 steps occur at within-element pairs (Metal at 1→2, Wood at 4→5, Earth at 7→8). Complement gives partial palindrome: T(k)=T(8-k) for k=1,2,3. The 8th step (坤→乾 = Earth→Metal = 生) is the wraparound "seam" — self-paired under complement, not constrained to match any other step.

**[measured] All 4 Hamming-1 steps on the mod-8 cycle flip bit₂ exclusively (XOR = 100).** Their 五行 types: 2比和, 2生, **zero 克**. The mod-8 cycle's Q₃ edges are entirely in the 克-free layer.

**[measured] The 2 克 transitions on the mod-8 cycle (steps 2→3 and 6→7) both occur at Hamming distance 2 (XOR = 110 = bit₂+bit₁).** They are NOT Q₃ edges. The 克 enters the cycle exclusively through the multi-bit jumps that include the 克-saturated bit₁.

**[measured] Gray code cycle: 比和=1, 生=3, 克=4.** 克-dominated, matching Q₃ edge proportions (6/12 = 50% 克). The Gray code samples Q₃ faithfully; the mod-8 cycle systematically deviates.

**[measured] All 6 Q₃ Hamiltonian cycles have 克 ≥ 3.** Distribution: {3, 3, 4, 4, 5, 5}. The mod-8 cycle's 克=2 is impossible for any Q₃ edge-path.

**[proven] Structural explanation:** The union of bit₀ and bit₂ edges forms exactly two disjoint 4-cycles: {坤,艮,離,震} (b₁=0 half) and {坎,巽,乾,兌} (b₁=1 half). Any Hamiltonian cycle must bridge these halves, requiring at least some bit₁ edges, each of which is 克. The mod-8 cycle avoids this by using non-Q₃ transitions (Hamming distance 2 and 3) to cross the b₁ boundary.

**[measured] No non-trivial cyclic shift S_k (k≠0) preserves the 五行 type of all 28 trigram pairs.** S₄ (complement) is minimally destructive: 12/28 pairs change. The element map is never well-defined for k≠0 (paired elements split under shifting). The 五行 structure is fundamentally incompatible with Z₈ cyclic symmetry.

**[measured] Complement-respecting surjection landscape: 192/240 (80%) have at least one 克-free bit-layer.** By partition: {2,2,2,1,1} = 168/192 (87.5%), {4,1,1,1,1} = 24/48 (50%). By S₃ symmetry of bit positions, each specific bit-layer is 克-free in ~30% of surjections. The canonical assignment's bit₂ being 克-free is a 1-in-3 coincidence relative to the 先天 ordering's bit₂ selection.

**[measured] The correct Z₅ complement involution is x ↦ (4−x) mod 5 (fixes 2/Wood, swaps 0↔4/Metal↔Earth, 1↔3/Water↔Fire).** The originally assumed x ↦ (5−x) mod 5 does NOT contain the canonical assignment.

### Key structural finding

Two independently determined facts conspire to produce 克-exclusion on the mod-8 cycle's Q₃ edges:
1. The 先天 ordering sorts by lower bits first (b₀→b₁→b₂), so single-step changes toggle bit₂ — the highest bit, which changes most frequently in the descending binary counter
2. The canonical 五行 assignment (forced by complement-respecting surjection uniqueness) makes bit₂ flips 克-free

The alignment is a 1/3 coincidence (any of the three bit-layers could be 克-free). The existence of a 克-free layer is generic (80% of surjections). But the **Q₃ floor** (克 ≥ 3 for any Q₃ Hamiltonian cycle) is structural: it follows from the bit₀+bit₂ union splitting into two 4-cycles, forcing any Q₃ path through 克-saturated bit₁ edges.

---

## Iteration 2: Trigram-Level Completion — Cycle Landscape and Q₃ Floor Mechanism

**Script:** `m2a_cycle_landscape.py`

### What was tested

Three computations closing the trigram-level analysis:

1. Bit₀+bit₂ union graph: cycle decomposition and identification of b₁ halves
2. Pure-克 layer count across all 240 complement-respecting surjections
3. Full 8-cycle scan: all 2520 distinct 8-cycles on 8 labeled vertices, 克-count distribution, complement-palindrome subset

Also: minimum bit₁ edge count across Q₃ Hamiltonian cycles.

### What was found

**[measured] Bit₀+bit₂ union = two disjoint 4-cycles.** Component 1: {坤,震,離,艮} (b₁=0 half). Component 2: {坎,兌,乾,巽} (b₁=1 half). Edge layers alternate [bit₀, bit₂] within each cycle. The b₁ bit is frozen within each component.

**[measured] Minimum bit₁ edges in any Q₃ Hamiltonian cycle: 2.** This is the topological minimum (must enter and exit each b₁ half). Since all bit₁ edges are 克, this gives 克 ≥ 2 from bit₁ alone.

**[proven] The floor rises from 2 to 3 due to asymmetric 克 distribution in b₁ halves.** In b₁=1 half {坎,兌,乾,巽}: both bit₀ edges are 克 (Water↔Metal and Wood↔Metal). Any Hamiltonian path through this 4-vertex component uses 3 of 4 edges, so at least one bit₀ 克 edge is unavoidable. In b₁=0 half {坤,震,離,艮}: one bit₀ edge is 克 (Earth↔Wood), one is 生 (Earth↔Fire) — avoidable. Complete forcing chain: bit₁ pure-克 → 2 bit₁ bridges forced → b₁=1 has 2/2 bit₀ edges 克 → Hamiltonian path forces ≥1 bit₀ 克 → total ≥ 3.

**[measured] Pure-克 layer prevalence: 120/240 (50%) of surjections have at least one pure-克 layer.** By partition: {2,2,2,1,1} = 120/192 (62.5%), {4,1,1,1,1} = 0/48 (0%). Per-layer counts: exactly 48 surjections have pure-克 at each bit-layer (perfect S₃ symmetry). The {4,1,1,1,1} partition never produces pure-克 — having 4 trigrams on one element guarantees at least one 比和 edge per layer.

**[measured] Full 8-cycle landscape (2520 cycles):**

| 克 count | Cycles | % | Cumulative % |
|----------|--------|---|--------------|
| 0 | 16 | 0.6% | 0.6% |
| 1 | 96 | 3.8% | 4.4% |
| **2** | **384** | **15.2%** | **19.7%** |
| 3 | 624 | 24.8% | 44.4% |
| 4 | 668 | 26.5% | 70.9% |
| 5 | 512 | 20.3% | 91.3% |
| 6 | 152 | 6.0% | 97.3% |
| 7 | 64 | 2.5% | 99.8% |
| 8 | 4 | 0.2% | 100% |

Mean 克 = 3.714 (= 8 × 13/28, matching the null model). The mod-8 cycle's 克=2 is at the **19.7th percentile** — below average but not extreme. 384 cycles share this count.

**[measured] Complement-palindrome cycles: 48 total.** All 48 complement-paired cycles automatically satisfy the type-palindrome T(k)=T(8-k). 克 distribution within this subset: {0:4, 2:14, 3:8, 4:12, 5:4, 6:2, 7:4}. 克=1 never appears (odd constraint from palindrome structure). The mod-8 cycle is one of 14 complement-palindrome cycles with 克=2.

**[measured] The mod-8 cycle appears as the reversed 先天 order** (坤→艮→坎→巽→震→離→兌→乾) in the canonical enumeration.

### Structural summary — trigram level complete

The bit-layer decomposition {P₂(比和), P₃(生), P₄(克)} from the Chebyshev sequence (R258) has a specific interaction with the mod-8 cyclic topology:

- The 先天 ordering selects bit₂ (克-free) for its Q₃ edges — a 1/3 coincidence
- The Q₃ floor (克 ≥ 3 for any Hamiltonian cycle) is a topological impossibility result with a complete forcing chain
- The mod-8 cycle achieves 克=2 (below the Q₃ floor) by leaving Q₃ at its 克 transitions
- This 克=2 is not extreme — 15.2% of all 8-cycles and 29.2% of complement-palindrome cycles achieve it
- No cyclic shift preserves 五行 pair types: the Z₈ and Z₅ structures are fundamentally incompatible

### What remains untested

- M3: hexagram-level distribution under the 梅花 date formula (lower = upper + hour mod 8)
- M4: grammar (GMS/valve) survival under mod-8 topology
- M5: which topology governs transition detection from sequential data
- 梅花 date formula verification against source text
- Connection between hour-shift 體用 distribution and M2 cyclic shift results

---

## Final Synthesis — Trigram-Level Investigation

### What was established

The mod-8 investigation answered its core question: the structural relationship between 先天 mod-8 divination arithmetic and the F₂³ algebraic structure is **topological separation with directional asymmetry**.

The algebraic layer (Q₃) is 克-dominated: 50% of edges carry 克 = P₄ (golden mean shift). The divination layer (Z₈) systematically filters 克 out: 0% of the mod-8 cycle's Q₃ edges are 克, and only 25% of its total transitions are 克. The divination layer selects for the structure that is complementary to the grammar.

Three categories of finding:

**Mechanism (proven):**
- Bit-layer decomposition: bit₂ = 克-free, bit₁ = pure 克, bit₀ = mixed. Traced to Z₅ distance structure within b₀-halves.
- Q₃ floor forcing chain: topological partition into b₁ halves → bridge requirement → asymmetric 克 in b₁=1 component → 克 ≥ 3 for any Q₃ Hamiltonian cycle.
- Mod-8 Q₃-edge selection mechanism: 先天 sorting order makes bit₂ the fastest-changing bit → all single-step Q₃ edges are bit₂ flips → all are 克-free.

**Coincidence (measured, calibrated):**
- Bit₂ being both the 先天-selected layer and the 克-free layer: 1/3 probability.
- 克-free layers exist in 80% of complement-respecting surjections — generic, not special.
- The mod-8 cycle's 克=2 is at the 19.7th percentile of all 8-cycles, 29.2nd percentile of complement-palindrome cycles — low but not extreme.

**Structural constraint (proven):**
- Q₃ floor theorem: 克 ≥ 3 is topologically forced for any Q₃ edge-path.
- Z₈/Z₅ incompatibility: no cyclic shift preserves 五行 pair types. The two algebraic frameworks are irreconcilable.

### Connection to broader investigation

The bit-layer decomposition is the Chebyshev sequence {P₂, P₃, P₄} = {1, √2, φ} from R258, reframed as 五行 content. The Q₃ floor theorem says φ (the GMS spectral radius) is topologically unavoidable on Q₃ — any process that stays on Q₃ edges must encounter the φ-sector. The mod-8 cycle escapes by leaving Q₃, but actual single-bit line changes in hexagrams cannot.

This operationalizes the Z₂/Z₅ incommensurability from number-structure.md: the 先天 arrangement is Z₂-optimal (complement-first), the 五行 grammar is Z₅-optimal (relational), and these two optimization axes are incompatible at the level of edge selection.

Cross-workflow observation: the mod-8 克-suppression at generation (25% of cycle steps, 0% of Q₃ edges) mirrors the ti_hu 克-dominance at evaluation (63% adversarial, from atlas-mh Finding I.1). If 克 is rare at input and dominant at interpretation, 克 signals carry high discriminative power — the system may be calibrated so that the informationally valuable signal (克) is rare at generation and amplified at evaluation. This parallels the "体互最紧" conjecture: the highest-adversarial position is where favorable signals are most informative.

### What remains untested

- **M3:** Hexagram-level 體用 distribution via date formula. Substantially answered by lower = upper + hour mod 8, but exact formula needs verification against 梅花易數 source text. The cyclic shift analysis from M2 already contains the per-hour 體用 distributions.
- **M4:** Grammar survival under mod-8 topology. The GMS lives on 克 edges; the divination's Q₃ edges avoid 克 entirely. Does this mean the grammar is invisible to divination-generated states, or does it re-emerge at hexagram level?
- **M5:** Which topology governs transition detection from sequential divination data or price discretization? Depends on M4.

---

## Iteration 3: M3 — 體用 Distribution Under the Date Formula

**Script:** `m3_tiyong_distribution.py`

### What was tested

Five computations addressing M3 (hexagram-level 體用 distribution via the 梅花 date formula):

1. Per-shift 體用 distribution: for each cyclic shift h ∈ {0..7}, the 五行 type (比和/生/克) of all 8 (upper, lower) pairs where lower = S_h(upper) on the 先天 ordering
2. Hour → shift mapping: how the 12 地支 hours map to 8 shifts via h mod 8, with weights
3. Ergodic average: hour-weighted and unweighted type distributions vs null (uniform independent pairs)
4. Special structure: S₄ analysis (is it the complement map?), 克-enrichment by shift, bit-layer decomposition of shift 2
5. Moving line interaction: how gcd(8,6) = 2 couples moving line parity to hexagram parity, directed 体用 distributions

### What was found

**[measured] Per-shift undirected type distribution:**

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

**[proven] Mirror symmetry: S_h and S_{8-h} produce identical undirected type distributions.** This follows from pair reversal: S_{8-h} generates the same pairs as S_h in opposite order, and undirected 五行 type is symmetric (d(a,b) = d(b,a)). No complement structure is needed for this proof. For directed relations, S_h and S_{8-h} have *transposed* distributions (克体 ↔ 体克用, 生体 ↔ 体生用).

**[proven] 比和 concentration at shifts {0, 1, 7} is forced by 先天 pairing structure.** 比和 requires same-element trigrams. The paired elements occupy adjacent 先天 positions: {乾,兌}=Metal at (1,2), {震,巽}=Wood at (4,5), {艮,坤}=Earth at (7,8). The singletons Fire(離=3) and Water(坎=6) can only produce 比和 with themselves (shift 0). Non-identity 比和 requires landing on the same-element neighbor = shift ±1. This is a direct consequence of the 先天 ordering placing paired elements adjacent.

**[proven] Unweighted shift average exactly equals the null distribution.** Cycling through all 8 shifts generates every ordered pair (upper, lower) exactly once across the 64 total pairs (8 shifts × 8 uppers). Therefore the type distribution must equal the distribution over all 64 ordered pairs: 比和 = 14/64 = 21.88%, 生 = 24/64 = 37.50%, 克 = 26/64 = 40.62%. This is algebraically necessary, not a measurement.

**[measured] Hour-weighted ergodic deviation from null:** The 12 地支 hours map non-uniformly to shifts: shifts 1–4 get weight 2 (hours H and H+8 collapse), shifts 0,5,6,7 get weight 1. The克-enriched shifts 2,3,4 are doubly weighted, pulling the actual distribution toward 克:

| Type | Actual (hour-weighted) | Null | Δ |
|------|------------------------|------|---|
| 比和 | 17.71% | 21.88% | −4.17% |
| 生 | 39.58% | 37.50% | +2.08% |
| 克 | 42.71% | 40.62% | +2.08% |

**[measured] S₄ is NOT the complement map.** S₄ maps position p to (p+4) mod 8, which sends 乾→巽, 兌→坎, etc. — flipping only bit₀ in F₂³. The true complement (bitwise NOT) maps p ↔ (9−p) in 先天 positions: {乾↔坤, 兌↔艮, 離↔坎, 震↔巽}. This is a reversal of the 先天 sequence, not a cyclic shift.

**[proven] Shift 2 decomposes into two maximally differentiated bit-layer populations.** The 8 pairs under shift 2 split exactly into:
- 4 pairs with XOR = 010 (pure bit₁): all 克 (乾→離, 兌→震, 巽→艮, 坎→坤)
- 4 pairs with XOR = 011 (bit₁⊕bit₀): all 生 (離→巽, 震→坎, 艮→乾, 坤→兌)

The 50% 克 at shift 2 is not a statistical balance — it's two perfectly typed populations from distinct bit-layer compositions. Even shifts (2, 4, 6) all produce exactly 50% 克 with zero 比和, likely from analogous clean partitions.

**[proven] Mod-8/mod-6 gcd=2 coupling.** The moving line m = S mod 6, where S = Y+M+D+H. Since lower_raw = S mod 8, and gcd(8,6) = 2, the parity of lower_raw determines the accessible moving lines:
- Even lower_raw → m ∈ {2, 4, 6} → P(upper = 体) = 1/3
- Odd lower_raw → m ∈ {1, 3, 5} → P(upper = 体) = 2/3

For any shift, exactly 4 of 8 uppers give each parity, so the average P(upper = 体) = 1/2. But for each specific (upper, shift) pair, there is a deterministic 2:1 bias. The 体/用 assignment is structurally constrained by the same timestamp that determines the trigrams.

**[measured] Directed ergodic average (hour-weighted, with moving-line 体 probability):**

| Relation | Actual | Null | Δ |
|----------|--------|------|---|
| 比和 | 17.71% | 21.88% | −4.17% |
| 生体 | 19.79% | 18.75% | +1.04% |
| 体生用 | 19.79% | 18.75% | +1.04% |
| 体克用 | 20.83% | 20.31% | +0.52% |
| 克体 | 21.88% | 20.31% | +1.56% |

Favorable (比和 + 生体 + 体克用) = 58.33% vs null 60.94%. The date formula is 2.6% less favorable than random chance — slightly more adversarial. The biggest driver: 比和 drops 4.17% (cyclic constraint eliminates identical-element pairs except at shifts 0,1,7). 克体 grows more than 体克用 (+1.56% vs +0.52%).

**[measured] Per-shift directed favorability:**
- Shifts 0: 100% favorable (all 比和)
- Shifts 1, 3, 5, 7: 58.3% favorable (4.67/8)
- Shifts 2, 4, 6: 50.0% balanced (4.00/8)

### Cross-level pattern noted during review

The investigation tracks a layered inversion across interpretation levels:

| Level | 克 tendency | Source |
|-------|------------|--------|
| Single reading (M3) | +2.6% unfavorable | Hour-weighting |
| Nuclear (ti_hu, atlas-mh) | 63% adversarial | Bit-sharing architecture |
| Arc (parity wall, atlas-mh) | Enriches favorable | Mod-8 parity constraint |

This is conjectured (not proven) to be a design principle: adversarial components make favorable signals high-information (rare at generation, amplified at evaluation). Finding 生体 at ti_hu has a 12.5% base rate, making it maximally discriminative. Whether this pattern is intentional design or structural consequence of the axioms is not established.

### What remains untested

- **M4:** Grammar (GMS/valve) survival at hexagram level. The specific test: for each fixed upper trigram, compute the 12-hour directed 体用 sequence and check for GMS violations (consecutive 克, consecutive 克体). The mod-6 moving-line coupling may act as a filter that prevents consecutive 克体 even when consecutive undirected 克 occurs.
- **M4 subtlety:** The three possible outcomes carry different implications:
  1. GMS holds at undirected level → grammar visible at coarsest level (surprising given shifts 2-6 carry 40-62.5% 克)
  2. GMS fails undirected, holds directed → mod-6 体 assignment acts as grammatical filter; moving line is the bridge between Z₈ and Q₃
  3. GMS fails at both levels → grammar does not survive the passage from Q₃ to Z₈ at hexagram level
- **M5:** Which topology governs transition detection from sequential data? Depends on M4.
- Bit-layer decomposition for all 8 shifts (currently only shift 2 analyzed)
- Verification that directed S_h ↔ S_{8-h} transposition holds in the computed data

---

## Iteration 4: M4 — Grammar Survival at Hexagram Level

**Script:** `m4_grammar_survival.py`

### What was tested

Six computations addressing M4 (does the Q₃ grammar — GMS, valve — survive at the hexagram level when the 梅花 date formula generates 体用 sequences?):

1. Per-upper 12-hour undirected 体用 sequences: for each of 8 upper trigrams, the sequence of undirected 五行 types (比和/生/克) across the 12 地支 hours, with consecutive-克 (GMS violation) markers
2. Per-upper 12-hour directed sequences: same with moving-line uncertainty (3 equally likely moving lines per hour from the gcd=2 constraint)
3. GMS test — undirected: count of consecutive-克 pairs across all 8 uppers × 11 consecutive pairs = 88 total
4. GMS test — directed: for each undirected 克-克 pair, check whether any of the 9 moving-line assignment combinations produces consecutive 克体-克体
5. Valve test: count 克→生 transitions (should be 0 under the Q₃ valve)
6. Transition matrix: full undirected type-to-type transition counts with null expectation comparison

### What was found

**OUTCOME 3: Grammar does not survive.** All three tests fail decisively.

**[measured] GMS undirected: FAIL.** 24/88 consecutive-hour pairs (27.3%) have consecutive 克. Every upper trigram has at least 1 violation. Per-upper counts:

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

Metal and Wood trigrams are worst offenders (4-5 violations). Fire has the fewest (1).

**[measured] GMS directed: FAIL.** All 24 undirected 克-克 pairs have at least one moving-line assignment producing consecutive 克体-克体. The mod-6 coupling provides zero structural protection. The probability of 克体-克体 per undirected 克-克 pair ranges from 0.2222 to 0.4444. Expected total 克体-克体 events across all 88 pairs: 7.33 (8.3%).

**[measured] Valve: FAIL.** 克→生 = 10 out of 37 克-outgoing transitions (27.0%). Not zero — not even close. The valve is thoroughly violated.

**[measured] 克 is clustered, not random.** The transition matrix:

|  | →比和 | →生 | →克 | Total |
|---|---|---|---|---|
| 比和→ | 6 | 7 | 4 | 17 |
| 生→ | 5 | 18 | 11 | 34 |
| 克→ | 3 | 10 | 24 | 37 |

克→克 = 24 vs null expectation 16.1 — 49% enrichment over i.i.d. 克→生 = 10 vs null 14.9 — suppressed ~33% from null, but not zero.

**[proven] Mechanism for GMS failure.** The 12-hour sequence visits shifts 1→2→3→4→5→6→7→0→1→2→3→4. Shifts 2-6 form a contiguous block of 克-heavy shifts (0% 比和, 50-62.5% 克). Any upper trigram that maps to 克 at shift h is likely to map to 克 at shift h+1 because 五行 distances change slowly across neighboring cyclic shifts. The grammar needs Q₃-edge locality (single bit-flips); the calendar navigates via Z₈ cyclic shifts (multi-bit jumps). These are structurally incompatible.

**[measured] 克-clustering is autocorrelation from sequential sampling of a spatially structured distribution.** The 先天 cycle organizes 五行 types spatially: {比和, 克, 生, 比和, 生, 克, 比和, 生}. Traversing this sequence hourly creates temporal correlations. The partial valve suppression (克→生 at 27% instead of null 40%) is the same autocorrelation seen from the other direction: if 克 clusters, 克→non-克 transitions are depleted. This is a Z₈ property, not a shadow of the Q₃ grammar.

### Structural conclusion

**The topological separation between Q₃ and Z₈ is total.** The grammar (GMS, valve, forcing chain) lives exclusively on Q₃ edges. The divination formula operates exclusively on Z₈ cyclic shifts. The 先天 permutation connects them as a bijection on vertices but cannot transport edge constraints.

| | Q₃ (algebraic) | Z₈ (calendrical) |
|---|---|---|
| Topology | Hypercube edges | Cyclic adjacency |
| 克 at edges | 50% (dominant) | 0% at Q₃ edges, 25% overall |
| Grammar | GMS, valve, forcing chain | None (free) |
| 克 at hexagram level | N/A | 42.71% |
| Temporal constraints | Forbidden patterns (GMS) | Autocorrelation only |

### Impact on M3 conjectures

The layered inversion pattern (adversarial components → favorable trajectories) from Iteration 3 is now fully attributed to Z₈ structure (parity wall, hour-weighting) rather than Q₃ grammar. The grammar was never the mechanism for arc-level favorability — the parity wall (atlas-mh IV.3) operates as a mod-8 parity constraint independent of GMS. Outcome 3 clarifies this: the Z₈ and Q₃ constraint systems are independent.

### What remains untested

- **M5:** Whether real sequential data (price returns, etc.), when discretized mod-8, preferentially produces Q₃-edge transitions (Hamming distance 1). This is an independent empirical question, no longer connected to the calendar formula. The calendar is one specific Z₈ navigation — arguably the worst for accessing Q₃ grammar, since it maximizes multi-bit jumps. Data-driven sequences might navigate Q₃ more naturally. Unknown effect size; requires external data.
- M5 is a different kind of question from M1-M4. M1-M4 were structural/algebraic with definitive answers from exhaustive enumeration. M5 is empirical with uncertain effect size. The structural investigation of the mod-8/Q₃ interface is complete at M4.

---

## Iteration 5: M5 — Topology Detection in Empirical Data

**Script:** `m5_topology_in_data.py`

### What was tested

Six computations addressing M5 (does discretized sequential data prefer Q₃ edges?):

1. Hamming distance distribution of consecutive transitions: for BTC daily returns (2015-2025, N=4016) and three synthetic baselines (Gaussian i.i.d., AR(1) ρ=0.3, GARCH(1,1), each N=4000), discretized into 8 quantile bins mapped through 先天→F₂³
2. 五行 type distribution of transitions: compared to null (比和=21.9%, 生=37.5%, 克=40.6%)
3. GMS test: consecutive-克 count vs i.i.d. expectation
4. Bit-layer decomposition of Hamming-1 transitions: 克-percentage per bit-layer, compared to grammar prediction (bit₁=100%, bit₂=0%, bit₀=50%)
5. Shuffled control: all tests repeated on randomly shuffled versions of each dataset (destroys temporal structure, preserves marginal distribution)
6. Summary table across all sources

### What was found

**[proven] Bit-layer grammar is tautological.** The bit-layer 克 percentages (bit₁=100%, bit₂=0%) hold identically across ALL datasets — BTC, Gaussian, AR(1), GARCH, and their shuffled controls. This is not a data signal. It is a mathematical property of the WUXING_MAP on Q₃: every bit₁ edge connects elements at Z₅ distance 2 (克), every bit₂ edge connects elements at Z₅ distance 0 or 1 (比和 or 生). Any sequence of 8-state symbols mapped through 先天→F₂³→Z₅ will show this. The grammar at the bit-layer level is baked into the functor, not extracted from data.

This retroactively clarifies M1's bit-layer decomposition: it was always a property of the map, not of any system being mapped. M5 establishes the boundary: observing bit-layer structure in data mapped through this functor cannot count as evidence about the data itself.

**[measured] GMS and valve fail for all data sources.** No dataset shows GMS suppression (all ratios ≥ 1.0) or valve suppression (克→生 is 30-37% everywhere, never near zero). Consistent with M4's structural result: the grammar requires Q₃-edge locality, which discretized time series do not provide.

| Source | GMS ratio | Valve (克→生%) |
|--------|-----------|----------------|
| BTC | 1.12x | 36.2% |
| Gaussian | 1.06x | 34.2% |
| AR(1) | 1.00x | 29.6% |
| GARCH | 1.05x | 36.9% |

**[measured] No data source shows Q₃-edge preference over null.** Hamming-1 transition fractions:

| Source | H=1 actual | H=1 shuffled | H=1 null | Δ from null |
|--------|-----------|-------------|----------|-------------|
| BTC | 34.8% | 38.5% | 37.5% | −2.7% |
| Gaussian | 37.0% | 37.2% | 37.5% | −0.5% |
| AR(1) | 40.3% | 38.1% | 37.5% | +2.8% |
| GARCH | 36.3% | 36.6% | 37.5% | −1.2% |

AR(1) shows slight Hamming-1 enrichment (+2.8%), but this is autocorrelation enriching small-step transitions generically — not Q₃-specific. BTC shows Hamming-1 *depletion* (−2.7%), the opposite of what Q₃ grammar access would require.

**[measured] BTC shows excess complement (Hamming-3) transitions.** BTC: 16.4% H=3 vs 12.5% null (+3.9%). This is the only substantial data-dependent signal. It reflects a known property of financial returns: extreme returns tend to be followed by opposite-extreme returns (volatility clustering + mean reversion from tails). The complement pairs in 先天 ordering are biased toward 生 (Metal↔Earth=生 appears twice), so excess complement transitions produce BTC's 克-depletion (34.5% vs 40.6% null, Δ=−6.1%). The 五行 map transforms a known data property into a specific element-type skew but adds no new information.

**[proven] Structural explanation for M5's null: R286-R287 obstruction.** Q₃ is not an interval graph (proven in projection/). Scalar time series are 1-dimensional. No 1-dimensional ordering of 8 states can reproduce Q₃ adjacency. The dimensional mismatch is topological — Q₃ has 3 independent binary dimensions, a scalar has 1. Q₃-edge preference would require the discretization to be a Gray code (the only encoding where metric proximity maps to Hamming proximity), but Gray code discretization encodes Q₃ adjacency by construction rather than discovering it.

### What M5 closes

M5 provides a definitive empirical null: no data source tested shows Q₃ grammar signals (GMS, valve) or Q₃-edge preference. Combined with M4's structural result (grammar fails for calendar formula), the conclusion is complete:

**The Q₃ grammar has no empirical footprint in discretized sequential data.** The grammar is an intrinsic property of the Q₃ edge-coloring under the complement-Z₅ surjection. It cannot be accessed by:
- Calendar-based navigation (M4: Z₈ cyclic shifts destroy forbidden-pattern structure)
- Quantile discretization of scalar time series (M5: topological dimensional mismatch, R286-R287)

The only way to access Q₃ adjacency would be through a system with natural 3-dimensional binary structure where each dimension transitions independently. Whether such systems exist is a question for the broader investigation, not the mod-8 thread.

---

## Final Synthesis — Complete Mod-8 Investigation

### What was established (M1-M5)

The mod-8 investigation answered its motivating question: **can the 先天 mod-8 divination arithmetic access the Q₃ algebraic grammar?** The answer is no, for topological reasons that constitute a clean impossibility result.

| Question | Answer | Type |
|----------|--------|------|
| M1: 先天 permutation on 五行 | Bit-layer decomposition: bit₂=克-free, bit₁=pure 克 | Proven |
| M2: Mod-8 addition on types | No shift preserves types; Z₈ ⊥ Z₅ | Proven |
| M3: 體用 distribution | Ergodic=null (proven); hour-weighted +2.6% adversarial (measured) | Proven+measured |
| M4: Grammar survival | Total failure — GMS 27.3% violation, valve non-zero | Measured |
| M5: Topology in data | Bit-layer tautological, GMS/valve fail empirically, no Q₃ signal | Proven+measured |

### The structural theorem

**Q₃ and Z₈ share vertices but are topologically incommensurable for grammar transport.**

The grammar (GMS, valve, forcing chain) is an intrinsic property of the Q₃ edge-coloring under the complement-Z₅ surjection. The divination (mod-8 calendar, quantile discretization) operates on Z₈ cyclic structure. The 先天 permutation bijects vertices but cannot transport edge constraints. It is a bijection, not a homomorphism — it maps objects but not relations.

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
- Bit-layer decomposition: bit₂=克-free, bit₁=pure 克. Traced to Z₅ distance structure. (M1)
- Q₃ floor forcing chain: 克 ≥ 3 for any Q₃ Hamiltonian cycle. (M1-M2)
- Ergodic null: unweighted shift average = null distribution exactly (8 shifts generate all 64 ordered pairs). (M3)
- R286-R287 obstruction: Q₃ is not an interval graph → scalar discretization cannot access Q₃ adjacency. (M5)
- Bit-layer tautology: 五行 typing of Q₃ edges is a functor property, not a data property. (M5)

**Measured (exhaustive or empirical):**
- Hour-weighting produces +2.08% 克-enrichment, −2.6% favorability vs null. (M3)
- GMS violation rate 27.3%, valve non-zero (10/37), at hexagram level under calendar formula. (M4)
- No Q₃-edge preference in BTC, Gaussian, AR(1), or GARCH data. (M5)
- BTC excess complement transitions (16.4% vs 12.5% null) = known financial tail reversion. (M5)

**Structural constraint (proven):**
- Z₈/Z₅ incompatibility: no cyclic shift preserves 五行 pair types. (M2)
- Topological separation is total: vertex bijection ≠ edge homomorphism. (M1-M5)

### Connection to broader investigation

The mod-8 investigation confirms the I Ching's algebraic structure (Q₃ grammar, complement-Z₅ forcing, φ-orbit) as a purely mathematical object — a property of the unique canonical edge-typing of Q₃ under complement-Z₅ axioms. The divination's operational structure (体用, parity wall, arc types) is an independent Z₈ arithmetic system that shares the same vertex set but has no access to the edge grammar.

The 梅花 divination system's practical structure — the parity wall favorability (OR=5.23), the ti_hu adversarial bias (63%), the layered inversion pattern — operates entirely within Z₈ arithmetic. These are real structural properties of the divination algorithm, but they derive from mod-8 parity constraints, not from Q₃ grammar.

### What remains at the boundary

One question sits at the edge of this investigation but belongs to the broader thread: is there a natural system with 3-dimensional binary structure (not scalar discretization) where Q₃ adjacency is intrinsic and the grammar would apply to actual state transitions? This is the question of whether the grammar has any physical instantiation beyond the mathematical object itself.

---

## Post-Synthesis Note

The investigation's resolution has three layers of increasing depth:

1. **M1-M2 (trigram level):** The topologies are incompatible. Z₈ cyclic adjacency ≠ Q₃ Hamming adjacency. No cyclic shift preserves 五行 types. This could have been accidental.

2. **M3-M4 (hexagram level):** The incompatibility persists through the date formula. GMS and valve are freely violated. The mod-6 moving-line coupling — the last candidate for a rescue mechanism — provides zero protection. This rules out workarounds.

3. **M5 (empirical/topological):** The incompatibility is topological, not accidental. Q₃ is not an interval graph (R286-R287). No scalar discretization can access Q₃ adjacency. The bit-layer grammar is tautological — a property of the functor 先天→F₂³→Z₅, indistinguishable from any data mapped through it. The representation's fingerprint is everywhere, and therefore evidentially nowhere.

Each layer deepens the previous. The result is not "the method doesn't work" but "the method works in Z₈ and the grammar works in Q₃, and these are genuinely different mathematical objects sharing a common labeling." The 先天 permutation lets you *read* both structures — it does not let you *cross* between them.
