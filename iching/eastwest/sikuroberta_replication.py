#!/usr/bin/env python3
"""sikuroberta_replication.py — Cross-architecture replication of Tier 1b findings.

Tests whether R156 (complement anti-correlation), R157 (algebraic R²), and
R159 (Hamming V-shape) replicate on SikuRoBERTa, a classical-Chinese BERT model.

This is the most consequential remaining test: replication extends consensus to
4 architecturally distinct models; failure reclassifies "text-intrinsic" as
"multilingual-transformer-intrinsic."
"""

import json
import gc
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.spatial.distance import cosine as cos_dist, pdist, squareform
from scipy.stats import spearmanr
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

# ════════════════════════════════════════════════════════════
# Paths
# ════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent          # memories/iching
Q1_DIR = ROOT / "reversal" / "Q1"
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
YAOCI_PATH = ROOT.parent / "texts" / "iching" / "yaoci.json"
EMB_CACHE = Q1_DIR / "embeddings_sikuroberta.npz"

N_PERM = 10_000
RNG = np.random.default_rng(42)


# ════════════════════════════════════════════════════════════
# Phase 0: Embedding Extraction
# ════════════════════════════════════════════════════════════

def load_texts():
    """Load 384 yaoci texts in hex_idx (0-63) × line (0-5) order.
    Reused from phase6_cross_model.py."""
    atlas = json.load(open(ATLAS_PATH))
    yaoci_data = json.load(open(YAOCI_PATH))
    hex_to_kw = {}
    for k, v in atlas.items():
        if k.isdigit() and int(k) < 64:
            hex_to_kw[int(k)] = v['kw_number']
    texts = []
    for h in range(64):
        kw_num = hex_to_kw[h]
        entry = yaoci_data['entries'][kw_num - 1]
        assert entry['number'] == kw_num
        for line in entry['lines']:
            texts.append(line['text'])
    assert len(texts) == 384
    return texts


