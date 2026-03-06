"""
Round 1: Single-Bit Perturbation Baseline

Flip each of the 27 free orientation bits independently from KW,
measure all four metrics for each flip, report the complete table.

Free bits 0-21:  22 unconstrained pairs (in pair-index order)
Free bits 22-26: 5 constraint components (in pair-index order)

Metrics:
  1. Kernel chi² (uniformity of 8 kernel dressings across 31 bridges)
  2. Canon asymmetry (binary-high-first upper minus lower)
  3. M-component score (among L2≠L5 pairs, count L2=yin in first hex)
  4. Coupling ratio (conditional sampling — 20K per flip)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import numpy as np
import json
import time

# ══════════════════════════════════════════════════════════════════════════════
# SETUP — copied from iter3 infrastructure
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


# ── S=2 constraints ──────────────────────────────────────────────────────────

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


# ── M-decisive pairs ─────────────────────────────────────────────────────────

M_DECISIVE = []
for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    if a[1] != a[4]:  # L2 ≠ L5
        M_DECISIVE.append(k)


# ══════════════════════════════════════════════════════════════════════════════
# METRIC COMPUTATION
# ══════════════════════════════════════════════════════════════════════════════

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
    """Return (kernel_chi2, canon_asymmetry, m_score, m_total) for orientation."""
    seq = build_sequence(o)

    # 1. Kernel chi²
    freq = Counter()
    for k in range(31):
        name = kernel_name(seq[2*k+1], seq[2*k+2])
        freq[name] += 1
    expected = 31 / 8
    chi2 = sum((freq.get(g, 0) - expected)**2 / expected for g in ALL_GEN_NAMES)

    # 2. Canon asymmetry
    upper_bh = sum(1 for k in range(15) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    lower_bh = sum(1 for k in range(15, 32) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    asym = upper_bh - lower_bh

    # 3. M-component score
    m_score = 0
    for k in M_DECISIVE:
        first_hex = seq[2*k]
        if first_hex[1] == 0:  # L2 = yin
            m_score += 1

    return chi2, asym, m_score, len(M_DECISIVE)


# ══════════════════════════════════════════════════════════════════════════════
# BUILD THE 27 FREE BITS INDEX
# ══════════════════════════════════════════════════════════════════════════════

# Type A: 22 unconstrained pairs (bits 0-21)
# Type B: 5 constraint components (bits 22-26)

free_bits = []

# Type A
for p in FREE_PAIRS:
    free_bits.append({
        'bit_index': len(free_bits),
        'type': 'A',
        'pairs': [p],
        'description': f'pair {p}',
    })

# Type B
for ci, ((p1, p2), valid) in enumerate(COMPONENT_VALID.items()):
    free_bits.append({
        'bit_index': len(free_bits),
        'type': 'B',
        'pairs': [p1, p2],
        'component': (p1, p2),
        'valid_states': valid,
        'description': f'component ({p1},{p2})',
    })

assert len(free_bits) == 27, f"Expected 27 free bits, got {len(free_bits)}"


def make_flipped_orientation(bit_info):
    """Create the orientation vector with one free bit flipped from KW (all zeros)."""
    o = [0] * 32
    if bit_info['type'] == 'A':
        # Flip the single unconstrained pair
        o[bit_info['pairs'][0]] = 1
    else:
        # Switch to the other valid state of the constraint component
        valid = bit_info['valid_states']
        # KW uses state 0 (both pairs = 0), which is valid[0] = (0, 0)
        # Find which valid state is NOT (0, 0)
        kw_state = (0, 0)
        other_state = [s for s in valid if s != kw_state]
        assert len(other_state) == 1, f"Expected 1 other state, got {other_state}"
        p1, p2 = bit_info['pairs']
        o[p1] = other_state[0][0]
        o[p2] = other_state[0][1]
    return o


# ══════════════════════════════════════════════════════════════════════════════
# KW BASELINE
# ══════════════════════════════════════════════════════════════════════════════

KW_O = [0] * 32
KW_CHI2, KW_ASYM, KW_M, KW_M_TOTAL = compute_all_metrics(KW_O)

print("=" * 80)
print("SINGLE-BIT PERTURBATION BASELINE")
print("=" * 80)
print()
print(f"KW baseline:")
print(f"  chi² = {KW_CHI2:.4f}")
print(f"  canon_asym = {KW_ASYM}")
print(f"  m_score = {KW_M}/{KW_M_TOTAL}")
print()
print(f"Free bits: {len(free_bits)}")
print(f"  Type A (unconstrained pairs): {sum(1 for b in free_bits if b['type'] == 'A')}")
print(f"  Type B (constraint components): {sum(1 for b in free_bits if b['type'] == 'B')}")
print()

# Show the constraint component valid states
print("Constraint component valid states:")
for ci, ((p1, p2), valid) in enumerate(COMPONENT_VALID.items()):
    print(f"  ({p1},{p2}): valid = {valid}, KW = (0,0), flip → {[s for s in valid if s != (0,0)][0]}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 1: SINGLE-BIT METRIC PROFILES
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("TABLE 1: SINGLE-BIT METRIC PROFILES")
print("=" * 80)
print()

results = []

header = (f"{'bit':>4s} {'pair(s)':>10s} {'type':>4s} "
          f"{'chi2':>8s} {'Δchi2':>8s} {'asym':>5s} {'Δasym':>6s} "
          f"{'m_sc':>5s} {'Δm':>4s} {'n_imp':>5s} {'n_deg':>5s}")
print(header)
print("─" * len(header))

for bi in free_bits:
    o = make_flipped_orientation(bi)
    assert is_s2_free(o), f"Flipped orientation for bit {bi['bit_index']} is NOT S=2-free!"

    chi2, asym, m_score, m_total = compute_all_metrics(o)

    d_chi2 = chi2 - KW_CHI2
    d_asym = asym - KW_ASYM
    d_m = m_score - KW_M

    # Improvement: chi2 lower is better, asym higher is better, m_score higher is better
    chi2_flag = 'improve' if d_chi2 < 0 else ('degrade' if d_chi2 > 0 else 'neutral')
    asym_flag = 'improve' if d_asym > 0 else ('degrade' if d_asym < 0 else 'neutral')
    m_flag = 'improve' if d_m > 0 else ('degrade' if d_m < 0 else 'neutral')

    flags = [chi2_flag, asym_flag, m_flag]
    n_improve = flags.count('improve')
    n_degrade = flags.count('degrade')

    pairs_str = ','.join(str(p) for p in bi['pairs'])
    print(f"{bi['bit_index']:4d} {pairs_str:>10s} {bi['type']:>4s} "
          f"{chi2:8.3f} {d_chi2:+8.3f} {asym:5d} {d_asym:+6d} "
          f"{m_score:5d} {d_m:+4d} {n_improve:5d} {n_degrade:5d}")

    results.append({
        'bit_index': bi['bit_index'],
        'pairs': bi['pairs'],
        'type': bi['type'],
        'description': bi['description'],
        'chi2': float(chi2),
        'd_chi2': float(d_chi2),
        'asym': int(asym),
        'd_asym': int(d_asym),
        'm_score': int(m_score),
        'd_m': int(d_m),
        'chi2_flag': chi2_flag,
        'asym_flag': asym_flag,
        'm_flag': m_flag,
        'n_improve': n_improve,
        'n_degrade': n_degrade,
    })

print()

# Summary
n_all_improve = sum(1 for r in results if r['n_improve'] == 3)
n_at_least_one_improve = sum(1 for r in results if r['n_improve'] >= 1)
n_at_least_one_degrade = sum(1 for r in results if r['n_degrade'] >= 1)
n_mixed = sum(1 for r in results if r['n_improve'] >= 1 and r['n_degrade'] >= 1)
n_pure_degrade = sum(1 for r in results if r['n_degrade'] >= 1 and r['n_improve'] == 0)

print(f"Summary:")
print(f"  Flips improving all 3 metrics: {n_all_improve}")
print(f"  Flips improving ≥1 metric: {n_at_least_one_improve}")
print(f"  Flips degrading ≥1 metric: {n_at_least_one_degrade}")
print(f"  Mixed (improve some, degrade others): {n_mixed}")
print(f"  Pure degradation (degrade ≥1, improve 0): {n_pure_degrade}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 2: COUPLING ESTIMATES (conditional sampling)
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("TABLE 2: CONDITIONAL COUPLING ESTIMATES (20K per flip)")
print("=" * 80)
print()

# First compute KW-stratum coupling (all bits at KW values = all 0)
N_COUPLING = 20_000

def sample_s2_free_with_fixed(rng, fixed_pairs):
    """Sample S=2-free orientation with certain pairs fixed."""
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        # Apply fixed pairs
        for p, v in fixed_pairs.items():
            o[p] = v
        if is_s2_free(o):
            return o


def compute_coupling(samples_chi2, samples_asym, ref_chi2, ref_asym):
    """Compute coupling ratio from sample arrays."""
    p_chi2 = np.mean(samples_chi2 <= ref_chi2)
    p_asym = np.mean(samples_asym >= ref_asym)
    joint = np.mean((samples_chi2 <= ref_chi2) & (samples_asym >= ref_asym))
    expected = p_chi2 * p_asym
    ratio = joint / expected if expected > 0 else float('inf')
    return p_chi2, p_asym, joint, ratio


# KW baseline coupling (unconditional)
print("Computing KW baseline coupling (20K unconditional)...")
rng_base = random.Random(42)
base_chi2 = np.empty(N_COUPLING)
base_asym = np.empty(N_COUPLING)

for i in range(N_COUPLING):
    o = sample_s2_free_with_fixed(rng_base, {})
    chi2, asym, _, _ = compute_all_metrics(o)
    base_chi2[i] = chi2
    base_asym[i] = asym

kw_p_chi2, kw_p_asym, kw_joint, kw_ratio = compute_coupling(base_chi2, base_asym, KW_CHI2, KW_ASYM)
print(f"  KW baseline: P(χ²≤KW)={kw_p_chi2:.4f}, P(asym≥KW)={kw_p_asym:.4f}, "
      f"P(joint)={kw_joint:.5f}, ratio={kw_ratio:.3f}")
print()

# Per-flip conditional coupling
coupling_results = []

t0 = time.time()
header2 = (f"{'bit':>4s} {'P(χ²≤KW)':>10s} {'P(as≥KW)':>10s} "
           f"{'P(joint)':>10s} {'ratio':>8s} {'Δratio':>8s}")
print(header2)
print("─" * len(header2))

for bi in free_bits:
    rng_flip = random.Random(1000 + bi['bit_index'])

    # Build fixed pairs dict: the flipped bit fixed to its non-KW value
    fixed = {}
    if bi['type'] == 'A':
        fixed[bi['pairs'][0]] = 1
    else:
        valid = bi['valid_states']  # already stored in Type B entries
        other_state = [s for s in valid if s != (0, 0)][0]
        p1, p2 = bi['pairs']
        fixed[p1] = other_state[0]
        fixed[p2] = other_state[1]

    s_chi2 = np.empty(N_COUPLING)
    s_asym = np.empty(N_COUPLING)

    for i in range(N_COUPLING):
        o = sample_s2_free_with_fixed(rng_flip, fixed)
        chi2, asym, _, _ = compute_all_metrics(o)
        s_chi2[i] = chi2
        s_asym[i] = asym

    p_c, p_a, p_j, ratio = compute_coupling(s_chi2, s_asym, KW_CHI2, KW_ASYM)
    d_ratio = ratio - kw_ratio

    print(f"{bi['bit_index']:4d} {p_c:10.4f} {p_a:10.4f} "
          f"{p_j:10.5f} {ratio:8.3f} {d_ratio:+8.3f}")

    coupling_results.append({
        'bit_index': bi['bit_index'],
        'p_chi2': float(p_c),
        'p_asym': float(p_a),
        'p_joint': float(p_j),
        'ratio': float(ratio),
        'd_ratio': float(d_ratio),
    })

t1 = time.time()
print()
print(f"Coupling pass completed in {t1-t0:.1f}s")
print()


# ══════════════════════════════════════════════════════════════════════════════
# TABLE 3: SUMMARY CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("TABLE 3: SUMMARY CLASSIFICATION")
print("=" * 80)
print()

header3 = f"{'bit':>4s} {'pair(s)':>10s} {'type':>4s} {'classification':>25s}"
print(header3)
print("─" * len(header3))

classifications = []
for r, cr in zip(results, coupling_results):
    bi = r['bit_index']
    n_imp = r['n_improve']
    n_deg = r['n_degrade']

    if n_imp == 0 and n_deg == 0:
        cls = 'neutral'
    elif n_imp >= 1 and n_deg == 0:
        cls = 'improves_at_least_one'
    elif n_deg >= 1 and n_imp == 0:
        cls = 'degrades_at_least_one'
    else:
        cls = 'mixed'

    pairs_str = ','.join(str(p) for p in r['pairs'])
    print(f"{bi:4d} {pairs_str:>10s} {r['type']:>4s} {cls:>25s}")

    classifications.append({
        'bit_index': bi,
        'classification': cls,
    })

print()

# Classification counts
from collections import Counter as Cnt
cls_counts = Cnt(c['classification'] for c in classifications)
for cls, count in sorted(cls_counts.items()):
    print(f"  {cls}: {count}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE RAW DATA
# ══════════════════════════════════════════════════════════════════════════════

data = {
    'kw_baseline': {
        'chi2': float(KW_CHI2),
        'asym': int(KW_ASYM),
        'm_score': int(KW_M),
        'm_total': int(KW_M_TOTAL),
        'coupling_ratio': float(kw_ratio),
        'coupling_p_chi2': float(kw_p_chi2),
        'coupling_p_asym': float(kw_p_asym),
        'coupling_p_joint': float(kw_joint),
    },
    'free_bits': [fb.copy() for fb in free_bits],
    'single_bit_metrics': results,
    'coupling_estimates': coupling_results,
    'classifications': classifications,
    'parameters': {
        'n_coupling_samples': N_COUPLING,
        'free_pairs': FREE_PAIRS,
        'components': [list(c) for c in COMPONENTS],
    },
}

# Fix tuples in free_bits for JSON
for fb in data['free_bits']:
    if 'component' in fb:
        fb['component'] = list(fb['component'])
    if 'valid_states' in fb:
        fb['valid_states'] = [list(s) for s in fb['valid_states']]

with open('/home/quasar/nous/logoswen/iter4/round1_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Raw data saved to logoswen/iter4/round1_data.json")
print()
print("=" * 80)
print("SINGLE-BIT PERTURBATION BASELINE COMPLETE")
print("=" * 80)
