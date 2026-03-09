# 梅花 Atlas — The Interpretive Circuit in 五行 Coordinates

## What this is

The existing atlas maps hexagram space as a static algebraic object: 64 hexagrams, each with a fixed 五行 profile. That atlas belongs to neither divination system — it's the algebraic ground truth both project from.

This atlas maps **梅花's operational space**: the 384 reading states (64 hexagrams × 6 動爻), each with a directed 體/用 evaluation across the 本→互→變 circuit. The unit of analysis is not the hexagram but the **reading** — a hexagram with a designated moving line.

## What 梅花 actually reads

A 梅花 reading is a sequence of directed Z₅ relations, evaluated from 體's perspective:

```
本卦: 體 vs 用     → relation₁ ∈ {比和, 生体, 体生用, 克体, 体克用}
互卦: 體 vs 互上/互下 → relation₂, relation₃ (amplify or dampen)
變卦: 體 vs 變用    → relation₄ (resolution)
```

體 is the trigram *without* the 動爻. Its element is the reference frame — fixed throughout the reading. Everything else (用, both 互 trigrams, the 變 trigram) is evaluated against it. **体一用百**: one self, many others.

The output is a 4-element relation vector, read as a narrative arc: present situation → mediating forces → outcome.

## The state space

**384 states = 64 hexagrams × 6 動爻 positions.**

Each state determines:
- Which trigram is 體 (the one without the moving line)
- Which trigram is 用 (contains the moving line)
- The 變卦 (flip the moving line → new hexagram)
- The 互卦 (lines 2-5 extracted as two trigrams — same for all 6 動爻 of the same hexagram, **except 乾 and 坤**)

**乾坤无互 exception:** Pure 乾 (hex 63) and pure 坤 (hex 0) have self-referential 互 (乾→乾, 坤→坤). Vol 1: "乾坤无互，互其变卦" — for these two hexagrams, 互 is replaced by the 互 of the 變卦. Since 變 depends on which line moves, this means 乾 and 坤 have **動爻-dependent 互**, unlike all other hexagrams. 12 of 384 states affected.

Since 動爻 in the upper vs lower trigram swaps 體/用, each hexagram produces exactly **2 distinct 體/用 assignments** (lines 1-3 → one assignment, lines 4-6 → the other). Within each assignment, the 3 possible 動爻 positions produce different 變卦 but the same 體/用 elements.

So: 384 states collapse to **128 evaluations** at the 本卦 level (64 × 2 polarities), but expand again at the 變卦 level (different moving lines → different outcomes). For 乾/坤, the 互 layer also expands — these hexagrams have up to 6 distinct 互 evaluations rather than 1.

## Dependencies

All hexagram-level data exists in `atlas/atlas.json` and `atlas/transitions.json`:
- Trigram elements, 互 chains, 變 fan, basin, depth, attractor
- Surface/hu cell coordinates

The 梅花 atlas adds the 體/用 interpretive layer on top. No new hexagram-level computation needed.

Source texts: `texts/meihuajingshu/vol1.txt` through `vol3.txt`, `opposition-theory/sy-divination.md`.

### Scope exclusion

**Vols 4-5 (character divination, 格物) are out of scope.** These volumes describe a different front end — stroke shapes → 五行/六神/星神 — feeding the same 生克 back end. The typing step is visual/phonological rather than arithmetic/perceptual. The back end (体/用 evaluation, 生克 engine, timing) is identical to vols 1-3. An atlas of character divination would extend the *input funnels* but not the *interpretive circuit*. Deferred unless the domain structure (§V) reveals that character divination uses different semantic bindings.

---

## I. The 384-State Table

### Per-state coordinates

For each (hexagram, 動爻) pair:

