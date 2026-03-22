# 黃帝內經 — 八纲 Diagnostic Axes Extraction

> Structured extraction from 素問 and 靈樞 chapters.
> Focus: the binary diagnostic axes (寒/热, 虚/实, 表/里), their 五行 connections, and any trigram/易 links.
> For the D1 domain investigation (TCM 八纲辨证 as test bed for the Z₅ grammar).

---

## 1. Note on 八纲辨证

The term 八纲辨证 (Eight Principles Pattern Identification) does **not appear** in the 黃帝內經. Grep for 八綱/八纲 returns zero hits. The framework as a formal system was codified later — the 傷寒論 (Zhang Zhongjing, ~200 CE) systematized 表/里/寒/热, and the full 八纲 formulation is traditionally attributed to Ming-Qing era systematizers.

The 內經 provides the **building blocks** — all six poles (寒, 热, 虚, 实, 表, 里) appear frequently as clinical concepts — but they are NOT organized into a single diagnostic framework with three independent binary axes.

---

## 2. 素問 Ch.5 — 陰陽應象大論 (suwen_02.txt lines 3-69)

### The foundational chapter. Establishes 陰陽 as the medical meta-axis.

### Binary axes present

**寒/热 ↔ 陰/陽 (DEFINITIONAL EQUIVALENCE):**
> 陽勝則熱，陰勝則寒。重寒則熱，重熱則寒。(line 18)

This is not a correlation — it's a definition. Hot = yang excess, cold = yin excess. The text also asserts mutual transformation at extremes: "extreme cold generates heat, extreme heat generates cold" (line 8: 寒極生熱，熱極生寒).

**虚/实 (IMPLICIT):**
> 形不足者，溫之以氣；精不足者，補之以味...其實者，散而寫之。(line 69)

Deficiency and excess are treatment categories but not yet named as a paired axis.

**表/里 (MENTIONED but not as diagnostic axis):**
> 外內之應，皆有表裏 (line 28)
> 以表知裏 (line 65)

Used as a general principle ("external reflects internal") rather than a diagnostic binary.

### 五行 → organ correspondence table

Lines 30-38 establish the canonical 五行 → 五臟 table:

| Direction | Element | Organ | Body tissue | Sense | Taste | Emotion | Climate |
|---|---|---|---|---|---|---|---|
| 東 | 木 Wood | 肝 Liver | 筋 Sinew | 目 Eye | 酸 Sour | 怒 Anger | 風 Wind |
| 南 | 火 Fire | 心 Heart | 脈 Vessel | 舌 Tongue | 苦 Bitter | 喜 Joy | 熱 Heat |
| 中央 | 土 Earth | 脾 Spleen | 肉 Flesh | 口 Mouth | 甘 Sweet | 思 Worry | 濕 Damp |
| 西 | 金 Metal | 肺 Lung | 皮毛 Skin | 鼻 Nose | 辛 Pungent | 憂 Grief | 燥 Dryness |
| 北 | 水 Water | 腎 Kidney | 骨 Bone | 耳 Ear | 鹹 Salty | 恐 Fear | 寒 Cold |

**Key for D1:** Each element has a natural thermal quality (熱/寒/濕/燥/風). This creates an inherent correlation between the 五行 identity and the 寒/热 axis — Fire organs (心) are "naturally" hot, Water organs (腎) are "naturally" cold. This means the 寒/热 axis is NOT independent of the 五行 identity of the affected organ.

### 克 cycle in medicine
> 怒傷肝，悲勝怒；風傷筋，燥勝風；酸傷筋，辛勝酸。(line 30)

Each element's pathology is克'd by the controlling element's emotion/climate/taste. The medical 克 cycle operates on the same structure as the abstract 五行 克 cycle.

### Diagnostic principle
> 善診者，察色按脈，先別陰陽 (line 67)
> 陽病治陰，陰病治陽 (line 69)

The master diagnostic move is "first distinguish yin from yang." All subsequent differentiation (寒/热, 虚/实, 表/里) is subdivisions of this primary classification.

---

## 3. 素問 Ch.28 — 通評虛實論 (suwen_08.txt lines 120-218)

### The definitive chapter on 虚/实.

### Definition of 虚/实
> 何謂虛實。邪氣盛則實，精氣奪則虛。(lines 122-124)

