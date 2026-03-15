#!/usr/bin/env python3
"""Phase 15: ETH Validation — Ambiguous Zone, Cross-Validation, Cross-Asset Transfer.

Downsamples to 5-min bars, computes OLS trends from scratch (matching Phase 14).
"""

import numpy as np
import pandas as pd
import warnings
from pathlib import Path
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings("ignore")

# ─── Configuration ───────────────────────────────────────────────────────────

BASE = Path(__file__).parent
ETH_PATH = BASE / "data" / "eth_datalog_2025-07-22_2026-02-20.csv"

BAR_MS = 300_000  # 5-minute bars
TREND_WINDOWS = {"trend_1h": 12, "trend_8h": 96, "trend_48h": 576}

MACRO_NAMES = {0: "C0(bear)", 1: "C1(rev)", 2: "C2(pull)", 3: "C3(bull)"}

# ETH fresh-fit coefficients from Phase 14 (fit on 5-min OLS trends)
ETH_C2 = {"const": 6.9062, "t1h": 3274.6, "t8h": 479897.9}
ETH_C1 = {"const": -6.4852, "t1h": 607.6, "t8h": 245163.2}

# BTC production coefficients (fitted on BTC OOS 2023-2024, 5-min OLS)
BTC_C2 = {"const": 5.209, "t1h": 1477.0, "t8h": 348533.0}
BTC_C1 = {"const": -4.890, "t1h": 3138.0, "t8h": 421505.0}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def section(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def subsection(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def predict_logistic(coefs, t1h, t8h):
    logit = coefs["const"] + coefs["t1h"] * t1h + coefs["t8h"] * t8h
    return sigmoid(logit)


def compute_ols_trends_fast(prices):
    """Vectorized OLS trend computation on 5-min bars.

    Matches Phase 14 exactly: slope = OLS on local index 0..w-1,
    fractional_rate = slope / mean_price.
    """
    n = len(prices)
    p = prices.astype(np.float64)
    idx = np.arange(n, dtype=np.float64)
    cum_p = np.cumsum(p)
    cum_ip = np.cumsum(idx * p)
    result = {}

    for name, w in TREND_WINDOWS.items():
        trends = np.full(n, np.nan)
        if n < w:
            result[name] = trends
            continue

        sum_x = w * (w - 1) / 2.0
        sum_x2 = w * (w - 1) * (2 * w - 1) / 6.0
        denom = w * sum_x2 - sum_x * sum_x

        ends = np.arange(w - 1, n)
        starts = ends - w + 1

        sum_y = cum_p[ends].copy()
        mask = starts > 0
        sum_y[mask] -= cum_p[starts[mask] - 1]

        sum_iy = cum_ip[ends].copy()
        sum_iy[mask] -= cum_ip[starts[mask] - 1]

        sum_ky = sum_iy - starts.astype(np.float64) * sum_y
        slope = (w * sum_ky - sum_x * sum_y) / denom
        mean_p = sum_y / w
        frac_rate = np.where(mean_p != 0, slope / mean_p, 0.0)

        trends[w - 1:] = frac_rate
        result[name] = trends

    return result


def compute_macro(t8h, t48h):
    return (t8h > 0).astype(int) + 2 * (t48h > 0).astype(int)


def extract_episodes(macros, prices, trend_1h, trend_8h):
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
        exit_dest = int(macros[i]) if i < n else -1
        episodes.append({
            "macro": int(macro),
            "duration": end - start + 1,
            "exit_dest": exit_dest,
            "exit_t1h": float(trend_1h[end]),
            "exit_t8h": float(trend_8h[end]),
            "entry_price": prices[start],
            "exit_price": prices[end],
            "log_return": float(np.log(prices[end] / prices[start])) if prices[start] > 0 else 0.0,
            "start_idx": start,
            "end_idx": end,
            "truncated": truncated,
        })
    return episodes


# ─── Data Loading ────────────────────────────────────────────────────────────

def load_eth():
    """Load ETH datalog, downsample to 5-min bars, compute OLS trends from price."""
    print(f"Loading ETH from {ETH_PATH.name}...")

    chunks = []
    for chunk in pd.read_csv(ETH_PATH, usecols=["timestamp", "price"], chunksize=2_000_000):
        chunk["bar"] = chunk["timestamp"] // BAR_MS
        chunks.append(chunk.groupby("bar").agg({"price": "last", "timestamp": "last"}).reset_index())

    df = pd.concat(chunks, ignore_index=True)
    df = df.groupby("bar").agg({"price": "last", "timestamp": "last"}).reset_index()
    df = df.sort_values("bar").reset_index(drop=True)

    print(f"  5-min bars: {len(df)}, Price: {df.price.min():.2f}–{df.price.max():.2f}")
    print(f"  Time span: {pd.to_datetime(df.timestamp.iloc[0], unit='ms', utc=True)} → "
          f"{pd.to_datetime(df.timestamp.iloc[-1], unit='ms', utc=True)}")

    # Compute OLS trends from 5-min prices
    print(f"  Computing OLS trends...")
    trends = compute_ols_trends_fast(df["price"].values)
    for name, vals in trends.items():
        df[name] = vals

    # Drop warmup (need 576 bars for trend_48h)
    valid = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    df = df[valid].reset_index(drop=True)
    print(f"  After warmup removal: {len(df)} bars")

    for name in TREND_WINDOWS:
        v = df[name].values
        print(f"  {name}: std={np.std(v):.6e}, p5={np.percentile(v,5):.6e}, p95={np.percentile(v,95):.6e}")

    return df


# ═══════════════════════════════════════════════════════════════════════════
#  15a: Ambiguous Zone Count
# ═══════════════════════════════════════════════════════════════════════════

def analysis_15a(episodes):
    section("15a: Ambiguous Zone Count")

    for regime, coefs, label, dest_label in [
        (2, ETH_C2, "C2", "bull"),
        (1, ETH_C1, "C1", "bt"),
    ]:
        subsection(f"{label} exits — ETH fresh-fit coefficients")

        eps = [e for e in episodes if e["macro"] == regime
               and not e["truncated"] and e["exit_dest"] in (0, 3)]

        t1h = np.array([e["exit_t1h"] for e in eps])
        t8h = np.array([e["exit_t8h"] for e in eps])
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in eps])
        prob = predict_logistic(coefs, t1h, t8h)

        print(f"  Total episodes: {len(eps)} ({dest_label}={sum(y)}, other={len(y)-sum(y)})")

        # Bin into deciles
        bin_edges = np.arange(0, 1.1, 0.1)
        print(f"\n  {'Bin':>14}  {'n':>5}  {'actual_rate':>12}")
        amb_count = 0
        for k in range(len(bin_edges) - 1):
            lo, hi = bin_edges[k], bin_edges[k + 1]
            if hi >= 1.0:
                mask = (prob >= lo) & (prob <= hi)
            else:
                mask = (prob >= lo) & (prob < hi)
            n = mask.sum()
            if n == 0:
                print(f"  [{lo:.1f},{hi:.1f}]  {0:>5}       —")
                continue
            actual = y[mask].mean()
            print(f"  [{lo:.1f},{hi:.1f}]  {n:>5}  {actual:>12.4f}")
            if 0.2 <= lo < 0.8:
                amb_count += n

        print(f"\n  Ambiguous zone [0.2, 0.8]: {amb_count} episodes")
        if amb_count < 30:
            print(f"  → Bimodal separation confirmed, question closed")
        else:
            print(f"  → Needs investigation ({amb_count} ≥ 30)")


