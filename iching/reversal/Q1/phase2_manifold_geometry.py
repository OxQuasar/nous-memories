#!/usr/bin/env python3
"""Q1 Phase 2: Geometry of the Thematic Manifold.

A. Principal axes of hex-thematic space (PCA on 64 hex centroids)
B. Complement axis analysis (pair-difference vectors)
C. Beyond complement — what else organizes the manifold?
D. Intra-hexagram narrative structure (6-line trajectories)
"""

import numpy as np
import json
from collections import Counter
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr, spearmanr, mannwhitneyu
from scipy.spatial.distance import pdist, squareform

# Reuse Phase 1 infrastructure
from phase1_residual_structure import load_data, build_design_matrix, extract_residuals

N_HEX = 64
N_LINES = 6
N_YAOCI = 384


# ═══════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════

def hex_centroids(residual):
    """Mean residual embedding per hexagram. Shape (64, 1024)."""
    return np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])


def atlas_coordinates(atlas):
    """Extract all usable coordinates per hexagram for correlation testing."""
    coords = {}
    for h in range(N_HEX):
        d = atlas[str(h)]
        coords.setdefault('kw_number', []).append(d['kw_number'])
        coords.setdefault('hex_val', []).append(d['hex_val'])
        coords.setdefault('complement', []).append(d['complement'])
        coords.setdefault('reverse', []).append(d['reverse'])
        coords.setdefault('depth', []).append(d['depth'])
        coords.setdefault('rank', []).append(d['rank'])
        coords.setdefault('hu_depth', []).append(d['hu_depth'])
        coords.setdefault('hu_attractor', []).append(d['hu_attractor'])
        coords.setdefault('shi', []).append(d['shi'])
        coords.setdefault('ying', []).append(d['ying'])
        coords.setdefault('inner_val', []).append(d['inner_val'])
        coords.setdefault('i_component', []).append(d['i_component'])
        coords.setdefault('hu_hex', []).append(d['hu_hex'])

        # Binary bits
        binary = d['binary']
        for bit_idx in range(6):
            coords.setdefault(f'bit_{bit_idx}', []).append(int(binary[bit_idx]))

        # Hamming weight
        coords.setdefault('hamming_weight', []).append(sum(int(b) for b in binary))

        # Trigram values
        coords.setdefault('lower_trigram', []).append(d['lower_trigram']['val'])
        coords.setdefault('upper_trigram', []).append(d['upper_trigram']['val'])

        # Categorical → numeric encoding
        for cat_name in ['basin', 'palace', 'palace_element', 'surface_relation']:
            val = d[cat_name]
            coords.setdefault(cat_name, []).append(val)

    # Convert categoricals to numeric (label encoding for correlation)
    for key in ['basin', 'palace', 'palace_element', 'surface_relation']:
        labels = coords[key]
        unique = sorted(set(labels), key=str)
        mapping = {v: i for i, v in enumerate(unique)}
        coords[key] = [mapping[v] for v in labels]

    return {k: np.array(v, dtype=float) for k, v in coords.items()}


# ═══════════════════════════════════════════════════════
# Part A: Principal axes of hex-thematic space
# ═══════════════════════════════════════════════════════

def part_a(centroids, atlas):
    print("PART A: Principal axes of hex-thematic space")
    print("=" * 70)

    pca = PCA(n_components=min(20, N_HEX - 1))
    scores = pca.fit_transform(centroids)
    var_explained = pca.explained_variance_ratio_
    cumvar = np.cumsum(var_explained)

    print(f"\n  PCA on 64 hex centroids (in residual space):")
    print(f"  {'PC':<5} {'Var%':>8} {'Cumul%':>8}")
    print(f"  {'─'*23}")
    for i in range(10):
        print(f"  PC{i+1:<3} {var_explained[i]*100:>7.2f}% {cumvar[i]*100:>7.2f}%")

    n90 = np.searchsorted(cumvar, 0.90) + 1
    n80 = np.searchsorted(cumvar, 0.80) + 1
    print(f"\n  Components for 80%: {n80}, for 90%: {n90}")

    # Correlate each PC with all atlas coordinates
    coords = atlas_coordinates(atlas)

    print(f"\n  PC correlations with atlas coordinates (|r| > 0.25 shown):")
    print(f"  {'PC':<5} {'Coordinate':<22} {'r':>7} {'p':>10}")
    print(f"  {'─'*46}")

    pc_correlations = {}
    for pc_idx in range(min(5, len(scores[0]))):
        pc_scores = scores[:, pc_idx]
        best_coords = []
        for name, values in coords.items():
            r, p = pearsonr(pc_scores, values)
            best_coords.append((name, r, p))
        best_coords.sort(key=lambda x: -abs(x[1]))
        pc_correlations[pc_idx] = best_coords

        for name, r, p in best_coords[:5]:
            if abs(r) > 0.25:
                sig = "*" if p < 0.05 else ""
                print(f"  PC{pc_idx+1:<3} {name:<22} {r:>7.3f} {p:>10.4f} {sig}")

    return scores, pca, var_explained, pc_correlations


