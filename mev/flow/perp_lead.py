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


OI_CONTROL_CACHE = DATA_DIR / "binance_oi_control.csv"

CONTROL_MONTHS = [
    ("2024-09-01", "2024-09-30"),  # No lending episode in Sep 2024
    ("2024-11-01", "2024-11-30"),  # Episode is Nov 12 (1 day) — mostly quiet
    ("2025-07-01", "2025-07-31"),  # No episode in Jul 2025
]


def fetch_control_oi() -> pd.DataFrame:
    """Fetch OI data for non-episode control months."""
    if OI_CONTROL_CACHE.exists():
        print(f"  Loading cached control OI from {OI_CONTROL_CACHE}")
        return pd.read_csv(OI_CONTROL_CACHE, parse_dates=["datetime"])

    all_dates = set()
    for start, end in CONTROL_MONTHS:
        d = pd.Timestamp(start)
        e = pd.Timestamp(end)
        while d <= e:
            all_dates.add(d.strftime("%Y-%m-%d"))
            d += pd.Timedelta(days=1)

    all_dates = sorted(all_dates)
    print(f"  Fetching {len(all_dates)} days of control OI data...")

    frames = []
    for i, date_str in enumerate(all_dates):
        df = download_binance_metrics(date_str)
        if df is not None:
            frames.append(df)
        time.sleep(0.1)

    if not frames:
        return pd.DataFrame()

    oi = pd.concat(frames, ignore_index=True)
    oi["datetime"] = pd.to_datetime(oi["create_time"], utc=True)
    oi = oi.sort_values("datetime").reset_index(drop=True)
    oi = oi[["datetime", "sum_open_interest", "sum_open_interest_value"]].copy()
    oi.to_csv(OI_CONTROL_CACHE, index=False)
    print(f"  Saved {len(oi)} rows to {OI_CONTROL_CACHE}")
    return oi


def load_raw_lending_events() -> pd.DataFrame:
    """Load all raw lending events with sub-daily timestamps and USD volumes."""
    price_h = pd.read_csv(DATA_DIR / "eth_price_1h.csv")
    price_h["datetime"] = pd.to_datetime(price_h["datetime"], utc=True).dt.floor("h")
    price_h = price_h.set_index("datetime").sort_index()

    frames = []

    # Aave (volume in ETH → needs price conversion)
    aave = pd.read_csv(DATA_DIR / "liquidation_events_raw.csv")
    aave["dt"] = pd.to_datetime(aave["timestamp"], unit="s", utc=True)
    aave["hour"] = aave["dt"].dt.floor("h")
    aave = aave.merge(price_h[["price"]].reset_index().rename(columns={"datetime": "hour"}),
                       on="hour", how="left")
    aave["volume_usd"] = aave["collateral_eth"] * aave["price"]
    frames.append(aave[["dt", "hour", "volume_usd"]].dropna(subset=["volume_usd"]))

    # Compound (volume already in USD)
    comp = pd.read_csv(DATA_DIR / "liquidation_compound_raw.csv")
    comp["dt"] = pd.to_datetime(comp["timestamp"], unit="s", utc=True)
    comp["hour"] = comp["dt"].dt.floor("h")
    frames.append(comp[["dt", "hour", "volume_usd"]])

    # Maker (volume in ETH → needs price conversion)
    maker = pd.read_csv(DATA_DIR / "liquidation_maker_raw.csv")
    maker["dt"] = pd.to_datetime(maker["timestamp"], unit="s", utc=True)
    maker["hour"] = maker["dt"].dt.floor("h")
    maker = maker.merge(price_h[["price"]].reset_index().rename(columns={"datetime": "hour"}),
                         on="hour", how="left")
    maker["volume_usd"] = maker["volume_eth"] * maker["price"]
    frames.append(maker[["dt", "hour", "volume_usd"]].dropna(subset=["volume_usd"]))

    events = pd.concat(frames, ignore_index=True).sort_values("dt").reset_index(drop=True)
    return events


