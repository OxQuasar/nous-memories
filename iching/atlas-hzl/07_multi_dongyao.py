#!/usr/bin/env python3
"""
§IV.2-3: Multi-line analysis + source text transformation patterns.

§IV.2: 世+應 both moving, 2-line patterns, 靜卦 reading
§IV.3: Named patterns from huozhulin source text
"""

import sys
import json
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations
import importlib.util

HERE = Path(__file__).resolve().parent
PHASE4 = HERE.parent / "opposition-theory" / "phase4"
HZL = HERE.parent / "huozhulin"

sys.path.insert(0, str(PHASE4))
from cycle_algebra import NUM_HEX, bit

def _load(name, filepath):
    s = importlib.util.spec_from_file_location(name, filepath)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

p1 = _load("p1", HZL / "01_najia_map.py")
p2 = _load("p2", HZL / "02_palace_kernel.py")
p3 = _load("p3", HZL / "03_liuqin.py")

najia        = p1.najia
BRANCHES     = p1.BRANCHES
BRANCH_ELEMENT = p1.BRANCH_ELEMENT
basin_fn     = p2.basin
liuqin_fn    = p3.liuqin
LIUQIN_NAMES = p3.LIUQIN_NAMES
LIUQIN_SHORT = p3.LIUQIN_SHORT


def load_profiles():
    return json.loads((HERE / "hzl_profiles.json").read_text())

def load_dongyao():
    return json.loads((HERE / "hzl_dongyao.json").read_text())


# ═══════════════════════════════════════════════════════════════════════════
# §IV.2: Multi-line analysis
# ═══════════════════════════════════════════════════════════════════════════

def analyze_shi_ying_both_moving(profiles, dongyao):
    """世+應 both moving analysis."""
    print("=" * 60)
    print("§IV.2.1: 世+應 BOTH MOVING")
    print("=" * 60)

    dy_lookup = {}
    for e in dongyao:
        dy_lookup[(e["hex_val"], e["moving_line"])] = e

    # For each hexagram, get the 化爻 types when 世 and 應 both move
    type_pairs = Counter()
    same_type = 0
    total = 0

    for p in profiles:
        h = p["hex_val"]
        shi = p["shi_line"]
        ying = p["ying_line"]

        shi_dy = dy_lookup[(h, shi)]
        ying_dy = dy_lookup[(h, ying)]

        shi_type = shi_dy["huayao_type"]
        ying_type = ying_dy["huayao_type"]

        type_pairs[(shi_type, ying_type)] += 1
        if shi_type == ying_type:
            same_type += 1
        total += 1

    print(f"\n  Total: {total} hexagrams")
    print(f"  Same 化爻 type (世 and 應): {same_type}/{total} ({same_type/total:.1%})")

    print(f"\n  世 化爻 type distribution:")
    shi_types = Counter()
    for (s, _), c in type_pairs.items():
        shi_types[s] += c
    for t, c in shi_types.most_common():
        print(f"    {t}: {c}")

    print(f"\n  應 化爻 type distribution:")
    ying_types = Counter()
    for (_, y), c in type_pairs.items():
        ying_types[y] += c
    for t, c in ying_types.most_common():
        print(f"    {t}: {c}")

    print(f"\n  Most common (世, 應) pairs:")
    for (s, y), c in type_pairs.most_common(10):
        print(f"    ({s}, {y}): {c}")


def analyze_two_line_patterns(profiles):
    """2-moving-line patterns: reachability and basin crossing."""
    print("\n" + "=" * 60)
    print("§IV.2.2: 2-LINE TRANSFORMATIONS")
    print("=" * 60)

    _, hex_info = p2.generate_palaces()

    total_pairs = 0
    basin_crosses = 0
    palace_changes = 0
    reachable_per_hex = []

    for p in profiles:
        h = p["hex_val"]
        reachable = set()
        for i, j in combinations(range(6), 2):
            mask = (1 << i) | (1 << j)
            biangua = h ^ mask
            reachable.add(biangua)

            if basin_fn(biangua) != basin_fn(h):
                basin_crosses += 1
            if hex_info[biangua]["palace"] != p["palace"]:
                palace_changes += 1
            total_pairs += 1

        reachable_per_hex.append(len(reachable))

    print(f"\n  Total 2-line pairs: {total_pairs} (64 × C(6,2) = 64 × 15 = {64*15})")
    print(f"\n  Reachable 變卦 per hexagram:")
    reach_dist = Counter(reachable_per_hex)
    for n in sorted(reach_dist):
        print(f"    {n} distinct: {reach_dist[n]} hexagrams")
    avg_reach = sum(reachable_per_hex) / 64
    print(f"    Average: {avg_reach:.1f}")

    print(f"\n  Basin crossing: {basin_crosses}/{total_pairs} ({basin_crosses/total_pairs:.1%})")
    print(f"    (cf. 1-line: 33.3%)")

    # Basin crossing by line pair
    print(f"\n  Basin crossing by line pair:")
    for i, j in combinations(range(6), 2):
        mask = (1 << i) | (1 << j)
        n_cross = sum(1 for h in range(NUM_HEX) if basin_fn(h ^ mask) != basin_fn(h))
        print(f"    L{i+1}-L{j+1}: {n_cross}/64 ({n_cross/64:.0%})")

    print(f"\n  Palace change: {palace_changes}/{total_pairs} ({palace_changes/total_pairs:.1%})")
    print(f"    (cf. 1-line: 66.7%)")


