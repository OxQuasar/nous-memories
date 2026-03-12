#!/usr/bin/env python3
"""
§V.4-5: Interaction graph (sampled) + 8 axes / 8 primitives formalization.

Selects 8 representative hexagrams (1 per palace root). For each, computes
a full interaction snapshot at Spring/子/L1-moving. Also documents the
8 evaluation axes and 8 operational primitives.

Outputs hzl_network.json.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

HERE = Path(__file__).resolve().parent

LIUQIN_NAMES = ["兄弟", "子孫", "父母", "妻財", "官鬼"]
LIUQIN_SHORT = {"兄弟": "兄", "子孫": "孫", "父母": "父", "妻財": "財", "官鬼": "鬼"}
ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 8 palace roots
SAMPLE_HEXES = [0, 1, 9, 18, 36, 45, 54, 63]

SEASON = "Spring"
RICHEN_IDX = 0  # 子
MOVING_LINE = 1


def load_all():
    profiles = json.loads((HERE / "hzl_profiles.json").read_text())
    seasonal = json.loads((HERE / "hzl_seasonal.json").read_text())
    richen = json.loads((HERE / "hzl_richen.json").read_text())
    dongyao = json.loads((HERE / "hzl_dongyao.json").read_text())
    topology = json.loads((HERE / "hzl_topology.json").read_text())
    return profiles, seasonal, richen, dongyao, topology


# ═══════════════════════════════════════════════════════════════════════════
# §V.4: Interaction graph snapshots
# ═══════════════════════════════════════════════════════════════════════════

def compute_snapshot(h, profiles, seasonal, richen, dongyao, topology):
    """Compute full interaction snapshot for one hexagram."""
    prof = next(p for p in profiles if p["hex_val"] == h)
    seas = next(s for s in seasonal if s["hex_val"] == h and s["season"] == SEASON)
    ri_all = richen["richen_interactions"]
    rich = next(r for r in ri_all if r["hex_val"] == h and r["richen_branch_idx"] == RICHEN_IDX)
    dy = next(d for d in dongyao if d["hex_val"] == h and d["moving_line"] == MOVING_LINE)
    topo = next(t for t in topology if t["hex_val"] == h)

    return {
        "hex_val": h,
        "name": prof["name"],
        "palace": prof["palace"],
        "palace_element": prof["palace_element"],
        "rank": prof["rank_name"],
        "shi_line": prof["shi_line"],
        "ying_line": prof["ying_line"],
        "guashen_line": prof["guashen_line"],
        "missing_liuqin": prof["missing_liuqin"],
        "lines": [{
            "pos": l["position"],
            "branch": l["branch"],
            "element": l["element"],
            "liuqin": l["liuqin"],
            "strength": seas["line_strengths"][l["position"] - 1],
            "richen_interactions": rich["line_interactions"][l["position"] - 1]["interactions"],
            "is_shi": l["position"] == prof["shi_line"],
            "is_ying": l["position"] == prof["ying_line"],
        } for l in prof["lines"]],
        "season": SEASON,
        "season_element": "Wood",
        "richen_branch": BRANCHES[RICHEN_IDX],
        "richen_element": "Water",
        "dongyao": {
            "moving_line": MOVING_LINE,
            "old": f"{dy['old_branch']}({dy['old_element']}) {dy['old_liuqin']}",
            "new": f"{dy['new_branch']}({dy['new_element']}) {dy['new_liuqin']}",
            "type": dy["huayao_type"],
        },
        "topology": topo["topology"],
        "liuqin_strengths": seas["liuqin_strengths"],
        "strong_liuqin": seas["strong_liuqin"],
        "functional_coverage": seas["functional_coverage"],
    }


def print_snapshot(snap):
    """Print readable interaction snapshot."""
    print(f"\n  ╔══ {snap['name']} (hex={snap['hex_val']}) ══╗")
    print(f"  ║ Palace: {snap['palace']} ({snap['palace_element']}), {snap['rank']}")
    print(f"  ║ 世=L{snap['shi_line']}, 應=L{snap['ying_line']}, "
          f"卦身={'L'+str(snap['guashen_line']) if snap['guashen_line'] else 'off'}")
    if snap['missing_liuqin']:
        print(f"  ║ Missing: {', '.join(snap['missing_liuqin'])}")

    print(f"  ╠── Season: {snap['season']} ({snap['season_element']})")
    print(f"  ╠── 日辰: {snap['richen_branch']} ({snap['richen_element']})")
    print(f"  ╠── 動爻: L{snap['dongyao']['moving_line']}")

    # Lines table
    print(f"  ╠── Lines:")
    print(f"  ║  {'Pos':>3} {'Branch':>4} {'Elem':>5} {'六親':>4} {'Str':>3} {'日辰':>10} {'Mark':>6}")
    print(f"  ║  {'─'*3} {'─'*4} {'─'*5} {'─'*4} {'─'*3} {'─'*10} {'─'*6}")
    for l in snap["lines"]:
        mark = ""
        if l["is_shi"]: mark += "世"
        if l["is_ying"]: mark += "應"
        if l["pos"] == MOVING_LINE: mark += "動"
        ri_str = ",".join(l["richen_interactions"]) if l["richen_interactions"] else "—"
        print(f"  ║  L{l['pos']:1d}  {l['branch']:>2}   {l['element']:>5} "
              f"{LIUQIN_SHORT[l['liuqin']]:>2}  {l['strength']:>2} {ri_str:>10} {mark:>6}")

    # Transformation
    dy = snap["dongyao"]
    print(f"  ╠── 動爻 L{dy['moving_line']}: {dy['old']} → {dy['new']} ({dy['type']})")

    # Static topology
    print(f"  ╠── Static topology:")
    for prim, edges in snap["topology"].items():
        if edges:
            edge_str = ", ".join(f"L{a}→L{b}" if prim in ("生","克","墓") else f"L{a}↔L{b}"
                                 for a, b in edges)
            print(f"  ║    {prim}: {edge_str}")

    # 六親 strengths
    print(f"  ╠── 六親 strengths:")
    for lq in LIUQIN_NAMES:
        s = snap["liuqin_strengths"][lq]
        marker = " ★" if s in ("旺", "相") else ""
        print(f"  ║    {lq}: {s}{marker}")

    # 用神 evaluation for 占求財 (用神=妻財)
    print(f"  ╠── 用神 evaluation (占求財, 用神=妻財):")
    wc_lines = [l for l in snap["lines"] if l["liuqin"] == "妻財"]
    if wc_lines:
        positions = ", ".join(f"L{l['pos']}" for l in wc_lines)
        print(f"  ║    Position: {positions}")
        for l in wc_lines:
            ris = l["richen_interactions"]
            ri_txt = ", ".join(ris) if ris else "none"
            print(f"  ║    L{l['pos']}: strength={l['strength']}, 日辰={ri_txt}")
    else:
        print(f"  ║    HIDDEN (missing from hexagram)")
    wc_str = snap["liuqin_strengths"]["妻財"]
    favorable = wc_str in ("旺", "相")
    print(f"  ║    Overall: {wc_str} → {'Favorable' if favorable else 'Unfavorable'}")
    print(f"  ╚══{'═'*40}")


def analyze_density(snapshots):
    """Graph density stats across all 8 snapshots."""
    print(f"\n  {'─'*60}")
    print(f"  GRAPH DENSITY STATS (across {len(snapshots)} snapshots)")
    print(f"  {'─'*60}")

    for prim in ["沖", "合", "刑", "害", "墓", "生", "克"]:
        counts = [len(s["topology"][prim]) for s in snapshots]
        avg = sum(counts) / len(counts)
        print(f"    {prim}: avg={avg:.1f}, range=[{min(counts)}, {max(counts)}]")

    # Total edges
    totals = [sum(len(s["topology"][p]) for p in s["topology"]) for s in snapshots]
    print(f"    Total: avg={sum(totals)/len(totals):.1f}, range=[{min(totals)}, {max(totals)}]")

    # 日辰 activation
    act_counts = [sum(1 for l in s["lines"] if l["richen_interactions"]) for s in snapshots]
    print(f"    日辰 active lines: avg={sum(act_counts)/len(act_counts):.1f}")

    # Functional coverage
    fc = [s["functional_coverage"] for s in snapshots]
    print(f"    Functional coverage: avg={sum(fc)/len(fc):.1f}")


# ═══════════════════════════════════════════════════════════════════════════
# §V.5: 8 axes + 8 primitives formalization
# ═══════════════════════════════════════════════════════════════════════════

EIGHT_AXES = [
    {
        "axis": "世",
        "chinese_source": "世爻乃我家情由",
        "description": "The querent's position — which line represents 'self'",
        "data_source": "hzl_profiles.json → shi_line",
        "evaluation": "What 六親 sits at 世? Is it the 用神? Strength? 日辰 interaction?",
        "interactions_with": ["應 (世應 生克)", "日辰 (日辰 acts on 世 line)", "動 (世 line moving?)"],
    },
    {
        "axis": "應",
        "chinese_source": "應爻為彼之事理",
        "description": "The other party / external situation",
        "data_source": "hzl_profiles.json → ying_line",
        "evaluation": "What 六親 sits at 應? 應 vs 世 relationship? 應 動 or 靜?",
        "interactions_with": ["世 (世應 生克)", "日辰 (日辰 acts on 應 line)", "動 (應 line moving?)"],
    },
    {
        "axis": "日",
        "chinese_source": "日辰",
        "description": "The day branch — external temporal influence on all lines",
        "data_source": "hzl_richen.json → richen_interactions",
        "evaluation": "Which lines does 日辰 生/克/沖/合/墓? Does it support or attack 用神?",
        "interactions_with": ["每一爻 (all 6 lines)", "旬空 (determines void)", "六神 (day stem → rotation)"],
    },
    {
        "axis": "月",
        "chinese_source": "月建/季節",
        "description": "The month/season — determines 旺相休囚死 strength levels",
        "data_source": "hzl_seasonal.json",
        "evaluation": "旺相 = strong, 休 = neutral, 囚死 = weak. Determines base power of every element.",
        "interactions_with": ["每一爻 (strength of all lines)", "用神 (is 用神 strong this season?)"],
    },
    {
        "axis": "飛",
        "chinese_source": "出現旺相，為久為遠",
        "description": "Visible/flying lines — 六親 types present in the hexagram",
        "data_source": "hzl_profiles.json → lines[].liuqin",
        "evaluation": "Is the 用神 飛 (visible)? If so, which line(s)? Multiple = pick strongest.",
        "interactions_with": ["伏 (what's hidden behind each line)", "日辰 (fly or hide?)"],
    },
    {
        "axis": "伏",
        "chinese_source": "伏藏有氣，只利暫時",
        "description": "Hidden lines — missing 六親 types lurking under visible lines",
        "data_source": "hzl_profiles.json → feifu + missing_liuqin, hzl_feifu_diagnostic.json",
        "evaluation": "If 用神 is 伏, what does it hide under? Apply 9 diagnostic cases. "
                       "Can 日辰 bring it out (透出)?",
        "interactions_with": ["飛 (the covering line)", "日辰 (透出 condition)", "旬空 (void blocks emergence)"],
    },
    {
        "axis": "動",
        "chinese_source": "獨發易取，亂動難尋",
        "description": "Moving lines — which lines change, and what they transform into",
        "data_source": "hzl_dongyao.json, hzl_dufa.json",
        "evaluation": "獨發 = single mover, read that line. 亂動 = multiple, read the 旺 one. "
                       "化爻 type determines transformation outcome.",
        "interactions_with": ["靜 (non-moving lines receive effects)", "用神 (does 用神 move or stay?)"],
    },
    {
        "axis": "靜",
        "chinese_source": "財官喜靜",
        "description": "Static lines — stability, resistance to change",
        "data_source": "implicit (complement of 動)",
        "evaluation": "靜 lines receive effects from 動 lines. For 用神: 靜 + 旺相 = stable foundation. "
                       "In some domains (marriage, wealth): 用神 靜 is better than 動.",
        "interactions_with": ["動 (moving lines act on static)", "日辰 (can activate static lines via 沖)"],
    },
]

EIGHT_PRIMITIVES = [
    {
        "primitive": "克",
        "chinese": "克",
        "operates_between": ["line ↔ line (element)", "日辰 → line (element)"],
        "condition": "Standard 五行 克 cycle: Wood→Earth, Earth→Water, Water→Fire, Fire→Metal, Metal→Wood",
        "effect": "Overcomes, attacks, suppresses — destructive",
        "frequency": "6.25/hexagram (static topology); 1.2/state (日辰)",
    },
    {
        "primitive": "合",
        "chinese": "合",
        "operates_between": ["line ↔ line (branch)", "日辰 ↔ line (branch)"],
        "condition": "Six harmony pairs: 子丑, 寅亥, 卯戌, 辰酉, 巳申, 午未",
        "effect": "Combines, binds, stabilizes — can prevent action but also secure outcome",
        "frequency": "0.72/hexagram (static); 6/hexagram across 12 日辰 (uniform)",
    },
    {
        "primitive": "刑",
        "chinese": "刑",
        "operates_between": ["line ↔ line (branch)"],
        "condition": "Three-punishment groups: 子↔卯, 丑↔戌↔未, 寅↔巳↔申. Self-punish: 辰辰, 午午, 酉酉, 亥亥",
        "effect": "Punishes through friction — harm, conflict, legal trouble",
        "frequency": "0.53/hexagram (static topology)",
    },
    {
        "primitive": "害",
        "chinese": "害",
        "operates_between": ["line ↔ line (branch)"],
        "condition": "Six harm pairs: 子未, 丑午, 寅巳, 卯辰, 申亥, 酉戌",
        "effect": "Covert damage — hidden harm, undermining",
        "frequency": "0.81/hexagram (static topology)",
    },
    {
        "primitive": "墓",
        "chinese": "墓",
        "operates_between": ["line → line (element→branch)", "日辰 → line"],
        "condition": "Element graveyard: Fire→戌, Water→辰, Wood→未, Metal→丑, Earth→辰",
        "effect": "Entombed, trapped, stored — frozen, unable to act",
        "frequency": "2.75/hexagram (static); present in 94% of hexagrams",
    },
    {
        "primitive": "旺",
        "chinese": "旺",
        "operates_between": ["season → element"],
        "condition": "Element matches season: Wood=Spring, Fire=Summer, Earth=Late Summer, Metal=Autumn, Water=Winter. "
                     "相 = generated by season element.",
        "effect": "Maximum power — strong foundation, events come quickly",
        "frequency": "2 elements 旺/相 per season → 2.4 lines/hexagram on average",
    },
    {
        "primitive": "空",
        "chinese": "空",
        "operates_between": ["旬 → line (branch)"],
        "condition": "旬空: 2 branches absent from current 旬 of 60 甲子 cycle",
        "effect": "Void, unrealized, empty — 真空(+死) worst, 假空(+旺) temporary",
        "frequency": "1.0 void lines per hexagram-旬 (exact average)",
    },
    {
        "primitive": "沖",
        "chinese": "沖",
        "operates_between": ["line ↔ line (branch)", "日辰 ↔ line (branch)"],
        "condition": "Opposite branches (distance 6): 子↔午, 丑↔未, 寅↔申, 卯↔酉, 辰↔戌, 巳↔亥",
        "effect": "Clashes — disrupts, activates, breaks 合, wakes 空. Context-dependent valence.",
        "frequency": "0.50/hexagram (static); 6/hexagram across 12 日辰 (uniform)",
    },
]


def print_axes():
    """Print 8 axes and 8 primitives."""
    print("\n" + "=" * 60)
    print("§V.5: EIGHT EVALUATION AXES")
    print("=" * 60)

    for ax in EIGHT_AXES:
        print(f"\n  ┌ {ax['axis']} — {ax['description']}")
        print(f"  │ Source: {ax['chinese_source']}")
        print(f"  │ Data: {ax['data_source']}")
        print(f"  │ Eval: {ax['evaluation'][:75]}")
        print(f"  └ Interacts: {', '.join(ax['interactions_with'])}")

    print("\n" + "=" * 60)
    print("EIGHT OPERATIONAL PRIMITIVES")
    print("=" * 60)

    print(f"\n  {'Prim':>4} {'Operates between':30s} {'Freq':>12}")
    print(f"  {'─'*4} {'─'*30} {'─'*12}")
    for p in EIGHT_PRIMITIVES:
        ops = p['operates_between'][0][:30]
        print(f"  {p['primitive']:>2}   {ops:30s} {p['frequency'][:12]}")

    print(f"\n  Source: 克合刑害墓旺空沖 — 知此八宗，與神奧通")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    profiles, seasonal, richen, dongyao, topology = load_all()

    print("=" * 60)
    print("§V.4: INTERACTION GRAPH SNAPSHOTS")
    print("=" * 60)
    print(f"  Context: Season={SEASON}, 日辰={BRANCHES[RICHEN_IDX]}, 動爻=L{MOVING_LINE}")

    snapshots = []
    for h in SAMPLE_HEXES:
        snap = compute_snapshot(h, profiles, seasonal, richen, dongyao, topology)
        snapshots.append(snap)
        print_snapshot(snap)

    analyze_density(snapshots)
    print_axes()

    # Output
    output = {
        "snapshots": snapshots,
        "context": {
            "season": SEASON,
            "richen_branch": BRANCHES[RICHEN_IDX],
            "moving_line": MOVING_LINE,
        },
        "eight_axes": EIGHT_AXES,
        "eight_primitives": EIGHT_PRIMITIVES,
    }
    out_path = HERE / "hzl_network.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote to {out_path}")


if __name__ == "__main__":
    main()
