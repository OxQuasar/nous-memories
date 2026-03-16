#!/usr/bin/env python3
"""Q1 Phase 8: Dimensionality Reduction of Opposition Directions.

Tests whether the trigram structure decomposes the directions of thematic opposition
between complement pairs. Each hexagram = (upper, lower) trigram; complement flips
both via XOR-7, yielding 4 trigram complement pairs: {0,7},{1,6},{2,5},{3,4}.

8a: Trigram additive model on difference vectors
8b: Cross-model consensus dimensions
8c: Trigram decomposition on consensus
8d: Algebraic groupings (五行, Fano line, basin)
"""

import numpy as np
import json
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine as cos_dist
from scipy.stats import spearmanr
from scipy.linalg import orthogonal_procrustes

from phase1_residual_structure import load_data, build_design_matrix, extract_residuals

# ═══════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
OUT_DIR = Path(__file__).resolve().parent

N_HEX = 64
N_LINES = 6
N_PERM = 10_000
RNG = np.random.default_rng(42)

MODELS = ['bge-m3', 'e5-large', 'labse']

# Trigram complement pair type: min(val, 7-val)
# {0,7}→0(KunQian), {1,6}→1(ZhenXun), {2,5}→2(KanLi), {3,4}→3(DuiGen)
TRI_PAIR_NAMES = {0: 'KunQian', 1: 'ZhenXun', 2: 'KanLi', 3: 'DuiGen'}

WUXING = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
WUXING_IDX = {e: i for i, e in enumerate(WUXING)}


# ═══════════════════════════════════════════════════════
# Infrastructure
# ═══════════════════════════════════════════════════════

def tri_pair_type(trigram_val):
    """Map trigram value to its complement pair type."""
    return min(trigram_val, 7 - trigram_val)


def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)


def load_embeddings(model_name):
    """Load cached embeddings for a model."""
    path = OUT_DIR / f"embeddings_{model_name}.npz"
    return np.load(path)['yaoci']


def get_complement_pairs(atlas):
    """Return 32 complement pairs (h, c) with h < c."""
    pairs = []
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        if h < c:
            pairs.append((h, c))
    assert len(pairs) == 32
    return pairs


def get_pair_trigram_types(atlas, pairs):
    """For each complement pair, return (lower_pair_type, upper_pair_type)."""
    types = []
    for h, c in pairs:
        d = atlas[str(h)]
        lt = tri_pair_type(d['lower_trigram']['val'])
        ut = tri_pair_type(d['upper_trigram']['val'])
        types.append((lt, ut))
    return types


def compute_residual_centroids(yaoci_emb, meta):
    """Regress out algebraic signal, compute hex centroids on residuals."""
    X, _ = build_design_matrix(meta)
    residual, r2, _ = extract_residuals(yaoci_emb, X)
    centroids = np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    return centroids, r2


def compute_diff_vectors(centroids, pairs):
    """Compute centroid_h - centroid_c for each pair."""
    return np.array([centroids[h] - centroids[c] for h, c in pairs])


# ═══════════════════════════════════════════════════════
# 8a: Trigram Additive Model
# ═══════════════════════════════════════════════════════

def build_trigram_design(pair_types, which='both'):
    """Build one-hot design matrix for trigram pair types.

    which: 'both' (8 cols), 'lower' (4 cols), 'upper' (4 cols)
    """
    n = len(pair_types)
    cols = []

    if which in ('both', 'lower'):
        for t in range(4):
            col = np.array([1.0 if lt == t else 0.0 for lt, ut in pair_types])
            cols.append(col)

    if which in ('both', 'upper'):
        for t in range(4):
            col = np.array([1.0 if ut == t else 0.0 for lt, ut in pair_types])
            cols.append(col)

    return np.column_stack(cols)


def multivariate_r2(Y, X):
    """Frobenius-norm R² for multivariate OLS: Y (n×d) on X (n×p)."""
    # Y_hat = X (X'X)^-1 X' Y = X @ pinv(X) @ Y
    Q, R = np.linalg.qr(X, mode='reduced')
    Y_hat = Q @ (Q.T @ Y)
    ss_res = np.sum((Y - Y_hat) ** 2)
    ss_tot = np.sum((Y - Y.mean(axis=0)) ** 2)
    return 1.0 - ss_res / ss_tot, Y_hat


