#!/usr/bin/env python3
"""Phase 14: Forward BTC Validation + ETH Structural Test.

Computation 1: Downsample + compute OLS trends from raw price
Computation 2: BTC Forward — topology check + logistic test
Computation 3: ETH — structural validation + logistic refit
"""

import sys
import numpy as np
import pandas as pd
import warnings
from pathlib import Path
from scipy.spatial.distance import jensenshannon
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")

# ─── Configuration ───────────────────────────────────────────────────────────

BASE = Path(__file__).parent
BTC_FWD_PATH = BASE / "data" / "btc_datalog_2026-02-20_2026-03-13.csv"
ETH_PATH = BASE / "data" / "eth_datalog_2025-07-21_2026-03-03.csv"

BAR_MS = 300_000  # 5-minute bars
TREND_WINDOWS = {"trend_1h": 12, "trend_8h": 96, "trend_48h": 576}

MACRO_NAMES = {0: "C0(bear)", 1: "C1(rev)", 2: "C2(pull)", 3: "C3(bull)"}
N_MACRO = 4

# Production coefficients from Phase 13 (fit on BTC OOS 2023-2024 raw scale)
PROD_C2 = {"const": 5.209, "t1h": 1477.0, "t8h": 348533.0}
PROD_C1 = {"const": -4.890, "t1h": 3138.0, "t8h": 421505.0}

# Reference values
REF_T8H_STD = 1.6e-4  # OOS trend_8h std


# ─── Helpers ─────────────────────────────────────────────────────────────────

