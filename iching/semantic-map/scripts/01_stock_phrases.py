"""S1: Stock Phrase Extraction — valence marker analysis across 384 line texts."""

import json
import numpy as np
from collections import Counter
from pathlib import Path
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"

# Ordered longest-first to handle overlap (无咎 before 咎, 悔亡 before 悔, etc.)
MARKERS = [
    "元亨利貞", "利涉大川", "元亨", "利貞", "无咎", "悔亡",
    "吉", "凶", "悔", "吝", "咎", "厲", "亨", "利", "貞",
]


def extract_markers(text: str) -> list[str]:
    """Extract markers from text, longest-first to avoid double-counting."""
    found = []
    remaining = text
    for marker in MARKERS:
        if marker in remaining:
            found.append(marker)
            # Remove all occurrences to prevent sub-markers from matching
            remaining = remaining.replace(marker, "□" * len(marker))
    return found


def load_lines():
    """Load 384 line texts indexed by (hex_val, line_pos)."""
    with open(TEXTS / "yaoci.json") as f:
        data = json.load(f)

    # Build hex_number -> hex_val mapping from atlas
    atlas_path = ROOT.parent / "atlas" / "atlas.json"
    with open(atlas_path) as f:
        atlas = json.load(f)
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    lines = []
    for entry in data["entries"]:
        hex_val = kw_to_hexval[entry["number"]]
        for j, line in enumerate(entry["lines"]):
            lines.append({
                "hex_val": hex_val,
                "kw_number": entry["number"],
                "name": entry["name"],
                "line": j,
                "label": line["label"],
                "text": line["text"],
            })
    return lines


def build_presence_matrix(lines):
    """384 x N binary presence matrix."""
    matrix = np.zeros((len(lines), len(MARKERS)), dtype=int)
    line_markers = []
    for i, line in enumerate(lines):
        found = extract_markers(line["text"])
        line_markers.append(found)
        for marker in found:
            matrix[i, MARKERS.index(marker)] = 1
    return matrix, line_markers


def co_occurrence_and_pmi(matrix):
    """NxN co-occurrence with PMI."""
    n_lines = matrix.shape[0]
    N = matrix.shape[1]
    co_occ = matrix.T @ matrix  # NxN
    marginals = matrix.sum(axis=0)  # N

    pmi = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if co_occ[i, j] > 0 and marginals[i] > 0 and marginals[j] > 0:
                p_ij = co_occ[i, j] / n_lines
                p_i = marginals[i] / n_lines
                p_j = marginals[j] / n_lines
                pmi[i, j] = np.log2(p_ij / (p_i * p_j))
    return co_occ.tolist(), pmi.tolist()


def pca_analysis(matrix):
    """PCA on binary presence matrix."""
    # Remove zero-variance columns
    nonzero = matrix.sum(axis=0) > 0
    X = matrix[:, nonzero].astype(float)
    if X.shape[1] < 2:
        return {"n_components_90pct": 1, "explained_variance_ratio": [1.0], "loadings": []}

    pca = PCA()
    pca.fit(X)
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    n90 = int(np.searchsorted(cumvar, 0.9)) + 1

    # Loadings: which markers load on first few components
    active_markers = [MARKERS[i] for i in range(len(MARKERS)) if nonzero[i]]
    loadings = {}
    for c in range(min(n90, 5)):
        top_idx = np.argsort(np.abs(pca.components_[c]))[::-1][:5]
        loadings[f"PC{c+1}"] = [
            {"marker": active_markers[int(idx)], "loading": float(pca.components_[c][idx])}
            for idx in top_idx
        ]

    return {
        "n_components_90pct": n90,
        "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "loadings": loadings,
    }


def positional_bias(matrix, lines):
    """χ² test for each marker across line positions 0-5."""
    results = {}
    positions = np.array([l["line"] for l in lines])

    for j, marker in enumerate(MARKERS):
        counts = np.zeros(6)
        for pos in range(6):
            counts[pos] = matrix[positions == pos, j].sum()
        total = counts.sum()
        if total < 5:  # too few for χ²
            continue
        expected = np.full(6, total / 6)
        chi2, p = stats.chisquare(counts, expected)
        results[marker] = {
            "counts_by_position": counts.tolist(),
            "total": int(total),
            "chi2": float(chi2),
            "p_value": float(p),
        }
    return results


def marker_families(pmi_matrix):
    """Cluster markers by PMI-based distance."""
    pmi = np.array(pmi_matrix)
    # Only cluster markers that actually appear
    active = [i for i in range(len(MARKERS)) if pmi[i, i] != 0 or pmi[i].any()]
    if len(active) < 3:
        return {"clusters": [], "note": "too few active markers"}

    sub = pmi[np.ix_(active, active)]
    # Convert PMI to distance: max_pmi - pmi (higher PMI = closer)
    mx = sub.max()
    dist = mx - sub
    np.fill_diagonal(dist, 0)
    # Make symmetric
    dist = (dist + dist.T) / 2

    from sklearn.cluster import AgglomerativeClustering
    for k in [2, 3, 4]:
        clust = AgglomerativeClustering(n_clusters=k, metric="precomputed", linkage="average")
        labels = clust.fit_predict(dist)
        families = {}
        for idx, lab in zip(active, labels):
            families.setdefault(int(lab), []).append(MARKERS[idx])
        if k == 3:  # use k=3 as default
            result_k3 = families

    # Also try k=2 for binary split
    clust2 = AgglomerativeClustering(n_clusters=2, metric="precomputed", linkage="average")
    labels2 = clust2.fit_predict(dist)
    families2 = {}
    for idx, lab in zip(active, labels2):
        families2.setdefault(int(lab), []).append(MARKERS[idx])

    return {"k2": families2, "k3": result_k3}


def main():
    lines = load_lines()
    print(f"Loaded {len(lines)} line texts")

    matrix, line_markers = build_presence_matrix(lines)
    print(f"Marker presence matrix: {matrix.shape}")
    print(f"Marker frequencies: {dict(zip(MARKERS, matrix.sum(axis=0).tolist()))}")

    co_occ, pmi = co_occurrence_and_pmi(matrix)
    print("\nCo-occurrence computed")

    pca = pca_analysis(matrix)
    print(f"\nPCA: {pca['n_components_90pct']} components for 90% variance")
    for pc, loads in pca["loadings"].items():
        top = ", ".join(f"{l['marker']}({l['loading']:.2f})" for l in loads[:3])
        print(f"  {pc}: {top}")

    pos_bias = positional_bias(matrix, lines)
    print(f"\nPositional bias (p < 0.05):")
    for marker, info in pos_bias.items():
        if info["p_value"] < 0.05:
            print(f"  {marker}: χ²={info['chi2']:.1f} p={info['p_value']:.4f} counts={info['counts_by_position']}")

    families = marker_families(pmi)
    print(f"\nMarker families (k=2): {families.get('k2', {})}")
    print(f"Marker families (k=3): {families.get('k3', {})}")

    # Build output
    marker_list = []
    for i, line in enumerate(lines):
        marker_list.append({
            "hex_val": line["hex_val"],
            "kw_number": line["kw_number"],
            "name": line["name"],
            "line": line["line"],
            "label": line["label"],
            "text": line["text"],
            "markers": line_markers[i],
        })

    output = {
        "marker_matrix": marker_list,
        "markers": MARKERS,
        "co_occurrence": co_occ,
        "pmi": pmi,
        "pca": pca,
        "positional_bias": pos_bias,
        "marker_families": families,
    }

    with open(DATA / "stock_phrases.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'stock_phrases.json'}")


if __name__ == "__main__":
    main()
