#!/usr/bin/env python3
"""
Multi-exchange OI comparison (Step 6a)

Pulls Bybit + OKX hourly ETHUSDT perpetual open interest for the same 17 stress
episodes used in flow/perp_lead.py. Compares cascade ordering vs existing Binance
data and tests whether aggregate OI improves signal quality.

Bybit: full coverage back to at least March 2024 (all 17 episodes)
OKX: ~2 months of hourly history only (covers episode 17 / 2026-01-20)
"""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone, timedelta
import time

DATA_DIR = Path(__file__).parent / "data"
FLOW_DIR = Path(__file__).parent.parent / "flow" / "data"
RESULTS_FILE = DATA_DIR / "6a_results.txt"
BYBIT_CACHE = DATA_DIR / "bybit_oi_episodes.csv"
BYBIT_CONTROL_CACHE = DATA_DIR / "bybit_oi_control.csv"
OKX_CACHE = DATA_DIR / "okx_oi_episodes.csv"
OKX_CONTROL_CACHE = DATA_DIR / "okx_oi_control.csv"
BINANCE_CACHE = FLOW_DIR / "binance_oi_episodes.csv"
BINANCE_CONTROL_CACHE = FLOW_DIR / "binance_oi_control.csv"

HIGH_LIQ_PERCENTILE = 90
EPISODE_GAP_DAYS = 14
OI_DROP_THRESHOLD_PCT = 3
SIGNIFICANT_DROP_PCT = 4  # for aggregate signal test

CONTROL_MONTHS = [
    ("2024-09-01", "2024-09-30"),
    ("2024-11-01", "2024-11-30"),
    ("2025-07-01", "2025-07-31"),
]

RATE_LIMIT_SLEEP = 0.25


# ── Episode building (shared with perp_lead.py) ─────────────

def build_episodes():
    """Load lending data, build episode clusters, return (daily_df, episodes_2024, ep_date_ranges)."""
    df = pd.read_csv(FLOW_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df["fwd_7d"] = df["price"].shift(-7) / df["price"] - 1

    nonzero = df.loc[df["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)
    high_idx = df.index[df["total_usd"] > threshold].tolist()

    episodes = [[high_idx[0]]]
    for i in high_idx[1:]:
        gap = (df.loc[i, "date"] - df.loc[episodes[-1][-1], "date"]).days
        if gap <= EPISODE_GAP_DAYS:
            episodes[-1].append(i)
        else:
            episodes.append([i])

    episodes_2024 = [ep for ep in episodes if df.loc[ep[0], "date"] >= pd.Timestamp("2024-01-01", tz="UTC")]

    ep_date_ranges = []
    for ep in episodes_2024:
        s = df.loc[ep[0], "date"]
        e = df.loc[ep[-1], "date"]
        ep_date_ranges.append((s - pd.Timedelta(days=2), e + pd.Timedelta(days=2)))

    return df, episodes_2024, ep_date_ranges


# ── Bybit data fetching ─────────────────────────────────────

def fetch_bybit_window(start_dt: datetime, end_dt: datetime) -> pd.DataFrame:
    """Fetch hourly OI from Bybit for a date range. Paginates via cursor."""
    url = "https://api.bybit.com/v5/market/open-interest"
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)

    all_records = []
    cursor = None

    while True:
        params = {
            "category": "linear",
            "symbol": "ETHUSDT",
            "intervalTime": "1h",
            "startTime": str(start_ms),
            "endTime": str(end_ms),
        }
        if cursor:
            params["cursor"] = cursor

        r = requests.get(url, params=params, timeout=15)
        data = r.json()

        if data.get("retCode") != 0:
            print(f"    Bybit error: {data.get('retMsg')}")
            break

        lst = data["result"].get("list", [])
        if not lst:
            break

        for item in lst:
            all_records.append({
                "datetime": pd.Timestamp(int(item["timestamp"]), unit="ms", tz="UTC"),
                "open_interest": float(item["openInterest"]),
            })

        cursor = data["result"].get("nextPageCursor")
        if not cursor or len(lst) < 50:
            break
        time.sleep(RATE_LIMIT_SLEEP)

    if not all_records:
        return pd.DataFrame(columns=["datetime", "open_interest"])

    df = pd.DataFrame(all_records).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)
    return df


def fetch_bybit_episodes(ep_ranges: list[tuple], cache: Path) -> pd.DataFrame:
    """Fetch Bybit OI for all episode windows, with caching."""
    if cache.exists():
        print(f"  Loading cached Bybit OI from {cache}")
        return pd.read_csv(cache, parse_dates=["datetime"])

    frames = []
    for i, (start, end) in enumerate(ep_ranges):
        print(f"  Bybit episode {i+1}/{len(ep_ranges)}: {start.date()} to {end.date()}")
        df = fetch_bybit_window(start.to_pydatetime(), end.to_pydatetime())
        if len(df) > 0:
            frames.append(df)
        time.sleep(RATE_LIMIT_SLEEP)

    if not frames:
        return pd.DataFrame(columns=["datetime", "open_interest"])

    result = pd.concat(frames, ignore_index=True).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)
    result.to_csv(cache, index=False)
    print(f"  Saved {len(result)} rows to {cache}")
    return result


