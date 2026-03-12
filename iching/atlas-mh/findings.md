# 梅花 Atlas — Findings

> The 梅花易數 interpretive framework projected onto the 384-state space (64 hexagrams × 6 動爻 positions).
> All statistics are exhaustive enumerations, not samples. p-values test structural hypotheses against null distributions.

**Epistemological key:** Each finding is marked:
- **[proven]** — algebraically necessary, follows from definitions
- **[measured]** — exhaustive enumeration over the 384-state space
- **[conjectured]** — interpretive inference from data + tradition

---

## §I. The 384-State Table

### Data
- `mh_states.json` — 384 entries, 33 fields per state
- Scripts: `01_mh_states.py`, `02_derived.py`, `03_torus_arcs.py`
- Validated against `atlas/transitions.json` and `atlas/atlas.json`

### Finding I.1: ti_hu 克-dominance

**[measured]** The 互 trigram on 體's side overwhelmingly produces 克 relationships:

| Relation | ti_hu | yong_hu | ben (baseline) |
|---|---|---|---|
| 比和 | 94 (24.5%) | 90 (23.4%) | 84 (21.9%) |
| 克体 | 121 (31.5%) | 87 (22.7%) | 78 (20.3%) |
| 体克用 | 121 (31.5%) | 87 (22.7%) | 78 (20.3%) |
| 生体 | 24 (6.3%) | 60 (15.6%) | 72 (18.8%) |
| 体生用 | 24 (6.3%) | 60 (15.6%) | 72 (18.8%) |

**63% adversarial (克+体克) vs 12.5% favorable (生+体生) at ti_hu.** At hexagram level: 40/64 have 克 between trigram and its same-side nuclear, only 8/64 have 生.

**[proven] Mechanism:** The nuclear trigram shares 2 of 3 bits with its parent trigram. The 五行 map through the parity structure (b₀⊕b₁) tends to produce 克 (parity-breaking) rather than 生 (parity-preserving). This is the L2/L5 asymmetry from the atlas perturbation onion manifesting at the interpretation level.

**[conjectured] Interpretive implication:** "体互最紧" is an information-weighting claim, not a favorability claim. The position with highest adversarial bias is where favorable signals carry the most discriminative power — finding 生体 at ti_hu (12.5%) is high-information precisely because it's rare. The tradition's emphasis is informationally calibrated.

### Finding I.2: ti_hu × yong_hu structural coupling

**[proven]** The two nuclear positions are NOT independent — they derive from the same 4-bit inner value (lines 2-5). Forbidden pairs exist:

| | 比和 | 生体 | 体生用 | 克体 | 体克用 |
|---|---|---|---|---|---|
| **比和** | 42 | **0** | **0** | 26 | 26 |
| **生体** | **0** | 0 | 6 | **0** | 18 |
| **体生用** | **0** | 6 | 0 | 18 | **0** |
| **克体** | 24 | 6 | 48 | 24 | 19 |
| **体克用** | 24 | 48 | 6 | 19 | 24 |

When one nuclear trigram generates 體, the other cannot be same-element as 體 (比和). The 互 layer is one structured signal with asymmetric access, not two independent channels. Positions 2-3 of the relation vector form a coupled pair: [ben, (ti_hu, yong_hu), bian].

### Finding I.3: 183/625 relation vectors realized (29.3%)

**[measured]** 70% of the 4-step arc space is algebraically forbidden. Constraints cascade:
1. ti_hu 克-bias eliminates 生-heavy vectors
2. ti_hu × yong_hu coupling eliminates independent combinations
3. ben × bian follows the atlas surface relation transition matrix

### 乾坤无互 exception

**[proven]** 12/384 states (hex 0 and hex 63, lines 1-6) correctly routed via 變卦's 互. Lines 2-5 of each produce genuinely different 互 data (動爻-dependent 互). Lines 1 and 6 map back to parent in some cases (e.g., 坤 line 1: bian=1, hu(1)=0=坤).

---

## §II. 梅花 Torus

### Data
- `mh_torus_flow.json` — 25 cells, per-cell flow data
- Script: `03_torus_arcs.py`

### Finding II.1: Maximally multi-valued 互 mapping

