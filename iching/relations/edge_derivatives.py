#!/usr/bin/env python3
"""
edge_derivatives.py — Edge derivative profile on the Boolean cube

For complement-respecting surjections f: F₂³ → Z₅, the Boolean cube has
12 directed edges (3 masks × 8 vertices, with d(x,m) = -d(x⊕m, m)).

Computes for each of the 5 orbits:
1. Derivative table: d(x, m) = f(x ⊕ m) - f(x) mod 5
2. Derivative distribution: frequency of each d value
3. Boolean sensitivity: s(x) = # masks where d(x,m) ≠ 0
4. Z₅-weighted sensitivity: sum of min(d, 5-d)
5. Comparison across orbits
"""

import sys
import io
from collections import Counter, defaultdict
from itertools import product as iterproduct

# Import from five_orbits
from five_orbits import (
    complement, mat_vec_f2, mat_inv_f2, enumerate_gl3f2,
    get_complement_pairs, enumerate_surjections, compute_stab111,
    compute_orbits, fiber_shape, type_distribution, is_ic_orbit,
    IC_WUXING, TRIG_ZH, ELEM_NAME
)

# ═══════════════════════════════════════════════════════════
# Edge derivatives
# ═══════════════════════════════════════════════════════════

MASKS = [1, 2, 4]  # 001, 010, 100
MASK_NAMES = {1: '001', 2: '010', 4: '100'}

def edge_derivative(s, x, m, p=5):
    """d(x, m) = f(x ⊕ m) - f(x) mod p"""
    return (s[x ^ m] - s[x]) % p

def derivative_table(s, p=5):
    """Full derivative table: {(x, m): d(x,m)} for all x, m."""
    table = {}
    for x in range(8):
        for m in MASKS:
            table[(x, m)] = edge_derivative(s, x, m, p)
    return table

def derivative_distribution(s, p=5):
    """Frequency of each derivative value across all edges."""
    vals = []
    for x in range(8):
        for m in MASKS:
            vals.append(edge_derivative(s, x, m, p))
    return Counter(vals)

def boolean_sensitivity(s, p=5):
    """For each vertex x: s(x) = # masks where d(x,m) ≠ 0."""
    result = {}
    for x in range(8):
        result[x] = sum(1 for m in MASKS if edge_derivative(s, x, m, p) != 0)
    return result

def z5_weight(d, p=5):
    """Z₅ distance: min(d, p-d). The unsigned version of d."""
    return min(d % p, (-d) % p)

def weighted_sensitivity(s, p=5):
    """Sum of Z₅-weighted derivatives: Σ_{x,m} min(d(x,m), 5-d(x,m))."""
    total = 0
    for x in range(8):
        for m in MASKS:
            d = edge_derivative(s, x, m, p)
            total += z5_weight(d, p)
    return total

def per_vertex_weighted(s, p=5):
    """Per-vertex weighted sensitivity."""
    result = {}
    for x in range(8):
        result[x] = sum(z5_weight(edge_derivative(s, x, m, p), p) for m in MASKS)
    return result


# ═══════════════════════════════════════════════════════════
# Orbit-level statistics
# ═══════════════════════════════════════════════════════════

def orbit_derivative_stats(orbit, p=5):
    """Compute derivative statistics for an orbit."""
    # Check if derivative distribution is orbit-invariant
    dists = set()
    weighted_sens = set()
    
    for s in orbit:
        dd = derivative_distribution(s, p)
        dists.add(tuple(sorted(dd.items())))
        weighted_sens.add(weighted_sensitivity(s, p))
    
    dist_invariant = len(dists) == 1
    weighted_invariant = len(weighted_sens) == 1
    
    # Use representative
    rep = sorted(orbit)[0]
    
    return {
        'rep': rep,
        'deriv_dist': derivative_distribution(rep, p),
        'dist_invariant': dist_invariant,
        'n_distinct_dists': len(dists),
        'bool_sens': boolean_sensitivity(rep, p),
        'avg_bool_sens': sum(boolean_sensitivity(rep, p).values()) / 8,
        'weighted_sens': weighted_sensitivity(rep, p),
        'weighted_invariant': weighted_invariant,
        'n_distinct_weighted': len(weighted_sens),
    }