def phase_8a(diff_vectors, pair_types, label=""):
    """Trigram additive model on difference vectors."""
    prefix = f"[{label}] " if label else ""
    print(f"\n  {prefix}8a: Trigram Additive Model")
    print(f"  {'-'*60}")

    n, d = diff_vectors.shape
    results = {}

    # Full model: 4 lower + 4 upper indicators
    X_full = build_trigram_design(pair_types, 'both')
    r2_full, Y_hat_full = multivariate_r2(diff_vectors, X_full)
    results['r2_full'] = r2_full
    print(f"  {prefix}Full model R² (lower+upper): {r2_full:.4f}")

    # Lower-only
    X_lower = build_trigram_design(pair_types, 'lower')
    r2_lower, _ = multivariate_r2(diff_vectors, X_lower)
    results['r2_lower'] = r2_lower
    print(f"  {prefix}Lower-only R²: {r2_lower:.4f}")

    # Upper-only
    X_upper = build_trigram_design(pair_types, 'upper')
    r2_upper, _ = multivariate_r2(diff_vectors, X_upper)
    results['r2_upper'] = r2_upper
    print(f"  {prefix}Upper-only R²: {r2_upper:.4f}")

    # Permutation test for full model
    null_r2 = np.empty(N_PERM)
    for i in range(N_PERM):
        perm = RNG.permutation(n)
        shuffled_types = [pair_types[j] for j in perm]
        X_perm = build_trigram_design(shuffled_types, 'both')
        null_r2[i], _ = multivariate_r2(diff_vectors, X_perm)

    p_full = np.mean(null_r2 >= r2_full)
    results['p_full'] = p_full
    results['null_r2_mean'] = float(np.mean(null_r2))
    results['null_r2_std'] = float(np.std(null_r2))
    print(f"  {prefix}Permutation p-value: {p_full:.4f} (null R²: {np.mean(null_r2):.4f} ± {np.std(null_r2):.4f})")

    # Per-trigram-pair fitted vectors and norms
    # Fit: Δ = X_full @ B, B = pinv(X_full) @ Δ
    B = np.linalg.pinv(X_full) @ diff_vectors  # (8, d)
    alpha = B[:4]  # lower pair contributions
    beta = B[4:]   # upper pair contributions
    alpha_norms = np.linalg.norm(alpha, axis=1)
    beta_norms = np.linalg.norm(beta, axis=1)

    print(f"\n  {prefix}Per-trigram-pair vector norms:")
    print(f"    Lower (α):")
    for t in range(4):
        print(f"      {TRI_PAIR_NAMES[t]}: ||α|| = {alpha_norms[t]:.4f}")
    print(f"    Upper (β):")
    for t in range(4):
        print(f"      {TRI_PAIR_NAMES[t]}: ||β|| = {beta_norms[t]:.4f}")

    results['alpha_norms'] = alpha_norms.tolist()
    results['beta_norms'] = beta_norms.tolist()

    # Interaction test: within-cell vs across-cell cosine similarity of residuals
    residuals_full = diff_vectors - Y_hat_full
    cell_map = defaultdict(list)
    for i, (lt, ut) in enumerate(pair_types):
        cell_map[(lt, ut)].append(i)

    # Within-cell cosines (each cell has 2 pairs)
    within_cosines = []
    for cell, indices in cell_map.items():
        assert len(indices) == 2, f"Cell {cell} has {len(indices)} pairs"
        cos = 1.0 - cos_dist(residuals_full[indices[0]], residuals_full[indices[1]])
        within_cosines.append(cos)

    # Across-cell cosines
    across_cosines = []
    all_indices = list(range(n))
    for i in range(n):
        for j in range(i+1, n):
            if pair_types[i] != pair_types[j]:  # different cell
                cos = 1.0 - cos_dist(residuals_full[i], residuals_full[j])
                across_cosines.append(cos)

    mean_within = np.mean(within_cosines)
    mean_across = np.mean(across_cosines)
    gap = mean_within - mean_across

    # Permutation test for interaction
    null_gaps = np.empty(N_PERM)
    for i in range(N_PERM):
        perm = RNG.permutation(n)
        shuffled_types = [pair_types[j] for j in perm]
        shuffled_cells = defaultdict(list)
        for idx, (lt, ut) in enumerate(shuffled_types):
            shuffled_cells[(lt, ut)].append(idx)
        w_cos = []
        for cell, indices in shuffled_cells.items():
            if len(indices) == 2:
                w_cos.append(1.0 - cos_dist(residuals_full[indices[0]], residuals_full[indices[1]]))
        a_cos = []
        for ii in range(n):
            for jj in range(ii+1, n):
                if shuffled_types[ii] != shuffled_types[jj]:
                    a_cos.append(1.0 - cos_dist(residuals_full[ii], residuals_full[jj]))
        null_gaps[i] = np.mean(w_cos) - np.mean(a_cos) if w_cos else 0

    p_interact = np.mean(null_gaps >= gap)
    results['within_cell_cos'] = float(mean_within)
    results['across_cell_cos'] = float(mean_across)
    results['interaction_gap'] = float(gap)
    results['interaction_p'] = float(p_interact)

    print(f"\n  {prefix}Interaction test (additive model residuals):")
    print(f"    Within-cell mean cosine: {mean_within:.4f}")
    print(f"    Across-cell mean cosine: {mean_across:.4f}")
    print(f"    Gap: {gap:+.4f}, p={p_interact:.4f}")
    if p_interact < 0.05:
        print(f"    → Significant interaction structure beyond additive model")
    else:
        print(f"    → No significant interaction (additive model sufficient)")

    return results


