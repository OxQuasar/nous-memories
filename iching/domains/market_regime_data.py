#!/usr/bin/env python3
"""
Build 4h regime sequence from BTC datalog.

Resamples 1-second data to 4h bars, constructs three binary axes
(trend, volatility, liquidity), assigns Q₃ vertex labels, and
outputs the regime transition sequence.
"""

import pandas as pd
import numpy as np
import sys
import os

# ── Import from existing predictions module ──────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from market_regime_predictions import (
    Z5_TYPING, Z5_NAMES, TRIGRAMS, REGIMES,
    edge_type as z5_edge_type, flipped_axis,
)

# ── Constants ────────────────────────────────────────────────────────

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../markets/data/btc_datalog_2025-07-21_2026-02-20.csv',
)
OUT_DIR = os.path.dirname(__file__)
BARS_CSV = os.path.join(OUT_DIR, 'market_4h_bars.csv')
TRANS_CSV = os.path.join(OUT_DIR, 'market_transitions.csv')

RESAMPLE_PERIOD = '4h'
VOL_ROLLING_WINDOW = 180   # 30 days × 6 bars/day
LIQ_ROLLING_WINDOW = 42    # 7 days × 6 bars/day

# NOTE: spread_bps_1m is degenerate (>97% zeros, entirely zero after Sep 2025).
# volume_since_last has MI=0.346 with volatility — collapses Q₃ to Q₂.
# Using ob100_ratio_1m (top-100 level order book ratio) as liquidity proxy:
#   MI=0.0025 with vol (independent), most uniform vertex distribution (min=143).
#   Higher ratio = more bid depth relative to ask = more liquid.

AXIS_NAMES = {0: 'trend', 1: 'volatility', 2: 'liquidity'}


# ── Step 1: Load and resample ────────────────────────────────────────

def load_and_resample():
    """Load raw data, resample to 4h bars."""
    print("Loading data (selected columns only)...")
    cols = ['timestamp', 'price', 'trend_4h', 'realized_vol_4h', 'ob100_ratio_1m']
    df = pd.read_csv(DATA_PATH, usecols=cols)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')

    print(f"  Raw rows: {len(df):,}")
    print(f"  Time range: {df.index.min()} → {df.index.max()}")

    print("Resampling to 4h bars...")
    bars = df.resample(RESAMPLE_PERIOD, label='left', closed='left').agg({
        'timestamp': 'last',
        'price': 'last',
        'trend_4h': 'last',
        'realized_vol_4h': 'last',
        'ob100_ratio_1m': 'mean',
    }).dropna(subset=['price'])

    bars = bars.rename(columns={'ob100_ratio_1m': 'liq_proxy'})

    # Next-bar return (percentage)
    bars['return_next_bar'] = bars['price'].pct_change().shift(-1) * 100

    bars = bars.reset_index()
    bars = bars.rename(columns={'datetime': 'timestamp_dt'})
    # Use the bar open time as the canonical timestamp
    bars['timestamp'] = bars['timestamp_dt'].dt.strftime('%Y-%m-%d %H:%M:%S')

    print(f"  4h bars: {len(bars)}")
    return bars


# ── Step 2: Construct binary axes ────────────────────────────────────

def construct_axes(bars):
    """Build b0 (trend), b1 (vol), b2 (liq) from rolling medians."""
    # b0: trend positive → 1
    bars['b0_trend'] = (bars['trend_4h'] > 0).astype(int)

    # b1: realized_vol above 30-day rolling median → 1
    vol_median = bars['realized_vol_4h'].rolling(
        VOL_ROLLING_WINDOW, min_periods=1
    ).median()
    bars['b1_vol'] = (bars['realized_vol_4h'] > vol_median).astype(int)

    # b2: ob100_ratio above 7-day rolling median → 1 (more bid depth = more liquid)
    liq_median = bars['liq_proxy'].rolling(
        LIQ_ROLLING_WINDOW, min_periods=1
    ).median()
    bars['b2_liq'] = (bars['liq_proxy'] > liq_median).astype(int)

    return bars


# ── Step 3: Assign Q₃ vertex ────────────────────────────────────────

