"""
Iter5 Round 2: Composite Generators

R2-A: Face-flow composite (M-rule + kernel-repeat override)
R2-C: Balanced kernel walk (sequential diversity + distributional uniformity)
R2-D: Asymmetry-aware sequential diversity
R2-E: Multi-objective greedy scalarization
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
from infra import *

import json
import time

print("=" * 80)
print("ITER5 ROUND 2: COMPOSITE GENERATORS")
print("=" * 80)
print()
print(f"KW baseline: chi²={KW_CHI2:.4f}  asym={KW_ASYM}  "
      f"m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()

all_results = {'kw_baseline': KW_METRICS}


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: M-rule default for a pair
# ══════════════════════════════════════════════════════════════════════════════

def m_rule_default(k):
    """Return orientation that M-rule prefers for pair k."""
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    if a[1] != a[4]:  # M-decisive
        return 0 if a[1] == 0 else 1  # L2=yin first
    else:  # binary-high-first
        return 0 if hex_to_int(a) >= hex_to_int(b) else 1


# ══════════════════════════════════════════════════════════════════════════════
# R2-A: FACE-FLOW COMPOSITE
# ══════════════════════════════════════════════════════════════════════════════

def generate_face_flow(min_hamming=1):
    """M-rule default with kernel-repeat override.
    Override when bridge kernel Hamming distance to previous < min_hamming."""
    o = [0] * 32
    o[0] = m_rule_default(0)
    
    for k in range(1, 32):
        default = m_rule_default(k)
        alt = 1 - default
        
        # Try default first
        o[k] = default
        
        # Check S=2 at bridge k-1
        s2_default_ok = True
        if k - 1 in CONSTRAINTS and (o[k-1], o[k]) in CONSTRAINTS[k-1]:
            s2_default_ok = False
        
        if s2_default_ok and k >= 2:
            bk = bridge_kernel_3bit(o, k - 1)
            bk_prev = bridge_kernel_3bit(o, k - 2)
            hdist = hamming_3bit(bk, bk_prev)
            if hdist < min_hamming:
                # Try alt
                o[k] = alt
                s2_alt_ok = True
                if k - 1 in CONSTRAINTS and (o[k-1], o[k]) in CONSTRAINTS[k-1]:
                    s2_alt_ok = False
                if s2_alt_ok:
                    bk_alt = bridge_kernel_3bit(o, k - 1)
                    hdist_alt = hamming_3bit(bk_alt, bk_prev)
                    if hdist_alt >= min_hamming:
                        pass  # keep alt
                    else:
                        o[k] = default  # alt not better, revert
                else:
                    o[k] = default  # alt violates S=2, revert
        elif not s2_default_ok:
            # Default violates S=2, must use alt
            o[k] = alt
            if k - 1 in CONSTRAINTS and (o[k-1], o[k]) in CONSTRAINTS[k-1]:
                print(f"  WARNING: both orientations violate S=2 at pair {k}")
                o[k] = default  # fallback
    
    return o


print("─" * 80)
print("R2-A: FACE-FLOW COMPOSITE (M-rule + kernel-repeat override)")
print("─" * 80)
print()

# Variant 1: override on exact repeat (Hamming < 1)
r2a1_o = generate_face_flow(min_hamming=1)
r2a1_s2 = is_s2_free(r2a1_o)
print(f"R2-A1 (override on exact repeat, min_hamming=1) S=2-free: {r2a1_s2}")
r2a1 = report_orientation("R2-A1", r2a1_o)

# Variant 2: override when Hamming < 2
r2a2_o = generate_face_flow(min_hamming=2)
r2a2_s2 = is_s2_free(r2a2_o)
print(f"R2-A2 (override when hamming < 2, min_hamming=2) S=2-free: {r2a2_s2}")
r2a2 = report_orientation("R2-A2", r2a2_o)

# Variant 3: override when Hamming < 3
r2a3_o = generate_face_flow(min_hamming=3)
r2a3_s2 = is_s2_free(r2a3_o)
print(f"R2-A3 (override when hamming < 3, min_hamming=3) S=2-free: {r2a3_s2}")
r2a3 = report_orientation("R2-A3", r2a3_o)

# Count overrides
for name, o_gen in [("R2-A1", r2a1_o), ("R2-A2", r2a2_o), ("R2-A3", r2a3_o)]:
    n_override = sum(1 for k in range(32) if o_gen[k] != m_rule_default(k))
    print(f"  {name}: {n_override} M-rule overrides out of 32 pairs")
print()

all_results['R2-A1'] = r2a1
all_results['R2-A2'] = r2a2
all_results['R2-A3'] = r2a3


# ══════════════════════════════════════════════════════════════════════════════
# R2-C: BALANCED KERNEL WALK
# ══════════════════════════════════════════════════════════════════════════════

def generate_balanced_walk(w_seq, w_dist):
    """Sequential processing with composite score.
    w_seq: weight on Hamming distance from previous kernel
    w_dist: weight on deficit of chosen kernel type"""
    o = [0] * 32
    kernel_counts = Counter()
    expected_per_type = 31 / 8  # ≈ 3.875
    
    o[0] = 0  # arbitrary start
    
    for k in range(1, 32):
        best_choice = None
        best_score = None
        
        for choice in [0, 1]:
            o[k] = choice
            
            # Check S=2
            if k - 1 in CONSTRAINTS and (o[k-1], o[k]) in CONSTRAINTS[k-1]:
                continue
            
            bk = bridge_kernel_3bit(o, k - 1)
            
            # Sequential diversity component
            if k >= 2:
                bk_prev = bridge_kernel_3bit(o, k - 2)
                hdist = hamming_3bit(bk, bk_prev)
            else:
                hdist = 1.5  # neutral for first bridge
            
            # Distributional uniformity component
            deficit = expected_per_type - kernel_counts.get(bk, 0)
            
            score = w_seq * hdist + w_dist * deficit
            
            if best_score is None or score > best_score:
                best_score = score
                best_choice = choice
        
        if best_choice is None:
            best_choice = 0
        
        o[k] = best_choice
        bk = bridge_kernel_3bit(o, k - 1)
        kernel_counts[bk] += 1
    
    return o


print("─" * 80)
print("R2-C: BALANCED KERNEL WALK")
print("─" * 80)
print()

weight_combos = [
    (1.0, 0.0, "pure sequential"),
    (0.7, 0.3, "seq-heavy"),
    (0.5, 0.5, "equal"),
    (0.3, 0.7, "dist-heavy"),
    (0.0, 1.0, "pure distributional"),
]

r2c_results = []
for w_seq, w_dist, label in weight_combos:
    o = generate_balanced_walk(w_seq, w_dist)
    s2_ok = is_s2_free(o)
    print(f"R2-C ({label}, w_seq={w_seq}, w_dist={w_dist}) S=2-free: {s2_ok}")
    result = report_orientation(f"R2-C ({label})", o)
    result['w_seq'] = w_seq
    result['w_dist'] = w_dist
    result['label'] = label
    
    # Show kernel distribution
    seq = build_sequence(o)
    kfreq = Counter()
    for bk in range(31):
        kfreq[kernel_name(seq[2*bk+1], seq[2*bk+2])] += 1
    result['kernel_distribution'] = dict(kfreq)
    print(f"    Kernel dist: {dict(sorted(kfreq.items()))}")
    print()
    
    r2c_results.append(result)

all_results['R2-C'] = r2c_results


# ══════════════════════════════════════════════════════════════════════════════
# R2-D: ASYMMETRY-AWARE SEQUENTIAL DIVERSITY
# ══════════════════════════════════════════════════════════════════════════════

def generate_asym_diversity(lower_pref='low'):
    """C2 algorithm with asymmetry-aware tie-breaking.
    In upper canon (pairs 0-14): prefer binary-high-first.
    In lower canon (pairs 15-31): prefer binary-low-first if lower_pref='low',
    no preference if lower_pref='none'."""
    o = [0] * 32
    kernel_counts = Counter()
    
    o[0] = 0
    
    for k in range(1, 32):
        best_choice = None
        best_score = None
        
        for choice in [0, 1]:
            o[k] = choice
            
            if k - 1 in CONSTRAINTS and (o[k-1], o[k]) in CONSTRAINTS[k-1]:
                continue
            
            bk = bridge_kernel_3bit(o, k - 1)
            
            # Primary: Hamming distance
            if k >= 2:
                bk_prev = bridge_kernel_3bit(o, k - 2)
                hdist = hamming_3bit(bk, bk_prev)
            else:
                hdist = 0
            
            # Secondary: least-seen kernel
            count = kernel_counts.get(bk, 0)
            
            # Tertiary: asymmetry preference
            # Compute binary value of first hex under this choice
            if choice == 0:
                first_hex = PAIRS[k]['a']
            else:
                first_hex = PAIRS[k]['b']
            second_hex = PAIRS[k]['b'] if choice == 0 else PAIRS[k]['a']
            bh_first = 1 if hex_to_int(first_hex) > hex_to_int(second_hex) else 0
            
            if k < 15:  # upper canon: prefer binary-high-first
                asym_bonus = bh_first
            else:  # lower canon
                if lower_pref == 'low':
                    asym_bonus = 1 - bh_first  # prefer binary-low-first
                elif lower_pref == 'none':
                    asym_bonus = 0  # no preference
                else:  # 'high'
                    asym_bonus = bh_first
            
            score = (hdist, -count, asym_bonus)
            
            if best_score is None or score > best_score:
                best_score = score
                best_choice = choice
        
        if best_choice is None:
            best_choice = 0
        
        o[k] = best_choice
        bk = bridge_kernel_3bit(o, k - 1)
        kernel_counts[bk] += 1
    
    return o


print("─" * 80)
print("R2-D: ASYMMETRY-AWARE SEQUENTIAL DIVERSITY")
print("─" * 80)
print()

r2d_results = []
for lower_pref, label in [('low', 'upper-high/lower-low'),
                           ('none', 'upper-high/lower-neutral'),
                           ('high', 'upper-high/lower-high')]:
    o = generate_asym_diversity(lower_pref)
    s2_ok = is_s2_free(o)
    print(f"R2-D ({label}) S=2-free: {s2_ok}")
    result = report_orientation(f"R2-D ({label})", o)
    result['lower_pref'] = lower_pref
    result['label'] = label
    r2d_results.append(result)

all_results['R2-D'] = r2d_results


# ══════════════════════════════════════════════════════════════════════════════
# R2-E: MULTI-OBJECTIVE GREEDY
# ══════════════════════════════════════════════════════════════════════════════

print("─" * 80)
print("R2-E: MULTI-OBJECTIVE GREEDY SCALARIZATION")
print("─" * 80)
print()

def scalarized_objective(o, weights):
    """Compute weighted scalarized objective (lower = better).
    weights = (w_chi2, w_asym, w_m, w_kac), each ≥ 0, sum to 1.
    Each metric normalized so KW ≈ 1.0."""
    m = compute_all_metrics(o)
    # Normalize: chi2/KW (lower better → higher ratio = worse)
    # asym: (KW - val)/KW_range → higher val = better → negate
    # m: (KW - val)/range → higher val = better → negate
    # kac: val/KW (more negative better → higher ratio = worse)
    
    # All terms: lower = better, KW ≈ 1.0
    t_chi2 = m['chi2'] / KW_CHI2 if KW_CHI2 > 0 else 0
    t_asym = -m['asym'] / KW_ASYM if KW_ASYM != 0 else 0  # KW=+3, want high → negate
    t_m = -m['m_score'] / KW_M if KW_M > 0 else 0  # KW=12, want high → negate
    t_kac = m['kac'] / KW_KAC if KW_KAC != 0 else 0  # KW=-0.464, want negative → ratio
    
    return (weights[0] * t_chi2 + weights[1] * t_asym +
            weights[2] * t_m + weights[3] * t_kac)


def greedy_optimize_scalar(start_o, weights, rng):
    """Greedy hill-climb minimizing scalarized objective."""
    o = list(start_o)
    val = scalarized_objective(o, weights)
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
                new_val = scalarized_objective(o, weights)
                if new_val < val - 1e-12:
                    val = new_val
                    improved = True
                    continue
            
            if bi['type'] == 'A':
                o[p] = old_val
            else:
                o[p1], o[p2] = old_vals
    return o, val


# Sample 10 weight vectors from the 4-simplex
N_WEIGHT_VECTORS = 10
N_STARTS_PER = 50

rng_e = random.Random(5555)

# Use Dirichlet sampling for uniform simplex points
def sample_simplex(rng, dim=4):
    """Sample uniformly from the dim-simplex."""
    # Exponential(1) samples → normalize
    vals = [-np.log(1 - rng.random()) for _ in range(dim)]
    total = sum(vals)
    return tuple(v / total for v in vals)

# Also include some structured weight vectors
structured_weights = [
    (0.25, 0.25, 0.25, 0.25),  # equal
    (0.5, 0.0, 0.0, 0.5),      # chi2 + kac only
    (0.0, 0.5, 0.5, 0.0),      # asym + m only
    (0.4, 0.1, 0.1, 0.4),      # chi2+kac heavy
    (0.1, 0.4, 0.4, 0.1),      # asym+m heavy
]

random_weights = [sample_simplex(rng_e) for _ in range(N_WEIGHT_VECTORS - len(structured_weights))]
all_weights = structured_weights + random_weights

r2e_results = []
t0 = time.time()

for wi, weights in enumerate(all_weights):
    w_str = f"({weights[0]:.2f},{weights[1]:.2f},{weights[2]:.2f},{weights[3]:.2f})"
    
    best_o = None
    best_val = float('inf')
    
    for trial in range(N_STARTS_PER):
        rng_trial = random.Random(6000 + wi * 100 + trial)
        start = sample_s2_free(rng_trial)
        final_o, final_val = greedy_optimize_scalar(start, weights, rng_trial)
        if final_val < best_val:
            best_val = final_val
            best_o = list(final_o)
    
    metrics = compute_all_metrics(best_o)
    result = report_orientation(f"R2-E w={w_str}", best_o, metrics)
    result['weights'] = list(weights)
    result['scalar_value'] = best_val
    r2e_results.append(result)
    
    elapsed = time.time() - t0
    print(f"  [{wi+1}/{len(all_weights)}] {elapsed:.1f}s elapsed")
    print()

all_results['R2-E'] = r2e_results


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("ROUND 2 SUMMARY: ALL GENERATORS vs KW")
print("=" * 80)
print()

summary_header = (f"{'Generator':>30s} {'chi²':>8s} {'asym':>6s} {'m':>4s} "
                  f"{'kac':>8s} {'Ham':>4s} {'Pareto':>18s}")
print(summary_header)
print("─" * len(summary_header))

# KW reference
print(f"{'KW':>30s} {KW_CHI2:8.3f} {KW_ASYM:6d} {KW_M:4d} "
      f"{KW_KAC:8.4f} {'0':>4s} {'reference':>18s}")

# R2-A variants
for name, result in [("R2-A1 (repeat)", r2a1), ("R2-A2 (h<2)", r2a2), ("R2-A3 (h<3)", r2a3)]:
    m = result['metrics']
    print(f"{name:>30s} {m['chi2']:8.3f} {m['asym']:6d} {m['m_score']:4d} "
          f"{m['kac']:8.4f} {result['hamming_from_kw']:4d} {result['pareto']:>18s}")

# R2-C variants
for r in r2c_results:
    name = f"R2-C ({r['label'][:15]})"
    m = r['metrics']
    print(f"{name:>30s} {m['chi2']:8.3f} {m['asym']:6d} {m['m_score']:4d} "
          f"{m['kac']:8.4f} {r['hamming_from_kw']:4d} {r['pareto']:>18s}")

# R2-D variants
for r in r2d_results:
    name = f"R2-D ({r['label'][:15]})"
    m = r['metrics']
    print(f"{name:>30s} {m['chi2']:8.3f} {m['asym']:6d} {m['m_score']:4d} "
          f"{m['kac']:8.4f} {r['hamming_from_kw']:4d} {r['pareto']:>18s}")

# R2-E: best by Pareto status
for r in r2e_results:
    w = r['weights']
    name = f"R2-E ({w[0]:.1f},{w[1]:.1f},{w[2]:.1f},{w[3]:.1f})"
    if len(name) > 30:
        name = name[:30]
    m = r['metrics']
    print(f"{name:>30s} {m['chi2']:8.3f} {m['asym']:6d} {m['m_score']:4d} "
          f"{m['kac']:8.4f} {r['hamming_from_kw']:4d} {r['pareto']:>18s}")

print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════════════════════════════

with open('/home/quasar/nous/logoswen/iter5/round2_data.json', 'w') as f:
    json.dump(json_clean(all_results), f, indent=2)

print("Data saved to logoswen/iter5/round2_data.json")
print()
print("=" * 80)
print("ROUND 2 COMPLETE")
print("=" * 80)