def phase_8a_cross_model(atlas, pairs, pair_types, meta):
    """Run 8a on all 3 models."""
    print(f"\n{'='*70}")
    print("8a: TRIGRAM DECOMPOSITION — CROSS-MODEL")
    print(f"{'='*70}")

    all_results = {}
    for model in MODELS:
        yaoci = load_embeddings(model)
        centroids, r2 = compute_residual_centroids(yaoci, meta)
        diff = compute_diff_vectors(centroids, pairs)
        print(f"\n  [{model}] Algebraic R²={r2:.4f}, diff shape={diff.shape}")
        res = phase_8a(diff, pair_types, label=model)
        all_results[model] = res

    # Summary table
    print(f"\n  Cross-model R² summary:")
    print(f"  {'Model':<12} {'Full':>8} {'Lower':>8} {'Upper':>8} {'p-value':>8}")
    for model in MODELS:
        r = all_results[model]
        print(f"  {model:<12} {r['r2_full']:>8.4f} {r['r2_lower']:>8.4f} {r['r2_upper']:>8.4f} {r['p_full']:>8.4f}")

    return all_results


# ═══════════════════════════════════════════════════════
# 8b: Cross-Model Consensus Dimensions
# ═══════════════════════════════════════════════════════

def phase_8b(atlas, pairs, pair_types, meta):
    """Cross-model consensus via direction concordance and Procrustes."""
    print(f"\n{'='*70}")
    print("8b: CROSS-MODEL CONSENSUS DIMENSIONS")
    print(f"{'='*70}")

    # Compute diff vectors per model
    model_diffs = {}
    for model in MODELS:
        yaoci = load_embeddings(model)
        centroids, _ = compute_residual_centroids(yaoci, meta)
        model_diffs[model] = compute_diff_vectors(centroids, pairs)

    results = {}

    # ── Direction concordance (Mantel on cosine similarity matrices) ──
    print(f"\n  Direction concordance (Mantel test on unit-vector cosine matrices):")
    model_cos_mats = {}
    for model in MODELS:
        dv = model_diffs[model]
        # Unit normalize
        norms = np.linalg.norm(dv, axis=1, keepdims=True)
        unit_dv = dv / norms
        cos_mat = unit_dv @ unit_dv.T  # 32×32
        model_cos_mats[model] = cos_mat

    for m1, m2 in combinations(MODELS, 2):
        mat1 = model_cos_mats[m1]
        mat2 = model_cos_mats[m2]
        triu = np.triu_indices(32, k=1)
        vec1 = mat1[triu]
        vec2 = mat2[triu]
        rho, p = spearmanr(vec1, vec2)
        results[f'mantel_{m1}_{m2}'] = (float(rho), float(p))
        print(f"    {m1} ↔ {m2}: Spearman ρ={rho:+.4f}, p={p:.6f}")

    # ── Procrustes analysis ──
    print(f"\n  Procrustes analysis (R² after alignment):")
    ks = [5, 8, 10, 15, 20]

    # PCA-reduce each model's diff vectors
    procrustes_results = {}
    for k in ks:
        print(f"\n    k={k}:")
        pca_reduced = {}
        for model in MODELS:
            dv = model_diffs[model]
            pca = PCA(n_components=min(k, dv.shape[0]-1, dv.shape[1]))
            pca_reduced[model] = pca.fit_transform(dv)

        for m1, m2 in combinations(MODELS, 2):
            A = pca_reduced[m1][:, :min(k, pca_reduced[m1].shape[1])]
            B = pca_reduced[m2][:, :min(k, pca_reduced[m2].shape[1])]
            # Ensure same number of columns
            min_cols = min(A.shape[1], B.shape[1])
            A = A[:, :min_cols]
            B = B[:, :min_cols]

            # Standardize (center + scale)
            A = A - A.mean(axis=0)
            B = B - B.mean(axis=0)
            A = A / np.linalg.norm(A, 'fro')
            B = B / np.linalg.norm(B, 'fro')

            R, s = orthogonal_procrustes(A, B)
            A_aligned = A @ R
            ss_res = np.sum((A_aligned - B) ** 2)
            ss_tot = np.sum(B ** 2)
            r2 = 1.0 - ss_res / ss_tot

            key = f'{m1}_{m2}_k{k}'
            procrustes_results[key] = float(r2)
            print(f"      {m1} ↔ {m2}: R²={r2:.4f}")

    results['procrustes'] = procrustes_results

    # ── Consensus vectors ──
    # Find best k (where R² plateaus across all pairs)
    print(f"\n  Procrustes R² by k (mean across model pairs):")
    best_k = ks[0]
    best_mean_r2 = -1
    for k in ks:
        r2s = [procrustes_results[f'{m1}_{m2}_k{k}']
               for m1, m2 in combinations(MODELS, 2)]
        mean_r2 = np.mean(r2s)
        print(f"    k={k}: mean R²={mean_r2:.4f} ({', '.join(f'{r:.4f}' for r in r2s)})")
        if mean_r2 > best_mean_r2:
            best_mean_r2 = mean_r2
            best_k = k

    print(f"\n  Best k: {best_k} (mean Procrustes R²={best_mean_r2:.4f})")

    # Build consensus at best_k: align all models to BGE-M3 reference, average
    ref_model = 'bge-m3'
    pca_ref = PCA(n_components=min(best_k, 31))
    ref_reduced = pca_ref.fit_transform(model_diffs[ref_model])[:, :best_k]
    ref_reduced = ref_reduced - ref_reduced.mean(axis=0)

    aligned_all = [ref_reduced.copy()]
    for model in MODELS:
        if model == ref_model:
            continue
        pca_m = PCA(n_components=min(best_k, model_diffs[model].shape[1], 31))
        m_reduced = pca_m.fit_transform(model_diffs[model])[:, :best_k]
        m_reduced = m_reduced - m_reduced.mean(axis=0)

        # Scale to match ref norm
        m_reduced = m_reduced * (np.linalg.norm(ref_reduced, 'fro') / np.linalg.norm(m_reduced, 'fro'))

        R, _ = orthogonal_procrustes(m_reduced, ref_reduced)
        aligned_all.append(m_reduced @ R)

    consensus = np.mean(aligned_all, axis=0)  # (32, best_k)

    # PCA on consensus
    pca_cons = PCA(n_components=min(consensus.shape[1], 31))
    cons_scores = pca_cons.fit_transform(consensus)
    cons_var = pca_cons.explained_variance_ratio_
    lam = pca_cons.explained_variance_
    pr = np.sum(lam) ** 2 / np.sum(lam ** 2)

    print(f"\n  Consensus ({best_k}-dim) PCA:")
    for i in range(min(10, len(cons_var))):
        print(f"    PC{i+1}: {cons_var[i]*100:.2f}%")
    print(f"  Participation ratio: {pr:.2f}")

    results['best_k'] = best_k
    results['consensus_pr'] = float(pr)
    results['consensus'] = consensus

    return results