def section_g(daily: pd.DataFrame, episodes_2024: list, hourly_oi: pd.DataFrame, out: list):
    """Test G: False positive rate — how often does OI drop >3% without a lending episode?"""
    out.append("\n" + "=" * 60)
    out.append("G. FALSE POSITIVE RATE")
    out.append("=" * 60)

    # 1. Count all >3% hourly OI drops in episode windows
    episode_drops = hourly_oi[hourly_oi["oi_pct_change"] < -OI_DROP_THRESHOLD_PCT]
    out.append(f"\n  Total hours with >{OI_DROP_THRESHOLD_PCT}% OI drop in episode windows: {len(episode_drops)}")

    # 2. Fetch control period OI
    print("Fetching control OI data...")
    control_oi = fetch_control_oi()
    if len(control_oi) == 0:
        out.append("  ERROR: Could not fetch control OI data")
        return

    control_hourly = compute_hourly_oi_change(control_oi)
    control_drops = control_hourly[control_hourly["oi_pct_change"] < -OI_DROP_THRESHOLD_PCT]

    control_days = (control_hourly["datetime"].max() - control_hourly["datetime"].min()).total_seconds() / 86400
    episode_days = (hourly_oi["datetime"].max() - hourly_oi["datetime"].min()).total_seconds() / 86400

    out.append(f"  Control period: {control_days:.0f} days ({len(control_hourly)} hours)")
    out.append(f"  Control drops >{OI_DROP_THRESHOLD_PCT}%: {len(control_drops)}")

    # 3. False positive rate calculation
    ep_rate = len(episode_drops) / episode_days if episode_days > 0 else 0
    ctrl_rate = len(control_drops) / control_days if control_days > 0 else 0

    out.append(f"\n  Drop rate (episode windows): {ep_rate:.2f} per day")
    out.append(f"  Drop rate (control periods): {ctrl_rate:.2f} per day")

    if ctrl_rate > 0:
        enrichment = ep_rate / ctrl_rate
        out.append(f"  Enrichment ratio: {enrichment:.1f}x (episode vs control)")
    else:
        enrichment = float("inf")
        out.append(f"  Enrichment ratio: ∞ (no control drops)")

    # 4. Estimate annualized false alarm rate
    annual_false_alarms = ctrl_rate * 365
    out.append(f"\n  Estimated annual false alarms (>{OI_DROP_THRESHOLD_PCT}% drop, no lending episode): {annual_false_alarms:.0f}")
    out.append(f"  Actual lending episodes per year: ~{len(episodes_2024) / 2:.0f}")

    if annual_false_alarms > 0:
        precision = len(episodes_2024) / (len(episodes_2024) + annual_false_alarms * 2) * 100
        out.append(f"  Rough precision estimate: ~{precision:.0f}%")
    else:
        out.append(f"  Precision: high (no false alarms in control period)")

    # 5. Test at lower thresholds too
    out.append(f"\n  Threshold sensitivity:")
    out.append(f"  {'Thresh':>7s}  {'Ep drops':>9s}  {'Ctrl drops':>10s}  {'Ep/day':>7s}  {'Ctrl/day':>9s}  {'Enrich':>7s}")
    out.append(f"  {'-'*55}")
    for thresh in [1.0, 2.0, 3.0, 4.0, 5.0]:
        n_ep = (hourly_oi["oi_pct_change"] < -thresh).sum()
        n_ctrl = (control_hourly["oi_pct_change"] < -thresh).sum()
        r_ep = n_ep / episode_days if episode_days > 0 else 0
        r_ctrl = n_ctrl / control_days if control_days > 0 else 0
        enrich = r_ep / r_ctrl if r_ctrl > 0 else float("inf")
        e_str = f"{enrich:.1f}x" if enrich < 1000 else "∞"
        out.append(f"  >{thresh:.0f}%  {n_ep:>9d}  {n_ctrl:>10d}  {r_ep:>7.2f}  {r_ctrl:>9.2f}  {e_str:>7s}")


