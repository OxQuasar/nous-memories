"""S5: 爻辭 Full Analysis — raw clusters, positional signatures, stripped comparison."""

import json
import numpy as np
import requests
from pathlib import Path
from collections import Counter, defaultdict
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from scipy import stats
from scipy.spatial.distance import pdist, squareform, cosine as cosine_dist

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"
ATLAS_PATH = ROOT.parent / "atlas" / "atlas.json"
EMBED_URL = "http://localhost:8103/embed"


def load_data():
    emb = np.load(ROOT.parent / "synthesis" / "embeddings.npz")
    yaoci_emb = emb["yaoci"]  # (384, 1024) ordered by kw_number then line

    with open(TEXTS / "yaoci.json") as f:
        yaoci_texts = json.load(f)["entries"]
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)

    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    lines = []
    for entry in yaoci_texts:
        hv = kw_to_hexval[entry["number"]]
        for j, line in enumerate(entry["lines"]):
            lines.append({
                "hex_val": hv,
                "kw_number": entry["number"],
                "name": entry["name"],
                "line": j,
                "label": line["label"],
                "text": line["text"],
            })

    return yaoci_emb, lines, atlas, kw_to_hexval


def embed_texts(texts):
    """Embed via RAG server."""
    resp = requests.post(EMBED_URL, json={"texts": texts})
    resp.raise_for_status()
    return np.array(resp.json()["embeddings"])


# ══════════════════════════════════════════════════════════════════════════════
# Part A: Raw cluster characterization
# ══════════════════════════════════════════════════════════════════════════════

def char_bigrams(text):
    """Extract character bigrams from Chinese text."""
    # Filter punctuation
    clean = "".join(c for c in text if "\u4e00" <= c <= "\u9fff")
    return [clean[i:i+2] for i in range(len(clean) - 1)]


def distinctive_vocab(labels, lines, k):
    """Find bigrams significantly more frequent in each cluster vs rest."""
    cluster_bigrams = defaultdict(Counter)
    for i, line in enumerate(lines):
        bgs = char_bigrams(line["text"])
        cluster_bigrams[labels[i]].update(bgs)

    # Compute total counts
    total = Counter()
    for c in cluster_bigrams.values():
        total.update(c)

    results = {}
    for cid in range(k):
        in_count = cluster_bigrams[cid]
        in_size = sum(1 for l in labels if l == cid)
        out_size = len(labels) - in_size

        scored = []
        for bg, cnt in in_count.items():
            if cnt < 3:
                continue
            out_cnt = total[bg] - cnt
            in_rate = cnt / in_size
            out_rate = (out_cnt / out_size) if out_size > 0 else 0
            ratio = in_rate / out_rate if out_rate > 0 else float("inf")
            if ratio > 1.5:
                scored.append((bg, ratio, cnt))
        scored.sort(key=lambda x: -x[1])
        results[cid] = scored[:15]
    return results


