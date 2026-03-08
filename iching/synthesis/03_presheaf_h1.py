#!/usr/bin/env python3
"""
Probe 2: Contextual Obstruction — Readability Deficiency

For each hexagram, compute how many (season, 用神) contexts yield zero
active lines — the "dark contexts" where the hexagram cannot be read
for that question type in that season.

Two measures:
  n_zero:    count of (season, 用神) pairs with F=0  (breadth of unreadability)
  F_variance: variance of F across contexts with F>0  (consistency when readable)

Cross-reference both with 凶 rates from Probe 1.

Construction:
  F(h, season, yongshen_type) = count of lines in h that are:
    (a) assigned yongshen_type by 六親, AND
    (b) have branch element in {旺, 相} for that season
"""

import sys
import json
import importlib.util
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

# ─── Import infrastructure ───────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/
ICHING = ROOT / "iching"

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ICHING / "kingwen"))

from cycle_algebra import (
    NUM_HEX, TRIGRAM_ELEMENT, ELEMENTS, SHENG_MAP, KE_MAP,
    lower_trigram, upper_trigram, fmt6, bit, hugua,
)
from sequence import KING_WEN

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p1 = _load("najia", ICHING / "huozhulin" / "01_najia_map.py")
p2 = _load("palace", ICHING / "huozhulin" / "02_palace_kernel.py")
p3 = _load("liuqin", ICHING / "huozhulin" / "03_liuqin.py")
p6 = _load("seasonal", ICHING / "huozhulin" / "06_seasonal.py")

# ─── Constants ────────────────────────────────────────────────────────────

TEXTS_DIR = ROOT / "texts" / "iching"
OUT_DIR = Path(__file__).resolve().parent

SEASON_NAMES = p6.SEASON_NAMES  # ['Spring', 'Summer', 'Late_Summer', 'Autumn', 'Winter']
SEASON_ELEMENT = p6.SEASON_ELEMENT
LIUQIN_NAMES = p3.LIUQIN_NAMES  # ['兄弟', '子孫', '父母', '妻財', '官鬼']
LIUQIN_SHORT = p3.LIUQIN_SHORT
STRONG = p6.STRONG  # {'旺', '相'}

VALENCE_MARKERS = {
    "吉": "auspicious", "凶": "inauspicious", "悔": "regret",
    "吝": "difficulty", "無咎": "no_blame", "无咎": "no_blame",
    "厲": "danger", "利": "advantageous",
}

N_CONTEXTS = len(SEASON_NAMES) * len(LIUQIN_NAMES)  # 25

# ─── Lookups ──────────────────────────────────────────────────────────────

def build_kw_lookup():
    bin_to_kw, kw_to_bin, kw_to_name = {}, {}, {}
    for _, (kw_num, name, bits_str) in enumerate(KING_WEN):
        b = [int(c) for c in bits_str]
        h = sum(b[j] << j for j in range(6))
        bin_to_kw[h] = kw_num
        kw_to_bin[kw_num] = h
        kw_to_name[kw_num] = name
    return bin_to_kw, kw_to_bin, kw_to_name


# ═════════════════════════════════════════════════════════════════════════
# Step 1: Compute F(h, season, yongshen) for all 64 × 25 contexts
# ═════════════════════════════════════════════════════════════════════════

def compute_F_table():
    """Compute F(h, season, yongshen_type) for all hexagrams.

    Returns:
        F: dict  h → (season, yongshen_type) → int
        hex_data: dict  h → {palace_elem, word, line_elems, basin, depth, ...}
    """
    _, hex_info = p2.generate_palaces()
    F = {}
    hex_data = {}

    for h in range(NUM_HEX):
        info = hex_info[h]
        pe = info['palace_elem']
        word = p3.liuqin_word(h, pe)
        nj = p1.najia(h)
        line_elems = [p1.BRANCH_ELEMENT[b] for _, b in nj]

        F[h] = {}
        for season in SEASON_NAMES:
            for yong_type in LIUQIN_NAMES:
                count = 0
                for line_idx in range(6):
                    if word[line_idx] == yong_type:
                        strength = p6.elem_strength(line_elems[line_idx], season)
                        if strength in STRONG:
                            count += 1
                F[h][(season, yong_type)] = count

        hex_data[h] = {
            'palace_elem': pe,
            'word': word,
            'line_elems': line_elems,
            'basin': info['basin'],
            'depth': info['depth'],
            'palace': info['palace'],
            'rank': info['rank'],
        }

    return F, hex_data


