#!/usr/bin/env python3
"""pair_concordance.py — Pair-level concordance test for SikuRoBERTa (R213 candidate).

Tests whether SikuRoBERTa agrees with prior models on WHICH specific complement
pairs oppose most strongly, and in WHICH directions.

Methodology follows phase8_trigram_decomposition.py exactly.
"""

import sys
import json
import numpy as np
from pathlib import Path
from itertools import combinations

from scipy.stats import spearmanr
from scipy.linalg import orthogonal_procrustes
from scipy.spatial.distance import cosine as cos_dist
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA

# ════════════════════════════════════════════════════════════
# Paths & Constants
# ════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent          # memories/iching
Q1_DIR = ROOT / "reversal" / "Q1"
ATLAS_PATH = ROOT / "atlas" / "atlas.json"

N_HEX = 64
N_PAIRS = 32
MODELS = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']
TIER1B_THRESHOLD = 0.78  # minimum ρ from prior 3-model set


# ════════════════════════════════════════════════════════════
# Data Loading (self-contained, matching phase1 pipeline)
# ════════════════════════════════════════════════════════════

def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)


def load_embeddings(model_name):
    return np.load(Q1_DIR / f"embeddings_{model_name}.npz")['yaoci']


def build_yaoci_meta(atlas):
    meta = []
    for i in range(384):
        hex_idx = i // 6
        line_pos = i % 6
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
    return meta


def build_design_matrix(meta):
    cat_features = {
        'line_pos': [m['line_pos'] for m in meta],
        'basin': [m['basin'] for m in meta],
        'surface_relation': [m['surface_relation'] for m in meta],
        'palace': [m['palace'] for m in meta],
        'palace_element': [m['palace_element'] for m in meta],
        'rank': [m['rank'] for m in meta],
    }
    cat_arrays = []
    for name, values in cat_features.items():
        enc = OneHotEncoder(sparse_output=False, drop='first')
        arr = enc.fit_transform(np.array(values).reshape(-1, 1))
        cat_arrays.append(arr)
    num_keys = ['depth', 'i_component', 'inner_val', 'hu_depth', 'shi', 'ying']
    num_arrays = [np.array([m[k] for m in meta], dtype=float).reshape(-1, 1)
                  for k in num_keys]
    return np.hstack(cat_arrays + num_arrays)


def extract_residuals(yaoci, X):
    reg = LinearRegression()
    reg.fit(X, yaoci)
    residual = yaoci - reg.predict(X)
    total_var = np.var(yaoci, axis=0).sum()
    resid_var = np.var(residual, axis=0).sum()
    r2 = 1 - resid_var / total_var
    return residual, r2


def get_complement_pairs(atlas):
    pairs = []
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        if h < c:
            pairs.append((h, c))
    assert len(pairs) == N_PAIRS
    return pairs


def compute_residual_centroids(yaoci, meta):
    X = build_design_matrix(meta)
    residual, r2 = extract_residuals(yaoci, X)
    centroids = np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    return centroids, r2


def compute_diff_vectors(centroids, pairs):
    return np.array([centroids[h] - centroids[c] for h, c in pairs])


# ════════════════════════════════════════════════════════════
# Step 1–2: Load All Models, Compute Diff Vectors
# ════════════════════════════════════════════════════════════

def load_all_models(atlas, meta, pairs):
    model_diffs = {}
    model_cosines = {}  # per-pair residual cosines
    model_centroids = {}

    for model in MODELS:
        yaoci = load_embeddings(model)
        centroids, r2 = compute_residual_centroids(yaoci, meta)
        dv = compute_diff_vectors(centroids, pairs)
        model_diffs[model] = dv
        model_centroids[model] = centroids

        # Per-pair residual cosines (for profile concordance)
        cosines = np.array([1 - cos_dist(centroids[h], centroids[c]) for h, c in pairs])
        model_cosines[model] = cosines

        print(f"  {model:>14}: dim={yaoci.shape[1]}, R²={r2:.4f}, "
              f"mean comp cos={cosines.mean():+.4f}, "
              f"anti-corr={np.sum(cosines < 0)}/32")

    return model_diffs, model_cosines, model_centroids


