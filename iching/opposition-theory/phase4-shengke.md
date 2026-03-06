# Phase 4 Capstone: 生克 and the Five-Phase Mapping Layer

## 1. The Scale-Bridge Thesis: Verdict and Evidence

**Thesis:** The 生克 system bridges concentrated opposition at n=3 (complement, maximum strength) with distributed opposition at n=6 (reversal-priority, weight preservation) — the 体/用 projection embeds n=3 evaluation within the n=6 framework, and the five-phase cycles encode the same anti-repetition principle that kac measures.

**Verdict: Refuted.** Two independent results close both pathways.

**First closure — uniform sampling theorem.** The 体/用 split assigns each hexagram's two trigrams directed roles (体=static reference, 用=dynamic event) based on which trigram contains the moving line. Across all 384 states (64 hexagrams × 6 moving lines), every ordered trigram pair (a, b) appears exactly 6 times. The Hamming distance distribution between 体 and 用 is *identically* the baseline distribution of all 64 ordered trigram pairs. The projection introduces zero bias — it is a structurally neutral sampling device. The bridge, if any, is not in the projection mechanism.

**Second closure — Z₂³ generation universality.** Both 生 and 克 cycle masks generate the full group Z₂³ under XOR closure. This was tested against all 50,400 valid surjections (8 trigrams → 5 elements, partition 2,2,2,1,1). Rate: 100% for both cycles, every assignment. This is forced by the partition geometry — 5 directed edges connecting groups of 1-2 trigrams in a 3-dimensional vector space over GF(2) always span. Z₂³ generation is a theorem of the partition shape, not a property of the traditional assignment.

The hypothesized bridge mechanism does not exist. The five-phase layer operates **orthogonally** to the hexagram-pairing structure — it neither concentrates nor distributes the opposition that Phases 1-3 characterized.

---

## 2. 生克 in Combinatorial Terms: What Survives the Mapping Layer

The traditional trigram→element assignment:

| Element | Trigrams | Intra-pair XOR | Intra-pair Hamming |
|---------|----------|----------------|--------------------|
| Metal (金) | Qian (111), Dui (110) | 001 | 1 |
| Wood (木) | Zhen (100), Xun (011) | 111 | 3 |
| Earth (土) | Gen (001), Kun (000) | 001 | 1 |
| Fire (火) | Li (101) | — | — |
| Water (水) | Kan (010) | — | — |

The mapping is 8→5, many-to-one, partition shape (2,2,2,1,1). Metal and Earth pair trigrams at minimum distance (d=1, single-bit flip). Wood is the anomaly: Zhen and Xun are **complements** (d=3). The tradition groups maximally distant trigrams as "same" in exactly one case.

### What the cycles produce

| Cycle | XOR masks | Count | Exclusive |
|-------|-----------|-------|-----------|
| 生 (generation) | {001, 100, 101, 110, 111} | 5 of 7 | {001, 110} |
| 克 (overcoming) | {010, 011, 100, 101, 111} | 5 of 7 | {010, 011} |
| Shared | {100, 101, 111} | 3 | — |

Both cycles use 5 masks and miss 2. The missed masks are exactly the other cycle's exclusives. The union covers all 7 nonzero elements of Z₂³.

### What survives the null model

Z₂³ generation: **universal** — every valid assignment achieves it. Not a finding.

**Partition cleanness** — the ratio of exclusive masks to total distinct masks — is 4/7 for the traditional assignment. This is the **maximum achievable value**. Only 6,720 of 50,400 surjections (13.3%) reach this maximum. The traditional mapping sits at the 100th percentile.

This is the Phase 4 replacement finding: the traditional assignment maximally differentiates the *transformation vocabularies* of the two interaction modes. Generation and overcoming use maximally non-overlapping XOR masks. The system is designed not for algebraic scope (which is generic) but for **modal complementarity** — making the two fundamental modes as distinguishable as possible in the transformation space.

---

## 3. The Evaluation Circuit (本→互→变): Opposition-Type Transitions

The Meihua system evaluates each (hexagram, moving_line) state through three hexagrams:

- **本卦** — the present hexagram
- **互卦** — the nuclear hexagram (L2-L3-L4 / L3-L4-L5)
- **变卦** — the hexagram after flipping the moving line

Each is evaluated against 体 by five-phase 生克, producing a triple (rel₁, rel₂, rel₃) of five-phase relationships.

### Non-redundancy

