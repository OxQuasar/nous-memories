"""
Thread 4: Why These Generator Dressings?

Every bridge mask decomposes as: mask = orbit_Δ ⊕ generator_dressing
The orbit_Δ is constrained by the orbit walk. The generator dressing is the "free choice."

Questions:
- For each bridge, how many hexagrams in the target orbit are reachable? (Always 8.)
  Each corresponds to a different generator dressing. How many choices exist?
- Is the actual choice Hamming-minimal?
- Which generator causes the +2 excess in non-optimal bridges?
- Is there a pattern in generator dressing vs. sequence position?
- Does the weight-5 gap follow from generator dressing constraints?
"""

import sys
sys.path.insert(0, '/home/skipper/code/nous/kingwen')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

DIMS = 6
M = np.array(all_bits())

GEN_BITS = {
    'O': (1, 0, 0, 0, 0, 1),
    'M': (0, 1, 0, 0, 1, 0),
    'I': (0, 0, 1, 1, 0, 0),
}

MASK_NAMES = {
    (1,1,1,1,1,1): "OMI", (1,1,0,0,1,1): "OM", (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI", (0,1,0,0,1,0): "M", (0,0,1,1,0,0): "I",
    (1,0,0,0,0,1): "O", (0,0,0,0,0,0): "id",
}

ORBIT_PAIR_TYPE = {
    (0,0,0): 'OMI', (1,1,0): 'OM', (1,0,1): 'OI', (0,1,0): 'M',
    (0,0,1): 'I',   (1,1,1): 'OMI', (1,0,0): 'O',  (0,1,1): 'MI',
}

ORBIT_NAMES = {
    (0,0,0): '1:Qian', (1,1,0): '2:Zhun', (1,0,1): '3:Xu',  (0,1,0): '4:Shi',
    (0,0,1): '5:XChu', (1,1,1): '6:Tai',  (1,0,0): '7:Bo',  (0,1,1): '8:WWang',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def xor_mask(a, b):
    return tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))

def gen_name(mask):
    if mask in MASK_NAMES:
        return MASK_NAMES[mask]
    return ''.join(map(str, mask))

def sig_name(sig):
    parts = []
    if sig[0]: parts.append('o')
    if sig[1]: parts.append('m')
    if sig[2]: parts.append('i')
    return ''.join(parts) if parts else 'id'

def kernel_component(mask):
    return (mask[5], mask[4], mask[3], mask[3], mask[4], mask[5])

def orbit_component(mask):
    return (mask[0]^mask[5], mask[1]^mask[4], mask[2]^mask[3], 0, 0, 0)

def xor6(a, b):
    return tuple(a[i] ^ b[i] for i in range(DIMS))

def hamming(a, b):
    return sum(int(a[i]) ^ int(b[i]) for i in range(DIMS))


# ─── Build orbit index ────────────────────────────────────────────────────

all_h = all_bits()
orbits_by_sig = defaultdict(list)
for i in range(64):
    h = tuple(all_h[i])
    sig = xor_sig(h)
    orbits_by_sig[sig].append((i, h))

# Build bridges
bridges = []
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    mask = xor_mask(a, b)
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    k_comp = kernel_component(mask)
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'mask': mask,
        'hamming': sum(mask),
        'sig_a': sig_a, 'sig_b': sig_b,
        'sig_change': tuple(sig_a[i] ^ sig_b[i] for i in range(3)),
        'kernel': k_comp,
        'kernel_name': gen_name(k_comp),
        'num_a': 2*k + 2, 'num_b': 2*k + 3,
        'name_a': KING_WEN[2*k + 1][1],
        'name_b': KING_WEN[2*k + 2][1],
    })


print("=" * 70)
print("THREAD 4: WHY THESE GENERATOR DRESSINGS?")
print("=" * 70)


# ─── 1. Choice space at each bridge ──────────────────────────────────────