**[measured]** 梅花 torus: **2/25 well-defined** (Fire,Water and Water,Fire) vs atlas's **8/25**.

The 梅花 torus is more multi-valued because each hexagram appears in 6 states (one per moving line), each potentially routing to different 互 targets. The atlas maps a single hexagram to a single 互; 梅花 maps a (hexagram, line) pair, so multiple lines of the same hexagram disperse across different 互 destinations.

**[proven]** The only well-defined cells (Fire,Water) and (Water,Fire) are singleton-element pairs with unique trigram representations (Kan and Li), so all states in those cells route identically.

### Finding II.2: Population follows {2,2,2,1,1} partition

**[proven]**

| 體 element | Trigram count | States as 體 |
|---|---|---|
| Wood | 2 (Zhen, Xun) | 96 |
| Fire | 1 (Li) | 48 |
| Earth | 2 (Gen, Kun) | 96 |
| Metal | 2 (Qian, Dui) | 96 |
| Water | 1 (Kan) | 48 |

The 24:12:6 population gradient across torus cells directly mirrors the trigram-element partition. Diagonal cells (比和) show the clearest gradient: (Earth,Earth) = 24, (Fire,Fire) = 6.

### Finding II.3: Wood,Wood reaches 6 互 targets (maximum)

**[measured]** The (Wood,Wood) cell has the highest 互 indeterminacy. Wood's two trigrams (Zhen=001, Xun=110) are maximally distant (Hamming 3), so their nuclear trigrams span more of the element space. This connects to Wood's maximal XOR mask coverage from the atlas cycle algebra findings.

---

## §III. Arc Classification

### Data
- `mh_arcs.json` — arc type distribution and per-type vector lists
- Script: `03_torus_arcs.py`

### Finding III.1: Arc symmetry with basin dependence

**[measured]**

| Arc type | Count | % |
|---|---|---|
| stable_neutral | 6 | 1.6% |
| rescued | 56 | 14.6% |
| betrayed | 56 | 14.6% |
| improving | 52 | 13.5% |
| deteriorating | 52 | 13.5% |
| stable_favorable | 47 | 12.2% |
| stable_unfavorable | 48 | 12.5% |
| mixed | 67 | 17.4% |

Perfect symmetry: rescued/betrayed = 56/56, improving/deteriorating = 52/52, stable_favorable/stable_unfavorable = 47/48. The 五行 生克 structure generates equal positive and negative trajectories.

**Basin dependence (χ² = 38.09, df=14, p < 0.001):** Cycle basin concentrates in mixed (51/67 = 76.1%). Mixed is the largest single arc type at 17.4%. Cycle basin → 26.6% mixed vs Kun/Qian → 8.3% mixed. This is structurally driven: Cycle hexagrams have more varied nuclear trigrams, creating cross-currents in the 互 layer.

**Mixed has the lowest 凶 rate: 5/67 = 7.5%.** Cross-cutting 互 signals reduce textual adversity. Stable_neutral (all 比和) has 0/6 吉 and 2/6 凶 (33.3%) — the all-harmonious arc is textually unfavorable.

### Finding III.2: ben_relation → arc_type structural constraints

**[proven]** The arc type is partially determined by ben_relation:

| Arc type | 生体 | 体克用 | 比和 | 体生用 | 克体 |
|---|---|---|---|---|---|
| stable_neutral | 0 | 0 | 6 | 0 | 0 |
| rescued | 0 | 0 | 0 | 30 | 26 |
| betrayed | 30 | 26 | 0 | 0 | 0 |
| improving | 0 | 18 | 34 | 0 | 0 |
| deteriorating | 0 | 0 | 34 | 18 | 0 |
| stable_favorable | 26 | 21 | 0 | 0 | 0 |
| stable_unfavorable | 0 | 0 | 0 | 13 | 35 |
| mixed | 16 | 13 | 10 | 11 | 17 |

Key constraints:
- **stable_neutral** only from 比和 (requires all four positions = 比和)
- **rescued** only from negative 本 (体生用 or 克体)
- **betrayed** only from positive 本 (生体 or 体克用)
- **比和-at-本** is locked to improving/deteriorating/stable_neutral/mixed (no rescued/betrayed possible from valence=0 starting point)

