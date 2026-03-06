"""
Embed Tuan, Xugua, and Guaci texts via BGE-M3.
Compute semantic similarity matrices.
Test: does semantic distance correlate with algebraic distance, basin membership, KW adjacency?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

import json
import requests
import numpy as np
from collections import Counter, defaultdict
from scipy import stats
from scipy.spatial.distance import cosine as cosine_dist

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6, fmt6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
)

# ══════════════════════════════════════════════════════════════════════════════
# 0. LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════

TEXTS_DIR = '/home/quasar/nous/memories/iching/texts'
EMBED_URL = 'http://localhost:8103/embed'

kw_hex = []
kw_names = []
kw_number = []  # KW number (1-64)
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])
    kw_number.append(KING_WEN[i][0])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1  # Kun
    elif b2 == 1 and b3 == 1: return 1  # Qian
    else: return 0  # KanLi

def get_inner(h): return (h >> 1) & 0xF
def get_outer(h): return (h & 1) | (((h >> 5) & 1) << 1)

basins = [get_basin(kw_hex[i]) for i in range(64)]

# Load texts — indexed by KW number (1-64)
with open(f'{TEXTS_DIR}/tuan.json') as f:
    tuan_data = json.load(f)
with open(f'{TEXTS_DIR}/xugua.json') as f:
    xugua_data = json.load(f)
with open(f'{TEXTS_DIR}/guaci.json') as f:
    guaci_data = json.load(f)

# Build lookup by KW number
tuan_by_num = {e['number']: e['text'] for e in tuan_data['entries']}
xugua_by_num = {e['number']: e['text'] for e in xugua_data['entries']}
guaci_by_num = {e['number']: e['text'] for e in guaci_data['entries']}

# Order texts by KW sequence position (0-63)
tuan_texts = [tuan_by_num[kw_number[i]] for i in range(64)]
xugua_texts = [xugua_by_num[kw_number[i]] for i in range(64)]
guaci_texts = [guaci_by_num[kw_number[i]] for i in range(64)]

# ══════════════════════════════════════════════════════════════════════════════
# 1. EMBED ALL TEXTS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. EMBEDDING TEXTS")
print("=" * 70)

def embed(texts):
    resp = requests.post(EMBED_URL, json={"texts": texts})
    resp.raise_for_status()
    data = resp.json()
    return np.array(data['embeddings'])

print(f"\n  Embedding Tuan (64 texts)...")
tuan_emb = embed(tuan_texts)
print(f"    Shape: {tuan_emb.shape}")

print(f"  Embedding Xugua (64 texts)...")
xugua_emb = embed(xugua_texts)
print(f"    Shape: {xugua_emb.shape}")

print(f"  Embedding Guaci (64 texts)...")
guaci_emb = embed(guaci_texts)
print(f"    Shape: {guaci_emb.shape}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. SEMANTIC SIMILARITY MATRICES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. SEMANTIC SIMILARITY MATRICES")
print("=" * 70)

def sim_matrix(emb):
    """Cosine similarity matrix (embeddings already normalized)."""
    return emb @ emb.T

tuan_sim = sim_matrix(tuan_emb)
xugua_sim = sim_matrix(xugua_emb)
guaci_sim = sim_matrix(guaci_emb)

# Basic stats
for name, sim in [("Tuan", tuan_sim), ("Xugua", xugua_sim), ("Guaci", guaci_sim)]:
    # Upper triangle only (exclude diagonal)
    upper = sim[np.triu_indices(64, k=1)]
    print(f"\n  {name} similarity: mean={np.mean(upper):.4f}  std={np.std(upper):.4f}  "
          f"min={np.min(upper):.4f}  max={np.max(upper):.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. ALGEBRAIC DISTANCE MATRICES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. ALGEBRAIC DISTANCE MATRICES")
print("=" * 70)

# Hamming distance
hamming_mat = np.zeros((64, 64))
hu_hamming_mat = np.zeros((64, 64))
basin_same_mat = np.zeros((64, 64))
inner_hamming_mat = np.zeros((64, 64))

for i in range(64):
    for j in range(64):
        hamming_mat[i, j] = hamming6(kw_hex[i], kw_hex[j])
        hu_hamming_mat[i, j] = hamming6(hugua(kw_hex[i]), hugua(kw_hex[j]))
        basin_same_mat[i, j] = 1 if basins[i] == basins[j] else 0
        inner_hamming_mat[i, j] = bin(get_inner(kw_hex[i]) ^ get_inner(kw_hex[j])).count('1')

# KW adjacency (1 if consecutive)
kw_adj = np.zeros((64, 64))
for i in range(63):
    kw_adj[i, i+1] = 1
    kw_adj[i+1, i] = 1

print(f"  Matrices computed: hamming, hu_hamming, basin_same, inner_hamming, kw_adj")

# ══════════════════════════════════════════════════════════════════════════════
# 4. CORRELATIONS: SEMANTIC vs ALGEBRAIC
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. CORRELATIONS: SEMANTIC SIMILARITY vs ALGEBRAIC DISTANCE")
print("=" * 70)

upper_idx = np.triu_indices(64, k=1)

for sem_name, sem_sim in [("Tuan", tuan_sim), ("Xugua", xugua_sim), ("Guaci", guaci_sim)]:
    print(f"\n  {sem_name} semantic similarity vs:")
    sem_upper = sem_sim[upper_idx]
    
    for alg_name, alg_mat, invert in [
        ("Hamming distance", hamming_mat, True),
        ("互 distance", hu_hamming_mat, True),
        ("Inner distance", inner_hamming_mat, True),
        ("Basin same", basin_same_mat, False),
        ("KW adjacent", kw_adj, False),
    ]:
        alg_upper = alg_mat[upper_idx]
        r, p = stats.pearsonr(sem_upper, alg_upper)
        direction = "closer hex → more similar text" if (invert and r < 0) or (not invert and r > 0) else ""
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"    {alg_name:20s}: r={r:+.4f}  p={p:.2e}  {sig} {direction}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. BASIN CLUSTERING IN SEMANTIC SPACE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. BASIN CLUSTERING IN SEMANTIC SPACE")
print("=" * 70)

basin_labels = {-1: 'Kun', 0: 'KanLi', 1: 'Qian'}

for sem_name, sem_sim in [("Tuan", tuan_sim), ("Xugua", xugua_sim), ("Guaci", guaci_sim)]:
    print(f"\n  {sem_name} — mean similarity by basin pair:")
    
    # Within-basin vs between-basin similarity
    within = []
    between = []
    by_pair = defaultdict(list)
    
    for i in range(64):
        for j in range(i+1, 64):
            bi, bj = basins[i], basins[j]
            s = sem_sim[i, j]
            pair_key = (min(bi, bj), max(bi, bj))
            by_pair[(basin_labels[bi], basin_labels[bj])].append(s)
            
            if bi == bj:
                within.append(s)
            else:
                between.append(s)
    
    print(f"    Within-basin:  mean={np.mean(within):.4f}  (n={len(within)})")
    print(f"    Between-basin: mean={np.mean(between):.4f}  (n={len(between)})")
    
    t, p = stats.ttest_ind(within, between)
    print(f"    t-test: t={t:.3f}  p={p:.2e}")
    
    # By specific basin pairs
    for (b1, b2) in sorted(set((basin_labels[basins[i]], basin_labels[basins[j]]) 
                               for i in range(64) for j in range(i+1, 64))):
        vals = by_pair[(b1, b2)] + by_pair.get((b2, b1), [])
        if vals:
            print(f"    {b1:6s}-{b2:6s}: mean={np.mean(vals):.4f}  n={len(vals)}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. KW ADJACENCY: ARE CONSECUTIVE HEXAGRAMS SEMANTICALLY CLOSER?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. KW ADJACENCY — CONSECUTIVE HEXAGRAMS SEMANTIC SIMILARITY")
print("=" * 70)

for sem_name, sem_sim in [("Tuan", tuan_sim), ("Xugua", xugua_sim), ("Guaci", guaci_sim)]:
    # Consecutive similarity
    consec = [sem_sim[i, i+1] for i in range(63)]
    # Non-consecutive
    non_consec = [sem_sim[i, j] for i in range(64) for j in range(i+2, 64)]
    
    # Intra-pair vs inter-pair
    intra = [sem_sim[2*k, 2*k+1] for k in range(32)]
    inter = [sem_sim[2*k+1, 2*(k+1)] for k in range(31)]
    
    print(f"\n  {sem_name}:")
    print(f"    Consecutive:     mean={np.mean(consec):.4f}")
    print(f"    Non-consecutive: mean={np.mean(non_consec):.4f}")
    t, p = stats.ttest_ind(consec, non_consec)
    print(f"    t-test: t={t:.3f}  p={p:.2e}")
    
    print(f"    Intra-pair:      mean={np.mean(intra):.4f}")
    print(f"    Inter-pair:      mean={np.mean(inter):.4f}")
    t2, p2 = stats.ttest_ind(intra, inter)
    print(f"    t-test intra vs inter: t={t2:.3f}  p={p2:.2e}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. XUGUA TRANSITION TYPES AND BRIDGE PROPERTIES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. XUGUA SEMANTIC SIMILARITY AT BRIDGES vs ALGEBRAIC PROPERTIES")
print("=" * 70)

# For each consecutive pair, compare Xugua semantic sim to algebraic bridge properties
print(f"\n  Inter-pair bridges: Xugua sim vs algebraic properties")

bridge_xugua_sims = []
bridge_hex_dists = []
bridge_hu_dists = []
bridge_inner_dists = []
bridge_basin_same = []

for k in range(31):
    i = 2*k + 1  # pair end
    j = 2*(k+1)  # next pair start
    
    bridge_xugua_sims.append(xugua_sim[i, j])
    bridge_hex_dists.append(hamming6(kw_hex[i], kw_hex[j]))
    bridge_hu_dists.append(hamming6(hugua(kw_hex[i]), hugua(kw_hex[j])))
    bridge_inner_dists.append(bin(get_inner(kw_hex[i]) ^ get_inner(kw_hex[j])).count('1'))
    bridge_basin_same.append(1 if basins[i] == basins[j] else 0)

for alg_name, alg_vals in [
    ("Hex distance", bridge_hex_dists),
    ("互 distance", bridge_hu_dists),
    ("Inner distance", bridge_inner_dists),
    ("Basin same", bridge_basin_same),
]:
    r, p = stats.pearsonr(bridge_xugua_sims, alg_vals)
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"    Xugua sim vs {alg_name:20s}: r={r:+.4f}  p={p:.2e}  {sig}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. CANON COMPARISON: UC vs LC SEMANTIC COHERENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. CANON COMPARISON: UC vs LC SEMANTIC COHERENCE")
print("=" * 70)

uc_idx = list(range(30))  # positions 0-29 (hexagrams 1-30)
lc_idx = list(range(30, 64))  # positions 30-63 (hexagrams 31-64)

for sem_name, sem_sim in [("Tuan", tuan_sim), ("Xugua", xugua_sim), ("Guaci", guaci_sim)]:
    uc_within = [sem_sim[i, j] for i in uc_idx for j in uc_idx if i < j]
    lc_within = [sem_sim[i, j] for i in lc_idx for j in lc_idx if i < j]
    cross = [sem_sim[i, j] for i in uc_idx for j in lc_idx]
    
    print(f"\n  {sem_name}:")
    print(f"    UC within:  mean={np.mean(uc_within):.4f}  (n={len(uc_within)})")
    print(f"    LC within:  mean={np.mean(lc_within):.4f}  (n={len(lc_within)})")
    print(f"    Cross:      mean={np.mean(cross):.4f}  (n={len(cross)})")

# ══════════════════════════════════════════════════════════════════════════════
# 9. MOST/LEAST SIMILAR PAIRS BY EACH TEXT
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. MOST SIMILAR PAIRS (non-adjacent, non-self)")
print("=" * 70)

for sem_name, sem_sim in [("Tuan", tuan_sim), ("Guaci", guaci_sim)]:
    print(f"\n  {sem_name} — top 10 most similar pairs:")
    pairs = []
    for i in range(64):
        for j in range(i+1, 64):
            pairs.append((sem_sim[i, j], i, j))
    pairs.sort(reverse=True)
    
    for rank, (s, i, j) in enumerate(pairs[:10]):
        bi, bj = basin_labels[basins[i]], basin_labels[basins[j]]
        hd = hamming6(kw_hex[i], kw_hex[j])
        kw_dist = abs(i - j)
        print(f"    {rank+1:2d}. {kw_names[i]:8s}({bi[0]}) - {kw_names[j]:8s}({bj[0]})  "
              f"sim={s:.4f}  hex_d={hd}  kw_dist={kw_dist}")

# ══════════════════════════════════════════════════════════════════════════════
# 10. PERMUTATION TEST: IS SEMANTIC-ALGEBRAIC CORRELATION SIGNIFICANT?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. PERMUTATION TEST: SEMANTIC vs HAMMING CORRELATION")
print("=" * 70)

import random
random.seed(42)

N_PERM = 10000

# Test: is the correlation between Tuan similarity and Hamming distance
# more negative than expected by chance?
tuan_upper = tuan_sim[upper_idx]
hamming_upper = hamming_mat[upper_idx]

real_r, _ = stats.pearsonr(tuan_upper, hamming_upper)

perm_rs = []
idx = list(range(64))
for _ in range(N_PERM):
    random.shuffle(idx)
    perm_sim = tuan_sim[np.ix_(idx, idx)]
    perm_upper = perm_sim[upper_idx]
    r, _ = stats.pearsonr(perm_upper, hamming_upper)
    perm_rs.append(r)

perm_p = np.mean([r <= real_r for r in perm_rs])
print(f"\n  Tuan sim vs Hamming distance:")
print(f"    Real r = {real_r:.4f}")
print(f"    Permutation p = {perm_p:.4f} ({N_PERM} permutations)")
print(f"    {'SIGNIFICANT' if perm_p < 0.05 else 'NOT SIGNIFICANT'}")

# Same for basin
basin_upper = basin_same_mat[upper_idx]
real_r_basin, _ = stats.pearsonr(tuan_upper, basin_upper)

perm_rs_basin = []
for _ in range(N_PERM):
    random.shuffle(idx)
    perm_sim = tuan_sim[np.ix_(idx, idx)]
    perm_upper = perm_sim[upper_idx]
    r, _ = stats.pearsonr(perm_upper, basin_upper)
    perm_rs_basin.append(r)

perm_p_basin = np.mean([r >= real_r_basin for r in perm_rs_basin])
print(f"\n  Tuan sim vs Basin same:")
print(f"    Real r = {real_r_basin:.4f}")
print(f"    Permutation p = {perm_p_basin:.4f}")
print(f"    {'SIGNIFICANT' if perm_p_basin < 0.05 else 'NOT SIGNIFICANT'}")

# ══════════════════════════════════════════════════════════════════════════════
# 11. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("11. SUMMARY")
print("=" * 70)
