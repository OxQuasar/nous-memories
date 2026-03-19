"""
D1: Semantic Laplacian and Walsh Spectrum Analysis
Analyzes yaoci thematic embeddings on the Q6 hypercube (hexagram transition graph).
"""

import numpy as np
from scipy import stats
import json
import sys

np.random.seed(42)

# ─── Config ───
N_PERM_WALSH = 1000
N_PERM_LAP = 1000
N_PERM_CORR = 10000
EMBED_DIM = 1024
N_HEX = 64
N_LINES = 6

# ─── Load Data ───
bge = np.load('memories/iching/reversal/Q1/embeddings_bge-m3.npz')['yaoci']  # 384×1024
e5  = np.load('memories/iching/reversal/Q1/embeddings_e5-large.npz')['yaoci']  # 384×1024

with open('memories/iching/atlas/atlas.json') as f:
    atlas = json.load(f)

# Aggregate yaoci to hexagram level: average 6 lines per hexagram
# Hexagrams indexed 0-63 in binary order, 6 lines each = 384 yaoci
def aggregate_to_hex(yaoci_emb):
    """Average 6 lines per hexagram. yaoci[h*6 + line] for hex h, line 0-5."""
    return yaoci_emb.reshape(N_HEX, N_LINES, -1).mean(axis=1)  # 64×1024

hex_bge = aggregate_to_hex(bge)
hex_e5  = aggregate_to_hex(e5)

# ─── Helpers ───
def popcount(x):
    """Count set bits."""
    c = 0
    while x:
        c += x & 1
        x >>= 1
    return c

def hamming_neighbors(h):
    """6 neighbors of h on Q6 hypercube (flip each bit)."""
    return [h ^ (1 << i) for i in range(N_LINES)]

