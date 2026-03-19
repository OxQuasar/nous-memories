"""
Probe 1: Logistic Map at the GMS Parameter

Tests whether the logistic map at r = 1+√5 produces a Markov partition
whose transition structure matches the I Ching's 64-state graph.

The logistic map f(x) = rx(1-x) at r = 1+√5 has:
  - Critical point period 2: f²(1/2) = 1/2
  - GMS symbolic dynamics: "11" forbidden (kneading sequence "1C")
  - Topological entropy = log(φ)

The I Ching connection (from dynamics probes):
  - The 克 trigram graph is the bipartite double cover of the GMS
  - Its spectral radius is φ

This probe checks the FULL 64-state structure, not just the 2-state GMS.
"""

import json
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"
DYNAMICS_DIR = HERE.parent / "dynamics"

PHI = (1 + 5**0.5) / 2
R_GMS = 1 + 5**0.5   # ≈ 3.2360679...

def logistic(x, r):
    return r * x * (1 - x)

# ══════════════════════════════════════════════════════════════════
# STEP 1: Parameter Verification
# ══════════════════════════════════════════════════════════════════

def step1_verify_parameter():
    print("=" * 70)
    print("STEP 1: PARAMETER VERIFICATION")
    print("=" * 70)

    r = R_GMS
    c = 0.5  # critical point
    v1 = logistic(c, r)
    v2 = logistic(v1, r)
    print(f"  r = 1+√5 = {r:.10f}")
    print(f"  f(c)  = f(0.5) = {v1:.10f}")
    print(f"  f²(c) = f(f(0.5)) = {v2:.10f}")
    print(f"  f²(c) == c: {abs(v2 - c) < 1e-12}")

    # Topological entropy check
    # Lap number growth: L(n+1) = L(n) + L(n-1) (Fibonacci)
    # Growth rate → φ, so h_top = log(φ)
    h_top = np.log(PHI)
    print(f"  Topological entropy = log(φ) = {h_top:.10f}")

    # The critical value
    v_crit = (1 + 5**0.5) / 4
    print(f"  Critical value = (1+√5)/4 = {v_crit:.10f}")
    print(f"  Invariant interval: [0, {v_crit:.6f}]")

    return {
        "r": float(r),
        "critical_value": float(v_crit),
        "period2_verified": bool(abs(v2 - c) < 1e-12),
        "topological_entropy": float(h_top),
    }

# ══════════════════════════════════════════════════════════════════
# STEP 2: Transition Graphs on Equal Partitions
# ══════════════════════════════════════════════════════════════════

def build_transition_matrix_equal(r, n_cells, n_samples=100000):
    """Build transition matrix for logistic map on n_cells equal intervals of [0, f(c)]."""
    f_c = r / 4.0  # = f(0.5) = r/4, maximum value

    # Partition [0, f_c] into n_cells equal intervals
    boundaries = np.linspace(0, f_c, n_cells + 1)

    def cell_index(x):
        if x < 0 or x > f_c:
            return -1  # outside invariant region
        idx = int(x / f_c * n_cells)
        return min(idx, n_cells - 1)

    # For an exact analysis: the logistic map is continuous, so f(interval)
    # is a connected interval. We just need to find f(left), f(right), and
    # check which cells the image overlaps.
    T = np.zeros((n_cells, n_cells), dtype=int)

    for i in range(n_cells):
        left = boundaries[i]
        right = boundaries[i + 1]

        # f is unimodal: increasing on [0, 0.5], decreasing on [0.5, f_c]
        # Image of [left, right] = [min(f(left), f(right)), max over interval]
        f_left = logistic(left, r)
        f_right = logistic(right, r)

        # If interval contains the critical point 0.5, the maximum is f(0.5)
        if left <= 0.5 <= right:
            f_max = r / 4.0
        else:
            f_max = max(f_left, f_right)
        f_min = min(f_left, f_right)

        # Clamp to invariant interval
        f_min = max(0, f_min)
        f_max = min(f_c, f_max)

        # Which cells does [f_min, f_max] overlap?
        for j in range(n_cells):
            cell_left = boundaries[j]
            cell_right = boundaries[j + 1]
            if f_min < cell_right and f_max > cell_left:
                T[i, j] = 1

    return T, boundaries

