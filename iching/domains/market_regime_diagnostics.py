#!/usr/bin/env python3
"""
Market regime diagnostics:
  Task 1: Liquidity axis candidate screening (MI independence test)
  Task 2: Timescale sweep (M1 vs bar size)
  Task 3: Hamming-3 transition characterization
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from market_regime_predictions import (
    Z5_TYPING, Z5_NAMES, TRIGRAMS, REGIMES,
    edge_type as z5_edge_type,
)

# ── Constants ────────────────────────────────────────────────────────

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../markets/data/btc_datalog_2025-07-21_2026-02-20.csv',
)
OUT_DIR = os.path.dirname(__file__)
BARS_CSV = os.path.join(OUT_DIR, 'market_4h_bars.csv')
TRANS_CSV = os.path.join(OUT_DIR, 'market_transitions.csv')

VOL_ROLLING_WINDOW_DAYS = 30
LIQ_ROLLING_WINDOW_DAYS = 7
AXIS_NAMES = {0: 'trend', 1: 'volatility', 2: 'liquidity'}

LIQ_CANDIDATES = [
    'ob_total_ratio_1m',
    'ob100_ratio_1m',
    'depth_asymmetry_10',
    'liquidity_shift_15m',
    'ob_imbalance_slope_5m',
]


# ── Shared utilities ─────────────────────────────────────────────────

def mutual_information(a, b):
    """MI between two binary arrays (0/1)."""
    a, b = np.asarray(a), np.asarray(b)
    n = len(a)
    ct = np.zeros((2, 2))
    for i, j in zip(a, b):
        ct[i, j] += 1
    ct /= n
    mi = 0.0
    for i in range(2):
        for j in range(2):
            if ct[i, j] > 0:
                mi += ct[i, j] * np.log2(ct[i, j] / (ct[i, :].sum() * ct[:, j].sum()))
    return mi


def phi_correlation(a, b):
    """Matthews/phi correlation for two binary arrays."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    n = len(a)
    n11 = ((a == 1) & (b == 1)).sum()
    n10 = ((a == 1) & (b == 0)).sum()
    n01 = ((a == 0) & (b == 1)).sum()
    n00 = ((a == 0) & (b == 0)).sum()
    denom = np.sqrt((n11 + n10) * (n11 + n01) * (n00 + n10) * (n00 + n01))
    if denom == 0:
        return 0.0
    return (n11 * n00 - n10 * n01) / denom


def vertex_entropy(vertices, n_vertices=8):
    """Shannon entropy of vertex distribution (bits)."""
    counts = np.bincount(vertices, minlength=n_vertices)
    p = counts / counts.sum()
    p = p[p > 0]
    return -np.sum(p * np.log2(p))


def bars_per_day(period_str):
    """Number of bars per day for a given resample period."""
    hours = pd.Timedelta(period_str).total_seconds() / 3600
    return 24 / hours


def build_transitions_fast(vertices):
    """Vectorized transition extraction. Returns DataFrame."""
    v = np.asarray(vertices, dtype=int)
    xor = v[:-1] ^ v[1:]
    hamming = np.array([bin(x).count('1') for x in xor])
    is_edge = hamming == 1
    is_self = hamming == 0

    edge_types = []
    for i in range(len(v) - 1):
        u, w = int(v[i]), int(v[i + 1])
        h = hamming[i]
        if h == 0:
            edge_types.append('self')
        elif h == 1:
            edge_types.append(z5_edge_type(Z5_TYPING[u], Z5_TYPING[w]))
        else:
            edge_types.append('multi')

    return pd.DataFrame({
        'from_vertex': v[:-1],
        'to_vertex': v[1:],
        'hamming_dist': hamming,
        'is_q3_edge': is_edge,
        'edge_type': edge_types,
    })


# ══════════════════════════════════════════════════════════════════════
# TASK 1: Liquidity axis candidate screening
# ══════════════════════════════════════════════════════════════════════