| Pattern | Count | Fraction |
|---------|-------|----------|
| All three same | 20 | 5.2% |
| One repeat | 200 | 52.1% |
| All three different | 164 | 42.7% |

94.8% of states have at least one change across the circuit. The three evaluations almost never agree. This is a geometric consequence of how the three hexagrams are constructed:

- 互卦 erases the outer shell and amplifies the inner core — it sees a different "slice" of the hexagram's structure
- 变卦 differs from 本卦 by exactly one line — a minimal perturbation that often shifts the trigram→element assignment

### Step transition rates

| Transition | Rate of five-phase change |
|------------|--------------------------|
| 本卦 → 互卦 | 71.9% |
| 互卦 → 变卦 | 77.1% |
| 本卦 → 变卦 | 83.3% |

Each step provides substantially new evaluative information. The circuit is designed for **progressive divergence** — each successive comparison is more likely to differ than the last.

---

## 4. Depth Separation and 体/用: Alignment or Independence

Phase 3 established a depth-function separation: outer lines buffer weight, inner lines carry opposition. Phase 4 asked whether the 体/用 assignment interacts with this depth structure.

**Answer: independence.** The 体/用 assignment depends only on which trigram contains the moving line — a binary choice between upper and lower — not on the line's depth position within the hexagram. The uniform sampling theorem (§1) confirms that all trigram pairs are represented equally regardless of which line is moving.

The connection between depth and evaluation is **indirect**, mediated entirely by the 互卦 amplification gradient:

**Theorem (互卦 amplification).** Flipping line k in a hexagram changes the 互卦 by a deterministic amount depending only on the line's depth layer:

| Layer | Lines | Hamming(互卦(x), 互卦(x ⊕ 2ᵏ)) |
|-------|-------|--------------------------------|
| Outer | L1 (bit 0), L6 (bit 5) | 0 — erased |
| Middle | L2 (bit 1), L5 (bit 4) | 1 — preserved |
| Inner | L3 (bit 2), L4 (bit 3) | 2 — amplified |

This follows deterministically from the 互卦 definition picking bits {1,2,3,2,3,4}: bits 2 and 3 each appear twice (amplification), bits 1 and 4 once (preservation), bits 0 and 5 never (erasure).

The gradient means that the 互卦 evaluation stage is **differentially sensitive** to changes at different depths — inner-line changes produce 2× the 互卦 perturbation of middle-line changes, and infinitely more than outer-line changes. This extends Phase 3's qualitative depth-function separation into a quantitative perturbation-sensitivity hierarchy.

But 体/用 itself is depth-blind. The depth structure enters the evaluation circuit only through the 互卦 transformation, not through the 体/用 assignment.

---

## 5. Shell-Only Opposition Pairs Under 生克

Phase 3 classified 4 KW pairs with signature (1,0,0) as "shell-only" — opposition lives entirely in L1/L6 and is invisible to nuclear projection. The remaining 28 pairs are "depth-penetrating."

### Five-phase agreement between partners

For each KW pair and each moving line, do both hexagrams receive the same five-phase evaluation?

| Category | Pairs | Agreement rate |
|----------|-------|----------------|
| Shell-only (1,0,0) | 4 | 50.0% |
| Depth-penetrating | 28 | 21.4% |
| All | 32 | 25.0% |

Shell-only pairs agree **2.33× more often**. The mechanism: when two hexagrams differ only at L1/L6, the perturbation often falls within the same element's trigram pair (Metal and Earth both pair at d=1, so a single-bit flip at the outer position frequently preserves element identity).

The overall 25.0% agreement rate is at the 41.4th percentile among surjections — unremarkable.

**Sample size caveat.** n=4 shell-only pairs is insufficient for statistical conclusions. The 2:0 split within these 4 pairs (2 at 100% agreement, 2 at 0%) is fully explained by whether the L1/L6 flip crosses an element boundary, but the pattern is too small to generalize.

---

## 6. The Five-Phase Cycle as Combinatorial Object

### Landscape

50,400 valid surjections from 8 trigrams to 5 elements with partition (2,2,2,1,1) were exhaustively enumerated. The 生 and 克 cycles are fixed directed pentagons on the abstract elements; what varies is which trigrams inhabit which vertices.

### Scorecard

