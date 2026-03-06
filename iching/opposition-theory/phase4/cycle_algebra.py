#!/usr/bin/env python3
"""
Phase 4, Round 2: Sequential and Algebraic Structure

A. Directed cycle profiles — per-edge Hamming sequences, asymmetry statistic
B. XOR mask algebra — subgroup structure of masks along 生/克 edges
C. Partner agreement null model — rate across 50,400 surjections
D. Shell-only pairs under 生克 — signature (1,0,0) vs depth-penetrating
E. 变卦 opposition map — 本卦→互卦→变卦 evaluation circuit

Encoding: L1 = bit 0 (bottom), L6 = bit 5 (top).
"""

from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_HEX = 1 << N
MASK_ALL = (1 << N) - 1
NUM_TRIG = 8
MASK3 = 0b111

TRIGRAM_NAMES = {  # keyed by value where bit0=bottom line, bit2=top line
    0b000: "Kun ☷", 0b001: "Zhen ☳", 0b010: "Kan ☵", 0b011: "Dui ☱",
    0b100: "Gen ☶", 0b101: "Li ☲",   0b110: "Xun ☴", 0b111: "Qian ☰",
}

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEMENT_ZH = {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}

TRIGRAM_ELEMENT = {  # keyed by value where bit0=bottom line, bit2=top line
    0b111: "Metal", 0b011: "Metal",   # Qian ☰, Dui ☱
    0b101: "Fire",                     # Li ☲
    0b001: "Wood",  0b110: "Wood",     # Zhen ☳, Xun ☴
    0b010: "Water",                    # Kan ☵
    0b100: "Earth", 0b000: "Earth",    # Gen ☶, Kun ☷
}

SHENG_CYCLE = ["Wood", "Fire", "Earth", "Metal", "Water"]
SHENG_EDGES = [(SHENG_CYCLE[i], SHENG_CYCLE[(i + 1) % 5]) for i in range(5)]
KE_CYCLE = ["Wood", "Earth", "Water", "Fire", "Metal"]
KE_EDGES = [(KE_CYCLE[i], KE_CYCLE[(i + 1) % 5]) for i in range(5)]

SHENG_MAP = {src: tgt for src, tgt in SHENG_EDGES}
KE_MAP = {src: tgt for src, tgt in KE_EDGES}

# Element → trigrams (precomputed)
ELEM_TRIGRAMS = {}
for _t, _e in TRIGRAM_ELEMENT.items():
    ELEM_TRIGRAMS.setdefault(_e, []).append(_t)
for _e in ELEM_TRIGRAMS:
    ELEM_TRIGRAMS[_e].sort()

# ─── Bit operations ──────────────────────────────────────────────────────────

def popcount(x):
    return bin(x).count('1')

def reverse6(x):
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    return r

def fmt6(x): return format(x, '06b')
def fmt3(x): return format(x, '03b')
def bit(x, i): return (x >> i) & 1

def lower_trigram(x): return x & MASK3
def upper_trigram(x): return (x >> 3) & MASK3

def hamming3(a, b): return popcount(a ^ b)
def hamming6(a, b): return popcount(a ^ b)

# ─── KW pairing ─────────────────────────────────────────────────────────────

def kw_partner(x):
    rev = reverse6(x)
    return x ^ MASK_ALL if rev == x else rev

def is_palindrome6(x):
    return reverse6(x) == x

def generate_kw_pairs():
    paired = set()
    pairs = []
    for a in range(NUM_HEX):
        if a in paired:
            continue
        b = kw_partner(a)
        ptype = "palindromic" if is_palindrome6(a) else "reversal"
        if a > b: a, b = b, a
        pairs.append((a, b, ptype))
        paired.add(a); paired.add(b)
    return pairs

def hex_kw_signature(x):
    b = kw_partner(x)
    xor = x ^ b
    return xor, (bit(xor, 0), bit(xor, 1), bit(xor, 2))

# ─── 互卦 ───────────────────────────────────────────────────────────────────

def hugua(x):
    """互卦: lower_nuc = (L2,L3,L4), upper_nuc = (L3,L4,L5)."""
    L2, L3, L4, L5 = bit(x, 1), bit(x, 2), bit(x, 3), bit(x, 4)
    return L2 | (L3 << 1) | (L4 << 2) | (L3 << 3) | (L4 << 4) | (L5 << 5)

# ─── Five-phase relationship ────────────────────────────────────────────────

def five_phase_relation(ti_elem, yong_elem):
    if ti_elem == yong_elem: return "比和"
    if SHENG_MAP[yong_elem] == ti_elem: return "生体"
    if KE_MAP[yong_elem] == ti_elem: return "克体"
    if SHENG_MAP[ti_elem] == yong_elem: return "体生用"
    if KE_MAP[ti_elem] == yong_elem: return "体克用"
    raise ValueError(f"No relation: {ti_elem} vs {yong_elem}")