# ════════════════════════════════════════════════════════════
# Step 3: Direction Concordance
# ════════════════════════════════════════════════════════════

def direction_concordance(model_diffs):
    print(f"\n{'='*70}")
    print("=== DIRECTION CONCORDANCE (Spearman ρ on 32×32 cosine matrices) ===")
    print(f"{'='*70}")

    model_cos_mats = {}
    for model in MODELS:
        dv = model_diffs[model]
        norms = np.linalg.norm(dv, axis=1, keepdims=True)
        unit_dv = dv / norms
        model_cos_mats[model] = unit_dv @ unit_dv.T

    triu = np.triu_indices(N_PAIRS, k=1)
    rho_matrix = np.eye(len(MODELS))
    rho_dict = {}

    for i, m1 in enumerate(MODELS):
        for j, m2 in enumerate(MODELS):
            if j <= i:
                continue
            vec1 = model_cos_mats[m1][triu]
            vec2 = model_cos_mats[m2][triu]
            rho, p = spearmanr(vec1, vec2)
            rho_matrix[i, j] = rho_matrix[j, i] = rho
            rho_dict[(m1, m2)] = (rho, p)

    # Print matrix
    header = f"{'':>14}" + "".join(f"{m:>14}" for m in MODELS)
    print(f"\n{header}")
    for i, m1 in enumerate(MODELS):
        row = f"{m1:>14}"
        for j, m2 in enumerate(MODELS):
            if i == j:
                row += f"{'—':>14}"
            elif j > i:
                rho = rho_dict[(m1, m2)][0]
                row += f"{rho:>14.4f}"
            else:
                rho = rho_dict[(m2, m1)][0]
                row += f"{rho:>14.4f}"
        print(row)

    print(f"\n  Prior Tier 1b threshold: ρ > {TIER1B_THRESHOLD}")

    # Separate existing vs siku
    existing_rhos = [rho_dict[(m1, m2)][0]
                     for m1, m2 in combinations(MODELS[:3], 2)]
    siku_rhos = [rho_dict[(m1, 'sikuroberta')][0] if (m1, 'sikuroberta') in rho_dict
                 else rho_dict[('sikuroberta', m1)][0]
                 for m1 in MODELS[:3]]

    print(f"  Existing 3-model ρ range: {min(existing_rhos):.4f} – {max(existing_rhos):.4f}")
    print(f"  SikuRoBERTa ρ range:     {min(siku_rhos):.4f} – {max(siku_rhos):.4f}")

    passes = all(r >= TIER1B_THRESHOLD for r in siku_rhos)
    print(f"  All SikuRoBERTa ρ > {TIER1B_THRESHOLD}: {'YES' if passes else 'NO'}")

    return rho_dict, rho_matrix, passes


# ════════════════════════════════════════════════════════════
# Step 4: Procrustes Alignment R²
# ════════════════════════════════════════════════════════════

def procrustes_analysis(model_diffs):
    print(f"\n{'='*70}")
    print("=== PROCRUSTES R² ===")
    print(f"{'='*70}")

    ks = [5, 8, 10, 15, 20]
    pairs_list = list(combinations(MODELS, 2))
    results = {}

    # Header
    header = f"{'k':>4}" + "".join(f"  {m1[:5]}↔{m2[:5]:>5}" for m1, m2 in pairs_list)
    print(f"\n{header}")
    print("  " + "─" * (4 + 13 * len(pairs_list)))

    for k in ks:
        pca_reduced = {}
        for model in MODELS:
            dv = model_diffs[model]
            n_comp = min(k, dv.shape[0] - 1, dv.shape[1])
            pca = PCA(n_components=n_comp)
            pca_reduced[model] = pca.fit_transform(dv)

        row = f"{k:>4}"
        for m1, m2 in pairs_list:
            A = pca_reduced[m1][:, :min(k, pca_reduced[m1].shape[1])]
            B = pca_reduced[m2][:, :min(k, pca_reduced[m2].shape[1])]
            min_cols = min(A.shape[1], B.shape[1])
            A, B = A[:, :min_cols], B[:, :min_cols]

            A = A - A.mean(axis=0)
            B = B - B.mean(axis=0)
            A = A / np.linalg.norm(A, 'fro')
            B = B / np.linalg.norm(B, 'fro')

            R, _ = orthogonal_procrustes(A, B)
            A_aligned = A @ R
            ss_res = np.sum((A_aligned - B) ** 2)
            ss_tot = np.sum(B ** 2)
            r2 = 1.0 - ss_res / ss_tot

            results[(m1, m2, k)] = r2
            row += f"  {r2:>11.4f}"
        print(row)

    # Summary at k=20
    print(f"\n  At k=20:")
    existing_r2 = [results[(m1, m2, 20)] for m1, m2 in combinations(MODELS[:3], 2)]
    siku_r2 = [results[(m1, 'sikuroberta', 20)] if (m1, 'sikuroberta', 20) in results
               else results[('sikuroberta', m1, 20)] if ('sikuroberta', m1, 20) in results
               else None
               for m1 in MODELS[:3]]
    siku_r2 = [r for r in siku_r2 if r is not None]

    # Fix: find all pairs involving sikuroberta
    siku_r2 = []
    for m1, m2 in combinations(MODELS, 2):
        if 'sikuroberta' in (m1, m2):
            siku_r2.append(results[(m1, m2, 20)])

    print(f"    Existing 3-model R² range: {min(existing_r2):.4f} – {max(existing_r2):.4f}")
    print(f"    SikuRoBERTa R² range:      {min(siku_r2):.4f} – {max(siku_r2):.4f}")

    return results


# ════════════════════════════════════════════════════════════
# Step 5: Per-Pair Profile Concordance
# ════════════════════════════════════════════════════════════

def profile_concordance(model_cosines):
    print(f"\n{'='*70}")
    print("=== PER-PAIR PROFILE CONCORDANCE ===")
    print(f"{'='*70}")
    print("  (Spearman ρ on 32-element anti-correlation vectors)")

    rho_dict = {}
    header = f"{'':>14}" + "".join(f"{m:>14}" for m in MODELS)
    print(f"\n{header}")

    for i, m1 in enumerate(MODELS):
        row = f"{m1:>14}"
        for j, m2 in enumerate(MODELS):
            if i == j:
                row += f"{'—':>14}"
            elif j > i:
                rho, p = spearmanr(model_cosines[m1], model_cosines[m2])
                rho_dict[(m1, m2)] = (rho, p)
                row += f"{rho:>14.4f}"
            else:
                rho = rho_dict[(m2, m1)][0]
                row += f"{rho:>14.4f}"
        print(row)

    existing_rhos = [rho_dict[(m1, m2)][0] for m1, m2 in combinations(MODELS[:3], 2)]
    siku_rhos = []
    for m1, m2 in combinations(MODELS, 2):
        if 'sikuroberta' in (m1, m2):
            siku_rhos.append(rho_dict[(m1, m2)][0])

    print(f"\n  Existing 3-model ρ range: {min(existing_rhos):.4f} – {max(existing_rhos):.4f}")
    print(f"  SikuRoBERTa ρ range:     {min(siku_rhos):.4f} – {max(siku_rhos):.4f}")

    return rho_dict


# ════════════════════════════════════════════════════════════
# Step 6: Diagnostic (rank discrepancy analysis)
# ════════════════════════════════════════════════════════════

