#!/usr/bin/env python3
"""
visibility_analysis.py — E=1 family visibility and information analysis

For E=1 members of the complement-respecting surjection family:
  (3,5): F₂³ → Z₅, 240 surjections, 1 orbit
  (4,13): F₂⁴ → Z₁₃, ~17M surjections, 960 orbits

Computes:
  1. Fiber size distributions
  2. Mutual information I(x; f(x)) for uniform input
  3. Visibility ceiling = max_fiber_size / |domain|
  4. How these quantities distribute across orbits
"""

import sys
import math
from collections import Counter, defaultdict
from itertools import product as iterproduct, permutations
from math import factorial, comb, log2

# ═══════════════════════════════════════════════════════════
# F₂ utilities (from existing infrastructure)
# ═══════════════════════════════════════════════════════════

def complement(x, n):
    return x ^ ((1 << n) - 1)

def get_complement_pair_reps(n):
    """Return sorted representatives of complement pairs in Z₂ⁿ."""
    reps, seen = [], set()
    for x in range(1 << n):
        if x not in seen:
            cx = complement(x, n)
            seen.add(x)
            seen.add(cx)
            reps.append(min(x, cx))
    return sorted(reps)

def mat_vec_f2(A, v, n):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_det_f2_n(A, n):
    M = [row[:] for row in A]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        for row in range(col + 1, n):
            if M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(n)]
    return 1

def enumerate_gl_f2(n):
    mats = []
    for bits in range(1 << (n*n)):
        A = [[(bits >> (i*n + j)) & 1 for j in range(n)] for i in range(n)]
        if mat_det_f2_n(A, n):
            mats.append(A)
    return mats

def mat_inv_f2(A, n):
    M = [A[i][:] + [1 if i==j else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]:
                pivot = row
                break
        if pivot is None:
            return None
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        for row in range(n):
            if row != col and M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(2*n)]
    return [M[i][n:] for i in range(n)]

# ═══════════════════════════════════════════════════════════
# Information-theoretic quantities
# ═══════════════════════════════════════════════════════════

def mutual_information(fiber_sizes, domain_size):
    """
    I(X; f(X)) for uniform X over domain.
    
    H(X) = log2(domain_size)
    H(X|f(X)) = Σ_y P(Y=y) · log2(|fiber(y)|)
    I = H(X) - H(X|f(X))
    
    Equivalently: I = H(Y) since H(Y) = H(f(X)) and X→f(X) is deterministic.
    Actually: I(X;Y) = H(X) - H(X|Y)
    H(X) = log2(N)
    H(X|Y=y) = log2(|fiber(y)|)
    H(X|Y) = Σ_y (|fiber(y)|/N) * log2(|fiber(y)|)
    I = log2(N) - Σ_y (|fiber(y)|/N) * log2(|fiber(y)|)
    """
    N = domain_size
    H_X = log2(N)
    H_X_given_Y = sum(
        (sz / N) * log2(sz) for sz in fiber_sizes if sz > 0
    )
    return H_X - H_X_given_Y

def entropy_output(fiber_sizes, domain_size):
    """H(f(X)) = H(Y) for uniform X."""
    N = domain_size
    return -sum(
        (sz / N) * log2(sz / N) for sz in fiber_sizes if sz > 0
    )

def visibility_ceiling(fiber_sizes, target_size):
    """Max fiber size / target size = max fraction of target covered by most common preimage count."""
    return max(fiber_sizes) / target_size

def max_fiber_fraction(fiber_sizes, domain_size):
    """Max fiber size / domain size."""
    return max(fiber_sizes) / domain_size


# ═══════════════════════════════════════════════════════════
# (3,5) analysis — full enumeration
# ═══════════════════════════════════════════════════════════

