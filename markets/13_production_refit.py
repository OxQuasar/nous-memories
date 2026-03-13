"""
Phase 13: Production logistic regression on raw-scale OOS data.

Key insight: macro regime detection uses 2-bit (trend_8h × trend_48h), not 3-bit.
The fast bit (trend_1h) causes noisy micro-episodes. Macro transitions are driven
by trend_8h flipping — the fast bit is a qualifier read at exit, not a regime determinant.

Output: production-ready coefficients in raw OLS slope units.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score, brier_score_loss

DATA = '/home/quasar/nous/memories/markets/data/btc_5m_2023-01-01_2024-12-31.csv'

df = pd.read_csv(DATA)
print(f"Loaded: {len(df)} bars, price {df.price.min():.0f}–{df.price.max():.0f}")

# ─── MACRO REGIME: 2-bit (trend_8h × trend_48h) ───
# trend_1h is too noisy for episode detection at raw scale.
# Macro regime = medium × slow alignment. Fast bit read at exit only.
df['b1'] = (df['trend_8h'] > 0).astype(int)
df['b2'] = (df['trend_48h'] > 0).astype(int)
df['macro'] = df['b1'] + 2*df['b2']
# 0=bear(both neg), 1=reversal(8h+,48h-), 2=pullback(8h-,48h+), 3=bull(both pos)

df['macro_change'] = (df['macro'] != df['macro'].shift(1)).astype(int)
df['episode_id'] = df['macro_change'].cumsum()

episodes = df.groupby('episode_id').agg(
    regime=('macro', 'first'),
    t1h_last=('trend_1h', 'last'),
    t8h_last=('trend_8h', 'last'),
    duration=('episode_id', 'count'),
).reset_index()
episodes['next_regime'] = episodes['regime'].shift(-1)
episodes = episodes.dropna(subset=['next_regime'])
episodes['next_regime'] = episodes['next_regime'].astype(int)

print(f"Macro episodes: {len(episodes)}, mean duration: {episodes.duration.mean()*5/60:.1f}h")
print(f"Regime counts: {episodes.regime.value_counts().sort_index().to_dict()}")

# Standardization for numerical stability
t1h_std = df['trend_1h'].std()
t8h_std = df['trend_8h'].std()
print(f"\nScale factors: trend_1h_std={t1h_std:.6f}, trend_8h_std={t8h_std:.6f}")


def fit_exit_model(ep, target_col, label):
    """Fit logistic regression on z-scored features, report in both scales."""
    ep = ep.copy()
    ep['t1h_z'] = ep['t1h_last'] / t1h_std
    ep['t8h_z'] = ep['t8h_last'] / t8h_std

    X = sm.add_constant(ep[['t1h_z', 't8h_z']])
    y = ep[target_col]
    model = sm.Logit(y, X).fit(disp=0, maxiter=200)
    pred = model.predict(X)
    auc = roc_auc_score(y, pred)
    brier = brier_score_loss(y, pred)

    # Raw-scale coefficients
    b0 = model.params['const']
    b1_raw = model.params['t1h_z'] / t1h_std
    b8_raw = model.params['t8h_z'] / t8h_std

    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"{'='*70}")
    print(f"  Episodes: {len(ep)} (positive={y.sum()}, negative={len(ep)-y.sum()})")
    print(f"  AUC: {auc:.4f}, Brier: {brier:.4f}, Pseudo R²: {model.prsquared:.4f}")

    print(f"\n  Z-scored coefficients:")
    for name in ['const', 't1h_z', 't8h_z']:
        print(f"    {name:>8s}: {model.params[name]:>10.4f}  (p={model.pvalues[name]:.4e})")

    print(f"\n  Raw-scale coefficients (PRODUCTION):")
    print(f"    const:    {b0:>12.4f}")
    print(f"    trend_1h: {b1_raw:>12.1f}")
    print(f"    trend_8h: {b8_raw:>12.1f}")

    # Decision boundary
    if b8_raw != 0:
        threshold = -b0 / b8_raw
        print(f"\n  Decision boundary (trend_1h=0): trend_8h = {threshold:.7f}")

    # Scorecard
    print(f"\n  Scorecard (trend_1h=0):")
    print(f"    {'trend_8h':>14s}  P({label.split('→')[1].strip() if '→' in label else 'positive'})")
    for t8h in [-5e-4, -3e-4, -1e-4, -5e-5, -1e-5, 0, 1e-5, 5e-5, 1e-4]:
        logit = b0 + b8_raw * t8h
        p = 1 / (1 + np.exp(-np.clip(logit, -500, 500)))
        print(f"    {t8h:>14.7f}  {p:.4f}")

    # Calibration
    print(f"\n  Calibration:")
    print(f"    {'Bin':>14s}  {'n':>5s}  {'pred':>8s}  {'actual':>8s}")
    bins = [(0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.0)]
    for lo, hi in bins:
        mask = (pred >= lo) & (pred < hi + 0.001 * (hi == 1.0))
        n = mask.sum()
        if n > 0:
            print(f"    [{lo:.1f},{hi:.1f}]  {n:>5d}  {pred[mask].mean():>8.4f}  {y[mask].mean():>8.4f}")

    return model, b0, b1_raw, b8_raw, auc


# ─── C2 PULLBACK EXIT ───
c2 = episodes[episodes['regime'] == 2].copy()
c2 = c2[c2['next_regime'].isin([0, 3])]
c2['bull'] = (c2['next_regime'] == 3).astype(int)
m_c2, b0_c2, b1_c2, b8_c2, auc_c2 = fit_exit_model(c2, 'bull', 'C2 Pullback Exit → P(bull)')

# ─── C1 REVERSAL EXIT ───
c1 = episodes[episodes['regime'] == 1].copy()
c1 = c1[c1['next_regime'].isin([0, 3])]
c1['bt'] = (c1['next_regime'] == 3).astype(int)
m_c1, b0_c1, b1_c1, b8_c1, auc_c1 = fit_exit_model(c1, 'bt', 'C1 Reversal Exit → P(breakthrough)')

# ─── PRODUCTION SUMMARY ───
th_c2 = -b0_c2 / b8_c2
th_c1 = -b0_c1 / b8_c1
print(f"""
{'='*70}
  PRODUCTION COEFFICIENTS — BTC OOS 2023-2024
{'='*70}

  Trend units: raw OLS slope / mean price (fractional rate per bar)
  Typical magnitude: ~1e-4 for trend_8h, ~5e-4 for trend_1h

  C2 Pullback Exit:
    P(bull) = σ({b0_c2:.4f} + {b1_c2:.1f} × trend_1h + {b8_c2:.1f} × trend_8h)
    Decision boundary (at trend_1h=0): trend_8h = {th_c2:.7f}
    AUC: {auc_c2:.4f}

  C1 Reversal Exit:
    P(bt) = σ({b0_c1:.4f} + {b1_c1:.1f} × trend_1h + {b8_c1:.1f} × trend_8h)
    Decision boundary (at trend_1h=0): trend_8h = {th_c1:.7f}
    AUC: {auc_c1:.4f}

  Regime detection: 2-bit macro (trend_8h sign × trend_48h sign)
    0 = bear (both negative)
    1 = reversal (8h positive, 48h negative)
    2 = pullback (8h negative, 48h positive)
    3 = bull (both positive)
""")
