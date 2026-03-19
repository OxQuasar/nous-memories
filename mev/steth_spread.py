"""
Pull stETH hourly prices from DefiLlama, compute stETH/ETH spread,
and test whether discount-widening predicts ETH price drops.

Segments analysis pre/post Shanghai upgrade (2023-04-12).
"""

import json
import os
import time
import urllib.request
from datetime import datetime, timezone

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

STETH_URL = "https://coins.llama.fi/chart/coingecko:staked-ether"
START = int(datetime(2022, 1, 1, tzinfo=timezone.utc).timestamp())
STETH_HOURLY_FILE = os.path.join(DATA_DIR, "steth_price_1h.csv")
ETH_HOURLY_FILE = os.path.join(DATA_DIR, "eth_price_1h.csv")
SPREAD_FILE = os.path.join(DATA_DIR, "steth_spread.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "steth_spread_results.txt")

SHANGHAI_TS = 1681257600  # 2023-04-12 UTC
SHANGHAI_DATE = "2023-04-12"
ROC_WINDOW = 7
LAG_RANGE = 30
ZSCORE_WINDOW = 30
LEAD_THRESHOLD = 3
SIGNAL_THRESHOLD = 0.10


def fetch(start_ts: int, span: int, retries: int = 3) -> list[dict]:
    """Fetch stETH price chunk with retries."""
    url = f"{STETH_URL}?start={start_ts}&span={span}&period=1h"
    req = urllib.request.Request(url, headers={"User-Agent": "signals/0.1"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read())
            return data["coins"]["coingecko:staked-ether"]["prices"]
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  retry {attempt+1} in {wait}s ({e})")
                time.sleep(wait)
            else:
                raise


def pull_steth_hourly() -> pd.DataFrame:
    """Pull stETH hourly prices, resuming from existing file."""
    now = int(time.time())
    chunk = 400

    if os.path.exists(STETH_HOURLY_FILE):
        existing = pd.read_csv(STETH_HOURLY_FILE)
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
        prices = fetch(cursor, span=span)
        new_count += len(prices)

        for p in prices:
            all_prices.append({
                "timestamp": p["timestamp"],
                "steth_price": p["price"],
            })
        print(f"{len(prices)} pts")

        if prices:
            cursor = prices[-1]["timestamp"] + 3600
        else:
            break
        time.sleep(0.5)

    df = pd.DataFrame(all_prices)
    df = df.drop_duplicates(subset="timestamp").sort_values("timestamp").reset_index(drop=True)
    df.to_csv(STETH_HOURLY_FILE, index=False)
    print(f"  +{new_count} new, {len(df)} total → {STETH_HOURLY_FILE}")
    return df


def round_to_hour(ts: int) -> int:
    """Round unix timestamp to nearest hour."""
    return round(ts / 3600) * 3600


def build_spread() -> pd.DataFrame:
    """Align stETH and ETH hourly, compute daily spread."""
    steth = pull_steth_hourly()
    eth = pd.read_csv(ETH_HOURLY_FILE)

    # Round both to nearest hour for alignment
    steth["hour"] = steth["timestamp"].apply(round_to_hour)
    eth["hour"] = eth["timestamp"].apply(round_to_hour)

    # Keep last value per hour if duplicates
    steth = steth.drop_duplicates(subset="hour", keep="last")
    eth = eth.drop_duplicates(subset="hour", keep="last")

    merged = steth[["hour", "steth_price"]].merge(
        eth[["hour", "price"]].rename(columns={"price": "eth_price"}),
        on="hour", how="inner"
    )
    merged["ratio"] = merged["steth_price"] / merged["eth_price"]
    merged["discount"] = 1.0 - merged["ratio"]

    # Resample to daily (last value of day)
    merged["date"] = pd.to_datetime(merged["hour"], unit="s", utc=True).dt.strftime("%Y-%m-%d")
    daily = merged.groupby("date").agg(
        eth_price=("eth_price", "last"),
        steth_price=("steth_price", "last"),
        ratio=("ratio", "last"),
        discount=("discount", "last"),
    ).reset_index().sort_values("date")

    daily.to_csv(SPREAD_FILE, index=False)
    print(f"Daily spread: {len(daily)} days → {SPREAD_FILE}")
    return daily


def cross_corr(x: np.ndarray, y: np.ndarray, max_lag: int) -> dict[int, float]:
    """Cross-correlation at integer lags. Positive lag = x leads y."""
    results = {}
    x_norm = (x - x.mean()) / (x.std() + 1e-12)
    y_norm = (y - y.mean()) / (y.std() + 1e-12)
    n = len(x_norm)
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            r = np.mean(x_norm[:n - lag] * y_norm[lag:]) if lag < n else 0
        else:
            r = np.mean(x_norm[-lag:] * y_norm[:n + lag]) if -lag < n else 0
        results[lag] = r
    return results


def classify_signal(peak_lag: int, peak_r: float) -> str:
    if abs(peak_r) < SIGNAL_THRESHOLD:
        return "NOISE"
    if peak_lag >= LEAD_THRESHOLD:
        return "LEAD"
    if peak_lag <= -LEAD_THRESHOLD:
        return "LAG"
    return "CONCURRENT"


def section_cross_corr(df: pd.DataFrame, label: str) -> list[str]:
    """Run cross-correlation analysis on a period segment."""
    lines = []
    if len(df) < ROC_WINDOW + LAG_RANGE + 5:
        lines.append(f"  [{label}] Too few data points ({len(df)}), skipping.")
        return lines

    df = df.copy().sort_values("date").reset_index(drop=True)
    df["disc_roc"] = df["discount"].diff(ROC_WINDOW)  # absolute change in discount
    df["eth_roc"] = df["eth_price"].pct_change(ROC_WINDOW)
    valid = df.dropna(subset=["disc_roc", "eth_roc"])

    r_concurrent = valid["disc_roc"].corr(valid["eth_roc"])
    lines.append(f"  [{label}] {ROC_WINDOW}d discount change vs ETH roc: r = {r_concurrent:+.3f} (n={len(valid)})")

    cc = cross_corr(valid["disc_roc"].values, valid["eth_roc"].values, LAG_RANGE)
    peak_lag = max(cc, key=lambda k: abs(cc[k]))
    peak_r = cc[peak_lag]
    verdict = classify_signal(peak_lag, peak_r)

    top5 = sorted(cc.items(), key=lambda kv: abs(kv[1]), reverse=True)[:5]
    lags_str = ", ".join(f"{l:+d}d:{r:+.3f}" for l, r in top5)
    lines.append(f"  [{label}] Peak cross-corr: r = {peak_r:+.3f} at lag {peak_lag:+d}d → {verdict}")
    lines.append(f"  [{label}] Top lags: {lags_str}")
    return lines


def section_conditional(df: pd.DataFrame) -> list[str]:
    """Conditional test: forward ETH returns after unusual discount-widening events."""
    lines = []
    df = df.copy().sort_values("date").reset_index(drop=True)

    if len(df) < ZSCORE_WINDOW + 15:
        lines.append("  Too few data points, skipping conditional test.")
        return lines

    # Rolling stats on discount
    df["disc_mean"] = df["discount"].rolling(ZSCORE_WINDOW, min_periods=ZSCORE_WINDOW).mean()
    df["disc_std"] = df["discount"].rolling(ZSCORE_WINDOW, min_periods=ZSCORE_WINDOW).std()
    df["disc_z"] = (df["discount"] - df["disc_mean"]) / (df["disc_std"] + 1e-12)

    # Only discount states (stETH < ETH, discount > 0) and z > 1
    events = df[(df["discount"] > 0) & (df["disc_z"] > 1.0)].copy()

    # Forward returns
    for horizon in [1, 3, 7, 14]:
        df[f"fwd_{horizon}d"] = df["eth_price"].shift(-horizon) / df["eth_price"] - 1

    events = events.merge(
        df[["date"] + [f"fwd_{h}d" for h in [1, 3, 7, 14]]],
        on="date", how="left", suffixes=("", "_y")
    )
    # Drop _y columns if merge created them
    events = events[[c for c in events.columns if not c.endswith("_y")]]

    lines.append(f"  Events (discount > 0, z > 1σ): {len(events)}")
    if len(events) == 0:
        lines.append("  No qualifying events found.")
        return lines

    lines.append(f"  {'Horizon':>10s}  {'Mean':>8s}  {'Median':>8s}  {'% Neg':>8s}  {'Count':>6s}")
    for horizon in [1, 3, 7, 14]:
        col = f"fwd_{horizon}d"
        vals = events[col].dropna()
        if len(vals) == 0:
            continue
        lines.append(
            f"  {horizon:>8d}d  {vals.mean():+8.3%}  {vals.median():+8.3%}"
            f"  {(vals < 0).mean():8.1%}  {len(vals):>6d}"
        )
    return lines


def top_discount_events(df: pd.DataFrame, n: int = 10) -> list[str]:
    """List top N largest discount days with forward 7d ETH return."""
    lines = []
    df = df.copy().sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["eth_price"].shift(-7) / df["eth_price"] - 1

    # Only discount states
    disc = df[df["discount"] > 0].nlargest(n, "discount")

    lines.append(f"  {'Date':>12s}  {'Discount':>10s}  {'ETH Price':>10s}  {'7d Fwd Ret':>10s}")
    for _, row in disc.iterrows():
        fwd = f"{row['fwd_7d']:+.2%}" if pd.notna(row["fwd_7d"]) else "N/A"
        lines.append(
            f"  {row['date']:>12s}  {row['discount']:10.4%}"
            f"  ${row['eth_price']:>9.0f}  {fwd:>10s}"
        )
    return lines


def analyze(daily: pd.DataFrame) -> str:
    """Full analysis, return summary text."""
    lines = []
    lines.append(f"Data: {daily['date'].iloc[0]} to {daily['date'].iloc[-1]} ({len(daily)} days)")
    lines.append(f"Discount range: {daily['discount'].min():+.4%} to {daily['discount'].max():+.4%}")
    lines.append(f"Mean discount: {daily['discount'].mean():+.4%}")
    lines.append(f"Shanghai upgrade: {SHANGHAI_DATE}")
    lines.append("")

    pre = daily[daily["date"] < SHANGHAI_DATE]
    post = daily[daily["date"] >= SHANGHAI_DATE]
    lines.append(f"Pre-Shanghai: {len(pre)} days, post-Shanghai: {len(post)} days")
    lines.append("")

    # A. Cross-correlation
    lines.append("=== A. CROSS-CORRELATION (discount change vs ETH roc) ===")
    lines.append("  (+lag = discount leads price)")
    lines.extend(section_cross_corr(daily, "Full"))
    lines.extend(section_cross_corr(pre, "Pre-Shanghai"))
    lines.extend(section_cross_corr(post, "Post-Shanghai"))
    lines.append("")

    # B. Conditional test (post-Shanghai only)
    lines.append("=== B. CONDITIONAL TEST: Forward ETH returns after unusual discount (post-Shanghai) ===")
    lines.extend(section_conditional(post))
    lines.append("")

    # Also run on pre-Shanghai for comparison
    lines.append("=== B2. CONDITIONAL TEST: Pre-Shanghai (for comparison) ===")
    lines.extend(section_conditional(pre))
    lines.append("")

    # C. Top discount events
    lines.append("=== C. TOP 10 LARGEST DISCOUNT DAYS ===")
    lines.extend(top_discount_events(daily))
    lines.append("")

    lines.append("=== C2. TOP 10 POST-SHANGHAI DISCOUNT DAYS ===")
    lines.extend(top_discount_events(post))
    lines.append("")

    # Verdicts
    lines.append("=== VERDICT ===")
    for label, subset in [("Pre-Shanghai", pre), ("Post-Shanghai", post)]:
        if len(subset) < ROC_WINDOW + LAG_RANGE + 5:
            lines.append(f"  {label}: insufficient data")
            continue
        s = subset.copy().sort_values("date").reset_index(drop=True)
        s["disc_roc"] = s["discount"].diff(ROC_WINDOW)
        s["eth_roc"] = s["eth_price"].pct_change(ROC_WINDOW)
        v = s.dropna(subset=["disc_roc", "eth_roc"])
        cc = cross_corr(v["disc_roc"].values, v["eth_roc"].values, LAG_RANGE)
        peak_lag = max(cc, key=lambda k: abs(cc[k]))
        peak_r = cc[peak_lag]
        verdict = classify_signal(peak_lag, peak_r)
        lines.append(f"  {label}: {verdict} (peak r = {peak_r:+.3f} at lag {peak_lag:+d}d)")

    return "\n".join(lines)


def main():
    print("Building stETH/ETH spread data...")
    daily = build_spread()
    print(f"  discount range: {daily['discount'].min():+.4%} to {daily['discount'].max():+.4%}")
    print()

    print("Analyzing...")
    summary = analyze(daily)
    print()
    print(summary)

    with open(RESULTS_FILE, "w") as f:
        f.write(summary + "\n")
    print(f"\nResults saved → {RESULTS_FILE}")


if __name__ == "__main__":
    main()