# ═══════════════════════════════════════════════════════
# Part B: Complement axis analysis
# ═══════════════════════════════════════════════════════

def part_b(centroids, atlas):
    print(f"\n\n{'='*70}")
    print("PART B: Complement axis analysis")
    print("=" * 70)

    # Build complement pairs (take h < complement(h))
    pairs = []
    for h in range(N_HEX):
        c = int(atlas[str(h)]['complement'])
        if h < c:
            pairs.append((h, c))
    assert len(pairs) == 32

    # Pair-difference vectors: centroid_h - centroid_c
    diff_vectors = np.array([centroids[h] - centroids[c] for h, c in pairs])
    print(f"\n  32 complement pair-difference vectors, shape: {diff_vectors.shape}")

    # PCA on difference vectors
    pca_diff = PCA(n_components=min(20, 31))
    diff_scores = pca_diff.fit_transform(diff_vectors)
    var_diff = pca_diff.explained_variance_ratio_
    cumvar_diff = np.cumsum(var_diff)

    print(f"\n  PCA on pair-difference vectors:")
    print(f"  {'PC':<5} {'Var%':>8} {'Cumul%':>8}")
    print(f"  {'─'*23}")
    for i in range(min(10, len(var_diff))):
        print(f"  PC{i+1:<3} {var_diff[i]*100:>7.2f}% {cumvar_diff[i]*100:>7.2f}%")

    n90 = np.searchsorted(cumvar_diff, 0.90) + 1
    print(f"\n  Components for 90%: {n90}")
    if n90 <= 3:
        print(f"  → Complement opposition is LOW-DIMENSIONAL ({n90} axes)")
    else:
        print(f"  → Complement opposition is MULTI-DIMENSIONAL ({n90} axes)")

    # Alignment test: cosine similarity among difference vectors
    diff_sims = cosine_similarity(diff_vectors)
    upper_tri = diff_sims[np.triu_indices(32, k=1)]
    print(f"\n  Pairwise alignment of difference vectors:")
    print(f"    Mean cosine similarity: {upper_tri.mean():.4f}")
    print(f"    Std: {upper_tri.std():.4f}")
    print(f"    Range: [{upper_tri.min():.4f}, {upper_tri.max():.4f}]")
    if upper_tri.mean() > 0.3:
        print(f"    → Difference vectors are ALIGNED (shared opposition direction)")
    elif upper_tri.mean() > 0.1:
        print(f"    → Difference vectors are MODERATELY aligned")
    else:
        print(f"    → Difference vectors are DIVERSE (each pair opposes its own way)")

    # Primary complement axis: PC1 of diff vectors
    comp_axis = pca_diff.components_[0]  # unit vector
    print(f"\n  Primary complement axis (PC1 of diff vectors):")
    print(f"    Explains {var_diff[0]*100:.1f}% of complement opposition variance")

    # Project all 64 hex centroids onto complement axis
    comp_projections = centroids @ comp_axis
    # Check: do complements project to opposite values?
    comp_proj_corr = []
    for h, c in pairs:
        comp_proj_corr.append((comp_projections[h], comp_projections[c]))
    proj_h = np.array([p[0] for p in comp_proj_corr])
    proj_c = np.array([p[1] for p in comp_proj_corr])
    r, p = pearsonr(proj_h, proj_c)
    print(f"    Correlation of complement projections: r={r:.3f}, p={p:.6f}")
    print(f"    (Expected: strongly negative if axis captures complement opposition)")

    return diff_vectors, pca_diff, comp_axis, pairs


# ═══════════════════════════════════════════════════════
# Part C: Beyond complement
# ═══════════════════════════════════════════════════════