**实 = pathogenic qi dominant.** 虚 = vital qi depleted. This is a **force-balance** definition — not a simple binary but a ratio (pathogen strength / vital qi strength).

### NOT a simple binary — gradations exist
- **重實** (double excess): "大熱病，氣熱脈滿，是謂重實" (line 132)
- **重虛** (double deficiency): "脈氣上虛尺虛，是謂重虛" (line 154)
- **Mixed 虚/实**: "經虛絡滿" (meridians deficient, collaterals full), "絡滿經虛" (collaterals full, meridians deficient) — lines 144-150. Different parts of the body can be simultaneously 虚 and 实.

### 虚/实 × 寒/热 interaction
> 脈實滿，手足寒，頭熱 (line 164) — simultaneously 实 (pulse full) and mixed 寒/热 (cold hands/feet, hot head)
> 手足溫則生，寒則死 (line 174) — extremity temperature is prognostic within 虚/实

This shows the axes are NOT independent: 实 with cold extremities has different prognosis from 实 with warm extremities. The temperature of extremities functions as a prognostic modifier within the 虚/实 evaluation.

### Seasonal modifiers on 虚/实
> 春秋則生，冬夏則死 (line 166) — same 虚/实 pattern has different outcomes depending on season.

This parallels 梅花's 旺/衰 seasonal modifier on the 生克 verdict.

---

## 4. 素問 Ch.29 — 太陰陽明論 (suwen_08.txt lines 220-255)

### The 表/里 axis as organ pairing.

> 太陰陽明為表裏，脾胃脈也 (line 222)

Here 表/里 specifically means the **paired relationship between 臟 and 腑**: 脾(太陰=里) and 胃(陽明=表). This is NOT the same as the 八纲 表/里 (exterior/interior of the body).

### Directional pathology
> 陽者...主外，陰者...主內 (line 228)
> 陽受之，則入六府，陰受之，則入五藏 (line 232)
> 傷於風者，上先受之；傷於濕者，下先受之 (line 240)

陽 = outer/上, 陰 = inner/下. Disease entry follows this: wind (yang pathogen) attacks from above, damp (yin pathogen) attacks from below. This establishes 表/里 as intrinsically correlated with 陰/陽 — 表 IS 陽, 里 IS 陰.

---

## 5. 素問 Ch.31 — 熱論 (suwen_09.txt lines 4-51)

### The six-channel disease progression — the clearest 表→里 model.

### Day-by-day progression of 傷寒:

| Day | Channel | Symptoms | Layer |
|---|---|---|---|
| 1 | 太陽 (Taiyang) | Headache, back stiffness | 表 (Exterior) |
| 2 | 陽明 (Yangming) | Body heat, eye pain, nose dry | 表 |
| 3 | 少陽 (Shaoyang) | Chest pain, deafness | 表/里 boundary |
| 4 | 太陰 (Taiyin) | Abdominal fullness, throat dry | 里 (Interior) |
| 5 | 少陰 (Shaoyin) | Mouth dry, thirsty | 里 |
| 6 | 厥陰 (Jueyin) | Irritability, scrotum retraction | 里 (deepest) |

### Treatment boundary:
> 其未滿三日者，可汗而已；其滿三日者，可泄而已。(lines 28-29)

Before day 3: sweat therapy (表 treatment). After day 3: purge therapy (里 treatment). The 表/里 transition occurs at the 三陽→三陰 boundary.

### 兩感 (dual-channel infection):
> 病一日，則巨陽與少陰俱病 (line 45)

太陽+少陰 (表+里 simultaneously). This is the lethal variant — when 表 and 里 are attacked together, the patient dies in 6 days. This shows 表 and 里 are NOT independent axes that can take arbitrary values — their simultaneous engagement creates a qualitatively different (fatal) condition.

### Key for D1: The 表/里 axis is sequential, not simultaneous. In the standard model, disease progresses from 表 to 里 over time. The axis measures disease depth, not an independent binary state.

---

## 6. 素問 Ch.32 — 刺熱論 (suwen_09.txt lines 53-76)

### Five-organ heat diseases — 五行 determines disease pattern.

