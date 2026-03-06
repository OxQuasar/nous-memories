"""
Deep analysis of orientation — following up on census findings.

Key finding from Thread A: inversion frame is all 1s (reverse(first) == second always).
Key finding from Thread B: no single structural rule exceeds 53% (all at 50% for inversion pairs).

Deeper questions:
1. For inversion pairs (28): which "reading direction" is chosen? 
   Since reverse(a) = b, the two hexagrams are literally the same pattern read 
   bottom-to-top vs top-to-bottom. What determines which reading is first?
2. Is the 14/14 split on every rule a coincidence, or is there structure in 
   WHICH 14 go each way?
3. Look at the orientation in terms of the position within the orbit (o,m,i coords)
4. Octet structure: the binary frame shows a beautiful monotonic decay then recovery
   (4,3,2,1,0,2,3,2 ones per octet). Is this significant?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter2')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
from analysis_utils import VALID_MASKS, xor_sig, xor_tuple, hamming, GEN_BITS

DIMS = 6
N_PAIRS = 32
N_TRIALS = 100000
RNG = np.random.default_rng(42)

M = [tuple(h) for h in all_bits()]


def reverse_bits(h):
    return tuple(h[5-i] for i in range(DIMS))

def complement(h):
    return tuple(1 - x for x in h)

def weight(h):
    return sum(h)

def to_int(h):
    val = 0
    for bit in h:
        val = val * 2 + bit
    return val

def is_palindrome(h):
    return h == reverse_bits(h)


# Build pairs
pairs = []
for k in range(N_PAIRS):
    a = M[2 * k]
    b = M[2 * k + 1]
    mask = xor_tuple(a, b)
    pairs.append({
        'idx': k,
        'a': a, 'b': b,
        'num_a': KING_WEN[2 * k][0],
        'num_b': KING_WEN[2 * k + 1][0],
        'name_a': KING_WEN[2 * k][1],
        'name_b': KING_WEN[2 * k + 1][1],
        'mask': mask,
        'sig': xor_sig(a),
        'is_palindrome': is_palindrome(a) and is_palindrome(b),
    })


# ─── 1. Reading direction analysis for inversion pairs ─────────────────────

def reading_direction():
    """
    For inversion pairs, the two hexagrams are the same pattern read in 
    opposite directions. Which reading is consistently chosen as "first"?
    
    Define: for hexagram a, let val = to_int(a) and rev_val = to_int(reverse(a)).
    If val < rev_val: bottom-to-top reading gives the "smaller" number.
    If val > rev_val: bottom-to-top reading gives the "larger" number.
    
    The pair is (a, reverse(a)). The first hexagram a defines a "reading direction."
    """
    print("=" * 80)
    print("1. READING DIRECTION FOR INVERSION PAIRS")
    print("=" * 80)
    
    inv_pairs = [p for p in pairs if not p['is_palindrome']]
    
    print(f"\n  {'Pair':>4s}  {'Hex A':>6s}  {'Val A':>5s} {'Val B':>5s}  "
          f"{'A<B':>3s}  {'L1A':>3s} {'L6A':>3s}  Names")
    
    a_smaller = 0
    l1_yang_count = 0
    l6_yang_count = 0
    
    for p in inv_pairs:
        a = p['a']
        b = p['b']
        va = to_int(a)
        vb = to_int(b)
        
        smaller = va < vb
        if smaller:
            a_smaller += 1
        
        l1 = a[0]
        l6 = a[5]
        if l1 == 1:
            l1_yang_count += 1
        if l6 == 1:
            l6_yang_count += 1
        
        a_str = ''.join(map(str, a))
        print(f"  {p['idx']+1:4d}  {a_str}  {va:5d} {vb:5d}  "
              f"{'Y' if smaller else 'N':>3s}  {l1:>3d} {l6:>3d}  "
              f"{p['name_a']}-{p['name_b']}")
    
    print(f"\n  A has smaller binary value: {a_smaller}/28")
    print(f"  A has L1=yang: {l1_yang_count}/28")
    print(f"  A has L6=yang: {l6_yang_count}/28")
    
    # The relationship between L1 and reading direction:
    # For non-palindromic hexagrams with inversion (reverse):
    # reverse swaps L1↔L6, L2↔L5, L3↔L4
    # So if a has L1=1, then b=reverse(a) has L6=1
    # The two hexagrams have "opposite" end lines
    # L1 of first = L6 of second, and L6 of first = L1 of second
    
    # Key insight: for inversion pairs, the choice of which comes first
    # is equivalent to choosing which end line (L1 or L6) is yang
    # ... but only for the lines that differ
    
    # More precisely: for lines that DO swap (Li ≠ L(7-i)):
    # the first hexagram's lower line is the one that appears
    
    print(f"\n  Line-by-line analysis of first hexagram:")
    line_yang = [0] * DIMS
    line_yin = [0] * DIMS
    for p in inv_pairs:
        for i in range(DIMS):
            if p['a'][i] == 1:
                line_yang[i] += 1
            else:
                line_yin[i] += 1
    
    for i in range(DIMS):
        print(f"    L{i+1}: yang={line_yang[i]}, yin={line_yin[i]} "
              f"(yang rate: {line_yang[i]/28:.3f})")


# ─── 2. The 14/14 split structure ──────────────────────────────────────────

def split_structure():
    """
    Every simple binary rule on inversion pairs gives exactly 14/14.
    Are the same 14 pairs always on the same side, or does the split change?
    """
    print("\n" + "=" * 80)
    print("2. THE 14/14 SPLIT STRUCTURE")
    print("=" * 80)
    
    inv_pairs = [p for p in pairs if not p['is_palindrome']]
    inv_indices = [p['idx'] for p in inv_pairs]
    
    # Define several rules and see which pairs each rule selects
    rules = {}
    
    # binary_high: to_int(a) > to_int(b)
    rules['binary_high'] = [1 if to_int(p['a']) > to_int(p['b']) else 0 for p in inv_pairs]
    
    # first_diff_yang: first differing line (from bottom) has a=yang
    def first_diff(a, b, from_top=False):
        rng = range(DIMS-1,-1,-1) if from_top else range(DIMS)
        for i in rng:
            if a[i] != b[i]:
                return a[i]
        return -1
    
    rules['first_diff_bot_yang'] = [first_diff(p['a'], p['b'], False) for p in inv_pairs]
    rules['first_diff_top_yang'] = [first_diff(p['a'], p['b'], True) for p in inv_pairs]
    rules['revbin_high'] = [1 if to_int(list(reversed(p['a']))) > to_int(list(reversed(p['b']))) else 0 for p in inv_pairs]
    
    # Check if binary_high == first_diff_bot_yang
    print(f"\n  Rule equivalences on inversion pairs:")
    for r1 in rules:
        for r2 in rules:
            if r1 < r2:
                match = sum(1 for a, b in zip(rules[r1], rules[r2]) if a == b)
                if match == 28 or match == 0:
                    rel = "identical" if match == 28 else "complement"
                    print(f"    {r1} vs {r2}: {rel}")
                else:
                    print(f"    {r1} vs {r2}: {match}/28 match")
    
    # For inversion pairs, binary_high(a,b) = first_diff_bot_yang(a,b)?
    # Proof: reverse(a) = b means b[i] = a[5-i].
    # binary value: a = sum(a[i] * 2^(5-i)), b = sum(a[5-i] * 2^(5-i)) = sum(a[j] * 2^j)
    # So to_int(a) vs to_int(b) compares reading left-to-right vs right-to-left.
    # The first differing bit from left (MSB) determines which is larger.
    # For first_diff_bot: first i where a[i] != b[i] = a[i] != a[5-i]
    # For binary: first i (from left, i.e. from L1) where a[i] != a[5-i]
    # These are the SAME comparison! So binary_high == first_diff_bot_yang.
    
    print(f"\n  Algebraic note: for inversion pairs (b = reverse(a)):")
    print(f"    to_int(a) = Σ a[i]·2^(5-i)")
    print(f"    to_int(b) = Σ a[5-i]·2^(5-i) = Σ a[j]·2^j")
    print(f"    So to_int(a) > to_int(b) iff the MSB (L1) reading wins")
    print(f"    This is equivalent to: first asymmetric line pair (L_k, L_{7-k})")
    print(f"    has L_k = yang (i.e., bottom line yang).")
    print(f"    And also equivalent to first_diff_bot_yang.")
    
    # Show which pairs go which way
    bin_high = rules['binary_high']
    group_1 = [inv_pairs[i]['idx']+1 for i in range(28) if bin_high[i] == 1]
    group_0 = [inv_pairs[i]['idx']+1 for i in range(28) if bin_high[i] == 0]
    print(f"\n  Binary-high group (14 pairs): {group_1}")
    print(f"  Binary-low group (14 pairs):  {group_0}")
    
    # Pattern: first 10 pairs are mostly group 1, second 18 mostly group 0
    # Is this the upper/lower canon split?
    upper_in_1 = [p for p in group_1 if p <= 15]
    lower_in_1 = [p for p in group_1 if p > 15]
    print(f"\n  Upper canon (1-15) in binary-high group: {upper_in_1} ({len(upper_in_1)})")
    print(f"  Lower canon (16-32) in binary-high group: {lower_in_1} ({len(lower_in_1)})")


# ─── 3. Octet pattern analysis ─────────────────────────────────────────────

def octet_analysis():
    """
    Binary frame by octet: 4,3,2,1,0,2,3,2
    This looks like a descending then ascending pattern.
    Is it statistically significant?
    """
    print("\n" + "=" * 80)
    print("3. OCTET PATTERN IN BINARY FRAME")
    print("=" * 80)
    
    # Binary frame: 1 if to_int(a) > to_int(b)
    binary_bits = []
    for p in pairs:
        binary_bits.append(1 if to_int(p['a']) > to_int(p['b']) else 0)
    
    octets = []
    for i in range(8):
        oct_bits = binary_bits[4*i:4*i+4]
        octets.append(sum(oct_bits))
    
    print(f"  Binary frame: {''.join(str(b) for b in binary_bits)}")
    print(f"  By octet: {octets}")
    print(f"  Pattern: {' → '.join(str(o) for o in octets)}")
    
    # Test: how often does a random 32-bit string produce this exact 
    # descending-then-ascending pattern in octets?
    actual_octets = octets
    
    # More general: test the "V-shape" quality
    # Descending for first 5 octets, then ascending?
    # Or: monotone decreasing from 4 to 0 in first 5?
    first_5_monotone_dec = all(octets[i] >= octets[i+1] for i in range(4))
    print(f"\n  First 5 octets monotone decreasing (4→0): {first_5_monotone_dec}")
    print(f"  Sequence: {octets[:5]}")
    
    # Monte Carlo: how often does random orientation produce:
    # (a) this exact octet sequence
    # (b) a monotone decrease in first 5 octets
    # (c) a V-shape (decrease then increase)
    
    count_exact = 0
    count_mono_dec_5 = 0
    count_v_shape = 0
    count_4_start = 0  # starts with octet sum = 4
    
    for _ in range(N_TRIALS):
        rand_bits = RNG.integers(0, 2, size=32)
        rand_octets = [sum(rand_bits[4*i:4*i+4]) for i in range(8)]
        
        if rand_octets == actual_octets:
            count_exact += 1
        
        if all(rand_octets[i] >= rand_octets[i+1] for i in range(4)):
            count_mono_dec_5 += 1
        
        # V-shape: find minimum, check decrease before and increase after
        min_idx = rand_octets.index(min(rand_octets))
        is_v = (all(rand_octets[i] >= rand_octets[i+1] for i in range(min_idx)) and
                all(rand_octets[i] <= rand_octets[i+1] for i in range(min_idx, 7)))
        if is_v:
            count_v_shape += 1
        
        if rand_octets[0] == 4:
            count_4_start += 1
    
    print(f"\n  Monte Carlo ({N_TRIALS} trials):")
    print(f"    Exact octet match: {count_exact}/{N_TRIALS} "
          f"(p={count_exact/N_TRIALS:.6f})")
    print(f"    First 5 octets monotone decreasing: {count_mono_dec_5}/{N_TRIALS} "
          f"(p={count_mono_dec_5/N_TRIALS:.6f})")
    print(f"    V-shape (dec then inc): {count_v_shape}/{N_TRIALS} "
          f"(p={count_v_shape/N_TRIALS:.6f})")
    print(f"    First octet = 4/4: {count_4_start}/{N_TRIALS} "
          f"(p={count_4_start/N_TRIALS:.5f})")
    
    # But wait — the binary frame depends on which hexagram is first, 
    # and the "binary high" criterion is not invariant under the choice.
    # We need to test this against random orientations of the SAME pairs.
    
    print(f"\n  Monte Carlo: random orientation of KW pairs (same pairs, random first/second)")
    count_exact_kw = 0
    count_mono_dec_5_kw = 0
    
    for _ in range(N_TRIALS):
        flips = RNG.integers(0, 2, size=32)
        rand_binary = []
        for k, p in enumerate(pairs):
            a, b = p['a'], p['b']
            if flips[k]:
                a, b = b, a
            rand_binary.append(1 if to_int(a) > to_int(b) else 0)
        
        rand_octets = [sum(rand_binary[4*i:4*i+4]) for i in range(8)]
        
        if rand_octets == actual_octets:
            count_exact_kw += 1
        
        if all(rand_octets[i] >= rand_octets[i+1] for i in range(4)):
            count_mono_dec_5_kw += 1
    
    print(f"    Exact octet match: {count_exact_kw}/{N_TRIALS} "
          f"(p={count_exact_kw/N_TRIALS:.6f})")
    print(f"    First 5 octets monotone decreasing: {count_mono_dec_5_kw}/{N_TRIALS} "
          f"(p={count_mono_dec_5_kw/N_TRIALS:.6f})")


# ─── 4. Position coordinates in factored basis ─────────────────────────────

def factored_basis_deep():
    """
    The orbit signature is (L1⊕L6, L2⊕L5, L3⊕L4) — this identifies the orbit.
    Within each orbit, a hexagram is specified by its "position" — a 3-bit value.
    
    One natural choice of position: (L1, L2, L3) — the bottom-half lines.
    Another: the factored basis from the analysis_utils.
    
    For inversion pairs: if a = (l1,l2,l3,l4,l5,l6), then b = (l6,l5,l4,l3,l2,l1).
    Both have the same signature (l1⊕l6, l2⊕l5, l3⊕l4).
    Position of a: (l1,l2,l3). Position of b: (l6,l5,l4).
    
    The mask is the XOR: for inversion, the mask in position space is 
    (l1⊕l6, l2⊕l5, l3⊕l4) = the orbit signature itself!
    So mask = sig, which is the key identity from iter2.
    
    The question is: given the orbit and mask (which together define the pair),
    which of the two positions is chosen first?
    """
    print("\n" + "=" * 80)
    print("4. POSITION COORDINATES IN FACTORED BASIS")
    print("=" * 80)
    
    # For each pair, compute position of first hex: (L1, L2, L3)
    print(f"\n  {'Pair':>4s}  {'Orbit':>5s}  {'Pos A':>5s} {'Pos B':>5s}  "
          f"{'Pos diff':>8s}  {'Orbit=diff':>10s}")
    
    orbit_pos_data = defaultdict(list)
    
    for p in pairs:
        a = p['a']
        sig = p['sig']
        pos_a = a[:3]
        pos_b = p['b'][:3]
        pos_diff = tuple(x ^ y for x, y in zip(pos_a, pos_b))
        
        sig_str = ''.join(map(str, sig))
        pa_str = ''.join(map(str, pos_a))
        pb_str = ''.join(map(str, pos_b))
        diff_str = ''.join(map(str, pos_diff))
        matches = pos_diff == sig
        
        orbit_pos_data[sig].append({
            'pair_idx': p['idx'],
            'pos_a': pos_a,
            'pos_b': pos_b,
        })
        
        print(f"  {p['idx']+1:4d}  {sig_str}  {pa_str} {pb_str}  "
              f"{diff_str:>8s}  {'YES' if matches else 'no':>10s}")
    
    # Verify: position difference = orbit signature always
    all_match = all(
        tuple(p['a'][i] ^ p['b'][i] for i in range(3)) == p['sig']
        for p in pairs
    )
    print(f"\n  Position diff = orbit sig for all pairs: {all_match}")
    
    # Within each orbit, what positions are chosen as "first"?
    print(f"\n  First-hexagram positions by orbit:")
    for sig in sorted(orbit_pos_data.keys()):
        items = orbit_pos_data[sig]
        positions = [d['pos_a'] for d in items]
        pos_strs = [f"{''.join(map(str, p))}" for p in positions]
        print(f"    Orbit {sig}: first positions = {pos_strs}")
        
        # Are the 4 first-positions a coset of anything?
        # In Z₂³, a coset of a subgroup H is {a ⊕ h : h ∈ H} for some a.
        # Check: do they form a 2-dimensional coset?
        pos_set = set(positions)
        if len(pos_set) == 4:
            # Check all pairs of XORs
            xors = set()
            pos_list = list(pos_set)
            for i in range(4):
                for j in range(i+1, 4):
                    x = tuple(a ^ b for a, b in zip(pos_list[i], pos_list[j]))
                    xors.add(x)
            print(f"           XORs between positions: {sorted(xors)}")
            # If they form a coset of a 2-dim subgroup, there should be 3 non-zero XORs
            # forming a subgroup (closed under XOR)
            if len(xors) == 3:
                xor_list = list(xors)
                closure = tuple(a ^ b for a, b in zip(xor_list[0], xor_list[1]))
                if closure in xors:
                    print(f"           → Forms a coset of subgroup generated by {xor_list[:2]}")
    
    # The position trajectory through the sequence
    print(f"\n  Position trajectory (all 64 hexagrams):")
    pos_trajectory = []
    for i in range(64):
        h = M[i]
        pos = h[:3]
        pos_trajectory.append(pos)
    
    # Show in pairs
    for k in range(N_PAIRS):
        pa = pos_trajectory[2*k]
        pb = pos_trajectory[2*k+1]
        sig = xor_sig(M[2*k])
        print(f"    Pair {k+1:2d}: ({','.join(map(str, pa))}) → ({','.join(map(str, pb))})  "
              f"orbit={sig}")


# ─── 5. Information content of orientation ──────────────────────────────────

def information_analysis():
    """
    How many bits of information are in the orientation?
    The inversion frame is trivial (all 1s → 0 bits).
    The binary frame has 17/15 balance → near-maximal entropy.
    But for inversion pairs, the binary frame is determined by 
    which asymmetric line pair has the bottom line yang.
    
    This means: for each inversion pair, there's one "meaningful" bit
    (which reading direction). 28 bits for inversion pairs.
    For complement pairs, there's also one bit. 4 bits.
    Total: 32 bits.
    
    But the inversion frame shows these are NOT independent choices —
    they're all "original first" which happens to map to reverse(a)=b.
    The question is whether the 32-bit binary frame string has structure
    beyond what we'd expect.
    """
    print("\n" + "=" * 80)
    print("5. INFORMATION CONTENT")
    print("=" * 80)
    
    binary_bits = []
    for p in pairs:
        binary_bits.append(1 if to_int(p['a']) > to_int(p['b']) else 0)
    
    bit_str = ''.join(str(b) for b in binary_bits)
    print(f"  Binary orientation: {bit_str}")
    print(f"  Balance: {sum(binary_bits)}/32")
    
    # Compute entropy
    p1 = sum(binary_bits) / 32
    p0 = 1 - p1
    if p0 > 0 and p1 > 0:
        entropy = -(p0 * np.log2(p0) + p1 * np.log2(p1))
    else:
        entropy = 0
    print(f"  Per-bit entropy: {entropy:.4f} bits")
    print(f"  Total naive entropy: {entropy * 32:.2f} bits (max 32)")
    
    # Sequential mutual information
    mi_sum = 0
    for lag in [1, 2, 4, 8, 16]:
        joint = Counter()
        for i in range(32 - lag):
            joint[(binary_bits[i], binary_bits[i + lag])] += 1
        
        total = 32 - lag
        mi = 0
        for (x, y), count in joint.items():
            pxy = count / total
            px = sum(1 for b in binary_bits[:32-lag] if b == x) / total
            py = sum(1 for b in binary_bits[lag:] if b == y) / total
            if pxy > 0 and px > 0 and py > 0:
                mi += pxy * np.log2(pxy / (px * py))
        
        print(f"  Mutual information at lag {lag:2d}: {mi:.4f} bits")
    
    # Kolmogorov-like: what's the shortest description?
    # Count runs
    runs = 1
    for i in range(1, 32):
        if binary_bits[i] != binary_bits[i-1]:
            runs += 1
    print(f"  Number of runs: {runs}")
    print(f"  Run-length encoding: {runs} transitions → ~{np.log2(32)*runs:.1f} bits")
    
    # The binary string reversed (pairs in reverse order)
    rev_bits = binary_bits[::-1]
    rev_str = ''.join(str(b) for b in rev_bits)
    
    # XOR with complement
    comp_bits = [1 - b for b in binary_bits]
    comp_str = ''.join(str(b) for b in comp_bits)
    
    # XOR of first half and second half
    xor_halves = [binary_bits[i] ^ binary_bits[i + 16] for i in range(16)]
    xor_str = ''.join(str(b) for b in xor_halves)
    
    print(f"\n  Symmetry tests:")
    print(f"    Original:  {bit_str}")
    print(f"    Reversed:  {rev_str}")
    print(f"    Complement:{comp_str}")
    print(f"    XOR halves:{xor_str} ({sum(xor_halves)}/16)")
    
    # Hamming distance between first and second half
    h12 = sum(binary_bits[i] != binary_bits[i+16] for i in range(16))
    print(f"    Hamming(first half, second half) = {h12}/16")
    
    # Is the second half close to the reverse-complement of the first?
    rev_comp = [1 - binary_bits[15 - i] for i in range(16)]
    h_rc = sum(binary_bits[i+16] != rev_comp[i] for i in range(16))
    print(f"    Hamming(second half, rev-comp of first) = {h_rc}/16")


# ─── 6. Upper canon vs lower canon inversion structure ──────────────────────

def canon_structure():
    """
    The traditional division: hex 1-30 = upper canon, 31-64 = lower canon.
    Upper = pairs 1-15, Lower = pairs 16-32.
    
    Is the orientation different between upper and lower?
    """
    print("\n" + "=" * 80)
    print("6. CANON STRUCTURE")
    print("=" * 80)
    
    binary_bits = [1 if to_int(p['a']) > to_int(p['b']) else 0 for p in pairs]
    
    upper = binary_bits[:15]
    lower = binary_bits[15:]
    
    print(f"  Upper canon (pairs 1-15): {''.join(str(b) for b in upper)} ({sum(upper)}/15)")
    print(f"  Lower canon (pairs 16-32): {''.join(str(b) for b in lower)} ({sum(lower)}/17)")
    
    # For inversion pairs only
    inv_upper = [(p, 1 if to_int(p['a']) > to_int(p['b']) else 0) 
                 for p in pairs[:15] if not p['is_palindrome']]
    inv_lower = [(p, 1 if to_int(p['a']) > to_int(p['b']) else 0) 
                 for p in pairs[15:] if not p['is_palindrome']]
    
    u_ones = sum(b for _, b in inv_upper)
    l_ones = sum(b for _, b in inv_lower)
    
    print(f"\n  Inversion pairs only:")
    print(f"    Upper (excl complement): {u_ones}/{len(inv_upper)} binary-high first")
    print(f"    Lower (excl complement): {l_ones}/{len(inv_lower)} binary-high first")
    
    # The switch point: where does binary_high change from mostly 1 to mostly 0?
    cumsum = np.cumsum(binary_bits)
    expected = np.arange(1, 33) * 17 / 32
    deviation = cumsum - expected
    
    print(f"\n  Cumulative binary-high minus expected:")
    for i in range(32):
        bar = '+' * max(0, int(deviation[i]*2)) + '-' * max(0, -int(deviation[i]*2))
        print(f"    Pair {i+1:2d}: cum={cumsum[i]:2.0f}, "
              f"dev={deviation[i]:+.2f} {bar}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("THREADS A+B: DEEP ANALYSIS")
    print("=" * 80)
    
    reading_direction()
    split_structure()
    octet_analysis()
    factored_basis_deep()
    information_analysis()
    canon_structure()


if __name__ == "__main__":
    main()
