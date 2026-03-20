# Atlas — Complete 五行 Map of Hexagram Space: Final Findings

> **Bit convention A:** b₀ = L1 (bottom), b₅ = L6 (top). Trigrams: b₀ = bottom line, b₂ = top line.

## Data Files

| File | Contents |
|------|----------|
| `atlas.json` | 64 entries × 33 fields — complete per-hexagram 五行 profile |
| `z5z5_cells.json` | 25 cells + reverse indices + 變 neighborhoods + 互 graph + valence + complement |
| `transitions.json` | 384 entries × 31 fields — 變 fan with full coordinate tracking |
| `temporal.json` | 60 temporal states + 梅花 reachability + presheaf properties |
| `constraints.json` | 13×13 MI matrix + DAG + forbidden combinations |

Supporting computation artifacts: `cross_network_results.json`, `torus_graphs.json`, `valence_torus.json`, `bian_hu_cross.json`, `semantic_screens.json`.

All files verified. Cross-references internally consistent. Population sums to 64. All reverse indices partition the full hexagram set.

---

## I. The Static Map

### A. Per-hexagram coordinates (atlas.json)

Each hexagram carries a unique 五行 profile across 13 coordinate axes organized in three independent chains:

**Shell chain** (from trigram pair, bits 0–2 and 3–5):
- Surface cell: (lower_element, upper_element) ∈ Z₅ × Z₅ — 25 values, H=4.50 bits
- Surface relation: 比和/生体/体生用/克体/体克用 — H=2.32 bits

**Core chain** (from inner bits 1–4):
- Inner value: 4-bit integer — H=4.00 bits
- 互 cell: (hu_lower_element, hu_upper_element) — 12 realized values, H=3.50 bits
- 互 relation: 5 values — H=2.05 bits
- 互 attractor: {坤, 乾, 既濟, 未濟} — H=2.00 bits
- Basin: Kun/Qian/Cycle — H=1.50 bits
- Depth: 0/1/2 — H=1.01 bits
- I-component: b₂⊕b₃ — H=1.00 bits

**Palace chain** (from palace walk construction):
- Palace: 8 values — H=3.00 bits
- Rank: 0–7 — H=3.00 bits
- Palace element: 5 values — H=2.25 bits
- 六親 word: 6-tuple of relation types — 59 unique values, H=5.84 bits

Additional coordinates: 納甲 branches (6 lines), 納音 (6 lines × element + name), S₄ partners (complement, reverse, rev∘comp).

### B. The zero residual

**Status: proven.**

H(hexagram | full 五行 profile) = 0.0 bits. The 13 coordinates jointly identify every hexagram uniquely. Combined with zero free parameters: the encoding is complete in both directions and uniquely determined. The Chinese coordinate system is informationally equivalent to Z₂⁶.

### C. The bit-5 residual

**Status: proven.**

The full 五行 profile (surface_cell, hu_cell, basin, palace_element) yields 58 classes: 52 singletons + 6 size-2 pairs. All 6 non-singleton pairs differ by exactly bit 5 (XOR = 32), the upper trigram MSB. This is the exact residual bit the 五行 projection discards — it distinguishes paired trigrams within the same element (e.g., Kun↔Gen, both Earth).

Without 六親 (which recovers this bit through 納甲 branch sensitivity), the 五行 system is a 5-bit coordinate on a 6-bit space. 六親 word captures 5.84 bits (97.4%); adding any disambiguator (surface_cell, inner_val, basin) reaches 6.00 bits.

### D. Two orthogonal degeneracy classes

**Status: proven.**

The 五行-profile degeneracy (6 pairs, all bit-5 flips) and the 六親 degeneracy (5 collision pairs, all surface-distinguished) are non-overlapping. One lives in the shell projection's residual, the other in the palace projection's residual. The three-chain independence from the dependency DAG made visible as two orthogonal degeneracy classes.

六親 collisions (5 pairs): 復/泰, 臨/中孚, 謙/履, 升/巽, 頤/小畜. Every collision pair is distinguished by surface_cell — the shell projection disambiguates what the palace projection conflates.

### E. Dependency DAG — three cascading chains

**Status: proven.**

