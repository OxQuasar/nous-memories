#!/usr/bin/env python3
"""
§I.3-4: Cross-tabulations + static interaction topology.

Loads hzl_profiles.json. Computes:
  1. 世/應 × 六親 cross-tab (per-palace breakdown)
  2. 飛伏 completeness by rank
  3. 納音 distribution across positions
  4. 卦身 distribution
  5. Static branch-level topology (沖/合/刑/害/墓/生/克)

Outputs hzl_topology.json with per-hexagram adjacency data.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

# ─── Constants ─────────────────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent

LIUQIN_NAMES = ["兄弟", "子孫", "父母", "妻財", "官鬼"]
LIUQIN_SHORT = {"兄弟": "兄", "子孫": "孫", "父母": "父", "妻財": "財", "官鬼": "鬼"}
RANK_NAMES = ["本宮", "一世", "二世", "三世", "四世", "五世", "游魂", "歸魂"]

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

# ─── Branch interaction tables ─────────────────────────────────────────────

# 六沖: opposite branches (index distance 6)
CHONG_PAIRS = {0: 6, 1: 7, 2: 8, 3: 9, 4: 10, 5: 11}
_CHONG_SET = set()
for a, b in CHONG_PAIRS.items():
    _CHONG_SET.add((min(a, b), max(a, b)))

# 六合: harmony pairs
HE_PAIRS = {0: 1, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7}
_HE_SET = set()
for a, b in HE_PAIRS.items():
    _HE_SET.add((min(a, b), max(a, b)))

# 三刑: punishment groups (mutual within group)
XING_GROUPS = [
    frozenset({0, 3}),         # 子↔卯
    frozenset({1, 10, 7}),     # 丑↔戌↔未
    frozenset({2, 5, 8}),      # 寅↔巳↔申
]
SELF_XING = {4, 6, 9, 11}     # 辰辰, 午午, 酉酉, 亥亥

# 六害: harm pairs
HAI_PAIRS = {0: 7, 1: 6, 2: 5, 3: 4, 8: 11, 9: 10}
_HAI_SET = set()
for a, b in HAI_PAIRS.items():
    _HAI_SET.add((min(a, b), max(a, b)))

# 墓: element → graveyard branch index
MU_BRANCH = {"Fire": 10, "Water": 4, "Wood": 7, "Metal": 1, "Earth": 4}


def is_chong(bi, bj):
    return (min(bi, bj), max(bi, bj)) in _CHONG_SET

def is_he(bi, bj):
    return (min(bi, bj), max(bi, bj)) in _HE_SET

def is_xing(bi, bj):
    for g in XING_GROUPS:
        if bi in g and bj in g and bi != bj:
            return True
    return False

def is_hai(bi, bj):
    return (min(bi, bj), max(bi, bj)) in _HAI_SET

def five_phase_rel(src, tgt):
    """Return 生/克/被生/被克/比和."""
    if src == tgt: return "比和"
    if SHENG_MAP[src] == tgt: return "生"
    if KE_MAP[src] == tgt: return "克"
    if SHENG_MAP[tgt] == src: return "被生"
    if KE_MAP[tgt] == src: return "被克"
    return None


# ─── Load data ─────────────────────────────────────────────────────────────

def load_profiles():
    return json.loads((HERE / "hzl_profiles.json").read_text())


# ═══════════════════════════════════════════════════════════════════════════
# §I.3 Cross-tabulations
# ═══════════════════════════════════════════════════════════════════════════

def cross_tab_shi_ying_liuqin(profiles):
    """世/應 × 六親 cross-tab."""
    print("=" * 60)
    print("世/應 × 六親 CROSS-TAB")
    print("=" * 60)

    shi_lq = Counter()
    ying_lq = Counter()
    # Per-palace
    palace_shi = defaultdict(Counter)
    palace_ying = defaultdict(Counter)

    for p in profiles:
        shi = p["shi_line"] - 1  # 0-indexed
        ying = p["ying_line"] - 1
        sl = p["lines"][shi]["liuqin"]
        yl = p["lines"][ying]["liuqin"]
        shi_lq[sl] += 1
        ying_lq[yl] += 1
        palace_shi[p["palace"]][sl] += 1
        palace_ying[p["palace"]][yl] += 1

    print(f"\n  {'六親':>6}  世   應")
    print(f"  {'─'*6}──────────")
    for lq in LIUQIN_NAMES:
        print(f"  {lq:>4}   {shi_lq[lq]:>3}  {ying_lq[lq]:>3}")
    print(f"  {'Total':>6}  {sum(shi_lq.values()):>3}  {sum(ying_lq.values()):>3}")

    # Per-palace breakdown
    palaces = sorted(set(p["palace"] for p in profiles))
    print(f"\n  Per-palace 世 六親:")
    header = f"  {'Palace':10s} " + " ".join(f"{LIUQIN_SHORT[lq]:>3}" for lq in LIUQIN_NAMES)
    print(header)
    print(f"  {'─'*10} " + " ".join("───" for _ in LIUQIN_NAMES))
    for pal in palaces:
        row = " ".join(f"{palace_shi[pal][lq]:>3}" for lq in LIUQIN_NAMES)
        print(f"  {pal:10s} {row}")

    print(f"\n  Per-palace 應 六親:")
    print(header)
    print(f"  {'─'*10} " + " ".join("───" for _ in LIUQIN_NAMES))
    for pal in palaces:
        row = " ".join(f"{palace_ying[pal][lq]:>3}" for lq in LIUQIN_NAMES)
        print(f"  {pal:10s} {row}")

    return shi_lq, ying_lq


def feifu_completeness_by_rank(profiles):
    """飛伏 completeness by rank."""
    print("\n" + "=" * 60)
    print("飛伏 COMPLETENESS BY RANK")
    print("=" * 60)

    rank_complete = Counter()
    rank_total = Counter()
    palace_rank_complete = defaultdict(lambda: defaultdict(int))
    palace_rank_total = defaultdict(lambda: defaultdict(int))

    for p in profiles:
        rank = p["palace_rank"]
        vis = set(l["liuqin"] for l in p["lines"])
        hid = set(l["feifu_liuqin"] for l in p["lines"])
        complete = (vis | hid) == set(LIUQIN_NAMES)
        rank_total[rank] += 1
        palace_rank_total[p["palace"]][rank] += 1
        if complete:
            rank_complete[rank] += 1
            palace_rank_complete[p["palace"]][rank] += 1

    print(f"\n  {'Rank':6s}  Complete  Total  Rate")
    print(f"  {'─'*6}──{'─'*8}──{'─'*5}──{'─'*5}")
    for r in range(8):
        c = rank_complete[r]
        t = rank_total[r]
        pct = f"{c/t:.0%}" if t else "—"
        marker = " ← all 8!" if c == 8 else ""
        print(f"  {RANK_NAMES[r]:4s}  {c:>8}  {t:>5}  {pct:>5}{marker}")
    total_c = sum(rank_complete.values())
    print(f"  {'Total':6s}  {total_c:>8}  {64:>5}  {total_c/64:.0%}")

    # Per-palace breakdown
    palaces = sorted(set(p["palace"] for p in profiles))
    print(f"\n  Per-palace completeness (✓=5/5, ✗=<5):")
    header = f"  {'Palace':10s} " + " ".join(f"{RANK_NAMES[r][:2]:>4}" for r in range(8))
    print(header)
    print(f"  {'─'*10} " + " ".join("────" for _ in range(8)))
    for pal in palaces:
        cells = []
        for r in range(8):
            c = palace_rank_complete[pal][r]
            t = palace_rank_total[pal][r]
            cells.append("  ✓ " if c == t and t > 0 else "  ✗ " if t > 0 else "  — ")
        print(f"  {pal:10s} {''.join(cells)}")

    return rank_complete


def nayin_distribution(profiles):
    """納音 distribution across positions."""
    print("\n" + "=" * 60)
    print("納音 DISTRIBUTION")
    print("=" * 60)

    # Name frequency
    name_freq = Counter()
    name_by_pos = defaultdict(Counter)
    elem_by_pos = defaultdict(Counter)
    name_positions = defaultdict(set)

    for p in profiles:
        for l in p["lines"]:
            pos = l["position"]
            name_freq[l["nayin_name"]] += 1
            name_by_pos[pos][l["nayin_name"]] += 1
            elem_by_pos[pos][l["nayin_element"]] += 1
            name_positions[l["nayin_name"]].add(pos)

    # Overall frequency
    print(f"\n  納音 name frequency (384 positions, 30 possible names):")
    used = sorted(name_freq.items(), key=lambda x: -x[1])
    for name, cnt in used:
        positions = sorted(name_positions[name])
        pos_str = ",".join(f"L{p}" for p in positions)
        print(f"    {name:6s}: {cnt:>3}× at {pos_str}")

    absent = set(n for n, _ in [
        ("海中金", ""), ("爐中火", ""), ("大林木", ""), ("路旁土", ""), ("劍鋒金", ""),
        ("山頭火", ""), ("澗下水", ""), ("城頭土", ""), ("白蠟金", ""), ("楊柳木", ""),
        ("泉中水", ""), ("屋上土", ""), ("霹靂火", ""), ("松柏木", ""), ("長流水", ""),
        ("沙中金", ""), ("山下火", ""), ("平地木", ""), ("壁上土", ""), ("金箔金", ""),
        ("覆燈火", ""), ("天河水", ""), ("大驛土", ""), ("釵釧金", ""), ("桑柘木", ""),
        ("大溪水", ""), ("沙中土", ""), ("天上火", ""), ("石榴木", ""), ("大海水", ""),
    ]) - set(name_freq.keys())
    if absent:
        print(f"\n  Absent 納音 names ({len(absent)}): {', '.join(sorted(absent))}")
    print(f"\n  Used: {len(name_freq)}/30 names")

    # Element by position
    print(f"\n  納音 element by position:")
    header = f"  {'Pos':>3} " + " ".join(f"{e[:2]:>5}" for e in ELEMENTS)
    print(header)
    print(f"  {'─'*3} " + " ".join("─────" for _ in ELEMENTS))
    for pos in range(1, 7):
        row = " ".join(f"{elem_by_pos[pos].get(e, 0):>5}" for e in ELEMENTS)
        print(f"  L{pos:1d}  {row}")

    # Position concentration: does any name cluster at specific positions?
    print(f"\n  Position concentration (names appearing at ≤2 positions):")
    concentrated = [(n, sorted(name_positions[n])) for n in name_freq
                    if len(name_positions[n]) <= 2]
    for name, poss in sorted(concentrated, key=lambda x: x[1]):
        pos_str = ",".join(f"L{p}" for p in poss)
        print(f"    {name}: only at {pos_str} ({name_freq[name]}×)")


def guashen_distribution(profiles):
    """卦身 distribution analysis."""
    print("\n" + "=" * 60)
    print("卦身 DISTRIBUTION")
    print("=" * 60)

    # By palace
    palace_gs = defaultdict(list)
    for p in profiles:
        palace_gs[p["palace"]].append(p)

    palaces = sorted(set(p["palace"] for p in profiles))
    print(f"\n  By palace (on-line / off-line):")
    for pal in palaces:
        members = palace_gs[pal]
        on = sum(1 for m in members if m["guashen_line"] is not None)
        off = len(members) - on
        print(f"    {pal:10s}: {on} on-line, {off} off-line")

    # By 六親 it lands on
    gs_liuqin = Counter()
    for p in profiles:
        gl = p["guashen_line"]
        if gl is not None:
            lq = p["lines"][gl - 1]["liuqin"]
            gs_liuqin[lq] += 1
    print(f"\n  卦身 lands on 六親 (when on-line, n={sum(gs_liuqin.values())}):")
    for lq in LIUQIN_NAMES:
        print(f"    {lq}: {gs_liuqin.get(lq, 0)}")

    # By line position
    gs_line = Counter()
    for p in profiles:
        gl = p["guashen_line"]
        if gl is not None:
            gs_line[gl] += 1
    print(f"\n  卦身 by line position:")
    for ln in range(1, 7):
        print(f"    L{ln}: {gs_line.get(ln, 0)}")

    # Element distribution
    gs_elem = Counter(p["guashen_element"] for p in profiles)
    print(f"\n  卦身 element distribution (all 64):")
    for e in ELEMENTS:
        print(f"    {e}: {gs_elem.get(e, 0)}")

    # 卦身 vs 世 line
    gs_at_shi = sum(1 for p in profiles if p["guashen_line"] == p["shi_line"])
    gs_at_ying = sum(1 for p in profiles if p["guashen_line"] == p["ying_line"])
    print(f"\n  卦身 at 世: {gs_at_shi}/64")
    print(f"  卦身 at 應: {gs_at_ying}/64")


# ═══════════════════════════════════════════════════════════════════════════
# §I.4 Static interaction topology
# ═══════════════════════════════════════════════════════════════════════════

def compute_topology(profiles):
    """Compute branch-level interaction topology for each hexagram."""
    print("\n" + "=" * 60)
    print("STATIC INTERACTION TOPOLOGY")
    print("=" * 60)

    PRIMITIVES = ["沖", "合", "刑", "害", "墓", "生", "克"]

    all_topo = []
    prim_counts = Counter()   # primitive → total edges across all hexagrams
    hex_edge_counts = []      # total edges per hexagram

    for p in profiles:
        lines = p["lines"]
        branch_indices = [BRANCH_IDX[l["branch"]] for l in lines]
        elements = [l["element"] for l in lines]

        topo = {prim: [] for prim in PRIMITIVES}

        # Check all 15 line pairs for 沖/合/刑/害
        for i in range(6):
            for j in range(i + 1, 6):
                bi, bj = branch_indices[i], branch_indices[j]
                li, lj = i + 1, j + 1  # 1-indexed

                if is_chong(bi, bj):
                    topo["沖"].append([li, lj])
                if is_he(bi, bj):
                    topo["合"].append([li, lj])
                if is_xing(bi, bj):
                    topo["刑"].append([li, lj])
                if is_hai(bi, bj):
                    topo["害"].append([li, lj])

                # 生/克 (element level, directional)
                ei, ej = elements[i], elements[j]
                if SHENG_MAP[ei] == ej:
                    topo["生"].append([li, lj])
                elif SHENG_MAP[ej] == ei:
                    topo["生"].append([lj, li])

                if KE_MAP[ei] == ej:
                    topo["克"].append([li, lj])
                elif KE_MAP[ej] == ei:
                    topo["克"].append([lj, li])

        # 墓: line i's element → graveyard branch = line j's branch
        for i in range(6):
            mu_bi = MU_BRANCH[elements[i]]
            for j in range(6):
                if i != j and branch_indices[j] == mu_bi:
                    topo["墓"].append([i + 1, j + 1])  # i enters tomb at j

        total_edges = sum(len(v) for v in topo.values())
        hex_edge_counts.append(total_edges)
        for prim in PRIMITIVES:
            prim_counts[prim] += len(topo[prim])

        all_topo.append({
            "hex_val": p["hex_val"],
            "topology": topo,
        })

    # Summary
    print(f"\n  Primitive frequency (across 64 hexagrams):")
    print(f"  {'Primitive':>6}  Total  Avg/hex")
    print(f"  {'─'*6}──{'─'*5}──{'─'*7}")
    for prim in PRIMITIVES:
        avg = prim_counts[prim] / 64
        print(f"  {prim:>4}    {prim_counts[prim]:>5}  {avg:>7.2f}")
    total = sum(prim_counts.values())
    print(f"  {'Total':>6}  {total:>5}  {total/64:>7.2f}")

    # Edge count distribution
    edge_dist = Counter(hex_edge_counts)
    print(f"\n  Total edges per hexagram:")
    mn, mx = min(hex_edge_counts), max(hex_edge_counts)
    avg = sum(hex_edge_counts) / 64
    print(f"    Range: [{mn}, {mx}], Mean: {avg:.1f}")
    print(f"    Distribution:")
    for n in sorted(edge_dist):
        bar = "█" * edge_dist[n]
        print(f"      {n:>2}: {edge_dist[n]:>2} {bar}")

    # Most/least common primitives
    most = max(PRIMITIVES, key=lambda x: prim_counts[x])
    least = min(PRIMITIVES, key=lambda x: prim_counts[x])
    print(f"\n  Most common: {most} ({prim_counts[most]} total, {prim_counts[most]/64:.1f}/hex)")
    print(f"  Least common: {least} ({prim_counts[least]} total, {prim_counts[least]/64:.1f}/hex)")

    # Per-primitive: how many hexagrams have ≥1 of this type?
    print(f"\n  Hexagrams with ≥1 of each primitive:")
    for prim in PRIMITIVES:
        n_with = sum(1 for t in all_topo if t["topology"][prim])
        print(f"    {prim}: {n_with}/64 ({n_with/64:.0%})")

    return all_topo


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    profiles = load_profiles()
    print(f"Loaded {len(profiles)} profiles\n")

    # §I.3
    cross_tab_shi_ying_liuqin(profiles)
    feifu_completeness_by_rank(profiles)
    nayin_distribution(profiles)
    guashen_distribution(profiles)

    # §I.4
    topo = compute_topology(profiles)

    # Write topology
    out_path = HERE / "hzl_topology.json"
    out_path.write_text(json.dumps(topo, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote {len(topo)} topology entries to {out_path}")


if __name__ == "__main__":
    main()
