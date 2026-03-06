"""
Threads D + E: Position trajectory and weight/yang flow dynamics.

Thread D: In the factored basis (ō,m̄,ī,o,m,i), track the position trajectory
through the full 64-hexagram sequence. Compare to orbit trajectory.
- Is there a preferred starting position within each orbit?
- Do the 8 visits to each orbit cover all 8 positions?
- Position trajectory autocorrelation structure
- Relationship between position trajectory (hidden) and orbit trajectory (visible)

Thread E: Weight and yang flow.
- Weight trajectory dependence on orientation (verify: inversion pairs are weight-neutral)
- Complement pairs (OMI mask): weight jump direction determined by orientation
- Does KW place the heavier or lighter hexagram first in the 8 complement pairs?
  (Round 1 found 4 complement pairs, but actually there are also OMI-mask pairs 
   in orbit (1,1,1) — need to clarify)
- Weight monotonicity / structured flow within quartets and octets
- Connection to the yang drainage pattern (7/8 octets lose yang)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter2')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
from analysis_utils import VALID_MASKS, xor_sig, xor_tuple, hamming

DIMS = 6
N_PAIRS = 32
N_TRIALS = 100000
RNG = np.random.default_rng(42)

M = [tuple(h) for h in all_bits()]

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}


def reverse_bits(h):
    return tuple(h[5-i] for i in range(DIMS))

def complement(h):
    return tuple(1 - x for x in h)

def weight(h):
    return sum(h)

def is_palindrome(h):
    return h == reverse_bits(h)

def to_int(h):
    val = 0
    for bit in h:
        val = val * 2 + bit
    return val

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

# Factored basis: h = (l1,l2,l3,l4,l5,l6)
# orbit: (l1⊕l6, l2⊕l5, l3⊕l4)
# position: (l6, l5, l4) = (l1⊕ō, l2⊕m̄, l3⊕ī)  [using lower half: l1,l2,l3]
# Alternative: position = (l1, l2, l3)

# We use position = (L1, L2, L3) — the bottom-half lines
# This is consistent with iter2's factored basis where position = lower 3 bits

hex_data = []
for i in range(64):
    h = M[i]
    orbit = xor_sig(h)
    pos = h[:3]  # (L1, L2, L3)
    hex_data.append({
        'idx': i,
        'hex': h,
        'orbit': orbit,
        'pos': pos,
        'weight': weight(h),
        'kw_num': KING_WEN[i][0],
        'name': KING_WEN[i][1],
    })

pairs = []
for k in range(N_PAIRS):
    a = hex_data[2*k]
    b = hex_data[2*k+1]
    mask = xor_tuple(a['hex'], b['hex'])
    pairs.append({
        'idx': k,
        'a': a, 'b': b,
        'mask': mask,
        'mask_name': VALID_MASKS.get(mask, '?'),
        'orbit': a['orbit'],
        'is_pal': is_palindrome(a['hex']) and is_palindrome(b['hex']),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD D: POSITION TRAJECTORY
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("THREAD D: POSITION TRAJECTORY IN THE FACTORED BASIS")
print("=" * 80)

# ─── D1: The full position and orbit trajectory ────────────────────────────

orbit_traj = [hd['orbit'] for hd in hex_data]
pos_traj = [hd['pos'] for hd in hex_data]

print("\n  Full trajectory (64 steps):")
print(f"  {'Step':>4s}  {'Hex':>8s}  {'Orbit':>5s}  {'Pos':>3s}  {'Wt':>2s}  {'ΔPos':>5s}  {'Name':>12s}")
for i in range(64):
    hd = hex_data[i]
    orb_str = ''.join(map(str, hd['orbit']))
    pos_str = ''.join(map(str, hd['pos']))
    
    if i > 0:
        delta_pos = xor3(pos_traj[i], pos_traj[i-1])
        dp_str = ''.join(map(str, delta_pos))
    else:
        dp_str = ' --- '
    
    pair_label = 'P' if i % 2 == 0 else 'B' if i < 63 else 'P'
    step_type = '→' if i % 2 == 1 and i < 63 else '│' if i % 2 == 0 else '→'
    
    print(f"  {i+1:4d}  {''.join(map(str, hd['hex']))}  {orb_str}  {pos_str}  {hd['weight']:2d}  {dp_str}  {hd['name']:>12s}")


# ─── D2: Position trajectory — per-orbit visit analysis ────────────────────

print("\n" + "─" * 80)
print("D2: POSITION VISITS PER ORBIT")
print("─" * 80)

orbit_visits = defaultdict(list)
for i, hd in enumerate(hex_data):
    orbit_visits[hd['orbit']].append({
        'step': i,
        'pos': hd['pos'],
        'weight': hd['weight'],
        'pair': i // 2,
        'is_first': i % 2 == 0,
    })

for sig in sorted(orbit_visits.keys()):
    visits = orbit_visits[sig]
    positions = [v['pos'] for v in visits]
    unique_pos = set(tuple(p) for p in positions)
    
    sig_str = ''.join(map(str, sig))
    name = ORBIT_NAMES[sig]
    
    print(f"\n  Orbit ({sig_str}) = {name}: {len(visits)} visits, {len(unique_pos)} unique positions")
    
    for v in visits:
        pos_str = ''.join(map(str, v['pos']))
        print(f"    Step {v['step']+1:2d} (pair {v['pair']+1:2d}, {'1st' if v['is_first'] else '2nd'}): "
              f"pos={pos_str}  wt={v['weight']}")
    
    # Check if all 8 positions are covered
    all_8 = len(unique_pos) == 8
    print(f"    All 8 positions covered: {all_8}")
    
    if not all_8:
        all_positions = set(tuple(h[:3]) for h in M if xor_sig(h) == sig)
        missing = all_positions - unique_pos
        print(f"    Missing: {sorted(missing)}")


# ─── D3: First-visit position preference ───────────────────────────────────

print("\n" + "─" * 80)
print("D3: FIRST-VISIT POSITION (first time each orbit appears)")
print("─" * 80)

first_visit = {}
for i, hd in enumerate(hex_data):
    sig = hd['orbit']
    if sig not in first_visit:
        first_visit[sig] = {
            'step': i,
            'pos': hd['pos'],
            'pair': i // 2,
        }

for sig in sorted(first_visit.keys()):
    fv = first_visit[sig]
    sig_str = ''.join(map(str, sig))
    pos_str = ''.join(map(str, fv['pos']))
    print(f"  Orbit ({sig_str}) = {ORBIT_NAMES[sig]:>6s}: "
          f"first at step {fv['step']+1:2d} (pair {fv['pair']+1:2d}), pos={pos_str}")


# ─── D4: Position trajectory autocorrelation ───────────────────────────────

print("\n" + "─" * 80)
print("D4: POSITION TRAJECTORY AUTOCORRELATION")
print("─" * 80)

# Convert position to integer for correlation
pos_ints = [p[0]*4 + p[1]*2 + p[2] for p in pos_traj]
pos_arr = np.array(pos_ints, dtype=float)

# Autocorrelation on the integer representation
pos_centered = pos_arr - np.mean(pos_arr)
pos_var = np.var(pos_arr)

print("\n  Full position trajectory autocorrelation:")
for lag in [1, 2, 4, 8, 16, 32]:
    if lag < 64 and pos_var > 0:
        ac = np.mean(pos_centered[:64-lag] * pos_centered[lag:]) / pos_var
        print(f"    lag {lag:2d}: {ac:+.4f}")

# Per-component autocorrelation
print("\n  Per-component autocorrelation:")
for comp, name in enumerate(['o (L1)', 'm (L2)', 'i (L3)']):
    comp_arr = np.array([p[comp] for p in pos_traj], dtype=float)
    comp_c = comp_arr - np.mean(comp_arr)
    comp_v = np.var(comp_arr)
    if comp_v > 0:
        print(f"  {name}:")
        for lag in [1, 2, 4, 8]:
            ac = np.mean(comp_c[:64-lag] * comp_c[lag:]) / comp_v
            print(f"    lag {lag:2d}: {ac:+.4f}")

# Cross-correlation between position and orbit trajectories
print("\n  Cross-correlation between position and orbit:")
orb_ints = [o[0]*4 + o[1]*2 + o[2] for o in orbit_traj]
orb_arr = np.array(orb_ints, dtype=float)
orb_c = orb_arr - np.mean(orb_arr)
orb_v = np.var(orb_arr)

if pos_var > 0 and orb_v > 0:
    for lag in [0, 1, 2, -1, -2]:
        if lag >= 0:
            cc = np.mean(pos_centered[:64-lag] * orb_c[lag:]) / np.sqrt(pos_var * orb_v)
        else:
            cc = np.mean(orb_c[:64+lag] * pos_centered[-lag:]) / np.sqrt(pos_var * orb_v)
        print(f"    lag {lag:+2d}: {cc:+.4f}")

# Per-component cross-correlation (o_pos vs o_orbit, etc.)
print("\n  Component-wise cross-correlation (pos vs orbit, lag 0):")
for comp, name in enumerate(['o', 'm', 'i']):
    p_arr = np.array([p[comp] for p in pos_traj], dtype=float)
    o_arr = np.array([o[comp] for o in orbit_traj], dtype=float)
    p_c = p_arr - np.mean(p_arr)
    o_c = o_arr - np.mean(o_arr)
    pv = np.var(p_arr)
    ov = np.var(o_arr)
    if pv > 0 and ov > 0:
        cc = np.mean(p_c * o_c) / np.sqrt(pv * ov)
        print(f"    {name}_pos vs {name}_orbit: r = {cc:+.4f}")


# ─── D5: Position transition structure ──────────────────────────────────────

print("\n" + "─" * 80)
print("D5: POSITION TRANSITION ANALYSIS")
print("─" * 80)

# Within-pair transitions vs bridge transitions
within_pair_deltas = []
bridge_deltas = []

for i in range(63):
    delta = xor3(pos_traj[i+1], pos_traj[i])
    delta_name = KERNEL_NAMES.get(delta, '?')
    
    if i % 2 == 0:  # within pair (even→odd)
        within_pair_deltas.append(delta)
    else:  # bridge (odd→even)
        bridge_deltas.append(delta)

print(f"\n  Within-pair position changes (32 transitions):")
wp_counts = Counter(within_pair_deltas)
for k in sorted(wp_counts.keys()):
    print(f"    {KERNEL_NAMES[k]:>3s}: {wp_counts[k]}")

print(f"\n  Bridge position changes (31 transitions) = kernel dressings:")
br_counts = Counter(bridge_deltas)
for k in sorted(br_counts.keys()):
    print(f"    {KERNEL_NAMES[k]:>3s}: {br_counts[k]}")

# The within-pair changes should equal the orbit signature (mask = sig identity)
print(f"\n  Verification: within-pair delta = orbit signature?")
match_count = 0
for k in range(N_PAIRS):
    sig = pairs[k]['orbit']
    delta = within_pair_deltas[k]
    # For complement pairs (sig=000), the position change is (1,1,1) ≠ sig
    if delta == sig:
        match_count += 1

print(f"    Match: {match_count}/32")

# For the 4 complement pairs, show the mismatch
for k in range(N_PAIRS):
    sig = pairs[k]['orbit']
    delta = within_pair_deltas[k]
    if delta != sig:
        print(f"    Pair {k+1}: orbit={sig}, pos_delta={delta}  [{pairs[k]['a']['name']}-{pairs[k]['b']['name']}]")


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD E: WEIGHT AND YANG FLOW
# ═══════════════════════════════════════════════════════════════════════════════

print("\n\n" + "=" * 80)
print("THREAD E: WEIGHT AND YANG FLOW")
print("=" * 80)

# ─── E1: Weight trajectory ─────────────────────────────────────────────────

print("\n" + "─" * 80)
print("E1: WEIGHT TRAJECTORY (64 steps)")
print("─" * 80)

weights = [hd['weight'] for hd in hex_data]

print(f"\n  Weight sequence:")
for k in range(N_PAIRS):
    wa = weights[2*k]
    wb = weights[2*k+1]
    delta = wb - wa
    pair_name = f"{hex_data[2*k]['name']}-{hex_data[2*k+1]['name']}"
    print(f"  Pair {k+1:2d}: {wa} → {wb}  Δ={delta:+d}  {pair_name}")

# Within-pair weight changes
pair_deltas = [weights[2*k+1] - weights[2*k] for k in range(N_PAIRS)]
print(f"\n  Within-pair weight changes:")
print(f"    Distribution: {Counter(pair_deltas)}")
print(f"    Non-zero: {sum(1 for d in pair_deltas if d != 0)}/32")

# Identify which pairs have non-zero weight change
print(f"\n  Pairs with weight change (should be complement/palindromic pairs only):")
for k in range(N_PAIRS):
    d = pair_deltas[k]
    if d != 0:
        p = pairs[k]
        print(f"    Pair {k+1}: Δ={d:+d}  orbit={p['orbit']}  mask={p['mask_name']}  "
              f"pal={p['is_pal']}  {p['a']['name']}-{p['b']['name']}")


# ─── E2: Weight-orientation interaction for inversion pairs ────────────────

print("\n" + "─" * 80)
print("E2: WEIGHT-ORIENTATION INTERACTION")
print("─" * 80)

# For inversion pairs: reverse preserves weight, so within-pair weight change = 0
# For complement pairs: complement(h) has weight 6 - weight(h)
# Only OMI-mask pairs (complement) can have weight changes

# But wait: the mask = sig identity means:
# - Orbit (0,0,0): mask = OMI → complement pairs
# - Orbit (1,1,1): mask = OMI → complement pairs?? 
# No: mask = sig. Orbit (1,1,1) has sig = (1,1,1), so mask = OMI.
# But these hexagrams are NOT palindromes (sig=(1,1,1) means all line pairs differ).
# So b = a ⊕ (1,1,1,1,1,1) = complement(a), but a is NOT palindromic.
# Weight of complement = 6 - weight(a).

# Let's check ALL OMI-mask pairs
omi_pairs = [p for p in pairs if p['mask_name'] == 'OMI']
print(f"\n  OMI-mask pairs (mask = complement): {len(omi_pairs)}")
for p in omi_pairs:
    wa = p['a']['weight']
    wb = p['b']['weight']
    delta = wb - wa
    print(f"    Pair {p['idx']+1}: orbit={p['orbit']}  pal={p['is_pal']}  "
          f"wt_a={wa}  wt_b={wb}  Δ={delta:+d}  "
          f"{p['a']['name']}-{p['b']['name']}")

# How many OMI pairs place heavier first?
heavier_first = sum(1 for p in omi_pairs if p['a']['weight'] > p['b']['weight'])
lighter_first = sum(1 for p in omi_pairs if p['a']['weight'] < p['b']['weight'])
equal = sum(1 for p in omi_pairs if p['a']['weight'] == p['b']['weight'])

print(f"\n  OMI pairs: heavier first={heavier_first}, lighter first={lighter_first}, equal={equal}")

# For orbit (1,1,1): ALL hexagrams have weight 3, so complement also has weight 3.
# So weight change is 0 for orbit (1,1,1) OMI pairs!
# Weight changes happen ONLY in orbit (0,0,0), where palindromic hexagrams are
# paired by complement.

print(f"\n  Key insight: OMI pairs in orbit (1,1,1) have Δweight = 0")
print(f"  (because all hexagrams in orbit (1,1,1) have weight 3)")
print(f"  Weight changes occur ONLY in the 4 complement pairs (orbit (0,0,0))")


# ─── E3: Bridge weight changes ─────────────────────────────────────────────

print("\n" + "─" * 80)
print("E3: BRIDGE WEIGHT TRANSITIONS")
print("─" * 80)

bridge_weight_changes = []
for k in range(31):
    w_exit = weights[2*k + 1]  # exit hex of pair k
    w_entry = weights[2*k + 2]  # entry hex of pair k+1
    delta = w_entry - w_exit
    bridge_weight_changes.append(delta)

print(f"\n  Bridge weight change distribution: {Counter(bridge_weight_changes)}")
print(f"  Mean: {np.mean(bridge_weight_changes):.3f}")
print(f"  Positive (gaining yang): {sum(1 for d in bridge_weight_changes if d > 0)}")
print(f"  Zero: {sum(1 for d in bridge_weight_changes if d == 0)}")
print(f"  Negative (losing yang): {sum(1 for d in bridge_weight_changes if d < 0)}")

# Net yang flow per bridge
print(f"\n  Bridge-by-bridge weight transitions:")
for k in range(31):
    w_exit = weights[2*k + 1]
    w_entry = weights[2*k + 2]
    delta = w_entry - w_exit
    orb_from = orbit_traj[2*k + 1]
    orb_to = orbit_traj[2*k + 2]
    print(f"    B{k+1:2d}: {w_exit}→{w_entry} Δ={delta:+d}  "
          f"{ORBIT_NAMES[orb_from]}→{ORBIT_NAMES[orb_to]}")


# ─── E4: Yang drainage by octet ────────────────────────────────────────────

print("\n" + "─" * 80)
print("E4: YANG DRAINAGE BY OCTET")
print("─" * 80)

for oct_idx in range(8):
    start = oct_idx * 8
    end = start + 8
    oct_weights = weights[start:end]
    oct_start_w = oct_weights[0]
    oct_end_w = oct_weights[-1]
    net = oct_end_w - oct_start_w
    total_yang = sum(oct_weights)
    mean_yang = np.mean(oct_weights)
    
    print(f"\n  Octet {oct_idx+1} (hex {start+1}-{end}):")
    print(f"    Weights: {oct_weights}")
    print(f"    Start={oct_start_w}, End={oct_end_w}, Net={net:+d}")
    print(f"    Total yang={total_yang}, Mean={mean_yang:.2f}")
    
    # Within-octet monotonicity
    pair_starts = [weights[start + 2*j] for j in range(4)]
    pair_ends = [weights[start + 2*j + 1] for j in range(4)]
    print(f"    Pair starts: {pair_starts}")
    print(f"    Pair ends: {pair_ends}")


# ─── E5: Weight trajectory under orientation flip ──────────────────────────

print("\n" + "─" * 80)
print("E5: ORIENTATION DEPENDENCE OF WEIGHT TRAJECTORY")
print("─" * 80)

# For each pair, flipping orientation swaps (a, b) to (b, a)
# For inversion pairs: weight(a) = weight(b), so weight trajectory unchanged
# For OMI pairs in orbit (0,0,0): weight(a) + weight(b) = 6
# For OMI pairs in orbit (1,1,1): weight(a) = weight(b) = 3

# Total weight trajectory change under a single pair flip:
print(f"\n  Weight change from flipping each pair:")
for k in range(N_PAIRS):
    p = pairs[k]
    wa = p['a']['weight']
    wb = p['b']['weight']
    
    if wa != wb:
        # Flipping changes:
        # - pair's weight sequence goes from (wa, wb) to (wb, wa)
        # - bridge before pair k changes exit weight
        # - bridge after pair k changes entry weight
        delta_internal = wb - wa  # within pair, was wb-wa, becomes wa-wb
        print(f"  Pair {k+1}: wa={wa}, wb={wb}  flip changes internal Δ from {wb-wa:+d} to {wa-wb:+d}  "
              f"[{p['a']['name']}-{p['b']['name']}]")
    else:
        pass  # no effect on weight trajectory

# Count pairs that affect weight trajectory
weight_affecting = sum(1 for p in pairs if p['a']['weight'] != p['b']['weight'])
print(f"\n  Pairs that affect weight trajectory when flipped: {weight_affecting}/32")
print(f"  All are complement pairs in orbit (0,0,0)")

# Total yang count is invariant under orientation (permutation of {0,1}^6)
total_yang = sum(weights)
print(f"\n  Total yang across sequence: {total_yang}")
print(f"  Expected (32 per line × 6 lines / 2... actually sum of all 64 weights):")
print(f"  = sum of weights of all 64 hexagrams = {sum(weight(tuple(h)) for h in all_bits())}")
print(f"  This is invariant — every hexagram appears exactly once.")


# ─── E6: Complement pair weight pattern ────────────────────────────────────

print("\n" + "─" * 80)
print("E6: COMPLEMENT PAIR WEIGHT PATTERN")
print("─" * 80)

comp_pairs = [p for p in pairs if p['is_pal']]
print(f"\n  Complement pairs (palindromic, orbit (0,0,0)):")
print(f"  {'Pair':>4s}  {'Wt A':>4s} {'Wt B':>4s}  {'Dir':>8s}  {'Position':>8s}  Names")

for p in comp_pairs:
    wa = p['a']['weight']
    wb = p['b']['weight']
    direction = 'HEAVIER→' if wa > wb else '→HEAVIER' if wb > wa else 'EQUAL'
    pos_label = 'upper' if p['idx'] < 15 else 'lower'
    print(f"  {p['idx']+1:4d}  {wa:4d} {wb:4d}  {direction:>8s}  {pos_label:>8s}  "
          f"{p['a']['name']}-{p['b']['name']}")

# The complement pairs in orbit (0,0,0) have these weight values:
# Pair 1: 6→0 (heavier first, Qian→Kun)
# Pair 14: 2→4 (lighter first, Yi→Da Guo)  
# Pair 15: 2→4 (lighter first, Kan→Li)
# Pair 31: 4→2 (heavier first, Zhong Fu→Xiao Guo)

# Pattern: pairs 1, 31 have heavier first (bookend pairs)
# Pairs 14, 15 have lighter first (adjacent pairs near canon break)
print(f"\n  Pattern: bookend pairs (1, 31) have heavier first")
print(f"  Interior pairs (14, 15) have lighter first")
print(f"  This correlates with canon position, not weight")


# ─── E7: Yang flow significance test ───────────────────────────────────────

print("\n" + "─" * 80)
print("E7: YANG DRAINAGE SIGNIFICANCE")
print("─" * 80)

# Under random orientation of the 4 complement pairs only (rest are weight-neutral),
# how often do we see the observed yang drainage pattern?

# The 4 complement pairs control the ONLY weight-dependent orientation effects
# All other pairs: flipping has zero effect on weight trajectory

# Octet yang drainage: net weight change from first to last hex in each octet
octet_drains = []
for oct_idx in range(8):
    start = oct_idx * 8
    end = start + 8
    octet_drains.append(weights[end-1] - weights[start])

print(f"  KW octet drains: {octet_drains}")
positive = sum(1 for d in octet_drains if d > 0)
negative = sum(1 for d in octet_drains if d < 0)
zero = sum(1 for d in octet_drains if d == 0)
print(f"  Gaining: {positive}, Losing: {negative}, Zero: {zero}")

# Monte Carlo: flip only the 4 complement pairs randomly
comp_indices = [p['idx'] for p in comp_pairs]
print(f"\n  Complement pair indices: {comp_indices}")
print(f"  These are the ONLY pairs whose flip affects the weight trajectory")

# Under the 2^4 = 16 possible orientations of complement pairs:
n_drain_more = 0
kw_negative_count = negative  # KW has this many negative octets

for flip_mask in range(16):
    # Build flipped weight sequence
    test_weights = list(weights)
    for bit_idx, pair_idx in enumerate(comp_indices):
        if (flip_mask >> bit_idx) & 1:
            # Flip this pair
            test_weights[2*pair_idx], test_weights[2*pair_idx+1] = \
                test_weights[2*pair_idx+1], test_weights[2*pair_idx]
    
    # Count octet drains
    drains = []
    for oct_idx in range(8):
        start = oct_idx * 8
        drains.append(test_weights[start+7] - test_weights[start])
    
    neg_count = sum(1 for d in drains if d < 0)
    if neg_count >= kw_negative_count:
        n_drain_more += 1

print(f"  Exhaustive search over 16 orientations of complement pairs:")
print(f"  KW negative octets: {kw_negative_count}")
print(f"  Orientations with ≥{kw_negative_count} negative octets: {n_drain_more}/16")

# Also test with full random orientation (all 32 pairs)
n_drain_full = 0
for _ in range(N_TRIALS):
    flips = RNG.integers(0, 2, size=32)
    test_weights = []
    for k in range(N_PAIRS):
        a_w = pairs[k]['a']['weight']
        b_w = pairs[k]['b']['weight']
        if flips[k]:
            test_weights.extend([b_w, a_w])
        else:
            test_weights.extend([a_w, b_w])
    
    drains = [test_weights[oct*8 + 7] - test_weights[oct*8] for oct in range(8)]
    neg = sum(1 for d in drains if d < 0)
    if neg >= kw_negative_count:
        n_drain_full += 1

print(f"\n  Full random orientation ({N_TRIALS} trials):")
print(f"  P(≥{kw_negative_count} negative octets) = {n_drain_full/N_TRIALS:.4f}")


# ─── E8: Weight monotonicity within quartets ───────────────────────────────

print("\n" + "─" * 80)
print("E8: WEIGHT MONOTONICITY WITHIN QUARTETS")
print("─" * 80)

# A quartet = 2 pairs = 4 hexagrams
for q_idx in range(16):
    start = q_idx * 4
    q_weights = weights[start:start+4]
    
    # Check monotonicity
    mono_inc = all(q_weights[i] <= q_weights[i+1] for i in range(3))
    mono_dec = all(q_weights[i] >= q_weights[i+1] for i in range(3))
    
    # The bridge is between positions 1→2 (index start+1 → start+2)
    bridge_change = q_weights[2] - q_weights[1]
    pair1_change = q_weights[1] - q_weights[0]
    pair2_change = q_weights[3] - q_weights[2]
    
    if mono_inc or mono_dec:
        label = '↑' if mono_inc else '↓'
    else:
        label = '~'
    
    print(f"  Q{q_idx+1:2d}: {q_weights}  {label}  "
          f"(pair: {pair1_change:+d}, bridge: {bridge_change:+d}, pair: {pair2_change:+d})")

# How many quartets are monotone?
mono_count = 0
for q_idx in range(16):
    q_weights = weights[q_idx*4:(q_idx+1)*4]
    mono_inc = all(q_weights[i] <= q_weights[i+1] for i in range(3))
    mono_dec = all(q_weights[i] >= q_weights[i+1] for i in range(3))
    if mono_inc or mono_dec:
        mono_count += 1

print(f"\n  Monotone quartets: {mono_count}/16")

# Monte Carlo
mc_mono = []
for _ in range(N_TRIALS):
    flips = RNG.integers(0, 2, size=32)
    test_w = []
    for k in range(N_PAIRS):
        aw = pairs[k]['a']['weight']
        bw = pairs[k]['b']['weight']
        if flips[k]:
            test_w.extend([bw, aw])
        else:
            test_w.extend([aw, bw])
    
    mc = 0
    for q in range(16):
        qw = test_w[q*4:(q+1)*4]
        if all(qw[i] <= qw[i+1] for i in range(3)) or all(qw[i] >= qw[i+1] for i in range(3)):
            mc += 1
    mc_mono.append(mc)

mc_mono = np.array(mc_mono)
p_mono = np.mean(mc_mono >= mono_count)
print(f"  p(≥{mono_count} monotone quartets) = {p_mono:.4f}")
print(f"  Random mean: {np.mean(mc_mono):.2f} ± {np.std(mc_mono):.2f}")


# ═══════════════════════════════════════════════════════════════════════════════
# JOINT D+E: POSITION-WEIGHT INTERACTION
# ═══════════════════════════════════════════════════════════════════════════════

print("\n\n" + "=" * 80)
print("JOINT D+E: POSITION-WEIGHT INTERACTION")
print("=" * 80)

# Position weight: in each orbit, different positions have different weights.
# For orbit (0,0,0): palindromes, weights span 0-6
# For orbit (1,1,1): all weight 3
# For other orbits: mixed weights

print("\n  Weight by position within each orbit:")
for sig in sorted(ORBIT_NAMES.keys()):
    hexes_in_orbit = [(tuple(h), weight(tuple(h)), tuple(h)[:3]) 
                       for h in all_bits() if xor_sig(tuple(h)) == sig]
    hexes_in_orbit.sort(key=lambda x: x[2])
    
    print(f"\n  Orbit ({','.join(map(str,sig))}) = {ORBIT_NAMES[sig]}:")
    for h, w, pos in hexes_in_orbit:
        pos_str = ''.join(map(str, pos))
        visited = any(hd['hex'] == h for hd in hex_data if hd['pos'] == pos and hd['orbit'] == sig)
        # Find when this hex appears
        step = next((hd['idx'] for hd in hex_data if hd['hex'] == h), None)
        print(f"    pos={pos_str}  wt={w}  hex={''.join(map(str,h))}  step={step+1 if step is not None else '?':>3}")


print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
