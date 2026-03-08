#!/usr/bin/env python3
"""
Probe 5: S₄ × 五行 — Involutions, Parity, and the Semantic Gap

Investigates how V₄ involutions (reverse, complement, reverse-complement)
interact with 五行 structure on Z₂³ (trigrams) and Z₂⁶ (hexagrams).

Encoding: bit 0 = bottom line, bit 2 = top (trigrams); bit 0 = bottom, bit 5 = top (hexagrams).
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict
from math import log2

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "opposition-theory" / "phase4"))
from cycle_algebra import (
    NUM_HEX, NUM_TRIG, MASK3, MASK_ALL,
    TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENTS, ELEMENT_ZH,
    SHENG_MAP, KE_MAP, SHENG_CYCLE,
    lower_trigram, upper_trigram, reverse6, fmt6, fmt3, bit, popcount,
    five_phase_relation, ELEM_TRIGRAMS,
)

# ─── Trigram-level involutions ──────────────────────────────────────────────

def reverse3(t):
    """Reverse bits 0↔2 of a 3-bit trigram."""
    return ((t & 1) << 2) | (t & 2) | ((t >> 2) & 1)

def complement3(t):
    return t ^ MASK3

def rev_comp3(t):
    return reverse3(complement3(t))

# ─── Hexagram-level involutions ─────────────────────────────────────────────

def complement6(x):
    return x ^ MASK_ALL

def rev_comp6(x):
    return reverse6(complement6(x))

# ─── Parity ─────────────────────────────────────────────────────────────────

def parity3(t):
    """b₀ ⊕ b₁ parity of a trigram."""
    return (t ^ (t >> 1)) & 1

PARITY_NAMES = {0: "even {Earth,Metal}", 1: "odd {Wood,Fire,Water}"}

# ─── Information theory ─────────────────────────────────────────────────────

def entropy(counts):
    """Shannon entropy from a dict/Counter of counts."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * log2(p)
    return h

def conditional_entropy(joint_counts):
    """H(Y|X) from joint_counts[(x, y)] → count."""
    x_counts = Counter()
    for (x, y), c in joint_counts.items():
        x_counts[x] += c
    total = sum(joint_counts.values())
    h = 0.0
    for x, cx in x_counts.items():
        if cx == 0:
            continue
        px = cx / total
        hy_given_x = 0.0
        for (xx, y), c in joint_counts.items():
            if xx == x and c > 0:
                py_x = c / cx
                hy_given_x -= py_x * log2(py_x)
        h += px * hy_given_x
    return h


# ═══════════════════════════════════════════════════════════════════════════
# A. V₄ orbits on trigrams
# ═══════════════════════════════════════════════════════════════════════════

def compute_v4_orbits():
    """Compute orbits of V₄ = {id, reverse, complement, rev∘comp} on 8 trigrams."""
    visited = set()
    orbits = []
    for t in range(NUM_TRIG):
        if t in visited:
            continue
        orbit = {t, reverse3(t), complement3(t), rev_comp3(t)}
        orbits.append(sorted(orbit))
        visited |= orbit
    return orbits

def analyze_orbits():
    orbits = compute_v4_orbits()
    results = []
    for orbit in orbits:
        parities = [parity3(t) for t in orbit]
        elements = [TRIGRAM_ELEMENT[t] for t in orbit]
        results.append({
            'trigrams': orbit,
            'names': [TRIGRAM_NAMES[t] for t in orbit],
            'parities': parities,
            'parity_constant': len(set(parities)) == 1,
            'elements': elements,
            'unique_elements': sorted(set(elements)),
        })
    return results


# ═══════════════════════════════════════════════════════════════════════════
# B. Which involutions preserve/break parity?
# ═══════════════════════════════════════════════════════════════════════════

TRIG_INVOLUTIONS = {
    'reverse': reverse3,
    'complement': complement3,
    'rev∘comp': rev_comp3,
}

def analyze_parity_preservation():
    results = {}
    for name, inv in TRIG_INVOLUTIONS.items():
        preserves = []
        breaks_ = []
        for t in range(NUM_TRIG):
            if parity3(t) == parity3(inv(t)):
                preserves.append(t)
            else:
                breaks_.append(t)
        if len(breaks_) == 0:
            classification = "preserves"
        elif len(preserves) == 0:
            classification = "breaks"
        else:
            classification = "mixed"
        results[name] = {
            'preserves': preserves,
            'breaks': breaks_,
            'classification': classification,
        }
    return results


# ═══════════════════════════════════════════════════════════════════════════
# C. Hexagram-level: parity and 五行 disruption per involution
# ═══════════════════════════════════════════════════════════════════════════

HEX_INVOLUTIONS = {
    'reverse₆': reverse6,
    'complement₆': complement6,
    'rev∘comp₆': rev_comp6,
}

RELATION_CLASS = {
    '比和': '比', '生体': '生', '体生用': '生', '克体': '克', '体克用': '克',
}

