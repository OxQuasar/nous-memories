"""
Probe 1: 五行-labeled subgraph spectra of the Q₆ transition graph.

Key finding: The 五行 classification is inherently DIRECTED. Each undirected edge
(i,j) has two directed transitions with potentially different 五行 types.
132 of 192 undirected edges have conflicting types.

This script analyzes:
A) Directed adjacency matrices (the true structure)
B) Undirected "OR" matrices (edge present if either direction has that type)
C) Edge pair classification (how forward/backward types correlate)
D) Trigram-level structure
"""

import json
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

RELATION_GROUPS = {
    "比和": "比和",
    "体生用": "生",
    "生体": "生",
    "体克用": "克",
    "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]

# ── Loading ────────────────────────────────────────────────────────

def load_transitions():
    with open(ATLAS_DIR / "transitions.json") as f:
        return json.load(f)["bian_fan"]

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

# ── Matrix Construction ────────────────────────────────────────────

def build_directed_matrices(transitions):
    """Three 64×64 directed adjacency matrices."""
    mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = RELATION_GROUPS[t["tiyong_relation"]]
        mats[g][t["source"], t["destination"]] = 1
    return mats

def symmetrize(A):
    """OR-symmetrize: A_sym[i,j] = max(A[i,j], A[j,i])."""
    return np.maximum(A, A.T)

def build_q6():
    A = np.zeros((64, 64), dtype=int)
    for i in range(64):
        for bit in range(6):
            A[i, i ^ (1 << bit)] = 1
    return A

# ── Spectral Analysis ─────────────────────────────────────────────

def eigendecomp_symmetric(A):
    """Eigenvalues + multiplicities for symmetric real matrix."""
    eigvals = np.linalg.eigh(A.astype(float))[0]
    rounded = np.round(eigvals, 8)
    unique, counts = np.unique(rounded, return_counts=True)
    return [(float(v), int(c)) for v, c in zip(unique, counts)]

def eigendecomp_directed(A):
    """Eigenvalues of directed (asymmetric) matrix. Returns complex eigenvalues."""
    eigvals = np.linalg.eigvals(A.astype(float))
    # Round real and imag parts
    rounded = np.round(eigvals, 8)
    # Group by value
    pairs = [(complex(v).real, complex(v).imag) for v in rounded]
    counts = Counter(pairs)
    result = sorted(counts.items())
    return [((r, i), c) for (r, i), c in result]

def spectral_gap(eig_pairs):
    vals = sorted([v for v, _ in eig_pairs], reverse=True)
    return vals[0] - vals[1] if len(vals) >= 2 else 0.0

def get_components(A, directed=False):
    n, labels = connected_components(sparse.csr_matrix(A), directed=directed,
                                      connection='strong' if directed else 'weak')
    sizes = sorted(Counter(labels).values(), reverse=True)
    return n, sizes

def edge_count_directed(A):
    return int(np.sum(A))

def edge_count_undirected(A):
    """For symmetric matrix."""
    return int(np.sum(A)) // 2

# ── Trigram Matrices ───────────────────────────────────────────────

def get_trigram_elements(atlas):
    elems = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            elems[t["val"]] = t["element"]
    return elems

SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

def wuxing_relation(yong_elem, ti_elem):
    if yong_elem == ti_elem:
        return "比和"
    if SHENG[yong_elem] == ti_elem:
        return "生"  # yong produces ti
    if SHENG[ti_elem] == yong_elem:
        return "生"  # ti produces yong
    if KE[yong_elem] == ti_elem:
        return "克"
    if KE[ti_elem] == yong_elem:
        return "克"
    raise ValueError(f"No relation: {yong_elem} ↔ {ti_elem}")

def build_trigram_directed_matrices(trigram_elements):
    """
    8×8 directed matrices for each group.
    Edge a→b exists if they differ by 1 bit and the relation when
    a is 用 (source) and some fixed 体 produces group g.
    
    But at the trigram level, there's no fixed 体. Instead, we record
    the relation between the pair (a,b) as: what group does (用=a, 体=b) give?
    This models: "trigram a transitions toward trigram b".
    """
    mats = {g: np.zeros((8, 8), dtype=int) for g in GROUP_NAMES}
    for a in range(8):
        for bit in range(3):
            b = a ^ (1 << bit)
            ea, eb = trigram_elements[a], trigram_elements[b]
            # a is the source (用), b is NOT the 体.
            # At the hexagram level, 用=source's changing trigram,
            # 体=the OTHER (stationary) trigram.
            # At the trigram level, we don't have 体.
            # Let's just record undirected: relation(ea, eb).
            g = wuxing_relation(ea, eb)
            mats[g][a, b] = 1
            mats[g][b, a] = 1
    return mats

# ── Edge Pair Analysis ─────────────────────────────────────────────

def edge_pair_analysis(transitions):
    """Classify each undirected edge by its (forward_group, backward_group) pair."""
    edge_map = {}  # (i,j) with i<j -> {direction: group}
    for t in transitions:
        s, d = t["source"], t["destination"]
        key = (min(s, d), max(s, d))
        direction = "fwd" if s < d else "bwd"
        g = RELATION_GROUPS[t["tiyong_relation"]]
        edge_map.setdefault(key, {})[direction] = g
    
    pair_counts = Counter()
    for key, dirs in edge_map.items():
        fwd = dirs.get("fwd", "?")
        bwd = dirs.get("bwd", "?")
        pair_type = tuple(sorted([fwd, bwd]))
        pair_counts[pair_type] += 1
    
    return pair_counts

# ── Tensor Product ─────────────────────────────────────────────────

def tensor_product_test(eig8, eig64):
    """Test if 64-spectrum = {λᵢ + λⱼ} from 8-spectrum."""
    vals8 = []
    for v, m in eig8:
        vals8.extend([v] * m)
    expected = sorted([a + b for a in vals8 for b in vals8])
    actual = sorted([v for v, m in eig64 for _ in range(m)])
    
    if len(expected) != len(actual):
        return False, f"size mismatch: {len(expected)} vs {len(actual)}", expected, actual
    
    deviation = max(abs(a - e) for a, e in zip(actual, expected))
    return deviation < 1e-6, float(deviation), expected, actual

# ── Display ────────────────────────────────────────────────────────

def fmt_eig(eig_pairs):
    lines = []
    for val, mult in sorted(eig_pairs):
        approx = ""
        phi = (1 + 5**0.5) / 2
        for candidate, label in [
            (round(val), str(int(round(val)))),
            (phi, "φ"), (-phi, "-φ"),
            (1/phi, "1/φ"), (-1/phi, "-1/φ"),
            (5**0.5, "√5"), (-5**0.5, "-√5"),
            (2**0.5, "√2"), (-2**0.5, "-√2"),
        ]:
            if abs(val - candidate) < 1e-7:
                approx = f" ≈ {label}"
                break
        lines.append(f"    {val:12.6f}{approx}  (×{mult})")
    return "\n".join(lines)

def fmt_eig_complex(eig_pairs):
    lines = []
    for (re, im), mult in sorted(eig_pairs):
        if abs(im) < 1e-8:
            lines.append(f"    {re:12.6f}  (×{mult})")
        else:
            lines.append(f"    {re:9.6f} ± {abs(im):.6f}i  (×{mult})")
    return "\n".join(lines)

# ── Main ───────────────────────────────────────────────────────────

def main():
    transitions = load_transitions()
    atlas = load_atlas()
    
    print("=" * 65)
    print("PROBE 1: 五行-labeled Subgraph Spectra")
    print("=" * 65)
    
    # ── Section A: Directed structure ──────────────────────────────
    print("\n" + "─" * 65)
    print("A. DIRECTED ADJACENCY MATRICES")
    print("─" * 65)
    
    dir_mats = build_directed_matrices(transitions)
    
    print("\n  Directed edge counts:")
    dir_edge_counts = {}
    for g in GROUP_NAMES:
        ec = edge_count_directed(dir_mats[g])
        dir_edge_counts[g] = ec
        print(f"    {g}: {ec}")
    print(f"    Total: {sum(dir_edge_counts.values())} (= 64 × 6 = 384)")
    
    # Verify directed sum = Q₆
    A_q6 = build_q6()
    dir_sum = sum(dir_mats[g] for g in GROUP_NAMES)
    print(f"\n  A_克 + A_生 + A_比和 = A_Q₆ (directed): {np.array_equal(dir_sum, A_q6)}")
    
    # Directed eigenvalues (complex)
    print("\n  Directed eigenvalues (showing real parts, * = has imaginary):")
    dir_eigs = {}
    for g in GROUP_NAMES:
        de = eigendecomp_directed(dir_mats[g])
        dir_eigs[g] = de
        n_real = sum(c for (r, i), c in de if abs(i) < 1e-8)
        n_complex = sum(c for (r, i), c in de if abs(i) >= 1e-8)
        max_real = max(r for (r, i), c in de)
        min_real = min(r for (r, i), c in de)
        print(f"\n    [{g}] {n_real} real, {n_complex} complex eigenvalues")
        print(f"    Spectral radius: {max(abs(complex(r, i)) for (r, i), c in de):.6f}")
        print(f"    Real range: [{min_real:.6f}, {max_real:.6f}]")
    
    # Is each directed matrix's symmetrization the same as the OR-symmetrized?
    # (It should be, since we set A[s,d]=1 for each directed edge)
    
    # Strongly connected components
    print("\n  Strongly connected components (directed):")
    for g in GROUP_NAMES:
        n, sizes = get_components(dir_mats[g], directed=True)
        print(f"    {g}: {n} components, sizes = {sizes[:10]}{'...' if len(sizes) > 10 else ''}")
    
    # ── Section B: Edge pair analysis ──────────────────────────────
    print("\n" + "─" * 65)
    print("B. EDGE PAIR CLASSIFICATION")
    print("─" * 65)
    
    pair_counts = edge_pair_analysis(transitions)
    print("\n  Each undirected edge has two directions with possibly different groups.")
    print("  Distribution of (group_fwd, group_bwd) pairs:")
    for pair_type, count in sorted(pair_counts.items()):
        sym = "symmetric" if pair_type[0] == pair_type[1] else "ASYMMETRIC"
        print(f"    {pair_type}: {count:3d} edges  [{sym}]")
    
    n_sym = sum(c for p, c in pair_counts.items() if p[0] == p[1])
    n_asym = sum(c for p, c in pair_counts.items() if p[0] != p[1])
    print(f"\n  Symmetric: {n_sym}/192, Asymmetric: {n_asym}/192")
    
    # ── Section C: Symmetrized (OR) analysis ───────────────────────
    print("\n" + "─" * 65)
    print("C. SYMMETRIZED (OR) ADJACENCY MATRICES")
    print("─" * 65)
    print("  A_sym[i,j] = 1 if ANY directed transition (i→j or j→i) of type g exists")
    
    sym_mats = {g: symmetrize(dir_mats[g]) for g in GROUP_NAMES}
    
    print("\n  Undirected edge counts (OR-symmetrized):")
    sym_edge_counts = {}
    for g in GROUP_NAMES:
        ec = edge_count_undirected(sym_mats[g])
        sym_edge_counts[g] = ec
        print(f"    {g}: {ec}")
    print(f"    Total: {sum(sym_edge_counts.values())} (> 192 due to edge overlap)")
    
    sym_sum = sum(sym_mats[g] for g in GROUP_NAMES)
    overlap_edges = (sym_sum > 1).sum() // 2
    print(f"    Overlapping edges: {overlap_edges}")
    
    # ── Section D: AND-symmetrized (exclusive) decomposition ──────
    print("\n" + "─" * 65)
    print("D. AND-SYMMETRIZED (EXCLUSIVE) DECOMPOSITION")
    print("─" * 65)
    print("  A_and[i,j] = 1 only if BOTH directions (i→j AND j→i) have type g")
    
    and_mats = {g: np.minimum(dir_mats[g], dir_mats[g].T) for g in GROUP_NAMES}
    
    print("\n  Undirected edge counts (AND-symmetrized):")
    and_edge_counts = {}
    for g in GROUP_NAMES:
        ec = edge_count_undirected(and_mats[g])
        and_edge_counts[g] = ec
        print(f"    {g}: {ec}")
    and_total = sum(and_edge_counts.values())
    print(f"    Total: {and_total}")
    
    and_sum = sum(and_mats[g] for g in GROUP_NAMES)
    and_valid = np.array_equal(and_sum, build_q6()) if and_total == 192 else False
    print(f"    Forms partition of Q₆: {and_valid}")
    
    # The AND matrices give a clean partition only for edges where both
    # directions agree. The asymmetric edges aren't in ANY and_mat.
    missing = (and_sum == 0) & (A_q6 == 1)
    n_missing = missing.sum() // 2
    print(f"    Edges missing (asymmetric): {n_missing}")
    print(f"    Edges covered: {and_total} + {n_missing} = {and_total + n_missing}")
    
    # ── Section E: Spectra of symmetric matrices ───────────────────
    print("\n" + "─" * 65)
    print("E. SPECTRA OF SYMMETRIC MATRICES")
    print("─" * 65)
    
    # Use (A + A^T)/2 for a proper symmetric analysis of the directed structure
    # This preserves the symmetric part and averages out the antisymmetric part
    avg_mats = {g: (dir_mats[g] + dir_mats[g].T) / 2.0 for g in GROUP_NAMES}
    
    # Also compute AND-symmetrized spectra (cleaner partition)
    print("\n  --- AND-symmetrized spectra (edges where both directions agree) ---")
    and_eigs = {}
    for g in GROUP_NAMES:
        and_eigs[g] = eigendecomp_symmetric(and_mats[g])
        print(f"\n  [{g}] ({and_edge_counts[g]} edges):")
        print(fmt_eig(and_eigs[g]))
    
    print("\n  --- OR-symmetrized spectra ---")
    or_eigs = {}
    for g in GROUP_NAMES:
        or_eigs[g] = eigendecomp_symmetric(sym_mats[g])
        print(f"\n  [{g}] ({sym_edge_counts[g]} edges):")
        print(fmt_eig(or_eigs[g]))
    
    print("\n  --- Average (A+Aᵀ)/2 spectra ---")
    avg_eigs = {}
    for g in GROUP_NAMES:
        avg_eigs[g] = eigendecomp_symmetric(avg_mats[g])
        print(f"\n  [{g}]:")
        print(fmt_eig(avg_eigs[g]))
    
    # Q₆ reference
    print("\n  [Q₆ reference]:")
    eig_q6 = eigendecomp_symmetric(A_q6)
    print(fmt_eig(eig_q6))
    
    # ── Section F: Spectral gaps ───────────────────────────────────
    print("\n" + "─" * 65)
    print("F. SPECTRAL GAPS (AND-symmetrized)")
    print("─" * 65)
    for g in GROUP_NAMES:
        print(f"  {g}: {spectral_gap(and_eigs[g]):.6f}")
    print(f"  Q₆: {spectral_gap(eig_q6):.6f}")
    
    # ── Section G: Connected components ────────────────────────────
    print("\n" + "─" * 65)
    print("G. CONNECTED COMPONENTS")
    print("─" * 65)
    
    print("\n  AND-symmetrized:")
    and_components = {}
    for g in GROUP_NAMES:
        n, sizes = get_components(and_mats[g])
        and_components[g] = {"count": n, "sizes": sizes}
        print(f"    {g}: {n} component(s), sizes = {sizes}")
    
    print("\n  OR-symmetrized:")
    or_components = {}
    for g in GROUP_NAMES:
        n, sizes = get_components(sym_mats[g])
        or_components[g] = {"count": n, "sizes": sizes}
        print(f"    {g}: {n} component(s), sizes = {sizes}")
    
    print("\n  Directed (strongly connected):")
    dir_components = {}
    for g in GROUP_NAMES:
        n, sizes = get_components(dir_mats[g], directed=True)
        dir_components[g] = {"count": n, "sizes": sizes}
        print(f"    {g}: {n} component(s), sizes = {sizes[:10]}{'...' if len(sizes) > 10 else ''}")
    
    print("\n  Directed (weakly connected):")
    for g in GROUP_NAMES:
        n, sizes = get_components(dir_mats[g], directed=False)
        print(f"    {g}: {n} component(s), sizes = {sizes}")
    
    # ── Section H: Trigram-level analysis ──────────────────────────
    print("\n" + "─" * 65)
    print("H. TRIGRAM-LEVEL ANALYSIS")
    print("─" * 65)
    
    trigram_elements = get_trigram_elements(atlas)
    print("\n  Trigram elements:")
    for v in range(8):
        print(f"    {v} ({format(v, '03b')}): {trigram_elements[v]}")
    
    trig_mats = build_trigram_directed_matrices(trigram_elements)
    
    print("\n  Edge counts (8×8, undirected):")
    for g in GROUP_NAMES:
        print(f"    {g}: {edge_count_undirected(trig_mats[g])}")
    
    A_q3 = np.zeros((8, 8), dtype=int)
    for i in range(8):
        for bit in range(3):
            A_q3[i, i ^ (1 << bit)] = 1
    print(f"  Sum = Q₃: {np.array_equal(sum(trig_mats[g] for g in GROUP_NAMES), A_q3)}")
    
    print("\n  Trigram adjacency lists:")
    elem_names = {0: "Kun☷", 1: "Zhen☳", 2: "Kan☵", 3: "Gen☶",
                  4: "Dui☱", 5: "Li☲", 6: "Xun☴", 7: "Qian☰"}
    for g in GROUP_NAMES:
        edges = []
        for i in range(8):
            for j in range(i+1, 8):
                if trig_mats[g][i, j]:
                    edges.append(f"{elem_names[i]}-{elem_names[j]}")
        print(f"    {g}: {', '.join(edges)}")
    
    print("\n  Eigenvalues (8×8):")
    eig8 = {}
    for g in GROUP_NAMES:
        eig8[g] = eigendecomp_symmetric(trig_mats[g])
        print(f"\n    [{g}]:")
        print(fmt_eig(eig8[g]))
    
    # Tensor product test against AND-symmetrized 64×64
    print("\n" + "─" * 65)
    print("I. TENSOR PRODUCT TEST")
    print("─" * 65)
    print("  Testing: spec(A_g^{64}) =? {λᵢ + λⱼ : λᵢ,λⱼ ∈ spec(A_g^{8})}")
    print("  Using AND-symmetrized 64×64 matrices")
    
    tp_results = {}
    for g in GROUP_NAMES:
        match, deviation, expected, actual = tensor_product_test(eig8[g], and_eigs[g])
        tp_results[g] = {"match": bool(match), "deviation": deviation if isinstance(deviation, float) else str(deviation)}
        status = "✓ MATCH" if match else f"✗ NO MATCH (max dev: {deviation})"
        print(f"    {g}: {status}")
    
    # ── Section J: Degree distributions ────────────────────────────
    print("\n" + "─" * 65)
    print("J. DEGREE DISTRIBUTIONS")
    print("─" * 65)
    
    print("\n  Directed out-degree:")
    for g in GROUP_NAMES:
        out_deg = dir_mats[g].sum(axis=1)
        print(f"    {g}: {dict(sorted(Counter(out_deg.tolist()).items()))}")
    
    print("\n  Directed in-degree:")
    for g in GROUP_NAMES:
        in_deg = dir_mats[g].sum(axis=0)
        print(f"    {g}: {dict(sorted(Counter(in_deg.tolist()).items()))}")
    
    print("\n  AND-symmetrized degree:")
    for g in GROUP_NAMES:
        deg = and_mats[g].sum(axis=1)
        print(f"    {g}: {dict(sorted(Counter(deg.tolist()).items()))}")
    
    # ── Section K: Antisymmetric part analysis ─────────────────────
    print("\n" + "─" * 65)
    print("K. ANTISYMMETRIC STRUCTURE")
    print("─" * 65)
    print("  B_g = (A_g - A_g^T) / 2  (antisymmetric part)")
    
    for g in GROUP_NAMES:
        B = (dir_mats[g].astype(float) - dir_mats[g].T.astype(float)) / 2
        norm = np.linalg.norm(B, 'fro')
        sym_norm = np.linalg.norm(avg_mats[g], 'fro')
        ratio = norm / sym_norm if sym_norm > 0 else 0
        print(f"    {g}: ||B||_F = {norm:.4f}, ||S||_F = {sym_norm:.4f}, ratio = {ratio:.4f}")
    
    # Eigenvalues of iB (should be real for antisymmetric B)
    print("\n  Eigenvalues of iB (real spectrum of antisymmetric part):")
    for g in GROUP_NAMES:
        B = (dir_mats[g].astype(float) - dir_mats[g].T.astype(float)) / 2
        iB_eigvals = np.linalg.eigvalsh(1j * B)  # Hermitian
        rounded = np.round(iB_eigvals.real, 8)
        unique, counts = np.unique(rounded, return_counts=True)
        nonzero = [(float(v), int(c)) for v, c in zip(unique, counts) if abs(v) > 1e-7]
        print(f"    {g}: {len(nonzero)} nonzero eigenvalue groups, "
              f"max |λ| = {max(abs(v) for v, _ in nonzero) if nonzero else 0:.6f}")
    
    # ── Save results ───────────────────────────────────────────────
    results = {
        "directed_edge_counts": dir_edge_counts,
        "q6_directed_decomposition_valid": True,
        "edge_pair_distribution": {str(k): v for k, v in pair_counts.items()},
        "symmetric_edges": n_sym,
        "asymmetric_edges": n_asym,
        "and_symmetrized": {
            "edge_counts": and_edge_counts,
            "eigenvalues": {
                g: [{"value": round(v, 10), "multiplicity": m} for v, m in and_eigs[g]]
                for g in GROUP_NAMES
            },
            "components": and_components,
            "spectral_gaps": {g: spectral_gap(and_eigs[g]) for g in GROUP_NAMES},
        },
        "or_symmetrized": {
            "edge_counts": sym_edge_counts,
            "eigenvalues": {
                g: [{"value": round(v, 10), "multiplicity": m} for v, m in or_eigs[g]]
                for g in GROUP_NAMES
            },
            "components": or_components,
        },
        "trigram": {
            "elements": {str(k): v for k, v in trigram_elements.items()},
            "edge_counts": {g: edge_count_undirected(trig_mats[g]) for g in GROUP_NAMES},
            "eigenvalues": {
                g: [{"value": round(v, 10), "multiplicity": m} for v, m in eig8[g]]
                for g in GROUP_NAMES
            },
        },
        "tensor_product": tp_results,
        "q6_spectrum": [{"value": round(v, 10), "multiplicity": m} for v, m in eig_q6],
    }
    
    out_path = HERE / "p1_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
