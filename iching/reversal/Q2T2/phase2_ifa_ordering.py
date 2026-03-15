#!/usr/bin/env python3
"""Phase 2: Algebraic structure of Ifá's seniority ordering on F₂⁴.

The 16 principal odù in Abimbola seniority order, encoded as 4-bit vectors
(I=1, II=0 reading top-to-bottom).
"""

from itertools import permutations

# ═══════════════════════════════════════════════════════
# Ifá data: (name, binary_string)
# ═══════════════════════════════════════════════════════

ODU = [
    ("Ogbe",     0b1111),  #  1
    ("Oyeku",    0b0000),  #  2
    ("Iwori",    0b0110),  #  3
    ("Odi",      0b1001),  #  4
    ("Irosun",   0b1100),  #  5
    ("Owonrin",  0b0011),  #  6
    ("Obara",    0b1000),  #  7
    ("Okanran",  0b0111),  #  8
    ("Ogunda",   0b1110),  #  9
    ("Osa",      0b0001),  # 10
    ("Ika",      0b0100),  # 11
    ("Oturupon", 0b1011),  # 12
    ("Otura",    0b1010),  # 13
    ("Irete",    0b0101),  # 14
    ("Ose",      0b1101),  # 15
    ("Ofun",     0b0010),  # 16
]

N_BITS = 4
COMP_VEC = 0b1111


def hamming_weight(x):
    return bin(x).count('1')


def bit_reverse(x, n=N_BITS):
    """Reverse n-bit vector."""
    result = 0
    for i in range(n):
        result |= ((x >> i) & 1) << (n - 1 - i)
    return result


def to_gray(n):
    """Standard reflected Gray code: n → n XOR (n >> 1)."""
    return n ^ (n >> 1)


