# 火珠林 Atlas — The 6-Node Network in Shell Coordinates

## What this is

The 梅花 atlas maps the core projection: 體/用 elements through 本→互→變, a directed arc on Z₅. It reads convergence — becoming.

This atlas maps the **shell projection**: 納甲 branches on all 6 lines, evaluated through 六親 against the palace element, gated by seasonal strength and 日辰. It reads identity — being.

Where 梅花 reduces (6→4→2 bits, spiral inward), 火珠林 keeps all six lines active as a network. Where 梅花 has one temporal input (the casting moment), 火珠林 has a floating daily reference (日辰) that changes the reading's activation pattern every day.

The unit of analysis is not the hexagram alone but the **hexagram × season × 日辰 × 動爻 configuration** — a hexagram with its full temporal context and moving line pattern.

## What 火珠林 actually reads

A 火珠林 reading is a 6-node network:

```
For each line:
  branch (地支) → element → 六親 (via palace element)
  × strength (旺相休囚死, from season)
  × state (動/靜, from casting)
  × visibility (飛/伏, from palace root)
  × 日辰 interaction (生/克/沖/合/墓/空)
```

The output is a snapshot of which relational roles are active, strong, visible, and temporally triggered — then read through 8 operational primitives (克/合/刑/害/墓/旺/空/沖, per the source text's enumeration).

**Three-layer architecture** (from 易中明義): 天干管天文 (celestial stems read heaven), 地支管人事 (earthly branches read human affairs), 納音管地理 (sixty tones read earth/geography). Most readings use the 地支 layer. 天干 and 納音 are specialized — the gravesite example in the source text uses all three layers simultaneously.

**卦身** — the "sixth relation." The five 六親 types plus the hexagram body makes literally six. 卦身 is computed from the 世 line (陽世從子月起, 陰世從午月起). When 世 is void (空), the reader falls back to 卦身. It's the system's fallback anchor.

**六神** — six spirits (青龍/朱雀/勾陳/螣蛇/白虎/玄武) assigned to lines daily, rotating with the day stem. They modify interpretation — 白虎 on a 財 line means the wealth comes with violence; 青龍 on 用神 means recovery even when the hexagram looks dire. A temporal overlay on top of the static 六親 assignment.

## The state space

The full state space is large:

- 64 hexagrams × 64 動爻 patterns (0 to 6 moving lines) = 4,096 hexagram configurations
- × 5 seasons × 60 日辰 = 300 temporal contexts
- = ~1.2M total states

But this factorizes. The hexagram determines the static structure (六親, 世/應, 飛伏). The temporal context determines activation (strength, 日辰 interactions). The 動爻 pattern determines transformation (which lines change, producing which 變卦).

### The tractable decomposition

1. **64 static profiles** — the hexagram's fixed structure (六親 assignment, 世/應 position, 飛伏 lines)
2. **64 × 5 seasonal activations** — which 六親 are strong/weak in each season
3. **64 × 60 日辰 interactions** — which lines are 沖'd, 合'd, 墓'd, or 空'd by today's branch
4. **64 × 64 動爻 → 變卦 table** — which configurations produce which transformations

### Key structural difference from 梅花

梅花's 384 states (64 × 6) assume exactly one moving line. 火珠林's coin mechanism produces 0–6 moving lines with P(multi) = 47%, P(none) = 17.8%. The modal outcome is 靜卦 (no change). This is the fundamental architectural difference: **梅花 presupposes transformation; 火珠林 first asks whether.**

## Dependencies

### From existing work (huozhulin/)

Six probes already computed:
- `01_najia_map.py` — 納甲 implementation, shell ⊥ core proof
- `02_palace_kernel.py` — palace walk = spectral traversal, onion decomposition
- `03_liuqin.py` — 六親 near-injection (59/64), word census
- `04_feifu.py` — 飛伏 completeness (2/8 full, 6/8 incomplete)
- `05_dongyao.py` — coin mechanism probability distribution
- `06_seasonal.py` — 旺相休囚死 seasonal gating, 2/5 ceiling

These establish the algebraic structure. The atlas operationalizes it.

### From atlas/

- `atlas.json` — 64 hexagram profiles (trigrams, elements, basin, depth)
- `transitions.json` — 互/變/palace data

### Source texts

- `huozhulin/method.md` — complete 11-step method description
- `huozhulin/example.md` — two worked examples (gravesite, ghost identification)
- Source texts for domain rules (to be identified)

---

## I. The 64 Static Profiles

### Per-hexagram coordinates

For each of 64 hexagrams:

| Coordinate | Source | Description |
|---|---|---|
| `palace` | from atlas | which of 8 palaces |
| `palace_element` | from palace | the reference element ∈ Z₅ |
| `palace_rank` | from palace walk | position 0–7 in palace (本宮/一世/.../遊魂/歸魂) |
| `shi_line` | from rank | 世 position (1–6) |
| `ying_line` | from rank | 應 position (1–6) |
| `lines[1-6].branch` | 納甲 | 地支 for each line |
| `lines[1-6].element` | from branch | element of each line |
| `lines[1-6].liuqin` | from element vs palace | 六親 label |
| `lines[1-6].fufu_branch` | from palace root | hidden (伏) branch underneath |
| `lines[1-6].fufu_element` | from hidden branch | hidden element |
| `lines[1-6].fufu_liuqin` | from hidden element vs palace | hidden 六親 |
| `liuqin_census` | count per type | which 六親 are present, which missing |
| `missing_liuqin` | from census | which relations must be found in 伏 lines |
| `nayin[1-6]` | from stem+branch | 納音 for each line |
| `guashen` | from 世 line | 卦身 branch (陽世從子, 陰世從午) |
| `guashen_element` | from guashen | 卦身's element |
| `guashen_line` | where guashen falls | which line (if any) hosts the 卦身 |

### Key questions

1. **六親 distribution across 512 hexagrams (64 × 8 palaces... wait, each hexagram belongs to exactly 1 palace).** Census: how often is each 六親 missing? Which are structurally most absent? (Known from probe 4: 兄弟 most absent.)
2. **世/應 × 六親 cross-tabulation.** What 六親 tends to sit at 世? At 應? Is the distribution uniform or biased?
3. **飛伏 completeness map.** For each hexagram: which 六親 are visible, which require 伏 access? How does this correlate with palace rank?
4. **納音 distribution.** 60 納音 across 384 line positions (64 × 6). Coverage? Clustering?

---

## II. The Seasonal Activation Layer

### 5 seasonal states per hexagram

For each hexagram × season (320 combinations):

| Coordinate | Description |
|---|---|
| `line_strengths[1-6]` | 旺/相/休/囚/死 for each line |
| `liuqin_strength` | strength of each present 六親 type |
| `yongshen_strength` | strength of the 用神 for common question types |
| `functional_coverage` | how many of the 5 六親 are 旺 or 相 |
| `conflict_count` | how many lines are 囚 or 死 |

### Key questions

1. **The 2/5 ceiling in practice.** At most 2 elements are 旺/相 in any season. For each hexagram, how many 六親 types are functionally active? Distribution across 320 states.
2. **Season × palace interaction.** Each palace has a fixed element. In the palace's own season, the root 六親 (兄弟) is 旺. In the opposing season, it's 囚 or 死. How does this modulate the reading?
3. **Comparison with 梅花's temporal layer.** 梅花 has no 日辰 and barely uses seasonal gating ("几乎不用旺相休囚死"). 火珠林's temporal resolution should be strictly higher. By how much? What information does the extra resolution buy?

---

## III. The 日辰 Layer

### The floating daily reference

日辰 = today's 地支 (one of 12 branches, cycling daily). It interacts with every line:

| Interaction | Condition | Effect |
|---|---|---|
| 生 | 日辰's element generates line's element | strengthens |
| 克 | 日辰's element overcomes line's element | weakens |
| 沖 | 日辰 is line's opposite branch (子↔午, 丑↔未, ...) | disrupts/activates |
| 合 | 日辰 is line's harmony partner (子丑, 寅亥, ...) | binds/stabilizes |
| 墓 | line's element is entombed at 日辰's branch | trapped |
| 空 | line's branch is one of the two 旬空 branches | empty/unrealized |

### Per-hexagram × 日辰 (64 × 12 = 768 combinations)

Note: 旬空 depends on the 旬 (10-day cycle), not just the 日辰. Full model needs 64 × 60 = 3,840 combinations. Simplified model uses 64 × 12 for the 6 interaction types (excluding 空).

| Coordinate | Description |
|---|---|
| `line_interactions[1-6]` | which interaction each line has with today's 日辰 |
| `yongshen_interaction` | how 日辰 affects the 用神 specifically |
| `activation_pattern` | which lines are 沖'd awake or 合'd still |
| `entombment` | which lines are 墓'd (trapped) |

### 六神 daily rotation

Six spirits rotate by day stem (甲乙→青龍起, 丙丁→朱雀起, etc.), assigned to lines top-down. This adds an interpretive color layer — same 六親 reads differently under different 六神. Produces 10 × 6 = 60 possible spirit-line assignments per hexagram.

### Key questions

1. **日辰 coverage.** Over a 12-day cycle, how many distinct activation patterns does each hexagram produce? Is the pattern space rich or constrained?
2. **日辰 × 動爻 interaction.** When a moving line is also 沖'd by 日辰, the activation is doubled. How often does this compound? Does it cluster by palace?
3. **The 4/5 ceiling.** 火珠林 accesses 4/5 of Z₅ through 日辰 + season combined (vs 梅花's 2/5). Verify: is the ceiling exactly 4/5, and what is the structural gap between the two systems?
4. **六神 × 六親 interaction.** How much does 六神 modulate interpretation? Is it additive (color overlay) or multiplicative (changes the reading type)?

---

## IV. The 動爻 Layer

### Coin mechanism probability distribution

From probe 5 (known):
- P(0 moving) = 17.8% (靜卦, modal)
- P(1 moving) = 35.6%
- P(2 moving) = 29.7%
- P(3 moving) = 13.2%
- P(4+) = 3.7%

### Per-configuration analysis

For each hexagram × 動爻 pattern:

| Coordinate | Description |
|---|---|
| `biangua` | the 變卦 (all moving lines flip) |
| `liuqin_disruption` | how many 六親 labels change in the 變卦 |
| `basin_cross` | whether 本卦 and 變卦 are in different basins |
| `palace_switch` | whether the palace changes |
| `depth_change` | change in onion depth |

The full 64 × 64 table is 4,096 entries. Most are reachable (any line can independently be old or young, though probabilities vary by pattern).

### 化爻 (transformation line semantics)

When a line moves, it doesn't just flip — it transforms its branch. The new branch produces a new element, which may change the 六親 label. The source text devotes extensive discussion to "化出" patterns: 財化鬼 (wealth transforms into trouble), 官化官 (authority shifting, deception), 父化父 (repeated difficulty), etc. Each X→Y transformation has specific divinatory meaning.

This is richer than just tracking which hexagram results. The per-line transformation type is an independent information channel — you can have the same 變卦 reached via different transformation patterns with different meanings.

### Key questions

1. **靜卦 readings.** 17.8% of readings have no moving lines. The system has a specific protocol for this: read the 世 line, check 日辰 interactions, assess 六親 strength. How does the information content of a 靜卦 reading compare to one with moving lines?
2. **Multi-line interactions.** When lines 2 and 5 both move (世/應 in many palaces), the reading has a structural resonance. How often do structurally significant line combinations occur?
3. **變卦 vs 本卦 六親 comparison.** The transformation changes branches → elements → 六親. A 官鬼 that transforms into 子孫 (as in the ghost example) is a type-crossing transformation. How common are type crossings? Do they cluster by palace?

---

## V. The Network Reading

### The 8 operational primitives

The source text names 8 (line 1229): 克/合/刑/害/墓/旺/空/沖 — 「知此八宗，與神奧通」. These operate between:
- Line ↔ line (within the hexagram)
- Line ↔ 日辰 (temporal trigger)
- Line ↔ season (strength)
- Flying ↔ hidden (飛伏 interaction)

### What to formalize

1. **The interaction graph.** For each hexagram × temporal context: build the 6-node graph where edges are the 8 primitive interaction types. What's the typical graph density? Clustering coefficient?
2. **用神 evaluation protocol.** Given a question type → select 用神 → evaluate its strength, interactions, visibility, and temporal triggers. The protocol is algorithmic. Formalize it.
3. **The 3-layer system (天干/地支/納音).** The example shows three layers producing different kinds of output (structural/directional/imagistic). Map which outputs come from which layer.

---

## VI. Domain Bindings

### ~30 domains in the source text

The 火珠林 source covers substantially more domains than 梅花's 18, with deeper per-domain specialization:

**Core domains (with extensive rules):** 占身命, 占形性, 占運限, 占婚姻(+婢妾), 占孕產, 占科舉, 占謁貴, 占買賣, 占求財, 占出行, 占行人, 占逃亡(+方位), 占失物/鬼祟, 占賊盜, 占鬼神, 占詞訟, 占脫事散憂, 占疾病(+醫藥+病忌), 占家宅(+人口+起造), 占墳墓, 占天時/晴雨

**Specialized domains:** 占博戲, 占耕種, 占蠶桑, 占畜養, 占漁獵, 占朝國, 占征戰, 占射覆, 占來情, 占姓字

**Key difference from 梅花:** Each domain has domain-specific 用神 selection AND domain-specific transformation rules. 梅花 uses the same 生克 engine everywhere with different semantic bindings. 火珠林 has genuinely different protocols per domain — the 占疾病 section alone has 3 sub-systems (鬼元素→disease type, 飛伏位→cause, 五行動→symptoms). The 占天時 section uses 天干 化氣 (stem transformation) which appears nowhere else in the system.

### What to extract

1. **用神 selection table.** The text's core principle (lines 108-117): 官用取官, 私用取財. But domain-specific overrides exist. Complete table needed.
2. **Domain-specific interpretation rules.** Each domain's protocol: which 六親 is 用神, which is 忌神, what transformation patterns mean.
3. **Structural comparison with 梅花.** 梅花: one engine, 18 skins. 火珠林: one framework, ~30 specialized protocols. Is the difference quantitative (more domains) or qualitative (different evaluation logic per domain)?

---

## VII. Outputs

### Data files

- `hzl_profiles.json` — 64 static profiles (六親, 世/應, 飛伏, 納甲, 納音)
- `hzl_seasonal.json` — 320 seasonal activations (64 × 5)
- `hzl_richen.json` — 768 日辰 interactions (64 × 12, excluding 旬空)
- `hzl_dongyao.json` — transformation table (selective, not full 4096)

### Findings

- `findings.md` — per-section results, structural comparisons with 梅花

### What carries over (no recomputation)

- All hexagram-level coordinates from atlas.json
- All probe results from huozhulin/ (shell⊥core, palace spectral, 六親 injection, 飛伏 completeness, coin distribution, seasonal ceiling)
- Valence data, embeddings, semantic probes

### What's genuinely new

- The 64 static profiles with full 納甲/飛伏/納音/卦身 coordinates (§I) — extending probe data into atlas format
- The seasonal activation map (§II) — operationalizing the 2/5 ceiling across all hexagrams
- The 日辰 interaction map (§III) — the temporal layer 梅花 doesn't have
- The 六神 rotation layer (§III) — interpretive color overlay, 10-day cycle
- The 化爻 transformation semantics (§IV) — per-line X→Y type as independent information channel
- The network formalization (§V) — the 8-primitive interaction system (克/合/刑/害/墓/旺/空/沖)
- Domain binding extraction (§VI) — ~30 domains with per-domain specialized protocols
- The three-layer architecture (天干/地支/納音) — which outputs come from which layer

---

## Estimated scope

**Computation:** Medium. §I extends existing probe scripts into atlas format. §II–III require new computation but are combinatorial (no LLM, no embeddings). §IV reuses probe 5 data. §V is the heaviest — formalizing the interaction graph.

**Text extraction:** Heavy. §VI requires systematic extraction of domain-specific rules from 火珠林 source texts. The method.md covers the framework but the domain rules need source material.

**~60% of the algebraic structure already exists** in the probes. The atlas extends it with the temporal layer (日辰, seasonal activation) and network formalization — the parts that make 火珠林 operationally distinct from 梅花.

### Key structural question

**Does the 日辰 layer access genuinely different information from 梅花's 互 chain, or is it a different encoding of the same structure?**

梅花 reads depth (本→互→變 = outside→inside→transformed). 火珠林 reads time (旺衰 + 日辰 = seasonal strength + daily trigger). Both are projections from Z₂⁶. The probes established they're orthogonal (shell ⊥ core). The atlas should quantify this: how much mutual information exists between the 日辰 activation pattern and the 互 chain trajectory? If near-zero, the two systems are genuinely complementary. If nonzero, there's hidden redundancy.