def cluster_analysis(yaoci_emb, lines, k):
    """Full cluster analysis at given k."""
    km = KMeans(n_clusters=k, n_init=20, random_state=42)
    labels = km.fit_predict(yaoci_emb)

    clusters = []
    for cid in range(k):
        mask = labels == cid
        members_idx = np.where(mask)[0]
        centroid = yaoci_emb[mask].mean(axis=0)
        dists = np.linalg.norm(yaoci_emb[mask] - centroid, axis=1)
        order = np.argsort(dists)

        nearest = [
            {"name": lines[members_idx[i]]["name"],
             "line": lines[members_idx[i]]["line"] + 1,
             "text": lines[members_idx[i]]["text"]}
            for i in order[:5]
        ]

        # Position distribution
        pos_counts = Counter(lines[idx]["line"] for idx in members_idx)

        # Hexagram distribution
        hex_counts = Counter(lines[idx]["hex_val"] for idx in members_idx)

        clusters.append({
            "id": int(cid),
            "size": int(mask.sum()),
            "nearest_5": nearest,
            "position_counts": {str(p): int(pos_counts.get(p, 0)) for p in range(6)},
            "n_hexagrams_represented": len(hex_counts),
            "hexagram_max_lines": max(hex_counts.values()),
        })

    # Cross-tab: cluster × position
    ct_pos = np.zeros((k, 6), dtype=int)
    for i, line in enumerate(lines):
        ct_pos[labels[i], line["line"]] += 1
    chi2_pos, p_pos, _, _ = stats.chi2_contingency(ct_pos)

    # Cross-tab: cluster × hexagram
    n_hex_coherent = 0  # hexagrams with all 6 lines in same cluster
    for hv in range(64):
        hex_mask = [i for i, l in enumerate(lines) if l["hex_val"] == hv]
        if len(hex_mask) == 6:
            hex_labels = set(labels[i] for i in hex_mask)
            if len(hex_labels) == 1:
                n_hex_coherent += 1

    # Distinctive vocab
    dist_vocab = distinctive_vocab(labels, lines, k)

    return {
        "k": k,
        "labels": labels.tolist(),
        "clusters": clusters,
        "position_chi2": {"chi2": float(chi2_pos), "p": float(p_pos)},
        "hexagram_coherent_count": n_hex_coherent,
        "distinctive_vocab": {
            str(cid): [{"bigram": bg, "ratio": round(r, 2), "count": c}
                       for bg, r, c in items]
            for cid, items in dist_vocab.items()
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# Part B: Positional signatures
# ══════════════════════════════════════════════════════════════════════════════

def positional_analysis(yaoci_emb, lines):
    """Position centroids, pairwise distances, PERMANOVA."""
    positions = np.array([l["line"] for l in lines])

    # Centroids per position
    centroids = np.zeros((6, yaoci_emb.shape[1]))
    for p in range(6):
        centroids[p] = yaoci_emb[positions == p].mean(axis=0)

    # Pairwise cosine distances between centroids
    cos_dist_matrix = np.zeros((6, 6))
    for i in range(6):
        for j in range(6):
            if i != j:
                cos_dist_matrix[i, j] = cosine_dist(centroids[i], centroids[j])

    # PERMANOVA (pseudo-F using distance matrix)
    dist_mat = squareform(pdist(yaoci_emb, metric="cosine"))
    n = len(positions)
    groups = [np.where(positions == p)[0] for p in range(6)]

    # SS_within and SS_between
    ss_total = 0
    ss_within = 0
    grand_mean_dist = dist_mat.mean()

    for g in groups:
        if len(g) > 1:
            within_dists = dist_mat[np.ix_(g, g)]
            ss_within += within_dists.sum() / (2 * len(g))

    ss_total_all = dist_mat.sum() / (2 * n)
    ss_between = ss_total_all - ss_within

    k_groups = 6
    pseudo_f = (ss_between / (k_groups - 1)) / (ss_within / (n - k_groups))

    # Permutation test for PERMANOVA
    np.random.seed(42)
    n_perm = 999
    perm_fs = []
    for _ in range(n_perm):
        perm_pos = np.random.permutation(positions)
        perm_groups = [np.where(perm_pos == p)[0] for p in range(6)]
        perm_ss_within = 0
        for g in perm_groups:
            if len(g) > 1:
                perm_ss_within += dist_mat[np.ix_(g, g)].sum() / (2 * len(g))
        perm_ss_between = ss_total_all - perm_ss_within
        perm_f = (perm_ss_between / (k_groups - 1)) / (perm_ss_within / (n - k_groups))
        perm_fs.append(perm_f)
    p_value = (np.sum(np.array(perm_fs) >= pseudo_f) + 1) / (n_perm + 1)

    # Hierarchy grouping: {0,5}={1,6}, {1,4}={2,5}, {2,3}={3,4}
    hierarchy_pairs = [(0, 5), (1, 4), (2, 3)]
    hierarchy_dists = {f"({p1+1},{p2+1})": float(cos_dist_matrix[p1, p2])
                       for p1, p2 in hierarchy_pairs}
    non_hierarchy = [(i, j) for i in range(6) for j in range(i+1, 6)
                     if (i, j) not in hierarchy_pairs]
    non_hier_dists = [float(cos_dist_matrix[i, j]) for i, j in non_hierarchy]

    return {
        "centroid_cosine_distances": cos_dist_matrix.tolist(),
        "permanova": {"pseudo_F": float(pseudo_f), "p_value": float(p_value)},
        "hierarchy_distances": hierarchy_dists,
        "hierarchy_mean": float(np.mean(list(hierarchy_dists.values()))),
        "non_hierarchy_mean": float(np.mean(non_hier_dists)),
    }


# ══════════════════════════════════════════════════════════════════════════════
# Part C: Stripped clustering (orthogonal projection)
# ══════════════════════════════════════════════════════════════════════════════

def stripped_analysis(yaoci_emb, lines):
    """Project out marker-related variance; compare clusters."""
    # Load marker matrix from S1
    with open(DATA / "stock_phrases.json") as f:
        sp = json.load(f)

    # Build binary marker matrix aligned with embeddings
    # S1 marker_matrix is ordered by kw_number then line (same as embeddings)
    markers = sp["markers"]
    n_markers = len(markers)
    marker_mat = np.zeros((384, n_markers), dtype=float)
    for i, entry in enumerate(sp["marker_matrix"]):
        for j, m in enumerate(markers):
            if m in entry["markers"]:
                marker_mat[i, j] = 1.0

    # Remove zero-variance columns
    active = marker_mat.var(axis=0) > 0
    X = marker_mat[:, active]

    # Center both before projection
    X_c = X - X.mean(axis=0)
    Y_c = yaoci_emb - yaoci_emb.mean(axis=0)

    # Orthogonal projection: residual = Y_c - X_c @ (X_c^T X_c)^{-1} X_c^T @ Y_c
    XtX_inv = np.linalg.pinv(X_c.T @ X_c)
    projection = X_c @ XtX_inv @ X_c.T
    residual_emb = Y_c - projection @ Y_c

    # Cluster residual at k=3
    km_raw = KMeans(n_clusters=3, n_init=20, random_state=42)
    labels_raw = km_raw.fit_predict(yaoci_emb)

    km_res = KMeans(n_clusters=3, n_init=20, random_state=42)
    labels_res = km_res.fit_predict(residual_emb)

    ari = adjusted_rand_score(labels_raw, labels_res)

    # How much variance was removed?
    var_raw = np.var(Y_c, axis=0).sum()
    var_res = np.var(residual_emb, axis=0).sum()
    var_removed_frac = 1 - var_res / var_raw

    return {
        "ari_raw_vs_stripped": float(ari),
        "variance_removed_fraction": float(var_removed_frac),
        "raw_labels": labels_raw.tolist(),
        "stripped_labels": labels_res.tolist(),
    }


def main():
    yaoci_emb, lines, atlas, kw_to_hexval = load_data()
    print(f"Loaded {yaoci_emb.shape[0]} yaoci embeddings ({yaoci_emb.shape[1]}-dim)")

    # ── Part A ──
    print("\n" + "=" * 60)
    print("PART A: Raw Cluster Characterization")
    print("=" * 60)

    results_by_k = {}
    for k in [3, 5]:
        res = cluster_analysis(yaoci_emb, lines, k)
        results_by_k[k] = res

        print(f"\n{'─'*40}")
        print(f"k={k}: position χ²={res['position_chi2']['chi2']:.1f} "
              f"p={res['position_chi2']['p']:.4f}, "
              f"hex-coherent={res['hexagram_coherent_count']}/64")

        for cl in res["clusters"]:
            print(f"\n  Cluster {cl['id']} (n={cl['size']}):")
            print(f"    Position distribution: {cl['position_counts']}")
            print(f"    Hexagrams represented: {cl['n_hexagrams_represented']}, "
                  f"max lines from one hex: {cl['hexagram_max_lines']}")
            print(f"    Nearest to centroid:")
            for t in cl["nearest_5"]:
                print(f"      {t['name']} line {t['line']}: {t['text']}")

        print(f"\n  Distinctive vocabulary (k={k}):")
        for cid, items in res["distinctive_vocab"].items():
            top = ", ".join(f"{it['bigram']}({it['ratio']:.1f}x)" for it in items[:8])
            print(f"    Cluster {cid}: {top}")

    # Dominant structure determination
    k3 = results_by_k[3]
    pos_significant = k3["position_chi2"]["p"] < 0.01
    hex_coherent_high = k3["hexagram_coherent_count"] > 10
    if pos_significant:
        dominant = "positional"
    elif hex_coherent_high:
        dominant = "hexagrammatic"
    else:
        dominant = "thematic"
    print(f"\n  >>> Dominant structure: {dominant}")

    # ── Part B ──
    print("\n" + "=" * 60)
    print("PART B: Positional Signatures")
    print("=" * 60)

    pos_res = positional_analysis(yaoci_emb, lines)
    print(f"\n  PERMANOVA: pseudo-F={pos_res['permanova']['pseudo_F']:.2f}, "
          f"p={pos_res['permanova']['p_value']:.4f}")
    print(f"  Hierarchy pair distances: {pos_res['hierarchy_distances']}")
    print(f"  Hierarchy mean: {pos_res['hierarchy_mean']:.6f}")
    print(f"  Non-hierarchy mean: {pos_res['non_hierarchy_mean']:.6f}")

    # Print full centroid distance matrix
    cdm = np.array(pos_res["centroid_cosine_distances"])
    print("\n  Centroid cosine distance matrix:")
    print("      L1     L2     L3     L4     L5     L6")
    for i in range(6):
        row = " ".join(f"{cdm[i,j]:.4f}" for j in range(6))
        print(f"  L{i+1} {row}")

    # ── Part C ──
    print("\n" + "=" * 60)
    print("PART C: Stripped Clustering (Marker Projection)")
    print("=" * 60)

    strip_res = stripped_analysis(yaoci_emb, lines)
    print(f"\n  Variance removed by marker projection: {strip_res['variance_removed_fraction']:.4f}")
    print(f"  ARI (raw k=3 vs stripped k=3): {strip_res['ari_raw_vs_stripped']:.4f}")
    if strip_res["ari_raw_vs_stripped"] > 0.7:
        print("  → Clusters barely changed: markers are NOT driving cluster structure")
    elif strip_res["ari_raw_vs_stripped"] > 0.3:
        print("  → Moderate change: markers contribute but don't dominate")
    else:
        print("  → Clusters changed substantially: markers were significant")

    # ── Save ──
    output = {
        "part_a": {
            "k3": {
                "clusters": results_by_k[3]["clusters"],
                "position_chi2": results_by_k[3]["position_chi2"],
                "hexagram_coherent": results_by_k[3]["hexagram_coherent_count"],
                "distinctive_vocab": results_by_k[3]["distinctive_vocab"],
                "labels": results_by_k[3]["labels"],
            },
            "k5": {
                "clusters": results_by_k[5]["clusters"],
                "position_chi2": results_by_k[5]["position_chi2"],
                "hexagram_coherent": results_by_k[5]["hexagram_coherent_count"],
                "distinctive_vocab": results_by_k[5]["distinctive_vocab"],
                "labels": results_by_k[5]["labels"],
            },
            "dominant_structure": dominant,
        },
        "part_b": pos_res,
        "part_c": strip_res,
    }

    with open(DATA / "yaoci_clusters.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'yaoci_clusters.json'}")


if __name__ == "__main__":
    main()
