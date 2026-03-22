# TCM Study — Exploration Log

---

## Iteration 1: 梅花易數 Medical Domain Extraction

**Task:** Extract and formalize the 疾病占 (illness divination) rules from 梅花易數 vols 2–4. Understand what TCM-like structure already exists inside the 梅花 framework before studying external TCM sources.

**Sources read:** vol2 lines 90–94 (疾病占第十六), vol3 lines 116–120 (verse summary), vol3 lines 205–223 (trigram correspondences), vol4 lines 328–333 (character-divination disease layer).

**Output:** `memories/iching/tcm/meihua_medical.md` — structured extraction document.

### What was found

**A. Prognosis rules [measured]:** The standard 5-relation template (体克用→easy recovery, 用克体→medicine useless, 体生用→lingering, 用生体→quick recovery, 比和→easy recovery) applies to illness identically to all 18 domains. Three illness-specific additions were identified:

1. **旺/衰 as life/death discriminator** — When 體 is克'd and seasonally 旺, "犹为庶几" (still hope). When 體 is克'd and seasonally 衰, "断无存日" (certain death). No other domain uses 旺/衰 as a binary life/death gate. Other domains use it for degree.

2. **Rescue signal (凶中有救)** — When 克体 is present, scan 互 and 變 positions for any 生体 trigram. If present → rescue possible. If absent → hopeless. Partially present in the general system but formalized as critical only in illness.

3. **Dual timing** — Recovery date (和平之日) determined by 主卦; crisis/death date (危厄之期) determined by 克体之卦's element timing. Other domains use a single timing formula (克應之期).

**B. Pharmacology sub-system [measured]:** Maps 生体 trigram → drug thermal quality. Five mappings extracted:

| 生体 trigram | Medicine type | Via 五行? |
|---|---|---|
| 离 (Fire) | 热药 (hot) | ✓ Direct |
| 坎 (Water) | 冷药 (cold) | ✓ Direct |
| 艮/坤 (Earth) | 温补 (warm tonics) | ✗ TCM-specific |
| 乾/兑 (Metal) | 凉药 (cooling) | Partial |
| 震/巽 (Wood) | absent | — |

Key finding: the mapping operates at **element level**, not individual trigram level. Vol2 says 艮 for warm tonics; vol3 says 坤. Both are Earth. The system does not distinguish between same-element trigrams for pharmacology.

**C. Spirit diagnosis sub-system [measured]:** Full 8-trigram mapping extracted. Triggered when 克体 trigram exists. Each trigram → specific spirit/ghost type. The mapping is **象 (image) driven, not 五行 driven** — each spirit type is a narrative extension of trigram imagery (巽=Wind/rope → hanging/shackles; 兑=Lake/sharp → blade deaths; etc.). This sub-system adds information that 五行 alone cannot derive.

**D. Body part mapping [measured]:** Two parallel systems identified:

- **說卦 spatial** (trigram → body region): 乾=head, 坤=abdomen, 震=foot, 巽=thigh, 坎=ear+blood, 离=eye, 艮=hand/fingers, 兑=mouth/teeth
- **TCM functional** (五行 → organ): Metal=lung, Earth=spleen, Wood=liver, Water=kidney, Fire=heart

These mostly disagree (乾=head ≠ Metal=lung). They converge only where TCM explicitly bridges (坎=ear because "kidney opens to ear"). The 梅花 illness section uses the 說卦 system for disease **localization** (where does it hurt?) and the 五行 system for disease **mechanism** (which organ system is dysfunctional?). The tradition holds both in parallel without reducing one to the other.

**E. Worked example (否 hexagram, 6 moving lines) [measured]:** Shao Yong walks through all 6 lines of 乾上坤下 for illness prognosis: 3 吉, 2 死, 1 危. 體 flips at the trigram boundary (lines 1-3: 体=Metal; lines 4-6: 体=Earth). 動爻 position is the primary discriminator.

### Methodological discovery: 互 computed from 變卦

**[measured]** In the worked example, Shao Yong computes 互 (nuclear trigrams) from the **變卦** (transformed hexagram), not the **本卦** (original). Computationally verified for line 2 of 否 (本卦互=艮/巽, 變卦互=离/巽, Shao says 巽/离 → matches 變卦).

**Status:** Flagged for cross-example verification in Iteration 2.

### Structural finding: 疾病 is the richest domain