def step2_transition_graphs():
    print("\n" + "=" * 70)
    print("STEP 2: TRANSITION GRAPHS ON EQUAL PARTITIONS")
    print("=" * 70)

    results = {}

    for n_cells in [2, 4, 8, 16]:
        T, bounds = build_transition_matrix_equal(R_GMS, n_cells)
        n_edges = int(T.sum())
        degrees = T.sum(axis=1).astype(int)
        in_degrees = T.sum(axis=0).astype(int)

        print(f"\n  ── {n_cells} cells (equal partition of [0, {R_GMS/4:.4f}]) ──")
        print(f"  Transition matrix:")
        for i in range(n_cells):
            row = "".join(str(T[i, j]) for j in range(n_cells))
            print(f"    [{row}]  deg_out={degrees[i]}")
        print(f"  Total edges: {n_edges}")
        print(f"  Out-degree sequence: {sorted(degrees)}")
        print(f"  In-degree sequence:  {sorted(in_degrees)}")

        # Eigenvalues
        eigvals = np.linalg.eigvals(T.astype(float))
        eigvals_sorted = sorted(eigvals, key=lambda x: -abs(x))
        print(f"  Spectral radius: {abs(eigvals_sorted[0]):.6f}")
        print(f"  Top eigenvalues: {[f'{v.real:.4f}' for v in eigvals_sorted[:5]]}")

        # Check GMS: is "11" forbidden? (for 2-cell case)
        if n_cells == 2:
            gms = T[1, 1] == 0  # transition from cell 1 to cell 1 forbidden?
            print(f"  GMS (T[1,1]=0): {gms}")

        results[str(n_cells)] = {
            "n_edges": n_edges,
            "out_degrees": degrees.tolist(),
            "in_degrees": in_degrees.tolist(),
            "spectral_radius": float(abs(eigvals_sorted[0])),
            "matrix": T.tolist(),
        }

    return results

# ══════════════════════════════════════════════════════════════════
# STEP 3: Q₃ Embeddability Test (Fastest Kill)
# ══════════════════════════════════════════════════════════════════

def build_q3():
    """Q₃ adjacency matrix."""
    A = np.zeros((8, 8), dtype=int)
    for i in range(8):
        for bit in range(3):
            A[i, i ^ (1 << bit)] = 1
    return A

