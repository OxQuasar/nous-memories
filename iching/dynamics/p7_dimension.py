"""
Probe 7: Spectral Dimension + Dimensional Synthesis

Part 1: Spectral dimension from return probabilities
Part 2: Effective dimension of each 五行 subgraph
Part 3: Dimensional comparison to the ~16-dim manifold
Part 4: Summary table
"""

import json
import math
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

GROUP_NAMES = ["比和", "生", "克"]
PHI = (1 + 5**0.5) / 2

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}

# ── Loading ────────────────────────────────────────────────────────

def load_p1():
    with open(HERE / "p1_results.json") as f:
        return json.load(f)

def load_p45():
    with open(HERE / "p45_results.json") as f:
        return json.load(f)

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def load_transitions():
    with open(ATLAS_DIR / "transitions.json") as f:
        return json.load(f)["bian_fan"]

def build_q6():
    A = np.zeros((64, 64), dtype=int)
    for i in range(64):
        for bit in range(6):
            A[i, i ^ (1 << bit)] = 1
    return A

def build_or_symmetrized(transitions):
    dir_mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = RELATION_GROUPS[t["tiyong_relation"]]
        dir_mats[g][t["source"], t["destination"]] = 1
    return {g: np.maximum(A, A.T) for g, A in dir_mats.items()}

def eigendecomp(A):
    eigvals = np.linalg.eigh(A.astype(float))[0]
    rounded = np.round(eigvals, 8)
    unique, counts = np.unique(rounded, return_counts=True)
    return [(float(v), int(c)) for v, c in zip(unique, counts)]

def get_trigram_elements(atlas):
    elems = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            elems[t["val"]] = t["element"]
    return elems

SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}

def wuxing_group(e1, e2):
    if e1 == e2: return "比和"
    if SHENG[e1] == e2 or SHENG[e2] == e1: return "生"
    return "克"

def build_trigram_matrices(trigram_elements):
    mats = {g: np.zeros((8, 8), dtype=int) for g in GROUP_NAMES}
    for a in range(8):
        for bit in range(3):
            b = a ^ (1 << bit)
            if b <= a:
                continue
            g = wuxing_group(trigram_elements[a], trigram_elements[b])
            mats[g][a, b] = 1
            mats[g][b, a] = 1
    return mats


# ── Part 1: Spectral Dimension ────────────────────────────────────

def spectral_dimension_from_walks(walk_counts, N, rho, label=""):
    """
    Compute spectral dimension from return probability scaling.
    P(n) = tr(A^n) / (N * rho^n) ~ n^{-d_s/2}
    log P(n) = -d_s/2 * log(n) + const
    """
    even_n = sorted([int(n) for n in walk_counts.keys() if int(n) % 2 == 0 and walk_counts[n] > 0])

    if len(even_n) < 3:
        return None, [], []

    log_n = []
    log_p = []
    for n in even_n:
        Nn = walk_counts[n]
        if Nn <= 0:
            continue
        p_n = Nn / (N * rho ** n)
        if p_n > 0:
            log_n.append(np.log(n))
            log_p.append(np.log(p_n))

    if len(log_n) < 3:
        return None, log_n, log_p

    # Linear fit: log_p = slope * log_n + intercept
    # d_s = -2 * slope
    log_n = np.array(log_n)
    log_p = np.array(log_p)
    slope, intercept = np.polyfit(log_n, log_p, 1)
    d_s = -2 * slope

    return d_s, log_n.tolist(), log_p.tolist()


def spectral_dimension_exact(eigenvalues, rho):
    """
    Compute return probability from eigenvalue sum directly.
    P(n) = (1/N) * sum_i (lambda_i / rho)^n
    """
    # Expand eigenvalues
    all_eigs = []
    for v, m in eigenvalues:
        all_eigs.extend([v] * m)
    N = len(all_eigs)

    results = {}
    for n in range(2, 42, 2):
        p_n = sum((lam / rho) ** n for lam in all_eigs) / N
        results[n] = float(p_n)
    return results


