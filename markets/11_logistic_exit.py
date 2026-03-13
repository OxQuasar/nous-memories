#!/usr/bin/env python3
"""Phase 11: Logistic Exit Models — P(outcome | continuous features) at each boundary.

Four parts:
  11a: C2 exit — P(bull | trend_1h, trend_8h)
  11b: C1 exit — P(breakthrough | trend_1h, trend_8h)
  11c: Generalization check — C0 and C3 exits
  11d: Summary table
"""

import numpy as np
import pandas as pd
import warnings
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss, average_precision_score
import statsmodels.api as sm

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ─── Configuration ───────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent / "datalog_2025-07-21_2026-02-20.csv"
DOWNSAMPLE_MS = 300_000
NEEDED_COLS = ["timestamp", "price", "trend_1h", "trend_8h", "trend_48h"]

STATE_TO_MACRO = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}
N_MACRO = 4
Z = 1.96

# Scorecard feature values
SCORECARD_T1H = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0]
SCORECARD_T8H = [-2.0, -1.0, -0.5, -0.1, 0.0]
CALIBRATION_BINS = 5


# ─── Helpers ─────────────────────────────────────────────────────────────────

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


def compute_states(df):
    mask = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    bdf = df[mask].copy().reset_index(drop=True)
    states = ((bdf["trend_48h"] > 0).astype(int) * 4
              + (bdf["trend_8h"] > 0).astype(int) * 2
              + (bdf["trend_1h"] > 0).astype(int)).values
    return bdf, states


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


def wilson_ci(count, n):
    if n == 0:
        return 0.0, 0.0, 0.0
    p = count / n
    denom = 1 + Z * Z / n
    center = (p + Z * Z / (2 * n)) / denom
    spread = Z * np.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / denom
    return p, max(0, center - spread), min(1, center + spread)


def safe_auc(y_true, y_score, label="ROC"):
    """AUC that handles single-class folds gracefully."""
    if len(set(y_true)) < 2:
        return None
    return roc_auc_score(y_true, y_score)


def cv_evaluate(X_h1, y_h1, X_h2, y_h2, balanced=False):
    """Cross-validate a logistic model on two halves. Returns dict of metrics."""
    kw = {"class_weight": "balanced"} if balanced else {}
    results = {"fold_aucs": [], "fold_briers": [], "fold_aprcs": []}

    for X_train, y_train, X_test, y_test, fold_name in [
        (X_h1, y_h1, X_h2, y_h2, "H1→H2"),
        (X_h2, y_h2, X_h1, y_h1, "H2→H1"),
    ]:
        if len(set(y_train)) < 2 or len(set(y_test)) < 2:
            print(f"      {fold_name}: SKIPPED (single class in train or test)")
            continue
        lr = LogisticRegression(max_iter=1000, **kw)
        lr.fit(X_train, y_train)
        probs = lr.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probs)
        brier = brier_score_loss(y_test, probs)
        aprc = average_precision_score(y_test, probs)
        results["fold_aucs"].append(auc)
        results["fold_briers"].append(brier)
        results["fold_aprcs"].append(aprc)
        print(f"      {fold_name}: AUC={auc:.4f}  Brier={brier:.4f}  AP={aprc:.4f}")

    if results["fold_aucs"]:
        results["mean_auc"] = np.mean(results["fold_aucs"])
        results["mean_brier"] = np.mean(results["fold_briers"])
        results["mean_aprc"] = np.mean(results["fold_aprcs"])
    else:
        results["mean_auc"] = None
        results["mean_brier"] = None
        results["mean_aprc"] = None
    return results


def build_features(episodes, bdf, feature_cols):
    """Extract feature matrix and labels from episodes."""
    X_rows = []
    y = []
    for e in episodes:
        row = [bdf[col].iloc[e["end_idx"]] for col in feature_cols]
        X_rows.append(row)
        y.append(e["outcome"])
    return np.array(X_rows), np.array(y)


# ═══════════════════════════════════════════════════════════════════════════
#  PART 11a: C2 Exit — P(bull | trend_1h, trend_8h)
# ═══════════════════════════════════════════════════════════════════════════

