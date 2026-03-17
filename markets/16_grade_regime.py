"""
Grade 16: Regime model validation on simulator datalogs.

Validates: trend magnitudes, topology, episode stats, exit AUC, calibration.
Compares jump chain to OOS reference (Phase 12, BTC 2023-2024).

Discovery: simulator computes OLS trends with 30-second subsampling (960 points
over 8h), giving slope-per-30s-index / mean_price. Research data (downloaded 5-min
bars) used slope-per-5min-index / mean_price — a factor of 10x larger. All trend
magnitudes in simulator data are 10x smaller than research convention.

For regime detection: sign-based → scale-invariant, no impact.
For exit scoring: production coefficients need trend_8h/trend_1h scaled by 10x.
"""

import sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

# ─── CONFIG ───
IS_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
FWD_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2026-02-20_2026-03-13.csv'

SUBSAMPLE = 300  # 1s → 5min

# Scale factor: simulator 30s-index convention vs research 5min-bar convention
# simulator_trend × SCALE = research_trend
SCALE_FACTOR = 10.0

# Production logistic coefficients (Phase 13, in research/5min-bar units)
# P = σ(b0 + b1 × trend_1h + b8 × trend_8h)
# For simulator units: multiply feature coefficients by SCALE_FACTOR
C2_COEFS_RESEARCH = (5.209, 1477.0, 348533.0)
C1_COEFS_RESEARCH = (-4.890, 3138.0, 421505.0)

# Adjusted for simulator units: same logit, trends are 10x smaller
# σ(b0 + b1*t1h_research + b8*t8h_research) = σ(b0 + b1*10*t1h_sim + b8*10*t8h_sim)
C2_COEFS_SIM = (C2_COEFS_RESEARCH[0],
                C2_COEFS_RESEARCH[1] * SCALE_FACTOR,
                C2_COEFS_RESEARCH[2] * SCALE_FACTOR)
C1_COEFS_SIM = (C1_COEFS_RESEARCH[0],
                C1_COEFS_RESEARCH[1] * SCALE_FACTOR,
                C1_COEFS_RESEARCH[2] * SCALE_FACTOR)

# OOS reference jump chain (Phase 12, BTC 2023-2024, 2947 episodes)
REF_JUMP = np.array([
    [0.0000, 0.9336, 0.0635, 0.0029],
    [0.7798, 0.0000, 0.0000, 0.2202],
    [0.1875, 0.0000, 0.0000, 0.8125],
    [0.0000, 0.0743, 0.9257, 0.0000],
])

REGIME_NAMES = ['C0(bear)', 'C1(rev)', 'C2(pull)', 'C3(bull)']
FORBIDDEN = [(0, 3), (3, 0), (1, 2), (2, 1)]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def load_subsample(path, every=SUBSAMPLE):
    """Load only needed columns, subsample to 5-min."""
    df = pd.read_csv(path, usecols=[0, 2, 32, 34, 37],
                     names=['timestamp', 'price', 'trend_1h', 'trend_8h', 'trend_48h'],
                     header=0)
    df = df.iloc[::every].reset_index(drop=True)
    return df


def assign_regime(df):
    """2-bit regime: sign(trend_8h) × sign(trend_48h). Zero treated as positive."""
    b8 = (df['trend_8h'] >= 0).astype(int)
    b48 = (df['trend_48h'] >= 0).astype(int)
    df['regime'] = b8 + 2 * b48
    return df


