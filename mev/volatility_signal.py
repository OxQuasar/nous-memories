"""
Test whether liquidation volume predicts forward volatility magnitude
(regardless of direction) and whether concentration ratio classifies
cascade vs absorption.

Uses existing CSVs — no new data pulls.
"""

import os

import numpy as np
import pandas as pd
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

LIQ_FILE = os.path.join(DATA_DIR, "liquidation_events.csv")
ETH_FILE = os.path.join(DATA_DIR, "eth_price.csv")
VOL_SIGNAL_FILE = os.path.join(DATA_DIR, "volatility_signal.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "volatility_signal_results.txt")

HORIZONS = [1, 3, 7]
TRAILING_WINDOW = 7
CONCENTRATION_THRESHOLD = 0.5


def load_data() -> pd.DataFrame:
    """Load and merge liquidation + ETH price data."""
    eth = pd.read_csv(ETH_FILE)
    eth["date"] = eth["date"].astype(str)

    liq = pd.read_csv(LIQ_FILE)
    liq["date"] = liq["date"].astype(str)

    # Use ETH price as base, left join liquidation data
    df = eth[["date", "price"]].merge(liq[["date", "total_usd", "event_count"]], on="date", how="left")
    df["total_usd"] = df["total_usd"].fillna(0)
    df["event_count"] = df["event_count"].fillna(0)
    df = df.sort_values("date").reset_index(drop=True)
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add forward returns, absolute returns, trailing vol, concentration ratio."""
    for h in HORIZONS:
        df[f"fwd_{h}d"] = df["price"].shift(-h) / df["price"] - 1
        df[f"abs_fwd_{h}d"] = df[f"fwd_{h}d"].abs()

    # Trailing 7d realized vol (std of daily returns)
    daily_ret = df["price"].pct_change()
    df["trailing_7d_vol"] = daily_ret.rolling(TRAILING_WINDOW).std()

    # Forward 7d realized vol
    df["fwd_7d_realized_vol"] = daily_ret.shift(-1).rolling(TRAILING_WINDOW).std().shift(-TRAILING_WINDOW + 1)

    # Trailing 7d liquidation volume (including today)
    df["trailing_7d_liq"] = df["total_usd"].rolling(TRAILING_WINDOW, min_periods=1).sum()

    # Concentration ratio: today / trailing 7d sum
    df["concentration_ratio"] = df["total_usd"] / df["trailing_7d_liq"].replace(0, np.nan)

    return df


def bucket_days(df: pd.DataFrame) -> pd.DataFrame:
    """Assign liquidation volume buckets."""
    active = df[df["total_usd"] > 0]["total_usd"]
    if len(active) == 0:
        df["bucket"] = "quiet"
        return df

    p75 = np.percentile(active, 75)
    p90 = np.percentile(active, 90)
    p95 = np.percentile(active, 95)

    conditions = [
        df["total_usd"] >= p95,
        df["total_usd"] >= p90,
        df["total_usd"] >= p75,
    ]
    choices = ["extreme", "elevated", "moderate"]
    df["bucket"] = np.select(conditions, choices, default="quiet")

    return df, p75, p90, p95


def section_a(df: pd.DataFrame) -> list[str]:
    """Forward realized volatility by liquidation regime."""
    lines = []
    lines.append("=== A. FORWARD VOLATILITY BY LIQUIDATION REGIME ===")
    lines.append("")

    buckets = ["quiet", "moderate", "elevated", "extreme"]
    bucket_counts = {b: (df["bucket"] == b).sum() for b in buckets}

    for h in HORIZONS:
        col = f"abs_fwd_{h}d"
        lines.append(f"  --- {h}-day absolute forward return ---")
        lines.append(f"  {'Bucket':>10s}  {'N':>6s}  {'Mean':>8s}  {'Median':>8s}  {'Std':>8s}  {'Kurt':>8s}  {'Max':>8s}")

        for b in buckets:
            vals = df.loc[df["bucket"] == b, col].dropna()
            if len(vals) < 5:
                continue
            lines.append(
                f"  {b:>10s}  {len(vals):>6d}  {vals.mean():8.2%}  {vals.median():8.2%}"
                f"  {vals.std():8.2%}  {vals.kurtosis():8.2f}  {vals.max():8.2%}"
            )
        lines.append("")

    return lines


def section_b(df: pd.DataFrame) -> list[str]:
    """Statistical significance test: extreme vs quiet absolute 7d returns."""
    lines = []
    lines.append("=== B. STATISTICAL SIGNIFICANCE (extreme vs quiet, abs 7d return) ===")

    quiet = df.loc[df["bucket"] == "quiet", "abs_fwd_7d"].dropna()
    extreme = df.loc[df["bucket"] == "extreme", "abs_fwd_7d"].dropna()

    if len(quiet) < 10 or len(extreme) < 5:
        lines.append("  Insufficient data for significance test.")
        return lines

    u_stat, p_value = stats.mannwhitneyu(extreme, quiet, alternative="greater")
    effect_size = extreme.median() / quiet.median() if quiet.median() > 0 else float("inf")

    lines.append(f"  Quiet days:  n={len(quiet)}, median abs 7d return = {quiet.median():.2%}")
    lines.append(f"  Extreme days: n={len(extreme)}, median abs 7d return = {extreme.median():.2%}")
    lines.append(f"  Mann-Whitney U = {u_stat:.0f}, p-value = {p_value:.4f}")
    lines.append(f"  Effect size (median ratio extreme/quiet) = {effect_size:.2f}x")
    lines.append(f"  Significant at 5%: {'YES' if p_value < 0.05 else 'NO'}")
    lines.append("")

    return lines


def section_c(df: pd.DataFrame) -> list[str]:
    """Save volatility signal time series."""
    lines = []
    lines.append("=== C. VOLATILITY SIGNAL TIME SERIES ===")

    out = df[["date", "total_usd", "abs_fwd_7d", "fwd_7d_realized_vol"]].copy()
    out.columns = ["date", "liq_volume", "fwd_7d_abs_return", "fwd_7d_realized_vol"]
    out.to_csv(VOL_SIGNAL_FILE, index=False)
    lines.append(f"  Saved {len(out)} rows → {VOL_SIGNAL_FILE}")

    # Correlation between liq volume and forward vol
    valid = out.dropna()
    r_abs = valid["liq_volume"].corr(valid["fwd_7d_abs_return"])
    r_vol = valid["liq_volume"].corr(valid["fwd_7d_realized_vol"])
    lines.append(f"  Correlation(liq_volume, fwd_7d_abs_return) = {r_abs:+.3f}")
    lines.append(f"  Correlation(liq_volume, fwd_7d_realized_vol) = {r_vol:+.3f}")

    # Log-volume correlation (liquidation volume is heavily right-skewed)
    valid_active = valid[valid["liq_volume"] > 0].copy()
    valid_active["log_liq"] = np.log1p(valid_active["liq_volume"])
    r_log_abs = valid_active["log_liq"].corr(valid_active["fwd_7d_abs_return"])
    r_log_vol = valid_active["log_liq"].corr(valid_active["fwd_7d_realized_vol"])
    lines.append(f"  Correlation(log_liq_volume, fwd_7d_abs_return) = {r_log_abs:+.3f} (active days only, n={len(valid_active)})")
    lines.append(f"  Correlation(log_liq_volume, fwd_7d_realized_vol) = {r_log_vol:+.3f}")
    lines.append("")

    return lines


def section_d(df: pd.DataFrame, p90: float) -> list[str]:
    """Volume concentration ratio as cascade vs absorption classifier."""
    lines = []
    lines.append("=== D. CONCENTRATION RATIO: CASCADE vs ABSORPTION CLASSIFIER ===")
    lines.append(f"  (Days with liq volume ≥ 90th pctl = ${p90/1e6:.1f}M)")
    lines.append(f"  Concentrated: today > {CONCENTRATION_THRESHOLD:.0%} of trailing 7d total (capitulation)")
    lines.append(f"  Distributed: today ≤ {CONCENTRATION_THRESHOLD:.0%} of trailing 7d total (ongoing cascade)")
    lines.append("")

    high_liq = df[(df["total_usd"] >= p90) & df["concentration_ratio"].notna()].copy()
    if len(high_liq) < 10:
        lines.append("  Insufficient high-liquidation days for analysis.")
        return lines

    concentrated = high_liq[high_liq["concentration_ratio"] > CONCENTRATION_THRESHOLD]
    distributed = high_liq[high_liq["concentration_ratio"] <= CONCENTRATION_THRESHOLD]

    lines.append(f"  Concentrated: {len(concentrated)} days, Distributed: {len(distributed)} days")
    lines.append("")

    for label, subset in [("Concentrated", concentrated), ("Distributed", distributed)]:
        if len(subset) < 3:
            lines.append(f"  {label}: too few days")
            continue
        lines.append(f"  {label} (n={len(subset)}):")
        lines.append(f"  {'Horizon':>10s}  {'Mean':>8s}  {'Median':>8s}  {'% Neg':>8s}")
        for h in HORIZONS:
            vals = subset[f"fwd_{h}d"].dropna()
            if len(vals) == 0:
                continue
            lines.append(
                f"  {h:>8d}d  {vals.mean():+8.3%}  {vals.median():+8.3%}"
                f"  {100*(vals < 0).mean():7.1f}%"
            )
        lines.append("")

    # Significance test on 7d returns between groups
    c7 = concentrated["fwd_7d"].dropna()
    d7 = distributed["fwd_7d"].dropna()
    if len(c7) >= 5 and len(d7) >= 5:
        u_stat, p_val = stats.mannwhitneyu(c7, d7, alternative="two-sided")
        lines.append(f"  7d return difference: Mann-Whitney p = {p_val:.4f}")
        lines.append(f"  Concentrated 7d median: {c7.median():+.3%}, Distributed 7d median: {d7.median():+.3%}")
    lines.append("")

    return lines


def verdict(df: pd.DataFrame, p90: float) -> list[str]:
    """Overall verdict."""
    lines = []
    lines.append("=== VERDICT ===")

    # Volatility prediction
    quiet_abs = df.loc[df["bucket"] == "quiet", "abs_fwd_7d"].dropna()
    extreme_abs = df.loc[df["bucket"] == "extreme", "abs_fwd_7d"].dropna()
    if len(quiet_abs) > 0 and len(extreme_abs) > 0:
        ratio = extreme_abs.median() / quiet_abs.median() if quiet_abs.median() > 0 else 0
        _, p_val = stats.mannwhitneyu(extreme_abs, quiet_abs, alternative="greater")

        if p_val < 0.05 and ratio > 1.3:
            lines.append(f"  Volatility prediction: YES — extreme liquidation days predict {ratio:.1f}x higher forward volatility (p={p_val:.4f})")
        elif p_val < 0.10:
            lines.append(f"  Volatility prediction: WEAK — {ratio:.1f}x ratio but marginal significance (p={p_val:.4f})")
        else:
            lines.append(f"  Volatility prediction: NO — ratio {ratio:.1f}x, not significant (p={p_val:.4f})")

    # Concentration ratio
    high_liq = df[(df["total_usd"] >= p90) & df["concentration_ratio"].notna()]
    conc = high_liq[high_liq["concentration_ratio"] > CONCENTRATION_THRESHOLD]["fwd_7d"].dropna()
    dist = high_liq[high_liq["concentration_ratio"] <= CONCENTRATION_THRESHOLD]["fwd_7d"].dropna()
    if len(conc) >= 5 and len(dist) >= 5:
        _, p_val = stats.mannwhitneyu(conc, dist, alternative="two-sided")
        lines.append(
            f"  Concentration classifier: "
            f"concentrated median {conc.median():+.3%} vs distributed median {dist.median():+.3%} "
            f"(p={p_val:.4f})"
        )
        if p_val < 0.05:
            if conc.median() > dist.median():
                lines.append("  → Concentrated spikes (capitulation) → better forward returns (absorption)")
            else:
                lines.append("  → Distributed liquidations → better forward returns (cascade from concentrated)")
        else:
            lines.append("  → No statistically significant difference between concentrated and distributed")

    return lines


def main():
    print("Loading data...")
    df = load_data()
    df = add_features(df)
    df, p75, p90, p95 = bucket_days(df)

    print(f"Days: {len(df)}, Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
    print(f"Thresholds — 75th: ${p75/1e6:.2f}M, 90th: ${p90/1e6:.2f}M, 95th: ${p95/1e6:.2f}M")
    print()

    all_lines = []
    all_lines.append(f"Data: {df['date'].iloc[0]} to {df['date'].iloc[-1]} ({len(df)} days)")
    all_lines.append(f"Liquidation volume thresholds (of active days):")
    all_lines.append(f"  75th: ${p75/1e6:.2f}M, 90th: ${p90/1e6:.2f}M, 95th: ${p95/1e6:.2f}M")
    all_lines.append("")

    all_lines.extend(section_a(df))
    all_lines.extend(section_b(df))
    all_lines.extend(section_c(df))
    all_lines.extend(section_d(df, p90))
    all_lines.extend(verdict(df, p90))

    summary = "\n".join(all_lines)
    print(summary)

    with open(RESULTS_FILE, "w") as f:
        f.write(summary + "\n")
    print(f"\nResults saved → {RESULTS_FILE}")


if __name__ == "__main__":
    main()