def analyze_hex_involutions():
    """For each hexagram involution, compute parity/element/relation disruption."""
    results = {}
    for name, inv in HEX_INVOLUTIONS.items():
        parity_changes_lower = 0
        parity_changes_upper = 0
        element_changes_lower = 0
        element_changes_upper = 0
        relation_changes = 0
        relation_class_changes = 0  # 比/生/克 category change
        element_set_changes = 0     # whether the *set* of elements changes
        relation_transitions = Counter()

        pairs_seen = set()
        pair_details = []

        for x in range(NUM_HEX):
            y = inv(x)
            pair_key = (min(x, y), max(x, y))
            if pair_key in pairs_seen or x == y:
                continue
            pairs_seen.add(pair_key)

            lo_x, up_x = lower_trigram(x), upper_trigram(x)
            lo_y, up_y = lower_trigram(y), upper_trigram(y)

            # Parity changes
            p_lo_changed = parity3(lo_x) != parity3(lo_y)
            p_up_changed = parity3(up_x) != parity3(up_y)
            if p_lo_changed:
                parity_changes_lower += 1
            if p_up_changed:
                parity_changes_upper += 1

            # Element changes
            e_lo_x, e_up_x = TRIGRAM_ELEMENT[lo_x], TRIGRAM_ELEMENT[up_x]
            e_lo_y, e_up_y = TRIGRAM_ELEMENT[lo_y], TRIGRAM_ELEMENT[up_y]
            if e_lo_x != e_lo_y:
                element_changes_lower += 1
            if e_up_x != e_up_y:
                element_changes_upper += 1

            # Element *set* preservation
            set_x = frozenset([e_lo_x, e_up_x])
            set_y = frozenset([e_lo_y, e_up_y])
            if set_x != set_y:
                element_set_changes += 1

            # Five-phase relation (体=upper, 用=lower for this analysis)
            rel_x = five_phase_relation(e_up_x, e_lo_x)
            rel_y = five_phase_relation(e_up_y, e_lo_y)
            if rel_x != rel_y:
                relation_changes += 1
            if RELATION_CLASS[rel_x] != RELATION_CLASS[rel_y]:
                relation_class_changes += 1
            relation_transitions[(rel_x, rel_y)] += 1

            pair_details.append({
                'x': x, 'y': y,
                'lo_x': lo_x, 'up_x': up_x, 'lo_y': lo_y, 'up_y': up_y,
                'e_lo_x': e_lo_x, 'e_up_x': e_up_x,
                'e_lo_y': e_lo_y, 'e_up_y': e_up_y,
                'set_x': set_x, 'set_y': set_y,
                'p_lo_changed': p_lo_changed, 'p_up_changed': p_up_changed,
                'rel_x': rel_x, 'rel_y': rel_y,
            })

        n_pairs = len(pairs_seen)
        results[name] = {
            'n_pairs': n_pairs,
            'parity_changes_lower': parity_changes_lower,
            'parity_changes_upper': parity_changes_upper,
            'element_changes_lower': element_changes_lower,
            'element_changes_upper': element_changes_upper,
            'element_set_changes': element_set_changes,
            'relation_changes': relation_changes,
            'relation_class_changes': relation_class_changes,
            'relation_transitions': relation_transitions,
            'pair_details': pair_details,
        }
    return results


# ═══════════════════════════════════════════════════════════════════════════
# D. Wood's special status
# ═══════════════════════════════════════════════════════════════════════════

def analyze_element_closure():
    """For each involution, which elements are preserved (element(t) == element(inv(t)))?"""
    results = {}
    for name, inv in TRIG_INVOLUTIONS.items():
        preserved = Counter()
        broken_to = defaultdict(Counter)
        total_by_elem = Counter()
        for t in range(NUM_TRIG):
            e_orig = TRIGRAM_ELEMENT[t]
            e_inv = TRIGRAM_ELEMENT[inv(t)]
            total_by_elem[e_orig] += 1
            if e_orig == e_inv:
                preserved[e_orig] += 1
            else:
                broken_to[e_orig][e_inv] += 1
        results[name] = {
            'preserved': preserved,
            'broken_to': dict(broken_to),
            'total': total_by_elem,
        }
    return results


# ═══════════════════════════════════════════════════════════════════════════
# E. The 1.50/2.25 bit prediction
# ═══════════════════════════════════════════════════════════════════════════

def compute_complement_pairs():
    """Return the 4 complement pairs as a partition of 8 trigrams."""
    pairs = []
    seen = set()
    for t in range(NUM_TRIG):
        if t in seen:
            continue
        c = complement3(t)
        pairs.append((t, c))
        seen.add(t)
        seen.add(c)
    return pairs

def analyze_complement_pair_mi():
    """MI(五行, complement_pair_partition) — the 1.50 number from wuxing findings."""
    pairs = compute_complement_pairs()

    # Build joint: (pair_id, element) → count
    joint = Counter()
    for pid, (t1, t2) in enumerate(pairs):
        joint[(pid, TRIGRAM_ELEMENT[t1])] += 1
        joint[(pid, TRIGRAM_ELEMENT[t2])] += 1

    elem_counts = Counter(TRIGRAM_ELEMENT[t] for t in range(NUM_TRIG))
    h_wuxing = entropy(elem_counts)
    h_cond = conditional_entropy(joint)
    mi = h_wuxing - h_cond

    return {
        'h_wuxing': h_wuxing,
        'h_conditional': h_cond,
        'mi': mi,
        'pairs': pairs,
    }

def analyze_function_mi(inv_func, label):
    """MI(element(t), element(inv(t))) for a given involution function."""
    joint = Counter()
    for t in range(NUM_TRIG):
        joint[(TRIGRAM_ELEMENT[t], TRIGRAM_ELEMENT[inv_func(t)])] += 1

    elem_counts = Counter(TRIGRAM_ELEMENT[t] for t in range(NUM_TRIG))
    h_wuxing = entropy(elem_counts)
    h_cond = conditional_entropy(joint)
    mi = h_wuxing - h_cond
    return {'h_wuxing': h_wuxing, 'h_conditional': h_cond, 'mi': mi, 'joint': joint}

