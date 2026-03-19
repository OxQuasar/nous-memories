"""
Pull ETH hourly price history from DefiLlama coins API.
Saves to data/eth_price_1h.csv (and data/eth_price.csv for daily).

Resumes from existing data if present. Retries on timeout.
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
HOURLY_FILE = os.path.join(DATA_DIR, "eth_price_1h.csv")
DAILY_FILE = os.path.join(DATA_DIR, "eth_price.csv")


def fetch(start_ts: int, span: int, period: str, retries: int = 3) -> list[dict]:
    """Fetch ETH price chunk with retries."""
    url = f"{COINS_URL}?start={start_ts}&span={span}&period={period}"
    req = urllib.request.Request(url, headers={"User-Agent": "signals/0.1"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read())
            return data["coins"]["coingecko:ethereum"]["prices"]
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  retry {attempt+1} in {wait}s ({e})")
                time.sleep(wait)
            else:
                raise


def pull_hourly() -> pd.DataFrame:
    """Pull hourly ETH prices, resuming from existing file."""
    now = int(time.time())
    chunk = 400

    # Resume from existing data
    if os.path.exists(HOURLY_FILE):
        existing = pd.read_csv(HOURLY_FILE)
        all_prices = existing.to_dict("records")
        cursor = int(existing["timestamp"].max()) + 3600
        print(f"  resuming from {len(existing)} existing points...")
    else:
        all_prices = []
        cursor = START

    new_count = 0
    while cursor < now:
        remaining = (now - cursor) // 3600
        span = min(remaining, chunk)
        if span <= 0:
            break

        d = datetime.fromtimestamp(cursor, tz=timezone.utc)
        print(f"  {d.date()} {d.strftime('%H:%M')} — {span}h...", end=" ", flush=True)
        prices = fetch(cursor, span=span, period="1h")
        new_count += len(prices)

        for p in prices:
            all_prices.append({
                "datetime": pd.Timestamp(p["timestamp"], unit="s", tz="UTC"),
                "timestamp": p["timestamp"],
                "price": p["price"],
            })
        print(f"{len(prices)} pts")

        if prices:
            cursor = prices[-1]["timestamp"] + 3600
        else:
            break

        time.sleep(0.5)

    df = pd.DataFrame(all_prices)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df = df.drop_duplicates(subset="timestamp").sort_values("timestamp").reset_index(drop=True)
    df = df[["datetime", "timestamp", "price"]]

    # Save incrementally
    df.to_csv(HOURLY_FILE, index=False)
    print(f"  +{new_count} new points, {len(df)} total")
    return df


def hourly_to_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Resample hourly to daily (last price of day)."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["datetime"]).dt.date
    daily = df.groupby("date").agg(
        timestamp=("timestamp", "last"),
        price=("price", "last"),
    ).reset_index()
    return daily


def main():
    print("Pulling hourly ETH prices from DefiLlama...")
    hourly = pull_hourly()

    print(f"\nHourly: {len(hourly)} points → {HOURLY_FILE}")
    print(f"  {hourly['datetime'].iloc[0]} → {hourly['datetime'].iloc[-1]}")

    daily = hourly_to_daily(hourly)
    daily.to_csv(DAILY_FILE, index=False)
    print(f"Daily:  {len(daily)} points → {DAILY_FILE}")
    print(f"  ${daily['price'].iloc[0]:.0f} → ${daily['price'].iloc[-1]:.0f}")


if __name__ == "__main__":
    main()
