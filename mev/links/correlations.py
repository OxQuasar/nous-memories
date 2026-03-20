#!/usr/bin/env python3
"""Correlation analysis: full-period, rolling, regime-split, lead/lag, calm-period ETH/BTC vs borrow."""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import datetime

DATA_DIR = Path(__file__).parent / "data"
DYNAMICS_DIR = Path(__file__).parent.parent / "dynamics" / "data"

# --- Crash epoch definitions ---
CRASH_EPOCHS = {
    "Terra/3AC":  ("2022-05-01", "2022-07-31"),
    "FTX":        ("2022-11-01", "2022-12-31"),
    "Yen carry":  ("2024-07-15", "2024-08-15"),
    "2025 crash": ("2025-01-01", "2025-04-30"),
    "2026 crash": ("2026-01-01", "2026-02-28"),
}

# Variables that use daily returns
RETURN_VARS = ["eth_price", "btc", "eth_btc", "sp500", "gold", "dxy"]
# Variables kept as levels
LEVEL_VARS = ["vix", "tnx", "fed_funds", "yield_spread"]


def load_data() -> pd.DataFrame:
    """Load and merge all data sources, compute returns and derived columns."""
    # TradFi daily
    tf = pd.read_csv(DATA_DIR / "tradfi_daily.csv", parse_dates=["date"])
    tf["date"] = tf["date"].dt.date
    tf = tf.set_index("date")

    # Liquidations: aggregate to daily count
    liq = pd.read_csv(DYNAMICS_DIR / "liquidations_full.csv", usecols=["timestamp"])
    liq["date"] = pd.to_datetime(liq["timestamp"], unit="s", utc=True).dt.date
    liq_daily = liq.groupby("date").size().rename("liq_count")

    # Protocol metrics
    pm = pd.read_csv(DYNAMICS_DIR / "protocol_metrics_daily.csv", parse_dates=["date"])
    pm["date"] = pm["date"].dt.date
    pm = pm.set_index("date")[["total_borrowed", "utilization_rate"]]

    # Merge
    df = tf.join(liq_daily, how="left").join(pm, how="left")
    df["liq_count"] = df["liq_count"].fillna(0).astype(int)

    # Compute daily returns for price-like vars
    for var in RETURN_VARS:
        df[f"{var}_ret"] = df[var].pct_change()

    # VIX change (not return — it's already a vol measure)
    df["vix_chg"] = df["vix"].diff()

    # Borrow growth: 30-day pct change
    df["borrow_chg_30d"] = df["total_borrowed"].pct_change(30)

    return df


def build_analysis_df(df: pd.DataFrame) -> pd.DataFrame:
    """Select the columns used in correlation analyses."""
    cols = (
        [f"{v}_ret" for v in RETURN_VARS]
        + LEVEL_VARS
        + ["liq_count", "total_borrowed", "utilization_rate", "borrow_chg_30d", "vix_chg"]
    )
    return df[cols].dropna(subset=["eth_price_ret"])


def is_crash(date, epochs=CRASH_EPOCHS) -> bool:
    for start, end in epochs.values():
        s = datetime.date.fromisoformat(start)
        e = datetime.date.fromisoformat(end)
        if s <= date <= e:
            return True
    return False


# ============================================================
# Analysis 1: Full-period correlation matrix
# ============================================================
def analysis_1(adf: pd.DataFrame):
    print("=" * 70)
    print("ANALYSIS 1: Full-Period Pearson Correlation Matrix")
    print("=" * 70)

    corr = adf.corr()
    corr.to_csv(DATA_DIR / "correlation_matrix.csv")
    print(f"Saved correlation_matrix.csv ({corr.shape[0]}×{corr.shape[1]})")

    # Top 10 strongest correlations with ETH return
    eth_corr = corr["eth_price_ret"].drop("eth_price_ret").abs().sort_values(ascending=False)
    print("\nTop 10 strongest correlations with ETH return:")
    for var, val in eth_corr.head(10).items():
        sign = corr.loc[var, "eth_price_ret"]
        print(f"  {var:25s}  r={sign:+.4f}  |r|={val:.4f}")

    # Top 10 for ETH/BTC return
    ethbtc_corr = corr["eth_btc_ret"].drop("eth_btc_ret").abs().sort_values(ascending=False)
    print("\nTop 10 strongest correlations with ETH/BTC return:")
    for var, val in ethbtc_corr.head(10).items():
        sign = corr.loc[var, "eth_btc_ret"]
        print(f"  {var:25s}  r={sign:+.4f}  |r|={val:.4f}")


