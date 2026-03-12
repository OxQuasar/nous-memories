#!/usr/bin/env python3
"""
§III.1-3: 日辰 interaction map, 旬空 model, 六神 rotation.

Loads hzl_profiles.json. Computes:
  1. 日辰 interactions (64 × 12 = 768 states): 生/克/被生/被克/沖/合/墓
  2. 旬空 (64 × 6 = 384 states): which lines are void per 旬
  3. 六神 rotation (6 patterns): spirit assignment per day-stem

Outputs hzl_richen.json.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

HERE = Path(__file__).resolve().parent

# ─── Constants ─────────────────────────────────────────────────────────────

BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_IDX = {b: i for i, b in enumerate(BRANCHES)}
BRANCH_ELEMENT = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood",
    "辰": "Earth", "巳": "Fire",  "午": "Fire",  "未": "Earth",
    "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
SHENG_MAP = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
             "Metal": "Water", "Water": "Wood"}
KE_MAP = {"Wood": "Earth", "Earth": "Water", "Water": "Fire",
          "Fire": "Metal", "Metal": "Wood"}

LIUQIN_NAMES = ["兄弟", "子孫", "父母", "妻財", "官鬼"]
LIUQIN_SHORT = {"兄弟": "兄", "子孫": "孫", "父母": "父", "妻財": "財", "官鬼": "鬼"}

# 六沖: opposite branches (distance 6)
CHONG = {}
for i in range(6):
    CHONG[i] = i + 6
    CHONG[i + 6] = i

# 六合: harmony pairs
HE = {0: 1, 1: 0, 2: 11, 11: 2, 3: 10, 10: 3, 4: 9, 9: 4, 5: 8, 8: 5, 6: 7, 7: 6}

# 墓: element → graveyard branch index
MU_BRANCH = {"Fire": 10, "Water": 4, "Wood": 7, "Metal": 1, "Earth": 4}

# ─── 旬空 ─────────────────────────────────────────────────────────────────

XUN_NAMES = ["甲子", "甲戌", "甲申", "甲午", "甲辰", "甲寅"]
XUN_STARTS = [0, 10, 20, 30, 40, 50]  # jiazi ordinal
# Each 旬 covers 10 consecutive 甲子 positions → 10 branches.
# The 2 branches NOT covered:
XUN_KONG = {
    0:  (10, 11),  # 甲子旬: 戌亥空
    10: (8, 9),    # 甲戌旬: 申酉空
    20: (6, 7),    # 甲申旬: 午未空
    30: (4, 5),    # 甲午旬: 辰巳空
    40: (2, 3),    # 甲辰旬: 寅卯空
    50: (0, 1),    # 甲寅旬: 子丑空
}

# ─── 六神 ─────────────────────────────────────────────────────────────────

LIUSHEN = ["青龍", "朱雀", "勾陳", "螣蛇", "白虎", "玄武"]
LIUSHEN_START = {
    "甲": 0, "乙": 0,
    "丙": 1, "丁": 1,
    "戊": 2,
    "己": 3,
    "庚": 4, "辛": 4,
    "壬": 5, "癸": 5,
}
STEM_GROUPS = [
    ("甲乙", 0), ("丙丁", 1), ("戊", 2),
    ("己", 3), ("庚辛", 4), ("壬癸", 5),
]


# ─── Load ─────────────────────────────────────────────────────────────────

def load_profiles():
    return json.loads((HERE / "hzl_profiles.json").read_text())


# ═══════════════════════════════════════════════════════════════════════════
# §III.1: 日辰 interaction map
# ═══════════════════════════════════════════════════════════════════════════

RICHEN_INTERACTIONS = ["生", "克", "被生", "被克", "沖", "合", "墓"]

def compute_richen(profiles):
    """Compute 日辰 interactions for 64 × 12 states."""
    entries = []
    for p in profiles:
        for ri in range(12):
            rb = BRANCHES[ri]
            re = BRANCH_ELEMENT[rb]

            line_interactions = []
            active_lines = {k: [] for k in RICHEN_INTERACTIONS}

            for l in p["lines"]:
                pos = l["position"]
                li = BRANCH_IDX[l["branch"]]
                le = l["element"]
                ixns = []

                # Element-level: 日辰 → line
                if SHENG_MAP[re] == le:
                    ixns.append("生")
                if KE_MAP[re] == le:
                    ixns.append("克")
                # Reverse
                if SHENG_MAP[le] == re:
                    ixns.append("被生")
                if KE_MAP[le] == re:
                    ixns.append("被克")
                # Branch-level
                if CHONG.get(ri) == li:
                    ixns.append("沖")
                if HE.get(ri) == li:
                    ixns.append("合")
                # 墓: line's element's graveyard = 日辰 branch
                if MU_BRANCH[le] == ri:
                    ixns.append("墓")

                line_interactions.append({
                    "position": pos,
                    "interactions": ixns,
                })
                for ix in ixns:
                    active_lines[ix].append(pos)

            activation_count = sum(1 for li in line_interactions if li["interactions"])

            entries.append({
                "hex_val": p["hex_val"],
                "richen_branch_idx": ri,
                "richen_branch": rb,
                "richen_element": re,
                "line_interactions": line_interactions,
                "active_lines": active_lines,
                "activation_count": activation_count,
            })
    return entries


def analyze_richen(entries):
    """Print 日辰 interaction analysis."""
    print("=" * 60)
    print("§III.1: 日辰 INTERACTION MAP")
    print("=" * 60)

    total = len(entries)
    print(f"\n  Total states: {total} (64 hex × 12 branches)")

    # Activation density
    act_dist = Counter(e["activation_count"] for e in entries)
    avg_act = sum(e["activation_count"] for e in entries) / total
    print(f"\n  Lines activated (≥1 interaction) per state:")
    print(f"    Mean: {avg_act:.2f}/6")
    for n in sorted(act_dist):
        pct = act_dist[n] / total
        bar = "█" * int(pct * 40)
        print(f"    {n}/6: {act_dist[n]:>3} ({pct:>5.1%}) {bar}")

    # Per-interaction frequency
    print(f"\n  Interaction frequency:")
    for ix in RICHEN_INTERACTIONS:
        total_hits = sum(len(e["active_lines"][ix]) for e in entries)
        states_with = sum(1 for e in entries if e["active_lines"][ix])
        avg = total_hits / total
        print(f"    {ix:>4}: {total_hits:>4} hits across {states_with:>3} states "
              f"(avg {avg:.2f}/state)")

    # 沖 distribution per hexagram (across 12 日辰)
    hex_chong = defaultdict(int)
    for e in entries:
        hex_chong[e["hex_val"]] += len(e["active_lines"]["沖"])
    chong_dist = Counter(hex_chong.values())
    print(f"\n  沖 total per hexagram (across 12 日辰):")
    for n in sorted(chong_dist):
        print(f"    {n}: {chong_dist[n]} hexagrams")

    # 合 distribution per hexagram
    hex_he = defaultdict(int)
    for e in entries:
        hex_he[e["hex_val"]] += len(e["active_lines"]["合"])
    he_dist = Counter(hex_he.values())
    print(f"\n  合 total per hexagram (across 12 日辰):")
    for n in sorted(he_dist):
        print(f"    {n}: {he_dist[n]} hexagrams")

    # Unique activation patterns per hexagram
    hex_patterns = defaultdict(set)
    for e in entries:
        # Pattern = tuple of (pos, sorted interactions) for all lines
        pattern = tuple(
            (li["position"], tuple(sorted(li["interactions"])))
            for li in e["line_interactions"]
        )
        hex_patterns[e["hex_val"]].add(pattern)

    pattern_counts = Counter(len(v) for v in hex_patterns.values())
    print(f"\n  Unique activation patterns per hexagram (over 12 日辰):")
    for n in sorted(pattern_counts):
        print(f"    {n} patterns: {pattern_counts[n]} hexagrams")
    avg_patterns = sum(len(v) for v in hex_patterns.values()) / 64
    print(f"    Average: {avg_patterns:.1f} unique patterns per hexagram")

    return entries


# ═══════════════════════════════════════════════════════════════════════════
# §III.2: 旬空
# ═══════════════════════════════════════════════════════════════════════════

def compute_xunkong(profiles):
    """Compute 旬空 for 64 × 6 states."""
    entries = []
    for p in profiles:
        branches = [BRANCH_IDX[l["branch"]] for l in p["lines"]]
        liuqin = [l["liuqin"] for l in p["lines"]]

        for xun_start, xun_name in zip(XUN_STARTS, XUN_NAMES):
            kong_bi = XUN_KONG[xun_start]
            kong_branches = [BRANCHES[bi] for bi in kong_bi]

            kong_lines = []
            kong_liuqin = []
            for pos in range(6):
                if branches[pos] in kong_bi:
                    kong_lines.append(pos + 1)
                    kong_liuqin.append(liuqin[pos])

            entries.append({
                "hex_val": p["hex_val"],
                "xun_name": xun_name,
                "kong_branches": kong_branches,
                "kong_lines": kong_lines,
                "kong_liuqin": kong_liuqin,
            })
    return entries


def analyze_xunkong(xk_entries, profiles):
    """Print 旬空 analysis."""
    print("\n" + "=" * 60)
    print("§III.2: 旬空 MODEL")
    print("=" * 60)

    total = len(xk_entries)
    print(f"\n  Total states: {total} (64 hex × 6 旬)")

    # Void count distribution
    void_dist = Counter(len(e["kong_lines"]) for e in xk_entries)
    avg_void = sum(len(e["kong_lines"]) for e in xk_entries) / total
    print(f"\n  Void lines per state:")
    print(f"    Mean: {avg_void:.2f}")
    for n in sorted(void_dist):
        pct = void_dist[n] / total
        print(f"    {n} void: {void_dist[n]:>3} ({pct:>5.1%})")

    # Per-hexagram: total void across 6 旬
    hex_void = defaultdict(int)
    for e in xk_entries:
        hex_void[e["hex_val"]] += len(e["kong_lines"])
    per_hex_dist = Counter(hex_void.values())
    avg_per_hex = sum(hex_void.values()) / 64
    print(f"\n  Total void-line instances per hexagram (across 6 旬):")
    print(f"    Mean: {avg_per_hex:.2f}")
    for n in sorted(per_hex_dist):
        print(f"    {n}: {per_hex_dist[n]} hexagrams")

    # Void by palace
    by_palace = defaultdict(list)
    for p in profiles:
        by_palace[p["palace"]].append(p["hex_val"])

    print(f"\n  Average void-lines per state by palace:")
    for pal in sorted(by_palace):
        hex_vals = set(by_palace[pal])
        states = [e for e in xk_entries if e["hex_val"] in hex_vals]
        avg = sum(len(e["kong_lines"]) for e in states) / len(states)
        print(f"    {pal:10s}: {avg:.2f}")

    # Which 六親 types are voided most?
    lq_void = Counter()
    for e in xk_entries:
        for lq in e["kong_liuqin"]:
            lq_void[lq] += 1
    total_void = sum(lq_void.values())
    print(f"\n  Voided 六親 frequency (total {total_void} void-instances):")
    for lq in LIUQIN_NAMES:
        cnt = lq_void.get(lq, 0)
        print(f"    {lq}: {cnt} ({cnt/total_void:.1%})")

    # 世 line void frequency
    shi_void = 0
    ying_void = 0
    for p in profiles:
        hex_xks = [e for e in xk_entries if e["hex_val"] == p["hex_val"]]
        for e in hex_xks:
            if p["shi_line"] in e["kong_lines"]:
                shi_void += 1
            if p["ying_line"] in e["kong_lines"]:
                ying_void += 1
    print(f"\n  世 voided: {shi_void}/{total} ({shi_void/total:.1%})")
    print(f"  應 voided: {ying_void}/{total} ({ying_void/total:.1%})")

    return xk_entries


# ═══════════════════════════════════════════════════════════════════════════
# §III.3: 六神 rotation
# ═══════════════════════════════════════════════════════════════════════════

def compute_liushen():
    """Build 6 六神 rotation patterns."""
    patterns = []
    for group_name, start in STEM_GROUPS:
        assignment = [LIUSHEN[(start + i) % 6] for i in range(6)]
        patterns.append({
            "stem_group": group_name,
            "start_spirit": LIUSHEN[start],
            "assignment": assignment,
        })
    return patterns


def analyze_liushen(patterns):
    """Print 六神 analysis."""
    print("\n" + "=" * 60)
    print("§III.3: 六神 ROTATION")
    print("=" * 60)

    print(f"\n  6 rotation patterns:")
    header = f"  {'Stems':>5}  " + "  ".join(f"L{i+1}" for i in range(6))
    print(header)
    print(f"  {'─'*5}  " + "  ".join("──" for _ in range(6)))
    for p in patterns:
        row = "  ".join(f"{s[:2]:>2}" for s in p["assignment"])
        print(f"  {p['stem_group']:>5}  {row}")

    # Cross-tab: which spirit appears at which position?
    print(f"\n  Spirit × position (count across 6 patterns):")
    pos_spirit = defaultdict(Counter)
    for p in patterns:
        for i, spirit in enumerate(p["assignment"]):
            pos_spirit[i + 1][spirit] += 1

    header = f"  {'Spirit':>4}  " + "  ".join(f"L{i+1}" for i in range(6)) + "  Total"
    print(header)
    print(f"  {'─'*4}  " + "  ".join("──" for _ in range(6)) + "  ─────")
    for spirit in LIUSHEN:
        cells = [pos_spirit[i + 1].get(spirit, 0) for i in range(6)]
        print(f"  {spirit[:2]:>4}  " + "  ".join(f"{c:>2}" for c in cells) +
              f"  {sum(cells):>5}")

    # Each spirit appears exactly once at each position across all 6 patterns
    uniform = all(
        pos_spirit[i + 1][spirit] == 1
        for i in range(6) for spirit in LIUSHEN
    )
    print(f"\n  Each spirit at each position exactly once: {'✓' if uniform else '✗'}")
    print(f"  → 六神 is a Latin square (6 rotations of a 6-element cycle)")

    return patterns


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    profiles = load_profiles()
    print(f"Loaded {len(profiles)} profiles\n")

    # §III.1
    richen = compute_richen(profiles)
    richen = analyze_richen(richen)

    # §III.2
    xunkong = compute_xunkong(profiles)
    xunkong = analyze_xunkong(xunkong, profiles)

    # §III.3
    liushen = compute_liushen()
    liushen = analyze_liushen(liushen)

    # Write output
    output = {
        "richen_interactions": richen,
        "xunkong": xunkong,
        "liushen_patterns": liushen,
    }
    out_path = HERE / "hzl_richen.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote to {out_path}")
    print(f"   richen: {len(richen)} entries")
    print(f"   xunkong: {len(xunkong)} entries")
    print(f"   liushen: {len(liushen)} patterns")


if __name__ == "__main__":
    main()