**[measured]** Of 18 梅花 domains, only 3 have sub-systems beyond the standard template. 疾病 has 3 sub-systems (pharmacology, spirit diagnosis, body localization) + 2 structural escalations (旺/衰 life/death binary, dual timing). No other domain approaches this density.

### Conjectures generated

1. **Three-mechanisms hypothesis [conjectured]:** The 八纲's three axes may each connect to the trigram system through a different mechanism — 寒/热 via element correspondence, 表/里 via positional structure, 虚/实 via temporal modulation. If so, there is no single Q₃ → 八纲 bijection.

2. **S₃ symmetry splits into two levels [conjectured]:** The three 八纲 axes may be symmetric *as clinical measurements* while being asymmetric *as mapped through the I Ching*. If the Z₅ grammar operates at the clinical-measurement level, the mapping asymmetry doesn't kill it.

3. **Pharmacology as partial anchor for 八纲 寒/热 axis [conjectured]:** The pharmacology maps 生体 element → drug thermal quality. Through the treatment-reversal principle, this partially assigns the 寒/热 axis to 五行 elements. Scope limitation: mapping is therapeutic, not constitutional.

---

## Iteration 2: 互 Resolution + 黃帝內經 Extraction

**Tasks:** (A) Check all 梅花 worked examples for 互(本) vs 互(變). (B) Read 黃帝內經 key chapters for T1 (八纲 definition) and T2 (axis independence).

**Sources read:** (A) All worked examples with named 互 trigrams in 梅花 vols 2-3. (B) suwen_02 (ch.5 陰陽應象大論), suwen_08 (ch.28 通評虛實論, ch.29 太陰陽明論), suwen_09 (ch.31 熱論, ch.32 刺熱論), lingshu_11 (ch.73 官能, ch.77 九宮八風).

**Outputs:** Section G appended to `meihua_medical.md`, new file `neijing_extract.md`.

### Task A Results: 互(本) vs 互(變) — RESOLVED

**[measured]** 10 worked examples checked. 6 decisive cases (where 互(本) ≠ 互(變)):
- 5 match 互(本): vol3 lines 18, 24; vol2 lines 233, 234, 235
- 1 matches 互(變): vol2 line 94 (the illness example)

**Verdict: 互(本) is standard practice (5:1).** The illness example is the sole exception — most likely a textual error (艮↔离 swap) or pedagogical artifact. The atlas-mh framework's assumption is confirmed.

### Task B Results: 黃帝內經 八纲 Extraction

**T1 answered [measured]:** The 內經 does NOT name 八纲辨证 as a framework (term absent from text). It provides the three binary pairs as clinical concepts:
- 寒/热: defined as 陰/陽 excess (Suwen 5: "陽勝則熱，陰勝則寒")
- 虚/实: defined as vital qi depletion / pathogen dominance (Suwen 28: "邪氣盛則實，精氣奪則虛")
- 表/里: defined as disease location depth (Suwen 31: six-channel progression model)

The full 八纲 formulation was codified later (Ming-Qing era systematizers).

**T2 answered [measured]:** The three axes are **correlated, not independent.** All three map onto the single 陰/陽 meta-axis:
- 表=陽, 里=陰
- 热=陽, 寒=陰
- 实=陽, 虚=陰

Strong default associations exist: 热-实-表 cluster, 寒-虚-里 cluster. Mixed states are clinically documented but less common. The text is explicit about the hierarchy: "善診者...先別陰陽" — first distinguish yin from yang, then subdivide. The three axes are subdivisions of one distinction, not three independent dimensions.

**T5 partially answered [measured]:** The only 內經 chapter mapping trigrams to medicine is 靈樞 ch.77 九宮八風, which maps trigrams to organs via directional winds and temporal 太一 position — a cosmological framework, not a clinical diagnostic system. No text maps 八纲 poles to trigram bits. Such a mapping would be an invention, not a discovery.

### Additional findings from the 內經

**1. 虚/实 is not a simple binary [measured]:** The 內經 documents 重虚, 重实, and mixed states (經虛絡滿) where different body regions have opposite 虚/实 simultaneously. It's a force-balance ratio, not a switch.

**2. 表/里 is sequential, not binary [measured]:** The 熱論 six-day model shows disease progressing through six channels from 表→里 (太陽→陽明→少陽→太陰→少陰→厥陰). It's a depth gradient. The 兩感 (simultaneous 表+里 attack) is the lethal exception variant. Imposing a binary threshold is a researcher construction.

