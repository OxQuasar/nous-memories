"""
Probe 5: Composability and Sequential Resolution (R6)

Tests whether the I Ching's transition structure preserves information
across multiple steps. Arena → rapid decorrelation. Specific referent →
structure-preserving composition.
"""

import json
import numpy as np
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"
DYNAMICS_DIR = HERE.parent / "dynamics"

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]
SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}

EPS = 1e-8
MAX_STEP = 20

# ── Data Loading ───────────────────────────────────────────────────

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
    """互 (mutual/nuclear trigram) transform."""
    b = [(h >> i) & 1 for i in range(6)]
    return b[1] | (b[2] << 1) | (b[3] << 2) | (b[2] << 3) | (b[3] << 4) | (b[4] << 5)

def build_directed_matrices(transitions):
    mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = RELATION_GROUPS[t["tiyong_relation"]]
        mats[g][t["source"], t["destination"]] = 1
    return mats

def build_full_directed(transitions):
    """Full adjacency matrix (all 384 edges)."""
    A = np.zeros((64, 64), dtype=int)
    for t in transitions:
        A[t["source"], t["destination"]] = 1
    return A

def build_or_symmetrized(dir_mats):
    return {g: np.maximum(A, A.T) for g, A in dir_mats.items()}

# ══════════════════════════════════════════════════════════════════
# PART 1: n-step Type Flow Matrices
# ══════════════════════════════════════════════════════════════════

def part1_type_flow(atlas, transitions):
    print("=" * 70)
    print("PART 1: n-STEP TRANSITION TYPE PRESERVATION")
    print("=" * 70)

    A = build_full_directed(transitions)
    vtypes = [vertex_type(atlas, h) for h in range(64)]
    type_counts = Counter(vtypes)
    print(f"  Vertex types: {dict(type_counts)}")

    # Type indices
    type_idx = {g: [h for h in range(64) if vtypes[h] == g] for g in GROUP_NAMES}

    results = {}
    An = np.eye(64, dtype=float)

    # Stationary distribution of the full graph
    # Row-normalize A to get transition probability matrix
    A_float = A.astype(float)
    row_sums = A_float.sum(axis=1)
    row_sums[row_sums == 0] = 1  # avoid division by zero
    P = A_float / row_sums[:, None]

    # Compute stationary distribution via eigenvalue
    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigvals - 1.0))
    pi = np.abs(eigvecs[:, idx].real)
    pi /= pi.sum()

    # Stationary type distribution
    pi_type = {g: sum(pi[h] for h in type_idx[g]) for g in GROUP_NAMES}
    print(f"  Stationary type distribution: " +
          ", ".join(f"{g}={pi_type[g]:.4f}" for g in GROUP_NAMES))

    mixing_time = None

    for n in range(MAX_STEP + 1):
        if n > 0:
            An = An @ A_float

        # Build 3×3 type flow matrix M(n)
        M = np.zeros((3, 3))
        for gi, g1 in enumerate(GROUP_NAMES):
            for gj, g2 in enumerate(GROUP_NAMES):
                for i in type_idx[g1]:
                    for j in type_idx[g2]:
                        M[gi, gj] += An[i, j]

        # Normalize to row-stochastic
        row_totals = M.sum(axis=1)
        row_totals[row_totals == 0] = 1
        Pn = M / row_totals[:, None]

        # Total variation from stationary
        pi_vec = np.array([pi_type[g] for g in GROUP_NAMES])
        tv = max(0.5 * np.abs(Pn[i] - pi_vec).sum() for i in range(3))

        if n <= 5 or n % 5 == 0:
            print(f"\n  Step {n}: TV distance = {tv:.6f}")
            for gi, g1 in enumerate(GROUP_NAMES):
                print(f"    {g1} → " + "  ".join(f"{g2}={Pn[gi,gj]:.4f}"
                      for gj, g2 in enumerate(GROUP_NAMES)))

        if mixing_time is None and tv < 0.01 and n > 0:
            mixing_time = n

        results[n] = {
            "type_flow": Pn.tolist(),
            "tv_distance": float(tv),
            "total_paths": float(An.sum()),
        }

    if mixing_time is None:
        mixing_time = -1  # didn't mix within MAX_STEP
    print(f"\n  Mixing time (TV < 0.01): {mixing_time}")

    return {"steps": results, "mixing_time": mixing_time,
            "stationary": pi_type}


