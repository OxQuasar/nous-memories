"""Exchange flow epoch analysis: net flows, epoch summaries, flow-price lead/lag."""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
MEV_DATA = Path(__file__).parent.parent / "data"

# --- Epoch definitions ---
EPOCHS = [
    ("2022_bear_1",          "2022-01-01", "2022-06-18"),
    ("2022_rally",           "2022-06-18", "2022-08-13"),
    ("2022_bear_2",          "2022-08-13", "2022-11-21"),
    ("2023_recovery",        "2022-11-21", "2024-03-11"),
    ("2024_consolidation",   "2024-03-11", "2024-08-07"),
    ("2024_bull",            "2024-08-07", "2024-12-16"),
    ("2025_crash",           "2024-12-16", "2025-04-08"),
    ("2025_recovery",        "2025-04-08", "2025-08-22"),
    ("2025_q4_chop",         "2025-08-22", "2025-12-17"),
    ("2026_crash",           "2025-12-17", "2026-02-24"),
    ("2026_recovery",        "2026-02-24", "2026-03-19"),
]

LAG_RANGE = range(-5, 6)


def load_daily_price(path: Path) -> pd.DataFrame:
    """Load hourly ETH price and resample to daily (mean)."""
    df = pd.read_csv(path, parse_dates=["datetime"])
    df["date"] = df["datetime"].dt.date
    daily = df.groupby("date")["price"].mean().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    return daily


def load_flows(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def compute_daily_flows(flows: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """Merge flows + price, compute net flow metrics."""
    df = flows.merge(prices, on="date", how="inner").sort_values("date").reset_index(drop=True)
    df["net_flow_ntv"] = df["flow_out_ntv"] - df["flow_in_ntv"]
    df["net_flow_usd"] = df["flow_out_usd"] - df["flow_in_usd"]
    df["reserve_change_ntv"] = df["sply_ex_ntv"].diff()
    df["net_flow_pct"] = df["net_flow_ntv"] / df["sply_ex_ntv"]
    df["price_return"] = df["price"].pct_change()
    return df


def epoch_summary(df: pd.DataFrame) -> pd.DataFrame:
    """One-row-per-epoch summary of flow and price metrics."""
    rows = []
    for name, start, end in EPOCHS:
        mask = (df["date"] >= start) & (df["date"] < end)
        ep = df.loc[mask]
        if ep.empty:
            continue

        n = len(ep)
        total_net_ntv = ep["net_flow_ntv"].sum()
        total_net_usd = ep["net_flow_usd"].sum()
        res_start = ep["sply_ex_ntv"].iloc[0]
        res_end = ep["sply_ex_ntv"].iloc[-1]
        p_start = ep["price"].iloc[0]
        p_end = ep["price"].iloc[-1]

        # Correlation: daily net_flow_ntv vs daily price_return
        valid = ep[["net_flow_ntv", "price_return"]].dropna()
        corr = valid["net_flow_ntv"].corr(valid["price_return"]) if len(valid) > 2 else np.nan

        rows.append({
            "epoch": name,
            "start": start,
            "end": end,
            "days": n,
            "total_net_flow_ntv": total_net_ntv,
            "total_net_flow_usd": total_net_usd,
            "avg_daily_net_flow_ntv": total_net_ntv / n,
            "avg_daily_net_flow_usd": total_net_usd / n,
            "reserve_start": res_start,
            "reserve_end": res_end,
            "reserve_change_ntv": res_end - res_start,
            "reserve_change_pct": (res_end - res_start) / res_start,
            "price_start": p_start,
            "price_end": p_end,
            "price_change_pct": (p_end - p_start) / p_start,
            "flow_price_correlation": corr,
            "days_net_outflow": (ep["net_flow_ntv"] > 0).sum(),
            "days_net_inflow": (ep["net_flow_ntv"] < 0).sum(),
        })
    return pd.DataFrame(rows)


def flow_price_lag_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-correlation of net_flow_ntv vs price_return at lags -5..+5."""
    clean = df[["net_flow_ntv", "price_return"]].dropna()
    flow = clean["net_flow_ntv"].values
    ret = clean["price_return"].values

    rows = []
    for lag in LAG_RANGE:
        if lag > 0:
            # flow leads price: correlate flow[:-lag] with return[lag:]
            corr = np.corrcoef(flow[:-lag], ret[lag:])[0, 1]
        elif lag < 0:
            # price leads flow: correlate flow[-lag:] with return[:lag]
            corr = np.corrcoef(flow[-lag:], ret[:lag])[0, 1]
        else:
            corr = np.corrcoef(flow, ret)[0, 1]
        rows.append({"lag": lag, "correlation": corr})
    return pd.DataFrame(rows)


def main():
    prices = load_daily_price(MEV_DATA / "eth_price_1h.csv")
    flows = load_flows(MEV_DATA / "exchange_flows.csv")

    # 1. Daily flows
    daily = compute_daily_flows(flows, prices)
    daily.to_csv(DATA_DIR / "daily_flows.csv", index=False)
    print(f"Daily flows: {len(daily)} rows, {daily['date'].min().date()} to {daily['date'].max().date()}")

    # 2. Epoch summary
    epochs = epoch_summary(daily)
    epochs.to_csv(DATA_DIR / "epoch_flow_summary.csv", index=False)
    print("\n=== EPOCH SUMMARY ===")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
    print(epochs.to_string(index=False))

    # 3. Flow-price lag correlation
    lag_df = flow_price_lag_correlation(daily)
    lag_df.to_csv(DATA_DIR / "flow_price_lag.csv", index=False)
    print("\n=== FLOW-PRICE LAG CORRELATION ===")
    print("(positive lag = flow leads price)")
    pd.set_option("display.float_format", lambda x: f"{x:.4f}")
    print(lag_df.to_string(index=False))


if __name__ == "__main__":
    main()
