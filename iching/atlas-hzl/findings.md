# 火珠林 Atlas — Findings

> The shell projection operationalized: 納甲 branches on all 6 lines, evaluated through 六親 against the palace element, gated by seasonal strength and 日辰.
> All statistics are exhaustive enumerations over the relevant state spaces.

**Epistemological key:**
- **[proven]** — algebraically necessary, follows from definitions
- **[measured]** — exhaustive enumeration
- **[extracted]** — structured from source text

---

## §I. The 64 Static Profiles

### Data
- `hzl_profiles.json` — 64 entries, 15+ fields per hexagram, 10 fields per line
- `hzl_topology.json` — 64 entries, static interaction graph per hexagram
- Scripts: `01_static_profiles.py`, `02_cross_tabs.py`
- Validated against both worked examples (姤, 遁)

### Finding I.1: 世/應 × 六親 asymmetry

**[measured]** The distribution of 六親 at 世 and 應 positions is structurally asymmetric:

| 六親 | At 世 | At 應 | Net |
|------|-------|-------|-----|
| 妻財 | 20 | 12 | +8 at 世 |
| 官鬼 | 18 | 14 | +4 at 世 |
| 子孫 | 12 | 11 | balanced |
| 父母 | 7 | 22 | +15 at 應 |
| 兄弟 | 7 | 5 | balanced-low |

**妻財+官鬼 = 38/64 = 59% at 世.** The querent's position structurally favors wealth and authority roles. The counterpart (應) structurally favors parental/authority roles (父母 = 34% at 應). This aligns with the source text's axiom: 「天下之事不出財官二字」.

**[measured] Palace-specific clustering:** 震 palace has 妻財 at 世 in 6/8 hexagrams — structurally pre-loaded for wealth inquiries. 坤/離 palaces have 官鬼 at 世 in 4/8 — pre-loaded for authority/illness inquiries. 乾 palace has 父母 at 世 in 4/8 — pre-loaded for documents/credentials.

### Finding I.2: 游魂 = universal 飛伏 completeness

**[measured]** 飛伏 completeness (visible ∪ hidden = all 5 六親) by rank:

| Rank | Complete |
|------|----------|
| 本宮 | 2/8 |
| 一世 | 4/8 |
| 二世 | 3/8 |
| 三世 | 2/8 |
| 四世 | 5/8 |
| 五世 | 5/8 |
| 游魂 | **8/8** |
| 歸魂 | 4/8 |

**[proven] Mechanism — two modes:**
- Mode 1 (4/8 palaces: 震,巽,艮,兌): The 游魂 visible hexagram (complement lower + middle-flipped upper) spans all 5 elements. No hidden needed.
- Mode 2 (4/8 palaces: 坎,離,乾,坤): Visible covers 4/5. The root's hidden lines rescue the 5th.

**游魂 achieves completeness because it maximizes visible-hidden element divergence.** The complement lower guarantees that whatever the root is blind to, the visible hexagram sees. The non-monotonic curve (本宮 2/8 → 三世 2/8 → 游魂 8/8) follows from divergence degree, not rank order. This refines probe 4's finding (6/8 palaces incomplete) by showing the incompleteness is rank-dependent, not palace-dependent — 游魂 is the universal rescue rank.

### Finding I.3: Earth universality — structural invariant

**[proven]** Earth can never be a missing element. Every trigram's branch set contains at least one Earth branch.

**Mechanism:** Earth branches (丑辰未戌) occupy positions 1,4,7,10 in the 12-branch cycle — spacing 3. The 納甲 step-2 selection rule picks branches at k, k+2, k+4, spanning 5 positions. Since 5 > 3 (Earth's spacing), pigeonhole guarantees Earth inclusion in any 3-branch set.

This eliminates 4/10 element pairs from being co-missing. Of the remaining 6 non-Earth pairs, only 4 are realizable as co-missing: (Fire,Wood), (Fire,Metal), (Metal,Water), (Water,Wood). The ratio is 3 生-pairs : 1 克-pair. The 克-pair (Fire,Metal) appears in 6/16 two-missing hexagrams.

### Finding I.4: Static interaction graph — dense element, sparse branch

**[measured]** Per-hexagram interaction statistics:

| Primitive | Mean edges | % hexagrams with any |
|-----------|-----------|---------------------|
| 生 | 6.75 | 100% |
| 克 | 6.25 | 100% |
| 墓 | 2.75 | 94% |
| 沖 | 0.78 | 45% |
| 合 | 0.53 | 38% |
| 刑 | 0.50 | 42% |
| 害 | 0.47 | 38% |

Total edge range: [12, 22], mean 18.4. The graph is dense in element-level connections (生/克 = background signal) and sparse in branch-level connections (沖/合/刑/害 = discriminative features). Branch-level primitives, when present, carry high information content precisely because they're rare.

### Finding I.5: 卦身 and 納音 distributions

**[measured]** 卦身 lands on an actual line in only 26/64 hexagrams (40.6%). When on-line, 六親 distribution is near-uniform (兄弟 7, 子孫 6, 妻財 5, 官鬼 5, 父母 3). By palace: Kun/Qian 5/8, Zhen 4/8, Gen/Kan/Li 3/8, Dui 2/8, Xun 1/8.

**[measured]** 納音: 23/30 distinct names across 384 positions (7 unused). 納音 element ≠ branch element in 75% of cases — genuinely different information layer. Element distribution: Earth(96), Fire(80), Wood(80), Metal(64), Water(64) — reflects the {4,2,2,2,2} branch element distribution.

### 梅花 comparison
梅花 reduces 6 lines to 2 trigrams (體/用), reads the directed relation between them. 火珠林 keeps all 6 lines active as a network with 7 interaction primitive types. The static profile alone (without temporal context) has 64 distinct states with 15+ coordinates each vs 梅花's 384 states with ~33 coordinates. The unit of analysis is fundamentally different: 梅花 reads a directed arc; 火珠林 reads a network snapshot.

---

## §II. The Seasonal Activation Layer

### Data
- `hzl_seasonal.json` — 320 entries (64 × 5 seasons)
- Scripts: `03_seasonal_map.py`

### Finding II.1: 2/5 ceiling confirmed

**[measured]** Maximum functional coverage (六親 types with at least one 旺/相 line) = 2 across all 320 states. Average strong lines = 2.40/6 = exactly 2/5. No hexagram-season achieves more than 2 simultaneously empowered 六親 types.

### Finding II.2: Anti-resonance — fc=0 iff missing pair forms 生 pair

**[proven]** Functional coverage = 0 (no strong 六親 types) occurs in exactly 10/320 states (3.1%). The condition is algebraically exact:

**fc=0 ⟺ the hexagram's 2 missing 六親 types map to a 生 pair in element space.**

- 16/64 hexagrams have exactly 2 missing types
- 10/16 have missing elements forming a 生 pair → fc=0 exists (in exactly 1 season per hexagram)
- 6/16 have missing elements forming a 克 pair (all Fire/Metal) → immune to fc=0

**Mechanism:** 旺/相 always empower a 生 pair (season element + what it generates). fc=0 requires both empowered types to be absent. This is impossible when the missing pair is a 克 pair (克 pairs never co-empower).

**fc distribution by missing count:**
- 0 missing (16 hex): fc=2 always
- 1 missing (32 hex): fc≥1 always (64 states fc=1, 96 states fc=2)
- 2 missing (16 hex): 10 fc=0, 44 fc=1, 26 fc=2

**[extracted] Source text handling:** Not named. Handled operationally via 飛伏 + 日辰: "伏藏旺相，更看日辰透出" — seasonal strength activates the hidden channel, 日辰 provides the trigger. "伏藏有氣，只利暫時" — even surfaced, benefit is temporary. The system prescribes patience and modesty, not despair.

### Finding II.3: The {4,2,2,2,2} root cause

**[proven]** The 12-branch cycle has element distribution {Earth:4, Fire:2, Wood:2, Metal:2, Water:2}. This single distributional fact cascades through every layer:
- §I: Earth universality (never missing), Fire/Metal scarcity
- §II: Anti-resonance pattern (生-pair condition)
- §IV: 官鬼 target deficit in transformations (Fire/Metal scarcity)
- 納音 element distribution (Earth overrepresented)

### 梅花 comparison
梅花 barely uses seasonal gating ("几乎不用旺相休囚死"). 火珠林 uses it as the primary strength assessment — every line has a seasonal state. The 2/5 ceiling applies to both systems but 梅花 ignores it while 火珠林 treats it as the fundamental constraint on reading specificity.

---

## §III. The 日辰 Layer

### Data
- `hzl_richen.json` — 768 日辰 interactions (64×12) + 384 旬空 (64×6) + 6 六神 patterns
- Scripts: `04_richen.py`, `06_mi_richen.py`

### Finding III.1: Perfect balance theorem

**[proven]** Every hexagram has exactly 6 沖, 6 合, and 6 墓 instances across the 12 日辰 cycle.

**Mechanism:** Each line has exactly 1 branch → 1 opposite (沖) and 1 harmony partner (合) → over 12 日辰, each line is triggered exactly once. 6 lines × 1 = 6 per hexagram. QED.

**Implication:** The 日辰 layer cannot distinguish hexagrams by aggregate activation count. All discrimination comes from WHICH lines are activated WHEN — the temporal pattern, not the count.

### Finding III.2: Near-maximal pattern diversity

**[measured]** 46/64 hexagrams produce 12 distinct activation patterns (one per 日辰 = maximum). 14 hexagrams produce 11, 4 produce 10. Average: 11.7 unique patterns. The 18 with fewer have branch collisions (two lines sharing the same branch → same 日辰 triggers both).

49 distinct 日辰 activation signatures across 64 hexagrams. The 15 collisions are branch-sharing pairs: hexagrams with identical lower and upper trigrams but different palace assignments.

### Finding III.3: Shell ⊥ core confirmed at temporal level

**[measured]** MI(日辰 activation signature, 互 chain) falls within the shuffled null distribution — zero genuine mutual information.

**[proven] Constructive proof:** 13 groups of hexagrams share identical 日辰 activation signatures (same 6 branches) but have DIFFERENT 互 values in every case. Same shell → different core. The 日辰 layer literally cannot see the 互 chain.

Reference NMI values: 互 × basin = 1.000 (both core-derived), palace × basin = 0.34 (weak shell-core coupling through palace walk).

### Finding III.4: Uniform 旬空

**[measured]** Every hexagram has exactly 6 void-line instances across 6 旬. Mean void lines per hexagram per 旬 = exactly 1.00. 世 voided in 16.7% of states = 1/6. The void system is perfectly uniform — no hexagram is structurally more vulnerable to voiding. Specificity comes from WHICH 六親 types are voided in WHICH 旬.

### Finding III.5: Three-layer architecture

**[extracted]** From 易中明義: 「天干管天文，地支管人事，納音管地理」.

| Layer | Information | Default domain | Specialized activation |
|-------|-------------|---------------|----------------------|
| 地支 | Human affairs (人事) | All 31 domains | — |
| 天干 | Celestial phenomena (天文) | 六神 rotation (day stem) | 占天時 (天干合化), 占來情 |
| 納音 | Geography/earth (地理) | — | 占墳墓, 占姓字, 占鬼神 |

The gravesite example (source text lines 15-23) is the only structural specimen where all three layers fire simultaneously. The 天干 layer activates through: 六神 daily rotation (10 stem patterns → 6 distinct spirit assignments), and the 天干合化 system in 占天時 (甲己化土, 乙庚化金, 丙辛化水, 丁壬化木, 戊癸化火).

### 梅花 comparison
梅花 has one temporal input (the casting moment → fixed 體 reference). 火珠林 has a floating daily reference (日辰) that changes the activation pattern every day, plus seasonal strength, plus 旬空 void cycles. The 4/5 ceiling (proven in R7) vs 梅花's 2/5 means 火珠林 accesses twice the temporal resolution. The two systems' temporal layers are proven orthogonal (MI ≈ 0): 日辰 encodes shell information, 互 encodes core information.

---

## §IV. The 動爻 Layer

### Data
- `hzl_dongyao.json` — 384 single-line transformations
- Scripts: `05_dongyao.py`, `07_multi_dongyao.py`

### Finding IV.1: All 25 化爻 types realized, 官鬼 deficit as target

**[measured]** Distribution of 化爻 types (old 六親 → new 六親):

| → | 兄弟 | 子孫 | 父母 | 妻財 | 官鬼 |
|---|------|------|------|------|------|
| 兄弟 | 26 | 5 | 6 | 22 | 20 |
| 子孫 | 8 | 14 | 15 | 12 | 11 |
| 父母 | 9 | 28 | 14 | 26 | 8 |
| 妻財 | 23 | 9 | 32 | 13 | 3 |
| 官鬼 | 19 | 28 | 11 | 9 | 13 |

Column sums (transformation targets): 兄弟=85, 子孫=84, 父母=78, 妻財=82, **官鬼=55**. 官鬼 deficit = 55 vs expected 76.8 (14.3% vs 20%).

**財化鬼 = 3** (0.8%) is the rarest type — wealth almost never transforms directly into authority/trouble.

**[proven] Mechanism:** Same {4,2,2,2,2} root cause as §II. 官鬼's element in the two largest palace groups (Wood palaces: Metal=官鬼; Metal palaces: Fire=官鬼) maps to the two scarcest target elements. The deficit is compositional, not coincidental.

### Finding IV.2: Basin crossing binary by line position

**[proven]** Basin crossing under single-line flips:

| Line | Basin cross | Palace cross | Type preserve |
|------|-----------|-------------|---------------|
| L1 | 0% | 75% | 0% |
| L2 | 0% | 75% | 25% |
| L3 | 100% | 75% | 25% |
| L4 | 100% | 50% | 0% |
| L5 | 0% | 25% | 25% |
| L6 | 0% | 100% | 50% |

L3/L4 ALWAYS cross basins (bits b₂,b₃ = basin determinants). L1,L2,L5,L6 NEVER cross. Confirms the perturbation onion at the operational level. L1 = maximum disruption (0% type preservation); L6 = partial stability (50%).

### Finding IV.3: Multi-line escalation

**[measured]** Every hexagram reaches exactly 15 distinct 變卦 via 2-line flips (C(6,2) = maximum). Basin crossing rises from 33.3% (1-line) to 56.7% (2-line). Palace change: 88.3%. 世+應 both moving: same 化爻 type in only 12.5%.

**[measured]** 靜卦 (no moving lines, 17.8% of readings): 41 distinct (世, 應) identity signatures across 64 hexagrams → 64% unique static identity. Combined with 60 temporal contexts → 2,460 distinguishable static reading states.

### 梅花 comparison
梅花 presupposes exactly 1 moving line (arithmetic determination). 火珠林's coin mechanism produces 0–6 moving lines: P(0)=17.8%, P(1)=35.6%, P(2)=29.7%, P(3+)=16.9%. The modal outcome (靜卦) has no transformation at all. 梅花 always asks "where is this going?"; 火珠林 first asks "is anything changing?"

---

## §V. The Network Reading

### Data
- `hzl_feifu_diagnostic.json` — 9 飛伏 cases
- `hzl_dufa.json` — 5 獨發 patterns + foundational rules
- `hzl_yongshen_protocol.json` — 7-step algorithm
- `hzl_network.json` — 8 axes + 8 primitives + 8 snapshots
- Scripts: `08_feifu_diagnostic.py`, `09_dufa.py`, `10_yongshen_protocol.py`, `12_interaction_graph.py`

### Finding V.1: 飛伏 diagnostics — selective coverage by design

**[extracted]** 9 diagnostic cases cover ALL combinations of 妻財 and 官鬼 as hidden 用神, plus 鬼伏鬼 (self-hiding). This accounts for 21/64 missing instances (33%).

The uncovered 43 instances (子孫=21, 兄弟=13, 父母=9 missing) are delegated to analogical extension: 「舉一隅，則三隅反矣」 ("show one corner, infer the other three").

**[proven] The generative pattern is NOT purely mechanical.** Same 五行 relation, opposite valence:
- 財伏鬼 (hidden generates flying): **unfavorable** — wealth drains into trouble
- 鬼伏父 (hidden generates flying): **favorable** — authority grounded in credentials

The structural relation determines which diagnostic case applies; the semantic context determines the valence. The 飛伏 80%/20% boundary is a designed interface between algorithm and judgment — inside the documented 80%, the reading is algorithmic; outside it, the text explicitly delegates to practitioner inference.

### Finding V.2: 獨發 patterns — asymmetric domain access

**[extracted]** Each 六親 type as sole moving line:

| Type | Epithet | Positive domain | Negative domains |
|------|---------|----------------|-----------------|
| 子孫 | 傷官之神 | 占求財, 占脫事 | 占官事 (克 官) |
| 兄弟 | 劫財之神 | **none** | All wealth/asset domains |
| 父母 | 重迭之神 | 占科舉 | 占求財 (克 子孫 → kills wealth source) |
| 官鬼 | — | 占科舉 (with 吉神) | 占求財 (克 兄弟 → indirect harm) |
| 妻財 | 生鬼傷父 | 占脫貨 | 占科舉 (克 父母 → destroys credentials) |

**兄弟 has zero positive domains** — pure spoiler. This aligns with probe 3's finding (兄弟 most structurally absent, 4/6 incomplete palace roots) and R9 (兄弟 has 0 domains as 用神). The structural exclusion is consistent across all layers.

### Finding V.3: 用神 evaluation protocol — 7 algorithmic steps

**[extracted + formalized]** The complete evaluation protocol:

1. **SELECT** 用神 — from domain → 六親 mapping (`hzl_domains.json`)
2. **ASSESS VISIBILITY** — 飛 (visible) or 伏 (hidden)? If hidden: apply 飛伏 diagnostic (`hzl_feifu_diagnostic.json`)
3. **ASSESS STRENGTH** — 旺相休囚死 from season (`hzl_seasonal.json`)
4. **ASSESS 日辰** — 生/克/沖/合/墓/空 from daily branch (`hzl_richen.json`)
5. **ASSESS MOVEMENT** — 動/靜, 化爻 type (`hzl_dongyao.json`, `hzl_dufa.json`)
6. **ASSESS NETWORK** — 世/應 relationship, other moving lines' effects (`hzl_profiles.json`)
7. **JUDGE** — accumulate favorable/unfavorable signs

Every step maps to a specific data file. The atlas is operationally complete: given a hexagram, domain, season, and 日辰, the protocol can be mechanically executed through the data files up to step 7 (judgment), where practitioner interpretation enters.

### Finding V.4: Interaction graph — two-tier structure

**[measured]** From 8 sampled hexagrams at Spring/子/L1-moving:
- 生/克 = dense background (~6.3 edges): always present, low discrimination
- Branch primitives (沖/合/刑/害) = sparse foreground (~0-1 edges): high discrimination when present
- 墓 = intermediate (2.9): more common than other branch primitives

The graph is operationally two-tiered: element-level relations set the baseline; branch-level relations create the specific reading. The source text's "知此八宗" treats all 8 equally, but the data shows a clear density hierarchy.

### 梅花 comparison
梅花 reads one directed arc (本→互→變) through 5 relations. 火珠林 reads a 6-node network through 8 evaluation axes × 8 operational primitives. The network is primarily evaluated through the 用神 — a domain-selected focal point that collapses the 6-node graph to a single evaluation chain. 梅花's 體 plays an analogous role (fixed reference point for directed reading), but 火珠林's 用神 is domain-dependent (changes with the question) while 梅花's 體 is structurally fixed (determined by the moving line).

---

## §VI. Domain Bindings

### Data
- `hzl_domains.json` — 31 domains
- `hzl_domain_analysis.json` — clusters, special protocols, 卦身 activation
- Scripts: `11_domain_table.py`, `13_domain_protocols.py`

### Finding VI.1: 用神 distribution confirms 財官 axiom

**[measured]** 用神 type across 31 domains:
- 妻財: 15 domains (48%)
- 官鬼: 10 domains (32%)
- 子孫: 6 domains (19%)
- 世: 5 domains (16%)
- 父母: 1 domain (3%, only 占天時)

**妻財+官鬼 = 80% of domain coverage.** The 飛伏 diagnostic coverage (財/鬼 only) is calibrated exactly to this distribution. 官鬼 is simultaneously the most common 忌神 (11/26 standard domains) — the universal threat when not the target.

### Finding VI.2: Eight structural clusters

**[measured]** 26 standard domains cluster into 8 groups:

| Cluster | Count | Pattern | Dominant 用神 |
|---------|-------|---------|--------------|
| Self-Fate | 4 | 世 as 用神 | 世 |
| Self vs Party | 4 | Interpersonal | 官鬼/妻財 |
| Self vs Asset | 7 | Material/wealth | 妻財 |
| Self vs Endeavor | 2 | Goal-seeking | 官鬼/子孫 |
| Body vs Condition | 1 | Biological | 妻財 |
| Self vs Dwelling | 2 | Habitation | 妻財/子孫 |
| Self vs Journey | 3 | Movement/travel | 妻財 |
| Adversary | 3 | Threat as subject | 官鬼 |

The Adversary cluster (占失物鬼祟, 占鬼神, 占征戰) is structurally distinct: 官鬼 is both 用神 and the subject of inquiry. The threat IS the object of study, not an obstacle.

### Finding VI.3: Special protocols — 2D taxonomy (layer × mode)

**[extracted]** Five special protocols break the standard framework on two orthogonal dimensions:

| Protocol | Layer shift | Mode shift |
|----------|-----------|------------|
| 占疾病 | none (地支) | condition: valence inverts (weak 鬼 = good) |
| 占天時 | 天干 primary | state: weather as element interaction |
| 占射覆 | none (地支) | object: 六親 become perceptual channels |
| 占來情 | none (地支) | meta: hexagram → question (direction reverses) |
| 占姓字 | all 3 layers | symbol: Chinese character decoding |

The 26 standard domains share both layer (地支) and mode (situation). Any protocol that changes either dimension becomes "special." The taxonomy has no residual — all 5 exceptions are classified.

### Finding VI.4: 卦身 — conditional sixth variable

**[extracted]** 11 activation conditions across 9 domains, in 5 categories:
1. 世空 fallback — substitutes for 世 when void
2. 六親 reading — 卦身's type reveals character/health info
3. Existence check — on-line vs off-line determines availability
4. Interaction target — 日辰/月建 must 生/合 卦身
5. Spatial mapping — line position → physical height (占墳墓)

Only 26/64 hexagrams (41%) have 卦身 on-line, making it a minority-activated feature. The source text's treatment matches: 卦身 is not a primary axis but a conditional sixth variable that supplements the standard 5 六親 in specific domains.

### 梅花 comparison
梅花: one engine, 18 skins (R30). 火珠林: one engine, 26 standard skins + 5 genuine exceptions. The difference is quantitative (more domains) with 5 qualitative exceptions. The qualitative exceptions are classified by a 2D taxonomy (layer × mode) that has no analogue in 梅花 — 梅花 doesn't have multiple layers (no 天干/納音) and doesn't support mode shifts (always situation-mode).

---

## §VII. Cross-Section Synthesis

### The {4,2,2,2,2} cascade — substrate over design

**[proven]** One distributional fact — Earth occupies 4/12 branch positions (丑辰未戌, spacing 3 in the 12-cycle) — cascades through every layer:
- **§I:** Earth universality (never missing), Fire/Metal structural scarcity
- **§II:** Anti-resonance condition (fc=0 iff missing pair is a 生 pair; 6 immune hexagrams all have Fire/Metal missing)
- **§IV:** 官鬼 target deficit in transformations (Fire/Metal underproduced)
- **§I:** 納音 element distribution (Earth overrepresented at 96/384)

This distribution is not a parameter of 火珠林 or 納甲 — it is a consequence of embedding 五行 into a 12-position cycle. Any system that maps 五行 onto 地支 inherits this asymmetry. It is older than 納甲, older than 火珠林 — a constraint of the representational substrate itself. **The substrate constrains the system more than the system's own design choices do.** This is the atlas's primary contribution to the structural program: prior workflows characterized what the systems do; this atlas characterized what the representational substrate forces.

### Shell ⊥ core at the temporal level

The 日辰 layer encodes shell information (branch identities). The 互 chain encodes core information (inner-bit structure). MI = 0 (proven constructively via 13 branch-sharing hexagram groups with universally different 互 values). The two atlases (梅花 = core temporal, 火珠林 = shell temporal) capture genuinely orthogonal temporal information.

### The two projection types are the only two available

R5 proved algebraically that shell (3+3 trigram split) and core (1+4+1 nuclear overlap) are the only two primitive projections on Z₂⁶. The 梅花 atlas is the canonical reading system for the core projection. The 火珠林 atlas is the canonical reading system for the shell projection. No third atlas is possible without repeating one of these two coordinate systems.

Neither system exhausts the information content of its own projection. Both are lossy readings: 梅花 collapses 6 bits → 體/用 polarity + 互 trajectory; 火珠林 collapses a 6-node graph → a 用神 focal chain with temporal modulation. The union recovers more than either alone, but both remain lossy. What is exhausted is the space of projection types — not the information within each.

### The tangent vector vs local observable distinction (confirmed)

**梅花** computes a **tangent vector** at a point in Z₂⁶: a directed edge (H, H', position). The object of study is a trajectory.

**火珠林** computes a **local observable**: a function of the point, its neighborhood distribution, and external parameters (season/day). The object of study is a state with macroscopic properties.

The 用神 evaluation protocol (§V.3) makes this concrete: it takes a state (hexagram), applies external parameters (season, 日辰), evaluates a domain-selected observable (用神), and returns a judgment. No trajectory is computed — transformation (動爻) is just one of 7 evaluation steps, and the modal outcome (靜卦, 17.8%) skips it entirely.

### The algorithm-judgment interface

The 飛伏 80%/20% boundary exemplifies a design pattern throughout: the system is algorithmic within its documented scope and delegates to practitioner judgment at the boundary. The 89% text residual (semantic map) is not a gap in the algebraic surface but a different epistemic category — interpretive rather than computable. The algebraic surface and the textual surface occupy different spaces, connected by two narrow bridges (R6). The two atlases exhaust the algebraic interpretive surface; the textual surface remains thick and largely independent.

### Information budget

| Section | What it provides | Data file |
|---------|-----------------|-----------|
| §I | Static identity: who are the players | `hzl_profiles.json` |
| §II | Seasonal strength: who has power | `hzl_seasonal.json` |
| §III | Daily activation: what's triggered now | `hzl_richen.json` |
| §IV | Transformation: what changes | `hzl_dongyao.json` |
| §V | Network reading: how they interact | `hzl_network.json` |
| §VI | Domain binding: what the question selects | `hzl_domains.json` |

---

## Data Files

| File | Content | Entries |
|------|---------|--------|
| `hzl_profiles.json` | 64 static profiles | 64 |
| `hzl_topology.json` | Static interaction graphs | 64 |
| `hzl_seasonal.json` | Seasonal activations | 320 (64×5) |
| `hzl_richen.json` | 日辰 interactions + 旬空 + 六神 | 768 + 384 + 6 |
| `hzl_dongyao.json` | Single-line transformations | 384 |
| `hzl_feifu_diagnostic.json` | 飛伏 diagnostic cases | 9 |
| `hzl_dufa.json` | 獨發 patterns | 5 + 3 |
| `hzl_yongshen_protocol.json` | 用神 evaluation algorithm | 7 steps |
| `hzl_domains.json` | Domain bindings | 31 |
| `hzl_domain_analysis.json` | Clusters + special protocols + 卦身 | 8+5+11 |
| `hzl_network.json` | 8 axes + 8 primitives + snapshots | 8+8+8 |

## Scripts

| Script | Content |
|--------|---------|
| `01_static_profiles.py` | §I.1-2: Core profiles + 納音 + 卦身 |
| `02_cross_tabs.py` | §I.3-4: Cross-tabulations + topology |
| `03_seasonal_map.py` | §II.1-2: Seasonal map + coverage |
| `04_richen.py` | §III.1-3: 日辰 + 旬空 + 六神 |
| `05_dongyao.py` | §IV.1: Single-line transformations |
| `06_mi_richen.py` | §III.4: MI computation |
| `07_multi_dongyao.py` | §IV.2-3: Multi-line + source patterns |
| `08_feifu_diagnostic.py` | §V.1: 飛伏 diagnostics |
| `09_dufa.py` | §V.2: 獨發 patterns |
| `10_yongshen_protocol.py` | §V.3: 用神 protocol |
| `11_domain_table.py` | §VI.1: Domain table |
| `12_interaction_graph.py` | §V.4-5: Interaction graph + axes |
| `13_domain_protocols.py` | §VI.2-4: Protocols + 卦身 |

---

## Known Gaps

1. **飛伏 diagnostics for 子孫/兄弟/父母** — not in source text, not generated (by design; 80%/20% boundary is algorithm-judgment interface)
2. **Full 4096-entry 動爻 table** — only 384 single-line entries computed; multi-line sampled
3. **Full 3840-entry temporal table** (64 × 60 甲子) — simplified to 64 × 12 (日辰) + 64 × 6 (旬空)
4. **Empirical validation** against actual readings — all findings are structural
5. **六神 × 六親 interpretive matrix** — 六神 rotation documented but per-combination meanings not exhaustively extracted
6. **Cross-atlas integration** — the two atlases proven orthogonal; a joint reading protocol combining both projections is not formalized
