#!/usr/bin/env python3
"""
Arc Follow-up: Forward-Window Contamination Check + OI Escalation Predictor

Test A: Do pre-concentrated distributed days only look good because the
        concentrated spike falls inside the 7d forward return window?
Test B: Can OI drops predict which episodes will escalate from distributed
        to concentrated?
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "arc_followup_results.txt"

HIGH_LIQ_PERCENTILE = 90
CONC_PERCENTILE = 97
FORWARD_HORIZON = 7
EPISODE_GAP_DAYS = 14
OI_DROP_THRESHOLD = -0.03  # >3% hourly drop


# ── Shared infrastructure ─────────────────────────────────────

def load_liquidations() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["price"].shift(-FORWARD_HORIZON) / df["price"] - 1
    df["trail_7d"] = df["price"] / df["price"].shift(7) - 1
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


def max_oi_drop_in_window(oi_pct: pd.Series, center: pd.Timestamp,
                          hours: int = 48) -> float:
    """Max (most negative) hourly OI change within ±hours of center."""
    ws = center - pd.Timedelta(hours=hours)
    we = center + pd.Timedelta(hours=hours)
    window = oi_pct[(oi_pct.index >= ws) & (oi_pct.index <= we)]
    return window.min() if len(window) > 0 else np.nan


# ── Test A: Forward-Window Contamination ──────────────────────

def test_a(high: pd.DataFrame, episodes: list, out: list):
    out.append("=" * 60)
    out.append("TEST A: FORWARD-WINDOW CONTAMINATION CHECK")
    out.append("=" * 60)
    out.append("")
    out.append("For pre-concentrated distributed days: is the first concentrated")
    out.append("spike ≤7 days away (inside the fwd_7d window)?")

    regimes = high["regime"].values

    # Identify mixed episodes and pre-concentrated distributed days
    pre_days = []

    for ep in episodes:
        ep_regimes = regimes[ep]
        r_set = set(ep_regimes)
        if not ("concentrated" in r_set and "distributed" in r_set):
            continue

        # First concentrated position within episode
        first_conc_pos = next(i for i, r in enumerate(ep_regimes) if r == "concentrated")
        first_conc_date = high.iloc[ep[first_conc_pos]]["date"]

        for j, idx in enumerate(ep):
            if j >= first_conc_pos:
                break
            if ep_regimes[j] != "distributed":
                continue
            row = high.iloc[idx]
            gap = (first_conc_date - row["date"]) / np.timedelta64(1, "D")
            pre_days.append({
                "date": row["date"],
                "fwd_7d": row["fwd_7d"],
                "trail_7d": row["trail_7d"],
                "price": row["price"],
                "total_usd": row["total_usd"],
                "first_conc_date": first_conc_date,
                "gap_days": gap,
                "contaminated": gap <= FORWARD_HORIZON,
            })

    pdf = pd.DataFrame(pre_days)
    n_contam = pdf["contaminated"].sum()
    n_clean = (~pdf["contaminated"]).sum()

    out.append(f"\n  Pre-concentrated distributed days: {len(pdf)}")
    out.append(f"  Contaminated (spike ≤7d away):     {n_contam}")
    out.append(f"  Clean (spike >7d away):             {n_clean}")

    # Per-day detail
    out.append(f"\n  {'Date':<12s} {'1st Conc':>12s} {'Gap':>5s} {'Label':>7s} "
               f"{'Fwd7d':>8s} {'Trail7d':>8s} {'Price':>8s}")
    out.append(f"  {'-'*68}")

    for _, r in pdf.sort_values("date").iterrows():
        label = "CONTAM" if r["contaminated"] else "CLEAN"
        f7 = f"{r['fwd_7d']*100:+.1f}%" if not np.isnan(r["fwd_7d"]) else "n/a"
        t7 = f"{r['trail_7d']*100:+.1f}%" if not np.isnan(r["trail_7d"]) else "n/a"
        out.append(f"  {str(r['date'].date()):<12s} {str(r['first_conc_date'].date()):>12s} "
                   f"{r['gap_days']:>5.0f} {label:>7s} {f7:>8s} {t7:>8s} ${r['price']:>7,.0f}")

    # Group comparison
    out.append(f"\n  --- Group outcomes ---")

    groups = [
        ("Contaminated (≤7d)", pdf[pdf["contaminated"]]),
        ("Clean (>7d)", pdf[~pdf["contaminated"]]),
        ("All pre-concentrated", pdf),
    ]

    out.append(f"\n  {'Group':<30s} {'n':>4s} {'%decline':>9s} {'Med fwd7d':>10s} {'Mean fwd7d':>11s}")
    out.append(f"  {'-'*66}")

    for label, sub in groups:
        fwd = sub["fwd_7d"].dropna()
        if len(fwd) > 0:
            neg = 100 * (fwd < 0).mean()
            med = fwd.median() * 100
            mean = fwd.mean() * 100
            out.append(f"  {label:<30s} {len(fwd):>4d} {neg:>8.1f}% {med:>+9.2f}% {mean:>+10.2f}%")

    # Also show non-mixed baseline for comparison
    non_mixed_dist = []
    for ep in episodes:
        r_set = set(regimes[ep])
        if "concentrated" in r_set and "distributed" in r_set:
            continue
        for idx in ep:
            if regimes[idx] == "distributed":
                non_mixed_dist.append(high.iloc[idx])
    if non_mixed_dist:
        nm_fwd = pd.DataFrame(non_mixed_dist)["fwd_7d"].dropna()
        neg = 100 * (nm_fwd < 0).mean()
        med = nm_fwd.median() * 100
        mean = nm_fwd.mean() * 100
        out.append(f"  {'Non-mixed baseline':<30s} {len(nm_fwd):>4d} {neg:>8.1f}% {med:>+9.2f}% {mean:>+10.2f}%")

    # Verdict
    clean_fwd = pdf.loc[~pdf["contaminated"], "fwd_7d"].dropna()
    out.append(f"\n  --- Verdict ---")
    if len(clean_fwd) > 0:
        neg = 100 * (clean_fwd < 0).mean()
        out.append(f"  Clean subset: {len(clean_fwd)} days, {neg:.1f}% decline rate")
        if neg >= 65:
            out.append(f"  → Clean pre-concentrated days STILL show elevated hit rate")
            out.append(f"  → Signal has independent predictive content beyond window contamination")
        elif neg >= 50:
            out.append(f"  → Clean subset is marginal — some but not strong independent signal")
        else:
            out.append(f"  → Clean subset ≤50% — pre-concentrated signal likely explained by window overlap")
    else:
        out.append(f"  No clean days available")

    return pdf


# ── Test B: OI as Episode Escalation Predictor ────────────────

def test_b(high: pd.DataFrame, episodes: list, oi_pct: pd.Series, out: list):
    out.append("")
    out.append("=" * 60)
    out.append("TEST B: OI AS EPISODE ESCALATION PREDICTOR")
    out.append("=" * 60)
    out.append("")
    out.append("Does a >3% hourly OI drop near the episode start predict")
    out.append("whether the episode will escalate to concentrated?")

    regimes = high["regime"].values
    oi_start = oi_pct.index.min()

    # Classify episodes that contain at least one distributed day
    ep_records = []
    for ep in episodes:
        ep_regimes = set(regimes[ep])

        has_distributed = "distributed" in ep_regimes
        if not has_distributed:
            continue  # pure concentrated — not relevant

        has_concentrated = "concentrated" in ep_regimes
        escalated = has_concentrated  # mixed = escalated

        # First day of episode
        first_day = high.iloc[ep[0]]
        first_date = first_day["date"]

        # Check if in OI period
        in_oi_period = first_date >= oi_start

        # OI drop near first day
        oi_drop = max_oi_drop_in_window(oi_pct, first_date) if in_oi_period else np.nan
        has_oi_drop = oi_drop < OI_DROP_THRESHOLD if not np.isnan(oi_drop) else None

        # Episode-level forward return (first day)
        first_fwd = first_day["fwd_7d"]

        ep_records.append({
            "start": first_date,
            "size": len(ep),
            "escalated": escalated,
            "in_oi_period": in_oi_period,
            "oi_drop": oi_drop,
            "has_oi_drop": has_oi_drop,
            "fwd_7d": first_fwd,
            "n_distributed": sum(1 for i in ep if regimes[i] == "distributed"),
            "n_concentrated": sum(1 for i in ep if regimes[i] == "concentrated"),
        })

    edf = pd.DataFrame(ep_records)

    out.append(f"\n  Total episodes with ≥1 distributed day: {len(edf)}")
    out.append(f"  Escalated (mixed): {edf['escalated'].sum()}")
    out.append(f"  Non-escalated (distributed-only): {(~edf['escalated']).sum()}")

    # Full episode list
    out.append(f"\n  {'Start':<12s} {'Size':>4s} {'D':>3s} {'C':>3s} {'Esc':>4s} "
               f"{'OI drop':>8s} {'Fwd7d':>8s}")
    out.append(f"  {'-'*50}")

    for _, r in edf.sort_values("start").iterrows():
        esc = "YES" if r["escalated"] else "no"
        oi_s = f"{r['oi_drop']*100:+.1f}%" if not np.isnan(r["oi_drop"]) else "—"
        f7 = f"{r['fwd_7d']*100:+.1f}%" if not np.isnan(r["fwd_7d"]) else "n/a"
        out.append(f"  {str(r['start'].date()):<12s} {r['size']:>4d} {r['n_distributed']:>3d} "
                   f"{r['n_concentrated']:>3d} {esc:>4s} {oi_s:>8s} {f7:>8s}")

    # OI-period cross-tab
    oi_edf = edf[edf["in_oi_period"] & edf["has_oi_drop"].notna()].copy()

    out.append(f"\n  --- OI-period episodes (2024-03+) ---")
    out.append(f"  Episodes with OI data: {len(oi_edf)}")

    if len(oi_edf) < 4:
        out.append(f"  Insufficient data for cross-tab")
        return

    # 2x2 table
    a = ((oi_edf["has_oi_drop"]) & (oi_edf["escalated"])).sum()    # OI drop + escalated
    b = ((oi_edf["has_oi_drop"]) & (~oi_edf["escalated"])).sum()   # OI drop + not escalated
    c = ((~oi_edf["has_oi_drop"]) & (oi_edf["escalated"])).sum()   # no drop + escalated
    d = ((~oi_edf["has_oi_drop"]) & (~oi_edf["escalated"])).sum()  # no drop + not escalated

    out.append(f"\n  Cross-tab:")
    out.append(f"    {'':22s} {'Escalated':>10s} {'Not esc.':>10s} {'Total':>7s}")
    out.append(f"    {'OI drop >3%':<22s} {a:>10d} {b:>10d} {a+b:>7d}")
    out.append(f"    {'No OI drop':<22s} {c:>10d} {d:>10d} {c+d:>7d}")
    out.append(f"    {'Total':<22s} {a+c:>10d} {b+d:>10d} {a+b+c+d:>7d}")

    # Rates
    if a + b > 0:
        out.append(f"\n  With OI drop:    {a}/{a+b} escalated ({100*a/(a+b):.1f}%)")
    if c + d > 0:
        out.append(f"  Without OI drop: {c}/{c+d} escalated ({100*c/(c+d):.1f}%)")

    # Fisher's exact test
    table = np.array([[a, b], [c, d]])
    if table.min() >= 0 and table.sum() >= 4:
        odds, pval = stats.fisher_exact(table)
        out.append(f"\n  Fisher's exact: odds ratio={odds:.2f}, p={pval:.4f}")

    # Escalation rate by OI drop magnitude
    out.append(f"\n  --- OI drop magnitude and escalation ---")
    out.append(f"  {'Start':<12s} {'Size':>4s} {'Esc':>4s} {'OI drop':>8s}")
    out.append(f"  {'-'*32}")
    for _, r in oi_edf.sort_values("oi_drop").iterrows():
        esc = "YES" if r["escalated"] else "no"
        out.append(f"  {str(r['start'].date()):<12s} {r['size']:>4d} {esc:>4s} "
                   f"{r['oi_drop']*100:+.2f}%")


# ── Main ──────────────────────────────────────────────────────

def main():
    out = []
    out.append("ARC FOLLOW-UP: CONTAMINATION CHECK + OI ESCALATION PREDICTOR")
    out.append("Classification: M1-P97 | Episodes: 14d gap clustering")
    out.append("")

    df = load_liquidations()
    df["regime"] = classify_m1p97(df)

    high = df[df["regime"].isin(["concentrated", "distributed"])].copy()
    high = high.reset_index(drop=True)
    episodes = build_episodes(high)

    oi_pct = load_oi_hourly_pct()

    test_a(high, episodes, out)
    test_b(high, episodes, oi_pct, out)

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