| Metric | Traditional value | Percentile | Interpretation |
|--------|-------------------|------------|----------------|
| Z₂³ generation (both cycles) | Yes | 100% (universal) | Generic — forced by partition geometry |
| **Partition cleanness** | **4/7 (maximum)** | **100% (top 13.3%)** | **Distinctive — modal complementarity** |
| 克 edge-mean variance | 0.3600 | 96.2% | Extreme — driven by Kan→Li complement edge |
| 生−克 Hamming asymmetry | +0.218 | 76.9% | Moderate — 生 edges slightly longer than 克 |
| 生 mask count | 5 (minimum possible for generation) | 16.7% | Low end — maximally efficient generation |
| Edge autocorrelation | −0.300 | 67.4% | Unremarkable |
| Intra-element Hamming | 1.667 | 65.4% | Unremarkable |

### What the tradition optimizes

The traditional assignment is distinguished not by algebraic scope (universal) nor by any single Hamming statistic (moderate), but by **maximum differentiation between the two interaction modes**. The 生 cycle and the 克 cycle traverse the trigram space via complementary XOR mask vocabularies: each produces 2 exclusive masks that the other never uses, with 3 shared masks providing common ground.

The 克 cycle's extreme edge-variance (96.2nd percentile) provides a secondary signal: the Water→Fire edge (Kan 010 → Li 101, d=3) is the only complement transition in either cycle, concentrating maximal opposition into a single overcoming step. This creates the asymmetry between 生 (relatively uniform edge distances) and 克 (one extreme edge among milder ones).

---

## 7. Epistemic Inventory: Theorems vs Observations

### Combinatorial theorems (hold for all assignments, mapping-independent)

1. **Uniform sampling.** Every ordered trigram pair (a, b) appears exactly 6 times in the 384 (hexagram × moving_line) states. The 体/用 projection introduces no bias. *(Proved by counting.)*

2. **Z₂³ generation universality.** All valid (2,2,2,1,1) surjections generate Z₂³ on both 生 and 克 cycles. *(Proved by exhaustive enumeration of 50,400 assignments.)*

3. **互卦 amplification gradient.** Flipping line k changes the 互卦 by {0, 1, 2} Hamming positions depending deterministically on depth: outer→0, middle→1, inner→2. *(Proved from the definition: 互卦 picks bits {1,2,3,2,3,4}.)*

4. **Circuit non-redundancy.** The 本→互→变 evaluation produces all-same readings in only 5.2% of states. *(Computed from all 384 states; geometric explanation from theorem 3.)*

### Mapping-dependent observations (specific to the traditional assignment)

5. **Partition cleanness at maximum** (4/7, 100th percentile, top 13.3%). *(Ranked against all 50,400 surjections.)*

6. **克 edge-variance extreme** (96.2nd percentile). *(Ranked; driven by the Kan→Li singleton edge.)*

7. **生−克 Hamming asymmetry** (76.9th percentile). *(Ranked; moderate.)*

8. **Shell-only pair agreement** (50% vs 21.4%). *(Measured; n=4, underpowered.)*

9. **Partner agreement unremarkable** (41.4th percentile). *(Ranked; no signal.)*

### Boundary

Theorems 1-4 are properties of the binary and combinatorial substrate — they would hold under any element assignment. Observations 5-9 depend entirely on the tradition's specific mapping choices. The clean separation is Phase 4's main epistemic contribution: it shows precisely where "structure" ends and "tradition" begins.

---

## 8. The Opposition Theory After Four Phases: Synthesis

Four phases form a deductive arc that progressively characterizes the tradition's structural choices:

**Phase 1** mapped the landscape. Strength and diversity are orthogonal (r = 0, exact). KW uses algebraically pure masks (the 7 nonzero elements of the mirror-pair signature group Z₂³, near-uniformly distributed). There is a phase transition from n=4 (KW mediocre) to n=6 (KW extreme at 99.98th percentile), driven by the number of independent mirror pairs crossing the threshold where the full signature vocabulary becomes expressible.

**Phase 2** identified the generating principle. KW is the unique weight-preserving pairing among the 9 invariants of the hexagram's mirror-pair partition group (order 384). The 7-mask structure, the near-maximal algebraic diversity, and the 99.98th percentile strength are all *consequences* of choosing reversal wherever possible. Unique among 9 — the sharpest selection result in the study.

**Phase 3** decomposed this spatially. The outer pair (L1, L6) buffers weight; the inner pair (L3, L4) carries opposition. Nuclear trigrams are a projection (64→16→4, convergent in 2 steps), not an independent structural level. Two-level, not three-level. The commutativity classification (shell-only vs depth-penetrating opposition) reveals the KW rule's two-branch structure as a depth classifier.

