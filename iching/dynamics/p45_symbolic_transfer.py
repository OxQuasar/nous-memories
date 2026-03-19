"""
Probes 4+5: Symbolic Dynamics, Transfer Matrices, and Stage-vs-Drama Test.

Part 1: Symbolic dynamics on the 五行-labeled transition graph
Part 2: Transfer matrices and φ
Part 3: Stage vs Drama — entropy across assignments
Part 4: Wood exclusion mechanism test
"""

import json
import numpy as np
from collections import Counter
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]
ELEMENTS = ["Earth", "Wood", "Water", "Metal", "Fire"]
SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

PHI = (1 + 5**0.5) / 2

# ── Loading ────────────────────────────────────────────────────────

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def load_transitions():
    with open(ATLAS_DIR / "transitions.json") as f:
        return json.load(f)["bian_fan"]

def vertex_type(atlas, h):
    return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

def wuxing_group(e1, e2):
    if e1 == e2: return "比和"
    if SHENG[e1] == e2 or SHENG[e2] == e1: return "生"
    return "克"

def hu_formula(h):
    b = [(h >> i) & 1 for i in range(6)]
    return b[1] | (b[2] << 1) | (b[3] << 2) | (b[2] << 3) | (b[3] << 4) | (b[4] << 5)

def build_q6():
    A = np.zeros((64, 64), dtype=int)
    for i in range(64):
        for bit in range(6):
            A[i, i ^ (1 << bit)] = 1
    return A

def build_directed_matrices(transitions):
    mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = RELATION_GROUPS[t["tiyong_relation"]]
        mats[g][t["source"], t["destination"]] = 1
    return mats

def build_or_symmetrized(dir_mats):
    return {g: np.maximum(A, A.T) for g, A in dir_mats.items()}

def build_and_symmetrized(dir_mats):
    return {g: np.minimum(A, A.T) for g, A in dir_mats.items()}

def get_trigram_elements(atlas):
    elems = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            elems[t["val"]] = t["element"]
    return elems

def build_trigram_matrices(trigram_elements):
    mats = {g: np.zeros((8, 8), dtype=int) for g in GROUP_NAMES}
    for a in range(8):
        for bit in range(3):
            b = a ^ (1 << bit)
            if b <= a:
                continue
            ea, eb = trigram_elements[a], trigram_elements[b]
            g = wuxing_group(ea, eb)
            mats[g][a, b] = 1
            mats[g][b, a] = 1
    return mats

def spectral_radius(A):
    if A.shape[0] == 0:
        return 0.0
    return float(max(abs(v) for v in np.linalg.eigvals(A.astype(float))))

def eigendecomp(A):
    eigvals = np.linalg.eigh(A.astype(float))[0]
    rounded = np.round(eigvals, 8)
    unique, counts = np.unique(rounded, return_counts=True)
    return [(float(v), int(c)) for v, c in zip(unique, counts)]


# ══════════════════════════════════════════════════════════════════
# PART 1: Symbolic Dynamics
# ══════════════════════════════════════════════════════════════════

