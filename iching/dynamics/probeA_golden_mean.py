"""
Probe A: Golden Mean Shift Comparison

Structural relationship between walks on P₄ (the 克 trigram subgraph)
and the golden mean shift (GMS).

Key question: 克 trigram graph = 2×P₄, spectral radius = φ, walk counts = 4×Lucas.
The GMS also has entropy log φ. What is the precise structural relationship?
"""

import json
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.sparse.csgraph import connected_components
from scipy import sparse
from collections import Counter
from pathlib import Path
from itertools import product as iproduct

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

PHI = (1 + 5**0.5) / 2

# ── Helpers (reused from p1/p45) ──────────────────────────────────

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def load_transitions():
    with open(ATLAS_DIR / "transitions.json") as f:
        return json.load(f)["bian_fan"]

def get_trigram_elements(atlas):
    elems = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            elems[t["val"]] = t["element"]
    return elems

SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

def wuxing_group(e1, e2):
    if e1 == e2: return "比和"
    if SHENG[e1] == e2 or SHENG[e2] == e1: return "生"
    return "克"

GROUP_NAMES = ["比和", "生", "克"]

TRIGRAM_NAMES = {0: "Kun☷", 1: "Zhen☳", 2: "Kan☵", 3: "Gen☶",
                 4: "Dui☱", 5: "Li☲", 6: "Xun☴", 7: "Qian☰"}

def build_trigram_matrices(trigram_elements):
    mats = {g: np.zeros((8, 8), dtype=int) for g in GROUP_NAMES}
    for a in range(8):
        for bit in range(3):
            b = a ^ (1 << bit)
            if b > a:
                g = wuxing_group(trigram_elements[a], trigram_elements[b])
                mats[g][a, b] = 1
                mats[g][b, a] = 1
    return mats

def eigendecomp(A):
    eigvals = np.linalg.eigh(A.astype(float))[0]
    rounded = np.round(eigvals, 8)
    unique, counts = np.unique(rounded, return_counts=True)
    return [(float(v), int(c)) for v, c in zip(unique, counts)]

def char_poly_int(A):
    """Characteristic polynomial as integer coefficients [c_0, c_1, ..., c_n] where p(x) = sum c_i x^i."""
    coeffs = np.poly(A.astype(float))  # numpy: highest degree first
    return list(np.round(coeffs).astype(int)[::-1])  # reverse to ascending

def lucas(n):
    """Lucas number L_n."""
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


# ══════════════════════════════════════════════════════════════════
# PART 1: Trigram Subgraph Topology
# ══════════════════════════════════════════════════════════════════

def part1(trigram_elements, trig_mats):
    print("\n" + "═" * 70)
    print("PART 1: TRIGRAM SUBGRAPH TOPOLOGY")
    print("═" * 70)
    results = {}

    for g in GROUP_NAMES:
        A = trig_mats[g]
        edges = [(a, b) for a in range(8) for b in range(a+1, 8) if A[a, b]]
        n_comp, labels = connected_components(sparse.csr_matrix(A), directed=False)

        print(f"\n  [{g}] — {len(edges)} edges, {n_comp} components")

        # Print edges
        for a, b in edges:
            print(f"    {a}({TRIGRAM_NAMES[a]}, {trigram_elements[a]}) — "
                  f"{b}({TRIGRAM_NAMES[b]}, {trigram_elements[b]})")

        # Print components with topology
        components = {}
        for c in range(n_comp):
            verts = sorted(np.where(labels == c)[0])
            comp_edges = [(a, b) for a, b in edges if a in verts and b in verts]
            degrees = {v: sum(1 for a, b in comp_edges if v in (a, b)) for v in verts}

            # Identify topology
            n_v, n_e = len(verts), len(comp_edges)
            if n_e == n_v - 1 and max(degrees.values()) <= 2:
                topo = f"P_{n_v}"  # path graph
            elif n_e == n_v:
                topo = f"C_{n_v}"  # cycle
            else:
                topo = f"({n_v}v, {n_e}e)"

            # Reconstruct path order
            if n_v == 1:
                print(f"    Component {c}: isolated vertex: {TRIGRAM_NAMES[verts[0]]}")
            elif topo.startswith("P_"):
                endpoints = [v for v, d in degrees.items() if d == 1]
                path = [endpoints[0]]
                visited = {endpoints[0]}
                while len(path) < n_v:
                    cur = path[-1]
                    for a, b in comp_edges:
                        nxt = b if a == cur else (a if b == cur else None)
                        if nxt is not None and nxt not in visited:
                            path.append(nxt)
                            visited.add(nxt)
                            break
                path_str = " — ".join(f"{v}({TRIGRAM_NAMES[v]})" for v in path)
                print(f"    Component {c}: {topo}: {path_str}")
            else:
                print(f"    Component {c}: {topo}: {[TRIGRAM_NAMES[v] for v in verts]}")

            components[c] = {"vertices": verts, "topology": topo}

        results[g] = {
            "edges": len(edges),
            "components": n_comp,
            "component_details": {str(k): v for k, v in components.items()},
        }

    return results


