"""
Liquidation dynamics analysis: temporal structure, intensity, and composition across epochs.
Uses debt-side USD estimation as primary value metric.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(__file__).parent / "data"
MEV_DATA = Path(__file__).parent.parent / "data"

# --- Epoch definitions ---
EPOCHS = [
    ("2022_bear_1",        "2022-01-01", "2022-06-18", "crash"),
    ("2022_rally",         "2022-06-18", "2022-08-13", "bull"),
    ("2022_bear_2",        "2022-08-13", "2022-11-21", "crash"),
    ("2023_recovery",      "2022-11-21", "2024-03-11", "bull"),
    ("2024_consolidation", "2024-03-11", "2024-08-07", "crash"),
    ("2024_bull",          "2024-08-07", "2024-12-16", "bull"),
    ("2025_crash",         "2024-12-16", "2025-04-08", "crash"),
    ("2025_recovery",      "2025-04-08", "2025-08-22", "bull"),
    ("2025_q4_chop",       "2025-08-22", "2025-12-17", "crash"),
    ("2026_crash",         "2025-12-17", "2026-02-24", "crash"),
    ("2026_recovery",      "2026-02-24", "2026-03-19", "bull"),
]

CRASH_EPOCHS = [e[0] for e in EPOCHS if e[3] == "crash"]

STABLECOINS = {"USDC", "USDT", "DAI", "GHO", "BUSD", "GUSD", "TUSD", "sUSD", "USDP", "FRAX", "PYUSD"}
ETH_LIKE = {"WETH", "stETH", "wstETH", "rETH", "cbETH", "weETH"}

# Collateral groups for composition analysis
COLLATERAL_GROUPS = {
    "WETH": {"WETH"},
    "stETH": {"stETH"},
    "wstETH": {"wstETH"},
    "other_LST": {"rETH", "cbETH", "weETH"},
    "WBTC": {"WBTC"},
    "LINK": {"LINK"},
    "stablecoin": STABLECOINS,
}


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load liquidation events and daily ETH prices."""
    liq = pd.read_csv(DATA_DIR / "liquidations_full.csv")
    liq["date"] = pd.to_datetime(liq["timestamp"], unit="s", utc=True).dt.strftime("%Y-%m-%d")

    prices = pd.read_csv(MEV_DATA / "eth_price.csv")
    prices["date"] = prices["date"].astype(str)
    return liq, prices


