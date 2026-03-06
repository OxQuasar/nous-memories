#!/usr/bin/env python3
"""
07_convergence_fivephase.py — Five-phase flow along convergence.

Attractor elements, feeder→attractor five-phase relations,
convergence tree annotations, 生 cycle geometry, KW walk dynamics.
"""

import sys
sys.path.insert(0, 'memories/iching/opposition-theory/phase4')
sys.path.insert(0, 'memories/iching/kingwen')

from collections import defaultdict, Counter
from cycle_algebra import (
    hugua, bit, fmt6, fmt3, lower_trigram, upper_trigram,
    TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENT_ZH,
    five_phase_relation, SHENG_MAP, KE_MAP, SHENG_CYCLE,
)
from sequence import KING_WEN

# ═══════════════════════════════════════════════════════════════════════
# Lookups
# ═══════════════════════════════════════════════════════════════════════

NUM_HEX = 64
ATTRACTORS = frozenset({0, 21, 42, 63})

KW_SEQ = []
KW = {}
for kw_num, name, binstr in KING_WEN:
    val = sum(int(c) << i for i, c in enumerate(binstr))
    KW_SEQ.append((kw_num, val, name))
    KW[val] = (kw_num, name)

def inner(h):
    return (h >> 1) & 0xF

def inner_hugua(v):
    x = v << 1
    return inner(hugua(x))

def basin_of(h):
    b2, b3 = bit(h, 2), bit(h, 3)
    if b2 == 0 and b3 == 0: return "Kun"
    if b2 == 1 and b3 == 1: return "Qian"
    return "Cycle"

def lower_nuclear(v):
    """Lower nuclear trigram from inner value (bits 0-2)."""
    return v & 0b111

def upper_nuclear(v):
    """Upper nuclear trigram from inner value (bits 1-3)."""
    return (v >> 1) & 0b111

def trig_label(t):
    return TRIGRAM_NAMES[t].split()[0]

def elem_zh(e):
    return ELEMENT_ZH.get(e, "?")

# Compute depths (BFS from attractors)
def compute_depths():
    edges = {h: hugua(h) for h in range(NUM_HEX)}
    depth = {a: 0 for a in ATTRACTORS}
    frontier = set(ATTRACTORS)
    d = 0
    while frontier:
        d += 1
        nxt = set()
        for h in range(NUM_HEX):
            if h not in depth and edges[h] in frontier:
                depth[h] = d
                nxt.add(h)
        frontier = nxt
    return depth

DEPTH = compute_depths()

# Inner space graph
INNER_EDGES = {v: inner_hugua(v) for v in range(16)}
INNER_ATTRACTORS = {0, 5, 10, 15}


# ═══════════════════════════════════════════════════════════════════════
# Part 1: Attractor Elements
# ═══════════════════════════════════════════════════════════════════════

def section_attractor_elements():
    print("=" * 80)
    print("PART 1: ATTRACTOR ELEMENTS")
    print("=" * 80)

    for h in sorted(ATTRACTORS):
        kw_num, name = KW[h]
        hu_lo = lower_trigram(hugua(h))  # nuclear trigrams = trigrams of hugua output
        hu_up = upper_trigram(hugua(h))
        # For attractors, hugua output maps to self or cycle partner
        lo_e = TRIGRAM_ELEMENT[hu_lo]
        up_e = TRIGRAM_ELEMENT[hu_up]
        b = basin_of(h)
        print(f"\n  {h:3d} = {fmt6(h)} = KW#{kw_num}({name}) [{b}]")
        print(f"    Nuclear lower: {trig_label(hu_lo)} ({fmt3(hu_lo)}) = {lo_e} ({elem_zh(lo_e)})")
        print(f"    Nuclear upper: {trig_label(hu_up)} ({fmt3(hu_up)}) = {up_e} ({elem_zh(up_e)})")

        # Also show the hexagram's own trigrams
        own_lo = lower_trigram(h)
        own_up = upper_trigram(h)
        print(f"    Own lower: {trig_label(own_lo)} ({fmt3(own_lo)})")
        print(f"    Own upper: {trig_label(own_up)} ({fmt3(own_up)})")


# ═══════════════════════════════════════════════════════════════════════
# Part 2: Feeder → Attractor Five-Phase
# ═══════════════════════════════════════════════════════════════════════

