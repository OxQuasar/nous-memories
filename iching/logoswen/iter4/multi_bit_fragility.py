"""
Round 2: Multi-Bit Interactions — Gradient to Curvature

Five experiments:
  1. Joint flip of bits 10+17 (improvement cone)
  2. Joint flip of bits 13+23 (catastrophic pair)
  3. Three-flip test {9,10,17} and subset {9,17}
  4. All 2-bit combos involving {10,17} (improvement cone neighborhood)
  5. Random Hessian sample — 50 random 2-bit flips

Metrics: chi², asymmetry, m-score.
Coupling: 20K conditional sampling for critical experiments (1, 2, 3 only).
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter
from sequence import KING_WEN, all_bits
import random
import numpy as np
import json
import time

# ══════════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE (from round 1)
# ══════════════════════════════════════════════════════════════════════════════

DIMS = 6
N_PAIRS = 32
M = [tuple(b) for b in all_bits()]

VALID_MASKS = {
    (0,0,0,0,0,0): 'id',  (1,0,0,0,0,1): 'O',  (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',   (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',  (1,1,1,1,1,1): 'OMI',
}
ALL_GEN_NAMES = list(VALID_MASKS.values())

PAIRS = []
for k in range(N_PAIRS):
    PAIRS.append({'a': M[2*k], 'b': M[2*k+1]})


def xor6(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def compute_S(ha, hb):
    m = xor6(ha, hb)
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])

def kernel_3bit(ha, hb):
    m = xor6(ha, hb)
    return (m[5], m[4], m[3])

def kernel_name(ha, hb):
    k3 = kernel_3bit(ha, hb)
    gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
    return VALID_MASKS.get(gen_6, '?')

def hex_to_int(h):
    v = 0
    for bit in h:
        v = v * 2 + bit
    return v


# S=2 constraints
CONSTRAINTS = {}
for k in range(31):
    forbidden = set()
    for o_k in [0, 1]:
        for o_k1 in [0, 1]:
            ex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
            en = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
            if compute_S(ex, en) == 2:
                forbidden.add((o_k, o_k1))
    if forbidden:
        CONSTRAINTS[k] = forbidden

CONSTRAINED_PAIRS = set()
for k in CONSTRAINTS:
    CONSTRAINED_PAIRS.add(k)
    CONSTRAINED_PAIRS.add(k+1)

FREE_PAIRS = sorted(set(range(32)) - CONSTRAINED_PAIRS)
COMPONENTS = [(13, 14), (19, 20), (25, 26), (27, 28), (29, 30)]

COMPONENT_VALID = {}
for p1, p2 in COMPONENTS:
    bridge_k = p1
    if bridge_k in CONSTRAINTS:
        forbidden = CONSTRAINTS[bridge_k]
        valid = [(o1, o2) for o1 in [0,1] for o2 in [0,1] if (o1, o2) not in forbidden]
        COMPONENT_VALID[(p1, p2)] = valid


def is_s2_free(o):
    for k, forbidden in CONSTRAINTS.items():
        if (o[k], o[k+1]) in forbidden:
            return False
    return True


# M-decisive pairs
M_DECISIVE = []
for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    if a[1] != a[4]:
        M_DECISIVE.append(k)


def build_sequence(o):
    seq = []
    for k in range(N_PAIRS):
        if o[k] == 0:
            seq.append(PAIRS[k]['a'])
            seq.append(PAIRS[k]['b'])
        else:
            seq.append(PAIRS[k]['b'])
            seq.append(PAIRS[k]['a'])
    return seq


def compute_all_metrics(o):
    seq = build_sequence(o)
    freq = Counter()
    for k in range(31):
        nm = kernel_name(seq[2*k+1], seq[2*k+2])
        freq[nm] += 1
    expected = 31 / 8
    chi2 = sum((freq.get(g, 0) - expected)**2 / expected for g in ALL_GEN_NAMES)
    upper_bh = sum(1 for k in range(15) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    lower_bh = sum(1 for k in range(15, 32) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    asym = upper_bh - lower_bh
    m_score = sum(1 for k in M_DECISIVE if seq[2*k][1] == 0)
    return chi2, asym, m_score


# Free bits index (same as round 1)
free_bits = []
for p in FREE_PAIRS:
    free_bits.append({
        'bit_index': len(free_bits), 'type': 'A', 'pairs': [p],
        'description': f'pair {p}',
    })
for ci, ((p1, p2), valid) in enumerate(COMPONENT_VALID.items()):
    free_bits.append({
        'bit_index': len(free_bits), 'type': 'B', 'pairs': [p1, p2],
        'component': (p1, p2), 'valid_states': valid,
        'description': f'component ({p1},{p2})',
    })
assert len(free_bits) == 27


def apply_bits_to_orientation(bit_indices):
    """Create orientation with multiple free bits flipped from KW."""
    o = [0] * 32
    for bi_idx in bit_indices:
        bi = free_bits[bi_idx]
        if bi['type'] == 'A':
            o[bi['pairs'][0]] = 1
        else:
            other = [s for s in bi['valid_states'] if s != (0, 0)][0]
            p1, p2 = bi['pairs']
            o[p1] = other[0]
            o[p2] = other[1]
    return o


def fixed_pairs_for_bits(bit_indices):
    """Return dict of pair_idx -> value for all specified flipped bits."""
    fixed = {}
    for bi_idx in bit_indices:
        bi = free_bits[bi_idx]
        if bi['type'] == 'A':
            fixed[bi['pairs'][0]] = 1
        else:
            other = [s for s in bi['valid_states'] if s != (0, 0)][0]
            p1, p2 = bi['pairs']
            fixed[p1] = other[0]
            fixed[p2] = other[1]
    return fixed


def sample_s2_free_with_fixed(rng, fixed_pairs):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        for p, v in fixed_pairs.items():
            o[p] = v
        if is_s2_free(o):
            return o


# ══════════════════════════════════════════════════════════════════════════════
# LOAD ROUND 1 DATA (for single-bit deltas)
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter4/round1_data.json') as f:
    r1 = json.load(f)

KW_CHI2 = r1['kw_baseline']['chi2']
KW_ASYM = r1['kw_baseline']['asym']
KW_M = r1['kw_baseline']['m_score']
KW_RATIO = r1['kw_baseline']['coupling_ratio']

# Single-bit deltas indexed by bit_index
R1_DELTA = {}
for r in r1['single_bit_metrics']:
    R1_DELTA[r['bit_index']] = {
        'd_chi2': r['d_chi2'],
        'd_asym': r['d_asym'],
        'd_m': r['d_m'],
    }


def expected_additive(bit_indices):
    """Sum of single-bit deltas — the linear prediction."""
    d_chi2 = sum(R1_DELTA[b]['d_chi2'] for b in bit_indices)
    d_asym = sum(R1_DELTA[b]['d_asym'] for b in bit_indices)
    d_m = sum(R1_DELTA[b]['d_m'] for b in bit_indices)
    return KW_CHI2 + d_chi2, KW_ASYM + d_asym, KW_M + d_m


def compute_multi_flip(bit_indices):
    """Compute actual metrics and interaction terms for a multi-bit flip."""
    o = apply_bits_to_orientation(bit_indices)
    s2ok = is_s2_free(o)
    if not s2ok:
        return None  # This combo violates S=2
    chi2, asym, m = compute_all_metrics(o)
    exp_chi2, exp_asym, exp_m = expected_additive(bit_indices)
    return {
        'bits': list(bit_indices),
        's2_free': True,
        'chi2': float(chi2),
        'asym': int(asym),
        'm_score': int(m),
        'exp_chi2': float(exp_chi2),
        'exp_asym': float(exp_asym),
        'exp_m': float(exp_m),
        'int_chi2': float(chi2 - exp_chi2),  # interaction term
        'int_asym': int(asym) - int(exp_asym),
        'int_m': int(m) - int(exp_m),
        'd_chi2': float(chi2 - KW_CHI2),
        'd_asym': int(asym - KW_ASYM),
        'd_m': int(m - KW_M),
    }


def coupling_for_bits(bit_indices, n_samples=20000, seed=None):
    """Sample conditional coupling ratio with given bits fixed to flipped."""
    fixed = fixed_pairs_for_bits(bit_indices)
    rng = random.Random(seed)
    s_chi2 = np.empty(n_samples)
    s_asym = np.empty(n_samples)
    for i in range(n_samples):
        o = sample_s2_free_with_fixed(rng, fixed)
        c2, asym, _ = compute_all_metrics(o)
        s_chi2[i] = c2
        s_asym[i] = asym
    p_c = float(np.mean(s_chi2 <= KW_CHI2))
    p_a = float(np.mean(s_asym >= KW_ASYM))
    p_j = float(np.mean((s_chi2 <= KW_CHI2) & (s_asym >= KW_ASYM)))
    expected = p_c * p_a
    ratio = p_j / expected if expected > 0 else float('inf')
    return {
        'p_chi2': p_c, 'p_asym': p_a, 'p_joint': p_j,
        'ratio': float(ratio), 'd_ratio': float(ratio - KW_RATIO),
    }


def classify_flip(d_chi2, d_asym, d_m):
    """Classify a flip's metric changes."""
    chi2_f = 'improve' if d_chi2 < -1e-9 else ('degrade' if d_chi2 > 1e-9 else 'neutral')
    asym_f = 'improve' if d_asym > 0 else ('degrade' if d_asym < 0 else 'neutral')
    m_f = 'improve' if d_m > 0 else ('degrade' if d_m < 0 else 'neutral')
    flags = [chi2_f, asym_f, m_f]
    return flags.count('improve'), flags.count('degrade'), flags


# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("ROUND 2: MULTI-BIT INTERACTIONS")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}, asym={KW_ASYM}, m={KW_M}")
print()

all_results = {}

# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 1: bits 10+17 (improvement cone)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 1: bits 10+17 (pairs 10, 21) — improvement cone")
print("─" * 80)

r = compute_multi_flip([10, 17])
print(f"  Actual:   chi²={r['chi2']:.4f}  asym={r['asym']}  m={r['m_score']}")
print(f"  Expected: chi²={r['exp_chi2']:.4f}  asym={r['exp_asym']}  m={r['exp_m']}")
print(f"  Interact: chi²={r['int_chi2']:+.4f}  asym={r['int_asym']:+d}  m={r['int_m']:+d}")
print(f"  Delta:    chi²={r['d_chi2']:+.4f}  asym={r['d_asym']:+d}  m={r['d_m']:+d}")
n_imp, n_deg, flags = classify_flip(r['d_chi2'], r['d_asym'], r['d_m'])
print(f"  Classification: {n_imp} improve, {n_deg} degrade — {flags}")

print("  Computing coupling (20K)...")
t0 = time.time()
c = coupling_for_bits([10, 17], seed=2001)
print(f"  Coupling: ratio={c['ratio']:.3f}  Δ={c['d_ratio']:+.3f}")
print(f"  (P_chi2={c['p_chi2']:.4f}, P_asym={c['p_asym']:.4f}, P_joint={c['p_joint']:.5f})")
print(f"  Time: {time.time()-t0:.1f}s")
r['coupling'] = c
all_results['exp1_bits_10_17'] = r
print()

# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 2: bits 13+23 (catastrophic pair)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 2: bits 13+23 (pair 15, component 19,20) — catastrophic pair")
print("─" * 80)

r = compute_multi_flip([13, 23])
if r is None:
    print("  ** S=2 VIOLATION — this combo is forbidden! **")
    all_results['exp2_bits_13_23'] = {'s2_free': False, 'bits': [13, 23]}
else:
    print(f"  Actual:   chi²={r['chi2']:.4f}  asym={r['asym']}  m={r['m_score']}")
    print(f"  Expected: chi²={r['exp_chi2']:.4f}  asym={r['exp_asym']}  m={r['exp_m']}")
    print(f"  Interact: chi²={r['int_chi2']:+.4f}  asym={r['int_asym']:+d}  m={r['int_m']:+d}")
    print(f"  Delta:    chi²={r['d_chi2']:+.4f}  asym={r['d_asym']:+d}  m={r['d_m']:+d}")
    n_imp, n_deg, flags = classify_flip(r['d_chi2'], r['d_asym'], r['d_m'])
    print(f"  Classification: {n_imp} improve, {n_deg} degrade — {flags}")

    print("  Computing coupling (20K)...")
    t0 = time.time()
    c = coupling_for_bits([13, 23], seed=2002)
    print(f"  Coupling: ratio={c['ratio']:.3f}  Δ={c['d_ratio']:+.3f}")
    print(f"  Time: {time.time()-t0:.1f}s")
    r['coupling'] = c
    all_results['exp2_bits_13_23'] = r
print()

# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 3: bits {9,10,17} and subset {9,17}
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 3a: bits {9, 17} (pairs 9, 21)")
print("─" * 80)

