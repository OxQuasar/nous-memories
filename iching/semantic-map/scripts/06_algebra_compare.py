"""S7-continuous: Algebraic Comparison — residual thickness via RDA/PERMANOVA."""

import json
import numpy as np
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from scipy import stats
from scipy.spatial.distance import pdist, squareform

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ATLAS_PATH = ROOT.parent / "atlas" / "atlas.json"


def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)


def encode_algebraic(atlas):
    """Build algebraic coordinate matrix for 64 hexagrams (by kw_number order).

    Returns: feature_matrix (64 × n_features), feature_names, raw_coords
    """
    # Build kw_number → hex_val mapping
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    raw = []
    for kw in range(1, 65):
        hv = kw_to_hexval[kw]
        h = atlas[str(hv)]
        raw.append({
            "kw_number": kw,
            "hex_val": hv,
            "basin": h["basin"],
            "depth": h["depth"],
            "i_component": h["i_component"],
            "surface_relation": h["surface_relation"],
            "palace": h["palace"],
            "upper_element": h["surface_cell"][1],  # [lower, upper] in atlas
            "lower_element": h["surface_cell"][0],
        })

    # Encode features
    # Categorical: basin (3), surface_relation (5), palace (8), upper/lower_element (5 each)
    # Numeric: depth (0/1/2), i_component (0/1)

    feature_blocks = []
    feature_names = []

    # basin
    le = LabelEncoder()
    basin_enc = le.fit_transform([r["basin"] for r in raw])
    ohe = OneHotEncoder(sparse_output=False)
    basin_oh = ohe.fit_transform(basin_enc.reshape(-1, 1))
    for cat in le.classes_:
        feature_names.append(f"basin_{cat}")
    feature_blocks.append(basin_oh)

    # surface_relation
    le2 = LabelEncoder()
    sr_enc = le2.fit_transform([r["surface_relation"] for r in raw])
    sr_oh = OneHotEncoder(sparse_output=False).fit_transform(sr_enc.reshape(-1, 1))
    for cat in le2.classes_:
        feature_names.append(f"srel_{cat}")
    feature_blocks.append(sr_oh)

    # palace
    le3 = LabelEncoder()
    pal_enc = le3.fit_transform([r["palace"] for r in raw])
    pal_oh = OneHotEncoder(sparse_output=False).fit_transform(pal_enc.reshape(-1, 1))
    for cat in le3.classes_:
        feature_names.append(f"palace_{cat}")
    feature_blocks.append(pal_oh)

    # upper_element / lower_element
    for el_name in ["upper_element", "lower_element"]:
        le_el = LabelEncoder()
        el_enc = le_el.fit_transform([r[el_name] for r in raw])
        el_oh = OneHotEncoder(sparse_output=False).fit_transform(el_enc.reshape(-1, 1))
        for cat in le_el.classes_:
            feature_names.append(f"{el_name}_{cat}")
        feature_blocks.append(el_oh)

    # depth, i_component (numeric)
    depth = np.array([r["depth"] for r in raw], dtype=float).reshape(-1, 1)
    icomp = np.array([r["i_component"] for r in raw], dtype=float).reshape(-1, 1)
    feature_blocks.append(depth)
    feature_names.append("depth")
    feature_blocks.append(icomp)
    feature_names.append("i_component")

    X = np.hstack(feature_blocks)
    return X, feature_names, raw


def permanova_single(emb_dist, grouping, n_perm=999):
    """PERMANOVA for a single categorical variable."""
    n = len(grouping)
    groups = np.unique(grouping)
    k = len(groups)
    if k < 2:
        return {"pseudo_F": 0.0, "p_value": 1.0, "R2": 0.0}

    def compute_pseudo_f(labels):
        ss_total = emb_dist.sum() / (2 * n)
        ss_within = 0
        for g in np.unique(labels):
            idx = np.where(labels == g)[0]
            if len(idx) > 1:
                ss_within += emb_dist[np.ix_(idx, idx)].sum() / (2 * len(idx))
        ss_between = ss_total - ss_within
        if ss_within == 0:
            return float("inf"), ss_between / ss_total
        f = (ss_between / (k - 1)) / (ss_within / (n - k))
        r2 = ss_between / ss_total
        return f, r2

    real_f, r2 = compute_pseudo_f(grouping)

    perm_count = 0
    rng = np.random.RandomState(42)
    for _ in range(n_perm):
        perm_labels = rng.permutation(grouping)
        perm_f, _ = compute_pseudo_f(perm_labels)
        if perm_f >= real_f:
            perm_count += 1
    p = (perm_count + 1) / (n_perm + 1)

    return {"pseudo_F": float(real_f), "p_value": float(p), "R2": float(r2)}


def rda_variance(emb, X_design):
    """RDA: fraction of embedding variance explained by design matrix.

    Uses ordinary least squares: Ŷ = X(X'X)⁻¹X'Y, R² = SS(Ŷ)/SS(Y).
    """
    # Center embedding
    Y = emb - emb.mean(axis=0)
    # Center design matrix
    X = X_design - X_design.mean(axis=0)

    # Remove zero-variance columns
    active = X.var(axis=0) > 1e-10
    X = X[:, active]

    if X.shape[1] == 0:
        return 0.0

    # Hat matrix projection
    try:
        Y_hat = X @ np.linalg.pinv(X.T @ X) @ X.T @ Y
    except np.linalg.LinAlgError:
        return 0.0

    ss_total = np.sum(Y ** 2)
    ss_explained = np.sum(Y_hat ** 2)
    return float(ss_explained / ss_total) if ss_total > 0 else 0.0


