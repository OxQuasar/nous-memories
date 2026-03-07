# 京氏易傳 — Exploration Plan

## Context

京氏易傳 is the Han dynasty source (Jing Fang, ~1st c. BC) from which 火珠林 extracted its core mechanics. 火珠林 kept 納甲/八宮/世應/飛伏/六親/旺相休囚死 but dropped several layers:

- **五星** — planet-per-hexagram assignments
- **二十八宿** — lunar mansion per hexagram (descends to 世 position)
- **氣候分數** — 28 or 36 per hexagram (yin/yang temporal count)
- **建始** — hexagram-specific 節氣 (solar term) active windows
- **積算** — calculation start/end cycles per hexagram

These are the layers 火珠林 compressed into simple seasonal strength (旺相休囚死). The temporal gating we found shallow in huozhulin/probe 6 may be a lossy compression of a richer structure.

**Goal:** Extract these layers from the source text, test whether they carry independent algebraic information beyond what we already know (basin, kernel, palace, 五行), and determine whether the finer temporal structure resolves any open questions.

## Dependencies

- huozhulin/ palace generation, 納甲, 六親 implementations
- wuxing/ 五行 decomposition (parity, b₀, cosmological bit)
- opposition-theory/phase4/cycle_algebra.py (trigram/hexagram primitives)

---

## Probe 1: 氣候分數 — the 28/36 binary

**Extract:** Each hexagram entry states 氣候分數 as either 二十八 or 三十六.

**Questions:**
- What determines 28 vs 36? Is it a function of palace, rank, 世 position, basin, yin/yang line count, or something else?
- The text associates 28 with yin, 36 with yang (likely from 4×7=28 old yin strategy count, 4×9=36 old yang). Does the assignment track any known partition?
- Is it redundant to parity (b₀⊕b₁), yang count, or basin? Or independent information?
- 28+36=64... do exactly 28 hexagrams get 28 and 36 get 36? Or different split?

**Method:** Parse all 64 entries, build dict hex→{28,36}, cross-tabulate against palace/rank/basin/kernel/parity/yang_count.

**Output:** `01_qihou.py`, `01_findings.md`

---

## Probe 2: 五星 — planetary assignments

**Extract:** Each hexagram entry names one of 5 planets: 鎮星(土/Saturn), 太白(金/Venus), 太隂(水/Moon-Mercury), 熒惑(火/Mars), 嵗星(木/Jupiter).

**Questions:**
- What determines the planet? Does it follow palace element, 世 line element, 納甲 element, or an independent cycle?
- The planets map to 五行: 鎮星=Earth, 太白=Metal, 太隂=Water, 熒惑=Fire, 嵗星=Wood. Is the planet assignment simply another expression of 五行, or does it add structure?
- Cross-tabulate with palace element: if planet = palace element, it's redundant. If not, what's the relationship?
- Does the planet assignment factor through shell (trigram pair) or core (inner bits)?

**Method:** Parse all 64 entries, build dict hex→planet, compare planet element to palace element / 世 line element / trigram elements. MI analysis.

**Output:** `02_wuxing_planets.py`, `02_findings.md`

---

## Probe 3: 二十八宿 — lunar mansion assignments

**Extract:** Each entry names a lunar mansion (宿) that descends to a specific position.

**Questions:**
- 28 mansions across 64 hexagrams — what's the distribution? Are some mansions shared? Which hexagrams share a mansion?
- The 二十八宿 are grouped into 4 quadrants of 7 (東青龍/北玄武/西白虎/南朱雀). Does quadrant correlate with palace, basin, or Later Heaven direction?
- Mansions have traditional element assignments. Does mansion element agree with planet element, palace element, or 世 line element?
- Is the mansion assignment determined by the 世 position's 地支? The text says the mansion "descends to" (從位降) a specific 干支 — likely the 世 line's 納甲 assignment.

**Method:** Parse all 64 entries, extract mansion name and target position. Build mansion→hexagram mapping. Cross-tabulate mansion quadrant with palace/basin. Test whether mansion is uniquely determined by 世 line's 納甲 branch.

**Output:** `03_mansions.py`, `03_findings.md`

---

## Probe 4: 建始 — hexagram-specific 節氣 windows

**Extract:** Each entry gives a start and end 節氣 (e.g. 立春至大暑, 秋分至春分).