def section_feeder_attractor():
    print("\n" + "=" * 80)
    print("PART 2: FEEDER → ATTRACTOR FIVE-PHASE RELATIONS")
    print("=" * 80)

    # Work in inner space: 16 nodes, 4 attractors, 12 feeders
    # For each feeder, compute five-phase relation of nuclear trigrams
    # to its attractor's nuclear trigrams

    print(f"\n  {'v':>3} {'lo_nuc':>7} {'up_nuc':>7} {'lo_e':>6} {'up_e':>6}"
          f" → {'att':>3} {'att_lo_e':>8} {'att_up_e':>8}"
          f" {'lo_rel':>8} {'up_rel':>8} {'basin':>6}")
    print("-" * 90)

    # Group by basin for analysis
    basin_relations = defaultdict(list)

    for v in range(16):
        if v in INNER_ATTRACTORS:
            continue  # skip attractors themselves

        att = INNER_EDGES[v]  # direct feeder → attractor (depth 1 in inner space)
        if att not in INNER_ATTRACTORS:
            # depth 2 in inner: follow one more step
            att = INNER_EDGES[att]

        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        att_lo = lower_nuclear(att)
        att_up = upper_nuclear(att)

        lo_e = TRIGRAM_ELEMENT[lo]
        up_e = TRIGRAM_ELEMENT[up]
        att_lo_e = TRIGRAM_ELEMENT[att_lo]
        att_up_e = TRIGRAM_ELEMENT[att_up]

        # five_phase_relation(ti_elem, yong_elem):
        # ti = attractor (体), yong = feeder (用)
        lo_rel = five_phase_relation(att_lo_e, lo_e)
        up_rel = five_phase_relation(att_up_e, up_e)

        basin = basin_of(v << 1)  # use representative hex
        basin_relations[basin].append((v, att, lo_rel, up_rel, lo_e, up_e, att_lo_e, att_up_e))

        print(f"  {v:3d} {trig_label(lo):>7} {trig_label(up):>7}"
              f" {lo_e[:3]:>6} {up_e[:3]:>6}"
              f" → {att:3d} {att_lo_e[:3]:>8} {att_up_e[:3]:>8}"
              f" {lo_rel:>8} {up_rel:>8} {basin:>6}")

    # Summary per basin
    print(f"\n{'─' * 70}")
    print(f"SUMMARY BY BASIN")
    print(f"{'─' * 70}")

    for basin_name in ["Kun", "Cycle", "Qian"]:
        rels = basin_relations[basin_name]
        if not rels:
            continue
        lo_rels = [r[2] for r in rels]
        up_rels = [r[3] for r in rels]

        print(f"\n  {basin_name} basin ({len(rels)} feeders):")
        print(f"    Lower nuclear relations: {Counter(lo_rels)}")
        print(f"    Upper nuclear relations: {Counter(up_rels)}")

        # Check if all relations are the same
        all_lo = set(lo_rels)
        all_up = set(up_rels)
        if len(all_lo) == 1:
            print(f"    → Lower: UNIFORM {all_lo.pop()}")
        if len(all_up) == 1:
            print(f"    → Upper: UNIFORM {all_up.pop()}")

    return basin_relations


# ═══════════════════════════════════════════════════════════════════════
# Part 3: Convergence Tree with Five-Phase Annotations
# ═══════════════════════════════════════════════════════════════════════