def tiyong_relation(hex_val, line):
    """Compute 体/用 five-phase relation for a hexagram and moving line (1-indexed)."""
    lo, up = lower_trigram(hex_val), upper_trigram(hex_val)
    if line <= 3:
        ti, yong = up, lo  # moving in lower → lower=用, upper=体
    else:
        ti, yong = lo, up  # moving in upper → upper=用, lower=体
    return five_phase_relation(TRIGRAM_ELEMENT[ti], TRIGRAM_ELEMENT[yong])

def tiyong_trigrams(hex_val, line):
    """Return (ti_trig, yong_trig) for a hexagram and moving line."""
    lo, up = lower_trigram(hex_val), upper_trigram(hex_val)
    if line <= 3:
        return up, lo
    else:
        return lo, up

# ─── Hexagram relationship classification ───────────────────────────────────

def classify_hex_relation(x, y):
    if x == y: return "identity"
    if y == reverse6(x): return "reversal"
    if y == x ^ MASK_ALL: return "complement"
    if y == reverse6(x ^ MASK_ALL): return "comp∘rev"
    return "other"

# ─── Enumeration (from Round 1) ─────────────────────────────────────────────

def enumerate_assignments():
    trigrams = list(range(NUM_TRIG))
    assignments = []
    for pair_elems in combinations(range(5), 3):
        single_elems = [i for i in range(5) if i not in pair_elems]
        for t0 in combinations(trigrams, 2):
            remaining1 = [t for t in trigrams if t not in t0]
            for t1 in combinations(remaining1, 2):
                remaining2 = [t for t in remaining1 if t not in t1]
                for t2 in combinations(remaining2, 2):
                    remaining3 = [t for t in remaining2 if t not in t2]
                    for perm in permutations(remaining3):
                        mapping = {}
                        for t in t0: mapping[t] = pair_elems[0]
                        for t in t1: mapping[t] = pair_elems[1]
                        for t in t2: mapping[t] = pair_elems[2]
                        for idx, t in enumerate(perm): mapping[t] = single_elems[idx]
                        assignments.append(mapping)
    return assignments

SHENG_EDGES_IDX = [(i, (i + 1) % 5) for i in range(5)]
KE_EDGES_IDX = [(0, 2), (2, 4), (4, 1), (1, 3), (3, 0)]

# ═══════════════════════════════════════════════════════════════════════════
# A. Directed Cycle Profiles
# ═══════════════════════════════════════════════════════════════════════════

def edge_detail(src_elem, tgt_elem):
    """All trigram pairs and their Hamming/XOR for one directed edge."""
    pairs = []
    for ts in ELEM_TRIGRAMS[src_elem]:
        for tt in ELEM_TRIGRAMS[tgt_elem]:
            pairs.append({
                'src': ts, 'tgt': tt,
                'xor': ts ^ tt, 'hamming': hamming3(ts, tt),
            })
    return pairs

def cycle_profile(edges):
    """Per-edge statistics for a full cycle."""
    profile = []
    for src, tgt in edges:
        detail = edge_detail(src, tgt)
        hammings = [d['hamming'] for d in detail]
        profile.append({
            'src': src, 'tgt': tgt,
            'pairs': detail,
            'mean_h': np.mean(hammings),
            'var_h': np.var(hammings),
            'n': len(detail),
        })
    return profile

def score_assignment_extended(mapping):
    """Extended scoring: mean Hamming, per-edge variance, asymmetry."""
    elem_trigs = {}
    for t, e in mapping.items():
        elem_trigs.setdefault(e, []).append(t)

    def cycle_stats(edges):
        edge_means = []
        total_h, total_n = 0, 0
        for src_e, tgt_e in edges:
            src_trigs = elem_trigs.get(src_e, [])
            tgt_trigs = elem_trigs.get(tgt_e, [])
            edge_h = []
            for ts in src_trigs:
                for tt in tgt_trigs:
                    h = hamming3(ts, tt)
                    edge_h.append(h)
                    total_h += h
                    total_n += 1
            edge_means.append(np.mean(edge_h) if edge_h else 0)
        mean_h = total_h / total_n if total_n > 0 else 0
        var_of_means = float(np.var(edge_means))
        return mean_h, var_of_means

    sh, sv = cycle_stats(SHENG_EDGES_IDX)
    kh, kv = cycle_stats(KE_EDGES_IDX)

    return sh, kh, sh - kh, sv, kv

def compute_partner_agreement(mapping):
    """Fraction of (KW_pair, line) states where both partners get same five-phase relation."""
    elem_map = {}
    for t, e_idx in mapping.items():
        elem_map[t] = ELEMENTS[e_idx]

    pairs = generate_kw_pairs()
    agree = 0
    total = 0
    for a, b, _ in pairs:
        for line in range(1, 7):
            ti_a, yong_a = tiyong_trigrams(a, line)
            ti_b, yong_b = tiyong_trigrams(b, line)
            rel_a = five_phase_relation(elem_map[ti_a], elem_map[yong_a])
            rel_b = five_phase_relation(elem_map[ti_b], elem_map[yong_b])
            if rel_a == rel_b:
                agree += 1
            total += 1
    return agree / total if total > 0 else 0