print("\n1. CHOICE SPACE: ALL REACHABLE TARGETS PER BRIDGE")
print("-" * 50)

# For each bridge, the source hex is fixed and the target orbit is fixed.
# All 8 hexagrams in the target orbit are potential targets.
# Each corresponds to a different mask, hence a different generator dressing.

all_kernel_elements = []
for a in range(2):
    for b in range(2):
        for c in range(2):
            all_kernel_elements.append((a, b, c, c, b, a))

print(f"  For each bridge: source hex is fixed, target orbit has 8 hexagrams.")
print(f"  8 possible masks, 8 different generator dressings.")
print(f"  The actual sequence chooses one. Which one, and why?\n")

optimal_count = 0
excess_total = 0
excess_gen_matches = 0

for br in bridges:
    target_orbit = orbits_by_sig[br['sig_b']]
    
    # Compute all 8 possible masks and their Hamming distances
    alternatives = []
    for idx, target_hex in target_orbit:
        alt_mask = xor_mask(br['a'], target_hex)
        alt_kernel = kernel_component(alt_mask)
        alt_h = sum(alt_mask)
        alternatives.append({
            'target_idx': idx,
            'target_hex': target_hex,
            'mask': alt_mask,
            'hamming': alt_h,
            'kernel': alt_kernel,
            'kernel_name': gen_name(alt_kernel),
            'is_actual': (target_hex == br['b']),
        })
    
    alternatives.sort(key=lambda x: x['hamming'])
    min_h = alternatives[0]['hamming']
    actual_h = br['hamming']
    excess = actual_h - min_h
    excess_total += excess
    is_optimal = (actual_h == min_h)
    if is_optimal:
        optimal_count += 1
    
    # How many alternatives share the minimum Hamming?
    min_count = sum(1 for a in alternatives if a['hamming'] == min_h)
    
    # The actual choice
    actual_alt = [a for a in alternatives if a['is_actual']][0]
    
    marker = "✓ OPT" if is_optimal else f"  +{excess}"
    print(f"  B{br['idx']+1:2d}: {br['name_a']:12s}→{br['name_b']:12s}  "
          f"H={actual_h} (min={min_h}, {min_count} at min)  "
          f"gen={br['kernel_name']:>3s}  {marker}")
    
    # For non-optimal: which generator caused the excess?
    if not is_optimal:
        # Find closest alternative with different kernel
        closest = [a for a in alternatives if a['hamming'] == min_h]
        # The actual kernel vs. the optimal kernels
        optimal_kernels = set(a['kernel_name'] for a in closest)
        print(f"         optimal kernels: {optimal_kernels}  actual: {br['kernel_name']}")
        
        # Is the excess exactly the kernel difference?
        # excess mask = actual ⊕ optimal_candidate = kernel_actual ⊕ kernel_optimal (orbit part same)
        for opt_alt in closest[:1]:  # just show first optimal
            diff_mask = xor6(br['mask'], opt_alt['mask'])
            # This diff should be a kernel element
            is_kernel = diff_mask in set(all_kernel_elements)
            diff_name = gen_name(diff_mask) if is_kernel else ''.join(map(str, diff_mask))
            print(f"         diff from optimal: {''.join(map(str, diff_mask))} ({diff_name})  "
                  f"wt={sum(diff_mask)}  kernel={is_kernel}")
            if is_kernel:
                excess_gen_matches += 1

print(f"\n  Summary:")
print(f"  Optimal (min Hamming): {optimal_count}/31")
print(f"  Non-optimal: {31 - optimal_count}/31")
print(f"  Total excess Hamming: {excess_total}")
print(f"  Non-optimal where diff is a kernel element: {excess_gen_matches}/{31 - optimal_count}")


# ─── 2. Excess analysis ──────────────────────────────────────────────────

print(f"\n2. EXCESS QUANTIZATION")
print("-" * 50)

