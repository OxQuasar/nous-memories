# Probe 8a: 梅花易數 Vol1 Worked Examples Verification

Source: `memories/texts/meihuajingshu/vol1.txt` lines 175–237

## Summary: 10/10 examples fully consistent

| # | Name | Hex | Moving | 變卦 | 互卦 | 體用 | Overall |
|---|------|-----|--------|------|------|------|---------|
| 1 | 观梅占 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 2 | 牡丹占 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 3 | 邻夜扣门 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 4 | 今日动静 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 5 | 西林寺 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 6 | 老人有忧色 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 7 | 少年有喜色 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 8 | 牛哀鸣 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 9 | 鸡悲鸣 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |
| 10 | 枯枝坠地 | ✓ | ✓ | ✓ | ✓ | ✓ | **PASS** |

---

## Example 1: 观梅占 (line 177)

**Hexagram ✓:** computed=Ge (upper=兑/2, lower=离/3), claimed=革 (Ge)
**Moving line ✓:** computed=1, claimed=1 (43 mod 6 = 1 → 1)
**變卦 ✓:** computed=Xian (val=28), claimed=咸 (Xian)
**互卦 ✓:** computed=upper=乾, lower=巽, claimed=upper=乾, lower=巽
**體用 ✓:** 体=兑(upper), 用=离(lower), claimed=体=兑(upper)

**五行 chain:**
- 體: 兑=金
- 用: 离=火
- 本卦 relation: **克体**
- 互卦 elements: 乾=金, 巽=木
- 互卦 relations: 互体侧: 比和, 互用侧: 体克用
- 變卦 用-side: 艮=土 → **生体**
- Text claim: 兑金为体，离火克之 → 用克体

---

## Example 2: 牡丹占 (line 183)

**Hexagram ✓:** computed=Gou (upper=乾/1, lower=巽/5), claimed=姤 (Gou)
**Moving line ✓:** computed=5, claimed=5 (29 mod 6 = 5 → 5)
**變卦 ✓:** computed=Ding (val=46), claimed=鼎 (Ding)
**互卦 ✓:** computed=upper=乾, lower=乾, claimed=upper=乾, lower=乾
**體用 ✓:** 体=巽(lower), 用=乾(upper), claimed=体=巽(lower)

**五行 chain:**
- 體: 巽=木
- 用: 乾=金
- 本卦 relation: **克体**
- 互卦 elements: 乾=金, 乾=金
- 互卦 relations: 互体侧: 克体, 互用侧: 克体
- 變卦 用-side: 离=火 → **体生用**
- Text claim: 巽木为体，乾金克之 → 用克体

---

## Example 3: 邻夜扣门 (line 189)

**Hexagram ✓:** computed=Gou (upper=乾/1, lower=巽/5), claimed=姤 (Gou)
**Moving line ✓:** computed=4, claimed=4 (16 mod 6 = 4 → 4)
**變卦 ✓:** computed=Xun (val=54), claimed=巽 (Xun)
**互卦 ✓:** computed=upper=乾, lower=乾, claimed=upper=乾, lower=乾
**體用 ✓:** 体=巽(lower), 用=乾(upper), claimed=体=巽(lower)

**五行 chain:**
- 體: 巽=木
- 用: 乾=金
- 本卦 relation: **克体**
- 互卦 elements: 乾=金, 乾=金
- 互卦 relations: 互体侧: 克体, 互用侧: 克体
- 變卦 用-side: 巽=木 → **比和**
- Text claim: 金木之物 (乾金=短, 巽木=长 → 斧)

---

## Example 4: 今日动静 (line 195)

**Hexagram ✓:** computed=Sheng (upper=坤/8, lower=巽/5), claimed=升 (Sheng)
**Moving line ✓:** computed=1, claimed=1 (13 mod 6 = 1 → 1)
**變卦 ✓:** computed=Tai (val=7), claimed=泰 (Tai)
**互卦 ✓:** computed=upper=震, lower=兑, claimed=upper=震, lower=兑
**體用 ✓:** 体=坤(upper), 用=巽(lower), claimed=体=坤(upper)

**五行 chain:**
- 體: 坤=土
- 用: 巽=木
- 本卦 relation: **克体**
- 互卦 elements: 震=木, 兑=金
- 互卦 relations: 互体侧: 克体, 互用侧: 体生用
- 變卦 用-side: 乾=金 → **体生用**
- Text claim: 口腹之事 (兑=口, 坤=腹); symbolic

---

## Example 5: 西林寺 (line 201)

**Hexagram ✓:** computed=Bo (upper=艮/7, lower=坤/8), claimed=剥 (Bo)
**Moving line ✓:** computed=3, claimed=3 (15 mod 6 = 3 → 3)
**變卦 ✓:** computed=Gen (val=36), claimed=艮 (Gen)
**互卦 ✓:** computed=upper=坤, lower=坤, claimed=upper=坤, lower=坤
**體用 ✓:** 体=艮(upper), 用=坤(lower), claimed=体=艮(upper)

**五行 chain:**
- 體: 艮=土
- 用: 坤=土
- 本卦 relation: **比和**
- 互卦 elements: 坤=土, 坤=土
- 互卦 relations: 互体侧: 比和, 互用侧: 比和
- 變卦 用-side: 艮=土 → **比和**
- Text claim: 群阴剥阳 (yin/yang symbolic); 体用 both 土 → 比和

---

## Example 6: 老人有忧色 (line 211)

