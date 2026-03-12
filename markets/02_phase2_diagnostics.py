#!/usr/bin/env python3
"""Phase 2 Diagnostics: 4×4 Cluster Characterization + Basis D.

Part 1: Collapse Basis A's 8 states into 4 clusters (by slow bits trend_8h × trend_48h).
Part 2: Basis D — timescale-matched orthogonal channels (tot_8h, trend_8h, realized_vol_8h).
"""

import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from scipy.spatial.distance import jensenshannon
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent / "datalog_2025-07-21_2026-02-20.csv"
OUTPUT_DIR = Path(__file__).parent
DOWNSAMPLE_MS = 300_000

NEEDED_COLS = [
    "timestamp", "price",
    "trend_1h", "trend_8h", "trend_48h",          # Basis A
    "tot_8h", "realized_vol_8h",                   # Basis D
    "cvd_div_1h",                                  # Side diagnostic
]

N_STATES = 8
N_CLUSTERS = 4
N_SUBPERIODS = 3
NEAR_ZERO_THRESH = 0.02

# Basis A cluster mapping: cluster = b₂*2 + b₁ (slow bits only)
# C0={S0,S1}: trend_48h<0, trend_8h<0  (b₂=0,b₁=0)
# C1={S2,S3}: trend_48h<0, trend_8h>0  (b₂=0,b₁=1)
# C2={S4,S5}: trend_48h>0, trend_8h<0  (b₂=1,b₁=0)
# C3={S6,S7}: trend_48h>0, trend_8h>0  (b₂=1,b₁=1)
STATE_TO_CLUSTER = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
CLUSTER_MEMBERS = {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7]}
CLUSTER_LABELS = {
    0: "C0 {S0,S1} 48h<0,8h<0",
    1: "C1 {S2,S3} 48h<0,8h>0",
    2: "C2 {S4,S5} 48h>0,8h<0",
    3: "C3 {S6,S7} 48h>0,8h>0",
}

# Basis D definition
BASIS_D = {
    "label": "Timescale-matched orthogonal (accel × vel × energy)",
    "bits": [
        ("tot_8h",          "zero",   0),
        ("trend_8h",        "zero",   0),
        ("realized_vol_8h", "median", None),
    ],
}


# ─── Helpers (from Phase 1) ─────────────────────────────────────────────────

def text_histogram(values, bins=10, width=40):
    counts, edges = np.histogram(values, bins=bins)
    max_count = counts.max()
    lines = []
    for i, c in enumerate(counts):
        bar_len = int(c / max_count * width) if max_count > 0 else 0
        lines.append(f"  [{edges[i]:+10.4f}, {edges[i+1]:+10.4f}) | {'█' * bar_len} {c}")
    return "\n".join(lines)


def compute_trigram(df, basis_def, medians=None):
    """Compute trigram state (0-7). medians: dict of feature→median for median-type thresholds."""
    bits = []
    for feat, thresh_type, _ in basis_def["bits"]:
        if thresh_type == "zero":
            bits.append((df[feat] > 0).astype(int))
        elif thresh_type == "median":
            m = medians[feat] if medians and feat in medians else df[feat].median()
            bits.append((df[feat] > m).astype(int))
    return bits[2] * 4 + bits[1] * 2 + bits[0]


def transition_matrix(states, n_states):
    T = np.zeros((n_states, n_states))
    for i in range(len(states) - 1):
        T[states[i], states[i + 1]] += 1
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return T / row_sums, T


def jump_chain(T):
    J = T.copy()
    np.fill_diagonal(J, 0)
    row_sums = J.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return J / row_sums


def eigenvalues_sorted(M):
    evals = np.linalg.eigvals(M)
    return evals[np.argsort(-np.abs(evals))]


def stationary_distribution(T):
    """Left eigenvector of T corresponding to eigenvalue 1."""
    evals, evecs = np.linalg.eig(T.T)
    idx = np.argmin(np.abs(evals - 1.0))
    pi = np.real(evecs[:, idx])
    pi = pi / pi.sum()
    return pi


def dwell_times(states, n_states):
    runs = {s: [] for s in range(n_states)}
    if len(states) == 0:
        return runs
    current = states[0]
    length = 1
    for i in range(1, len(states)):
        if states[i] == current:
            length += 1
        else:
            runs[current].append(length)
            current = states[i]
            length = 1
    runs[current].append(length)
    return runs


