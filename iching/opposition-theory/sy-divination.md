# Shao Yong Divination System — 梅花易數 Analysis

## The State Space

384 distinct states: 8 (upper trigram) × 8 (lower trigram) × 6 (moving line). Every casting maps a phenomenon into one of these states — one line-position in the complete Yi. The moving line determines which trigram is 体 (body/self) and which is 用 (function/event), then five-phase 生克 logic evaluates the interaction across four layers.

---

## Two Casting Modes

### 先天 (Pre-heaven): Number → Hexagram

Start from countable data (date, strokes, sounds, measurements), derive the hexagram through modular arithmetic:
- Upper trigram: count mod 8
- Lower trigram: (count + hour) mod 8
- Moving line: total mod 6

The hexagram is fully determined by the data. No randomization step. The timestamp IS the hexagram. The claim: the moment you ask already encodes the answer; the arithmetic just makes it legible.

### 後天 (Post-heaven): Phenomenon → Hexagram

The event carries its own trigram identity. Old man = 乾, direction = 巽, cow = 坤, falling branch = 离. The world hands you the hexagram directly; only the moving line still requires computation (trigram numbers + hour, mod 6).

後天 is hybrid: 2 of 3 coordinates from perception, 1 from arithmetic.

### The Relationship

先天 = structured/mechanical. 後天 = perceptual/immediate. The ti/yong split applied to method itself. 先天 works when you have data but no vivid event. 後天 works when the event is vivid enough to be its own trigram. Both land in the same 384-space.

---

## The Casting Funnels

Every method is a different projection from world → Z₈ × Z₈ × Z₆:

| Method | Upper trigram | Lower trigram | Moving line |
|--------|-------------|---------------|-------------|
| Date/time | year+month+day mod 8 | same + hour mod 8 | total mod 6 |
| Object count | count mod 8 | hour mod 8 | (count+hour) mod 6 |
| Sound | sound-count mod 8 | hour mod 8 | total mod 6 |
| Words (even) | first half mod 8 | second half mod 8 | total mod 6 |
| Words (odd) | fewer chars mod 8 | more chars mod 8 | total mod 6 |
| Characters (1-3) | left strokes mod 8 | right strokes mod 8 | total mod 6 |
| Characters (4+) | tonal values mod 8 | tonal values mod 8 | total mod 6 |
| Measurement | zhang mod 8 | chi mod 8 | total mod 6 |
| Person/object | trigram-attribute | direction/context | total mod 6 |

The hour always enters the lower trigram or the line — the grounding anchor that differentiates otherwise identical situations.

### Character Casting Threshold

1-3 characters: spatial (stroke geometry, left/right split). 4+ characters: acoustic (tonal register — 平=1, 上=2, 去=3, 入=4). The encoding shifts from visual to phonological at the complexity threshold.

---

## The Interpretive Circuit

After casting, four layers evaluate in sequence:

```
本卦 (present)  →  体 vs 用: five-phase 生克  →  overall fortune
互卦 (middle)   →  middle 4 lines split into two trigrams  →  what amplifies or dampens
变卦 (outcome)  →  hexagram after moving line flips  →  resolution
象 (images)     →  trigram symbolism overlaid  →  narrative content (who/what/where)
```

The 生克 chain gives **valence** (good/bad/mixed). The trigram images give **content** (who/what/how). Both are required.

### 体/用 Assignment

The trigram containing the moving line is 用 (active, the event acting on you). The other is 体 (passive, the subject). This single cut determines perspective — everything that follows is evaluated from 体's standpoint.

### The 生克 Evaluation

For each layer, check the five-phase relationship to 体:
- **生体** (generates body): beneficial
- **克体** (overcomes body): harmful
- **体克用** (body overcomes function): body dominates, favorable
- **体生用** (body generates function): body is drained, unfavorable
- **比和** (same phase): harmonious

The layers stack: 互 amplifies or dampens the 本 reading, 变 determines whether the situation resolves well or badly.

### Optional: Yi Line Text

先天 method: "止以卦論，不甚用易之爻辭" — judge by trigram logic alone, don't rely on line texts.
後天 method: use the line text as additional evidence, alongside the trigram logic.

---

## The Trigger Problem

### What Initiates a Casting

"不動不占，不因事不占" — no movement, no casting; no cause, no casting.

