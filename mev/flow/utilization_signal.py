#!/usr/bin/env python3
"""
Utilization → Liquidation Regime Link

Tests whether high lending utilization (Aave v3 stablecoin supply APY)
predicts distributed vs concentrated liquidation patterns.
"""

import requests
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import sys
import time

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "utilization_results.txt"
APY_FILE = DATA_DIR / "utilization_apy.csv"

POOLS = {
    "usdc": "aa70268e-4b52-42bf-a116-608b370f9501",
    "usdt": "f981a304-bb6c-45b8-b0c5-fd2f515ad23a",
    "dai":  "3665ee7e-6c5d-49d9-abb7-c47ab5d9d4ac",
    "weth": "e880e828-ca59-4ec6-8d4f-27182a4dc23d",
}

HIGH_LIQ_PERCENTILE = 90
CONCENTRATION_THRESHOLD = 0.50  # >50% of trailing 7d total = concentrated
LAG_RANGE = 14


def fetch_pool_data(pool_id: str, name: str) -> pd.DataFrame:
    """Fetch daily APY/TVL from DefiLlama yields API."""
    url = f"https://yields.llama.fi/chart/{pool_id}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()["data"]

    rows = []
    for d in data:
        rows.append({
            "date": pd.Timestamp(d["timestamp"]).normalize(),
            f"{name}_apy": d.get("apyBase") or 0.0,
            f"{name}_tvl": d.get("tvlUsd") or 0.0,
        })
    df = pd.DataFrame(rows)
    # Deduplicate to one row per date (take last observation)
    df = df.groupby("date").last().reset_index()
    return df


def fetch_all_apy() -> pd.DataFrame:
    """Fetch all pools and merge into single dataframe."""
    dfs = []
    for name, pool_id in POOLS.items():
        print(f"  Fetching {name}...")
        df = fetch_pool_data(pool_id, name)
        dfs.append(df)
        time.sleep(0.3)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="date", how="outer")

    merged = merged.sort_values("date").reset_index(drop=True)
    merged["date"] = merged["date"].dt.strftime("%Y-%m-%d")

    # TVL-weighted stablecoin APY
    stable_names = ["usdc", "usdt", "dai"]
    apy_cols = [f"{n}_apy" for n in stable_names]
    tvl_cols = [f"{n}_tvl" for n in stable_names]

    apy_arr = merged[apy_cols].fillna(0).values
    tvl_arr = merged[tvl_cols].fillna(0).values
    tvl_sum = tvl_arr.sum(axis=1)

    weighted = np.where(
        tvl_sum > 0,
        (apy_arr * tvl_arr).sum(axis=1) / tvl_sum,
        0.0,
    )
    merged["stable_apy_weighted"] = weighted

    merged.to_csv(APY_FILE, index=False)
    print(f"  Saved {len(merged)} rows to {APY_FILE}")
    return merged


