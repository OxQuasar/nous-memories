"""
Probe 8: Triple-Null Projection Test

Does the semantic manifold avoid the 5 directions invisible to ALL three
五行 subgraphs, concentrating variance in the 15 visible weight-3 directions?
"""

import json
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"
Q1_DIR = HERE.parent / "reversal" / "Q1"

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]
N_HEX = 64
N_LINES = 6
N_PERMS = 10000

# ── Helpers ────────────────────────────────────────────────────────

def popcount(x):
    c = 0
    while x:
        c += x & 1
        x >>= 1
    return c

def build_walsh_hadamard():
    """64×64 Walsh-Hadamard matrix (unnormalized: entries ±1)."""
    H = np.array([[(-1) ** popcount(i & j) for j in range(64)] for i in range(64)])
    return H

def weight3_indices():
    """Indices of Hamming weight 3 among 0..63."""
    return [i for i in range(64) if popcount(i) == 3]

def build_or_symmetrized():
    """Build three OR-symmetrized 64×64 adjacency matrices."""
    with open(ATLAS_DIR / "transitions.json") as f:
        transitions = json.load(f)["bian_fan"]

    dir_mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = RELATION_GROUPS[t["tiyong_relation"]]
        dir_mats[g][t["source"], t["destination"]] = 1

    return {g: np.maximum(A, A.T) for g, A in dir_mats.items()}

def null_basis(A, tol=1e-10):
    """Null space basis via eigendecomposition (for symmetric A)."""
    eigvals, eigvecs = np.linalg.eigh(A.astype(float))
    mask = np.abs(eigvals) < tol
    return eigvecs[:, mask]

def subspace_intersection(bases, tol=1e-8):
    """
    Intersection of null spaces given their bases.
    Intersection = kernel of the matrix whose columns are all null-space bases stacked.
    Actually: intersection of subspaces spanned by columns of each basis.

    For null spaces: a vector is in the intersection iff it's in ALL null spaces.
    null(A) ∩ null(B) = null([A; B]) for symmetric A, B.
    But we're given bases, not the matrices.

    Use: v in span(B_i) for all i. Stack [B_1 | B_2 | ... ] and find the
    subspace reachable from each factor. Better: use the product of projectors.
    """
    # Iterative projection approach
    # Start with the first basis, project onto each subsequent
    current = bases[0].copy()
    for B in bases[1:]:
        # Project columns of current onto span of B
        P_B = B @ np.linalg.pinv(B)  # Projector onto span(B)
        current = P_B @ current
        # Re-orthogonalize
        U, S, _ = np.linalg.svd(current, full_matrices=False)
        mask = S > tol
        current = U[:, mask] * S[mask]

    # Final orthogonalization
    if current.shape[1] == 0:
        return np.zeros((current.shape[0], 0))
    U, S, _ = np.linalg.svd(current, full_matrices=False)
    mask = S > tol
    return U[:, mask]

def load_hex_embeddings(name):
    """Load yaoci embeddings and aggregate to hexagram level."""
    path = Q1_DIR / f"embeddings_{name}.npz"
    yaoci = np.load(path)["yaoci"]
    return yaoci.reshape(N_HEX, N_LINES, -1).mean(axis=1)


# ── Main Computation ──────────────────────────────────────────────

