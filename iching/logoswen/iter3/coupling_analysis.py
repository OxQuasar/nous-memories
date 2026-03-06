"""
Coupling Analysis: Kernel Uniformity × Canon Asymmetry

The observed joint p(chi² ≤ 2.29 AND asymmetry ≥ +3) = 0.0052,
vs 0.0029 expected under independence (ratio 1.79).

This script determines whether the coupling is:
(a) genuine holistic constraint,
(b) S=2 geography artifact, or
(c) sampling noise.

Four analyses:
1. Stratify by constraint configuration (16 strata)
2. Free-pairs-only test (hold constrained pairs fixed)
3. Bridge sensitivity map (per-bridge contribution)
4. Large-sample confirmation (500K with confidence intervals)
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

ALL_GEN_NAMES = list(VALID_MASKS.values())

# ── Build pairs ──────────────────────────────────────────────────────────────

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


# ── S=2 constraints ─────────────────────────────────────────────────────────

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

# Constraint components: {13,14}, {19,20}, {25,26}, {27,28}, {29,30}
# Each bridge constraint forces o_k = o_{k+1} (equality) or fixes a value
CONSTRAINED_PAIRS = set()
for k in CONSTRAINTS:
    CONSTRAINED_PAIRS.add(k)
    CONSTRAINED_PAIRS.add(k+1)

FREE_PAIRS = sorted(set(range(32)) - CONSTRAINED_PAIRS)

# Components
COMPONENTS = [(13, 14), (19, 20), (25, 26), (27, 28), (29, 30)]

# For each component, what are the valid (o_k, o_{k+1}) pairs?
COMPONENT_VALID = {}
for p1, p2 in COMPONENTS:
    bridge_k = p1  # bridge between pair p1 and pair p1+1 = p2
    if bridge_k in CONSTRAINTS:
        forbidden = CONSTRAINTS[bridge_k]
        valid = [(o1, o2) for o1 in [0,1] for o2 in [0,1] if (o1, o2) not in forbidden]
        COMPONENT_VALID[(p1, p2)] = valid

print("Constraint components and their valid states:")
for comp, valid in COMPONENT_VALID.items():
    print(f"  Pairs {comp}: valid = {valid}")


def is_s2_free(o):
    for k, forbidden in CONSTRAINTS.items():
        if (o[k], o[k+1]) in forbidden:
            return False
    return True


# ── Metrics ──────────────────────────────────────────────────────────────────

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


def compute_metrics(o):
    """Return (kernel_chi2, canon_asymmetry) for an orientation vector."""
    seq = build_sequence(o)
    
    # Kernel chi²
    freq = Counter()
    for k in range(31):
        name = kernel_name(seq[2*k+1], seq[2*k+2])
        freq[name] += 1
    expected = 31 / 8
    chi2 = sum((freq.get(g, 0) - expected)**2 / expected for g in ALL_GEN_NAMES)
    
    # Canon asymmetry
    def to_int(h):
        v = 0
        for bit in h:
            v = v * 2 + bit
        return v
    
    upper_bh = sum(1 for k in range(15) if to_int(seq[2*k]) > to_int(seq[2*k+1]))
    lower_bh = sum(1 for k in range(15, 32) if to_int(seq[2*k]) > to_int(seq[2*k+1]))
    asym = upper_bh - lower_bh
    
    return chi2, asym


def sample_s2_free(rng):
    """Sample a uniformly random S=2-free orientation."""
    while True:
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        if is_s2_free(o):
            return o


# ── KW baseline ──────────────────────────────────────────────────────────────

KW_O = [0] * 32
KW_CHI2, KW_ASYM = compute_metrics(KW_O)
print(f"\nKW baseline: chi² = {KW_CHI2:.4f}, canon_asym = {KW_ASYM}")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. STRATIFY BY CONSTRAINT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("1. STRATIFY BY CONSTRAINT CONFIGURATION")
print("=" * 80)
print()

# There are 5 constraint components, each with 2 valid states.
# Total configurations: 2^5 = 32.
# For each configuration, sample orientations with those constraint values
# and measure the chi²–asym correlation WITHIN the stratum.

N_PER_STRATUM = 20_000

# Enumerate constraint configurations
configs = []
for c0 in range(2):
    for c1 in range(2):
        for c2 in range(2):
            for c3 in range(2):
                for c4 in range(2):
                    configs.append((c0, c1, c2, c3, c4))

print(f"Total constraint configurations: {len(configs)}")
print(f"Samples per stratum: {N_PER_STRATUM}")
print()

t0 = time.time()

stratum_results = {}
for ci, config in enumerate(configs):
    # Set the constrained pairs according to this configuration
    # Component (p1, p2) with valid states [(v1a, v1b), (v2a, v2b)]
    # config[i] selects which valid state to use
    
    fixed = {}
    for i, ((p1, p2), valid) in enumerate(COMPONENT_VALID.items()):
        state = valid[config[i]]  # (o_p1, o_p2)
        fixed[p1] = state[0]
        fixed[p2] = state[1]
    
    rng = random.Random(42 + ci)
    chi2_vals = []
    asym_vals = []
    
    for _ in range(N_PER_STRATUM):
        o = [0] * 32
        # Set constrained pairs
        for p, v in fixed.items():
            o[p] = v
        # Randomize free pairs
        for p in FREE_PAIRS:
            o[p] = rng.randint(0, 1)
        
        chi2, asym = compute_metrics(o)
        chi2_vals.append(chi2)
        asym_vals.append(asym)
    
    chi2_arr = np.array(chi2_vals)
    asym_arr = np.array(asym_vals)
    
    if chi2_arr.std() > 0 and asym_arr.std() > 0:
        corr = np.corrcoef(chi2_arr, asym_arr)[0, 1]
    else:
        corr = 0.0
    
    # Joint p-value within stratum
    p_chi2 = np.mean(chi2_arr <= KW_CHI2)
    p_asym = np.mean(asym_arr >= KW_ASYM)
    joint = np.mean((chi2_arr <= KW_CHI2) & (asym_arr >= KW_ASYM))
    expected = p_chi2 * p_asym
    ratio = joint / expected if expected > 0 else float('inf')
    
    stratum_results[config] = {
        'corr': corr,
        'p_chi2': p_chi2,
        'p_asym': p_asym,
        'joint': joint,
        'expected': expected,
        'ratio': ratio,
        'chi2_mean': chi2_arr.mean(),
        'asym_mean': asym_arr.mean(),
    }

t1 = time.time()
print(f"Completed in {t1-t0:.1f}s\n")

# Summary table
print(f"{'Config':>7s}  {'r(χ²,asym)':>10s}  {'p(χ²≤KW)':>9s}  {'p(as≥KW)':>9s}  "
      f"{'p(joint)':>9s}  {'p(indep)':>9s}  {'ratio':>6s}  {'χ²_mean':>7s}  {'as_mean':>7s}")
print("─" * 90)

corrs = []
ratios = []
for config in configs:
    r = stratum_results[config]
    corrs.append(r['corr'])
    ratios.append(r['ratio'])
    kw_marker = " ★" if config == (0, 0, 0, 0, 0) else ""
    print(f"{''.join(map(str,config)):>7s}  {r['corr']:+10.4f}  {r['p_chi2']:9.4f}  "
          f"{r['p_asym']:9.4f}  {r['joint']:9.5f}  {r['expected']:9.5f}  "
          f"{r['ratio']:6.2f}  {r['chi2_mean']:7.2f}  {r['asym_mean']:+7.2f}{kw_marker}")

corrs = np.array(corrs)
ratios = np.array(ratios)

print(f"\nWithin-stratum correlation summary:")
print(f"  Mean r: {corrs.mean():+.4f}")
print(f"  Std r:  {corrs.std():.4f}")
print(f"  Min r:  {corrs.min():+.4f}")
print(f"  Max r:  {corrs.max():+.4f}")
print(f"  Fraction r > 0: {np.mean(corrs > 0):.3f}")

# Key question: does the coupling vanish within strata?
print(f"\nWithin-stratum dependence ratio summary:")
print(f"  Mean ratio: {ratios.mean():.3f}")
print(f"  Median ratio: {np.median(ratios):.3f}")
print(f"  Fraction ratio > 1.0: {np.mean(ratios > 1.0):.3f}")
print(f"  Fraction ratio > 1.5: {np.mean(ratios > 1.5):.3f}")

# Compare to the overall ratio of 1.79
print(f"\n  Overall ratio (50K from prior work): 1.79")
print(f"  Mean within-stratum ratio: {ratios.mean():.3f}")
if ratios.mean() > 1.3:
    print(f"  → Coupling PERSISTS within strata → GENUINE (not constraint-mediated)")
elif ratios.mean() < 0.9:
    print(f"  → Coupling VANISHES within strata → CONSTRAINT-MEDIATED artifact")
else:
    print(f"  → Coupling WEAKENS but persists → PARTIALLY constraint-mediated")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FREE-PAIRS-ONLY TEST
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("2. FREE-PAIRS-ONLY TEST")
print("   Hold constrained components at KW values; randomize only free pairs")
print("=" * 80)
print()

# KW's constrained values
kw_constrained = {}
for p1, p2 in COMPONENTS:
    kw_constrained[p1] = KW_O[p1]
    kw_constrained[p2] = KW_O[p2]

print(f"KW constrained values: {dict(sorted(kw_constrained.items()))}")
print(f"Free pairs: {FREE_PAIRS} ({len(FREE_PAIRS)} pairs)")
print()

N_FREE = 200_000
rng_free = random.Random(123)

free_chi2 = []
free_asym = []

for _ in range(N_FREE):
    o = [0] * 32
    for p, v in kw_constrained.items():
        o[p] = v
    for p in FREE_PAIRS:
        o[p] = rng_free.randint(0, 1)
    
    chi2, asym = compute_metrics(o)
    free_chi2.append(chi2)
    free_asym.append(asym)

free_chi2 = np.array(free_chi2)
free_asym = np.array(free_asym)

corr_free = np.corrcoef(free_chi2, free_asym)[0, 1]
p_chi2_free = np.mean(free_chi2 <= KW_CHI2)
p_asym_free = np.mean(free_asym >= KW_ASYM)
joint_free = np.mean((free_chi2 <= KW_CHI2) & (free_asym >= KW_ASYM))
expected_free = p_chi2_free * p_asym_free
ratio_free = joint_free / expected_free if expected_free > 0 else float('inf')

print(f"Results (N={N_FREE}, constrained pairs fixed at KW):")
print(f"  r(chi², asym) = {corr_free:+.4f}")
print(f"  P(chi² ≤ KW) = {p_chi2_free:.4f}")
print(f"  P(asym ≥ KW) = {p_asym_free:.4f}")
print(f"  P(joint) = {joint_free:.5f}")
print(f"  P(independent) = {expected_free:.5f}")
print(f"  Ratio = {ratio_free:.3f}")
print()

if abs(ratio_free - 1.0) < 0.3:
    print(f"  → Under fixed constraints, coupling VANISHES (ratio ≈ 1)")
    print(f"     → The coupling is mediated by constraint configuration variation")
else:
    print(f"  → Under fixed constraints, coupling PERSISTS (ratio = {ratio_free:.2f})")
    print(f"     → The coupling is genuine, not constraint-mediated")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. BRIDGE SENSITIVITY MAP
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("3. BRIDGE SENSITIVITY MAP")
print("   Per-pair contribution to kernel chi² and canon asymmetry")
print("=" * 80)
print()

# For each pair, compute the marginal effect of flipping that pair on each metric.
# Start from KW orientation, flip one pair at a time.

kw_chi2_base, kw_asym_base = compute_metrics(KW_O)

print(f"{'Pair':>5s}  {'Δchi²':>8s}  {'Δasym':>6s}  {'Constrained?':>12s}  "
      f"{'Bridge(s) affected':>20s}")
print("─" * 65)

delta_chi2 = []
delta_asym = []
pair_constrained = []

for p in range(N_PAIRS):
    o_flipped = list(KW_O)
    o_flipped[p] = 1 - o_flipped[p]
    
    chi2_f, asym_f = compute_metrics(o_flipped)
    d_chi2 = chi2_f - kw_chi2_base
    d_asym = asym_f - kw_asym_base
    
    is_const = p in CONSTRAINED_PAIRS
    
    # Which bridges does this pair affect?
    affected_bridges = []
    if p > 0:
        affected_bridges.append(f"B{p-1}(exit)")
    if p < 31:
        affected_bridges.append(f"B{p}(entry)")
    
    delta_chi2.append(d_chi2)
    delta_asym.append(d_asym)
    pair_constrained.append(is_const)
    
    flag = "CONSTRAINED" if is_const else ""
    print(f"  {p+1:3d}  {d_chi2:+8.3f}  {d_asym:+6d}  {flag:>12s}  "
          f"{', '.join(affected_bridges):>20s}")

delta_chi2 = np.array(delta_chi2)
delta_asym = np.array(delta_asym)
pair_constrained = np.array(pair_constrained)

print(f"\nSummary:")
print(f"  Mean |Δchi²| (free pairs):        {np.abs(delta_chi2[~pair_constrained]).mean():.3f}")
print(f"  Mean |Δchi²| (constrained pairs): {np.abs(delta_chi2[pair_constrained]).mean():.3f}")
print(f"  Mean |Δasym| (free pairs):        {np.abs(delta_asym[~pair_constrained]).mean():.3f}")
print(f"  Mean |Δasym| (constrained pairs): {np.abs(delta_asym[pair_constrained]).mean():.3f}")

# Correlation between Δchi² and Δasym across pairs
r_delta = np.corrcoef(delta_chi2, delta_asym)[0, 1]
print(f"\n  r(Δchi², Δasym) across pairs: {r_delta:+.4f}")

# Do the same pairs that improve chi² also improve asym?
# "Improve" = Δchi² < 0 (more uniform) and Δasym > 0 (more positive)
both_improve = sum(1 for i in range(N_PAIRS) if delta_chi2[i] < 0 and delta_asym[i] > 0)
either_improve = sum(1 for i in range(N_PAIRS) 
                     if delta_chi2[i] < 0 or delta_asym[i] > 0)
print(f"\n  Pairs where flipping improves BOTH chi² and asym: {both_improve}/{N_PAIRS}")
print(f"  Pairs where flipping improves chi² (Δ < 0): {sum(delta_chi2 < 0)}/{N_PAIRS}")
print(f"  Pairs where flipping improves asym (Δ > 0): {sum(delta_asym > 0)}/{N_PAIRS}")

# Identify the pairs with strongest coupling (large |Δchi²| AND |Δasym|)
product = np.abs(delta_chi2) * np.abs(delta_asym)
top_coupling = np.argsort(product)[::-1][:10]
print(f"\n  Top 10 coupling-contributing pairs (by |Δchi²| × |Δasym|):")
for idx in top_coupling:
    flag = "CONST" if pair_constrained[idx] else "free"
    print(f"    Pair {idx+1:2d}: Δchi² = {delta_chi2[idx]:+.3f}, "
          f"Δasym = {delta_asym[idx]:+d}, product = {product[idx]:.3f}  [{flag}]")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. LARGE-SAMPLE CONFIRMATION (500K)
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("4. LARGE-SAMPLE CONFIRMATION (500K S=2-free orientations)")
print("=" * 80)
print()

N_LARGE = 500_000
rng_large = random.Random(999)

large_chi2 = np.empty(N_LARGE)
large_asym = np.empty(N_LARGE)

t0 = time.time()
for i in range(N_LARGE):
    o = sample_s2_free(rng_large)
    chi2, asym = compute_metrics(o)
    large_chi2[i] = chi2
    large_asym[i] = asym
    
    if (i + 1) % 100_000 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{N_LARGE} in {elapsed:.1f}s")

t1 = time.time()
print(f"  Completed {N_LARGE} samples in {t1-t0:.1f}s")

# Marginals
p_chi2_L = np.mean(large_chi2 <= KW_CHI2)
p_asym_L = np.mean(large_asym >= KW_ASYM)
joint_L = np.mean((large_chi2 <= KW_CHI2) & (large_asym >= KW_ASYM))
expected_L = p_chi2_L * p_asym_L
ratio_L = joint_L / expected_L if expected_L > 0 else float('inf')

# Confidence intervals via bootstrap
n_boot = 10_000
boot_ratios = []
rng_boot = random.Random(777)

joint_mask = (large_chi2 <= KW_CHI2) & (large_asym >= KW_ASYM)
chi2_mask = large_chi2 <= KW_CHI2
asym_mask = large_asym >= KW_ASYM

for _ in range(n_boot):
    idx = rng_boot.choices(range(N_LARGE), k=N_LARGE)
    b_joint = np.mean(joint_mask[idx])
    b_p1 = np.mean(chi2_mask[idx])
    b_p2 = np.mean(asym_mask[idx])
    b_exp = b_p1 * b_p2
    if b_exp > 0:
        boot_ratios.append(b_joint / b_exp)
    else:
        boot_ratios.append(float('nan'))

boot_ratios = np.array([r for r in boot_ratios if not np.isnan(r)])
ci_lo = np.percentile(boot_ratios, 2.5)
ci_hi = np.percentile(boot_ratios, 97.5)

print(f"\nResults (N={N_LARGE}):")
print(f"  P(chi² ≤ KW)         = {p_chi2_L:.5f}  ({int(p_chi2_L*N_LARGE)}/{N_LARGE})")
print(f"  P(asym ≥ KW)         = {p_asym_L:.5f}  ({int(p_asym_L*N_LARGE)}/{N_LARGE})")
print(f"  P(joint)             = {joint_L:.6f}  ({int(joint_L*N_LARGE)}/{N_LARGE})")
print(f"  P(if independent)    = {expected_L:.6f}")
print(f"  Dependence ratio     = {ratio_L:.3f}")
print(f"  95% CI for ratio     = [{ci_lo:.3f}, {ci_hi:.3f}]")
print(f"  r(chi², asym)        = {np.corrcoef(large_chi2, large_asym)[0,1]:+.4f}")

# Stability check: split into 5 blocks of 100K
print(f"\n  Stability across 100K blocks:")
for block in range(5):
    sl = slice(block * 100_000, (block + 1) * 100_000)
    b_joint = np.mean((large_chi2[sl] <= KW_CHI2) & (large_asym[sl] >= KW_ASYM))
    b_p1 = np.mean(large_chi2[sl] <= KW_CHI2)
    b_p2 = np.mean(large_asym[sl] >= KW_ASYM)
    b_exp = b_p1 * b_p2
    b_ratio = b_joint / b_exp if b_exp > 0 else float('inf')
    print(f"    Block {block+1}: p_joint={b_joint:.5f}, ratio={b_ratio:.3f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SYNTHESIS
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("5. SYNTHESIS")
print("=" * 80)
print()

print("Coupling mechanism determination:")
print()
print(f"  Overall dependence ratio (500K): {ratio_L:.3f}  95% CI [{ci_lo:.3f}, {ci_hi:.3f}]")
print(f"  Mean within-stratum ratio:       {ratios.mean():.3f}")
print(f"  Free-pairs-only ratio:           {ratio_free:.3f}")
print(f"  r(Δchi², Δasym) across pairs:    {r_delta:+.4f}")
print()

# Decision logic
if ci_hi < 1.2:
    verdict = "SAMPLING NOISE — ratio consistent with 1.0"
elif ratios.mean() < 1.1 and ratio_free < 1.1:
    verdict = "S=2 GEOGRAPHY ARTIFACT — coupling vanishes when constraints are controlled"
elif ratios.mean() > 1.3 and ratio_free > 1.3:
    verdict = "GENUINE HOLISTIC CONSTRAINT — coupling persists within all strata"
elif ratios.mean() > 1.2 and ratio_free < 1.2:
    verdict = "PARTIALLY CONSTRAINT-MEDIATED — coupling from cross-stratum variation"
elif ratio_free > 1.2 and ratios.mean() < 1.2:
    verdict = "GENUINE BUT WEAK — free pairs drive the coupling"
else:
    verdict = "MIXED — requires further investigation"

print(f"  VERDICT: {verdict}")
print()

# Additional detail
if abs(r_delta) > 0.3:
    print(f"  The per-pair sensitivity analysis shows that flipping pairs tends to")
    print(f"  move chi² and asymmetry in the {'same' if r_delta > 0 else 'opposite'} direction")
    print(f"  (r = {r_delta:+.3f}), meaning the two metrics share {'positive' if r_delta > 0 else 'negative'}")
    print(f"  sensitivity to the same pair orientations.")
else:
    print(f"  The per-pair sensitivities are weakly correlated (r = {r_delta:+.3f}),")
    print(f"  meaning chi² and asymmetry respond to DIFFERENT pairs.")
    print(f"  The coupling, if genuine, is a COLLECTIVE property — not traceable")
    print(f"  to individual pairs.")

print()
print("=" * 80)
print("COUPLING ANALYSIS COMPLETE")
print("=" * 80)
