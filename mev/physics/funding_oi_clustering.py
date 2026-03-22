"""
Funding Settlement → OI Closure Clustering Analysis

Tests whether OI drops cluster in the 0-4h window after negative funding
settlements on Binance, relative to neutral/positive settlements.

Cross-exchange: Binance funding, Bybit OI (market-wide positioning signal).
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

BASE = "memories/mev/dynamics/data"
OUT = "memories/mev/physics"

# --- Funding rate bin thresholds (expressed as proportions) ---
# 0.0001 = 0.01% = 1 bps
BINS = {
    "deeply_neg":  (-np.inf, -0.0001),
    "mod_neg":     (-0.0001, 0.0),
    "mod_pos":     (0.0, 0.0003),
    "deeply_pos":  (0.0003, np.inf),
}
BIN_LABELS = ["deeply_neg", "mod_neg", "mod_pos", "deeply_pos"]
BIN_DISPLAY = {
    "deeply_neg": "< -1bps",
    "mod_neg": "-1bps to 0",
    "mod_pos": "0 to 3bps",
    "deeply_pos": "> 3bps",
}

HOURS_POST = 8  # hours to track after settlement


def load_data():
    """Load and combine episodes + control data."""
    fund_ep = pd.read_csv(f"{BASE}/binance_funding_episodes.csv", parse_dates=["datetime"])
    fund_ct = pd.read_csv(f"{BASE}/binance_funding_control.csv", parse_dates=["datetime"])
    funding = pd.concat([fund_ep, fund_ct], ignore_index=True)
    funding["datetime"] = pd.to_datetime(funding["datetime"], format="mixed", utc=True).dt.tz_localize(None)
    # Snap to nearest 8h settlement (00/08/16 UTC) to clean up millisecond offsets
    funding["datetime"] = funding["datetime"].dt.round("h")
    funding = funding.sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)

    oi_ep = pd.read_csv(f"{BASE}/bybit_oi_episodes.csv")
    oi_ct = pd.read_csv(f"{BASE}/bybit_oi_control.csv")
    oi = pd.concat([oi_ep, oi_ct], ignore_index=True)
    oi["datetime"] = pd.to_datetime(oi["datetime"], format="mixed", utc=True).dt.tz_localize(None)
    oi = oi.sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)
    oi = oi.set_index("datetime")

    price = pd.read_csv("memories/mev/data/eth_price_1h.csv")
    price["datetime"] = pd.to_datetime(price["datetime"], format="mixed", utc=True).dt.tz_localize(None)
    # Round to nearest hour for clean joins
    price["datetime"] = price["datetime"].dt.round("h")
    price = price.sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)
    price = price.set_index("datetime")

    return funding, oi, price


def assign_bin(rate):
    for label in BIN_LABELS:
        lo, hi = BINS[label]
        if lo <= rate < hi:
            return label
    return BIN_LABELS[-1]


def build_settlement_table(funding, oi, price):
    """For each funding settlement, compute OI and price changes in post windows."""
    rows = []
    for _, row in funding.iterrows():
        t0 = row["datetime"]
        fr = row["funding_rate"]

        # Extract hourly OI for 0..+8h
        hours = [t0 + pd.Timedelta(hours=h) for h in range(HOURS_POST + 1)]
        oi_vals = [oi.loc[h, "open_interest"] if h in oi.index else np.nan for h in hours]

        # Also check pre-settlement: -2h to 0
        pre_hours = [t0 + pd.Timedelta(hours=h) for h in range(-2, 1)]
        pre_oi = [oi.loc[h, "open_interest"] if h in oi.index else np.nan for h in pre_hours]

        # Price at same timestamps
        price_vals = [price.loc[h, "price"] if h in price.index else np.nan for h in hours]

        if np.isnan(oi_vals[0]) or np.isnan(oi_vals[4]):
            continue

        oi_0 = oi_vals[0]
        oi_4 = oi_vals[4]
        oi_8 = oi_vals[8] if not np.isnan(oi_vals[8]) else np.nan

        oi_chg_0_4 = (oi_4 - oi_0) / oi_0 * 100
        oi_chg_4_8 = (oi_8 - oi_4) / oi_4 * 100 if not np.isnan(oi_8) else np.nan

        # Price change
        p0 = price_vals[0] if not np.isnan(price_vals[0]) else np.nan
        p4 = price_vals[4] if not np.isnan(price_vals[4]) else np.nan
        price_chg_0_4 = (p4 - p0) / p0 * 100 if not (np.isnan(p0) or np.isnan(p4)) else np.nan

        # Pre-settlement OI change (-2h to 0)
        pre_oi_chg = np.nan
        if not np.isnan(pre_oi[0]) and not np.isnan(pre_oi[2]):
            pre_oi_chg = (pre_oi[2] - pre_oi[0]) / pre_oi[0] * 100

        # Hour-by-hour OI pct change from t0
        hourly_oi_pct = [(v - oi_0) / oi_0 * 100 if not np.isnan(v) else np.nan for v in oi_vals]

        rec = {
            "datetime": t0,
            "funding_rate": fr,
            "funding_bps": fr * 10000,
            "bin": assign_bin(fr),
            "oi_chg_0_4": oi_chg_0_4,
            "oi_chg_4_8": oi_chg_4_8,
            "price_chg_0_4": price_chg_0_4,
            "pre_oi_chg": pre_oi_chg,
            "price_falling": price_chg_0_4 < 0 if not np.isnan(price_chg_0_4) else None,
        }
        for h in range(HOURS_POST + 1):
            rec[f"oi_h{h}"] = hourly_oi_pct[h]

        rows.append(rec)

    return pd.DataFrame(rows)


def run_stats(df):
    """Compute summary statistics and tests."""
    lines = []
    lines.append("=" * 70)
    lines.append("FUNDING SETTLEMENT → OI CLOSURE CLUSTERING")
    lines.append("=" * 70)

    # --- Bin summary ---
    lines.append("\n## Sample sizes per funding rate bin\n")
    for b in BIN_LABELS:
        sub = df[df["bin"] == b]
        lines.append(f"  {BIN_DISPLAY[b]:>15s}: n={len(sub):4d}  "
                      f"mean_fr={sub['funding_bps'].mean():+.2f}bps  "
                      f"median_fr={sub['funding_bps'].median():+.2f}bps")

    # --- OI change by bin and window ---
    lines.append("\n## OI change (%) by funding bin and time window\n")
    lines.append(f"  {'Bin':>15s} | {'Window':>8s} | {'Mean':>8s} | {'Median':>8s} | {'Std':>8s} | {'N':>4s}")
    lines.append("  " + "-" * 60)
    for b in BIN_LABELS:
        sub = df[df["bin"] == b]
        for window, col in [("0-4h", "oi_chg_0_4"), ("4-8h", "oi_chg_4_8")]:
            vals = sub[col].dropna()
            lines.append(f"  {BIN_DISPLAY[b]:>15s} | {window:>8s} | {vals.mean():+8.4f} | "
                          f"{vals.median():+8.4f} | {vals.std():8.4f} | {len(vals):4d}")

    # --- Pre-settlement OI change ---
    lines.append("\n## Pre-settlement OI change (-2h to 0h) by bin\n")
    for b in BIN_LABELS:
        sub = df[df["bin"] == b]
        vals = sub["pre_oi_chg"].dropna()
        lines.append(f"  {BIN_DISPLAY[b]:>15s}: mean={vals.mean():+.4f}%  median={vals.median():+.4f}%  n={len(vals)}")

    # --- Statistical tests ---
    lines.append("\n## Statistical tests: OI change 0-4h\n")

    neg = df[df["bin"].isin(["deeply_neg", "mod_neg"])]["oi_chg_0_4"].dropna()
    pos = df[df["bin"].isin(["mod_pos", "deeply_pos"])]["oi_chg_0_4"].dropna()
    u_stat, u_p = stats.mannwhitneyu(neg, pos, alternative="less")
    t_stat, t_p = stats.ttest_ind(neg, pos, equal_var=False)
    lines.append(f"  Negative vs Positive funding (all):")
    lines.append(f"    Mann-Whitney U (one-sided, neg < pos): U={u_stat:.1f}, p={u_p:.6f}")
    lines.append(f"    Welch t-test (two-sided): t={t_stat:.3f}, p={t_p:.6f}")
    lines.append(f"    Neg mean={neg.mean():+.4f}%, Pos mean={pos.mean():+.4f}%")

    deep_neg = df[df["bin"] == "deeply_neg"]["oi_chg_0_4"].dropna()
    deep_pos = df[df["bin"] == "deeply_pos"]["oi_chg_0_4"].dropna()
    if len(deep_neg) > 5 and len(deep_pos) > 5:
        u2, p2 = stats.mannwhitneyu(deep_neg, deep_pos, alternative="less")
        lines.append(f"\n  Deeply negative vs Deeply positive:")
        lines.append(f"    Mann-Whitney U (one-sided): U={u2:.1f}, p={p2:.6f}")
        lines.append(f"    Deep neg mean={deep_neg.mean():+.4f}%, Deep pos mean={deep_pos.mean():+.4f}%")

    # --- 0-4h vs 4-8h within deeply negative ---
    lines.append("\n## Within deeply-negative: 0-4h vs 4-8h OI change\n")
    dn = df[df["bin"] == "deeply_neg"]
    w1 = dn["oi_chg_0_4"].dropna()
    w2 = dn["oi_chg_4_8"].dropna()
    if len(w1) > 5 and len(w2) > 5:
        u3, p3 = stats.mannwhitneyu(w1, w2, alternative="less")
        lines.append(f"  0-4h: mean={w1.mean():+.4f}%, median={w1.median():+.4f}%")
        lines.append(f"  4-8h: mean={w2.mean():+.4f}%, median={w2.median():+.4f}%")
        lines.append(f"  Mann-Whitney (0-4h < 4-8h): U={u3:.1f}, p={p3:.6f}")

    # --- Price-conditional analysis ---
    lines.append("\n## Price-conditional: OI change 0-4h when price is falling vs rising\n")
    for b in BIN_LABELS:
        sub = df[df["bin"] == b]
        fall = sub[sub["price_falling"] == True]["oi_chg_0_4"].dropna()
        rise = sub[sub["price_falling"] == False]["oi_chg_0_4"].dropna()
        lines.append(f"  {BIN_DISPLAY[b]:>15s}:  price_falling: mean={fall.mean():+.4f}% (n={len(fall)})  "
                      f"price_rising: mean={rise.mean():+.4f}% (n={len(rise)})")

    # Negative funding + price falling vs negative funding + price rising
    lines.append("\n  Test: negative funding + price falling vs negative funding + price rising")
    neg_fall = df[(df["bin"].isin(["deeply_neg", "mod_neg"])) & (df["price_falling"] == True)]["oi_chg_0_4"].dropna()
    neg_rise = df[(df["bin"].isin(["deeply_neg", "mod_neg"])) & (df["price_falling"] == False)]["oi_chg_0_4"].dropna()
    if len(neg_fall) > 5 and len(neg_rise) > 5:
        u4, p4 = stats.mannwhitneyu(neg_fall, neg_rise, alternative="less")
        lines.append(f"    Neg+falling: mean={neg_fall.mean():+.4f}% (n={len(neg_fall)})")
        lines.append(f"    Neg+rising:  mean={neg_rise.mean():+.4f}% (n={len(neg_rise)})")
        lines.append(f"    Mann-Whitney (falling < rising): U={u4:.1f}, p={p4:.6f}")

    # Bonus: does funding add signal beyond price?
    lines.append("\n  Test: negative funding + price falling vs POSITIVE funding + price falling")
    pos_fall = df[(df["bin"].isin(["mod_pos", "deeply_pos"])) & (df["price_falling"] == True)]["oi_chg_0_4"].dropna()
    if len(neg_fall) > 5 and len(pos_fall) > 5:
        u5, p5 = stats.mannwhitneyu(neg_fall, pos_fall, alternative="less")
        lines.append(f"    Neg+falling: mean={neg_fall.mean():+.4f}% (n={len(neg_fall)})")
        lines.append(f"    Pos+falling: mean={pos_fall.mean():+.4f}% (n={len(pos_fall)})")
        lines.append(f"    Mann-Whitney: U={u5:.1f}, p={p5:.6f}")
        lines.append(f"    → If significant: funding adds signal beyond price movement alone")

    # --- Summary ---
    lines.append("\n" + "=" * 70)
    lines.append("SUMMARY")
    lines.append("=" * 70)

    return "\n".join(lines)


def plot_boxplot(df):
    """Box plot of OI change (0-4h) by funding rate bin."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: 0-4h window by bin
    data_04 = [df[df["bin"] == b]["oi_chg_0_4"].dropna().values for b in BIN_LABELS]
    labels = [BIN_DISPLAY[b] for b in BIN_LABELS]

    bp = axes[0].boxplot(data_04, tick_labels=labels, patch_artist=True, showfliers=True,
                          flierprops=dict(marker='.', markersize=3, alpha=0.3))
    colors = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    axes[0].axhline(0, color="gray", linestyle="--", alpha=0.5)
    axes[0].set_ylabel("OI Change (%)")
    axes[0].set_title("OI Change 0-4h After Funding Settlement")
    axes[0].set_xlabel("Funding Rate Bin")
    # Add sample sizes
    for i, b in enumerate(BIN_LABELS):
        n = len(df[df["bin"] == b]["oi_chg_0_4"].dropna())
        axes[0].text(i + 1, axes[0].get_ylim()[0], f"n={n}", ha="center", va="bottom", fontsize=8)

    # Right: 0-4h vs 4-8h for deeply negative
    dn = df[df["bin"] == "deeply_neg"]
    data_compare = [dn["oi_chg_0_4"].dropna().values, dn["oi_chg_4_8"].dropna().values]
    bp2 = axes[1].boxplot(data_compare, tick_labels=["0-4h post", "4-8h post"], patch_artist=True,
                           flierprops=dict(marker='.', markersize=3, alpha=0.3))
    bp2["boxes"][0].set_facecolor("#d62728")
    bp2["boxes"][0].set_alpha(0.6)
    bp2["boxes"][1].set_facecolor("#aaaaaa")
    bp2["boxes"][1].set_alpha(0.6)
    axes[1].axhline(0, color="gray", linestyle="--", alpha=0.5)
    axes[1].set_ylabel("OI Change (%)")
    axes[1].set_title("Deeply Negative Funding: 0-4h vs 4-8h")

    plt.tight_layout()
    plt.savefig(f"{OUT}/funding_oi_clustering.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/funding_oi_clustering.png")