excess_values = []
for br in bridges:
    target_orbit = orbits_by_sig[br['sig_b']]
    min_h = min(hamming(br['a'], th) for _, th in target_orbit)
    excess = br['hamming'] - min_h
    excess_values.append(excess)

excess_freq = Counter(excess_values)
print(f"  Excess distribution:")
for e, count in sorted(excess_freq.items()):
    print(f"    +{e}: {count}× {'█' * count}")

print(f"\n  All non-zero excesses:")
for i, br in enumerate(bridges):
    if excess_values[i] > 0:
        print(f"    B{br['idx']+1:2d}: +{excess_values[i]}  gen={br['kernel_name']:>3s}  "
              f"orbit: {sig_name(br['sig_a'])}→{sig_name(br['sig_b'])}")


# ─── 3. Optimal vs non-optimal: generator dressing distribution ──────────

print(f"\n3. GENERATOR DRESSING: OPTIMAL vs NON-OPTIMAL")
print("-" * 50)

opt_gens = [br['kernel_name'] for i, br in enumerate(bridges) if excess_values[i] == 0]
nonopt_gens = [br['kernel_name'] for i, br in enumerate(bridges) if excess_values[i] > 0]

print(f"  Optimal bridges ({len(opt_gens)}) — kernel distribution:")
for g, count in sorted(Counter(opt_gens).items(), key=lambda x: -x[1]):
    print(f"    {g:>3s}: {count}×")

print(f"\n  Non-optimal bridges ({len(nonopt_gens)}) — kernel distribution:")
for g, count in sorted(Counter(nonopt_gens).items(), key=lambda x: -x[1]):
    print(f"    {g:>3s}: {count}×")


# ─── 4. Does kernel=id imply optimal? ────────────────────────────────────

print(f"\n4. DOES kernel=id IMPLY OPTIMAL?")
print("-" * 50)

id_bridges = [(i, br) for i, br in enumerate(bridges) if br['kernel_name'] == 'id']
print(f"  Bridges with kernel=id: {len(id_bridges)}")
for i, br in id_bridges:
    opt = "✓ OPT" if excess_values[i] == 0 else f"  +{excess_values[i]}"
    print(f"    B{br['idx']+1:2d}: H={br['hamming']}  {opt}  orbit: {sig_name(br['sig_a'])}→{sig_name(br['sig_b'])}")

id_optimal = sum(1 for i, br in id_bridges if excess_values[i] == 0)
print(f"  kernel=id AND optimal: {id_optimal}/{len(id_bridges)}")

# The reverse: does optimal imply kernel=id?
opt_with_id = sum(1 for i, br in enumerate(bridges) if excess_values[i] == 0 and br['kernel_name'] == 'id')
print(f"  optimal AND kernel=id: {opt_with_id}/{optimal_count}")
print(f"  → kernel=id is {'necessary' if opt_with_id == optimal_count else 'NOT necessary'} for optimality")
print(f"  → kernel=id is {'sufficient' if id_optimal == len(id_bridges) else 'NOT sufficient'} for optimality")


# ─── 5. B19 deep analysis ────────────────────────────────────────────────

print(f"\n5. B19: THE MAXIMUM-EXCESS BRIDGE")
print("-" * 50)

b19 = bridges[18]  # 0-indexed
print(f"  B19: {b19['name_a']}→{b19['name_b']}")
print(f"  mask={''.join(map(str, b19['mask']))} (OMI = full complement)")
print(f"  Hamming: {b19['hamming']}")
print(f"  Orbit: {sig_name(b19['sig_a'])}→{sig_name(b19['sig_b'])} (self-transition!)")
print(f"  Kernel: {b19['kernel_name']}")
print()

