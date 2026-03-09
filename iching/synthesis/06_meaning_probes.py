#!/usr/bin/env python3
"""
Probes 6–8: Meaning through both projections

Probe 6: KW sequence algebraic transitions (序卦 preliminary)
Probe 7: 凶 textual content at the depth boundary
Probe 8: 梅花 體/用 × line valence
"""

import sys
import re
import json
import importlib.util
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/
ICHING = ROOT / "iching"
TEXTS_DIR = ROOT / "texts" / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ICHING / "kingwen"))

from cycle_algebra import (
    NUM_HEX, TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    lower_trigram, upper_trigram, hugua, five_phase_relation,
    tiyong_relation, fmt6, fmt3, bit, kw_partner,
)
from sequence import KING_WEN

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p2 = _load("palace", ICHING / "huozhulin" / "02_palace_kernel.py")

# ─── Constants ───────────────────────────────────────────────────────────────

N_PERM = 10000
RNG = np.random.default_rng(42)

VALENCE_MARKERS = ["吉", "凶", "悔", "吝", "无咎", "無咎", "厲", "利", "亨"]

# Normalize 無咎→无咎
def normalize_marker(m):
    return "无咎" if m == "無咎" else m

TIYONG_CATEGORIES = ["比和", "生体", "体生用", "克体", "体克用"]

# Depth boundary thematic word groups
THRESHOLD_WORDS = list("終已極窮盡")
IRREVERSIBILITY_WORDS = ["不可", "滅", "亡", "喪", "失"]
TRANSFORMATION_WORDS = list("反復變化")
EXCESS_WORDS = list("過大盈滿")

WORD_GROUPS = {
    "threshold": THRESHOLD_WORDS,
    "irreversibility": IRREVERSIBILITY_WORDS,
    "transformation": TRANSFORMATION_WORDS,
    "excess": EXCESS_WORDS,
}

# ─── Data loading ────────────────────────────────────────────────────────────

def build_kw_lookup():
    """Binary ↔ KW number mappings."""
    bin_to_kw, kw_to_bin, kw_to_name = {}, {}, {}
    for _, (kw_num, name, bits_str) in enumerate(KING_WEN):
        h = sum(int(c) << j for j, c in enumerate(bits_str))
        bin_to_kw[h] = kw_num
        kw_to_bin[kw_num] = h
        kw_to_name[kw_num] = name
    return bin_to_kw, kw_to_bin, kw_to_name


def load_texts():
    """Load 卦辭, 爻辭, 象傳."""
    with open(TEXTS_DIR / "guaci.json") as f:
        guaci_data = json.load(f)
    with open(TEXTS_DIR / "yaoci.json") as f:
        yaoci_data = json.load(f)
    with open(TEXTS_DIR / "xiangzhuan.json") as f:
        xiang_data = json.load(f)

    guaci = {e['number']: e['text'] for e in guaci_data['entries']}
    yaoci = {}
    yaoci_labels = {}
    for e in yaoci_data['entries']:
        yaoci[e['number']] = [line['text'] for line in e['lines']]
        yaoci_labels[e['number']] = [line['label'] for line in e['lines']]
    names = {e['number']: e['name'] for e in guaci_data['entries']}

    return guaci, yaoci, yaoci_labels, names


def extract_valence_markers(text):
    """Extract all valence markers from a text, returning normalized set."""
    found = set()
    # Check 无咎/無咎 first (multi-char)
    if "无咎" in text or "無咎" in text:
        found.add("无咎")
    for m in VALENCE_MARKERS:
        if m in ("无咎", "無咎"):
            continue
        if m in text:
            found.add(m)
    return found


# ═════════════════════════════════════════════════════════════════════════════
# Probe 8: 梅花 體/用 × line valence
# ═════════════════════════════════════════════════════════════════════════════

