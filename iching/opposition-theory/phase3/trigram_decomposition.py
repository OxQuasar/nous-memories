#!/usr/bin/env python3
"""
Phase 3: Trigram and Nuclear Trigram Decomposition of KW Pairs

For each of the 32 KW pairs (a, b), computes:
  1. Trigram-level decomposition (lower/upper) and inter-partner relationships
  2. Nuclear trigram decomposition (L2-L3-L4, L3-L4-L5) and XOR/Hamming structure
  3. Weight analysis at each sub-hexagram level
  4. Summary statistics (reversal vs palindromic, distributions, correlations)
  5. Cross-decomposition: mirror-pair vs trigram overlap matrix

Encoding: L1 = bit 0 (bottom), L6 = bit 5 (top).
KW rule: b = reverse(a) for non-palindromes, b = complement(a) for palindromes.
"""

import math
from collections import Counter
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N  # 64
NUM_PAIRS = NUM_STATES // 2  # 32
MASK_ALL = (1 << N) - 1

TRIGRAM_NAMES = {  # keyed by value where bit0=bottom line, bit2=top line
    0b000: "Kun ☷",
    0b001: "Zhen ☳",
    0b010: "Kan ☵",
    0b011: "Dui ☱",
    0b100: "Gen ☶",
    0b101: "Li ☲",
    0b110: "Xun ☴",
    0b111: "Qian ☰",
}

# ─── Bit operations ──────────────────────────────────────────────────────────

def popcount(x):
    return bin(x).count('1')

def reverse6(x):
    """Reverse a 6-bit string: bit i -> bit (5-i)."""
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    return r

def reverse3(x):
    """Reverse a 3-bit string: bit i -> bit (2-i)."""
    r = 0
    for i in range(3):
        if x & (1 << i):
            r |= 1 << (2 - i)
    return r

def complement3(x):
    return x ^ 0b111

def fmt6(x):
    return format(x, '06b')

def fmt3(x):
    return format(x, '03b')

# ─── Trigram extraction ──────────────────────────────────────────────────────

def lower_trigram(x):
    """L1, L2, L3 = bits 0, 1, 2."""
    return x & 0b111

def upper_trigram(x):
    """L4, L5, L6 = bits 3, 4, 5."""
    return (x >> 3) & 0b111

def lower_nuclear(x):
    """L2, L3, L4 = bits 1, 2, 3."""
    return (x >> 1) & 0b111

def upper_nuclear(x):
    """L3, L4, L5 = bits 2, 3, 4."""
    return (x >> 2) & 0b111

# ─── Trigram relationship classification ─────────────────────────────────────

def classify_trigram_relation(t1, t2):
    """Classify the relationship between two trigrams."""
    if t1 == t2:
        return "identity"
    if t2 == reverse3(t1):
        if t2 == complement3(t1):
            return "rev=comp"  # both at once (e.g., 010 <-> 101)
        return "reversal"
    if t2 == complement3(t1):
        return "complement"
    if t2 == complement3(reverse3(t1)):
        return "comp∘rev"
    return "other"

# ─── KW pair generation ─────────────────────────────────────────────────────

def generate_kw_pairs():
    """Generate 32 KW pairs. Returns list of (a, b, pair_type)."""
    paired = set()
    pairs = []
    for a in range(NUM_STATES):
        if a in paired:
            continue
        rev_a = reverse6(a)
        if rev_a == a:  # palindrome
            b = a ^ MASK_ALL  # complement
            pair_type = "palindromic"
        else:
            b = rev_a
            pair_type = "reversal"
        # canonical order: smaller index first
        if a > b:
            a, b = b, a
        pairs.append((a, b, pair_type))
        paired.add(a)
        paired.add(b)
    return pairs

# ─── Per-pair decomposition ──────────────────────────────────────────────────