def analyze_35():
    """Complete analysis of (3,5): F₂³ → Z₅."""
    print("=" * 72)
    print("  (3,5): F₂³ → Z₅ — Full Enumeration")
    print("=" * 72)
    
    n, p = 3, 5
    N = 1 << n  # 8
    comp_mask = N - 1  # 7
    reps = get_complement_pair_reps(n)  # [0, 1, 2, 3]
    R = len(reps)
    
    # Enumerate all complement-respecting surjections
    surjections = []
    for assignment in iterproduct(range(p), repeat=R):
        fmap = {}
        for i, r in enumerate(reps):
            fmap[r] = assignment[i]
            fmap[complement(r, n)] = (-assignment[i]) % p
        if len(set(fmap.values())) == p:
            surjections.append(tuple(fmap[x] for x in range(N)))
    
    print(f"\n  Total surjections: {len(surjections)}")
    
    # Compute fiber sizes and info quantities for each surjection
    results = []
    for s in surjections:
        fibers = Counter(s)
        sizes = tuple(sorted(fibers.values(), reverse=True))
        mi = mutual_information(list(fibers.values()), N)
        H_Y = entropy_output(list(fibers.values()), N)
        vc = max(fibers.values()) / p  # visibility ceiling (re: target)
        mf = max(fibers.values()) / N  # max fiber fraction (re: domain)
        results.append({
            'surjection': s,
            'fiber_sizes': sizes,
            'MI': mi,
            'H_Y': H_Y,
            'vis_ceiling': vc,
            'max_fiber_frac': mf,
        })
    
    # Group by fiber shape
    by_shape = defaultdict(list)
    for r in results:
        by_shape[r['fiber_sizes']].append(r)
    
    print(f"\n  Fiber shapes:")
    for shape, rs in sorted(by_shape.items(), key=lambda x: -len(x[1])):
        mi_vals = [r['MI'] for r in rs]
        hy_vals = [r['H_Y'] for r in rs]
        vc_vals = [r['vis_ceiling'] for r in rs]
        print(f"\n    Shape {list(shape)}: {len(rs)} surjections")
        print(f"      I(X;f(X)) = {mi_vals[0]:.4f} bits (constant within shape)")
        print(f"      H(f(X))   = {hy_vals[0]:.4f} bits")
        print(f"      Max fiber / |Z₅| = {vc_vals[0]:.4f}")
        print(f"      Max fiber / |F₂³| = {max(shape)/N:.4f}")
    
    # The IC-specific fiber: {2,2,2,1,1}
    ic_shape = (2, 2, 2, 1, 1)
    ic_results = by_shape.get(ic_shape, [])
    if ic_results:
        r = ic_results[0]
        print(f"\n  ★ The I Ching shape {list(ic_shape)}:")
        print(f"    I(X;f(X)) = {r['MI']:.6f} bits")
        print(f"    H(f(X))   = {r['H_Y']:.6f} bits")
        print(f"    H(f(X))/log₂(5) = {r['H_Y']/log2(5):.6f} (fraction of max)")
        print(f"    Visibility ceiling = max_fiber/|Z₅| = {r['vis_ceiling']:.4f}")
        print(f"    Max visible fraction = max_fiber/8 = {r['max_fiber_frac']:.4f}")
    
    # Channel capacity comparison
    print(f"\n  Channel comparison:")
    print(f"    log₂(8) = {log2(8):.4f} bits (entropy of uniform input)")
    print(f"    log₂(5) = {log2(5):.4f} bits (max possible H(Y))")
    for shape in sorted(by_shape.keys()):
        rs = by_shape[shape]
        r = rs[0]
        print(f"    Shape {list(shape)}: I = {r['MI']:.4f}, H(Y) = {r['H_Y']:.4f}, "
              f"efficiency = {r['H_Y']/log2(5):.4f}")
    
    return results, by_shape


# ═══════════════════════════════════════════════════════════
# (4,13) analysis — partition-based (no full enumeration)
# ═══════════════════════════════════════════════════════════