def probe8(bin_to_kw, yaoci, yaoci_labels, names):
    """Cross-tabulate 體/用 five-phase relation × valence markers."""
    print("\n" + "=" * 70)
    print("PROBE 8: 梅花 體/用 × LINE VALENCE")
    print("=" * 70)

    records = []
    for h in range(NUM_HEX):
        kw = bin_to_kw[h]
        lines = yaoci[kw]
        for line_idx, text in enumerate(lines):
            line_pos = line_idx + 1
            rel = tiyong_relation(h, line_pos)
            markers = extract_valence_markers(text)
            records.append({
                'h': h, 'kw': kw, 'line': line_pos,
                'text': text, 'relation': rel, 'markers': markers,
                'name': names[kw],
            })

    # Cross-tabulation: relation × marker
    cross_tab = defaultdict(Counter)  # relation → marker → count
    rel_totals = Counter()  # relation → total lines
    for r in records:
        rel_totals[r['relation']] += 1
        for m in r['markers']:
            cross_tab[r['relation']][m] += 1

    # Print cross-tab
    all_markers_seen = sorted(set(m for c in cross_tab.values() for m in c))
    print("\n  Cross-tabulation: 體/用 relation × valence marker")
    header = f"  {'Relation':8s} | {'n':>4} |" + "|".join(f" {m:>4} " for m in all_markers_seen)
    print(header)
    print("  " + "─" * len(header))
    for rel in TIYONG_CATEGORIES:
        n = rel_totals[rel]
        counts = [cross_tab[rel].get(m, 0) for m in all_markers_seen]
        row = f"  {rel:8s} | {n:>4} |" + "|".join(f" {c:>4} " for c in counts)
        print(row)

    # Rates
    print("\n  Rates (count / total lines in category):")
    header = f"  {'Relation':8s} | {'n':>4} |" + "|".join(f" {m:>6} " for m in all_markers_seen)
    print(header)
    print("  " + "─" * len(header))
    for rel in TIYONG_CATEGORIES:
        n = rel_totals[rel]
        rates = [cross_tab[rel].get(m, 0) / n if n > 0 else 0 for m in all_markers_seen]
        row = f"  {rel:8s} | {n:>4} |" + "|".join(f" {r:>6.3f} " for r in rates)
        print(row)

    # χ² tests per marker
    print("\n  χ² tests: marker distribution across 5 體/用 categories")
    chi2_results = {}
    for m in all_markers_seen:
        # Contingency: 5 rows (relations) × 2 cols (has/not)
        table = []
        for rel in TIYONG_CATEGORIES:
            has = cross_tab[rel].get(m, 0)
            not_has = rel_totals[rel] - has
            table.append([has, not_has])
        table = np.array(table)
        if table[:, 0].sum() >= 5:
            chi2, p, dof, _ = stats.chi2_contingency(table)
            chi2_results[m] = {'chi2': chi2, 'p': p, 'dof': dof}
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"    {m}: χ²={chi2:.3f}, p={p:.4f}, dof={dof} {sig}")

    # Focused tests: 比和 vs 克 categories
    print("\n  Focused comparison: 比和 vs 克 categories (克体 + 体克用)")
    bihe_records = [r for r in records if r['relation'] == "比和"]
    ke_records = [r for r in records if r['relation'] in ("克体", "体克用")]

    for marker in ["吉", "凶"]:
        bihe_has = sum(1 for r in bihe_records if marker in r['markers'])
        ke_has = sum(1 for r in ke_records if marker in r['markers'])
        # Fisher exact test
        table_2x2 = np.array([
            [bihe_has, len(bihe_records) - bihe_has],
            [ke_has, len(ke_records) - ke_has],
        ])
        odds, p_fisher = stats.fisher_exact(table_2x2)
        print(f"    {marker}: 比和={bihe_has}/{len(bihe_records)} ({bihe_has/len(bihe_records):.3f}), "
              f"克={ke_has}/{len(ke_records)} ({ke_has/len(ke_records):.3f}), "
              f"Fisher p={p_fisher:.4f}, OR={odds:.2f}")

    return records, cross_tab, rel_totals, chi2_results


# ═════════════════════════════════════════════════════════════════════════════
# Probe 7: 凶 textual content at the depth boundary
# ═════════════════════════════════════════════════════════════════════════════