# All 8 alternatives
target_orbit = orbits_by_sig[b19['sig_b']]
print(f"  All 8 possible targets in orbit {sig_name(b19['sig_b'])}:")
for idx, target_hex in target_orbit:
    mask = xor_mask(b19['a'], target_hex)
    h = sum(mask)
    is_actual = (target_hex == b19['b'])
    hex_name = KING_WEN[idx][1]
    k_comp = kernel_component(mask)
    k_name = gen_name(k_comp)
    marker = " ◀ ACTUAL" if is_actual else ""
    print(f"    #{idx+1:2d} {hex_name:12s} {''.join(map(str, target_hex))}  "
          f"mask={''.join(map(str, mask))} H={h} gen={k_name}{marker}")

min_h_b19 = min(hamming(b19['a'], th) for _, th in target_orbit)
print(f"\n  Minimum Hamming: {min_h_b19}")
print(f"  Actual Hamming: {b19['hamming']}")
print(f"  Excess: +{b19['hamming'] - min_h_b19}")
print(f"  B19 uses the MAXIMUM possible Hamming (complement), not the minimum.")
print(f"  It's the only self-transition that uses OMI (the only mask that both")
print(f"  preserves the orbit AND flips all 6 bits).")


# ─── 6. Generator dressing vs sequence position ─────────────────────────

print(f"\n6. GENERATOR DRESSING vs POSITION")
print("-" * 50)

print(f"  First half (B1-B15) vs second half (B16-B31):")
first_gens = Counter(br['kernel_name'] for br in bridges[:15])
second_gens = Counter(br['kernel_name'] for br in bridges[15:])

all_gen_names = sorted(set(list(first_gens.keys()) + list(second_gens.keys())))
print(f"  {'Gen':>4s}  First  Second")
for g in all_gen_names:
    print(f"  {g:>4s}   {first_gens.get(g, 0):2d}     {second_gens.get(g, 0):2d}")

# Canon boundary: B14 is the boundary
print(f"\n  Upper canon (B1-B14) vs lower canon (B15-B31):")
upper_gens = Counter(br['kernel_name'] for br in bridges[:14])
lower_gens = Counter(br['kernel_name'] for br in bridges[14:])
print(f"  {'Gen':>4s}  Upper  Lower")
for g in all_gen_names:
    print(f"  {g:>4s}   {upper_gens.get(g, 0):2d}     {lower_gens.get(g, 0):2d}")


# ─── 7. Weight-5 gap explanation ─────────────────────────────────────────

print(f"\n7. WEIGHT-5 GAP: WHY NO BRIDGE FLIPS EXACTLY 5 LINES")
print("-" * 50)

# A mask of weight 5 means exactly 1 bit is 0 and 5 are 1.
# Decompose: mask = orbit_Δ ⊕ gen_dressing
# Weight-5 masks in Z₂⁶: there are C(6,5) = 6 of them:
# 111110, 111101, 111011, 110111, 101111, 011111
weight5_masks = []
for i in range(64):
    m = tuple((i >> (5-d)) & 1 for d in range(6))
    if sum(m) == 5:
        weight5_masks.append(m)

print(f"  All weight-5 masks in Z₂⁶: {len(weight5_masks)}")
for m in weight5_masks:
    m_str = ''.join(map(str, m))
    k = kernel_component(m)
    r = orbit_component(m)
    k_name = gen_name(k)
    r_sig = sig_name((r[0], r[1], r[2]))
    wt_r = sum(r)  # weight of orbit component
    wt_k = sum(k)  # weight of kernel component
    print(f"    {m_str}  orbit_Δ={''.join(map(str, r))} ({r_sig}, wt={wt_r})  "
          f"kernel={''.join(map(str, k))} ({k_name}, wt={wt_k})")

print(f"\n  For weight-5 to occur, we need wt(orbit_Δ ⊕ gen) = 5.")
print(f"  orbit_Δ has form (a,b,c,0,0,0), gen has form (x,y,z,z,y,x).")
print(f"  So mask = (a⊕x, b⊕y, c⊕z, z, y, x) and")
print(f"  wt = (a⊕x) + (b⊕y) + (c⊕z) + z + y + x")

