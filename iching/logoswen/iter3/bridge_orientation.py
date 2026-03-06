"""
Thread C — Part 1: Bridge-orientation interaction analysis.

For each of the 31 bridges (between pair k and pair k+1), the bridge mask
depends on which hexagram exits pair k and which enters pair k+1.
Flipping orientation of either pair changes the bridge mask.

This script:
1. For each bridge, compute the 4 orientation variants (flip pair k, flip pair k+1, flip both)
2. Verify that orbit_Δ is invariant under orientation flips
3. For each variant: compute S value, Hamming weight, kernel dressing
4. Identify which bridges are S=2-susceptible under which orientations
5. Compute per-bridge S=2 avoidance constraints
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

DIMS = 6

# ── Data ──────────────────────────────────────────────────────────────────────

M = [tuple(b) for b in all_bits()]

# The 32 KW pairs
PAIRS = []
for k in range(32):
    a = M[2 * k]
    b = M[2 * k + 1]
    mask = tuple(a[i] ^ b[i] for i in range(DIMS))
    PAIRS.append({'a': a, 'b': b, 'mask': mask})

# Generator lookup
VALID_MASKS = {
    (0,0,0,0,0,0): 'id',  (1,0,0,0,0,1): 'O',  (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',   (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',  (1,1,1,1,1,1): 'OMI',
}

GEN_BITS = {
    'O': (1,0,0,0,0,1), 'M': (0,1,0,0,1,0), 'I': (0,0,1,1,0,0),
}

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}


def xor_sig(h):
    """Orbit signature."""
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])


def xor6(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def compute_S(hex_a, hex_b):
    """S value: number of mirror-pair positions where both bits change."""
    m = xor6(hex_a, hex_b)
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])


def kernel_dressing(hex_a, hex_b):
    """
    Kernel dressing: the symmetric (position) component of the bridge mask.
    For mask m, kernel 3-bit code = (m[5], m[4], m[3]) — the upper half.
    This decomposes the 6-bit bridge mask into orbit change + position change.
    Returns the kernel as a 3-bit tuple and its generator name.
    """
    m = xor6(hex_a, hex_b)
    k = (m[5], m[4], m[3])
    gen_6 = (k[0], k[1], k[2], k[2], k[1], k[0])
    name = VALID_MASKS.get(gen_6, '?')
    return k, name


def orbit_delta(hex_a, hex_b):
    """Orbit change between two hexagrams."""
    return tuple(xor_sig(hex_a)[i] ^ xor_sig(hex_b)[i] for i in range(3))


# ═══════════════════════════════════════════════════════════════════════════════
# 1. PER-BRIDGE: 4 ORIENTATION VARIANTS
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("1. PER-BRIDGE ORIENTATION ANALYSIS")
print("   For each bridge k (between pair k and pair k+1):")
print("   4 variants: (kw, flip_left, flip_right, flip_both)")
print("=" * 80)
print()

# Orientation labels
ORI_LABELS = ['kw', 'flip_L', 'flip_R', 'flip_LR']

bridge_data = []

for k in range(31):
    pair_L = PAIRS[k]      # left pair (pair k)
    pair_R = PAIRS[k + 1]  # right pair (pair k+1)
    
    # KW orientation: exit = pair_L['b'], entry = pair_R['a']
    # Flip left: exit = pair_L['a'], entry = pair_R['a']
    # Flip right: exit = pair_L['b'], entry = pair_R['b']
    # Flip both: exit = pair_L['a'], entry = pair_R['b']
    
    exits  = [pair_L['b'], pair_L['a'], pair_L['b'], pair_L['a']]
    enters = [pair_R['a'], pair_R['a'], pair_R['b'], pair_R['b']]
    
    variants = []
    for label, ex, en in zip(ORI_LABELS, exits, enters):
        mask = xor6(ex, en)
        h = sum(mask)
        s = compute_S(ex, en)
        k3, k_name = kernel_dressing(ex, en)
        od = orbit_delta(ex, en)
        variants.append({
            'label': label,
            'exit': ex, 'entry': en,
            'mask': mask, 'hamming': h, 'S': s,
            'kernel': k3, 'kernel_name': k_name,
            'orbit_delta': od,
        })
    
    bridge_data.append({
        'idx': k,
        'pair_L': k, 'pair_R': k + 1,
        'orbit_L': xor_sig(pair_L['a']),
        'orbit_R': xor_sig(pair_R['a']),
        'variants': variants,
    })

# Print results
for bd in bridge_data:
    k = bd['idx']
    oL = ORBIT_NAMES[bd['orbit_L']]
    oR = ORBIT_NAMES[bd['orbit_R']]
    
    print(f"  Bridge {k:2d}: {oL:>6s} → {oR:<6s}")
    for v in bd['variants']:
        s2_flag = " ★S=2" if v['S'] == 2 else ""
        print(f"    {v['label']:>8s}: H={v['hamming']} S={v['S']} "
              f"kernel={v['kernel_name']:>4s} "
              f"orbit_Δ={''.join(map(str,v['orbit_delta']))}"
              f"{s2_flag}")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. VERIFY: ORBIT DELTA IS ORIENTATION-INVARIANT
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("2. ORBIT DELTA INVARIANCE CHECK")
print("=" * 80)

all_invariant = True
for bd in bridge_data:
    deltas = [v['orbit_delta'] for v in bd['variants']]
    if len(set(deltas)) != 1:
        print(f"  Bridge {bd['idx']}: VARIANT ORBIT DELTAS! {deltas}")
        all_invariant = False

if all_invariant:
    print(f"  ✓ All 31 bridges: orbit_Δ identical across all 4 orientations")
else:
    print(f"  ✗ Some bridges have variant-dependent orbit_Δ!")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. S DISTRIBUTION ACROSS ORIENTATION VARIANTS
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("3. S VALUE DISTRIBUTION ACROSS ORIENTATIONS")
print("=" * 80)
print()

# For each bridge, how many of the 4 orientations produce S=0, S=1, S=2, S=3?
s_counts_per_bridge = []
s2_variants_per_bridge = []

for bd in bridge_data:
    s_vals = [v['S'] for v in bd['variants']]
    s_dist = Counter(s_vals)
    has_s2 = any(s == 2 for s in s_vals)
    s_counts_per_bridge.append(s_dist)
    s2_variants_per_bridge.append([v['label'] for v in bd['variants'] if v['S'] == 2])
    
    if has_s2:
        s2_labels = [v['label'] for v in bd['variants'] if v['S'] == 2]
        print(f"  B{bd['idx']:2d} ({ORBIT_NAMES[bd['orbit_L']]:>6s}→{ORBIT_NAMES[bd['orbit_R']]:<6s}): "
              f"S={s_vals}  S=2 at: {s2_labels}")

print()

# How many bridges can produce S=2 under any orientation?
bridges_with_any_s2 = sum(1 for sv in s2_variants_per_bridge if sv)
print(f"  Bridges with S=2 in at least one orientation: {bridges_with_any_s2}/31")

# How many of the 4 orientations produce S=2 at each susceptible bridge?
s2_count_dist = Counter(len(sv) for sv in s2_variants_per_bridge)
print(f"  Distribution of S=2 orientation count per bridge:")
for count in sorted(s2_count_dist.keys()):
    print(f"    {count}/4 orientations: {s2_count_dist[count]} bridges")

print()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. THE 11 S=2-SUSCEPTIBLE BRIDGES: KW ORIENTATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("4. S=2-SUSCEPTIBLE BRIDGES: DOES KW AVOID S=2?")
print("=" * 80)
print()

kw_avoids_s2 = True
for bd in bridge_data:
    kw_variant = bd['variants'][0]  # index 0 = KW orientation
    if kw_variant['S'] == 2:
        print(f"  B{bd['idx']}: KW HAS S=2!")
        kw_avoids_s2 = False

if kw_avoids_s2:
    print(f"  ✓ KW orientation avoids S=2 at all 31 bridges")
print()

# For each susceptible bridge, count how many orientations avoid S=2
print("  Per-bridge S=2 avoidance:")
for bd in bridge_data:
    s_vals = [v['S'] for v in bd['variants']]
    n_s2 = sum(1 for s in s_vals if s == 2)
    if n_s2 > 0:
        n_avoid = 4 - n_s2
        kw_s = bd['variants'][0]['S']
        status = "KW=✓" if kw_s != 2 else "KW=✗"
        print(f"    B{bd['idx']:2d} ({ORBIT_NAMES[bd['orbit_L']]:>6s}→{ORBIT_NAMES[bd['orbit_R']]:<6s}): "
              f"{n_avoid}/4 avoid S=2, {n_s2}/4 produce S=2  [{status}]")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. ORIENTATION BIT CONSTRAINTS FROM S=2 AVOIDANCE
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("5. ORIENTATION BIT CONSTRAINTS")
print("   Each bridge depends on 2 orientation bits: o_k (pair k) and o_{k+1} (pair k+1)")
print("   S=2 avoidance at bridge k constrains (o_k, o_{k+1})")
print("=" * 80)
print()

# Model: orientation bit o_k = 0 means KW orientation, o_k = 1 means flipped
# Bridge k connects pair k (exit) and pair k+1 (entry)
# (o_k, o_{k+1}) maps to: (0,0)=kw, (1,0)=flip_L, (0,1)=flip_R, (1,1)=flip_LR

constraints = []  # list of (bridge_idx, forbidden (o_k, o_{k+1}) tuples)
ori_map = [(0,0), (1,0), (0,1), (1,1)]  # maps variant index to (o_k, o_{k+1})

for bd in bridge_data:
    forbidden = []
    for vi, v in enumerate(bd['variants']):
        if v['S'] == 2:
            forbidden.append(ori_map[vi])
    if forbidden:
        constraints.append((bd['idx'], forbidden))
        k = bd['idx']
        print(f"  B{k:2d}: forbidden (o_{k}, o_{k+1}) = {forbidden}")

print(f"\n  Total constrained bridges: {len(constraints)}/31")

# Count the number of orientation bits that are involved in constraints
constrained_bits = set()
for k, forbid in constraints:
    constrained_bits.add(k)
    constrained_bits.add(k + 1)
print(f"  Pair indices involved in S=2 constraints: {sorted(constrained_bits)}")
print(f"  Number of constrained pairs: {len(constrained_bits)}/32")
unconstrained_bits = set(range(32)) - constrained_bits
print(f"  Unconstrained pairs: {sorted(unconstrained_bits)}")
print(f"  Number of unconstrained pairs: {len(unconstrained_bits)}")
print(f"  Free bits (no constraint): {len(unconstrained_bits)}")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. KERNEL CHAIN DEPENDENCE ON ORIENTATION
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("6. KERNEL CHAIN: KW vs ALTERNATIVE ORIENTATIONS")
print("=" * 80)
print()

# KW kernel chain
kw_kernels = [bd['variants'][0]['kernel_name'] for bd in bridge_data]
kw_kernel_freq = Counter(kw_kernels)
print(f"  KW kernel chain:")
print(f"    Sequence: {' '.join(kw_kernels)}")
print(f"    Frequency: {dict(kw_kernel_freq)}")

# For each bridge, show how the kernel changes across orientations
print(f"\n  Kernel variation across orientations:")
for bd in bridge_data:
    kernels = [v['kernel_name'] for v in bd['variants']]
    unique_kernels = set(kernels)
    if len(unique_kernels) > 1:
        print(f"    B{bd['idx']:2d}: {kernels} ({len(unique_kernels)} distinct)")

# Count how many bridges have orientation-dependent kernels
n_variable_kernel = sum(
    1 for bd in bridge_data
    if len(set(v['kernel_name'] for v in bd['variants'])) > 1
)
print(f"\n  Bridges with kernel dependent on orientation: {n_variable_kernel}/31")
print(f"  Bridges with kernel invariant to orientation: {31 - n_variable_kernel}/31")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. HAMMING WEIGHT DISTRIBUTION ACROSS ORIENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("7. HAMMING WEIGHT PATTERNS ACROSS ORIENTATIONS")
print("=" * 80)
print()

# KW Hamming weights
kw_weights = [bd['variants'][0]['hamming'] for bd in bridge_data]
print(f"  KW bridge weights: {kw_weights}")
print(f"  KW weight distribution: {dict(Counter(kw_weights))}")

# For each variant (kw, flip_L, flip_R, flip_LR), compute the weight distribution
for vi, label in enumerate(ORI_LABELS):
    weights = [bd['variants'][vi]['hamming'] for bd in bridge_data]
    wdist = Counter(weights)
    has_5 = 5 in wdist
    print(f"  {label:>8s}: {dict(sorted(wdist.items()))} {'★ has weight-5!' if has_5 else ''}")


print()
print("=" * 80)
print("BRIDGE ORIENTATION ANALYSIS COMPLETE")
print("=" * 80)
