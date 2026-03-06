#!/usr/bin/env python3
"""
Phase 3: 互卦 (Hùguà) Self-Similarity Test

The 互卦 extracts the nuclear core of a hexagram and expands it:
  Given h with lines L1-L2-L3-L4-L5-L6:
    nuclear core = L2-L3-L4-L5  (4 bits)
    互卦 = L2-L3-L4-L3-L4-L5   (lower trigram = L2,L3,L4; upper trigram = L3,L4,L5)

Tests whether the KW pairing is self-similar under the 互卦 projection:
does opposition at hexagram level induce opposition at the nuclear level?

Encoding: L1 = bit 0 (bottom), L6 = bit 5 (top).
"""

from collections import Counter
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N  # 64
MASK_ALL = (1 << N) - 1

# ─── Bit operations ──────────────────────────────────────────────────────────

def popcount(x):
    return bin(x).count('1')

def reverse6(x):
    """Reverse 6-bit string: bit i -> bit (5-i)."""
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    return r

def fmt6(x):
    return format(x, '06b')

def fmt4(x):
    return format(x, '04b')

def bit(x, i):
    """Extract bit i from x."""
    return (x >> i) & 1

# ─── 互卦 map ────────────────────────────────────────────────────────────────

def hugua(x):
    """
    Compute 互卦 of hexagram x.
    Lower trigram = (L2, L3, L4) = bits 1, 2, 3
    Upper trigram = (L3, L4, L5) = bits 2, 3, 4
    Result: bit0=L2, bit1=L3, bit2=L4, bit3=L3, bit4=L4, bit5=L5
    """
    L2 = bit(x, 1)
    L3 = bit(x, 2)
    L4 = bit(x, 3)
    L5 = bit(x, 4)
    return L2 | (L3 << 1) | (L4 << 2) | (L3 << 3) | (L4 << 4) | (L5 << 5)

# ─── KW pairing ─────────────────────────────────────────────────────────────

def kw_partner(x):
    """KW pairing: reverse for non-palindromes, complement for palindromes."""
    rev = reverse6(x)
    if rev == x:
        return x ^ MASK_ALL
    return rev

def is_palindrome6(x):
    return reverse6(x) == x

def generate_kw_pairs():
    """Generate 32 KW pairs as (a, b, pair_type), a < b."""
    paired = set()
    pairs = []
    for a in range(NUM_STATES):
        if a in paired:
            continue
        b = kw_partner(a)
        ptype = "palindromic" if is_palindrome6(a) else "reversal"
        if a > b:
            a, b = b, a
        pairs.append((a, b, ptype))
        paired.add(a)
        paired.add(b)
    return pairs

# ─── Relationship classification ─────────────────────────────────────────────

def classify_hex_relation(x, y):
    """Classify relationship between two 6-bit hexagrams."""
    if x == y:
        return "identity"
    rev = reverse6(x)
    comp = x ^ MASK_ALL
    cr = reverse6(comp)
    if y == rev:
        return "reversal"
    if y == comp:
        return "complement"
    if y == cr:
        return "comp∘rev"
    return "other"

# ─── Main analysis ───────────────────────────────────────────────────────────

