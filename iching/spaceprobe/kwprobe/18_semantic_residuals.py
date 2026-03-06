"""
Test whether Tuan's Hamming correlation survives after removing trigram/structural keyword effects.

Two approaches:
  A. Regression residuals: predict similarity from trigram-word overlap, test if residual correlates with Hamming.
  B. Masked embedding: strip trigram names + structural keywords from texts, re-embed, retest.

If residual Hamming correlation persists, the Tuan captures algebraic structure beyond
explicit trigram references.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

import json
import re
import requests
import numpy as np
from scipy import stats
from scipy.spatial.distance import cosine as cosine_dist

from sequence import KING_WEN
from cycle_algebra import hugua, hamming6

# ══════════════════════════════════════════════════════════════════════════════
# 0. SETUP
# ══════════════════════════════════════════════════════════════════════════════

TEXTS_DIR = '/home/quasar/nous/memories/iching/texts'
EMBED_URL = 'http://localhost:8103/embed'

# Trigram names (traditional)
TRIGRAM_NAMES_ZH = ['乾', '坤', '坎', '離', '震', '艮', '巽', '兌']

# Structural keywords that encode algebraic information
STRUCTURAL_KEYWORDS = ['剛', '柔', '中', '正', '上', '下', '內', '外', '陰', '陽', '天', '地', '動', '止']

ALL_MARKERS = TRIGRAM_NAMES_ZH + STRUCTURAL_KEYWORDS

# Load KW sequence
kw_hex = []
kw_names = []
kw_number = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])
    kw_number.append(KING_WEN[i][0])

def get_basin(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    if b2 == 1 and b3 == 1: return 1
    return 0

basins = [get_basin(kw_hex[i]) for i in range(64)]

# Load texts
with open(f'{TEXTS_DIR}/tuan.json') as f:
    tuan_data = json.load(f)
with open(f'{TEXTS_DIR}/xugua.json') as f:
    xugua_data = json.load(f)
with open(f'{TEXTS_DIR}/guaci.json') as f:
    guaci_data = json.load(f)

tuan_by_num = {e['number']: e['text'] for e in tuan_data['entries']}
xugua_by_num = {e['number']: e['text'] for e in xugua_data['entries']}
guaci_by_num = {e['number']: e['text'] for e in guaci_data['entries']}

tuan_texts = [tuan_by_num[kw_number[i]] for i in range(64)]
xugua_texts = [xugua_by_num[kw_number[i]] for i in range(64)]
guaci_texts = [guaci_by_num[kw_number[i]] for i in range(64)]

# Distance matrices
hamming_mat = np.zeros((64, 64))
basin_same_mat = np.zeros((64, 64))
kw_adj = np.zeros((64, 64))
for i in range(64):
    for j in range(64):
        hamming_mat[i, j] = hamming6(kw_hex[i], kw_hex[j])
        basin_same_mat[i, j] = 1 if basins[i] == basins[j] else 0
for i in range(63):
    kw_adj[i, i+1] = 1
    kw_adj[i+1, i] = 1

upper_idx = np.triu_indices(64, k=1)

def embed(texts):
    resp = requests.post(EMBED_URL, json={"texts": texts})
    resp.raise_for_status()
    return np.array(resp.json()['embeddings'])

def sim_matrix(emb):
    return emb @ emb.T

def report_correlations(name, sem_sim):
    """Report correlations of a similarity matrix against algebraic features."""
    sem_upper = sem_sim[upper_idx]
    results = {}
    for alg_name, alg_mat in [("Hamming", hamming_mat), ("Basin same", basin_same_mat), ("KW adj", kw_adj)]:
        alg_upper = alg_mat[upper_idx]
        r, p = stats.pearsonr(sem_upper, alg_upper)
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        print(f"    {name} vs {alg_name:12s}: r={r:+.4f}  p={p:.2e}  {sig}")
        results[alg_name] = (r, p)
    return results

# ══════════════════════════════════════════════════════════════════════════════
# 1. TRIGRAM FEATURE VECTORS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. TRIGRAM + STRUCTURAL KEYWORD FEATURE VECTORS")
print("=" * 70)

def count_markers(text):
    """Count occurrences of each marker in text."""
    return np.array([text.count(m) for m in ALL_MARKERS], dtype=float)

def build_feature_matrix(texts):
    return np.array([count_markers(t) for t in texts])

tuan_feat = build_feature_matrix(tuan_texts)
xugua_feat = build_feature_matrix(xugua_texts)
guaci_feat = build_feature_matrix(guaci_texts)

for name, feat in [("Tuan", tuan_feat), ("Xugua", xugua_feat), ("Guaci", guaci_feat)]:
    nonzero = np.count_nonzero(feat, axis=0)
    total = feat.sum()
    print(f"\n  {name}: {int(total)} total marker occurrences across 64 texts")
    for k, marker in enumerate(ALL_MARKERS):
        if feat[:, k].sum() > 0:
            print(f"    {marker}: {int(feat[:, k].sum())} occurrences in {nonzero[k]} texts")

# ══════════════════════════════════════════════════════════════════════════════
# 2. APPROACH A: REGRESSION RESIDUALS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. APPROACH A: REGRESSION RESIDUALS")
print("=" * 70)
print("\n  Predict semantic similarity from trigram-word cosine overlap.")
print("  Test if RESIDUAL still correlates with Hamming distance.")

def feature_cosine_sim(feat):
    """Cosine similarity from feature vectors. Handle zero vectors."""
    norms = np.linalg.norm(feat, axis=1, keepdims=True)
    # Replace zero norms with 1 to avoid division by zero
    norms = np.where(norms == 0, 1, norms)
    normed = feat / norms
    return normed @ normed.T

def residual_analysis(name, sem_sim, feat):
    """Regress out feature-predicted similarity, test residual."""
    feat_sim = feature_cosine_sim(feat)

    sem_upper = sem_sim[upper_idx]
    feat_upper = feat_sim[upper_idx]
    hamming_upper = hamming_mat[upper_idx]

    # How much does feature overlap predict semantic similarity?
    r_feat_sem, p_feat_sem = stats.pearsonr(feat_upper, sem_upper)
    print(f"\n  {name}:")
    print(f"    Feature overlap → semantic sim: r={r_feat_sem:+.4f}  p={p_feat_sem:.2e}")

    # How much does feature overlap predict Hamming?
    r_feat_ham, p_feat_ham = stats.pearsonr(feat_upper, hamming_upper)
    print(f"    Feature overlap → Hamming dist:  r={r_feat_ham:+.4f}  p={p_feat_ham:.2e}")

    # Original correlation
    r_orig, p_orig = stats.pearsonr(sem_upper, hamming_upper)
    print(f"    Original sem → Hamming:          r={r_orig:+.4f}  p={p_orig:.2e}")

    # Residualize: regress semantic sim on feature sim, take residuals
    slope, intercept = np.polyfit(feat_upper, sem_upper, 1)
    predicted = slope * feat_upper + intercept
    residual = sem_upper - predicted

    # Residual vs Hamming
    r_resid, p_resid = stats.pearsonr(residual, hamming_upper)
    print(f"    RESIDUAL sem → Hamming:          r={r_resid:+.4f}  p={p_resid:.2e}")

    # Variance explained
    var_explained = r_feat_sem**2 * 100
    print(f"    Variance explained by features:   {var_explained:.1f}%")

    reduction = (1 - abs(r_resid)/abs(r_orig)) * 100 if r_orig != 0 else 0
    print(f"    Correlation reduction:            {reduction:.1f}%")

    # Also test residual vs KW adjacency and basin
    kw_upper = kw_adj[upper_idx]
    basin_upper = basin_same_mat[upper_idx]
    r_kw, p_kw = stats.pearsonr(residual, kw_upper)
    r_bas, p_bas = stats.pearsonr(residual, basin_upper)
    print(f"    RESIDUAL sem → KW adjacency:     r={r_kw:+.4f}  p={p_kw:.2e}")
    print(f"    RESIDUAL sem → Basin same:        r={r_bas:+.4f}  p={p_bas:.2e}")

    return r_orig, r_resid, var_explained

print("\n  --- Tuan ---")
tuan_orig, tuan_resid, tuan_var = residual_analysis("Tuan", sim_matrix(embed(tuan_texts)), tuan_feat)

print("\n  --- Xugua ---")
xugua_orig, xugua_resid, xugua_var = residual_analysis("Xugua", sim_matrix(embed(xugua_texts)), xugua_feat)

print("\n  --- Guaci ---")
guaci_orig, guaci_resid, guaci_var = residual_analysis("Guaci", sim_matrix(embed(guaci_texts)), guaci_feat)

# ══════════════════════════════════════════════════════════════════════════════
# 3. APPROACH B: MASKED EMBEDDING
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. APPROACH B: MASKED EMBEDDING (remove markers before embedding)")
print("=" * 70)

def mask_text(text, markers):
    """Remove all marker characters from text."""
    result = text
    for m in markers:
        result = result.replace(m, '')
    return result

for text_name, texts in [("Tuan", tuan_texts), ("Xugua", xugua_texts), ("Guaci", guaci_texts)]:
    masked = [mask_text(t, ALL_MARKERS) for t in texts]

    # Show masking extent
    orig_chars = sum(len(t) for t in texts)
    masked_chars = sum(len(t) for t in masked)
    removed_pct = (1 - masked_chars / orig_chars) * 100

    print(f"\n  {text_name}: removed {removed_pct:.1f}% of characters ({orig_chars - masked_chars}/{orig_chars})")

    # Check for empty texts after masking
    empty = sum(1 for t in masked if len(t.strip()) == 0)
    if empty:
        print(f"    WARNING: {empty} texts are empty after masking!")
        # Replace empty texts with a placeholder
        masked = [t if t.strip() else '。' for t in masked]

    # Embed masked texts
    masked_emb = embed(masked)
    masked_sim = sim_matrix(masked_emb)

    print(f"  Correlations (masked):")
    report_correlations(f"{text_name} masked", masked_sim)

    # Compare to original
    orig_emb = embed(texts)
    orig_sim = sim_matrix(orig_emb)

    orig_upper = orig_sim[upper_idx]
    masked_upper = masked_sim[upper_idx]
    r_orig_masked, _ = stats.pearsonr(orig_upper, masked_upper)
    print(f"    Original ↔ masked similarity correlation: r={r_orig_masked:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. DEEPER: PARTIAL REGRESSION (trigrams only vs structural only)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. DECOMPOSED: TRIGRAM NAMES ONLY vs STRUCTURAL KEYWORDS ONLY")
print("=" * 70)

n_trigram = len(TRIGRAM_NAMES_ZH)

def partial_residual(name, sem_sim, feat, feature_slice, slice_name):
    """Regress out only a subset of features."""
    partial_feat = feat[:, feature_slice]
    partial_sim = feature_cosine_sim(partial_feat)

    sem_upper = sem_sim[upper_idx]
    partial_upper = partial_sim[upper_idx]
    hamming_upper = hamming_mat[upper_idx]

    r_feat_sem, _ = stats.pearsonr(partial_upper, sem_upper)
    r_orig, _ = stats.pearsonr(sem_upper, hamming_upper)

    slope, intercept = np.polyfit(partial_upper, sem_upper, 1)
    residual = sem_upper - (slope * partial_upper + intercept)
    r_resid, p_resid = stats.pearsonr(residual, hamming_upper)

    print(f"    {name} regressing out {slice_name}:")
    print(f"      Feature → semantic: r={r_feat_sem:+.4f}")
    print(f"      Original → Hamming: r={r_orig:+.4f}")
    print(f"      Residual → Hamming: r={r_resid:+.4f}  p={p_resid:.2e}")

# Tuan only (where Hamming correlation exists)
tuan_sim_fresh = sim_matrix(embed(tuan_texts))
print(f"\n  Tuan decomposition:")
partial_residual("Tuan", tuan_sim_fresh, tuan_feat, slice(0, n_trigram), "trigram names only")
partial_residual("Tuan", tuan_sim_fresh, tuan_feat, slice(n_trigram, None), "structural kw only")
partial_residual("Tuan", tuan_sim_fresh, tuan_feat, slice(None), "all markers")

# ══════════════════════════════════════════════════════════════════════════════
# 5. PERMUTATION TEST ON RESIDUAL
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. PERMUTATION TEST: RESIDUAL TUAN vs HAMMING")
print("=" * 70)

import random
random.seed(42)

N_PERM = 10000

# Compute Tuan residual after removing all marker features
feat_sim = feature_cosine_sim(tuan_feat)
tuan_upper = tuan_sim_fresh[upper_idx]
feat_upper = feat_sim[upper_idx]
hamming_upper = hamming_mat[upper_idx]

slope, intercept = np.polyfit(feat_upper, tuan_upper, 1)
tuan_residual = tuan_upper - (slope * feat_upper + intercept)

real_r, _ = stats.pearsonr(tuan_residual, hamming_upper)

perm_rs = []
idx = list(range(64))
for _ in range(N_PERM):
    random.shuffle(idx)
    perm_sim = tuan_sim_fresh[np.ix_(idx, idx)]
    perm_upper = perm_sim[upper_idx]
    perm_residual = perm_upper - (slope * feat_upper + intercept)
    r, _ = stats.pearsonr(perm_residual, hamming_upper)
    perm_rs.append(r)

perm_p = np.mean([r <= real_r for r in perm_rs])
print(f"\n  Residual Tuan sim vs Hamming distance:")
print(f"    Real r = {real_r:+.4f}")
print(f"    Permutation p = {perm_p:.4f} ({N_PERM} permutations)")
print(f"    {'SIGNIFICANT — algebraic awareness survives trigram removal' if perm_p < 0.05 else 'NOT SIGNIFICANT — trigram references explain the correlation'}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. SUMMARY")
print("=" * 70)
print("""
  Question: Is Tuan's Hamming correlation just "texts mentioning same trigrams"?

  Two independent tests:
    A. Regression residuals: remove trigram-word overlap from semantic similarity
    B. Masked embedding: physically remove trigram names + structural keywords, re-embed

  If both show surviving Hamming correlation → deep algebraic awareness
  If both show eliminated correlation → surface trigram references only
  If mixed → partial explanation
""")
