# 梅花 Atlas — Operational Plan

## Execution Architecture

**Cap:** 32 iterations. Target: 20–24 segments, leaving margin for correction.

**Dependency graph:**
```
§I (384-state table)  ←→  §V (text extraction, parallel)
       ↓                        ↓
§II (torus flow)  +  §III (relation arcs)
       ↓                        ↓
§IV (temporal) ← §V timing rules
       ↓
§VI (assembly + findings)
```

**Key data sources (existing):**
- `atlas/atlas.json` — 64 hexagrams × 33 fields (surface_cell, hu_cell, basin, depth, etc.)
- `atlas/transitions.json` — 384-entry 變 fan with full coordinate tracking
- `atlas/valence_torus.json` — per-cell valence rates, bridges
- `opposition-theory/phase4/cycle_algebra.py` — primitives: `hugua()`, `tiyong_relation()`, `tiyong_trigrams()`, `biangua()`, `five_phase_relation()`, `TRIGRAM_ELEMENT`, `SHENG_MAP`, `KE_MAP`
- `texts/iching/yaoci.json` — 384 爻辭 texts with valence markers
- `opposition-theory/sy-divination.md` — extracted analysis of 梅花易數 vols 1-3

**Source texts for §V:** The 梅花易數 volumes are not in the repo as raw text. `sy-divination.md` IS the prior extraction. §V formalizes from that document + any gaps that need original text consultation.

**Output directory:** `memories/iching/mh-atlas/`

---

## Phase 1: Foundation (§I)

### Segment 1: Build 384-state table
**Script:** `01_mh_states.py`
**Input:** `atlas/atlas.json`, `atlas/transitions.json`, `cycle_algebra.py` primitives
**Compute:** For each (hexagram, 動爻) pair (384 states):
- `ti_element`, `yong_element` — from `tiyong_trigrams()`
- `ben_relation` — directed Z₅ relation (用→體)
- `hu_upper_element`, `hu_lower_element` — from atlas hu data (handle 乾坤无互 below)
- `ti_hu_element`, `yong_hu_element` — 互 trigram on 體's side vs 用's side
- `hu_upper_relation`, `hu_lower_relation` — each vs 體
- `bian_hex` — from `biangua()`
- `bian_yong_element` — 變卦's 用-side trigram element
- `bian_relation` — 變用 vs 體
- `relation_vector` — [ben, ti_hu, yong_hu, bian] (position = weight)

**乾坤无互 exception (12/384 states):** For hex 0 (坤) and hex 63 (乾), 互 is self-referential. Rule: "互其变卦" — use the 互 of the 變卦 instead. Since 變 depends on 動爻, these 12 states each get a different 互 hexagram. Route: `biangua(h, line)` → `hugua(bian_hex)` → extract 互 trigrams.

**Output:** `mh_states.json` — 384 entries with all coordinates.

### Segment 2: Derived coordinates + verification
**Input:** `mh_states.json`, `texts/iching/yaoci.json`
**Compute:**
- `ti_party_count` — count of trigrams (用, 互上, 互下, 變用) sharing 體's element or generating it (on 生 cycle)
- `yong_party_count` — count of trigrams that 克 體 or drain 體 (體 generates them)
- `arc_valence` — net direction of 4-step vector (classify as improving/worsening/stable)
- `ben_bian_shift` — how 體/用 relation changes from 本 to 變

**Attach valence markers** from yaoci.json to each state for later cross-reference.

