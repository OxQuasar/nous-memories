"""
Round 3: Structural Census — What Does the Improvement Cone Cost?

Compare KW to flipped orientations on every structural property
outside the {chi², asym, m-score} metric space.

Experiments:
  1. bits {10,17} flip (improvement cone)
  2. bits {9,10,17} flip (all-three-improving)
  3. bit 22 flip (coupling-only, metrics-invisible)
  4. bit 13 flip (primary keystone, control)

For calibration: 200 random S=2-free orientations.
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
# INFRASTRUCTURE
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

TRIGRAMS = {
    (1,1,1): 'Heaven', (0,0,0): 'Earth',
    (0,1,0): 'Water',  (1,0,1): 'Fire',
    (1,0,0): 'Thunder',(0,1,1): 'Wind',
    (0,0,1): 'Mountain',(1,1,0): 'Lake',
}
TRI_NAMES = ['Heaven','Earth','Water','Fire','Thunder','Wind','Mountain','Lake']
TRI_IDX = {n: i for i, n in enumerate(TRI_NAMES)}

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

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

def lower_tri(h):
    return h[:3]

def upper_tri(h):
    return h[3:]

def tri_name(t):
    return TRIGRAMS.get(t, '?')

def is_complement(a, b):
    return all(x ^ y == 1 for x, y in zip(a, b))

def is_inversion(a, b):
    return all(a[i] == b[5-i] for i in range(6))

def is_palindrome(h):
    return all(h[i] == h[5-i] for i in range(3))


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

# Free bits index
free_bits = []
for p in FREE_PAIRS:
    free_bits.append({'bit_index': len(free_bits), 'type': 'A', 'pairs': [p]})
for ci, ((p1, p2), valid) in enumerate(COMPONENT_VALID.items()):
    free_bits.append({'bit_index': len(free_bits), 'type': 'B', 'pairs': [p1, p2],
                      'valid_states': valid})

def apply_bits_to_orientation(bit_indices):
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
# STRUCTURAL CENSUS FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def structural_census(o):
    """Compute comprehensive structural properties of an orientation."""
    seq = build_sequence(o)
    props = {}

    # ── 1a. Trigram-level statistics ──────────────────────────────────────

    # Trigram transition matrix across bridges (exit_hex → entry_hex)
    # Lower trigram transitions and upper trigram transitions
    lower_trans = np.zeros((8, 8), dtype=int)
    upper_trans = np.zeros((8, 8), dtype=int)

    for k in range(31):
        exit_hex = seq[2*k + 1]   # second hex of pair k
        entry_hex = seq[2*k + 2]  # first hex of pair k+1

        lt_exit = tri_name(lower_tri(exit_hex))
        lt_entry = tri_name(lower_tri(entry_hex))
        ut_exit = tri_name(upper_tri(exit_hex))
        ut_entry = tri_name(upper_tri(entry_hex))

        lower_trans[TRI_IDX[lt_exit], TRI_IDX[lt_entry]] += 1
        upper_trans[TRI_IDX[ut_exit], TRI_IDX[ut_entry]] += 1

    # Trigram transition uniformity (chi² for each matrix)
    def trans_chi2(mat):
        expected = mat.sum() / (8 * 8)
        return float(np.sum((mat - expected)**2 / expected))

    props['lower_tri_trans_chi2'] = trans_chi2(lower_trans)
    props['upper_tri_trans_chi2'] = trans_chi2(upper_trans)

    # How many distinct trigram transitions used (out of 64 possible)?
    props['lower_tri_trans_distinct'] = int(np.sum(lower_trans > 0))
    props['upper_tri_trans_distinct'] = int(np.sum(upper_trans > 0))

    # Trigram self-transitions (same trigram exit→entry)
    props['lower_tri_self'] = int(np.trace(lower_trans))
    props['upper_tri_self'] = int(np.trace(upper_trans))

    # Trigram distribution across all 64 positions
    lower_tri_dist = Counter()
    upper_tri_dist = Counter()
    for h in seq:
        lower_tri_dist[tri_name(lower_tri(h))] += 1
        upper_tri_dist[tri_name(upper_tri(h))] += 1
    # Uniformity: each trigram should appear 8 times
    props['lower_tri_uniformity'] = float(sum((lower_tri_dist.get(t, 0) - 8)**2 / 8 for t in TRI_NAMES))
    props['upper_tri_uniformity'] = float(sum((upper_tri_dist.get(t, 0) - 8)**2 / 8 for t in TRI_NAMES))

    # Store transition matrices as flat lists for JSON
    props['lower_tri_trans_flat'] = lower_trans.flatten().tolist()
    props['upper_tri_trans_flat'] = upper_trans.flatten().tolist()

    # ── 1b. Line-level statistics ─────────────────────────────────────────

    # Extract each line as a 64-element binary sequence
    lines = []
    for L in range(6):
        line_seq = [seq[i][L] for i in range(64)]
        lines.append(line_seq)

    # Autocorrelation for each line (lags 1–16)
    line_autocorr = []
    for L in range(6):
        ls = np.array(lines[L], dtype=float) - np.mean(lines[L])
        var = np.var(lines[L])
        ac = []
        for lag in range(1, 17):
            if var > 0:
                c = np.mean(ls[:-lag] * ls[lag:]) / var
            else:
                c = 0.0
            ac.append(float(c))
        line_autocorr.append(ac)

    props['line_autocorr'] = line_autocorr

    # Sum of absolute autocorrelations (lag 1-8) per line — total "memory"
    for L in range(6):
        props[f'line_{L}_autocorr_sum'] = float(sum(abs(line_autocorr[L][lag]) for lag in range(8)))

    # Total line autocorrelation across all lines
    props['total_line_autocorr'] = float(sum(
        sum(abs(line_autocorr[L][lag]) for lag in range(8))
        for L in range(6)
    ))

    # Line balance (number of 1s per line)
    for L in range(6):
        props[f'line_{L}_ones'] = sum(lines[L])

    # Line parity correlation: do lines 0,5 correlate? 1,4? 2,3?
    # (These are the palindrome-paired lines)
    for p1, p2 in [(0,5), (1,4), (2,3)]:
        corr = float(np.corrcoef(lines[p1], lines[p2])[0,1]) if np.std(lines[p1]) > 0 and np.std(lines[p2]) > 0 else 0.0
        props[f'line_pair_{p1}_{p2}_corr'] = corr

    # ── 1c. Hamming distance statistics ───────────────────────────────────

    # Within-pair Hamming distances
    pair_hamming = []
    for k in range(N_PAIRS):
        h = hamming(seq[2*k], seq[2*k+1])
        pair_hamming.append(h)
    props['pair_hamming_mean'] = float(np.mean(pair_hamming))
    props['pair_hamming_std'] = float(np.std(pair_hamming))
    props['pair_hamming_dist'] = dict(Counter(pair_hamming))

    # Bridge Hamming distances (between consecutive pairs)
    bridge_hamming = []
    for k in range(31):
        h = hamming(seq[2*k+1], seq[2*k+2])
        bridge_hamming.append(h)
    props['bridge_hamming_mean'] = float(np.mean(bridge_hamming))
    props['bridge_hamming_std'] = float(np.std(bridge_hamming))
    props['bridge_hamming_dist'] = dict(Counter(bridge_hamming))

    # Consecutive hexagram Hamming (all 63 consecutive pairs in the 64-seq)
    consec_hamming = []
    for i in range(63):
        h = hamming(seq[i], seq[i+1])
        consec_hamming.append(h)
    props['consec_hamming_mean'] = float(np.mean(consec_hamming))
    props['consec_hamming_std'] = float(np.std(consec_hamming))
    props['consec_hamming_dist'] = dict(Counter(consec_hamming))

    # S-value distribution across bridges
    bridge_S = []
    for k in range(31):
        s = compute_S(seq[2*k+1], seq[2*k+2])
        bridge_S.append(s)
    props['bridge_S_dist'] = dict(Counter(bridge_S))
    props['bridge_S_mean'] = float(np.mean(bridge_S))

    # ── 1d. Pair-internal symmetry ────────────────────────────────────────

    n_complement = 0
    n_inversion = 0
    n_palindrome_first = 0  # first hex is a palindrome (h == reverse(h))
    n_palindrome_second = 0
    n_both_palindrome = 0

    # Binary ordering within pairs
    n_first_larger = 0  # binary value of first > second

    for k in range(N_PAIRS):
        a, b = seq[2*k], seq[2*k+1]
        if is_complement(a, b):
            n_complement += 1
        if is_inversion(a, b):
            n_inversion += 1
        if is_palindrome(a):
            n_palindrome_first += 1
        if is_palindrome(b):
            n_palindrome_second += 1
        if is_palindrome(a) and is_palindrome(b):
            n_both_palindrome += 1
        if hex_to_int(a) > hex_to_int(b):
            n_first_larger += 1

    props['n_complement_pairs'] = n_complement
    props['n_inversion_pairs'] = n_inversion
    props['n_palindrome_first'] = n_palindrome_first
    props['n_palindrome_second'] = n_palindrome_second
    props['n_both_palindrome'] = n_both_palindrome
    props['n_first_larger'] = n_first_larger

    # Yin/yang balance: total yang lines in first hex of each pair vs second
    first_yang = sum(sum(seq[2*k]) for k in range(N_PAIRS))
    second_yang = sum(sum(seq[2*k+1]) for k in range(N_PAIRS))
    props['first_hex_total_yang'] = first_yang
    props['second_hex_total_yang'] = second_yang
    props['yang_balance'] = first_yang - second_yang

    # ── 1e. Sequence-level patterns ───────────────────────────────────────

    # Trigram runs: longest consecutive run of same lower/upper trigram
    def longest_run(values):
        if not values:
            return 0
        max_run = 1
        current = 1
        for i in range(1, len(values)):
            if values[i] == values[i-1]:
                current += 1
                max_run = max(max_run, current)
            else:
                current = 1
        return max_run

    lower_tri_seq = [tri_name(lower_tri(h)) for h in seq]
    upper_tri_seq = [tri_name(upper_tri(h)) for h in seq]

    props['lower_tri_longest_run'] = longest_run(lower_tri_seq)
    props['upper_tri_longest_run'] = longest_run(upper_tri_seq)

    # Number of trigram boundaries (where trigram changes)
    lower_boundaries = sum(1 for i in range(63) if lower_tri_seq[i] != lower_tri_seq[i+1])
    upper_boundaries = sum(1 for i in range(63) if upper_tri_seq[i] != upper_tri_seq[i+1])
    props['lower_tri_boundaries'] = lower_boundaries
    props['upper_tri_boundaries'] = upper_boundaries

    # Line-level FFT — dominant frequency per line
    for L in range(6):
        ls = np.array(lines[L], dtype=float)
        ls = ls - ls.mean()
        fft = np.abs(np.fft.rfft(ls))[1:]  # skip DC
        if len(fft) > 0 and fft.max() > 0:
            props[f'line_{L}_dominant_freq'] = int(np.argmax(fft) + 1)
            props[f'line_{L}_fft_peak'] = float(fft.max())
            props[f'line_{L}_fft_energy'] = float(np.sum(fft**2))
        else:
            props[f'line_{L}_dominant_freq'] = 0
            props[f'line_{L}_fft_peak'] = 0.0
            props[f'line_{L}_fft_energy'] = 0.0

    # Total FFT energy across all lines
    props['total_fft_energy'] = sum(props[f'line_{L}_fft_energy'] for L in range(6))

    # ── Additional: Weight spectrum ───────────────────────────────────────

    # Weight (number of yang lines) distribution across the sequence
    weights = [sum(h) for h in seq]
    props['weight_mean'] = float(np.mean(weights))
    props['weight_std'] = float(np.std(weights))
    props['weight_dist'] = dict(Counter(weights))

    # Weight autocorrelation (lag 1)
    w = np.array(weights, dtype=float) - np.mean(weights)
    if np.var(weights) > 0:
        props['weight_autocorr_1'] = float(np.mean(w[:-1] * w[1:]) / np.var(weights))
    else:
        props['weight_autocorr_1'] = 0.0

    # ── Additional: Kernel chain properties ───────────────────────────────

    # Already measured by chi², but compute some additional kernel stats
    kernel_chain = []
    for k in range(31):
        m = xor6(seq[2*k+1], seq[2*k+2])
        k3 = (m[5], m[4], m[3])
        gen_6 = (k3[0], k3[1], k3[2], k3[2], k3[1], k3[0])
        name = VALID_MASKS.get(gen_6, '?')
        kernel_chain.append(name)

    # Kernel runs
    props['kernel_longest_run'] = longest_run(kernel_chain)
    kernel_boundaries = sum(1 for i in range(30) if kernel_chain[i] != kernel_chain[i+1])
    props['kernel_boundaries'] = kernel_boundaries

    # Kernel autocorrelation (encode as integers)
    kernel_int = [ALL_GEN_NAMES.index(k) for k in kernel_chain]
    ki = np.array(kernel_int, dtype=float) - np.mean(kernel_int)
    if np.var(kernel_int) > 0:
        props['kernel_autocorr_1'] = float(np.mean(ki[:-1] * ki[1:]) / np.var(kernel_int))
    else:
        props['kernel_autocorr_1'] = 0.0

    # ── Additional: Pair ordering patterns ────────────────────────────────

    # Upper vs lower canon first-larger counts (already in asym metric, but break down further)
    props['upper_first_larger'] = sum(1 for k in range(15)
                                       if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    props['lower_first_larger'] = sum(1 for k in range(15, 32)
                                       if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))

    # Weight ordering: in how many pairs is the first hex heavier (more yang)?
    n_first_heavier = sum(1 for k in range(N_PAIRS) if sum(seq[2*k]) > sum(seq[2*k+1]))
    n_first_lighter = sum(1 for k in range(N_PAIRS) if sum(seq[2*k]) < sum(seq[2*k+1]))
    props['n_first_heavier'] = n_first_heavier
    props['n_first_lighter'] = n_first_lighter
    props['weight_ordering_bias'] = n_first_heavier - n_first_lighter

    # ── Additional: Positional balance ────────────────────────────────────

    # Even vs odd position yang count
    even_yang = sum(sum(seq[i]) for i in range(0, 64, 2))
    odd_yang = sum(sum(seq[i]) for i in range(1, 64, 2))
    props['even_pos_yang'] = even_yang
    props['odd_pos_yang'] = odd_yang
    props['pos_yang_imbalance'] = even_yang - odd_yang

    # First half vs second half yang count
    first_half_yang = sum(sum(seq[i]) for i in range(32))
    second_half_yang = sum(sum(seq[i]) for i in range(32, 64))
    props['first_half_yang'] = first_half_yang
    props['second_half_yang'] = second_half_yang
    props['half_yang_imbalance'] = first_half_yang - second_half_yang

    return props


# ══════════════════════════════════════════════════════════════════════════════
# SCALAR PROPERTY KEYS (for comparison tables)
# ══════════════════════════════════════════════════════════════════════════════

SCALAR_KEYS = [
    'lower_tri_trans_chi2', 'upper_tri_trans_chi2',
    'lower_tri_trans_distinct', 'upper_tri_trans_distinct',
    'lower_tri_self', 'upper_tri_self',
    'lower_tri_uniformity', 'upper_tri_uniformity',
    'total_line_autocorr',
    'line_0_autocorr_sum', 'line_1_autocorr_sum', 'line_2_autocorr_sum',
    'line_3_autocorr_sum', 'line_4_autocorr_sum', 'line_5_autocorr_sum',
    'line_pair_0_5_corr', 'line_pair_1_4_corr', 'line_pair_2_3_corr',
    'pair_hamming_mean', 'pair_hamming_std',
    'bridge_hamming_mean', 'bridge_hamming_std',
    'consec_hamming_mean', 'consec_hamming_std',
    'bridge_S_mean',
    'n_complement_pairs', 'n_inversion_pairs',
    'n_palindrome_first', 'n_palindrome_second', 'n_both_palindrome',
    'n_first_larger',
    'first_hex_total_yang', 'second_hex_total_yang', 'yang_balance',
    'lower_tri_longest_run', 'upper_tri_longest_run',
    'lower_tri_boundaries', 'upper_tri_boundaries',
    'total_fft_energy',
    'line_0_fft_energy', 'line_1_fft_energy', 'line_2_fft_energy',
    'line_3_fft_energy', 'line_4_fft_energy', 'line_5_fft_energy',
    'weight_mean', 'weight_std', 'weight_autocorr_1',
    'kernel_longest_run', 'kernel_boundaries', 'kernel_autocorr_1',
    'upper_first_larger', 'lower_first_larger',
    'n_first_heavier', 'n_first_lighter', 'weight_ordering_bias',
    'even_pos_yang', 'odd_pos_yang', 'pos_yang_imbalance',
    'first_half_yang', 'second_half_yang', 'half_yang_imbalance',
]

# Per-line keys
for L in range(6):
    SCALAR_KEYS.append(f'line_{L}_ones')
    SCALAR_KEYS.append(f'line_{L}_dominant_freq')
    SCALAR_KEYS.append(f'line_{L}_fft_peak')


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTE KW BASELINE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("ROUND 3: STRUCTURAL CENSUS")
print("=" * 80)
print()

KW_O = [0] * 32
kw_props = structural_census(KW_O)

print(f"KW census computed: {len(SCALAR_KEYS)} scalar properties")
print()


# ══════════════════════════════════════════════════════════════════════════════
# RANDOM CALIBRATION (200 S=2-free orientations)
# ══════════════════════════════════════════════════════════════════════════════

N_CAL = 200
print(f"Computing calibration distribution ({N_CAL} random S=2-free)...")
t0 = time.time()

rng = random.Random(42)
cal_props = {k: [] for k in SCALAR_KEYS}

for i in range(N_CAL):
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break
    p = structural_census(o)
    for k in SCALAR_KEYS:
        cal_props[k].append(p.get(k, 0))

cal_arrays = {k: np.array(v) for k, v in cal_props.items()}
t1 = time.time()
print(f"  Done in {t1-t0:.1f}s")
print()


def percentile_rank(value, distribution):
    """Where does value fall in the distribution? Return percentile 0-100."""
    return float(np.mean(distribution <= value) * 100)


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def run_experiment(name, bit_indices, kw_props, cal_arrays):
    """Run structural census on a flipped orientation, compare to KW and random."""
    print(f"{'─' * 80}")
    print(f"EXPERIMENT: {name}")
    print(f"  Bits flipped: {bit_indices}")
    o = apply_bits_to_orientation(bit_indices)
    assert is_s2_free(o), f"S=2 violation for {name}!"

    flip_props = structural_census(o)

    # Build comparison table
    rows = []
    significant = []

    for k in SCALAR_KEYS:
        kw_val = kw_props.get(k, 0)
        fl_val = flip_props.get(k, 0)

        # Handle potential type issues
        if isinstance(kw_val, (list, dict)):
            continue
        if isinstance(fl_val, (list, dict)):
            continue

        delta = fl_val - kw_val
        pct = percentile_rank(fl_val, cal_arrays[k])
        kw_pct = percentile_rank(kw_val, cal_arrays[k])

        # Flag if delta != 0 AND the flipped value is more extreme than 95th or below 5th
        is_sig = (abs(delta) > 1e-9 and (pct <= 5 or pct >= 95))
        # Also flag if KW is extreme but flip moves it toward center
        kw_extreme = (kw_pct <= 5 or kw_pct >= 95)

        row = {
            'property': k,
            'kw': kw_val,
            'flip': fl_val,
            'delta': delta,
            'kw_pctile': kw_pct,
            'flip_pctile': pct,
            'significant': is_sig,
            'kw_extreme': kw_extreme,
        }
        rows.append(row)

        if is_sig:
            significant.append(row)

    # Print significant changes
    print(f"  Properties with significant change (flip at ≤5th or ≥95th pctile):")
    if significant:
        print(f"  {'Property':<35s} {'KW':>8s} {'Flip':>8s} {'Δ':>8s} {'KW%':>6s} {'Flip%':>6s}")
        print(f"  {'─'*75}")
        for r in significant:
            print(f"  {r['property']:<35s} {r['kw']:8.3f} {r['flip']:8.3f} "
                  f"{r['delta']:+8.3f} {r['kw_pctile']:5.1f}% {r['flip_pctile']:5.1f}%")
    else:
        print(f"  (none)")

    # Also print changes where delta != 0 regardless of significance
    changed = [r for r in rows if abs(r['delta']) > 1e-9]
    print(f"\n  All changed properties ({len(changed)}/{len(rows)}):")
    print(f"  {'Property':<35s} {'KW':>8s} {'Flip':>8s} {'Δ':>8s} {'KW%':>6s} {'Flip%':>6s} {'Sig':>4s}")
    print(f"  {'─'*80}")
    for r in sorted(changed, key=lambda r: -abs(r['delta'])):
        sig_mark = ' ***' if r['significant'] else ('  KW' if r['kw_extreme'] else '')
        print(f"  {r['property']:<35s} {r['kw']:8.3f} {r['flip']:8.3f} "
              f"{r['delta']:+8.3f} {r['kw_pctile']:5.1f}% {r['flip_pctile']:5.1f}%{sig_mark}")

    # Print unchanged count
    unchanged = [r for r in rows if abs(r['delta']) <= 1e-9]
    print(f"\n  Unchanged properties: {len(unchanged)}/{len(rows)}")

    print()
    return {'name': name, 'bits': bit_indices, 'rows': rows, 'flip_props': flip_props}


# ══════════════════════════════════════════════════════════════════════════════
# RUN ALL EXPERIMENTS
# ══════════════════════════════════════════════════════════════════════════════

experiments = {}

# Experiment 1: bits {10,17} — improvement cone
exp1 = run_experiment("bits {10,17} — improvement cone", [10, 17], kw_props, cal_arrays)
experiments['exp1_10_17'] = exp1

# Experiment 2: bits {9,10,17} — all-three-improving
exp2 = run_experiment("bits {9,10,17} — all-three-improving", [9, 10, 17], kw_props, cal_arrays)
experiments['exp2_9_10_17'] = exp2

# Experiment 3: bit 22 — coupling-only (component 13,14)
exp3 = run_experiment("bit 22 — coupling-only (component 13,14)", [22], kw_props, cal_arrays)
experiments['exp3_22'] = exp3

# Experiment 4: bit 13 — primary keystone (pair 15)
exp4 = run_experiment("bit 13 — keystone control (pair 15)", [13], kw_props, cal_arrays)
experiments['exp4_13'] = exp4


# ══════════════════════════════════════════════════════════════════════════════
# CROSS-EXPERIMENT COMPARISON
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("CROSS-EXPERIMENT COMPARISON")
print("=" * 80)
print()

# For each property, show KW value and all 4 experiment values
print(f"{'Property':<35s} {'KW':>8s} {'10+17':>8s} {'9+10+17':>8s} {'22':>8s} {'13':>8s} {'KW%':>6s}")
print(f"{'─'*85}")

for k in SCALAR_KEYS:
    kw_val = kw_props.get(k, 0)
    if isinstance(kw_val, (list, dict)):
        continue

    vals = []
    for exp_key in ['exp1_10_17', 'exp2_9_10_17', 'exp3_22', 'exp4_13']:
        fp = experiments[exp_key]['flip_props']
        v = fp.get(k, 0)
        if isinstance(v, (list, dict)):
            v = 0
        vals.append(v)

    # Only show rows where at least one experiment differs from KW
    if all(abs(v - kw_val) < 1e-9 for v in vals):
        continue

    kw_pct = percentile_rank(kw_val, cal_arrays[k])
    print(f"{k:<35s} {kw_val:8.3f} {vals[0]:8.3f} {vals[1]:8.3f} {vals[2]:8.3f} {vals[3]:8.3f} {kw_pct:5.1f}%")

print()


# ══════════════════════════════════════════════════════════════════════════════
# KW EXTREMITY ANALYSIS — where is KW already extreme?
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("KW EXTREMITY — properties where KW is at ≤5th or ≥95th percentile")
print("=" * 80)
print()

kw_extreme = []
for k in SCALAR_KEYS:
    kw_val = kw_props.get(k, 0)
    if isinstance(kw_val, (list, dict)):
        continue
    pct = percentile_rank(kw_val, cal_arrays[k])
    if pct <= 5 or pct >= 95:
        kw_extreme.append((k, kw_val, pct))

print(f"{'Property':<35s} {'KW':>8s} {'Pctile':>7s} {'Random mean':>12s} {'Random std':>11s}")
print(f"{'─'*75}")
for k, val, pct in sorted(kw_extreme, key=lambda x: x[2]):
    rm = float(cal_arrays[k].mean())
    rs = float(cal_arrays[k].std())
    print(f"{k:<35s} {val:8.3f} {pct:6.1f}% {rm:12.3f} {rs:11.3f}")

print(f"\nTotal extreme properties: {len(kw_extreme)}/{len(SCALAR_KEYS)}")
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
    elif isinstance(obj, tuple):
        return list(obj)
    return obj

save_data = json_clean({
    'kw_props': {k: kw_props[k] for k in SCALAR_KEYS if not isinstance(kw_props.get(k), (list, dict))},
    'calibration_stats': {
        k: {'mean': float(cal_arrays[k].mean()), 'std': float(cal_arrays[k].std()),
            'p5': float(np.percentile(cal_arrays[k], 5)),
            'p95': float(np.percentile(cal_arrays[k], 95)),
            'kw_pctile': percentile_rank(kw_props.get(k, 0), cal_arrays[k])}
        for k in SCALAR_KEYS if not isinstance(kw_props.get(k), (list, dict))
    },
    'experiments': {
        name: {
            'bits': exp['bits'],
            'changed_properties': [
                {k: json_clean(v) for k, v in r.items()}
                for r in exp['rows'] if abs(r.get('delta', 0)) > 1e-9
            ],
            'significant_properties': [
                {k: json_clean(v) for k, v in r.items()}
                for r in exp['rows'] if r.get('significant', False)
            ],
        }
        for name, exp in experiments.items()
    },
})

with open('/home/quasar/nous/logoswen/iter4/round3_data.json', 'w') as f:
    json.dump(save_data, f, indent=2)

print("Data saved to logoswen/iter4/round3_data.json")
print()
print("=" * 80)
print("ROUND 3 COMPLETE")
print("=" * 80)