def part1(atlas, transitions, dir_mats, or_mats, and_mats):
    print("\n" + "═" * 70)
    print("PART 1: SYMBOLIC DYNAMICS ON 五行-LABELED TRANSITION GRAPH")
    print("═" * 70)
    results = {}

    # ── 1a: Two-step type transitions ──────────────────────────────
    print("\n── 1a. Two-Step Type Transitions ──")

    # Build adjacency list for directed transitions
    adj = {h: [] for h in range(64)}
    for t in transitions:
        adj[t["source"]].append(t["destination"])

    # Count all length-2 paths with type triples
    tensor = {}
    for g1 in GROUP_NAMES:
        for g2 in GROUP_NAMES:
            for g3 in GROUP_NAMES:
                tensor[(g1, g2, g3)] = 0

    total_paths = 0
    for h in range(64):
        g1 = vertex_type(atlas, h)
        for h_prime in adj[h]:
            g2 = vertex_type(atlas, h_prime)
            for h_double in adj[h_prime]:
                g3 = vertex_type(atlas, h_double)
                tensor[(g1, g2, g3)] += 1
                total_paths += 1

    print(f"  Total length-2 paths: {total_paths} (expected: 384 × 6 = {384*6})")

    # Display as slices
    forbidden = []
    for g1 in GROUP_NAMES:
        print(f"\n  Starting from {g1}:")
        print(f"    {'mid→end':>10} | {'比和':>5} {'生':>5} {'克':>5}")
        print(f"    {'-'*10}-+-{'-'*5}-{'-'*5}-{'-'*5}")
        for g2 in GROUP_NAMES:
            row = [tensor[(g1, g2, g3)] for g3 in GROUP_NAMES]
            print(f"    {g2:>10} | {row[0]:>5} {row[1]:>5} {row[2]:>5}")
            for g3, count in zip(GROUP_NAMES, row):
                if count == 0:
                    forbidden.append((g1, g2, g3))

    print(f"\n  Forbidden two-step triples: {len(forbidden)}")
    for f in forbidden:
        print(f"    {f[0]} → {f[1]} → {f[2]}")

    results["1a"] = {
        "tensor": {f"{a},{b},{c}": v for (a, b, c), v in tensor.items()},
        "total_paths": total_paths,
        "forbidden_triples": [list(f) for f in forbidden],
    }

    # ── 1b: 3×3 type transition matrix ─────────────────────────────
    print("\n── 1b. 3×3 Type Transition Matrix ──")

    # Count directed edges between type classes
    M_counts = np.zeros((3, 3), dtype=int)
    type_sizes = {g: sum(1 for h in range(64) if vertex_type(atlas, h) == g) for g in GROUP_NAMES}

    for t in transitions:
        src_type = vertex_type(atlas, t["source"])
        dst_type = vertex_type(atlas, t["destination"])
        i = GROUP_NAMES.index(src_type)
        j = GROUP_NAMES.index(dst_type)
        M_counts[i, j] += 1

    print("  Edge counts between type classes:")
    print(f"    {'':>5} | {'比和':>5} {'生':>5} {'克':>5} | out")
    print(f"    {'-'*5}-+-{'-'*5}-{'-'*5}-{'-'*5}-+-----")
    for i, g in enumerate(GROUP_NAMES):
        row = M_counts[i]
        print(f"    {g:>5} | {row[0]:>5} {row[1]:>5} {row[2]:>5} | {row.sum():>5}")

    # Normalize to Markov transition matrix
    row_sums = M_counts.sum(axis=1, keepdims=True)
    P = M_counts.astype(float) / row_sums

    print("\n  Markov transition matrix P:")
    for i, g in enumerate(GROUP_NAMES):
        row = P[i]
        print(f"    {g:>5}: [{row[0]:.6f}  {row[1]:.6f}  {row[2]:.6f}]")

    # Eigenvalues
    eig_P = np.linalg.eigvals(P)
    print(f"\n  Eigenvalues of P: {[f'{v:.6f}' for v in sorted(eig_P, key=lambda x: -abs(x))]}")

    # Stationary distribution: π P = π
    eigvals_T, eigvecs_T = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigvals_T - 1.0))
    pi = eigvecs_T[:, idx].real
    pi = pi / pi.sum()
    print(f"  Stationary distribution: {[f'{v:.6f}' for v in pi]}")
    proportional = np.array([type_sizes[g] for g in GROUP_NAMES]) / 64.0
    print(f"  Size-proportional:       {[f'{v:.6f}' for v in proportional]}")
    print(f"  Stationary ≈ proportional: {np.allclose(pi, proportional, atol=0.01)}")

    results["1b"] = {
        "edge_counts": M_counts.tolist(),
        "markov_matrix": P.tolist(),
        "eigenvalues": [float(v.real) for v in sorted(eig_P, key=lambda x: -abs(x))],
        "stationary": pi.tolist(),
        "proportional": proportional.tolist(),
    }

    # ── 1c: Topological entropy ────────────────────────────────────
    print("\n── 1c. Topological Entropy ──")

    h_top = {"Q6": float(np.log(6))}
    for label, mats in [("OR-sym", or_mats), ("AND-sym", and_mats), ("directed", dir_mats)]:
        for g in GROUP_NAMES:
            rho = spectral_radius(mats[g])
            h = float(np.log(rho)) if rho > 0 else float('-inf')
            key = f"{g}_{label}"
            h_top[key] = h
            print(f"  {label:>10} {g}: ρ = {rho:.6f}, h_top = {h:.6f}")
        print()

    print(f"  Q₆: ρ = 6, h_top = {h_top['Q6']:.6f}")

    results["1c"] = h_top

    # ── 1d: Closed walk counts (zeta coefficients) ─────────────────
    print("\n── 1d. Closed Walk Counts N_n = tr(A^n) (OR-symmetrized) ──")

    walk_counts = {}
    print(f"  {'n':>3} | {'比和':>12} {'生':>12} {'克':>12} | {'Q₆':>12}")
    print(f"  {'-'*3}-+-{'-'*12}-{'-'*12}-{'-'*12}-+-{'-'*12}")

    A_q6 = build_q6()
    for n in range(1, 21):
        row = {}
        for g in GROUP_NAMES:
            An = np.linalg.matrix_power(or_mats[g].astype(float), n)
            row[g] = int(round(np.trace(An)))
        An_q6 = np.linalg.matrix_power(A_q6, n)
        row["Q6"] = int(round(np.trace(An_q6)))
        walk_counts[n] = row
        print(f"  {n:>3} | {row['比和']:>12} {row['生']:>12} {row['克']:>12} | {row['Q6']:>12}")

    results["1d"] = walk_counts

    return results