def decompose_pair(a, b, pair_type):
    """Full trigram/nuclear decomposition for one KW pair."""
    d = {}
    d['a'] = a
    d['b'] = b
    d['pair_type'] = pair_type

    # Trigrams
    la, ua = lower_trigram(a), upper_trigram(a)
    lb, ub = lower_trigram(b), upper_trigram(b)
    d['lower_a'] = la
    d['upper_a'] = ua
    d['lower_b'] = lb
    d['upper_b'] = ub

    # Trigram relationships: direct and cross
    d['lower_rel'] = classify_trigram_relation(la, lb)   # lower(a) vs lower(b)
    d['upper_rel'] = classify_trigram_relation(ua, ub)   # upper(a) vs upper(b)
    d['cross_la_ub'] = classify_trigram_relation(la, ub) # lower(a) vs upper(b)
    d['cross_ua_lb'] = classify_trigram_relation(ua, lb) # upper(a) vs lower(b)

    # For reversal pairs: verify swap+reverse pattern
    # rev₆ swaps and reverses trigrams: upper(b) = rev₃(lower(a)), lower(b) = rev₃(upper(a))
    if pair_type == "reversal":
        d['swap_rev_check'] = (ub == reverse3(la) and lb == reverse3(ua))
    else:
        d['swap_rev_check'] = None

    # Nuclear trigrams
    ln_a, un_a = lower_nuclear(a), upper_nuclear(a)
    ln_b, un_b = lower_nuclear(b), upper_nuclear(b)
    d['lnuc_a'] = ln_a
    d['unuc_a'] = un_a
    d['lnuc_b'] = ln_b
    d['unuc_b'] = un_b

    # Nuclear XOR and Hamming
    d['lnuc_xor'] = ln_a ^ ln_b
    d['unuc_xor'] = un_a ^ un_b
    d['lnuc_hamming'] = popcount(ln_a ^ ln_b)
    d['unuc_hamming'] = popcount(un_a ^ un_b)

    # Nuclear relationship classification
    d['lnuc_rel'] = classify_trigram_relation(ln_a, ln_b)
    d['unuc_rel'] = classify_trigram_relation(un_a, un_b)

    # Weights
    d['w_lower_a'] = popcount(la)
    d['w_upper_a'] = popcount(ua)
    d['w_lower_b'] = popcount(lb)
    d['w_upper_b'] = popcount(ub)
    d['w_lnuc_a'] = popcount(ln_a)
    d['w_unuc_a'] = popcount(un_a)
    d['w_lnuc_b'] = popcount(ln_b)
    d['w_unuc_b'] = popcount(un_b)

    # Weight differences
    d['dw_lower'] = abs(d['w_lower_a'] - d['w_lower_b'])
    d['dw_upper'] = abs(d['w_upper_a'] - d['w_upper_b'])
    d['dw_lnuc'] = abs(d['w_lnuc_a'] - d['w_lnuc_b'])
    d['dw_unuc'] = abs(d['w_unuc_a'] - d['w_unuc_b'])

    return d

# ─── Summary statistics ─────────────────────────────────────────────────────

