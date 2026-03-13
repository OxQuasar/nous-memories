#!/usr/bin/env python3
"""Phase 9: Timescale Universality — Does the 4-regime cycle hold across
different timescale combinations?

Tests whether the K=4 directed cycle (Bear→Reversal→Bull→Pullback) is a
universal property of multi-timescale trend coupling, or specific to
the 1h/8h/48h combination.

Four bases tested:
  A: trend_1h  / trend_8h  / trend_48h  (original, ratio 1:8:48)
  E: trend_4h  / trend_24h / trend_96h  (shifted up 4×, ratio 4:24:96)
  F: trend_1h  / trend_4h  / trend_16h  (compressed, ratio 1:4:16)
  G: trend_1h  / trend_16h / trend_96h  (widest spread, ratio 1:16:96)

All trend features binarized at zero (positive = uptrend), consistent
with all prior phases.
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path("/home/quasar/nous/memories/markets/datalog_2025-07-21_2026-02-20.csv")
OUTPUT_DIR = Path("/home/quasar/nous/memories/markets")
DOWNSAMPLE_MS = 300_000
N_STATES = 8
N_MACRO = 4

# All features we need across all bases
ALL_TREND_COLS = ["trend_1h", "trend_4h", "trend_8h", "trend_16h",
                  "trend_24h", "trend_48h", "trend_96h"]
NEEDED_COLS = ["timestamp", "price"] + ALL_TREND_COLS

# Basis definitions: (fast, medium, slow) — all binarized at zero
BASES = {
    "A": {"fast": "trend_1h",  "med": "trend_8h",  "slow": "trend_48h", "label": "1h/8h/48h (original)"},
    "E": {"fast": "trend_4h",  "med": "trend_24h", "slow": "trend_96h", "label": "4h/24h/96h (shifted up)"},
    "F": {"fast": "trend_1h",  "med": "trend_4h",  "slow": "trend_16h", "label": "1h/4h/16h (compressed)"},
    "G": {"fast": "trend_1h",  "med": "trend_16h", "slow": "trend_96h", "label": "1h/16h/96h (widest)"},
}

# K=4 macro mapping: cluster = slow_bit*2 + med_bit (Hamming-adjacent pairs)
# C0 = {S0,S1}: slow=0, med=0 → bear
# C1 = {S2,S3}: slow=0, med=1 → reversal
# C2 = {S4,S5}: slow=1, med=0 → pullback
# C3 = {S6,S7}: slow=1, med=1 → bull
STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
MACRO_LABELS = ["C0 bear", "C1 reversal", "C2 pullback", "C3 bull"]

# Expected structural zeros in directed cycle
EXPECTED_ZEROS = [(0, 3), (1, 2), (2, 1), (3, 0)]
NEAR_ZERO_THRESH = 0.02


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

def compute_8states(df, basis):
    """Compute 8-state trigram: slow(bit2) × med(bit1) × fast(bit0). All at zero threshold."""
    feats = [basis["fast"], basis["med"], basis["slow"]]
    mask = df[feats].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    b0 = (bdf[basis["fast"]] > 0).astype(int).values
    b1 = (bdf[basis["med"]] > 0).astype(int).values
    b2 = (bdf[basis["slow"]] > 0).astype(int).values
    states = b2 * 4 + b1 * 2 + b0
    return bdf, states


def transition_matrix(states, n=N_STATES):
    T = np.zeros((n, n))
    for i in range(len(states) - 1):
        T[states[i], states[i + 1]] += 1
    raw = T.copy()
    rs = T.sum(axis=1, keepdims=True)
    rs[rs == 0] = 1
    return T / rs, raw


def jump_chain(T):
    J = T.copy()
    np.fill_diagonal(J, 0)
    rs = J.sum(axis=1, keepdims=True)
    rs[rs == 0] = 1
    return J / rs


def eigenvalues_sorted(M):
    evals = np.linalg.eigvals(M)
    return evals[np.argsort(-np.abs(evals))]


def stationary_dist(T):
    evals, evecs = np.linalg.eig(T.T)
    idx = np.argmin(np.abs(evals - 1.0))
    pi = np.real(evecs[:, idx])
    return pi / pi.sum()


def format_matrix(M, labels, decimals=3):
    w = max(len(l) for l in labels)
    header = " " * (w + 2) + "".join(f"{l:>{w+2}}" for l in labels)
    lines = [header]
    for i, l in enumerate(labels):
        row = f"{l:<{w+2}}" + "".join(f"{M[i,j]:>{w+2}.{decimals}f}" for j in range(M.shape[1]))
        lines.append(row)
    return "\n".join(lines)


def complement_symmetry(J):
    """Test complement symmetry (x ↦ x⊕7) on 8×8 jump chain. Returns (all_pass, jsds)."""
    pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    jsds = []
    for sa, sb in pairs:
        row_a = J[sa].copy()
        row_b_relabeled = np.array([J[sb, j ^ 7] for j in range(N_STATES)])
        if row_a.sum() == 0 or row_b_relabeled.sum() == 0:
            jsds.append(float("nan"))
            continue
        jsds.append(jensenshannon(row_a, row_b_relabeled))
    jsds = np.array(jsds)
    valid = jsds[~np.isnan(jsds)]
    all_pass = len(valid) > 0 and np.all(valid < 0.1)
    return all_pass, jsds


def extract_episodes(macro_states, states_8, prices):
    n = len(macro_states)
    episodes = []
    i = 0
    while i < n:
        macro = macro_states[i]
        start = i
        while i < n and macro_states[i] == macro:
            i += 1
        end = i - 1
        truncated = (start == 0) or (end == n - 1)
        exit_dest = macro_states[i] if i < n else -1
        episodes.append({
            "macro": macro,
            "duration": end - start + 1,
            "entry_sub": states_8[start],
            "exit_sub": states_8[end],
            "exit_dest": exit_dest,
            "entry_price": prices[start],
            "exit_price": prices[end],
            "log_return": np.log(prices[end] / prices[start]) if prices[start] > 0 else 0,
            "start_idx": start,
            "end_idx": end,
            "truncated": truncated,
        })
    return episodes


def wilson_ci(count, n, z=1.96):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = count / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    spread = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return p, max(0, center - spread), min(1, center + spread)


# ═══════════════════════════════════════════════════════════════════════════
#  Per-Basis Analysis
# ═══════════════════════════════════════════════════════════════════════════

def analyze_basis(df, basis_key, basis):
    """Full analysis for one timescale basis. Returns summary dict."""
    label = basis["label"]
    print(f"\n{'=' * 70}")
    print(f"  BASIS {basis_key}: {label}")
    print(f"  Features: {basis['fast']} (bit0) × {basis['med']} (bit1) × {basis['slow']} (bit2)")
    print(f"{'=' * 70}")

    bdf, states = compute_8states(df, basis)
    prices = bdf["price"].values
    macro = np.array([STATE_TO_MACRO[s] for s in states])
    n_rows = len(bdf)
    print(f"  Working rows: {n_rows}")

    # ── Pairwise correlation of binary features ──────────────────────────
    b0 = (bdf[basis["fast"]] > 0).astype(int).values
    b1 = (bdf[basis["med"]] > 0).astype(int).values
    b2 = (bdf[basis["slow"]] > 0).astype(int).values
    corr = np.corrcoef([b0, b1, b2])
    max_off = max(abs(corr[i, j]) for i in range(3) for j in range(3) if i != j)
    print(f"  Max pairwise |r|: {max_off:.4f} {'(OK < 0.3)' if max_off < 0.3 else '(HIGH > 0.3) ⚠️'}")
    for i, n1 in enumerate([basis["fast"], basis["med"], basis["slow"]]):
        for j, n2 in enumerate([basis["fast"], basis["med"], basis["slow"]]):
            if j > i:
                print(f"    r({n1}, {n2}) = {corr[i,j]:.4f}")

    # ── State frequencies ────────────────────────────────────────────────
    print(f"\n--- State Frequencies ---")
    for s in range(N_STATES):
        c = np.sum(states == s)
        print(f"  S{s} ({s>>2}{(s>>1)&1}{s&1}): {c:>8}  ({c/len(states)*100:.1f}%)")

    # ── T₈, J₈ ──────────────────────────────────────────────────────────
    T8, T8_raw = transition_matrix(states, N_STATES)
    J8 = jump_chain(T8)
    print(f"\n--- J₈ (jump chain) ---")
    print(format_matrix(J8, [f"S{i}" for i in range(N_STATES)]))

    # ── Eigenvalue gap ───────────────────────────────────────────────────
    evals_J = eigenvalues_sorted(J8)
    print(f"\n--- Eigenvalues (J₈) ---")
    print(f"  {', '.join(f'{e.real:+.4f}' for e in evals_J)}")
    gaps = [abs(abs(evals_J[i]) - abs(evals_J[i + 1])) for i in range(len(evals_J) - 1)]
    print(f"  Gaps: {', '.join(f'{g:.4f}' for g in gaps)}")
    max_gap_idx = np.argmax(gaps)
    k_eigenvalue = max_gap_idx + 1
    print(f"  Largest gap: between eigenvalue {max_gap_idx} and {max_gap_idx+1} → K={k_eigenvalue}")

    # ── Complement symmetry ──────────────────────────────────────────────
    sym_holds, jsds = complement_symmetry(J8)
    print(f"\n--- Complement Symmetry ---")
    pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    for pi, (sa, sb) in enumerate(pairs):
        status = "✓" if jsds[pi] < 0.1 else "✗"
        print(f"  (S{sa}, S{sb}): JSD={jsds[pi]:.4f}  [{status}]")
    mean_jsd = np.nanmean(jsds)
    print(f"  Mean JSD: {mean_jsd:.4f}  → {'HOLDS' if sym_holds else 'FAILS'}")

    # ── J₄ collapse ─────────────────────────────────────────────────────
    macro_states_4 = np.array([STATE_TO_MACRO[s] for s in states])
    T4, T4_raw = transition_matrix(macro_states_4, N_MACRO)
    J4 = jump_chain(T4)
    clabels = [f"C{i}" for i in range(N_MACRO)]
    print(f"\n--- J₄ (4-state collapse) ---")
    print(format_matrix(J4, clabels))

    # ── Structural zeros ────────────────────────────────────────────────
    print(f"\n--- Structural Zeros (< {NEAR_ZERO_THRESH*100:.0f}% of row) ---")
    found_zeros = []
    for i in range(N_MACRO):
        for j in range(N_MACRO):
            if i == j:
                continue
            if J4[i, j] < NEAR_ZERO_THRESH:
                found_zeros.append((i, j))
                expected = "EXPECTED" if (i, j) in EXPECTED_ZEROS else "UNEXPECTED"
                print(f"  C{i}→C{j}: {J4[i,j]:.4f}  [{expected}]")

    # Check which expected zeros are present
    zeros_match = set(found_zeros) == set(EXPECTED_ZEROS)
    missing = set(EXPECTED_ZEROS) - set(found_zeros)
    extra = set(found_zeros) - set(EXPECTED_ZEROS)
    if zeros_match:
        print(f"  → All 4 expected zeros present, no extras. TOPOLOGY MATCHES.")
    else:
        if missing:
            print(f"  → Missing expected zeros: {[(f'C{i}→C{j}') for i,j in missing]}")
        if extra:
            print(f"  → Extra unexpected zeros: {[(f'C{i}→C{j}') for i,j in extra]}")

    # ── Cycle direction check ───────────────────────────────────────────
    # Expected: C0→C1 dominant, C1→C3 (not C1→C2), C3→C2 dominant, C2→C0 (not C2→C3... wait)
    # Cycle: C0→C1→C3→C2→C0
    # Dominant cross-macro: C0→C1 (.924), C1→C0 (.795) with C1→C3 (.205),
    #   C3→C2 (.919), C2→C3 (.770) with C2→C0 (.230)
    # Each macro pair oscillates internally, with "leaks" advancing the cycle

    print(f"\n--- Cycle Direction ---")
    # Check that within each macro pair, the dominant transition matches expected
    # And the cross-macro transition follows the cycle
    # For the cycle C0→C1→C3→C2→C0:
    forward_transitions = [(0, 1), (1, 3), (3, 2), (2, 0)]
    # Each pair also has backward transition (return within the sub-cycle)
    backward_transitions = [(1, 0), (3, 2), (2, 3), (0, 2)]
    # Actually let me just print the key transition rates
    print(f"  C0→C1: {J4[0,1]:.3f}  C0→C2: {J4[0,2]:.3f}  (C0→C3: {J4[0,3]:.3f})")
    print(f"  C1→C0: {J4[1,0]:.3f}  C1→C3: {J4[1,3]:.3f}  (C1→C2: {J4[1,2]:.3f})")
    print(f"  C2→C3: {J4[2,3]:.3f}  C2→C0: {J4[2,0]:.3f}  (C2→C1: {J4[2,1]:.3f})")
    print(f"  C3→C2: {J4[3,2]:.3f}  C3→C1: {J4[3,1]:.3f}  (C3→C0: {J4[3,0]:.3f})")

    # Determine if the cycle direction is consistent
    # Forward: C0→C1 > C0→C2, C1→C3 secondary to C1→C0, C3→C2 dominant, C2→C3 > C2→C0 usually
    cycle_forward = (J4[0,1] > J4[0,2] and J4[3,2] > J4[3,1])
    print(f"  Forward cycle (C0→C1→C3→C2→C0): {'YES' if cycle_forward else 'NO / DIFFERENT'}")

    # ── Stationary distribution ─────────────────────────────────────────
    pi4 = stationary_dist(T4)
    print(f"\n--- Stationary Distribution (π₄) ---")
    for i in range(N_MACRO):
        print(f"  C{i}: {pi4[i]:.4f} ({pi4[i]*100:.1f}%)")
    pi_range = (pi4.min(), pi4.max())
    print(f"  Range: {pi_range[0]*100:.1f}%–{pi_range[1]*100:.1f}%")

    # ── Episodes ────────────────────────────────────────────────────────
    episodes = extract_episodes(macro, states, prices)
    clean = [e for e in episodes if not e["truncated"]]
    print(f"\n--- Episodes ---")
    print(f"  Total: {len(episodes)}, Clean: {len(clean)}")

    print(f"  {'Regime':>15}  {'n':>6}  {'Mean (bars)':>12}  {'Mean (h)':>10}  {'Median (h)':>11}")
    for m in range(N_MACRO):
        eps = [e for e in clean if e["macro"] == m]
        if not eps:
            print(f"  {MACRO_LABELS[m]:>15}  {0:>6}")
            continue
        durs = np.array([e["duration"] for e in eps])
        print(f"  {MACRO_LABELS[m]:>15}  {len(eps):>6}  {np.mean(durs):>12.1f}  "
              f"{np.mean(durs)*5/60:>10.1f}  {np.median(durs)*5/60:>11.1f}")

    all_durs = np.array([e["duration"] for e in clean])
    mean_dur_h = np.mean(all_durs) * 5 / 60

    # ── Exit sub-state signal (C2 equivalent) ───────────────────────────
    print(f"\n--- Exit Sub-State Signal (C2 pullback) ---")
    c2_clean = [e for e in clean if e["macro"] == 2 and e["exit_dest"] in (0, 3)]
    s5_bull = sum(1 for e in c2_clean if e["exit_sub"] == 5 and e["exit_dest"] == 3)
    s5_total = sum(1 for e in c2_clean if e["exit_sub"] == 5)
    s4_bull = sum(1 for e in c2_clean if e["exit_sub"] == 4 and e["exit_dest"] == 3)
    s4_total = sum(1 for e in c2_clean if e["exit_sub"] == 4)

    s5_rate, s5_lo, s5_hi = wilson_ci(s5_bull, s5_total)
    s4_rate, s4_lo, s4_hi = wilson_ci(s4_bull, s4_total)
    print(f"  S5 (fast↑) exits: n={s5_total}, → bull={s5_bull} ({s5_rate*100:.1f}%) [{s5_lo*100:.0f}%, {s5_hi*100:.0f}%]")
    print(f"  S4 (fast↓) exits: n={s4_total}, → bull={s4_bull} ({s4_rate*100:.1f}%) [{s4_lo*100:.0f}%, {s4_hi*100:.0f}%]")
    signal_gap = s5_rate - s4_rate
    print(f"  Signal gap (S5 - S4): {signal_gap*100:.1f} pp")

    # ── Within-pair heterogeneity ───────────────────────────────────────
    print(f"\n--- Within-Pair Heterogeneity (JSD of cross-cluster exit profiles) ---")
    for c_idx in range(N_MACRO):
        members = [c_idx * 2, c_idx * 2 + 1]  # S0,S1 or S2,S3 etc.
        profiles = []
        for m in members:
            # Distribution over other macro-regimes when leaving this cluster
            cross = np.zeros(N_MACRO)
            for j in range(N_STATES):
                tc = STATE_TO_MACRO[j]
                if tc != c_idx:
                    cross[tc] += J8[m, j]
            total = cross.sum()
            if total > 0:
                cross /= total
            profiles.append(cross)
        jsd = jensenshannon(profiles[0], profiles[1])
        flag = " ⚠️ HETEROGENEOUS" if jsd > 0.1 else ""
        print(f"  C{c_idx} {{S{members[0]},S{members[1]}}}: JSD={jsd:.4f}{flag}")

    # ── Build summary ───────────────────────────────────────────────────
    summary = {
        "basis": basis_key,
        "label": label,
        "k_eigenvalue": k_eigenvalue,
        "zeros_match": zeros_match,
        "cycle_forward": cycle_forward,
        "sym_holds": sym_holds,
        "mean_jsd": mean_jsd,
        "n_episodes": len(clean),
        "mean_dur_h": mean_dur_h,
        "s5_rate": s5_rate,
        "s5_n": s5_total,
        "s4_rate": s4_rate,
        "s4_n": s4_total,
        "signal_gap": signal_gap,
        "pi_range": f"{pi_range[0]*100:.1f}–{pi_range[1]*100:.1f}%",
        "max_corr": max_off,
        "J4": J4,
    }
    return summary


# ═══════════════════════════════════════════════════════════════════════════
#  Summary Table
# ═══════════════════════════════════════════════════════════════════════════

def print_summary(summaries):
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY TABLE: Timescale Universality")
    print(f"{'=' * 70}")

    keys = ["A", "E", "F", "G"]
    headers = [summaries[k]["label"] for k in keys]

    rows = [
        ("K (eigenvalue gap)", [str(summaries[k]["k_eigenvalue"]) for k in keys]),
        ("Topology matches A?", ["(ref)" if k == "A" else ("YES" if summaries[k]["zeros_match"] and summaries[k]["cycle_forward"] else "NO") for k in keys]),
        ("Structural zeros", ["4/4" if summaries[k]["zeros_match"] else "DIFFERENT" for k in keys]),
        ("Complement sym (mean JSD)", [f"{summaries[k]['mean_jsd']:.3f}" for k in keys]),
        ("Complement sym holds?", ["YES" if summaries[k]["sym_holds"] else "NO" for k in keys]),
        ("Clean episodes", [str(summaries[k]["n_episodes"]) for k in keys]),
        ("Mean duration (h)", [f"{summaries[k]['mean_dur_h']:.1f}" for k in keys]),
        ("S5→bull rate", [f"{summaries[k]['s5_rate']*100:.1f}% (n={summaries[k]['s5_n']})" for k in keys]),
        ("S4→bull rate", [f"{summaries[k]['s4_rate']*100:.1f}% (n={summaries[k]['s4_n']})" for k in keys]),
        ("Signal gap (S5-S4)", [f"{summaries[k]['signal_gap']*100:.1f}pp" for k in keys]),
        ("Stationary dist range", [summaries[k]["pi_range"] for k in keys]),
        ("Max feature |r|", [f"{summaries[k]['max_corr']:.3f}" for k in keys]),
    ]

    # Print
    col_w = 22
    label_w = 28
    print(f"\n  {'Property':<{label_w}}" + "".join(f"  {h:>{col_w}}" for h in headers))
    print(f"  {'─' * label_w}" + "".join(f"  {'─' * col_w}" for _ in headers))
    for name, vals in rows:
        print(f"  {name:<{label_w}}" + "".join(f"  {v:>{col_w}}" for v in vals))

    # ── Duration scaling check ──────────────────────────────────────────
    print(f"\n--- Duration Scaling ---")
    print(f"  If episode duration scales with slow timescale:")
    # Slow timescales: A=48h, E=96h, F=16h, G=96h
    slow_scales = {"A": 48, "E": 96, "F": 16, "G": 96}
    ref_dur = summaries["A"]["mean_dur_h"]
    ref_slow = slow_scales["A"]
    for k in keys:
        actual = summaries[k]["mean_dur_h"]
        predicted = ref_dur * slow_scales[k] / ref_slow
        ratio = actual / ref_dur
        print(f"  Basis {k}: slow={slow_scales[k]}h, dur={actual:.1f}h, "
              f"ratio to A={ratio:.2f}× (predicted {slow_scales[k]/ref_slow:.2f}×)")

    # ── Interpretation ─────────────────────────────────────────────────
    print(f"\n--- Interpretation ---")
    all_k4 = all(summaries[k]["k_eigenvalue"] == 4 for k in keys)
    all_topo = all(summaries[k]["zeros_match"] and summaries[k]["cycle_forward"] for k in keys)
    all_sym = all(summaries[k]["sym_holds"] for k in keys)

    if all_k4 and all_topo:
        print(f"  ★ K=4 directed cycle is UNIVERSAL across all tested timescales.")
        print(f"    The regime structure is a property of multi-timescale trend coupling,")
        print(f"    not specific to any particular timescale combination.")
    elif all_k4:
        print(f"  K=4 emerges universally, but topology differs across bases.")
    else:
        non_k4 = [k for k in keys if summaries[k]["k_eigenvalue"] != 4]
        print(f"  K≠4 for bases: {non_k4}. The cycle is NOT timescale-universal.")

    if all_sym:
        print(f"  Complement symmetry holds for ALL bases — coherence parity is universal.")
    else:
        fail = [k for k in keys if not summaries[k]["sym_holds"]]
        print(f"  Complement symmetry fails for: {fail}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()

    summaries = {}
    for key in ["A", "E", "F", "G"]:
        summaries[key] = analyze_basis(df, key, BASES[key])

    print_summary(summaries)

    print(f"\n{'=' * 70}")
    print("  Phase 9 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