# ══════════════════════════════════════════════════════════════════
# PART 2: Transfer Matrices and φ
# ══════════════════════════════════════════════════════════════════

def part2(atlas, trig_mats, or_mats):
    print("\n" + "═" * 70)
    print("PART 2: TRANSFER MATRICES AND φ")
    print("═" * 70)
    results = {}

    # ── 2a: Trigram-level walk counts ──────────────────────────────
    print("\n── 2a. Trigram-Level Walk Counts ──")

    trig_walks = {}
    print(f"  {'n':>3} | {'比和 tr':>8} {'比和 Σ':>8} | {'生 tr':>8} {'生 Σ':>8} | {'克 tr':>8} {'克 Σ':>8}")
    print(f"  {'-'*3}-+-{'-'*8}-{'-'*8}-+-{'-'*8}-{'-'*8}-+-{'-'*8}-{'-'*8}")

    for n in range(1, 21):
        row = {}
        for g in GROUP_NAMES:
            Tn = np.linalg.matrix_power(trig_mats[g].astype(float), n)
            tr = int(round(np.trace(Tn)))
            total = int(round(Tn.sum()))
            row[g] = {"trace": tr, "total": total}
        trig_walks[n] = row
        print(f"  {n:>3} | {row['比和']['trace']:>8} {row['比和']['total']:>8} | "
              f"{row['生']['trace']:>8} {row['生']['total']:>8} | "
              f"{row['克']['trace']:>8} {row['克']['total']:>8}")

    results["2a"] = trig_walks

    # ── 2b: Recurrence verification ────────────────────────────────
    print("\n── 2b. Walk Count Recurrence Verification ──")

    # Lucas numbers: L_0=2, L_1=1, L_n = L_{n-1} + L_{n-2}
    lucas = [2, 1]
    for i in range(2, 25):
        lucas.append(lucas[-1] + lucas[-2])

    print("\n  克 trigram: tr(T^n) vs 4·L_n (even n) / 0 (odd n)")
    ke_match = True
    for n in range(1, 21):
        actual = trig_walks[n]["克"]["trace"]
        if n % 2 == 0:
            expected = 4 * lucas[n]
            match = actual == expected
            print(f"    n={n:2d}: tr={actual:>8}, 4·L_{n}={expected:>8}, match={match}")
        else:
            match = actual == 0
            print(f"    n={n:2d}: tr={actual:>8}, expected=0, match={match}")
        ke_match = ke_match and match
    print(f"  克 Lucas identity holds: {ke_match}")

    # 生 eigenvalues: ±√2 (×2) + 0 (×4)
    # tr(T^n) = 2(√2)^n + 2(-√2)^n = 2·2^(n/2)(1+(-1)^n) = 4·2^(n/2) for even n, 0 for odd
    print("\n  生 trigram: tr(T^n) vs 4·2^(n/2) (even n) / 0 (odd n)")
    sheng_match = True
    for n in range(1, 21):
        actual = trig_walks[n]["生"]["trace"]
        if n % 2 == 0:
            expected = int(round(4 * 2 ** (n / 2)))
            match = actual == expected
            print(f"    n={n:2d}: tr={actual:>8}, 4·2^({n//2})={expected:>8}, match={match}")
        else:
            match = actual == 0
            print(f"    n={n:2d}: tr={actual:>8}, expected=0, match={match}")
        sheng_match = sheng_match and match
    print(f"  生 identity holds: {sheng_match}")

    print("\n  比和 trigram: tr(T^n) vs 4 (even n) / 0 (odd n)")
    bihe_match = True
    for n in range(1, 21):
        actual = trig_walks[n]["比和"]["trace"]
        if n % 2 == 0:
            expected = 4
            match = actual == expected
        else:
            expected = 0
            match = actual == 0
        bihe_match = bihe_match and match
    print(f"  比和 identity holds: {bihe_match}")

    results["2b"] = {
        "ke_lucas": ke_match,
        "sheng_power2": sheng_match,
        "bihe_constant": bihe_match,
    }

    # ── 2c: Hexagram-level walk analysis ───────────────────────────
    print("\n── 2c. Hexagram-Level Walk Counts (OR-symmetrized) ──")

    hex_walks = {}
    print(f"  {'n':>3} | {'比和':>12} {'生':>12} {'克':>12}")
    print(f"  {'-'*3}-+-{'-'*12}-{'-'*12}-{'-'*12}")
    for n in range(1, 21):
        row = {}
        for g in GROUP_NAMES:
            An = np.linalg.matrix_power(or_mats[g].astype(float), n)
            row[g] = int(round(np.trace(An)))
        hex_walks[n] = row
        print(f"  {n:>3} | {row['比和']:>12} {row['生']:>12} {row['克']:>12}")

    # Check if 克 hexagram walks have any Fibonacci/Lucas structure
    ke_hex_traces = [hex_walks[n]["克"] for n in range(1, 21)]
    print(f"\n  克 hexagram closed walk sequence (n=2,4,...,20):")
    even_traces = [ke_hex_traces[n - 1] for n in range(2, 21, 2)]
    print(f"    {even_traces}")

    # Check ratios: should converge to ρ² = spectral_radius²
    rho_ke = spectral_radius(or_mats["克"])
    print(f"\n  克 OR spectral radius: ρ = {rho_ke:.6f}")
    print(f"  Successive ratios of even-n traces (should → ρ²={rho_ke**2:.4f}):")
    for i in range(1, len(even_traces)):
        if even_traces[i - 1] > 0:
            ratio = even_traces[i] / even_traces[i - 1]
            print(f"    N_{2*(i+1)}/N_{2*i} = {ratio:.6f}")

    # Check for linear recurrence
    print(f"\n  Testing linear recurrence for 克 hex even-n traces:")
    # For a graph with char poly of degree d, traces satisfy a linear recurrence of order d
    # But d=64 is too large. Instead check if ratios converge (they should to ρ²)

    results["2c"] = hex_walks

    # ── 2d: Characteristic polynomial of A_克^{OR} ─────────────────
    print("\n── 2d. Characteristic Polynomial of A_克^{OR} ──")

    A_ke = or_mats["克"].astype(float)
    char_coeffs = np.round(np.poly(A_ke)).astype(int)

    # Show degree and leading/trailing coefficients
    deg = len(char_coeffs) - 1
    print(f"  Degree: {deg}")
    print(f"  Leading 10 coefficients: {char_coeffs[:10].tolist()}")
    print(f"  Trailing 10 coefficients: {char_coeffs[-10:].tolist()}")

    # Check constant term = (-1)^64 * det(A) = det(A)
    det_A = int(round(np.linalg.det(A_ke)))
    print(f"  det(A_克^{{OR}}) = {det_A}")
    print(f"  Constant term of char poly = {char_coeffs[-1]}")

    # Check if eigenvalues include φ-related values
    eigs_ke = eigendecomp(A_ke)
    phi_eigs = [(v, m) for v, m in eigs_ke if any(abs(v - x) < 1e-6
                for x in [PHI, -PHI, 1/PHI, -1/PHI, PHI+1/PHI, -(PHI+1/PHI)])]
    print(f"\n  φ-related eigenvalues in A_克^{{OR}}:")
    for v, m in phi_eigs:
        # Identify
        for cand, label in [(PHI, "φ"), (-PHI, "-φ"), (1/PHI, "1/φ"),
                            (-1/PHI, "-1/φ"), (PHI**2, "φ²"), (-PHI**2, "-φ²"),
                            (3+PHI, "3+φ"), (-(3+PHI), "-(3+φ)"),
                            (2*PHI, "2φ"), (-2*PHI, "-2φ"),
                            (2+PHI, "2+φ"), (-(2+PHI), "-(2+φ)"),
                            (1+PHI, "1+φ"), (-(1+PHI), "-(1+φ)")]:
            if abs(v - cand) < 1e-6:
                print(f"    {v:.6f} ≈ {label} (×{m})")
                break
        else:
            print(f"    {v:.6f} (×{m})")

    # Check: 3.236068 ≈ 2+φ = 2+1.618 = 3.618? No.
    # 3.236068 ≈ 2φ = 3.236... yes!
    # And 1.236068 ≈ 2/φ? No, 2/φ = 2×0.618 = 1.236. Yes!
    print(f"\n  All eigenvalues with identification:")
    for v, m in sorted(eigs_ke):
        ident = ""
        for cand, label in [
            (0, "0"), (1, "1"), (-1, "-1"), (2, "2"), (-2, "-2"),
            (PHI, "φ"), (-PHI, "-φ"), (1/PHI, "1/φ"), (-1/PHI, "-1/φ"),
            (2*PHI, "2φ"), (-2*PHI, "-2φ"), (2/PHI, "2/φ"), (-2/PHI, "-2/φ"),
            (PHI**2, "φ²"), (-PHI**2, "-φ²"),
        ]:
            if abs(v - cand) < 1e-5:
                ident = f" = {label}"
                break
        print(f"    {v:12.6f}{ident}  (×{m})")

    results["2d"] = {
        "char_poly_leading": char_coeffs[:10].tolist(),
        "char_poly_trailing": char_coeffs[-10:].tolist(),
        "determinant": det_A,
    }

    return results


