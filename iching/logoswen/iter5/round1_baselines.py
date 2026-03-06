"""
Iter5 Round 1: Baseline Generators

6 generators tested against KW's 4-axis profile:
  A1. Random S=2-free orientation (10K samples)
  A2. All-flipped orientation (complement of KW)
  B1. Greedy χ² minimizer (100 starts)
  B2. Greedy kac minimizer (100 starts)
  C1. M-component rule (semantic)
  C2. Sequential kernel diversity (structural)

Metrics:
  1. Kernel χ² (lower = better)
  2. Canon asymmetry (higher = better)
  3. M-score (higher = better, out of 16 decisive pairs)
  4. Kernel autocorrelation lag-1 (more negative = better)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter
from sequence import all_bits
import random
import numpy as np
import json
import time

# ══════════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE
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
    """Lag-1 autocorrelation of the kernel type sequence."""
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
        if first_hex[1] == 0:  # L2 = yin
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
# RANDOM S=2-FREE SAMPLING
# ══════════════════════════════════════════════════════════════════════════════

def sample_s2_free(rng):
    """Sample a uniformly random S=2-free orientation via rejection."""
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            return o


# ══════════════════════════════════════════════════════════════════════════════
# KW BASELINE
# ══════════════════════════════════════════════════════════════════════════════

KW_O = [0] * 32
KW_METRICS = compute_all_metrics(KW_O)
KW_CHI2 = KW_METRICS['chi2']
KW_ASYM = KW_METRICS['asym']
KW_M = KW_METRICS['m_score']
KW_KAC = KW_METRICS['kac']

print("=" * 80)
print("ITER5 ROUND 1: BASELINE GENERATORS")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}  asym={KW_ASYM}  m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()

# Store all results for JSON output
all_results = {'kw_baseline': KW_METRICS}


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: Pareto comparison to KW
# ══════════════════════════════════════════════════════════════════════════════

def pareto_compare(metrics):
    """Compare to KW. Returns 'dominates-kw', 'dominated-by-kw', or 'trade-off'."""
    # Better means: chi2 lower, asym higher, m_score higher, kac more negative
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
    """Return per-axis comparison string."""
    axes = []
    for name, kw_val, higher_better in [
        ('chi2', KW_CHI2, False),
        ('asym', KW_ASYM, True),
        ('m_score', KW_M, True),
        ('kac', KW_KAC, False),  # more negative = better = lower
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


# ══════════════════════════════════════════════════════════════════════════════
# A1: RANDOM S=2-FREE ORIENTATION (10K samples)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("A1: RANDOM S=2-FREE ORIENTATION (10,000 samples)")
print("─" * 80)
print()

N_RANDOM = 10_000
rng_a1 = random.Random(42)

a1_chi2 = np.empty(N_RANDOM)
a1_asym = np.empty(N_RANDOM)
a1_m = np.empty(N_RANDOM)
a1_kac = np.empty(N_RANDOM)

t0 = time.time()
for i in range(N_RANDOM):
    o = sample_s2_free(rng_a1)
    m = compute_all_metrics(o)
    a1_chi2[i] = m['chi2']
    a1_asym[i] = m['asym']
    a1_m[i] = m['m_score']
    a1_kac[i] = m['kac']
    if (i + 1) % 2000 == 0:
        print(f"  ... {i+1}/{N_RANDOM} ({time.time()-t0:.1f}s)")

t1 = time.time()
print(f"  Sampling complete: {t1-t0:.1f}s")
print()

# Distribution table
def dist_row(name, arr, kw_val, lower_better=True):
    pcts = np.percentile(arr, [5, 50, 95])
    if lower_better:
        rank = np.mean(arr <= kw_val) * 100
    else:
        rank = np.mean(arr >= kw_val) * 100
    return {
        'metric': name,
        'mean': float(np.mean(arr)),
        'std': float(np.std(arr)),
        'min': float(np.min(arr)),
        'max': float(np.max(arr)),
        'p5': float(pcts[0]),
        'p50': float(pcts[1]),
        'p95': float(pcts[2]),
        'kw_val': float(kw_val),
        'kw_percentile': float(rank),
    }

a1_dist = [
    dist_row('chi2', a1_chi2, KW_CHI2, lower_better=True),
    dist_row('asym', a1_asym, KW_ASYM, lower_better=False),
    dist_row('m_score', a1_m, KW_M, lower_better=False),
    dist_row('kac', a1_kac, KW_KAC, lower_better=True),
]

header = f"{'metric':>8s} {'mean':>8s} {'std':>7s} {'min':>8s} {'p5':>8s} {'p50':>8s} {'p95':>8s} {'max':>8s} {'KW':>8s} {'KW%ile':>7s}"
print(header)
print("─" * len(header))
for d in a1_dist:
    print(f"{d['metric']:>8s} {d['mean']:8.3f} {d['std']:7.3f} {d['min']:8.3f} "
          f"{d['p5']:8.3f} {d['p50']:8.3f} {d['p95']:8.3f} {d['max']:8.3f} "
          f"{d['kw_val']:8.3f} {d['kw_percentile']:6.1f}%")
print()

# Best orientations by each axis (track during a second pass? No — we didn't save orientations.
# Re-sample to find best, or just report from distribution. Let's do a focused search.)

# Find Pareto-dominant orientations
n_dominate_kw = 0
n_dominated_by_kw = 0
n_tradeoff = 0
n_equal = 0

for i in range(N_RANDOM):
    m = {'chi2': a1_chi2[i], 'asym': a1_asym[i], 'm_score': a1_m[i], 'kac': a1_kac[i]}
    p = pareto_compare(m)
    if p == 'dominates-kw':
        n_dominate_kw += 1
    elif p == 'dominated-by-kw':
        n_dominated_by_kw += 1
    elif p == 'equal':
        n_equal += 1
    else:
        n_tradeoff += 1

print(f"Pareto comparison to KW across {N_RANDOM} random orientations:")
print(f"  Dominate KW:     {n_dominate_kw:6d} ({100*n_dominate_kw/N_RANDOM:.2f}%)")
print(f"  Dominated by KW: {n_dominated_by_kw:6d} ({100*n_dominated_by_kw/N_RANDOM:.2f}%)")
print(f"  Trade-off:       {n_tradeoff:6d} ({100*n_tradeoff/N_RANDOM:.2f}%)")
print(f"  Equal:           {n_equal:6d} ({100*n_equal/N_RANDOM:.2f}%)")
print()

all_results['A1'] = {
    'distribution': a1_dist,
    'pareto': {
        'dominate_kw': n_dominate_kw,
        'dominated_by_kw': n_dominated_by_kw,
        'tradeoff': n_tradeoff,
        'equal': n_equal,
    },
    'n_samples': N_RANDOM,
}


# ══════════════════════════════════════════════════════════════════════════════
# A2: ALL-FLIPPED ORIENTATION
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("A2: ALL-FLIPPED ORIENTATION")
print("─" * 80)
print()

# All 32 bits flipped
a2_raw = [1] * 32
a2_raw_s2free = is_s2_free(a2_raw)
print(f"All-32-flipped S=2-free: {a2_raw_s2free}")

if not a2_raw_s2free:
    # Find which constraints are violated
    violations = []
    for k, forbidden in CONSTRAINTS.items():
        if (a2_raw[k], a2_raw[k + 1]) in forbidden:
            violations.append(k)
    print(f"  Violated constraints at bridges: {violations}")

    # Flip only the 27 free bits (leave constrained pairs at KW default)
    a2_free = [0] * 32
    for bi in free_bits:
        if bi['type'] == 'A':
            a2_free[bi['pairs'][0]] = 1
        else:
            # For components, use the non-KW valid state
            other = [s for s in bi['valid_states'] if s != (0, 0)][0]
            a2_free[bi['pairs'][0]] = other[0]
            a2_free[bi['pairs'][1]] = other[1]

    a2_free_s2free = is_s2_free(a2_free)
    print(f"  27-free-bits-flipped S=2-free: {a2_free_s2free}")
    a2_o = a2_free
else:
    a2_o = a2_raw

a2_metrics = compute_all_metrics(a2_o)
a2_axes = per_axis_comparison(a2_metrics)
a2_pareto = pareto_compare(a2_metrics)
a2_hamming = hamming(a2_o, KW_O)

print(f"  Orientation: {orientation_str(a2_o)}")
print(f"  chi²={a2_metrics['chi2']:.4f}  asym={a2_metrics['asym']}  "
      f"m_score={a2_metrics['m_score']}/{len(M_DECISIVE)}  kac={a2_metrics['kac']:.4f}")
print(f"  Hamming from KW: {a2_hamming}")
print(f"  Per-axis: {', '.join(a2_axes)}")
print(f"  Pareto: {a2_pareto}")
print()

all_results['A2'] = {
    'orientation': a2_o,
    'metrics': a2_metrics,
    'per_axis': a2_axes,
    'pareto': a2_pareto,
    'hamming_from_kw': a2_hamming,
    'raw_all32_s2free': a2_raw_s2free,
}


# ══════════════════════════════════════════════════════════════════════════════
# B1: GREEDY χ² MINIMIZER (100 random starts)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("B1: GREEDY χ² MINIMIZER (100 random starts)")
print("─" * 80)
print()

N_GREEDY = 100

def greedy_optimize(start_o, metric_fn, rng):
    """Greedy hill-climb by flipping free bits one at a time.
    metric_fn(o) returns the value to minimize."""
    o = list(start_o)
    val = metric_fn(o)
    improved = True
    while improved:
        improved = False
        # Shuffle bit order for tie-breaking randomness
        indices = list(range(27))
        rng.shuffle(indices)
        for bi_idx in indices:
            bi = free_bits[bi_idx]
            # Save current state
            if bi['type'] == 'A':
                p = bi['pairs'][0]
                old_val = o[p]
                o[p] = 1 - old_val
            else:
                p1, p2 = bi['pairs']
                old_vals = (o[p1], o[p2])
                # Toggle to the other valid state
                cur = (o[p1], o[p2])
                other = [s for s in bi['valid_states'] if s != cur]
                if not other:
                    continue
                o[p1], o[p2] = other[0]

            if is_s2_free(o):
                new_val = metric_fn(o)
                if new_val < val - 1e-12:
                    val = new_val
                    improved = True
                    continue  # keep the flip
            # Revert
            if bi['type'] == 'A':
                o[p] = old_val
            else:
                o[p1], o[p2] = old_vals
    return o, val


t0 = time.time()
b1_results = []
for trial in range(N_GREEDY):
    rng_b1 = random.Random(7000 + trial)
    start = sample_s2_free(rng_b1)
    def chi2_fn(o):
        return compute_chi2(build_sequence(o))
    final_o, final_chi2 = greedy_optimize(start, chi2_fn, rng_b1)
    final_metrics = compute_all_metrics(final_o)
    b1_results.append({'o': list(final_o), 'metrics': final_metrics})
    if (trial + 1) % 20 == 0:
        print(f"  ... {trial+1}/{N_GREEDY} ({time.time()-t0:.1f}s)")

t1 = time.time()
print(f"  Greedy χ² complete: {t1-t0:.1f}s")
print()

# Distribution
b1_chi2 = np.array([r['metrics']['chi2'] for r in b1_results])
b1_asym = np.array([r['metrics']['asym'] for r in b1_results])
b1_m = np.array([r['metrics']['m_score'] for r in b1_results])
b1_kac = np.array([r['metrics']['kac'] for r in b1_results])

b1_dist = [
    dist_row('chi2', b1_chi2, KW_CHI2, lower_better=True),
    dist_row('asym', b1_asym, KW_ASYM, lower_better=False),
    dist_row('m_score', b1_m, KW_M, lower_better=False),
    dist_row('kac', b1_kac, KW_KAC, lower_better=True),
]

print(header)
print("─" * len(header))
for d in b1_dist:
    print(f"{d['metric']:>8s} {d['mean']:8.3f} {d['std']:7.3f} {d['min']:8.3f} "
          f"{d['p5']:8.3f} {d['p50']:8.3f} {d['p95']:8.3f} {d['max']:8.3f} "
          f"{d['kw_val']:8.3f} {d['kw_percentile']:6.1f}%")
print()

# Best by χ²
best_b1_idx = int(np.argmin(b1_chi2))
best_b1 = b1_results[best_b1_idx]
best_b1_axes = per_axis_comparison(best_b1['metrics'])
best_b1_pareto = pareto_compare(best_b1['metrics'])
print(f"Best χ² orientation:")
print(f"  Orientation: {orientation_str(best_b1['o'])}")
print(f"  chi²={best_b1['metrics']['chi2']:.4f}  asym={best_b1['metrics']['asym']}  "
      f"m_score={best_b1['metrics']['m_score']}/{len(M_DECISIVE)}  kac={best_b1['metrics']['kac']:.4f}")
print(f"  Hamming from KW: {hamming(best_b1['o'], KW_O)}")
print(f"  Per-axis: {', '.join(best_b1_axes)}")
print(f"  Pareto: {best_b1_pareto}")
print()

# Pareto summary
b1_pareto_counts = Counter()
for r in b1_results:
    b1_pareto_counts[pareto_compare(r['metrics'])] += 1
print(f"Pareto summary across {N_GREEDY} greedy χ² runs:")
for cls in ['dominates-kw', 'dominated-by-kw', 'trade-off', 'equal']:
    print(f"  {cls}: {b1_pareto_counts.get(cls, 0)}")
print()

all_results['B1'] = {
    'distribution': b1_dist,
    'best_orientation': best_b1['o'],
    'best_metrics': best_b1['metrics'],
    'best_per_axis': best_b1_axes,
    'best_pareto': best_b1_pareto,
    'best_hamming': hamming(best_b1['o'], KW_O),
    'pareto_counts': dict(b1_pareto_counts),
    'n_starts': N_GREEDY,
}


# ══════════════════════════════════════════════════════════════════════════════
# B2: GREEDY kac MINIMIZER (100 random starts)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("B2: GREEDY kac MINIMIZER (100 random starts)")
print("─" * 80)
print()

t0 = time.time()
b2_results = []
for trial in range(N_GREEDY):
    rng_b2 = random.Random(8000 + trial)
    start = sample_s2_free(rng_b2)
    def kac_fn(o):
        return compute_kac(build_sequence(o))
    final_o, final_kac = greedy_optimize(start, kac_fn, rng_b2)
    final_metrics = compute_all_metrics(final_o)
    b2_results.append({'o': list(final_o), 'metrics': final_metrics})
    if (trial + 1) % 20 == 0:
        print(f"  ... {trial+1}/{N_GREEDY} ({time.time()-t0:.1f}s)")

t1 = time.time()
print(f"  Greedy kac complete: {t1-t0:.1f}s")
print()

b2_chi2 = np.array([r['metrics']['chi2'] for r in b2_results])
b2_asym = np.array([r['metrics']['asym'] for r in b2_results])
b2_m = np.array([r['metrics']['m_score'] for r in b2_results])
b2_kac = np.array([r['metrics']['kac'] for r in b2_results])

b2_dist = [
    dist_row('chi2', b2_chi2, KW_CHI2, lower_better=True),
    dist_row('asym', b2_asym, KW_ASYM, lower_better=False),
    dist_row('m_score', b2_m, KW_M, lower_better=False),
    dist_row('kac', b2_kac, KW_KAC, lower_better=True),
]

print(header)
print("─" * len(header))
for d in b2_dist:
    print(f"{d['metric']:>8s} {d['mean']:8.3f} {d['std']:7.3f} {d['min']:8.3f} "
          f"{d['p5']:8.3f} {d['p50']:8.3f} {d['p95']:8.3f} {d['max']:8.3f} "
          f"{d['kw_val']:8.3f} {d['kw_percentile']:6.1f}%")
print()

# Best by kac
best_b2_idx = int(np.argmin(b2_kac))
best_b2 = b2_results[best_b2_idx]
best_b2_axes = per_axis_comparison(best_b2['metrics'])
best_b2_pareto = pareto_compare(best_b2['metrics'])
print(f"Best kac orientation:")
print(f"  Orientation: {orientation_str(best_b2['o'])}")
print(f"  chi²={best_b2['metrics']['chi2']:.4f}  asym={best_b2['metrics']['asym']}  "
      f"m_score={best_b2['metrics']['m_score']}/{len(M_DECISIVE)}  kac={best_b2['metrics']['kac']:.4f}")
print(f"  Hamming from KW: {hamming(best_b2['o'], KW_O)}")
print(f"  Per-axis: {', '.join(best_b2_axes)}")
print(f"  Pareto: {best_b2_pareto}")
print()

b2_pareto_counts = Counter()
for r in b2_results:
    b2_pareto_counts[pareto_compare(r['metrics'])] += 1
print(f"Pareto summary across {N_GREEDY} greedy kac runs:")
for cls in ['dominates-kw', 'dominated-by-kw', 'trade-off', 'equal']:
    print(f"  {cls}: {b2_pareto_counts.get(cls, 0)}")
print()

all_results['B2'] = {
    'distribution': b2_dist,
    'best_orientation': best_b2['o'],
    'best_metrics': best_b2['metrics'],
    'best_per_axis': best_b2_axes,
    'best_pareto': best_b2_pareto,
    'best_hamming': hamming(best_b2['o'], KW_O),
    'pareto_counts': dict(b2_pareto_counts),
    'n_starts': N_GREEDY,
}


# ══════════════════════════════════════════════════════════════════════════════
# C1: M-COMPONENT RULE
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("C1: M-COMPONENT RULE")
print("─" * 80)
print()

# Rule: For each pair, orient so that L2=yin comes first (when L2≠L5).
# For M-indecisive pairs (L2=L5), default to binary-high-first.

c1_o = [0] * 32
for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    if a[1] != a[4]:  # M-decisive (L2 ≠ L5)
        # Orient so L2=yin (L2=0) comes first
        if a[1] == 0:  # a has L2=yin
            c1_o[k] = 0  # a first
        else:  # b has L2=yin
            c1_o[k] = 1  # b first
    else:  # M-indecisive
        # Default: binary-high-first
        if hex_to_int(a) >= hex_to_int(b):
            c1_o[k] = 0  # a first (already high)
        else:
            c1_o[k] = 1  # b first

c1_s2free = is_s2_free(c1_o)
print(f"C1 raw orientation S=2-free: {c1_s2free}")
print(f"  Orientation: {orientation_str(c1_o)}")

if not c1_s2free:
    # Find violations and make nearest S=2-free variant
    violations = []
    for k, forbidden in CONSTRAINTS.items():
        if (c1_o[k], c1_o[k + 1]) in forbidden:
            violations.append(k)
    print(f"  Violated constraints at bridges: {violations}")

    # Greedy fix: for each violation, flip the bit that affects fewer other constraints
    c1_fixed = list(c1_o)
    for v_k in violations:
        if (c1_fixed[v_k], c1_fixed[v_k + 1]) in CONSTRAINTS.get(v_k, set()):
            # Try flipping v_k
            c1_try_k = list(c1_fixed)
            c1_try_k[v_k] = 1 - c1_try_k[v_k]
            # Try flipping v_k+1
            c1_try_k1 = list(c1_fixed)
            c1_try_k1[v_k + 1] = 1 - c1_try_k1[v_k + 1]
            # Pick whichever introduces fewer new violations
            v1 = sum(1 for kk, forb in CONSTRAINTS.items() if (c1_try_k[kk], c1_try_k[kk+1]) in forb)
            v2 = sum(1 for kk, forb in CONSTRAINTS.items() if (c1_try_k1[kk], c1_try_k1[kk+1]) in forb)
            if v1 <= v2:
                c1_fixed = c1_try_k
            else:
                c1_fixed = c1_try_k1

    c1_fixed_s2free = is_s2_free(c1_fixed)
    print(f"  Fixed orientation S=2-free: {c1_fixed_s2free}")
    if not c1_fixed_s2free:
        # Brute force fix: try all minimal edits
        print("  Brute-force fix needed...")
        best_fix = None
        best_fix_dist = 33
        # Try flipping each subset of violating+adjacent bits
        for mask in range(1, 2**32):
            if bin(mask).count('1') >= best_fix_dist:
                continue
            candidate = [c1_o[i] ^ ((mask >> i) & 1) for i in range(32)]
            if is_s2_free(candidate):
                d = hamming(candidate, c1_o)
                if d < best_fix_dist:
                    best_fix = candidate
                    best_fix_dist = d
        if best_fix:
            c1_fixed = best_fix
            print(f"  Best fix: {best_fix_dist} bits flipped")
    c1_o_final = c1_fixed
    c1_hamming_raw = hamming(c1_o, c1_o_final)
    print(f"  Bits changed for S=2 compliance: {c1_hamming_raw}")
else:
    c1_o_final = c1_o

c1_metrics = compute_all_metrics(c1_o_final)
c1_axes = per_axis_comparison(c1_metrics)
c1_pareto = pareto_compare(c1_metrics)
c1_hamming = hamming(c1_o_final, KW_O)

print(f"  Final orientation: {orientation_str(c1_o_final)}")
print(f"  chi²={c1_metrics['chi2']:.4f}  asym={c1_metrics['asym']}  "
      f"m_score={c1_metrics['m_score']}/{len(M_DECISIVE)}  kac={c1_metrics['kac']:.4f}")
print(f"  Hamming from KW: {c1_hamming}")
print(f"  Per-axis: {', '.join(c1_axes)}")
print(f"  Pareto: {c1_pareto}")
print()

all_results['C1'] = {
    'raw_orientation': list(c1_o),
    'raw_s2free': c1_s2free,
    'orientation': list(c1_o_final),
    'metrics': c1_metrics,
    'per_axis': c1_axes,
    'pareto': c1_pareto,
    'hamming_from_kw': c1_hamming,
}


# ══════════════════════════════════════════════════════════════════════════════
# C2: SEQUENTIAL KERNEL DIVERSITY
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("C2: SEQUENTIAL KERNEL DIVERSITY")
print("─" * 80)
print()

# Process pairs in sequence order. For each pair, choose orientation that
# makes next bridge kernel maximally different from previous bridge kernel.
# Bridge k connects pair k to pair k+1 (exit of pair k → entry of pair k+1).
# Bridge kernel = kernel_name(seq[2k+1], seq[2k+2]).

def bridge_kernel_3bit(o, k):
    """Compute the 3-bit kernel code at bridge k (between pairs k and k+1)."""
    # Exit of pair k
    if o[k] == 0:
        ex = PAIRS[k]['b']
    else:
        ex = PAIRS[k]['a']
    # Entry of pair k+1
    if o[k+1] == 0:
        en = PAIRS[k+1]['a']
    else:
        en = PAIRS[k+1]['b']
    return kernel_3bit(ex, en)


def hamming_3bit(a, b):
    return sum(x != y for x, y in zip(a, b))


# Build greedily: process pairs 0..31, choosing orientation to maximize
# kernel Hamming distance at the bridge.

c2_o = [0] * 32
kernel_counts = Counter()  # for tie-breaking

# Pair 0: no previous bridge, default to 0
# The first bridge is bridge 0 (between pair 0 and pair 1)
# We need to decide pair 0 first (it affects bridge 0), but bridge 0 also
# depends on pair 1. So we process forward:
# - For pair 0, no choice criterion yet (no bridge before it). Default to 0.
# - For pair k (k≥1), we know bridge k-1's kernel (depends on pair k-1 exit
#   and pair k entry). We choose o[k] to maximize Hamming distance between
#   bridge k-1 and bridge k.

# Wait — bridge k-1 depends on o[k] (it's the entry of pair k).
# And bridge k depends on o[k] (it's the exit of pair k) AND o[k+1].
# So choosing o[k] affects BOTH bridge k-1 and bridge k.

# Let's re-think: process sequentially. At step k, we choose o[k].
# This determines bridge k-1 (fully, since o[k-1] is already set).
# We want bridge k-1 to be maximally different from bridge k-2.

# For k=0: no bridge to compare. Default to 0.
# For k=1: bridge 0 depends on o[0] and o[1]. o[0] is set.
#   Choose o[1] to... but we don't have bridge -1. Still no comparison.
#   Actually, bridge 0 is the first bridge. Choose o[1] to maximize diversity
#   of bridge 0 (not much to compare to). Let's say: for k≥1, choosing o[k]
#   determines bridge k-1. We want bridge k-1 different from bridge k-2.
#   Bridge k-2 is fully determined (o[k-2] and o[k-1] already set).

# So:
# k=0: set o[0]=0 (arbitrary)
# k=1: set o[1] — determines bridge 0. No previous bridge. Choose to minimize
#       frequency of kernel type (break ties: prefer higher Hamming from most common).
#       Actually, for first bridge, let's just try both and pick one with less-seen kernel.
# k≥2: set o[k] — determines bridge k-1. Compare to bridge k-2 (known).
#       Choose o[k] that maximizes hamming_3bit(bridge_k-1, bridge_k-2).
#       Tie-break: prefer kernel not yet seen (or seen least).

c2_o[0] = 0  # arbitrary start

for k in range(1, 32):
    best_choice = None
    best_score = None

    for choice in [0, 1]:
        c2_o[k] = choice

        # Check S=2 constraint at bridge k-1
        if k - 1 in CONSTRAINTS and (c2_o[k-1], c2_o[k]) in CONSTRAINTS[k-1]:
            continue  # invalid

        # Compute bridge k-1 kernel
        bk_prev = bridge_kernel_3bit(c2_o, k - 1)

        if k >= 2:
            # Compare to bridge k-2
            bk_prev2 = bridge_kernel_3bit(c2_o, k - 2)
            hdist = hamming_3bit(bk_prev, bk_prev2)
        else:
            hdist = 0  # no comparison for first bridge

        count = kernel_counts.get(bk_prev, 0)
        # Score: primary = Hamming distance, secondary = prefer least-seen kernel
        score = (hdist, -count)

        if best_score is None or score > best_score:
            best_score = score
            best_choice = choice

    if best_choice is None:
        # Both violate S=2? Shouldn't happen. Default to 0.
        print(f"  WARNING: no valid choice for pair {k}, defaulting to 0")
        best_choice = 0

    c2_o[k] = best_choice
    bk = bridge_kernel_3bit(c2_o, k - 1)
    kernel_counts[bk] += 1

c2_s2free = is_s2_free(c2_o)
print(f"C2 orientation S=2-free: {c2_s2free}")

if not c2_s2free:
    violations = []
    for k, forbidden in CONSTRAINTS.items():
        if (c2_o[k], c2_o[k + 1]) in forbidden:
            violations.append(k)
    print(f"  Violated constraints at bridges: {violations}")
    print("  ERROR: C2 algorithm should not produce S=2 violations")

c2_metrics = compute_all_metrics(c2_o)
c2_axes = per_axis_comparison(c2_metrics)
c2_pareto = pareto_compare(c2_metrics)
c2_hamming = hamming(c2_o, KW_O)

print(f"  Orientation: {orientation_str(c2_o)}")
print(f"  chi²={c2_metrics['chi2']:.4f}  asym={c2_metrics['asym']}  "
      f"m_score={c2_metrics['m_score']}/{len(M_DECISIVE)}  kac={c2_metrics['kac']:.4f}")
print(f"  Hamming from KW: {c2_hamming}")
print(f"  Per-axis: {', '.join(c2_axes)}")
print(f"  Pareto: {c2_pareto}")
print()

# Also show kernel distribution
c2_seq = build_sequence(c2_o)
c2_kernel_freq = Counter()
for k in range(31):
    name = kernel_name(c2_seq[2*k+1], c2_seq[2*k+2])
    c2_kernel_freq[name] += 1
print(f"  Kernel distribution: {dict(sorted(c2_kernel_freq.items()))}")
print()

all_results['C2'] = {
    'orientation': list(c2_o),
    'metrics': c2_metrics,
    'per_axis': c2_axes,
    'pareto': c2_pareto,
    'hamming_from_kw': c2_hamming,
    'kernel_distribution': dict(c2_kernel_freq),
}


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("SUMMARY: ALL GENERATORS vs KW")
print("=" * 80)
print()

summary_header = f"{'Generator':>12s} {'chi²':>8s} {'asym':>6s} {'m_score':>8s} {'kac':>8s} {'Hamming':>8s} {'Pareto':>18s}"
print(summary_header)
print("─" * len(summary_header))

# KW
print(f"{'KW':>12s} {KW_CHI2:8.3f} {KW_ASYM:6d} {KW_M:8d} {KW_KAC:8.4f} {'0':>8s} {'reference':>18s}")

# A1 (median)
a1_med = {
    'chi2': float(np.median(a1_chi2)),
    'asym': float(np.median(a1_asym)),
    'm_score': float(np.median(a1_m)),
    'kac': float(np.median(a1_kac)),
}
print(f"{'A1 (median)':>12s} {a1_med['chi2']:8.3f} {a1_med['asym']:6.0f} {a1_med['m_score']:8.0f} "
      f"{a1_med['kac']:8.4f} {'~16':>8s} {'(distribution)':>18s}")

# A2
print(f"{'A2':>12s} {a2_metrics['chi2']:8.3f} {a2_metrics['asym']:6d} {a2_metrics['m_score']:8d} "
      f"{a2_metrics['kac']:8.4f} {a2_hamming:8d} {a2_pareto:>18s}")

# B1 best
print(f"{'B1 (best)':>12s} {best_b1['metrics']['chi2']:8.3f} {best_b1['metrics']['asym']:6d} "
      f"{best_b1['metrics']['m_score']:8d} {best_b1['metrics']['kac']:8.4f} "
      f"{hamming(best_b1['o'], KW_O):8d} {best_b1_pareto:>18s}")

# B2 best
print(f"{'B2 (best)':>12s} {best_b2['metrics']['chi2']:8.3f} {best_b2['metrics']['asym']:6d} "
      f"{best_b2['metrics']['m_score']:8d} {best_b2['metrics']['kac']:8.4f} "
      f"{hamming(best_b2['o'], KW_O):8d} {best_b2_pareto:>18s}")

# C1
print(f"{'C1':>12s} {c1_metrics['chi2']:8.3f} {c1_metrics['asym']:6d} {c1_metrics['m_score']:8d} "
      f"{c1_metrics['kac']:8.4f} {c1_hamming:8d} {c1_pareto:>18s}")

# C2
print(f"{'C2':>12s} {c2_metrics['chi2']:8.3f} {c2_metrics['asym']:6d} {c2_metrics['m_score']:8d} "
      f"{c2_metrics['kac']:8.4f} {c2_hamming:8d} {c2_pareto:>18s}")

print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════════════════════════════

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

with open('/home/quasar/nous/logoswen/iter5/round1_data.json', 'w') as f:
    json.dump(json_clean(all_results), f, indent=2)

print("Data saved to logoswen/iter5/round1_data.json")
print()
print("=" * 80)
print("ROUND 1 COMPLETE")
print("=" * 80)