### Finding III.3: Two-channel architecture

**[measured]** The 爻辭 (line texts) track **present state** (ben_relation), not trajectory:

| ben_relation | 吉 rate | 凶 rate |
|---|---|---|
| 生体 | 44.4% | 6.9% |
| 体克用 | 29.5% | 16.7% |
| 比和 | 22.6% | 20.2% |
| 体生用 | 31.9% | 8.3% |
| 克体 | 26.9% | 14.1% |

吉 rate peaks at 生体-at-本 (44.4%), consistent with favorable present state. 凶 rate peaks at 比和-at-本 (20.2%). Neither marker tracks the arc trajectory — they are snapshots, not predictions.

**"Betrayed" paradox resolved:** States classified as "betrayed" (positive 本, negative 變) can still carry 吉 markers. 吉 marks the favorable present state, not the outcome. The 先天 method, which drops 爻辭 entirely ("止以卦論"), avoids this channel mismatch.

**[conjectured]** This is not a mismatch but two parallel channels by design. Vol 2 prescribes a sequential multi-track evaluation: (1) 爻辭 (present state), (2) 體/用 生克 (trajectory), (3) external omens, (4) observer state. The 爻辭 do their original job even inside 梅花's later framework.

### Finding III.4: 比和 discrepancy

**[measured]** 比和-at-本 states (84/384) show elevated 凶 rate (20.2%) vs non-比和 (11.7%), with residual beyond basin confound:

| Basin | 比和-本 凶 | non-比和 凶 |
|---|---|---|
| Kun | 29.2% (7/24) | 18.1% (13/72) |
| Qian | 25.0% (6/24) | 19.4% (14/72) |
| Cycle | 11.1% (4/36) | 5.1% (8/156) |

The elevation persists within each basin: 比和 → 凶 is not purely a basin artifact. Small within-basin samples prevent definitive statistical closure, but the direction is consistent across all three basins.

**[conjectured]** The tradition's "百事順遂" (vol 2) is scoped to 体用 only — not the full arc. The textual tradition penalizes states where no dynamic force acts. The 西林寺 example provides the theoretical warrant: pure harmony can mask structural contradiction.

### Finding III.5: All arc types realized

**[measured]** All 8 arc types are populated. 183 realized relation vectors distribute across:

| Arc type | Distinct vectors |
|---|---|
| stable_neutral | 1 |
| rescued | 30 |
| betrayed | 30 |
| improving | 27 |
| deteriorating | 28 |
| stable_favorable | 17 |
| stable_unfavorable | 17 |
| mixed | 33 |

No arc type is algebraically impossible. The rescued/betrayed symmetry (30/30 vectors) and stable symmetry (17/17 vectors) extend from state counts to vector counts.

### Finding III.6: 互 amplifier effect confirmed

**[measured]** When ti_hu's direction agrees with 本's direction (both favorable or both adversarial), 變 follows 本's direction in 48.0% of cases. When ti_hu disagrees with 本, 變 follows only 32.0%. Fisher exact test: **OR=1.96, p=0.007**.

The tradition's claim that 互 amplifies or dampens the reading is statistically confirmed — 互 genuinely predicts whether the outcome reinforces or reverses the starting condition. **[proven]** The amplifier operates through positional coupling: 互 and 變 share structural constraints (both depend on the inner 4 bits), so 互's direction is a noisy but real predictor of 變's direction.

---

## §IV. Temporal Layer

### Data
- `mh_temporal.json` — reachability, distribution, seasonal cross-tabs
- Script: `04_temporal.py`

### Finding IV.1: 先天 parity wall — exactly 192/384 reachable

**[proven]** The 先天 (calendar-based) casting formula has a **hard parity constraint**:
- Lower trigram = total mod 8 → determines bit 0 of hex_val
- Line = (total mod 6) + 1 → parity determined by total mod 2

Since total determines both lower trigram and line, and both depend on total's parity:
- Even total → even lower trigram → odd lines only (1, 3, 5)
- Odd total → odd lower trigram → even lines only (2, 4, 6)

