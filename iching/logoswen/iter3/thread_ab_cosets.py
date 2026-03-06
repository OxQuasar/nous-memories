"""
Follow-up: coset structure in position coordinates.

Finding: In 6/8 orbits, the 4 first-hexagram positions form a coset of a 
2-dimensional subgroup in Z₂³. This is strong algebraic structure.

Questions:
1. Which subgroups appear? Is there a pattern?
2. For the 2 orbits where it's NOT a coset, what's different?
3. Those 2 are orbits (0,0,0) and (1,1,1) — the "special" orbits 
   (identity and OMI). Both contain the 4 complement pairs.
4. If we exclude complement pairs from orbits (0,0,0), do the remaining 
   positions form structured subsets?
5. Statistical test: how likely is random orientation to produce 6/8 cosets?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter2')

import numpy as np
from collections import Counter, defaultdict
from itertools import combinations
from sequence import KING_WEN, all_bits
from analysis_utils import xor_sig, xor_tuple

DIMS = 6
N_PAIRS = 32
N_TRIALS = 100000
RNG = np.random.default_rng(42)

M = [tuple(h) for h in all_bits()]


def reverse_bits(h):
    return tuple(h[5-i] for i in range(DIMS))

def complement(h):
    return tuple(1 - x for x in h)

def is_palindrome(h):
    return h == reverse_bits(h)

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


# Build pairs with position info
pairs = []
for k in range(N_PAIRS):
    a = M[2 * k]
    b = M[2 * k + 1]
    mask = xor_tuple(a, b)
    sig = xor_sig(a)
    pairs.append({
        'idx': k,
        'a': a, 'b': b,
        'mask': mask,
        'sig': sig,
        'pos_a': a[:3],
        'pos_b': b[:3],
        'is_palindrome': is_palindrome(a) and is_palindrome(b),
        'num_a': KING_WEN[2 * k][0],
        'name_a': KING_WEN[2 * k][1],
        'name_b': KING_WEN[2 * k + 1][1],
    })


def check_coset(positions):
    """
    Check if a set of 4 positions in Z₂³ form a coset of a 2-dim subgroup.
    A 2-dim subgroup has 4 elements: {0, g1, g2, g1⊕g2}.
    A coset is {a⊕h : h ∈ H} for some a, H.
    
    Equivalently: the 4 elements form a coset iff the set of 6 pairwise XORs
    contains exactly 3 distinct non-zero values that form a subgroup.
    """
    pos_list = list(positions)
    if len(pos_list) != 4:
        return False, None
    
    xors = set()
    for i in range(4):
        for j in range(i+1, 4):
            x = xor3(pos_list[i], pos_list[j])
            xors.add(x)
    
    xors.discard((0,0,0))
    
    if len(xors) != 3:
        return False, None
    
    xor_list = list(xors)
    # Check closure: any two XORed should give the third
    for i in range(3):
        for j in range(i+1, 3):
            result = xor3(xor_list[i], xor_list[j])
            if result != (0,0,0) and result not in xors:
                return False, None
    
    return True, sorted(xors)


# ─── 1. Coset analysis per orbit ───────────────────────────────────────────

def coset_analysis():
    print("=" * 80)
    print("1. COSET STRUCTURE PER ORBIT")
    print("=" * 80)
    
    orbit_data = defaultdict(list)
    for p in pairs:
        orbit_data[p['sig']].append(p)
    
    SUBGROUP_NAMES = {
        ((0,0,1), (0,1,0), (0,1,1)): '{I, M, MI}',
        ((0,0,1), (1,0,0), (1,0,1)): '{I, O, OI}',
        ((0,1,0), (1,0,0), (1,1,0)): '{M, O, OM}',
        ((0,0,1), (1,1,0), (1,1,1)): '{I, OM, OMI}',
        ((0,1,0), (1,0,1), (1,1,1)): '{M, OI, OMI}',
        ((1,0,0), (0,1,1), (1,1,1)): '{O, MI, OMI}',
        ((0,1,1), (1,0,0), (1,1,1)): '{MI, O, OMI}',  # same as above
        ((0,1,1), (1,0,1), (1,1,0)): '{MI, OI, OM}',
    }
    
    coset_count = 0
    
    for sig in sorted(orbit_data.keys()):
        items = orbit_data[sig]
        positions_a = [tuple(p['pos_a']) for p in items]
        positions_b = [tuple(p['pos_b']) for p in items]
        
        is_coset_a, subgroup_a = check_coset(positions_a)
        is_coset_b, subgroup_b = check_coset(positions_b)
        
        sig_str = ''.join(map(str, sig))
        has_pal = any(p['is_palindrome'] for p in items)
        
        print(f"\n  Orbit ({sig_str}){'  [has complement pairs]' if has_pal else ''}:")
        print(f"    Pairs: {[p['idx']+1 for p in items]}")
        print(f"    First positions (A): {[''.join(map(str, p)) for p in positions_a]}")
        print(f"    Second positions (B): {[''.join(map(str, p)) for p in positions_b]}")
        print(f"    A is coset: {is_coset_a}", end="")
        
        if is_coset_a:
            coset_count += 1
            sub_key = tuple(sorted(subgroup_a))
            sg_name = SUBGROUP_NAMES.get(sub_key, str(sub_key))
            print(f"  subgroup = {sg_name}")
        else:
            print()
        
        print(f"    B is coset: {is_coset_b}", end="")
        if is_coset_b:
            sub_key = tuple(sorted(subgroup_b))
            sg_name = SUBGROUP_NAMES.get(sub_key, str(sub_key))
            print(f"  subgroup = {sg_name}")
        else:
            print()
        
        # For non-coset cases, what IS the structure?
        if not is_coset_a:
            xors = set()
            pos_list = list(set(positions_a))
            for i in range(len(pos_list)):
                for j in range(i+1, len(pos_list)):
                    x = xor3(pos_list[i], pos_list[j])
                    xors.add(x)
            print(f"    A pairwise XORs: {sorted(xors)} ({len(xors)} distinct)")
    
    print(f"\n  Coset count (A positions): {coset_count}/8 orbits")
    
    return coset_count


# ─── 2. The special orbits: complement pair analysis ───────────────────────

def complement_pair_deep():
    """
    Orbits (0,0,0) and (1,1,0)/(1,1,1) etc contain complement pairs.
    Wait — which orbits have complement pairs?
    
    Complement pairs: palindromic hexagrams (sig = 0,0,0 since L_i = L_{7-i}).
    So ALL complement pairs are in orbit (0,0,0).
    
    But orbit (0,0,0) has 4 pairs visiting it, and the 4 complement pairs
    are pairs 1, 14, 15, 31. Let's check which orbit each is in.
    """
    print("\n" + "=" * 80)
    print("2. COMPLEMENT PAIRS — ORBIT ANALYSIS")
    print("=" * 80)
    
    comp_pairs = [p for p in pairs if p['is_palindrome']]
    
    print(f"  Complement pairs and their orbits:")
    for p in comp_pairs:
        print(f"    Pair {p['idx']+1}: orbit={p['sig']}  "
              f"{p['name_a']}-{p['name_b']}  "
              f"pos_a={''.join(map(str, p['pos_a']))}  "
              f"pos_b={''.join(map(str, p['pos_b']))}")
    
    # Palindromic means sig = (0,0,0). Verify:
    all_zero_sig = all(p['sig'] == (0,0,0) for p in comp_pairs)
    print(f"\n  All complement pairs in orbit (0,0,0): {all_zero_sig}")
    
    # What's special about orbit (0,0,0)?
    # It has 8 hexagrams where L1=L6, L2=L5, L3=L4 (palindromes).
    # These 8 palindromes are paired into 4 complement pairs.
    # Plus, orbit (0,0,0) is visited by other pairs too... wait, is it?
    
    orbit_000 = [p for p in pairs if p['sig'] == (0,0,0)]
    print(f"\n  All pairs in orbit (0,0,0): {[p['idx']+1 for p in orbit_000]}")
    print(f"  Count: {len(orbit_000)} (should be 4 since 8 hexagrams / 2 per pair)")
    
    for p in orbit_000:
        print(f"    Pair {p['idx']+1}: {p['name_a']}-{p['name_b']}  "
              f"pal={p['is_palindrome']}  "
              f"mask={''.join(map(str, p['mask']))}")
    
    # The non-coset result for orbit (0,0,0): the 4 first-positions span 
    # all 6 non-zero XOR differences. This means the 4 positions are in 
    # "general position" — no 2-dim subgroup structure.
    
    # But for complement pairs, the mask = (1,1,1,1,1,1), which in position 
    # space maps to (1,1,1). So pos_a ⊕ pos_b = (1,1,1) for complement pairs.
    # For inversion pairs in orbit (0,0,0)... wait, can inversion pairs be in 
    # orbit (0,0,0)? sig=(0,0,0) means L1=L6, L2=L5, L3=L4 (palindrome).
    # For a palindrome, reverse(a) = a, so if the pair is by inversion, b = a.
    # That can't be (pairs have distinct hexagrams). So ALL pairs in orbit (0,0,0)
    # must be complement pairs!
    
    all_comp = all(p['is_palindrome'] for p in orbit_000)
    print(f"\n  All pairs in orbit (0,0,0) are complement: {all_comp}")


# ─── 3. Monte Carlo: coset probability ─────────────────────────────────────

def coset_monte_carlo():
    """
    Under random orientation, how often do the 4 first-positions form 
    a coset in each orbit?
    """
    print("\n" + "=" * 80)
    print("3. MONTE CARLO: COSET PROBABILITY")
    print("=" * 80)
    
    # For each orbit, we have 4 pairs. Each pair has two hexagrams.
    # Random orientation: for each pair, independently choose which is first.
    # Check if the 4 first-positions form a coset.
    
    orbit_pairs = defaultdict(list)
    for p in pairs:
        orbit_pairs[p['sig']].append(p)
    
    # For each orbit, count how often random orientation gives a coset
    for sig in sorted(orbit_pairs.keys()):
        items = orbit_pairs[sig]
        n_coset = 0
        
        for _ in range(N_TRIALS):
            positions = []
            for p in items:
                if RNG.integers(2) == 0:
                    positions.append(tuple(p['pos_a']))
                else:
                    positions.append(tuple(p['pos_b']))
            
            is_c, _ = check_coset(positions)
            if is_c:
                n_coset += 1
        
        actual_is_coset, actual_sub = check_coset([tuple(p['pos_a']) for p in items])
        
        sig_str = ''.join(map(str, sig))
        print(f"  Orbit ({sig_str}): actual={'coset' if actual_is_coset else 'no'}  "
              f"p(coset under random)={n_coset/N_TRIALS:.4f}")
    
    # Overall: how often do ALL non-complement orbits produce cosets?
    # (Exclude orbits 000 since all pairs there are complement)
    print(f"\n  Overall: how often do random orientations give cosets in all 7 non-(000) orbits?")
    
    non_000_orbits = {sig: items for sig, items in orbit_pairs.items() if sig != (0,0,0)}
    
    n_all_coset = 0
    n_at_least_6 = 0
    coset_count_dist = Counter()
    
    for _ in range(N_TRIALS):
        c = 0
        for sig, items in non_000_orbits.items():
            positions = []
            for p in items:
                if RNG.integers(2) == 0:
                    positions.append(tuple(p['pos_a']))
                else:
                    positions.append(tuple(p['pos_b']))
            is_c, _ = check_coset(positions)
            if is_c:
                c += 1
        coset_count_dist[c] += 1
        if c == 7:
            n_all_coset += 1
        if c >= 6:
            n_at_least_6 += 1
    
    # KW actual: how many of the 7 non-(000) orbits are cosets?
    actual_cosets_non000 = 0
    for sig, items in non_000_orbits.items():
        positions = [tuple(p['pos_a']) for p in items]
        is_c, _ = check_coset(positions)
        if is_c:
            actual_cosets_non000 += 1
    
    print(f"  KW actual: {actual_cosets_non000}/7 non-(000) orbits are cosets")
    print(f"  p(all 7 coset) = {n_all_coset/N_TRIALS:.6f}")
    print(f"  p(≥6 cosets) = {n_at_least_6/N_TRIALS:.6f}")
    print(f"  Coset count distribution:")
    for k in sorted(coset_count_dist.keys()):
        print(f"    {k}/7: {coset_count_dist[k]/N_TRIALS:.4f}")


# ─── 4. Which subgroups appear? ────────────────────────────────────────────

def subgroup_pattern():
    """
    For the orbits with coset structure, which 2-dim subgroup appears?
    Is there a pattern linking the orbit signature to the subgroup?
    """
    print("\n" + "=" * 80)
    print("4. SUBGROUP PATTERN")
    print("=" * 80)
    
    GEN_NAMES_3 = {
        (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
        (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
    }
    
    orbit_data = defaultdict(list)
    for p in pairs:
        orbit_data[p['sig']].append(p)
    
    print(f"  {'Orbit':>7s}  {'Coset?':>6s}  {'Subgroup generators':>20s}  "
          f"{'Subgroup':>15s}  Notes")
    
    subgroups_found = []
    
    for sig in sorted(orbit_data.keys()):
        items = orbit_data[sig]
        positions = [tuple(p['pos_a']) for p in items]
        is_coset, subgroup = check_coset(positions)
        
        sig_str = ''.join(map(str, sig))
        
        if is_coset:
            # Find generators (2 of the 3 non-identity elements)
            sg = sorted(subgroup)
            gens = [GEN_NAMES_3.get(s, str(s)) for s in sg]
            
            # The subgroup is generated by any 2 of its 3 non-identity elements
            gen_pair = gens[:2]
            
            # Note: the orbit signature is one of the Z₂³ elements.
            # Is the subgroup related to sig?
            sig_in_subgroup = sig in [s for s in sg]
            
            subgroups_found.append((sig, sg))
            
            print(f"  {sig_str:>7s}  {'YES':>6s}  {gen_pair[0]:>3s},{gen_pair[1]:>3s}"
                  f"{'':>14s}  {{{','.join(gens)}}}  "
                  f"{'sig ∈ H' if sig_in_subgroup else 'sig ∉ H'}")
        else:
            print(f"  {sig_str:>7s}  {'no':>6s}")
    
    # Pattern analysis: is there a relationship between orbit sig and subgroup?
    print(f"\n  Relationship between orbit signature and subgroup:")
    for sig, sg in subgroups_found:
        sig_name = GEN_NAMES_3.get(sig, 'id')
        sg_names = [GEN_NAMES_3.get(s, '?') for s in sg]
        
        # Check: is sig orthogonal to the subgroup? 
        # (dot product sig · h = 0 for all h in H?)
        orthogonal = all(sum(a*b for a,b in zip(sig, h)) % 2 == 0 for h in sg)
        
        # Check: is sig the "missing" direction?
        # Z₂³ has 7 two-dim subgroups. Each has a unique "orthogonal complement" 
        # which is a 1-dim subgroup.
        # Orthogonal complement of H = {v : v·h = 0 for all h ∈ H}
        
        print(f"    Orbit {sig_name:>3s} ({sig}): subgroup {{{','.join(sg_names)}}}  "
              f"sig⊥H: {orthogonal}")


# ─── 5. Orbit (1,1,1) special analysis ─────────────────────────────────────

def orbit_111_analysis():
    """
    Orbit (1,1,1) also failed the coset test. But it has no complement pairs.
    What's happening there?
    """
    print("\n" + "=" * 80)
    print("5. ORBIT (1,1,1) ANALYSIS")
    print("=" * 80)
    
    orbit_111 = [p for p in pairs if p['sig'] == (1,1,1)]
    
    print(f"  Pairs in orbit (1,1,1): {[p['idx']+1 for p in orbit_111]}")
    for p in orbit_111:
        pa = ''.join(map(str, p['pos_a']))
        pb = ''.join(map(str, p['pos_b']))
        mask_3 = ''.join(str(p['pos_a'][i] ^ p['pos_b'][i]) for i in range(3))
        print(f"    Pair {p['idx']+1}: pos_a={pa}  pos_b={pb}  diff={mask_3}  "
              f"mask_6={''.join(map(str, p['mask']))}  "
              f"{p['name_a']}-{p['name_b']}")
    
    positions = [tuple(p['pos_a']) for p in orbit_111]
    print(f"\n  First positions: {positions}")
    
    xors = set()
    for i in range(4):
        for j in range(i+1, 4):
            x = xor3(positions[i], positions[j])
            xors.add(x)
    print(f"  Pairwise XORs: {sorted(xors)} ({len(xors)} distinct)")
    
    # Check: does flipping ONE pair's orientation create a coset?
    print(f"\n  Testing single flips:")
    for flip_idx in range(4):
        test_pos = list(positions)
        p = orbit_111[flip_idx]
        test_pos[flip_idx] = tuple(p['pos_b'])
        is_c, sg = check_coset(test_pos)
        print(f"    Flip pair {p['idx']+1}: positions = {test_pos}  "
              f"coset = {is_c}" + (f"  subgroup = {sg}" if is_c else ""))


# ─── 6. Orbit (1,1,0) deep look ────────────────────────────────────────────

def orbit_110_analysis():
    """Check orbit (1,1,0) which has the OM signature - it IS a coset."""
    print("\n" + "=" * 80) 
    print("6. ORBIT (1,1,0) COSET DETAILS")
    print("=" * 80)
    
    orbit_110 = [p for p in pairs if p['sig'] == (1,1,0)]
    
    positions_a = [tuple(p['pos_a']) for p in orbit_110]
    positions_b = [tuple(p['pos_b']) for p in orbit_110]
    
    print(f"  Pairs: {[p['idx']+1 for p in orbit_110]}")
    print(f"  First positions: {positions_a}")
    print(f"  Second positions: {positions_b}")
    
    is_c_a, sg_a = check_coset(positions_a)
    is_c_b, sg_b = check_coset(positions_b)
    
    print(f"  A coset: {is_c_a}, subgroup: {sg_a}")
    print(f"  B coset: {is_c_b}, subgroup: {sg_b}")
    
    # If A is a coset of H, then B should be the other coset of the SAME subgroup
    # (since for each pair, pos_b = pos_a ⊕ sig)
    if is_c_a and is_c_b:
        print(f"  Same subgroup: {sg_a == sg_b}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    coset_analysis()
    complement_pair_deep()
    coset_monte_carlo()
    subgroup_pattern()
    orbit_111_analysis()
    orbit_110_analysis()


if __name__ == "__main__":
    main()