**3. 五行 determines disease timing [measured]:** The 刺熱論 (Suwen ch.32) shows each organ's disease worsening on 克-element days and recovering on same-element days, with exact 天干 day assignments:
- 肝(Wood) worsens on 庚辛(Metal days), recovers on 甲乙(Wood days)
- 心(Fire) worsens on 壬癸(Water days), recovers on 丙丁(Fire days)
- 脾(Earth) worsens on 甲乙(Wood days), recovers on 戊己(Earth days)
- 肺(Metal) worsens on 丙丁(Fire days), recovers on 庚辛(Metal days)
- 腎(Water) worsens on 戊己(Earth days), recovers on 壬癸(Water days)

This is the Z₅ 克 cycle applied directly to temporal disease dynamics. No Q₃ substrate needed.

**4. 九宮八風 trigram→organ mapping has a dual organizational principle [measured]:** Cardinal directions use 五臟 (matching standard 五行). Intercardinal directions use 六腑 with assignments that follow 表裏 organ pairing, not 五行. Creates an asymmetric 8-position system. Connects to Lo Shu / mod-9 investigation (N7-N8), not the Z₅ question.

**5. Facial color diagnostics [measured]:** Each organ's heat disease manifests in a different facial zone (Suwen ch.32 line 65). This is a 五行→body-region mapping independent of both the 說卦 mapping (梅花) and the standard 五行→五臟 mapping.

### Key conclusions from discussion

**D1 as originally conceived is closed.** Three structural reasons:
1. **Axis correlation:** All three axes share a common 陰/陽 factor, creating hierarchically nested subdivisions of one distinction rather than three parallel binaries.
2. **表/里 sequentiality:** Disease depth is a gradient, not a state variable.
3. **No classical mapping:** The 八纲 → trigram assignment would be invented, introducing researcher degrees of freedom.

**Domain criterion sharpened (third condition added).**

**New thread: 刺熱論 Z₅ temporal periodicity.** The disease timing pattern is a direct Z₅ claim without Q₃. Test design: 2×5 contingency table testing whether 克 relation between organ element and day element predicts symptom direction.

**Grammar decomposability [conjectured]:** Q₃ = substrate (hexagram generation), Z₅ = content (medical interpretation via 生克). These are algebraically separable.

---

## Iteration 3: D1 Closure + 刺熱論 Scoping + 傷寒論 Read

**Tasks:** (A) Update findings.md with D1 results and domain criterion. (B) Scope the 刺熱論 Z₅ temporal test. (C) Read 傷寒論 channel openings for disease progression model.

### Task A: D1 Closed in findings.md

`domains/findings.md` updated with D1-R1 through D1-R4, cross-domain synthesis, three-condition domain criterion, grammar decomposability section, and updated open questions.

### Task B: 刺熱論 Z₅ Test Scoping

**天干 day computation [measured]:** Straightforward mod-10 from a known reference. The 60-day 干支 cycle is computable for any calendar date. Element assignment: 甲乙=Wood, 丙丁=Fire, 戊己=Earth, 庚辛=Metal, 壬癸=Water (each element = 2/10 days = 20%).

**Test design [conjectured]:** 2×5 contingency table (organ identity × day element), testing whether symptoms worsen on 克-element days. This tests Z₅-as-edge-typing (pairwise relation between positioned elements), not Z₅-as-group (spectral periodicity).

**Data landscape [measured]:** No existing dataset combines daily symptom tracking + TCM organ classification + sufficient patient-days. Structured TCM databases (SymMap, LTM-TCM) are cross-sectional, not longitudinal. Historical 医案 are narrative, not structured. MDASI-TCM tracks daily but classifies by Western diagnosis. No published studies have tested the 刺熱論's specific temporal claim. No known ~10-day biological rhythm exists in chronobiology literature.

**Verdict: Currently theoretical.** The test is well-defined but there is no available data. Parked as testable-but-not-with-available-data.

### Task C: 傷寒論 Disease Progression

**Output:** Section 11 appended to `neijing_extract.md`.

**Key findings [measured]:**

1. **六經 transitions are treatment-triggered, not deterministic.** The 傷寒論 explicitly allows "不传" (no transmission) and documents treatment-error-induced transitions (over-sweating → 太陽 skips to 陽明).

2. **Resolution timing uses 地支 (12-hour cycle), not 天干 (10-day cycle).** Each channel has a specific 3-hour resolution window. The pattern is purely 陰陽: yang channels during yang hours, yin channels during yin hours. No 五行 temporal element appears.

3. **Treatment logic is 陰陽, not 五行.** "阳盛阴虚，汗之则死，下之则愈" — treatment selection depends on 陰/陽 classification, not 五行 克 cycle.

