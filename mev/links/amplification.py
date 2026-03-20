#!/usr/bin/env python3
"""Crash amplification analysis: does DeFi liquidation selling make ETH crashes worse?"""

import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import statsmodels.api as sm

DATA_DIR = Path(__file__).parent / "data"
DYNAMICS_DIR = Path(__file__).parent.parent / "dynamics" / "data"

CRASH_EPOCHS = {
    "Terra/3AC":  ("2022-05-01", "2022-07-31"),
    "FTX":        ("2022-11-01", "2022-12-31"),
    "Yen carry":  ("2024-07-15", "2024-08-15"),
    "2025 crash": ("2025-01-01", "2025-04-30"),
    "2026 crash": ("2026-01-01", "2026-02-28"),
}

LIQ_BUCKETS = [(0, 0), (1, 10), (11, 50), (51, 200), (201, 500), (501, None)]
LIQ_BUCKET_LABELS = ["0", "1-10", "11-50", "51-200", "201-500", "500+"]


def load_data() -> pd.DataFrame:
    """Load tradfi, liquidations, protocol metrics. Compute returns."""
    tf = pd.read_csv(DATA_DIR / "tradfi_daily.csv", parse_dates=["date"])
    tf["date"] = tf["date"].dt.date
    tf = tf.set_index("date")

    # Daily liquidation count
    liq = pd.read_csv(DYNAMICS_DIR / "liquidations_full.csv", usecols=["timestamp"])
    liq["date"] = pd.to_datetime(liq["timestamp"], unit="s", utc=True).dt.date
    liq_daily = liq.groupby("date").size().rename("liq_count")

    # Protocol metrics
    pm = pd.read_csv(DYNAMICS_DIR / "protocol_metrics_daily.csv", parse_dates=["date"])
    pm["date"] = pm["date"].dt.date
    pm = pm.set_index("date")[["total_borrowed", "utilization_rate"]]

    df = tf.join(liq_daily, how="left").join(pm, how="left")
    df["liq_count"] = df["liq_count"].fillna(0).astype(int)

    # Daily returns
    df["eth_ret"] = df["eth_price"].pct_change()
    df["btc_ret"] = df["btc"].pct_change()
    df["sp_ret"] = df["sp500"].pct_change()

    return df.dropna(subset=["eth_ret", "btc_ret", "sp_ret"])


def crash_label(date) -> str | None:
    """Return crash epoch name if date falls in one, else None."""
    for name, (start, end) in CRASH_EPOCHS.items():
        if datetime.date.fromisoformat(start) <= date <= datetime.date.fromisoformat(end):
            return name
    return None


def is_crash(date) -> bool:
    return crash_label(date) is not None


# ============================================================
# Part 1: Baseline OLS model on non-crash days
# ============================================================
def part1(df: pd.DataFrame):
    print("=" * 70)
    print("PART 1: Baseline OLS Model (trained on non-crash days)")
    print("=" * 70)

    calm = df[[not is_crash(d) for d in df.index]].copy()
    X = sm.add_constant(calm[["btc_ret", "sp_ret"]])
    y = calm["eth_ret"]
    model = sm.OLS(y, X).fit()

    print(model.summary().tables[1])
    print(f"\nR² = {model.rsquared:.4f}, Adj R² = {model.rsquared_adj:.4f}")
    print(f"Residual mean = {model.resid.mean():.6f}, std = {model.resid.std():.6f}")
    print(f"Training days: {len(calm)}")

    return model