# ============================================================
# Analysis 2: Rolling correlations
# ============================================================
def analysis_2(adf: pd.DataFrame):
    print("\n" + "=" * 70)
    print("ANALYSIS 2: 30-Day Rolling Correlations")
    print("=" * 70)

    WINDOW = 30

    eth_pairs = {
        "sp500_ret": "sp500_ret",
        "btc_ret": "btc_ret",
        "vix": "vix",
        "dxy_ret": "dxy_ret",
        "gold_ret": "gold_ret",
        "liq_count": "liq_count",
    }
    ethbtc_pairs = {
        "sp500_ret": "sp500_ret",
        "vix": "vix",
        "liq_count": "liq_count",
        "total_borrowed": "total_borrowed",
    }

    rolling = pd.DataFrame(index=adf.index)

    for label, col in eth_pairs.items():
        rolling[f"eth_vs_{label}"] = adf["eth_price_ret"].rolling(WINDOW).corr(adf[col])

    for label, col in ethbtc_pairs.items():
        rolling[f"ethbtc_vs_{label}"] = adf["eth_btc_ret"].rolling(WINDOW).corr(adf[col])

    rolling.index.name = "date"
    rolling.to_csv(DATA_DIR / "rolling_correlations.csv")
    print(f"Saved rolling_correlations.csv ({len(rolling)} rows, {len(rolling.columns)} cols)")

    # Summary stats
    print("\nRolling correlation summary (mean ± std):")
    for col in rolling.columns:
        s = rolling[col].dropna()
        print(f"  {col:30s}  mean={s.mean():+.3f}  std={s.std():.3f}  "
              f"min={s.min():+.3f}  max={s.max():+.3f}")


# ============================================================
# Analysis 3: Regime-split correlations
# ============================================================
def analysis_3(adf: pd.DataFrame):
    print("\n" + "=" * 70)
    print("ANALYSIS 3: Regime-Split Correlations (Crash vs Calm)")
    print("=" * 70)

    crash_mask = pd.Series([is_crash(d) for d in adf.index], index=adf.index)
    crash_df = adf[crash_mask]
    calm_df = adf[~crash_mask]
    print(f"Crash days: {crash_mask.sum()}, Calm days: {(~crash_mask).sum()}")

    crash_corr = crash_df.corr()
    calm_corr = calm_df.corr()

    # Key pairs for ETH return
    eth_pairs = ["sp500_ret", "btc_ret", "vix", "dxy_ret", "liq_count"]
    # Key pairs for ETH/BTC return
    ethbtc_pairs = ["sp500_ret", "vix", "liq_count", "total_borrowed", "borrow_chg_30d"]

    print(f"\n{'Variable':25s} {'Crash r':>10s} {'Calm r':>10s} {'Δ':>10s}")
    print("-" * 57)
    print("ETH return vs:")
    for var in eth_pairs:
        cr = crash_corr.loc["eth_price_ret", var]
        ca = calm_corr.loc["eth_price_ret", var]
        print(f"  {var:23s} {cr:+10.4f} {ca:+10.4f} {cr - ca:+10.4f}")

    print("\nETH/BTC return vs:")
    for var in ethbtc_pairs:
        cr = crash_corr.loc["eth_btc_ret", var]
        ca = calm_corr.loc["eth_btc_ret", var]
        print(f"  {var:23s} {cr:+10.4f} {ca:+10.4f} {cr - ca:+10.4f}")


