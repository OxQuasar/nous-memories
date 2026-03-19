#!/usr/bin/env python3
"""
Regime-Invariance Stress Test for Concentration Ratio

Tests whether the concentrated/distributed forward return spread is
structural or a regime artifact, using regime-invariant alternative
classifications, threshold stability analysis, within-regime controls,
and episode clustering.
"""

import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
RESULTS_FILE = DATA_DIR / "regime_test_results.txt"

HIGH_LIQ_PERCENTILE = 90
ORIGINAL_CONC_THRESHOLD = 0.50
FORWARD_HORIZON = 7


# ── Data loading ──────────────────────────────────────────────

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "liquidation_events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["fwd_7d"] = df["price"].shift(-FORWARD_HORIZON) / df["price"] - 1
    df["trail_30d"] = df["price"] / df["price"].shift(30) - 1
    return df


def high_liq_threshold(df: pd.DataFrame) -> float:
    nonzero = df.loc[df["total_usd"] > 0, "total_usd"]
    return nonzero.quantile(HIGH_LIQ_PERCENTILE / 100)


# ── Classification methods ────────────────────────────────────

def original_classification(df: pd.DataFrame, threshold: float) -> pd.Series:
    """Original: today / trailing 7d sum > 0.5 → concentrated."""
    trail_7d_sum = df["total_usd"].rolling(7, min_periods=1).sum()
    ratio = np.where(trail_7d_sum > 0, df["total_usd"] / trail_7d_sum, 0.0)
    is_high = df["total_usd"] > threshold
    regime = pd.Series("normal", index=df.index)
    regime[is_high & (ratio > ORIGINAL_CONC_THRESHOLD)] = "concentrated"
    regime[is_high & (ratio <= ORIGINAL_CONC_THRESHOLD)] = "distributed"
    return regime


def method1_longwindow(df: pd.DataFrame, threshold: float, pctl: float) -> pd.Series:
    """Method 1: Today's volume as percentile within trailing 180d window.
    Concentrated = ≥pctl of that window."""
    is_high = df["total_usd"] > threshold
    vol = df["total_usd"].values
    n = len(vol)

    pctl_in_window = np.full(n, np.nan)
    for i in range(n):
        start = max(0, i - 179)
        window = vol[start:i + 1]
        nonzero = window[window > 0]
        if len(nonzero) >= 10:
            pctl_in_window[i] = stats.percentileofscore(nonzero, vol[i], kind="rank")

    regime = pd.Series("normal", index=df.index)
    valid_high = is_high & ~np.isnan(pctl_in_window)
    regime[valid_high & (pctl_in_window >= pctl)] = "concentrated"
    regime[valid_high & (pctl_in_window < pctl)] = "distributed"
    return regime


def method2_peakratio(df: pd.DataFrame, threshold: float) -> pd.Series:
    """Method 2: Today / max(preceding 6 days). Concentrated = ratio > 0.5.
    Excludes today from the max to avoid trivial ratio=1 for spike days."""
    is_high = df["total_usd"] > threshold
    # Max of the 6 days BEFORE today (shift(1) then rolling 6)
    prior_max = df["total_usd"].shift(1).rolling(6, min_periods=1).max()
    ratio = np.where(prior_max > 0, df["total_usd"] / prior_max, np.inf)
    regime = pd.Series("normal", index=df.index)
    # ratio > 1 means today exceeds the prior 6d peak → spike = concentrated
    # ratio ≤ 1 means today is within the prior 6d range → not a standout = distributed
    # Use 0.5 threshold: today is at least half the prior peak
    regime[is_high & (ratio > 2.0)] = "concentrated"
    regime[is_high & (ratio <= 2.0)] = "distributed"
    return regime


# ── Reporting helpers ─────────────────────────────────────────

