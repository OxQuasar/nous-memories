#!/usr/bin/env python3
"""
Seasonal window + 日辰 extension on Z₅×Z₅.

Part A: 5 seasonal windows — which torus cells are active/partial/dark
Part B: 60 temporal states (5 seasons × 12 day-branches) — expanded active sets
Part C: Summary statistics — active set sizes, excluded element patterns

Outputs: stdout tables + temporal_data.json
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

# ─── Constants ───────────────────────────────────────────────────────────────

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
EL_IDX = {e: i for i, e in enumerate(ELEMENTS)}
ALL_CELLS = [(a, b) for a in ELEMENTS for b in ELEMENTS]

# 生 cycle: each generates the next
SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
# 克 cycle: each overcomes the next
KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}
# Inverse maps
SHENG_INV = {v: k for k, v in SHENG.items()}  # parent: who generates me
KE_INV = {v: k for k, v in KE.items()}        # who overcomes me

# Seasons
SEASON_NAMES = ["Spring", "Summer", "Late_Summer", "Autumn", "Winter"]
SEASON_ELEMENT = {
    "Spring": "Wood", "Summer": "Fire", "Late_Summer": "Earth",
    "Autumn": "Metal", "Winter": "Water",
}
SEASON_ZH = {
    "Spring": "春", "Summer": "夏", "Late_Summer": "長夏",
    "Autumn": "秋", "Winter": "冬",
}

# 旺相休囚死 assignment
STRENGTH_LEVELS = ["旺", "相", "休", "囚", "死"]

# 12 Earthly Branches
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_ELEMENT = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood",
    "辰": "Earth", "巳": "Fire",  "午": "Fire",  "未": "Earth",
    "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}

SEPARATOR = "─" * 78


def cell_key(cell):
    return f"({cell[0]},{cell[1]})"


# ─── Seasonal system ────────────────────────────────────────────────────────

def seasonal_strength(season_elem):
    """Return {level: element} for a season with the given element."""
    return {
        "旺": season_elem,
        "相": SHENG[season_elem],
        "休": SHENG_INV[season_elem],
        "囚": KE_INV[season_elem],
        "死": KE[season_elem],
    }


def active_pair(season_elem):
    """The 2 active elements for a season: {旺, 相}."""
    return {season_elem, SHENG[season_elem]}


def classify_cell(cell, active_set):
    """Classify a cell as active/partial/dark based on active element set."""
    lo_in = cell[0] in active_set
    up_in = cell[1] in active_set
    if lo_in and up_in:
        return "active"
    elif lo_in or up_in:
        return "partial"
    else:
        return "dark"


# ─── Part A: Seasonal windows ───────────────────────────────────────────────

def seasonal_windows():
    """Compute cell status for each of the 5 seasons."""
    results = {}

    for season in SEASON_NAMES:
        se = SEASON_ELEMENT[season]
        strengths = seasonal_strength(se)
        active = active_pair(se)
        excluded = set(ELEMENTS) - active

        status = {}
        counts = Counter()
        for cell in ALL_CELLS:
            s = classify_cell(cell, active)
            status[cell] = s
            counts[s] += 1

        results[season] = {
            "season_element": se,
            "strengths": strengths,
            "active_elements": sorted(active),
            "excluded_elements": sorted(excluded),
            "cell_status": status,
            "counts": dict(counts),
        }

    return results


def print_seasonal_windows(results):
    print(f"\n{SEPARATOR}")
    print("PART A: SEASONAL WINDOWS ON Z₅×Z₅")
    print(SEPARATOR)

    # Strength table
    print(f"\n{'Season':12s} {'旺':>5} {'相':>5} {'休':>5} {'囚':>5} {'死':>5}  Active pair")
    print("─" * 65)
    for season in SEASON_NAMES:
        r = results[season]
        s = r["strengths"]
        print(f"{season:12s} {s['旺']:>5} {s['相']:>5} {s['休']:>5} {s['囚']:>5} {s['死']:>5}  "
              f"{{{', '.join(r['active_elements'])}}}")

    # Cell status grid per season
    print(f"\nCell status grid (A=active, P=partial, ·=dark):")
    LABEL = {"active": "A", "partial": "P", "dark": "·"}

    for season in SEASON_NAMES:
        r = results[season]
        print(f"\n  {season} ({SEASON_ZH[season]}, 旺={r['season_element']}):  "
              f"active={r['counts'].get('active',0)}, partial={r['counts'].get('partial',0)}, "
              f"dark={r['counts'].get('dark',0)}")
        print(f"  {'':7s}", end="")
        for up in ELEMENTS:
            print(f"{up:>6}", end="")
        print()
        for lo in ELEMENTS:
            print(f"  {lo:7s}", end="")
            for up in ELEMENTS:
                s = r["cell_status"][(lo, up)]
                print(f"{LABEL[s]:>6}", end="")
            print()

    # Verify counts
    print(f"\n{'Season':12s} {'Active':>6} {'Partial':>7} {'Dark':>5}  Expected: 4/12/9")
    print("─" * 40)
    for season in SEASON_NAMES:
        c = results[season]["counts"]
        print(f"{season:12s} {c.get('active',0):6d} {c.get('partial',0):7d} {c.get('dark',0):5d}")

    print(f"\nDiagonal sweep: as seasons rotate through 生 cycle, the 2×2 active block")
    print(f"moves diagonally across the 5×5 grid with wraparound at the torus boundary.")


# ─── Part B: 日辰 extension ─────────────────────────────────────────────────

def day_branch_data():
    """Compute day-branch promoted elements."""
    branches = {}
    for b in BRANCHES:
        de = BRANCH_ELEMENT[b]
        promotes = {de, SHENG[de]}
        branches[b] = {
            "element": de,
            "promotes": sorted(promotes),
        }
    return branches


def temporal_states(seasonal_results, branch_data):
    """Compute all 60 (season × day-branch) states."""
    states = []

    for season in SEASON_NAMES:
        sr = seasonal_results[season]
        season_active = set(sr["active_elements"])

        for branch in BRANCHES:
            bd = branch_data[branch]
            day_promotes = set(bd["promotes"])

            # Joint active set: season ∪ day
            joint = season_active | day_promotes
            excluded = set(ELEMENTS) - joint

            # Classify cells
            status = {}
            counts = Counter()
            for cell in ALL_CELLS:
                s = classify_cell(cell, joint)
                status[cell] = s
                counts[s] += 1

            fire_water_both = ("Fire" in joint and "Water" in joint)

            states.append({
                "season": season,
                "season_element": sr["season_element"],
                "day_branch": branch,
                "day_element": bd["element"],
                "season_active": sorted(season_active),
                "day_promotes": sorted(day_promotes),
                "active_elements": sorted(joint),
                "active_count": len(joint),
                "excluded_elements": sorted(excluded),
                "excluded_count": len(excluded),
                "cell_status": status,
                "cell_counts": dict(counts),
                "fire_water_both": fire_water_both,
            })

    return states


def print_temporal_states(states, branch_data):
    print(f"\n{SEPARATOR}")
    print("PART B: 日辰 EXTENSION (60 TEMPORAL STATES)")
    print(SEPARATOR)

    # Day branch table
    print(f"\n{'Branch':>6} {'Element':>7} {'Promotes':>20}")
    print("─" * 38)
    for b in BRANCHES:
        bd = branch_data[b]
        print(f"{b:>6} {bd['element']:>7} {{{', '.join(bd['promotes'])}}}".rjust(38))

    # Summary per season
    print(f"\n{'Season':12s} {'Branch':>6} {'Day':>5} {'Active':>6} {'#Act':>4} {'Excl':>15} {'FW':>3}  {'A':>2} {'P':>2} {'D':>2}")
    print("─" * 78)

    for season in SEASON_NAMES:
        season_states = [s for s in states if s["season"] == season]
        for s in season_states:
            fw = "✓" if s["fire_water_both"] else " "
            excl_str = ",".join(s["excluded_elements"]) if s["excluded_elements"] else "—"
            act_str = ",".join(s["active_elements"])
            cc = s["cell_counts"]
            print(f"{season:12s} {s['day_branch']:>6} {s['day_element']:>5} "
                  f"{act_str:>20} {s['active_count']:>4} {excl_str:>15} {fw:>3}  "
                  f"{cc.get('active',0):2d} {cc.get('partial',0):2d} {cc.get('dark',0):2d}")
        print()


# ─── Part C: Summary statistics ─────────────────────────────────────────────

def summary_statistics(states, seasonal_results):
    print(f"\n{SEPARATOR}")
    print("PART C: SUMMARY STATISTICS")
    print(SEPARATOR)

    # Active set size distribution
    size_dist = Counter(s["active_count"] for s in states)
    print(f"\nActive set size distribution across 60 states:")
    for sz in sorted(size_dist):
        print(f"  {sz} elements: {size_dist[sz]}/60 ({100*size_dist[sz]/60:.1f}%)")

    # Per season: how many day-branches expand beyond baseline
    print(f"\nPer season: day-branches that expand beyond seasonal baseline (2 elements):")
    for season in SEASON_NAMES:
        season_states = [s for s in states if s["season"] == season]
        expanded = sum(1 for s in season_states if s["active_count"] > 2)
        print(f"  {season:12s}: {expanded}/12 branches expand ({100*expanded/12:.0f}%)")

    # Excluded element pattern at max coverage (active=4)
    max_states = [s for s in states if s["active_count"] == 4]
    if max_states:
        excl_counter = Counter()
        for s in max_states:
            for e in s["excluded_elements"]:
                excl_counter[e] += 1
        print(f"\nExcluded element at max coverage (active=4, {len(max_states)} states):")
        for e in ELEMENTS:
            print(f"  {e:>5}: excluded in {excl_counter.get(e, 0)}/{len(max_states)} max-coverage states")

        # Check 休/死 pattern
        print(f"\nVerify excluded element is always 休 or 死:")
        violations = 0
        for s in max_states:
            se = s["season_element"]
            strengths = seasonal_strength(se)
            strength_map = {v: k for k, v in strengths.items()}
            for e in s["excluded_elements"]:
                level = strength_map.get(e, "?")
                if level not in ("休", "死"):
                    violations += 1
                    print(f"  VIOLATION: {s['season']}+{s['day_branch']}: "
                          f"excluded {e} is {level}")
        if violations == 0:
            print(f"  All {len(max_states)} states: excluded element is 休 or 死 ✓")

    # Fire & Water both active
    fw_count = sum(1 for s in states if s["fire_water_both"])
    print(f"\nFire AND Water both active: {fw_count}/60 states ({100*fw_count/60:.1f}%)")

    # Mean active cells
    mean_active = sum(s["cell_counts"].get("active", 0) for s in states) / len(states)
    mean_partial = sum(s["cell_counts"].get("partial", 0) for s in states) / len(states)
    mean_dark = sum(s["cell_counts"].get("dark", 0) for s in states) / len(states)
    print(f"\nMean cells per state: active={mean_active:.1f}, partial={mean_partial:.1f}, dark={mean_dark:.1f}")

    # Active cell count distribution
    act_cell_dist = Counter(s["cell_counts"].get("active", 0) for s in states)
    print(f"\nActive cell count distribution:")
    for n in sorted(act_cell_dist):
        print(f"  {n:2d} cells active: {act_cell_dist[n]}/60 states")

    return {
        "active_size_distribution": dict(size_dist),
        "mean_active_cells": round(mean_active, 2),
        "mean_partial_cells": round(mean_partial, 2),
        "mean_dark_cells": round(mean_dark, 2),
        "fire_water_both_count": fw_count,
        "active_cell_count_dist": dict(act_cell_dist),
    }


# ─── Serialize ───────────────────────────────────────────────────────────────

def serialize(seasonal_results, branch_data, states, summary):
    seasons_out = {}
    for season, r in seasonal_results.items():
        cell_status_out = {cell_key(c): s for c, s in r["cell_status"].items()}
        seasons_out[season] = {
            "season_element": r["season_element"],
            "strengths": r["strengths"],
            "active_elements": r["active_elements"],
            "excluded_elements": r["excluded_elements"],
            "cell_status": cell_status_out,
            "counts": r["counts"],
        }

    states_out = []
    for s in states:
        cell_status_out = {cell_key(c): st for c, st in s["cell_status"].items()}
        states_out.append({
            "season": s["season"],
            "season_element": s["season_element"],
            "day_branch": s["day_branch"],
            "day_element": s["day_element"],
            "active_elements": s["active_elements"],
            "active_count": s["active_count"],
            "excluded_elements": s["excluded_elements"],
            "cell_status": cell_status_out,
            "fire_water_both": s["fire_water_both"],
            "cell_counts": s["cell_counts"],
        })

    return {
        "seasons": seasons_out,
        "day_branches": branch_data,
        "states": states_out,
        "summary": summary,
    }


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    seasonal = seasonal_windows()
    print_seasonal_windows(seasonal)

    branches = day_branch_data()
    states = temporal_states(seasonal, branches)
    print_temporal_states(states, branches)

    summary = summary_statistics(states, seasonal)

    out = serialize(seasonal, branches, states, summary)
    out_path = Path(__file__).parent / "temporal_data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
