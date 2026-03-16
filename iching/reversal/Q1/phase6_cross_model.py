#!/usr/bin/env python3
"""Q1 Phase 6: Cross-model robustness.

Tests which findings about the thematic manifold are properties of the TEXT
versus artifacts of one embedding model (BGE-M3).

Models: BGE-M3 (baseline), multilingual-e5-large, gte-multilingual-base
Tests per model: algebraic R², complement anti-correlation, effective dim,
                 participation ratio, exception set, Mantel test, bridge smoothness
Cross-model: per-pair complement cosine concordance, exception set overlap
"""

import numpy as np
import json
import gc
from pathlib import Path
from collections import defaultdict

from scipy.spatial.distance import cosine as cos_dist, pdist, squareform
from scipy.stats import pearsonr, spearmanr
from sklearn.decomposition import PCA

from phase1_residual_structure import load_data, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
YAOCI_PATH = ROOT.parent / "texts" / "iching" / "yaoci.json"
EXISTING_EMB = ROOT / "synthesis" / "embeddings.npz"
OUT_DIR = Path(__file__).resolve().parent

N_PERM = 10_000
N_MANTEL = 1000
RNG = np.random.default_rng(42)

MODELS = [
    ('bge-m3', 'BAAI/bge-m3'),
    ('e5-large', 'intfloat/multilingual-e5-large'),
    ('labse', 'sentence-transformers/LaBSE'),
]


# ═══════════════════════════════════════════════════════
# Text extraction (hex-index order)
# ═══════════════════════════════════════════════════════

def load_texts():
    """Load 384 yaoci texts in hex_idx (0-63) × line (0-5) order."""
    atlas = json.load(open(ATLAS_PATH))
    yaoci_data = json.load(open(YAOCI_PATH))

    # hex_idx -> kw_number
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


# ═══════════════════════════════════════════════════════
# Embedding
# ═══════════════════════════════════════════════════════

def embed_all_models(texts):
    """Embed texts with each model. Returns dict: shortname → (384, dim) array."""
    import torch
    from sentence_transformers import SentenceTransformer

    embeddings = {}

    for shortname, model_name in MODELS:
        cache_path = OUT_DIR / f"embeddings_{shortname}.npz"
        if cache_path.exists():
            emb = np.load(cache_path)['yaoci']
            print(f"  [{shortname}] Loaded cached embeddings: {emb.shape}")
            embeddings[shortname] = emb
            continue

        print(f"\n  [{shortname}] Loading {model_name}...")
        model = SentenceTransformer(model_name, device='cuda')
        dim = model.get_sentence_embedding_dimension()
        print(f"  [{shortname}] Embedding dim: {dim}")

        emb = model.encode(texts, normalize_embeddings=True,
                           batch_size=64, show_progress_bar=True)
        emb = emb.astype(np.float32)
        print(f"  [{shortname}] Embedded: {emb.shape}, norm[0]={np.linalg.norm(emb[0]):.4f}")

        np.savez_compressed(cache_path, yaoci=emb)
        embeddings[shortname] = emb

        # Free GPU
        del model
        torch.cuda.empty_cache()
        gc.collect()

    # Verify BGE-M3 against existing
    existing = np.load(EXISTING_EMB)['yaoci']
    cos_sims = np.sum(embeddings['bge-m3'] * existing, axis=1)
    min_sim = cos_sims.min()
    print(f"\n  BGE-M3 verification: min cosine to existing = {min_sim:.6f}")
    assert min_sim > 0.99, f"BGE-M3 mismatch! min cosine = {min_sim}"

    return embeddings


# ═══════════════════════════════════════════════════════
# Structural data (atlas, pairs, complements)
# ═══════════════════════════════════════════════════════