| Coordinate | Source | Description |
|---|---|---|
| `ti_element` | trigram without 動爻 | 體 element ∈ Z₅ |
| `yong_element` | trigram with 動爻 | 用 element ∈ Z₅ |
| `ben_relation` | (用 - 體) mod 5 | 本卦 directed relation |
| `hu_upper_element` | from atlas (or 變's 互 for 乾/坤) | 互上 element |
| `hu_lower_element` | from atlas (or 變's 互 for 乾/坤) | 互下 element |
| `ti_hu_element` | 互 trigram on 體's side | 体互 element (weighted higher) |
| `yong_hu_element` | 互 trigram on 用's side | 用互 element (weighted lower) |
| `hu_upper_relation` | (互上 - 體) mod 5 | 互上 vs 體 |
| `hu_lower_relation` | (互下 - 體) mod 5 | 互下 vs 體 |
| `bian_hex` | flip 動爻 | 變卦 identity |
| `bian_yong_element` | 變卦's 用-side trigram | 變 trigram element |
| `bian_relation` | (變用 - 體) mod 5 | 變卦 directed relation |
| `relation_vector` | [ben, ti_hu, yong_hu, bian] | full 4-step arc (体互 weighted > 用互) |

### Derived coordinates

| Coordinate | Description |
|---|---|
| `ti_party_count` | count of trigrams sharing 體's element or generating it (體黨) |
| `yong_party_count` | count of trigrams that 克 體 or drain 體 (用黨) |
| `arc_valence` | net direction of the 4-step vector (improving / worsening / stable) |
| `ben_bian_shift` | how the 體/用 relation changes from 本 to 變 (the outcome delta) |

### Key questions for this section

1. **Distribution of relation vectors.** How many of the 5⁴ = 625 possible 4-step arcs are actually realized? Which are forbidden? (Note: 体互 and 用互 are asymmetrically weighted — the vector is ordered [ben, ti_hu, yong_hu, bian], not interchangeable at positions 2-3.)
2. **體黨/用黨 balance.** The tradition claims majority determines outcome. Does 體黨 > 用黨 correlate with favorable arc_valence?
3. **The 128→384 expansion.** At 本卦 level, only 128 distinct (體, 用) evaluations exist. The 變 layer splits each into up to 3. How much information does the specific 動爻 position add beyond the 體/用 polarity?

---

## II. The Torus Flow

### 梅花's torus vs the atlas torus

The atlas torus: axes = (upper_element, lower_element). Positional. Fixed per hexagram.

梅花's torus: axes = (體_element, 用_element). Relational. Depends on 動爻.

Same 25-cell Z₅×Z₅ surface. Different coordinate semantics. A hexagram at atlas cell (A, B) maps to 梅花 cell (A, B) or (B, A) depending on which trigram is 體. Axis transposition = the reverse involution restricted to element coordinates.

### The flow

Each 梅花 reading traces a directed tree on the torus:

```
本卦: (體, 用) cell
          ↓
互卦: (體, 体互) cell + (體, 用互) cell    [1→2 branch, 体互 weighted higher]
          ↓
變卦: (體, 變用) cell
```

體 stays fixed (same element throughout). The other axis changes at each step. So the trajectory is always **axis-parallel** — it moves along the 用-dimension while 體's row/column is constant. The reading is a 1D pattern embedded in the 2D torus.

The 互 step produces TWO torus cells (体互 and 用互), not one. The flow is 1→2→1: one 本 cell, two 互 cells (with asymmetric weighting), one 變 cell. Vol 3: "体互最紧，用互次之" — the 互 trigram on 體's side is primary, the one on 用's side is secondary.

### What to compute

1. **Project all 互 chains with 體/用 polarity** onto the torus. The 互 chain (from transitions.json) gives the hexagram-level trajectory. Projecting with 體 fixed gives the torus-level trajectory.
2. **Catalog directed edges** between torus cells. Each (hexagram, 動爻) → (互 hexagram, same 體) produces one edge.
3. **Identify clean vs turbulent cells.** Where 互 is well-defined on the torus (all hexagrams in the cell agree on next cell) vs multi-valued (17/25 atlas cells — does this count change with 體/用 polarity?).
4. **Convergence basins at torus level.** The 3 hexagram-level basins (Qian, Kun, Cycle) project to which torus cells? Does basin membership become visible at torus level when 體/用 polarity is applied?
5. **The 變 step.** Unlike 互, 變 depends on the specific 動爻 line. This is where the 384-state granularity matters — same 本 cell, same 互 trajectory, but 3 different 變 destinations.

---

## III. The Relation Arc

### The narrative structure

梅花 reads a temporal arc: 本 = now, 互 = development, 變 = outcome. Each step gives a Z₅ relation to 體. The sequence of relations IS the reading.

### Arc classification

Classify all 384 arcs by their shape:

| Arc type | Pattern | Meaning |
|---|---|---|
| Stable favorable | 生体 → 生体 → 生体 | uniformly good |
| Stable unfavorable | 克体 → 克体 → 克体 | uniformly bad |
| Improving | 克体 → 比和 → 生体 | bad → good |
| Deteriorating | 生体 → 比和 → 克体 | good → bad |
| Rescued | 克体 → 克体 → 生体 | bad throughout, saved at end |
| Betrayed | 生体 → 生体 → 克体 | good throughout, collapses at end |
| Mixed | various | no clear trend |

### What to compute

1. **Arc distribution.** Which arc types dominate? Are any forbidden by the algebra (e.g., does basin constrain which arcs are possible)?
2. **Arc × valence.** Cross-reference arc types with 卦辭/爻辭 吉/凶 markers. Do "improving" arcs correlate with 吉? Do "deteriorating" arcs correlate with 凶? This tests the tradition's temporal reading against the texts.
3. **互 as amplifier/dampener.** The tradition says 互 modulates the 本→變 arc. Test: does the 互 relation predict whether the 本→變 transition strengthens or reverses? Is 互 genuinely intermediate or structurally independent?
4. **The 比和 discrepancy.** 梅花 texts unanimously say 比和 = auspicious (vol 2: "体用比和，则百事顺遂"). The atlas found the opposite in 卦辭: 比和 diagonal has the highest 凶 rate (basin enrichment, p=0.0002). The two systems disagree. Test: does 比和's position in the arc matter? Is 比和 at 互 or 變 different from 比和 at 本? Does the arc context resolve the discrepancy?
5. **Structural override cases.** When does the arc give a clear signal but the hexagram's structural identity contradicts it? (The 西林寺 pattern — 比和 everywhere but the hexagram is 剝.) How frequent are these overrides?

---

## IV. Temporal Layer

### A. Casting funnels

**先天 (calendar-based):** upper = (year+month+day) mod 8, lower = (year+month+day+hour) mod 8, line = total mod 6. Maps calendar time → 384-state space. Distribution non-uniform (calendar χ²=481.8, abstract χ²=10.7).

**後天 (perception-based):** 9+ methods, all landing in the same Z₈×Z₈×Z₆ space but with different input distributions:

| Method | Upper | Lower | Line |
|---|---|---|---|
| Object count | count mod 8 | hour mod 8 | total mod 6 |
| Sound | sound-count mod 8 | hour mod 8 | total mod 6 |
| Words (even split) | first half mod 8 | second half mod 8 | total mod 6 |
| Words (odd split) | fewer chars mod 8 | more chars mod 8 | total mod 6 |
| Characters (1-3) | left strokes mod 8 | right strokes mod 8 | total mod 6 |
| Characters (4+) | tonal values mod 8 | tonal values mod 8 | total mod 6 |
| Measurement | zhang mod 8 | chi mod 8 | total mod 6 |
| Person/object | trigram-attribute | direction/context | total mod 6 |

The hour enters as grounding anchor in most methods. 後天 methods are hybrid: 2/3 coordinates from perception, 1/3 from arithmetic.

### B. 克應之期 (Timing output)

When the predicted event manifests. A core output of every reading, described in vol 3 as "卦之切要" (the most critical part).

**Mechanics:**
- Base timing = 全卦之数 (total number from the casting)
- Observer state scales the number: 行 (walking) = halve, 坐 (sitting) = double, 立 (standing) = as-is
- Unit depends on event type: days for ephemeral, months for medium, years for durable
- 生体 卦气 = timing of favorable events; 克体 卦气 = timing of unfavorable events

**先天 vs 後天 timing:**
- 先天: uses 卦气 (trigram-associated stems/branches) for timing precision
- 後天: uses total number + observer state

**Advanced timing (vol 5):** The 渾天甲子定局 provides a 60-entry lookup table for hour-level timing precision.

### C. What to compute

1. **先天 per-state reachability.** Which of the 384 states are reachable? Are any unreachable?
2. **後天 distributional analysis.** For each casting method, what's the theoretical distribution across 384 states? Which methods produce the most uniform coverage?
3. **Temporal clustering.** Which (體, 用) cells are overrepresented / underrepresented in the calendrical distribution?
4. **Seasonal bias on arc types.** When casting in spring (Wood 旺), are 木-體 states overrepresented? Does the casting mechanism bias toward arc types where 體 is seasonally strong?
5. **The 2/5 ceiling in 梅花.** 梅花 has no 日辰 mechanism. The seasonal ceiling stays at 2/5 (only 2 of 5 elements are 旺/相). How does this interact with the arc? When 體 is 休/囚/死, does the arc still give valid readings, or is this where 梅花's resolution degrades?
6. **Timing formula structure.** Is 克應之期 algebraically determined by the casting numbers, or does it require practitioner judgment (choosing the unit)? How much of the timing output is mechanical vs interpretive?

---

## V. Semantic Bindings

### The 18 application domains

Vol 2 lists 18 domains, each with specific 體/用 semantic bindings and per-trigram interpretations. This is the practitioner's lookup table — the bridge from abstract 生克 to concrete prediction.

### What to extract

1. **Domain → semantic binding table.** For each domain: what does 體 represent? What does 用 represent? What do the 8 trigram images map to in this domain?
2. **Cross-domain structure.** Do related domains share bindings? (e.g., wealth and trade both map 用 to money-related imagery.) Is there an internal taxonomy?
3. **Weather exception.** Weather reads all trigrams as a committee — no 體/用 split. This is the sole domain that operates differently. What drives the exception? (Answer likely: weather has no "self" — it's not a relationship but an environment.)
4. **Illness sub-systems.** Three sub-systems (spirit diagnosis, pharmacology, 乾坤 walkthrough) operate within the same domain. How do they relate?

### The 10 response channels (十応)

Ten categories of 用 input (本/互/變/日/刻/外/天時/地理/人事/方), each evaluated against 體. The hexagram provides 3 (本/互/變). The remaining 7 come from observation at the moment of casting.

### 三要灵应 — theoretical framework

The perceptual theory underlying the 7 observational channels. Three faculties — 耳 (ear), 目 (eye), 心 (heart-mind) — operating in 虚灵 (empty sensitivity). The ontological claim: "性理，具于人心者也" — the Yi's structure is intrinsic to the mind. The resonance principle: "我心忧者，彼事亦忧" — the observer's internal state at casting is signal, not noise.

This is not formalizable as algebra, but it's the framework that makes the 十應 coherent. The 7 observational channels are applications of 三要 — typed perception feeding the 生克 engine. Without 三要, the channels are an arbitrary list; with it, they're instances of a principle.

### What to formalize

1. **Channel → element mapping.** How does each observational channel produce an element? (For hexagram channels, it's algebraic. For observational channels, it's perceptual typing via 三要.)
2. **Channel interaction and the inversion principle.** When channels conflict, 体/用 生克 always overrides naive sign reading. Vol 2 (十应奥论): gold is auspicious in 三要, but if 体 is wood, metal克wood = harmful. The hexagram's algebraic evaluation inverts the perceptual omen. Priority order: hexagram > external omens (vol 2: "必须以易卦为主，克应次之").
3. **The 向背 vector.** Each observational channel has a direction (approaching/receding). This adds a temporal arrow to every 用 input. Approaching 生体 = good fortune coming; departing 生体 = good fortune spent. How does 向背 interact with the arc narrative (本=now, 互=development, 變=outcome)?

---

## VI. Outputs

### Data files

- `mh_states.json` — 384-state table with all coordinates from §I
- `mh_torus_flow.json` — directed edges on Z₅×Z₅ with 體/用 polarity, clean/turbulent cell classification
- `mh_arcs.json` — arc classification for all 384 states, with valence cross-reference
- `mh_temporal.json` — casting funnel distribution over 384 states (if not already in atlas temporal.json)

### Findings

- `findings.md` — per-section results, forbidden arcs, distribution properties, tradition-vs-text comparisons

### What carries over from the existing atlas (no recomputation)

- All hexagram-level coordinates (surface_cell, hu_cell, basin, depth, attractor, palace, rank, 六親, 納甲)
- 互 chains and 變 fan (transitions.json)
- Temporal overlay (seasonal window geometry, 旺相休囚死 states)
- Valence data (吉/凶 markers per hexagram and line)
- Embeddings and semantic probes (all null results carry over)

### What's genuinely new

- The 384-state 體/用 layer (§I) — thin but foundational, with 乾坤无互 exception
- The torus flow with polarity (§II) — the main structural contribution (1→2→1 branching)
- The relation arc analysis (§III) — where 梅花's temporal reading meets the texts
- The timing formalization (§IV-B) — 克應之期 mechanics, currently undocumented algebraically
- The semantic bindings (§V) — extraction from vol 2, not computation

---

## Estimated scope

**Computation:** Small. §I is a single script reading atlas.json + transitions.json (with 乾坤 exception handling). §II is projection of existing 互 chains. §III is classification + cross-reference. §IV-A reuses temporal.json; §IV-B requires formalizing the timing formula.

**Text extraction:** Medium. §V requires systematic extraction from vols 2-3 (18 domains, 10 channels, timing rules). Semi-manual — the text is in Chinese, structured but not tabular.

**~90% of the data already exists.** The 梅花 atlas is primarily a *lens* — a 384-row interpretive layer on the existing 64-hexagram atlas, plus timing formalization and semantic binding extraction.