# ══════════════════════════════════════════════════════════════════
# PART 2: Per-Type Composition (Subgraph Powers)
# ══════════════════════════════════════════════════════════════════

def part2_per_type_composition(atlas, transitions):
    print("\n" + "=" * 70)
    print("PART 2: PER-TYPE SUBGRAPH COMPOSITION")
    print("=" * 70)

    dir_mats = build_directed_matrices(transitions)
    or_mats = build_or_symmetrized(dir_mats)
    vtypes = [vertex_type(atlas, h) for h in range(64)]

    results = {}

    for g in GROUP_NAMES:
        print(f"\n  ── {g} (OR-symmetrized) ──")
        A = or_mats[g].astype(float)

        for n in range(1, 7):
            An = np.linalg.matrix_power(A, n)
            n_nonzero = int((An > EPS).sum())
            # Classify nonzero entries by vertex types
            same_type = 0
            diff_type = 0
            for i in range(64):
                for j in range(64):
                    if An[i, j] > EPS:
                        if vtypes[i] == vtypes[j]:
                            same_type += 1
                        else:
                            diff_type += 1
            total = same_type + diff_type
            frac_same = same_type / total if total > 0 else 0

            if n <= 4:
                print(f"    A^{n}: nonzero={n_nonzero}, same_type={frac_same:.4f}")

            if g not in results:
                results[g] = {}
            results[g][n] = {
                "nonzero_entries": n_nonzero,
                "fraction_same_type": float(frac_same),
            }

        # Mutual information: I(type_start; type_end | n steps on g)
        print(f"    Mutual information I(start_type; end_type | n):")
        for n in range(1, 7):
            An = np.linalg.matrix_power(A, n)
            # Joint distribution P(type_i, type_j) over reachable pairs
            joint = np.zeros((3, 3))
            for i in range(64):
                for j in range(64):
                    if An[i, j] > EPS:
                        gi = GROUP_NAMES.index(vtypes[i])
                        gj = GROUP_NAMES.index(vtypes[j])
                        joint[gi, gj] += An[i, j]
            total = joint.sum()
            if total == 0:
                continue
            joint /= total
            marg_i = joint.sum(axis=1)
            marg_j = joint.sum(axis=0)

            mi = 0.0
            for a in range(3):
                for b in range(3):
                    if joint[a, b] > EPS and marg_i[a] > EPS and marg_j[b] > EPS:
                        mi += joint[a, b] * np.log2(joint[a, b] / (marg_i[a] * marg_j[b]))

            if n <= 4:
                print(f"      n={n}: I = {mi:.6f} bits")
            results[g][n]["mutual_info_bits"] = float(mi)

    return results


# ══════════════════════════════════════════════════════════════════
# PART 3: Eigenvalue Composition (Coherent/Dark Under Powers)
# ══════════════════════════════════════════════════════════════════

