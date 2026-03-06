"""
Thread B1: Random Hamiltonian paths on the 6-cube.

The 6-cube has 64 vertices, each with 6 neighbors (differ in exactly 1 bit).
Generate random Hamiltonian paths via Warnsdorff heuristic with random 
tie-breaking, plus backtracking fallback.

Target: 2000 samples.
"""

import sys
import random
import time
from collections import Counter, defaultdict

sys.path.insert(0, '../../kingwen')
from analysis_utils import analyze_sequence, summarize

# --- 6-cube adjacency (precomputed) ---

ALL_VERTICES = [tuple((i >> b) & 1 for b in range(6)) for i in range(64)]
VERTEX_TO_INT = {v: i for i, v in enumerate(ALL_VERTICES)}

# Adjacency: neighbors of each vertex (differ in exactly 1 bit)
ADJ = {}
for v in ALL_VERTICES:
    neighbors = []
    for bit in range(6):
        n = list(v)
        n[bit] = 1 - n[bit]
        neighbors.append(tuple(n))
    ADJ[v] = neighbors


def random_hamiltonian_warnsdorff(rng):
    """
    Generate a random Hamiltonian path using Warnsdorff's heuristic.
    
    At each step, choose the unvisited neighbor with the fewest
    unvisited neighbors (breaking ties randomly). This succeeds 
    with very high probability on the 6-cube.
    
    Returns the path or None if stuck.
    """
    start = rng.choice(ALL_VERTICES)
    path = [start]
    visited = set()
    visited.add(start)
    
    for step in range(63):
        current = path[-1]
        
        # Get unvisited neighbors
        candidates = [n for n in ADJ[current] if n not in visited]
        
        if not candidates:
            return None  # stuck
        
        # Warnsdorff: sort by number of unvisited neighbors of each candidate
        def degree(v):
            return sum(1 for n in ADJ[v] if n not in visited and n != v)
        
        # Group by degree, pick randomly within minimum-degree group
        min_deg = min(degree(c) for c in candidates)
        best = [c for c in candidates if degree(c) == min_deg]
        
        choice = rng.choice(best)
        path.append(choice)
        visited.add(choice)
    
    return path


def random_hamiltonian_backtrack(rng, max_backtracks=50000):
    """
    Fallback: backtracking DFS with random neighbor order.
    Uses Warnsdorff ordering to improve backtracking efficiency.
    """
    start = rng.choice(ALL_VERTICES)
    path = [start]
    visited = {start}
    backtrack_count = 0
    
    def get_sorted_neighbors(v):
        unvisited = [n for n in ADJ[v] if n not in visited]
        # Sort by Warnsdorff degree (ascending)
        unvisited.sort(key=lambda n: sum(1 for nn in ADJ[n] if nn not in visited))
        # Add some randomness within same-degree groups
        result = []
        i = 0
        while i < len(unvisited):
            j = i
            while j < len(unvisited) and sum(1 for nn in ADJ[unvisited[j]] if nn not in visited) == \
                  sum(1 for nn in ADJ[unvisited[i]] if nn not in visited):
                j += 1
            group = unvisited[i:j]
            rng.shuffle(group)
            result.extend(group)
            i = j
        return result
    
    neighbor_iters = [iter(get_sorted_neighbors(start))]
    
    while len(path) < 64:
        if backtrack_count > max_backtracks:
            return None
        
        found = False
        for neighbor in neighbor_iters[-1]:
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                neighbor_iters.append(iter(get_sorted_neighbors(neighbor)))
                found = True
                break
        
        if not found:
            backtrack_count += 1
            removed = path.pop()
            visited.remove(removed)
            neighbor_iters.pop()
            if not path:
                return None
    
    return path


def sample_hamiltonian_paths(n_samples, seed=42):
    """Sample random Hamiltonian paths on the 6-cube."""
    rng = random.Random(seed)
    
    paths = []
    warnsdorff_success = 0
    backtrack_success = 0
    failures = 0
    t0 = time.time()
    
    while len(paths) < n_samples:
        # Try Warnsdorff first (fast, usually works)
        path = random_hamiltonian_warnsdorff(rng)
        if path is not None:
            paths.append(path)
            warnsdorff_success += 1
        else:
            # Fallback to backtracking
            path = random_hamiltonian_backtrack(rng)
            if path is not None:
                paths.append(path)
                backtrack_success += 1
            else:
                failures += 1
        
        if len(paths) % 200 == 0:
            elapsed = time.time() - t0
            rate = len(paths) / elapsed if elapsed > 0 else 0
            print(f"  {len(paths)}/{n_samples} paths ({rate:.0f}/s, "
                  f"W={warnsdorff_success}, BT={backtrack_success}, "
                  f"fail={failures})", flush=True)
    
    elapsed = time.time() - t0
    print(f"  Done: {n_samples} in {elapsed:.1f}s "
          f"(Warnsdorff={warnsdorff_success}, Backtrack={backtrack_success}, "
          f"Failed={failures})")
    
    return paths