# ═══════════════════════════════════════════════════════════════════════════
# B. XOR Mask Algebra
# ═══════════════════════════════════════════════════════════════════════════

def collect_masks(edges):
    """Collect all XOR masks from trigram pairs along cycle edges."""
    masks = set()
    for src, tgt in edges:
        for ts in ELEM_TRIGRAMS[src]:
            for tt in ELEM_TRIGRAMS[tgt]:
                masks.add(ts ^ tt)
    return masks

def xor_closure(mask_set):
    """Compute XOR-closure of a set of 3-bit values."""
    closed = set(mask_set)
    changed = True
    while changed:
        changed = False
        new = set()
        for a in closed:
            for b in closed:
                c = a ^ b
                if c not in closed:
                    new.add(c)
                    changed = True
        closed |= new
    return closed

# ═══════════════════════════════════════════════════════════════════════════
# D. Shell-Only Pairs
# ═══════════════════════════════════════════════════════════════════════════

def identify_shell_only_pairs():
    """Find KW pairs with signature (1,0,0) — opposition only in outer shell."""
    pairs = generate_kw_pairs()
    shell_only = []
    depth_penetrating = []
    for a, b, ptype in pairs:
        _, sig = hex_kw_signature(a)
        if sig == (1, 0, 0):
            shell_only.append((a, b, ptype))
        else:
            depth_penetrating.append((a, b, ptype))
    return shell_only, depth_penetrating

def pair_agreement_rate(pair_list):
    """For a list of KW pairs, compute agreement rate across all (pair, line) states."""
    agree = 0
    total = 0
    for a, b, _ in pair_list:
        for line in range(1, 7):
            rel_a = tiyong_relation(a, line)
            rel_b = tiyong_relation(b, line)
            if rel_a == rel_b:
                agree += 1
            total += 1
    return agree, total

# ═══════════════════════════════════════════════════════════════════════════
# E. 变卦 Opposition Map
# ═══════════════════════════════════════════════════════════════════════════

def biangua(hex_val, line):
    """Compute 变卦: flip the moving line (1-indexed)."""
    return hex_val ^ (1 << (line - 1))

def hugua_tiyong_relation(hex_val, line):
    """
    Compute 体/用 relation for the 互卦 of hex_val with given moving line.
    
    The 互卦's lower trigram = lower_nuclear(hex_val), upper = upper_nuclear(hex_val).
    The 体 position is inherited from 本卦: if moving line is in lower (1-3),
    then 体 = upper position → 互卦's upper (upper_nuclear).
    If moving line is in upper (4-6), 体 = lower position → 互卦's lower (lower_nuclear).
    """
    hg = hugua(hex_val)
    lo_nuc = lower_trigram(hg)  # = lower_nuclear of hex_val
    up_nuc = upper_trigram(hg)  # = upper_nuclear of hex_val
    if line <= 3:
        ti, yong = up_nuc, lo_nuc  # 体 = upper position
    else:
        ti, yong = lo_nuc, up_nuc  # 体 = lower position
    return five_phase_relation(TRIGRAM_ELEMENT[ti], TRIGRAM_ELEMENT[yong])

def compute_biangua_states():
    """Compute 本卦→互卦→变卦 evaluation circuit for all 384 states."""
    states = []
    for h in range(NUM_HEX):
        for line in range(1, 7):
            bg = biangua(h, line)
            hg_h = hugua(h)

            # 本卦 relation
            rel_ben = tiyong_relation(h, line)

            # 互卦 relation (体 position inherited from 本卦)
            rel_hu = hugua_tiyong_relation(h, line)

            # 变卦 relation (same moving line position, but in the changed hexagram)
            rel_bian = tiyong_relation(bg, line)

            # Opposition between 本卦 and 变卦
            hex_rel = classify_hex_relation(h, bg)
            hex_hamming = hamming6(h, bg)

            # Opposition between 互卦(本卦) and 互卦(变卦)
            hg_bg = hugua(bg)
            hugua_rel = classify_hex_relation(hg_h, hg_bg)
            hugua_hamming = hamming6(hg_h, hg_bg)

            # Repetition pattern
            triple = (rel_ben, rel_hu, rel_bian)
            n_unique = len(set(triple))

            states.append({
                'hex': h, 'line': line, 'biangua': bg,
                'hugua_ben': hg_h, 'hugua_bian': hg_bg,
                'rel_ben': rel_ben, 'rel_hu': rel_hu, 'rel_bian': rel_bian,
                'hex_rel': hex_rel, 'hex_hamming': hex_hamming,
                'hugua_rel': hugua_rel, 'hugua_hamming': hugua_hamming,
                'triple': triple, 'n_unique': n_unique,
            })
    return states


# ═══════════════════════════════════════════════════════════════════════════
# Markdown Formatting
# ═══════════════════════════════════════════════════════════════════════════