**Questions:**
- Do the 節氣 windows tile the year? Overlap? Leave gaps?
- Is the window determined by palace + rank? Same-palace hexagrams should have related windows if the palace walk is temporal.
- The text gives 24 節氣. With 64 hexagrams, some must share. What's the sharing pattern?
- 卷下 gives a separate 節氣-to-line mapping (24 terms → specific hexagram lines). How does this relate to the per-hexagram windows?
- Does the 節氣 window interact with 旺相休囚死? A hexagram whose active window falls in its palace element's 旺 season would be "self-resonant" — how many achieve this?

**Method:** Parse all 64 entries for 建始 ranges. Map 節氣 to months. Build timeline. Cross-reference with palace element's 旺 season. Compare with the 卷下 line-level mapping.

**Output:** `04_jieqi.py`, `04_findings.md`

---

## Probe 5: 積算 — calculation cycles

**Extract:** Each entry gives 積算起X至Y (calculation from X to Y, 周而復始).

**Questions:**
- What are X and Y? They appear to be 干支 pairs. Is the cycle length constant or variable?
- Does the cycle relate to 納甲 assignments? (Likely — the start/end points are 干支.)
- Is 積算 determined by palace + rank, or does it carry independent information?
- The text often notes "金土入卦" or "火木入卦" alongside 積算 — element pairs entering the calculation. Do these element pairs correlate with shell elements?

**Method:** Parse all 64 entries for 積算 start/end 干支. Compute cycle lengths. Cross-tabulate with palace/rank/shell elements.

**Output:** `05_jisuan.py`, `05_findings.md`

---

## Probe 6: Text comparison — 京氏易傳 vs 火珠林 overlap

**Context:** Both texts share core mechanics (納甲, 八宮, 世應, 飛伏, 六親). But they were written centuries apart and may diverge on specifics. The overlap is the validation surface — agreements confirm shared tradition, disagreements reveal drift or reinterpretation.

**Questions:**
- **納甲 assignments:** Do 京氏易傳's stem/branch assignments per hexagram match 火珠林's? Any hexagrams where they diverge?
- **八宮 classification:** Same 8×8 grouping? Same palace order? Same 游魂/歸魂 treatment?
- **世應 positions:** Same line assignments per rank? 京氏 卷下 defines the rule explicitly — does it match what we implemented from 火珠林?
- **飛伏 pairings:** Same trigram pairings (乾↔坤, 震↔巽, 坎↔離, 艮↔兌)? Same position logic?
- **六親 terminology:** 京氏 uses different names (繫爻/制爻/義爻/寶爻/専爻 vs 官鬼/妻財/父母/子孫/兄弟). Do they map 1:1? Any relational differences in definition?
- **Interpretive emphasis:** 京氏 embeds 易 quotes and cosmological commentary per hexagram. Does 火珠林 preserve any of this, or strip it entirely for the procedural method?

**Method:** 
- For each of the 64 hexagrams, extract 京氏's 世應 position and 飛伏 pair. Compare against huozhulin implementation output.
- Tabulate 六親 name mapping. Verify bijectivity.
- Identify any hexagrams where the two texts assign different structural attributes.
- Catalog interpretive content in 京氏 that 火珠林 drops vs preserves.

**Output:** `06_text_comparison.py`, `06_findings.md`

---

## Probe 7: Synthesis — the dropped layers as temporal coordinates

**Questions:**
- How much independent information do the 5 dropped layers carry collectively? MI analysis: how many bits beyond palace/rank/shell/core?
- Do the dropped layers resolve the 2/5 seasonal ceiling? (The hexagram-specific 節氣 window could break the uniform seasonal gating.)
- Is there a natural "temporal presheaf" where the base space is (節氣 window × planet × mansion) and the stalks are the 六親 functional profiles?
- Do the dropped layers bridge algebra to meaning? (Planetary/mansion associations carry traditional semantic content that might connect to hexagram meanings.)

**Method:** Combine outputs from probes 1-6. Joint MI matrix with all known partitions. Test whether the full 京氏 temporal system achieves higher functional coverage than 火珠林's simplified version.

**Output:** `07_synthesis.py`, `07_findings.md`

---

## Probe 8: Captain Discretionary

Based on above findings, captain to explore a question or resolve unanswered questions at his discretion. 

**Output:** `08_discretion.py`, `08_discretion.md`

---

## Extraction strategy

The text is dense classical Chinese with no consistent delimiters. Extraction approach:
1. Use regex patterns on known markers: 氣候/分數/二十八/三十六, 五星從位起, 宿從位降, 建始/建起, 積算起
2. Associate each match with its hexagram via the ䷀-style unicode markers or sequential position
3. Validate against known data (世 positions, 納甲 assignments from huozhulin probes)
4. Manual correction where regex fails

Source files: `memories/texts/jingshi_yizhuan/jingshi_yizhuan_{1,2,3}.md`