def main():
    old_stdout = sys.stdout
    captured = io.StringIO()

    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
        def flush(self):
            for f in self.files:
                f.flush()

    sys.stdout = Tee(old_stdout, captured)

    try:
        p = 5
        
        print("=" * 72)
        print("  EDGE DERIVATIVE PROFILE")
        print("=" * 72)
        print()
        
        # Get orbits
        surjections = enumerate_surjections()
        stab = compute_stab111()
        orbits = compute_orbits(surjections, stab, p)
        
        print(f"  {len(orbits)} orbits, sizes: {[len(o) for o in orbits]}")
        print()
        
        # ─── I Ching derivative table ───
        ic_tuple = tuple(IC_WUXING[x] for x in range(8))
        ic_orbit_idx = None
        for idx, orbit in enumerate(orbits):
            if ic_tuple in orbit:
                ic_orbit_idx = idx
                break
        
        print("  " + "=" * 68)
        print("  I CHING DERIVATIVE TABLE")
        print("  " + "=" * 68)
        print()
        print(f"  f = {list(ic_tuple)}")
        print(f"  {'x':>5} {'f(x)':>5}   {'d(x,001)':>8} {'d(x,010)':>8} {'d(x,100)':>8}   {'s(x)':>4} {'w(x)':>4}")
        print(f"  {'-'*52}")
        
        bs = boolean_sensitivity(ic_tuple, p)
        pvw = per_vertex_weighted(ic_tuple, p)
        
        for x in range(8):
            fx = ic_tuple[x]
            d001 = edge_derivative(ic_tuple, x, 1, p)
            d010 = edge_derivative(ic_tuple, x, 2, p)
            d100 = edge_derivative(ic_tuple, x, 4, p)
            sx = bs[x]
            wx = pvw[x]
            label = f"{TRIG_ZH[x]}({ELEM_NAME[fx]})"
            print(f"  {format(x,'03b'):>5} {fx:>5}   {d001:>8} {d010:>8} {d100:>8}   {sx:>4} {wx:>4}   {label}")
        
        dd = derivative_distribution(ic_tuple, p)
        ws = weighted_sensitivity(ic_tuple, p)
        avg_s = sum(bs.values()) / 8
        
        print()
        print(f"  Derivative distribution: {dict(sorted(dd.items()))}")
        print(f"  Average Boolean sensitivity: {avg_s:.3f}")
        print(f"  Total weighted sensitivity: {ws}")
        print()
        
        # Verify complement antisymmetry: d(x,m) = -d(x⊕m, m)
        print("  Complement antisymmetry check: d(x,m) + d(x⊕m, m) ≡ 0 mod 5")
        all_ok = True
        for x in range(8):
            for m in MASKS:
                cx = x ^ m
                d1 = edge_derivative(ic_tuple, x, m, p)
                d2 = edge_derivative(ic_tuple, cx, m, p)
                if (d1 + d2) % p != 0:
                    print(f"    FAIL: d({format(x,'03b')},{MASK_NAMES[m]}) + d({format(cx,'03b')},{MASK_NAMES[m]}) = {d1}+{d2} = {(d1+d2)%p}")
                    all_ok = False
        print(f"  {'✓ All pass' if all_ok else '✗ Some fail'}")
        print()
        
        # Also verify: d(x,m) = -d(~x, m) where ~x is complement
        # This follows from f(~x) = -f(x): d(x,m) = f(x⊕m)-f(x), 
        # d(~x,m) = f(~x⊕m)-f(~x) = f(~(x⊕m)⊕(m⊕111⊕m))... hmm, 
        # ~x⊕m = (x⊕111)⊕m = x⊕(111⊕m) ≠ ~(x⊕m) in general.
        # So this isn't a simple relation. Skip.
        
        # ─── All orbits comparison ───
        print("  " + "=" * 68)
        print("  DERIVATIVE COMPARISON ACROSS ALL ORBITS")
        print("  " + "=" * 68)
        print()
        
        orbit_stats = []
        for idx, orbit in enumerate(orbits):
            stats = orbit_derivative_stats(orbit, p)
            stats['idx'] = idx
            stats['size'] = len(orbit)
            stats['is_ic'] = is_ic_orbit(orbit)
            stats['shape'] = fiber_shape(sorted(orbit)[0])
            orbit_stats.append(stats)
        
        # Summary table
        print(f"  {'Orbit':>5} {'Size':>5} {'Shape':>15} {'Deriv Dist':>25} {'Avg s(x)':>8} {'W':>4} {'IC':>3} {'Dinv':>4}")
        print(f"  {'-'*75}")
        
        for stats in orbit_stats:
            dd = stats['deriv_dist']
            dd_str = str(dict(sorted(dd.items())))
            marker = "★" if stats['is_ic'] else ""
            dinv = "✓" if stats['dist_invariant'] else f"({stats['n_distinct_dists']})"
            print(f"  {stats['idx']:>5} {stats['size']:>5} {str(list(stats['shape'])):>15} {dd_str:>25} {stats['avg_bool_sens']:>8.3f} {stats['weighted_sens']:>4} {marker:>3} {dinv:>4}")
        
        print()
        print(f"  Dinv = derivative distribution is orbit-invariant (same for all elements)")
        print()
        
        # ─── Detailed derivative tables for all orbits ───
        print("  " + "=" * 68)
        print("  DERIVATIVE TABLES FOR ORBIT REPRESENTATIVES")
        print("  " + "=" * 68)
        
        for stats in orbit_stats:
            rep = stats['rep']
            idx = stats['idx']
            is_ic = stats['is_ic']
            
            print(f"\n  ─── Orbit {idx} {'(I Ching)' if is_ic else ''} ───")
            print(f"  f = {list(rep)}, shape = {list(stats['shape'])}")
            print(f"  {'x':>5} {'f(x)':>5}   {'d(001)':>6} {'d(010)':>6} {'d(100)':>6}   {'s(x)':>4}")
            
            bs_rep = boolean_sensitivity(rep, p)
            for x in range(8):
                fx = rep[x]
                d001 = edge_derivative(rep, x, 1, p)
                d010 = edge_derivative(rep, x, 2, p)
                d100 = edge_derivative(rep, x, 4, p)
                sx = bs_rep[x]
                print(f"  {format(x,'03b'):>5} {fx:>5}   {d001:>6} {d010:>6} {d100:>6}   {sx:>4}")
            
            print(f"  Dist: {dict(sorted(stats['deriv_dist'].items()))}, W={stats['weighted_sens']}")
        
        # ─── Orbit-level aggregate analysis ───
        print()
        print("  " + "=" * 68)
        print("  ORBIT-LEVEL AGGREGATE ANALYSIS")
        print("  " + "=" * 68)
        print()
        
        # Per-representative comparison is misleading — derivative dist
        # varies within orbits. Compute the AVERAGED distributions.
        print("  NOTE: Derivative distribution varies within orbits (not orbit-invariant).")
        print("  Computing ORBIT-AVERAGED statistics.")
        print()
        
        for idx, orbit in enumerate(orbits):
            total_dd = Counter()
            total_w = 0
            w_dist = Counter()
            for s in orbit:
                for x in range(8):
                    for m in MASKS:
                        d = edge_derivative(s, x, m, p)
                        total_dd[d] += 1
                total_w += weighted_sensitivity(s, p)
                w_dist[weighted_sensitivity(s, p)] += 1
            
            is_ic = is_ic_orbit(orbit)
            marker = " ★" if is_ic else ""
            avg_w = total_w / len(orbit)
            avg_dd = {d: total_dd[d] / len(orbit) for d in range(p)}
            shape = fiber_shape(sorted(orbit)[0])
            
            print(f"  Orbit {idx} (size {len(orbit)}, shape {list(shape)}){marker}:")
            print(f"    Avg derivative dist: {{{', '.join(f'{d}:{avg_dd[d]:.1f}' for d in range(p))}}}")
            print(f"    Avg weighted sensitivity: {avg_w:.2f}")
            print(f"    W distribution: {dict(sorted(w_dist.items()))}")
            print()
        
        # ─── Analysis ───
        print("  " + "=" * 68)
        print("  ANALYSIS")
        print("  " + "=" * 68)
        print()
        
        print("  KEY FINDINGS:")
        print()
        print("  1. Derivative distribution is NOT orbit-invariant.")
        print("     Within each orbit, different surjections have different")
        print("     derivative distributions. This is because the Stab(111)")
        print("     action permutes vertices but the mask directions are fixed.")
        print()
        print("  2. ORBIT-AVERAGED derivative distribution distinguishes")
        print("     Shape A from Shape B:")
        print("     - Shape A (orbits 0,1,2): avg {0:2.0, 1:5.5, 2:5.5, 3:5.5, 4:5.5}")
        print("     - Shape B (orbits 3,4):   avg {0:4.0, 1:5.0, 2:5.0, 3:5.0, 4:5.0}")
        print("     Shape B has more zero derivatives (4 vs 2) — consistent")
        print("     with its larger fiber ({4,1,1,1,1} has more local degeneracy).")
        print()
        print("  3. Average derivative distribution does NOT distinguish")
        print("     the IC orbit from other Shape A orbits.")
        print("     All three Shape A orbits have identical averages.")
        print()
        print("  4. Weighted sensitivity W distribution:")
        print("     - Shape A orbits: {28:24, 32:48, 40:24} — avg 33.0")
        print("     - Shape B orbits: {28:12, 32:12} — avg 30.0")
        print("     The proportions scale with orbit size but the values")
        print("     are the same within each shape.")
        print()
        print("  5. The I Ching's SPECIFIC surjection has:")
        print(f"     - Derivative dist: {dict(sorted(derivative_distribution(ic_tuple, p).items()))}")
        print(f"     - W = {weighted_sensitivity(ic_tuple, p)}")
        print(f"     - This is the {{{', '.join(f'{d}:{derivative_distribution(ic_tuple,p).get(d,0)}' for d in range(5))}}} type,")
        print(f"       one of 4 types in the IC orbit (24 surjections each).")
        print()
        print("  CONCLUSION: Derivative statistics separate fiber shapes but")
        print("  do NOT distinguish the IC orbit from other Shape A orbits.")
        print("  The IC orbit's uniqueness lies in its algebraic property:")
        print("  it is the ONLY orbit with FREE action (|orbit| = |G| = 96).")
        
    finally:
        sys.stdout = old_stdout
    
    path = "/home/quasar/nous/memories/iching/relations/edge_derivatives_output.md"
    with open(path, 'w') as f:
        f.write(captured.getvalue())
    print(f"\nResults written to {path}")


if __name__ == "__main__":
    main()
