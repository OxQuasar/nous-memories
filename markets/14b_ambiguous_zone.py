#!/usr/bin/env python3
"""Phase 14b: Ambiguous-Zone AUC Decomposition on ETH.

Tests whether logistic exit model has discriminative content beyond
proximity-to-zero (mechanical bit-flip detection).

Method: split exits by median |trend_8h|, compute AUC on each half.
- Clear zone (|t8h| ≥ median): model predicts easily (near-mechanical)
- Ambiguous zone (|t8h| < median): tests real discriminative content
"""

import numpy as np
import pandas as pd
import warnings
from pathlib import Path
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

warnings.filterwarnings("ignore")

# ─── Configuration ───────────────────────────────────────────────────────────

BASE = Path(__file__).parent
ETH_PATH = BASE / "data" / "eth_datalog_2025-07-21_2026-03-03.csv"
BAR_MS = 300_000
TREND_WINDOWS = {"trend_1h": 12, "trend_8h": 96, "trend_48h": 576}


# ─── Reused pipeline from Phase 14 ──────────────────────────────────────────

def compute_ols_trends_fast(prices):
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


def load_eth():
    print("Loading ETH data...")
    chunks = []
    for chunk in pd.read_csv(ETH_PATH, usecols=["timestamp", "price"], chunksize=2_000_000):
        chunk["bar"] = chunk["timestamp"] // BAR_MS
        chunks.append(chunk.groupby("bar").agg({"price": "last", "timestamp": "last"}).reset_index())
    df = pd.concat(chunks, ignore_index=True)
    df = df.groupby("bar").agg({"price": "last", "timestamp": "last"}).reset_index()
    df = df.sort_values("bar").reset_index(drop=True)
    print(f"  5-min bars: {len(df)}")

    print("  Computing OLS trends...")
    trends = compute_ols_trends_fast(df["price"].values)
    for name, vals in trends.items():
        df[name] = vals
    valid = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    df = df[valid].reset_index(drop=True)
    print(f"  After warmup: {len(df)} bars")
    return df


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
            "truncated": truncated,
        })
    return episodes


# ─── Ambiguous-zone analysis ────────────────────────────────────────────────

