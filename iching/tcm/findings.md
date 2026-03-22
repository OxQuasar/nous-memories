# TCM Investigation — Findings

> **Convention:** This document uses Convention A (b₀=bottom, b₂=top) where bit positions are referenced.

## Summary

**D1 hypothesis (TCM 八纲 as Q₃ domain for Z₅ grammar): CLOSED — structurally incompatible.**

The investigation ran three iterations: (1) 梅花 medical domain extraction, (2) 黃帝內經 + 互 resolution, (3) 傷寒論 + synthesis. Four independent structural reasons rule out TCM's 八纲辨证 as a domain where the Q₃ × Z₅ grammar can be tested.

**Interpretive conclusion:** The grammar is a uniqueness classification of the mathematical object (F₂³, Z₅, complement), not a transferable natural law. D4 (markets) failed because axes are too different; D1 (TCM) failed because axes are too correlated. The three-condition domain criterion is so restrictive that the question inverts from "which domain?" to "is the grammar domain-specific to trigram space?"

---

## D1-R1: 八纲 axes are correlated, not independent

**[measured]** All three diagnostic axes (寒/热, 虚/实, 表/里) map onto a single 陰/陽 meta-axis:
- 表=陽, 里=陰
- 热=陽, 寒=陰
- 实=陽, 虚=陰

The 內經 is explicit: "善診者...先別陰陽" — first distinguish yin from yang, then subdivide (素問 ch.5). Strong default associations exist: 热-实-表 cluster, 寒-虚-里 cluster. Mixed states are documented but clinically uncommon. The axes are three noisy readouts of one underlying bit, not three independent bits.

Source: 素問 ch.5 (陰陽應象大論), ch.28 (通評虛實論), ch.29 (太陰陽明論).

## D1-R2: 表/里 is sequential, not binary

**[measured]** The 熱論 (素問 ch.31) models disease as progressing through six channels from exterior to interior over six days: 太陽→陽明→少陽→太陰→少陰→厥陰. This is a depth gradient, not a binary switch. The treatment boundary (sweat therapy vs purge therapy) falls at day 3, but the underlying axis is continuous progression.

The lethal exception (兩感 — simultaneous 表+里 attack) is documented precisely because it violates the normal sequential model. 表 and 里 engaged simultaneously = qualitatively different (fatal) condition, not just another combination.

Source: 素問 ch.31 (熱論).

## D1-R3: No classical 八纲→trigram mapping exists

**[measured]** The only 內經 chapter mapping trigrams to medicine is 靈樞 ch.77 (九宮八風), which maps trigrams to organs via compass directions and seasonal winds. This is a cosmological/meteorological framework — which wind causes which disease — not a clinical diagnostic system. No classical text maps 八纲 poles (寒/热, 虚/实, 表/里) to trigram bit positions.

Any 八纲→trigram assignment would be an invention, not a discovery. This introduces researcher degrees of freedom that invalidate the test.

Source: full grep of 黃帝內經 for 八卦/卦 references; 靈樞 ch.77 analysis.

## D1-R4: Native clinical structure is 2×3, not 2³

**[measured]** The 傷寒論's 六經 (Six Channel) model — the most clinically influential disease classification — has architecture Z₂ × Z₃ = 6 states: three 陽 channels (太陽, 陽明, 少陽) subdivide 表; three 陰 channels (太陰, 少陰, 厥陰) subdivide 里. This is a two-level tree, not three independent binary axes. Dimensional mismatch with Q₃ = 2³ = 8.

The 八纲 framework, which recasts this as 2³, is a later systematization (Ming-Qing era) that doesn't match the native clinical structure.

Source: 傷寒論 channel opening clauses and transition rules.

---

## Additional findings

### F1: 虚/实 is not a simple binary

**[measured]** The 內經 documents 重虚 (double deficiency), 重实 (double excess), and mixed states where different body regions have opposite 虚/实 simultaneously (經虛絡滿). It is a force-balance ratio (pathogen strength / vital qi strength), not a switch.

### F2: 五行 temporal disease timing (刺熱論)

**[measured]** 素問 ch.32 asserts each organ's disease worsens on 克-element days:
- 肝(Wood) worsens on 庚辛(Metal days), recovers on 甲乙(Wood days)
- 心(Fire) worsens on 壬癸(Water days), recovers on 丙丁(Fire days)
- 脾(Earth) worsens on 甲乙(Wood days), recovers on 戊己(Earth days)
- 肺(Metal) worsens on 丙丁(Fire days), recovers on 庚辛(Metal days)
- 腎(Water) worsens on 戊己(Earth days), recovers on 壬癸(Water days)

This is Z₅ 克 cycle applied to temporal disease dynamics — the most concrete, testable 五行 claim in the text. It operates on organs directly, without Q₃ substrate. Test design: 2×5 contingency table (organ × day-element). **No data currently exists** to run this test.

### F3: 傷寒論 uses 陰陽, not 五行

**[measured]** The 傷寒論's treatment logic is entirely 陰陽-based. Disease resolution uses the 12-hour 地支 cycle (yang channels resolve in yang hours, yin in yin hours), not the 10-day 天干 cycle of the 刺熱論. No 五行 temporal disease timing appears in the most influential clinical text. The 天干/五行 temporal framework (刺熱論) and the 地支/陰陽 temporal framework (傷寒論) are different intellectual layers in the same tradition.

### F4: TCM uses 五行 for organ identity, pathological transmission, and treatment strategy

