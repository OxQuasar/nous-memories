# 火珠林 Atlas — Operational Plan

## Overview

Six sections (I–VI), executed sequentially. Each produces data files and findings. 
~60% of algebraic structure exists in huozhulin probes 01–06. Atlas extends with 
temporal layers, network formalization, and domain extraction.

Working directory: `memories/iching/atlas-hzl/`
Dependencies: probes (`huozhulin/01-06*.py`), atlas (`atlas/atlas.json`, `atlas/transitions.json`)
Source text: `texts/huozhulin/huozhulin.md` (1237 lines)

---

## §I: 64 Static Profiles (iterations 1–6)

**Goal:** Consolidate probes 01–04 into atlas format. Add 納音, 卦身, static interaction topology.

**Output:** `hzl_profiles.json` — 64 entries, one per hexagram.

### Iteration 1: Core profile builder
- Script `01_static_profiles.py`
- Import from probes 01–04: 納甲, palace, 六親, 飛伏
- Per hexagram: palace, palace_element, palace_rank, shi_line, ying_line
- Per line: stem, branch, element, liuqin
- Per line: feifu_branch, feifu_element, feifu_liuqin (from palace root)
- liuqin_census, missing_liuqin
- Validate against worked examples (姤, 遁)

### Iteration 2: 納音 + 卦身
- 納音 computation (stem+branch → 60 甲子 → 納音 name + element)
  - The 60 甲子 cycle assigns each stem-branch pair a 納音 (e.g., 甲子/乙丑 = 海中金)
  - Source: standard 納音 table (三命通會 or equivalent)
- 卦身 computation from 世 line (陽世從子月起, 陰世從午月起)
  - Count from 世 line's position to find the 卦身 branch
  - Determine which line (if any) hosts the 卦身
- Add to profiles, validate

### Iteration 3: Cross-tabulations and distributions
- 世/應 × 六親 cross-tab: what 六親 tends to sit at 世? at 應? 
- 飛伏 completeness map: per hexagram, which 六親 visible vs require 伏 access
  - Correlate with palace rank
- 納音 distribution: 60 names across 384 positions, coverage/clustering
- 卦身 distribution: which lines host 卦身, element distribution