def section(title):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def subsection(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def compute_ols_trends(prices):
    """Compute rolling OLS trends for all three timescales.

    For window of n bars: slope = cov(X,Y)/var(X) where X=0..n-1
    Fractional rate = slope / mean_price_in_window
    Uses vectorized rolling computation via stride_tricks.
    """
    n = len(prices)
    result = {}
    for name, w in TREND_WINDOWS.items():
        trends = np.full(n, np.nan)
        if n < w:
            result[name] = trends
            continue
        # Precompute X stats (constant for all windows)
        X = np.arange(w, dtype=np.float64)
        x_mean = X.mean()
        x_var = np.sum((X - x_mean) ** 2)
        # Rolling computation using cumulative sums
        p = prices.astype(np.float64)
        # sum_y[i] = sum of prices[i-w+1..i]
        cum_p = np.cumsum(p)
        cum_px = np.cumsum(p * np.arange(n, dtype=np.float64))
        for i in range(w - 1, n):
            start = i - w + 1
            if start == 0:
                sum_y = cum_p[i]
                sum_xy_raw = cum_px[i]
            else:
                sum_y = cum_p[i] - cum_p[start - 1]
                sum_xy_raw = cum_px[i] - cum_px[start - 1]
            # Adjust: we need sum of Y_k * k where k = 0..w-1
            # Y_k = prices[start+k], so sum(Y_k * k) = sum_xy_raw - start * sum_y
            sum_xy = sum_xy_raw - start * sum_y
            y_mean = sum_y / w
            cov_xy = sum_xy / w - x_mean * y_mean
            slope = cov_xy / (x_var / w)  # = w * cov_xy / x_var
            trends[i] = slope / y_mean if y_mean != 0 else 0.0
        result[name] = trends
    return result


def compute_ols_trends_fast(prices):
    """Vectorized OLS trend computation using cumsum tricks.

    slope = (n*sum(i*y_i) - sum(i)*sum(y_i)) / (n*sum(i^2) - (sum(i))^2)
    fractional_rate = slope / mean_price
    """
    n = len(prices)
    p = prices.astype(np.float64)
    result = {}

    # Global index array
    idx = np.arange(n, dtype=np.float64)

    # Cumulative sums
    cum_p = np.cumsum(p)        # cum_p[i] = sum(p[0..i])
    cum_ip = np.cumsum(idx * p) # cum_ip[i] = sum(j*p[j] for j=0..i)

    for name, w in TREND_WINDOWS.items():
        trends = np.full(n, np.nan)
        if n < w:
            result[name] = trends
            continue

        # For window ending at position i (inclusive), starting at i-w+1:
        # sum_y = cum_p[i] - cum_p[i-w]  (with cum_p[-1]=0 convention)
        # sum_iy = cum_ip[i] - cum_ip[i-w]
        # We need sum over local index k=0..w-1, where y_k = p[start+k]
        # sum(k * y_k) = sum((j - start) * p[j]) = sum_iy - start * sum_y
        # where j = global index, start = i - w + 1

        # Precompute constants for the local regression
        # X = 0, 1, ..., w-1
        sum_x = w * (w - 1) / 2.0
        sum_x2 = w * (w - 1) * (2 * w - 1) / 6.0
        denom = w * sum_x2 - sum_x * sum_x  # = w^2 * var(X)

        # Vectorized: indices where we have full windows
        ends = np.arange(w - 1, n)  # ending positions
        starts = ends - w + 1       # starting positions

        # sum_y for each window
        sum_y = cum_p[ends].copy()
        mask = starts > 0
        sum_y[mask] -= cum_p[starts[mask] - 1]

        # sum_iy (global index weighted) for each window
        sum_iy = cum_ip[ends].copy()
        sum_iy[mask] -= cum_ip[starts[mask] - 1]

        # Convert to local index: sum(k * y_k) = sum_iy - start * sum_y
        sum_ky = sum_iy - starts.astype(np.float64) * sum_y

        # OLS slope: (w * sum_ky - sum_x * sum_y) / denom
        slope = (w * sum_ky - sum_x * sum_y) / denom

        # Mean price in window
        mean_p = sum_y / w

        # Fractional rate
        frac_rate = np.where(mean_p != 0, slope / mean_p, 0.0)

        trends[w - 1:] = frac_rate
        result[name] = trends

    return result


def downsample_and_compute(path, label, chunk_size=2_000_000):
    """Read CSV, downsample to 5-min bars, compute OLS trends."""
    print(f"\nLoading {label} from {path.name}...")

    # Read in chunks, keep only timestamp + price
    chunks = []
    for chunk in pd.read_csv(path, usecols=["timestamp", "price"], chunksize=chunk_size):
        chunk["bar"] = chunk["timestamp"] // BAR_MS
        # Keep last price per bar per chunk
        chunks.append(chunk.groupby("bar").agg({"price": "last", "timestamp": "last"}).reset_index())

    df = pd.concat(chunks, ignore_index=True)
    # Final aggregation across chunk boundaries
    df = df.groupby("bar").agg({"price": "last", "timestamp": "last"}).reset_index()
    df = df.sort_values("bar").reset_index(drop=True)

    print(f"  5-min bars: {len(df)}, Price: {df.price.min():.2f}–{df.price.max():.2f}")
    print(f"  Time span: {pd.to_datetime(df.timestamp.iloc[0], unit='ms', utc=True)} → "
          f"{pd.to_datetime(df.timestamp.iloc[-1], unit='ms', utc=True)}")

    # Compute OLS trends
    print(f"  Computing OLS trends...")
    trends = compute_ols_trends_fast(df["price"].values)
    for name, vals in trends.items():
        df[name] = vals

    # Drop warmup
    valid = df[["trend_1h", "trend_8h", "trend_48h"]].notna().all(axis=1)
    df = df[valid].reset_index(drop=True)
    print(f"  After warmup removal: {len(df)} bars")

    # Print trend stats
    for name in TREND_WINDOWS:
        vals = df[name].values
        print(f"  {name}: mean={np.mean(vals):.6e}, std={np.std(vals):.6e}, "
              f"p5={np.percentile(vals,5):.6e}, p95={np.percentile(vals,95):.6e}")

    return df


def compute_macro(df):
    """2-bit macro regime: macro = (trend_8h > 0) + 2*(trend_48h > 0)."""
    macros = (df["trend_8h"].values > 0).astype(int) + 2 * (df["trend_48h"].values > 0).astype(int)
    return macros


def extract_episodes(macros, prices, trend_1h, trend_8h):
    """Extract consecutive regime episodes with exit features."""
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
            "entry_price": prices[start],
            "exit_price": prices[end],
            "log_return": float(np.log(prices[end] / prices[start])) if prices[start] > 0 else 0.0,
            "exit_t1h": float(trend_1h[end]),
            "exit_t8h": float(trend_8h[end]),
            "start_idx": start,
            "end_idx": end,
            "truncated": truncated,
        })
    return episodes


def build_jump_chain(episodes):
    """Build 4×4 jump chain from episodes (exclude self-transitions)."""
    counts = np.zeros((N_MACRO, N_MACRO), dtype=int)
    for e in episodes:
        if e["truncated"] or e["exit_dest"] < 0:
            continue
        if e["macro"] != e["exit_dest"]:
            counts[e["macro"], e["exit_dest"]] += 1
    row_sums = counts.sum(axis=1, keepdims=True)
    jump = counts / np.maximum(row_sums, 1)
    return counts, jump


def compute_8state(df):
    """3-bit state: trend_1h × trend_8h × trend_48h."""
    states = ((df["trend_48h"].values > 0).astype(int) * 4
              + (df["trend_8h"].values > 0).astype(int) * 2
              + (df["trend_1h"].values > 0).astype(int))
    return states


def eigenvalue_analysis(states_8):
    """8×8 transition matrix eigenvalue analysis for K detection."""
    N = 8
    full = np.zeros((N, N))
    for i in range(len(states_8) - 1):
        full[states_8[i], states_8[i + 1]] += 1
    row_sums = full.sum(axis=1, keepdims=True)
    full = full / np.maximum(row_sums, 1)

    evals = np.sort(np.abs(np.linalg.eigvals(full)))[::-1]
    gaps = [float(evals[i] - evals[i + 1]) for i in range(len(evals) - 1)]
    # Skip λ1→λ2 gap (trivial), find largest gap after that
    max_gap_idx = np.argmax(gaps[1:]) + 1
    K = max_gap_idx + 1

    return evals, gaps, K


