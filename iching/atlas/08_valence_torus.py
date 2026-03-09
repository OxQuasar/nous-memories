#!/usr/bin/env python3
"""
Valence rates per Z₅×Z₅ cell.

Extracts 凶/吉/无咎/悔/吝/厲 markers from 爻辭 and maps to torus cells.
Tests spatial structure of the two known bridges:
  - Core bridge: 凶 × basin
  - Shell bridge: 吉 × 生体

Outputs: stdout tables + valence_torus.json
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
from scipy import stats as sp_stats

# ─── Constants ───────────────────────────────────────────────────────────────

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
ALL_CELLS = [(a, b) for a in ELEMENTS for b in ELEMENTS]

VALENCE_MARKERS = {
    "吉": "auspicious",
    "凶": "inauspicious",
    "悔": "regret",
    "吝": "difficulty",
    "無咎": "no_blame",
    "无咎": "no_blame",
    "厲": "danger",
}

SEPARATOR = "─" * 78

ATLAS_DIR = Path(__file__).parent
TEXTS_DIR = ATLAS_DIR.parent.parent / "texts" / "iching"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def cell_key(cell):
    return f"({cell[0]},{cell[1]})"


# ─── Data loading ────────────────────────────────────────────────────────────

def load_yaoci():
    """Load 爻辭 texts, return dict: kw_number → [line1_text, ..., line6_text]."""
    data = load_json(TEXTS_DIR / "yaoci.json")
    yaoci = {}
    for entry in data["entries"]:
        yaoci[entry["number"]] = [line["text"] for line in entry["lines"]]
    return yaoci


def extract_valence(atlas, yaoci):
    """Extract valence markers per 爻 (384 records).

    Each record has hex_val, kw_number, line (1-6), surface_cell, basin,
    surface_relation, and marker presence flags.
    """
    records = []
    for h in range(64):
        entry = atlas[str(h)]
        kw = entry["kw_number"]
        lines = yaoci[kw]

        for line_idx, text in enumerate(lines):
            line_pos = line_idx + 1
            markers = {}
            for marker, label in VALENCE_MARKERS.items():
                if marker in text:
                    markers[label] = True

            records.append({
                "hex_val": h,
                "kw_number": kw,
                "kw_name": entry["kw_name"],
                "line": line_pos,
                "surface_cell": tuple(entry["surface_cell"]),
                "surface_relation": entry["surface_relation"],
                "basin": entry["basin"],
                "depth": entry["depth"],
                "markers": markers,
            })

    return records


# ─── 1. Per-cell valence rates ───────────────────────────────────────────────

def per_cell_rates(records):
    """Compute 凶/吉 rates per Z₅×Z₅ cell."""
    cell_data = defaultdict(lambda: {
        "total": 0,
        "auspicious": 0,
        "inauspicious": 0,
        "no_blame": 0,
        "regret": 0,
        "difficulty": 0,
        "danger": 0,
        "hexagrams": set(),
        "basins": Counter(),
    })

    for r in records:
        cell = r["surface_cell"]
        d = cell_data[cell]
        d["total"] += 1
        d["hexagrams"].add(r["hex_val"])
        d["basins"][r["basin"]] += 1
        for label in ["auspicious", "inauspicious", "no_blame", "regret", "difficulty", "danger"]:
            if label in r["markers"]:
                d[label] += 1

    return cell_data


def print_cell_rates(cell_data):
    print(f"\n{SEPARATOR}")
    print("1. VALENCE RATES PER Z₅×Z₅ CELL")
    print(SEPARATOR)

    print(f"\n{'Cell':17s} {'Pop':>3} {'N爻':>4} {'凶':>4} {'凶%':>6} {'吉':>4} {'吉%':>6} {'无咎':>4} {'悔':>3} {'吝':>3} {'厲':>3}  Basins")
    print("─" * 95)

    all_xiong = 0
    all_ji = 0
    all_n = 0

    for cell in ALL_CELLS:
        d = cell_data.get(cell)
        if d is None:
            continue
        n = d["total"]
        pop = len(d["hexagrams"])
        xiong = d["inauspicious"]
        ji = d["auspicious"]
        all_xiong += xiong
        all_ji += ji
        all_n += n

        xiong_pct = 100 * xiong / n if n else 0
        ji_pct = 100 * ji / n if n else 0

        basin_str = " ".join(f"{b}:{c//6}" for b, c in sorted(d["basins"].items()))
        flag = " ◂" if pop <= 1 else ""

        print(f"{cell_key(cell):17s} {pop:3d} {n:4d} {xiong:4d} {xiong_pct:5.1f}% {ji:4d} {ji_pct:5.1f}% "
              f"{d['no_blame']:4d} {d['regret']:3d} {d['difficulty']:3d} {d['danger']:3d}  {basin_str}{flag}")

    print(f"\n{'TOTAL':17s}     {all_n:4d} {all_xiong:4d} {100*all_xiong/all_n:5.1f}% {all_ji:4d} {100*all_ji/all_n:5.1f}%")
    print(f"  ◂ = singleton cell (pop=1, only 6 爻 — low statistical power)")


# ─── 2. Core bridge: 凶 × basin at cell level ───────────────────────────────

def core_bridge(records, cell_data):
    """Test 凶 × basin, then check if cell-level 凶 rates vary beyond basin effect."""
    print(f"\n{SEPARATOR}")
    print("2. CORE BRIDGE: 凶 × BASIN")
    print(SEPARATOR)

    # Basin-level 凶 rates
    basin_xiong = defaultdict(lambda: {"total": 0, "xiong": 0})
    for r in records:
        basin_xiong[r["basin"]]["total"] += 1
        if "inauspicious" in r["markers"]:
            basin_xiong[r["basin"]]["xiong"] += 1

    print(f"\n{'Basin':>8} {'N':>4} {'凶':>4} {'凶%':>7}")
    print("─" * 28)
    for basin in ["Kun", "Qian", "Cycle"]:
        d = basin_xiong[basin]
        pct = 100 * d["xiong"] / d["total"]
        print(f"{basin:>8} {d['total']:4d} {d['xiong']:4d} {pct:6.1f}%")

    # Chi-square: basin × 凶
    basins = ["Kun", "Qian", "Cycle"]
    obs = np.array([[basin_xiong[b]["xiong"], basin_xiong[b]["total"] - basin_xiong[b]["xiong"]]
                     for b in basins])
    chi2, p, dof, _ = sp_stats.chi2_contingency(obs)
    print(f"\nχ² test (凶 × basin): χ²={chi2:.3f}, p={p:.4f}, dof={dof}")

    # Per-cell 凶 rate: is there variation beyond basin?
    # Group cells by basin composition
    print(f"\n凶 rate by cell, grouped by dominant basin:")
    mixed_cells = []
    pure_cells = defaultdict(list)

    for cell in ALL_CELLS:
        d = cell_data.get(cell)
        if d is None:
            continue
        basin_counts = d["basins"]
        total = d["total"]
        xiong_rate = d["inauspicious"] / total if total else 0

        # Determine if cell is pure or mixed basin
        basin_hexes = {b: c // 6 for b, c in basin_counts.items()}
        if len(basin_hexes) == 1:
            basin_name = list(basin_hexes.keys())[0]
            pure_cells[basin_name].append((cell, xiong_rate, len(d["hexagrams"])))
        else:
            mixed_cells.append((cell, xiong_rate, basin_hexes, len(d["hexagrams"])))

    for basin in ["Kun", "Qian", "Cycle"]:
        cells = pure_cells.get(basin, [])
        if cells:
            rates = [r for _, r, _ in cells]
            print(f"  Pure {basin}: {len(cells)} cells, 凶 rates: {[f'{r:.1%}' for r in rates]}")

    if mixed_cells:
        print(f"  Mixed basin: {len(mixed_cells)} cells")
        for cell, rate, basin_hexes, pop in mixed_cells:
            print(f"    {cell_key(cell)} (pop={pop}): 凶={rate:.1%}, basins={dict(basin_hexes)}")

    return {"chi2": chi2, "p": p, "basin_rates": {b: d for b, d in basin_xiong.items()}}


# ─── 3. Shell bridge: 吉 × 生体 at cell level ───────────────────────────────

def shell_bridge(records, cell_data):
    """Test 吉 × surface_relation, especially 生体."""
    print(f"\n{SEPARATOR}")
    print("3. SHELL BRIDGE: 吉 × 生体 (surface_relation)")
    print(SEPARATOR)

    # Relation-level 吉 rates
    rel_data = defaultdict(lambda: {"total": 0, "ji": 0, "xiong": 0})
    for r in records:
        rel = r["surface_relation"]
        rel_data[rel]["total"] += 1
        if "auspicious" in r["markers"]:
            rel_data[rel]["ji"] += 1
        if "inauspicious" in r["markers"]:
            rel_data[rel]["xiong"] += 1

    relations = ["比和", "生体", "体生用", "克体", "体克用"]
    print(f"\n{'Relation':>8} {'N':>4} {'吉':>4} {'吉%':>7} {'凶':>4} {'凶%':>7}")
    print("─" * 42)
    for rel in relations:
        d = rel_data[rel]
        ji_pct = 100 * d["ji"] / d["total"]
        xiong_pct = 100 * d["xiong"] / d["total"]
        print(f"{rel:>8} {d['total']:4d} {d['ji']:4d} {ji_pct:6.1f}% {d['xiong']:4d} {xiong_pct:6.1f}%")

    # Fisher exact test: 生体 vs rest for 吉
    shengtai = rel_data["生体"]
    rest_ji = sum(d["ji"] for r, d in rel_data.items() if r != "生体")
    rest_total = sum(d["total"] for r, d in rel_data.items() if r != "生体")

    table_fisher = np.array([
        [shengtai["ji"], shengtai["total"] - shengtai["ji"]],
        [rest_ji, rest_total - rest_ji],
    ])
    odds_ratio, p_fisher = sp_stats.fisher_exact(table_fisher)
    print(f"\nFisher exact (生体 vs rest, 吉): OR={odds_ratio:.3f}, p={p_fisher:.4f}")

    # Chi-square: all 5 relations × 吉
    obs = np.array([[rel_data[r]["ji"], rel_data[r]["total"] - rel_data[r]["ji"]]
                     for r in relations])
    chi2, p, dof, _ = sp_stats.chi2_contingency(obs)
    print(f"χ² test (吉 × relation, 5 levels): χ²={chi2:.3f}, p={p:.4f}, dof={dof}")

    # Per-cell 吉 rates grouped by relation
    print(f"\n吉 rate by cell, grouped by surface_relation:")
    for rel in relations:
        cells_in_rel = []
        for cell in ALL_CELLS:
            d = cell_data.get(cell)
            if d is None:
                continue
            # Check if all hexagrams in cell have this relation
            # Actually: cell determines the relation (since cell = (lower_elem, upper_elem))
            # Let me check by examining the data
            pass

        # Group by relation at hexagram level — each cell has one relation
        rel_cells = [(cell, cell_data[cell]) for cell in ALL_CELLS
                     if cell in cell_data and _cell_relation(cell) == rel]
        if rel_cells:
            rates = []
            for cell, d in rel_cells:
                rate = d["auspicious"] / d["total"] if d["total"] else 0
                rates.append(f"{cell_key(cell)}={rate:.0%}")
            print(f"  {rel}: {', '.join(rates)}")

    return {
        "fisher_or": odds_ratio, "fisher_p": p_fisher,
        "chi2": chi2, "chi2_p": p,
        "relation_rates": {r: dict(d) for r, d in rel_data.items()},
    }


def _cell_relation(cell):
    """Determine surface_relation from cell coordinates."""
    # This is the five_phase_relation(lower, upper) = relation of lower to upper
    lo, up = cell
    SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
    KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

    if lo == up:
        return "比和"
    elif SHENG[lo] == up:
        return "体生用"
    elif SHENG[up] == lo:
        return "生体"
    elif KE[lo] == up:
        return "体克用"
    elif KE[up] == lo:
        return "克体"
    return "unknown"


# ─── 4. Torus-level spatial test ─────────────────────────────────────────────

def torus_spatial(records, cell_data):
    """Test for spatial patterns beyond basin and relation."""
    print(f"\n{SEPARATOR}")
    print("4. TORUS-LEVEL SPATIAL ANALYSIS")
    print(SEPARATOR)

    EL_IDX = {e: i for i, e in enumerate(ELEMENTS)}

    # Compute 生/克 distances
    # 生 distance: (idx_upper - idx_lower) mod 5, where sheng cycle = 0→1→2→3→4
    # 克 distance: (idx_upper - idx_lower) mod 5 on the 克 cycle
    # Actually: on Z₅, 生 = +1, 克 = +2

    # For each cell, compute the 生 distance and 克 distance
    print(f"\n凶/吉 rates by torus distance (lower→upper along 生 cycle):")
    dist_data = defaultdict(lambda: {"total": 0, "xiong": 0, "ji": 0})

    for r in records:
        lo_idx = EL_IDX[r["surface_cell"][0]]
        up_idx = EL_IDX[r["surface_cell"][1]]
        d = (up_idx - lo_idx) % 5  # distance along 生 cycle
        dist_data[d]["total"] += 1
        if "inauspicious" in r["markers"]:
            dist_data[d]["xiong"] += 1
        if "auspicious" in r["markers"]:
            dist_data[d]["ji"] += 1

    print(f"\n{'Dist':>4} {'Relation':>8} {'N':>4} {'凶':>4} {'凶%':>7} {'吉':>4} {'吉%':>7}")
    print("─" * 48)
    dist_labels = {0: "比和", 1: "体生用", 2: "体克用", 3: "克体", 4: "生体"}
    for d in range(5):
        dd = dist_data[d]
        xiong_pct = 100 * dd["xiong"] / dd["total"]
        ji_pct = 100 * dd["ji"] / dd["total"]
        print(f"{d:4d} {dist_labels[d]:>8} {dd['total']:4d} {dd['xiong']:4d} {xiong_pct:6.1f}% {dd['ji']:4d} {ji_pct:6.1f}%")

    # Residual analysis: 凶 rate per cell after controlling for basin
    print(f"\nResidual 凶 rate (cell rate − basin expected rate):")
    basin_rates = {}
    basin_totals = defaultdict(lambda: {"total": 0, "xiong": 0})
    for r in records:
        basin_totals[r["basin"]]["total"] += 1
        if "inauspicious" in r["markers"]:
            basin_totals[r["basin"]]["xiong"] += 1
    for b, d in basin_totals.items():
        basin_rates[b] = d["xiong"] / d["total"]

    print(f"\n{'Cell':17s} {'Pop':>3} {'凶_obs':>6} {'凶_exp':>6} {'residual':>8}")
    print("─" * 48)
    residuals = []
    for cell in ALL_CELLS:
        d = cell_data.get(cell)
        if d is None:
            continue
        n = d["total"]
        obs_rate = d["inauspicious"] / n

        # Expected rate: weighted average of basin rates by basin composition
        exp_xiong = sum(basin_rates[b] * c for b, c in d["basins"].items()) / n
        resid = obs_rate - exp_xiong
        residuals.append((cell, obs_rate, exp_xiong, resid, len(d["hexagrams"])))
        print(f"{cell_key(cell):17s} {len(d['hexagrams']):3d} {obs_rate:6.1%} {exp_xiong:6.1%} {resid:+7.1%}")

    # Test: are residuals significantly non-zero? (chi-square of residuals)
    # This tests whether cell position adds info beyond basin
    obs_arr = []
    exp_arr = []
    for cell in ALL_CELLS:
        d = cell_data.get(cell)
        if d is None:
            continue
        n = d["total"]
        obs_arr.append(d["inauspicious"])
        exp = sum(basin_rates[b] * c for b, c in d["basins"].items()) / n * n
        exp_arr.append(exp)

    obs_arr = np.array(obs_arr)
    exp_arr = np.array(exp_arr)
    # Avoid division by zero
    mask = exp_arr > 0
    chi2_resid = np.sum((obs_arr[mask] - exp_arr[mask])**2 / exp_arr[mask])
    dof_resid = mask.sum() - 1  # approximate
    p_resid = 1 - sp_stats.chi2.cdf(chi2_resid, dof_resid)
    print(f"\nResidual χ² (cell 凶 | basin): χ²={chi2_resid:.3f}, dof≈{dof_resid}, p={p_resid:.4f}")
    print(f"{'SIGNIFICANT' if p_resid < 0.05 else 'NOT significant'}: "
          f"cell position {'adds' if p_resid < 0.05 else 'does not add'} information beyond basin")

    return {"dist_data": {str(d): dict(dd) for d, dd in dist_data.items()},
            "residual_chi2": chi2_resid, "residual_p": p_resid}


# ─── Summary ─────────────────────────────────────────────────────────────────

def print_summary(core_result, shell_result, spatial_result):
    print(f"\n{'═' * 78}")
    print("SUMMARY: Valence on the torus")
    print(f"{'═' * 78}")

    print(f"""