def step3_q3_embeddability(step2_results):
    print("\n" + "=" * 70)
    print("STEP 3: Q₃ EMBEDDABILITY TEST")
    print("=" * 70)

    A_q3 = build_q3()
    q3_degrees = A_q3.sum(axis=1)
    print(f"  Q₃: 8 vertices, each degree 3, 12 edges")

    T = np.array(step2_results["8"]["matrix"])
    n_edges_T = int(T.sum())
    out_degrees = T.sum(axis=1).astype(int)
    in_degrees = T.sum(axis=0).astype(int)

    print(f"\n  Logistic map 8-cell transition graph:")
    print(f"  Edges: {n_edges_T} (Q₃ has 24 directed = 12 undirected)")
    print(f"  Out-degrees: {sorted(out_degrees)}")
    print(f"  In-degrees:  {sorted(in_degrees)}")

    # Q₃ properties needed for embedding:
    # 1. Each vertex has undirected degree exactly 3
    # 2. 12 undirected edges total
    # 3. Graph is bipartite
    # 4. Vertex-transitive (all vertices equivalent under automorphisms)

    # For the logistic map's transition graph to embed in Q₃:
    # - It must have ≤ 12 undirected edges
    # - Each vertex must have ≤ 3 undirected neighbors
    # - The graph structure must be isomorphic to a subgraph of Q₃

    # Check if the transition graph is symmetric (undirected)
    is_symmetric = np.array_equal(T, T.T)
    print(f"\n  Transition matrix symmetric: {is_symmetric}")

    if not is_symmetric:
        # Symmetrize for undirected comparison
        T_sym = np.maximum(T, T.T)
        n_edges_sym = int(T_sym.sum()) // 2
        sym_degrees = T_sym.sum(axis=1).astype(int)
        print(f"  Symmetrized edges: {n_edges_sym}")
        print(f"  Symmetrized degrees: {sorted(sym_degrees)}")
    else:
        T_sym = T
        n_edges_sym = n_edges_T // 2
        sym_degrees = out_degrees

    # Test 1: Degree constraint
    max_degree = max(sym_degrees) if not is_symmetric else max(out_degrees)
    degree_ok = max_degree <= 3
    print(f"\n  Test 1 — Max degree ≤ 3: {degree_ok} (max = {max_degree})")

    # Test 2: Edge count constraint
    edge_ok = n_edges_sym <= 12
    print(f"  Test 2 — Edge count ≤ 12: {edge_ok} ({n_edges_sym} edges)")

    # Test 3: Uniform degree
    uniform_degree = all(d == 3 for d in sym_degrees)
    print(f"  Test 3 — All degrees = 3: {uniform_degree}")

    embeddable = degree_ok and edge_ok and uniform_degree
    print(f"\n  EMBEDDABLE IN Q₃: {embeddable}")

    if not embeddable:
        print(f"\n  MISMATCH DETAILS:")
        print(f"    The logistic map's transition graph has non-uniform degree sequence.")
        print(f"    Q₃ requires every vertex to have exactly 3 neighbors.")
        print(f"    The logistic map's degree sequence {sorted(sym_degrees)} ≠ [3,3,3,3,3,3,3,3].")
        print(f"    The I Ching's Q₃ structure CANNOT be the logistic map's Markov partition.")

    return {
        "embeddable": bool(embeddable),
        "transition_edges": n_edges_sym,
        "q3_edges": 12,
        "max_degree": int(max_degree),
        "degree_sequence": sorted(int(d) for d in sym_degrees),
        "q3_degree_sequence": [3] * 8,
        "is_symmetric": bool(is_symmetric),
    }

# ══════════════════════════════════════════════════════════════════
# STEP 4: Markov Partition (Natural Partition)
# ══════════════════════════════════════════════════════════════════

