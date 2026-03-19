"""
Pull ETH hourly price history from DefiLlama coins API.
Saves to data/eth_price_1h.csv (and data/eth_price.csv for daily).

DefiLlama coins API: no auth.
Endpoint: GET /chart/coingecko:{id}?start={unix}&span={n}&period={1h|1d}
"""

import json
import os
import time
import urllib.request
from datetime import datetime, timezone

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

COINS_URL = "https://coins.llama.fi/chart/coingecko:ethereum"
START = int(datetime(2022, 1, 1, tzinfo=timezone.utc).timestamp())


def fetch(start_ts: int, span: int, period: str) -> list[dict]:
    """Fetch ETH price chunk from DefiLlama."""
    url = f"{COINS_URL}?start={start_ts}&span={span}&period={period}"
    req = urllib.request.Request(url, headers={"User-Agent": "signals/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data["coins"]["coingecko:ethereum"]["prices"]


def pull_hourly() -> pd.DataFrame:
    """Pull hourly ETH prices from 2022-01-01 to now."""
    all_prices = []
    now = int(time.time())
    cursor = START
    chunk = 500  # max reliable span for hourly

    while cursor < now:
        remaining = (now - cursor) // 3600
        span = min(remaining, chunk)
        if span <= 0:
            break

        d = datetime.fromtimestamp(cursor, tz=timezone.utc)
        print(f"  {d.date()} {d.strftime('%H:%M')} — {span}h...", end=" ", flush=True)
        prices = fetch(cursor, span=span, period="1h")
        all_prices.extend(prices)
        print(f"{len(prices)} pts")

        if prices:
            cursor = prices[-1]["timestamp"] + 3600
        else:
            break

        time.sleep(0.3)

    df = pd.DataFrame(all_prices)
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
    df = df.drop_duplicates(subset="timestamp").sort_values("timestamp").reset_index(drop=True)
    df = df[["datetime", "timestamp", "price"]]
    return df


def hourly_to_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Resample hourly to daily (last price of day)."""
    df = df.copy()
    df["date"] = df["datetime"].dt.date
    daily = df.groupby("date").agg(
        timestamp=("timestamp", "last"),
        price=("price", "last"),
    ).reset_index()
    return daily


def main():
    print("Pulling hourly ETH prices from DefiLlama...")
    hourly = pull_hourly()

    h_out = os.path.join(DATA_DIR, "eth_price_1h.csv")
    hourly.to_csv(h_out, index=False)
    print(f"\nHourly: {len(hourly)} points → {h_out}")
    print(f"  {hourly['datetime'].iloc[0]} → {hourly['datetime'].iloc[-1]}")

    daily = hourly_to_daily(hourly)
    d_out = os.path.join(DATA_DIR, "eth_price.csv")
    daily.to_csv(d_out, index=False)
    print(f"Daily:  {len(daily)} points → {d_out}")
    print(f"  ${daily['price'].iloc[0]:.0f} → ${daily['price'].iloc[-1]:.0f}")


if __name__ == "__main__":
    main()