def main():
    N_SAMPLES = 2000
    
    print("=" * 70)
    print(f"THREAD B1: RANDOM HAMILTONIAN PATHS ON THE 6-CUBE")
    print(f"Sampling {N_SAMPLES} paths...")
    print("=" * 70)
    
    paths = sample_hamiltonian_paths(N_SAMPLES, seed=42)
    
    # Verify all are valid Hamiltonian paths
    for i, path in enumerate(paths):
        assert len(path) == 64, f"Path {i} has length {len(path)}"
        assert len(set(path)) == 64, f"Path {i} has duplicates"
        for j in range(63):
            h = sum(a != b for a, b in zip(path[j], path[j+1]))
            assert h == 1, f"Path {i} step {j}: Hamming {h} != 1"
    print("  All paths verified as valid Hamiltonian paths on the 6-cube.")
    
    # Analyze each path
    print(f"\nAnalyzing {len(paths)} paths...")
    
    results = []
    for i, path in enumerate(paths):
        r = analyze_sequence(path)
        results.append(r)
        if (i + 1) % 500 == 0:
            print(f"  Analyzed {i+1}/{len(paths)}")
    
    # --- Aggregate statistics ---
    print(f"\n{'=' * 70}")
    print("AGGREGATE STATISTICS")
    print(f"{'=' * 70}")
    
    # 1. Orbit consistency
    oc_values = [r['orbit_consistent'] for r in results]
    oc_counter = Counter(oc_values)
    print(f"\n1. ORBIT CONSISTENCY (pairs using valid Z₂³ masks)")
    print(f"   Mean: {sum(oc_values)/len(oc_values):.2f}/32")
    print(f"   Min: {min(oc_values)}, Max: {max(oc_values)}")
    print(f"   Distribution (top 10): ", end="")
    for val, cnt in sorted(oc_counter.items(), key=lambda x: -x[1])[:10]:
        print(f"{val}:{cnt}", end=" ")
    print()
    all_32 = sum(1 for v in oc_values if v == 32)
    print(f"   All 32 consistent: {all_32}/{N_SAMPLES} ({all_32/N_SAMPLES*100:.4f}%)")
    
    # 2. Eulerian property
    eulerian_count = sum(1 for r in results if r['is_eulerian'])
    print(f"\n2. EULERIAN PROPERTY")
    print(f"   Eulerian: {eulerian_count}/{N_SAMPLES} ({eulerian_count/N_SAMPLES*100:.2f}%)")
    
    # Among orbit-consistent sequences only
    oc_full = [r for r in results if r['orbit_consistent'] == 32]
    if oc_full:
        euler_of_oc = sum(1 for r in oc_full if r['is_eulerian'])
        print(f"   Eulerian | all orbit-consistent: {euler_of_oc}/{len(oc_full)}")
    
    # 3. S distribution
    print(f"\n3. S DISTRIBUTION (H = w + 2S quantization)")
    all_S = []
    for r in results:
        all_S.extend(r['S_values'])
    S_counter = Counter(all_S)
    total_bridges = len(all_S)
    print(f"   Overall S distribution across all bridges:")
    for s_val in sorted(S_counter.keys()):
        print(f"     S={s_val}: {S_counter[s_val]} ({S_counter[s_val]/total_bridges*100:.1f}%)")
    
    mean_S = [sum(r['S_values'])/31 for r in results]
    print(f"   Mean S per sequence: {sum(mean_S)/len(mean_S):.3f}")
    
    s0_fracs = [sum(1 for s in r['S_values'] if s == 0)/31 for r in results]
    print(f"   Mean fraction S=0: {sum(s0_fracs)/len(s0_fracs):.3f}")
    
    s_max_1 = sum(1 for r in results 
                  if all(s in (0, 1) for s in r['S_values']))
    print(f"   All S ∈ {{0,1}} (like KW): {s_max_1}/{N_SAMPLES}")
    
    # 4. Self-loops
    sl_values = [r['self_loop_count'] for r in results]
    sl_counter = Counter(sl_values)
    print(f"\n4. SELF-LOOP COUNT (bridges staying in same orbit)")
    print(f"   Mean: {sum(sl_values)/len(sl_values):.2f}")
    print(f"   Distribution: {dict(sorted(sl_counter.items()))}")
    exactly_2 = sum(1 for v in sl_values if v == 2)
    print(f"   Exactly 2 (like KW): {exactly_2}/{N_SAMPLES}")
    
    # 5. Weight-5 gap
    w5_count = sum(1 for r in results if r['has_weight_5'])
    print(f"\n5. WEIGHT-5 GAP")
    print(f"   Has weight-5 bridges: {w5_count}/{N_SAMPLES} ({w5_count/N_SAMPLES*100:.1f}%)")
    print(f"   No weight-5 (like KW): {N_SAMPLES - w5_count}/{N_SAMPLES}")
    
    all_weights = []
    for r in results:
        all_weights.extend(r['bridge_weights'])
    wt_counter = Counter(all_weights)
    print(f"   Overall bridge weight distribution: {dict(sorted(wt_counter.items()))}")
    
    # 6. Hamiltonian prefix
    prefix_values = [r['prefix_length'] for r in results]
    prefix_counter = Counter(prefix_values)
    print(f"\n6. HAMILTONIAN PREFIX (new orbits before first revisit)")
    print(f"   Mean: {sum(prefix_values)/len(prefix_values):.2f}")
    print(f"   Distribution: {dict(sorted(prefix_counter.items()))}")
    at_least_6 = sum(1 for v in prefix_values if v >= 6)
    print(f"   ≥6 (like KW): {at_least_6}/{N_SAMPLES}")
    
    # 7. Number of orbits used  
    orbits_used = [r['n_orbits_used'] for r in results]
    ou_counter = Counter(orbits_used)
    print(f"\n7. NUMBER OF ORBITS IN BRIDGE GRAPH")
    print(f"   Distribution: {dict(sorted(ou_counter.items()))}")
    
    # 8. Start/end orbits
    start_orbits = Counter(r['start_orbit'] for r in results)
    end_orbits = Counter(r['end_orbit'] for r in results)
    qian_tai = sum(1 for r in results if r['qian_to_tai'])
    print(f"\n8. ENDPOINTS")
    print(f"   Start orbit distribution: {dict(sorted(start_orbits.items()))}")
    print(f"   End orbit distribution: {dict(sorted(end_orbits.items()))}")
    print(f"   Qian(000)→Tai(111) (like KW): {qian_tai}/{N_SAMPLES}")
    
    # 9. Degree balance (how far from Eulerian)
    max_imbalances = []
    for r in results:
        if r['degree_diff']:
            max_imbalances.append(max(abs(d) for d in r['degree_diff'].values()))
        else:
            max_imbalances.append(0)
    imb_counter = Counter(max_imbalances)
    print(f"\n9. MAX DEGREE IMBALANCE (0 or 1 = Eulerian-compatible)")
    print(f"   Distribution: {dict(sorted(imb_counter.items()))}")
    
    # 10. Joint probability: orbit-consistent AND Eulerian
    both = sum(1 for r in results if r['orbit_consistent'] == 32 and r['is_eulerian'])
    print(f"\n10. JOINT: orbit-consistent AND Eulerian: {both}/{N_SAMPLES}")
    
    # --- King Wen reference ---
    print(f"\n{'=' * 70}")
    print("KING WEN REFERENCE VALUES")
    print(f"{'=' * 70}")
    
    from sequence import all_bits
    M = all_bits()
    kw_seq = [tuple(M[i]) for i in range(64)]
    kw_result = analyze_sequence(kw_seq)
    print(summarize(kw_result, "King Wen"))
    print(f"   S_dist: {kw_result['S_dist']}")
    print(f"   Self-loop positions: {kw_result['self_loop_positions']}")
    print(f"   Start orbit: {kw_result['start_orbit']}, End orbit: {kw_result['end_orbit']}")
    print(f"   Weight dist: {kw_result['weight_dist']}")
    
    print(f"\n{'=' * 70}")
    print("B1 ANALYSIS COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