def report_group_stats(df: pd.DataFrame, regime_col: str, out: list):
    """Report 7d forward return stats for concentrated vs distributed."""
    high = df[df[regime_col].isin(["concentrated", "distributed"])].copy()
    conc = high.loc[high[regime_col] == "concentrated", "fwd_7d"].dropna()
    dist = high.loc[high[regime_col] == "distributed", "fwd_7d"].dropna()

    for name, s in [("Concentrated", conc), ("Distributed", dist)]:
        if len(s) > 0:
            out.append(f"    {name:14s} n={len(s):3d}  median={s.median()*100:+.3f}%  "
                       f"mean={s.mean()*100:+.3f}%  %neg={100*(s<0).mean():.1f}%")
        else:
            out.append(f"    {name:14s} n=  0")

    if len(conc) >= 3 and len(dist) >= 3:
        spread = (conc.median() - dist.median()) * 100
        stat, pval = stats.mannwhitneyu(conc, dist, alternative="two-sided")
        out.append(f"    Spread (conc - dist median): {spread:+.3f}pp")
        out.append(f"    Mann-Whitney U={stat:.0f}, p={pval:.4f}")
        return spread, pval
    else:
        out.append(f"    Insufficient data for test")
        return None, None


def confusion_matrix(original: pd.Series, new: pd.Series, out: list, method_name: str):
    """2×2 overlap between original and new classification on high-liq days."""
    both = original.isin(["concentrated", "distributed"]) & new.isin(["concentrated", "distributed"])
    o, a = original[both], new[both]

    cc = ((o == "concentrated") & (a == "concentrated")).sum()
    cd = ((o == "concentrated") & (a == "distributed")).sum()
    dc = ((o == "distributed") & (a == "concentrated")).sum()
    dd = ((o == "distributed") & (a == "distributed")).sum()

    out.append(f"\n  Confusion matrix: Original vs {method_name}")
    out.append(f"  (rows=original, cols={method_name})")
    out.append(f"  {'':20s} {'New Conc':>10s} {'New Dist':>10s}")
    out.append(f"  {'Orig Concentrated':<20s} {cc:>10d} {cd:>10d}")
    out.append(f"  {'Orig Distributed':<20s} {dc:>10d} {dd:>10d}")

    for label, num, denom in [
        ("Original distributed → new distributed", dd, dc + dd),
        ("Original concentrated → new concentrated", cc, cc + cd),
    ]:
        if denom > 0:
            out.append(f"  {label}: {num}/{denom} = {num/denom*100:.1f}%")


# ── SECTION A ─────────────────────────────────────────────────

def section_a(df: pd.DataFrame, threshold: float, out: list):
    out.append("=" * 60)
    out.append("A. ALTERNATIVE CLASSIFICATION METHODS")
    out.append("=" * 60)

    df["regime_original"] = original_classification(df, threshold)

    out.append("\n--- Original (trailing 7d sum, >50%) ---")
    report_group_stats(df, "regime_original", out)

    for pctl in [95, 97]:
        col = f"regime_m1_p{pctl}"
        df[col] = method1_longwindow(df, threshold, pctl)
        out.append(f"\n--- Method 1: 180d window, ≥{pctl}th pctl ---")
        report_group_stats(df, col, out)
        confusion_matrix(df["regime_original"], df[col], out, f"M1-P{pctl}")

    df["regime_m2"] = method2_peakratio(df, threshold)
    out.append(f"\n--- Method 2: Peak ratio (today/prior_6d_max > 2.0) ---")
    report_group_stats(df, "regime_m2", out)
    confusion_matrix(df["regime_original"], df["regime_m2"], out, "M2-Peak")

    return df


# ── SECTION B ─────────────────────────────────────────────────

def section_b(df: pd.DataFrame, threshold: float, out: list):
    out.append("\n" + "=" * 60)
    out.append("B. THRESHOLD STABILITY CURVE (Method 1: 180d window)")
    out.append("=" * 60)

    header = f"  {'Pctl':>5s}  {'n_conc':>7s}  {'n_dist':>7s}  {'Med Conc':>10s}  {'Med Dist':>10s}  {'Spread':>10s}  {'p-val':>8s}"
    out.append(f"\n{header}")
    out.append(f"  {'-'*62}")

    for pctl in range(85, 100, 2):
        regime = method1_longwindow(df, threshold, pctl)
        high = df[regime.isin(["concentrated", "distributed"])].copy()
        high["_r"] = regime[high.index]

        conc = high.loc[high["_r"] == "concentrated", "fwd_7d"].dropna()
        dist = high.loc[high["_r"] == "distributed", "fwd_7d"].dropna()

        n_c, n_d = len(conc), len(dist)
        med_c = conc.median() * 100 if n_c > 0 else float("nan")
        med_d = dist.median() * 100 if n_d > 0 else float("nan")
        spread = med_c - med_d if n_c > 0 and n_d > 0 else float("nan")

        if n_c >= 3 and n_d >= 3:
            _, pval = stats.mannwhitneyu(conc, dist, alternative="two-sided")
            p_str = f"{pval:.4f}"
        else:
            p_str = "n/a"

        out.append(f"  {pctl:>4d}th  {n_c:>7d}  {n_d:>7d}  {med_c:>+10.3f}%  {med_d:>+10.3f}%  {spread:>+10.3f}pp  {p_str:>8s}")