def estimate_usd(liq: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """Estimate USD value per event using debt-side conversion."""
    df = liq.merge(prices[["date", "price"]], on="date", how="left")
    df["price"] = df["price"].ffill().bfill()

    def debt_usd(row):
        if row["debt_label"] in STABLECOINS:
            return row["debt_amount"]
        if row["debt_label"] == "WETH":
            return row["debt_amount"] * row["price"]
        # WBTC debt — rough 15x ETH (close enough for magnitude)
        if row["debt_label"] == "WBTC":
            return row["debt_amount"] * row["price"] * 15
        # Unknown debt: use collateral side estimate
        if row["collateral_label"] in ETH_LIKE:
            return row["collateral_amount"] * row["price"]
        return row["debt_amount"]  # fallback: assume 1:1

    df["liquidation_usd"] = df.apply(debt_usd, axis=1)
    return df


def collateral_group(label: str) -> str:
    for group, members in COLLATERAL_GROUPS.items():
        if label in members:
            return group
    return "other"


def epoch_summary(df: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """Per-epoch liquidation summary for real + all categories."""
    rows = []
    for name, start, end, regime in EPOCHS:
        mask = (df["date"] >= start) & (df["date"] < end)
        ep_all = df[mask]
        ep_real = ep_all[ep_all["category"] == "real"]

        if ep_all.empty:
            continue

        price_start = prices.loc[prices["date"] >= start, "price"].iloc[0] if len(prices[prices["date"] >= start]) > 0 else np.nan
        price_end = prices.loc[prices["date"] < end, "price"].iloc[-1] if len(prices[prices["date"] < end]) > 0 else np.nan
        price_change_pct = (price_end - price_start) / price_start if price_start else np.nan

        total_days = (pd.Timestamp(end) - pd.Timestamp(start)).days

        for cat_name, ep in [("all", ep_all), ("real", ep_real)]:
            if ep.empty:
                rows.append({"epoch": name, "category_filter": cat_name, "regime": regime})
                continue

            daily = ep.groupby("date")["liquidation_usd"].sum()
            top3 = daily.nlargest(3).sum()
            total_vol = ep["liquidation_usd"].sum()

            rows.append({
                "epoch": name,
                "category_filter": cat_name,
                "regime": regime,
                "total_liquidation_usd": total_vol,
                "event_count": len(ep),
                "avg_event_usd": ep["liquidation_usd"].mean(),
                "median_event_usd": ep["liquidation_usd"].median(),
                "max_event_usd": ep["liquidation_usd"].max(),
                "unique_users": ep["user"].nunique(),
                "days_with_liqs": daily.index.nunique(),
                "total_days": total_days,
                "top_3_days_pct": top3 / total_vol if total_vol > 0 else 0,
                "price_start": price_start,
                "price_end": price_end,
                "price_change_pct": price_change_pct,
                "liq_per_day_usd": total_vol / total_days,
                "liq_intensity": total_vol / abs(price_change_pct) if price_change_pct and abs(price_change_pct) > 0.01 else np.nan,
            })

    return pd.DataFrame(rows)


def crash_spike_days(df: pd.DataFrame) -> pd.DataFrame:
    """Identify spike days in crash epochs."""
    real = df[df["category"] == "real"]
    rows = []

    for name, start, end, regime in EPOCHS:
        if name not in CRASH_EPOCHS:
            continue

        mask = (real["date"] >= start) & (real["date"] < end)
        ep = real[mask]
        if ep.empty:
            continue

        daily = ep.groupby("date").agg(
            volume_usd=("liquidation_usd", "sum"),
            events=("liquidation_usd", "count"),
            eth_price=("price", "first"),
        ).reset_index()

        # Fill all dates in range for price return calculation
        all_dates = pd.date_range(start, end, freq="D")[:-1].strftime("%Y-%m-%d")
        daily = daily.set_index("date").reindex(all_dates).fillna(0).reset_index()
        daily.columns = ["date", "volume_usd", "events", "eth_price"]

        # Get price for all dates from the df
        price_by_date = df.groupby("date")["price"].first()
        daily["eth_price"] = daily["date"].map(price_by_date)
        daily["eth_price"] = daily["eth_price"].ffill().bfill()
        daily["price_return"] = daily["eth_price"].pct_change()

        mean_vol = daily["volume_usd"].mean()
        std_vol = daily["volume_usd"].std()
        threshold = mean_vol + 2 * std_vol

        # Time to first major spike
        major_days = daily[daily["volume_usd"] > 10_000_000]
        first_spike_day = int((pd.Timestamp(major_days.iloc[0]["date"]) - pd.Timestamp(start)).days) if len(major_days) > 0 else -1

        spike_mask = daily["volume_usd"] > threshold
        spike_vol = daily.loc[spike_mask, "volume_usd"].sum()
        total_vol = daily["volume_usd"].sum()

        for _, row in daily[spike_mask].iterrows():
            rows.append({
                "epoch": name,
                "date": row["date"],
                "volume_usd": row["volume_usd"],
                "events": int(row["events"]),
                "eth_price": row["eth_price"],
                "price_return_1d": row["price_return"],
                "is_spike": True,
            })

        # Add epoch-level spike summary as a special row
        rows.append({
            "epoch": name,
            "date": "SUMMARY",
            "volume_usd": total_vol,
            "events": int(ep.shape[0]),
            "eth_price": np.nan,
            "price_return_1d": np.nan,
            "spike_days": int(spike_mask.sum()),
            "spike_vol_pct": spike_vol / total_vol if total_vol > 0 else 0,
            "days_to_first_10m": first_spike_day,
            "threshold_usd": threshold,
        })

    return pd.DataFrame(rows)


def collateral_composition(df: pd.DataFrame) -> pd.DataFrame:
    """Per-epoch collateral composition for real liquidations."""
    real = df[df["category"] == "real"].copy()
    real["coll_group"] = real["collateral_label"].apply(collateral_group)

    rows = []
    for name, start, end, regime in EPOCHS:
        mask = (real["date"] >= start) & (real["date"] < end)
        ep = real[mask]
        if ep.empty:
            continue

        total = ep["liquidation_usd"].sum()
        by_group = ep.groupby("coll_group")["liquidation_usd"].sum()

        row = {"epoch": name, "regime": regime, "total_real_usd": total}
        for g in ["WETH", "stETH", "wstETH", "other_LST", "WBTC", "LINK", "stablecoin", "other"]:
            val = by_group.get(g, 0)
            row[f"{g}_usd"] = val
            row[f"{g}_pct"] = val / total if total > 0 else 0
        rows.append(row)

    return pd.DataFrame(rows)


def print_epoch_summary(summary: pd.DataFrame):
    """Print epoch summary tables."""
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 220)

    print("\n" + "=" * 80)
    print("EPOCH LIQUIDATION SUMMARY — REAL ONLY")
    print("=" * 80)
    real = summary[summary["category_filter"] == "real"].copy()
    cols = ["epoch", "regime", "event_count", "total_liquidation_usd", "avg_event_usd",
            "median_event_usd", "max_event_usd", "unique_users", "days_with_liqs",
            "total_days", "top_3_days_pct", "price_change_pct", "liq_per_day_usd"]
    pd.set_option("display.float_format", lambda x: f"{x:,.0f}" if abs(x) > 100 else f"{x:.3f}")
    print(real[cols].to_string(index=False))

    print("\n" + "=" * 80)
    print("CROSS-EPOCH COMPARISON — REAL LIQUIDATIONS")
    print("=" * 80)
    crash_rows = real[real["regime"] == "crash"].copy()
    cols2 = ["epoch", "price_change_pct", "total_liquidation_usd", "liq_per_day_usd", "liq_intensity",
             "event_count", "unique_users", "top_3_days_pct"]
    print(crash_rows[cols2].to_string(index=False))


def print_spike_days(spikes: pd.DataFrame):
    print("\n" + "=" * 80)
    print("CRASH EPOCH SPIKE DAYS (>2σ above mean)")
    print("=" * 80)

    summaries = spikes[spikes["date"] == "SUMMARY"]
    detail = spikes[spikes["date"] != "SUMMARY"]

    for _, s in summaries.iterrows():
        epoch = s["epoch"]
        print(f"\n--- {epoch} ---")
        print(f"  Total real volume: ${s['volume_usd']:,.0f}")
        print(f"  Events: {int(s['events'])}")
        spike_days = int(s.get("spike_days", 0))
        spike_pct = s.get("spike_vol_pct", 0)
        print(f"  Spike days: {spike_days} ({spike_pct:.1%} of volume)")
        first = int(s.get("days_to_first_10m", -1))
        print(f"  Days to first >$10M day: {first if first >= 0 else 'never'}")
        print(f"  Spike threshold: ${s.get('threshold_usd', 0):,.0f}")

        ep_detail = detail[detail["epoch"] == epoch].sort_values("volume_usd", ascending=False)
        if len(ep_detail) > 0:
            print(f"  {'Date':>12s}  {'Volume':>14s}  {'Events':>6s}  {'ETH Price':>10s}  {'1d Return':>9s}")
            for _, d in ep_detail.head(10).iterrows():
                print(f"  {d['date']:>12s}  ${d['volume_usd']:>13,.0f}  {int(d['events']):>6d}  ${d['eth_price']:>9,.0f}  {d['price_return_1d']:>8.1%}")


def print_composition(comp: pd.DataFrame):
    print("\n" + "=" * 80)
    print("COLLATERAL COMPOSITION — REAL LIQUIDATIONS BY EPOCH")
    print("=" * 80)

    groups = ["WETH", "stETH", "wstETH", "other_LST", "WBTC", "LINK", "stablecoin", "other"]
    header = f"{'Epoch':<22s} {'Total $':>14s}"
    for g in groups:
        header += f" {g:>8s}"
    print(header)

    for _, row in comp.iterrows():
        line = f"{row['epoch']:<22s} ${row['total_real_usd']:>13,.0f}"
        for g in groups:
            pct = row.get(f"{g}_pct", 0)
            line += f" {pct:>7.1%}"
        print(line)


def main():
    liq, prices = load_data()
    df = estimate_usd(liq, prices)

    # Quick sanity check
    print(f"Total events: {len(df):,}")
    print(f"Events with USD estimate: {(df['liquidation_usd'] > 0).sum():,}")
    print(f"Total liquidation volume: ${df['liquidation_usd'].sum():,.0f}")
    real_vol = df[df["category"] == "real"]["liquidation_usd"].sum()
    print(f"Real liquidation volume: ${real_vol:,.0f}")

    # 1. Epoch summary
    summary = epoch_summary(df, prices)
    summary.to_csv(DATA_DIR / "epoch_liquidation_summary.csv", index=False)
    print_epoch_summary(summary)

    # 2. Crash spike days
    spikes = crash_spike_days(df)
    spikes.to_csv(DATA_DIR / "crash_spike_days.csv", index=False)
    print_spike_days(spikes)

    # 3. Collateral composition
    comp = collateral_composition(df)
    print_composition(comp)

    # 4. Intensity relationship analysis
    print("\n" + "=" * 80)
    print("LIQUIDATION INTENSITY ANALYSIS")
    print("=" * 80)
    real_summary = summary[(summary["category_filter"] == "real") & (summary["regime"] == "crash")].copy()
    real_summary = real_summary.dropna(subset=["liq_intensity"])
    if len(real_summary) > 1:
        # Check if relationship is linear/convex/concave
        pct = real_summary["price_change_pct"].abs().values
        vol = real_summary["total_liquidation_usd"].values
        # Log-log regression
        valid = (pct > 0) & (vol > 0)
        if valid.sum() > 1:
            log_pct = np.log(pct[valid])
            log_vol = np.log(vol[valid])
            slope, intercept = np.polyfit(log_pct, log_vol, 1)
            print(f"\n  Log-log regression: log(volume) = {slope:.2f} * log(|price_change|) + {intercept:.1f}")
            print(f"  Elasticity = {slope:.2f}")
            if slope > 1.2:
                print("  → CONVEX: Liquidation volume accelerates with larger crashes")
            elif slope < 0.8:
                print("  → CONCAVE: Liquidation volume saturates in larger crashes")
            else:
                print("  → ROUGHLY LINEAR: Liquidation volume scales proportionally")

    for _, row in real_summary.iterrows():
        print(f"  {row['epoch']:<22s} Δprice={row['price_change_pct']:>7.1%}  vol=${row['total_liquidation_usd']:>14,.0f}  intensity=${row['liq_intensity']:>14,.0f}/1%")


if __name__ == "__main__":
    main()
