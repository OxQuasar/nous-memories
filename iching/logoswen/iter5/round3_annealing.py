"""
Iter5 Round 3, Priority 2: Simulated Annealing

Two objectives:
  A) Minimax: minimize max normalized deviation from KW
  B) L1: minimize sum of normalized deviations from KW

50 independent runs each, 100K steps, geometric cooling.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
from infra import *

import json
import time
import math

print("=" * 80)
print("PRIORITY 2: SIMULATED ANNEALING")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}  asym={KW_ASYM}  "
      f"m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# OBJECTIVE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def normalized_deviations(metrics):
    """Return 4 normalized deviations, all ≥ 0, where 0 = matches KW."""
    # chi2: lower better. dev = (chi2 - KW) / KW. If chi2 < KW, dev < 0 → clip to 0? 
    # No: we want distance from KW profile, not improvement. Use absolute deviation.
    # But the objective is to MATCH KW, not beat it. So deviation = |metric - KW| / scale.
    d_chi2 = abs(metrics['chi2'] - KW_CHI2) / KW_CHI2
    d_asym = abs(metrics['asym'] - KW_ASYM) / max(abs(KW_ASYM), 1)
    d_m = abs(metrics['m_score'] - KW_M) / KW_M
    d_kac = abs(metrics['kac'] - KW_KAC) / abs(KW_KAC)
    return (d_chi2, d_asym, d_m, d_kac)


def cost_minimax(metrics):
    """Minimax: minimize the worst normalized deviation from KW."""
    devs = normalized_deviations(metrics)
    return max(devs)


def cost_l1(metrics):
    """L1: minimize sum of normalized deviations from KW."""
    devs = normalized_deviations(metrics)
    return sum(devs)


# Verify: KW should have cost 0
kw_test = compute_all_metrics(KW_O)
print(f"KW minimax cost: {cost_minimax(kw_test):.6f}")
print(f"KW L1 cost: {cost_l1(kw_test):.6f}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATED ANNEALING
# ══════════════════════════════════════════════════════════════════════════════

def sa_run(start_o, cost_fn, rng, T_start=1.0, alpha=0.999, n_steps=100_000):
    """Single SA run. Returns (best_o, best_cost, final_o, final_cost, accept_rate)."""
    o = list(start_o)
    metrics = compute_all_metrics(o)
    cost = cost_fn(metrics)
    
    best_o = list(o)
    best_cost = cost
    best_metrics = dict(metrics)
    
    T = T_start
    n_accept = 0
    
    for step in range(n_steps):
        # Pick a random free bit to flip
        bi_idx = rng.randint(0, 26)
        bi = free_bits[bi_idx]
        
        # Save and flip
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
        
        if not is_s2_free(o):
            # Revert
            if bi['type'] == 'A':
                o[p] = old_val
            else:
                o[p1], o[p2] = old_vals
            continue
        
        new_metrics = compute_all_metrics(o)
        new_cost = cost_fn(new_metrics)
        delta = new_cost - cost
        
        if delta < 0 or (T > 0 and rng.random() < math.exp(-delta / T)):
            # Accept
            cost = new_cost
            metrics = new_metrics
            n_accept += 1
            if cost < best_cost:
                best_cost = cost
                best_o = list(o)
                best_metrics = dict(metrics)
        else:
            # Reject: revert
            if bi['type'] == 'A':
                o[p] = old_val
            else:
                o[p1], o[p2] = old_vals
        
        T *= alpha
    
    return best_o, best_cost, best_metrics, float(n_accept) / n_steps


# ── Run SA ────────────────────────────────────────────────────────────────────

N_RUNS = 50
N_STEPS = 100_000

sa_results = {}

for label, cost_fn in [("minimax", cost_minimax), ("L1", cost_l1)]:
    print(f"─── SA with {label} objective ({N_RUNS} runs × {N_STEPS} steps) ───")
    print()
    
    results = []
    t0 = time.time()
    
    for run in range(N_RUNS):
        rng_sa = random.Random(10000 + run)
        start = sample_s2_free(rng_sa)
        best_o, best_cost, best_metrics, accept_rate = sa_run(
            start, cost_fn, rng_sa, T_start=1.0, alpha=0.999, n_steps=N_STEPS)
        
        h = hamming(best_o, KW_O)
        pareto = pareto_compare(best_metrics)
        
        results.append({
            'orientation': best_o,
            'metrics': best_metrics,
            'cost': best_cost,
            'hamming_from_kw': h,
            'pareto': pareto,
            'accept_rate': accept_rate,
        })
        
        if (run + 1) % 10 == 0:
            elapsed = time.time() - t0
            print(f"  ... {run+1}/{N_RUNS} ({elapsed:.1f}s)")
    
    elapsed = time.time() - t0
    print(f"  Complete: {elapsed:.1f}s")
    print()
    
    # Sort by cost
    results.sort(key=lambda r: r['cost'])
    
    # Summary statistics
    costs = np.array([r['cost'] for r in results])
    hammings = np.array([r['hamming_from_kw'] for r in results])
    accept_rates = np.array([r['accept_rate'] for r in results])
    
    pareto_counts = Counter(r['pareto'] for r in results)
    
    print(f"  Cost:    min={costs.min():.4f}  mean={costs.mean():.4f}  "
          f"max={costs.max():.4f}")
    print(f"  Hamming: min={hammings.min()}  mean={hammings.mean():.1f}  "
          f"max={hammings.max()}")
    print(f"  Accept:  mean={accept_rates.mean():.3f}")
    print(f"  Pareto:  {dict(pareto_counts)}")
    print()
    
    # Top 5 results
    print(f"  TOP 5 (lowest cost):")
    print(f"  {'#':>3s} {'cost':>8s} {'chi²':>8s} {'asym':>6s} {'m':>4s} "
          f"{'kac':>8s} {'Ham':>4s} {'Pareto':>15s}")
    print(f"  " + "─" * 65)
    for i, r in enumerate(results[:5]):
        m = r['metrics']
        print(f"  {i+1:3d} {r['cost']:8.4f} {m['chi2']:8.3f} {m['asym']:6d} "
              f"{m['m_score']:4d} {m['kac']:8.4f} {r['hamming_from_kw']:4d} "
              f"{r['pareto']:>15s}")
    print()
    
    # Check: does any result match or dominate KW?
    n_dominate = sum(1 for r in results if r['pareto'] == 'dominates-kw')
    n_equal = sum(1 for r in results if r['pareto'] == 'equal')
    n_dominated = sum(1 for r in results if r['pareto'] == 'dominated-by-kw')
    
    print(f"  Dominate KW: {n_dominate}")
    print(f"  Equal to KW: {n_equal}")
    print(f"  Dominated by KW: {n_dominated}")
    print(f"  Trade-off: {pareto_counts.get('trade-off', 0)}")
    print()
    
    # How close does the best get?
    best = results[0]
    devs = normalized_deviations(best['metrics'])
    print(f"  Best result deviations from KW:")
    print(f"    chi²: {devs[0]:.4f}  asym: {devs[1]:.4f}  m: {devs[2]:.4f}  kac: {devs[3]:.4f}")
    print(f"    Orientation: {orientation_str(best['orientation'])}")
    print()
    
    # Clustering: do results converge to similar orientations?
    if len(results) >= 2:
        mutual_hammings = []
        for i in range(min(10, len(results))):
            for j in range(i+1, min(10, len(results))):
                mutual_hammings.append(hamming(results[i]['orientation'],
                                               results[j]['orientation']))
        print(f"  Mutual Hamming distances (top 10): "
              f"min={min(mutual_hammings)}  mean={np.mean(mutual_hammings):.1f}  "
              f"max={max(mutual_hammings)}")
    print()
    
    sa_results[label] = {
        'runs': [{
            'orientation': r['orientation'],
            'metrics': r['metrics'],
            'cost': r['cost'],
            'hamming_from_kw': r['hamming_from_kw'],
            'pareto': r['pareto'],
            'accept_rate': r['accept_rate'],
        } for r in results],
        'summary': {
            'cost_min': float(costs.min()),
            'cost_mean': float(costs.mean()),
            'cost_max': float(costs.max()),
            'hamming_min': int(hammings.min()),
            'hamming_mean': float(hammings.mean()),
            'hamming_max': int(hammings.max()),
            'pareto_counts': dict(pareto_counts),
            'n_dominate_kw': n_dominate,
            'n_equal_kw': n_equal,
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# COMPARISON: BEST SA RESULTS vs KW
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("SA COMPARISON: BEST RESULTS vs KW")
print("=" * 80)
print()

print(f"{'Method':>12s} {'chi²':>8s} {'asym':>6s} {'m':>4s} {'kac':>8s} "
      f"{'Ham':>4s} {'cost':>8s} {'Pareto':>15s}")
print("─" * 75)
print(f"{'KW':>12s} {KW_CHI2:8.3f} {KW_ASYM:6d} {KW_M:4d} {KW_KAC:8.4f} "
      f"{'0':>4s} {'0.000':>8s} {'reference':>15s}")

for label in ['minimax', 'L1']:
    best = sa_results[label]['runs'][0]
    m = best['metrics']
    print(f"{label:>12s} {m['chi2']:8.3f} {m['asym']:6d} {m['m_score']:4d} "
          f"{m['kac']:8.4f} {best['hamming_from_kw']:4d} "
          f"{best['cost']:8.4f} {best['pareto']:>15s}")

print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter5/round3_sa_data.json', 'w') as f:
    json.dump(json_clean(sa_results), f, indent=2)

print("SA data saved to round3_sa_data.json")
print()
print("=" * 80)
print("PRIORITY 2 COMPLETE")
print("=" * 80)