def format_matrix(M, decimals=4, labels=None):
    n = M.shape[0]
    if labels is None:
        labels = [f"S{i}" for i in range(n)]
    max_lbl = max(len(l) for l in labels)
    header = " " * (max_lbl + 1) + "".join(f"{l:>8}" for l in labels)
    lines = [header]
    for i in range(n):
        row = f"{labels[i]:<{max_lbl+1}}" + " ".join(f"{M[i,j]:.{decimals}f}" for j in range(n))
        lines.append(row)
    return "\n".join(lines)


def print_eigenvalues(T, J, label_T="T", label_J="J"):
    evals_T = eigenvalues_sorted(T)
    evals_J = eigenvalues_sorted(J)
    print(f"\n--- Eigenvalues ---")
    print(f"  {label_T}: {', '.join(f'{e.real:+.4f}' for e in evals_T)}")
    print(f"  {label_J}: {', '.join(f'{e.real:+.4f}' for e in evals_J)}")
    gaps_J = [abs(abs(evals_J[i]) - abs(evals_J[i + 1])) for i in range(len(evals_J) - 1)]
    print(f"  {label_J} magnitude gaps: {', '.join(f'{g:.4f}' for g in gaps_J)}")
    max_gap_idx = np.argmax(gaps_J)
    print(f"  Largest gap: between eigenvalue {max_gap_idx} and {max_gap_idx + 1} "
          f"(suggests ~{max_gap_idx + 1} natural clusters)")
    return evals_T, evals_J


