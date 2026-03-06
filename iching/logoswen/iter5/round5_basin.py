"""
Iter5 Round 5: Basin Characterization

Test 1: Metropolis-like descent from 200 random starts under 3 criteria.
Test 2: Random walk from KW, then reconverge — maps basin boundary.

All criteria are KW-agnostic: they define "better" without targeting KW's values.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
from infra import *

import json
import time
from collections import Counter

print("=" * 80)
print("ITER5 ROUND 5: BASIN CHARACTERIZATION")
print("=" * 80)
print()
print(f"KW baseline: χ²={KW_CHI2:.4f}  asym={KW_ASYM}  "
      f"m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()

# ── A1 distribution parameters (from round1) ────────────────────────────────
# Used for KW-agnostic normalization
A1_CHI2_STD = 3.803
A1_ASYM_STD = 2.410
A1_M_STD = 1.867
A1_KAC_STD = 0.165
A1_CHI2_MED = 6.419
A1_ASYM_MED = -2.0
A1_M_MED = 8.0
A1_KAC_MED = -0.142

# Load known dominators for comparison
with open('/home/quasar/nous/logoswen/iter5/round4_dominators_extended.json') as f:
    dom_data = json.load(f)
KNOWN_DOMINATORS = [d['orientation'] for d in dom_data['dominators']]

all_results = {'kw_baseline': KW_METRICS}


# ══════════════════════════════════════════════════════════════════════════════
# FREE-BIT FLIP HELPER
# ══════════════════════════════════════════════════════════════════════════════

def flip_free_bit(o, bi_idx):
    """Flip free bit bi_idx in orientation o (in-place). Returns True if valid."""
    bi = free_bits[bi_idx]
    if bi['type'] == 'A':
        p = bi['pairs'][0]
        o[p] = 1 - o[p]
    else:
        p1, p2 = bi['pairs']
        cur = (o[p1], o[p2])
        other = [s for s in bi['valid_states'] if s != cur]
        if not other:
            return False
        o[p1], o[p2] = other[0]
    return True


def unflip_free_bit(o, bi_idx, saved_state):
    """Restore orientation after a flip."""
    bi = free_bits[bi_idx]
    if bi['type'] == 'A':
        p = bi['pairs'][0]
        o[p] = saved_state
    else:
        p1, p2 = bi['pairs']
        o[p1], o[p2] = saved_state


def save_bit_state(o, bi_idx):
    """Save the current state of a free bit."""
    bi = free_bits[bi_idx]
    if bi['type'] == 'A':
        return o[bi['pairs'][0]]
    else:
        p1, p2 = bi['pairs']
        return (o[p1], o[p2])


# ══════════════════════════════════════════════════════════════════════════════
# ACCEPTANCE CRITERIA (KW-agnostic)
# ══════════════════════════════════════════════════════════════════════════════

def is_better_or_equal(old, new, name, higher_better):
    """Check if new is at least as good as old on one axis."""
    if higher_better:
        return new >= old - 1e-9
    else:
        return new <= old + 1e-9


def criterion_a_accept(old_m, new_m):
    """Pareto non-degradation: accept if no axis gets worse."""
    # chi2: lower better. asym: higher better. m: higher better. kac: lower better.
    if new_m['chi2'] > old_m['chi2'] + 1e-9:
        return False
    if new_m['asym'] < old_m['asym']:
        return False
    if new_m['m_score'] < old_m['m_score']:
        return False
    if new_m['kac'] > old_m['kac'] + 1e-9:
        return False
    # Must improve on at least one axis (not just lateral)
    improves = (new_m['chi2'] < old_m['chi2'] - 1e-9 or
                new_m['asym'] > old_m['asym'] or
                new_m['m_score'] > old_m['m_score'] or
                new_m['kac'] < old_m['kac'] - 1e-9)
    return improves


def balanced_cost(m):
    """Criterion B: each metric normalized by random-distribution std.
    All terms: lower = better. No KW values used."""
    return (m['chi2'] / A1_CHI2_STD +
            -m['asym'] / A1_ASYM_STD +
            -m['m_score'] / A1_M_STD +
            m['kac'] / A1_KAC_STD)


def criterion_b_accept(old_m, new_m):
    """Balanced improvement: accept if balanced_cost decreases."""
    return balanced_cost(new_m) < balanced_cost(old_m) - 1e-12


def worst_axis_distance_from_median(m):
    """Return (worst_axis_name, distance) for the axis closest to random median.
    Distance measured in std units. Higher distance = more exceptional."""
    distances = {
        'chi2': (A1_CHI2_MED - m['chi2']) / A1_CHI2_STD,   # positive = better than median
        'asym': (m['asym'] - A1_ASYM_MED) / A1_ASYM_STD,   # positive = better than median
        'm_score': (m['m_score'] - A1_M_MED) / A1_M_STD,   # positive = better than median
        'kac': (A1_KAC_MED - m['kac']) / A1_KAC_STD,       # positive = better than median
    }
    worst_name = min(distances, key=distances.get)
    return worst_name, distances[worst_name], distances


def criterion_c_accept(old_m, new_m):
    """Worst-axis improvement: accept if the minimum distance-from-median increases."""
    _, old_worst_dist, _ = worst_axis_distance_from_median(old_m)
    _, new_worst_dist, _ = worst_axis_distance_from_median(new_m)
    return new_worst_dist > old_worst_dist + 1e-12


CRITERIA = {
    'A': ('Pareto non-degradation', criterion_a_accept),
    'B': ('Balanced improvement', criterion_b_accept),
    'C': ('Worst-axis improvement', criterion_c_accept),
}


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: METROPOLIS DESCENT FROM RANDOM STARTS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("TEST 1: DESCENT FROM 200 RANDOM STARTS × 3 CRITERIA")
print("=" * 80)
print()

N_STARTS = 200
MAX_STEPS = 10_000
STABLE_THRESHOLD = 1000  # stop after this many consecutive rejections

test1_results = {}

for crit_name, (crit_label, accept_fn) in CRITERIA.items():
    print(f"─── Criterion {crit_name}: {crit_label} ({N_STARTS} starts) ───")
    
    results = []
    t0 = time.time()
    
    for trial in range(N_STARTS):
        rng = random.Random(50000 + trial)
        o = sample_s2_free(rng)
        m = compute_all_metrics(o)
        
        steps_taken = 0
        consecutive_rejects = 0
        total_accepts = 0
        
        for step in range(MAX_STEPS):
            bi_idx = rng.randint(0, 26)
            saved = save_bit_state(o, bi_idx)
            
            if not flip_free_bit(o, bi_idx):
                unflip_free_bit(o, bi_idx, saved)
                continue
            
            if not is_s2_free(o):
                unflip_free_bit(o, bi_idx, saved)
                continue
            
            new_m = compute_all_metrics(o)
            
            if accept_fn(m, new_m):
                m = new_m
                total_accepts += 1
                consecutive_rejects = 0
            else:
                unflip_free_bit(o, bi_idx, saved)
                consecutive_rejects += 1
            
            steps_taken = step + 1
            
            if consecutive_rejects >= STABLE_THRESHOLD:
                break
        
        h_kw = hamming(o, KW_O)
        pareto = pareto_compare(m)
        
        # Check if final matches any known dominator
        matches_dominator = -1
        for di, dom_o in enumerate(KNOWN_DOMINATORS):
            if hamming(o, dom_o) == 0:
                matches_dominator = di
                break
        
        results.append({
            'orientation': list(o),
            'metrics': m,
            'hamming_kw': h_kw,
            'pareto': pareto,
            'steps': steps_taken,
            'accepts': total_accepts,
            'matches_dominator': matches_dominator,
        })
        
        if (trial + 1) % 50 == 0:
            print(f"  ... {trial+1}/{N_STARTS} ({time.time()-t0:.1f}s)")
    
    elapsed = time.time() - t0
    print(f"  Complete: {elapsed:.1f}s")
    
    # ── Analysis ─────────────────────────────────────────────────────────
    
    hammings = np.array([r['hamming_kw'] for r in results])
    pareto_counts = Counter(r['pareto'] for r in results)
    
    # Convergence: count distinct final orientations (Hamming ≥ 2 = distinct)
    distinct = []
    for r in results:
        is_new = True
        for d in distinct:
            if hamming(r['orientation'], d) < 2:
                is_new = False
                break
        if is_new:
            distinct.append(r['orientation'])
    n_distinct = len(distinct)
    
    # KW recovery
    n_kw_exact = sum(1 for r in results if r['hamming_kw'] == 0)
    n_kw_close = sum(1 for r in results if r['hamming_kw'] <= 4)
    
    # Dominator discovery
    n_dom = sum(1 for r in results if r['matches_dominator'] >= 0)
    dom_indices = [r['matches_dominator'] for r in results if r['matches_dominator'] >= 0]
    
    # Best final result (closest to KW)
    best_idx = int(np.argmin(hammings))
    best = results[best_idx]
    
    print()
    print(f"  Hamming from KW: min={hammings.min()}  mean={hammings.mean():.1f}  "
          f"median={np.median(hammings):.0f}  max={hammings.max()}")
    print(f"  KW exact recovery: {n_kw_exact}/{N_STARTS} ({100*n_kw_exact/N_STARTS:.1f}%)")
    print(f"  Within Hamming ≤4: {n_kw_close}/{N_STARTS} ({100*n_kw_close/N_STARTS:.1f}%)")
    print(f"  Pareto: {dict(pareto_counts)}")
    print(f"  Distinct attractors: {n_distinct}")
    print(f"  Dominator matches: {n_dom}")
    if dom_indices:
        print(f"    Dominator indices: {Counter(dom_indices)}")
    print(f"  Best result: Ham={best['hamming_kw']}  "
          f"χ²={best['metrics']['chi2']:.3f}  asym={best['metrics']['asym']}  "
          f"m={best['metrics']['m_score']}  kac={best['metrics']['kac']:.4f}")
    print()
    
    # Hamming distribution
    ham_dist = Counter(int(h) for h in hammings)
    print(f"  Hamming distribution:")
    for h in sorted(ham_dist.keys()):
        bar = '█' * ham_dist[h]
        print(f"    {h:3d}: {ham_dist[h]:4d} {bar}")
    print()
    
    # Metric distributions at convergence
    final_chi2 = np.array([r['metrics']['chi2'] for r in results])
    final_asym = np.array([r['metrics']['asym'] for r in results])
    final_m = np.array([r['metrics']['m_score'] for r in results])
    final_kac = np.array([r['metrics']['kac'] for r in results])
    
    print(f"  Final metric distributions:")
    print(f"    χ²:   mean={final_chi2.mean():.3f}  std={final_chi2.std():.3f}  "
          f"min={final_chi2.min():.3f}  max={final_chi2.max():.3f}")
    print(f"    asym: mean={final_asym.mean():.1f}  std={final_asym.std():.1f}  "
          f"min={final_asym.min():.0f}  max={final_asym.max():.0f}")
    print(f"    m:    mean={final_m.mean():.1f}  std={final_m.std():.1f}  "
          f"min={final_m.min():.0f}  max={final_m.max():.0f}")
    print(f"    kac:  mean={final_kac.mean():.4f}  std={final_kac.std():.4f}  "
          f"min={final_kac.min():.4f}  max={final_kac.max():.4f}")
    print()
    
    test1_results[crit_name] = {
        'label': crit_label,
        'n_starts': N_STARTS,
        'hamming_stats': {
            'min': int(hammings.min()), 'mean': float(hammings.mean()),
            'median': float(np.median(hammings)), 'max': int(hammings.max()),
        },
        'hamming_distribution': {str(k): v for k, v in sorted(ham_dist.items())},
        'n_kw_exact': n_kw_exact,
        'n_kw_close_4': n_kw_close,
        'pareto_counts': dict(pareto_counts),
        'n_distinct_attractors': n_distinct,
        'n_dominator_matches': n_dom,
        'dominator_indices': dict(Counter(dom_indices)) if dom_indices else {},
        'metric_stats': {
            'chi2': {'mean': float(final_chi2.mean()), 'std': float(final_chi2.std())},
            'asym': {'mean': float(final_asym.mean()), 'std': float(final_asym.std())},
            'm': {'mean': float(final_m.mean()), 'std': float(final_m.std())},
            'kac': {'mean': float(final_kac.mean()), 'std': float(final_kac.std())},
        },
        # Save the 10 closest-to-KW final orientations
        'closest_to_kw': sorted([{
            'orientation': r['orientation'],
            'metrics': r['metrics'],
            'hamming_kw': r['hamming_kw'],
            'pareto': r['pareto'],
        } for r in results], key=lambda x: x['hamming_kw'])[:10],
    }

all_results['test1'] = test1_results


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: BASIN BOUNDARY PROBING
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("TEST 2: BASIN BOUNDARY — RANDOM WALK FROM KW THEN RECONVERGE")
print("=" * 80)
print()

WALK_LENGTHS = [1, 2, 3, 4, 5, 8, 12, 16, 20]
N_TRIALS = 100

# Use Criterion B for reconvergence (the balanced, KW-agnostic criterion)
reconverge_fn = criterion_b_accept

test2_results = {}

for walk_len in WALK_LENGTHS:
    recoveries = 0
    final_hammings = []
    final_paretos = []
    
    t0 = time.time()
    
    for trial in range(N_TRIALS):
        rng = random.Random(60000 + walk_len * 1000 + trial)
        o = list(KW_O)
        
        # Random walk: flip walk_len random free bits
        flipped = []
        attempts = 0
        while len(flipped) < walk_len and attempts < walk_len * 10:
            bi_idx = rng.randint(0, 26)
            attempts += 1
            saved = save_bit_state(o, bi_idx)
            if not flip_free_bit(o, bi_idx):
                unflip_free_bit(o, bi_idx, saved)
                continue
            if not is_s2_free(o):
                unflip_free_bit(o, bi_idx, saved)
                continue
            flipped.append(bi_idx)
        
        # Reconverge using Criterion B
        m = compute_all_metrics(o)
        consecutive_rejects = 0
        
        for step in range(MAX_STEPS):
            bi_idx = rng.randint(0, 26)
            saved = save_bit_state(o, bi_idx)
            
            if not flip_free_bit(o, bi_idx):
                unflip_free_bit(o, bi_idx, saved)
                continue
            
            if not is_s2_free(o):
                unflip_free_bit(o, bi_idx, saved)
                continue
            
            new_m = compute_all_metrics(o)
            
            if reconverge_fn(m, new_m):
                m = new_m
                consecutive_rejects = 0
            else:
                unflip_free_bit(o, bi_idx, saved)
                consecutive_rejects += 1
            
            if consecutive_rejects >= STABLE_THRESHOLD:
                break
        
        h_kw = hamming(o, KW_O)
        pareto = pareto_compare(m)
        
        final_hammings.append(h_kw)
        final_paretos.append(pareto)
        if h_kw == 0:
            recoveries += 1
    
    elapsed = time.time() - t0
    ham_arr = np.array(final_hammings)
    pareto_cts = Counter(final_paretos)
    
    n_close = sum(1 for h in final_hammings if h <= 4)
    
    print(f"  Walk={walk_len:2d}: recovery={recoveries:3d}/{N_TRIALS}  "
          f"≤4={n_close:3d}/{N_TRIALS}  "
          f"Ham mean={ham_arr.mean():.1f} med={np.median(ham_arr):.0f} max={ham_arr.max()}  "
          f"({elapsed:.1f}s)")
    
    test2_results[str(walk_len)] = {
        'walk_length': walk_len,
        'n_trials': N_TRIALS,
        'kw_recovered': recoveries,
        'within_ham_4': n_close,
        'hamming_stats': {
            'min': int(ham_arr.min()), 'mean': float(ham_arr.mean()),
            'median': float(np.median(ham_arr)), 'max': int(ham_arr.max()),
        },
        'hamming_distribution': {str(k): v for k, v in sorted(Counter(int(h) for h in final_hammings).items())},
        'pareto_counts': dict(pareto_cts),
    }

print()
all_results['test2'] = test2_results


# ══════════════════════════════════════════════════════════════════════════════
# CROSS-CRITERION COMPARISON
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("CROSS-CRITERION COMPARISON")
print("=" * 80)
print()

print(f"{'Criterion':>30s} {'KW=0':>6s} {'≤4':>6s} {'median':>7s} {'distinct':>8s} {'dom':>4s} {'dom-by':>7s} {'trade':>6s}")
print("─" * 85)
for crit_name in ['A', 'B', 'C']:
    r = test1_results[crit_name]
    p = r['pareto_counts']
    print(f"  {crit_name}: {r['label']:>26s} {r['n_kw_exact']:6d} {r['n_kw_close_4']:6d} "
          f"{r['hamming_stats']['median']:7.0f} {r['n_distinct_attractors']:8d} "
          f"{p.get('dominates-kw', 0):4d} {p.get('dominated-by-kw', 0):7d} "
          f"{p.get('trade-off', 0):6d}")
print()

# Basin boundary summary
print("BASIN BOUNDARY (Criterion B reconvergence):")
print(f"{'walk':>5s} {'recovery%':>10s} {'≤4%':>8s} {'median Ham':>10s}")
print("─" * 40)
for wl in WALK_LENGTHS:
    r = test2_results[str(wl)]
    print(f"{wl:5d} {100*r['kw_recovered']/r['n_trials']:9.0f}% "
          f"{100*r['within_ham_4']/r['n_trials']:7.0f}% "
          f"{r['hamming_stats']['median']:10.0f}")
print()

# Find basin radius: last walk_length with >50% recovery
basin_radius = 0
for wl in WALK_LENGTHS:
    r = test2_results[str(wl)]
    if r['kw_recovered'] > r['n_trials'] * 0.5:
        basin_radius = wl
print(f"Basin radius (>50% recovery): ~{basin_radius} bits")
print()


# ══════════════════════════════════════════════════════════════════════════════
# ATTRACTOR ANALYSIS: WHAT DO THE FINAL ORIENTATIONS LOOK LIKE?
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("ATTRACTOR ANALYSIS (Criterion B — most balanced)")
print("=" * 80)
print()

crit_b_results = [r for r in sorted(
    test1_results['B']['closest_to_kw'], key=lambda x: x['hamming_kw'])]

# Also examine the most common Hamming distance
b_all_ham = [int(k) for k, v in test1_results['B']['hamming_distribution'].items() for _ in range(v)]
most_common_ham = Counter(b_all_ham).most_common(3)
print(f"Most common final Hamming distances (Criterion B): {most_common_ham}")
print()

# Show the 5 closest-to-KW under criterion B
print("5 closest to KW under Criterion B:")
for i, r in enumerate(crit_b_results[:5]):
    m = r['metrics']
    print(f"  #{i+1}: Ham={r['hamming_kw']}  χ²={m['chi2']:.3f}  asym={m['asym']}  "
          f"m={m['m_score']}  kac={m['kac']:.4f}  {r['pareto']}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# THE SUMMARY PARAGRAPH
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("BASIN CHARACTERIZATION SUMMARY")
print("=" * 80)
print()

# Collect key numbers
b_exact = test1_results['B']['n_kw_exact']
b_close = test1_results['B']['n_kw_close_4']
b_med = test1_results['B']['hamming_stats']['median']
b_distinct = test1_results['B']['n_distinct_attractors']
b_dom = test1_results['B']['pareto_counts'].get('dominated-by-kw', 0)

a_exact = test1_results['A']['n_kw_exact']
a_close = test1_results['A']['n_kw_close_4']

c_exact = test1_results['C']['n_kw_exact']
c_close = test1_results['C']['n_kw_close_4']

# Basin radius
radius_str = f"~{basin_radius}" if basin_radius > 0 else "<1"

print(f"Under Criterion B (balanced std-normalized improvement), {b_exact} of {N_STARTS} "
      f"random starts ({100*b_exact/N_STARTS:.0f}%) converge to KW exactly, and "
      f"{b_close} ({100*b_close/N_STARTS:.0f}%) converge to within Hamming ≤4. "
      f"The median final Hamming distance is {b_med:.0f}, with {b_distinct} distinct "
      f"attractors. Under Criterion A (strict Pareto non-degradation), {a_exact} "
      f"({100*a_exact/N_STARTS:.0f}%) reach KW exactly, {a_close} ({100*a_close/N_STARTS:.0f}%) "
      f"reach Hamming ≤4. Under Criterion C (worst-axis improvement), {c_exact} "
      f"({100*c_exact/N_STARTS:.0f}%) reach KW exactly, {c_close} ({100*c_close/N_STARTS:.0f}%) "
      f"reach Hamming ≤4. The basin radius (walk from KW, then reconverge under "
      f"Criterion B, >50% recovery) is {radius_str} bits.")
print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter5/round5_data.json', 'w') as f:
    json.dump(json_clean(all_results), f, indent=2)

print("Data saved to round5_data.json")
print()
print("=" * 80)
print("ROUND 5 COMPLETE")
print("=" * 80)
