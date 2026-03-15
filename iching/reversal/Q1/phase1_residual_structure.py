#!/usr/bin/env python3
"""Q1 Phase 1: Residual extraction and intrinsic structure.

1. Load 384 yaoci embeddings + atlas coordinates
2. Build design matrix from ALL known algebraic coordinates + line position
3. Regress out algebraic signal → extract residual embeddings (the 89%)
4. Cluster residuals (not raw embeddings) — what structure lives beyond algebra?
5. Test whether any algebraic coordinate predicts residual cluster membership
6. Compare residual clusters to raw clusters from prior work
"""

import numpy as np
import json
from collections import Counter
from pathlib import Path

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, adjusted_rand_score
from scipy.stats import chi2_contingency
from scipy.spatial.distance import pdist, squareform

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
SYNTH = ROOT / "synthesis"
ATLAS = ROOT / "atlas" / "atlas.json"
PRIOR = ROOT / "semantic-map" / "data"


# ═══════════════════════════════════════════════════════
# Data loading
# ═══════════════════════════════════════════════════════

def load_data():
    emb = np.load(SYNTH / "embeddings.npz")
    yaoci = emb['yaoci']  # (384, 1024)
    assert yaoci.shape == (384, 1024)

    with open(ATLAS) as f:
        atlas = json.load(f)

    # Build per-yaoci metadata: yaoci i → hex i//6, line i%6
    meta = []
    for i in range(384):
        hex_idx = i // 6
        line_pos = i % 6  # 0-indexed (line 1 = 0)
        h = atlas[str(hex_idx)]
        meta.append({
            'hex_idx': hex_idx,
            'line_pos': line_pos,
            'basin': h['basin'],
            'surface_relation': h['surface_relation'],
            'palace': h['palace'],
            'palace_element': h['palace_element'],
            'rank': h['rank'],
            'depth': h['depth'],
            'i_component': h['i_component'],
            'inner_val': h['inner_val'],
            'hu_depth': h['hu_depth'],
            'shi': h['shi'],
            'ying': h['ying'],
        })

    return yaoci, meta, atlas


# ═══════════════════════════════════════════════════════
# Design matrix construction
# ═══════════════════════════════════════════════════════

def build_design_matrix(meta):
    """Build design matrix from all algebraic coordinates.

    Categorical: line_pos (6), basin (8), surface_relation (5), palace (8),
                 palace_element (5), rank (8)
    Numeric: depth, i_component, inner_val, hu_depth, shi, ying
    """
    n = len(meta)

    # Categorical features → one-hot
    cat_features = {
        'line_pos': [m['line_pos'] for m in meta],
        'basin': [m['basin'] for m in meta],
        'surface_relation': [m['surface_relation'] for m in meta],
        'palace': [m['palace'] for m in meta],
        'palace_element': [m['palace_element'] for m in meta],
        'rank': [m['rank'] for m in meta],
    }

    cat_arrays = []
    cat_names = []
    for name, values in cat_features.items():
        enc = OneHotEncoder(sparse_output=False, drop='first')
        arr = enc.fit_transform(np.array(values).reshape(-1, 1))
        categories = enc.categories_[0]
        for cat in categories[1:]:  # first is dropped
            cat_names.append(f"{name}={cat}")
        cat_arrays.append(arr)

    # Numeric features
    num_features = {
        'depth': [m['depth'] for m in meta],
        'i_component': [m['i_component'] for m in meta],
        'inner_val': [m['inner_val'] for m in meta],
        'hu_depth': [m['hu_depth'] for m in meta],
        'shi': [m['shi'] for m in meta],
        'ying': [m['ying'] for m in meta],
    }
    num_arrays = []
    num_names = []
    for name, values in num_features.items():
        arr = np.array(values, dtype=float).reshape(-1, 1)
        num_arrays.append(arr)
        num_names.append(name)

    X = np.hstack(cat_arrays + num_arrays)
    feature_names = cat_names + num_names

    return X, feature_names


# ═══════════════════════════════════════════════════════
# Residual extraction
# ═══════════════════════════════════════════════════════

def extract_residuals(yaoci, X):
    """Regress out algebraic coordinates from embeddings.

    OLS regression: Y = X·B + residual, per embedding dimension.
    Returns residuals (384, 1024).
    """
    reg = LinearRegression()
    reg.fit(X, yaoci)
    predicted = reg.predict(X)
    residual = yaoci - predicted

    # Variance explained
    total_var = np.var(yaoci, axis=0).sum()
    residual_var = np.var(residual, axis=0).sum()
    r_squared = 1 - residual_var / total_var

    return residual, r_squared, predicted