r = compute_multi_flip([9, 17])
print(f"  Actual:   chi²={r['chi2']:.4f}  asym={r['asym']}  m={r['m_score']}")
print(f"  Expected: chi²={r['exp_chi2']:.4f}  asym={r['exp_asym']}  m={r['exp_m']}")
print(f"  Interact: chi²={r['int_chi2']:+.4f}  asym={r['int_asym']:+d}  m={r['int_m']:+d}")
print(f"  Delta:    chi²={r['d_chi2']:+.4f}  asym={r['d_asym']:+d}  m={r['d_m']:+d}")
n_imp, n_deg, flags = classify_flip(r['d_chi2'], r['d_asym'], r['d_m'])
print(f"  Classification: {n_imp} improve, {n_deg} degrade — {flags}")
all_results['exp3a_bits_9_17'] = r
print()

print("─" * 80)
print("EXPERIMENT 3b: bits {9, 10, 17} (pairs 9, 10, 21) — all-three test")
print("─" * 80)

r = compute_multi_flip([9, 10, 17])
print(f"  Actual:   chi²={r['chi2']:.4f}  asym={r['asym']}  m={r['m_score']}")
print(f"  Expected: chi²={r['exp_chi2']:.4f}  asym={r['exp_asym']}  m={r['exp_m']}")
print(f"  Interact: chi²={r['int_chi2']:+.4f}  asym={r['int_asym']:+d}  m={r['int_m']:+d}")
print(f"  Delta:    chi²={r['d_chi2']:+.4f}  asym={r['d_asym']:+d}  m={r['d_m']:+d}")
n_imp, n_deg, flags = classify_flip(r['d_chi2'], r['d_asym'], r['d_m'])
print(f"  Classification: {n_imp} improve, {n_deg} degrade — {flags}")

# Is this all-three-improving?
if r['d_chi2'] < -1e-9 and r['d_asym'] > 0 and r['d_m'] > 0:
    print("  *** ALL THREE METRICS IMPROVE! First all-improving perturbation found. ***")
elif n_deg == 0 and n_imp >= 1:
    print("  Pure improvement (no degradation).")
else:
    print("  Not an all-three-improver.")

print("  Computing coupling (20K)...")
t0 = time.time()
c = coupling_for_bits([9, 10, 17], seed=2003)
print(f"  Coupling: ratio={c['ratio']:.3f}  Δ={c['d_ratio']:+.3f}")
print(f"  Time: {time.time()-t0:.1f}s")
r['coupling'] = c
all_results['exp3b_bits_9_10_17'] = r
print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 4: Improvement cone neighborhood
# All 2-bit combos involving {10, 17} with other bits
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 4: Improvement cone neighborhood — 2-bit combos with {10,17}")
print("─" * 80)
print()

other_bits = [b for b in range(27) if b not in (10, 17)]

exp4_results = []

header = (f"{'anchor':>6s} {'other':>5s} {'pair(s)':>10s} "
          f"{'chi2':>7s} {'asym':>5s} {'m':>3s} "
          f"{'i_chi2':>8s} {'i_asym':>6s} {'i_m':>4s} "
          f"{'#imp':>4s} {'#deg':>4s} {'flag':>6s}")
print(header)
print("─" * len(header))

for anchor in [10, 17]:
    for other in other_bits:
        bits_combo = sorted([anchor, other])
        r = compute_multi_flip(bits_combo)
        if r is None:
            exp4_results.append({
                'anchor': anchor, 'other': other, 'bits': bits_combo,
                's2_free': False,
            })
            other_bi = free_bits[other]
            pairs_str = ','.join(str(p) for p in other_bi['pairs'])
            print(f"{anchor:6d} {other:5d} {pairs_str:>10s}   ** S=2 VIOLATION **")
            continue

        n_imp, n_deg, flags = classify_flip(r['d_chi2'], r['d_asym'], r['d_m'])

        # Flag special cases
        flag = ''
        if n_imp >= 1 and n_deg == 0:
            flag = 'PURE+'
        if r['d_chi2'] < -1e-9 and r['d_asym'] > 0 and r['d_m'] > 0:
            flag = 'ALL3!'

        other_bi = free_bits[other]
        pairs_str = ','.join(str(p) for p in other_bi['pairs'])
        print(f"{anchor:6d} {other:5d} {pairs_str:>10s} "
              f"{r['chi2']:7.3f} {r['asym']:5d} {r['m_score']:3d} "
              f"{r['int_chi2']:+8.4f} {r['int_asym']:+6d} {r['int_m']:+4d} "
              f"{n_imp:4d} {n_deg:4d} {flag:>6s}")

        r['anchor'] = anchor
        r['other'] = other
        r['n_improve'] = n_imp
        r['n_degrade'] = n_deg
        exp4_results.append(r)

