#!/usr/bin/env python3
"""
Probe 8c-ext2: I=D Under Arbitrary Symmetric Valence Alphabets.

Tests whether improving=deteriorating (I=D) symmetry holds for all
"symmetric" alphabets parameterized by (a, b):
  V(生体)=+a, V(克体)=-a, V(体克用)=+b, V(体生用)=-b, V(比和)=0

Also examines the complement involution σ: (hex,line)→(63-hex,line)
which maps 体克用↔克体, 体生用↔生体, 比和↔比和.

Key question: σ negates SIGNS of all valence entries but NOT magnitudes
(when a≠b). Under what conditions does I=D hold?
"""

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ─── Arc classifier (from 03_torus_arcs.py) ──────────────────────────────────

ARC_TYPES = [
    "stable_neutral", "rescued", "betrayed", "improving",
    "deteriorating", "stable_favorable", "stable_unfavorable", "mixed",
]


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


# ─── Data ────────────────────────────────────────────────────────────────────

def load_states():
    with open(HERE.parent / "atlas-mh" / "mh_states.json") as f:
        return json.load(f)


SIGMA_REL = {
    "体克用": "克体", "克体": "体克用",
    "体生用": "生体", "生体": "体生用",
    "比和": "比和",
}


def make_vmap(a, b):
    """Build valence map for symmetric alphabet (a, b)."""
    return {"生体": a, "克体": -a, "体克用": b, "体生用": -b, "比和": 0}


def classify_all(states, vmap):
    """Classify all states under a valence map. Returns list of arc types."""
    arcs = []
    for s in states:
        vals = [vmap[r] for r in s["relation_vector"]]
        arcs.append(classify_arc(vals))
    return arcs


def arc_counts(arcs):
    return Counter(arcs)


def id_check(arcs):
    c = Counter(arcs)
    return c.get("improving", 0) == c.get("deteriorating", 0)


def rb_check(arcs):
    c = Counter(arcs)
    return c.get("rescued", 0) == c.get("betrayed", 0)


# ─── Part 1: Symmetric alphabet sweep ────────────────────────────────────────