def detect_episodes(df):
    """Detect regime episodes with flicker debounce.

    Debounce only A→B(1-bar)→A patterns (flicker back to same regime).
    Preserve A→B(1-bar)→C where C≠A (genuine transit through B).
    """
    regime = df['regime'].values
    n = len(regime)

    # Detect raw episodes
    changes = np.where(np.diff(regime) != 0)[0] + 1
    starts = np.concatenate([[0], changes])
    ends = np.concatenate([changes, [n]])
    raw_regimes = regime[starts]
    raw_durations = ends - starts

    # Flicker debounce: absorb 1-bar A→B→A back into A
    kept_idx = list(range(len(starts)))
    changed = True
    while changed:
        changed = False
        new_kept = []
        i = 0
        while i < len(kept_idx):
            idx = kept_idx[i]
            # Check if this is a 1-bar flicker: same regime before and after
            if (raw_durations[idx] == 1
                    and i > 0 and i < len(kept_idx) - 1):
                prev_r = raw_regimes[kept_idx[i - 1]]
                next_r = raw_regimes[kept_idx[i + 1]]
                if prev_r == next_r:
                    # Flicker: skip this episode, merge prev and next
                    changed = True
                    i += 1
                    continue
            new_kept.append(idx)
            i += 1
        kept_idx = new_kept

    # Merge consecutive same-regime episodes (from flicker absorption)
    merged = []
    for idx in kept_idx:
        r = raw_regimes[idx]
        if merged and merged[-1][1] == r:
            continue  # will be merged by end computation
        merged.append((starts[idx], r))

    # Build episode dataframe
    ep_data = []
    for k in range(len(merged)):
        s, r = merged[k]
        e = merged[k + 1][0] if k + 1 < len(merged) else n
        ep_data.append({
            'regime': r,
            'start': s,
            'end': e,
            'duration_bars': e - s,
            'trend_1h_last': df['trend_1h'].iloc[e - 1],
            'trend_8h_last': df['trend_8h'].iloc[e - 1],
        })

    return pd.DataFrame(ep_data)


def gate0_trend_divergence(df):
    """Verify simulator trends match OLS recomputation (with 30s-index convention)."""
    print("=" * 70)
    print("  GATE 0: Trend Divergence Check")
    print("=" * 70)
    print("  (Recomputing OLS on 5-min bars, dividing by 10 for 30s-index convention)")

    WARMUP = 96  # 8h of 5-min bars
    valid = df.iloc[WARMUP:]
    n_samples = min(1000, len(valid))
    indices = np.linspace(0, len(valid) - 1, n_samples, dtype=int)

    divergences = []
    for idx in indices:
        actual_idx = WARMUP + idx
        window = df['price'].iloc[actual_idx - 96 + 1:actual_idx + 1].values
        if len(window) < 96:
            continue
        mean_price = window.mean()
        x = np.arange(len(window))
        slope_per_bar = np.polyfit(x, window, 1)[0]
        # Convert to simulator's 30s-index convention: ÷10
        recomputed = slope_per_bar / SCALE_FACTOR / mean_price
        native = df['trend_8h'].iloc[actual_idx]

        if abs(recomputed) > 1e-12:
            div = abs(native - recomputed) / abs(recomputed)
            divergences.append(div)

    divergences = np.array(divergences)
    med = np.median(divergences)
    p95 = np.percentile(divergences, 95)
    mx = np.max(divergences)

    print(f"  Samples: {len(divergences)}")
    print(f"  Median divergence: {med:.4%}")
    print(f"  P95 divergence:    {p95:.4%}")
    print(f"  Max divergence:    {mx:.4%}")

    if med < 0.05:
        print(f"  → PASS (median {med:.4%} < 5%)")
        return True
    elif med < 0.10:
        print(f"  → WARN (median {med:.4%} between 5-10%)")
        return True
    else:
        print(f"  → HALT (median {med:.4%} > 10%)")
        return False


def check_trend_magnitudes(df, label):
    """Report trend magnitudes. Simulator uses 30s-index convention (~1e-5 std)."""
    print()
    print("─" * 60)
    print(f"  Trend Magnitudes ({label})")
    print("─" * 60)

    for col in ['trend_1h', 'trend_8h', 'trend_48h']:
        s = df[col]
        print(f"  {col:>12s}: mean={s.mean():.2e}, std={s.std():.2e}, "
              f"p5={s.quantile(0.05):.2e}, p95={s.quantile(0.95):.2e}")

    std_8h = df['trend_8h'].std()
    # Simulator uses 30s subsampling → std ~1.5e-5 (= research ~1.5e-4 / 10)
    research_equiv = std_8h * SCALE_FACTOR
    print(f"\n  trend_8h std (simulator):  {std_8h:.2e}")
    print(f"  trend_8h std (×10 = research equiv): {research_equiv:.2e}")

    if 5e-5 < research_equiv < 5e-4:
        print(f"  → PASS (research-equiv {research_equiv:.2e} ~ 1e-4)")
    else:
        print(f"  → FAIL (research-equiv {research_equiv:.2e}, expected ~1e-4)")


