#!/usr/bin/env python3
"""
Rank Bimodality Analysis — Follow-up to position_resolved.py
==============================================================
Determines whether 升↔无妄's bimodal rank pattern (strongly opposed at L3/L5,
weakly opposed at L1/L2/L4/L6) is pair-specific or an artifact of marginals.

Steps:
1. Build full 32×6 rank matrix per model
2. Rank variance per pair (raw)
3. Marginal-corrected rank variance
4. Cross-model consistency of bimodality patterns
"""

import json
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
N_LINES = 6

MODEL_PATHS = {
    'bge-m3':      Q1_DIR / "embeddings_bge-m3.npz",
    'e5-large':    Q1_DIR / "embeddings_e5-large.npz",
    'labse':       Q1_DIR / "embeddings_labse.npz",
    'sikuroberta': Q1_DIR / "embeddings_sikuroberta.npz",
}
MODEL_ORDER = list(MODEL_PATHS.keys())

H_SHENG = 6    # 升, KW#46
H_WUWANG = 57  # 无妄, KW#25


def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)


def load_data():
    atlas = json.load(open(ATLAS_PATH))

    pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)
    assert len(pairs) == 32

    models = {}
    for name, path in MODEL_PATHS.items():
        models[name] = np.load(path)['yaoci']

    return atlas, pairs, models


def build_rank_matrix(emb, pairs):
    """Build 32×6 rank matrix. rank_mat[i, k] = rank of pair i at position k+1.
    Rank 1 = lowest cosine (most opposed), rank 32 = highest (least opposed)."""
    rank_mat = np.zeros((32, 6), dtype=int)

    for k in range(6):
        pos_emb = emb[k::6]  # 64 embeddings at position k+1
        cos_vals = np.array([cosine_sim(pos_emb[h1], pos_emb[h2]) for h1, h2 in pairs])
        # argsort gives indices that would sort ascending (lowest cos first)
        order = np.argsort(cos_vals)
        # rank[order[i]] = i+1
        ranks = np.empty(32, dtype=int)
        ranks[order] = np.arange(1, 33)
        rank_mat[:, k] = ranks

    return rank_mat


# ══════════════════════════════════════════════════════════════
# STEP 1: Full 32×6 Rank Matrices
# ══════════════════════════════════════════════════════════════

def step1(models, pairs, atlas):
    print("=" * 80)
    print("STEP 1: 32×6 RANK MATRICES")
    print("=" * 80)
    print()

    sw_pair = (min(H_SHENG, H_WUWANG), max(H_SHENG, H_WUWANG))
    sw_idx = pairs.index(sw_pair)

    rank_mats = {}
    for m in MODEL_ORDER:
        rank_mats[m] = build_rank_matrix(models[m], pairs)

    # Show 升↔无妄 row across models for verification
    print(f"  升↔无妄 (pair {sw_idx}) rank vectors:")
    for m in MODEL_ORDER:
        row = rank_mats[m][sw_idx]
        print(f"    {m:14s}: {row.tolist()}")
    print()

    # Show a few other pairs for context
    print(f"  Sample pairs for context:")
    for i in [0, 5, 15, 25, 31]:
        h1, h2 = pairs[i]
        n1 = atlas[str(h1)]['kw_name']
        n2 = atlas[str(h2)]['kw_name']
        # Average ranks across models
        avg_row = np.mean([rank_mats[m][i] for m in MODEL_ORDER], axis=0)
        print(f"    Pair {i:2d} ({n1:10s}↔{n2:10s}): avg ranks = "
              f"[{', '.join(f'{r:.1f}' for r in avg_row)}]")
    print()

    return rank_mats, sw_idx


# ══════════════════════════════════════════════════════════════
# STEP 2: Rank Variance Per Pair (Raw)
# ══════════════════════════════════════════════════════════════

def step2(rank_mats, pairs, atlas, sw_idx):
    print("=" * 80)
    print("STEP 2: RANK VARIANCE PER PAIR (RAW)")
    print("  High variance = pair's rank varies strongly across positions")
    print("=" * 80)
    print()

    # For each pair, compute variance of its 6-position ranks, averaged across models
    avg_variances = np.zeros(32)
    per_model_var = {m: np.zeros(32) for m in MODEL_ORDER}

    for i in range(32):
        model_vars = []
        for m in MODEL_ORDER:
            v = np.var(rank_mats[m][i], ddof=0)
            per_model_var[m][i] = v
            model_vars.append(v)
        avg_variances[i] = np.mean(model_vars)

    # Sort by descending variance
    order = np.argsort(-avg_variances)

    print(f"  {'Rank':>4s} | {'Pair':>4s} {'Name1':>10s} {'Name2':>10s} | {'Avg Var':>8s} |", end="")
    for m in MODEL_ORDER:
        print(f" {m[:6]:>7s}", end="")
    print(" | Flag")
    print("  " + "-" * 100)

    for rank_pos, i in enumerate(order):
        h1, h2 = pairs[i]
        n1 = atlas[str(h1)]['kw_name']
        n2 = atlas[str(h2)]['kw_name']
        flag = " ◄ 升↔无妄" if i == sw_idx else ""

        row = f"  {rank_pos+1:4d} | {i:4d} {n1:>10s} {n2:>10s} | {avg_variances[i]:8.1f} |"
        for m in MODEL_ORDER:
            row += f" {per_model_var[m][i]:7.1f}"
        row += f" | {flag}"
        print(row)

    print()

    # Summary stats
    sw_var = avg_variances[sw_idx]
    sw_rank = np.where(order == sw_idx)[0][0] + 1
    print(f"  升↔无妄: avg variance = {sw_var:.1f}, rank = {sw_rank}/32")
    print(f"  Distribution: min={avg_variances.min():.1f}, median={np.median(avg_variances):.1f}, "
          f"max={avg_variances.max():.1f}, mean={avg_variances.mean():.1f}")
    print()

    return avg_variances, per_model_var