def task1_liquidity_candidates():
    print("=" * 70)
    print("TASK 1: LIQUIDITY AXIS CANDIDATE SCREENING")
    print("=" * 70)

    # Load all candidate fields + vol axis
    cols = ['timestamp', 'realized_vol_4h'] + LIQ_CANDIDATES
    print(f"\nLoading {len(cols)} columns from raw data...")
    df = pd.read_csv(DATA_PATH, usecols=cols)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')
    print(f"  Raw rows: {len(df):,}")

    # Also load trend for full vertex assignment
    df_trend = pd.read_csv(DATA_PATH, usecols=['timestamp', 'trend_4h'])
    df_trend['datetime'] = pd.to_datetime(df_trend['timestamp'], unit='ms', utc=True)
    df_trend = df_trend.set_index('datetime')

    # Resample to 4h
    period = '4h'
    bpd = bars_per_day(period)
    vol_window = int(VOL_ROLLING_WINDOW_DAYS * bpd)
    liq_window = int(LIQ_ROLLING_WINDOW_DAYS * bpd)

    agg_dict = {'realized_vol_4h': 'last'}
    for c in LIQ_CANDIDATES:
        agg_dict[c] = 'mean'

    bars = df.resample(period, label='left', closed='left').agg(agg_dict)
    trend_bars = df_trend.resample(period, label='left', closed='left').agg({'trend_4h': 'last'})
    bars = bars.join(trend_bars).dropna(subset=['realized_vol_4h'])

    # b0, b1 (fixed)
    bars['b0_trend'] = (bars['trend_4h'] > 0).astype(int)
    vol_median = bars['realized_vol_4h'].rolling(vol_window, min_periods=1).median()
    bars['b1_vol'] = (bars['realized_vol_4h'] > vol_median).astype(int)

    print(f"  4h bars: {len(bars)}")
    print(f"  b1_vol mean: {bars['b1_vol'].mean():.3f}")

    # Also include volume_since_last as baseline
    df_vol = pd.read_csv(DATA_PATH, usecols=['timestamp', 'volume_since_last'])
    df_vol['datetime'] = pd.to_datetime(df_vol['timestamp'], unit='ms', utc=True)
    df_vol = df_vol.set_index('datetime')
    vol_bars = df_vol.resample(period, label='left', closed='left').agg({'volume_since_last': 'sum'})
    bars = bars.join(vol_bars)
    all_candidates = ['volume_since_last'] + LIQ_CANDIDATES

    # Screen each candidate
    results = []
    for field in all_candidates:
        col = bars[field].copy()
        n_valid = col.notna().sum()
        if n_valid < 100:
            print(f"  SKIP {field}: only {n_valid} non-NaN values")
            continue

        # Binarize by rolling median
        med = col.rolling(liq_window, min_periods=1).median()
        b2 = (col > med).astype(int)

        mi = mutual_information(bars['b1_vol'].values, b2.values)
        phi = phi_correlation(bars['b1_vol'].values, b2.values)

        # Vertex distribution
        vertex = bars['b0_trend'].values + 2 * bars['b1_vol'].values + 4 * b2.values
        vcounts = np.bincount(vertex.astype(int), minlength=8)
        min_v = vcounts.min()
        ent = vertex_entropy(vertex.astype(int))
        agree_pct = ((bars['b1_vol'].values == b2.values).sum() / len(b2)) * 100

        results.append({
            'field': field,
            'MI': mi,
            'phi': phi,
            'agree%': agree_pct,
            'min_vertex': min_v,
            'entropy': ent,
            'vcounts': vcounts.tolist(),
        })

    # Print comparison table
    print(f"\n{'─'*70}")
    print(f"  {'Field':>26s}   MI     phi    agree%  min_v  entropy")
    print(f"  {'─'*26:>26s}  {'─'*5}  {'─'*6}  {'─'*6}  {'─'*5}  {'─'*7}")
    for r in sorted(results, key=lambda x: x['MI']):
        marker = ' ✓' if r['MI'] < 0.1 and r['min_vertex'] >= 30 else ''
        print(f"  {r['field']:>26s}  {r['MI']:.4f}  {r['phi']:+.4f}  "
              f"{r['agree%']:5.1f}%  {r['min_vertex']:>5d}  {r['entropy']:.3f}{marker}")

    # Print vertex distributions for top candidates
    print(f"\n── Vertex distributions (top candidates by MI) ──")
    for r in sorted(results, key=lambda x: x['MI'])[:4]:
        print(f"\n  {r['field']} (MI={r['MI']:.4f}):")
        for v in range(8):
            pct = 100 * r['vcounts'][v] / sum(r['vcounts'])
            bar = '█' * int(pct / 2)
            print(f"    {v} ({v:03b}) {REGIMES[v]:>20s}: {r['vcounts'][v]:>4d} ({pct:5.1f}%) {bar}")

    # Return best candidate
    viable = [r for r in results if r['MI'] < 0.1 and r['min_vertex'] >= 30]
    if viable:
        best = min(viable, key=lambda x: x['MI'])
        print(f"\n  ★ BEST: {best['field']} — MI={best['MI']:.4f}, min_vertex={best['min_vertex']}")
        return best['field']
    else:
        # Relax: best MI regardless
        best = min(results, key=lambda x: x['MI'])
        print(f"\n  ⚠ No candidate achieves MI<0.1 AND min_vertex≥30")
        print(f"    Best MI: {best['field']} — MI={best['MI']:.4f}, min_vertex={best['min_vertex']}")
        return best['field']