def part_c(raw_centroids, atlas):
    # Uses RAW hex centroids: tests structural predictors on unmanipulated
    # data. Residual centroids show regression artifacts (partial correlation
    # reversal) that make all predictors appear negatively correlated.
    print(f"\n\n{'='*70}")
    print("PART C: Beyond complement — what else organizes the manifold?")
    print("=" * 70)

    print(f"\n  Testing on RAW hex centroids (not residuals — avoids regression artifacts)")

    # Similarity matrix on raw hex centroids
    sim_matrix = cosine_similarity(raw_centroids)

    # Test various structural predictors
    print(f"\n  Structural predictors of semantic similarity (raw embeddings):")
    print(f"  {'Predictor':<35} {'Mantel r':>10} {'p':>10}")
    print(f"  {'─'*57}")

    # Build predictor matrices
    n = N_HEX

    # 1. King Wen proximity
    kw = [int(atlas[str(h)]['kw_number']) for h in range(n)]
    kw_dist = squareform(pdist(np.array(kw).reshape(-1, 1), metric='cityblock'))
    kw_prox = 1.0 / (1.0 + kw_dist)  # proximity
    _test_predictor("KW number proximity", sim_matrix, kw_prox)

    # 2. Same basin
    basins = [atlas[str(h)]['basin'] for h in range(n)]
    same_basin = np.array([[1 if basins[i] == basins[j] else 0
                            for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same basin", sim_matrix, same_basin)

    # 3. Same palace
    palaces = [atlas[str(h)]['palace'] for h in range(n)]
    same_palace = np.array([[1 if palaces[i] == palaces[j] else 0
                             for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same palace", sim_matrix, same_palace)

    # 4. Same surface relation
    surf = [atlas[str(h)]['surface_relation'] for h in range(n)]
    same_surf = np.array([[1 if surf[i] == surf[j] else 0
                           for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same surface relation", sim_matrix, same_surf)

    # 5. Same upper trigram
    upper = [atlas[str(h)]['upper_trigram']['val'] for h in range(n)]
    same_upper = np.array([[1 if upper[i] == upper[j] else 0
                            for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same upper trigram", sim_matrix, same_upper)

    # 6. Same lower trigram
    lower = [atlas[str(h)]['lower_trigram']['val'] for h in range(n)]
    same_lower = np.array([[1 if lower[i] == lower[j] else 0
                            for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same lower trigram", sim_matrix, same_lower)

    # 7. Shared ANY trigram (upper or lower)
    shared_tri = np.array([[1 if (upper[i] == upper[j] or lower[i] == lower[j] or
                                   upper[i] == lower[j] or lower[i] == upper[j]) else 0
                            for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Any shared trigram", sim_matrix, shared_tri)

    # 8. Hamming distance
    binaries = [atlas[str(h)]['binary'] for h in range(n)]
    ham_dist = np.array([[sum(a != b for a, b in zip(binaries[i], binaries[j]))
                          for j in range(n)] for i in range(n)], dtype=float)
    ham_prox = 1.0 - ham_dist / 6.0
    _test_predictor("Hamming proximity", sim_matrix, ham_prox)

    # 9. Nuclear hex sharing
    hu = [int(atlas[str(h)]['hu_hex']) for h in range(n)]
    same_hu = np.array([[1 if hu[i] == hu[j] else 0
                         for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same nuclear hexagram", sim_matrix, same_hu)

    # 10. Reverse pair
    rev = [int(atlas[str(h)]['reverse']) for h in range(n)]
    is_reverse = np.array([[1 if rev[i] == j else 0
                            for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Reverse pair", sim_matrix, is_reverse)

    # 11. Same i_component
    ic = [atlas[str(h)]['i_component'] for h in range(n)]
    same_ic = np.array([[1 if ic[i] == ic[j] else 0
                         for j in range(n)] for i in range(n)], dtype=float)
    _test_predictor("Same i_component", sim_matrix, same_ic)

    # 12. Hamming weight proximity
    hw = [sum(int(b) for b in atlas[str(h)]['binary']) for h in range(n)]
    hw_dist = squareform(pdist(np.array(hw).reshape(-1, 1), metric='cityblock'))
    hw_prox = 1.0 - hw_dist / 6.0
    _test_predictor("Hamming weight proximity", sim_matrix, hw_prox)

    # 13. KW sequence adjacency (Xugua)
    kw_adj = np.zeros((n, n))
    kw_to_hex = {atlas[str(h)]['kw_number']: h for h in range(n)}
    for kw_num in range(1, 64):
        if kw_num in kw_to_hex and kw_num + 1 in kw_to_hex:
            i, j = kw_to_hex[kw_num], kw_to_hex[kw_num + 1]
            kw_adj[i, j] = kw_adj[j, i] = 1
    _test_predictor("KW sequence adjacency (Xugua)", sim_matrix, kw_adj)

    return sim_matrix


def _test_predictor(name, sim_matrix, pred_matrix):
    """Mantel-like test: Pearson correlation between upper triangles."""
    n = sim_matrix.shape[0]
    idx = np.triu_indices(n, k=1)
    sim_vec = sim_matrix[idx]
    pred_vec = pred_matrix[idx]

    # Skip if predictor is constant
    if pred_vec.std() == 0:
        print(f"  {name:<35} {'N/A':>10} {'(constant)':>10}")
        return

    r, p = pearsonr(sim_vec, pred_vec)
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"  {name:<35} {r:>10.4f} {p:>10.4f} {sig}")


# ═══════════════════════════════════════════════════════
# Part D: Intra-hexagram narrative structure
# ═══════════════════════════════════════════════════════

def part_d(yaoci, atlas):
    # Uses RAW embeddings: position was regressed out of residuals, so all
    # positional effects are zero by construction in the residual. Raw
    # embeddings retain the positional structure we want to measure.
    print(f"\n\n{'='*70}")
    print("PART D: Intra-hexagram narrative structure")
    print("=" * 70)

    # Extract 6-line trajectories per hexagram
    trajectories = np.array([yaoci[h*6:(h+1)*6] for h in range(N_HEX)])  # (64, 6, 1024)

    # Center each trajectory at its hex centroid
    centroids = trajectories.mean(axis=1, keepdims=True)  # (64, 1, 1024)
    centered = trajectories - centroids  # (64, 6, 1024)

    # Average trajectory (mean over all 64 hexagrams)
    mean_traj = centered.mean(axis=0)  # (6, 1024)

    # Directional consistency: for each hex, measure how linearly the 6 points progress
    # Use: fraction of variance explained by a linear fit (position 0..5 → embedding)
    linearities = []
    for h in range(N_HEX):
        positions = np.arange(6).reshape(-1, 1).astype(float)
        traj = centered[h]  # (6, 1024)
        reg = LinearRegression()
        reg.fit(positions, traj)
        pred = reg.predict(positions)
        total_var = np.var(traj, axis=0).sum()
        resid_var = np.var(traj - pred, axis=0).sum()
        r2 = 1 - resid_var / total_var if total_var > 0 else 0
        linearities.append(r2)

    linearities = np.array(linearities)
    print(f"\n  Directional consistency (linearity R² of 6-line trajectory):")
    print(f"    Mean: {linearities.mean():.4f}")
    print(f"    Std:  {linearities.std():.4f}")
    print(f"    Range: [{linearities.min():.4f}, {linearities.max():.4f}]")
    print(f"    Expected if random: ~1/5 = 0.200 (1 predictor, 6 points, 5 df)")

    # Most/least linear hexagrams
    order = np.argsort(linearities)
    print(f"\n  Most linear trajectories:")
    for h in order[-5:]:
        print(f"    Hex {h} ({atlas[str(h)]['kw_name']}): R²={linearities[h]:.4f}")
    print(f"  Least linear trajectories:")
    for h in order[:5]:
        print(f"    Hex {h} ({atlas[str(h)]['kw_name']}): R²={linearities[h]:.4f}")

    # Mean trajectory shape: cosine similarity between consecutive positions
    print(f"\n  Mean trajectory (averaged over 64 hexagrams):")
    print(f"    Cosine similarity between consecutive mean positions:")
    for i in range(5):
        sim = cosine_similarity(mean_traj[i:i+1], mean_traj[i+1:i+2])[0, 0]
        print(f"      L{i+1}→L{i+2}: {sim:.4f}")

    # Mean trajectory: magnitude at each position (how far from centroid?)
    magnitudes = np.linalg.norm(mean_traj, axis=1)
    print(f"\n    Magnitude (distance from centroid) at each position:")
    for i in range(6):
        print(f"      L{i+1}: {magnitudes[i]:.4f}")

    # PCA on mean trajectory: what's the main direction of the narrative arc?
    pca_traj = PCA(n_components=5)
    traj_scores = pca_traj.fit_transform(mean_traj)
    print(f"\n    PCA of mean trajectory (6 points in 1024-dim):")
    for i in range(5):
        print(f"      PC{i+1}: {pca_traj.explained_variance_ratio_[i]*100:.1f}%")
    print(f"      PC1 scores by position: {traj_scores[:, 0].round(4).tolist()}")

    # Is the PC1 score monotonic in position? (narrative arc test)
    pc1_scores = traj_scores[:, 0]
    # Spearman correlation with position
    rho, p = spearmanr(np.arange(6), pc1_scores)
    print(f"      PC1 vs position: Spearman ρ={rho:.3f}, p={p:.4f}")
    if abs(rho) > 0.8:
        direction = "ascending" if rho > 0 else "descending"
        print(f"      → Strong monotonic narrative arc ({direction})")
    elif abs(rho) > 0.5:
        print(f"      → Moderate narrative arc")
    else:
        print(f"      → No clear monotonic arc")

    # Cross-hexagram trajectory variance
    # How much do individual hex trajectories deviate from the mean trajectory?
    traj_devs = centered - mean_traj[np.newaxis, :, :]  # (64, 6, 1024)
    mean_var = np.var(mean_traj, axis=0).sum()
    dev_var = np.var(traj_devs.reshape(-1, 1024), axis=0).sum()
    total_var = np.var(centered.reshape(-1, 1024), axis=0).sum()
    shared_frac = mean_var / total_var if total_var > 0 else 0
    print(f"\n  Trajectory variance decomposition:")
    print(f"    Shared (mean trajectory): {shared_frac*100:.2f}%")
    print(f"    Hex-specific deviation: {(1-shared_frac)*100:.2f}%")

    # Position-pair similarity: are certain position pairs semantically close
    # across all hexagrams?
    print(f"\n  Position-pair similarity (mean cosine across all hexagrams):")
    pos_sims = np.zeros((6, 6))
    for h in range(N_HEX):
        s = cosine_similarity(centered[h])
        pos_sims += s
    pos_sims /= N_HEX
    print(f"  {'':>6}", end="")
    for j in range(6):
        print(f"  L{j+1:>3}", end="")
    print()
    for i in range(6):
        print(f"    L{i+1}", end="")
        for j in range(6):
            print(f"  {pos_sims[i,j]:>5.3f}", end="")
        print()

    # Classical pairing test: are (L1,L4), (L2,L5), (L3,L6) more similar?
    classical_pairs = [(0, 3), (1, 4), (2, 5)]
    non_classical = [(i, j) for i in range(6) for j in range(i+1, 6)
                     if (i, j) not in classical_pairs]
    classical_sims = [pos_sims[i, j] for i, j in classical_pairs]
    non_classical_sims = [pos_sims[i, j] for i, j in non_classical]
    print(f"\n  Classical position pairs (L1↔L4, L2↔L5, L3↔L6):")
    for i, j in classical_pairs:
        print(f"    L{i+1}↔L{j+1}: {pos_sims[i,j]:.4f}")
    print(f"    Mean classical: {np.mean(classical_sims):.4f}")
    print(f"    Mean non-classical: {np.mean(non_classical_sims):.4f}")

    return linearities, mean_traj


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 2: Geometry of the Thematic Manifold")
    print("=" * 70)

    # Load and extract residuals
    yaoci, meta, atlas = load_data()
    X, feature_names = build_design_matrix(meta)
    residual, r_squared, _ = extract_residuals(yaoci, X)
    print(f"  Residual: {(1-r_squared)*100:.1f}% of variance ({residual.shape})")

    centroids = hex_centroids(residual)
    print(f"  Hex centroids (residual): {centroids.shape}")

    # Parts A & B use residual centroids (algebra removed, hex-thematic layer)
    # Part A
    scores, pca, var_explained, pc_corrs = part_a(centroids, atlas)

    # Part B
    diff_vectors, pca_diff, comp_axis, pairs = part_b(centroids, atlas)

    # Parts C & D use RAW embeddings: Part C tests structural predictors on
    # unmanipulated data; Part D measures positional effects that were removed
    # in the regression residuals.
    raw_centroids = np.array([yaoci[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])

    # Part C
    sim_matrix = part_c(raw_centroids, atlas)

    # Part D
    linearities, mean_traj = part_d(yaoci, atlas)

    # ═══════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print("=" * 70)

    print(f"""
  Part A — Principal axes:
    Top 5 PCs explain: {np.cumsum(var_explained)[:5][-1]*100:.1f}% of hex-centroid variance
    PC1: {var_explained[0]*100:.1f}%
    Dominant correlates: see above

  Part B — Complement axis:
    Pair-difference PC1: {pca_diff.explained_variance_ratio_[0]*100:.1f}% of complement variance
    Complement is {'low-dimensional' if np.searchsorted(np.cumsum(pca_diff.explained_variance_ratio_), 0.90) + 1 <= 5 else 'multi-dimensional'}

  Part C — Beyond complement:
    Best structural predictor of raw semantic similarity: (see table above)

  Part D — Narrative structure (raw embeddings):
    Mean trajectory linearity: {linearities.mean():.4f} (expected random: 0.200)
    Shared narrative arc: {np.var(mean_traj, axis=0).sum() / np.var(yaoci.reshape(64,6,1024) - yaoci.reshape(64,6,1024).mean(axis=1, keepdims=True), axis=(0,1)).sum() * 100 if True else 0:.2f}% of within-hex variance
""")


if __name__ == '__main__':
    main()