# ═══════════════════════════════════════════════════════════════════════════
#  15b: ETH Cross-Validated AUC (split-half, chronological)
# ═══════════════════════════════════════════════════════════════════════════

def analysis_15b(episodes):
    section("15b: ETH Cross-Validated AUC (chronological split-half)")

    for regime, label, dest_label in [
        (2, "C2", "bull"),
        (1, "C1", "bt"),
    ]:
        subsection(f"{label} exits — chronological CV")

        eps = [e for e in episodes if e["macro"] == regime
               and not e["truncated"] and e["exit_dest"] in (0, 3)]

        t1h = np.array([e["exit_t1h"] for e in eps])
        t8h = np.array([e["exit_t8h"] for e in eps])
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in eps])

        mid = len(eps) // 2
        print(f"  Total: {len(eps)}, H1: {mid}, H2: {len(eps) - mid}")
        print(f"  H1 class balance: pos={sum(y[:mid])}, neg={mid - sum(y[:mid])}")
        print(f"  H2 class balance: pos={sum(y[mid:])}, neg={len(y) - mid - sum(y[mid:])}")

        X = np.column_stack([t1h, t8h])

        aucs = []
        for train_label, train_sl, test_label, test_sl in [
            ("H1", slice(None, mid), "H2", slice(mid, None)),
            ("H2", slice(mid, None), "H1", slice(None, mid)),
        ]:
            X_train, y_train = X[train_sl], y[train_sl]
            X_test, y_test = X[test_sl], y[test_sl]

            if len(set(y_train)) < 2 or len(set(y_test)) < 2:
                print(f"\n  {train_label}→{test_label}: SKIPPED (single class in train or test)")
                aucs.append(None)
                continue

            # No regularization — match the statsmodels logistic from Phase 14
            model = LogisticRegression(C=1e10, max_iter=2000, solver="lbfgs")
            model.fit(X_train, y_train)

            b1, b2 = model.coef_[0]
            b0 = model.intercept_[0]

            prob_test = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, prob_test)
            aucs.append(auc)

            print(f"\n  Train={train_label}, Test={test_label}:")
            print(f"    Coefficients: const={b0:.4f}, trend_1h={b1:.1f}, trend_8h={b2:.1f}")
            if b2 != 0:
                print(f"    Decision boundary (t1h=0): trend_8h = {-b0/b2:.6e}")
            print(f"    AUC: {auc:.4f}")

        if all(a is not None for a in aucs):
            mean_auc = np.mean(aucs)
            print(f"\n  Mean CV AUC: {mean_auc:.4f}")
            if min(aucs) > 0.90:
                print(f"  → Confirmed (both > 0.90)")
            elif min(aucs) < 0.85:
                print(f"  → Fresh-fit likely inflated (min < 0.85)")
            else:
                print(f"  → Marginal (0.85–0.90 range)")


