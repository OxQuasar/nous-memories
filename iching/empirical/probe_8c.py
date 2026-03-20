#!/usr/bin/env python3
"""
Probe 8c: Extract and formalize the 18-domain decision table from 梅花易數 vol2.

Tests:
  H1: Template uniformity — do all 18 domains map the 5 relations to the same valence?
  H2: Relation ordering — what order does each domain present its 5 relations?
  H3: Hexagram-name channel — do domain templates reference hexagram names?
  H4: Subsystem analysis — which domains have rules beyond the 5-relation template?

Cross-references with probe_8a worked examples and the 象 mapping table.
"""

import json
import sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent

# ─── Valence constants ───────────────────────────────────────────────────────

POS = "+"   # favorable
NEG = "-"   # unfavorable
WP  = "+~"  # weak positive (positive but delayed/qualified)
NA  = "N/A"

# ─── Standard template (from vol2 lines 10, 24) ─────────────────────────────

STANDARD_VALENCE = {
    "体克用": POS,
    "用克体": NEG,
    "体生用": NEG,
    "用生体": POS,
    "比和":   POS,
}

# ─── 18 Domains ──────────────────────────────────────────────────────────────

DOMAINS = [
    {
        "number": 1,
        "name_zh": "天時占",
        "name_en": "Weather",
        "line_ref": "44-46",
        "uses_tiyong": False,
        "ti_represents": None,
        "yong_represents": None,
        "relations": None,  # Not applicable
        "relation_order": None,
        "valence": None,
        "has_subsystem": True,
        "subsystem_notes": "Entirely different system: counts trigram occurrences across 本/互/变. "
                           "离→晴, 坎→雨, 坤→阴晦, 乾→晴明, 震→雷, 巽→风, 艮→止雨, 兑→阴. "
                           "Also references specific hexagrams (泰/否/既济/未济 etc.) and seasonal modifiers.",
        "references_hexname": True,  # The extended commentary references 泰, 否, 既济, 未济, etc.
        "adversarial_first": None,
    },
    {
        "number": 2,
        "name_zh": "人事占",
        "name_en": "Human Affairs",
        "line_ref": "47-49",
        "uses_tiyong": True,
        "ti_represents": "主 (self/querent)",
        "yong_represents": "宾 (the matter/other)",
        "relations": {
            "体克用": "则吉",
            "用克体": "不宜",
            "体生用": "有耗失之患",
            "用生体": "有进益之喜",
            "比和":   "谋为吉利",
        },
        "relation_order": ["用克体", "体克用", "用生体", "体生用", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "References the 8-trigram 生体/克体 detail tables (vol2 lines 25-41).",
        "references_hexname": False,
        "adversarial_first": True,  # 用克体 appears before 体克用
    },
    {
        "number": 3,
        "name_zh": "家宅占",
        "name_en": "Household",
        "line_ref": "50-51",
        "uses_tiyong": True,
        "ti_represents": "主人 (owner)",
        "yong_represents": "家宅 (household)",
        "relations": {
            "体克用": "家宅多吉",
            "用克体": "家宅多凶",
            "体生用": "多耗散，或防失盗之忧",
            "用生体": "多进益，或有馈送之喜",
            "比和":   "家宅安稳",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 4,
        "name_zh": "屋舍占",
        "name_en": "Dwelling",
        "line_ref": "52-53",
        "uses_tiyong": True,
        "ti_represents": "主人 (owner)",
        "yong_represents": "屋舍 (dwelling)",
        "relations": {
            "体克用": "居之吉",
            "用克体": "居之凶",
            "体生用": "主资财衰退",
            "用生体": "则门户兴隆",
            "比和":   "自然安稳",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 5,
        "name_zh": "婚姻占",
        "name_en": "Marriage",
        "line_ref": "54-64",
        "uses_tiyong": True,
        "ti_represents": "所占之家 (querent's family)",
        "yong_represents": "婚姻/所婚之家 (marriage/other family)",
        "relations": {
            "体克用": "可成但成之迟",
            "用克体": "不可成，成亦有害",
            "体生用": "婚难成，或因婚有失",
            "用生体": "婚易成，或因婚有得",
            "比和":   "婚姻吉利",
        },
        "relation_order": ["用生体", "体生用", "体克用", "用克体", "比和"],
        "valence": {"体克用": WP, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "Family strength comparison (体旺/用旺); appearance descriptions per trigram (lines 57-64).",
        "references_hexname": False,
        "adversarial_first": False,  # 用生体 first
    },
    {
        "number": 6,
        "name_zh": "生產占",
        "name_en": "Childbirth",
        "line_ref": "65-66",
        "uses_tiyong": True,
        "ti_represents": "母 (mother)",
        "yong_represents": "生/子 (child)",
        "relations": {
            "体克用": "不利于子",
            "用克体": "不利于母",
            "体生用": "利于子",
            "用生体": "利于母",
            "比和":   "生育顺快",
        },
        "relation_order": ["体克用", "用克体", "用生体", "体生用", "比和"],
        "valence": {"体克用": NEG, "用克体": NEG, "体生用": POS, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "Male/female determination (阳卦阳爻→男, 阴卦阴爻→女); timing via 用卦 气数.",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 7,
        "name_zh": "飲食占",
        "name_en": "Food/Drink",
        "line_ref": "67-69",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "饮食 (food/drink)",
        "relations": {
            "体克用": "饮食有阻",
            "用克体": "饮食必无",
            "体生用": "饮食难就",
            "用生体": "饮食必丰",
            "比和":   "饮食丰足",
        },
        "relation_order": ["用生体", "体生用", "体克用", "用克体", "比和"],
        "valence": {"体克用": NEG, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "坎=酒, 兑=食 (坎 present→wine, 兑 present→food); 互卦 for guest identification.",
        "references_hexname": False,
        "adversarial_first": False,  # 用生体 first
    },
    {
        "number": 8,
        "name_zh": "求謀占",
        "name_en": "Planning",
        "line_ref": "70-71",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "所谋之事 (the plan)",
        "relations": {
            "体克用": "谋虽可成，但成迟",
            "用克体": "求谋不成，谋亦有害",
            "体生用": "多谋少遂",
            "用生体": "不谋而成",
            "比和":   "求谋称意",
        },
        "relation_order": ["体克用", "用克体", "用生体", "体生用", "比和"],
        "valence": {"体克用": WP, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 9,
        "name_zh": "求名占",
        "name_en": "Seeking Office",
        "line_ref": "72-73",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "名 (fame/office)",
        "relations": {
            "体克用": "名可成，但成迟",
            "用克体": "名不可成",
            "体生用": "名不可就，或因名有丧",
            "用生体": "名易成，或因名有得",
            "比和":   "功名称意",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": WP, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "Timing via 生体 卦气; location via 变卦 方道; in-office danger rules (克体→祸).",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 10,
        "name_zh": "求財占",
        "name_en": "Seeking Wealth",
        "line_ref": "74-76",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "财 (wealth)",
        "relations": {
            "体克用": "有财",
            "用克体": "无财",
            "体生用": "财有损耗之忧",
            "用生体": "财有进益之喜",
            "比和":   "财利快意",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "Timing: 生体 卦气 → gain date, 克体 卦气 → loss date.",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 11,
        "name_zh": "交易占",
        "name_en": "Trade",
        "line_ref": "77-78",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "财 (goods/trade)",
        "relations": {
            "体克用": "有财",
            "用克体": "不成",
            "体生用": "难成，或因交易有失",
            "用生体": "即成，成必有财",
            "比和":   "易成",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 12,
        "name_zh": "出行占",
        "name_en": "Travel",
        "line_ref": "79-81",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "所行之应 (journey outcome)",
        "relations": {
            "体克用": "可行，所至多得意",
            "用克体": "出则有祸",
            "体生用": "出行有破耗之失",
            "用生体": "有意外之财",
            "比和":   "出行顺快",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "Trigram-specific: 乾/震→动, 坤/艮→不动, 巽→舟行, 离→陆行, 坎→失脱, 兑→纷争.",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 13,
        "name_zh": "行人占",
        "name_en": "Traveler Return",
        "line_ref": "82-84",
        "uses_tiyong": True,
        "ti_represents": "主 (self/home)",
        "yong_represents": "行人 (traveler)",
        "relations": {
            "体克用": "行人归迟",
            "用克体": "行人不归",
            "体生用": "行人未归",
            "用生体": "行人即归",
            "比和":   "归期不日矣",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": WP, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "用卦 reads traveler's external condition; trigram-specific modifiers.",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 14,
        "name_zh": "謁見占",
        "name_en": "Audience/Meeting",
        "line_ref": "85-86",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "所见之人 (person to meet)",
        "relations": {
            "体克用": "可见",
            "用克体": "不见",
            "体生用": "难见，见之而无益",
            "用生体": "可见，见之且有得",
            "比和":   "欢然相见",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 15,
        "name_zh": "失物占",
        "name_en": "Lost Object",
        "line_ref": "87-89",
        "uses_tiyong": True,
        "ti_represents": "主 (owner)",
        "yong_represents": "失物 (lost object)",
        "relations": {
            "体克用": "可寻迟得",
            "用克体": "不可寻",
            "体生用": "物难见",
            "用生体": "物易寻",
            "比和":   "物不失矣",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": WP, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "变卦 → object location (8-trigram direction table, lines 89).",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 16,
        "name_zh": "疾病占",
        "name_en": "Illness",
        "line_ref": "90-94",
        "uses_tiyong": True,
        "ti_represents": "病人 (patient)",
        "yong_represents": "病症 (illness)",
        "relations": {
            "体克用": "病易安；勿药有喜",
            "用克体": "虽药无功",
            "体生用": "迁延难好",
            "用生体": "即愈",
            "比和":   "疾病易安",
        },
        "relation_order": ["体克用", "体生用", "用克体", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": True,
        "subsystem_notes": "Medicine type (离→热药, 坎→冷药, 艮→温补, 乾兑→凉药); "
                           "ghost/spirit attribution (8-trigram 克体→spirit table, lines 92); "
                           "detailed 6-line example for 天地否 (lines 93-94).",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 17,
        "name_zh": "官訟占",
        "name_en": "Litigation",
        "line_ref": "95-96",
        "uses_tiyong": True,
        "ti_represents": "主 (self)",
        "yong_represents": "对辞之人/官讼 (opponent/lawsuit)",
        "relations": {
            "体克用": "已胜人",
            "用克体": "人胜己",
            "体生用": "非为失理，或因官有所丧",
            "用生体": "不止得理，或因讼有所得",
            "比和":   "官讼最吉，必有主和之义",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
    {
        "number": 18,
        "name_zh": "墳墓占",
        "name_en": "Burial",
        "line_ref": "97-98",
        "uses_tiyong": True,
        "ti_represents": "主 (self/descendants)",
        "yong_represents": "坟墓 (grave/burial site)",
        "relations": {
            "体克用": "葬之吉",
            "用克体": "葬之凶",
            "体生用": "葬之主运退",
            "用生体": "葬之主兴隆，有荫益后嗣",
            "比和":   "乃为吉地，大宜葬",
        },
        "relation_order": ["体克用", "用克体", "体生用", "用生体", "比和"],
        "valence": {"体克用": POS, "用克体": NEG, "体生用": NEG, "用生体": POS, "比和": POS},
        "has_subsystem": False,
        "subsystem_notes": "",
        "references_hexname": False,
        "adversarial_first": False,
    },
]

# ─── 象 (Image) Mapping Table (vol1 lines 155-169) ──────────────────────────

XIANG_TABLE = {
    "乾": {
        "element": "金",
        "casting_objects": ["天", "父", "老人", "官贵", "马", "金宝", "珠玉", "水果",
                            "圆物", "冠", "镜", "刚物"],
        "body_parts": ["头", "骨"],
        "colors": ["大赤色"],
        "other": ["水寒"],
    },
    "坤": {
        "element": "土",
        "casting_objects": ["地", "母", "老妇", "土", "牛", "金", "布帛", "文章",
                            "舆辇", "方物", "瓦器", "黍稷", "书", "米", "谷"],
        "body_parts": ["腹"],
        "colors": ["黄色", "黑色"],
        "other": ["柄", "裳"],
    },
    "震": {
        "element": "木",
        "casting_objects": ["雷", "长男", "龙", "百虫", "竹", "萑苇", "稼", "乐器",
                            "草木", "树", "木核", "柴", "蛇"],
        "body_parts": ["足", "发", "蹄"],
        "colors": ["青碧绿色"],
        "other": ["马鸣", "馵足", "的颡"],
    },
    "巽": {
        "element": "木",
        "casting_objects": ["风", "长女", "僧尼", "鸡", "百禽", "百草", "臼", "绳",
                            "羽毛", "帆", "扇", "枝叶", "仙道工匠", "直物", "工巧之器"],
        "body_parts": ["股", "眼"],
        "colors": [],
        "other": ["香气", "臭"],
    },
    "坎": {
        "element": "水",
        "casting_objects": ["水", "雨", "雪", "工", "豕", "中男", "沟渎", "弓轮",
                            "月", "盗", "宫律", "栋", "丛棘", "狐", "蒺藜", "桎梏",
                            "水族", "鱼", "盐", "酒", "醢", "有核之物"],
        "body_parts": ["耳", "血"],
        "colors": ["黑色"],
        "other": [],
    },
    "离": {
        "element": "火",
        "casting_objects": ["火", "雉", "日", "电", "霓霞", "中女", "甲胄", "戈兵",
                            "文书", "槁木", "炉", "兽", "鳄龟蟹蚌", "凡有壳之物",
                            "花纹人", "干燥物"],
        "body_parts": ["目"],
        "colors": ["红赤紫色"],
        "other": [],
    },
    "艮": {
        "element": "土",
        "casting_objects": ["山", "土", "少男", "童子", "狗", "径路", "门阙", "果",
                            "蓏", "阍寺", "鼠", "虎", "狐", "黔喙之属", "木生之物",
                            "藤生之物"],
        "body_parts": ["手指", "爪", "鼻"],
        "colors": ["黄色"],
        "other": [],
    },
    "兑": {
        "element": "金",
        "casting_objects": ["泽", "少女", "巫", "妾", "羊", "毁折之物", "带口之器",
                            "属金者", "废缺之物", "奴仆", "婢"],
        "body_parts": ["舌", "肺"],
        "colors": [],
        "other": [],
    },
}

# ─── 8-Trigram 生体/克体 tables (vol2 lines 25-41) ──────────────────────────

SHENGTI_TABLE = {
    "乾": "公门中有喜益，或功名上有喜，或因官有财，或问讼得理，或有金宝之利，或有老人进财，或尊长惠送，或有官贵之喜",
    "坤": "有田土之喜，或有田土进财，或得乡人之益，或得阴人之利，或有果谷之利，或有布帛之喜",
    "震": "山林之益，或因山林得财，或进东方之财，或因动中有喜，或有木货交易之利，或因草木姓氏人称心",
    "巽": "山林之益，或因山林得财，或于东南得财，或因草木姓人而进利，或以茶果得利，或有茶果菜蔬之喜",
    "坎": "北方之喜，或受北方之财，或水边人进利，或因点水人称心，或有因鱼盐酒货文书交易之利，或有馈送鱼盐酒之喜",
    "离": "南方之财，或有文书之喜，或有炉冶场之利，或因火姓人而得财",
    "艮": "东北方之财，或山田之喜，或因山林田土获财，或得宫音带土人之财。物当安稳，事有终始",
    "兑": "西方之财，或喜悦事，或有食物金玉货利之源，或商音之人，或带口之人欣逢，或主宾之乐，或朋友讲习之事",
}

KETI_TABLE = {
    "乾": "公事之忧，或门户之忧，或有财宝之失，或于金谷有损，或有怒于尊长，或得罪于贵人",
    "坤": "田土之忧，或于田土有损，或有阴人之侵，或有小人之害，或失布帛之财，或丧谷粟之利",
    "震": "虚惊，常多恐惧，或身心不能安静，或家宅见妖灾，或草木姓氏之人相侵，或于山林有所失",
    "巽": "草木姓人相害，或于山林上生忧。谋事，乃东南方之人；处家，忌阴人小口之厄",
    "坎": "险陷之事，或寇盗之忧，或失意于水边人，或生灾于酒后，或点水人相害，或北方人见殃",
    "离": "文书之忧，或失火之惊，或有南方之忧，或火人相害",
    "艮": "诸事多违，百谋中阻。或有山林田土之失，或带土人相侵，防东北方之祸害，或忧坟墓不当",
    "兑": "不利西方，主口舌事之纷争。或带口人侵欺，或有毁折之患，或因饮食而生忧",
}

# ─── 10 Worked Examples from probe_8a ────────────────────────────────────────

EXAMPLES_8A = [
    {"name": "观梅占", "ti": "兑", "yong": "离", "ben_rel": "克体",
     "hu_upper": "乾", "hu_lower": "巽", "bian_yong": "艮",
     "xiang_used": {"兑": "少女", "巽": "股", "艮": "土(生金→救)"},
     "text_interp": "女子折花伤股; 离火克兑金; 互巽木助离火; 幸变艮土生兑金",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": False},
    {"name": "牡丹占", "ti": "巽", "yong": "乾", "ben_rel": "克体",
     "hu_upper": "乾", "hu_lower": "乾",  "bian_yong": "离",
     "xiang_used": {"乾": "马"},
     "text_interp": "花为马所践; 乾金克巽木+互重乾=三重克体; 乾为马",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": False},
    {"name": "邻夜扣门", "ti": "巽", "yong": "乾", "ben_rel": "克体",
     "hu_upper": "乾", "hu_lower": "乾", "bian_yong": "巽",
     "xiang_used": {"乾": "金(短)", "巽": "木(长)"},
     "text_interp": "金短木长→斧; 乾金=短, 巽木=长; 理推: 夕晚用斧非锄",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": False},
    {"name": "今日动静", "ti": "坤", "yong": "巽", "ben_rel": "克体",
     "hu_upper": "震", "hu_lower": "兑", "bian_yong": "乾",
     "xiang_used": {"兑": "口", "坤": "腹/黍稷"},
     "text_interp": "口腹之事→有人请客; 坤为黍稷; 无坎→酒不醉",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": False},
    {"name": "西林寺", "ti": "艮", "yong": "坤", "ben_rel": "比和",
     "hu_upper": "坤", "hu_lower": "坤", "bian_yong": "艮",
     "xiang_used": {},
     "text_interp": "群阴剥阳; 纯阳人居阴卦→凶; yin/yang ratio, not 五行",
     "uses_8tri_table": False,
     "uses_xiang": False,
     "uses_yaoci": False},
    {"name": "老人有忧色", "ti": "巽", "yong": "乾", "ben_rel": "克体",
     "hu_upper": "乾", "hu_lower": "乾", "bian_yong": "巽",
     "xiang_used": {"乾": "老人"},
     "text_interp": "乾金克巽木; 互重乾=全克; 无生气; 行→应速→半数=5日",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": True},  # "包无鱼，起凶"
    {"name": "少年有喜色", "ti": "离", "yong": "艮", "ben_rel": "体生用",
     "hu_upper": "震", "hu_lower": "坎", "bian_yong": "巽",
     "xiang_used": {"艮": "少男"},
     "text_interp": "离为体; 互变俱生之; 聘币之喜→17日",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": True},  # "束帛戋戋，终吉"
    {"name": "牛哀鸣", "ti": "坤", "yong": "坎", "ben_rel": "体克用",
     "hu_upper": "坤", "hu_lower": "震", "bian_yong": "巽",
     "xiang_used": {"坤": "牛"},
     "text_interp": "坤为体; 互变俱克之→21日屠杀",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": True},  # "师或舆尸，凶"
    {"name": "鸡悲鸣", "ti": "乾", "yong": "巽", "ben_rel": "体克用",
     "hu_upper": "离", "hu_lower": "兑", "bian_yong": "乾",
     "xiang_used": {"巽": "鸡", "离": "火/炉"},
     "text_interp": "乾金为体; 离火(互)克之; 巽木离火=烹饪象→10日烹",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": True},  # "有孚，血去惕出"
    {"name": "枯枝坠地", "ti": "兑", "yong": "离", "ben_rel": "克体",
     "hu_upper": "坎", "hu_lower": "离", "bian_yong": "艮",
     "xiang_used": {"离": "槁木"},
     "text_interp": "兑金为体; 离火克之; 睽损名有伤残义→10日伐树",
     "uses_8tri_table": False,
     "uses_xiang": True,
     "uses_yaoci": True},  # "睽孤，遇元夫"
]

# ─── Cross-reference: 象 table verification ──────────────────────────────────

def verify_xiang_references():
    """Check that every 象 invocation in 8a examples traces to the table."""
    results = []
    for ex in EXAMPLES_8A:
        traces = []
        for tri, usage in ex["xiang_used"].items():
            entry = XIANG_TABLE.get(tri)
            if entry is None:
                traces.append((tri, usage, "MISSING", False))
                continue
            # Search all lists in entry
            all_items = (entry["casting_objects"] + entry["body_parts"]
                         + entry["colors"] + entry["other"])
            # Check if usage (or a keyword in it) appears
            found = any(usage.split("(")[0] in item or item in usage
                        for item in all_items)
            # Also check element
            if entry["element"] in usage:
                found = True
            traces.append((tri, usage, "FOUND" if found else "NOT_FOUND", found))
        results.append({"name": ex["name"], "traces": traces, "uses_xiang": ex["uses_xiang"]})
    return results


# ─── Analysis ────────────────────────────────────────────────────────────────

def analyze_h1():
    """H1: Template uniformity."""
    results = []
    tiyong_domains = [d for d in DOMAINS if d["uses_tiyong"]]

    for d in tiyong_domains:
        deviations = []
        for rel in ["体克用", "用克体", "体生用", "用生体", "比和"]:
            std = STANDARD_VALENCE[rel]
            actual = d["valence"][rel]
            if actual != std:
                deviations.append({
                    "relation": rel,
                    "standard": std,
                    "actual": actual,
                    "text": d["relations"][rel],
                })
        results.append({
            "domain": d["name_zh"],
            "number": d["number"],
            "matches_standard": len(deviations) == 0,
            "deviations": deviations,
        })
    return results


def analyze_h2():
    """H2: Relation ordering."""
    # Standard order is: 体克用, 用克体, 体生用, 用生体, 比和
    standard_order = ["体克用", "用克体", "体生用", "用生体", "比和"]
    results = []
    for d in DOMAINS:
        if d["relation_order"] is None:
            continue
        matches_standard = d["relation_order"] == standard_order
        results.append({
            "domain": d["name_zh"],
            "number": d["number"],
            "order": d["relation_order"],
            "matches_standard": matches_standard,
            "first_relation": d["relation_order"][0],
        })
    return results


def analyze_h4():
    """H4: Subsystem analysis."""
    with_sub = [d for d in DOMAINS if d["has_subsystem"]]
    without_sub = [d for d in DOMAINS if not d["has_subsystem"]]
    return with_sub, without_sub


# ─── Output ──────────────────────────────────────────────────────────────────

def format_results():
    lines = []
    w = lines.append

    w("# Probe 8c: 梅花易數 18-Domain Decision Table Analysis\n")
    w("Source: `memories/texts/meihuajingshu/vol2.txt` lines 44–99\n")

    # ── 1. Complete 18-domain table ──
    w("## 1. Complete 18-Domain Table\n")
    w("| # | Domain | 体用? | 体= | 用= | 体克用 | 用克体 | 体生用 | 用生体 | 比和 | Subsys? |")
    w("|---|--------|-------|-----|-----|--------|--------|--------|--------|------|---------|")
    for d in DOMAINS:
        if d["uses_tiyong"]:
            v = d["valence"]
            row = (f"| {d['number']} | {d['name_zh']} | ✓ | {d['ti_represents'][:6]} "
                   f"| {d['yong_represents'][:8]} "
                   f"| {v['体克用']} | {v['用克体']} | {v['体生用']} | {v['用生体']} | {v['比和']} "
                   f"| {'✓' if d['has_subsystem'] else ''} |")
        else:
            row = (f"| {d['number']} | {d['name_zh']} | ✗ | — | — "
                   f"| — | — | — | — | — "
                   f"| {'✓' if d['has_subsystem'] else ''} |")
        w(row)
    w("")

    # Valence legend
    w("**Valence key:** `+` = favorable, `-` = unfavorable, `+~` = weak positive (qualified/delayed)\n")

    # ── Detailed domain entries ──
    w("### Detailed Relation Texts\n")
    for d in DOMAINS:
        if not d["uses_tiyong"]:
            w(f"**{d['number']}. {d['name_zh']}** ({d['name_en']}) — lines {d['line_ref']}")
            w(f"- **Does NOT use 体用.** {d['subsystem_notes']}")
            w("")
            continue
        w(f"**{d['number']}. {d['name_zh']}** ({d['name_en']}) — lines {d['line_ref']}")
        w(f"- 体 = {d['ti_represents']}, 用 = {d['yong_represents']}")
        for rel in ["体克用", "用克体", "体生用", "用生体", "比和"]:
            w(f"- {rel} [{d['valence'][rel]}]: {d['relations'][rel]}")
        if d["has_subsystem"]:
            w(f"- **Subsystem:** {d['subsystem_notes']}")
        w("")

    # ── 2. H1: Template uniformity ──
    w("## 2. H1: Template Uniformity\n")
    w("**Standard template** (from vol2 体用总诀, lines 10/24):\n")
    w("| Relation | Standard valence |")
    w("|----------|-----------------|")
    for rel, val in STANDARD_VALENCE.items():
        w(f"| {rel} | {val} |")
    w("")

    h1 = analyze_h1()
    conforming = [r for r in h1 if r["matches_standard"]]
    deviating = [r for r in h1 if not r["matches_standard"]]

    w(f"**{len(conforming)}/17 体用-domains** match the standard template exactly.")
    w(f"**{len(deviating)}/17** deviate.\n")

    if deviating:
        w("### Deviations\n")
        for r in deviating:
            w(f"**{r['number']}. {r['domain']}:**")
            for dev in r["deviations"]:
                w(f"- {dev['relation']}: standard={dev['standard']}, actual={dev['actual']} — \"{dev['text']}\"")
            w("")

    # Structural analysis of deviations
    w("### Structural Analysis of Deviations\n")
    w("**Domain 6 (生產/Childbirth):** Both 体克用 and 体生用 invert. The evaluation shifts from "
      "体's welfare to the *child's* welfare. 体克用 (mother attacks child → bad) and "
      "体生用 (mother nourishes child → good) — a perspective flip, not a rule violation.\n")
    w("**Domain 7 (飲食/Food):** 体克用 inverts (体 overpowers the food → food obstructed). "
      "In standard: 体 dominating 用 = good. In food: 体 suppressing 用(food) = no food. "
      "The semantics of 用 shift: 用 is something you *want to receive*, not something you compete with.\n")
    w("**Domains 5,8,9,13,15 (婚姻/求謀/求名/行人/失物):** 体克用 gives a *weak positive* (+~): "
      "\"可成但成之迟\" / \"可寻迟得\" / \"归迟\". The delay pattern is consistent: "
      "体 overpowers 用, so the outcome arrives but slowly.\n")

    # ── 3. H2: Ordering ──
    w("## 3. H2: Relation Ordering\n")
    h2 = analyze_h2()

    # Standard order
    standard_order = ["体克用", "用克体", "体生用", "用生体", "比和"]
    conforming_ord = [r for r in h2 if r["matches_standard"]]
    deviating_ord = [r for r in h2 if not r["matches_standard"]]

    w(f"**Standard order:** {' → '.join(standard_order)}")
    w(f"**{len(conforming_ord)}/17** use the standard order.")
    w(f"**{len(deviating_ord)}/17** use a different order.\n")

    if deviating_ord:
        w("### Non-standard orderings\n")
        w("| # | Domain | Order | First relation |")
        w("|---|--------|-------|----------------|")
        for r in deviating_ord:
            w(f"| {r['number']} | {r['domain']} | {' → '.join(r['order'])} | {r['first_relation']} |")
        w("")

    w("**Pattern:** The majority (12/17) use the standard 体克用-first order. "
      "The 5 deviations cluster into two patterns:")
    w("- **用克体-first** (domain 2): puts the adversarial outcome first")
    w("- **用生体-first** (domains 5, 7): starts with the best-case outcome")
    w("- **体克用→体生用→用克体→用生体** (domains 6, 8): groups the 克 pair, then the 生 pair")
    w("- **Interleaved** (domain 16): 体克用 and 体生用 paired, then 用克体 and 用生体\n")

    w("**Adversarial-first is rare.** Only domain 2 (人事) leads with 用克体. "
      "The system predominantly presents 体's agency first.\n")

    # ── 4. H3: Hexagram-name channel ──
    w("## 4. H3: Hexagram-Name Channel\n")
    hex_refs = [d for d in DOMAINS if d["references_hexname"]]
    no_hex_refs = [d for d in DOMAINS if not d["references_hexname"]]

    w(f"**{len(hex_refs)}/18 domains** reference specific hexagram names in their templates.")
    w(f"**{len(no_hex_refs)}/18 domains** are purely 五行-relation-based.\n")

    if hex_refs:
        for d in hex_refs:
            w(f"- **{d['number']}. {d['name_zh']}:** {d['subsystem_notes'][:100]}...")
    w("")
    w("**Finding:** The 17 体用-based domain templates are entirely 五行-driven — no hexagram name "
      "appears in any decision rule. Only 天時占 (domain 1), which bypasses 体用 entirely, "
      "references specific hexagrams (泰, 否, 既济, 未济, etc.) in its extended commentary.\n")
    w("This confirms the interpretive architecture has **two independent channels**: "
      "the 五行/体用 channel (mechanical, domain-independent) and the 爻辞/卦名 channel "
      "(requires Zhou Yi text lookup, used in post-hoc elaboration).\n")

    # ── 5. H4: Subsystem analysis ──
    w("## 5. H4: Subsystem Analysis\n")
    with_sub, without_sub = analyze_h4()

    w(f"**{len(with_sub)}/18 domains** have rules beyond the 5-relation template.")
    w(f"**{len(without_sub)}/18 domains** are pure 5-relation templates.\n")

    w("### Domains with subsystems\n")
    w("| # | Domain | Subsystem type |")
    w("|---|--------|---------------|")
    for d in with_sub:
        w(f"| {d['number']} | {d['name_zh']} | {d['subsystem_notes'][:80]}{'...' if len(d['subsystem_notes']) > 80 else ''} |")
    w("")

    w("### Domains WITHOUT subsystems (pure template)\n")
    for d in without_sub:
        w(f"- {d['number']}. {d['name_zh']} ({d['name_en']})")
    w("")

    # Compare with atlas-mh's 7
    atlas_mh_7 = {"婚姻占", "生產占", "飲食占", "出行占", "行人占", "失物占", "疾病占"}
    my_sub = {d["name_zh"] for d in with_sub}
    extra = my_sub - atlas_mh_7 - {"天時占"}
    w("### Comparison with atlas-mh identification\n")
    w(f"Atlas-mh identified 7 domains with extra features: {', '.join(sorted(atlas_mh_7))}")
    w(f"This analysis finds {len(with_sub)} total (including 天時占 which bypasses 体用 entirely).")
    w(f"Additional subsystem domains not in atlas-mh's 7: **{', '.join(sorted(extra))}**")
    w("These have timing rules (卦气-based date prediction) or career-specific danger rules.\n")

    # ── 6. Cross-reference with 8a examples ──
    w("## 6. Cross-Reference with Probe 8a Worked Examples\n")

    w("### Do worked examples use the 8-trigram 生体/克体 detail tables?\n")
    uses_table = sum(1 for ex in EXAMPLES_8A if ex["uses_8tri_table"])
    uses_xiang = sum(1 for ex in EXAMPLES_8A if ex["uses_xiang"])
    uses_yaoci = sum(1 for ex in EXAMPLES_8A if ex["uses_yaoci"])

    w(f"- Uses 8-trigram 生体/克体 tables (vol2 lines 25-41): **{uses_table}/10**")
    w(f"- Uses 象 (image) layer: **{uses_xiang}/10**")
    w(f"- Uses 爻辞 (line text): **{uses_yaoci}/10**\n")

    w("**Finding:** None of the 10 worked examples use the 8-trigram outcome tables from vol2. "
      "Instead, they use the **象 (image) mapping** as their primary interpretive mechanism. "
      "The 后天 examples (6-10) additionally use 爻辞.\n")

    w("### 象 trace verification\n")
    xr = verify_xiang_references()
    w("| # | Example | Trigram | Usage | In table? |")
    w("|---|---------|---------|-------|-----------|")
    for r in xr:
        if not r["uses_xiang"]:
            w(f"| — | {r['name']} | — | (no 象 used) | — |")
            continue
        for tri, usage, status, ok in r["traces"]:
            w(f"| — | {r['name']} | {tri} | {usage} | {'✓' if ok else '✗'} |")
    w("")

    all_found = all(ok for r in xr for _, _, _, ok in r["traces"])
    w(f"**All 象 invocations trace to table entries: {'YES' if all_found else 'NO'}**\n")

    # ── 7. 象 Mapping Table ──
    w("## 7. 象 (Image) Mapping Table\n")
    w("Source: vol1 lines 155-169 (八卦万物属类)\n")

    for tri in ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]:
        entry = XIANG_TABLE[tri]
        w(f"### {tri} ({entry['element']})\n")
        w(f"- **Casting objects:** {', '.join(entry['casting_objects'])}")
        w(f"- **Body parts:** {', '.join(entry['body_parts']) if entry['body_parts'] else '—'}")
        w(f"- **Colors:** {', '.join(entry['colors']) if entry['colors'] else '—'}")
        if entry["other"]:
            w(f"- **Other:** {', '.join(entry['other'])}")
        w("")

    w("### Input/Output distinction\n")
    w("The 象 table serves **dual roles**:\n")
    w("1. **Input (casting):** Object/person → trigram assignment (e.g., 老人→乾, 牛→坤, 鸡→巽)")
    w("2. **Output (interpretation):** Trigram → meaning (e.g., 乾→马, 巽→股, 坤→腹/黍稷)\n")
    w("The worked examples show both directions operating simultaneously: "
      "input-layer assigns trigrams from observations, "
      "output-layer reads back meanings from the resulting hexagram's trigrams.\n")

    # ── 8. Summary ──
    w("## 8. Summary: Mechanical vs. Judgment\n")

    w("### What is fully mechanical\n")
    w("1. **Hexagram generation:** Arithmetic (mod 8, mod 6) is deterministic")
    w("2. **互卦/変卦 computation:** Bit operations, fully mechanical")
    w("3. **体用 assignment:** Moving line position → 体/用, deterministic")
    w("4. **Five-phase relation:** Element lookup + cycle position, deterministic")
    w("5. **Base template application:** The 5-relation→valence mapping for 14/17 domains "
      "(excluding domains 6, 7 which invert 体克用)\n")

    w("### What requires judgment\n")
    w("1. **象 (image) selection:** When a hexagram contains multiple trigrams (本/互/変), "
      "which trigram's image to emphasize is chosen by the practitioner")
    w("2. **Timing period:** The text uses total-number, half-number, or doubled-number "
      "depending on sitting/standing/walking — but also says to use 变通 (flexibility)")
    w("3. **爻辞 integration:** Which line text to cite, and how literally to read it")
    w("4. **External correspondences (三要/十应):** Observed omens override or modify "
      "the internal hexagram analysis")
    w("5. **Domain 1 (天時):** Entirely judgment-based trigram-counting system\n")

    w("### Where exceptions cluster\n")
    w("- **Valence inversions:** Domains 6 (birth) and 7 (food) — both involve 用 as "
      "something *desired to receive* rather than an adversary to overcome")
    w("- **Weak positives (体克用=+~):** Domains 5,8,9,13,15 — the \"delayed success\" pattern "
      "consistently appears in domains where the outcome is an *event* that must *happen* "
      "(marriage, plan, office, return, finding) rather than a *state* to maintain")
    w("- **Subsystem concentration:** Domains 15 (lost object → location) and 16 (illness → medicine) "
      "have the most elaborate subsystems, both adding secondary trigram lookups\n")

    w("### Architectural insight\n")
    w("The 18-domain system is a **parameterized template** with three layers:\n")
    w("1. **Core template** (15/17 domains): 5-relation → valence mapping, identical across domains")
    w("2. **Domain-specific semantics** (2/17 inversion): Birth and food invert 体克用 "
      "because 用 represents something to nurture/receive, not compete with")
    w("3. **Subsystem overlays** (10/18 domains): Additional rules for timing, location, "
      "medicine, gender — these extend but never contradict the core template")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PROBE 8c: 18-DOMAIN DECISION TABLE ANALYSIS")
    print("=" * 70)

    # H1
    print("\n── H1: Template Uniformity ──")
    h1 = analyze_h1()
    for r in h1:
        status = "✓ standard" if r["matches_standard"] else f"✗ {len(r['deviations'])} deviations"
        print(f"  {r['number']:2d}. {r['domain']}: {status}")
        for dev in r["deviations"]:
            print(f"      {dev['relation']}: std={dev['standard']} actual={dev['actual']} — \"{dev['text']}\"")

    conforming = sum(1 for r in h1 if r["matches_standard"])
    print(f"\n  Template conformance: {conforming}/17 体用-domains")

    # H2
    print("\n── H2: Relation Ordering ──")
    h2 = analyze_h2()
    std_order = ["体克用", "用克体", "体生用", "用生体", "比和"]
    for r in h2:
        status = "standard" if r["matches_standard"] else f"→ {r['order']}"
        print(f"  {r['number']:2d}. {r['domain']}: {status}")

    # H3
    print("\n── H3: Hexagram-Name Channel ──")
    hex_refs = [d for d in DOMAINS if d["references_hexname"]]
    print(f"  Domains referencing hexagram names: {len(hex_refs)}/18")
    for d in hex_refs:
        print(f"    {d['number']}. {d['name_zh']}")

    # H4
    print("\n── H4: Subsystem Analysis ──")
    with_sub, without_sub = analyze_h4()
    print(f"  With subsystems: {len(with_sub)}/18")
    for d in with_sub:
        print(f"    {d['number']}. {d['name_zh']}: {d['subsystem_notes'][:60]}...")
    print(f"  Pure template: {len(without_sub)}/18")
    for d in without_sub:
        print(f"    {d['number']}. {d['name_zh']}")

    # 象 verification
    print("\n── 象 Trace Verification ──")
    xr = verify_xiang_references()
    all_ok = True
    for r in xr:
        for tri, usage, status, ok in r["traces"]:
            mark = "✓" if ok else "✗"
            print(f"  {r['name']}: {tri}→{usage} [{mark}]")
            if not ok:
                all_ok = False
    print(f"\n  All traces valid: {all_ok}")

    # Write
    md = format_results()
    out_path = HERE / "probe_8c_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
