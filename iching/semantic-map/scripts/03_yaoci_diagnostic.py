"""S3: 爻辭 Diagnostic — are yaoci embedding clusters dominated by formulaic markers?"""

import json
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"
ATLAS = ROOT.parent / "atlas" / "atlas.json"

VALENCE_MARKERS = ["吉", "凶", "无咎", "悔", "吝", "厲"]


def extract_markers(text: str) -> dict:
    """Extract binary presence of each valence marker."""
    remaining = text
    found = {}
    # 无咎 before 咎 (longest first)
    for marker in VALENCE_MARKERS:
        if marker in remaining:
            found[marker] = 1
            remaining = remaining.replace(marker, "□" * len(marker))
        else:
            found[marker] = 0
    return found


def load_data():
    emb = np.load(ROOT.parent / "synthesis" / "embeddings.npz")
    yaoci = emb["yaoci"]  # (384, 1024)

    with open(TEXTS / "yaoci.json") as f:
        texts = json.load(f)["entries"]

    with open(ATLAS) as f:
        atlas = json.load(f)
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    line_texts = []
    for entry in texts:
        hv = kw_to_hexval[entry["number"]]
        for j, line in enumerate(entry["lines"]):
            line_texts.append({
                "hex_val": hv,
                "kw_number": entry["number"],
                "name": entry["name"],
                "line": j,
                "text": line["text"],
            })

    # Build marker feature matrix
    marker_matrix = np.zeros((len(line_texts), len(VALENCE_MARKERS)), dtype=int)
    for i, lt in enumerate(line_texts):
        markers = extract_markers(lt["text"])
        for j, m in enumerate(VALENCE_MARKERS):
            marker_matrix[i, j] = markers[m]

    return yaoci, line_texts, marker_matrix


def cluster_marker_fractions(labels, marker_matrix, k):
    """For each cluster, compute fraction containing each marker."""
    clusters = []
    for cid in range(k):
        mask = labels == cid
        size = int(mask.sum())
        fracs = {}
        for j, marker in enumerate(VALENCE_MARKERS):
            fracs[marker] = float(marker_matrix[mask, j].sum() / size) if size > 0 else 0.0
        clusters.append({"id": int(cid), "size": size, "marker_fractions": fracs})
    return clusters


def chi2_tests(labels, marker_matrix, k):
    """χ² test: marker presence × cluster assignment."""
    results = {}
    for j, marker in enumerate(VALENCE_MARKERS):
        # Contingency table: cluster × marker_present
        table = np.zeros((k, 2), dtype=int)
        for cid in range(k):
            mask = labels == cid
            table[cid, 1] = marker_matrix[mask, j].sum()
            table[cid, 0] = mask.sum() - table[cid, 1]
        # Remove rows with all zeros
        if table.sum() == 0 or table[:, 1].sum() == 0:
            continue
        chi2, p, dof, expected = stats.chi2_contingency(table)
        results[marker] = {"chi2": float(chi2), "p_value": float(p), "dof": int(dof)}
    return results


def prediction_accuracy(labels, marker_matrix):
    """How well can marker features predict cluster assignment?"""
    if len(np.unique(labels)) < 2:
        return 0.0
    # Check if marker_matrix has any variance
    if marker_matrix.sum() == 0:
        return 0.0
    from sklearn.ensemble import RandomForestClassifier
    try:
        # RF handles sparse binary features better than LR here
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(marker_matrix, labels)
        rf_acc = float(rf.score(marker_matrix, labels))
        # Also compute majority-class baseline for context
        from collections import Counter
        baseline = max(Counter(labels).values()) / len(labels)
        # Return the lift above baseline, but report raw accuracy
        return rf_acc
    except Exception:
        return 0.0


def main():
    yaoci, line_texts, marker_matrix = load_data()
    print(f"Yaoci embeddings: {yaoci.shape}")
    print(f"Marker frequency: {dict(zip(VALENCE_MARKERS, marker_matrix.sum(axis=0).tolist()))}")

    K_VALUES = [3, 5, 8]
    all_clusters = {}
    all_chi2 = {}
    all_accuracy = {}

    for k in K_VALUES:
        km = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels = km.fit_predict(yaoci)
        sil = silhouette_score(yaoci, labels)

        clusters = cluster_marker_fractions(labels, marker_matrix, k)
        chi2 = chi2_tests(labels, marker_matrix, k)
        acc = prediction_accuracy(labels, marker_matrix)

        all_clusters[k] = clusters
        all_chi2[k] = chi2
        all_accuracy[k] = acc

        print(f"\n{'='*50}")
        print(f"k={k} (silhouette={sil:.3f}, marker prediction accuracy={acc:.3f}):")
        for cl in clusters:
            marker_str = ", ".join(
                f"{m}:{cl['marker_fractions'][m]:.0%}"
                for m in VALENCE_MARKERS if cl["marker_fractions"][m] > 0.05
            )
            print(f"  Cluster {cl['id']} (n={cl['size']}): {marker_str or 'no dominant markers'}")

        print(f"  χ² tests (p < 0.05):")
        for marker, res in chi2.items():
            if res["p_value"] < 0.05:
                print(f"    {marker}: χ²={res['chi2']:.1f} p={res['p_value']:.6f}")

    # Decision
    best_k = max(all_accuracy, key=all_accuracy.get)
    best_acc = all_accuracy[best_k]

    # Check if any k has χ² significant for most markers
    any_significant = False
    for k in K_VALUES:
        sig_count = sum(1 for m, r in all_chi2[k].items() if r["p_value"] < 0.001)
        if sig_count >= len(VALENCE_MARKERS) // 2:
            any_significant = True

    formulaic_dominated = any_significant and best_acc > 0.60

    print(f"\n{'='*60}")
    print(f"DIAGNOSTIC DECISION:")
    print(f"  Best prediction accuracy: {best_acc:.3f} (k={best_k})")
    print(f"  Strong χ² significance: {any_significant}")
    print(f"  formulaic_dominated = {formulaic_dominated}")

    output = {
        "clusters": {str(k): v for k, v in all_clusters.items()},
        "chi2_tests": {str(k): v for k, v in all_chi2.items()},
        "prediction_accuracy": {str(k): v for k, v in all_accuracy.items()},
        "formulaic_dominated": formulaic_dominated,
        "valence_separation_strength": best_acc,
    }

    with open(DATA / "yaoci_diagnostic.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'yaoci_diagnostic.json'}")


if __name__ == "__main__":
    main()
