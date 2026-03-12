#!/usr/bin/env python3
"""Phase 1 Diagnostics: Trigram Construction & Raw Transition Structure.

Downsamples 1s BTC data to 5min bars, constructs three binary trigram bases,
computes transition matrices, jump chains, eigenvalues, dwell times,
and subperiod stability.
"""

import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent / "datalog_2025-07-21_2026-02-20.csv"
OUTPUT_DIR = Path(__file__).parent
DOWNSAMPLE_MS = 300_000  # 5 minutes in milliseconds

# Columns needed across all bases
NEEDED_COLS = [
    "timestamp", "price",
    "trend_1h", "trend_8h", "trend_48h",
    "vp12h_poc_dist", "vp48h_poc_dist", "vp96h_poc_dist",
    "cvd_slope_15m", "realized_vol_8h",
]

# ─── Basis Definitions ──────────────────────────────────────────────────────
# Each basis: name, list of 3 (feature, threshold_type, threshold_value)
# threshold_type: "zero" = >0→1, "median" = >median→1

BASES = {
    "A": {
        "label": "Cross-timescale trend",
        "bits": [
            ("trend_1h",       "zero", 0),
            ("trend_8h",       "zero", 0),
            ("trend_48h",      "zero", 0),
        ],
    },
    "B": {
        "label": "Price vs volume profile",
        "bits": [
            ("vp12h_poc_dist", "zero", 0),
            ("vp48h_poc_dist", "zero", 0),
            ("vp96h_poc_dist", "zero", 0),
        ],
    },
    "C": {
        "label": "Flow × structure × activity",
        "bits": [
            ("cvd_slope_15m",   "zero",   0),
            ("trend_8h",        "zero",   0),
            ("realized_vol_8h", "median", None),  # computed at runtime
        ],
    },
}

N_STATES = 8
N_SUBPERIODS = 3


# ─── Helpers ─────────────────────────────────────────────────────────────────

def text_histogram(values, bins=10, width=40):
    """Return a text histogram string."""
    counts, edges = np.histogram(values, bins=bins)
    max_count = counts.max()
    lines = []
    for i, c in enumerate(counts):
        bar_len = int(c / max_count * width) if max_count > 0 else 0
        lines.append(f"  [{edges[i]:+10.4f}, {edges[i+1]:+10.4f}) | {'█' * bar_len} {c}")
    return "\n".join(lines)


def compute_trigram(df, basis_def, vol_median=None):
    """Compute trigram state (0-7) from basis definition."""
    bits = []
    for feat, thresh_type, thresh_val in basis_def["bits"]:
        if thresh_type == "zero":
            bits.append((df[feat] > 0).astype(int))
        elif thresh_type == "median":
            median_val = vol_median if vol_median is not None else df[feat].median()
            bits.append((df[feat] > median_val).astype(int))
    return bits[2] * 4 + bits[1] * 2 + bits[0]


def transition_matrix(states, n_states=N_STATES):
    """Row-normalized transition matrix from state sequence."""
    T = np.zeros((n_states, n_states))
    for i in range(len(states) - 1):
        T[states[i], states[i + 1]] += 1
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # avoid div by zero for unvisited states
    return T / row_sums, T  # normalized, raw counts


def jump_chain(T):
    """Embedded jump chain: remove self-transitions."""
    J = T.copy()
    np.fill_diagonal(J, 0)
    row_sums = J.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return J / row_sums


def eigenvalues_sorted(M):
    """Eigenvalues sorted by descending magnitude."""
    evals = np.linalg.eigvals(M)
    order = np.argsort(-np.abs(evals))
    return evals[order]


def dwell_times(states):
    """Compute dwell time runs per state. Returns dict: state → list of run lengths."""
    runs = {s: [] for s in range(N_STATES)}
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


def format_matrix(M, decimals=4):
    """Format matrix as aligned string."""
    lines = []
    header = "     " + "".join(f"   S{j}   " for j in range(M.shape[1]))
    lines.append(header)
    for i in range(M.shape[0]):
        row = f"S{i}  " + " ".join(f"{M[i,j]:.{decimals}f}" for j in range(M.shape[1]))
        lines.append(row)
    return "\n".join(lines)


# ─── Step 1: Downsample ─────────────────────────────────────────────────────

