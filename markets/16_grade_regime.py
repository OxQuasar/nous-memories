"""
Grade 16: Regime model validation on simulator datalogs.

Validates: trend magnitudes, topology, episode stats, exit AUC, calibration.
Compares jump chain to OOS reference (Phase 12, BTC 2023-2024).
"""

import sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

# ─── CONFIG ───
IS_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
FWD_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2026-02-20_2026-03-13.csv'

SUBSAMPLE = 300  # 1s → 5min

# Production logistic coefficients (Phase 13)
C2_COEFS = (5.209, 1477.0, 348533.0)   # intercept, trend_1h, trend_8h
C1_COEFS = (-4.890, 3138.0, 421505.0)  # intercept, trend_1h, trend_8h

# OOS reference jump chain (Phase 12, BTC 2023-2024, 2947 episodes)
REF_JUMP = np.array([
    [0.0000, 0.9336, 0.0635, 0.0029],
    [0.7798, 0.0000, 0.0000, 0.2202],
    [0.1875, 0.0000, 0.0000, 0.8125],
    [0.0000, 0.0743, 0.9257, 0.0000],
])

REGIME_NAMES = ['C0(bear)', 'C1(rev)', 'C2(pull)', 'C3(bull)']

# Forbidden transitions (topology violations)
FORBIDDEN = [(0, 3), (3, 0), (1, 2), (2, 1)]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def load_subsample(path, every=SUBSAMPLE):
    """Load only needed columns, subsample to 5-min."""
    cols = ['price', 'trend_1h', 'trend_8h', 'trend_48h']
    # Use column indices (0-based): 2, 32, 34, 37
    df = pd.read_csv(path, usecols=[0, 2, 32, 34, 37],
                     names=['timestamp', 'price', 'trend_1h', 'trend_8h', 'trend_48h'],
                     header=0)
    df = df.iloc[::every].reset_index(drop=True)
    return df


def assign_regime(df):
    """2-bit regime: sign(trend_8h) × sign(trend_48h)."""
    b8 = (df['trend_8h'] >= 0).astype(int)
    b48 = (df['trend_48h'] >= 0).astype(int)
    df['regime'] = b8 + 2 * b48
    # 0=bear(both neg), 1=rev(8h+,48h-), 2=pull(8h-,48h+), 3=bull(both pos)
    return df


def detect_episodes(df):
    """Detect regime episodes with 1-bar debounce."""
    regime = df['regime'].values
    n = len(regime)

    # Raw episode detection
    changes = np.where(np.diff(regime) != 0)[0] + 1
    starts = np.concatenate([[0], changes])
    ends = np.concatenate([changes, [n]])
    durations = ends - starts

    # Debounce: merge 1-bar episodes into previous
    merged_starts = []
    merged_regimes = []
    i = 0
    while i < len(starts):
        s = starts[i]
        r = regime[s]
        # Skip forward through 1-bar episodes that follow
        j = i + 1
        while j < len(starts) and durations[j] == 1:
            j += 1
        if durations[i] == 1 and merged_regimes:
            # This 1-bar episode gets absorbed into previous
            i = j
            continue
        merged_starts.append(s)
        merged_regimes.append(r)
        i += 1 if durations[i] > 1 else j

    # Rebuild episodes from merged
    ep_data = []
    for k in range(len(merged_starts)):
        s = merged_starts[k]
        e = merged_starts[k + 1] if k + 1 < len(merged_starts) else n
        r = merged_regimes[k]
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
    """Verify simulator trends match OLS recomputation."""
    print("=" * 70)
    print("  GATE 0: Trend Divergence Check")
    print("=" * 70)

    # Skip first 8h warmup (96 bars at 5-min)
    WARMUP = 96
    valid = df.iloc[WARMUP:]
    n_samples = min(1000, len(valid))
    indices = np.linspace(0, len(valid) - 1, n_samples, dtype=int)

    divergences = []
    for idx in indices:
        actual_idx = WARMUP + idx
        if actual_idx < WARMUP:
            continue
        window = df['price'].iloc[actual_idx - 96 + 1:actual_idx + 1].values
        if len(window) < 96:
            continue
        mean_price = window.mean()
        x = np.arange(len(window))
        slope = np.polyfit(x, window, 1)[0]
        recomputed = slope / mean_price
        native = df['trend_8h'].iloc[actual_idx]

        if abs(recomputed) > 1e-10:
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
    """Verify trend_8h std is ~1e-4."""
    print()
    print("─" * 60)
    print(f"  Trend Magnitudes ({label})")
    print("─" * 60)

    for col in ['trend_1h', 'trend_8h', 'trend_48h']:
        s = df[col]
        print(f"  {col:>12s}: mean={s.mean():.2e}, std={s.std():.2e}, "
              f"p5={s.quantile(0.05):.2e}, p95={s.quantile(0.95):.2e}")

    std_8h = df['trend_8h'].std()
    if 5e-5 < std_8h < 5e-4:
        print(f"  → PASS (trend_8h std = {std_8h:.2e}, expected ~1e-4)")
    else:
        print(f"  → FAIL (trend_8h std = {std_8h:.2e}, expected ~1e-4)")


