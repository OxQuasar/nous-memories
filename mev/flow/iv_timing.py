#!/usr/bin/env python3
"""
Options IV Timing Probe — Deribit DVOL Around Liquidation Episodes

Tests whether implied volatility (Deribit ETH DVOL index) provides
timing information relative to concentrated spikes and OI drops.

Data source: Deribit public API (no auth).
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from datetime import datetime, timezone
import requests
import sys
import time

DATA_DIR = Path(__file__).parent / "data"
IV_CSV = DATA_DIR / "eth_iv_history.csv"
RESULTS_FILE = DATA_DIR / "iv_timing_results.txt"

HIGH_LIQ_PERCENTILE = 90
CONC_PERCENTILE = 97
FORWARD_HORIZON = 7
EPISODE_GAP_DAYS = 14

DERIBIT_URL = "https://www.deribit.com/api/v2/public/get_volatility_index_data"
CHUNK_DAYS = 950  # stay under 1000 row limit for daily resolution


# ── Data fetching ─────────────────────────────────────────────

def fetch_dvol() -> pd.DataFrame:
    """Fetch daily ETH DVOL from Deribit, chunked to respect 1000-row limit."""
    if IV_CSV.exists():
        df = pd.read_csv(IV_CSV)
        df["date"] = pd.to_datetime(df["date"])
        print(f"Loaded cached IV data: {len(df)} rows")
        return df

    print("Fetching ETH DVOL from Deribit...")
    all_rows = []

    start = datetime(2022, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 3, 19, tzinfo=timezone.utc)

    cursor = start
    while cursor < end:
        chunk_end = min(cursor + pd.Timedelta(days=CHUNK_DAYS), end)
        start_ms = int(cursor.timestamp() * 1000)
        end_ms = int(chunk_end.timestamp() * 1000)

        r = requests.get(DERIBIT_URL, params={
            "currency": "ETH",
            "start_timestamp": start_ms,
            "end_timestamp": end_ms,
            "resolution": 86400,
        }, timeout=30)

        if r.status_code != 200:
            print(f"Deribit API error: {r.status_code} {r.text[:500]}")
            sys.exit(1)

        data = r.json()
        if "error" in data:
            print(f"Deribit error: {data['error']}")
            sys.exit(1)

        rows = data["result"]["data"]
        all_rows.extend(rows)
        print(f"  Chunk {cursor.date()} → {chunk_end.date()}: {len(rows)} rows")

        cursor = chunk_end + pd.Timedelta(days=1)
        time.sleep(0.5)  # rate limit courtesy

    # Rows: [timestamp_ms, open, high, low, close]
    records = []
    for row in all_rows:
        ts = pd.Timestamp(row[0], unit="ms", tz="UTC").normalize()
        records.append({
            "date": ts,
            "dvol_open": row[1],
            "dvol_high": row[2],
            "dvol_low": row[3],
            "dvol_close": row[4],
        })

    df = pd.DataFrame(records).drop_duplicates(subset="date").sort_values("date").reset_index(drop=True)
    df["date"] = df["date"].dt.tz_localize(None)
    df.to_csv(IV_CSV, index=False)
    print(f"Saved {len(df)} daily DVOL rows to {IV_CSV}")
    return df


# ── Shared classification logic ───────────────────────────────

def load_liquidations() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["price"].shift(-FORWARD_HORIZON) / df["price"] - 1
    return df


def classify_m1p97(df: pd.DataFrame) -> pd.Series:
    nonzero = df.loc[df["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)
    is_high = df["total_usd"] > threshold

    vol = df["total_usd"].values
    n = len(vol)
    pctl = np.full(n, np.nan)
    for i in range(n):
        start = max(0, i - 179)
        window = vol[start:i + 1]
        nz = window[window > 0]
        if len(nz) >= 10:
            pctl[i] = stats.percentileofscore(nz, vol[i], kind="rank")

    regime = pd.Series("normal", index=df.index)
    valid_high = is_high & ~np.isnan(pctl)
    regime[valid_high & (pctl >= CONC_PERCENTILE)] = "concentrated"
    regime[valid_high & (pctl < CONC_PERCENTILE)] = "distributed"
    return regime


def build_episodes(high: pd.DataFrame) -> list[list[int]]:
    high = high.reset_index(drop=True)
    dates = high["date"].values
    episodes = [[0]]
    for i in range(1, len(dates)):
        gap = (dates[i] - dates[episodes[-1][-1]]) / np.timedelta64(1, "D")
        if gap <= EPISODE_GAP_DAYS:
            episodes[-1].append(i)
        else:
            episodes.append([i])
    return episodes


def load_oi_hourly_pct() -> pd.Series:
    """Load OI data, resample to hourly, return pct_change series."""
    oi = pd.read_csv(DATA_DIR / "binance_oi_episodes.csv")
    oi["datetime"] = pd.to_datetime(oi["datetime"]).dt.tz_localize(None)
    oi = oi.sort_values("datetime").set_index("datetime")
    hourly = oi["sum_open_interest_value"].resample("1h").last().dropna()
    return hourly.pct_change()


# ── Helpers ───────────────────────────────────────────────────

def get_dvol_on_date(iv_df: pd.DataFrame, date: pd.Timestamp) -> float:
    match = iv_df[iv_df["date"] == date]
    return match.iloc[0]["dvol_close"] if len(match) > 0 else np.nan


def get_peak_dvol_in_window(iv_df: pd.DataFrame, center: pd.Timestamp,
                             window_days: int = 7) -> tuple:
    """Return (peak_dvol, peak_date) within ±window_days of center."""
    start = center - pd.Timedelta(days=window_days)
    end = center + pd.Timedelta(days=window_days)
    mask = (iv_df["date"] >= start) & (iv_df["date"] <= end)
    window = iv_df[mask]
    if len(window) == 0:
        return np.nan, pd.NaT
    peak_idx = window["dvol_close"].idxmax()
    return window.loc[peak_idx, "dvol_close"], window.loc[peak_idx, "date"]


# ── Tests ─────────────────────────────────────────────────────

def test1_iv_around_concentrated(liq_df: pd.DataFrame, iv_df: pd.DataFrame, out: list):
    """IV level on concentrated days vs 7d prior."""
    out.append("=" * 60)
    out.append("TEST 1: IV LEVEL AROUND CONCENTRATED SPIKES")
    out.append("=" * 60)

    conc = liq_df[liq_df["regime"] == "concentrated"].copy()

    records = []
    for _, row in conc.iterrows():
        d = row["date"]
        iv_now = get_dvol_on_date(iv_df, d)
        iv_7d_prior = get_dvol_on_date(iv_df, d - pd.Timedelta(days=7))
        iv_change = iv_now - iv_7d_prior if not (np.isnan(iv_now) or np.isnan(iv_7d_prior)) else np.nan

        records.append({
            "date": d,
            "total_usd": row["total_usd"],
            "price": row["price"],
            "dvol": iv_now,
            "dvol_7d_prior": iv_7d_prior,
            "dvol_change": iv_change,
        })

    cdf = pd.DataFrame(records)
    valid = cdf.dropna(subset=["dvol", "dvol_change"])

    out.append(f"\n  Concentrated days: {len(conc)}")
    out.append(f"  With IV data: {len(valid)}")

    if len(valid) > 0:
        out.append(f"\n  DVOL on concentrated day:")
        out.append(f"    Median: {valid['dvol'].median():.1f}")
        out.append(f"    Mean:   {valid['dvol'].mean():.1f}")
        out.append(f"  DVOL 7d prior:")
        out.append(f"    Median: {valid['dvol_7d_prior'].median():.1f}")
        out.append(f"    Mean:   {valid['dvol_7d_prior'].mean():.1f}")
        out.append(f"  DVOL change (spike − 7d prior):")
        out.append(f"    Median: {valid['dvol_change'].median():+.1f}")
        out.append(f"    Mean:   {valid['dvol_change'].mean():+.1f}")
        out.append(f"    % positive (IV rose): {100*(valid['dvol_change']>0).mean():.1f}%")

    # Compare to random-day baseline
    merged = iv_df.copy()
    merged["dvol_change_7d"] = merged["dvol_close"] - merged["dvol_close"].shift(7)
    baseline = merged["dvol_change_7d"].dropna()
    conc_changes = valid["dvol_change"].dropna()

    out.append(f"\n  Baseline (all days) 7d IV change:")
    out.append(f"    Median: {baseline.median():+.1f}, Mean: {baseline.mean():+.1f}")
    out.append(f"    % positive: {100*(baseline>0).mean():.1f}%")

    if len(conc_changes) >= 3:
        stat, pval = stats.mannwhitneyu(conc_changes, baseline, alternative="two-sided")
        out.append(f"\n  Mann-Whitney (conc vs baseline): U={stat:.0f}, p={pval:.4f}")

    # Per-day table
    out.append(f"\n  {'Date':<12s} {'LiqUSD':>12s} {'Price':>8s} {'DVOL':>6s} "
               f"{'7d Prior':>8s} {'Change':>8s}")
    out.append(f"  {'-'*58}")
    for _, r in cdf.sort_values("date").iterrows():
        dv = f"{r['dvol']:.1f}" if not np.isnan(r["dvol"]) else "n/a"
        pr = f"{r['dvol_7d_prior']:.1f}" if not np.isnan(r["dvol_7d_prior"]) else "n/a"
        ch = f"{r['dvol_change']:+.1f}" if not np.isnan(r["dvol_change"]) else "n/a"
        out.append(f"  {str(r['date'].date()):<12s} ${r['total_usd']:>11,.0f} "
                   f"${r['price']:>7,.0f} {dv:>6s} {pr:>8s} {ch:>8s}")


def test2_iv_timing_vs_spike(high: pd.DataFrame, episodes: list,
                              iv_df: pd.DataFrame, out: list):
    """For escalating episodes, when does peak IV occur relative to the first concentrated spike?"""
    out.append("")
    out.append("=" * 60)
    out.append("TEST 2: IV TIMING RELATIVE TO CONCENTRATED SPIKE")
    out.append("=" * 60)

    regimes = high["regime"].values
    records = []

    for ep in episodes:
        ep_regimes = regimes[ep]
        r_set = set(ep_regimes)
        if not ("concentrated" in r_set and "distributed" in r_set):
            continue  # only mixed/escalating

        first_conc_pos = next(i for i, r in enumerate(ep_regimes) if r == "concentrated")
        first_conc_date = high.iloc[ep[first_conc_pos]]["date"]

        peak_dvol, peak_date = get_peak_dvol_in_window(iv_df, first_conc_date, 7)
        conc_dvol = get_dvol_on_date(iv_df, first_conc_date)

        if pd.isna(peak_date):
            continue

        gap = (peak_date - first_conc_date) / np.timedelta64(1, "D")

        records.append({
            "ep_start": high.iloc[ep[0]]["date"],
            "first_conc": first_conc_date,
            "conc_dvol": conc_dvol,
            "peak_dvol": peak_dvol,
            "peak_date": peak_date,
            "gap_days": gap,
        })

    rdf = pd.DataFrame(records)

    out.append(f"\n  Escalating episodes with IV data: {len(rdf)}")

    out.append(f"\n  {'Ep Start':<12s} {'1st Conc':>12s} {'Conc DVOL':>10s} "
               f"{'Peak DVOL':>10s} {'Peak Date':>12s} {'Gap':>6s}")
    out.append(f"  {'-'*66}")

    for _, r in rdf.sort_values("ep_start").iterrows():
        cd = f"{r['conc_dvol']:.1f}" if not np.isnan(r["conc_dvol"]) else "n/a"
        pd_ = f"{r['peak_dvol']:.1f}"
        gap_s = f"{r['gap_days']:+.0f}d"
        out.append(f"  {str(r['ep_start'].date()):<12s} {str(r['first_conc'].date()):>12s} "
                   f"{cd:>10s} {pd_:>10s} {str(r['peak_date'].date()):>12s} {gap_s:>6s}")

    if len(rdf) > 0:
        gaps = rdf["gap_days"]
        n_before = (gaps < 0).sum()
        n_same = (gaps == 0).sum()
        n_after = (gaps > 0).sum()

        out.append(f"\n  Peak IV timing (negative = IV peaked before conc spike):")
        out.append(f"    Before spike: {n_before}")
        out.append(f"    Same day:     {n_same}")
        out.append(f"    After spike:  {n_after}")
        out.append(f"    Median gap:   {gaps.median():+.1f} days")
        out.append(f"    Mean gap:     {gaps.mean():+.1f} days")


def test3_iv_vs_oi(high: pd.DataFrame, episodes: list, iv_df: pd.DataFrame,
                    oi_pct: pd.Series, out: list):
    """Compare IV peak timing to OI drop timing and lending spike timing."""
    out.append("")
    out.append("=" * 60)
    out.append("TEST 3: IV TIMING vs OI DROP vs LENDING SPIKE")
    out.append("=" * 60)

    regimes = high["regime"].values
    oi_start = oi_pct.index.min()
    records = []

    for ep in episodes:
        ep_regimes = regimes[ep]
        r_set = set(ep_regimes)
        if not ("concentrated" in r_set and "distributed" in r_set):
            continue

        ep_start = high.iloc[ep[0]]["date"]
        if ep_start < oi_start:
            continue

        first_conc_pos = next(i for i, r in enumerate(ep_regimes) if r == "concentrated")
        first_conc_date = high.iloc[ep[first_conc_pos]]["date"]

        # IV peak in ±7d of conc spike
        peak_dvol, iv_peak_date = get_peak_dvol_in_window(iv_df, first_conc_date, 7)

        # OI trough (most negative hourly change) in ±7d of conc spike
        oi_start_w = first_conc_date - pd.Timedelta(days=7)
        oi_end_w = first_conc_date + pd.Timedelta(days=7)
        oi_window = oi_pct[(oi_pct.index >= oi_start_w) & (oi_pct.index <= oi_end_w)]

        if len(oi_window) == 0 or pd.isna(iv_peak_date):
            continue

        oi_trough_idx = oi_window.idxmin()
        oi_trough_date = oi_trough_idx.normalize()  # day-level
        oi_trough_val = oi_window[oi_trough_idx]

        # Lending peak day = first concentrated day (by definition, highest liq volume)
        lending_peak_date = first_conc_date

        iv_vs_conc = (iv_peak_date - first_conc_date) / np.timedelta64(1, "D")
        oi_vs_conc = (oi_trough_date - first_conc_date) / np.timedelta64(1, "D")
        iv_vs_oi = (iv_peak_date - oi_trough_date) / np.timedelta64(1, "D")

        records.append({
            "ep_start": ep_start,
            "first_conc": first_conc_date,
            "iv_peak_date": iv_peak_date,
            "oi_trough_date": oi_trough_date,
            "iv_vs_conc": iv_vs_conc,
            "oi_vs_conc": oi_vs_conc,
            "iv_vs_oi": iv_vs_oi,
            "peak_dvol": peak_dvol,
            "oi_trough_pct": oi_trough_val,
        })

    rdf = pd.DataFrame(records)

    out.append(f"\n  Escalating episodes in OI period with IV data: {len(rdf)}")
    out.append(f"  Gaps are in days. Negative = event occurred BEFORE conc spike.")

    out.append(f"\n  {'Ep Start':<12s} {'1st Conc':>12s} {'IV peak':>12s} {'OI trough':>12s} "
               f"{'IV−Conc':>8s} {'OI−Conc':>8s} {'IV−OI':>6s}")
    out.append(f"  {'-'*76}")

    for _, r in rdf.sort_values("ep_start").iterrows():
        iv_c = f"{r['iv_vs_conc']:+.0f}d"
        oi_c = f"{r['oi_vs_conc']:+.0f}d"
        iv_oi = f"{r['iv_vs_oi']:+.0f}d"
        out.append(f"  {str(r['ep_start'].date()):<12s} {str(r['first_conc'].date()):>12s} "
                   f"{str(r['iv_peak_date'].date()):>12s} {str(r['oi_trough_date'].date()):>12s} "
                   f"{iv_c:>8s} {oi_c:>8s} {iv_oi:>6s}")

    if len(rdf) > 0:
        out.append(f"\n  --- Summary ---")
        out.append(f"  IV peak vs concentrated spike:")
        out.append(f"    Median: {rdf['iv_vs_conc'].median():+.1f}d, "
                   f"Mean: {rdf['iv_vs_conc'].mean():+.1f}d")
        iv_before = (rdf["iv_vs_conc"] < 0).sum()
        iv_same = (rdf["iv_vs_conc"] == 0).sum()
        iv_after = (rdf["iv_vs_conc"] > 0).sum()
        out.append(f"    Before: {iv_before}, Same day: {iv_same}, After: {iv_after}")

        out.append(f"\n  OI trough vs concentrated spike:")
        out.append(f"    Median: {rdf['oi_vs_conc'].median():+.1f}d, "
                   f"Mean: {rdf['oi_vs_conc'].mean():+.1f}d")
        oi_before = (rdf["oi_vs_conc"] < 0).sum()
        oi_same = (rdf["oi_vs_conc"] == 0).sum()
        oi_after = (rdf["oi_vs_conc"] > 0).sum()
        out.append(f"    Before: {oi_before}, Same day: {oi_same}, After: {oi_after}")

        out.append(f"\n  IV peak vs OI trough (does IV lead OI?):")
        out.append(f"    Median: {rdf['iv_vs_oi'].median():+.1f}d, "
                   f"Mean: {rdf['iv_vs_oi'].mean():+.1f}d")
        leads = (rdf["iv_vs_oi"] < 0).sum()
        same = (rdf["iv_vs_oi"] == 0).sum()
        lags = (rdf["iv_vs_oi"] > 0).sum()
        out.append(f"    IV leads OI: {leads}, Same day: {same}, IV lags OI: {lags}")

        if leads > lags:
            out.append(f"\n  → IV tends to peak BEFORE OI trough — IV provides earlier warning")
        elif lags > leads:
            out.append(f"\n  → IV tends to peak AFTER OI trough — OI moves first")
        else:
            out.append(f"\n  → No clear ordering between IV and OI")


# ── Main ──────────────────────────────────────────────────────

def main():
    out = []
    out.append("OPTIONS IV TIMING PROBE — DERIBIT ETH DVOL")
    out.append("Source: Deribit public API (DVOL index, daily resolution)")
    out.append("Classification: M1-P97 | Episodes: 14d gap clustering")
    out.append("")

    iv_df = fetch_dvol()

    df = load_liquidations()
    df["regime"] = classify_m1p97(df)

    high = df[df["regime"].isin(["concentrated", "distributed"])].copy()
    high = high.reset_index(drop=True)
    episodes = build_episodes(high)

    oi_pct = load_oi_hourly_pct()

    out.append(f"DVOL data: {iv_df['date'].min().date()} to {iv_df['date'].max().date()} "
               f"({len(iv_df)} daily observations)")
    out.append(f"DVOL range: [{iv_df['dvol_close'].min():.1f}, {iv_df['dvol_close'].max():.1f}]")
    out.append(f"DVOL median: {iv_df['dvol_close'].median():.1f}")
    out.append("")

    test1_iv_around_concentrated(df, iv_df, out)
    test2_iv_timing_vs_spike(high, episodes, iv_df, out)
    test3_iv_vs_oi(high, episodes, iv_df, oi_pct, out)

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