def part1(p1, p45, transitions):
    print("\n" + "═" * 70)
    print("PART 1: SPECTRAL DIMENSION FROM RETURN PROBABILITIES")
    print("═" * 70)
    results = {}

    atlas = load_atlas()
    trig_elems = get_trigram_elements(atlas)
    or_mats = build_or_symmetrized(transitions)
    trig_mats = build_trigram_matrices(trig_elems)
    A_q6 = build_q6()

    # ── Hexagram-level spectral dimensions ─────────────────────────
    print("\n── Hexagram-Level (64 vertices, OR-symmetrized) ──")

    # Get walk counts from p45
    walk_data_hex = {}
    for n_str, counts in p45["part1"]["1d"].items():
        n = int(n_str)
        for g in GROUP_NAMES + ["Q6"]:
            walk_data_hex.setdefault(g, {})[n] = counts[g]

    # Get spectral radii from eigenvalues
    hex_rhos = {}
    for g in GROUP_NAMES:
        eigs = p1["or_symmetrized"]["eigenvalues"][g]
        hex_rhos[g] = max(e["value"] for e in eigs)
    hex_rhos["Q6"] = 6.0

    print(f"\n  {'Subgraph':>10} | {'ρ':>8} | {'d_s (fit)':>10} | N=64")
    print(f"  {'-'*10}-+-{'-'*8}-+-{'-'*10}-+-----")

    hex_dims = {}
    for g in GROUP_NAMES + ["Q6"]:
        d_s, log_n, log_p = spectral_dimension_from_walks(
            walk_data_hex[g], 64, hex_rhos[g], g
        )
        hex_dims[g] = d_s
        d_s_str = f"{d_s:.4f}" if d_s is not None else "N/A"
        print(f"  {g:>10} | {hex_rhos[g]:>8.4f} | {d_s_str:>10} |")

    # Exact return probabilities for longer range
    print("\n  Exact return probabilities (from eigenvalues) for extended range:")
    exact_returns = {}
    for g in GROUP_NAMES:
        eigs = [(e["value"], e["multiplicity"]) for e in p1["or_symmetrized"]["eigenvalues"][g]]
        exact = spectral_dimension_exact(eigs, hex_rhos[g])
        exact_returns[g] = exact

    # Q₆ exact
    q6_eigs = [(6 - 2*k, int(round(math.comb(6, k)))) for k in range(7)]
    exact_returns["Q6"] = spectral_dimension_exact(q6_eigs, 6.0)

    print(f"\n  {'n':>4} | {'P_比和(n)':>12} {'P_生(n)':>12} {'P_克(n)':>12} {'P_Q₆(n)':>12}")
    print(f"  {'-'*4}-+-{'-'*12}-{'-'*12}-{'-'*12}-{'-'*12}")
    for n in range(2, 42, 2):
        vals = [exact_returns[g].get(n, 0) for g in GROUP_NAMES + ["Q6"]]
        print(f"  {n:>4} | {vals[0]:>12.8f} {vals[1]:>12.8f} {vals[2]:>12.8f} {vals[3]:>12.8f}")

    # Refit with extended range
    print("\n  Spectral dimension from extended exact return probabilities (n=2..40):")
    extended_dims = {}
    for g in GROUP_NAMES + ["Q6"]:
        log_n = [np.log(n) for n in range(2, 42, 2)]
        log_p = [np.log(exact_returns[g][n]) for n in range(2, 42, 2) if exact_returns[g][n] > 0]
        log_n = log_n[:len(log_p)]
        if len(log_n) >= 3:
            slope, _ = np.polyfit(log_n, log_p, 1)
            d_s = -2 * slope
            extended_dims[g] = d_s
            print(f"    {g:>10}: d_s = {d_s:.4f}")
        else:
            extended_dims[g] = None
            print(f"    {g:>10}: insufficient data")

    # ── Trigram-level spectral dimensions ──────────────────────────
    print("\n── Trigram-Level (8 vertices) ──")

    trig_rhos = {}
    trig_exact = {}
    for g in GROUP_NAMES:
        eigs = [(e["value"], e["multiplicity"]) for e in p1["trigram"]["eigenvalues"][g]]
        rho = max(e["value"] for e in p1["trigram"]["eigenvalues"][g])
        trig_rhos[g] = rho
        trig_exact[g] = spectral_dimension_exact(eigs, rho)

    # Q₃ for reference
    q3_eigs = [(3 - 2*k, int(round(math.comb(3, k)))) for k in range(4)]
    trig_rhos["Q3"] = 3.0
    trig_exact["Q3"] = spectral_dimension_exact(q3_eigs, 3.0)

    trig_dims = {}
    for g in list(GROUP_NAMES) + ["Q3"]:
        log_n = [np.log(n) for n in range(2, 42, 2)]
        log_p = [np.log(trig_exact[g][n]) for n in range(2, 42, 2) if trig_exact[g][n] > 0]
        log_n = log_n[:len(log_p)]
        if len(log_n) >= 3:
            slope, _ = np.polyfit(log_n, log_p, 1)
            d_s = -2 * slope
            trig_dims[g] = d_s
            print(f"    {g:>10}: d_s = {d_s:.4f} (ρ = {trig_rhos[g]:.4f})")
        else:
            trig_dims[g] = None
            print(f"    {g:>10}: insufficient data")

    # ── Analytic comparison ────────────────────────────────────────
    print("\n── Analytic Check ──")
    # For Q_d, the spectral dimension is d (as d → ∞)
    # For finite Q_d, the return prob has corrections
    # P_Q_d(2n) = (1/2^d) * sum_{k=0}^{d} C(d,k) * ((d-2k)/d)^{2n}
    # For Q₆: P(2) = (1/64) * sum C(6,k)(1-2k/6)^2
    p2_q6 = sum(math.comb(6, k) * ((6-2*k)/6)**2 for k in range(7)) / 64
    print(f"  Q₆ P(2) = {p2_q6:.8f} (verify: {exact_returns['Q6'][2]:.8f})")

    results = {
        "hex_spectral_dims_short": hex_dims,
        "hex_spectral_dims_extended": extended_dims,
        "trig_spectral_dims": trig_dims,
        "hex_rhos": hex_rhos,
        "trig_rhos": trig_rhos,
        "exact_returns_hex": exact_returns,
        "exact_returns_trig": trig_exact,
    }
    return results