def check_topology(episodes, label):
    """Check for forbidden transitions."""
    print()
    print("─" * 60)
    print(f"  Check 1: Topology Violations ({label})")
    print("─" * 60)

    violations = 0
    details = []
    for i in range(len(episodes) - 1):
        src = episodes['regime'].iloc[i]
        dst = episodes['regime'].iloc[i + 1]
        if (src, dst) in FORBIDDEN:
            violations += 1
            details.append(f"    ep {i}: {REGIME_NAMES[src]} → {REGIME_NAMES[dst]}")

    if violations == 0:
        print(f"  → PASS (0 violations)")
    else:
        print(f"  → FAIL ({violations} violations)")
        for d in details[:10]:
            print(d)
    return violations


def check_episodes(episodes, label, n_days):
    """Episode count and duration stats."""
    print()
    print("─" * 60)
    print(f"  Check 2: Episode Statistics ({label}, ~{n_days} days)")
    print("─" * 60)

    n_ep = len(episodes)
    dur_h = episodes['duration_bars'] * 5 / 60
    mean_dur = dur_h.mean()

    print(f"  Total episodes: {n_ep}")
    print(f"  Mean duration:  {mean_dur:.2f}h")
    print(f"  Median duration: {dur_h.median():.2f}h")
    print()

    for r in range(4):
        sub = episodes[episodes['regime'] == r]
        if len(sub) > 0:
            d = sub['duration_bars'] * 5 / 60
            print(f"    {REGIME_NAMES[r]:>12s}: n={len(sub):>4d}, "
                  f"mean={d.mean():.2f}h, med={d.median():.2f}h, std={d.std():.2f}h")

    if n_days > 100:
        ep_pass = 400 <= n_ep <= 1200
        dur_pass = 3 <= mean_dur <= 12
        ok = ep_pass and dur_pass
        verdicts = []
        if not ep_pass:
            verdicts.append(f"count {n_ep} outside [400,1200]")
        if not dur_pass:
            verdicts.append(f"mean_dur {mean_dur:.1f}h outside [3,12]")
        if ok:
            print(f"\n  → PASS (n={n_ep}, mean_dur={mean_dur:.1f}h)")
        else:
            print(f"\n  → FAIL ({'; '.join(verdicts)})")
        return ok
    else:
        print(f"\n  (forward: no hard threshold, informational only)")
        return True


def check_jump_chain(episodes, label):
    """Build and compare jump chain to reference."""
    print()
    print("─" * 60)
    print(f"  Check 3: Transition Matrix ({label})")
    print("─" * 60)

    count = np.zeros((4, 4), dtype=int)
    for i in range(len(episodes) - 1):
        src = episodes['regime'].iloc[i]
        dst = episodes['regime'].iloc[i + 1]
        count[src, dst] += 1

    row_sums = count.sum(axis=1, keepdims=True).astype(float)
    row_sums[row_sums == 0] = 1
    jump = count / row_sums

    print(f"\n  Count matrix:")
    print(f"    {'':>12s}  " + "  ".join(f"{REGIME_NAMES[j]:>10s}" for j in range(4)))
    for i in range(4):
        print(f"    {REGIME_NAMES[i]:>12s}  " + "  ".join(f"{count[i, j]:>10d}" for j in range(4)))

    print(f"\n  Jump chain (row-normalized):")
    print(f"    {'':>12s}  " + "  ".join(f"{REGIME_NAMES[j]:>10s}" for j in range(4)))
    for i in range(4):
        print(f"    {REGIME_NAMES[i]:>12s}  " + "  ".join(f"{jump[i, j]:>10.4f}" for j in range(4)))

    frob = np.linalg.norm(jump - REF_JUMP)
    print(f"\n  OOS reference (Phase 12, BTC 2023-2024):")
    print(f"    {'':>12s}  " + "  ".join(f"{REGIME_NAMES[j]:>10s}" for j in range(4)))
    for i in range(4):
        print(f"    {REGIME_NAMES[i]:>12s}  " + "  ".join(f"{REF_JUMP[i, j]:>10.4f}" for j in range(4)))

    print(f"\n  Frobenius distance vs reference: {frob:.4f}")
    if frob < 0.1:
        print(f"  → PASS (Frobenius {frob:.4f} < 0.1)")
    else:
        print(f"  → FAIL (Frobenius {frob:.4f} >= 0.1)")

    return jump, frob < 0.1