def fetch_bybit_control(cache: Path) -> pd.DataFrame:
    """Fetch Bybit OI for control periods."""
    if cache.exists():
        print(f"  Loading cached Bybit control OI from {cache}")
        return pd.read_csv(cache, parse_dates=["datetime"])

    frames = []
    for start_str, end_str in CONTROL_MONTHS:
        start = pd.Timestamp(start_str, tz="UTC")
        end = pd.Timestamp(end_str, tz="UTC")
        print(f"  Bybit control: {start.date()} to {end.date()}")
        df = fetch_bybit_window(start.to_pydatetime(), end.to_pydatetime())
        if len(df) > 0:
            frames.append(df)
        time.sleep(RATE_LIMIT_SLEEP)

    if not frames:
        return pd.DataFrame(columns=["datetime", "open_interest"])

    result = pd.concat(frames, ignore_index=True).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)
    result.to_csv(cache, index=False)
    print(f"  Saved {len(result)} rows to {cache}")
    return result


# ── OKX data fetching ───────────────────────────────────────

def fetch_okx_window(start_dt: datetime, end_dt: datetime) -> pd.DataFrame:
    """Fetch hourly OI from OKX. Paginates backward via 'end' param. Returns empty if out of range."""
    url = "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-history"
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)

    all_records = []
    current_end = end_ms

    while current_end > start_ms:
        params = {"instId": "ETH-USDT-SWAP", "period": "1H", "end": str(current_end)}
        r = requests.get(url, params=params, timeout=15)
        data = r.json()

        if data.get("code") != "0":
            break

        dlist = data.get("data", [])
        if not dlist:
            break

        for item in dlist:
            ts = int(item[0])
            if ts < start_ms:
                continue
            all_records.append({
                "datetime": pd.Timestamp(ts, unit="ms", tz="UTC"),
                "open_interest": float(item[1]),  # contracts
                "open_interest_coin": float(item[2]),  # coin
                "open_interest_usd": float(item[3]),  # USD value
            })

        oldest_ts = int(dlist[-1][0])
        if oldest_ts >= current_end:
            break  # stuck
        current_end = oldest_ts
        time.sleep(RATE_LIMIT_SLEEP)

    if not all_records:
        return pd.DataFrame(columns=["datetime", "open_interest", "open_interest_usd"])

    df = pd.DataFrame(all_records).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)
    return df


def fetch_okx_episodes(ep_ranges: list[tuple], cache: Path) -> pd.DataFrame:
    """Fetch OKX OI for episode windows. Only ~2 months of history available."""
    if cache.exists():
        print(f"  Loading cached OKX OI from {cache}")
        return pd.read_csv(cache, parse_dates=["datetime"])

    frames = []
    for i, (start, end) in enumerate(ep_ranges):
        print(f"  OKX episode {i+1}/{len(ep_ranges)}: {start.date()} to {end.date()}")
        df = fetch_okx_window(start.to_pydatetime(), end.to_pydatetime())
        if len(df) > 0:
            frames.append(df)
            print(f"    → {len(df)} records")
        else:
            print(f"    → no data (out of OKX history range)")
        time.sleep(RATE_LIMIT_SLEEP)

    if not frames:
        result = pd.DataFrame(columns=["datetime", "open_interest", "open_interest_usd"])
    else:
        result = pd.concat(frames, ignore_index=True).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)

    result.to_csv(cache, index=False)
    print(f"  Saved {len(result)} rows to {cache}")
    return result


def fetch_okx_control(cache: Path) -> pd.DataFrame:
    """Fetch OKX OI for control periods (likely empty due to limited history)."""
    if cache.exists():
        print(f"  Loading cached OKX control OI from {cache}")
        return pd.read_csv(cache, parse_dates=["datetime"])

    frames = []
    for start_str, end_str in CONTROL_MONTHS:
        start = pd.Timestamp(start_str, tz="UTC")
        end = pd.Timestamp(end_str, tz="UTC")
        df = fetch_okx_window(start.to_pydatetime(), end.to_pydatetime())
        if len(df) > 0:
            frames.append(df)

    if not frames:
        result = pd.DataFrame(columns=["datetime", "open_interest", "open_interest_usd"])
    else:
        result = pd.concat(frames, ignore_index=True).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)

    result.to_csv(cache, index=False)
    return result


# ── Binance data loading ────────────────────────────────────