def part3_eigenvalue_composition(transitions):
    print("\n" + "=" * 70)
    print("PART 3: EIGENVALUE COMPOSITION (COHERENT/DARK UNDER POWERS)")
    print("=" * 70)

    dir_mats = build_directed_matrices(transitions)
    or_mats = build_or_symmetrized(dir_mats)

    # Load trigram eigenvalues from p1_results
    with open(DYNAMICS_DIR / "p1_results.json") as f:
        p1 = json.load(f)

    results = {}

    for g in GROUP_NAMES:
        A = or_mats[g].astype(float)
        eigvals, eigvecs = np.linalg.eigh(A)

        # Trigram eigenvalues → coherent candidates
        trig_eigs = p1["trigram"]["eigenvalues"][g]
        trig_vals = []
        for e in trig_eigs:
            trig_vals.extend([e["value"]] * e["multiplicity"])
        coherent_cands = sorted([a + b for a in trig_vals for b in trig_vals])

        # Match
        eigvals_sorted = sorted(eigvals)
        cands_sorted = sorted(coherent_cands)
        coherent_idx = set()
        ci = 0
        for ei, ev in enumerate(eigvals_sorted):
            while ci < len(cands_sorted) and cands_sorted[ci] < ev - 1e-5:
                ci += 1
            if ci < len(cands_sorted) and abs(ev - cands_sorted[ci]) < 1e-5:
                coherent_idx.add(ei)
                ci += 1

        dark_idx = set(range(64)) - coherent_idx
        coh_vals = [eigvals_sorted[i] for i in sorted(coherent_idx)]
        dark_vals = [eigvals_sorted[i] for i in sorted(dark_idx)]

        rho_coh = max(abs(v) for v in coh_vals) if coh_vals else 0
        rho_dark = max(abs(v) for v in dark_vals) if dark_vals else 0

        print(f"\n  ── {g}: ρ_coh={rho_coh:.4f}, ρ_dark={rho_dark:.4f} ──")

        # For A^n: eigenvalues are λ^n. Track when dark spectral radius exceeds coherent.
        crossover = None
        for n in range(1, 21):
            rho_coh_n = rho_coh ** n
            rho_dark_n = rho_dark ** n
            ratio = rho_dark_n / rho_coh_n if rho_coh_n > EPS else float('inf')
            if n <= 5:
                print(f"    A^{n}: ρ_coh^n = {rho_coh_n:.4f}, ρ_dark^n = {rho_dark_n:.4f}, ratio = {ratio:.4f}")
            if crossover is None and ratio > 1 and n >= 1:
                crossover = n

        # Eigenvector persistence: eigenvectors of A^n are SAME as A (since they commute)
        # So the coherent/dark decomposition is IDENTICAL for all powers.
        print(f"    Eigenvectors: IDENTICAL for all powers (A^n and A share eigenbasis)")
        print(f"    Dark spectral radius dominates from step n={crossover}")

        results[g] = {
            "rho_coherent": float(rho_coh),
            "rho_dark": float(rho_dark),
            "dark_dominates_from": crossover if crossover else 1,
            "eigenvectors_preserved": True,
            "coherent_eigenvalues": [float(v) for v in coh_vals],
            "dark_eigenvalues": [float(v) for v in dark_vals],
        }

    return results


# ══════════════════════════════════════════════════════════════════
# PART 4: 互 Composition Interaction
# ══════════════════════════════════════════════════════════════════

def part4_hu_interaction(atlas, transitions):
    print("\n" + "=" * 70)
    print("PART 4: 互 COMPOSITION INTERACTION")
    print("=" * 70)

    A = build_full_directed(transitions)

    # For each directed edge h→h': compare 互(h') vs transitions from 互(h)
    # Path A: h → h' → 互(h')
    # Path B: h → 互(h) → neighbors of 互(h)
    # Question: is 互(h') reachable from 互(h)?

    reachable_count = 0
    not_reachable_count = 0
    type_preserved_count = 0
    type_changed_count = 0
    total_edges = 0

    # Neighbors of each vertex in full directed graph
    neighbors = {h: set(np.where(A[h] > 0)[0]) for h in range(64)}

    vtypes = [vertex_type(atlas, h) for h in range(64)]

    detail_by_type = {g: {"reachable": 0, "not_reachable": 0} for g in GROUP_NAMES}

    for t in transitions:
        src, dst = t["source"], t["destination"]
        g = RELATION_GROUPS[t["tiyong_relation"]]
        total_edges += 1

        hu_dst = hu_formula(dst)   # 互(h')
        hu_src = hu_formula(src)   # 互(h)

        # Is 互(h') reachable from 互(h)?
        nbrs_hu_src = neighbors[hu_src]
        if hu_dst in nbrs_hu_src:
            reachable_count += 1
            detail_by_type[g]["reachable"] += 1
        else:
            not_reachable_count += 1
            detail_by_type[g]["not_reachable"] += 1

        # Type preservation: does 互 preserve 五行 type?
        if vtypes[src] == vtypes[hu_src]:
            type_preserved_count += 1
        else:
            type_changed_count += 1

    frac_reachable = reachable_count / total_edges
    frac_type_preserved = type_preserved_count / total_edges

    print(f"  Total directed edges: {total_edges}")
    print(f"  互(transition) reachable from transition(互): {reachable_count}/{total_edges} = {frac_reachable:.4f}")
    print(f"  互 preserves vertex type: {type_preserved_count}/{total_edges} = {frac_type_preserved:.4f}")

    print(f"\n  By transition type:")
    for g in GROUP_NAMES:
        d = detail_by_type[g]
        total_g = d["reachable"] + d["not_reachable"]
        frac = d["reachable"] / total_g if total_g > 0 else 0
        print(f"    {g}: reachable {d['reachable']}/{total_g} = {frac:.4f}")

    # Also check: does 互 commute with transitions at the matrix level?
    # Build 互 permutation matrix
    H = np.zeros((64, 64), dtype=int)
    for h in range(64):
        H[hu_formula(h), h] = 1

    comm = A @ H - H @ A
    comm_norm = np.linalg.norm(comm, 'fro')
    print(f"\n  Commutator ||AH - HA||_F = {comm_norm:.4f}")
    print(f"  互 and transitions commute: {comm_norm < EPS}")

    # How many fixed points does 互 have?
    fixed = sum(1 for h in range(64) if hu_formula(h) == h)
    print(f"  互 fixed points: {fixed}/64")

    # 互 orbits
    visited = set()
    orbit_sizes = []
    for h in range(64):
        if h in visited:
            continue
        orbit = set()
        cur = h
        while cur not in orbit:
            orbit.add(cur)
            cur = hu_formula(cur)
        visited |= orbit
        orbit_sizes.append(len(orbit))
    orbit_sizes.sort(reverse=True)
    print(f"  互 orbit sizes: {orbit_sizes}")

    return {
        "fraction_reachable": float(frac_reachable),
        "fraction_type_preserved": float(frac_type_preserved),
        "commutator_norm": float(comm_norm),
        "commutes": bool(comm_norm < EPS),
        "by_type": {g: detail_by_type[g] for g in GROUP_NAMES},
        "hu_fixed_points": fixed,
        "hu_orbit_sizes": orbit_sizes,
    }


