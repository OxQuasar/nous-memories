"""
Shared utilities for baseline and comparison analyses.

Provides the core metrics computed on any 64-hexagram sequence:
- Orbit consistency of pairs
- Bridge orbit transitions and Eulerian check
- S distribution (H = w + 2S quantization)
- Self-loop count
- Hamiltonian prefix length (new orbits before first revisit)
- Weight-5 gap check
"""

import sys
sys.path.insert(0, '../../kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

DIMS = 6

# The 8 orbit-consistent masks (Z₂³ acting via O, M, I)
VALID_MASKS = {
    (0,0,0,0,0,0): 'id',
    (1,0,0,0,0,1): 'O',
    (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',
    (1,1,0,0,1,1): 'OM',
    (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',
    (1,1,1,1,1,1): 'OMI',
}

# Generator bits for decomposition
GEN_BITS = {
    'O': (1,0,0,0,0,1),
    'M': (0,1,0,0,1,0),
    'I': (0,0,1,1,0,0),
}


def xor_sig(h):
    """Orbit signature: (L1⊕L6, L2⊕L5, L3⊕L4)."""
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def xor_tuple(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def build_orbit_lookup():
    """Map each hexagram (as tuple) to its orbit signature."""
    M = all_bits()
    lookup = {}
    for i in range(64):
        h = tuple(M[i])
        lookup[h] = xor_sig(h)
    return lookup


def build_orbits_by_sig():
    """Map orbit signature -> list of hexagrams in that orbit."""
    M = all_bits()
    orbits = defaultdict(list)
    for i in range(64):
        h = tuple(M[i])
        orbits[xor_sig(h)].append(h)
    return orbits


# Precompute for efficiency
_ORBIT_LOOKUP = build_orbit_lookup()
_ORBITS_BY_SIG = build_orbits_by_sig()


def analyze_sequence(seq):
    """
    Analyze a 64-element sequence of hexagrams (each a tuple of 6 ints).
    
    Returns a dict with all computed metrics.
    """
    assert len(seq) == 64
    
    # --- Pair analysis (32 pairs) ---
    pairs = []
    orbit_consistent_count = 0
    pair_masks = []
    pair_orbits = []
    
    for k in range(32):
        a = seq[2 * k]
        b = seq[2 * k + 1]
        mask = xor_tuple(a, b)
        is_valid = mask in VALID_MASKS
        if is_valid:
            orbit_consistent_count += 1
        pairs.append({'a': a, 'b': b, 'mask': mask, 'valid': is_valid})
        pair_masks.append(mask)
        pair_orbits.append(xor_sig(a))
    
    # --- Bridge analysis (31 bridges: pair k's second hex -> pair k+1's first hex) ---
    bridges = []
    bridge_orbit_transitions = []
    
    for k in range(31):
        a = seq[2 * k + 1]   # second hex of pair k
        b = seq[2 * k + 2]   # first hex of pair k+1
        mask = xor_tuple(a, b)
        sig_a = xor_sig(a)
        sig_b = xor_sig(b)
        h = sum(mask)
        
        # Minimum Hamming to target orbit
        target_hexes = _ORBITS_BY_SIG[sig_b]
        min_h = min(hamming(a, th) for th in target_hexes)
        excess = h - min_h
        S = excess // 2 if excess % 2 == 0 else -1  # -1 means non-even excess
        
        bridges.append({
            'idx': k,
            'a': a, 'b': b,
            'mask': mask,
            'hamming': h,
            'sig_a': sig_a, 'sig_b': sig_b,
            'min_h': min_h,
            'excess': excess,
            'S': S,
            'is_self_loop': sig_a == sig_b,
        })
        bridge_orbit_transitions.append((sig_a, sig_b))
    
    # --- Eulerian check ---
    # Build orbit multigraph: directed edges from sig_a -> sig_b
    # Eulerian path exists iff:
    #   - graph is connected (on used orbits)
    #   - all nodes have in-degree == out-degree, except possibly one source and one sink
    in_deg = Counter()
    out_deg = Counter()
    for sig_a, sig_b in bridge_orbit_transitions:
        out_deg[sig_a] += 1
        in_deg[sig_b] += 1
    
    all_nodes = set(in_deg.keys()) | set(out_deg.keys())
    degree_diff = {}  # out - in
    for node in all_nodes:
        degree_diff[node] = out_deg[node] - in_deg[node]
    
    sources = [n for n, d in degree_diff.items() if d > 0]
    sinks = [n for n, d in degree_diff.items() if d < 0]
    balanced = [n for n, d in degree_diff.items() if d == 0]
    
    is_eulerian = False
    eulerian_type = None
    if len(sources) == 0 and len(sinks) == 0:
        is_eulerian = True
        eulerian_type = 'circuit'
    elif (len(sources) == 1 and len(sinks) == 1 and 
          degree_diff[sources[0]] == 1 and degree_diff[sinks[0]] == -1):
        is_eulerian = True
        eulerian_type = 'path'
    
    # Check connectivity
    if is_eulerian:
        adj = defaultdict(set)
        for sig_a, sig_b in bridge_orbit_transitions:
            adj[sig_a].add(sig_b)
            adj[sig_b].add(sig_a)
        visited = set()
        stack = [next(iter(all_nodes))]
        while stack:
            n = stack.pop()
            if n in visited:
                continue
            visited.add(n)
            for nb in adj[n]:
                if nb not in visited:
                    stack.append(nb)
        if visited != all_nodes:
            is_eulerian = False
            eulerian_type = 'disconnected'
    
    # Eulerian endpoints
    start_orbit = xor_sig(seq[0])
    end_orbit = xor_sig(seq[63])
    qian_to_tai = (start_orbit == (0,0,0) and end_orbit == (1,1,1))
    
    # --- S distribution ---
    S_values = [b['S'] for b in bridges]
    S_dist = Counter(S_values)
    
    # --- Self-loop count ---
    self_loop_count = sum(1 for b in bridges if b['is_self_loop'])
    self_loop_positions = [b['idx'] for b in bridges if b['is_self_loop']]
    
    # --- Weight-5 gap ---
    bridge_weights = [b['hamming'] for b in bridges]
    has_weight_5 = 5 in bridge_weights
    weight_dist = Counter(bridge_weights)
    
    # --- Hamiltonian prefix length ---
    # How many unique orbits are visited before first revisit (in pair orbit sequence)
    seen_orbits = set()
    prefix_length = 0
    for sig in pair_orbits:
        if sig in seen_orbits:
            break
        seen_orbits.add(sig)
        prefix_length += 1
    
    # --- Orbit visit counts ---
    orbit_visits = Counter(pair_orbits)
    
    return {
        'orbit_consistent': orbit_consistent_count,
        'orbit_consistent_frac': orbit_consistent_count / 32,
        'is_eulerian': is_eulerian,
        'eulerian_type': eulerian_type,
        'qian_to_tai': qian_to_tai,
        'start_orbit': start_orbit,
        'end_orbit': end_orbit,
        'S_dist': dict(S_dist),
        'S_values': S_values,
        'self_loop_count': self_loop_count,
        'self_loop_positions': self_loop_positions,
        'has_weight_5': has_weight_5,
        'weight_dist': dict(weight_dist),
        'bridge_weights': bridge_weights,
        'prefix_length': prefix_length,
        'orbit_visits': dict(orbit_visits),
        'n_orbits_used': len(all_nodes),
        'bridges': bridges,
        'pair_masks': pair_masks,
        'degree_diff': degree_diff,
        'sources': sources,
        'sinks': sinks,
    }


def summarize(result, label=""):
    """Print a one-line summary of analysis results."""
    s = f"{label:>15s} | " if label else ""
    s += f"OrbitCons={result['orbit_consistent']}/32 "
    s += f"Euler={'Y' if result['is_eulerian'] else 'N'} "
    s += f"S_dist={result['S_dist']} "
    s += f"SelfLoops={result['self_loop_count']} "
    s += f"Prefix={result['prefix_length']} "
    s += f"Wt5={'Y' if result['has_weight_5'] else 'N'} "
    s += f"Orbits={result['n_orbits_used']}"
    return s