def diagnostic(model_cosines, atlas, pairs, direction_passes):
    print(f"\n{'='*70}")
    print("=== DIAGNOSTIC ===")
    print(f"{'='*70}")

    if direction_passes:
        print("  All SikuRoBERTa direction ρ above threshold — diagnostic not triggered.")
        return

    # Compute per-pair ranks for each model
    ranks = {}
    for model in MODELS:
        order = np.argsort(model_cosines[model])  # ascending (most negative first)
        r = np.empty_like(order)
        r[order] = np.arange(N_PAIRS)
        ranks[model] = r

    # Average rank across multilingual models
    avg_multi_rank = np.mean([ranks[m] for m in MODELS[:3]], axis=0)
    siku_rank = ranks['sikuroberta']

    # Rank discrepancy
    discrepancy = np.abs(siku_rank - avg_multi_rank)
    top5_idx = np.argsort(discrepancy)[-5:][::-1]

    print(f"\n  Top 5 complement pairs by rank discrepancy (SikuRoBERTa vs multilingual avg):")
    print(f"  {'Pair':>20} {'Siku rank':>10} {'Multi avg':>10} {'|Δ|':>8} {'Siku cos':>10} {'BGE cos':>10}")
    print("  " + "─" * 72)

    exception_set = set()
    for model in MODELS:
        for i, (h, c) in enumerate(pairs):
            if model_cosines[model][i] >= 0:
                exception_set.add(i)

    for idx in top5_idx:
        h, c = pairs[idx]
        name_h = atlas[str(h)].get('kw_name', str(h))
        name_c = atlas[str(c)].get('kw_name', str(c))
        pair_str = f"{name_h}↔{name_c}"
        is_exc = "← exception" if idx in exception_set else ""
        print(f"  {pair_str:>20} {siku_rank[idx]:>10.0f} {avg_multi_rank[idx]:>10.1f} "
              f"{discrepancy[idx]:>8.1f} {model_cosines['sikuroberta'][idx]:>+10.4f} "
              f"{model_cosines['bge-m3'][idx]:>+10.4f}  {is_exc}")

    n_overlap = sum(1 for idx in top5_idx if idx in exception_set)
    print(f"\n  Overlap with exception set (residual cosine ≥ 0): {n_overlap}/5")


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════

def main():
    print("Pair-Level Concordance Test (R213 candidate)")
    print("=" * 70)

    atlas = load_atlas()
    meta = build_yaoci_meta(atlas)
    pairs = get_complement_pairs(atlas)

    print(f"\nLoading 4 models and computing residual complement diff vectors:")
    model_diffs, model_cosines, model_centroids = load_all_models(atlas, meta, pairs)

    # Step 3
    rho_dict, rho_matrix, direction_passes = direction_concordance(model_diffs)

    # Step 4
    procrustes_results = procrustes_analysis(model_diffs)

    # Step 5
    profile_rhos = profile_concordance(model_cosines)

    # Step 6
    diagnostic(model_cosines, atlas, pairs, direction_passes)

    # ── Final Verdict ──
    print(f"\n{'='*70}")
    print("=== VERDICT ===")
    print(f"{'='*70}")

    # Direction concordance
    siku_dir_rhos = []
    for m1, m2 in combinations(MODELS, 2):
        if 'sikuroberta' in (m1, m2):
            siku_dir_rhos.append(rho_dict[(m1, m2)][0])
    min_siku_dir = min(siku_dir_rhos)
    dir_verdict = "PASSES" if direction_passes else "FAILS"

    # Procrustes at k=20
    siku_proc_r2 = []
    for m1, m2 in combinations(MODELS, 2):
        if 'sikuroberta' in (m1, m2):
            siku_proc_r2.append(procrustes_results[(m1, m2, 20)])
    mean_siku_proc = np.mean(siku_proc_r2)

    existing_proc_r2 = [procrustes_results[(m1, m2, 20)]
                        for m1, m2 in combinations(MODELS[:3], 2)]
    mean_existing_proc = np.mean(existing_proc_r2)

    # Profile concordance
    siku_prof_rhos = []
    for m1, m2 in combinations(MODELS, 2):
        if 'sikuroberta' in (m1, m2):
            siku_prof_rhos.append(profile_rhos[(m1, m2)][0])
    mean_siku_prof = np.mean(siku_prof_rhos)

    print(f"  Pair-level direction concordance: {dir_verdict} ρ > {TIER1B_THRESHOLD} threshold")
    print(f"    SikuRoBERTa ρ range: {min(siku_dir_rhos):.4f} – {max(siku_dir_rhos):.4f}")
    print(f"  Procrustes R² at k=20: {mean_siku_proc:.4f} (vs prior {mean_existing_proc:.4f})")
    print(f"  Profile concordance:   {mean_siku_prof:.4f}")
    print(f"    SikuRoBERTa ρ range: {min(siku_prof_rhos):.4f} – {max(siku_prof_rhos):.4f}")

    # Sage's prediction comparison
    print(f"\n  Sage predicted ρ ≈ 0.55–0.65 for SikuRoBERTa direction concordance")
    print(f"  Actual: {min(siku_dir_rhos):.4f} – {max(siku_dir_rhos):.4f}")


if __name__ == '__main__':
    main()
