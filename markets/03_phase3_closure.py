#!/usr/bin/env python3
"""Phase 3: Complement-Pair 4×4 + (3,5) Formal Closure.

Part 1: Collapse Basis D's 8 states into 4 complement-pair clusters.
Part 2: Exhaustive search over all 240 complement-equivariant surjections 8→5.
"""

import numpy as np
import pandas as pd
from itertools import product
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent / "datalog_2025-07-21_2026-02-20.csv"
OUTPUT_DIR = Path(__file__).parent
DOWNSAMPLE_MS = 300_000

NEEDED_COLS = ["timestamp", "tot_8h", "trend_8h", "realized_vol_8h"]

N_STATES = 8
N_SUBPERIODS = 3
NEAR_ZERO_THRESH = 0.02

# Complement-pair clusters for Basis D
# P0 = {S0(000), S7(111)}, P1 = {S1(001), S6(110)},
# P2 = {S2(010), S5(101)}, P3 = {S3(011), S4(100)}
COMPLEMENT_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]
STATE_TO_CPAIR = {}
for idx, (a, b) in enumerate(COMPLEMENT_PAIRS):
    STATE_TO_CPAIR[a] = idx
    STATE_TO_CPAIR[b] = idx
N_CPAIRS = 4

CPAIR_LABELS = [
    "P0 {S0,S7} calm↓decel∪vol↑accel",
    "P1 {S1,S6} calm↓accel∪vol↑decel",
    "P2 {S2,S5} calm↑decel∪vol↓accel",
    "P3 {S3,S4} calm↑accel∪vol↓decel",
]