def check_topology(episodes, label):
    """Check for forbidden transitions."""
    print()
    print("─" * 60)
    print(f"  Check 1: Topology Violations ({label})")
    print("─" * 60)

    violations = 0
    for i in range(len(episodes) - 1):
        src = episodes['regime'].iloc[i]
        dst = episodes['regime'].iloc[i + 1]
        if (src, dst) in FORBIDDEN:
            violations += 1

    if violations == 0:
        print(f"  → PASS (0 violations)")
    else:
        print(f"  → FAIL ({violations} violations)")
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

    if n_days > 100:  # IS thresholds
        ep_pass = 400 <= n_ep <= 1200
        dur_pass = 3 <= mean_dur <= 12
        ok = ep_pass and dur_pass
        verdicts = []
        if not ep_pass:
            verdicts.append(f"count {n_ep} outside [400,1200]")
        if not dur_pass:
            verdicts.append(f"mean_dur {mean_dur:.1f}h outside [3,12]")
        if ok:
            print(f"  → PASS (n={n_ep}, mean_dur={mean_dur:.1f}h)")
        else:
            print(f"  → FAIL ({'; '.join(verdicts)})")
        return ok
    else:
        print(f"  (forward: no hard threshold, informational only)")
        return True


def check_jump_chain(episodes, label):
    """Build and compare jump chain to reference."""
    print()
    print("─" * 60)
    print(f"  Check 3: Transition Matrix ({label})")
    print("─" * 60)

    # Count matrix (exclude self-transitions by construction — episodes are contiguous same-regime)
    count = np.zeros((4, 4), dtype=int)
    for i in range(len(episodes) - 1):
        src = episodes['regime'].iloc[i]
        dst = episodes['regime'].iloc[i + 1]
        count[src, dst] += 1

    # Row-normalize
    row_sums = count.sum(axis=1, keepdims=True).astype(float)
    row_sums[row_sums == 0] = 1  # avoid div by zero
    jump = count / row_sums

    # Print
    print(f"\n  Count matrix:")
    print(f"    {'':>12s}  " + "  ".join(f"{REGIME_NAMES[j]:>10s}" for j in range(4)))
    for i in range(4):
        print(f"    {REGIME_NAMES[i]:>12s}  " + "  ".join(f"{count[i, j]:>10d}" for j in range(4)))

    print(f"\n  Jump chain (row-normalized):")
    print(f"    {'':>12s}  " + "  ".join(f"{REGIME_NAMES[j]:>10s}" for j in range(4)))
    for i in range(4):
        print(f"    {REGIME_NAMES[i]:>12s}  " + "  ".join(f"{jump[i, j]:>10.4f}" for j in range(4)))

    # Frobenius vs reference
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