| Organ | 五行 | Exacerbation days | Crisis days | Death days |
|---|---|---|---|---|
| 肝 | Wood | 庚辛 (Metal days) | 甲乙 (Wood days=recovery) | 庚辛 (Metal=克) |
| 心 | Fire | 壬癸 (Water days) | 丙丁 (Fire days) | 壬癸 (Water=克) |
| 脾 | Earth | 甲乙 (Wood days) | 戊己 (Earth days) | 甲乙 (Wood=克) |
| 肺 | Metal | 丙丁 (Fire days) | 庚辛 (Metal days) | 丙丁 (Fire=克) |
| 腎 | Water | 戊己 (Earth days) | 壬癸 (Water days) | 戊己 (Earth=克) |

**Pattern:** Disease worsens on the days of its 克 element, recovers on its own element's days, and dies if 氣逆 occurs on 克-element days. This is the medical 五行 克 cycle determining temporal disease dynamics.

### Facial color diagnostics (line 65):
> 肝熱病者，左頰先赤，心熱病者，顏先赤，脾熱病者，鼻先赤，肺熱病者，右頰先赤，腎熱病者，頤先赤。

Each organ's heat manifests in a different facial zone. This is NOT random — it's a systematic 五行→body-region mapping independent of the 說卦 mapping used in 梅花.

---

## 7. 靈樞 Ch.73 — 官能 (lingshu_11.txt lines 3-13)

### The closest passage to a diagnostic axis enumeration.

> 用鍼之理，必知形氣之所在，左右上下，**陰陽表裏**，血氣多少，行之逆順，出入之合...知補**虛**寫**實**...**寒**與**熱**爭，能合而調之，**虛**與**實**鄰，知決而通之 (line 9)

This passage lists the diagnostic pairs in sequence:
1. 左/右 (left/right)
2. 上/下 (upper/lower)
3. 陰/陽 (yin/yang)
4. 表/裏 (exterior/interior)
5. 虛/實 (deficiency/excess)
6. 寒/熱 (cold/hot)

All six binary pairs appear as things the acupuncturist must be able to assess. But they are presented as a **checklist**, not as a formal multi-axis coordinate system. No claim is made about independence.

---

## 8. 靈樞 Ch.77 — 九宮八風 (lingshu_11.txt lines 155-177)

### The trigram connection chapter. Explicit 八卦 → organ → wind → disease mapping.

### 太一 (Great Unity) moves through the nine palaces:
The nine palaces correspond to the 八卦 + center, arranged on the 洛書 magic square:

| SE巽(4) | S离(9) | SW坤(2) |
|---|---|---|
| E震(3) | Center(5) | W兑(7) |
| NE艮(8) | N坎(1) | NW乾(6) |

### Eight winds → organ mapping:

| Direction | Trigram | Wind name | Internal organ (內舍) | External body (外在) | Quality (氣主) |
|---|---|---|---|---|---|
| 南 S | 离 | 大弱風 | **心** | 脈 | **熱** |
| 西南 SW | 坤 | 謀風 | **脾** | 肌 | 弱 |
| 西 W | 兑 | 剛風 | **肺** | 皮膚 | **燥** |
| 西北 NW | 乾 | 折風 | **小腸** | 手太陽脈 | 暴死 |
| 北 N | 坎 | 大剛風 | **腎** | 骨+肩背膂筋 | **寒** |
| 東北 NE | 艮 | 凶風 | **大腸** | 兩恢腋骨+肢節 | — |
| 東 E | 震 | 嬰兒風 | **肝** | 筋紐 | **身濕** |
| 東南 SE | 巽 | 弱風 | **胃** | 肌肉 | 體重 |

### Analysis of the mapping:

**Cardinal directions use 五臟 (yin organs), matching standard 五行:**
- 离(S/Fire) → 心 ✓
- 坎(N/Water) → 腎 ✓
- 震(E/Wood) → 肝 ✓
- 兑(W/Metal) → 肺 ✓

**坤(Earth) also maps to 五臟:**
- 坤(SW/Earth) → 脾 ✓

**Intercardinal directions use 六腑 (yang organs):**
- 乾(NW) → 小腸 (Small Intestine)
- 艮(NE) → 大腸 (Large Intestine)
- 巽(SE) → 胃 (Stomach)