def section_convergence_tree(basin_relations):
    print("\n" + "=" * 80)
    print("PART 3: CONVERGENCE TREE WITH FIVE-PHASE ANNOTATIONS")
    print("=" * 80)

    # Build reverse tree in inner space
    children = defaultdict(list)
    for v in range(16):
        if v not in INNER_ATTRACTORS:
            children[INNER_EDGES[v]].append(v)

    # For each basin, show the tree
    basin_attractors = {
        "Kun": [0], "Qian": [15], "Cycle": [5, 10]
    }

    for basin_name in ["Kun", "Cycle", "Qian"]:
        print(f"\n{'─' * 60}")
        print(f"  {basin_name} Basin")
        print(f"{'─' * 60}")

        attractors = basin_attractors[basin_name]
        if len(attractors) == 2:
            print(f"  {_inner_label(attractors[0])} ←→ {_inner_label(attractors[1])} [2-cycle]")

        for att in attractors:
            att_lo = lower_nuclear(att)
            att_up = upper_nuclear(att)
            att_lo_e = TRIGRAM_ELEMENT[att_lo]
            att_up_e = TRIGRAM_ELEMENT[att_up]

            print(f"\n  Attractor {att} ({trig_label(att_lo)}/{trig_label(att_up)})"
                  f" [{att_lo_e}/{att_up_e}]")

            feeders = children.get(att, [])
            for f in sorted(feeders):
                f_lo = lower_nuclear(f)
                f_up = upper_nuclear(f)
                f_lo_e = TRIGRAM_ELEMENT[f_lo]
                f_up_e = TRIGRAM_ELEMENT[f_up]

                lo_rel = five_phase_relation(att_lo_e, f_lo_e)
                up_rel = five_phase_relation(att_up_e, f_up_e)

                print(f"    ← {f:2d} ({trig_label(f_lo)}/{trig_label(f_up)})"
                      f" [{f_lo_e}/{f_up_e}]"
                      f"  lo:{lo_rel} up:{up_rel}")

                # Depth-2 feeders (feed into this depth-1 feeder)
                d2_feeders = children.get(f, [])
                for g in sorted(d2_feeders):
                    g_lo = lower_nuclear(g)
                    g_up = upper_nuclear(g)
                    g_lo_e = TRIGRAM_ELEMENT[g_lo]
                    g_up_e = TRIGRAM_ELEMENT[g_up]

                    g_lo_rel = five_phase_relation(f_lo_e, g_lo_e)
                    g_up_rel = five_phase_relation(f_up_e, g_up_e)

                    print(f"        ← {g:2d} ({trig_label(g_lo)}/{trig_label(g_up)})"
                          f" [{g_lo_e}/{g_up_e}]"
                          f"  lo:{g_lo_rel} up:{g_up_rel}")


def _inner_label(v):
    lo = lower_nuclear(v)
    up = upper_nuclear(v)
    return f"{v}({trig_label(lo)}/{trig_label(up)})"


# ═══════════════════════════════════════════════════════════════════════
# Part 4: 生 Cycle Geometry
# ═══════════════════════════════════════════════════════════════════════

def section_sheng_cycle():
    print("\n" + "=" * 80)
    print("PART 4: 生 CYCLE GEOMETRY")
    print("=" * 80)

    # Map each inner value to its elements
    print(f"\n  Inner value element map:")
    print(f"  {'v':>3} {'lo':>5} {'up':>5} {'lo_e':>6} {'up_e':>6}")
    for v in range(16):
        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        print(f"  {v:3d} {trig_label(lo):>5} {trig_label(up):>5}"
              f" {TRIGRAM_ELEMENT[lo]:>6} {TRIGRAM_ELEMENT[up]:>6}")

    # Count five-phase relation types along ALL convergence edges
    # (both depth-1→attractor and depth-2→depth-1)
    all_lo_rels = []
    all_up_rels = []

    for v in range(16):
        target = INNER_EDGES[v]
        if v == target:
            continue  # self-loop

        v_lo_e = TRIGRAM_ELEMENT[lower_nuclear(v)]
        v_up_e = TRIGRAM_ELEMENT[upper_nuclear(v)]
        t_lo_e = TRIGRAM_ELEMENT[lower_nuclear(target)]
        t_up_e = TRIGRAM_ELEMENT[upper_nuclear(target)]

        # Relation: target is 体 (receiving), v is 用 (giving)
        lo_rel = five_phase_relation(t_lo_e, v_lo_e)
        up_rel = five_phase_relation(t_up_e, v_up_e)

        all_lo_rels.append(lo_rel)
        all_up_rels.append(up_rel)

    print(f"\n  All convergence edge relations:")
    print(f"    Lower nuclear: {Counter(all_lo_rels)}")
    print(f"    Upper nuclear: {Counter(all_up_rels)}")

    combined = all_lo_rels + all_up_rels
    print(f"    Combined: {Counter(combined)}")

    total = len(combined)
    print(f"\n  Distribution:")
    for rel, count in sorted(Counter(combined).items(), key=lambda x: -x[1]):
        pct = 100 * count / total
        print(f"    {rel}: {count}/{total} ({pct:.0f}%)")

    # 生 cycle step analysis
    print(f"\n  生 cycle: {' → '.join(SHENG_CYCLE)} → (cycle)")
    print(f"\n  How many convergence edges are 生 steps?")

    sheng_count = 0
    ke_count = 0
    bi_count = 0

    for v in range(16):
        target = INNER_EDGES[v]
        if v == target:
            continue

        for nuc_fn in [lower_nuclear, upper_nuclear]:
            v_e = TRIGRAM_ELEMENT[nuc_fn(v)]
            t_e = TRIGRAM_ELEMENT[nuc_fn(target)]

            if v_e == t_e:
                bi_count += 1
            elif SHENG_MAP[v_e] == t_e:
                sheng_count += 1  # v generates t (v 生 t)
            elif SHENG_MAP[t_e] == v_e:
                sheng_count += 1  # t generates v (reverse 生)
            elif KE_MAP[v_e] == t_e:
                ke_count += 1
            elif KE_MAP[t_e] == v_e:
                ke_count += 1

    total2 = sheng_count + ke_count + bi_count
    print(f"    生 (either direction): {sheng_count}/{total2}")
    print(f"    克 (either direction): {ke_count}/{total2}")
    print(f"    比和: {bi_count}/{total2}")