def check_exit_auc(episodes, label):
    """Exit AUC for C2 and C1 using production logistic coefficients."""
    print()
    print("─" * 60)
    print(f"  Check 4: Exit AUC ({label})")
    print("─" * 60)

    results = {}
    for regime, coefs, target_regime, model_label in [
        (2, C2_COEFS, 3, "C2 Pullback → P(bull)"),
        (1, C1_COEFS, 3, "C1 Reversal → P(breakthrough)"),
    ]:
        ep = episodes[episodes['regime'] == regime].copy()
        # Need next regime
        idx = ep.index
        next_reg = []
        for i in idx:
            pos = episodes.index.get_loc(i)
            if pos + 1 < len(episodes):
                next_reg.append(episodes['regime'].iloc[pos + 1])
            else:
                next_reg.append(np.nan)
        ep['next_regime'] = next_reg
        ep = ep.dropna(subset=['next_regime'])
        ep['next_regime'] = ep['next_regime'].astype(int)

        # Filter to exits that go to C0 or C3
        exits = ep[ep['next_regime'].isin([0, 3])].copy()
        if len(exits) < 5:
            print(f"\n  {model_label}: too few exits ({len(exits)}), skipping")
            results[regime] = (np.nan, len(exits))
            continue

        y = (exits['next_regime'] == target_regime).astype(int)
        b0, b1, b8 = coefs
        logit = b0 + b1 * exits['trend_1h_last'] + b8 * exits['trend_8h_last']
        pred = sigmoid(logit)

        auc = roc_auc_score(y, pred) if y.nunique() > 1 else float('nan')

        print(f"\n  {model_label}:")
        print(f"    Exits: {len(exits)} (positive={y.sum()}, negative={len(exits)-y.sum()})")
        print(f"    AUC: {auc:.4f}" if not np.isnan(auc) else "    AUC: N/A (single class)")

        if not np.isnan(auc):
            if auc > 0.90:
                print(f"    → PASS (AUC {auc:.4f} > 0.90)")
            elif auc > 0.85:
                print(f"    → WARN (AUC {auc:.4f} in [0.85, 0.90])")
            else:
                print(f"    → FAIL (AUC {auc:.4f} < 0.85)")

        results[regime] = (auc, len(exits))

    return results


def check_calibration(episodes, label):
    """Calibration check for exit predictions."""
    print()
    print("─" * 60)
    print(f"  Check 5: Calibration ({label})")
    print("─" * 60)

    bins = [(0, 0.10), (0.10, 0.50), (0.50, 0.90), (0.90, 1.01)]

    for regime, coefs, target_regime, model_label in [
        (2, C2_COEFS, 3, "C2 Pullback → P(bull)"),
        (1, C1_COEFS, 3, "C1 Reversal → P(bt)"),
    ]:
        ep = episodes[episodes['regime'] == regime].copy()
        idx = ep.index
        next_reg = []
        for i in idx:
            pos = episodes.index.get_loc(i)
            if pos + 1 < len(episodes):
                next_reg.append(episodes['regime'].iloc[pos + 1])
            else:
                next_reg.append(np.nan)
        ep['next_regime'] = next_reg
        ep = ep.dropna(subset=['next_regime'])
        ep['next_regime'] = ep['next_regime'].astype(int)
        exits = ep[ep['next_regime'].isin([0, 3])].copy()

        if len(exits) < 5:
            print(f"\n  {model_label}: too few exits, skipping")
            continue

        y = (exits['next_regime'] == target_regime).astype(int).values
        b0, b1, b8 = coefs
        logit = b0 + b1 * exits['trend_1h_last'].values + b8 * exits['trend_8h_last'].values
        pred = sigmoid(logit)

        print(f"\n  {model_label} ({len(exits)} exits):")
        print(f"    {'Bin':>14s}  {'n':>5s}  {'pred_mean':>9s}  {'actual':>8s}  {'gap':>6s}")

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
                is_extreme = (lo < 0.10 + 1e-9) or (lo >= 0.90 - 1e-9)
                if is_extreme:
                    extreme_n += n
                marker = ""
                if is_extreme and abs(gap) > 0.15:
                    marker = " ← FAIL"
                    cal_ok = False
                elif is_extreme and abs(gap) > 0.10:
                    marker = " ← WARN"
                print(f"    [{lo:.2f},{hi:.2f})  {n:>5d}  {pm:>9.4f}  {act:>8.4f}  {gap:>+6.2%}{marker}")
            else:
                print(f"    [{lo:.2f},{hi:.2f})  {0:>5d}      -         -       -")

        extreme_pct = extreme_n / total_n if total_n > 0 else 0
        print(f"\n    Bimodal: {extreme_pct:.1%} in extreme bins (<0.10 or >0.90)")
        if extreme_pct > 0.90:
            print(f"    → PASS (>{90}%)")
        elif extreme_pct > 0.85:
            print(f"    → WARN ({extreme_pct:.1%})")
        else:
            print(f"    → FAIL ({extreme_pct:.1%} < 85%)")


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
    all_verdicts = {}

    # IS dataset
    is_verdicts = grade_dataset(IS_FILE, "BTC IS (Jul 2025 – Feb 2026)", n_days=214)
    all_verdicts['IS'] = is_verdicts

    # Forward dataset
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
            if not passed and dataset == 'IS':  # Only IS failures count for overall
                overall = False

    print(f"\n  Overall: {'PASS' if overall else 'FAIL'}")
    print("=" * 70)


if __name__ == '__main__':
    main()