The calendar runs continuously but only gets applied when an anomaly punctures the observer's attention. The hexagram is the temporal address of the disruption.

### Significance Detection

Not formalized. Three loose criteria emerge from the examples:

1. **Anomaly**: deviation from natural baseline — branch falls without wind, bird falls to ground, cow cries with extreme sorrow
2. **Intrusion**: arrives uninvited into the perceptual field — you're not looking for it, it finds you
3. **Affect**: emotional charge in the phenomenon — worry on the old man's face, joy on the young man's, grief in the cow's cry

The 三要灵应篇 frames it through three faculties: 耳 (ear), 目 (eye), 心 (heart-mind), operating in 虛靈 (emptiness-sensitivity). "思慮未動，鬼神不知；不由乎我，更由乎誰？" — before thought stirs, even ghosts can't know; if it doesn't originate from me, then from whom?

Significance detection is treated as a cultivated skill (心易), not an algorithm. The system formalizes everything after the moment of recognition but leaves recognition itself to the practitioner.

---

## Timing (克應之期)

The total number from the casting determines the response period, modulated by the observer's state at the moment of casting:

- **Walking** (行): fast response → halve the number
- **Sitting** (坐): slow response → double the number
- **Standing** (立): moderate → use the number as-is

The unit (days/months/years) depends on the nature of the question — ephemeral events use days, durable situations use years.

---

## The Remedial Principle

The system is bidirectional: read signs, but also write corrections. The 西林寺 example: the temple plaque's 林 character lacks two strokes, producing hexagram 剝 (stripping, decay). Adding the strokes changes the hexagram to 損 (decrease leading to increase), with生体 relationships throughout. The monks add the strokes; the trouble ceases.

This implies the semiotic mapping is not just diagnostic but operative — changing the sign changes the situation. The hexagram space is not read-only.

---

## 推數又須明理

"Pushing numbers must also illuminate principle."

The foundational methodological statement (from the axe/hoe example). A son casts and reads "metal + wood = long-handled metal tool" → hoe. The master corrects: it's evening, who needs a hoe at night? It's an axe for splitting firewood.

The numbers narrow the space; reason (理) selects within it. Numerically equivalent readings are disambiguated by context, season, time, practical logic. The system is number + perception + context, not number alone. A pure formalist reading is explicitly rejected.

---

## Key Worked Examples

### 觀梅占 (Plum Blossom) — 先天

辰年十二月十七日申時. Two sparrows fight and fall from plum tree.

- (5+12+17) mod 8 = 2 → 兑; (34+9) mod 8 = 3 → 离; 43 mod 6 = 1 → line 1
- 泽火革, line 1 moves → 泽山咸. 互: 乾, 巽
- 体 = 兑金 (no moving line). 用 = 离火 (has moving line)
- 离火克兑金 → harm. 互巽木生离火 → amplified harm. 变艮土生兑金 → rescue
- 兑 = young woman, 巽 = thigh, 乾金克巽木 → thigh injured, 艮 saves → not fatal
- Result: next evening, girl picks flowers, gardener chases her, she falls, injures her thigh

### 老人有忧色 (Old Man with Worry) — 後天

己丑日卯時. Old man walking toward southeast, worry visible on face.

- Old man = 乾 (upper), 巽 direction (lower). Moving: (1+5+4) mod 6 = 4 → line 4
- 天風姤, line 4 moves → 重巽. 互: 重乾
- 体 = 巽木. 用 = 乾金. 乾克巽 → harm. 互重乾 → doubled harm. 並無生氣
- Yi text 姤九四: "包無魚，起凶"
- Walking → halve total (10/2) = 5 days
- Result: 5 days later, old man chokes on fish bone at a banquet and dies. "無魚" in the text; fish as instrument of death.

---

## Structural Observations

### The Calendar as Address Space

先天 treats the sexagenary calendar as a coordinate system. Each moment has a hexagram address. The casting reads the address; the event selects which moment to read. The calendar is Shao Yong's temporal grid (Huangji Jingshi) applied at the scale of individual moments rather than cosmic epochs.

### 後天 as Compressed Perception

後天 bypasses the calendar for 2 of 3 coordinates, letting the phenomenon carry its own trigram identity. This requires the observer to perceive in trigram categories — to see an old man and register 乾, not "elderly male." The eight trigrams function as perceptual primitives, a trained phenomenological vocabulary.

### Absence of Randomization

