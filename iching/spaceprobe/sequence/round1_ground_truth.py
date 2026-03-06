"""
Round 1: Computational ground truth for the King Wen sequence layer.

Computes bridge kernels, algebraic properties, constraint satisfaction,
Pareto frontier sampling, and orientation bit sensitivity.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
from sequence import KING_WEN

import numpy as np
from collections import Counter
from itertools import product as iterproduct

# ─── Constants ───────────────────────────────────────────────────────────────

M = [h[2] for h in KING_WEN]  # binary strings, 0-indexed
PAIRS = [(M[2*k], M[2*k+1]) for k in range(32)]
PAIR_INDICES = [(2*k, 2*k+1) for k in range(32)]

KERNEL_NAMES = {
    (0,0,0): "id",
    (1,0,0): "O",
    (0,1,0): "M",
    (0,0,1): "I",
    (1,1,0): "OM",
    (1,0,1): "OI",
    (0,1,1): "MI",
    (1,1,1): "OMI",
}
KERNEL_INDEX = {v: k for k, v in KERNEL_NAMES.items()}
ALL_KERNELS = list(KERNEL_NAMES.keys())

# ─── Utility functions ───────────────────────────────────────────────────────

def xor6(a, b):
    """XOR two 6-bit strings, return tuple of ints."""
    return tuple(int(a[i]) ^ int(b[i]) for i in range(6))

def kernel_bits(mask6):
    """Extract 3-bit kernel from 6-bit mask: (m5, m4, m3)."""
    return (mask6[5], mask6[4], mask6[3])

def kernel_dressing(k3):
    """Expand 3-bit kernel to 6-bit palindromic dressing."""
    return (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])

def hamming3(a, b):
    return sum(x != y for x, y in zip(a, b))

def hamming6(a, b):
    return sum(x != y for x, y in zip(a, b))

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def reverse_str(s):
    """Reverse a binary string."""
    return s[::-1]

def complement_str(s):
    """Complement a binary string."""
    return ''.join('1' if c == '0' else '0' for c in s)

# ─── Bridge computation ─────────────────────────────────────────────────────

def compute_bridges(ordered_pairs):
    """Given list of (hex_a_str, hex_b_str) pairs, compute 31 bridges.
    Bridge k: XOR between exit(pair k) = pair[k][1] and entry(pair k+1) = pair[k+1][0].
    Returns list of 3-bit kernel tuples."""
    bridges = []
    for k in range(len(ordered_pairs) - 1):
        exit_hex = ordered_pairs[k][1]
        entry_hex = ordered_pairs[k + 1][0]
        mask = xor6(exit_hex, entry_hex)
        bridges.append(kernel_bits(mask))
    return bridges

def compute_bridges_full(ordered_pairs):
    """Returns list of dicts with full bridge info."""
    bridges = []
    for k in range(len(ordered_pairs) - 1):
        exit_hex = ordered_pairs[k][1]
        entry_hex = ordered_pairs[k + 1][0]
        mask = xor6(exit_hex, entry_hex)
        kb = kernel_bits(mask)
        bridges.append({
            'k': k,
            'mask': mask,
            'kernel': kb,
            'kernel_name': KERNEL_NAMES[kb],
        })
    return bridges

# ─── KW bridges ──────────────────────────────────────────────────────────────

KW_BRIDGES = compute_bridges_full(PAIRS)
KW_KERNELS = [b['kernel'] for b in KW_BRIDGES]

# ─── Section 0: Orientation freedom ─────────────────────────────────────────

def section_orientation_freedom():
    print("=" * 80)
    print("SECTION 0: ORIENTATION FREEDOM")
    print("=" * 80)
    
    fixed = []
    free = []
    for k in range(32):
        a, b = PAIRS[k]
        # Check if swapping a,b produces the same pair (a==b impossible for distinct hex)
        # A pair has NO orientation freedom if a == b (never) or if reversal is self-inverse
        # Actually: the pair {a, b} as a set is fixed. Orientation = which is first.
        # Freedom exists unless the pair is a palindrome pair where both orderings 
        # produce identical bridges in context — but that's sequence-dependent.
        # 
        # The real question: is a the reversal of b, the complement, or rev∘comp?
        # For reversal pairs: rev(a) = b. Then swapping gives exit=a, entry from next pair.
        # For complement pairs (palindromes): comp(a) = b. 
        # 
        # A pair has no orientation freedom iff a == b (never happens).
        # Actually re-reading: "5 fixed" means 5 pairs where the two hexagrams
        # form a palindromic pair with identical hexagram (self-reverse + self-complement?).
        # 
        # Let's just check: which pairs have a == reverse(b)?
        # And which have a == complement(b)? (the palindrome pairs)
        
        rev_a = reverse_str(a)
        comp_a = complement_str(a)
        
        is_reversal = (b == rev_a)
        is_complement = (b == comp_a)
        is_rev_comp = (b == complement_str(rev_a))
        
        # Check if a is a palindrome
        a_palindrome = (a == reverse_str(a))
        b_palindrome = (b == reverse_str(b))
        
        # A pair where both members are identical would have no freedom — but that can't happen
        # A pair where swapping doesn't change the SET — always true since {a,b} = {b,a}
        # The question is whether the pair is an ORDERED pair where order matters
        
        # Orientation is free unless the pair is self-inverse under swap:
        # i.e., unless (b, a) == (a, b) which requires a == b
        
        # But some pairs might be "palindromic pairs" where a is palindrome and b = comp(a),
        # and in that case swapping (a, b) to (b, a) = (comp(a), a) is NOT the same.
        # So all 32 pairs should have orientation freedom.
        
        # Let me re-read the synthesis: "All 27 orientation bits load-bearing"
        # This implies 27 free + 5 forced. Let's figure out which 5.
        
        # Perhaps the 5 forced are the ones where a and b are related by complement
        # (palindrome hexagrams), and the "natural" order is the one KW uses?
        # No — complement pairs also have two orderings.
        
        # OR: 5 pairs where swapping doesn't change ANY bridge (both neighbors see same kernel).
        # This would happen if a == b, which never occurs.
        
        # Let me reconsider: maybe "orientation" means the canonical form of the pair,
        # not the ordered position. If the pair is {h, rev(h)}, there's a choice of which 
        # is first. But if h IS rev(h) (palindrome), then the pair must be {h, comp(h)},
        # and there's still a choice. Unless h == comp(h) too, but that's impossible for 6 bits.
        
        # Actually: for palindromic hexagrams, rev(h) = h, so the pair can't be {h, rev(h)} 
        # as an unordered pair with two distinct elements. The KW pairing uses complement
        # for palindromes. So complement pairs always have 2 orderings.
        
        # WAIT: Perhaps the 5 "fixed" pairs are the ones that are self-complementary under
        # the pair-swap + bridge recomputation? Let me check a different interpretation:
        # 
        # Some pairs might be such that BOTH orderings produce the same bridge kernels
        # with their neighbors. But that depends on sequence position, not pair identity.
        # 
        # Simplest interpretation: 32 pairs, each has a "swap" degree of freedom.
        # But 5 of the 32 pairs are palindromic (h is its own reverse), and for those
        # the pairing is by complement. Maybe for these 5 pairs the kernel contribution
        # is symmetric? Let me just count palindromes.
        
        pair_type = "reversal" if is_reversal else ("complement" if is_complement else "rev+comp")
        
        info = {
            'k': k,
            'kw_nums': (KING_WEN[2*k][0], KING_WEN[2*k+1][0]),
            'a': a, 'b': b,
            'pair_type': pair_type,
            'a_palindrome': a_palindrome,
            'b_palindrome': b_palindrome,
        }
        
        if a_palindrome and b_palindrome:
            fixed.append(info)
        else:
            free.append(info)
    
    print(f"\nTotal pairs: 32")
    print(f"Palindrome pairs (both members are palindromes): {len(fixed)}")
    print(f"Non-palindrome pairs: {len(free)}")
    
    print(f"\nPalindrome pairs (both members self-reverse):")
    for p in fixed:
        print(f"  Pair {p['k']}: hex {p['kw_nums']} = {p['a']}, {p['b']} ({p['pair_type']})")
    
    # Now count: how many pairs have reversal vs complement relationship?
    rev_count = sum(1 for k in range(32) if PAIRS[k][1] == reverse_str(PAIRS[k][0]))
    comp_count = sum(1 for k in range(32) if PAIRS[k][1] == complement_str(PAIRS[k][0]))
    revcomp_count = 32 - rev_count - comp_count
    
    print(f"\nPair relationship types:")
    print(f"  Reversal pairs: {rev_count}")
    print(f"  Complement pairs: {comp_count}")
    print(f"  Rev+comp pairs: {revcomp_count}")
    
    # Count palindromic hexagrams
    palindromes = [i for i in range(64) if M[i] == reverse_str(M[i])]
    print(f"\nPalindromic hexagrams (self-reverse): {len(palindromes)}")
    print(f"  Numbers: {[KING_WEN[i][0] for i in palindromes]}")
    
    # The 5 fixed pairs: these are complement pairs (both members are palindromes)
    # For these, swapping means the exit/entry hex changes, so they DO have orientation freedom.
    # 
    # Let me reconsider: maybe the "5 fixed" means pairs where the two hexagrams
    # produce identical bridge kernel contributions regardless of order.
    # For a pair (a, b): exit in one order is b, in other is a.
    # If a and b are both palindromes and complements: 
    #   The XOR with neighbors will differ. So orientation matters.
    #
    # Perhaps "5 forced" means 5 pairs where one ordering is forced by some constraint
    # (e.g., the first hexagram must have lower number, or some structural reason).
    # Let me just note the counts and move on — the Monte Carlo will test all 32 bits.
    
    # Actually, let me check: for complement pairs (palindromes), does the pair have
    # a canonical ordering? If h and comp(h) are both palindromes, then rev(h) = h
    # and the pair is {h, comp(h)}. There's still a binary choice.
    # 
    # UNLESS for some pairs, h = comp(h), but that requires all bits = 0.5, impossible.
    # 
    # I think the "27 free + 5 fixed" might come from the previous analysis counting
    # slightly differently. Let me just proceed with 32 orientation bits for now
    # and the sensitivity analysis will reveal which ones matter.
    
    print(f"\n  → Working with all 32 orientation bits for analysis.")
    print(f"     (Sensitivity analysis in Section 8 will reveal which are load-bearing.)")
    
    return fixed, free

# ─── Section 1: Bridge kernel sequence ───────────────────────────────────────

def section_bridge_kernel_sequence():
    print("\n" + "=" * 80)
    print("SECTION 1: BRIDGE KERNEL SEQUENCE")
    print("=" * 80)
    
    print(f"\n{'Bridge':>6} {'Exit→Entry':>30} {'Mask':>8} {'Kernel':>5} {'Name':>5}")
    print("-" * 60)
    for b in KW_BRIDGES:
        k = b['k']
        exit_n = KING_WEN[2*k+1][0]
        entry_n = KING_WEN[2*(k+1)][0]
        mask_s = ''.join(str(x) for x in b['mask'])
        kb_s = ''.join(str(x) for x in b['kernel'])
        print(f"{k+1:>6} {exit_n:>3} → {entry_n:<3}  {'':>20} {mask_s:>8} {kb_s:>5} {b['kernel_name']:>5}")
    
    seq_str = ' '.join(b['kernel_name'] for b in KW_BRIDGES)
    print(f"\nKernel sequence (31 symbols):")
    print(f"  {seq_str}")

# ─── Section 2: Kernel type statistics ───────────────────────────────────────

def section_kernel_statistics():
    print("\n" + "=" * 80)
    print("SECTION 2: KERNEL TYPE STATISTICS")
    print("=" * 80)
    
    names = [b['kernel_name'] for b in KW_BRIDGES]
    freq = Counter(names)
    
    print(f"\nFrequency distribution (31 bridges total):")
    for kname in KERNEL_NAMES.values():
        count = freq.get(kname, 0)
        bar = '█' * count
        print(f"  {kname:>5}: {count:>2}  {bar}")
    
    print(f"\nDistinct kernel types used: {len(freq)} / 8")
    print(f"Most common: {freq.most_common(1)[0]}")
    print(f"Least common: {freq.most_common()[-1]}")
    
    # Entropy
    probs = np.array([freq.get(kn, 0) for kn in KERNEL_NAMES.values()]) / 31
    probs = probs[probs > 0]
    entropy = -np.sum(probs * np.log2(probs))
    max_entropy = np.log2(8)
    print(f"\nShannon entropy: {entropy:.3f} bits (max = {max_entropy:.3f})")
    print(f"Normalized entropy: {entropy / max_entropy:.3f}")

# ─── Section 3: Consecutive kernel distance matrix ──────────────────────────

def section_consecutive_distances():
    print("\n" + "=" * 80)
    print("SECTION 3: CONSECUTIVE KERNEL DISTANCES")
    print("=" * 80)
    
    dists = []
    for i in range(30):
        d = hamming3(KW_KERNELS[i], KW_KERNELS[i+1])
        dists.append(d)
    
    print(f"\nConsecutive kernel distances (3-bit Hamming, ×2 = dressing Hamming):")
    for i, d in enumerate(dists):
        a_name = KW_BRIDGES[i]['kernel_name']
        b_name = KW_BRIDGES[i+1]['kernel_name']
        print(f"  B{i+1:>2} → B{i+2:>2}: d={d} ({a_name:>5} → {b_name:<5})")
    
    dist_counts = Counter(dists)
    print(f"\nDistance distribution (3-bit):")
    for d in sorted(dist_counts):
        print(f"  d={d}: {dist_counts[d]:>2} ({dist_counts[d]/30*100:.1f}%)")
    
    print(f"\nMean consecutive distance: {np.mean(dists):.3f}")
    print(f"Std: {np.std(dists):.3f}")
    
    # Dressing distances (×2)
    print(f"\nDressing (6-bit) distance distribution:")
    for d in sorted(dist_counts):
        print(f"  d={2*d}: {dist_counts[d]:>2}")
    
    return dists

# ─── Section 4: Algebraic properties of the kernel word ─────────────────────

def section_algebraic_properties():
    print("\n" + "=" * 80)
    print("SECTION 4: ALGEBRAIC PROPERTIES OF THE KERNEL WORD")
    print("=" * 80)
    
    # Running product (cumulative XOR)
    print("\n--- Running product (cumulative XOR) ---")
    running = (0, 0, 0)
    products = []
    for i, k in enumerate(KW_KERNELS):
        running = xor3(running, k)
        products.append(running)
        print(f"  After B{i+1:>2}: {KERNEL_NAMES[running]:>5}  "
              f"({''.join(str(x) for x in running)})")
    
    # How many times each element visited
    prod_counts = Counter(products)
    print(f"\nElement visit counts in running product:")
    for kname in KERNEL_NAMES.values():
        kb = KERNEL_INDEX[kname]
        count = prod_counts.get(kb, 0)
        print(f"  {kname:>5}: {count}")
    
    all_visited = len(prod_counts) == 8
    print(f"\nVisits all 8 elements: {all_visited}")
    
    # Total product
    total = products[-1]
    print(f"\nTotal product (k₁ ⊕ k₂ ⊕ ... ⊕ k₃₁): {KERNEL_NAMES[total]} "
          f"({''.join(str(x) for x in total)})")
    
    # Subgroup generation: smallest prefix generating Z₂³
    print("\n--- Subgroup generation ---")
    generators = set()
    span = {(0,0,0)}  # identity always in span
    
    def compute_span(gens):
        """Compute the subgroup generated by a set of generators in Z₂³."""
        span = {(0,0,0)}
        changed = True
        while changed:
            changed = False
            new = set()
            for a in span:
                for g in gens:
                    prod = xor3(a, g)
                    if prod not in span:
                        new.add(prod)
                        changed = True
            span |= new
        return span
    
    for i, k in enumerate(KW_KERNELS):
        generators.add(k)
        span = compute_span(generators)
        if len(span) == 8:
            print(f"  Full Z₂³ generated after first {i+1} bridges")
            print(f"  Generators used: {[KERNEL_NAMES[g] for g in sorted(generators)]}")
            break

# ─── Section 5: Transition graph structure ───────────────────────────────────

def section_transition_graph():
    print("\n" + "=" * 80)
    print("SECTION 5: TRANSITION GRAPH STRUCTURE")
    print("=" * 80)
    
    # Transition count matrix
    all_names = list(KERNEL_NAMES.values())
    name_to_idx = {n: i for i, n in enumerate(all_names)}
    trans_matrix = np.zeros((8, 8), dtype=int)
    
    for i in range(30):
        from_name = KW_BRIDGES[i]['kernel_name']
        to_name = KW_BRIDGES[i+1]['kernel_name']
        trans_matrix[name_to_idx[from_name]][name_to_idx[to_name]] += 1
    
    print(f"\nTransition matrix (row=from, col=to):")
    header = "     " + " ".join(f"{n:>4}" for n in all_names)
    print(header)
    for i, name in enumerate(all_names):
        row = " ".join(f"{trans_matrix[i][j]:>4}" for j in range(8))
        print(f"{name:>4} {row}")
    
    # Diagonal = self-transitions (repeats)
    self_trans = sum(trans_matrix[i][i] for i in range(8))
    print(f"\nSelf-transitions (kernel repeats): {self_trans} / 30")
    
    # Longest run
    max_run = 1
    current_run = 1
    for i in range(1, 31):
        if KW_KERNELS[i] == KW_KERNELS[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    print(f"Longest run of same kernel: {max_run}")
    
    # Second-order entropy H(k_{n+1} | k_n)
    # H(Y|X) = -sum_x p(x) sum_y p(y|x) log2 p(y|x)
    # p(x) = frequency of x as "from" state
    from_counts = trans_matrix.sum(axis=1)
    h_cond = 0
    for i in range(8):
        if from_counts[i] == 0:
            continue
        p_x = from_counts[i] / 30
        for j in range(8):
            if trans_matrix[i][j] == 0:
                continue
            p_y_given_x = trans_matrix[i][j] / from_counts[i]
            h_cond -= p_x * p_y_given_x * np.log2(p_y_given_x)
    
    print(f"\nConditional entropy H(k_{{n+1}} | k_n): {h_cond:.3f} bits")
    print(f"Unconditional entropy H(k): {-sum(p * np.log2(p) for p in from_counts[from_counts > 0] / 30):.3f} bits")
    print(f"Mutual information I(k_n; k_{{n+1}}): {-sum(p * np.log2(p) for p in from_counts[from_counts > 0] / 30) - h_cond:.3f} bits")

# ─── Section 6: Constraint satisfaction test ────────────────────────────────

def section_constraint_satisfaction():
    print("\n" + "=" * 80)
    print("SECTION 6: CONSTRAINT SATISFACTION TEST")
    print("=" * 80)
    
    # KW values
    kw_dists = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
    
    c1_kw = sum(1 for d in kw_dists if d > 0)  # no consecutive repeat
    c2_kw = sum(1 for d in kw_dists if d >= 2)  # distance >= 2 (in 3-bit = 4 in dressing)
    c1c2_kw = sum(1 for d in kw_dists if d >= 2)  # same as c2 since d>=2 implies d>0
    
    print(f"\nKW constraint satisfaction (out of 30 consecutive pairs):")
    print(f"  C1 (no repeat, d>0): {c1_kw} / 30")
    print(f"  C2 (d≥2 in 3-bit):  {c2_kw} / 30")
    print(f"  C1∧C2:              {c1c2_kw} / 30")
    
    all_c1 = (c1_kw == 30)
    all_c2 = (c2_kw == 30)
    print(f"\n  KW satisfies ALL C1: {all_c1}")
    print(f"  KW satisfies ALL C2: {all_c2}")
    
    # Monte Carlo
    print(f"\n--- Monte Carlo: 100,000 random trials ---")
    print(f"  (random pair permutation + random orientations)")
    
    rng = np.random.default_rng(42)
    N_TRIALS = 100_000
    
    # Precompute pair data as arrays for speed
    pair_hex_a = []
    pair_hex_b = []
    for k in range(32):
        a = [int(c) for c in PAIRS[k][0]]
        b = [int(c) for c in PAIRS[k][1]]
        pair_hex_a.append(a)
        pair_hex_b.append(b)
    pair_hex_a = np.array(pair_hex_a, dtype=np.int8)
    pair_hex_b = np.array(pair_hex_b, dtype=np.int8)
    
    rand_c1_counts = []  # fraction satisfying C1 per trial
    rand_c2_counts = []  # fraction satisfying C2 per trial
    rand_all_c1 = 0      # trials where ALL 30 satisfy C1
    rand_all_c2 = 0      # trials where ALL 30 satisfy C2
    rand_all_c1c2 = 0    # trials where ALL 30 satisfy C1∧C2
    
    for trial in range(N_TRIALS):
        perm = rng.permutation(32)
        orient = rng.integers(0, 2, size=32)  # 0 = original, 1 = swap
        
        # Build ordered sequence: for each pair, pick exit and entry
        # exit[k] = pair[perm[k]]'s second hex (or first if swapped)
        # entry[k] = pair[perm[k]]'s first hex (or second if swapped)
        
        exits = np.empty((32, 6), dtype=np.int8)
        entries = np.empty((32, 6), dtype=np.int8)
        for k in range(32):
            pk = perm[k]
            if orient[k] == 0:
                entries[k] = pair_hex_a[pk]
                exits[k] = pair_hex_b[pk]
            else:
                entries[k] = pair_hex_b[pk]
                exits[k] = pair_hex_a[pk]
        
        # Bridges: XOR between exit[k] and entry[k+1]
        # Kernel bits: positions 5, 4, 3 of the 6-bit mask
        bridge_masks = np.bitwise_xor(exits[:31], entries[1:32])  # shape (31, 6)
        kernels = bridge_masks[:, [5, 4, 3]]  # shape (31, 3)
        
        # Consecutive kernel distances
        diffs = np.bitwise_xor(kernels[:30], kernels[1:31])  # shape (30, 3)
        cons_dists = diffs.sum(axis=1)  # shape (30,)
        
        c1_sat = (cons_dists > 0).sum()
        c2_sat = (cons_dists >= 2).sum()
        
        rand_c1_counts.append(c1_sat)
        rand_c2_counts.append(c2_sat)
        
        if c1_sat == 30:
            rand_all_c1 += 1
        if c2_sat == 30:
            rand_all_c2 += 1
        if c1_sat == 30 and c2_sat == 30:
            rand_all_c1c2 += 1
    
    rand_c1_counts = np.array(rand_c1_counts)
    rand_c2_counts = np.array(rand_c2_counts)
    
    print(f"\n  C1 (no repeat) satisfaction per trial:")
    print(f"    Mean: {rand_c1_counts.mean():.2f} / 30")
    print(f"    Std:  {rand_c1_counts.std():.2f}")
    print(f"    KW value: {c1_kw} / 30")
    print(f"    KW percentile: {(rand_c1_counts <= c1_kw).mean() * 100:.2f}%")
    print(f"    Trials with ALL 30 satisfying C1: {rand_all_c1} / {N_TRIALS} ({rand_all_c1/N_TRIALS*100:.4f}%)")
    
    print(f"\n  C2 (d≥2) satisfaction per trial:")
    print(f"    Mean: {rand_c2_counts.mean():.2f} / 30")
    print(f"    Std:  {rand_c2_counts.std():.2f}")
    print(f"    KW value: {c2_kw} / 30")
    print(f"    KW percentile: {(rand_c2_counts <= c2_kw).mean() * 100:.2f}%")
    print(f"    Trials with ALL 30 satisfying C2: {rand_all_c2} / {N_TRIALS} ({rand_all_c2/N_TRIALS*100:.4f}%)")
    
    print(f"\n  Trials with ALL C1∧C2: {rand_all_c1c2} / {N_TRIALS} ({rand_all_c1c2/N_TRIALS*100:.4f}%)")

# ─── Section 7: Pareto frontier sampling ────────────────────────────────────

def section_pareto_frontier():
    print("\n" + "=" * 80)
    print("SECTION 7: PARETO FRONTIER SAMPLING")
    print("=" * 80)
    
    rng = np.random.default_rng(42)
    N_TRIALS = 1_000_000
    
    # Precompute pair data
    pair_hex_a = np.array([[int(c) for c in PAIRS[k][0]] for k in range(32)], dtype=np.int8)
    pair_hex_b = np.array([[int(c) for c in PAIRS[k][1]] for k in range(32)], dtype=np.int8)
    
    # KW values
    kw_dists_3bit = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
    kw_f1 = np.mean(kw_dists_3bit)
    kw_f2 = len(set(KW_KERNELS))
    
    print(f"\nKW objectives:")
    print(f"  f1 (mean consecutive kernel distance, 3-bit): {kw_f1:.4f}")
    print(f"  f2 (distinct kernel types): {kw_f2}")
    
    # Batch sampling
    f1_samples = np.empty(N_TRIALS)
    f2_samples = np.empty(N_TRIALS, dtype=int)
    
    for trial in range(N_TRIALS):
        perm = rng.permutation(32)
        orient = rng.integers(0, 2, size=32)
        
        exits = np.empty((32, 6), dtype=np.int8)
        entries = np.empty((32, 6), dtype=np.int8)
        for k in range(32):
            pk = perm[k]
            if orient[k] == 0:
                entries[k] = pair_hex_a[pk]
                exits[k] = pair_hex_b[pk]
            else:
                entries[k] = pair_hex_b[pk]
                exits[k] = pair_hex_a[pk]
        
        bridge_masks = np.bitwise_xor(exits[:31], entries[1:32])
        kernels_3bit = bridge_masks[:, [5, 4, 3]]
        
        # f1: mean consecutive kernel distance
        diffs = np.bitwise_xor(kernels_3bit[:30], kernels_3bit[1:31])
        cons_dists = diffs.sum(axis=1)
        f1_samples[trial] = cons_dists.mean()
        
        # f2: distinct kernel types
        kernel_ids = kernels_3bit[:, 0] * 4 + kernels_3bit[:, 1] * 2 + kernels_3bit[:, 2]
        f2_samples[trial] = len(np.unique(kernel_ids))
    
    print(f"\n--- f1 (mean consecutive kernel distance) ---")
    print(f"  Random mean: {f1_samples.mean():.4f}")
    print(f"  Random std:  {f1_samples.std():.4f}")
    print(f"  Random min:  {f1_samples.min():.4f}")
    print(f"  Random max:  {f1_samples.max():.4f}")
    print(f"  KW f1:       {kw_f1:.4f}")
    print(f"  KW percentile: {(f1_samples <= kw_f1).mean() * 100:.4f}%")
    
    print(f"\n--- f2 (distinct kernel types) ---")
    f2_dist = Counter(f2_samples)
    for v in sorted(f2_dist):
        print(f"  f2={v}: {f2_dist[v]:>8} ({f2_dist[v]/N_TRIALS*100:.2f}%)")
    print(f"  KW f2:       {kw_f2}")
    print(f"  KW percentile: {(f2_samples <= kw_f2).mean() * 100:.4f}%")
    
    # Pareto frontier
    print(f"\n--- Pareto frontier analysis ---")
    
    # A point (f1, f2) dominates (f1', f2') if f1 >= f1' and f2 >= f2' with at least one strict
    # For integer f2, we can compute Pareto front per f2 level
    pareto_f1_by_f2 = {}
    for f2_val in sorted(f2_dist.keys()):
        mask = f2_samples == f2_val
        max_f1 = f1_samples[mask].max()
        pareto_f1_by_f2[f2_val] = max_f1
    
    # Build actual Pareto front (non-dominated points)
    pareto_front = []
    sorted_f2 = sorted(pareto_f1_by_f2.keys(), reverse=True)
    best_f1_so_far = -1
    for f2_val in sorted_f2:
        if pareto_f1_by_f2[f2_val] > best_f1_so_far:
            best_f1_so_far = pareto_f1_by_f2[f2_val]
            pareto_front.append((f2_val, best_f1_so_far))
    pareto_front.reverse()
    
    print(f"  Pareto-optimal (f2, max f1):")
    for f2_val, f1_val in pareto_front:
        kw_marker = " ← KW" if f2_val == kw_f2 and abs(f1_val - kw_f1) < 0.01 else ""
        print(f"    f2={f2_val}, f1={f1_val:.4f}{kw_marker}")
    
    # Is KW on the Pareto front?
    kw_dominated = False
    for trial in range(N_TRIALS):
        if f1_samples[trial] >= kw_f1 and f2_samples[trial] >= kw_f2:
            if f1_samples[trial] > kw_f1 or f2_samples[trial] > kw_f2:
                kw_dominated = True
                break
    
    print(f"\n  KW is Pareto-dominated: {kw_dominated}")
    
    # Maximum achievable f1
    max_f1_overall = f1_samples.max()
    print(f"\n  Maximum f1 found (any f2): {max_f1_overall:.4f}")
    print(f"  KW f1 / max f1: {kw_f1 / max_f1_overall:.4f}")
    
    # Count how many trials dominate KW (both f1 >= kw_f1 AND f2 >= kw_f2, at least one strict)
    dominating = ((f1_samples >= kw_f1) & (f2_samples >= kw_f2) & 
                  ((f1_samples > kw_f1) | (f2_samples > kw_f2)))
    print(f"  Trials that dominate KW: {dominating.sum()} / {N_TRIALS} ({dominating.sum()/N_TRIALS*100:.4f}%)")
    
    # Matching trials (same or better on both)
    matching = (f1_samples >= kw_f1) & (f2_samples >= kw_f2)
    print(f"  Trials matching or better on both: {matching.sum()} / {N_TRIALS} ({matching.sum()/N_TRIALS*100:.4f}%)")
    
    return f1_samples, f2_samples

# ─── Section 8: Orientation bit sensitivity ─────────────────────────────────

def section_orientation_sensitivity():
    print("\n" + "=" * 80)
    print("SECTION 8: ORIENTATION BIT SENSITIVITY")
    print("=" * 80)
    
    # Baseline KW values
    kw_dists_3bit = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
    kw_f1 = np.mean(kw_dists_3bit)
    kw_repeats = sum(1 for d in kw_dists_3bit if d == 0)
    kw_f2 = len(set(KW_KERNELS))
    
    print(f"\nBaseline KW:")
    print(f"  f1 (mean cons. kernel dist): {kw_f1:.4f}")
    print(f"  Kernel repeats: {kw_repeats}")
    print(f"  f2 (distinct kernels): {kw_f2}")
    
    print(f"\n{'Pair':>4} {'KW nums':>10} {'Type':>10} {'Δf1':>8} {'Δrepeats':>9} {'Δf2':>4} {'Degraded?':>10}")
    print("-" * 65)
    
    degradation_info = []
    
    for flip_k in range(32):
        # Create a new pair list with pair flip_k swapped
        new_pairs = []
        for k in range(32):
            if k == flip_k:
                new_pairs.append((PAIRS[k][1], PAIRS[k][0]))  # swap
            else:
                new_pairs.append(PAIRS[k])
        
        # Recompute bridges
        new_kernels = compute_bridges(new_pairs)
        new_dists = [hamming3(new_kernels[i], new_kernels[i+1]) for i in range(30)]
        new_f1 = np.mean(new_dists)
        new_repeats = sum(1 for d in new_dists if d == 0)
        new_f2 = len(set(new_kernels))
        
        delta_f1 = new_f1 - kw_f1
        delta_repeats = new_repeats - kw_repeats
        delta_f2 = new_f2 - kw_f2
        
        # Degraded = f1 decreased OR repeats increased OR f2 decreased
        degraded = delta_f1 < -0.001 or delta_repeats > 0 or delta_f2 < 0
        
        kw_nums = (KING_WEN[2*flip_k][0], KING_WEN[2*flip_k+1][0])
        
        # Pair type
        a, b = PAIRS[flip_k]
        if b == reverse_str(a):
            ptype = "rev"
        elif b == complement_str(a):
            ptype = "comp"
        else:
            ptype = "rev+comp"
        
        degradation_info.append({
            'k': flip_k, 'kw_nums': kw_nums, 'type': ptype,
            'delta_f1': delta_f1, 'delta_repeats': delta_repeats, 
            'delta_f2': delta_f2, 'degraded': degraded,
        })
        
        marker = "YES" if degraded else "no"
        print(f"{flip_k:>4} {str(kw_nums):>10} {ptype:>10} {delta_f1:>+8.4f} {delta_repeats:>+9d} {delta_f2:>+4d} {marker:>10}")
    
    load_bearing = sum(1 for d in degradation_info if d['degraded'])
    print(f"\nLoad-bearing orientation bits: {load_bearing} / 32")
    print(f"Non-load-bearing (swap has no effect): {32 - load_bearing}")
    
    non_lb = [d for d in degradation_info if not d['degraded']]
    if non_lb:
        print(f"\nNon-load-bearing pairs:")
        for d in non_lb:
            print(f"  Pair {d['k']}: hex {d['kw_nums']} ({d['type']})")
    
    # Most sensitive
    by_f1_impact = sorted(degradation_info, key=lambda d: d['delta_f1'])
    print(f"\nTop 5 most sensitive (largest f1 decrease on flip):")
    for d in by_f1_impact[:5]:
        print(f"  Pair {d['k']} ({d['kw_nums']}): Δf1 = {d['delta_f1']:+.4f}, "
              f"Δrepeats = {d['delta_repeats']:+d}, Δf2 = {d['delta_f2']:+d}")

# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    section_orientation_freedom()
    section_bridge_kernel_sequence()
    section_kernel_statistics()
    cons_dists = section_consecutive_distances()
    section_algebraic_properties()
    section_transition_graph()
    section_constraint_satisfaction()
    f1_samples, f2_samples = section_pareto_frontier()
    section_orientation_sensitivity()
    
    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
