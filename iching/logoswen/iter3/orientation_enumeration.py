"""
Thread C — Part 2: Enumerate S=2-free orientations.

Given KW's pairs and pair ordering, how many of the 2^32 possible
orientations (choice of which hexagram is first in each pair) produce
an S=2-free bridge sequence?

From bridge_orientation.py we know:
- Only 5 bridges can produce S=2 under some orientation
- Each constrains a pair of consecutive orientation bits
- Constraints are LOCAL (each involves exactly 2 adjacent pairs)

This script:
1. Enumerates the exact constraint structure
2. Computes the number of S=2-free orientations exactly
3. Computes the fraction of 2^32 that are S=2-free
4. For S=2-free orientations: characterizes kernel chain diversity
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import time

DIMS = 6
M = [tuple(b) for b in all_bits()]

# ── Data (reproduce from bridge_orientation.py) ──────────────────────────────

PAIRS = []
for k in range(32):
    a = M[2 * k]
    b = M[2 * k + 1]
    mask = tuple(a[i] ^ b[i] for i in range(DIMS))
    PAIRS.append({'a': a, 'b': b, 'mask': mask})

VALID_MASKS = {
    (0,0,0,0,0,0): 'id',  (1,0,0,0,0,1): 'O',  (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',   (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',  (1,1,1,1,1,1): 'OMI',
}


def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def xor6(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def compute_S(hex_a, hex_b):
    m = xor6(hex_a, hex_b)
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])

def kernel_name(hex_a, hex_b):
    """
    Kernel dressing: the symmetric (position) component of the bridge mask.
    For mask m, kernel 3-bit code = (m[5], m[4], m[3]) — the upper half.
    This represents the Z₂³ element acting on position coordinates.
    """
    m = xor6(hex_a, hex_b)
    k = (m[5], m[4], m[3])
    gen_6 = (k[0], k[1], k[2], k[2], k[1], k[0])
    return VALID_MASKS.get(gen_6, '?')


# ═══════════════════════════════════════════════════════════════════════════════
# 1. EXACT CONSTRAINT STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

# For each bridge k: orientation (o_k, o_{k+1}) determines the exit/entry hexagrams
# o_i = 0: KW orientation (pair[i].a first, pair[i].b second)
# o_i = 1: flipped (pair[i].b first, pair[i].a second)
# Bridge exit = pair[k].b if o_k=0, pair[k].a if o_k=1
# Bridge entry = pair[k+1].a if o_{k+1}=0, pair[k+1].b if o_{k+1}=1

def bridge_S(k, o_k, o_k1):
    """Compute S for bridge k given orientation bits o_k and o_{k+1}."""
    exit_hex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
    entry_hex = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
    return compute_S(exit_hex, entry_hex)


def bridge_kernel(k, o_k, o_k1):
    """Compute kernel dressing name for bridge k given orientations."""
    exit_hex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
    entry_hex = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
    return kernel_name(exit_hex, entry_hex)


def bridge_hamming(k, o_k, o_k1):
    """Compute Hamming distance for bridge k given orientations."""
    exit_hex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
    entry_hex = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
    return sum(xor6(exit_hex, entry_hex))


# Find all S=2-producing (bridge, orientation) combinations
print("=" * 80)
print("1. EXACT S=2 CONSTRAINT ENUMERATION")
print("=" * 80)
print()

constraints = {}  # bridge_idx -> set of forbidden (o_k, o_{k+1}) pairs
for k in range(31):
    forbidden = set()
    for o_k in [0, 1]:
        for o_k1 in [0, 1]:
            if bridge_S(k, o_k, o_k1) == 2:
                forbidden.add((o_k, o_k1))
    if forbidden:
        constraints[k] = forbidden
        print(f"  Bridge {k:2d}: forbidden (o_{k}, o_{k+1}) = {sorted(forbidden)}")

print(f"\n  Constrained bridges: {len(constraints)}")
print(f"  Unconstrained bridges: {31 - len(constraints)}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CONSTRAINT GRAPH: INDEPENDENT COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("2. CONSTRAINT GRAPH: INDEPENDENT COMPONENTS")
print("=" * 80)
print()

# The constraints form a graph on pair indices (0..31).
# Bridge k constrains (pair k, pair k+1).
# Connected components of this graph can be analyzed independently.

# Build adjacency
adj = defaultdict(set)
constrained_pairs = set()
for k, forbidden in constraints.items():
    adj[k].add(k + 1)
    adj[k + 1].add(k)
    constrained_pairs.add(k)
    constrained_pairs.add(k + 1)

# Find connected components among constrained pairs
visited = set()
components = []
for start in sorted(constrained_pairs):
    if start in visited:
        continue
    component = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        component.append(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    components.append(sorted(component))

print(f"  Constrained pairs: {sorted(constrained_pairs)}")
print(f"  Number of connected components: {len(components)}")
for i, comp in enumerate(components):
    bridges_in = [k for k in constraints if k in comp or k+1 in comp]
    print(f"    Component {i+1}: pairs {comp}, bridges {bridges_in}")

# Unconstrained pairs
free_pairs = set(range(32)) - constrained_pairs
print(f"\n  Unconstrained pairs: {sorted(free_pairs)} ({len(free_pairs)} pairs)")
print(f"  Free bits from unconstrained pairs: 2^{len(free_pairs)} = {2**len(free_pairs)}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. EXACT COUNT: S=2-FREE ORIENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("3. EXACT COUNT OF S=2-FREE ORIENTATIONS")
print("=" * 80)
print()

# For each connected component, enumerate all valid orientation assignments
# of the pairs in that component. Then multiply across components and free pairs.

def count_valid_for_component(comp_pairs, comp_constraints):
    """
    Count valid orientation assignments for pairs in a connected component.
    comp_pairs: sorted list of pair indices
    comp_constraints: dict of bridge_idx -> forbidden set
    """
    n = len(comp_pairs)
    pair_to_local = {p: i for i, p in enumerate(comp_pairs)}
    
    count = 0
    for bits in range(2**n):
        orientation = {}
        for i, p in enumerate(comp_pairs):
            orientation[p] = (bits >> i) & 1
        
        valid = True
        for k, forbidden in comp_constraints.items():
            if k in orientation and k+1 in orientation:
                if (orientation[k], orientation[k+1]) in forbidden:
                    valid = False
                    break
        
        if valid:
            count += 1
    
    return count


total_valid = 1
component_counts = []

for i, comp in enumerate(components):
    # Get constraints involving this component
    comp_constraints = {}
    for k, forbidden in constraints.items():
        if k in comp or k+1 in comp:
            comp_constraints[k] = forbidden
    
    valid = count_valid_for_component(comp, comp_constraints)
    total_valid *= valid
    component_counts.append(valid)
    
    total_possible = 2**len(comp)
    print(f"  Component {i+1} (pairs {comp}): "
          f"{valid}/{total_possible} valid ({100*valid/total_possible:.1f}%)")

# Free pairs contribute 2^|free| each
free_contribution = 2 ** len(free_pairs)
total_valid *= free_contribution

print(f"\n  Free pairs: 2^{len(free_pairs)} = {free_contribution}")
print(f"  Total S=2-free orientations: {total_valid}")
print(f"  Total possible orientations: {2**32}")
print(f"  Fraction S=2-free: {total_valid / 2**32:.6f} ({total_valid / 2**32 * 100:.4f}%)")
print(f"  Bits constrained: {32 - (32 - len(constrained_pairs))} pair bits involved")
print(f"  Effective constraint: eliminates {1 - total_valid / 2**32:.6f} of orientation space")

# How many bits of freedom remain?
import math
effective_bits = math.log2(total_valid)
print(f"\n  Effective degrees of freedom: 2^{effective_bits:.2f}")
print(f"  Bits lost to S=2 constraint: {32 - effective_bits:.2f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DETAILED CONSTRAINT ANALYSIS: WHICH PATTERNS ARE FORBIDDEN?
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("4. CONSTRAINT PATTERN ANALYSIS")
print("=" * 80)
print()

# For each constrained bridge, what is the constraint pattern?
for k, forbidden in sorted(constraints.items()):
    allowed = [(o_k, o_k1) for o_k in [0, 1] for o_k1 in [0, 1]
               if (o_k, o_k1) not in forbidden]
    
    # Interpret the constraint
    if forbidden == {(1, 0), (0, 1)}:
        constraint_type = "o_k ≠ o_{k+1} forbidden → must be EQUAL"
    elif forbidden == {(0, 0), (1, 1)}:
        constraint_type = "o_k = o_{k+1} forbidden → must be DIFFERENT"
    elif forbidden == {(0, 1), (1, 1)}:
        constraint_type = "o_{k+1} = 1 when o_k ∈ {0,1} → o_{k+1} must be 0"
        # Check: is it simply o_{k+1} = 0?
        if all(o_k1 == 0 for _, o_k1 in allowed):
            constraint_type = "o_{k+1} MUST be 0"
        elif all(o_k == 0 for o_k, _ in allowed):
            constraint_type = "o_k MUST be 0"
        else:
            constraint_type = f"allowed: {allowed}"
    else:
        constraint_type = f"allowed: {allowed}"
    
    print(f"  Bridge {k:2d}: forbidden={sorted(forbidden)}, "
          f"allowed={sorted(allowed)}")
    print(f"            → {constraint_type}")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SAMPLE S=2-FREE ORIENTATIONS: KERNEL CHAIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("5. KERNEL CHAIN PROPERTIES ACROSS S=2-FREE ORIENTATIONS")
print("=" * 80)
print()

N_SAMPLES = 100_000
rng = random.Random(42)

# Efficient sampling: pick random orientation, reject if S=2
# Since ~25% are valid (from the exact count), rejection is efficient


def random_s2_free_orientation(rng):
    """Sample a uniformly random S=2-free orientation."""
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> i) & 1 for i in range(32)]
        
        valid = True
        for k, forbidden in constraints.items():
            if (o[k], o[k+1]) in forbidden:
                valid = False
                break
        
        if valid:
            return o


def compute_kernel_chain(orientation):
    """Compute the 31-element kernel chain for a given orientation."""
    chain = []
    for k in range(31):
        chain.append(bridge_kernel(k, orientation[k], orientation[k+1]))
    return chain


def kernel_chain_stats(chain):
    """Compute statistics of a kernel chain."""
    freq = Counter(chain)
    
    # Chi-squared for uniformity (8 generators)
    expected = len(chain) / 8
    chi2 = sum((freq.get(g, 0) - expected) ** 2 / expected
               for g in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI'])
    
    # OMI consecutive XOR count
    omi_count = 0
    for i in range(len(chain) - 1):
        # XOR in generator space: the "difference" between consecutive kernels
        # Two generators g1, g2 have XOR = g1 ⊕ g2
        # OMI XOR means g1 ⊕ g2 = OMI, i.e., they differ in all 3 components
        # Simple approach: compare 3-bit representations
        pass
    
    return {
        'freq': dict(freq),
        'chi2': chi2,
        'n_generators_used': len(freq),
    }


# KW kernel chain baseline
kw_orientation = [0] * 32  # 0 = KW orientation for all pairs
kw_chain = compute_kernel_chain(kw_orientation)
kw_stats = kernel_chain_stats(kw_chain)

print(f"  KW kernel chain: {' '.join(kw_chain)}")
print(f"  KW frequency: {kw_stats['freq']}")
print(f"  KW chi² (uniformity): {kw_stats['chi2']:.2f}")
print(f"  KW generators used: {kw_stats['n_generators_used']}/8")
print()

# Sample S=2-free orientations
print(f"  Sampling {N_SAMPLES} S=2-free orientations...")
t0 = time.time()

chi2_values = []
n_gens_values = []
freq_accum = Counter()
acceptance_count = 0
total_tried = 0

for i in range(N_SAMPLES):
    while True:
        total_tried += 1
        bits = rng.getrandbits(32)
        o = [(bits >> i) & 1 for i in range(32)]
        
        valid = True
        for k, forbidden in constraints.items():
            if (o[k], o[k+1]) in forbidden:
                valid = False
                break
        if valid:
            break
    
    chain = compute_kernel_chain(o)
    stats = kernel_chain_stats(chain)
    chi2_values.append(stats['chi2'])
    n_gens_values.append(stats['n_generators_used'])
    for g, c in stats['freq'].items():
        freq_accum[g] += c

t1 = time.time()
acceptance_rate = N_SAMPLES / total_tried
print(f"  Done in {t1-t0:.1f}s. Acceptance rate: {acceptance_rate:.4f}")
print()

# Summary statistics
import numpy as np

chi2_arr = np.array(chi2_values)
n_gens_arr = np.array(n_gens_values)

print(f"  Kernel chi² (uniformity):")
print(f"    KW: {kw_stats['chi2']:.2f}")
print(f"    Random S=2-free: mean={chi2_arr.mean():.2f}, std={chi2_arr.std():.2f}")
print(f"    P(chi² ≤ KW): {np.mean(chi2_arr <= kw_stats['chi2']):.4f}")
print()

print(f"  Number of distinct generators used:")
print(f"    KW: {kw_stats['n_generators_used']}")
print(f"    Random S=2-free: mean={n_gens_arr.mean():.2f}")
print(f"    Distribution: {dict(Counter(n_gens_values))}")
print()

# Mean frequency per generator
total_bridges = N_SAMPLES * 31
print(f"  Mean kernel frequency across S=2-free orientations:")
for g in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    mean_frac = freq_accum.get(g, 0) / total_bridges
    kw_frac = Counter(kw_chain).get(g, 0) / 31
    print(f"    {g:>4s}: random={mean_frac:.4f}  KW={kw_frac:.4f}")

print()

# Check: does KW orientation match any special property?
# Count how many S=2-free orientations match KW exactly
kw_bits = 0  # all zeros = KW orientation
kw_match_count = 0
n_check = min(N_SAMPLES, 10000)
print(f"  Checking kernel chi² distribution (lower = more uniform):")
pctiles = np.percentile(chi2_arr, [1, 5, 10, 25, 50, 75, 90, 95, 99])
for p, v in zip([1, 5, 10, 25, 50, 75, 90, 95, 99], pctiles):
    marker = " ← KW" if abs(v - kw_stats['chi2']) < 0.5 else ""
    print(f"    {p:3d}th percentile: {v:.2f}{marker}")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. WEIGHT-5 BRIDGE ANALYSIS ACROSS ORIENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("6. WEIGHT-5 BRIDGE ABSENCE ACROSS ORIENTATIONS")
print("=" * 80)
print()

# Check: of the S=2-free orientations, how many also avoid weight-5 bridges?
# (Weight-5 ↔ S=2 for single-component orbit changes, but let's verify)

n_check_w5 = 50_000
w5_free_count = 0
s2_free_count = 0

for _ in range(n_check_w5):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> i) & 1 for i in range(32)]
        valid = True
        for k, forbidden in constraints.items():
            if (o[k], o[k+1]) in forbidden:
                valid = False
                break
        if valid:
            break
    
    s2_free_count += 1
    has_w5 = False
    for k in range(31):
        h = bridge_hamming(k, o[k], o[k+1])
        if h == 5:
            has_w5 = True
            break
    
    if not has_w5:
        w5_free_count += 1

print(f"  Among {n_check_w5} S=2-free orientations:")
print(f"    Weight-5-free: {w5_free_count} ({100*w5_free_count/n_check_w5:.2f}%)")
print(f"    Has weight-5: {n_check_w5 - w5_free_count} ({100*(1-w5_free_count/n_check_w5):.2f}%)")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. VERIFY: S=2 AND WEIGHT-5 EQUIVALENCE
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("7. VERIFY: S=2 ↔ WEIGHT-5 ACROSS ALL ORIENTATIONS")
print("=" * 80)
print()

# For each bridge, check all 4 orientations
s2_not_w5 = 0
w5_not_s2 = 0
both = 0
neither = 0

for k in range(31):
    for o_k in [0, 1]:
        for o_k1 in [0, 1]:
            s = bridge_S(k, o_k, o_k1)
            h = bridge_hamming(k, o_k, o_k1)
            has_s2 = (s == 2)
            has_w5 = (h == 5)
            if has_s2 and has_w5:
                both += 1
            elif has_s2 and not has_w5:
                s2_not_w5 += 1
            elif has_w5 and not has_s2:
                w5_not_s2 += 1
            else:
                neither += 1

print(f"  Across all 31 bridges × 4 orientations = {31*4} cases:")
print(f"    S=2 AND weight-5: {both}")
print(f"    S=2 but NOT weight-5: {s2_not_w5}")
print(f"    weight-5 but NOT S=2: {w5_not_s2}")
print(f"    neither: {neither}")

if s2_not_w5 == 0 and w5_not_s2 == 0:
    print(f"  ✓ S=2 ↔ weight-5 is a perfect equivalence across all orientation variants!")
elif w5_not_s2 == 0:
    print(f"  S=2 → weight-5 always, but weight-5 → S=2 not always")
else:
    print(f"  S=2 and weight-5 are NOT equivalent across orientations")


print()
print("=" * 80)
print("ORIENTATION ENUMERATION COMPLETE")
print("=" * 80)
