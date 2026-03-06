"""
Round 3: Three-Signal Independence Analysis

The three Layer 4 signals:
  1. Kernel uniformity (chi² = 2.29, p ≈ 0.06)
  2. Canon asymmetry (+3, p ≈ 0.05)
  3. M-component preference (12/16, p ≈ 0.04 uncorrected)

Questions:
  A. Three-way joint distribution — are these one, two, or three phenomena?
  B. S=2 constraint mediation of M-component
  C. Upper-canon isolation (zero S=2 constraints there)
  D. Partial correlations controlling for constraint configuration
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import numpy as np
import time

DIMS = 6
N_PAIRS = 32
M = [tuple(b) for b in all_bits()]

VALID_MASKS = {
    (0,0,0,0,0,0): 'id',  (1,0,0,0,0,1): 'O',  (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',   (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',  (1,1,1,1,1,1): 'OMI',
}

# ── Build pairs ───────────────────────────────────────────────────────────────

PAIRS = []
for k in range(N_PAIRS):
    PAIRS.append({'a': M[2*k], 'b': M[2*k+1]})


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

def reverse_hex(h):
    return tuple(h[5-i] for i in range(6))

def is_palindrome(h):
    return h == reverse_hex(h)

def hex_to_int(h):
    v = 0
    for bit in h:
        v = v * 2 + bit
    return v


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

# Identify constrained pair sets
CONSTRAINED_PAIRS = set()
CONSTRAINT_COMPONENTS = []  # list of (set_of_pairs, bridge_idx)
for k in CONSTRAINTS:
    CONSTRAINED_PAIRS.add(k)
    CONSTRAINED_PAIRS.add(k+1)

# Build components
adj = defaultdict(set)
for k in CONSTRAINTS:
    adj[k].add(k+1)
    adj[k+1].add(k)

visited = set()
for start in sorted(CONSTRAINED_PAIRS):
    if start in visited:
        continue
    comp = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        comp.append(node)
        for nb in adj[node]:
            if nb not in visited:
                stack.append(nb)
    CONSTRAINT_COMPONENTS.append(sorted(comp))


def is_s2_free(o):
    for k, forbidden in CONSTRAINTS.items():
        if (o[k], o[k+1]) in forbidden:
            return False
    return True


# ── Identify M-decisive pairs ────────────────────────────────────────────────

# A pair is M-decisive if L2 ≠ L5 in the first hexagram (KW orientation)
# For inversion pairs, flipping swaps L2↔L5, so this is equivalent to
# the pair having an asymmetric M-component.

M_DECISIVE = []
M_DECISIVE_IN_CONSTRAINT = []
M_DECISIVE_FREE = []

for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    if a[1] != a[4]:  # L2 ≠ L5
        M_DECISIVE.append(k)
        if k in CONSTRAINED_PAIRS:
            M_DECISIVE_IN_CONSTRAINT.append(k)
        else:
            M_DECISIVE_FREE.append(k)

print("=" * 80)
print("SETUP: M-DECISIVE PAIRS AND CONSTRAINT GEOGRAPHY")
print("=" * 80)
print()
print(f"  M-decisive pairs (L2≠L5): {len(M_DECISIVE)}")
print(f"    In constraint groups: {M_DECISIVE_IN_CONSTRAINT}")
print(f"    Free of constraints: {M_DECISIVE_FREE}")
print(f"  Constraint components: {CONSTRAINT_COMPONENTS}")
print(f"  Constrained pairs: {sorted(CONSTRAINED_PAIRS)}")
print()

# For each M-decisive pair, what is KW's L2 value?
print(f"  M-decisive pairs detail:")
for k in M_DECISIVE:
    a = PAIRS[k]['a']
    L2, L5 = a[1], a[4]
    in_constraint = k in CONSTRAINED_PAIRS
    kw_l2yin = (L2 == 0)
    print(f"    Pair {k:2d}: L2={L2} L5={L5} L2=yin={kw_l2yin} "
          f"constrained={'YES' if in_constraint else 'no '} "
          f"{KING_WEN[2*k][1]}")


# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL COMPUTATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def compute_signals(orientation):
    """Compute all three signals for an orientation vector."""
    # Build sequence
    seq = []
    for k in range(N_PAIRS):
        if orientation[k] == 0:
            seq.append(PAIRS[k]['a'])
            seq.append(PAIRS[k]['b'])
        else:
            seq.append(PAIRS[k]['b'])
            seq.append(PAIRS[k]['a'])

    # --- Signal 1: Kernel chi² (uniformity) ---
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

    # --- Signal 2: Canon asymmetry ---
    upper_binhigh = 0
    lower_binhigh = 0
    for k in range(N_PAIRS):
        va = hex_to_int(seq[2*k])
        vb = hex_to_int(seq[2*k+1])
        if k < 15:
            if va > vb:
                upper_binhigh += 1
        else:
            if va > vb:
                lower_binhigh += 1
    canon_asym = upper_binhigh - lower_binhigh

    # --- Signal 3: M-component score ---
    # Count: among M-decisive pairs, how many have L2=yin in the first hex?
    m_score = 0
    m_total = 0
    for k in M_DECISIVE:
        first_hex = seq[2*k]
        if first_hex[1] == 0:  # L2 = yin
            m_score += 1
        m_total += 1

    # --- Signal 3 variants: free-only M-component ---
    m_score_free = 0
    m_total_free = 0
    for k in M_DECISIVE_FREE:
        first_hex = seq[2*k]
        if first_hex[1] == 0:
            m_score_free += 1
        m_total_free += 1

    m_score_constrained = 0
    m_total_constrained = 0
    for k in M_DECISIVE_IN_CONSTRAINT:
        first_hex = seq[2*k]
        if first_hex[1] == 0:
            m_score_constrained += 1
        m_total_constrained += 1

    # --- Upper-canon-only signals ---
    # Upper canon: pairs 0-11 (bridges 0-11)
    # Bridges 0-11 have ZERO S=2 constraints
    uc_chain_names = chain_names[:12]  # bridges 0-11
    uc_freq = Counter(uc_chain_names)
    uc_expected = 12 / 8
    uc_chi2 = sum((uc_freq.get(g, 0) - uc_expected) ** 2 / uc_expected
                  for g in VALID_MASKS.values())

    uc_binhigh = upper_binhigh  # already just pairs 0-14

    uc_m_score = 0
    uc_m_total = 0
    for k in M_DECISIVE:
        if k < 15:  # upper canon
            first_hex = seq[2*k]
            if first_hex[1] == 0:
                uc_m_score += 1
            uc_m_total += 1

    # --- Constraint configuration (16-state variable) ---
    # The 5 constraint components each have 2 valid states
    # Encode as a 5-bit integer
    constraint_config = 0
    for i, comp in enumerate(CONSTRAINT_COMPONENTS):
        # The constraint is an equality constraint on adjacent pairs
        # State = orientation of the first pair in the component
        constraint_config |= (orientation[comp[0]] << i)

    return {
        'chi2': chi2,
        'canon_asym': canon_asym,
        'm_score': m_score,
        'm_total': m_total,
        'm_score_free': m_score_free,
        'm_total_free': m_total_free,
        'm_score_constrained': m_score_constrained,
        'm_total_constrained': m_total_constrained,
        'uc_chi2': uc_chi2,
        'uc_binhigh': uc_binhigh,
        'uc_m_score': uc_m_score,
        'uc_m_total': uc_m_total,
        'constraint_config': constraint_config,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 1. THREE-WAY JOINT DISTRIBUTION (200K samples)
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("1. THREE-WAY JOINT DISTRIBUTION (200K S=2-free samples)")
print("=" * 80)
print()

N_SAMPLES = 200_000
rng = random.Random(42)

# Storage
all_chi2 = np.empty(N_SAMPLES)
all_asym = np.empty(N_SAMPLES)
all_m = np.empty(N_SAMPLES)
all_m_free = np.empty(N_SAMPLES)
all_m_constr = np.empty(N_SAMPLES)
all_uc_chi2 = np.empty(N_SAMPLES)
all_uc_bh = np.empty(N_SAMPLES)
all_uc_m = np.empty(N_SAMPLES)
all_cc = np.empty(N_SAMPLES, dtype=int)

t0 = time.time()
n_tried = 0

for i in range(N_SAMPLES):
    while True:
        n_tried += 1
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            break

    s = compute_signals(o)
    all_chi2[i] = s['chi2']
    all_asym[i] = s['canon_asym']
    all_m[i] = s['m_score']
    all_m_free[i] = s['m_score_free']
    all_m_constr[i] = s['m_score_constrained']
    all_uc_chi2[i] = s['uc_chi2']
    all_uc_bh[i] = s['uc_binhigh']
    all_uc_m[i] = s['uc_m_score']
    all_cc[i] = s['constraint_config']

    if (i+1) % 50000 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{N_SAMPLES} in {elapsed:.1f}s (acc={N_SAMPLES/(n_tried if n_tried>0 else 1):.3f})")

t1 = time.time()
print(f"  Done: {N_SAMPLES} samples in {t1-t0:.1f}s, acceptance={N_SAMPLES/n_tried:.4f}")

# KW baseline
kw = compute_signals([0]*32)
print(f"\n  KW values:")
print(f"    chi² = {kw['chi2']:.2f}")
print(f"    canon_asym = {kw['canon_asym']}")
print(f"    m_score = {kw['m_score']}/{kw['m_total']}")
print(f"    m_score_free = {kw['m_score_free']}/{kw['m_total_free']}")
print(f"    m_score_constrained = {kw['m_score_constrained']}/{kw['m_total_constrained']}")
print(f"    uc_chi2 = {kw['uc_chi2']:.2f}")
print(f"    uc_binhigh = {kw['uc_binhigh']}/15")
print(f"    uc_m_score = {kw['uc_m_score']}/{kw['uc_m_total']}")
print(f"    constraint_config = {kw['constraint_config']}")


# ─── 1a: Marginal p-values ───────────────────────────────────────────────────

print(f"\n  Marginal p-values:")
p_chi2 = np.mean(all_chi2 <= kw['chi2'])
p_asym = np.mean(all_asym >= kw['canon_asym'])
p_m = np.mean(all_m >= kw['m_score'])
print(f"    P(chi² ≤ {kw['chi2']:.2f}) = {p_chi2:.4f}")
print(f"    P(asym ≥ {kw['canon_asym']}) = {p_asym:.4f}")
print(f"    P(m_score ≥ {kw['m_score']}) = {p_m:.4f}")


# ─── 1b: Pairwise correlations ───────────────────────────────────────────────

print(f"\n  Pairwise correlations:")
r_chi2_asym = np.corrcoef(all_chi2, all_asym)[0, 1]
r_chi2_m = np.corrcoef(all_chi2, all_m)[0, 1]
r_asym_m = np.corrcoef(all_asym, all_m)[0, 1]
print(f"    r(chi², canon_asym) = {r_chi2_asym:+.4f}")
print(f"    r(chi², m_score)    = {r_chi2_m:+.4f}")
print(f"    r(canon_asym, m_score) = {r_asym_m:+.4f}")


# ─── 1c: Pairwise joint p-values ─────────────────────────────────────────────

print(f"\n  Pairwise joint p-values:")

j_chi2_asym = np.mean((all_chi2 <= kw['chi2']) & (all_asym >= kw['canon_asym']))
j_chi2_m = np.mean((all_chi2 <= kw['chi2']) & (all_m >= kw['m_score']))
j_asym_m = np.mean((all_asym >= kw['canon_asym']) & (all_m >= kw['m_score']))

print(f"    P(chi² ≤ KW AND asym ≥ KW) = {j_chi2_asym:.5f}  "
      f"(if indep: {p_chi2*p_asym:.5f}, ratio: {j_chi2_asym/(p_chi2*p_asym) if p_chi2*p_asym>0 else 0:.2f})")
print(f"    P(chi² ≤ KW AND m ≥ KW)    = {j_chi2_m:.5f}  "
      f"(if indep: {p_chi2*p_m:.5f}, ratio: {j_chi2_m/(p_chi2*p_m) if p_chi2*p_m>0 else 0:.2f})")
print(f"    P(asym ≥ KW AND m ≥ KW)    = {j_asym_m:.5f}  "
      f"(if indep: {p_asym*p_m:.5f}, ratio: {j_asym_m/(p_asym*p_m) if p_asym*p_m>0 else 0:.2f})")


# ─── 1d: Three-way joint p-value ─────────────────────────────────────────────

j_all = np.mean((all_chi2 <= kw['chi2']) & 
                 (all_asym >= kw['canon_asym']) & 
                 (all_m >= kw['m_score']))
j_all_count = np.sum((all_chi2 <= kw['chi2']) & 
                      (all_asym >= kw['canon_asym']) & 
                      (all_m >= kw['m_score']))
indep_all = p_chi2 * p_asym * p_m

print(f"\n  Three-way joint:")
print(f"    P(chi² ≤ KW AND asym ≥ KW AND m ≥ KW) = {j_all:.6f} ({j_all_count}/{N_SAMPLES})")
print(f"    If fully independent: {indep_all:.6f}")
print(f"    Ratio: {j_all/indep_all if indep_all>0 else 0:.2f}")


# ─── 1e: Redundancy test ─────────────────────────────────────────────────────

print(f"\n  Redundancy test: does adding the third signal help?")

# Given chi² and asym, does m add information?
mask_chi2_asym = (all_chi2 <= kw['chi2']) & (all_asym >= kw['canon_asym'])
n_chi2_asym = np.sum(mask_chi2_asym)
if n_chi2_asym > 0:
    p_m_given_chi2_asym = np.mean(all_m[mask_chi2_asym] >= kw['m_score'])
    print(f"    P(m ≥ KW | chi² ≤ KW, asym ≥ KW) = {p_m_given_chi2_asym:.4f} "
          f"(unconditional: {p_m:.4f})")

# Given chi² and m, does asym add information?
mask_chi2_m = (all_chi2 <= kw['chi2']) & (all_m >= kw['m_score'])
n_chi2_m = np.sum(mask_chi2_m)
if n_chi2_m > 0:
    p_asym_given_chi2_m = np.mean(all_asym[mask_chi2_m] >= kw['canon_asym'])
    print(f"    P(asym ≥ KW | chi² ≤ KW, m ≥ KW) = {p_asym_given_chi2_m:.4f} "
          f"(unconditional: {p_asym:.4f})")

# Given asym and m, does chi² add information?
mask_asym_m = (all_asym >= kw['canon_asym']) & (all_m >= kw['m_score'])
n_asym_m = np.sum(mask_asym_m)
if n_asym_m > 0:
    p_chi2_given_asym_m = np.mean(all_chi2[mask_asym_m] <= kw['chi2'])
    print(f"    P(chi² ≤ KW | asym ≥ KW, m ≥ KW) = {p_chi2_given_asym_m:.4f} "
          f"(unconditional: {p_chi2:.4f})")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. S=2 CONSTRAINT MEDIATION OF M-COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("2. S=2 CONSTRAINT MEDIATION OF M-COMPONENT")
print("=" * 80)
print()

# The 5 constraint components involve pairs:
# {13,14}, {19,20}, {25,26}, {27,28}, {29,30}
# (0-indexed: {12,13}, {18,19}, {24,25}, {26,27}, {28,29})
# Constraints force co-orientation: o_k = o_{k+1}
#
# M-decisive pairs in constraint groups:
# If both pairs in a group are M-decisive, their co-orientation
# mechanically links their M-scores.

print(f"  M-decisive pairs: {M_DECISIVE}")
print(f"  In constraint groups: {M_DECISIVE_IN_CONSTRAINT}")
print(f"  Free of constraints: {M_DECISIVE_FREE}")
print(f"  KW M-score (all): {kw['m_score']}/{kw['m_total']}")
print(f"  KW M-score (free only): {kw['m_score_free']}/{kw['m_total_free']}")
print(f"  KW M-score (constrained only): {kw['m_score_constrained']}/{kw['m_total_constrained']}")

# p-value for free-only M-score
p_m_free = np.mean(all_m_free >= kw['m_score_free'])
p_m_constr = np.mean(all_m_constr >= kw['m_score_constrained'])
print(f"\n  P(m_free ≥ {kw['m_score_free']}) = {p_m_free:.4f}")
print(f"  P(m_constrained ≥ {kw['m_score_constrained']}) = {p_m_constr:.4f}")

# Check: for each constraint component, are both pairs M-decisive?
print(f"\n  Constraint component M-decisiveness:")
for comp in CONSTRAINT_COMPONENTS:
    m_dec = [k for k in comp if k in M_DECISIVE]
    print(f"    Component {comp}: M-decisive members = {m_dec}")
    if len(m_dec) == 2:
        # Both are M-decisive. The co-orientation constraint means:
        # both keep KW orientation or both flip.
        # If both flip, their L2 values swap to L5 values.
        # Check if this creates a mechanical coupling
        for k in m_dec:
            a = PAIRS[k]['a']
            print(f"      Pair {k}: a=(L2={a[1]},L5={a[4]})")

# Binomial test for free-only M-score
from math import comb
n_free = kw['m_total_free']
k_free = kw['m_score_free']
p_binom_free = sum(comb(n_free, j) for j in range(k_free, n_free+1)) / 2**n_free
print(f"\n  Binomial test (free-only): {k_free}/{n_free}, "
      f"p = {p_binom_free:.4f} (one-tailed)")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. UPPER-CANON ISOLATION
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("3. UPPER-CANON ISOLATION (pairs 0-11, bridges 0-11: zero S=2 constraints)")
print("=" * 80)
print()

# Upper canon pairs 0-14 (bridges 0-13)
# But constraints start at bridge 12 (pair 12-13). So:
# Pairs 0-11: fully unconstrained (bridges 0-10 are fully free)
# Pair 12: in constraint component {12,13}
# Let's use pairs 0-11 (12 pairs, 11 bridges) as the clean zone.

print(f"  Upper canon clean zone: pairs 0-11 (12 pairs, 11 bridges)")
print(f"  These pairs have ZERO S=2 constraints.")
print()

# KW upper-canon signals
print(f"  KW upper-canon signals:")
print(f"    Kernel chi² (bridges 0-11): {kw['uc_chi2']:.2f}")
print(f"    Binary-high first (pairs 0-14): {kw['uc_binhigh']}/15")
print(f"    M-score (upper canon M-decisive): {kw['uc_m_score']}/{kw['uc_m_total']}")

# p-values
p_uc_chi2 = np.mean(all_uc_chi2 <= kw['uc_chi2'])
p_uc_bh = np.mean(all_uc_bh >= kw['uc_binhigh'])
p_uc_m = np.mean(all_uc_m >= kw['uc_m_score'])

print(f"\n  P(uc_chi² ≤ KW) = {p_uc_chi2:.4f}")
print(f"  P(uc_binhigh ≥ KW) = {p_uc_bh:.4f}")
print(f"  P(uc_m ≥ KW) = {p_uc_m:.4f}")

# Upper-canon pairwise correlations
r_uc_chi2_bh = np.corrcoef(all_uc_chi2, all_uc_bh)[0, 1]
r_uc_chi2_m = np.corrcoef(all_uc_chi2, all_uc_m)[0, 1]
r_uc_bh_m = np.corrcoef(all_uc_bh, all_uc_m)[0, 1]

print(f"\n  Upper-canon pairwise correlations:")
print(f"    r(uc_chi², uc_binhigh) = {r_uc_chi2_bh:+.4f}")
print(f"    r(uc_chi², uc_m)       = {r_uc_chi2_m:+.4f}")
print(f"    r(uc_binhigh, uc_m)    = {r_uc_bh_m:+.4f}")

# Upper-canon joint
uc_joint = np.mean((all_uc_chi2 <= kw['uc_chi2']) & (all_uc_bh >= kw['uc_binhigh']))
uc_indep = p_uc_chi2 * p_uc_bh
print(f"\n  Upper-canon joint P(chi² ≤ KW AND binhigh ≥ KW) = {uc_joint:.5f}")
print(f"  If independent: {uc_indep:.5f}")
if uc_indep > 0:
    print(f"  Ratio: {uc_joint/uc_indep:.2f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PARTIAL CORRELATIONS CONTROLLING FOR CONSTRAINT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("4. PARTIAL CORRELATIONS CONTROLLING FOR CONSTRAINT CONFIGURATION")
print("=" * 80)
print()

# The constraint configuration is a 5-bit variable (32 possible states,
# but only 2^5 = 32 valid constraint states exist, and each has equal probability
# since the constraints are independent).
# We can compute within-stratum correlations.

# Group samples by constraint configuration
config_groups = defaultdict(list)
for i in range(N_SAMPLES):
    config_groups[all_cc[i]].append(i)

print(f"  Constraint configurations: {len(config_groups)} distinct")
print(f"  Expected: 2^5 = 32 (each with ~{N_SAMPLES/32:.0f} samples)")

# Sizes
sizes = [len(v) for v in config_groups.values()]
print(f"  Sizes: min={min(sizes)}, max={max(sizes)}, mean={np.mean(sizes):.0f}")

# Compute within-stratum correlations (weighted average)
def partial_correlation(x, y, groups):
    """Compute partial correlation of x and y controlling for group membership."""
    # Pool within-group deviations
    x_resid = np.empty_like(x)
    y_resid = np.empty_like(y)
    for indices in groups.values():
        idx = np.array(indices)
        x_resid[idx] = x[idx] - x[idx].mean()
        y_resid[idx] = y[idx] - y[idx].mean()
    
    # Correlation of residuals
    if np.std(x_resid) == 0 or np.std(y_resid) == 0:
        return 0.0
    return np.corrcoef(x_resid, y_resid)[0, 1]

r_partial_chi2_asym = partial_correlation(all_chi2, all_asym, config_groups)
r_partial_chi2_m = partial_correlation(all_chi2, all_m, config_groups)
r_partial_asym_m = partial_correlation(all_asym, all_m, config_groups)

print(f"\n  Partial correlations (controlling for constraint config):")
print(f"    r_partial(chi², asym) = {r_partial_chi2_asym:+.4f}  (raw: {r_chi2_asym:+.4f})")
print(f"    r_partial(chi², m)    = {r_partial_chi2_m:+.4f}  (raw: {r_chi2_m:+.4f})")
print(f"    r_partial(asym, m)    = {r_partial_asym_m:+.4f}  (raw: {r_asym_m:+.4f})")

# Check: do any pairwise correlations COLLAPSE when controlling for constraints?
print(f"\n  Correlation changes:")
for name, raw, partial in [
    ("chi²,asym", r_chi2_asym, r_partial_chi2_asym),
    ("chi²,m", r_chi2_m, r_partial_chi2_m),
    ("asym,m", r_asym_m, r_partial_asym_m),
]:
    change = partial - raw
    collapsed = abs(partial) < 0.01 and abs(raw) > 0.02
    print(f"    {name:>12s}: raw={raw:+.4f} → partial={partial:+.4f} "
          f"(Δ={change:+.4f}) {'COLLAPSED' if collapsed else ''}")

# Conditional p-values within each constraint stratum
print(f"\n  Within-stratum p-values (averaged):")
stratum_p_chi2 = []
stratum_p_asym = []
stratum_p_m = []
for config, indices in config_groups.items():
    if len(indices) < 100:
        continue
    idx = np.array(indices)
    stratum_p_chi2.append(np.mean(all_chi2[idx] <= kw['chi2']))
    stratum_p_asym.append(np.mean(all_asym[idx] >= kw['canon_asym']))
    stratum_p_m.append(np.mean(all_m[idx] >= kw['m_score']))

print(f"    P(chi² ≤ KW): mean={np.mean(stratum_p_chi2):.4f} "
      f"range=[{min(stratum_p_chi2):.4f}, {max(stratum_p_chi2):.4f}]")
print(f"    P(asym ≥ KW): mean={np.mean(stratum_p_asym):.4f} "
      f"range=[{min(stratum_p_asym):.4f}, {max(stratum_p_asym):.4f}]")
print(f"    P(m ≥ KW):    mean={np.mean(stratum_p_m):.4f} "
      f"range=[{min(stratum_p_m):.4f}, {max(stratum_p_m):.4f}]")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SUMMARY: SIGNAL INDEPENDENCE MATRIX
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("5. SIGNAL INDEPENDENCE MATRIX")
print("=" * 80)
print()

print("  Correlation matrix (raw):")
print(f"                chi²    asym    m_score")
print(f"    chi²     {1.000:+.4f}  {r_chi2_asym:+.4f}  {r_chi2_m:+.4f}")
print(f"    asym     {r_chi2_asym:+.4f}  {1.000:+.4f}  {r_asym_m:+.4f}")
print(f"    m_score  {r_chi2_m:+.4f}  {r_asym_m:+.4f}  {1.000:+.4f}")

print()
print("  Correlation matrix (partial, controlling for constraint config):")
print(f"                chi²    asym    m_score")
print(f"    chi²     {1.000:+.4f}  {r_partial_chi2_asym:+.4f}  {r_partial_chi2_m:+.4f}")
print(f"    asym     {r_partial_chi2_asym:+.4f}  {1.000:+.4f}  {r_partial_asym_m:+.4f}")
print(f"    m_score  {r_partial_chi2_m:+.4f}  {r_partial_asym_m:+.4f}  {1.000:+.4f}")

print()
print("  Joint p-values vs independence expectation:")
print(f"    {'Pair':>15s}  {'Observed':>10s}  {'Expected':>10s}  {'Ratio':>8s}")
print(f"    {'-'*48}")
print(f"    {'chi²+asym':>15s}  {j_chi2_asym:10.5f}  {p_chi2*p_asym:10.5f}  "
      f"{j_chi2_asym/(p_chi2*p_asym) if p_chi2*p_asym>0 else 0:8.2f}")
print(f"    {'chi²+m':>15s}  {j_chi2_m:10.5f}  {p_chi2*p_m:10.5f}  "
      f"{j_chi2_m/(p_chi2*p_m) if p_chi2*p_m>0 else 0:8.2f}")
print(f"    {'asym+m':>15s}  {j_asym_m:10.5f}  {p_asym*p_m:10.5f}  "
      f"{j_asym_m/(p_asym*p_m) if p_asym*p_m>0 else 0:8.2f}")
print(f"    {'all three':>15s}  {j_all:10.6f}  {indep_all:10.6f}  "
      f"{j_all/indep_all if indep_all>0 else 0:8.2f}")

# Constraint-mediation assessment
print()
print("  Constraint-mediation assessment:")
m_survived = kw['m_score_free'] >= kw['m_total_free'] * 0.7  # >70% in free pairs
print(f"    M-component in free pairs: {kw['m_score_free']}/{kw['m_total_free']} "
      f"({100*kw['m_score_free']/kw['m_total_free'] if kw['m_total_free']>0 else 0:.0f}%) "
      f"{'→ SURVIVES' if m_survived else '→ WEAKENS'}")
print(f"    M-component in constrained pairs: {kw['m_score_constrained']}/{kw['m_total_constrained']}")


print()
print("=" * 80)
print("THREE-SIGNAL ANALYSIS COMPLETE")
print("=" * 80)
