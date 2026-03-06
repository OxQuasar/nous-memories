"""
Compute Hamming distances between consecutive 6-bit bridge kernel masks
in the King Wen sequence.

Bridge k connects exit hexagram of pair k to entry hexagram of pair k+1.
The full XOR mask decomposes into kernel (palindromic part) + orbit delta.
We compute distances between consecutive full bridge masks and between
consecutive kernel dressings.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
from sequence import KING_WEN

import numpy as np
from collections import Counter

# Extract binary representations
M = [h[2] for h in KING_WEN]

# 32 pairs: (hex[0],hex[1]), (hex[2],hex[3]), ...
pairs = [(M[2*k], M[2*k+1]) for k in range(32)]

def xor(a, b):
    return tuple(int(a[i]) ^ int(b[i]) for i in range(6))

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

def kernel_dressing(mask):
    """Palindromic part: (m5, m4, m3, m3, m4, m5)"""
    return (mask[5], mask[4], mask[3], mask[3], mask[4], mask[5])

def orbit_delta(mask):
    """Anti-symmetric part: (m0^m5, m1^m4, m2^m3)"""
    return (mask[0]^mask[5], mask[1]^mask[4], mask[2]^mask[3])

KERNEL_NAMES = {
    (0,0,0,0,0,0): "id",
    (1,0,0,0,0,1): "O",
    (0,1,0,0,1,0): "M",
    (0,0,1,1,0,0): "I",
    (1,1,0,0,1,1): "OM",
    (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI",
    (1,1,1,1,1,1): "OMI",
}

# Compute 31 bridges
bridges = []
for k in range(31):
    exit_hex = M[2*k + 1]       # second hex of pair k
    entry_hex = M[2*(k+1)]      # first hex of pair k+1
    mask = xor(exit_hex, entry_hex)
    kern = kernel_dressing(mask)
    orb = orbit_delta(mask)
    bridges.append({
        'k': k,
        'exit': exit_hex,
        'entry': entry_hex,
        'mask': mask,
        'kernel': kern,
        'orbit_delta': orb,
        'kernel_name': KERNEL_NAMES.get(kern, '?'),
        'exit_name': KING_WEN[2*k+1][1],
        'entry_name': KING_WEN[2*(k+1)][1],
    })

# Print bridge table
print("=" * 90)
print("BRIDGE TABLE")
print("=" * 90)
print(f"{'B#':>3} {'Exit':>12} → {'Entry':<12} {'Mask':>8} {'Kernel':>8} {'KName':>5} {'OrbΔ':>5} {'Hdist':>5}")
print("-" * 90)
for b in bridges:
    mask_str = ''.join(str(x) for x in b['mask'])
    kern_str = ''.join(str(x) for x in b['kernel'])
    orb_str = ''.join(str(x) for x in b['orbit_delta'])
    hdist = sum(b['mask'])
    print(f"{b['k']+1:>3} {b['exit_name']:>12} → {b['entry_name']:<12} {mask_str:>8} {kern_str:>8} {b['kernel_name']:>5} {orb_str:>5} {hdist:>5}")

# Consecutive bridge mask Hamming distances
print("\n" + "=" * 90)
print("CONSECUTIVE BRIDGE DISTANCES (full 6-bit mask)")
print("=" * 90)

mask_dists = []
for i in range(30):
    d = hamming(bridges[i]['mask'], bridges[i+1]['mask'])
    mask_dists.append(d)
    print(f"  B{i+1:>2} → B{i+2:>2}: {d}  "
          f"({''.join(str(x) for x in bridges[i]['mask'])} → "
          f"{''.join(str(x) for x in bridges[i+1]['mask'])})")

print(f"\n  Mean: {np.mean(mask_dists):.3f}")
print(f"  Std:  {np.std(mask_dists):.3f}")
print(f"  Min:  {min(mask_dists)}, Max: {max(mask_dists)}")
print(f"  Distribution: {dict(sorted(Counter(mask_dists).items()))}")

# Consecutive kernel dressing Hamming distances
print("\n" + "=" * 90)
print("CONSECUTIVE KERNEL DISTANCES (palindromic dressing)")
print("=" * 90)

kern_dists = []
for i in range(30):
    d = hamming(bridges[i]['kernel'], bridges[i+1]['kernel'])
    kern_dists.append(d)
    print(f"  B{i+1:>2} → B{i+2:>2}: {d}  "
          f"{bridges[i]['kernel_name']:>5} → {bridges[i+1]['kernel_name']:<5}")

print(f"\n  Mean: {np.mean(kern_dists):.3f}")
print(f"  Std:  {np.std(kern_dists):.3f}")
print(f"  Min:  {min(kern_dists)}, Max: {max(kern_dists)}")
print(f"  Distribution: {dict(sorted(Counter(kern_dists).items()))}")

# Consecutive orbit delta distances
print("\n" + "=" * 90)
print("CONSECUTIVE ORBIT DELTA DISTANCES (3-bit)")
print("=" * 90)

orb_dists = []
for i in range(30):
    d = hamming(bridges[i]['orbit_delta'], bridges[i+1]['orbit_delta'])
    orb_dists.append(d)

print(f"  Mean: {np.mean(orb_dists):.3f}")
print(f"  Std:  {np.std(orb_dists):.3f}")
print(f"  Distribution: {dict(sorted(Counter(orb_dists).items()))}")

# Now compare to random: shuffle pair order, recompute
print("\n" + "=" * 90)
print("RANDOM BASELINE (10,000 shuffles of pair order, same pairs)")
print("=" * 90)

rng = np.random.default_rng(42)
n_trials = 10000

rand_mask_means = []
rand_kern_means = []

for _ in range(n_trials):
    # Shuffle pair order (keep pair contents fixed, shuffle which pair comes where)
    perm = rng.permutation(32)
    shuffled_pairs = [pairs[p] for p in perm]
    
    # Compute bridges for shuffled sequence
    rand_bridges = []
    for k in range(31):
        exit_hex = shuffled_pairs[k][1]   # second hex of pair k
        entry_hex = shuffled_pairs[k+1][0]  # first hex of pair k+1
        mask = xor(exit_hex, entry_hex)
        kern = kernel_dressing(mask)
        rand_bridges.append({'mask': mask, 'kernel': kern})
    
    # Consecutive distances
    md = [hamming(rand_bridges[i]['mask'], rand_bridges[i+1]['mask']) 
          for i in range(30)]
    kd = [hamming(rand_bridges[i]['kernel'], rand_bridges[i+1]['kernel']) 
          for i in range(30)]
    
    rand_mask_means.append(np.mean(md))
    rand_kern_means.append(np.mean(kd))

kw_mask_mean = np.mean(mask_dists)
kw_kern_mean = np.mean(kern_dists)

mask_pctile = np.mean(np.array(rand_mask_means) <= kw_mask_mean) * 100
kern_pctile = np.mean(np.array(rand_kern_means) <= kw_kern_mean) * 100

print(f"  Full mask consecutive distance:")
print(f"    KW mean:     {kw_mask_mean:.3f}")
print(f"    Random mean: {np.mean(rand_mask_means):.3f} ± {np.std(rand_mask_means):.3f}")
print(f"    KW percentile: {mask_pctile:.1f}%")

print(f"\n  Kernel dressing consecutive distance:")
print(f"    KW mean:     {kw_kern_mean:.3f}")
print(f"    Random mean: {np.mean(rand_kern_means):.3f} ± {np.std(rand_kern_means):.3f}")
print(f"    KW percentile: {kern_pctile:.1f}%")

# Also check: does KW maximize consecutive kernel distance?
# (anti-repetition = high distance between consecutive kernels)
mask_pctile_high = np.mean(np.array(rand_mask_means) >= kw_mask_mean) * 100
kern_pctile_high = np.mean(np.array(rand_kern_means) >= kw_kern_mean) * 100
print(f"\n  KW at HIGH end (maximizes consecutive distance?):")
print(f"    Full mask: {100-mask_pctile:.1f}th percentile from top")
print(f"    Kernel:    {100-kern_pctile:.1f}th percentile from top")
