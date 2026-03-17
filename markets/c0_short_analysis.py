"""
C0 Short Analysis: Measure hypothetical short returns during C0 (Bear) regime episodes.

Matches the Go strategy's 5-minute debounce by using 5-min subsampled data with
flicker debounce (absorb 1-bar A→B→A patterns).

Date ranges match backtest periods:
  P1: Oct 1 - Oct 29, 2025
  P2: Nov 15 - Dec 13, 2025
  P3: Jan 5 - Feb 2, 2026
  Fwd: Feb 20 - Mar 13, 2026
"""
import numpy as np
import pandas as pd

IS_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2025-07-21_2026-02-20.csv'
FWD_FILE = '/home/quasar/nous/memories/markets/data/btc_datalog_2026-02-20_2026-03-13.csv'
SUBSAMPLE = 300  # 1s → 5min

LEVERAGE = 2.0
FEE_RT = 0.0018  # 0.18% round-trip (0.045% × 2 sides × 2 leverage)

PERIODS = [
    ('P1', '2025-10-01', '2025-10-29', IS_FILE),
    ('P2', '2025-11-15', '2025-12-13', IS_FILE),
    ('P3', '2026-01-05', '2026-02-02', IS_FILE),
    ('Fwd', '2026-02-20', '2026-03-13', FWD_FILE),
]

# v3.0 long PnL from backtests (for combined reporting)
LONG_PNL = {'P1': -1.03, 'P2': -4.92, 'P3': 2.21, 'Fwd': 7.95}

REGIME_NAMES = ['C0(Bear)', 'C1(Rev)', 'C2(Pull)', 'C3(Bull)']


def load_subsample(path, start, end):
    """Load price + trend columns, subsample to 5-min, filter to date range."""
    # 0-indexed: col 1=time_str, col 2=price, col 34=trend_8h, col 37=trend_48h
    df = pd.read_csv(path, usecols=[1, 2, 34, 37],
                     names=['time_str', 'price', 'trend_8h', 'trend_48h'],
                     header=0)
    df = df.iloc[::SUBSAMPLE].reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['time_str'])
    mask = (df['datetime'] >= start) & (df['datetime'] < end)
    return df[mask].reset_index(drop=True)


def classify_regimes(df):
    """2-bit regime from trend signs."""
    b8 = (df['trend_8h'] >= 0).astype(int)
    b48 = (df['trend_48h'] >= 0).astype(int)
    df['regime'] = b8 + 2 * b48
    return df


def detect_episodes(df):
    """Detect regime episodes with flicker debounce (absorb 1-bar A→B→A)."""
    regime = df['regime'].values
    n = len(regime)

    changes = np.where(np.diff(regime) != 0)[0] + 1
    starts = np.concatenate([[0], changes])
    raw_regimes = regime[starts]
    raw_durations = np.diff(np.concatenate([starts, [n]]))

    # Iterative flicker removal
    kept = list(range(len(starts)))
    changed = True
    while changed:
        changed = False
        new_kept = []
        i = 0
        while i < len(kept):
            idx = kept[i]
            if (raw_durations[idx] <= 1
                    and i > 0 and i < len(kept) - 1
                    and raw_regimes[kept[i - 1]] == raw_regimes[kept[i + 1]]):
                changed = True
                i += 1
                continue
            new_kept.append(idx)
            i += 1
        kept = new_kept

    # Merge consecutive same-regime
    merged = []
    for idx in kept:
        r = raw_regimes[idx]
        if merged and merged[-1][1] == r:
            continue
        merged.append((starts[idx], r))

    episodes = []
    for k in range(len(merged)):
        s, r = merged[k]
        e = merged[k + 1][0] if k + 1 < len(merged) else n
        episodes.append({
            'regime': r,
            'start_price': df['price'].iloc[s],
            'end_price': df['price'].iloc[e - 1],
            'start_time': df['datetime'].iloc[s],
            'end_time': df['datetime'].iloc[e - 1],
            'duration_bars': e - s,
        })
    return pd.DataFrame(episodes)


def analyze_c0_shorts(episodes, label):
    """Compute hypothetical short returns for C0 episodes."""
    c0 = episodes[episodes['regime'] == 0].copy()
    if len(c0) == 0:
        return None

    # Short return: profit when price falls
    c0['spot_pct'] = (c0['start_price'] - c0['end_price']) / c0['start_price'] * 100
    c0['duration_h'] = c0['duration_bars'] * 5 / 60
    c0['lev_pct'] = c0['spot_pct'] * LEVERAGE
    c0['fee_pct'] = FEE_RT * 100  # per trade
    c0['net_pct'] = c0['lev_pct'] - c0['fee_pct']

    n = len(c0)
    wins = (c0['spot_pct'] > 0).sum()
    total_spot = c0['spot_pct'].sum()
    total_lev = c0['lev_pct'].sum()
    total_fees = n * FEE_RT * 100
    total_net = total_lev - total_fees

    return {
        'label': label,
        'n_episodes': n,
        'wins': wins,
        'wr': 100 * wins / n,
        'mean_spot': c0['spot_pct'].mean(),
        'median_spot': c0['spot_pct'].median(),
        'total_spot': total_spot,
        'total_lev': total_lev,
        'total_fees': total_fees,
        'total_net': total_net,
        'mean_dur_h': c0['duration_h'].mean(),
        'median_dur_h': c0['duration_h'].median(),
        'episodes': c0,
    }


