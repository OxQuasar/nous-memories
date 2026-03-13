#!/usr/bin/env python3
"""Phase 7: Transition-Level Clustering at the 8-State Level.

Tests whether transitions between 8 observable states decompose into
a small number of qualitative types. If K=5, flags for I Ching surjection test.

Basis A: trend_1h × trend_8h × trend_48h → 8 states S0–S7.
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path("/home/quasar/nous/memories/markets/datalog_2025-07-21_2026-02-20.csv")
OUTPUT_DIR = Path("/home/quasar/nous/memories/markets")
DOWNSAMPLE_MS = 300_000
N_STATES = 8

NEEDED_COLS = ["timestamp", "price", "trend_1h", "trend_8h", "trend_48h"]

# K=4 macro-regime mapping (from Phase 2)
STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
MACRO_LABELS = {0: "C0 bear", 1: "C1 reversal", 2: "C2 pullback", 3: "C3 bull"}

# J₄ structural zeros (from Phase 2): stage-skipping forbidden
# C0↛C3, C1↛C2, C2↛C1, C3↛C0
FORBIDDEN_PAIRS = {(0, 3), (1, 2), (2, 1), (3, 0)}

K_RANGE = range(2, 9)
N_GAP_REFS = 20  # reference datasets for gap statistic


# ─── Data Loading ────────────────────────────────────────────────────────────

def load_and_downsample():
    print("Loading and downsampling to 5-minute bars...")
    chunks = []
    for chunk in pd.read_csv(DATA_PATH, usecols=NEEDED_COLS, chunksize=500_000):
        chunk["bar"] = chunk["timestamp"] // DOWNSAMPLE_MS
        chunks.append(chunk.groupby("bar").last().reset_index())
    df = pd.concat(chunks, ignore_index=True)
    df = df.groupby("bar").last().reset_index()
    df = df.sort_values("bar").reset_index(drop=True)
    print(f"  Rows: {len(df)}")
    return df


# ─── Helpers ─────────────────────────────────────────────────────────────────

def compute_states(df):
    """Basis A: trend_48h(bit2) × trend_8h(bit1) × trend_1h(bit0)."""
    mask = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    states = ((bdf["trend_48h"] > 0).astype(int) * 4
              + (bdf["trend_8h"] > 0).astype(int) * 2
              + (bdf["trend_1h"] > 0).astype(int)).values
    return bdf, states


def transition_matrix(states, n=N_STATES):
    T = np.zeros((n, n))
    for i in range(len(states) - 1):
        T[states[i], states[i + 1]] += 1
    raw = T.copy()
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return T / row_sums, raw


def jump_chain(T):
    J = T.copy()
    np.fill_diagonal(J, 0)
    row_sums = J.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return J / row_sums


def format_matrix(M, decimals=4, labels=None):
    n = M.shape[0]
    labels = labels or [f"S{i}" for i in range(n)]
    w = max(len(l) for l in labels)
    header = " " * (w + 1) + "".join(f"{l:>9}" for l in labels)
    lines = [header]
    for i in range(n):
        row = f"{labels[i]:<{w+1}}" + " ".join(f"{M[i,j]:>8.{decimals}f}" for j in range(n))
        lines.append(row)
    return "\n".join(lines)


def gap_statistic(X, k_range, n_refs=N_GAP_REFS):
    """Compute gap statistic for K-means clustering."""
    rng = np.random.RandomState(42)
    gaps = []
    sks = []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        wk = km.inertia_
        # Reference datasets: uniform over bounding box
        ref_wks = []
        for _ in range(n_refs):
            X_ref = rng.uniform(X.min(axis=0), X.max(axis=0), size=X.shape)
            km_ref = KMeans(n_clusters=k, n_init=5, random_state=42).fit(X_ref)
            ref_wks.append(np.log(km_ref.inertia_))
        ref_mean = np.mean(ref_wks)
        ref_std = np.std(ref_wks) * np.sqrt(1 + 1 / n_refs)
        gaps.append(ref_mean - np.log(wk))
        sks.append(ref_std)
    # Optimal K: smallest k where gap(k) >= gap(k+1) - s(k+1)
    gaps = np.array(gaps)
    sks = np.array(sks)
    opt_k = k_range[-1]
    for i in range(len(gaps) - 1):
        if gaps[i] >= gaps[i + 1] - sks[i + 1]:
            opt_k = list(k_range)[i]
            break
    return gaps, sks, opt_k


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 1: Compute J₈
# ═══════════════════════════════════════════════════════════════════════════

def step1_compute_j8(states):
    print("\n" + "=" * 70)
    print("  STEP 1: Compute J₈ for Basis A")
    print("=" * 70)

    T, T_raw = transition_matrix(states)
    J = jump_chain(T)

    print("\n--- J₈ (jump chain) ---")
    print(format_matrix(J))

    print("\n--- Count matrix (off-diagonal transitions only) ---")
    counts = T_raw.copy()
    np.fill_diagonal(counts, 0)
    print(format_matrix(counts, decimals=0, labels=[f"S{i}" for i in range(N_STATES)]))

    print(f"\n  Total off-diagonal transitions: {int(counts.sum())}")
    # Print the 56 off-diagonal probabilities
    print("\n--- All 56 off-diagonal transition probabilities ---")
    for i in range(N_STATES):
        for j in range(N_STATES):
            if i == j:
                continue
            print(f"  {i}→{j}: prob={J[i,j]:.4f}  count={int(counts[i,j])}")

    return J, counts


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 2: Complement symmetry check
# ═══════════════════════════════════════════════════════════════════════════

def step2_complement_symmetry(J):
    print("\n" + "=" * 70)
    print("  STEP 2: Complement Symmetry Check at J₈ Level (Basis A)")
    print("=" * 70)
    print("  Complement map: x ↦ x⊕7")
    print("  Threshold: JSD < 0.1 means symmetry holds\n")

    complement_pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    jsds = []
    all_pass = True

    for s_a, s_b in complement_pairs:
        # Row of s_a
        row_a = J[s_a].copy()
        # Row of s_b, relabeled: column j of s_a ↔ column j⊕7 of s_b
        row_b_relabeled = np.array([J[s_b, j ^ 7] for j in range(N_STATES)])

        jsd = jensenshannon(row_a, row_b_relabeled)
        jsds.append(jsd)
        status = "✓ PASS" if jsd < 0.1 else "✗ FAIL"
        if jsd >= 0.1:
            all_pass = False

        print(f"  (S{s_a}, S{s_b}): JSD = {jsd:.4f}  [{status}]")
        print(f"    J₈[S{s_a}]: {np.array2string(row_a, precision=4, separator=', ')}")
        print(f"    J₈[S{s_b}] relabeled: {np.array2string(row_b_relabeled, precision=4, separator=', ')}")

    print(f"\n  Overall: {'COMPLEMENT SYMMETRY HOLDS' if all_pass else 'COMPLEMENT SYMMETRY FAILS'}")
    print(f"  Mean JSD: {np.mean(jsds):.4f}, Max JSD: {np.max(jsds):.4f}")
    return all_pass, jsds


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 3: Transition feature vectors
# ═══════════════════════════════════════════════════════════════════════════

def step3_transition_features(states, prices, J, counts):
    print("\n" + "=" * 70)
    print("  STEP 3: Transition Feature Vectors")
    print("=" * 70)

    n = len(states)

    # Compute log returns per bar
    log_returns = np.log(prices[1:] / prices[:-1])

    # Compute per-transition: mean return at transition, mean dwell before
    # Identify transition bars and their dwell times
    transition_returns = {(i, j): [] for i in range(N_STATES) for j in range(N_STATES) if i != j}
    transition_dwells = {(i, j): [] for i in range(N_STATES) for j in range(N_STATES) if i != j}

    # Track dwell times
    current_state = states[0]
    dwell = 1
    for t in range(1, n):
        if states[t] != states[t - 1]:
            i, j = states[t - 1], states[t]
            transition_returns[(i, j)].append(log_returns[t - 1])
            transition_dwells[(i, j)].append(dwell)
            dwell = 1
        else:
            dwell += 1

    # Build feature matrix for 56 transitions
    transitions = []
    feat_matrix = []
    for i in range(N_STATES):
        for j in range(N_STATES):
            if i == j:
                continue
            prob = J[i, j]
            count = counts[i, j]
            rets = transition_returns[(i, j)]
            dwells = transition_dwells[(i, j)]
            mean_ret = np.mean(rets) if rets else 0.0
            mean_dwell = np.mean(dwells) if dwells else 0.0
            transitions.append((i, j))
            feat_matrix.append([prob, count, mean_ret, mean_dwell])

    feat_matrix = np.array(feat_matrix)
    feat_names = ["prob", "count", "mean_return", "mean_dwell"]

    print(f"\n  56 transition feature vectors (4 features each):")
    print(f"  {'Transition':>12}  {'Prob':>8}  {'Count':>8}  {'Mean Ret':>12}  {'Mean Dwell':>10}")
    for k, (i, j) in enumerate(transitions):
        print(f"  {i}→{j:>2}         {feat_matrix[k,0]:>8.4f}  {feat_matrix[k,1]:>8.0f}  "
              f"{feat_matrix[k,2]:>12.6f}  {feat_matrix[k,3]:>10.1f}")

    return transitions, feat_matrix, feat_names


def merge_complement_pairs(transitions, feat_matrix):
    """Merge complement-paired transitions by averaging features."""
    print("\n--- Merging complement pairs ---")
    # Complement map: i→j pairs with (7-i)→(7-j)
    merged = {}
    merged_labels = []
    merged_feats = []

    for k, (i, j) in enumerate(transitions):
        ci, cj = 7 - i, 7 - j
        key = tuple(sorted([(i, j), (ci, cj)]))
        if key not in merged:
            merged[key] = []
        merged[key].append(k)

    for key in sorted(merged.keys()):
        indices = merged[key]
        avg_feat = feat_matrix[indices].mean(axis=0)
        merged_feats.append(avg_feat)
        pairs = [f"{transitions[k][0]}→{transitions[k][1]}" for k in indices]
        merged_labels.append(" / ".join(pairs))

    merged_feats = np.array(merged_feats)
    print(f"  {len(merged_labels)} merged transition groups (from 56 raw)")

    return merged_labels, merged_feats


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 4: Unsupervised clustering
# ═══════════════════════════════════════════════════════════════════════════

def step4_clustering(transitions, feat_matrix, feat_names, merged_labels, merged_feats, sym_holds):
    print("\n" + "=" * 70)
    print("  STEP 4: Unsupervised Clustering")
    print("=" * 70)

    # Decide whether to use merged or raw
    if sym_holds:
        X_raw = merged_feats
        labels_raw = merged_labels
        print(f"  Using MERGED data ({len(X_raw)} points) — complement symmetry holds")
    else:
        X_raw = feat_matrix
        labels_raw = [f"{i}→{j}" for i, j in transitions]
        print(f"  Using RAW data ({len(X_raw)} points) — complement symmetry fails")

    results = {}

    for version, feat_idx, version_label in [
        ("prob_only", [0], "(a) Probability-only"),
        ("full_4feat", [0, 1, 2, 3], "(b) Full 4-feature"),
    ]:
        print(f"\n{'─' * 60}")
        print(f"  {version_label}")
        print(f"{'─' * 60}")

        X = X_raw[:, feat_idx]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Gap statistic
        gaps, sks, gap_k = gap_statistic(X_scaled, K_RANGE)
        print(f"\n  Gap statistic:")
        for ki, k in enumerate(K_RANGE):
            print(f"    K={k}: gap={gaps[ki]:.4f} ± {sks[ki]:.4f}")
        print(f"  → Optimal K (gap): {gap_k}")

        # Silhouette
        sil_scores = {}
        for k in K_RANGE:
            if k >= len(X_scaled):
                break
            km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_scaled)
            if k > 1:
                sil = silhouette_score(X_scaled, km.labels_)
                sil_scores[k] = sil
        print(f"\n  Silhouette scores:")
        for k, s in sil_scores.items():
            print(f"    K={k}: {s:.4f}")
        sil_k = max(sil_scores, key=sil_scores.get) if sil_scores else 2
        print(f"  → Optimal K (silhouette): {sil_k}")

        # BIC from GMM
        bic_scores = {}
        for k in K_RANGE:
            if k >= len(X_scaled):
                break
            try:
                gmm = GaussianMixture(n_components=k, n_init=5, random_state=42).fit(X_scaled)
                bic_scores[k] = gmm.bic(X_scaled)
            except Exception:
                pass
        print(f"\n  BIC (GMM):")
        for k, b in bic_scores.items():
            print(f"    K={k}: {b:.2f}")
        bic_k = min(bic_scores, key=bic_scores.get) if bic_scores else 2
        print(f"  → Optimal K (BIC): {bic_k}")

        results[version] = {
            "gap_k": gap_k,
            "sil_k": sil_k,
            "bic_k": bic_k,
            "gaps": gaps,
            "sks": sks,
            "sil_scores": sil_scores,
            "bic_scores": bic_scores,
            "X_scaled": X_scaled,
            "labels_raw": labels_raw,
        }

    # Check if (a) and (b) agree
    pa, pb = results["prob_only"], results["full_4feat"]
    agreed = (pa["gap_k"] == pb["gap_k"] and pa["sil_k"] == pb["sil_k"])
    print(f"\n  Do (a) and (b) agree?")
    print(f"    Gap: (a)={pa['gap_k']}, (b)={pb['gap_k']}")
    print(f"    Silhouette: (a)={pa['sil_k']}, (b)={pb['sil_k']}")
    print(f"    BIC: (a)={pa['bic_k']}, (b)={pb['bic_k']}")
    if agreed:
        print(f"    → YES — non-probability features add no clustering structure")
    else:
        print(f"    → NO — features contribute additional structure")

    # Plot spectral gaps
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for vi, (version, label) in enumerate([("prob_only", "Prob-only"), ("full_4feat", "Full 4-feat")]):
        r = results[version]
        axes[0].plot(list(K_RANGE), r["gaps"], marker="o", label=label)
        axes[0].fill_between(list(K_RANGE),
                             r["gaps"] - r["sks"], r["gaps"] + r["sks"], alpha=0.2)

        ks = sorted(r["sil_scores"].keys())
        axes[1].plot(ks, [r["sil_scores"][k] for k in ks], marker="o", label=label)

        ks = sorted(r["bic_scores"].keys())
        axes[2].plot(ks, [r["bic_scores"][k] for k in ks], marker="o", label=label)

    axes[0].set_xlabel("K"); axes[0].set_ylabel("Gap"); axes[0].set_title("Gap Statistic")
    axes[1].set_xlabel("K"); axes[1].set_ylabel("Silhouette"); axes[1].set_title("Silhouette Score")
    axes[2].set_xlabel("K"); axes[2].set_ylabel("BIC"); axes[2].set_title("BIC (GMM)")
    for ax in axes:
        ax.legend()
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_clustering_metrics.png", dpi=150)
    print(f"\n  Saved plot → {OUTPUT_DIR / '07_clustering_metrics.png'}")

    return results


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 5: K=4 null model comparison
# ═══════════════════════════════════════════════════════════════════════════

def step5_k4_null(transitions, feat_matrix, sym_holds, merged_labels, merged_feats):
    print("\n" + "=" * 70)
    print("  STEP 5: K=4-Implied Null Model Comparison")
    print("=" * 70)

    # Classify each of 56 transitions by K=4 structure
    groups = {}
    group_labels = []

    for k, (i, j) in enumerate(transitions):
        ci = STATE_TO_MACRO[i]
        cj = STATE_TO_MACRO[j]

        # (a) Forbidden?
        forbidden = (ci, cj) in FORBIDDEN_PAIRS

        # (b) Within-macro-pair? (same C_k, just fast-bit flip)
        within = (ci == cj)  # impossible since i≠j within same 8-state, but ci could == cj
        # Actually: if ci == cj, they're in the same macro-pair (fast-bit flip within cluster)
        # This happens for transitions like S0→S1 (both in C0)

        if forbidden:
            group = "forbidden"
        elif within:
            group = "within_pair"
        else:
            # Cross-macro: determine forward vs backward in the cycle
            # Cycle: C0→C1→C3→C2→C0
            cycle_order = {0: 0, 1: 1, 3: 2, 2: 3}  # position in directed cycle
            pos_i = cycle_order[ci]
            pos_j = cycle_order[cj]
            forward = (pos_j - pos_i) % 4 == 1
            group = "cross_forward" if forward else "cross_backward"

        groups.setdefault(group, []).append(k)
        group_labels.append(group)

    print("\n  K=4-implied transition grouping:")
    for g, indices in sorted(groups.items()):
        trans_str = ", ".join(f"{transitions[k][0]}→{transitions[k][1]}" for k in indices[:8])
        if len(indices) > 8:
            trans_str += f" ... ({len(indices)} total)"
        print(f"    {g}: n={len(indices)}  [{trans_str}]")

    n_groups_k4 = len(groups)
    print(f"\n  Number of K=4-implied groups: {n_groups_k4}")

    # Compute BIC for K=4-implied grouping using GMM with fixed assignments
    # Use merged or raw data based on symmetry
    if sym_holds:
        X = merged_feats
        labels = merged_labels
        # Need to remap group assignments for merged data
        # For merged transitions, take the group of the first transition in each pair
        merged_groups = {}
        merged_idx = 0
        seen = set()
        group_assignments = []
        for k, (i, j) in enumerate(transitions):
            ci, cj = 7 - i, 7 - j
            key = tuple(sorted([(i, j), (ci, cj)]))
            if key not in seen:
                seen.add(key)
                group_assignments.append(group_labels[k])
                merged_idx += 1
        X_for_bic = X
    else:
        X_for_bic = feat_matrix
        group_assignments = group_labels

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_for_bic)

    # Encode group assignments as integers
    unique_groups = sorted(set(group_assignments))
    group_to_int = {g: i for i, g in enumerate(unique_groups)}
    y = np.array([group_to_int[g] for g in group_assignments])

    print(f"\n  Group assignment counts (for BIC computation):")
    for g in unique_groups:
        c = np.sum(y == group_to_int[g])
        print(f"    {g}: {c}")

    # Fit Gaussians per group, compute BIC
    n_samples, n_features = X_scaled.shape
    n_groups = len(unique_groups)
    log_likelihood = 0
    n_params = 0

    for gi in range(n_groups):
        mask = y == gi
        X_g = X_scaled[mask]
        n_g = len(X_g)
        if n_g == 0:
            continue
        if n_g == 1:
            # Single point: use global variance
            mu = X_g[0]
            cov = np.eye(n_features)
        else:
            mu = X_g.mean(axis=0)
            cov = np.cov(X_g.T) if n_features > 1 else np.array([[np.var(X_g)]])
            # Regularize
            cov += np.eye(n_features) * 1e-6

        # Log-likelihood contribution
        from scipy.stats import multivariate_normal
        try:
            ll = multivariate_normal.logpdf(X_g, mean=mu, cov=cov).sum()
        except Exception:
            ll = -1e10
        log_likelihood += ll
        # Parameters: n_features (mean) + n_features*(n_features+1)/2 (cov) + 1 (weight)
        n_params += n_features + n_features * (n_features + 1) // 2

    # Add weight parameters (n_groups - 1 free weights)
    n_params += n_groups - 1
    bic_k4_implied = n_params * np.log(n_samples) - 2 * log_likelihood
    print(f"\n  K=4-implied BIC: {bic_k4_implied:.2f}")
    print(f"    log-likelihood: {log_likelihood:.2f}")
    print(f"    n_params: {n_params}")

    return n_groups_k4, bic_k4_implied, group_assignments, unique_groups


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 6: Decision
# ═══════════════════════════════════════════════════════════════════════════

def step6_decision(results, n_groups_k4, bic_k4_implied, transitions, feat_matrix,
                   merged_labels, merged_feats, sym_holds, group_assignments, unique_groups):
    print("\n" + "=" * 70)
    print("  STEP 6: Decision")
    print("=" * 70)

    # Use full 4-feature results as primary
    r = results["full_4feat"]
    # Determine the consensus optimal K
    candidates = [r["gap_k"], r["sil_k"], r["bic_k"]]
    from collections import Counter
    k_counts = Counter(candidates)
    opt_k = k_counts.most_common(1)[0][0]

    print(f"\n  Consensus from full 4-feature clustering:")
    print(f"    Gap statistic K: {r['gap_k']}")
    print(f"    Silhouette K: {r['sil_k']}")
    print(f"    BIC (GMM) K: {r['bic_k']}")
    print(f"    → Consensus K: {opt_k}")

    # Get BIC at optimal K from GMM
    bic_opt = r["bic_scores"].get(opt_k, float("inf"))
    print(f"\n  BIC comparison:")
    print(f"    Unsupervised K={opt_k} BIC: {bic_opt:.2f}")
    print(f"    K=4-implied ({n_groups_k4} groups) BIC: {bic_k4_implied:.2f}")

    # Fit cluster assignments at optimal K
    if sym_holds:
        X = merged_feats
        labels = merged_labels
    else:
        X = feat_matrix
        labels = [f"{i}→{j}" for i, j in transitions]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    gmm = GaussianMixture(n_components=opt_k, n_init=10, random_state=42).fit(X_scaled)
    cluster_assignments = gmm.predict(X_scaled)

    # Print cluster membership and mean features
    print(f"\n  Cluster assignments at K={opt_k}:")
    feat_names = ["prob", "count", "mean_return", "mean_dwell"]
    for c in range(opt_k):
        mask = cluster_assignments == c
        members = [labels[i] for i in range(len(labels)) if mask[i]]
        mean_feats = X[mask].mean(axis=0)
        print(f"\n  Cluster {c} (n={mask.sum()}):")
        print(f"    Mean features: " + "  ".join(f"{feat_names[fi]}={mean_feats[fi]:.4f}"
                                                  for fi in range(len(feat_names))))
        # Print K=4 group composition
        if sym_holds:
            cluster_groups = [group_assignments[i] for i in range(len(group_assignments)) if mask[i]]
        else:
            cluster_groups = [group_assignments[i] for i in range(len(group_assignments)) if mask[i]]
        from collections import Counter as Ctr
        gc = Ctr(cluster_groups)
        print(f"    K=4 group composition: " + ", ".join(f"{g}={n}" for g, n in gc.most_common()))
        # Show members (truncated)
        shown = members[:6]
        extra = f" ... +{len(members)-6} more" if len(members) > 6 else ""
        print(f"    Members: {', '.join(shown)}{extra}")

    # Decision
    print(f"\n{'─' * 60}")
    if opt_k == 5 and bic_opt < bic_k4_implied:
        print(f"  ★ K=5 FOUND with lower BIC than K=4-implied!")
        print(f"  → FLAG FOR I CHING SURJECTION TEST (next phase)")
    else:
        print(f"  Natural K={opt_k}")
        if bic_opt < bic_k4_implied:
            print(f"  Unsupervised K={opt_k} has LOWER BIC than K=4-implied grouping")
        else:
            print(f"  K=4-implied grouping has LOWER BIC (better fit)")

        if opt_k < 5:
            print(f"  → Transition structure is COARSER than 5 types")
        elif opt_k > 5:
            print(f"  → Transition structure has FINER sub-decomposition than 5")
        print(f"  → STOP. No I Ching surjection test needed.")

    # Summary table
    rp = results["prob_only"]
    print(f"\n{'─' * 60}")
    print(f"  SUMMARY TABLE")
    print(f"{'─' * 60}")
    print(f"  {'Metric':<30}  {'Prob-only':>10}  {'Full 4-feat':>12}")
    print(f"  {'K (gap statistic)':<30}  {rp['gap_k']:>10}  {r['gap_k']:>12}")
    print(f"  {'K (silhouette)':<30}  {rp['sil_k']:>10}  {r['sil_k']:>12}")
    print(f"  {'K (BIC/GMM)':<30}  {rp['bic_k']:>10}  {r['bic_k']:>12}")
    print(f"  {'BIC at optimal K':<30}  {rp['bic_scores'].get(rp['bic_k'], 'N/A'):>10}  {bic_opt:>12.2f}")
    print(f"  {'K=4-implied BIC':<30}  {'':>10}  {bic_k4_implied:>12.2f}")
    print(f"  {'K=4-implied n_groups':<30}  {'':>10}  {n_groups_k4:>12}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()
    bdf, states = compute_states(df)
    prices = bdf["price"].values

    # Step 1: J₈ and counts
    J, counts = step1_compute_j8(states)

    # Step 2: Complement symmetry
    sym_holds, jsds = step2_complement_symmetry(J)

    # Step 3: Transition feature vectors
    transitions, feat_matrix, feat_names = step3_transition_features(states, prices, J, counts)

    # Merge if symmetry holds
    merged_labels, merged_feats = merge_complement_pairs(transitions, feat_matrix)

    # Step 4: Unsupervised clustering
    results = step4_clustering(transitions, feat_matrix, feat_names,
                               merged_labels, merged_feats, sym_holds)

    # Step 5: K=4 null model
    n_groups_k4, bic_k4_implied, group_assignments, unique_groups = step5_k4_null(
        transitions, feat_matrix, sym_holds, merged_labels, merged_feats)

    # Step 6: Decision
    step6_decision(results, n_groups_k4, bic_k4_implied, transitions, feat_matrix,
                   merged_labels, merged_feats, sym_holds, group_assignments, unique_groups)

    print(f"\n{'=' * 70}")
    print("  Phase 7 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