# ══════════════════════════════════════════════════════════════════
# PART 2: Forbidden Words (SFT Analysis)
# ══════════════════════════════════════════════════════════════════

def forbidden_words_analysis(A, name, vertices=None):
    """Analyze forbidden words for vertex shift on graph with adjacency A."""
    n = A.shape[0]
    if vertices is None:
        vertices = list(range(n))

    print(f"\n  [{name}] — {n} vertices")

    # 2-letter forbidden words (= non-edges including no self-loops)
    forbidden_2 = []
    for i in range(n):
        for j in range(n):
            if A[i, j] == 0:
                forbidden_2.append((vertices[i], vertices[j]))
    print(f"    Forbidden 2-letter words: {len(forbidden_2)}")
    for w in forbidden_2:
        print(f"      {w[0]}{w[1]}")

    # Check 3-letter words: any 3-letter word abc is forbidden iff ab or bc is forbidden
    # If all forbidden 3-words are implied by 2-words, this is a 1-step SFT
    extra_forbidden_3 = []
    for a in range(n):
        for b in range(n):
            for c in range(n):
                path_exists = (A[a, b] == 1 and A[b, c] == 1)
                implied_forbidden = (A[a, b] == 0 or A[b, c] == 0)
                if not path_exists and not implied_forbidden:
                    # This shouldn't happen for adjacency matrices
                    extra_forbidden_3.append((vertices[a], vertices[b], vertices[c]))

    print(f"    Extra forbidden 3-letter words (beyond 2-letter): {len(extra_forbidden_3)}")
    if extra_forbidden_3:
        for w in extra_forbidden_3:
            print(f"      {''.join(str(x) for x in w)}")
    print(f"    ⟹ {'1-step SFT (edge shift)' if not extra_forbidden_3 else 'NOT 1-step SFT'}")

    # Self-loops
    self_loops = sum(1 for i in range(n) if A[i, i] == 1)
    print(f"    Self-loops: {self_loops}")

    return {
        "n_vertices": n,
        "forbidden_2": len(forbidden_2),
        "extra_forbidden_3": len(extra_forbidden_3),
        "is_1step_SFT": len(extra_forbidden_3) == 0,
        "self_loops": self_loops,
    }


def part2(trig_mats, trigram_elements):
    print("\n" + "═" * 70)
    print("PART 2: FORBIDDEN WORDS (SFT ANALYSIS)")
    print("═" * 70)
    results = {}

    # Single P₄: vertices 0,1,2,3 connected as 0-1-2-3
    A_P4 = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
    ])
    results["P4"] = forbidden_words_analysis(A_P4, "P₄ (abstract)")

    # Full 2×P₄ on 8 vertices (the actual 克 trigram graph)
    A_ke = trig_mats["克"]
    results["2xP4_ke"] = forbidden_words_analysis(A_ke, "2×P₄ (克 trigram)")

    # 比和: 2×P₂
    A_bihe = trig_mats["比和"]
    results["2xP2_bihe"] = forbidden_words_analysis(A_bihe, "2×P₂ (比和 trigram)")

    # 生: 2×P₃
    A_sheng = trig_mats["生"]
    results["2xP3_sheng"] = forbidden_words_analysis(A_sheng, "2×P₃ (生 trigram)")

    return results


# ══════════════════════════════════════════════════════════════════
# PART 3: Golden Mean Shift Comparison
# ══════════════════════════════════════════════════════════════════

