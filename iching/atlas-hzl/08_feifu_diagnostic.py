#!/usr/bin/env python3
"""
§V.1: 飛伏 diagnostic table extraction from huozhulin source text.

Extracts 8 飛伏 diagnostic cases from the source text, structures them,
and cross-references with computed hexagram data to count actual instances.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

HERE = Path(__file__).resolve().parent

LIUQIN_NAMES = ["兄弟", "子孫", "父母", "妻財", "官鬼"]
LIUQIN_SHORT = {"兄弟": "兄", "子孫": "孫", "父母": "父", "妻財": "財", "官鬼": "鬼"}

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
SHENG_MAP = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
             "Metal": "Water", "Water": "Wood"}
KE_MAP = {"Wood": "Earth", "Earth": "Water", "Water": "Fire",
          "Fire": "Metal", "Metal": "Wood"}


def five_phase_rel(src_elem, tgt_elem):
    """Relationship from src to tgt."""
    if src_elem == tgt_elem: return "比和"
    if SHENG_MAP[src_elem] == tgt_elem: return "生"
    if KE_MAP[src_elem] == tgt_elem: return "克"
    if SHENG_MAP[tgt_elem] == src_elem: return "被生"
    if KE_MAP[tgt_elem] == src_elem: return "被克"
    return "?"


# ═══════════════════════════════════════════════════════════════════════════
# Diagnostic cases — extracted from huozhulin.md lines 137–237
# ═══════════════════════════════════════════════════════════════════════════

DIAGNOSTIC_CASES = [
    {
        "id": 1,
        "title": "占財伏鬼",
        "source_lines": "137-146",
        "hidden_type": "妻財",
        "flying_type": "官鬼",
        "fei_to_fu_relation": "fu generates fei",
        # 財 generates 官 (財→生→鬼): 妻財泄氣 → the hidden drains into the flying
        "mechanism": "財爻泄鬼無氣 — hidden 妻財 drains its energy generating the flying 官鬼",
        "favorable_conditions": [
            "子孫旺相 (子 can overcome 鬼, releasing 財)",
            "日辰是子孫 (external support from day branch)",
            "子孫透出日辰或持世 (子 manifests externally)",
            "日辰是財 (財 can overcome 父, allowing emergence)",
        ],
        "unfavorable_conditions": [
            "官鬼旺 (the drainer is strong → 財 weaker)",
            "父母旺 (官 generates 父 which overcomes 子, cutting rescue chain)",
        ],
        "summary": "買賣遭傷 — hidden wealth drains into authority. "
                   "Requires 子孫 to break the 鬼 hold.",
    },
    {
        "id": 2,
        "title": "占財伏兄",
        "source_lines": "149-157",
        "hidden_type": "妻財",
        "flying_type": "兄弟",
        "fei_to_fu_relation": "fei overcomes fu",
        # 兄 overcomes 財: the flying actively suppresses the hidden
        "mechanism": "財被兄弟把住 — 兄弟 (sibling/rival) holds 妻財 captive, "
                     "generates 口舌 (disputes)",
        "favorable_conditions": [
            "財爻旺相 (hidden wealth is strong enough to resist)",
            "伏世下 (hidden under 世 → within your control)",
            "透出直日辰 (emerges when day branch matches)",
        ],
        "unfavorable_conditions": [
            "兄弟旺相 (captor is strong)",
            "財休囚 (hidden wealth is weak)",
        ],
        "summary": "口舌相侵 — wealth trapped by rival. If hidden under 世 "
                   "and 旺相, you control the captor and can extract wealth.",
    },
    {
        "id": 3,
        "title": "財伏父母",
        "source_lines": "161-172",
        "hidden_type": "妻財",
        "flying_type": "父母",
        "fei_to_fu_relation": "fu overcomes fei",
        # 財 overcomes 父: the hidden suppresses the flying (but is itself hidden)
        "mechanism": "財伏父下, 子不能生財 — under 父母, 子孫 (財's support) "
                     "is blocked by 父母's克, so only 'half wealth'",
        "favorable_conditions": [
            "財爻旺相 (旺相得半 — at least half is retrievable)",
        ],
        "unfavorable_conditions": [
            "父母旺 (文書/authority figure blocks more)",
            "子孫被克 (support chain cut)",
        ],
        "summary": "旺相得半 — wealth hidden under documents/authority. "
                   "子孫 support chain blocked. At best, half return.",
    },
    {
        "id": 4,
        "title": "財伏子孫",
        "source_lines": "161-172",
        "hidden_type": "妻財",
        "flying_type": "子孫",
        "fei_to_fu_relation": "fei generates fu",
        # 子 generates 財: the flying nourishes the hidden
        "mechanism": "子孫生財, 有氣必滿 — flying 子孫 naturally generates "
                     "the hidden 妻財; most favorable hiding position",
        "favorable_conditions": [
            "子孫旺相 (generator is strong → wealth accumulates)",
            "世應不克子孫 (no interference from 世/應)",
        ],
        "unfavorable_conditions": [
            "父母持世應克子孫 (but even then, if 子孫旺相, still possible)",
        ],
        "summary": "有氣必滿 — wealth hidden under its generator. "
                   "Best possible hiding position. Wealth will manifest.",
    },
    {
        "id": 5,
        "title": "占鬼伏兄",
        "source_lines": "176-184",
        "hidden_type": "官鬼",
        "flying_type": "兄弟",
        "fei_to_fu_relation": "fu overcomes fei",
        # 鬼 overcomes 兄: hidden overcomes flying (hidden is inherently stronger)
        "mechanism": "同類欺凌、不忠 — 兄弟 (peers) covering up 官鬼 means "
                     "colleagues deceive or bureaucrats are untrustworthy",
        "favorable_conditions": [
            "官鬼旺相 (authority is strong enough to emerge)",
            "持世 (anchored to self)",
            "日辰是官鬼 (external authority support)",
            "官鬼能克兄 (authority overcomes deception)",
        ],
        "unfavorable_conditions": [
            "兄弟旺 (deception/rivalry is strong)",
            "所謀之事到底脫空 (plan ultimately amounts to nothing)",
        ],
        "summary": "同類欺凌 — authority hidden under rivalry/deception. "
                   "Main theme: betrayal by peers. Need strong 鬼 to overcome.",
    },
    {
        "id": 6,
        "title": "占鬼伏財",
        "source_lines": "188-198",
        "hidden_type": "官鬼",
        "flying_type": "妻財",
        "fei_to_fu_relation": "fei generates fu",
        # 財 generates 官: flying nourishes hidden, but at the cost of 父母
        "mechanism": "因財不吉, 官吏阻節 — 財 generates 官, but 財 also "
                     "overcomes 父母 (documents), causing bureaucratic blockage",
        "favorable_conditions": [
            "官鬼旺相伏世下 (strong authority under your control)",
            "父爻透出直日辰 (documents manifest at right time)",
        ],
        "unfavorable_conditions": [
            "父母持世獨發 (documents alone move → 重迭艱辛)",
            "財去克了文書 (wealth destroys documentation)",
        ],
        "summary": "因財有傷 — authority hidden under wealth. Wealth "
                   "undermines documentation. Official matters obstructed.",
    },
    {
        "id": 7,
        "title": "官伏父母",
        "source_lines": "202-210",
        "hidden_type": "官鬼",
        "flying_type": "父母",
        "fei_to_fu_relation": "fu generates fei",
        # 官 generates 父: hidden generates flying (hidden drains into documents)
        "mechanism": "官化文書 — authority transforms into paperwork. "
                     "Good for filing suits, filling positions",
        "favorable_conditions": [
            "貼世 (attached to self)",
            "官鬼旺相 (strong authority)",
            "文書直日 (documents match day branch)",
            "利經官下狀、補名目 (suits, appointments)",
        ],
        "unfavorable_conditions": [
            "不伏世下 (not under 世 → not within your control → 艱辛)",
        ],
        "summary": "舉狀經官 — authority hidden under documents. "
                   "Favorable for legal filings and official appointments.",
    },
    {
        "id": 8,
        "title": "官伏子孫",
        "source_lines": "214-222",
        "hidden_type": "官鬼",
        "flying_type": "子孫",
        "fei_to_fu_relation": "fei overcomes fu",
        # 子 overcomes 官: flying actively suppresses hidden
        "mechanism": "去路無門 — 子孫 (the overcomer of 官) sits on top, "
                     "blocking authority completely. Stuck.",
        "favorable_conditions": [
            "官爻旺相在世下 (strong authority under your control)",
            "子孫無氣落空 (blocker is weakened/void)",
            "透出直日辰 (emerges at right time)",
        ],
        "unfavorable_conditions": [
            "子孫旺相 (blocker is strong → 占看夫病即死)",
            "官爻無氣落空 (authority is weak/void → merely 阻滯)",
        ],
        "summary": "去路無門 — authority blocked by its natural overcomer. "
                   "Worst hiding position for 官. Only 散憂 (dispersing worry) is favorable.",
    },
    {
        "id": 9,
        "title": "官鬼伏官",
        "source_lines": "226-237",
        "hidden_type": "官鬼",
        "flying_type": "官鬼",
        "fei_to_fu_relation": "比和",
        # 官 under 官: same type, but 旁爻 官 blocks 親爻 官
        "mechanism": "關隔之象, 小人作難 — a subordinate 官 (petty official) "
                     "screens off the true 官 (authority). Obstruction by middlemen.",
        "favorable_conditions": [
            "旺相相扶 (mutual support when both strong)",
            "親見貴人 (go personally to meet the authority)",
            "世爻動化官鬼父母 (transform through action)",
        ],
        "unfavorable_conditions": [
            "旁爻所隔 (blocked by side lines)",
            "小人作難 (petty interference)",
        ],
        "summary": "小人作難 — true authority hidden behind false authority. "
                   "Must personally bypass intermediaries.",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Cross-reference with computed data
# ═══════════════════════════════════════════════════════════════════════════

def cross_reference(profiles):
    """Match diagnostic cases to actual hexagram-line positions."""
    print("=" * 60)
    print("§V.1: 飛伏 DIAGNOSTIC CROSS-REFERENCE")
    print("=" * 60)

    # For each hexagram with missing 六親: identify which diagnostic applies
    # A 六親 is "hidden" when it's missing from visible lines.
    # The hiding position = the feifu line where that type appears in the root.

    case_matches = defaultdict(list)  # case_id → list of (hex_val, position, details)

    for p in profiles:
        if not p["missing_liuqin"]:
            continue

        pe = p["palace_element"]
        visible_types = {l["liuqin"] for l in p["lines"]}

        for missing_lq in p["missing_liuqin"]:
            # Find which line(s) in the feifu have this missing type
            for l in p["lines"]:
                if l["feifu_liuqin"] == missing_lq and l["liuqin"] != missing_lq:
                    # This position: flying = l["liuqin"], hidden = missing_lq
                    flying = l["liuqin"]
                    hidden = missing_lq

                    # Find matching diagnostic case
                    for case in DIAGNOSTIC_CASES:
                        if case["hidden_type"] == hidden and case["flying_type"] == flying:
                            case_matches[case["id"]].append({
                                "hex_val": p["hex_val"],
                                "hex_name": p["name"],
                                "position": l["position"],
                                "hidden_element": l["feifu_element"],
                                "flying_element": l["element"],
                                "relation": five_phase_rel(l["element"], l["feifu_element"]),
                            })

    # Report
    print(f"\n  {'Case':5s} {'Title':12s} {'Hidden':6s} {'Flying':6s} {'Matches':>7}")
    print(f"  {'─'*5} {'─'*12} {'─'*6} {'─'*6} {'─'*7}")
    total_matches = 0
    for case in DIAGNOSTIC_CASES:
        matches = case_matches.get(case["id"], [])
        print(f"  {case['id']:>5} {case['title']:10s} {case['hidden_type']:6s} "
              f"{case['flying_type']:6s} {len(matches):>7}")
        total_matches += len(matches)

    print(f"\n  Total diagnostic instances: {total_matches}")
    hexes_with_missing = sum(1 for p in profiles if p["missing_liuqin"])
    print(f"  Hexagrams with missing 六親: {hexes_with_missing}/64")

    # Uncovered cases: missing types where no diagnostic applies
    uncovered = 0
    uncov_types = Counter()
    for p in profiles:
        if not p["missing_liuqin"]:
            continue
        for missing_lq in p["missing_liuqin"]:
            for l in p["lines"]:
                if l["feifu_liuqin"] == missing_lq and l["liuqin"] != missing_lq:
                    flying = l["liuqin"]
                    found = any(c["hidden_type"] == missing_lq and c["flying_type"] == flying
                                for c in DIAGNOSTIC_CASES)
                    if not found:
                        uncovered += 1
                        uncov_types[(missing_lq, flying)] += 1

    if uncovered:
        print(f"\n  Uncovered diagnostic combinations: {uncovered}")
        for (h, f), c in uncov_types.most_common():
            print(f"    {h} under {f}: {c}")
    else:
        print(f"\n  All instances covered by diagnostic cases ✓")

    # Detail for each case
    print(f"\n  Detailed matches:")
    for case in DIAGNOSTIC_CASES:
        matches = case_matches.get(case["id"], [])
        if not matches:
            continue
        print(f"\n  Case {case['id']}: {case['title']} ({len(matches)} matches)")
        print(f"    {case['summary'][:70]}")
        for m in matches[:4]:
            print(f"    hex {m['hex_val']:>2} ({m['hex_name']:>6}) L{m['position']}: "
                  f"{m['flying_element']}(飛) {m['relation']} {m['hidden_element']}(伏)")
        if len(matches) > 4:
            print(f"    ... and {len(matches) - 4} more")

    return case_matches


def print_diagnostic_table():
    """Print the full diagnostic table."""
    print("\n" + "=" * 60)
    print("§V.1: 飛伏 DIAGNOSTIC TABLE")
    print("=" * 60)

    print(f"\n  9 diagnostic cases from 火珠林 source text:\n")
    for case in DIAGNOSTIC_CASES:
        print(f"  ┌─ Case {case['id']}: {case['title']} (lines {case['source_lines']})")
        print(f"  │  Hidden: {case['hidden_type']}  Flying: {case['flying_type']}")
        print(f"  │  Relation: {case['fei_to_fu_relation']}")
        print(f"  │  Mechanism: {case['mechanism'][:80]}")
        print(f"  │  Favorable: {case['favorable_conditions'][0]}")
        if len(case['favorable_conditions']) > 1:
            for c in case['favorable_conditions'][1:]:
                print(f"  │             {c}")
        print(f"  │  Unfavorable: {case['unfavorable_conditions'][0]}")
        if len(case['unfavorable_conditions']) > 1:
            for c in case['unfavorable_conditions'][1:]:
                print(f"  │               {c}")
        print(f"  └  Summary: {case['summary'][:70]}")
        print()


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    profiles = json.loads((HERE / "hzl_profiles.json").read_text())
    print(f"Loaded {len(profiles)} profiles\n")

    print_diagnostic_table()
    case_matches = cross_reference(profiles)

    # Write output
    output = []
    for case in DIAGNOSTIC_CASES:
        entry = dict(case)
        entry["matches"] = case_matches.get(case["id"], [])
        entry["match_count"] = len(entry["matches"])
        output.append(entry)

    out_path = HERE / "hzl_feifu_diagnostic.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote {len(output)} diagnostic cases to {out_path}")


if __name__ == "__main__":
    main()