def load_structure():
    """Load atlas, build complement pairs, KW ordering."""
    atlas = json.load(open(ATLAS_PATH))

    kw_map = {int(k): v['kw_number'] for k, v in atlas.items()
              if k.isdigit() and int(k) < 64}
    kw_order = sorted(range(64), key=lambda h: kw_map[h])

    # 32 complement pairs (structural, not KW-pair)
    complement_pairs = []
    seen = set()
    for h in range(64):
        c = atlas[str(h)]['complement']
        key = (min(h, c), max(h, c))
        if key not in seen:
            complement_pairs.append(key)
            seen.add(key)
    assert len(complement_pairs) == 32

    # 32 KW pairs
    kw_pairs = [(kw_order[2*i], kw_order[2*i+1]) for i in range(32)]

    # Element pairs per hex (for anti-clustering)
    def elem_pair(h):
        a = atlas[str(h)]
        return (a['lower_trigram']['element'], a['upper_trigram']['element'])

    # 6-bit binary strings for Hamming distance
    binary = {h: format(h, '06b') for h in range(64)}

    return {
        'atlas': atlas,
        'kw_map': kw_map,
        'kw_order': kw_order,
        'complement_pairs': complement_pairs,
        'kw_pairs': kw_pairs,
        'elem_pair': elem_pair,
        'binary': binary,
    }


# ═══════════════════════════════════════════════════════
# Null permutations (model-independent)
# ═══════════════════════════════════════════════════════

def generate_null_perms(structure):
    """Same null model as Phase 4: permute 30 interior KW pairs."""
    kw_pairs = structure['kw_pairs']
    elem_pair = structure['elem_pair']
    interior = list(range(1, 31))

    tail_elem = [elem_pair(kw_pairs[i][1]) for i in range(32)]
    head_elem = [elem_pair(kw_pairs[i][0]) for i in range(32)]

    perms = []
    n_tried = 0
    while len(perms) < N_PERM:
        perm = [0] + list(RNG.permutation(interior)) + [31]
        ok = True
        for j in range(31):
            if tail_elem[perm[j]] == head_elem[perm[j+1]]:
                ok = False
                break
        if ok:
            perms.append(perm)
        n_tried += 1

    print(f"  Null model: {N_PERM} perms, acceptance={len(perms)/n_tried:.3f}")
    return perms


# ═══════════════════════════════════════════════════════
# Per-model analysis
# ═══════════════════════════════════════════════════════