all_results['exp4_cone_neighborhood'] = exp4_results
print()

# Summary
valid_results = [r for r in exp4_results if r.get('s2_free', True)]
pure_improve = [r for r in valid_results if r.get('n_improve', 0) >= 1 and r.get('n_degrade', 0) == 0]
all_three = [r for r in valid_results if r.get('d_chi2', 0) < -1e-9 and r.get('d_asym', 0) > 0 and r.get('d_m', 0) > 0]
s2_violations = [r for r in exp4_results if not r.get('s2_free', True)]

print(f"  Experiment 4 summary:")
print(f"    Total combos: {len(exp4_results)}")
print(f"    S=2 violations: {len(s2_violations)}")
print(f"    Valid: {len(valid_results)}")
print(f"    Pure improvement (≥1 improve, 0 degrade): {len(pure_improve)}")
if pure_improve:
    for r in pure_improve:
        print(f"      bits {r['bits']}: chi²={r['d_chi2']:+.4f} asym={r['d_asym']:+d} m={r['d_m']:+d}")
print(f"    All-three-improving: {len(all_three)}")
if all_three:
    for r in all_three:
        print(f"      bits {r['bits']}: chi²={r['d_chi2']:+.4f} asym={r['d_asym']:+d} m={r['d_m']:+d}")
print()