These are NOT the 五行-predicted organs for these trigrams. 乾(Metal) should map to 肺, not 小腸. 巽(Wood) should map to 肝, not 胃. The system assigns 六腑 organs to the "secondary" trigrams of each element:
- Metal: 兑→肺(臟), 乾→小腸(腑) — but 小腸 is Fire's 腑, not Metal's
- Earth: 坤→脾(臟), 艮→大腸(腑) — but 大腸 is Metal's 腑, not Earth's
- Wood: 震→肝(臟), 巽→胃(腑) — but 胃 is Earth's 腑, not Wood's

**The 六腑 assignments follow meridian 表裏 pairing, not 五行:**
- 小腸 is 表裏 with 心 (which is at 离/S, opposite to 乾/NW)
- 胃 is 表裏 with 脾 (which is at 坤/SW, adjacent to 巽/SE)
- 大腸 is 表裏 with 肺 (which is at 兑/W, adjacent to 艮/NE)

### 實風 vs 虛風:
> 風從其所居之鄉來為實風，主生，長養萬物。從其衝後來為虛風，傷人者也 (line 175)

Wind from the direction where 太一 currently resides = 實風 (nourishing). Wind from the opposite direction = 虛風 (pathogenic). This creates a dynamically-determined 虚/实 based on temporal position of 太一 in the nine-palace circuit. 虚/实 is NOT a fixed property of the patient but depends on the temporal context.

### Three-deficiency rule:
> 此八風皆從其虛之鄉來，乃能病人，三虛相搏，則為暴病卒死，兩實一虛，病則為淋露寒熱 (line 177)

Three simultaneous 虛 conditions → sudden death. Two 實 + one 虛 → chronic disease with 寒/热 oscillation. This is a combinatorial rule involving 虚/实 counts, not a binary axis.

### Key for D1: This is the only 內經 chapter that explicitly maps 八卦 to medical concepts. But it does so via wind direction and temporal 太一 position — a cosmological framework, not a clinical diagnostic system. The mapping is weather → disease, not symptom → diagnosis.

---

## 9. Cross-Chapter Synthesis

### T1: What are the 八纲? How defined clinically?

The 內經 does NOT define 八纲 as a framework. It provides three binary pairs used in clinical assessment:

1. **寒/热**: Defined as 陰/陽 excess (Suwen 5). Clinically assessed by body temperature, extremity warmth, pulse quality.
2. **虚/实**: Defined as vital qi depletion / pathogen dominance (Suwen 28). Clinically assessed by pulse, breathing, body habitus.
3. **表/里**: Defined as disease location depth (Suwen 31). Clinically determined by which channel is affected and symptom pattern.

陰/陽 is the meta-axis that subsumes the other three:
- 表 = 陽, 里 = 陰
- 热 = 陽, 寒 = 陰
- 实 = 陽, 虚 = 陰

### T2: Are the three axes independent?

**Evidence for correlation (not independence):**

1. **寒/热 ↔ 表/里:** Disease progresses from 表(陽=hot) → 里(陰=cold). The 熱論 six-day model shows this is sequential. Early disease is in 陽 channels (exterior, hot). Late disease is in 陰 channels (interior, cold).

2. **虚/实 ↔ 寒/热:** Deficiency (虚) is typically cold; excess (实) is typically hot. "重實 = 大熱病" (Suwen 28). But mixed states exist (line 164: pulse full/实 but hands cold/寒).

3. **表/里 ↔ 虚/实:** The 九宮八風 chapter dynamically determines 虚/实 from temporal-spatial context. The 太陰陽明論 shows that 表(陽明) "道实" and 里(太陰) "道虚" — the axes have a default correlation.

4. **ALL three axes map onto the single 陰/陽 meta-axis.** This means they share a common factor. True independence would require each axis to vary freely while the others remain fixed.

**Evidence for partial independence:**

1. Mixed states exist: "經虛絡滿" (meridian-虚 + collateral-实, Suwen 28) — different body regions can have opposite 虚/实 simultaneously.
2. 兩感 (dual-channel infection, Suwen 31): 表 and 里 simultaneously attacked — this violates the normal sequential progression.
3. Clinical reality admits all 8 combinations (hot-excess-exterior, cold-deficiency-interior, etc.), though some are far more common than others.

**Verdict:** The axes are **correlated but not redundant**. They share a common 陰/陽 factor, creating strong default associations (热-实-表, 寒-虚-里), but mixed/crossed states are clinically documented. The correlation is stronger than the market-axis correlation that failed the D4 test (MI=0.346), but the axes are also of more similar character (all are assessments of the same body).

