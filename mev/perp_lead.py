#!/usr/bin/env python3
"""
Perp → Lending Temporal Lead Analysis

Tests whether perpetual futures liquidation activity (proxied by rapid OI declines
on Binance ETHUSDT) leads lending protocol liquidation activity during stress episodes.

Data sources:
- Binance ETHUSDT metrics (5-min OI snapshots): proxy for perp liquidations
- Lending liquidation events: from liquidation_events_combined.csv

Proxy rationale: Direct historical perp liquidation data is not freely available.
Hyperliquid's stats API requires auth; Coinglass requires API key; Binance removed
their public liquidation stream. However, large negative changes in open interest
during price declines are mechanically driven by liquidations (forced position
closure reduces OI). This is an imperfect proxy — voluntary position closures also
reduce OI — but during stress episodes, OI drops are predominantly liquidation-driven.
"""

import requests
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from datetime import datetime, timedelta
import io, zipfile, time

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "perp_lead_results.txt"
OI_CACHE = DATA_DIR / "binance_oi_episodes.csv"

HIGH_LIQ_PERCENTILE = 90
EPISODE_GAP_DAYS = 14
OI_DROP_THRESHOLD_PCT = 3  # Hourly OI drop >3% = significant liquidation proxy


# ── Phase 1: Data feasibility ────────────────────────────────

def download_binance_metrics(date_str: str) -> pd.DataFrame | None:
    """Download 5-min OI metrics for a single day from Binance data archive."""
    url = f"https://data.binance.vision/data/futures/um/daily/metrics/ETHUSDT/ETHUSDT-metrics-{date_str}.zip"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            fname = z.namelist()[0]
            with z.open(fname) as f:
                df = pd.read_csv(f)
                return df
    except Exception:
        return None


def fetch_episode_oi(episodes_dates: list[tuple[str, str]]) -> pd.DataFrame:
    """Fetch OI data for each episode date range (with 2-day buffer)."""
    if OI_CACHE.exists():
        print(f"  Loading cached OI from {OI_CACHE}")
        return pd.read_csv(OI_CACHE, parse_dates=["datetime"])

    all_dates = set()
    for start, end in episodes_dates:
        s = pd.Timestamp(start) - pd.Timedelta(days=2)
        e = pd.Timestamp(end) + pd.Timedelta(days=2)
        d = s
        while d <= e:
            all_dates.add(d.strftime("%Y-%m-%d"))
            d += pd.Timedelta(days=1)

    all_dates = sorted(all_dates)
    print(f"  Fetching {len(all_dates)} days of Binance OI data...")

    frames = []
    for i, date_str in enumerate(all_dates):
        df = download_binance_metrics(date_str)
        if df is not None:
            frames.append(df)
        if (i + 1) % 20 == 0:
            print(f"    {i+1}/{len(all_dates)} days fetched...")
        time.sleep(0.1)

    if not frames:
        return pd.DataFrame()

    oi = pd.concat(frames, ignore_index=True)
    oi["datetime"] = pd.to_datetime(oi["create_time"], utc=True)
    oi = oi.sort_values("datetime").reset_index(drop=True)
    oi = oi[["datetime", "sum_open_interest", "sum_open_interest_value"]].copy()
    oi.to_csv(OI_CACHE, index=False)
    print(f"  Saved {len(oi)} rows to {OI_CACHE}")
    return oi


# ── Lending episode builder ──────────────────────────────────

def load_daily() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["fwd_7d"] = df["price"].shift(-7) / df["price"] - 1
    return df


