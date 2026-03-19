"""
Pull DeFi-native stablecoin supply (DAI, GHO, USDS) from DefiLlama.
Compute correlation with ETH price to test lead/lag/concurrent signal.
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

STABLECOINS = {"dai": 5, "gho": 118, "usds": 209}
BASE_URL = "https://stablecoins.llama.fi/stablecoin"
START_DATE = "2022-01-01"
SUPPLY_FILE = os.path.join(DATA_DIR, "stablecoin_supply.csv")
ETH_FILE = os.path.join(DATA_DIR, "eth_price.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "stablecoin_supply_results.txt")

ROC_WINDOW = 7  # days for rate-of-change
LAG_RANGE = 30  # cross-correlation lags
LEAD_THRESHOLD = 3  # min lag days to count as lead
SIGNAL_THRESHOLD = 0.10  # min |r| for meaningful signal


def fetch_supply(coin_id: int, retries: int = 3) -> list[dict]:
    """Fetch stablecoin supply history."""
    url = f"{BASE_URL}/{coin_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "signals/0.1"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read())
            return data["tokens"]
        except (TimeoutError, urllib.error.URLError) as e:
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  retry {attempt+1} in {wait}s ({e})")
                time.sleep(wait)
            else:
                raise


def pull_supplies() -> pd.DataFrame:
    """Pull all stablecoin supplies, merge into daily DataFrame."""
    frames = {}
    for name, coin_id in STABLECOINS.items():
        print(f"  fetching {name} (id={coin_id})...", end=" ", flush=True)
        tokens = fetch_supply(coin_id)
        rows = []
        for t in tokens:
            supply = t.get("circulating", {}).get("peggedUSD", 0) or 0
            rows.append({
                "date": datetime.fromtimestamp(t["date"], tz=timezone.utc).strftime("%Y-%m-%d"),
                f"{name}_supply": supply,
            })
        df = pd.DataFrame(rows).drop_duplicates(subset="date", keep="last")
        frames[name] = df.set_index("date")
        print(f"{len(df)} days")
        time.sleep(0.3)

    combined = pd.concat(frames.values(), axis=1, join="outer").sort_index()
    combined = combined.fillna(0)
    combined["total_supply"] = sum(combined[f"{n}_supply"] for n in STABLECOINS)
    combined = combined.loc[START_DATE:]
    combined.index.name = "date"
    return combined.reset_index()


def load_eth_price() -> pd.DataFrame:
    """Load daily ETH price."""
    df = pd.read_csv(ETH_FILE)
    df["date"] = df["date"].astype(str)
    return df[["date", "price"]]


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
    """Classify as lead/lag/concurrent/noise."""
    if abs(peak_r) < SIGNAL_THRESHOLD:
        return "NOISE"
    if peak_lag >= LEAD_THRESHOLD:
        return "LEAD"
    if peak_lag <= -LEAD_THRESHOLD:
        return "LAG"
    return "CONCURRENT"


def analyze(supply_df: pd.DataFrame, eth_df: pd.DataFrame) -> str:
    """Run all correlation analyses, return summary text."""
    merged = supply_df.merge(eth_df, on="date", how="inner").sort_values("date")
    lines = []
    lines.append(f"Data: {merged['date'].iloc[0]} to {merged['date'].iloc[-1]} ({len(merged)} days)")
    lines.append("")

    # 1. Level correlation
    lines.append("=== LEVEL CORRELATION (raw, expect high) ===")
    for col in [f"{n}_supply" for n in STABLECOINS] + ["total_supply"]:
        r = merged[col].corr(merged["price"])
        lines.append(f"  {col:>15s} vs ETH price:  r = {r:+.3f}")
    lines.append("")

    # 2-4. Rate-of-change analysis
    # Use pct_change but replace inf (from 0-base) with NaN
    merged["eth_roc"] = merged["price"].pct_change(ROC_WINDOW)
    for name in list(STABLECOINS) + ["total"]:
        col = f"{name}_supply"
        roc = merged[col].pct_change(ROC_WINDOW)
        roc = roc.replace([np.inf, -np.inf], np.nan)
        merged[f"{name}_roc"] = roc

    # Valid rows need at least eth_roc and total_roc
    valid = merged.dropna(subset=["eth_roc", "total_roc"])

    lines.append(f"=== {ROC_WINDOW}-DAY RATE-OF-CHANGE CORRELATION ===")
    for name in list(STABLECOINS) + ["total"]:
        v = valid.dropna(subset=[f"{name}_roc"])
        r = v[f"{name}_roc"].corr(v["eth_roc"])
        lines.append(f"  {name:>10s} roc vs ETH roc:  r = {r:+.3f}  (n={len(v)})")
    lines.append("")

    # 3. Cross-correlation
    lines.append(f"=== CROSS-CORRELATION (lags -{LAG_RANGE} to +{LAG_RANGE}, +lag = supply leads) ===")
    for name in list(STABLECOINS) + ["total"]:
        v = valid.dropna(subset=[f"{name}_roc"])
        x = v[f"{name}_roc"].values
        y = v["eth_roc"].values
        cc = cross_corr(x, y, LAG_RANGE)
        peak_lag = max(cc, key=lambda k: abs(cc[k]))
        peak_r = cc[peak_lag]
        verdict = classify_signal(peak_lag, peak_r)

        lines.append(f"  {name:>10s}:  peak r = {peak_r:+.3f} at lag {peak_lag:+d}d → {verdict}")

        # Show top 5 lags
        top5 = sorted(cc.items(), key=lambda kv: abs(kv[1]), reverse=True)[:5]
        lags_str = ", ".join(f"{l:+d}d:{r:+.3f}" for l, r in top5)
        lines.append(f"             top lags: {lags_str}")
    lines.append("")

    # Overall verdict on total
    x_total = valid["total_roc"].values
    y_eth = valid["eth_roc"].values
    cc_total = cross_corr(x_total, y_eth, LAG_RANGE)
    peak_lag = max(cc_total, key=lambda k: abs(cc_total[k]))
    peak_r = cc_total[peak_lag]
    verdict = classify_signal(peak_lag, peak_r)

    lines.append("=== VERDICT ===")
    lines.append(f"Combined supply signal: {verdict}")
    lines.append(f"  Peak cross-corr: r = {peak_r:+.3f} at lag {peak_lag:+d} days")
    if verdict == "LEAD":
        lines.append(f"  → Supply change LEADS ETH price change by ~{peak_lag} days")
    elif verdict == "LAG":
        lines.append(f"  → Supply change LAGS ETH price change by ~{abs(peak_lag)} days (not actionable)")
    elif verdict == "CONCURRENT":
        lines.append(f"  → Supply and price move together (confirms but doesn't predict)")
    else:
        lines.append(f"  → No meaningful relationship detected")

    return "\n".join(lines)


def main():
    print("Pulling stablecoin supply data from DefiLlama...")
    supply_df = pull_supplies()
    supply_df.to_csv(SUPPLY_FILE, index=False)
    print(f"Saved {len(supply_df)} days → {SUPPLY_FILE}")
    print(f"  total supply range: {supply_df['total_supply'].min()/1e9:.1f}B → {supply_df['total_supply'].max()/1e9:.1f}B")
    print()

    print("Loading ETH price...")
    eth_df = load_eth_price()
    print(f"  {len(eth_df)} days loaded")
    print()

    print("Analyzing correlations...")
    summary = analyze(supply_df, eth_df)
    print()
    print(summary)

    with open(RESULTS_FILE, "w") as f:
        f.write(summary + "\n")
    print(f"\nResults saved → {RESULTS_FILE}")


if __name__ == "__main__":
    main()