# Interaction term statistics for experiment 4
int_chi2_vals = [abs(r['int_chi2']) for r in valid_results]
int_asym_vals = [abs(r.get('int_asym', 0)) for r in valid_results]
int_m_vals = [abs(r.get('int_m', 0)) for r in valid_results]
print(f"  Interaction term magnitudes (experiment 4):")
print(f"    |int_chi2|: mean={np.mean(int_chi2_vals):.4f} max={np.max(int_chi2_vals):.4f}")
print(f"    |int_asym|: mean={np.mean(int_asym_vals):.2f} max={np.max(int_asym_vals)}")
print(f"    |int_m|:    mean={np.mean(int_m_vals):.2f} max={np.max(int_m_vals)}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 5: Random Hessian sample — 50 random 2-bit flips
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 5: Random Hessian — 50 random 2-bit combos (not involving 10 or 17)")
print("─" * 80)
print()

# Pick 50 random pairs of bits not including 10 or 17
non_cone_bits = [b for b in range(27) if b not in (10, 17)]
rng_hess = random.Random(7777)

# Generate 50 unique pairs
hessian_pairs = set()
while len(hessian_pairs) < 50:
    b1 = rng_hess.choice(non_cone_bits)
    b2 = rng_hess.choice(non_cone_bits)
    if b1 != b2:
        pair = tuple(sorted([b1, b2]))
        hessian_pairs.add(pair)

hessian_pairs = sorted(hessian_pairs)

exp5_results = []

header5 = (f"{'b1':>3s} {'b2':>3s} {'p1':>6s} {'p2':>6s} "
           f"{'chi2':>7s} {'asym':>5s} {'m':>3s} "
           f"{'i_chi2':>8s} {'i_asym':>6s} {'i_m':>4s} "
           f"{'nl_chi2':>7s}")
print(header5)
print("─" * len(header5))

for b1, b2 in hessian_pairs:
    r = compute_multi_flip([b1, b2])
    if r is None:
        exp5_results.append({
            'bits': [b1, b2], 's2_free': False,
        })
        p1_str = ','.join(str(p) for p in free_bits[b1]['pairs'])
        p2_str = ','.join(str(p) for p in free_bits[b2]['pairs'])
        print(f"{b1:3d} {b2:3d} {p1_str:>6s} {p2_str:>6s}   ** S=2 VIOLATION **")
        continue

    # Nonlinearity coefficient: |interaction| / |sum of individual deltas|
    sum_d_chi2 = R1_DELTA[b1]['d_chi2'] + R1_DELTA[b2]['d_chi2']
    nl_chi2 = abs(r['int_chi2']) / abs(sum_d_chi2) if abs(sum_d_chi2) > 1e-9 else float('nan')

    p1_str = ','.join(str(p) for p in free_bits[b1]['pairs'])
    p2_str = ','.join(str(p) for p in free_bits[b2]['pairs'])
    nl_str = f"{nl_chi2:.4f}" if not np.isnan(nl_chi2) else "   NaN"
    print(f"{b1:3d} {b2:3d} {p1_str:>6s} {p2_str:>6s} "
          f"{r['chi2']:7.3f} {r['asym']:5d} {r['m_score']:3d} "
          f"{r['int_chi2']:+8.4f} {r['int_asym']:+6d} {r['int_m']:+4d} "
          f"{nl_str:>7s}")

    r['nl_chi2'] = float(nl_chi2) if not np.isnan(nl_chi2) else None
    exp5_results.append(r)

all_results['exp5_random_hessian'] = exp5_results
print()

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 4: NONLINEARITY SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("TABLE 4: NONLINEARITY SUMMARY")
print("─" * 80)
print()

# Gather all 2-bit combos (from experiments 4 and 5) that are S=2-free
all_2bit = []
for r in exp4_results:
    if r.get('s2_free', True) and 'int_chi2' in r:
        all_2bit.append(r)
for r in exp5_results:
    if r.get('s2_free', True) and 'int_chi2' in r:
        all_2bit.append(r)

print(f"Total valid 2-bit combos analyzed: {len(all_2bit)}")
print()

# Chi² interaction statistics
int_chi2_all = [r['int_chi2'] for r in all_2bit]
abs_int_chi2 = [abs(v) for v in int_chi2_all]
print(f"Chi² interaction terms:")
print(f"  Mean: {np.mean(int_chi2_all):+.4f}")
print(f"  Mean |int|: {np.mean(abs_int_chi2):.4f}")
print(f"  Std: {np.std(int_chi2_all):.4f}")
print(f"  Min: {min(int_chi2_all):+.4f}")
print(f"  Max: {max(int_chi2_all):+.4f}")
print(f"  Fraction exactly zero: {sum(1 for v in int_chi2_all if abs(v) < 1e-9) / len(int_chi2_all):.3f}")
print()

# Asym interaction statistics
int_asym_all = [r['int_asym'] for r in all_2bit]
abs_int_asym = [abs(v) for v in int_asym_all]
print(f"Asymmetry interaction terms:")
print(f"  Mean: {np.mean(int_asym_all):+.2f}")
print(f"  Mean |int|: {np.mean(abs_int_asym):.2f}")
print(f"  Distribution: {dict(Counter(int_asym_all))}")
print()

# M-score interaction statistics
int_m_all = [r['int_m'] for r in all_2bit]
abs_int_m = [abs(v) for v in int_m_all]
print(f"M-score interaction terms:")
print(f"  Mean: {np.mean(int_m_all):+.2f}")
print(f"  Mean |int|: {np.mean(abs_int_m):.2f}")
print(f"  Distribution: {dict(Counter(int_m_all))}")
print()

# Nonlinearity coefficient for chi² (experiment 5 only — non-cone pairs)
nl_vals = [r['nl_chi2'] for r in exp5_results if r.get('nl_chi2') is not None]
if nl_vals:
    print(f"Nonlinearity coefficient (|interaction| / |sum of singles|) for chi²:")
    print(f"  (From experiment 5 — random pairs, excluding cone bits)")
    print(f"  Mean: {np.mean(nl_vals):.4f}")
    print(f"  Median: {np.median(nl_vals):.4f}")
    print(f"  Std: {np.std(nl_vals):.4f}")
    print(f"  Min: {min(nl_vals):.4f}")
    print(f"  Max: {max(nl_vals):.4f}")
    print(f"  Fraction < 0.1 (near-additive): {sum(1 for v in nl_vals if v < 0.1) / len(nl_vals):.3f}")
    print(f"  Fraction > 0.5 (strongly epistatic): {sum(1 for v in nl_vals if v > 0.5) / len(nl_vals):.3f}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════════════════════════════

# Clean up for JSON (remove any np types)
def json_clean(obj):
    if isinstance(obj, dict):
        return {k: json_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [json_clean(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

save_data = json_clean({
    'kw_baseline': {
        'chi2': KW_CHI2, 'asym': KW_ASYM, 'm_score': KW_M,
        'coupling_ratio': KW_RATIO,
    },
    'experiments': all_results,
})

with open('/home/quasar/nous/logoswen/iter4/round2_data.json', 'w') as f:
    json.dump(save_data, f, indent=2)

print("Data saved to logoswen/iter4/round2_data.json")
print()
print("=" * 80)
print("ROUND 2 COMPLETE")
print("=" * 80)