# ═══════════════════════════════════════════════════════
# 8c: Trigram Decomposition on Consensus
# ═══════════════════════════════════════════════════════

def phase_8c(consensus, pair_types):
    """Re-run 8a additive model on consensus difference vectors."""
    print(f"\n{'='*70}")
    print("8c: TRIGRAM DECOMPOSITION ON CONSENSUS")
    print(f"{'='*70}")

    return phase_8a(consensus, pair_types, label="consensus")


# ═══════════════════════════════════════════════════════
# 8d: Algebraic Groupings
# ═══════════════════════════════════════════════════════

def wuxing_relation(e1, e2):
    """Determine the 五行 relation between two elements.

    Returns: 'same', 'generating', 'generated', 'overcoming', 'overcome'
    """
    if e1 == e2:
        return 'same'
    i1, i2 = WUXING_IDX[e1], WUXING_IDX[e2]
    if (i1 + 1) % 5 == i2:
        return 'generating'  # e1 generates e2
    if (i2 + 1) % 5 == i1:
        return 'generated'   # e1 is generated by e2
    if (i1 + 2) % 5 == i2:
        return 'overcoming'  # e1 overcomes e2
    if (i2 + 2) % 5 == i1:
        return 'overcome'    # e1 is overcome by e2
    return 'unknown'


