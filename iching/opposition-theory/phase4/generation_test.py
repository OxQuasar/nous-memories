#!/usr/bin/env python3
"""
Phase 4, Round 3: The Critical Null Model + Consolidation

A. Z₂³ generation null model — does generating full Z₂³ from cycle masks distinguish
   the traditional assignment, or is it a generic property of the partition shape?
B. Exclusive mask partition quality — how cleanly do 生/克 divide the mask space?
C. Directed-cycle Hamming profile — autocorrelation of edge-distance sequences
D. 互卦 amplification verification — confirm deterministic Hamming per line position

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

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

TRIGRAM_ELEMENT = {  # keyed by value where bit0=bottom line, bit2=top line
    0b111: "Metal", 0b011: "Metal",   # Qian ☰, Dui ☱
    0b101: "Fire",                     # Li ☲
    0b001: "Wood",  0b110: "Wood",     # Zhen ☳, Xun ☴
    0b010: "Water",                    # Kan ☵
    0b100: "Earth", 0b000: "Earth",    # Gen ☶, Kun ☷
}

SHENG_EDGES_IDX = [(i, (i + 1) % 5) for i in range(5)]
KE_EDGES_IDX = [(0, 2), (2, 4), (4, 1), (1, 3), (3, 0)]

EDGE_LABELS_SHENG = ["W→F", "F→E", "E→M", "M→Wa", "Wa→W"]
EDGE_LABELS_KE = ["W→E", "E→Wa", "Wa→F", "F→M", "M→W"]

# ─── Bit operations ──────────────────────────────────────────────────────────

def popcount(x):
    return bin(x).count('1')

def bit(x, i):
    return (x >> i) & 1

def fmt3(x):
    return format(x, '03b')

def fmt6(x):
    return format(x, '06b')

def hamming3(a, b):
    return popcount(a ^ b)

# ─── 互卦 ───────────────────────────────────────────────────────────────────

def hugua(x):
    L2, L3, L4, L5 = bit(x, 1), bit(x, 2), bit(x, 3), bit(x, 4)
    return L2 | (L3 << 1) | (L4 << 2) | (L3 << 3) | (L4 << 4) | (L5 << 5)

# ─── GF(2) rank ─────────────────────────────────────────────────────────────

def gf2_rank(vectors, n_bits=3):
    """Compute rank of a set of n_bits-dimensional vectors over GF(2)."""
    # Gaussian elimination over GF(2)
    rows = list(set(vectors))  # deduplicate
    rows = [v for v in rows if v != 0]  # remove zero vector
    pivot_row = 0
    for col in range(n_bits - 1, -1, -1):
        # Find a row with 1 in this column
        found = -1
        for r in range(pivot_row, len(rows)):
            if rows[r] & (1 << col):
                found = r
                break
        if found == -1:
            continue
        # Swap to pivot position
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        # Eliminate
        for r in range(len(rows)):
            if r != pivot_row and rows[r] & (1 << col):
                rows[r] ^= rows[pivot_row]
        pivot_row += 1
    return pivot_row

def generates_z2_cubed(mask_set):
    """Test whether a set of 3-bit masks generates Z₂³ (rank = 3 over GF(2))."""
    nonzero = [m for m in mask_set if m != 0]
    return gf2_rank(nonzero) == 3

# ─── Enumeration ─────────────────────────────────────────────────────────────

def enumerate_assignments():
    trigrams = list(range(NUM_TRIG))
    assignments = []
    for pair_elems in combinations(range(5), 3):
        single_elems = [i for i in range(5) if i not in pair_elems]
        for t0 in combinations(trigrams, 2):
            rem1 = [t for t in trigrams if t not in t0]
            for t1 in combinations(rem1, 2):
                rem2 = [t for t in rem1 if t not in t1]
                for t2 in combinations(rem2, 2):
                    rem3 = [t for t in rem2 if t not in t2]
                    for perm in permutations(rem3):
                        m = {}
                        for t in t0: m[t] = pair_elems[0]
                        for t in t1: m[t] = pair_elems[1]
                        for t in t2: m[t] = pair_elems[2]
                        for idx, t in enumerate(perm): m[t] = single_elems[idx]
                        assignments.append(m)
    return assignments

# ─── Per-assignment scoring ──────────────────────────────────────────────────

def score_assignment(mapping):
    """
    For a given trigram→element mapping, compute:
    - XOR mask sets for 生 and 克 cycles
    - Whether each generates Z₂³
    - Number of distinct nonzero masks
    - Edge-mean Hamming sequences
    """
    elem_trigs = {}
    for t, e in mapping.items():
        elem_trigs.setdefault(e, []).append(t)

    def cycle_masks_and_profile(edges):
        masks = set()
        edge_means = []
        for src_e, tgt_e in edges:
            st = elem_trigs.get(src_e, [])
            tt = elem_trigs.get(tgt_e, [])
            edge_h = []
            for s in st:
                for t in tt:
                    masks.add(s ^ t)
                    edge_h.append(hamming3(s, t))
            edge_means.append(np.mean(edge_h) if edge_h else 0.0)
        nonzero = masks - {0}
        return nonzero, edge_means

    s_masks, s_profile = cycle_masks_and_profile(SHENG_EDGES_IDX)
    k_masks, k_profile = cycle_masks_and_profile(KE_EDGES_IDX)

    s_gen = generates_z2_cubed(s_masks)
    k_gen = generates_z2_cubed(k_masks)

    # Exclusive masks
    shared = s_masks & k_masks
    excl_s = s_masks - k_masks
    excl_k = k_masks - s_masks
    all_masks = s_masks | k_masks
    partition_cleanness = (len(excl_s) + len(excl_k)) / len(all_masks) if all_masks else 0

    # Autocorrelation at lag 1 of edge-mean sequence
    def autocorr_lag1(seq):
        arr = np.array(seq, dtype=float)
        if np.std(arr) == 0:
            return 0.0
        arr = arr - arr.mean()
        n = len(arr)
        return float(np.sum(arr[:-1] * arr[1:]) / np.sum(arr ** 2))

    s_ac1 = autocorr_lag1(s_profile)
    k_ac1 = autocorr_lag1(k_profile)

    return {
        's_masks': s_masks, 'k_masks': k_masks,
        's_gen': s_gen, 'k_gen': k_gen,
        's_n_masks': len(s_masks), 'k_n_masks': len(k_masks),
        'shared': len(shared), 'excl_s': len(excl_s), 'excl_k': len(excl_k),
        'partition_cleanness': partition_cleanness,
        's_profile': s_profile, 'k_profile': k_profile,
        's_ac1': s_ac1, 'k_ac1': k_ac1,
    }

# ─── D. 互卦 verification ───────────────────────────────────────────────────

def verify_hugua_amplification():
    """
    For every hexagram and every line position, verify that
    Hamming(互卦(x), 互卦(x ⊕ bit_k)) is deterministic per line position.
    """
    expected = {0: 0, 1: 1, 2: 2, 3: 2, 4: 1, 5: 0}
    results = {}
    all_pass = True

    for k in range(6):
        hammings = set()
        for x in range(NUM_HEX):
            x_flipped = x ^ (1 << k)
            h = popcount(hugua(x) ^ hugua(x_flipped))
            hammings.add(h)
        is_deterministic = len(hammings) == 1
        actual = hammings.pop() if is_deterministic else hammings
        matches = is_deterministic and actual == expected[k]
        if not matches:
            all_pass = False
        results[k] = {
            'deterministic': is_deterministic,
            'value': actual if is_deterministic else sorted(hammings),
            'expected': expected[k],
            'matches': matches,
        }
    return all_pass, results

# ─── Markdown formatting ────────────────────────────────────────────────────

def format_markdown(gen_data, partition_data, profile_data, hugua_data):
    lines = []
    w = lines.append

    w("# Phase 4 Round 3: Critical Null Model + Consolidation\n")

    # ══════════════════════════════════════════════════════════════════════
    # A. Z₂³ Generation Null Model
    # ══════════════════════════════════════════════════════════════════════
    w("## A. Z₂³ Generation Null Model\n")
    w("For each of 50,400 valid surjections (8 trigrams → 5 elements, partition 2,2,2,1,1),")
    w("compute the XOR masks produced by each five-phase cycle and test whether they generate")
    w("the full group Z₂³ under XOR closure (i.e., GF(2)-rank = 3).\n")

    g = gen_data
    n = g['n_total']

    w("### Generation rates\n")
    w(f"| Condition | Count | Rate |")
    w(f"|-----------|-------|------|")
    w(f"| 生 generates Z₂³ | {g['s_gen_count']} | {g['s_gen_count']/n:.4f} |")
    w(f"| 克 generates Z₂³ | {g['k_gen_count']} | {g['k_gen_count']/n:.4f} |")
    w(f"| **Both** generate Z₂³ | {g['both_count']} | {g['both_count']/n:.4f} |")
    w(f"| **Neither** generates Z₂³ | {g['neither_count']} | {g['neither_count']/n:.4f} |")
    w(f"| 生 only | {g['s_only_count']} | {g['s_only_count']/n:.4f} |")
    w(f"| 克 only | {g['k_only_count']} | {g['k_only_count']/n:.4f} |")
    w("")

    both_rate = g['both_count'] / n
    if both_rate < 0.10:
        verdict = "**REMARKABLE:** Fewer than 10% of assignments achieve dual generation."
    elif both_rate < 0.30:
        verdict = "**NOTABLE:** The dual-generation property is uncommon but not rare."
    elif both_rate < 0.50:
        verdict = "**MODERATE:** A substantial minority achieves dual generation."
    else:
        verdict = "**GENERIC:** Dual generation is the common case — the finding is not distinctive."

    w(f"### Verdict\n")
    w(f"Both-generate rate: **{both_rate:.1%}**\n")
    w(f"{verdict}")
    w(f"The traditional assignment {'**is**' if both_rate < 0.30 else 'is **not**'} "
      f"algebraically distinguished by dual Z₂³ generation alone.\n")

    # Mask count distribution
    w("### Number of distinct nonzero masks per cycle\n")
    w("| # masks | 生 count | 生 frac | 克 count | 克 frac |")
    w("|---------|----------|---------|----------|---------|")
    for nm in sorted(set(list(g['s_mask_dist'].keys()) + list(g['k_mask_dist'].keys()))):
        sc = g['s_mask_dist'].get(nm, 0)
        kc = g['k_mask_dist'].get(nm, 0)
        w(f"| {nm} | {sc} | {sc/n:.4f} | {kc} | {kc/n:.4f} |")
    w("")
    w(f"**Traditional:** 生 has {g['trad_s_n_masks']} masks, 克 has {g['trad_k_n_masks']} masks.")

    # Mean masks
    s_mask_arr = np.array(g['all_s_n_masks'])
    k_mask_arr = np.array(g['all_k_n_masks'])
    w(f"**Mean masks:** 生 = {s_mask_arr.mean():.2f}, 克 = {k_mask_arr.mean():.2f}\n")

    # Relationship between mask count and generation
    w("### Mask count → generation rate\n")
    w("| # masks | 生 gen rate | 克 gen rate |")
    w("|---------|------------|------------|")
    for nm in sorted(g['masks_vs_gen_s'].keys()):
        s_total, s_gen = g['masks_vs_gen_s'].get(nm, (0, 0))
        k_total, k_gen = g['masks_vs_gen_k'].get(nm, (0, 0))
        sr = s_gen / s_total if s_total > 0 else 0
        kr = k_gen / k_total if k_total > 0 else 0
        w(f"| {nm} | {sr:.4f} (n={s_total}) | {kr:.4f} (n={k_total}) |")
    w("")

    # ══════════════════════════════════════════════════════════════════════
    # B. Exclusive Mask Partition Quality
    # ══════════════════════════════════════════════════════════════════════
    w("## B. Exclusive Mask Partition Quality\n")
    w("Among surjections where both cycles generate Z₂³:\n")

    p = partition_data
    if p['n_dual'] > 0:
        w(f"**N (both generate):** {p['n_dual']}\n")

        w("### Partition cleanness distribution\n")
        w(f"Cleanness = (exclusive_生 + exclusive_克) / total_distinct_masks\n")
        w(f"**Traditional:** excl_生={p['trad_excl_s']}, excl_克={p['trad_excl_k']}, "
          f"shared={p['trad_shared']}, cleanness={p['trad_cleanness']:.4f}\n")

        pc_arr = np.array(p['all_cleanness'])
        pct = 100.0 * np.sum(pc_arr <= p['trad_cleanness']) / len(pc_arr)
        w(f"**Distribution:** min={pc_arr.min():.4f}, max={pc_arr.max():.4f}, "
          f"mean={pc_arr.mean():.4f}, std={pc_arr.std():.4f}")
        w(f"**Traditional percentile:** {pct:.1f}%\n")

        # Histogram
        w("```")
        bins = np.linspace(pc_arr.min() - 0.01, pc_arr.max() + 0.01, 15)
        hist, edges = np.histogram(pc_arr, bins=bins)
        max_bar = max(hist) if max(hist) > 0 else 1
        for i in range(len(hist)):
            lo, hi = edges[i], edges[i + 1]
            bar_len = int(50 * hist[i] / max_bar)
            marker = " ◄ TRAD" if lo <= p['trad_cleanness'] < hi else ""
            w(f"  {lo:.3f}-{hi:.3f} | {'█' * bar_len} {hist[i]}{marker}")
        w("```\n")

        # Exclusive count distribution
        w("### Exclusive mask counts\n")
        w("| excl_生 | excl_克 | shared | Count | Frac |")
        w("|---------|---------|--------|-------|------|")
        for key, cnt in sorted(p['excl_dist'].items(), key=lambda x: -x[1]):
            es, ek, sh = key
            is_trad = (es == p['trad_excl_s'] and ek == p['trad_excl_k'] and sh == p['trad_shared'])
            marker = " ◄ TRAD" if is_trad else ""
            w(f"| {es} | {ek} | {sh} | {cnt} | {cnt/p['n_dual']:.4f} |{marker}")
        w("")
    else:
        w("No surjections achieve dual Z₂³ generation.\n")

    # ══════════════════════════════════════════════════════════════════════
    # C. Directed-Cycle Hamming Profile
    # ══════════════════════════════════════════════════════════════════════
    w("## C. Directed-Cycle Hamming Profile\n")

    pr = profile_data
    w("### Traditional edge-mean sequences\n")
    w(f"**生:** {[f'{d:.2f}' for d in pr['trad_s_profile']]}")
    w(f"  Edges: {EDGE_LABELS_SHENG}\n")
    w(f"**克:** {[f'{d:.2f}' for d in pr['trad_k_profile']]}")
    w(f"  Edges: {EDGE_LABELS_KE}\n")

    w("### Autocorrelation at lag 1\n")
    w("Measures whether high/low distance edges cluster together (+) or alternate (−).\n")

    s_ac = np.array(pr['all_s_ac1'])
    k_ac = np.array(pr['all_k_ac1'])
    trad_s_ac = pr['trad_s_ac1']
    trad_k_ac = pr['trad_k_ac1']
    s_pct = 100.0 * np.sum(s_ac <= trad_s_ac) / len(s_ac)
    k_pct = 100.0 * np.sum(k_ac <= trad_k_ac) / len(k_ac)

    w(f"| Cycle | Traditional AC(1) | Mean | Std | Percentile |")
    w(f"|-------|-------------------|------|-----|------------|")
    w(f"| 生 | {trad_s_ac:+.4f} | {s_ac.mean():+.4f} | {s_ac.std():.4f} | {s_pct:.1f}% |")
    w(f"| 克 | {trad_k_ac:+.4f} | {k_ac.mean():+.4f} | {k_ac.std():.4f} | {k_pct:.1f}% |")
    w("")

    # Histograms
    for label, arr, trad_val in [("生", s_ac, trad_s_ac), ("克", k_ac, trad_k_ac)]:
        w(f"### Histogram: {label} AC(1)\n")
        w("```")
        finite = arr[np.isfinite(arr)]
        if len(finite) > 0:
            bins = np.linspace(finite.min() - 0.01, finite.max() + 0.01, 21)
            hist, edges = np.histogram(finite, bins=bins)
            max_bar = max(hist) if max(hist) > 0 else 1
            for i in range(len(hist)):
                lo, hi = edges[i], edges[i + 1]
                bar_len = int(50 * hist[i] / max_bar)
                marker = " ◄ TRAD" if lo <= trad_val < hi else ""
                w(f"  {lo:+6.3f} to {hi:+6.3f} | {'█' * bar_len} {hist[i]}{marker}")
        w("```\n")

    # ══════════════════════════════════════════════════════════════════════
    # D. 互卦 Amplification Verification
    # ══════════════════════════════════════════════════════════════════════
    w("## D. 互卦 Amplification Verification\n")

    hd = hugua_data
    w(f"**All pass:** {hd['all_pass']}\n")
    w("| Line | Bit | Expected Hamming | Actual | Deterministic | Matches |")
    w("|------|-----|-----------------|--------|---------------|---------|")
    line_names = ["L1 (outer)", "L2 (middle)", "L3 (inner)", "L4 (inner)", "L5 (middle)", "L6 (outer)"]
    for k in range(6):
        r = hd['results'][k]
        w(f"| {line_names[k]} | {k} | {r['expected']} | {r['value']} | {r['deterministic']} | {r['matches']} |")
    w("")

    if hd['all_pass']:
        w("**Theorem (confirmed):** The 互卦 map has deterministic Hamming response to single-line flips:\n")
        w("- **Outer pair (L1, L6):** Hamming = 0 — completely erased")
        w("- **Middle pair (L2, L5):** Hamming = 1 — faithfully transmitted")
        w("- **Inner pair (L3, L4):** Hamming = 2 — doubled (amplified)\n")
        w("This follows directly from the 互卦 definition: it picks bits {1,2,3,2,3,4},")
        w("so bit 2 (L3) and bit 3 (L4) each appear twice in the output, bits 1,4 appear once,")
        w("and bits 0,5 are absent. The amplification factor per mirror-pair layer is:")
        w("O→0, M→1, I→2.\n")
    else:
        w("**Verification FAILED** — see table above for details.\n")

    # ══════════════════════════════════════════════════════════════════════
    # Structural Summary
    # ══════════════════════════════════════════════════════════════════════
    w("## Structural Summary\n")

    w("### Is dual Z₂³ generation remarkable?\n")
    if both_rate < 0.10:
        w(f"**Yes.** Only {both_rate:.1%} of assignments achieve it.")
        w("The traditional mapping is in a small algebraic elite.\n")
    elif both_rate < 0.30:
        w(f"**Somewhat.** {both_rate:.1%} achieve it — uncommon but not rare.")
        w("The traditional mapping has a notable algebraic property, but it's not uniquely determined by it.\n")
    elif both_rate < 0.50:
        w(f"**Weakly.** {both_rate:.1%} achieve it — a substantial minority.")
        w("The property narrows the space but doesn't strongly distinguish the traditional mapping.\n")
    else:
        w(f"**No.** {both_rate:.1%} achieve it — this is the generic case.")
        w("Dual Z₂³ generation is a near-automatic consequence of the partition shape,")
        w("not a distinguishing feature of the traditional assignment.\n")

    w("### What IS distinctive about the traditional mapping?\n")
    w("Combining all Phase 4 results:\n")

    # List findings by strength
    findings = []
    findings.append(f"- **克 edge variance** is extreme (96.2nd percentile from Round 2) — "
                    f"the Water→Fire singleton edge at d=3 is structurally forced")
    findings.append(f"- **生−克 asymmetry** ({pr['trad_asymmetry']:.4f}) at ~77th percentile — "
                    f"moderately unusual directional bias")

    if p['n_dual'] > 0:
        findings.append(f"- **Partition cleanness** ({p['trad_cleanness']:.4f}) at "
                        f"{100*np.sum(np.array(p['all_cleanness']) <= p['trad_cleanness'])/len(p['all_cleanness']):.1f}th percentile")

    if both_rate < 0.50:
        findings.append(f"- **Dual Z₂³ generation** ({both_rate:.1%}) — "
                        f"{'distinctive' if both_rate < 0.30 else 'somewhat selective'}")
    else:
        findings.append(f"- **Dual Z₂³ generation** ({both_rate:.1%}) — generic, not distinctive")

    findings.append(f"- **XOR mask coverage:** all 7 nonzero masks covered (生 ∪ 克 = Z₂³ \\ {{0}})")
    findings.append(f"- **Shell-only pairs** show 2.33× agreement ratio (structural, not mapping-dependent)")
    findings.append(f"- **互卦 amplification** O→0, M→1, I→2 (theorem, not mapping-dependent)")
    findings.append(f"- **体/用 samples uniformly** from all trigram pairs (theorem, not mapping-dependent)")

    for f in findings:
        w(f)
    w("")

    return '\n'.join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PHASE 4 ROUND 3: CRITICAL NULL MODEL + CONSOLIDATION")
    print("=" * 70)

    # ── D. Quick verification (fast, do first) ──
    print("\n── D. 互卦 Amplification Verification ──")
    all_pass, hugua_results = verify_hugua_amplification()
    print(f"  All pass: {all_pass}")
    for k in range(6):
        r = hugua_results[k]
        print(f"  L{k+1} (bit {k}): expected={r['expected']}, actual={r['value']}, ok={r['matches']}")

    # ── Enumerate surjections ──
    print("\n── Enumerating 50,400 surjections ──")
    assignments = enumerate_assignments()
    n_total = len(assignments)
    print(f"  Total: {n_total}")

    # Find traditional
    trad_map = {t: ELEMENTS.index(e) for t, e in TRIGRAM_ELEMENT.items()}
    trad_idx = -1
    for i, m in enumerate(assignments):
        if m == trad_map:
            trad_idx = i
            break
    print(f"  Traditional index: {trad_idx}")

    # ── Score all assignments ──
    print("\n── A. Z₂³ Generation Null Model ──")
    print("  Scoring all assignments...")

    all_scores = []
    for m in assignments:
        all_scores.append(score_assignment(m))

    trad = all_scores[trad_idx]

    # Generation counts
    s_gen_count = sum(1 for s in all_scores if s['s_gen'])
    k_gen_count = sum(1 for s in all_scores if s['k_gen'])
    both_count = sum(1 for s in all_scores if s['s_gen'] and s['k_gen'])
    neither_count = sum(1 for s in all_scores if not s['s_gen'] and not s['k_gen'])
    s_only_count = sum(1 for s in all_scores if s['s_gen'] and not s['k_gen'])
    k_only_count = sum(1 for s in all_scores if s['k_gen'] and not s['s_gen'])

    print(f"\n  生 generates Z₂³: {s_gen_count}/{n_total} = {s_gen_count/n_total:.4f}")
    print(f"  克 generates Z₂³: {k_gen_count}/{n_total} = {k_gen_count/n_total:.4f}")
    print(f"  Both: {both_count}/{n_total} = {both_count/n_total:.4f}")
    print(f"  Neither: {neither_count}/{n_total} = {neither_count/n_total:.4f}")
    print(f"  Traditional: 生={trad['s_gen']}, 克={trad['k_gen']}")

    # Mask count distribution
    s_mask_dist = Counter(s['s_n_masks'] for s in all_scores)
    k_mask_dist = Counter(s['k_n_masks'] for s in all_scores)
    all_s_n_masks = [s['s_n_masks'] for s in all_scores]
    all_k_n_masks = [s['k_n_masks'] for s in all_scores]

    print(f"\n  Mask count distribution (生):")
    for nm in sorted(s_mask_dist):
        print(f"    {nm} masks: {s_mask_dist[nm]} ({s_mask_dist[nm]/n_total:.4f})")
    print(f"  Mask count distribution (克):")
    for nm in sorted(k_mask_dist):
        print(f"    {nm} masks: {k_mask_dist[nm]} ({k_mask_dist[nm]/n_total:.4f})")
    print(f"  Traditional: 生={trad['s_n_masks']}, 克={trad['k_n_masks']}")

    # Mask count vs generation rate
    masks_vs_gen_s = {}
    masks_vs_gen_k = {}
    for s in all_scores:
        nm = s['s_n_masks']
        total, gen = masks_vs_gen_s.get(nm, (0, 0))
        masks_vs_gen_s[nm] = (total + 1, gen + (1 if s['s_gen'] else 0))
        nm = s['k_n_masks']
        total, gen = masks_vs_gen_k.get(nm, (0, 0))
        masks_vs_gen_k[nm] = (total + 1, gen + (1 if s['k_gen'] else 0))

    gen_data = {
        'n_total': n_total,
        's_gen_count': s_gen_count, 'k_gen_count': k_gen_count,
        'both_count': both_count, 'neither_count': neither_count,
        's_only_count': s_only_count, 'k_only_count': k_only_count,
        's_mask_dist': s_mask_dist, 'k_mask_dist': k_mask_dist,
        'all_s_n_masks': all_s_n_masks, 'all_k_n_masks': all_k_n_masks,
        'trad_s_n_masks': trad['s_n_masks'], 'trad_k_n_masks': trad['k_n_masks'],
        'masks_vs_gen_s': masks_vs_gen_s, 'masks_vs_gen_k': masks_vs_gen_k,
    }

    # ── B. Partition quality ──
    print("\n── B. Exclusive Mask Partition Quality ──")
    dual_scores = [s for s in all_scores if s['s_gen'] and s['k_gen']]
    n_dual = len(dual_scores)
    print(f"  Dual-generation assignments: {n_dual}")

    all_cleanness = [s['partition_cleanness'] for s in dual_scores]
    excl_dist = Counter((s['excl_s'], s['excl_k'], s['shared']) for s in dual_scores)

    if n_dual > 0:
        pc_arr = np.array(all_cleanness)
        trad_clean = trad['partition_cleanness']
        pct = 100.0 * np.sum(pc_arr <= trad_clean) / len(pc_arr)
        print(f"  Traditional cleanness: {trad_clean:.4f} (percentile: {pct:.1f}%)")
        print(f"  Distribution: min={pc_arr.min():.4f}, max={pc_arr.max():.4f}, mean={pc_arr.mean():.4f}")

    partition_data = {
        'n_dual': n_dual,
        'all_cleanness': all_cleanness,
        'excl_dist': excl_dist,
        'trad_excl_s': trad['excl_s'],
        'trad_excl_k': trad['excl_k'],
        'trad_shared': trad['shared'],
        'trad_cleanness': trad['partition_cleanness'],
    }

    # ── C. Profile / autocorrelation ──
    print("\n── C. Directed-Cycle Hamming Profile ──")
    all_s_ac1 = [s['s_ac1'] for s in all_scores]
    all_k_ac1 = [s['k_ac1'] for s in all_scores]

    trad_s_profile = trad['s_profile']
    trad_k_profile = trad['k_profile']

    print(f"  Traditional 生 profile: {[f'{d:.2f}' for d in trad_s_profile]}")
    print(f"  Traditional 克 profile: {[f'{d:.2f}' for d in trad_k_profile]}")
    print(f"  Traditional 生 AC(1): {trad['s_ac1']:+.4f}")
    print(f"  Traditional 克 AC(1): {trad['k_ac1']:+.4f}")

    # Compute asymmetry for structural summary
    s_overall = sum(d * n for d, n in zip(trad_s_profile, [2, 2, 4, 2, 2])) / 12
    k_overall = sum(d * n for d, n in zip(trad_k_profile, [4, 2, 1, 2, 4])) / 13
    trad_asymmetry = s_overall - k_overall

    profile_data = {
        'trad_s_profile': trad_s_profile,
        'trad_k_profile': trad_k_profile,
        'trad_s_ac1': trad['s_ac1'],
        'trad_k_ac1': trad['k_ac1'],
        'all_s_ac1': all_s_ac1,
        'all_k_ac1': all_k_ac1,
        'trad_asymmetry': trad_asymmetry,
    }

    hugua_data = {'all_pass': all_pass, 'results': hugua_results}

    # ── Write markdown ──
    md = format_markdown(gen_data, partition_data, profile_data, hugua_data)
    out_path = Path(__file__).parent / "generation_test_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == '__main__':
    main()