Neither method uses a random process (coins, yarrow stalks). This is a deliberate departure from the Zhouyi tradition. The philosophical claim: if the world already has hexagram structure, randomization is unnecessary — you just need to read what's already there. Casting becomes perception, not chance.

### The Bidirectional Claim

Reading signs and writing corrections (西林寺 example) implies the mapping between hexagram space and world is not merely epistemic but causal — or at least, that the semiotic and the real share enough structure that modifying one modifies the other. This is the strongest metaphysical claim in the system.

---

## Vol 2: The Interpretive Theory (体用生克篇)

### 心易 — The Anti-Literalist Principle

The volume opens by rejecting fixed trigram-to-referent mapping. Getting 革 today and seeing a girl pick flowers does NOT mean 革 always means girl-picks-flowers. 兑 is not only "young woman"; 乾 is not only "horse." Trigram images are categories with multiple valid instantiations. The practitioner selects the right one from context. "占卜之道，要变通。得变通之道者，在乎心易之妙耳。"

### The Decision Procedure (Explicit Priority Order)

1. Check the Zhou Yi line text (爻辞) for the moving line
2. Evaluate 体/用 five-phase 生克
3. Read external 克應 (omens at the moment)
4. Assess the observer's own state (sitting/walking/standing/lying)

"必须以易卦为主，克应次之" — hexagram is primary, external omens secondary. When they conflict, the hexagram wins. When both agree, the verdict is strong.

### 体一用百 — One Body, Hundred Functions

体 is singular: you, the subject. Everything else is 用: the event trigram, both 互 trigrams, the 变 trigram, all ten external response channels. The circuit is 1:N, not 1:1. Every element in the hexagram and environment is evaluated from the one 体 perspective.

### When 体/用 Fails — The Structural Override

西林寺: all trigrams are 比和 (harmonious) → should be auspicious, but a pure-yang dwelling (monastery) with pure-yin hexagram (剥, all yin lines) = structural contradiction. "群陰剥陽之义显然也。此理甚明，不必拘体用也。" When the hexagram's structural meaning directly conflicts with the mechanical 生克 verdict, structure wins. The 生克 engine is the default; the hexagram's symbolic identity is the exception handler.

### 先天 vs 後天 — Formal Boundary

先天: "辞前之易" — the Yi before texts existed. Judge by trigram logic alone; don't use line texts.
後天: "辞后之易" — the Yi after texts. Use both line texts and trigram logic.

Explicit prohibition against mixing in 六十甲子 calendar astrology: "历象选时，并于《周易》不相干涉，不可用也." Keep the systems clean.

### The Eighteen Application Domains

Eighteen templates, all running the same 体/用 生克 engine with different semantic bindings:

| Domain | 体 = | 用 = | Special rules |
|--------|-------|-------|---------------|
| Weather | — | all trigrams | No 体/用 split; trigrams vote as committee |
| Human affairs | self | situation | Standard 生克 |
| Household | self | the house | Standard |
| Marriage | one's family | other family | Trigram象 gives appearance of spouse |
| Childbirth | mother | child | 陽爻多=boy, 陰爻多=girl |
| Food/drink | self | the meal | 坎=wine, 兑=food |
| Wealth | self | money | 生体 date = gain; 克体 date = loss |
| Lost objects | self | object | 变卦 direction = search location |
| Illness | patient | disease | 生体 trigram = medicine type |
| Litigation | self | opponent | Standard |
| Graves | self | burial site | Standard |

**Weather** is the sole exception to 体/用 — it reads the entire hexagram as a weather committee. Multiple trigrams of one type amplify (重坎 = heavy rain). Trigrams suppress each other by 克: many 乾兑 (metal) → 震 has no thunder, 巽 has no wind (metal克wood). This is the 生克 engine applied at the trigram-population level rather than the body-function level.

**Illness** extends into three sub-systems:
- Spirit diagnosis: each 克体 trigram maps to a ghost/deity class by direction and death-manner
- Pharmacology: 生体 trigram determines medicine (离→hot, 坎→cold, 艮→warming, 乾兑→cooling)
- The 乾坤 walkthrough: same hexagram (天地否), all six moving lines traced, showing opposite outcomes (life vs death) from the same hexagram — proving the 384 states are genuinely distinct

**Lost objects** uses 变卦 as a spatial compass: 乾→northwest/high ground, 坤→southwest/fields, 坎→water's edge, 离→south/kitchen, etc.