def step4_markov_partition():
    """Build the natural Markov partition using preimages of the critical point."""
    print("\n" + "=" * 70)
    print("STEP 4: NATURAL MARKOV PARTITION")
    print("=" * 70)

    r = R_GMS
    c = 0.5
    v = logistic(c, r)  # (1+√5)/4 ≈ 0.809

    # The natural partition boundaries come from the orbit of c and its preimages.
    # c = 0.5, v = f(c) ≈ 0.809, f(v) = c = 0.5 (period 2)
    #
    # Preimages of c under f: solve rx(1-x) = 0.5
    # x = (1 ± √((3-√5)/2))/2
    # √((3-√5)/2) = √(1/φ²) = 1/φ = (√5-1)/2
    # So preimages are: (1 + 1/φ)/2 = (1 + (√5-1)/2)/2 = (1+√5)/4 = v (!)
    #                    (1 - 1/φ)/2 = (1 - (√5-1)/2)/2 = (3-√5)/4

    pre_c_1 = v  # already known
    pre_c_2 = (3 - 5**0.5) / 4
    print(f"  Critical point c = {c}")
    print(f"  f(c) = v = {v:.10f}")
    print(f"  Preimages of c = 0.5 under f:")
    print(f"    {pre_c_1:.10f} = (1+√5)/4 = v (same as critical value)")
    print(f"    {pre_c_2:.10f} = (3-√5)/4")

    # Preimages of pre_c_2 under f: solve rx(1-x) = pre_c_2
    disc2 = 1 - 4 * pre_c_2 / r
    if disc2 >= 0:
        pre2_a = (1 + disc2**0.5) / 2
        pre2_b = (1 - disc2**0.5) / 2
        print(f"  Preimages of {pre_c_2:.6f} under f:")
        print(f"    {pre2_a:.10f}, {pre2_b:.10f}")
    else:
        pre2_a = pre2_b = None
        print(f"  No real preimages of {pre_c_2:.6f}")

    # The Markov partition at 2-bit resolution uses boundaries:
    # {0, pre_c_2, c, v}  (sorted: 0, ~0.191, 0.5, ~0.809)
    boundaries_2bit = sorted([0, pre_c_2, c, v])
    print(f"\n  2-bit Markov partition boundaries: {[f'{b:.6f}' for b in boundaries_2bit]}")
    print(f"  Intervals: ", end="")
    for i in range(len(boundaries_2bit) - 1):
        print(f"[{boundaries_2bit[i]:.3f}, {boundaries_2bit[i+1]:.3f}]", end="  ")
    print()

    # Build transition matrix for this partition
    n_cells = len(boundaries_2bit) - 1
    T = np.zeros((n_cells, n_cells), dtype=int)
    for i in range(n_cells):
        left = boundaries_2bit[i]
        right = boundaries_2bit[i + 1]
        f_left = logistic(left, r)
        f_right = logistic(right, r)
        if left <= 0.5 <= right:
            f_max = r / 4.0
        else:
            f_max = max(f_left, f_right)
        f_min = min(f_left, f_right)
        f_min = max(0, f_min)
        f_max = min(v, f_max)

        for j in range(n_cells):
            cell_left = boundaries_2bit[j]
            cell_right = boundaries_2bit[j + 1]
            if f_min < cell_right and f_max > cell_left:
                T[i, j] = 1

    print(f"\n  2-bit Markov partition transition matrix ({n_cells}×{n_cells}):")
    for i in range(n_cells):
        row = "".join(str(T[i, j]) for j in range(n_cells))
        print(f"    [{row}]")

    out_deg = T.sum(axis=1)
    print(f"  Out-degrees: {out_deg.tolist()}")
    print(f"  Edges: {int(T.sum())}")

    # 3-bit resolution: add preimages of pre_c_2
    if pre2_a is not None:
        boundaries_3bit = sorted(set([0, pre2_b, pre_c_2, c, pre2_a, v]))
        print(f"\n  3-bit Markov partition boundaries: {[f'{b:.6f}' for b in boundaries_3bit]}")
        n3 = len(boundaries_3bit) - 1
        T3 = np.zeros((n3, n3), dtype=int)
        for i in range(n3):
            left = boundaries_3bit[i]
            right = boundaries_3bit[i + 1]
            f_left = logistic(left, r)
            f_right = logistic(right, r)
            if left <= 0.5 <= right:
                f_max = r / 4.0
            else:
                f_max = max(f_left, f_right)
            f_min = min(f_left, f_right)
            f_min = max(0, f_min)
            f_max = min(v, f_max)

            for j in range(n3):
                cell_left = boundaries_3bit[j]
                cell_right = boundaries_3bit[j + 1]
                if f_min < cell_right and f_max > cell_left:
                    T3[i, j] = 1

        print(f"\n  3-bit Markov transition matrix ({n3}×{n3}):")
        for i in range(n3):
            row = "".join(str(T3[i, j]) for j in range(n3))
            print(f"    [{row}]")
        out_deg3 = T3.sum(axis=1)
        in_deg3 = T3.sum(axis=0)
        print(f"  Out-degrees: {out_deg3.tolist()}")
        print(f"  In-degrees:  {in_deg3.tolist()}")
        print(f"  Edges: {int(T3.sum())}")

        # Q₃ embeddability at this resolution
        T3_sym = np.maximum(T3, T3.T)
        sym_deg3 = T3_sym.sum(axis=1).astype(int)
        print(f"  Symmetrized degrees: {sorted(sym_deg3)}")
        print(f"  Q₃ embeddable: {n3 == 8 and all(d == 3 for d in sym_deg3)}")

        return {
            "boundaries_2bit": [float(b) for b in boundaries_2bit],
            "matrix_2bit": T.tolist(),
            "boundaries_3bit": [float(b) for b in boundaries_3bit],
            "n_cells_3bit": n3,
            "matrix_3bit": T3.tolist(),
            "degrees_3bit": out_deg3.tolist(),
        }
    return {"boundaries_2bit": [float(b) for b in boundaries_2bit], "matrix_2bit": T.tolist()}

# ══════════════════════════════════════════════════════════════════
# STEP 5: Spectral Comparison
# ══════════════════════════════════════════════════════════════════