# ============================================================
# Part 2: Crash-day residuals
# ============================================================
def part2(df: pd.DataFrame, model):
    print("\n" + "=" * 70)
    print("PART 2: Crash-Day Residuals")
    print("=" * 70)

    # Predict on ALL days
    X_all = sm.add_constant(df[["btc_ret", "sp_ret"]])
    df["predicted"] = model.predict(X_all)
    df["residual"] = df["eth_ret"] - df["predicted"]

    # Per-crash summary
    print(f"\n{'Crash':15s} {'Days':>5s} {'Mean resid':>12s} {'Cum resid':>12s} {'Neg days':>10s} {'Worst 7d':>12s} {'Worst 7d dates':>25s}")
    print("-" * 95)

    for name, (start, end) in CRASH_EPOCHS.items():
        s = datetime.date.fromisoformat(start)
        e = datetime.date.fromisoformat(end)
        mask = (df.index >= s) & (df.index <= e)
        crash = df[mask]

        mean_r = crash["residual"].mean()
        cum_r = crash["residual"].sum()
        neg = (crash["residual"] < 0).sum()

        # Worst 7-day rolling residual window
        roll7 = crash["residual"].rolling(7).sum()
        if roll7.dropna().empty:
            worst7 = np.nan
            worst7_end = "N/A"
        else:
            worst7_idx = roll7.idxmin()
            worst7 = roll7.min()
            worst7_end = str(worst7_idx)

        print(f"{name:15s} {len(crash):5d} {mean_r:+12.6f} {cum_r:+12.4f} {neg:10d} {worst7:+12.4f} {worst7_end:>25s}")

    return df