BASIS_D = {
    "bits": [
        ("tot_8h",          "zero",   0),
        ("trend_8h",        "zero",   0),
        ("realized_vol_8h", "median", None),
    ],
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

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
    evals, evecs = np.linalg.eig(T.T)
    idx = np.argmin(np.abs(evals - 1.0))
    pi = np.real(evecs[:, idx])
    return pi / pi.sum()


def format_matrix(M, decimals=4, labels=None):
    n = M.shape[0]
    if labels is None:
        labels = [f"S{i}" for i in range(n)]
    max_lbl = max(len(l) for l in labels)
    header = " " * (max_lbl + 1) + "".join(f"{l:>8}" for l in labels)
    lines = [header]
    for i in range(n):
        row = f"{labels[i]:<{max_lbl + 1}}" + " ".join(f"{M[i, j]:.{decimals}f}" for j in range(n))
        lines.append(row)
    return "\n".join(lines)


def print_eigenvalues(T, J, label_T, label_J):
    evals_T = eigenvalues_sorted(T)
    evals_J = eigenvalues_sorted(J)
    print(f"\n--- Eigenvalues ---")
    print(f"  {label_T}: {', '.join(f'{e.real:+.4f}' for e in evals_T)}")
    print(f"  {label_J}: {', '.join(f'{e.real:+.4f}' for e in evals_J)}")
    gaps = [abs(abs(evals_J[i]) - abs(evals_J[i + 1])) for i in range(len(evals_J) - 1)]
    print(f"  {label_J} magnitude gaps: {', '.join(f'{g:.4f}' for g in gaps)}")
    max_gap_idx = np.argmax(gaps)
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
    return sub_Js


def lumpability_error(T, pi, partition, n_classes):
    """Compute lumpability error for a partition of states into classes.

    E(f) = Σ_i Σ_{x,x': f(x)=f(x')=i} Σ_j |Σ_{y:f(y)=j} T(x,y) − Σ_{y:f(y)=j} T(x',y)|²

    partition: dict mapping state → class (or array).
    """
    n = T.shape[0]
    error = 0.0
    for c in range(n_classes):
        members = [s for s in range(n) if partition[s] == c]
        if len(members) < 2:
            continue
        # For each pair of members, compute transition disagreement
        # First, compute aggregated transition probabilities to each class
        agg = np.zeros((len(members), n_classes))
        for mi, m in enumerate(members):
            for s in range(n):
                agg[mi, partition[s]] += T[m, s]
        # Compare all pairs
        for mi in range(len(members)):
            for mj in range(mi + 1, len(members)):
                error += np.sum((agg[mi] - agg[mj]) ** 2)
    return error


def lumped_transition_matrix(T, pi, partition, n_classes):
    """Compute lumped transition matrix T_K(i,j) = Σ_{x:f(x)=i} π(x)/π_i * Σ_{y:f(y)=j} T(x,y)."""
    n = T.shape[0]
    T_K = np.zeros((n_classes, n_classes))
    pi_class = np.zeros(n_classes)
    for s in range(n):
        pi_class[partition[s]] += pi[s]

    for i in range(n_classes):
        if pi_class[i] == 0:
            continue
        members_i = [s for s in range(n) if partition[s] == i]
        for j in range(n_classes):
            members_j = [s for s in range(n) if partition[s] == j]
            for x in members_i:
                weight = pi[x] / pi_class[i]
                T_K[i, j] += weight * sum(T[x, y] for y in members_j)
    return T_K


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


def compute_basis_d_states(df, vol_median):
    features = [b[0] for b in BASIS_D["bits"]]
    mask = df[features].notna().all(axis=1)
    bdf = df[mask]
    b0 = (bdf["tot_8h"] > 0).astype(int)
    b1 = (bdf["trend_8h"] > 0).astype(int)
    b2 = (bdf["realized_vol_8h"] > vol_median).astype(int)
    return (b2 * 4 + b1 * 2 + b0).values.astype(int)


# ═══════════════════════════════════════════════════════════════════════════
#  PART 1: 4×4 Complement-Pair Clusters
# ═══════════════════════════════════════════════════════════════════════════

def part1_complement_pairs(states_8):
    print(f"\n{'=' * 70}")
    print("  PART 1: Basis D → 4×4 Complement-Pair Clusters")
    print(f"{'=' * 70}")

    for lbl in CPAIR_LABELS:
        print(f"  {lbl}")

    # Map to 4-state sequence
    states_4 = np.array([STATE_TO_CPAIR[s] for s in states_8])
    plabels = [f"P{i}" for i in range(N_CPAIRS)]

    # Cluster frequencies
    print(f"\n--- Cluster Frequencies ---")
    for p in range(N_CPAIRS):
        c = np.sum(states_4 == p)
        print(f"  P{p}: {c} ({c / len(states_4) * 100:.2f}%)")

    # Transitions
    changes = np.sum(states_4[1:] != states_4[:-1])
    total = len(states_4) - 1
    print(f"\n--- Transitions ---")
    print(f"  Total state changes: {changes} (out of {total} bars = {changes / total * 100:.2f}%)")

    # T₄ and J₄
    T4, _ = transition_matrix(states_4, N_CPAIRS)
    J4 = jump_chain(T4)
    print(f"\n--- T₄ (complement-pair transition matrix) ---")
    print(format_matrix(T4, labels=plabels))
    print(f"\n--- J₄ (jump chain) ---")
    print(format_matrix(J4, labels=plabels))

    # Eigenvalues
    print_eigenvalues(T4, J4, "T₄", "J₄")

    # Stationary distribution
    pi4 = stationary_distribution(T4)
    print(f"\n--- Stationary Distribution π₄ ---")
    for i in range(N_CPAIRS):
        print(f"  P{i}: {pi4[i]:.4f} ({pi4[i] * 100:.2f}%)")
    sorted_pi = np.sort(pi4)[::-1]
    print(f"  Top-3 concentration: {sorted_pi[:3].sum():.4f} ({sorted_pi[:3].sum() * 100:.2f}%)")

    # Zero structure
    print(f"\n--- Zero Structure in J₄ (<2% of row mass) ---")
    n_zeros = 0
    for i in range(N_CPAIRS):
        for j in range(N_CPAIRS):
            if i == j:
                continue
            if J4[i, j] < NEAR_ZERO_THRESH:
                print(f"  P{i} → P{j}: {J4[i, j]:.4f} (near-zero)")
                n_zeros += 1
    if n_zeros == 0:
        print("  (none)")

    # Subperiod stability
    subperiod_stability(states_4, J4, N_CPAIRS, plabels)

    # Save
    np.save(OUTPUT_DIR / "j4_basis_d_complement.npy", J4)
    print(f"\n  Saved J₄ → {OUTPUT_DIR / 'j4_basis_d_complement.npy'}")

    # ── Topology Comparison with Basis A ─────────────────────────────────
    print(f"\n--- Topology Comparison: Basis D complement-pairs vs Basis A slow-bit clusters ---")
    J4_A = np.load(OUTPUT_DIR / "j4_basis_a.npy")
    a_labels = [f"C{i}" for i in range(4)]

    print(f"\n  Basis A J₄:")
    print(format_matrix(J4_A, labels=a_labels))
    print(f"\n  Basis D J₄ (complement-pairs):")
    print(format_matrix(J4, labels=plabels))

    # Near-zero count
    nz_a = sum(1 for i in range(4) for j in range(4) if i != j and J4_A[i, j] < NEAR_ZERO_THRESH)
    nz_d = sum(1 for i in range(4) for j in range(4) if i != j and J4[i, j] < NEAR_ZERO_THRESH)
    print(f"\n  Near-zero cells (<2%): Basis A = {nz_a}/12, Basis D = {nz_d}/12")

    # Dominant outgoing per state (cycle structure check)
    print(f"\n  Dominant outgoing transition (cycle structure):")
    for label_set, J_mat, name in [(a_labels, J4_A, "Basis A"), (plabels, J4, "Basis D")]:
        targets = []
        for i in range(4):
            best_j = np.argmax(J_mat[i])
            targets.append(best_j)
            print(f"    {name} {label_set[i]} → {label_set[best_j]} ({J_mat[i, best_j]:.4f})")
        # Check if it forms a cycle
        visited = set()
        pos = 0
        cycle = [pos]
        for _ in range(4):
            pos = targets[pos]
            if pos in visited:
                break
            visited.add(pos)
            cycle.append(pos)
        is_cycle = len(visited) == 4
        print(f"    → {'Forms full 4-cycle' if is_cycle else 'Does NOT form full 4-cycle'}")

    # Spectral gap comparison
    evals_a = eigenvalues_sorted(J4_A)
    evals_d = eigenvalues_sorted(J4)
    gap_a = abs(evals_a[0]) - abs(evals_a[1])
    gap_d = abs(evals_d[0]) - abs(evals_d[1])
    print(f"\n  Spectral gap (|λ₀|−|λ₁|): Basis A = {gap_a:.4f}, Basis D = {gap_d:.4f}")

    return T4, J4, states_4


# ═══════════════════════════════════════════════════════════════════════════
#  PART 2: (3,5) Surjection Search — Formal Closure
# ═══════════════════════════════════════════════════════════════════════════

def enumerate_surjections():
    """Enumerate all complement-equivariant surjections F₂³ → Z₅.

    Complement pairs: {0,7}, {1,6}, {2,5}, {3,4}.
    For each pair, assign f(lower) ∈ {0..4}; f(upper) = (5 - f(lower)) % 5.
    Filter to surjective maps.
    """
    surjections = []
    for f0, f1, f2, f3 in product(range(5), repeat=4):
        # Compute partner assignments
        f7 = (5 - f0) % 5
        f6 = (5 - f1) % 5
        f5 = (5 - f2) % 5
        f4 = (5 - f3) % 5
        mapping = {0: f0, 1: f1, 2: f2, 3: f3, 4: f4, 5: f5, 6: f6, 7: f7}
        # Check surjectivity
        if len(set(mapping.values())) == 5:
            surjections.append(mapping)
    return surjections


def part2_surjection_search(states_8, T8, pi8):
    print(f"\n{'=' * 70}")
    print("  PART 2: (3,5) Surjection Search — Formal Closure")
    print(f"{'=' * 70}")

    # Step 1: Enumerate
    surjections = enumerate_surjections()
    print(f"\n  Total complement-equivariant surjections: {len(surjections)}")

    # Step 2: Compute lumpability error for each
    errors_5 = []
    for idx, mapping in enumerate(surjections):
        err = lumpability_error(T8, pi8, mapping, 5)
        errors_5.append((err, idx, mapping))
    errors_5.sort()

    # Step 3: Report top 5
    print(f"\n--- Top 5 Surjections by Lumpability Error ---")
    for rank, (err, idx, mapping) in enumerate(errors_5[:5]):
        # Format mapping as grouping
        groups = {v: [] for v in range(5)}
        for s, v in mapping.items():
            groups[v].append(f"S{s}")
        group_str = "  ".join(f"Z{v}={{{','.join(groups[v])}}}" for v in range(5))
        print(f"\n  #{rank + 1}: E = {err:.8f}")
        print(f"    Mapping: {group_str}")

    # Best surjection: full analysis
    best_err, best_idx, best_map = errors_5[0]
    print(f"\n--- Best Surjection: Full Analysis ---")
    groups = {v: [] for v in range(5)}
    for s, v in best_map.items():
        groups[v].append(f"S{s}")
    for v in range(5):
        print(f"  Z{v} = {{{', '.join(groups[v])}}}")

    # Lumped T₅ and J₅
    T5 = lumped_transition_matrix(T8, pi8, best_map, 5)
    J5 = jump_chain(T5)
    z_labels = [f"Z{i}" for i in range(5)]
    print(f"\n--- T₅ (lumped transition matrix, best surjection) ---")
    print(format_matrix(T5, labels=z_labels))
    print(f"\n--- J₅ (jump chain) ---")
    print(format_matrix(J5, labels=z_labels))

    # Eigenvalues
    evals_T5 = eigenvalues_sorted(T5)
    evals_J5 = eigenvalues_sorted(J5)
    print(f"\n--- Eigenvalues (best K=5 surjection) ---")
    print(f"  T₅: {', '.join(f'{e.real:+.4f}' for e in evals_T5)}")
    print(f"  J₅: {', '.join(f'{e.real:+.4f}' for e in evals_J5)}")
    spectral_gap_5 = abs(evals_J5[0]) - abs(evals_J5[1])
    print(f"  Spectral gap (|λ₀|−|λ₁|): {spectral_gap_5:.4f}")
    print(f"  (3,5) prediction: 0.71")

    # Stationary distribution
    pi5 = stationary_distribution(T5)
    print(f"\n--- Stationary Distribution π₅ ---")
    for v in range(5):
        print(f"  Z{v}: {pi5[v]:.4f} ({pi5[v] * 100:.2f}%)")
    sorted_pi5 = np.sort(pi5)[::-1]
    print(f"  Top-3 concentration: {sorted_pi5[:3].sum():.4f} ({sorted_pi5[:3].sum() * 100:.2f}%)")
    print(f"  (3,5) prediction: 0.89")

    # Step 4: Compare K=4 vs K=5
    print(f"\n--- K=4 vs K=5 Comparison ---")
    err_4 = lumpability_error(T8, pi8, STATE_TO_CPAIR, N_CPAIRS)
    print(f"  K=4 complement-pair lumpability error: {err_4:.8f}")
    print(f"  K=5 best surjection lumpability error: {best_err:.8f}")

    # Per-degree-of-freedom comparison
    # K=4: 4 classes from 8 states → 4 partition cells → 4 pairs to compare
    # K=5: 5 classes from 8 states → some cells have 2 members, some have 1
    # Better: normalize by number of constraint pairs
    n_pairs_4 = sum(len([s for s in range(8) if STATE_TO_CPAIR[s] == c])
                     for c in range(4))  # not quite right, let's count actual pairs
    pairs_4 = sum(max(0, len([s for s in range(8) if STATE_TO_CPAIR[s] == c]) - 1)
                  for c in range(4))
    pairs_5 = sum(max(0, len([s for s in range(8) if best_map[s] == c]) - 1)
                  for c in range(5))
    if pairs_4 > 0 and pairs_5 > 0:
        print(f"  K=4: {pairs_4} within-class pairs, error/pair = {err_4 / pairs_4:.8f}")
        print(f"  K=5: {pairs_5} within-class pairs, error/pair = {best_err / pairs_5:.8f}")

    if err_4 < best_err:
        verdict = "K=4 WINS"
    elif best_err < err_4:
        verdict = "K=5 WINS"
    else:
        verdict = "TIE"

    print(f"\n  ═══ VERDICT: K=5 surjection error = {best_err:.8f} vs K=4 complement-pair error = {err_4:.8f} → {verdict} ═══")

    # Distribution of K=5 errors for context
    all_errs = [e[0] for e in errors_5]
    print(f"\n--- K=5 Error Distribution (all {len(surjections)} surjections) ---")
    print(f"  Min: {min(all_errs):.8f}")
    print(f"  Median: {np.median(all_errs):.8f}")
    print(f"  Max: {max(all_errs):.8f}")
    print(f"  Mean: {np.mean(all_errs):.8f}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()
    vol_median = df["realized_vol_8h"].median()
    print(f"  Global realized_vol_8h median: {vol_median:.6f}")

    states_8 = compute_basis_d_states(df, vol_median)
    print(f"  Basis D 8-state series: {len(states_8)} bars")

    # Part 1: complement-pair 4×4
    T4, J4, states_4 = part1_complement_pairs(states_8)

    # Part 2: surjection search
    T8, _ = transition_matrix(states_8, N_STATES)
    pi8 = stationary_distribution(T8)
    print(f"\n  Basis D π₈: {', '.join(f'S{i}={pi8[i]:.4f}' for i in range(8))}")
    part2_surjection_search(states_8, T8, pi8)

    print(f"\n{'=' * 70}")
    print("  Phase 3 closure complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