**Every hexagram reaches exactly 3 of 6 lines.** No hexagram achieves full line coverage. The 先天 method structurally cannot access half the 384-state space.

**[measured] Input distribution:** 288 total (S mod 24 × hour) inputs. 96 states get 1 input, 96 get 2 inputs, 192 get 0. Per-line distribution is perfectly uniform (48 inputs per line position).

**Implication:** The 後天 (perception-based) casting methods are required for full 384-state coverage. 先天 accesses a 192-state subspace with a clean parity structure. 先天 and 後天 literally operate in different (overlapping) state spaces.

### Finding IV.2: Seasonal bias is structural, not seasonal

**[proven]** Arc_valence and arc_type are fixed properties of each (hex, line) state. Seasons don't change which arcs exist — they change the **strength overlay** (旺相休囚死) applied to 體.

When 體's element is seasonally 旺, 體 has maximum resilience regardless of arc direction. When 體 is 死, even favorable arcs may be insufficient. Seasons modulate the **magnitude** of the arc effect, not its **direction**. The structure is: season × arc_type → outcome_strength, not season → arc_type.

The seasonal 體 distribution across elements is fixed (determined by the {2,2,2,1,1} trigram partition), so no season systematically favors or disfavors 體. The 2/5 ceiling (only 2 of 5 elements are 旺/相 in any season) applies equally to all arc types.

### Finding IV.3: Parity wall selects for arc-level favorability

**[measured]** The 先天 reachable half (192 states) is NOT arc-neutral:

| Arc type | Reachable | Unreachable |
|---|---|---|
| stable_favorable | **34** | 13 |
| stable_unfavorable | 16 | **32** |
| rescued | 26 | 30 |
| betrayed | 30 | 26 |
| mixed | 34 | 33 |
| improving | 23 | 29 |
| deteriorating | 26 | 26 |
| stable_neutral | 3 | 3 |

stable_favorable vs stable_unfavorable by reachability: **OR=5.23, p=0.0002**. Full χ²=16.0 (df=7, p=0.025) across all arc types.

Yet **valence markers are balanced**: 吉=30.7% in both halves, 凶=15.1% reachable vs 12.0% unreachable (not significant). Basin distribution is perfectly symmetric (48/96/48 each half).

**[measured]** The parity wall filters the arc channel (trajectory) but not the text channel (present state). Since 先天 drops the text channel entirely, the arc bias IS the operative effect for 先天 readings — 先天 has a structurally optimistic arc space with no countervailing text channel.

**[conjectured]** The arc bias is an emergent consequence of mod arithmetic, likely third-order (mod structure → parity wall → line selection → arc enrichment). No evidence Shao Yong computed the 384-state distribution. The tradition may have noticed the effect empirically and attributed it to metaphysical priority ("辞前之易").

---

## §V. Semantic Bindings

### Data
- `mh_domains.json` — 18 application domains
- `mh_channels.json` — 十應 channels, inversion rule, 向背
- `mh_timing.json` — 克應之期 timing formula
- `mh_two_channel.json` — two-channel architecture
- Script: `05_semantic.py`

### Finding V.1: Two-channel architecture

**[measured + conjectured]** 梅花 operates with two independent information channels:

| Channel | Source | Encodes | Used in |
|---|---|---|---|
| Text | 爻辭 | Present state snapshot | 後天 only |
| Arc | 體/用 生克 | Trajectory (本→互→變) | 先天 + 後天 |

先天 explicitly drops the text channel ("止以卦論，不甚用《易》之爻辭"). 後天 uses both, with arc primary and text supporting. When channels disagree, the practitioner exercises judgment — the system acknowledges that no mechanical rule resolves all conflicts ("详审卦辞...要在圆机，不可执").

The 18 domain templates and 10 response channels operate on the arc layer. The 爻辭 remain a separate input. When both channels agree, confidence is high ("俱吉则大吉；俱凶则大凶").

### Finding V.2: 先天/後天 structural difference

**[proven]** Beyond the channel count difference:

| Dimension | 先天 | 後天 |
|---|---|---|
| State space | 192/384 (parity-constrained) | All 384 |
| Channels | Arc only | Arc + text |
| Arc bias | Enriched for stable_favorable (OR=5.23) | No structural bias |
| Text access | None ("止以卦論") | 爻辭 at 本 position |