**Verify:**
- All 384 states present
- 乾坤 states have correct routed 互 (different from all other hexagrams')
- 128 distinct (ti_element, yong_element) pairs at 本 level (64 × 2 polarities)
- relation_vector covers expected range

**Update:** `mh_states.json` with derived fields.

### Segment 3: Distribution analysis of §I
**Input:** `mh_states.json`
**Compute §I key questions:**
1. Distribution of relation vectors — how many of 5⁴=625 possible arcs realized? Which forbidden?
2. The 128→384 expansion — how much information does specific 動爻 add beyond polarity?
3. Count distinct 互 evaluations for 乾/坤 (should be up to 6 each, vs 1 for others)

**Output:** Console analysis + update findings draft.

---

## Phase 2: Geometry + Narrative (§II + §III, after §I)

### Segment 4: §II — Project onto 梅花 torus
**Script:** `02_mh_torus.py`
**Input:** `mh_states.json`, `atlas/z5z5_cells.json`
**Compute:**
- Each state maps to 梅花 torus cell (ti_element, yong_element) — different from atlas surface_cell (lower, upper)
- The 本→互 transition as directed edge on torus (體 fixed, 用-axis changes)
- The 互 step: 1→2→1 branching (體 vs 体互 cell + 用互 cell → 變用 cell)

**Note:** Atlas torus axes = (lower, upper) positional. 梅花 torus axes = (體, 用) relational. Same hexagram maps to different cells depending on 動爻 polarity. Axis transposition = reverse involution.

**Output:** `mh_torus_flow.json`

### Segment 5: §II — Clean/turbulent cells + convergence
**Input:** `mh_torus_flow.json`, `mh_states.json`
**Compute:**
- Per-cell: is 互 mapping well-defined on 梅花 torus? (All hexagrams in cell agree on next cell?)
- Compare with atlas's 17/25 multi-valued — does count change with 體/用 polarity?
- Convergence basins at torus level — which cells map to which attractors?
- 變 step destinations per cell — where do the 3 possible 動爻 positions send you?

### Segment 6: §III — Arc classification
**Script:** `03_mh_arcs.py`
**Input:** `mh_states.json`
**Compute:** Classify all 384 arcs by shape:

| Arc type | Pattern | Description |
|---|---|---|
| Stable favorable | all 生体 or 比和 | uniformly good |
| Stable unfavorable | all 克体 | uniformly bad |
| Improving | starts 克/drain, ends 生体 | bad → good |
| Deteriorating | starts 生体, ends 克/drain | good → bad |
| Rescued | 克体 throughout, but 變 is 生体 | saved at end |
| Betrayed | 生体 throughout, but 變 is 克体 | collapses at end |
| Mixed | no clear trend | |

Classification uses the 4-element relation vector [ben, ti_hu, yong_hu, bian].

**Output:** `mh_arcs.json` — arc type + metadata per state.

### Segment 7: §III — Arc distribution + forbidden arcs
**Input:** `mh_arcs.json`, `mh_states.json`
**Compute:**
- Which arc types dominate? Frequency distribution.
- Are any arc types forbidden by the algebra? (Does basin constrain which arcs are possible?)
- Cross-tabulate arc type × basin. χ² test.

### Segment 8: §III — 比和 by arc position
**Input:** `mh_states.json`, valence data
**Compute §III.4:**
- Count 比和 appearances at each arc position (本, 体互, 用互, 變)
- Test: does 比和 at 本 have different 凶 rate than 比和 at 互 or 變?
- Compare with atlas 比和 diagonal (p=0.0002 凶 enrichment)
- Key reframe: atlas measured at hexagram level (surface relation → 爻辭 valence). 梅花 measures at reading level (體/用 → arc position). Different objects — may produce different results.

### Segment 9: §III — 互 as amplifier/dampener
**Input:** `mh_states.json`
**Compute §III.3:**
- Does 互 relation predict whether the 本→變 transition strengthens or reverses?
- Test: when 互 relation matches 本 relation direction, does 變 relation follow? When 互 opposes 本, does 變 break?
- Is 互 genuinely intermediate or structurally independent of the 本→變 arc?

### Segment 10: §III — 體黨/用黨 + structural overrides
**Input:** `mh_states.json`, valence data
**Compute §III.2 + §III.5:**
- 體黨 > 用黨 correlation with favorable arc_valence
- Cross-reference with 爻辭 吉/凶 markers
- Structural override cases: when arc gives clear signal but hexagram identity contradicts (the 西林寺 pattern — 比和 everywhere but structurally 剝). How frequent?

---

## Phase 3: §V Text Extraction (can start parallel with Phase 1)

### Segment 11: §V — 18 domain bindings
**Source:** `sy-divination.md` (already extracted 11 domains in the table)
**Extract:** Complete table for all 18 domains:
- Domain name → 體 meaning → 用 meaning → special rules
- Per-trigram image bindings per domain (where available)
- Note Weather exception (no 體/用 split) and Illness sub-systems

**Output:** `mh_domains.json` — structured domain bindings.

### Segment 12: §V — 十應 channels + inversion + 向背
**Source:** `sy-divination.md`
**Extract:**
- 10 channels → element derivation method (algebraic for channels 1-3, perceptual for 4-10)
- Inversion priority rule: hexagram 生克 > perceptual omen (formalizable)
- 向背 sign modifier: approaching = +1, departing = -1 on valence (semi-formalizable)
- Document boundary: 三要 framework = context only; 真生真克 intensity = boundary marker

**Output:** `mh_channels.json`

### Segment 13: §V — Timing formula (→ feeds §IV-B)
**Source:** `sy-divination.md` + sage's vol 3 observations
**Formalize:**
```
timing = f(arc_position) × g(observer_state) × base_number
```
Where:
- f: {本生体→immediate, 互生体→gradual, 變生体→slow}
- g: {walking→0.5, standing→1.0, sitting→2.0}
- base_number: 全卦之数 (total from casting)
- Unit: practitioner judgment (days/months/years by event type)

**Output:** `mh_timing.json` + documentation in findings.

---

## Phase 4: Temporal (§IV, after §I + §V timing)

### Segment 14: §IV-A — 先天 reachability over 384 states
**Script:** `04_mh_temporal.py`
**Input:** `mh_states.json`, `atlas/temporal.json`
**Compute:**
- Which of 384 states are reachable via 先天 casting?
- Are any unreachable? (All 64 hexagrams reachable per atlas; but specific 動爻 positions?)
- Distribution across torus cells

### Segment 15: §IV-A — 後天 distributional analysis
**Input:** `mh_states.json`
**Compute:**
- For each 後天 casting method, theoretical distribution across 384 states
- Which methods produce most uniform coverage?
- Temporal clustering: which (體, 用) cells overrepresented in calendar distribution?

### Segment 16: §IV-B — Timing integration + seasonal bias
**Input:** `mh_timing.json`, `mh_states.json`, `atlas/temporal.json`
**Compute §IV.4-5:**
- Seasonal bias on arc types: when casting in spring (Wood 旺), are 木-體 states overrepresented?
- Does casting mechanism bias toward arcs where 體 is seasonally strong?
- The 2/5 ceiling in 梅花 context: when 體 is 休/囚/死, does the arc still give valid structure?

---

## Phase 5: Assembly (§VI)

### Segment 17: Assemble final data files
**Verify + merge:**
- `mh_states.json` — complete 384-state table (§I)
- `mh_torus_flow.json` — torus edges + cell classification (§II)
- `mh_arcs.json` — arc classification (§III)
- `mh_domains.json` — semantic bindings (§V)
- `mh_channels.json` — 十應 formalization (§V)
- `mh_timing.json` — timing formula (§V→§IV)

### Segment 18: Write findings.md
**Synthesize per-section results:**
- §I: relation vector distribution, forbidden combinations, 乾坤 exception behavior
- §II: 梅花 torus vs atlas torus, clean/turbulent regions
- §III: arc types, 比和 resolution, 互 role, tradition interpolation table
- §IV: reachability, seasonal bias, timing formalization
- §V: extractable vs contextual boundary, domain structure

### Segment 19: Cross-reference + open questions
**Compare with prior findings:**
- Atlas findings (complement structure, perturbation onion, valence bridges)
- Synthesis findings (two bridges, orthogonality wall, pipeline asymmetry)
- Does the 384-state view reveal anything invisible at 64-hexagram level?
- Update open-questions.md if new questions emerge

---

## Design Decisions (from discussion)

1. **Relation vector [ben, ti_hu, yong_hu, bian]** — position IS the weighting. No separate weight metadata. Slot 2 (ti_hu) structurally prioritized over slot 3 (yong_hu) by positional semantics.

2. **§V extractability boundary:**
   - Extractable: 18 domain bindings, 十應 channel→element, inversion priority rule, 向背 sign modifier, timing formula
   - Context only: 三要 framework, 真生真克 intensity gradient

3. **比和 discrepancy** — let emerge from §III arc classification naturally. Atlas measured at hexagram level; 梅花 measures at reading level. Different measurement objects.

4. **Timing formula** — more mechanical than initially planned:
   ```
   timing = f(arc_position) × g(observer_state) × 全卦之数
   ```
   Only unit selection (days/months/years) is interpretive.

---

## Iteration Budget

| Phase | Segments | Est. iterations |
|-------|----------|----------------|
| §I Foundation | 1–3 | 4–5 |
| §II Torus | 4–5 | 3–4 |
| §III Arcs | 6–10 | 5–7 |
| §V Text | 11–13 | 3–4 |
| §IV Temporal | 14–16 | 3–4 |
| §VI Assembly | 17–19 | 3–4 |
| **Total** | **19** | **21–28** |

Margin: 4–11 iterations for correction/iteration.