### 三要灵应篇 — The Perceptual Theory

The philosophical center of the system. Lineage: 鬼谷子 → 严君平 → 东方朔 → 诸葛孔明 → 邵康节 → ... → 朱清灵子 (author of the preface, 宝庆四年/1228).

**The Ontological Claim**: "《易》者，性理之学也。性理，具于人心者也。" The Yi is the study of nature-principle; nature-principle is intrinsic to the human heart-mind. When the mind is clear ("方寸湛然，灵台皎洁"), the Yi exists fully within it — this IS the pre-heaven Yi. Thought arising obscures it "如云之蔽室，如尘之蒙镜."

**The Three Faculties**: 耳 (ear), 目 (eye), 心 (heart-mind), operating in 虚灵 (empty sensitivity). "必使视之不见，吾见之；听之不闻者，吾闻之" — perceive what others miss.

**The Response Catalog** — a taxonomy of sign→meaning across perceptual channels:

- **天文**: clouds clearing = success; fog = obscuration; rain on clothes = receiving grace
- **地理**: double mountains = blocked; flowing water = proceeding; dry marsh = exhaustion
- **人品**: officials→rank; merchants→wealth; crying children→offspring worry; monks→solitude
- **身体**: waving hand = don't; shaking head = refusal; kneeling = submission
- **器物**: chess = strategy; lock = obstruction; mirror = responding to a summons
- **草木**: orchid = auspicious; pine = longevity; young shoots = ephemeral
- **禽兽**: crow = disaster; magpie = joy; geese = letters; carp leaping = transformation
- **拆字**: stone+skin = 破; person+wood = 休 (character decomposition as omen)
- **叶音**: 鹿=禄 (deer/salary); 蜂=封 (bee/enfeoffment); 梨=離 (pear/separation); 鞋=諧 (shoe/harmony)

**The Resonance Principle**: "我心忧者，彼事亦忧；我心乐者，彼事亦乐." The observer's internal state at the moment of casting is signal, not noise. Your emotion is a direct readout of the querent's situation.

### 十应 — The Ten Response Channels

Formalizes ten categories of 用 input, each evaluated against 体 by 生克:

1. 正应 — the 本卦
2. 互应 — the 互卦
3. 变应 — the 变卦
4. 日应 — the day's elemental quality
5. 刻应 — omens at the casting instant
6. 外应 — objects/people appearing
7. 天时应 — current weather
8. 地理应 — physical environment
9. 人事应 — human activities nearby
10. 方应 — querent's directional position

**The Inversion Principle (十应奥论)**: 三要 and 十应 can give opposite verdicts. Gold = auspicious in 三要, but if 体 is wood, metal克wood = harmful. Coffin = death in 三要, but if 体 is fire, wood生fire = recovery. The 体/用 生克 logic always overrides naive sign reading. "内卦不可无外卦，外卦不可无内卦."

### 向背 — The Directional Vector

Omens have direction. Crow flying toward you = disaster approaching. Crow flying away = disaster already past. A 生体 object arriving = good fortune coming; departing = good fortune spent. Adds a temporal arrow (approaching/receding) to the spatial omen.

### 静占 — Graceful Degradation

In a quiet room with nothing to see or hear, there are no external 用 channels. Drop all external response logic; use only the hexagram's internal 体/用 生克 plus seasonal 衰旺. The system degrades gracefully to its core engine when perceptual input is absent.

### 观物洞玄歌 — Dwelling Assessment

The 三要 method applied to passive observation rather than specific casting. Walk into someone's home and read its state directly from physical signs: spring-like atmosphere = prosperity; cold/autumn feel = decline; fragrance = blessing; filth = poverty. A verse catalog — no hexagram needed, pure pattern-recognition on environmental cues.

### The Surname Fix (起卦加数例)

Three families building houses on the same day/hour get the same hexagram. Solution: add surname stroke count to the date numbers. Different surnames → different hexagrams → different predictions. Explicit acknowledgment that the calendar alone is insufficient for individuated prediction — personal identity must enter the arithmetic. Extends to marriage (add both surnames), and for nameless persons, use the sound of their designation.

### Lifespan Calculation

