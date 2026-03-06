"""
R2-E RERUN: Multi-objective greedy with corrected kac normalization.

The original R2-E had t_kac = kac/KW_KAC — dividing by a negative inverted the
direction. This fix uses absolute value normalization for all terms.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
from infra import *

import json
import time

print("=" * 80)
print("R2-E FIXED: MULTI-OBJECTIVE GREEDY (corrected normalization)")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}  asym={KW_ASYM}  "
      f"m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()


def scalarized_objective_fixed(o, weights):
    """Corrected: all terms lower=better, KW maps to consistent reference.
    chi2: lower better → t = chi2 (unnormed, scale ~2)
    asym: higher better → t = -asym (negate, scale ~3)  
    m: higher better → t = -m (negate, scale ~12)
    kac: more negative better → t = kac (already lower=better, scale ~0.5)
    
    Normalize each to KW=1.0 with correct sign."""
    m = compute_all_metrics(o)
    
    # All terms: lower = better
    t_chi2 = m['chi2'] / KW_CHI2                    # KW→1.0, lower chi2→<1
    t_asym = -m['asym'] / abs(KW_ASYM) if KW_ASYM != 0 else -m['asym']  # KW→-1.0, higher asym→<-1
    t_m = -m['m_score'] / abs(KW_M) if KW_M > 0 else -m['m_score']      # KW→-1.0, higher m→<-1
    t_kac = m['kac'] / abs(KW_KAC) if KW_KAC != 0 else m['kac']         # KW→-1.0, more neg kac→<-1
    
    return (weights[0] * t_chi2 + weights[1] * t_asym +
            weights[2] * t_m + weights[3] * t_kac)


def greedy_optimize_fixed(start_o, weights, rng):
    o = list(start_o)
    val = scalarized_objective_fixed(o, weights)
    improved = True
    while improved:
        improved = False
        indices = list(range(27))
        rng.shuffle(indices)
        for bi_idx in indices:
            bi = free_bits[bi_idx]
            if bi['type'] == 'A':
                p = bi['pairs'][0]
                old_val = o[p]
                o[p] = 1 - old_val
            else:
                p1, p2 = bi['pairs']
                old_vals = (o[p1], o[p2])
                cur = (o[p1], o[p2])
                other = [s for s in bi['valid_states'] if s != cur]
                if not other:
                    continue
                o[p1], o[p2] = other[0]
            
            if is_s2_free(o):
                new_val = scalarized_objective_fixed(o, weights)
                if new_val < val - 1e-12:
                    val = new_val
                    improved = True
                    continue
            
            if bi['type'] == 'A':
                o[p] = old_val
            else:
                o[p1], o[p2] = old_vals
    return o, val


# Verify normalization is correct
kw_test = scalarized_objective_fixed(KW_O, (0.25, 0.25, 0.25, 0.25))
print(f"Normalization check: KW at equal weights → {kw_test:.4f}")
m_test = compute_all_metrics(KW_O)
print(f"  t_chi2={m_test['chi2']/KW_CHI2:.3f}  "
      f"t_asym={-m_test['asym']/abs(KW_ASYM):.3f}  "
      f"t_m={-m_test['m_score']/abs(KW_M):.3f}  "
      f"t_kac={m_test['kac']/abs(KW_KAC):.3f}")
print()


# Weight vectors — more focused than before, including KW-targeting combinations
weight_vectors = [
    ((0.25, 0.25, 0.25, 0.25), "equal"),
    ((0.40, 0.10, 0.10, 0.40), "chi2+kac heavy"),
    ((0.10, 0.40, 0.40, 0.10), "asym+m heavy"),
    ((0.50, 0.00, 0.00, 0.50), "chi2+kac only"),
    ((0.00, 0.50, 0.50, 0.00), "asym+m only"),
    ((0.30, 0.20, 0.20, 0.30), "balanced kernel+face"),
    ((0.20, 0.30, 0.20, 0.30), "asym+kac emphasis"),
    ((0.35, 0.15, 0.15, 0.35), "strong kernel"),
    ((0.15, 0.35, 0.35, 0.15), "strong face"),
    ((0.10, 0.10, 0.10, 0.70), "kac dominant"),
    ((0.70, 0.10, 0.10, 0.10), "chi2 dominant"),
    ((0.10, 0.10, 0.70, 0.10), "m dominant"),
]

N_STARTS = 50

all_results = {'kw_baseline': KW_METRICS}
r2e_results = []
t0 = time.time()

for wi, (weights, label) in enumerate(weight_vectors):
    w_str = f"({weights[0]:.2f},{weights[1]:.2f},{weights[2]:.2f},{weights[3]:.2f})"
    
    best_o = None
    best_val = float('inf')
    
    for trial in range(N_STARTS):
        rng_trial = random.Random(9000 + wi * 100 + trial)
        start = sample_s2_free(rng_trial)
        final_o, final_val = greedy_optimize_fixed(start, weights, rng_trial)
        if final_val < best_val:
            best_val = final_val
            best_o = list(final_o)
    
    metrics = compute_all_metrics(best_o)
    result = report_orientation(f"R2-Ef {label}", best_o, metrics)
    result['weights'] = list(weights)
    result['label'] = label
    result['scalar_value'] = best_val
    r2e_results.append(result)
    
    elapsed = time.time() - t0
    print(f"  [{wi+1}/{len(weight_vectors)}] {elapsed:.1f}s elapsed")
    print()

all_results['R2-E-fixed'] = r2e_results


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("R2-E FIXED SUMMARY")
print("=" * 80)
print()

header = (f"{'Label':>25s} {'chi²':>8s} {'asym':>6s} {'m':>4s} "
          f"{'kac':>8s} {'Ham':>4s} {'Pareto':>18s}")
print(header)
print("─" * len(header))

print(f"{'KW':>25s} {KW_CHI2:8.3f} {KW_ASYM:6d} {KW_M:4d} "
      f"{KW_KAC:8.4f} {'0':>4s} {'reference':>18s}")

for r in r2e_results:
    m = r['metrics']
    print(f"{r['label']:>25s} {m['chi2']:8.3f} {m['asym']:6d} {m['m_score']:4d} "
          f"{m['kac']:8.4f} {r['hamming_from_kw']:4d} {r['pareto']:>18s}")

print()

# Count Pareto statuses
from collections import Counter
pareto_counts = Counter(r['pareto'] for r in r2e_results)
print(f"Pareto summary: {dict(pareto_counts)}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# CLOSEST TO KW (Euclidean in normalized space)
# ══════════════════════════════════════════════════════════════════════════════

print("Closest to KW (normalized Euclidean distance):")
print()

for r in r2e_results:
    m = r['metrics']
    d_chi2 = (m['chi2'] - KW_CHI2) / KW_CHI2
    d_asym = (m['asym'] - KW_ASYM) / max(abs(KW_ASYM), 1)
    d_m = (m['m_score'] - KW_M) / KW_M
    d_kac = (m['kac'] - KW_KAC) / abs(KW_KAC)
    dist = (d_chi2**2 + d_asym**2 + d_m**2 + d_kac**2)**0.5
    r['kw_distance'] = dist

r2e_sorted = sorted(r2e_results, key=lambda r: r['kw_distance'])
for r in r2e_sorted[:5]:
    m = r['metrics']
    print(f"  {r['label']:>25s}: dist={r['kw_distance']:.3f}  "
          f"chi²={m['chi2']:.3f} asym={m['asym']} m={m['m_score']} kac={m['kac']:.4f}")

print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter5/round2e_fixed_data.json', 'w') as f:
    json.dump(json_clean(all_results), f, indent=2)

print("Data saved to round2e_fixed_data.json")
print()
print("=" * 80)
print("R2-E FIXED COMPLETE")
print("=" * 80)
