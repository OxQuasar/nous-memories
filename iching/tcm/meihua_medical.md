# 梅花易數 — 疾病占 (Medical/Illness Domain)

> Structured extraction from 梅花易數 vols 2–4.
> Focus: what the medical domain adds beyond the standard 18-domain 體/用 template.
> Cross-references atlas-mh findings V.4 for the template baseline.

---

## A. Prognosis Rules (體/用 生克 Applied to Illness)

### Standard 5-relation template [standard template]

These follow the same logic as all 18 domains, with 體=patient, 用=disease:

| Relation | Prognosis | Chinese |
|---|---|---|
| 体克用 | Easy recovery; medicine unnecessary | 体克用，病易安；勿药有喜 |
| 用克体 | Medicine useless | 用克体，虽药无功 |
| 体生用 | Lingering illness, slow recovery | 体生用，病难愈；迁延难好 |
| 用生体 | Quick recovery | 用生体，即愈 |
| 比和 | Easy recovery | 体用比和，疾病易安 |

### Illness-specific additions [illness-specific]

These rules appear ONLY in 疾病占 — no other domain has them:

**1. 體旺/衰 modifier:**
> 若体逢克而乘旺，犹为庶几。体遇克而更衰，断无存日。

- 體 克'd + seasonally 旺 → still some hope (庶几)
- 體 克'd + seasonally 衰 → certain death (断无存日)

Note: the 旺/衰 concept (seasonal strength) exists in the general system, but the illness domain makes it a **life/death discriminator**, not just a severity modifier. No other domain has "断无存日" (literally "no surviving day").

**2. Rescue signal (凶中有救):**
> 欲知凶中有救，生体之卦存焉。

When 克体 is present, look for ANY 生体 trigram (in 互 or 變 positions). If present → rescue possible. If absent → hopeless. This is formalized in vol3 line 192:
> 互变中俱有克体之卦，而本卦中又无生体之卦者，断不吉也。

**3. Timing rules [illness-specific]:**
- 和平之日 (recovery date): determined by 主卦 (本卦)
- 危厄之期 (crisis/death date): determined by 克体之卦's element timing
- These domain-specific timing bindings don't appear in other domains which use the general 克應之期 formula.

**4. 體宜旺不宜衰 [standard template, but emphasized]:**
> 体卦宜旺不宜衰，体宜逢生，不宜见克。

Vol3 verse confirms: 疾病最宜体旺相 (line 116). Standard, but the medical domain states it more forcefully than other domains.

---

## B. Pharmacology Sub-system [illness-specific]

### The trigram→medicine mapping

Source: vol2 line 91.

> 若论医药之属，当看生体之卦。如离卦生体，宜服热药；坎卦生体，宜服冷药，如艮温补；乾、兑凉药是也。

| 生体 trigram | Medicine type | 五行 | Via 五行? |
|---|---|---|---|
| 离 | 热药 (hot drugs) | Fire | ✓ Direct: Fire=hot |
| 坎 | 冷药 (cold drugs) | Water | ✓ Direct: Water=cold |
| 艮 | 温补 (warm tonics) | Earth | ✗ Earth→warm is TCM-specific, not 五行-inherent |
| 乾 | 凉药 (cooling drugs) | Metal | Partial: Metal→cool is TCM 五行, not raw 五行 |
| 兑 | 凉药 (cooling drugs) | Metal | Partial: same as 乾 |

**Analysis:** The mapping partially follows 五行 (Fire=hot, Water=cold are universal), but adds TCM-specific thermal associations. Earth→温 and Metal→凉 require the TCM thermal framework (四气 — cold/hot/warm/cool). This sub-system bridges 易 五行 into Chinese medical 五行, which has its own thermal assignments not derivable from abstract 五行 alone.

**Missing trigrams:** 震 and 巽 (both Wood) have no explicit medicine mapping in this passage. Presumably Wood→liver corresponds to TCM herbal categories, but the text is silent.

### Vol3 verse confirmation (lines 118):
> 离宜服热坎服冷，卦见坤土温补亨。

Note: this verse says 坤 for warm tonics where vol2 says 艮. Both are Earth trigrams. The system maps at the **element level** (Earth=温補), not individual trigram level, for pharmacology.

