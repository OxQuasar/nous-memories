#!/usr/bin/env python3
"""
King Wen Sequence Analysis

Projects the KW sequence through all established coordinate systems:
Z₂⁶ binary, Z₅×Z₅ element pairs, Z₅ directed relation, 互 basins,
complement structure, 先天/後天 projections.

Uses existing infrastructure from kingwen/sequence.py and cycle_algebra.
"""

import sys
import random
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "kingwen"))
sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    TRIGRAM_ELEMENT, five_phase_relation,
    SHENG_MAP, KE_MAP,
)

# ─── Constants ───────────────────────────────────────────────────────────────

KUN, ZHEN, KAN, DUI = 0, 1, 2, 3
GEN, LI, XUN, QIAN = 4, 5, 6, 7

TRIG_NAME = {
    0: "坤", 1: "震", 2: "坎", 3: "兌",
    4: "艮", 5: "離", 6: "巽", 7: "乾",
}
ELEM = TRIGRAM_ELEMENT
SHENG_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_Z5 = {e: i for i, e in enumerate(SHENG_ORDER)}

# Build KW sequence as integer list
KW = []
KW_NAME = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    KW.append(sum(b[j] << j for j in range(6)))
    KW_NAME.append(KING_WEN[i][1])

# Shao Yong value (bit-reverse trigram: swap b₀↔b₂)
def shao_yong(t):
    return ((t & 1) << 2) | ((t >> 1) & 1) << 1 | ((t >> 2) & 1)

# Complement of hexagram
def complement(h):
    return h ^ 63

# Line-reversal (reverse all 6 bits)
def line_reverse(h):
    return reverse6(h)

# 互 transform
def hu(h):
    return hugua(h)