Core bridge (凶 × basin):
  χ² test: χ²={core_result['chi2']:.3f}, p={core_result['p']:.4f}
  {'CONFIRMED' if core_result['p'] < 0.05 else 'Not significant'} at cell level
  Basin 凶 rates: {', '.join(f"{b}={d['xiong']/d['total']:.1%}" for b,d in core_result['basin_rates'].items())}

Shell bridge (吉 × 生体):
  Fisher exact (生体 vs rest): OR={shell_result['fisher_or']:.3f}, p={shell_result['fisher_p']:.4f}
  {'CONFIRMED' if shell_result['fisher_p'] < 0.05 else 'Not significant'} at cell level
  χ² (all 5 relations): χ²={shell_result['chi2']:.3f}, p={shell_result['chi2_p']:.4f}

Torus spatial residual (凶 | basin):
  χ²={spatial_result['residual_chi2']:.3f}, p={spatial_result['residual_p']:.4f}
  {'Cell position carries information beyond basin' if spatial_result['residual_p'] < 0.05 else 'No spatial structure beyond basin — the bridges explain the signal'}

Population gradient: 4:2:1 on the torus
  Singleton cells (6 爻 each) have very low statistical power
  Results dominated by pop-4 cells (24 爻 each)
""")


# ─── Serialize ───────────────────────────────────────────────────────────────

def serialize(cell_data, core_result, shell_result, spatial_result):
    cells_out = {}
    for cell in ALL_CELLS:
        d = cell_data.get(cell)
        if d is None:
            continue
        n = d["total"]
        cells_out[cell_key(cell)] = {
            "population": len(d["hexagrams"]),
            "n_yao": n,
            "auspicious": d["auspicious"],
            "auspicious_rate": round(d["auspicious"] / n, 4) if n else 0,
            "inauspicious": d["inauspicious"],
            "inauspicious_rate": round(d["inauspicious"] / n, 4) if n else 0,
            "no_blame": d["no_blame"],
            "regret": d["regret"],
            "difficulty": d["difficulty"],
            "danger": d["danger"],
            "basin_distribution": dict(d["basins"]),
            "surface_relation": _cell_relation(cell),
        }

    return {
        "per_cell": cells_out,
        "core_bridge": {
            "chi2": core_result["chi2"],
            "p": core_result["p"],
            "basin_rates": {b: {"total": d["total"], "xiong": d["xiong"],
                                 "rate": round(d["xiong"]/d["total"], 4)}
                            for b, d in core_result["basin_rates"].items()},
        },
        "shell_bridge": {
            "fisher_or": shell_result["fisher_or"],
            "fisher_p": shell_result["fisher_p"],
            "chi2": shell_result["chi2"],
            "chi2_p": shell_result["chi2_p"],
            "relation_rates": {r: {"total": d["total"], "ji": d["ji"],
                                    "rate": round(d["ji"]/d["total"], 4)}
                               for r, d in shell_result["relation_rates"].items()},
        },
        "spatial_residual": {
            "chi2": spatial_result["residual_chi2"],
            "p": spatial_result["residual_p"],
        },
    }


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    atlas = load_json(ATLAS_DIR / "atlas.json")
    yaoci = load_yaoci()

    records = extract_valence(atlas, yaoci)
    print(f"Extracted {len(records)} 爻 records")

    marker_counts = Counter()
    for r in records:
        for m in r["markers"]:
            marker_counts[m] += 1
    print(f"Marker counts: {dict(marker_counts.most_common())}")

    cell_data = per_cell_rates(records)
    print_cell_rates(cell_data)

    core_result = core_bridge(records, cell_data)
    shell_result = shell_bridge(records, cell_data)
    spatial_result = torus_spatial(records, cell_data)
    print_summary(core_result, shell_result, spatial_result)

    out = serialize(cell_data, core_result, shell_result, spatial_result)
    out_path = ATLAS_DIR / "valence_torus.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