# ============================================================
# Analysis 4: Lead/lag cross-correlation
# ============================================================
def analysis_4(adf: pd.DataFrame):
    print("\n" + "=" * 70)
    print("ANALYSIS 4: Lead/Lag Cross-Correlation (ETH return vs others)")
    print("=" * 70)

    MAX_LAG = 5
    target = adf["eth_price_ret"].dropna()
    predictors = {
        "sp500_ret": adf["sp500_ret"],
        "btc_ret": adf["btc_ret"],
        "vix_chg": adf["vix_chg"],
        "dxy_ret": adf["dxy_ret"],
        "liq_count": adf["liq_count"],
    }

    print(f"\nLag convention: negative = other variable leads ETH")
    print(f"{'Variable':15s} ", end="")
    for lag in range(-MAX_LAG, MAX_LAG + 1):
        print(f"{'lag=' + str(lag):>8s}", end="")
    print(f"  {'Peak lag':>10s} {'Peak r':>8s}")
    print("-" * (15 + 8 * 11 + 20))

    for name, series in predictors.items():
        # Align
        common = target.index.intersection(series.dropna().index)
        t = target.loc[common]
        s = series.loc[common]

        corrs = {}
        print(f"{name:15s} ", end="")
        for lag in range(-MAX_LAG, MAX_LAG + 1):
            # Positive lag: shift target forward (= other leads)
            # np convention: positive shift means s is shifted right
            if lag < 0:
                # Other variable leads: compare s[t] with target[t + |lag|]
                c = t.iloc[-lag:].reset_index(drop=True).corr(s.iloc[:lag].reset_index(drop=True))
            elif lag > 0:
                c = t.iloc[:-lag].reset_index(drop=True).corr(s.iloc[lag:].reset_index(drop=True))
            else:
                c = t.corr(s)
            corrs[lag] = c
            print(f"{c:+8.4f}", end="")

        peak_lag = max(corrs, key=lambda k: abs(corrs[k]))
        print(f"  {peak_lag:>10d} {corrs[peak_lag]:+8.4f}")


# ============================================================
# Analysis 5: Calm-period ETH/BTC vs borrow growth
# ============================================================
def analysis_5(adf: pd.DataFrame):
    print("\n" + "=" * 70)
    print("ANALYSIS 5: Calm-Period ETH/BTC Return vs Borrow Growth (30d)")
    print("=" * 70)

    crash_mask = pd.Series([is_crash(d) for d in adf.index], index=adf.index)
    calm = adf[~crash_mask][["eth_btc_ret", "borrow_chg_30d"]].dropna()

    r_all, p_all = stats.spearmanr(calm["eth_btc_ret"], calm["borrow_chg_30d"])
    print(f"\nAll calm periods: Spearman r={r_all:+.4f}, p={p_all:.4e}, n={len(calm)}")

    # Pre-2024 vs post-2024 split (BTC ETF launch ~Jan 10, 2024)
    split = datetime.date(2024, 1, 1)
    pre = calm[calm.index < split]
    post = calm[calm.index >= split]

    if len(pre) > 10:
        r_pre, p_pre = stats.spearmanr(pre["eth_btc_ret"], pre["borrow_chg_30d"])
        print(f"Pre-2024 calm:   Spearman r={r_pre:+.4f}, p={p_pre:.4e}, n={len(pre)}")
    else:
        print(f"Pre-2024 calm:   insufficient data (n={len(pre)})")

    if len(post) > 10:
        r_post, p_post = stats.spearmanr(post["eth_btc_ret"], post["borrow_chg_30d"])
        print(f"Post-2024 calm:  Spearman r={r_post:+.4f}, p={p_post:.4e}, n={len(post)}")
    else:
        print(f"Post-2024 calm:  insufficient data (n={len(post)})")

    # Also test: does borrow growth predict ETH/BTC at a lag?
    print("\n  Lagged Spearman (borrow_chg_30d leads ETH/BTC return by N days):")
    calm_full = adf[~crash_mask][["eth_btc_ret", "borrow_chg_30d"]]
    for lag in [1, 5, 10, 20, 30]:
        shifted = calm_full["borrow_chg_30d"].shift(lag)
        pair = pd.concat([calm_full["eth_btc_ret"], shifted], axis=1).dropna()
        if len(pair) > 20:
            r, p = stats.spearmanr(pair.iloc[:, 0], pair.iloc[:, 1])
            print(f"    lag={lag:2d}d: r={r:+.4f}, p={p:.4e}, n={len(pair)}")


def main():
    print("Loading data...")
    df = load_data()
    adf = build_analysis_df(df)
    print(f"Analysis dataframe: {len(adf)} rows, {len(adf.columns)} cols")
    print(f"Date range: {adf.index[0]} → {adf.index[-1]}")

    analysis_1(adf)
    analysis_2(adf)
    analysis_3(adf)
    analysis_4(adf)
    analysis_5(adf)

    print("\n" + "=" * 70)
    print("All analyses complete.")


if __name__ == "__main__":
    main()
