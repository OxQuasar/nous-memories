"""
Thread B: The Traditional Rule

Test whether a single structural rule recovers King Wen's first/second
assignment within each pair. 

Traditional claim: pairs are formed by inversion (flip upside-down), 
palindromes by complement. The "original" comes first. 
But what defines "original"?

Tests:
1. Verify inversion/complement pairing for all 32 pairs
2. Test candidate structural rules for orientation
3. Test reading direction preference for non-palindromic pairs
4. Test whether orientation correlates with sequence position
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter2')

import numpy as np
from collections import Counter, defaultdict
from itertools import product as iproduct
from sequence import KING_WEN, all_bits
from analysis_utils import VALID_MASKS, xor_sig, xor_tuple, hamming

DIMS = 6
N_PAIRS = 32
N_TRIALS = 10000
RNG = np.random.default_rng(42)

M = [tuple(h) for h in all_bits()]


# ─── Helpers ────────────────────────────────────────────────────────────────

def reverse_bits(h):
    return tuple(h[5-i] for i in range(DIMS))

def complement(h):
    return tuple(1 - x for x in h)

def weight(h):
    return sum(h)

def to_int(h):
    """Binary value treating bit string as written (L1 L2 L3 L4 L5 L6)."""
    val = 0
    for bit in h:
        val = val * 2 + bit
    return val

def to_int_reversed(h):
    """Binary value with reversed bit order (L6 L5 L4 L3 L2 L1)."""
    val = 0
    for bit in reversed(h):
        val = val * 2 + bit
    return val

def is_palindrome(h):
    return h == reverse_bits(h)

def lower_trigram(h):
    return h[:3]

def upper_trigram(h):
    return h[3:]

def trigram_int(t):
    return t[0]*4 + t[1]*2 + t[2]


# ─── Build pairs ────────────────────────────────────────────────────────────

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


# ─── 1. Verify pairing rule ────────────────────────────────────────────────

def verify_pairing():
    """Verify that all pairs follow inversion (or complement for palindromes)."""
    print("=" * 80)
    print("1. PAIRING RULE VERIFICATION")
    print("=" * 80)
    
    inversion_pairs = 0
    complement_pairs = 0
    exceptions = []
    
    for p in pairs:
        a, b = p['a'], p['b']
        
        if reverse_bits(a) == b:
            inversion_pairs += 1
            p['pair_type'] = 'inversion'
            p['original'] = 'a'  # a inverted = b
        elif reverse_bits(b) == a:
            inversion_pairs += 1
            p['pair_type'] = 'inversion'
            p['original'] = 'b'  # but b inverted = a, so b would be "original"?
            # Actually: if reverse(a) != b but reverse(b) == a, 
            # then a = reverse(b), meaning a is the inversion of b
            # In the traditional view, the "first" is the original...
            # Let's just check both directions
        elif complement(a) == b:
            complement_pairs += 1
            p['pair_type'] = 'complement'
            p['original'] = 'a'
        elif complement(b) == a:
            complement_pairs += 1
            p['pair_type'] = 'complement'
            p['original'] = 'b'  # b complement = a
        else:
            exceptions.append(p)
            p['pair_type'] = 'other'
            p['original'] = '?'
    
    # Actually let me redo this more carefully
    # For inversion pairs: reverse(a) should equal b OR reverse(b) should equal a
    # These are equivalent: reverse(a) == b iff reverse(b) == a (since reverse is involution)
    
    print(f"\n  Checking: for each pair, does reverse(first) == second?")
    
    forward_inversion = 0  # reverse(a) == b
    backward_inversion = 0  # reverse(b) == a (same thing for non-palindromes)
    forward_complement = 0  # complement(a) == b
    palindromic_count = 0
    
    for p in pairs:
        a, b = p['a'], p['b']
        rev_a = reverse_bits(a)
        comp_a = complement(a)
        
        is_inv = (rev_a == b)
        is_comp = (comp_a == b)
        is_pal = is_palindrome(a)
        
        p['forward_inv'] = is_inv
        p['forward_comp'] = is_comp
        p['a_is_palindrome'] = is_pal
        
        if is_inv:
            forward_inversion += 1
        if is_comp:
            forward_complement += 1
        if is_pal:
            palindromic_count += 1
    
    print(f"    reverse(first) == second: {forward_inversion}/32")
    print(f"    complement(first) == second: {forward_complement}/32")
    print(f"    first is palindrome: {palindromic_count}/32")
    
    # Detail for non-inversion pairs
    non_inv = [p for p in pairs if not p['forward_inv']]
    if non_inv:
        print(f"\n  Pairs where reverse(first) ≠ second ({len(non_inv)}):")
        for p in non_inv:
            a, b = p['a'], p['b']
            a_str = ''.join(map(str, a))
            b_str = ''.join(map(str, b))
            rev_a = ''.join(map(str, reverse_bits(a)))
            print(f"    Pair {p['idx']+1}: {a_str} → rev={rev_a}, actual={b_str}  "
                  f"palindrome={'Y' if p['a_is_palindrome'] else 'N'}  "
                  f"complement={'Y' if p['forward_comp'] else 'N'}  "
                  f"{p['name_a']}-{p['name_b']}")
    
    # Cross-check: for palindromic pairs, inversion = identity, so 
    # they should all be complement pairs
    print(f"\n  Palindromic pair check:")
    for p in pairs:
        if p['a_is_palindrome']:
            a, b = p['a'], p['b']
            b_pal = is_palindrome(b)
            comp = complement(a) == b
            print(f"    Pair {p['idx']+1}: A pal=Y, B pal={'Y' if b_pal else 'N'}, "
                  f"complement(A)==B: {'Y' if comp else 'N'}  "
                  f"{p['name_a']}-{p['name_b']}")


# ─── 2. Candidate structural rules ─────────────────────────────────────────

def test_structural_rules():
    """Test candidate rules for determining which hexagram comes first."""
    print("\n" + "=" * 80)
    print("2. CANDIDATE STRUCTURAL RULES")
    print("=" * 80)
    
    # For each candidate rule, compute how many pairs it correctly predicts
    rules = {}
    
    # Rule 1: Higher weight (more yang) first
    def rule_weight(a, b):
        return weight(a) > weight(b)
    
    # Rule 2: Lower weight first
    def rule_weight_low(a, b):
        return weight(a) < weight(b)
    
    # Rule 3: Higher binary value first
    def rule_binary_high(a, b):
        return to_int(a) > to_int(b)
    
    # Rule 4: Lower binary value first
    def rule_binary_low(a, b):
        return to_int(a) < to_int(b)
    
    # Rule 5: Higher reversed-binary value first
    def rule_revbin_high(a, b):
        return to_int_reversed(a) > to_int_reversed(b)
    
    # Rule 6: Lower reversed-binary value first
    def rule_revbin_low(a, b):
        return to_int_reversed(a) < to_int_reversed(b)
    
    # Rule 7: Lower trigram has higher binary value
    def rule_lower_tri_high(a, b):
        return trigram_int(lower_trigram(a)) > trigram_int(lower_trigram(b))
    
    # Rule 8: Upper trigram has higher binary value
    def rule_upper_tri_high(a, b):
        return trigram_int(upper_trigram(a)) > trigram_int(upper_trigram(b))
    
    # Rule 9: Lower trigram has lower binary value
    def rule_lower_tri_low(a, b):
        return trigram_int(lower_trigram(a)) < trigram_int(lower_trigram(b))
    
    # Rule 10: Upper trigram has lower binary value
    def rule_upper_tri_low(a, b):
        return trigram_int(upper_trigram(a)) < trigram_int(upper_trigram(b))
    
    # Rule 11: L1 (bottom line) is yang
    def rule_L1_yang(a, b):
        return a[0] > b[0]
    
    # Rule 12: L6 (top line) is yang
    def rule_L6_yang(a, b):
        return a[5] > b[5]
    
    # Rule 13: First line that differs is yang
    def rule_first_diff_yang(a, b):
        for i in range(DIMS):
            if a[i] != b[i]:
                return a[i] > b[i]
        return False  # equal
    
    # Rule 14: First line that differs (from top) is yang
    def rule_first_diff_top_yang(a, b):
        for i in range(DIMS-1, -1, -1):
            if a[i] != b[i]:
                return a[i] > b[i]
        return False
    
    # Rule 15: First line that differs is yin
    def rule_first_diff_yin(a, b):
        for i in range(DIMS):
            if a[i] != b[i]:
                return a[i] < b[i]
        return False
    
    # Rule 16: First line that differs (from top) is yin
    def rule_first_diff_top_yin(a, b):
        for i in range(DIMS-1, -1, -1):
            if a[i] != b[i]:
                return a[i] < b[i]
        return False
    
    # Rule 17: Sum of lower trigram > sum of upper trigram
    def rule_lower_heavier(a, b):
        la = sum(lower_trigram(a))
        lb = sum(lower_trigram(b))
        return la > lb
    
    # Rule 18: for inversion pairs, the "reading" with lower binary value is first
    # This tests reading direction: bottom-to-top vs top-to-bottom
    def rule_reading_direction(a, b):
        # a is what's written; reverse(a) gives the "other reading"
        # If to_int(a) < to_int(reverse(a)), we chose the lower reading
        return to_int(a) < to_int(reverse_bits(a))
    
    all_rules = {
        'weight_high_first': rule_weight,
        'weight_low_first': rule_weight_low,
        'binary_high_first': rule_binary_high,
        'binary_low_first': rule_binary_low,
        'revbin_high_first': rule_revbin_high,
        'revbin_low_first': rule_revbin_low,
        'lower_tri_high': rule_lower_tri_high,
        'upper_tri_high': rule_upper_tri_high,
        'lower_tri_low': rule_lower_tri_low,
        'upper_tri_low': rule_upper_tri_low,
        'L1_yang': rule_L1_yang,
        'L6_yang': rule_L6_yang,
        'first_diff_yang': rule_first_diff_yang,
        'first_diff_top_yang': rule_first_diff_top_yang,
        'first_diff_yin': rule_first_diff_yin,
        'first_diff_top_yin': rule_first_diff_top_yin,
        'lower_tri_heavier': rule_lower_heavier,
        'reading_lower_val': rule_reading_direction,
    }
    
    # Test each rule
    results = []
    for rname, rfunc in all_rules.items():
        correct = 0
        applicable = 0
        exceptions = []
        
        for p in pairs:
            a, b = p['a'], p['b']
            try:
                pred = rfunc(a, b)
                applicable += 1
                if pred:
                    correct += 1
                else:
                    exceptions.append(p['idx'] + 1)
            except:
                pass
        
        results.append((rname, correct, applicable, exceptions))
    
    # Sort by accuracy
    results.sort(key=lambda x: -x[1])
    
    print(f"\n  {'Rule':>25s}  {'Correct':>7s}  {'Applic':>6s}  {'Rate':>6s}  Exceptions")
    print("  " + "-" * 75)
    for rname, correct, applicable, exceptions in results:
        rate = correct / applicable if applicable > 0 else 0
        exc_str = str(exceptions[:10]) if exceptions else '[]'
        if len(exceptions) > 10:
            exc_str += '...'
        print(f"  {rname:>25s}  {correct:>4d}/32  {applicable:>6d}  {rate:>6.3f}  {exc_str}")
    
    # Best rule analysis
    best = results[0]
    print(f"\n  Best rule: {best[0]} ({best[1]}/32 = {best[1]/32*100:.1f}%)")
    if best[3]:
        print(f"  Exceptions at pairs: {best[3]}")
        for pidx in best[3]:
            p = pairs[pidx - 1]
            a_str = ''.join(map(str, p['a']))
            b_str = ''.join(map(str, p['b']))
            print(f"    Pair {pidx}: {a_str} vs {b_str}  "
                  f"({p['name_a']}-{p['name_b']})")
    
    return results


# ─── 3. Separate analysis for inversion vs complement pairs ────────────────

def separate_rule_test():
    """Test rules separately for inversion pairs and complement pairs."""
    print("\n" + "=" * 80)
    print("3. RULES BY PAIR TYPE (Inversion vs Complement)")
    print("=" * 80)
    
    inv_pairs = [p for p in pairs if not p['is_palindrome']]
    comp_pairs = [p for p in pairs if p['is_palindrome']]
    
    print(f"\n  Inversion pairs: {len(inv_pairs)}")
    print(f"  Complement pairs: {len(comp_pairs)}")
    
    # For inversion pairs: test reading direction
    print(f"\n  --- Inversion pairs ({len(inv_pairs)}) ---")
    
    # Which reading direction is chosen?
    bottom_up_lower = 0  # bottom-to-top reading gives lower binary value
    for p in inv_pairs:
        a = p['a']
        val_as_is = to_int(a)
        val_reversed = to_int(reverse_bits(a))
        if val_as_is < val_reversed:
            bottom_up_lower += 1
    
    print(f"  First hex has lower binary value than its reversal: "
          f"{bottom_up_lower}/{len(inv_pairs)}")
    
    # Test: heavier first for inversion pairs
    heavier_first = sum(1 for p in inv_pairs if weight(p['a']) > weight(p['b']))
    lighter_first = sum(1 for p in inv_pairs if weight(p['a']) < weight(p['b']))
    equal_weight = sum(1 for p in inv_pairs if weight(p['a']) == weight(p['b']))
    print(f"  Heavier first: {heavier_first}, lighter first: {lighter_first}, "
          f"equal: {equal_weight}")
    
    # For inversion pairs, weight(a) + weight(reverse(a)) = weight(a) + weight(a) = 2*weight(a)
    # No wait: weight(reverse(a)) = weight(a) since reversal preserves weight!
    # So inversion pairs always have equal weight.
    print(f"  NOTE: inversion preserves weight, so inversion pairs always have equal weight")
    
    # Key test for inversion pairs: L1 value
    l1_yang = sum(1 for p in inv_pairs if p['a'][0] == 1)
    print(f"  First hex has L1=yang: {l1_yang}/{len(inv_pairs)}")
    l6_yang = sum(1 for p in inv_pairs if p['a'][5] == 1)
    print(f"  First hex has L6=yang: {l6_yang}/{len(inv_pairs)}")
    
    # Lower trigram comparison
    lt_higher = sum(1 for p in inv_pairs 
                    if trigram_int(lower_trigram(p['a'])) > trigram_int(lower_trigram(p['b'])))
    lt_lower = sum(1 for p in inv_pairs 
                   if trigram_int(lower_trigram(p['a'])) < trigram_int(lower_trigram(p['b'])))
    lt_equal = sum(1 for p in inv_pairs 
                   if trigram_int(lower_trigram(p['a'])) == trigram_int(lower_trigram(p['b'])))
    print(f"  First hex lower-tri higher: {lt_higher}, lower: {lt_lower}, equal: {lt_equal}")
    
    # For complement pairs
    print(f"\n  --- Complement pairs ({len(comp_pairs)}) ---")
    
    heavier_first_c = sum(1 for p in comp_pairs if weight(p['a']) > weight(p['b']))
    lighter_first_c = sum(1 for p in comp_pairs if weight(p['a']) < weight(p['b']))
    equal_c = sum(1 for p in comp_pairs if weight(p['a']) == weight(p['b']))
    print(f"  Heavier first: {heavier_first_c}, lighter: {lighter_first_c}, equal: {equal_c}")
    
    # For complement: weight(a) + weight(complement(a)) = 6
    # So if weight(a) > 3, a is heavier; if weight(a) < 3, complement is heavier
    # weight(a) == 3: equal
    for p in comp_pairs:
        a, b = p['a'], p['b']
        wa, wb = weight(a), weight(b)
        a_str = ''.join(map(str, a))
        b_str = ''.join(map(str, b))
        print(f"    Pair {p['idx']+1}: {a_str}(w={wa}) vs {b_str}(w={wb})  "
              f"{'heavier first' if wa > wb else 'lighter first' if wa < wb else 'equal'}  "
              f"{p['name_a']}-{p['name_b']}")


# ─── 4. Composite rules ────────────────────────────────────────────────────

def test_composite_rules():
    """Test rules that handle inversion and complement pairs differently."""
    print("\n" + "=" * 80)
    print("4. COMPOSITE RULES (different rule per pair type)")
    print("=" * 80)
    
    inv_pairs = [p for p in pairs if not p['is_palindrome']]
    comp_pairs = [p for p in pairs if p['is_palindrome']]
    
    # For complement pairs, the clear signal is weight
    # Test: heavier first for complement pairs + various rules for inversion
    
    # Check if complement pairs are uniformly heavier-first
    comp_heavier = all(weight(p['a']) > weight(p['b']) for p in comp_pairs)
    comp_lighter = all(weight(p['a']) < weight(p['b']) for p in comp_pairs)
    print(f"\n  Complement pairs all heavier-first: {comp_heavier}")
    print(f"  Complement pairs all lighter-first: {comp_lighter}")
    
    if not comp_heavier and not comp_lighter:
        comp_heavier_count = sum(1 for p in comp_pairs if weight(p['a']) > weight(p['b']))
        print(f"  Complement heavier-first count: {comp_heavier_count}/{len(comp_pairs)}")
    
    # For inversion pairs, test various rules
    inv_rules = {
        'binary_high': lambda a, b: to_int(a) > to_int(b),
        'binary_low': lambda a, b: to_int(a) < to_int(b),
        'revbin_high': lambda a, b: to_int_reversed(a) > to_int_reversed(b),
        'revbin_low': lambda a, b: to_int_reversed(a) < to_int_reversed(b),
        'first_diff_yang': lambda a, b: next((a[i] > b[i] for i in range(DIMS) if a[i] != b[i]), False),
        'first_diff_yin': lambda a, b: next((a[i] < b[i] for i in range(DIMS) if a[i] != b[i]), False),
        'first_diff_top_yang': lambda a, b: next((a[i] > b[i] for i in range(DIMS-1,-1,-1) if a[i] != b[i]), False),
        'first_diff_top_yin': lambda a, b: next((a[i] < b[i] for i in range(DIMS-1,-1,-1) if a[i] != b[i]), False),
        'L1_yang': lambda a, b: a[0] > b[0],
        'L6_yang': lambda a, b: a[5] > b[5],
        'lower_tri_heavier': lambda a, b: sum(a[:3]) > sum(b[:3]),
        'upper_tri_heavier': lambda a, b: sum(a[3:]) > sum(b[3:]),
    }
    
    print(f"\n  Rules tested on inversion pairs ({len(inv_pairs)}):")
    print(f"  {'Rule':>25s}  {'Correct':>7s}  Rate")
    print("  " + "-" * 50)
    
    inv_results = []
    for rname, rfunc in inv_rules.items():
        correct = 0
        exceptions = []
        for p in inv_pairs:
            try:
                if rfunc(p['a'], p['b']):
                    correct += 1
                else:
                    exceptions.append(p['idx'] + 1)
            except StopIteration:
                pass
        inv_results.append((rname, correct, len(inv_pairs), exceptions))
    
    inv_results.sort(key=lambda x: -x[1])
    for rname, correct, total, exceptions in inv_results:
        rate = correct / total if total > 0 else 0
        print(f"  {rname:>25s}  {correct:>4d}/{total}  {rate:.3f}  exc={exceptions[:5]}{'...' if len(exceptions)>5 else ''}")
    
    # Best composite rule
    best_inv = inv_results[0]
    print(f"\n  Best inversion rule: {best_inv[0]} ({best_inv[1]}/{best_inv[2]})")
    if best_inv[3]:
        print(f"  Exceptions at pairs: {best_inv[3]}")


# ─── 5. Sequence position correlation ──────────────────────────────────────

def position_correlation():
    """Test whether orientation correlates with position in sequence."""
    print("\n" + "=" * 80)
    print("5. POSITION CORRELATION")
    print("=" * 80)
    
    # For each pair, compute various orientation bits
    binary_bits = []
    for p in pairs:
        a, b = p['a'], p['b']
        binary_bits.append(1 if to_int(a) > to_int(b) else 0)
    
    positions = np.arange(N_PAIRS)
    bits_arr = np.array(binary_bits, dtype=float)
    
    # Correlation
    if np.std(bits_arr) > 0:
        corr = np.corrcoef(positions, bits_arr)[0, 1]
        print(f"\n  Binary-high-first vs pair position: r = {corr:+.3f}")
    
    # First half vs second half
    first_half = sum(binary_bits[:16])
    second_half = sum(binary_bits[16:])
    print(f"  First 16 pairs binary-high-first: {first_half}/16")
    print(f"  Last 16 pairs binary-high-first: {second_half}/16")
    
    # Upper vs lower canon (pairs 1-15 vs 16-32)
    upper = sum(binary_bits[:15])
    lower = sum(binary_bits[15:])
    print(f"  Upper canon (1-15): {upper}/15")
    print(f"  Lower canon (16-32): {lower}/17")
    
    # Octets
    print(f"\n  By octet (groups of 4 pairs):")
    for oct_idx in range(8):
        start = oct_idx * 4
        end = start + 4
        oct_bits = binary_bits[start:end]
        print(f"    Octet {oct_idx+1} (pairs {start+1}-{end}): "
              f"{''.join(str(b) for b in oct_bits)} ({sum(oct_bits)}/4)")


# ─── 6. Detailed exception analysis ────────────────────────────────────────

def exception_analysis():
    """For the best-performing rules, analyze exceptions in detail."""
    print("\n" + "=" * 80)
    print("6. DETAILED EXCEPTION ANALYSIS")
    print("=" * 80)
    
    # We'll analyze the "first_diff" rules since they're natural
    print("\n  For each pair, show which line first differs and its direction:")
    print(f"  {'Pair':>4s}  {'Hex A':>6s} {'Hex B':>6s}  {'First diff':>10s}  "
          f"{'Direction':>9s}  Names")
    
    for p in pairs:
        a, b = p['a'], p['b']
        first_diff_line = None
        first_diff_dir = None
        for i in range(DIMS):
            if a[i] != b[i]:
                first_diff_line = i + 1
                first_diff_dir = 'A yang' if a[i] == 1 else 'B yang'
                break
        
        first_diff_top_line = None
        first_diff_top_dir = None
        for i in range(DIMS-1, -1, -1):
            if a[i] != b[i]:
                first_diff_top_line = i + 1
                first_diff_top_dir = 'A yang' if a[i] == 1 else 'B yang'
                break
        
        a_str = ''.join(map(str, a))
        b_str = ''.join(map(str, b))
        
        print(f"  {p['idx']+1:4d}  {a_str} {b_str}  "
              f"L{first_diff_line}={first_diff_dir:>7s}  "
              f"L{first_diff_top_line}={'top '+first_diff_top_dir:>9s}  "
              f"{p['name_a']}-{p['name_b']}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("THREAD B: THE TRADITIONAL RULE")
    print("=" * 80)
    
    verify_pairing()
    results = test_structural_rules()
    separate_rule_test()
    test_composite_rules()
    position_correlation()
    exception_analysis()
    
    # Final summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    # Collect the key findings
    inv_pairs = [p for p in pairs if not p['is_palindrome']]
    comp_pairs = [p for p in pairs if p['is_palindrome']]
    
    print(f"\n  Pair types: {len(inv_pairs)} inversion + {len(comp_pairs)} complement = 32")
    
    # Verify: all inversion pairs have reverse(first) == second?
    all_inv_forward = all(reverse_bits(p['a']) == p['b'] for p in inv_pairs)
    all_comp_forward = all(complement(p['a']) == p['b'] for p in comp_pairs)
    print(f"  All inversion pairs: reverse(A) == B: {all_inv_forward}")
    print(f"  All complement pairs: complement(A) == B: {all_comp_forward}")
    
    # Best overall rule accuracy
    best = results[0]
    print(f"\n  Best single rule: {best[0]} ({best[1]}/32 = {best[1]/32*100:.1f}%)")
    print(f"  Exceptions: {best[3]}")


if __name__ == "__main__":
    main()
