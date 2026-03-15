#!/usr/bin/env python3
"""Q3 Phase 3: 說卦傳 象 Space vs Complement Embedding Geometry.

Tests whether the traditional 象 (image/association) space captures
the same geometric structure that BGE-M3 embeddings detect.

Phases:
  1. Build 說卦傳 association matrix (8 trigrams × N associations)
  2. Build hexagram 象 profiles from trigram pairs
  3. Test correlation with complement embedding geometry
  4. If significant, characterize which 象 categories carry the signal
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from itertools import combinations

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
Q3 = Path(__file__).resolve().parent
ATLAS = ROOT / "atlas" / "atlas.json"
EMBEDDINGS = ROOT.parent / "iching" / "synthesis" / "embeddings.npz"
N_HEX = 64
N_LINES = 6

# Trigram values: binary encoding
# 坤=0(000), 震=1(001), 坎=2(010), 兌=4(100), 艮=3(011),
# 離=5(101), 巽=6(110), 乾=7(111)
TRI_NAMES = {0: '坤', 1: '震', 2: '坎', 3: '艮', 4: '兌', 5: '離', 6: '巽', 7: '乾'}

# ═══════════════════════════════════════════════════════
# Phase 1: 說卦傳 Association Matrix
# ═══════════════════════════════════════════════════════
#
# Built from:
#   - 說卦傳 original text (vol3.txt lines 217-223)
#   - 八卦萬物屬類 (vol1.txt lines 155-169)
#   - Standard 說卦傳 reference
#
# Each association is categorized and each trigram's membership recorded.

SHUOGUA_RAW = {
    '乾': {
        'nature': ['天', '冰', '雪', '寒'],
        'animal': ['馬', '龍'],
        'body': ['首', '頭', '骨', '面'],
        'family': ['父', '老人'],
        'direction': ['西北'],
        'quality': ['剛', '健', '圓', '直', '尊'],
        'material': ['金', '玉', '寶', '珠'],
        'color': ['大赤', '白'],
        'shape': ['圓'],
        'object': ['冠', '鏡', '木果', '水果'],
        'social': ['君', '官', '貴'],
    },
    '坤': {
        'nature': ['地'],
        'animal': ['牛'],
        'body': ['腹'],
        'family': ['母', '老婦'],
        'direction': ['西南'],
        'quality': ['順', '柔', '吝', '均'],
        'material': ['土', '布', '帛', '瓦'],
        'color': ['黃', '黑'],
        'shape': ['方'],
        'object': ['釜', '舆', '裳', '書', '文章'],
        'social': ['眾'],
        'grain': ['黍', '稷', '米', '穀'],
    },
    '震': {
        'nature': ['雷'],
        'animal': ['龍', '蛇', '百蟲'],
        'body': ['足', '髮'],
        'family': ['長男'],
        'direction': ['東'],
        'quality': ['動', '躁', '決', '健'],
        'material': ['竹', '木', '草'],
        'color': ['青', '碧', '綠', '玄黃'],
        'shape': ['長'],
        'object': ['樂器', '蹄', '稼', '柴', '樹'],
        'social': [],
    },
    '巽': {
        'nature': ['風'],
        'animal': ['雞', '百禽'],
        'body': ['股', '眼'],
        'family': ['長女'],
        'direction': ['東南'],
        'quality': ['入', '高', '長', '進退', '不果'],
        'material': ['木', '繩', '草'],
        'color': ['白'],
        'shape': ['直', '長'],
        'object': ['臼', '帆', '扇', '枝葉', '羽毛', '香'],
        'social': ['僧尼', '仙道', '工匠'],
    },
    '坎': {
        'nature': ['水', '雨', '月'],
        'animal': ['豕', '狐', '魚', '水族'],
        'body': ['耳', '血'],
        'family': ['中男'],
        'direction': ['北'],
        'quality': ['險', '隱', '伏', '陷', '憂', '通'],
        'material': ['弓', '輪', '棟'],
        'color': ['黑', '赤'],
        'shape': ['矯', '輮'],
        'object': ['溝渠', '桎梏', '棘', '酒', '鹽', '醢'],
        'social': ['盜', '工'],
    },
    '離': {
        'nature': ['火', '日', '電', '霓霞'],
        'animal': ['雉', '龜', '蟹', '蚌', '鱉', '螺'],
        'body': ['目', '大腹'],
        'family': ['中女'],
        'direction': ['南'],
        'quality': ['明', '麗', '燥', '附'],
        'material': ['甲胄', '戈兵', '文書', '槁木'],
        'color': ['紅', '赤', '紫'],
        'shape': ['中虛'],
        'object': ['爐', '花紋'],
        'social': [],
    },
    '艮': {
        'nature': ['山'],
        'animal': ['狗', '鼠', '虎', '狐'],
        'body': ['手', '指', '鼻', '爪'],
        'family': ['少男', '童子'],
        'direction': ['東北'],
        'quality': ['止', '堅', '靜'],
        'material': ['石', '土'],
        'color': ['黃'],
        'shape': ['小'],
        'object': ['門', '闕', '徑路', '果蓏', '藤'],
        'social': ['閽寺'],
    },
    '兌': {
        'nature': ['澤'],
        'animal': ['羊'],
        'body': ['口', '舌', '肺'],
        'family': ['少女'],
        'direction': ['西'],
        'quality': ['悅', '說', '毀折', '缺'],
        'material': ['金'],
        'color': ['白'],
        'shape': ['上缺'],
        'object': ['帶口之器', '廢物'],
        'social': ['巫', '妾', '奴僕', '婢'],
    },
}

# All association categories
XIANG_CATEGORIES = [
    'nature', 'animal', 'body', 'family', 'direction',
    'quality', 'material', 'color', 'shape', 'object', 'social',
]


def phase1_build_associations():
    """Build the 8×N association matrix from 說卦傳 data."""
    print("=" * 70)
    print("PHASE 1: 說卦傳 Association Matrix")
    print("=" * 70)

    # Collect all unique associations per category
    all_assocs = {}  # category → list of unique items
    for cat in XIANG_CATEGORIES:
        items = set()
        for tri_name, tri_data in SHUOGUA_RAW.items():
            for item in tri_data.get(cat, []):
                items.add(item)
        # Also add 'grain' if present (merge into object)
        all_assocs[cat] = sorted(items)

    # Handle grain separately — merge into object
    grain_items = set()
    for tri_name, tri_data in SHUOGUA_RAW.items():
        for item in tri_data.get('grain', []):
            grain_items.add(item)
    all_assocs['object'] = sorted(set(all_assocs.get('object', [])) | grain_items)

    # Build flat association list with category tags
    flat_assocs = []
    for cat in XIANG_CATEGORIES:
        for item in all_assocs[cat]:
            flat_assocs.append((cat, item))

    N = len(flat_assocs)
    print(f"\n  Total unique associations: {N}")
    for cat in XIANG_CATEGORIES:
        print(f"    {cat:<12}: {len(all_assocs[cat])}")

    # Build 8×N binary matrix
    tri_order = [0, 1, 2, 3, 4, 5, 6, 7]  # binary order
    matrix = np.zeros((8, N), dtype=int)

    for ti, tv in enumerate(tri_order):
        tri_name = TRI_NAMES[tv]
        tri_data = SHUOGUA_RAW[tri_name]
        for fi, (cat, item) in enumerate(flat_assocs):
            items_in_cat = set(tri_data.get(cat, []))
            if cat == 'object':
                items_in_cat |= set(tri_data.get('grain', []))
            if item in items_in_cat:
                matrix[ti, fi] = 1

    # Stats
    print(f"\n  Matrix shape: {matrix.shape}")
    print(f"  Non-zero entries: {matrix.sum()} / {matrix.size} "
          f"({100*matrix.sum()/matrix.size:.1f}%)")
    for ti, tv in enumerate(tri_order):
        print(f"    {TRI_NAMES[tv]}: {matrix[ti].sum()} associations")

    # Save
    save_data = {
        'trigram_order': [TRI_NAMES[tv] for tv in tri_order],
        'trigram_vals': tri_order,
        'associations': [{'category': cat, 'item': item} for cat, item in flat_assocs],
        'categories': {cat: all_assocs[cat] for cat in XIANG_CATEGORIES},
        'matrix': matrix.tolist(),
    }
    with open(Q3 / 'shuogua_associations.json', 'w') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    print(f"\n  Saved to {Q3 / 'shuogua_associations.json'}")

    return matrix, flat_assocs, all_assocs


# ═══════════════════════════════════════════════════════
# Phase 2: Hexagram 象 Profiles
# ═══════════════════════════════════════════════════════

def phase2_hex_profiles(tri_matrix, atlas):
    """Build hexagram 象 profiles from trigram pairs."""
    print("\n" + "=" * 70)
    print("PHASE 2: Hexagram 象 Profiles")
    print("=" * 70)

    N_assoc = tri_matrix.shape[1]

    # Concatenation: [upper_profile, lower_profile] → 2N-dim
    hex_concat = np.zeros((N_HEX, 2 * N_assoc), dtype=int)
    # Union: element-wise OR → N-dim
    hex_union = np.zeros((N_HEX, N_assoc), dtype=int)

    for hv in range(N_HEX):
        h = atlas[str(hv)]
        upper_val = h['upper_trigram']['val']
        lower_val = h['lower_trigram']['val']

        upper_vec = tri_matrix[upper_val]
        lower_vec = tri_matrix[lower_val]

        hex_concat[hv, :N_assoc] = upper_vec
        hex_concat[hv, N_assoc:] = lower_vec
        hex_union[hv] = np.maximum(upper_vec, lower_vec)

    print(f"\n  Concatenation profile: {hex_concat.shape}")
    print(f"  Union profile: {hex_union.shape}")

    # How many distinct profiles?
    unique_concat = len(set(tuple(row) for row in hex_concat))
    unique_union = len(set(tuple(row) for row in hex_union))
    print(f"  Distinct concat profiles: {unique_concat} / {N_HEX}")
    print(f"  Distinct union profiles: {unique_union} / {N_HEX}")

    # Complement pair 象 distances (Hamming)
    comp_hamming_c = []
    comp_hamming_u = []
    comp_pairs = []
    for hv in range(N_HEX):
        cv = int(atlas[str(hv)]['complement'])
        if hv < cv:
            comp_pairs.append((hv, cv))
            hd_c = np.sum(hex_concat[hv] != hex_concat[cv])
            hd_u = np.sum(hex_union[hv] != hex_union[cv])
            comp_hamming_c.append(hd_c)
            comp_hamming_u.append(hd_u)

    print(f"\n  Complement pair Hamming distances (concat):")
    print(f"    mean={np.mean(comp_hamming_c):.1f}, std={np.std(comp_hamming_c):.1f}")
    print(f"  Complement pair Hamming distances (union):")
    print(f"    mean={np.mean(comp_hamming_u):.1f}, std={np.std(comp_hamming_u):.1f}")

    return hex_concat, hex_union, comp_pairs


# ═══════════════════════════════════════════════════════
# Phase 3: Test Against Embedding Geometry
# ═══════════════════════════════════════════════════════

def phase3_test_correlation(hex_concat, hex_union, comp_pairs, atlas):
    """Test whether 象 space predicts embedding geometry."""
    print("\n" + "=" * 70)
    print("PHASE 3: 象 Space vs Embedding Geometry")
    print("=" * 70)

    # Load embeddings and compute hexagram centroids
    emb_data = np.load(str(EMBEDDINGS))
    yaoci_emb = emb_data['yaoci']  # (384, 1024)

    # Reorder to hex_val order (yaoci is in kw_number order)
    # Need mapping: for each hex_val, find kw_number, then index
    kw_to_hv = {}
    for hv in range(N_HEX):
        kw = atlas[str(hv)]['kw_number']
        kw_to_hv[kw] = hv

    hex_centroids = np.zeros((N_HEX, yaoci_emb.shape[1]))
    for kw in range(1, N_HEX + 1):
        hv = kw_to_hv[kw]
        start = (kw - 1) * N_LINES
        hex_centroids[hv] = yaoci_emb[start:start + N_LINES].mean(axis=0)

    print(f"\n  Hex centroids: {hex_centroids.shape}")

    # ─── 3a: Mantel test (full distance matrix correlation) ───
    print(f"\n  --- 3a: Mantel Test ---")

    from scipy.spatial.distance import pdist, squareform
    from scipy.stats import pearsonr, spearmanr

    # Distance matrices
    emb_dist = pdist(hex_centroids, metric='cosine')
    xiang_dist_c = pdist(hex_concat, metric='hamming')
    xiang_dist_u = pdist(hex_union, metric='hamming')

    # Mantel: correlation of distance matrices
    r_c, p_c = pearsonr(emb_dist, xiang_dist_c)
    r_u, p_u = pearsonr(emb_dist, xiang_dist_u)
    rs_c, ps_c = spearmanr(emb_dist, xiang_dist_c)
    rs_u, ps_u = spearmanr(emb_dist, xiang_dist_u)

    print(f"  Concat 象 vs embedding distance:")
    print(f"    Pearson r={r_c:.4f}, p={p_c:.4g}")
    print(f"    Spearman ρ={rs_c:.4f}, p={ps_c:.4g}")
    print(f"  Union 象 vs embedding distance:")
    print(f"    Pearson r={r_u:.4f}, p={p_u:.4g}")
    print(f"    Spearman ρ={rs_u:.4f}, p={ps_u:.4g}")

    # Permutation test for Mantel
    n_perm = 9999
    r_observed_c = r_c
    r_observed_u = r_u
    count_c = 0
    count_u = 0
    for _ in range(n_perm):
        perm = np.random.permutation(N_HEX)
        perm_centroids = hex_centroids[perm]
        perm_dist = pdist(perm_centroids, metric='cosine')
        r_perm_c = np.corrcoef(perm_dist, xiang_dist_c)[0, 1]
        r_perm_u = np.corrcoef(perm_dist, xiang_dist_u)[0, 1]
        if r_perm_c >= r_observed_c:
            count_c += 1
        if r_perm_u >= r_observed_u:
            count_u += 1

    p_perm_c = (count_c + 1) / (n_perm + 1)
    p_perm_u = (count_u + 1) / (n_perm + 1)
    print(f"\n  Permutation test ({n_perm} permutations):")
    print(f"    Concat: p_perm={p_perm_c:.4f}")
    print(f"    Union:  p_perm={p_perm_u:.4f}")

    # ─── 3b: Complement-specific test ───
    print(f"\n  --- 3b: Complement-Specific Test ---")

    # For each complement pair: difference vectors in both spaces
    n_pairs = len(comp_pairs)
    emb_diffs = np.zeros((n_pairs, hex_centroids.shape[1]))
    xiang_diffs_c = np.zeros((n_pairs, hex_concat.shape[1]))
    xiang_diffs_u = np.zeros((n_pairs, hex_union.shape[1]))

    for i, (h, c) in enumerate(comp_pairs):
        emb_diffs[i] = hex_centroids[h] - hex_centroids[c]
        xiang_diffs_c[i] = hex_concat[h].astype(float) - hex_concat[c].astype(float)
        xiang_diffs_u[i] = hex_union[h].astype(float) - hex_union[c].astype(float)

    # CCA: canonical correlation between 象 diffs and embedding diffs
    # Use PCA to reduce dimensionality first
    from sklearn.decomposition import PCA
    from sklearn.cross_decomposition import CCA

    # Reduce embedding diffs to manageable dimensionality
    pca_emb = PCA(n_components=min(20, n_pairs - 1))
    emb_diffs_pca = pca_emb.fit_transform(emb_diffs)
    print(f"  Embedding diffs PCA: {emb_diffs_pca.shape}, "
          f"var explained: {pca_emb.explained_variance_ratio_.sum():.3f}")

    # For concat: reduce too
    n_comp_c = min(15, n_pairs - 1, hex_concat.shape[1])
    pca_xc = PCA(n_components=n_comp_c)
    xiang_diffs_c_pca = pca_xc.fit_transform(xiang_diffs_c)
    print(f"  Concat 象 diffs PCA: {xiang_diffs_c_pca.shape}, "
          f"var explained: {pca_xc.explained_variance_ratio_.sum():.3f}")

    # For union
    n_comp_u = min(15, n_pairs - 1, hex_union.shape[1])
    pca_xu = PCA(n_components=n_comp_u)
    xiang_diffs_u_pca = pca_xu.fit_transform(xiang_diffs_u)
    print(f"  Union 象 diffs PCA: {xiang_diffs_u_pca.shape}, "
          f"var explained: {pca_xu.explained_variance_ratio_.sum():.3f}")

    # CCA
    n_cca = min(5, n_comp_c, 20)
    try:
        cca_c = CCA(n_components=n_cca)
        cca_c.fit(xiang_diffs_c_pca[:, :n_cca], emb_diffs_pca[:, :n_cca])
        Xc, Yc = cca_c.transform(xiang_diffs_c_pca[:, :n_cca], emb_diffs_pca[:, :n_cca])
        cca_corrs_c = [np.corrcoef(Xc[:, i], Yc[:, i])[0, 1] for i in range(n_cca)]
        print(f"\n  CCA (concat 象 → embedding), {n_cca} components:")
        for i, r in enumerate(cca_corrs_c):
            print(f"    CC{i+1}: r={r:.4f}")
    except Exception as e:
        print(f"  CCA concat failed: {e}")
        cca_corrs_c = []

    try:
        cca_u = CCA(n_components=n_cca)
        cca_u.fit(xiang_diffs_u_pca[:, :n_cca], emb_diffs_pca[:, :n_cca])
        Xu, Yu = cca_u.transform(xiang_diffs_u_pca[:, :n_cca], emb_diffs_pca[:, :n_cca])
        cca_corrs_u = [np.corrcoef(Xu[:, i], Yu[:, i])[0, 1] for i in range(n_cca)]
        print(f"\n  CCA (union 象 → embedding), {n_cca} components:")
        for i, r in enumerate(cca_corrs_u):
            print(f"    CC{i+1}: r={r:.4f}")
    except Exception as e:
        print(f"  CCA union failed: {e}")
        cca_corrs_u = []

    # ─── 3c: Procrustes test ───
    print(f"\n  --- 3c: Procrustes Analysis ---")
    from scipy.spatial import procrustes

    # Normalize to same dim for Procrustes
    proc_dim = min(n_comp_c, 20)
    try:
        _, _, disparity_c = procrustes(emb_diffs_pca[:, :proc_dim],
                                        xiang_diffs_c_pca[:, :proc_dim])
        print(f"  Concat Procrustes disparity: {disparity_c:.4f}")
    except Exception as e:
        disparity_c = None
        print(f"  Concat Procrustes failed: {e}")

    proc_dim_u = min(n_comp_u, 20)
    try:
        _, _, disparity_u = procrustes(emb_diffs_pca[:, :proc_dim_u],
                                        xiang_diffs_u_pca[:, :proc_dim_u])
        print(f"  Union Procrustes disparity: {disparity_u:.4f}")
    except Exception as e:
        disparity_u = None
        print(f"  Union Procrustes failed: {e}")

    # Permutation null for Procrustes
    if disparity_c is not None:
        count_proc = 0
        for _ in range(n_perm):
            perm = np.random.permutation(n_pairs)
            try:
                _, _, d_perm = procrustes(emb_diffs_pca[perm, :proc_dim],
                                           xiang_diffs_c_pca[:, :proc_dim])
                if d_perm <= disparity_c:
                    count_proc += 1
            except:
                pass
        p_proc_c = (count_proc + 1) / (n_perm + 1)
        print(f"  Concat Procrustes permutation p={p_proc_c:.4f}")
    else:
        p_proc_c = None

    if disparity_u is not None:
        count_proc_u = 0
        for _ in range(n_perm):
            perm = np.random.permutation(n_pairs)
            try:
                _, _, d_perm = procrustes(emb_diffs_pca[perm, :proc_dim_u],
                                           xiang_diffs_u_pca[:, :proc_dim_u])
                if d_perm <= disparity_u:
                    count_proc_u += 1
            except:
                pass
        p_proc_u = (count_proc_u + 1) / (n_perm + 1)
        print(f"  Union Procrustes permutation p={p_proc_u:.4f}")
    else:
        p_proc_u = None

    # ─── 3d: Simple category-level correlation ───
    print(f"\n  --- 3d: Per-Category Embedding Prediction ---")

    # For each 象 category: does distance within that category
    # predict embedding distance?
    cat_results = {}
    flat_assocs_data = json.load(open(Q3 / 'shuogua_associations.json'))
    assoc_list = flat_assocs_data['associations']
    cat_starts = {}
    cat_ends = {}
    idx = 0
    for cat in XIANG_CATEGORIES:
        cat_starts[cat] = idx
        n_in_cat = sum(1 for a in assoc_list if a['category'] == cat)
        cat_ends[cat] = idx + n_in_cat
        idx += n_in_cat

    for cat in XIANG_CATEGORIES:
        cs, ce = cat_starts[cat], cat_ends[cat]
        if ce - cs == 0:
            continue
        # Category-specific distance (concat: upper + lower portions)
        cat_concat = np.hstack([hex_concat[:, cs:ce],
                                 hex_concat[:, hex_concat.shape[1]//2 + cs:
                                            hex_concat.shape[1]//2 + ce]])
        cat_dist = pdist(cat_concat, metric='hamming')

        r_cat, p_cat = pearsonr(emb_dist, cat_dist)
        rs_cat, ps_cat = spearmanr(emb_dist, cat_dist)
        cat_results[cat] = {'pearson_r': r_cat, 'pearson_p': p_cat,
                             'spearman_r': rs_cat, 'spearman_p': ps_cat,
                             'n_assocs': ce - cs}
        sig = '*' if p_cat < 0.05 else ''
        print(f"    {cat:<12} (n={ce-cs:>2}): Pearson r={r_cat:>+.4f} p={p_cat:.4g} "
              f"Spearman ρ={rs_cat:>+.4f} p={ps_cat:.4g} {sig}")

    return {
        'mantel': {
            'concat': {'r': r_c, 'p': p_c, 'rs': rs_c, 'ps': ps_c, 'p_perm': p_perm_c},
            'union': {'r': r_u, 'p': p_u, 'rs': rs_u, 'ps': ps_u, 'p_perm': p_perm_u},
        },
        'cca': {'concat': cca_corrs_c, 'union': cca_corrs_u},
        'procrustes': {
            'concat': {'disparity': disparity_c, 'p_perm': p_proc_c},
            'union': {'disparity': disparity_u, 'p_perm': p_proc_u},
        },
        'per_category': cat_results,
    }


# ═══════════════════════════════════════════════════════
# Phase 4: Category Contribution Analysis
# ═══════════════════════════════════════════════════════

def phase4_category_analysis(hex_concat, hex_union, comp_pairs, atlas, results):
    """If Mantel is significant, determine which categories drive it."""
    print("\n" + "=" * 70)
    print("PHASE 4: Category Contribution Analysis")
    print("=" * 70)

    mantel_r = results['mantel']['concat']['r']
    mantel_p = results['mantel']['concat']['p_perm']

    if mantel_p > 0.10:
        print(f"\n  Mantel p={mantel_p:.4f} > 0.10 — no significant correlation to decompose.")
        print(f"  The 說卦傳 象 space does NOT capture the embedding geometry.")
        print(f"  The embeddings encode semantic structure beyond traditional 象 associations.")
        return

    print(f"\n  Mantel r={mantel_r:.4f}, p_perm={mantel_p:.4f} — significant. Decomposing...")

    # Leave-one-category-out analysis
    emb_data = np.load(str(EMBEDDINGS))
    yaoci_emb = emb_data['yaoci']

    kw_to_hv = {}
    for hv in range(N_HEX):
        kw = atlas[str(hv)]['kw_number']
        kw_to_hv[kw] = hv

    hex_centroids = np.zeros((N_HEX, yaoci_emb.shape[1]))
    for kw in range(1, N_HEX + 1):
        hv = kw_to_hv[kw]
        start = (kw - 1) * N_LINES
        hex_centroids[hv] = yaoci_emb[start:start + N_LINES].mean(axis=0)

    from scipy.spatial.distance import pdist
    emb_dist = pdist(hex_centroids, metric='cosine')

    flat_assocs_data = json.load(open(Q3 / 'shuogua_associations.json'))
    assoc_list = flat_assocs_data['associations']

    print(f"\n  Leave-one-category-out Mantel test:")
    for cat in XIANG_CATEGORIES:
        # Remove this category's columns
        keep_cols = [i for i, a in enumerate(assoc_list) if a['category'] != cat]
        N_half = len(assoc_list)
        keep_concat = keep_cols + [i + N_half for i in keep_cols]
        reduced = hex_concat[:, keep_concat]
        dist_reduced = pdist(reduced, metric='hamming')
        r_red = np.corrcoef(emb_dist, dist_reduced)[0, 1]
        delta = mantel_r - r_red
        print(f"    Without {cat:<12}: r={r_red:.4f} (Δ={delta:+.4f})")


# ═══════════════════════════════════════════════════════
# Results Writer
# ═══════════════════════════════════════════════════════

def write_results(tri_matrix, all_assocs, results, comp_pairs, hex_concat, hex_union):
    """Write xiang_space_results.md."""
    lines = []
    w = lines.append

    w("# Q3 Phase 3: 說卦傳 象 Space vs Complement Embedding Geometry\n")

    w("## Phase 1: Association Matrix\n")
    N = tri_matrix.shape[1]
    w(f"- **Total unique associations:** {N}")
    w(f"- **Matrix:** 8 trigrams × {N} associations\n")

    w("| Category | N associations | Example items |")
    w("|----------|---------------|---------------|")
    for cat in XIANG_CATEGORIES:
        items = all_assocs[cat]
        examples = ', '.join(items[:5])
        if len(items) > 5:
            examples += '...'
        w(f"| {cat} | {len(items)} | {examples} |")

    w(f"\n| Trigram | Total associations |")
    w(f"|---------|-------------------|")
    for ti in range(8):
        w(f"| {TRI_NAMES[ti]} | {tri_matrix[ti].sum()} |")

    w("\n## Phase 2: Hexagram 象 Profiles\n")
    unique_c = len(set(tuple(row) for row in hex_concat))
    unique_u = len(set(tuple(row) for row in hex_union))
    w(f"- Concatenation: 64 × {hex_concat.shape[1]} ({unique_c} distinct profiles)")
    w(f"- Union: 64 × {hex_union.shape[1]} ({unique_u} distinct profiles)")

    w("\n## Phase 3: Correlation Tests\n")

    w("### 3a: Mantel Test (full distance matrix)\n")
    m = results['mantel']
    w("| Space | Pearson r | p (parametric) | p (permutation) |")
    w("|-------|-----------|---------------|-----------------|")
    w(f"| Concat | {m['concat']['r']:.4f} | {m['concat']['p']:.4g} | {m['concat']['p_perm']:.4f} |")
    w(f"| Union | {m['union']['r']:.4f} | {m['union']['p']:.4g} | {m['union']['p_perm']:.4f} |")

    w("\n### 3b: CCA (complement difference vectors)\n")
    if results['cca']['concat']:
        w("| CC | Concat r | Union r |")
        w("|----|----------|---------|")
        for i in range(len(results['cca']['concat'])):
            rc = results['cca']['concat'][i] if i < len(results['cca']['concat']) else '-'
            ru = results['cca']['union'][i] if i < len(results['cca']['union']) else '-'
            w(f"| CC{i+1} | {rc:.4f} | {ru:.4f} |")

    w("\n### 3c: Procrustes Analysis\n")
    p = results['procrustes']
    w(f"- Concat: disparity={p['concat']['disparity']:.4f}, p_perm={p['concat']['p_perm']:.4f}")
    w(f"- Union: disparity={p['union']['disparity']:.4f}, p_perm={p['union']['p_perm']:.4f}")

    w("\n### 3d: Per-Category Prediction\n")
    w("| Category | N | Pearson r | p | Spearman ρ | p |")
    w("|----------|---|-----------|---|------------|---|")
    for cat in XIANG_CATEGORIES:
        if cat in results['per_category']:
            cr = results['per_category'][cat]
            sig = '**' if cr['pearson_p'] < 0.01 else ('*' if cr['pearson_p'] < 0.05 else '')
            w(f"| {cat} | {cr['n_assocs']} | {cr['pearson_r']:.4f} | "
              f"{cr['pearson_p']:.4g} | {cr['spearman_r']:.4f} | {cr['spearman_p']:.4g} | {sig}")

    w("\n## Interpretation\n")
    mc = m['concat']
    mu = m['union']
    if mc['p_perm'] < 0.05 or mu['p_perm'] < 0.05:
        w("**The 說卦傳 象 space DOES predict embedding geometry** (Mantel p < 0.05).\n")
        w("The traditional association system captures structure that modern embeddings also detect. "
          "The practitioners' navigation instrument aligns with the text's semantic geometry.")
    else:
        w("**The 說卦傳 象 space does NOT predict embedding geometry** (Mantel p > 0.05).\n")
        w("The embeddings capture semantic structure BEYOND what the traditional 象 system encodes. "
          "The 18-dimensional complement space (R133) contains information that the 說卦傳 "
          "categorization cannot access — a richer or different semantic structure.")
        w("\nThis is consistent with R135 (complement opposition lexically invisible) and extends it: "
          "the opposition is not just invisible at the vocabulary level, but also invisible at the "
          "level of traditional 象 categories. Whatever the embeddings see operates below both layers.")

    with open(Q3 / 'xiang_space_results.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\n  Results written to {Q3 / 'xiang_space_results.md'}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    with open(ATLAS) as f:
        atlas = json.load(f)

    # Phase 1
    tri_matrix, flat_assocs, all_assocs = phase1_build_associations()

    # Phase 2
    hex_concat, hex_union, comp_pairs = phase2_hex_profiles(tri_matrix, atlas)

    # Phase 3
    results = phase3_test_correlation(hex_concat, hex_union, comp_pairs, atlas)

    # Phase 4
    phase4_category_analysis(hex_concat, hex_union, comp_pairs, atlas, results)

    # Write results
    write_results(tri_matrix, all_assocs, results, comp_pairs, hex_concat, hex_union)

    print("\n" + "=" * 70)
    print("DONE — Q3 Phase 3 complete.")
    print("=" * 70)


if __name__ == '__main__':
    main()