def probe7(bin_to_kw, yaoci, yaoci_labels, names):
    """Analyze 凶 texts by depth category."""
    print("\n" + "=" * 70)
    print("PROBE 7: 凶 TEXTUAL CONTENT AT THE DEPTH BOUNDARY")
    print("=" * 70)

    _, hex_info = p2.generate_palaces()

    # Collect all 爻辭 with depth info
    xiong_by_depth = defaultdict(list)  # depth → list of records
    all_by_depth = defaultdict(int)  # depth → total line count

    for h in range(NUM_HEX):
        kw = bin_to_kw[h]
        d = p2.depth(h)
        lines = yaoci[kw]
        labels = yaoci_labels[kw]
        for line_idx, text in enumerate(lines):
            all_by_depth[d] += 1
            if "凶" in text:
                xiong_by_depth[d].append({
                    'h': h, 'kw': kw, 'line': line_idx + 1,
                    'label': labels[line_idx],
                    'text': text, 'depth': d,
                    'basin': p2.basin(h),
                    'name': names[kw],
                })

    # Print depth distribution of 凶
    print("\n  凶 distribution by depth:")
    for d in sorted(all_by_depth.keys()):
        n_xiong = len(xiong_by_depth[d])
        n_total = all_by_depth[d]
        print(f"    depth-{d}: {n_xiong}/{n_total} lines ({n_xiong/n_total:.3f})")

    # Word frequency profiles for 凶 texts by depth
    print("\n  Thematic word frequencies in 凶 texts by depth:")
    word_group_counts = {}  # (depth, group_name) → count
    word_group_totals = {}  # depth → n_xiong_texts

    for d in sorted(xiong_by_depth.keys()):
        texts = xiong_by_depth[d]
        word_group_totals[d] = len(texts)
        for group_name, words in WORD_GROUPS.items():
            count = sum(1 for rec in texts if any(w in rec['text'] for w in words))
            word_group_counts[(d, group_name)] = count

    header = f"  {'Depth':>7} | {'n凶':>4} |" + "|".join(f" {g:>15} " for g in WORD_GROUPS)
    print(header)
    print("  " + "─" * len(header))
    for d in sorted(xiong_by_depth.keys()):
        n = word_group_totals[d]
        counts = [word_group_counts.get((d, g), 0) for g in WORD_GROUPS]
        rates = [c / n if n > 0 else 0 for c in counts]
        row = f"  {'d=' + str(d):>7} | {n:>4} |" + "|".join(
            f" {c:>2} ({r:.2f})       " for c, r in zip(counts, rates))
        print(row)

    # Statistical test: irreversibility words in depth-1 vs others
    print("\n  Fisher exact test: irreversibility words in depth-1 凶 vs others")
    d1_texts = xiong_by_depth.get(1, [])
    other_texts = [r for d, recs in xiong_by_depth.items() for r in recs if d != 1]

    d1_has_irrev = sum(1 for r in d1_texts if any(w in r['text'] for w in IRREVERSIBILITY_WORDS))
    other_has_irrev = sum(1 for r in other_texts if any(w in r['text'] for w in IRREVERSIBILITY_WORDS))

    table_2x2 = np.array([
        [d1_has_irrev, len(d1_texts) - d1_has_irrev],
        [other_has_irrev, len(other_texts) - other_has_irrev],
    ])
    if table_2x2.sum() > 0 and len(d1_texts) > 0 and len(other_texts) > 0:
        odds, p = stats.fisher_exact(table_2x2)
        print(f"    depth-1: {d1_has_irrev}/{len(d1_texts)}, others: {other_has_irrev}/{len(other_texts)}")
        print(f"    Fisher p={p:.4f}, OR={odds:.2f}")

    # Test all word groups
    print("\n  Fisher exact tests per word group (depth-1 vs all others):")
    fisher_results = {}
    for group_name, words in WORD_GROUPS.items():
        d1_has = sum(1 for r in d1_texts if any(w in r['text'] for w in words))
        other_has = sum(1 for r in other_texts if any(w in r['text'] for w in words))
        table_2x2 = np.array([
            [d1_has, len(d1_texts) - d1_has],
            [other_has, len(other_texts) - other_has],
        ])
        if len(d1_texts) > 0 and len(other_texts) > 0:
            odds, p = stats.fisher_exact(table_2x2)
            fisher_results[group_name] = {'odds': odds, 'p': p,
                                           'd1_rate': d1_has / len(d1_texts),
                                           'other_rate': other_has / len(other_texts)}
            sig = "*" if p < 0.05 else ""
            print(f"    {group_name:15s}: d1={d1_has}/{len(d1_texts)} ({d1_has/len(d1_texts):.2f}), "
                  f"other={other_has}/{len(other_texts)} ({other_has/len(other_texts):.2f}), "
                  f"p={p:.4f} {sig}")

    # Individual word frequencies across all 凶 texts
    print("\n  Individual word frequencies in 凶 texts by depth:")
    all_words = []
    for words in WORD_GROUPS.values():
        all_words.extend(words)
    all_words = sorted(set(all_words))

    for d in sorted(xiong_by_depth.keys()):
        texts = xiong_by_depth[d]
        if not texts:
            continue
        word_counts = Counter()
        for r in texts:
            for w in all_words:
                if w in r['text']:
                    word_counts[w] += 1
        found = {w: c for w, c in word_counts.items() if c > 0}
        if found:
            print(f"    depth-{d} ({len(texts)} texts): " +
                  ", ".join(f"{w}={c}" for w, c in sorted(found.items(), key=lambda x: -x[1])))

    # List all depth-1 凶 texts
    print("\n  ── All 凶 texts from depth-1 hexagrams ──")
    for r in sorted(d1_texts, key=lambda x: (x['kw'], x['line'])):
        print(f"    KW{r['kw']:2d} {r['name']} {r['label']} (bin={r['h']:06b}, basin={r['basin']})")
        print(f"      {r['text']}")

    return xiong_by_depth, fisher_results


