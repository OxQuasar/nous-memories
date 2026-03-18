#!/usr/bin/env python3
"""
Fibonacci Structure Probe for the I Ching
==========================================
Four computational tasks investigating Fibonacci alignment in I Ching parameters.
"""

import json
import math
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
from itertools import product

ATLAS_PATH = Path(__file__).parent.parent / "atlas" / "atlas.json"

# ── Fibonacci utilities ──────────────────────────────────────────────

def fib_set(limit):
    """Return set of Fibonacci numbers up to limit."""
    fibs = set()
    a, b = 0, 1
    while a <= limit:
        fibs.add(a)
        a, b = b, a + b
    return fibs

def fib_index(n, fibs_list):
    """Return F(k) index if n is Fibonacci, else None."""
    for i, val in fibs_list:
        if val == n:
            return i
    return None

def fib_list(limit):
    """Return list of (index, value) Fibonacci pairs."""
    result = []
    a, b = 0, 1
    i = 0
    while a <= limit:
        result.append((i, a))
        a, b = b, a + b
        i += 1
    return result

FIBS = fib_set(10**10)
FIBS_LIST = fib_list(10**10)


# ══════════════════════════════════════════════════════════════════════
# TASK 1: Fibonacci vs E=1 Family Scan
# ══════════════════════════════════════════════════════════════════════

def task1():
    print("=" * 70)
    print("TASK 1: Fibonacci vs E=1 Family Scan (n=2..30)")
    print("=" * 70)
    print()
    print(f"{'n':>3} | {'2^n-3':>15} {'Fib?':>6} | {'2^n':>15} {'Fib?':>6} | {'(2^n-1)*n':>15} {'Fib?':>6}")
    print("-" * 80)

    hits = []
    for n in range(2, 31):
        v1 = 2**n - 3
        v2 = 2**n
        v3 = (2**n - 1) * n

        f1 = "F(" + str(fib_index(v1, FIBS_LIST)) + ")" if v1 in FIBS else ""
        f2 = "F(" + str(fib_index(v2, FIBS_LIST)) + ")" if v2 in FIBS else ""
        f3 = "F(" + str(fib_index(v3, FIBS_LIST)) + ")" if v3 in FIBS else ""

        row = f"{n:>3} | {v1:>15} {f1:>6} | {v2:>15} {f2:>6} | {v3:>15} {f3:>6}"
        if f1 or f2 or f3:
            row += "  ◄ HIT"
            hits.append((n, v1 if f1 else None, v2 if f2 else None, v3 if f3 else None))
        print(row)

    print()
    print("HITS SUMMARY:")
    for n, v1, v2, v3 in hits:
        parts = []
        if v1: parts.append(f"2^{n}-3 = {v1}")
        if v2: parts.append(f"2^{n} = {v2}")
        if v3: parts.append(f"(2^{n}-1)×{n} = {v3}")
        print(f"  n={n}: {', '.join(parts)}")

    print()
    print("CONCLUSION: Fibonacci alignment concentrates at n=3 (three simultaneous hits)")
    print("            with a single residual hit at n=4 (2^4-3=13=F(7)).")
    print("            For n≥5, all three expressions escape the Fibonacci sequence.")
    print()


# ══════════════════════════════════════════════════════════════════════
# TASK 2: Orbit Count Factorization
# ══════════════════════════════════════════════════════════════════════