# ── SECTION C ─────────────────────────────────────────────────

def section_c(df: pd.DataFrame, out: list):
    out.append("\n" + "=" * 60)
    out.append("C. WITHIN-REGIME CONTROL (trailing 30d ETH return)")
    out.append("=" * 60)

    methods = [
        ("regime_original", "Original"),
        ("regime_m1_p95", "M1-P95"),
        ("regime_m1_p97", "M1-P97"),
        ("regime_m2", "M2-Peak"),
    ]

    for col, label in methods:
        if col not in df.columns:
            continue

        out.append(f"\n--- {label} ---")
        high = df[df[col].isin(["concentrated", "distributed"])].copy()
        high["_r"] = df.loc[high.index, col]
        high = high.dropna(subset=["trail_30d", "fwd_7d"])

        for ctx_name, ctx_mask in [
            ("Bull (30d ret > 0)", high["trail_30d"] > 0),
            ("Bear (30d ret ≤ 0)", high["trail_30d"] <= 0),
        ]:
            sub = high[ctx_mask]
            conc = sub.loc[sub["_r"] == "concentrated", "fwd_7d"].dropna()
            dist = sub.loc[sub["_r"] == "distributed", "fwd_7d"].dropna()

            out.append(f"  {ctx_name}:")
            for name, s in [("Concentrated", conc), ("Distributed", dist)]:
                if len(s) > 0:
                    out.append(f"    {name}: n={len(s)}, median 7d={s.median()*100:+.3f}%, %neg={100*(s<0).mean():.1f}%")
                else:
                    out.append(f"    {name}: n=0")

            if len(conc) >= 3 and len(dist) >= 3:
                spread = (conc.median() - dist.median()) * 100
                stat, pval = stats.mannwhitneyu(conc, dist, alternative="two-sided")
                out.append(f"    Spread: {spread:+.3f}pp, Mann-Whitney p={pval:.4f}")
            else:
                out.append(f"    Insufficient data for within-regime test")


# ── SECTION D ─────────────────────────────────────────────────