def analyze_model(shortname, yaoci_emb, structure, null_perms):
    """Run all per-model tests. Returns results dict."""
    print(f"\n{'='*70}")
    print(f"MODEL: {shortname} ({yaoci_emb.shape})")
    print(f"{'='*70}")

    atlas = structure['atlas']
    complement_pairs = structure['complement_pairs']
    kw_pairs = structure['kw_pairs']

    results = {'shortname': shortname, 'dim': yaoci_emb.shape[1]}

    # ── A: Algebraic regression ──
    _, meta, _ = load_data()
    X, _ = build_design_matrix(meta)
    residual, r2, _ = extract_residuals(yaoci_emb, X)
    results['algebraic_r2'] = float(r2)
    print(f"\n  A. Algebraic R²: {r2:.4f}")

    # ── Hex centroids (raw and residual) ──
    raw_centroids = np.array([yaoci_emb[h*6:(h+1)*6].mean(axis=0) for h in range(64)])
    res_centroids = np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(64)])

    # ── B: Complement anti-correlation ──
    raw_comp_cosines = []
    res_comp_cosines = []
    for h1, h2 in complement_pairs:
        raw_cos = 1 - cos_dist(raw_centroids[h1], raw_centroids[h2])
        res_cos = 1 - cos_dist(res_centroids[h1], res_centroids[h2])
        raw_comp_cosines.append(raw_cos)
        res_comp_cosines.append(res_cos)

    raw_comp_cosines = np.array(raw_comp_cosines)
    res_comp_cosines = np.array(res_comp_cosines)

    n_anti = np.sum(res_comp_cosines < 0)
    results['raw_comp_cos_mean'] = float(np.mean(raw_comp_cosines))
    results['res_comp_cos_mean'] = float(np.mean(res_comp_cosines))
    results['n_anti_corr'] = int(n_anti)
    results['res_comp_cosines'] = res_comp_cosines.tolist()

    print(f"  B. Complement anti-correlation:")
    print(f"     Raw mean cosine:      {np.mean(raw_comp_cosines):+.5f}")
    print(f"     Residual mean cosine: {np.mean(res_comp_cosines):+.5f}")
    print(f"     Anti-correlated pairs: {n_anti}/32")

    # ── C: Effective dimensionality ──
    pca = PCA(n_components=min(32, res_centroids.shape[1]))
    pca.fit(res_centroids)
    var_exp = pca.explained_variance_ratio_
    cumvar = np.cumsum(var_exp)
    n90 = int(np.searchsorted(cumvar, 0.90) + 1)
    results['eff_dim_90'] = n90
    results['pc1_var'] = float(var_exp[0])
    print(f"  C. Effective dim (90% var): {n90} PCs, PC1={var_exp[0]:.3f}")

    # ── D: Participation ratio ──
    diff_vecs = np.array([res_centroids[h1] - res_centroids[h2]
                          for h1, h2 in complement_pairs])
    _, S, _ = np.linalg.svd(diff_vecs, full_matrices=False)
    lam = S**2
    pr = (np.sum(lam))**2 / np.sum(lam**2)
    results['participation_ratio'] = float(pr)
    print(f"  D. Participation ratio: {pr:.2f}")

    # ── E: Exception set ──
    exceptions = []
    for i, (h1, h2) in enumerate(complement_pairs):
        if res_comp_cosines[i] >= 0:
            a1, a2 = atlas[str(h1)], atlas[str(h2)]
            exceptions.append((h1, h2, a1['kw_name'], a2['kw_name'],
                              float(res_comp_cosines[i])))
    results['exception_set'] = exceptions
    print(f"  E. Exception set ({len(exceptions)} pairs):")
    for h1, h2, n1, n2, cos in exceptions:
        print(f"     {n1}({h1})↔{n2}({h2}): cosine={cos:+.5f}")

    # ── F: Mantel test ──
    res_dist = squareform(pdist(res_centroids, 'cosine'))
    hamming_dist = np.zeros((64, 64))
    binary = structure['binary']
    for i in range(64):
        for j in range(i+1, 64):
            d = sum(a != b for a, b in zip(binary[i], binary[j]))
            hamming_dist[i, j] = d
            hamming_dist[j, i] = d

    # Extract upper triangle
    triu_idx = np.triu_indices(64, k=1)
    res_upper = res_dist[triu_idx]
    ham_upper = hamming_dist[triu_idx]

    r_mantel, _ = pearsonr(res_upper, ham_upper)
    # Permutation test
    null_r = []
    for _ in range(N_MANTEL):
        perm = RNG.permutation(64)
        perm_dist = res_dist[np.ix_(perm, perm)]
        null_r.append(pearsonr(perm_dist[triu_idx], ham_upper)[0])
    null_r = np.array(null_r)
    mantel_p = np.mean(np.abs(null_r) >= np.abs(r_mantel))

    results['mantel_r'] = float(r_mantel)
    results['mantel_p'] = float(mantel_p)
    print(f"  F. Mantel test (residual×Hamming): r={r_mantel:+.4f}, p={mantel_p:.4f}")

    # ── G: Bridge smoothness ──
    kw_pairs_list = structure['kw_pairs']

    def compute_bridges_from_centroids(perm, centroids, pairs):
        bridges = []
        for j in range(31):
            h2_prev = pairs[perm[j]][1]
            h1_next = pairs[perm[j+1]][0]
            bridges.append(cos_dist(centroids[h2_prev], centroids[h1_next]))
        return np.array(bridges)

    kw_perm = list(range(32))
    kw_bridges = compute_bridges_from_centroids(kw_perm, res_centroids, kw_pairs_list)
    kw_mean_bridge = float(np.mean(kw_bridges))

    null_means = []
    for perm in null_perms:
        bridges = compute_bridges_from_centroids(perm, res_centroids, kw_pairs_list)
        null_means.append(np.mean(bridges))
    null_means = np.array(null_means)

    bridge_pct = float(np.mean(null_means <= kw_mean_bridge) * 100)
    bridge_z = float((kw_mean_bridge - np.mean(null_means)) / np.std(null_means))

    results['bridge_kw_mean'] = kw_mean_bridge
    results['bridge_null_mean'] = float(np.mean(null_means))
    results['bridge_null_std'] = float(np.std(null_means))
    results['bridge_pct'] = bridge_pct
    results['bridge_z'] = bridge_z
    print(f"  G. Bridge smoothness: KW={kw_mean_bridge:.5f}, "
          f"null={np.mean(null_means):.5f}±{np.std(null_means):.5f}, "
          f"pct={bridge_pct:.1f}%, z={bridge_z:+.2f}")

    return results


