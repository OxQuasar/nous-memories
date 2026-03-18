#!/usr/bin/env python3
"""
Cross-Layer Opposition Geometry + Guaci Length Asymmetry
=========================================================
Thread 1: Compare complement opposition structure across yaoci/guaci/tuan/daxiang.
Thread 2: Investigate guaci text-length asymmetry in complement pairs.
"""

import json
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy.stats import spearmanr, binomtest
from scipy.linalg import orthogonal_procrustes
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
SYNTH_PATH = ROOT / "synthesis" / "embeddings.npz"
TEXTS = ROOT.parent / "texts" / "iching"

N_HEX = 64
N_PERM = 10_000
LAYERS = ['yaoci', 'guaci', 'tuan', 'daxiang']
PCA_K = 20

# Sheng ↔ Wu Wang
H_SHENG = 6
H_WUWANG = 57


# ── Data ─────────────────────────────────────────────────────

def load_data():
    atlas = json.load(open(ATLAS_PATH))
    emb = np.load(SYNTH_PATH)

    # Build centroids per layer
    centroids = {}
    for layer in LAYERS:
        raw = emb[layer]
        if layer == 'yaoci':
            centroids[layer] = np.array([raw[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
        else:
            centroids[layer] = raw  # already (64, 1024)

    # Complement pairs (h_lo < h_hi)
    pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)
    assert len(pairs) == 32

    return atlas, centroids, pairs


def complement_cosines(centroids, pairs):
    """Return array of 32 cosine similarities for complement pairs."""
    cos = np.zeros(len(pairs))
    for i, (h1, h2) in enumerate(pairs):
        a, b = centroids[h1], centroids[h2]
        cos[i] = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos


def difference_vectors(centroids, pairs):
    """Return (32, d) matrix of centroid[h1] - centroid[h2]."""
    return np.array([centroids[h1] - centroids[h2] for h1, h2 in pairs])


def participation_ratio(eigenvalues):
    """PR = (Σλ)² / Σ(λ²). Effective dimensionality."""
    ev = np.maximum(eigenvalues, 0)
    s = ev.sum()
    if s < 1e-12:
        return 0.0
    return s**2 / (ev**2).sum()


def upper_triangle(mat):
    """Extract upper triangle (excluding diagonal) as flat array."""
    n = mat.shape[0]
    idx = np.triu_indices(n, k=1)
    return mat[idx]


def mantel_test(mat1, mat2, n_perm=N_PERM):
    """Mantel test: Spearman correlation of upper triangles, permutation p-value."""
    ut1 = upper_triangle(mat1)
    ut2 = upper_triangle(mat2)
    rho_actual, _ = spearmanr(ut1, ut2)

    n = mat1.shape[0]
    rng = np.random.default_rng(42)
    n_ge = 0
    for _ in range(n_perm):
        perm = rng.permutation(n)
        mat2_perm = mat2[np.ix_(perm, perm)]
        ut2_perm = upper_triangle(mat2_perm)
        rho_perm, _ = spearmanr(ut1, ut2_perm)
        if rho_perm >= rho_actual:
            n_ge += 1

    p_val = (n_ge + 1) / (n_perm + 1)
    return rho_actual, p_val


def procrustes_r2(scores1, scores2):
    """Orthogonal Procrustes R² between two score matrices.
    Center and scale-normalize before alignment.
    """
    # Center
    s1 = scores1 - scores1.mean(axis=0)
    s2 = scores2 - scores2.mean(axis=0)

    # Scale-normalize by Frobenius norm
    s1 /= np.linalg.norm(s1, 'fro')
    s2 /= np.linalg.norm(s2, 'fro')

    # Orthogonal Procrustes: find R minimizing ||s1 - s2 @ R||
    R, _ = orthogonal_procrustes(s2, s1)  # s2 @ R ≈ s1
    s2_aligned = s2 @ R

    ss_res = np.sum((s1 - s2_aligned)**2)
    ss_tot = np.sum(s1**2)
    return 1.0 - ss_res / ss_tot


# ══════════════════════════════════════════════════════════════
# THREAD 1: Cross-Layer Opposition Geometry
# ══════════════════════════════════════════════════════════════

def thread1(atlas, centroids, pairs):
    print("=" * 80)
    print("THREAD 1: CROSS-LAYER OPPOSITION GEOMETRY")
    print("=" * 80)
    print()

    # ── Step 1: Per-layer metrics ──
    print("--- Step 1: Per-layer metrics ---")
    print()

    # Find 升↔无妄 pair index
    sw_idx = None
    for i, (h1, h2) in enumerate(pairs):
        if {h1, h2} == {H_SHENG, H_WUWANG}:
            sw_idx = i
            break

    layer_cos = {}    # layer → 32 cosines
    layer_diffs = {}  # layer → (32, 1024) difference vectors
    layer_pca = {}    # layer → PCA object

    hdr = f"{'Layer':10s} | {'mean cos':>8s} {'std':>6s} {'#neg':>5s} | {'PR':>5s} | {'升↔无妄 cos':>12s} {'rank':>5s}"
    print(hdr)
    print("-" * len(hdr))

    for layer in LAYERS:
        C = centroids[layer]
        cos = complement_cosines(C, pairs)
        diffs = difference_vectors(C, pairs)

        layer_cos[layer] = cos
        layer_diffs[layer] = diffs

        # PCA on difference vectors
        pca = PCA(n_components=min(31, diffs.shape[0] - 1))
        pca.fit(diffs)
        layer_pca[layer] = pca

        pr = participation_ratio(pca.explained_variance_)
        n_neg = (cos < 0).sum()

        # 升↔无妄
        sw_cos = cos[sw_idx]
        # Rank: 1 = most negative (lowest cosine)
        rank = np.argsort(cos).tolist().index(sw_idx) + 1

        print(f"{layer:10s} | {cos.mean():8.4f} {cos.std():6.4f} {n_neg:5d} | {pr:5.1f} | {sw_cos:12.4f} {rank:5d}/32")

    print()

    # PCA variance explained (top 10 components per layer)
    print("  PCA variance explained (% cumulative, top 10 components):")
    print(f"  {'k':>3s}", end="")
    for layer in LAYERS:
        print(f" | {layer:>8s}", end="")
    print()

    for k in range(10):
        print(f"  {k+1:3d}", end="")
        for layer in LAYERS:
            cum = layer_pca[layer].explained_variance_ratio_[:k+1].sum() * 100
            print(f" | {cum:7.1f}%", end="")
        print()
    print()

    # ── Step 2: Cross-layer comparisons ──
    print("--- Step 2: Cross-layer pairwise comparisons ---")
    print()

    layer_pairs = list(combinations(LAYERS, 2))

    # Pre-compute needed matrices
    centroid_dists = {}  # layer → 64×64 cosine distance matrix
    diff_cos = {}        # layer → 32×32 cosine similarity matrix of diff vectors
    pca_scores = {}      # layer → 32×PCA_K scores

    for layer in LAYERS:
        centroid_dists[layer] = cosine_distances(centroids[layer])
        diff_cos[layer] = cosine_similarity(layer_diffs[layer])
        scores = layer_pca[layer].transform(layer_diffs[layer])
        pca_scores[layer] = scores[:, :PCA_K]

    # Run all comparisons
    print(f"{'Pair':18s} | {'ρ_centroid':>10s} {'p':>8s} | {'ρ_diff':>8s} {'p':>8s} | {'Procrustes':>10s} | {'profile ρ':>10s} {'p':>8s}")
    print("-" * 100)

    for L1, L2 in layer_pairs:
        # A. Mantel on centroid distances
        rho_c, p_c = mantel_test(centroid_dists[L1], centroid_dists[L2])

        # B. Mantel on difference-vector cosine similarity
        rho_d, p_d = mantel_test(diff_cos[L1], diff_cos[L2])

        # C. Procrustes R²
        pr2 = procrustes_r2(pca_scores[L1], pca_scores[L2])

        # D. Pair-profile ρ
        rho_p, p_p = spearmanr(layer_cos[L1], layer_cos[L2])

        print(f"{L1+'-'+L2:18s} | {rho_c:+10.4f} {p_c:8.4f} | {rho_d:+8.4f} {p_d:8.4f} | {pr2:10.4f} | {rho_p:+10.4f} {p_p:8.4f}")

    print()

    # ── Interpretation guide ──
    print("  INTERPRETATION GUIDE:")
    print("  ρ_centroid:  Do layers agree on which hexagrams are semantically similar?")
    print("  ρ_diff:      Do layers agree on which pairs oppose similarly?")
    print("  Procrustes:  Can one layer's opposition subspace be rotated to match another?")
    print("  profile ρ:   Do layers agree on which pairs oppose most/least strongly?")
    print()

    return layer_cos, layer_diffs


# ══════════════════════════════════════════════════════════════
# THREAD 2: Guaci Length Asymmetry
# ══════════════════════════════════════════════════════════════

def thread2(atlas, pairs):
    print("=" * 80)
    print("THREAD 2: GUACI LENGTH ASYMMETRY")
    print("=" * 80)
    print()

    guaci_data = json.load(open(TEXTS / "guaci.json"))['entries']
    guaci_by_kw = {e['number']: e['text'] for e in guaci_data}

    hex_to_kw = {int(k): v['kw_number'] for k, v in atlas.items() if k.isdigit()}

    # Per-hexagram: guaci text, length, valence
    lengths = {}
    valence = {}
    guaci_text = {}
    POS_TOKENS = ['吉', '元吉', '大吉', '無咎']
    NEG_TOKENS = ['凶', '厲', '悔', '吝']

    for h in range(N_HEX):
        kw = hex_to_kw[h]
        text = guaci_by_kw[kw]
        guaci_text[h] = text
        lengths[h] = len(text)

        pos = sum(text.count(t) for t in POS_TOKENS)
        neg = sum(text.count(t) for t in NEG_TOKENS)
        valence[h] = pos - neg

    # ── KW ordering test ──
    print("  KW ORDERING TEST:")
    print("  In what fraction of pairs is the lower-KW-number member longer?")
    print()

    lower_kw_longer = 0
    ties = 0
    for h1, h2 in pairs:
        kw1, kw2 = hex_to_kw[h1], hex_to_kw[h2]
        lo = h1 if kw1 < kw2 else h2
        hi = h2 if kw1 < kw2 else h1
        if lengths[lo] > lengths[hi]:
            lower_kw_longer += 1
        elif lengths[lo] == lengths[hi]:
            ties += 1

    n_non_tie = 32 - ties
    frac = lower_kw_longer / n_non_tie if n_non_tie > 0 else 0.5
    # Binomial test (two-sided) against 50%
    binom_result = binomtest(lower_kw_longer, n_non_tie, 0.5, alternative='two-sided')

    print(f"  Lower-KW longer: {lower_kw_longer}/{n_non_tie} non-tied pairs ({frac:.1%})")
    print(f"  Ties: {ties}")
    print(f"  Binomial test p = {binom_result.pvalue:.4f}")
    if binom_result.pvalue < 0.05:
        print(f"  ◄ SIGNIFICANT: KW ordering predicts text length")
    else:
        print(f"  Not significant — no KW ordering effect")
    print()

    # ── Valence correlation ──
    print("  VALENCE CORRELATION:")
    print()

    len_arr = np.array([lengths[h] for h in range(N_HEX)])
    val_arr = np.array([valence[h] for h in range(N_HEX)])

    rho_lv, p_lv = spearmanr(len_arr, val_arr)
    print(f"  ρ(guaci_length, valence) across 64 hexagrams: {rho_lv:+.4f} (p={p_lv:.4f})")

    # Pair-level: length diff vs valence diff
    len_diffs = np.array([lengths[h1] - lengths[h2] for h1, h2 in pairs])
    val_diffs = np.array([valence[h1] - valence[h2] for h1, h2 in pairs])

    rho_pair, p_pair = spearmanr(len_diffs, val_diffs)
    print(f"  ρ(Δlength, Δvalence) across 32 pairs: {rho_pair:+.4f} (p={p_pair:.4f})")

    if abs(rho_lv) > 0.3 and p_lv < 0.05:
        print(f"  ◄ Length and valence are correlated — longer guaci texts tend to be "
              f"{'more auspicious' if rho_lv > 0 else 'less auspicious'}")
    print()

    # ── Most asymmetric pairs ──
    print("  5 MOST ASYMMETRIC COMPLEMENT PAIRS (by |Δlength|):")
    print()
    pair_asym = [(h1, h2, abs(lengths[h1] - lengths[h2])) for h1, h2 in pairs]
    pair_asym.sort(key=lambda x: -x[2])

    print(f"  {'Hex1':10s} {'KW#':>4s} {'len':>4s} {'val':>4s} | {'Hex2':10s} {'KW#':>4s} {'len':>4s} {'val':>4s} | {'|Δlen|':>6s} {'Δval':>5s}")
    print("  " + "-" * 75)
    for h1, h2, delta in pair_asym[:5]:
        n1 = atlas[str(h1)]['kw_name']
        n2 = atlas[str(h2)]['kw_name']
        kw1, kw2 = hex_to_kw[h1], hex_to_kw[h2]
        print(f"  {n1:10s} {kw1:4d} {lengths[h1]:4d} {valence[h1]:+4d} | "
              f"{n2:10s} {kw2:4d} {lengths[h2]:4d} {valence[h2]:+4d} | "
              f"{delta:6d} {valence[h1]-valence[h2]:+5d}")
    print()

    # ── 升↔无妄 specifically ──
    print("  升↔无妄 DETAIL:")
    for h, label in [(H_SHENG, "升 (Sheng)"), (H_WUWANG, "无妄 (Wu Wang)")]:
        kw = hex_to_kw[h]
        print(f"    {label}: KW #{kw}, len={lengths[h]}, valence={valence[h]}")
        print(f"      Text: {guaci_text[h]}")
    print()

    # ── Distribution of valence scores ──
    print("  VALENCE DISTRIBUTION:")
    from collections import Counter
    vc = Counter(val_arr)
    for v in sorted(vc):
        print(f"    valence={v:+2d}: {vc[v]:3d} hexagrams")
    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    atlas, centroids, pairs = load_data()

    layer_cos, layer_diffs = thread1(atlas, centroids, pairs)

    thread2(atlas, pairs)

    # ── Final summary ──
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("  Thread 1 answers: How similar is complement opposition across text layers?")
    print("  Thread 2 answers: Why are guaci complement pairs length-asymmetric?")


if __name__ == "__main__":
    main()