# ══════════════════════════════════════════════════════════════════
# PART 5: Information Loss per Step
# ══════════════════════════════════════════════════════════════════

def part5_information_loss(atlas, transitions):
    print("\n" + "=" * 70)
    print("PART 5: INFORMATION LOSS PER STEP")
    print("=" * 70)

    A = build_full_directed(transitions).astype(float)
    vtypes = [vertex_type(atlas, h) for h in range(64)]
    type_idx = {g: np.array([h for h in range(64) if vtypes[h] == g]) for g in GROUP_NAMES}

    # Row-normalize to get transition probabilities
    row_sums = A.sum(axis=1)
    row_sums[row_sums == 0] = 1
    P = A / row_sums[:, None]

    results = {}

    for g in GROUP_NAMES:
        # Start from uniform distribution over type g
        p0 = np.zeros(64)
        idx = type_idx[g]
        p0[idx] = 1.0 / len(idx)

        entropies = []
        type_probs_history = []
        pn = p0.copy()

        for n in range(MAX_STEP + 1):
            if n > 0:
                pn = pn @ P

            # Type probabilities
            type_probs = {g2: float(pn[type_idx[g2]].sum()) for g2 in GROUP_NAMES}

            # Entropy over types
            probs = np.array([type_probs[g2] for g2 in GROUP_NAMES])
            probs = probs[probs > EPS]
            H = -float(np.sum(probs * np.log2(probs)))

            entropies.append(H)
            type_probs_history.append(type_probs)

            if n <= 5 or n == 10 or n == 20:
                print(f"  {g} → step {n}: H = {H:.6f} bits, " +
                      ", ".join(f"{g2}={type_probs[g2]:.4f}" for g2 in GROUP_NAMES))

        # Rate of entropy increase (bits per step in first 5 steps)
        if len(entropies) > 1:
            rates = [entropies[i+1] - entropies[i] for i in range(min(5, len(entropies)-1))]
            avg_rate = np.mean(rates)
        else:
            avg_rate = 0

        # Steps to reach 95% of max entropy
        max_H = np.log2(3)
        steps_to_95 = next((n for n, H in enumerate(entropies) if H > 0.95 * max_H), -1)

        results[g] = {
            "entropies": [float(h) for h in entropies],
            "avg_rate_first5": float(avg_rate),
            "steps_to_95pct": steps_to_95,
            "type_probs": type_probs_history,
        }
        print(f"  {g}: avg rate (first 5) = {avg_rate:.6f} bits/step, "
              f"steps to 95% max entropy = {steps_to_95}")
        print()

    return results


# ══════════════════════════════════════════════════════════════════
# PART 6: Arena Diagnostic (Autocorrelation Decay)
# ══════════════════════════════════════════════════════════════════