def grouping_test(diff_vectors, group_labels, group_name):
    """Test within-group vs between-group cosine similarity of unit diff vectors."""
    n = len(diff_vectors)
    norms = np.linalg.norm(diff_vectors, axis=1, keepdims=True)
    unit_dv = diff_vectors / norms

    # Compute all pairwise cosines
    cos_mat = unit_dv @ unit_dv.T

    # Group assignments
    groups = defaultdict(list)
    for i, g in enumerate(group_labels):
        groups[g].append(i)

    # Within-group cosines
    within = []
    for g, indices in groups.items():
        for i, j in combinations(indices, 2):
            within.append(cos_mat[i, j])

    # Between-group cosines
    between = []
    for i in range(n):
        for j in range(i+1, n):
            if group_labels[i] != group_labels[j]:
                between.append(cos_mat[i, j])

    mean_within = np.mean(within) if within else 0
    mean_between = np.mean(between) if between else 0
    gap = mean_within - mean_between

    # Permutation test
    null_gaps = np.empty(N_PERM)
    for p in range(N_PERM):
        perm = RNG.permutation(n)
        perm_labels = [group_labels[j] for j in perm]
        perm_groups = defaultdict(list)
        for i, g in enumerate(perm_labels):
            perm_groups[g].append(i)
        w = []
        for g, indices in perm_groups.items():
            for ii, jj in combinations(indices, 2):
                w.append(cos_mat[ii, jj])
        b = []
        for ii in range(n):
            for jj in range(ii+1, n):
                if perm_labels[ii] != perm_labels[jj]:
                    b.append(cos_mat[ii, jj])
        null_gaps[p] = (np.mean(w) if w else 0) - (np.mean(b) if b else 0)

    p_val = np.mean(null_gaps >= gap)

    print(f"\n    {group_name}:")
    print(f"      Groups: {dict(Counter(group_labels))}")
    print(f"      Within-group mean cos: {mean_within:.4f} ({len(within)} pairs)")
    print(f"      Between-group mean cos: {mean_between:.4f} ({len(between)} pairs)")
    print(f"      Gap: {gap:+.4f}, p={p_val:.4f}")
    if p_val < 0.05:
        print(f"      → SIGNIFICANT: groups share opposition direction")
    else:
        print(f"      → Not significant")

    return {
        'mean_within': float(mean_within),
        'mean_between': float(mean_between),
        'gap': float(gap),
        'p': float(p_val),
        'n_groups': len(groups),
        'group_sizes': dict(Counter(group_labels)),
    }