# ═══════════════════════════════════════════════════════
# Clustering
# ═══════════════════════════════════════════════════════

def cluster_analysis(embeddings, label, ks=range(2, 11)):
    """Multi-method clustering with silhouette evaluation."""
    results = {}

    # PCA for dimensionality reduction (clustering in top PCs)
    pca = PCA(n_components=50)
    reduced = pca.fit_transform(embeddings)
    var_explained = pca.explained_variance_ratio_.cumsum()
    n90 = np.searchsorted(var_explained, 0.90) + 1
    print(f"  [{label}] PCA: {n90} components for 90% variance")
    results['pca_n90'] = int(n90)
    results['pca_var_50'] = float(var_explained[49])

    # K-means sweep
    km_results = {}
    best_k, best_sil = 2, -1
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = km.fit_predict(reduced)
        sil = silhouette_score(reduced, labels)
        km_results[k] = {'silhouette': float(sil), 'labels': labels.tolist()}
        if sil > best_sil:
            best_k, best_sil = k, sil
    results['kmeans'] = {k: v['silhouette'] for k, v in km_results.items()}
    results['best_k'] = best_k
    results['best_sil'] = float(best_sil)
    print(f"  [{label}] Best k-means: k={best_k}, silhouette={best_sil:.4f}")

    # Ward hierarchical for the best k
    ward = AgglomerativeClustering(n_clusters=best_k)
    ward_labels = ward.fit_predict(reduced)
    ward_sil = silhouette_score(reduced, ward_labels)
    results['ward_sil'] = float(ward_sil)

    # DBSCAN
    scaler = StandardScaler()
    scaled = scaler.fit_transform(reduced[:, :n90])
    dbscan = DBSCAN(eps=2.0, min_samples=5)
    db_labels = dbscan.fit_predict(scaled)
    n_clusters_db = len(set(db_labels) - {-1})
    n_noise = (db_labels == -1).sum()
    results['dbscan_clusters'] = n_clusters_db
    results['dbscan_noise'] = int(n_noise)
    print(f"  [{label}] DBSCAN: {n_clusters_db} clusters, {n_noise} noise")

    # Cross-method stability (ARI)
    km_labels = km_results[best_k]['labels']
    ari_km_ward = adjusted_rand_score(km_labels, ward_labels)
    results['ari_km_ward'] = float(ari_km_ward)
    print(f"  [{label}] ARI(kmeans, ward) at k={best_k}: {ari_km_ward:.3f}")

    # Store labels for downstream analysis
    results['labels_kmeans'] = km_labels
    results['labels_ward'] = ward_labels.tolist()
    results['reduced'] = reduced

    return results


# ═══════════════════════════════════════════════════════
# Algebraic independence tests
# ═══════════════════════════════════════════════════════

def test_algebraic_independence(labels, meta):
    """Test whether any algebraic coordinate predicts cluster membership."""
    coords = {
        'line_pos': [m['line_pos'] for m in meta],
        'basin': [m['basin'] for m in meta],
        'surface_relation': [m['surface_relation'] for m in meta],
        'palace': [m['palace'] for m in meta],
        'palace_element': [m['palace_element'] for m in meta],
        'rank': [m['rank'] for m in meta],
        'depth': [m['depth'] for m in meta],
        'i_component': [m['i_component'] for m in meta],
    }

    results = {}
    for name, values in coords.items():
        # Build contingency table
        ct = {}
        for v, l in zip(values, labels):
            ct.setdefault(v, Counter())[l] += 1
        # Convert to array
        all_vals = sorted(ct.keys(), key=str)
        all_labels = sorted(set(labels))
        table = np.array([[ct[v].get(l, 0) for l in all_labels] for v in all_vals])

        # Skip if any dimension is 1
        if table.shape[0] < 2 or table.shape[1] < 2:
            continue

        chi2, p, dof, expected = chi2_contingency(table)
        cramer_v = np.sqrt(chi2 / (sum(sum(table)) * (min(table.shape) - 1)))
        results[name] = {
            'chi2': float(chi2),
            'p': float(p),
            'dof': int(dof),
            'cramer_v': float(cramer_v),
        }

    return results


# ═══════════════════════════════════════════════════════
# Cluster characterization
# ═══════════════════════════════════════════════════════