def sweep_symmetric(states):
    """Test (a, b) grid for I=D and R=B."""
    pairs = [(1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (2, 2), (3, 2), (2, 3),
             (5, 1), (1, 5), (3, 3), (4, 1), (1, 4), (4, 2), (2, 4), (5, 5)]
    results = []
    for a, b in pairs:
        vmap = make_vmap(a, b)
        arcs = classify_all(states, vmap)
        c = arc_counts(arcs)
        results.append({
            "a": a, "b": b,
            "improving": c.get("improving", 0),
            "deteriorating": c.get("deteriorating", 0),
            "rescued": c.get("rescued", 0),
            "betrayed": c.get("betrayed", 0),
            "id_holds": id_check(arcs),
            "rb_holds": rb_check(arcs),
            "counts": {at: c.get(at, 0) for at in ARC_TYPES},
        })
    return results


# ─── Part 2: Perturbation of V(体克用) ────────────────────────────────────────

def perturbation_sweep(states):
    """Fix a=2, others standard. Slide V(体克用) from +2 to -2 in 0.5 steps."""
    results = []
    for step in range(-4, 5):  # -2.0 to +2.0 in 0.5 steps
        v_tky = step * 0.5
        vmap = {"生体": 2, "克体": -2, "体克用": v_tky, "体生用": -1, "比和": 0}
        arcs = classify_all(states, vmap)
        c = arc_counts(arcs)
        results.append({
            "v_tky": v_tky,
            "improving": c.get("improving", 0),
            "deteriorating": c.get("deteriorating", 0),
            "id_holds": id_check(arcs),
            "delta_id": c.get("improving", 0) - c.get("deteriorating", 0),
            "rescued": c.get("rescued", 0),
            "betrayed": c.get("betrayed", 0),
            "rb_holds": rb_check(arcs),
        })
    return results


# ─── Part 3: Complement pairing analysis ─────────────────────────────────────

def complement_analysis(states):
    """Check σ-pairing properties under various alphabets."""
    by_key = {(s["hex_val"], s["line"]): s for s in states}

    results = {}
    for label, a, b in [("competition", 2, 1), ("equal", 2, 2), ("inverse", 1, 2)]:
        vmap = make_vmap(a, b)
        negates_total = 0
        negates_per_position = [0, 0, 0, 0]
        negates_signs = 0
        same_magnitude_different_sign = 0
        total_pairs = 0

        improving_maps_to = Counter()
        deteriorating_maps_to = Counter()

        for s in states:
            h, l = s["hex_val"], s["line"]
            ch = 63 - h
            partner = by_key[(ch, l)]

            vals = [vmap[r] for r in s["relation_vector"]]
            pvals = [vmap[r] for r in partner["relation_vector"]]

            arc_s = classify_arc(vals)
            arc_p = classify_arc(pvals)

            if arc_s == "improving":
                improving_maps_to[arc_p] += 1
            if arc_s == "deteriorating":
                deteriorating_maps_to[arc_p] += 1

            total_pairs += 1

            # Check if σ negates the total
            v_total = sum(vals)
            p_total = sum(pvals)
            if p_total == -v_total:
                negates_total += 1

            # Check per-position negation
            for i in range(4):
                if pvals[i] == -vals[i]:
                    negates_per_position[i] += 1

            # Check sign negation (all positions)
            if all((v > 0 and p < 0) or (v < 0 and p > 0) or (v == 0 and p == 0)
                   for v, p in zip(vals, pvals)):
                negates_signs += 1

        results[label] = {
            "a": a, "b": b,
            "negates_total": negates_total,
            "negates_per_position": negates_per_position,
            "negates_signs": negates_signs,
            "total_pairs": total_pairs,
            "improving_maps_to": dict(improving_maps_to),
            "deteriorating_maps_to": dict(deteriorating_maps_to),
        }

    return results


# ─── Part 4: The key test — true negation vs. sign-only negation ─────────────

def negation_test(states):
    """
    Under a=b (true negation), σ negates each valence exactly.
    Under a≠b, σ flips signs but changes magnitudes.
    Check I=D under both.
    """
    results = []

    # Equal weights: a=b for various values
    for v in [1, 2, 3, 5]:
        vmap = make_vmap(v, v)
        arcs = classify_all(states, vmap)
        c = arc_counts(arcs)
        results.append({
            "type": "equal", "a": v, "b": v,
            "id_holds": id_check(arcs),
            "rb_holds": rb_check(arcs),
            "I": c.get("improving", 0), "D": c.get("deteriorating", 0),
            "R": c.get("rescued", 0), "B": c.get("betrayed", 0),
        })

    # Unequal weights
    for a, b in [(2, 1), (1, 2), (3, 1), (1, 3), (3, 2), (2, 3),
                 (5, 1), (1, 5), (10, 1), (1, 10)]:
        vmap = make_vmap(a, b)
        arcs = classify_all(states, vmap)
        c = arc_counts(arcs)
        results.append({
            "type": "unequal", "a": a, "b": b,
            "id_holds": id_check(arcs),
            "rb_holds": rb_check(arcs),
            "I": c.get("improving", 0), "D": c.get("deteriorating", 0),
            "R": c.get("rescued", 0), "B": c.get("betrayed", 0),
        })

    return results


# ─── Output ──────────────────────────────────────────────────────────────────

def format_results(states, sweep, perturb, complement, negation):
    lines = []
    w = lines.append

    w("# Probe 8c-ext2: I=D Under Arbitrary Symmetric Valence Alphabets\n")

    # ── Part 1 ──
    w("## 1. Symmetric Alphabet Sweep\n")
    w("Alphabet: V(生体)=+a, V(克体)=-a, V(体克用)=+b, V(体生用)=-b, V(比和)=0\n")
    w("| a | b | a=b? | I | D | I=D? | R | B | R=B? |")
    w("|---|---|------|---|---|------|---|---|------|")
    for r in sweep:
        eq = "✓" if r["a"] == r["b"] else ""
        id_mark = "✓" if r["id_holds"] else "✗"
        rb_mark = "✓" if r["rb_holds"] else "✗"
        w(f"| {r['a']} | {r['b']} | {eq} | {r['improving']} | {r['deteriorating']} | {id_mark} "
          f"| {r['rescued']} | {r['betrayed']} | {rb_mark} |")
    w("")

    # Count how many hold
    id_holds_all = all(r["id_holds"] for r in sweep)
    id_holds_eq = all(r["id_holds"] for r in sweep if r["a"] == r["b"])
    id_holds_neq = all(r["id_holds"] for r in sweep if r["a"] != r["b"])
    rb_holds_all = all(r["rb_holds"] for r in sweep)

    w(f"**R=B holds for all tested (a,b):** {rb_holds_all}")
    w(f"**I=D holds for a=b:** {id_holds_eq}")
    w(f"**I=D holds for a≠b:** {id_holds_neq}")
    w(f"**I=D holds universally:** {id_holds_all}\n")

    # ── Part 2 ──
    w("## 2. Perturbation of V(体克用)\n")
    w("Fixed: V(生体)=+2, V(克体)=-2, V(体生用)=-1, V(比和)=0")
    w("Slide V(体克用) from -2.0 to +2.0:\n")
    w("| V(体克用) | I | D | I-D | I=D? | R | B | R=B? |")
    w("|-----------|---|---|-----|------|---|---|------|")
    for r in perturb:
        id_mark = "✓" if r["id_holds"] else "✗"
        rb_mark = "✓" if r["rb_holds"] else "✗"
        w(f"| {r['v_tky']:+5.1f} | {r['improving']:>3d} | {r['deteriorating']:>3d} "
          f"| {r['delta_id']:+4d} | {id_mark} | {r['rescued']:>3d} | {r['betrayed']:>3d} | {rb_mark} |")
    w("")

    # Find break point
    id_holds_at = [(r["v_tky"], r["id_holds"]) for r in perturb]
    holds = [v for v, h in id_holds_at if h]
    breaks = [v for v, h in id_holds_at if not h]
    if holds and breaks:
        w(f"**I=D holds at V(体克用) =** {', '.join(f'{v:+.1f}' for v in holds)}")
        w(f"**I=D breaks at V(体克用) =** {', '.join(f'{v:+.1f}' for v in breaks)}\n")

    # Key observation
    w("**Key observation:** This is an asymmetric perturbation — V(体克用) varies while "
      "V(体生用) stays fixed at -1. The alphabet is only symmetric when V(体克用)=+1 "
      "(matching the original competition template where it mirrors V(体生用)=-1... but wait, "
      "in competition V(体克用)=+1 ≠ -V(克体)=+2). The alphabet is truly symmetric "
      "(V(体克用)=-V(克体)) only at V(体克用)=+2.\n")

    # ── Part 3 ──
    w("## 3. Complement Involution Analysis\n")
    w("σ: (hex, line) → (63-hex, line) maps 体克用↔克体, 体生用↔生体, 比和↔比和.\n")
    w("Under alphabet (a, b), σ maps valences: +a→-b, -a→+b, +b→-a, -b→+a, 0→0.\n")

    for label, data in complement.items():
        a, b = data["a"], data["b"]
        w(f"### {label} (a={a}, b={b})\n")

        n = data["total_pairs"]
        w(f"- σ negates V_total: **{data['negates_total']}/{n}** states "
          f"({100*data['negates_total']/n:.1f}%)")
        w(f"- σ negates all signs: **{data['negates_signs']}/{n}** states "
          f"({100*data['negates_signs']/n:.1f}%)")

        for i, lbl in enumerate(["ben", "ti_hu", "yong_hu", "bian"]):
            pct = 100 * data["negates_per_position"][i] / n
            w(f"- σ negates position {i} ({lbl}): {data['negates_per_position'][i]}/{n} ({pct:.1f}%)")

        w(f"\n**Where σ sends 'improving' states:**")
        for arc, count in sorted(data["improving_maps_to"].items()):
            w(f"  - → {arc}: {count}")

        w(f"\n**Where σ sends 'deteriorating' states:**")
        for arc, count in sorted(data["deteriorating_maps_to"].items()):
            w(f"  - → {arc}: {count}")
        w("")

    # ── Part 4 ──
    w("## 4. True Negation vs. Sign-Only Negation\n")

    w("### Equal weights (a=b): σ is exact negation\n")
    w("| a=b | I | D | I=D? | R | B | R=B? |")
    w("|-----|---|---|------|---|---|------|")
    for r in negation:
        if r["type"] != "equal":
            continue
        id_mark = "✓" if r["id_holds"] else "✗"
        rb_mark = "✓" if r["rb_holds"] else "✗"
        w(f"| {r['a']} | {r['I']} | {r['D']} | {id_mark} | {r['R']} | {r['B']} | {rb_mark} |")
    w("")

    w("### Unequal weights (a≠b): σ flips signs but changes magnitudes\n")
    w("| a | b | I | D | I=D? | R | B | R=B? |")
    w("|---|---|---|---|------|---|---|------|")
    for r in negation:
        if r["type"] != "unequal":
            continue
        id_mark = "✓" if r["id_holds"] else "✗"
        rb_mark = "✓" if r["rb_holds"] else "✗"
        w(f"| {r['a']} | {r['b']} | {r['I']} | {r['D']} | {id_mark} | {r['R']} | {r['B']} | {rb_mark} |")
    w("")

    # Check if equal always works
    eq_all_id = all(r["id_holds"] for r in negation if r["type"] == "equal")
    neq_all_id = all(r["id_holds"] for r in negation if r["type"] == "unequal")
    w(f"**Equal weights (a=b) — I=D always holds:** {eq_all_id}")
    w(f"**Unequal weights (a≠b) — I=D always holds:** {neq_all_id}\n")

    # ── Summary ──
    w("## 5. Mechanism Analysis\n")

    w("### Why R=B is universal\n")
    w("The complement involution σ always negates the **sign** of each valence entry "
      "(since a,b > 0, swapping 体克用(+b)↔克体(-a) always flips positive↔negative). "
      "The rescued/betrayed classification depends ONLY on `sign(ben_v)` and `sign(bian_v)`. "
      "Since σ flips all signs: rescued (ben<0, bian>0) ↔ betrayed (ben>0, bian<0). "
      "This holds for ANY positive (a, b).\n")

    w("### Why I=D depends on the alphabet\n")
    w("The improving/deteriorating classification depends on both the **sign** and the "
      "**relative ordering** of ben_v and bian_v:\n")
    w("- improving: bian_v > ben_v AND bian_v > 0")
    w("- deteriorating: bian_v < ben_v AND bian_v < 0\n")

    w("Under σ, a state with (ben_v=+b, bian_v=+a) maps to (ben_v'=-a, bian_v'=-b).")
    w("If a=b, then |+b|=|+a| and the ordering reversal is symmetric. "
      "If a≠b, σ can send an improving state to mixed/stable_unfavorable instead of deteriorating.\n")

    w("**Concrete example** (a=2, b=1, competition):")
    w("- State with rv=[体克用, 生体, 克体, 生体], vals=[+1, +2, -2, +2] → improving (bian=+2 > ben=+1, bian>0)")
    w("- σ partner has rv=[克体, 体生用, 体克用, 体生用], vals=[-2, -1, +1, -1]")
    w("- σ vals: bian=-1, ben=-2. bian > ben (-1>-2), but bian<0 → NOT improving. "
      "Also bian<0 but bian>ben → NOT deteriorating. → falls to stable_unfavorable or mixed.\n")

    w("Yet I=D STILL holds under competition weights. This means the states that σ "
      "\"misroutes\" (improving→non-deteriorating) are exactly compensated by states "
      "routed INTO deteriorating from other arc types.\n")

    # Determine the verdict
    if eq_all_id and neq_all_id:
        verdict = ("I=D is a **theorem of all symmetric valence alphabets**. "
                   "The compensation mechanism works for any (a, b) > 0 where "
                   "V(体克用)=-V(克体) and V(体生用)=-V(生体).")
    elif eq_all_id and not neq_all_id:
        # Find which fail
        fails = [(r["a"], r["b"]) for r in negation if r["type"] == "unequal" and not r["id_holds"]]
        holds = [(r["a"], r["b"]) for r in negation if r["type"] == "unequal" and r["id_holds"]]
        verdict = (f"I=D holds for all equal-weight alphabets (a=b) but fails for some "
                   f"unequal ones: fails at {fails}, holds at {holds}. "
                   f"It is NOT a universal theorem of symmetric alphabets.")
    else:
        verdict = "I=D behavior is complex — see detailed results above."

    w(f"### Verdict\n")
    w(verdict)
    w("")

    # Final classification
    w("### Classification of I=D\n")
    perturb_holds = all(r["id_holds"] for r in perturb)
    w("| Property | Status |")
    w("|----------|--------|")
    w(f"| R=B under all symmetric alphabets | {'✓ universal' if rb_holds_all else '✗'} |")
    w(f"| I=D under all equal-weight (a=b) | {'✓ theorem' if eq_all_id else '✗'} |")
    w(f"| I=D under all symmetric (a,b) | {'✓ theorem' if id_holds_all else '✗'} |")
    w(f"| I=D under perturbation (breaks symmetry) | {'✓ robust' if perturb_holds else '✗ breaks'} |")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PROBE 8c-ext2: I=D UNDER SYMMETRIC VALENCE ALPHABETS")
    print("=" * 70)

    states = load_states()
    print(f"Loaded {len(states)} states\n")

    # Part 1: Symmetric alphabet sweep
    print("── Part 1: Symmetric Alphabet Sweep ──")
    sweep = sweep_symmetric(states)
    for r in sweep:
        id_s = "✓" if r["id_holds"] else "✗"
        rb_s = "✓" if r["rb_holds"] else "✗"
        print(f"  a={r['a']}, b={r['b']}: I={r['improving']:3d} D={r['deteriorating']:3d} [{id_s}]  "
              f"R={r['rescued']:3d} B={r['betrayed']:3d} [{rb_s}]")

    # Part 2: Perturbation
    print("\n── Part 2: V(体克用) Perturbation ──")
    perturb = perturbation_sweep(states)
    for r in perturb:
        id_s = "✓" if r["id_holds"] else "✗"
        print(f"  V(体克用)={r['v_tky']:+5.1f}: I={r['improving']:3d} D={r['deteriorating']:3d} "
              f"Δ={r['delta_id']:+4d} [{id_s}]")

    # Part 3: Complement analysis
    print("\n── Part 3: Complement Involution ──")
    complement = complement_analysis(states)
    for label, data in complement.items():
        n = data["total_pairs"]
        print(f"  {label} (a={data['a']}, b={data['b']}): "
              f"negates_total={data['negates_total']}/{n}, "
              f"negates_signs={data['negates_signs']}/{n}")
        print(f"    improving→ {data['improving_maps_to']}")
        print(f"    deteriorating→ {data['deteriorating_maps_to']}")

    # Part 4: Negation test
    print("\n── Part 4: True Negation vs. Sign-Only ──")
    negation = negation_test(states)
    for r in negation:
        id_s = "✓" if r["id_holds"] else "✗"
        print(f"  {r['type']:7s} a={r['a']}, b={r['b']}: "
              f"I={r['I']:3d} D={r['D']:3d} [{id_s}]")

    # Write
    md = format_results(states, sweep, perturb, complement, negation)
    out_path = HERE / "probe_8c_ext2_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