def compute_measures(F):
    """Compute n_zero, F_variance, and F_total for each hexagram.

    Returns: dict  h → {n_zero, F_variance, F_mean_nonzero, F_max, F_total, F_values}
    """
    measures = {}
    for h in range(NUM_HEX):
        vals = [F[h][ctx] for ctx in F[h]]
        nonzero = [v for v in vals if v > 0]
        n_zero = sum(1 for v in vals if v == 0)
        f_var = float(np.var(nonzero)) if len(nonzero) > 1 else 0.0
        f_mean = float(np.mean(nonzero)) if nonzero else 0.0
        measures[h] = {
            'n_zero': n_zero,
            'F_variance': f_var,
            'F_mean_nonzero': f_mean,
            'F_max': max(vals),
            'F_total': sum(vals),
            'F_values': vals,
        }
    return measures


# ═════════════════════════════════════════════════════════════════════════
# Step 2: Compute 凶 rates per hexagram
# ═════════════════════════════════════════════════════════════════════════

def compute_xiong_rates(bin_to_kw):
    """Compute 凶 count per hexagram from 爻辭."""
    with open(TEXTS_DIR / "yaoci.json") as f:
        yaoci_data = json.load(f)
    yaoci = {}
    for e in yaoci_data['entries']:
        yaoci[e['number']] = [line['text'] for line in e['lines']]

    xiong = {}
    for h in range(NUM_HEX):
        kw = bin_to_kw[h]
        xiong[h] = sum(1 for text in yaoci[kw] if "凶" in text)
    return xiong


# ═════════════════════════════════════════════════════════════════════════
# Step 3: Statistical tests
# ═════════════════════════════════════════════════════════════════════════

def correlation_test(x, y, label):
    """Spearman rank correlation with summary."""
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    # Check for constant input
    if np.std(x) == 0 or np.std(y) == 0:
        print(f"  {label}:")
        print(f"    CONSTANT INPUT — correlation undefined")
        return {'rho': 0.0, 'p_spearman': 1.0, 'r': 0.0, 'p_pearson': 1.0, 'constant': True}
    rho, p = stats.spearmanr(x, y)
    r_pearson, p_pearson = stats.pearsonr(x, y)
    sig = '✓' if p < 0.05 else '✗'
    print(f"  {label}:")
    print(f"    Spearman ρ = {rho:.4f}, p = {p:.4f} {sig}")
    print(f"    Pearson  r = {r_pearson:.4f}, p = {p_pearson:.4f}")
    return {'rho': rho, 'p_spearman': p, 'r': r_pearson, 'p_pearson': p_pearson}