def cosine(a, b):
    """Cosine similarity between vectors."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return np.dot(a, b) / (na * nb)

# ─── Walsh-Hadamard Matrix ───
W = np.zeros((N_HEX, N_HEX))
for a in range(N_HEX):
    for b in range(N_HEX):
        W[a, b] = (-1) ** popcount(a & b)
W /= 8  # normalize: W @ W^T = I

# Group Walsh indices by Hamming weight
hw_groups = {}  # weight -> list of indices
for i in range(N_HEX):
    w = popcount(i)
    hw_groups.setdefault(w, []).append(i)

# Eigenvalues: weight k → eigenvalue 2k
EIGENVALUES = [2 * k for k in range(N_LINES + 1)]
MULTIPLICITIES = [len(hw_groups[k]) for k in range(N_LINES + 1)]

# ═══════════════════════════════════════════════════════════════
# STEP 1: Walsh Spectral Decomposition
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print("STEP 1: WALSH SPECTRAL DECOMPOSITION (BGE-M3)")
print("=" * 70)

# Center embeddings
hex_centered = hex_bge - hex_bge.mean(axis=0, keepdims=True)

# Project onto Walsh basis
walsh_coeffs = W @ hex_centered  # 64×1024

# Total variance
total_var = np.sum(walsh_coeffs ** 2)

# Variance per eigenspace
real_var_fracs = []
for k in range(N_LINES + 1):
    idx = hw_groups[k]
    var_k = np.sum(walsh_coeffs[idx] ** 2)
    real_var_fracs.append(var_k / total_var)

# Permutation null
null_var_fracs = np.zeros((N_PERM_WALSH, N_LINES + 1))
for p in range(N_PERM_WALSH):
    perm = np.random.permutation(N_HEX)
    perm_centered = hex_bge[perm] - hex_bge[perm].mean(axis=0, keepdims=True)
    perm_coeffs = W @ perm_centered
    perm_total = np.sum(perm_coeffs ** 2)
    for k in range(N_LINES + 1):
        idx = hw_groups[k]
        null_var_fracs[p, k] = np.sum(perm_coeffs[idx] ** 2) / perm_total

# Compute percentiles
percentiles = []
for k in range(N_LINES + 1):
    pct = np.mean(null_var_fracs[:, k] <= real_var_fracs[k]) * 100
    percentiles.append(pct)

# Print table
print(f"\n{'Eigenval':>8} {'Mult':>5} {'Real Var%':>10} {'Null Mean±Std':>16} {'Pctile':>8}")
print("-" * 55)
for k in range(N_LINES + 1):
    ev = EIGENVALUES[k]
    mult = MULTIPLICITIES[k]
    real = real_var_fracs[k] * 100
    null_mean = null_var_fracs[:, k].mean() * 100
    null_std = null_var_fracs[:, k].std() * 100
    pct = percentiles[k]
    print(f"{ev:>8d} {mult:>5d} {real:>9.3f}% {null_mean:>7.3f}±{null_std:<6.3f}% {pct:>7.1f}%")

# Spectral slope: log variance vs eigenvalue
print(f"\nTotal variance: {total_var:.4f}")
# Effective dimensionality check
cumvar = np.cumsum(real_var_fracs)
print(f"Cumulative variance through eigenvalue 4: {cumvar[2]*100:.1f}%")
print(f"Cumulative variance through eigenvalue 6: {cumvar[3]*100:.1f}%")

# ═══════════════════════════════════════════════════════════════
# STEP 2: Laplacian Field Analysis
# ═══════════════════════════════════════════════════════════════

def compute_laplacian_vectors(emb):
    """Compute Lap(h) = mean(neighbors) - emb(h) for all hexagrams."""
    lap = np.zeros_like(emb)
    for h in range(N_HEX):
        nbrs = hamming_neighbors(h)
        lap[h] = emb[nbrs].mean(axis=0) - emb[h]
    return lap

def compute_lap_norms(emb):
    """L2 norms of Laplacian vectors."""
    lap = compute_laplacian_vectors(emb)
    return np.linalg.norm(lap, axis=1)

def compute_complement_cosines(emb):
    """Cosine of Laplacian vectors for 32 complement pairs."""
    lap = compute_laplacian_vectors(emb)
    cosines = []
    for h in range(32):
        comp = 63 - h
        cosines.append(cosine(lap[h], lap[comp]))
    return np.array(cosines)

# ─── Step 2a: Divergence Existence ───
print("\n" + "=" * 70)
print("STEP 2a: LAPLACIAN DIVERGENCE (BGE-M3, RAW)")
print("=" * 70)

real_norms = compute_lap_norms(hex_bge)
real_mean_norm = real_norms.mean()
print(f"\nMean ||Lap(h)||: {real_mean_norm:.6f}")
print(f"Std  ||Lap(h)||: {real_norms.std():.6f}")
print(f"Min: {real_norms.min():.6f}, Max: {real_norms.max():.6f}")

# Permutation null for mean norm
null_mean_norms = np.zeros(N_PERM_LAP)
for p in range(N_PERM_LAP):
    perm = np.random.permutation(N_HEX)
    null_mean_norms[p] = compute_lap_norms(hex_bge[perm]).mean()

pct_norm = np.mean(null_mean_norms >= real_mean_norm) * 100
print(f"Null mean norm: {null_mean_norms.mean():.6f} ± {null_mean_norms.std():.6f}")
print(f"Percentile (real ≤ null): {pct_norm:.1f}%  (lower = smoother than random)")

# ─── Step 2b: Complement Anti-parallelism (KEY TEST) ───
print("\n" + "=" * 70)
print("STEP 2b: COMPLEMENT LAPLACIAN ANTI-PARALLELISM (KEY TEST)")
print("=" * 70)

# BGE-M3
real_cos_bge = compute_complement_cosines(hex_bge)
print(f"\n--- BGE-M3 (raw) ---")
print(f"Mean cosine(Lap(h), Lap(63-h)): {real_cos_bge.mean():.6f}")
print(f"Median: {np.median(real_cos_bge):.6f}")
print(f"Std: {real_cos_bge.std():.6f}")
print(f"Fraction negative: {np.mean(real_cos_bge < 0):.3f} ({np.sum(real_cos_bge < 0)}/32)")
print(f"Min: {real_cos_bge.min():.6f}, Max: {real_cos_bge.max():.6f}")

# Permutation null for BGE-M3
null_mean_cos_bge = np.zeros(N_PERM_LAP)
for p in range(N_PERM_LAP):
    perm = np.random.permutation(N_HEX)
    null_mean_cos_bge[p] = compute_complement_cosines(hex_bge[perm]).mean()

pct_cos_bge = np.mean(null_mean_cos_bge <= real_cos_bge.mean()) * 100
print(f"Null mean cosine: {null_mean_cos_bge.mean():.6f} ± {null_mean_cos_bge.std():.6f}")
print(f"Percentile: {pct_cos_bge:.1f}%")

# E5-large cross-model check
real_cos_e5 = compute_complement_cosines(hex_e5)
print(f"\n--- E5-large (raw) ---")
print(f"Mean cosine(Lap(h), Lap(63-h)): {real_cos_e5.mean():.6f}")
print(f"Median: {np.median(real_cos_e5):.6f}")
print(f"Std: {real_cos_e5.std():.6f}")
print(f"Fraction negative: {np.mean(real_cos_e5 < 0):.3f} ({np.sum(real_cos_e5 < 0)}/32)")

null_mean_cos_e5 = np.zeros(N_PERM_LAP)
for p in range(N_PERM_LAP):
    perm = np.random.permutation(N_HEX)
    null_mean_cos_e5[p] = compute_complement_cosines(hex_e5[perm]).mean()

pct_cos_e5 = np.mean(null_mean_cos_e5 <= real_cos_e5.mean()) * 100
print(f"Null mean cosine: {null_mean_cos_e5.mean():.6f} ± {null_mean_cos_e5.std():.6f}")
print(f"Percentile: {pct_cos_e5:.1f}%")

# ─── Step 2c: Algebraic Correlates ───
print("\n" + "=" * 70)
print("STEP 2c: ALGEBRAIC CORRELATES OF ||Lap(h)|| (BGE-M3, RAW)")
print("=" * 70)

# Extract atlas properties
element_map = {}
element_idx = 0
ranks = np.zeros(N_HEX)
shis = np.zeros(N_HEX)
hu_depths = np.zeros(N_HEX)
palace_els = np.zeros(N_HEX)

for h in range(N_HEX):
    a = atlas[str(h)]
    ranks[h] = a['rank']
    shis[h] = a['shi']
    hu_depths[h] = a['hu_depth']
    pe = a['palace_element']
    if pe not in element_map:
        element_map[pe] = element_idx
        element_idx += 1
    palace_els[h] = element_map[pe]

properties = {
    'rank': ranks,
    'shi': shis,
    'hu_depth': hu_depths,
    'palace_element': palace_els,
}

print(f"\nElement encoding: {element_map}")
print(f"\n{'Property':>16} {'Spearman r':>11} {'p-value (perm)':>15}")
print("-" * 48)

for name, vals in properties.items():
    rho, _ = stats.spearmanr(real_norms, vals)
    # Permutation p-value
    count = 0
    for p in range(N_PERM_CORR):
        perm_norms = real_norms[np.random.permutation(N_HEX)]
        rho_perm, _ = stats.spearmanr(perm_norms, vals)
        if abs(rho_perm) >= abs(rho):
            count += 1
    pval = count / N_PERM_CORR
    print(f"{name:>16} {rho:>+11.4f} {pval:>15.4f}")

# ═══════════════════════════════════════════════════════════════
# STEP 2 IN RESIDUAL SPACE
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("RESIDUAL SPACE: Regressing out linear bit effects")
print("=" * 70)

def compute_residual_embeddings(emb):
    """OLS regression of embeddings on 6 binary bit features, return residuals."""
    # Design matrix: 64×6, X[h,i] = bit i of h
    X = np.zeros((N_HEX, N_LINES))
    for h in range(N_HEX):
        for i in range(N_LINES):
            X[h, i] = (h >> i) & 1
    # Add intercept
    X_int = np.column_stack([np.ones(N_HEX), X])  # 64×7
    # OLS: beta = (X'X)^{-1} X'Y
    beta = np.linalg.lstsq(X_int, emb, rcond=None)[0]  # 7×1024
    predicted = X_int @ beta
    residuals = emb - predicted
    # Report variance explained
    total_var = np.sum((emb - emb.mean(axis=0)) ** 2)
    resid_var = np.sum(residuals ** 2)
    print(f"Variance explained by linear bits: {(1 - resid_var/total_var)*100:.1f}%")
    return residuals

res_bge = compute_residual_embeddings(hex_bge)
res_e5  = compute_residual_embeddings(hex_e5)

# ─── Residual Step 2a ───
print("\n" + "=" * 70)
print("STEP 2a (RESIDUAL): LAPLACIAN DIVERGENCE")
print("=" * 70)

res_norms = compute_lap_norms(res_bge)
res_mean_norm = res_norms.mean()
print(f"\nMean ||Lap(h)||: {res_mean_norm:.6f}")
print(f"Std: {res_norms.std():.6f}")

null_res_norms = np.zeros(N_PERM_LAP)
for p in range(N_PERM_LAP):
    perm = np.random.permutation(N_HEX)
    null_res_norms[p] = compute_lap_norms(res_bge[perm]).mean()

pct_res_norm = np.mean(null_res_norms >= res_mean_norm) * 100
print(f"Null mean: {null_res_norms.mean():.6f} ± {null_res_norms.std():.6f}")
print(f"Percentile (real ≤ null): {pct_res_norm:.1f}%")

# ─── Residual Step 2b (KEY TEST) ───
print("\n" + "=" * 70)
print("STEP 2b (RESIDUAL): COMPLEMENT ANTI-PARALLELISM (KEY TEST)")
print("=" * 70)

# BGE-M3 residual
res_cos_bge = compute_complement_cosines(res_bge)
print(f"\n--- BGE-M3 (residual) ---")
print(f"Mean cosine(Lap(h), Lap(63-h)): {res_cos_bge.mean():.6f}")
print(f"Median: {np.median(res_cos_bge):.6f}")
print(f"Std: {res_cos_bge.std():.6f}")
print(f"Fraction negative: {np.mean(res_cos_bge < 0):.3f} ({np.sum(res_cos_bge < 0)}/32)")

null_res_cos_bge = np.zeros(N_PERM_LAP)
for p in range(N_PERM_LAP):
    perm = np.random.permutation(N_HEX)
    null_res_cos_bge[p] = compute_complement_cosines(res_bge[perm]).mean()

pct_res_cos_bge = np.mean(null_res_cos_bge <= res_cos_bge.mean()) * 100
print(f"Null mean cosine: {null_res_cos_bge.mean():.6f} ± {null_res_cos_bge.std():.6f}")
print(f"Percentile: {pct_res_cos_bge:.1f}%")

# E5-large residual
res_cos_e5 = compute_complement_cosines(res_e5)
print(f"\n--- E5-large (residual) ---")
print(f"Mean cosine(Lap(h), Lap(63-h)): {res_cos_e5.mean():.6f}")
print(f"Median: {np.median(res_cos_e5):.6f}")
print(f"Std: {res_cos_e5.std():.6f}")
print(f"Fraction negative: {np.mean(res_cos_e5 < 0):.3f} ({np.sum(res_cos_e5 < 0)}/32)")

null_res_cos_e5 = np.zeros(N_PERM_LAP)
for p in range(N_PERM_LAP):
    perm = np.random.permutation(N_HEX)
    null_res_cos_e5[p] = compute_complement_cosines(res_e5[perm]).mean()

pct_res_cos_e5 = np.mean(null_res_cos_e5 <= res_cos_e5.mean()) * 100
print(f"Null mean cosine: {null_res_cos_e5.mean():.6f} ± {null_res_cos_e5.std():.6f}")
print(f"Percentile: {pct_res_cos_e5:.1f}%")

# ─── Residual Step 2c ───
print("\n" + "=" * 70)
print("STEP 2c (RESIDUAL): ALGEBRAIC CORRELATES OF ||Lap(h)||")
print("=" * 70)

print(f"\n{'Property':>16} {'Spearman r':>11} {'p-value (perm)':>15}")
print("-" * 48)

for name, vals in properties.items():
    rho, _ = stats.spearmanr(res_norms, vals)
    count = 0
    for p in range(N_PERM_CORR):
        perm_norms = res_norms[np.random.permutation(N_HEX)]
        rho_perm, _ = stats.spearmanr(perm_norms, vals)
        if abs(rho_perm) >= abs(rho):
            count += 1
    pval = count / N_PERM_CORR
    print(f"{name:>16} {rho:>+11.4f} {pval:>15.4f}")

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SUMMARY OF KEY NUMBERS")
print("=" * 70)

print(f"""
Walsh Spectrum Shape:
  Low-freq (eigenval 0-4) cumulative variance: {cumvar[2]*100:.1f}%
  k=1 (eigenval 2) real variance: {real_var_fracs[1]*100:.3f}% vs null {null_var_fracs[:,1].mean()*100:.3f}% (pctile {percentiles[1]:.1f}%)

Complement Laplacian Cosine (mean):
  BGE-M3 raw:      {real_cos_bge.mean():.6f}  (null: {null_mean_cos_bge.mean():.6f}, pctile: {pct_cos_bge:.1f}%)
  BGE-M3 residual:  {res_cos_bge.mean():.6f}  (null: {null_res_cos_bge.mean():.6f}, pctile: {pct_res_cos_bge:.1f}%)
  E5-large raw:     {real_cos_e5.mean():.6f}  (null: {null_mean_cos_e5.mean():.6f}, pctile: {pct_cos_e5:.1f}%)
  E5-large residual: {res_cos_e5.mean():.6f}  (null: {null_res_cos_e5.mean():.6f}, pctile: {pct_res_cos_e5:.1f}%)

Laplacian Smoothness:
  BGE-M3 raw mean ||Lap||:     {real_mean_norm:.6f}  (null: {null_mean_norms.mean():.6f}, pctile ≤null: {pct_norm:.1f}%)
  BGE-M3 residual mean ||Lap||: {res_mean_norm:.6f}  (null: {null_res_norms.mean():.6f}, pctile ≤null: {pct_res_norm:.1f}%)
""")