def section_h(daily: pd.DataFrame, episodes_2024: list, hourly_oi: pd.DataFrame, out: list):
    """Test H: Corrected lead time using sub-daily lending timestamps + price diagnostic."""
    out.append("\n" + "=" * 60)
    out.append("H. CORRECTED LEAD TIME + PRICE DIAGNOSTIC")
    out.append("=" * 60)

    # Load raw lending events
    print("Loading raw lending events for sub-daily timestamps...")
    raw_events = load_raw_lending_events()

    # Load hourly ETH price for price diagnostic
    price_h = pd.read_csv(DATA_DIR / "eth_price_1h.csv")
    price_h["datetime"] = pd.to_datetime(price_h["datetime"], utc=True).dt.floor("h")
    price_h = price_h.set_index("datetime").sort_index()

    out.append(f"  Raw lending events: {len(raw_events)}")

    rows = []
    out.append(f"\n  {'Start':<12s} {'Peak day':<12s}  {'Lend peak hr':>13s}  {'OI drop hr':>13s}  "
               f"{'Corr lag':>9s}  {'P@OI':>8s}  {'P@Lend':>8s}  {'ΔP':>7s}")
    out.append(f"  {'-'*95}")

    for ep_idx in episodes_2024:
        ep_start = daily.loc[ep_idx[0], "date"]
        peak_idx = daily.loc[ep_idx, "total_usd"].idxmax()
        peak_day = daily.loc[peak_idx, "date"]

        # Find peak lending hour on peak day
        day_start = peak_day
        day_end = peak_day + pd.Timedelta(days=1)
        day_events = raw_events[(raw_events["dt"] >= day_start) & (raw_events["dt"] < day_end)]

        if len(day_events) > 0:
            hourly_vol = day_events.groupby("hour")["volume_usd"].sum()
            lending_peak_hour = hourly_vol.idxmax()
        else:
            lending_peak_hour = peak_day + pd.Timedelta(hours=12)  # fallback to noon

        # Find OI drop (same method as before)
        oi_spike = find_oi_spike(hourly_oi, peak_day)

        if oi_spike is None:
            rows.append({
                "start": str(ep_start.date()), "peak_day": str(peak_day.date()),
                "lending_peak_hour": lending_peak_hour,
                "oi_drop_hour": pd.NaT, "corrected_lag_hours": np.nan,
                "price_at_oi": np.nan, "price_at_lend": np.nan, "price_change_pct": np.nan,
                "fwd_7d": daily.loc[ep_idx[0], "fwd_7d"],
            })
            out.append(f"  {str(ep_start.date()):<12s} {str(peak_day.date()):<12s}  "
                       f"{str(lending_peak_hour)[:13]:>13s}  {'—':>13s}  {'no drop':>9s}  "
                       f"{'—':>8s}  {'—':>8s}  {'—':>7s}")
            continue

        oi_drop_hour = oi_spike["first_drop_time"]
        corr_lag = (lending_peak_hour - oi_drop_hour).total_seconds() / 3600

        # Price at each point
        oi_hour_floor = oi_drop_hour.floor("h")
        lend_hour_floor = lending_peak_hour.floor("h") if hasattr(lending_peak_hour, "floor") else lending_peak_hour

        price_at_oi = price_h.loc[oi_hour_floor, "price"] if oi_hour_floor in price_h.index else np.nan
        price_at_lend = price_h.loc[lend_hour_floor, "price"] if lend_hour_floor in price_h.index else np.nan

        if not np.isnan(price_at_oi) and not np.isnan(price_at_lend) and price_at_oi > 0:
            price_change = (price_at_lend / price_at_oi - 1) * 100
        else:
            price_change = np.nan

        rows.append({
            "start": str(ep_start.date()), "peak_day": str(peak_day.date()),
            "lending_peak_hour": lending_peak_hour,
            "oi_drop_hour": oi_drop_hour, "corrected_lag_hours": corr_lag,
            "price_at_oi": price_at_oi, "price_at_lend": price_at_lend,
            "price_change_pct": price_change,
            "fwd_7d": daily.loc[ep_idx[0], "fwd_7d"],
        })

        p_oi_str = f"${price_at_oi:,.0f}" if not np.isnan(price_at_oi) else "—"
        p_lend_str = f"${price_at_lend:,.0f}" if not np.isnan(price_at_lend) else "—"
        dp_str = f"{price_change:+.1f}%" if not np.isnan(price_change) else "—"

        out.append(f"  {str(ep_start.date()):<12s} {str(peak_day.date()):<12s}  "
                   f"{str(lending_peak_hour)[:13]:>13s}  {str(oi_drop_hour)[:13]:>13s}  "
                   f"{corr_lag:>+8.1f}h  {p_oi_str:>8s}  {p_lend_str:>8s}  {dp_str:>7s}")

    h_df = pd.DataFrame(rows)
    corr_lags = h_df["corrected_lag_hours"].dropna()

    out.append(f"\n  Corrected lead/lag statistics (n={len(corr_lags)}):")
    if len(corr_lags) >= 3:
        out.append(f"    Median corrected lag: {corr_lags.median():+.1f}h")
        out.append(f"    Mean corrected lag: {corr_lags.mean():+.1f}h")
        out.append(f"    Perps lead: {(corr_lags > 0).sum()} / {len(corr_lags)} ({100*(corr_lags > 0).mean():.1f}%)")

    price_changes = h_df["price_change_pct"].dropna()
    if len(price_changes) >= 3:
        out.append(f"\n  Price change (OI drop → lending peak):")
        out.append(f"    Median: {price_changes.median():+.1f}%")
        out.append(f"    Mean: {price_changes.mean():+.1f}%")
        neg_pct = (price_changes < 0).mean() * 100
        out.append(f"    Price declined between OI drop and lending peak: {neg_pct:.0f}% of episodes")

        if price_changes.median() < -1:
            out.append(f"\n    → GENUINE WARNING: price typically fell {abs(price_changes.median()):.1f}% between")
            out.append(f"      OI drop and lending peak. The OI drop fires while further decline is coming.")
        elif abs(price_changes.median()) <= 1:
            out.append(f"\n    → SAME EVENT: price is essentially flat ({price_changes.median():+.1f}%) between")
            out.append(f"      OI drop and lending peak. Faster measurement of the same shock, not a warning.")
        else:
            out.append(f"\n    → LAGGING INDICATOR: price rose {price_changes.median():+.1f}% between OI drop")
            out.append(f"      and lending peak. OI drop fires after the worst is over.")

    return h_df


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

    # Discriminant tests
    section_g(daily, episodes_2024, hourly_oi, out)
    h_df = section_h(daily, episodes_2024, hourly_oi, out)

    # Verdict (updated with discriminant test results)
    out.append("\n" + "=" * 60)
    out.append("VERDICT")
    out.append("=" * 60)

    lags = ep_df["lag_hours"].dropna()
    corr_lags = h_df["corrected_lag_hours"].dropna() if h_df is not None else pd.Series(dtype=float)
    price_changes = h_df["price_change_pct"].dropna() if h_df is not None else pd.Series(dtype=float)

    if len(corr_lags) >= 5:
        pct_lead = (corr_lags > 0).mean() * 100
        med_lag = corr_lags.median()
        med_price = price_changes.median() if len(price_changes) >= 3 else 0
    elif len(lags) >= 5:
        pct_lead = (lags > 0).mean() * 100
        med_lag = lags.median()
        med_price = 0
    else:
        out.append(f"\n  INSUFFICIENT DATA")
        med_lag = 0
        pct_lead = 0
        med_price = 0

    if pct_lead > 65 and med_lag > 6:
        out.append(f"\n  PERPS LEAD: {pct_lead:.0f}% of episodes, corrected median {med_lag:+.1f}h.")
        if med_price < -1:
            out.append(f"  Price typically fell {abs(med_price):.1f}% between OI drop and lending peak.")
            out.append(f"  → GENUINE EARLY WARNING: further decline still coming when OI drop fires.")
        elif abs(med_price) <= 1:
            out.append(f"  Price essentially flat ({med_price:+.1f}%) between OI drop and lending peak.")
            out.append(f"  → FASTER MEASUREMENT of the same shock, not an independent early warning.")
        else:
            out.append(f"  Price rose {med_price:+.1f}% between OI drop and lending peak.")
            out.append(f"  → OI drop fires AFTER the worst of the price decline.")
    elif pct_lead < 35:
        out.append(f"\n  LENDING LEADS or SIMULTANEOUS.")
    else:
        out.append(f"\n  MIXED: {pct_lead:.0f}% perps-first, median {med_lag:+.1f}h.")

    out.append(f"\n  Proxy caveat: OI changes are an imperfect proxy for liquidations.")
    out.append(f"  Direct liquidation data (from Hyperliquid or Coinglass with API key)")
    out.append(f"  would provide higher fidelity.")

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