def analyze_guaci(atlas):
    """Residual thickness for guaci (64 × 1024)."""
    emb = np.load(ROOT.parent / "synthesis" / "embeddings.npz")
    guaci = emb["guaci"]  # (64, 1024)

    # PCA
    pca = PCA()
    guaci_pca = pca.fit_transform(guaci)
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    n_comp = int(np.searchsorted(cumvar, 0.9)) + 1
    guaci_red = guaci_pca[:, :n_comp]

    print(f"  Guaci PCA: {n_comp} components for 90% variance")

    # Distance matrix
    dist_mat = squareform(pdist(guaci_red, metric="euclidean"))

    # Algebraic features
    X_alg, feat_names, raw_coords = encode_algebraic(atlas)

    # Per-coordinate PERMANOVA
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}
    coord_results = {}

    for coord_name in ["basin", "depth", "i_component", "surface_relation", "palace"]:
        grouping = np.array([raw_coords[i][coord_name] for i in range(64)])
        res = permanova_single(dist_mat, grouping)
        coord_results[coord_name] = res
        sig = "***" if res["p_value"] < 0.001 else "**" if res["p_value"] < 0.01 else \
              "*" if res["p_value"] < 0.05 else ""
        print(f"    {coord_name:20s}: R²={res['R2']:.4f}  F={res['pseudo_F']:.2f}  "
              f"p={res['p_value']:.4f} {sig}")

    # Joint RDA on full algebraic matrix
    joint_r2 = rda_variance(guaci_red, X_alg)
    print(f"    {'JOINT':20s}: R²={joint_r2:.4f}")

    residual = 1 - joint_r2
    print(f"\n    Residual thickness (guaci): {residual:.4f}")

    return {
        "n_pca_components": n_comp,
        "per_coordinate": coord_results,
        "joint_R2": joint_r2,
        "residual_thickness": residual,
    }


def analyze_yaoci(atlas):
    """Residual thickness for yaoci (384 × 1024)."""
    emb = np.load(ROOT.parent / "synthesis" / "embeddings.npz")
    yaoci = emb["yaoci"]  # (384, 1024)

    # PCA
    pca = PCA()
    yaoci_pca = pca.fit_transform(yaoci)
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    n_comp = int(np.searchsorted(cumvar, 0.9)) + 1
    yaoci_red = yaoci_pca[:, :n_comp]

    print(f"  Yaoci PCA: {n_comp} components for 90% variance")

    # Build per-line algebraic coords
    with open(Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching" / "yaoci.json") as f:
        yaoci_texts = json.load(f)["entries"]
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    line_positions = []
    line_coords = []
    for entry in yaoci_texts:
        hv = kw_to_hexval[entry["number"]]
        h = atlas[str(hv)]
        for j in range(6):
            line_positions.append(j)
            line_coords.append({
                "basin": h["basin"],
                "depth": h["depth"],
                "i_component": h["i_component"],
                "surface_relation": h["surface_relation"],
                "palace": h["palace"],
                "line_position": j,
            })

    line_positions = np.array(line_positions)
    dist_mat = squareform(pdist(yaoci_red, metric="euclidean"))

    # (a) Line position alone
    res_pos = permanova_single(dist_mat, line_positions)
    print(f"    Line position alone: R²={res_pos['R2']:.4f}  p={res_pos['p_value']:.4f}")

    # (b) Each algebraic coordinate alone
    alg_results = {}
    for coord in ["basin", "surface_relation", "palace"]:
        grouping = np.array([lc[coord] for lc in line_coords])
        res = permanova_single(dist_mat, grouping)
        alg_results[coord] = res
        sig = "***" if res["p_value"] < 0.001 else "**" if res["p_value"] < 0.01 else \
              "*" if res["p_value"] < 0.05 else ""
        print(f"    {coord:20s}: R²={res['R2']:.4f}  p={res['p_value']:.4f} {sig}")

    # (c) Joint: algebraic + position via RDA
    # Build design matrix for lines
    alg_X, _, _ = encode_algebraic(atlas)  # 64 features per hex
    # Expand to 384 (repeat each hex 6 times)
    alg_384 = np.zeros((384, alg_X.shape[1]))
    pos_oh = np.zeros((384, 6))
    idx = 0
    for kw in range(1, 65):
        for j in range(6):
            alg_384[idx] = alg_X[kw - 1]
            pos_oh[idx, j] = 1
            idx += 1

    # Algebraic only
    r2_alg = rda_variance(yaoci_red, alg_384)
    # Position only
    r2_pos = rda_variance(yaoci_red, pos_oh)
    # Joint
    X_joint = np.hstack([alg_384, pos_oh])
    r2_joint = rda_variance(yaoci_red, X_joint)

    print(f"\n    RDA — Algebraic alone: R²={r2_alg:.4f}")
    print(f"    RDA — Position alone:  R²={r2_pos:.4f}")
    print(f"    RDA — Joint:           R²={r2_joint:.4f}")
    print(f"\n    Residual thickness (yaoci): {1 - r2_joint:.4f}")

    return {
        "n_pca_components": n_comp,
        "position_permanova": res_pos,
        "per_coordinate": alg_results,
        "rda_algebraic_R2": r2_alg,
        "rda_position_R2": r2_pos,
        "rda_joint_R2": r2_joint,
        "residual_thickness": 1 - r2_joint,
    }


def main():
    atlas = load_atlas()

    print("=" * 60)
    print("GUACI (64 hexagrams)")
    print("=" * 60)
    guaci_res = analyze_guaci(atlas)

    print(f"\n{'=' * 60}")
    print("YAOCI (384 lines)")
    print("=" * 60)
    yaoci_res = analyze_yaoci(atlas)

    output = {
        "guaci": guaci_res,
        "yaoci": yaoci_res,
    }

    with open(DATA / "algebra_comparison.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'algebra_comparison.json'}")


if __name__ == "__main__":
    main()
