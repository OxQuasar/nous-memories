"""
Thread B2: Random orbit-paired Hamiltonian paths.

Constraint: pairs must use orbit-determined masks (one of the 8 Z₂³ masks).
This means each pair of consecutive hexagrams stays within an orbit.

Approach:
1. Enumerate/sample orbit-consistent pairings (partition 64 hexagrams into 
   32 pairs, each pair connected by a valid generator mask)
2. For each pairing, sample random orderings that form Hamiltonian paths
3. Analyze bridge structure

The constraint is: within each orbit (8 hexagrams), choose 4 pairs that form
a perfect matching using generator edges. Then order the 32 pairs randomly.
"""

import sys
import random
import time
from collections import Counter, defaultdict
from itertools import product

sys.path.insert(0, '../../kingwen')
from analysis_utils import (analyze_sequence, summarize, xor_sig, 
                             VALID_MASKS, DIMS, build_orbits_by_sig)


# --- Build orbit structure ---

def build_orbit_matchings():
    """
    For each orbit, enumerate all perfect matchings using generator edges.
    
    Each orbit is an 8-vertex graph where edges connect pairs that differ by
    a valid mask (O, M, I, OM, OI, MI, OMI, or id). Only non-identity masks 
    make meaningful pairs (id means the pair is the same hexagram).
    
    Returns dict: orbit_sig -> list of matchings, where each matching is 
    a list of 4 pairs [(a,b), ...].
    """
    orbits = build_orbits_by_sig()
    all_matchings = {}
    
    for sig, hexagrams in orbits.items():
        hexagrams = [tuple(h) for h in hexagrams]
        hex_set = set(hexagrams)
        
        # Build edges: pairs connected by non-identity valid masks
        edges = []
        for i, a in enumerate(hexagrams):
            for j, b in enumerate(hexagrams):
                if i >= j:
                    continue
                mask = tuple(x ^ y for x, y in zip(a, b))
                if mask in VALID_MASKS and mask != (0,0,0,0,0,0):
                    edges.append((a, b, VALID_MASKS[mask]))
        
        # Find all perfect matchings via backtracking
        matchings = []
        _find_matchings(hexagrams, edges, [], set(), matchings)
        all_matchings[sig] = matchings
    
    return all_matchings


def _find_matchings(vertices, edges, current_matching, used, all_matchings):
    """Recursive backtracking to find all perfect matchings."""
    if len(used) == len(vertices):
        all_matchings.append(list(current_matching))
        return
    
    # Find first unused vertex
    first_unused = None
    for v in vertices:
        if v not in used:
            first_unused = v
            break
    
    if first_unused is None:
        return
    
    # Try all edges from first_unused
    for a, b, mask_name in edges:
        partner = None
        if a == first_unused and b not in used:
            partner = b
        elif b == first_unused and a not in used:
            partner = a
        
        if partner is not None:
            used.add(first_unused)
            used.add(partner)
            current_matching.append((first_unused, partner))
            _find_matchings(vertices, edges, current_matching, used, all_matchings)
            current_matching.pop()
            used.remove(first_unused)
            used.remove(partner)


def sample_orbit_paired_sequences(n_samples, seed=42):
    """
    Sample random sequences where all pairs are orbit-consistent.
    
    Method:
    1. For each orbit, randomly choose a perfect matching
    2. Collect all 32 pairs
    3. Randomly order them
    4. For each pair, randomly choose orientation (which hex comes first)
    5. Check if the result forms a valid Hamiltonian path on the 6-cube
       (consecutive hexagrams differ by exactly 1 bit)
    
    Note: We do NOT require the sequence to be a Hamiltonian path on the 6-cube.
    We only require orbit-consistent pairing + random ordering.
    This is the null model: orbit-paired but otherwise random.
    """
    print("  Building orbit matchings...")
    all_matchings = build_orbit_matchings()
    
    # Report matching counts per orbit
    for sig in sorted(all_matchings.keys()):
        n = len(all_matchings[sig])
        print(f"    Orbit {sig}: {n} perfect matchings")
    
    total_matching_combos = 1
    for sig, matchings in all_matchings.items():
        total_matching_combos *= len(matchings)
    print(f"  Total matching combinations: {total_matching_combos}")
    
    rng = random.Random(seed)
    sequences = []
    
    for i in range(n_samples):
        # Pick random matching per orbit
        all_pairs = []
        for sig, matchings in all_matchings.items():
            matching = rng.choice(matchings)
            all_pairs.extend(matching)
        
        # Random ordering of the 32 pairs
        rng.shuffle(all_pairs)
        
        # Random orientation per pair
        seq = []
        for a, b in all_pairs:
            if rng.random() < 0.5:
                seq.extend([a, b])
            else:
                seq.extend([b, a])
        
        sequences.append(seq)
        
        if (i + 1) % 100 == 0:
            print(f"  Generated {i+1}/{n_samples} sequences", flush=True)
    
    return sequences, all_matchings