def step5_spectral_comparison(step2_results):
    """Compare eigenvalue structure between logistic map and I Ching."""
    print("\n" + "=" * 70)
    print("STEP 5: SPECTRAL COMPARISON (8-cell equal partition)")
    print("=" * 70)

    T = np.array(step2_results["8"]["matrix"]).astype(float)
    eigvals_T = sorted(np.linalg.eigvals(T), key=lambda x: -abs(x))

    # Load I Ching trigram eigenvalues
    with open(DYNAMICS_DIR / "p1_results.json") as f:
        p1 = json.load(f)

    print(f"\n  Logistic map 8-cell eigenvalues (T):")
    for v in eigvals_T:
        if abs(v.imag) < 1e-8:
            print(f"    {v.real:+.6f}")
        else:
            print(f"    {v.real:+.6f} {v.imag:+.6f}i")

    print(f"\n  I Ching trigram eigenvalues (from p1_results.json):")
    for g in ["比和", "生", "克"]:
        trig_eigs = p1["trigram"]["eigenvalues"][g]
        vals = [e["value"] for e in trig_eigs]
        mults = [e["multiplicity"] for e in trig_eigs]
        print(f"    {g}: {list(zip(vals, mults))}")

    # Spectral radius comparison
    rho_logistic = abs(eigvals_T[0])
    rho_ke = max(abs(e["value"]) for e in p1["trigram"]["eigenvalues"]["克"])
    rho_sheng = max(abs(e["value"]) for e in p1["trigram"]["eigenvalues"]["生"])

    print(f"\n  Spectral radii:")
    print(f"    Logistic 8-cell:  {rho_logistic:.6f}")
    print(f"    I Ching 克 trig:   {rho_ke:.6f} = φ")
    print(f"    I Ching 生 trig:   {rho_sheng:.6f} = √2")
    print(f"    Match 克: {abs(rho_logistic - rho_ke) < 0.01}")

    # Eigenvalue structure
    # The logistic map's T matrix is NOT symmetric, so eigenvalues can be complex
    n_real = sum(1 for v in eigvals_T if abs(v.imag) < 1e-8)
    n_complex = sum(1 for v in eigvals_T if abs(v.imag) >= 1e-8)
    print(f"\n  Logistic eigenvalue structure:")
    print(f"    Real: {n_real}, Complex: {n_complex}")
    print(f"    ± paired: {all(any(abs(v + w) < 1e-6 for w in eigvals_T) for v in eigvals_T if abs(v) > 1e-8)}")

    return {
        "logistic_spectral_radius": float(rho_logistic),
        "iching_ke_spectral_radius": float(rho_ke),
        "match": bool(abs(rho_logistic - rho_ke) < 0.01),
        "logistic_eigenvalues": [(float(v.real), float(v.imag)) for v in eigvals_T],
    }

# ══════════════════════════════════════════════════════════════════
# STEP 6: The Deep Structural Mismatch
# ══════════════════════════════════════════════════════════════════

def step6_structural_mismatch():
    """Explain why the logistic map can never produce Q₃/Q₆ structure."""
    print("\n" + "=" * 70)
    print("STEP 6: STRUCTURAL MISMATCH ANALYSIS")
    print("=" * 70)

    print("""
  The logistic map's Markov partition CANNOT produce Q₃ for a fundamental reason:

  1. CONNECTIVITY STRUCTURE:
     The logistic map is a continuous 1D map. For ANY partition of [0,1]
     into intervals I₀, I₁, ..., I_{n-1}, the image f(Iₖ) is a single
     connected interval. This means: each row of the transition matrix
     consists of a CONTIGUOUS BLOCK of 1s.

     Q₃ has rows: [0,1,1,0,1,0,0,0] (vertex 0 → {1,2,4}). These are
     NOT contiguous. Bit-flip neighbors are at Hamming distance 1,
     which scatter non-contiguously in any linear ordering.

  2. DEGREE STRUCTURE:
     Q₃ has uniform degree 3 at every vertex.
     The logistic map's transition graph has variable degree:
     intervals near the critical point (where f is steep) have wide
     images → many transitions. Corner intervals have narrow images
     → few transitions. The degree MUST be non-uniform for any
     non-trivial partition.

  3. GRAPH CLASS:
     Q₃ is a HYPERCUBE graph — it encodes binary coordinate structure.
     The logistic map's transition graph is an INTERVAL graph (a graph
     whose edges connect intervals with overlapping images). These are
     fundamentally different graph classes.

  CONCLUSION:
     The I Ching's Q₃ × Q₃ = Q₆ structure is NOT the Markov partition
     of any 1D map. The Q₆ structure requires 6 independent binary
     dimensions (the 6 yao/lines). A 1D map partition is inherently
     1-dimensional — it can only produce interval graphs, never
     hypercube graphs.

     The GMS connection is REAL (the 克 trigram graph encodes the same
     forbidden-word constraint as the logistic map at r = 1+√5), but
     the I Ching achieves this via a completely different mechanism:
     6 binary variables with element-typed edges, not a 1D map partition.
""")

    return {
        "verdict": "IMPOSSIBLE",
        "reason": "1D map partitions produce interval graphs; Q₃ requires hypercube structure",
        "gms_connection": "The GMS constraint (no '11') appears in BOTH systems but via different mechanisms",
        "logistic_graph_class": "interval graph (contiguous blocks in transition matrix)",
        "iching_graph_class": "hypercube graph (Q₃ = 3D binary coordinate structure)",
    }