# ═══════════════════════════════════════════════════════════════════════════
#  15c: Cross-Asset Coefficient Transfer (BTC → ETH)
# ═══════════════════════════════════════════════════════════════════════════

def analysis_15c(episodes):
    section("15c: Cross-Asset Coefficient Transfer (BTC production → ETH)")

    for regime, btc_coefs, eth_coefs, label, dest_label in [
        (2, BTC_C2, ETH_C2, "C2", "bull"),
        (1, BTC_C1, ETH_C1, "C1", "bt"),
    ]:
        subsection(f"{label} exits — BTC coefficients applied to ETH")

        eps = [e for e in episodes if e["macro"] == regime
               and not e["truncated"] and e["exit_dest"] in (0, 3)]

        t1h = np.array([e["exit_t1h"] for e in eps])
        t8h = np.array([e["exit_t8h"] for e in eps])
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in eps])

        prob_btc = predict_logistic(btc_coefs, t1h, t8h)
        prob_eth = predict_logistic(eth_coefs, t1h, t8h)

        print(f"  Episodes: {len(eps)} ({dest_label}={sum(y)}, other={len(y)-sum(y)})")

        if len(set(y)) < 2:
            print(f"  SKIPPED: single class")
            continue

        auc_btc = roc_auc_score(y, prob_btc)
        auc_eth = roc_auc_score(y, prob_eth)

        print(f"  AUC (BTC coefficients): {auc_btc:.4f}")
        print(f"  AUC (ETH fresh-fit):    {auc_eth:.4f}")
        print(f"  Δ AUC: {auc_eth - auc_btc:+.4f}")

        # Calibration
        bins = [(0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.0)]
        print(f"\n  Calibration (BTC coefficients on ETH):")
        print(f"  {'Bin':>14}  {'n':>5}  {'pred_mean':>10}  {'actual':>8}")
        for lo, hi in bins:
            if hi >= 1.0:
                mask = (prob_btc >= lo) & (prob_btc <= hi)
            else:
                mask = (prob_btc >= lo) & (prob_btc < hi)
            n = mask.sum()
            if n == 0:
                continue
            pred_m = prob_btc[mask].mean()
            act_m = y[mask].mean()
            print(f"  [{lo:.1f},{hi:.1f}]  {n:>5}  {pred_m:>10.4f}  {act_m:>8.4f}")

        # Portability assessment
        lo_mask = prob_btc < 0.3
        hi_mask = prob_btc > 0.7
        lo_actual = y[lo_mask].mean() if lo_mask.sum() > 0 else float("nan")
        hi_actual = y[hi_mask].mean() if hi_mask.sum() > 0 else float("nan")

        portable = auc_btc > 0.90 and (np.isnan(lo_actual) or lo_actual < 0.3) and (np.isnan(hi_actual) or hi_actual > 0.7)
        print(f"\n  Portability: AUC={auc_btc:.4f}, lo_bin(<0.3)_actual={lo_actual:.4f}, hi_bin(>0.7)_actual={hi_actual:.4f}")
        print(f"  → {'Portable' if portable else 'Needs refit'}")


