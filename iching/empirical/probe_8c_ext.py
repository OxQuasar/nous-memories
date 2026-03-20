#!/usr/bin/env python3
"""
Probe 8c-ext: Arc Symmetry Under Three 体克用 Modes.

Tests whether the arc symmetries (rescued=betrayed, improving=deteriorating)
hold when 体克用 is revalued across the three domain modes from probe 8c:
  - Competition (standard): 体克用 = +1
  - Manifestation: 体克用 = 0 (delayed/ambiguous)
  - Nurture: 体克用 = -1
  - Nurture-full (生產): 体克用 = -1, 体生用 = +1
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ─── Constants ───────────────────────────────────────────────────────────────

ARC_TYPES = [
    "stable_neutral", "rescued", "betrayed", "improving",
    "deteriorating", "stable_favorable", "stable_unfavorable", "mixed",
]

# Four valence templates
# Each maps relation_name → integer valence
TEMPLATES = {
    "competition": {
        "生体": 2, "体克用": 1, "比和": 0, "体生用": -1, "克体": -2,
    },
    "manifestation": {
        "生体": 2, "体克用": 0, "比和": 0, "体生用": -1, "克体": -2,
    },
    "nurture": {
        "生体": 2, "体克用": -1, "比和": 0, "体生用": -1, "克体": -2,
    },
    "nurture_full": {
        "生体": 2, "体克用": -1, "比和": 0, "体生用": 1, "克体": -2,
    },
}

# ─── Arc classifier (identical logic to 03_torus_arcs.py) ────────────────────

def classify_arc(vals):
    """Classify a 4-element valence list into arc type."""
    ben_v, ti_hu_v, yong_hu_v, bian_v = vals

    if all(v == 0 for v in vals):
        return "stable_neutral"
    if ben_v < 0 and bian_v > 0:
        return "rescued"
    if ben_v > 0 and bian_v < 0:
        return "betrayed"
    if bian_v > ben_v and bian_v > 0:
        return "improving"
    if bian_v < ben_v and bian_v < 0:
        return "deteriorating"
    if all(v >= 0 for v in vals) and any(v > 0 for v in vals):
        return "stable_favorable"
    if all(v <= 0 for v in vals) and any(v < 0 for v in vals):
        return "stable_unfavorable"
    return "mixed"


# ─── Analysis ────────────────────────────────────────────────────────────────

def load_states():
    with open(HERE.parent / "atlas-mh" / "mh_states.json") as f:
        return json.load(f)


def classify_under_template(states, template_name):
    """Reclassify all states under a given valence template."""
    vmap = TEMPLATES[template_name]
    results = []
    for s in states:
        rv = s["relation_vector"]
        vals = [vmap[r] for r in rv]
        arc = classify_arc(vals)
        results.append({
            "hex_val": s["hex_val"],
            "line": s["line"],
            "relation_vector": rv,
            "valence_vector": vals,
            "arc_type": arc,
            "original_arc": s["arc_type"],
        })
    return results


def arc_distribution(classified):
    """Count arc types."""
    return Counter(r["arc_type"] for r in classified)


def transition_matrix(classified):
    """Count (original_arc → new_arc) transitions."""
    matrix = Counter()
    for r in classified:
        matrix[(r["original_arc"], r["arc_type"])] += 1
    return matrix


def symmetry_check(dist):
    """Check rescued=betrayed, improving=deteriorating."""
    return {
        "rescued": dist.get("rescued", 0),
        "betrayed": dist.get("betrayed", 0),
        "rescued_eq_betrayed": dist.get("rescued", 0) == dist.get("betrayed", 0),
        "improving": dist.get("improving", 0),
        "deteriorating": dist.get("deteriorating", 0),
        "improving_eq_deteriorating": dist.get("improving", 0) == dist.get("deteriorating", 0),
    }


def stable_neutral_check(classified):
    """Verify the 6 stable_neutral states survive."""
    sn = [r for r in classified if r["original_arc"] == "stable_neutral"]
    survived = sum(1 for r in sn if r["arc_type"] == "stable_neutral")
    return {"total": len(sn), "survived": survived,
            "all_survive": survived == len(sn)}


def fav_unfav_flips(classified):
    """States that flip between favorable and unfavorable families."""
    fav_types = {"stable_favorable", "rescued", "improving"}
    unfav_types = {"stable_unfavorable", "betrayed", "deteriorating"}

    fav_to_unfav = []
    unfav_to_fav = []
    for r in classified:
        orig = r["original_arc"]
        new = r["arc_type"]
        if orig in fav_types and new in unfav_types:
            fav_to_unfav.append(r)
        elif orig in unfav_types and new in fav_types:
            unfav_to_fav.append(r)
    return fav_to_unfav, unfav_to_fav


# ─── Output ──────────────────────────────────────────────────────────────────

def format_results(states, all_classified):
    lines = []
    w = lines.append

    w("# Probe 8c-ext: Arc Symmetry Under Three 体克用 Modes\n")
    w("Tests whether the arc symmetries from atlas-mh hold when 体克用 is revalued.\n")

    # Template definitions
    w("## 1. Valence Templates\n")
    w("| Relation | Competition | Manifestation | Nurture | Nurture-full |")
    w("|----------|-------------|---------------|---------|-------------|")
    for rel in ["生体", "体克用", "比和", "体生用", "克体"]:
        row = f"| {rel} |"
        for t in ["competition", "manifestation", "nurture", "nurture_full"]:
            row += f" {TEMPLATES[t][rel]:+d} |"
        w(row)
    w("")
    w("**Competition:** Standard atlas-mh (14/17 domains)")
    w("**Manifestation:** 体克用 = delayed/ambiguous (5 domains: 婚姻, 求謀, 求名, 行人, 失物)")
    w("**Nurture:** 体克用 = unfavorable (2 domains: 飲食, 生產)")
    w("**Nurture-full:** Additionally 体生用 inverted (1 domain: 生產)\n")

    # Arc distributions
    w("## 2. Arc Type Distributions\n")
    w("| Arc type | Competition | Manifestation | Nurture | Nurture-full |")
    w("|----------|-------------|---------------|---------|-------------|")
    for at in ARC_TYPES:
        row = f"| {at} |"
        for tname in ["competition", "manifestation", "nurture", "nurture_full"]:
            dist = arc_distribution(all_classified[tname])
            row += f" {dist.get(at, 0):>4d} |"
        w(row)

    # Totals
    row = "| **total** |"
    for tname in ["competition", "manifestation", "nurture", "nurture_full"]:
        row += f" {sum(arc_distribution(all_classified[tname]).values()):>4d} |"
    w(row)
    w("")

    # Symmetry checks
    w("## 3. Symmetry Checks\n")
    w("| Template | rescued | betrayed | R=B? | improving | deteriorating | I=D? |")
    w("|----------|---------|----------|------|-----------|---------------|------|")
    for tname in TEMPLATES:
        sc = symmetry_check(arc_distribution(all_classified[tname]))
        rb = "✓" if sc["rescued_eq_betrayed"] else "✗"
        id_ = "✓" if sc["improving_eq_deteriorating"] else "✗"
        w(f"| {tname} | {sc['rescued']} | {sc['betrayed']} | {rb} | "
          f"{sc['improving']} | {sc['deteriorating']} | {id_} |")
    w("")

    # Analyze symmetry breaking
    for tname in TEMPLATES:
        sc = symmetry_check(arc_distribution(all_classified[tname]))
        if not sc["rescued_eq_betrayed"] or not sc["improving_eq_deteriorating"]:
            w(f"### Symmetry breaking in {tname}\n")
            dist = arc_distribution(all_classified[tname])

            # Show what changed
            orig_dist = arc_distribution(all_classified["competition"])
            w("| Arc type | Competition | {0} | Delta |".format(tname))
            w("|----------|-------------|---------|-------|")
            for at in ARC_TYPES:
                o = orig_dist.get(at, 0)
                n = dist.get(at, 0)
                d = n - o
                if d != 0:
                    w(f"| {at} | {o} | {n} | {d:+d} |")
            w("")

    # Stable neutral check
    w("## 4. Stable Neutral Invariance\n")
    w("| Template | 6 stable_neutral states survive? |")
    w("|----------|---------------------------------|")
    for tname in TEMPLATES:
        snc = stable_neutral_check(all_classified[tname])
        mark = "✓ all 6" if snc["all_survive"] else f"✗ {snc['survived']}/6"
        w(f"| {tname} | {mark} |")
    w("")

    # Favorable ↔ Unfavorable flips
    w("## 5. Favorable ↔ Unfavorable Flips\n")
    for tname in TEMPLATES:
        if tname == "competition":
            continue
        f2u, u2f = fav_unfav_flips(all_classified[tname])
        w(f"### {tname}")
        w(f"- Favorable → Unfavorable: **{len(f2u)}** states")
        w(f"- Unfavorable → Favorable: **{len(u2f)}** states")

        if f2u:
            w(f"\n  Sample favorable→unfavorable transitions:")
            for r in f2u[:5]:
                w(f"  - hex={r['hex_val']:2d} line={r['line']}: "
                  f"{r['original_arc']} → {r['arc_type']} "
                  f"(rv={r['relation_vector']}, vals={r['valence_vector']})")
        if u2f:
            w(f"\n  Sample unfavorable→favorable transitions:")
            for r in u2f[:5]:
                w(f"  - hex={r['hex_val']:2d} line={r['line']}: "
                  f"{r['original_arc']} → {r['arc_type']} "
                  f"(rv={r['relation_vector']}, vals={r['valence_vector']})")
        w("")

    # Transition matrices
    w("## 6. Arc Type Transition Matrices\n")
    w("Shows how arc types change from competition (standard) to each alternative template.\n")
    for tname in ["manifestation", "nurture", "nurture_full"]:
        w(f"### Competition → {tname}\n")
        tm = transition_matrix(all_classified[tname])

        # Get all arc types that appear
        orig_types = sorted(set(k[0] for k in tm))
        new_types = sorted(set(k[1] for k in tm))

        # Total changed
        changed = sum(v for (o, n), v in tm.items() if o != n)
        unchanged = sum(v for (o, n), v in tm.items() if o == n)
        w(f"**{changed} states changed** arc type, {unchanged} unchanged.\n")

        header = "| from \\ to |" + "|".join(f" {at[:8]:>8s} " for at in ARC_TYPES) + "| total |"
        w(header)
        w("|" + "---|" * (len(ARC_TYPES) + 2))
        for orig in ARC_TYPES:
            row_total = sum(tm.get((orig, new), 0) for new in ARC_TYPES)
            if row_total == 0:
                continue
            row = f"| {orig[:12]:12s} |"
            for new in ARC_TYPES:
                c = tm.get((orig, new), 0)
                if c == 0:
                    row += "          |"
                elif orig == new:
                    row += f" **{c:>4d}** |"
                else:
                    row += f"    {c:>4d}  |"
            row += f" {row_total:>5d} |"
            w(row)
        w("")

    # Deep dive: what relation vectors involve 体克用 at each position?
    w("## 7. 体克用 Position Analysis\n")
    w("Which vector positions contain 体克用, and how reclassification redistributes them.\n")

    # Count how many states have 体克用 at each position
    for pos, label in enumerate(["ben", "ti_hu", "yong_hu", "bian"]):
        count = sum(1 for s in states if s["relation_vector"][pos] == "体克用")
        w(f"- Position {pos} ({label}): **{count}** states contain 体克用")
    w("")

    # Critical subset: states where 体克用 appears at ben or bian (the arc endpoints)
    ben_tky = [s for s in states if s["relation_vector"][0] == "体克用"]
    bian_tky = [s for s in states if s["relation_vector"][3] == "体克用"]
    both_tky = [s for s in states
                if s["relation_vector"][0] == "体克用" and s["relation_vector"][3] == "体克用"]

    w(f"- 体克用 at ben (start): {len(ben_tky)} states")
    w(f"- 体克用 at bian (end): {len(bian_tky)} states")
    w(f"- 体克用 at both endpoints: {len(both_tky)} states")
    w("")

    w("These are the states most affected by revaluation, since the arc classifier "
      "primarily uses ben (start) and bian (end) valences.\n")

    # Show arc distribution for the 体克用-at-ben subset under each template
    w("### Arc types for states with 体克用 at ben position\n")
    w("| Arc type | Competition | Manifestation | Nurture | Nurture-full |")
    w("|----------|-------------|---------------|---------|-------------|")
    for at in ARC_TYPES:
        row = f"| {at} |"
        for tname in TEMPLATES:
            count = sum(1 for r in all_classified[tname]
                        if r["relation_vector"][0] == "体克用" and r["arc_type"] == at)
            row += f" {count:>4d} |"
        w(row)
    w("")

    # Summary
    w("## 8. Summary\n")

    comp_sc = symmetry_check(arc_distribution(all_classified["competition"]))
    man_sc = symmetry_check(arc_distribution(all_classified["manifestation"]))
    nur_sc = symmetry_check(arc_distribution(all_classified["nurture"]))
    nf_sc = symmetry_check(arc_distribution(all_classified["nurture_full"]))

    all_symmetric = all(
        sc["rescued_eq_betrayed"] and sc["improving_eq_deteriorating"]
        for sc in [comp_sc, man_sc, nur_sc, nf_sc]
    )
    any_broken = not all_symmetric

    if all_symmetric:
        w("**All four templates preserve both symmetries (R=B, I=D).**\n")
        w("The arc symmetries are structural invariants of the hexagram↔moving-line system, "
          "not artifacts of the particular valence assigned to 体克用.\n")
    else:
        w("**Symmetry is broken under some templates.**\n")
        for tname, sc in [("competition", comp_sc), ("manifestation", man_sc),
                          ("nurture", nur_sc), ("nurture_full", nf_sc)]:
            rb = "✓" if sc["rescued_eq_betrayed"] else "✗ BROKEN"
            id_ = "✓" if sc["improving_eq_deteriorating"] else "✗ BROKEN"
            w(f"- {tname}: R=B {rb}, I=D {id_}")
        w("")

    # Check stable_neutral
    all_sn_ok = all(
        stable_neutral_check(all_classified[t])["all_survive"]
        for t in TEMPLATES
    )
    if all_sn_ok:
        w("**All 6 stable_neutral states survive under every template** — "
          "they have all-比和 vectors, which map to all-zero valence regardless of 体克用 mode.\n")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PROBE 8c-ext: ARC SYMMETRY UNDER THREE 体克用 MODES")
    print("=" * 70)

    states = load_states()
    print(f"Loaded {len(states)} states")

    all_classified = {}
    for tname in TEMPLATES:
        classified = classify_under_template(states, tname)
        all_classified[tname] = classified
        dist = arc_distribution(classified)
        sc = symmetry_check(dist)

        print(f"\n── {tname} ──")
        for at in ARC_TYPES:
            print(f"  {at:22s}: {dist.get(at, 0):>4d}")
        print(f"  R=B: {sc['rescued_eq_betrayed']}, I=D: {sc['improving_eq_deteriorating']}")

        # Changes from competition
        if tname != "competition":
            changed = sum(1 for c, r in zip(all_classified["competition"], classified)
                          if c["arc_type"] != r["arc_type"])
            print(f"  States changed: {changed}/384")

    # Stable neutral check
    print("\n── Stable Neutral ──")
    for tname in TEMPLATES:
        snc = stable_neutral_check(all_classified[tname])
        print(f"  {tname}: {snc['survived']}/{snc['total']} survive")

    # Write
    md = format_results(states, all_classified)
    out_path = HERE / "probe_8c_ext_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