# ═══════════════════════════════════════════════════════
# Cross-model concordance
# ═══════════════════════════════════════════════════════

def cross_model_concordance(all_results):
    """Compare per-pair complement cosines across models."""
    print(f"\n{'='*70}")
    print("CROSS-MODEL CONCORDANCE")
    print(f"{'='*70}")

    names = [r['shortname'] for r in all_results]
    cosines = {r['shortname']: np.array(r['res_comp_cosines']) for r in all_results}
    exceptions = {r['shortname']: set(
        (e[0], e[1]) for e in r['exception_set']
    ) for r in all_results}

    concordance = {}

    # Pairwise Spearman on per-pair cosines
    print("\n  Per-pair complement cosine concordance (Spearman ρ):")
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            n1, n2 = names[i], names[j]
            rho, p = spearmanr(cosines[n1], cosines[n2])
            print(f"    {n1} ↔ {n2}: ρ={rho:+.4f}, p={p:.4f}")
            concordance[f'{n1}_{n2}_spearman'] = float(rho)
            concordance[f'{n1}_{n2}_spearman_p'] = float(p)

    # Exception set overlap (Jaccard)
    print("\n  Exception set overlap (Jaccard):")
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            n1, n2 = names[i], names[j]
            s1, s2 = exceptions[n1], exceptions[n2]
            if len(s1 | s2) == 0:
                jaccard = 1.0
            else:
                jaccard = len(s1 & s2) / len(s1 | s2)
            print(f"    {n1} ↔ {n2}: |{n1}|={len(s1)}, |{n2}|={len(s2)}, "
                  f"intersection={len(s1 & s2)}, Jaccard={jaccard:.3f}")
            concordance[f'{n1}_{n2}_jaccard'] = float(jaccard)

    return concordance


# ═══════════════════════════════════════════════════════
# Degenerate embedding check
# ═══════════════════════════════════════════════════════

def check_degenerate(shortname, emb):
    """Check if a model produced degenerate embeddings."""
    # All-pairs mean cosine on a random subset
    idx = RNG.choice(384, size=50, replace=False)
    subset = emb[idx]
    cos_mat = subset @ subset.T
    # Off-diagonal mean
    mask = ~np.eye(50, dtype=bool)
    mean_cos = cos_mat[mask].mean()
    std_cos = cos_mat[mask].std()
    print(f"  [{shortname}] Mean pairwise cosine: {mean_cos:.4f} ± {std_cos:.4f}")
    if mean_cos > 0.95:
        print(f"  ⚠️ [{shortname}] DEGENERATE — embeddings near-identical!")
        return True
    return False


# ═══════════════════════════════════════════════════════
# Report
# ═══════════════════════════════════════════════════════