4. **The 六經 model is a two-level tree (2×3), not a cube (2³).** Three 陽 channels subdivide 表; three 陰 channels subdivide 里. This is Z₂ × Z₃ = 6, not Z₂³ = 8 — a dimensional mismatch with Q₃. → Added as D1-R4 in findings.md.

### Discussion findings (review stage)

**1. Historical layering ≠ mathematical decomposability [correction from discussion]:**

The coexistence of Z₅ (刺熱論's 天干/五行 timing) and Z₂ (傷寒論's 地支/陰陽 timing) in the TCM tradition reflects historical compilation of different medical schools' frameworks, not a deliberate decomposition of mathematical structures. The 素問 is a multi-layered text with chapters from different periods. The 刺熱論's cosmological temporality and the 傷寒論's clinical temporality are different intellectual projects, not evidence that Z₅ has autonomous empirical content.

**Refined position on decomposability:** Algebraic decomposability is confirmed — Q₃ and Z₅ are logically independent structures. Empirical decomposability is unknown — no evidence that Z₅ has autonomous predictive content outside the Q₃-embedded I Ching system. The tradition's parallel usage patterns reflect historical layering, not a test of whether the grammar components work independently.

**2. 2×3 vs 2³ as a fourth structural failure for D1 [measured]:**

The 六經's native architecture is 2×3 (陰/陽 × three subdivisions), not 2³ (three independent binary axes). The 八纲 framework, which recasts this as 2³, is a later systematization that doesn't match the native clinical structure. This is a deeper kind of evidence for D1 closure than the axis-property arguments (R1-R3): the underlying clinical material has the wrong combinatorial dimension. Recorded as D1-R4.

**3. Recurring pattern: parallel classification systems [observed]:**

The tradition holds structurally different systems in parallel without reducing one to the other:
- Body mapping: 說卦 spatial vs 五行 functional
- Temporal disease: Z₅ (天干/刺熱論) vs Z₂ (地支/傷寒論)
- Diagnostic axes: 八纲 (three binary pairs) as later systematization of 六經 (2×3 tree)
- Medical sub-systems: pharmacology (五行-driven), spirit diagnosis (象-driven), body localization (說卦-driven)

This is a structural observation about how the Chinese intellectual tradition organizes knowledge: multiple classification systems coexist as parallel channels rather than being unified into a single framework.

---

## Final Synthesis

### Interpretive shift: uniqueness classification vs natural law

The uniqueness theorem (synthesis-3) proves the 五行 assignment is the unique complement-respecting surjection F₂³ → Z₅. Uniqueness theorems classify — they establish that a mathematical object is the only one of its kind under given axioms. They do not predict that the classified pattern will appear in physical systems.

D4 and D1 together are evidence that the grammar may be specific to the abstract trigram space where it was derived. Each domain fails for a *different* structural reason, and the failure reasons are complementary (D4: axes too different; D1: axes too similar). The three-condition criterion is so restrictive that the question has effectively inverted — from "which domain will the grammar transfer to?" to "is the grammar domain-specific to trigram space?"

This shifts the research orientation from seeking external validation toward characterizing the grammar's nature as a mathematical object. The grammar's content may be its uniqueness — that it is the only way to type Q₃ edges under complement-Z₅ axioms — not its transferability to physical systems.

### Investigation outputs (ordered by importance)

1. **Interpretive shift:** The grammar is a uniqueness classification of a mathematical object, not a transferable natural law. D4 + D1 together make this case.

2. **Three-condition domain criterion:** Reusable screening filter — any future Q₃ domain proposal checked against (S₃ symmetry, independence, parallelism) before investment.

3. **Grammar decomposability:** Algebraically confirmed (Q₃ = substrate, Z₅ = content, logically separable). Empirically unknown.

4. **Z₅ edge-typing test design:** 2×5 contingency table for the 刺熱論 claim. The narrowest operationalization of "does 五行 have empirical content?" Currently no data.

5. **梅花 medical domain extraction:** Independent value for the atlas work. Three sub-systems, parallel classification architecture, worked example analysis, 互(本) confirmed 5:1.

### What remains untested

- Whether Z₅-as-edge-typing has empirical content in any domain (requires new data, not more TCM reading)
- Whether any Q₃-compatible domain exists given the three-condition criterion
- The 九宮八風 dual-principle mapping's connection to Lo Shu / mod-9 (N7-N8 open questions)