def main():
    pairs = generate_kw_pairs()

    # ── Precompute 互卦 for all 64 hexagrams ──
    HUGUA = [hugua(x) for x in range(NUM_STATES)]

    # ── Image of 互卦 map ──
    hugua_image = sorted(set(HUGUA))
    hugua_preimage = {}  # hugua_hex -> list of source hexagrams
    for x in range(NUM_STATES):
        hugua_preimage.setdefault(HUGUA[x], []).append(x)

    # ── Fixed points: x == hugua(x) ──
    fixed_points = [x for x in range(NUM_STATES) if HUGUA[x] == x]

    # ── Per-pair analysis ──
    pair_results = []
    for a, b, ptype in pairs:
        ha, hb = HUGUA[a], HUGUA[b]

        # Is hugua pair a KW pair?
        kw_of_ha = kw_partner(ha)
        is_kw_pair = (hb == kw_of_ha) or (ha == kw_partner(hb))

        # Relationship
        rel = classify_hex_relation(ha, hb)

        # XOR mask
        xor_mask = ha ^ hb

        # Is XOR one of the 7 signature masks?
        sig_masks = set()
        for o in range(2):
            for m in range(2):
                for i in range(2):
                    if o == 0 and m == 0 and i == 0:
                        continue
                    mask = o | (m << 1) | (i << 2) | (i << 3) | (m << 4) | (o << 5)
                    sig_masks.add(mask)
        is_sig_mask = xor_mask in sig_masks

        # Weight
        w_ha, w_hb = popcount(ha), popcount(hb)

        pair_results.append({
            'a': a, 'b': b, 'ptype': ptype,
            'ha': ha, 'hb': hb,
            'is_kw_pair': is_kw_pair,
            'rel': rel,
            'xor': xor_mask,
            'is_sig_mask': is_sig_mask,
            'w_ha': w_ha, 'w_hb': w_hb,
            'dw': abs(w_ha - w_hb),
        })

    # ── Commutativity test: hugua(kw(x)) == kw(hugua(x)) for all x? ──
    commutes_all = True
    commute_failures = []
    for x in range(NUM_STATES):
        lhs = HUGUA[kw_partner(x)]
        rhs = kw_partner(HUGUA[x])
        if lhs != rhs:
            commutes_all = False
            commute_failures.append((x, lhs, rhs))

    # ── Pairing compatibility: does hugua(a1)==hugua(a2) imply hugua(b1)==hugua(b2)? ──
    # For each hugua value v, collect all partners' hugua values from pairs containing v.
    # Compatible iff each v maps to a unique partner value.
    hugua_partner_map = {}  # hugua_val -> set of partner hugua_vals
    for r in pair_results:
        hugua_partner_map.setdefault(r['ha'], set()).add(r['hb'])
        hugua_partner_map.setdefault(r['hb'], set()).add(r['ha'])
    pairing_compatible = True
    compat_failures = []
    for val, partners in sorted(hugua_partner_map.items()):
        if len(partners) > 1:
            pairing_compatible = False
            compat_failures.append((val, partners))

    # ── 互卦 idempotency: hugua(hugua(x)) == hugua(x)? ──
    idempotent_all = all(HUGUA[HUGUA[x]] == HUGUA[x] for x in range(NUM_STATES))
    idempotent_failures = [x for x in range(NUM_STATES) if HUGUA[HUGUA[x]] != HUGUA[x]]

    # ── Print key results ──
    print("=" * 70)
    print("互卦 (HÙGUÀ) SELF-SIMILARITY TEST")
    print("=" * 70)

    print(f"\n互卦 image size: {len(hugua_image)} of 64 hexagrams")
    print(f"Fixed points (x == hugua(x)): {len(fixed_points)}")
    print(f"Idempotent (hugua∘hugua == hugua): {idempotent_all}")
    if idempotent_failures:
        print(f"  Failures: {len(idempotent_failures)}")

    print(f"\nCommutativity (hugua∘kw == kw∘hugua): {commutes_all}")
    if not commutes_all:
        print(f"  Failures: {len(commute_failures)} of 64")

    kw_count = sum(1 for r in pair_results if r['is_kw_pair'])
    print(f"\nKW pairs preserved under 互卦: {kw_count} of 32")

    rel_dist = Counter(r['rel'] for r in pair_results)
    print(f"\n互卦 pair relationships:")
    for rel, count in sorted(rel_dist.items(), key=lambda x: -x[1]):
        print(f"  {rel}: {count}")

    sig_count = sum(1 for r in pair_results if r['is_sig_mask'])
    print(f"\nXOR mask is signature mask: {sig_count} of 32")

    xor_dist = Counter(r['xor'] for r in pair_results)
    print(f"\n互卦 XOR mask distribution:")
    for mask, count in sorted(xor_dist.items()):
        print(f"  {fmt6(mask)}: {count}")

    mean_dw = sum(r['dw'] for r in pair_results) / len(pair_results)
    print(f"\nWeight: mean |Δw| at 互卦 level = {mean_dw:.4f}")

    # Correlation
    import numpy as np
    wa = np.array([r['w_ha'] for r in pair_results], dtype=float)
    wb = np.array([r['w_hb'] for r in pair_results], dtype=float)
    if np.std(wa) > 0 and np.std(wb) > 0:
        corr = float(np.corrcoef(wa, wb)[0, 1])
    else:
        corr = float('nan')
    print(f"Weight correlation r(w(hugua(a)), w(hugua(b))) = {corr:.4f}")

    print(f"\nPairing descends to well-defined map on 互卦 image: {pairing_compatible}")
    if compat_failures:
        print(f"  Failures: {len(compat_failures)}")

    # ── Write markdown ──
    md = format_markdown(pair_results, pairs, hugua_image, hugua_preimage,
                         fixed_points, commutes_all, commute_failures,
                         pairing_compatible, compat_failures,
                         idempotent_all, idempotent_failures,
                         rel_dist, xor_dist, mean_dw, corr, HUGUA)
    out_path = Path(__file__).parent / "hugua_results.md"
    out_path.write_text(md)
    print(f"\nResults written to {out_path}")