def section_d(df: pd.DataFrame, out: list):
    out.append("\n" + "=" * 60)
    out.append("D. EPISODE CLUSTERING (14d gap threshold)")
    out.append("=" * 60)

    high = df[df["regime_original"].isin(["concentrated", "distributed"])].copy()
    high = high.reset_index(drop=True)
    dates = high["date"].values

    # Cluster: gap > 14d between consecutive high-liq days → new episode
    episodes = [[0]]
    for i in range(1, len(dates)):
        gap_days = (dates[i] - dates[episodes[-1][-1]]) / np.timedelta64(1, "D")
        if gap_days <= 14:
            episodes[-1].append(i)
        else:
            episodes.append([i])

    out.append(f"\n  Total high-liquidation days: {len(high)}")
    out.append(f"  Total independent episodes: {len(episodes)}")

    sizes = [len(e) for e in episodes]
    out.append(f"  Episode sizes: min={min(sizes)}, max={max(sizes)}, "
               f"median={np.median(sizes):.0f}, mean={np.mean(sizes):.1f}")
    out.append(f"  Size distribution: {dict(sorted(Counter(sizes).items()))}")

    # Mixed vs pure episodes
    n_mixed = n_pure_conc = n_pure_dist = 0
    ep_returns = []

    for ep_idx in episodes:
        regimes = high.iloc[ep_idx]["regime_original"].values
        regime_set = set(regimes)

        if "concentrated" in regime_set and "distributed" in regime_set:
            n_mixed += 1
        elif "concentrated" in regime_set:
            n_pure_conc += 1
        else:
            n_pure_dist += 1

        # Episode-level return: use first day's forward return, dominant regime
        dominant = max(set(regimes), key=list(regimes).count)
        fwd = high.iloc[ep_idx[0]]["fwd_7d"]
        if not np.isnan(fwd):
            ep_returns.append({"regime": dominant, "fwd_7d": fwd,
                               "date": str(high.iloc[ep_idx[0]]["date"].date()),
                               "size": len(ep_idx)})

    out.append(f"\n  Episode composition (original classification):")
    out.append(f"    Pure concentrated: {n_pure_conc}")
    out.append(f"    Pure distributed:  {n_pure_dist}")
    out.append(f"    Mixed (both):      {n_mixed}")
    out.append(f"    Total episodes:    {len(episodes)} (vs {len(high)} individual days)")

    ep_df = pd.DataFrame(ep_returns)
    if len(ep_df) > 0:
        out.append(f"\n  Episode-level 7d forward returns (dominant regime, first day):")
        conc_ep = ep_df.loc[ep_df["regime"] == "concentrated", "fwd_7d"]
        dist_ep = ep_df.loc[ep_df["regime"] == "distributed", "fwd_7d"]

        for name, s in [("Concentrated", conc_ep), ("Distributed", dist_ep)]:
            if len(s) > 0:
                out.append(f"    {name}: n={len(s)}, median={s.median()*100:+.3f}%, "
                           f"mean={s.mean()*100:+.3f}%, %neg={100*(s<0).mean():.1f}%")

        if len(conc_ep) >= 3 and len(dist_ep) >= 3:
            spread = (conc_ep.median() - dist_ep.median()) * 100
            stat, pval = stats.mannwhitneyu(conc_ep, dist_ep, alternative="two-sided")
            out.append(f"    Spread: {spread:+.3f}pp, Mann-Whitney p={pval:.4f}")

        # List episodes for inspection
        out.append(f"\n  Episode detail:")
        out.append(f"    {'Start':<12s} {'Size':>5s} {'Dominant':<14s} {'7d Ret':>8s}")
        out.append(f"    {'-'*42}")
        for _, row in ep_df.iterrows():
            out.append(f"    {row['date']:<12s} {row['size']:>5d} {row['regime']:<14s} {row['fwd_7d']*100:>+8.2f}%")


# ── SECTION E ─────────────────────────────────────────────────