# ══════════════════════════════════════════════════════════════
# STEP 3: Marginal-Corrected Rank Variance
# ══════════════════════════════════════════════════════════════

def step3(rank_mats, pairs, atlas, sw_idx):
    print("=" * 80)
    print("STEP 3: MARGINAL-CORRECTED RANK VARIANCE")
    print("  Subtract position means to remove L1 marginal effect")
    print("=" * 80)
    print()

    # For each model, compute position means and correct
    corrected_vars = np.zeros(32)
    per_model_corrected = {m: np.zeros(32) for m in MODEL_ORDER}

    for m in MODEL_ORDER:
        rm = rank_mats[m].astype(float)
        # Position means (column means)
        pos_means = rm.mean(axis=0)
        # Corrected ranks
        corrected = rm - pos_means[np.newaxis, :]

        for i in range(32):
            per_model_corrected[m][i] = np.var(corrected[i], ddof=0)

    # Show position means per model
    print("  Position means (should be ~16.5 = uniform mean rank):")
    for m in MODEL_ORDER:
        rm = rank_mats[m].astype(float)
        pm = rm.mean(axis=0)
        print(f"    {m:14s}: [{', '.join(f'{v:.2f}' for v in pm)}]")
    print()

    # Average corrected variance across models
    for i in range(32):
        corrected_vars[i] = np.mean([per_model_corrected[m][i] for m in MODEL_ORDER])

    order = np.argsort(-corrected_vars)

    print(f"  {'Rank':>4s} | {'Pair':>4s} {'Name1':>10s} {'Name2':>10s} | {'Corr Var':>9s} |", end="")
    for m in MODEL_ORDER:
        print(f" {m[:6]:>7s}", end="")
    print(" | Flag")
    print("  " + "-" * 105)

    for rank_pos, i in enumerate(order[:10]):
        h1, h2 = pairs[i]
        n1 = atlas[str(h1)]['kw_name']
        n2 = atlas[str(h2)]['kw_name']
        flag = " ◄ 升↔无妄" if i == sw_idx else ""

        row = f"  {rank_pos+1:4d} | {i:4d} {n1:>10s} {n2:>10s} | {corrected_vars[i]:9.1f} |"
        for m in MODEL_ORDER:
            row += f" {per_model_corrected[m][i]:7.1f}"
        row += f" | {flag}"
        print(row)

    # Show 升↔无妄 if not in top 10
    sw_rank_corr = np.where(order == sw_idx)[0][0] + 1
    if sw_rank_corr > 10:
        i = sw_idx
        h1, h2 = pairs[i]
        n1 = atlas[str(h1)]['kw_name']
        n2 = atlas[str(h2)]['kw_name']
        print(f"  ...")
        row = f"  {sw_rank_corr:4d} | {i:4d} {n1:>10s} {n2:>10s} | {corrected_vars[i]:9.1f} |"
        for m in MODEL_ORDER:
            row += f" {per_model_corrected[m][i]:7.1f}"
        row += " |  ◄ 升↔无妄"
        print(row)

    print()
    print(f"  升↔无妄: corrected variance = {corrected_vars[sw_idx]:.1f}, rank = {sw_rank_corr}/32")
    print(f"  Distribution: min={corrected_vars.min():.1f}, median={np.median(corrected_vars):.1f}, "
          f"max={corrected_vars.max():.1f}")
    print()

    # Show corrected rank profile for top pairs
    print("  CORRECTED RANK PROFILES (top 5 + 升↔无妄):")
    print(f"  {'Pair':>4s} {'Name':>22s} | {'L1':>6s} {'L2':>6s} {'L3':>6s} {'L4':>6s} {'L5':>6s} {'L6':>6s}")
    print("  " + "-" * 65)
    shown = set()
    for rank_pos, i in enumerate(order[:5]):
        h1, h2 = pairs[i]
        n = f"{atlas[str(h1)]['kw_name']}↔{atlas[str(h2)]['kw_name']}"
        avg_ranks = np.mean([rank_mats[m][i].astype(float) for m in MODEL_ORDER], axis=0)
        print(f"  {i:4d} {n:>22s} | {' '.join(f'{r:6.1f}' for r in avg_ranks)}")
        shown.add(i)
    if sw_idx not in shown:
        i = sw_idx
        h1, h2 = pairs[i]
        n = f"{atlas[str(h1)]['kw_name']}↔{atlas[str(h2)]['kw_name']}"
        avg_ranks = np.mean([rank_mats[m][i].astype(float) for m in MODEL_ORDER], axis=0)
        print(f"  {i:4d} {n:>22s} | {' '.join(f'{r:6.1f}' for r in avg_ranks)}  ◄ 升↔无妄")
    print()

    return corrected_vars


