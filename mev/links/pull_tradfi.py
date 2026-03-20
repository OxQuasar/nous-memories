#!/usr/bin/env python3
"""Pull TradFi + BTC daily data, merge with ETH price → tradfi_daily.csv"""

import pandas as pd
import yfinance as yf
from pathlib import Path
from io import StringIO
import requests

START = "2022-01-01"
END = "2026-03-19"

DATA_DIR = Path(__file__).parent / "data"
ETH_PATH = Path(__file__).parent.parent / "data" / "eth_price.csv"
OUT_PATH = DATA_DIR / "tradfi_daily.csv"

# --- yfinance tickers ---
YF_TICKERS = {
    "^GSPC": "sp500",
    "^VIX": "vix",
    "JPY=X": "usdjpy",
    "DX-Y.NYB": "dxy",
    "^TNX": "tnx",
    "GC=F": "gold",
    "BTC-USD": "btc",
}

# --- FRED series ---
FRED_SERIES = {
    "FEDFUNDS": "fed_funds",
    "T10Y2Y": "yield_spread",
    "CPIAUCSL": "cpi",
}
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={start}&coed={end}"


def pull_yfinance() -> pd.DataFrame:
    """Download all yfinance tickers, return daily close DataFrame."""
    tickers = list(YF_TICKERS.keys())
    raw = yf.download(tickers, start=START, end=END, auto_adjust=True)
    # Extract Close prices
    close = raw["Close"]
    # Rename columns
    close = close.rename(columns=YF_TICKERS)
    close.index = pd.to_datetime(close.index).date
    close.index.name = "date"
    return close


def pull_fred() -> pd.DataFrame:
    """Download FRED series via direct CSV URLs."""
    frames = {}
    for series_id, col_name in FRED_SERIES.items():
        url = FRED_URL.format(series=series_id, start=START, end=END)
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text), parse_dates=["observation_date"])
        df = df.rename(columns={"observation_date": "date", series_id: col_name})
        df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
        df["date"] = df["date"].dt.date
        df = df.set_index("date")
        frames[col_name] = df[col_name]
        print(f"  FRED {series_id} → {len(df)} rows")
    return pd.DataFrame(frames)


def load_eth() -> pd.DataFrame:
    """Load ETH daily price."""
    df = pd.read_csv(ETH_PATH, parse_dates=["date"])
    df["date"] = df["date"].dt.date
    df = df[["date", "price"]].rename(columns={"price": "eth_price"})
    return df.set_index("date")


def main():
    print("Pulling yfinance data...")
    yf_df = pull_yfinance()
    print(f"  yfinance: {len(yf_df)} rows, {list(yf_df.columns)}")

    print("Pulling FRED data...")
    fred_df = pull_fred()

    print("Loading ETH price...")
    eth_df = load_eth()
    print(f"  ETH: {len(eth_df)} rows")

    # Daily date index
    date_idx = pd.date_range(START, END, freq="D")
    date_idx_date = [d.date() for d in date_idx]
    merged = pd.DataFrame(index=date_idx_date)
    merged.index.name = "date"

    # Join all sources
    merged = merged.join(eth_df)
    merged = merged.join(yf_df)
    merged = merged.join(fred_df)

    # Forward-fill all (market gaps, monthly FRED, etc.)
    merged = merged.ffill()

    # Derived: ETH/BTC ratio
    merged["eth_btc"] = merged["eth_price"] / merged["btc"]

    # Final column order
    cols = ["eth_price", "btc", "eth_btc", "sp500", "vix", "usdjpy", "dxy", "tnx", "gold",
            "fed_funds", "yield_spread", "cpi"]
    merged = merged[cols]

    # Save
    merged.to_csv(OUT_PATH)
    print(f"\nSaved to {OUT_PATH}")
    print(f"  Rows: {len(merged)}")
    print(f"  Date range: {merged.index[0]} → {merged.index[-1]}")

    # Report missing
    total = len(merged)
    for col in cols:
        missing = merged[col].isna().sum()
        pct = missing / total * 100
        if pct > 5:
            print(f"  ⚠ {col}: {missing}/{total} missing ({pct:.1f}%)")
        elif missing > 0:
            print(f"  {col}: {missing}/{total} missing ({pct:.1f}%)")

    print("Done.")


if __name__ == "__main__":
    main()