# ── Part 2: Effective Dimension ───────────────────────────────────

def part2(p1):
    print("\n" + "═" * 70)
    print("PART 2: EFFECTIVE DIMENSION OF EACH 五行 SUBGRAPH")
    print("═" * 70)
    results = {}

    for g in GROUP_NAMES:
        eigs = [(e["value"], e["multiplicity"]) for e in p1["or_symmetrized"]["eigenvalues"][g]]
        rho = max(v for v, _ in eigs)
        n_nonzero = sum(m for v, m in eigs if abs(v) > 1e-8)
        n_distinct_nonzero = sum(1 for v, m in eigs if abs(v) > 1e-8)
        total_mult = sum(m for _, m in eigs)
        rank = n_nonzero

        # Effective dimension: participation ratio of eigenvalue magnitudes
        all_eigs = []
        for v, m in eigs:
            all_eigs.extend([abs(v)] * m)
        all_eigs = np.array(all_eigs)
        nonzero_eigs = all_eigs[all_eigs > 1e-8]

        # Participation ratio: (sum |λ|)^2 / (N * sum |λ|^2)
        if len(nonzero_eigs) > 0:
            pr = (np.sum(nonzero_eigs))**2 / (len(nonzero_eigs) * np.sum(nonzero_eigs**2))
            eff_dim_pr = pr * len(nonzero_eigs)
        else:
            pr = 0
            eff_dim_pr = 0

        # Shannon entropy of normalized eigenvalue magnitudes
        probs = nonzero_eigs / np.sum(nonzero_eigs)
        entropy = -np.sum(probs * np.log2(probs))
        eff_dim_entropy = 2**entropy

        print(f"\n  [{g}] OR-symmetrized:")
        print(f"    Spectral radius ρ: {rho:.6f}")
        print(f"    Rank (nonzero eigenvalues): {rank}")
        print(f"    Distinct nonzero eigenvalues: {n_distinct_nonzero}")
        print(f"    Total eigenvalues: {total_mult}")
        print(f"    Nullity (zero eigenvalues): {total_mult - rank}")
        print(f"    Participation ratio: {pr:.4f}")
        print(f"    Effective dimension (PR × rank): {eff_dim_pr:.2f}")
        print(f"    Shannon effective dimension: {eff_dim_entropy:.2f}")

        results[g] = {
            "spectral_radius": rho,
            "rank": rank,
            "distinct_nonzero": n_distinct_nonzero,
            "nullity": total_mult - rank,
            "participation_ratio": float(pr),
            "eff_dim_pr": float(eff_dim_pr),
            "eff_dim_entropy": float(eff_dim_entropy),
        }

    # Q₆ reference
    q6_eigs = [(6 - 2*k, int(round(math.comb(6, k)))) for k in range(7)]
    all_q6 = []
    for v, m in q6_eigs:
        all_q6.extend([abs(v)] * m)
    all_q6 = np.array(all_q6)
    nonzero_q6 = all_q6[all_q6 > 1e-8]
    rank_q6 = len(nonzero_q6)
    pr_q6 = (np.sum(nonzero_q6))**2 / (len(nonzero_q6) * np.sum(nonzero_q6**2))

    print(f"\n  [Q₆] Reference:")
    print(f"    Rank: {rank_q6}")
    print(f"    Nullity: {64 - rank_q6} (weight-3 eigenspace = {int(round(math.comb(6,3)))})")
    print(f"    Participation ratio: {pr_q6:.4f}")

    results["Q6"] = {
        "rank": rank_q6,
        "nullity": 64 - rank_q6,
        "participation_ratio": float(pr_q6),
    }

    return results