def analyze_pair_partition_mi(inv_func, label):
    """MI(五行, pair_partition_under_inv) for any involution."""
    pairs = []
    seen = set()
    for t in range(NUM_TRIG):
        if t in seen:
            continue
        partner = inv_func(t)
        if partner == t:
            pairs.append((t,))
            seen.add(t)
        else:
            pairs.append((t, partner))
            seen.add(t)
            seen.add(partner)

    joint = Counter()
    for pid, members in enumerate(pairs):
        for t in members:
            joint[(pid, TRIGRAM_ELEMENT[t])] += 1

    elem_counts = Counter(TRIGRAM_ELEMENT[t] for t in range(NUM_TRIG))
    h_wuxing = entropy(elem_counts)
    h_cond = conditional_entropy(joint)
    mi = h_wuxing - h_cond
    return {'h_wuxing': h_wuxing, 'h_conditional': h_cond, 'mi': mi, 'pairs': pairs}


# ═══════════════════════════════════════════════════════════════════════════
# Markdown output
# ═══════════════════════════════════════════════════════════════════════════

def format_results(orbit_data, parity_data, hex_data, closure_data,
                   comp_pair_mi, func_mi, pair_mi):
    lines = []
    w = lines.append

    w("# Probe 5: S₄ × 五行 — Involutions, Parity, and the Semantic Gap\n")

    # ── A ──
    w("## A. V₄ Orbits on Trigrams vs Parity\n")
    w("V₄ = ⟨reverse, complement⟩ on Z₂³. Three non-identity elements:")
    w("reverse (swap b₀↔b₂), complement (XOR 111), reverse∘complement.\n")

    w("### Orbits\n")
    w("| Orbit | Trigrams | Parities (b₀⊕b₁) | Elements | Parity constant? |")
    w("|-------|---------|-------------------|----------|------------------|")
    for o in orbit_data:
        tnames = ", ".join(o['names'])
        pars = ", ".join(str(p) for p in o['parities'])
        elems = ", ".join(o['unique_elements'])
        w(f"| {{{', '.join(fmt3(t) for t in o['trigrams'])}}} | {tnames} | {pars} | {elems} | "
          f"{'✓' if o['parity_constant'] else '✗'} |")
    w("")

    n_const = sum(1 for o in orbit_data if o['parity_constant'])
    n_total = len(orbit_data)
    w(f"**Result:** {n_const}/{n_total} orbits have constant parity.")

    # Describe the mixed orbit
    mixed = [o for o in orbit_data if not o['parity_constant']]
    if mixed:
        o = mixed[0]
        w(f"The size-4 orbit {{{', '.join(o['names'])}}} mixes parities {o['parities']} "
          f"and crosses three elements ({', '.join(o['unique_elements'])}).")
    w("")
    w("**Parity partially overlaps V₄ orbits.** The two size-2 orbits (fixed points of specific")
    w("involutions) are parity-pure, but the generic orbit crosses the parity boundary. V₄ action")
    w("does NOT respect the {Earth,Metal} / {Wood,Fire,Water} split in general.\n")

    # ── B ──
    w("## B. Which Involutions Preserve vs Break Parity?\n")

    w("### Per-involution classification\n")
    w("| Involution | Classification | Preserves | Breaks |")
    w("|-----------|----------------|-----------|--------|")
    for name in ['reverse', 'complement', 'rev∘comp']:
        d = parity_data[name]
        n_pres = len(d['preserves'])
        n_brk = len(d['breaks'])
        w(f"| {name} | **{d['classification']}** | {n_pres}/8 | {n_brk}/8 |")
    w("")

    w("### Detail: parity(t) vs parity(inv(t)) for each trigram\n")
    w("| Trigram | Element | Parity | Reverse | Complement | Rev∘Comp |")
    w("|---------|---------|--------|---------|------------|----------|")
    for t in range(NUM_TRIG):
        p = parity3(t)
        checks = []
        for inv in [reverse3, complement3, rev_comp3]:
            pi = parity3(inv(t))
            checks.append(f"{pi} {'✓' if p == pi else '✗'}")
        w(f"| {TRIGRAM_NAMES[t]} ({fmt3(t)}) | {TRIGRAM_ELEMENT[t]} | {p} | " + " | ".join(checks) + " |")
    w("")

    # Key finding: complement preserves parity
    w("### Key finding: complement preserves parity universally\n")
    w("Complement XOR mask = 111. Parity = b₀⊕b₁. Under XOR with 111:")
    w("b₀' = b₀⊕1, b₁' = b₁⊕1, so b₀'⊕b₁' = (b₀⊕1)⊕(b₁⊕1) = b₀⊕b₁. ✓\n")
    w("This means complement is **生-compatible** at the parity level: it preserves the")
    w("b₀⊕b₁ bit that separates {Earth,Metal} from {Wood,Fire,Water}.\n")

    w("Reverse swaps b₀↔b₂, changing parity to b₂⊕b₁, which ≠ b₀⊕b₁ in general.")
    w("Reverse is **mixed**: preserves parity for trigrams where b₀=b₂ (palindromes),")
    w("breaks it otherwise.\n")

    w("### Connection to 生/克 XOR masks\n")
    w("From wuxing findings:\n")
    w("- 生-exclusive masks {011, 100}: preserve b₀⊕b₁ parity")
    w("- 克-exclusive masks {010, 110}: break b₀⊕b₁ parity\n")
    w("**Complement (mask 111)** is in the *shared* mask set (used by both 生 and 克),")
    w("and it preserves parity. **Reverse (mask for b₀↔b₂ swap, not a single XOR mask)")
    w("is mixed — neither purely 生 nor 克 compatible.**\n")
    w("The involution-to-生克 mapping is not a clean dichotomy at the parity level.")
    w("Instead, complement is parity-preserving (生-compatible), while reverse and rev∘comp")
    w("are mixed. The semantic gap must arise from a deeper mechanism.\n")

    # ── C ──
    w("## C. Hexagram-Level: Does 五行 Structure Explain the Semantic Gap?\n")
    w("kwprobe found: reversal pairs mean similarity ~0.720, complement pairs ~0.680,")
    w("rev∘comp ~0.673 (baseline 0.683).\n")

    w("### Disruption metrics per involution\n")
    w("| Metric | reverse₆ | complement₆ | rev∘comp₆ |")
    w("|--------|----------|-------------|-----------|")
    metrics = [
        ('Pairs', 'n_pairs'),
        ('Parity Δ (lower)', 'parity_changes_lower'),
        ('Parity Δ (upper)', 'parity_changes_upper'),
        ('Element Δ (lower)', 'element_changes_lower'),
        ('Element Δ (upper)', 'element_changes_upper'),
        ('Element SET Δ', 'element_set_changes'),
        ('Relation Δ (exact)', 'relation_changes'),
        ('Relation Δ (比/生/克)', 'relation_class_changes'),
    ]
    for label, key in metrics:
        vals = []
        for name in ['reverse₆', 'complement₆', 'rev∘comp₆']:
            d = hex_data[name]
            v = d[key]
            n = d['n_pairs']
            if key == 'n_pairs':
                vals.append(str(v))
            else:
                vals.append(f"{v}/{n} ({100*v/n:.0f}%)")
        w(f"| {label} | " + " | ".join(vals) + " |")
    w("")

    w("### The critical metric: element SET preservation\n")
    w("Reversal swaps upper↔lower trigrams but keeps the same two elements present.")
    w("Complement changes each trigram to a different element (except Wood pairs).\n")
    sem_sims = {'reverse₆': 0.720, 'complement₆': 0.680, 'rev∘comp₆': 0.673}
    for name in ['reverse₆', 'complement₆', 'rev∘comp₆']:
        d = hex_data[name]
        n = d['n_pairs']
        pct = 100 * d['element_set_changes'] / n
        w(f"- **{name}**: element set changes in {d['element_set_changes']}/{n} ({pct:.0f}%) pairs → "
          f"semantic similarity {sem_sims[name]:.3f}")
    w("")

    # Rank order check with element set changes
    set_scores = {name: hex_data[name]['element_set_changes'] / hex_data[name]['n_pairs']
                  for name in ['reverse₆', 'complement₆', 'rev∘comp₆']}
    score_rank = sorted(set_scores, key=lambda k: set_scores[k])
    sim_rank = sorted(sem_sims, key=lambda k: -sem_sims[k])
    rank_match = score_rank == sim_rank

    w(f"**Element-set disruption rank:** {' < '.join(f'{n}({set_scores[n]:.3f})' for n in score_rank)}")
    w(f"**Similarity rank:** {' > '.join(f'{n}({sem_sims[n]:.3f})' for n in sim_rank)}")
    w(f"**Anti-correlation (more set-disruption → less similarity)?** "
      f"{'✓ YES' if rank_match else '✗ NO'}\n")

    # Also: relation class preservation
    class_scores = {name: hex_data[name]['relation_class_changes'] / hex_data[name]['n_pairs']
                    for name in ['reverse₆', 'complement₆', 'rev∘comp₆']}
    class_rank = sorted(class_scores, key=lambda k: class_scores[k])
    class_match = class_rank == sim_rank

    w("### Relation category (比/生/克) preservation\n")
    w("Reversal swaps the *direction* of 生/克 (e.g., 生体 ↔ 体生用) but preserves the")
    w("*category* (both are 生-type). This is a weaker disruption.\n")
    for name in ['reverse₆', 'complement₆', 'rev∘comp₆']:
        d = hex_data[name]
        n = d['n_pairs']
        exact = d['relation_changes']
        cat = d['relation_class_changes']
        w(f"- **{name}**: exact relation changes {exact}/{n} ({100*exact/n:.0f}%), "
          f"category changes {cat}/{n} ({100*cat/n:.0f}%)")
    w("")
    w(f"**Category disruption rank:** {' < '.join(f'{n}({class_scores[n]:.3f})' for n in class_rank)}")
    w(f"**Anti-correlation with similarity?** {'✓ YES' if class_match else '✗ NO'}\n")

    # Relation transition detail
    rels = ['比和', '生体', '克体', '体生用', '体克用']
    for name in ['reverse₆', 'complement₆', 'rev∘comp₆']:
        d = hex_data[name]
        w(f"### Relation transition matrix: {name} (n={d['n_pairs']})\n")
        w("| Original \\ Transformed | " + " | ".join(rels) + " |")
        w("|" + "----|" * (len(rels) + 1))
        for r1 in rels:
            row = []
            for r2 in rels:
                c = d['relation_transitions'].get((r1, r2), 0)
                row.append(f"**{c}**" if r1 == r2 else str(c))
            w(f"| {r1} | " + " | ".join(row) + " |")
        diag = sum(d['relation_transitions'].get((r, r), 0) for r in rels)
        w(f"\nDiagonal (preserved): {diag}/{d['n_pairs']} ({100*diag/d['n_pairs']:.0f}%)\n")

    # Reversal-specific analysis
    w("### Why reversal preserves meaning despite high positional disruption\n")
    d = hex_data['reverse₆']
    rev_details = d['pair_details']
    set_preserved = [p for p in rev_details if p['set_x'] == p['set_y']]
    set_changed = [p for p in rev_details if p['set_x'] != p['set_y']]
    w(f"Reversal pairs: {len(set_preserved)} preserve element set, {len(set_changed)} change it.\n")

    # For set-preserved: relation transitions
    if set_preserved:
        w("Among set-preserving reversal pairs, the relation transition pattern:")
        rev_pres_trans = Counter()
        for p in set_preserved:
            rev_pres_trans[(RELATION_CLASS[p['rel_x']], RELATION_CLASS[p['rel_y']])] += 1
        for (c1, c2), count in sorted(rev_pres_trans.items(), key=lambda x: -x[1]):
            w(f"  {c1} → {c2}: {count}")
        w("")

    w("Reversal = 'visual flip' of the hexagram. While it changes trigrams (reverse₃ applied")
    w("to each), 6/28 pairs preserve the element set and all set-preserving pairs preserve")
    w("the 比/生/克 category. The Tuan treats reversed hexagrams as related perspectives.\n")

    w("Complement = all lines flipped. New elements in most pairs, but the 比/生/克 category")
    w("is **always preserved** (0% category disruption — complement is an anti-automorphism")
    w("of the 五行 graph). Despite this, the Tuan sees different situations.\n")

    # ── D ──
    w("## D. Wood's Special Status\n")

    w("### Element preservation under each involution\n")
    for name in ['reverse', 'complement', 'rev∘comp']:
        d = closure_data[name]
        w(f"**{name}:**\n")
        w("| Element | Size | Preserved | Broken to |")
        w("|---------|------|-----------|-----------|")
        for elem in ELEMENTS:
            sz = d['total'][elem]
            pres = d['preserved'].get(elem, 0)
            broken = d['broken_to'].get(elem, {})
            broken_str = ", ".join(f"{e}({c})" for e, c in broken.items()) if broken else "—"
            w(f"| {elem} ({ELEMENT_ZH[elem]}) | {sz} | {pres}/{sz} | {broken_str} |")
        w("")

    w("### Element closure under complement\n")
    w("| Element | Trigrams | Complement → | Elements | Closed? |")
    w("|---------|---------|-------------|----------|---------|")
    for elem in ELEMENTS:
        trigs = ELEM_TRIGRAMS[elem]
        ctrig = [complement3(t) for t in trigs]
        celems = [TRIGRAM_ELEMENT[c] for c in ctrig]
        closed = all(e == elem for e in celems)
        w(f"| {elem} | {', '.join(TRIGRAM_NAMES[t] for t in trigs)} | "
          f"{', '.join(TRIGRAM_NAMES[c] for c in ctrig)} | "
          f"{', '.join(celems)} | {'✓' if closed else '✗'} |")
    w("")

    w("**Wood is the unique element closed under complement.** The complement permutation on elements:")
    w("- Earth ↔ Metal (swap)")
    w("- Fire ↔ Water (swap)")
    w("- Wood → Wood (fixed)\n")

    w("### Wood as the 生-cycle hinge\n")
    w("The 生 cycle: Wood → Fire → Earth → Metal → Water → Wood")
    w("")
    w("Under complement, the cycle undergoes two transpositions: Earth↔Metal, Fire↔Water.")
    w("Applied to the cycle order:")
    w("```")
    w("Original: Wood → Fire  → Earth → Metal → Water → Wood")
    w("Compl'd:  Wood → Water → Metal → Earth → Fire  → Wood")
    w("```")
    w("The complemented cycle = the original cycle reversed (克 direction).")
    w("**Complement maps the 生 cycle to the 克 cycle.** Wood is the hinge: the fixed")
    w("point of complement, connecting the two directions of the cycle.\n")

    # Verify: complement permutation π conjugates σ (生) to σ⁻¹ (counter-生)
    # π = (Earth Metal)(Fire Water)(Wood)
    # σ = the 生 cycle permutation: Wood→Fire→Earth→Metal→Water→Wood
    # Claim: π∘σ∘π⁻¹ = σ⁻¹
    comp_perm = {'Earth': 'Metal', 'Metal': 'Earth', 'Fire': 'Water', 'Water': 'Fire', 'Wood': 'Wood'}
    all_match = True
    w("**Verification: π∘σ∘π⁻¹ = σ⁻¹?** (π = complement perm, σ = 生 cycle)\n")
    # σ⁻¹: reverse of 生 cycle
    sheng_inv = {v: k for k, v in SHENG_MAP.items()}  # counter-生
    for elem in ELEMENTS:
        # π⁻¹(elem) = comp_perm (since π is an involution, π⁻¹ = π)
        pi_inv_elem = comp_perm[elem]
        sigma_of_that = SHENG_MAP[pi_inv_elem]
        pi_of_that = comp_perm[sigma_of_that]
        sigma_inv_elem = sheng_inv[elem]
        match = pi_of_that == sigma_inv_elem
        w(f"- {elem}: π∘σ∘π⁻¹({elem}) = π(σ({comp_perm[elem]})) = π({sigma_of_that}) = "
          f"{pi_of_that} {'=' if match else '≠'} σ⁻¹({elem}) = {sigma_inv_elem} {'✓' if match else '✗'}")
        if not match:
            all_match = False
    w(f"\n**Complement is an anti-automorphism of the 生 cycle?** {'✓ YES' if all_match else '✗ NO'}\n")
    w("This means complement reverses all directed 生-edges: if A生B, then π(B)生π(A).")
    w("Equivalently, complement swaps 生体↔体生用 and 克体↔体克用, while preserving 比和.")
    w("The *category* (比/生/克) is invariant — only the direction within each category reverses.\n")
    w("This explains the complement₆ transition matrix: 0% category changes, but 生体↔体生用")
    w("and 克体↔体克用 swap perfectly.\n")

    w("### Structural role summary\n")
    w("| Property | Wood | Earth/Metal | Fire/Water |")
    w("|----------|------|-------------|------------|")
    w("| Complement closure | ✓ Fixed | ✗ Swap | ✗ Swap |")
    w("| Parity | Odd (1) | Even (0) | Odd (1) |")
    w("| 生-cycle role | Hinge (start/end) | Middle | Middle |")
    w("| Trigram geometry | Body diagonal | Edge pair | Singletons |")
    w("| Basin intrusion | Both fixed-point basins | Within respective basin | Cycle basin only |")
    w("")

    # ── E ──
    w("## E. The 1.50/2.25 Bit Prediction\n")

    w("Two related quantities:\n")
    w("1. **MI(五行, complement_pair_partition)** — how much does knowing the pair {t, comp(t)}")
    w("   tell you about element? This is the 1.50 from the wuxing MI matrix.")
    w("2. **MI(五行, complement_function)** — how much does element(comp(t)) tell you about")
    w("   element(t)? This is potentially different.\n")

    # Complement pair partition
    cmi = comp_pair_mi
    w("### 1. Complement pair partition\n")
    w(f"H(五行) = {cmi['h_wuxing']:.4f} bits")
    w(f"H(五行 | complement_pair) = {cmi['h_conditional']:.4f} bits")
    w(f"MI(五行, complement_pair) = {cmi['mi']:.4f} bits")
    w(f"Fraction preserved: {cmi['mi']/cmi['h_wuxing']:.1%}\n")

    w("Pair decomposition:\n")
    w("| Pair | Trigrams | Elements | H(五行 | pair) |")
    w("|------|---------|----------|---------------|")
    for pid, (t1, t2) in enumerate(cmi['pairs']):
        e1, e2 = TRIGRAM_ELEMENT[t1], TRIGRAM_ELEMENT[t2]
        h = 0 if e1 == e2 else 1.0
        w(f"| {pid} | {TRIGRAM_NAMES[t1]}, {TRIGRAM_NAMES[t2]} | {e1}, {e2} | {h:.1f} |")
    w("")
    w("Three of four pairs have distinct elements (H=1 bit each). One pair (Wood) has")
    w(f"identical elements (H=0). Weighted: H(五行|pair) = 3/4 × 1 + 1/4 × 0 = {cmi['h_conditional']:.4f}\n")

    # Complement function
    comp_func = func_mi['complement']
    w("### 2. Complement function (element → element)\n")
    w(f"H(五行 | element(comp(t))) = {comp_func['h_conditional']:.4f} bits")
    w(f"MI = {comp_func['mi']:.4f} bits\n")
    w("The complement function is a **deterministic permutation** on elements:")
    w("Earth↔Metal, Fire↔Water, Wood→Wood. Knowing element(comp(t)) determines element(t)")
    w("with zero ambiguity. Hence MI = H(五行) = 2.25.\n")
    w("**The 1.50 vs 2.25 gap:** the pair partition tells you WHICH pair but not WHICH")
    w("member you are. The complement function tells you exactly which element your partner")
    w("has, which determines your element. The 0.75-bit gap is the within-pair identity.\n")

    # Is the 0.75 the cosmological bit?
    w("### 3. Is the missing 0.75 bits the cosmological choice?\n")
    w("The three-layer decomposition of H(五行) = 2.25 bits:")
    w("- Layer 1: b₀⊕b₁ parity = 1.000 bits")
    w("- Layer 2: b₀ within even coset = 0.750 bits (Earth vs Metal)")
    w("- Layer 3: complement pair choice in odd coset = 0.500 bits (cosmological)\n")
    w(f"Lost information: H(五行|pair) = {cmi['h_conditional']:.4f} bits")
    w("")
    w("This 0.750 bits is NOT just the cosmological Layer 3 (0.500 bits). It decomposes as:")
    w("- Earth/Metal ambiguity in pair {Kun,Qian}: 0.25 bits")
    w("- Earth/Metal ambiguity in pair {Dui,Gen}: 0.25 bits")
    w("- Fire/Water ambiguity in pair {Kan,Li}: 0.25 bits")
    w("Total: 0.75 bits\n")
    w("The lost information spans **both** Layer 2 (Earth vs Metal, two occurrences)")
    w("**and** part of the structure that Layer 3 encodes (Fire vs Water).")
    w("It is exactly **Layer 2** in the information-theoretic sense:")
    w("complement pairs preserve Layer 1 (parity — each pair is parity-pure) and Layer 3")
    w("(which complement pair in the odd coset — {Zhen,Xun}=Wood vs {Kan,Li}=Fire/Water),")
    w("but lose Layer 2 (the within-pair identity).\n")

    # Verification: what does the pair partition capture?
    w("**What the pair partition captures (1.500 bits):**")
    w("- Layer 1 (parity): 1.000 bits — each pair is parity-pure ✓")
    w("- Within parity-1: {Zhen,Xun}=Wood vs {Kan,Li}={Fire,Water} = 0.500 bits ✓")
    w("- Total: 1.500 bits ✓\n")
    w("**What it loses (0.750 bits):**")
    w("- Within parity-0: Earth vs Metal (0.750 bits, covering 4 trigrams in 2 pairs)")
    w("- Within parity-1, pair {Kan,Li}: Fire vs Water (implicit in the 0.750)\n")
    w("The within-pair ambiguity accounts for all lost information. The cosmological")
    w("choice (Layer 3 = 0.500 bits) is PRESERVED: the pair partition distinguishes")
    w("{Zhen,Xun} from {Kan,Li}, which is exactly the cosmological input.\n")

    # Comparison across involutions
    w("### 4. Comparison across all involutions (pair partition MI)\n")
    w("| Involution | MI(五行, pair partition) | H(五行|pair) | Pairs |")
    w("|-----------|------------------------|------------|-------|")
    for label in ['complement', 'reverse', 'rev∘comp']:
        info = pair_mi[label]
        pair_desc = ", ".join(f"{{{', '.join(TRIGRAM_NAMES[t] for t in p)}}}" for p in info['pairs'])
        w(f"| {label} | {info['mi']:.4f} | {info['h_conditional']:.4f} | {pair_desc} |")
    w("")

    w("| Involution | MI(五行, partner_element) | H(五行|partner_elem) |")
    w("|-----------|-------------------------|---------------------|")
    for label in ['complement', 'reverse', 'rev∘comp']:
        info = func_mi[label]
        w(f"| {label} | {info['mi']:.4f} | {info['h_conditional']:.4f} |")
    w("")

    # ── Synthesis ──
    w("## Synthesis\n")

    w("### 1. Complement preserves parity — hypothesis corrected\n")
    w("The initial hypothesis was that complement, being 克-associated, would break parity.")
    w("In fact, complement **preserves** b₀⊕b₁ parity universally: XOR with 111 flips both")
    w("b₀ and b₁, so their XOR is unchanged. Complement belongs to the *shared* XOR mask")
    w("vocabulary (used by both 生 and 克), not the 克-exclusive set.\n")
    w("The 克-exclusive masks {010, 110} break parity by flipping exactly one of {b₀, b₁}.")
    w("Complement flips both, canceling the effect. Reverse replaces b₀ with b₂ in the")
    w("parity calculation — mixed behavior depending on whether b₀ = b₂.\n")

    w("### 2. Complement is an anti-automorphism of 五行 — the deepest structural finding\n")
    w("The complement permutation π = (Earth↔Metal)(Fire↔Water)(Wood) conjugates the 生 cycle")
    w("to its inverse: π∘σ∘π⁻¹ = σ⁻¹. This means complement reverses all directed edges in the")
    w("五行 graph. Consequences:\n")
    w("- 比和 → 比和 (identity preserved)")
    w("- 生体 ↔ 体生用 (direction of generation reverses)")
    w("- 克体 ↔ 体克用 (direction of overcoming reverses)")
    w("- **The 比/生/克 category is always preserved** (0% category disruption at hex level)\n")
    w("This is why the complement₆ transition matrix is perfectly block-diagonal: every pair")
    w("stays within its 比/生/克 class. The complement swaps 'who generates whom' but preserves")
    w("*whether* generation or overcoming is occurring.\n")

    w("### 3. The semantic gap has a layered explanation\n")
    w("The three involutions create a hierarchy of 五行 disruption:\n")
    w("| Layer | reverse₆ | complement₆ | rev∘comp₆ |")
    w("|-------|----------|-------------|-----------|")
    w("| 比/生/克 category | 50% changed | **0% changed** | 50% changed |")
    w(f"| Element vocabulary | {hex_data['reverse₆']['element_set_changes']}/{hex_data['reverse₆']['n_pairs']} ({100*hex_data['reverse₆']['element_set_changes']/hex_data['reverse₆']['n_pairs']:.0f}%) changed | "
      f"{hex_data['complement₆']['element_set_changes']}/{hex_data['complement₆']['n_pairs']} ({100*hex_data['complement₆']['element_set_changes']/hex_data['complement₆']['n_pairs']:.0f}%) changed | "
      f"{hex_data['rev∘comp₆']['element_set_changes']}/{hex_data['rev∘comp₆']['n_pairs']} (100%) changed |")
    w("| Semantic similarity | 0.720 | 0.680 | 0.673 |")
    w("")
    w("The semantic similarity does NOT track 比/生/克 preservation (complement has 0% disruption")
    w("but only middle similarity). Nor does it purely track element-set changes (reverse and")
    w("complement are nearly equal at ~79%). The gap arises from what reversal uniquely preserves:\n")
    w("**Reversal produces the 'visual flip'** — the hexagram turned upside down. While this")
    w("also reverses bits within each trigram (not just swapping positions), it preserves the")
    w("hexagram's 'shape.' The Tuan sees structurally related situations. Complement preserves")
    w("the abstract interaction category but changes all concrete elements — structurally")
    w("analogous but elementally different situations. Rev∘comp changes both.\n")
    w("The semantic hierarchy: **visual flip** (0.720) > **category-preserving element change**")
    w("(0.680) > **full disruption** (0.673). The gap between reverse and complement is the")
    w("difference between concrete similarity and abstract structural analogy.\n")

    w("### 4. Wood is the complement fixed point and cycle conjugator\n")
    w("Wood is the unique element closed under complement. The complement permutation maps the 生")
    w("cycle to its inverse, with Wood as the fixed point. This is the algebraic expression of")
    w("Wood's role as universal intruder: it bridges 生 and 克 because it is the hinge where")
    w("the direction of causation reverses. Wood creates 克 friction in every convergence path")
    w("because it connects the two directions of the cycle.\n")

    w("### 5. The complement pair captures 1.500/2.250 bits — cosmological choice preserved\n")
    w("MI(五行, complement_pair_partition) = 1.500 bits (67%). The 0.750 bits lost is the")
    w("within-pair element identity. The cosmological choice (Layer 3 = 0.500 bits) is")
    w("PRESERVED: complement pairs distinguish {Zhen,Xun}=Wood from {Kan,Li}={Fire,Water}.")
    w("The complement function itself preserves ALL 五行 information (MI = 2.250): it is a")
    w("deterministic permutation on elements. The 1.500 of the pair partition reflects the")
    w("loss of *which member you are*, not any structural degradation.\n")

    w("### 6. Summary of corrections to initial hypotheses\n")
    w("| Hypothesis | Result |")
    w("|-----------|--------|")
    w("| Complement breaks parity | **Wrong.** Complement preserves parity (mask 111 flips b₀ and b₁ together) |")
    w("| Complement is 克-compatible | **Partially wrong.** At parity level, complement is in the shared vocabulary. As a permutation on elements, complement is an anti-automorphism (reverses both 生 and 克 directions) |")
    w("| 五行 disruption rank-orders with semantic similarity | **Wrong for simple metrics.** Category disruption anti-correlates with the gap. The semantic gap tracks concrete trigram identity, not abstract relational structure |")
    w("| Missing 33% = cosmological choice | **Wrong.** Missing 0.750 bits = within-pair ambiguity (Layer 2), not Layer 3. The cosmological choice is preserved by complement pairs |")
    w("| Complement predicts 67% of 五行 | **Correct as pair partition.** But as a function, complement predicts 100% of 五行 — it's a perfect permutation |")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PROBE 5: S₄ × 五行 — INVOLUTIONS, PARITY, AND THE SEMANTIC GAP")
    print("=" * 70)

    # A
    print("\n── A. V₄ Orbits ──")
    orbit_data = analyze_orbits()
    for o in orbit_data:
        print(f"  Orbit: {o['names']}")
        print(f"    Parities: {o['parities']}, Elements: {o['unique_elements']}, "
              f"Constant: {o['parity_constant']}")

    # B
    print("\n── B. Parity Preservation ──")
    parity_data = analyze_parity_preservation()
    for name, d in parity_data.items():
        print(f"  {name}: {d['classification']} "
              f"(preserves {len(d['preserves'])}/8, breaks {len(d['breaks'])}/8)")

    # C
    print("\n── C. Hexagram-Level Disruption ──")
    hex_data = analyze_hex_involutions()
    for name, d in hex_data.items():
        n = d['n_pairs']
        print(f"  {name}: {n} pairs")
        print(f"    element set changes: {d['element_set_changes']}/{n} ({100*d['element_set_changes']/n:.0f}%)")
        print(f"    relation class changes: {d['relation_class_changes']}/{n} ({100*d['relation_class_changes']/n:.0f}%)")

    # D
    print("\n── D. Element Closure ──")
    closure_data = analyze_element_closure()
    for name, d in closure_data.items():
        print(f"  {name}:")
        for elem in ELEMENTS:
            pres = d['preserved'].get(elem, 0)
            tot = d['total'][elem]
            print(f"    {elem}: {pres}/{tot} preserved")

    # E
    print("\n── E. Information Theory ──")
    comp_pair_mi = analyze_complement_pair_mi()
    print(f"  Complement pair partition: MI={comp_pair_mi['mi']:.4f}, "
          f"H(W|pair)={comp_pair_mi['h_conditional']:.4f}")

    func_mi = {}
    pair_mi = {}
    for label, inv in [('complement', complement3), ('reverse', reverse3), ('rev∘comp', rev_comp3)]:
        func_mi[label] = analyze_function_mi(inv, label)
        pair_mi[label] = analyze_pair_partition_mi(inv, label)
        print(f"  {label}: func MI={func_mi[label]['mi']:.4f}, pair MI={pair_mi[label]['mi']:.4f}")

    # Write markdown
    md = format_results(orbit_data, parity_data, hex_data, closure_data,
                        comp_pair_mi, func_mi, pair_mi)
    out_path = Path(__file__).parent / "probe5_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


if __name__ == '__main__':
    main()
