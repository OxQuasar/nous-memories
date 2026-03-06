"""
Thread C Extended — Valid Orientation Subspace Analysis

Round 1 found: S=2 avoidance constrains 5 bits of 32, leaving 2^27 valid orientations.
This is a LOOSE constraint. This script characterizes what ELSE distinguishes KW's
orientation among S=2-free ones.

1. Enumerate the valid orientation subspace structure
2. Properties that distinguish KW's orientation among S=2-free alternatives
3. Kernel chain properties across sampled valid orientations (uniformity, OMI contrast)
4. Trigram-level discriminants across valid orientations
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits, TRIGRAMS
import random
import numpy as np
import math

DIMS = 6
N_PAIRS = 32
M = [tuple(b) for b in all_bits()]

TRIGRAM_NAMES = {
    (1,1,1): 'Heaven', (0,0,0): 'Earth',
    (0,1,0): 'Water',  (1,0,1): 'Fire',
    (1,0,0): 'Thunder',(0,1,1): 'Wind',
    (0,0,1): 'Mountain',(1,1,0): 'Lake',
}

VALID_MASKS = {
    (0,0,0,0,0,0): 'id',  (1,0,0,0,0,1): 'O',  (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',   (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',  (1,1,1,1,1,1): 'OMI',
}

GEN_3BIT = {
    'id': (0,0,0), 'O': (1,0,0), 'M': (0,1,0), 'I': (0,0,1),
    'OM': (1,1,0), 'OI': (1,0,1), 'MI': (0,1,1), 'OMI': (1,1,1),
}

# ── Build pairs ───────────────────────────────────────────────────────────────

PAIRS = []
for k in range(N_PAIRS):
    a = M[2*k]
    b = M[2*k+1]
    PAIRS.append({'a': a, 'b': b})


def xor6(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def compute_S(hex_a, hex_b):
    m = xor6(hex_a, hex_b)
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])

def kernel_3bit(hex_a, hex_b):
    m = xor6(hex_a, hex_b)
    return (m[5], m[4], m[3])

def kernel_name_from_3bit(k3):
    gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
    return VALID_MASKS.get(gen_6, '?')

def lower_tri(h):
    return h[:3]

def upper_tri(h):
    return h[3:]


# ── Build S=2 constraints ────────────────────────────────────────────────────

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

CONSTRAINED_COMPONENTS = []
adj = defaultdict(set)
constrained_pairs = set()
for k, forbidden in CONSTRAINTS.items():
    adj[k].add(k+1)
    adj[k+1].add(k)
    constrained_pairs.add(k)
    constrained_pairs.add(k+1)

visited = set()
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
        for nb in adj[node]:
            if nb not in visited:
                stack.append(nb)
    CONSTRAINED_COMPONENTS.append(sorted(component))

FREE_PAIRS = set(range(32)) - constrained_pairs


def is_s2_free(o):
    for k, forbidden in CONSTRAINTS.items():
        if (o[k], o[k+1]) in forbidden:
            return False
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 1. VALID ORIENTATION SUBSPACE STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("1. VALID ORIENTATION SUBSPACE STRUCTURE")
print("=" * 80)
print()

print(f"  Total orientation space: 2^32 = {2**32}")
print(f"  S=2-free orientations: 2^27 = {2**27}")
print(f"  Fraction: {2**27 / 2**32:.6f} (1/32)")
print()

print(f"  Constraint components: {len(CONSTRAINED_COMPONENTS)}")
for i, comp in enumerate(CONSTRAINED_COMPONENTS):
    bridges_in = [k for k in CONSTRAINTS if k in comp or k+1 in comp]
    print(f"    Component {i+1}: pairs {comp}, bridges {bridges_in}")

print(f"\n  Free pairs: {len(FREE_PAIRS)} ({sorted(FREE_PAIRS)})")
print()

# Describe each constraint
for k, forbidden in sorted(CONSTRAINTS.items()):
    allowed = [(o_k, o_k1) for o_k in [0,1] for o_k1 in [0,1]
               if (o_k, o_k1) not in forbidden]
    
    if set(allowed) == {(0,0), (1,1)}:
        ctype = f"o_{k} = o_{k+1} (must be EQUAL)"
    elif set(allowed) == {(0,1), (1,0)}:
        ctype = f"o_{k} ≠ o_{k+1} (must be DIFFERENT)"
    elif all(o_k1 == 0 for _, o_k1 in allowed):
        ctype = f"o_{k+1} = 0 (fixed)"
    elif all(o_k == 0 for o_k, _ in allowed):
        ctype = f"o_{k} = 0 (fixed)"
    else:
        ctype = f"allowed: {allowed}"
    
    print(f"  Bridge {k}: {ctype}")

print()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. COMPREHENSIVE PROPERTY COMPARISON: KW vs S=2-FREE SAMPLE
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("2. COMPREHENSIVE PROPERTY COMPARISON (50K S=2-free samples)")
print("=" * 80)
print()

N_SAMPLES = 50_000
rng = random.Random(42)


def full_analysis(orientation):
    """Compute comprehensive metrics for an orientation."""
    # Build sequence
    seq = []
    for k in range(N_PAIRS):
        if orientation[k] == 0:
            seq.append(PAIRS[k]['a'])
            seq.append(PAIRS[k]['b'])
        else:
            seq.append(PAIRS[k]['b'])
            seq.append(PAIRS[k]['a'])
    
    # --- Kernel chain ---
    chain_3bit = []
    chain_names = []
    for k in range(31):
        exit_hex = seq[2*k + 1]
        entry_hex = seq[2*k + 2]
        k3 = kernel_3bit(exit_hex, entry_hex)
        chain_3bit.append(k3)
        chain_names.append(kernel_name_from_3bit(k3))
    
    freq = Counter(chain_names)
    expected = 31 / 8
    chi2 = sum((freq.get(g, 0) - expected) ** 2 / expected
               for g in VALID_MASKS.values())
    
    # OMI XOR
    omi_count = 0
    xor_weights = []
    for i in range(30):
        xor_3 = tuple(chain_3bit[i][j] ^ chain_3bit[i+1][j] for j in range(3))
        xor_weights.append(sum(xor_3))
        if xor_3 == (1,1,1):
            omi_count += 1
    
    omi_frac = omi_count / 30
    mean_xor_weight = sum(xor_weights) / 30
    n_gens = len(freq)
    
    # --- Trigram stats ---
    lo_traj = [lower_tri(h) for h in seq]
    up_traj = [upper_tri(h) for h in seq]
    
    # Bridge trigram preservation
    lo_bridge_same = sum(1 for k in range(31) if lo_traj[2*k+1] == lo_traj[2*k+2])
    up_bridge_same = sum(1 for k in range(31) if up_traj[2*k+1] == up_traj[2*k+2])
    
    # Trigram pair diversity
    pair_freq = Counter((lo_traj[i], up_traj[i]) for i in range(64))
    n_unique_tri_pairs = len(pair_freq)
    
    # First hex trigram balance (how far from uniform?)
    first_lo = Counter(lo_traj[2*k] for k in range(N_PAIRS))
    first_up = Counter(up_traj[2*k] for k in range(N_PAIRS))
    
    # Chi-squared for trigram uniformity in first hex
    tri_expected = N_PAIRS / 8  # = 4
    lo_chi2 = sum((first_lo.get(t, 0) - tri_expected)**2 / tri_expected
                  for t in TRIGRAM_NAMES)
    up_chi2 = sum((first_up.get(t, 0) - tri_expected)**2 / tri_expected
                  for t in TRIGRAM_NAMES)
    
    # Bridge Hamming distances
    bridge_weights = []
    for k in range(31):
        h = sum(seq[2*k+1][i] ^ seq[2*k+2][i] for i in range(6))
        bridge_weights.append(h)
    mean_bridge_h = sum(bridge_weights) / 31
    
    # Canon asymmetry: binary-high count in upper vs lower canon
    def hex_to_int(h):
        v = 0
        for bit in h:
            v = v * 2 + bit
        return v
    
    upper_canon_binhigh = 0
    lower_canon_binhigh = 0
    for k in range(N_PAIRS):
        va = hex_to_int(seq[2*k])
        vb = hex_to_int(seq[2*k+1])
        if k < 15:
            if va > vb: upper_canon_binhigh += 1
        else:
            if va > vb: lower_canon_binhigh += 1
    
    return {
        'chi2': chi2,
        'omi_frac': omi_frac,
        'mean_xor_weight': mean_xor_weight,
        'n_gens': n_gens,
        'lo_bridge_same': lo_bridge_same,
        'up_bridge_same': up_bridge_same,
        'n_unique_tri_pairs': n_unique_tri_pairs,
        'lo_chi2': lo_chi2,
        'up_chi2': up_chi2,
        'mean_bridge_h': mean_bridge_h,
        'upper_binhigh': upper_canon_binhigh,
        'lower_binhigh': lower_canon_binhigh,
        'canon_asym': upper_canon_binhigh - lower_canon_binhigh,
    }


# KW baseline
kw_stats = full_analysis([0]*32)
print(f"  KW metrics:")
for key, val in sorted(kw_stats.items()):
    print(f"    {key}: {val}")
print()

# Sample S=2-free orientations
print(f"  Sampling {N_SAMPLES} S=2-free orientations...")
sample_results = defaultdict(list)
n_tried = 0

for i in range(N_SAMPLES):
    while True:
        n_tried += 1
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    
    stats = full_analysis(o)
    for key, val in stats.items():
        sample_results[key].append(val)

print(f"  Done. Acceptance rate: {N_SAMPLES/n_tried:.4f}")
print()

# Summary table
print(f"  {'Metric':>22s}  {'KW':>7s}  {'Mean':>7s}  {'Std':>7s}  "
      f"{'p-low':>7s}  {'p-high':>7s}")
print(f"  {'-'*65}")

for key in sorted(kw_stats.keys()):
    kw_val = kw_stats[key]
    arr = np.array(sample_results[key])
    p_low = np.mean(arr <= kw_val)
    p_high = np.mean(arr >= kw_val)
    
    print(f"  {key:>22s}  {kw_val:7.3f}  {arr.mean():7.3f}  {arr.std():7.3f}  "
          f"{p_low:7.4f}  {p_high:7.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. CANON ASYMMETRY — THE STRONGEST CANDIDATE SIGNAL
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("3. CANON ASYMMETRY (binary-high in upper vs lower canon)")
print("=" * 80)
print()

asym_arr = np.array(sample_results['canon_asym'])
kw_asym = kw_stats['canon_asym']
print(f"  KW canon asymmetry: {kw_asym}")
print(f"  Random S=2-free: mean = {asym_arr.mean():.2f}, std = {asym_arr.std():.2f}")
print(f"  P(asym ≥ KW) = {np.mean(asym_arr >= kw_asym):.4f}")
print(f"  P(|asym| ≥ |KW|) = {np.mean(np.abs(asym_arr) >= abs(kw_asym)):.4f}")

# Histogram of canon asymmetry
print(f"\n  Canon asymmetry distribution:")
hist, edges = np.histogram(asym_arr, bins=range(-12, 13))
for i in range(len(hist)):
    lo, hi = int(edges[i]), int(edges[i+1])
    pct = 100 * hist[i] / N_SAMPLES
    bar = '█' * max(1, int(pct * 2))
    marker = ' ← KW' if lo <= kw_asym < hi else ''
    print(f"    [{lo:+3d},{hi:+3d}): {hist[i]:5d} ({pct:5.1f}%) {bar}{marker}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. JOINT ANALYSIS: KERNEL UNIFORMITY + CANON ASYMMETRY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("4. JOINT ANALYSIS: kernel chi² + canon asymmetry")
print("=" * 80)
print()

chi2_arr = np.array(sample_results['chi2'])
asym_arr = np.array(sample_results['canon_asym'])

# Correlation
corr = np.corrcoef(chi2_arr, asym_arr)[0, 1]
print(f"  r(chi², canon_asym) = {corr:.4f}")

# Joint: chi² ≤ KW AND asym ≥ KW
p_chi2 = np.mean(chi2_arr <= kw_stats['chi2'])
p_asym = np.mean(asym_arr >= kw_stats['canon_asym'])
joint_count = np.sum((chi2_arr <= kw_stats['chi2']) & 
                      (asym_arr >= kw_stats['canon_asym']))
p_joint = joint_count / N_SAMPLES
p_expected = p_chi2 * p_asym

print(f"  P(chi² ≤ KW) = {p_chi2:.4f}")
print(f"  P(asym ≥ KW) = {p_asym:.4f}")
print(f"  P(joint) = {p_joint:.5f} ({joint_count}/{N_SAMPLES})")
print(f"  If independent: {p_expected:.5f}")
print(f"  Ratio: {p_joint / p_expected:.3f}" if p_expected > 0 else "")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. KERNEL CHAIN DEEP DIVE: DISTRIBUTION ACROSS S=2-FREE
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("5. KERNEL CHAIN: DETAILED DISTRIBUTION ACROSS S=2-FREE ORIENTATIONS")
print("=" * 80)
print()

# Percentile analysis for kernel chi²
pctiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
chi2_pctvals = np.percentile(chi2_arr, pctiles)
print(f"  Kernel chi² distribution:")
for p, v in zip(pctiles, chi2_pctvals):
    marker = ' ← KW' if abs(v - kw_stats['chi2']) < 0.5 else ''
    print(f"    {p:3d}th percentile: {v:.2f}{marker}")

print(f"\n  KW chi² = {kw_stats['chi2']:.2f}")
print(f"  Percentile: {100*np.mean(chi2_arr <= kw_stats['chi2']):.1f}")

# OMI-XOR distribution
omi_arr = np.array(sample_results['omi_frac'])
print(f"\n  OMI-XOR fraction distribution:")
print(f"    KW: {kw_stats['omi_frac']:.3f}")
print(f"    Mean: {omi_arr.mean():.3f} ± {omi_arr.std():.3f}")
print(f"    P(OMI ≥ KW) = {np.mean(omi_arr >= kw_stats['omi_frac']):.4f}")

# Independence check: chi² vs OMI
corr_chi_omi = np.corrcoef(chi2_arr, omi_arr)[0, 1]
print(f"\n  r(chi², OMI) = {corr_chi_omi:.4f}")

# Joint: chi² ≤ KW AND OMI ≥ KW
joint_chi_omi = np.sum((chi2_arr <= kw_stats['chi2']) & 
                        (omi_arr >= kw_stats['omi_frac']))
p_joint_co = joint_chi_omi / N_SAMPLES
p_omi = np.mean(omi_arr >= kw_stats['omi_frac'])
p_expected_co = p_chi2 * p_omi
print(f"  P(chi² ≤ KW AND OMI ≥ KW) = {p_joint_co:.5f} ({joint_chi_omi}/{N_SAMPLES})")
print(f"  If independent: {p_expected_co:.5f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. TRIGRAM BRIDGE PRESERVATION: IS KW SPECIAL?
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("6. TRIGRAM BRIDGE PRESERVATION")
print("=" * 80)
print()

lo_bridge_arr = np.array(sample_results['lo_bridge_same'])
up_bridge_arr = np.array(sample_results['up_bridge_same'])

print(f"  Lower trigram preserved at bridges:")
print(f"    KW: {kw_stats['lo_bridge_same']}/31")
print(f"    Random S=2-free: mean = {lo_bridge_arr.mean():.2f} ± {lo_bridge_arr.std():.2f}")
print(f"    P(≥ KW) = {np.mean(lo_bridge_arr >= kw_stats['lo_bridge_same']):.4f}")
print(f"    P(≤ KW) = {np.mean(lo_bridge_arr <= kw_stats['lo_bridge_same']):.4f}")

print(f"\n  Upper trigram preserved at bridges:")
print(f"    KW: {kw_stats['up_bridge_same']}/31")
print(f"    Random S=2-free: mean = {up_bridge_arr.mean():.2f} ± {up_bridge_arr.std():.2f}")
print(f"    P(≥ KW) = {np.mean(up_bridge_arr >= kw_stats['up_bridge_same']):.4f}")
print(f"    P(≤ KW) = {np.mean(up_bridge_arr <= kw_stats['up_bridge_same']):.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. MULTI-PROPERTY FILTER: HOW MANY S=2-FREE MATCH KW'S PROFILE?
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("7. MULTI-PROPERTY FILTER")
print("   How many S=2-free orientations match KW on multiple properties?")
print("=" * 80)
print()

# Progressive filtering
conditions = [
    ('chi2 ≤ KW', lambda i: sample_results['chi2'][i] <= kw_stats['chi2']),
    ('OMI ≥ KW', lambda i: sample_results['omi_frac'][i] >= kw_stats['omi_frac']),
    ('asym ≥ KW', lambda i: sample_results['canon_asym'][i] >= kw_stats['canon_asym']),
    ('lo_bridge ≥ KW', lambda i: sample_results['lo_bridge_same'][i] >= kw_stats['lo_bridge_same']),
    ('up_bridge ≤ KW', lambda i: sample_results['up_bridge_same'][i] <= kw_stats['up_bridge_same']),
]

# All combinations
from itertools import combinations

remaining = set(range(N_SAMPLES))
print(f"  Starting with {N_SAMPLES} S=2-free orientations")

for n_conds in range(1, len(conditions) + 1):
    best_label = None
    best_count = N_SAMPLES + 1
    
    for combo in combinations(range(len(conditions)), n_conds):
        label = ' AND '.join(conditions[c][0] for c in combo)
        count = sum(1 for i in range(N_SAMPLES) 
                    if all(conditions[c][1](i) for c in combo))
        if count < best_count:
            best_count = count
            best_label = label
    
    # Also show the cumulative filter
    cum_count = sum(1 for i in range(N_SAMPLES) 
                    if all(conditions[c][1](i) for c in range(n_conds)))
    
    print(f"  After {n_conds} conditions (cumulative): {cum_count} ({100*cum_count/N_SAMPLES:.2f}%)")
    print(f"    Tightest {n_conds}-combination: '{best_label}' → {best_count} ({100*best_count/N_SAMPLES:.3f}%)")

# Final: all 5 conditions
all_match = sum(1 for i in range(N_SAMPLES)
                if all(conditions[c][1](i) for c in range(len(conditions))))
print(f"\n  All conditions: {all_match}/{N_SAMPLES} ({100*all_match/N_SAMPLES:.4f}%)")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. BRIDGE WEIGHT SMOOTHNESS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("8. BRIDGE WEIGHT SMOOTHNESS")
print("=" * 80)
print()

bridge_h_arr = np.array(sample_results['mean_bridge_h'])
print(f"  Mean bridge Hamming weight:")
print(f"    KW: {kw_stats['mean_bridge_h']:.3f}")
print(f"    Random S=2-free: mean = {bridge_h_arr.mean():.3f} ± {bridge_h_arr.std():.3f}")
print(f"    P(≤ KW) = {np.mean(bridge_h_arr <= kw_stats['mean_bridge_h']):.4f}")
print(f"    P(≥ KW) = {np.mean(bridge_h_arr >= kw_stats['mean_bridge_h']):.4f}")


print()
print("=" * 80)
print("THREAD C EXTENDED ANALYSIS COMPLETE")
print("=" * 80)