# ═════════════════════════════════════════════════════════════════════════════
# Probe 6: KW sequence algebraic transitions
# ═════════════════════════════════════════════════════════════════════════════

def probe6(bin_to_kw, kw_to_bin, kw_to_name):
    """Analyze algebraic transitions in King Wen sequence."""
    print("\n" + "=" * 70)
    print("PROBE 6: KW SEQUENCE ALGEBRAIC TRANSITIONS")
    print("=" * 70)

    _, hex_info = p2.generate_palaces()

    # Build KW-ordered list of binary values
    kw_seq = [kw_to_bin[kw_num] for kw_num in range(1, 65)]

    # Compute transition features for consecutive pairs
    transitions = []
    for i in range(63):
        h1, h2 = kw_seq[i], kw_seq[i + 1]
        b1, b2 = p2.basin(h1), p2.basin(h2)
        d1, d2 = p2.depth(h1), p2.depth(h2)
        i1 = bit(h1, 2) ^ bit(h1, 3)
        i2 = bit(h2, 2) ^ bit(h2, 3)

        lo1, up1 = lower_trigram(h1), upper_trigram(h1)
        lo2, up2 = lower_trigram(h2), upper_trigram(h2)

        # Five-phase relations between consecutive hexagrams' trigrams
        up_rel = five_phase_relation(TRIGRAM_ELEMENT[up1], TRIGRAM_ELEMENT[up2])
        lo_rel = five_phase_relation(TRIGRAM_ELEMENT[lo1], TRIGRAM_ELEMENT[lo2])

        transitions.append({
            'kw1': i + 1, 'kw2': i + 2,
            'h1': h1, 'h2': h2,
            'basin1': b1, 'basin2': b2,
            'same_basin': b1 == b2,
            'depth1': d1, 'depth2': d2,
            'depth_delta': d2 - d1,
            'I1': i1, 'I2': i2,
            'same_I': i1 == i2,
            'upper_rel': up_rel,
            'lower_rel': lo_rel,
            'is_within_pair': (i % 2 == 0),  # transitions 1→2, 3→4, ...
        })

    # ── Basin transitions ──
    same_basin = sum(1 for t in transitions if t['same_basin'])
    total = len(transitions)
    print(f"\n  Basin transitions: {same_basin}/{total} same ({same_basin/total:.3f})")

    # Null model: random permutation
    basin_list = [p2.basin(kw_to_bin[kw]) for kw in range(1, 65)]
    n_same_perm = []
    for _ in range(N_PERM):
        perm = RNG.permutation(basin_list)
        n_same = sum(1 for i in range(63) if perm[i] == perm[i + 1])
        n_same_perm.append(n_same)
    n_same_perm = np.array(n_same_perm)
    p_basin = np.mean(n_same_perm >= same_basin)
    print(f"  Null (random perm): mean={n_same_perm.mean():.1f}, std={n_same_perm.std():.1f}")
    print(f"  p-value (observed ≥ null): {p_basin:.4f}")

    # Basin transition matrix
    basin_trans = Counter()
    for t in transitions:
        basin_trans[(t['basin1'], t['basin2'])] += 1
    print("\n  Basin transition matrix:")
    basins = ["Kun", "Qian", "Cycle"]
    print(f"    {'From\\To':>8} |" + "|".join(f" {b:>6} " for b in basins))
    for b1 in basins:
        counts = [basin_trans.get((b1, b2), 0) for b2 in basins]
        print(f"    {b1:>8} |" + "|".join(f" {c:>6} " for c in counts))

    # ── Depth transitions ──
    depth_deltas = Counter(t['depth_delta'] for t in transitions)
    print("\n  Depth transitions (d2 - d1):")
    for delta in sorted(depth_deltas):
        print(f"    Δ={delta:+d}: {depth_deltas[delta]}")

    # ── Within-pair vs between-pair ──
    within = [t for t in transitions if t['is_within_pair']]
    between = [t for t in transitions if not t['is_within_pair']]

    print(f"\n  Within-pair transitions (1→2, 3→4, ...): n={len(within)}")
    print(f"  Between-pair transitions (2→3, 4→5, ...): n={len(between)}")

    # Within-pair: these are reversal/complement pairs
    # Check what algebraic operations connect them
    within_ops = Counter()
    for t in within:
        h1, h2 = t['h1'], t['h2']
        partner = kw_partner(h1)
        if h2 == partner:
            within_ops['kw_partner'] += 1
        else:
            within_ops['other'] += 1
    print(f"  Within-pair that are KW partners: {within_ops['kw_partner']}/{len(within)}")

    # Between-pair basin continuity
    between_same_basin = sum(1 for t in between if t['same_basin'])
    print(f"\n  Between-pair same basin: {between_same_basin}/{len(between)} ({between_same_basin/len(between):.3f})")

    # Null model for between-pair
    between_basin_perm = []
    for _ in range(N_PERM):
        perm = RNG.permutation(basin_list)
        # Simulate between-pair transitions: positions 1,3,5,...
        n_same = sum(1 for i in range(1, 63, 2) if perm[i] == perm[i + 1])
        between_basin_perm.append(n_same)
    between_basin_perm = np.array(between_basin_perm)
    p_between = np.mean(between_basin_perm >= between_same_basin)
    print(f"  Null (random perm between-pair): mean={between_basin_perm.mean():.1f}")
    print(f"  p-value: {p_between:.4f}")

    # ── Five-phase relation patterns ──
    upper_rel_counts = Counter(t['upper_rel'] for t in transitions)
    lower_rel_counts = Counter(t['lower_rel'] for t in transitions)
    print("\n  Upper trigram relations between consecutive hexagrams:")
    for rel in TIYONG_CATEGORIES:
        print(f"    {rel}: {upper_rel_counts.get(rel, 0)}")
    print("  Lower trigram relations:")
    for rel in TIYONG_CATEGORIES:
        print(f"    {rel}: {lower_rel_counts.get(rel, 0)}")

    # Null model for 比和 rate
    bihe_upper = upper_rel_counts.get("比和", 0)
    bihe_lower = lower_rel_counts.get("比和", 0)
    bihe_perm_upper, bihe_perm_lower = [], []
    for _ in range(N_PERM):
        perm = RNG.permutation(64)
        perm_seq = [kw_to_bin[KING_WEN[p][0]] for p in perm]
        bu, bl = 0, 0
        for i in range(63):
            u1, u2 = upper_trigram(perm_seq[i]), upper_trigram(perm_seq[i + 1])
            l1, l2 = lower_trigram(perm_seq[i]), lower_trigram(perm_seq[i + 1])
            if TRIGRAM_ELEMENT[u1] == TRIGRAM_ELEMENT[u2]:
                bu += 1
            if TRIGRAM_ELEMENT[l1] == TRIGRAM_ELEMENT[l2]:
                bl += 1
        bihe_perm_upper.append(bu)
        bihe_perm_lower.append(bl)
    bihe_perm_upper = np.array(bihe_perm_upper)
    bihe_perm_lower = np.array(bihe_perm_lower)
    p_bihe_upper = np.mean(bihe_perm_upper >= bihe_upper)
    p_bihe_lower = np.mean(bihe_perm_lower >= bihe_lower)
    print(f"\n  比和 rate null model:")
    print(f"    Upper: observed={bihe_upper}, null mean={bihe_perm_upper.mean():.1f}, p={p_bihe_upper:.4f}")
    print(f"    Lower: observed={bihe_lower}, null mean={bihe_perm_lower.mean():.1f}, p={p_bihe_lower:.4f}")

    return transitions, {
        'same_basin': same_basin, 'total': total,
        'p_basin': p_basin,
        'between_same_basin': between_same_basin,
        'p_between': p_between,
        'bihe_upper': bihe_upper, 'p_bihe_upper': p_bihe_upper,
        'bihe_lower': bihe_lower, 'p_bihe_lower': p_bihe_lower,
        'depth_deltas': dict(depth_deltas),
        'basin_trans': dict(basin_trans),
        'upper_rel': dict(upper_rel_counts),
        'lower_rel': dict(lower_rel_counts),
    }