### Vol3 乾 expanded entry (line 216):
> 附药：丸子。

For 乾 specifically, the medicine **form** is pill (丸子). This is an additional layer — not just drug thermal quality, but dosage form. Only 乾 has this in the surviving text.

### Key structural point:
The pharmacology rule operates on the **生体** trigram specifically — "当看生体之卦". It's the trigram that heals 體, prescribing what kind of medicine aids recovery. The pharmacology sub-system is thus structurally integrated into the 生克 arc: it reads the "rescue channel" of the relation vector.

---

## C. Spirit Diagnosis Sub-system (鬼神) [illness-specific]

Source: vol2 line 92.

> 又有信鬼神之说，虽非《易》道，然不可谓《易》道之不该。姑以理推之。如卦有克体者，即可测其鬼神。

### Trigger rule:
Spirit diagnosis activates when 克体 trigram exists. Read the 克体 trigram's identity → diagnose the supernatural cause. If no 克体 trigram exists → skip spirit diagnosis entirely (卦中无克体之卦者，不必论之).

### Full 8-trigram mapping:

| 克体 trigram | Direction | Spirit type | Chinese |
|---|---|---|---|
| 乾 | 西北 | War/blade ghost, epidemic spirit, or righteous deity | 兵刀之鬼，天行时气，乘正之邪神 |
| 坤 | 西南 | Wilderness ghost, deceased relative, earth/community god, directionless spirit | 旷野之鬼，连亲之鬼，水土里社之神，无主之祟 |
| 震 | 东 | Tree spirit, shape-shifting apparitions | 木下之神，妖怪百端，影响时见 |
| 巽 | 东南 | Suicide by hanging, death by shackles | 自缢戕生，枷锁致命 |
| 坎 | 北 | Waterside spirit, drowning ghost, blood-disease ghost | 水旁之神，没溺而亡，血疾之鬼 |
| 离 | 南 | Fierce warrior spirit, kitchen deity offense, incense/fire spirit, burning death ghost | 猛勇之神，犯灶司，得衍于香火，焚烧之鬼 |
| 艮 | 东北 | Mountain spirit, tree demon, earth/stone spirit | 山林之祟，山魈木客，土怪石精 |
| 兑 | 西 | Battle death ghost, disability ghost, throat-cut suicide ghost | 阵亡之鬼，废疾之鬼，刎颈戕生之鬼 |

### Analysis:

The spirit types map to trigram imagery, NOT 五行:
- 乾 (Heaven/ruler) → military, epidemic (天行), authoritative spirits
- 坤 (Earth/field) → wilderness, soil, community shrines, rootless spirits
- 震 (Thunder/movement) → shape-shifting, intermittent apparitions
- 巽 (Wind/rope) → hanging, shackles (rope/binding imagery)
- 坎 (Water/danger) → drowning, blood
- 离 (Fire/brightness) → fire death, kitchen god, incense
- 艮 (Mountain/stillness) → mountain creatures, stone spirits
- 兑 (Lake/sharp) → blade deaths, dismemberment, battle

This is **trigram象 (image) driven**, not 五行 driven. Each spirit type is a narrative extension of the trigram's natural imagery into the death/supernatural domain. This sub-system adds information that 五行 alone cannot derive.

### Vol3 verse (lines 119-120):
> 亦把鬼神卦象推，震主娇怪为状貌。
> 巽为自缢井锁枷，坤艮落水及血刃。

Partial summary only — confirms the mapping but is incomplete (坤艮 merged together, and坤 listed with 落水 which is more 坎-like — possible textual corruption or abbreviation in the verse form).

---

## D. Trigram → Body Part Mapping

### Primary mapping: 近取诸身 (vol3 line 28)

Source: the standard 說卦 body correspondence, cited in 梅花 context.

| Trigram | Body part | 五行 | Standard 五行→organ |
|---|---|---|---|
| 乾 | 头 (head) | Metal | 肺 (lung) |
| 坤 | 腹 (abdomen) | Earth | 脾 (spleen) |
| 震 | 足 (foot) | Wood | 肝 (liver) |
| 巽 | 股 (thigh) | Wood | 肝 (liver) |
| 坎 | 耳 (ear) + 血 (blood) | Water | 腎 (kidney) |
| 离 | 目 (eye) | Fire | 心 (heart) |
| 艮 | 手/手指 (hand/fingers) | Earth | 脾 (spleen) |
| 兑 | 口/口齿 (mouth/teeth) | Metal | 肺 (lung) |