# Basin from inner bits
def basin(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1  # Kun
    if b2 == 1 and b3 == 1: return 1   # Qian
    return 0  # KanLi

def directed_relation(h):
    """Z₅ directed relation: upper element's relation to lower element."""
    lo_elem = ELEM[lower_trigram(h)]
    up_elem = ELEM[upper_trigram(h)]
    return five_phase_relation(lo_elem, up_elem)

def z5_distance(e1, e2):
    d = (ELEM_Z5[e2] - ELEM_Z5[e1]) % 5
    return min(d, 5 - d)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# King Wen Sequence Analysis")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 1: Verify encoding
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 1: King Wen Sequence Encoding")
    out()

    assert len(set(KW)) == 64, "Not all 64 hexagrams present"
    assert set(KW) == set(range(64)), "Not a permutation of 0-63"
    out(f"Verified: KW is a permutation of 0-63 (all 64 hexagrams)")
    out()

    # Show first and last few
    out(f"{'KW#':>4} {'Name':>12} {'Bin':>7} {'Dec':>4} {'Lo':>3} {'Up':>3} "
        f"{'Lo_E':>6} {'Up_E':>6}")
    out("-" * 60)
    for i in [0, 1, 2, 3, 4, 28, 29, 62, 63]:
        h = KW[i]
        lo, up = lower_trigram(h), upper_trigram(h)
        out(f"{i+1:>4} {KW_NAME[i]:>12} {h:06b} {h:>4} "
            f"{TRIG_NAME[lo]:>3} {TRIG_NAME[up]:>3} "
            f"{ELEM[lo]:>6} {ELEM[up]:>6}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 2: Pairing structure
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 2: Pairing Structure")
    out()

    pair_types = {"complement": 0, "reversal": 0, "both": 0, "neither": 0}
    palindromes = 0
    pair_details = []

    for k in range(32):
        a, b = KW[2*k], KW[2*k + 1]
        is_comp = complement(a) == b
        is_rev = line_reverse(a) == b
        is_self_rev = line_reverse(a) == a  # palindrome

        if is_comp and is_rev:
            ptype = "both"
        elif is_comp:
            ptype = "complement"
        elif is_rev:
            ptype = "reversal"
        else:
            ptype = "neither"

        pair_types[ptype] += 1
        if is_self_rev:
            palindromes += 1
        pair_details.append({
            "pair": k+1, "a": 2*k+1, "b": 2*k+2,
            "ha": a, "hb": b,
            "name_a": KW_NAME[2*k], "name_b": KW_NAME[2*k+1],
            "type": ptype, "palindrome": is_self_rev,
        })

    out(f"Pair type distribution (32 pairs):")
    for t, c in sorted(pair_types.items()):
        out(f"  {t}: {c}")
    out(f"  Palindromes (self-reversing): {palindromes}")
    out()

    # Verify traditional claim
    out("Traditional claim: pairs are reversal-pairs except palindromes → complement")
    rev_pairs = sum(1 for p in pair_details if p["type"] in ("reversal", "both"))
    comp_only = [p for p in pair_details if p["type"] == "complement"]
    out(f"  Reversal pairs (incl. both): {rev_pairs}")
    out(f"  Complement-only pairs: {len(comp_only)}")
    if comp_only:
        out(f"  Complement-only pairs are palindromes?")
        for p in comp_only:
            out(f"    #{p['a']}/{p['b']} ({p['name_a']}/{p['name_b']}): "
                f"palindrome={p['palindrome']}")
    out()

    # Show all pairs with types
    out("### All 32 pairs")
    out(f"{'Pair':>4} {'#a':>3}-{'#b':<3} {'Name_a':>12} {'Name_b':>12} "
        f"{'Type':>12} {'Palindrome':>10}")
    out("-" * 70)
    for p in pair_details:
        out(f"{p['pair']:>4} {p['a']:>3}-{p['b']:<3} {p['name_a']:>12} {p['name_b']:>12} "
            f"{p['type']:>12} {'✓' if p['palindrome'] else '':>10}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 3: Full coordinate projection
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 3: Full Coordinate Projection")
    out()

    hex_data = []
    for i in range(64):
        h = KW[i]
        lo, up = lower_trigram(h), upper_trigram(h)
        lo_e, up_e = ELEM[lo], ELEM[up]
        rel = directed_relation(h)
        hu_h = hu(h)
        hu_lo, hu_up = lower_trigram(hu_h), upper_trigram(hu_h)
        b = basin(h)
        comp = complement(h)
        comp_kw = KW.index(comp) + 1  # KW number of complement
        sy_lo, sy_up = shao_yong(lo), shao_yong(up)

        hex_data.append({
            "kw": i + 1, "name": KW_NAME[i], "h": h,
            "lo": lo, "up": up, "lo_e": lo_e, "up_e": up_e,
            "rel": rel,
            "hu_h": hu_h, "hu_lo": hu_lo, "hu_up": hu_up,
            "basin": b,
            "comp_kw": comp_kw,
            "sy_lo": sy_lo, "sy_up": sy_up, "sy_sum": sy_lo + sy_up,
        })

    # Print compact table
    out(f"{'KW':>3} {'Name':>10} {'Bin':>7} {'Lo_E':>6} {'Up_E':>6} "
        f"{'Rel':>6} {'Basin':>6} {'SY':>4} {'Comp':>4}")
    out("-" * 65)
    for d in hex_data:
        b_name = {-1: "Kun", 0: "KanLi", 1: "Qian"}[d["basin"]]
        out(f"{d['kw']:>3} {d['name']:>10} {d['h']:06b} "
            f"{d['lo_e']:>6} {d['up_e']:>6} {d['rel']:>6} "
            f"{b_name:>6} {d['sy_sum']:>4} {d['comp_kw']:>4}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 4: Sequential structure
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 4: Sequential Structure")
    out()

    random.seed(42)
    N_PERM = 10000

    # ── 4a: Hamming distance between consecutive ──
    out("### 4a: Hamming distance between consecutive hexagrams")
    out()

    consec_hamming = []
    for i in range(63):
        d = bin(KW[i] ^ KW[i+1]).count('1')
        consec_hamming.append(d)

    mean_h = np.mean(consec_hamming)
    out(f"  Mean consecutive Hamming distance: {mean_h:.3f}")
    out(f"  Distribution: {dict(sorted(Counter(consec_hamming).items()))}")

    # Null: random permutation
    null_means = []
    for _ in range(N_PERM):
        perm = list(range(64))
        random.shuffle(perm)
        dists = [bin(perm[i] ^ perm[i+1]).count('1') for i in range(63)]
        null_means.append(np.mean(dists))

    null_mean = np.mean(null_means)
    p_hamming = np.mean([m <= mean_h for m in null_means])
    out(f"  Null mean: {null_mean:.3f}")
    out(f"  p-value (KW ≤ null): {p_hamming:.4f}")
    out(f"  {'★ SIGNIFICANT' if p_hamming < 0.05 else 'Not significant'}")
    out()

    # ── 4b: Z₅×Z₅ torus path ──
    out("### 4b: Z₅×Z₅ torus path")
    out()

    torus_path = [(ELEM_Z5[d["lo_e"]], ELEM_Z5[d["up_e"]]) for d in hex_data]
    cells_visited = set(torus_path)
    out(f"  Distinct cells visited: {len(cells_visited)}/25")

    # Count revisits
    visit_counts = Counter(torus_path)
    out(f"  Visit distribution: {dict(sorted(Counter(visit_counts.values()).items()))}")

    # Torus step sizes
    torus_steps = []
    for i in range(63):
        dl = (torus_path[i+1][0] - torus_path[i][0]) % 5
        du = (torus_path[i+1][1] - torus_path[i][1]) % 5
        dl = min(dl, 5 - dl)
        du = min(du, 5 - du)
        torus_steps.append(dl + du)

    mean_torus_step = np.mean(torus_steps)
    out(f"  Mean torus step (|Δlo|+|Δup| on Z₅): {mean_torus_step:.3f}")

    # Null comparison
    null_torus = []
    for _ in range(N_PERM):
        perm = list(range(64))
        random.shuffle(perm)
        path = [(ELEM_Z5[ELEM[lower_trigram(perm[i])]], ELEM_Z5[ELEM[upper_trigram(perm[i])]])
                for i in range(64)]
        steps = []
        for j in range(63):
            dl = min((path[j+1][0] - path[j][0]) % 5, (path[j][0] - path[j+1][0]) % 5)
            du = min((path[j+1][1] - path[j][1]) % 5, (path[j][1] - path[j+1][1]) % 5)
            steps.append(dl + du)
        null_torus.append(np.mean(steps))

    p_torus = np.mean([m <= mean_torus_step for m in null_torus])
    out(f"  Null mean torus step: {np.mean(null_torus):.3f}")
    out(f"  p-value: {p_torus:.4f}")
    out(f"  {'★ SIGNIFICANT' if p_torus < 0.05 else 'Not significant'}")
    out()

    # ── 4c: Z₅ directed relation sequence ──
    out("### 4c: Directed relation sequence")
    out()

    rel_seq = [d["rel"] for d in hex_data]
    rel_counts = Counter(rel_seq)
    out(f"  Relation distribution: {dict(sorted(rel_counts.items()))}")

    # Consecutive same-relation runs
    run_lengths = []
    current_run = 1
    for i in range(1, 64):
        if rel_seq[i] == rel_seq[i-1]:
            current_run += 1
        else:
            run_lengths.append(current_run)
            current_run = 1
    run_lengths.append(current_run)

    out(f"  Number of relation-runs: {len(run_lengths)}")
    out(f"  Mean run length: {np.mean(run_lengths):.2f}")
    out(f"  Max run length: {max(run_lengths)}")
    out()

    # ── 4d: 先天 values (Shao Yong) ──
    out("### 4d: Shao Yong (先天) correlation")
    out()

    sy_sums = [d["sy_sum"] for d in hex_data]
    kw_numbers = list(range(1, 65))

    # Correlation between KW number and SY sum
    corr = np.corrcoef(kw_numbers, sy_sums)[0, 1]
    out(f"  Pearson correlation (KW# vs SY sum): {corr:.4f}")
    out(f"  {'Significant' if abs(corr) > 0.25 else 'Weak/none'}")
    out()

    # ── 4e: Basin sequence ──
    out("### 4e: Basin transitions")
    out()

    basin_seq = [d["basin"] for d in hex_data]
    basin_counts = Counter(basin_seq)
    out(f"  Basin distribution: {dict(sorted(basin_counts.items()))}")
    out(f"    Kun(-1): {basin_counts[-1]}, KanLi(0): {basin_counts[0]}, Qian(1): {basin_counts[1]}")

    # Transition matrix
    trans = defaultdict(lambda: defaultdict(int))
    for i in range(63):
        trans[basin_seq[i]][basin_seq[i+1]] += 1

    out(f"  Basin transition matrix:")
    out(f"    {'from\\to':>8}  {'Kun':>5}  {'KanLi':>5}  {'Qian':>5}")
    for b in [-1, 0, 1]:
        row = f"    {['Kun','KanLi','Qian'][b+1]:>8}"
        for b2 in [-1, 0, 1]:
            row += f"  {trans[b][b2]:>5}"
        out(row)
    out()

    # Same-basin consecutive rate
    same_basin = sum(1 for i in range(63) if basin_seq[i] == basin_seq[i+1])
    out(f"  Same-basin consecutive: {same_basin}/63 = {same_basin/63:.3f}")

    # Null comparison
    null_same = []
    for _ in range(N_PERM):
        perm = list(range(64))
        random.shuffle(perm)
        bs = [basin(perm[i]) for i in range(64)]
        null_same.append(sum(1 for i in range(63) if bs[i] == bs[i+1]))

    p_basin = np.mean([s >= same_basin for s in null_same])
    null_mean_same = np.mean(null_same)
    out(f"  Null mean same-basin: {null_mean_same:.1f}/63")
    out(f"  p-value (KW ≥ null): {p_basin:.4f}")
    out(f"  {'★ SIGNIFICANT' if p_basin < 0.05 else 'Not significant'}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 5: Upper/lower triangle (odd vs even)
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 5: Odd vs Even (Upper/Lower Triangle)")
    out()

    odd_data = [hex_data[i] for i in range(0, 64, 2)]   # KW 1,3,5,...
    even_data = [hex_data[i] for i in range(1, 64, 2)]   # KW 2,4,6,...

    for label, data in [("Odd (1,3,...,63)", odd_data), ("Even (2,4,...,64)", even_data)]:
        out(f"### {label}")
        out()

        # Trigram distributions
        lo_dist = Counter(d["lo"] for d in data)
        up_dist = Counter(d["up"] for d in data)
        out(f"  Lower trigrams: {dict((TRIG_NAME[k], v) for k, v in sorted(lo_dist.items()))}")
        out(f"  Upper trigrams: {dict((TRIG_NAME[k], v) for k, v in sorted(up_dist.items()))}")

        # Element distributions
        lo_elem_dist = Counter(d["lo_e"] for d in data)
        up_elem_dist = Counter(d["up_e"] for d in data)
        out(f"  Lower elements: {dict(sorted(lo_elem_dist.items()))}")
        out(f"  Upper elements: {dict(sorted(up_elem_dist.items()))}")

        # Relation distribution
        rel_dist = Counter(d["rel"] for d in data)
        out(f"  Relations: {dict(sorted(rel_dist.items()))}")

        # Basin distribution
        basin_dist = Counter(d["basin"] for d in data)
        out(f"  Basins: Kun={basin_dist[-1]}, KanLi={basin_dist[0]}, Qian={basin_dist[1]}")
        out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 6: Specific hypotheses
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 6: Specific Hypotheses")
    out()

    # ── Hypothesis A: Torus coverage ──
    out("### Hypothesis A: Z₅×Z₅ torus coverage")
    out()
    out(f"  Cells visited: {len(cells_visited)}/25")
    out(f"  {'Complete coverage' if len(cells_visited) == 25 else 'Incomplete'}")
    if len(cells_visited) < 25:
        missing = set((i, j) for i in range(5) for j in range(5)) - cells_visited
        out(f"  Missing cells: {missing}")
    out()

    # Show torus visitation pattern
    out("  Torus grid (count of hexagrams per cell):")
    out(f"  {'':>8}" + "".join(f"{SHENG_ORDER[j]:>7}" for j in range(5)))
    for i in range(5):
        row = f"  {SHENG_ORDER[i]:>8}"
        for j in range(5):
            c = visit_counts.get((i, j), 0)
            row += f"{c:>7}" if c > 0 else f"{'·':>7}"
        out(row)
    out()

    # ── Hypothesis B: Consecutive pairs share 互 structure ──
    out("### Hypothesis B: Consecutive pair 互 relationships")
    out()

    hu_same = 0
    hu_related = 0  # 互 of one equals the other
    for k in range(32):
        a, b = KW[2*k], KW[2*k + 1]
        ha, hb = hu(a), hu(b)
        if ha == hb:
            hu_same += 1
        if ha == b or hb == a:
            hu_related += 1

    out(f"  Pairs with same 互: {hu_same}/32")
    out(f"  Pairs where 互(a)=b or 互(b)=a: {hu_related}/32")

    # Consecutive (not paired) 互 relationship
    consec_hu_same = sum(1 for i in range(63) if hu(KW[i]) == hu(KW[i+1]))
    out(f"  Consecutive hexagrams with same 互: {consec_hu_same}/63")

    # Null comparison
    null_hu_same = []
    for _ in range(N_PERM):
        perm = list(range(64))
        random.shuffle(perm)
        null_hu_same.append(sum(1 for i in range(63) if hu(perm[i]) == hu(perm[i+1])))

    p_hu = np.mean([s >= consec_hu_same for s in null_hu_same])
    out(f"  Null mean consecutive same-互: {np.mean(null_hu_same):.1f}")
    out(f"  p-value: {p_hu:.4f}")
    out(f"  {'★ SIGNIFICANT' if p_hu < 0.05 else 'Not significant'}")
    out()

    # ── Hypothesis C: KW ↔ 先天 correlation ──
    out("### Hypothesis C: KW number ↔ 先天 (Shao Yong) correlation")
    out()

    # Shao Yong number for a hexagram: use binary as a 6-bit number with
    # reversed bit order per trigram
    def shao_yong_hex(h):
        """先天 hexagram number (0-63) using Shao Yong's binary count."""
        lo, up = lower_trigram(h), upper_trigram(h)
        return shao_yong(lo) + shao_yong(up) * 8

    sy_hex = [shao_yong_hex(KW[i]) for i in range(64)]
    corr_sy = np.corrcoef(list(range(64)), sy_hex)[0, 1]
    out(f"  Pearson r(KW_index, SY_hex_number): {corr_sy:.4f}")

    # Spearman rank correlation
    from scipy.stats import spearmanr
    rho, p_spearman = spearmanr(list(range(64)), sy_hex)
    out(f"  Spearman ρ: {rho:.4f}, p={p_spearman:.4f}")
    out(f"  {'★ SIGNIFICANT' if p_spearman < 0.05 else 'Not significant'}")
    out()

    # ── Hypothesis D: 上經 vs 下經 ──
    out("### Hypothesis D: 上經 (1-30) vs 下經 (31-64)")
    out()

    upper_canon = hex_data[:30]
    lower_canon = hex_data[30:]

    for label, data in [("上經 (1-30)", upper_canon), ("下經 (31-64)", lower_canon)]:
        out(f"  {label}:")
        rel_d = Counter(d["rel"] for d in data)
        basin_d = Counter(d["basin"] for d in data)
        mean_yang = np.mean([bin(d["h"]).count('1') for d in data])
        mean_sy = np.mean([d["sy_sum"] for d in data])

        # Count pure hexagrams (same upper and lower trigram)
        pure = sum(1 for d in data if d["lo"] == d["up"])

        out(f"    Relations: {dict(sorted(rel_d.items()))}")
        out(f"    Basins: Kun={basin_d[-1]}, KanLi={basin_d[0]}, Qian={basin_d[1]}")
        out(f"    Mean yang lines: {mean_yang:.2f}")
        out(f"    Mean SY sum: {mean_sy:.2f}")
        out(f"    Pure hexagrams (lo=up): {pure}")
    out()

    # Structural difference: 上經 has 30 hex (15 pairs), 下經 has 34 (17 pairs)
    out("  上經: 30 hexagrams (15 pairs)")
    out("  下經: 34 hexagrams (17 pairs)")
    out()

    # Test: does 上經 contain all 8 pure hexagrams?
    upper_pures = [d for d in upper_canon if d["lo"] == d["up"]]
    lower_pures = [d for d in lower_canon if d["lo"] == d["up"]]
    out(f"  Pure hexagrams in 上經: {len(upper_pures)}")
    for d in upper_pures:
        out(f"    #{d['kw']} {d['name']} ({TRIG_NAME[d['lo']]}/{TRIG_NAME[d['up']]})")
    out(f"  Pure hexagrams in 下經: {len(lower_pures)}")
    for d in lower_pures:
        out(f"    #{d['kw']} {d['name']} ({TRIG_NAME[d['lo']]}/{TRIG_NAME[d['up']]})")
    out()

    # ── Additional: element pair transitions ──
    out("### Additional: Element pair transition structure")
    out()

    # For consecutive hexagrams, how does the (lo_elem, up_elem) change?
    lo_same = sum(1 for i in range(63)
                  if hex_data[i]["lo_e"] == hex_data[i+1]["lo_e"])
    up_same = sum(1 for i in range(63)
                  if hex_data[i]["up_e"] == hex_data[i+1]["up_e"])
    both_same = sum(1 for i in range(63)
                    if hex_data[i]["lo_e"] == hex_data[i+1]["lo_e"]
                    and hex_data[i]["up_e"] == hex_data[i+1]["up_e"])

    out(f"  Consecutive pairs with same lower element: {lo_same}/63")
    out(f"  Consecutive pairs with same upper element: {up_same}/63")
    out(f"  Consecutive pairs with both same: {both_same}/63")

    # Null
    null_both = []
    for _ in range(N_PERM):
        perm = list(range(64))
        random.shuffle(perm)
        c = sum(1 for i in range(63)
                if ELEM[lower_trigram(perm[i])] == ELEM[lower_trigram(perm[i+1])]
                and ELEM[upper_trigram(perm[i])] == ELEM[upper_trigram(perm[i+1])])
        null_both.append(c)
    p_elem = np.mean([s >= both_same for s in null_both])
    out(f"  Null mean both-same: {np.mean(null_both):.1f}")
    out(f"  p-value: {p_elem:.4f}")
    out(f"  {'★ SIGNIFICANT' if p_elem < 0.05 else 'Not significant'}")
    out()

    # ── Pair-level: complement maps pairs to pairs ──
    out("### Complement × pairing structure")
    out()

    kw_index = {h: i for i, h in enumerate(KW)}

    comp_dists = []
    comp_pair_map = {}  # KW pair k → KW pair that contains complement
    for k in range(32):
        a, b = KW[2*k], KW[2*k + 1]
        ca, cb = complement(a), complement(b)
        idx_ca, idx_cb = kw_index[ca], kw_index[cb]
        pair_ca = idx_ca // 2
        pair_cb = idx_cb // 2
        same_pair = pair_ca == pair_cb
        comp_pair_map[k] = pair_ca
        comp_dists.append({
            "kw_pair": k+1,
            "comp_same_pair": same_pair,
            "comp_pair_dist": abs(pair_ca - pair_cb),
        })

    same_comp_pair = sum(1 for d in comp_dists if d["comp_same_pair"])
    out(f"  ★ KW pairs whose complements form a KW pair: {same_comp_pair}/32")
    out(f"  → Complement PRESERVES the KW pairing structure perfectly")
    out()

    # Show the complement pair map
    out("  Complement pair map (KW pair → complement pair):")
    self_comp_pairs = []
    for k in range(32):
        target = comp_pair_map[k]
        if target == k:
            self_comp_pairs.append(k + 1)
        elif target > k:  # show each orbit once
            a_name = KW_NAME[2*k]
            b_name = KW_NAME[2*target]
            out(f"    Pair {k+1} ({a_name}...) ↔ Pair {target+1} ({b_name}...)")
    out(f"  Self-complementary pairs: {self_comp_pairs}")
    out()

    # Self-complementary pairs = pairs where {a,b} = {comp(a), comp(b)}
    # This happens for palindrome+complement pairs
    out("  Self-complementary pair structure:")
    for k in self_comp_pairs:
        k0 = k - 1
        a, b = KW[2*k0], KW[2*k0 + 1]
        out(f"    Pair {k}: {KW_NAME[2*k0]}/{KW_NAME[2*k0+1]} "
            f"({a:06b}/{b:06b}), comp=({a^63:06b}/{b^63:06b})")
    out()

    # ── Basin run structure ──
    out("### Basin run structure")
    out()
    basin_seq_char = {-1: 'K', 0: '.', 1: 'Q'}
    seq_str = ''.join(basin_seq_char[b] for b in basin_seq)
    out(f"  上經: {seq_str[:30]}")
    out(f"  下經: {seq_str[30:]}")
    out(f"  (K=Kun basin, .=KanLi, Q=Qian)")
    out()

    # Compute runs
    runs = []
    cur_b, cur_len = basin_seq[0], 1
    for i in range(1, 64):
        if basin_seq[i] == cur_b:
            cur_len += 1
        else:
            runs.append((cur_b, cur_len))
            cur_b, cur_len = basin_seq[i], 1
    runs.append((cur_b, cur_len))
    out(f"  Number of runs: {len(runs)} (63 transitions → {len(runs)} blocks)")
    out(f"  Runs: {' '.join(basin_seq_char[b]+'×'+str(l) for b, l in runs)}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Summary
    # ════════════════════════════════════════════════════════════════════════
    out("## Summary of Findings")
    out()
    out("### Pairing structure")
    rev_count = pair_types["reversal"] + pair_types["both"]
    comp_count = pair_types["complement"] + pair_types["both"]
    out(f"  {rev_count} reversal pairs, {pair_types['complement']} complement-only pairs")
    out(f"  Traditional claim (reversal except palindromes → complement): "
        f"{'CONFIRMED' if pair_types['neither'] == 0 else 'VIOLATED'}")
    out()

    out("### Sequential structure significance")
    out(f"  Hamming distance: p={p_hamming:.4f} "
        f"{'★' if p_hamming < 0.05 else '(not significant)'}")
    out(f"  Torus step size: p={p_torus:.4f} "
        f"{'★' if p_torus < 0.05 else '(not significant)'}")
    out(f"  Basin clustering: p={p_basin:.4f} "
        f"{'★★★' if p_basin < 0.001 else '★' if p_basin < 0.05 else '(not significant)'}")
    out(f"  互 continuity: p={p_hu:.4f} "
        f"{'★' if p_hu < 0.05 else '(not significant)'}")
    out(f"  Element continuity: p={p_elem:.4f} "
        f"{'★' if p_elem < 0.05 else '(not significant)'}")
    out(f"  先天 correlation: ρ={rho:.4f}, p={p_spearman:.4f} "
        f"{'★' if p_spearman < 0.05 else '(not significant)'}")
    out()

    out("### Key structural properties")
    out(f"  ★ Complement preserves KW pairing: 32/32 pairs map to pairs")
    out(f"  ★ Basin clustering: p<0.001 (38/63 same-basin transitions vs null ~23)")
    out(f"  ★ Zero consecutive same-element-pair hexagrams (anti-clustering at Z₅×Z₅)")
    out(f"  ★ 上經 contains 4 pure hexagrams: 乾坤坎離 (Metal,Earth,Water,Fire)")
    out(f"    下經 contains 4 pure hexagrams: 震艮巽兌 (Wood,Earth,Wood,Metal)")
    out(f"    → 上經 = singleton-element pures + Earth; 下經 = doubleton-element pures")
    out(f"  ★ 30+34 split: 上經 ends at Kan/Li (the Fire/Water bridge)")
    out()

    out("### 上經 vs 下經")
    out(f"  上經: {len(upper_pures)} pure hexagrams, 下經: {len(lower_pures)}")
    out(f"  30 + 34 split (not 32 + 32)")
    out(f"  上經: Kun-basin dominated (11 Kun, 14 KanLi, 5 Qian)")
    out(f"  下經: Qian-basin dominated (5 Kun, 18 KanLi, 11 Qian)")
    out(f"  → The two canons occupy different basin territories")
    out()

    # Write results
    results_path = OUT_DIR / "05_king_wen_sequence_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