def characterize_clusters(labels, meta):
    """For each cluster, report over-represented hexagrams and positions."""
    n_clusters = len(set(labels))
    n = len(labels)

    print(f"\n  Cluster characterization:")
    for c in sorted(set(labels)):
        members = [i for i, l in enumerate(labels) if l == c]
        size = len(members)

        # Position distribution
        pos_dist = Counter(meta[i]['line_pos'] for i in members)
        pos_str = ", ".join(f"L{p+1}:{pos_dist.get(p,0)}" for p in range(6))

        # Basin distribution
        basin_dist = Counter(meta[i]['basin'] for i in members)
        top_basins = basin_dist.most_common(3)

        # How many distinct hexagrams?
        hex_set = set(meta[i]['hex_idx'] for i in members)

        print(f"    Cluster {c}: {size} yaoci, {len(hex_set)} hexagrams")
        print(f"      Positions: {pos_str}")
        print(f"      Top basins: {top_basins}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 1: Residual Extraction and Intrinsic Structure")
    print("=" * 70)

    # ── Load data ──
    print("\nStep 1: Load data")
    yaoci, meta, atlas = load_data()
    print(f"  Yaoci embeddings: {yaoci.shape}")
    print(f"  Metadata: {len(meta)} entries")

    # ── Build design matrix ──
    print("\nStep 2: Build design matrix")
    X, feature_names = build_design_matrix(meta)
    print(f"  Design matrix: {X.shape} ({len(feature_names)} features)")
    print(f"  Features: {feature_names[:10]}... (+ {len(feature_names)-10} more)")

    # ── Extract residuals ──
    print("\nStep 3: Regress out algebraic coordinates")
    residual, r_squared, predicted = extract_residuals(yaoci, X)
    residual_frac = 1 - r_squared
    print(f"  R² (all coordinates + position): {r_squared:.4f}")
    print(f"  Residual fraction: {residual_frac:.4f} ({residual_frac*100:.1f}%)")
    print(f"  Residual embedding shape: {residual.shape}")

    # Decompose: position-only vs algebra-only
    X_pos, _ = build_design_matrix_subset(meta, ['line_pos'])
    X_alg, _ = build_design_matrix_subset(meta, ['basin', 'surface_relation', 'palace',
                                                   'palace_element', 'rank'])
    _, r2_pos, _ = extract_residuals(yaoci, X_pos)
    _, r2_alg, _ = extract_residuals(yaoci, X_alg)
    print(f"  R² (position only): {r2_pos:.4f}")
    print(f"  R² (algebra only, no position): {r2_alg:.4f}")
    print(f"  R² (joint): {r_squared:.4f}")
    print(f"  Interaction/overlap: {r2_pos + r2_alg - r_squared:.4f}")

    # ── Cluster raw embeddings (baseline) ──
    print(f"\n{'='*70}")
    print("Step 4: Cluster RAW embeddings (baseline)")
    raw_clusters = cluster_analysis(yaoci, "RAW")

    # ── Cluster residual embeddings ──
    print(f"\n{'='*70}")
    print("Step 5: Cluster RESIDUAL embeddings (the 89%)")
    res_clusters = cluster_analysis(residual, "RESIDUAL")

    # ── Compare raw vs residual clusters ──
    print(f"\n{'='*70}")
    print("Step 6: Compare raw vs residual clusters")
    raw_labels = raw_clusters['labels_kmeans']
    res_labels = res_clusters['labels_kmeans']
    ari = adjusted_rand_score(raw_labels, res_labels)
    print(f"  ARI(raw k={raw_clusters['best_k']}, residual k={res_clusters['best_k']}): {ari:.3f}")

    # Also compare at matching k values
    for k in [3, 5]:
        km_raw = KMeans(n_clusters=k, n_init=10, random_state=42)
        km_res = KMeans(n_clusters=k, n_init=10, random_state=42)
        pca_raw = PCA(n_components=50).fit_transform(yaoci)
        pca_res = PCA(n_components=50).fit_transform(residual)
        l_raw = km_raw.fit_predict(pca_raw)
        l_res = km_res.fit_predict(pca_res)
        ari_k = adjusted_rand_score(l_raw, l_res)
        print(f"  ARI(raw, residual) at k={k}: {ari_k:.3f}")

    # ── Load prior raw cluster labels for comparison ──
    try:
        with open(PRIOR / "yaoci_clusters.json") as f:
            prior = json.load(f)
        prior_labels = prior['part_c']['raw_labels']
        ari_prior = adjusted_rand_score(prior_labels, raw_labels)
        print(f"  ARI(our raw k=3, prior raw k=3): {ari_prior:.3f}")
    except Exception as e:
        print(f"  [Could not load prior clusters: {e}]")

    # ── Test algebraic independence of residual clusters ──
    print(f"\n{'='*70}")
    print("Step 7: Algebraic independence of RESIDUAL clusters")
    best_k = res_clusters['best_k']
    print(f"  Using residual k-means labels (k={best_k})")
    indep = test_algebraic_independence(res_labels, meta)
    print(f"\n  {'Coordinate':<20} {'χ²':>8} {'p-value':>10} {'Cramér V':>10} {'Significant?':>14}")
    print(f"  {'─'*62}")
    for name, r in sorted(indep.items(), key=lambda x: x[1]['p']):
        sig = "✓ YES" if r['p'] < 0.05 else "no"
        print(f"  {name:<20} {r['chi2']:>8.2f} {r['p']:>10.4f} {r['cramer_v']:>10.4f} {sig:>14}")

    # Also test for RAW clusters (should show position)
    print(f"\n  Comparison: algebraic independence of RAW clusters (k={raw_clusters['best_k']}):")
    indep_raw = test_algebraic_independence(raw_labels, meta)
    for name, r in sorted(indep_raw.items(), key=lambda x: x[1]['p']):
        sig = "✓ YES" if r['p'] < 0.05 else "no"
        print(f"  {name:<20} {r['chi2']:>8.2f} {r['p']:>10.4f} {r['cramer_v']:>10.4f} {sig:>14}")

    # ── Characterize residual clusters ──
    print(f"\n{'='*70}")
    print("Step 8: Characterize residual clusters")
    characterize_clusters(res_labels, meta)

    print(f"\n  For comparison, RAW clusters:")
    characterize_clusters(raw_labels, meta)

    # ── Key findings ──
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"""
  Variance decomposition:
    Position only:     {r2_pos*100:.1f}%
    Algebra only:      {r2_alg*100:.1f}%
    Joint:             {r_squared*100:.1f}%
    RESIDUAL:          {residual_frac*100:.1f}%

  Raw embedding clusters:
    Best k={raw_clusters['best_k']}, silhouette={raw_clusters['best_sil']:.4f}
    DBSCAN: {raw_clusters['dbscan_clusters']} clusters, {raw_clusters['dbscan_noise']} noise

  Residual embedding clusters:
    Best k={res_clusters['best_k']}, silhouette={res_clusters['best_sil']:.4f}
    DBSCAN: {res_clusters['dbscan_clusters']} clusters, {res_clusters['dbscan_noise']} noise

  ARI(raw, residual) at best k: {ari:.3f}

  Key question: does the residual have structure?
    - If silhouette > 0.1 and stable across methods → YES, structure beyond algebra
    - If silhouette < 0.05 and DBSCAN finds 1 cluster → NO, residual is diffuse
    - If algebraic coordinates predict residual clusters → LEAKAGE (regression incomplete)
""")