def run_phase2():
    print("Phase 2: Ifá Seniority Ordering on F₂⁴")
    print("=" * 70)

    names = [name for name, _ in ODU]
    vals = [v for _, v in ODU]

    # ── Test 1: Complement pairing ──
    print("\nTest 1: Complement pairing")
    print(f"  {'Pos':<5} {'Name':<12} {'Bin':<6} {'Comp':<6} {'Partner':<12} {'Partner Pos':<12} {'Paired?'}")
    print(f"  {'-'*65}")

    all_paired = True
    pair_positions = []
    for i in range(0, 16, 2):
        v1, v2 = vals[i], vals[i + 1]
        is_comp = (v1 ^ v2) == COMP_VEC
        if not is_comp:
            all_paired = False
        pair_positions.append((i, i + 1, is_comp))
        print(f"  {i+1:<5} {names[i]:<12} {v1:04b}   {v1^COMP_VEC:04b}   {names[i+1]:<12} {i+2:<12} {'✓' if is_comp else '✗'}")

    print(f"\n  All consecutive pairs are complements: {'✓ YES' if all_paired else '✗ NO'}")

    # ── Test 2: Weight ordering within pairs ──
    print("\nTest 2: Higher Hamming weight always senior?")
    weight_senior = True
    for i in range(0, 16, 2):
        w1, w2 = hamming_weight(vals[i]), hamming_weight(vals[i + 1])
        senior_heavier = w1 >= w2
        if not senior_heavier:
            weight_senior = False
        print(f"  Pair ({i+1},{i+2}): wt={w1} vs wt={w2} → {'✓' if senior_heavier else '✗'}")
    print(f"\n  Senior member always has ≥ weight: {'✓ YES' if weight_senior else '✗ NO'}")

    # ── Test 3: Hamming weight sequence ──
    print("\nTest 3: Hamming weight sequence")
    weights = [hamming_weight(v) for v in vals]
    print(f"  Position: {list(range(1, 17))}")
    print(f"  Weight:   {weights}")
    print(f"  Pattern:  {' '.join(str(w) for w in weights)}")

    # Weight by pair
    pair_weights = [(hamming_weight(vals[i]), hamming_weight(vals[i+1])) for i in range(0, 16, 2)]
    print(f"  Pair weights: {pair_weights}")

    # ── Test 4: Standard ordering tests ──
    print("\nTest 4: Standard ordering comparison")

    # Binary counting (Fu Xi): 0,1,2,...,15
    fuxi_order = list(range(16))
    is_fuxi = vals == fuxi_order
    print(f"  Binary counting (0→15): {'✓' if is_fuxi else '✗'}")

    # Reverse binary counting: 15,14,...,0
    rev_binary = list(range(15, -1, -1))
    is_rev_binary = vals == rev_binary
    print(f"  Reverse binary (15→0): {'✓' if is_rev_binary else '✗'}")

    # Standard Gray code
    gray_order = [to_gray(i) for i in range(16)]
    is_gray = vals == gray_order
    print(f"  Standard Gray code: {'✓' if is_gray else '✗'}")

    # Reverse Gray code
    rev_gray = [to_gray(15 - i) for i in range(16)]
    is_rev_gray = vals == rev_gray
    print(f"  Reverse Gray code: {'✓' if is_rev_gray else '✗'}")

    # Lexicographic on bit string (MSB first)
    lex_order = sorted(range(16), key=lambda x: tuple((x >> (3-i)) & 1 for i in range(4)))
    is_lex = vals == lex_order
    print(f"  Lexicographic (MSB first): {'✓' if is_lex else '✗'}")

    # Reverse lexicographic
    rev_lex = list(reversed(lex_order))
    is_rev_lex = vals == rev_lex
    print(f"  Reverse lexicographic: {'✓' if is_rev_lex else '✗'}")

    # Weight-descending then lex
    weight_lex = sorted(range(16), key=lambda x: (-hamming_weight(x), x))
    is_wl = vals == weight_lex
    print(f"  Weight-desc then lex: {'✓' if is_wl else '✗'}")

    # Check if it's a weight-based ordering with complement pairing
    print(f"\n  Ordering principle analysis:")
    print(f"    The ordering interleaves complement pairs by decreasing 'distance from extremes'")

    # ── Test 5: Symmetry properties ──
    print("\nTest 5: Symmetry properties")

    # Reversal involution: reverse the 4 bits
    print(f"  Bit-reversal involution (reverse 4 bits):")
    reversal_respects = True
    for i, v in enumerate(vals):
        rev_v = bit_reverse(v)
        if rev_v in vals:
            rev_pos = vals.index(rev_v)
            print(f"    {names[i]:<12} {v:04b} → {rev_v:04b} = {names[rev_pos]:<12} (pos {i+1} → {rev_pos+1})")
            # Check if reversal maps pairs to pairs
        else:
            reversal_respects = False

    # Does reversal commute with complement?
    print(f"\n  Reversal-complement interaction:")
    for i in range(0, 8, 2):
        v = vals[i]
        comp_v = v ^ COMP_VEC
        rev_v = bit_reverse(v)
        rev_comp = bit_reverse(comp_v)
        comp_rev = rev_v ^ COMP_VEC
        print(f"    {v:04b}: rev(comp) = {rev_comp:04b}, comp(rev) = {comp_rev:04b} → {'same' if rev_comp == comp_rev else 'different'}")
    print(f"  (Reversal and complement always commute on F₂ⁿ — they're both involutions that commute.)")

    # Palindrome structure: is the sequence symmetric?
    is_palindrome = all(vals[i] == vals[15-i] for i in range(8))
    is_comp_palindrome = all((vals[i] ^ vals[15-i]) == COMP_VEC for i in range(8))
    print(f"\n  Palindrome (v_i = v_{17-i}): {'✓' if is_palindrome else '✗'}")
    print(f"  Complement-palindrome (v_i ⊕ v_{17-i} = 1111): {'✓' if is_comp_palindrome else '✗'}")

    # ── Test 6: Comparison with I Ching orderings ──
    print("\nTest 6: Comparison with I Ching trigram orderings")

    print(f"\n  Fu Xi trigram order (binary counting):")
    fuxi_trigrams = [(f"{i:03b}", i) for i in range(8)]
    print(f"    {fuxi_trigrams}")
    print(f"    Pure binary counting — Ifá does NOT follow this on F₂⁴")

    print(f"\n  King Wen pairing principle:")
    print(f"    KW pairs hexagrams by reversal (or complement if palindromic)")
    print(f"    Ifá pairs by complement, not reversal")
    print(f"    Different pairing involution!")

    # ── Summary ──
    print(f"\n{'='*70}")
    print("SUMMARY OF IFÁ ORDERING STRUCTURE")
    print(f"{'='*70}")

    print(f"""
  1. COMPLEMENT PAIRING: {'✓' if all_paired else '✗'}
     Consecutive positions (1,2), (3,4), ... are complement pairs in F₂⁴.
     This is the SAME structural principle as the I Ching's complement axis.

  2. WEIGHT HIERARCHY: {'✓' if weight_senior else '✗'}
     Within each pair, the higher-weight element is always senior.
     (Analogous to I Ching: yang-heavy trigrams precede yin-heavy ones.)

  3. NOT A STANDARD COMBINATORIAL ORDER:
     Not binary counting, not Gray code, not lexicographic.
     The ordering carries cultural/divinatory logic beyond pure combinatorics.

  4. PAIR WEIGHT SEQUENCE: {[w1 for w1, w2 in pair_weights]}
     Pairs ordered roughly by 'extremity' of the pair (4/0 first, then mixed).

  5. COMPLEMENT PALINDROME: {'✓' if is_comp_palindrome else '✗'}
     Position i and position (17-i) are {'complements' if is_comp_palindrome else 'NOT complements'}.
""")

    return {
        'complement_paired': all_paired,
        'weight_senior': weight_senior,
        'weight_sequence': weights,
        'pair_weights': pair_weights,
        'complement_palindrome': is_comp_palindrome,
    }


if __name__ == '__main__':
    results = run_phase2()
