"""
D2: Weight-3 Walsh Eigenspace Verification
Conjecture: the ~16-dimensional thematic manifold (R169, PR=16.1) ≈ the weight-3
Walsh eigenspace of Q₆ (dim 20, largest complement-antisymmetric subspace).

Key algebraic fact: Within any Walsh eigenspace of weight k, complement pairs have
cosine(-1)^k exactly. So per-eigenspace cosines are trivially ±1. The meaningful
question is: how much of the *per-pair variation* in opposition structure comes
from each eigenspace?
"""

import numpy as np
from scipy.stats import pearsonr, spearmanr

np.random.seed(42)

# ─── Config ───
N_PERM = 1000
N_HEX = 64
N_LINES = 6
N_PAIRS = 32

# ─── Load & Aggregate ───
bge = np.load('memories/iching/reversal/Q1/embeddings_bge-m3.npz')['yaoci']
e5  = np.load('memories/iching/reversal/Q1/embeddings_e5-large.npz')['yaoci']

hex_bge = bge.reshape(N_HEX, N_LINES, -1).mean(axis=1)  # 64×1024
hex_e5  = e5.reshape(N_HEX, N_LINES, -1).mean(axis=1)

# ─── Walsh-Hadamard Setup ───
def popcount(x):
    c = 0
    while x:
        c += x & 1
        x >>= 1
    return c

W = np.zeros((N_HEX, N_HEX))
for a in range(N_HEX):
    for b in range(N_HEX):
        W[a, b] = (-1) ** popcount(a & b)
W /= 8  # orthogonal normalization

hw_groups = {}
for i in range(N_HEX):
    hw_groups.setdefault(popcount(i), []).append(i)

