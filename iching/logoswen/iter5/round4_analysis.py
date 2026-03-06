"""
Iter5 Round 4: Dominator Investigation

P1. Validate all 12 dominators independently
P2. Semantic analysis of Hamming-2 dominator (which hexagrams, what changes)
P3. Structural preservation check — do dominators preserve known KW properties?
P4. Extend search to Hamming ≤8 for full Pareto frontier characterization
P5. Sequential construction hypothesis — can greedy/iterative processes reach KW?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
sys.path.insert(0, '/home/quasar/nous/kingwen')
from infra import *
from sequence import KING_WEN, TRIGRAMS

import json
import time
import itertools
from collections import Counter

print("=" * 80)
print("ITER5 ROUND 4: DOMINATOR INVESTIGATION")
print("=" * 80)
print()
print(f"KW baseline: χ²={KW_CHI2:.4f}  asym={KW_ASYM}  "
      f"m_score={KW_M}/{len(M_DECISIVE)}  kac={KW_KAC:.4f}")
print()

# Load dominator data
with open('/home/quasar/nous/logoswen/iter5/round3_dominators.json') as f:
    dom_data = json.load(f)

all_results = {'kw_baseline': KW_METRICS}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 1: INDEPENDENT VALIDATION OF ALL 12 DOMINATORS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("P1: INDEPENDENT VALIDATION OF ALL 12 DOMINATORS")
print("=" * 80)
print()

validated = []
for i, d in enumerate(dom_data['dominators']):
    o = d['orientation']
    
    # Verify S=2 compliance
    s2ok = is_s2_free(o)
    
    # Recompute metrics from scratch
    m = compute_all_metrics(o)
    
    # Compare to stored values
    stored = d['metrics']
    chi2_match = abs(m['chi2'] - stored['chi2']) < 1e-10
    asym_match = m['asym'] == stored['asym']
    m_match = m['m_score'] == stored['m_score']
    kac_match = abs(m['kac'] - stored['kac']) < 1e-10
    
    # Pareto comparison
    p = pareto_compare(m)
    
    # Check domination: must match or beat KW on all 4 axes
    dom_chi2 = m['chi2'] <= KW_CHI2 + 1e-9
    dom_asym = m['asym'] >= KW_ASYM
    dom_m = m['m_score'] >= KW_M
    dom_kac = m['kac'] <= KW_KAC + 1e-9
    dominates = dom_chi2 and dom_asym and dom_m and dom_kac and (
        m['chi2'] < KW_CHI2 - 1e-9 or m['asym'] > KW_ASYM or 
        m['m_score'] > KW_M or m['kac'] < KW_KAC - 1e-9)
    
    status = "✓ VALID" if (s2ok and chi2_match and asym_match and m_match and 
                            kac_match and dominates) else "✗ INVALID"
    
    print(f"  #{i+1:2d} Ham={d['hamming']:d}  χ²={m['chi2']:.4f}  asym={m['asym']:+d}  "
          f"m={m['m_score']}  kac={m['kac']:.6f}  S2={s2ok}  dom={dominates}  {status}")
    
    validated.append({
        'index': i+1,
        'hamming': d['hamming'],
        'label': d['label'],
        'free_bits': d['free_bit_combo'],
        's2_free': s2ok,
        'metrics_match': chi2_match and asym_match and m_match and kac_match,
        'dominates_kw': dominates,
        'pareto': p,
        'metrics': m,
    })

n_valid = sum(1 for v in validated if v['dominates_kw'] and v['s2_free'])
print(f"\n  VALIDATED: {n_valid}/12 dominators confirmed")
print()

all_results['P1_validation'] = validated


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 2: SEMANTIC ANALYSIS OF HAMMING-2 DOMINATOR
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("P2: SEMANTIC ANALYSIS OF HAMMING-2 DOMINATOR")
print("=" * 80)
print()

dom2 = dom_data['dominators'][0]  # Hamming-2
dom2_o = dom2['orientation']
dom2_bits = dom2['free_bit_combo']  # [17, 26]
dom2_pairs = dom2['pair_indices']   # [21, 29, 30]

print("Flipped free bits: 17, 26")
print(f"  Free bit 17 → pair 21 (Type A)")
print(f"  Free bit 26 → component (29, 30) (Type B)")
print()

# Pair 21 hexagrams
kw_seq = build_sequence(KW_O)
dom2_seq = build_sequence(dom2_o)

# Detail each affected pair
affected_pairs = [21, 29, 30]
for pk in affected_pairs:
    # KW order
    kw_first = kw_seq[2*pk]
    kw_second = kw_seq[2*pk + 1]
    # Dominator order
    d_first = dom2_seq[2*pk]
    d_second = dom2_seq[2*pk + 1]
    
    # Find hexagram names
    kw_first_bits = ''.join(str(b) for b in kw_first)
    kw_second_bits = ''.join(str(b) for b in kw_second)
    d_first_bits = ''.join(str(b) for b in d_first)
    d_second_bits = ''.join(str(b) for b in d_second)
    
    # Find matching hexagram in KING_WEN
    def find_hex_name(bits_str):
        for num, name, bstr in KING_WEN:
            if bstr == bits_str:
                return f"#{num} {name}"
        return f"?({bits_str})"
    
    kw_f_name = find_hex_name(kw_first_bits)
    kw_s_name = find_hex_name(kw_second_bits)
    d_f_name = find_hex_name(d_first_bits)
    d_s_name = find_hex_name(d_second_bits)
    
    swapped = (KW_O[pk] != dom2_o[pk])
    
    print(f"  Pair {pk}{'  [SWAPPED]' if swapped else '  [unchanged]'}:")
    print(f"    KW:        {kw_f_name} ({kw_first_bits}) → {kw_s_name} ({kw_second_bits})")
    if swapped:
        print(f"    Dominator: {d_f_name} ({d_first_bits}) → {d_s_name} ({d_second_bits})")
    print()

# Bridge analysis: which bridges change?
print("BRIDGE CHANGES:")
print(f"{'bridge':>6s} {'KW kernel':>10s} {'Dom kernel':>10s} {'changed':>8s}")
print("─" * 40)

changed_bridges = []
for bk in range(31):
    kw_kern = kernel_name(kw_seq[2*bk+1], kw_seq[2*bk+2])
    d_kern = kernel_name(dom2_seq[2*bk+1], dom2_seq[2*bk+2])
    changed = kw_kern != d_kern
    if changed:
        changed_bridges.append(bk)
    # Only print if near affected pairs or changed
    near_affected = any(abs(bk - pk) <= 1 for pk in affected_pairs)
    if changed or near_affected:
        print(f"{bk:6d} {kw_kern:>10s} {d_kern:>10s} {'***' if changed else '':>8s}")

print()
print(f"  Total bridges changed: {len(changed_bridges)}")
print(f"  Changed bridges: {changed_bridges}")
print()

# Kernel distributions comparison
print("KERNEL DISTRIBUTIONS:")
kw_kernels = Counter()
dom2_kernels = Counter()
for bk in range(31):
    kw_kernels[kernel_name(kw_seq[2*bk+1], kw_seq[2*bk+2])] += 1
    dom2_kernels[kernel_name(dom2_seq[2*bk+1], dom2_seq[2*bk+2])] += 1

print(f"{'kernel':>6s} {'KW':>4s} {'Dom':>4s} {'diff':>5s}")
print("─" * 25)
for g in ALL_GEN_NAMES:
    kc = kw_kernels.get(g, 0)
    dc = dom2_kernels.get(g, 0)
    diff = dc - kc
    print(f"{g:>6s} {kc:4d} {dc:4d} {diff:+5d}" if diff != 0 
          else f"{g:>6s} {kc:4d} {dc:4d}      ")

print()

# Kernel autocorrelation decomposition
print("KERNEL CHAIN COMPARISON (around changed bridges):")
for bk in changed_bridges:
    # Show 3-bridge context
    context_start = max(0, bk - 1)
    context_end = min(31, bk + 2)
    kw_chain = [kernel_name(kw_seq[2*b+1], kw_seq[2*b+2]) for b in range(context_start, context_end)]
    d_chain = [kernel_name(dom2_seq[2*b+1], dom2_seq[2*b+2]) for b in range(context_start, context_end)]
    print(f"  Bridge {bk}: KW chain [{context_start}..{context_end-1}] = {kw_chain}")
    print(f"          Dom chain [{context_start}..{context_end-1}] = {d_chain}")
    
    # Check: do changed bridges reduce adjacent repeats?
    # kac measures sequential anti-repetition

print()

# M-score check for affected pairs
print("M-SCORE CHECK FOR AFFECTED PAIRS:")
for pk in affected_pairs:
    if pk in set(M_DECISIVE):
        kw_l2 = kw_seq[2*pk][1]
        d_l2 = dom2_seq[2*pk][1]
        print(f"  Pair {pk}: M-decisive. KW L2={kw_l2}, Dom L2={d_l2}")
    else:
        print(f"  Pair {pk}: Not M-decisive")
print()

# Asymmetry check
print("ASYMMETRY CHECK:")
for pk in affected_pairs:
    kw_first_val = hex_to_int(kw_seq[2*pk])
    kw_second_val = hex_to_int(kw_seq[2*pk+1])
    d_first_val = hex_to_int(dom2_seq[2*pk])
    d_second_val = hex_to_int(dom2_seq[2*pk+1])
    kw_bh = kw_first_val > kw_second_val
    d_bh = d_first_val > d_second_val
    canon = 'upper' if pk < 15 else 'lower'
    print(f"  Pair {pk} ({canon}): KW binary-high-first={kw_bh}, Dom binary-high-first={d_bh}")
print()

all_results['P2_semantic'] = {
    'affected_pairs': affected_pairs,
    'changed_bridges': changed_bridges,
    'n_changed_bridges': len(changed_bridges),
    'kw_kernel_dist': dict(kw_kernels),
    'dom2_kernel_dist': dict(dom2_kernels),
}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 3: STRUCTURAL PRESERVATION CHECK
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("P3: STRUCTURAL PRESERVATION CHECK — DO DOMINATORS PRESERVE KW PROPERTIES?")
print("=" * 80)
print()

def compute_structural_properties(o):
    """Compute structural properties beyond the 4 core axes."""
    seq = build_sequence(o)
    props = {}
    
    # 1. Kernel chain (full sequence of 31 kernels)
    kernel_chain = []
    for bk in range(31):
        kernel_chain.append(kernel_name(seq[2*bk+1], seq[2*bk+2]))
    props['kernel_chain'] = kernel_chain
    
    # 2. Kernel distribution
    kfreq = Counter(kernel_chain)
    props['kernel_dist'] = dict(kfreq)
    props['kernel_range'] = max(kfreq.values()) - min(kfreq.values()) if kfreq else 0
    
    # 3. Consecutive kernel repeats (count of bridge pairs with same kernel)
    repeats = sum(1 for i in range(30) if kernel_chain[i] == kernel_chain[i+1])
    props['kernel_repeats'] = repeats
    
    # 4. Kernel Hamming chain: sum of Hamming distances between consecutive kernels
    kernel_3bits = []
    for bk in range(31):
        kernel_3bits.append(bridge_kernel_3bit(o, bk))
    ham_chain = sum(hamming_3bit(kernel_3bits[i], kernel_3bits[i+1]) for i in range(30))
    props['kernel_hamming_chain'] = ham_chain
    
    # 5. S-value distribution across bridges  
    s_vals = []
    for bk in range(31):
        s_vals.append(compute_S(seq[2*bk+1], seq[2*bk+2]))
    props['s_distribution'] = dict(Counter(s_vals))
    props['max_s'] = max(s_vals)
    
    # 6. Hamming weight trajectory: sum of Hamming weights of all 64 hexagrams
    weights = [sum(h) for h in seq]
    props['total_weight'] = sum(weights)
    
    # 7. Weight ordering balance (binary-high-first count per pair)
    bh_count = 0
    for k in range(32):
        if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]):
            bh_count += 1
    props['binary_high_first'] = bh_count
    
    # 8. Upper/lower binary-high-first separately
    upper_bh = sum(1 for k in range(15) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    lower_bh = sum(1 for k in range(15, 32) if hex_to_int(seq[2*k]) > hex_to_int(seq[2*k+1]))
    props['upper_bh'] = upper_bh
    props['lower_bh'] = lower_bh
    
    # 9. Kernel autocorrelation lag-2
    kernel_int = [ALL_GEN_NAMES.index(k) for k in kernel_chain]
    ki = np.array(kernel_int, dtype=float)
    ki_centered = ki - ki.mean()
    var = np.var(ki)
    if var > 0 and len(ki) > 2:
        props['kac_lag2'] = float(np.mean(ki_centered[:-2] * ki_centered[2:]) / var)
    else:
        props['kac_lag2'] = 0.0
    
    # 10. Full Hamming weight sequence (64 values)
    props['weight_sequence'] = weights
    
    return props


# Compute for KW
kw_props = compute_structural_properties(KW_O)
print(f"KW structural properties:")
print(f"  Kernel repeats: {kw_props['kernel_repeats']}")
print(f"  Kernel Hamming chain: {kw_props['kernel_hamming_chain']}")
print(f"  Kernel range (max-min count): {kw_props['kernel_range']}")
print(f"  S-distribution: {kw_props['s_distribution']}")
print(f"  Max S: {kw_props['max_s']}")
print(f"  Binary-high-first: {kw_props['binary_high_first']}")
print(f"  Upper BH: {kw_props['upper_bh']}, Lower BH: {kw_props['lower_bh']}")
print(f"  kac lag-2: {kw_props['kac_lag2']:.4f}")
print()

# Compare each dominator
print(f"{'#':>3s} {'Ham':>4s} {'kern_rep':>8s} {'kern_ham':>8s} {'k_range':>7s} "
      f"{'maxS':>4s} {'BH':>4s} {'up_bh':>5s} {'lo_bh':>5s} {'kac2':>8s} "
      f"{'S_dist':>20s}")
print("─" * 95)

# KW row
print(f"{'KW':>3s} {'0':>4s} {kw_props['kernel_repeats']:8d} {kw_props['kernel_hamming_chain']:8d} "
      f"{kw_props['kernel_range']:7d} {kw_props['max_s']:4d} {kw_props['binary_high_first']:4d} "
      f"{kw_props['upper_bh']:5d} {kw_props['lower_bh']:5d} {kw_props['kac_lag2']:8.4f} "
      f"{str(kw_props['s_distribution']):>20s}")

preservation_data = []
for i, d in enumerate(dom_data['dominators']):
    o = d['orientation']
    props = compute_structural_properties(o)
    h = d['hamming']
    
    # Check what's preserved
    same_repeats = props['kernel_repeats'] == kw_props['kernel_repeats']
    same_max_s = props['max_s'] == kw_props['max_s']
    same_bh = props['binary_high_first'] == kw_props['binary_high_first']
    same_s_dist = props['s_distribution'] == kw_props['s_distribution']
    
    print(f"{i+1:3d} {h:4d} {props['kernel_repeats']:8d} {props['kernel_hamming_chain']:8d} "
          f"{props['kernel_range']:7d} {props['max_s']:4d} {props['binary_high_first']:4d} "
          f"{props['upper_bh']:5d} {props['lower_bh']:5d} {props['kac_lag2']:8.4f} "
          f"{str(props['s_distribution']):>20s}")
    
    preservation_data.append({
        'index': i+1,
        'hamming': h,
        'same_kernel_repeats': same_repeats,
        'same_max_s': same_max_s,
        'same_bh': same_bh,
        'same_s_dist': same_s_dist,
        'kernel_repeats': props['kernel_repeats'],
        'kernel_hamming_chain': props['kernel_hamming_chain'],
        'kernel_range': props['kernel_range'],
        'max_s': props['max_s'],
        'binary_high_first': props['binary_high_first'],
        'kac_lag2': props['kac_lag2'],
        's_distribution': props['s_distribution'],
    })

print()

# Summary: what's preserved across all dominators?
all_same_maxS = all(p['same_max_s'] for p in preservation_data)
all_same_bh = all(p['same_bh'] for p in preservation_data)
all_same_s_dist = all(p['same_s_dist'] for p in preservation_data)

print("PRESERVATION SUMMARY:")
print(f"  All preserve max S=1: {all_same_maxS}")
print(f"  All preserve BH count: {all_same_bh}")
print(f"  All preserve S-distribution: {all_same_s_dist}")
print()

# Focus on Hamming-2 dominator structural preservation
dom2_props = compute_structural_properties(dom2_o)
print("HAMMING-2 DOMINATOR vs KW (detailed):")
print(f"  Kernel repeats: KW={kw_props['kernel_repeats']} → Dom={dom2_props['kernel_repeats']}")
print(f"  Kernel Hamming chain: KW={kw_props['kernel_hamming_chain']} → Dom={dom2_props['kernel_hamming_chain']}")
print(f"  kac lag-1: KW={KW_KAC:.4f} → Dom={dom2['metrics']['kac']:.4f}")
print(f"  kac lag-2: KW={kw_props['kac_lag2']:.4f} → Dom={dom2_props['kac_lag2']:.4f}")
print(f"  S-dist match: {dom2_props['s_distribution'] == kw_props['s_distribution']}")
print()

all_results['P3_preservation'] = {
    'kw_properties': {k: v for k, v in kw_props.items() if k != 'weight_sequence' and k != 'kernel_chain'},
    'preservation_data': preservation_data,
    'all_preserve_max_s': all_same_maxS,
    'all_preserve_bh': all_same_bh,
}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 4: EXTEND SEARCH TO HAMMING ≤8 FOR FULL PARETO FRONTIER
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("P4: EXHAUSTIVE SEARCH — HAMMING ≤8 DOMINATORS")
print("=" * 80)
print()

# We already have ≤6. Now extend to 7 and 8.
# 27 choose 7 = 888,030; 27 choose 8 = 2,220,075
# Each combo needs S=2 check and metric computation — expensive but feasible.

# First, build the mapping from free bit index to orientation changes
def apply_free_bits(kw_o, bit_indices):
    """Apply a set of free-bit flips to KW orientation. Return (orientation, valid)."""
    o = list(kw_o)
    for bi_idx in bit_indices:
        bi = free_bits[bi_idx]
        if bi['type'] == 'A':
            p = bi['pairs'][0]
            o[p] = 1 - o[p]
        else:
            p1, p2 = bi['pairs']
            cur = (o[p1], o[p2])
            other = [s for s in bi['valid_states'] if s != cur]
            if not other:
                return o, False
            o[p1], o[p2] = other[0]
    return o, True


# Collect all dominators found so far (from ≤6 search)
known_dominator_sets = set()
for d in dom_data['dominators']:
    known_dominator_sets.add(tuple(sorted(d['free_bit_combo'])))

all_dominators = list(dom_data['dominators'])  # Will extend this

t0 = time.time()

for n_bits in [7, 8]:
    print(f"  Searching Hamming {n_bits}...")
    count = 0
    found = 0
    
    for combo in itertools.combinations(range(27), n_bits):
        o, valid = apply_free_bits(KW_O, combo)
        if not valid:
            continue
        if not is_s2_free(o):
            continue
        count += 1
        
        m = compute_all_metrics(o)
        
        # Check domination
        if (m['chi2'] <= KW_CHI2 + 1e-9 and 
            m['asym'] >= KW_ASYM and
            m['m_score'] >= KW_M and
            m['kac'] <= KW_KAC + 1e-9 and
            (m['chi2'] < KW_CHI2 - 1e-9 or m['asym'] > KW_ASYM or
             m['m_score'] > KW_M or m['kac'] < KW_KAC - 1e-9)):
            
            combo_key = tuple(sorted(combo))
            if combo_key not in known_dominator_sets:
                known_dominator_sets.add(combo_key)
                
                h = hamming(o, KW_O)
                all_dominators.append({
                    'free_bit_combo': list(combo),
                    'label': f'ham-{h}',
                    'hamming': h,
                    'orientation': o,
                    'metrics': m,
                })
                found += 1
    
    elapsed = time.time() - t0
    print(f"    Checked {count} valid orientations, found {found} new dominators ({elapsed:.1f}s)")

print()
print(f"  TOTAL DOMINATORS (Hamming ≤8): {len(all_dominators)}")
print()

# Summarize new dominators
new_doms = [d for d in all_dominators if tuple(sorted(d['free_bit_combo'])) not in 
            set(tuple(sorted(dd['free_bit_combo'])) for dd in dom_data['dominators'])]
if new_doms:
    print(f"  NEW DOMINATORS (Hamming 7-8):")
    for d in sorted(new_doms, key=lambda x: x['metrics']['kac']):
        m = d['metrics']
        print(f"    bits={d['free_bit_combo']}  Ham={d['hamming']}  "
              f"χ²={m['chi2']:.4f}  asym={m['asym']}  m={m['m_score']}  kac={m['kac']:.6f}")
    print()

# Bit frequency across ALL dominators
bit_freq = Counter()
for d in all_dominators:
    for b in d['free_bit_combo']:
        bit_freq[b] += 1

total_doms = len(all_dominators)
print("BIT FREQUENCY ACROSS ALL DOMINATORS:")
print(f"{'bit':>4s} {'pair(s)':>10s} {'freq':>5s} {'%':>6s}")
print("─" * 30)
for bit, freq in sorted(bit_freq.items(), key=lambda x: -x[1]):
    bi = free_bits[bit]
    pairs = bi['pairs']
    print(f"{bit:4d} {str(pairs):>10s} {freq:5d} {100*freq/total_doms:5.1f}%")
print()

# Check: is bit 17 still in ALL dominators?
bit17_in_all = bit_freq.get(17, 0) == total_doms
print(f"  Bit 17 in ALL dominators: {bit17_in_all} ({bit_freq.get(17, 0)}/{total_doms})")
print()

# Hamming distribution of dominators
ham_dist = Counter(d['hamming'] for d in all_dominators)
print("HAMMING DISTRIBUTION:")
for h in sorted(ham_dist.keys()):
    print(f"  Hamming {h}: {ham_dist[h]} dominators")
print()

# kac range across dominators
kac_vals = [d['metrics']['kac'] for d in all_dominators]
print(f"kac range: min={min(kac_vals):.6f}  max={max(kac_vals):.6f}  "
      f"median={np.median(kac_vals):.6f}")
print(f"  KW kac: {KW_KAC:.6f}")
print(f"  Best improvement: {(min(kac_vals) - KW_KAC)/abs(KW_KAC)*100:.1f}%")
print()

all_results['P4_extended_search'] = {
    'total_dominators': len(all_dominators),
    'hamming_distribution': dict(ham_dist),
    'bit_frequency': dict(bit_freq),
    'bit17_in_all': bit17_in_all,
    'kac_range': {'min': min(kac_vals), 'max': max(kac_vals), 'median': float(np.median(kac_vals))},
    'new_dominators_count': len(new_doms),
}


# ══════════════════════════════════════════════════════════════════════════════
# PRIORITY 5: SEQUENTIAL CONSTRUCTION HYPOTHESIS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("P5: SEQUENTIAL CONSTRUCTION HYPOTHESIS")
print("=" * 80)
print()

# Hypothesis: KW was constructed by a sequential process where pairs are 
# oriented one at a time, in order. What objective would lead to KW?

# Test 1: Sequential greedy with L1-to-KW objective
# Process pairs 0..31. For each, choose the orientation (0 or 1) that 
# minimizes the L1 distance to KW's metrics on the partial sequence so far.

# Test 2: Sequential greedy with "M-rule default + kac-aware override"
# Default: M-rule. Override if it worsens kac of partial sequence.

# Test 3: Forward sequential diversity with distributional balance

def compute_partial_metrics(seq_so_far, n_pairs_set):
    """Compute what we can from a partial sequence (first n_pairs_set pairs)."""
    # Only bridges 0..n_pairs_set-2 are defined
    n_bridges = n_pairs_set - 1
    if n_bridges < 1:
        return {'chi2': 0, 'asym': 0, 'm_score': 0, 'kac': 0}
    
    kernel_chain = []
    kfreq = Counter()
    for bk in range(n_bridges):
        kn = kernel_name(seq_so_far[2*bk+1], seq_so_far[2*bk+2])
        kernel_chain.append(kn)
        kfreq[kn] += 1
    
    # Partial chi2
    expected = n_bridges / 8
    chi2 = sum((kfreq.get(g, 0) - expected)**2 / expected for g in ALL_GEN_NAMES) if expected > 0 else 0
    
    # Partial kac
    if n_bridges >= 2:
        ki = np.array([ALL_GEN_NAMES.index(k) for k in kernel_chain], dtype=float)
        ki_c = ki - ki.mean()
        var = np.var(ki)
        kac = float(np.mean(ki_c[:-1] * ki_c[1:]) / var) if var > 0 else 0
    else:
        kac = 0
    
    # Partial asym
    upper_bh = sum(1 for k in range(min(15, n_pairs_set)) 
                   if hex_to_int(seq_so_far[2*k]) > hex_to_int(seq_so_far[2*k+1]))
    lower_bh = sum(1 for k in range(15, n_pairs_set)
                   if hex_to_int(seq_so_far[2*k]) > hex_to_int(seq_so_far[2*k+1]))
    asym = upper_bh - lower_bh
    
    # Partial m_score
    m_score = 0
    m_dec_set = set(M_DECISIVE)
    for k in range(n_pairs_set):
        if k in m_dec_set:
            if seq_so_far[2*k][1] == 0:
                m_score += 1
    
    return {'chi2': chi2, 'asym': asym, 'm_score': m_score, 'kac': kac}


# ── Test 1: Sequential greedy targeting KW profile ────────────────────────

print("TEST 1: Sequential greedy targeting KW's exact profile")
print()

seq_o = [0] * 32

for k in range(32):
    best_choice = 0
    best_cost = float('inf')
    
    for choice in [0, 1]:
        seq_o[k] = choice
        
        # Check S=2 constraint with previous pair
        if k > 0 and k-1 in CONSTRAINTS and (seq_o[k-1], seq_o[k]) in CONSTRAINTS[k-1]:
            continue
        
        # Build partial sequence
        partial_seq = build_sequence(seq_o)
        
        # Compute metrics on what we have so far
        pm = compute_partial_metrics(partial_seq, k + 1)
        
        # L1 cost vs KW's final profile
        # But we can't compute final metrics from partial — use current chi2 trend
        # Actually, just evaluate the FULL metrics assuming rest stays at 0
        trial_o = list(seq_o)
        # Leave rest as 0 (KW default)
        full_m = compute_all_metrics(trial_o)
        cost = (abs(full_m['chi2'] - KW_CHI2) / KW_CHI2 +
                abs(full_m['asym'] - KW_ASYM) / max(abs(KW_ASYM), 1) +
                abs(full_m['m_score'] - KW_M) / KW_M +
                abs(full_m['kac'] - KW_KAC) / abs(KW_KAC))
        
        if cost < best_cost:
            best_cost = cost
            best_choice = choice
    
    seq_o[k] = best_choice

seq1_metrics = compute_all_metrics(seq_o)
seq1_pareto = pareto_compare(seq1_metrics)
seq1_hamming = hamming(seq_o, KW_O)

print(f"  Result: {orientation_str(seq_o)}")
report_orientation("Greedy-L1-forward", seq_o, seq1_metrics)

all_results['P5_seq1'] = {
    'orientation': seq_o,
    'metrics': seq1_metrics,
    'pareto': seq1_pareto,
    'hamming_from_kw': seq1_hamming,
}


# ── Test 2: M-rule default + kac-aware override ──────────────────────────

print("TEST 2: M-rule default + kac-aware override")
print()

seq2_o = [0] * 32
overrides = []

for k in range(32):
    a = PAIRS[k]['a']
    
    # M-rule default
    if a[1] != a[4]:  # M-decisive
        m_choice = 0 if a[1] == 0 else 1
    else:  # M-indecisive: binary-high-first
        m_choice = 0 if hex_to_int(a) >= hex_to_int(PAIRS[k]['b']) else 1
    
    # Check S=2 compliance
    if k > 0 and k-1 in CONSTRAINTS and (seq2_o[k-1], m_choice) in CONSTRAINTS[k-1]:
        # M-rule violates S=2; use the other choice
        alt_choice = 1 - m_choice
        seq2_o[k] = alt_choice
        overrides.append({'pair': k, 'reason': 'S=2', 'from': m_choice, 'to': alt_choice})
        continue
    
    # Check kac: would M-rule worsen kac compared to current trajectory?
    # Compare: set k to m_choice vs 1-m_choice, evaluate kac of full orientation (rest at 0)
    trial_m = list(seq2_o)
    trial_m[k] = m_choice
    trial_alt = list(seq2_o)
    trial_alt[k] = 1 - m_choice
    
    # Check alt is S=2 valid
    alt_valid = True
    if k > 0 and k-1 in CONSTRAINTS and (seq2_o[k-1], 1-m_choice) in CONSTRAINTS[k-1]:
        alt_valid = False
    
    if alt_valid:
        # Both choices are valid; compare kac
        if is_s2_free(trial_m) and is_s2_free(trial_alt):
            m_metrics = compute_all_metrics(trial_m)
            alt_metrics = compute_all_metrics(trial_alt)
            
            if alt_metrics['kac'] < m_metrics['kac'] - 0.01:  # kac threshold for override
                seq2_o[k] = 1 - m_choice
                overrides.append({'pair': k, 'reason': 'kac-override', 
                                  'kac_diff': alt_metrics['kac'] - m_metrics['kac']})
                continue
    
    seq2_o[k] = m_choice

seq2_metrics = compute_all_metrics(seq2_o)
seq2_pareto = pareto_compare(seq2_metrics)
seq2_hamming = hamming(seq2_o, KW_O)

print(f"  Overrides: {len(overrides)}")
for ov in overrides:
    print(f"    Pair {ov['pair']}: {ov['reason']}" + 
          (f" (Δkac={ov.get('kac_diff', 0):.4f})" if 'kac_diff' in ov else ""))
print()
print(f"  Result: {orientation_str(seq2_o)}")
report_orientation("M-rule+kac-override", seq2_o, seq2_metrics)

all_results['P5_seq2'] = {
    'orientation': list(seq2_o),
    'metrics': seq2_metrics,
    'pareto': seq2_pareto,
    'hamming_from_kw': seq2_hamming,
    'overrides': overrides,
}


# ── Test 3: Reverse-engineer — what objective gives KW? ──────────────────

print("TEST 3: Which single-objective greedy gives KW or closest?")
print()

# Try various objectives:
objectives = {
    'kac_only': lambda m: m['kac'],  # more negative = better → minimize
    'chi2_only': lambda m: m['chi2'],  # lower = better → minimize
    'L1_to_target': lambda m: (abs(m['chi2'] - KW_CHI2)/KW_CHI2 + 
                                abs(m['asym'] - KW_ASYM)/3 +
                                abs(m['m_score'] - KW_M)/KW_M +
                                abs(m['kac'] - KW_KAC)/abs(KW_KAC)),
    'kac_weighted': lambda m: 0.2*m['chi2']/KW_CHI2 + 0.1*(-m['asym']/3) + 0.1*(-m['m_score']/12) + 0.6*m['kac']/abs(KW_KAC),
    'balanced': lambda m: m['chi2']/KW_CHI2 + (-m['asym']/3) + (-m['m_score']/12) + m['kac']/abs(KW_KAC),
}

for obj_name, obj_fn in objectives.items():
    # Greedy sequential: process pairs in order, choose orientation minimizing objective
    o = [0] * 32
    for k in range(32):
        best = None
        best_val = float('inf')
        for choice in [0, 1]:
            o[k] = choice
            if k > 0 and k-1 in CONSTRAINTS and (o[k-1], o[k]) in CONSTRAINTS[k-1]:
                continue
            if is_s2_free(o):
                m = compute_all_metrics(o)
                val = obj_fn(m)
                if val < best_val:
                    best_val = val
                    best = choice
        if best is not None:
            o[k] = best
        else:
            o[k] = 0  # fallback
    
    m = compute_all_metrics(o)
    h = hamming(o, KW_O)
    p = pareto_compare(m)
    print(f"  {obj_name:>18s}: χ²={m['chi2']:.3f}  asym={m['asym']:+d}  "
          f"m={m['m_score']}  kac={m['kac']:.4f}  Ham={h:2d}  {p}")

print()

# ── Test 4: Reverse greedy from the other end ────────────────────────────

print("TEST 4: Reverse sequential (pairs 31→0)")
print()

for obj_name, obj_fn in [('kac_only', lambda m: m['kac']),
                          ('L1_to_target', lambda m: (abs(m['chi2'] - KW_CHI2)/KW_CHI2 + 
                                abs(m['asym'] - KW_ASYM)/3 +
                                abs(m['m_score'] - KW_M)/KW_M +
                                abs(m['kac'] - KW_KAC)/abs(KW_KAC)))]:
    o = [0] * 32
    for k in range(31, -1, -1):
        best = None
        best_val = float('inf')
        for choice in [0, 1]:
            o[k] = choice
            if k < 31 and k in CONSTRAINTS and (o[k], o[k+1]) in CONSTRAINTS[k]:
                continue
            if is_s2_free(o):
                m = compute_all_metrics(o)
                val = obj_fn(m)
                if val < best_val:
                    best_val = val
                    best = choice
        if best is not None:
            o[k] = best
        else:
            o[k] = 0
    
    m = compute_all_metrics(o)
    h = hamming(o, KW_O)
    p = pareto_compare(m)
    print(f"  {obj_name:>18s}: χ²={m['chi2']:.3f}  asym={m['asym']:+d}  "
          f"m={m['m_score']}  kac={m['kac']:.4f}  Ham={h:2d}  {p}")

print()


# ── Test 5: Can a process find KW from the dominators? ────────────────────

print("TEST 5: Is KW reachable from dominators via single-bit descent?")
print()

# Starting from the Hamming-2 dominator, try to reach KW by greedy single-bit
# flips on the L1 objective
dom2_o_copy = list(dom2_o)
dom2_m = compute_all_metrics(dom2_o_copy)
dom2_l1 = (abs(dom2_m['chi2'] - KW_CHI2)/KW_CHI2 + 
           abs(dom2_m['asym'] - KW_ASYM)/3 +
           abs(dom2_m['m_score'] - KW_M)/KW_M +
           abs(dom2_m['kac'] - KW_KAC)/abs(KW_KAC))

print(f"  Hamming-2 dominator L1 cost (distance from KW): {dom2_l1:.6f}")
print(f"  KW L1 cost: 0.000000")
print()

# From the dominator, which single-bit flips move toward KW?
print("  Single-bit descents from Hamming-2 dominator toward KW:")
for bi_idx in range(27):
    o_trial = list(dom2_o_copy)
    bi = free_bits[bi_idx]
    if bi['type'] == 'A':
        p = bi['pairs'][0]
        o_trial[p] = 1 - o_trial[p]
    else:
        p1, p2 = bi['pairs']
        cur = (o_trial[p1], o_trial[p2])
        other = [s for s in bi['valid_states'] if s != cur]
        if not other:
            continue
        o_trial[p1], o_trial[p2] = other[0]
    
    if not is_s2_free(o_trial):
        continue
    
    m = compute_all_metrics(o_trial)
    l1 = (abs(m['chi2'] - KW_CHI2)/KW_CHI2 + 
          abs(m['asym'] - KW_ASYM)/3 +
          abs(m['m_score'] - KW_M)/KW_M +
          abs(m['kac'] - KW_KAC)/abs(KW_KAC))
    
    h_from_kw = hamming(o_trial, KW_O)
    
    # Is this moving toward KW?
    if l1 < dom2_l1 - 1e-9:
        p = pareto_compare(m)
        print(f"    bit {bi_idx:2d}: L1={l1:.6f} (↓{dom2_l1-l1:.6f})  Ham={h_from_kw}  "
              f"kac={m['kac']:.4f}  {p}")

print()

# Does bit 17 flip (back to KW value) improve or worsen?
# Bit 17 is flipped in the dominator. Flipping it back → KW at pair 21.
o_back17 = list(dom2_o_copy)
o_back17[21] = 0  # KW value
if is_s2_free(o_back17):
    m17 = compute_all_metrics(o_back17)
    l17 = (abs(m17['chi2'] - KW_CHI2)/KW_CHI2 + 
           abs(m17['asym'] - KW_ASYM)/3 +
           abs(m17['m_score'] - KW_M)/KW_M +
           abs(m17['kac'] - KW_KAC)/abs(KW_KAC))
    p17 = pareto_compare(m17)
    print(f"  Flipping bit 17 back (pair 21 → KW): L1={l17:.6f}  kac={m17['kac']:.4f}  {p17}")
    print(f"    This is 1 bit from KW (only bit 26 differs)")
    print(f"    Single-bit 26 from KW → {p17} (trade-off, so KW doesn't take it)")
print()


# ══════════════════════════════════════════════════════════════════════════════
# 5TH AXIS HYPOTHESIS: CHECK IF DOMINATORS DIFFER ON UNMEASURED PROPERTIES
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("BONUS: 5TH AXIS HYPOTHESIS — KERNEL AUTOCORRELATION LAG-2")
print("=" * 80)
print()

# Check kac lag-2 for all dominators vs KW
print(f"  KW kac_lag2: {kw_props['kac_lag2']:.6f}")
print()

dom_better_lag2 = 0
dom_worse_lag2 = 0
for i, d in enumerate(all_dominators):
    props = compute_structural_properties(d['orientation'])
    diff = props['kac_lag2'] - kw_props['kac_lag2']
    if diff > 0.01:
        dom_worse_lag2 += 1
    elif diff < -0.01:
        dom_better_lag2 += 1
    
    if i < 12:  # Print first 12
        print(f"    #{i+1} Ham={d['hamming']} kac_lag2={props['kac_lag2']:+.6f}  "
              f"diff={diff:+.6f}")

print()
print(f"  Dominators with worse kac_lag2: {dom_worse_lag2}/{len(all_dominators)}")
print(f"  Dominators with better kac_lag2: {dom_better_lag2}/{len(all_dominators)}")
print()

# Check another candidate 5th axis: kernel run lengths
print("KERNEL RUN LENGTH ANALYSIS:")
def max_kernel_run(o):
    seq = build_sequence(o)
    chain = [kernel_name(seq[2*bk+1], seq[2*bk+2]) for bk in range(31)]
    max_run = 1
    cur_run = 1
    for i in range(1, len(chain)):
        if chain[i] == chain[i-1]:
            cur_run += 1
            max_run = max(max_run, cur_run)
        else:
            cur_run = 1
    return max_run

kw_max_run = max_kernel_run(KW_O)
print(f"  KW max kernel run: {kw_max_run}")

for i, d in enumerate(all_dominators[:12]):
    mr = max_kernel_run(d['orientation'])
    print(f"    #{i+1} Ham={d['hamming']} max_run={mr}")
print()

# Check: weight balance per-pair
print("HAMMING WEIGHT BALANCE (total weight of 64 hexagrams is invariant):")
kw_total_weight = sum(sum(h) for h in kw_seq)
print(f"  KW total weight: {kw_total_weight}")
for i, d in enumerate(all_dominators[:3]):
    ds = build_sequence(d['orientation'])
    tw = sum(sum(h) for h in ds)
    print(f"    #{i+1} total weight: {tw}")
print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE ALL DATA
# ══════════════════════════════════════════════════════════════════════════════

# Save extended dominator list
extended_doms = {
    'total_dominators': len(all_dominators),
    'dominators': [{
        'free_bit_combo': d['free_bit_combo'],
        'label': d.get('label', f"ham-{d['hamming']}"),
        'hamming': d['hamming'],
        'orientation': d['orientation'],
        'metrics': d['metrics'],
    } for d in all_dominators],
    'bit_frequency': dict(bit_freq),
    'bit17_in_all': bit17_in_all,
    'hamming_distribution': dict(ham_dist),
}

with open('/home/quasar/nous/logoswen/iter5/round4_dominators_extended.json', 'w') as f:
    json.dump(json_clean(extended_doms), f, indent=2)

# Save analysis results
with open('/home/quasar/nous/logoswen/iter5/round4_data.json', 'w') as f:
    json.dump(json_clean(all_results), f, indent=2)

print("Data saved to round4_data.json and round4_dominators_extended.json")
print()
print("=" * 80)
print("ROUND 4 COMPLETE")
print("=" * 80)
