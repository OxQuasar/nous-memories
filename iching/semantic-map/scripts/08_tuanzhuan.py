"""S9: 彖傳 Structural Analysis — does 彖傳 structural vocabulary track algebraic coordinates?"""

import json
import re
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ATLAS_PATH = ROOT.parent / "atlas" / "atlas.json"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"


def load_data():
    with open(DATA / "tuanzhuan_structure.json") as f:
        tuan_data = json.load(f)
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)
    with open(TEXTS / "tuan.json") as f:
        tuan_texts = json.load(f)["entries"]

    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}
    return tuan_data, atlas, tuan_texts, kw_to_hexval


def gang_rou_analysis(tuan_texts, atlas, kw_to_hexval):
    """Check if 剛/柔 references in 彖傳 match actual yang/yin line values."""
    print("\n  剛柔 + line reference analysis:")

    # Patterns: e.g., "九二剛", "六五柔", "剛中", "柔得中"
    # Look for line references near 剛/柔
    line_refs = {"初": 0, "二": 1, "三": 2, "四": 3, "五": 4, "上": 5}
    correct = 0
    total = 0
    examples = []

    for entry in tuan_texts:
        hv = kw_to_hexval[entry["number"]]
        h = atlas[str(hv)]
        binary = h["binary"]  # 6-char binary string, bit 0 = line 1

        text = entry["text"]

        # Find 剛/柔 near line references
        for line_char, line_idx in line_refs.items():
            # Check various patterns
            for pattern in [f"{line_char}.*剛", f"剛.*{line_char}", f"{line_char}.*柔", f"柔.*{line_char}"]:
                matches = re.findall(pattern, text[:50])  # limit search window
                for m in matches:
                    if len(m) > 10:
                        continue  # too far apart
                    is_gang = "剛" in m
                    actual_yang = int(binary[line_idx])
                    match = (is_gang and actual_yang == 1) or (not is_gang and actual_yang == 0)
                    if match:
                        correct += 1
                    total += 1
                    examples.append({
                        "hex": entry["name"],
                        "line": line_idx + 1,
                        "text_fragment": m,
                        "claimed": "剛" if is_gang else "柔",
                        "actual": "陽" if actual_yang else "陰",
                        "correct": match,
                    })

    if total > 0:
        print(f"    Matches found: {total}, correct: {correct} ({correct/total:.0%})")
    else:
        print("    No direct line-reference + 剛/柔 matches found")

    return {"correct": correct, "total": total, "examples": examples[:10]}


def zhong_analysis(tuan_texts, atlas, kw_to_hexval):
    """Analyze which lines '中' refers to in 彖傳."""
    print("\n  中 analysis:")

    # 中 in 彖傳 typically refers to lines 2 and 5 (central positions)
    # Count 剛中, 柔中, 得中 patterns
    zhong_contexts = []
    for entry in tuan_texts:
        hv = kw_to_hexval[entry["number"]]
        h = atlas[str(hv)]
        binary = h["binary"]
        text = entry["text"]

        # Find all 中 with surrounding context
        for m in re.finditer("中", text):
            start = max(0, m.start() - 3)
            end = min(len(text), m.end() + 3)
            ctx = text[start:end]
            # Try to infer which line: 剛中 = yang line at 2 or 5; 柔中 = yin line at 2 or 5
            line_2_yang = int(binary[1])
            line_5_yang = int(binary[4])

            if "剛中" in ctx or "剛得中" in ctx:
                # Refers to a yang line at position 2 or 5
                zhong_contexts.append({"type": "剛中", "line2_yang": line_2_yang,
                                       "line5_yang": line_5_yang, "hex": entry["name"]})
            elif "柔中" in ctx or "柔得中" in ctx:
                zhong_contexts.append({"type": "柔中", "line2_yang": line_2_yang,
                                       "line5_yang": line_5_yang, "hex": entry["name"]})

    # Check consistency
    gang_zhong = [c for c in zhong_contexts if c["type"] == "剛中"]
    rou_zhong = [c for c in zhong_contexts if c["type"] == "柔中"]

    if gang_zhong:
        # 剛中 → should have yang at line 2 or 5
        has_yang_25 = sum(1 for c in gang_zhong if c["line2_yang"] or c["line5_yang"])
        print(f"    剛中: {len(gang_zhong)} occurrences, {has_yang_25} have yang at line 2 or 5")

    if rou_zhong:
        has_yin_25 = sum(1 for c in rou_zhong
                         if not c["line2_yang"] or not c["line5_yang"])
        print(f"    柔中: {len(rou_zhong)} occurrences, {has_yin_25} have yin at line 2 or 5")

    # Total 中 occurrences
    total_zhong = sum(1 for e in tuan_texts if "中" in e["text"])
    print(f"    Total hexagrams with 中: {total_zhong}/64")

    return {"剛中": len(gang_zhong), "柔中": len(rou_zhong),
            "total_with_zhong": total_zhong, "contexts": zhong_contexts[:10]}