def plot_time_profile(df):
    """Hour-by-hour OI change profile after settlement, by funding bin."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    hours = list(range(HOURS_POST + 1))
    colors_map = {
        "deeply_neg": "#d62728",
        "mod_neg": "#ff7f0e",
        "mod_pos": "#2ca02c",
        "deeply_pos": "#1f77b4",
    }

    # Left: All bins
    for b in BIN_LABELS:
        sub = df[df["bin"] == b]
        means = [sub[f"oi_h{h}"].mean() for h in hours]
        sems = [sub[f"oi_h{h}"].sem() for h in hours]
        axes[0].plot(hours, means, marker="o", markersize=4, label=f"{BIN_DISPLAY[b]} (n={len(sub)})",
                     color=colors_map[b], linewidth=2)
        axes[0].fill_between(hours,
                              [m - s for m, s in zip(means, sems)],
                              [m + s for m, s in zip(means, sems)],
                              alpha=0.15, color=colors_map[b])

    axes[0].axhline(0, color="gray", linestyle="--", alpha=0.5)
    axes[0].axvline(4, color="gray", linestyle=":", alpha=0.5, label="4h mark")
    axes[0].set_xlabel("Hours After Settlement")
    axes[0].set_ylabel("Cumulative OI Change from Settlement (%)")
    axes[0].set_title("OI Profile After Funding Settlement")
    axes[0].legend(fontsize=8)
    axes[0].set_xticks(hours)

    # Right: Deeply negative, split by price falling/rising
    dn = df[df["bin"] == "deeply_neg"]
    for cond, label, color in [(True, "Price Falling", "#d62728"), (False, "Price Rising", "#2ca02c")]:
        sub = dn[dn["price_falling"] == cond]
        if len(sub) < 3:
            continue
        means = [sub[f"oi_h{h}"].mean() for h in hours]
        sems = [sub[f"oi_h{h}"].sem() for h in hours]
        axes[1].plot(hours, means, marker="o", markersize=4, label=f"{label} (n={len(sub)})",
                     color=color, linewidth=2)
        axes[1].fill_between(hours,
                              [m - s for m, s in zip(means, sems)],
                              [m + s for m, s in zip(means, sems)],
                              alpha=0.15, color=color)

    axes[1].axhline(0, color="gray", linestyle="--", alpha=0.5)
    axes[1].axvline(4, color="gray", linestyle=":", alpha=0.5)
    axes[1].set_xlabel("Hours After Settlement")
    axes[1].set_ylabel("Cumulative OI Change from Settlement (%)")
    axes[1].set_title("Deeply Negative Funding: Price-Conditional")
    axes[1].legend(fontsize=8)
    axes[1].set_xticks(hours)

    plt.tight_layout()
    plt.savefig(f"{OUT}/funding_oi_timeprofile.png", dpi=150)
    plt.close()
    print(f"Saved {OUT}/funding_oi_timeprofile.png")


def main():
    funding, oi, price = load_data()
    print(f"Funding settlements: {len(funding)}")
    print(f"OI hourly rows: {len(oi)}")
    print(f"Price hourly rows: {len(price)}")
    print(f"Funding date range: {funding['datetime'].min()} to {funding['datetime'].max()}")
    print(f"OI date range: {oi.index.min()} to {oi.index.max()}")

    df = build_settlement_table(funding, oi, price)
    print(f"Matched settlements: {len(df)}")

    results = run_stats(df)
    print(results)

    # Append summary interpretation
    # Check the key results to write a summary
    neg = df[df["bin"].isin(["deeply_neg", "mod_neg"])]["oi_chg_0_4"].dropna()
    pos = df[df["bin"].isin(["mod_pos", "deeply_pos"])]["oi_chg_0_4"].dropna()
    deep_neg = df[df["bin"] == "deeply_neg"]

    summary_lines = []
    if neg.mean() < pos.mean():
        diff = pos.mean() - neg.mean()
        summary_lines.append(f"OI change in 0-4h is more negative after negative funding than positive funding "
                              f"(diff={diff:.4f}pp).")
    else:
        summary_lines.append("No evidence that OI drops more after negative funding than positive.")

    dn_04 = deep_neg["oi_chg_0_4"].dropna()
    dn_48 = deep_neg["oi_chg_4_8"].dropna()
    if len(dn_04) > 0 and len(dn_48) > 0:
        if dn_04.mean() < dn_48.mean():
            summary_lines.append(f"After deeply negative funding, closures are front-loaded: "
                                  f"0-4h mean={dn_04.mean():+.4f}% vs 4-8h mean={dn_48.mean():+.4f}%.")
        else:
            summary_lines.append(f"After deeply negative funding, closures are NOT front-loaded: "
                                  f"0-4h mean={dn_04.mean():+.4f}% vs 4-8h mean={dn_48.mean():+.4f}%.")

    pre = deep_neg["pre_oi_chg"].dropna()
    if len(pre) > 0:
        summary_lines.append(f"Pre-settlement (-2h to 0h) OI change for deeply negative: "
                              f"mean={pre.mean():+.4f}% — {'suggests preemptive closing' if pre.mean() < 0 else 'no preemptive closing signal'}.")

    results += "\n" + "\n".join(summary_lines) + "\n"

    with open(f"{OUT}/funding_oi_results.txt", "w") as f:
        f.write(results)
    print(f"\nSaved {OUT}/funding_oi_results.txt")

    plot_boxplot(df)
    plot_time_profile(df)


if __name__ == "__main__":
    main()