def section_e(df: pd.DataFrame, out: list):
    """Within-episode position test: do concentrated days (M1-P97) cluster
    later in episodes than distributed days?"""
    out.append("\n" + "=" * 60)
    out.append("E. WITHIN-EPISODE POSITION (M1-P97)")
    out.append("=" * 60)

    col = "regime_m1_p97"
    high = df[df[col].isin(["concentrated", "distributed"])].copy()
    high = high.reset_index(drop=True)
    dates = high["date"].values
    regimes = high[col].values

    # Build episodes (same 14d gap logic as section D)
    episodes = [[0]]
    for i in range(1, len(dates)):
        gap = (dates[i] - dates[episodes[-1][-1]]) / np.timedelta64(1, "D")
        if gap <= 14:
            episodes[-1].append(i)
        else:
            episodes.append([i])

    # Only multi-day episodes that contain both types
    mixed_eps = [ep for ep in episodes if len(ep) > 1
                 and "concentrated" in set(regimes[ep])
                 and "distributed" in set(regimes[ep])]

    out.append(f"\n  Total episodes (M1-P97): {len(episodes)}")
    out.append(f"  Multi-day episodes with both types: {len(mixed_eps)}")

    if not mixed_eps:
        out.append("  No mixed episodes — cannot test within-episode position")
        return

    conc_positions = []
    dist_positions = []

    for ep in mixed_eps:
        n = len(ep)
        for j, idx in enumerate(ep):
            norm_pos = j / (n - 1) if n > 1 else 0.5
            if regimes[idx] == "concentrated":
                conc_positions.append(norm_pos)
            else:
                dist_positions.append(norm_pos)

    conc_pos = np.array(conc_positions)
    dist_pos = np.array(dist_positions)

    out.append(f"\n  Within mixed episodes:")
    out.append(f"    Concentrated days: n={len(conc_pos)}, mean position={conc_pos.mean():.3f}, median={np.median(conc_pos):.3f}")
    out.append(f"    Distributed days:  n={len(dist_pos)}, mean position={dist_pos.mean():.3f}, median={np.median(dist_pos):.3f}")
    out.append(f"    (0.0 = episode start, 1.0 = episode end)")

    if len(conc_pos) >= 3 and len(dist_pos) >= 3:
        stat, pval = stats.mannwhitneyu(conc_pos, dist_pos, alternative="two-sided")
        out.append(f"    Mann-Whitney: U={stat:.0f}, p={pval:.4f}")

        if conc_pos.mean() > dist_pos.mean():
            out.append(f"    → Concentrated days appear LATER in episodes")
            out.append(f"    → Position-in-crash may contribute to forward return spread")
        else:
            out.append(f"    → Concentrated days appear EARLIER or uniformly in episodes")
            out.append(f"    → Position-in-crash does NOT explain the spread")
    else:
        out.append(f"    Insufficient data for position test")

    # Also report per-episode breakdown for transparency
    out.append(f"\n  Episode-level detail (mixed episodes only):")
    out.append(f"    {'Start':<12s} {'Size':>5s}  {'Conc positions':<25s}  {'Dist positions'}")
    out.append(f"    {'-'*70}")
    for ep in mixed_eps:
        start_date = str(high.iloc[ep[0]]["date"].date())
        n = len(ep)
        c_pos = [f"{j/(n-1):.2f}" for j, idx in enumerate(ep) if regimes[idx] == "concentrated"]
        d_pos = [f"{j/(n-1):.2f}" for j, idx in enumerate(ep) if regimes[idx] == "distributed"]
        out.append(f"    {start_date:<12s} {n:>5d}  C:[{','.join(c_pos)}]  D:[{','.join(d_pos)}]")


# ── SECTION F ─────────────────────────────────────────────────