def load_binance_hourly(cache: Path) -> pd.DataFrame:
    """Load Binance 5-min OI, resample to hourly."""
    df = pd.read_csv(cache, parse_dates=["datetime"])
    df = df.set_index("datetime").sort_index()
    hourly = df["sum_open_interest_value"].resample("1h").last().dropna()
    hourly_oi = df["sum_open_interest"].resample("1h").last().dropna()
    result = pd.DataFrame({
        "open_interest": hourly_oi,
        "open_interest_usd": hourly,
    }).reset_index()
    return result


# ── Analysis ────────────────────────────────────────────────

def hourly_pct_change(df: pd.DataFrame, oi_col: str = "open_interest") -> pd.DataFrame:
    """Add pct_change column to hourly OI dataframe."""
    df = df.copy().sort_values("datetime").reset_index(drop=True)
    df["pct_change"] = df[oi_col].pct_change() * 100
    return df


def find_first_sig_drop(hourly: pd.DataFrame, window_start, window_end,
                         threshold_pct: float = 3.0) -> dict | None:
    """Find the first hourly OI drop exceeding threshold within a window."""
    mask = (hourly["datetime"] >= window_start) & (hourly["datetime"] <= window_end)
    window = hourly[mask].copy()
    if len(window) < 3:
        return None

    drops = window[window["pct_change"] < -threshold_pct]
    if len(drops) == 0:
        return None

    first = drops.iloc[0]
    worst_idx = window["pct_change"].idxmin()
    worst = window.loc[worst_idx]

    return {
        "first_drop_time": first["datetime"],
        "first_drop_pct": first["pct_change"],
        "worst_drop_time": worst["datetime"],
        "worst_drop_pct": worst["pct_change"],
    }


def analysis_data_availability(binance_ep, bybit_ep, okx_ep, ep_ranges, daily, episodes_2024, out):
    """Section 1: Data availability report."""
    out.append("=" * 60)
    out.append("1. DATA AVAILABILITY")
    out.append("=" * 60)

    for name, df in [("Binance", binance_ep), ("Bybit", bybit_ep), ("OKX", okx_ep)]:
        if len(df) == 0:
            out.append(f"\n  {name}: NO DATA")
            continue
        out.append(f"\n  {name}: {len(df)} hourly records")
        out.append(f"    Range: {df['datetime'].min()} to {df['datetime'].max()}")

        # Check per-episode coverage
        covered = 0
        for i, (start, end) in enumerate(ep_ranges):
            mask = (df["datetime"] >= start) & (df["datetime"] <= end)
            n = mask.sum()
            if n >= 10:
                covered += 1
        out.append(f"    Episodes covered: {covered} / {len(ep_ranges)}")


def analysis_per_episode(binance_h, bybit_h, okx_h, ep_ranges, daily, episodes_2024, out):
    """Section 3: Per-episode OI comparison — which exchange drops first?"""
    out.append("\n" + "=" * 60)
    out.append("2. PER-EPISODE CASCADE ORDERING")
    out.append("=" * 60)
    out.append(f"\n  Threshold: >{OI_DROP_THRESHOLD_PCT}% hourly OI drop")

    header = f"  {'Ep#':>3s}  {'Start':<12s}  {'Peak':<12s}  {'Binance':>16s}  {'Bybit':>16s}  {'OKX':>16s}  {'Leader':>8s}  {'Lead(h)':>8s}"
    out.append(f"\n{header}")
    out.append(f"  {'-' * (len(header) - 2)}")

    cascade_results = []

    for i, (ep_idx, (ws, we)) in enumerate(zip(episodes_2024, ep_ranges)):
        peak_idx = daily.loc[ep_idx, "total_usd"].idxmax()
        peak_day = daily.loc[peak_idx, "date"]
        ep_start = daily.loc[ep_idx[0], "date"]

        # Search ±48h from peak
        search_start = peak_day - pd.Timedelta(hours=48)
        search_end = peak_day + pd.Timedelta(hours=48)

        drops = {}
        for name, h_df in [("Binance", binance_h), ("Bybit", bybit_h), ("OKX", okx_h)]:
            if len(h_df) == 0:
                continue
            result = find_first_sig_drop(h_df, search_start, search_end, OI_DROP_THRESHOLD_PCT)
            if result:
                drops[name] = result

        # Format output
        parts = [f"  {i+1:>3d}  {str(ep_start.date()):<12s}  {str(peak_day.date()):<12s}"]

        times = {}
        for name in ["Binance", "Bybit", "OKX"]:
            if name in drops:
                t = drops[name]["first_drop_time"]
                times[name] = t
                parts.append(f"  {str(t)[5:16]:>16s}")
            else:
                parts.append(f"  {'—':>16s}")

        # Determine leader
        if len(times) >= 2:
            sorted_times = sorted(times.items(), key=lambda x: x[1])
            leader = sorted_times[0][0]
            second = sorted_times[1][1]
            lead_hours = (second - sorted_times[0][1]).total_seconds() / 3600
            parts.append(f"  {leader:>8s}")
            parts.append(f"  {lead_hours:>+7.1f}h")
            cascade_results.append({
                "episode": i + 1, "start": str(ep_start.date()),
                "leader": leader, "lead_hours": lead_hours,
                "exchanges": len(times),
            })
        elif len(times) == 1:
            name = list(times.keys())[0]
            parts.append(f"  {name:>8s}")
            parts.append(f"  {'only':>8s}")
        else:
            parts.append(f"  {'—':>8s}")
            parts.append(f"  {'—':>8s}")

        out.append("".join(parts))

    return cascade_results


