#!/usr/bin/env python3
"""Q3: Extract and analyze worked divination examples from 梅花易數 and 火珠林.

Phase 1: Extract worked cases with algorithmic inputs + judgment steps + outcomes.
Phase 2: Classify judgment moves and cross-tabulate.

The 梅花易數 worked examples are primarily in vol1 (先天/後天 examples)
and vol3 (变卦式八则, theoretical cases). The 火珠林 has a different
methodology (六爻 with 六親) but the judgment structure is similar.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
TEXTS = ROOT.parent / "texts"
Q3 = Path(__file__).resolve().parent

# ═══════════════════════════════════════════════════════
# Phase 1: Manual extraction of worked examples
# ═══════════════════════════════════════════════════════
#
# These are hand-extracted from the source texts because the classical
# Chinese text doesn't follow a machine-parseable template. Each case
# is identified by reading the source, extracting the structural
# components, and annotating the judgment moves.

WORKED_EXAMPLES = [
    # ─── 梅花易數 卷一: 先天占例 ───
    {
        "id": "MH01",
        "source": "梅花易數 卷一",
        "title": "觀梅占 (Plum Blossom Observation)",
        "text_ref": "vol1.txt:177-179",
        "domain": "event_prediction",
        "algorithmic_inputs": {
            "method": "先天 (date-time numerology)",
            "date": "辰年十二月十七日申時",
            "upper_trigram": "兌 (from remainder 2)",
            "lower_trigram": "離 (from remainder 3)",
            "hexagram": "澤火革",
            "moving_line": "初爻",
            "changed_hex": "咸",
            "hu_gua": "乾, 巽",
            "ti_yong": "兌金=體, 離火=用",
            "wuxing_relations": ["離火克兌金(用克體)", "巽木生離火(互生用)", "乾金=體黨"]
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "兌為少女 → 女子",
                "reasoning": "Trigram象 mapped to person type: 兌 = youngest daughter → young woman"
            },
            {
                "type": "analogy",
                "content": "巽為股 → 傷股 (injury to thigh)",
                "reasoning": "Trigram body-part mapping: 巽 = thigh. 巽 is克'd by 乾金兑金 → thigh is injured"
            },
            {
                "type": "integration",
                "content": "互中巽木又逢乾金兑金克之 → 巽木被傷",
                "reasoning": "Combined multiple克 relations on 巽 to conclude injury, not just misfortune"
            },
            {
                "type": "weighting",
                "content": "克體之卦氣盛 (克體 signals dominate)",
                "reasoning": "Counted克體 vs 生體: 離火克兌金 + 巽木生離火 = overwhelming克, so outcome is negative"
            },
            {
                "type": "exception",
                "content": "變為艮土, 兌金得生 → 不至凶危",
                "reasoning": "變卦 provides a生體 signal (艮土生兌金), overriding the dominant克 to prevent death"
            },
            {
                "type": "external",
                "content": "明晚 (timing from context)",
                "reasoning": "Tomorrow evening predicted — timing derived from the situation (plum viewing) not from卦 numerics"
            }
        ],
        "outcome": "明晚有女子折花，園丁逐之，女子失驚墜地，傷其股。不至凶危。",
        "outcome_verified": True
    },
    {
        "id": "MH02",
        "source": "梅花易數 卷一",
        "title": "牡丹占 (Peony Divination)",
        "text_ref": "vol1.txt:181-185",
        "domain": "event_prediction",
        "algorithmic_inputs": {
            "method": "先天 (date-time numerology)",
            "date": "巳年三月十六日卯時",
            "upper_trigram": "乾 (from remainder 1)",
            "lower_trigram": "巽 (from remainder 5)",
            "hexagram": "天風姤",
            "moving_line": "五爻",
            "changed_hex": "鼎",
            "hu_gua": "重乾",
            "ti_yong": "巽木=體, 乾金=用",
            "wuxing_relations": ["乾金克巽木(用克體)", "重乾=克體黨多", "無生體之卦"]
        },
        "judgment_steps": [
            {
                "type": "weighting",
                "content": "互卦又見重乾，克體之卦多矣，卦中無生意",
                "reasoning": "Extreme imbalance: ALL signals克體, zero生體 → destruction certain"
            },
            {
                "type": "analogy",
                "content": "乾為馬 → 被馬踐毀",
                "reasoning": "Trigram象: 乾 = horse. Since乾 is the克ing force, destruction comes via horses"
            },
            {
                "type": "external",
                "content": "午時 = 離明之象 → timing",
                "reasoning": "午 = noon = 離(fire/brightness). Used branch-trigram correspondence for timing"
            }
        ],
        "outcome": "明日午時，貴官觀牡丹，二馬相嚙，群至花間馳驟，花盡為之踐毀。",
        "outcome_verified": True
    },
    {
        "id": "MH03",
        "source": "梅花易數 卷一",
        "title": "鄰夜扣門借物占 (Neighbor Knocking at Night)",
        "text_ref": "vol1.txt:187-191",
        "domain": "object_identification",
        "algorithmic_inputs": {
            "method": "先天 (sound counting)",
            "date": "冬夕酉時",
            "upper_trigram": "乾 (1 knock)",
            "lower_trigram": "巽 (5 knocks)",
            "hexagram": "天風姤",
            "moving_line": "四爻",
            "changed_hex": "巽",
            "hu_gua": "重乾",
            "ti_yong": "N/A (object identification)",
            "wuxing_relations": ["三乾金, 二巽木 → 金木之物"]
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "三乾金, 二巽木 → 金木之物",
                "reasoning": "五行 composition directly maps to material composition: metal+wood object"
            },
            {
                "type": "weighting",
                "content": "乾金短, 巽木長 → 斧",
                "reasoning": "Relative proportion: metal is shorter than wood handle → axe shape"
            },
            {
                "type": "external",
                "content": "夕晚安用鋤？必借斧。蓋斧切於劈柴之用耳。",
                "reasoning": "Time-of-day reasoning: evening → need to chop firewood, not hoe. EXPLICITLY teaches: 推數又須明理"
            }
        ],
        "outcome": "借斧 (borrowing an axe)",
        "outcome_verified": True
    },
    {
        "id": "MH04",
        "source": "梅花易數 卷一",
        "title": "今日動靜如何 (Today's Fortune)",
        "text_ref": "vol1.txt:193-197",
        "domain": "daily_fortune",
        "algorithmic_inputs": {
            "method": "先天 (character tones)",
            "upper_trigram": "坤 (from 今日動 = 1+4+3 = 8)",
            "lower_trigram": "巽 (from 靜如何 = 3+1+1 = 5)",
            "hexagram": "地風升",
            "moving_line": "初爻",
            "changed_hex": "泰",
            "hu_gua": "震, 兌",
            "ti_yong": "巽木=體, 坤土=用",
            "wuxing_relations": ["巽木克坤土(體克用)", "震木=體黨", "兌金克體"]
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "升者, 有升階之義 → going up (to someone's house)",
                "reasoning": "Hexagram name meaning: 升 = ascending → being invited up/elevated"
            },
            {
                "type": "analogy",
                "content": "互震兌有東西席之分",
                "reasoning": "互卦 trigram positions mapped to seating arrangement at a banquet"
            },
            {
                "type": "analogy",
                "content": "兌為口, 坤為腹 → 口腹之事 (dining)",
                "reasoning": "Body part象: mouth + belly = eating/dining occasion"
            },
            {
                "type": "weighting",
                "content": "客不多: 坤土獨立, 無同類之卦氣",
                "reasoning": "Counted坤's party: only one坤, no allies → few guests"
            },
            {
                "type": "weighting",
                "content": "酒不醉: 卦中無坎",
                "reasoning": "Absence reasoning: no坎(water) → no heavy drinking"
            },
            {
                "type": "analogy",
                "content": "坤為黍稷 → 味止黍雞",
                "reasoning": "坤's food象 = grain/millet. Specific menu predicted from trigram associations"
            },
            {
                "type": "integration",
                "content": "卦無相生之義 → 酒不多, 食品不豐",
                "reasoning": "Overall harmony assessment: no mutual生 = modest affair"
            }
        ],
        "outcome": "今日有人相請, 客不多, 酒不醉, 味至黍雞而已。果然。",
        "outcome_verified": True
    },
    {
        "id": "MH05",
        "source": "梅花易數 卷一",
        "title": "西林寺牌額占 (Temple Sign)",
        "text_ref": "vol1.txt:199-205",
        "domain": "feng_shui",
        "algorithmic_inputs": {
            "method": "先天 (stroke counting)",
            "upper_trigram": "艮 (西=7 strokes)",
            "lower_trigram": "坤 (林=8 strokes)",
            "hexagram": "山地剝",
            "moving_line": "三爻",
            "changed_hex": "艮",
            "hu_gua": "重坤",
            "ti_yong": "坤土=體, 艮土=用",
            "wuxing_relations": ["比和(坤艮皆土)", "群陰剝陽"]
        },
        "judgment_steps": [
            {
                "type": "exception",
                "content": "寺者純陽之所居, 今卦得重陰之爻 → 不吉",
                "reasoning": "OVERRIDES the比和(normally吉) reading. Context: Buddhist temple = pure陽 place, but卦 is pure陰 → contradiction"
            },
            {
                "type": "analogy",
                "content": "群陰剝陽 → 陰人之禍",
                "reasoning": "Hexagram name/meaning: 剝 = stripping away. 陰 overwhelming 陽 → women causing trouble in monks' quarters"
            },
            {
                "type": "external",
                "content": "Remedy: add hooks to 林 → changes卦 to 山澤損 → 吉",
                "reasoning": "Physical intervention changes the numerological input → new卦 is favorable. Practitioner intervenes in causality."
            }
        ],
        "outcome": "寺中果有陰人之禍。添林字兩鉤後，寺果無事。",
        "outcome_verified": True
    },
    {
        "id": "MH06",
        "source": "梅花易數 卷一",
        "title": "老人有憂色占 (Worried Old Man)",
        "text_ref": "vol1.txt:209-213",
        "domain": "personal_fate",
        "algorithmic_inputs": {
            "method": "後天 (observed person + direction)",
            "date": "己丑日卯時",
            "upper_trigram": "乾 (old man → 乾)",
            "lower_trigram": "巽 (巽方 direction)",
            "hexagram": "天風姤",
            "moving_line": "九四",
            "changed_hex": "N/A",
            "hu_gua": "重乾",
            "ti_yong": "巽木=體, 乾金=用",
            "wuxing_relations": ["乾金克巽木(用克體)", "重乾克體(互克體)", "無生體之卦"]
        },
        "judgment_steps": [
            {
                "type": "integration",
                "content": "易辭: 包無魚, 起凶 → 不吉",
                "reasoning": "爻辭 consulted AND found consonant with卦理 (both negative)"
            },
            {
                "type": "weighting",
                "content": "巽木為體, 乾金克之, 互卦重乾俱克體, 無生氣",
                "reasoning": "All signals克體, zero生體 → certain disaster"
            },
            {
                "type": "external",
                "content": "時在途行, 其應速 → 取成卦之數中分其半 → 5日",
                "reasoning": "Practitioner's own motion state (walking) determines speed of outcome. Then halves the total卦 number to get the day count."
            },
            {
                "type": "analogy",
                "content": "包無魚 + 卦象 → 魚骨鯁而終",
                "reasoning": "爻辭 mentions 'no fish' → death comes via fish (fish bone choking). Ironic inversion of the text."
            }
        ],
        "outcome": "五日後赴吉席, 因魚骨鯁而終。",
        "outcome_verified": True
    },
    {
        "id": "MH07",
        "source": "梅花易數 卷一",
        "title": "少年有喜色占 (Happy Young Man)",
        "text_ref": "vol1.txt:215-217",
        "domain": "personal_fate",
        "algorithmic_inputs": {
            "method": "後天 (observed person + direction)",
            "date": "壬申日午時",
            "upper_trigram": "艮 (少年 → 艮少男)",
            "lower_trigram": "離 (離方 south)",
            "hexagram": "山火賁",
            "moving_line": "六五",
            "changed_hex": "家人",
            "hu_gua": "震, 坎",
            "ti_yong": "離火=體, 艮土=用",
            "wuxing_relations": ["艮土泄離火(用泄體)", "互變俱生體"]
        },
        "judgment_steps": [
            {
                "type": "integration",
                "content": "爻辭: 賁於丘園, 束帛戔戔, 吝終吉 → 吉 + 聘幣",
                "reasoning": "爻辭 mentions 束帛(bundled silk) = betrothal gifts. Combined with卦理(生體) = engagement"
            },
            {
                "type": "weighting",
                "content": "離為體, 互變俱生之 → 大吉",
                "reasoning": "All互 and變卦 signals生體 → strongly positive outcome"
            },
            {
                "type": "analogy",
                "content": "束帛戔戔 → 聘幣之喜",
                "reasoning": "Silk gifts in爻辭 → betrothal/engagement gifts. Direct textual-to-situational analogy."
            },
            {
                "type": "external",
                "content": "十七日內 (from total number 17)",
                "reasoning": "Timing from the sum of numbers used to construct the卦"
            }
        ],
        "outcome": "十七日內必有聘幣之喜。至期果然定親。",
        "outcome_verified": True
    },
    {
        "id": "MH08",
        "source": "梅花易數 卷一",
        "title": "牛哀鳴占 (Ox Mournful Cry)",
        "text_ref": "vol1.txt:219-223",
        "domain": "animal_fate",
        "algorithmic_inputs": {
            "method": "後天 (animal + direction)",
            "date": "癸卯日午時",
            "upper_trigram": "坤 (牛 → 坤)",
            "lower_trigram": "坎 (坎方 north)",
            "hexagram": "地水師",
            "moving_line": "三爻",
            "changed_hex": "升",
            "hu_gua": "坤, 震",
            "ti_yong": "坤土=體, 坎水=用",
            "wuxing_relations": ["坤土克坎水(體克用)", "互變俱克體(震木克坤土)"]
        },
        "judgment_steps": [
            {
                "type": "integration",
                "content": "爻辭: 師或輿尸, 凶 → combined with卦理",
                "reasoning": "爻辭 says 'army transports corpses' = death. Consonant with克體 signals."
            },
            {
                "type": "weighting",
                "content": "坤為體, 互變俱克之, 無生氣",
                "reasoning": "All signals克體, zero生 → certain death for the animal"
            },
            {
                "type": "external",
                "content": "二十一日 (from total number 21: 坎6+坤8+午7)",
                "reasoning": "Timing from卦 construction numbers"
            }
        ],
        "outcome": "二十一日內必遭屠殺。二十日果買此牛殺以犒眾。",
        "outcome_verified": True
    },
    {
        "id": "MH09",
        "source": "梅花易數 卷一",
        "title": "雞悲鳴占 (Chicken Sad Cry)",
        "text_ref": "vol1.txt:225-229",
        "domain": "animal_fate",
        "algorithmic_inputs": {
            "method": "後天 (animal + direction)",
            "date": "甲申日卯時",
            "upper_trigram": "巽 (雞 → 巽)",
            "lower_trigram": "乾 (乾方 northwest)",
            "hexagram": "風天小畜",
            "moving_line": "六四",
            "changed_hex": "乾",
            "hu_gua": "離, 兌",
            "ti_yong": "乾金=體, 巽木=用",
            "wuxing_relations": ["乾金克巽木(體克用)", "離火克乾金(互克體)"]
        },
        "judgment_steps": [
            {
                "type": "integration",
                "content": "爻辭: 有孚, 血去惕出, 無咎 → 推之割雞之義",
                "reasoning": "血去 = blood removed → interpreted as slaughter/butchering"
            },
            {
                "type": "analogy",
                "content": "巽木離火 → 烹飪之象",
                "reasoning": "Wood + fire in卦 = cooking imagery. The chicken will be cooked."
            },
            {
                "type": "external",
                "content": "十日 (from total number 10: 巽5+乾1+卯4)",
                "reasoning": "Timing from卦 construction numbers"
            }
        ],
        "outcome": "十日當烹。果十日客至, 有烹雞之驗。",
        "outcome_verified": True
    },
    {
        "id": "MH10",
        "source": "梅花易數 卷一",
        "title": "枯枝墜地占 (Dead Branch Falls)",
        "text_ref": "vol1.txt:231-235",
        "domain": "event_prediction",
        "algorithmic_inputs": {
            "method": "後天 (object + direction)",
            "date": "戊子日辰時",
            "upper_trigram": "離 (枯木 → 離)",
            "lower_trigram": "兌 (兌方 west)",
            "hexagram": "火澤睽",
            "moving_line": "九四",
            "changed_hex": "損",
            "hu_gua": "坎, 離",
            "ti_yong": "兌金=體, 離火=用",
            "wuxing_relations": ["離火克兌金(用克體)", "睽損卦名皆有傷殘之義"]
        },
        "judgment_steps": [
            {
                "type": "integration",
                "content": "爻辭: 睽孤, 遇元夫 + 卦理俱凶",
                "reasoning": "Both爻辭 and五行 analysis point to damage/loss"
            },
            {
                "type": "analogy",
                "content": "睽損卦名俱有傷殘之義",
                "reasoning": "Hexagram NAMES as semantic content: 睽(discord) + 損(diminish) = damage"
            },
            {
                "type": "external",
                "content": "十日 → 伐樹起公榭, 匠者適字元夫",
                "reasoning": "The爻辭 character 元夫 matched the carpenter's actual name. Textual coincidence becomes prophetic."
            }
        ],
        "outcome": "十日當伐。果十日伐樹起公榭, 匠者適字元夫。",
        "outcome_verified": True
    },
    # ─── 梅花易數 卷一: 物數占例 (觀物占) ───
    {
        "id": "MH11",
        "source": "梅花易數 卷三",
        "title": "籠盛物占 (Basket of Objects)",
        "text_ref": "vol3.txt:163",
        "domain": "object_identification",
        "algorithmic_inputs": {
            "method": "後天 (hexagram interpretation)",
            "hexagram": "地天泰",
            "moving_line": "初爻",
            "changed_hex": "升",
            "hu_gua": "震, 兌",
            "ti_yong": "N/A (object identification)"
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "互震兌 → 草木類生土中, 色青根黃",
                "reasoning": "震=wood/green, 兌=yellow → green plant with yellow root"
            },
            {
                "type": "integration",
                "content": "爻辭: 拔茅茹, 以其彙 → 連根之草木, 幹根之草木",
                "reasoning": "爻辭 about pulling up thatch by the roots directly describes the object"
            },
            {
                "type": "analogy",
                "content": "互震為青色, 兌為黃根",
                "reasoning": "Color assignments from trigram associations"
            }
        ],
        "outcome": "草木連根, 新採於土中。互震為青色, 兌為黃根。",
        "outcome_verified": True
    },
    {
        "id": "MH12",
        "source": "梅花易數 卷三",
        "title": "鐘覆物占 (Object Under Bell)",
        "text_ref": "vol3.txt:164",
        "domain": "object_identification",
        "algorithmic_inputs": {
            "method": "後天 (hexagram interpretation)",
            "hexagram": "火風鼎",
            "changed_hex": "雷風恆",
            "hu_gua": "乾, 兌"
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "有聲價氣勢之物 → valuable",
                "reasoning": "鼎 = cauldron/vessel of state → object of value and authority"
            },
            {
                "type": "analogy",
                "content": "互乾兌雖圓而毀 → round but broken",
                "reasoning": "乾=round/complete + 兌=broken/damaged → round object with damage"
            },
            {
                "type": "integration",
                "content": "爻辭: 鼎玉鉉, 大吉 → 玉 + 其色白可用",
                "reasoning": "爻辭 mentions jade → white precious object"
            }
        ],
        "outcome": "玉綬環, 果破矣。(Jade belt ring, indeed broken.)",
        "outcome_verified": True
    },
    # ─── 梅花易數 卷三: 变卦式 ───
    {
        "id": "MH13",
        "source": "梅花易數 卷三",
        "title": "澤火革之傷股 (Revolution Hexagram - Thigh Injury)",
        "text_ref": "vol3.txt:13-14",
        "domain": "person_harm",
        "algorithmic_inputs": {
            "hexagram": "澤火革",
            "hu_gua": "巽",
            "changed_hex": "澤山咸",
            "ti_yong": "兌金=體, 離火=用",
            "wuxing_relations": ["離火克兌金", "巽為股, 乾金克巽"]
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "兌金為少女, 離火克之 → 少女受傷",
                "reasoning": "兌=young woman, fire克金 → young woman is harmed"
            },
            {
                "type": "analogy",
                "content": "巽為股, 乾金克之 → 傷股",
                "reasoning": "巽=thigh, metal克wood → thigh injury"
            },
            {
                "type": "exception",
                "content": "得艮土生入兌金 → 不至於死",
                "reasoning": "變卦 provides rescue signal: 艮土生兌金 → survival"
            }
        ],
        "outcome": "少女傷股, 不至於死。"
    },
    # ─── 梅花易數 卷一: 屋宅占 ───
    {
        "id": "MH14",
        "source": "梅花易數 卷二",
        "title": "田姓起造占 (House Building - Tian Family)",
        "text_ref": "vol2.txt:233",
        "domain": "feng_shui",
        "algorithmic_inputs": {
            "method": "先天 + surname strokes",
            "date": "寅年十二月初一日午時",
            "surname_strokes": "田=6",
            "hexagram": "水風井",
            "changed_hex": "升",
            "hu_gua": "離, 兌",
            "ti_yong": "巽木=體, 坎水=用",
            "wuxing_relations": ["坎水生巽木(用生體)", "兌金克巽木(互克體)", "離火制兌金"]
        },
        "judgment_steps": [
            {
                "type": "weighting",
                "content": "用坎水生體, 雖兌金克, 有離火制金",
                "reasoning": "生體 dominant, 克體 neutralized by離 → overall positive but with caveats"
            },
            {
                "type": "external",
                "content": "酉年月日有損失之憂 (兌金旺時)",
                "reasoning": "Timing of misfortune tied to when the克體 element is seasonally strong"
            },
            {
                "type": "external",
                "content": "亥子水年月日有進益 (坎水旺時)",
                "reasoning": "Timing of fortune tied to when the生體 element is seasonally strong"
            },
            {
                "type": "analogy",
                "content": "家必多口舌之聒, 亦為兌也",
                "reasoning": "兌 = mouth/speech → household arguments. Even when兌 isn't dominant, its象 manifests."
            },
            {
                "type": "integration",
                "content": "木體近春, 喜逢坎水 → 必能發旺",
                "reasoning": "季節 resonance: wood體 + spring season + water生 = flourishing"
            },
            {
                "type": "weighting",
                "content": "二十九年後此屋當毀 (全卦成數). 若非有兌, 再見二十九年無恙。",
                "reasoning": "Lifespan from total卦 number. 兌's presence halves the durability."
            }
        ],
        "outcome": "此居必能發旺, 但多口舌。二十九年後此屋當毀。"
    },
    # ─── 火珠林 examples ───
    {
        "id": "HZL01",
        "source": "火珠林",
        "title": "姤之鼎卦 葬地占 (Burial Site Divination)",
        "text_ref": "huozhulin.md:lines11-18",
        "domain": "feng_shui",
        "algorithmic_inputs": {
            "method": "六爻 (six-line with 六親)",
            "hexagram": "姤之鼎",
            "key_lines": "世持辛丑, 伏甲子金",
            "six_relations": "壬申化己未火, 火克本宮為鬼"
        },
        "judgment_steps": [
            {
                "type": "analogy",
                "content": "世下伏金 → 土中有石",
                "reasoning": "辛丑(earth) conceals 甲子(metal) → earth containing stone"
            },
            {
                "type": "analogy",
                "content": "巽下伏乾 → 乾為大赤 → 石色大赤",
                "reasoning": "Concealed乾 trigram → red color attribute"
            },
            {
                "type": "integration",
                "content": "壬申化己未火, 火克本宮為鬼 → 伏屍鬼",
                "reasoning": "Transformation producing fire克 = ghost/corpse spirit"
            },
            {
                "type": "analogy",
                "content": "申化未 → 西南方",
                "reasoning": "Branch transformation gives directional reading"
            },
            {
                "type": "external",
                "content": "距離計算: 壬申金重數4 + 丑未土5 = 40步",
                "reasoning": "Numerical computation from stem-branch values for physical distance"
            },
            {
                "type": "analogy",
                "content": "壬申乃劍鋒金 → 刀傷之人",
                "reasoning": "納音 five-phase (劍鋒金 = sword-edge metal) → cause of death was blade"
            },
            {
                "type": "analogy",
                "content": "壬午乃楊柳木 → 柳樹旁",
                "reasoning": "納音 identification: 壬午 = willow wood → near willow tree"
            }
        ],
        "outcome": "掘地五尺土中有石, 其色大赤, 離穴四十步西南近柳樹有伏屍, 葬出刀傷之人, 並主火災。"
    },
    # ─── 梅花易數 卷三: 天水訟 ───
    {
        "id": "MH15",
        "source": "梅花易數 卷三",
        "title": "天水訟卦求財 (Seeking Wealth)",
        "text_ref": "vol3.txt:29",
        "domain": "wealth",
        "algorithmic_inputs": {
            "hexagram": "天水訟",
            "changed_hex": "兌",
            "ti_yong": "乾金=體, 坎水=用",
            "wuxing_relations": ["體生用(乾金生坎水) → 泄己之氣"]
        },
        "judgment_steps": [
            {
                "type": "weighting",
                "content": "體生用 → 泄己之氣, 其財空望",
                "reasoning": "體 feeds用 (gold produces water) → energy drain, wealth unobtainable"
            },
            {
                "type": "integration",
                "content": "得離卦屬火能克金 + 午時客來食去酒 → 消耗",
                "reasoning": "離 fire克體金 + temporal context = loss through hospitality expenses"
            }
        ],
        "outcome": "財空望, 午時客來食去酒, 返自消耗。"
    },
]


def phase1_extract():
    """Phase 1: Output structured examples."""
    print("=" * 70)
    print("PHASE 1: Worked Example Extraction")
    print("=" * 70)

    print(f"\n  Total examples extracted: {len(WORKED_EXAMPLES)}")

    # Summary by source
    by_source = Counter(e['source'] for e in WORKED_EXAMPLES)
    print(f"\n  By source:")
    for src, n in by_source.most_common():
        print(f"    {src}: {n}")

    # Summary by domain
    by_domain = Counter(e['domain'] for e in WORKED_EXAMPLES)
    print(f"\n  By domain:")
    for dom, n in by_domain.most_common():
        print(f"    {dom}: {n}")

    # Total judgment steps
    total_steps = sum(len(e['judgment_steps']) for e in WORKED_EXAMPLES)
    print(f"\n  Total judgment steps: {total_steps}")
    print(f"  Mean steps per example: {total_steps/len(WORKED_EXAMPLES):.1f}")

    # Save
    with open(Q3 / 'worked_examples.json', 'w') as f:
        json.dump(WORKED_EXAMPLES, f, ensure_ascii=False, indent=2)
    print(f"\n  Saved to {Q3 / 'worked_examples.json'}")

    return WORKED_EXAMPLES


# ═══════════════════════════════════════════════════════
# Phase 2: Judgment Move Classification
# ═══════════════════════════════════════════════════════

MOVE_TYPES = {
    'analogy': 'Mapping trigram/hexagram imagery to specific situation',
    'weighting': 'Choosing which of multiple signals to prioritize',
    'exception': 'Overriding standard protocol based on special conditions',
    'integration': 'Combining multiple signals into coherent narrative',
    'external': 'Incorporating information not in the hexagram (time, context, querent)',
}


def phase2_classify(examples):
    """Phase 2: Classify and cross-tabulate judgment moves."""
    print("\n" + "=" * 70)
    print("PHASE 2: Judgment Move Classification")
    print("=" * 70)

    # Collect all moves
    all_moves = []
    for ex in examples:
        for step in ex['judgment_steps']:
            all_moves.append({
                'type': step['type'],
                'example_id': ex['id'],
                'domain': ex['domain'],
                'source': ex['source'],
                'content': step['content'],
                'reasoning': step['reasoning'],
            })

    total = len(all_moves)
    print(f"\n  Total judgment moves: {total}")

    # ─── Type distribution ───
    type_counts = Counter(m['type'] for m in all_moves)
    print(f"\n  Move type distribution:")
    print(f"  {'Type':<14} {'Count':>6} {'%':>7}")
    print(f"  {'-'*29}")
    for t in ['analogy', 'weighting', 'integration', 'external', 'exception']:
        n = type_counts.get(t, 0)
        pct = 100 * n / total
        print(f"  {t:<14} {n:>6} {pct:>6.1f}%")

    # ─── Type × Domain cross-tabulation ───
    domains = sorted(set(m['domain'] for m in all_moves))
    types = ['analogy', 'weighting', 'integration', 'external', 'exception']

    cross = defaultdict(Counter)
    for m in all_moves:
        cross[m['domain']][m['type']] += 1

    print(f"\n  Type × Domain cross-tabulation:")
    header = f"  {'Domain':<22}" + ''.join(f"{t[:8]:>9}" for t in types) + f"{'Total':>8}"
    print(header)
    print(f"  {'-'*len(header)}")
    for dom in domains:
        row = cross[dom]
        total_dom = sum(row.values())
        cells = ''.join(f"{row.get(t,0):>9}" for t in types)
        print(f"  {dom:<22}{cells}{total_dom:>8}")

    # ─── Moves per example ───
    moves_per_ex = [len(e['judgment_steps']) for e in examples]
    print(f"\n  Moves per example: min={min(moves_per_ex)}, "
          f"max={max(moves_per_ex)}, mean={sum(moves_per_ex)/len(moves_per_ex):.1f}")

    # ─── Dominant type per example ───
    print(f"\n  Dominant move type per example:")
    for ex in examples:
        tc = Counter(s['type'] for s in ex['judgment_steps'])
        dom_type = tc.most_common(1)[0]
        print(f"    {ex['id']:>5} ({ex['title'][:30]:<30}): "
              f"{dom_type[0]}({dom_type[1]}/{len(ex['judgment_steps'])})")

    # ─── Key patterns ───
    print(f"\n  --- Key Patterns ---")

    # Pattern: Does every example use analogy?
    examples_with_analogy = sum(1 for e in examples
                                if any(s['type'] == 'analogy' for s in e['judgment_steps']))
    print(f"\n  Examples containing 'analogy': {examples_with_analogy}/{len(examples)} "
          f"({100*examples_with_analogy/len(examples):.0f}%)")

    # Pattern: Does every example use external?
    examples_with_external = sum(1 for e in examples
                                 if any(s['type'] == 'external' for s in e['judgment_steps']))
    print(f"  Examples containing 'external': {examples_with_external}/{len(examples)} "
          f"({100*examples_with_external/len(examples):.0f}%)")

    # Pattern: Multi-signal integration
    examples_with_integration = sum(1 for e in examples
                                     if any(s['type'] == 'integration' for s in e['judgment_steps']))
    print(f"  Examples containing 'integration': {examples_with_integration}/{len(examples)} "
          f"({100*examples_with_integration/len(examples):.0f}%)")

    # Pattern: Exception moves (where standard rules are overridden)
    exception_moves = [m for m in all_moves if m['type'] == 'exception']
    print(f"\n  Exception moves (standard rules overridden): {len(exception_moves)}")
    for m in exception_moves:
        print(f"    {m['example_id']}: {m['content'][:60]}")

    # ─── Recurring micro-operations ───
    print(f"\n  --- Recurring Micro-Operations ---")
    operations = Counter()
    for m in all_moves:
        if '為' in m['content'] and '→' in m['content']:
            operations['trigram→象 mapping'] += 1
        if '克體' in m['content'] or '生體' in m['content']:
            operations['生克 balance assessment'] += 1
        if '爻辭' in m['reasoning'] or '易辭' in m['reasoning']:
            operations['爻辭 text consultation'] += 1
        if '日' in m['content'] and ('年' in m['content'] or '月' in m['content'] or '時' in m['content']):
            operations['temporal mapping'] += 1

    for op, n in operations.most_common():
        print(f"    {op}: {n}")

    return all_moves


def write_results(examples, all_moves):
    """Write Q3 results."""
    lines = []
    w = lines.append

    w("# Q3 Phase 1-2: Judgment Boundary Analysis — Results\n")
    w("## Phase 1: Worked Example Extraction\n")
    w(f"- **Total examples:** {len(examples)}")
    w(f"- **Sources:** 梅花易數 卷一-三 ({sum(1 for e in examples if '梅花' in e['source'])}), "
      f"火珠林 ({sum(1 for e in examples if '火珠林' in e['source'])})")
    w(f"- **Total judgment steps:** {len(all_moves)}")
    w(f"- **Mean steps/example:** {len(all_moves)/len(examples):.1f}\n")

    # Domain table
    by_domain = Counter(e['domain'] for e in examples)
    w("| Domain | Examples |")
    w("|--------|---------|")
    for dom, n in by_domain.most_common():
        w(f"| {dom} | {n} |")

    w("\n## Phase 2: Judgment Move Classification\n")

    # Type distribution
    type_counts = Counter(m['type'] for m in all_moves)
    total = len(all_moves)
    w("### Move Type Distribution\n")
    w("| Type | Count | % | Description |")
    w("|------|-------|---|-------------|")
    for t in ['analogy', 'weighting', 'integration', 'external', 'exception']:
        n = type_counts.get(t, 0)
        pct = 100 * n / total
        w(f"| {t} | {n} | {pct:.1f}% | {MOVE_TYPES[t]} |")

    # Coverage
    w("\n### Coverage per Example\n")
    examples_with = {}
    for t in ['analogy', 'weighting', 'integration', 'external', 'exception']:
        n = sum(1 for e in examples if any(s['type'] == t for s in e['judgment_steps']))
        examples_with[t] = n
        w(f"- **{t}** appears in {n}/{len(examples)} examples ({100*n/len(examples):.0f}%)")

    # Key findings
    w("\n## Key Findings\n")
    w("### The Five Judgment Operations\n")
    w("The practitioner's judgment at the 80/20 boundary consists of exactly five "
      "recurring operations:\n")
    w("1. **Analogy** (most frequent): Mapping trigram象 to concrete situation. "
      "This is the PRIMARY judgment operation — it bridges the abstract五行 structure "
      "to the specific question.")
    w("2. **Weighting**: Counting and balancing生克 signals. When multiple卦 give "
      "conflicting signals, the practitioner must decide which dominates.")
    w("3. **Integration**: Combining爻辭 text with卦理 analysis. Neither source alone "
      "determines the judgment — both must converge.")
    w("4. **External**: Incorporating context the hexagram doesn't contain — time of day, "
      "season, the querent's state, the practitioner's own motion.")
    w("5. **Exception**: Overriding standard rules. The rarest move, reserved for cases "
      "where context contradicts the normal reading (e.g., 西林寺: 比和 should be吉 "
      "but context inverts it).\n")

    w("### The Analogy-Dominance Pattern\n")
    w(f"Analogy appears in {examples_with['analogy']}/{len(examples)} examples and "
      f"accounts for {type_counts.get('analogy',0)}/{total} ({100*type_counts.get('analogy',0)/total:.0f}%) "
      f"of all moves. This is the irreducibly non-algorithmic operation — "
      f"no formula determines which of a trigram's dozens of象 associations to activate. "
      f"The practitioner navigates a high-dimensional象 space guided by context.\n")

    w("### The 推數又須明理 Principle\n")
    w("MH03 (axe vs hoe) contains the explicit methodological statement: "
      "'推數又須明理' — calculation must be supplemented by reasoning. "
      "The external/context move is not an add-on but is doctrinally required. "
      "The system is DESIGNED to have an algorithmic gap that judgment fills.\n")

    w("### Connection to Q1 Findings\n")
    w("The 18-dimensional complement opposition (R133) is invisible at the vocabulary level (R135). "
      "This analysis shows WHY: the opposition operates through analogy (trigram→situation mapping), "
      "not through word choice. Two complement hexagrams use different analogies from the same "
      "trigram象 space, creating semantic opposition without vocabulary contrast.")

    with open(Q3 / 'phase12_results.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\n  Results written to {Q3 / 'phase12_results.md'}")


def main():
    examples = phase1_extract()
    all_moves = phase2_classify(examples)
    write_results(examples, all_moves)

    print("\n" + "=" * 70)
    print("DONE — Q3 Phases 1-2 complete.")
    print("=" * 70)


if __name__ == '__main__':
    main()