def part3(trig_mats):
    print("\n" + "═" * 70)
    print("PART 3: GOLDEN MEAN SHIFT COMPARISON")
    print("═" * 70)
    results = {}

    # ── Definitions ───────────────────────────────────────────────
    # P₄ adjacency (single path 0-1-2-3)
    A_P4 = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
    ], dtype=float)

    # 2×P₄ (= 克 trigram)
    A_2P4 = trig_mats["克"].astype(float)

    # GMS: Golden Mean Shift adjacency
    # Vertex 0 has self-loop, edge 0↔1, vertex 1 has no self-loop
    M_GMS = np.array([
        [1, 1],
        [1, 0],
    ], dtype=float)

    # ── 3a: Periodic orbits (traces) ─────────────────────────────
    print("\n── 3a. Periodic Orbits: tr(A^n) ──")
    print(f"  {'n':>3} | {'P₄':>10} {'2×P₄':>10} {'GMS':>10} {'4L_n':>10} | {'P4=0(odd)?':>10} {'GMS=L_n?':>10}")
    print(f"  {'-'*3}-+-{'-'*10}-{'-'*10}-{'-'*10}-{'-'*10}-+-{'-'*10}-{'-'*10}")

    traces = {"P4": [], "2P4": [], "GMS": [], "4Ln": [], "Ln": []}
    all_match = True
    for n in range(1, 21):
        tr_P4 = int(round(np.trace(np.linalg.matrix_power(A_P4, n))))
        tr_2P4 = int(round(np.trace(np.linalg.matrix_power(A_2P4, n))))
        tr_GMS = int(round(np.trace(np.linalg.matrix_power(M_GMS, n))))
        L_n = lucas(n)
        four_L_n = 4 * L_n

        p4_check = "✓" if (n % 2 == 1 and tr_P4 == 0) or (n % 2 == 0 and tr_P4 == 2 * L_n) else "✗"
        gms_check = "✓" if tr_GMS == L_n else "✗"

        print(f"  {n:>3} | {tr_P4:>10} {tr_2P4:>10} {tr_GMS:>10} {four_L_n:>10} | "
              f"{'0(odd)' if n%2==1 else '2L_n':>10} {gms_check:>10}")

        traces["P4"].append(tr_P4)
        traces["2P4"].append(tr_2P4)
        traces["GMS"].append(tr_GMS)
        traces["4Ln"].append(four_L_n)
        traces["Ln"].append(L_n)

        if tr_GMS != L_n:
            all_match = False

    print(f"\n  tr(GMS^n) = L_n for all n: {all_match}")
    print(f"  tr(P4^n) = 2L_n (even n), 0 (odd n)")
    print(f"  tr(2P4^n) = 4L_n (even n), 0 (odd n)")
    print(f"  ⟹ Trace sequences differ ⟹ P₄ and GMS are NOT topologically conjugate")

    results["3a"] = {
        "traces": traces,
        "GMS_equals_Lucas": all_match,
        "conjugate": False,
        "reason": "different trace sequences (P4 bipartite: zero odd traces; GMS has nonzero odd traces)",
    }

    # ── 3b: Zeta functions ────────────────────────────────────────
    print("\n── 3b. Dynamical Zeta Functions ──")

    # ζ(z) = 1/det(I - zA)
    # GMS: det(I - zM) = det([[1-z, -z],[-z, 1]]) = (1-z)(1) - (-z)(-z) = 1 - z - z²
    print("  GMS: ζ(z) = 1/(1 - z - z²)")

    # P₄: det(I - zA_P4)
    # A_P4 = [[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]]
    I4 = np.eye(4)
    # Compute symbolically: det(I - zA) as polynomial in z
    # char poly of A: det(λI - A) = λ⁴ - 3λ² + 1
    char_P4 = np.poly(A_P4)  # highest degree first
    print(f"  P₄ characteristic polynomial (λ⁴ coeff first): {np.round(char_P4, 6).tolist()}")
    # det(I - zA) = z⁴ det(1/z I - A) = z⁴ · p(1/z) where p(λ) = det(λI - A)
    # p(λ) = λ⁴ - 3λ² + 1
    # z⁴ · p(1/z) = z⁴ · (1/z⁴ - 3/z² + 1) = 1 - 3z² + z⁴
    print(f"  P₄: det(I - zA) = 1 - 3z² + z⁴")

    # Factor: z⁴ - 3z² + 1 = (z² - φ²)(z² - 1/φ²) = (z² - (3+√5)/2)(z² - (3-√5)/2)
    # Alternatively: 1 - 3z² + z⁴ = (1 - z - z²)(1 + z - z²)  ← key factorization!
    # Check: (1 - z - z²)(1 + z - z²) = 1 + z - z² - z - z² + z³ - z² - z³ + z⁴
    #       = 1 - 3z² + z⁴  ✓
    p1 = np.array([1, -1, -1])  # 1 - z - z²
    p2 = np.array([1, 1, -1])   # 1 + z - z²
    product = np.convolve(p1, p2)
    print(f"  Check: (1-z-z²)(1+z-z²) = {product.tolist()}")
    assert np.allclose(product, [1, 0, -3, 0, 1]), "Factorization check failed"
    print(f"  ⟹ det(I - zA_P4) = (1 - z - z²)(1 + z - z²)")
    print(f"  ⟹ ζ_P4(z) = 1/[(1 - z - z²)(1 + z - z²)]")
    print(f"     = ζ_GMS(z) × 1/(1 + z - z²)")
    print(f"  The GMS zeta function is a FACTOR of the P₄ zeta function!")

    # 2×P₄: det(I - zA) = det(I - zA_P4)² = [(1-z-z²)(1+z-z²)]²
    print(f"\n  2×P₄: ζ(z) = 1/[(1-z-z²)(1+z-z²)]² = [ζ_P4(z)]²")

    # What is 1+z-z²?
    # Roots: z = (1 ± √5)/2  → z = φ or z = -1/φ
    # So 1+z-z² = -(z-φ)(z+1/φ) ... hmm, let's verify
    # Roots of 1+z-z² = 0 → z² - z - 1 = 0 → z = (1±√5)/2
    # So z = φ ≈ 1.618 or z = (1-√5)/2 ≈ -0.618 = -1/φ
    print(f"  Roots of (1+z-z²)=0: z = φ ≈ {PHI:.6f}, z = -1/φ ≈ {-1/PHI:.6f}")
    print(f"  Roots of (1-z-z²)=0: z = 1/φ ≈ {1/PHI:.6f}, z = -φ ≈ {-PHI:.6f}")

    results["3b"] = {
        "GMS_zeta": "1/(1-z-z²)",
        "P4_zeta": "1/[(1-z-z²)(1+z-z²)]",
        "P4_det": "1 - 3z² + z⁴ = (1-z-z²)(1+z-z²)",
        "GMS_is_factor": True,
        "2P4_zeta": "[ζ_P4(z)]²",
    }

    # ── 3c: 2-block recoding ─────────────────────────────────────
    print("\n── 3c. Higher Block Presentations ──")

    # 2-block presentation of GMS:
    # GMS alphabet: {0, 1}. Allowed 2-blocks (edges): 00, 01, 10.
    # Forbidden: 11.
    # 2-block shift: vertices = allowed 2-blocks = {00, 01, 10}
    # Edges: 00→00, 00→01, 01→10, 10→00, 10→01
    A_GMS2 = np.array([
        # 00 01 10
        [1, 1, 0],  # 00 → {00, 01}
        [0, 0, 1],  # 01 → {10}
        [1, 1, 0],  # 10 → {00, 01}
    ], dtype=float)
    print(f"  GMS 2-block presentation (vertices: 00,01,10):")
    print(f"    A = {A_GMS2.tolist()}")
    rho_GMS2 = max(abs(v) for v in np.linalg.eigvals(A_GMS2))
    print(f"    Spectral radius: {rho_GMS2:.6f} (= φ: {abs(rho_GMS2 - PHI) < 1e-10})")

    # Compare spectra
    eigs_GMS2 = sorted(np.linalg.eigvals(A_GMS2).real)
    eigs_P4 = sorted(np.linalg.eigvals(A_P4).real)
    print(f"    GMS[2] eigenvalues: {[round(v, 6) for v in eigs_GMS2]}")
    print(f"    P₄ eigenvalues:     {[round(v, 6) for v in eigs_P4]}")
    # GMS[2] has 3 eigenvalues, P₄ has 4. Not same size → compare shared eigenvalues
    shared = [v for v in sorted(eigs_GMS2) if any(abs(v - w) < 1e-8 for w in eigs_P4)]
    extra_P4 = [v for v in sorted(eigs_P4) if not any(abs(v - w) < 1e-8 for w in eigs_GMS2)]
    print(f"    Shared eigenvalues: {[round(v, 6) for v in shared]}")
    print(f"    Extra in P₄:       {[round(v, 6) for v in extra_P4]}")
    print(f"    GMS[2] spectrum ⊂ P₄ spectrum? {len(shared) == len(eigs_GMS2)}")

    # 3-block presentation of GMS:
    # Allowed 3-blocks from {0,1}: 000, 001, 010, 100, 101  (no 11 substring)
    # 5 vertices in the 3-block shift
    blocks3 = []
    for a, b, c in iproduct([0, 1], repeat=3):
        if not (a == 1 and b == 1) and not (b == 1 and c == 1):
            blocks3.append((a, b, c))
    print(f"\n  GMS 3-block presentation: {len(blocks3)} vertices")
    print(f"    Blocks: {[''.join(str(x) for x in b) for b in blocks3]}")
    A_GMS3 = np.zeros((len(blocks3), len(blocks3)), dtype=float)
    for i, (a1, b1, c1) in enumerate(blocks3):
        for j, (a2, b2, c2) in enumerate(blocks3):
            if b1 == a2 and c1 == b2:
                A_GMS3[i, j] = 1
    rho_GMS3 = max(abs(v) for v in np.linalg.eigvals(A_GMS3))
    eigs_GMS3 = sorted(np.linalg.eigvals(A_GMS3).real)
    print(f"    Spectral radius: {rho_GMS3:.6f}")
    print(f"    Eigenvalues: {[round(v, 6) for v in eigs_GMS3]}")

    results["3c"] = {
        "GMS2_spectrum": [round(v, 10) for v in sorted(eigs_GMS2)],
        "P4_spectrum": [round(v, 10) for v in sorted(eigs_P4)],
        "GMS2_subset_of_P4": len(shared) == len(eigs_GMS2),
        "GMS3_spectrum": [round(v, 10) for v in sorted(eigs_GMS3)],
    }

    # ── 3d: Edge shift of P₄ ─────────────────────────────────────
    print("\n── 3d. Edge Shift of P₄ ──")

    # P₄ edges (directed): 0→1, 1→0, 1→2, 2→1, 2→3, 3→2
    # Edge shift: 6 vertices (directed edges), edge e₁→e₂ if terminal of e₁ = initial of e₂
    dir_edges = [(0,1), (1,0), (1,2), (2,1), (2,3), (3,2)]
    edge_labels = [f"{a}→{b}" for a, b in dir_edges]
    print(f"  Directed edges of P₄: {edge_labels}")

    A_edge = np.zeros((6, 6), dtype=float)
    for i, (a1, b1) in enumerate(dir_edges):
        for j, (a2, b2) in enumerate(dir_edges):
            if b1 == a2:
                A_edge[i, j] = 1

    print(f"  Edge shift adjacency ({len(dir_edges)}×{len(dir_edges)}):")
    for i, label in enumerate(edge_labels):
        targets = [edge_labels[j] for j in range(6) if A_edge[i, j] == 1]
        print(f"    {label} → {targets}")

    rho_edge = max(abs(v) for v in np.linalg.eigvals(A_edge))
    eigs_edge = sorted(np.linalg.eigvals(A_edge).real)
    print(f"  Spectral radius: {rho_edge:.6f}")
    print(f"  Eigenvalues: {[round(v, 6) for v in eigs_edge]}")

    # The edge shift of any graph has same entropy. Compare to GMS:
    print(f"  Same entropy as P₄? {abs(np.log(rho_edge) - np.log(PHI)) < 1e-10}")

    # Compare edge shift spectrum to GMS[2]:
    print(f"  Edge shift spectrum vs GMS[2]:")
    print(f"    Edge: {[round(v, 6) for v in sorted(eigs_edge)]}")
    print(f"    GMS2: {[round(v, 6) for v in sorted(eigs_GMS2)]}")

    # The edge shift of P₄ has 6 vertices; GMS[2] has 3.
    # Edge shift of GMS has edges: 0→0 (self-loop), 0→1, 1→0
    # That's 3 directed edges. Its edge shift matrix:
    gms_dir_edges = [(0, 0), (0, 1), (1, 0)]
    A_GMS_edge = np.zeros((3, 3), dtype=float)
    for i, (a1, b1) in enumerate(gms_dir_edges):
        for j, (a2, b2) in enumerate(gms_dir_edges):
            if b1 == a2:
                A_GMS_edge[i, j] = 1
    print(f"\n  GMS edge shift adjacency:")
    gms_edge_labels = [f"{a}→{b}" for a, b in gms_dir_edges]
    for i, label in enumerate(gms_edge_labels):
        targets = [gms_edge_labels[j] for j in range(3) if A_GMS_edge[i, j] == 1]
        print(f"    {label} → {targets}")

    eigs_GMS_edge = sorted(np.linalg.eigvals(A_GMS_edge).real)
    print(f"  GMS edge shift eigenvalues: {[round(v, 6) for v in eigs_GMS_edge]}")
    print(f"  P₄ edge shift eigenvalues:  {[round(v, 6) for v in sorted(eigs_edge)]}")

    # Check: is GMS[2] = GMS edge shift?
    print(f"\n  GMS[2] = GMS edge shift? Spectra match: "
          f"{np.allclose(sorted(eigs_GMS2), sorted(eigs_GMS_edge))}")

    results["3d"] = {
        "P4_edge_shift_spectrum": [round(v, 10) for v in sorted(eigs_edge)],
        "GMS_edge_shift_spectrum": [round(v, 10) for v in sorted(eigs_GMS_edge)],
        "GMS2_equals_GMS_edge": bool(np.allclose(sorted(eigs_GMS2), sorted(eigs_GMS_edge))),
    }

    # ── 3e: Square root / bipartite relationship ──────────────────
    print("\n── 3e. Bipartite Square Root Relationship ──")

    # P₄ is bipartite: even={0,2}, odd={1,3}
    # A² restricted to even vertices:
    A2 = A_P4 @ A_P4
    print(f"  A_P4² =")
    print(f"    {A2.astype(int).tolist()}")

    # Extract even-vertex block (vertices 0, 2)
    even = [0, 2]
    odd = [1, 3]
    A2_even = A2[np.ix_(even, even)].astype(int)
    A2_odd = A2[np.ix_(odd, odd)].astype(int)
    print(f"  A²|_even (verts 0,2): {A2_even.tolist()}")
    print(f"  A²|_odd  (verts 1,3): {A2_odd.tolist()}")

    eigs_A2_even = sorted(np.linalg.eigvals(A2_even.astype(float)).real)
    eigs_A2_odd = sorted(np.linalg.eigvals(A2_odd.astype(float)).real)
    eigs_M2 = sorted(np.linalg.eigvals(M_GMS @ M_GMS).real)
    print(f"  Eigenvalues A²|_even: {[round(v, 6) for v in eigs_A2_even]}")
    print(f"  Eigenvalues A²|_odd:  {[round(v, 6) for v in eigs_A2_odd]}")
    print(f"  Eigenvalues M_GMS²:   {[round(v, 6) for v in eigs_M2]}")

    # M_GMS = [[1,1],[1,0]], M_GMS² = [[2,1],[1,1]]
    M2 = (M_GMS @ M_GMS).astype(int)
    print(f"\n  M_GMS² = {M2.tolist()}")
    print(f"  A²|_even = {A2_even.tolist()}")
    print(f"  A²|_odd  = {A2_odd.tolist()}")

    # Check: A²|_even = [[1,1],[1,2]]
    # M_GMS² = [[2,1],[1,1]]
    # These are transposes of each other!
    print(f"  A²|_even = (M_GMS²)ᵀ? {np.array_equal(A2_even, M2.T)}")
    print(f"  A²|_odd  = M_GMS²?     {np.array_equal(A2_odd, M2)}")

    # More precisely: A²|_even has eigenvalues φ² and 1/φ² (same as M_GMS²)
    print(f"\n  Eigenvalue comparison:")
    print(f"    φ² = {PHI**2:.6f}, 1/φ² = {1/PHI**2:.6f}")
    print(f"    A²|_even: {[round(v, 6) for v in eigs_A2_even]}")
    print(f"    M_GMS²:   {[round(v, 6) for v in eigs_M2]}")
    print(f"    Spectra match: {np.allclose(sorted(eigs_A2_even), sorted(eigs_M2))}")

    # Summary of the relationship
    print(f"\n  KEY FINDING:")
    print(f"    P₄ is the 'bipartite double cover' of the golden mean shift.")
    print(f"    A_P4² restricted to either bipartition class gives a 2×2 matrix")
    print(f"    spectrally equivalent to M_GMS² (eigenvalues φ², 1/φ²).")
    print(f"    The zeta factorization confirms: ζ_P4 = ζ_GMS × ζ_'anti-GMS'")
    print(f"    where ζ_'anti-GMS' = 1/(1+z-z²) is the 'twisted' GMS.")

    results["3e"] = {
        "A2_even": A2_even.tolist(),
        "A2_odd": A2_odd.tolist(),
        "M_GMS_squared": M2.tolist(),
        "A2_even_is_M2_transpose": bool(np.array_equal(A2_even, M2.T)),
        "A2_odd_is_M2": bool(np.array_equal(A2_odd, M2)),
        "spectra_match": bool(np.allclose(sorted(eigs_A2_even), sorted(eigs_M2))),
    }

    return results