# ── Part 3: Dimensional Comparison ────────────────────────────────

def part3():
    print("\n" + "═" * 70)
    print("PART 3: DIMENSIONAL COMPARISON TO ~16-DIM MANIFOLD")
    print("═" * 70)

    print("\n  ── Combinatorial Dimensions ──")
    print(f"  Q₆ ambient dimension: 6")
    print(f"  Total states: 64 = 2^6")
    print(f"  log₂(64) = 6 bits of information")

    print(f"\n  Weight-3 Walsh eigenspace: C(6,3) = 20 basis vectors")
    print(f"  Semantic manifold effective dim: ~16 (measured)")
    print(f"  Ratio: 16/20 = {16/20:.2f} (80% of weight-3 capacity)")

    print(f"\n  ── 互 Map Dimensional Reduction ──")
    print(f"  互 image: 16 states = 2^4 → 4 effective bits")
    print(f"  互 constraint: bit3=bit1, bit4=bit2 → removes 2 bits")
    print(f"  互² image: 4 states = 2^2 → 2 effective bits")
    print(f"  互² constraint: retains only bits 2,3")
    print(f"  Dimensional reduction: 6 → 4 → 2 bits (per application)")

    print(f"\n  ── Resolution per Dimension ──")
    print(f"  If 64 states discretize d-dimensional space:")
    for d in [2, 3, 4, 5, 6, 8, 10, 16, 20]:
        res = 64 ** (1/d)
        print(f"    d={d:2d}: resolution = 64^(1/{d}) = {res:.4f} per dimension")

    print(f"\n  ── Information Budget ──")
    print(f"  6 bits encode the state. These bits are structured as:")
    print(f"    Bits 0,5 (lines 1,6): 'outer' — dropped by 互, no effect on nuclear structure")
    print(f"    Bits 1,4 (lines 2,5): 'middle' — survive one 互 application, dropped by 互²")
    print(f"    Bits 2,3 (lines 3,4): 'hinge' — survive all 互 applications, determine attractor")
    print(f"  Layer structure: 2 outer + 2 middle + 2 hinge = 6 bits")
    print(f"  互 retains: 4 bits (middle + hinge)")
    print(f"  互² retains: 2 bits (hinge only)")

    results = {
        "ambient_dim": 6,
        "total_states": 64,
        "weight3_basis": 20,
        "semantic_manifold_dim": 16,
        "hu_image_states": 16,
        "hu_image_bits": 4,
        "hu2_image_states": 4,
        "hu2_image_bits": 2,
        "bit_layers": {
            "outer": {"bits": [0, 5], "survives_hu": False, "survives_hu2": False},
            "middle": {"bits": [1, 4], "survives_hu": True, "survives_hu2": False},
            "hinge": {"bits": [2, 3], "survives_hu": True, "survives_hu2": True},
        },
    }
    return results


# ── Part 4: Summary Table ─────────────────────────────────────────