def compute_statistics(decompositions):
    """Compute aggregate statistics from all 32 pair decompositions."""
    stats = {}

    rev_pairs = [d for d in decompositions if d['pair_type'] == 'reversal']
    pal_pairs = [d for d in decompositions if d['pair_type'] == 'palindromic']
    stats['n_reversal'] = len(rev_pairs)
    stats['n_palindromic'] = len(pal_pairs)

    # Trigram relationship distributions
    for group_name, group in [('all', decompositions), ('reversal', rev_pairs), ('palindromic', pal_pairs)]:
        for rel_type in ['lower_rel', 'upper_rel', 'cross_la_ub', 'cross_ua_lb']:
            stats[f'{group_name}_{rel_type}'] = Counter(d[rel_type] for d in group)

    # Nuclear XOR mask distributions
    for group_name, group in [('all', decompositions), ('reversal', rev_pairs), ('palindromic', pal_pairs)]:
        stats[f'{group_name}_lnuc_xor_dist'] = Counter(d['lnuc_xor'] for d in group)
        stats[f'{group_name}_unuc_xor_dist'] = Counter(d['unuc_xor'] for d in group)

    # Nuclear weight correlation
    lnuc_wa = np.array([d['w_lnuc_a'] for d in decompositions], dtype=float)
    lnuc_wb = np.array([d['w_lnuc_b'] for d in decompositions], dtype=float)
    unuc_wa = np.array([d['w_unuc_a'] for d in decompositions], dtype=float)
    unuc_wb = np.array([d['w_unuc_b'] for d in decompositions], dtype=float)

    if np.std(lnuc_wa) > 0 and np.std(lnuc_wb) > 0:
        stats['lnuc_weight_corr'] = float(np.corrcoef(lnuc_wa, lnuc_wb)[0, 1])
    else:
        stats['lnuc_weight_corr'] = float('nan')
    if np.std(unuc_wa) > 0 and np.std(unuc_wb) > 0:
        stats['unuc_weight_corr'] = float(np.corrcoef(unuc_wa, unuc_wb)[0, 1])
    else:
        stats['unuc_weight_corr'] = float('nan')

    # Full hexagram weight correlation for reference
    hex_wa = np.array([popcount(d['a']) for d in decompositions], dtype=float)
    hex_wb = np.array([popcount(d['b']) for d in decompositions], dtype=float)
    stats['hex_weight_corr'] = float(np.corrcoef(hex_wa, hex_wb)[0, 1])

    # Trigram-level weight correlations
    low_wa = np.array([d['w_lower_a'] for d in decompositions], dtype=float)
    low_wb = np.array([d['w_lower_b'] for d in decompositions], dtype=float)
    up_wa = np.array([d['w_upper_a'] for d in decompositions], dtype=float)
    up_wb = np.array([d['w_upper_b'] for d in decompositions], dtype=float)
    stats['lower_trig_weight_corr'] = float(np.corrcoef(low_wa, low_wb)[0, 1])
    stats['upper_trig_weight_corr'] = float(np.corrcoef(up_wa, up_wb)[0, 1])

    # Mean |Δw| at each level
    stats['mean_dw_lower'] = np.mean([d['dw_lower'] for d in decompositions])
    stats['mean_dw_upper'] = np.mean([d['dw_upper'] for d in decompositions])
    stats['mean_dw_lnuc'] = np.mean([d['dw_lnuc'] for d in decompositions])
    stats['mean_dw_unuc'] = np.mean([d['dw_unuc'] for d in decompositions])

    # Same for reversal only
    if rev_pairs:
        stats['rev_mean_dw_lower'] = np.mean([d['dw_lower'] for d in rev_pairs])
        stats['rev_mean_dw_upper'] = np.mean([d['dw_upper'] for d in rev_pairs])
        stats['rev_mean_dw_lnuc'] = np.mean([d['dw_lnuc'] for d in rev_pairs])
        stats['rev_mean_dw_unuc'] = np.mean([d['dw_unuc'] for d in rev_pairs])

    # Swap+reverse check pass rate
    rev_checks = [d['swap_rev_check'] for d in rev_pairs]
    stats['swap_rev_all_pass'] = all(rev_checks)
    stats['swap_rev_pass_count'] = sum(rev_checks)

    return stats

# ─── Cross-decomposition analysis ───────────────────────────────────────────

def cross_decomposition():
    """
    Mirror-pair layers: O={L1,L6}, M={L2,L5}, I={L3,L4}
    Trigram layers: lower={L1,L2,L3}, upper={L4,L5,L6}
    Nuclear layers: lower_nuc={L2,L3,L4}, upper_nuc={L3,L4,L5}

    Compute overlap matrices.
    """
    # Line positions (1-indexed in the I Ching, 0-indexed as bits)
    lines = {
        'L1': 0, 'L2': 1, 'L3': 2, 'L4': 3, 'L5': 4, 'L6': 5
    }

    mirror_pairs = {'O (outer)': {'L1', 'L6'}, 'M (middle)': {'L2', 'L5'}, 'I (inner)': {'L3', 'L4'}}
    trigram_layers = {'lower': {'L1', 'L2', 'L3'}, 'upper': {'L4', 'L5', 'L6'}}
    nuclear_layers = {'lower_nuc': {'L2', 'L3', 'L4'}, 'upper_nuc': {'L3', 'L4', 'L5'}}

    # Mirror-pair × trigram overlap
    mp_trig_matrix = {}
    for mp_name, mp_lines in mirror_pairs.items():
        for trig_name, trig_lines in trigram_layers.items():
            mp_trig_matrix[(mp_name, trig_name)] = mp_lines & trig_lines

    # Mirror-pair × nuclear overlap
    mp_nuc_matrix = {}
    for mp_name, mp_lines in mirror_pairs.items():
        for nuc_name, nuc_lines in nuclear_layers.items():
            mp_nuc_matrix[(mp_name, nuc_name)] = mp_lines & nuc_lines

    # Per-line membership
    line_membership = {}
    for L in ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']:
        mp = [name for name, lines in mirror_pairs.items() if L in lines][0]
        trig = [name for name, lines in trigram_layers.items() if L in lines][0]
        nuc_list = [name for name, lines in nuclear_layers.items() if L in lines]
        nuc = ', '.join(nuc_list) if nuc_list else 'none'
        line_membership[L] = (mp, trig, nuc)

    return {
        'mirror_pairs': mirror_pairs,
        'trigram_layers': trigram_layers,
        'nuclear_layers': nuclear_layers,
        'mp_trig_matrix': mp_trig_matrix,
        'mp_nuc_matrix': mp_nuc_matrix,
        'line_membership': line_membership,
    }