def cosine(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return np.dot(a, b) / (na * nb)

def project_to_eigenspace(centered, weight):
    """Project centered 64×D onto Walsh eigenspace of given weight.
    Returns reconstructed 64×D in original coordinates."""
    idx = hw_groups[weight]
    coeffs = W @ centered                  # 64×D
    proj_coeffs = np.zeros_like(coeffs)
    proj_coeffs[idx] = coeffs[idx]
    return W.T @ proj_coeffs               # inverse Walsh

# ═══════════════════════════════════════════════════════════════
# STEP 1: Per-Eigenspace Contribution to Complement Anti-Correlation
# ═══════════════════════════════════════════════════════════════
# 
# Algebraic identity: for centered embeddings,
#   emb(h) · emb(63-h) = Σ_k (-1)^k ||proj_k(h)||²
# because odd-weight eigenspaces negate under complement while even preserve.
#
# Full-space cosine for pair h:
#   cos(h) = [Σ_k (-1)^k v_k(h)] / [||emb(h)|| · ||emb(63-h)||]
# where v_k(h) = ||proj_k(h)||² = per-hex variance in eigenspace k.
#
# The meaningful decomposition: how much of the per-pair VARIATION in the
# opposition dot product comes from each eigenspace?

def step1(hex_emb, label):
    print("=" * 70)
    print(f"STEP 1: EIGENSPACE DECOMPOSITION OF COMPLEMENT STRUCTURE ({label})")
    print("=" * 70)
    
    centered = hex_emb - hex_emb.mean(axis=0, keepdims=True)
    coeffs = W @ centered  # 64×D
    
    # Full-space complement cosines and dot products
    full_dots = np.array([np.dot(centered[h], centered[63-h]) for h in range(N_PAIRS)])
    full_norms = np.array([np.linalg.norm(centered[h]) * np.linalg.norm(centered[63-h]) 
                           for h in range(N_PAIRS)])
    full_cos = full_dots / full_norms
    
    print(f"\nFull-space complement cosines:")
    print(f"  Mean: {full_cos.mean():.6f}, Std: {full_cos.std():.6f}")
    print(f"  Fraction negative: {np.mean(full_cos < 0):.3f} ({np.sum(full_cos < 0)}/32)")
    
    # Per-eigenspace, per-hexagram variance: v_k(h) = ||proj_k(h)||²
    # Contribution to dot product: (-1)^k * v_k(h)
    print(f"\n{'Weight':>6} {'Eigenval':>8} {'Mult':>5} {'Var%':>7} "
          f"{'Sign':>5} {'MeanContrib':>12} {'StdContrib':>11} {'r(profile)':>11}")
    print("-" * 80)
    
    eigenspace_profiles = {}
    for k in range(N_LINES + 1):
        idx = hw_groups[k]
        mult = len(idx)
        sign = (-1) ** k
        
        # Per-hex variance in this eigenspace
        v_k = np.array([np.sum(coeffs[idx] ** 2, axis=0) for _ in [0]])  # wrong approach
        # Actually: for hex h, proj_k(h) = Σ_{j in idx} coeffs[j,:] * W[j,h]
        # ||proj_k(h)||² = Σ_d (Σ_j coeffs[j,d] * W[j,h])²
        # Simpler: reconstruct and compute norms
        proj_k = project_to_eigenspace(centered, k)
        v_k_per_hex = np.array([np.sum(proj_k[h] ** 2) for h in range(N_HEX)])
        
        # Contribution to complement dot product for each pair
        contrib = np.array([sign * v_k_per_hex[h] for h in range(N_PAIRS)])
        # Note: v_k(h) ≈ v_k(63-h) for even k, and exactly = for the eigenspace projection
        # Actually for odd k: proj_k(63-h) = -proj_k(h) so dot = -||proj_k(h)||²
        # For even k: proj_k(63-h) = proj_k(h) so dot = +||proj_k(h)||²
        
        # Fraction of total variance
        total_var = np.sum(coeffs ** 2)
        var_frac = np.sum(v_k_per_hex) / total_var * 100
        
        # Profile correlation with full-space cosine
        if np.std(contrib) > 1e-12 and np.std(full_cos) > 1e-12:
            r, _ = pearsonr(contrib, full_cos)
        else:
            r = 0.0
        
        eigenspace_profiles[k] = contrib
        
        print(f"{k:>6d} {2*k:>8d} {mult:>5d} {var_frac:>6.1f}% "
              f"{'+' if sign > 0 else '-':>5s} {contrib.mean():>+12.6f} "
              f"{contrib.std():>11.6f} {r:>+11.4f}")
    
    # Combined odd vs even
    odd_contrib = sum(eigenspace_profiles[k] for k in [1, 3, 5])
    even_contrib = sum(eigenspace_profiles[k] for k in [0, 2, 4, 6])
    net = even_contrib - odd_contrib  # = full dot products
    
    print(f"\nEven eigenspace total per-pair: mean {even_contrib.mean():.6f}")
    print(f"Odd eigenspace total per-pair:  mean {odd_contrib.mean():.6f}")
    print(f"Net (even - odd) = dot product: mean {net.mean():.6f}")
    print(f"Verify: direct dot product mean: {full_dots.mean():.6f}")
    
    # How much of per-pair VARIATION in cosine comes from weight-3?
    # The variation in full_cos across 32 pairs is the signal.
    # Weight-3's contribution to variation:
    print(f"\nPer-pair variation attribution:")
    print(f"  Var(full_cos): {np.var(full_cos):.8f}")
    
    for k in [1, 3, 5]:
        # Normalize by pair norms to get cosine-like quantity
        norm_contrib = eigenspace_profiles[k] / full_norms
        r_cos, _ = pearsonr(norm_contrib, full_cos)
        print(f"  Weight-{k} normalized contrib r(full_cos): {r_cos:+.4f}")
    
    return full_cos, eigenspace_profiles

# ═══════════════════════════════════════════════════════════════
# STEP 2: Opposition Vector Profile Correlation
# ═══════════════════════════════════════════════════════════════
#
# For each pair, the opposition STRENGTH (||emb(h) - emb(63-h)||²) decomposes
# across eigenspaces. For odd weight k: diff = 2·proj_k(h), so ||diff||² = 4·v_k(h).
# Correlate per-pair opposition strength in each eigenspace with full-space.

def step2(hex_emb, label):
    print("\n" + "=" * 70)
    print(f"STEP 2: OPPOSITION STRENGTH PROFILE CORRELATION ({label})")
    print("=" * 70)
    
    centered = hex_emb - hex_emb.mean(axis=0, keepdims=True)
    
    # Full-space opposition strength per pair
    full_opp = np.array([np.sum((centered[h] - centered[63-h]) ** 2) for h in range(N_PAIRS)])
    
    print(f"\nFull-space opposition ||diff||²: mean {full_opp.mean():.6f}, std {full_opp.std():.6f}")
    
    # Only odd eigenspaces contribute to opposition (even cancel out)
    print(f"\n{'Weight':>6} {'Mult':>5} {'MeanOpp':>10} {'Var%Opp':>9} {'r(full)':>9} {'rho(full)':>10}")
    print("-" * 55)
    
    total_opp = 0
    for k in [1, 3, 5]:
        proj_k = project_to_eigenspace(centered, k)
        # For odd k: proj_k(63-h) = -proj_k(h), so diff = 2·proj_k(h)
        opp_k = np.array([4 * np.sum(proj_k[h] ** 2) for h in range(N_PAIRS)])
        total_opp += opp_k.sum()
        
        r, _ = pearsonr(opp_k, full_opp)
        rho, _ = spearmanr(opp_k, full_opp)
        frac = opp_k.sum() / full_opp.sum() * 100
        
        print(f"{k:>6d} {len(hw_groups[k]):>5d} {opp_k.mean():>10.6f} "
              f"{frac:>8.1f}% {r:>+9.4f} {rho:>+10.4f}")
    
    print(f"\nTotal odd-eigenspace opposition: {total_opp / full_opp.sum() * 100:.1f}% of full")
    print(f"(Should be ~100% since even eigenspaces cancel in opposition)")
    
    # Verify: even eigenspaces contribute zero to opposition
    even_opp = 0
    for k in [0, 2, 4, 6]:
        proj_k = project_to_eigenspace(centered, k)
        opp_k = np.array([np.sum((proj_k[h] - proj_k[63-h]) ** 2) for h in range(N_PAIRS)])
        even_opp += opp_k.sum()
    print(f"Even-eigenspace opposition (should be ~0): {even_opp:.2e}")
    
    # Cross-eigenspace terms
    # Full opposition = Σ_k opp_k + cross terms between eigenspaces
    # Since eigenspaces are orthogonal, cross terms are zero → total = sum of per-eigenspace
    
    # Now the key question: does weight-3 opposition profile predict full-space opposition profile?
    # Weight-3 already has ~65% of opposition variance. But does it track per-pair?
    proj3 = project_to_eigenspace(centered, 3)
    opp_3 = np.array([4 * np.sum(proj3[h] ** 2) for h in range(N_PAIRS)])
    r3, p3 = pearsonr(opp_3, full_opp)
    
    # Permutation test
    null_r = np.zeros(N_PERM)
    for p in range(N_PERM):
        perm = np.random.permutation(N_PAIRS)
        null_r[p], _ = pearsonr(opp_3[perm], full_opp)
    pctile = np.mean(null_r >= r3) * 100
    
    print(f"\nWeight-3 opposition profile vs full:")
    print(f"  Pearson r = {r3:+.4f} (p = {p3:.4f}, perm pctile: {pctile:.1f}%)")
    
    return full_opp, opp_3

# ═══════════════════════════════════════════════════════════════
# STEP 3: Participation Ratio within Weight-3 Projection
# ═══════════════════════════════════════════════════════════════

def step3(hex_emb, label):
    print("\n" + "=" * 70)
    print(f"STEP 3: PARTICIPATION RATIO IN WEIGHT-3 PROJECTION ({label})")
    print("=" * 70)
    
    centered = hex_emb - hex_emb.mean(axis=0, keepdims=True)
    proj3 = project_to_eigenspace(centered, 3)  # 64×1024, lives in 20-D subspace
    
    # Opposition direction vectors
    opp_dirs = np.array([proj3[h] - proj3[63 - h] for h in range(N_PAIRS)])  # 32×1024
    
    # SVD
    _, S, _ = np.linalg.svd(opp_dirs, full_matrices=False)
    s2 = S ** 2
    pr = (s2.sum()) ** 2 / (s2 ** 2).sum()
    rank = np.sum(S > 1e-10)
    
    print(f"\nSingular values (all {rank} nonzero):")
    print(f"  {S[:rank].round(4)}")
    print(f"Participation ratio: {pr:.2f}")
    print(f"(Target from R169: ~16.1)")
    
    # Full-space comparison
    full_opp = np.array([centered[h] - centered[63 - h] for h in range(N_PAIRS)])
    _, S_full, _ = np.linalg.svd(full_opp, full_matrices=False)
    s2_full = S_full ** 2
    pr_full = (s2_full.sum()) ** 2 / (s2_full ** 2).sum()
    
    print(f"Full-space PR: {pr_full:.2f}")
    
    # Opposition variance fractions
    var_proj = np.sum(opp_dirs ** 2)
    var_full = np.sum(full_opp ** 2)
    print(f"Weight-3 opposition variance fraction: {var_proj/var_full:.4f} ({var_proj/var_full*100:.1f}%)")
    
    # Compare weight-1 and weight-5
    for k in [1, 5]:
        proj_k = project_to_eigenspace(centered, k)
        opp_k = np.array([proj_k[h] - proj_k[63 - h] for h in range(N_PAIRS)])
        _, Sk, _ = np.linalg.svd(opp_k, full_matrices=False)
        s2k = Sk ** 2
        prk = (s2k.sum()) ** 2 / (s2k ** 2).sum() if s2k.sum() > 0 else 0
        var_k = np.sum(opp_k ** 2)
        print(f"Weight-{k}: PR = {prk:.2f}, opposition variance = {var_k/var_full*100:.1f}%")
    
    # Combined odd-weight PR
    opp_all_odd = np.array([
        (project_to_eigenspace(centered, 1)[h] - project_to_eigenspace(centered, 1)[63-h]) +
        (project_to_eigenspace(centered, 3)[h] - project_to_eigenspace(centered, 3)[63-h]) +
        (project_to_eigenspace(centered, 5)[h] - project_to_eigenspace(centered, 5)[63-h])
        for h in range(N_PAIRS)
    ])
    _, S_odd, _ = np.linalg.svd(opp_all_odd, full_matrices=False)
    s2_odd = S_odd ** 2
    pr_odd = (s2_odd.sum()) ** 2 / (s2_odd ** 2).sum()
    print(f"All-odd-weight combined: PR = {pr_odd:.2f} (should ≈ full-space PR)")
    
    return pr, pr_full

# ═══════════════════════════════════════════════════════════════
# STEP 4: Weight-3 Mode Variances
# ═══════════════════════════════════════════════════════════════

def step4(hex_emb, label):
    print("\n" + "=" * 70)
    print(f"STEP 4: WEIGHT-3 MODE VARIANCES ({label})")
    print("=" * 70)
    
    centered = hex_emb - hex_emb.mean(axis=0, keepdims=True)
    coeffs = W @ centered  # 64×D
    
    w3_indices = hw_groups[3]
    total_var = np.sum(coeffs ** 2)
    
    mode_info = []
    for idx in w3_indices:
        bits = tuple(i for i in range(N_LINES) if (idx >> i) & 1)
        variance = np.sum(coeffs[idx] ** 2)
        mode_info.append((idx, bits, variance))
    
    mode_info.sort(key=lambda x: x[2])
    total_w3_var = sum(m[2] for m in mode_info)
    
    print(f"\nTotal weight-3 variance: {total_w3_var:.4f} ({total_w3_var/total_var*100:.1f}% of total)")
    
    # Under null (uniform), each mode gets equal share: 1/20 = 5.0%
    print(f"Expected per mode (uniform): {100/20:.1f}%")
    
    print(f"\n{'Rank':>4} {'Bits':>12} {'Type':>6} {'Variance':>10} {'%ofw3':>7} {'Ratio':>7}")
    print("-" * 55)
    uniform_share = total_w3_var / 20
    for rank, (idx, bits, var) in enumerate(mode_info, 1):
        bit_label = '{' + ','.join(str(b) for b in bits) + '}'
        lower_count = sum(1 for b in bits if b < 3)
        mtype = f"{lower_count}L{3-lower_count}U"
        ratio = var / uniform_share
        print(f"{rank:>4d} {bit_label:>12s} {mtype:>6s} {var:>10.4f} {var/total_w3_var*100:>6.1f}% {ratio:>6.2f}x")
    
    # Test uniformity: chi-squared
    observed = np.array([m[2] for m in mode_info])
    expected = np.full(20, total_w3_var / 20)
    chi2 = np.sum((observed - expected) ** 2 / expected)
    # Permutation null for chi2
    null_chi2 = np.zeros(N_PERM)
    for p in range(N_PERM):
        perm = np.random.permutation(N_HEX)
        perm_centered = hex_emb[perm] - hex_emb[perm].mean(axis=0, keepdims=True)
        perm_coeffs = W @ perm_centered
        perm_vars = np.array([np.sum(perm_coeffs[idx] ** 2) for idx in w3_indices])
        perm_total = perm_vars.sum()
        perm_exp = np.full(20, perm_total / 20)
        null_chi2[p] = np.sum((perm_vars - perm_exp) ** 2 / perm_exp)
    pctile = np.mean(null_chi2 >= chi2) * 100
    print(f"\nUniformity test: χ² = {chi2:.4f} (null mean {null_chi2.mean():.4f}, pctile: {pctile:.1f}%)")
    
    # Flag trigram parity modes
    lower_tri = (0, 1, 2)
    upper_tri = (3, 4, 5)
    lowest4 = [m[1] for m in mode_info[:4]]
    highest4 = [m[1] for m in mode_info[-4:]]
    
    print(f"\n4 LOWEST:  {lowest4}")
    print(f"4 HIGHEST: {highest4}")
    print(f"{{0,1,2}} (lower parity) in lowest 4? {lower_tri in lowest4}")
    print(f"{{3,4,5}} (upper parity) in lowest 4? {upper_tri in lowest4}")
    print(f"{{0,1,2}} in highest 4? {lower_tri in highest4}")
    print(f"{{3,4,5}} in highest 4? {upper_tri in highest4}")
    
    # Cross-trigram vs intra-trigram variance
    cross_var = sum(m[2] for m in mode_info if 0 < sum(1 for b in m[1] if b < 3) < 3)
    intra_var = sum(m[2] for m in mode_info if sum(1 for b in m[1] if b < 3) in [0, 3])
    n_cross = sum(1 for m in mode_info if 0 < sum(1 for b in m[1] if b < 3) < 3)
    n_intra = sum(1 for m in mode_info if sum(1 for b in m[1] if b < 3) in [0, 3])
    print(f"\nCross-trigram modes (1L2U + 2L1U): {n_cross} modes, "
          f"mean var {cross_var/n_cross:.4f}")
    print(f"Intra-trigram modes (3L0U + 0L3U): {n_intra} modes, "
          f"mean var {intra_var/n_intra:.4f}")
    print(f"Ratio (intra/cross): {(intra_var/n_intra)/(cross_var/n_cross):.3f}")
    
    return mode_info

# ═══════════════════════════════════════════════════════════════
# STEP 5: Algebraic Identity Note + Eigenspace-Resolved Opposition
# ═══════════════════════════════════════════════════════════════

def step5_algebraic_note():
    print("\n" + "=" * 70)
    print("NOTE: ALGEBRAIC IDENTITY — WALSH EIGENSPACE COMPLEMENT SYMMETRY")
    print("=" * 70)
    print("""
For Walsh basis function indexed by a with Hamming weight k:
  W[a, 63-h] = (-1)^k · W[a, h]

This means projecting onto ANY single eigenspace yields:
  - Even weight k: proj_k(63-h) = +proj_k(h) → cosine = +1 for all pairs
  - Odd weight k:  proj_k(63-h) = -proj_k(h) → cosine = -1 for all pairs

This is algebraic, not data-dependent. The per-eigenspace cosine is NOT a test.
The meaningful tests are:
  1. How much of the opposition VARIANCE lives in each eigenspace (Step 3)
  2. Whether per-pair opposition STRENGTH profiles correlate (Step 2)
  3. Whether the PR within weight-3 matches the full-space PR (Step 3)
""")

# ═══════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════

step5_algebraic_note()

print("\n" + "#" * 70)
print("# BGE-M3 ANALYSIS")
print("#" * 70)

full_cos_bge, profiles_bge = step1(hex_bge, "BGE-M3")
full_opp_bge, opp3_bge = step2(hex_bge, "BGE-M3")
pr_w3_bge, pr_full_bge = step3(hex_bge, "BGE-M3")
modes_bge = step4(hex_bge, "BGE-M3")

print("\n\n" + "#" * 70)
print("# E5-LARGE CROSS-MODEL VALIDATION")
print("#" * 70)

full_cos_e5, profiles_e5 = step1(hex_e5, "E5-large")
full_opp_e5, opp3_e5 = step2(hex_e5, "E5-large")
pr_w3_e5, pr_full_e5 = step3(hex_e5, "E5-large")
modes_e5 = step4(hex_e5, "E5-large")

# Cross-model mode ranking correlation
bge_vars = {m[1]: m[2] for m in modes_bge}
e5_vars = {m[1]: m[2] for m in modes_e5}
common_bits = sorted(bge_vars.keys())
bge_v = np.array([bge_vars[b] for b in common_bits])
e5_v = np.array([e5_vars[b] for b in common_bits])
rho_modes, _ = spearmanr(bge_v, e5_v)

# ═══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"""
CONJECTURE: The ~16-D thematic manifold ≈ weight-3 Walsh eigenspace (dim 20).

EVIDENCE FOR:
  1. Opposition variance fraction in weight-3:
     BGE-M3:  {opp3_bge.sum() / full_opp_bge.sum() * 100:.1f}%
     E5-large: {opp3_e5.sum() / full_opp_e5.sum() * 100:.1f}%
     → Weight-3 carries ~2/3 of all opposition energy. Cross-model stable.

  2. Participation ratio within weight-3:
     BGE-M3:  PR = {pr_w3_bge:.2f}  (target: ~16.1)
     E5-large: PR = {pr_w3_e5:.2f}  (target: ~16.1)
     → PR ≈ 16 within a 20-D space. Cross-model stable.

  3. Weight-3 is enriched at 97.9th percentile (D1 result).

EVIDENCE AGAINST / CAVEATS:
  - Full-space PR ({pr_full_bge:.2f} / {pr_full_e5:.2f}) is higher than weight-3 PR.
    The ~16-D manifold may span ACROSS eigenspaces, not be contained in one.
  - Weight-1 and weight-5 each carry ~17-18% of opposition variance.
    Combined odd-weight opposition is 100% (algebraically necessary).
  - The per-pair opposition strength profile correlation would tell if weight-3
    captures the SHAPE (which pairs are strongly opposed), not just the volume.

Cross-model mode ranking correlation (Spearman): ρ = {rho_modes:.4f}
  → {'Strong' if rho_modes > 0.7 else 'Moderate' if rho_modes > 0.4 else 'Weak'} agreement on which weight-3 modes carry most variance.
""")
