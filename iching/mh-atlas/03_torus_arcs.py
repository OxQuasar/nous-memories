#!/usr/bin/env python3
"""
03_torus_arcs: 梅花 torus flow (§II) + arc classification (§III).

§II: Torus axes = (ti_element, yong_element). 體 fixed throughout →
     flow is 1D along the 用-axis: 本→互(ti_hu, yong_hu)→變.
§III: Classify relation_vector into arc types by valence trajectory.

Updates mh_states.json with mh_torus_cell, arc_type.
Writes mh_torus_flow.json, mh_arcs.json.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATES_PATH = HERE / "mh_states.json"
ATLAS_Z5_PATH = HERE.parent / "atlas" / "z5z5_cells.json"

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

VALENCE_ORDER = {"生体": 2, "体克用": 1, "比和": 0, "体生用": -1, "克体": -2}

# Arc types in priority order (first match wins)
ARC_PRIORITY = [
    "stable_neutral",
    "rescued",
    "betrayed",
    "improving",
    "deteriorating",
    "stable_favorable",
    "stable_unfavorable",
    "mixed",
]


def cell_key(a, b):
    return f"({a},{b})"


# ═══════════════════════════════════════════════════════════════════════════
# §II: Torus flow
# ═══════════════════════════════════════════════════════════════════════════

def compute_torus_cells(states):
    """Add mh_torus_cell to each state; build per-cell flow data."""
    cells = defaultdict(lambda: {
        "states": [],
        "hu_target_pairs": set(),  # (ti_hu_cell, yong_hu_cell)
        "bian_targets": set(),
        "basin_dist": Counter(),
    })

    for s in states:
        ti_e = s["ti_element"]
        yong_e = s["yong_element"]
        ck = cell_key(ti_e, yong_e)
        s["mh_torus_cell"] = [ti_e, yong_e]

        # Flow cells (體 fixed on first axis)
        ti_hu_ck = cell_key(ti_e, s["ti_hu_element"])
        yong_hu_ck = cell_key(ti_e, s["yong_hu_element"])
        bian_ck = cell_key(ti_e, s["bian_yong_element"])

        c = cells[ck]
        c["states"].append(s)
        c["hu_target_pairs"].add((ti_hu_ck, yong_hu_ck))
        c["bian_targets"].add(bian_ck)
        c["basin_dist"][s["basin"]] += 1

    return cells


def build_torus_flow_json(cells):
    """Build serializable per-cell data."""
    flow = {}
    for ck in sorted(cells):
        c = cells[ck]
        parts = ck.strip("()").split(",")
        flow[ck] = {
            "cell": [parts[0], parts[1]],
            "population": len(c["states"]),
            "hu_target_pairs": sorted(list(c["hu_target_pairs"])),
            "hu_target_count": len(c["hu_target_pairs"]),
            "well_defined": len(c["hu_target_pairs"]) == 1,
            "bian_targets": sorted(list(c["bian_targets"])),
            "bian_target_count": len(c["bian_targets"]),
            "basin_distribution": dict(c["basin_dist"]),
        }
    return flow


def print_torus_analysis(flow):
    print("=" * 70)
    print("§II: 梅花 TORUS FLOW")
    print("=" * 70)

    populated = {k: v for k, v in flow.items() if v["population"] > 0}
    total_cells = 25
    pop_count = len(populated)
    print(f"\nPopulated cells: {pop_count}/{total_cells}")

    # Population grid
    print(f"\nPopulation grid (ti_element rows × yong_element cols):")
    print(f"{'':8s}", end="")
    for e in ELEMENTS:
        print(f"{e:>8s}", end="")
    print(f"{'total':>8s}")
    for ti in ELEMENTS:
        print(f"{ti:8s}", end="")
        row_total = 0
        for yo in ELEMENTS:
            ck = cell_key(ti, yo)
            p = flow.get(ck, {}).get("population", 0)
            row_total += p
            print(f"{p:8d}", end="")
        print(f"{row_total:8d}")

    # Well-defined analysis
    wd = sum(1 for v in populated.values() if v["well_defined"])
    mv = pop_count - wd
    print(f"\nWell-defined 互 cells: {wd}/{pop_count}")
    print(f"Multi-valued 互 cells: {mv}/{pop_count}")
    print(f"(Atlas comparison: 17/25 multi-valued)")

    # Show well-defined cells
    if wd > 0:
        print(f"\nWell-defined cells:")
        for ck, v in sorted(populated.items()):
            if v["well_defined"]:
                pair = v["hu_target_pairs"][0]
                print(f"  {ck:20s} (pop={v['population']:3d}) → 互: {pair}")

    # Show multi-valued cells (top by target count)
    if mv > 0:
        print(f"\nMulti-valued cells (sorted by 互 target count):")
        mvs = [(ck, v) for ck, v in sorted(populated.items()) if not v["well_defined"]]
        mvs.sort(key=lambda x: -x[1]["hu_target_count"])
        for ck, v in mvs:
            print(f"  {ck:20s} (pop={v['population']:3d}) → {v['hu_target_count']} 互 targets, "
                  f"{v['bian_target_count']} 變 targets")

    # 變 target counts
    bian_counts = Counter(v["bian_target_count"] for v in populated.values())
    print(f"\n變 target count distribution:")
    for k in sorted(bian_counts):
        print(f"  {k} targets: {bian_counts[k]} cells")


# ═══════════════════════════════════════════════════════════════════════════
# §III: Arc classification
# ═══════════════════════════════════════════════════════════════════════════

def classify_arc(relation_vector):
    """Classify relation_vector into arc type. Priority-ordered."""
    vals = [VALENCE_ORDER[r] for r in relation_vector]
    ben_v, ti_hu_v, yong_hu_v, bian_v = vals

    # stable_neutral: all == 0
    if all(v == 0 for v in vals):
        return "stable_neutral"

    # rescued: starts negative, ends positive
    if ben_v < 0 and bian_v > 0:
        return "rescued"

    # betrayed: starts positive, ends negative
    if ben_v > 0 and bian_v < 0:
        return "betrayed"

    # improving: ends better than start, ends positive
    if bian_v > ben_v and bian_v > 0:
        return "improving"

    # deteriorating: ends worse than start, ends negative
    if bian_v < ben_v and bian_v < 0:
        return "deteriorating"

    # stable_favorable: all >= 0, at least one > 0
    if all(v >= 0 for v in vals) and any(v > 0 for v in vals):
        return "stable_favorable"

    # stable_unfavorable: all <= 0, at least one < 0
    if all(v <= 0 for v in vals) and any(v < 0 for v in vals):
        return "stable_unfavorable"

    return "mixed"


def build_arcs_json(states):
    """Build arc summary data."""
    arc_dist = Counter(s["arc_type"] for s in states)
    vec_to_arc = {}
    for s in states:
        vec = tuple(s["relation_vector"])
        vec_to_arc[vec] = s["arc_type"]

    arc_to_vecs = defaultdict(list)
    for vec, arc in sorted(vec_to_arc.items()):
        arc_to_vecs[arc].append(list(vec))

    return {
        "arc_type_distribution": {k: arc_dist.get(k, 0) for k in ARC_PRIORITY},
        "total_states": len(states),
        "realized_vectors": len(vec_to_arc),
        "vectors_per_arc_type": {k: len(v) for k, v in arc_to_vecs.items()},
        "arc_type_vectors": dict(arc_to_vecs),
    }


def print_arc_analysis(states):
    print("\n" + "=" * 70)
    print("§III: ARC CLASSIFICATION")
    print("=" * 70)

    # Distribution
    arc_dist = Counter(s["arc_type"] for s in states)
    print(f"\nArc type distribution (384 states):")
    for at in ARC_PRIORITY:
        cnt = arc_dist.get(at, 0)
        bar = "█" * (cnt // 4)
        print(f"  {at:22s}: {cnt:3d} ({100*cnt/384:5.1f}%) {bar}")

    # Arc type × basin cross-tab
    basins = sorted(set(s["basin"] for s in states))
    print(f"\nArc type × basin cross-tab:")
    print(f"{'':22s}", end="")
    for b in basins:
        print(f"{b:>8s}", end="")
    print(f"{'total':>8s}")

    observed = []
    expected = []
    total_n = len(states)
    basin_totals = Counter(s["basin"] for s in states)

    for at in ARC_PRIORITY:
        cnt = arc_dist.get(at, 0)
        if cnt == 0:
            continue
        row = []
        print(f"{at:22s}", end="")
        for b in basins:
            c = sum(1 for s in states if s["arc_type"] == at and s["basin"] == b)
            row.append(c)
            print(f"{c:8d}", end="")
            observed.append(c)
            expected.append(cnt * basin_totals[b] / total_n)
        print(f"{sum(row):8d}")

    print(f"{'total':22s}", end="")
    for b in basins:
        print(f"{basin_totals[b]:8d}", end="")
    print(f"{total_n:8d}")

    # χ² test
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
    df = (sum(1 for at in ARC_PRIORITY if arc_dist.get(at, 0) > 0) - 1) * (len(basins) - 1)
    print(f"\n  χ² = {chi2:.2f}, df = {df}")
    # Rough p-value thresholds
    if df > 0:
        # Critical values for common α levels (df=7×2=14 typical)
        print(f"  (critical values: df={df}, α=0.05 → ~{1.5*df + 2:.0f}, α=0.01 → ~{2*df + 3:.0f})")
        if chi2 < df:
            print(f"  → NOT significant (χ² < df)")
        elif chi2 > 2 * df:
            print(f"  → Likely significant")
        else:
            print(f"  → Marginal")

    # Arc type × ben_relation cross-tab
    ben_rels = ["生体", "体克用", "比和", "体生用", "克体"]
    print(f"\nArc type × ben_relation cross-tab:")
    print(f"{'':22s}", end="")
    for br in ben_rels:
        print(f"{br:>8s}", end="")
    print(f"{'total':>8s}")

    for at in ARC_PRIORITY:
        if arc_dist.get(at, 0) == 0:
            continue
        print(f"{at:22s}", end="")
        row = []
        for br in ben_rels:
            c = sum(1 for s in states if s["arc_type"] == at and s["ben_relation"] == br)
            row.append(c)
            print(f"{c:8d}", end="")
        print(f"{sum(row):8d}")

    # Forbidden arc analysis
    vec_to_arc = {}
    for s in states:
        vec = tuple(s["relation_vector"])
        vec_to_arc[vec] = s["arc_type"]

    print(f"\nRealized vectors per arc type:")
    arc_to_vecs = defaultdict(set)
    for vec, arc in vec_to_arc.items():
        arc_to_vecs[arc].add(vec)
    for at in ARC_PRIORITY:
        n = len(arc_to_vecs.get(at, set()))
        print(f"  {at:22s}: {n} vectors")

    # Any arc types algebraically impossible?
    empty_arcs = [at for at in ARC_PRIORITY if at not in arc_to_vecs]
    if empty_arcs:
        print(f"\nAlgebraically absent arc types: {empty_arcs}")
    else:
        print(f"\nAll arc types realized.")

    # ─── Critical test: 比和-at-本 states ───────────────────────────────────
    print(f"\n{'=' * 70}")
    print("CRITICAL TEST: 比和-at-本 states (ben_relation == '比和')")
    print("=" * 70)

    bihe_states = [s for s in states if s["ben_relation"] == "比和"]
    other_states = [s for s in states if s["ben_relation"] != "比和"]
    print(f"\n比和-at-本 count: {len(bihe_states)}")

    # ti_hu_relation distribution for 比和-at-本
    print(f"\nti_hu_relation distribution (比和-at-本 vs others):")
    print(f"{'relation':12s} {'比和-本':>10s} {'%':>7s} {'others':>10s} {'%':>7s}")
    for rel in ben_rels:
        bh_cnt = sum(1 for s in bihe_states if s["ti_hu_relation"] == rel)
        ot_cnt = sum(1 for s in other_states if s["ti_hu_relation"] == rel)
        bh_pct = 100 * bh_cnt / len(bihe_states) if bihe_states else 0
        ot_pct = 100 * ot_cnt / len(other_states) if other_states else 0
        print(f"  {rel:10s} {bh_cnt:10d} {bh_pct:6.1f}% {ot_cnt:10d} {ot_pct:6.1f}%")

    # Adversarial rate (克体 + 体生用)
    bh_adv = sum(1 for s in bihe_states
                 if s["ti_hu_relation"] in ("克体", "体生用"))
    ot_adv = sum(1 for s in other_states
                 if s["ti_hu_relation"] in ("克体", "体生用"))
    bh_pct = 100 * bh_adv / len(bihe_states)
    ot_pct = 100 * ot_adv / len(other_states)
    print(f"\n  Adversarial rate (克体+体生用):")
    print(f"    比和-at-本: {bh_adv}/{len(bihe_states)} = {bh_pct:.1f}%")
    print(f"    Others:     {ot_adv}/{len(other_states)} = {ot_pct:.1f}%")
    print(f"    Baseline (all 384): {(bh_adv+ot_adv)}/384 = "
          f"{100*(bh_adv+ot_adv)/384:.1f}%")

    # Arc type distribution for 比和-at-本
    bh_arc = Counter(s["arc_type"] for s in bihe_states)
    print(f"\nArc type distribution (比和-at-本):")
    for at in ARC_PRIORITY:
        cnt = bh_arc.get(at, 0)
        if cnt > 0:
            print(f"  {at:22s}: {cnt:3d} ({100*cnt/len(bihe_states):5.1f}%)")

    # 凶 rate: 比和-at-本 vs others
    bh_xiong = sum(1 for s in bihe_states if s["valence_markers"]["凶"])
    ot_xiong = sum(1 for s in other_states if s["valence_markers"]["凶"])
    bh_ji = sum(1 for s in bihe_states if s["valence_markers"]["吉"])
    ot_ji = sum(1 for s in other_states if s["valence_markers"]["吉"])
    print(f"\nValence marker comparison:")
    print(f"  {'':15s} {'比和-本':>10s} {'others':>10s}")
    print(f"  {'凶 rate':15s} {bh_xiong:3d}/{len(bihe_states)} = "
          f"{100*bh_xiong/len(bihe_states):.1f}%  "
          f"{ot_xiong:3d}/{len(other_states)} = "
          f"{100*ot_xiong/len(other_states):.1f}%")
    print(f"  {'吉 rate':15s} {bh_ji:3d}/{len(bihe_states)} = "
          f"{100*bh_ji/len(bihe_states):.1f}%  "
          f"{ot_ji:3d}/{len(other_states)} = "
          f"{100*ot_ji/len(other_states):.1f}%")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    with open(STATES_PATH) as f:
        states = json.load(f)

    # §II: Torus
    cells = compute_torus_cells(states)
    flow = build_torus_flow_json(cells)
    print_torus_analysis(flow)

    # §III: Arc classification
    for s in states:
        s["arc_type"] = classify_arc(s["relation_vector"])
    print_arc_analysis(states)

    # Write outputs
    with open(STATES_PATH, "w") as f:
        json.dump(states, f, ensure_ascii=False, indent=2)
    print(f"\nUpdated {STATES_PATH.name} with mh_torus_cell, arc_type")

    with open(HERE / "mh_torus_flow.json", "w") as f:
        json.dump(flow, f, ensure_ascii=False, indent=2)
    print(f"Written mh_torus_flow.json ({len(flow)} cells)")

    arcs = build_arcs_json(states)
    with open(HERE / "mh_arcs.json", "w") as f:
        json.dump(arcs, f, ensure_ascii=False, indent=2)
    print(f"Written mh_arcs.json")


if __name__ == "__main__":
    main()