```
inner_val (4.0) → hu_cell (3.5) → { basin (1.5) → i_component (1.0) }
                                 → { hu_relation (2.0) }
                                 → { hu_attractor (2.0) → basin }
surface_cell (4.5) → surface_relation (2.3)
palace (3.0) → palace_element (2.25)
```

Each arrow: source fully determines target. Each step: lossy compression. The three chains (core, shell, palace) are the three projections of Z₂⁶ that jointly span it.

### F. Minimal identifying pairs

Five minimal coordinate pairs uniquely identify all 64 hexagrams:
1. palace + rank (the traditional 八宮 system)
2. inner_val + rank
3. hu_cell + rank
4. surface_cell + liuqin_word
5. inner_val + liuqin_word

surface_cell + inner_val is NOT sufficient: 16 collisions from bit 5.

### G. The Z₅×Z₅ torus

Z₅×Z₅ is the quotient of Z₂⁶ under the 五行 element map applied independently to each trigram. Population structure entirely forced by the {2,2,2,1,1} partition:

| Cell type | Count | Population per cell |
|-----------|:-----:|:---:|
| Paired × Paired | 9 | 4 |
| Paired × Singleton | 12 | 2 |
| Singleton × Singleton | 4 | 1 |

Population of cell (a,b) = |a| × |b|. The surface relation distribution (比和=14, 生体=12, 体生用=12, 克体=13, 体克用=13) matches the partition prediction exactly.

### H. Joint constraints and information content

**Status: proven.**

Orthogonality is scale-dependent: basin ⊥ rank is exact (MI=0.000, forced by palace mask sequence), but inner_val × surface_cell share 3.000 bits (through boundary bits 1–4). The orthogonality wall holds at coarse resolution, breaks at fine resolution.

Forbidden combinations:
- hu_relation × basin: 7/15 forbidden (比和 only in FP basins, 生 only in Cycle)
- surface_relation × hu_relation: 6/25 forbidden (surface 克 excludes nuclear 生)
- surface_cell × hu_cell: 252/300 forbidden (shared boundary bits create massive constraint)

---

## II. Transformations

### A. 互 algebra on Z₅×Z₅

**Status: proven.**

互 is NOT well-defined on Z₅×Z₅. 17/25 cells set-valued, 8/25 well-defined.

**Corrected well-definedness criterion:** lower ∈ {Fire, Water} AND upper ∉ {Wood}.

Mechanism: 互 reads bits (b₁,b₂,b₃,b₄). Lower trigram contributes (b₁,b₂) — only singletons fix these. Upper contributes (b₃,b₄) — all elements except Wood have trigrams agreeing on these bits. Wood's trigrams (巽=001, 震=110) give distinct (b₃,b₄).

**互 chains terminate at torus level after 1 step.** Even starting from well-defined cells, one 互 step lands in a set-valued cell. The torus is definitively the wrong level for 互 iteration.

**互 graph on torus (z5z5_cells.json):** Per-cell: set of hu target cells, well_defined flag, reachable attractors. Multi-attractor reachability: 12 cells reach 2, 3 cells reach 3, 1 cell (Wood,Wood) reaches all 4.

### B. 變 geometry — the 4-layer perturbation onion