# ══════════════════════════════════════════════════════════════
# STEP 4: Cross-Model Consistency of Bimodality
# ══════════════════════════════════════════════════════════════

def step4(rank_mats, pairs, atlas, sw_idx):
    print("=" * 80)
    print("STEP 4: CROSS-MODEL CONSISTENCY OF BIMODALITY")
    print("  Are the same pairs positionally heterogeneous across models?")
    print("=" * 80)
    print()

    # Per-model rank variance vector (32,)
    var_vectors = {}
    for m in MODEL_ORDER:
        var_vectors[m] = np.array([np.var(rank_mats[m][i], ddof=0) for i in range(32)])

    # Pairwise Spearman correlations
    model_pairs = list(combinations(MODEL_ORDER, 2))
    rhos = []

    print(f"  Cross-model Spearman ρ of rank-variance vectors (32 pairs):")
    for m1, m2 in model_pairs:
        rho, p = spearmanr(var_vectors[m1], var_vectors[m2])
        rhos.append(rho)
        sig = " ***" if p < 0.01 else " *" if p < 0.05 else ""
        print(f"    {m1:14s} × {m2:14s}: ρ={rho:+.4f} (p={p:.4f}){sig}")

    print(f"    Mean ρ: {np.mean(rhos):+.4f}")
    print(f"    Range: [{min(rhos):+.4f}, {max(rhos):+.4f}]")
    print()

    if np.mean(rhos) > 0.5:
        print("  → HIGH CONSISTENCY: rank heterogeneity is text-intrinsic, not model noise")
    elif np.mean(rhos) > 0.2:
        print("  → MODERATE CONSISTENCY: partial text-intrinsic signal")
    else:
        print("  → LOW CONSISTENCY: rank heterogeneity is model-specific noise")
    print()

    # Identify which pairs are consistently most variable
    print("  PAIRS WITH HIGHEST RANK VARIANCE IN ≥3 OF 4 MODELS:")
    threshold_per_model = {m: np.percentile(var_vectors[m], 75) for m in MODEL_ORDER}
    for i in range(32):
        n_above = sum(1 for m in MODEL_ORDER if var_vectors[m][i] >= threshold_per_model[m])
        if n_above >= 3:
            h1, h2 = pairs[i]
            n1 = atlas[str(h1)]['kw_name']
            n2 = atlas[str(h2)]['kw_name']
            flag = " ◄ 升↔无妄" if i == sw_idx else ""
            per_model = " ".join(f"{var_vectors[m][i]:6.1f}" for m in MODEL_ORDER)
            print(f"    Pair {i:2d} ({n1:10s}↔{n2:10s}): vars = [{per_model}] "
                  f"(above p75 in {n_above}/4){flag}")
    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    atlas, pairs, models = load_data()

    rank_mats, sw_idx = step1(models, pairs, atlas)
    avg_variances, per_model_var = step2(rank_mats, pairs, atlas, sw_idx)
    corrected_vars = step3(rank_mats, pairs, atlas, sw_idx)
    step4(rank_mats, pairs, atlas, sw_idx)

    # Final verdict
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()

    # Compare raw vs corrected rank for 升↔无妄
    raw_order = np.argsort(-avg_variances)
    raw_rank = np.where(raw_order == sw_idx)[0][0] + 1
    corr_order = np.argsort(-corrected_vars)
    corr_rank = np.where(corr_order == sw_idx)[0][0] + 1

    print(f"  升↔无妄 raw rank-variance rank: {raw_rank}/32")
    print(f"  升↔无妄 corrected rank-variance rank: {corr_rank}/32")
    print()

    if corr_rank <= 5:
        print("  → PAIR-SPECIFIC: 升↔无妄 bimodality survives marginal correction.")
        print("    The L3/L5 opposition is intrinsic to this pair, not a marginal artifact.")
    elif corr_rank <= 10:
        print("  → MODERATE: 升↔无妄 bimodality partially survives correction.")
        print("    Some of the effect is pair-specific, some is marginal.")
    else:
        print("  → MARGINAL ARTIFACT: 升↔无妄 bimodality is explained by position means.")
        print("    Many pairs show comparable or greater positional heterogeneity.")


if __name__ == "__main__":
    main()
