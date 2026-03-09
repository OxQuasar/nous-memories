#!/usr/bin/env python3
"""
Probe 9: 序卦 Narrative Classification × Algebraic Transitions

Tests whether the categories of causal reasoning in the 序卦傳 correlate
with algebraic transition properties (basin, depth, I-component, five-phase).
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
    lower_trigram, upper_trigram, five_phase_relation,
    bit, fmt6, kw_partner, reverse6, MASK_ALL,
)
from sequence import KING_WEN

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p2 = _load("palace", ICHING / "huozhulin" / "02_palace_kernel.py")

# ─── Data loading ────────────────────────────────────────────────────────────

def build_kw_lookup():
    bin_to_kw, kw_to_bin, kw_to_name = {}, {}, {}
    for _, (kw_num, name, bits_str) in enumerate(KING_WEN):
        h = sum(int(c) << j for j, c in enumerate(bits_str))
        bin_to_kw[h] = kw_num
        kw_to_bin[kw_num] = h
        kw_to_name[kw_num] = name
    return bin_to_kw, kw_to_bin, kw_to_name


def load_xugua():
    with open(TEXTS_DIR / "xugua.json") as f:
        data = json.load(f)
    return {e['number']: {'name': e['name'], 'text': e['text']} for e in data['entries']}


# ─── Step 1: Classify 序卦 narratives ────────────────────────────────────────

# Classification patterns, tested in priority order
REVERSAL_PAT = re.compile(r'不可以終|不可終|不可窮|不可以久')
NEGATION_PAT = re.compile(r'不可不|不可以[^終久窮]')  # "must not fail to" / "cannot merely"
CONSEQUENCE_PAT = re.compile(r'必')
ACCUMULATION_PAT = re.compile(r'然後|而後|而後')
DEFINITION_PAT = re.compile(r'者[，,].{1,4}也')

# Categories
CAT_REVERSAL = "reversal"       # 物不可以終X → opposite arises
CAT_CONSEQUENCE = "consequence"  # X必Y — causal necessity
CAT_ACCUMULATION = "accumulation"  # 然後/而後 — sequential buildup
CAT_NEGATION = "negation"       # 不可不/不可以苟 — cannot fail to / cannot merely
CAT_ORIGIN = "origin"           # cosmogonic framing (KW1-2, KW31)
CAT_ANALOGY = "analogy"         # 莫若 — "nothing is better than"
ALL_CATS = [CAT_REVERSAL, CAT_CONSEQUENCE, CAT_ACCUMULATION,
            CAT_NEGATION, CAT_ORIGIN, CAT_ANALOGY]


def classify_narrative(kw_num, text):
    """Classify the primary reasoning type in a 序卦 narrative.
    
    Returns (category, secondary_flags).
    We look at the reasoning BEFORE 故受之以, which explains the transition.
    """
    # Special cases
    if kw_num in (1, 2):
        return CAT_ORIGIN, set()
    if kw_num == 31:
        return CAT_ORIGIN, set()

    # Split at 故受之以 to isolate the reasoning
    parts = text.split("故受之以")
    reasoning = parts[0] if len(parts) > 1 else text

    flags = set()
    if REVERSAL_PAT.search(reasoning):
        flags.add(CAT_REVERSAL)
    if NEGATION_PAT.search(reasoning) and CAT_REVERSAL not in flags:
        flags.add(CAT_NEGATION)
    if CONSEQUENCE_PAT.search(reasoning) and CAT_REVERSAL not in flags:
        flags.add(CAT_CONSEQUENCE)
    if ACCUMULATION_PAT.search(reasoning):
        flags.add(CAT_ACCUMULATION)
    if re.search(r'莫若', reasoning):
        flags.add(CAT_ANALOGY)
    if DEFINITION_PAT.search(text):
        flags.add("definition")

    # Primary category by priority: reversal > negation > consequence > accumulation > analogy
    for cat in [CAT_REVERSAL, CAT_NEGATION, CAT_CONSEQUENCE, CAT_ACCUMULATION, CAT_ANALOGY]:
        if cat in flags:
            return cat, flags - {cat, "definition"}

    # Fallback: check for loose patterns
    if "則" in reasoning:
        return CAT_CONSEQUENCE, flags
    if "而" in reasoning:
        return CAT_ACCUMULATION, flags

    return "other", flags


def classify_all(xugua):
    """Classify all 63 transitions."""
    classifications = []
    for kw_target in range(1, 65):
        entry = xugua[kw_target]
        cat, secondary = classify_narrative(kw_target, entry['text'])
        classifications.append({
            'kw': kw_target,
            'name': entry['name'],
            'text': entry['text'],
            'category': cat,
            'secondary': secondary,
        })
    return classifications


# ─── Step 2 & 3: Algebraic transition properties ────────────────────────────

def compute_transitions(kw_to_bin, classifications):
    """Compute algebraic properties for all 63 consecutive transitions."""
    transitions = []
    for i in range(63):
        kw_src = i + 1
        kw_tgt = i + 2
        h_src = kw_to_bin[kw_src]
        h_tgt = kw_to_bin[kw_tgt]

        b_src = p2.basin(h_src)
        b_tgt = p2.basin(h_tgt)
        d_src = p2.depth(h_src)
        d_tgt = p2.depth(h_tgt)
        i_src = bit(h_src, 2) ^ bit(h_src, 3)
        i_tgt = bit(h_tgt, 2) ^ bit(h_tgt, 3)

        lo_src = lower_trigram(h_src)
        up_src = upper_trigram(h_src)
        lo_tgt = lower_trigram(h_tgt)
        up_tgt = upper_trigram(h_tgt)

        # Algebraic relationship between source and target
        is_reversal = (h_tgt == reverse6(h_src))
        is_complement = (h_tgt == h_src ^ MASK_ALL)
        is_kw_partner = (h_tgt == kw_partner(h_src))

        # Five-phase relations between trigrams
        up_up_rel = five_phase_relation(
            TRIGRAM_ELEMENT[up_src], TRIGRAM_ELEMENT[up_tgt])
        lo_lo_rel = five_phase_relation(
            TRIGRAM_ELEMENT[lo_src], TRIGRAM_ELEMENT[lo_tgt])
        # "Meeting point": source's upper meets target's lower
        meet_rel = five_phase_relation(
            TRIGRAM_ELEMENT[up_src], TRIGRAM_ELEMENT[lo_tgt])

        is_within_pair = (i % 2 == 0)  # 1→2, 3→4, ... are within-pair

        transitions.append({
            'kw_src': kw_src, 'kw_tgt': kw_tgt,
            'h_src': h_src, 'h_tgt': h_tgt,
            'basin_src': b_src, 'basin_tgt': b_tgt,
            'same_basin': b_src == b_tgt,
            'depth_src': d_src, 'depth_tgt': d_tgt,
            'depth_delta': d_tgt - d_src,
            'I_src': i_src, 'I_tgt': i_tgt,
            'same_I': i_src == i_tgt,
            'is_reversal': is_reversal,
            'is_complement': is_complement,
            'is_kw_partner': is_kw_partner,
            'up_up_rel': up_up_rel,
            'lo_lo_rel': lo_lo_rel,
            'meet_rel': meet_rel,
            'is_within_pair': is_within_pair,
            'narrative_cat': classifications[kw_tgt - 1]['category'],
            'text': classifications[kw_tgt - 1]['text'],
            'name_tgt': classifications[kw_tgt - 1]['name'],
        })
    return transitions


# ─── Step 4: Cross-tabulation and tests ──────────────────────────────────────

def cross_tab_test(transitions, cat_key, prop_key, prop_values=None, subset=None):
    """Build contingency table: category × property, run χ² or Fisher."""
    data = subset if subset else transitions
    cats = sorted(set(t[cat_key] for t in data))
    if prop_values is None:
        prop_values = sorted(set(t[prop_key] for t in data))

    table = []
    for cat in cats:
        row = []
        for pv in prop_values:
            count = sum(1 for t in data if t[cat_key] == cat and t[prop_key] == pv)
            row.append(count)
        table.append(row)
    table = np.array(table)

    result = {'table': table, 'rows': cats, 'cols': prop_values}

    if table.shape[0] >= 2 and table.shape[1] >= 2:
        # Use Fisher for 2×2, χ² otherwise
        if table.shape == (2, 2):
            odds, p = stats.fisher_exact(table)
            result['test'] = 'Fisher'
            result['statistic'] = odds
            result['p'] = p
        else:
            try:
                chi2, p, dof, _ = stats.chi2_contingency(table)
                result['test'] = 'chi2'
                result['statistic'] = chi2
                result['p'] = p
                result['dof'] = dof
            except ValueError:
                result['test'] = 'chi2_failed'
                result['p'] = 1.0
    else:
        result['test'] = 'insufficient'
        result['p'] = 1.0

    return result


def depth_delta_category(delta):
    """Categorize depth change as -, 0, +."""
    if delta < 0: return "−"
    if delta > 0: return "+"
    return "0"


# ─── Step 5: Additional analyses ─────────────────────────────────────────────

def analyze_reversal_algebra(transitions):
    """Do reversal-logic narratives correspond to algebraic reversals?"""
    rev_narratives = [t for t in transitions if t['narrative_cat'] == CAT_REVERSAL]
    other_narratives = [t for t in transitions if t['narrative_cat'] != CAT_REVERSAL]

    rev_has_alg_rev = sum(1 for t in rev_narratives if t['is_reversal'])
    rev_has_alg_comp = sum(1 for t in rev_narratives if t['is_complement'])
    rev_has_partner = sum(1 for t in rev_narratives if t['is_kw_partner'])

    other_has_partner = sum(1 for t in other_narratives if t['is_kw_partner'])

    return {
        'n_rev': len(rev_narratives),
        'n_other': len(other_narratives),
        'rev_is_alg_reversal': rev_has_alg_rev,
        'rev_is_alg_complement': rev_has_alg_comp,
        'rev_is_kw_partner': rev_has_partner,
        'other_is_kw_partner': other_has_partner,
    }


def analyze_consequence_sheng(transitions):
    """Do consequence-logic narratives match 生 relations?"""
    cons_narratives = [t for t in transitions if t['narrative_cat'] == CAT_CONSEQUENCE]
    other_narratives = [t for t in transitions if t['narrative_cat'] != CAT_CONSEQUENCE]

    # Check if meeting-point relation is 生 (生体 or 体生用)
    sheng_rels = {"生体", "体生用"}
    cons_has_sheng = sum(1 for t in cons_narratives if t['meet_rel'] in sheng_rels)
    other_has_sheng = sum(1 for t in other_narratives if t['meet_rel'] in sheng_rels)

    return {
        'n_cons': len(cons_narratives),
        'n_other': len(other_narratives),
        'cons_sheng_meet': cons_has_sheng,
        'other_sheng_meet': other_has_sheng,
    }


# ─── Output ──────────────────────────────────────────────────────────────────

def write_results(classifications, transitions, between_pair):
    lines = []
    w = lines.append

    w("# Probe 9: 序卦 Narrative Classification × Algebraic Transitions\n")

    # ── Full classification table ──
    w("## 1. Full Classification Table\n")
    w("All 63 transitions with narrative type and algebraic properties.\n")

    w("### Within-pair transitions (odd→even KW#)\n")
    w("| KW# | → | Name | Cat | Basin | Depth | I | Partner? | Text |")
    w("|-----|---|------|-----|-------|-------|---|----------|------|")
    for t in transitions:
        if not t['is_within_pair']:
            continue
        partner = "✓" if t['is_kw_partner'] else ""
        w(f"| {t['kw_src']} | {t['kw_tgt']} | {t['name_tgt']} | {t['narrative_cat']} "
          f"| {t['basin_src']}→{t['basin_tgt']} | {t['depth_src']}→{t['depth_tgt']} "
          f"| {t['I_src']}→{t['I_tgt']} | {partner} "
          f"| {t['text'][:40]}{'…' if len(t['text']) > 40 else ''} |")

    w("\n### Between-pair transitions (even→odd KW#)\n")
    w("| KW# | → | Name | Cat | Basin | Depth | I | Meet rel | Text |")
    w("|-----|---|------|-----|-------|-------|---|----------|------|")
    for t in transitions:
        if t['is_within_pair']:
            continue
        w(f"| {t['kw_src']} | {t['kw_tgt']} | {t['name_tgt']} | {t['narrative_cat']} "
          f"| {t['basin_src']}→{t['basin_tgt']} | {t['depth_src']}→{t['depth_tgt']} "
          f"| {t['I_src']}→{t['I_tgt']} | {t['meet_rel']} "
          f"| {t['text'][:40]}{'…' if len(t['text']) > 40 else ''} |")

    # ── Category distribution ──
    w("\n## 2. Narrative Category Distribution\n")
    cat_counts_all = Counter(t['narrative_cat'] for t in transitions)
    cat_counts_within = Counter(t['narrative_cat'] for t in transitions if t['is_within_pair'])
    cat_counts_between = Counter(t['narrative_cat'] for t in between_pair)

    w("| Category | All (63) | Within-pair (32) | Between-pair (31) |")
    w("|----------|---------|-----------------|------------------|")
    for cat in ALL_CATS + ["other"]:
        w(f"| {cat} | {cat_counts_all.get(cat, 0)} | "
          f"{cat_counts_within.get(cat, 0)} | {cat_counts_between.get(cat, 0)} |")

    # ── Cross-tabulations (between-pair only) ──
    w("\n## 3. Cross-tabulations (Between-pair Transitions Only)\n")
    w("Focus on the 31 between-pair transitions where algebraic structure is non-trivial.\n")

    # 3a: Category × basin-preserving
    w("### 3a. Narrative category × basin preservation\n")
    r = cross_tab_test(between_pair, 'narrative_cat', 'same_basin',
                       prop_values=[True, False])
    w("| Category |" + "|".join(f" same={v} " for v in r['cols']) + "| Total |")
    w("|----------|" + "|".join("---" for _ in r['cols']) + "|-------|")
    for i, cat in enumerate(r['rows']):
        total = sum(r['table'][i])
        w(f"| {cat} |" + "|".join(f" {c} " for c in r['table'][i]) + f"| {total} |")
    if r['test'] != 'insufficient':
        w(f"\n{r['test']}: statistic={r['statistic']:.3f}, p={r['p']:.4f}")
    w("")

    # 3b: Category × depth change direction
    for t in between_pair:
        t['depth_dir'] = depth_delta_category(t['depth_delta'])
    w("### 3b. Narrative category × depth change direction\n")
    r = cross_tab_test(between_pair, 'narrative_cat', 'depth_dir',
                       prop_values=["−", "0", "+"])
    w("| Category |" + "|".join(f" Δ={v} " for v in r['cols']) + "| Total |")
    w("|----------|" + "|".join("---" for _ in r['cols']) + "|-------|")
    for i, cat in enumerate(r['rows']):
        total = sum(r['table'][i])
        w(f"| {cat} |" + "|".join(f" {c} " for c in r['table'][i]) + f"| {total} |")
    if r['test'] != 'insufficient':
        w(f"\n{r['test']}: statistic={r['statistic']:.3f}, p={r['p']:.4f}")
    w("")

    # 3c: Category × I-component preserving
    w("### 3c. Narrative category × I-component preservation\n")
    r = cross_tab_test(between_pair, 'narrative_cat', 'same_I',
                       prop_values=[True, False])
    w("| Category |" + "|".join(f" same_I={v} " for v in r['cols']) + "| Total |")
    w("|----------|" + "|".join("---" for _ in r['cols']) + "|-------|")
    for i, cat in enumerate(r['rows']):
        total = sum(r['table'][i])
        w(f"| {cat} |" + "|".join(f" {c} " for c in r['table'][i]) + f"| {total} |")
    if r['test'] != 'insufficient':
        w(f"\n{r['test']}: statistic={r['statistic']:.3f}, p={r['p']:.4f}")
    w("")

    # 3d: Category × meeting-point five-phase relation
    w("### 3d. Narrative category × meeting-point 五行 relation\n")
    w("Meeting point = source upper trigram element → target lower trigram element.\n")
    rels_order = ["比和", "生体", "体生用", "克体", "体克用"]
    r = cross_tab_test(between_pair, 'narrative_cat', 'meet_rel',
                       prop_values=rels_order)
    w("| Category |" + "|".join(f" {v} " for v in r['cols']) + "| Total |")
    w("|----------|" + "|".join("---" for _ in r['cols']) + "|-------|")
    for i, cat in enumerate(r['rows']):
        total = sum(r['table'][i])
        w(f"| {cat} |" + "|".join(f" {c} " for c in r['table'][i]) + f"| {total} |")
    if r['test'] != 'insufficient':
        w(f"\n{r['test']}: statistic={r['statistic']:.3f}, p={r['p']:.4f}")
    w("")

    # ── Additional analyses ──
    w("## 4. Additional Analyses\n")

    # 4a: Basin-crossing vs basin-preserving reasoning
    w("### 4a. Reasoning type for basin-crossing vs basin-preserving\n")
    crossing = [t for t in between_pair if not t['same_basin']]
    preserving = [t for t in between_pair if t['same_basin']]
    w(f"Basin-crossing transitions: {len(crossing)}")
    w(f"Basin-preserving transitions: {len(preserving)}\n")

    w("**Basin-crossing transitions:**\n")
    cross_cats = Counter(t['narrative_cat'] for t in crossing)
    for cat in ALL_CATS + ["other"]:
        if cross_cats.get(cat, 0) > 0:
            w(f"- {cat}: {cross_cats[cat]}")
    w("")
    w("**Basin-preserving transitions:**\n")
    pres_cats = Counter(t['narrative_cat'] for t in preserving)
    for cat in ALL_CATS + ["other"]:
        if pres_cats.get(cat, 0) > 0:
            w(f"- {cat}: {pres_cats[cat]}")
    w("")

    # Fisher: reversal vs others for basin-crossing
    rev_crossing = sum(1 for t in crossing if t['narrative_cat'] == CAT_REVERSAL)
    rev_preserving = sum(1 for t in preserving if t['narrative_cat'] == CAT_REVERSAL)
    other_crossing = len(crossing) - rev_crossing
    other_preserving = len(preserving) - rev_preserving
    if len(crossing) > 0 and len(preserving) > 0:
        table_2x2 = np.array([[rev_crossing, other_crossing],
                               [rev_preserving, other_preserving]])
        odds, p = stats.fisher_exact(table_2x2)
        w(f"Reversal narrative × basin-crossing: Fisher OR={odds:.2f}, p={p:.4f}")
        w(f"  Reversal in crossing: {rev_crossing}/{len(crossing)}")
        w(f"  Reversal in preserving: {rev_preserving}/{len(preserving)}")
    w("")

    # 4b: Reversal narratives vs algebraic reversals
    w("### 4b. Reversal narratives vs algebraic operations\n")
    rev_alg = analyze_reversal_algebra(transitions)
    w(f"Reversal narratives (all transitions): {rev_alg['n_rev']}")
    w(f"  - Algebraic reversal (bit-reverse): {rev_alg['rev_is_alg_reversal']}")
    w(f"  - Algebraic complement (bit-flip): {rev_alg['rev_is_alg_complement']}")
    w(f"  - KW partner (rev or comp): {rev_alg['rev_is_kw_partner']}")
    w(f"Other narratives: {rev_alg['n_other']}")
    w(f"  - KW partner: {rev_alg['other_is_kw_partner']}")
    w("")

    # Reversal narratives: which are within-pair vs between-pair?
    rev_within = sum(1 for t in transitions
                     if t['narrative_cat'] == CAT_REVERSAL and t['is_within_pair'])
    rev_between = sum(1 for t in transitions
                      if t['narrative_cat'] == CAT_REVERSAL and not t['is_within_pair'])
    w(f"Reversal narratives within-pair: {rev_within}")
    w(f"Reversal narratives between-pair: {rev_between}")
    w("")

    # List reversal narratives with algebraic details
    w("**All reversal-narrative transitions:**\n")
    w("| KW | → | Pair type | Alg reversal? | Alg complement? | Basin | Text |")
    w("|-----|---|-----------|--------------|----------------|-------|------|")
    for t in transitions:
        if t['narrative_cat'] != CAT_REVERSAL:
            continue
        pair_type = "within" if t['is_within_pair'] else "between"
        rev = "✓" if t['is_reversal'] else ""
        comp = "✓" if t['is_complement'] else ""
        w(f"| {t['kw_src']} | {t['kw_tgt']} | {pair_type} | {rev} | {comp} "
          f"| {t['basin_src']}→{t['basin_tgt']} | {t['text'][:35]}… |")
    w("")

    # 4c: Consequence narratives and 生 relations
    w("### 4c. Consequence narratives and 生 relations\n")
    cons_sheng = analyze_consequence_sheng(transitions)
    sheng_rels = {"生体", "体生用"}
    n_cons = cons_sheng['n_cons']
    n_other = cons_sheng['n_other']
    cons_s = cons_sheng['cons_sheng_meet']
    other_s = cons_sheng['other_sheng_meet']
    w(f"Consequence narratives: {n_cons}")
    w(f"  - Meeting-point is 生 relation: {cons_s} ({cons_s/n_cons*100:.1f}%)")
    w(f"Other narratives: {n_other}")
    w(f"  - Meeting-point is 生 relation: {other_s} ({other_s/n_other*100:.1f}%)")
    if n_cons > 0 and n_other > 0:
        table_2x2 = np.array([[cons_s, n_cons - cons_s],
                               [other_s, n_other - other_s]])
        odds, p = stats.fisher_exact(table_2x2)
        w(f"Fisher OR={odds:.2f}, p={p:.4f}")
    w("")

    # Also check for between-pair only
    cons_bp = [t for t in between_pair if t['narrative_cat'] == CAT_CONSEQUENCE]
    other_bp = [t for t in between_pair if t['narrative_cat'] != CAT_CONSEQUENCE]
    if cons_bp and other_bp:
        cons_s_bp = sum(1 for t in cons_bp if t['meet_rel'] in sheng_rels)
        other_s_bp = sum(1 for t in other_bp if t['meet_rel'] in sheng_rels)
        w(f"Between-pair only:")
        w(f"  Consequence: {cons_s_bp}/{len(cons_bp)} have 生 meeting-point")
        w(f"  Others: {other_s_bp}/{len(other_bp)} have 生 meeting-point")
        table_2x2 = np.array([[cons_s_bp, len(cons_bp) - cons_s_bp],
                               [other_s_bp, len(other_bp) - other_s_bp]])
        odds, p = stats.fisher_exact(table_2x2)
        w(f"  Fisher OR={odds:.2f}, p={p:.4f}")
    w("")

    # ── Interpretation ──
    w("## 5. Interpretation\n")

    # Summarize which tests are significant
    w("### Statistical summary\n")
    w("All tests below are on the 31 between-pair transitions only.\n")

    tests = [
        ("Category × basin preservation", "3a"),
        ("Category × depth direction", "3b"),
        ("Category × I-component", "3c"),
        ("Category × meeting-point 五行", "3d"),
    ]

    # Re-run tests for summary
    test_results = {}
    r = cross_tab_test(between_pair, 'narrative_cat', 'same_basin',
                       prop_values=[True, False])
    test_results['basin'] = r
    r = cross_tab_test(between_pair, 'narrative_cat', 'depth_dir',
                       prop_values=["−", "0", "+"])
    test_results['depth'] = r
    r = cross_tab_test(between_pair, 'narrative_cat', 'same_I',
                       prop_values=[True, False])
    test_results['I'] = r
    r = cross_tab_test(between_pair, 'narrative_cat', 'meet_rel',
                       prop_values=rels_order)
    test_results['meet'] = r

    w("| Test | Statistic | p-value | Sig |")
    w("|------|-----------|---------|-----|")
    for (label, _), key in zip(tests, ['basin', 'depth', 'I', 'meet']):
        r = test_results[key]
        if r['test'] == 'insufficient':
            w(f"| {label} | — | — | — |")
        else:
            sig = "***" if r['p'] < 0.001 else "**" if r['p'] < 0.01 else "*" if r['p'] < 0.05 else ""
            stat_name = "χ²" if r['test'] == 'chi2' else "OR"
            w(f"| {label} | {stat_name}={r['statistic']:.3f} | {r['p']:.4f} | {sig} |")
    w("")

    # Qualitative interpretation
    any_sig = any(r['p'] < 0.05 for r in test_results.values() if r['test'] != 'insufficient')
    if any_sig:
        w("Significant associations found between narrative categories and algebraic properties.")
    else:
        w("**No significant associations** between 序卦 narrative categories and algebraic")
        w("transition properties. The reasoning the 序卦傳 uses to justify the King Wen")
        w("sequence does not correlate with basin, depth, I-component, or five-phase")
        w("relations between consecutive hexagrams.")
    w("")

    w("### Reversal narratives\n")
    w(f"Of {rev_alg['n_rev']} reversal narratives across all 63 transitions, "
      f"{rev_alg['rev_is_kw_partner']} are within-pair KW partners. "
      f"These are the trivial within-pair transitions where reversal/complement")
    w(f"is the algebraic relationship by construction. The {rev_between} between-pair")
    w("reversal narratives describe conceptual reversal ('things cannot remain X forever')")
    w("but this does NOT correspond to algebraic reversal/complement operations.")
    w("")

    w("### Consequence narratives and 生\n")
    w(f"Consequence-logic narratives ('X必Y') {'' if cons_s/n_cons > other_s/n_other else 'do not '}"
      f"show elevated 生 meeting-point relations compared to other categories.")
    w("The 序卦's causal reasoning does not systematically track the five-phase")
    w("生 (generation) relationship between consecutive hexagrams' trigrams.")
    w("")

    out_path = OUT_DIR / "probe7_xugua_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nResults written to {out_path}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PROBE 9: 序卦 NARRATIVE × ALGEBRAIC TRANSITIONS")
    print("=" * 70)

    bin_to_kw, kw_to_bin, kw_to_name = build_kw_lookup()
    xugua = load_xugua()

    # Step 1: Classify
    print("\n── Step 1: Classifying narratives ──")
    classifications = classify_all(xugua)

    cat_counts = Counter(c['category'] for c in classifications)
    print("  Category distribution:")
    for cat in ALL_CATS + ["other"]:
        print(f"    {cat}: {cat_counts.get(cat, 0)}")

    # Print all classifications
    print("\n  All classifications:")
    for c in classifications:
        sec = f" +{','.join(c['secondary'])}" if c['secondary'] else ""
        print(f"    KW{c['kw']:2d} [{c['category']:13s}{sec}] {c['text'][:60]}")

    # Steps 2-3: Compute transitions
    print("\n── Steps 2-3: Computing algebraic transitions ──")
    transitions = compute_transitions(kw_to_bin, classifications)

    within_pair = [t for t in transitions if t['is_within_pair']]
    between_pair = [t for t in transitions if not t['is_within_pair']]
    print(f"  Within-pair: {len(within_pair)}")
    print(f"  Between-pair: {len(between_pair)}")

    # Step 4: Cross-tabulations
    print("\n── Step 4: Cross-tabulations (between-pair) ──")

    # Cat × basin-preserving
    for t in between_pair:
        t['depth_dir'] = depth_delta_category(t['depth_delta'])

    r = cross_tab_test(between_pair, 'narrative_cat', 'same_basin',
                       prop_values=[True, False])
    print(f"  Cat × basin: {r['test']} p={r['p']:.4f}")

    r = cross_tab_test(between_pair, 'narrative_cat', 'depth_dir',
                       prop_values=["−", "0", "+"])
    print(f"  Cat × depth: {r['test']} p={r['p']:.4f}")

    r = cross_tab_test(between_pair, 'narrative_cat', 'same_I',
                       prop_values=[True, False])
    print(f"  Cat × I-comp: {r['test']} p={r['p']:.4f}")

    r = cross_tab_test(between_pair, 'narrative_cat', 'meet_rel',
                       prop_values=["比和", "生体", "体生用", "克体", "体克用"])
    print(f"  Cat × meet-rel: {r['test']} p={r['p']:.4f}")

    # Step 5: Additional
    print("\n── Step 5: Additional analyses ──")
    rev_alg = analyze_reversal_algebra(transitions)
    print(f"  Reversal narratives: {rev_alg['n_rev']}")
    print(f"    KW partners: {rev_alg['rev_is_kw_partner']}")

    cons_sheng = analyze_consequence_sheng(transitions)
    print(f"  Consequence narratives: {cons_sheng['n_cons']}")
    print(f"    生 meeting-point: {cons_sheng['cons_sheng_meet']}")

    # Write output
    print("\n── Writing results ──")
    write_results(classifications, transitions, between_pair)

    print("\nDone.")


if __name__ == "__main__":
    main()
