"""
Shared infrastructure for iter5 generators.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter
from sequence import all_bits
import numpy as np
import random

# ══════════════════════════════════════════════════════════════════════════════
# CORE DATA
# ══════════════════════════════════════════════════════════════════════════════

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

def hex_to_int(h):
    v = 0
    for bit in h:
        v = v * 2 + bit
    return v

def kernel_3bit(ha, hb):
    m = xor6(ha, hb)
    return (m[5], m[4], m[3])

def kernel_name(ha, hb):
    k3 = kernel_3bit(ha, hb)
    gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
    return VALID_MASKS.get(gen_6, '?')


# ══════════════════════════════════════════════════════════════════════════════
# S=2 CONSTRAINTS
# ══════════════════════════════════════════════════════════════════════════════

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
    CONSTRAINED_PAIRS.add(k + 1)

FREE_PAIRS = sorted(set(range(32)) - CONSTRAINED_PAIRS)
COMPONENTS = [(13, 14), (19, 20), (25, 26), (27, 28), (29, 30)]

COMPONENT_VALID = {}
for p1, p2 in COMPONENTS:
    bridge_k = p1
    if bridge_k in CONSTRAINTS:
        forbidden = CONSTRAINTS[bridge_k]
        valid = [(o1, o2) for o1 in [0, 1] for o2 in [0, 1]
                 if (o1, o2) not in forbidden]
        COMPONENT_VALID[(p1, p2)] = valid


def is_s2_free(o):
    for k, forbidden in CONSTRAINTS.items():
        if (o[k], o[k + 1]) in forbidden:
            return False
    return True


# ── Free bits index ───────────────────────────────────────────────────────────

free_bits = []
for p in FREE_PAIRS:
    free_bits.append({'bit_index': len(free_bits), 'type': 'A', 'pairs': [p]})
for (p1, p2), valid in COMPONENT_VALID.items():
    free_bits.append({'bit_index': len(free_bits), 'type': 'B', 'pairs': [p1, p2],
                      'valid_states': valid})
assert len(free_bits) == 27


# ── M-decisive pairs ─────────────────────────────────────────────────────────

M_DECISIVE = []
for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    if a[1] != a[4]:  # L2 ≠ L5
        M_DECISIVE.append(k)


# ══════════════════════════════════════════════════════════════════════════════
# METRIC FUNCTIONS
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


def compute_chi2(seq):
    freq = Counter()
    for k in range(31):
        name = kernel_name(seq[2*k+1], seq[2*k+2])
        freq[name] += 1
    expected = 31 / 8
    return sum((freq.get(g, 0) - expected)**2 / expected for g in ALL_GEN_NAMES)


def compute_kac(seq):
    kernel_int = []
    for k in range(31):
        name = kernel_name(seq[2*k+1], seq[2*k+2])
        kernel_int.append(ALL_GEN_NAMES.index(name))
    ki = np.array(kernel_int, dtype=float)
    ki = ki - ki.mean()
    var = np.var(kernel_int)
    if var == 0:
        return 0.0
    return float(np.mean(ki[:-1] * ki[1:]) / var)


def compute_asym(seq):
    upper_bh = sum(1 for k in range(15) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    lower_bh = sum(1 for k in range(15, 32) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    return upper_bh - lower_bh


def compute_m_score(seq):
    score = 0
    for k in M_DECISIVE:
        first_hex = seq[2*k]
        if first_hex[1] == 0:
            score += 1
    return score


def compute_all_metrics(o):
    seq = build_sequence(o)
    return {
        'chi2': compute_chi2(seq),
        'asym': compute_asym(seq),
        'm_score': compute_m_score(seq),
        'kac': compute_kac(seq),
    }


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def orientation_str(o):
    return ''.join(str(x) for x in o)


# ══════════════════════════════════════════════════════════════════════════════
# KW BASELINE
# ══════════════════════════════════════════════════════════════════════════════

KW_O = [0] * 32
KW_METRICS = compute_all_metrics(KW_O)
KW_CHI2 = KW_METRICS['chi2']
KW_ASYM = KW_METRICS['asym']
KW_M = KW_METRICS['m_score']
KW_KAC = KW_METRICS['kac']


# ══════════════════════════════════════════════════════════════════════════════
# COMPARISON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def pareto_compare(metrics):
    better = [
        metrics['chi2'] < KW_CHI2 - 1e-9,
        metrics['asym'] > KW_ASYM,
        metrics['m_score'] > KW_M,
        metrics['kac'] < KW_KAC - 1e-9,
    ]
    worse = [
        metrics['chi2'] > KW_CHI2 + 1e-9,
        metrics['asym'] < KW_ASYM,
        metrics['m_score'] < KW_M,
        metrics['kac'] > KW_KAC + 1e-9,
    ]
    if any(better) and not any(worse):
        return 'dominates-kw'
    if any(worse) and not any(better):
        return 'dominated-by-kw'
    if not any(better) and not any(worse):
        return 'equal'
    return 'trade-off'


def per_axis_comparison(metrics):
    axes = []
    for name, kw_val, higher_better in [
        ('chi2', KW_CHI2, False),
        ('asym', KW_ASYM, True),
        ('m_score', KW_M, True),
        ('kac', KW_KAC, False),
    ]:
        val = metrics[name]
        if higher_better:
            if val > kw_val + 1e-9:
                axes.append(f'{name}:better')
            elif val < kw_val - 1e-9:
                axes.append(f'{name}:worse')
            else:
                axes.append(f'{name}:equal')
        else:
            if val < kw_val - 1e-9:
                axes.append(f'{name}:better')
            elif val > kw_val + 1e-9:
                axes.append(f'{name}:worse')
            else:
                axes.append(f'{name}:equal')
    return axes


def report_orientation(name, o, metrics=None):
    """Print a standard report for an orientation."""
    if metrics is None:
        metrics = compute_all_metrics(o)
    axes = per_axis_comparison(metrics)
    pareto = pareto_compare(metrics)
    h = hamming(o, KW_O)
    print(f"  {name}:")
    print(f"    Orientation: {orientation_str(o)}")
    print(f"    chi²={metrics['chi2']:.4f}  asym={metrics['asym']}  "
          f"m_score={metrics['m_score']}/{len(M_DECISIVE)}  kac={metrics['kac']:.4f}")
    print(f"    Hamming from KW: {h}")
    print(f"    Per-axis: {', '.join(axes)}")
    print(f"    Pareto: {pareto}")
    print()
    return {'orientation': list(o), 'metrics': metrics, 'per_axis': axes,
            'pareto': pareto, 'hamming_from_kw': h}


def bridge_kernel_3bit(o, k):
    if o[k] == 0:
        ex = PAIRS[k]['b']
    else:
        ex = PAIRS[k]['a']
    if o[k+1] == 0:
        en = PAIRS[k+1]['a']
    else:
        en = PAIRS[k+1]['b']
    return kernel_3bit(ex, en)


def hamming_3bit(a, b):
    return sum(x != y for x, y in zip(a, b))


def sample_s2_free(rng):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            return o


def json_clean(obj):
    if isinstance(obj, dict):
        return {str(k): json_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [json_clean(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj
