# Atlas Phase 2 — Findings

> **Bit convention A:** b₀ = L1 (bottom), b₅ = L6 (top). Trigrams: b₀ = bottom line, b₂ = top line.

## Iteration 1: Cross-hexagram Network (II.E)

### Complement pairs on Z₅×Z₅

**Status: proven.** All 32 complement pairs verified: anti-automorphism π = (Earth↔Metal)(Fire↔Water)(Wood) maps cell (a,b) → (π(a),π(b)) with zero errors. Complement is a well-defined order-2 involution on Z₅×Z₅ that reverses the 生 cycle direction. Confirms synthesis result at atlas level.

Data: `cross_network_results.json` → `complement_pairs` (32 entries, all `pi_verified: true`).

### Reverse pairs on Z₅×Z₅

**Status: proven.** Reversal is NOT a Z₅ operation. 8 palindromes self-map. Of 28 non-palindromic pairs, exactly 6 exhibit coordinate swap (a,b)→(b,a):

| Pair | Cell mapping |
|------|-------------|
| 師 Shi ↔ 比 Bi | (Water,Earth) ↔ (Earth,Water) |
| 明夷 Ming Yi ↔ 晉 Jin | (Fire,Earth) ↔ (Earth,Fire) |
| 泰 Tai ↔ 否 Pi | (Metal,Earth) ↔ (Earth,Metal) |
| 既濟 Ji Ji ↔ 未濟 Wei Ji | (Fire,Water) ↔ (Water,Fire) |
| 需 Xu ↔ 訟 Song | (Metal,Water) ↔ (Water,Metal) |
| 大有 Da You ↔ 同人 Tong Ren | (Metal,Fire) ↔ (Fire,Metal) |

**Selection rule:** The 6 swapping pairs are exactly those where both trigrams are either both singletons (Fire, Water) or from the same paired-element class. When reversal crosses element boundaries asymmetrically (paired→singleton or vice versa), the coordinate swap fails. This is the {2,2,2,1,1} partition shape acting as a selection rule on which reversals the torus can see.

The remaining 22 pairs have no clean torus description — reversal operates at the Z₂³ level (bit-reversal within trigrams), not at the Z₅ level.

### 五行-equivalent hexagram classes

**Status: proven.** Two granularities:

**Full profile** (surface_cell, hu_cell, basin, palace_element): 58 classes — 52 singletons + 6 size-2 pairs. The 6 non-singleton pairs:

| Profile | Pair | XOR |
|---------|------|-----|
| (Metal,Earth \| Wood,Earth \| Kun \| Earth) | 臨/3 & 升/35 | 32 |
| (Wood,Earth \| Metal,Wood \| Cycle \| Wood) | 升/6 & 益/38 | 32 |
| (Metal,Earth \| Metal,Wood \| Cycle \| Earth) | 泰/7 & 蠱/39 | 32 |
| (Earth,Metal \| Earth,Wood \| Cycle \| Metal) | 復/24 & 歸妹/56 | 32 |
| (Wood,Metal \| Earth,Wood \| Cycle \| Wood) | 无妄/25 & 漸/57 | 32 |
| (Earth,Metal \| Wood,Metal \| Qian \| Metal) | 大過/28 & 遯/60 | 32 |

**All 6 pairs differ by exactly bit 5** (XOR = 32 = 0b100000). Bit 5 is the upper trigram MSB — it distinguishes paired trigrams within the same element (e.g., Kun↔Gen, both Earth). This is the exact residual bit the 五行 projection discards. Without 六親 (which recovers this bit through 納甲 branch sensitivity), the 五行 system is a 5-bit coordinate on a 6-bit space.

**Coarse** (surface_cell, basin): 45 classes — 26 singletons + 19 size-2 pairs. The 19 ambiguous pairs are consistently resolved by hu_cell or palace.

### 六親 word collisions

**Status: proven.** 59 unique 六親 words among 64 hexagrams. 5 collision pairs:

| Shared 六親 word | Pair | Distinguished by |
|-----------------|------|-----------------|
| 妻財 官鬼 兄弟 兄弟 妻財 子孫 | 復 Fu / 泰 Tai | surface_cell, hu_cell, basin, inner_val |
| 父母 官鬼 兄弟 兄弟 妻財 子孫 | 臨 Lin / 中孚 Zhong Fu | surface_cell, inner_val |
| 父母 官鬼 兄弟 父母 子孫 兄弟 | 謙 Qian / 履 Lu | surface_cell, hu_cell, palace_element, inner_val |
| 妻財 父母 官鬼 妻財 父母 官鬼 | 升 Sheng / 巽 Xun | surface_cell, hu_cell, inner_val |
| 父母 兄弟 妻財 妻財 父母 官鬼 | 頤 Yi / 小畜 Xiao Chu | surface_cell, hu_cell, basin, inner_val |

