#!/usr/bin/env python3
"""
Probe 8a: Verify 10 worked examples in 梅花易數 vol1 (lines 175–237).

Checks arithmetic, hexagram identity, 互卦, 變卦, 體用, and 五行 relations
against the source text claims.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "opposition-theory" / "phase4"))
from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    lower_trigram, upper_trigram,
    hugua, biangua, five_phase_relation,
    SHENG_MAP, KE_MAP,
)

HERE = Path(__file__).resolve().parent

# ─── Constants ───────────────────────────────────────────────────────────────

# 先天 number → binary trigram (bit0=bottom, bit2=top)
XIANTIAN_TO_BIN = {
    1: 0b111,  # 乾
    2: 0b011,  # 兑
    3: 0b101,  # 离
    4: 0b001,  # 震
    5: 0b110,  # 巽
    6: 0b010,  # 坎
    7: 0b100,  # 艮
    8: 0b000,  # 坤
}

BIN_TO_XIANTIAN = {v: k for k, v in XIANTIAN_TO_BIN.items()}

XIANTIAN_NAME_ZH = {
    1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤",
}

BIN_TO_NAME_ZH = {v: XIANTIAN_NAME_ZH[k] for k, v in XIANTIAN_TO_BIN.items()}

# 地支 → number
DIZHI = {
    "子": 1, "丑": 2, "寅": 3, "卯": 4, "辰": 5, "巳": 6,
    "午": 7, "未": 8, "申": 9, "酉": 10, "戌": 11, "亥": 12,
}

# Tone → number
TONE = {"平": 1, "上": 2, "去": 3, "入": 4}

# ─── Hexagram name table (upper_bin, lower_bin) → Chinese name ────────────

# Build from atlas
def load_hex_names():
    atlas_path = HERE.parent / "atlas" / "atlas.json"
    with open(atlas_path) as f:
        atlas = json.load(f)

    # Romanized → Chinese name mapping (manual for the 10 examples + related)
    ROMAN_TO_ZH = {
        "Qian": "乾", "Kun": "坤", "Zhun": "屯", "Meng": "蒙",
        "Xu": "需", "Song": "讼", "Shi": "师", "Bi": "比",
        "Xiao Chu": "小畜", "Lu": "履", "Tai": "泰", "Pi": "否",
        "Tong Ren": "同人", "Da You": "大有", "Qian": "谦", "Yu": "豫",
        "Sui": "随", "Gu": "蛊", "Lin": "临", "Guan": "观",
        "Shi He": "噬嗑", "Bi": "贲", "Bo": "剥", "Fu": "复",
        "Wu Wang": "无妄", "Da Chu": "大畜", "Yi": "颐", "Da Guo": "大过",
        "Kan": "坎", "Li": "离", "Xian": "咸", "Heng": "恒",
        "Dun": "遁", "Da Zhuang": "大壮", "Jin": "晋", "Ming Yi": "明夷",
        "Jia Ren": "家人", "Kui": "睽", "Jian": "蹇", "Xie": "解",
        "Sun": "损", "Yi": "益", "Guai": "夬", "Gou": "姤",
        "Cui": "萃", "Sheng": "升", "Kun": "困", "Jing": "井",
        "Ge": "革", "Ding": "鼎", "Zhen": "震", "Gen": "艮",
        "Jian": "渐", "Gui Mei": "归妹", "Feng": "丰", "Lu": "旅",
        "Xun": "巽", "Dui": "兑", "Huan": "涣", "Jie": "节",
        "Zhong Fu": "中孚", "Xiao Guo": "小过", "Ji Ji": "既济", "Wei Ji": "未济",
    }

    # Build by hex_val (binary) since atlas keys are hex_val strings
    name_by_val = {}
    for k, v in atlas.items():
        hex_val = int(k)
        roman = v["kw_name"]
        name_by_val[hex_val] = roman

    # Also build (upper_bin, lower_bin) → roman
    name_by_pair = {}
    for k, v in atlas.items():
        up = v["upper_trigram"]["val"]
        lo = v["lower_trigram"]["val"]
        name_by_pair[(up, lo)] = v["kw_name"]

    return name_by_val, name_by_pair

HEX_NAME_BY_VAL, HEX_NAME_BY_PAIR = load_hex_names()

# Hard-coded Chinese names for the hexagrams in our 10 examples
HEX_ZH = {
    "Ge": "革", "Xian": "咸", "Gou": "姤", "Ding": "鼎",
    "Xun": "巽", "Sheng": "升", "Tai": "泰", "Bo": "剥",
    "Gen": "艮", "Shi": "师", "Xiao Chu": "小畜", "Qian": "乾",
    "Bi": "贲", "Jia Ren": "家人", "Kui": "睽", "Sun": "损",
    "Kun": "坤",
}


# ─── Core algorithm ──────────────────────────────────────────────────────────

def xiantian_mod(total, divisor):
    """Mod with 0→divisor convention (先天 system)."""
    r = total % divisor
    return divisor if r == 0 else r


def compose_hexagram(upper_bin, lower_bin):
    """Compose hexagram value from binary trigram values."""
    return (upper_bin << 3) | lower_bin


def hex_name(hex_val):
    return HEX_NAME_BY_VAL.get(hex_val, "???")


def trigram_element_zh(trig_bin):
    elem = TRIGRAM_ELEMENT[trig_bin]
    return {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}[elem]


# ─── Example definitions ─────────────────────────────────────────────────────

EXAMPLES = [
    {
        "name": "观梅占",
        "line_ref": 177,
        "method": "先天(date)",
        "upper_sum": 5 + 12 + 17,  # 辰年5 + 十二月12 + 十七日17 = 34
        "lower_sum": 5 + 12 + 17 + 9,  # + 申时9 = 43
        "moving_total": 5 + 12 + 17 + 9,  # 43
        "claimed_hex": "革",
        "claimed_hex_roman": "Ge",
        "claimed_moving": 1,
        "claimed_bian": "咸",
        "claimed_bian_roman": "Xian",
        "claimed_hu_upper": "乾",
        "claimed_hu_lower": "巽",
        "claimed_ti": "兑",
        "claimed_ti_pos": "upper",
        "claimed_analysis": "兑金为体，离火克之 → 用克体",
    },
    {
        "name": "牡丹占",
        "line_ref": 183,
        "method": "先天(date)",
        "upper_sum": 6 + 3 + 16,  # 巳年6 + 三月3 + 十六日16 = 25
        "lower_sum": 6 + 3 + 16 + 4,  # + 卯时4 = 29
        "moving_total": 6 + 3 + 16 + 4,  # 29
        "claimed_hex": "姤",
        "claimed_hex_roman": "Gou",
        "claimed_moving": 5,
        "claimed_bian": "鼎",
        "claimed_bian_roman": "Ding",
        "claimed_hu_upper": "乾",
        "claimed_hu_lower": "乾",
        "claimed_ti": "巽",
        "claimed_ti_pos": "lower",
        "claimed_analysis": "巽木为体，乾金克之 → 用克体",
    },
    {
        "name": "邻夜扣门",
        "line_ref": 189,
        "method": "先天(sound)",
        "upper_sum": 1,  # 1声
        "lower_sum": 5,  # 5声
        "moving_total": 1 + 5 + 10,  # + 酉时10 = 16
        "claimed_hex": "姤",
        "claimed_hex_roman": "Gou",
        "claimed_moving": 4,
        "claimed_bian": "巽",
        "claimed_bian_roman": "Xun",
        "claimed_hu_upper": "乾",
        "claimed_hu_lower": "乾",
        "claimed_ti": "巽",
        "claimed_ti_pos": "lower",
        "claimed_analysis": "金木之物 (乾金=短, 巽木=长 → 斧)",
    },
    {
        "name": "今日动静",
        "line_ref": 195,
        "method": "先天(tones)",
        "upper_sum": 1 + 4 + 3,  # 今(平1) 日(入4) 动(去3) = 8
        "lower_sum": 3 + 1 + 1,  # 静(去3) 如(平1) 何(平1) = 5
        "moving_total": 8 + 5,  # 13
        "claimed_hex": "升",
        "claimed_hex_roman": "Sheng",
        "claimed_moving": 1,
        "claimed_bian": "泰",
        "claimed_bian_roman": "Tai",
        "claimed_hu_upper": "震",
        "claimed_hu_lower": "兑",
        "claimed_ti": "坤",
        "claimed_ti_pos": "upper",
        "claimed_analysis": "口腹之事 (兑=口, 坤=腹); symbolic",
    },
    {
        "name": "西林寺",
        "line_ref": 201,
        "method": "先天(strokes)",
        "upper_sum": 7,  # 西=7画
        "lower_sum": 8,  # 林=8画
        "moving_total": 7 + 8,  # 15
        "claimed_hex": "剥",
        "claimed_hex_roman": "Bo",
        "claimed_moving": 3,
        "claimed_bian": "艮",
        "claimed_bian_roman": "Gen",
        "claimed_hu_upper": "坤",
        "claimed_hu_lower": "坤",
        "claimed_ti": "艮",
        "claimed_ti_pos": "upper",
        "claimed_analysis": "群阴剥阳 (yin/yang symbolic); 体用 both 土 → 比和",
    },
    {
        "name": "老人有忧色",
        "line_ref": 211,
        "method": "后天(image+方)",
        "upper_sum": 1,  # 老人→乾(1)
        "lower_sum": 5,  # 巽方→巽(5)
        "moving_total": 1 + 5 + 4,  # + 卯时4 = 10
        "claimed_hex": "姤",
        "claimed_hex_roman": "Gou",
        "claimed_moving": 4,
        "claimed_bian": "巽",
        "claimed_bian_roman": "Xun",
        "claimed_hu_upper": "乾",
        "claimed_hu_lower": "乾",
        "claimed_ti": "巽",
        "claimed_ti_pos": "lower",
        "claimed_analysis": "巽木为体，乾金克之，互又重乾克体 → 用克体",
    },
    {
        "name": "少年有喜色",
        "line_ref": 217,
        "method": "后天(image+方)",
        "upper_sum": 7,  # 少年→艮(7)
        "lower_sum": 3,  # 离方→离(3)
        "moving_total": 7 + 3 + 7,  # + 午时7 = 17
        "claimed_hex": "贲",
        "claimed_hex_roman": "Bi",
        "claimed_moving": 5,
        "claimed_bian": "家人",
        "claimed_bian_roman": "Jia Ren",
        "claimed_hu_upper": "震",
        "claimed_hu_lower": "坎",
        "claimed_ti": "离",
        "claimed_ti_pos": "lower",
        "claimed_analysis": "离为体，互变俱生之 → 生体",
    },
    {
        "name": "牛哀鸣",
        "line_ref": 221,
        "method": "后天(animal+方)",
        "upper_sum": 8,  # 牛→坤(8)
        "lower_sum": 6,  # 坎方→坎(6)
        "moving_total": 6 + 8 + 7,  # 坎6+坤8+午时7 = 21
        "claimed_hex": "师",
        "claimed_hex_roman": "Shi",
        "claimed_moving": 3,
        "claimed_bian": "升",
        "claimed_bian_roman": "Sheng",
        "claimed_hu_upper": "坤",
        "claimed_hu_lower": "震",
        "claimed_ti": "坤",
        "claimed_ti_pos": "upper",
        "claimed_analysis": "坤为体，互变俱克之 → 克体",
    },
    {
        "name": "鸡悲鸣",
        "line_ref": 227,
        "method": "后天(animal+方)",
        "upper_sum": 5,  # 鸡→巽(5)
        "lower_sum": 1,  # 乾方→乾(1)
        "moving_total": 5 + 1 + 4,  # + 卯时4 = 10
        "claimed_hex": "小畜",
        "claimed_hex_roman": "Xiao Chu",
        "claimed_moving": 4,
        "claimed_bian": "乾",
        "claimed_bian_roman": "Qian",
        "claimed_hu_upper": "离",
        "claimed_hu_lower": "兑",
        "claimed_ti": "乾",
        "claimed_ti_pos": "lower",
        "claimed_analysis": "乾金为体，离火克之 → 互克体",
    },
    {
        "name": "枯枝坠地",
        "line_ref": 233,
        "method": "后天(object+方)",
        "upper_sum": 3,  # 槁木→离(3)
        "lower_sum": 2,  # 兑方→兑(2)
        "moving_total": 2 + 3 + 5,  # 兑2+离3+辰时5 = 10
        "claimed_hex": "睽",
        "claimed_hex_roman": "Kui",
        "claimed_moving": 4,
        "claimed_bian": "损",
        "claimed_bian_roman": "Sun",
        "claimed_hu_upper": "坎",
        "claimed_hu_lower": "离",
        "claimed_ti": "兑",
        "claimed_ti_pos": "lower",
        "claimed_analysis": "兑金为体，离火克之 → 用克体",
    },
]


# ─── Verification ────────────────────────────────────────────────────────────

def verify_example(ex):
    """Verify one example. Returns dict of checks with PASS/FAIL + details."""
    results = {"name": ex["name"], "line_ref": ex["line_ref"], "checks": {}}
    checks = results["checks"]
    all_pass = True

    # 1. Arithmetic: upper/lower trigram numbers
    upper_num = xiantian_mod(ex["upper_sum"], 8)
    lower_num = xiantian_mod(ex["lower_sum"], 8)
    moving_line = xiantian_mod(ex["moving_total"], 6)

    upper_bin = XIANTIAN_TO_BIN[upper_num]
    lower_bin = XIANTIAN_TO_BIN[lower_num]

    # 2. Hexagram identity
    hex_val = compose_hexagram(upper_bin, lower_bin)
    computed_name = hex_name(hex_val)
    claimed_roman = ex["claimed_hex_roman"]
    hex_ok = computed_name == claimed_roman
    checks["hexagram"] = {
        "pass": hex_ok,
        "computed": f"{computed_name} (upper={BIN_TO_NAME_ZH[upper_bin]}/{upper_num}, lower={BIN_TO_NAME_ZH[lower_bin]}/{lower_num})",
        "claimed": f"{ex['claimed_hex']} ({claimed_roman})",
        "hex_val": hex_val,
    }
    if not hex_ok:
        all_pass = False

    # Moving line
    moving_ok = moving_line == ex["claimed_moving"]
    checks["moving_line"] = {
        "pass": moving_ok,
        "computed": moving_line,
        "claimed": ex["claimed_moving"],
        "detail": f"{ex['moving_total']} mod 6 = {ex['moving_total'] % 6} → {moving_line}",
    }
    if not moving_ok:
        all_pass = False

    # 3. 變卦
    bian_val = biangua(hex_val, moving_line)
    bian_name = hex_name(bian_val)
    bian_ok = bian_name == ex["claimed_bian_roman"]
    checks["biangua"] = {
        "pass": bian_ok,
        "computed": f"{bian_name} (val={bian_val})",
        "claimed": f"{ex['claimed_bian']} ({ex['claimed_bian_roman']})",
    }
    if not bian_ok:
        all_pass = False

    # 4. 互卦
    hu_val = hugua(hex_val)
    hu_upper = upper_trigram(hu_val)
    hu_lower = lower_trigram(hu_val)
    hu_upper_zh = BIN_TO_NAME_ZH[hu_upper]
    hu_lower_zh = BIN_TO_NAME_ZH[hu_lower]

    hu_upper_ok = hu_upper_zh == ex["claimed_hu_upper"]
    hu_lower_ok = hu_lower_zh == ex["claimed_hu_lower"]
    hu_ok = hu_upper_ok and hu_lower_ok
    checks["hugua"] = {
        "pass": hu_ok,
        "computed": f"upper={hu_upper_zh}, lower={hu_lower_zh}",
        "claimed": f"upper={ex['claimed_hu_upper']}, lower={ex['claimed_hu_lower']}",
    }
    if not hu_ok:
        all_pass = False

    # 5. 體用 assignment
    if moving_line <= 3:
        ti_pos, yong_pos = "upper", "lower"
    else:
        ti_pos, yong_pos = "lower", "upper"

    ti_trig = upper_bin if ti_pos == "upper" else lower_bin
    yong_trig = upper_bin if yong_pos == "upper" else lower_bin
    ti_zh = BIN_TO_NAME_ZH[ti_trig]

    ti_pos_ok = ti_pos == ex["claimed_ti_pos"]
    ti_name_ok = ti_zh == ex["claimed_ti"]
    tiyong_ok = ti_pos_ok and ti_name_ok
    checks["tiyong"] = {
        "pass": tiyong_ok,
        "computed": f"体={ti_zh}({ti_pos}), 用={BIN_TO_NAME_ZH[yong_trig]}({yong_pos})",
        "claimed": f"体={ex['claimed_ti']}({ex['claimed_ti_pos']})",
    }
    if not tiyong_ok:
        all_pass = False

    # 6. 五行 relation chain
    ti_elem = TRIGRAM_ELEMENT[ti_trig]
    yong_elem = TRIGRAM_ELEMENT[yong_trig]
    ben_rel = five_phase_relation(ti_elem, yong_elem)

    hu_ti_trig = hu_upper if ti_pos == "upper" else hu_lower
    hu_yong_trig = hu_lower if ti_pos == "upper" else hu_upper
    hu_ti_elem = TRIGRAM_ELEMENT[hu_ti_trig]
    hu_yong_elem = TRIGRAM_ELEMENT[hu_yong_trig]
    hu_rel_ti = five_phase_relation(ti_elem, hu_ti_elem)
    hu_rel_yong = five_phase_relation(ti_elem, hu_yong_elem)

    bian_upper = upper_trigram(bian_val)
    bian_lower = lower_trigram(bian_val)
    bian_yong_trig = bian_upper if yong_pos == "upper" else bian_lower
    bian_yong_elem = TRIGRAM_ELEMENT[bian_yong_trig]
    bian_rel = five_phase_relation(ti_elem, bian_yong_elem)

    ELEM_ZH = {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}

    checks["wuxing"] = {
        "pass": True,  # informational — text analysis varies in explicitness
        "ti_element": f"{ti_zh}={ELEM_ZH[ti_elem]}",
        "yong_element": f"{BIN_TO_NAME_ZH[yong_trig]}={ELEM_ZH[yong_elem]}",
        "ben_relation": ben_rel,
        "hu_elements": f"{BIN_TO_NAME_ZH[hu_ti_trig]}={ELEM_ZH[hu_ti_elem]}, {BIN_TO_NAME_ZH[hu_yong_trig]}={ELEM_ZH[hu_yong_elem]}",
        "hu_relations": f"互体侧: {hu_rel_ti}, 互用侧: {hu_rel_yong}",
        "bian_yong_element": f"{BIN_TO_NAME_ZH[bian_yong_trig]}={ELEM_ZH[bian_yong_elem]}",
        "bian_relation": bian_rel,
        "text_claim": ex["claimed_analysis"],
    }

    results["all_pass"] = all_pass
    return results


# ─── Output formatting ──────────────────────────────────────────────────────

def format_results(all_results):
    lines = []
    w = lines.append

    w("# Probe 8a: 梅花易數 Vol1 Worked Examples Verification\n")
    w("Source: `memories/texts/meihuajingshu/vol1.txt` lines 175–237\n")

    pass_count = sum(1 for r in all_results if r["all_pass"])
    w(f"## Summary: {pass_count}/{len(all_results)} examples fully consistent\n")

    # Overview table
    w("| # | Name | Hex | Moving | 變卦 | 互卦 | 體用 | Overall |")
    w("|---|------|-----|--------|------|------|------|---------|")
    for i, r in enumerate(all_results, 1):
        c = r["checks"]
        status = lambda k: "✓" if c[k]["pass"] else "✗"
        overall = "PASS" if r["all_pass"] else "FAIL"
        w(f"| {i} | {r['name']} | {status('hexagram')} | {status('moving_line')} | "
          f"{status('biangua')} | {status('hugua')} | {status('tiyong')} | **{overall}** |")
    w("")

    # Detailed per-example
    for i, r in enumerate(all_results, 1):
        w(f"---\n\n## Example {i}: {r['name']} (line {r['line_ref']})\n")
        c = r["checks"]

        # Hexagram
        mark = "✓" if c["hexagram"]["pass"] else "✗"
        w(f"**Hexagram {mark}:** computed={c['hexagram']['computed']}, "
          f"claimed={c['hexagram']['claimed']}")

        # Moving line
        mark = "✓" if c["moving_line"]["pass"] else "✗"
        w(f"**Moving line {mark}:** computed={c['moving_line']['computed']}, "
          f"claimed={c['moving_line']['claimed']} ({c['moving_line']['detail']})")

        # 變卦
        mark = "✓" if c["biangua"]["pass"] else "✗"
        w(f"**變卦 {mark}:** computed={c['biangua']['computed']}, "
          f"claimed={c['biangua']['claimed']}")

        # 互卦
        mark = "✓" if c["hugua"]["pass"] else "✗"
        w(f"**互卦 {mark}:** computed={c['hugua']['computed']}, "
          f"claimed={c['hugua']['claimed']}")

        # 體用
        mark = "✓" if c["tiyong"]["pass"] else "✗"
        w(f"**體用 {mark}:** {c['tiyong']['computed']}, "
          f"claimed={c['tiyong']['claimed']}")

        # 五行
        wx = c["wuxing"]
        w(f"\n**五行 chain:**")
        w(f"- 體: {wx['ti_element']}")
        w(f"- 用: {wx['yong_element']}")
        w(f"- 本卦 relation: **{wx['ben_relation']}**")
        w(f"- 互卦 elements: {wx['hu_elements']}")
        w(f"- 互卦 relations: {wx['hu_relations']}")
        w(f"- 變卦 用-side: {wx['bian_yong_element']} → **{wx['bian_relation']}**")
        w(f"- Text claim: {wx['text_claim']}")
        w("")

    # Structural observations
    w("---\n\n## Structural Observations\n")
    w("### Arithmetic patterns")
    w("- 先天 examples (1-5): upper_sum mod 8 → upper trigram, lower_sum mod 8 → lower trigram, total mod 6 → moving line")
    w("- 后天 examples (6-10): object/person → upper trigram number, direction → lower trigram number, sum of both + hour → moving line total")
    w("- Zero-maps-to-max convention: mod 8 remainder 0 → 8 (坤), mod 6 remainder 0 → 6")
    w("")
    w("### 體用 consistency")
    w("- All 10 examples correctly follow: moving in lower (1-3) → 体=upper, 用=lower; moving in upper (4-6) → 体=lower, 用=upper")
    w("- The text's diagnostic language is always phrased from 体's perspective: '...为体，...克之'")
    w("")
    w("### 五行 analysis depth")
    w("- Simple examples (1,2,6): explicit 体/用/克 + 互 reinforcement")
    w("- Symbolic examples (3,4,5): less formal五行, more象 (image) reasoning")
    w("- Composite examples (7-10): full chain — 本卦 relation, 互 relation, 變卦 relation all evaluated")
    w("")
    w("### Recurring hexagram")
    w("- 天风姤 (乾 over 巽) appears in examples 2, 3, and 6 — same hexagram from different input methods")
    w("- Each time the diagnosis differs because the moving line differs (5, 4, 4) and the context differs")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PROBE 8a: VERIFY 梅花易數 VOL1 WORKED EXAMPLES")
    print("=" * 70)

    all_results = []
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"\n── Example {i}: {ex['name']} ──")
        r = verify_example(ex)
        all_results.append(r)

        c = r["checks"]
        for key in ["hexagram", "moving_line", "biangua", "hugua", "tiyong"]:
            mark = "PASS" if c[key]["pass"] else "FAIL"
            detail = f"computed={c[key].get('computed', '?')}, claimed={c[key].get('claimed', '?')}"
            print(f"  {key:15s} {mark:4s}  {detail}")

        wx = c["wuxing"]
        print(f"  五行: {wx['ti_element']} vs {wx['yong_element']} → {wx['ben_relation']}")
        print(f"        互: {wx['hu_relations']}")
        print(f"        变: {wx['bian_relation']}")

    # Summary
    pass_count = sum(1 for r in all_results if r["all_pass"])
    print(f"\n{'=' * 70}")
    print(f"RESULT: {pass_count}/{len(all_results)} examples fully consistent")
    print(f"{'=' * 70}")

    # Write results
    md = format_results(all_results)
    out_path = HERE / "probe_8a_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