def section_f(df: pd.DataFrame, out: list):
    """Trailing 7d return control: does momentum/mean-reversion explain
    the forward return spread within bear markets?"""
    out.append("\n" + "=" * 60)
    out.append("F. TRAILING 7d RETURN CONTROL (M1-P97, bear market)")
    out.append("=" * 60)

    col = "regime_m1_p97"
    df["trail_7d"] = df["price"] / df["price"].shift(FORWARD_HORIZON) - 1

    high = df[df[col].isin(["concentrated", "distributed"])].copy()
    high["_r"] = df.loc[high.index, col]
    bear = high[high["trail_30d"] <= 0].dropna(subset=["trail_7d", "fwd_7d"])

    conc = bear[bear["_r"] == "concentrated"]
    dist = bear[bear["_r"] == "distributed"]

    out.append(f"\n  Bear-market high-liquidation days (M1-P97): {len(bear)}")
    out.append(f"  Concentrated: {len(conc)}, Distributed: {len(dist)}")

    # 1. Compare trailing 7d returns
    out.append(f"\n  --- Trailing 7d return (drawdown into event) ---")
    c_trail = conc["trail_7d"].dropna()
    d_trail = dist["trail_7d"].dropna()
    out.append(f"    Concentrated: median={c_trail.median()*100:+.3f}%, mean={c_trail.mean()*100:+.3f}%")
    out.append(f"    Distributed:  median={d_trail.median()*100:+.3f}%, mean={d_trail.mean()*100:+.3f}%")

    if len(c_trail) >= 3 and len(d_trail) >= 3:
        stat, pval = stats.mannwhitneyu(c_trail, d_trail, alternative="two-sided")
        out.append(f"    Mann-Whitney: U={stat:.0f}, p={pval:.4f}")
        trail_differs = pval < 0.10
    else:
        trail_differs = False
        out.append(f"    Insufficient data")

    # 2. Compare forward 7d returns (repeat from section C for context)
    out.append(f"\n  --- Forward 7d return ---")
    c_fwd = conc["fwd_7d"].dropna()
    d_fwd = dist["fwd_7d"].dropna()
    out.append(f"    Concentrated: median={c_fwd.median()*100:+.3f}%, mean={c_fwd.mean()*100:+.3f}%")
    out.append(f"    Distributed:  median={d_fwd.median()*100:+.3f}%, mean={d_fwd.mean()*100:+.3f}%")
    fwd_spread = (c_fwd.median() - d_fwd.median()) * 100

    if len(c_fwd) >= 3 and len(d_fwd) >= 3:
        stat, pval_fwd = stats.mannwhitneyu(c_fwd, d_fwd, alternative="two-sided")
        out.append(f"    Spread: {fwd_spread:+.3f}pp, Mann-Whitney p={pval_fwd:.4f}")

    # 3. Excess return: forward − trailing (removes momentum component)
    out.append(f"\n  --- Excess forward return (fwd_7d − trail_7d) ---")
    bear_valid = bear.dropna(subset=["trail_7d", "fwd_7d"]).copy()
    bear_valid["excess"] = bear_valid["fwd_7d"] - bear_valid["trail_7d"]

    c_exc = bear_valid.loc[bear_valid["_r"] == "concentrated", "excess"]
    d_exc = bear_valid.loc[bear_valid["_r"] == "distributed", "excess"]
    out.append(f"    Concentrated: median={c_exc.median()*100:+.3f}%, mean={c_exc.mean()*100:+.3f}%")
    out.append(f"    Distributed:  median={d_exc.median()*100:+.3f}%, mean={d_exc.mean()*100:+.3f}%")

    if len(c_exc) >= 3 and len(d_exc) >= 3:
        exc_spread = (c_exc.median() - d_exc.median()) * 100
        stat, pval_exc = stats.mannwhitneyu(c_exc, d_exc, alternative="two-sided")
        out.append(f"    Excess spread: {exc_spread:+.3f}pp, Mann-Whitney p={pval_exc:.4f}")

    # 4. Verdict
    out.append(f"\n  --- Interpretation ---")
    if trail_differs:
        out.append(f"    Trailing 7d returns DIFFER significantly between groups.")
        if len(c_exc) >= 3 and len(d_exc) >= 3 and pval_exc < 0.10:
            out.append(f"    Excess return spread PERSISTS ({exc_spread:+.3f}pp, p={pval_exc:.4f}).")
            out.append(f"    → Signal survives momentum control — not purely mean-reversion.")
        elif len(c_exc) >= 3 and len(d_exc) >= 3:
            out.append(f"    Excess return spread DOES NOT persist ({exc_spread:+.3f}pp, p={pval_exc:.4f}).")
            out.append(f"    → Forward return spread is explained by momentum/mean-reversion.")
            out.append(f"    → Distributed days had deeper prior drawdowns → bigger bounces expected anyway.")
        else:
            out.append(f"    Insufficient data for excess return test.")
    else:
        out.append(f"    Trailing 7d returns do NOT differ significantly between groups.")
        out.append(f"    → Momentum cannot explain the forward return spread.")
        out.append(f"    → The classification captures something beyond recent price momentum.")


# ── Main ──────────────────────────────────────────────────────

def main():
    out = []
    out.append("REGIME-INVARIANCE STRESS TEST")
    out.append("Concentration Ratio: Structural Signal or Regime Artifact?")
    out.append("Data: liquidation_events_combined.csv (Jan 2022 → Mar 2026)")
    out.append("")

    df = load_data()
    threshold = high_liq_threshold(df)
    out.append(f"High-liquidation threshold (P{HIGH_LIQ_PERCENTILE} of non-zero): ${threshold:,.0f}")
    out.append(f"Total days: {len(df)}, days with liquidations: {(df['total_usd'] > 0).sum()}")

    df = section_a(df, threshold, out)
    section_b(df, threshold, out)
    section_c(df, out)
    section_d(df, out)
    section_e(df, out)
    section_f(df, out)

    result_text = "\n".join(out)
    RESULTS_FILE.write_text(result_text)
    print(result_text)
    print(f"\nResults written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