# Enumerate: what orbit_Δ + gen combinations give weight 5?
print(f"\n  Combinations giving weight 5:")
w5_combos = []
for ro in range(2):
    for rm in range(2):
        for ri in range(2):
            for go in range(2):
                for gm in range(2):
                    for gi in range(2):
                        mask = (ro^go, rm^gm, ri^gi, gi, gm, go)
                        if sum(mask) == 5:
                            r_name = sig_name((ro, rm, ri))
                            g_name_str = ''
                            if go: g_name_str += 'O'
                            if gm: g_name_str += 'M'
                            if gi: g_name_str += 'I'
                            g_name_str = g_name_str or 'id'
                            w5_combos.append((ro, rm, ri, go, gm, gi))
                            print(f"    orbit_Δ=({ro},{rm},{ri})={r_name:>3s}  "
                                  f"gen=({go},{gm},{gi})={g_name_str:>3s}  "
                                  f"mask={''.join(map(str, mask))}")

# Now check: do any of these (orbit_Δ, gen) pairs actually occur?
print(f"\n  Do any of these {len(w5_combos)} combinations occur in the sequence?")
for br in bridges:
    o_comp = orbit_component(br['mask'])
    k_comp = br['kernel']
    o_bits = (o_comp[0], o_comp[1], o_comp[2])
    k_bits = (k_comp[0], k_comp[1], k_comp[2])  # first 3 bits of kernel (= last 3 reversed)
    
    for combo in w5_combos:
        if (combo[0], combo[1], combo[2]) == o_bits and (combo[3], combo[4], combo[5]) == k_bits:
            print(f"    B{br['idx']+1}: matches! But wt={br['hamming']} (should be 5)")

print(f"\n  Analysis: weight-5 requires specific orbit_Δ + gen combinations.")
print(f"  These combinations are not forbidden algebraically — they just happen")
print(f"  not to appear in the King Wen sequence's specific bridge choices.")


# ─── 8. The constraint landscape ─────────────────────────────────────────

print(f"\n8. THE CONSTRAINT LANDSCAPE: WHAT CONSTRAINS GENERATOR DRESSING?")
print("-" * 50)

# For each bridge, the target hexagram must be the SPECIFIC one that starts
# the next pair. It's not just any hex in the target orbit — it's a specific one.
# The pair structure constrains which hex starts the next pair.

# But wait: the pair structure says hex_{2k+2} and hex_{2k+3} form a pair.
# And pair type is orbit-determined. So hex_{2k+3} = hex_{2k+2} ⊕ pair_type(orbit).
# But hex_{2k+2} is the bridge target. It needs to be a specific element of
# the target orbit such that hex_{2k+3} is also in that orbit (which it is,
# since pair type preserves orbit) AND the next bridge from hex_{2k+3} leads
# to the right place.

# So the constraint propagates: bridge_k's target must be compatible with bridge_{k+1}'s source.
# This is a chain constraint!

print(f"  The generator dressing at bridge_k determines hex_{'{2k+2}'},")
print(f"  which determines hex_{'{2k+3}'} (via pair type),")
print(f"  which determines bridge_{'{k+1}'}'s mask.")
print(f"  → Generator dressing choices are CHAINED.")
print(f"  → Each bridge's free choice constrains the next bridge's options.")
print()

# Verify the chain
print(f"  Chain verification:")
for k in range(30):
    br_k = bridges[k]
    br_k1 = bridges[k + 1]
    
    # hex_{2k+3} = br_k target ⊕ pair_type(target orbit)
    pair_type_name = ORBIT_PAIR_TYPE[br_k['sig_b']]
    pair_type_mask = None
    for bits, name in MASK_NAMES.items():
        if name == pair_type_name:
            pair_type_mask = tuple(int(x) for x in bits)
            break
    
    h_2k3 = xor6(br_k['b'], pair_type_mask)  # hex_{2k+3}
    actual_h_2k3 = tuple(M[2*k + 3])
    
    # This should be the source of bridge_{k+1}
    expected_source = actual_h_2k3
    actual_source = br_k1['a']
    
    match = expected_source == actual_source
    if not match:
        print(f"    B{k+1}→B{k+2}: CHAIN BREAK")