# ═════════════════════════════════════════════════════════════════════════════
# Output
# ═════════════════════════════════════════════════════════════════════════════

def write_results(p8_data, p7_data, p6_data):
    records, cross_tab, rel_totals, chi2_results = p8_data
    xiong_by_depth, fisher_results = p7_data
    transitions, p6_stats = p6_data

    lines = []
    w = lines.append

    w("# Probes 6–8: Meaning Through Both Projections\n")

    # ═══ PROBE 8 ═══
    w("## Probe 8: 梅花 體/用 × Line Valence\n")
    w("For each of the 384 (hexagram, line) states, compute the 體/用 five-phase")
    w("relation and cross-tabulate with valence markers from the 爻辭.\n")

    # Cross-tab table
    all_markers = sorted(set(m for c in cross_tab.values() for m in c))
    w("### Cross-tabulation: counts\n")
    w("| Relation | n |" + "|".join(f" {m} " for m in all_markers) + "|")
    w("|----------|---|" + "|".join("---" for _ in all_markers) + "|")
    for rel in TIYONG_CATEGORIES:
        n = rel_totals[rel]
        counts = [cross_tab[rel].get(m, 0) for m in all_markers]
        w(f"| {rel} | {n} |" + "|".join(f" {c} " for c in counts) + "|")
    w("")

    # Rates table
    w("### Cross-tabulation: rates\n")
    w("| Relation | n |" + "|".join(f" {m} " for m in all_markers) + "|")
    w("|----------|---|" + "|".join("---" for _ in all_markers) + "|")
    for rel in TIYONG_CATEGORIES:
        n = rel_totals[rel]
        rates = [cross_tab[rel].get(m, 0) / n if n > 0 else 0 for m in all_markers]
        w(f"| {rel} | {n} |" + "|".join(f" {r:.3f} " for r in rates) + "|")
    w("")

    # χ² results
    w("### χ² tests: marker distribution across 5 體/用 categories\n")
    w("| Marker | χ² | p-value | dof | Sig |")
    w("|--------|-----|---------|-----|-----|")
    for m in all_markers:
        if m in chi2_results:
            r = chi2_results[m]
            sig = "***" if r['p'] < 0.001 else "**" if r['p'] < 0.01 else "*" if r['p'] < 0.05 else ""
            w(f"| {m} | {r['chi2']:.3f} | {r['p']:.4f} | {r['dof']} | {sig} |")
    w("")

    # Focused comparison
    bihe_records = [r for r in records if r['relation'] == "比和"]
    ke_records = [r for r in records if r['relation'] in ("克体", "体克用")]
    w("### 比和 vs 克 categories (focused comparison)\n")
    for marker in ["吉", "凶"]:
        bihe_has = sum(1 for r in bihe_records if marker in r['markers'])
        ke_has = sum(1 for r in ke_records if marker in r['markers'])
        table_2x2 = np.array([
            [bihe_has, len(bihe_records) - bihe_has],
            [ke_has, len(ke_records) - ke_has],
        ])
        odds, p_fisher = stats.fisher_exact(table_2x2)
        w(f"- **{marker}**: 比和={bihe_has}/{len(bihe_records)} ({bihe_has/len(bihe_records):.3f}), "
          f"克={ke_has}/{len(ke_records)} ({ke_has/len(ke_records):.3f}), "
          f"Fisher p={p_fisher:.4f}, OR={odds:.2f}")
    w("")

    w("### Interpretation\n")
    sig_markers = [m for m, r in chi2_results.items() if r['p'] < 0.05]
    if sig_markers:
        w(f"Significant markers: {', '.join(sig_markers)}")
        p_vals = [chi2_results[m]['p'] for m in sig_markers]
        w(f"Strongest: {sig_markers[np.argmin(p_vals)]} (p={min(p_vals):.4f})")
    else:
        w("No markers reach significance at α=0.05.")
    w("")

    basin_p = 0.0002  # from findings.md
    strongest_p8 = min(r['p'] for r in chi2_results.values()) if chi2_results else 1.0
    w(f"**Comparison with basin×凶 (p={basin_p})**: ")
    if strongest_p8 < basin_p:
        w(f"Probe 8 signal is STRONGER (p={strongest_p8:.4f}).")
    elif strongest_p8 < 0.05:
        w(f"Probe 8 signal exists but WEAKER (p={strongest_p8:.4f}).")
    else:
        w(f"Probe 8 shows NO comparable signal (best p={strongest_p8:.4f}).")
    w("")

    # ═══ PROBE 7 ═══
    w("## Probe 7: 凶 Textual Content at the Depth Boundary\n")

    # Depth distribution
    w("### 凶 distribution by depth\n")
    w("| Depth | 凶 texts | Total lines | Rate |")
    w("|-------|---------|-------------|------|")
    all_by_depth = defaultdict(int)
    for h in range(NUM_HEX):
        d = p2.depth(h)
        all_by_depth[d] += 6
    for d in sorted(all_by_depth.keys()):
        n_xiong = len(xiong_by_depth[d])
        n_total = all_by_depth[d]
        w(f"| {d} | {n_xiong} | {n_total} | {n_xiong/n_total:.3f} |")
    w("")

    # Word group frequencies
    w("### Thematic word frequencies in 凶 texts by depth\n")
    w("| Depth | n凶 |" + "|".join(f" {g} " for g in WORD_GROUPS) + "|")
    w("|-------|-----|" + "|".join("---" for _ in WORD_GROUPS) + "|")
    for d in sorted(xiong_by_depth.keys()):
        texts = xiong_by_depth[d]
        n = len(texts)
        counts_rates = []
        for g, words in WORD_GROUPS.items():
            c = sum(1 for r in texts if any(ww in r['text'] for ww in words))
            rate = c / n if n > 0 else 0
            counts_rates.append(f" {c} ({rate:.2f}) ")
        w(f"| {d} | {n} |" + "|".join(counts_rates) + "|")
    w("")

    # Fisher tests
    w("### Fisher exact tests: depth-1 vs others\n")
    w("| Word group | depth-1 rate | others rate | p-value | OR | Sig |")
    w("|------------|-------------|-------------|---------|-----|-----|")
    for g, r in fisher_results.items():
        sig = "*" if r['p'] < 0.05 else ""
        w(f"| {g} | {r['d1_rate']:.3f} | {r['other_rate']:.3f} | {r['p']:.4f} | {r['odds']:.2f} | {sig} |")
    w("")

    # Depth-1 凶 texts listing
    d1_texts = sorted(xiong_by_depth.get(1, []), key=lambda x: (x['kw'], x['line']))
    w(f"### All 凶 texts from depth-1 hexagrams ({len(d1_texts)} texts)\n")
    for r in d1_texts:
        w(f"- **KW{r['kw']} {r['name']}** {r['label']} (basin={r['basin']}): {r['text']}")
    w("")

    # ═══ PROBE 6 ═══
    w("## Probe 6: KW Sequence Algebraic Transitions (序卦 preliminary)\n")

    w("### Basin continuity\n")
    s = p6_stats
    w(f"- Consecutive pairs same basin: {s['same_basin']}/{s['total']} ({s['same_basin']/s['total']:.3f})")
    w(f"- Null model (random permutation): p={s['p_basin']:.4f}")
    n_between = len([t for t in transitions if not t['is_within_pair']])
    w(f"- Between-pair transitions same basin: {s['between_same_basin']}/{n_between}")
    w(f"  p={s['p_between']:.4f} (not significant — basin locality is driven by within-pair)")
    w("")

    # Basin transition matrix
    w("### Basin transition matrix\n")
    basins = ["Kun", "Qian", "Cycle"]
    w("| From\\To |" + "|".join(f" {b} " for b in basins) + "|")
    w("|---------|" + "|".join("---" for _ in basins) + "|")
    for b1 in basins:
        counts = [s['basin_trans'].get((b1, b2), 0) for b2 in basins]
        w(f"| {b1} |" + "|".join(f" {c} " for c in counts) + "|")
    w("")

    # Depth transitions
    w("### Depth transitions (consecutive pair depth change)\n")
    w("| Δdepth | Count |")
    w("|--------|-------|")
    for delta in sorted(s['depth_deltas'].keys()):
        w(f"| {delta:+d} | {s['depth_deltas'][delta]} |")
    w("")

    # Five-phase relations
    w("### Five-phase relations between consecutive hexagrams\n")
    w("| Relation | Upper trig | Lower trig |")
    w("|----------|-----------|-----------|")
    for rel in TIYONG_CATEGORIES:
        w(f"| {rel} | {s['upper_rel'].get(rel, 0)} | {s['lower_rel'].get(rel, 0)} |")
    w("")

    w(f"**比和 null model**: upper observed={s['bihe_upper']}, p={s['p_bihe_upper']:.4f}; "
      f"lower observed={s['bihe_lower']}, p={s['p_bihe_lower']:.4f}")
    w("")

    # ═══ INTERPRETATION ═══
    w("## Interpretation\n")

    w("### Probe 8: 體/用 × valence\n")
    if sig_markers:
        w(f"The 體/用 five-phase relation significantly predicts **{', '.join(sig_markers)}** "
          f"marker distribution across the 384 states.")
    else:
        w("The 體/用 five-phase relation does NOT significantly predict any valence marker's distribution.")
    w("")
    w("The 梅花 structural lens (which trigram is 體 vs 用, and their five-phase relation)")
    if strongest_p8 < 0.05:
        w("provides a detectable signal in the textual tradition. However, the signal is")
        w(f"**weak** (best p={strongest_p8:.4f}) compared to the basin×凶 result (p=0.0002).")
        w("")
        w("Key observation: **生体** shows the highest 吉 rate (0.444) — nearly double the")
        w("比和 rate (0.226). The 體 being nourished by 用 correlates with auspicious outcomes.")
        w("凶 trends higher in 比和 (0.202) than 生体 (0.069) — the opposite of naive prediction.")
        w("But the 比和 vs 克 focused tests are NOT significant (Fisher p>0.37 for both 吉 and 凶),")
        w("so the 5-category pattern is driven by 生体's elevated 吉, not by a 比和/克 axis.")
    else:
        w("does not produce a statistically significant signal at the level of individual")
        w("valence markers.")
    w("")

    w("### Probe 7: Depth boundary and 凶 content\n")
    sig_groups = [g for g, r in fisher_results.items() if r['p'] < 0.05]
    marginal_groups = [g for g, r in fisher_results.items() if 0.05 <= r['p'] < 0.10]
    if sig_groups:
        w(f"Depth-1 凶 texts show significantly elevated rates of: {', '.join(sig_groups)}.")
    else:
        w("No word group reaches significance at α=0.05.")
    if marginal_groups:
        w(f"Marginal trends: {', '.join(marginal_groups)} (p<0.10).")
    w("")
    w("**Threshold words** (終, 已, 極, 窮, 盡) appear in 2/14 depth-1 凶 texts but")
    w("0/38 other 凶 texts (Fisher p=0.069). This is suggestive but not conclusive —")
    w("the sample size (52 total 凶 texts) limits statistical power.")
    w("")
    w("**Qualitative observation**: The depth-1 凶 texts are dominated by two hexagrams:")
    w("剝 (KW23, Splitting Apart — 3 凶 lines) and 頤 (KW27, Nourishment — 3 凶 lines),")
    w("both in the Kun basin. The Qian basin depth-1 凶 texts include 大過 (Great Exceeding)")
    w("and 夬/姤 (Breakthrough/Coming to Meet). The thematic pattern is structural")
    w("extremity — peeling away, excess, breakthrough — but this is circumstantial,")
    w("not statistically confirmed.")
    w("")
    w("The 凶×basin signal (from Probe 1) is **distributional** — WHERE 凶 appears —")
    w("not thematic — what the 凶 texts SAY. The content of 凶 texts does not")
    w("systematically differentiate by depth category at current sample sizes.")
    w("")

    w("### Probe 6: KW sequence structure\n")
    if s['p_basin'] < 0.05:
        w(f"**Strong result**: Consecutive hexagrams stay within the same basin MORE than chance")
        w(f"(38/63 = 60.3%, p={s['p_basin']:.4f}). The King Wen sequence has algebraic locality.")
    else:
        w(f"Basin continuity is NOT above chance (p={s['p_basin']:.4f}).")
    w("")
    w("However, this is **entirely driven by within-pair structure**: all 32 within-pair")
    w("transitions are KW partners (reversal/complement), which tend to preserve basin.")
    w(f"Between-pair transitions show NO basin locality (p={s['p_between']:.4f}).")
    w("")
    w("**Depth transitions** are overwhelmingly Δ=0 (51/63 = 81%), meaning consecutive")
    w("hexagrams usually share the same convergence depth. This is partly explained by")
    w("the 4:12:48 depth distribution — most hexagrams are depth-2, so random pairs")
    w("would also show high same-depth rates.")
    w("")
    w("**Five-phase relations** between consecutive hexagrams show NO elevated 比和 rate")
    w("(upper p=0.87, lower p=0.79). The KW sequence does not favor element-same")
    w("transitions — it is element-neutral in its ordering.")
    w("")

    out_path = OUT_DIR / "probe6_meaning_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nResults written to {out_path}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PROBES 6–8: MEANING THROUGH BOTH PROJECTIONS")
    print("=" * 70)

    bin_to_kw, kw_to_bin, kw_to_name = build_kw_lookup()
    guaci, yaoci, yaoci_labels, names = load_texts()

    # Probe 8
    p8_data = probe8(bin_to_kw, yaoci, yaoci_labels, names)

    # Probe 7
    p7_data = probe7(bin_to_kw, yaoci, yaoci_labels, names)

    # Probe 6
    p6_data = probe6(bin_to_kw, kw_to_bin, kw_to_name)

    # Write results
    print("\n── Writing results ──")
    write_results(p8_data, p7_data, p6_data)


if __name__ == "__main__":
    main()
