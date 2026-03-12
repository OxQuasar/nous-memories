#!/usr/bin/env python3
"""
04_temporal: §IV Temporal analysis for 梅花 384-state space.

1. 先天 reachability: which (hex, line) states are reachable via calendar casting?
2. Seasonal bias on arc types: does 旺-element upper trigram bias 體 strength?

Read: mh_states.json, atlas/temporal.json
Write: mh_temporal.json
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATES_PATH = HERE / "mh_states.json"
TEMPORAL_PATH = HERE.parent / "atlas" / "temporal.json"

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

TRIGRAM_ELEMENT = {
    7: "Metal", 3: "Metal",   # Qian, Dui
    5: "Fire",                 # Li
    1: "Wood",  6: "Wood",     # Zhen, Xun
    2: "Water",                # Kan
    4: "Earth", 0: "Earth",    # Gen, Kun
}

SEASONS = ["Spring", "Summer", "Late_Summer", "Autumn", "Winter"]

# ─── 先天 reachability ─────────────────────────────────────────────────────

def compute_reachability():
    """Enumerate all (S mod 24, hour) inputs → (hex, line) states.
    S mod 24 covers lcm(8,6)=24 residues. Hour ∈ 1..12."""
    reached = set()
    input_map = defaultdict(list)  # (hex, line) → list of (S, hour) inputs

    for s in range(24):
        for hour in range(1, 13):
            total = s + hour
            upper = s % 8
            lower = total % 8
            hex_val = lower | (upper << 3)
            line = (total % 6) + 1  # 1-indexed
            state = (hex_val, line)
            reached.add(state)
            input_map[state].append((s, hour))

    # Full space
    all_states = {(h, l) for h in range(64) for l in range(1, 7)}
    unreached = all_states - reached

    return reached, unreached, input_map


def analyze_reachability(reached, unreached, input_map):
    print("=" * 70)
    print("§IV.A: 先天 384-STATE REACHABILITY")
    print("=" * 70)

    print(f"\nReachable: {len(reached)}/384")
    print(f"Unreachable: {len(unreached)}/384")

    if unreached:
        print(f"\nUnreachable states:")
        for h, l in sorted(unreached):
            print(f"  hex {h} line {l}")
    else:
        print("All 384 states reachable.")

    # Input multiplicity distribution
    mult = Counter(len(v) for v in input_map.values())
    print(f"\nInput multiplicity (how many (S,hour) pairs produce each state):")
    for k in sorted(mult):
        print(f"  {k} inputs: {mult[k]} states")

    # Per-hexagram: how many lines reachable?
    hex_lines = defaultdict(set)
    for h, l in reached:
        hex_lines[h].add(l)
    line_coverage = Counter(len(v) for v in hex_lines.values())
    print(f"\nPer-hexagram line coverage:")
    for k in sorted(line_coverage):
        print(f"  {k}/6 lines: {line_coverage[k]} hexagrams")

    # Any hexagram with < 6 lines?
    partial = {h: lines for h, lines in hex_lines.items() if len(lines) < 6}
    if partial:
        print(f"\nHexagrams with partial line coverage:")
        for h, lines in sorted(partial.items()):
            missing = set(range(1, 7)) - lines
            print(f"  hex {h}: missing lines {sorted(missing)}")

    return {
        "n_reachable": len(reached),
        "n_unreachable": len(unreached),
        "unreachable_states": sorted(list(unreached)),
        "multiplicity_distribution": {str(k): v for k, v in sorted(mult.items())},
        "full_coverage_hexagrams": sum(1 for v in hex_lines.values() if len(v) == 6),
    }


# ─── Seasonal bias ─────────────────────────────────────────────────────────

def analyze_seasonal_bias(states, temporal):
    print(f"\n{'=' * 70}")
    print("§IV.B: SEASONAL BIAS ON ARC TYPES")
    print("=" * 70)

    seasons_data = temporal["seasons"]
    # State lookup by (hex, line)
    state_by_key = {(s["hex_val"], s["line"]): s for s in states}

    # For each season: which elements are 旺/相 (strong)?
    # When upper trigram is 旺-element, what happens to 體?
    print(f"\nSeason → 旺/相 elements:")
    for sn in SEASONS:
        sd = seasons_data[sn]
        wang = sd["strengths"]["旺"]
        xiang = sd["strengths"]["相"]
        print(f"  {sn:12s}: 旺={wang}, 相={xiang}")

    # For each season, check: among states where upper trigram matches 旺 element,
    # what is the 體 element distribution? (體=upper when 動 in lower)
    print(f"\nWhen upper trigram is seasonally 旺:")
    print(f"  → Lines 1-3: 體=upper (strong) → 體 is 旺")
    print(f"  → Lines 4-6: 體=lower (varies) → 體 may or may not be 旺")

    season_arc_cross = defaultdict(Counter)
    season_ti_strength = defaultdict(Counter)

    for sn in SEASONS:
        sd = seasons_data[sn]
        wang = sd["strengths"]["旺"]
        active = sd["active_elements"]  # [旺, 相]

        for s in states:
            # Determine 體's seasonal strength
            ti_elem = s["ti_element"]
            # Find ti_elem's seasonal status
            for status, elem in sd["strengths"].items():
                if elem == ti_elem:
                    ti_strength = status
                    break

            season_ti_strength[sn][ti_strength] += 1
            season_arc_cross[sn][s["arc_type"]] += 1

    # Ti seasonal strength distribution
    strength_order = ["旺", "相", "休", "囚", "死"]
    print(f"\n體's seasonal strength distribution (all 384 states × 5 seasons):")
    print(f"{'Season':12s}", end="")
    for st in strength_order:
        print(f"{st:>8s}", end="")
    print()
    for sn in SEASONS:
        print(f"{sn:12s}", end="")
        for st in strength_order:
            print(f"{season_ti_strength[sn][st]:8d}", end="")
        print()

    # Since 體 is determined by hex structure not season, the distribution
    # is the same for every season (体 element doesn't change with season).
    # What changes is the STRENGTH assigned to each element.
    # So we need to ask: is the 旺 element overrepresented among 體?

    # Check: for states where 體 is 旺, what arc types?
    print(f"\nArc type when 體 is 旺 vs 體 is 死 (by season):")
    arc_types = ["stable_neutral", "rescued", "betrayed", "improving",
                 "deteriorating", "stable_favorable", "stable_unfavorable", "mixed"]

    for sn in SEASONS:
        sd = seasons_data[sn]
        wang_elem = sd["strengths"]["旺"]
        si_elem = sd["strengths"]["死"]

        wang_states = [s for s in states if s["ti_element"] == wang_elem]
        si_states = [s for s in states if s["ti_element"] == si_elem]

        wang_arcs = Counter(s["arc_type"] for s in wang_states)
        si_arcs = Counter(s["arc_type"] for s in si_states)

        print(f"\n  {sn} (旺={wang_elem}, 死={si_elem}):")
        print(f"    {'arc_type':22s} {'旺':>6s} {'%':>6s} {'死':>6s} {'%':>6s}")
        for at in arc_types:
            wc = wang_arcs.get(at, 0)
            sc = si_arcs.get(at, 0)
            wn = len(wang_states) or 1
            sn2 = len(si_states) or 1
            if wc > 0 or sc > 0:
                print(f"    {at:22s} {wc:6d} {100*wc/wn:5.1f}% {sc:6d} {100*sc/sn2:5.1f}%")

    # Key question: does 旺 体 bias toward favorable arcs?
    print(f"\n{'=' * 70}")
    print("SEASONAL SUMMARY: 旺 vs 死 favorability")
    print("=" * 70)

    for sn in SEASONS:
        sd = seasons_data[sn]
        wang_elem = sd["strengths"]["旺"]
        si_elem = sd["strengths"]["死"]

        wang_states = [s for s in states if s["ti_element"] == wang_elem]
        si_states = [s for s in states if s["ti_element"] == si_elem]

        wang_fav = sum(1 for s in wang_states if s["arc_valence"] == "favorable")
        si_fav = sum(1 for s in si_states if s["arc_valence"] == "favorable")
        wang_unfav = sum(1 for s in wang_states if s["arc_valence"] == "unfavorable")
        si_unfav = sum(1 for s in si_states if s["arc_valence"] == "unfavorable")

        wn = len(wang_states) or 1
        sn2 = len(si_states) or 1
        print(f"  {sn:12s} 旺={wang_elem:6s} (n={len(wang_states):3d}): "
              f"fav={100*wang_fav/wn:5.1f}% unfav={100*wang_unfav/wn:5.1f}%  |  "
              f"死={si_elem:6s} (n={len(si_states):3d}): "
              f"fav={100*si_fav/sn2:5.1f}% unfav={100*si_unfav/sn2:5.1f}%")

    print(f"\n  NOTE: arc_valence is structurally determined (hex+line), NOT seasonal.")
    print(f"  Seasons affect 衰旺 overlay, not the underlying 生克 relations.")
    print(f"  A 旺-體 state with 克体 arc is still algebraically unfavorable —")
    print(f"  but 旺 gives 體 resilience to survive the adversity.")

    return {
        "ti_seasonal_strength": {sn: dict(v) for sn, v in season_ti_strength.items()},
        "season_arc_cross": {sn: dict(v) for sn, v in season_arc_cross.items()},
    }


# ─── 先天 casting distribution over 384 states ────────────────────────────

def compute_casting_distribution(reached, input_map):
    """Analyze non-uniformity of 先天 casting over the 384 states."""
    print(f"\n{'=' * 70}")
    print("§IV.C: 先天 CASTING DISTRIBUTION")
    print("=" * 70)

    weights = {k: len(v) for k, v in input_map.items()}
    total_inputs = sum(weights.values())
    expected = total_inputs / 384

    print(f"\nTotal (S mod 24 × hour) inputs: {total_inputs}")
    print(f"Expected per state (uniform): {expected:.2f}")

    # χ² test
    chi2 = sum((w - expected) ** 2 / expected for w in weights.values())
    # Add 0-weight states
    n_zero = 384 - len(weights)
    chi2 += n_zero * expected  # (0 - expected)^2 / expected = expected
    df = 383
    print(f"χ² = {chi2:.1f} (df={df})")
    if chi2 < df * 1.5:
        print("  → Reasonably uniform (χ² ≈ df)")
    elif chi2 < df * 2:
        print("  → Moderately non-uniform")
    else:
        print("  → Highly non-uniform")

    # Per-line distribution
    line_weights = defaultdict(int)
    for (h, l), w in weights.items():
        line_weights[l] += w
    print(f"\nPer-line totals:")
    for l in range(1, 7):
        print(f"  line {l}: {line_weights[l]} inputs ({100*line_weights[l]/total_inputs:.1f}%)")

    return {
        "total_inputs": total_inputs,
        "chi2": chi2,
        "per_line_totals": dict(line_weights),
    }


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    with open(STATES_PATH) as f:
        states = json.load(f)
    with open(TEMPORAL_PATH) as f:
        temporal = json.load(f)

    # §IV.A: Reachability
    reached, unreached, input_map = compute_reachability()
    reach_data = analyze_reachability(reached, unreached, input_map)

    # §IV.C: Distribution
    dist_data = compute_casting_distribution(reached, input_map)

    # §IV.B: Seasonal bias
    seasonal_data = analyze_seasonal_bias(states, temporal)

    # Write output
    output = {
        "reachability": reach_data,
        "casting_distribution": dist_data,
        "seasonal_bias": seasonal_data,
    }
    out_path = HERE / "mh_temporal.json"
    with open(out_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nWritten {out_path.name}")


if __name__ == "__main__":
    main()