# ══════════════════════════════════════════════════════════════════
# PART 3: Stage vs Drama — Entropy Across Assignments
# ══════════════════════════════════════════════════════════════════

def generate_assignments():
    """Generate all distinct labeled assignments."""
    seen = {}
    for perm in permutations(ELEMENTS):
        elem_map = {
            0: perm[0], 4: perm[0],
            3: perm[1], 7: perm[1],
            1: perm[2], 6: perm[2],
            2: perm[3], 5: perm[4],
        }
        groups = {g: frozenset(h for h in range(64)
                    if wuxing_group(elem_map[h & 7], elem_map[(h >> 3) & 7]) == g)
                  for g in GROUP_NAMES}
        # Use unlabeled key: sorted set of group memberships
        unlabeled_key = tuple(sorted(tuple(sorted(s)) for s in groups.values()))

        if unlabeled_key not in seen:
            seen[unlabeled_key] = {
                "perm": list(perm),
                "elem_map": dict(elem_map),
                "groups": {g: sorted(s) for g, s in groups.items()},
                "sizes": {g: len(s) for g, s in groups.items()},
            }
    return list(seen.values())

def build_or_mats_from_assignment(asgn, transitions):
    """Build OR-symmetrized matrices for a given assignment."""
    elem_map = asgn["elem_map"]
    dir_mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}

    for t in transitions:
        s, d = t["source"], t["destination"]
        # Under this assignment, the source's type determines the directed edge label
        src_type = wuxing_group(elem_map[s & 7], elem_map[(s >> 3) & 7])
        dir_mats[src_type][s, d] = 1

    return {g: np.maximum(A, A.T) for g, A in dir_mats.items()}