def main():
    print('=' * 70)
    print('  C0 (Bear) Short Analysis — All Periods')
    print('=' * 70)

    results = []
    for label, start, end, path in PERIODS:
        print(f'\nLoading {label} ({start} to {end})...')
        df = load_subsample(path, start, end)
        if len(df) == 0:
            print(f'  No data for {label}')
            continue

        classify_regimes(df)
        episodes = detect_episodes(df)
        print(f'  {len(df)} bars, {len(episodes)} episodes, '
              f'price {df["price"].min():.0f}-{df["price"].max():.0f}')

        r = analyze_c0_shorts(episodes, label)
        if r is None:
            print(f'  No C0 episodes')
            continue

        results.append(r)

        # Per-episode detail
        c0 = r['episodes']
        print(f'\n  C0 episodes: {r["n_episodes"]}')
        print(f'  {"#":>3s}  {"Start":>20s}  {"Dur":>6s}  {"Entry":>10s}  {"Exit":>10s}  '
              f'{"Spot":>7s}  {"Net2x":>7s}')
        for i, (_, row) in enumerate(c0.iterrows()):
            print(f'  {i+1:3d}  {str(row["start_time"]):>20s}  {row["duration_h"]:>5.1f}h  '
                  f'${row["start_price"]:>9.0f}  ${row["end_price"]:>9.0f}  '
                  f'{row["spot_pct"]:>+6.2f}%  {row["net_pct"]:>+6.2f}%')

        print(f'\n  Summary: {r["wins"]}/{r["n_episodes"]} wins ({r["wr"]:.0f}% WR), '
              f'spot {r["total_spot"]:+.2f}%, net 2x {r["total_net"]:+.2f}%, '
              f'mean dur {r["mean_dur_h"]:.1f}h')

    # Aggregate table
    print('\n' + '=' * 70)
    print('  SUMMARY TABLE')
    print('=' * 70)
    print(f'  {"Period":>6s}  {"Eps":>4s}  {"WR":>5s}  {"Spot":>8s}  {"Lev2x":>8s}  '
          f'{"Fees":>7s}  {"Net":>8s}  {"LongPnL":>8s}  {"Combined":>8s}')
    print(f'  {"------":>6s}  {"----":>4s}  {"-----":>5s}  {"--------":>8s}  {"--------":>8s}  '
          f'{"-------":>7s}  {"--------":>8s}  {"--------":>8s}  {"--------":>8s}')

    total_net = 0
    total_long = 0
    total_combined = 0
    n_positive = 0

    for r in results:
        lbl = r['label']
        long_pnl = LONG_PNL.get(lbl, 0)
        combined = r['total_net'] + long_pnl
        total_net += r['total_net']
        total_long += long_pnl
        total_combined += combined
        if r['total_net'] > 0:
            n_positive += 1

        print(f'  {lbl:>6s}  {r["n_episodes"]:>4d}  {r["wr"]:>4.0f}%  '
              f'{r["total_spot"]:>+7.2f}%  {r["total_lev"]:>+7.2f}%  '
              f'{-r["total_fees"]:>+6.2f}%  {r["total_net"]:>+7.2f}%  '
              f'{long_pnl:>+7.2f}%  {combined:>+7.2f}%')

    print(f'  {"Total":>6s}  {"":>4s}  {"":>5s}  {"":>8s}  {"":>8s}  '
          f'{"":>7s}  {total_net:>+7.2f}%  {total_long:>+7.2f}%  {total_combined:>+7.2f}%')

    # Decision gate
    print('\n' + '=' * 70)
    print('  DECISION GATE')
    print('=' * 70)
    print(f'  C0 shorts net positive in {n_positive}/{len(results)} periods')
    if n_positive >= 3:
        print(f'  → PASS: Proceed to Phase 2 (implement C0 shorts)')
    elif n_positive == 1:
        print(f'  → FAIL: Hedge-only value, skip Phase 2')
    else:
        print(f'  → MARGINAL: {n_positive}/4 positive, review before proceeding')


if __name__ == '__main__':
    main()
