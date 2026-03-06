"""
Meta-hexagram analysis: stack orbit signatures of adjacent pairs
into 6-bit meta-hexagrams. Each pair has a 3-bit XOR signature
(L1⊕L6, L2⊕L5, L3⊕L4). Two adjacent pairs → 6-bit object.

32 pairs → 16 non-overlapping meta-hexagrams (quartets)
32 pairs → 31 sliding-window meta-hexagrams
"""

import numpy as np
from collections import Counter
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
N_PAIRS = 32

M = np.array(all_bits())

# Orbit signatures
ORBIT_SIGS = {}
for i in range(N):
    h = tuple(M[i])
    sig = (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])
    ORBIT_SIGS[i] = sig

# Pair signatures (= orbit signature of either member, since pairs are intra-orbit)
pair_sigs = []
for k in range(N_PAIRS):
    sig = ORBIT_SIGS[2 * k]
    pair_sigs.append(sig)

# Pair masks (generator type)
MASKS = {
    (1,1,1,1,1,1): "OMI", (1,1,0,0,1,1): "OM", (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI", (0,1,0,0,1,0): "M", (0,0,1,1,0,0): "I",
    (1,0,0,0,0,1): "O",
}

pair_masks = []
for k in range(N_PAIRS):
    a = tuple(M[2*k])
    b = tuple(M[2*k+1])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    pair_masks.append(MASKS[xor])

# KW hexagram lookup by bits
KW_BY_BITS = {}
for i in range(N):
    KW_BY_BITS[tuple(M[i])] = (i + 1, KING_WEN[i][1])


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ─── 1. Non-overlapping meta-hexagrams (quartets) ────────────────────────────

def nonoverlapping():
    print("=" * 70)
    print("1. NON-OVERLAPPING META-HEXAGRAMS (16 quartets)")
    print("   Lower trigram = pair k signature, upper = pair k+1 signature")
    print("=" * 70)

    metas = []
    for q in range(16):
        lower = pair_sigs[2 * q]       # pair 2q+1
        upper = pair_sigs[2 * q + 1]   # pair 2q+2
        meta = lower + upper           # 6-bit tuple
        metas.append(meta)

        # Look up as KW hexagram
        kw_match = KW_BY_BITS.get(meta)
        kw_str = f"= #{kw_match[0]} {kw_match[1]}" if kw_match else "not a KW hex"

        mask_lower = pair_masks[2 * q]
        mask_upper = pair_masks[2 * q + 1]

        print(f"\n  Q{q+1:2d}: pair {2*q+1},{2*q+2} "
              f"({mask_lower}→{mask_upper})")
        print(f"    Lower sig: {lower}  Upper sig: {upper}")
        print(f"    Meta-hex: {''.join(map(str, meta))}  {kw_str}")

    # How many unique meta-hexagrams?
    unique = len(set(metas))
    print(f"\n  Unique meta-hexagrams: {unique}/16")

    # Do the meta-hexagrams themselves form pairs?
    print(f"\n  Meta-hexagram pairing:")
    for q in range(0, 16, 2):
        m1 = metas[q]
        m2 = metas[q + 1]
        dist = hamming(m1, m2)
        xor = tuple(m1[i] ^ m2[i] for i in range(6))
        xor_name = MASKS.get(xor, f"{''.join(map(str, xor))}")
        print(f"    Q{q+1}-Q{q+2}: "
              f"{''.join(map(str, m1))} vs {''.join(map(str, m2))}  "
              f"dist={dist}  XOR={xor_name}")

    return metas


# ─── 2. Sliding window meta-hexagrams ────────────────────────────────────────

def sliding():
    print("\n" + "=" * 70)
    print("2. SLIDING WINDOW META-HEXAGRAMS (31 transitions)")
    print("=" * 70)

    metas = []
    for k in range(N_PAIRS - 1):
        lower = pair_sigs[k]
        upper = pair_sigs[k + 1]
        meta = lower + upper
        metas.append(meta)

    # Map to KW hexagrams
    kw_matches = 0
    for k, meta in enumerate(metas):
        kw_match = KW_BY_BITS.get(meta)
        if kw_match:
            kw_matches += 1

    print(f"  Meta-hexagrams that ARE King Wen hexagrams: {kw_matches}/31")

    # List them
    print(f"\n  Sliding meta-hex sequence:")
    for k, meta in enumerate(metas):
        kw_match = KW_BY_BITS.get(meta)
        kw_str = f"#{kw_match[0]:2d} {kw_match[1]}" if kw_match else "—"
        print(f"    P{k+1:2d}→P{k+2:2d}: "
              f"{''.join(map(str, meta))}  {kw_str}")

    # Unique meta-hexagrams
    unique = len(set(metas))
    print(f"\n  Unique: {unique}/31")

    # Frequency
    freq = Counter(metas)
    repeated = {k: v for k, v in freq.items() if v > 1}
    if repeated:
        print(f"  Repeated meta-hexagrams:")
        for meta, count in sorted(repeated.items(), key=lambda x: -x[1]):
            kw_match = KW_BY_BITS.get(meta)
            kw_str = f"#{kw_match[0]} {kw_match[1]}" if kw_match else "—"
            print(f"    {''.join(map(str, meta))}: {count}×  {kw_str}")

    return metas


# ─── 3. Meta-hexagram orbit signatures (meta-meta) ──────────────────────────

def meta_orbits():
    print("\n" + "=" * 70)
    print("3. META-HEXAGRAM ORBIT SIGNATURES (self-similarity test)")
    print("=" * 70)

    # Non-overlapping meta-hexagrams
    metas = []
    for q in range(16):
        lower = pair_sigs[2 * q]
        upper = pair_sigs[2 * q + 1]
        metas.append(lower + upper)

    # Each meta-hexagram is itself a 6-bit string — what's ITS orbit signature?
    print(f"  Meta-hexagram orbit signatures:")
    meta_sigs = []
    for q, meta in enumerate(metas):
        sig = (meta[0] ^ meta[5], meta[1] ^ meta[4], meta[2] ^ meta[3])
        meta_sigs.append(sig)

        kw_match = KW_BY_BITS.get(meta)
        kw_str = f"#{kw_match[0]} {kw_match[1]}" if kw_match else "—"
        print(f"    Q{q+1:2d}: {''.join(map(str, meta))} → sig {sig}  {kw_str}")

    # Distribution of meta-signatures
    sig_freq = Counter(meta_sigs)
    print(f"\n  Meta-signature distribution:")
    for sig in sorted(sig_freq.keys()):
        print(f"    {sig}: {sig_freq[sig]}×")

    # The meta-sig of stacking (s1, s2) is:
    # (s1[0]⊕s2[2], s1[1]⊕s2[1], s1[2]⊕s2[0])
    # — it's the XOR of the two signatures with reversed pairing!
    print(f"\n  Meta-sig = XOR of lower sig with REVERSED upper sig:")
    for q in range(16):
        lower = pair_sigs[2 * q]
        upper = pair_sigs[2 * q + 1]
        xor_reversed = (lower[0] ^ upper[2], lower[1] ^ upper[1], lower[2] ^ upper[0])
        actual = meta_sigs[q]
        match = "✓" if xor_reversed == actual else "✗"
        print(f"    Q{q+1:2d}: {lower} ⊕ rev({upper})={upper[::-1]} → "
              f"{xor_reversed} {match}")


# ─── 3b. Cross-generator decomposition ───────────────────────────────────────

def cross_generator():
    print("\n" + "=" * 70)
    print("3b. CROSS-GENERATOR DECOMPOSITION")
    print("    meta_sig = (O_lower⊕I_upper, M_lower⊕M_upper, I_lower⊕O_upper)")
    print("=" * 70)

    GEN_NAMES = {0: 'O', 1: 'M', 2: 'I'}

    # Non-overlapping meta-hexagrams
    print(f"\n  {'Q':>3s}  {'lower':>7s} {'upper':>7s}  "
          f"{'O_lo⊕I_up':>9s} {'M_lo⊕M_up':>9s} {'I_lo⊕O_up':>9s}  "
          f"meta_sig  interpretation")
    print(f"  {'─'*3}  {'─'*7} {'─'*7}  {'─'*9} {'─'*9} {'─'*9}  {'─'*8}  {'─'*30}")

    meta_sigs = []
    cross_bits = []
    for q in range(16):
        lower = pair_sigs[2 * q]
        upper = pair_sigs[2 * q + 1]

        # Cross-generator XOR: O↔I swap
        o_lo_x_i_up = lower[0] ^ upper[2]  # O_lower ⊕ I_upper
        m_lo_x_m_up = lower[1] ^ upper[1]  # M_lower ⊕ M_upper
        i_lo_x_o_up = lower[2] ^ upper[0]  # I_lower ⊕ O_upper

        meta_sig = (o_lo_x_i_up, m_lo_x_m_up, i_lo_x_o_up)
        meta_sigs.append(meta_sig)
        cross_bits.append((o_lo_x_i_up, m_lo_x_m_up, i_lo_x_o_up))

        # Interpretation
        parts = []
        if o_lo_x_i_up == 0:
            parts.append("O=I across")
        else:
            parts.append("O≠I across")
        if m_lo_x_m_up == 0:
            parts.append("M stable")
        else:
            parts.append("M shifts")
        if i_lo_x_o_up == 0:
            parts.append("I=O across")
        else:
            parts.append("I≠O across")

        lo_str = ''.join(map(str, lower))
        up_str = ''.join(map(str, upper))

        print(f"  Q{q+1:2d}  {lo_str:>7s} {up_str:>7s}  "
              f"{'=':>9s} {'=':>9s} {'=':>9s}  "
              f"({meta_sig[0]},{meta_sig[1]},{meta_sig[2]})  "
              f"{'; '.join(parts)}".replace(
                  f"{'=':>9s} {'=':>9s} {'=':>9s}",
                  f"{o_lo_x_i_up:>9d} {m_lo_x_m_up:>9d} {i_lo_x_o_up:>9d}"))

    # Summary statistics
    print(f"\n  Cross-generator bit frequencies:")
    o_i_count = sum(1 for b in cross_bits if b[0] == 1)
    m_m_count = sum(1 for b in cross_bits if b[1] == 1)
    i_o_count = sum(1 for b in cross_bits if b[2] == 1)
    print(f"    O_lower ≠ I_upper: {o_i_count}/16 ({o_i_count/16:.1%})")
    print(f"    M_lower ≠ M_upper: {m_m_count}/16 ({m_m_count/16:.1%})")
    print(f"    I_lower ≠ O_upper: {i_o_count}/16 ({i_o_count/16:.1%})")

    # Symmetry test: is bit 0 always equal to bit 2?
    # (O_lo⊕I_up) vs (I_lo⊕O_up) — these are the same comparison reversed
    symmetric = sum(1 for b in cross_bits if b[0] == b[2])
    print(f"\n  Symmetry test (bit 0 = bit 2, i.e. O↔I cross is symmetric):")
    print(f"    {symmetric}/16 symmetric")

    # What does meta_sig (0,0,0) mean? Lower sig = reverse of upper sig
    print(f"\n  Special meta-signatures:")
    for q in range(16):
        lower = pair_sigs[2 * q]
        upper = pair_sigs[2 * q + 1]
        ms = meta_sigs[q]
        if ms == (0, 0, 0):
            print(f"    Q{q+1:2d}: (0,0,0) — lower {lower} is reverse of upper "
                  f"{upper} → structural mirror")
        elif ms == (1, 1, 1):
            print(f"    Q{q+1:2d}: (1,1,1) — maximum cross-disagreement "
                  f"({lower} vs {upper})")

    # Do the sliding-window meta-sigs show the same pattern?
    print(f"\n  Sliding-window cross-generator decomposition:")
    for k in range(N_PAIRS - 1):
        lower = pair_sigs[k]
        upper = pair_sigs[k + 1]
        o_x_i = lower[0] ^ upper[2]
        m_x_m = lower[1] ^ upper[1]
        i_x_o = lower[2] ^ upper[0]
        meta = lower + upper
        kw_match = KW_BY_BITS.get(meta)
        kw_str = f"#{kw_match[0]:2d} {kw_match[1]}" if kw_match else "—"

        print(f"    P{k+1:2d}→P{k+2:2d}: "
              f"O⊕I={o_x_i} M⊕M={m_x_m} I⊕O={i_x_o}  "
              f"→ ({o_x_i},{m_x_m},{i_x_o})  {kw_str}")

    # Sliding-window frequencies
    slide_bits = []
    for k in range(N_PAIRS - 1):
        lower = pair_sigs[k]
        upper = pair_sigs[k + 1]
        slide_bits.append((lower[0]^upper[2], lower[1]^upper[1], lower[2]^upper[0]))

    print(f"\n  Sliding cross-generator frequencies:")
    s_oi = sum(1 for b in slide_bits if b[0] == 1)
    s_mm = sum(1 for b in slide_bits if b[1] == 1)
    s_io = sum(1 for b in slide_bits if b[2] == 1)
    print(f"    O_lower ≠ I_upper: {s_oi}/31 ({s_oi/31:.1%})")
    print(f"    M_lower ≠ M_upper: {s_mm}/31 ({s_mm/31:.1%})")
    print(f"    I_lower ≠ O_upper: {s_io}/31 ({s_io/31:.1%})")

    s_sym = sum(1 for b in slide_bits if b[0] == b[2])
    print(f"    Bit 0 = Bit 2 (symmetric): {s_sym}/31 ({s_sym/31:.1%})")


# ─── 4. Meta-sequence as a path ──────────────────────────────────────────────

def meta_path():
    print("\n" + "=" * 70)
    print("4. META-SEQUENCE AS A PATH IN {0,1}^6")
    print("=" * 70)

    metas = []
    for q in range(16):
        lower = pair_sigs[2 * q]
        upper = pair_sigs[2 * q + 1]
        metas.append(lower + upper)

    # Consecutive distances
    print(f"  Consecutive meta-hex distances:")
    dists = []
    for q in range(15):
        d = hamming(metas[q], metas[q + 1])
        dists.append(d)
    print(f"    {' '.join(str(d) for d in dists)}")
    print(f"    Mean: {np.mean(dists):.2f}, dist distribution: {dict(Counter(dists))}")

    # Does the meta-sequence visit all vertices?
    unique_metas = set(metas)
    print(f"\n  Unique vertices visited: {len(unique_metas)}/16 "
          f"(of 64 possible in {{0,1}}^6)")

    # Weight trajectory
    weights = [sum(m) for m in metas]
    print(f"\n  Meta-hex weights: {weights}")
    print(f"    Mean: {np.mean(weights):.2f}, range: {min(weights)}-{max(weights)}")

    # Does the meta-sequence have the same orbit structure?
    print(f"\n  Meta-sequence orbit signatures (which orbit is each meta-hex in?):")
    for q, meta in enumerate(metas):
        sig = (meta[0] ^ meta[5], meta[1] ^ meta[4], meta[2] ^ meta[3])
        # Which original orbit has this signature?
        orbit_sigs_to_num = {
            (0,0,0): 1, (1,1,0): 2, (1,0,1): 3, (0,1,0): 4,
            (0,0,1): 5, (1,1,1): 6, (1,0,0): 7, (0,1,1): 8,
        }
        orbit_num = orbit_sigs_to_num[sig]
        kw_match = KW_BY_BITS.get(meta)
        kw_str = f"#{kw_match[0]} {kw_match[1]}" if kw_match else "—"
        print(f"    Q{q+1:2d}: orbit {orbit_num} ({kw_str})")


# ─── 5. Signature transition matrix ──────────────────────────────────────────

def sig_transitions():
    print("\n" + "=" * 70)
    print("5. SIGNATURE TRANSITION STRUCTURE")
    print("=" * 70)

    # The 32 pair signatures form a sequence in {0,1}³
    # What's the transition pattern?
    print(f"  Pair signature sequence:")
    print(f"    {' → '.join(''.join(map(str, s)) for s in pair_sigs)}")

    # Consecutive XOR (what changes between adjacent pair signatures)
    print(f"\n  Consecutive signature XOR (what changes at each bridge):")
    sig_xors = []
    for k in range(N_PAIRS - 1):
        xor = tuple(pair_sigs[k][i] ^ pair_sigs[k+1][i] for i in range(3))
        sig_xors.append(xor)

    xor_names = {
        (0,0,0): 'id', (1,0,0): 'o', (0,1,0): 'm', (0,0,1): 'i',
        (1,1,0): 'om', (1,0,1): 'oi', (0,1,1): 'mi', (1,1,1): 'omi',
    }
    xor_seq = [xor_names[x] for x in sig_xors]
    print(f"    {' → '.join(xor_seq)}")

    # Frequency
    xor_freq = Counter(sig_xors)
    print(f"\n  Signature change frequency:")
    for xor in sorted(xor_freq.keys()):
        print(f"    {xor_names[xor]:>3s} ({xor}): {xor_freq[xor]}×")

    # The signature transitions form THEIR OWN generator sequence!
    # Is it related to the original pair mask sequence?
    print(f"\n  Original pair mask sequence:")
    print(f"    {' → '.join(pair_masks)}")
    print(f"\n  Signature change sequence:")
    print(f"    {' → '.join(xor_seq)}")

    # Correlation between mask at position k and sig change at bridge k→k+1?
    print(f"\n  Mask at bridge vs signature change:")
    for k in range(N_PAIRS - 1):
        print(f"    P{k+1:2d}→P{k+2:2d}: mask={pair_masks[k]:>3s}→{pair_masks[k+1]:>3s}  "
              f"sig_change={xor_seq[k]}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("META-HEXAGRAM ANALYSIS")
    print("Stacking orbit signatures of adjacent pairs")
    print("=" * 70)

    nonoverlapping()
    sliding()
    meta_orbits()
    cross_generator()
    meta_path()
    sig_transitions()

    print("\n" + "=" * 70)
    print("META-HEXAGRAM ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