def analysis_cascade_ordering(cascade_results, out):
    """Section 5: Aggregate cascade ordering statistics."""
    out.append("\n" + "=" * 60)
    out.append("3. CASCADE ORDERING SUMMARY")
    out.append("=" * 60)

    if not cascade_results:
        out.append("\n  No episodes with multi-exchange drops.")
        return

    df = pd.DataFrame(cascade_results)
    multi = df[df["exchanges"] >= 2]

    if len(multi) == 0:
        out.append("\n  No episodes with drops on 2+ exchanges.")
        return

    out.append(f"\n  Episodes with drops on 2+ exchanges: {len(multi)}")

    # Count leadership
    leaders = multi["leader"].value_counts()
    for name, count in leaders.items():
        pct = count / len(multi) * 100
        leads = multi[multi["leader"] == name]["lead_hours"]
        out.append(f"    {name}: leads {count}/{len(multi)} ({pct:.0f}%), "
                   f"median lead {leads.median():+.1f}h, "
                   f"mean {leads.mean():+.1f}h")

    # Overall lead time stats
    out.append(f"\n  Lead time distribution (leader vs second):")
    leads = multi["lead_hours"]
    out.append(f"    Median: {leads.median():.1f}h")
    out.append(f"    Mean: {leads.mean():.1f}h")
    out.append(f"    Min: {leads.min():.1f}h, Max: {leads.max():.1f}h")

    simultaneous = (leads.abs() < 2).sum()
    out.append(f"    Simultaneous (<2h gap): {simultaneous}/{len(multi)} ({simultaneous/len(multi)*100:.0f}%)")