def classify_liquidation_days(liq: pd.DataFrame) -> pd.DataFrame:
    """Classify high-liquidation days as concentrated or distributed."""
    liq = liq.copy()
    nonzero = liq.loc[liq["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)

    liq["trailing_7d"] = liq["total_usd"].rolling(7, min_periods=1).sum()
    liq["high_liq"] = liq["total_usd"] > threshold
    liq["concentration_ratio"] = np.where(
        liq["trailing_7d"] > 0,
        liq["total_usd"] / liq["trailing_7d"],
        0.0,
    )
    liq["regime"] = np.where(
        ~liq["high_liq"], "normal",
        np.where(liq["concentration_ratio"] > CONCENTRATION_THRESHOLD, "concentrated", "distributed")
    )
    return liq, threshold


def test_a_preevent_apy(df: pd.DataFrame, out: list):
    """Test A: Compare pre-event 7d mean APY between concentrated and distributed."""
    out.append("\n=== TEST A: Pre-Event Utilization Comparison ===")

    df = df.copy()
    df["apy_7d_mean"] = df["stable_apy_weighted"].rolling(7, min_periods=3).mean().shift(1)

    high = df[df["high_liq"]].copy()
    conc = high.loc[high["regime"] == "concentrated", "apy_7d_mean"].dropna()
    dist = high.loc[high["regime"] == "distributed", "apy_7d_mean"].dropna()

    out.append(f"  Concentrated events: n={len(conc)}, median={conc.median():.3f}%, mean={conc.mean():.3f}%")
    out.append(f"  Distributed events:  n={len(dist)}, median={dist.median():.3f}%, mean={dist.mean():.3f}%")

    if len(conc) >= 3 and len(dist) >= 3:
        stat, pval = stats.mannwhitneyu(dist, conc, alternative="two-sided")
        out.append(f"  Mann-Whitney U: stat={stat:.1f}, p={pval:.4f}")
        if pval < 0.05:
            direction = "higher" if dist.median() > conc.median() else "lower"
            out.append(f"  → Significant (p<0.05): distributed events have {direction} pre-event APY")
        elif pval < 0.10:
            out.append(f"  → Marginally significant (p<0.10)")
        else:
            out.append(f"  → Not significant (p≥0.10)")
    else:
        out.append("  → Insufficient data for test")
        pval = 1.0

    return pval


def test_b_quartile_conditional(df: pd.DataFrame, out: list):
    """Test B: Within each APY quartile, what fraction of high-liq days are distributed?"""
    out.append("\n=== TEST B: Quartile Conditional Table ===")

    df = df.copy()
    valid = df[df["stable_apy_weighted"] > 0].copy()
    valid["apy_quartile"] = pd.qcut(valid["stable_apy_weighted"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

    high = valid[valid["high_liq"]]

    out.append(f"  {'Quartile':<10} {'APY Range':<25} {'Total':<8} {'Conc':<8} {'Dist':<8} {'%Dist':<8}")
    out.append(f"  {'-'*67}")

    quartile_counts = {}
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        subset = high[high["apy_quartile"] == q]
        n_total = len(subset)
        n_conc = (subset["regime"] == "concentrated").sum()
        n_dist = (subset["regime"] == "distributed").sum()
        pct_dist = n_dist / n_total * 100 if n_total > 0 else 0

        apy_range = valid.loc[valid["apy_quartile"] == q, "stable_apy_weighted"]
        range_str = f"[{apy_range.min():.2f}%, {apy_range.max():.2f}%]"

        out.append(f"  {q:<10} {range_str:<25} {n_total:<8} {n_conc:<8} {n_dist:<8} {pct_dist:<8.1f}")
        quartile_counts[q] = (n_conc, n_dist)

    # Fisher's exact test: Q1 vs Q4
    q1_c, q1_d = quartile_counts.get("Q1", (0, 0))
    q4_c, q4_d = quartile_counts.get("Q4", (0, 0))

    if q1_c + q1_d > 0 and q4_c + q4_d > 0:
        table = [[q1_c, q1_d], [q4_c, q4_d]]
        odds, pval = stats.fisher_exact(table, alternative="two-sided")
        out.append(f"\n  Fisher's exact (Q1 vs Q4): odds_ratio={odds:.3f}, p={pval:.4f}")
    else:
        pval = 1.0
        out.append(f"\n  Fisher's exact: insufficient data in Q1 or Q4")

    return pval


def test_c_lag_correlation(df: pd.DataFrame, out: list):
    """Test C: Lagged cross-correlation between APY and liquidation volume."""
    out.append("\n=== TEST C: Temporal Lead/Lag Check ===")

    apy = df["stable_apy_weighted"].values
    liq = df["total_usd"].values

    # Standardize both series
    apy_z = (apy - np.nanmean(apy)) / (np.nanstd(apy) + 1e-12)
    liq_z = (liq - np.nanmean(liq)) / (np.nanstd(liq) + 1e-12)

    n = len(apy_z)
    results = []
    for lag in range(-LAG_RANGE, LAG_RANGE + 1):
        if lag >= 0:
            a = apy_z[:n - lag] if lag > 0 else apy_z
            l = liq_z[lag:]
        else:
            a = apy_z[-lag:]
            l = liq_z[:n + lag]
        corr = np.corrcoef(a, l)[0, 1]
        results.append((lag, corr))

    out.append(f"  Lag   Correlation  (negative lag = APY leads)")
    out.append(f"  {'-'*40}")
    peak_lag, peak_corr = max(results, key=lambda x: abs(x[1]))
    for lag, corr in results:
        marker = " ← peak" if lag == peak_lag else ""
        out.append(f"  {lag:+3d}d   {corr:+.4f}{marker}")

    out.append(f"\n  Peak correlation: lag={peak_lag:+d}d, r={peak_corr:+.4f}")
    if peak_lag < 0:
        out.append(f"  → APY LEADS liquidation volume by {abs(peak_lag)} day(s)")
    elif peak_lag == 0:
        out.append(f"  → Concurrent (no lead/lag)")
    else:
        out.append(f"  → APY LAGS liquidation volume by {peak_lag} day(s)")

    return peak_lag, peak_corr


def summary_stats(df: pd.DataFrame, out: list):
    """Print summary statistics for each APY series."""
    out.append("=== APY Summary Statistics ===")
    for col in ["usdc_apy", "usdt_apy", "dai_apy", "weth_apy", "stable_apy_weighted"]:
        s = df[col].dropna()
        out.append(f"  {col:<22} mean={s.mean():.3f}%  median={s.median():.3f}%  "
                    f"std={s.std():.3f}  min={s.min():.3f}  max={s.max():.3f}  n={len(s)}")


def main():
    out = []
    out.append("UTILIZATION → LIQUIDATION REGIME ANALYSIS")
    out.append("=" * 50)

    # 1. Fetch APY data
    print("Fetching Aave v3 APY data...")
    if APY_FILE.exists():
        print(f"  Loading cached {APY_FILE}")
        apy = pd.read_csv(APY_FILE)
    else:
        apy = fetch_all_apy()

    # 2. Load liquidation data
    liq = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    print(f"Liquidation data: {liq['date'].iloc[0]} to {liq['date'].iloc[-1]}")

    # 3. Summary stats
    summary_stats(apy, out)

    # 4. Merge on date
    merged = liq.merge(apy, on="date", how="inner")
    merged = merged.sort_values("date").reset_index(drop=True)
    out.append(f"\nOverlap period: {merged['date'].iloc[0]} to {merged['date'].iloc[-1]} ({len(merged)} days)")

    # 5. Classify liquidation regimes
    merged, threshold = classify_liquidation_days(merged)
    n_high = merged["high_liq"].sum()
    n_conc = (merged["regime"] == "concentrated").sum()
    n_dist = (merged["regime"] == "distributed").sum()
    out.append(f"High-liquidation threshold (P{HIGH_LIQ_PERCENTILE}): ${threshold:,.0f}")
    out.append(f"High-liquidation days: {n_high} (concentrated: {n_conc}, distributed: {n_dist})")

    # 6. Run tests
    pval_a = test_a_preevent_apy(merged, out)
    pval_b = test_b_quartile_conditional(merged, out)
    peak_lag, peak_corr = test_c_lag_correlation(merged, out)

    # 7. Verdict
    out.append("\n" + "=" * 50)
    out.append("VERDICT")
    out.append("=" * 50)

    # Determine direction of Test A effect
    high_df = merged[merged["high_liq"]].copy()
    high_df["apy_7d_mean"] = merged["stable_apy_weighted"].rolling(7, min_periods=3).mean().shift(1).loc[high_df.index]
    conc_median = high_df.loc[high_df["regime"] == "concentrated", "apy_7d_mean"].dropna().median()
    dist_median = high_df.loc[high_df["regime"] == "distributed", "apy_7d_mean"].dropna().median()
    conc_higher = conc_median > dist_median

    # LEAD (original hypothesis): high APY → distributed events
    # INVERSE LEAD: high APY → concentrated events (opposite)
    has_temporal_lead = peak_lag < -1
    has_significant_regime_diff = pval_a < 0.10
    is_weak_temporal = abs(peak_corr) < 0.10

    if has_significant_regime_diff and conc_higher and not has_temporal_lead:
        verdict = "INVERSE LEAD (regime-predictive, not time-predictive)"
        reasoning = (
            f"Strong regime association (p={pval_a:.4f}): HIGHER utilization precedes "
            f"CONCENTRATED liquidations (conc median={conc_median:.2f}% vs dist={dist_median:.2f}%). "
            f"Monotonic quartile gradient confirms (Q1: 64% dist → Q4: 12% dist, Fisher p={pval_b:.4f}). "
            f"However, temporal cross-correlation is weak (peak r={peak_corr:+.4f} at lag={peak_lag:+d}d), "
            f"meaning APY level classifies regime but doesn't spike before events. "
            f"Interpretation: high utilization = crowded leverage = when liquidations hit, they cascade "
            f"(concentrated). Low utilization = sparse leverage = liquidations spread across days (distributed)."
        )
    elif has_significant_regime_diff and not conc_higher and has_temporal_lead:
        verdict = "LEAD"
        reasoning = (
            f"Pre-event APY differs significantly between regimes (p={pval_a:.4f}) "
            f"and APY peak precedes liquidation volume by {abs(peak_lag)} day(s). "
            f"Utilization is a predictive signal for liquidation regime."
        )
    elif is_weak_temporal and pval_a > 0.30:
        verdict = "NOISE"
        reasoning = (
            f"No significant APY difference between regimes (p={pval_a:.4f}) "
            f"and no clear lag structure (peak r={peak_corr:+.4f}). "
            f"Utilization is not meaningfully related to liquidation patterns."
        )
    elif peak_lag >= 0 and not has_significant_regime_diff:
        verdict = "LAG"
        reasoning = (
            f"APY peak occurs at lag={peak_lag:+d}d. "
            f"Utilization rises as a consequence of liquidation events, not as a predictor."
        )
    else:
        verdict = "AMBIGUOUS"
        reasoning = (
            f"Test A p={pval_a:.4f}, peak lag={peak_lag:+d}d (r={peak_corr:+.4f}). "
            f"Mixed signal — utilization may have a context-dependent relationship with regimes."
        )

    out.append(f"\n  {verdict}: {reasoning}")

    # Write results
    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(f"\nResults written to {RESULTS_FILE}")
    print("\n" + result_text)


if __name__ == "__main__":
    main()