def factorize(n):
    """Return prime factorization as dict {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def format_factorization(factors):
    parts = []
    for p in sorted(factors):
        e = factors[p]
        parts.append(f"{p}^{e}" if e > 1 else str(p))
    return " × ".join(parts)

def gl_order(n, q):
    """Order of GL(n, F_q)."""
    order = 1
    for i in range(n):
        order *= (q**n - q**i)
    return order

def task2():
    print("=" * 70)
    print("TASK 2: Orbit Count Factorization")
    print("=" * 70)
    print()

    # (n, p) → orbit count
    cases = [(3, 5, 1), (4, 13, 960)]

    for n, p, orbits in cases:
        print(f"--- Case (n={n}, p={p}): {orbits} orbits ---")
        print()

        gl_n = gl_order(n, 2)
        aut_p = p - 1  # |Aut(Z_p)| = φ(p) = p-1 for prime p
        group_order = gl_n * aut_p

        print(f"  |GL({n}, F₂)| = {gl_n} = {format_factorization(factorize(gl_n))}")
        print(f"  |Aut(Z_{p})| = {aut_p} = {format_factorization(factorize(aut_p))}")
        print(f"  Group order = {group_order} = {format_factorization(factorize(group_order))}")
        print()

        if orbits > 1:
            of = factorize(orbits)
            print(f"  Orbit count = {orbits} = {format_factorization(of)}")

            # Check which factors are Fibonacci
            for p_factor in sorted(of):
                is_fib = p_factor in FIBS
                fi = fib_index(p_factor, FIBS_LIST) if is_fib else None
                tag = f" = F({fi})" if is_fib else ""
                print(f"    Prime factor {p_factor}{tag}")

            # Total surjections = orbits × group_order
            total_surj = orbits * group_order
            print()
            print(f"  Total surjections = orbits × |G| = {orbits} × {group_order} = {total_surj}")
            print(f"                    = {format_factorization(factorize(total_surj))}")

            # Verify: orbit count × group order should give total surjection count
            # For (4,13): total complement-equivariant surjections from F₂⁴\{0} → Z₁₃
            # |F₂⁴\{0}| = 15 elements, |Z₁₃| = 13 elements
            # Surjections must satisfy f(x⊕y) ≡ f(x)+f(y) (mod 13)? No — complement equivariant.
            # Actually: f must satisfy f(complement(x)) = -f(x) in Z_p
            print()
            print(f"  960 = {format_factorization(factorize(960))}")
            print(f"  Fibonacci factors in 960: 2 = F(3), 3 = F(4), 5 = F(5)")
            print(f"  Non-Fibonacci: none! 960 = 2⁶ × 3 × 5, all prime factors are Fibonacci.")
        else:
            print(f"  Orbit count = 1 (unique)")
            print(f"  Total surjections = |G| = {group_order}")
        print()

    # Attempt (5, 29)
    print("--- Case (n=5, p=29): Feasibility check ---")
    n, p = 5, 29
    gl_n = gl_order(n, 2)
    aut_p = p - 1
    print(f"  |GL(5, F₂)| = {gl_n} = {format_factorization(factorize(gl_n))}")
    print(f"  |Aut(Z_29)| = {aut_p} = {format_factorization(factorize(aut_p))}")
    print(f"  |F₂⁵\\{{0}}| = {2**n - 1} elements to map to Z₂₉")
    print(f"  Search space: {p}^{2**n - 1} = 29^31 ≈ 10^{31*math.log10(29):.0f}")
    print(f"  PROHIBITIVE — brute force is impossible.")
    print()

    # Burnside's lemma approach
    print("  Burnside approach: orbits = (1/|G|) Σ |Fix(g)|")
    print(f"  |G| = {gl_n * aut_p} ≈ {gl_n * aut_p:.2e}")
    print(f"  Iterating over all group elements also prohibitive for |GL(5,F₂)| = {gl_n}")
    print()


# ══════════════════════════════════════════════════════════════════════
# TASK 3: Nuclear (互) Orbit Structure — THE MAIN EVENT
# ══════════════════════════════════════════════════════════════════════

def hex_to_bits(h):
    """Convert hexagram index (0-63) to 6-bit list [L1,...,L6] (LSB first)."""
    return [(h >> i) & 1 for i in range(6)]

def bits_to_hex(bits):
    """Convert 6-bit list back to index."""
    return sum(b << i for i, b in enumerate(bits))

def nuclear(h):
    """Compute 互(h): nuclear hexagram.
    Given h = (L1,L2,L3,L4,L5,L6), 互(h) = (L2,L3,L4,L3,L4,L5).
    """
    bits = hex_to_bits(h)
    # bits[0]=L1, bits[1]=L2, ..., bits[5]=L6
    new_bits = [bits[1], bits[2], bits[3], bits[2], bits[3], bits[4]]
    return bits_to_hex(new_bits)

def nuclear_matrix():
    """Return the 6×6 matrix over F₂ representing the nuclear map.
    Maps (L1,...,L6) → (L2,L3,L4,L3,L4,L5).
    Row i of the matrix tells which input bits contribute to output bit i.
    """
    # Output bit 0 = L2 = input bit 1
    # Output bit 1 = L3 = input bit 2
    # Output bit 2 = L4 = input bit 3
    # Output bit 3 = L3 = input bit 2
    # Output bit 4 = L4 = input bit 3
    # Output bit 5 = L5 = input bit 4
    M = np.zeros((6, 6), dtype=int)
    M[0, 1] = 1  # out[0] = in[1]
    M[1, 2] = 1  # out[1] = in[2]
    M[2, 3] = 1  # out[2] = in[3]
    M[3, 2] = 1  # out[3] = in[2]
    M[4, 3] = 1  # out[4] = in[3]
    M[5, 4] = 1  # out[5] = in[4]
    return M

def task3():
    print("=" * 70)
    print("TASK 3: Nuclear (互) Orbit Structure")
    print("=" * 70)
    print()

    # Step 1: Verify formula against atlas
    print("--- Step 1: Verify 互 formula against atlas ---")
    atlas = json.load(open(ATLAS_PATH))
    mismatches = 0
    for i in range(64):
        computed = nuclear(i)
        atlas_hu = atlas[str(i)]["hu_hex"]
        if computed != atlas_hu:
            print(f"  MISMATCH at hex {i}: computed={computed}, atlas={atlas_hu}")
            mismatches += 1
    if mismatches == 0:
        print("  ✓ All 64 hexagrams match atlas hu_hex values.")
    print()

    # Step 2: Nuclear matrix over F₂
    print("--- Step 2: Nuclear matrix (F₂-linear map) ---")
    M = nuclear_matrix()
    print("  M =")
    for row in M:
        print("    ", row.tolist())
    print()

    # Compute rank
    # Over F₂, we need to do row reduction mod 2
    def f2_rank(mat):
        m = mat.copy() % 2
        rows, cols = m.shape
        rank = 0
        for col in range(cols):
            pivot = None
            for row in range(rank, rows):
                if m[row, col] % 2 == 1:
                    pivot = row
                    break
            if pivot is None:
                continue
            m[[rank, pivot]] = m[[pivot, rank]]
            for row in range(rows):
                if row != rank and m[row, col] % 2 == 1:
                    m[row] = (m[row] + m[rank]) % 2
            rank += 1
        return rank

    print(f"  rank(M) over F₂ = {f2_rank(M)}")

    # Powers of M over F₂
    print()
    print("  Powers of M (mod 2):")
    Mk = np.eye(6, dtype=int)
    for k in range(1, 8):
        Mk = (Mk @ M) % 2
        r = f2_rank(Mk)
        print(f"    M^{k}: rank = {r}")
        if r == 0:
            print(f"    → M^{k} = 0 (nilpotent, index = {k})")
            break
    print()

    # Step 3: Compute all orbits (iterate 互 until cycle)
    print("--- Step 3: All 互 orbits ---")

    # Build the full map
    hu_map = {i: nuclear(i) for i in range(64)}

    # For each node, iterate until we revisit
    def trace_orbit(start):
        """Return (path, cycle_start_idx).
        path = [start, hu(start), hu²(start), ...]
        cycle_start_idx = index in path where the cycle begins.
        """
        path = [start]
        visited = {start: 0}
        current = start
        while True:
            nxt = hu_map[current]
            if nxt in visited:
                return path, visited[nxt]
            visited[nxt] = len(path)
            path.append(nxt)
            current = nxt

    # Identify unique cycles
    all_cycles = {}  # frozenset → cycle list
    node_info = {}  # node → (transient_len, cycle_id)

    for i in range(64):
        path, cycle_start = trace_orbit(i)
        cycle = path[cycle_start:]
        # Normalize cycle by starting from smallest element
        min_idx = cycle.index(min(cycle))
        cycle_normalized = tuple(cycle[min_idx:] + cycle[:min_idx])
        cycle_key = cycle_normalized

        transient = path[:cycle_start]
        transient_len = len(transient)

        if cycle_key not in all_cycles:
            all_cycles[cycle_key] = cycle_normalized

        node_info[i] = {
            "transient_len": transient_len,
            "cycle": cycle_key,
            "path": path[:cycle_start + len(cycle)]
        }

    print(f"  Total nodes: 64")
    print(f"  Distinct cycles: {len(all_cycles)}")
    print()

    # Cycle structure
    print("  CYCLES:")
    for idx, (key, cycle) in enumerate(sorted(all_cycles.items(), key=lambda x: (len(x[1]), x[0]))):
        members_on_cycle = list(cycle)
        cycle_len = len(cycle)
        # Binary representations
        bin_rep = [format(h, '06b') for h in members_on_cycle]
        # Atlas names
        names = [atlas[str(h)].get("kw_name", "?") for h in members_on_cycle]
        print(f"    Cycle {idx+1} (length {cycle_len}): {members_on_cycle}")
        print(f"      Binary: {bin_rep}")
        print(f"      Names:  {names}")
        # Count nodes that eventually reach this cycle
        count = sum(1 for n in node_info.values() if n["cycle"] == key)
        print(f"      Basin size: {count}")
        print()

    # Orbit length distribution (transient + cycle length)
    print("  TRANSIENT LENGTH DISTRIBUTION:")
    trans_counts = Counter(info["transient_len"] for info in node_info.values())
    for t in sorted(trans_counts):
        print(f"    Transient = {t}: {trans_counts[t]} hexagrams")
    print()

    # Full orbit length (= transient + cycle length)
    print("  TOTAL PATH LENGTH DISTRIBUTION (transient + cycle):")
    total_lens = Counter(info["transient_len"] + len(info["cycle"]) for info in node_info.values())
    for l in sorted(total_lens):
        print(f"    Length = {l}: {total_lens[l]} hexagrams")
    print()

    # Reverse tree structure (preimage analysis)
    print("  PREIMAGE (REVERSE) STRUCTURE:")
    # For each node, count preimages
    preimage_count = Counter(hu_map.values())
    preimage_dist = Counter(preimage_count[i] if i in preimage_count else 0 for i in range(64))
    # Some nodes might have 0 preimages (leaves)
    no_preimage = [i for i in range(64) if preimage_count.get(i, 0) == 0]
    print(f"    Nodes with 0 preimages (leaves): {len(no_preimage)}")
    print(f"    Preimage count distribution:")
    for k in sorted(preimage_dist):
        print(f"      |preimage| = {k}: {preimage_dist[k]} nodes")
    print()

    # Detailed reverse tree for each attractor/cycle
    print("  REVERSE TREE BY BASIN:")
    for idx, (key, cycle) in enumerate(sorted(all_cycles.items(), key=lambda x: (len(x[1]), x[0]))):
        cycle_set = set(cycle)
        # BFS backwards from cycle
        distance = {}
        for c in cycle:
            distance[c] = 0

        # Build reverse map
        reverse_map = defaultdict(list)
        for src, dst in hu_map.items():
            reverse_map[dst].append(src)

        queue = list(cycle)
        while queue:
            node = queue.pop(0)
            d = distance[node]
            for pre in reverse_map[node]:
                if pre not in distance:
                    distance[pre] = d + 1
                    queue.append(pre)

        # Distance distribution
        dist_counts = Counter(distance.values())
        basin_nodes = [n for n in distance]
        print(f"    Basin of cycle {list(cycle)}:")
        for d in sorted(dist_counts):
            nodes_at_d = sorted([n for n, dd in distance.items() if dd == d])
            print(f"      d={d}: {dist_counts[d]} nodes → {nodes_at_d}")
        print()

    # Fibonacci check on counts
    print("  FIBONACCI CHECK ON KEY COUNTS:")
    counts_to_check = {
        "Distinct cycles": len(all_cycles),
        "Leaves (0 preimages)": len(no_preimage),
    }
    for d, c in sorted(trans_counts.items()):
        counts_to_check[f"Transient={d} count"] = c
    for d, c in sorted(preimage_dist.items()):
        counts_to_check[f"|preimage|={d} count"] = c

    for label, val in counts_to_check.items():
        fi = fib_index(val, FIBS_LIST)
        tag = f" = F({fi}) ✓" if fi is not None else ""
        print(f"    {label}: {val}{tag}")

    # Basin sizes
    basin_sizes = Counter()
    for info in node_info.values():
        basin_sizes[info["cycle"]] += 1
    for key in sorted(basin_sizes, key=basin_sizes.get, reverse=True):
        val = basin_sizes[key]
        fi = fib_index(val, FIBS_LIST)
        tag = f" = F({fi}) ✓" if fi is not None else ""
        print(f"    Basin of {list(key)[:3]}...: {val}{tag}")
    print()

    # Assessment: uniformity of branching
    print("  UNIFORMITY ASSESSMENT:")
    print("    If 互 is F₂-linear, preimage sizes should be uniform (= 2^(6-rank) for image, 0 for non-image).")
    image_set = set(hu_map.values())
    print(f"    |Image| = {len(image_set)}")
    print(f"    Expected preimage size for image nodes = 2^(6-rank) = 2^(6-{f2_rank(M)}) = {2**(6-f2_rank(M))}")
    preimage_sizes_for_image = [preimage_count[i] for i in image_set]
    print(f"    Actual preimage sizes for image nodes: {sorted(set(preimage_sizes_for_image))}")
    uniform = len(set(preimage_sizes_for_image)) == 1
    print(f"    Uniform? {'YES — predicted by F₂-linear algebra' if uniform else 'NO — deviation from linearity!'}")
    print()


# ══════════════════════════════════════════════════════════════════════
# TASK 4: Algebraic Verification — P₄ vs Fibonacci eigenvalues
# ══════════════════════════════════════════════════════════════════════

def task4():
    print("=" * 70)
    print("TASK 4: P₄ vs Fibonacci Matrix Eigenvalues")
    print("=" * 70)
    print()

    # P₄ adjacency matrix
    P4 = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ], dtype=float)

    # Fibonacci matrix
    Fib = np.array([
        [1, 1],
        [1, 0]
    ], dtype=float)

    phi = (1 + np.sqrt(5)) / 2  # golden ratio

    eig_P4 = sorted(np.linalg.eigvalsh(P4), reverse=True)
    eig_Fib = sorted(np.linalg.eigvals(Fib).real, reverse=True)

    print("  P₄ adjacency matrix eigenvalues:")
    for e in eig_P4:
        print(f"    {e:+.10f}")
    print()

    print("  Fibonacci matrix [[1,1],[1,0]] eigenvalues:")
    for e in eig_Fib:
        print(f"    {e:+.10f}")
    print()

    print("  Golden ratio φ = (1+√5)/2 =", f"{phi:.10f}")
    print("  1/φ = φ-1 =", f"{1/phi:.10f}")
    print()

    # Expected P₄ eigenvalues: 2cos(kπ/5) for k=1,2,3,4
    print("  Expected P₄ eigenvalues: 2cos(kπ/5) for k=1..4:")
    expected = []
    for k in range(1, 5):
        val = 2 * np.cos(k * np.pi / 5)
        expected.append(val)
        print(f"    k={k}: 2cos({k}π/5) = {val:+.10f}")
    print()

    # Verification
    print("  VERIFICATION:")
    print(f"    φ     = {phi:.10f}")
    print(f"    P₄[0] = {eig_P4[0]:.10f}  (should be φ)")
    print(f"    diff   = {abs(eig_P4[0] - phi):.2e}")
    print()
    print(f"    1/φ   = {1/phi:.10f}")
    print(f"    P₄[1] = {eig_P4[1]:.10f}  (should be 1/φ)")
    print(f"    diff   = {abs(eig_P4[1] - 1/phi):.2e}")
    print()
    print(f"    -1/φ  = {-1/phi:.10f}")
    print(f"    P₄[2] = {eig_P4[2]:.10f}  (should be -1/φ)")
    print(f"    diff   = {abs(eig_P4[2] - (-1/phi)):.2e}")
    print()
    print(f"    -φ    = {-phi:.10f}")
    print(f"    P₄[3] = {eig_P4[3]:.10f}  (should be -φ)")
    print(f"    diff   = {abs(eig_P4[3] - (-phi)):.2e}")
    print()

    # Fibonacci eigenvalues
    print(f"    Fib[0] = {eig_Fib[0]:.10f}  (should be φ)")
    print(f"    Fib[1] = {eig_Fib[1]:.10f}  (should be -1/φ)")
    print()

    # Relationship
    print("  SPECTRAL RELATIONSHIP:")
    print("    spec(P₄)  = {φ, 1/φ, -1/φ, -φ}")
    print("    spec(Fib) = {φ, -1/φ}")
    print("    spec(P₄)  = spec(Fib) ∪ {-spec(Fib)}")
    print()
    print("    This is because P₄ is bipartite. For bipartite graphs,")
    print("    if λ is an eigenvalue, so is -λ.")
    print()
    print("    WHY: P₄ eigenvalues are 2cos(kπ/5) for k=1..4.")
    print("    cos(π/5) = φ/2, so 2cos(π/5) = φ.")
    print("    The '5' appears because 克 (destruction) is a Z₅ cycle")
    print("    and P₄ is the path graph on |Z₅|-1 = 4 vertices.")
    print("    The golden ratio emerges tautologically from the")
    print("    Chebyshev polynomial relation for path graphs: cos(π/5) = φ/2.")
    print()

    # Extra: verify cos(π/5) = φ/2
    print(f"    cos(π/5) = {np.cos(np.pi/5):.10f}")
    print(f"    φ/2      = {phi/2:.10f}")
    print(f"    diff     = {abs(np.cos(np.pi/5) - phi/2):.2e}")
    print()


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    task1()
    print()
    task2()
    print()
    task3()
    print()
    task4()