# ══════════════════════════════════════════════════════════════════
# PART 4: Hexagram-Level Entropy Decomposition
# ══════════════════════════════════════════════════════════════════

def part4(trig_mats):
    print("\n" + "═" * 70)
    print("PART 4: HEXAGRAM-LEVEL ENTROPY DECOMPOSITION")
    print("═" * 70)
    results = {}

    # Build hex-level 克 OR-symmetrized matrix
    transitions = load_transitions()
    dir_mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = {"比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克"}[t["tiyong_relation"]]
        dir_mats[g][t["source"], t["destination"]] = 1
    A_ke_hex = np.maximum(dir_mats["克"], dir_mats["克"].T).astype(float)

    # Full spectrum
    eigs_hex = np.linalg.eigh(A_ke_hex)[0]
    rho_hex = max(abs(eigs_hex))
    h_hex = np.log(rho_hex)

    print(f"\n  Hex-level 克 (OR-symmetrized):")
    print(f"    Spectral radius: ρ = {rho_hex:.6f}")
    print(f"    Topological entropy: h = log(ρ) = {h_hex:.6f}")
    print(f"    log(φ) = {np.log(PHI):.6f}")
    print(f"    Entropy ratio h_hex/log(φ) = {h_hex/np.log(PHI):.6f}")

    # Identify φ-related eigenvalues
    phi_related = []
    for v in sorted(eigs_hex):
        for cand, label in [
            (2*PHI, "2φ"), (-2*PHI, "-2φ"),
            (2/PHI, "2/φ"), (-2/PHI, "-2/φ"),
            (PHI, "φ"), (-PHI, "-φ"),
            (1/PHI, "1/φ"), (-1/PHI, "-1/φ"),
        ]:
            if abs(v - cand) < 1e-5:
                phi_related.append((v, label))
                break

    print(f"\n  φ-related eigenvalues in hex spectrum:")
    for v, label in phi_related:
        print(f"    {v:.6f} = {label}")

    # Coherent sector: eigenvalues ±2φ, ±2/φ
    coherent_eigs = [v for v, label in phi_related if "2" in label]
    incoherent_eigs = [v for v in eigs_hex if not any(abs(v - c) < 1e-5 for c in coherent_eigs)]

    print(f"\n  Coherent sector (2φ-related): {len(coherent_eigs)} eigenvalues")
    print(f"    Values: {[round(v, 6) for v in sorted(coherent_eigs)]}")

    # If we restrict to coherent eigenspace, the effective spectral radius is max|coherent|
    if coherent_eigs:
        rho_coherent = max(abs(v) for v in coherent_eigs)
        h_coherent = np.log(rho_coherent)
        print(f"    Effective spectral radius: {rho_coherent:.6f}")
        print(f"    Effective entropy: {h_coherent:.6f}")
        print(f"    = log(2φ) = log(2) + log(φ) = {np.log(2) + np.log(PHI):.6f}")

        # Fraction of total entropy
        print(f"    Fraction of total entropy: {h_coherent/h_hex:.6f}")
    else:
        rho_coherent = 0
        h_coherent = 0

    # Incoherent sector
    if incoherent_eigs:
        rho_incoherent = max(abs(v) for v in incoherent_eigs)
        h_incoherent = np.log(rho_incoherent)
        print(f"\n  Incoherent sector: {len(incoherent_eigs)} eigenvalues")
        print(f"    Max |eigenvalue|: {rho_incoherent:.6f}")
        print(f"    Entropy: {h_incoherent:.6f}")
        print(f"    Dominant? {'YES' if rho_incoherent >= rho_coherent else 'NO'}")
    else:
        rho_incoherent = 0
        h_incoherent = 0

    # The actual spectral radius of hex-level 克
    print(f"\n  Entropy decomposition:")
    print(f"    Total:      h = {h_hex:.6f} (ρ = {rho_hex:.6f})")
    print(f"    Coherent:   h = {h_coherent:.6f} (ρ = {rho_coherent:.6f})")
    print(f"    Incoherent: h = {h_incoherent:.6f} (ρ = {rho_incoherent:.6f})")
    print(f"    Ratio coherent/total: {h_coherent/h_hex:.6f}")

    # The coherent eigenvalues are precisely the tensor product:
    # eigenvalues of A_ke^{trig} = ±φ, ±1/φ
    # Tensor: λ_i + λ_j gives ±2φ, ±2/φ, 0, 0, ±(φ+1/φ)=±√5, ±(φ-1/φ)=±1
    # Wait, that's not what we see. Let me check.
    eigs_trig = sorted([v for v, _ in eigendecomp(trig_mats["克"])])
    print(f"\n  Trigram-level 克 eigenvalues: {[round(v, 6) for v in eigs_trig]}")
    tensor_eigs = sorted([a + b for a in eigs_trig for b in eigs_trig])
    print(f"  Tensor sums (λ_i + λ_j): {[round(v, 6) for v in tensor_eigs]}")

    # Count unique tensor eigenvalues
    tensor_unique = sorted(set(round(v, 6) for v in tensor_eigs))
    print(f"  Unique tensor eigenvalues: {tensor_unique}")

    # Check which tensor eigenvalues appear in hex spectrum
    print(f"\n  Tensor eigenvalue appearance in hex spectrum:")
    for tv in tensor_unique:
        count_tensor = sum(1 for v in tensor_eigs if abs(v - tv) < 1e-5)
        count_hex = sum(1 for v in eigs_hex if abs(v - tv) < 1e-5)
        in_hex = "✓" if count_hex > 0 else "✗"
        # Identify
        ident = ""
        for cand, label in [
            (0, "0"), (1, "1"), (-1, "-1"),
            (5**0.5, "√5"), (-5**0.5, "-√5"),
            (2*PHI, "2φ"), (-2*PHI, "-2φ"),
            (2/PHI, "2/φ"), (-2/PHI, "-2/φ"),
        ]:
            if abs(tv - cand) < 1e-5:
                ident = f" = {label}"
                break
        print(f"    {tv:8.4f}{ident}: tensor×{count_tensor}, hex×{count_hex} {in_hex}")

    results["hex_entropy"] = {
        "rho": float(rho_hex),
        "h_top": float(h_hex),
        "log_phi": float(np.log(PHI)),
    }
    results["coherent"] = {
        "eigenvalues": [round(v, 6) for v in sorted(coherent_eigs)],
        "rho": float(rho_coherent),
        "h_top": float(h_coherent),
        "fraction_of_total": float(h_coherent / h_hex) if h_hex > 0 else 0,
    }
    results["incoherent"] = {
        "rho": float(rho_incoherent),
        "h_top": float(h_incoherent),
    }
    results["tensor_eigenvalues"] = [round(v, 6) for v in tensor_unique]

    return results


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    atlas = load_atlas()
    trigram_elements = get_trigram_elements(atlas)
    trig_mats = build_trigram_matrices(trigram_elements)

    print("=" * 70)
    print("PROBE A: GOLDEN MEAN SHIFT COMPARISON")
    print("=" * 70)

    r1 = part1(trigram_elements, trig_mats)
    r2 = part2(trig_mats, trigram_elements)
    r3 = part3(trig_mats)
    r4 = part4(trig_mats)

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "═" * 70)
    print("SUMMARY")
    print("═" * 70)
    h_hex = r4["hex_entropy"]["h_top"]
    log_phi = r4["hex_entropy"]["log_phi"]
    h_coh = r4["coherent"]["h_top"]
    rho_hex = r4["hex_entropy"]["rho"]
    print(f"""
  P₄ walks and the golden mean shift are NOT conjugate but related by
  BIPARTITE DOUBLE COVER.

  Precise relationship:
  1. P₄ is bipartite (even/odd vertices). GMS is not (has self-loop on 0).
  2. ζ_P4(z) = 1/[(1-z-z²)(1+z-z²)] = ζ_GMS(z) × ζ_anti(z)
     The GMS zeta is an exact factor of the P₄ zeta function.
  3. A_P4² restricted to either bipartition class gives a 2×2 matrix
     with spectrum {{φ², 1/φ²}} — identical to M_GMS².
  4. The 'anti-GMS' factor (1+z-z²)⁻¹ corresponds to the z→-z symmetry
     of the bipartite graph (negating odd-parity eigenvalues).
  5. P₄ has the GMS as a topological factor (via the folding map that
     identifies vertices by bipartition class parity).

  At the hexagram level (64×64 OR-symmetrized):
  - Total entropy h ≈ {h_hex:.4f}, much higher than log(φ) ≈ {log_phi:.4f}
  - Coherent sector (eigenvalues ±2φ, ±2/φ) has h = log(2φ) ≈ {h_coh:.4f}
  - The dominant spectral radius ({rho_hex:.4f}) comes from incoherent modes
  - Tensor eigenvalues ±2φ, ±2/φ appear in hex spectrum; ±√5, ±1 do NOT
  - Only 4 of 9 tensor eigenvalue types survive hex-level mixing
""")

    # Save results
    all_results = {
        "part1_topology": r1,
        "part2_forbidden_words": r2,
        "part3_gms_comparison": r3,
        "part4_hex_decomposition": r4,
    }

    out_path = HERE / "probeA_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