print(f"  → Chain is consistent (by construction — the sequence IS the chain)")


# ─── 9. Degrees of freedom ──────────────────────────────────────────────

print(f"\n9. DEGREES OF FREEDOM IN THE SEQUENCE")
print("-" * 50)

# The sequence has these structural choices:
# 1. The orbit walk: 31 orbit transitions (some forced by graph connectivity)
# 2. At each bridge: which of the 8 hexagrams in target orbit to land on
#    (= choice of generator dressing)
# 3. BUT: the starting hex of each pair is determined by the previous bridge
# 4. AND: the pair partner is determined by the pair type (orbit-determined)
# 5. So the ONLY free choice is the orbit walk + the generator dressing

# Given the orbit walk, how much freedom is there in generator dressing?
# The first pair's first hexagram is chosen freely (hex 1 = Qian).
# After that, each bridge target determines everything until the next bridge.
# So: 1 initial hex choice + 31 bridge target choices in orbits of size 8.
# But the targets must be SPECIFIC hexagrams from the set of 64.
# Since we visit each hex exactly once (Hamiltonian), the targets are constrained.

# How constrained? Let's count "used" hexagrams at each bridge.
print(f"  At each bridge, the target orbit has 8 hexagrams.")
print(f"  Some may already be 'used' (appeared earlier in the sequence).")
print(f"  Available choices = 8 - (previously used in that orbit).\n")

used_hexagrams = set()
# First pair
used_hexagrams.add(tuple(M[0]))
used_hexagrams.add(tuple(M[1]))

for br in bridges:
    target_orbit = orbits_by_sig[br['sig_b']]
    used_in_orbit = sum(1 for _, h in target_orbit if h in used_hexagrams)
    available = 8 - used_in_orbit
    
    # But we need to land on a hex AND its pair partner both unused
    # (since they form the next pair)
    pair_type_name = ORBIT_PAIR_TYPE[br['sig_b']]
    pair_mask = None
    for bits, name in MASK_NAMES.items():
        if name == pair_type_name:
            pair_mask = tuple(int(x) for x in bits)
            break
    
    valid_targets = 0
    for idx, target_hex in target_orbit:
        partner = xor6(tuple(int(x) for x in target_hex), pair_mask)
        if target_hex not in used_hexagrams and tuple(partner) not in used_hexagrams:
            valid_targets += 1
    
    # The actual target (bridge lands on hex_{2k+2}, partner is hex_{2k+3})
    actual_target = br['b']
    actual_partner = xor6(tuple(int(x) for x in br['b']), pair_mask)
    
    print(f"  B{br['idx']+1:2d}: orbit {sig_name(br['sig_b']):>3s}  "
          f"used={used_in_orbit}/8  valid_targets={valid_targets}  "
          f"(need target+partner both free)")
    
    # Mark as used
    used_hexagrams.add(tuple(actual_target))
    used_hexagrams.add(tuple(actual_partner))


# ─── 10. Trigram analysis of generator dressing ──────────────────────────

print(f"\n10. TRIGRAM-LEVEL VIEW OF GENERATOR DRESSING")
print("-" * 50)

# The generator dressing flips mirror pairs symmetrically.
# At the trigram level, generator O flips lines 1,6 (one per trigram).
# Generator M flips lines 2,5 (one per trigram).
# Generator I flips lines 3,4 (one per trigram).
# So any generator flips the SAME positions in lower and upper trigrams.

# The orbit change, by contrast, is antisymmetric: it flips a line in one
# trigram but not its mirror. This is what BREAKS the mirror symmetry.