def stationary_distribution(macros):
    """Compute stationary distribution from full transition matrix."""
    full = np.zeros((N_MACRO, N_MACRO))
    for i in range(len(macros) - 1):
        full[macros[i], macros[i + 1]] += 1
    full = full / full.sum(axis=1, keepdims=True)

    evals, evecs = np.linalg.eig(full.T)
    idx = np.argmin(np.abs(evals - 1.0))
    pi = np.real(evecs[:, idx])
    pi = pi / pi.sum()
    return pi


def complement_jsd(jump):
    """JSD between complement pairs in the jump chain.
    Complement pairs: (C0,C3) and (C1,C2).
    C0↔C3: compare row C0 with row C3 permuted by [3,2,1,0]
    C1↔C2: compare row C1 with row C2 permuted by [3,2,1,0]
    """
    perm = [3, 2, 1, 0]  # complement: 0↔3, 1↔2
    jsds = []
    for a, b in [(0, 3), (1, 2)]:
        row_a = jump[a] + 1e-12
        row_b = jump[b][perm] + 1e-12
        jsd = float(jensenshannon(row_a, row_b))
        jsds.append(jsd)
    return jsds, np.mean(jsds)


def print_topology(label, macros, states_8, episodes):
    """Full topology printout."""
    subsection(f"{label}: Topology")

    counts, jump = build_jump_chain(episodes)

    # Jump chain
    print(f"\n  Jump chain counts:")
    print("  " + "".join(f"  {MACRO_NAMES[j]:>8}" for j in range(N_MACRO)))
    for i in range(N_MACRO):
        row_str = "".join(f"{counts[i, j]:>10d}" for j in range(N_MACRO))
        print(f"  {MACRO_NAMES[i]:>8}{row_str}")

    print(f"\n  Jump chain probabilities:")
    print("  " + "".join(f"  {MACRO_NAMES[j]:>8}" for j in range(N_MACRO)))
    for i in range(N_MACRO):
        row_str = "".join(f"{jump[i, j]:>10.4f}" for j in range(N_MACRO))
        print(f"  {MACRO_NAMES[i]:>8}{row_str}")

    # Eigenvalues + K (from 8×8 state matrix)
    evals, gaps, K = eigenvalue_analysis(states_8)
    print(f"\n  Eigenvalues of 8×8 transition matrix (|λ|, descending):")
    for i, ev in enumerate(evals):
        gap_str = f"  gap={gaps[i-1]:.4f}" if i > 0 else ""
        print(f"    λ{i + 1} = {ev:.6f}{gap_str}")
    print(f"  K = {K} (largest gap after λ1: between λ{K} and λ{K+1}, gap={gaps[K-1]:.4f})")

    # Structural zeros
    print(f"\n  Structural zeros (< 0.01):")
    zeros_found = 0
    for i in range(N_MACRO):
        for j in range(N_MACRO):
            if i == j:
                continue
            if counts[i, j] == 0:
                print(f"    {MACRO_NAMES[i]} → {MACRO_NAMES[j]}: ZERO")
                zeros_found += 1
            elif jump[i, j] < 0.01:
                print(f"    {MACRO_NAMES[i]} → {MACRO_NAMES[j]}: {jump[i, j]:.4f} (n={counts[i, j]})")
                zeros_found += 1
    if zeros_found == 0:
        print(f"    None found")

    # Complement symmetry
    jsds, mean_jsd = complement_jsd(jump)
    print(f"\n  Complement symmetry JSD:")
    print(f"    (C0,C3): {jsds[0]:.4f}")
    print(f"    (C1,C2): {jsds[1]:.4f}")
    print(f"    Mean: {mean_jsd:.4f}")

    # Stationary distribution
    pi = stationary_distribution(macros)
    print(f"\n  Stationary distribution:")
    for i in range(N_MACRO):
        print(f"    {MACRO_NAMES[i]:>10}: {pi[i]:.4f}")

    # Episode stats
    non_trunc = [e for e in episodes if not e["truncated"]]
    print(f"\n  Episodes: {len(episodes)} total, {len(non_trunc)} non-truncated")
    print(f"  {'Regime':>10}  {'count':>6}  {'mean_dur_h':>10}  {'med_dur_h':>10}")
    for m in range(N_MACRO):
        eps_m = [e for e in non_trunc if e["macro"] == m]
        if eps_m:
            durs = np.array([e["duration"] for e in eps_m]) * 5 / 60  # bars → hours
            print(f"  {MACRO_NAMES[m]:>10}  {len(eps_m):>6}  {np.mean(durs):>10.2f}  {np.median(durs):>10.2f}")

    return counts, jump, K, mean_jsd