**Every collision pair is distinguished by surface_cell.** The palace system (which generates 六親) confuses pairs that differ in surface coordinates — the shell projection disambiguates what the palace projection conflates. This is three-chain independence from the dependency DAG: palace and surface_cell sit on independent chains.

### Two orthogonal degeneracy classes

The 五行-profile degeneracy (6 pairs, all bit-5 flips) and the 六親 degeneracy (5 pairs, all surface-distinguished) are non-overlapping. One lives in the shell projection's residual, the other in the palace projection's residual. This is the three-chain independence made visible as two orthogonal degeneracy classes.

---

## Iteration 2: 變 Neighborhood + 互 Graph on Torus (II.E continued)

### 變 neighborhood: four structural classes

**Status: proven.** The 25 torus cells partition into exactly 4 neighborhood classes, determined by element partition type:

| Class | Cells | Reachable | Universal | Partial | Pattern |
|-------|:-----:|:---------:|:---------:|:-------:|---------|
| Singleton×Singleton | 4 | 6 | 6 | 0 | Fully deterministic |
| Mixed (Singleton involved) | 12 | 7 | 5 | 2 | Moderate variation |
| Paired×Paired (no Wood) | 4 | 7 | 3 | 4 | Most within-cell variation |
| Wood-containing | 5 | 8 | 4 | 4 | Largest neighborhoods |

- Singleton×Singleton cells: zero within-cell variation. Every hexagram reaches the same 6 targets.
- Wood-containing cells reach 8/25 targets (32%) — the widest 變 spread.
- The 4-class structure is entirely forced by the {2,2,2,1,1} partition and the Hamming structure of trigram representatives within each element class.

Data: `torus_graphs.json` → `bian_neighborhood`.

### 互 graph: corrected well-definedness criterion

**Status: proven (corrects phase 1).**

Phase 1 stated: "cells containing at least one singleton element." The exact criterion is:

**lower ∈ {Fire, Water} AND upper ∉ {Wood}.**

Mechanism: 互 reads bits (b₁,b₂,b₃,b₄). Lower trigram contributes (b₁,b₂), upper contributes (b₃,b₄). For 互 to be well-defined on the torus, the element must uniquely determine the relevant bits:
- Lower position: only Fire (101) and Water (010) have 1 trigram, fixing (b₁,b₂).
- Upper position: all elements except Wood have trigrams that agree on (b₃,b₄). Wood's trigrams (巽=001, 震=110) give distinct (b₃,b₄) = (01) vs (11).

Result: 8/25 cells well-defined, 17/25 set-valued. Data: `torus_graphs.json` → `hu_graph`.

### 互 chains terminate at torus level after 1 step

Even starting from well-defined cells, one 互 step lands in a set-valued cell (e.g., (Fire,Earth) → (Water,Wood) → multi). The chain can only be continued at hexagram level, not torus level. The torus is definitively the wrong level for 互 iteration.

### Multi-attractor reachability

| Reachable attractors | Cells |
|:--------------------:|:-----:|
| 2 | 12 |
| 3 | 3 — (Earth,Wood), (Metal,Wood), (Wood,Earth) |
| 4 | 1 — (Wood,Wood) |

(Wood,Wood) is maximally ambiguous: all 4 attractors reachable. The *,Wood cells consistently reach 3+ attractors.

### Wood as maximal torus-level indeterminacy source

**Status: proven — single root cause.** Three independent observations:
1. Fixed point of complement anti-automorphism
2. Widest 變 neighborhood spread (8 targets vs 6–7 for others)
3. Most 互 attractors reachable (up to all 4)

All three trace to one fact: Wood's two trigrams (巽=001, 震=110) have Hamming distance 3 — the maximum possible. They share no bit positions. Every other paired element's trigrams share at least one bit. This is not three findings — it is one finding appearing three times through different projections.

---

## Iteration 3: 變×互 Cross-transformation (II.B/II.E)

### The 4-layer perturbation onion