# ═══════════════════════════════════════════════════════════════════════
# Part 5: KW Walk Five-Phase Dynamics
# ═══════════════════════════════════════════════════════════════════════

def section_kw_walk():
    print("\n" + "=" * 80)
    print("PART 5: KW WALK FIVE-PHASE DYNAMICS")
    print("=" * 80)

    # For each consecutive KW pair (n, n+1):
    # - depth change
    # - five-phase relation between nuclear trigrams

    print(f"\n  {'n':>3} {'→':>1} {'n+1':>3} {'d_n':>3} {'d_{n+1}':>7} {'Δd':>3}"
          f" {'lo_rel':>8} {'up_rel':>8}"
          f" {'name_n':>12} {'name_n1':>12}")
    print("-" * 80)

    depth_changes = []
    rel_pairs_by_delta = defaultdict(list)

    for i in range(len(KW_SEQ) - 1):
        kw_n, val_n, name_n = KW_SEQ[i]
        kw_n1, val_n1, name_n1 = KW_SEQ[i + 1]

        d_n = DEPTH[val_n]
        d_n1 = DEPTH[val_n1]
        delta_d = d_n1 - d_n

        # Nuclear trigrams from hugua output
        hu_n = hugua(val_n)
        hu_n1 = hugua(val_n1)

        lo_n = lower_trigram(hu_n)
        up_n = upper_trigram(hu_n)
        lo_n1 = lower_trigram(hu_n1)
        up_n1 = upper_trigram(hu_n1)

        lo_e_n = TRIGRAM_ELEMENT[lo_n]
        up_e_n = TRIGRAM_ELEMENT[up_n]
        lo_e_n1 = TRIGRAM_ELEMENT[lo_n1]
        up_e_n1 = TRIGRAM_ELEMENT[up_n1]

        # Relation: n+1 as 体, n as 用
        lo_rel = five_phase_relation(lo_e_n1, lo_e_n)
        up_rel = five_phase_relation(up_e_n1, up_e_n)

        depth_changes.append(delta_d)
        rel_pairs_by_delta[delta_d].append((lo_rel, up_rel))

        print(f"  {kw_n:3d} → {kw_n1:3d} {d_n:3d} {d_n1:7d} {delta_d:+3d}"
              f" {lo_rel:>8} {up_rel:>8}"
              f" {name_n:>12} {name_n1:>12}")

    # Summary: depth change distribution
    dc = Counter(depth_changes)
    print(f"\n  Depth change distribution:")
    for delta in sorted(dc.keys()):
        print(f"    Δd={delta:+d}: {dc[delta]} transitions")

    # Relation distribution by depth change
    print(f"\n  Five-phase relations BY depth change:")
    for delta in sorted(rel_pairs_by_delta.keys()):
        pairs = rel_pairs_by_delta[delta]
        lo_rels = Counter(r[0] for r in pairs)
        up_rels = Counter(r[1] for r in pairs)
        print(f"\n    Δd={delta:+d} ({len(pairs)} transitions):")
        print(f"      Lower nuclear: {dict(lo_rels)}")
        print(f"      Upper nuclear: {dict(up_rels)}")

    # Correlation test: does descending depth correlate with 生?
    print(f"\n  Correlation test: depth descent vs 生")
    for delta in sorted(rel_pairs_by_delta.keys()):
        pairs = rel_pairs_by_delta[delta]
        all_rels = [r[0] for r in pairs] + [r[1] for r in pairs]
        total = len(all_rels)
        sheng = sum(1 for r in all_rels if '生' in r)
        ke = sum(1 for r in all_rels if '克' in r)
        bi = sum(1 for r in all_rels if '比' in r)
        print(f"    Δd={delta:+d}: 生={sheng}/{total} ({100*sheng/total:.0f}%),"
              f" 克={ke}/{total} ({100*ke/total:.0f}%),"
              f" 比={bi}/{total} ({100*bi/total:.0f}%)")