def main():
    N_SAMPLES = 500
    
    print("=" * 70)
    print(f"THREAD B2: RANDOM ORBIT-PAIRED SEQUENCES")
    print(f"Sampling {N_SAMPLES} sequences...")
    print("=" * 70)
    
    sequences, matchings_info = sample_orbit_paired_sequences(N_SAMPLES, seed=42)
    
    # Analyze each
    print(f"\nAnalyzing {len(sequences)} sequences...")
    
    results = []
    for i, seq in enumerate(sequences):
        r = analyze_sequence(seq)
        results.append(r)
        if (i + 1) % 100 == 0:
            print(f"  Analyzed {i+1}/{len(sequences)}")
    
    # --- Aggregate statistics ---
    print(f"\n{'=' * 70}")
    print("AGGREGATE STATISTICS (ORBIT-PAIRED NULL MODEL)")
    print(f"{'=' * 70}")
    
    # 1. Verify orbit consistency (should be 32/32 by construction)
    oc_values = [r['orbit_consistent'] for r in results]
    print(f"\n1. ORBIT CONSISTENCY: all {min(oc_values)}/32 (by construction)")
    
    # 2. Eulerian property
    eulerian_count = sum(1 for r in results if r['is_eulerian'])
    print(f"\n2. EULERIAN PROPERTY")
    print(f"   Eulerian: {eulerian_count}/{N_SAMPLES} ({eulerian_count/N_SAMPLES*100:.3f}%)")
    if eulerian_count > 0:
        euler_types = Counter(r['eulerian_type'] for r in results if r['is_eulerian'])
        print(f"   Types: {dict(euler_types)}")
    
    # 3. S distribution
    print(f"\n3. S DISTRIBUTION")
    all_S = []
    for r in results:
        all_S.extend(r['S_values'])
    S_counter = Counter(all_S)
    total_S = len(all_S)
    print(f"   Overall S distribution:")
    for s_val in sorted(S_counter.keys()):
        print(f"     S={s_val}: {S_counter[s_val]} ({S_counter[s_val]/total_S*100:.1f}%)")
    
    mean_S_per_seq = [sum(r['S_values'])/31 for r in results]
    print(f"   Mean S per sequence: {sum(mean_S_per_seq)/len(mean_S_per_seq):.3f}")
    
    s_max_1 = sum(1 for r in results 
                  if all(s in (0, 1) for s in r['S_values']))
    print(f"   All S ∈ {{0,1}} (like KW): {s_max_1}/{N_SAMPLES}")
    
    # 4. Self-loops
    sl_values = [r['self_loop_count'] for r in results]
    sl_counter = Counter(sl_values)
    print(f"\n4. SELF-LOOP COUNT")
    print(f"   Mean: {sum(sl_values)/len(sl_values):.2f}")
    print(f"   Distribution: {dict(sorted(sl_counter.items()))}")
    exactly_2 = sum(1 for v in sl_values if v == 2)
    print(f"   Exactly 2 (like KW): {exactly_2}/{N_SAMPLES}")
    
    # 5. Weight-5 gap
    w5_count = sum(1 for r in results if r['has_weight_5'])
    print(f"\n5. WEIGHT-5 GAP")
    print(f"   Has weight-5 bridges: {w5_count}/{N_SAMPLES} ({w5_count/N_SAMPLES*100:.1f}%)")
    
    all_weights = []
    for r in results:
        all_weights.extend(r['bridge_weights'])
    wt_counter = Counter(all_weights)
    print(f"   Overall bridge weight distribution: {dict(sorted(wt_counter.items()))}")
    
    # 6. Hamiltonian prefix
    prefix_values = [r['prefix_length'] for r in results]
    prefix_counter = Counter(prefix_values)
    print(f"\n6. HAMILTONIAN PREFIX")
    print(f"   Mean: {sum(prefix_values)/len(prefix_values):.2f}")
    print(f"   Distribution: {dict(sorted(prefix_counter.items()))}")
    
    # 7. Orbits used in bridge graph
    orbits_used = [r['n_orbits_used'] for r in results]
    ou_counter = Counter(orbits_used)
    print(f"\n7. NUMBER OF ORBITS IN BRIDGE GRAPH")
    print(f"   Distribution: {dict(sorted(ou_counter.items()))}")
    
    # 8. Endpoints
    qian_tai = sum(1 for r in results if r['qian_to_tai'])
    print(f"\n8. ENDPOINTS")
    print(f"   Qian(000)→Tai(111): {qian_tai}/{N_SAMPLES}")
    
    # 9. Degree imbalance
    max_imbalances = []
    for r in results:
        if r['degree_diff']:
            max_imbalances.append(max(abs(d) for d in r['degree_diff'].values()))
        else:
            max_imbalances.append(0)
    imb_counter = Counter(max_imbalances)
    print(f"\n9. MAX DEGREE IMBALANCE")
    print(f"   Distribution: {dict(sorted(imb_counter.items()))}")
    
    # --- King Wen reference ---
    print(f"\n{'=' * 70}")
    print("KING WEN REFERENCE")
    print(f"{'=' * 70}")
    
    from sequence import all_bits
    M = all_bits()
    kw_seq = [tuple(M[i]) for i in range(64)]
    kw_result = analyze_sequence(kw_seq)
    print(summarize(kw_result, "King Wen"))
    
    print(f"\n{'=' * 70}")
    print("B2 ANALYSIS COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