def analyze_413():
    """Analysis of (4,13): F₂⁴ → Z₁₃ via partition formulas + orbit sampling."""
    print(f"\n\n{'='*72}")
    print("  (4,13): F₂⁴ → Z₁₃ — Partition Analysis + Orbit Sampling")
    print("=" * 72)
    
    n, p = 4, 13
    N = 1 << n  # 16
    comp_mask = N - 1  # 15
    R = N // 2  # 8
    num_neg = (p - 1) // 2  # 6
    S = 1 + num_neg  # 7
    E = R - S  # 1
    
    print(f"\n  R = {R} complement pairs, S = {S} slots, E = {E}")
    
    # Two shapes at E=1:
    # Shape A (majority): m₀=1, one c_j=2, rest c_j=1
    #   Fiber: (2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    # Shape B (minority): m₀=2, all c_j=1
    #   Fiber: (4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    
    shape_A = tuple(sorted([2*1] + [2, 2] + [1]*10, reverse=True))  # 2,2,2 + 10×1
    shape_B = tuple(sorted([2*2] + [1]*12, reverse=True))            # 4 + 12×1
    
    # Recompute properly
    # Shape A: fiber(0)=2, one negation pair has fiber=(2,2), five have fiber=(1,1)
    shape_A = tuple(sorted([2] + [2, 2] + [1, 1]*5, reverse=True))
    # = (2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) — 13 elements, sum = 16 ✓
    
    # Shape B: fiber(0)=4, all negation pairs have fiber=(1,1)
    shape_B = tuple(sorted([4] + [1, 1]*6, reverse=True))
    # = (4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) — 13 elements, sum = 16 ✓
    
    assert sum(shape_A) == N, f"Shape A sum = {sum(shape_A)}"
    assert sum(shape_B) == N, f"Shape B sum = {sum(shape_B)}"
    assert len(shape_A) == p, f"Shape A has {len(shape_A)} fibers"
    assert len(shape_B) == p, f"Shape B has {len(shape_B)} fibers"
    
    # Counts (from np_landscape formulas)
    # Shape A: multi = 8!/(1!·2!·1⁵) = 20160, orderings = 6!/(5!·1!) = 6, orient = 2⁷ = 128
    count_A = (factorial(8) // (factorial(1) * factorial(2))) * \
              (factorial(6) // factorial(5)) * (1 << 7)
    # Shape B: multi = 8!/(2!·1⁶) = 20160, orderings = 6!/6! = 1, orient = 2⁶ = 64
    count_B = (factorial(8) // factorial(2)) * 1 * (1 << 6)
    
    total = count_A + count_B
    
    print(f"\n  Shape A: {list(shape_A)}")
    print(f"    Count: {count_A:,}")
    print(f"  Shape B: {list(shape_B)}")
    print(f"    Count: {count_B:,}")
    print(f"  Total: {total:,}")
    print(f"  Ratio A/B = {count_A/count_B:.1f} (= p-1 = {p-1})")
    
    # Info-theoretic quantities for each shape
    for label, shape in [("A (majority)", shape_A), ("B (minority)", shape_B)]:
        mi = mutual_information(list(shape), N)
        hy = entropy_output(list(shape), N)
        vc = max(shape) / p
        mf = max(shape) / N
        
        print(f"\n  Shape {label}: {list(shape)}")
        print(f"    I(X;f(X)) = {mi:.6f} bits")
        print(f"    H(f(X))   = {hy:.6f} bits")
        print(f"    H(f(X))/log₂(13) = {hy/log2(13):.6f}")
        print(f"    Visibility ceiling = max_fiber/|Z₁₃| = {vc:.4f}")
        print(f"    Max fiber/|F₂⁴| = {mf:.4f}")
    
    # ─── Orbit sampling ───
    print(f"\n  --- Orbit sampling (via construction) ---")
    
    # Sample surjections from shape A and compute orbits
    # Shape A: m₀=1, one c_j=2, five c_j=1
    # We can construct representatives directly
    
    reps = get_complement_pair_reps(n)  # [0, 1, 2, 3, 4, 5, 6, 7]
    comp_pairs = [(r, complement(r, n)) for r in reps]
    neg_pairs = [(k, p-k) for k in range(1, num_neg+1)]
    
    # Construct a few representatives
    sample_surjections = []
    
    # Fix: pair 0 (Frame {0,15}) is Type 0 (maps to 0)
    # Pairs 1,7 are Type 2 (share negation pair {1,12})
    # Pairs 2,3,4,5,6 are Type 1 (each uniquely covers a negation pair)
    
    type0_pair = 0
    type2_pairs = (1, 7)
    type1_pairs = [2, 3, 4, 5, 6]
    
    # Choose shared negation pair for type-2: pair {1,12}
    shared_neg = neg_pairs[0]  # (1, 12)
    remaining_neg = neg_pairs[1:]  # [(2,11), (3,10), (4,9), (5,8), (6,7)]
    
    # Generate some samples with different orientations
    count = 0
    for assignment in permutations(remaining_neg):
        for t2_orient in iterproduct([0,1], repeat=2):
            for t1_orient in iterproduct([0,1], repeat=5):
                vals = [None]*8
                vals[type0_pair] = 0
                for k, pi in enumerate(type2_pairs):
                    vals[pi] = shared_neg[t2_orient[k]]
                for k, pi in enumerate(type1_pairs):
                    vals[pi] = assignment[k][t1_orient[k]]
                
                fmap = {}
                for i, (a, b) in enumerate(comp_pairs):
                    fmap[a] = vals[i]
                    fmap[b] = (-vals[i]) % p
                
                if len(set(fmap.values())) == p:
                    s = tuple(fmap[x] for x in range(N))
                    sample_surjections.append(s)
                    count += 1
                
                if count >= 500:
                    break
            if count >= 500:
                break
        if count >= 500:
            break
    
    print(f"  Sampled {len(sample_surjections)} surjections from shape A")
    
    # Verify they all have shape A
    for s in sample_surjections[:10]:
        fibers = Counter(s)
        shape = tuple(sorted(fibers.values(), reverse=True))
        assert shape == shape_A, f"Wrong shape: {shape}"
    print(f"  Shape verified on sample ✓")
    
    # Compute orbits on sample using kernel × Aut(Z₁₃)
    # Kernel: elements of Stab(1111) that fix all complement pairs
    all_ones = comp_mask
    kernel = []
    for bits in range(16):
        lam = [(bits >> i) & 1 for i in range(4)]
        if lam[0] ^ lam[1] ^ lam[2] ^ lam[3] != 0:
            continue
        g_matrix = [[0]*4 for _ in range(4)]
        for col in range(4):
            e_col = 1 << col
            lam_e = lam[col]
            img = e_col ^ (lam_e * all_ones)
            for row in range(4):
                g_matrix[row][col] = (img >> row) & 1
        kernel.append(g_matrix)
    
    print(f"  |Kernel| = {len(kernel)}")
    
    aut_zp = list(range(1, p))
    kernel_invs = [mat_inv_f2(g, 4) for g in kernel]
    
    # Check how many distinct orbits in our sample
    sample_set = set(sample_surjections)
    parent = {s: s for s in sample_surjections}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    
    for s in sample_surjections:
        for g_inv in kernel_invs:
            for alpha in aut_zp:
                t = tuple((alpha * s[mat_vec_f2(g_inv, x, 4)]) % p for x in range(N))
                if t in sample_set:
                    union(s, t)
    
    orbit_roots = set(find(s) for s in sample_surjections)
    orbit_sizes = Counter()
    for s in sample_surjections:
        orbit_sizes[find(s)] += 1
    
    print(f"  Orbits in sample: {len(orbit_roots)}")
    print(f"  Orbit size distribution: {sorted(Counter(orbit_sizes.values()).items())}")
    
    return shape_A, shape_B, count_A, count_B


# ═══════════════════════════════════════════════════════════
# Cross-comparison
# ═══════════════════════════════════════════════════════════

def compare():
    """Compare visibility properties across E=1 family."""
    print(f"\n\n{'='*72}")
    print("  CROSS-COMPARISON: E=1 Family Visibility")
    print("=" * 72)
    
    # Collect all shape data
    cases = []
    
    # (3,5)
    n, p, N = 3, 5, 8
    shape_35_A = (2, 2, 2, 1, 1)
    shape_35_B = (4, 1, 1, 1, 1)
    cases.append(('(3,5)', n, p, N, shape_35_A, 192, 'A (majority)'))
    cases.append(('(3,5)', n, p, N, shape_35_B, 48, 'B (minority)'))
    
    # (4,13)
    n, p, N = 4, 13, 16
    shape_413_A = tuple(sorted([2] + [2,2] + [1,1]*5, reverse=True))
    shape_413_B = tuple(sorted([4] + [1,1]*6, reverse=True))
    count_A_413 = (factorial(8)//(factorial(1)*factorial(2))) * \
                  (factorial(6)//factorial(5)) * (1<<7)
    count_B_413 = (factorial(8)//factorial(2)) * 1 * (1<<6)
    cases.append(('(4,13)', n, p, N, shape_413_A, count_A_413, 'A (majority)'))
    cases.append(('(4,13)', n, p, N, shape_413_B, count_B_413, 'B (minority)'))
    
    # (5,29)
    n, p, N = 5, 29, 32
    # Shape A: m₀=1, one c_j=2, rest c_j=1 → 14 negation pairs, one gets 2
    # fiber(0)=2, one neg pair has (2,2), 13 have (1,1)
    shape_529_A = tuple(sorted([2] + [2,2] + [1,1]*13, reverse=True))
    # Shape B: m₀=2, all c_j=1
    shape_529_B = tuple(sorted([4] + [1,1]*14, reverse=True))
    # Just use placeholder counts
    cases.append(('(5,29)', n, p, N, shape_529_A, None, 'A (majority)'))
    cases.append(('(5,29)', n, p, N, shape_529_B, None, 'B (minority)'))
    
    print(f"\n  {'Case':<10} {'Shape':<6} {'n':>2} {'p':>3} {'|Dom|':>5} "
          f"{'I(X;f)':>8} {'H(Y)':>8} {'H/Hmax':>7} {'MaxFib/p':>9} {'MaxFib/N':>9}")
    print(f"  {'─'*10} {'─'*6} {'─'*2} {'─'*3} {'─'*5} "
          f"{'─'*8} {'─'*8} {'─'*7} {'─'*9} {'─'*9}")
    
    for label, n, p, N, shape, count, stype in cases:
        mi = mutual_information(list(shape), N)
        hy = entropy_output(list(shape), N)
        hmax = log2(p)
        vc = max(shape) / p
        mf = max(shape) / N
        
        print(f"  {label:<10} {stype:<6} {n:>2} {p:>3} {N:>5} "
              f"{mi:>8.4f} {hy:>8.4f} {hy/hmax:>7.4f} {vc:>9.4f} {mf:>9.4f}")
    
    # ─── Key comparison: visibility ceiling ───
    print(f"\n  Key metric: Visibility ceiling (max_fiber / |target|)")
    print(f"  ─────────────────────────────────────────────────────")
    for label, n, p, N, shape, count, stype in cases:
        if 'A' in stype:
            vc = max(shape) / p
            print(f"    {label} Shape A: {max(shape)}/{p} = {vc:.4f}")
    
    print(f"\n  For Shape A (majority) across E=1 family:")
    print(f"    (3,5):  max fiber = 2, vc = 2/5  = 0.4000")
    print(f"    (4,13): max fiber = 2, vc = 2/13 = 0.1538")
    print(f"    (5,29): max fiber = 2, vc = 2/29 = 0.0690")
    print(f"    Pattern: vc = 2/p → 0 as p → ∞")
    print(f"    The (3,5) case has the HIGHEST visibility ceiling in the E=1 family.")
    print(f"    This is because p is smallest.")
    
    print(f"\n  For Shape B (minority):")
    print(f"    (3,5):  max fiber = 4, vc = 4/5  = 0.8000")
    print(f"    (4,13): max fiber = 4, vc = 4/13 = 0.3077")
    print(f"    (5,29): max fiber = 4, vc = 4/29 = 0.1379")
    print(f"    Pattern: vc = 4/p → 0 as p → ∞")
    
    # ─── Information efficiency ───
    print(f"\n  Information efficiency H(Y)/log₂(p):")
    print(f"  ─────────────────────────────────────")
    for label, n, p, N, shape, count, stype in cases:
        hy = entropy_output(list(shape), N)
        eff = hy / log2(p)
        print(f"    {label} {stype}: {eff:.6f}")
    
    print(f"\n  Shape A efficiency converges to 1 as n→∞ (uniform in the limit).")
    print(f"  Shape B efficiency is lower due to the concentrated fiber(0)=4.")
    
    # ─── The 2/5 structural constant ───
    print(f"\n  ═══════════════════════════════════════════════════")
    print(f"  THE 2/5 VISIBILITY CEILING")
    print(f"  ═══════════════════════════════════════════════════")
    print(f"  At (3,5) Shape A: max fiber = 2 out of 5 target elements.")
    print(f"  This means: at most 2 of 5 relational types are 'visible'")
    print(f"  (can be distinguished) from any single fiber preimage.")
    print(f"")
    print(f"  The 2/5 = 0.4 ceiling is the MAXIMUM across all E=1 members")
    print(f"  for Shape A (three-type coexistence shape).")
    print(f"  It decreases as 2/(2ⁿ-3) for larger n.")
    print(f"")
    print(f"  The I Ching lives at the point of maximum partial visibility:")
    print(f"  large enough to be informative (2/5 > 0), small enough to be")
    print(f"  genuinely partial (2/5 < 1/2).")


def main():
    out_lines = []
    
    # Redirect stdout to capture
    import io
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
        results_35, by_shape_35 = analyze_35()
        shape_A_413, shape_B_413, count_A_413, count_B_413 = analyze_413()
        compare()
    finally:
        sys.stdout = old_stdout
    
    # Write output
    path = "/home/quasar/nous/memories/iching/relations/visibility_analysis_output.txt"
    with open(path, 'w') as f:
        f.write(captured.getvalue())
    print(f"\nResults written to {path}")


if __name__ == "__main__":
    main()