def subperiod_stability(states, J_full, n_states, labels=None):
    print(f"\n--- Subperiod Stability ---")
    n = len(states)
    splits = [0, n // 3, 2 * n // 3, n]
    sub_Js = []
    for k in range(N_SUBPERIODS):
        sub = states[splits[k]:splits[k + 1]]
        sub_T, _ = transition_matrix(sub, n_states)
        sub_J = jump_chain(sub_T)
        sub_Js.append(sub_J)
        frob = np.linalg.norm(sub_J - J_full, 'fro')
        print(f"  Subperiod {k + 1} ({splits[k]}:{splits[k + 1]}): "
              f"‖J_sub - J_full‖_F = {frob:.4f}")

    # Zero-pattern stability
    total_off_diag = n_states * (n_states - 1)
    stable_zeros = 0
    unstable_cells = []
    for i in range(n_states):
        for j in range(n_states):
            if i == j:
                continue
            nz = [sub_Js[k][i, j] < NEAR_ZERO_THRESH for k in range(N_SUBPERIODS)]
            if all(nz):
                stable_zeros += 1
            elif any(nz) and not all(nz):
                unstable_cells.append((i, j))
    print(f"\n  Zero-pattern stability (<{NEAR_ZERO_THRESH * 100}% of row mass):")
    print(f"    {stable_zeros}/{total_off_diag} off-diagonal cells are stable near-zeros")
    if unstable_cells:
        li = labels or [str(x) for x in range(n_states)]
        print(f"    {len(unstable_cells)} cells shift:")
        for i, j in unstable_cells[:12]:
            vals = [f"{sub_Js[k][i, j]:.4f}" for k in range(N_SUBPERIODS)]
            print(f"      ({li[i]}→{li[j]}): [{', '.join(vals)}]")
        if len(unstable_cells) > 12:
            print(f"      ... and {len(unstable_cells) - 12} more")
    return sub_Js


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


# ═══════════════════════════════════════════════════════════════════════════
#  PART 1: 4×4 Cluster Analysis on Basis A
# ═══════════════════════════════════════════════════════════════════════════

def part1_cluster_analysis(df):
    print(f"\n{'=' * 70}")
    print("  PART 1: 4×4 Cluster Characterization (Basis A)")
    print(f"{'=' * 70}")

    # Compute Basis A 8-state sequence
    features_a = ["trend_1h", "trend_8h", "trend_48h"]
    mask = df[features_a].notna().all(axis=1)
    bdf = df[mask].copy()
    states_8 = ((bdf["trend_48h"] > 0).astype(int) * 4
                + (bdf["trend_8h"] > 0).astype(int) * 2
                + (bdf["trend_1h"] > 0).astype(int)).values
    states_4 = np.array([STATE_TO_CLUSTER[s] for s in states_8])

    clabels = [f"C{i}" for i in range(N_CLUSTERS)]
    print(f"\n  Cluster definitions:")
    for k, lbl in CLUSTER_LABELS.items():
        print(f"    {lbl}")
    print(f"  Working rows: {len(bdf)}")

    # ── 1. T₄ and J₄ ────────────────────────────────────────────────────
    T4, T4_raw = transition_matrix(states_4, N_CLUSTERS)
    J4 = jump_chain(T4)
    print(f"\n--- T₄ (full transition matrix) ---")
    print(format_matrix(T4, labels=clabels))
    print(f"\n--- J₄ (jump chain) ---")
    print(format_matrix(J4, labels=clabels))

    # ── 2. Eigenvalues ───────────────────────────────────────────────────
    print_eigenvalues(T4, J4, "T₄", "J₄")

    # ── 3. Stationary distribution ───────────────────────────────────────
    pi = stationary_distribution(T4)
    print(f"\n--- Stationary Distribution π₄ ---")
    for i in range(N_CLUSTERS):
        print(f"  C{i}: {pi[i]:.4f} ({pi[i] * 100:.2f}%)")
    # Concentration
    sorted_pi = np.sort(pi)[::-1]
    print(f"  Top-3 concentration: {sorted_pi[:3].sum():.4f} ({sorted_pi[:3].sum() * 100:.2f}%)")

    # ── 4. Zero structure ────────────────────────────────────────────────
    print(f"\n--- Zero Structure in J₄ (<2% of row mass) ---")
    for i in range(N_CLUSTERS):
        for j in range(N_CLUSTERS):
            if i == j:
                continue
            if J4[i, j] < NEAR_ZERO_THRESH:
                print(f"  C{i} → C{j}: {J4[i, j]:.4f} (near-zero)")

    # ── 5. Subperiod stability ───────────────────────────────────────────
    subperiod_stability(states_4, J4, N_CLUSTERS, clabels)

    # ── 6. Within-pair heterogeneity ─────────────────────────────────────
    print(f"\n--- Within-Pair Heterogeneity ---")
    # For each 8-state, compute its cross-cluster distribution when leaving its cluster
    T8, T8_raw = transition_matrix(states_8, N_STATES)
    J8 = jump_chain(T8)

    for c_idx, members in CLUSTER_MEMBERS.items():
        other_clusters = [c for c in range(N_CLUSTERS) if c != c_idx]
        print(f"\n  Cluster C{c_idx} = {{S{members[0]}, S{members[1]}}}:")
        profiles = []
        for m in members:
            # When state m transitions outside its cluster, what's the distribution over other clusters?
            cross_mass = {}
            total_cross = 0
            for j in range(N_STATES):
                target_cluster = STATE_TO_CLUSTER[j]
                if target_cluster != c_idx:
                    cross_mass.setdefault(target_cluster, 0)
                    cross_mass[target_cluster] += J8[m, j]
                    total_cross += J8[m, j]
            # Normalize
            profile = np.zeros(N_CLUSTERS)
            if total_cross > 0:
                for tc, mass in cross_mass.items():
                    profile[tc] = mass / total_cross
            profiles.append(profile)
            dist_str = "  ".join(f"C{c}={profile[c]:.4f}" for c in range(N_CLUSTERS))
            print(f"    S{m} → [{dist_str}]")

        # Jensen-Shannon divergence between the two profiles (only over other clusters)
        # Use the full 4-element profiles (cluster's own entry is 0 for both)
        jsd = jensenshannon(profiles[0], profiles[1])
        flag = " ⚠️ HETEROGENEOUS" if jsd > 0.1 else ""
        print(f"    JSD(S{members[0]}, S{members[1]}) = {jsd:.4f}{flag}")

    # Save J₄
    np.save(OUTPUT_DIR / "j4_basis_a.npy", J4)
    print(f"\n  Saved J₄ → {OUTPUT_DIR / 'j4_basis_a.npy'}")


# ═══════════════════════════════════════════════════════════════════════════
#  PART 2: Basis D — Full Phase 1 Diagnostics
# ═══════════════════════════════════════════════════════════════════════════

def part2_basis_d(df, vol_median):
    print(f"\n{'=' * 70}")
    print("  PART 2: Basis D — Timescale-matched orthogonal channels")
    print(f"{'=' * 70}")

    features_d = [b[0] for b in BASIS_D["bits"]]
    mask = df[features_d].notna().all(axis=1)
    bdf = df[mask].copy()
    n_dropped = len(df) - len(bdf)
    if n_dropped > 0:
        print(f"\n  Dropped {n_dropped} rows with NaN ({n_dropped / len(df) * 100:.1f}%)")
    print(f"  Working rows: {len(bdf)}")

    medians = {"realized_vol_8h": vol_median}

    # ── Side diagnostic: cvd_div_1h ──────────────────────────────────────
    print(f"\n--- Side Diagnostic: cvd_div_1h ---")
    cdv = bdf["cvd_div_1h"].dropna().values
    near_zero = np.mean(np.abs(cdv) < 0.01) * 100
    print(f"  mean={np.mean(cdv):.6f}  median={np.median(cdv):.6f}  "
          f"std={np.std(cdv):.6f}  skew={sp_stats.skew(cdv):.4f}")
    print(f"  within ±0.01 of 0: {near_zero:.2f}%")
    print(text_histogram(cdv))
    # Compare with tot_8h
    tot = bdf["tot_8h"].dropna().values
    print(f"\n  Comparison — tot_8h:")
    print(f"  mean={np.mean(tot):.6f}  median={np.median(tot):.6f}  "
          f"std={np.std(tot):.6f}  skew={sp_stats.skew(tot):.4f}")
    near_zero_tot = np.mean(np.abs(tot) < 0.01) * 100
    print(f"  within ±0.01 of 0: {near_zero_tot:.2f}%")
    print(text_histogram(tot))
    if near_zero < near_zero_tot:
        print(f"\n  ✓ cvd_div_1h has fewer values near threshold ({near_zero:.1f}% vs {near_zero_tot:.1f}%)")
    else:
        print(f"\n  ✗ tot_8h has fewer values near threshold ({near_zero_tot:.1f}% vs {near_zero:.1f}%)")

    # ── Feature Marginals ────────────────────────────────────────────────
    print(f"\n--- Feature Marginals (Basis D) ---")
    for feat, thresh_type, _ in BASIS_D["bits"]:
        vals = bdf[feat].values
        if thresh_type == "median":
            effective_thresh = medians.get(feat, np.median(vals))
            thresh_label = f"median ({effective_thresh:.6f})"
        else:
            effective_thresh = 0
            thresh_label = "0"
        near_thresh = np.mean(np.abs(vals - effective_thresh) < 0.01) * 100
        print(f"\n  {feat} (threshold: {thresh_label}):")
        print(f"    mean={np.mean(vals):.6f}  median={np.median(vals):.6f}  "
              f"std={np.std(vals):.6f}  skew={sp_stats.skew(vals):.4f}")
        print(f"    within ±0.01 of threshold: {near_thresh:.2f}%")
        print(text_histogram(vals))

    # ── Pairwise Correlation ─────────────────────────────────────────────
    print(f"\n--- Pairwise Pearson Correlation (binary series) ---")
    binary_bits = []
    bit_names = []
    for feat, thresh_type, _ in BASIS_D["bits"]:
        if thresh_type == "zero":
            binary_bits.append((bdf[feat] > 0).astype(int).values)
        else:
            binary_bits.append((bdf[feat] > medians.get(feat, bdf[feat].median())).astype(int).values)
        bit_names.append(feat)
    corr = np.corrcoef(binary_bits)
    header = "               " + "".join(f"{n:>18}" for n in bit_names)
    print(header)
    for i, name in enumerate(bit_names):
        row = f"  {name:<13}" + "".join(f"{corr[i, j]:>18.4f}" for j in range(len(bit_names)))
        print(row)
    # Check independence
    max_off_diag = max(abs(corr[i, j]) for i in range(3) for j in range(3) if i != j)
    if max_off_diag < 0.3:
        print(f"  ✓ All pairwise |r| < 0.3 (max = {max_off_diag:.4f})")
    else:
        print(f"  ⚠️ Max pairwise |r| = {max_off_diag:.4f} (above 0.3 threshold)")

    # ── Compute trigram states ───────────────────────────────────────────
    states = compute_trigram(bdf, BASIS_D, medians).values.astype(int)

    # ── State Frequencies ────────────────────────────────────────────────
    print(f"\n--- State Frequencies ---")
    print(f"  {'State':>5}  {'Count':>8}  {'Pct':>7}  Bits (vol,trend,accel)")
    for s in range(N_STATES):
        c = np.sum(states == s)
        b2, b1, b0 = (s >> 2) & 1, (s >> 1) & 1, s & 1
        desc = f"vol={'H' if b2 else 'L'} trend={'↑' if b1 else '↓'} accel={'↑' if b0 else '↓'}"
        print(f"  S{s:<4}  {c:>8}  {c / len(states) * 100:>6.2f}%  ({b2}{b1}{b0}) {desc}")

    # ── Transition Count ─────────────────────────────────────────────────
    changes = np.sum(states[1:] != states[:-1])
    total = len(states) - 1
    print(f"\n--- Transitions ---")
    print(f"  Total state changes: {changes} (out of {total} bars = {changes / total * 100:.2f}%)")

    # ── Dwell Times ──────────────────────────────────────────────────────
    print(f"\n--- Dwell Times (5-min bars) ---")
    runs = dwell_times(states, N_STATES)
    print(f"  {'State':>5}  {'Runs':>6}  {'Mean':>8}  {'Median':>8}  {'Max':>8}  {'CV':>6}  {'Flag':>10}")
    for s in range(N_STATES):
        r = runs[s]
        if not r:
            print(f"  S{s:<4}  {'N/A':>6}")
            continue
        r = np.array(r)
        mean_r = np.mean(r)
        cv = np.std(r) / mean_r if mean_r > 0 else 0
        flag = "HEAVY-TAIL" if cv > 1 else ""
        print(f"  S{s:<4}  {len(r):>6}  {mean_r:>8.1f}  {np.median(r):>8.1f}  "
              f"{np.max(r):>8}  {cv:>6.2f}  {flag:>10}")

    # ── T₈ and J₈ ────────────────────────────────────────────────────────
    T, _ = transition_matrix(states, N_STATES)
    J = jump_chain(T)
    print(f"\n--- T₈ (full transition matrix) ---")
    print(format_matrix(T))
    print(f"\n--- J₈ (jump chain) ---")
    print(format_matrix(J))

    # ── Eigenvalues ──────────────────────────────────────────────────────
    print_eigenvalues(T, J, "T₈", "J₈")

    # ── Subperiod Stability ──────────────────────────────────────────────
    subperiod_stability(states, J, N_STATES)

    # ── Complement Structure Test ────────────────────────────────────────
    print(f"\n--- Complement Structure Test ---")
    print("  Under (3,5) equivariance: complement pairs should have similar")
    print("  transition behavior when relabeled by complement map x ↦ x⊕7.")
    complement_pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    for s_a, s_b in complement_pairs:
        b_a = f"{s_a:03b}"
        b_b = f"{s_b:03b}"
        print(f"\n  S{s_a} ({b_a}) vs S{s_b} ({b_b}):")
        # Print J₈ rows side by side
        row_a_str = "  ".join(f"S{j}={J[s_a, j]:.4f}" for j in range(N_STATES))
        row_b_str = "  ".join(f"S{j}={J[s_b, j]:.4f}" for j in range(N_STATES))
        print(f"    J₈[S{s_a}]: {row_a_str}")
        print(f"    J₈[S{s_b}]: {row_b_str}")

        # For JSD comparison: relabel s_b's row under complement map
        # Column j of s_a corresponds to column j⊕7 of s_b
        row_a = J[s_a].copy()
        row_b_relabeled = np.zeros(N_STATES)
        for j in range(N_STATES):
            row_b_relabeled[j] = J[s_b, j ^ 7]

        # Handle zero rows
        if row_a.sum() == 0 or row_b_relabeled.sum() == 0:
            print(f"    JSD: undefined (zero row)")
            continue

        jsd = jensenshannon(row_a, row_b_relabeled)
        flag = " (similar ✓)" if jsd < 0.1 else " (different ✗)" if jsd > 0.3 else ""
        print(f"    Relabeled J₈[S{s_b}]: {'  '.join(f'S{j}={row_b_relabeled[j]:.4f}' for j in range(N_STATES))}")
        print(f"    JSD = {jsd:.4f}{flag}")

    # Save
    np.save(OUTPUT_DIR / "j8_basis_d.npy", J)
    print(f"\n  Saved J₈ → {OUTPUT_DIR / 'j8_basis_d.npy'}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()
    vol_median = df["realized_vol_8h"].median()
    print(f"\nGlobal realized_vol_8h median: {vol_median:.6f}")

    part1_cluster_analysis(df)
    part2_basis_d(df, vol_median)

    print(f"\n{'=' * 70}")
    print("  Phase 2 diagnostics complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