### Diagnostic application (vol3 line 53):
> 若问病，如乾卦受克，病在头。坤宫见克，病在腹，推之震足、巽股、离目、坎耳及血、艮手指、兑口齿，于其克者定见其病。

**Rule:** Look at which trigram position is 受克 (receiving克). That trigram's body part is where the disease manifests. This is a positional reading — not just the 體/用 pair, but scanning all positions (本互變) for which trigram is being attacked.

### Expanded 乾 body parts (vol3 line 210):
> 身体：顶、面颊、頄辅。

乾 expands beyond just 头 to: crown of head (顶), cheeks (面颊), cheekbones (頄辅). The other 7 trigrams lack this expansion in the surviving text.

### 說卦 health references (vol3 lines 220-221):

Additional body/disease associations from the 說卦 layer:
- 坎: 心病 (heart disease), 耳痛 (ear pain), 血卦 (blood trigram)
- 离: 大腹 (large abdomen — pregnancy or bloating)

### 乾 disease specifics (vol3 line 215):
> 疾病：于太陽脉弦紧，天威所罚、上壅目熟、寒热。

For 乾: taut/tight 太陽 pulse, punished by heaven, upper congestion with eye heat, alternating chills and fever. This uses TCM pulse diagnosis terminology (脉弦紧) — a medical-technical layer beyond 五行.

### Discrepancies: 近取诸身 vs 五行→organ

| Trigram | 近取诸身 (body region) | 五行→organ (TCM zangfu) | Match? |
|---|---|---|---|
| 乾 (Metal) | Head | Lung | ✗ Different systems |
| 坤 (Earth) | Abdomen | Spleen | Partial — abdomen contains spleen |
| 震 (Wood) | Foot | Liver | ✗ Different systems |
| 巽 (Wood) | Thigh | Liver | ✗ Different systems |
| 坎 (Water) | Ear + blood | Kidney | ✓ TCM: kidney opens to ear |
| 离 (Fire) | Eye | Heart | ✓ TCM: heart opens to tongue, but 离=eye is 說卦 |
| 艮 (Earth) | Hand/fingers | Spleen | ✗ Different systems |
| 兑 (Metal) | Mouth/teeth | Lung | Partial — TCM: lung→nose, but 兑=mouth is 說卦 |

**Key finding:** The 近取诸身 mapping is from 說卦 (body topology — spatial correspondence) while 五行→organ is from TCM (functional correspondence). They are two different systems that the 梅花 medical domain holds in parallel. The 梅花 illness section (vol2 line 91, vol3 line 53) uses the 說卦 body-region mapping for disease **localization** — "where does it hurt?" The 五行→organ mapping operates separately for understanding disease **mechanism** — "which organ system is dysfunctional?"

---

## E. Worked Example: 乾上坤下 with 6 Moving Lines

Source: vol2 lines 93-94. Shao Yong (尧夫) analyzes hexagram 12 (否 — 乾 upper, 坤 lower) for illness, varying the moving line.

**Setup:** 乾上坤下 (否). Standard 梅花 rule: the trigram containing the 動爻 is 用 (it moves/changes); the non-moving trigram is 体. Therefore 体 flips at line 4:

- **Lines 1-3:** 動爻 in lower 坤 → 坤=用, 乾=体. **体=乾=Metal.**
- **Lines 4-6:** 動爻 in upper 乾 → 乾=用, 坤=体. **体=坤=Earth.**

This 体 flip is the key to reading all 6 cases consistently.

### Summary table:

本 relation differs by which trigram is 体:
- **Lines 1-3:** 体=乾=Metal, 用=坤=Earth. Earth生Metal → **用生体** (favorable baseline)
- **Lines 4-6:** 体=坤=Earth, 用=乾=Metal. Earth生Metal → **体生用/泄** (unfavorable — 体 drained)

