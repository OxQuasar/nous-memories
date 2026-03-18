#!/usr/bin/env python3
"""edge_type_decomposition.py — Test whether 克-type transitions drive the d=1
thematic anti-correlation (R159) more than 生 or 比和 transitions.

Cross-validated across BGE-M3, E5-large, and LaBSE.
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict

from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from scipy.spatial.distance import cosine

# ════════════════════════════════════════════════════════════
# Paths
# ════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent  # memories/iching
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
CROSS_EMB_DIR = ROOT / "reversal" / "Q1"

MODELS = ['bge-m3', 'e5-large', 'labse']

ELEM_TO_Z5 = {'Wood': 0, 'Fire': 1, 'Earth': 2, 'Metal': 3, 'Water': 4}
REL_LABELS = {0: '比和', 1: '生', 2: '克'}

N_PERM = 10_000
RNG = np.random.default_rng(42)


# ════════════════════════════════════════════════════════════
# Data Loading
# ════════════════════════════════════════════════════════════

def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)


def load_hex_centroids(model):
    """Load yaoci embeddings and aggregate to hex centroids (64, D)."""
    path = CROSS_EMB_DIR / f"embeddings_{model}.npz"
    yaoci = np.load(path)['yaoci']  # (384, D)
    return yaoci.reshape(64, 6, -1).mean(axis=1)  # (64, D)


def build_hex_design_matrix(atlas):
    """Build design matrix at hex level (64 rows).
    Categorical: basin, surface_relation, palace, palace_element, rank
    Numeric: depth, i_component, inner_val, hu_depth, shi, ying
    (No line_pos — we're at hex level.)
    """
    meta = []
    for i in range(64):
        h = atlas[str(i)]
        meta.append({
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

    cat_keys = ['basin', 'surface_relation', 'palace', 'palace_element', 'rank']
    num_keys = ['depth', 'i_component', 'inner_val', 'hu_depth', 'shi', 'ying']

    cat_arrays = []
    for key in cat_keys:
        enc = OneHotEncoder(sparse_output=False, drop='first')
        arr = enc.fit_transform(np.array([m[key] for m in meta]).reshape(-1, 1))
        cat_arrays.append(arr)

    num_arrays = [np.array([m[k] for m in meta], dtype=float).reshape(-1, 1)
                  for k in num_keys]

    return np.hstack(cat_arrays + num_arrays)


def extract_hex_residuals(centroids, X):
    """Regress out algebraic coords from hex centroids. Returns residuals and R²."""
    reg = LinearRegression()
    reg.fit(X, centroids)
    predicted = reg.predict(X)
    residuals = centroids - predicted
    total_var = np.var(centroids, axis=0).sum()
    resid_var = np.var(residuals, axis=0).sum()
    r2 = 1 - resid_var / total_var
    return residuals, r2


# ════════════════════════════════════════════════════════════
# Pair Classification
# ════════════════════════════════════════════════════════════

def get_d1_pairs(atlas):
    """All 192 hexagram pairs differing at exactly 1 bit.
    Returns list of (h1, h2, line_pos, relation).
    line_pos: 1-6 (1-indexed).
    relation: 0=比和, 1=生, 2=克.
    """
    pairs = []
    for h1 in range(64):
        for bit in range(6):
            h2 = h1 ^ (1 << bit)
            if h2 <= h1:
                continue  # avoid double-counting
            line_pos = bit + 1  # 1-indexed

            # Which trigram changed?
            if bit < 3:
                e1_name = atlas[str(h1)]['lower_trigram']['element']
                e2_name = atlas[str(h2)]['lower_trigram']['element']
            else:
                e1_name = atlas[str(h1)]['upper_trigram']['element']
                e2_name = atlas[str(h2)]['upper_trigram']['element']

            z1, z2 = ELEM_TO_Z5[e1_name], ELEM_TO_Z5[e2_name]
            d = min((z2 - z1) % 5, (z1 - z2) % 5)
            # d: 0=比和, 1=生, 2=克
            pairs.append((h1, h2, line_pos, d))

    return pairs


def pairwise_cosine_dist(vecs):
    """Full pairwise cosine distance matrix (n, n)."""
    # Normalize
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    normed = vecs / norms
    sim = normed @ normed.T
    return 1 - sim


# ════════════════════════════════════════════════════════════
# Computations
# ════════════════════════════════════════════════════════════

def run_all():
    atlas = load_atlas()
    pairs = get_d1_pairs(atlas)
    X_hex = build_hex_design_matrix(atlas)

    # Verify pair counts
    rel_counts = defaultdict(int)
    line_counts = defaultdict(int)
    for _, _, lp, rel in pairs:
        rel_counts[rel] += 1
        line_counts[lp] += 1
    print(f"Total d=1 pairs: {len(pairs)}")
    print(f"  Per relation: 比和={rel_counts[0]}, 生={rel_counts[1]}, 克={rel_counts[2]}")
    print(f"  Per line: {dict(sorted(line_counts.items()))}")

    # Verify line-relation structure
    line_rel = defaultdict(lambda: defaultdict(int))
    for _, _, lp, rel in pairs:
        line_rel[lp][rel] += 1
    print(f"\n  Line × Relation breakdown:")
    for lp in sorted(line_rel.keys()):
        parts = ", ".join(f"{REL_LABELS[r]}={line_rel[lp][r]}" for r in sorted(line_rel[lp].keys()))
        print(f"    Line {lp}: {parts}")

    all_results = {}

    for model in MODELS:
        print(f"\n{'='*72}")
        print(f"MODEL: {model}")
        print(f"{'='*72}")

        centroids = load_hex_centroids(model)
        residuals, r2 = extract_hex_residuals(centroids, X_hex)
        print(f"  Hex centroids: {centroids.shape}, R² = {r2:.4f}")

        # Cosine distance matrix on residuals
        dist_mat = pairwise_cosine_dist(residuals)

        # Collect distances for all d=1 pairs
        pair_dists = [(h1, h2, lp, rel, dist_mat[h1, h2]) for h1, h2, lp, rel in pairs]

        # ── PASS 1: Line-position decomposition ──
        print(f"\n  PASS 1: LINE-POSITION DECOMPOSITION")
        print(f"  {'─'*50}")
        overall_mean = np.mean([d for _, _, _, _, d in pair_dists])
        print(f"  Overall d=1 mean distance: {overall_mean:.6f} (n={len(pair_dists)})")

        line_means = {}
        for lp in range(1, 7):
            dists = [d for _, _, l, _, d in pair_dists if l == lp]
            m = np.mean(dists)
            line_means[lp] = m
            # Determine line type
            rels = set(rel for _, _, l, rel, _ in pair_dists if l == lp)
            rel_str = "+".join(REL_LABELS[r] for r in sorted(rels))
            print(f"    Line {lp}: {m:.6f} (n={len(dists)})  [{rel_str}]")

        # ── PASS 2: Controlled test (lines 1,4: 克 vs 生) ──
        print(f"\n  PASS 2: CONTROLLED TEST (lines 1,4: 克 vs 生)")
        print(f"  {'─'*50}")
        controlled = [(h1, h2, lp, rel, d) for h1, h2, lp, rel, d in pair_dists
                       if lp in (1, 4)]
        ke_dists = np.array([d for _, _, _, rel, d in controlled if rel == 2])
        sh_dists = np.array([d for _, _, _, rel, d in controlled if rel == 1])

        ke_mean = ke_dists.mean()
        sh_mean = sh_dists.mean()
        diff = ke_mean - sh_mean
        print(f"    克 mean: {ke_mean:.6f} (n={len(ke_dists)})")
        print(f"    生 mean: {sh_mean:.6f} (n={len(sh_dists)})")
        print(f"    Δ(克−生): {diff:+.6f}")

        # Permutation test
        all_controlled_dists = np.array([d for _, _, _, _, d in controlled])
        all_controlled_rels = np.array([rel for _, _, _, rel, _ in controlled])
        n_ke = (all_controlled_rels == 2).sum()
        n_sh = (all_controlled_rels == 1).sum()
        n_exceed = 0
        for _ in range(N_PERM):
            perm = RNG.permutation(len(all_controlled_dists))
            perm_ke = all_controlled_dists[perm[:n_ke]].mean()
            perm_sh = all_controlled_dists[perm[n_ke:n_ke + n_sh]].mean()
            if abs(perm_ke - perm_sh) >= abs(diff):
                n_exceed += 1
        p_val = (n_exceed + 1) / (N_PERM + 1)
        print(f"    Permutation p-value (two-sided): {p_val:.4f}")

        # ── PASS 3: Full 五行 decomposition (confounded) ──
        print(f"\n  PASS 3: FULL 五行 DECOMPOSITION (confounded with line position)")
        print(f"  {'─'*50}")
        for rel_code in (0, 1, 2):
            dists = [d for _, _, _, rel, d in pair_dists if rel == rel_code]
            m = np.mean(dists) if dists else float('nan')
            print(f"    {REL_LABELS[rel_code]} mean: {m:.6f} (n={len(dists)})")

        all_results[model] = {
            'r2': r2,
            'overall_mean': overall_mean,
            'line_means': line_means,
            'ke_mean': ke_mean,
            'sh_mean': sh_mean,
            'diff': diff,
            'p_val': p_val,
            'rel_means': {rel: np.mean([d for _, _, _, r, d in pair_dists if r == rel])
                          for rel in (0, 1, 2)},
        }

    # ── PASS 4: Cross-validation summary ──
    print(f"\n{'='*72}")
    print("SUMMARY")
    print(f"{'='*72}")

    print(f"\n  Pass 2 results across models (controlled: lines 1,4 only):")
    print(f"  {'Model':>10} {'Δ(克−生)':>12} {'p-value':>10} {'克 mean':>10} {'生 mean':>10}")
    print(f"  {'─'*55}")
    all_same_sign = True
    first_sign = None
    for model in MODELS:
        r = all_results[model]
        sign = '+' if r['diff'] > 0 else '-'
        if first_sign is None:
            first_sign = sign
        elif sign != first_sign:
            all_same_sign = False
        print(f"  {model:>10} {r['diff']:>+12.6f} {r['p_val']:>10.4f} "
              f"{r['ke_mean']:>10.6f} {r['sh_mean']:>10.6f}")

    any_sig = any(all_results[m]['p_val'] < 0.05 for m in MODELS)
    all_sig = all(all_results[m]['p_val'] < 0.05 for m in MODELS)

    print(f"\n  Cross-model consistent sign: {'YES' if all_same_sign else 'NO'}")
    print(f"  Any model significant (p<0.05): {'YES' if any_sig else 'NO'}")
    print(f"  All models significant: {'YES' if all_sig else 'NO'}")

    if all_sig and all_same_sign:
        verdict = "BRIDGE EXISTS — 克 transitions drive d=1 signal differentially"
    elif any_sig and all_same_sign:
        verdict = "SUGGESTIVE — consistent direction, partial significance"
    elif not any_sig:
        verdict = "BRIDGE DEAD — no detectable 五行-type differentiation in d=1 signal"
    else:
        verdict = "INCONCLUSIVE — inconsistent across models"
    print(f"  Verdict: {verdict}")

    # Full decomposition comparison
    print(f"\n  Pass 3 (confounded) across models:")
    print(f"  {'Model':>10} {'比和':>10} {'生':>10} {'克':>10}")
    print(f"  {'─'*45}")
    for model in MODELS:
        r = all_results[model]
        print(f"  {model:>10} {r['rel_means'][0]:>10.6f} "
              f"{r['rel_means'][1]:>10.6f} {r['rel_means'][2]:>10.6f}")

    # Line position comparison
    print(f"\n  Pass 1 (line position means) across models:")
    print(f"  {'Model':>10} " + " ".join(f"{'L'+str(i):>10}" for i in range(1, 7)))
    print(f"  {'─'*75}")
    for model in MODELS:
        r = all_results[model]
        vals = " ".join(f"{r['line_means'][i]:>10.6f}" for i in range(1, 7))
        print(f"  {model:>10} {vals}")

    return all_results


if __name__ == '__main__':
    run_all()