**Phase 4** added the five-phase layer and found it **orthogonal to the hexagram-pairing structure**. The 体/用 projection is neutral; Z₂³ generation is universal. The tradition's distinctive contribution at this level is modal complementarity: maximum differentiation between the transformation vocabularies of 生 and 克. The 互卦 amplification gradient bridges Phase 3's depth separation into a quantitative sensitivity hierarchy for the evaluation circuit.

### The overarching characterization

The I Ching's traditional structural choices occupy distinguished positions in their respective combinatorial spaces:

| Level | Choice | Space | Position | Sharpness |
|-------|--------|-------|----------|-----------|
| Hexagram pairing | Reversal-priority (KW rule) | 9 mirror-pair-symmetric pairings | Unique minimum weight-tilt | **Unique among 9** |
| Trigram→element mapping | Traditional 五行 assignment | 50,400 valid surjections | Maximum partition cleanness | **Top 13.3% (6,720 of 50,400)** |

Both are selection principles — the tradition's choices are characterized by conservation and differentiation properties, not by extremization of any single opposition measure. The two levels operate independently, connected only by the shared geometric substrate of the binary structure. The first selection (Phase 2) is sharper than the second (Phase 4), suggesting the hexagram-pairing structure is more tightly constrained than the five-phase assignment.

This is a modest claim. It asserts structural characterization, not design intent, historical awareness, or metaphysical significance: *these choices, among all possible choices, have specific mathematical properties, and those properties are non-trivially rare.*

---

## 9. Open Questions Remaining

### Within the Phase 4 domain

1. **Max-cleanness elite structure.** ~6,700 surjections achieve maximum partition cleanness. The traditional assignment sits within this set but has not been further distinguished. The 克 edge-variance (96.2nd percentile) and the Wood anomaly (intra-element complement, d=3) might filter this set further, but the analysis is uninvestigated.

2. **Directed mask sequences.** The ordered sequence of XOR masks around each cycle may carry structure beyond what partition cleanness captures. Lag-1 autocorrelation was uninformative (67th percentile). More refined sequence statistics — or comparison to the kac measure at the hexagram level — remain untested.

3. **The Wood anomaly.** Zhen (100) and Xun (011) are the only intra-element complement pair (d=3). The only complement edge in either cycle is Kan→Li (also d=3) in the 克 cycle. Whether these two "complement anomalies" are structurally connected is open.

4. **互卦 amplification × partition cleanness interaction.** The sage identified this as the missing connection between Phase 4's two positive findings. Do inner-line perturbations (amplified by 互卦) preferentially land in 生-exclusive vs 克-exclusive mask territory? This would link the depth-sensitivity gradient to the modal complementarity finding.

### Across all phases

5. **Cross-scale divergence.** The n=3 tradition chose complement; n≥5 chose reversal. Phase 4 showed the five-phase layer is orthogonal to this — the divergence remains genuinely open. At n=3, the mirror-pair structure is too sparse to give reversal any advantage. At n≥5, richer geometry makes weight-preservation decisive. This may be an irreducible fork — two design logics appropriate to two geometric regimes — rather than a gap to be closed.

6. **Sequential variety (kac) integration.** The fourth axis (kernel anti-repetition along the KW sequence) has not been connected to the five-phase evaluation layer. Phase 4 established that the pairing level and the mapping level are orthogonal; whether the *sequence* level interacts with the mapping level is untested.

7. **Algebra ↔ meaning complementarity.** The inverse correlation between algebraic and semantic coverage in the KW sequence has no known precursor at n=3 or n=4.

8. **互卦 convergence interpretation.** The iteration 64→16→4 converges to {000000, 010101, 101010, 111111} in exactly 2 steps. Observed, documented, uninterpreted across three phases.

---

## Files

| File | Description |
|------|-------------|
| `phase4/shengke_foundation.py` | Round 1: 体/用 projection, element mapping, surjection enumeration |
| `phase4/foundation_results.md` | Round 1 results |
| `phase4/cycle_algebra.py` | Round 2: XOR mask algebra, partner agreement, 变卦 circuit |
| `phase4/cycle_algebra_results.md` | Round 2 results |
| `phase4/generation_test.py` | Round 3: Z₂³ null model, partition cleanness, directed profiles |
| `phase4/generation_test_results.md` | Round 3 results |
| `phase4/shengke_analysis.md` | Detailed Phase 4 analysis document |
| `phase4-shengke.md` | This document — Phase 4 capstone |