def analyze_zone(label, episodes, target_dest):
    """Full ambiguous-zone AUC decomposition for one exit type."""
    print(f"\n{'=' * 70}")
    print(f"  {label}")
    print(f"{'=' * 70}")

    y = np.array([1 if e["exit_dest"] == target_dest else 0 for e in episodes])
    X_raw = np.column_stack([
        [e["exit_t1h"] for e in episodes],
        [e["exit_t8h"] for e in episodes],
    ])
    abs_t8h = np.abs(X_raw[:, 1])

    n_pos, n_neg = y.sum(), len(y) - y.sum()
    print(f"\n  Total: n={len(y)}, positive={n_pos}, negative={n_neg}")

    # Fit logistic on z-scored features (all data)
    scaler = StandardScaler().fit(X_raw)
    X_z = scaler.transform(X_raw)
    X_z_const = sm.add_constant(X_z)
    model = sm.Logit(y, X_z_const).fit(disp=0, maxiter=500)
    pred = model.predict(X_z_const)

    # Convert to raw-scale coefficients for reporting
    b0_z, b1_z, b2_z = model.params
    s1, s2 = scaler.scale_
    m1, m2 = scaler.mean_
    b0_raw = b0_z - b1_z * m1 / s1 - b2_z * m2 / s2
    b1_raw = b1_z / s1
    b2_raw = b2_z / s2

    overall_auc = roc_auc_score(y, pred)
    print(f"  Overall AUC (in-sample): {overall_auc:.4f}")
    print(f"  Coefficients (z-scored): const={b0_z:.4f}, t1h={b1_z:.4f}, t8h={b2_z:.4f}")
    print(f"  Coefficients (raw):      const={b0_raw:.4f}, t1h={b1_raw:.1f}, t8h={b2_raw:.1f}")

    if b2_raw != 0:
        db = -b0_raw / b2_raw
        print(f"  Decision boundary (t1h=0): trend_8h = {db:.6e}")

    # ── Split by median |trend_8h| ──
    median_abs_t8h = np.median(abs_t8h)
    print(f"\n  Median |trend_8h|: {median_abs_t8h:.6e}")

    amb_mask = abs_t8h < median_abs_t8h
    clr_mask = ~amb_mask

    for zone_name, mask in [("AMBIGUOUS (|t8h| < median)", amb_mask),
                             ("CLEAR (|t8h| ≥ median)", clr_mask)]:
        n_zone = mask.sum()
        y_zone = y[mask]
        pred_zone = pred[mask]
        n_pos_z = y_zone.sum()
        n_neg_z = n_zone - n_pos_z

        print(f"\n  {zone_name}:")
        print(f"    n={n_zone}, positive={n_pos_z}, negative={n_neg_z}")
        print(f"    |trend_8h| range: [{abs_t8h[mask].min():.6e}, {abs_t8h[mask].max():.6e}]")

        if len(set(y_zone)) < 2:
            print(f"    AUC: N/A (single class)")
        elif min(n_pos_z, n_neg_z) < 5:
            print(f"    AUC: N/A (minority class n={min(n_pos_z, n_neg_z)} < 5)")
        else:
            zone_auc = roc_auc_score(y_zone, pred_zone)
            print(f"    AUC: {zone_auc:.4f}")

        # Show prediction distribution in this zone
        print(f"    Prediction quantiles: "
              f"p5={np.percentile(pred_zone, 5):.4f}, "
              f"p25={np.percentile(pred_zone, 25):.4f}, "
              f"p50={np.percentile(pred_zone, 50):.4f}, "
              f"p75={np.percentile(pred_zone, 75):.4f}, "
              f"p95={np.percentile(pred_zone, 95):.4f}")

    # ── Tertile decomposition (finer granularity) ──
    print(f"\n  Tertile decomposition:")
    t33 = np.percentile(abs_t8h, 33.3)
    t67 = np.percentile(abs_t8h, 66.7)
    tertiles = [
        ("Bottom third (most ambiguous)", abs_t8h < t33),
        ("Middle third", (abs_t8h >= t33) & (abs_t8h < t67)),
        ("Top third (most clear)", abs_t8h >= t67),
    ]
    print(f"    Boundaries: |t8h| = {t33:.6e}, {t67:.6e}")
    for tname, tmask in tertiles:
        n_t = tmask.sum()
        y_t = y[tmask]
        pred_t = pred[tmask]
        n_pos_t = y_t.sum()
        n_neg_t = n_t - n_pos_t
        if len(set(y_t)) < 2 or min(n_pos_t, n_neg_t) < 3:
            auc_str = f"N/A (pos={n_pos_t}, neg={n_neg_t})"
        else:
            auc_str = f"{roc_auc_score(y_t, pred_t):.4f}"
        print(f"    {tname}: n={n_t}, pos={n_pos_t}, neg={n_neg_t}, AUC={auc_str}")

    return overall_auc


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    eth = load_eth()
    macros = (eth["trend_8h"].values > 0).astype(int) + 2 * (eth["trend_48h"].values > 0).astype(int)
    episodes = extract_episodes(macros, eth["price"].values,
                                eth["trend_1h"].values, eth["trend_8h"].values)
    non_trunc = [e for e in episodes if not e["truncated"]]

    # C2 exits
    c2_eps = [e for e in non_trunc if e["macro"] == 2 and e["exit_dest"] in (0, 3)]
    c2_auc = analyze_zone("C2 Pullback Exit → P(bull)", c2_eps, target_dest=3)

    # C1 exits
    c1_eps = [e for e in non_trunc if e["macro"] == 1 and e["exit_dest"] in (0, 3)]
    c1_auc = analyze_zone("C1 Reversal Exit → P(breakthrough)", c1_eps, target_dest=3)

    # ── Interpretation ──
    print(f"\n{'=' * 70}")
    print(f"  INTERPRETATION")
    print(f"{'=' * 70}")
    print(f"""
  Three-outcome framework:
    A) Ambiguous AUC > 0.8 with n ≥ 20 per class
       → Model has real discriminative content beyond mechanical bit-flip
    B) Ambiguous AUC ~ 0.5-0.6 with decent n
       → AUC was mostly mechanical (proximity to zero crossing)
    C) Ambiguous zone has < 10 in minority class
       → Bimodality makes question moot (model is inherently bimodal)

  The ambiguous zone tests whether trend_1h provides discriminative signal
  when trend_8h alone is insufficient to determine the outcome (near zero).
  If ambiguous AUC ≈ overall AUC, the model works everywhere.
  If ambiguous AUC << overall AUC, the model is mostly reading proximity.
""")


if __name__ == "__main__":
    main()
