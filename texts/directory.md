# Source Texts — Directory

Primary source texts in classical Chinese

---

## `iching/` — The Yi Jing (易經) and Ten Wings

The core text, structured as JSON for computational analysis.

| File | Title | Contents |
|------|-------|----------|
| `guaci.json` | 卦辭 | Hexagram judgments. 64 entries — one statement per hexagram. The primary oracular text. "元亨利貞" (乾), "元亨，利牝馬之貞" (坤), etc. |
| `yaoci.json` | 爻辭 | Line statements. 384 entries (6 per hexagram). The situational descriptions — imagery, actions, outcomes. The layer the semantic-map and residual analysis operate on. |
| `tuan.json` | 彖傳 | Commentary on the Judgment (Tuan zhuan). 64 entries. Attributed to Confucius. Explains why each hexagram's judgment says what it says. R72 showed it functions as a systematic anomaly detector on binary (Z₂) structure. |
| `xiangzhuan.json` | 象傳 | Image commentary (Xiang zhuan). Contains both 大象 (daxiang, one per hexagram — imagistic, using trigram symbolism) and 小象 (xiaoxiang, one per line — positional commentary). The semantic-map found 大象 is imagistic (non-algebraic) and 小象 is positional. |
| `xugua.json` | 序卦傳 | Sequence of the Hexagrams (Xugua zhuan). 64 entries explaining why each hexagram follows the previous in the King Wen ordering. Narrative justifications, not algebraic. The authored layer. |

---

## `jingshi_yizhuan/` — 京氏易傳 (Jingshi Yizhuan)

Han dynasty text by 京房 (Jing Fang, 77–37 BC). The foundational source for 納甲 (branch assignment to hexagram lines) and the palace system. Three volumes.

| File | Contents |
|------|----------|
| `jingshi_yizhuan_1.md` | Volume 1. 乾 through 巽 palaces. Dense per-hexagram entries: palace assignment, 納甲 branches, 飛伏 pairs, 積算, 五星, 二十八宿, 建始, and interpretive commentary. |
| `jingshi_yizhuan_2.md` | Volume 2. Remaining palaces. Same format. |
| `jingshi_yizhuan_3.md` | Volume 3. Theoretical summary and supplementary material. |

The jingshiyizhuan workflow (memories/iching/jingshiyizhuan) found that 火珠林 dropped 5 deterministic layers from this text (氣候分數, 五星, 二十八宿, 建始, 積算) — all were lossless functions of (palace, rank), so the compression was informationally complete. Also discovered the universal 納甲 offset rule (+3 for upper trigrams, exception-free).

---

## `huozhulin/` — 火珠林 (Huo Zhu Lin)

Song dynasty text attributed to 麻衣道者 (Mayi Daozhe). The operational manual for the 火珠林 divination method — the dominant Chinese divination system from Song dynasty onward.

| File | Contents |
|------|----------|
| `huozhulin.md` | Complete text. Covers: 六爻 mechanics, 六親 relations, 用神 selection, 日辰 interaction, 動爻 transformation, domain-specific protocols. The source for the atlas-hzl formalization. |

---

## `meihuajingshu/` — 梅花易數 (Meihua Yishu)

Attributed to 邵雍 (Shao Yong, 1011–1077). The manual for 梅花 (Plum Blossom) numerology — the lighter, faster divination method using 先天 number assignments and 体用 (body/function) analysis.

| File | Contents |
|------|----------|
| `vol1.txt` | 象数易理篇之一. Foundations: trigram numbers, 五行 生克, method of obtaining hexagrams from numbers, time, and observation. |
| `vol2.txt` | 象数易理篇之二. 体用 theory, 互卦, worked examples of number-based divination. |
| `vol3.txt` | 象数易理篇之三. Observational method (觀梅), advanced 体用 interpretation, more worked examples. |
| `vol4.txt` | 象数易理篇之四. Trigram/hexagram image dictionaries — comprehensive lists of what each trigram represents (animals, body parts, objects, directions, etc.). |
| `vol5.txt` | 象数易理篇之五. Extended worked examples and case studies. The largest volume. |
| `appendix.txt` | Supplementary material. |

---

## `huangjijingshi/` — 皇極經世書 (Huangji Jingshi Shu)

By 邵雍 (Shao Yong, 1011–1077). Same author as 梅花易數. A cosmological work applying the hexagram structure to history and natural philosophy. 14 volumes, the largest text collection in this repository (~1.4 MB total).

| File | Contents |
|------|----------|
| `1-hj.txt` | 觀物篇一. "Observing Things" — cosmological framework, 元會運世 (epoch system mapping hexagram structure to historical time). |
| `2-hj.txt` | 觀物篇二. Continuation — the number-image-principle framework. |
| `3-hj.txt` | 觀物篇三. Application of framework to natural phenomena. |
| `4-hj.txt` | 觀物篇四. Historical chronology through the hexagram lens. |
| `5-hj.txt` | 觀物篇五. Continuation of historical application. |
| `6-hj.txt` | 觀物篇六. The 聲音 (sound/phonology) system — mapping Chinese phonetics to hexagram structure. |
| `7-hj.txt` | 觀物篇七. Diagrams and tables — numerical correspondences. |
| `8-hj.txt` | 觀物篇八. More diagrams and tables. |
| `9-hj.txt` | 觀物篇九. More diagrams and tables. |
| `10-hj.txt` | 觀物篇十. Extended tables. |
| `11-hj.txt` | 觀物外篇上. "Outer chapters" — philosophical discussion. |
| `12-hj.txt` | 觀物外篇下. Continuation. |
| `13-hj.txt` | Supplementary material. |
| `14-hj.txt` | Supplementary material. |

Not yet directly analyzed by any workflow. Potentially relevant to Q2 (axioms from below) — Shao Yong's cosmological framework is the most systematic pre-modern attempt to derive the hexagram structure from first principles.

---

## Usage in the Research Program

| Text | Primary workflow | Key findings |
|------|-----------------|--------------|
| 卦辭 guaci | semantic-map | 凶×basin bridge (OR=4.25) |
| 爻辭 yaoci | semantic-map, reversal Q1 | 89% residual, ~20-dim thematic manifold, complement antipodality |
| 彖傳 tuan | semantic-map, i-summary | R72: systematic anomaly detector on Z₂ structure |
| 象傳 xiangzhuan | semantic-map | 大象 imagistic, 小象 positional — neither algebraic |
| 序卦傳 xugua | kw-final | Narrative justifications for KW ordering; R61: no algebraic metric discriminates |
| 京氏易傳 | jingshiyizhuan | Universal 納甲 offset, lossless 5-layer compression |
| 火珠林 | atlas-hzl | {4,2,2,2,2} cascade, 用神 protocol, 31 domains |
| 梅花易數 | atlas-mh | 384 states, 8 arc types, 体互 adversarial structure |
| 皇極經世書 | (not yet analyzed) | — |