def part6_arena_diagnostic(atlas, transitions):
    print("=" * 70)
    print("PART 6: ARENA DIAGNOSTIC (AUTOCORRELATION DECAY)")
    print("=" * 70)

    A = build_full_directed(transitions).astype(float)
    vtypes = [vertex_type(atlas, h) for h in range(64)]
    type_idx = {g: np.array([h for h in range(64) if vtypes[h] == g]) for g in GROUP_NAMES}

    # KEY STRUCTURAL FACT: the full transition graph IS Q₆.
    # Every hexagram has exactly 6 neighbors (one per bit flip).
    # The 五行 labels classify edges but don't affect connectivity.
    print(f"  Full transition graph IS Q₆ (all {int(A.sum())} = 64×6 single-bit-flip edges)")

    # The graph is BIPARTITE (period 2): each transition flips parity.
    # Use the LAZY chain P_lazy = (I + P)/2 to remove periodicity.
    row_sums = A.sum(axis=1)
    row_sums[row_sums == 0] = 1
    P = A / row_sums[:, None]
    P_lazy = (np.eye(64) + P) / 2

    # Stationary distribution (uniform for regular graph)
    pi = np.ones(64) / 64
    pi_type = {g: float(pi[type_idx[g]].sum()) for g in GROUP_NAMES}

    # Spectral analysis of lazy chain
    # Q₆ adjacency eigenvalues: 6-2k for k=0,...,6, mult C(6,k)
    # P = A/6, so P eigenvalues: 1-k/3 for k=0,...,6
    # P_lazy = (I+P)/2, so eigenvalues: (1 + 1-k/3)/2 = 1 - k/6
    # Second eigenvalue: k=1 → 5/6, mult C(6,1)=6
    eigvals_lazy = np.linalg.eigvals(P_lazy)
    eig_sorted = sorted(np.abs(eigvals_lazy), reverse=True)
    spectral_gap = 1.0 - eig_sorted[1]
    print(f"\n  Lazy chain spectral gap: {spectral_gap:.6f} (= 1/6 for Q₆)")
    print(f"  Second eigenvalue: {eig_sorted[1]:.6f} (= 5/6)")
    print(f"  Predicted mixing time ~ 1/gap = {1/spectral_gap:.2f} steps")

    results = {"spectral_gap": float(spectral_gap),
               "second_eigenvalue": float(eig_sorted[1]),
               "predicted_mixing_time": float(1/spectral_gap),
               "graph_is_Q6": True}

    # Autocorrelation on LAZY chain (removes bipartite oscillation)
    for g in GROUP_NAMES:
        idx_g = type_idx[g]
        p0 = np.zeros(64)
        p0[idx_g] = 1.0 / len(idx_g)

        autocorr = []
        pn = p0.copy()
        for n in range(MAX_STEP + 1):
            if n > 0:
                pn = pn @ P_lazy
            prob_g = float(pn[idx_g].sum())
            C = prob_g - pi_type[g]
            autocorr.append(C)

        # Fit exponential decay
        valid = [(n, c) for n, c in enumerate(autocorr) if n > 0 and abs(c) > 1e-8]
        if len(valid) >= 2:
            ns = np.array([v[0] for v in valid])
            log_c = np.log(np.abs([v[1] for v in valid]))
            coeffs = np.polyfit(ns, log_c, 1)
            tau = -1.0 / coeffs[0] if abs(coeffs[0]) > EPS else float('inf')
        else:
            tau = float('inf')

        print(f"\n  {g}: C(0)={autocorr[0]:.4f}, τ={tau:.4f}, π(g)={pi_type[g]:.4f}")
        print(f"    First 8: {[f'{c:.6f}' for c in autocorr[:8]]}")

        results[g] = {
            "autocorrelation": [float(c) for c in autocorr],
            "decay_time_tau": float(tau),
            "stationary_prob": float(pi_type[g]),
        }

    # Arena verdict
    print(f"\n  ── ARENA DIAGNOSTIC ──")
    taus = [results[g]["decay_time_tau"] for g in GROUP_NAMES]
    avg_tau = np.mean(taus)
    print(f"  Decay times: " + ", ".join(f"{g}={results[g]['decay_time_tau']:.2f}" for g in GROUP_NAMES))
    print(f"  Average decay time: {avg_tau:.4f} steps")
    print(f"  Spectral gap prediction: {1/spectral_gap:.2f} steps")

    if avg_tau < 3:
        verdict = "rapid_decorrelation"
        print(f"  VERDICT: RAPID DECORRELATION — consistent with arena interpretation")
    elif avg_tau < 10:
        verdict = "moderate_persistence"
        print(f"  VERDICT: MODERATE PERSISTENCE — ambiguous")
    else:
        verdict = "slow_mixing"
        print(f"  VERDICT: SLOW MIXING — suggests referent structure")

    results["verdict"] = verdict
    results["avg_tau"] = float(avg_tau)

    return results