# ═══════════════════════════════════════════════════════════════════════
# Key Findings
# ═══════════════════════════════════════════════════════════════════════

def section_key_findings(basin_relations):
    print("\n" + "=" * 70)
    print("## Key Findings")
    print("=" * 70)

    # Compute overall relation stats
    all_rels = []
    for basin, rels in basin_relations.items():
        for _, _, lo_r, up_r, *_ in rels:
            all_rels.extend([lo_r, up_r])
    rel_counts = Counter(all_rels)
    total = len(all_rels)

    print(f"""
1. ATTRACTOR ELEMENTS
   Kun  (000000): Kun/Kun   = Earth/Earth — pure Earth
   Qian (111111): Qian/Qian = Metal/Metal — pure Metal
   JiJi (010101): Li/Kan    = Fire/Water  — opposition pair
   WeiJi(101010): Kan/Li    = Water/Fire  — opposition pair (reversed)

2. FEEDER→ATTRACTOR FIVE-PHASE RELATIONS
   Overall distribution of relations (feeder→attractor):""")
    for r, c in sorted(rel_counts.items(), key=lambda x: -x[1]):
        print(f"     {r}: {c}/{total} ({100*c/total:.0f}%)")

    # Per-basin summary
    for basin_name in ["Kun", "Cycle", "Qian"]:
        rels = basin_relations.get(basin_name, [])
        if not rels:
            continue
        lo_rels = Counter(r[2] for r in rels)
        up_rels = Counter(r[3] for r in rels)
        print(f"\n   {basin_name} basin:")
        print(f"     Lower: {dict(lo_rels)}")
        print(f"     Upper: {dict(up_rels)}")

    print(f"""
3. UPPER NUCLEAR IS ALWAYS 比和 IN FIXED-POINT BASINS
   Kun feeders:  upper always Earth → 比和 with attractor Kun
   Qian feeders: upper always Metal → 比和 with attractor Qian
   STRUCTURAL REASON: upper nuclear = (b₂,b₃,b₄). Within a basin,
   (b₂,b₃) is fixed. For Kun: (0,0,b₄) = Kun or Gen, both Earth.
   For Qian: (1,1,b₄) = Dui or Qian, both Metal.
   The interface bits force the element identity.

4. LOWER NUCLEAR VARIES — ONLY b₁ IS FREE
   Lower nuclear = (b₁,b₂,b₃). Within a basin, (b₂,b₃) is fixed.
   Kun basin: (b₁,0,0) = Kun(Earth) or Zhen(Wood) → 比和 or 克体
   Qian basin: (b₁,1,1) = Xun(Wood) or Qian(Metal) → 体克用 or 比和
   Single free bit (b₁) toggles between exactly 2 elements.

5. CYCLE BASIN IS MIXED
   JiJi/WeiJi have Fire/Water (opposition pair).
   Interface bits (1,0) or (0,1) give non-paired trigrams,
   breaking the element-purity of fixed-point basins.
   Result: all five relations appear in Cycle feeders.

6. KW WALK: NO 生/克 CORRELATION WITH DEPTH
   Δd=0 transitions (51/63): 克 41%, 比 30%, 生 28% — slightly 克-biased.
   Δd=±1 (small samples): mixed.
   The KW ordering is NOT organized by five-phase convergence.

7. CONVERGENCE IS ELEMENT-CONSERVATIVE
   33% of all feeder→attractor relations are 比和.
   This is forced by the overlap constraint: 2 of 3 nuclear
   trigram bits are shared → the element can only change via
   the single free bit (b₁ or b₄).
""")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("07: FIVE-PHASE FLOW ALONG CONVERGENCE")
    print("=" * 70)

    section_attractor_elements()
    basin_relations = section_feeder_attractor()
    section_convergence_tree(basin_relations)
    section_sheng_cycle()
    section_kw_walk()
    section_key_findings(basin_relations)


if __name__ == '__main__':
    main()