For durable things (houses, graves), the total casting number gives lifespan in years. The 克体 trigram determines what destroys it (兑=metal/demolition, 离=fire). Three houses from the surname example: 29 years (田), 22 years then fire (王), 31 years then metal-year destruction (韩). The 生克 circuit predicts not just whether but when and how.

## Vol 3: Detailed Manual
Details in text

---

## The Underlying Operation

Across all five volumes — hexagram casting, trigram interpretation, character divination, object reading — the same operation repeats:

```
perceive form  →  type by category  →  evaluate interaction  →  read in temporal context
```

### The Four Steps

**1. Perceive Form** — Input acquisition. The system accepts anything as input: a date (vol 1 先天), a falling bird (vol 1 後天), a written character (vols 4-5), a physical object (vol 5 格物章), environmental cues (vol 2 三要), a person's appearance (vol 2 人品). The surface varies completely. The operation doesn't care what the input is — only that something has entered the perceptual field with enough salience to trigger attention.

**2. Type by Category** — Classification into the combinatorial vocabulary. Every input is decomposed into elements from a small set of type systems:

| System | Categories | Applied to |
|--------|-----------|------------|
| 八卦 (trigrams) | 8 | phenomena, character regions, objects |
| 五行 (five phases) | 5 | trigrams, stroke shapes, seasons, directions |
| 六神 (six spirits) | 6 | stroke patterns (vols 4-5) |
| 星神 (star spirits) | ~15 | sub-character components (vol 5) |

These stack: a single stroke can be typed as a trigram region (spatial), a five-phase element (shape), a six-spirit (pattern), and a star spirit (identity) simultaneously. A natural phenomenon gets typed as a trigram directly. The typing step maps unlimited input diversity onto a finite combinatorial space.

**3. Evaluate Interaction** — The 生克 engine. Once typed, elements interact through five-phase logic:

- 生 (generates): wood→fire→earth→metal→water→wood
- 克 (overcomes): wood→earth→water→fire→metal→wood

One element is designated 体 (self/subject), everything else is 用 (function/other). The evaluation is always from 体's perspective: what generates 体 is beneficial, what overcomes 体 is harmful, what 体 generates drains 体, what 体 overcomes favors 体.

The 体 designation is the critical cut. In hexagram divination, arithmetic determines it (which trigram holds the moving line = 用). In character divination, the diviner's judgment determines it (which stroke represents the matter asked about = 用神; the querent's birth element = 主神/体). Same function, different assignment mechanism.

**4. Read in Temporal Context** — When and how the verdict manifests. Seasonal 衰旺 (strength/weakness) modulates the five-phase interaction: wood is strong in spring, weak in autumn. The casting total gives the response period. The 60×12 timing table (vol 5) gives hour-level precision. The observer's kinetic state (sitting/standing/walking) scales the timing.

### What Changes Across Volumes

| | Input | Typing | 体 assignment | Interaction engine |
|--|-------|--------|--------------|-------------------|
| Vols 1-3 (hexagram) | phenomena, numbers | trigrams via arithmetic or perception | moving line determines | 五行 生克 |
| Vols 4-5 (character) | handwriting | stroke shape → 五行/六神/星神 | diviner's judgment selects | 五行 生克 |
| Vol 5 (object) | physical things | object symbolism → 五行 | context determines | 五行 生克 |

The input funnel and typing method change completely. The interaction engine never changes. The 体/用 structure never changes. The temporal modulation never changes. The volumes describe different **front ends** feeding the same **back end**.

### The Skill Gradient

The operation has a mechanical core (五行 生克 evaluation, mod arithmetic, timing tables) and a perceptual periphery (significance detection, trigram perception, stroke reading, contextual override). The mechanical core can be taught algorithmically. The perceptual periphery cannot — it requires 心易 (heart-Yi), the trained capacity to perceive the world in the system's categories and to select the right instantiation from context.

Vol 2's 推數又須明理 states this directly: numbers narrow the space, reason selects within it. The system is designed with a hard algorithmic skeleton and a soft perceptual skin. The skeleton is the same across all volumes; the skin is what differentiates master from student.

### The Bidirectional Claim

The operation runs in both directions. Forward: perceive → type → evaluate → predict. Reverse: choose desired state → construct the appropriate sign → alter the situation (西林寺 example, vol 1). If the typing is a genuine structural mapping (not merely epistemic), then modifying the sign modifies the typed reality. This is the system's strongest metaphysical commitment and the foundation of its remedial applications.