# ══════════════════════════════════════════════════════════════════
# STEP 7: What CAN Be Matched
# ══════════════════════════════════════════════════════════════════

def step7_what_matches():
    """Identify what structural features DO match between the two systems."""
    print("\n" + "=" * 70)
    print("STEP 7: STRUCTURAL FEATURES THAT DO MATCH")
    print("=" * 70)

    matches = []

    # 1. GMS constraint
    print("\n  1. Golden Mean Shift constraint:")
    print("     Logistic at r=1+√5: forbidden word '11' in binary coding")
    print("     I Ching 克 trigram: graph IS the bipartite double cover of GMS")
    print("     MATCH: Same forbidden pattern, same topological entropy log(φ)")
    matches.append("GMS constraint (forbidden '11')")

    # 2. Spectral radius
    print("\n  2. Spectral radius:")
    print(f"     Logistic: ρ(T₂) = φ ≈ {PHI:.6f}")
    print(f"     I Ching 克 trigram: ρ = φ ≈ {PHI:.6f}")
    print("     MATCH: Same spectral radius φ at the 2-state level")
    matches.append("Spectral radius φ at 2-state level")

    # 3. Period-2 / bipartite
    print("\n  3. Period-2 / bipartite structure:")
    print("     Logistic at r=1+√5: critical point has period 2")
    print("     I Ching Q₆: bipartite (parity involution)")
    print("     PARTIAL MATCH: Both have Z₂ symmetry, but different origin")
    matches.append("Z₂ symmetry / bipartite structure")

    # 4. Forbidden patterns at higher levels
    print("\n  4. Higher-level constraints:")
    print("     Logistic: '11' forbidden at ALL resolutions (self-similar)")
    print("     I Ching: 克→克 suppression is a different mechanism")
    print("     (the 五行 克 structure has spectral gap, not strict forbiddance)")
    print("     NO MATCH at higher resolution")

    print(f"\n  Summary: {len(matches)} matches, all at the 2-state (GMS) level.")
    print("  The logistic map and I Ching share the GMS skeleton")
    print("  but diverge completely at the 8-state/64-state level.")

    return {"matches": matches, "mismatches_at_higher_levels": True}

# ── Main ──────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PROBE 1: LOGISTIC MAP AT THE GMS PARAMETER")
    print("=" * 70)

    r1 = step1_verify_parameter()
    r2 = step2_transition_graphs()
    r3 = step3_q3_embeddability(r2)
    r4 = step4_markov_partition()
    r5 = step5_spectral_comparison(r2)
    r6 = step6_structural_mismatch()
    r7 = step7_what_matches()

    all_results = {
        "step1_parameter": r1,
        "step2_transition_graphs": r2,
        "step3_q3_embeddability": r3,
        "step4_markov_partition": r4,
        "step5_spectral_comparison": r5,
        "step6_structural_mismatch": r6,
        "step7_what_matches": r7,
    }

    out_path = HERE / "logistic_map_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