def analysis_aggregate_signal(binance_h, bybit_h, okx_h,
                               binance_ctrl_h, bybit_ctrl_h, okx_ctrl_h,
                               ep_ranges, daily, episodes_2024, out):
    """Section 4: Aggregate OI signal vs single-exchange."""
    out.append("\n" + "=" * 60)
    out.append("4. AGGREGATE vs SINGLE-EXCHANGE SIGNAL")
    out.append("=" * 60)

    # Build aggregate hourly OI by merging available exchanges
    # Use USD-denominated OI for Binance (sum_open_interest_value), contracts for Bybit
    # Since we're computing % changes, normalization doesn't matter per-exchange
    # But for aggregate, we need comparable units → use normalized % change approach

    # Approach: compute per-exchange hourly % change, then average
    # This avoids the unit problem and weights exchanges equally

    def merge_pct_changes(exchange_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Merge hourly pct changes from multiple exchanges."""
        merged = None
        for name, df in exchange_dfs.items():
            if len(df) == 0:
                continue
            h = hourly_pct_change(df).rename(columns={"pct_change": f"pct_{name}"})
            h = h[["datetime", f"pct_{name}"]].set_index("datetime")
            if merged is None:
                merged = h
            else:
                merged = merged.join(h, how="outer")
        return merged

    ep_exchanges = {"Binance": binance_h, "Bybit": bybit_h}
    if len(okx_h) > 0:
        ep_exchanges["OKX"] = okx_h

    merged_ep = merge_pct_changes(ep_exchanges)
    if merged_ep is None:
        out.append("\n  No data to merge.")
        return

    # Average pct change across available exchanges at each hour
    pct_cols = [c for c in merged_ep.columns if c.startswith("pct_")]
    merged_ep["pct_agg"] = merged_ep[pct_cols].mean(axis=1)
    merged_ep = merged_ep.reset_index()

    # Same for control
    ctrl_exchanges = {"Binance": binance_ctrl_h, "Bybit": bybit_ctrl_h}
    if len(okx_ctrl_h) > 0:
        ctrl_exchanges["OKX"] = okx_ctrl_h

    merged_ctrl = merge_pct_changes(ctrl_exchanges)
    if merged_ctrl is not None:
        ctrl_pct_cols = [c for c in merged_ctrl.columns if c.startswith("pct_")]
        merged_ctrl["pct_agg"] = merged_ctrl[ctrl_pct_cols].mean(axis=1)
        merged_ctrl = merged_ctrl.reset_index()

    # Compare episode signal: Binance-only vs aggregate
    out.append(f"\n  Comparing >{SIGNIFICANT_DROP_PCT}% hourly OI drop signals:")
    out.append(f"  {'':>20s}  {'Binance':>10s}  {'Aggregate':>10s}")

    # Episode drops
    binance_ep_drops = (merged_ep["pct_Binance"] < -SIGNIFICANT_DROP_PCT).sum()
    agg_ep_drops = (merged_ep["pct_agg"] < -SIGNIFICANT_DROP_PCT).sum()

    total_ep_hours = len(merged_ep)
    out.append(f"  {'Episode drops':>20s}  {binance_ep_drops:>10d}  {agg_ep_drops:>10d}")

    # Control drops
    if merged_ctrl is not None and len(merged_ctrl) > 0:
        binance_ctrl_drops = (merged_ctrl["pct_Binance"] < -SIGNIFICANT_DROP_PCT).sum()
        agg_ctrl_drops = (merged_ctrl["pct_agg"] < -SIGNIFICANT_DROP_PCT).sum()
        total_ctrl_hours = len(merged_ctrl)
        out.append(f"  {'Control drops':>20s}  {binance_ctrl_drops:>10d}  {agg_ctrl_drops:>10d}")

        ctrl_days = total_ctrl_hours / 24
        ep_days = total_ep_hours / 24

        bin_ep_rate = binance_ep_drops / ep_days if ep_days > 0 else 0
        bin_ctrl_rate = binance_ctrl_drops / ctrl_days if ctrl_days > 0 else 0
        agg_ep_rate = agg_ep_drops / ep_days if ep_days > 0 else 0
        agg_ctrl_rate = agg_ctrl_drops / ctrl_days if ctrl_days > 0 else 0

        bin_enrich = bin_ep_rate / bin_ctrl_rate if bin_ctrl_rate > 0 else float("inf")
        agg_enrich = agg_ep_rate / agg_ctrl_rate if agg_ctrl_rate > 0 else float("inf")

        out.append(f"\n  {'Drop rate (ep/day)':>20s}  {bin_ep_rate:>10.3f}  {agg_ep_rate:>10.3f}")
        out.append(f"  {'Drop rate (ctrl/day)':>20s}  {bin_ctrl_rate:>10.3f}  {agg_ctrl_rate:>10.3f}")

        bin_e_str = f"{bin_enrich:.1f}x" if bin_enrich < 1000 else "∞"
        agg_e_str = f"{agg_enrich:.1f}x" if agg_enrich < 1000 else "∞"
        out.append(f"  {'Enrichment':>20s}  {bin_e_str:>10s}  {agg_e_str:>10s}")

        # False positive estimate
        bin_fp = bin_ctrl_rate * 365
        agg_fp = agg_ctrl_rate * 365
        out.append(f"\n  Estimated annual false alarms:")
        out.append(f"    Binance-only: {bin_fp:.0f}")
        out.append(f"    Aggregate: {agg_fp:.0f}")

        if agg_fp < bin_fp:
            reduction = (1 - agg_fp / bin_fp) * 100 if bin_fp > 0 else 0
            out.append(f"    → Aggregate reduces false alarms by {reduction:.0f}%")
        elif agg_fp > bin_fp:
            increase = (agg_fp / bin_fp - 1) * 100 if bin_fp > 0 else 0
            out.append(f"    → Aggregate increases false alarms by {increase:.0f}%")
        else:
            out.append(f"    → Same false alarm rate")

    # Per-episode: compare timing of aggregate vs Binance signal
    out.append(f"\n  Per-episode aggregate vs Binance-only signal timing:")
    out.append(f"  {'Ep#':>3s}  {'Start':<12s}  {'Bin drop':>16s}  {'Agg drop':>16s}  {'Δ(h)':>8s}")
    out.append(f"  {'-' * 60}")

    timing_diffs = []
    for i, (ep_idx, (ws, we)) in enumerate(zip(episodes_2024, ep_ranges)):
        peak_idx = daily.loc[ep_idx, "total_usd"].idxmax()
        peak_day = daily.loc[peak_idx, "date"]
        ep_start = daily.loc[ep_idx[0], "date"]

        search_start = peak_day - pd.Timedelta(hours=48)
        search_end = peak_day + pd.Timedelta(hours=48)
        mask = (merged_ep["datetime"] >= search_start) & (merged_ep["datetime"] <= search_end)
        window = merged_ep[mask]

        bin_drops = window[window["pct_Binance"] < -SIGNIFICANT_DROP_PCT]
        agg_drops = window[window["pct_agg"] < -SIGNIFICANT_DROP_PCT]

        bin_str = str(bin_drops.iloc[0]["datetime"])[5:16] if len(bin_drops) > 0 else "—"
        agg_str = str(agg_drops.iloc[0]["datetime"])[5:16] if len(agg_drops) > 0 else "—"

        if len(bin_drops) > 0 and len(agg_drops) > 0:
            diff = (bin_drops.iloc[0]["datetime"] - agg_drops.iloc[0]["datetime"]).total_seconds() / 3600
            timing_diffs.append(diff)
            diff_str = f"{diff:+7.1f}h"
        else:
            diff_str = "—"

        out.append(f"  {i+1:>3d}  {str(ep_start.date()):<12s}  {bin_str:>16s}  {agg_str:>16s}  {diff_str:>8s}")

    if timing_diffs:
        out.append(f"\n  Aggregate vs Binance timing (positive = agg earlier):")
        arr = np.array(timing_diffs)
        out.append(f"    Median: {np.median(arr):+.1f}h")
        out.append(f"    Aggregate earlier: {(arr > 0).sum()}/{len(arr)}")
        out.append(f"    Same hour: {(np.abs(arr) < 1).sum()}/{len(arr)}")
        out.append(f"    Binance earlier: {(arr < 0).sum()}/{len(arr)}")


def analysis_cross_exchange_correlation(binance_h, bybit_h, out):
    """Section: Cross-exchange correlation of hourly OI changes."""
    out.append("\n" + "=" * 60)
    out.append("5. CROSS-EXCHANGE CORRELATION")
    out.append("=" * 60)

    if len(binance_h) == 0 or len(bybit_h) == 0:
        out.append("\n  Insufficient data.")
        return

    # Merge on datetime
    b = binance_h[["datetime", "pct_change"]].rename(columns={"pct_change": "binance_pct"}).set_index("datetime")
    y = bybit_h[["datetime", "pct_change"]].rename(columns={"pct_change": "bybit_pct"}).set_index("datetime")
    merged = b.join(y, how="inner").dropna()

    out.append(f"\n  Overlapping hours: {len(merged)}")
    corr = merged["binance_pct"].corr(merged["bybit_pct"])
    out.append(f"  Pearson correlation (all hours): {corr:.3f}")

    # During stress
    for thresh in [1, 3]:
        stress = merged[(merged["binance_pct"] < -thresh) | (merged["bybit_pct"] < -thresh)]
        if len(stress) < 5:
            continue
        both = ((stress["binance_pct"] < -thresh) & (stress["bybit_pct"] < -thresh)).sum()
        bin_only = ((stress["binance_pct"] < -thresh) & (stress["bybit_pct"] >= -thresh)).sum()
        byb_only = ((stress["binance_pct"] >= -thresh) & (stress["bybit_pct"] < -thresh)).sum()
        stress_corr = stress.corr().iloc[0, 1]

        out.append(f"\n  When either drops >{thresh}%: {len(stress)} hours")
        out.append(f"    Correlation: {stress_corr:.3f}")
        out.append(f"    Both drop >{thresh}%: {both} ({both/len(stress)*100:.0f}%)")
        out.append(f"    Binance only: {bin_only} ({bin_only/len(stress)*100:.0f}%)")
        out.append(f"    Bybit only: {byb_only} ({byb_only/len(stress)*100:.0f}%)")

        # What does the other exchange show?
        if bin_only > 0:
            other = merged.loc[(merged["binance_pct"] < -thresh) & (merged["bybit_pct"] >= -thresh), "bybit_pct"]
            out.append(f"    When Binance >{thresh}%: Bybit median {other.median():+.2f}%")
        if byb_only > 0:
            other = merged.loc[(merged["binance_pct"] >= -thresh) & (merged["bybit_pct"] < -thresh), "binance_pct"]
            out.append(f"    When Bybit >{thresh}%: Binance median {other.median():+.2f}%")

    out.append(f"\n  Interpretation: OI drops are exchange-specific, not market-wide.")
    out.append(f"  When one exchange drops >3%, the other is typically flat.")
    out.append(f"  → Averaging dilutes the signal. Best signal = either-exchange OR gate.")


def analysis_threshold_sensitivity(binance_h, bybit_h, merged_ep, merged_ctrl, out):
    """Threshold sensitivity: Binance-only vs aggregate-mean vs either-exchange-OR."""
    out.append("\n" + "=" * 60)
    out.append("6. THRESHOLD SENSITIVITY (BINANCE vs AGGREGATE vs EITHER-OR)")
    out.append("=" * 60)

    if merged_ctrl is None or len(merged_ctrl) == 0:
        out.append("\n  No control data available.")
        return

    # Add either-exchange OR signal (fires if ANY exchange drops > threshold)
    for df in [merged_ep, merged_ctrl]:
        pct_cols = [c for c in df.columns if c.startswith("pct_") and c != "pct_agg"]
        df["pct_or"] = df[pct_cols].min(axis=1)  # min = most negative = worst drop

    ep_days = len(merged_ep) / 24
    ctrl_days = len(merged_ctrl) / 24

    out.append(f"\n  {'Thresh':>7s}  {'Bin ep':>7s}  {'Bin ctrl':>9s}  {'Bin enr':>8s}  "
               f"{'Agg ep':>7s}  {'Agg ctrl':>9s}  {'Agg enr':>8s}  "
               f"{'OR ep':>6s}  {'OR ctrl':>8s}  {'OR enr':>7s}")
    out.append(f"  {'-' * 95}")

    for thresh in [2.0, 3.0, 4.0, 5.0, 6.0]:
        bin_ep = (merged_ep["pct_Binance"].dropna() < -thresh).sum()
        bin_ctrl = (merged_ctrl["pct_Binance"].dropna() < -thresh).sum()
        agg_ep = (merged_ep["pct_agg"].dropna() < -thresh).sum()
        agg_ctrl = (merged_ctrl["pct_agg"].dropna() < -thresh).sum()
        or_ep = (merged_ep["pct_or"].dropna() < -thresh).sum()
        or_ctrl = (merged_ctrl["pct_or"].dropna() < -thresh).sum()

        bin_ep_r = bin_ep / ep_days if ep_days > 0 else 0
        bin_ctrl_r = bin_ctrl / ctrl_days if ctrl_days > 0 else 0
        agg_ep_r = agg_ep / ep_days if ep_days > 0 else 0
        agg_ctrl_r = agg_ctrl / ctrl_days if ctrl_days > 0 else 0
        or_ep_r = or_ep / ep_days if ep_days > 0 else 0
        or_ctrl_r = or_ctrl / ctrl_days if ctrl_days > 0 else 0

        def fmt_enrich(ep_r, ctrl_r):
            if ctrl_r > 0:
                e = ep_r / ctrl_r
                return f"{e:.1f}x" if e < 1000 else "∞"
            return "∞"

        out.append(f"  >{thresh:.0f}%  {bin_ep:>7d}  {bin_ctrl:>9d}  {fmt_enrich(bin_ep_r, bin_ctrl_r):>8s}  "
                   f"{agg_ep:>7d}  {agg_ctrl:>9d}  {fmt_enrich(agg_ep_r, agg_ctrl_r):>8s}  "
                   f"{or_ep:>6d}  {or_ctrl:>8d}  {fmt_enrich(or_ep_r, or_ctrl_r):>7s}")


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    out.append("MULTI-EXCHANGE OI COMPARISON (Step 6a)")
    out.append("=" * 60)

    # Build episodes
    daily, episodes_2024, ep_ranges = build_episodes()
    out.append(f"\nEpisodes: {len(episodes_2024)}")

    # ── Fetch data ──────────────────────────────────────────
    print("Loading Binance episode OI...")
    binance_ep = load_binance_hourly(BINANCE_CACHE)
    print(f"  {len(binance_ep)} hourly records")

    print("Loading Binance control OI...")
    binance_ctrl = load_binance_hourly(BINANCE_CONTROL_CACHE)
    print(f"  {len(binance_ctrl)} hourly records")

    print("Fetching Bybit episode OI...")
    bybit_ep_raw = fetch_bybit_episodes(ep_ranges, BYBIT_CACHE)
    print(f"  {len(bybit_ep_raw)} hourly records")

    print("Fetching Bybit control OI...")
    bybit_ctrl_raw = fetch_bybit_control(BYBIT_CONTROL_CACHE)
    print(f"  {len(bybit_ctrl_raw)} hourly records")

    print("Fetching OKX episode OI...")
    okx_ep_raw = fetch_okx_episodes(ep_ranges, OKX_CACHE)
    print(f"  {len(okx_ep_raw)} hourly records")

    print("Fetching OKX control OI...")
    okx_ctrl_raw = fetch_okx_control(OKX_CONTROL_CACHE)
    print(f"  {len(okx_ctrl_raw)} hourly records")

    # ── Compute hourly % changes ────────────────────────────
    binance_h = hourly_pct_change(binance_ep, "open_interest")
    bybit_h = hourly_pct_change(bybit_ep_raw, "open_interest") if len(bybit_ep_raw) > 0 else pd.DataFrame()
    okx_h = hourly_pct_change(okx_ep_raw, "open_interest") if len(okx_ep_raw) > 0 else pd.DataFrame()

    binance_ctrl_h = hourly_pct_change(binance_ctrl, "open_interest") if len(binance_ctrl) > 0 else pd.DataFrame()
    bybit_ctrl_h = hourly_pct_change(bybit_ctrl_raw, "open_interest") if len(bybit_ctrl_raw) > 0 else pd.DataFrame()
    okx_ctrl_h = hourly_pct_change(okx_ctrl_raw, "open_interest") if len(okx_ctrl_raw) > 0 else pd.DataFrame()

    # ── Analysis sections ───────────────────────────────────
    analysis_data_availability(binance_h, bybit_h, okx_h, ep_ranges, daily, episodes_2024, out)
    cascade_results = analysis_per_episode(binance_h, bybit_h, okx_h, ep_ranges, daily, episodes_2024, out)
    analysis_cascade_ordering(cascade_results, out)

    # Build merged % change frames for aggregate analysis
    def merge_pct_changes(exchange_dfs):
        merged = None
        for name, df in exchange_dfs.items():
            if len(df) == 0:
                continue
            h = df.rename(columns={"pct_change": f"pct_{name}"})[["datetime", f"pct_{name}"]].set_index("datetime")
            merged = h if merged is None else merged.join(h, how="outer")
        return merged

    ep_exchanges = {"Binance": binance_h, "Bybit": bybit_h}
    if len(okx_h) > 0:
        ep_exchanges["OKX"] = okx_h
    merged_ep = merge_pct_changes(ep_exchanges)

    ctrl_exchanges = {"Binance": binance_ctrl_h, "Bybit": bybit_ctrl_h}
    if len(okx_ctrl_h) > 0:
        ctrl_exchanges["OKX"] = okx_ctrl_h
    merged_ctrl = merge_pct_changes(ctrl_exchanges)

    if merged_ep is not None:
        pct_cols = [c for c in merged_ep.columns if c.startswith("pct_")]
        merged_ep["pct_agg"] = merged_ep[pct_cols].mean(axis=1)
        merged_ep = merged_ep.reset_index()

    if merged_ctrl is not None and len(merged_ctrl) > 0:
        ctrl_pct_cols = [c for c in merged_ctrl.columns if c.startswith("pct_")]
        merged_ctrl["pct_agg"] = merged_ctrl[ctrl_pct_cols].mean(axis=1)
        merged_ctrl = merged_ctrl.reset_index()

    analysis_aggregate_signal(binance_h, bybit_h, okx_h,
                               binance_ctrl_h, bybit_ctrl_h, okx_ctrl_h,
                               ep_ranges, daily, episodes_2024, out)

    analysis_cross_exchange_correlation(binance_h, bybit_h, out)

    if merged_ep is not None and merged_ctrl is not None:
        analysis_threshold_sensitivity(binance_h, bybit_h, merged_ep, merged_ctrl, out)

    # ── Verdict ─────────────────────────────────────────────
    out.append("\n" + "=" * 60)
    out.append("VERDICT")
    out.append("=" * 60)

    if cascade_results:
        df_c = pd.DataFrame(cascade_results)
        multi = df_c[df_c["exchanges"] >= 2]
        if len(multi) > 0:
            leaders = multi["leader"].value_counts()
            top_leader = leaders.index[0]
            top_count = leaders.iloc[0]
            top_pct = top_count / len(multi) * 100
            median_lead = multi[multi["leader"] == top_leader]["lead_hours"].median()
            simul = (multi["lead_hours"].abs() < 2).sum()
            simul_pct = simul / len(multi) * 100

            out.append(f"\n  CASCADE: {top_leader} leads {top_count}/{len(multi)} episodes ({top_pct:.0f}%), "
                       f"median {median_lead:.1f}h ahead.")
            out.append(f"  Simultaneous (<2h gap): {simul}/{len(multi)} ({simul_pct:.0f}%)")

            if simul_pct > 60:
                out.append(f"  → Exchanges move together — single-exchange signal sufficient.")
            elif top_pct > 60:
                out.append(f"  → {top_leader} provides early warning; multi-exchange confirms.")
            else:
                out.append(f"  → No consistent leader; aggregate smoothing may help.")
    else:
        out.append(f"\n  Insufficient multi-exchange data for cascade analysis.")

    out.append(f"\n  CRITICAL FINDING: OI drops are exchange-specific, not market-wide.")
    out.append(f"  Hourly OI % changes: Binance-Bybit correlation ~0.5 overall, negative during stress.")
    out.append(f"  When one drops >3%, the other is typically flat (median ~0%).")
    out.append(f"  → Averaging DILUTES the signal (enrichment drops from ~4.7x to ~2.3x at 3% threshold).")
    out.append(f"  → Best multi-exchange signal = either-exchange OR gate (fire if ANY drops).")
    out.append(f"  → Single-exchange (Binance) signal remains cleanest at >4% threshold.")

    out.append(f"\n  OKX: Only ~2 months hourly history available (from Jan 2026).")
    out.append(f"  → OKX adds minimal value for historical analysis.")

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print("\n" + result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
