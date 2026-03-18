#!/usr/bin/env python3
"""perturbation_directions.py — Do single-line perturbations push hexagrams
in consistent, distinguishable directions in embedding space?

Key insight: the naive mean over all 64 deltas is identically zero because
h → h⊕mask is a bijection (sum_h embed[h⊕m] = sum_h embed[h]). We use
CANONICAL displacements: for each of 32 pairs per line, compute embed[h₁] - embed[h₀]
where h₀ has bit=0 and h₁ has bit=1 at the flipped position.

6 computations across 5 embedding sources.
"""

import numpy as np
from pathlib import Path

# ════════════════════════════════════════════════════════════
# Paths & Constants
# ════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
SYNTH_EMB = ROOT / "synthesis" / "embeddings.npz"
CROSS_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
N_LINES = 6
N_PAIRS = 32  # 32 canonical pairs per line
N_PERM = 10_000
N_BOOT = 10_000

WITHIN_PAIRS = [(0, 3), (1, 4), (2, 5)]  # bit-paired lines (0-indexed)

RNG = np.random.default_rng(42)


# ════════════════════════════════════════════════════════════
# Data Loading
# ════════════════════════════════════════════════════════════

def load_sources():
    sources = {}
    synth = np.load(SYNTH_EMB)
    sources['bge-m3_guaci'] = synth['guaci']
    sources['bge-m3_tuan'] = synth['tuan']
    for model in ['bge-m3', 'e5-large', 'labse']:
        yaoci = np.load(CROSS_DIR / f"embeddings_{model}.npz")['yaoci']
        sources[f'{model}_yaoci'] = yaoci.reshape(64, 6, -1).mean(axis=1)
    return sources


# ════════════════════════════════════════════════════════════
# Core: Canonical Displacement Vectors
# ════════════════════════════════════════════════════════════

def canonical_deltas(embed, line_idx):
    """For line (0-indexed), return 32 displacement vectors: embed[h₁] - embed[h₀]
    where h₀ has bit=0 and h₁=h₀⊕mask has bit=1 at position line_idx."""
    mask = 1 << line_idx
    deltas = []
    for h in range(N_HEX):
        if (h >> line_idx) & 1 == 0:  # h has bit=0
            deltas.append(embed[h ^ mask] - embed[h])
    return np.array(deltas)  # (32, D)


def mean_displacements(embed):
    """Return (6, D) matrix of canonical mean displacement vectors."""
    return np.array([canonical_deltas(embed, i).mean(axis=0) for i in range(N_LINES)])


# ════════════════════════════════════════════════════════════
# Computations
# ════════════════════════════════════════════════════════════

def comp1_norms(embed):
    """Mean displacement norms for each line."""
    M = mean_displacements(embed)
    norms = np.linalg.norm(M, axis=1)
    # Also compute individual delta norms for context
    indiv_norms = np.array([np.linalg.norm(canonical_deltas(embed, i), axis=1).mean()
                            for i in range(N_LINES)])
    return norms, indiv_norms


def comp2_pvalues(embed):
    """Permutation test: is the mean displacement norm larger than random pairings?
    Null: randomly pair 32 source hexagrams with 32 targets (without replacement)."""
    M = mean_displacements(embed)
    norms = np.linalg.norm(M, axis=1)

    pvals = np.zeros(N_LINES)
    for i in range(N_LINES):
        observed = norms[i]
        mask = 1 << i
        h0s = [h for h in range(N_HEX) if (h >> i) & 1 == 0]
        h1s = [h ^ mask for h in h0s]
        # Null: shuffle the h1 targets
        null_norms = np.zeros(N_PERM)
        for t in range(N_PERM):
            perm_h1 = RNG.permutation(h1s)
            null_deltas = np.array([embed[perm_h1[k]] - embed[h0s[k]] for k in range(N_PAIRS)])
            null_norms[t] = np.linalg.norm(null_deltas.mean(axis=0))
        pvals[i] = (np.sum(null_norms >= observed) + 1) / (N_PERM + 1)

    return pvals


def comp3_svd(M):
    """SVD of (6, D) mean displacement matrix."""
    _, S, _ = np.linalg.svd(M, full_matrices=False)
    var = S ** 2
    cumvar = np.cumsum(var) / var.sum()
    participation = var.sum() ** 2 / (var ** 2).sum()
    return S, cumvar, participation