**Status: proven (upgrades phase 1's 3-layer model).**

The 互 coordinate breaks the shell layer's internal symmetry, revealing 4 concentric layers:

| Layer | Lines | Bit | Surface | 互 cell | Basin | Mechanism |
|-------|-------|-----|:-------:|:-------:|:-----:|-----------|
| Outer | L1,L6 | b₀,b₅ | changes | 100% preserved | 100% | Invisible to 互 |
| Shell-outer | L5 | b₄ | changes | 50% preserved | 100% | MSB of hu_upper; Earth/Metal preserve |
| Shell-inner | L2 | b₁ | changes | 0% preserved | 100% | LSB of hu_lower; always changes element |
| Interface | L3,L4 | b₂,b₃ | changes | 0% preserved | 0% | In both hu trigrams — total destruction |

**L2/L5 asymmetry mechanism (proven at bit level):**
- L2 (b₁) = LSB of hu_lower. Every LSB-adjacent trigram pair crosses elements. 0/4 preserve → 0%.
- L5 (b₄) = MSB of hu_upper. MSB-adjacent pairs: Kun↔Gen (Earth=Earth), Dui↔Qian (Metal=Metal), but Zhen↔Li and Kan↔Xun cross. 2/4 preserve → 50%.

The preserving pairs are exactly the parity-0 coset {Earth, Metal}.

**Attractor stability:** P(attractor changes | hu_cell changes) = 100% at interface, 25% at shell. Three-quarters of shell-layer 互 disruptions stay in-basin.

**Bridge orthogonality at perturbation level (proven):** 體/用 distribution identical between boundary states (flip b₂/b₃) and non-boundary states. The two bridges do not interact through the 變 fan.

### C. 變 neighborhood on Z₅×Z₅

**Status: proven.** Four structural classes, determined by element partition type:

| Class | Cells | Reachable | Universal | Pattern |
|-------|:-----:|:---------:|:---------:|---------|
| Singleton×Singleton | 4 | 6 | 6 | Fully deterministic |
| Mixed | 12 | 7 | 5 | Moderate variation |
| Paired×Paired (no Wood) | 4 | 7 | 3 | Most within-cell variation |
| Wood-containing | 5 | 8 | 4 | Largest neighborhoods |

Per-cell reachable sets stored in z5z5_cells.json (union, intersection, and partial).

### D. Palace walk trajectories

**Three Z₅ equivalence classes:** {Qian,Kun,Dui,Gen} (Earth+Metal), {Kan,Li} (singletons), {Xun,Zhen} (Wood).

**Two abstract basin patterns:**
- FP-rooted `[FP,FP,FP,C,FP,FP,C,FP]`: palaces {Qian, Kun, Kan, Li}
- Cycle-rooted `[C,C,C,FP,C,C,FP,C]`: palaces {Dui, Gen, Xun, Zhen}

Basin flips at ranks 3 and 6 where palace mask has b₂⊕b₃=1. The 游魂/歸魂 names track the return journey.

### E. S₄ involutions on Z₅×Z₅

**Complement: clean.** π = (Earth↔Metal)(Fire↔Water)(Wood fixed). Verified for all 32 pairs. Anti-automorphism that reverses the 生 cycle direction.

**Reversal: not a Z₅ operation.** Of 28 non-palindromic pairs, exactly 6 exhibit coordinate swap (a,b)→(b,a). The 6 swapping pairs are exactly those where both trigrams are either both singletons or from the same paired-element class. The {2,2,2,1,1} partition shape acts as a selection rule on which reversals the torus can see.

### F. Cross-hexagram network

**五行-equivalent classes:** Full profile → 58 classes (52 singletons + 6 pairs, all bit-5 flips). Coarse (surface+basin) → 45 classes.

**六親 collisions:** 59 unique words, 5 collision pairs. All distinguished by surface_cell.

**Surface relation transition matrix (384 flips):**

|  | 比和 | 生体 | 体生用 | 克体 | 体克用 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **比和** | 16 | 12 | 12 | 22 | 22 |
| **生体** | 12 | 12 | 16 | 14 | 18 |
| **体生用** | 12 | 16 | 12 | 18 | 14 |
| **克体** | 22 | 14 | 18 | 12 | 12 |
| **体克用** | 22 | 18 | 14 | 12 | 12 |

Symmetric under complement anti-automorphism.

### G. 變×互 cross-transformation

**Status: proven.** Outer bit flips are invisible to 互 (100% hu_cell preserved — proven by construction). Interface flips maximally disrupt 互 (0% preserved, 100% attractor change). Shell flips partially disrupt (L2: 0%, L5: 50%).

The outer attractor "anomaly" (93.8%) is a labeling artifact of the 2-cycle: since hu_cell is 100% preserved, the entire 互 chain is identical → attractor-as-set is 100% preserved.

---

## III. Temporal Overlay

### A. Seasonal window — the diagonal sweep

**Status: proven.** Each season activates 2 consecutive elements on the 生 cycle → 2×2 active block on Z₅×Z₅. Perfectly invariant: 4 active, 12 partial, 9 dark per season.

The active block sweeps diagonally across the torus: Spring (Wood,Fire) → Summer (Fire,Earth) → Late_Summer (Earth,Metal) → Autumn (Metal,Water) → Winter (Water,Wood). The wraparound at Winter is irreducibly toroidal — the one place where torus topology is essential.

### B. 日辰 extension — quadratic amplification

**Status: proven.** 60 (season × day-branch) states. Active element counts: 2 (20%), 3 (40%), 4 (40%).

**Active cells = n² exactly**, where n = active elements. Cell (a,b) is active iff both a,b ∈ active set. The torus's product structure provides quadratic amplification:

| Active elements | Active cells | Torus fraction |
|:-:|:-:|:-:|
| 2 | 4 | 16% |
| 3 | 9 | 36% |
| 4 | 16 | 64% |

**Ceiling confirmed:** maximum 4 elements, never 5. Excluded element always 休 or 死. Distribution: Water 6, Fire 6, Earth 4, Metal 4, Wood 4. The Water/Fire asymmetry reflects the non-uniform branch-element distribution (Earth governs 4/12 branches).

**Fire/Water simultaneous access:** 16/60 states (26.7%). These are the temporal contexts where the Cycle basin's 2-cycle attractor has both elements accessible.

**The 1/5 residual stripe:** At max coverage (4/5 elements active), the excluded element's row and column form a cross-shaped shadow: 9 cells dark or partial. The 1/5 minimal aperture theorem made geometric on the torus.

### C. Presheaf on Z₅

**Status: verified from atlas coordinates.** All four properties confirmed:
1. **F_total = 12** for all 64 hexagrams (6 lines × 2 active seasons each)
2. **n_zero ∈ {15, 17, 19}** with 16:32:16 distribution; formula: n_zero = 15 + 2·n_missing_types
3. **Orthogonality wall** at 納甲 level: shell ⊥ core confirmed
4. **Ceiling**: 2/5 seasonal → 4/5 with 日辰; excluded always 休 or 死

**Shell/core asymmetry is structural:** The core has no temporal overlay because the orthogonality wall prevents temporal modulation from reaching it. The core is time-independent (skeleton); the shell is time-modulated (skin). The atlas reflects this by having temporal data only for shell coordinates.

### D. 梅花 temporal input

**Status: proven — two different objects.**

**Formula distribution** over Z₂⁶: 96 abstract input classes (8 S-values × 12 hours) → all 64 hexagrams reachable. Weight distribution bimodal: 32 at weight 1, 32 at weight 2. χ²=10.7 (df=63, p≈1.0) — under-dispersed, more uniform than chance. The modular arithmetic is structurally equitable.

**Calendar distribution** conditioned on specific year/month/day: heavily biased (synthesis χ²=481.8). Upper trigram fixed for a given day, constraining to 12 hexagrams.

The non-uniformity in practice comes from the temporal context (date constraining S mod 8), not from the formula's structure. Per-cell on torus: paired-element cells → weight 2, singleton cells → weight 1 — the {2,2,2,1,1} partition creating variable input-path density.

**Pipeline asymmetry:** 梅花 curves domain (which hexagram generated), 火珠林 curves codomain (which aspects visible). 梅花 inherits 2/5 ceiling (no 日辰 mechanism).

### E. Torus coverage statistics

| | Active | Partial | Dark |
|---|:---:|:---:|:---:|
| Seasonal baseline | 16% | 48% | 36% |
| Maximum coverage | 64% | 32% | 4% |
| Mean (60 states) | 43% | 42% | 15% |

Data: pre-computed in `temporal.json` — 60 states queryable without re-running computations.

---

## IV. The Semantic Layer

### A. Valence bridges — confirmed at torus level

**Core bridge (凶×basin):** χ²=17.44, p=0.0002. Kun 20.8%, Qian 20.8%, Cycle 6.2%. Fixed-point basins carry 3.3× the 凶 rate. Exact replication of synthesis at cell level.

**Shell bridge (吉×生体):** Fisher p=0.033, OR=1.82. Full relation test χ²=13.55, p=0.009.

| Relation | N爻 | 吉 rate |
|----------|:---:|:------:|
| 生体 | 72 | 41.7% |
| 体克用 | 78 | 37.2% |
| 体生用 | 72 | 34.7% |
| 比和 | 84 | 22.6% |
| 克体 | 78 | 19.2% |

### B. Spatial residual: NULL

**Status: proven.** χ²=19.0, p=0.75 (df=24). Cell position adds zero information beyond basin and surface relation. **Valence is a function of the Z₅ quotient (directed relation), not Z₅×Z₅ position.** The 25 cells collapse to 5 relation types; no cell-level information survives beyond the relation. The torus carries valence only through its diagonal quotient.

### C. Thematic screen by surface relation (IV.B)

**Status: semantically null.** KW H=20.24, p=0.0004, but within−between similarity gap = 0.003 (0.62% of baseline). Surface relation explains <1% of embedding variance. The statistical significance reflects high power (~73k comparisons), not meaningful structure.

**Verdict: surface relation does not predict what 爻辭 texts say.**

### D. 納音 semantic probe (IV.C)

**Status: null at name level — element artefact.** KW H=57.67, p<0.0001 at 納音 name level, entirely explained by element grouping (KW at element level: H=33.08, p<0.0001). 劍鋒金 does not predict sharp imagery. 海中金 does not predict water imagery. The finest-grained 五行 coordinate carries no semantic weight beyond its element.

### E. Tradition interpolation table (IV.D)

| Relation | Tradition claims | 吉% | 凶% | Verdict |
|----------|-----------------|:---:|:---:|---------|
| 比和 | 百事順遂 (all auspicious) | 22.6 | **20.2** | **Contradicted** — highest 凶 |
| 生体 | 進益之喜 (gains/joy) | **41.7** | 8.3 | **Confirmed** — OR≈2.1 |
| 体生用 | 耗失之患 (loss/depletion) | 34.7 | 6.9 | **Partial** — lower 吉 than 生体 |
| 克体 | 諸事凶 (inauspicious) | 19.2 | 16.7 | **Weak** |
| 体克用 | 諸事吉 (auspicious) | 37.2 | 14.1 | **Contradicted** |

### F. The directional principle

**Texts encode flow direction; tradition encodes relation category.** The distortion is systematic: symmetrization erases the inward/outward distinction that carries the actual signal.

Single principle — **receiving > giving** (inward flow → 吉):
- 生体 (41.7%) > 体生用 (34.7%) — being nourished > nourishing outward
- 体克用 (37.2%) > 克体 (19.2%) — conquering > being conquered

The 18pp gap between 体克用 and 克体 is the largest directional asymmetry. One finding (inward flow favors 吉) appearing in both 生 and 克 channels.

### G. The 比和 contradiction

比和 = same element = torus diagonal = enriched in fixed-point basins = core bridge's 凶 signal. Tradition reads 比和 as "harmony" (state). Texts encode convergence (process) — which correlates with danger, not safety. The process/state confusion is maximally visible at 比和.

---

## V. The Torus — What the Geometry Reveals

### The {2,2,2,1,1} partition as single organizing principle

**Status: proven.** Every structural finding traces back to how 8 trigrams partition into 5 elements with sizes {2,2,2,1,1}. The partition determines:

- **Wood's maximal indeterminacy:** Hamming distance 3 between Wood's trigrams (巽=001, 震=110) — the maximum possible, sharing no bits. Appears as: complement fixed point, widest 變 neighborhood (8 targets), most 互 attractors reachable (all 4 at Wood,Wood cell). Not three findings — one finding appearing three times.
- **The 4-layer onion:** L2/L5 asymmetry via LSB/MSB position in 互 trigrams. Parity-0 elements (Earth, Metal) preserve under MSB flip; no element preserves under LSB flip.
- **Reversal selection rule:** 6/28 non-palindromic pairs swap on torus = partition shape filter.
- **互 well-definedness:** Lower singleton + upper non-Wood = the asymmetric bit-reading of 互.
- **梅花 weight bimodality:** Paired elements → weight 2, singletons → weight 1.
- **The bit-5 residual:** The gap between 五行 and Z₂⁶ is exactly the partition's degeneracy.
- **Population gradient:** 4:2:1 = product of element class sizes.

The atlas is, in a precise sense, a consequence of assigning 8 objects to 5 categories in this specific way. Whether this assignment is arbitrary or necessary is a question the atlas can frame but not answer — it would require showing the 五行 assignment is the unique partition satisfying some natural criterion.

### What the torus earns

The torus earns its geometry in exactly one place: **the temporal overlay.**

The seasonal diagonal sweep with wraparound is irreducibly toroidal. The n² amplification (2 active elements → 4 cells, 4 → 16) is the product structure doing work. The 1/5 residual stripe is the ceiling theorem made geometric. This is where torus topology is essential — not for the static map, not for valence, not for transformations.

### What the torus does not earn

- **Valence:** Lives on the Z₅ diagonal quotient, not Z₅×Z₅. Spatial residual p=0.75.
- **互 iteration:** Set-valued on the torus after 1 step. Wrong level.
- **Reversal:** Not a Z₅ operation. Only 6/28 swap.
- **Semantic content:** <1% of embedding variance explained by cell position.

### The epistemology/ontology distinction

The torus encodes **when you can see what** (epistemology — the seasonal access pattern). It does not encode **what things mean** (ontology — that lives on the Z₅ quotient). The frame is geometric; the content is algebraic. The frame is two-dimensional; the picture is one-dimensional.

---

## Epistemic Status

| Category | Claims |
|----------|--------|
| **Proven** (algebraically necessary) | Zero residual (H=0.0); dependency DAG (12 edges); 5 minimal identifying pairs; 4-layer perturbation onion with L2/L5 asymmetry; bridge orthogonality at perturbation level; 體/用 uniformity; 互 not well-defined on Z₅×Z₅ (exact criterion: lower singleton + upper non-Wood); complement anti-automorphism; reversal not Z₅; 6/28 selection rule; bit-5 residual; 4-class 變 neighborhood; forbidden constraints (7/15, 6/25, 252/300); basin ⊥ rank; seasonal invariance (4-12-9); n² amplification; ceiling (4/5); F_total=12 |
| **Measured** (empirically confirmed) | Core bridge χ²=17.44, p=0.0002; shell bridge Fisher p=0.033, OR=1.82; spatial residual p=0.75; thematic screen <1% variance; 納音 null beyond element; 梅花 formula χ²=10.7; Fire/Water access 16/60; tradition table verdicts |
| **Derived** (follows from partition shape) | Population gradient 4:2:1; Wood maximal indeterminacy; 梅花 weight bimodality; L5 MSB preservation rate; torus coverage statistics |
| **Conjectured** (open) | Whether the {2,2,2,1,1} partition is the unique/optimal assignment under some natural criterion |

---

## What the Atlas Does NOT Contain (Known Gaps)

1. **Formal H¹ computation.** Qualitative picture clear; numerical refinement lower priority. Basin ⊥ rank (MI=0.000) limits degrees of freedom for curvature variation.
2. **Curvature optimization criterion.** No natural measure of "discriminative power" identified. The question is not well-posed without conceptual development.
3. **納甲 modification history.** When the 京氏 universal offset was replaced by the 火珠林 乾/坤-only rule. Historical-philological question requiring 唐–宋 dynasty intermediate texts.
4. **Visualizations.** The torus, heatmaps, flow diagrams — sketched in PLAN.md §V.Outputs, not computed. Data is ready; rendering is deferred.
5. **Temporal × semantic interaction.** Whether valence rates vary by season (does 凶×basin signal change when the basin's element is 旺 vs 死?). Requires temporal.json × valence_torus.json cross-analysis.

---

## The Torus Belongs to Neither System

The atlas `surface_cell` = (upper_element, lower_element) is the natural algebraic projection of the hexagram's trigram pair onto Z₅×Z₅. It determines forbidden combinations, population gradients, seasonal access windows. It is algebraically real. But neither divination system reads it directly.

**火珠林** decomposes *below* the torus. It reads each of 6 lines individually: stem-branch → element → compare against palace element → 六親 type. Six parallel Z₅ comparisons against a fixed reference. The trigram pair is never composed into a 2D coordinate. The torus cell exists in the hexagram's algebra but is invisible to 納甲 practice.

**梅花** reinterprets the torus axes. The two dimensions aren't upper/lower (positional) but 體/用 (relational) — which trigram is self, which is other. Assignment depends on the 動爻 position, so the same hexagram occupies two different cells depending on which line moves. 梅花 reads a *rotated* torus where the axes carry directional meaning (who acts on whom).

The atlas torus is the algebraic ground truth from which both systems project differently. It is the territory; neither system's map matches it exactly. `surface_cell` is a coordinate of the hexagram as a mathematical object — not a coordinate of any practitioner's reading.