def get_exits(episodes, regime, target_regime):
    """Extract exit events for a given regime → target transition."""
    ep = episodes[episodes['regime'] == regime].copy()
    idx = ep.index
    next_reg = []
    for i in idx:
        pos = episodes.index.get_loc(i)
        if pos + 1 < len(episodes):
            next_reg.append(episodes['regime'].iloc[pos + 1])
        else:
            next_reg.append(np.nan)
    ep = ep.copy()
    ep['next_regime'] = next_reg
    ep = ep.dropna(subset=['next_regime'])
    ep['next_regime'] = ep['next_regime'].astype(int)
    exits = ep[ep['next_regime'].isin([0, target_regime])].copy()
    return exits


def check_exit_auc(episodes, label):
    """Exit AUC using production logistic (adjusted to simulator units)."""
    print()
    print("─" * 60)
    print(f"  Check 4: Exit AUC ({label})")
    print("─" * 60)
    print(f"  (Coefficients scaled ×{SCALE_FACTOR:.0f} for simulator 30s-index units)")

    results = {}
    for regime, coefs, target_regime, model_label in [
        (2, C2_COEFS_SIM, 3, "C2 Pullback → P(bull)"),
        (1, C1_COEFS_SIM, 3, "C1 Reversal → P(breakthrough)"),
    ]:
        exits = get_exits(episodes, regime, target_regime)
        if len(exits) < 5:
            print(f"\n  {model_label}: too few exits ({len(exits)}), skipping")
            results[regime] = (np.nan, len(exits))
            continue

        y = (exits['next_regime'] == target_regime).astype(int)
        b0, b1, b8 = coefs
        logit = b0 + b1 * exits['trend_1h_last'].values + b8 * exits['trend_8h_last'].values
        pred = sigmoid(logit)

        auc = roc_auc_score(y, pred) if y.nunique() > 1 else float('nan')

        print(f"\n  {model_label}:")
        print(f"    Exits: {len(exits)} (positive={y.sum()}, negative={len(exits)-y.sum()})")
        if not np.isnan(auc):
            print(f"    AUC: {auc:.4f}")
            if auc > 0.90:
                print(f"    → PASS (AUC {auc:.4f} > 0.90)")
            elif auc > 0.85:
                print(f"    → WARN (AUC {auc:.4f} in [0.85, 0.90])")
            else:
                print(f"    → FAIL (AUC {auc:.4f} < 0.85)")
        else:
            print(f"    AUC: N/A (single class)")

        results[regime] = (auc, len(exits))

    return results


def check_calibration(episodes, label):
    """Calibration of exit predictions (simulator-unit coefficients)."""
    print()
    print("─" * 60)
    print(f"  Check 5: Calibration ({label})")
    print("─" * 60)

    bins = [(0, 0.10), (0.10, 0.50), (0.50, 0.90), (0.90, 1.01)]

    for regime, coefs, target_regime, model_label in [
        (2, C2_COEFS_SIM, 3, "C2 Pullback → P(bull)"),
        (1, C1_COEFS_SIM, 3, "C1 Reversal → P(bt)"),
    ]:
        exits = get_exits(episodes, regime, target_regime)
        if len(exits) < 5:
            print(f"\n  {model_label}: too few exits, skipping")
            continue

        y = (exits['next_regime'] == target_regime).astype(int).values
        b0, b1, b8 = coefs
        logit = b0 + b1 * exits['trend_1h_last'].values + b8 * exits['trend_8h_last'].values
        pred = sigmoid(logit)

        print(f"\n  {model_label} ({len(exits)} exits):")
        print(f"    {'Bin':>14s}  {'n':>5s}  {'pred_mean':>9s}  {'actual':>8s}  {'gap':>8s}")

        extreme_n = 0
        total_n = 0
        cal_ok = True
        for lo, hi in bins:
            mask = (pred >= lo) & (pred < hi)
            n = mask.sum()
            total_n += n
            if n > 0:
                pm = pred[mask].mean()
                act = y[mask].mean()
                gap = act - pm
                is_extreme = (lo < 0.101) or (lo >= 0.899)
                if is_extreme:
                    extreme_n += n
                marker = ""
                if is_extreme and abs(gap) > 0.15:
                    marker = " ← FAIL"
                    cal_ok = False
                elif is_extreme and abs(gap) > 0.10:
                    marker = " ← WARN"
                print(f"    [{lo:.2f},{hi:.2f})  {n:>5d}  {pm:>9.4f}  {act:>8.4f}  {gap:>+8.4f}{marker}")
            else:
                print(f"    [{lo:.2f},{hi:.2f})  {0:>5d}      -         -       -")

        extreme_pct = extreme_n / total_n if total_n > 0 else 0
        print(f"\n    Bimodal: {extreme_pct:.1%} in extreme bins (<0.10 or >0.90)")
        if extreme_pct > 0.90:
            print(f"    → PASS (bimodal {extreme_pct:.1%} > 90%)")
        elif extreme_pct > 0.85:
            print(f"    → WARN (bimodal {extreme_pct:.1%})")
        else:
            print(f"    → FAIL (bimodal {extreme_pct:.1%} < 85%)")