def part3(atlas, transitions):
    print("\n" + "═" * 70)
    print("PART 3: STAGE VS DRAMA — ENTROPY ACROSS ASSIGNMENTS")
    print("═" * 70)
    results = {}

    actual_elems = get_trigram_elements(atlas)
    assignments = generate_assignments()

    print(f"\n  {len(assignments)} distinct unlabeled assignments")

    print(f"\n  {'#':>3} {'Perm':>35} | {'ρ_比':>6} {'ρ_生':>6} {'ρ_克':>6} | "
          f"{'h_比':>6} {'h_生':>6} {'h_克':>6} | {'gap_比':>6} {'gap_生':>6} {'gap_克':>6}")
    print(f"  {'-'*3} {'-'*35}-+-{'-'*6}-{'-'*6}-{'-'*6}-+-{'-'*6}-{'-'*6}-{'-'*6}-+-{'-'*6}-{'-'*6}-{'-'*6}")

    assignment_results = []
    for i, asgn in enumerate(assignments):
        is_actual = all(asgn["elem_map"].get(k) == actual_elems.get(k) for k in range(8))

        or_mats = build_or_mats_from_assignment(asgn, transitions)

        rhos = {}
        entropies = {}
        gaps = {}
        for g in GROUP_NAMES:
            rho = spectral_radius(or_mats[g])
            rhos[g] = rho
            entropies[g] = float(np.log(rho)) if rho > 1 else 0.0
            eigs = sorted([v for v, _ in eigendecomp(or_mats[g])], reverse=True)
            gaps[g] = eigs[0] - eigs[1] if len(eigs) >= 2 else 0.0

        marker = " ← ACTUAL" if is_actual else ""
        print(f"  {i+1:>3} {str(asgn['perm']):>35} | "
              f"{rhos['比和']:>6.3f} {rhos['生']:>6.3f} {rhos['克']:>6.3f} | "
              f"{entropies['比和']:>6.3f} {entropies['生']:>6.3f} {entropies['克']:>6.3f} | "
              f"{gaps['比和']:>6.3f} {gaps['生']:>6.3f} {gaps['克']:>6.3f}{marker}")

        assignment_results.append({
            "perm": asgn["perm"],
            "sizes": asgn["sizes"],
            "is_actual": is_actual,
            "spectral_radii": rhos,
            "entropies": entropies,
            "spectral_gaps": gaps,
        })

    # Analyze: is entropy ordering invariant?
    print("\n  ── Entropy Ordering Analysis ──")
    orderings = []
    for ar in assignment_results:
        ent = ar["entropies"]
        ordering = sorted(GROUP_NAMES, key=lambda g: -ent[g])
        orderings.append(tuple(ordering))
        marker = " ← ACTUAL" if ar["is_actual"] else ""
        print(f"    {ar['perm']}: {' > '.join(ordering)}{marker}")

    unique_orderings = set(orderings)
    print(f"\n  Distinct entropy orderings: {len(unique_orderings)}")
    print(f"  Entropy ordering invariant across assignments: {len(unique_orderings) == 1}")

    # Spectral gap ordering
    print("\n  ── Spectral Gap Ordering Analysis ──")
    gap_orderings = []
    for ar in assignment_results:
        gap = ar["spectral_gaps"]
        ordering = sorted(GROUP_NAMES, key=lambda g: -gap[g])
        gap_orderings.append(tuple(ordering))

    unique_gap_orderings = set(gap_orderings)
    print(f"  Distinct gap orderings: {len(unique_gap_orderings)}")

    results["assignments"] = assignment_results
    results["entropy_ordering_invariant"] = len(unique_orderings) == 1
    results["gap_ordering_invariant"] = len(unique_gap_orderings) == 1

    return results