### T5: Classical connections between 八纲 and trigrams?

**Direct connection: Lingshu Ch.77 only.** The 九宮八風 chapter maps trigrams to organs via directional winds, but does NOT map trigrams to the 八纲 axes themselves. No text says "乾 = 表+热+实" or anything similar.

**Structural parallel:** The梅花 medical domain's illness rules (体旺/衰, 生体 pharmacology, 克体 spirit diagnosis) operate on a 五行 framework that parallels the 內經's 五行 → organ → disease model. But the 梅花 system reads trigrams, not 八纲 axes. There is no classical text that bridges the two frameworks by mapping 八纲 axes to trigram bits.

**The 八纲 → trigram mapping would be an INVENTION, not a DISCOVERY.** If we assign 寒/热, 虚/实, 表/里 to three bit positions, we create a trigram from clinical state. This mapping does not appear in classical literature. The D1 test would need to justify this construction independently.

---

## 10. Key Passages Index

| Chapter | Line | Chinese | Significance |
|---|---|---|---|
| Suwen 5 | 18 | 陽勝則熱，陰勝則寒 | 寒/热 = 陰/陽 (definitional) |
| Suwen 5 | 8 | 寒極生熱，熱極生寒 | Mutual transformation at extremes |
| Suwen 5 | 30-38 | 東方生風...北方生寒 | Full 五行 correspondence table |
| Suwen 5 | 67 | 善診者...先別陰陽 | Diagnostic priority: 陰/陽 first |
| Suwen 5 | 69 | 陽病治陰，陰病治陽 | Treatment principle |
| Suwen 8/28 | 124 | 邪氣盛則實，精氣奪則虛 | 虚/实 definition |
| Suwen 8/28 | 132 | 大熱病...是謂重實 | 重实 = compound excess |
| Suwen 8/28 | 174 | 手足溫則生，寒則死 | 寒/热 as prognostic within 虚/实 |
| Suwen 8/29 | 228 | 陽者...主外，陰者...主內 | 表=陽, 里=陰 |
| Suwen 9/31 | 11-16 | 傷寒一日...六日厥陰受之 | Six-channel 表→里 progression |
| Suwen 9/31 | 28-29 | 未滿三日者可汗...滿三日者可泄 | 表/里 treatment boundary |
| Suwen 9/31 | 45 | 巨陽與少陰俱病 | 兩感 (simultaneous 表+里) |
| Suwen 9/32 | 55-63 | 肝熱病者...腎熱病者 | 五行 determines disease timing |
| Lingshu 11/73 | 9 | 陰陽表裏...寒與熱爭...虛與實鄰 | All axes listed as diagnostic checklist |
| Lingshu 11/77 | 175 | 實風...虛風 | Dynamic 虚/实 from 太一 position |
| Lingshu 11/77 | 177 | 風從南方來...內舍於心 | Full trigram→organ→wind mapping |

---

## 11. 傷寒論 Disease Progression (shang-han-lun.md)

### The 六經 model in clinical practice

The 傷寒論 (Zhang Zhongjing, ~200 CE) formalizes the 內經's six-channel model into a clinical treatment system. Each of the six channels (三陽 + 三陰) gets a dedicated chapter with defining symptoms, transition rules, and prescriptions.

### Channel definitions (opening clauses)

| Channel | Key symptoms | Line |
|---|---|---|
| 太陽 | 脈浮，頭項強痛而惡寒 (floating pulse, headache, neck stiffness, aversion to cold) | (1) |
| 陽明 | 胃家實 (stomach excess) — body heat, sweating, aversion to heat not cold | (180) |
| 少陽 | 口苦，咽乾，目眩 (bitter mouth, dry throat, dizziness) | (263) |
| 太陰 | 腹滿而吐，食不下...時腹自痛 (abdominal fullness, vomiting, pain) | (273) |
| 少陰 | 脈微細，但欲寐 (faint thin pulse, desire only to sleep) | (281) |
| 厥陰 | 消渴，氣上撞心，心中疼熱，飢而不欲食 (thirst, qi surging to heart, heat/pain) | (326) |

### Disease state transitions

**Primary transition pathway:** 太陽 → 陽明 (most documented transition)