def ying_analysis(tuan_texts, atlas, kw_to_hexval):
    """Analyze 應 (correspondence) references."""
    print("\n  應 analysis:")

    ying_hexes = []
    for entry in tuan_texts:
        hv = kw_to_hexval[entry["number"]]
        h = atlas[str(hv)]
        binary = h["binary"]
        text = entry["text"]

        if "應" in text:
            # Standard correspondence: 1↔4, 2↔5, 3↔6
            # Corresponding lines "應" if they differ in yin/yang
            correspondences = []
            pairs = [(0, 3), (1, 4), (2, 5)]
            for i, j in pairs:
                # 應 = lines differ (one yang, one yin)
                has_ying = int(binary[i]) != int(binary[j])
                correspondences.append({"pair": f"{i+1}↔{j+1}", "has_ying": has_ying})

            ying_hexes.append({
                "hex": entry["name"],
                "correspondences": correspondences,
                "n_responding": sum(1 for c in correspondences if c["has_ying"]),
            })

    if ying_hexes:
        total_responding = sum(h["n_responding"] for h in ying_hexes)
        total_pairs = len(ying_hexes) * 3
        print(f"    Hexagrams mentioning 應: {len(ying_hexes)}")
        print(f"    Responding pairs: {total_responding}/{total_pairs} "
              f"({total_responding/total_pairs:.0%})")
        # Compare: hexagrams NOT mentioning 應
        non_ying_hexes = [e for e in tuan_texts if "應" not in e["text"]]
        non_ying_responding = 0
        non_total = 0
        for entry in non_ying_hexes:
            hv = kw_to_hexval[entry["number"]]
            binary = atlas[str(hv)]["binary"]
            for i, j in [(0, 3), (1, 4), (2, 5)]:
                if int(binary[i]) != int(binary[j]):
                    non_ying_responding += 1
                non_total += 1
        print(f"    Non-應 hexagrams responding pairs: {non_ying_responding}/{non_total} "
              f"({non_ying_responding/non_total:.0%})" if non_total > 0 else "")

    return {"n_hexagrams": len(ying_hexes), "details": ying_hexes[:10]}