**Status: proven (upgrades phase 1's 3-layer model).**

The 互 coordinate breaks the shell layer's internal symmetry, revealing 4 concentric layers:

| Layer | Lines | Bit | Surface | 互 cell | 互 attractor | Basin | Mechanism |
|-------|-------|-----|:-------:|:-------:|:------------:|:-----:|-----------|
| Outer | L1,L6 | b₀,b₅ | changes | 100% | 100%* | 100% | Invisible to 互 |
| Shell-outer | L5 | b₄ | changes | 50% | ~81% | 100% | MSB of hu_upper; parity-0 elements preserve |
| Shell-inner | L2 | b₁ | changes | 0% | ~81% | 100% | LSB of hu_lower; always changes element |
| Interface | L3,L4 | b₂,b₃ | changes | 0% | 0% | 0% | In both hu trigrams — total destruction |

*The reported 93.8% outer attractor preservation is a labeling artifact: the 8 "changes" are all 2-cycle label swaps (既濟↔未濟). Since hu_cell is 100% preserved for outer flips, the entire 互 chain is identical → attractor-as-set is 100% preserved. The "change" is which member of the 2-cycle is reached first — a convention, not a structural disruption.

### L2/L5 asymmetry mechanism

**Status: proven at bit level.**

- **L2 (b₁) = LSB of hu_lower** (trigram value = b₁ + 2b₂ + 4b₃). Every LSB-adjacent trigram pair maps to a different element: Kun/Earth↔Zhen/Wood, Kan/Water↔Dui/Metal, Gen/Earth↔Li/Fire, Xun/Wood↔Qian/Metal. **0/4 preserve element → 0% hu_cell preservation.**

- **L5 (b₄) = MSB of hu_upper** (trigram value = b₂ + 2b₃ + 4b₄). MSB-adjacent pairs: Kun/Earth↔Gen/Earth (SAME), Dui/Metal↔Qian/Metal (SAME), Zhen/Wood↔Li/Fire (DIFF), Kan/Water↔Xun/Wood (DIFF). **2/4 preserve element → 50% hu_cell preservation.**

The preserving pairs are exactly the parity-0 coset {Earth, Metal} — the paired elements whose two trigrams differ by ±4 (the MSB). The {2,2,2,1,1} partition determines which bit position preserves element identity.

### Attractor stability conditional on hu_cell change

| Layer | P(attractor changes \| hu_cell changes) |
|-------|:---------------------------------------:|
| Interface | 100% — total destruction |
| Shell | 25% — most changes stay in-basin |
| Outer | N/A (hu_cell never changes) |

Three-quarters of shell-layer 互 disruptions change the local neighborhood but not the convergence destination. The 25% that DO change attractor correspond to transitions crossing between the 2-cycle attractor neighborhood and fixed-point attractor neighborhoods.

### Basin ≥ attractor preservation

**Verified at every layer.** Basin is a coarser invariant than attractor (each attractor belongs to exactly one basin). Basin crossing always implies attractor crossing, but attractor can change within basin (the 2-cycle label swap).

Data: `bian_hu_cross.json`.

---

## Iteration 4: 凶/吉 Rates per Z₅×Z₅ Cell (IV.A)

### Core bridge at torus level

**Status: confirmed.** χ²=17.44, p=0.0002. Basin rates: Kun 20.8%, Qian 20.8%, Cycle 6.2%. Fixed-point basins carry 3.3× the 凶 rate. Exact replication of synthesis at cell level.

比和 cells (torus diagonal) carry the highest 凶 rates because 比和 is enriched in fixed-point basins (57.1% vs 50% baseline). The core bridge manifests on the torus through basin composition, not through cell position.

### Shell bridge at torus level

**Status: confirmed.** Fisher p=0.033, OR=1.82. Full relation test χ²=13.55, p=0.009.

| Relation | N爻 | 吉 rate |
|----------|:---:|:------:|
| 生体 | 72 | 41.7% |
| 体克用 | 78 | 37.2% |
| 体生用 | 72 | 34.7% |
| 比和 | 84 | 22.6% |
| 克体 | 78 | 19.2% |

生体 highest, 克体 lowest. Uses per-hexagram surface relation (fixed), not per-爻 體/用 (動爻-dependent). Synthesis found 44.4% for 生体 using the per-爻 method — same signal, slightly different magnitude.

### Spatial residual: NULL

**Status: proven.** χ²=19.0, p=0.75 (df=24). Cell position adds zero information beyond basin and surface relation. The two bridges fully explain the spatial valence pattern on Z₅×Z₅.

### Resolution of open question §4

**Valence is a function of the Z₅ quotient (directed relation), not Z₅×Z₅ position.** The 25 cells collapse to 5 relation types; no cell-level information survives beyond the relation. The torus carries valence only through its diagonal quotient. The bridges do not have independent spatial structure on Z₅×Z₅.

Data: `valence_torus.json`.

---

## Iteration 5: z5z5_cells.json Integration (Block 1 Complete)

**Status: complete.** All Block 1 results consolidated into z5z5_cells.json.

Per-cell (25 cells): hex names, basin distribution, valence rates (8 markers), 變 neighborhood (reachable/universal/partial), 互 targets + well_defined flag, complement cell mapping.

Global: reverse indices by basin (16:32:16), palace (8×8), relation (14:13:13:12:12); 六親 collisions (5 pairs); 五行 equivalent pairs (6 non-singleton, all bit-5 flips); complement anti-automorphism; valence test summaries (core bridge p=0.0002, shell bridge p=0.033, spatial residual p=0.75).

Verification: all 64 hexagrams present, each in exactly one cell, population sums correct, all reverse indices partition the full set.

---

## Iteration 6: Temporal Overlay on Z₅×Z₅ (III.A–B)

### Seasonal window — the diagonal sweep

**Status: proven.** Each season activates 2 consecutive elements on the 生 cycle, producing a 2×2 active block on Z₅×Z₅. Cell counts are perfectly invariant: 4 active, 12 partial, 9 dark per season.

The active block sweeps diagonally across the torus as seasons rotate: Spring (Wood,Fire) → Summer (Fire,Earth) → Late_Summer (Earth,Metal) → Autumn (Metal,Water) → Winter (Water,Wood). The wraparound at the boundary (Winter's active block spans opposite corners) is irreducibly toroidal — this is where torus geometry is essential.

### 日辰 extension — quadratic amplification

**Status: proven.** 60 (season × day-branch) states. Active element counts: 2 (20%), 3 (40%), 4 (40%).

**Active cells = n² exactly**, where n = number of active elements. Cell (a,b) is active iff both a,b ∈ active set — the torus's product structure provides quadratic amplification:

| Active elements | Active cells | Fraction of torus |
|:-:|:-:|:-:|
| 2 | 4 | 16% |
| 3 | 9 | 36% |
| 4 | 16 | 64% |

Ceiling confirmed: maximum 4 elements, never 5.

### Excluded element at max coverage

**Verified: always 休 or 死.** Distribution across 24 max-coverage states: Water 6, Fire 6, Earth 4, Metal 4, Wood 4. The Water/Fire asymmetry (6 vs 4) reflects the non-uniform branch-element distribution: Earth governs 4/12 branches (most of any element), causing Late_Summer to have fewer expansion opportunities (8/12 vs 10/12 for other seasons). Not a structural anomaly — a distributional artifact of the branch system.

### Fire/Water simultaneous access

16/60 states (26.7%) have both Fire and Water active. These are the temporal contexts where the Cycle basin's 2-cycle attractor (既濟↔未濟) has both elements accessible, partially resolving the "permanent internal conflict."

### The 1/5 residual stripe

At maximum coverage (4/5 elements active), the excluded element's row and column on Z₅×Z₅ form a cross-shaped shadow: 5 + 5 − 1 = 9 cells affected (dark or partial). This is the 1/5 minimal aperture theorem made geometric on the torus — one element always dark, its shadow rotating with the day.

### Torus coverage statistics

| | Active | Partial | Dark |
|---|:---:|:---:|:---:|
| Seasonal baseline | 16% | 48% | 36% |
| Maximum coverage | 64% | 32% | 4% |
| Mean (60 states) | 43% | 42% | 15% |

Data: `temporal_data.json`.

---

## Iterations 8+9: temporal.json + 梅花 Reachability + Presheaf (III.C–D)

### 梅花 reachability — abstract formula is near-uniform

**Status: proven.** 96 abstract input classes (8 S-values × 12 hours) → all 64 hexagrams reachable. Weight distribution perfectly bimodal: 32 at weight 1, 32 at weight 2. χ²=10.7 (df=63, p≈1.0) — under-dispersed, more uniform than chance.

**Two different objects:**
- **Formula distribution** over Z₂⁶: near-perfect equipartition (χ²=10.7). The modular arithmetic is structurally equitable.
- **Calendar distribution** conditioned on specific year/month/day: heavily biased (synthesis χ²=481.8). Upper trigram is fixed for a given day, constraining to 12 hexagrams.

The non-uniformity in practice comes from the temporal context (date constraining S mod 8), not from the formula's structure. Per-cell on the torus: paired-element cells tend toward weight 2, singleton cells toward weight 1 — the {2,2,2,1,1} partition creating variable input-path density.

### Presheaf properties verified from atlas

All four presheaf properties confirmed by direct computation on atlas.json:
1. **F_total = 12** for all 64 hexagrams (6 lines × 2 active seasons each)
2. **n_zero ∈ {15, 17, 19}** with 16:32:16 distribution; formula: n_zero = 15 + 2·n_missing_types
3. **Orthogonality wall** at 納甲 level: shell ⊥ core confirmed
4. **Ceiling**: 2/5 seasonal → 4/5 with 日辰; excluded always 休 or 死; 梅花 inherits 2/5

### temporal.json delivered

93KB reference document. 7 top-level keys: seasons (5), day_branches (12), states (60 with full cell-status maps), summary, meihua (per-hex weights + per-cell aggregates), presheaf (4 verified properties), season_expansion (per-season rates: 83% except Late_Summer at 67%).

Block 2 complete.

---

## Iterations 10–12: Semantic Screens + Tradition Table (IV.B–D)

### Thematic screen by surface relation (IV.B)

**Status: semantically null.** Permutation p<0.0001, KW H=20.24, p=0.0004. Within−between similarity gap = 0.003 (0.62% of baseline 0.545). With 384 vectors and ~73k pairwise comparisons, trivial structure is detectable at high power. Surface relation explains <1% of embedding variance.

克体 lines cluster highest (0.562), 体克用 lowest (0.537). The 2.5pp spread is likely driven by trigram-pair identity (specific element combinations sharing vocabulary contexts), not thematic content about adversity or conquest.

**Verdict: surface relation does not meaningfully predict what 爻辭 texts say.**

### 納音 semantic probe (IV.C)

**Status: null at name level — element artefact.** KW H=57.67, p<0.0001 at 納音 name level, but entirely explained by element grouping (KW at element level: H=33.08, p<0.0001). Earth-element 納音 names cluster together (0.556–0.567). Adding 納音 name beyond element assignment adds zero semantic information.

劍鋒金 does not predict sharp imagery. 海中金 does not predict water imagery. The finest-grained 五行 coordinate carries no semantic weight.

**Verdict: null.** Confirms synthesis finding that deeper algebraic constructs are null for semantic content.

### Tradition interpolation table (IV.D)

| Relation | Tradition claims | 吉% | 凶% | Verdict |
|----------|-----------------|:---:|:---:|---------|
| 比和 | 百事順遂 (all auspicious) | 22.6 | **20.2** | **Contradicted** — highest 凶 |
| 生体 | 進益之喜 (gains/joy) | **41.7** | 8.3 | **Confirmed** — OR≈2.1 |
| 体生用 | 耗失之患 (loss/depletion) | 34.7 | 6.9 | **Partial** — lower 吉 than 生体 |
| 克体 | 諸事凶 (inauspicious) | 19.2 | 16.7 | **Weak** |
| 体克用 | 諸事吉 (auspicious) | 37.2 | 14.1 | **Contradicted** |

Sources: 梅花易數 vol2:24 (體用生克 section).

### The directional principle

**Texts encode flow direction; tradition encodes relation category.** The distortion is systematic: symmetrization erases the inward/outward distinction that carries the actual signal.

The single principle: **receiving > giving** (inward flow → 吉):
- 生体 (41.7%) > 体生用 (34.7%) — being nourished > nourishing outward
- 体克用 (37.2%) > 克体 (19.2%) — conquering > being conquered

The 18pp gap between 体克用 and 克体 is the largest directional asymmetry. This is one finding (inward flow favors 吉) appearing in both 生 and 克 channels.

### The 比和 contradiction

比和 = same element = torus diagonal = enriched in fixed-point basins = core bridge's 凶 signal. Tradition reads 比和 as "harmony" (state). Texts encode convergence (process) — which correlates with danger, not safety. The process/state confusion is maximally visible at 比和.

Block 3 complete.

---