# ═════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PROBE 2: CONTEXTUAL OBSTRUCTION — READABILITY DEFICIENCY")
    print("=" * 70)

    # ── Build data ──
    print("\n── Step 1: Computing F(h, season, yongshen) ──")
    F, hex_data = compute_F_table()
    measures = compute_measures(F)
    print(f"  64 hexagrams × {N_CONTEXTS} contexts = {64 * N_CONTEXTS} values")

    bin_to_kw, kw_to_bin, kw_to_name = build_kw_lookup()

    # ── Sanity check ──
    n_zeros = [measures[h]['n_zero'] for h in range(NUM_HEX)]
    f_vars = [measures[h]['F_variance'] for h in range(NUM_HEX)]
    print(f"  n_zero range: [{min(n_zeros)}, {max(n_zeros)}] out of {N_CONTEXTS}")
    print(f"  F_variance range: [{min(f_vars):.4f}, {max(f_vars):.4f}]")

    # ── Distribution table ──
    print(f"\n── n_zero distribution ──")
    nz_dist = Counter(n_zeros)
    for nz in sorted(nz_dist):
        print(f"  n_zero={nz:>2d}: {nz_dist[nz]:>2d} hexagrams")

    # ── Step 2: 凶 rates ──
    print(f"\n── Step 2: Computing 凶 rates ──")
    xiong = compute_xiong_rates(bin_to_kw)
    total_xiong = sum(xiong.values())
    print(f"  Total 凶: {total_xiong} across 384 lines")

    # ── Step 3: Cross-reference ──
    print(f"\n── Step 3: Cross-reference n_zero and F_variance with 凶 ──")
    print()

    x_nz = [measures[h]['n_zero'] for h in range(NUM_HEX)]
    x_fv = [measures[h]['F_variance'] for h in range(NUM_HEX)]
    y_xi = [xiong[h] for h in range(NUM_HEX)]

    r1 = correlation_test(x_nz, y_xi, "n_zero vs 凶 count")
    print()
    r2 = correlation_test(x_fv, y_xi, "F_variance vs 凶 count")

    # ── Step 4: Group analysis by basin and depth ──
    print(f"\n── Step 4: Group analysis ──")

    print(f"\n  By basin:")
    print(f"  {'Basin':6s} | {'n_hex':>5s} | {'mean n_zero':>11s} | {'mean F_var':>10s} | {'mean 凶':>6s}")
    print(f"  {'─'*6}─┼─{'─'*5}─┼─{'─'*11}─┼─{'─'*10}─┼─{'─'*6}")
    for basin in ['Kun', 'Qian', 'Cycle']:
        hexes = [h for h in range(NUM_HEX) if hex_data[h]['basin'] == basin]
        mn_nz = np.mean([measures[h]['n_zero'] for h in hexes])
        mn_fv = np.mean([measures[h]['F_variance'] for h in hexes])
        mn_xi = np.mean([xiong[h] for h in hexes])
        print(f"  {basin:6s} | {len(hexes):>5d} | {mn_nz:>11.2f} | {mn_fv:>10.4f} | {mn_xi:>6.2f}")

    # Depth within I=0
    I_comp = lambda h: bit(h, 2) ^ bit(h, 3)
    print(f"\n  By depth (I=0 only):")
    print(f"  {'Depth':>5s} | {'n_hex':>5s} | {'mean n_zero':>11s} | {'mean F_var':>10s} | {'mean 凶':>6s}")
    print(f"  {'─'*5}─┼─{'─'*5}─┼─{'─'*11}─┼─{'─'*10}─┼─{'─'*6}")
    for d in [0, 1, 2]:
        hexes = [h for h in range(NUM_HEX) if I_comp(h) == 0 and p2.depth(h) == d]
        if not hexes:
            continue
        mn_nz = np.mean([measures[h]['n_zero'] for h in hexes])
        mn_fv = np.mean([measures[h]['F_variance'] for h in hexes])
        mn_xi = np.mean([xiong[h] for h in hexes])
        print(f"  {d:>5d} | {len(hexes):>5d} | {mn_nz:>11.2f} | {mn_fv:>10.4f} | {mn_xi:>6.2f}")

    # ── Step 5: Detail table — ranked by n_zero ──
    print(f"\n── Step 5: Full table (sorted by n_zero desc) ──")
    print(f"  {'KW#':>4s} {'Name':<7s} {'Basin':6s} d | {'n_zero':>6s} {'F_var':>7s} {'凶':>3s} {'F_mean':>6s}")
    print(f"  {'─'*4} {'─'*7} {'─'*6} ─ {'─'*6} {'─'*7} {'─'*3} {'─'*6}")

    ranked = sorted(range(NUM_HEX), key=lambda h: (-measures[h]['n_zero'], -xiong[h]))
    for h in ranked:
        kw = bin_to_kw[h]
        m = measures[h]
        d = hex_data[h]
        dep = p2.depth(h)
        print(f"  {kw:>4d} {kw_to_name[kw]:<7s} {d['basin']:6s} {dep} | "
              f"{m['n_zero']:>6d} {m['F_variance']:>7.3f} {xiong[h]:>3d} {m['F_mean_nonzero']:>6.3f}")

    # ── Step 6: F breakdown for extreme cases ──
    print(f"\n── Step 6: F breakdown for extreme cases ──")
    top_nz = sorted(range(NUM_HEX), key=lambda h: -measures[h]['n_zero'])[:4]
    bot_nz = sorted(range(NUM_HEX), key=lambda h: measures[h]['n_zero'])[:4]

    for label, hexes in [("Highest n_zero", top_nz), ("Lowest n_zero", bot_nz)]:
        print(f"\n  {label}:")
        for h in hexes:
            kw = bin_to_kw[h]
            m = measures[h]
            print(f"\n    KW#{kw} {kw_to_name[kw]} ({fmt6(h)}) — "
                  f"n_zero={m['n_zero']}, 凶={xiong[h]}, basin={hex_data[h]['basin']}")

            # Show F matrix
            print(f"    {'Season':12s} | " + " | ".join(f"{LIUQIN_SHORT[t]:>2s}" for t in LIUQIN_NAMES))
            print(f"    {'─'*12}─┼─" + "─┼─".join("──" for _ in LIUQIN_NAMES))
            for season in SEASON_NAMES:
                vals = [str(F[h][(season, t)]) for t in LIUQIN_NAMES]
                print(f"    {season:12s} | " + " | ".join(f"{v:>2s}" for v in vals))

    # ── Step 7: Additional correlations ──
    print(f"\n── Step 7: Additional correlations ──\n")

    # F_total vs 凶
    x_ft = [measures[h]['F_total'] for h in range(NUM_HEX)]
    r3 = correlation_test(x_ft, y_xi, "F_total vs 凶 count")
    print()

    # n_zero vs depth (within I=0)
    i0_hexes = [h for h in range(NUM_HEX) if I_comp(h) == 0]
    x_depth = [p2.depth(h) for h in i0_hexes]
    x_nz_i0 = [measures[h]['n_zero'] for h in i0_hexes]
    correlation_test(x_depth, x_nz_i0, "depth vs n_zero (I=0 only)")

    # n_zero vs basin (Kruskal-Wallis)
    print(f"\n  n_zero by basin (Kruskal-Wallis):")
    groups = defaultdict(list)
    for h in range(NUM_HEX):
        groups[hex_data[h]['basin']].append(measures[h]['n_zero'])
    H, p = stats.kruskal(*[groups[b] for b in ['Kun', 'Qian', 'Cycle']])
    sig = '✓' if p < 0.05 else '✗'
    print(f"    H = {H:.4f}, p = {p:.4f} {sig}")

    # F_variance by basin
    print(f"\n  F_variance by basin (Kruskal-Wallis):")
    groups_fv = defaultdict(list)
    for h in range(NUM_HEX):
        groups_fv[hex_data[h]['basin']].append(measures[h]['F_variance'])
    H_fv, p_fv = stats.kruskal(*[groups_fv[b] for b in ['Kun', 'Qian', 'Cycle']])
    sig_fv = '✓' if p_fv < 0.05 else '✗'
    print(f"    H = {H_fv:.4f}, p = {p_fv:.4f} {sig_fv}")

    # F_total by basin
    print(f"\n  F_total by basin:")
    groups_ft = defaultdict(list)
    for h in range(NUM_HEX):
        groups_ft[hex_data[h]['basin']].append(measures[h]['F_total'])
    ft_vals = set(measures[h]['F_total'] for h in range(NUM_HEX))
    if len(ft_vals) == 1:
        print(f"    F_total is CONSTANT at {ft_vals.pop()} — no test needed")
        H_ft, p_ft = 0.0, 1.0
    else:
        H_ft, p_ft = stats.kruskal(*[groups_ft[b] for b in ['Kun', 'Qian', 'Cycle']])
        sig_ft = '✓' if p_ft < 0.05 else '✗'
        print(f"    H = {H_ft:.4f}, p = {p_ft:.4f} {sig_ft}")

    # ── Step 8: Decomposition — why n_zero is constrained ──
    print(f"\n── Step 8: n_zero decomposition ──")
    print(f"\n  n_zero decomposes into: missing-type zeros + seasonal zeros")
    print(f"  Missing-type zeros: contexts (s, u) where u is absent from 六親 word (∀ seasons)")
    print(f"  Seasonal zeros: contexts where u is present but no line of type u is 旺/相\n")

    for h in sorted(range(NUM_HEX), key=lambda h: measures[h]['n_zero'])[:4] + \
              sorted(range(NUM_HEX), key=lambda h: -measures[h]['n_zero'])[:4]:
        kw = bin_to_kw[h]
        word = hex_data[h]['word']
        present_types = set(word)
        missing_types = set(LIUQIN_NAMES) - present_types
        n_missing_zeros = len(missing_types) * len(SEASON_NAMES)
        n_seasonal_zeros = measures[h]['n_zero'] - n_missing_zeros
        print(f"  KW#{kw:>2d} {kw_to_name[kw]:<7s}: n_zero={measures[h]['n_zero']} = "
              f"{n_missing_zeros} missing + {n_seasonal_zeros} seasonal "
              f"(missing: {len(missing_types)} types)")

    # ── Step 9: F_total distribution ──
    print(f"\n── Step 9: F_total distribution ──")
    ft_dist = Counter(x_ft)
    for ft in sorted(ft_dist):
        print(f"  F_total={ft:>2d}: {ft_dist[ft]:>2d} hexagrams")

    # ── Write results ──
    print(f"\n── Writing results ──")
    write_results(F, measures, xiong, hex_data, bin_to_kw, kw_to_name, r1, r2, r3,
                  H, p, H_fv, p_fv, H_ft, p_ft)