def comp4_cosine_matrix(M):
    """6×6 cosine similarity of mean displacement vectors."""
    norms = np.linalg.norm(M, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    Mn = M / norms
    return Mn @ Mn.T


def comp5_within_cross(cos_mat):
    """Within-pair (same bit position) vs cross-pair cosines."""
    within = np.array([cos_mat[i, j] for i, j in WITHIN_PAIRS])
    cross = []
    for i in range(N_LINES):
        for j in range(i + 1, N_LINES):
            if (i, j) not in WITHIN_PAIRS:
                cross.append(cos_mat[i, j])
    return within, np.array(cross)


def comp6_angular_diversity(embed):
    """Bootstrap test: is angular diversity of 6 directions real or noise?"""
    M = mean_displacements(embed)
    cos_mat = comp4_cosine_matrix(M)
    mask = ~np.eye(N_LINES, dtype=bool)
    observed = cos_mat[mask].mean()

    boot_vals = np.zeros(N_BOOT)
    for t in range(N_BOOT):
        idx = RNG.choice(N_HEX, size=N_HEX, replace=True)
        bM = mean_displacements(embed[idx])
        bcos = comp4_cosine_matrix(bM)
        boot_vals[t] = bcos[mask].mean()

    # Lower cosine = more diverse. p = fraction with cosine ≤ observed
    p_diverse = (np.sum(boot_vals <= observed) + 1) / (N_BOOT + 1)
    boot_5th = np.percentile(boot_vals, 5)

    return observed, boot_5th, p_diverse


# ════════════════════════════════════════════════════════════
# Analysis per source
# ════════════════════════════════════════════════════════════

def analyze_source(name, embed):
    D = embed.shape[1]
    print(f"\nSource: {name} ({N_HEX} × {D})")
    print("=" * 60)

    # Comp 1: norms
    norms, indiv_norms = comp1_norms(embed)
    # Comp 2: p-values
    pvals = comp2_pvalues(embed)

    print(f"\nMEAN DISPLACEMENT NORMS (canonical 32-pair, bit 0→1):")
    for i in range(N_LINES):
        print(f"  Line {i+1}: ‖⟨Δ{i+1}⟩‖ = {norms[i]:.6f}  "
              f"(p = {pvals[i]:.4f})  "
              f"[indiv mean ‖δ‖ = {indiv_norms[i]:.4f}, "
              f"ratio = {norms[i]/indiv_norms[i]:.4f}]")

    # Comp 3: SVD
    M = mean_displacements(embed)
    S, cumvar, pr = comp3_svd(M)
    print(f"\nSVD OF MEAN DISPLACEMENT MATRIX (6×{D}):")
    print(f"  Singular values: [{', '.join(f'{s:.6f}' for s in S)}]")
    print(f"  Cumulative var:  [{', '.join(f'{v:.1%}' for v in cumvar)}]")
    print(f"  Participation ratio: {pr:.2f} (effective rank)")
    print(f"  σ₁/σ₂ = {S[0]/S[1]:.2f}")

    # Comp 4: cosine matrix
    cos_mat = comp4_cosine_matrix(M)
    print(f"\nCOSINE SIMILARITY MATRIX:")
    header = "      " + "  ".join(f"  L{i+1}" for i in range(N_LINES))
    print(header)
    for i in range(N_LINES):
        row = f"  L{i+1} " + "  ".join(f"{cos_mat[i,j]:+.2f}" for j in range(N_LINES))
        print(row)

    # Comp 5: within vs cross
    within, cross = comp5_within_cross(cos_mat)
    print(f"\nWITHIN-PAIR COSINES (same bit position, different trigram):")
    for k, (i, j) in enumerate(WITHIN_PAIRS):
        print(f"  cos(L{i+1},L{j+1}) = {within[k]:+.4f}   (bit {k})")
    print(f"  Mean within-pair: {within.mean():+.4f}")
    print(f"  Mean cross-pair:  {cross.mean():+.4f}")

    # Comp 6: angular diversity
    obs_cos, boot_5, p_div = comp6_angular_diversity(embed)
    print(f"\nANGULAR DIVERSITY:")
    print(f"  Mean off-diagonal cosine: {obs_cos:+.4f}")
    print(f"  Bootstrap 5th percentile: {boot_5:+.4f}")
    print(f"  Observed < bootstrap 5th: {'YES' if obs_cos < boot_5 else 'NO'} (p = {p_div:.4f})")

    return {
        'norms': norms,
        'pvals': pvals,
        'singular_values': S,
        'cumvar': cumvar,
        'participation': pr,
        'cos_matrix': cos_mat,
        'within_cosines': within,
        'mean_within': within.mean(),
        'mean_cross': cross.mean(),
        'obs_mean_cos': obs_cos,
        'boot_5th': boot_5,
        'p_diverse': p_div,
    }


# ════════════════════════════════════════════════════════════
# Cross-model summary
# ════════════════════════════════════════════════════════════

def cross_model_summary(results):
    print(f"\n{'='*60}")
    print("CROSS-MODEL SUMMARY")
    print(f"{'='*60}")

    # Significance
    print(f"\nSignificance (p < 0.05) per line:")
    print(f"  {'Source':>20}  " + "  ".join(f"  L{i+1}" for i in range(N_LINES)))
    print(f"  {'─'*60}")
    for name in results:
        pv = results[name]['pvals']
        row = "  ".join(f"{'***' if p<0.001 else '** ' if p<0.01 else '*  ' if p<0.05 else 'ns ':>5}"
                        for p in pv)
        print(f"  {name:>20}  {row}")

    n_sig = sum(1 for name in results for p in results[name]['pvals'] if p < 0.05)
    n_total = len(results) * N_LINES
    print(f"\n  Significant tests: {n_sig}/{n_total}")

    # Effective rank
    print(f"\nEffective rank (participation ratio):")
    for name in results:
        pr = results[name]['participation']
        print(f"  {name:>20}: {pr:.2f}")

    print(f"\nσ₁/σ₂ ratio:")
    for name in results:
        S = results[name]['singular_values']
        print(f"  {name:>20}: {S[0]/S[1]:.2f}")

    # Within vs cross
    print(f"\nWithin-pair cosine means:")
    print(f"  {'Source':>20}  {'bit0':>7}  {'bit1':>7}  {'bit2':>7}  {'mean':>7}")
    print(f"  {'─'*55}")
    for name in results:
        w = results[name]['within_cosines']
        print(f"  {name:>20}  {w[0]:+.4f}  {w[1]:+.4f}  {w[2]:+.4f}  {w.mean():+.4f}")

    print(f"\nMean within-pair vs cross-pair cosine:")
    print(f"  {'Source':>20}  {'within':>8}  {'cross':>8}  {'Δ':>8}")
    print(f"  {'─'*50}")
    for name in results:
        w = results[name]['mean_within']
        c = results[name]['mean_cross']
        print(f"  {name:>20}  {w:+.4f}    {c:+.4f}    {w-c:+.4f}")

    # Angular diversity
    print(f"\nAngular diversity test:")
    for name in results:
        r = results[name]
        sig = "SIG" if r['p_diverse'] < 0.05 else "ns"
        print(f"  {name:>20}: obs={r['obs_mean_cos']:+.4f}  "
              f"boot_5th={r['boot_5th']:+.4f}  p={r['p_diverse']:.4f}  [{sig}]")

    # Verdict
    prs = [results[n]['participation'] for n in results]
    mean_pr = np.mean(prs)
    ratios = [results[n]['singular_values'][0] / results[n]['singular_values'][1] for n in results]
    mean_ratio = np.mean(ratios)

    within_gt_cross = [results[n]['mean_within'] > results[n]['mean_cross'] for n in results]
    consistent_within = all(within_gt_cross) or not any(within_gt_cross)

    if mean_pr < 1.5:
        rank_verdict = "rank 1 — all lines push in the same direction"
    elif mean_pr < 2.5:
        rank_verdict = "rank 2 — two independent perturbation directions"
    elif mean_pr < 3.5:
        rank_verdict = "rank 3 — three independent perturbation directions"
    else:
        rank_verdict = f"rank {mean_pr:.1f}"

    print(f"\n  Mean participation ratio: {mean_pr:.2f}")
    print(f"  Mean σ₁/σ₂: {mean_ratio:.2f}")
    print(f"  Within > cross consistent: {'YES' if consistent_within else 'NO (inconsistent)'}")
    print(f"  Verdict: {rank_verdict}")


if __name__ == '__main__':
    sources = load_sources()
    results = {}
    for name, embed in sources.items():
        results[name] = analyze_source(name, embed)
    cross_model_summary(results)