def load_and_downsample():
    """Load CSV in chunks, downsample to 5min bars by taking last value per window."""
    print("Loading and downsampling to 5-minute bars...")
    chunks = []
    for chunk in pd.read_csv(DATA_PATH, usecols=NEEDED_COLS, chunksize=500_000):
        chunk["bar"] = chunk["timestamp"] // DOWNSAMPLE_MS
        last_per_bar = chunk.groupby("bar").last().reset_index()
        chunks.append(last_per_bar)

    df = pd.concat(chunks, ignore_index=True)
    # Re-aggregate: multiple chunks may have partial bars at boundaries
    df = df.groupby("bar").last().reset_index()
    df = df.sort_values("bar").reset_index(drop=True)
    print(f"  Rows after downsample: {len(df)}")
    print(f"  Time range: {pd.to_datetime(df['timestamp'].iloc[0], unit='ms', utc=True)} → "
          f"{pd.to_datetime(df['timestamp'].iloc[-1], unit='ms', utc=True)}")
    print(f"  Price range: {df['price'].min():.0f} → {df['price'].max():.0f}")
    return df


# ─── Step 3: Per-basis diagnostics ──────────────────────────────────────────

def analyze_basis(df, basis_key, basis_def, vol_median=None):
    """Run all diagnostics for one basis."""
    label = basis_def["label"]
    print(f"\n{'=' * 70}")
    print(f"  BASIS {basis_key}: {label}")
    print(f"{'=' * 70}")

    # Drop NaN rows for this basis's features
    features = [b[0] for b in basis_def["bits"]]
    mask = df[features].notna().all(axis=1)
    bdf = df[mask].copy()
    n_dropped = len(df) - len(bdf)
    if n_dropped > 0:
        print(f"\n  Dropped {n_dropped} rows with NaN ({n_dropped/len(df)*100:.1f}%)")
    print(f"  Working rows: {len(bdf)}")

    # ── 3a: Feature Marginals ────────────────────────────────────────────
    print(f"\n--- Feature Marginals ---")
    for feat, thresh_type, thresh_val in basis_def["bits"]:
        vals = bdf[feat].values
        if thresh_type == "median":
            effective_thresh = vol_median if vol_median is not None else np.median(vals)
            thresh_label = f"median ({effective_thresh:.6f})"
        else:
            effective_thresh = 0
            thresh_label = "0"

        near_thresh = np.mean(np.abs(vals - effective_thresh) < 0.01) * 100
        skewness = sp_stats.skew(vals)
        print(f"\n  {feat} (threshold: {thresh_label}):")
        print(f"    mean={np.mean(vals):.6f}  median={np.median(vals):.6f}  "
              f"std={np.std(vals):.6f}  skew={skewness:.4f}")
        print(f"    within ±0.01 of threshold: {near_thresh:.2f}%")
        print(text_histogram(vals))

    # ── Compute trigram states ───────────────────────────────────────────
    states = compute_trigram(bdf, basis_def, vol_median).values.astype(int)

    # ── 3b: State Frequencies ────────────────────────────────────────────
    print(f"\n--- State Frequencies ---")
    print(f"  {'State':>5}  {'Count':>8}  {'Pct':>7}")
    for s in range(N_STATES):
        c = np.sum(states == s)
        print(f"  S{s:<4}  {c:>8}  {c/len(states)*100:>6.2f}%")

    # ── 3c: Transition Count ─────────────────────────────────────────────
    changes = np.sum(states[1:] != states[:-1])
    total_transitions = len(states) - 1
    print(f"\n--- Transitions ---")
    print(f"  Total state changes: {changes} (out of {total_transitions} bars = {changes/total_transitions*100:.2f}%)")
    if changes < 300:
        print(f"  ⚠️  WARNING: <300 transitions, 8×8 matrix will be sparse!")

    # ── 3d: Dwell Time Distributions ─────────────────────────────────────
    print(f"\n--- Dwell Times (in 5-min bars) ---")
    runs = dwell_times(states)
    print(f"  {'State':>5}  {'Runs':>6}  {'Mean':>8}  {'Median':>8}  {'Max':>8}  {'CV':>6}  {'Flag':>10}")
    for s in range(N_STATES):
        r = runs[s]
        if len(r) == 0:
            print(f"  S{s:<4}  {'N/A':>6}")
            continue
        r = np.array(r)
        mean_r = np.mean(r)
        cv = np.std(r) / mean_r if mean_r > 0 else 0
        flag = "HEAVY-TAIL" if cv > 1 else ""
        print(f"  S{s:<4}  {len(r):>6}  {mean_r:>8.1f}  {np.median(r):>8.1f}  "
              f"{np.max(r):>8}  {cv:>6.2f}  {flag:>10}")

    # ── 3e: T₈ Full Transition Matrix ───────────────────────────────────
    T, T_raw = transition_matrix(states)
    print(f"\n--- T₈ (full transition matrix) ---")
    print(format_matrix(T))

    # ── 3f: J₈ Jump Chain ───────────────────────────────────────────────
    J = jump_chain(T)
    print(f"\n--- J₈ (jump chain, self-transitions removed) ---")
    print(format_matrix(J))

    # ── 3g: Eigenvalues ──────────────────────────────────────────────────
    evals_T = eigenvalues_sorted(T)
    evals_J = eigenvalues_sorted(J)
    print(f"\n--- Eigenvalues ---")
    print(f"  T₈: {', '.join(f'{e.real:+.4f}' for e in evals_T)}")
    print(f"  J₈: {', '.join(f'{e.real:+.4f}' for e in evals_J)}")
    gaps_J = [abs(abs(evals_J[i]) - abs(evals_J[i+1])) for i in range(len(evals_J)-1)]
    print(f"  J₈ magnitude gaps: {', '.join(f'{g:.4f}' for g in gaps_J)}")
    max_gap_idx = np.argmax(gaps_J)
    print(f"  Largest gap: between eigenvalue {max_gap_idx} and {max_gap_idx+1} "
          f"(suggests ~{max_gap_idx+1} natural clusters)")

    # ── 3h: Subperiod Stability ──────────────────────────────────────────
    print(f"\n--- Subperiod Stability ---")
    n = len(states)
    split_points = [0, n // 3, 2 * n // 3, n]
    sub_Js = []
    for k in range(N_SUBPERIODS):
        sub_states = states[split_points[k]:split_points[k+1]]
        sub_T, _ = transition_matrix(sub_states)
        sub_J = jump_chain(sub_T)
        sub_Js.append(sub_J)
        frob = np.linalg.norm(sub_J - J, 'fro')
        print(f"  Subperiod {k+1} ({split_points[k]}:{split_points[k+1]}): "
              f"‖J₈_sub - J₈_full‖_F = {frob:.4f}")

    # Zero-pattern stability
    NEAR_ZERO_THRESH = 0.02
    stable_zeros = 0
    total_off_diag = N_STATES * (N_STATES - 1)  # 56
    unstable_cells = []
    for i in range(N_STATES):
        for j in range(N_STATES):
            if i == j:
                continue
            is_near_zero = [sub_Js[k][i, j] < NEAR_ZERO_THRESH for k in range(N_SUBPERIODS)]
            if all(is_near_zero):
                stable_zeros += 1
            elif any(is_near_zero) and not all(is_near_zero):
                unstable_cells.append((i, j))
    print(f"\n  Zero-pattern stability (<{NEAR_ZERO_THRESH*100}% of row mass):")
    print(f"    {stable_zeros}/{total_off_diag} off-diagonal cells are stable near-zeros across all subperiods")
    if unstable_cells:
        print(f"    {len(unstable_cells)} cells shift between near-zero and non-zero:")
        for i, j in unstable_cells[:10]:  # cap output
            vals = [f"{sub_Js[k][i,j]:.4f}" for k in range(N_SUBPERIODS)]
            print(f"      ({i}→{j}): subperiods = [{', '.join(vals)}]")
        if len(unstable_cells) > 10:
            print(f"      ... and {len(unstable_cells) - 10} more")

    # Save J₈
    out_path = OUTPUT_DIR / f"j8_basis_{basis_key.lower()}.npy"
    np.save(out_path, J)
    print(f"\n  Saved J₈ → {out_path}")

    return J


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()

    # Pre-compute median for Basis C's realized_vol_8h (on full dataset before splits)
    vol_median = df["realized_vol_8h"].median()
    print(f"\nGlobal realized_vol_8h median: {vol_median:.6f}")

    for key, basis_def in BASES.items():
        analyze_basis(df, key, basis_def, vol_median=vol_median if key == "C" else None)

    print(f"\n{'=' * 70}")
    print("  Phase 1 diagnostics complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