# ═══════════════════════════════════════════════════════════════════════════
#  COMPUTATION 1: Downsample + Compute Raw Trends
# ═══════════════════════════════════════════════════════════════════════════

def computation_1():
    section("COMPUTATION 1: Downsample + Compute Raw Trends")

    btc = downsample_and_compute(BTC_FWD_PATH, "BTC Forward (Feb-Mar 2026)")

    # SANITY GATE
    t8h_std = np.std(btc["trend_8h"].values)
    print(f"\n  SANITY GATE: trend_8h std = {t8h_std:.6e}")
    print(f"  Reference OOS std = {REF_T8H_STD:.6e}")
    print(f"  Acceptable range: [{0.5 * REF_T8H_STD:.6e}, {2.0 * REF_T8H_STD:.6e}]")
    if t8h_std < 0.5 * REF_T8H_STD or t8h_std > 2.0 * REF_T8H_STD:
        print(f"  *** SANITY GATE FAILED ***")
        print(f"  Ratio to reference: {t8h_std / REF_T8H_STD:.4f}")
        print(f"  STOPPING — trends may be computed incorrectly.")
        sys.exit(1)
    print(f"  Ratio to reference: {t8h_std / REF_T8H_STD:.4f} — PASS")

    eth = downsample_and_compute(ETH_PATH, "ETH (Jul 2025–Mar 2026)")

    return btc, eth


# ═══════════════════════════════════════════════════════════════════════════
#  COMPUTATION 2: BTC Forward — Topology Check + Logistic Test
# ═══════════════════════════════════════════════════════════════════════════

def computation_2(btc):
    section("COMPUTATION 2: BTC Forward Validation")

    macros = compute_macro(btc)
    states_8 = compute_8state(btc)
    prices = btc["price"].values
    t1h = btc["trend_1h"].values
    t8h = btc["trend_8h"].values
    episodes = extract_episodes(macros, prices, t1h, t8h)

    total_eps = len([e for e in episodes if not e["truncated"]])
    print(f"\n  Total non-truncated episodes: {total_eps}")
    if total_eps < 150:
        print(f"  NOTE: Below 150 minimum for full validation — topology check only")

    # Topology
    counts, jump, K, mean_jsd = print_topology("BTC Forward", macros, states_8, episodes)

    # ── Logistic test: C2 exits ──
    subsection("BTC Forward: C2 Logistic Test (production coefficients)")

    c2_eps = [e for e in episodes if e["macro"] == 2 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]

    if len(c2_eps) < 5:
        print(f"  Only {len(c2_eps)} C2 exit episodes — too few for logistic test")
    else:
        y_c2 = np.array([1 if e["exit_dest"] == 3 else 0 for e in c2_eps])
        t1h_c2 = np.array([e["exit_t1h"] for e in c2_eps])
        t8h_c2 = np.array([e["exit_t8h"] for e in c2_eps])

        logit = PROD_C2["const"] + PROD_C2["t1h"] * t1h_c2 + PROD_C2["t8h"] * t8h_c2
        prob = 1.0 / (1.0 + np.exp(-logit))

        print(f"  C2 exit episodes: {len(c2_eps)} (bull={sum(y_c2)}, bear={len(y_c2)-sum(y_c2)})")

        if len(set(y_c2)) > 1:
            auc_all = roc_auc_score(y_c2, prob)
            print(f"  AUC (overall): {auc_all:.4f}")

            # Ambiguous zone: |trend_8h| < median
            median_t8h = np.median(np.abs(t8h_c2))
            amb_mask = np.abs(t8h_c2) < median_t8h
            if len(set(y_c2[amb_mask])) > 1 and amb_mask.sum() > 5:
                auc_amb = roc_auc_score(y_c2[amb_mask], prob[amb_mask])
                print(f"  Median |trend_8h|: {median_t8h:.6e}")
                print(f"  AUC (ambiguous zone, |t8h| < median): {auc_amb:.4f} (n={amb_mask.sum()})")
            else:
                print(f"  Ambiguous zone: insufficient class diversity (n={amb_mask.sum()})")
        else:
            print(f"  AUC: SKIPPED (single class — all outcomes are {'bull' if y_c2[0] else 'bear'})")

        # Decision boundary
        if PROD_C2["t8h"] != 0:
            db = -PROD_C2["const"] / PROD_C2["t8h"]
            print(f"  Decision boundary (t1h=0): trend_8h = {db:.6e}")

    # ── Logistic test: C1 exits ──
    subsection("BTC Forward: C1 Logistic Test (production coefficients)")

    c1_eps = [e for e in episodes if e["macro"] == 1 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]

    if len(c1_eps) < 5:
        print(f"  Only {len(c1_eps)} C1 exit episodes — too few for logistic test")
    else:
        y_c1 = np.array([1 if e["exit_dest"] == 3 else 0 for e in c1_eps])
        t1h_c1 = np.array([e["exit_t1h"] for e in c1_eps])
        t8h_c1 = np.array([e["exit_t8h"] for e in c1_eps])

        logit = PROD_C1["const"] + PROD_C1["t1h"] * t1h_c1 + PROD_C1["t8h"] * t8h_c1
        prob = 1.0 / (1.0 + np.exp(-logit))

        print(f"  C1 exit episodes: {len(c1_eps)} (bt={sum(y_c1)}, fail={len(y_c1)-sum(y_c1)})")

        if len(set(y_c1)) > 1:
            auc_all = roc_auc_score(y_c1, prob)
            print(f"  AUC (overall): {auc_all:.4f}")

            median_t8h = np.median(np.abs(t8h_c1))
            amb_mask = np.abs(t8h_c1) < median_t8h
            if len(set(y_c1[amb_mask])) > 1 and amb_mask.sum() > 5:
                auc_amb = roc_auc_score(y_c1[amb_mask], prob[amb_mask])
                print(f"  Median |trend_8h|: {median_t8h:.6e}")
                print(f"  AUC (ambiguous zone, |t8h| < median): {auc_amb:.4f} (n={amb_mask.sum()})")
            else:
                print(f"  Ambiguous zone: insufficient class diversity (n={amb_mask.sum()})")
        else:
            print(f"  AUC: SKIPPED (single class — all outcomes are {'bt' if y_c1[0] else 'fail'})")

        if PROD_C1["t8h"] != 0:
            db = -PROD_C1["const"] / PROD_C1["t8h"]
            print(f"  Decision boundary (t1h=0): trend_8h = {db:.6e}")

    return episodes, macros, states_8