# ══════════════════════════════════════════════════════════════════
# PART 4: Wood Exclusion Mechanism
# ══════════════════════════════════════════════════════════════════

def part4(atlas):
    print("\n" + "═" * 70)
    print("PART 4: ELEMENT REPRESENTATION IN 互 IMAGE")
    print("═" * 70)
    results = {}

    # The 互 image consists of 16 hexagrams
    hu_image = sorted(set(hu_formula(h) for h in range(64)))
    print(f"\n  互 image: {hu_image} (size {len(hu_image)})")

    # The hu image constraint: hex h is in image iff bit3=bit1 and bit4=bit2
    # This constrains which (lower, upper) trigram pairs can appear.
    # For lower L, upper U must have U_b0=L_b1, U_b1=L_b2, U_b2 free.
    print("\n  Structural constraint: h in 互-image iff bit3(h)=bit1(h) and bit4(h)=bit2(h)")

    # All 8 trigrams appear in both lower and upper positions
    lower_trigs = sorted(set(h & 7 for h in hu_image))
    upper_trigs = sorted(set((h >> 3) & 7 for h in hu_image))
    print(f"  Lower trigrams: {lower_trigs} (all 8)")
    print(f"  Upper trigrams: {upper_trigs} (all 8)")

    # But not all PAIRS appear: only 16 of 64 possible (lower, upper) pairs
    image_pairs = [(h & 7, (h >> 3) & 7) for h in hu_image]
    print(f"  Trigram pairs in image: {len(image_pairs)} of 64")

    # For each assignment: which element pairs appear in the image?
    assignments = generate_assignments()
    actual_elems = get_trigram_elements(atlas)

    print(f"\n  ── Element Pair Coverage in 互 Image ──")

    exclusion_results = []
    for i, asgn in enumerate(assignments):
        elem_map = asgn["elem_map"]
        is_actual = all(elem_map.get(k) == actual_elems.get(k) for k in range(8))

        # Element pairs in hu image
        elem_pairs = set()
        for h in hu_image:
            e_lower = elem_map[h & 7]
            e_upper = elem_map[(h >> 3) & 7]
            elem_pairs.add((e_lower, e_upper))

        # Types present in hu image
        image_types = Counter()
        for h in hu_image:
            g = wuxing_group(elem_map[h & 7], elem_map[(h >> 3) & 7])
            image_types[g] += 1

        # Which same-element pairs (比和 sources) appear?
        bihe_pairs = [(e1, e2) for e1, e2 in elem_pairs if e1 == e2]
        missing_bihe = [e for e in ELEMENTS if (e, e) not in elem_pairs]

        # Compute 互 transition matrix
        trans = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
        for h in range(64):
            src = wuxing_group(elem_map[h & 7], elem_map[(h >> 3) & 7])
            hu_h = hu_formula(h)
            dst = wuxing_group(elem_map[hu_h & 7], elem_map[(hu_h >> 3) & 7])
            trans[(src, dst)] += 1
        zeros = [f"{a}→{b}" for (a, b), v in trans.items() if v == 0]

        marker = " ← ACTUAL" if is_actual else ""
        print(f"\n  Assignment {i+1}{marker}: {asgn['perm']}")
        print(f"    Element pairs in image: {len(elem_pairs)} of 25")
        print(f"    比和 pairs present: {bihe_pairs}")
        print(f"    Missing 比和 elements: {missing_bihe}")
        print(f"    Image type distribution: {dict(sorted(image_types.items()))}")
        print(f"    Zero cells: {zeros if zeros else 'none'}")

        exclusion_results.append({
            "perm": asgn["perm"],
            "is_actual": is_actual,
            "n_elem_pairs": len(elem_pairs),
            "bihe_pairs": bihe_pairs,
            "missing_bihe_elements": missing_bihe,
            "image_type_dist": dict(image_types),
            "zero_cells": zeros,
            "has_zero_cell": len(zeros) > 0,
        })

    # Test hypothesis: zero cell iff certain element structure
    print("\n  ── Correlation: Zero Cell ↔ Image Type Imbalance ──")
    for er in exclusion_results:
        marker = " ← ACTUAL" if er["is_actual"] else ""
        img = er["image_type_dist"]
        min_type = min(img, key=img.get)
        min_count = img[min_type]
        print(f"    {er['perm']}: min_type={min_type}({min_count}), "
              f"missing_bihe={er['missing_bihe_elements']}, "
              f"zeros={er['zero_cells']}{marker}")

    # Check: does zero cell correlate with 生 being the minority type in the image?
    print("\n  ── Hypothesis: Zero cell ↔ Type with count ≤ 2 in image ──")
    for er in exclusion_results:
        img = er["image_type_dist"]
        has_minority = any(v <= 2 for v in img.values())
        match = er["has_zero_cell"] == has_minority
        print(f"    {er['perm']}: minority={has_minority}, zero={er['has_zero_cell']}, match={'✓' if match else '✗'}")

    hypothesis_holds = all(
        er["has_zero_cell"] == any(v <= 2 for v in er["image_type_dist"].values())
        for er in exclusion_results
    )
    print(f"\n  Hypothesis holds: {hypothesis_holds}")

    results["hu_image"] = hu_image
    results["exclusion_results"] = exclusion_results
    results["minority_hypothesis_holds"] = hypothesis_holds

    return results


# ── Main ───────────────────────────────────────────────────────────

def main():
    atlas = load_atlas()
    transitions = load_transitions()

    print("=" * 70)
    print("PROBES 4+5: SYMBOLIC DYNAMICS, TRANSFER MATRICES, STAGE VS DRAMA")
    print("=" * 70)

    # Build matrices
    dir_mats = build_directed_matrices(transitions)
    or_mats = build_or_symmetrized(dir_mats)
    and_mats = build_and_symmetrized(dir_mats)
    trig_elems = get_trigram_elements(atlas)
    trig_mats = build_trigram_matrices(trig_elems)

    r1 = part1(atlas, transitions, dir_mats, or_mats, and_mats)
    r2 = part2(atlas, trig_mats, or_mats)
    r3 = part3(atlas, transitions)
    r4 = part4(atlas)

    json_results = {"part1": r1, "part2": r2, "part3": r3, "part4": r4}

    out_path = HERE / "p45_results.json"
    with open(out_path, "w") as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