def analyze_jinggua(profiles):
    """靜卦 reading: information available when no lines move."""
    print("\n" + "=" * 60)
    print("§IV.2.3: 靜卦 (NO MOVING LINES)")
    print("=" * 60)

    # When no lines move, the reading uses:
    # - 世 line's 六親 + element
    # - 應 line's 六親 + element
    # - 日辰 interactions (external, variable)
    # - Seasonal strength (external, variable)
    # Static info available from the hexagram itself:

    shi_pairs = Counter()
    ying_pairs = Counter()
    for p in profiles:
        shi_l = p["lines"][p["shi_line"] - 1]
        ying_l = p["lines"][p["ying_line"] - 1]
        shi_pairs[(shi_l["liuqin"], shi_l["element"])] += 1
        ying_pairs[(ying_l["liuqin"], ying_l["element"])] += 1

    print(f"\n  Distinct (世 六親, 世 element) pairs: {len(shi_pairs)}")
    print(f"  Distribution:")
    for (lq, elem), c in shi_pairs.most_common():
        print(f"    {lq} {elem}: {c} hexagrams")

    print(f"\n  Distinct (應 六親, 應 element) pairs: {len(ying_pairs)}")
    for (lq, elem), c in ying_pairs.most_common(10):
        print(f"    {lq} {elem}: {c}")

    # Combined static signature
    static_sigs = Counter()
    for p in profiles:
        shi_l = p["lines"][p["shi_line"] - 1]
        ying_l = p["lines"][p["ying_line"] - 1]
        sig = (shi_l["liuqin"], shi_l["element"],
               ying_l["liuqin"], ying_l["element"])
        static_sigs[sig] += 1

    print(f"\n  Distinct (世, 應) combined signatures: {len(static_sigs)}/64")
    print(f"  → {len(static_sigs)/64:.0%} of hexagrams have unique static reading identity")

    # How much external context adds
    # 5 seasons × 12 日辰 = 60 external contexts
    # × distinct internal sigs = total reading space
    print(f"\n  Static reading space:")
    print(f"    Internal signatures: {len(static_sigs)}")
    print(f"    × 5 seasons × 12 日辰 = {len(static_sigs) * 60} total contexts")
    print(f"    (but 64 × 60 = {64*60} is the max possible)")


# ═══════════════════════════════════════════════════════════════════════════
# §IV.3: Source text transformation patterns
# ═══════════════════════════════════════════════════════════════════════════

# Named patterns extracted from huozhulin.md lines 256–317
NAMED_PATTERNS = [
    {
        "section": "子孫獨發",
        "pattern_type": "子孫 moves",
        "description": "退散之神。利脫事、散事。旺相可求財。子孫為福德、醫藥、九流。",
        "favorable": "旺相 → can seek wealth; 出現 → check 變爻",
        "unfavorable": "官用時不利 (子孫傷官)",
        "huayao_relevant": ["孫化兄", "孫化孫", "孫化父", "孫化財", "孫化鬼"],
    },
    {
        "section": "兄弟獨發",
        "pattern_type": "兄弟 moves",
        "description": "劫財之神。虛詐不實。旺相主口舌破財。",
        "favorable": "—",
        "unfavorable": "化鬼爻凶; 隱伏發動大忌; 旺相主口舌憂疑破財",
        "huayao_relevant": ["兄化兄", "兄化孫", "兄化父", "兄化財", "兄化鬼"],
    },
    {
        "section": "父母獨發",
        "pattern_type": "父母 moves",
        "description": "重迭之神。大忌出現發動。旺相利文書、名缺、契約。",
        "favorable": "旺相 → 文書可成; 趲補名缺、求書札取契",
        "unfavorable": "休囚不可憑; 重迭艱辛 (父母有兩重)",
        "huayao_relevant": ["父化兄", "父化孫", "父化父", "父化財", "父化鬼"],
    },
    {
        "section": "官鬼獨發",
        "pattern_type": "官鬼 moves",
        "description": "臨吉神功名可望。臨囚神主興訟、賊盜、害人之事。",
        "favorable": "臨吉神 → 功名清高",
        "unfavorable": "臨囚神 → 訟、盜、鬼魅",
        "huayao_relevant": ["鬼化兄", "鬼化孫", "鬼化父", "鬼化財", "鬼化鬼"],
    },
    {
        "section": "妻財獨發",
        "pattern_type": "妻財 moves",
        "description": "生鬼傷父。問病難瘳，占親無路。財動克父、生鬼。",
        "favorable": "占脫貨要財爻發動; 財鬼俱動 → 父有元神,文書有成",
        "unfavorable": "占婚姻財動克翁姑; 占訟克文書; 宜旺不宜空,宜靜不宜動",
        "huayao_relevant": ["財化兄", "財化孫", "財化父", "財化財", "財化鬼"],
    },
]