def phase_8d(atlas, pairs, pair_types, diff_vectors_bge, consensus):
    """Test algebraic groupings on whichever representation shows more structure."""
    print(f"\n{'='*70}")
    print("8d: ALGEBRAIC GROUPINGS")
    print(f"{'='*70}")

    # Test on both representations
    results = {}
    for name, dv in [('bge-m3', diff_vectors_bge), ('consensus', consensus)]:
        print(f"\n  Representation: {name} (shape {dv.shape})")

        # 1. 五行 relation between surface elements
        wuxing_labels = []
        for h, c in pairs:
            sc_h = atlas[str(h)]['surface_cell']
            sc_c = atlas[str(c)]['surface_cell']
            # Use lower element relation
            rel = wuxing_relation(sc_h[0], sc_c[0])
            wuxing_labels.append(rel)
        r = grouping_test(dv, wuxing_labels, "五行 lower-element relation")
        results[f'{name}_wuxing_lower'] = r

        # Upper element relation
        wuxing_upper_labels = []
        for h, c in pairs:
            sc_h = atlas[str(h)]['surface_cell']
            sc_c = atlas[str(c)]['surface_cell']
            rel = wuxing_relation(sc_h[1], sc_c[1])
            wuxing_upper_labels.append(rel)
        r = grouping_test(dv, wuxing_upper_labels, "五行 upper-element relation")
        results[f'{name}_wuxing_upper'] = r

        # 2. Fano line (upper trigram pair type) — 4 groups of 8
        upper_labels = [ut for lt, ut in pair_types]
        r = grouping_test(dv, upper_labels, "Upper trigram pair type (Fano)")
        results[f'{name}_fano_upper'] = r

        # Lower trigram pair type
        lower_labels = [lt for lt, ut in pair_types]
        r = grouping_test(dv, lower_labels, "Lower trigram pair type")
        results[f'{name}_fano_lower'] = r

        # 3. Basin type: same basin vs different basin
        basin_labels = []
        for h, c in pairs:
            b1 = atlas[str(h)]['basin']
            b2 = atlas[str(c)]['basin']
            basin_labels.append('same' if b1 == b2 else 'different')
        r = grouping_test(dv, basin_labels, "Basin (same vs different)")
        results[f'{name}_basin'] = r

    return results


# ═══════════════════════════════════════════════════════
# Report
# ═══════════════════════════════════════════════════════