def format_markdown(sheng_profile, ke_profile, masks_data,
                    asymmetry_data, shell_data, biangua_data):
    lines = []
    w = lines.append

    w("# Phase 4 Round 2: Sequential and Algebraic Structure\n")

    # ── A. Directed Cycle Profiles ──
    w("## A. Directed Cycle Profiles\n")

    for label, cycle_name, profile in [
        ("生 (generation)", "生", sheng_profile),
        ("克 (overcoming)", "克", ke_profile),
    ]:
        w(f"### {label} cycle — per-edge detail\n")
        for edge in profile:
            w(f"**{edge['src']} → {edge['tgt']}** (n={edge['n']} pairs, "
              f"mean d={edge['mean_h']:.2f})\n")
            w("| Source | Target | XOR | Hamming |")
            w("|--------|--------|-----|---------|")
            for p in edge['pairs']:
                w(f"| {TRIGRAM_NAMES[p['src']]} ({fmt3(p['src'])}) "
                  f"| {TRIGRAM_NAMES[p['tgt']]} ({fmt3(p['tgt'])}) "
                  f"| {fmt3(p['xor'])} | {p['hamming']} |")
            w("")

        edge_means = [e['mean_h'] for e in profile]
        overall = sum(e['mean_h'] * e['n'] for e in profile) / sum(e['n'] for e in profile)
        var_means = float(np.var(edge_means))
        w(f"**{cycle_name} overall:** mean d = {overall:.4f}, "
          f"variance of edge means = {var_means:.4f}")
        w(f"**Edge means:** {[f'{m:.2f}' for m in edge_means]}\n")

    # Asymmetry
    w("### Asymmetry statistic (生 − 克 mean Hamming)\n")
    trad_asym = asymmetry_data['trad_asymmetry']
    w(f"**Traditional value:** {trad_asym:.4f}\n")

    all_asym = asymmetry_data['all_asymmetry']
    a = np.array(all_asym)
    w(f"**Distribution (n={len(all_asym)}):** "
      f"min={a.min():.4f}, max={a.max():.4f}, "
      f"mean={a.mean():.4f}, std={a.std():.4f}")
    pct = 100.0 * np.sum(a <= trad_asym) / len(a)
    w(f"**Traditional percentile:** {pct:.1f}%\n")

    # Histogram
    w("```")
    bins = np.linspace(a.min() - 0.01, a.max() + 0.01, 21)
    hist, edges_h = np.histogram(a, bins=bins)
    max_bar = max(hist) if max(hist) > 0 else 1
    for i in range(len(hist)):
        lo, hi = edges_h[i], edges_h[i + 1]
        bar_len = int(50 * hist[i] / max_bar)
        marker = " ◄ TRAD" if lo <= trad_asym < hi else ""
        w(f"  {lo:+6.3f} to {hi:+6.3f} | {'█' * bar_len} {hist[i]}{marker}")
    w("```\n")

    # Variance distributions
    w("### Per-edge variance of Hamming distances\n")
    trad_sv = asymmetry_data['trad_sheng_var']
    trad_kv = asymmetry_data['trad_ke_var']
    all_sv = np.array(asymmetry_data['all_sheng_var'])
    all_kv = np.array(asymmetry_data['all_ke_var'])
    sv_pct = 100.0 * np.sum(all_sv <= trad_sv) / len(all_sv)
    kv_pct = 100.0 * np.sum(all_kv <= trad_kv) / len(all_kv)

    w(f"| Metric | Traditional | Mean | Std | Percentile |")
    w(f"|--------|-------------|------|-----|------------|")
    w(f"| 生 edge-mean variance | {trad_sv:.4f} | {all_sv.mean():.4f} | {all_sv.std():.4f} | {sv_pct:.1f}% |")
    w(f"| 克 edge-mean variance | {trad_kv:.4f} | {all_kv.mean():.4f} | {all_kv.std():.4f} | {kv_pct:.1f}% |")
    w("")

    # ── B. XOR Mask Algebra ──
    w("## B. XOR Mask Algebra\n")

    for label, mdata in [("生", masks_data['sheng']), ("克", masks_data['ke'])]:
        w(f"### {label} cycle masks\n")
        w(f"**Masks:** {{{', '.join(fmt3(m) for m in sorted(mdata['masks']))}}}")
        w(f"**Count:** {len(mdata['masks'])} of 7 nonzero masks")
        w(f"**XOR-closure:** {{{', '.join(fmt3(m) for m in sorted(mdata['closure']))}}}")
        w(f"**Closure size:** {len(mdata['closure'])} (= {'Z₂³' if len(mdata['closure']) == 8 else 'subgroup'})")
        is_group = mdata['closure'] == set(range(8))
        w(f"**Generates full Z₂³?** {is_group}\n")

    # Overlap analysis
    sm = masks_data['sheng']['masks']
    km = masks_data['ke']['masks']
    both = sm & km
    only_sheng = sm - km
    only_ke = km - sm
    neither = set(range(1, 8)) - sm - km

    w("### Mask overlap\n")
    w(f"| Category | Masks | Count |")
    w(f"|----------|-------|-------|")
    w(f"| 生 only | {{{', '.join(fmt3(m) for m in sorted(only_sheng))}}} | {len(only_sheng)} |")
    w(f"| 克 only | {{{', '.join(fmt3(m) for m in sorted(only_ke))}}} | {len(only_ke)} |")
    w(f"| Both | {{{', '.join(fmt3(m) for m in sorted(both))}}} | {len(both)} |")
    w(f"| Neither | {{{', '.join(fmt3(m) for m in sorted(neither))}}} | {len(neither)} |")
    w("")

    # KW n=3 vocabulary comparison
    # Later Heaven diameters use complement (111) as the pairing operation
    # But n=3 KW masks from cross_scale.py: the complement pairing uses mask 111 for all pairs
    kw_masks = {0b111}  # n=3 complement pairing uses only mask 111
    w("### Comparison with n=3 KW vocabulary\n")
    w("The n=3 KW pairing (complement) uses a single mask: {111}.")
    w(f"- 生 edges include mask 111: **{0b111 in sm}**")
    w(f"- 克 edges include mask 111: **{0b111 in km}**\n")

    w("The n=3 KW-style pairing (reversal for the size-4 orbit) would use masks {001, 110}.")
    kw_style = {0b001, 0b110}
    w(f"- 生 ∩ KW-style: {{{', '.join(fmt3(m) for m in sorted(sm & kw_style))}}}")
    w(f"- 克 ∩ KW-style: {{{', '.join(fmt3(m) for m in sorted(km & kw_style))}}}\n")

    # ── C. Partner Agreement Null Model ──
    w("## C. Partner Agreement Null Model\n")

    pa_data = asymmetry_data['partner_agreement']
    trad_pa = pa_data['trad_rate']
    all_pa = np.array(pa_data['all_rates'])
    pa_pct = 100.0 * np.sum(all_pa <= trad_pa) / len(all_pa)

    w(f"**Traditional agreement rate:** {trad_pa:.4f} (= {int(trad_pa * 192)}/192)")
    w(f"**Distribution:** min={all_pa.min():.4f}, max={all_pa.max():.4f}, "
      f"mean={all_pa.mean():.4f}, std={all_pa.std():.4f}")
    w(f"**Traditional percentile:** {pa_pct:.1f}%\n")

    w("```")
    bins = np.linspace(all_pa.min() - 0.005, all_pa.max() + 0.005, 21)
    hist, edges_h = np.histogram(all_pa, bins=bins)
    max_bar = max(hist) if max(hist) > 0 else 1
    for i in range(len(hist)):
        lo, hi = edges_h[i], edges_h[i + 1]
        bar_len = int(50 * hist[i] / max_bar)
        marker = " ◄ TRAD" if lo <= trad_pa < hi else ""
        w(f"  {lo:.3f}-{hi:.3f} | {'█' * bar_len} {hist[i]}{marker}")
    w("```\n")

    # ── D. Shell-Only Pairs ──
    w("## D. Shell-Only Pairs Under 生克\n")

    sd = shell_data
    w("### Shell-only pairs (signature (1,0,0))\n")
    w("These 4 KW pairs differ only at L1 and L6 — identical nuclear cores.\n")

    for a, b, ptype in sd['shell_pairs']:
        w(f"**{fmt6(a)} ↔ {fmt6(b)}**\n")
        w("| Line | 体(a) | 用(a) | rel(a) | 体(b) | 用(b) | rel(b) | Agree? |")
        w("|------|-------|-------|--------|-------|-------|--------|--------|")
        for line in range(1, 7):
            ti_a, yo_a = tiyong_trigrams(a, line)
            ti_b, yo_b = tiyong_trigrams(b, line)
            rel_a = tiyong_relation(a, line)
            rel_b = tiyong_relation(b, line)
            w(f"| {line} | {fmt3(ti_a)} | {fmt3(yo_a)} | {rel_a} "
              f"| {fmt3(ti_b)} | {fmt3(yo_b)} | {rel_b} "
              f"| {'✓' if rel_a == rel_b else '✗'} |")
        w("")

    w("### Agreement rate comparison\n")
    sa, st = sd['shell_agree'], sd['shell_total']
    da, dt = sd['depth_agree'], sd['depth_total']
    w("| Category | Agree | Total | Rate |")
    w("|----------|-------|-------|------|")
    w(f"| Shell-only (4 pairs) | {sa} | {st} | {sa/st:.4f} |")
    w(f"| Depth-penetrating (28 pairs) | {da} | {dt} | {da/dt:.4f} |")
    w(f"| All (32 pairs) | {sa+da} | {st+dt} | {(sa+da)/(st+dt):.4f} |")
    w("")

    ratio = (sa/st) / (da/dt) if da > 0 else float('inf')
    w(f"**Shell-only / Depth ratio:** {ratio:.2f}×")
    if ratio > 1.5:
        w("Shell-only pairs show **substantially more agreement** — as expected,")
        w("since their trigrams are nearly identical (only L1/L6 differ).\n")
    elif ratio > 1.1:
        w("Shell-only pairs show **moderately more agreement**.\n")
    else:
        w("Shell-only pairs show **similar agreement** to depth-penetrating pairs.\n")

    # ── E. 变卦 Opposition Map ──
    w("## E. 变卦 Opposition Map\n")

    bd = biangua_data

    w("### 本卦 → 变卦 opposition type\n")
    w("Flipping one line always gives Hamming distance 1 at the hexagram level.\n")
    hex_rel_dist = bd['hex_rel_dist']
    w("| Hex-level relation | Count | Fraction |")
    w("|-------------------|-------|----------|")
    for rel, cnt in sorted(hex_rel_dist.items(), key=lambda x: -x[1]):
        w(f"| {rel} | {cnt} | {cnt/384:.4f} |")
    w("")

    w("### 互卦(本) vs 互卦(变) opposition type\n")
    w("How does flipping one line propagate through the 互卦 map?\n")
    hugua_rel_dist = bd['hugua_rel_dist']
    w("| 互卦-level relation | Count | Fraction |")
    w("|-------------------|-------|----------|")
    for rel, cnt in sorted(hugua_rel_dist.items(), key=lambda x: -x[1]):
        w(f"| {rel} | {cnt} | {cnt/384:.4f} |")
    w("")

    hugua_h_dist = bd['hugua_hamming_dist']
    w("| 互卦 Hamming | Count | Fraction |")
    w("|-------------|-------|----------|")
    for h, cnt in sorted(hugua_h_dist.items()):
        w(f"| {h} | {cnt} | {cnt/384:.4f} |")
    w("")

    w("### Line position → 互卦 Hamming\n")
    w("Which moving lines are visible to the 互卦 map?\n")
    line_hugua_h = bd['line_hugua_hamming']
    w("| Moving line | 互卦 Hamming | Visible? |")
    w("|------------|-------------|----------|")
    for line in range(1, 7):
        h_vals = line_hugua_h[line]
        # All should be same value for a given line position
        unique = set(h_vals)
        if len(unique) == 1:
            hval = unique.pop()
            w(f"| L{line} (bit {line-1}) | {hval} | {'yes' if hval > 0 else 'no (erased)'} |")
        else:
            w(f"| L{line} (bit {line-1}) | varies: {sorted(unique)} | partial |")
    w("")

    w("### 本卦→互卦→变卦 evaluation circuit\n")
    w("For each (hexagram, moving_line) state, the triple of five-phase relations:\n")
    w("1. **本卦:** 体/用 relation of the original hexagram")
    w("2. **互卦:** 体/用 relation using nuclear trigrams (体 position inherited)")
    w("3. **变卦:** 体/用 relation of the changed hexagram\n")

    # Repetition pattern
    n_unique_dist = bd['n_unique_dist']
    w("### Repetition pattern\n")
    w("| # unique relations | Count | Fraction |")
    w("|-------------------|-------|----------|")
    for nu in sorted(n_unique_dist):
        w(f"| {nu} (={'all same' if nu == 1 else 'all different' if nu == 3 else 'one repeat'}) "
          f"| {n_unique_dist[nu]} | {n_unique_dist[nu]/384:.4f} |")
    w("")

    # Triple distribution (top patterns)
    triple_dist = bd['triple_dist']
    w("### Most common triples (top 20)\n")
    w("| 本卦 | 互卦 | 变卦 | Count |")
    w("|------|------|------|-------|")
    for triple, cnt in sorted(triple_dist.items(), key=lambda x: -x[1])[:20]:
        w(f"| {triple[0]} | {triple[1]} | {triple[2]} | {cnt} |")
    w("")

    # Anti-repetition analysis
    all_same = n_unique_dist.get(1, 0)
    all_diff = n_unique_dist.get(3, 0)
    w("### Anti-repetition summary\n")
    w(f"- **All three same:** {all_same}/384 = {all_same/384:.4f}")
    w(f"- **All three different:** {all_diff}/384 = {all_diff/384:.4f}")
    w(f"- **One repeated:** {384 - all_same - all_diff}/384 = {(384 - all_same - all_diff)/384:.4f}\n")

    # Transition analysis: how often does relation change at each step?
    ben_to_hu = sum(1 for s in bd['states'] if s['rel_ben'] != s['rel_hu'])
    hu_to_bian = sum(1 for s in bd['states'] if s['rel_hu'] != s['rel_bian'])
    ben_to_bian = sum(1 for s in bd['states'] if s['rel_ben'] != s['rel_bian'])
    w("### Step-by-step transition rates\n")
    w(f"| Transition | Changes | Rate |")
    w(f"|------------|---------|------|")
    w(f"| 本卦 → 互卦 | {ben_to_hu}/384 | {ben_to_hu/384:.4f} |")
    w(f"| 互卦 → 变卦 | {hu_to_bian}/384 | {hu_to_bian/384:.4f} |")
    w(f"| 本卦 → 变卦 | {ben_to_bian}/384 | {ben_to_bian/384:.4f} |")
    w("")

    # ── Structural Analysis ──
    w("## Structural Analysis\n")

    w("### Key finding 1: Asymmetry is moderately unusual\n")
    w(f"The traditional 生−克 asymmetry ({trad_asym:.4f}) sits at percentile {pct:.1f}%.")
    w(f"生 connects more distant trigrams than 克. Among 50,400 random assignments,")
    if pct > 75 or pct < 25:
        w(f"this is a **moderate outlier** — the directional difference is not random.\n")
    else:
        w(f"this is **average** — no strong evidence the traditional mapping was chosen for this.\n")

    w("### Key finding 2: XOR masks span nearly all of Z₂³\n")
    w(f"生 uses {len(sm)} masks, 克 uses {len(km)} masks.")
    w(f"Together they cover {len(sm | km)} of 7 nonzero masks.")
    if len(masks_data['sheng']['closure']) == 8:
        w("生's masks alone generate the full group Z₂³ under XOR.\n")
    if len(masks_data['ke']['closure']) == 8:
        w("克's masks alone generate the full group Z₂³ under XOR.\n")

    w("### Key finding 3: Shell-only pairs and agreement\n")
    w(f"Shell-only agreement: {sa/st:.4f}, depth-penetrating: {da/dt:.4f}.")
    if sa/st > da/dt:
        w("Shell-only pairs are more stable under 生克 evaluation — changing only L1/L6")
        w("often preserves the 体/用 five-phase relationship.\n")

    w("### Key finding 4: 互卦 erases L1/L6 flips\n")
    l1_h = set(line_hugua_h[1])
    l6_h = set(line_hugua_h[6])
    if l1_h == {0} and l6_h == {0}:
        w("Flipping L1 or L6 produces **zero** change in the 互卦 —")
        w("the nuclear map is completely blind to outer-shell perturbations.")
        w("This directly connects to the shell-only pair stability above.\n")

    w("### Key finding 5: Evaluation circuit diversity\n")
    w(f"All-same: {all_same/384:.1%}, all-different: {all_diff/384:.1%}, one-repeat: {(384-all_same-all_diff)/384:.1%}.")
    w("The 本→互→变 circuit produces **substantial diversity** in five-phase evaluations —")
    w("the three viewpoints usually disagree, providing non-redundant information.\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASE 4 ROUND 2: SEQUENTIAL AND ALGEBRAIC STRUCTURE")
    print("=" * 70)

    # ── A. Directed Cycle Profiles ──
    print("\n── A. Directed Cycle Profiles ──")
    sheng_profile = cycle_profile(SHENG_EDGES)
    ke_profile = cycle_profile(KE_EDGES)

    sheng_overall = sum(e['mean_h'] * e['n'] for e in sheng_profile) / sum(e['n'] for e in sheng_profile)
    ke_overall = sum(e['mean_h'] * e['n'] for e in ke_profile) / sum(e['n'] for e in ke_profile)
    print(f"  生 overall mean d: {sheng_overall:.4f}")
    print(f"  克 overall mean d: {ke_overall:.4f}")
    print(f"  Asymmetry (生−克): {sheng_overall - ke_overall:.4f}")

    print(f"\n  生 edge means: {[f'{e['mean_h']:.2f}' for e in sheng_profile]}")
    print(f"  克 edge means: {[f'{e['mean_h']:.2f}' for e in ke_profile]}")

    # Enumerate surjections and score
    print("\n  Enumerating 50,400 surjections...")
    assignments = enumerate_assignments()
    print(f"  Total: {len(assignments)}")

    print("  Scoring all assignments (extended)...")
    all_sh, all_kh, all_asym, all_sv, all_kv = [], [], [], [], []
    for m in assignments:
        sh, kh, asym, sv, kv = score_assignment_extended(m)
        all_sh.append(sh)
        all_kh.append(kh)
        all_asym.append(asym)
        all_sv.append(sv)
        all_kv.append(kv)

    trad_asym = sheng_overall - ke_overall
    a_asym = np.array(all_asym)
    pct = 100.0 * np.sum(a_asym <= trad_asym) / len(a_asym)
    print(f"\n  Asymmetry distribution: min={a_asym.min():.4f}, max={a_asym.max():.4f}, "
          f"mean={a_asym.mean():.4f}")
    print(f"  Traditional percentile: {pct:.1f}%")

    trad_sv = float(np.var([e['mean_h'] for e in sheng_profile]))
    trad_kv = float(np.var([e['mean_h'] for e in ke_profile]))
    print(f"\n  生 edge-mean variance: {trad_sv:.4f} (pct: "
          f"{100*np.sum(np.array(all_sv) <= trad_sv)/len(all_sv):.1f}%)")
    print(f"  克 edge-mean variance: {trad_kv:.4f} (pct: "
          f"{100*np.sum(np.array(all_kv) <= trad_kv)/len(all_kv):.1f}%)")

    # ── B. XOR Mask Algebra ──
    print("\n── B. XOR Mask Algebra ──")
    sheng_masks = collect_masks(SHENG_EDGES)
    ke_masks = collect_masks(KE_EDGES)
    sheng_closure = xor_closure(sheng_masks)
    ke_closure = xor_closure(ke_masks)

    print(f"  生 masks: {{{', '.join(fmt3(m) for m in sorted(sheng_masks))}}}")
    print(f"  克 masks: {{{', '.join(fmt3(m) for m in sorted(ke_masks))}}}")
    print(f"  生 closure size: {len(sheng_closure)} {'(= Z₂³)' if len(sheng_closure) == 8 else ''}")
    print(f"  克 closure size: {len(ke_closure)} {'(= Z₂³)' if len(ke_closure) == 8 else ''}")
    print(f"  生 ∩ 克: {{{', '.join(fmt3(m) for m in sorted(sheng_masks & ke_masks))}}}")
    print(f"  Missing: {{{', '.join(fmt3(m) for m in sorted(set(range(1,8)) - sheng_masks - ke_masks))}}}")

    masks_data = {
        'sheng': {'masks': sheng_masks, 'closure': sheng_closure},
        'ke': {'masks': ke_masks, 'closure': ke_closure},
    }

    # ── C. Partner Agreement ──
    print("\n── C. Partner Agreement Null Model ──")

    # Traditional agreement
    pairs = generate_kw_pairs()
    trad_agree = 0
    trad_total = 0
    for a, b, _ in pairs:
        for line in range(1, 7):
            if tiyong_relation(a, line) == tiyong_relation(b, line):
                trad_agree += 1
            trad_total += 1
    trad_rate = trad_agree / trad_total
    print(f"  Traditional: {trad_agree}/{trad_total} = {trad_rate:.4f}")

    print("  Computing agreement for all surjections...")
    all_pa = []
    for m in assignments:
        all_pa.append(compute_partner_agreement(m))
    a_pa = np.array(all_pa)
    pa_pct = 100.0 * np.sum(a_pa <= trad_rate) / len(a_pa)
    print(f"  Distribution: min={a_pa.min():.4f}, max={a_pa.max():.4f}, "
          f"mean={a_pa.mean():.4f}")
    print(f"  Traditional percentile: {pa_pct:.1f}%")

    # ── D. Shell-Only Pairs ──
    print("\n── D. Shell-Only Pairs ──")
    shell_only, depth_pen = identify_shell_only_pairs()
    print(f"  Shell-only pairs: {len(shell_only)}")
    print(f"  Depth-penetrating pairs: {len(depth_pen)}")

    sa, st = pair_agreement_rate(shell_only)
    da, dt = pair_agreement_rate(depth_pen)
    print(f"  Shell-only agreement: {sa}/{st} = {sa/st:.4f}")
    print(f"  Depth-pen agreement: {da}/{dt} = {da/dt:.4f}")

    shell_data = {
        'shell_pairs': shell_only,
        'depth_pairs': depth_pen,
        'shell_agree': sa, 'shell_total': st,
        'depth_agree': da, 'depth_total': dt,
    }

    # ── E. 变卦 Opposition Map ──
    print("\n── E. 变卦 Opposition Map ──")
    bg_states = compute_biangua_states()

    hex_rel_dist = Counter(s['hex_rel'] for s in bg_states)
    hugua_rel_dist = Counter(s['hugua_rel'] for s in bg_states)
    hugua_hamming_dist = Counter(s['hugua_hamming'] for s in bg_states)
    n_unique_dist = Counter(s['n_unique'] for s in bg_states)
    triple_dist = Counter(s['triple'] for s in bg_states)

    # Line → hugua Hamming
    line_hugua_hamming = {}
    for line in range(1, 7):
        line_hugua_hamming[line] = [s['hugua_hamming'] for s in bg_states if s['line'] == line]

    print(f"  本→变 relation distribution: {dict(hex_rel_dist)}")
    print(f"  互卦 Hamming distribution: {dict(sorted(hugua_hamming_dist.items()))}")
    print(f"  Repetition pattern: {dict(sorted(n_unique_dist.items()))}")

    print(f"\n  Line → 互卦 Hamming:")
    for line in range(1, 7):
        unique = set(line_hugua_hamming[line])
        print(f"    L{line}: {sorted(unique)}")

    biangua_data = {
        'states': bg_states,
        'hex_rel_dist': hex_rel_dist,
        'hugua_rel_dist': hugua_rel_dist,
        'hugua_hamming_dist': hugua_hamming_dist,
        'n_unique_dist': n_unique_dist,
        'triple_dist': triple_dist,
        'line_hugua_hamming': line_hugua_hamming,
    }

    # ── Assemble asymmetry data ──
    asymmetry_data = {
        'trad_asymmetry': trad_asym,
        'all_asymmetry': all_asym,
        'trad_sheng_var': trad_sv,
        'trad_ke_var': trad_kv,
        'all_sheng_var': all_sv,
        'all_ke_var': all_kv,
        'partner_agreement': {
            'trad_rate': trad_rate,
            'all_rates': all_pa,
        },
    }

    # ── Write markdown ──
    md = format_markdown(sheng_profile, ke_profile, masks_data,
                         asymmetry_data, shell_data, biangua_data)
    out_path = Path(__file__).parent / "cycle_algebra_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == '__main__':
    main()
