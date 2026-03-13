#!/usr/bin/env python3
"""Phase 12: OOS Validation — BTC 2023-2024 vs IS (Jul 2025–Feb 2026).

Step 0: Distribution Diagnostic
Part A: Topology (OOS)
Part B: Exit Prediction (IS→OOS cross-validation)
Part C: Returns
"""

import sys
import numpy as np
import pandas as pd
import warnings
from pathlib import Path
from scipy.spatial.distance import jensenshannon
from scipy.stats import skew
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ─── Configuration ───────────────────────────────────────────────────────────

BASE = Path(__file__).parent
OOS_PATH = BASE / "data" / "btc_5m_2023-01-01_2024-12-31.csv"
IS_PATH = BASE / "data" / "datalog_2025-07-21_2026-02-20.csv"
IS_DOWNSAMPLE_MS = 300_000
NEEDED_COLS = ["timestamp", "time_str", "price", "trend_1h", "trend_8h", "trend_48h"]

STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
MACRO_NAMES = {0: "C0(bear)", 1: "C1(rev)", 2: "C2(pull)", 3: "C3(bull)"}
N_STATES = 8
N_MACRO = 4
Z = 1.96

# IS reference values from Phase 11
IS_REF = {
    "c2_coef_t8h": 42.2,
    "c2_coef_t1h": 2.23,
    "c2_intercept": 5.91,
    "c2_auc": 0.973,
    "c1_coef_t8h": 48.1,
    "c1_auc": 0.965,
    "s5_bull_rate": 0.918,
    "c2s5_bull_return": 0.0009,
    "c2s4_bull_return": -0.0017,
    "c1_breakthrough_return": 0.0109,
    "c1_failure_return": -0.0025,
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def load_oos():
    print("Loading OOS data (BTC 5m, 2023-2024)...")
    df = pd.read_csv(OOS_PATH, usecols=NEEDED_COLS)
    df = df.sort_values("time_str").reset_index(drop=True)
    print(f"  Rows: {len(df)}, Price: {df.price.min():.0f}–{df.price.max():.0f}")
    print(f"  Time: {df.time_str.iloc[0]} → {df.time_str.iloc[-1]}")
    return df


def load_is():
    print("Loading IS data (BTC 1s, Jul 2025–Feb 2026) → 5-min downsample...")
    chunks = []
    for chunk in pd.read_csv(IS_PATH, usecols=NEEDED_COLS, chunksize=500_000):
        chunk["bar"] = chunk["timestamp"] // IS_DOWNSAMPLE_MS
        chunks.append(chunk.groupby("bar").last().reset_index())
    df = pd.concat(chunks, ignore_index=True)
    df = df.groupby("bar").last().reset_index()
    df = df.sort_values("bar").reset_index(drop=True)
    print(f"  Rows: {len(df)}, Price: {df.price.min():.0f}–{df.price.max():.0f}")
    return df


def compute_states(df):
    mask = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    states = ((bdf["trend_48h"] > 0).astype(int) * 4
              + (bdf["trend_8h"] > 0).astype(int) * 2
              + (bdf["trend_1h"] > 0).astype(int)).values
    macros = np.array([STATE_TO_MACRO[s] for s in states])
    return bdf, states, macros


def extract_episodes(macros, states, prices):
    n = len(macros)
    episodes = []
    i = 0
    while i < n:
        macro = macros[i]
        start = i
        while i < n and macros[i] == macro:
            i += 1
        end = i - 1
        truncated = (start == 0) or (end == n - 1)
        exit_dest = macros[i] if i < n else -1
        episodes.append({
            "macro": macro,
            "duration": end - start + 1,
            "entry_sub": states[start],
            "exit_sub": states[end],
            "exit_dest": exit_dest,
            "entry_price": prices[start],
            "exit_price": prices[end],
            "log_return": np.log(prices[end] / prices[start]) if prices[start] > 0 else 0,
            "start_idx": start,
            "end_idx": end,
            "truncated": truncated,
        })
    return episodes


def wilson_ci(count, n):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = count / n
    denom = 1 + Z * Z / n
    center = (p + Z * Z / (2 * n)) / denom
    spread = Z * np.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / denom
    return p, max(0, center - spread), min(1, center + spread)


def build_features(episodes, bdf, cols=("trend_1h", "trend_8h")):
    X, y = [], []
    for e in episodes:
        X.append([bdf[c].iloc[e["end_idx"]] for c in cols])
        y.append(e["outcome"])
    return np.array(X), np.array(y)


def section(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def subsection(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ═══════════════════════════════════════════════════════════════════════════
#  STEP 0: Distribution Diagnostic
# ═══════════════════════════════════════════════════════════════════════════

def step0_distribution(is_df, oos_df):
    section("STEP 0: Distribution Diagnostic")

    features = ["trend_1h", "trend_8h", "trend_48h"]
    pcts = [5, 25, 50, 75, 95]

    for feat in features:
        subsection(feat)
        is_vals = is_df[feat].dropna().values
        oos_vals = oos_df[feat].dropna().values

        is_std = np.std(is_vals)
        oos_std = np.std(oos_vals)
        var_ratio = oos_std**2 / is_std**2 if is_std > 0 else np.inf
        flag = " *** VARIANCE RATIO > 2x ***" if var_ratio > 2 or var_ratio < 0.5 else ""

        print(f"  {'':>12}  {'IS':>12}  {'OOS':>12}  {'ratio':>8}")
        print(f"  {'mean':>12}  {np.mean(is_vals):>12.6f}  {np.mean(oos_vals):>12.6f}")
        print(f"  {'std':>12}  {is_std:>12.6f}  {oos_std:>12.6f}  {oos_std/is_std:>8.3f}")
        print(f"  {'skew':>12}  {skew(is_vals):>12.4f}  {skew(oos_vals):>12.4f}")
        for p in pcts:
            print(f"  {'p'+str(p):>12}  {np.percentile(is_vals, p):>12.6f}  {np.percentile(oos_vals, p):>12.6f}")
        print(f"  var_ratio: {var_ratio:.4f}{flag}")

    print(f"\n  NOTE: IS trends appear pre-normalized (std ~1), OOS are raw (std ~1e-4).")
    print(f"  Binary state construction (sign-based) is scale-invariant — topology unaffected.")
    print(f"  Logistic models require standardization for cross-domain comparison.")


# ═══════════════════════════════════════════════════════════════════════════
#  PART A: Topology (OOS)
# ═══════════════════════════════════════════════════════════════════════════

def part_a_topology(oos_bdf, oos_states, oos_macros, oos_episodes):
    section("PART A: Topology (OOS)")

    # ── 8×8 transition matrix ──
    subsection("A1: 8×8 Transition Count Matrix")
    counts_8 = np.zeros((N_STATES, N_STATES), dtype=int)
    for i in range(len(oos_states) - 1):
        counts_8[oos_states[i], oos_states[i+1]] += 1

    print("  " + "".join(f"  S{j:d}" for j in range(N_STATES)))
    for i in range(N_STATES):
        row_str = "".join(f"{counts_8[i,j]:>5d}" for j in range(N_STATES))
        print(f"  S{i}{row_str}")

    # Row-normalized
    row_sums = counts_8.sum(axis=1, keepdims=True)
    trans_8 = counts_8 / np.maximum(row_sums, 1)

    subsection("A2: 8×8 Transition Probabilities")
    print("  " + "".join(f"    S{j:d}" for j in range(N_STATES)))
    for i in range(N_STATES):
        row_str = "".join(f"{trans_8[i,j]:>6.3f}" for j in range(N_STATES))
        print(f"  S{i}{row_str}")

    # ── Eigenvalues ──
    subsection("A3: Eigenvalues of 8×8 Transition Matrix")
    evals = np.sort(np.abs(np.linalg.eigvals(trans_8)))[::-1]
    print(f"  Eigenvalues (|λ|, descending):")
    for i, ev in enumerate(evals):
        gap = f"  gap={evals[i-1]-ev:.4f}" if i > 0 else ""
        print(f"    λ{i+1} = {ev:.6f}{gap}")

    # Where is the biggest gap after λ1?
    gaps = [evals[i] - evals[i+1] for i in range(len(evals)-1)]
    max_gap_idx = np.argmax(gaps[1:]) + 1  # skip λ1→λ2
    print(f"\n  Largest gap (after λ1): between λ{max_gap_idx+1} and λ{max_gap_idx+2}, "
          f"gap={gaps[max_gap_idx]:.4f}")
    print(f"  → Suggests K={max_gap_idx+1}")

    # ── Complement symmetry ──
    # Under complement equivariance: P(s→j) ≈ P(s⊕7 → j⊕7)
    # So compare trans[s,:] with trans[s^7, perm] where perm[j] = j^7
    subsection("A4: Complement Symmetry (JSD of complement pairs, relabeled)")
    perm = [j ^ 7 for j in range(N_STATES)]  # complement permutation
    print(f"  {'Pair':>10}  {'JSD':>8}")
    jsds = []
    for s in range(4):
        comp = s ^ 7
        row_s = trans_8[s]
        row_comp_relabeled = trans_8[comp][perm]
        jsd = jensenshannon(row_s + 1e-12, row_comp_relabeled + 1e-12)
        jsds.append(jsd)
        print(f"  S{s}↔S{comp}  {jsd:>8.4f}")
    print(f"  Mean JSD: {np.mean(jsds):.4f}")
    print(f"  IS reference mean JSD: 0.051")

    # ── 4×4 macro jump chain ──
    subsection("A5: 4×4 Macro Jump Chain (exclude self-transitions)")
    counts_4 = np.zeros((N_MACRO, N_MACRO), dtype=int)
    for i in range(len(oos_macros) - 1):
        if oos_macros[i] != oos_macros[i+1]:
            counts_4[oos_macros[i], oos_macros[i+1]] += 1

    print("  Count matrix:")
    print("  " + "".join(f"    {MACRO_NAMES[j]:>8}" for j in range(N_MACRO)))
    for i in range(N_MACRO):
        row_str = "".join(f"{counts_4[i,j]:>12d}" for j in range(N_MACRO))
        print(f"  {MACRO_NAMES[i]:>8}{row_str}")

    row_sums_4 = counts_4.sum(axis=1, keepdims=True)
    jump_4 = counts_4 / np.maximum(row_sums_4, 1)

    print("\n  Jump chain (row-normalized):")
    print("  " + "".join(f"  {MACRO_NAMES[j]:>8}" for j in range(N_MACRO)))
    for i in range(N_MACRO):
        row_str = "".join(f"{jump_4[i,j]:>10.4f}" for j in range(N_MACRO))
        print(f"  {MACRO_NAMES[i]:>8}{row_str}")

    # IS reference jump chain
    print("\n  IS reference jump chain:")
    is_ref_jump = np.array([
        [0, 0.925, 0.076, 0.000],
        [0.795, 0, 0.000, 0.205],
        [0.230, 0.000, 0, 0.770],
        [0.005, 0.075, 0.919, 0],
    ])
    print("  " + "".join(f"  {MACRO_NAMES[j]:>8}" for j in range(N_MACRO)))
    for i in range(N_MACRO):
        row_str = "".join(f"{is_ref_jump[i,j]:>10.4f}" for j in range(N_MACRO))
        print(f"  {MACRO_NAMES[i]:>8}{row_str}")

    # Frobenius distance
    frob = np.linalg.norm(jump_4 - is_ref_jump)
    print(f"\n  Frobenius distance (OOS vs IS): {frob:.4f}")

    # ── Structural zeros ──
    subsection("A6: Structural Zeros in 4×4 Jump Chain")
    for i in range(N_MACRO):
        for j in range(N_MACRO):
            if i == j:
                continue
            if counts_4[i, j] == 0:
                print(f"  {MACRO_NAMES[i]} → {MACRO_NAMES[j]}: ZERO (count=0)")
            elif jump_4[i, j] < 0.02:
                print(f"  {MACRO_NAMES[i]} → {MACRO_NAMES[j]}: near-zero (rate={jump_4[i,j]:.4f}, count={counts_4[i,j]})")

    # ── Stationary distribution ──
    subsection("A7: Stationary Distribution (4×4)")
    # Build full transition matrix including self-transitions for stationary calc
    full_4 = np.zeros((N_MACRO, N_MACRO))
    for i in range(len(oos_macros) - 1):
        full_4[oos_macros[i], oos_macros[i+1]] += 1
    full_4 = full_4 / full_4.sum(axis=1, keepdims=True)

    evals4, evecs4 = np.linalg.eig(full_4.T)
    idx = np.argmin(np.abs(evals4 - 1.0))
    pi = np.real(evecs4[:, idx])
    pi = pi / pi.sum()
    for i in range(N_MACRO):
        print(f"  {MACRO_NAMES[i]:>10}: {pi[i]:.4f}")

    # ── Episode extraction ──
    subsection("A8: Episode Breakdown")
    print(f"  Total episodes: {len(oos_episodes)}")
    print(f"  Non-truncated: {sum(1 for e in oos_episodes if not e['truncated'])}")

    print(f"\n  {'Regime':>10}  {'count':>6}  {'mean_dur':>10}  {'med_dur':>10}  {'std_dur':>10}")
    for m in range(N_MACRO):
        eps_m = [e for e in oos_episodes if e["macro"] == m and not e["truncated"]]
        if eps_m:
            durs = [e["duration"] for e in eps_m]
            bars_to_hours = 5 / 60  # 5-min bars to hours
            print(f"  {MACRO_NAMES[m]:>10}  {len(eps_m):>6}  "
                  f"{np.mean(durs)*bars_to_hours:>10.2f}h  "
                  f"{np.median(durs)*bars_to_hours:>10.2f}h  "
                  f"{np.std(durs)*bars_to_hours:>10.2f}h")

    return jump_4


# ═══════════════════════════════════════════════════════════════════════════
#  PART B: Exit Prediction
# ═══════════════════════════════════════════════════════════════════════════

def part_b_exit_prediction(is_bdf, is_states, is_macros, is_episodes,
                            oos_bdf, oos_states, oos_macros, oos_episodes):
    section("PART B: Exit Prediction")

    # ── B1: Bit-flip attribution ──
    subsection("B1: Bit-Flip Attribution at Macro Exits")
    flips = {"trend_1h": 0, "trend_8h": 0, "trend_48h": 0}
    total_exits = 0
    for e in oos_episodes:
        if e["truncated"] or e["exit_dest"] < 0:
            continue
        end_idx = e["end_idx"]
        next_idx = end_idx + 1
        if next_idx >= len(oos_states):
            continue
        s_end = oos_states[end_idx]
        s_next = oos_states[next_idx]
        if STATE_TO_MACRO[s_end] == STATE_TO_MACRO[s_next]:
            continue  # not a macro transition
        total_exits += 1
        xor = s_end ^ s_next
        if xor & 1:
            flips["trend_1h"] += 1
        if xor & 2:
            flips["trend_8h"] += 1
        if xor & 4:
            flips["trend_48h"] += 1

    print(f"  Total macro exits: {total_exits}")
    for bit, name in [(1, "trend_1h (bit 0)"), (2, "trend_8h (bit 1)"), (4, "trend_48h (bit 2)")]:
        key = name.split(" ")[0]
        pct = flips[key] / total_exits * 100 if total_exits > 0 else 0
        print(f"  {name}: {flips[key]} ({pct:.1f}%)")

    # ── B2: S5→bull rate at C2 ──
    subsection("B2: S5→Bull Rate at C2 (OOS)")
    c2_eps = [e for e in oos_episodes if e["macro"] == 2 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]
    s5_eps = [e for e in c2_eps if e["exit_sub"] == 5]  # S5: trend_1h↑ in C2
    s4_eps = [e for e in c2_eps if e["exit_sub"] == 4]  # S4: trend_1h↓ in C2
    s5_bull = sum(1 for e in s5_eps if e["exit_dest"] == 3)
    s4_bull = sum(1 for e in s4_eps if e["exit_dest"] == 3)

    rate_s5, lo_s5, hi_s5 = wilson_ci(s5_bull, len(s5_eps))
    rate_s4, lo_s4, hi_s4 = wilson_ci(s4_bull, len(s4_eps))

    print(f"  S5 (trend_1h↑): {s5_bull}/{len(s5_eps)} → bull rate={rate_s5:.3f} "
          f"[{lo_s5:.3f}, {hi_s5:.3f}]")
    print(f"  S4 (trend_1h↓): {s4_bull}/{len(s4_eps)} → bull rate={rate_s4:.3f} "
          f"[{lo_s4:.3f}, {hi_s4:.3f}]")
    print(f"  IS reference: S5→bull = {IS_REF['s5_bull_rate']:.3f}")
    accept = lo_s5 >= 0.85
    print(f"  Acceptance (>85% lower CI): {'PASS' if accept else 'FAIL'} (lower={lo_s5:.3f})")

    # ── B3: True OOS logistic — IS→OOS and OOS→IS ──
    subsection("B3: True OOS Logistic Regression")

    # Prepare IS C2 episodes
    is_c2 = [e for e in is_episodes if e["macro"] == 2 and not e["truncated"]
             and e["exit_dest"] in (0, 3)]
    for e in is_c2:
        e["outcome"] = 1 if e["exit_dest"] == 3 else 0

    # Prepare OOS C2 episodes
    oos_c2 = [e for e in oos_episodes if e["macro"] == 2 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]
    for e in oos_c2:
        e["outcome"] = 1 if e["exit_dest"] == 3 else 0

    X_is, y_is = build_features(is_c2, is_bdf)
    X_oos, y_oos = build_features(oos_c2, oos_bdf)

    print(f"\n  C2 episodes — IS: {len(is_c2)} (bull={sum(y_is)}), "
          f"OOS: {len(oos_c2)} (bull={sum(y_oos)})")

    # Standardize each dataset independently
    from sklearn.preprocessing import StandardScaler
    sc_is_c2 = StandardScaler().fit(X_is)
    sc_oos_c2 = StandardScaler().fit(X_oos)

    # IS → OOS (standardized)
    print(f"\n  [C2] IS→OOS (standardized):")
    lr_is = LogisticRegression(max_iter=1000)
    lr_is.fit(sc_is_c2.transform(X_is), y_is)
    probs_is_oos = lr_is.predict_proba(sc_oos_c2.transform(X_oos))[:, 1]
    auc_is_oos = roc_auc_score(y_oos, probs_is_oos) if len(set(y_oos)) > 1 else None
    brier_is_oos = brier_score_loss(y_oos, probs_is_oos)
    print(f"    IS std coefs: intercept={lr_is.intercept_[0]:.4f}, "
          f"trend_1h={lr_is.coef_[0][0]:.4f}, trend_8h={lr_is.coef_[0][1]:.4f}")
    print(f"    AUC={auc_is_oos:.4f}, Brier={brier_is_oos:.4f}")

    # OOS → IS (standardized)
    print(f"\n  [C2] OOS→IS (standardized):")
    lr_oos = LogisticRegression(max_iter=1000)
    lr_oos.fit(sc_oos_c2.transform(X_oos), y_oos)
    probs_oos_is = lr_oos.predict_proba(sc_is_c2.transform(X_is))[:, 1]
    auc_oos_is = roc_auc_score(y_is, probs_oos_is) if len(set(y_is)) > 1 else None
    brier_oos_is = brier_score_loss(y_is, probs_oos_is)
    print(f"    OOS std coefs: intercept={lr_oos.intercept_[0]:.4f}, "
          f"trend_1h={lr_oos.coef_[0][0]:.4f}, trend_8h={lr_oos.coef_[0][1]:.4f}")
    print(f"    AUC={auc_oos_is:.4f}, Brier={brier_oos_is:.4f}")

    # ── C1 logistic: IS→OOS and OOS→IS ──
    print(f"\n  --- C1 Reversal Exit ---")
    is_c1 = [e for e in is_episodes if e["macro"] == 1 and not e["truncated"]
             and e["exit_dest"] in (0, 3)]
    for e in is_c1:
        e["outcome"] = 1 if e["exit_dest"] == 3 else 0

    oos_c1 = [e for e in oos_episodes if e["macro"] == 1 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]
    for e in oos_c1:
        e["outcome"] = 1 if e["exit_dest"] == 3 else 0

    X_is_c1, y_is_c1 = build_features(is_c1, is_bdf)
    X_oos_c1, y_oos_c1 = build_features(oos_c1, oos_bdf)

    print(f"  C1 episodes — IS: {len(is_c1)} (bt={sum(y_is_c1)}), "
          f"OOS: {len(oos_c1)} (bt={sum(y_oos_c1)})")

    # Standardize each dataset independently for cross-domain prediction
    from sklearn.preprocessing import StandardScaler
    sc_is_c1 = StandardScaler().fit(X_is_c1)
    sc_oos_c1 = StandardScaler().fit(X_oos_c1)

    for label, X_train, y_train, X_test, y_test, sc_train, sc_test in [
        ("IS→OOS", X_is_c1, y_is_c1, X_oos_c1, y_oos_c1, sc_is_c1, sc_oos_c1),
        ("OOS→IS", X_oos_c1, y_oos_c1, X_is_c1, y_is_c1, sc_oos_c1, sc_is_c1),
    ]:
        if len(set(y_train)) < 2 or len(set(y_test)) < 2:
            print(f"\n  [C1] {label}: SKIPPED (single class)")
            continue
        lr = LogisticRegression(max_iter=1000, class_weight="balanced")
        lr.fit(sc_train.transform(X_train), y_train)
        # Predict on test data using test's own scaler (so z-scores are comparable)
        probs = lr.predict_proba(sc_test.transform(X_test))[:, 1]
        auc = roc_auc_score(y_test, probs)
        brier = brier_score_loss(y_test, probs)
        print(f"\n  [C1] {label} (standardized):")
        print(f"    std coefs: intercept={lr.intercept_[0]:.4f}, "
              f"trend_1h={lr.coef_[0][0]:.4f}, trend_8h={lr.coef_[0][1]:.4f}")
        print(f"    AUC={auc:.4f}, Brier={brier:.4f}")

    # ── B4: Threshold comparison (OOS C2 standalone fit) ──
    subsection("B4: Threshold Comparison (OOS C2 standalone)")
    print("  NOTE: IS and OOS trend features are on different scales")
    print("  (IS std ~1.0, OOS std ~0.0001 — different normalization)")
    print("  Raw coefficients are not comparable. Using standardized features.\n")

    # Standardized fit for coefficient comparison
    from sklearn.preprocessing import StandardScaler
    sc_oos = StandardScaler().fit(X_oos)
    sc_is = StandardScaler().fit(X_is)

    lr_oos_std = LogisticRegression(max_iter=1000)
    lr_oos_std.fit(sc_oos.transform(X_oos), y_oos)

    lr_is_std = LogisticRegression(max_iter=1000)
    lr_is_std.fit(sc_is.transform(X_is), y_is)

    print(f"  Standardized C2 logistic coefficients:")
    print(f"  {'':>12}  {'IS':>10}  {'OOS':>10}  {'ratio':>8}")
    print(f"  {'intercept':>12}  {lr_is_std.intercept_[0]:>10.4f}  {lr_oos_std.intercept_[0]:>10.4f}")
    print(f"  {'trend_1h':>12}  {lr_is_std.coef_[0][0]:>10.4f}  {lr_oos_std.coef_[0][0]:>10.4f}  "
          f"{lr_oos_std.coef_[0][0]/lr_is_std.coef_[0][0]:>8.2f}" if abs(lr_is_std.coef_[0][0]) > 0.01 else "")
    print(f"  {'trend_8h':>12}  {lr_is_std.coef_[0][1]:>10.4f}  {lr_oos_std.coef_[0][1]:>10.4f}  "
          f"{lr_oos_std.coef_[0][1]/lr_is_std.coef_[0][1]:>8.2f}" if abs(lr_is_std.coef_[0][1]) > 0.01 else "")

    # AUC with standardized features (IS→OOS)
    probs_std_is_oos = lr_is_std.predict_proba(sc_is.transform(X_oos))[:, 1]
    # Note: sc_is transform on OOS data will produce different z-scores
    # The proper cross-domain test: fit on IS standardized, predict on OOS standardized with OOS scaler
    # But AUC only cares about ranking, so let's do both
    probs_cross_same_scaler = lr_is_std.predict_proba(sc_oos.transform(X_oos))[:, 1]
    auc_cross = roc_auc_score(y_oos, probs_cross_same_scaler) if len(set(y_oos)) > 1 else None
    print(f"\n  IS-fitted standardized model → OOS (OOS-scaled): AUC={auc_cross:.4f}")

    # Decision boundary in standardized space
    if abs(lr_oos_std.coef_[0][1]) > 0.01:
        oos_z_threshold = -lr_oos_std.intercept_[0] / lr_oos_std.coef_[0][1]
        is_z_threshold = -lr_is_std.intercept_[0] / lr_is_std.coef_[0][1]
        print(f"\n  Implied trend_8h z-score threshold (at trend_1h=0):")
        print(f"    IS:  z = {is_z_threshold:.4f}  → raw = {is_z_threshold * sc_is.scale_[1] + sc_is.mean_[1]:.4f}")
        print(f"    OOS: z = {oos_z_threshold:.4f}  → raw = {oos_z_threshold * sc_oos.scale_[1] + sc_oos.mean_[1]:.4f}")

    # ── B5: Calibration (IS→OOS, standardized) ──
    subsection("B5: Calibration (IS→OOS, C2, standardized)")
    n_bins = 5
    bin_edges = np.linspace(0, 1, n_bins + 1)
    print(f"  {'Bin':>14}  {'n':>5}  {'pred_mean':>10}  {'actual':>8}")
    for b in range(n_bins):
        if b == n_bins - 1:
            mask = (probs_is_oos >= bin_edges[b]) & (probs_is_oos <= bin_edges[b + 1])
        else:
            mask = (probs_is_oos >= bin_edges[b]) & (probs_is_oos < bin_edges[b + 1])
        n = mask.sum()
        if n == 0:
            continue
        pred_m = probs_is_oos[mask].mean()
        act_m = y_oos[mask].mean()
        print(f"  [{bin_edges[b]:.2f},{bin_edges[b+1]:.2f}]  {n:>5}  {pred_m:>10.4f}  {act_m:>8.4f}")

    # Also show OOS standalone AUC for comparison
    subsection("B6: OOS Standalone Logistic AUC (C2 & C1)")
    lr_oos_only = LogisticRegression(max_iter=1000)
    lr_oos_only.fit(sc_oos_c2.transform(X_oos), y_oos)
    probs_oos_self = lr_oos_only.predict_proba(sc_oos_c2.transform(X_oos))[:, 1]
    auc_oos_self = roc_auc_score(y_oos, probs_oos_self)
    print(f"  C2 OOS in-sample AUC: {auc_oos_self:.4f}")

    lr_oos_c1_only = LogisticRegression(max_iter=1000, class_weight="balanced")
    lr_oos_c1_only.fit(sc_oos_c1.transform(X_oos_c1), y_oos_c1)
    probs_oos_c1_self = lr_oos_c1_only.predict_proba(sc_oos_c1.transform(X_oos_c1))[:, 1]
    auc_oos_c1_self = roc_auc_score(y_oos_c1, probs_oos_c1_self)
    print(f"  C1 OOS in-sample AUC: {auc_oos_c1_self:.4f}")


# ═══════════════════════════════════════════════════════════════════════════
#  PART C: Returns
# ═══════════════════════════════════════════════════════════════════════════

def part_c_returns(oos_episodes):
    section("PART C: Returns")

    # ── C2 exit sub-state returns ──
    subsection("C1: C2 Exit Sub-State Returns (OOS)")
    c2_eps = [e for e in oos_episodes if e["macro"] == 2 and not e["truncated"]
              and e["exit_dest"] == 3]

    s5_bull = [e for e in c2_eps if e["exit_sub"] == 5]
    s4_bull = [e for e in c2_eps if e["exit_sub"] == 4]

    s5_ret = [e["log_return"] for e in s5_bull]
    s4_ret = [e["log_return"] for e in s4_bull]

    print(f"  C2-S5 → C3 (confirmed → bull):")
    print(f"    n={len(s5_ret)}, mean={np.mean(s5_ret)*100:.4f}%, "
          f"std={np.std(s5_ret)*100:.4f}%")
    print(f"    IS ref: +0.09% (n=111)")

    print(f"\n  C2-S4 → C3 (uncertain → bull):")
    print(f"    n={len(s4_ret)}, mean={np.mean(s4_ret)*100:.4f}%, "
          f"std={np.std(s4_ret)*100:.4f}%")
    print(f"    IS ref: −0.17% (n=32)")

    # ── C1 breakthrough vs failure returns ──
    subsection("C2: C1 Breakthrough vs Failure Returns (OOS)")
    c1_eps = [e for e in oos_episodes if e["macro"] == 1 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]

    bt = [e for e in c1_eps if e["exit_dest"] == 3]
    fail = [e for e in c1_eps if e["exit_dest"] == 0]

    bt_ret = [e["log_return"] for e in bt]
    fail_ret = [e["log_return"] for e in fail]

    print(f"  C1 → C3 (breakthrough):")
    print(f"    n={len(bt_ret)}, mean={np.mean(bt_ret)*100:.4f}%, "
          f"std={np.std(bt_ret)*100:.4f}%")
    print(f"    IS ref: +1.09% (n=43)")

    print(f"\n  C1 → C0 (failure):")
    print(f"    n={len(fail_ret)}, mean={np.mean(fail_ret)*100:.4f}%, "
          f"std={np.std(fail_ret)*100:.4f}%")
    print(f"    IS ref: −0.25% (n=167)")

    if bt_ret and fail_ret:
        print(f"\n  Asymmetry ratio (|bt_mean| / |fail_mean|): "
              f"{abs(np.mean(bt_ret)) / abs(np.mean(fail_ret)):.2f}  "
              f"(IS: {abs(0.0109) / abs(0.0025):.2f})")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    oos_df = load_oos()
    is_df = load_is()

    oos_bdf, oos_states, oos_macros = compute_states(oos_df)
    is_bdf, is_states, is_macros = compute_states(is_df)

    oos_episodes = extract_episodes(oos_macros, oos_states, oos_bdf["price"].values)
    is_episodes = extract_episodes(is_macros, is_states, is_bdf["price"].values)

    print(f"\n  OOS: {len(oos_bdf)} bars, {len(oos_episodes)} episodes")
    print(f"  IS:  {len(is_bdf)} bars, {len(is_episodes)} episodes")

    step0_distribution(is_bdf, oos_bdf)
    part_a_topology(oos_bdf, oos_states, oos_macros, oos_episodes)
    part_b_exit_prediction(is_bdf, is_states, is_macros, is_episodes,
                           oos_bdf, oos_states, oos_macros, oos_episodes)
    part_c_returns(oos_episodes)

    section("Phase 12 Complete")


if __name__ == "__main__":
    main()