def write_report(results_8a, results_8b, results_8c, results_8d):
    """Write summary to markdown."""
    lines = [
        "# Phase 8: Dimensionality Reduction of Opposition Directions",
        "",
        "Tests whether trigram structure decomposes the directions of thematic "
        "opposition between complement pairs.",
        "",
    ]

    # 8a Cross-model table
    lines += ["## 8a: Trigram Additive Model (Cross-Model)", ""]
    lines.append("| Model | Full R² | Lower R² | Upper R² | p-value | Within cos | Across cos | Interact p |")
    lines.append("|-------|---------|----------|----------|---------|------------|------------|------------|")
    for model in MODELS:
        r = results_8a[model]
        lines.append(
            f"| {model} | {r['r2_full']:.4f} | {r['r2_lower']:.4f} | "
            f"{r['r2_upper']:.4f} | {r['p_full']:.4f} | "
            f"{r['within_cell_cos']:.4f} | {r['across_cell_cos']:.4f} | "
            f"{r['interaction_p']:.4f} |"
        )
    lines.append("")

    # Alpha/beta norms for BGE-M3
    r = results_8a['bge-m3']
    lines += ["### Per-trigram-pair vector norms (BGE-M3)", ""]
    lines.append("| Pair | α (lower) | β (upper) |")
    lines.append("|------|-----------|-----------|")
    for t in range(4):
        lines.append(f"| {TRI_PAIR_NAMES[t]} | {r['alpha_norms'][t]:.4f} | {r['beta_norms'][t]:.4f} |")
    lines.append("")

    # 8b
    lines += ["## 8b: Cross-Model Consensus", ""]
    lines.append(f"Best k: {results_8b['best_k']}")
    lines.append(f"Consensus participation ratio: {results_8b['consensus_pr']:.2f}")
    lines.append("")

    # Direction concordance
    lines.append("### Direction concordance (Spearman ρ)")
    lines.append("")
    for m1, m2 in combinations(MODELS, 2):
        rho, p = results_8b[f'mantel_{m1}_{m2}']
        lines.append(f"- {m1} ↔ {m2}: ρ={rho:+.4f} (p={p:.6f})")
    lines.append("")

    # Procrustes
    lines.append("### Procrustes R²")
    lines.append("")
    lines.append("| k | " + " | ".join(f"{m1}↔{m2}" for m1, m2 in combinations(MODELS, 2)) + " |")
    lines.append("|---|" + "|".join("---:" for _ in combinations(MODELS, 2)) + "|")
    for k in [5, 8, 10, 15, 20]:
        vals = []
        for m1, m2 in combinations(MODELS, 2):
            key = f'{m1}_{m2}_k{k}'
            if key in results_8b['procrustes']:
                vals.append(f"{results_8b['procrustes'][key]:.4f}")
            else:
                vals.append("N/A")
        lines.append(f"| {k} | " + " | ".join(vals) + " |")
    lines.append("")

    # 8c
    lines += ["## 8c: Trigram Decomposition on Consensus", ""]
    lines.append(f"Full R²: {results_8c['r2_full']:.4f} (p={results_8c['p_full']:.4f})")
    lines.append(f"Lower R²: {results_8c['r2_lower']:.4f}")
    lines.append(f"Upper R²: {results_8c['r2_upper']:.4f}")
    lines.append(f"Interaction: within={results_8c['within_cell_cos']:.4f}, "
                 f"across={results_8c['across_cell_cos']:.4f}, "
                 f"p={results_8c['interaction_p']:.4f}")
    lines.append("")

    # 8d
    lines += ["## 8d: Algebraic Groupings", ""]
    lines.append("| Representation | Grouping | Within cos | Between cos | Gap | p |")
    lines.append("|----------------|----------|------------|-------------|-----|---|")
    for key in sorted(results_8d.keys()):
        r = results_8d[key]
        parts = key.split('_', 1)
        rep = parts[0]
        grp = parts[1] if len(parts) > 1 else key
        sig = "✓" if r['p'] < 0.05 else ""
        lines.append(
            f"| {rep} | {grp} | {r['mean_within']:.4f} | "
            f"{r['mean_between']:.4f} | {r['gap']:+.4f} | {r['p']:.4f} {sig} |"
        )
    lines.append("")

    out_path = OUT_DIR / "phase8_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nReport saved to {out_path}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 8: Dimensionality Reduction of Opposition Directions")
    print("=" * 70)

    # Load infrastructure
    atlas = load_atlas()
    _, meta, _ = load_data()
    pairs = get_complement_pairs(atlas)
    pair_types = get_pair_trigram_types(atlas, pairs)

    # 8a: Cross-model trigram decomposition
    results_8a = phase_8a_cross_model(atlas, pairs, pair_types, meta)

    # 8b: Cross-model consensus
    results_8b = phase_8b(atlas, pairs, pair_types, meta)

    # 8c: Trigram decomposition on consensus
    results_8c = phase_8c(results_8b['consensus'], pair_types)

    # 8d: Algebraic groupings
    yaoci_bge = load_embeddings('bge-m3')
    centroids_bge, _ = compute_residual_centroids(yaoci_bge, meta)
    diff_bge = compute_diff_vectors(centroids_bge, pairs)
    results_8d = phase_8d(atlas, pairs, pair_types, diff_bge, results_8b['consensus'])

    # Final summary
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")

    print(f"\n  8a — Trigram additive model R² across models:")
    for model in MODELS:
        r = results_8a[model]
        sig = "***" if r['p_full'] < 0.001 else "**" if r['p_full'] < 0.01 else "*" if r['p_full'] < 0.05 else "ns"
        print(f"    {model}: {r['r2_full']:.4f} ({sig})")

    print(f"\n  8b — Cross-model direction concordance:")
    for m1, m2 in combinations(MODELS, 2):
        rho, p = results_8b[f'mantel_{m1}_{m2}']
        print(f"    {m1} ↔ {m2}: ρ={rho:+.4f}")

    print(f"\n  8c — Consensus trigram R²: {results_8c['r2_full']:.4f} (p={results_8c['p_full']:.4f})")

    print(f"\n  8d — Significant groupings (p<0.05):")
    for key, r in sorted(results_8d.items()):
        if r['p'] < 0.05:
            print(f"    {key}: gap={r['gap']:+.4f}, p={r['p']:.4f}")
    no_sig = all(r['p'] >= 0.05 for r in results_8d.values())
    if no_sig:
        print(f"    (none)")

    # Key interpretation
    r2_vals = [results_8a[m]['r2_full'] for m in MODELS]
    mean_r2 = np.mean(r2_vals)
    all_sig = all(results_8a[m]['p_full'] < 0.05 for m in MODELS)

    print(f"\n  Interpretation:")
    if all_sig and mean_r2 > 0.3:
        print(f"    Trigram structure STRONGLY organizes opposition direction (mean R²={mean_r2:.3f})")
    elif all_sig:
        print(f"    Trigram structure MODERATELY organizes opposition direction (mean R²={mean_r2:.3f})")
    elif any(results_8a[m]['p_full'] < 0.05 for m in MODELS):
        print(f"    Trigram structure WEAKLY organizes opposition direction (inconsistent across models)")
    else:
        print(f"    Trigram structure does NOT organize opposition direction (mean R²={mean_r2:.3f})")

    write_report(results_8a, results_8b, results_8c, results_8d)


if __name__ == '__main__':
    main()
