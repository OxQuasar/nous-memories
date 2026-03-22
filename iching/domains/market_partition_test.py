#!/usr/bin/env python3
"""
Task 1: Timescale check with ob100_ratio_1m at {1h, 2h, 4h}
Task 2: Edge-level partition test — first genuine test of Z₅ grammar
"""

import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from market_regime_predictions import (
    Z5_TYPING, Z5_NAMES, TRIGRAMS, REGIMES, VERTICES,
    EDGES, AXIS_NAMES,
    edge_type as z5_edge_type, flipped_axis,
)

# ── Constants ────────────────────────────────────────────────────────

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../markets/data/btc_datalog_2025-07-21_2026-02-20.csv',
)
OUT_DIR = os.path.dirname(__file__)

VOL_ROLLING_WINDOW_DAYS = 30
LIQ_ROLLING_WINDOW_DAYS = 7


# ── Shared utilities ─────────────────────────────────────────────────

def mutual_information(a, b):
    """MI between two binary arrays (0/1)."""
    a, b = np.asarray(a), np.asarray(b)
    n = len(a)
    ct = np.zeros((2, 2))
    for i, j in zip(a, b):
        ct[int(i), int(j)] += 1
    ct /= n
    mi = 0.0
    for i in range(2):
        for j in range(2):
            if ct[i, j] > 0:
                mi += ct[i, j] * np.log2(ct[i, j] / (ct[i, :].sum() * ct[:, j].sum()))
    return mi


def build_bars(df, period):
    """Resample raw df to bars at given period, construct axes, assign vertices."""
    bpd = 24 / (pd.Timedelta(period).total_seconds() / 3600)
    vol_window = max(1, int(VOL_ROLLING_WINDOW_DAYS * bpd))
    liq_window = max(1, int(LIQ_ROLLING_WINDOW_DAYS * bpd))

    bars = df.resample(period, label='left', closed='left').agg({
        'price': 'last',
        'trend_4h': 'last',
        'realized_vol_4h': 'last',
        'ob100_ratio_1m': 'mean',
    }).dropna(subset=['price'])

    bars['b0_trend'] = (bars['trend_4h'] > 0).astype(int)
    vol_med = bars['realized_vol_4h'].rolling(vol_window, min_periods=1).median()
    bars['b1_vol'] = (bars['realized_vol_4h'] > vol_med).astype(int)
    liq_med = bars['ob100_ratio_1m'].rolling(liq_window, min_periods=1).median()
    bars['b2_liq'] = (bars['ob100_ratio_1m'] > liq_med).astype(int)

    bars['vertex'] = bars['b0_trend'] + 2 * bars['b1_vol'] + 4 * bars['b2_liq']
    return bars


# ══════════════════════════════════════════════════════════════════════
# TASK 1: Timescale check with ob100_ratio_1m
# ══════════════════════════════════════════════════════════════════════

def task1(df):
    print("=" * 70)
    print("TASK 1: TIMESCALE CHECK WITH ob100_ratio_1m")
    print("=" * 70)

    results = []
    for period in ['1h', '2h', '4h']:
        bars = build_bars(df, period)
        v = bars['vertex'].values.astype(int)

        mi = mutual_information(bars['b1_vol'].values, bars['b2_liq'].values)

        xor = v[:-1] ^ v[1:]
        hamming = np.array([bin(x).count('1') for x in xor])
        n_self = (hamming == 0).sum()
        n_q3 = (hamming == 1).sum()
        n_multi = (hamming > 1).sum()
        n_nonself = n_q3 + n_multi
        m1 = n_q3 / n_nonself if n_nonself else 0

        results.append({
            'period': period, 'n_bars': len(bars), 'mi': mi,
            'm1': m1, 'n_q3': n_q3, 'self_frac': n_self / len(xor),
        })

    print(f"\n  {'Period':>6}  {'Bars':>5}  {'MI':>6}  {'M1':>6}  {'Q₃ edges':>8}  {'Self%':>6}")
    print(f"  {'─'*6:>6}  {'─'*5:>5}  {'─'*6:>6}  {'─'*6:>6}  {'─'*8:>8}  {'─'*6:>6}")
    for r in results:
        ok = '✓' if r['mi'] < 0.1 and r['m1'] > 0.7 else ''
        print(f"  {r['period']:>6}  {r['n_bars']:>5}  {r['mi']:.4f}  "
              f"{r['m1']:.4f}  {r['n_q3']:>8}  {100*r['self_frac']:5.1f}% {ok}")

    # Select timescale
    best = None
    for r in results:
        if r['mi'] < 0.1 and r['m1'] > 0.7:
            best = r
            break
    if best is None:
        best = results[-1]  # fallback to 4h
        print(f"\n  No timescale achieves MI<0.1 AND M1>0.7. Using 4h.")
    else:
        print(f"\n  ★ Selected: {best['period']} — MI={best['mi']:.4f}, M1={best['m1']:.4f}, "
              f"Q₃ edges={best['n_q3']}")

    return best['period']


