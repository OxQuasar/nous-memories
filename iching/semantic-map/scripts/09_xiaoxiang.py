"""S10: 小象 Full Analysis — vocab clusters, embeddings, algebraic residual."""

import json
import numpy as np
import requests
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from scipy import stats
from scipy.spatial.distance import pdist, squareform

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ATLAS_PATH = ROOT.parent / "atlas" / "atlas.json"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"
EMBED_URL = "http://localhost:8103/embed"

# Algebraic hierarchy grouping: {1,6}, {2,5}, {3,4}
HIERARCHY = {0: "outer", 5: "outer", 1: "middle", 4: "middle", 2: "inner", 3: "inner"}


def load_data():
    with open(DATA / "xiaoxiang_vocab.json") as f:
        xx_data = json.load(f)
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)

    feat_matrix = np.array(xx_data["feature_matrix"])  # 384 × N
    feat_names = xx_data["feature_names"]
    entries = xx_data["entries"]

    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    return xx_data, feat_matrix, feat_names, entries, atlas, kw_to_hexval


def vocab_clustering(feat_matrix, entries, atlas):
    """Cluster 384 小象 by vocabulary features."""
    results = {}

    for k in [3, 4, 6]:
        km = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels = km.fit_predict(feat_matrix.astype(float))

        # Cross-tab: cluster × position
        positions = np.array([e["line"] for e in entries])
        ct_pos = np.zeros((k, 6), dtype=int)
        for i in range(len(entries)):
            ct_pos[labels[i], positions[i]] += 1
        chi2_pos, p_pos, _, _ = stats.chi2_contingency(ct_pos)

        # Cross-tab: cluster × hierarchy
        hierarchy = np.array([HIERARCHY[e["line"]] for e in entries])
        hier_cats = sorted(set(hierarchy))
        ct_hier = np.zeros((k, len(hier_cats)), dtype=int)
        for i in range(len(entries)):
            ct_hier[labels[i], hier_cats.index(hierarchy[i])] += 1
        chi2_hier, p_hier, _, _ = stats.chi2_contingency(ct_hier)

        sil = silhouette_score(feat_matrix, labels) if k < len(feat_matrix) else 0

        results[k] = {
            "labels": labels.tolist(),
            "silhouette": float(sil),
            "position_chi2": {"chi2": float(chi2_pos), "p": float(p_pos)},
            "hierarchy_chi2": {"chi2": float(chi2_hier), "p": float(p_hier)},
            "position_crosstab": ct_pos.tolist(),
            "hierarchy_crosstab": ct_hier.tolist(),
        }

        print(f"\n  k={k}: sil={sil:.3f}")
        print(f"    Position χ²={chi2_pos:.1f} p={p_pos:.6f}")
        print(f"    Hierarchy χ²={chi2_hier:.1f} p={p_hier:.6f}")
        print(f"    Position crosstab:")
        print(f"      {'':8s} " + " ".join(f"L{p+1:d}" for p in range(6)))
        for c in range(k):
            print(f"      Cl {c:d}:   " + "  ".join(f"{ct_pos[c, p]:2d}" for p in range(6)))

    return results


def embed_xiaoxiang():
    """Embed 384 小象 texts via RAG server."""
    with open(TEXTS / "xiangzhuan.json") as f:
        xiang = json.load(f)["entries"]

    texts = []
    for entry in xiang:
        for j in range(min(6, len(entry["xiaoxiang"]))):
            texts.append(entry["xiaoxiang"][j])

    print(f"\n  Embedding {len(texts)} 小象 texts...")
    resp = requests.post(EMBED_URL, json={"texts": texts})
    resp.raise_for_status()
    embeddings = np.array(resp.json()["embeddings"])
    print(f"  Shape: {embeddings.shape}")
    return embeddings


def embedding_clustering(emb, feat_matrix, entries, atlas):
    """Cluster 小象 embeddings, compare with vocab clusters."""
    results = {}

    for k in [3, 6]:
        km_emb = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels_emb = km_emb.fit_predict(emb)

        km_vocab = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels_vocab = km_vocab.fit_predict(feat_matrix.astype(float))

        ari = adjusted_rand_score(labels_emb, labels_vocab)

        # Cross-tab with position
        positions = np.array([e["line"] for e in entries])
        ct_pos = np.zeros((k, 6), dtype=int)
        for i in range(len(entries)):
            ct_pos[labels_emb[i], positions[i]] += 1
        chi2_pos, p_pos, _, _ = stats.chi2_contingency(ct_pos)

        sil = silhouette_score(emb, labels_emb)

        results[k] = {
            "labels_emb": labels_emb.tolist(),
            "ari_vs_vocab": float(ari),
            "silhouette": float(sil),
            "position_chi2": {"chi2": float(chi2_pos), "p": float(p_pos)},
        }

        print(f"\n  Embedding k={k}: sil={sil:.3f}, ARI vs vocab={ari:.3f}")
        print(f"    Position χ²={chi2_pos:.1f} p={p_pos:.6f}")

    return results


