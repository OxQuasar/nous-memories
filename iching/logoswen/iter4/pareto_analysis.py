"""
Round 4: The Pareto Frontier Test

Experiments:
  1. kernel_autocorr_1 gradient (all 27 single-bit flips)
  2. Additivity test (20 random 2-bit combos)
  3. Joint Pareto test for pure-improvement 2-bit combos
  4. Weight-ordering sensitivity (all 27 bits)

All computations are deterministic — no sampling needed.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter
from sequence import all_bits
import random
import numpy as np
import json

# ══════════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE (from rounds 1–3)
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

# Free bits index
free_bits = []
for p in FREE_PAIRS:
    free_bits.append({'bit_index': len(free_bits), 'type': 'A', 'pairs': [p],
                      'description': f'pair {p}'})
for (p1, p2), valid in COMPONENT_VALID.items():
    free_bits.append({'bit_index': len(free_bits), 'type': 'B', 'pairs': [p1, p2],
                      'valid_states': valid, 'description': f'component ({p1},{p2})'})
assert len(free_bits) == 27


def apply_bits(bit_indices):
    o = [0] * 32
    for bi_idx in bit_indices:
        bi = free_bits[bi_idx]
        if bi['type'] == 'A':
            o[bi['pairs'][0]] = 1
        else:
            other = [s for s in bi['valid_states'] if s != (0, 0)][0]
            o[bi['pairs'][0]] = other[0]
            o[bi['pairs'][1]] = other[1]
    return o


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


# ══════════════════════════════════════════════════════════════════════════════
# METRIC FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def compute_chi2(seq):
    freq = Counter()
    for k in range(31):
        m = xor6(seq[2*k+1], seq[2*k+2])
        k3 = (m[5], m[4], m[3])
        gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
        freq[VALID_MASKS.get(gen_6, '?')] += 1
    expected = 31 / 8
    return sum((freq.get(g, 0) - expected)**2 / expected for g in ALL_GEN_NAMES)


def compute_kernel_autocorr(seq):
    """Lag-1 autocorrelation of the kernel type sequence (encoded as integers)."""
    kernel_int = []
    for k in range(31):
        m = xor6(seq[2*k+1], seq[2*k+2])
        k3 = (m[5], m[4], m[3])
        gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
        name = VALID_MASKS.get(gen_6, '?')
        kernel_int.append(ALL_GEN_NAMES.index(name))
    ki = np.array(kernel_int, dtype=float)
    ki = ki - ki.mean()
    var = np.var(kernel_int)
    if var == 0:
        return 0.0
    return float(np.mean(ki[:-1] * ki[1:]) / var)


def compute_weight_ordering_bias(seq):
    """n_first_heavier - n_first_lighter across all 32 pairs."""
    heavier = 0
    lighter = 0
    for k in range(N_PAIRS):
        w1 = sum(seq[2*k])
        w2 = sum(seq[2*k+1])
        if w1 > w2:
            heavier += 1
        elif w1 < w2:
            lighter += 1
    return heavier - lighter


# ══════════════════════════════════════════════════════════════════════════════
# LOAD ROUND 1 DATA
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter4/round1_data.json') as f:
    r1 = json.load(f)

KW_CHI2 = r1['kw_baseline']['chi2']
R1_CHI2 = {r['bit_index']: r['chi2'] for r in r1['single_bit_metrics']}
R1_DCHI2 = {r['bit_index']: r['d_chi2'] for r in r1['single_bit_metrics']}

# KW baseline
KW_O = [0] * 32
KW_SEQ = build_sequence(KW_O)
KW_KAC = compute_kernel_autocorr(KW_SEQ)
KW_WOB = compute_weight_ordering_bias(KW_SEQ)

print("=" * 80)
print("ROUND 4: THE PARETO FRONTIER TEST")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}  kernel_autocorr_1={KW_KAC:.4f}  weight_bias={KW_WOB}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 1: kernel_autocorr_1 gradient (all 27 single-bit flips)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 1: kernel_autocorr_1 gradient — all 27 single-bit flips")
print("─" * 80)
print()

exp1_results = []

header = (f"{'bit':>4s} {'pair(s)':>8s} {'kac':>8s} {'Δkac':>8s} "
          f"{'chi2':>8s} {'Δchi2':>8s} {'pareto':>15s}")
print(header)
print("─" * len(header))

for bi in free_bits:
    idx = bi['bit_index']
    o = apply_bits([idx])
    seq = build_sequence(o)
    kac = compute_kernel_autocorr(seq)
    d_kac = kac - KW_KAC
    chi2 = R1_CHI2[idx]
    d_chi2 = R1_DCHI2[idx]

    # Pareto classification on {chi², kernel_autocorr}
    # Lower chi² is better, more negative kernel_autocorr is better
    chi2_better = d_chi2 < -1e-9
    chi2_worse = d_chi2 > 1e-9
    chi2_equal = abs(d_chi2) < 1e-9
    kac_better = d_kac < -1e-9     # more negative = more anti-correlated = better
    kac_worse = d_kac > 1e-9
    kac_equal = abs(d_kac) < 1e-9

    if chi2_better and not kac_worse:
        pareto = 'cone-escape'
    elif kac_better and not chi2_worse:
        pareto = 'cone-escape'
    elif chi2_worse and kac_worse:
        pareto = 'double-degrade'
    elif (chi2_worse or chi2_equal) and (kac_worse or kac_equal):
        pareto = 'KW-dominated'
    elif (chi2_better or chi2_equal) and (kac_better or kac_equal):
        pareto = 'cone-escape'
    else:
        pareto = 'trade-off'

    pairs_str = ','.join(str(p) for p in bi['pairs'])
    print(f"{idx:4d} {pairs_str:>8s} {kac:8.4f} {d_kac:+8.4f} "
          f"{chi2:8.4f} {d_chi2:+8.4f} {pareto:>15s}")

    exp1_results.append({
        'bit_index': idx,
        'pairs': bi['pairs'],
        'type': bi['type'],
        'description': bi['description'],
        'kernel_autocorr_1': float(kac),
        'd_kac': float(d_kac),
        'chi2': float(chi2),
        'd_chi2': float(d_chi2),
        'pareto': pareto,
    })

print()

# Summary counts
pareto_counts = Counter(r['pareto'] for r in exp1_results)
print("Pareto classification summary:")
for cls in ['cone-escape', 'trade-off', 'KW-dominated', 'double-degrade']:
    count = pareto_counts.get(cls, 0)
    bits = [r['bit_index'] for r in exp1_results if r['pareto'] == cls]
    print(f"  {cls:>15s}: {count:2d}  — bits {bits}")
print()

# List cone-escape details if any
cone_escapes = [r for r in exp1_results if r['pareto'] == 'cone-escape']
if cone_escapes:
    print("** CONE ESCAPES FOUND **")
    for r in cone_escapes:
        print(f"  bit {r['bit_index']} ({r['description']}): "
              f"chi²={r['chi2']:.4f} (Δ={r['d_chi2']:+.4f})  "
              f"kac={r['kernel_autocorr_1']:.4f} (Δ={r['d_kac']:+.4f})")
else:
    print("** NO CONE ESCAPES — KW is on the Pareto frontier of {chi², kernel_autocorr_1} **")
print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 2: Additivity test (20 random 2-bit combos)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 2: kernel_autocorr_1 additivity test — 20 random 2-bit combos")
print("─" * 80)
print()

# Single-bit kac deltas
R1_DKAC = {r['bit_index']: r['d_kac'] for r in exp1_results}

rng = random.Random(9999)
pairs_done = set()
exp2_results = []

while len(exp2_results) < 20:
    b1 = rng.randint(0, 26)
    b2 = rng.randint(0, 26)
    if b1 == b2:
        continue
    pair_key = tuple(sorted([b1, b2]))
    if pair_key in pairs_done:
        continue
    pairs_done.add(pair_key)

    o = apply_bits(list(pair_key))
    if not is_s2_free(o):
        continue

    seq = build_sequence(o)
    kac = compute_kernel_autocorr(seq)
    d_kac = kac - KW_KAC
    expected_kac = KW_KAC + R1_DKAC[pair_key[0]] + R1_DKAC[pair_key[1]]
    int_kac = kac - expected_kac

    # Also get chi² for comparison
    chi2 = compute_chi2(seq)
    exp_chi2 = KW_CHI2 + R1_DCHI2[pair_key[0]] + R1_DCHI2[pair_key[1]]
    int_chi2 = chi2 - exp_chi2

    exp2_results.append({
        'bits': list(pair_key),
        'kac': float(kac),
        'd_kac': float(d_kac),
        'exp_kac': float(expected_kac),
        'int_kac': float(int_kac),
        'chi2': float(chi2),
        'int_chi2': float(int_chi2),
    })

header2 = (f"{'b1':>3s} {'b2':>3s} {'kac':>8s} {'exp_kac':>8s} {'int_kac':>8s} "
           f"{'chi2':>8s} {'int_chi2':>8s}")
print(header2)
print("─" * len(header2))

for r in exp2_results:
    print(f"{r['bits'][0]:3d} {r['bits'][1]:3d} {r['kac']:8.4f} {r['exp_kac']:8.4f} "
          f"{r['int_kac']:+8.4f} {r['chi2']:8.4f} {r['int_chi2']:+8.4f}")

print()

# Statistics
int_kac_vals = [r['int_kac'] for r in exp2_results]
abs_int_kac = [abs(v) for v in int_kac_vals]
int_chi2_vals = [r['int_chi2'] for r in exp2_results]
abs_int_chi2 = [abs(v) for v in int_chi2_vals]

# Nonlinearity coefficient for kac
nl_kac_vals = []
for r in exp2_results:
    sum_d = R1_DKAC[r['bits'][0]] + R1_DKAC[r['bits'][1]]
    if abs(sum_d) > 1e-9:
        nl_kac_vals.append(abs(r['int_kac']) / abs(sum_d))

print(f"kernel_autocorr_1 interaction statistics:")
print(f"  Mean int:     {np.mean(int_kac_vals):+.4f}")
print(f"  Mean |int|:   {np.mean(abs_int_kac):.4f}")
print(f"  Max |int|:    {np.max(abs_int_kac):.4f}")
print(f"  Fraction zero: {sum(1 for v in int_kac_vals if abs(v) < 1e-9) / len(int_kac_vals):.3f}")
if nl_kac_vals:
    print(f"  Nonlinearity coeff: mean={np.mean(nl_kac_vals):.3f} median={np.median(nl_kac_vals):.3f}")
print()

print(f"chi² interaction statistics (same combos):")
print(f"  Mean int:     {np.mean(int_chi2_vals):+.4f}")
print(f"  Mean |int|:   {np.mean(abs_int_chi2):.4f}")
print(f"  Fraction zero: {sum(1 for v in int_chi2_vals if abs(v) < 1e-9) / len(int_chi2_vals):.3f}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 3: Joint Pareto test for pure-improvement 2-bit combos
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 3: Pareto test — 15 pure-improvement 2-bit combos + {10,17}")
print("─" * 80)
print()

# The 15 pure-improvement combos from round 2
pure_combos = [
    [3, 10], [4, 10], [5, 10], [9, 10], [10, 15], [10, 26],
    [0, 17], [2, 17], [3, 17], [4, 17], [5, 17], [9, 17],
    [11, 17], [15, 17], [17, 22],
]

# Add {10, 17} explicitly
if [10, 17] not in pure_combos:
    pure_combos.append([10, 17])

exp3_results = []

header3 = (f"{'bits':>8s} {'pairs':>10s} {'chi2':>8s} {'Δchi2':>8s} "
           f"{'kac':>8s} {'Δkac':>8s} {'pareto':>15s}")
print(header3)
print("─" * len(header3))

for combo in pure_combos:
    o = apply_bits(combo)
    assert is_s2_free(o)
    seq = build_sequence(o)
    chi2 = compute_chi2(seq)
    kac = compute_kernel_autocorr(seq)
    d_chi2 = chi2 - KW_CHI2
    d_kac = kac - KW_KAC

    # Pareto classification
    chi2_better = d_chi2 < -1e-9
    chi2_worse = d_chi2 > 1e-9
    kac_better = d_kac < -1e-9
    kac_worse = d_kac > 1e-9

    if chi2_better and not kac_worse:
        pareto = 'cone-escape'
    elif kac_better and not chi2_worse:
        pareto = 'cone-escape'
    elif chi2_worse and kac_worse:
        pareto = 'double-degrade'
    elif chi2_better and kac_worse:
        pareto = 'trade-off'
    elif chi2_worse and kac_better:
        pareto = 'trade-off'
    else:
        pareto = 'KW-dominated'

    pair_strs = []
    for b in combo:
        pair_strs.append(','.join(str(p) for p in free_bits[b]['pairs']))
    pairs_label = '+'.join(pair_strs)

    bits_str = ','.join(str(b) for b in combo)
    print(f"{bits_str:>8s} {pairs_label:>10s} {chi2:8.4f} {d_chi2:+8.4f} "
          f"{kac:8.4f} {d_kac:+8.4f} {pareto:>15s}")

    exp3_results.append({
        'bits': combo,
        'chi2': float(chi2),
        'd_chi2': float(d_chi2),
        'kac': float(kac),
        'd_kac': float(d_kac),
        'pareto': pareto,
    })

print()

pareto3_counts = Counter(r['pareto'] for r in exp3_results)
print("Pareto summary (2-bit pure-improvement combos):")
for cls in ['cone-escape', 'trade-off', 'KW-dominated', 'double-degrade']:
    count = pareto3_counts.get(cls, 0)
    bits = [r['bits'] for r in exp3_results if r['pareto'] == cls]
    print(f"  {cls:>15s}: {count:2d}  — {bits}")

escapes_3 = [r for r in exp3_results if r['pareto'] == 'cone-escape']
if escapes_3:
    print()
    print("** 2-BIT CONE ESCAPES FOUND **")
    for r in escapes_3:
        print(f"  bits {r['bits']}: chi²={r['chi2']:.4f} (Δ={r['d_chi2']:+.4f})  "
              f"kac={r['kac']:.4f} (Δ={r['d_kac']:+.4f})")
else:
    print()
    print("** NO 2-BIT CONE ESCAPES — all pure-improvement combos trade off against kernel_autocorr_1 **")
print()


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 4: Weight-ordering sensitivity (all 27 bits)
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("EXPERIMENT 4: Weight-ordering bias — all 27 single-bit flips")
print("─" * 80)
print()

exp4_results = []

header4 = f"{'bit':>4s} {'pair(s)':>8s} {'wob':>5s} {'Δwob':>6s}"
print(header4)
print("─" * len(header4))

for bi in free_bits:
    idx = bi['bit_index']
    o = apply_bits([idx])
    seq = build_sequence(o)
    wob = compute_weight_ordering_bias(seq)
    d_wob = wob - KW_WOB

    pairs_str = ','.join(str(p) for p in bi['pairs'])
    print(f"{idx:4d} {pairs_str:>8s} {wob:5d} {d_wob:+6d}")

    exp4_results.append({
        'bit_index': idx,
        'pairs': bi['pairs'],
        'description': bi['description'],
        'weight_ordering_bias': wob,
        'd_wob': d_wob,
    })

print()

# Summary
wob_changes = Counter(r['d_wob'] for r in exp4_results)
print(f"Weight-ordering bias changes: {dict(sorted(wob_changes.items()))}")
n_changed = sum(1 for r in exp4_results if r['d_wob'] != 0)
print(f"Bits that change wob: {n_changed}/27")
changers = [(r['bit_index'], r['description'], r['d_wob'])
            for r in exp4_results if r['d_wob'] != 0]
for idx, desc, d in changers:
    print(f"  bit {idx} ({desc}): Δwob={d:+d}")
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

save_data = json_clean({
    'kw_baseline': {
        'chi2': KW_CHI2,
        'kernel_autocorr_1': KW_KAC,
        'weight_ordering_bias': KW_WOB,
    },
    'exp1_single_bit_gradient': exp1_results,
    'exp2_additivity': exp2_results,
    'exp3_pareto_2bit': exp3_results,
    'exp4_weight_ordering': exp4_results,
})

with open('/home/quasar/nous/logoswen/iter4/round4_data.json', 'w') as f:
    json.dump(save_data, f, indent=2)

print("Data saved to logoswen/iter4/round4_data.json")
print()
print("=" * 80)
print("ROUND 4 COMPLETE")
print("=" * 80)