def main():
    np.random.seed(42)

    print("=" * 70)
    print("PROBE 8: TRIPLE-NULL PROJECTION TEST")
    print("=" * 70)

    # ── Step 1: Build 五行 subgraphs ──────────────────────────────
    print("\n── Step 1: Build OR-symmetrized subgraphs ──")
    or_mats = build_or_symmetrized()
    for g in GROUP_NAMES:
        print(f"  {g}: {int(np.sum(or_mats[g])) // 2} undirected edges")

    # ── Step 2: Weight-3 Walsh basis ──────────────────────────────
    print("\n── Step 2: Weight-3 Walsh basis ──")
    H = build_walsh_hadamard()  # 64×64, unnormalized
    w3_idx = weight3_indices()
    print(f"  Weight-3 indices: {w3_idx}")
    print(f"  Count: {len(w3_idx)} = C(6,3)")

    # Weight-3 basis: normalized Walsh functions at weight-3 indices
    # Each row H[k, :] for k in w3_idx is a Walsh function
    # As column vectors of the 64-dim space:
    W3_basis = H[w3_idx, :].T / 8.0  # 64 × 20, normalized
    # Verify orthonormality
    gram = W3_basis.T @ W3_basis
    assert np.allclose(gram, np.eye(20), atol=1e-10), "W3 basis not orthonormal"
    print(f"  W3 basis: {W3_basis.shape}, orthonormal ✓")

    # Projector onto weight-3
    P_w3 = W3_basis @ W3_basis.T  # 64×64

    # ── Step 3: Null spaces ───────────────────────────────────────
    print("\n── Step 3: Null spaces of 五行 subgraphs ──")
    null_bases = {}
    for g in GROUP_NAMES:
        nb = null_basis(or_mats[g])
        null_bases[g] = nb
        print(f"  null({g}): dim = {nb.shape[1]}")

    # ── Step 4: Triple null intersection ──────────────────────────
    print("\n── Step 4: Triple null intersection ──")

    # Better method: kernel of stacked matrices
    stacked = np.vstack([or_mats[g].astype(float) for g in GROUP_NAMES])
    U, S, Vt = np.linalg.svd(stacked)
    triple_null_dim_candidates = np.sum(S < 1e-10)
    # The null space of the stacked matrix = intersection of null spaces
    # stacked is 192×64, its null space has dim = 64 - rank(stacked)
    rank_stacked = np.sum(S > 1e-10)
    triple_null_dim = 64 - rank_stacked
    triple_null_basis = Vt[rank_stacked:].T  # 64 × triple_null_dim

    print(f"  Rank of stacked matrix: {rank_stacked}")
    print(f"  Triple null dimension: {triple_null_dim}")

    # Verify it's within weight-3
    triple_in_w3 = P_w3 @ triple_null_basis
    residual = triple_null_basis - triple_in_w3
    max_residual = np.max(np.abs(residual))
    print(f"  Triple null ⊂ weight-3: max residual = {max_residual:.2e} "
          f"({'✓' if max_residual < 1e-8 else '✗'})")

    # ── Step 5: Split weight-3 into visible/invisible ─────────────
    print("\n── Step 5: Split weight-3 into V_invisible (5) ⊕ V_visible (15) ──")

    # Express triple null in weight-3 coordinates
    # triple_null_basis is 64×5, W3_basis is 64×20
    # Coordinates: c = W3_basis^T @ triple_null_basis → 20×5
    coords_invisible = W3_basis.T @ triple_null_basis  # 20 × 5

    # Orthogonalize within weight-3 coordinates
    U_inv, S_inv, _ = np.linalg.svd(coords_invisible, full_matrices=False)
    V_invisible_w3 = U_inv[:, :triple_null_dim]  # 20 × 5 (orthonormal)

    # V_visible = orthogonal complement within 20-dim space
    # Use SVD: complete to orthonormal basis
    Q, _ = np.linalg.qr(np.hstack([V_invisible_w3,
                                     np.random.randn(20, 15)]))
    V_invisible_w3 = Q[:, :5]
    V_visible_w3 = Q[:, 5:]

    # Verify orthogonality
    cross = V_invisible_w3.T @ V_visible_w3
    assert np.allclose(cross, 0, atol=1e-10), "Not orthogonal"
    print(f"  V_invisible: {V_invisible_w3.shape} (in w3 coords)")
    print(f"  V_visible:   {V_visible_w3.shape} (in w3 coords)")
    print(f"  Orthogonality check: max |cross| = {np.max(np.abs(cross)):.2e} ✓")

    # Convert back to 64-dim: V_invisible_64 = W3_basis @ V_invisible_w3
    V_invisible_64 = W3_basis @ V_invisible_w3  # 64 × 5
    V_visible_64 = W3_basis @ V_visible_w3      # 64 × 15

    # ── Steps 6-10: Embedding analysis ────────────────────────────
    MODELS = ["bge-m3", "e5-large", "sikuroberta"]
    model_results = {}

    for model_name in MODELS:
        print(f"\n{'─' * 70}")
        print(f"  MODEL: {model_name}")
        print(f"{'─' * 70}")

        # Step 6: Load and center
        hex_emb = load_hex_embeddings(model_name)
        hex_emb_centered = hex_emb - hex_emb.mean(axis=0)
        print(f"  Hex embeddings: {hex_emb.shape}")

        # Step 7: Project onto weight-3
        # E_w3 = P_w3 @ E, but E is 64×d, P_w3 is 64×64
        E_w3 = P_w3 @ hex_emb_centered  # 64 × d

        # Total weight-3 variance
        var_w3_total = np.sum(E_w3 ** 2)

        # Total variance across ALL weights
        var_total = np.sum(hex_emb_centered ** 2)
        print(f"  Total variance: {var_total:.4f}")
        print(f"  Weight-3 variance: {var_w3_total:.4f} ({100*var_w3_total/var_total:.1f}%)")

        # Step 8: Partition weight-3 variance
        # Project onto invisible: P_inv @ E = V_inv_64 @ V_inv_64^T @ E
        E_invisible = V_invisible_64 @ (V_invisible_64.T @ hex_emb_centered)
        E_visible = V_visible_64 @ (V_visible_64.T @ hex_emb_centered)

        var_invisible = np.sum(E_invisible ** 2)
        var_visible = np.sum(E_visible ** 2)

        # Sanity check: var_invisible + var_visible ≈ var_w3_total
        var_sum = var_invisible + var_visible
        print(f"  Invisible (5d) variance: {var_invisible:.4f}")
        print(f"  Visible (15d) variance: {var_visible:.4f}")
        print(f"  Sum: {var_sum:.4f} (should ≈ {var_w3_total:.4f})")

        f_invisible = var_invisible / var_sum if var_sum > 0 else 0
        f_expected = 5.0 / 20.0

        print(f"\n  f_invisible = {f_invisible:.6f}")
        print(f"  Expected (uniform): {f_expected:.6f}")
        print(f"  Ratio to expected: {f_invisible / f_expected:.4f}")

        # Step 9: Permutation null
        print(f"\n  Running {N_PERMS} permutation shuffles...")
        f_null = np.zeros(N_PERMS)
        for trial in range(N_PERMS):
            perm = np.random.permutation(64)
            E_perm = hex_emb_centered[perm]
            E_inv_p = V_invisible_64 @ (V_invisible_64.T @ E_perm)
            E_vis_p = V_visible_64 @ (V_visible_64.T @ E_perm)
            v_inv = np.sum(E_inv_p ** 2)
            v_vis = np.sum(E_vis_p ** 2)
            f_null[trial] = v_inv / (v_inv + v_vis) if (v_inv + v_vis) > 0 else 0

        percentile = 100 * np.mean(f_null <= f_invisible)
        mean_null = np.mean(f_null)
        std_null = np.std(f_null)

        print(f"  Null distribution: mean = {mean_null:.6f}, std = {std_null:.6f}")
        print(f"  Observed percentile: {percentile:.1f}th")
        print(f"  Z-score: {(f_invisible - mean_null) / std_null:.2f}")

        if percentile < 5:
            verdict = "AVOIDS invisible (concentrates in visible) — ALIGNED"
        elif percentile > 95:
            verdict = "CONCENTRATES in invisible — ANTI-ALIGNED"
        else:
            verdict = "NO significant alignment"
        print(f"  Verdict: {verdict}")

        model_results[model_name] = {
            "emb_shape": list(hex_emb.shape),
            "var_total": float(var_total),
            "var_w3_total": float(var_w3_total),
            "var_w3_fraction": float(var_w3_total / var_total),
            "var_invisible": float(var_invisible),
            "var_visible": float(var_visible),
            "f_invisible": float(f_invisible),
            "f_expected": float(f_expected),
            "ratio_to_expected": float(f_invisible / f_expected),
            "percentile": float(percentile),
            "null_mean": float(mean_null),
            "null_std": float(std_null),
            "z_score": float((f_invisible - mean_null) / std_null),
            "verdict": verdict,
        }

    # ── Step 11: Per-dimension breakdown ──────────────────────────
    print(f"\n{'═' * 70}")
    print("STEP 11: PER-DIMENSION BREAKDOWN WITHIN WEIGHT-3")
    print(f"{'═' * 70}")

    # Use BGE-M3 as primary
    hex_emb = load_hex_embeddings("bge-m3")
    hex_emb_centered = hex_emb - hex_emb.mean(axis=0)

    # Variance per weight-3 Walsh direction
    # Each W3 basis vector w_k (64×1): variance = ||w_k^T @ E||^2 = sum_j (w_k · e_j)^2
    # where e_j is column j of hex_emb_centered
    w3_proj = W3_basis.T @ hex_emb_centered  # 20 × d
    var_per_w3_dim = np.sum(w3_proj ** 2, axis=1)  # 20 values

    # Which of the 20 are "invisible" (in the triple null)?
    # Project each W3 basis onto V_invisible_w3
    invisible_membership = np.sum((V_invisible_w3.T @ np.eye(20)[:, :]) ** 2, axis=0)
    # Actually: for each of 20 W3 basis vectors, how much is in V_invisible?
    # If the W3 basis vectors don't align with the invisible/visible split,
    # this requires a different approach.
    # Better: compute the projection of each W3 basis vector onto V_invisible
    invisible_fraction_per_dim = np.zeros(20)
    for k in range(20):
        e_k = np.eye(20)[:, k]  # k-th W3 coordinate vector
        proj_inv = V_invisible_w3 @ (V_invisible_w3.T @ e_k)
        invisible_fraction_per_dim[k] = np.dot(proj_inv, proj_inv)

    # Sort by variance
    order = np.argsort(-var_per_w3_dim)
    print(f"\n  Weight-3 Walsh dimensions ranked by variance (BGE-M3):")
    print(f"  {'Rank':>5} {'W3 idx':>7} {'Walsh idx':>10} {'Variance':>12} {'% of w3':>8} {'Inv frac':>9}")
    print(f"  {'-'*5}-{'-'*7}-{'-'*10}-{'-'*12}-{'-'*8}-{'-'*9}")
    total_w3_var = np.sum(var_per_w3_dim)
    for rank, k in enumerate(order):
        walsh_idx = w3_idx[k]
        pct = 100 * var_per_w3_dim[k] / total_w3_var
        inv_frac = invisible_fraction_per_dim[k]
        marker = " ◄" if inv_frac > 0.5 else ""
        print(f"  {rank+1:>5} {k:>7} {walsh_idx:>10} ({format(walsh_idx, '06b')}) "
              f"{var_per_w3_dim[k]:>10.4f} {pct:>7.2f}% {inv_frac:>8.3f}{marker}")

    # Top-5 invisible: which Walsh vectors are most invisible?
    inv_order = np.argsort(-invisible_fraction_per_dim)
    print(f"\n  Top 5 most 'invisible' Walsh directions:")
    for i in range(5):
        k = inv_order[i]
        print(f"    W3[{k}] = Walsh[{w3_idx[k]}] ({format(w3_idx[k], '06b')}): "
              f"inv_frac={invisible_fraction_per_dim[k]:.4f}, "
              f"variance={var_per_w3_dim[k]:.4f} "
              f"(rank {list(order).index(k)+1}/20)")

    # Overlap test: do the 5 lowest-variance dimensions match the 5 most invisible?
    bottom5_var = set(order[-5:])
    top5_inv = set(inv_order[:5])
    overlap = bottom5_var & top5_inv
    print(f"\n  Bottom-5 variance dims: {sorted(bottom5_var)}")
    print(f"  Top-5 invisible dims: {sorted(top5_inv)}")
    print(f"  Overlap: {len(overlap)} of 5")

    per_dim_data = {
        "var_per_w3_dim": var_per_w3_dim.tolist(),
        "invisible_fraction_per_dim": invisible_fraction_per_dim.tolist(),
        "bottom5_var_overlap_top5_inv": len(overlap),
    }

    # ── Step 12: Full triple-null test (all weights) ──────────────
    print(f"\n{'═' * 70}")
    print("STEP 12: FULL TRIPLE-NULL (ALL WEIGHTS, NOT JUST WEIGHT-3)")
    print(f"{'═' * 70}")

    # Triple null is 5-dim and entirely within weight-3 (verified above)
    # So the full triple null projection = weight-3 triple null projection
    # But let's verify: what fraction of TOTAL variance is in the triple null?
    for model_name in MODELS:
        hex_emb = load_hex_embeddings(model_name)
        hex_emb_centered = hex_emb - hex_emb.mean(axis=0)

        E_triple_null = V_invisible_64 @ (V_invisible_64.T @ hex_emb_centered)
        var_triple_null = np.sum(E_triple_null ** 2)
        var_total = np.sum(hex_emb_centered ** 2)

        f_total = var_triple_null / var_total
        f_expected_total = 5.0 / 64.0  # if variance uniform across all 64 dims

        print(f"  {model_name}: triple-null variance = {var_triple_null:.4f} / {var_total:.4f} "
              f"= {100*f_total:.3f}% (uniform: {100*f_expected_total:.2f}%)")

    # ── Save results ──────────────────────────────────────────────
    print(f"\n{'═' * 70}")
    print("SUMMARY")
    print(f"{'═' * 70}")

    print(f"\n  {'Model':>15} | {'f_invisible':>12} {'Expected':>10} {'Ratio':>8} {'%ile':>6} {'Z':>6} | Verdict")
    print(f"  {'-'*15}-+-{'-'*12}-{'-'*10}-{'-'*8}-{'-'*6}-{'-'*6}-+---------")
    for model_name in MODELS:
        r = model_results[model_name]
        print(f"  {model_name:>15} | {r['f_invisible']:>12.6f} {r['f_expected']:>10.6f} "
              f"{r['ratio_to_expected']:>8.4f} {r['percentile']:>5.1f}% {r['z_score']:>6.2f} | "
              f"{r['verdict']}")

    json_results = {
        "triple_null_dim": int(triple_null_dim),
        "triple_null_in_weight3": bool(max_residual < 1e-8),
        "weight3_dim": 20,
        "invisible_dim": 5,
        "visible_dim": 15,
        "model_results": model_results,
        "per_dimension": per_dim_data,
    }

    out_path = HERE / "p8_results.json"
    with open(out_path, "w") as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
