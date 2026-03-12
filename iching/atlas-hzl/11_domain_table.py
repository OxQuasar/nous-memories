#!/usr/bin/env python3
"""
§VI.1: 用神 selection table — domain-specific reading protocols.

Extracts from huozhulin.md lines 322–1160: each domain section's
用神, 忌神, 世/應 meaning, and key rules.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ═══════════════════════════════════════════════════════════════════════════
# Domain table — extracted from source text
# ═══════════════════════════════════════════════════════════════════════════

DOMAINS = [
    {
        "domain": "占身命",
        "source_lines": "322-328",
        "yongshen": "世",
        "fushen": None,
        "jishen": None,
        "shi_represents": "命 (fate/destiny)",
        "ying_represents": "external circumstances",
        "key_rule": "世爻為命，月卦為身。得時(陽卦陽爻)吉，失時凶。有財有子 + 旺相祿馬 = 福貴。",
        "special": False,
    },
    {
        "domain": "占形性",
        "source_lines": "331-362",
        "yongshen": "世(inner=性) / 應(outer=形)",
        "fushen": None,
        "jishen": None,
        "shi_represents": "inner character (性)",
        "ying_represents": "outer appearance (形)",
        "key_rule": "外卦為形貌，內卦為性情。Eight trigrams map to personality/physique. "
                    "Five elements map to detailed physical attributes.",
        "special": False,
    },
    {
        "domain": "占運限",
        "source_lines": "365-377",
        "yongshen": "世",
        "fushen": None,
        "jishen": None,
        "shi_represents": "starting point of life periods",
        "ying_represents": "—",
        "key_rule": "大限: 陽世順/陰世逆, 5 years per line, cycling. 逢生令吉, 遇刑傷凶. "
                    "Also: 本體=初, 互體=中, 化體=末.",
        "special": False,
    },
    {
        "domain": "占婚姻",
        "source_lines": "380-420",
        "yongshen": "妻財(man) / 官鬼(woman)",
        "fushen": "子孫(嗣)",
        "jishen": "兄弟(man) / 子孫(woman)",
        "shi_represents": "夫 (groom's side)",
        "ying_represents": "婦 (bride's side)",
        "key_rule": "世應宜靜, 財官旺相婚姻可成. 世動男家進退, 應動女家不肯. "
                    "間爻=媒. 附:占婢妾 — 財爻為主象.",
        "special": False,
    },
    {
        "domain": "占孕產",
        "source_lines": "423-433",
        "yongshen": "妻財",
        "fushen": "龍喜胎神",
        "jishen": None,
        "shi_represents": "—",
        "ying_represents": "—",
        "key_rule": "白虎臨財旺相=男, 休囚=女. 乾兌坎離下卦=順產, 震巽艮坤下卦=逆產. "
                    "胎爻陽=男, 陰=女.",
        "special": False,
    },
    {
        "domain": "占科舉",
        "source_lines": "436-449",
        "yongshen": "官鬼",
        "fushen": "父母",
        "jishen": "子孫",
        "shi_represents": "candidate",
        "ying_represents": "examiner/authority",
        "key_rule": "官爻旺相便吉. 父母在世上最佳(文書持世=狀元). "
                    "忌子孫持世不中. 官與文書俱旺相持世方可成.",
        "special": False,
    },
    {
        "domain": "占謁貴",
        "source_lines": "453-464",
        "yongshen": "官鬼",
        "fushen": "妻財",
        "jishen": None,
        "shi_represents": "我 (visitor)",
        "ying_represents": "彼 (the dignitary)",
        "key_rule": "外卦取: 外陽爻可見, 外陰爻不見. 用支出現旺相不動在家. "
                    "世應相生合吉, 相剋凶.",
        "special": False,
    },
    {
        "domain": "占買賣",
        "source_lines": "468-481",
        "yongshen": "妻財",
        "fushen": "子孫",
        "jishen": "兄弟",
        "shi_represents": "seller",
        "ying_represents": "buyer",
        "key_rule": "財福出現必利. 外克內/應克世=易得財. 財旺相主貴宜賣, 休囚主賤宜買.",
        "special": False,
    },
    {
        "domain": "占求財",
        "source_lines": "484-497",
        "yongshen": "妻財",
        "fushen": "子孫",
        "jishen": "兄弟",
        "shi_represents": "求財者 (seeker of wealth)",
        "ying_represents": "wealth source / counterpart",
        "key_rule": "財來扶世不難, 財空鬼旺千水萬山. 子孫=財之源, 加青龍發動大吉. "
                    "父母動=子受傷=財源已絕.",
        "special": False,
    },
    {
        "domain": "占博戲",
        "source_lines": "500-508",
        "yongshen": "子孫",
        "fushen": "妻財",
        "jishen": "官鬼",
        "shi_represents": "我 (player)",
        "ying_represents": "彼 (opponent)",
        "key_rule": "子孫持世旺相獨發便贏. 鬼兄財動便輸. 世旺克應我勝.",
        "special": False,
    },
    {
        "domain": "占出行",
        "source_lines": "512-527",
        "yongshen": "妻財",
        "fushen": "子孫",
        "jishen": "官鬼",
        "shi_represents": "traveler",
        "ying_represents": "destination",
        "key_rule": "財旺大吉, 鬼旺多凶. 遊魂八純皆不可出行. 世墓方大忌. "
                    "財子持世好, 鬼兄動忌.",
        "special": False,
    },
    {
        "domain": "占行人",
        "source_lines": "530-551",
        "yongshen": "妻財(本宮)",
        "fushen": "父母(信)",
        "jishen": "官鬼",
        "shi_represents": "waiting party",
        "ying_represents": "traveler",
        "key_rule": "財為用(本宮財=行人, 旁爻財=音信). 持世立至. "
                    "大忌應坐鬼. 初爻=足, 二爻=身, 俱動來速.",
        "special": False,
    },
    {
        "domain": "占逃亡",
        "source_lines": "554-594",
        "yongshen": "世(逃亡) / 妻財(失物)",
        "fushen": None,
        "jishen": None,
        "shi_represents": "fugitive / querent",
        "ying_represents": "location / captor",
        "key_rule": "歸魂自歸, 八純在親友家. 1-3世易尋, 4-5世難尋. "
                    "附:方位 — 世宮為方, 應宮為所.",
        "special": False,
    },
    {
        "domain": "占失物鬼祟",
        "source_lines": "598-615",
        "yongshen": "官鬼(祟/賊)",
        "fushen": "子孫(捕捉)",
        "jishen": None,
        "shi_represents": "victim",
        "ying_represents": "thief / ghost",
        "key_rule": "陽宮鬼出現=男, 伏藏=女(反對取之). 鬼生方向尋之. "
                    "子孫旺日=獲賊之日.",
        "special": False,
    },
    {
        "domain": "占賊盜",
        "source_lines": "619-641",
        "yongshen": "官鬼(賊) / 妻財(失物)",
        "fushen": "子孫(捕)",
        "jishen": None,
        "shi_represents": "victim",
        "ying_represents": "thief",
        "key_rule": "兩爻鬼以單拆分取. 失物看財: 旺相不空不動可見, 空了動了出屋. "
                    "六爻無鬼安靜=非賊偷去, 乃自失.",
        "special": False,
    },
    {
        "domain": "占鬼神",
        "source_lines": "644-683",
        "yongshen": "官鬼",
        "fushen": None,
        "jishen": None,
        "shi_represents": "household",
        "ying_represents": "spirit",
        "key_rule": "休囚為鬼, 旺相為神. 本象=家親, 旁爻=外人. "
                    "六爻定體(初=小口/灶君, ..., 六=公婆/佛道). 附:六神解.",
        "special": False,
    },
    {
        "domain": "占詞訟",
        "source_lines": "687-710",
        "yongshen": "官鬼",
        "fushen": "父母",
        "jishen": "妻財(折理)",
        "shi_represents": "party (plaintiff or defendant)",
        "ying_represents": "opposing party",
        "key_rule": "下狀論人: 官旺出現必贏. 被論: 官休囚+子孫持世=反得理. "
                    "財動折理(財克文書). 五化爻 patterns for litigation.",
        "special": False,
    },
    {
        "domain": "占脫事散憂",
        "source_lines": "713-726",
        "yongshen": "子孫",
        "fushen": None,
        "jishen": "官鬼",
        "shi_represents": "person seeking release",
        "ying_represents": "obstacle / matter",
        "key_rule": "子孫旺相出現或獨發. 世動自消. 忌應克世, 鬼旺相獨發凶.",
        "special": False,
    },
    {
        "domain": "占疾病",
        "source_lines": "730-818",
        "yongshen": "官鬼(病)",
        "fushen": "子孫(藥/recovery)",
        "jishen": "官鬼(itself — 用神 IS the illness)",
        "shi_represents": "身 (patient's body)",
        "ying_represents": "藥 (medicine/doctor)",
        "key_rule": "應為藥忌坐鬼. 三墓(宮墓/鬼墓/財墓). 鬼五行=病種(金=肺, 木=肝, "
                    "水=腎, 火=心, 土=脾). 鬼內/外=下/上體. 子孫動=recovery. "
                    "附: 病忌官鬼, 病忌父兄, 占醫藥.",
        "special": True,
        "special_protocol": (
            "Inverted protocol: 用神 IS the illness (官鬼). Weaker 鬼 = better. "
            "Three-墓 system (宮墓/鬼墓/財墓) determines prognosis. 鬼's element = "
            "disease type and organ. 鬼's position (inner/outer) = body location. "
            "子孫 active = recovery. Multiple sub-sections: 醫藥(treatment), "
            "病忌官鬼(contraindications), 病忌父兄(support failure)."
        ),
    },
    {
        "domain": "占家宅",
        "source_lines": "822-871",
        "yongshen": "妻財 + 子孫",
        "fushen": None,
        "jishen": "官鬼",
        "shi_represents": "household prosperity",
        "ying_represents": "house structure",
        "key_rule": "專用財福. 內三爻=家. 印綬=堂屋, 財=廚灶, 子=廊廟, 鬼=前廳. "
                    "旺相=新, 休囚=舊. 附: 人口, 起造遷移, 陽宅.",
        "special": False,
    },
    {
        "domain": "占耕種",
        "source_lines": "875-883",
        "yongshen": "妻財",
        "fushen": "子孫",
        "jishen": "官鬼",
        "shi_represents": "farmer",
        "ying_represents": "harvest",
        "key_rule": "財福上卦. 忌鬼值五位. 世克應=倉廩實. 初=田, 二=種, 三=生長, "
                    "四=秀實, 五=收成, 六=農夫. 鬼克各位有對應害處.",
        "special": False,
    },
    {
        "domain": "占蠶桑",
        "source_lines": "886-892",
        "yongshen": "妻財",
        "fushen": "子孫",
        "jishen": "官鬼",
        "shi_represents": "sericulturist",
        "ying_represents": "—",
        "key_rule": "財旺福興大吉. 鬼爻交重不賽終失. 鬼動遠賽, 兄動損. "
                    "子孫木火大吉, 亥子濕死.",
        "special": False,
    },
    {
        "domain": "占畜養",
        "source_lines": "895-905",
        "yongshen": "子孫",
        "fushen": "妻財",
        "jishen": "官鬼",
        "shi_represents": "keeper",
        "ying_represents": "—",
        "key_rule": "財福上卦. 鬼持初爻雞鴨不吉, 官坐五爻牛馬難安. "
                    "鬼五行=疾病類型. 本命爻臨財福無傷則吉.",
        "special": False,
    },
    {
        "domain": "占漁獵",
        "source_lines": "908-916",
        "yongshen": "妻財(物)",
        "fushen": "子孫",
        "jishen": "官鬼",
        "shi_represents": "hunter/fisher",
        "ying_represents": "—",
        "key_rule": "世為主, 財為物, 財子俱見旺相大吉. 震棒/離網/艮犬, 克財者宜用. "
                    "惡殺臨財旺相克世=獸傷.",
        "special": False,
    },
    {
        "domain": "占墳墓",
        "source_lines": "919-930",
        "yongshen": "子孫(祀) + 妻財(祿)",
        "fushen": None,
        "jishen": "官鬼(旺時)",
        "shi_represents": "風水 (geomancy)",
        "ying_represents": "棺槨 (coffin)",
        "key_rule": "鬼=屍, 要無氣. 父=墳宜靜. 財=祿, 子=祀, 要旺相持世. "
                    "鬼旺宜火(化)不宜葬.",
        "special": False,
    },
    {
        "domain": "占朝國",
        "source_lines": "933-945",
        "yongshen": "世(帝王)",
        "fushen": None,
        "jishen": None,
        "shi_represents": "帝王 (emperor)",
        "ying_represents": "功臣 (meritorious officials)",
        "key_rule": "世應相得君臣用心. 六位無克萬國咸寧. 五爻=至尊. "
                    "子孫=儲君, 宜旺相不空.",
        "special": False,
    },
    {
        "domain": "占征戰",
        "source_lines": "949-963",
        "yongshen": "子孫(我軍)",
        "fushen": "妻財(糧)",
        "jishen": "官鬼(敵兵)",
        "shi_represents": "our forces",
        "ying_represents": "enemy",
        "key_rule": "子孫旺相必獲全勝. 出現宜先, 伏藏宜後. "
                    "世應空=和. 兄弟獨發凶. 鬼父旺相/獨發/持世身=大敗.",
        "special": False,
    },
    {
        "domain": "占天時",
        "source_lines": "967-1017",
        "yongshen": "父母(雨) / 妻財(晴)",
        "fushen": None,
        "jishen": None,
        "shi_represents": "weather condition",
        "ying_represents": "—",
        "key_rule": "先看內卦干合, 次看外卦定體. 甲己化土=陰雲, 丁壬化木=風, "
                    "乙庚化金=雨, 丙辛化水=雨, 戊癸化火=晴. "
                    "六親: 父=雨, 財=晴, 兄=風, 子=雲霧, 鬼=雷.",
        "special": True,
        "special_protocol": (
            "Dual-layer system: (1) 天干合化 — day stem + hexagram stems combine "
            "to determine cloud/wind/rain/clear via five transformations. "
            "(2) 六親 overlay — 父母=rain, 妻財=clear, 兄弟=wind, 子孫=cloud, "
            "官鬼=thunder. Inner 動=day, outer 動=night. 辰丑=rain, 未戌=clear. "
            "Detailed timing via 十干 克日定時."
        ),
    },
    {
        "domain": "占射覆",
        "source_lines": "1020-1053",
        "yongshen": "妻財(表) + 官鬼(里)",
        "fushen": None,
        "jishen": None,
        "shi_represents": "里 (inner substance / shape)",
        "ying_represents": "表 (outer surface / material)",
        "key_rule": "財=表(surface), 鬼=里(interior). 陽卦=圓, 陰卦=方. "
                    "應旺=新, 衰=舊. 鬼值八卦定物類. "
                    "附: 覆射物色 — 以官為色, 出現正色, 伏藏旁色.",
        "special": True,
        "special_protocol": (
            "Object identification protocol: 財=surface/material, 鬼=interior/type. "
            "Both visible = complete object. One hidden = partially knowable. "
            "Both hidden = light/empty object. Trigrams determine material class "
            "(乾兌=metal/jade, 震巽=wood/bamboo, 坤艮=earth/stone, 坎=fish/water goods, "
            "離=silk/thread). Shape from 世應 interaction: 合=round, 扶=long, "
            "生=square, 克=damaged. 六神 = directional position."
        ),
    },
    {
        "domain": "占來情",
        "source_lines": "1057-1089",
        "yongshen": "varies — read the dominant 六親",
        "fushen": None,
        "jishen": None,
        "shi_represents": "the diviner",
        "ying_represents": "the querent's hidden concern",
        "key_rule": "卦中多者取來情 — the most frequent 六親 = what the person came to ask about. "
                    "附: 達人事 — 18 pattern-matching rules to identify question type before reading.",
        "special": True,
        "special_protocol": (
            "Reverse protocol: instead of the domain determining the 用神, "
            "the hexagram's composition reveals the domain. Count 六親 frequencies; "
            "the dominant type indicates the concern (父母多=文書/官, 妻財多=財/婚, etc.). "
            "18 pattern rules in 達人事 match structural features (六神 positions, "
            "動爻 patterns, 世應 interactions) to specific question types."
        ),
    },
    {
        "domain": "占姓字",
        "source_lines": "1103-1158",
        "yongshen": "官鬼(object) + 日干",
        "fushen": None,
        "jishen": None,
        "shi_represents": "—",
        "ying_represents": "—",
        "key_rule": "日配用爻, 兼內外互卦正化體象取勝為主. "
                    "干配姓, 支配合, 納音配字. 附: 八卦類/天干類/地支類/五行類 = stroke pattern tables.",
        "special": True,
        "special_protocol": (
            "Character identification protocol: maps trigrams, stems, branches, and "
            "five-phase elements to Chinese character radicals, stroke patterns, and "
            "structural forms. Day stem × 用爻 × inner/outer/互 trigrams combine to "
            "identify surname characters. 30 entries of radical-to-trigram/stem/branch "
            "correspondence tables."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Analysis
# ═══════════════════════════════════════════════════════════════════════════

def analyze():
    """Print domain table summary."""
    print("=" * 60)
    print("§VI.1: 用神 SELECTION TABLE")
    print("=" * 60)

    print(f"\n  Total domains extracted: {len(DOMAINS)}")
    special = [d for d in DOMAINS if d.get("special")]
    standard = [d for d in DOMAINS if not d.get("special")]
    print(f"  Standard protocols: {len(standard)}")
    print(f"  Special protocols: {len(special)}")

    # Summary table
    print(f"\n  {'Domain':14s} {'用神':20s} {'輔神':8s} {'忌神':10s} {'世':12s}")
    print(f"  {'─'*14} {'─'*20} {'─'*8} {'─'*10} {'─'*12}")
    for d in DOMAINS:
        y = (d['yongshen'] or '—')[:20]
        f = (d['fushen'] or '—')[:8]
        j = (d['jishen'] or '—')[:10]
        s = (d['shi_represents'] or '—')[:12]
        marker = " ★" if d.get("special") else ""
        print(f"  {d['domain']:12s}   {y:20s} {f:8s} {j:10s} {s:12s}{marker}")

    # 用神 frequency
    print(f"\n  用神 TYPE FREQUENCY:")
    from collections import Counter
    yongshen_types = Counter()
    for d in DOMAINS:
        y = d['yongshen'] or ''
        for t in ["妻財", "官鬼", "子孫", "父母", "兄弟", "世"]:
            if t in y:
                yongshen_types[t] += 1
    for t, c in yongshen_types.most_common():
        pct = c / len(DOMAINS)
        print(f"    {t}: {c} domains ({pct:.0%})")

    # Special protocols
    print(f"\n  SPECIAL PROTOCOLS:")
    for d in special:
        print(f"\n  ★ {d['domain']} (lines {d['source_lines']})")
        print(f"    {d['special_protocol'][:100]}...")

    # 世/應 meaning distribution
    print(f"\n  世 REPRESENTS:")
    from collections import defaultdict
    shi_cats = defaultdict(list)
    for d in DOMAINS:
        s = d['shi_represents']
        if 'patient' in s or '身' in s:
            shi_cats['self/body'].append(d['domain'])
        elif 'player' in s or 'seeker' in s or 'visitor' in s:
            shi_cats['active seeker'].append(d['domain'])
        elif 'seller' in s or 'farmer' in s:
            shi_cats['producer'].append(d['domain'])
        else:
            shi_cats['other'].append(d['domain'])
    for cat, domains in sorted(shi_cats.items()):
        print(f"    {cat}: {', '.join(domains)}")


def main():
    analyze()

    out_path = HERE / "hzl_domains.json"
    out_path.write_text(json.dumps(DOMAINS, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote {len(DOMAINS)} domains to {out_path}")


if __name__ == "__main__":
    main()
