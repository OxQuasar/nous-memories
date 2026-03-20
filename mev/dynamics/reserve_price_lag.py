"""Task A: Reserve-change vs price cross-correlation at lags -5..+5."""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
LAG_RANGE = range(-5, 6)


def lag_correlation(x: np.ndarray, y: np.ndarray) -> list[dict]:
    rows = []
    for lag in LAG_RANGE:
        if lag > 0:
            corr = np.corrcoef(x[:-lag], y[lag:])[0, 1]
        elif lag < 0:
            corr = np.corrcoef(x[-lag:], y[:lag])[0, 1]
        else:
            corr = np.corrcoef(x, y)[0, 1]
        rows.append({"lag": lag, "correlation": corr})
    return rows


def main():
    df = pd.read_csv(DATA_DIR / "daily_flows.csv", parse_dates=["date"])
    clean = df[["reserve_change_ntv", "price_return", "net_flow_ntv"]].dropna()

    reserve = clean["reserve_change_ntv"].values
    net_flow = clean["net_flow_ntv"].values
    ret = clean["price_return"].values

    res_lag = pd.DataFrame(lag_correlation(reserve, ret))
    flow_lag = pd.DataFrame(lag_correlation(net_flow, ret))

    res_lag.to_csv(DATA_DIR / "reserve_price_lag.csv", index=False)

    # Side-by-side comparison
    combined = pd.DataFrame({
        "lag": res_lag["lag"],
        "net_flow_corr": flow_lag["correlation"],
        "reserve_chg_corr": res_lag["correlation"],
    })

    pd.set_option("display.float_format", lambda x: f"{x:.4f}")
    print("=== FLOW vs RESERVE-CHANGE: LAG CORRELATION WITH PRICE RETURN ===")
    print("(positive lag = signal leads price)\n")
    print(combined.to_string(index=False))

    # Quick summary
    best_flow = flow_lag.loc[flow_lag["correlation"].abs().idxmax()]
    best_res = res_lag.loc[res_lag["correlation"].abs().idxmax()]
    print(f"\nStrongest net_flow signal:      lag={int(best_flow['lag'])}, r={best_flow['correlation']:.4f}")
    print(f"Strongest reserve_change signal: lag={int(best_res['lag'])}, r={best_res['correlation']:.4f}")


if __name__ == "__main__":
    main()