def assign_vertices(bars):
    """Compute vertex = b0 + 2*b1 + 4*b2, plus trigram and element."""
    bars['vertex'] = bars['b0_trend'] + 2 * bars['b1_vol'] + 4 * bars['b2_liq']
    bars['trigram'] = bars['vertex'].map(TRIGRAMS)
    bars['element'] = bars['vertex'].map(lambda v: Z5_NAMES[Z5_TYPING[v]])
    return bars


# ── Step 4: Extract transitions ──────────────────────────────────────

def extract_transitions(bars):
    """Build transition sequence between consecutive bars."""
    v = bars['vertex'].values
    ts = bars['timestamp'].values

    rows = []
    for i in range(len(v) - 1):
        u, w = int(v[i]), int(v[i + 1])
        xor = u ^ w
        hamming = bin(xor).count('1')

        # Which axes flipped
        flipped = [AXIS_NAMES[bit] for bit in range(3) if xor & (1 << bit)]
        flipped_str = '+'.join(flipped) if flipped else 'none'

        is_edge = hamming == 1
        is_self = hamming == 0

        if is_self:
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

    return pd.DataFrame(rows)


# ── Step 5: Output and summary ───────────────────────────────────────

def print_summary(bars, trans):
    """Print summary statistics."""
    n = len(bars)
    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")

    print(f"\nTotal 4h bars: {n}")

    # Vertex distribution
    print(f"\n── Vertex Distribution ──")
    vc = bars['vertex'].value_counts().sort_index()
    for v in range(8):
        count = vc.get(v, 0)
        pct = 100 * count / n
        print(f"  {v} ({v:03b}) {TRIGRAMS[v]} {REGIMES[v]:>20}  "
              f"{count:>5} ({pct:5.1f}%)")

    # Transition counts
    n_trans = len(trans)
    n_self = (trans['edge_type'] == 'self').sum()
    n_q3 = trans['is_q3_edge'].sum()
    n_multi = (trans['edge_type'] == 'multi').sum()

    print(f"\n── Transition Counts ──")
    print(f"  Total transitions: {n_trans}")
    print(f"  Self-loops (same regime):  {n_self:>5} ({100*n_self/n_trans:.1f}%)")
    print(f"  Q₃ edges (single-axis):   {n_q3:>5} ({100*n_q3/n_trans:.1f}%)")
    print(f"  Multi-axis jumps:          {n_multi:>5} ({100*n_multi/n_trans:.1f}%)")
    print(f"\n  Q₃ edge fraction (M1): {n_q3/(n_q3+n_multi):.4f} "
          f"({n_q3} / {n_q3+n_multi} non-self transitions)")

    # Edge type distribution among Q₃ edges
    q3_edges = trans[trans['is_q3_edge']]
    print(f"\n── Q₃ Edge Type Distribution ──")
    for etype in ['比和', '生', '克']:
        count = (q3_edges['edge_type'] == etype).sum()
        pct = 100 * count / len(q3_edges) if len(q3_edges) > 0 else 0
        print(f"  {etype}: {count:>5} ({pct:5.1f}%)")

    # Axis flip distribution among Q₃ edges
    print(f"\n── Axis Flip Distribution (Q₃ edges) ──")
    for axis in ['trend', 'volatility', 'liquidity']:
        count = (q3_edges['flipped_axes'] == axis).sum()
        pct = 100 * count / len(q3_edges) if len(q3_edges) > 0 else 0
        print(f"  {axis}: {count:>5} ({pct:5.1f}%)")


def main():
    bars = load_and_resample()
    bars = construct_axes(bars)
    bars = assign_vertices(bars)
    trans = extract_transitions(bars)

    # Save outputs
    out_cols = [
        'timestamp', 'price', 'trend_4h', 'realized_vol_4h',
        'liq_proxy', 'b0_trend', 'b1_vol', 'b2_liq',
        'vertex', 'trigram', 'element', 'return_next_bar',
    ]
    bars[out_cols].to_csv(BARS_CSV, index=False)
    print(f"\nSaved 4h bars → {BARS_CSV}")

    trans.to_csv(TRANS_CSV, index=False)
    print(f"Saved transitions → {TRANS_CSV}")

    print_summary(bars, trans)


if __name__ == '__main__':
    main()