先天 and 後天 are structurally complementary: different state spaces, different channel counts, different arc distributions. 後天's text channel leaks core-layer information (凶×basin through 爻辭) that 先天 cannot access. 先天 is confined to the shell projection.

### Finding V.3: Timing formula formalized

**[extracted from vol 3]** 克應之期 = base_number × observer_modifier, unit by event type.

- **Arc position** determines speed: 本生体 = immediate (即成), 互生体 = gradual (渐成), 變生体 = slow (稍迟)
- **Observer state** scales: walking ×0.5, standing ×1.0, sitting ×2.0
- **Unit** is practitioner judgment (days/months/years)

The timing formula is partially mechanical (number + modifier) and partially interpretive (unit selection). This matches the system's general principle: "推數又須明理" — computation narrows, reason selects.

### Finding V.4: Cross-domain taxonomy — one engine, 18 skins

**[proven]** All 17 體/用 domains follow the identical 5-relation evaluation template. No domain modifies the 生克 logic itself. Domain-specific content enters only through: (1) semantic binding (what 體 and 用 represent), (2) trigram imagery (what the 8 trigrams mean in this context), (3) optional sub-systems (present in 3 domains only).

**Six structural clusters:**

| Cluster | Domains | Pattern |
|---|---|---|
| Self vs other party | 婚姻, 謁見, 官訟 | 體=self, 用=person. Trigram 象 characterizes the other. |
| Self vs asset | 屋舍, 求財, 交易, 失物 | 體=self, 用=material object. 生克 reads acquisition/loss. |
| Self vs endeavor | 人事, 求謀, 求名, 出行 | 體=self, 用=abstract goal. 生克 reads feasibility. |
| Body vs condition | 生產, 疾病 | 體=physical body, 用=biological process. Sub-systems present. |
| Self vs dwelling | 家宅, 屋舍, 墳墓 | 體=self/descendants, 用=location. 生克 reads fortune of habitation. |
| Self vs absent | 行人 | Unique: 用卦 dual-reads (return probability AND condition abroad). |

**Domains with unique features beyond the standard template:**
- 婚姻: 8 trigram appearance types for spouse
- 生產: 陰/陽 爻 counting for gender
- 飲食: 坎=wine, 兌=food presence test; 互卦 for companions
- 出行: movement trigrams (乾震=go, 坤艮=stay, 巽=boat, 離=land)
- 行人: 用卦 dual reading (return + condition)
- 失物: 變卦 as spatial compass (8 directions with detailed locations)
- 疾病: 3 sub-systems (prognosis, pharmacology, spirit diagnosis)

**Key insight:** The text says "庶務之多，豈止十八占而已乎！此十八占，乃大事之切要者，占者以類而推之可也" — the 18 are exemplars, not exhaustive. The practitioner extends by analogy. The system is one template with parameterized bindings, not 18 separate procedures.

### Finding V.5: Extractability boundary

| Extractable (formalized) | Context-only (not formalizable) |
|---|---|
| Channel → element mapping (algebraic channels) | 三要 framework (perceptual cultivation) |
| Inversion priority (hexagram > omens) | 真生真克 intensity gradient |
| 向背 sign modifier (temporal arrow) | 心易 anti-literalism |
| 静占 degradation (drop perceptual channels) | Practitioner judgment in unit/context |

The boundary is where computation ends and cultivation begins. The algebraic core (channels 1-3) is fully formalized. The perceptual channels (5-10) require 三要 — a trained perceptual faculty that operates in "虛靈" (empty sensitivity). The system deliberately places this boundary.

---

## §VI. Synthesis — How 梅花 Atlas Relates to the Static Atlas

### Bridge 1: ti_hu 克-dominance = perturbation onion at interpretation level

The atlas perturbation onion showed that L2/L5 (nuclear lines) have asymmetric element-change behavior. The ti_hu 克-dominance (63% adversarial) is this same asymmetry appearing in the 梅花 interpretive layer. The nuclear trigram's 2-bit overlap with its parent trigram structurally favors 克 over 生. This is not a design choice — it's a mathematical consequence of the bit-sharing architecture.

