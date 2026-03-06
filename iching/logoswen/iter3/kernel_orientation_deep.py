"""
Thread C — Part 3: Deep kernel chain analysis for S=2-free orientations.

Extends the enumeration analysis with:
1. Consecutive kernel XOR (OMI dominance) across S=2-free orientations
2. Joint chi² + OMI-XOR statistics
3. Structural analysis of how orientation changes propagate through kernel chain
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import time
import numpy as np

DIMS = 6
M = [tuple(b) for b in all_bits()]

PAIRS = []
for k in range(32):
    a = M[2 * k]
    b = M[2 * k + 1]
    PAIRS.append({'a': a, 'b': b})

VALID_MASKS = {
    (0,0,0,0,0,0): 'id',  (1,0,0,0,0,1): 'O',  (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',   (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',  (1,1,1,1,1,1): 'OMI',
}

# Reverse lookup: name -> 3-bit tuple
GEN_3BIT = {
    'id': (0,0,0), 'O': (1,0,0), 'M': (0,1,0), 'I': (0,0,1),
    'OM': (1,1,0), 'OI': (1,0,1), 'MI': (0,1,1), 'OMI': (1,1,1),
}

def xor6(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def compute_S(hex_a, hex_b):
    m = xor6(hex_a, hex_b)
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])

def kernel_3bit(hex_a, hex_b):
    """Kernel as 3-bit tuple: (m[5], m[4], m[3])."""
    m = xor6(hex_a, hex_b)
    return (m[5], m[4], m[3])

def kernel_name_from_3bit(k3):
    gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
    return VALID_MASKS.get(gen_6, '?')

# S=2 constraints (from bridge_orientation.py results)
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
    """Check if orientation (list of 32 bits) is S=2-free."""
    for k, forbidden in CONSTRAINTS.items():
        if (orientation[k], orientation[k+1]) in forbidden:
            return False
    return True


def compute_full_stats(orientation):
    """Compute kernel chain statistics for an orientation."""
    chain_3bit = []
    chain_names = []
    for k in range(31):
        exit_hex = PAIRS[k]['b'] if orientation[k] == 0 else PAIRS[k]['a']
        entry_hex = PAIRS[k+1]['a'] if orientation[k+1] == 0 else PAIRS[k+1]['b']
        k3 = kernel_3bit(exit_hex, entry_hex)
        chain_3bit.append(k3)
        chain_names.append(kernel_name_from_3bit(k3))
    
    freq = Counter(chain_names)
    
    # Chi-squared for uniformity
    expected = 31 / 8
    chi2 = sum((freq.get(g, 0) - expected) ** 2 / expected
               for g in VALID_MASKS.values())
    
    # OMI XOR count: consecutive kernel pairs that XOR to OMI
    omi_count = 0
    xor_weights = []
    for i in range(30):
        xor_3 = tuple(chain_3bit[i][j] ^ chain_3bit[i+1][j] for j in range(3))
        w = sum(xor_3)
        xor_weights.append(w)
        if xor_3 == (1, 1, 1):
            omi_count += 1
    
    omi_frac = omi_count / 30
    mean_xor_weight = sum(xor_weights) / 30 if xor_weights else 0
    
    return {
        'chi2': chi2,
        'omi_count': omi_count,
        'omi_frac': omi_frac,
        'mean_xor_weight': mean_xor_weight,
        'n_generators': len(freq),
        'freq': dict(freq),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 1. KW BASELINE
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("1. KW BASELINE KERNEL CHAIN STATISTICS")
print("=" * 80)
print()

kw_stats = compute_full_stats([0] * 32)
print(f"  chi² = {kw_stats['chi2']:.2f}")
print(f"  OMI-XOR count = {kw_stats['omi_count']}/30 ({kw_stats['omi_frac']:.3f})")
print(f"  Mean XOR weight = {kw_stats['mean_xor_weight']:.3f}")
print(f"  Generators used = {kw_stats['n_generators']}/8")
print(f"  Frequency: {kw_stats['freq']}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. SAMPLE S=2-FREE ORIENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("2. JOINT STATISTICS ACROSS S=2-FREE ORIENTATIONS (100K samples)")
print("=" * 80)
print()

N_SAMPLES = 100_000
rng = random.Random(42)

chi2_vals = []
omi_counts = []
omi_fracs = []
xor_weights = []
n_gens_vals = []

t0 = time.time()
total_tried = 0

for i in range(N_SAMPLES):
    while True:
        total_tried += 1
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    stats = compute_full_stats(o)
    chi2_vals.append(stats['chi2'])
    omi_counts.append(stats['omi_count'])
    omi_fracs.append(stats['omi_frac'])
    xor_weights.append(stats['mean_xor_weight'])
    n_gens_vals.append(stats['n_generators'])

t1 = time.time()
print(f"  Sampled {N_SAMPLES} S=2-free orientations in {t1-t0:.1f}s")
print(f"  Acceptance rate: {N_SAMPLES/total_tried:.4f}")
print()

chi2_arr = np.array(chi2_vals)
omi_arr = np.array(omi_fracs)
xw_arr = np.array(xor_weights)

# Summary
print(f"  {'Metric':>20s}  {'KW':>8s}  {'Mean':>8s}  {'Std':>8s}  {'p-value':>8s}")
print(f"  {'-'*60}")

p_chi2 = np.mean(chi2_arr <= kw_stats['chi2'])
p_omi = np.mean(omi_arr >= kw_stats['omi_frac'])
p_xw = np.mean(xw_arr >= kw_stats['mean_xor_weight'])

print(f"  {'chi² (uniformity)':>20s}  {kw_stats['chi2']:8.2f}  {chi2_arr.mean():8.2f}  "
      f"{chi2_arr.std():8.2f}  {p_chi2:8.4f}")
print(f"  {'OMI-XOR fraction':>20s}  {kw_stats['omi_frac']:8.3f}  {omi_arr.mean():8.3f}  "
      f"{omi_arr.std():8.3f}  {p_omi:8.4f}")
print(f"  {'Mean XOR weight':>20s}  {kw_stats['mean_xor_weight']:8.3f}  {xw_arr.mean():8.3f}  "
      f"{xw_arr.std():8.3f}  {p_xw:8.4f}")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. INDEPENDENCE: chi² vs OMI-XOR (conditional on S=2-free)
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("3. INDEPENDENCE: chi² vs OMI-XOR (among S=2-free orientations)")
print("=" * 80)
print()

corr = np.corrcoef(chi2_arr, omi_arr)[0, 1]
print(f"  Correlation r(chi², OMI-frac) = {corr:.4f}")

# Joint probability
joint_count = np.sum((chi2_arr <= kw_stats['chi2']) & (omi_arr >= kw_stats['omi_frac']))
joint_p = joint_count / N_SAMPLES
expected_joint = p_chi2 * p_omi
print(f"  P(chi² ≤ KW AND OMI ≥ KW) = {joint_p:.5f} ({joint_count}/{N_SAMPLES})")
print(f"  If independent: {expected_joint:.5f}")
print(f"  Ratio: {joint_p / expected_joint:.3f}" if expected_joint > 0 else "  Expected: 0")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. HOW MANY BRIDGES CHANGE KERNEL WHEN ORIENTATION FLIPS?
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("4. KERNEL SENSITIVITY TO SINGLE-PAIR ORIENTATION FLIPS")
print("=" * 80)
print()

# For each pair, how many bridges change kernel if we flip just that pair?
for p in range(32):
    kw_o = [0] * 32
    flip_o = [0] * 32
    flip_o[p] = 1
    
    # Check S=2 safety
    if not is_s2_free(flip_o):
        print(f"  Pair {p:2d}: flip violates S=2 — skip")
        continue
    
    kw_chain = []
    flip_chain = []
    for k in range(31):
        exit_kw = PAIRS[k]['b'] if kw_o[k] == 0 else PAIRS[k]['a']
        entry_kw = PAIRS[k+1]['a'] if kw_o[k+1] == 0 else PAIRS[k+1]['b']
        exit_fl = PAIRS[k]['b'] if flip_o[k] == 0 else PAIRS[k]['a']
        entry_fl = PAIRS[k+1]['a'] if flip_o[k+1] == 0 else PAIRS[k+1]['b']
        kw_chain.append(kernel_name_from_3bit(kernel_3bit(exit_kw, entry_kw)))
        flip_chain.append(kernel_name_from_3bit(kernel_3bit(exit_fl, entry_fl)))
    
    changed = sum(1 for i in range(31) if kw_chain[i] != flip_chain[i])
    
    # Which bridges changed?
    changed_bridges = [i for i in range(31) if kw_chain[i] != flip_chain[i]]
    
    stats = compute_full_stats(flip_o)
    print(f"  Pair {p:2d}: {changed} bridges change kernel. "
          f"Bridges: {changed_bridges if changed_bridges else 'none'}"
          f"  chi²={stats['chi2']:.2f}  OMI-XOR={stats['omi_count']}/30")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. WHICH ORIENTATION BITS AFFECT WHICH BRIDGES?
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("5. ORIENTATION-BRIDGE DEPENDENCY STRUCTURE")
print("=" * 80)
print()

# Each bridge k depends on exactly 2 orientation bits: o_k and o_{k+1}
# But the kernel at bridge k depends on the actual hexagrams at the exit/entry,
# which are determined by o_k and o_{k+1} respectively.
#
# Flipping pair p changes:
#   - Bridge p-1 (if p > 0): exit hexagram changes
#   - Bridge p (if p < 31): entry hexagram changes
#
# So each pair's orientation affects exactly 1 or 2 bridges.

print("  Pair → affected bridges mapping:")
for p in range(32):
    affected = []
    if p > 0:
        affected.append(p - 1)
    if p < 31:
        affected.append(p)
    print(f"    Pair {p:2d} → bridges {affected}")

# How many independent kernel "control points" are there?
# Each bridge k has kernel = f(o_k, o_{k+1})
# The kernel chain has 31 elements, controlled by 32 orientation bits
# But adjacent bridges share a bit: bridge k and k+1 both depend on o_{k+1}
print()
print("  Each bridge depends on exactly 2 consecutive orientation bits.")
print("  Adjacent bridges share one orientation bit.")
print("  The 31-bridge kernel chain is a Markov-like chain controlled by 32 bits.")
print()

# For each bridge, how many distinct kernels are possible?
for k in range(31):
    kernels = set()
    for o_k in [0, 1]:
        for o_k1 in [0, 1]:
            exit_hex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
            entry_hex = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
            kn = kernel_name_from_3bit(kernel_3bit(exit_hex, entry_hex))
            kernels.add(kn)
    if len(kernels) < 4:
        print(f"  Bridge {k:2d}: {len(kernels)} distinct kernels (out of 4 orientations)")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. COMPARISON: CONDITIONAL ON S=2-FREE vs UNCONDITIONAL
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("6. COMPARISON: S=2-FREE vs ALL ORIENTATIONS")
print("=" * 80)
print()

# Sample from ALL orientations (including S=2-producing ones)
N_ALL = 100_000
rng2 = random.Random(123)

chi2_all = []
omi_all = []

for i in range(N_ALL):
    bits = rng2.getrandbits(32)
    o = [(bits >> j) & 1 for j in range(32)]
    stats = compute_full_stats(o)
    chi2_all.append(stats['chi2'])
    omi_all.append(stats['omi_frac'])

chi2_all_arr = np.array(chi2_all)
omi_all_arr = np.array(omi_all)

print(f"  {'Metric':>20s}  {'S=2-free mean':>14s}  {'All mean':>14s}  {'Diff':>8s}")
print(f"  {'-'*60}")
print(f"  {'chi² (uniformity)':>20s}  {chi2_arr.mean():14.2f}  {chi2_all_arr.mean():14.2f}  "
      f"{chi2_arr.mean() - chi2_all_arr.mean():+8.2f}")
print(f"  {'OMI-XOR fraction':>20s}  {omi_arr.mean():14.4f}  {omi_all_arr.mean():14.4f}  "
      f"{omi_arr.mean() - omi_all_arr.mean():+8.4f}")

# KW p-values under both null models
p_chi2_all = np.mean(chi2_all_arr <= kw_stats['chi2'])
p_omi_all = np.mean(omi_all_arr >= kw_stats['omi_frac'])

print(f"\n  KW p-values:")
print(f"    P(chi² ≤ KW) | S=2-free: {p_chi2:.4f}  | All: {p_chi2_all:.4f}")
print(f"    P(OMI ≥ KW)  | S=2-free: {p_omi:.4f}  | All: {p_omi_all:.4f}")


print()
print("=" * 80)
print("DEEP KERNEL ORIENTATION ANALYSIS COMPLETE")
print("=" * 80)