**[measured]** 五行 in TCM operates at the organ level, not the diagnostic-axis level:
1. **Organ identity:** 肝=Wood, 心=Fire, 脾=Earth, 肺=Metal, 腎=Water (definitional)
2. **Pathological transmission:** 生 direction = mother→child spread; 克 direction = overcontrol attack
3. **Treatment strategy:** 虚則補其母, 实則瀉其子 (tonify mother for deficiency, drain child for excess)
4. **Taste/climate/emotion:** Each element's pathology is countered by its 克 element's taste/emotion (怒傷肝，悲勝怒)

The 五行 medical framework is a property of the organ network, not of the diagnostic state space.

### F5: Trigrams have almost no role in TCM proper

**[measured]** The trigram as a three-bit object plays no clinical function in TCM. The 九宮八風 mapping (靈樞 ch.77) connects trigrams to organs via compass directions, but this is cosmological, not diagnostic. No practitioner assigns a trigram to a patient's clinical state. The 梅花易數 medical domain does read trigrams for illness, but that is divination practice, not medicine.

What TCM and the I Ching share: 陰陽 and 五行 as relational frameworks. What they don't share: the Q₃ binary structure.

### F6: 九宮八風 trigram→organ mapping uses dual principles

**[measured]** Cardinal-direction trigrams map to 五臟 (yin organs) following standard 五行 (离→心, 坎→腎, 震→肝, 兑→肺, 坤→脾). Intercardinal trigrams map to 六腑 (yang organs) following 表裏 meridian pairing, not 五行 (乾→小腸, 艮→大腸, 巽→胃). The assignment is structurally inconsistent — two organizational principles coexist.

---

## 梅花 Medical Domain Extraction

### F7: 疾病 is the richest of 18 梅花 domains

**[measured]** Three sub-systems beyond the standard 體/用 template:
1. **Pharmacology** — 生体 trigram → drug thermal quality (离→热药, 坎→冷药, 艮/坤→温补, 乾/兑→凉药). Operates at element level, not individual trigram level.
2. **Spirit diagnosis** — 克体 trigram → supernatural cause. Driven by trigram 象 (imagery), not 五行.
3. **Body localization** — 受克 trigram → body region via 說卦 mapping (乾=head, 坤=abdomen, etc.). Different system from 五行→organ.

Plus two structural escalations: 旺/衰 as life/death binary (unique to illness), dual timing (recovery date vs crisis date).

### F8: Two parallel body-mapping systems

**[measured]** 梅花 illness holds two incompatible body mappings simultaneously:
- **說卦 spatial:** trigram → body region (乾=head, 震=foot, 坎=ear, 离=eye...)
- **五行 functional:** element → organ (Metal=lung, Wood=liver, Water=kidney...)

These mostly disagree (乾=head ≠ Metal=lung). Illness divination uses 說卦 for localization ("where does it hurt?") and 五行 for mechanism ("which organ system?"). The tradition holds both in parallel without reducing one to the other.

### F9: 互(本) confirmed as standard practice (5:1)

**[measured]** 10 worked examples checked across 梅花 vols 2-3. Of 6 decisive cases (where 互(本) ≠ 互(變)): 5 match 互(本), 1 matches 互(變). The sole exception is the illness worked example (vol2 line 94, 否 line 2) — likely a textual error or isolated pedagogical variant.

---

## Domain criterion (updated)

Three necessary conditions for a Q₃ domain to be testable against the Z₅ grammar:

1. **Three independent binary axes** — mutual information between any two axes ≈ 0
2. **Commensurable axes** — all three measured the same way, same kind of quantity, similar timescales
3. **Matching axis-type hierarchy** — domain's axis asymmetry aligns with algebra's (pure-克 axis matches domain's most adversarial axis)

**D4 (markets):** Failed #2 (trend ≠ vol ≠ liquidity) and #3 (no alignment).
**D1 (TCM):** Failed #1 (axes share 陰/陽 factor) and additionally #3 (native structure is 2×3, not 2³).

The failures are complementary — markets had independent but incommensurable axes; TCM had commensurable but correlated axes. The criterion demands all three conditions simultaneously.

---

## What remains

1. **刺熱論 Z₅ test** — well-defined, testable, no Q₃ needed. Requires longitudinal organ-disease symptom data matched to 天干 calendar days. Currently no such dataset exists.
2. **Grammar decomposability** — algebraically confirmed (Q₃ substrate separable from Z₅ content). Empirically unknown (no evidence Z₅ has autonomous predictive content outside the I Ching system).
3. **Alternative Q₃ domains** — three assets (BTC/ETH/SOL each up/down), three timescales (1h/4h/daily trend), or other systems with three instances of the same binary measurement. Not yet tested.

---

## Sources

| Source | Location | Used for |
|---|---|---|
| 黃帝內經 素問 | `texts/huangdineijing/suwen_*.txt` | D1-R1, R2, R3; F1-F6 |
| 黃帝內經 靈樞 | `texts/huangdineijing/lingshu_*.txt` | D1-R3; F5, F6 |
| 傷寒論 | `texts/shanghanlun/shang-han-lun.md` | D1-R4; F3 |
| 梅花易數 | `texts/meihuajingshu/vol2-4.txt` | F7-F9 |
| 九宮八風 detail | `tcm/neijing_extract.md` §8 | F6 |
| Full extraction notes | `tcm/neijing_extract.md` | Supporting analysis |
| 梅花 medical detail | `tcm/meihua_medical.md` | F7-F9 |
| Exploration log | `tcm/exploration-log.md` | Iteration details |
