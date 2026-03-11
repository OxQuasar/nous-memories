"""S2: 卦辭 Clustering — cluster the 64 guaci embeddings."""

import json
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import linkage, fcluster

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"
ATLAS = ROOT.parent / "atlas" / "atlas.json"


def load_data():
    emb = np.load(ROOT.parent / "synthesis" / "embeddings.npz")
    guaci = emb["guaci"]  # (64, 1024)

    with open(TEXTS / "guaci.json") as f:
        texts = json.load(f)["entries"]

    with open(ATLAS) as f:
        atlas = json.load(f)
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    hex_info = []
    for entry in texts:
        hv = kw_to_hexval[entry["number"]]
        hex_info.append({
            "hex_val": hv,
            "kw_number": entry["number"],
            "name": entry["name"],
            "text": entry["text"],
        })
    return guaci, hex_info, atlas


def kmeans_sweep(X):
    scores = {}
    for k in range(2, 11):
        km = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels = km.fit_predict(X)
        scores[k] = float(silhouette_score(X, labels))
    optimal_k = max(scores, key=scores.get)
    return scores, optimal_k


def hierarchical_clustering(X, k, method="ward"):
    clust = AgglomerativeClustering(n_clusters=k, linkage=method)
    return clust.fit_predict(X)


def dbscan_clustering(X):
    """DBSCAN with k-distance knee detection."""
    nn = NearestNeighbors(n_neighbors=5)
    nn.fit(X)
    dists, _ = nn.kneighbors(X)
    k_dists = np.sort(dists[:, -1])

    # Find knee: max second derivative
    d1 = np.diff(k_dists)
    d2 = np.diff(d1)
    knee_idx = np.argmax(d2) + 2
    eps = float(k_dists[knee_idx])

    db = DBSCAN(eps=eps, min_samples=3)
    labels = db.fit_predict(X)
    return labels, eps


def build_cluster_details(X, labels, hex_info, k):
    """For each cluster: members, centroid distances."""
    clusters = []
    for cid in range(k):
        mask = labels == cid
        members_idx = np.where(mask)[0]
        centroid = X[mask].mean(axis=0)
        dists = np.linalg.norm(X[mask] - centroid, axis=1)

        members = []
        for i, idx in enumerate(members_idx):
            members.append({
                "hex_val": hex_info[idx]["hex_val"],
                "kw_number": hex_info[idx]["kw_number"],
                "name": hex_info[idx]["name"],
                "text": hex_info[idx]["text"],
                "dist_to_centroid": float(dists[i]),
            })
        members.sort(key=lambda m: m["dist_to_centroid"])

        clusters.append({
            "id": int(cid),
            "size": int(mask.sum()),
            "nearest_3": [m["name"] for m in members[:3]],
            "farthest_3": [m["name"] for m in members[-3:]],
            "members": members,
        })
    return clusters


def main():
    X, hex_info, atlas = load_data()
    # Sort hex_info by kw_number to align with embedding order
    # Embeddings are ordered by kw_number (1-64), index = kw_number - 1
    print(f"Guaci embeddings: {X.shape}")

    # K-means sweep
    sil_scores, optimal_k = kmeans_sweep(X)
    print(f"\nSilhouette scores: {sil_scores}")
    print(f"Optimal k: {optimal_k}")

    # Assignments by method
    km = KMeans(n_clusters=optimal_k, n_init=20, random_state=42)
    km_labels = km.fit_predict(X)
    ward_labels = hierarchical_clustering(X, optimal_k, "ward")
    complete_labels = hierarchical_clustering(X, optimal_k, "complete")
    average_labels = hierarchical_clustering(X, optimal_k, "average")
    dbscan_labels, dbscan_eps = dbscan_clustering(X)

    assignments = {
        "kmeans": km_labels.tolist(),
        "ward": ward_labels.tolist(),
        "complete": complete_labels.tolist(),
        "average": average_labels.tolist(),
        "dbscan": dbscan_labels.tolist(),
    }

    # Stability: ARI between all pairs
    methods = ["kmeans", "ward", "complete", "average"]
    stability = {}
    for i, m1 in enumerate(methods):
        for m2 in methods[i+1:]:
            a = np.array(assignments[m1])
            b = np.array(assignments[m2])
            ari = adjusted_rand_score(a, b)
            stability[f"{m1}_vs_{m2}"] = float(ari)
    print(f"\nStability (ARI): {stability}")

    # Cluster details at optimal k (using kmeans)
    clusters = build_cluster_details(X, km_labels, hex_info, optimal_k)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Cluster summary (k={optimal_k}, kmeans):")
    for cl in clusters:
        print(f"\n  Cluster {cl['id']} ({cl['size']} members):")
        print(f"    Nearest to centroid: {cl['nearest_3']}")
        print(f"    Farthest from centroid: {cl['farthest_3']}")
        member_names = [m["name"] for m in cl["members"]]
        print(f"    All: {', '.join(member_names)}")

    # DBSCAN info
    n_dbscan_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
    n_noise = (dbscan_labels == -1).sum()
    print(f"\nDBSCAN: eps={dbscan_eps:.4f}, {n_dbscan_clusters} clusters, {n_noise} noise points")

    output = {
        "silhouette_scores": {str(k): v for k, v in sil_scores.items()},
        "optimal_k": optimal_k,
        "assignments": assignments,
        "stability": stability,
        "clusters": clusters,
        "dbscan_info": {"eps": dbscan_eps, "n_clusters": n_dbscan_clusters, "n_noise": int(n_noise)},
    }

    with open(DATA / "guaci_clusters.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'guaci_clusters.json'}")


if __name__ == "__main__":
    main()