### Bridge 2: Mixed → Cycle basin mechanism

Mixed arc type concentrates in Cycle basin (76.1% of mixed states are Cycle). Cycle hexagrams have the most varied nuclear trigrams (higher 互 indeterminacy), which creates cross-currents in the relation vector. This connects to the atlas finding that Cycle basin has the most diverse 互 cell targets. Mixed also has the lowest 凶 rate (7.5%) — the cross-cutting 互 signals, while creating interpretive complexity, reduce textual adversity. This is the mechanism behind the synthesis finding that Cycle basin has lowest 凶 (6.3%).

### Bridge 3: 吉 × 生体 at 本

The synthesis finding that 吉 correlates with favorable 本-state is confirmed at the 384-state level: 生体-at-本 has 44.4% 吉 rate, the highest of any ben_relation. But this correlation is with present state, not trajectory — betrayed states (positive 本, negative 變) can carry 吉. The two-channel architecture explains this: the text channel and arc channel encode different information.

### Bridge 4: 比和 residual

比和-at-本 凶 elevation (20.2% vs 11.7%) persists within each basin (Kun 29.2% vs 18.1%, Qian 25.0% vs 19.4%, Cycle 11.1% vs 5.1%). Partially but not fully explained by basin confound. The residual suggests the 爻辭 tradition encodes a principle beyond pure 五行 structure: stasis (比和) is textually penalized relative to dynamic states.

### Bridge 5: 先天 parity wall and the 後天 rationale

The 先天 method's parity wall (192/384 reachable) provides a structural rationale for the 後天 method's existence. If 先天 could reach all 384 states, 後天 would be redundant. The parity constraint means 先天 systematically cannot access half the state space — specifically, the half where lower trigram parity and line parity disagree. 後天 methods, which derive trigrams from perception rather than arithmetic, are not subject to this constraint. The two methods are structurally complementary, not just philosophically distinct.

### The deepest structural finding: temporal = depth-stratified evaluation

The 梅花 arc is not physical time. It is the hexagram's multi-layer profile (surface → core → perturbation response) read directionally because 體 provides an orientation. Without 體, the 互 and 變 are symmetric transformations with no preferred direction. With 體, they become a narrative: "this is where I stand (本), this is the hidden structure (互), this is what changes produce (變)."

The 體/用 cut is the generative step — it converts static algebra into directed reading. The temporal language is a representation of structural depth, which the tradition renders as narrative because narrative is how humans process multi-step dependency.

The atlas sees the hexagram as a static coordinate (surface cell, 互 cell, basin, depth). 梅花 sees the same hexagram as one frame in a 4-step arc, with 體 as the fixed reference point. The 動爻 breaks the hexagram's symmetry, creating a directed reading. The 384-state expansion (64×6) is the cost of this directionality. What 梅花 gains is trajectory structure — improving, deteriorating, rescued, betrayed — categories that don't exist at the hexagram level.

---

## Known Gaps

This atlas does NOT contain:

1. **火珠林 operational projection.** The other major divination system uses 六親 × 日辰 activation (a time-dependent 五行 overlay) with a floating daily reference, vs 梅花's fixed 體 reference. A third atlas would be needed.

2. **Character divination (vols 4-5).** Different front-end (字 → trigram decomposition), same 體/用 back-end. Deferred by design.

3. **Semantic content of 爻辭 beyond valence markers.** The atlas proved (synthesis) that embeddings don't predict line text content from algebraic coordinates, suggesting this may be inherently non-algebraic.

4. **真生真克 intensity gradient.** The distinction between 真火 and 形色之火 requires perceptual typing of instances — not computable from the algebraic structure.

5. **三要 perceptual framework.** The trained perceptual faculty that selects which of the 10 response channels to activate is documented as context but not formalized as data.

6. **Empirical validation against actual 梅花 readings.** All findings are structural (what the algebra permits/requires), not predictive (what happens when practitioners use the system).

7. **後天 distributional analysis.** The specific distribution across 384 states for each 後天 method (object counting, character decomposition, etc.) is not computed — only the structural fact that 後天 can reach all 384 states.