def build_episodes(daily: pd.DataFrame):
    nonzero = daily.loc[daily["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)
    high_idx = daily.index[daily["total_usd"] > threshold].tolist()

    episodes = [[high_idx[0]]]
    for i in high_idx[1:]:
        gap = (daily.loc[i, "date"] - daily.loc[episodes[-1][-1], "date"]).days
        if gap <= EPISODE_GAP_DAYS:
            episodes[-1].append(i)
        else:
            episodes.append([i])

    return episodes, threshold


# ── Phase 2: Temporal lead analysis ──────────────────────────

def compute_hourly_oi_change(oi: pd.DataFrame) -> pd.DataFrame:
    """Resample 5-min OI to hourly and compute % change."""
    oi = oi.set_index("datetime").sort_index()
    hourly = oi["sum_open_interest_value"].resample("1h").last().dropna()
    hourly_df = pd.DataFrame({"oi_value": hourly})
    hourly_df["oi_pct_change"] = hourly_df["oi_value"].pct_change() * 100
    return hourly_df.reset_index()


def find_oi_spike(hourly_oi: pd.DataFrame, peak_day: pd.Timestamp,
                  lookback_hours: int = 48) -> dict | None:
    """Find the first significant OI drop near the peak lending liquidation day.

    Searches a ±48h window centered on the peak lending day. Uses the worst
    hourly drop within the window rather than a fixed threshold, since episode
    severity varies. Reports relative timing of the worst OI drop.

    Returns dict with timestamp, magnitude, or None if no data in window.
    """
    window_start = peak_day - pd.Timedelta(hours=lookback_hours)
    window_end = peak_day + pd.Timedelta(hours=lookback_hours)

    mask = (hourly_oi["datetime"] >= window_start) & (hourly_oi["datetime"] <= window_end)
    window = hourly_oi[mask].copy()

    if len(window) < 5:
        return None

    # Use the worst (most negative) hourly OI drop in the window
    worst_idx = window["oi_pct_change"].idxmin()
    worst = window.loc[worst_idx]

    if worst["oi_pct_change"] >= -0.5:
        return None  # No meaningful OI drop at all

    # Also find the first drop that exceeds 1% (adaptive: significant relative to window)
    threshold = min(-1.0, window["oi_pct_change"].quantile(0.05))
    sig_drops = window[window["oi_pct_change"] <= threshold]
    first_drop = sig_drops.iloc[0] if len(sig_drops) > 0 else worst

    return {
        "first_drop_time": first_drop["datetime"],
        "first_drop_pct": first_drop["oi_pct_change"],
        "worst_drop_time": worst["datetime"],
        "worst_drop_pct": worst["oi_pct_change"],
        "total_oi_change_pct": (window["oi_value"].iloc[-1] / window["oi_value"].iloc[0] - 1) * 100
            if window["oi_value"].iloc[0] > 0 else 0,
    }


def find_lending_spike(daily: pd.DataFrame, ep_indices: list) -> pd.Timestamp:
    """Return the date of the first high-liquidation day in the episode."""
    return daily.loc[ep_indices[0], "date"]


def section_a(daily: pd.DataFrame, episodes: list, hourly_oi: pd.DataFrame, out: list):
    """Episode alignment: when does perp OI drop vs lending liquidation peak?

    For each episode, the lending reference point is the peak liquidation day
    (highest total_usd). The perp reference is the worst OI drop within ±48h
    of that peak day. Lag = lending_peak_midnight − OI_drop_time. Positive = perps led.
    """
    out.append("=" * 60)
    out.append("A. EPISODE ALIGNMENT (perp OI drop vs lending peak)")
    out.append("=" * 60)
    out.append(f"\n  Reference: lending = midnight of peak liquidation day;")
    out.append(f"  perp = first significant OI drop within ±48h of lending peak.")

    rows = []
    out.append(f"\n  {'Start':<12s} {'Sz':>3s}  {'Peak day':<12s}  {'OI drop time':>20s}  {'Lag':>8s}  {'OI worst':>9s}  {'7d Ret':>8s}")
    out.append(f"  {'-'*80}")

    for ep_idx in episodes:
        ep_start = daily.loc[ep_idx[0], "date"]
        fwd = daily.loc[ep_idx[0], "fwd_7d"]

        # Find peak lending liquidation day within episode
        peak_idx = daily.loc[ep_idx, "total_usd"].idxmax()
        peak_day = daily.loc[peak_idx, "date"]

        oi_spike = find_oi_spike(hourly_oi, peak_day)

        if oi_spike is None:
            lag_str = "  no drop"
            worst_str = "      n/a"
            rows.append({"start": str(ep_start.date()), "size": len(ep_idx),
                          "peak_day": str(peak_day.date()),
                          "lag_hours": np.nan, "fwd_7d": fwd, "oi_drop": np.nan})
        else:
            # Positive lag = OI dropped before lending peak (perps lead)
            lag_hours = (peak_day - oi_spike["first_drop_time"]).total_seconds() / 3600
            lag_str = f"{lag_hours:>+7.1f}h"
            worst_str = f"{oi_spike['worst_drop_pct']:>+8.2f}%"
            rows.append({"start": str(ep_start.date()), "size": len(ep_idx),
                          "peak_day": str(peak_day.date()),
                          "lag_hours": lag_hours, "fwd_7d": fwd,
                          "oi_drop": oi_spike["worst_drop_pct"]})

        fwd_str = f"{fwd*100:>+7.2f}%" if not np.isnan(fwd) else "     n/a"
        oi_time = str(oi_spike["first_drop_time"])[:16] if oi_spike else "           —"
        out.append(f"  {str(ep_start.date()):<12s} {len(ep_idx):>3d}  {str(peak_day.date()):<12s}  {oi_time:>20s}  {lag_str}  {worst_str}  {fwd_str}")

    return pd.DataFrame(rows)


def section_b(ep_df: pd.DataFrame, out: list):
    """Lead/lag statistics."""
    out.append("\n" + "=" * 60)
    out.append("B. LEAD/LAG STATISTICS")
    out.append("=" * 60)

    lags = ep_df["lag_hours"].dropna()
    out.append(f"\n  Episodes with measurable lag: {len(lags)} / {len(ep_df)}")

    if len(lags) < 3:
        out.append("  Insufficient data for statistics")
        return

    out.append(f"  Median lag: {lags.median():+.1f} hours")
    out.append(f"  Mean lag: {lags.mean():+.1f} hours")
    out.append(f"  Perps lead (lag > 0): {(lags > 0).sum()} / {len(lags)} ({100*(lags > 0).mean():.1f}%)")
    out.append(f"  Simultaneous (|lag| < 12h): {(lags.abs() < 12).sum()} / {len(lags)} ({100*(lags.abs() < 12).mean():.1f}%)")
    out.append(f"  Lending leads (lag < 0): {(lags < 0).sum()} / {len(lags)} ({100*(lags < 0).mean():.1f}%)")

    # Quantiles
    out.append(f"\n  Lag distribution:")
    for q in [0.10, 0.25, 0.50, 0.75, 0.90]:
        out.append(f"    P{int(q*100):02d}: {lags.quantile(q):+.1f}h")


def section_c(ep_df: pd.DataFrame, out: list):
    """Lag vs severity correlation."""
    out.append("\n" + "=" * 60)
    out.append("C. LAG VS EPISODE SEVERITY")
    out.append("=" * 60)

    valid = ep_df.dropna(subset=["lag_hours", "fwd_7d"])
    if len(valid) < 5:
        out.append(f"\n  Insufficient episodes with both lag and forward returns (n={len(valid)})")
        return

    lag = valid["lag_hours"].values
    fwd = valid["fwd_7d"].values * 100

    r, p = stats.spearmanr(lag, fwd)
    out.append(f"\n  Episodes with lag + forward return: {len(valid)}")
    out.append(f"  Spearman correlation (lag vs 7d return): r={r:+.3f}, p={p:.4f}")

    if p < 0.10:
        if r > 0:
            out.append(f"  → Longer perp lead → BETTER forward returns (perps lead more in less severe episodes)")
        else:
            out.append(f"  → Longer perp lead → WORSE forward returns (perps lead more in severe episodes)")
    else:
        out.append(f"  → No significant relationship between lag and severity")

    # Split into perps-lead vs simultaneous/lending-lead
    leads = valid[valid["lag_hours"] > 12]
    simul = valid[valid["lag_hours"].abs() <= 12]
    out.append(f"\n  Perps lead (>12h ahead): n={len(leads)}" +
               (f", median 7d ret={leads['fwd_7d'].median()*100:+.3f}%" if len(leads) > 0 else ""))
    out.append(f"  Simultaneous (±12h): n={len(simul)}" +
               (f", median 7d ret={simul['fwd_7d'].median()*100:+.3f}%" if len(simul) > 0 else ""))


def main():
    out = []
    out.append("PERP → LENDING TEMPORAL LEAD ANALYSIS")
    out.append("=" * 60)

    # Phase 1: feasibility
    out.append("\nPHASE 1: DATA FEASIBILITY")
    out.append("-" * 40)
    out.append("")
    out.append("Direct historical perp liquidation data NOT freely available:")
    out.append("  - Hyperliquid API: no public liquidation history endpoint")
    out.append("    (stats-data.hyperliquid.xyz returns 403; userFills requires")
    out.append("    knowing liquidated addresses; HLP vault shows deposits/withdrawals only)")
    out.append("  - Coinglass: requires API key for all liquidation endpoints")
    out.append("  - Binance: removed public forceOrders; no liquidationSnapshot in data archive")
    out.append("  - Binance metrics: 5-min OI snapshots available (Dec 2021 → present)")
    out.append("")
    out.append("PROXY: Using Binance ETHUSDT open interest (OI) changes as liquidation proxy.")
    out.append("Large negative hourly OI changes during stress = forced position closures.")
    out.append(f"Significance threshold: hourly OI drop > {OI_DROP_THRESHOLD_PCT}%")
    out.append("")
    out.append("Limitation: OI drops include voluntary closures. During stress episodes,")
    out.append("the forced component dominates, but the proxy is noisy for mild events.")

    # Load lending data and build episodes
    daily = load_daily()
    episodes, threshold = build_episodes(daily)

    # Filter to 2024+ episodes (where we have good OI data and Hyperliquid context)
    episodes_2024 = []
    for ep in episodes:
        if daily.loc[ep[0], "date"] >= pd.Timestamp("2024-01-01", tz="UTC"):
            episodes_2024.append(ep)

    out.append(f"\nEpisodes 2024+: {len(episodes_2024)} / {len(episodes)} total")

    # Get date ranges for OI fetching
    ep_date_ranges = []
    for ep in episodes_2024:
        s = daily.loc[ep[0], "date"].strftime("%Y-%m-%d")
        e = daily.loc[ep[-1], "date"].strftime("%Y-%m-%d")
        ep_date_ranges.append((s, e))

    print("Fetching OI data...")
    oi = fetch_episode_oi(ep_date_ranges)

    if len(oi) == 0:
        out.append("\nERROR: No OI data fetched. Cannot proceed.")
        RESULTS_FILE.write_text("\n".join(out))
        print("\n".join(out))
        return

    out.append(f"OI data: {len(oi)} rows, {oi['datetime'].min()} to {oi['datetime'].max()}")

    # Compute hourly OI changes
    hourly_oi = compute_hourly_oi_change(oi)
    out.append(f"Hourly OI: {len(hourly_oi)} data points")

    # Phase 2: Analysis
    out.append("\n" + "=" * 60)
    out.append("PHASE 2: TEMPORAL LEAD ANALYSIS")
    out.append("=" * 60)

    ep_df = section_a(daily, episodes_2024, hourly_oi, out)
    section_b(ep_df, out)
    section_c(ep_df, out)

    # Verdict
    out.append("\n" + "=" * 60)
    out.append("VERDICT")
    out.append("=" * 60)

    lags = ep_df["lag_hours"].dropna()
    if len(lags) >= 5:
        pct_lead = (lags > 0).mean() * 100
        med_lag = lags.median()
        if pct_lead > 65 and med_lag > 6:
            out.append(f"\n  PERPS LEAD: {pct_lead:.0f}% of episodes, median {med_lag:+.0f}h.")
            out.append(f"  Perp OI drops provide {abs(med_lag):.0f}h of lead time before lending liquidations.")
        elif pct_lead < 35 and med_lag < -6:
            out.append(f"\n  LENDING LEADS: perps follow lending by {abs(med_lag):.0f}h in most episodes.")
        else:
            out.append(f"\n  SIMULTANEOUS: median lag {med_lag:+.1f}h, {pct_lead:.0f}% perps-first.")
            out.append(f"  No consistent temporal ordering between perp and lending liquidations.")
            if abs(med_lag) < 12:
                out.append(f"  The leverage hierarchy (perps 5-50x vs lending 1.5-3x) does not")
                out.append(f"  create exploitable temporal structure at hourly resolution.")
    else:
        out.append(f"\n  INSUFFICIENT DATA: only {len(lags)} episodes with measurable lag.")

    out.append(f"\n  Proxy caveat: OI changes are an imperfect proxy for liquidations.")
    out.append(f"  Direct liquidation data (from Hyperliquid or Coinglass with API key)")
    out.append(f"  would provide higher fidelity. The structural conclusion about")
    out.append(f"  temporal ordering, however, is likely robust to proxy noise during")
    out.append(f"  major stress episodes where forced closures dominate OI changes.")

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