def write_report(all_results, concordance):
    """Write markdown summary."""
    lines = [
        "# Phase 6: Cross-Model Robustness",
        "",
        f"3 models, {N_PERM} null permutations, {N_MANTEL} Mantel permutations.",
        "",
        "## Summary Table",
        "",
        "| Metric | " + " | ".join(r['shortname'] for r in all_results) + " |",
        "|--------|" + "|".join("--------:" for _ in all_results) + "|",
    ]

    metrics = [
        ('Dim', 'dim', 'd'),
        ('Algebraic R²', 'algebraic_r2', '.4f'),
        ('Raw complement cos', 'raw_comp_cos_mean', '+.4f'),
        ('Resid complement cos', 'res_comp_cos_mean', '+.4f'),
        ('Anti-corr pairs (/32)', 'n_anti_corr', 'd'),
        ('Eff dim (90%)', 'eff_dim_90', 'd'),
        ('PC1 var', 'pc1_var', '.3f'),
        ('Participation ratio', 'participation_ratio', '.1f'),
        ('Mantel r', 'mantel_r', '+.4f'),
        ('Mantel p', 'mantel_p', '.4f'),
        ('Bridge KW mean', 'bridge_kw_mean', '.5f'),
        ('Bridge %ile', 'bridge_pct', '.1f'),
        ('Bridge z', 'bridge_z', '+.2f'),
    ]

    for label, key, fmt in metrics:
        vals = []
        for r in all_results:
            v = r[key]
            vals.append(format(v, fmt))
        lines.append(f"| {label} | " + " | ".join(vals) + " |")

    # Exception sets
    lines += ["", "## Exception Sets (complement pairs with residual cosine ≥ 0)", ""]
    for r in all_results:
        exc = r['exception_set']
        lines.append(f"### {r['shortname']} ({len(exc)} pairs)")
        if exc:
            for h1, h2, n1, n2, cos in exc:
                lines.append(f"- {n1}({h1})↔{n2}({h2}): {cos:+.5f}")
        else:
            lines.append("- None")
        lines.append("")

    # Cross-model concordance
    names = [r['shortname'] for r in all_results]
    lines += ["## Cross-Model Concordance", ""]
    lines.append("### Per-pair complement cosine (Spearman ρ)")
    lines.append("")
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            key = f'{names[i]}_{names[j]}_spearman'
            rho = concordance[key]
            p = concordance[f'{key}_p']
            lines.append(f"- {names[i]} ↔ {names[j]}: ρ={rho:+.4f} (p={p:.4f})")
    lines.append("")

    lines.append("### Exception set overlap (Jaccard)")
    lines.append("")
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            key = f'{names[i]}_{names[j]}_jaccard'
            lines.append(f"- {names[i]} ↔ {names[j]}: {concordance[key]:.3f}")
    lines.append("")

    out_path = OUT_DIR / "phase6_cross_model_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nReport saved to {out_path}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 6: Cross-Model Robustness")
    print("=" * 70)

    # Step 0: Load texts and structure
    print("\nLoading texts and structure...")
    texts = load_texts()
    structure = load_structure()

    # Step 1: Embed with all models
    print("\nStep 1: Multi-model embedding")
    embeddings = embed_all_models(texts)

    # Check for degenerate models
    print("\nDegenerate check:")
    degenerate = set()
    for shortname, emb in embeddings.items():
        if check_degenerate(shortname, emb):
            degenerate.add(shortname)

    # Step 2: Generate null permutations (model-independent)
    print("\nGenerating null permutations...")
    null_perms = generate_null_perms(structure)

    # Step 3: Per-model analysis
    all_results = []
    for shortname, emb in embeddings.items():
        if shortname in degenerate:
            print(f"\n  SKIPPING {shortname} (degenerate)")
            continue
        r = analyze_model(shortname, emb, structure, null_perms)
        all_results.append(r)

    # Step 4: Cross-model concordance
    concordance = cross_model_concordance(all_results)

    # Step 5: Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'Model':<12} {'R²':>6} {'RawCos':>8} {'ResCos':>8} {'Anti':>5} "
          f"{'Dim90':>6} {'PR':>6} {'Mantel':>8} {'Bridge%':>8}")
    print("-" * 75)
    for r in all_results:
        print(f"{r['shortname']:<12} {r['algebraic_r2']:>6.4f} "
              f"{r['raw_comp_cos_mean']:>+8.4f} {r['res_comp_cos_mean']:>+8.4f} "
              f"{r['n_anti_corr']:>5}/32 {r['eff_dim_90']:>6} "
              f"{r['participation_ratio']:>6.1f} {r['mantel_r']:>+8.4f} "
              f"{r['bridge_pct']:>7.1f}%")

    # Key finding
    anti_counts = [r['n_anti_corr'] for r in all_results]
    if all(n >= 28 for n in anti_counts):
        print("\n✓ Complement anti-correlation is ROBUST across all models (≥28/32)")
    elif all(n >= 20 for n in anti_counts):
        print("\n~ Complement anti-correlation is MOSTLY robust (≥20/32)")
    else:
        print("\n✗ Complement anti-correlation varies substantially across models")

    write_report(all_results, concordance)


if __name__ == '__main__':
    main()