# ══════════════════════════════════════════════════════════════════
# PART 7: Directed vs OR-symmetrized Comparison
# ══════════════════════════════════════════════════════════════════

def part7_directed_vs_symmetric(atlas, transitions):
    print("\n" + "=" * 70)
    print("PART 7: DIRECTED vs OR-SYMMETRIZED COMPARISON")
    print("=" * 70)

    dir_mats = build_directed_matrices(transitions)
    or_mats = build_or_symmetrized(dir_mats)
    vtypes = [vertex_type(atlas, h) for h in range(64)]
    type_idx = {g: np.array([h for h in range(64) if vtypes[h] == g]) for g in GROUP_NAMES}

    results = {}

    for g in GROUP_NAMES:
        A_dir = dir_mats[g].astype(float)
        A_sym = or_mats[g].astype(float)

        # Compare mixing on directed vs symmetric
        # Directed: row-normalize
        rs = A_dir.sum(axis=1)
        rs[rs == 0] = 1
        P_dir = A_dir / rs[:, None]

        # Symmetric: row-normalize
        rs2 = A_sym.sum(axis=1)
        rs2[rs2 == 0] = 1
        P_sym = A_sym / rs2[:, None]

        # Information loss comparison
        idx_g = type_idx[g]
        p0 = np.zeros(64)
        p0[idx_g] = 1.0 / len(idx_g)

        for label, Pm in [("directed", P_dir), ("symmetric", P_sym)]:
            pn = p0.copy()
            entropies = []
            for n in range(11):
                if n > 0:
                    pn = pn @ Pm
                type_probs = np.array([float(pn[type_idx[g2]].sum()) for g2 in GROUP_NAMES])
                type_probs = type_probs[type_probs > EPS]
                H = -float(np.sum(type_probs * np.log2(type_probs)))
                entropies.append(H)

            max_H = np.log2(3)
            steps_to_90 = next((n for n, H in enumerate(entropies) if H > 0.90 * max_H), -1)

            if g not in results:
                results[g] = {}
            results[g][label] = {
                "entropy_at_5": float(entropies[5]) if len(entropies) > 5 else 0,
                "steps_to_90pct": steps_to_90,
            }

        print(f"  {g}:")
        for label in ["directed", "symmetric"]:
            r = results[g][label]
            print(f"    {label:10s}: H(5)={r['entropy_at_5']:.4f}, steps_to_90%={r['steps_to_90pct']}")

    return results


# ── Main ──────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("PROBE 5: COMPOSABILITY AND SEQUENTIAL RESOLUTION")
    print("=" * 70)

    atlas = load_atlas()
    transitions = load_transitions()

    r1 = part1_type_flow(atlas, transitions)
    r2 = part2_per_type_composition(atlas, transitions)
    r3 = part3_eigenvalue_composition(transitions)
    r4 = part4_hu_interaction(atlas, transitions)
    r5 = part5_information_loss(atlas, transitions)
    r6 = part6_arena_diagnostic(atlas, transitions)
    r7 = part7_directed_vs_symmetric(atlas, transitions)

    all_results = {
        "part1_type_flow": {"mixing_time": r1["mixing_time"],
                            "stationary": r1["stationary"]},
        "part2_per_type": r2,
        "part3_eigenvalue_composition": r3,
        "part4_hu_interaction": r4,
        "part5_information_loss": {g: {"entropies": r5[g]["entropies"],
                                        "avg_rate_first5": r5[g]["avg_rate_first5"],
                                        "steps_to_95pct": r5[g]["steps_to_95pct"]}
                                    for g in GROUP_NAMES},
        "part6_arena_diagnostic": {
            "spectral_gap": r6["spectral_gap"],
            "second_eigenvalue": r6["second_eigenvalue"],
            "avg_tau": r6["avg_tau"],
            "verdict": r6["verdict"],
            "by_type": {g: {"decay_time_tau": r6[g]["decay_time_tau"],
                           "stationary_prob": r6[g]["stationary_prob"]}
                       for g in GROUP_NAMES},
        },
        "part7_directed_vs_symmetric": r7,
    }

    out_path = HERE / "composability_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
