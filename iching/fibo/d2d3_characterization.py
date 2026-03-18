#!/usr/bin/env python3
"""
d=2/d=3 characterization: text-length mediation + extremes analysis.
"""

import sys
import json
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr, rankdata, kruskal
from scipy.stats import t as t_dist

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "reversal" / "Q1"))
from phase1_residual_structure import load_data as _load_phase1, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent  # memories/iching
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
TEXTS_DIR = ROOT.parent / "texts" / "iching"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']

# ── Helpers ──────────────────────────────────────────────────────────

def cosine_dist(a, b):
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

def dk_neighbors(h, k):
    return [x for x in range(N_HEX) if bin(h ^ x).count('1') == k]

def sig(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "** "
    if p < 0.05:  return "*  "
    return "   "

def partial_spearman(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    rz_c = rz - rz.mean()
    denom = np.dot(rz_c, rz_c)
    if denom < 1e-12:
        return np.nan, 1.0
    res_x = rx - rx.mean() - (np.dot(rx, rz_c) / denom) * rz_c
    res_y = ry - ry.mean() - (np.dot(ry, rz_c) / denom) * rz_c
    norm_prod = np.linalg.norm(res_x) * np.linalg.norm(res_y)
    if norm_prod < 1e-12:
        return np.nan, 1.0
    rho = np.dot(res_x, res_y) / norm_prod
    df = len(x) - 3
    t_val = rho * np.sqrt(df) / np.sqrt(1 - rho**2 + 1e-12)
    p = 2 * t_dist.sf(abs(t_val), df)
    return rho, p

# ── Data loading ─────────────────────────────────────────────────────

def load_all():
    atlas = json.load(open(ATLAS_PATH))
    _, meta, _ = _load_phase1()
    X, _ = build_design_matrix(meta)

    neighbors = {k: {h: dk_neighbors(h, k) for h in range(N_HEX)} for k in range(1, 6)}

    # Text lengths
    hex_to_kw = {int(k): v['kw_number'] for k, v in atlas.items() if k.isdigit()}
    yaoci_data = json.load(open(TEXTS_DIR / "yaoci.json"))['entries']
    yaoci_by_kw = {e['number']: e for e in yaoci_data}
    yaoci_lengths = np.array([
        sum(len(line['text']) for line in yaoci_by_kw[hex_to_kw[h]]['lines'])
        for h in range(N_HEX)
    ])

    # Compute per-model data
    results = {}
    for mname in MODEL_ORDER:
        emb = np.load(Q1_DIR / f"embeddings_{mname}.npz")['yaoci']
        resid, r2, _ = extract_residuals(emb, X)
        cents = np.array([resid[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])

        dk_diff = {}
        for k in range(1, 6):
            dk_diff[k] = np.array([
                np.mean([cosine_dist(cents[h], cents[n]) for n in neighbors[k][h]])
                for h in range(N_HEX)
            ])

        comp_opp = np.array([
            cosine_dist(cents[h], cents[atlas[str(h)]['complement']])
            for h in range(N_HEX)
        ])

        results[mname] = {'cents': cents, 'dk_diff': dk_diff, 'comp_opp': comp_opp}

    return atlas, results, yaoci_lengths, hex_to_kw

# ══════════════════════════════════════════════════════════════════════
# THREAD A: Text-length mediation
# ══════════════════════════════════════════════════════════════════════

def thread_a(results, yaoci_lengths):
    print("=" * 80)
    print("THREAD A: Text-length mediation of d=2 and d=3 couplings")
    print("=" * 80)
    print()

    print(f"  Yaoci text lengths: mean={yaoci_lengths.mean():.1f}, std={yaoci_lengths.std():.1f}, "
          f"min={yaoci_lengths.min()}, max={yaoci_lengths.max()}")
    print()

    # A1: ρ(dk_diff, text_length) for k=2,3 and ρ(comp_opp, text_length)
    print("  A1: Correlations with text length")
    print(f"  {'Model':14s} | {'ρ(d2,len)':>10s} {'p':>7s} | {'ρ(d3,len)':>10s} {'p':>7s} | {'ρ(comp,len)':>11s} {'p':>7s}")
    print("  " + "-" * 75)

    any_sig = False
    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        co = results[mname]['comp_opp']

        r2, p2 = spearmanr(dk[2], yaoci_lengths)
        r3, p3 = spearmanr(dk[3], yaoci_lengths)
        rc, pc = spearmanr(co, yaoci_lengths)

        if p2 < 0.05 or p3 < 0.05:
            any_sig = True

        print(f"  {mname:14s} | {r2:+10.4f} {p2:6.4f}{sig(p2)} | {r3:+10.4f} {p3:6.4f}{sig(p3)} | "
              f"{rc:+11.4f} {pc:6.4f}{sig(pc)}")

    # Also check d=1,4,5 for completeness
    print()
    print("  Full dk_diff vs text_length profile:")
    header = f"  {'Model':14s} |"
    for k in range(1, 6):
        header += f" {'d='+str(k):>10s}"
    print(header)
    print("  " + "-" * 72)

    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        row = f"  {mname:14s} |"
        for k in range(1, 6):
            rho, p = spearmanr(dk[k], yaoci_lengths)
            row += f" {rho:+.3f}{sig(p)}"
        print(row)

    # A2: Partial correlations controlling for text length
    print()
    print("  A2: Partial correlations controlling for text length")
    print(f"  {'Model':14s} | {'bivar d2':>10s} | {'d2|len':>10s} | {'bivar d3':>10s} | {'d3|len':>10s}")
    print("  " + "-" * 62)

    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        co = results[mname]['comp_opp']

        r2_biv, p2_biv = spearmanr(dk[2], co)
        r2_part, p2_part = partial_spearman(dk[2], co, yaoci_lengths)
        r3_biv, p3_biv = spearmanr(dk[3], co)
        r3_part, p3_part = partial_spearman(dk[3], co, yaoci_lengths)

        print(f"  {mname:14s} | {r2_biv:+.3f}{sig(p2_biv)} | {r2_part:+.3f}{sig(p2_part)} | "
              f"{r3_biv:+.3f}{sig(p3_biv)} | {r3_part:+.3f}{sig(p3_part)}")

    print()
    if any_sig:
        print("  ◄ Some dk_diff correlates with text length — check partial column for mediation")
    else:
        print("  ✓ No significant dk_diff–text_length correlation — text length does NOT mediate")

# ══════════════════════════════════════════════════════════════════════
# THREAD B: Extremes analysis
# ══════════════════════════════════════════════════════════════════════

def thread_b(atlas, results, yaoci_lengths, hex_to_kw):
    print()
    print("=" * 80)
    print("THREAD B: Extremes analysis — composite d2−d3 score")
    print("  score(h) = z(d2_diff(h)) − z(d3_diff(h))")
    print("  High = d2-distinctive + d3-blending → predicted: strongly complement-opposed")
    print("=" * 80)
    print()

    # B1: Compute composite score averaged across models
    per_model_scores = {}
    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        z2 = (dk[2] - dk[2].mean()) / dk[2].std()
        z3 = (dk[3] - dk[3].mean()) / dk[3].std()
        per_model_scores[mname] = z2 - z3

    # Average across models
    composite = np.mean([per_model_scores[m] for m in MODEL_ORDER], axis=0)
    # Also average comp_opp
    avg_comp_opp = np.mean([results[m]['comp_opp'] for m in MODEL_ORDER], axis=0)

    # B2: Rank and report top/bottom 10
    order = np.argsort(composite)[::-1]  # high to low
    top10 = order[:10]
    bot10 = order[-10:][::-1]  # reverse so most negative is last

    hamming_weight = np.array([bin(h).count('1') for h in range(N_HEX)])

    def hex_info(h):
        a = atlas[str(h)]
        return {
            'hex_val': h,
            'binary': f"{h:06b}",
            'kw': a['kw_number'],
            'name': a['kw_name'],
            'hw': hamming_weight[h],
            'upper': a['upper_trigram']['name'],
            'lower': a['lower_trigram']['name'],
            'palace': a['palace'],
            'basin': a['basin'],
            'rank': a['rank'],
            'element': a['palace_element'],
            'surface_rel': a['surface_relation'],
            'comp_opp': avg_comp_opp[h],
            'score': composite[h],
        }

    print("  TOP 10 (high d2_diff − d3_diff → predicted most complement-opposed):")
    print(f"  {'#':>2s} {'hex':>3s} {'binary':>6s} {'KW':>3s} {'Name':12s} {'HW':>2s} {'Upper':8s} {'Lower':8s} "
          f"{'Palace':8s} {'Basin':8s} {'Rk':>2s} {'Elem':6s} {'Rel':4s} {'comp_opp':>8s} {'score':>6s}")
    print("  " + "-" * 110)
    for i, h in enumerate(top10):
        info = hex_info(h)
        print(f"  {i+1:2d} {info['hex_val']:3d} {info['binary']:>6s} {info['kw']:3d} {info['name']:12s} "
              f"{info['hw']:2d} {info['upper']:8s} {info['lower']:8s} "
              f"{info['palace']:8s} {info['basin']:8s} {info['rank']:2d} {info['element']:6s} "
              f"{info['surface_rel']:4s} {info['comp_opp']:8.4f} {info['score']:+6.2f}")

    print()
    print("  BOTTOM 10 (low d2_diff − d3_diff → predicted least complement-opposed):")
    print(f"  {'#':>2s} {'hex':>3s} {'binary':>6s} {'KW':>3s} {'Name':12s} {'HW':>2s} {'Upper':8s} {'Lower':8s} "
          f"{'Palace':8s} {'Basin':8s} {'Rk':>2s} {'Elem':6s} {'Rel':4s} {'comp_opp':>8s} {'score':>6s}")
    print("  " + "-" * 110)
    for i, h in enumerate(bot10):
        info = hex_info(h)
        print(f"  {i+1:2d} {info['hex_val']:3d} {info['binary']:>6s} {info['kw']:3d} {info['name']:12s} "
              f"{info['hw']:2d} {info['upper']:8s} {info['lower']:8s} "
              f"{info['palace']:8s} {info['basin']:8s} {info['rank']:2d} {info['element']:6s} "
              f"{info['surface_rel']:4s} {info['comp_opp']:8.4f} {info['score']:+6.2f}")

    # B3: Statistical tests
    print()
    print("  B3: Statistical tests on composite score")
    print("  " + "-" * 60)

    # ρ(composite, comp_opp)
    rho, p = spearmanr(composite, avg_comp_opp)
    print(f"  ρ(composite, comp_opp) = {rho:+.4f}  p={p:.4f} {sig(p)}  ← prediction check")

    # ρ(composite, Hamming weight)
    rho, p = spearmanr(composite, hamming_weight)
    print(f"  ρ(composite, Hamming_weight) = {rho:+.4f}  p={p:.4f} {sig(p)}")

    # ρ(composite, KW number)
    kw_numbers = np.array([atlas[str(h)]['kw_number'] for h in range(N_HEX)])
    rho, p = spearmanr(composite, kw_numbers)
    print(f"  ρ(composite, KW_number) = {rho:+.4f}  p={p:.4f} {sig(p)}")

    # ρ(composite, rank)
    ranks = np.array([atlas[str(h)]['rank'] for h in range(N_HEX)])
    rho, p = spearmanr(composite, ranks)
    print(f"  ρ(composite, rank) = {rho:+.4f}  p={p:.4f} {sig(p)}")

    # ρ(composite, text length)
    rho, p = spearmanr(composite, yaoci_lengths)
    print(f"  ρ(composite, text_length) = {rho:+.4f}  p={p:.4f} {sig(p)}")

    # ρ(composite, depth)
    depths = np.array([atlas[str(h)]['depth'] for h in range(N_HEX)])
    rho, p = spearmanr(composite, depths)
    print(f"  ρ(composite, depth) = {rho:+.4f}  p={p:.4f} {sig(p)}")

    # Kruskal-Wallis by palace
    palaces = [atlas[str(h)]['palace'] for h in range(N_HEX)]
    palace_groups = {}
    for h in range(N_HEX):
        palace_groups.setdefault(palaces[h], []).append(composite[h])
    groups = list(palace_groups.values())
    H_stat, p = kruskal(*groups)
    print(f"  Kruskal-Wallis by palace (8 groups): H={H_stat:.3f}  p={p:.4f} {sig(p)}")

    # Show palace means
    print(f"    {'Palace':10s} {'n':>3s} {'mean':>8s} {'std':>8s}")
    for pal in sorted(palace_groups.keys()):
        vals = palace_groups[pal]
        print(f"    {pal:10s} {len(vals):3d} {np.mean(vals):+8.3f} {np.std(vals):8.3f}")

    # Kruskal-Wallis by basin
    basins = [atlas[str(h)]['basin'] for h in range(N_HEX)]
    basin_groups = {}
    for h in range(N_HEX):
        basin_groups.setdefault(basins[h], []).append(composite[h])
    groups = list(basin_groups.values())
    H_stat, p = kruskal(*groups)
    print(f"\n  Kruskal-Wallis by basin: H={H_stat:.3f}  p={p:.4f} {sig(p)}")

    # Show basin means
    print(f"    {'Basin':10s} {'n':>3s} {'mean':>8s} {'std':>8s}")
    for bas in sorted(basin_groups.keys()):
        vals = basin_groups[bas]
        print(f"    {bas:10s} {len(vals):3d} {np.mean(vals):+8.3f} {np.std(vals):8.3f}")

    # Kruskal-Wallis by surface relation
    surf_rels = [atlas[str(h)]['surface_relation'] for h in range(N_HEX)]
    surf_groups = {}
    for h in range(N_HEX):
        surf_groups.setdefault(surf_rels[h], []).append(composite[h])
    groups = list(surf_groups.values())
    H_stat, p = kruskal(*groups)
    print(f"\n  Kruskal-Wallis by surface_relation: H={H_stat:.3f}  p={p:.4f} {sig(p)}")
    print(f"    {'Relation':10s} {'n':>3s} {'mean':>8s} {'std':>8s}")
    for rel in sorted(surf_groups.keys()):
        vals = surf_groups[rel]
        print(f"    {rel:10s} {len(vals):3d} {np.mean(vals):+8.3f} {np.std(vals):8.3f}")

    # Kruskal-Wallis by Hamming weight
    hw_groups = {}
    for h in range(N_HEX):
        hw_groups.setdefault(hamming_weight[h], []).append(composite[h])
    groups = [hw_groups[k] for k in sorted(hw_groups.keys())]
    H_stat, p = kruskal(*groups)
    print(f"\n  Kruskal-Wallis by Hamming weight: H={H_stat:.3f}  p={p:.4f} {sig(p)}")
    print(f"    {'HW':>3s} {'n':>3s} {'mean':>8s} {'std':>8s}")
    for hw in sorted(hw_groups.keys()):
        vals = hw_groups[hw]
        print(f"    {hw:3d} {len(vals):3d} {np.mean(vals):+8.3f} {np.std(vals):8.3f}")

    # B4: Per-model consistency
    print()
    print("  B4: Per-model consistency of composite score")
    print(f"  {'':14s} |", end="")
    for m2 in MODEL_ORDER:
        print(f" {m2[:6]:>8s}", end="")
    print()
    print("  " + "-" * 55)
    for m1 in MODEL_ORDER:
        row = f"  {m1:14s} |"
        for m2 in MODEL_ORDER:
            if m2 == m1:
                row += "      — "
            else:
                rho, _ = spearmanr(per_model_scores[m1], per_model_scores[m2])
                row += f" {rho:+.3f}  "
        print(row)

    # B5: Verify prediction: ρ(composite, comp_opp) per model
    print()
    print("  B5: ρ(composite, comp_opp) per model:")
    for mname in MODEL_ORDER:
        co = results[mname]['comp_opp']
        rho, p = spearmanr(per_model_scores[mname], co)
        print(f"    {mname:14s}: ρ = {rho:+.4f}  p={p:.4f} {sig(p)}")


# ══════════════════════════════════════════════════════════════════════

def main():
    atlas, results, yaoci_lengths, hex_to_kw = load_all()
    thread_a(results, yaoci_lengths)
    thread_b(atlas, results, yaoci_lengths, hex_to_kw)

if __name__ == "__main__":
    main()