# ══════════════════════════════════════════════════════════════════════
# TASK 2: Timescale sweep — M1 vs bar size
# ══════════════════════════════════════════════════════════════════════

def task2_timescale_sweep():
    print("\n" + "=" * 70)
    print("TASK 2: TIMESCALE SWEEP — M1 VS BAR SIZE")
    print("=" * 70)

    # Load once
    cols = ['timestamp', 'price', 'trend_4h', 'realized_vol_4h', 'volume_since_last']
    print("\nLoading data...")
    df = pd.read_csv(DATA_PATH, usecols=cols)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')
    print(f"  Raw rows: {len(df):,}")

    periods = ['1h', '2h', '4h', '8h', '12h', '24h']
    results = []

    for period in periods:
        bpd = bars_per_day(period)
        vol_window = int(VOL_ROLLING_WINDOW_DAYS * bpd)
        liq_window = int(LIQ_ROLLING_WINDOW_DAYS * bpd)

        bars = df.resample(period, label='left', closed='left').agg({
            'price': 'last',
            'trend_4h': 'last',
            'realized_vol_4h': 'last',
            'volume_since_last': 'sum',
        }).dropna(subset=['price'])

        # Axes
        bars['b0'] = (bars['trend_4h'] > 0).astype(int)
        vol_med = bars['realized_vol_4h'].rolling(vol_window, min_periods=1).median()
        bars['b1'] = (bars['realized_vol_4h'] > vol_med).astype(int)
        liq_med = bars['volume_since_last'].rolling(liq_window, min_periods=1).median()
        bars['b2'] = (bars['volume_since_last'] > liq_med).astype(int)

        bars['vertex'] = bars['b0'] + 2 * bars['b1'] + 4 * bars['b2']
        trans = build_transitions_fast(bars['vertex'].values)

        n_bars = len(bars)
        n_trans = len(trans)
        n_self = (trans['edge_type'] == 'self').sum()
        n_q3 = trans['is_q3_edge'].sum()
        n_multi = (trans['edge_type'] == 'multi').sum()
        n_h2 = (trans['hamming_dist'] == 2).sum()
        n_h3 = (trans['hamming_dist'] == 3).sum()
        n_nonself = n_q3 + n_multi

        results.append({
            'period': period,
            'n_bars': n_bars,
            'n_trans': n_trans,
            'self_frac': n_self / n_trans if n_trans else 0,
            'M1': n_q3 / n_nonself if n_nonself else 0,
            'q3_frac': n_q3 / n_trans if n_trans else 0,
            'multi_frac': n_multi / n_trans if n_trans else 0,
            'h2_frac': n_h2 / n_trans if n_trans else 0,
            'h3_frac': n_h3 / n_trans if n_trans else 0,
            'n_q3': n_q3,
            'n_multi': n_multi,
            'n_self': n_self,
        })

    # Print table
    print(f"\n{'─'*85}")
    print(f"  {'Period':>6s}  {'Bars':>5s}  {'Self%':>6s}  {'M1':>6s}  "
          f"{'Q3%':>5s}  {'Multi%':>6s}  {'H2%':>5s}  {'H3%':>5s}  "
          f"{'Q3':>4s}  {'Multi':>5s}")
    print(f"  {'─'*6:>6s}  {'─'*5:>5s}  {'─'*6:>6s}  {'─'*6:>6s}  "
          f"{'─'*5:>5s}  {'─'*6:>6s}  {'─'*5:>5s}  {'─'*5:>5s}  "
          f"{'─'*4:>4s}  {'─'*5:>5s}")
    for r in results:
        print(f"  {r['period']:>6s}  {r['n_bars']:>5d}  "
              f"{100*r['self_frac']:5.1f}%  {r['M1']:.4f}  "
              f"{100*r['q3_frac']:4.1f}%  {100*r['multi_frac']:5.1f}%  "
              f"{100*r['h2_frac']:4.1f}%  {100*r['h3_frac']:4.1f}%  "
              f"{r['n_q3']:>4d}  {r['n_multi']:>5d}")

    # Trend
    m1_vals = [r['M1'] for r in results]
    print(f"\n  M1 range: {min(m1_vals):.4f} ({results[m1_vals.index(min(m1_vals))]['period']}) "
          f"→ {max(m1_vals):.4f} ({results[m1_vals.index(max(m1_vals))]['period']})")
    random_baseline = 3.0 / 7.0  # 3 single-axis neighbors / 7 total non-self neighbors
    print(f"  Random baseline (uniform): {random_baseline:.4f}")

    return results


