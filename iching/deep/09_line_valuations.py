#!/usr/bin/env python3
"""
Line Text Valuations and the Binary Hierarchy

Analyzes the 384 yaoci (line texts) for valuation markers and tests
whether the algebraic hierarchy of line positions manifests in textual
valuations.
"""

import sys
import json
from pathlib import Path
from collections import Counter, defaultdict
import importlib.util

import numpy as np
from scipy import stats as sp_stats

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
TEXTS_DIR = ROOT / "texts" / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "kingwen"))
sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    TRIGRAM_ELEMENT, five_phase_relation,
)

_spec = importlib.util.spec_from_file_location(
    "palace_kernel", str(ICHING / "huozhulin" / "02_palace_kernel.py"))
_pk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pk)
generate_palaces = _pk.generate_palaces
SHI_BY_RANK = _pk.SHI_BY_RANK
PALACE_ROOTS = _pk.PALACE_ROOTS

# ─── Constants ───────────────────────────────────────────────────────────────

ELEM = TRIGRAM_ELEMENT
SHENG_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]

# KW data
KW = []
KW_NAME = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    KW.append(sum(b[j] << j for j in range(6)))
    KW_NAME.append(KING_WEN[i][1])
KW_INDEX = {h: i for i, h in enumerate(KW)}

def directed_rel(h):
    return five_phase_relation(ELEM[lower_trigram(h)], ELEM[upper_trigram(h)])