| Line | 動爻 in | 体 | 用 becomes | 本 relation | 互 | 變 relation | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | 坤 | 乾=Metal | 坤→震(Wood) | 用生体 | 巽(Wood)+艮(Earth) | 体克用 | 吉 |
| 2 | 坤 | 乾=Metal | 坤→坎(Water) | 用生体 | 巽(Wood)+离(Fire) | 体生用(泄) | 死 |
| 3 | 坤 | 乾=Metal | 坤→艮(Earth) | 用生体 | — | 用生体 | 吉 |
| 4 | 乾 | 坤=Earth | 乾→巽(Wood) | 体生用(泄) | — | 用克体 | 死 |
| 5 | 乾 | 坤=Earth | 乾→离(Fire) | 体生用(泄) | — | 用生体 | 吉 |
| 6 | 乾 | 坤=Earth | 乾→兑(Metal) | 体生用(泄) | 巽(Wood)+艮(Earth) | 体生用(泄) | 危 |

### Detailed reasoning chains:

**Line 1 (吉):** 坤→震(Wood). 体=乾=Metal. 變用=震Wood: Metal克Wood → **体克用** (favorable). 互巽(Wood)+艮(Earth): Metal克Wood + Earth生Metal → 生体+体克用. "俱是生成之义" — all layers support recovery. Prognosis: "不灾，逢生之日即愈" (no disaster, heals on the day of its生-element).

**Line 2 (死):** 坤→坎(Water). 体=乾=Metal. 變用=坎Water: Metal生Water → **体生用(泄)**. "金入水乡，泄体败金" — Metal drains into Water. 互巽(Wood)+离(Fire): "风火扇炉" — Wind(巽) fans Fire(离), Fire克Metal = **克体**. All layers adversarial: 泄 at 變 + 克体 at 互. "焚尸之象，断之死无疑" — cremation image, certain death.
- Note: "更看占时外应如何" — external omens mentioned but structural verdict is already decisive.
- "以春夏秋冬四季推之" — seasonal 旺衰 adds further specificity.

**Line 3 (吉):** 坤→艮(Earth). 体=乾=Metal. 變用=艮Earth: Earth生Metal → **用生体** (strongly favorable). "俱在生体之义，不问互卦，亦断其吉无疑" — 變 so clearly生体 that 互 can be skipped entirely. **Interpretive shortcut:** when 變 overwhelmingly favors 体, the 互 layer need not be consulted.

**Line 4 (死):** 乾→巽(Wood). 体=坤=Earth. 變用=巽Wood: Wood克Earth → **用克体** (adversarial). "金木俱有克体之义" — 金(乾, original用) was draining 体(Earth生Metal=泄), and now 木(巽, transformed用) directly attacks 体(Wood克Earth=克体). Transformation worsens the situation. "互吉亦凶" — even favorable 互 cannot save this. Trigram imagery locks the verdict: "木有扛尸之义" (wood = coffin bearer), "金为砖椁之推" (metal = burial vault). "必定之推，必定之理" — certain, non-negotiable death.

**Line 5 (吉):** 乾→离(Fire). 体=坤=Earth. 變用=离Fire: Fire生Earth → **用生体** (favorable). "反能生体" — "反" (reversal) because the original 用=乾Metal was draining 体 (体生用=Earth生Metal), but transformation to 离Fire **reverses the polarity**: Fire生Earth = 生体. The harmful drain converts to nourishing support. "互变俱生体" — all layers favor 体. "更有吉兆则愈吉" — external omens amplify.

**Line 6 (危 — critical):** 乾→兑(Metal). 体=坤=Earth. 變用=兑Metal: Earth生Metal → **体生用(泄)** — same draining relation as 本卦, no improvement. 互巽(Wood)+艮(Earth): Wood克Earth = **凶** (巽 attacks 体), Earth比和 = **neutral/吉** (艮 is same element as 体). "一凶一吉" — 互 signals split. "非死必危" (not death but critical). External omens become the tiebreaker: "吉则言吉，凶则言凶."

### Structural observations from the worked example:

