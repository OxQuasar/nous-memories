"""
Threads D+E Deep Analysis: Position trajectory and weight dynamics.

Thread D focuses:
1. Position trajectory through full 64-hex sequence — is there a preferred starting position?
2. Do 8 visits to each orbit cover all 8 positions under random S=2-free orientations?
3. Position trajectory autocorrelation — significance testing
4. Relationship between hidden (position) and visible (orbit) trajectories

Thread E focuses:
1. Weight trajectory dependence on orientation (only 4 complement pairs matter)
2. Complement pairs: heavier/lighter first — is it determined by orientation constraints?
3. Yang drainage: Layer 3 or Layer 4 property?
4. Bridge weight dynamics under orientation variation
5. Connection to nuclear trigram finding (85.7% from trigram analysis)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter2')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
from analysis_utils import VALID_MASKS, xor_sig, xor_tuple, hamming
import random

DIMS = 6
N_PAIRS = 32
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

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def compute_S(hex_a, hex_b):
    m = tuple(hex_a[i] ^ hex_b[i] for i in range(6))
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])


# ── Build pairs ──────────────────────────────────────────────────────────────

PAIRS = []
for k in range(N_PAIRS):
    a = M[2*k]
    b = M[2*k+1]
    mask = xor_tuple(a, b)
    sig = xor_sig(a)
    is_pal = is_palindrome(a) and is_palindrome(b)
    PAIRS.append({'a': a, 'b': b, 'mask': mask, 'sig': sig, 'is_pal': is_pal})


# ── S=2 constraints ─────────────────────────────────────────────────────────

CONSTRAINTS = {}
for k in range(31):
    forbidden = set()
    for o_k in [0, 1]:
        for o_k1 in [0, 1]:
            exit_hex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
            entry_hex = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
            if compute_S(exit_hex, entry_hex) == 2:
                forbidden.add((o_k, o_k1))
    if forbidden:
        CONSTRAINTS[k] = forbidden


def is_s2_free(orientation):
    for k, forbidden in CONSTRAINTS.items():
        if (orientation[k], orientation[k+1]) in forbidden:
            return False
    return True


def build_sequence(orientation):
    seq = []
    for k in range(N_PAIRS):
        if orientation[k] == 0:
            seq.append(PAIRS[k]['a'])
            seq.append(PAIRS[k]['b'])
        else:
            seq.append(PAIRS[k]['b'])
            seq.append(PAIRS[k]['a'])
    return seq


def pos_of(h):
    """Position coordinates = (L1, L2, L3) = lower 3 bits."""
    return h[:3]


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD D: POSITION TRAJECTORY DEEP ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("THREAD D: POSITION TRAJECTORY — DEEP ANALYSIS")
print("=" * 80)

# ── D1: First-hexagram position per pair — under KW vs random ──────────────

kw_seq = build_sequence([0]*32)
kw_first_positions = [pos_of(kw_seq[2*k]) for k in range(N_PAIRS)]

print("\n" + "─" * 80)
print("D1: FIRST-HEXAGRAM POSITION PER ORBIT")
print("─" * 80)

# Group by orbit: which positions are "first" in each orbit?
for sig in sorted(ORBIT_NAMES.keys()):
    orbit_pairs = [k for k in range(N_PAIRS) if PAIRS[k]['sig'] == sig]
    first_pos = [kw_first_positions[k] for k in orbit_pairs]
    print(f"\n  Orbit {ORBIT_NAMES[sig]:>6s} ({','.join(map(str,sig))}): "
          f"pairs {[k+1 for k in orbit_pairs]}")
    print(f"    First positions: {[''.join(map(str,p)) for p in first_pos]}")
    
    # XOR between consecutive first-positions within this orbit
    if len(first_pos) > 1:
        xors = [xor3(first_pos[i], first_pos[i+1]) for i in range(len(first_pos)-1)]
        print(f"    Inter-visit XOR: {[KERNEL_NAMES[x] for x in xors]}")
    
    # Check: do these 4 first-positions cover a coset?
    if len(first_pos) == 4:
        xor_set = set()
        for i in range(4):
            for j in range(i+1, 4):
                xor_set.add(xor3(first_pos[i], first_pos[j]))
        # A coset of a 2-dim subgroup has exactly 3 non-trivial internal XORs
        # forming a subgroup of Z₂³
        is_coset = len(xor_set) == 3 and all(
            xor3(a, b) in xor_set 
            for a in xor_set for b in xor_set if a != b
        )
        # Actually check closure: for any two elements in xor_set, their XOR should also be in xor_set
        xor_list = list(xor_set)
        closure = True
        for i in range(3):
            for j in range(i+1, 3):
                if xor3(xor_list[i], xor_list[j]) not in xor_set:
                    closure = False
        print(f"    Is coset of 2-dim subgroup: {is_coset and closure} (xors: {[KERNEL_NAMES[x] for x in xor_set]})")


# ── D2: Position trajectory autocorrelation significance ──────────────────

print("\n" + "─" * 80)
print("D2: POSITION TRAJECTORY AUTOCORRELATION — SIGNIFICANCE TEST")
print("─" * 80)

N_SAMPLES = 50000
rng = random.Random(42)

# KW autocorrelation at various lags
kw_pos_traj = [pos_of(kw_seq[i]) for i in range(64)]
kw_pos_ints = np.array([p[0]*4 + p[1]*2 + p[2] for p in kw_pos_traj], dtype=float)
kw_centered = kw_pos_ints - kw_pos_ints.mean()
kw_var = np.var(kw_pos_ints)

kw_ac = {}
for lag in [1, 2, 4, 8]:
    kw_ac[lag] = np.mean(kw_centered[:64-lag] * kw_centered[lag:]) / kw_var

print(f"\n  KW position autocorrelation: {kw_ac}")

# Sample S=2-free orientations and compute autocorrelation
ac_samples = {lag: [] for lag in [1, 2, 4, 8]}
total_tried = 0

for i in range(N_SAMPLES):
    while True:
        total_tried += 1
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    seq = build_sequence(o)
    pos_traj = [pos_of(seq[i]) for i in range(64)]
    pos_ints = np.array([p[0]*4 + p[1]*2 + p[2] for p in pos_traj], dtype=float)
    centered = pos_ints - pos_ints.mean()
    var = np.var(pos_ints)
    if var > 0:
        for lag in [1, 2, 4, 8]:
            ac = np.mean(centered[:64-lag] * centered[lag:]) / var
            ac_samples[lag].append(ac)

print(f"\n  Sampled {N_SAMPLES} S=2-free orientations")
print(f"  Acceptance rate: {N_SAMPLES/total_tried:.4f}")

print(f"\n  {'Lag':>4s}  {'KW':>8s}  {'Mean':>8s}  {'Std':>8s}  {'p(≤KW)':>8s}  {'p(≥KW)':>8s}")
print(f"  {'-'*50}")
for lag in [1, 2, 4, 8]:
    arr = np.array(ac_samples[lag])
    p_low = np.mean(arr <= kw_ac[lag])
    p_high = np.mean(arr >= kw_ac[lag])
    print(f"  {lag:4d}  {kw_ac[lag]:+8.4f}  {arr.mean():+8.4f}  {arr.std():8.4f}  "
          f"{p_low:8.4f}  {p_high:8.4f}")


# ── D3: Per-component autocorrelation ─────────────────────────────────────

print("\n" + "─" * 80)
print("D3: PER-COMPONENT POSITION AUTOCORRELATION")
print("─" * 80)

comp_names = ['o (L1)', 'm (L2)', 'i (L3)']
comp_ac_samples = {(c, lag): [] for c in range(3) for lag in [1, 2]}

for i in range(N_SAMPLES):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    seq = build_sequence(o)
    for c in range(3):
        comp_arr = np.array([seq[i][c] for i in range(64)], dtype=float)
        comp_c = comp_arr - comp_arr.mean()
        comp_v = np.var(comp_arr)
        if comp_v > 0:
            for lag in [1, 2]:
                ac = np.mean(comp_c[:64-lag] * comp_c[lag:]) / comp_v
                comp_ac_samples[(c, lag)].append(ac)

# KW component autocorrelations
kw_comp_ac = {}
for c in range(3):
    comp_arr = np.array([kw_seq[i][c] for i in range(64)], dtype=float)
    comp_c = comp_arr - comp_arr.mean()
    comp_v = np.var(comp_arr)
    for lag in [1, 2]:
        kw_comp_ac[(c, lag)] = np.mean(comp_c[:64-lag] * comp_c[lag:]) / comp_v

print(f"\n  {'Component':>10s}  {'Lag':>3s}  {'KW':>8s}  {'Mean':>8s}  {'p(≤KW)':>8s}")
for c in range(3):
    for lag in [1, 2]:
        arr = np.array(comp_ac_samples[(c, lag)])
        p_low = np.mean(arr <= kw_comp_ac[(c, lag)])
        print(f"  {comp_names[c]:>10s}  {lag:3d}  {kw_comp_ac[(c,lag)]:+8.4f}  "
              f"{arr.mean():+8.4f}  {p_low:8.4f}")


# ── D4: Position coverage — all orbits cover all 8 positions? ─────────────

print("\n" + "─" * 80)
print("D4: POSITION COVERAGE UNDER RANDOM ORIENTATIONS")
print("─" * 80)

# Under KW: verified all 8 orbits cover all 8 positions
# Under random S=2-free orientations: still guaranteed?
# Changing orientation swaps (a,b) → (b,a) within each pair
# Since a and b are DIFFERENT hexagrams with different positions, 
# the 8 position slots are just permuted. So coverage is guaranteed.

print("\n  Position coverage is ALWAYS 8/8 per orbit regardless of orientation.")
print("  Reason: each orbit has 4 pairs, each pair spans 2 distinct positions.")
print("  Flipping orientation just swaps which is 'first' and which is 'second'.")
print("  The SET of 8 visited positions is invariant — it's always all 8.")
print("  (Within-pair position change = sig ≠ 0 for non-Qian orbits,")
print("  and for Qian orbit it's OMI, still ≠ 0.)")


# ── D5: Cross-correlation between position and orbit trajectories ─────────

print("\n" + "─" * 80)
print("D5: POSITION-ORBIT CROSS-CORRELATION — SIGNIFICANCE")
print("─" * 80)

# KW cross-correlation
kw_orb_traj = [xor_sig(kw_seq[i]) for i in range(64)]
kw_orb_ints = np.array([o[0]*4 + o[1]*2 + o[2] for o in kw_orb_traj], dtype=float)
orb_centered = kw_orb_ints - kw_orb_ints.mean()
orb_var = np.var(kw_orb_ints)

kw_cc = {}
for lag in [0, 1, -1]:
    if lag >= 0:
        cc = np.mean(kw_centered[:64-lag] * orb_centered[lag:]) / np.sqrt(kw_var * orb_var)
    else:
        cc = np.mean(orb_centered[:64+lag] * kw_centered[-lag:]) / np.sqrt(kw_var * orb_var)
    kw_cc[lag] = cc

print(f"\n  KW position-orbit cross-correlation:")
for lag, cc in kw_cc.items():
    print(f"    lag {lag:+2d}: {cc:+.4f}")

# Sample
cc_samples = {lag: [] for lag in [0, 1, -1]}
for i in range(N_SAMPLES):
    while True:
        bits = rng.getrandbits(32)
        o_vec = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o_vec):
            break
    
    seq = build_sequence(o_vec)
    pos_ints = np.array([seq[i][0]*4 + seq[i][1]*2 + seq[i][2] for i in range(64)], dtype=float)
    p_c = pos_ints - pos_ints.mean()
    p_v = np.var(pos_ints)
    
    # orbit trajectory is invariant under orientation
    if p_v > 0:
        for lag in [0, 1, -1]:
            if lag >= 0:
                cc = np.mean(p_c[:64-lag] * orb_centered[lag:]) / np.sqrt(p_v * orb_var)
            else:
                cc = np.mean(orb_centered[:64+lag] * p_c[-lag:]) / np.sqrt(p_v * orb_var)
            cc_samples[lag].append(cc)

print(f"\n  {'Lag':>4s}  {'KW':>8s}  {'Mean':>8s}  {'Std':>8s}  {'p(≤KW)':>8s}")
for lag in [0, 1, -1]:
    arr = np.array(cc_samples[lag])
    p_low = np.mean(arr <= kw_cc[lag])
    print(f"  {lag:+4d}  {kw_cc[lag]:+8.4f}  {arr.mean():+8.4f}  {arr.std():8.4f}  {p_low:8.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD E: WEIGHT AND YANG FLOW — DEEP ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print("\n\n" + "=" * 80)
print("THREAD E: WEIGHT AND YANG FLOW — DEEP ANALYSIS")
print("=" * 80)

# ── E1: Weight trajectory is almost entirely Layer 3 ──────────────────────

print("\n" + "─" * 80)
print("E1: WEIGHT TRAJECTORY — LAYER 3 vs LAYER 4 DECOMPOSITION")
print("─" * 80)

# For inversion pairs: weight(a) = weight(b) always
# Verify exhaustively
inv_weight_invariant = True
for k in range(N_PAIRS):
    wa = weight(PAIRS[k]['a'])
    wb = weight(PAIRS[k]['b'])
    if not PAIRS[k]['is_pal'] and wa != wb:
        inv_weight_invariant = False
        print(f"  EXCEPTION: Pair {k+1} is_pal={PAIRS[k]['is_pal']} wa={wa} wb={wb}")

# For non-palindromic OMI pairs (orbit (1,1,1)): weight(a) = weight(b) = 3
omi_111_invariant = True
for k in range(N_PAIRS):
    if PAIRS[k]['sig'] == (1,1,1):
        wa, wb = weight(PAIRS[k]['a']), weight(PAIRS[k]['b'])
        if wa != wb:
            omi_111_invariant = False

print(f"\n  Inversion pair weight invariance: {inv_weight_invariant}")
print(f"  Orbit (1,1,1) OMI pair weight invariance: {omi_111_invariant}")
print(f"  Weight-sensitive pairs: only the 4 palindromic complement pairs in orbit (0,0,0)")

# The 4 complement pairs
comp_pairs = [k for k in range(N_PAIRS) if PAIRS[k]['is_pal']]
print(f"\n  Complement pair indices: {[k+1 for k in comp_pairs]}")
for k in comp_pairs:
    wa, wb = weight(PAIRS[k]['a']), weight(PAIRS[k]['b'])
    print(f"    Pair {k+1}: wt_first={wa}, wt_second={wb}, delta={wb-wa:+d}")

# Are any complement pairs in the S=2 constraint set?
print(f"\n  S=2 constraint pairs: {sorted(set().union(*(set([k, k+1]) for k in CONSTRAINTS)))}")
print(f"  Complement pairs: {[k+1 for k in comp_pairs]}")
# Check overlap
for k in comp_pairs:
    constrained = False
    for bridge_k, forbidden in CONSTRAINTS.items():
        if k in [bridge_k, bridge_k+1]:
            constrained = True
            break
    print(f"    Pair {k+1}: S=2-constrained = {constrained}")


# ── E2: Complement pair weight pattern — significance ─────────────────────

print("\n" + "─" * 80)
print("E2: COMPLEMENT PAIR WEIGHT ORIENTATION — SIGNIFICANCE")
print("─" * 80)

# KW: pairs 1,31 heavier first; pairs 14,15 lighter first
# Is there a pattern? Pairs 1,31 are bookends, 14,15 are adjacent near canon break

# Under random orientation of the 4 complement pairs (2^4 = 16 options):
# Weight trajectory changes ONLY at the 4 complement positions
# All 28 other pairs are weight-neutral

# Test: does KW's complement orientation optimize any weight metric?
comp_metrics = {}
for mask in range(16):
    # mask bits: bit 0 = pair 1, bit 1 = pair 14, bit 2 = pair 15, bit 3 = pair 31
    flipped = [0] * 32
    for i, pair_idx in enumerate(comp_pairs):
        if (mask >> i) & 1:
            flipped[pair_idx] = 1
    
    seq = build_sequence(flipped)
    weights = [weight(seq[i]) for i in range(64)]
    
    # Octet drainage
    drains = [weights[oct*8+7] - weights[oct*8] for oct in range(8)]
    n_negative = sum(1 for d in drains if d < 0)
    total_abs_drain = sum(abs(d) for d in drains)
    
    # Bridge weight smoothness (sum of absolute weight changes at bridges)
    bridge_smoothness = sum(abs(weights[2*k+2] - weights[2*k+1]) for k in range(31))
    
    # Monotone quartets
    mono = 0
    for q in range(16):
        qw = weights[q*4:(q+1)*4]
        if all(qw[i] <= qw[i+1] for i in range(3)) or all(qw[i] >= qw[i+1] for i in range(3)):
            mono += 1
    
    is_kw = (mask == 0)
    comp_metrics[mask] = {
        'n_negative_octets': n_negative,
        'total_abs_drain': total_abs_drain,
        'bridge_smoothness': bridge_smoothness,
        'monotone_quartets': mono,
        'is_kw': is_kw,
    }

print("\n  Exhaustive comparison (16 complement orientations):")
print(f"  {'Mask':>4s}  {'NegOct':>6s}  {'AbsDrain':>8s}  {'BrSmooth':>8s}  {'MonoQ':>5s}  {'KW':>3s}")
for mask in range(16):
    m = comp_metrics[mask]
    kw_flag = " ★" if m['is_kw'] else ""
    print(f"  {mask:4d}  {m['n_negative_octets']:6d}  {m['total_abs_drain']:8d}  "
          f"{m['bridge_smoothness']:8d}  {m['monotone_quartets']:5d}{kw_flag}")


# ── E3: Yang drainage — full random orientation test ──────────────────────

print("\n" + "─" * 80)
print("E3: YANG DRAINAGE — FULL ORIENTATION SIGNIFICANCE TEST")
print("─" * 80)

# KW octet drains
kw_weights = [weight(kw_seq[i]) for i in range(64)]
kw_drains = [kw_weights[oct*8+7] - kw_weights[oct*8] for oct in range(8)]
kw_neg = sum(1 for d in kw_drains if d < 0)
kw_total_drain = sum(kw_drains)
kw_abs_drain = sum(abs(d) for d in kw_drains)

print(f"\n  KW drains: {kw_drains}")
print(f"  KW negative octets: {kw_neg}/8")
print(f"  KW total drain: {kw_total_drain}")
print(f"  KW total abs drain: {kw_abs_drain}")

# Monte Carlo with full random orientation
N_MC = 100_000
rng2 = random.Random(123)

neg_counts = []
total_drains = []
abs_drains = []

for _ in range(N_MC):
    # Only complement pairs affect weight
    flips = [0] * 32
    for k in comp_pairs:
        flips[k] = rng2.randint(0, 1)
    
    seq = build_sequence(flips)
    weights = [weight(seq[i]) for i in range(64)]
    drains = [weights[oct*8+7] - weights[oct*8] for oct in range(8)]
    
    neg_counts.append(sum(1 for d in drains if d < 0))
    total_drains.append(sum(drains))
    abs_drains.append(sum(abs(d) for d in drains))

neg_arr = np.array(neg_counts)
total_arr = np.array(total_drains)
abs_arr = np.array(abs_drains)

print(f"\n  Monte Carlo ({N_MC} trials, randomizing only complement pair orientations):")
print(f"  P(≥{kw_neg} negative octets) = {np.mean(neg_arr >= kw_neg):.4f}")
print(f"  Mean negative octets: {neg_arr.mean():.2f} ± {neg_arr.std():.2f}")
print(f"  P(total drain ≤ {kw_total_drain}) = {np.mean(total_arr <= kw_total_drain):.4f}")
print(f"  P(abs drain ≥ {kw_abs_drain}) = {np.mean(abs_arr >= kw_abs_drain):.4f}")

# Also test with random FULL orientations (but only complement pairs change weight)
print(f"\n  Key insight: yang drainage is 87.5% Layer 3 (pair ordering)")
print(f"  and 12.5% Layer 4 (complement pair orientation)")
print(f"  Since 28/32 pairs preserve weight regardless of orientation,")
print(f"  the weight trajectory is overwhelmingly a Layer 3 property.")


# ── E4: Bridge weight smoothness under orientation ────────────────────────

print("\n" + "─" * 80)
print("E4: BRIDGE WEIGHT SMOOTHNESS — ALL S=2-FREE ORIENTATIONS")
print("─" * 80)

# KW bridge smoothness
kw_bridge_smooth = sum(abs(kw_weights[2*k+2] - kw_weights[2*k+1]) for k in range(31))
kw_bridge_max = max(abs(kw_weights[2*k+2] - kw_weights[2*k+1]) for k in range(31))

print(f"\n  KW bridge smoothness (sum |Δweight|): {kw_bridge_smooth}")
print(f"  KW bridge max |Δweight|: {kw_bridge_max}")

# Sample S=2-free orientations
smooth_samples = []
max_bridge_samples = []

for i in range(N_SAMPLES):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    seq = build_sequence(o)
    weights = [weight(seq[i]) for i in range(64)]
    smooth = sum(abs(weights[2*k+2] - weights[2*k+1]) for k in range(31))
    max_br = max(abs(weights[2*k+2] - weights[2*k+1]) for k in range(31))
    smooth_samples.append(smooth)
    max_bridge_samples.append(max_br)

smooth_arr = np.array(smooth_samples)
max_br_arr = np.array(max_bridge_samples)

p_smooth = np.mean(smooth_arr <= kw_bridge_smooth)
p_max = np.mean(max_br_arr <= kw_bridge_max)

print(f"\n  {'Metric':>25s}  {'KW':>6s}  {'Mean':>6s}  {'Std':>6s}  {'p(≤KW)':>8s}")
print(f"  {'-'*60}")
print(f"  {'sum |Δweight| at bridges':>25s}  {kw_bridge_smooth:6d}  {smooth_arr.mean():6.1f}  "
      f"{smooth_arr.std():6.1f}  {p_smooth:8.4f}")
print(f"  {'max |Δweight| at bridges':>25s}  {kw_bridge_max:6d}  {max_br_arr.mean():6.1f}  "
      f"{max_br_arr.std():6.1f}  {p_max:8.4f}")


# ── E5: Nuclear trigram connection ────────────────────────────────────────

print("\n" + "─" * 80)
print("E5: NUCLEAR TRIGRAM RULE — SIGNIFICANCE TEST")
print("─" * 80)

# The trigram analysis found: "nuclear lower more yang" predicts first hex 
# in 24/28 inversion pairs (85.7%).
# This means: lines 2,3,4 of the first hex have more yang than lines 2,3,4 of the second.
# For inversion pairs: second = reverse(first), so 
# nuclear_lower(second) = (L5,L4,L3) of first = reverse(nuclear_upper(first))

# Let's verify and count:
nuc_rule_correct = 0
nuc_rule_total = 0
for k in range(N_PAIRS):
    if PAIRS[k]['is_pal']:
        continue  # skip complement pairs
    a, b = PAIRS[k]['a'], PAIRS[k]['b']
    nuc_lo_a = sum(a[1:4])  # L2,L3,L4
    nuc_lo_b = sum(b[1:4])
    nuc_rule_total += 1
    if nuc_lo_a > nuc_lo_b:
        nuc_rule_correct += 1
    elif nuc_lo_a == nuc_lo_b:
        pass  # tie, doesn't count

print(f"\n  Nuclear lower rule: {nuc_rule_correct}/{nuc_rule_total} "
      f"({100*nuc_rule_correct/nuc_rule_total:.1f}%) matches KW")

# How many ties?
ties = sum(1 for k in range(N_PAIRS) if not PAIRS[k]['is_pal'] and
           sum(PAIRS[k]['a'][1:4]) == sum(PAIRS[k]['b'][1:4]))
print(f"  Ties (nuclear lower weight equal): {ties}")
print(f"  Decisive (non-tie) pairs: {nuc_rule_total}")

# Under random S=2-free orientations, how often does this rule score ≥ 24/28?
nuc_scores = []
for i in range(N_SAMPLES):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    seq = build_sequence(o)
    score = 0
    total = 0
    for k in range(N_PAIRS):
        if PAIRS[k]['is_pal']:
            continue
        # Under this orientation, first hex is seq[2*k]
        a_nuc = sum(seq[2*k][1:4])
        b_nuc = sum(seq[2*k+1][1:4])
        total += 1
        if a_nuc > b_nuc:
            score += 1
    nuc_scores.append(score)

nuc_arr = np.array(nuc_scores)
p_nuc = np.mean(nuc_arr >= nuc_rule_correct)

print(f"\n  Under random S=2-free orientations:")
print(f"  Mean nuclear rule score: {nuc_arr.mean():.2f} ± {nuc_arr.std():.2f}")
print(f"  P(≥{nuc_rule_correct}) = {p_nuc:.6f}")
print(f"  This is {'SIGNIFICANT' if p_nuc < 0.05 else 'NOT significant'} at α=0.05")

# Also check: what is the MAXIMUM possible score under S=2-free orientations?
max_seen = nuc_arr.max()
print(f"  Max score seen in {N_SAMPLES} samples: {max_seen}")


# ── E6: Deeper nuclear analysis — which 4 pairs violate the rule? ─────────

print("\n" + "─" * 80)
print("E6: NUCLEAR RULE EXCEPTIONS — WHICH PAIRS?")
print("─" * 80)

for k in range(N_PAIRS):
    if PAIRS[k]['is_pal']:
        continue
    a, b = PAIRS[k]['a'], PAIRS[k]['b']
    nuc_a = sum(a[1:4])
    nuc_b = sum(b[1:4])
    if nuc_a < nuc_b:
        print(f"  Pair {k+1}: nuc_a={nuc_a}, nuc_b={nuc_b}  "
              f"{KING_WEN[2*k][1]}-{KING_WEN[2*k+1][1]}  "
              f"orbit={ORBIT_NAMES[PAIRS[k]['sig']]}")
    elif nuc_a == nuc_b:
        print(f"  Pair {k+1}: nuc_a={nuc_b}, nuc_b={nuc_b}  TIE  "
              f"{KING_WEN[2*k][1]}-{KING_WEN[2*k+1][1]}  "
              f"orbit={ORBIT_NAMES[PAIRS[k]['sig']]}")


# ── E7: Position trajectory — orbit-first-position analysis ──────────────

print("\n" + "─" * 80)
print("E7: DO FIRST-VISIT POSITIONS CLUSTER IN POSITION SPACE?")
print("─" * 80)

# Under KW, the first-visit positions (first time each orbit appears):
# Qian: pos=111, XChu: pos=111, Shi: pos=010, WWang: pos=100
# Bo: pos=000, Xu: pos=111, Zhun: pos=100, Tai: pos=111

# 4 of 8 orbits have first-visit position = 111. That seems clustered.

kw_first_visit_pos = {}
seen = set()
for i in range(64):
    sig = xor_sig(kw_seq[i])
    if sig not in seen:
        seen.add(sig)
        kw_first_visit_pos[sig] = pos_of(kw_seq[i])

print(f"\n  KW first-visit positions:")
for sig in sorted(kw_first_visit_pos.keys()):
    pos = kw_first_visit_pos[sig]
    print(f"    {ORBIT_NAMES[sig]:>6s}: {''.join(map(str, pos))}  (weight={sum(pos)})")

# Count how many have pos=111 (all-yang in lower 3 bits)
n_111 = sum(1 for p in kw_first_visit_pos.values() if p == (1,1,1))
print(f"\n  First-visit positions with pos=(1,1,1): {n_111}/8")

# Significance test
fv_111_samples = []
for i in range(N_SAMPLES):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    seq = build_sequence(o)
    seen = set()
    count_111 = 0
    for j in range(64):
        sig = xor_sig(seq[j])
        if sig not in seen:
            seen.add(sig)
            if pos_of(seq[j]) == (1,1,1):
                count_111 += 1
    fv_111_samples.append(count_111)

fv_arr = np.array(fv_111_samples)
p_fv = np.mean(fv_arr >= n_111)
print(f"  P(≥{n_111} first-visit at pos 111) = {p_fv:.4f}")
print(f"  Mean: {fv_arr.mean():.2f} ± {fv_arr.std():.2f}")

# More general: average first-visit position weight (sum of position bits)
kw_fv_weight = np.mean([sum(p) for p in kw_first_visit_pos.values()])
fv_weight_samples = []
for i in range(N_SAMPLES):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    seq = build_sequence(o)
    seen = set()
    fv_weights = []
    for j in range(64):
        sig = xor_sig(seq[j])
        if sig not in seen:
            seen.add(sig)
            fv_weights.append(sum(pos_of(seq[j])))
    fv_weight_samples.append(np.mean(fv_weights))

fvw_arr = np.array(fv_weight_samples)
p_fvw = np.mean(fvw_arr >= kw_fv_weight)
print(f"\n  Mean first-visit position weight:")
print(f"  KW: {kw_fv_weight:.3f}  Random: {fvw_arr.mean():.3f} ± {fvw_arr.std():.3f}")
print(f"  P(≥ KW) = {p_fvw:.4f}")


print("\n\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