def basin_int(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    if b2 == 1 and b3 == 1: return 1
    return 0

BASIN_NAME = {-1: "Kun", 0: "KanLi", 1: "Qian"}

# ─── Load yaoci ──────────────────────────────────────────────────────────────

def load_yaoci():
    with open(TEXTS_DIR / "yaoci.json") as f:
        data = json.load(f)
    yaoci = {}
    for entry in data["entries"]:
        yaoci[entry["number"]] = entry
    return yaoci

# ─── Valuation extraction ────────────────────────────────────────────────────

# Positive markers: 吉, 无咎/無咎, 亨
# Negative markers: 凶, 悔, 吝, 厲, 咎 (when not 无咎)
# Note: a line can have both positive and negative markers (e.g., "厲，无咎")

POSITIVE_MARKERS = ["吉", "元吉", "大吉"]
NEGATIVE_MARKERS = ["凶"]
NEUTRAL_POSITIVE = ["无咎", "無咎"]
MILD_NEGATIVE = ["悔", "吝", "厲"]

def classify_line(text):
    """Classify a line text into valuation categories.
    
    Returns dict with:
      ji: bool (contains 吉)
      xiong: bool (contains 凶)
      wu_jiu: bool (contains 无咎/無咎)
      hui: bool (contains 悔)
      lin: bool (contains 吝)
      li: bool (contains 厲)
      heng: bool (contains 亨)
      positive: bool (has any positive marker)
      negative: bool (has any clear negative marker)
      valence: "positive", "negative", "mixed", or "neutral"
    """
    ji = "吉" in text
    xiong = "凶" in text
    wu_jiu = "无咎" in text or "無咎" in text
    hui = "悔" in text and "无悔" not in text  # exclude 无悔
    lin = "吝" in text
    li = "厲" in text
    heng = "亨" in text
    
    has_positive = ji or wu_jiu
    has_negative = xiong or hui or lin or li
    
    if has_positive and has_negative:
        valence = "mixed"
    elif has_positive:
        valence = "positive"
    elif has_negative:
        valence = "negative"
    else:
        valence = "neutral"
    
    return {
        "ji": ji, "xiong": xiong, "wu_jiu": wu_jiu,
        "hui": hui, "lin": lin, "li": li, "heng": heng,
        "positive": has_positive, "negative": has_negative,
        "valence": valence,
    }


# ─── Build records ───────────────────────────────────────────────────────────

def build_records(yaoci):
    """Build 384 records with hex info + valuation."""
    with open(ICHING / "atlas" / "atlas.json") as f:
        atlas = json.load(f)
    
    entries_p, hex_info = generate_palaces()
    
    records = []
    for h in range(64):
        a = atlas[str(h)]
        kw_num = a["kw_number"]
        entry = yaoci[kw_num]
        p_info = hex_info[h]
        shi_line = p_info['shi']
        
        for line_idx in range(6):
            line_pos = line_idx + 1
            text = entry["lines"][line_idx]["text"]
            val = classify_line(text)
            
            records.append({
                "hex_val": h,
                "kw_number": kw_num,
                "line": line_pos,
                "text": text,
                "surface_relation": a["surface_relation"],
                "basin": BASIN_NAME[basin_int(h)],
                "palace": p_info['palace'],
                "palace_elem": p_info['palace_elem'],
                "rank": p_info['rank'],
                "shi": shi_line,
                "is_shi": line_pos == shi_line,
                **val,
            })
    
    return records


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# Line Text Valuations and the Binary Hierarchy")
    out()

    yaoci = load_yaoci()
    records = build_records(yaoci)
    
    out(f"Total records: {len(records)}")
    
    # Overall valence distribution
    val_dist = Counter(r["valence"] for r in records)
    out(f"Valence distribution: {dict(val_dist)}")
    out()
    
    # Marker frequencies
    marker_counts = {
        "吉": sum(1 for r in records if r["ji"]),
        "凶": sum(1 for r in records if r["xiong"]),
        "无咎": sum(1 for r in records if r["wu_jiu"]),
        "悔": sum(1 for r in records if r["hui"]),
        "吝": sum(1 for r in records if r["lin"]),
        "厲": sum(1 for r in records if r["li"]),
        "亨": sum(1 for r in records if r["heng"]),
    }
    out(f"Marker frequencies: {marker_counts}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 2: Valuation by line position
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 2: Valuation by Line Position")
    out()
    
    out(f"  {'Line':>4}  {'N':>3}  {'吉':>3}  {'吉%':>5}  {'凶':>3}  {'凶%':>5}  "
        f"{'无咎':>4}  {'悔':>3}  {'吝':>3}  {'厲':>3}  {'Pos':>3}  {'Neg':>3}  "
        f"{'Mix':>3}  {'Neu':>3}")
    out("  " + "-" * 85)
    
    for line in range(1, 7):
        recs = [r for r in records if r["line"] == line]
        n = len(recs)
        ji = sum(1 for r in recs if r["ji"])
        xiong = sum(1 for r in recs if r["xiong"])
        wu_jiu = sum(1 for r in recs if r["wu_jiu"])
        hui = sum(1 for r in recs if r["hui"])
        lin = sum(1 for r in recs if r["lin"])
        li = sum(1 for r in recs if r["li"])
        pos = sum(1 for r in recs if r["valence"] == "positive")
        neg = sum(1 for r in recs if r["valence"] == "negative")
        mix = sum(1 for r in recs if r["valence"] == "mixed")
        neu = sum(1 for r in recs if r["valence"] == "neutral")
        
        out(f"  {line:>4}  {n:>3}  {ji:>3}  {ji/n*100:>4.1f}%  {xiong:>3}  {xiong/n*100:>4.1f}%  "
            f"{wu_jiu:>4}  {hui:>3}  {lin:>3}  {li:>3}  {pos:>3}  {neg:>3}  "
            f"{mix:>3}  {neu:>3}")
    out()
    
    # Chi-square test: line position × 吉
    ji_table = np.array([[sum(1 for r in records if r["line"] == l and r["ji"]),
                          sum(1 for r in records if r["line"] == l and not r["ji"])]
                         for l in range(1, 7)])
    chi2, p, dof, _ = sp_stats.chi2_contingency(ji_table)
    out(f"  χ² test (吉 × line position): χ²={chi2:.3f}, p={p:.4f}, dof={dof}")
    
    # Chi-square test: line position × 凶
    xiong_table = np.array([[sum(1 for r in records if r["line"] == l and r["xiong"]),
                             sum(1 for r in records if r["line"] == l and not r["xiong"])]
                            for l in range(1, 7)])
    chi2x, px, dofx, _ = sp_stats.chi2_contingency(xiong_table)
    out(f"  χ² test (凶 × line position): χ²={chi2x:.3f}, p={px:.4f}, dof={dofx}")
    
    # Valence by line position
    valence_table = np.array([[sum(1 for r in records if r["line"] == l and r["valence"] == v)
                               for v in ["positive", "negative", "mixed", "neutral"]]
                              for l in range(1, 7)])
    chi2v, pv, dofv, _ = sp_stats.chi2_contingency(valence_table)
    out(f"  χ² test (valence × line position): χ²={chi2v:.3f}, p={pv:.4f}, dof={dofv}")
    out()
    
    # ════════════════════════════════════════════════════════════════════════
    # Task 3: Valuation by algebraic role
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 3: Valuation by Algebraic Role")
    out()
    
    ROLE_MAP = {
        1: "outer_core",   # always change elem, never change basin
        2: "outer_core",
        5: "outer_core",
        3: "interface",    # change basin
        4: "interface",
        6: "shell",        # palace invariant, intra-fiber
    }
    ROLE_NAMES = ["outer_core", "interface", "shell"]
    
    out(f"  Outer core (lines 1,2,5): always change element, never change basin")
    out(f"  Interface (lines 3,4): change basin (b₂, b₃)")
    out(f"  Shell (line 6): palace invariant (b₅), intra-fiber discriminator")
    out()
    
    out(f"  {'Role':>12}  {'N':>4}  {'吉':>3}  {'吉%':>6}  {'凶':>3}  {'凶%':>6}  "
        f"{'Pos':>3}  {'Neg':>3}  {'Mix':>3}  {'Neu':>3}")
    out("  " + "-" * 70)
    
    for role in ROLE_NAMES:
        lines_in_role = [l for l, r in ROLE_MAP.items() if r == role]
        recs = [r for r in records if r["line"] in lines_in_role]
        n = len(recs)
        ji = sum(1 for r in recs if r["ji"])
        xiong = sum(1 for r in recs if r["xiong"])
        pos = sum(1 for r in recs if r["valence"] == "positive")
        neg = sum(1 for r in recs if r["valence"] == "negative")
        mix = sum(1 for r in recs if r["valence"] == "mixed")
        neu = sum(1 for r in recs if r["valence"] == "neutral")
        out(f"  {role:>12}  {n:>4}  {ji:>3}  {ji/n*100:>5.1f}%  {xiong:>3}  {xiong/n*100:>5.1f}%  "
            f"{pos:>3}  {neg:>3}  {mix:>3}  {neu:>3}")
    out()
    
    # Chi-square test
    role_ji_table = np.array([
        [sum(1 for r in records if ROLE_MAP[r["line"]] == role and r["ji"]),
         sum(1 for r in records if ROLE_MAP[r["line"]] == role and not r["ji"])]
        for role in ROLE_NAMES
    ])
    chi2r, pr, dofr, _ = sp_stats.chi2_contingency(role_ji_table)
    out(f"  χ² test (吉 × algebraic role): χ²={chi2r:.3f}, p={pr:.4f}, dof={dofr}")
    
    role_xiong_table = np.array([
        [sum(1 for r in records if ROLE_MAP[r["line"]] == role and r["xiong"]),
         sum(1 for r in records if ROLE_MAP[r["line"]] == role and not r["xiong"])]
        for role in ROLE_NAMES
    ])
    chi2rx, prx, dofrx, _ = sp_stats.chi2_contingency(role_xiong_table)
    out(f"  χ² test (凶 × algebraic role): χ²={chi2rx:.3f}, p={prx:.4f}, dof={dofrx}")
    out()
    
    # ════════════════════════════════════════════════════════════════════════
    # Task 4: Valuation by 体/用 position
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 4: Valuation by 体/用 Position")
    out()
    
    TI_YONG = {1: "体", 2: "体", 3: "体", 4: "用", 5: "用", 6: "用"}
    
    for ty in ["体", "用"]:
        lines_in_ty = [l for l, t in TI_YONG.items() if t == ty]
        recs = [r for r in records if r["line"] in lines_in_ty]
        n = len(recs)
        ji = sum(1 for r in recs if r["ji"])
        xiong = sum(1 for r in recs if r["xiong"])
        wu_jiu = sum(1 for r in recs if r["wu_jiu"])
        pos = sum(1 for r in recs if r["valence"] == "positive")
        neg = sum(1 for r in recs if r["valence"] == "negative")
        out(f"  {ty} (lines {lines_in_ty}): "
            f"N={n}, 吉={ji}({ji/n*100:.1f}%), 凶={xiong}({xiong/n*100:.1f}%), "
            f"无咎={wu_jiu}, pos={pos}, neg={neg}")
    out()
    
    # Fisher exact for 吉
    ti_recs = [r for r in records if TI_YONG[r["line"]] == "体"]
    yong_recs = [r for r in records if TI_YONG[r["line"]] == "用"]
    ti_ji = sum(1 for r in ti_recs if r["ji"])
    yong_ji = sum(1 for r in yong_recs if r["ji"])
    table_ty = np.array([
        [ti_ji, len(ti_recs) - ti_ji],
        [yong_ji, len(yong_recs) - yong_ji],
    ])
    odds_ty, p_ty = sp_stats.fisher_exact(table_ty)
    out(f"  Fisher exact (吉: 体 vs 用): OR={odds_ty:.3f}, p={p_ty:.4f}")
    
    # 凶
    ti_xiong = sum(1 for r in ti_recs if r["xiong"])
    yong_xiong = sum(1 for r in yong_recs if r["xiong"])
    table_tyx = np.array([
        [ti_xiong, len(ti_recs) - ti_xiong],
        [yong_xiong, len(yong_recs) - yong_xiong],
    ])
    odds_tyx, p_tyx = sp_stats.fisher_exact(table_tyx)
    out(f"  Fisher exact (凶: 体 vs 用): OR={odds_tyx:.3f}, p={p_tyx:.4f}")
    out()
    
    # ════════════════════════════════════════════════════════════════════════
    # Task 5: Valuation by element relation
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 5: Valuation by Element Relation")
    out()
    
    relations = ["比和", "生体", "体生用", "克体", "体克用"]
    
    out("### Average rates by relation")
    out()
    out(f"  {'Relation':>8}  {'N':>4}  {'吉':>3}  {'吉%':>6}  {'凶':>3}  {'凶%':>6}  "
        f"{'无咎':>4}  {'悔':>3}  {'吝':>3}  {'厲':>3}")
    out("  " + "-" * 65)
    
    for rel in relations:
        recs = [r for r in records if r["surface_relation"] == rel]
        n = len(recs)
        ji = sum(1 for r in recs if r["ji"])
        xiong = sum(1 for r in recs if r["xiong"])
        wu_jiu = sum(1 for r in recs if r["wu_jiu"])
        hui = sum(1 for r in recs if r["hui"])
        lin = sum(1 for r in recs if r["lin"])
        li = sum(1 for r in recs if r["li"])
        out(f"  {rel:>8}  {n:>4}  {ji:>3}  {ji/n*100:>5.1f}%  {xiong:>3}  {xiong/n*100:>5.1f}%  "
            f"{wu_jiu:>4}  {hui:>3}  {lin:>3}  {li:>3}")
    out()
    
    # Interaction: relation × line position for 吉
    out("### Interaction: 吉 rate by relation × line position")
    out()
    out(f"  {'Relation':>8}  " + "  ".join(f"{'L'+str(l):>5}" for l in range(1, 7)) + "  {'Total':>6}")
    out("  " + "-" * 55)
    
    for rel in relations:
        rates = []
        for line in range(1, 7):
            recs = [r for r in records if r["surface_relation"] == rel and r["line"] == line]
            n = len(recs)
            ji = sum(1 for r in recs if r["ji"])
            rates.append(f"{ji/n*100:>4.0f}%" if n > 0 else "  N/A")
        total_recs = [r for r in records if r["surface_relation"] == rel]
        total_ji = sum(1 for r in total_recs if r["ji"])
        total_n = len(total_recs)
        out(f"  {rel:>8}  " + "  ".join(rates) + f"  {total_ji/total_n*100:>5.1f}%")
    out()
    
    # Interaction: relation × line position for 凶
    out("### Interaction: 凶 rate by relation × line position")
    out()
    out(f"  {'Relation':>8}  " + "  ".join(f"{'L'+str(l):>5}" for l in range(1, 7)) + "  {'Total':>6}")
    out("  " + "-" * 55)
    
    for rel in relations:
        rates = []
        for line in range(1, 7):
            recs = [r for r in records if r["surface_relation"] == rel and r["line"] == line]
            n = len(recs)
            xiong = sum(1 for r in recs if r["xiong"])
            rates.append(f"{xiong/n*100:>4.0f}%" if n > 0 else "  N/A")
        total_recs = [r for r in records if r["surface_relation"] == rel]
        total_xiong = sum(1 for r in total_recs if r["xiong"])
        total_n = len(total_recs)
        out(f"  {rel:>8}  " + "  ".join(rates) + f"  {total_xiong/total_n*100:>5.1f}%")
    out()
    
    # Test interaction term
    # Chi-square on relation × line × 吉 interaction
    # Full model: 5 relations × 6 lines = 30 cells
    full_table = np.zeros((30, 2), dtype=int)
    for ri, rel in enumerate(relations):
        for li in range(6):
            line = li + 1
            recs = [r for r in records if r["surface_relation"] == rel and r["line"] == line]
            ji_count = sum(1 for r in recs if r["ji"])
            full_table[ri * 6 + li] = [ji_count, len(recs) - ji_count]
    
    # Remove rows with zero total (shouldn't happen but safety)
    mask = full_table.sum(axis=1) > 0
    if mask.all():
        chi2_full, p_full, dof_full, _ = sp_stats.chi2_contingency(full_table)
        out(f"  χ² test (吉 × relation × line, full 30-cell): χ²={chi2_full:.3f}, p={p_full:.4f}, dof={dof_full}")
    out()
    
    # ════════════════════════════════════════════════════════════════════════
    # Task 6: The 世 line valuation
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 6: 世 Line Valuation")
    out()
    
    shi_recs = [r for r in records if r["is_shi"]]
    non_shi_recs = [r for r in records if not r["is_shi"]]
    
    shi_ji = sum(1 for r in shi_recs if r["ji"])
    non_shi_ji = sum(1 for r in non_shi_recs if r["ji"])
    
    out(f"  世 lines: {len(shi_recs)} records (1 per hexagram)")
    out(f"    吉: {shi_ji} ({shi_ji/len(shi_recs)*100:.1f}%)")
    out(f"    凶: {sum(1 for r in shi_recs if r['xiong'])} "
        f"({sum(1 for r in shi_recs if r['xiong'])/len(shi_recs)*100:.1f}%)")
    out(f"    无咎: {sum(1 for r in shi_recs if r['wu_jiu'])} "
        f"({sum(1 for r in shi_recs if r['wu_jiu'])/len(shi_recs)*100:.1f}%)")
    out()
    out(f"  Non-世 lines: {len(non_shi_recs)} records")
    out(f"    吉: {non_shi_ji} ({non_shi_ji/len(non_shi_recs)*100:.1f}%)")
    out(f"    凶: {sum(1 for r in non_shi_recs if r['xiong'])} "
        f"({sum(1 for r in non_shi_recs if r['xiong'])/len(non_shi_recs)*100:.1f}%)")
    out(f"    无咎: {sum(1 for r in non_shi_recs if r['wu_jiu'])} "
        f"({sum(1 for r in non_shi_recs if r['wu_jiu'])/len(non_shi_recs)*100:.1f}%)")
    out()
    
    # Fisher exact: 世 vs non-世 for 吉
    table_shi_ji = np.array([
        [shi_ji, len(shi_recs) - shi_ji],
        [non_shi_ji, len(non_shi_recs) - non_shi_ji],
    ])
    odds_shi, p_shi = sp_stats.fisher_exact(table_shi_ji)
    out(f"  Fisher exact (吉: 世 vs non-世): OR={odds_shi:.3f}, p={p_shi:.4f}")
    
    # 凶
    shi_xiong = sum(1 for r in shi_recs if r["xiong"])
    non_shi_xiong = sum(1 for r in non_shi_recs if r["xiong"])
    table_shi_xiong = np.array([
        [shi_xiong, len(shi_recs) - shi_xiong],
        [non_shi_xiong, len(non_shi_recs) - non_shi_xiong],
    ])
    odds_shi_x, p_shi_x = sp_stats.fisher_exact(table_shi_xiong)
    out(f"  Fisher exact (凶: 世 vs non-世): OR={odds_shi_x:.3f}, p={p_shi_x:.4f}")
    out()
    
    # Break down by 世 line position
    out("### 世 line valuation by position")
    out()
    out(f"  {'世 line':>7}  {'N':>3}  {'吉':>3}  {'吉%':>6}  {'凶':>3}  {'凶%':>6}  {'无咎':>4}")
    out("  " + "-" * 45)
    
    for shi_pos in sorted(set(SHI_BY_RANK)):
        recs_at_pos = [r for r in shi_recs if r["shi"] == shi_pos]
        n = len(recs_at_pos)
        if n == 0:
            continue
        ji = sum(1 for r in recs_at_pos if r["ji"])
        xiong = sum(1 for r in recs_at_pos if r["xiong"])
        wu_jiu = sum(1 for r in recs_at_pos if r["wu_jiu"])
        out(f"  {shi_pos:>7}  {n:>3}  {ji:>3}  {ji/n*100:>5.1f}%  "
            f"{xiong:>3}  {xiong/n*100:>5.1f}%  {wu_jiu:>4}")
    out()
    
    # Control: compare 世 at line 5 vs non-世 at line 5
    out("### 世 vs non-世 at same line position")
    out()
    out(f"  {'Line':>4}  {'世_N':>4}  {'世_吉%':>7}  {'Non世_N':>6}  {'Non世_吉%':>9}  {'p(Fisher)':>10}")
    out("  " + "-" * 55)
    
    for line in range(1, 7):
        shi_at_line = [r for r in records if r["line"] == line and r["is_shi"]]
        non_shi_at_line = [r for r in records if r["line"] == line and not r["is_shi"]]
        n_shi = len(shi_at_line)
        n_non = len(non_shi_at_line)
        if n_shi == 0 or n_non == 0:
            out(f"  {line:>4}  {n_shi:>4}  {'N/A':>7}  {n_non:>6}  {'N/A':>9}  {'N/A':>10}")
            continue
        ji_shi = sum(1 for r in shi_at_line if r["ji"])
        ji_non = sum(1 for r in non_shi_at_line if r["ji"])
        tab = np.array([[ji_shi, n_shi - ji_shi], [ji_non, n_non - ji_non]])
        _, p_line = sp_stats.fisher_exact(tab)
        out(f"  {line:>4}  {n_shi:>4}  {ji_shi/n_shi*100:>6.1f}%  {n_non:>6}  "
            f"{ji_non/n_non*100:>8.1f}%  {p_line:>10.4f}")
    out()
    
    # ════════════════════════════════════════════════════════════════════════
    # Additional: Line 5 as the "ruler" position
    # ════════════════════════════════════════════════════════════════════════
    out("## Additional: Line 5 as Ruler Position")
    out()
    out("Traditionally, line 5 is the 'ruler' (君位) — the central yang position.")
    out()
    
    line5 = [r for r in records if r["line"] == 5]
    other = [r for r in records if r["line"] != 5]
    l5_ji = sum(1 for r in line5 if r["ji"])
    ot_ji = sum(1 for r in other if r["ji"])
    tab5 = np.array([[l5_ji, len(line5) - l5_ji], [ot_ji, len(other) - ot_ji]])
    odds5, p5 = sp_stats.fisher_exact(tab5)
    out(f"  Line 5: 吉={l5_ji}/{len(line5)} ({l5_ji/len(line5)*100:.1f}%)")
    out(f"  Others: 吉={ot_ji}/{len(other)} ({ot_ji/len(other)*100:.1f}%)")
    out(f"  Fisher exact: OR={odds5:.3f}, p={p5:.4f}")
    out()
    
    l5_xiong = sum(1 for r in line5 if r["xiong"])
    ot_xiong = sum(1 for r in other if r["xiong"])
    out(f"  Line 5: 凶={l5_xiong}/{len(line5)} ({l5_xiong/len(line5)*100:.1f}%)")
    out(f"  Others: 凶={ot_xiong}/{len(other)} ({ot_xiong/len(other)*100:.1f}%)")
    tab5x = np.array([[l5_xiong, len(line5) - l5_xiong], [ot_xiong, len(other) - ot_xiong]])
    odds5x, p5x = sp_stats.fisher_exact(tab5x)
    out(f"  Fisher exact: OR={odds5x:.3f}, p={p5x:.4f}")
    out()
    
    # Line 3 and line 6: the two "transition" positions
    out("## Additional: Lines 3 and 6 — Transition Positions")
    out()
    out("Lines 3 (top of lower trigram) and 6 (top of upper trigram) are")
    out("traditionally considered transition/ending positions.")
    out()
    
    for tl in [3, 6]:
        tl_recs = [r for r in records if r["line"] == tl]
        ot_recs = [r for r in records if r["line"] != tl]
        tl_ji = sum(1 for r in tl_recs if r["ji"])
        tl_xiong = sum(1 for r in tl_recs if r["xiong"])
        ot_ji2 = sum(1 for r in ot_recs if r["ji"])
        ot_xiong2 = sum(1 for r in ot_recs if r["xiong"])
        
        tab_j = np.array([[tl_ji, len(tl_recs) - tl_ji], [ot_ji2, len(ot_recs) - ot_ji2]])
        tab_x = np.array([[tl_xiong, len(tl_recs) - tl_xiong], [ot_xiong2, len(ot_recs) - ot_xiong2]])
        _, pj_line = sp_stats.fisher_exact(tab_j)
        _, px_line = sp_stats.fisher_exact(tab_x)
        
        out(f"  Line {tl}: 吉={tl_ji}({tl_ji/len(tl_recs)*100:.1f}%), "
            f"凶={tl_xiong}({tl_xiong/len(tl_recs)*100:.1f}%)")
        out(f"    vs others: 吉 p={pj_line:.4f}, 凶 p={px_line:.4f}")
    out()
    
    # ════════════════════════════════════════════════════════════════════════
    # Summary
    # ════════════════════════════════════════════════════════════════════════
    out("## Summary")
    out()
    
    out("### Line position hierarchy in text")
    out(f"  吉 × line position: χ²={chi2:.3f}, p={p:.4f}")
    out(f"  凶 × line position: χ²={chi2x:.3f}, p={px:.4f}")
    out(f"  → {'Significant' if p < 0.05 else 'Not significant'} variation in 吉 across lines")
    out(f"  → {'Significant' if px < 0.05 else 'Not significant'} variation in 凶 across lines")
    out()
    
    out("### Algebraic role")
    out(f"  吉 × role: χ²={chi2r:.3f}, p={pr:.4f}")
    out(f"  → {'Roles differ' if pr < 0.05 else 'No difference'} in 吉 rate")
    out()
    
    out("### 体/用")
    out(f"  吉: 体 vs 用: OR={odds_ty:.3f}, p={p_ty:.4f}")
    out(f"  凶: 体 vs 用: OR={odds_tyx:.3f}, p={p_tyx:.4f}")
    out()
    
    out("### 世 line")
    out(f"  吉: 世 vs non-世: OR={odds_shi:.3f}, p={p_shi:.4f}")
    out(f"  凶: 世 vs non-世: OR={odds_shi_x:.3f}, p={p_shi_x:.4f}")
    out()
    
    # Write
    results_path = OUT_DIR / "09_line_valuations_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
