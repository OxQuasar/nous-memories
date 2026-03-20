#!/usr/bin/env python3
"""
False Positive Anatomy — Distributed Episodes That Don't Decline

Characterize what distinguishes the ~32% of distributed liquidation days
where 7d forward return is positive (signal fails) from the ~68% where
it works. Identify filterable conditions.

Classification: M1-P97 (180d window, ≥97th percentile → concentrated).
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "false_positive_results.txt"

HIGH_LIQ_PERCENTILE = 90
CONC_PERCENTILE = 97
FORWARD_HORIZON = 7
EPISODE_GAP_DAYS = 14


# ── Data loading ──────────────────────────────────────────────

def load_liquidations() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["price"].shift(-FORWARD_HORIZON) / df["price"] - 1
    df["fwd_14d"] = df["price"].shift(-14) / df["price"] - 1
    df["trail_7d"] = df["price"] / df["price"].shift(7) - 1
    df["trail_14d"] = df["price"] / df["price"].shift(14) - 1
    df["trail_30d"] = df["price"] / df["price"].shift(30) - 1
    return df


def classify_m1p97(df: pd.DataFrame) -> pd.Series:
    """180d window percentile classification. ≥P97 → concentrated, else distributed."""
    nonzero = df.loc[df["total_usd"] > 0, "total_usd"]
    threshold = nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)
    is_high = df["total_usd"] > threshold

    vol = df["total_usd"].values
    n = len(vol)
    pctl_in_window = np.full(n, np.nan)

    for i in range(n):
        start = max(0, i - 179)
        window = vol[start:i + 1]
        nz = window[window > 0]
        if len(nz) >= 10:
            pctl_in_window[i] = stats.percentileofscore(nz, vol[i], kind="rank")

    regime = pd.Series("normal", index=df.index)
    valid_high = is_high & ~np.isnan(pctl_in_window)
    regime[valid_high & (pctl_in_window >= CONC_PERCENTILE)] = "concentrated"
    regime[valid_high & (pctl_in_window < CONC_PERCENTILE)] = "distributed"

    df["pctl_180d"] = pctl_in_window
    return regime


def build_episodes(high: pd.DataFrame) -> list[list[int]]:
    """Cluster high-liq days into episodes (14d gap)."""
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


def load_utilization() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "utilization_apy.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df[["date", "stable_apy_weighted"]].rename(columns={"stable_apy_weighted": "apy"})


def load_oi() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "binance_oi_episodes.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


def load_hourly_price() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "eth_price_1h.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


# ── Analysis helpers ──────────────────────────────────────────

def compare_groups(g1: pd.Series, g2: pd.Series, label1: str, label2: str, out: list,
                   pct=True):
    """Compare two groups, report stats + Mann-Whitney.
    pct=True: values are fractions, display as %. pct=False: display raw."""
    for name, s in [(label1, g1), (label2, g2)]:
        if len(s) > 0:
            if pct:
                out.append(f"    {name}: n={len(s)}, median={s.median()*100:+.2f}%, "
                           f"mean={s.mean()*100:+.2f}%")
            else:
                out.append(f"    {name}: n={len(s)}, median={s.median():+.2f}, "
                           f"mean={s.mean():+.2f}")
        else:
            out.append(f"    {name}: n=0")

    if len(g1) >= 3 and len(g2) >= 3:
        stat, pval = stats.mannwhitneyu(g1, g2, alternative="two-sided")
        out.append(f"    Mann-Whitney U={stat:.0f}, p={pval:.4f}")
        return pval
    else:
        out.append(f"    Insufficient data for test")
        return None


# ── Tests ─────────────────────────────────────────────────────

def test1_episode_position(dist: pd.DataFrame, episodes: list, high: pd.DataFrame, out: list):
    """Position within episode: do false positives cluster at episode end?"""
    out.append("\n" + "=" * 60)
    out.append("TEST 1: POSITION WITHIN EPISODE")
    out.append("=" * 60)

    # Map each distributed day to its normalized position
    high_reset = high.reset_index(drop=True)
    date_to_idx = {d: i for i, d in enumerate(high_reset["date"].values)}

    positions = {}
    for ep in episodes:
        n = len(ep)
        for j, idx in enumerate(ep):
            d = high_reset.iloc[idx]["date"]
            norm_pos = j / (n - 1) if n > 1 else 0.5
            positions[d] = norm_pos

    dist = dist.copy()
    dist["ep_position"] = dist["date"].map(positions)
    dist = dist.dropna(subset=["ep_position", "fwd_7d"])

    fp = dist[dist["fwd_7d"] >= 0]
    tp = dist[dist["fwd_7d"] < 0]

    out.append(f"\n  False positives (fwd_7d ≥ 0): n={len(fp)}")
    out.append(f"  True positives  (fwd_7d < 0): n={len(tp)}")

    out.append(f"\n  Episode position (0=start, 1=end):")
    compare_groups(fp["ep_position"], tp["ep_position"], "False pos", "True pos", out)

    # Also: single-day episodes vs multi-day
    single = dist[dist["ep_position"] == 0.5]  # single-day episodes get 0.5
    out.append(f"\n  Single-day episode distributed days: {len(single)}")
    if len(single) > 0:
        out.append(f"    Fwd 7d: median={single['fwd_7d'].median()*100:+.2f}%, "
                   f"%neg={100*(single['fwd_7d']<0).mean():.1f}%")

    return dist


def test2_trailing_drawdown(dist: pd.DataFrame, out: list):
    """Trailing drawdown magnitude for false vs true positive distributed days."""
    out.append("\n" + "=" * 60)
    out.append("TEST 2: TRAILING DRAWDOWN MAGNITUDE")
    out.append("=" * 60)

    fp = dist[dist["fwd_7d"] >= 0].dropna(subset=["trail_7d"])
    tp = dist[dist["fwd_7d"] < 0].dropna(subset=["trail_7d"])

    out.append(f"\n  --- Trailing 7d return ---")
    compare_groups(fp["trail_7d"], tp["trail_7d"], "False pos", "True pos", out)

    fp14 = dist[dist["fwd_7d"] >= 0].dropna(subset=["trail_14d"])
    tp14 = dist[dist["fwd_7d"] < 0].dropna(subset=["trail_14d"])

    out.append(f"\n  --- Trailing 14d return ---")
    compare_groups(fp14["trail_14d"], tp14["trail_14d"], "False pos", "True pos", out)

    # Extreme drawdown test: trail_7d < -15%
    deep = dist.dropna(subset=["trail_7d", "fwd_7d"])
    extreme = deep[deep["trail_7d"] < -0.15]
    moderate = deep[(deep["trail_7d"] >= -0.15) & (deep["trail_7d"] < 0)]
    shallow = deep[deep["trail_7d"] >= 0]

    out.append(f"\n  --- By trailing 7d drawdown bucket ---")
    for label, sub in [("Extreme (<-15%)", extreme), ("Moderate (-15% to 0)", moderate), ("Positive (≥0)", shallow)]:
        if len(sub) > 0:
            out.append(f"    {label}: n={len(sub)}, fwd_7d median={sub['fwd_7d'].median()*100:+.2f}%, "
                       f"%neg={100*(sub['fwd_7d']<0).mean():.1f}%")
        else:
            out.append(f"    {label}: n=0")


def test3_volume_percentile(dist: pd.DataFrame, out: list):
    """Liquidation volume proximity to thresholds."""
    out.append("\n" + "=" * 60)
    out.append("TEST 3: VOLUME PERCENTILE RANK (180d window)")
    out.append("=" * 60)

    valid = dist.dropna(subset=["pctl_180d", "fwd_7d"])
    fp = valid[valid["fwd_7d"] >= 0]
    tp = valid[valid["fwd_7d"] < 0]

    out.append(f"\n  Percentile rank within 180d window:")
    compare_groups(fp["pctl_180d"], tp["pctl_180d"], "False pos", "True pos", out, pct=False)

    # Bin by percentile ranges
    bins = [(90, 93), (93, 95), (95, 97)]
    out.append(f"\n  --- By 180d percentile bin ---")
    for lo, hi in bins:
        sub = valid[(valid["pctl_180d"] >= lo) & (valid["pctl_180d"] < hi)]
        if len(sub) > 0:
            out.append(f"    P{lo}-P{hi}: n={len(sub)}, fwd_7d median={sub['fwd_7d'].median()*100:+.2f}%, "
                       f"%neg={100*(sub['fwd_7d']<0).mean():.1f}%")
        else:
            out.append(f"    P{lo}-P{hi}: n=0")

    # Correlation
    if len(valid) >= 5:
        r, p = stats.spearmanr(valid["pctl_180d"], valid["fwd_7d"])
        out.append(f"\n  Spearman correlation (pctl_180d vs fwd_7d): r={r:.3f}, p={p:.4f}")


def test4_utilization_regime(dist: pd.DataFrame, util_df: pd.DataFrame, out: list):
    """Utilization/APY at time of distributed day."""
    out.append("\n" + "=" * 60)
    out.append("TEST 4: UTILIZATION REGIME (APY)")
    out.append("=" * 60)

    merged = dist.merge(util_df, on="date", how="left")
    valid = merged.dropna(subset=["apy", "fwd_7d"])

    out.append(f"\n  Distributed days with APY data: {len(valid)} / {len(dist)}")

    if len(valid) < 5:
        out.append("  Insufficient overlap for analysis")
        return

    fp = valid[valid["fwd_7d"] >= 0]
    tp = valid[valid["fwd_7d"] < 0]

    out.append(f"\n  APY at time of event:")
    compare_groups(fp["apy"], tp["apy"], "False pos", "True pos", out, pct=False)

    # Low vs high APY
    apy_median = valid["apy"].median()
    low_apy = valid[valid["apy"] < apy_median]
    high_apy = valid[valid["apy"] >= apy_median]

    out.append(f"\n  --- Split by APY median ({apy_median:.2f}%) ---")
    for label, sub in [("Low APY", low_apy), ("High APY", high_apy)]:
        if len(sub) > 0:
            out.append(f"    {label}: n={len(sub)}, fwd_7d median={sub['fwd_7d'].median()*100:+.2f}%, "
                       f"%neg={100*(sub['fwd_7d']<0).mean():.1f}%")

    # Also test at 2.7% threshold from plan
    low27 = valid[valid["apy"] < 2.7]
    high27 = valid[valid["apy"] >= 2.7]
    out.append(f"\n  --- Split at APY=2.7% ---")
    for label, sub in [("APY < 2.7%", low27), ("APY ≥ 2.7%", high27)]:
        if len(sub) > 0:
            out.append(f"    {label}: n={len(sub)}, fwd_7d median={sub['fwd_7d'].median()*100:+.2f}%, "
                       f"%neg={100*(sub['fwd_7d']<0).mean():.1f}%")
        else:
            out.append(f"    {label}: n=0")

    if len(valid) >= 5:
        r, p = stats.spearmanr(valid["apy"], valid["fwd_7d"])
        out.append(f"\n  Spearman correlation (APY vs fwd_7d): r={r:.3f}, p={p:.4f}")


def test5_prior_episode_recency(dist: pd.DataFrame, all_high: pd.DataFrame, out: list):
    """Time since prior high-liquidation episode."""
    out.append("\n" + "=" * 60)
    out.append("TEST 5: PRIOR EPISODE RECENCY")
    out.append("=" * 60)

    # For each distributed day, find days since last high-liq day (any type)
    all_dates = sorted(all_high["date"].values)
    dist = dist.copy()

    days_since = []
    for _, row in dist.iterrows():
        d = row["date"]
        # Find preceding high-liq days (before this day)
        prior = [x for x in all_dates if x < d]
        if prior:
            gap = (d - prior[-1]) / np.timedelta64(1, "D")
            days_since.append(gap)
        else:
            days_since.append(np.nan)

    dist["days_since_prior"] = days_since
    valid = dist.dropna(subset=["days_since_prior", "fwd_7d"])

    fp = valid[valid["fwd_7d"] >= 0]
    tp = valid[valid["fwd_7d"] < 0]

    out.append(f"\n  Days since prior high-liquidation day:")
    compare_groups(fp["days_since_prior"], tp["days_since_prior"], "False pos", "True pos", out, pct=False)

    # Cluster: within same episode (≤14d) vs fresh episode (>14d)
    same_ep = valid[valid["days_since_prior"] <= EPISODE_GAP_DAYS]
    fresh_ep = valid[valid["days_since_prior"] > EPISODE_GAP_DAYS]

    out.append(f"\n  --- Same episode (≤{EPISODE_GAP_DAYS}d gap) vs fresh episode ---")
    for label, sub in [("Same episode", same_ep), ("Fresh episode", fresh_ep)]:
        if len(sub) > 0:
            out.append(f"    {label}: n={len(sub)}, fwd_7d median={sub['fwd_7d'].median()*100:+.2f}%, "
                       f"%neg={100*(sub['fwd_7d']<0).mean():.1f}%")
        else:
            out.append(f"    {label}: n=0")

    return dist


def test6_oi_confirmation(dist: pd.DataFrame, oi_df: pd.DataFrame, out: list):
    """OI drop presence/magnitude within ±48h of distributed day."""
    out.append("\n" + "=" * 60)
    out.append("TEST 6: OPEN INTEREST CONFIRMATION (2024-03+)")
    out.append("=" * 60)

    # Only distributed days after OI data starts
    oi_start = oi_df["datetime"].min()
    oi_start_date = pd.Timestamp(oi_start.date())
    dist_oi = dist[dist["date"] >= oi_start_date].copy()

    out.append(f"\n  OI data starts: {oi_start.date()}")
    out.append(f"  Distributed days in OI period: {len(dist_oi)}")

    if len(dist_oi) < 3:
        out.append("  Insufficient data for OI analysis")
        return

    # Compute hourly OI changes
    oi = oi_df.copy()
    oi = oi.sort_values("datetime").reset_index(drop=True)
    oi["datetime"] = oi["datetime"].dt.tz_localize(None)
    # Resample to ~1h for cleaner analysis
    oi = oi.set_index("datetime")
    oi_hourly = oi["sum_open_interest_value"].resample("1h").last().dropna()
    oi_pct = oi_hourly.pct_change()

    # For each distributed day, find max OI drop in ±48h window
    max_oi_drops = []
    for _, row in dist_oi.iterrows():
        d = row["date"]
        window_start = d - pd.Timedelta(hours=48)
        window_end = d + pd.Timedelta(hours=48)
        mask = (oi_pct.index >= window_start) & (oi_pct.index <= window_end)
        window_drops = oi_pct[mask]
        if len(window_drops) > 0:
            max_drop = window_drops.min()  # most negative = biggest drop
            max_oi_drops.append(max_drop)
        else:
            max_oi_drops.append(np.nan)

    dist_oi["max_oi_drop_48h"] = max_oi_drops
    dist_oi["oi_drop_gt3pct"] = dist_oi["max_oi_drop_48h"] < -0.03

    valid = dist_oi.dropna(subset=["max_oi_drop_48h", "fwd_7d"])

    out.append(f"  With OI data in ±48h window: {len(valid)}")

    fp = valid[valid["fwd_7d"] >= 0]
    tp = valid[valid["fwd_7d"] < 0]

    out.append(f"\n  Max hourly OI drop within ±48h:")
    compare_groups(fp["max_oi_drop_48h"], tp["max_oi_drop_48h"], "False pos", "True pos", out)

    # Binary: >3% OI drop present
    out.append(f"\n  --- >3% hourly OI drop present ---")
    with_drop = valid[valid["oi_drop_gt3pct"]]
    without_drop = valid[~valid["oi_drop_gt3pct"]]

    for label, sub in [("With >3% OI drop", with_drop), ("Without", without_drop)]:
        if len(sub) > 0:
            out.append(f"    {label}: n={len(sub)}, fwd_7d median={sub['fwd_7d'].median()*100:+.2f}%, "
                       f"%neg={100*(sub['fwd_7d']<0).mean():.1f}%")
        else:
            out.append(f"    {label}: n=0")

    # Cross-tab: OI confirmation × outcome
    if len(valid) >= 3:
        oi_fp = ((valid["fwd_7d"] >= 0) & valid["oi_drop_gt3pct"]).sum()
        oi_tp = ((valid["fwd_7d"] < 0) & valid["oi_drop_gt3pct"]).sum()
        no_oi_fp = ((valid["fwd_7d"] >= 0) & ~valid["oi_drop_gt3pct"]).sum()
        no_oi_tp = ((valid["fwd_7d"] < 0) & ~valid["oi_drop_gt3pct"]).sum()
        out.append(f"\n  Cross-tab:")
        out.append(f"    {'':20s} {'FP (≥0)':>10s} {'TP (<0)':>10s}")
        out.append(f"    {'OI drop >3%':<20s} {oi_fp:>10d} {oi_tp:>10d}")
        out.append(f"    {'No OI drop':<20s} {no_oi_fp:>10d} {no_oi_tp:>10d}")


def episode_detail_2026(df: pd.DataFrame, dist: pd.DataFrame, util_df: pd.DataFrame,
                        oi_df: pd.DataFrame, episodes: list, high: pd.DataFrame, out: list):
    """Detail table for 2026-01-20 episode days."""
    out.append("\n" + "=" * 60)
    out.append("2026-01-20 EPISODE DETAIL")
    out.append("=" * 60)

    # Find the episode starting around 2026-01-20
    high_reset = high.reset_index(drop=True)
    ep_2026 = None
    for ep in episodes:
        start_date = high_reset.iloc[ep[0]]["date"]
        if start_date >= pd.Timestamp("2026-01-15") and start_date <= pd.Timestamp("2026-01-25"):
            ep_2026 = ep
            break

    if ep_2026 is None:
        out.append("  Episode not found near 2026-01-20")
        return

    ep_days = high_reset.iloc[ep_2026].copy()

    # Merge utilization
    ep_days = ep_days.merge(util_df, on="date", how="left")

    # OI info
    oi = oi_df.copy().sort_values("datetime")
    oi["datetime"] = oi["datetime"].dt.tz_localize(None)
    oi = oi.set_index("datetime")
    oi_hourly = oi["sum_open_interest_value"].resample("1h").last().dropna()
    oi_pct = oi_hourly.pct_change()

    out.append(f"\n  {'Date':<12s} {'Regime':<14s} {'LiqUSD':>12s} {'P180d':>7s} "
               f"{'Trail7d':>8s} {'Trail14d':>9s} {'Fwd7d':>8s} {'APY':>6s} {'MaxOIdrop':>10s}")
    out.append(f"  {'-'*90}")

    for _, row in ep_days.iterrows():
        d = row["date"]
        regime = row.get("regime", "?")
        liq = row["total_usd"]
        p180 = row.get("pctl_180d", np.nan)
        t7 = row.get("trail_7d", np.nan)
        t14 = row.get("trail_14d", np.nan)
        f7 = row.get("fwd_7d", np.nan)
        apy = row.get("apy", np.nan)

        # OI drop in ±48h
        ws = d - pd.Timedelta(hours=48)
        we = d + pd.Timedelta(hours=48)
        mask = (oi_pct.index >= ws) & (oi_pct.index <= we)
        oi_drop = oi_pct[mask].min() if mask.sum() > 0 else np.nan

        p180_s = f"{p180:.1f}" if not np.isnan(p180) else "n/a"
        t7_s = f"{t7*100:+.1f}%" if not np.isnan(t7) else "n/a"
        t14_s = f"{t14*100:+.1f}%" if not np.isnan(t14) else "n/a"
        f7_s = f"{f7*100:+.1f}%" if not np.isnan(f7) else "n/a"
        apy_s = f"{apy:.2f}" if not np.isnan(apy) else "n/a"
        oi_s = f"{oi_drop*100:+.2f}%" if not np.isnan(oi_drop) else "n/a"

        out.append(f"  {str(d.date()):<12s} {regime:<14s} ${liq:>11,.0f} {p180_s:>7s} "
                   f"{t7_s:>8s} {t14_s:>9s} {f7_s:>8s} {apy_s:>6s} {oi_s:>10s}")


def summary_synthesis(dist: pd.DataFrame, util_df: pd.DataFrame, oi_df: pd.DataFrame, out: list):
    """Synthesize findings across all tests."""
    out.append("\n" + "=" * 60)
    out.append("SYNTHESIS: FALSE POSITIVE CHARACTERISTICS")
    out.append("=" * 60)

    valid = dist.dropna(subset=["fwd_7d"]).copy()
    fp = valid[valid["fwd_7d"] >= 0]
    tp = valid[valid["fwd_7d"] < 0]
    n_fp = len(fp)
    n_tp = len(tp)
    total = n_fp + n_tp

    out.append(f"\n  Total distributed days (M1-P97) with fwd data: {total}")
    out.append(f"  True positives (fwd_7d < 0):  {n_tp} ({100*n_tp/total:.0f}%)")
    out.append(f"  False positives (fwd_7d ≥ 0): {n_fp} ({100*n_fp/total:.0f}%)")

    # Trait prevalence comparison
    out.append(f"\n  --- Trait prevalence (FP% vs TP%) ---")
    out.append(f"  Trait that separates: present in ≥60% of one group, <30% of other")

    traits = []

    # Extreme trailing drawdown
    t7_valid = valid.dropna(subset=["trail_7d"])
    for label, cond in [
        ("trail_7d < -15%", t7_valid["trail_7d"] < -0.15),
        ("trail_7d < -20%", t7_valid["trail_7d"] < -0.20),
        ("trail_7d ≥ 0", t7_valid["trail_7d"] >= 0),
    ]:
        fp_pct = cond[t7_valid["fwd_7d"] >= 0].mean() * 100 if (t7_valid["fwd_7d"] >= 0).sum() > 0 else 0
        tp_pct = cond[t7_valid["fwd_7d"] < 0].mean() * 100 if (t7_valid["fwd_7d"] < 0).sum() > 0 else 0
        traits.append((label, fp_pct, tp_pct, len(t7_valid)))

    # Bull context
    t30_valid = valid.dropna(subset=["trail_30d"])
    for label, cond in [
        ("trail_30d > 0 (bull)", t30_valid["trail_30d"] > 0),
    ]:
        fp_pct = cond[t30_valid["fwd_7d"] >= 0].mean() * 100 if (t30_valid["fwd_7d"] >= 0).sum() > 0 else 0
        tp_pct = cond[t30_valid["fwd_7d"] < 0].mean() * 100 if (t30_valid["fwd_7d"] < 0).sum() > 0 else 0
        traits.append((label, fp_pct, tp_pct, len(t30_valid)))

    out.append(f"\n  {'Trait':<25s} {'FP%':>6s} {'TP%':>6s} {'n':>5s}")
    out.append(f"  {'-'*45}")
    for label, fp_pct, tp_pct, n in traits:
        flag = " ←" if (fp_pct >= 60 and tp_pct < 30) or (tp_pct >= 60 and fp_pct < 30) else ""
        out.append(f"  {label:<25s} {fp_pct:>5.1f}% {tp_pct:>5.1f}% {n:>5d}{flag}")

    # Combined filter analysis (OI period only)
    out.append(f"\n  --- Combined filter: OI drop + bear context (2024-03+) ---")
    oi_start_date = pd.Timestamp(oi_df["datetime"].min().date()).tz_localize(None)
    oi_valid = valid[valid["date"] >= oi_start_date].copy()

    # Merge APY
    oi_valid = oi_valid.merge(util_df, on="date", how="left")

    # Compute OI drop for these days
    oi = oi_df.copy().sort_values("datetime")
    oi["datetime"] = oi["datetime"].dt.tz_localize(None)
    oi = oi.set_index("datetime")
    oi_hourly = oi["sum_open_interest_value"].resample("1h").last().dropna()
    oi_pct = oi_hourly.pct_change()

    oi_drops = []
    for _, row in oi_valid.iterrows():
        d = row["date"]
        ws = d - pd.Timedelta(hours=48)
        we = d + pd.Timedelta(hours=48)
        mask = (oi_pct.index >= ws) & (oi_pct.index <= we)
        drop = oi_pct[mask].min() if mask.sum() > 0 else np.nan
        oi_drops.append(drop)
    oi_valid["oi_drop"] = oi_drops
    oi_valid["has_oi_drop"] = oi_valid["oi_drop"] < -0.03

    # Filter combinations
    filters = [
        ("No filter (baseline)", pd.Series(True, index=oi_valid.index)),
        ("OI drop >3%", oi_valid["has_oi_drop"]),
        ("Bear (trail_30d ≤ 0)", oi_valid["trail_30d"] <= 0),
        ("OI drop + bear", oi_valid["has_oi_drop"] & (oi_valid["trail_30d"] <= 0)),
        ("OI drop + extreme trail (<-15%)", oi_valid["has_oi_drop"] & (oi_valid["trail_7d"] < -0.15)),
    ]

    out.append(f"\n  {'Filter':<35s} {'n':>4s} {'%neg':>6s} {'Med fwd7d':>10s}")
    out.append(f"  {'-'*58}")
    for label, mask in filters:
        sub = oi_valid[mask].dropna(subset=["fwd_7d"])
        if len(sub) > 0:
            neg_pct = 100 * (sub["fwd_7d"] < 0).mean()
            med = sub["fwd_7d"].median() * 100
            out.append(f"  {label:<35s} {len(sub):>4d} {neg_pct:>5.1f}% {med:>+9.2f}%")
        else:
            out.append(f"  {label:<35s}    0")

    # List all false positive days
    out.append(f"\n  --- All false positive distributed days ---")
    out.append(f"  {'Date':<12s} {'Fwd7d':>8s} {'Trail7d':>8s} {'Price':>8s}")
    for _, row in fp.sort_values("date").iterrows():
        f7 = row["fwd_7d"]
        t7 = row.get("trail_7d", np.nan)
        p = row.get("price", np.nan)
        t7_s = f"{t7*100:+.1f}%" if not np.isnan(t7) else "n/a"
        out.append(f"  {str(row['date'].date()):<12s} {f7*100:>+7.1f}% {t7_s:>8s} ${p:>7,.0f}")


# ── Main ──────────────────────────────────────────────────────

def main():
    out = []
    out.append("FALSE POSITIVE ANATOMY — DISTRIBUTED EPISODES")
    out.append("Classification: M1-P97 (180d window, ≥97th pctl → concentrated)")
    out.append("")

    # Load data
    df = load_liquidations()
    df["regime"] = classify_m1p97(df)
    util_df = load_utilization()
    oi_df = load_oi()

    # Extract high-liquidation days
    all_high = df[df["regime"].isin(["concentrated", "distributed"])].copy()
    dist = df[df["regime"] == "distributed"].copy()

    out.append(f"Total days: {len(df)}")
    out.append(f"High-liquidation days: {len(all_high)}")
    out.append(f"  Concentrated: {(all_high['regime']=='concentrated').sum()}")
    out.append(f"  Distributed:  {len(dist)}")
    out.append(f"  Distributed with fwd_7d: {dist['fwd_7d'].notna().sum()}")

    fwd_valid = dist.dropna(subset=["fwd_7d"])
    n_neg = (fwd_valid["fwd_7d"] < 0).sum()
    n_pos = (fwd_valid["fwd_7d"] >= 0).sum()
    out.append(f"  → True positives (decline): {n_neg} ({100*n_neg/len(fwd_valid):.1f}%)")
    out.append(f"  → False positives (no decline): {n_pos} ({100*n_pos/len(fwd_valid):.1f}%)")

    # Build episodes
    episodes = build_episodes(all_high)

    # Run tests
    dist = test1_episode_position(dist, episodes, all_high, out)
    test2_trailing_drawdown(dist, out)
    test3_volume_percentile(dist, out)
    test4_utilization_regime(dist, util_df, out)
    dist = test5_prior_episode_recency(dist, all_high, out)
    test6_oi_confirmation(dist, oi_df, out)

    # 2026-01-20 episode detail
    episode_detail_2026(df, dist, util_df, oi_df, episodes, all_high, out)

    # Synthesis
    summary_synthesis(dist, util_df, oi_df, out)

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