def extract_embeddings(texts):
    """Extract SikuRoBERTa last-hidden-layer embeddings via mean-pooling."""
    if EMB_CACHE.exists():
        emb = np.load(EMB_CACHE)['yaoci']
        print(f"  Loaded cached embeddings: {emb.shape}")
        return emb

    import torch
    from transformers import AutoTokenizer, AutoModel

    MODEL_NAME = "SIKU-BERT/sikuroberta"
    print(f"  Loading {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device).eval()
    print(f"  Device: {device}, hidden size: {model.config.hidden_size}")

    embeddings = []
    batch_size = 32

    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            encoded = tokenizer(batch, padding=True, truncation=True,
                                max_length=512, return_tensors="pt").to(device)
            outputs = model(**encoded)
            last_hidden = outputs.last_hidden_state  # (B, seq_len, hidden)

            # Mean-pool excluding [CLS] (pos 0) and [SEP] + padding
            attention_mask = encoded['attention_mask']  # (B, seq_len)
            # Zero out [CLS] position
            mask = attention_mask.clone()
            mask[:, 0] = 0
            # For each sequence, also zero out the [SEP] token (last non-pad position)
            for b in range(mask.size(0)):
                seq_len = attention_mask[b].sum().item()
                if seq_len > 1:
                    mask[b, seq_len - 1] = 0

            mask_expanded = mask.unsqueeze(-1).float()  # (B, seq_len, 1)
            summed = (last_hidden * mask_expanded).sum(dim=1)
            counts = mask_expanded.sum(dim=1).clamp(min=1)
            pooled = summed / counts  # (B, hidden)

            # L2-normalize
            pooled = torch.nn.functional.normalize(pooled, dim=1)
            embeddings.append(pooled.cpu().numpy())

            if (i // batch_size) % 4 == 0:
                print(f"    Batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")

    embeddings = np.vstack(embeddings).astype(np.float32)
    print(f"  Extracted: {embeddings.shape}, norm[0]={np.linalg.norm(embeddings[0]):.4f}")

    np.savez_compressed(EMB_CACHE, yaoci=embeddings)
    print(f"  Saved to {EMB_CACHE}")

    del model, tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

    return embeddings


# ════════════════════════════════════════════════════════════
# Phase 1: Diagnostic — Participation Ratio
# ════════════════════════════════════════════════════════════

def phase1_diagnostic(yaoci):
    """Compute participation ratio of the covariance matrix."""
    print("\n" + "=" * 60)
    print("PHASE 1: DIAGNOSTIC")
    print("=" * 60)

    centered = yaoci - yaoci.mean(axis=0)
    _, S, _ = np.linalg.svd(centered, full_matrices=False)
    lam = S ** 2
    pr = (lam.sum()) ** 2 / (lam ** 2).sum()

    print(f"  SikuRoBERTa yaoci (384×{yaoci.shape[1]}):")
    print(f"    Participation ratio: {pr:.1f}")
    print(f"    Top 5 singular values: {S[:5].round(2)}")
    print(f"    σ₁/σ₂ = {S[0]/S[1]:.2f}")

    # Compare with BGE-M3
    bge_path = Q1_DIR / "embeddings_bge-m3.npz"
    if bge_path.exists():
        bge = np.load(bge_path)['yaoci']
        bge_centered = bge - bge.mean(axis=0)
        _, S_bge, _ = np.linalg.svd(bge_centered, full_matrices=False)
        lam_bge = S_bge ** 2
        pr_bge = (lam_bge.sum()) ** 2 / (lam_bge ** 2).sum()
        print(f"\n  BGE-M3 yaoci (384×{bge.shape[1]}):")
        print(f"    Participation ratio: {pr_bge:.1f}")
        print(f"    σ₁/σ₂ = {S_bge[0]/S_bge[1]:.2f}")

    adequate = pr > 50
    whiten = pr < 10
    print(f"\n  Verdict: PR={pr:.1f} → {'adequate' if adequate else 'LOW'}")
    if whiten:
        print("  ⚠ PR < 10: whitening applied")
        yaoci = (yaoci - yaoci.mean(axis=0)) / (yaoci.std(axis=0) + 1e-8)

    return yaoci, pr


# ════════════════════════════════════════════════════════════
# Shared Infrastructure
# ════════════════════════════════════════════════════════════

def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)


def build_yaoci_meta(atlas):
    """Build per-yaoci metadata (384 entries)."""
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
    """Build design matrix from all algebraic coordinates.
    Reused from phase1_residual_structure.py."""
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

    num_features = ['depth', 'i_component', 'inner_val', 'hu_depth', 'shi', 'ying']
    num_arrays = [np.array([m[k] for m in meta], dtype=float).reshape(-1, 1)
                  for k in num_features]

    return np.hstack(cat_arrays + num_arrays)


def extract_residuals(yaoci, X):
    """OLS regression: Y = X·B + residual. Returns residuals and R²."""
    reg = LinearRegression()
    reg.fit(X, yaoci)
    predicted = reg.predict(X)
    residual = yaoci - predicted
    total_var = np.var(yaoci, axis=0).sum()
    resid_var = np.var(residual, axis=0).sum()
    r2 = 1 - resid_var / total_var
    return residual, r2


def get_complement_pairs(atlas):
    """32 complement pairs (structural, not KW-pair)."""
    pairs, seen = [], set()
    for h in range(64):
        c = atlas[str(h)]['complement']
        key = (min(h, c), max(h, c))
        if key not in seen:
            pairs.append(key)
            seen.add(key)
    assert len(pairs) == 32
    return pairs


def build_pairs_by_hamming():
    """All 2016 hex pairs grouped by Hamming distance."""
    pairs_by_d = defaultdict(list)
    for i in range(64):
        for j in range(i + 1, 64):
            d = bin(i ^ j).count('1')
            pairs_by_d[d].append((i, j))
    return pairs_by_d


# ════════════════════════════════════════════════════════════
# Phase 2: Replication Tests
# ════════════════════════════════════════════════════════════

def test_r156(res_centroids, complement_pairs):
    """R156: Complement anti-correlation."""
    print("\n  TEST 1 — R156 (Complement Anti-Correlation)")
    print("  " + "─" * 50)

    cosines = []
    for h1, h2 in complement_pairs:
        c = 1 - cos_dist(res_centroids[h1], res_centroids[h2])
        cosines.append(c)
    cosines = np.array(cosines)

    mean_cos = cosines.mean()
    n_negative = (cosines < 0).sum()

    print(f"    Mean residual cosine:   {mean_cos:+.5f}")
    print(f"    Negative pairs:         {n_negative}/32")
    print(f"    Min/Max:                {cosines.min():+.5f} / {cosines.max():+.5f}")

    # Permutation test: shuffle hex labels, recompute mean complement cosine
    n_exceed = 0
    for _ in range(N_PERM):
        perm = RNG.permutation(64)
        perm_cosines = []
        for h1, h2 in complement_pairs:
            c = 1 - cos_dist(res_centroids[perm[h1]], res_centroids[perm[h2]])
            perm_cosines.append(c)
        if np.mean(perm_cosines) <= mean_cos:
            n_exceed += 1
    p_value = (n_exceed + 1) / (N_PERM + 1)

    print(f"    Permutation p-value:    {p_value:.4f}")
    print(f"    Prior (3 models):       mean ≈ −0.19, 28-29/32 negative")

    replicated = mean_cos < 0 and p_value < 0.05
    print(f"    REPLICATED: {'YES' if replicated else 'NO'}")

    return {
        'mean_cos': float(mean_cos),
        'n_negative': int(n_negative),
        'p_value': float(p_value),
        'replicated': replicated,
        'cosines': cosines,
    }


def test_r157(yaoci, meta):
    """R157: Algebraic R²."""
    print("\n  TEST 2 — R157 (Algebraic R²)")
    print("  " + "─" * 50)

    X = build_design_matrix(meta)
    _, r2 = extract_residuals(yaoci, X)

    print(f"    R² (all coordinates + position): {r2:.4f} ({r2*100:.1f}%)")
    print(f"    Prior (3 models):                10.8–11.0%")

    replicated = 0.05 <= r2 <= 0.15
    print(f"    In range [5%, 15%]:              {'YES' if replicated else 'NO'}")
    print(f"    REPLICATED: {'YES' if replicated else 'NO'}")

    return {
        'r2': float(r2),
        'replicated': replicated,
    }


def test_r159(res_centroids, pairs_by_d):
    """R159: Hamming V-shape."""
    print("\n  TEST 3 — R159 (Hamming V-shape)")
    print("  " + "─" * 50)

    dist_mat = squareform(pdist(res_centroids, 'cosine'))

    means = {}
    for d in range(1, 7):
        dists = [dist_mat[i, j] for i, j in pairs_by_d[d]]
        means[d] = np.mean(dists)
        print(f"    d={d}: mean cosine dist = {means[d]:.6f}  (n={len(dists)})")

    v_shape = means[1] > means[2] and means[1] > means[3]
    print(f"\n    d=1 > d=2: {means[1] > means[2]} ({means[1]:.6f} vs {means[2]:.6f})")
    print(f"    d=1 > d=3: {means[1] > means[3]} ({means[1]:.6f} vs {means[3]:.6f})")
    print(f"    Prior (3 models): V-shape with d=1 highest")
    print(f"    REPLICATED: {'YES' if v_shape else 'NO'}")

    return {
        'means': {int(d): float(v) for d, v in means.items()},
        'v_shape': v_shape,
        'replicated': v_shape,
    }


# ════════════════════════════════════════════════════════════
# Phase 3: Cross-Model Correlation
# ════════════════════════════════════════════════════════════

def phase3_cross_model(siku_centroids, atlas):
    """Spearman ρ between pairwise distance matrices across all 4 models."""
    print("\n" + "=" * 60)
    print("PHASE 3: CROSS-MODEL CORRELATION")
    print("=" * 60)

    # Load other models
    models = {}

    # SikuRoBERTa
    models['sikuroberta'] = siku_centroids

    # Load cross-model yaoci and aggregate to centroids
    for name in ['bge-m3', 'e5-large', 'labse']:
        path = Q1_DIR / f"embeddings_{name}.npz"
        if path.exists():
            yaoci = np.load(path)['yaoci']
            centroids = yaoci.reshape(64, 6, -1).mean(axis=1)
            models[name] = centroids
        else:
            print(f"  Warning: {path} not found, skipping")

    # Compute upper-triangle distance vectors
    triu_idx = np.triu_indices(64, k=1)
    dist_vecs = {}
    for name, centroids in models.items():
        dist_mat = squareform(pdist(centroids, 'cosine'))
        dist_vecs[name] = dist_mat[triu_idx]

    # Pairwise Spearman ρ
    names = sorted(models.keys())
    print(f"\n  Spearman ρ between pairwise cosine distance matrices:")
    rho_values = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            rho, p = spearmanr(dist_vecs[n1], dist_vecs[n2])
            rho_values.append(rho)
            is_siku = 'sikuroberta' in (n1, n2)
            marker = " ← NEW" if is_siku else ""
            print(f"    {n1:>14} ↔ {n2:<14}: ρ = {rho:+.4f}  (p = {p:.2e}){marker}")

    # Existing model pairs only
    existing_rhos = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if names[i] != 'sikuroberta' and names[j] != 'sikuroberta':
                rho, _ = spearmanr(dist_vecs[names[i]], dist_vecs[names[j]])
                existing_rhos.append(rho)

    # SikuRoBERTa pairs only
    siku_rhos = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if 'sikuroberta' in (names[i], names[j]):
                rho, _ = spearmanr(dist_vecs[names[i]], dist_vecs[names[j]])
                siku_rhos.append(rho)

    print(f"\n  Existing 3-model ρ range: {min(existing_rhos):.4f} – {max(existing_rhos):.4f}")
    print(f"  SikuRoBERTa ρ range:     {min(siku_rhos):.4f} – {max(siku_rhos):.4f}")

    return {
        'rho_values': rho_values,
        'existing_range': (min(existing_rhos), max(existing_rhos)),
        'siku_range': (min(siku_rhos), max(siku_rhos)),
    }


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════

def main():
    print("SikuRoBERTa Cross-Architecture Replication")
    print("=" * 60)

    # ── Phase 0: Extract embeddings ──
    print("\nPHASE 0: EMBEDDING EXTRACTION")
    print("=" * 60)
    texts = load_texts()
    print(f"  Loaded {len(texts)} yaoci texts")
    yaoci = extract_embeddings(texts)
    print(f"  Embedding shape: {yaoci.shape}")

    # Degeneracy check
    idx = RNG.choice(384, size=50, replace=False)
    subset = yaoci[idx]
    cos_mat = subset @ subset.T
    mask = ~np.eye(50, dtype=bool)
    mean_cos = cos_mat[mask].mean()
    print(f"  Mean pairwise cosine (50 random): {mean_cos:.4f}")
    if mean_cos > 0.95:
        print("  ⚠ DEGENERATE — embeddings near-identical! Results unreliable.")

    # ── Phase 1: Diagnostic ──
    yaoci_diag, pr = phase1_diagnostic(yaoci)

    # ── Phase 2: Replication tests ──
    print("\n" + "=" * 60)
    print("PHASE 2: REPLICATION TESTS")
    print("=" * 60)

    atlas = load_atlas()
    meta = build_yaoci_meta(atlas)

    # Extract residuals at yaoci level
    X = build_design_matrix(meta)
    residual, r2 = extract_residuals(yaoci_diag, X)

    # Aggregate to hex centroids (residual)
    raw_centroids = yaoci_diag.reshape(64, 6, -1).mean(axis=1)
    res_centroids = residual.reshape(64, 6, -1).mean(axis=1)

    complement_pairs = get_complement_pairs(atlas)
    pairs_by_d = build_pairs_by_hamming()

    r156 = test_r156(res_centroids, complement_pairs)
    r157 = test_r157(yaoci_diag, meta)
    r159 = test_r159(res_centroids, pairs_by_d)

    # ── Phase 3: Cross-model correlation ──
    cross = phase3_cross_model(raw_centroids, atlas)

    # ── Verdict ──
    print("\n" + "=" * 60)
    print("=== REPLICATION VERDICT ===")
    print("=" * 60)

    r156_str = "REPLICATED" if r156['replicated'] else "FAILED"
    r157_str = "REPLICATED" if r157['replicated'] else "FAILED"
    r159_str = "REPLICATED" if r159['replicated'] else "FAILED"

    pr_str = f"{pr:.0f} ({'adequate' if pr > 50 else 'degenerate' if pr < 10 else 'marginal'})"
    rho_lo, rho_hi = cross['siku_range']

    print(f"  R156 (complement anti-correlation): {r156_str}")
    print(f"    mean={r156['mean_cos']:+.4f}, {r156['n_negative']}/32 negative, p={r156['p_value']:.4f}")
    print(f"  R157 (algebraic R²):                {r157_str}")
    print(f"    R²={r157['r2']:.4f} ({r157['r2']*100:.1f}%)")
    print(f"  R159 (Hamming V-shape):             {r159_str}")
    print(f"    d=1={r159['means'][1]:.6f}, d=2={r159['means'][2]:.6f}, d=3={r159['means'][3]:.6f}")
    print(f"  Effective dimensionality:           PR = {pr_str}")
    print(f"  Cross-model ρ range:                {rho_lo:.4f} – {rho_hi:.4f}")

    n_replicated = sum([r156['replicated'], r157['replicated'], r159['replicated']])
    if n_replicated == 3:
        print(f"\n  ✓ ALL THREE Tier 1b findings REPLICATE on classical-Chinese BERT")
        print(f"    → Consensus extends to 4 architecturally distinct models")
        print(f"    → 'Text-intrinsic' classification CONFIRMED")
    elif n_replicated == 0:
        print(f"\n  ✗ ALL THREE findings FAIL to replicate")
        print(f"    → Reclassify as 'multilingual-transformer-intrinsic'")
    else:
        print(f"\n  ~ PARTIAL replication ({n_replicated}/3)")
        print(f"    → Findings are architecture-sensitive at this margin")


if __name__ == '__main__':
    main()