# ═══════════════════════════════════════════════════════════════════════════
#  COMPUTATION 3: ETH Structural Validation
# ═══════════════════════════════════════════════════════════════════════════

def computation_3(eth):
    section("COMPUTATION 3: ETH Structural Validation")

    macros = compute_macro(eth)
    states_8 = compute_8state(eth)
    prices = eth["price"].values
    t1h = eth["trend_1h"].values
    t8h = eth["trend_8h"].values
    episodes = extract_episodes(macros, prices, t1h, t8h)

    # Topology
    counts, jump, K, mean_jsd = print_topology("ETH", macros, states_8, episodes)

    # ── Logistic refit: C2 exits ──
    subsection("ETH: C2 Logistic Refit (fresh fit, NOT BTC coefficients)")

    c2_eps = [e for e in episodes if e["macro"] == 2 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]

    eth_c2_auc = None
    eth_c2_db = None
    if len(c2_eps) < 10:
        print(f"  Only {len(c2_eps)} C2 exit episodes — too few")
    else:
        import statsmodels.api as sm
        from sklearn.preprocessing import StandardScaler

        y_c2 = np.array([1 if e["exit_dest"] == 3 else 0 for e in c2_eps])
        X_c2_raw = np.column_stack([
            [e["exit_t1h"] for e in c2_eps],
            [e["exit_t8h"] for e in c2_eps],
        ])

        print(f"  C2 exit episodes: {len(c2_eps)} (bull={sum(y_c2)}, bear={len(y_c2)-sum(y_c2)})")

        # Fit on z-scored features, then convert to raw scale
        scaler = StandardScaler().fit(X_c2_raw)
        X_c2_z = scaler.transform(X_c2_raw)
        X_c2_z_const = sm.add_constant(X_c2_z)

        try:
            model = sm.Logit(y_c2, X_c2_z_const).fit(disp=0, maxiter=500)

            # Convert z-scored coefficients to raw scale
            # logit = b0 + b1*z1 + b2*z2 = b0 + b1*(x1-m1)/s1 + b2*(x2-m2)/s2
            #       = (b0 - b1*m1/s1 - b2*m2/s2) + (b1/s1)*x1 + (b2/s2)*x2
            b0_z, b1_z, b2_z = model.params
            s1, s2 = scaler.scale_
            m1, m2 = scaler.mean_
            b0_raw = b0_z - b1_z * m1 / s1 - b2_z * m2 / s2
            b1_raw = b1_z / s1
            b2_raw = b2_z / s2

            print(f"\n  Z-scored coefficients:")
            names_z = ["const", "trend_1h_z", "trend_8h_z"]
            for k, name in enumerate(names_z):
                print(f"    {name:>12}: {model.params[k]:>12.4f}  (p={model.pvalues[k]:.4e})")

            print(f"\n  Raw-scale coefficients:")
            print(f"    {'const':>12}: {b0_raw:>12.4f}")
            print(f"    {'trend_1h':>12}: {b1_raw:>12.1f}")
            print(f"    {'trend_8h':>12}: {b2_raw:>12.1f}")

            # Dominance check (using z-scored impact)
            print(f"\n  Feature impact (|z-coef|):")
            print(f"    trend_1h: {abs(b1_z):.4f}")
            print(f"    trend_8h: {abs(b2_z):.4f}")
            dominant = "trend_8h" if abs(b2_z) > abs(b1_z) else "trend_1h"
            t8h_pval = model.pvalues[2]
            t1h_pval = model.pvalues[1]
            print(f"    Dominant: {dominant} (p={t8h_pval:.4e} vs {t1h_pval:.4e})")

            # AUC
            pred = model.predict(X_c2_z_const)
            if len(set(y_c2)) > 1:
                eth_c2_auc = roc_auc_score(y_c2, pred)
                print(f"\n  AUC (in-sample): {eth_c2_auc:.4f}")

            # Decision boundary at t1h=0 (raw scale)
            if b2_raw != 0:
                eth_c2_db = -b0_raw / b2_raw
                print(f"  Decision boundary (t1h=0): trend_8h = {eth_c2_db:.6e}")

            # Calibration
            print(f"\n  Calibration:")
            bins = [(0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.0)]
            print(f"  {'Bin':>14}  {'n':>5}  {'pred_mean':>10}  {'actual':>8}")
            extreme_mass = 0
            total_n = len(pred)
            for lo, hi in bins:
                if hi == 1.0:
                    mask = (pred >= lo) & (pred <= hi)
                else:
                    mask = (pred >= lo) & (pred < hi)
                n = mask.sum()
                if n == 0:
                    continue
                pred_m = pred[mask].mean()
                act_m = y_c2[mask].mean()
                print(f"  [{lo:.1f},{hi:.1f}]  {n:>5}  {pred_m:>10.4f}  {act_m:>8.4f}")
                if lo <= 0.1 or lo >= 0.9:
                    extreme_mass += n
            bimodal = extreme_mass / total_n > 0.7
            print(f"  Extreme bins mass: {extreme_mass}/{total_n} = {extreme_mass/total_n:.2%} → {'bimodal' if bimodal else 'not bimodal'}")

        except Exception as ex:
            print(f"  Logistic fit failed: {ex}")
            import traceback; traceback.print_exc()

    # ── Logistic refit: C1 exits ──
    subsection("ETH: C1 Logistic Refit (fresh fit)")

    c1_eps = [e for e in episodes if e["macro"] == 1 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]

    eth_c1_auc = None
    eth_c1_db = None
    if len(c1_eps) < 10:
        print(f"  Only {len(c1_eps)} C1 exit episodes — too few")
    else:
        import statsmodels.api as sm
        from sklearn.preprocessing import StandardScaler

        y_c1 = np.array([1 if e["exit_dest"] == 3 else 0 for e in c1_eps])
        X_c1_raw = np.column_stack([
            [e["exit_t1h"] for e in c1_eps],
            [e["exit_t8h"] for e in c1_eps],
        ])

        print(f"  C1 exit episodes: {len(c1_eps)} (bt={sum(y_c1)}, fail={len(y_c1)-sum(y_c1)})")

        scaler = StandardScaler().fit(X_c1_raw)
        X_c1_z = scaler.transform(X_c1_raw)
        X_c1_z_const = sm.add_constant(X_c1_z)

        try:
            model = sm.Logit(y_c1, X_c1_z_const).fit(disp=0, maxiter=500)

            b0_z, b1_z, b2_z = model.params
            s1, s2 = scaler.scale_
            m1, m2 = scaler.mean_
            b0_raw = b0_z - b1_z * m1 / s1 - b2_z * m2 / s2
            b1_raw = b1_z / s1
            b2_raw = b2_z / s2

            print(f"\n  Z-scored coefficients:")
            names_z = ["const", "trend_1h_z", "trend_8h_z"]
            for k, name in enumerate(names_z):
                print(f"    {name:>12}: {model.params[k]:>12.4f}  (p={model.pvalues[k]:.4e})")

            print(f"\n  Raw-scale coefficients:")
            print(f"    {'const':>12}: {b0_raw:>12.4f}")
            print(f"    {'trend_1h':>12}: {b1_raw:>12.1f}")
            print(f"    {'trend_8h':>12}: {b2_raw:>12.1f}")

            print(f"\n  Feature impact (|z-coef|):")
            print(f"    trend_1h: {abs(b1_z):.4f}")
            print(f"    trend_8h: {abs(b2_z):.4f}")
            dominant = "trend_8h" if abs(b2_z) > abs(b1_z) else "trend_1h"
            t8h_pval = model.pvalues[2]
            t1h_pval = model.pvalues[1]
            print(f"    Dominant: {dominant} (p={t8h_pval:.4e} vs {t1h_pval:.4e})")

            pred = model.predict(X_c1_z_const)
            if len(set(y_c1)) > 1:
                eth_c1_auc = roc_auc_score(y_c1, pred)
                print(f"\n  AUC (in-sample): {eth_c1_auc:.4f}")

            if b2_raw != 0:
                eth_c1_db = -b0_raw / b2_raw
                print(f"  Decision boundary (t1h=0): trend_8h = {eth_c1_db:.6e}")

            # Calibration
            print(f"\n  Calibration:")
            bins = [(0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.0)]
            print(f"  {'Bin':>14}  {'n':>5}  {'pred_mean':>10}  {'actual':>8}")
            extreme_mass = 0
            total_n = len(pred)
            for lo, hi in bins:
                if hi == 1.0:
                    mask = (pred >= lo) & (pred <= hi)
                else:
                    mask = (pred >= lo) & (pred < hi)
                n = mask.sum()
                if n == 0:
                    continue
                pred_m = pred[mask].mean()
                act_m = y_c1[mask].mean()
                print(f"  [{lo:.1f},{hi:.1f}]  {n:>5}  {pred_m:>10.4f}  {act_m:>8.4f}")
                if lo <= 0.1 or lo >= 0.9:
                    extreme_mass += n
            bimodal = extreme_mass / total_n > 0.7
            print(f"  Extreme bins mass: {extreme_mass}/{total_n} = {extreme_mass/total_n:.2%} → {'bimodal' if bimodal else 'not bimodal'}")

        except Exception as ex:
            print(f"  Logistic fit failed: {ex}")
            import traceback; traceback.print_exc()

    # ── Returns analysis ──
    subsection("ETH: Returns Analysis")

    non_trunc = [e for e in episodes if not e["truncated"]]

    # C2→C3 vs C2→C0
    c2_bull = [e for e in non_trunc if e["macro"] == 2 and e["exit_dest"] == 3]
    c2_bear = [e for e in non_trunc if e["macro"] == 2 and e["exit_dest"] == 0]
    print(f"  C2 → C3 (confirmed bull): n={len(c2_bull)}, "
          f"mean return={np.mean([e['log_return'] for e in c2_bull])*100:.4f}%" if c2_bull else "  C2 → C3: no episodes")
    print(f"  C2 → C0 (failed):         n={len(c2_bear)}, "
          f"mean return={np.mean([e['log_return'] for e in c2_bear])*100:.4f}%" if c2_bear else "  C2 → C0: no episodes")

    # C1→C3 vs C1→C0
    c1_bt = [e for e in non_trunc if e["macro"] == 1 and e["exit_dest"] == 3]
    c1_fail = [e for e in non_trunc if e["macro"] == 1 and e["exit_dest"] == 0]
    print(f"\n  C1 → C3 (breakthrough):   n={len(c1_bt)}, "
          f"mean return={np.mean([e['log_return'] for e in c1_bt])*100:.4f}%" if c1_bt else "  C1 → C3: no episodes")
    print(f"  C1 → C0 (failure):         n={len(c1_fail)}, "
          f"mean return={np.mean([e['log_return'] for e in c1_fail])*100:.4f}%" if c1_fail else "  C1 → C0: no episodes")

    if c1_bt and c1_fail:
        bt_mean = abs(np.mean([e["log_return"] for e in c1_bt]))
        fail_mean = abs(np.mean([e["log_return"] for e in c1_fail]))
        asym = bt_mean / fail_mean if fail_mean > 0 else float("inf")
        print(f"  Asymmetry ratio: {asym:.2f} (BTC IS: 4.36, BTC OOS: 3.95)")

    # BTC reference comparison
    print(f"\n  BTC reference: C1→C3 = +1.08–1.09%, C1→C0 = −0.25–0.27%")

    return episodes, macros, states_8, eth_c2_auc, eth_c1_auc, eth_c2_db, eth_c1_db, K, mean_jsd