# ─── Output formatting ──────────────────────────────────────────────────────

def format_results(pairs, decomps, stats, cross):
    """Format all results as markdown."""
    lines = []
    w = lines.append

    w("# Phase 3: Trigram and Nuclear Trigram Decomposition of KW Pairs\n")

    # ── 1. Full decomposition table ──
    w("## 1. Full Trigram Decomposition (32 pairs)\n")
    w("Encoding: L1=bit0 (bottom) … L6=bit5 (top). Trigrams shown as 3-bit binary.\n")
    w("| # | a | b | Type | lower(a) | upper(a) | lower(b) | upper(b) | lower rel | upper rel | cross(la↔ub) | cross(ua↔lb) |")
    w("|---|---|---|------|----------|----------|----------|----------|-----------|-----------|-------------|-------------|")
    for i, d in enumerate(decomps):
        w(f"| {i+1} | {fmt6(d['a'])} | {fmt6(d['b'])} | {d['pair_type'][:3]} "
          f"| {fmt3(d['lower_a'])} | {fmt3(d['upper_a'])} "
          f"| {fmt3(d['lower_b'])} | {fmt3(d['upper_b'])} "
          f"| {d['lower_rel']} | {d['upper_rel']} "
          f"| {d['cross_la_ub']} | {d['cross_ua_lb']} |")

    w("")

    # ── Swap+reverse verification ──
    w("### Reversal pair structure verification\n")
    w(f"For reversal pairs: upper(b) = rev₃(lower(a)) and lower(b) = rev₃(upper(a)).\n")
    w(f"**All {stats['n_reversal']} reversal pairs pass: {stats['swap_rev_all_pass']}** "
      f"({stats['swap_rev_pass_count']}/{stats['n_reversal']})\n")

    # ── 2. Nuclear trigram table ──
    w("## 2. Nuclear Trigram Decomposition\n")
    w("Nuclear trigrams: lower_nuc = (L2,L3,L4) = bits 1,2,3; upper_nuc = (L3,L4,L5) = bits 2,3,4.\n")
    w("| # | a | b | Type | lnuc(a) | unuc(a) | lnuc(b) | unuc(b) | lnuc XOR | unuc XOR | lnuc H | unuc H |")
    w("|---|---|---|------|---------|---------|---------|---------|----------|----------|--------|--------|")
    for i, d in enumerate(decomps):
        w(f"| {i+1} | {fmt6(d['a'])} | {fmt6(d['b'])} | {d['pair_type'][:3]} "
          f"| {fmt3(d['lnuc_a'])} | {fmt3(d['unuc_a'])} "
          f"| {fmt3(d['lnuc_b'])} | {fmt3(d['unuc_b'])} "
          f"| {fmt3(d['lnuc_xor'])} | {fmt3(d['unuc_xor'])} "
          f"| {d['lnuc_hamming']} | {d['unuc_hamming']} |")

    w("")

    # Nuclear relationship classification
    w("### Nuclear trigram relationships\n")
    w("| # | a | b | Type | lnuc rel | unuc rel |")
    w("|---|---|---|------|----------|----------|")
    for i, d in enumerate(decomps):
        w(f"| {i+1} | {fmt6(d['a'])} | {fmt6(d['b'])} | {d['pair_type'][:3]} "
          f"| {d['lnuc_rel']} | {d['unuc_rel']} |")

    w("")

    # ── 3. Weight analysis ──
    w("## 3. Sub-hexagram Weight Analysis\n")
    w("w = yang-count (popcount). Δw = |w(a_part) − w(b_part)|.\n")
    w("| # | a | b | Type | w(lo_a) | w(up_a) | w(lo_b) | w(up_b) | Δw lo | Δw up | w(ln_a) | w(un_a) | w(ln_b) | w(un_b) | Δw ln | Δw un |")
    w("|---|---|---|------|---------|---------|---------|---------|-------|-------|---------|---------|---------|---------|-------|-------|")
    for i, d in enumerate(decomps):
        w(f"| {i+1} | {fmt6(d['a'])} | {fmt6(d['b'])} | {d['pair_type'][:3]} "
          f"| {d['w_lower_a']} | {d['w_upper_a']} "
          f"| {d['w_lower_b']} | {d['w_upper_b']} "
          f"| {d['dw_lower']} | {d['dw_upper']} "
          f"| {d['w_lnuc_a']} | {d['w_unuc_a']} "
          f"| {d['w_lnuc_b']} | {d['w_unuc_b']} "
          f"| {d['dw_lnuc']} | {d['dw_unuc']} |")

    w("")

    # ── 4. Summary statistics ──
    w("## 4. Summary Statistics\n")

    w("### Trigram relationship distributions\n")
    for group in ['all', 'reversal', 'palindromic']:
        n = stats[f'n_{group.replace("all", "reversal")}'] if group != 'all' else len(decomps)
        w(f"#### {group.capitalize()} pairs (n={n})\n")
        w("| Relationship | lower(a)↔lower(b) | upper(a)↔upper(b) | lower(a)↔upper(b) | upper(a)↔lower(b) |")
        w("|-------------|-------------------|-------------------|-------------------|-------------------|")
        all_rels = set()
        for rel_type in ['lower_rel', 'upper_rel', 'cross_la_ub', 'cross_ua_lb']:
            all_rels.update(stats[f'{group}_{rel_type}'].keys())
        for rel in sorted(all_rels):
            counts = []
            for rel_type in ['lower_rel', 'upper_rel', 'cross_la_ub', 'cross_ua_lb']:
                c = stats[f'{group}_{rel_type}'].get(rel, 0)
                counts.append(str(c))
            w(f"| {rel} | {' | '.join(counts)} |")
        w("")

    w("### Nuclear XOR mask distributions\n")
    for group in ['all', 'reversal', 'palindromic']:
        w(f"#### {group.capitalize()} pairs\n")
        w("| XOR mask | lower nuclear | upper nuclear |")
        w("|----------|--------------|--------------|")
        all_masks = set()
        all_masks.update(stats[f'{group}_lnuc_xor_dist'].keys())
        all_masks.update(stats[f'{group}_unuc_xor_dist'].keys())
        for mask in sorted(all_masks):
            lc = stats[f'{group}_lnuc_xor_dist'].get(mask, 0)
            uc = stats[f'{group}_unuc_xor_dist'].get(mask, 0)
            w(f"| {fmt3(mask)} | {lc} | {uc} |")
        w("")

    w("### Weight correlations within KW pairs\n")
    w("| Level | Pearson r |")
    w("|-------|----------|")
    w(f"| Full hexagram (w(a) vs w(b)) | {stats['hex_weight_corr']:.4f} |")
    w(f"| Lower trigram | {stats['lower_trig_weight_corr']:.4f} |")
    w(f"| Upper trigram | {stats['upper_trig_weight_corr']:.4f} |")
    w(f"| Lower nuclear | {stats['lnuc_weight_corr']:.4f} |")
    w(f"| Upper nuclear | {stats['unuc_weight_corr']:.4f} |")
    w("")

    w("### Mean |Δw| by sub-hexagram level\n")
    w("| Level | All pairs | Reversal only |")
    w("|-------|-----------|---------------|")
    w(f"| Lower trigram | {stats['mean_dw_lower']:.4f} | {stats.get('rev_mean_dw_lower', 'N/A'):.4f} |")
    w(f"| Upper trigram | {stats['mean_dw_upper']:.4f} | {stats.get('rev_mean_dw_upper', 'N/A'):.4f} |")
    w(f"| Lower nuclear | {stats['mean_dw_lnuc']:.4f} | {stats.get('rev_mean_dw_lnuc', 'N/A'):.4f} |")
    w(f"| Upper nuclear | {stats['mean_dw_unuc']:.4f} | {stats.get('rev_mean_dw_unuc', 'N/A'):.4f} |")
    w("")

    # ── 5. Cross-decomposition analysis ──
    w("## 5. Cross-Decomposition Analysis\n")

    w("### Line position membership\n")
    w("| Line | Mirror pair | Trigram | Nuclear |")
    w("|------|-------------|---------|---------|")
    for L in ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']:
        mp, trig, nuc = cross['line_membership'][L]
        w(f"| {L} (bit {int(L[1])-1}) | {mp} | {trig} | {nuc} |")
    w("")

    w("### Mirror-pair × Trigram overlap matrix\n")
    w("Each cell shows which line positions fall in both categories.\n")
    w("| Mirror pair | lower | upper |")
    w("|-------------|-------|-------|")
    for mp in ['O (outer)', 'M (middle)', 'I (inner)']:
        lo = cross['mp_trig_matrix'].get((mp, 'lower'), set())
        up = cross['mp_trig_matrix'].get((mp, 'upper'), set())
        w(f"| {mp} | {', '.join(sorted(lo)) or '—'} | {', '.join(sorted(up)) or '—'} |")
    w("")

    w("### Mirror-pair × Nuclear trigram overlap matrix\n")
    w("| Mirror pair | lower_nuc (L2,L3,L4) | upper_nuc (L3,L4,L5) |")
    w("|-------------|----------------------|----------------------|")
    for mp in ['O (outer)', 'M (middle)', 'I (inner)']:
        lo = cross['mp_nuc_matrix'].get((mp, 'lower_nuc'), set())
        up = cross['mp_nuc_matrix'].get((mp, 'upper_nuc'), set())
        w(f"| {mp} | {', '.join(sorted(lo)) or '—'} | {', '.join(sorted(up)) or '—'} |")
    w("")

    w("### Key structural observations\n")
    w("")
    w("The **inner pair I = {L3, L4}** is the unique mirror pair split across trigrams:")
    w("- L3 belongs to lower trigram; L4 belongs to upper trigram.")
    w("- Both L3 and L4 belong to BOTH nuclear trigrams.")
    w("- The outer pair O = {L1, L6} is fully split (L1 in lower only, L6 in upper only) with no nuclear overlap.")
    w("- The middle pair M = {L2, L5} is fully split across trigrams but each member belongs to exactly one nuclear trigram.")
    w("")
    w("Nuclear trigrams bridge the trigram boundary: lower_nuc = {L2, L3, **L4**} reaches into upper; upper_nuc = {**L3**, L4, L5} reaches into lower.")
    w("The L3|L4 membrane is the site where mirror-pair geometry and trigram geometry are maximally non-aligned,")
    w("and the nuclear trigrams are the structural elements that span this membrane.\n")

    # ── 6. Analytical observations ──
    w("## 6. Analytical Observations\n")

    w("### 6.1 Trigram-level structure of reversal pairs\n")
    w("For all 28 reversal pairs, the hexagram-level reversal (rev₆) decomposes as:")
    w("- **Swap** the upper and lower trigrams")
    w("- **Reverse** each trigram internally (rev₃)")
    w("")
    w("This means the cross-relationships (lower(a)↔upper(b), upper(a)↔lower(b)) are always either")
    w("**identity** (when the trigram is a palindrome under rev₃) or **reversal** (when it's not).")
    w("The direct relationships (lower(a)↔lower(b), upper(a)↔upper(b)) are generically unrelated")
    w("('other') because they compare trigrams that have been both swapped and reversed.\n")

    w("### 6.2 The 'other' category\n")
    w("20 of 28 reversal pairs show 'other' for direct trigram relationships. This is expected:")
    w("lower(b) = rev₃(upper(a)), which equals lower(a) only when upper(a) = rev₃(lower(a)) —")
    w("i.e., when the hexagram has the form T|rev₃(T). The 4 'complement' pairs among reversal pairs")
    w("are those where T and rev₃(T) happen to be complements (e.g., 000↔111). The 2 'reversal' pairs")
    w("are where the hexagram has the form T|T (both trigrams identical and self-palindromic under rev₃).")
    w("The 2 'comp∘rev' pairs arise when T|rev₃(T) yields comp∘rev₃ as the direct relationship.\n")

    w("### 6.3 Nuclear XOR mask structure\n")
    w("The nuclear XOR masks show a striking pattern:\n")
    w("- **Lower nuclear** uses masks: {000, 001, 110, 111}")
    w("- **Upper nuclear** uses masks: {000, 011, 100, 111}")
    w("- Only mask **111** and **000** are shared between lower and upper nuclear")
    w("")
    w("This is structurally determined. Nuclear trigrams are extracted by bit-shifting:")
    w("lower_nuc = bits[1:4], upper_nuc = bits[2:5]. Their XOR masks inherit structure from")
    w("the hexagram-level XOR mask. For reversal pairs, the hexagram mask is palindromic")
    w("(determined by mirror-pair signature). The nuclear XOR is a contiguous 3-bit window")
    w("of this 6-bit palindromic mask.\n")

    # Verify the nuclear XOR derivation from hex-level mask
    w("### 6.4 Nuclear XOR as window of hexagram mask\n")
    w("For each pair, the hexagram-level XOR mask m = a⊕b has 6 bits. The nuclear XOR masks are:\n")
    w("- lower_nuc XOR = m[1:4] (bits 1,2,3 of m)")
    w("- upper_nuc XOR = m[2:5] (bits 2,3,4 of m)\n")
    w("Since reversal pairs have palindromic masks (mᵢ = m₅₋ᵢ), the 7 possible masks")
    w("(from the signature group) map to specific nuclear XOR patterns:")
    w("")
    w("| Hex mask (6-bit) | Signature | lower_nuc XOR | upper_nuc XOR |")
    w("|-----------------|-----------|---------------|---------------|")
    # Compute for each of the 7 signature masks
    sig_masks = []
    for o in range(2):
        for m in range(2):
            for i in range(2):
                if o == 0 and m == 0 and i == 0:
                    continue
                # Build 6-bit palindromic mask from signature (o,m,i)
                mask = (o << 0) | (m << 1) | (i << 2) | (i << 3) | (m << 4) | (o << 5)
                sig = f"({o},{m},{i})"
                ln_xor = (mask >> 1) & 0b111
                un_xor = (mask >> 2) & 0b111
                sig_masks.append((mask, sig, ln_xor, un_xor))
                w(f"| {fmt6(mask)} | {sig} | {fmt3(ln_xor)} | {fmt3(un_xor)} |")
    w("")
    w("The nuclear XOR vocabulary is fully determined by the hexagram-level signature vocabulary.")
    w("Both nuclear layers use exactly 4 masks. The overlap is {000, 111} — exactly the masks")
    w("where the inner pair (I) contributes the same way to both nuclear windows.\n")

    w("### 6.5 Weight preservation at sub-hexagram levels\n")
    w("Hexagram-level weight is perfectly preserved for reversal pairs (Δw = 0), but this does NOT")
    w("propagate to sub-hexagram levels:\n")
    w("- **Trigram level:** mean |Δw| = 1.07 for reversal pairs. The swap+reverse operation")
    w("  redistributes weight between lower and upper trigrams. Weight is preserved globally")
    w("  but NOT locally.")
    w("- **Nuclear level:** mean |Δw| = 0.57 for reversal pairs — better than trigrams (0.57 < 1.07).")
    w("  The nuclear trigrams, which span the L3|L4 boundary, experience less weight disruption")
    w("  than the standard trigrams.")
    w("- **Implication:** Nuclear trigrams are more weight-stable under reversal than standard trigrams.")
    w("  This is because nuclear trigrams overlap at {L3, L4} — the inner pair — which contributes")
    w("  the same bits to both nuclear trigrams. The shared core dampens weight fluctuations.\n")

    w("### 6.6 Weight correlation hierarchy\n")
    w("The weight correlation between KW partners varies dramatically by decomposition level:\n")
    w("- Full hexagram: r = +0.52 (strong positive, driven by 28/32 reversal pairs with Δw=0)")
    w("- Lower nuclear: r = +0.28; Upper nuclear: r = +0.28 (moderate positive)")
    w("- Upper trigram: r = +0.13 (weak positive)")
    w("- Lower trigram: r = −0.08 (near zero / weak negative)\n")
    w("The nuclear level preserves more of the hexagram-level correlation than the trigram level.")
    w("This is consistent with nuclear trigrams spanning the inner pair boundary —")
    w("they see more of the global structure than either trigram alone.\n")

    return '\n'.join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    pairs = generate_kw_pairs()
    print(f"Generated {len(pairs)} KW pairs: {sum(1 for _,_,t in pairs if t=='reversal')} reversal, "
          f"{sum(1 for _,_,t in pairs if t=='palindromic')} palindromic\n")

    # Decompose all pairs
    decomps = [decompose_pair(a, b, t) for a, b, t in pairs]

    # Compute statistics
    stats = compute_statistics(decomps)

    # Cross-decomposition
    cross = cross_decomposition()

    # Print key results to stdout
    print("=" * 70)
    print("TRIGRAM RELATIONSHIP DISTRIBUTION (all 32 pairs)")
    print("=" * 70)
    for rel_type in ['lower_rel', 'upper_rel', 'cross_la_ub', 'cross_ua_lb']:
        print(f"\n  {rel_type}:")
        for rel, count in sorted(stats[f'all_{rel_type}'].items(), key=lambda x: -x[1]):
            print(f"    {rel}: {count}")

    print(f"\n  Swap+reverse verification (reversal pairs): all pass = {stats['swap_rev_all_pass']}")

    print("\n" + "=" * 70)
    print("NUCLEAR XOR MASK DISTRIBUTION (all 32 pairs)")
    print("=" * 70)
    print("\n  Lower nuclear XOR masks:")
    for mask, count in sorted(stats['all_lnuc_xor_dist'].items()):
        print(f"    {fmt3(mask)}: {count}")
    print("\n  Upper nuclear XOR masks:")
    for mask, count in sorted(stats['all_unuc_xor_dist'].items()):
        print(f"    {fmt3(mask)}: {count}")

    print("\n" + "=" * 70)
    print("WEIGHT CORRELATIONS WITHIN KW PAIRS")
    print("=" * 70)
    print(f"  Full hexagram:  r = {stats['hex_weight_corr']:.4f}")
    print(f"  Lower trigram:  r = {stats['lower_trig_weight_corr']:.4f}")
    print(f"  Upper trigram:  r = {stats['upper_trig_weight_corr']:.4f}")
    print(f"  Lower nuclear:  r = {stats['lnuc_weight_corr']:.4f}")
    print(f"  Upper nuclear:  r = {stats['unuc_weight_corr']:.4f}")

    print("\n" + "=" * 70)
    print("MEAN |Δw| BY LEVEL")
    print("=" * 70)
    print(f"  {'Level':<20} {'All pairs':>10} {'Reversal':>10}")
    print(f"  {'Lower trigram':<20} {stats['mean_dw_lower']:>10.4f} {stats.get('rev_mean_dw_lower', float('nan')):>10.4f}")
    print(f"  {'Upper trigram':<20} {stats['mean_dw_upper']:>10.4f} {stats.get('rev_mean_dw_upper', float('nan')):>10.4f}")
    print(f"  {'Lower nuclear':<20} {stats['mean_dw_lnuc']:>10.4f} {stats.get('rev_mean_dw_lnuc', float('nan')):>10.4f}")
    print(f"  {'Upper nuclear':<20} {stats['mean_dw_unuc']:>10.4f} {stats.get('rev_mean_dw_unuc', float('nan')):>10.4f}")

    print("\n" + "=" * 70)
    print("CROSS-DECOMPOSITION: MIRROR-PAIR × TRIGRAM")
    print("=" * 70)
    for mp in ['O (outer)', 'M (middle)', 'I (inner)']:
        lo = cross['mp_trig_matrix'].get((mp, 'lower'), set())
        up = cross['mp_trig_matrix'].get((mp, 'upper'), set())
        print(f"  {mp}: lower={sorted(lo)}, upper={sorted(up)}")

    print("\nCROSS-DECOMPOSITION: MIRROR-PAIR × NUCLEAR")
    for mp in ['O (outer)', 'M (middle)', 'I (inner)']:
        lo = cross['mp_nuc_matrix'].get((mp, 'lower_nuc'), set())
        up = cross['mp_nuc_matrix'].get((mp, 'upper_nuc'), set())
        print(f"  {mp}: lower_nuc={sorted(lo)}, upper_nuc={sorted(up)}")

    # Write markdown results
    md = format_results(pairs, decomps, stats, cross)
    out_path = Path(__file__).parent / "trigram_decomposition_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == '__main__':
    main()