# Specific 化爻 patterns from 兄弟獨發 section
SPECIFIC_HUAYAO = [
    {
        "type": "兄化鬼",
        "source_section": "兄弟獨發",
        "text_note": "大怕化鬼爻，凶",
        "interpretation": "兄弟 transforms into 官鬼 — worst outcome, deception becomes harm",
    },
    {
        "type": "財化鬼",
        "source_section": "implied from 妻財獨發",
        "text_note": "財動生鬼 — wealth activates authority/threat",
        "interpretation": "妻財 transforms into 官鬼 — wealth becomes its own threat",
    },
]


def analyze_source_patterns(dongyao):
    """Cross-reference source text patterns with computed frequencies."""
    print("\n" + "=" * 60)
    print("§IV.3: SOURCE TEXT TRANSFORMATION PATTERNS")
    print("=" * 60)

    type_freq = Counter(e["huayao_type"] for e in dongyao)
    total = len(dongyao)

    # Which 六親 type moves most often?
    by_old = defaultdict(list)
    for e in dongyao:
        by_old[e["old_liuqin"]].append(e)

    print(f"\n  六親 as moving line:")
    for lq in LIUQIN_NAMES:
        n = len(by_old[lq])
        print(f"    {lq}: {n}/384 ({n/384:.1%})")

    # Named patterns from source text
    print(f"\n  Named patterns from source text:")
    print(f"  {'Section':12s} {'Freq':>6} {'Rate':>6}  Key rule")
    print(f"  {'─'*12} {'─'*6} {'─'*6}  {'─'*40}")
    for pat in NAMED_PATTERNS:
        relevant_count = sum(type_freq.get(t, 0) for t in pat["huayao_relevant"])
        rate = relevant_count / total
        print(f"  {pat['section']:10s} {relevant_count:>6} {rate:>5.1%}  {pat['description'][:50]}")

    # Full 5×5 matrix with frequency classification
    print(f"\n  化爻 type rarity classification:")
    shorts = ["兄", "孫", "父", "財", "鬼"]
    thresholds = {"rare": 10, "moderate": 20, "common": 384}

    print(f"\n  {'Type':>6} {'Freq':>5} {'Rate':>6} {'Rarity':>10}  Source note")
    print(f"  {'─'*6} {'─'*5} {'─'*6} {'─'*10}  {'─'*30}")
    for old_s in shorts:
        for new_s in shorts:
            key = f"{old_s}化{new_s}"
            freq = type_freq.get(key, 0)
            rate = freq / total
            if freq < 10:
                rarity = "rare"
            elif freq < 20:
                rarity = "moderate"
            else:
                rarity = "common"

            # Find source note
            note = ""
            for sp in SPECIFIC_HUAYAO:
                if sp["type"] == key:
                    note = sp["text_note"]
            print(f"  {key:>6} {freq:>5} {rate:>5.1%} {rarity:>10}  {note}")

    # Specific callouts
    print(f"\n  Specific callouts from source text:")
    for sp in SPECIFIC_HUAYAO:
        freq = type_freq.get(sp["type"], 0)
        print(f"    {sp['type']}: {freq}/384 ({freq/384:.1%}) — {sp['text_note']}")
        print(f"      → {sp['interpretation']}")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    profiles = load_profiles()
    dongyao = load_dongyao()
    print(f"Loaded {len(profiles)} profiles, {len(dongyao)} dongyao entries\n")

    # §IV.2
    analyze_shi_ying_both_moving(profiles, dongyao)
    analyze_two_line_patterns(profiles)
    analyze_jinggua(profiles)

    # §IV.3
    analyze_source_patterns(dongyao)


if __name__ == "__main__":
    main()