# ═══════════════════════════════════════════════════════════════════════════
#  SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

def print_summary(btc_fwd_episodes, btc_fwd_macros, btc_fwd_states8,
                  eth_episodes, eth_macros, eth_states8,
                  eth_c2_auc, eth_c1_auc, eth_c2_db, eth_c1_db,
                  eth_K, eth_mean_jsd):
    section("SUMMARY COMPARISON TABLE")

    # Compute BTC Forward stats
    btc_counts, btc_jump = build_jump_chain(btc_fwd_episodes)
    btc_evals, btc_gaps, btc_K = eigenvalue_analysis(btc_fwd_states8)
    btc_jsds, btc_mean_jsd = complement_jsd(btc_jump)

    # Structural zeros for each
    def count_zeros(jump):
        z = 0
        for i in range(N_MACRO):
            for j in range(N_MACRO):
                if i != j and jump[i, j] < 0.01:
                    z += 1
        return z

    btc_zeros = count_zeros(btc_jump)

    eth_counts, eth_jump = build_jump_chain(eth_episodes)
    eth_zeros = count_zeros(eth_jump)
    eth_evals, eth_gaps, eth_K_recomp = eigenvalue_analysis(eth_states8)

    # BTC Forward C2 AUC (with production coefficients)
    c2_fwd = [e for e in btc_fwd_episodes if e["macro"] == 2 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]
    btc_fwd_c2_auc = None
    btc_fwd_c2_db = None
    if len(c2_fwd) >= 5:
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in c2_fwd])
        t1h = np.array([e["exit_t1h"] for e in c2_fwd])
        t8h = np.array([e["exit_t8h"] for e in c2_fwd])
        logit = PROD_C2["const"] + PROD_C2["t1h"] * t1h + PROD_C2["t8h"] * t8h
        prob = 1.0 / (1.0 + np.exp(-logit))
        if len(set(y)) > 1:
            btc_fwd_c2_auc = roc_auc_score(y, prob)
        btc_fwd_c2_db = -PROD_C2["const"] / PROD_C2["t8h"]

    c1_fwd = [e for e in btc_fwd_episodes if e["macro"] == 1 and not e["truncated"]
              and e["exit_dest"] in (0, 3)]
    btc_fwd_c1_auc = None
    btc_fwd_c1_db = None
    if len(c1_fwd) >= 5:
        y = np.array([1 if e["exit_dest"] == 3 else 0 for e in c1_fwd])
        t1h = np.array([e["exit_t1h"] for e in c1_fwd])
        t8h = np.array([e["exit_t8h"] for e in c1_fwd])
        logit = PROD_C1["const"] + PROD_C1["t1h"] * t1h + PROD_C1["t8h"] * t8h
        prob = 1.0 / (1.0 + np.exp(-logit))
        if len(set(y)) > 1:
            btc_fwd_c1_auc = roc_auc_score(y, prob)
        btc_fwd_c1_db = -PROD_C1["const"] / PROD_C1["t8h"]

    def fmt(v, fmt_str=".4f"):
        return f"{v:{fmt_str}}" if v is not None else "N/A"

    def fmt_e(v):
        return f"{v:.2e}" if v is not None else "N/A"

    print(f"\n  {'Metric':>25}  {'BTC OOS 23-24':>15}  {'BTC Fwd 26':>15}  {'ETH':>15}")
    print(f"  {'─' * 25}  {'─' * 15}  {'─' * 15}  {'─' * 15}")
    print(f"  {'K':>25}  {'4':>15}  {btc_K:>15}  {eth_K:>15}")
    print(f"  {'Structural zeros':>25}  {'4':>15}  {btc_zeros:>15}  {eth_zeros:>15}")
    print(f"  {'Complement JSD':>25}  {'0.007':>15}  {fmt(btc_mean_jsd):>15}  {fmt(eth_mean_jsd):>15}")

    btc_fwd_non_trunc = len([e for e in btc_fwd_episodes if not e["truncated"]])
    eth_non_trunc = len([e for e in eth_episodes if not e["truncated"]])
    print(f"  {'Episodes':>25}  {'2947':>15}  {btc_fwd_non_trunc:>15}  {eth_non_trunc:>15}")

    print(f"  {'C2 AUC':>25}  {'0.992':>15}  {fmt(btc_fwd_c2_auc):>15}  {fmt(eth_c2_auc):>15}")
    print(f"  {'C1 AUC':>25}  {'0.989':>15}  {fmt(btc_fwd_c1_auc):>15}  {fmt(eth_c1_auc):>15}")
    print(f"  {'C2 DB (t1h=0)':>25}  {'-1.49e-05':>15}  {fmt_e(btc_fwd_c2_db):>15}  {fmt_e(eth_c2_db):>15}")
    print(f"  {'C1 DB (t1h=0)':>25}  {'1.16e-05':>15}  {fmt_e(btc_fwd_c1_db):>15}  {fmt_e(eth_c1_db):>15}")

    print(f"\n  Note: BTC OOS 23-24 AUCs are in-sample (production fit). BTC Fwd uses production coefficients.")
    print(f"  ETH AUCs are from fresh logistic refit (in-sample). ETH decision boundaries from fresh fit.")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    btc, eth = computation_1()
    btc_fwd_episodes, btc_fwd_macros, btc_fwd_states8 = computation_2(btc)
    (eth_episodes, eth_macros, eth_states8, eth_c2_auc, eth_c1_auc,
     eth_c2_db, eth_c1_db, eth_K, eth_mean_jsd) = computation_3(eth)
    print_summary(btc_fwd_episodes, btc_fwd_macros, btc_fwd_states8,
                  eth_episodes, eth_macros, eth_states8,
                  eth_c2_auc, eth_c1_auc, eth_c2_db, eth_c1_db,
                  eth_K, eth_mean_jsd)
    section("Phase 14 Complete")


if __name__ == "__main__":
    main()
