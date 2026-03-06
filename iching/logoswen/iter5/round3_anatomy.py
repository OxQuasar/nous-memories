"""
Iter5 Round 3: Anatomy, Annealing, Substrate Effects, M-Rule Exceptions

Priority 1: Anatomy of the Hamming-4 neighbor (R2-Ef "m dominant")
Priority 2: Simulated annealing with minimax and L1 objectives
Priority 3: Asymmetry as substrate effect
Priority 4: KW's M-rule exceptions
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
from infra import *

import json
import time
import math

# ══════════════════════════════════════════════════════════════════════════════
# LOAD PRIOR DATA
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter5/round2e_fixed_data.json') as f:
    r2e_data = json.load(f)

with open('/home/quasar/nous/logoswen/iter5/round1_data.json') as f:
    r1_data = json.load(f)

print("=" * 80)
print("ITER5 ROUND 3")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}  asym={KW_ASYM}  "
      f"m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()

all_results = {'kw_baseline': KW_METRICS}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 1: ANATOMY OF THE HAMMING-4 NEIGHBOR
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("PRIORITY 1: ANATOMY OF HAMMING-4 NEIGHBOR (R2-Ef 'm dominant')")
print("=" * 80)
print()

# Extract m-dominant orientation
m_dom = None
for r in r2e_data['R2-E-fixed']:
    if r['label'] == 'm dominant':
        m_dom = r
        break

m_dom_o = m_dom['orientation']
m_dom_metrics = m_dom['metrics']

# Identify differing bit positions
diff_bits = [i for i in range(32) if m_dom_o[i] != KW_O[i]]
print(f"M-dominant orientation: {orientation_str(m_dom_o)}")
print(f"Differing bits (pair indices): {diff_bits}")
print(f"Hamming from KW: {m_dom['hamming_from_kw']}")
print(f"Metrics: chi²={m_dom_metrics['chi2']:.4f}  asym={m_dom_metrics['asym']}  "
      f"m={m_dom_metrics['m_score']}  kac={m_dom_metrics['kac']:.4f}")
print()

# Per-bit analysis
print("PER-BIT ANALYSIS:")
print(f"{'pair':>4s} {'M-dec':>5s} {'L2a':>3s} {'L5a':>3s}  "
      f"{'Δχ²':>8s} {'Δasym':>6s} {'Δm':>4s} {'Δkac':>8s}  "
      f"{'4-axis':>15s}  {'kernel effect':>30s}")
print("─" * 100)

single_bit_deltas = []
kw_seq = build_sequence(KW_O)

for bit_pos in diff_bits:
    a = PAIRS[bit_pos]['a']
    m_dec = bit_pos in set(M_DECISIVE)
    
    # Single-bit flip from KW
    o_flip = list(KW_O)
    o_flip[bit_pos] = 1
    assert is_s2_free(o_flip), f"Single flip at {bit_pos} violates S=2"
    
    flip_metrics = compute_all_metrics(o_flip)
    d_chi2 = flip_metrics['chi2'] - KW_CHI2
    d_asym = flip_metrics['asym'] - KW_ASYM
    d_m = flip_metrics['m_score'] - KW_M
    d_kac = flip_metrics['kac'] - KW_KAC
    
    # 4-axis Pareto status
    axes = per_axis_comparison(flip_metrics)
    pareto = pareto_compare(flip_metrics)
    
    # Kernel effect at adjacent bridges
    flip_seq = build_sequence(o_flip)
    kernel_effects = []
    for bk in range(max(0, bit_pos - 1), min(31, bit_pos + 1)):
        kw_kern = kernel_name(kw_seq[2*bk+1], kw_seq[2*bk+2])
        flip_kern = kernel_name(flip_seq[2*bk+1], flip_seq[2*bk+2])
        if kw_kern != flip_kern:
            kernel_effects.append(f"B{bk}:{kw_kern}→{flip_kern}")
    kern_str = ', '.join(kernel_effects) if kernel_effects else '(no change)'
    
    print(f"{bit_pos:4d} {'Y' if m_dec else 'N':>5s} {a[1]:3d} {a[4]:3d}  "
          f"{d_chi2:+8.3f} {d_asym:+6d} {d_m:+4d} {d_kac:+8.4f}  "
          f"{pareto:>15s}  {kern_str:>30s}")
    
    single_bit_deltas.append({
        'pair': bit_pos, 'm_decisive': m_dec, 'L2_a': a[1], 'L5_a': a[4],
        'd_chi2': d_chi2, 'd_asym': d_asym, 'd_m': d_m, 'd_kac': d_kac,
        'pareto': pareto, 'kernel_effects': kernel_effects,
    })

print()

# Additive prediction vs actual combined effect
sum_d_chi2 = sum(d['d_chi2'] for d in single_bit_deltas)
sum_d_asym = sum(d['d_asym'] for d in single_bit_deltas)
sum_d_m = sum(d['d_m'] for d in single_bit_deltas)
sum_d_kac = sum(d['d_kac'] for d in single_bit_deltas)

actual_d_chi2 = m_dom_metrics['chi2'] - KW_CHI2
actual_d_asym = m_dom_metrics['asym'] - KW_ASYM
actual_d_m = m_dom_metrics['m_score'] - KW_M
actual_d_kac = m_dom_metrics['kac'] - KW_KAC

print("ADDITIVITY TEST (4-bit combined effect):")
print(f"{'':>12s} {'Δχ²':>8s} {'Δasym':>6s} {'Δm':>4s} {'Δkac':>8s}")
print("─" * 42)
print(f"{'Additive':>12s} {sum_d_chi2:+8.3f} {sum_d_asym:+6d} {sum_d_m:+4d} {sum_d_kac:+8.4f}")
print(f"{'Actual':>12s} {actual_d_chi2:+8.3f} {actual_d_asym:+6d} {actual_d_m:+4d} {actual_d_kac:+8.4f}")
print(f"{'Epistasis':>12s} {actual_d_chi2-sum_d_chi2:+8.3f} {actual_d_asym-sum_d_asym:+6d} "
      f"{actual_d_m-sum_d_m:+4d} {actual_d_kac-sum_d_kac:+8.4f}")
print()

# Are these the m-for-kac trade points?
print("INTERPRETATION:")
m_dec_flips = [d for d in single_bit_deltas if d['m_decisive']]
non_m_flips = [d for d in single_bit_deltas if not d['m_decisive']]
m_improving = [d for d in single_bit_deltas if d['d_m'] > 0]
kac_worsening = [d for d in single_bit_deltas if d['d_kac'] > 0]

print(f"  M-decisive pairs among the 4 flips: {len(m_dec_flips)}")
print(f"  Flips that improve m-score: {len(m_improving)} (pairs: {[d['pair'] for d in m_improving]})")
print(f"  Flips that worsen kac: {len(kac_worsening)} (pairs: {[d['pair'] for d in kac_worsening]})")
print(f"  All 4 flips improve m AND worsen kac? {len(m_improving) == 4 and len(kac_worsening) == 4}")
print()

# Does flipping these 4 bits from the m-dominant orientation back to KW
# correspond exactly to "sacrifice m for kac"?
print(f"  m-dominant → KW means: reverse these 4 flips")
print(f"  Net trade: Δm={actual_d_m:+d} → KW has m={KW_M} vs m-dom has m={m_dom_metrics['m_score']}")
print(f"  Net trade: Δkac={actual_d_kac:+.4f} → KW has kac={KW_KAC:.4f} vs m-dom has kac={m_dom_metrics['kac']:.4f}")
print(f"  KW sacrifices {-actual_d_m} m-score points to gain {-actual_d_kac:.4f} kac improvement")
print()

all_results['P1_anatomy'] = {
    'diff_bits': diff_bits,
    'm_dom_orientation': m_dom_o,
    'm_dom_metrics': m_dom_metrics,
    'single_bit_deltas': single_bit_deltas,
    'additivity': {
        'predicted': {'chi2': sum_d_chi2, 'asym': sum_d_asym, 'm': sum_d_m, 'kac': sum_d_kac},
        'actual': {'chi2': actual_d_chi2, 'asym': actual_d_asym, 'm': actual_d_m, 'kac': actual_d_kac},
        'epistasis': {
            'chi2': actual_d_chi2 - sum_d_chi2,
            'asym': actual_d_asym - sum_d_asym,
            'm': actual_d_m - sum_d_m,
            'kac': actual_d_kac - sum_d_kac,
        },
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 4: KW's M-RULE EXCEPTIONS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("PRIORITY 4: KW's M-RULE EXCEPTIONS")
print("=" * 80)
print()

# For each M-decisive pair, check if KW follows the M-rule
m_decisive_set = set(M_DECISIVE)
exceptions = []
conforming = []

for k in M_DECISIVE:
    a = PAIRS[k]['a']
    # M-rule: put L2=yin (0) first
    # KW has o[k]=0, so first hex is a
    kw_first_l2 = a[1]  # L2 of the first hexagram under KW orientation
    m_rule_wants = 0  # L2=yin=0 first
    
    if kw_first_l2 != m_rule_wants:
        exceptions.append(k)
    else:
        conforming.append(k)

print(f"M-decisive pairs: {len(M_DECISIVE)}")
print(f"KW follows M-rule: {len(conforming)}/{len(M_DECISIVE)}")
print(f"KW exceptions (L2=yang first): {exceptions}")
print()

# For each exception, analyze the kernel context
print("EXCEPTION ANALYSIS:")
print(f"{'pair':>4s} {'L2a':>3s} {'L5a':>3s}  "
      f"{'Δχ²':>8s} {'Δasym':>6s} {'Δm':>4s} {'Δkac':>8s}  "
      f"{'kac improves?':>13s}  {'kernel context':>35s}")
print("─" * 110)

exception_data = []
for k in exceptions:
    a = PAIRS[k]['a']
    
    # What if we flip to M-rule? (flip bit k from 0 to 1)
    o_mrule = list(KW_O)
    o_mrule[k] = 1
    
    if not is_s2_free(o_mrule):
        print(f"{k:4d} {a[1]:3d} {a[4]:3d}  {'S=2 VIOLATION — cannot flip':>60s}")
        exception_data.append({
            'pair': k, 'L2_a': a[1], 'L5_a': a[4],
            's2_violation': True,
        })
        continue
    
    mrule_metrics = compute_all_metrics(o_mrule)
    d_chi2 = mrule_metrics['chi2'] - KW_CHI2
    d_asym = mrule_metrics['asym'] - KW_ASYM
    d_m = mrule_metrics['m_score'] - KW_M
    d_kac = mrule_metrics['kac'] - KW_KAC
    
    kac_improves = d_kac < -1e-9
    
    # Kernel context: bridges around this pair
    mrule_seq = build_sequence(o_mrule)
    kern_context = []
    for bk in range(max(0, k-1), min(31, k+1)):
        kw_kern = kernel_name(kw_seq[2*bk+1], kw_seq[2*bk+2])
        mr_kern = kernel_name(mrule_seq[2*bk+1], mrule_seq[2*bk+2])
        if kw_kern != mr_kern:
            kern_context.append(f"B{bk}:{kw_kern}→{mr_kern}")
    kern_str = ', '.join(kern_context) if kern_context else '(no change)'
    
    print(f"{k:4d} {a[1]:3d} {a[4]:3d}  "
          f"{d_chi2:+8.3f} {d_asym:+6d} {d_m:+4d} {d_kac:+8.4f}  "
          f"{'YES' if kac_improves else 'NO':>13s}  {kern_str:>35s}")
    
    exception_data.append({
        'pair': k, 'L2_a': a[1], 'L5_a': a[4],
        's2_violation': False,
        'd_chi2': d_chi2, 'd_asym': d_asym, 'd_m': d_m, 'd_kac': d_kac,
        'kac_improves_if_flipped': kac_improves,
        'kernel_context': kern_context,
    })

print()

# Summary: does KW always prefer the kac-better choice at exceptions?
non_s2 = [e for e in exception_data if not e.get('s2_violation', False)]
# Note: "kac_improves_if_flipped" means flipping TO M-rule would improve kac.
# KW chose AGAINST the M-rule. So if flipping to M-rule improves kac, KW is
# choosing WORSE kac (opposite of what we'd expect).
# If flipping to M-rule WORSENS kac, then KW's choice preserves kac (expected).
kw_preserves_kac = [e for e in non_s2 if not e['kac_improves_if_flipped']]
kw_sacrifices_kac = [e for e in non_s2 if e['kac_improves_if_flipped']]

print(f"At M-rule exceptions (flipping TO M-rule):")
print(f"  Worsens kac (KW preserves kac): {len(kw_preserves_kac)} pairs")
print(f"  Improves kac (KW sacrifices kac): {len(kw_sacrifices_kac)} pairs")
print()
print(f"Interpretation: KW deviates from M-rule at pairs where following it would")
if len(kw_preserves_kac) > len(kw_sacrifices_kac):
    print(f"  worsen kac → KW is protecting sequential diversity over M-preference")
else:
    print(f"  NOT primarily to protect kac — pattern is more complex")
print()

all_results['P4_m_exceptions'] = {
    'exceptions': exceptions,
    'conforming': conforming,
    'exception_data': exception_data,
    'summary': {
        'n_exceptions': len(exceptions),
        'kw_preserves_kac': len(kw_preserves_kac),
        'kw_sacrifices_kac': len(kw_sacrifices_kac),
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 3: ASYMMETRY AS SUBSTRATE EFFECT
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("PRIORITY 3: ASYMMETRY AS SUBSTRATE EFFECT")
print("=" * 80)
print()

# Sample 10K random S=2-free orientations, compute metrics
N_SAMPLE = 10_000
rng_p3 = random.Random(42)

all_chi2 = np.empty(N_SAMPLE)
all_asym = np.empty(N_SAMPLE)
all_m = np.empty(N_SAMPLE)
all_kac = np.empty(N_SAMPLE)

t0 = time.time()
for i in range(N_SAMPLE):
    o = sample_s2_free(rng_p3)
    m = compute_all_metrics(o)
    all_chi2[i] = m['chi2']
    all_asym[i] = m['asym']
    all_m[i] = m['m_score']
    all_kac[i] = m['kac']
    if (i+1) % 2000 == 0:
        print(f"  ... {i+1}/{N_SAMPLE} ({time.time()-t0:.1f}s)")

print(f"  Sampling complete: {time.time()-t0:.1f}s")
print()

# Unconditional statistics
print("UNCONDITIONAL STATISTICS:")
print(f"  asym:  mean={np.mean(all_asym):.3f}  std={np.std(all_asym):.3f}  "
      f"median={np.median(all_asym):.0f}")
print(f"  chi²:  mean={np.mean(all_chi2):.3f}  std={np.std(all_chi2):.3f}")
print(f"  m:     mean={np.mean(all_m):.3f}  std={np.std(all_m):.3f}")
print(f"  kac:   mean={np.mean(all_kac):.4f}  std={np.std(all_kac):.4f}")
print()

# Conditional on kernel-balanced (chi² < 3.0)
chi2_mask = all_chi2 < 3.0
n_balanced = np.sum(chi2_mask)
print(f"CONDITIONAL ON χ² < 3.0 ({n_balanced} samples, {100*n_balanced/N_SAMPLE:.1f}%):")
if n_balanced > 0:
    print(f"  asym:  mean={np.mean(all_asym[chi2_mask]):.3f}  "
          f"std={np.std(all_asym[chi2_mask]):.3f}  "
          f"median={np.median(all_asym[chi2_mask]):.0f}")
    print(f"  m:     mean={np.mean(all_m[chi2_mask]):.3f}")
    print(f"  kac:   mean={np.mean(all_kac[chi2_mask]):.4f}")
else:
    print("  (no samples with chi² < 3.0)")
print()

# Conditional on strong kac (kac < -0.3)
kac_mask = all_kac < -0.3
n_strong_kac = np.sum(kac_mask)
print(f"CONDITIONAL ON kac < −0.3 ({n_strong_kac} samples, {100*n_strong_kac/N_SAMPLE:.1f}%):")
if n_strong_kac > 0:
    print(f"  asym:  mean={np.mean(all_asym[kac_mask]):.3f}  "
          f"std={np.std(all_asym[kac_mask]):.3f}  "
          f"median={np.median(all_asym[kac_mask]):.0f}")
    print(f"  chi²:  mean={np.mean(all_chi2[kac_mask]):.3f}")
    print(f"  m:     mean={np.mean(all_m[kac_mask]):.3f}")
else:
    print("  (no samples)")
print()

# Conditional on both (chi² < 3.0 AND kac < -0.3)
both_mask = chi2_mask & kac_mask
n_both = np.sum(both_mask)
print(f"CONDITIONAL ON χ² < 3.0 AND kac < −0.3 ({n_both} samples, {100*n_both/N_SAMPLE:.1f}%):")
if n_both > 0:
    print(f"  asym:  mean={np.mean(all_asym[both_mask]):.3f}  "
          f"std={np.std(all_asym[both_mask]):.3f}  "
          f"median={np.median(all_asym[both_mask]):.0f}")
    print(f"  m:     mean={np.mean(all_m[both_mask]):.3f}")
else:
    print("  (no samples)")
print()

# Conditional on high m-score (m >= 10)
m_mask = all_m >= 10
n_high_m = np.sum(m_mask)
print(f"CONDITIONAL ON m ≥ 10 ({n_high_m} samples, {100*n_high_m/N_SAMPLE:.1f}%):")
if n_high_m > 0:
    print(f"  asym:  mean={np.mean(all_asym[m_mask]):.3f}  "
          f"std={np.std(all_asym[m_mask]):.3f}")
    print(f"  chi²:  mean={np.mean(all_chi2[m_mask]):.3f}")
    print(f"  kac:   mean={np.mean(all_kac[m_mask]):.4f}")
print()

# Correlation matrix
print("CORRELATION MATRIX:")
corr_chi2_asym = np.corrcoef(all_chi2, all_asym)[0, 1]
corr_chi2_m = np.corrcoef(all_chi2, all_m)[0, 1]
corr_chi2_kac = np.corrcoef(all_chi2, all_kac)[0, 1]
corr_asym_m = np.corrcoef(all_asym, all_m)[0, 1]
corr_asym_kac = np.corrcoef(all_asym, all_kac)[0, 1]
corr_m_kac = np.corrcoef(all_m, all_kac)[0, 1]

print(f"  chi²-asym:  {corr_chi2_asym:+.4f}")
print(f"  chi²-m:     {corr_chi2_m:+.4f}")
print(f"  chi²-kac:   {corr_chi2_kac:+.4f}")
print(f"  asym-m:     {corr_asym_m:+.4f}")
print(f"  asym-kac:   {corr_asym_kac:+.4f}")
print(f"  m-kac:      {corr_m_kac:+.4f}")
print()

# Interpretation
uncond_asym = np.mean(all_asym)
cond_asym_chi2 = np.mean(all_asym[chi2_mask]) if n_balanced > 0 else float('nan')
cond_asym_kac = np.mean(all_asym[kac_mask]) if n_strong_kac > 0 else float('nan')

print("INTERPRETATION:")
if not np.isnan(cond_asym_chi2) and cond_asym_chi2 > 0:
    print(f"  Conditioning on χ²<3 shifts mean asym from {uncond_asym:.3f} to {cond_asym_chi2:.3f}")
    print(f"  → Positive asymmetry IS partially a substrate effect of kernel balance")
elif not np.isnan(cond_asym_chi2):
    print(f"  Conditioning on χ²<3 shifts mean asym from {uncond_asym:.3f} to {cond_asym_chi2:.3f}")
    print(f"  → Asymmetry is NOT a substrate effect of kernel balance (still negative)")
print()

all_results['P3_substrate'] = {
    'n_samples': N_SAMPLE,
    'unconditional': {
        'asym_mean': float(np.mean(all_asym)),
        'asym_std': float(np.std(all_asym)),
        'chi2_mean': float(np.mean(all_chi2)),
        'kac_mean': float(np.mean(all_kac)),
        'm_mean': float(np.mean(all_m)),
    },
    'conditional_chi2_lt3': {
        'n': int(n_balanced),
        'asym_mean': float(np.mean(all_asym[chi2_mask])) if n_balanced > 0 else None,
        'asym_std': float(np.std(all_asym[chi2_mask])) if n_balanced > 0 else None,
        'm_mean': float(np.mean(all_m[chi2_mask])) if n_balanced > 0 else None,
        'kac_mean': float(np.mean(all_kac[chi2_mask])) if n_balanced > 0 else None,
    },
    'conditional_kac_lt_neg03': {
        'n': int(n_strong_kac),
        'asym_mean': float(np.mean(all_asym[kac_mask])) if n_strong_kac > 0 else None,
    },
    'conditional_both': {
        'n': int(n_both),
        'asym_mean': float(np.mean(all_asym[both_mask])) if n_both > 0 else None,
    },
    'correlations': {
        'chi2_asym': float(corr_chi2_asym),
        'chi2_m': float(corr_chi2_m),
        'chi2_kac': float(corr_chi2_kac),
        'asym_m': float(corr_asym_m),
        'asym_kac': float(corr_asym_kac),
        'm_kac': float(corr_m_kac),
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# SAVE INTERMEDIATE (before slow annealing)
# ══════════════════════════════════════════════════════════════════════════════

print("Priorities 1, 3, 4 complete. Starting Priority 2 (annealing)...")
print()
