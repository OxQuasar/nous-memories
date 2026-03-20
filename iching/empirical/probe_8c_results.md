# Probe 8c: 梅花易數 18-Domain Decision Table Analysis

Source: `memories/texts/meihuajingshu/vol2.txt` lines 44–99

## 1. Complete 18-Domain Table

| # | Domain | 体用? | 体= | 用= | 体克用 | 用克体 | 体生用 | 用生体 | 比和 | Subsys? |
|---|--------|-------|-----|-----|--------|--------|--------|--------|------|---------|
| 1 | 天時占 | ✗ | — | — | — | — | — | — | — | ✓ |
| 2 | 人事占 | ✓ | 主 (sel | 宾 (the m | + | - | - | + | + | ✓ |
| 3 | 家宅占 | ✓ | 主人 (ow | 家宅 (hous | + | - | - | + | + |  |
| 4 | 屋舍占 | ✓ | 主人 (ow | 屋舍 (dwel | + | - | - | + | + |  |
| 5 | 婚姻占 | ✓ | 所占之家 ( | 婚姻/所婚之家  | +~ | - | - | + | + | ✓ |
| 6 | 生產占 | ✓ | 母 (mot | 生/子 (chi | - | - | + | + | + | ✓ |
| 7 | 飲食占 | ✓ | 主 (sel | 饮食 (food | - | - | - | + | + | ✓ |
| 8 | 求謀占 | ✓ | 主 (sel | 所谋之事 (th | +~ | - | - | + | + |  |
| 9 | 求名占 | ✓ | 主 (sel | 名 (fame/ | +~ | - | - | + | + | ✓ |
| 10 | 求財占 | ✓ | 主 (sel | 财 (wealt | + | - | - | + | + | ✓ |
| 11 | 交易占 | ✓ | 主 (sel | 财 (goods | + | - | - | + | + |  |
| 12 | 出行占 | ✓ | 主 (sel | 所行之应 (jo | + | - | - | + | + | ✓ |
| 13 | 行人占 | ✓ | 主 (sel | 行人 (trav | +~ | - | - | + | + | ✓ |
| 14 | 謁見占 | ✓ | 主 (sel | 所见之人 (pe | + | - | - | + | + |  |
| 15 | 失物占 | ✓ | 主 (own | 失物 (lost | +~ | - | - | + | + | ✓ |
| 16 | 疾病占 | ✓ | 病人 (pa | 病症 (illn | + | - | - | + | + | ✓ |
| 17 | 官訟占 | ✓ | 主 (sel | 对辞之人/官讼  | + | - | - | + | + |  |
| 18 | 墳墓占 | ✓ | 主 (sel | 坟墓 (grav | + | - | - | + | + |  |

**Valence key:** `+` = favorable, `-` = unfavorable, `+~` = weak positive (qualified/delayed)

### Detailed Relation Texts

**1. 天時占** (Weather) — lines 44-46
- **Does NOT use 体用.** Entirely different system: counts trigram occurrences across 本/互/变. 离→晴, 坎→雨, 坤→阴晦, 乾→晴明, 震→雷, 巽→风, 艮→止雨, 兑→阴. Also references specific hexagrams (泰/否/既济/未济 etc.) and seasonal modifiers.

**2. 人事占** (Human Affairs) — lines 47-49
- 体 = 主 (self/querent), 用 = 宾 (the matter/other)
- 体克用 [+]: 则吉
- 用克体 [-]: 不宜
- 体生用 [-]: 有耗失之患
- 用生体 [+]: 有进益之喜
- 比和 [+]: 谋为吉利
- **Subsystem:** References the 8-trigram 生体/克体 detail tables (vol2 lines 25-41).

**3. 家宅占** (Household) — lines 50-51
- 体 = 主人 (owner), 用 = 家宅 (household)
- 体克用 [+]: 家宅多吉
- 用克体 [-]: 家宅多凶
- 体生用 [-]: 多耗散，或防失盗之忧
- 用生体 [+]: 多进益，或有馈送之喜
- 比和 [+]: 家宅安稳

**4. 屋舍占** (Dwelling) — lines 52-53
- 体 = 主人 (owner), 用 = 屋舍 (dwelling)
- 体克用 [+]: 居之吉
- 用克体 [-]: 居之凶
- 体生用 [-]: 主资财衰退
- 用生体 [+]: 则门户兴隆
- 比和 [+]: 自然安稳

**5. 婚姻占** (Marriage) — lines 54-64
- 体 = 所占之家 (querent's family), 用 = 婚姻/所婚之家 (marriage/other family)
- 体克用 [+~]: 可成但成之迟
- 用克体 [-]: 不可成，成亦有害
- 体生用 [-]: 婚难成，或因婚有失
- 用生体 [+]: 婚易成，或因婚有得
- 比和 [+]: 婚姻吉利
- **Subsystem:** Family strength comparison (体旺/用旺); appearance descriptions per trigram (lines 57-64).

**6. 生產占** (Childbirth) — lines 65-66
- 体 = 母 (mother), 用 = 生/子 (child)
- 体克用 [-]: 不利于子
- 用克体 [-]: 不利于母
- 体生用 [+]: 利于子
- 用生体 [+]: 利于母
- 比和 [+]: 生育顺快
- **Subsystem:** Male/female determination (阳卦阳爻→男, 阴卦阴爻→女); timing via 用卦 气数.

**7. 飲食占** (Food/Drink) — lines 67-69
- 体 = 主 (self), 用 = 饮食 (food/drink)
- 体克用 [-]: 饮食有阻
- 用克体 [-]: 饮食必无
- 体生用 [-]: 饮食难就
- 用生体 [+]: 饮食必丰
- 比和 [+]: 饮食丰足
- **Subsystem:** 坎=酒, 兑=食 (坎 present→wine, 兑 present→food); 互卦 for guest identification.

**8. 求謀占** (Planning) — lines 70-71
- 体 = 主 (self), 用 = 所谋之事 (the plan)
- 体克用 [+~]: 谋虽可成，但成迟
- 用克体 [-]: 求谋不成，谋亦有害
- 体生用 [-]: 多谋少遂
- 用生体 [+]: 不谋而成
- 比和 [+]: 求谋称意

**9. 求名占** (Seeking Office) — lines 72-73
- 体 = 主 (self), 用 = 名 (fame/office)
- 体克用 [+~]: 名可成，但成迟
- 用克体 [-]: 名不可成
- 体生用 [-]: 名不可就，或因名有丧
- 用生体 [+]: 名易成，或因名有得
- 比和 [+]: 功名称意
- **Subsystem:** Timing via 生体 卦气; location via 变卦 方道; in-office danger rules (克体→祸).

**10. 求財占** (Seeking Wealth) — lines 74-76
- 体 = 主 (self), 用 = 财 (wealth)
- 体克用 [+]: 有财
- 用克体 [-]: 无财
- 体生用 [-]: 财有损耗之忧
- 用生体 [+]: 财有进益之喜
- 比和 [+]: 财利快意
- **Subsystem:** Timing: 生体 卦气 → gain date, 克体 卦气 → loss date.

**11. 交易占** (Trade) — lines 77-78
- 体 = 主 (self), 用 = 财 (goods/trade)
- 体克用 [+]: 有财
- 用克体 [-]: 不成
- 体生用 [-]: 难成，或因交易有失
- 用生体 [+]: 即成，成必有财
- 比和 [+]: 易成

**12. 出行占** (Travel) — lines 79-81
- 体 = 主 (self), 用 = 所行之应 (journey outcome)
- 体克用 [+]: 可行，所至多得意
- 用克体 [-]: 出则有祸
- 体生用 [-]: 出行有破耗之失
- 用生体 [+]: 有意外之财
- 比和 [+]: 出行顺快
- **Subsystem:** Trigram-specific: 乾/震→动, 坤/艮→不动, 巽→舟行, 离→陆行, 坎→失脱, 兑→纷争.

**13. 行人占** (Traveler Return) — lines 82-84
- 体 = 主 (self/home), 用 = 行人 (traveler)
- 体克用 [+~]: 行人归迟
- 用克体 [-]: 行人不归
- 体生用 [-]: 行人未归
- 用生体 [+]: 行人即归
- 比和 [+]: 归期不日矣
- **Subsystem:** 用卦 reads traveler's external condition; trigram-specific modifiers.

**14. 謁見占** (Audience/Meeting) — lines 85-86
- 体 = 主 (self), 用 = 所见之人 (person to meet)
- 体克用 [+]: 可见
- 用克体 [-]: 不见
- 体生用 [-]: 难见，见之而无益
- 用生体 [+]: 可见，见之且有得
- 比和 [+]: 欢然相见

**15. 失物占** (Lost Object) — lines 87-89
- 体 = 主 (owner), 用 = 失物 (lost object)
- 体克用 [+~]: 可寻迟得
- 用克体 [-]: 不可寻
- 体生用 [-]: 物难见
- 用生体 [+]: 物易寻
- 比和 [+]: 物不失矣
- **Subsystem:** 变卦 → object location (8-trigram direction table, lines 89).

**16. 疾病占** (Illness) — lines 90-94
- 体 = 病人 (patient), 用 = 病症 (illness)
- 体克用 [+]: 病易安；勿药有喜
- 用克体 [-]: 虽药无功
- 体生用 [-]: 迁延难好
- 用生体 [+]: 即愈
- 比和 [+]: 疾病易安
- **Subsystem:** Medicine type (离→热药, 坎→冷药, 艮→温补, 乾兑→凉药); ghost/spirit attribution (8-trigram 克体→spirit table, lines 92); detailed 6-line example for 天地否 (lines 93-94).

**17. 官訟占** (Litigation) — lines 95-96
- 体 = 主 (self), 用 = 对辞之人/官讼 (opponent/lawsuit)
- 体克用 [+]: 已胜人
- 用克体 [-]: 人胜己
- 体生用 [-]: 非为失理，或因官有所丧
- 用生体 [+]: 不止得理，或因讼有所得
- 比和 [+]: 官讼最吉，必有主和之义

**18. 墳墓占** (Burial) — lines 97-98
- 体 = 主 (self/descendants), 用 = 坟墓 (grave/burial site)
- 体克用 [+]: 葬之吉
- 用克体 [-]: 葬之凶
- 体生用 [-]: 葬之主运退
- 用生体 [+]: 葬之主兴隆，有荫益后嗣
- 比和 [+]: 乃为吉地，大宜葬

## 2. H1: Template Uniformity

**Standard template** (from vol2 体用总诀, lines 10/24):

| Relation | Standard valence |
|----------|-----------------|
| 体克用 | + |
| 用克体 | - |
| 体生用 | - |
| 用生体 | + |
| 比和 | + |

**10/17 体用-domains** match the standard template exactly.
**7/17** deviate.

### Deviations

**5. 婚姻占:**
- 体克用: standard=+, actual=+~ — "可成但成之迟"

**6. 生產占:**
- 体克用: standard=+, actual=- — "不利于子"
- 体生用: standard=-, actual=+ — "利于子"

**7. 飲食占:**
- 体克用: standard=+, actual=- — "饮食有阻"

**8. 求謀占:**
- 体克用: standard=+, actual=+~ — "谋虽可成，但成迟"

**9. 求名占:**
- 体克用: standard=+, actual=+~ — "名可成，但成迟"

**13. 行人占:**
- 体克用: standard=+, actual=+~ — "行人归迟"

**15. 失物占:**
- 体克用: standard=+, actual=+~ — "可寻迟得"

### Structural Analysis of Deviations

**Domain 6 (生產/Childbirth):** Both 体克用 and 体生用 invert. The evaluation shifts from 体's welfare to the *child's* welfare. 体克用 (mother attacks child → bad) and 体生用 (mother nourishes child → good) — a perspective flip, not a rule violation.

**Domain 7 (飲食/Food):** 体克用 inverts (体 overpowers the food → food obstructed). In standard: 体 dominating 用 = good. In food: 体 suppressing 用(food) = no food. The semantics of 用 shift: 用 is something you *want to receive*, not something you compete with.

**Domains 5,8,9,13,15 (婚姻/求謀/求名/行人/失物):** 体克用 gives a *weak positive* (+~): "可成但成之迟" / "可寻迟得" / "归迟". The delay pattern is consistent: 体 overpowers 用, so the outcome arrives but slowly.

## 3. H2: Relation Ordering

**Standard order:** 体克用 → 用克体 → 体生用 → 用生体 → 比和
**11/17** use the standard order.
**6/17** use a different order.

### Non-standard orderings

| # | Domain | Order | First relation |
|---|--------|-------|----------------|
| 2 | 人事占 | 用克体 → 体克用 → 用生体 → 体生用 → 比和 | 用克体 |
| 5 | 婚姻占 | 用生体 → 体生用 → 体克用 → 用克体 → 比和 | 用生体 |
| 6 | 生產占 | 体克用 → 用克体 → 用生体 → 体生用 → 比和 | 体克用 |
| 7 | 飲食占 | 用生体 → 体生用 → 体克用 → 用克体 → 比和 | 用生体 |
| 8 | 求謀占 | 体克用 → 用克体 → 用生体 → 体生用 → 比和 | 体克用 |
| 16 | 疾病占 | 体克用 → 体生用 → 用克体 → 用生体 → 比和 | 体克用 |

**Pattern:** The majority (12/17) use the standard 体克用-first order. The 5 deviations cluster into two patterns:
- **用克体-first** (domain 2): puts the adversarial outcome first
- **用生体-first** (domains 5, 7): starts with the best-case outcome
- **体克用→体生用→用克体→用生体** (domains 6, 8): groups the 克 pair, then the 生 pair
- **Interleaved** (domain 16): 体克用 and 体生用 paired, then 用克体 and 用生体

**Adversarial-first is rare.** Only domain 2 (人事) leads with 用克体. The system predominantly presents 体's agency first.

## 4. H3: Hexagram-Name Channel

**1/18 domains** reference specific hexagram names in their templates.
**17/18 domains** are purely 五行-relation-based.

- **1. 天時占:** Entirely different system: counts trigram occurrences across 本/互/变. 离→晴, 坎→雨, 坤→阴晦, 乾→晴明, 震→雷, 巽→风, ...

**Finding:** The 17 体用-based domain templates are entirely 五行-driven — no hexagram name appears in any decision rule. Only 天時占 (domain 1), which bypasses 体用 entirely, references specific hexagrams (泰, 否, 既济, 未济, etc.) in its extended commentary.

This confirms the interpretive architecture has **two independent channels**: the 五行/体用 channel (mechanical, domain-independent) and the 爻辞/卦名 channel (requires Zhou Yi text lookup, used in post-hoc elaboration).

## 5. H4: Subsystem Analysis

**11/18 domains** have rules beyond the 5-relation template.
**7/18 domains** are pure 5-relation templates.

### Domains with subsystems

| # | Domain | Subsystem type |
|---|--------|---------------|
| 1 | 天時占 | Entirely different system: counts trigram occurrences across 本/互/变. 离→晴, 坎→雨, 坤→... |
| 2 | 人事占 | References the 8-trigram 生体/克体 detail tables (vol2 lines 25-41). |
| 5 | 婚姻占 | Family strength comparison (体旺/用旺); appearance descriptions per trigram (lines 5... |
| 6 | 生產占 | Male/female determination (阳卦阳爻→男, 阴卦阴爻→女); timing via 用卦 气数. |
| 7 | 飲食占 | 坎=酒, 兑=食 (坎 present→wine, 兑 present→food); 互卦 for guest identification. |
| 9 | 求名占 | Timing via 生体 卦气; location via 变卦 方道; in-office danger rules (克体→祸). |
| 10 | 求財占 | Timing: 生体 卦气 → gain date, 克体 卦气 → loss date. |
| 12 | 出行占 | Trigram-specific: 乾/震→动, 坤/艮→不动, 巽→舟行, 离→陆行, 坎→失脱, 兑→纷争. |
| 13 | 行人占 | 用卦 reads traveler's external condition; trigram-specific modifiers. |
| 15 | 失物占 | 变卦 → object location (8-trigram direction table, lines 89). |
| 16 | 疾病占 | Medicine type (离→热药, 坎→冷药, 艮→温补, 乾兑→凉药); ghost/spirit attribution (8-trigram 克体→... |

### Domains WITHOUT subsystems (pure template)

- 3. 家宅占 (Household)
- 4. 屋舍占 (Dwelling)
- 8. 求謀占 (Planning)
- 11. 交易占 (Trade)
- 14. 謁見占 (Audience/Meeting)
- 17. 官訟占 (Litigation)
- 18. 墳墓占 (Burial)

### Comparison with atlas-mh identification

Atlas-mh identified 7 domains with extra features: 出行占, 失物占, 婚姻占, 生產占, 疾病占, 行人占, 飲食占
This analysis finds 11 total (including 天時占 which bypasses 体用 entirely).
Additional subsystem domains not in atlas-mh's 7: **人事占, 求名占, 求財占**
These have timing rules (卦气-based date prediction) or career-specific danger rules.

## 6. Cross-Reference with Probe 8a Worked Examples

### Do worked examples use the 8-trigram 生体/克体 detail tables?

- Uses 8-trigram 生体/克体 tables (vol2 lines 25-41): **0/10**
- Uses 象 (image) layer: **9/10**
- Uses 爻辞 (line text): **5/10**

**Finding:** None of the 10 worked examples use the 8-trigram outcome tables from vol2. Instead, they use the **象 (image) mapping** as their primary interpretive mechanism. The 后天 examples (6-10) additionally use 爻辞.

### 象 trace verification

| # | Example | Trigram | Usage | In table? |
|---|---------|---------|-------|-----------|
| — | 观梅占 | 兑 | 少女 | ✓ |
| — | 观梅占 | 巽 | 股 | ✓ |
| — | 观梅占 | 艮 | 土(生金→救) | ✓ |
| — | 牡丹占 | 乾 | 马 | ✓ |
| — | 邻夜扣门 | 乾 | 金(短) | ✓ |
| — | 邻夜扣门 | 巽 | 木(长) | ✓ |
| — | 今日动静 | 兑 | 口 | ✓ |
| — | 今日动静 | 坤 | 腹/黍稷 | ✓ |
| — | 西林寺 | — | (no 象 used) | — |
| — | 老人有忧色 | 乾 | 老人 | ✓ |
| — | 少年有喜色 | 艮 | 少男 | ✓ |
| — | 牛哀鸣 | 坤 | 牛 | ✓ |
| — | 鸡悲鸣 | 巽 | 鸡 | ✓ |
| — | 鸡悲鸣 | 离 | 火/炉 | ✓ |
| — | 枯枝坠地 | 离 | 槁木 | ✓ |

**All 象 invocations trace to table entries: YES**

## 7. 象 (Image) Mapping Table

Source: vol1 lines 155-169 (八卦万物属类)

### 乾 (金)

- **Casting objects:** 天, 父, 老人, 官贵, 马, 金宝, 珠玉, 水果, 圆物, 冠, 镜, 刚物
- **Body parts:** 头, 骨
- **Colors:** 大赤色
- **Other:** 水寒

### 坤 (土)

- **Casting objects:** 地, 母, 老妇, 土, 牛, 金, 布帛, 文章, 舆辇, 方物, 瓦器, 黍稷, 书, 米, 谷
- **Body parts:** 腹
- **Colors:** 黄色, 黑色
- **Other:** 柄, 裳

### 震 (木)

- **Casting objects:** 雷, 长男, 龙, 百虫, 竹, 萑苇, 稼, 乐器, 草木, 树, 木核, 柴, 蛇
- **Body parts:** 足, 发, 蹄
- **Colors:** 青碧绿色
- **Other:** 马鸣, 馵足, 的颡

### 巽 (木)

- **Casting objects:** 风, 长女, 僧尼, 鸡, 百禽, 百草, 臼, 绳, 羽毛, 帆, 扇, 枝叶, 仙道工匠, 直物, 工巧之器
- **Body parts:** 股, 眼
- **Colors:** —
- **Other:** 香气, 臭

### 坎 (水)

- **Casting objects:** 水, 雨, 雪, 工, 豕, 中男, 沟渎, 弓轮, 月, 盗, 宫律, 栋, 丛棘, 狐, 蒺藜, 桎梏, 水族, 鱼, 盐, 酒, 醢, 有核之物
- **Body parts:** 耳, 血
- **Colors:** 黑色

### 离 (火)

- **Casting objects:** 火, 雉, 日, 电, 霓霞, 中女, 甲胄, 戈兵, 文书, 槁木, 炉, 兽, 鳄龟蟹蚌, 凡有壳之物, 花纹人, 干燥物
- **Body parts:** 目
- **Colors:** 红赤紫色

### 艮 (土)

- **Casting objects:** 山, 土, 少男, 童子, 狗, 径路, 门阙, 果, 蓏, 阍寺, 鼠, 虎, 狐, 黔喙之属, 木生之物, 藤生之物
- **Body parts:** 手指, 爪, 鼻
- **Colors:** 黄色

### 兑 (金)

- **Casting objects:** 泽, 少女, 巫, 妾, 羊, 毁折之物, 带口之器, 属金者, 废缺之物, 奴仆, 婢
- **Body parts:** 舌, 肺
- **Colors:** —

### Input/Output distinction

The 象 table serves **dual roles**:

1. **Input (casting):** Object/person → trigram assignment (e.g., 老人→乾, 牛→坤, 鸡→巽)
2. **Output (interpretation):** Trigram → meaning (e.g., 乾→马, 巽→股, 坤→腹/黍稷)

The worked examples show both directions operating simultaneously: input-layer assigns trigrams from observations, output-layer reads back meanings from the resulting hexagram's trigrams.

## 8. Summary: Mechanical vs. Judgment

### What is fully mechanical

1. **Hexagram generation:** Arithmetic (mod 8, mod 6) is deterministic
2. **互卦/変卦 computation:** Bit operations, fully mechanical
3. **体用 assignment:** Moving line position → 体/用, deterministic
4. **Five-phase relation:** Element lookup + cycle position, deterministic
5. **Base template application:** The 5-relation→valence mapping for 14/17 domains (excluding domains 6, 7 which invert 体克用)

### What requires judgment

1. **象 (image) selection:** When a hexagram contains multiple trigrams (本/互/変), which trigram's image to emphasize is chosen by the practitioner
2. **Timing period:** The text uses total-number, half-number, or doubled-number depending on sitting/standing/walking — but also says to use 变通 (flexibility)
3. **爻辞 integration:** Which line text to cite, and how literally to read it
4. **External correspondences (三要/十应):** Observed omens override or modify the internal hexagram analysis
5. **Domain 1 (天時):** Entirely judgment-based trigram-counting system

### Where exceptions cluster

- **Valence inversions:** Domains 6 (birth) and 7 (food) — both involve 用 as something *desired to receive* rather than an adversary to overcome
- **Weak positives (体克用=+~):** Domains 5,8,9,13,15 — the "delayed success" pattern consistently appears in domains where the outcome is an *event* that must *happen* (marriage, plan, office, return, finding) rather than a *state* to maintain
- **Subsystem concentration:** Domains 15 (lost object → location) and 16 (illness → medicine) have the most elaborate subsystems, both adding secondary trigram lookups

### Architectural insight

The 18-domain system is a **parameterized template** with three layers:

1. **Core template** (15/17 domains): 5-relation → valence mapping, identical across domains
2. **Domain-specific semantics** (2/17 inversion): Birth and food invert 体克用 because 用 represents something to nurture/receive, not compete with
3. **Subsystem overlays** (10/18 domains): Additional rules for timing, location, medicine, gender — these extend but never contradict the core template