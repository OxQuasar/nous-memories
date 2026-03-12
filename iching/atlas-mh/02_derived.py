#!/usr/bin/env python3
"""
02_derived: Add derived coordinates and valence markers to mh_states.json.

Adds: ti_party_count, yong_party_count, arc_valence, ben_bian_shift,
      valence_markers, basin.
"""

import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ATLAS_PATH = HERE.parent / "atlas" / "atlas.json"
YAOCI_PATH = HERE.parent.parent / "texts" / "iching" / "yaoci.json"
STATES_PATH = HERE / "mh_states.json"

VALENCE_ORDER = {"生体": 2, "体克用": 1, "比和": 0, "体生用": -1, "克体": -2}
FAVORABLE = {"比和", "生体"}
ADVERSARIAL = {"克体", "体生用"}

VALENCE_MARKERS = ["吉", "凶", "悔", "吝", "厲"]
WUJIU_PAT = re.compile(r"[无無]咎")

# ─── Data loading ───────────────────────────────────────────────────────────

def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)

def load_yaoci():
    with open(YAOCI_PATH) as f:
        return json.load(f)

def load_states():
    with open(STATES_PATH) as f:
        return json.load(f)

def build_yaoci_lookup(yaoci, atlas):
    """Map (hex_val, line_1indexed) → yaoci text."""
    # KW number → yaoci entry
    kw_to_entry = {e["number"]: e for e in yaoci["entries"]}
    # hex_val → KW number
    hex_to_kw = {int(k): v["kw_number"] for k, v in atlas.items()}

    lookup = {}
    for hex_val in range(64):
        kw = hex_to_kw[hex_val]
        entry = kw_to_entry[kw]
        for i, line_data in enumerate(entry["lines"]):
            lookup[(hex_val, i + 1)] = line_data["text"]
    return lookup


def extract_valence_markers(text):
    """Extract valence markers from 爻辭 text."""
    markers = {}
    for m in VALENCE_MARKERS:
        markers[m] = m in text
    markers["无咎"] = bool(WUJIU_PAT.search(text))
    return markers


# ─── Derived field computation ──────────────────────────────────────────────

def count_parties(state):
    """Count favorable (ti_party) and adversarial (yong_party) among 4 non-體 elements."""
    # The 4 relations: ben (用 vs 體), ti_hu, yong_hu, bian
    rels = [state["ben_relation"], state["ti_hu_relation"],
            state["yong_hu_relation"], state["bian_relation"]]
    ti_party = sum(1 for r in rels if r in FAVORABLE)
    yong_party = sum(1 for r in rels if r in ADVERSARIAL)
    return ti_party, yong_party


def classify_arc_valence(ti_party, yong_party):
    if ti_party > yong_party:
        return "favorable"
    if yong_party > ti_party:
        return "unfavorable"
    return "balanced"


def classify_ben_bian_shift(ben_rel, bian_rel):
    ben_v = VALENCE_ORDER[ben_rel]
    bian_v = VALENCE_ORDER[bian_rel]
    if bian_v > ben_v:
        return "improving"
    if bian_v < ben_v:
        return "deteriorating"
    return "stable"


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    states = load_states()
    atlas = load_atlas()
    yaoci = load_yaoci()
    yaoci_lookup = build_yaoci_lookup(yaoci, atlas)

    # Basin lookup from atlas
    basin_map = {int(k): v["basin"] for k, v in atlas.items()}

    # Enrich each state
    for s in states:
        ti_p, yong_p = count_parties(s)
        s["ti_party_count"] = ti_p
        s["yong_party_count"] = yong_p
        s["arc_valence"] = classify_arc_valence(ti_p, yong_p)
        s["ben_bian_shift"] = classify_ben_bian_shift(s["ben_relation"], s["bian_relation"])
        s["valence_markers"] = extract_valence_markers(yaoci_lookup[(s["hex_val"], s["line"])])
        s["basin"] = basin_map[s["hex_val"]]

    # Write updated states
    with open(STATES_PATH, "w") as f:
        json.dump(states, f, ensure_ascii=False, indent=2)
    print(f"Updated {len(states)} states in {STATES_PATH.name}\n")

    # ─── Analysis ───────────────────────────────────────────────────────────

    # ti_party / yong_party distribution
    print("=== Party count distributions ===")
    ti_dist = Counter(s["ti_party_count"] for s in states)
    yong_dist = Counter(s["yong_party_count"] for s in states)
    print("ti_party_count:")
    for k in range(5):
        print(f"  {k}: {ti_dist.get(k, 0)}")
    print("yong_party_count:")
    for k in range(5):
        print(f"  {k}: {yong_dist.get(k, 0)}")

    # arc_valence
    print("\n=== arc_valence ===")
    val_dist = Counter(s["arc_valence"] for s in states)
    for v in ["favorable", "balanced", "unfavorable"]:
        print(f"  {v}: {val_dist.get(v, 0)}")

    # ben_bian_shift
    print("\n=== ben_bian_shift ===")
    shift_dist = Counter(s["ben_bian_shift"] for s in states)
    for v in ["improving", "stable", "deteriorating"]:
        print(f"  {v}: {shift_dist.get(v, 0)}")

    # Cross-tab: arc_valence × basin
    print("\n=== arc_valence × basin ===")
    basins = sorted(set(s["basin"] for s in states))
    valences = ["favorable", "balanced", "unfavorable"]
    header = f"{'':15s}" + "".join(f"{b:>8s}" for b in basins) + f"{'total':>8s}"
    print(header)
    for v in valences:
        row = [sum(1 for s in states if s["arc_valence"] == v and s["basin"] == b) for b in basins]
        total = sum(row)
        print(f"{v:15s}" + "".join(f"{c:8d}" for c in row) + f"{total:8d}")
    # Totals
    totals = [sum(1 for s in states if s["basin"] == b) for b in basins]
    print(f"{'total':15s}" + "".join(f"{c:8d}" for c in totals) + f"{sum(totals):8d}")

    # Forbidden relation vectors
    realized = set(tuple(s["relation_vector"]) for s in states)
    rels = list(VALENCE_ORDER.keys())
    total_possible = len(rels) ** 4  # 5^4 = 625
    forbidden = total_possible - len(realized)
    print(f"\n=== Relation vector space ===")
    print(f"  Possible: {total_possible}")
    print(f"  Realized: {len(realized)}")
    print(f"  Forbidden: {forbidden}")

    # Valence marker summary
    print("\n=== Valence marker frequencies ===")
    marker_keys = VALENCE_MARKERS + ["无咎"]
    for m in marker_keys:
        cnt = sum(1 for s in states if s["valence_markers"].get(m, False))
        print(f"  {m}: {cnt}/{len(states)} ({100*cnt/len(states):.1f}%)")

    # Cross-tab: arc_valence × valence markers
    print("\n=== arc_valence × 吉 / 凶 rates ===")
    for v in valences:
        subset = [s for s in states if s["arc_valence"] == v]
        n = len(subset)
        ji = sum(1 for s in subset if s["valence_markers"]["吉"])
        xiong = sum(1 for s in subset if s["valence_markers"]["凶"])
        print(f"  {v:15s}: n={n:3d}, 吉={ji:3d} ({100*ji/n:.1f}%), 凶={xiong:2d} ({100*xiong/n:.1f}%)")


if __name__ == "__main__":
    main()