**Hexagram ✓:** computed=Gou (upper=乾/1, lower=巽/5), claimed=姤 (Gou)
**Moving line ✓:** computed=4, claimed=4 (10 mod 6 = 4 → 4)
**變卦 ✓:** computed=Xun (val=54), claimed=巽 (Xun)
**互卦 ✓:** computed=upper=乾, lower=乾, claimed=upper=乾, lower=乾
**體用 ✓:** 体=巽(lower), 用=乾(upper), claimed=体=巽(lower)

**五行 chain:**
- 體: 巽=木
- 用: 乾=金
- 本卦 relation: **克体**
- 互卦 elements: 乾=金, 乾=金
- 互卦 relations: 互体侧: 克体, 互用侧: 克体
- 變卦 用-side: 巽=木 → **比和**
- Text claim: 巽木为体，乾金克之，互又重乾克体 → 用克体

---

## Example 7: 少年有喜色 (line 217)

**Hexagram ✓:** computed=Bi (upper=艮/7, lower=离/3), claimed=贲 (Bi)
**Moving line ✓:** computed=5, claimed=5 (17 mod 6 = 5 → 5)
**變卦 ✓:** computed=Jia Ren (val=53), claimed=家人 (Jia Ren)
**互卦 ✓:** computed=upper=震, lower=坎, claimed=upper=震, lower=坎
**體用 ✓:** 体=离(lower), 用=艮(upper), claimed=体=离(lower)

**五行 chain:**
- 體: 离=火
- 用: 艮=土
- 本卦 relation: **体生用**
- 互卦 elements: 坎=水, 震=木
- 互卦 relations: 互体侧: 克体, 互用侧: 生体
- 變卦 用-side: 巽=木 → **生体**
- Text claim: 离为体，互变俱生之 → 生体

---

## Example 8: 牛哀鸣 (line 221)

**Hexagram ✓:** computed=Shi (upper=坤/8, lower=坎/6), claimed=师 (Shi)
**Moving line ✓:** computed=3, claimed=3 (21 mod 6 = 3 → 3)
**變卦 ✓:** computed=Sheng (val=6), claimed=升 (Sheng)
**互卦 ✓:** computed=upper=坤, lower=震, claimed=upper=坤, lower=震
**體用 ✓:** 体=坤(upper), 用=坎(lower), claimed=体=坤(upper)

**五行 chain:**
- 體: 坤=土
- 用: 坎=水
- 本卦 relation: **体克用**
- 互卦 elements: 坤=土, 震=木
- 互卦 relations: 互体侧: 比和, 互用侧: 克体
- 變卦 用-side: 巽=木 → **克体**
- Text claim: 坤为体，互变俱克之 → 克体

---

## Example 9: 鸡悲鸣 (line 227)

**Hexagram ✓:** computed=Xiao Chu (upper=巽/5, lower=乾/1), claimed=小畜 (Xiao Chu)
**Moving line ✓:** computed=4, claimed=4 (10 mod 6 = 4 → 4)
**變卦 ✓:** computed=Qian (val=63), claimed=乾 (Qian)
**互卦 ✓:** computed=upper=离, lower=兑, claimed=upper=离, lower=兑
**體用 ✓:** 体=乾(lower), 用=巽(upper), claimed=体=乾(lower)

**五行 chain:**
- 體: 乾=金
- 用: 巽=木
- 本卦 relation: **体克用**
- 互卦 elements: 兑=金, 离=火
- 互卦 relations: 互体侧: 比和, 互用侧: 克体
- 變卦 用-side: 乾=金 → **比和**
- Text claim: 乾金为体，离火克之 → 互克体

---

## Example 10: 枯枝坠地 (line 233)

**Hexagram ✓:** computed=Kui (upper=离/3, lower=兑/2), claimed=睽 (Kui)
**Moving line ✓:** computed=4, claimed=4 (10 mod 6 = 4 → 4)
**變卦 ✓:** computed=Sun (val=35), claimed=损 (Sun)
**互卦 ✓:** computed=upper=坎, lower=离, claimed=upper=坎, lower=离
**體用 ✓:** 体=兑(lower), 用=离(upper), claimed=体=兑(lower)

**五行 chain:**
- 體: 兑=金
- 用: 离=火
- 本卦 relation: **克体**
- 互卦 elements: 离=火, 坎=水
- 互卦 relations: 互体侧: 克体, 互用侧: 体生用
- 變卦 用-side: 艮=土 → **生体**
- Text claim: 兑金为体，离火克之 → 用克体

---

## Structural Observations

### Arithmetic patterns
- 先天 examples (1-5): upper_sum mod 8 → upper trigram, lower_sum mod 8 → lower trigram, total mod 6 → moving line
- 后天 examples (6-10): object/person → upper trigram number, direction → lower trigram number, sum of both + hour → moving line total
- Zero-maps-to-max convention: mod 8 remainder 0 → 8 (坤), mod 6 remainder 0 → 6

### 體用 consistency
- All 10 examples correctly follow: moving in lower (1-3) → 体=upper, 用=lower; moving in upper (4-6) → 体=lower, 用=upper
- The text's diagnostic language is always phrased from 体's perspective: '...为体，...克之'

### 五行 analysis depth
- Simple examples (1,2,6): explicit 体/用/克 + 互 reinforcement
- Symbolic examples (3,4,5): less formal五行, more象 (image) reasoning
- Composite examples (7-10): full chain — 本卦 relation, 互 relation, 變卦 relation all evaluated

### Recurring hexagram
- 天风姤 (乾 over 巽) appears in examples 2, 3, and 6 — same hexagram from different input methods
- Each time the diagnosis differs because the moving line differs (5, 4, 4) and the context differs