### Iteration 4: Static interaction topology
- For each hexagram: compute which line pairs are connected by the 8 primitives
  - 沖 (opposite branches): 子↔午, 丑↔未, 寅↔申, 卯↔酉, 辰↔戌, 巳↔亥
  - 合 (six harmony pairs): 子丑, 寅亥, 卯戌, 辰酉, 巳申, 午未
  - 刑 (three-punishment groups): 子卯, 丑戌未, 寅巳申, 辰辰/午午/酉酉/亥亥 (self-punishment)
  - 害 (six harm pairs): 子未, 丑午, 寅巳, 卯辰, 申亥, 酉戌
  - 墓 (element's graveyard branch): Fire→戌, Water→辰, Wood→未, Metal→丑, Earth→辰
  - 生/克: element-level between lines
- Output: per-hexagram adjacency data (primitive → list of (line_i, line_j) pairs)
- Compute graph density statistics across all 64

### Iteration 5: Findings for §I
- Write §I findings to `findings.md`
- 梅花 comparison note: 梅花 reduces 6 lines to 2 trigrams; 火珠林 keeps all 6 active
- Key metrics: graph density, 六親 distribution at 世/應, 飛伏 correlation with rank

---

## §II: Seasonal Activation (iterations 6–8)

**Goal:** Full 320-state map (64 hexagrams × 5 seasons). Operationalize 2/5 ceiling.

**Output:** `hzl_seasonal.json` — 320 entries.

### Iteration 6: Seasonal map builder
- Script `02_seasonal_map.py`
- Load profiles from §I
- For each hexagram × season: compute 旺/相/休/囚/死 for each line's element
- Per entry: line_strengths[1-6], per-六親-type strength summary
- 用神 strength for common question types (which 六親 is 旺/相 for which domain)

### Iteration 7: Functional coverage analysis
- functional_coverage: how many of 5 六親 types are 旺 or 相 per state
  - Verify 2/5 ceiling across all 320 states
- Season × palace interaction: in palace's own season, 兄弟 is 旺; in opposing season, 囚/死
- conflict_count: how many lines are 囚 or 死

### Iteration 8: §II findings
- Distribution of functional coverage across 320 states
- Which hexagram-season combinations are most/least functionally active
- 梅花 comparison: 梅花 barely uses seasonal gating ("几乎不用旺相休囚死")
  - 火珠林 uses it as primary strength assessment → strictly higher temporal resolution

---

## §III: 日辰 Layer (iterations 9–13)

**Goal:** 768 日辰 interactions (64×12) + 六神 rotation + MI computation.

**Output:** `hzl_richen.json`

### Iteration 9: 日辰 interaction map
- Script `03_richen.py`
- For each hexagram × 12 branches: compute per-line interactions
  - 生: 日辰's element generates line's element
  - 克: 日辰's element overcomes line's element
  - 沖: 日辰 is line's opposite branch
  - 合: 日辰 is line's harmony partner
  - 墓: line's element is entombed at 日辰's branch
- Note: 空 (旬空) depends on 10-day cycle, not just branch — track separately
- Output: per-hexagram × 日辰 activation pattern

### Iteration 10: 旬空 and full temporal context
- Model the 旬空 system: 60 甲子 cycle, each 旬 has 2 void branches
  - Simplified: 6 旬 × 2 void branches → 6 void-pair patterns
  - Full: 64 × 60 = 3840 states (defer unless needed)
- Compute: for each hexagram, which lines are void in which 旬

### Iteration 11: 六神 rotation
- 六神 assignment by day stem: 
  - 甲乙日→青龍起初爻, 丙丁日→朱雀起初爻, etc.
  - 6 spirits cycle through 6 lines: 青龍/朱雀/勾陳/螣蛇/白虎/玄武
- 10 stem patterns → 10 possible spirit-line assignments (but only 6 distinct rotations)
- Document which 六神 × 六親 combinations have specific interpretive weight
  (e.g., 白虎+財=wealth with violence, 青龍+用神=recovery)

### Iteration 12: MI computation — 日辰 vs 互 chain
- The central structural question: does 日辰 access genuinely different information from 互?
- Compute: for each hexagram, the 日辰 activation pattern (12 states)
- Compare with 互 chain trajectory (which elements the 互 chain traverses)
- MI(日辰 pattern, 互 trajectory) — expect near-zero (orthogonality)
- Also: activation pattern diversity — over 12-day cycle, how many distinct patterns per hexagram?

### Iteration 13: §III findings + three-layer documentation
- Three-layer activation map:
  - 地支 layer: all domains (default)
  - 天干 layer: 占天時 (天干化氣), 六神 rotation (day stem)
  - 納音 layer: 占墳墓, 占姓字, 占鬼神
- Document the gravesite example as the structural specimen (all 3 layers)
- 梅花 comparison: 梅花 has one temporal input (casting moment); 火珠林 has floating daily reference
- 4/5 ceiling (already proven in R7) — verify geometrically in the 日辰 data

---

## §IV: 動爻 Layer (iterations 14–17)

**Goal:** 化爻 transformation semantics as independent information channel.

**Output:** `hzl_dongyao.json`

### Iteration 14: Transformation table builder
- Script `04_dongyao.py`
- For each line position: when it moves, what's the new branch? new element? new 六親?
- The new branch: line flips → trigram changes → new 納甲 assignment
- 化爻 type: X→Y where X,Y ∈ {兄弟,子孫,父母,妻財,官鬼}
  - 5×5 = 25 possible types
  - Count distribution: which types are common, which rare
- Selective: compute for single-line moves (64 hexagrams × 6 lines = 384 cases)

### Iteration 15: Multi-line transformations
- For structurally significant multi-line patterns:
  - 世+應 both moving (structural resonance)
  - All lines of one trigram moving (trigram-level transformation)
  - Common coin outcomes (2 moving lines = 29.7% probability)
- Basin crossing: does 變卦 cross basin? Cross palace?
- Depth change analysis

### Iteration 16: Per-line transformation type analysis
- The source text's transformation semantics: 
  - 財化鬼 (wealth→trouble), 官化官 (shifting authority), 父化父 (repeated difficulty)
  - Extract the named patterns from source text (lines 62-89: 獨發亂動)
- Cross-tabulate: transformation type × palace → frequency
- Same 變卦 reached via different transformation patterns → different meanings
  - Quantify: how many cases have identical 變卦 but different per-line transformation types?

### Iteration 17: §IV findings
- Distribution of 25 化爻 types
- Which types cluster by palace
- 靜卦 analysis: 17.8% of readings have no moving lines — what information remains?
  - 世 line + 日辰 interactions + 六親 strength = the 靜卦 reading protocol
- 梅花 comparison: 梅花 presupposes exactly 1 moving line; 火珠林 first asks whether

---

## §V: Network Reading (iterations 18–23)

**Goal:** Formalize the reading framework. Three components: 飛伏 diagnostics, 用神 protocol, interaction graph.

**Output:** `hzl_network.json` + text in findings

### Iteration 18: 飛伏 diagnostic table extraction
- Source text lines 137-240: 8+ diagnostic cases
  - 占財伏鬼, 占財伏兄, 財伏父子, 占鬼伏兄, 占鬼伏財, 官伏父母, 官伏子孫, 官鬼伏官
- For each case: extract the evaluation protocol
  - What 飛 type sits above → how it interacts with the hidden 用神
  - Seasonal conditions for the hidden line to be accessible
  - 日辰 conditions for emergence (透出)
- Structure as: {伏_type: X, 飛_type: Y, interaction: ..., conditions: [...]}

### Iteration 19: 獨發 patterns (single 六親 moving)
- Source text lines 256-321: 子孫獨發, 兄弟獨發, 父母獨發, 官鬼獨發, 妻財獨發
- Each has domain-dependent effects: same 六親 moving means different things for different questions
- Extract the per-type × per-domain interaction table
- This is the bridge between §IV (which lines move) and §VI (domain bindings)

### Iteration 20: 用神 evaluation protocol
- Formalize the algorithmic protocol from method.md Steps 8-10:
  1. Select 用神 (from domain → 六親 mapping)
  2. Assess visibility: is 用神 飛 (visible) or 伏 (hidden)?
     - If hidden: apply 飛伏 diagnostic from iteration 18
  3. Assess strength: 旺相休囚死 (from seasonal layer)
  4. Assess 日辰 interaction: 生/克/沖/合/墓/空
  5. Assess 動/靜: is 用神 moving? what does it transform into?
  6. Assess network: what are the interactions with other lines?
  7. Judge: favorable signs vs unfavorable signs (method.md Step 10)

### Iteration 21: Interaction graph computation (sampled)
- Select 8 representative hexagrams (1 per palace, varying ranks)
- For each: compute the full interaction graph with §I-IV data
  - Static topology (from §I iteration 4)
  - Seasonal activation (from §II, 1 season)
  - 日辰 activation (from §III, 2-3 日辰 values)
  - 動爻 overlay (1 moving line pattern)
- Characterize: graph density, which connections are semantically relevant
- Expected: sparse graphs where 飛伏 diagnostic + 用神 chain are primary content

### Iteration 22: The 8 axes formalization
- Source text line 1229: "世、應、日、月、飛、伏、動、靜" = 8 evaluation axes
- Map each axis to its data source (which §I-IV output)
- Document: how the 8 axes compose into a reading
- The 8 primitives (克合刑害墓旺空沖) operate BETWEEN axes

### Iteration 23: §V findings
- The evaluation protocol as an algorithm
- 飛伏 diagnostic table (structured)
- Interaction graph characterization
- 梅花 comparison: 梅花 uses one arc (本→互→變); 火珠林 uses a network with 8 axes × 8 primitives

---

## §VI: Domain Bindings (iterations 24–28)

**Goal:** 用神 selection table + 5 special protocols + 卦身 activation conditions.

**Output:** `hzl_domains.json` + text in findings

### Iteration 24: 用神 selection table
- Source text domains (lines 322-1060): extract per domain:
  - 用神 (primary 六親)
  - 忌神 (antagonist 六親)
  - 世 represents what
  - 應 represents what
- ~25 rows, one per domain
- Validate against method.md Step 8 table

### Iteration 25: Standard domain protocols
- For the ~20 standard domains: verify they follow the same engine
  - Select 用神 → assess strength/visibility/temporal → read 生克
- Document the semantic bindings (what 體/用 represent) per domain
- Six structural clusters (from discussion):
  self-vs-other, self-vs-asset, self-vs-endeavor, body-vs-condition, self-vs-dwelling, self-vs-absent

### Iteration 26: Five special protocols
- 占疾病(+醫藥+病忌): 3 sub-systems
  - 鬼元素→disease type mapping
  - 飛伏位→cause/origin
  - 五行動→symptoms
- 占天時/晴雨: 天干化氣 (甲己化土, 乙庚化金, 丙辛化水, 丁壬化木, 戊癸化火)
- 占射覆/覆射: 財=外, 鬼=里 framework
- 占來情: meta-diagnostic
- 占姓字: character decomposition using all three layers

### Iteration 27: 卦身 activation conditions
- Per-domain: does 卦身 activate?
  - 占謁貴 (line 464), 占墳墓 (line 927), 占起造 (line 867), 占婚姻 (line 401)
- What does 卦身 indicate in each domain?
- 卦身 × 六親 interaction: when 卦身 falls on a specific 六親 type

### Iteration 28: §VI findings + structural comparison
- 火珠林 vs 梅花 domain structure:
  - 梅花: one engine, 18 skins (R30)
  - 火珠林: one engine, ~25 skins + 5 genuine exceptions
  - Difference: quantitative (more domains) with 5 qualitative exceptions
- The 3 deepest qualitative differences:
  1. 火珠林 has floating daily reference (日辰), 梅花 has fixed 體 reference
  2. 火珠林 has per-domain 用神 selection, 梅花 always uses 體/用
  3. 火珠林 has 飛伏 hidden structure, 梅花 has 互 nuclear structure

---

## Final (iterations 29–30)

### Iteration 29: Cross-section synthesis
- The central question: does 日辰 access genuinely different information from 互?
  - Use MI computation from iteration 12
  - If near-zero: the two systems are genuinely complementary (tangent vector vs local observable)
  - This confirms the huozhulin findings.md characterization
- Information budget: what does each section contribute?
  - §I: static identity (palace, 六親, 飛伏) — who are the players
  - §II: seasonal strength — who has power
  - §III: daily activation — what's triggered now
  - §IV: transformation — what changes
  - §V: network reading — how they interact
  - §VI: domain binding — what the question selects

### Iteration 30: Final findings + open questions
- Complete findings.md
- Validate all data files
- Open questions for future work
- Update open-questions.md

---

## Budget

- 30 iterations planned out of 32 cap
- 2 reserved for corrections/extensions
- §I heaviest (6 iterations): foundation, most new computation
- §III second heaviest (5 iterations): genuinely new layer
- §V third (6 iterations): synthesis of text + computation
- §II, §IV lighter (3 each): extend existing probe work
- §VI moderate (5 iterations): text extraction