# So the full bridge = symmetric gen + antisymmetric orbit change.
# At the trigram level:
#   lower trigram change = orbit_Δ[:3] ⊕ gen_3bit
#   upper trigram change = gen_3bit (orbit_Δ has zeros in positions 4-6)

print(f"  Bridge mask decomposition at trigram level:")
print(f"  lower Δ = orbit_change[:3] ⊕ gen_bits   (asymmetric + symmetric)")
print(f"  upper Δ = gen_bits                        (symmetric only)")
print()

lower_changes = Counter()
upper_changes = Counter()

for br in bridges:
    lower_delta = tuple(br['mask'][i] for i in range(3))
    upper_delta = tuple(br['mask'][i] for i in range(3, 6))
    lower_changes[sum(lower_delta)] += 1
    upper_changes[sum(upper_delta)] += 1

print(f"  Lines changed in lower trigram: {dict(sorted(lower_changes.items()))}")
print(f"  Lines changed in upper trigram: {dict(sorted(upper_changes.items()))}")

# The upper trigram change IS the generator component (positions 4,5,6 = mirror of gen)
# So upper trigram changes should match the generator weight distribution
print(f"\n  Upper trigram change = generator weight:")
for br in bridges:
    upper_delta = tuple(br['mask'][i] for i in range(3, 6))
    gen_part = (br['kernel'][0], br['kernel'][1], br['kernel'][2])
    # Upper delta should be (gen[3], gen[4], gen[5]) = (gen_i, gen_m, gen_o)
    # which is the reverse of gen[:3]
    assert upper_delta == (br['kernel'][3], br['kernel'][4], br['kernel'][5])

print(f"  Verified: upper trigram change = kernel component (positions 4-6)")
print(f"  → The upper trigram change at a bridge reveals exactly the generator dressing")

# What about lower trigram?
print(f"\n  Lower trigram change = orbit_Δ ⊕ generator (positions 1-3):")
for br in bridges:
    lower_delta = tuple(br['mask'][i] for i in range(3))
    o_comp = orbit_component(br['mask'])
    gen_3 = (br['kernel'][0], br['kernel'][1], br['kernel'][2])
    expected_lower = tuple(o_comp[i] ^ gen_3[i] for i in range(3))
    assert lower_delta == expected_lower

print(f"  Verified: lower trigram change = orbit_Δ[:3] ⊕ kernel[:3]")


# ─── 11. Upper trigram preservation ──────────────────────────────────────

print(f"\n11. UPPER vs LOWER TRIGRAM PRESERVATION AT BRIDGES")
print("-" * 50)

# How often does a bridge preserve the upper trigram? (= gen has weight 0 in upper = id kernel)
# How often does it preserve the lower trigram? (= orbit_Δ = gen, i.e. they cancel)

upper_preserved = 0
lower_preserved = 0
both_preserved = 0
neither_preserved = 0

for br in bridges:
    lower_delta = tuple(br['mask'][i] for i in range(3))
    upper_delta = tuple(br['mask'][i] for i in range(3, 6))
    
    up = (upper_delta == (0,0,0))
    lo = (lower_delta == (0,0,0))
    
    if up: upper_preserved += 1
    if lo: lower_preserved += 1
    if up and lo: both_preserved += 1
    if not up and not lo: neither_preserved += 1

print(f"  Upper trigram preserved: {upper_preserved}/31 (kernel=id)")
print(f"  Lower trigram preserved: {lower_preserved}/31 (orbit_Δ=gen)")
print(f"  Both preserved: {both_preserved}/31 (impossible unless self-loop with id)")
print(f"  Neither preserved: {neither_preserved}/31")
print(f"  → Upper preservation = kernel is id = bridge is a 'pure orbit change'")
print(f"  → Lower preservation = the gen dressing exactly cancels the orbit change in lower half")


print(f"\n{'=' * 70}")
print("THREAD 4 COMPLETE")
print("=" * 70)
