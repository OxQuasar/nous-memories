"""
Round 3: Path geometry of the KW sequence through the 8×8 trigram-pair grid.

Tasks:
  A. Row and column coverage balance
  B. Return times
  C. Step-distance distribution
  D. Trigram sequence projection (autocorrelation, runs, transitions)
  E. Pair footprints on the grid
  F. Within-pair vs bridge geometry comparison
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, TRIGRAMS

RNG = np.random.default_rng(42)
N_TRIALS = 100_000

# ── Constants ────────────────────────────────────────────────────────────────

TRI_ORDER = ["111", "110", "101", "100", "011", "010", "001", "000"]
TRI_NAMES = {b: TRIGRAMS[b] for b in TRI_ORDER}
TRI_IDX = {b: i for i, b in enumerate(TRI_ORDER)}

FAMILY = {
    "111": "father", "000": "mother",
    "100": "son1", "010": "son2", "001": "son3",
    "011": "dau1", "101": "dau2", "110": "dau3",
}
FAMILY_GROUP = {
    "father": "parent", "mother": "parent",
    "son1": "son", "son2": "son", "son3": "son",
    "dau1": "daughter", "dau2": "daughter", "dau3": "daughter",
}


# ── Build hexagram data ──────────────────────────────────────────────────────

hexagrams = []
for idx in range(64):
    num, name, binary = KING_WEN[idx]
    lo, up = binary[:3], binary[3:]
    hexagrams.append({
        'idx': idx, 'num': num, 'name': name, 'binary': binary,
        'lo': lo, 'up': up,
        'lo_name': TRI_NAMES[lo], 'up_name': TRI_NAMES[up],
    })


def hamming3(a, b):
    return sum(c1 != c2 for c1, c2 in zip(a, b))


# ══════════════════════════════════════════════════════════════════════════════
# TASK A: Row and column coverage balance
# ══════════════════════════════════════════════════════════════════════════════

def task_a():
    print("=" * 90)
    print("TASK A: ROW AND COLUMN COVERAGE BALANCE")
    print("=" * 90)

    # For each trigram as lower (row): KW positions of cells in that row
    row_positions = defaultdict(list)
    col_positions = defaultdict(list)
    for h in hexagrams:
        row_positions[h['lo']].append(h['idx'] + 1)  # 1-based position
        col_positions[h['up']].append(h['idx'] + 1)

    print(f"\n  --- Row coverage (lower trigram) ---")
    print(f"  {'Trigram':>8s} {'Name':>8s}  {'Positions':>40s}  "
          f"{'Mean':>6s} {'StdDev':>6s} {'Min':>4s} {'Max':>4s} {'MinGap':>6s} {'MaxGap':>6s}")
    print("  " + "-" * 100)

    row_means = {}
    for tri in TRI_ORDER:
        pos = sorted(row_positions[tri])
        mean = np.mean(pos)
        std = np.std(pos)
        gaps = [pos[i+1] - pos[i] for i in range(len(pos)-1)]
        min_gap = min(gaps) if gaps else 0
        max_gap = max(gaps) if gaps else 0
        row_means[tri] = mean
        pos_str = ','.join(f'{p:2d}' for p in pos)
        print(f"  {tri:>8s} {TRI_NAMES[tri]:>8s}  {pos_str:>40s}  "
              f"{mean:6.1f} {std:6.1f} {min(pos):4d} {max(pos):4d} {min_gap:6d} {max_gap:6d}")

    print(f"\n  --- Column coverage (upper trigram) ---")
    print(f"  {'Trigram':>8s} {'Name':>8s}  {'Positions':>40s}  "
          f"{'Mean':>6s} {'StdDev':>6s} {'Min':>4s} {'Max':>4s} {'MinGap':>6s} {'MaxGap':>6s}")
    print("  " + "-" * 100)

    col_means = {}
    for tri in TRI_ORDER:
        pos = sorted(col_positions[tri])
        mean = np.mean(pos)
        std = np.std(pos)
        gaps = [pos[i+1] - pos[i] for i in range(len(pos)-1)]
        min_gap = min(gaps) if gaps else 0
        max_gap = max(gaps) if gaps else 0
        col_means[tri] = mean
        pos_str = ','.join(f'{p:2d}' for p in pos)
        print(f"  {tri:>8s} {TRI_NAMES[tri]:>8s}  {pos_str:>40s}  "
              f"{mean:6.1f} {std:6.1f} {min(pos):4d} {max(pos):4d} {min_gap:6d} {max_gap:6d}")

    # Significance: compare to random permutation
    # Under null: 64 positions, group into 8 groups of 8. Mean of each group ~ 32.5
    # Variance of group mean = Var(uniform 1-64) / 8 = (64²-1)/12/8 ≈ 42.6
    # So std of group mean ≈ 6.5
    null_mean = 32.5
    null_std_of_mean = np.sqrt((64**2 - 1) / 12.0 / 8)

    print(f"\n  --- Significance test ---")
    print(f"  Null: mean = {null_mean}, std of mean ≈ {null_std_of_mean:.1f}")
    print(f"\n  Row means (z-scores):")
    for tri in TRI_ORDER:
        z = (row_means[tri] - null_mean) / null_std_of_mean
        sig = " *" if abs(z) > 2 else ""
        print(f"    {TRI_NAMES[tri]:>8s}: mean={row_means[tri]:5.1f}, z={z:+.2f}{sig}")

    print(f"\n  Column means (z-scores):")
    for tri in TRI_ORDER:
        z = (col_means[tri] - null_mean) / null_std_of_mean
        sig = " *" if abs(z) > 2 else ""
        print(f"    {TRI_NAMES[tri]:>8s}: mean={col_means[tri]:5.1f}, z={z:+.2f}{sig}")

    # Range of row means and col means
    row_range = max(row_means.values()) - min(row_means.values())
    col_range = max(col_means.values()) - min(col_means.values())
    print(f"\n  Row mean range: {row_range:.1f}")
    print(f"  Column mean range: {col_range:.1f}")

    # MC: range of group means under null
    null_ranges = []
    for _ in range(min(N_TRIALS, 10000)):
        perm = RNG.permutation(64) + 1
        groups = [perm[i*8:(i+1)*8] for i in range(8)]
        means = [np.mean(g) for g in groups]
        null_ranges.append(max(means) - min(means))
    null_ranges = np.array(null_ranges)

    print(f"  Null mean range: {np.mean(null_ranges):.1f} ± {np.std(null_ranges):.1f}")
    p_row = np.mean(null_ranges >= row_range)
    p_col = np.mean(null_ranges >= col_range)
    print(f"  Row range p(≥{row_range:.1f}): {p_row:.4f}")
    print(f"  Col range p(≥{col_range:.1f}): {p_col:.4f}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK B: Return times
# ══════════════════════════════════════════════════════════════════════════════

def task_b():
    print("\n" + "=" * 90)
    print("TASK B: RETURN TIMES")
    print("=" * 90)

    # Return time: gap between consecutive visits to same row (lower trigram)
    lo_seq = [h['lo'] for h in hexagrams]
    up_seq = [h['up'] for h in hexagrams]

    def return_times(seq):
        """Compute return times for each trigram in a sequence."""
        last_seen = {}
        returns = defaultdict(list)
        for i, t in enumerate(seq):
            if t in last_seen:
                returns[t].append(i - last_seen[t])
            last_seen[t] = i
        return returns

    lo_returns = return_times(lo_seq)
    up_returns = return_times(up_seq)

    print(f"\n  --- Lower trigram return times ---")
    print(f"  {'Trigram':>8s} {'Name':>8s}  {'Returns':>35s}  "
          f"{'Mean':>5s} {'Min':>4s} {'Max':>4s} {'Std':>5s}")
    print("  " + "-" * 85)

    all_lo_returns = []
    for tri in TRI_ORDER:
        rets = lo_returns.get(tri, [])
        all_lo_returns.extend(rets)
        ret_str = ','.join(f'{r}' for r in rets)
        if rets:
            print(f"  {tri:>8s} {TRI_NAMES[tri]:>8s}  {ret_str:>35s}  "
                  f"{np.mean(rets):5.1f} {min(rets):4d} {max(rets):4d} {np.std(rets):5.1f}")
        else:
            print(f"  {tri:>8s} {TRI_NAMES[tri]:>8s}  {'(none)':>35s}")

    print(f"\n  --- Upper trigram return times ---")
    print(f"  {'Trigram':>8s} {'Name':>8s}  {'Returns':>35s}  "
          f"{'Mean':>5s} {'Min':>4s} {'Max':>4s} {'Std':>5s}")
    print("  " + "-" * 85)

    all_up_returns = []
    for tri in TRI_ORDER:
        rets = up_returns.get(tri, [])
        all_up_returns.extend(rets)
        ret_str = ','.join(f'{r}' for r in rets)
        if rets:
            print(f"  {tri:>8s} {TRI_NAMES[tri]:>8s}  {ret_str:>35s}  "
                  f"{np.mean(rets):5.1f} {min(rets):4d} {max(rets):4d} {np.std(rets):5.1f}")
        else:
            print(f"  {tri:>8s} {TRI_NAMES[tri]:>8s}  {'(none)':>35s}")

    # Overall stats
    print(f"\n  --- Overall return time statistics ---")
    print(f"  Lower trigram: mean={np.mean(all_lo_returns):.2f}, "
          f"median={np.median(all_lo_returns):.1f}, "
          f"std={np.std(all_lo_returns):.2f}")
    print(f"  Upper trigram: mean={np.mean(all_up_returns):.2f}, "
          f"median={np.median(all_up_returns):.1f}, "
          f"std={np.std(all_up_returns):.2f}")

    # Expected return time for balanced coverage: 64/8 = 8
    print(f"  Expected (balanced): 8.0")

    # Distribution of return times
    lo_hist = Counter(all_lo_returns)
    up_hist = Counter(all_up_returns)
    print(f"\n  Lower return time histogram:")
    for r in sorted(lo_hist.keys()):
        bar = "█" * lo_hist[r]
        print(f"    {r:3d}: {lo_hist[r]:2d} {bar}")

    print(f"\n  Upper return time histogram:")
    for r in sorted(up_hist.keys()):
        bar = "█" * up_hist[r]
        print(f"    {r:3d}: {up_hist[r]:2d} {bar}")

    # Short returns (1-2) indicate clustering
    lo_short = sum(1 for r in all_lo_returns if r <= 2)
    up_short = sum(1 for r in all_up_returns if r <= 2)
    print(f"\n  Short returns (≤2): lower={lo_short}/{len(all_lo_returns)}, "
          f"upper={up_short}/{len(all_up_returns)}")

    # MC: short returns under random permutation
    null_lo_short = []
    null_up_short = []
    for _ in range(min(N_TRIALS, 10000)):
        perm = RNG.permutation(64)
        lo_s = [hexagrams[p]['lo'] for p in perm]
        up_s = [hexagrams[p]['up'] for p in perm]
        lo_r = return_times(lo_s)
        up_r = return_times(up_s)
        all_lo = [r for rets in lo_r.values() for r in rets]
        all_up = [r for rets in up_r.values() for r in rets]
        null_lo_short.append(sum(1 for r in all_lo if r <= 2))
        null_up_short.append(sum(1 for r in all_up if r <= 2))

    null_lo_short = np.array(null_lo_short)
    null_up_short = np.array(null_up_short)
    print(f"  Null short returns: lower mean={np.mean(null_lo_short):.1f}, "
          f"upper mean={np.mean(null_up_short):.1f}")
    p_lo = np.mean(null_lo_short >= lo_short)
    p_up = np.mean(null_up_short >= up_short)
    print(f"  p(≥KW): lower={p_lo:.4f}, upper={p_up:.4f}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK C: Step-distance distribution
# ══════════════════════════════════════════════════════════════════════════════

def task_c():
    print("\n" + "=" * 90)
    print("TASK C: STEP-DISTANCE DISTRIBUTION")
    print("=" * 90)

    within_dists = []
    bridge_dists = []
    within_lo = []
    within_up = []
    bridge_lo = []
    bridge_up = []

    for i in range(63):
        h1 = hexagrams[i]
        h2 = hexagrams[i + 1]
        lo_d = hamming3(h1['lo'], h2['lo'])
        up_d = hamming3(h1['up'], h2['up'])
        total = lo_d + up_d

        if i % 2 == 0:  # within-pair
            within_dists.append(total)
            within_lo.append(lo_d)
            within_up.append(up_d)
        else:  # bridge
            bridge_dists.append(total)
            bridge_lo.append(lo_d)
            bridge_up.append(up_d)

    all_dists = within_dists + bridge_dists

    print(f"\n  --- Distance distributions ---")
    print(f"  {'Dist':>5s}  {'Within(32)':>10s}  {'Bridge(31)':>10s}  {'All(63)':>8s}")
    for d in range(7):
        w = within_dists.count(d)
        b = bridge_dists.count(d)
        a = all_dists.count(d)
        print(f"  {d:5d}  {w:10d}  {b:10d}  {a:8d}")

    print(f"\n  Mean distance: within={np.mean(within_dists):.3f}, "
          f"bridge={np.mean(bridge_dists):.3f}, all={np.mean(all_dists):.3f}")
    print(f"  Std distance:  within={np.std(within_dists):.3f}, "
          f"bridge={np.std(bridge_dists):.3f}")

    # Within-pair: always ≥2 (cross-trigram theorem)
    print(f"\n  Within-pair distance range: [{min(within_dists)}, {max(within_dists)}]")
    print(f"  Within-pair distance histogram:")
    for d in sorted(set(within_dists)):
        cnt = within_dists.count(d)
        bar = "█" * cnt
        print(f"    {d}: {cnt:2d} {bar}")

    print(f"\n  Bridge distance range: [{min(bridge_dists)}, {max(bridge_dists)}]")
    print(f"  Bridge distance histogram:")
    for d in sorted(set(bridge_dists)):
        cnt = bridge_dists.count(d)
        bar = "█" * cnt
        print(f"    {d}: {cnt:2d} {bar}")

    # Component distances
    print(f"\n  --- Component distances ---")
    print(f"  Within-pair: lo_mean={np.mean(within_lo):.3f}, up_mean={np.mean(within_up):.3f}")
    print(f"  Bridge:      lo_mean={np.mean(bridge_lo):.3f}, up_mean={np.mean(bridge_up):.3f}")

    # Within-pair lo and up always equal (forced by generator symmetry)
    lo_eq_up_within = sum(1 for i in range(32) if within_lo[i] == within_up[i])
    print(f"  Within-pair lo_dist == up_dist: {lo_eq_up_within}/32")


# ══════════════════════════════════════════════════════════════════════════════
# TASK D: Trigram sequence projection
# ══════════════════════════════════════════════════════════════════════════════

def task_d():
    print("\n" + "=" * 90)
    print("TASK D: TRIGRAM SEQUENCE PROJECTION")
    print("=" * 90)

    lo_seq = [h['lo'] for h in hexagrams]
    up_seq = [h['up'] for h in hexagrams]

    # Encode as integers for autocorrelation
    lo_int = np.array([TRI_IDX[t] for t in lo_seq])
    up_int = np.array([TRI_IDX[t] for t in up_seq])

    # ── Autocorrelation ──
    print(f"\n  --- Autocorrelation ---")
    print(f"  Using indicator function: AC(lag) = P(same trigram at step k and k+lag) - 1/8")
    print(f"  Under null (random permutation): AC ≈ -1/63 ≈ -0.016 for all lags")

    def autocorr_same(seq, max_lag=16):
        """Fraction of pairs (k, k+lag) with same value, minus 1/8."""
        n = len(seq)
        results = []
        for lag in range(1, max_lag + 1):
            matches = sum(1 for k in range(n - lag) if seq[k] == seq[k + lag])
            total = n - lag
            results.append(matches / total - 1/8)
        return results

    lo_ac = autocorr_same(lo_seq)
    up_ac = autocorr_same(up_seq)

    print(f"\n  {'Lag':>4s}  {'Lower AC':>10s}  {'Upper AC':>10s}")
    for lag in range(16):
        print(f"  {lag+1:4d}  {lo_ac[lag]:+10.4f}  {up_ac[lag]:+10.4f}")

    # MC significance for lag-1 autocorrelation
    null_lo_ac1 = []
    null_up_ac1 = []
    for _ in range(min(N_TRIALS, 10000)):
        perm = RNG.permutation(64)
        lo_s = [hexagrams[p]['lo'] for p in perm]
        up_s = [hexagrams[p]['up'] for p in perm]
        lo_a = autocorr_same(lo_s, max_lag=1)
        up_a = autocorr_same(up_s, max_lag=1)
        null_lo_ac1.append(lo_a[0])
        null_up_ac1.append(up_a[0])

    null_lo_ac1 = np.array(null_lo_ac1)
    null_up_ac1 = np.array(null_up_ac1)

    print(f"\n  Lag-1 autocorrelation significance:")
    print(f"  Lower: KW={lo_ac[0]:+.4f}, null={np.mean(null_lo_ac1):+.4f}±{np.std(null_lo_ac1):.4f}, "
          f"p(≥KW)={np.mean(null_lo_ac1 >= lo_ac[0]):.4f}")
    print(f"  Upper: KW={up_ac[0]:+.4f}, null={np.mean(null_up_ac1):+.4f}±{np.std(null_up_ac1):.4f}, "
          f"p(≥KW)={np.mean(null_up_ac1 >= up_ac[0]):.4f}")

    # ── Run lengths ──
    print(f"\n  --- Run lengths (same row/column streaks) ---")

    def run_lengths(seq):
        """Length of consecutive same-value runs."""
        runs = []
        current = seq[0]
        length = 1
        for i in range(1, len(seq)):
            if seq[i] == current:
                length += 1
            else:
                runs.append((current, length))
                current = seq[i]
                length = 1
        runs.append((current, length))
        return runs

    lo_runs = run_lengths(lo_seq)
    up_runs = run_lengths(up_seq)

    lo_run_lens = [r[1] for r in lo_runs]
    up_run_lens = [r[1] for r in up_runs]

    print(f"  Lower trigram runs: {len(lo_runs)} runs")
    print(f"    Run lengths: {lo_run_lens}")
    print(f"    Max run: {max(lo_run_lens)} (trigram {TRI_NAMES[lo_runs[lo_run_lens.index(max(lo_run_lens))][0]]})")
    print(f"    Mean run: {np.mean(lo_run_lens):.2f}")
    print(f"    Runs > 1: {sum(1 for r in lo_run_lens if r > 1)}")

    print(f"\n  Upper trigram runs: {len(up_runs)} runs")
    print(f"    Run lengths: {up_run_lens}")
    print(f"    Max run: {max(up_run_lens)} (trigram {TRI_NAMES[up_runs[up_run_lens.index(max(up_run_lens))][0]]})")
    print(f"    Mean run: {np.mean(up_run_lens):.2f}")
    print(f"    Runs > 1: {sum(1 for r in up_run_lens if r > 1)}")

    # MC: number of runs under null
    null_lo_nruns = []
    null_up_nruns = []
    for _ in range(min(N_TRIALS, 10000)):
        perm = RNG.permutation(64)
        lo_s = [hexagrams[p]['lo'] for p in perm]
        up_s = [hexagrams[p]['up'] for p in perm]
        null_lo_nruns.append(len(run_lengths(lo_s)))
        null_up_nruns.append(len(run_lengths(up_s)))

    null_lo_nruns = np.array(null_lo_nruns)
    null_up_nruns = np.array(null_up_nruns)

    print(f"\n  Number of runs significance:")
    print(f"  Lower: KW={len(lo_runs)}, null={np.mean(null_lo_nruns):.1f}±{np.std(null_lo_nruns):.1f}, "
          f"p(≤KW)={np.mean(null_lo_nruns <= len(lo_runs)):.4f}")
    print(f"  Upper: KW={len(up_runs)}, null={np.mean(null_up_nruns):.1f}±{np.std(null_up_nruns):.1f}, "
          f"p(≤KW)={np.mean(null_up_nruns <= len(up_runs)):.4f}")

    # ── Transition matrix ──
    print(f"\n  --- Transition matrix (lower trigram) ---")
    lo_trans = defaultdict(lambda: defaultdict(int))
    for i in range(63):
        lo_trans[lo_seq[i]][lo_seq[i+1]] += 1

    header = "  " + " " * 10 + "".join(f"{TRI_NAMES[t]:>8s}" for t in TRI_ORDER)
    print(header)
    for t1 in TRI_ORDER:
        row = f"  {TRI_NAMES[t1]:>8s}  "
        for t2 in TRI_ORDER:
            row += f"{lo_trans[t1][t2]:8d}"
        print(row)

    # Count self-transitions (staying in same row)
    lo_self = sum(lo_trans[t][t] for t in TRI_ORDER)
    print(f"  Self-transitions (same lower): {lo_self}/63")

    print(f"\n  --- Transition matrix (upper trigram) ---")
    up_trans = defaultdict(lambda: defaultdict(int))
    for i in range(63):
        up_trans[up_seq[i]][up_seq[i+1]] += 1

    header = "  " + " " * 10 + "".join(f"{TRI_NAMES[t]:>8s}" for t in TRI_ORDER)
    print(header)
    for t1 in TRI_ORDER:
        row = f"  {TRI_NAMES[t1]:>8s}  "
        for t2 in TRI_ORDER:
            row += f"{up_trans[t1][t2]:8d}"
        print(row)

    up_self = sum(up_trans[t][t] for t in TRI_ORDER)
    print(f"  Self-transitions (same upper): {up_self}/63")

    # MC: self-transitions
    null_lo_self = []
    null_up_self = []
    for _ in range(min(N_TRIALS, 10000)):
        perm = RNG.permutation(64)
        lo_s = [hexagrams[p]['lo'] for p in perm]
        up_s = [hexagrams[p]['up'] for p in perm]
        null_lo_self.append(sum(1 for j in range(63) if lo_s[j] == lo_s[j+1]))
        null_up_self.append(sum(1 for j in range(63) if up_s[j] == up_s[j+1]))

    null_lo_self = np.array(null_lo_self)
    null_up_self = np.array(null_up_self)

    print(f"\n  Self-transition significance:")
    print(f"  Lower: KW={lo_self}, null={np.mean(null_lo_self):.1f}±{np.std(null_lo_self):.1f}, "
          f"p(≥KW)={np.mean(null_lo_self >= lo_self):.4f}")
    print(f"  Upper: KW={up_self}, null={np.mean(null_up_self):.1f}±{np.std(null_up_self):.1f}, "
          f"p(≥KW)={np.mean(null_up_self >= up_self):.4f}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK E: Pair footprints on the grid
# ══════════════════════════════════════════════════════════════════════════════

def task_e():
    print("\n" + "=" * 90)
    print("TASK E: PAIR FOOTPRINTS ON THE GRID")
    print("=" * 90)

    pairs = []
    for k in range(32):
        a = hexagrams[2*k]
        b = hexagrams[2*k + 1]
        lo_d = hamming3(a['lo'], b['lo'])
        up_d = hamming3(a['up'], b['up'])
        total = lo_d + up_d
        pairs.append({
            'k': k, 'a': a, 'b': b,
            'lo_dist': lo_d, 'up_dist': up_d, 'total_dist': total,
        })

    # Pair distance distribution
    print(f"\n  --- Pair distance (grid distance between pair members) ---")
    dist_counter = Counter(p['total_dist'] for p in pairs)
    print(f"  Distribution: {dict(sorted(dist_counter.items()))}")
    print(f"  Mean: {np.mean([p['total_dist'] for p in pairs]):.2f}")
    print(f"  Range: [{min(p['total_dist'] for p in pairs)}, {max(p['total_dist'] for p in pairs)}]")

    # Detailed pair distances
    print(f"\n  {'P':>3s}  {'Hex A':>12s} {'Lo A':>8s}/{'Up A':>8s}  "
          f"{'Hex B':>12s} {'Lo B':>8s}/{'Up B':>8s}  "
          f"{'Lo Δ':>4s} {'Up Δ':>4s} {'Tot':>4s}")
    print("  " + "-" * 90)

    for p in pairs:
        a, b = p['a'], p['b']
        print(f"  {p['k']+1:3d}  {a['name']:>12s} {a['lo_name']:>8s}/{a['up_name']:>8s}  "
              f"{b['name']:>12s} {b['lo_name']:>8s}/{b['up_name']:>8s}  "
              f"{p['lo_dist']:4d} {p['up_dist']:4d} {p['total_dist']:4d}")

    # (lo_dist, up_dist) distribution
    print(f"\n  (lo_dist, up_dist) distribution:")
    pair_dist = Counter((p['lo_dist'], p['up_dist']) for p in pairs)
    for dp, cnt in sorted(pair_dist.items()):
        print(f"    ({dp[0]}, {dp[1]}): {cnt}")

    # Cross-trigram theorem verification: all distances ≥ (1,1)
    min_pairs = [(p['lo_dist'], p['up_dist']) for p in pairs]
    all_both_change = all(d[0] > 0 and d[1] > 0 for d in min_pairs)
    print(f"\n  All pairs have lo_dist>0 AND up_dist>0: {all_both_change} (cross-trigram theorem)")

    # Within-pair: lo_dist always equals up_dist?
    lo_eq_up = sum(1 for p in pairs if p['lo_dist'] == p['up_dist'])
    print(f"  Pairs with lo_dist == up_dist: {lo_eq_up}/32")

    # Family quadrant analysis
    print(f"\n  --- Family quadrant analysis ---")
    # Group trigrams: parent, son, daughter
    quadrant_counter = Counter()
    for p in pairs:
        a, b = p['a'], p['b']
        for h in [a, b]:
            lo_fam = FAMILY_GROUP[FAMILY[h['lo']]]
            up_fam = FAMILY_GROUP[FAMILY[h['up']]]
            quadrant_counter[(lo_fam, up_fam)] += 1

    print(f"  Cell counts by family quadrant (all 64 hexagrams):")
    fam_order = ['parent', 'son', 'daughter']
    header = "  " + " " * 15 + "".join(f"{'Up:'+f:>12s}" for f in fam_order)
    print(header)
    for f1 in fam_order:
        row = f"  {'Lo:'+f1:>13s}  "
        for f2 in fam_order:
            row += f"{quadrant_counter[(f1, f2)]:12d}"
        print(row)

    # Pair footprint: which quadrant pairs span
    print(f"\n  Pair footprints across quadrants:")
    pair_quadrants = Counter()
    for p in pairs:
        a, b = p['a'], p['b']
        q_a = (FAMILY_GROUP[FAMILY[a['lo']]], FAMILY_GROUP[FAMILY[a['up']]])
        q_b = (FAMILY_GROUP[FAMILY[b['lo']]], FAMILY_GROUP[FAMILY[b['up']]])
        key = tuple(sorted([q_a, q_b]))
        pair_quadrants[key] += 1

    for key, cnt in sorted(pair_quadrants.items(), key=lambda x: -x[1]):
        print(f"    {key[0]} ↔ {key[1]}: {cnt}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK F: Within-pair vs bridge geometry comparison
# ══════════════════════════════════════════════════════════════════════════════

def task_f():
    print("\n" + "=" * 90)
    print("TASK F: WITHIN-PAIR vs BRIDGE GEOMETRY")
    print("=" * 90)

    within_lo = []
    within_up = []
    bridge_lo = []
    bridge_up = []

    for i in range(63):
        h1 = hexagrams[i]
        h2 = hexagrams[i + 1]
        lo_d = hamming3(h1['lo'], h2['lo'])
        up_d = hamming3(h1['up'], h2['up'])

        if i % 2 == 0:
            within_lo.append(lo_d)
            within_up.append(up_d)
        else:
            bridge_lo.append(lo_d)
            bridge_up.append(up_d)

    print(f"\n  --- Component distance distributions ---")
    print(f"  Within-pair (32 steps):")
    print(f"    Lo Hamming: {dict(sorted(Counter(within_lo).items()))}")
    print(f"    Up Hamming: {dict(sorted(Counter(within_up).items()))}")
    print(f"    Lo mean: {np.mean(within_lo):.3f}, Up mean: {np.mean(within_up):.3f}")

    print(f"\n  Bridge (31 steps):")
    print(f"    Lo Hamming: {dict(sorted(Counter(bridge_lo).items()))}")
    print(f"    Up Hamming: {dict(sorted(Counter(bridge_up).items()))}")
    print(f"    Lo mean: {np.mean(bridge_lo):.3f}, Up mean: {np.mean(bridge_up):.3f}")

    # Asymmetry: lo vs up within each type
    within_lo_minus_up = [within_lo[i] - within_up[i] for i in range(32)]
    bridge_lo_minus_up = [bridge_lo[i] - bridge_up[i] for i in range(31)]

    print(f"\n  --- Asymmetry (lo_dist - up_dist) ---")
    print(f"  Within-pair: mean={np.mean(within_lo_minus_up):.3f}, "
          f"always zero? {all(d == 0 for d in within_lo_minus_up)}")
    print(f"  Bridge:      mean={np.mean(bridge_lo_minus_up):.3f}")

    # Within-pair: lo always equals up because generators flip equal numbers
    # Verify
    assert all(d == 0 for d in within_lo_minus_up), "Within-pair lo≠up!"
    print(f"\n  CONFIRMED: Within-pair lo_dist always equals up_dist.")
    print(f"  This is forced: each generator flips k bits in lower and k bits in upper.")

    # Bridge lo vs up distribution difference
    print(f"\n  Bridge: lo_dist - up_dist distribution: {dict(sorted(Counter(bridge_lo_minus_up).items()))}")

    # Is bridge lo_dist correlated with bridge up_dist?
    corr = np.corrcoef(bridge_lo, bridge_up)[0, 1]
    print(f"  Bridge lo-up correlation: r = {corr:.3f}")

    # Detailed: generator type determines within-pair distance
    print(f"\n  --- Within-pair distance by generator type ---")
    gen_dists = defaultdict(list)
    for k in range(32):
        a = hexagrams[2*k]
        b = hexagrams[2*k + 1]
        h_a = [int(c) for c in a['binary']]
        sig = (h_a[0] ^ h_a[5], h_a[1] ^ h_a[4], h_a[2] ^ h_a[3])
        gen_names = {(0,0,0):'id', (1,0,0):'O', (0,1,0):'M', (0,0,1):'I',
                     (1,1,0):'OM', (1,0,1):'OI', (0,1,1):'MI', (1,1,1):'OMI'}
        gen = gen_names.get(sig, '?')
        d = hamming3(a['lo'], b['lo'])  # = hamming3(a['up'], b['up'])
        gen_dists[gen].append(d)

    print(f"  {'Gen':>4s}  {'Trigram Δ':>9s}  {'Count':>5s}  {'Total grid Δ':>12s}")
    for gen in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
        dists = gen_dists.get(gen, [])
        if dists:
            d = dists[0]  # all same for a given generator
            print(f"  {gen:>4s}  {d:>9d}  {len(dists):>5d}  {2*d:>12d}")

    # The within-pair distance is determined by the generator:
    # O,M,I → 1 bit each → total 2
    # OM,OI,MI → 2 bits each → total 4
    # OMI → 3 bits each → total 6
    # id (complement) → 3 bits each → total 6


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    task_a()
    task_b()
    task_c()
    task_d()
    task_e()
    task_f()

    print("\n" + "=" * 90)
    print("PATH GEOMETRY ANALYSIS COMPLETE")
    print("=" * 90)