def algebra_crosstab(tuan_data, atlas, kw_to_hexval):
    """Cross-tabulate 彖傳 structural categories with algebraic coordinates."""
    print("\n  Cross-tab: structural vocabulary × algebraic coordinates")

    entries = tuan_data["entries"]

    gang_count = []
    rou_count = []
    zhong_count = []
    wang_lai_count = []
    basins = []
    i_components = []
    surface_rels = []

    for entry in entries:
        hv = entry["hex_val"]
        h = atlas[str(hv)]
        text = entry["text"]

        gang_count.append(text.count("剛"))
        rou_count.append(text.count("柔"))
        zhong_count.append(text.count("中"))
        wang_lai_count.append(text.count("往") + text.count("來"))
        basins.append(h["basin"])
        i_components.append(h["i_component"])
        surface_rels.append(h["surface_relation"])

    gang_count = np.array(gang_count, dtype=float)
    rou_count = np.array(rou_count, dtype=float)
    zhong_count = np.array(zhong_count, dtype=float)
    wang_lai_count = np.array(wang_lai_count, dtype=float)

    # 剛/柔 ratio by basin
    print("\n    剛/柔 counts by basin:")
    for basin in sorted(set(basins)):
        mask = np.array([b == basin for b in basins])
        g = gang_count[mask].sum()
        r = rou_count[mask].sum()
        ratio = g / r if r > 0 else float("inf")
        print(f"      {basin}: 剛={g} 柔={r} ratio={ratio:.2f}")

    # Structural term density by I-component
    print("\n    Term density by I-component:")
    for ic in [0, 1]:
        mask = np.array([c == ic for c in i_components])
        n = mask.sum()
        g = gang_count[mask].mean()
        r = rou_count[mask].mean()
        z = zhong_count[mask].mean()
        print(f"      I={ic} (n={n}): 剛={g:.2f} 柔={r:.2f} 中={z:.2f}")

    # 往/來 by surface relation
    print("\n    往/來 by surface relation:")
    wang_lai = wang_lai_count
    for sr in sorted(set(surface_rels)):
        mask = np.array([s == sr for s in surface_rels])
        n = mask.sum()
        mean_wl = wang_lai[mask].mean()
        print(f"      {sr} (n={n}): mean 往來={mean_wl:.2f}")

    # Statistical tests
    results = {}

    # Kruskal-Wallis: gang-rou ratio by basin
    gr_ratio = np.where(rou_count > 0, gang_count / rou_count,
                        np.where(gang_count > 0, 10.0, 1.0))
    basin_groups = defaultdict(list)
    for i, b in enumerate(basins):
        basin_groups[b].append(gr_ratio[i])
    if len(basin_groups) >= 2:
        kw_stat, kw_p = stats.kruskal(*basin_groups.values())
        print(f"\n    Kruskal-Wallis (剛/柔 ratio by basin): H={kw_stat:.2f}, p={kw_p:.4f}")
        results["gang_rou_basin"] = {"H": float(kw_stat), "p": float(kw_p)}

    # Mann-Whitney: structural density by I-component
    ic0_density = (gang_count + rou_count + zhong_count)[np.array([c == 0 for c in i_components])]
    ic1_density = (gang_count + rou_count + zhong_count)[np.array([c == 1 for c in i_components])]
    if len(ic0_density) > 0 and len(ic1_density) > 0:
        u_stat, u_p = stats.mannwhitneyu(ic0_density, ic1_density, alternative="two-sided")
        print(f"    Mann-Whitney (density by I-component): U={u_stat:.0f}, p={u_p:.4f}")
        results["density_icomp"] = {"U": float(u_stat), "p": float(u_p)}

    # Kruskal-Wallis: wang/lai by surface relation
    sr_groups = defaultdict(list)
    for i, sr in enumerate(surface_rels):
        sr_groups[sr].append(wang_lai[i])
    if len(sr_groups) >= 2:
        kw2, kw2_p = stats.kruskal(*sr_groups.values())
        print(f"    Kruskal-Wallis (往來 by surface rel): H={kw2:.2f}, p={kw2_p:.4f}")
        results["wanglai_srel"] = {"H": float(kw2), "p": float(kw2_p)}

    return results


def main():
    tuan_data, atlas, tuan_texts, kw_to_hexval = load_data()

    print("=" * 60)
    print("彖傳 Structural Analysis")
    print("=" * 60)

    gr_res = gang_rou_analysis(tuan_texts, atlas, kw_to_hexval)
    zhong_res = zhong_analysis(tuan_texts, atlas, kw_to_hexval)
    ying_res = ying_analysis(tuan_texts, atlas, kw_to_hexval)
    algebra_res = algebra_crosstab(tuan_data, atlas, kw_to_hexval)

    output = {
        "gang_rou": gr_res,
        "zhong": zhong_res,
        "ying": ying_res,
        "algebra_crosstab": algebra_res,
    }

    with open(DATA / "tuanzhuan_analysis.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'tuanzhuan_analysis.json'}")


if __name__ == "__main__":
    main()