# ══════════════════════════════════════════════════════════════════════
# TASK 3: Hamming-3 transition characterization
# ══════════════════════════════════════════════════════════════════════

def task3_hamming3_characterization():
    print("\n" + "=" * 70)
    print("TASK 3: HAMMING-3 TRANSITION CHARACTERIZATION")
    print("=" * 70)

    bars = pd.read_csv(BARS_CSV)
    trans = pd.read_csv(TRANS_CSV)

    # Merge return info onto transitions
    trans['return_abs'] = bars['return_next_bar'].iloc[1:].abs().values[:len(trans)]

    h3 = trans[trans['hamming_dist'] == 3]
    h2 = trans[trans['hamming_dist'] == 2]
    q3 = trans[trans['is_q3_edge']]
    self_loops = trans[trans['hamming_dist'] == 0]

    print(f"\nTotal transitions: {len(trans)}")
    print(f"  Self-loops (H0): {len(self_loops)} ({100*len(self_loops)/len(trans):.1f}%)")
    print(f"  Q₃ edges  (H1): {len(q3)} ({100*len(q3)/len(trans):.1f}%)")
    print(f"  H2 jumps:        {len(h2)} ({100*len(h2)/len(trans):.1f}%)")
    print(f"  H3 jumps:        {len(h3)} ({100*len(h3)/len(trans):.1f}%)")

    # ── Mean |return| by transition type ──
    print(f"\n── Mean |return_next_bar| by transition type ──")
    for label, subset in [('Self (H0)', self_loops), ('Q₃ edge (H1)', q3),
                           ('H2 jump', h2), ('H3 jump', h3)]:
        vals = subset['return_abs'].dropna()
        if len(vals) > 0:
            print(f"  {label:>15s}: mean={vals.mean():.4f}%  "
                  f"median={vals.median():.4f}%  n={len(vals)}")

    # ── Vertex pair distribution for H3 ──
    # H3 transitions are complement pairs: v ↔ (7-v) since all 3 bits flip
    print(f"\n── H3 vertex pairs (complement pairs v ↔ 7-v) ──")
    pair_counts = {}
    for _, row in h3.iterrows():
        u, w = int(row['from_vertex']), int(row['to_vertex'])
        key = (min(u, w), max(u, w))
        pair_counts[key] = pair_counts.get(key, 0) + 1

    for (u, w), count in sorted(pair_counts.items(), key=lambda x: -x[1]):
        pct = 100 * count / len(h3)
        print(f"  {REGIMES[u]:>20s} ({u:03b}) ↔ {REGIMES[w]:<20s} ({w:03b}): "
              f"{count:>3d} ({pct:5.1f}%)")

    # ── Temporal clustering ──
    print(f"\n── Temporal clustering of H3 transitions ──")
    h3_indices = h3.index.tolist()

    # Count consecutive H3 runs
    if len(h3_indices) > 1:
        gaps = np.diff(h3_indices)
        consecutive = (gaps == 1).sum()
        runs = []
        run_len = 1
        for g in gaps:
            if g == 1:
                run_len += 1
            else:
                if run_len > 1:
                    runs.append(run_len)
                run_len = 1
        if run_len > 1:
            runs.append(run_len)

        print(f"  Total H3 transitions: {len(h3)}")
        print(f"  Consecutive H3 pairs (gap=1): {consecutive}")
        print(f"  Runs of consecutive H3: {len(runs)}")
        if runs:
            print(f"    Run lengths: {sorted(runs, reverse=True)[:10]}")

        # Time distribution by month
        h3_ts = pd.to_datetime(h3['timestamp'])
        print(f"\n  H3 by month:")
        for month, group in h3_ts.groupby(h3_ts.dt.to_period('M')):
            print(f"    {month}: {len(group)}")

    # ── Are H3 transitions associated with price extremes? ──
    print(f"\n── H3 transitions and price behavior ──")
    # Look at the bars surrounding H3 transitions
    h3_bar_indices = [i + 1 for i in h3_indices if i + 1 < len(bars)]
    h3_prices = bars.iloc[h3_bar_indices]['price'].values
    all_prices = bars['price'].values

    print(f"  Price at H3 bars — mean: ${np.mean(h3_prices):,.0f}, "
          f"median: ${np.median(h3_prices):,.0f}")
    print(f"  Price overall    — mean: ${np.mean(all_prices):,.0f}, "
          f"median: ${np.median(all_prices):,.0f}")