def build_design_matrix_subset(meta, cat_names):
    """Build design matrix with only specified categorical features."""
    n = len(meta)
    cat_features = {}
    if 'line_pos' in cat_names:
        cat_features['line_pos'] = [m['line_pos'] for m in meta]
    for name in ['basin', 'surface_relation', 'palace', 'palace_element', 'rank']:
        if name in cat_names:
            cat_features[name] = [m[name] for m in meta]

    cat_arrays = []
    names = []
    for name, values in cat_features.items():
        enc = OneHotEncoder(sparse_output=False, drop='first')
        arr = enc.fit_transform(np.array(values).reshape(-1, 1))
        for cat in enc.categories_[0][1:]:
            names.append(f"{name}={cat}")
        cat_arrays.append(arr)

    # Numeric features always included
    num_features = {
        'depth': [m['depth'] for m in meta],
        'i_component': [m['i_component'] for m in meta],
        'inner_val': [m['inner_val'] for m in meta],
        'hu_depth': [m['hu_depth'] for m in meta],
        'shi': [m['shi'] for m in meta],
        'ying': [m['ying'] for m in meta],
    }
    num_arrays = []
    for name, values in num_features.items():
        arr = np.array(values, dtype=float).reshape(-1, 1)
        num_arrays.append(arr)
        names.append(name)

    if cat_arrays:
        X = np.hstack(cat_arrays + num_arrays)
    else:
        X = np.hstack(num_arrays)

    return X, names


if __name__ == '__main__':
    main()