# ============================================================
# Part 3: Liquidation-conditioned residuals
# ============================================================
def part3(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("PART 3: Liquidation-Conditioned Residuals (all days)")
    print("=" * 70)

    print(f"\n{'Bucket':>10s} {'N':>6s} {'Mean resid':>12s} {'Median resid':>14s} {'Mean ETH ret':>14s}")
    print("-" * 60)

    for (lo, hi), label in zip(LIQ_BUCKETS, LIQ_BUCKET_LABELS):
        if hi is None:
            mask = df["liq_count"] >= lo
        else:
            mask = (df["liq_count"] >= lo) & (df["liq_count"] <= hi)
        bucket = df[mask]
        if len(bucket) == 0:
            continue
        print(f"{label:>10s} {len(bucket):6d} {bucket['residual'].mean():+12.6f} "
              f"{bucket['residual'].median():+14.6f} {bucket['eth_ret'].mean():+14.6f}")


# ============================================================
# Part 4: Amplification quantification
# ============================================================
def part4(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("PART 4: Amplification Quantification (crash days only)")
    print("=" * 70)

    crash = df[[is_crash(d) for d in df.index]].copy()

    # Linear: residual = γ + δ(liq_count)
    X_lin = sm.add_constant(crash["liq_count"])
    model_lin = sm.OLS(crash["residual"], X_lin).fit()
    print("\nLinear model: residual = γ + δ(liq_count)")
    print(model_lin.summary().tables[1])
    delta_lin = model_lin.params["liq_count"]
    print(f"\nδ = {delta_lin:.8f} ({delta_lin * 10000:.4f} bps per liquidation event)")
    print(f"R² = {model_lin.rsquared:.4f}")

    # Log: residual = γ + δ(log(1 + liq_count))
    crash["log_liq"] = np.log1p(crash["liq_count"])
    X_log = sm.add_constant(crash["log_liq"])
    model_log = sm.OLS(crash["residual"], X_log).fit()
    print("\nLog model: residual = γ + δ·log(1 + liq_count)")
    print(model_log.summary().tables[1])
    delta_log = model_log.params["log_liq"]
    print(f"\nδ = {delta_log:.6f} ({delta_log * 10000:.2f} bps per unit log-liq)")
    print(f"R² = {model_log.rsquared:.4f}")


# ============================================================
# Part 5: Per-crash breakdown by catalyst type
# ============================================================
def part5(df: pd.DataFrame, model):
    print("\n" + "=" * 70)
    print("PART 5: Per-Crash Breakdown (Macro vs Crypto-Native)")
    print("=" * 70)

    results = []
    for name, (start, end) in CRASH_EPOCHS.items():
        s = datetime.date.fromisoformat(start)
        e = datetime.date.fromisoformat(end)
        mask = (df.index >= s) & (df.index <= e)
        crash = df[mask].copy()

        vix_peak = crash["vix"].max()
        catalyst = "macro" if vix_peak > 30 else "crypto-native"

        mean_r = crash["residual"].mean()
        cum_r = crash["residual"].sum()
        roll7 = crash["residual"].rolling(7).sum()
        worst7 = roll7.min() if not roll7.dropna().empty else np.nan
        mean_liq = crash["liq_count"].mean()

        # Per-crash δ
        if crash["liq_count"].std() > 0 and len(crash) > 5:
            X = sm.add_constant(crash["liq_count"])
            m = sm.OLS(crash["residual"], X).fit()
            delta = m.params["liq_count"]
            delta_p = m.pvalues["liq_count"]
        else:
            delta = np.nan
            delta_p = np.nan

        results.append({
            "crash": name, "catalyst": catalyst, "vix_peak": vix_peak,
            "days": len(crash), "mean_residual": mean_r, "cum_residual": cum_r,
            "worst_7d": worst7, "mean_liq": mean_liq,
            "delta": delta, "delta_p": delta_p,
        })

    rdf = pd.DataFrame(results)

    print(f"\n{'Crash':15s} {'Type':>13s} {'VIX pk':>7s} {'Days':>5s} {'Mean resid':>12s} "
          f"{'Cum resid':>11s} {'Worst 7d':>10s} {'Mean liq':>10s} {'δ (bps/liq)':>12s} {'δ p-val':>10s}")
    print("-" * 120)
    for _, r in rdf.iterrows():
        print(f"{r['crash']:15s} {r['catalyst']:>13s} {r['vix_peak']:7.1f} {r['days']:5d} "
              f"{r['mean_residual']:+12.6f} {r['cum_residual']:+11.4f} {r['worst_7d']:+10.4f} "
              f"{r['mean_liq']:10.1f} {r['delta'] * 10000:+12.4f} {r['delta_p']:10.4f}")

    # Aggregate by type
    print("\nAggregate by catalyst type:")
    for catalyst in ["macro", "crypto-native"]:
        sub = rdf[rdf["catalyst"] == catalyst]
        if sub.empty:
            continue
        total_days = sub["days"].sum()
        # Weighted mean residual
        wt_mean = (sub["mean_residual"] * sub["days"]).sum() / total_days
        total_cum = sub["cum_residual"].sum()
        worst = sub["worst_7d"].min()
        wt_liq = (sub["mean_liq"] * sub["days"]).sum() / total_days
        print(f"  {catalyst:15s}  days={total_days:4d}  mean_resid={wt_mean:+.6f}  "
              f"cum_resid={total_cum:+.4f}  worst_7d={worst:+.4f}  mean_liq={wt_liq:.1f}")


# ============================================================
# Part 6: Per-crash worst-day timelines
# ============================================================
def part6(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("PART 6: Per-Crash Worst Residual Days")
    print("=" * 70)

    all_crash_rows = []

    for name, (start, end) in CRASH_EPOCHS.items():
        s = datetime.date.fromisoformat(start)
        e = datetime.date.fromisoformat(end)
        mask = (df.index >= s) & (df.index <= e)
        crash = df[mask].copy()
        crash["crash"] = name

        # Collect for CSV
        all_crash_rows.append(crash[["crash", "eth_ret", "btc_ret", "sp_ret", "predicted", "residual", "liq_count"]])

        # Print worst 10
        worst = crash.nsmallest(10, "residual")
        cum = crash["residual"].cumsum()

        print(f"\n--- {name} ({start} to {end}) ---")
        print(f"{'Date':>12s} {'ETH ret':>10s} {'BTC ret':>10s} {'SP ret':>10s} {'Predicted':>10s} "
              f"{'Residual':>10s} {'Liq cnt':>8s} {'Cum resid':>10s}")
        print("-" * 85)
        for d, row in worst.iterrows():
            print(f"{str(d):>12s} {row['eth_ret']:+10.4f} {row['btc_ret']:+10.4f} {row['sp_ret']:+10.4f} "
                  f"{row['predicted']:+10.4f} {row['residual']:+10.4f} {row['liq_count']:8.0f} "
                  f"{cum.loc[d]:+10.4f}")

    # Save CSV
    out = pd.concat(all_crash_rows)
    out.index.name = "date"
    out.to_csv(DATA_DIR / "crash_residuals.csv")
    print(f"\nSaved crash_residuals.csv ({len(out)} rows)")


def main():
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} days ({df.index[0]} → {df.index[-1]})")

    model = part1(df)
    df = part2(df, model)
    part3(df)
    part4(df)
    part5(df, model)
    part6(df)

    print("\n" + "=" * 70)
    print("All amplification analyses complete.")


if __name__ == "__main__":
    main()