# ═══════════════════════════════════════════════════════════════════════════
#  Summary
# ═══════════════════════════════════════════════════════════════════════════

def print_summary(episodes):
    section("SUMMARY")

    # 15a
    for regime, coefs, label in [(2, ETH_C2, "C2"), (1, ETH_C1, "C1")]:
        eps = [e for e in episodes if e["macro"] == regime
               and not e["truncated"] and e["exit_dest"] in (0, 3)]
        t1h = np.array([e["exit_t1h"] for e in eps])
        t8h = np.array([e["exit_t8h"] for e in eps])
        prob = predict_logistic(coefs, t1h, t8h)
        amb = ((prob >= 0.2) & (prob <= 0.8)).sum()
        status = "closed" if amb < 30 else "needs investigation"
        print(f"  15a: {label} ambiguous zone: {amb} episodes in [0.2, 0.8] → {status}")

    # 15b
    print()
    for regime, label in [(2, "C2"), (1, "C1")]:
        eps = [e for e in episodes if e["macro"] == regime
               and not e["truncated"] and e["exit_dest"] in (0, 3)]
        t1h = np.array([e["exit_t1h"] for e in eps])
        t8h = np.array([e["exit_t8h"] for e in eps])
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in eps])
        X = np.column_stack([t1h, t8h])
        mid = len(eps) // 2
        aucs = []
        for train_sl, test_sl in [(slice(None, mid), slice(mid, None)),
                                   (slice(mid, None), slice(None, mid))]:
            if len(set(y[train_sl])) < 2 or len(set(y[test_sl])) < 2:
                aucs.append(None)
                continue
            m = LogisticRegression(C=1e10, max_iter=2000, solver="lbfgs").fit(X[train_sl], y[train_sl])
            aucs.append(roc_auc_score(y[test_sl], m.predict_proba(X[test_sl])[:, 1]))
        if all(a is not None for a in aucs):
            status = "confirmed" if min(aucs) > 0.90 else ("inflated" if min(aucs) < 0.85 else "marginal")
            print(f"  15b: ETH CV AUC {label} = {aucs[0]:.4f}/{aucs[1]:.4f} → {status}")
        else:
            print(f"  15b: ETH CV AUC {label} = N/A")

    # 15c
    print()
    for regime, btc_coefs, label in [(2, BTC_C2, "C2"), (1, BTC_C1, "C1")]:
        eps = [e for e in episodes if e["macro"] == regime
               and not e["truncated"] and e["exit_dest"] in (0, 3)]
        t1h = np.array([e["exit_t1h"] for e in eps])
        t8h = np.array([e["exit_t8h"] for e in eps])
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in eps])
        prob = predict_logistic(btc_coefs, t1h, t8h)
        if len(set(y)) < 2:
            print(f"  15c: BTC→ETH transfer {label} AUC = N/A")
            continue
        auc = roc_auc_score(y, prob)
        lo_mask = prob < 0.3
        hi_mask = prob > 0.7
        lo_act = y[lo_mask].mean() if lo_mask.sum() > 0 else float("nan")
        hi_act = y[hi_mask].mean() if hi_mask.sum() > 0 else float("nan")
        portable = auc > 0.90 and (np.isnan(lo_act) or lo_act < 0.3) and (np.isnan(hi_act) or hi_act > 0.7)
        cal_str = "portable" if portable else "needs refit"
        print(f"  15c: BTC→ETH transfer {label} AUC = {auc:.4f} (calibration: {cal_str})")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    df = load_eth()

    macros = compute_macro(df["trend_8h"].values, df["trend_48h"].values)
    episodes = extract_episodes(
        macros, df["price"].values, df["trend_1h"].values, df["trend_8h"].values
    )

    non_trunc = [e for e in episodes if not e["truncated"]]
    print(f"\n  Total episodes: {len(episodes)}, non-truncated: {len(non_trunc)}")
    for m in range(4):
        n = sum(1 for e in non_trunc if e["macro"] == m)
        print(f"    {MACRO_NAMES[m]}: {n}")

    analysis_15a(episodes)
    analysis_15b(episodes)
    analysis_15c(episodes)
    print_summary(episodes)

    section("Phase 15 Complete")


if __name__ == "__main__":
    main()