# ══════════════════════════════════════════════════════════════════════
# TASK 2: Edge-level partition test
# ══════════════════════════════════════════════════════════════════════

def compute_persistence(vertices):
    """For each index i, count how many consecutive bars share vertex[i]."""
    n = len(vertices)
    persist = np.zeros(n, dtype=int)
    i = 0
    while i < n:
        j = i
        while j < n and vertices[j] == vertices[i]:
            j += 1
        run_len = j - i
        for k in range(i, j):
            persist[k] = run_len - (k - i)  # bars remaining in this run
        i = j
    return persist


def task2(df, period):
    print("\n" + "=" * 70)
    print(f"TASK 2: EDGE-LEVEL PARTITION TEST ({period} bars)")
    print("=" * 70)

    bars = build_bars(df, period)
    v = bars['vertex'].values.astype(int)
    vol = bars['realized_vol_4h'].values

    # Persistence: after arriving at bar i, how many bars until vertex changes?
    persistence = compute_persistence(v)

    # Build edge-level observations
    # For each Q₃-edge transition i→i+1: record (from, to, persistence at dest, vol_ratio)
    edge_obs = {(u, w): {'persist': [], 'vol_ratio': []}
                for u, w in EDGES}
    # Also track reverse direction (same undirected edge)
    for u, w in EDGES:
        edge_obs[(w, u)] = edge_obs[(u, w)]  # alias

    n_bars = len(v)
    for i in range(n_bars - 1):
        u, w = int(v[i]), int(v[i + 1])
        xor = u ^ w
        if bin(xor).count('1') != 1:
            continue  # skip non-Q₃ transitions

        # Canonical key: smaller vertex first
        key = (min(u, w), max(u, w))

        # Persistence at destination
        dest_persist = persistence[i + 1]
        edge_obs[key]['persist'].append(dest_persist)

        # Volatility ratio (dest / origin)
        if vol[i] > 0:
            edge_obs[key]['vol_ratio'].append(vol[i + 1] / vol[i])

    # ── Per-edge table ──
    print(f"\n── Per-edge statistics ({period}) ──")
    print(f"  {'Edge':>9}  {'Axis':>10}  {'Type':>4}  {'N':>5}  "
          f"{'Persist':>8}  {'±SE':>6}  {'VolR':>7}  {'±SE':>6}")
    print(f"  {'─'*9:>9}  {'─'*10:>10}  {'─'*4:>4}  {'─'*5:>5}  "
          f"{'─'*8:>8}  {'─'*6:>6}  {'─'*7:>7}  {'─'*6:>6}")

    edge_results = []
    for u, w in EDGES:
        key = (u, w)
        ax = flipped_axis(u, w)
        t = z5_edge_type(Z5_TYPING[u], Z5_TYPING[w])
        obs = edge_obs[key]
        n = len(obs['persist'])

        p_arr = np.array(obs['persist'], dtype=float)
        vr_arr = np.array(obs['vol_ratio'], dtype=float)

        p_mean = p_arr.mean() if n > 0 else np.nan
        p_se = p_arr.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
        vr_mean = vr_arr.mean() if len(vr_arr) > 0 else np.nan
        vr_se = vr_arr.std(ddof=1) / np.sqrt(len(vr_arr)) if len(vr_arr) > 1 else np.nan

        edge_results.append({
            'u': u, 'w': w, 'axis': ax, 'type': t, 'n': n,
            'p_mean': p_mean, 'p_se': p_se,
            'vr_mean': vr_mean, 'vr_se': vr_se,
        })

        print(f"  {u:03b}↔{w:03b}  {AXIS_NAMES[ax]:>10}  {t:>4}  {n:>5}  "
              f"{p_mean:>8.2f}  {p_se:>5.2f}  {vr_mean:>7.4f}  {vr_se:>5.4f}")

    # ── Traffic distribution by type ──
    print(f"\n── Traffic by Z₅ type ──")
    for t in ['比和', '生', '克']:
        edges_t = [e for e in edge_results if e['type'] == t]
        total_n = sum(e['n'] for e in edges_t)
        per_edge = [e['n'] for e in edges_t]
        print(f"  {t}: {len(edges_t)} edges, {total_n} total traversals, "
              f"per-edge: {per_edge}")

    # ── Axis-level partition test ──
    print(f"\n── Axis-level partition test ──")

    axis_stats = {}
    for axis_id in range(3):
        axis_edges = [e for e in edge_results if e['axis'] == axis_id]
        p_means = [e['p_mean'] for e in axis_edges if not np.isnan(e['p_mean'])]
        vr_means = [e['vr_mean'] for e in axis_edges if not np.isnan(e['vr_mean'])]
        types = [e['type'] for e in axis_edges]

        p_range = max(p_means) - min(p_means) if len(p_means) >= 2 else 0
        vr_range = max(vr_means) - min(vr_means) if len(vr_means) >= 2 else 0
        p_var = np.var(p_means, ddof=1) if len(p_means) >= 2 else 0
        vr_var = np.var(vr_means, ddof=1) if len(vr_means) >= 2 else 0

        axis_stats[axis_id] = {
            'p_means': p_means, 'vr_means': vr_means,
            'p_range': p_range, 'vr_range': vr_range,
            'p_var': p_var, 'vr_var': vr_var,
            'types': types,
        }

        print(f"\n  {AXIS_NAMES[axis_id]} (types: {types}):")
        print(f"    Persistence means: {['%.2f' % x for x in p_means]}")
        print(f"      range={p_range:.3f}  var={p_var:.3f}")
        print(f"    Vol ratio means:   {['%.4f' % x for x in vr_means]}")
        print(f"      range={vr_range:.4f}  var={vr_var:.6f}")

    # ── Level 1 criterion ──
    print(f"\n── LEVEL 1 TEST: {'{'}4, 2+2, 2+2{'}'} partition ──")
    print(f"  Prediction: ONE axis has largest within-axis range (bimodal/mixed),")
    print(f"  the other two have small range (uniform).")

    for obs_name, key_range, key_var, fmt in [
        ('Persistence', 'p_range', 'p_var', '.3f'),
        ('Vol ratio', 'vr_range', 'vr_var', '.4f'),
    ]:
        ranges = {ax: axis_stats[ax][key_range] for ax in range(3)}
        sorted_axes = sorted(ranges, key=lambda x: ranges[x], reverse=True)
        max_range = ranges[sorted_axes[0]]
        med_range = ranges[sorted_axes[1]]
        min_range = ranges[sorted_axes[2]]

        ratio = max_range / med_range if med_range > 0 else float('inf')
        passed = ratio > 2.0

        print(f"\n  {obs_name}:")
        for ax in sorted_axes:
            marker = ' ← MAX' if ax == sorted_axes[0] else ''
            print(f"    {AXIS_NAMES[ax]:>10}: range={ranges[ax]:{fmt}}  "
                  f"(types: {axis_stats[ax]['types']}){marker}")
        print(f"    max/median ratio: {ratio:.2f}  {'✓ PASS (>2.0)' if passed else '✗ FAIL (<2.0)'}")

    # ── Level 2 criterion ──
    print(f"\n── LEVEL 2 TEST: canonical assignment check ──")
    print(f"  Canonical prediction:")
    print(f"    trend     = mixed  (2克+2生) → LARGEST range")
    print(f"    volatility = pure-克 (4克)    → uniform high disruption")
    print(f"    liquidity  = doublet (2比和+2生) → uniform low disruption")

    for obs_name, key_range in [('Persistence', 'p_range'), ('Vol ratio', 'vr_range')]:
        ranges = {ax: axis_stats[ax][key_range] for ax in range(3)}
        largest_axis = max(ranges, key=lambda x: ranges[x])
        print(f"\n  {obs_name}: largest range on {AXIS_NAMES[largest_axis]} axis")
        canonical = largest_axis == 0  # trend = axis 0
        print(f"    Canonical prediction (trend = largest): "
              f"{'✓ MATCH' if canonical else '✗ MISMATCH'}")

    # ── Per-type aggregate ──
    print(f"\n── Observable means by Z₅ type (pooled across all edges) ──")
    for t in ['比和', '生', '克']:
        edges_t = [e for e in edge_results if e['type'] == t]
        all_p = []
        all_vr = []
        for e in edges_t:
            key = (e['u'], e['w'])
            all_p.extend(edge_obs[key]['persist'])
            all_vr.extend(edge_obs[key]['vol_ratio'])

        p_arr = np.array(all_p, dtype=float)
        vr_arr = np.array(all_vr, dtype=float)
        n_p = len(p_arr)
        n_vr = len(vr_arr)

        p_mean = p_arr.mean() if n_p > 0 else np.nan
        p_se = p_arr.std(ddof=1) / np.sqrt(n_p) if n_p > 1 else np.nan
        vr_mean = vr_arr.mean() if n_vr > 0 else np.nan
        vr_se = vr_arr.std(ddof=1) / np.sqrt(n_vr) if n_vr > 1 else np.nan

        print(f"  {t}: persist={p_mean:.2f}±{p_se:.2f} (n={n_p})  "
              f"vol_ratio={vr_mean:.4f}±{vr_se:.4f} (n={n_vr})")

    print(f"\n  Grammar prediction: 克 → low persistence, high vol_ratio")
    print(f"                      生 → high persistence, low vol_ratio")
    print(f"                      比和 → intermediate")


# ══════════════════════════════════════════════════════════════════════

def main():
    print("Loading raw data...")
    cols = ['timestamp', 'price', 'trend_4h', 'realized_vol_4h', 'ob100_ratio_1m']
    df = pd.read_csv(DATA_PATH, usecols=cols)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')
    print(f"  {len(df):,} rows loaded\n")

    selected_period = task1(df)
    task2(df, selected_period)


if __name__ == '__main__':
    main()