def residual_algebraic_signal(emb, entries, atlas):
    """After controlling for position, is there residual algebraic signal?"""
    print("\n  Residual algebraic signal (controlling for position):")

    positions = np.array([e["line"] for e in entries])
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    # Get algebraic coords per line
    basins = []
    surface_rels = []
    for entry in entries:
        h = atlas[str(entry["hex_val"])]
        basins.append(h["basin"])
        surface_rels.append(h["surface_relation"])
    basins = np.array(basins)
    surface_rels = np.array(surface_rels)

    # Distance matrix
    dist_mat = squareform(pdist(emb, metric="cosine"))

    # PERMANOVA: position alone
    n = len(positions)

    def ss_within(grouping):
        ss_w = 0
        for g in np.unique(grouping):
            idx = np.where(grouping == g)[0]
            if len(idx) > 1:
                ss_w += dist_mat[np.ix_(idx, idx)].sum() / (2 * len(idx))
        return ss_w

    ss_total = dist_mat.sum() / (2 * n)

    # Position R²
    ss_w_pos = ss_within(positions)
    r2_pos = 1 - ss_w_pos / ss_total

    # Combined: position × basin (interaction groups)
    combined_pos_basin = np.array([f"{p}_{b}" for p, b in zip(positions, basins)])
    ss_w_combined = ss_within(combined_pos_basin)
    r2_combined = 1 - ss_w_combined / ss_total

    r2_basin_residual = r2_combined - r2_pos

    # Combined: position × surface_relation
    combined_pos_sr = np.array([f"{p}_{s}" for p, s in zip(positions, surface_rels)])
    ss_w_combined_sr = ss_within(combined_pos_sr)
    r2_combined_sr = 1 - ss_w_combined_sr / ss_total

    r2_sr_residual = r2_combined_sr - r2_pos

    print(f"    Position R²: {r2_pos:.4f}")
    print(f"    Position + Basin R²: {r2_combined:.4f} (basin residual: {r2_basin_residual:.4f})")
    print(f"    Position + SurfRel R²: {r2_combined_sr:.4f} (srel residual: {r2_sr_residual:.4f})")

    # Permutation test for basin residual
    rng = np.random.RandomState(42)
    n_perm = 999
    perm_count = 0
    for _ in range(n_perm):
        # Permute basin labels within each position group
        perm_basins = basins.copy()
        for p in range(6):
            mask = positions == p
            idx = np.where(mask)[0]
            perm_basins[idx] = rng.permutation(perm_basins[idx])
        perm_combined = np.array([f"{p}_{b}" for p, b in zip(positions, perm_basins)])
        perm_ss_w = ss_within(perm_combined)
        perm_r2 = 1 - perm_ss_w / ss_total
        perm_residual = perm_r2 - r2_pos
        if perm_residual >= r2_basin_residual:
            perm_count += 1
    p_residual = (perm_count + 1) / (n_perm + 1)
    print(f"    Basin residual p-value (controlling for position): {p_residual:.4f}")

    return {
        "position_R2": float(r2_pos),
        "position_basin_R2": float(r2_combined),
        "basin_residual_R2": float(r2_basin_residual),
        "basin_residual_p": float(p_residual),
        "position_srel_R2": float(r2_combined_sr),
        "srel_residual_R2": float(r2_sr_residual),
    }


def main():
    xx_data, feat_matrix, feat_names, entries, atlas, kw_to_hexval = load_data()
    print(f"Loaded {len(entries)} 小象 entries, {feat_matrix.shape[1]} features")

    # ── Vocab clustering ──
    print("\n" + "=" * 60)
    print("Vocabulary-based clustering")
    print("=" * 60)
    vocab_res = vocab_clustering(feat_matrix, entries, atlas)

    # ── Embedding ──
    print("\n" + "=" * 60)
    print("Embedding-based clustering")
    print("=" * 60)
    xx_emb = embed_xiaoxiang()
    emb_res = embedding_clustering(xx_emb, feat_matrix, entries, atlas)

    # ── Residual signal ──
    print("\n" + "=" * 60)
    print("Residual algebraic signal")
    print("=" * 60)
    resid_res = residual_algebraic_signal(xx_emb, entries, atlas)

    output = {
        "vocab_clusters": {str(k): v for k, v in vocab_res.items()},
        "embedding_clusters": {str(k): v for k, v in emb_res.items()},
        "residual_signal": resid_res,
    }

    with open(DATA / "xiaoxiang_clusters.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'xiaoxiang_clusters.json'}")


if __name__ == "__main__":
    main()