# ══════════════════════════════════════════════════════════════════════
# Re-run pipeline with best liquidity axis
# ══════════════════════════════════════════════════════════════════════

def rerun_pipeline_with_field(field):
    """Re-run full pipeline replacing b₂ with the chosen field."""
    print("\n" + "=" * 70)
    print(f"RE-RUNNING PIPELINE WITH b₂ = {field}")
    print("=" * 70)

    cols = ['timestamp', 'price', 'trend_4h', 'realized_vol_4h', field]
    print(f"\nLoading data...")
    df = pd.read_csv(DATA_PATH, usecols=cols)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')

    period = '4h'
    bpd = bars_per_day(period)
    vol_window = int(VOL_ROLLING_WINDOW_DAYS * bpd)
    liq_window = int(LIQ_ROLLING_WINDOW_DAYS * bpd)

    bars = df.resample(period, label='left', closed='left').agg({
        'timestamp': 'last',
        'price': 'last',
        'trend_4h': 'last',
        'realized_vol_4h': 'last',
        field: 'mean',
    }).dropna(subset=['price'])

    bars = bars.rename(columns={field: 'liq_proxy'})

    # Next-bar return
    bars['return_next_bar'] = bars['price'].pct_change().shift(-1) * 100

    bars = bars.reset_index()
    bars = bars.rename(columns={'datetime': 'timestamp_dt'})
    bars['timestamp'] = bars['timestamp_dt'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Axes
    bars['b0_trend'] = (bars['trend_4h'] > 0).astype(int)
    vol_med = bars['realized_vol_4h'].rolling(vol_window, min_periods=1).median()
    bars['b1_vol'] = (bars['realized_vol_4h'] > vol_med).astype(int)
    liq_med = bars['liq_proxy'].rolling(liq_window, min_periods=1).median()
    bars['b2_liq'] = (bars['liq_proxy'] > liq_med).astype(int)

    # Vertex
    bars['vertex'] = bars['b0_trend'] + 2 * bars['b1_vol'] + 4 * bars['b2_liq']
    bars['trigram'] = bars['vertex'].map(TRIGRAMS)
    bars['element'] = bars['vertex'].map(lambda v: Z5_NAMES[Z5_TYPING[v]])

    # Transitions
    v = bars['vertex'].values
    ts = bars['timestamp'].values
    rows = []
    for i in range(len(v) - 1):
        u, w = int(v[i]), int(v[i + 1])
        xor = u ^ w
        hamming = bin(xor).count('1')
        flipped = [AXIS_NAMES[bit] for bit in range(3) if xor & (1 << bit)]
        flipped_str = '+'.join(flipped) if flipped else 'none'
        is_edge = hamming == 1
        if hamming == 0:
            etype = 'self'
        elif is_edge:
            etype = z5_edge_type(Z5_TYPING[u], Z5_TYPING[w])
        else:
            etype = 'multi'
        rows.append({
            'timestamp': ts[i + 1],
            'from_vertex': u,
            'to_vertex': w,
            'hamming_dist': hamming,
            'flipped_axes': flipped_str,
            'is_q3_edge': is_edge,
            'edge_type': etype,
        })
    trans = pd.DataFrame(rows)

    # Independence check
    mi = mutual_information(bars['b1_vol'].values, bars['b2_liq'].values)
    phi = phi_correlation(bars['b1_vol'].values, bars['b2_liq'].values)
    agree = ((bars['b1_vol'].values == bars['b2_liq'].values).sum() / len(bars)) * 100

    print(f"\n  MI(b1_vol, b2_liq) = {mi:.4f}")
    print(f"  Phi correlation    = {phi:+.4f}")
    print(f"  Agreement          = {agree:.1f}%")

    # Vertex distribution
    n = len(bars)
    vc = bars['vertex'].value_counts().sort_index()
    print(f"\n── Vertex Distribution ({n} bars) ──")
    for vv in range(8):
        count = vc.get(vv, 0)
        pct = 100 * count / n
        print(f"  {vv} ({vv:03b}) {TRIGRAMS[vv]} {REGIMES[vv]:>20}  "
              f"{count:>5} ({pct:5.1f}%)")

    # Transition summary
    n_trans = len(trans)
    n_self = (trans['edge_type'] == 'self').sum()
    n_q3 = trans['is_q3_edge'].sum()
    n_multi = (trans['edge_type'] == 'multi').sum()
    n_nonself = n_q3 + n_multi

    print(f"\n── Transition Counts ──")
    print(f"  Self-loops: {n_self} ({100*n_self/n_trans:.1f}%)")
    print(f"  Q₃ edges:  {n_q3} ({100*n_q3/n_trans:.1f}%)")
    print(f"  Multi-axis: {n_multi} ({100*n_multi/n_trans:.1f}%)")
    print(f"  M1: {n_q3/n_nonself:.4f} ({n_q3}/{n_nonself})")

    q3e = trans[trans['is_q3_edge']]
    print(f"\n── Q₃ Edge Type Distribution ──")
    for etype in ['比和', '生', '克']:
        count = (q3e['edge_type'] == etype).sum()
        pct = 100 * count / len(q3e) if len(q3e) > 0 else 0
        print(f"  {etype}: {count:>5} ({pct:5.1f}%)")

    print(f"\n── Axis Flip Distribution (Q₃ edges) ──")
    for axis in ['trend', 'volatility', 'liquidity']:
        count = (q3e['flipped_axes'] == axis).sum()
        pct = 100 * count / len(q3e) if len(q3e) > 0 else 0
        print(f"  {axis}: {count:>5} ({pct:5.1f}%)")

    # Save
    out_cols = [
        'timestamp', 'price', 'trend_4h', 'realized_vol_4h',
        'liq_proxy', 'b0_trend', 'b1_vol', 'b2_liq',
        'vertex', 'trigram', 'element', 'return_next_bar',
    ]
    bars[out_cols].to_csv(BARS_CSV, index=False)
    print(f"\n  Saved bars → {BARS_CSV}")

    trans.to_csv(TRANS_CSV, index=False)
    print(f"  Saved transitions → {TRANS_CSV}")


# ══════════════════════════════════════════════════════════════════════

def main():
    best_field = task1_liquidity_candidates()
    task2_timescale_sweep()
    task3_hamming3_characterization()

    if best_field and best_field != 'volume_since_last':
        rerun_pipeline_with_field(best_field)


if __name__ == '__main__':
    main()