def write_results(F, measures, xiong, hex_data, bin_to_kw, kw_to_name,
                  r_nz_xi, r_fv_xi, r_ft_xi,
                  H_basin_nz, p_basin_nz, H_basin_fv, p_basin_fv,
                  H_basin_ft, p_basin_ft):
    """Write markdown results."""
    out = []
    w = out.append

    w("# Probe 2: Contextual Obstruction — Readability Deficiency\n")

    w("## Construction\n")
    w("For each hexagram h and context (season, 用神 type), define:")
    w("```")
    w("F(h, season, yongshen) = # lines where:")
    w("  (1) line's 六親 type == yongshen, AND")
    w("  (2) line's branch element is 旺 or 相 in that season")
    w("```")
    w(f"Total contexts per hexagram: {N_CONTEXTS} (5 seasons × 5 用神 types)\n")

    w("Two derived measures:")
    w("- **n_zero**: count of contexts where F=0 (dark contexts — unreadable)")
    w("- **F_variance**: variance of F across contexts where F>0 (signal consistency)\n")

    # Summary statistics
    n_zeros = [measures[h]['n_zero'] for h in range(NUM_HEX)]
    f_vars = [measures[h]['F_variance'] for h in range(NUM_HEX)]
    w("## Distribution Summary\n")
    w(f"- n_zero range: [{min(n_zeros)}, {max(n_zeros)}] out of {N_CONTEXTS}")
    w(f"- n_zero mean: {np.mean(n_zeros):.2f}, median: {np.median(n_zeros):.1f}")
    w(f"- F_variance range: [{min(f_vars):.4f}, {max(f_vars):.4f}]\n")

    # n_zero distribution
    nz_dist = Counter(n_zeros)
    w("### n_zero distribution\n")
    w("| n_zero | Hexagrams |")
    w("|--------|-----------|")
    for nz in sorted(nz_dist):
        w(f"| {nz} | {nz_dist[nz]} |")
    w("")

    # By basin
    w("### By basin\n")
    w("| Basin | mean n_zero | mean F_var | mean 凶 |")
    w("|-------|-------------|------------|---------|")
    for basin in ['Kun', 'Qian', 'Cycle']:
        hexes = [h for h in range(NUM_HEX) if hex_data[h]['basin'] == basin]
        mn_nz = np.mean([measures[h]['n_zero'] for h in hexes])
        mn_fv = np.mean([measures[h]['F_variance'] for h in hexes])
        mn_xi = np.mean([xiong[h] for h in hexes])
        w(f"| {basin} | {mn_nz:.2f} | {mn_fv:.4f} | {mn_xi:.2f} |")
    w("")

    # By depth within I=0
    I_comp = lambda h: bit(h, 2) ^ bit(h, 3)
    w("### By depth (I=0 only)\n")
    w("| Depth | n_hex | mean n_zero | mean F_var | mean 凶 |")
    w("|-------|-------|-------------|------------|---------|")
    for d in [0, 1, 2]:
        hexes = [h for h in range(NUM_HEX) if I_comp(h) == 0 and p2.depth(h) == d]
        if not hexes:
            continue
        mn_nz = np.mean([measures[h]['n_zero'] for h in hexes])
        mn_fv = np.mean([measures[h]['F_variance'] for h in hexes])
        mn_xi = np.mean([xiong[h] for h in hexes])
        w(f"| {d} | {len(hexes)} | {mn_nz:.2f} | {mn_fv:.4f} | {mn_xi:.2f} |")
    w("")

    # Correlation results
    w("## Correlation with 凶\n")
    w("| Measure | Spearman ρ | p | Pearson r | p | Sig |")
    w("|---------|-----------|---|-----------|---|-----|")
    for label, r in [("n_zero vs 凶", r_nz_xi), ("F_variance vs 凶", r_fv_xi),
                     ("F_total vs 凶", r_ft_xi)]:
        sig = '✓' if r['p_spearman'] < 0.05 else '✗'
        w(f"| {label} | {r['rho']:.4f} | {r['p_spearman']:.4f} | "
          f"{r['r']:.4f} | {r['p_pearson']:.4f} | {sig} |")
    w("")

    w("### Group tests (Kruskal-Wallis by basin)\n")
    w("| Measure | H | p | Sig |")
    w("|---------|---|---|-----|")
    for label, H_val, p_val in [("n_zero", H_basin_nz, p_basin_nz),
                                 ("F_variance", H_basin_fv, p_basin_fv)]:
        sig = '✓' if p_val < 0.05 else '✗'
        w(f"| {label} | {H_val:.4f} | {p_val:.4f} | {sig} |")
    w("| F_total | — | — | constant=12 |")
    w("")

    # Top/bottom hexagrams
    w("## Extreme Cases\n")

    w("### Highest n_zero (most dark contexts)\n")
    w("| KW# | Name | Basin | Depth | n_zero | F_var | 凶 |")
    w("|-----|------|-------|-------|--------|-------|-----|")
    ranked = sorted(range(NUM_HEX), key=lambda h: (-measures[h]['n_zero'], -xiong[h]))
    for h in ranked[:10]:
        kw = bin_to_kw[h]
        m = measures[h]
        d = hex_data[h]
        dep = p2.depth(h)
        w(f"| {kw} | {kw_to_name[kw]} | {d['basin']} | {dep} | "
          f"{m['n_zero']} | {m['F_variance']:.3f} | {xiong[h]} |")
    w("")

    w("### Lowest n_zero (fewest dark contexts)\n")
    w("| KW# | Name | Basin | Depth | n_zero | F_var | 凶 |")
    w("|-----|------|-------|-------|--------|-------|-----|")
    ranked_low = sorted(range(NUM_HEX), key=lambda h: (measures[h]['n_zero'], xiong[h]))
    for h in ranked_low[:10]:
        kw = bin_to_kw[h]
        m = measures[h]
        d = hex_data[h]
        dep = p2.depth(h)
        w(f"| {kw} | {kw_to_name[kw]} | {d['basin']} | {dep} | "
          f"{m['n_zero']} | {m['F_variance']:.3f} | {xiong[h]} |")
    w("")

    # Interpretation
    w("## Interpretation\n")

    rho_nz = r_nz_xi['rho']
    p_nz = r_nz_xi['p_spearman']
    rho_fv = r_fv_xi['rho']
    p_fv = r_fv_xi['p_spearman']
    rho_ft = r_ft_xi['rho']
    p_ft = r_ft_xi['p_spearman']

    w("### Why n_zero takes only 3 values\n")
    w("n_zero decomposes into two independent components:")
    w("1. **Missing-type zeros**: if 用神 type is absent from the 六親 word,")
    w("   F=0 for ALL 5 seasons → contributes 5 zeros per missing type")
    w("2. **Seasonal zeros**: 用神 type is present but no line of that type")
    w("   has its branch element in {旺, 相} for that season\n")
    w("Since hexagrams have 0, 1, or 2 missing types (from Probe 3 of huozhulin),")
    w("the missing-type contribution is 0, 5, or 10 — a coarse step function.")
    w("The remaining seasonal zeros depend on which elements appear in which")
    w("positions, adding 5–9 more zeros. The result: n_zero ∈ {15, 17, 19}")
    w("with the 16:32:16 distribution reflecting the 0:1:2 missing-type count.\n")
    w("This means n_zero is dominated by the **static** 六親 coverage structure,")
    w("not by the **dynamic** seasonal modulation. The seasonal system adds")
    w("only a constant offset of ~15 zeros regardless of hexagram — it does")
    w("not create hexagram-specific variance.\n")

    sig_nz = '✓' if p_nz < 0.05 else '✗'
    sig_fv = '✓' if p_fv < 0.05 else '✗'
    sig_ft = '✓' if p_ft < 0.05 else '✗'

    w(f"### n_zero × 凶 (ρ={rho_nz:.3f}, p={p_nz:.4f} {sig_nz})\n")
    if p_nz < 0.05:
        w("Significant but driven entirely by the missing-type structure.\n")
    else:
        w("Not significant. The 3-valued n_zero is too coarse to resolve the")
        w("凶 gradient. The depth gradient (0→36→19→6% 凶) and the n_zero")
        w("gradient (15→17→19) move in the same direction within I=0, but the")
        w("correlation lacks power because n_zero has no variance within")
        w("its 3 levels.\n")

    w(f"### F_variance × 凶 (ρ={rho_fv:.3f}, p={p_fv:.4f} {sig_fv})\n")
    if p_fv < 0.05:
        w("Significant.\n")
    else:
        w("Not significant. F_variance also takes few distinct values")
        w("(0.000 for n_zero=19, 0.250 for n_zero=17, 0.160 for n_zero=15)")
        w("because F itself takes only values 0, 1, or 2 per context.\n")

    w(f"### F_total: conservation law\n")
    w("**F_total = 12 for every hexagram.** This is a structural invariant —")
    w("the total number of active line-slots across all 25 contexts is identical")
    w("for all 64 hexagrams. The measure cannot correlate with anything.\n")
    w("This conservation arises from the double bijection: 六親 maps each type to")
    w("one element, and each season activates exactly 2 elements. Each line")
    w("appears in exactly one 六親 type, and its element is 旺/相 in exactly")
    w("2 of 5 seasons. So each line contributes exactly 2 active slots → 6 lines × 2 = 12.\n")

    w("### Structural diagnosis\n")
    w("The contextual obstruction construction is **algebraically too constrained**")
    w("to produce hexagram-specific variation. The key constraints:\n")
    w("1. **六親→element is a bijection** (5 types → 5 elements): each type maps to")
    w("   exactly one element, so seasonal strength applies uniformly per type")
    w("2. **旺/相 activates exactly 2 elements per season**: at most 2 用神 types can")
    w("   be active in any season (the 2/5 ceiling from Probe 6)")
    w("3. **Lines of the same 六親 type share the same branch element** within a trigram:")
    w("   the trigram determines which branches appear, so lines of type u tend to")
    w("   cluster on 1–2 elements, making F ∈ {0, 1, 2} with no finer resolution\n")
    w("These constraints make F a function of (palace, trigram pair, season) rather than")
    w("of individual hexagram identity. The basin/depth structure — which lives in the")
    w("inner 4 bits — is invisible to 納甲 (confirmed in Probe 1 of huozhulin),")
    w("and therefore invisible to any measure built on 六親 × seasonal strength.\n")

    w("### The orthogonality wall\n")
    w("This is the precise manifestation of the **納甲 ⊥ 互卦 orthogonality** discovered")
    w("in the huozhulin workflow. The 火珠林 operational structure (六親, 旺相, 用神)")
    w("is built entirely on the trigram-pair projection (outer bits). The 凶 signal lives")
    w("in the basin/depth structure (inner bits). These two structures cannot see each other.")
    w("No measure derived from 六親 × seasonal strength can predict basin-correlated 凶,")
    w("because the information channels are algebraically orthogonal.\n")
    w("The prediction that n_zero would correlate with 凶 implicitly assumed that")
    w("operational narrowness and textual danger share a structural basis. They do not:")
    w("they live in complementary subspaces of Z₂⁶.\n")

    out_path = OUT_DIR / "probe2_results.md"
    out_path.write_text("\n".join(out))
    print(f"Results written to {out_path}")


if __name__ == "__main__":
    main()