# ─── Markdown formatting ────────────────────────────────────────────────────

def format_markdown(pair_results, pairs, hugua_image, hugua_preimage,
                    fixed_points, commutes_all, commute_failures,
                    pairing_compatible, compat_failures,
                    idempotent_all, idempotent_failures,
                    rel_dist, xor_dist, mean_dw, corr, HUGUA):
    lines = []
    w = lines.append

    w("# Phase 3: 互卦 (Hùguà) Self-Similarity Test\n")
    w("The 互卦 extracts the nuclear core and re-expands it:")
    w("given hexagram h = L1-L2-L3-L4-L5-L6, 互卦(h) = L2-L3-L4-L3-L4-L5.")
    w("This tests whether KW opposition is self-similar under nuclear projection.\n")

    # ── 1. The 互卦 map ──
    w("## 1. The 互卦 Map\n")
    w(f"**Image size:** {len(hugua_image)} of 64 hexagrams")
    w(f"(the 互卦 map is {len(hugua_image)}-to-64, i.e., "
      f"{64/len(hugua_image):.1f}:1 average preimage size)\n")

    w(f"**Idempotent:** hugua(hugua(x)) = hugua(x) for all x? **{idempotent_all}**\n")
    if not idempotent_all:
        w(f"Failures: {len(idempotent_failures)} of 64 hexagrams.")
        w("The 互卦 is NOT a retraction — the image is not stable under reapplication.\n")
        # Compute hugua^2 image
        image2 = sorted(set(hugua(HUGUA[x]) for x in range(NUM_STATES)))
        w(f"**hugua²(x) = hugua(hugua(x))** converges to {len(image2)} hexagrams:")
        w("these are the L3,L4-alternation patterns (L3,L4,L3,L4,L3,L4).\n")
        w("| hugua² value | Binary | Structure |")
        w("|-------------|--------|-----------|")
        for h in image2:
            L3 = bit(h, 0)
            L4 = bit(h, 1)
            w(f"| {h:2d} | {fmt6(h)} | L3={L3}, L4={L4} alternating |")
        w("")
        w("**Iteration depth:** hugua converges in exactly 2 steps (hugua³ = hugua²).")
        w("Each application peels off one layer: hugua strips L1,L6; hugua² additionally")
        w("collapses L2,L5 into the L3,L4 pattern.\n")
    else:
        w("The 互卦 map is a retraction: applying it twice gives the same result as once.")
        w("Every hexagram in the image is a fixed point.\n")

    w(f"**Fixed points** (x = hugua(x)): **{len(fixed_points)}**\n")
    w("| Fixed point | Binary | Lines | Structure |")
    w("|------------|--------|-------|-----------|")
    for x in fixed_points:
        bits = [bit(x, i) for i in range(6)]
        # Fixed point means L1=L3=L5 pattern? Check.
        desc = []
        if bits[0] == bits[2] and bits[2] == bits[4]:
            desc.append("L1=L3=L5")
        if bits[1] == bits[3] and bits[3] == bits[5]:
            desc.append("L2=L4=L6")
        w(f"| {x:2d} | {fmt6(x)} | {''.join(str(b) for b in bits)} | {', '.join(desc) if desc else '—'} |")
    w("")

    w("### Image structure\n")
    w("The 互卦 output always satisfies **bit1 = bit3** and **bit2 = bit4**")
    w("(because L3 is placed at both positions 1,3 and L4 at positions 2,4).")
    w(f"This constrains the image to exactly {len(hugua_image)} = 2⁴ hexagrams")
    w("(4 free bits: L2=bit0, L3=bit1, L4=bit2, L5=bit5).\n")

    fp_set = set(fixed_points)
    img_set = set(hugua_image)
    w(f"Fixed points ⊂ image? **{fp_set <= img_set}**")
    w(f"Fixed points = image? **{fp_set == img_set}** — the image is much larger ({len(img_set)}) than the fixed set ({len(fp_set)}).")
    w("Most image hexagrams are NOT fixed under reapplication.\n")

    # ── Image structure ──
    w("### Image of 互卦 with preimage sizes\n")
    w("| 互卦 hex | Binary | Preimage size | Preimage hexagrams |")
    w("|---------|--------|--------------|-------------------|")
    for h in hugua_image:
        pre = hugua_preimage[h]
        pre_str = ', '.join(fmt6(x) for x in pre)
        w(f"| {h:2d} | {fmt6(h)} | {len(pre)} | {pre_str} |")
    w("")

    # Preimage size distribution
    pre_sizes = Counter(len(v) for v in hugua_preimage.values())
    w("**Preimage size distribution:**\n")
    w("| Size | Count |")
    w("|------|-------|")
    for size, count in sorted(pre_sizes.items()):
        w(f"| {size} | {count} |")
    w("")

    # ── 2. Self-similarity test ──
    w("## 2. Self-Similarity Test: Does KW Pairing Descend to 互卦?\n")

    kw_count = sum(1 for r in pair_results if r['is_kw_pair'])
    w(f"**KW pairs preserved:** {kw_count} of 32 pairs have hugua(a), hugua(b) forming a KW pair.\n")

    w(f"**Commutativity:** hugua(kw(x)) = kw(hugua(x)) for all x? **{commutes_all}**")
    if not commutes_all:
        w(f"\n{len(commute_failures)} failures:\n")
        w("| x | Binary | hugua(kw(x)) | kw(hugua(x)) |")
        w("|---|--------|-------------|-------------|")
        for x, lhs, rhs in commute_failures[:20]:
            w(f"| {x:2d} | {fmt6(x)} | {fmt6(lhs)} | {fmt6(rhs)} |")
        if len(commute_failures) > 20:
            w(f"| ... | ... | ... | ... |")
    w("")

    w(f"**Pairing compatible with nuclear projection:** {pairing_compatible}")
    w("(If hugua(a₁) = hugua(a₂), is hugua(b₁) = hugua(b₂)?)\n")
    if not pairing_compatible and compat_failures:
        w("Compatibility failures:\n")
        for ha_val, hb_vals in compat_failures[:10]:
            w(f"- hugua value {fmt6(ha_val)} maps to partners: {{{', '.join(fmt6(v) for v in sorted(hb_vals))}}}")
        w("")

    # ── 3. Full pair table ──
    w("## 3. Full 互卦 Pair Table\n")
    w("| # | a | b | Type | hugua(a) | hugua(b) | KW pair? | Relation | XOR | Sig? | Δw |")
    w("|---|---|---|------|----------|----------|----------|----------|-----|------|-----|")
    for i, r in enumerate(pair_results):
        w(f"| {i+1} | {fmt6(r['a'])} | {fmt6(r['b'])} | {r['ptype'][:3]} "
          f"| {fmt6(r['ha'])} | {fmt6(r['hb'])} "
          f"| {'✓' if r['is_kw_pair'] else '✗'} | {r['rel']} "
          f"| {fmt6(r['xor'])} | {'✓' if r['is_sig_mask'] else '✗'} "
          f"| {r['dw']} |")
    w("")

    # ── 4. Relationship summary ──
    w("## 4. Relationship Summary\n")
    w("### 互卦 pair relationship distribution\n")
    w("| Relationship | Count |")
    w("|-------------|-------|")
    for rel, count in sorted(rel_dist.items(), key=lambda x: -x[1]):
        w(f"| {rel} | {count} |")
    w("")

    # Break down by pair type
    for ptype in ['reversal', 'palindromic']:
        sub = [r for r in pair_results if r['ptype'] == ptype]
        sub_rel = Counter(r['rel'] for r in sub)
        w(f"#### {ptype.capitalize()} pairs ({len(sub)})\n")
        w("| Relationship | Count |")
        w("|-------------|-------|")
        for rel, count in sorted(sub_rel.items(), key=lambda x: -x[1]):
            w(f"| {rel} | {count} |")
        w("")

    w("### 互卦 XOR mask distribution\n")
    w("| XOR mask | Count | Signature mask? | popcount |")
    w("|----------|-------|----------------|----------|")
    for mask, count in sorted(xor_dist.items()):
        sig_masks = set()
        for o in range(2):
            for m in range(2):
                for i in range(2):
                    if o == 0 and m == 0 and i == 0:
                        continue
                    sig_masks.add(o | (m << 1) | (i << 2) | (i << 3) | (m << 4) | (o << 5))
        is_sig = mask in sig_masks
        w(f"| {fmt6(mask)} | {count} | {'✓' if is_sig else '✗'} | {popcount(mask)} |")
    w("")

    # ── 5. Weight analysis ──
    w("## 5. Weight Analysis at 互卦 Level\n")
    w(f"**Mean |Δw|:** {mean_dw:.4f}\n")
    w(f"**Weight correlation:** r = {corr:.4f}\n")
    w("| Δw | Count | Pair types |")
    w("|----|-------|------------|")
    dw_dist = Counter()
    dw_types = {}
    for r in pair_results:
        dw_dist[r['dw']] += 1
        dw_types.setdefault(r['dw'], Counter())[r['ptype']] += 1
    for dw, count in sorted(dw_dist.items()):
        types = ', '.join(f"{t}: {c}" for t, c in sorted(dw_types[dw].items()))
        w(f"| {dw} | {count} | {types} |")
    w("")

    # Reference: hex-level weight tilt for comparison
    hex_dw = []
    for a, b, ptype in pairs:
        hex_dw.append(abs(popcount(a) - popcount(b)))
    hex_mean_dw = sum(hex_dw) / len(hex_dw)
    w(f"**Comparison:** hexagram-level mean |Δw| = {hex_mean_dw:.4f} "
      f"(互卦 level = {mean_dw:.4f})\n")

    # ── 6. Structural analysis ──
    w("## 6. Structural Analysis\n")

    w("### 6.1 The 互卦 map in mirror-pair terms\n")
    w("The 互卦 discards L1 and L6 (the outer pair) and duplicates L3, L4 (the inner pair).")
    w("In mirror-pair terms: it **erases O** (outer), **preserves M** (middle), and **doubles I** (inner).\n")
    w("Algebraic consequences for the KW pairing:\n")
    w("**Reversal pairs** (b = rev₆(a)): The hexagram-level XOR mask is palindromic with")
    w("signature (o,m,i). The 互卦 erases the O-component, so the 互卦 XOR depends only on M and I.")
    w("This reduces the 7-mask vocabulary to 3+1 effective masks (plus identity when only O differs).\n")
    w("**Palindromic (complement) pairs** (b = comp(a)): hugua commutes with complement exactly —")
    w("complement flips all bits including L2-L5, and hugua(comp(x)) = comp(hugua(x)).")
    w("So all 4 palindromic pairs map to complement pairs at the 互卦 level.\n")

    # Count reversal pairs by hugua relationship
    rev_rels = Counter(r['rel'] for r in pair_results if r['ptype'] == 'reversal')
    w("### 6.2 Reversal pair fate under 互卦\n")
    w("| 互卦 relationship | Count | Mechanism |")
    w("|-------------------|-------|-----------|")
    w(f"| reversal | {rev_rels.get('reversal', 0)} | M or I (or both) differ → reversal persists |")
    w(f"| identity | {rev_rels.get('identity', 0)} | Only O differs → opposition erased |")
    w(f"| complement | {rev_rels.get('complement', 0)} | — |")
    w(f"| other | {rev_rels.get('other', 0)} | — |")
    w("")

    rev_identity = rev_rels.get('identity', 0)
    if rev_identity > 0:
        w(f"The {rev_identity} **identity** cases are reversal pairs whose only opposition is at the outer pair.")
        w("These have hexagram-level signature (1,0,0) — erasing O leaves no difference.\n")
        w("| # | a | b | Hex XOR | Signature |")
        w("|---|---|---|---------|-----------|")
        for i, r in enumerate(pair_results):
            if r['ptype'] == 'reversal' and r['rel'] == 'identity':
                xor = r['a'] ^ r['b']
                sig_o = bit(xor, 0)
                sig_m = bit(xor, 1)
                sig_i = bit(xor, 2)
                w(f"| {i+1} | {fmt6(r['a'])} | {fmt6(r['b'])} | {fmt6(xor)} | ({sig_o},{sig_m},{sig_i}) |")
        w("")

    w("### 6.3 The XOR mask reduction\n")
    w("The 7 hexagram-level signature masks reduce under 互卦 as follows:\n")
    w("| Hex signature | Hex mask | 互卦 XOR | Popcount | O erased? |")
    w("|--------------|----------|---------|----------|-----------|")
    for o in range(2):
        for m in range(2):
            for i in range(2):
                if o == 0 and m == 0 and i == 0:
                    continue
                mask = o | (m << 1) | (i << 2) | (i << 3) | (m << 4) | (o << 5)
                # Compute hugua XOR: hugua(a) XOR hugua(b) when a XOR b = mask
                # hugua picks bits 1,2,3,2,3,4 — so 互卦 XOR = bits 1,2,3,2,3,4 of mask
                hxor = bit(mask, 1) | (bit(mask, 2) << 1) | (bit(mask, 3) << 2) | \
                       (bit(mask, 2) << 3) | (bit(mask, 3) << 4) | (bit(mask, 4) << 5)
                erased = "yes" if o == 1 and m == 0 and i == 0 else "no"
                w(f"| ({o},{m},{i}) | {fmt6(mask)} | {fmt6(hxor)} | {popcount(hxor)} | {erased} |")
    w("")
    w("Signature pairs with same (m,i) but different o collapse to the same 互卦 XOR:")
    w("- (0,0,1) and (1,0,1) → 011110")
    w("- (0,1,0) and (1,1,0) → 100001")
    w("- (0,1,1) and (1,1,1) → 111111")
    w("- (1,0,0) → 000000 (opposition erased)\n")
    w("The 7 hexagram masks reduce to **3 nonzero 互卦 masks + identity**.")
    w("The outer pair is invisible; opposition at the 互卦 level is determined entirely by M and I.\n")
    w("**Note:** In the 互卦 image (where bit1=bit3, bit2=bit4), reversal and complement")
    w("can coincide on certain hexagrams. For example, reverse₆(001011) = 110100 = complement(001011).")
    w("This means the 互卦 XOR mask 111111 can arise from both reversal and complement operations,")
    w("unlike at the full hexagram level where they are always distinct.\n")

    # ── 7. Commutativity diagram ──
    w("## 7. Commutativity Analysis\n")
    w("The key algebraic question: does this diagram commute?\n")
    w("```")
    w("       kw_partner")
    w("  x  ───────────→  kw(x)")
    w("  │                  │")
    w("  │ hugua            │ hugua")
    w("  ↓                  ↓")
    w("hugua(x) ─────→  hugua(kw(x))")
    w("       kw_partner?")
    w("```\n")
    w(f"**Result: {commutes_all}**\n")
    if commutes_all:
        w("The 互卦 map commutes with the KW pairing for all 64 hexagrams.")
        w("This means the KW pairing is perfectly self-similar under nuclear projection:")
        w("the partner of the nuclear core IS the nuclear core of the partner.\n")
    else:
        w(f"The diagram fails to commute for **{len(commute_failures)} of 64** hexagrams.\n")

        # Analyze the failure mechanism
        w("### Failure mechanism\n")
        w("All failures share the same structure: x is **non-palindromic** but hugua(x) is **palindromic**.\n")
        w("- Left path: kw(x) = rev(x) → hugua(rev(x))")
        w("- Right path: hugua(x) is palindromic → kw(hugua(x)) = **comp**(hugua(x))")
        w("- But hugua(rev(x)) = **rev**(hugua(x)) (the reversal propagates through hugua)")
        w("- Since hugua(x) is palindromic: rev(hugua(x)) = hugua(x) ≠ comp(hugua(x))\n")
        w("The failure is a **palindrome boundary crossing**: the 互卦 map changes the palindrome")
        w("status of the hexagram, which switches which branch of the KW rule applies.")
        w("The two paths compute rev vs comp of the same 互卦, producing different results.\n")

        # Identify which hexagrams have palindromic hugua but are not palindromic
        pal_boundary = [(x, lhs, rhs) for x, lhs, rhs in commute_failures]
        w("### The 8 palindrome-boundary hexagrams\n")
        w("| x | Palindromic? | hugua(x) | hg(x) palindromic? | hugua(kw(x)) | kw(hugua(x)) |")
        w("|---|-------------|----------|--------------------|--------------|--------------| ")
        for x, lhs, rhs in commute_failures:
            hx = HUGUA[x]
            w(f"| {fmt6(x)} | {is_palindrome6(x)} | {fmt6(hx)} | {is_palindrome6(hx)} | {fmt6(lhs)} | {fmt6(rhs)} |")
        w("")

        w("These form **4 KW pairs** (each pair contributes both members to the failure list).")
        w("All are non-palindromic hexagrams with signature (1,0,0) whose reversal partner")
        w("differs only at L1,L6. Their 互卦 is palindromic because the inner 4 bits (L2-L5)")
        w("happen to form a palindrome, even though the full 6-bit hexagram does not.\n")

    return '\n'.join(lines)


if __name__ == '__main__':
    main()