def part_11a(episodes, bdf, ts_mid):
    print(f"\n{'=' * 70}")
    print("  PART 11a: C2 Exit — P(bull | trend_1h, trend_8h)")
    print(f"{'=' * 70}")

    # Filter C2 episodes, non-truncated, exit to bear(0) or bull(3)
    c2 = [e for e in episodes if e["macro"] == 2 and not e["truncated"]
          and e["exit_dest"] in (0, 3)]
    for e in c2:
        e["outcome"] = 1 if e["exit_dest"] == 3 else 0
        e["ts"] = bdf["timestamp"].iloc[e["end_idx"]]

    print(f"  C2 episodes: {len(c2)}")
    print(f"  Bull exits: {sum(e['outcome'] for e in c2)}, Bear exits: {sum(1 - e['outcome'] for e in c2)}")

    # Split halves by timestamp
    h1_eps = [e for e in c2 if e["ts"] <= ts_mid]
    h2_eps = [e for e in c2 if e["ts"] > ts_mid]
    print(f"  Half 1: {len(h1_eps)} episodes, Half 2: {len(h2_eps)} episodes")

    X_h1, y_h1 = build_features(h1_eps, bdf, ["trend_1h", "trend_8h"])
    X_h2, y_h2 = build_features(h2_eps, bdf, ["trend_1h", "trend_8h"])

    # ── Model comparison ──
    models = {
        "M1: trend_1h only": (X_h1[:, [0]], X_h2[:, [0]]),
        "M2: trend_1h + trend_8h": (X_h1[:, :2], X_h2[:, :2]),
        "M3: t1h + t8h + t1h×t8h": (
            np.column_stack([X_h1[:, :2], X_h1[:, 0] * X_h1[:, 1]]),
            np.column_stack([X_h2[:, :2], X_h2[:, 0] * X_h2[:, 1]]),
        ),
    }

    print(f"\n  Cross-validated model comparison:")
    model_results = {}
    for name, (Xh1, Xh2) in models.items():
        print(f"\n    {name}:")
        res = cv_evaluate(Xh1, y_h1, Xh2, y_h2)
        model_results[name] = res
        if res["mean_auc"] is not None:
            print(f"      → Mean AUC: {res['mean_auc']:.4f}  Mean Brier: {res['mean_brier']:.4f}")

    # Best model by mean AUC
    valid = {k: v for k, v in model_results.items() if v["mean_auc"] is not None}
    best_name = max(valid, key=lambda k: valid[k]["mean_auc"])
    best_res = valid[best_name]
    print(f"\n  Best model: {best_name} (mean AUC = {best_res['mean_auc']:.4f})")

    # ── Full-data fit with statsmodels for inference ──
    print(f"\n{'─' * 60}")
    print(f"  Full-data logistic regression ({best_name})")
    print(f"{'─' * 60}")

    X_full, y_full = build_features(c2, bdf, ["trend_1h", "trend_8h"])
    if "interaction" in best_name or "×" in best_name:
        X_sm = np.column_stack([X_full, X_full[:, 0] * X_full[:, 1]])
        feat_names = ["trend_1h", "trend_8h", "t1h×t8h"]
    elif "trend_8h" in best_name:
        X_sm = X_full[:, :2]
        feat_names = ["trend_1h", "trend_8h"]
    else:
        X_sm = X_full[:, [0]]
        feat_names = ["trend_1h"]

    X_sm_c = sm.add_constant(X_sm)
    try:
        logit_model = sm.Logit(y_full, X_sm_c).fit(disp=0)
        print(f"\n  Coefficients:")
        for i, name in enumerate(["const"] + feat_names):
            print(f"    {name:>12}: coef={logit_model.params[i]:>8.4f}  "
                  f"p={logit_model.pvalues[i]:.4e}  "
                  f"95%CI=[{logit_model.conf_int()[i][0]:.4f}, {logit_model.conf_int()[i][1]:.4f}]")
        print(f"  Pseudo R²: {logit_model.prsquared:.4f}")
        print(f"  Log-likelihood: {logit_model.llf:.2f}")
        print(f"  AIC: {logit_model.aic:.2f}")
    except Exception as ex:
        print(f"  Statsmodels fit failed: {ex}")
        logit_model = None

    # ── Calibration ──
    if logit_model is not None:
        pred_probs = logit_model.predict(X_sm_c)
        print(f"\n  Calibration (predicted vs actual bull rate, {CALIBRATION_BINS} bins):")
        bin_edges = np.linspace(0, 1, CALIBRATION_BINS + 1)
        print(f"    {'Bin':>12}  {'n':>5}  {'pred_mean':>10}  {'actual':>8}")
        for b in range(CALIBRATION_BINS):
            mask = (pred_probs >= bin_edges[b]) & (pred_probs < bin_edges[b + 1])
            if b == CALIBRATION_BINS - 1:
                mask = (pred_probs >= bin_edges[b]) & (pred_probs <= bin_edges[b + 1])
            n = mask.sum()
            if n == 0:
                continue
            pred_m = pred_probs[mask].mean()
            act_m = y_full[mask].mean()
            print(f"    [{bin_edges[b]:.2f},{bin_edges[b+1]:.2f}]  {n:>5}  {pred_m:>10.4f}  {act_m:>8.4f}")

    # ── Scorecard ──
    if logit_model is not None:
        med_t1h = np.median(X_full[:, 0])
        med_t8h = np.median(X_full[:, 1])
        print(f"\n  Scorecard (medians: trend_1h={med_t1h:.4f}, trend_8h={med_t8h:.4f}):")

        print(f"\n    trend_1h sweep (trend_8h = {med_t8h:.4f}):")
        print(f"    {'trend_1h':>10}  {'P(bull)':>8}")
        for t1h in SCORECARD_T1H:
            row = [1.0, t1h]
            if len(feat_names) >= 2:
                row.append(med_t8h)
            if len(feat_names) >= 3:
                row.append(t1h * med_t8h)
            p = logit_model.predict(np.array([row]))[0]
            print(f"    {t1h:>10.1f}  {p:>8.4f}")

        print(f"\n    trend_8h sweep (trend_1h = {med_t1h:.4f}):")
        print(f"    {'trend_8h':>10}  {'P(bull)':>8}")
        for t8h in SCORECARD_T8H:
            row = [1.0, med_t1h]
            if len(feat_names) >= 2:
                row.append(t8h)
            if len(feat_names) >= 3:
                row.append(med_t1h * t8h)
            p = logit_model.predict(np.array([row]))[0]
            print(f"    {t8h:>10.1f}  {p:>8.4f}")

    # ── Binary baseline comparison ──
    print(f"\n  Binary baseline comparison:")
    binary_probs = np.array([0.918 if bdf["trend_1h"].iloc[e["end_idx"]] > 0 else 0.492 for e in c2])
    binary_auc = safe_auc(y_full, binary_probs)
    print(f"    Binary model AUC: {binary_auc:.4f}" if binary_auc else "    Binary model AUC: N/A")
    print(f"    Best continuous AUC: {best_res['mean_auc']:.4f}")
    if binary_auc:
        print(f"    AUC improvement: {best_res['mean_auc'] - binary_auc:+.4f}")

    return {
        "boundary": "C2→{C0,C3}",
        "n": len(c2),
        "binary_auc": binary_auc,
        "best_model": best_name,
        "cv_auc": best_res["mean_auc"],
        "t8h_adds": model_results["M2: trend_1h + trend_8h"]["mean_auc"] is not None and
                     model_results["M2: trend_1h + trend_8h"]["mean_auc"] >
                     (model_results["M1: trend_1h only"]["mean_auc"] or 0),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  PART 11b: C1 Exit — P(breakthrough | trend_1h, trend_8h)
# ═══════════════════════════════════════════════════════════════════════════

def part_11b(episodes, bdf, ts_mid):
    print(f"\n{'=' * 70}")
    print("  PART 11b: C1 Exit — P(breakthrough | trend_1h, trend_8h)")
    print(f"{'=' * 70}")

    c1 = [e for e in episodes if e["macro"] == 1 and not e["truncated"]
          and e["exit_dest"] in (0, 3)]
    for e in c1:
        e["outcome"] = 1 if e["exit_dest"] == 3 else 0  # breakthrough=1, failure=0
        e["ts"] = bdf["timestamp"].iloc[e["end_idx"]]

    n_bt = sum(e["outcome"] for e in c1)
    n_fail = len(c1) - n_bt
    print(f"  C1 episodes: {len(c1)}")
    print(f"  Breakthroughs (→C3): {n_bt} ({n_bt/len(c1)*100:.1f}%)")
    print(f"  Failures (→C0): {n_fail} ({n_fail/len(c1)*100:.1f}%)")

    h1_eps = [e for e in c1 if e["ts"] <= ts_mid]
    h2_eps = [e for e in c1 if e["ts"] > ts_mid]
    print(f"  Half 1: {len(h1_eps)} episodes ({sum(e['outcome'] for e in h1_eps)} bt)")
    print(f"  Half 2: {len(h2_eps)} episodes ({sum(e['outcome'] for e in h2_eps)} bt)")

    X_h1, y_h1 = build_features(h1_eps, bdf, ["trend_1h", "trend_8h"])
    X_h2, y_h2 = build_features(h2_eps, bdf, ["trend_1h", "trend_8h"])

    models = {
        "M1: trend_1h only": (X_h1[:, [0]], X_h2[:, [0]]),
        "M2: trend_1h + trend_8h": (X_h1[:, :2], X_h2[:, :2]),
        "M3: t1h + t8h + t1h×t8h": (
            np.column_stack([X_h1[:, :2], X_h1[:, 0] * X_h1[:, 1]]),
            np.column_stack([X_h2[:, :2], X_h2[:, 0] * X_h2[:, 1]]),
        ),
    }

    print(f"\n  Cross-validated model comparison (balanced class weights):")
    model_results = {}
    for name, (Xh1, Xh2) in models.items():
        print(f"\n    {name}:")
        res = cv_evaluate(Xh1, y_h1, Xh2, y_h2, balanced=True)
        model_results[name] = res
        if res["mean_auc"] is not None:
            print(f"      → Mean AUC: {res['mean_auc']:.4f}  Mean Brier: {res['mean_brier']:.4f}  Mean AP: {res['mean_aprc']:.4f}")

    valid = {k: v for k, v in model_results.items() if v["mean_auc"] is not None}
    if not valid:
        print("  No valid models (single-class folds)")
        return {"boundary": "C1→{C0,C3}", "n": len(c1), "binary_auc": None,
                "best_model": "N/A", "cv_auc": None, "t8h_adds": False}

    best_name = max(valid, key=lambda k: valid[k]["mean_auc"])
    best_res = valid[best_name]
    print(f"\n  Best model: {best_name} (mean AUC = {best_res['mean_auc']:.4f})")

    # Full-data statsmodels fit
    print(f"\n{'─' * 60}")
    print(f"  Full-data logistic regression ({best_name})")
    print(f"{'─' * 60}")

    X_full, y_full = build_features(c1, bdf, ["trend_1h", "trend_8h"])
    if "×" in best_name:
        X_sm = np.column_stack([X_full, X_full[:, 0] * X_full[:, 1]])
        feat_names = ["trend_1h", "trend_8h", "t1h×t8h"]
    elif "trend_8h" in best_name:
        X_sm = X_full[:, :2]
        feat_names = ["trend_1h", "trend_8h"]
    else:
        X_sm = X_full[:, [0]]
        feat_names = ["trend_1h"]

    X_sm_c = sm.add_constant(X_sm)
    try:
        logit_model = sm.Logit(y_full, X_sm_c).fit(disp=0)
        print(f"\n  Coefficients:")
        for i, name in enumerate(["const"] + feat_names):
            print(f"    {name:>12}: coef={logit_model.params[i]:>8.4f}  "
                  f"p={logit_model.pvalues[i]:.4e}  "
                  f"95%CI=[{logit_model.conf_int()[i][0]:.4f}, {logit_model.conf_int()[i][1]:.4f}]")
        print(f"  Pseudo R²: {logit_model.prsquared:.4f}")
        print(f"  Log-likelihood: {logit_model.llf:.2f}")
        print(f"  AIC: {logit_model.aic:.2f}")
    except Exception as ex:
        print(f"  Statsmodels fit failed: {ex}")

    # Binary baseline: S3→breakthrough rate from Phase 4 data
    # S3 (exit_sub==3) vs S2 (exit_sub==2)
    s3_eps = [e for e in c1 if e["exit_sub"] == 3]
    s2_eps = [e for e in c1 if e["exit_sub"] == 2]
    s3_bt = sum(e["outcome"] for e in s3_eps)
    s2_bt = sum(e["outcome"] for e in s2_eps)
    p_s3 = s3_bt / len(s3_eps) if s3_eps else 0
    p_s2 = s2_bt / len(s2_eps) if s2_eps else 0
    print(f"\n  Sub-state breakdown:")
    print(f"    S3 (trend_1h > 0): n={len(s3_eps)}, bt rate={p_s3:.3f}")
    print(f"    S2 (trend_1h ≤ 0): n={len(s2_eps)}, bt rate={p_s2:.3f}")

    binary_probs = np.array([p_s3 if e["exit_sub"] == 3 else p_s2 for e in c1])
    binary_auc = safe_auc(y_full, binary_probs)
    print(f"\n  Binary baseline comparison:")
    print(f"    Binary model AUC: {binary_auc:.4f}" if binary_auc else "    Binary model AUC: N/A")
    print(f"    Best continuous AUC: {best_res['mean_auc']:.4f}")
    if binary_auc:
        print(f"    AUC improvement: {best_res['mean_auc'] - binary_auc:+.4f}")

    return {
        "boundary": "C1→{C0,C3}",
        "n": len(c1),
        "binary_auc": binary_auc,
        "best_model": best_name,
        "cv_auc": best_res["mean_auc"],
        "t8h_adds": model_results["M2: trend_1h + trend_8h"]["mean_auc"] is not None and
                     model_results["M2: trend_1h + trend_8h"]["mean_auc"] >
                     (model_results["M1: trend_1h only"]["mean_auc"] or 0),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  PART 11c: Generalization Check — C0 and C3 Exits
# ═══════════════════════════════════════════════════════════════════════════

def boundary_check(episodes, bdf, ts_mid, macro, pos_dest, neg_dest, label):
    """Quick CV AUC check for a boundary. Returns summary dict."""
    eps = [e for e in episodes if e["macro"] == macro and not e["truncated"]
           and e["exit_dest"] in (pos_dest, neg_dest)]
    for e in eps:
        e["outcome"] = 1 if e["exit_dest"] == pos_dest else 0
        e["ts"] = bdf["timestamp"].iloc[e["end_idx"]]

    n_pos = sum(e["outcome"] for e in eps)
    n_neg = len(eps) - n_pos
    print(f"\n  {label}: {len(eps)} episodes (pos={n_pos}, neg={n_neg})")

    if len(eps) < 20 or n_pos < 5 or n_neg < 5:
        print(f"    Too few episodes for reliable analysis")
        return {"boundary": label, "n": len(eps), "binary_auc": None,
                "best_model": "N/A", "cv_auc": None, "t8h_adds": False}

    h1_eps = [e for e in eps if e["ts"] <= ts_mid]
    h2_eps = [e for e in eps if e["ts"] > ts_mid]

    X_h1, y_h1 = build_features(h1_eps, bdf, ["trend_1h", "trend_8h"])
    X_h2, y_h2 = build_features(h2_eps, bdf, ["trend_1h", "trend_8h"])

    # Check each fold has both classes
    h1_classes = len(set(y_h1))
    h2_classes = len(set(y_h2))
    if h1_classes < 2 or h2_classes < 2:
        print(f"    Single class in one half (H1 classes={h1_classes}, H2 classes={h2_classes})")
        return {"boundary": label, "n": len(eps), "binary_auc": None,
                "best_model": "N/A", "cv_auc": None, "t8h_adds": False}

    model_aucs = {}
    for mname, Xh1_m, Xh2_m in [
        ("M1: trend_1h", X_h1[:, [0]], X_h2[:, [0]]),
        ("M2: t1h+t8h", X_h1[:, :2], X_h2[:, :2]),
    ]:
        fold_aucs = []
        for Xtr, ytr, Xte, yte in [(Xh1_m, y_h1, Xh2_m, y_h2), (Xh2_m, y_h2, Xh1_m, y_h1)]:
            if len(set(ytr)) < 2 or len(set(yte)) < 2:
                continue
            lr = LogisticRegression(max_iter=1000, class_weight="balanced")
            lr.fit(Xtr, ytr)
            probs = lr.predict_proba(Xte)[:, 1]
            fold_aucs.append(roc_auc_score(yte, probs))
        if fold_aucs:
            model_aucs[mname] = np.mean(fold_aucs)
            print(f"    {mname}: CV AUC = {model_aucs[mname]:.4f}")
        else:
            model_aucs[mname] = None
            print(f"    {mname}: CV AUC = N/A")

    valid = {k: v for k, v in model_aucs.items() if v is not None}
    if not valid:
        print(f"    No continuous signal at this boundary")
        return {"boundary": label, "n": len(eps), "binary_auc": None,
                "best_model": "N/A", "cv_auc": None, "t8h_adds": False}

    best_name = max(valid, key=valid.get)
    best_auc = valid[best_name]

    if best_auc < 0.55:
        print(f"    → No continuous signal at this boundary (best AUC = {best_auc:.4f} < 0.55)")
    else:
        print(f"    → Signal present: {best_name} AUC = {best_auc:.4f}")

    # Binary baseline
    members = {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7]}[macro]
    sub_a, sub_b = members
    X_full, y_full = build_features(eps, bdf, ["trend_1h", "trend_8h"])
    sa_eps = [e for e in eps if e["exit_sub"] == sub_a]
    sb_eps = [e for e in eps if e["exit_sub"] == sub_b]
    pa = sum(e["outcome"] for e in sa_eps) / len(sa_eps) if sa_eps else 0.5
    pb = sum(e["outcome"] for e in sb_eps) / len(sb_eps) if sb_eps else 0.5
    binary_probs = np.array([pb if e["exit_sub"] == sub_b else pa for e in eps])
    binary_auc = safe_auc(y_full, binary_probs)
    if binary_auc is not None:
        print(f"    Binary baseline AUC: {binary_auc:.4f}")

    t8h_adds = ("t8h" in best_name) if best_auc >= 0.55 else False
    m1_auc = model_aucs.get("M1: trend_1h")
    m2_auc = model_aucs.get("M2: t1h+t8h")
    if m1_auc is not None and m2_auc is not None:
        t8h_adds = m2_auc > m1_auc

    return {
        "boundary": label,
        "n": len(eps),
        "binary_auc": binary_auc,
        "best_model": best_name,
        "cv_auc": best_auc,
        "t8h_adds": t8h_adds,
    }


def part_11c(episodes, bdf, ts_mid):
    print(f"\n{'=' * 70}")
    print("  PART 11c: Generalization Check — C0 and C3 Exits")
    print(f"{'=' * 70}")

    # C0 bear: exit to C2 (skip ahead) vs C1 (normal cycle)
    r_c0 = boundary_check(episodes, bdf, ts_mid,
                          macro=0, pos_dest=2, neg_dest=1,
                          label="C0→{C1,C2} (skip vs normal)")

    # C3 bull: exit to C0 (crash) vs C2 (orderly pullback)
    r_c3 = boundary_check(episodes, bdf, ts_mid,
                          macro=3, pos_dest=0, neg_dest=2,
                          label="C3→{C2,C0} (crash vs orderly)")

    return r_c0, r_c3


# ═══════════════════════════════════════════════════════════════════════════
#  PART 11d: Summary Table
# ═══════════════════════════════════════════════════════════════════════════

def part_11d(results):
    print(f"\n{'=' * 70}")
    print("  PART 11d: Summary Table")
    print(f"{'=' * 70}")

    print(f"\n  {'Boundary':<28}  {'n':>4}  {'Binary AUC':>11}  {'Best model':<22}  "
          f"{'CV AUC':>7}  {'AUC gain':>9}  {'t8h adds?':>10}")
    print(f"  {'─' * 28}  {'─' * 4}  {'─' * 11}  {'─' * 22}  {'─' * 7}  {'─' * 9}  {'─' * 10}")

    for r in results:
        b_auc = f"{r['binary_auc']:.4f}" if r['binary_auc'] is not None else "N/A"
        cv_auc = f"{r['cv_auc']:.4f}" if r['cv_auc'] is not None else "N/A"
        gain = ""
        if r['binary_auc'] is not None and r['cv_auc'] is not None:
            gain = f"{r['cv_auc'] - r['binary_auc']:+.4f}"
        t8h = "yes" if r['t8h_adds'] else "no"
        print(f"  {r['boundary']:<28}  {r['n']:>4}  {b_auc:>11}  {r['best_model']:<22}  "
              f"{cv_auc:>7}  {gain:>9}  {t8h:>10}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_and_downsample()
    bdf, states = compute_states(df)
    macro_states = np.array([STATE_TO_MACRO[s] for s in states])
    prices = bdf["price"].values

    print(f"  Working rows: {len(bdf)}")
    print(f"  Price range: {prices.min():.0f} → {prices.max():.0f}")

    episodes = extract_episodes(macro_states, states, prices)
    print(f"  Total regime episodes: {len(episodes)}")

    # Timestamp midpoint (same as Phase 10c)
    ts_mid = (bdf["timestamp"].min() + bdf["timestamp"].max()) / 2
    print(f"  Timestamp midpoint: {ts_mid:.0f}")

    r_c2 = part_11a(episodes, bdf, ts_mid)
    r_c1 = part_11b(episodes, bdf, ts_mid)
    r_c0, r_c3 = part_11c(episodes, bdf, ts_mid)

    part_11d([r_c2, r_c1, r_c0, r_c3])

    print(f"\n{'=' * 70}")
    print("  Phase 11 complete.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