def part4(results_1, results_2, results_3):
    print("\n" + "═" * 70)
    print("PART 4: DIMENSIONAL SUMMARY TABLE")
    print("═" * 70)

    print(f"\n  {'Object':>25} | {'Dim type':>18} | {'Value':>8}")
    print(f"  {'-'*25}-+-{'-'*18}-+-{'-'*8}")

    rows = [
        ("Q₆", "Combinatorial", "6"),
        ("Q₆", "Spectral (fit)", f"{results_1['hex_spectral_dims_extended'].get('Q6', 'N/A'):.2f}"
         if results_1['hex_spectral_dims_extended'].get('Q6') else "N/A"),
        ("Q₆", "Rank", "44"),
        ("Q₆", "Nullity (=C(6,3))", "20"),
        ("", "", ""),
        ("克 OR-sym", "Spectral (fit)", f"{results_1['hex_spectral_dims_extended'].get('克', 'N/A'):.2f}"
         if results_1['hex_spectral_dims_extended'].get('克') else "N/A"),
        ("克 OR-sym", "Rank", str(results_2["克"]["rank"])),
        ("克 OR-sym", "Nullity", str(results_2["克"]["nullity"])),
        ("克 OR-sym", "Eff dim (PR)", f"{results_2['克']['eff_dim_pr']:.1f}"),
        ("克 OR-sym", "Spectral radius", f"{results_2['克']['spectral_radius']:.3f}"),
        ("", "", ""),
        ("生 OR-sym", "Spectral (fit)", f"{results_1['hex_spectral_dims_extended'].get('生', 'N/A'):.2f}"
         if results_1['hex_spectral_dims_extended'].get('生') else "N/A"),
        ("生 OR-sym", "Rank", str(results_2["生"]["rank"])),
        ("生 OR-sym", "Nullity", str(results_2["生"]["nullity"])),
        ("生 OR-sym", "Eff dim (PR)", f"{results_2['生']['eff_dim_pr']:.1f}"),
        ("生 OR-sym", "Spectral radius", f"{results_2['生']['spectral_radius']:.3f}"),
        ("", "", ""),
        ("比和 OR-sym", "Spectral (fit)", f"{results_1['hex_spectral_dims_extended'].get('比和', 'N/A'):.2f}"
         if results_1['hex_spectral_dims_extended'].get('比和') else "N/A"),
        ("比和 OR-sym", "Rank", str(results_2["比和"]["rank"])),
        ("比和 OR-sym", "Nullity", str(results_2["比和"]["nullity"])),
        ("比和 OR-sym", "Eff dim (PR)", f"{results_2['比和']['eff_dim_pr']:.1f}"),
        ("比和 OR-sym", "Spectral radius", f"{results_2['比和']['spectral_radius']:.3f}"),
        ("", "", ""),
        ("Semantic manifold", "Effective (measured)", "~16"),
        ("Weight-3 eigenspace", "Basis dimension", "20"),
        ("互 image", "Combinatorial", "4 bits"),
        ("互 attractor", "Combinatorial", "2 bits"),
        ("互² bits retained", "Algebraic", "2 (hinge)"),
    ]

    for obj, dim_type, value in rows:
        if obj == "":
            print(f"  {'-'*25}-+-{'-'*18}-+-{'-'*8}")
        else:
            print(f"  {obj:>25} | {dim_type:>18} | {value:>8}")

    # ── Rank decomposition ─────────────────────────────────────────
    print("\n  ── Rank Decomposition ──")
    ranks = {g: results_2[g]["rank"] for g in GROUP_NAMES}
    nullities = {g: results_2[g]["nullity"] for g in GROUP_NAMES}
    total_rank = sum(ranks.values())
    total_nullity = sum(nullities.values())
    print(f"  Sum of ranks: {' + '.join(f'{ranks[g]}' for g in GROUP_NAMES)} = {total_rank}")
    print(f"  Q₆ rank: 44")
    print(f"  Difference: {total_rank} - 44 = {total_rank - 44}")
    print(f"  Sum of nullities: {' + '.join(f'{nullities[g]}' for g in GROUP_NAMES)} = {total_nullity}")
    print(f"  (64 × 3 = 192 total eigenvalues; null: {total_nullity}; nonzero: {total_rank})")


# ── Main ───────────────────────────────────────────────────────────

def main():
    p1 = load_p1()
    p45 = load_p45()
    transitions = load_transitions()

    print("=" * 70)
    print("PROBE 7: SPECTRAL DIMENSION + DIMENSIONAL SYNTHESIS")
    print("=" * 70)

    r1 = part1(p1, p45, transitions)
    r2 = part2(p1)
    r3 = part3()
    part4(r1, r2, r3)

    json_results = {
        "part1_spectral_dimension": {
            "hex_dims_short": r1["hex_spectral_dims_short"],
            "hex_dims_extended": r1["hex_spectral_dims_extended"],
            "trig_dims": r1["trig_spectral_dims"],
            "hex_rhos": r1["hex_rhos"],
            "trig_rhos": r1["trig_rhos"],
        },
        "part2_effective_dimension": r2,
        "part3_dimensional_comparison": r3,
    }

    out_path = HERE / "p7_results.json"
    with open(out_path, "w") as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
