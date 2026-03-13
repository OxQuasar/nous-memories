"""
Download BTC/USDT 1-minute candles from Binance and compute trend indicators.
Output: BTC 5-min bars with OLS trend features matching the datalog methodology.

Usage: python download_btc.py [--start 2023-01-01] [--end 2024-12-31]
"""

import ccxt
import pandas as pd
import numpy as np
import time
import os
import argparse
from datetime import datetime, timezone

# ─── CONFIG ───

SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
BATCH_SIZE = 1000  # Binance max per request
RATE_LIMIT_SLEEP = 0.5  # seconds between requests
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Trend timescales in hours (matching original datalog)
TREND_TIMESCALES = [1, 4, 8, 16, 24, 48, 96]
VOL_TIMESCALES = [1, 4, 8, 16, 24, 48, 96]

# ─── DOWNLOAD ───

def download_1m_candles(start_date, end_date):
    """Download 1-min candles from Binance via CCXT."""
    exchange = ccxt.binance({'enableRateLimit': True})

    start_ms = int(datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp() * 1000)
    end_ms = int(datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp() * 1000)

    raw_file = os.path.join(OUTPUT_DIR, f'btc_1m_{start_date}_{end_date}.csv')

    # Resume support: check existing file
    if os.path.exists(raw_file):
        existing = pd.read_csv(raw_file)
        if len(existing) > 0:
            last_ts = existing['timestamp'].iloc[-1]
            if last_ts >= end_ms:
                print(f"  Already complete: {len(existing)} rows")
                return raw_file
            start_ms = last_ts + 60000  # next minute
            print(f"  Resuming from {datetime.fromtimestamp(start_ms/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')}, {len(existing)} rows exist")

    all_candles = []
    current_ms = start_ms
    total_expected = (end_ms - start_ms) // 60000

    print(f"  Downloading {SYMBOL} 1m: {start_date} → {end_date}")
    print(f"  Expected: ~{total_expected:,} candles")

    while current_ms < end_ms:
        try:
            candles = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, since=current_ms, limit=BATCH_SIZE)
            if not candles:
                break

            # Filter to before end_ms
            candles = [c for c in candles if c[0] < end_ms]
            if not candles:
                break

            all_candles.extend(candles)
            current_ms = candles[-1][0] + 60000  # next minute after last

            downloaded = len(all_candles)
            pct = downloaded / total_expected * 100 if total_expected > 0 else 0
            if downloaded % 10000 < BATCH_SIZE:
                dt = datetime.fromtimestamp(candles[-1][0]/1000, tz=timezone.utc)
                print(f"    {downloaded:>8,} / ~{total_expected:,} ({pct:.1f}%) — {dt.strftime('%Y-%m-%d %H:%M')} UTC")

            time.sleep(RATE_LIMIT_SLEEP)

        except Exception as e:
            print(f"    Error at {datetime.fromtimestamp(current_ms/1000, tz=timezone.utc)}: {e}")
            print(f"    Retrying in 10s...")
            time.sleep(10)

    if not all_candles:
        print("  No data downloaded!")
        return None

    df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Append to existing if resuming
    if os.path.exists(raw_file):
        existing = pd.read_csv(raw_file)
        df = pd.concat([existing, df], ignore_index=True)
        df = df.drop_duplicates(subset='timestamp').sort_values('timestamp').reset_index(drop=True)

    df.to_csv(raw_file, index=False)
    print(f"  Saved {len(df):,} candles → {raw_file}")
    return raw_file


# ─── FEATURE COMPUTATION ───

def compute_ols_trend(prices, window_bars):
    """OLS slope through last `window_bars` prices. Matches datalog methodology."""
    n = len(prices)
    result = np.full(n, np.nan)

    if window_bars > n:
        return result

    # Precompute OLS components for fixed window
    x = np.arange(window_bars, dtype=np.float64)
    x_mean = x.mean()
    x_var = ((x - x_mean) ** 2).sum()

    for i in range(window_bars - 1, n):
        y = prices[i - window_bars + 1: i + 1]
        y_mean = y.mean()
        if y_mean == 0:
            result[i] = 0.0
            continue
        slope = ((x - x_mean) * (y - y_mean)).sum() / x_var
        # Normalize: slope per bar / mean price → fractional rate
        result[i] = slope / y_mean

    return result


def compute_realized_vol(returns, window_bars):
    """Realized volatility: std of returns over window."""
    n = len(returns)
    result = np.full(n, np.nan)

    if window_bars > n:
        return result

    # Rolling std
    for i in range(window_bars - 1, n):
        result[i] = np.std(returns[i - window_bars + 1: i + 1])

    return result


def build_features(raw_file, start_date, end_date):
    """Resample to 5-min and compute trend + vol features."""
    print(f"\n  Building features from {raw_file}")

    df = pd.read_csv(raw_file)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')

    # Resample to 5-minute
    df_5m = df['close'].resample('5min').last().dropna()
    df_vol = df['volume'].resample('5min').sum()

    print(f"  1-min rows: {len(df):,}")
    print(f"  5-min rows: {len(df_5m):,}")
    print(f"  Date range: {df_5m.index[0]} → {df_5m.index[-1]}")

    prices = df_5m.values.astype(np.float64)
    returns = np.diff(np.log(prices))
    returns = np.concatenate([[0.0], returns])

    result = pd.DataFrame({
        'timestamp': (df_5m.index.astype(np.int64) // 10**9).values,
        'time_str': df_5m.index.strftime('%Y-%m-%d %H:%M:%S').values,
        'price': prices,
    })

    # Compute OLS trends
    for h in TREND_TIMESCALES:
        window = h * 12  # hours → 5-min bars
        print(f"    trend_{h}h (window={window} bars)...")
        result[f'trend_{h}h'] = compute_ols_trend(prices, window)

    # Compute realized vol
    for h in VOL_TIMESCALES:
        window = h * 12
        print(f"    realized_vol_{h}h (window={window} bars)...")
        result[f'realized_vol_{h}h'] = compute_realized_vol(returns, window)

    # Drop warmup rows (need 96h = 1152 bars)
    warmup = max(TREND_TIMESCALES) * 12
    result = result.iloc[warmup:].reset_index(drop=True)
    print(f"  After warmup removal: {len(result):,} rows")

    out_file = os.path.join(OUTPUT_DIR, f'btc_5m_{start_date}_{end_date}.csv')
    result.to_csv(out_file, index=False)
    print(f"  Saved → {out_file}")
    print(f"  Price range: ${result['price'].min():,.2f} – ${result['price'].max():,.2f}")

    return out_file


# ─── MAIN ───

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', default='2023-01-01')
    parser.add_argument('--end', default='2024-12-31')
    parser.add_argument('--skip-download', action='store_true', help='Skip download, use existing 1m file')
    args = parser.parse_args()

    print(f"=== BTC Data Pipeline: {args.start} → {args.end} ===\n")

    raw_file = os.path.join(OUTPUT_DIR, f'btc_1m_{args.start}_{args.end}.csv')

    if not args.skip_download:
        raw_file = download_1m_candles(args.start, args.end)
        if raw_file is None:
            print("Download failed!")
            exit(1)
    else:
        if not os.path.exists(raw_file):
            print(f"No existing file: {raw_file}")
            exit(1)
        print(f"  Using existing: {raw_file}")

    build_features(raw_file, args.start, args.end)
    print("\n=== Done ===")