The text describes "转属" (transfer/belong-to) as the main transition mechanism:
- "太阳病...亡津液，胃中干燥，因转属阳明" (line 181) — fluid depletion from over-sweating → stomach dries out → transfers to 阳明
- "本太阳初得病时，发其汗，汗先出不彻，因转属阳明" (line 185) — incomplete sweating → transfers to 阳明
- "本太阳病不解，转入少阳者" (line 266) — unresolved → transfers to 少阳

**Critical finding:** Transitions are NOT purely sequential (太陽→陽明→少陽→...). They are **triggered by treatment errors or natural disease evolution**:
- Over-sweating → 太陽 jumps to 陽明 (skipping 少陽)
- Wrong purging → creates complications (结胸, 痞)
- Natural resolution → disease resolves at its current channel

**Non-progression clause:** "伤寒一日，太阳受之，脉若静者，为不传" (line 4) — if the pulse is quiet, disease does NOT transmit. The 傷寒論 explicitly allows for non-progression, unlike the 內經's deterministic 6-day model.

**陽→陰 transition:** "伤寒六七日，无大热，其人躁烦者，此为阳去入阴故也" (line 269) — after 6-7 days, restlessness without high fever signals yang departing, entering yin. This confirms the 表→里 directionality but also suggests it's not always sequential through all channels.

### Resolution timing (欲解時)

Each channel has a 地支 time window when disease naturally resolves:

| Channel | 欲解時 | Clock time | Significance |
|---|---|---|---|
| 太陽 | 巳→未 | 9am–3pm | Peak yang (midday) |
| 陽明 | 申→戌 | 3pm–9pm | Declining yang |
| 少陽 | 寅→辰 | 3am–9am | Rising yang |
| 太陰 | 亥→丑 | 9pm–3am | Deep yin |
| 少陰 | 子→寅 | 11pm–5am | Deepest yin → dawn |
| 厥陰 | 丑→卯 | 1am–7am | Yin → yang transition |

**Key observation:** This uses a **12-hour (地支) cycle**, NOT the 10-day (天干) cycle of the 刺熱論. The 傷寒論 and 刺熱論 use completely different temporal frameworks:
- 刺熱論 (Suwen ch.32): disease severity oscillates on a 10-day 天干 cycle, with element-克 days being worst
- 傷寒論: disease resolution windows are tied to the 12-hour 地支 cycle within each day

There is NO mention of 天干-element disease timing in the 傷寒論. The temporal framework is entirely 陰陽-based (yang hours for yang-channel resolution, yin hours for yin-channel resolution), not 五行-based.

### Treatment logic: 陰陽, not 五行

> 夫阳盛阴虚，汗之则死，下之则愈。阳虚阴盛，汗之则愈，下之则死。(line 256)

The 傷寒論's treatment logic is structured around 陰/陽 classification of disease AND treatment method, not around 五行 克 cycles. Sweat therapy (汗法) is 表/陽 treatment; purge therapy (下法) is 里/陰 treatment. Mismatching treatment to disease type is fatal: sweating a yin-excess patient kills them.

The transition pairs reinforce this 陰陽 pairing:
- 太陽 ↔ 少陰 (most yang ↔ least yin — 表裏 pair)
- 陽明 ↔ 太陰 (bright yang ↔ most yin — 表裏 pair)
- 少陽 ↔ 厥陰 (least yang ↔ terminal yin — 表裏 pair)

### Implications for the Z₅ / 刺熱論 thread

1. **The 傷寒論 does NOT use 五行 temporal disease timing.** Zhang Zhongjing's clinical system operates entirely on 陰陽 logic (六經 channels + 12-hour 地支 resolution windows). The 天干 10-day cycle from the 刺熱論 is absent from the most influential clinical text in Chinese medicine.

2. **The 六經 model is fundamentally a hierarchical nesting**, not a Q₃ cube. The three陽 channels are subdivisions of 陽 (表); the three 陰 channels are subdivisions of 陰 (里). This is a two-level tree (陰/陽 → 3 channels each), not three independent binary axes.

3. **If the 刺熱論 claim is testable, the test must use 內經-style organ-disease classification, not 傷寒論-style channel classification.** The 傷寒論 classifies disease by syndrome pattern, while the 刺熱論 classifies by affected organ. Different diagnostic frameworks, different temporal predictions.