1. **互 computed from 變卦, not 本卦:** Verification of Shao's 互 trigrams reveals he computes nuclear trigrams from the **transformed hexagram** (after the moving line flips), not from the original 否. Evidence:
   - Line 1: 否→无妄(hex 25). 互 of 无妄 = 巽/艮. Shao says 巽/艮. ✓ (Same as 本卦's 互, so inconclusive.)
   - Line 2: 否→訟(hex 6). 互 of 訟 = 巽/离. Shao says 巽/离. ✓ (Different from 本卦's 互=巽/艮 — **proves 互 is from 變卦.**)
   - Line 6: 否→萃(hex 45). 互 of 萃 = 巽/艮. Shao says 巽/艮. ✓
   
   This is a methodological departure from the standard atlas-mh framework (which computes 互 from 本卦). In this medical example at minimum, Shao reads the nuclear structure of the **destination state** — the hexagram the situation is evolving toward. Whether this is illness-specific or general 梅花 practice requires further investigation.

2. **互 and 變 interact hierarchically:** When 變 is overwhelmingly clear (line 3: 生体), 互 can be skipped ("不问互卦"). When 變 is mixed (line 6), 互 becomes the tiebreaker. When all layers agree in adversity (line 2), certainty is absolute. When 互 is favorable but 本+變 are both adverse (line 4), 互 cannot rescue ("互吉亦凶").

3. **Trigram imagery adds to 五行 生克:** Lines 2 and 4 invoke specific images (焚尸, 扛尸, 砖椁) that go beyond the 生克 calculation. The imagery provides NARRATIVE confirmation, not additional logical weight. But line 4 shows imagery can lock in a verdict even when 互 is favorable ("木有扛尸之义，金为砖椁之推").

4. **The example teaches the method systematically:** By walking through all 6 lines of one hexagram, Shao Yong shows how the same structural position (乾上坤下) yields 3 吉, 2 死, 1 危 — demonstrating that 動爻 position is the primary discriminator. The instruction "余卦皆仿此断" (all other hexagrams follow this method) confirms this is meant as a template, not special-case reasoning.

5. **体 flips at the trigram boundary** (line 3→4): Lines 1-3 have 体=Metal (favorable baseline: 用生体), lines 4-6 have 体=Earth (unfavorable baseline: 体生用/泄). This means the prognosis systematically worsens for upper-trigram moving lines in this hexagram. The 3吉/2死/1危 split reflects this: all 3 吉 have either favorable baseline (lines 1-3) or polarity reversal (line 5); both 死 are in the unfavorable half (lines 2, 4, though line 2 is also unfavorable despite its favorable baseline due to total adversity at 互+變).

---

## F. Structural Comparison: Illness vs Standard Template

### What the 18-domain template provides (all domains):
1. 體/用 semantic binding (what 體 and 用 represent)
2. 5-relation evaluation (体克用, 用克体, 体生用, 用生体, 比和)
3. Timing via 克應之期

### What 疾病 adds beyond the template:

| Feature | Present in other domains? | Notes |
|---|---|---|
| **旺/衰 as life/death discriminator** | No — other domains use 旺/衰 for degree, not binary outcome | "断无存日" only appears in 疾病 |
| **Pharmacology sub-system** | No | Unique: reads 生体 trigram for medicine type |
| **Spirit diagnosis sub-system** | No | Unique: reads 克体 trigram for supernatural cause |
| **Rescue signal (凶中有救)** | Partial — vol3 line 32 has generic "生体之卦则有救无害" | Illness domain makes it critical: "欲知凶中有救" |
| **Body localization** | No | Unique: which trigram is克'd → body region |
| **Timing split (recovery vs crisis)** | No — other domains have one timing | 和平之日 vs 危厄之期 — two separate timing queries |
| **External omen integration** | Yes — but illness makes it a tiebreaker | "更看占时外应如何" when structural signals are mixed |

### Domains with comparable sub-system richness:
Per atlas-mh findings V.4, only 3 of 18 domains have sub-systems:
- 疾病: **3 sub-systems** (pharmacology, spirit diagnosis, body localization)
- 生產: 1 sub-system (gender determination via 陰/陽 爻 counting)
- 飲食: 1 sub-system (wine/food presence test + companion reading)

疾病 is the richest domain by sub-system count.

### The vol4 character-divination disease layer:

Vol4 (lines 328-333) adds a parallel system for 拆字 (character analysis) illness diagnosis:

| 五行 stroke type | Disease | Spirit |
|---|---|---|
| 金筆多 | Heart/lung, phlegm, visceral disease | 西方金神 |
| 木筆多 | Heart qi, limb disease | 木神林壇 |
| 水筆多 | Diarrhea, vomiting | 水鬼 |
| 火筆多 | Fever, epidemic (but: won't die) | 火鬼 |
| 土筆多 | Spleen/stomach, sores, pain | 伏尸鬼 (but: will die) |

Note the asymmetry: 火筆多 → won't die (fire=yang=vitality), 土筆多 → will die (earth=yin=burial). This adds a prognostic rule absent from the trigram system.

---

## Summary of illness-specific information content

The medical domain is the most informationally dense of the 18 domains. It adds three complete sub-systems to the standard template:

1. **Pharmacology** — maps 生体 trigram → drug thermal quality (via TCM 四气, partially but not fully derivable from 五行)
2. **Spirit diagnosis** — maps 克体 trigram → supernatural cause (via trigram 象, NOT derivable from 五行)
3. **Body localization** — maps 受克 trigram → body region (via 說卦 body correspondence, a separate system from 五行→organ)

Plus two structural escalations:
4. **旺/衰 → life/death binary** (other domains: degree modifier; illness: absolute discriminator)
5. **Dual timing** (recovery date vs crisis date, separate calculations)

The net effect is that illness divination operates on **more channels simultaneously** than any other domain: the standard 體/用 arc + pharmacology channel + spirit channel + body-region channel + external-omen tiebreaker. This is consistent with medicine being the highest-stakes application — more information channels are activated when the reading concerns survival.

---

## G. 互(本) vs 互(變): Cross-Example Verification

Section E observation 1 noted that Shao Yong's illness worked example (vol2 line 94) computes 互 from the 變卦, not the 本卦. This contradicts the atlas-mh framework. Systematic verification against ALL worked examples that name specific 互 trigrams:

### Method
For each worked example, compute 互(本) and 互(變). Cases where 互(本) = 互(變) are inconclusive (lines 1, 6, and cases where the moving line doesn't affect lines 2-5). Decisive cases are where 互(本) ≠ 互(變) — the text's named trigrams disambiguate.

### Results

| Source | Hexagram | Line | 互(本) | 互(變) | Text says | Match |
|---|---|---|---|---|---|---|
| vol3 line 13 | 革→咸 | 1 | 巽/乾 | 巽/乾 | 巽 | INCON |
| vol3 line 18 | 履→乾 | 3 | 离/巽 | 乾/乾 | 巽+离 | **→本** |
| vol3 line 22 | 归妹→睽 | 6 | 离/坎 | 离/坎 | 坎+离 | INCON |
| vol3 line 24 | 夬→兑 | 3 | 乾/乾 | 离/巽 | 乾 | **→本** |
| vol3 line 163 | 泰→升 | 1 | 兑/震 | 兑/震 | 震+兑 | INCON |
| vol3 line 164 | 鼎→恒 | 6 | 乾/兑 | 乾/兑 | 乾+兑 | INCON |
| vol2 line 233 | 井→升(田) | 5 | 兑/离 | 兑/震 | 离+兑 | **→本** |
| vol2 line 234 | 丰→震(王) | 3 | 巽/兑 | 艮/坎 | 兑+巽 | **→本** |
| vol2 line 235 | 益→中孚(韩) | 2 | 坤/艮 | 震/艮 | 艮+坤 | **→本** |
| **vol2 line 94** | **否 line 2** | **2** | **艮/巽** | **离/巽** | **巽+离** | **→變** |

### Verdict

**5 decisive matches for 互(本), 1 for 互(變).** The standard 梅花 method computes 互 from the 本卦. The illness worked example (vol2 line 94, 否 line 2) is the sole exception.

**Possible explanations for the anomaly:**
1. **Textual error** — a scribe wrote 离 where 艮 was intended. 本卦 互 = 艮/巽; switching 艮→离 would produce the stated 巽/离.
2. **Deliberate medical variant** — Shao Yong used 互(變) in the illness context to read the structure of the state the disease evolves toward (the "destination state"). This would be a domain-specific methodological choice.
3. **Dual 互 reading** — Shao may have computed both 互(本) and 互(變), selecting whichever produced the more narratively consistent reading for that particular case.

Given the 5:1 ratio, the atlas-mh framework's assumption that 互 comes from 本卦 is **confirmed as the standard practice**. The illness example's divergence requires noting but does not overturn the general rule.