def grade_dataset(path, label, n_days):
    """Full grading pipeline for one dataset."""
    print()
    print("=" * 70)
    print(f"  GRADING: {label}")
    print(f"  File: {path}")
    print("=" * 70)

    df = load_subsample(path)
    print(f"  Loaded: {len(df)} bars (5-min), price {df['price'].min():.0f}–{df['price'].max():.0f}")

    verdicts = {}

    # Trend magnitudes
    check_trend_magnitudes(df, label)

    # Gate 0
    gate0_ok = gate0_trend_divergence(df)
    verdicts['gate0'] = gate0_ok
    if not gate0_ok:
        print("\n  *** GATE 0 FAILED — halting further checks ***")
        return verdicts

    # Regime assignment
    assign_regime(df)
    episodes = detect_episodes(df)
    print(f"\n  Episodes detected: {len(episodes)}")

    # Check 1: Topology
    violations = check_topology(episodes, label)
    verdicts['topology'] = violations == 0

    # Check 2: Episode stats
    verdicts['episodes'] = check_episodes(episodes, label, n_days)

    # Check 3: Jump chain
    _, verdicts['jump_chain'] = check_jump_chain(episodes, label)

    # Check 4: Exit AUC
    auc_results = check_exit_auc(episodes, label)
    verdicts['exit_auc'] = all(
        auc > 0.85 for auc, n in auc_results.values()
        if not np.isnan(auc) and n >= 5
    )

    # Check 5: Calibration
    check_calibration(episodes, label)

    return verdicts


def main():
    print("=" * 70)
    print("  SCALE FACTOR DISCOVERY")
    print("=" * 70)
    print(f"  Simulator OLS: 30-second subsampling (960 pts over 8h)")
    print(f"  Research OLS:  5-minute bars (96 pts over 8h)")
    print(f"  Scale factor:  ×{SCALE_FACTOR:.0f} (simulator × 10 = research units)")
    print(f"  Impact: regime detection (sign-based) unaffected.")
    print(f"          exit coefficients rescaled: b_sim = b_research × {SCALE_FACTOR:.0f}")

    all_verdicts = {}

    is_verdicts = grade_dataset(IS_FILE, "BTC IS (Jul 2025 – Feb 2026)", n_days=214)
    all_verdicts['IS'] = is_verdicts

    fwd_verdicts = grade_dataset(FWD_FILE, "BTC Forward (Feb 20 – Mar 13, 2026)", n_days=21)
    all_verdicts['Forward'] = fwd_verdicts

    # Final summary
    print()
    print("=" * 70)
    print("  FINAL SUMMARY")
    print("=" * 70)

    overall = True
    for dataset, verdicts in all_verdicts.items():
        print(f"\n  {dataset}:")
        for check, passed in verdicts.items():
            status = "PASS" if passed else "FAIL"
            print(f"    {check:>15s}: {status}")
            if not passed and dataset == 'IS':
                overall = False

    print(f"\n  Overall: {'PASS' if overall else 'FAIL'}")
    print("=" * 70)


if __name__ == '__main__':
    main()
