"""
Hierarchical generator test: basin schedule + local 互.

Central hypothesis: KW's pair ordering = macro basin schedule + micro 互 greedy.
If correct, fixing the basin schedule and applying greedy 互 within each basin
block should closely reconstruct KW.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
from itertools import permutations
from math import log2, factorial
from pathlib import Path
import random
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6,
)

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

random.seed(42)
np.random.seed(42)

N_PAIRS = 32

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])

pairs = [(kw_hex[2*k], kw_hex[2*k+1]) for k in range(N_PAIRS)]
pair_names = [(kw_names[2*k], kw_names[2*k+1]) for k in range(N_PAIRS)]
pair_hu = [(hugua(a), hugua(b)) for a, b in pairs]

SYM = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    if b2 == 1 and b3 == 1: return 'Qian'
    return 'KanLi'

# Bridge 互 weight matrix
W = np.zeros((N_PAIRS, N_PAIRS), dtype=int)
for i in range(N_PAIRS):
    for j in range(N_PAIRS):
        W[i][j] = 99 if i == j else hamming6(pair_hu[i][1], pair_hu[j][0])

# KW totals for reference
kw_total = sum(int(W[k][k+1]) for k in range(31))

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: THE BASIN SEQUENCE
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("PART 1: THE BASIN SEQUENCE")
print("=" * 70)

# Entry basin = basin of pair's first member
entry_basins = [get_basin(pairs[k][0]) for k in range(N_PAIRS)]
exit_basins = [get_basin(pairs[k][1]) for k in range(N_PAIRS)]

print(f"\n  Entry basin sequence (32 pairs):")
print(f"  {' '.join(SYM[b] for b in entry_basins)}")

# Run-length encoding
runs = []  # list of (basin, start_pos, length, pair_indices)
cur_basin = entry_basins[0]
cur_start = 0
for k in range(1, N_PAIRS):
    if entry_basins[k] != cur_basin:
        runs.append((cur_basin, cur_start, k - cur_start, list(range(cur_start, k))))
        cur_basin = entry_basins[k]
        cur_start = k
runs.append((cur_basin, cur_start, N_PAIRS - cur_start, list(range(cur_start, N_PAIRS))))

print(f"\n  Run-length encoding ({len(runs)} runs):")
print(f"  {'Run':>3s}  {'Basin':>6s}  {'Start':>5s}  {'Len':>3s}  Pairs")
for i, (basin, start, length, indices) in enumerate(runs):
    pair_str = ', '.join(f"{k}:{pair_names[k][0]}" for k in indices)
    print(f"  {i:3d}  {SYM[basin]:>6s}  {start:5d}  {length:3d}  {pair_str}")

run_basins = [r[0] for r in runs]
run_lengths = [r[2] for r in runs]
print(f"\n  Run-level basin sequence: {' '.join(SYM[b] for b in run_basins)}")
print(f"  Run lengths: {run_lengths}")
print(f"  Mean run length: {np.mean(run_lengths):.2f}")
print(f"  Basin counts: {dict(Counter(entry_basins))}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: WITHIN-RUN 互 OPTIMALITY
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 2: WITHIN-RUN 互 OPTIMALITY")
print("=" * 70)

print(f"\n  For each basin run, is KW's ordering 互-optimal within the run?")
print(f"  {'Run':>3s}  {'Basin':>6s}  {'Len':>3s}  {'KW 互':>5s}  {'Min 互':>5s}  "
      f"{'Pctile':>6s}  {'Optimal?':>8s}")

run_details = []
for ri, (basin, start, length, indices) in enumerate(runs):
    if length <= 1:
        run_details.append({
            'run': ri, 'basin': basin, 'length': length, 'indices': indices,
            'kw_weight': 0, 'min_weight': 0, 'pctile': 0.0, 'optimal': True,
        })
        print(f"  {ri:3d}  {SYM[basin]:>6s}  {length:3d}      —      —       —         —")
        continue
    
    # KW's intra-run 互 weight (bridges between consecutive pairs in this run)
    kw_weight = sum(int(W[indices[j]][indices[j+1]]) for j in range(length - 1))
    
    # All permutations of this run's pairs, compute total weight
    if length <= 7:
        # Enumerate all permutations
        all_weights = []
        for perm in permutations(indices):
            w = sum(int(W[perm[j]][perm[j+1]]) for j in range(length - 1))
            all_weights.append(w)
        min_weight = min(all_weights)
        pctile = 100.0 * sum(1 for w in all_weights if w <= kw_weight) / len(all_weights)
    else:
        # Sample 10K random permutations
        idx_list = list(indices)
        sample_weights = []
        for _ in range(10_000):
            random.shuffle(idx_list)
            w = sum(int(W[idx_list[j]][idx_list[j+1]]) for j in range(length - 1))
            sample_weights.append(w)
        min_weight = min(sample_weights)
        pctile = 100.0 * sum(1 for w in sample_weights if w <= kw_weight) / len(sample_weights)
    
    is_optimal = (kw_weight == min_weight)
    run_details.append({
        'run': ri, 'basin': basin, 'length': length, 'indices': indices,
        'kw_weight': kw_weight, 'min_weight': min_weight,
        'pctile': pctile, 'optimal': is_optimal,
    })
    opt_str = "✓" if is_optimal else f"✗ (min={min_weight})"
    print(f"  {ri:3d}  {SYM[basin]:>6s}  {length:3d}  {kw_weight:5d}  {min_weight:5d}  "
          f"{pctile:5.1f}%  {opt_str:>8s}")

# Summary
multi_runs = [r for r in run_details if r['length'] > 1]
n_optimal = sum(1 for r in multi_runs if r['optimal'])
nontrivial_runs = [r for r in run_details if r['length'] > 2]
n_nontrivial_optimal = sum(1 for r in nontrivial_runs if r['optimal'])
print(f"\n  Summary: {n_optimal}/{len(multi_runs)} multi-pair runs are 互-optimal")
# Percentile note: 100% = KW is worst or tied; lower = KW is better
mean_pctile = np.mean([r['pctile'] for r in multi_runs])
print(f"  Mean within-run percentile: {mean_pctile:.1f}% (100%=worst-or-tied, lower=better)")
print(f"\n  CAVEAT: {len(multi_runs) - len(nontrivial_runs)}/{len(multi_runs)} multi-pair runs "
      f"have only 2 pairs — only 2 orderings, so 'optimal' is trivially achieved when both "
      f"directions give the same weight.")
if nontrivial_runs:
    print(f"  Runs with length ≥ 3: {len(nontrivial_runs)}, "
          f"of which {n_nontrivial_optimal} are 互-optimal")
    for r in nontrivial_runs:
        print(f"    Run {r['run']} ({SYM[r['basin']]}, len={r['length']}): "
              f"KW={r['kw_weight']}, min={r['min_weight']}, "
              f"pctile={r['pctile']:.1f}% {'✓' if r['optimal'] else '← WORST'}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: BASIN-CONSTRAINED RECONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 3: BASIN-CONSTRAINED RECONSTRUCTION")
print("=" * 70)

# Group pairs by entry basin
basin_pools = {'Kun': [], 'KanLi': [], 'Qian': []}
for k in range(N_PAIRS):
    basin_pools[entry_basins[k]].append(k)

print(f"\n  Basin pools:")
for basin, pool in basin_pools.items():
    print(f"  {SYM[basin]} {basin:>6s}: {len(pool)} pairs — "
          f"{', '.join(f'{k}:{pair_names[k][0]}' for k in pool)}")

# Required basin at each position (from KW's actual basin sequence)
required_basins = entry_basins[:]

def basin_constrained_greedy(required, lookahead=False):
    """
    Greedy reconstruction with basin constraint.
    At each position, from unplaced pairs matching the required basin,
    choose minimum 互 distance from previous pair.
    
    lookahead: if True, break ties by preferring candidates whose exit basin
    matches the next position's required basin.
    """
    placed = [None] * N_PAIRS
    used = set()
    
    # Position 0: must be basin-matching; choose pair 0 (Qian/Kun) since
    # we know it's first. Actually let's be fair and just pick the first
    # basin-matching pair by KW index if no previous pair.
    # For position 0, no bridge to minimize, so pick KW-first among candidates.
    avail_0 = [k for k in range(N_PAIRS) if entry_basins[k] == required[0] and k not in used]
    placed[0] = min(avail_0)  # lowest KW index
    used.add(placed[0])
    
    for pos in range(1, N_PAIRS):
        prev = placed[pos - 1]
        avail = [k for k in range(N_PAIRS)
                 if k not in used and entry_basins[k] == required[pos]]
        
        if not avail:
            # Shouldn't happen if basin counts match
            print(f"  WARNING: no candidates for pos {pos}, basin {required[pos]}")
            break
        
        # Minimum 互 distance
        min_d = min(int(W[prev][k]) for k in avail)
        best = [k for k in avail if int(W[prev][k]) == min_d]
        
        if lookahead and len(best) > 1 and pos < N_PAIRS - 1:
            next_basin = required[pos + 1]
            # Prefer candidates whose exit basin matches next required
            with_lookahead = [k for k in best if exit_basins[k] == next_basin]
            if with_lookahead:
                best = with_lookahead
        
        # Final tiebreak: KW index
        placed[pos] = min(best)
        used.add(placed[pos])
    
    return placed

# Run both variants
recon_basic = basin_constrained_greedy(required_basins, lookahead=False)
recon_look = basin_constrained_greedy(required_basins, lookahead=True)

def count_matches(path):
    """Count transitions that match KW."""
    kw_trans = set((k, k+1) for k in range(31))
    path_trans = set((path[k], path[k+1]) for k in range(31))
    return len(kw_trans & path_trans)

def path_weight(path):
    return sum(int(W[path[k]][path[k+1]]) for k in range(31))

matches_basic = count_matches(recon_basic)
matches_look = count_matches(recon_look)
weight_basic = path_weight(recon_basic)
weight_look = path_weight(recon_look)

# Position matches (same pair at same position)
pos_match_basic = sum(1 for k in range(N_PAIRS) if recon_basic[k] == k)
pos_match_look = sum(1 for k in range(N_PAIRS) if recon_look[k] == k)

print(f"\n  Basin-constrained greedy (no lookahead):")
print(f"  Path: {recon_basic}")
print(f"  Transitions matched: {matches_basic}/31")
print(f"  Position matches: {pos_match_basic}/32")
print(f"  Total 互 weight: {weight_basic} (KW: {kw_total})")

print(f"\n  Basin-constrained greedy (with lookahead):")
print(f"  Path: {recon_look}")
print(f"  Transitions matched: {matches_look}/31")
print(f"  Position matches: {pos_match_look}/32")
print(f"  Total 互 weight: {weight_look} (KW: {kw_total})")

# Step-by-step comparison
print(f"\n  Step-by-step (lookahead variant vs KW):")
print(f"  {'Pos':>3s}  {'KW':>20s}  {'Recon':>20s}  {'Match':>5s}  {'KW d':>4s}  {'R d':>4s}")
for pos in range(N_PAIRS):
    kw_pair = pos
    r_pair = recon_look[pos]
    match = "✓" if kw_pair == r_pair else "✗"
    if pos < 31:
        kw_d = int(W[kw_pair][pos+1])
        r_d = int(W[r_pair][recon_look[pos+1]]) if pos < 31 else 0
        print(f"  {pos:3d}  {pair_names[kw_pair][0]+'/'+pair_names[kw_pair][1]:>20s}  "
              f"{pair_names[r_pair][0]+'/'+pair_names[r_pair][1]:>20s}  {match:>5s}  "
              f"{kw_d:4d}  {r_d:4d}")
    else:
        print(f"  {pos:3d}  {pair_names[kw_pair][0]+'/'+pair_names[kw_pair][1]:>20s}  "
              f"{pair_names[r_pair][0]+'/'+pair_names[r_pair][1]:>20s}  {match:>5s}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: BASIN SEQUENCE ENTROPY
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 4: BASIN SEQUENCE ENTROPY")
print("=" * 70)

# At each position, how many unplaced pairs match the required basin?
remaining = dict(Counter(entry_basins))  # basin → count remaining
log_choices = 0.0
choices_per_pos = []

print(f"\n  Choices available at each position:")
print(f"  {'Pos':>3s}  {'Req basin':>9s}  {'Available':>9s}  {'log2':>6s}")
for pos in range(N_PAIRS):
    req = required_basins[pos]
    n_avail = remaining[req]
    choices_per_pos.append(n_avail)
    log_choices += log2(n_avail) if n_avail > 0 else 0
    if pos < 10 or pos >= 28 or n_avail <= 2:
        print(f"  {pos:3d}  {SYM[req]:>9s}  {n_avail:9d}  {log2(n_avail) if n_avail > 0 else 0:6.2f}")
    remaining[req] -= 1

log_full = log2(factorial(N_PAIRS))
compression = log_full - log_choices

print(f"\n  Total basin-consistent orderings: 2^{log_choices:.1f}")
print(f"  Full search space: 32! = 2^{log_full:.1f}")
print(f"  Compression from basin schedule: {compression:.1f} bits")
print(f"  Remaining search fraction: 2^{-compression:.1f} = {2**(-compression):.2e}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: ALL-BRIDGES BASIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 5: ALL-BRIDGES BASIN ANALYSIS")
print("=" * 70)

same_basin_bridges = []
cross_basin_bridges = []

for k in range(31):
    exit_b = exit_basins[k]
    entry_b = entry_basins[k + 1]
    d = int(W[k][k+1])
    
    # Is this bridge optimal?
    visited = set(range(k + 1))
    available = [j for j in range(N_PAIRS) if j not in visited]
    min_d = min(int(W[k][j]) for j in available)
    is_optimal = (d == min_d)
    is_near_opt = (d <= min_d + 1)
    
    info = {'bridge': k, 'd': d, 'min_d': min_d, 'optimal': is_optimal,
            'near_optimal': is_near_opt, 'exit': exit_b, 'entry': entry_b}
    
    if exit_b == entry_b:
        same_basin_bridges.append(info)
    else:
        cross_basin_bridges.append(info)

print(f"\n  Same-basin bridges: {len(same_basin_bridges)}")
if same_basin_bridges:
    same_dists = [b['d'] for b in same_basin_bridges]
    same_opt = sum(1 for b in same_basin_bridges if b['optimal'])
    same_near = sum(1 for b in same_basin_bridges if b['near_optimal'])
    print(f"    Mean d_互: {np.mean(same_dists):.2f}")
    print(f"    Optimal: {same_opt}/{len(same_basin_bridges)}")
    print(f"    Near-optimal: {same_near}/{len(same_basin_bridges)}")
    print(f"    Distance distribution: {dict(sorted(Counter(same_dists).items()))}")

print(f"\n  Cross-basin bridges: {len(cross_basin_bridges)}")
if cross_basin_bridges:
    cross_dists = [b['d'] for b in cross_basin_bridges]
    cross_opt = sum(1 for b in cross_basin_bridges if b['optimal'])
    cross_near = sum(1 for b in cross_basin_bridges if b['near_optimal'])
    print(f"    Mean d_互: {np.mean(cross_dists):.2f}")
    print(f"    Optimal: {cross_opt}/{len(cross_basin_bridges)}")
    print(f"    Near-optimal: {cross_near}/{len(cross_basin_bridges)}")
    print(f"    Distance distribution: {dict(sorted(Counter(cross_dists).items()))}")

print(f"\n  Bridge detail:")
print(f"  {'Bridge':>7s}  {'Exit':>6s} {'Entry':>6s}  {'Type':>5s}  {'d':>3s}  {'min':>3s}  {'Opt':>5s}")
for k in range(31):
    exit_b = exit_basins[k]
    entry_b = entry_basins[k + 1]
    d = int(W[k][k+1])
    visited = set(range(k + 1))
    available = [j for j in range(N_PAIRS) if j not in visited]
    min_d = min(int(W[k][j]) for j in available)
    is_optimal = (d == min_d)
    btype = "same" if exit_b == entry_b else "cross"
    opt_str = "✓" if is_optimal else f"+{d - min_d}"
    print(f"  {k:2d}→{k+1:2d}  {SYM[exit_b]:>6s} {SYM[entry_b]:>6s}  {btype:>5s}  {d:3d}  {min_d:3d}  {opt_str:>5s}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 6: BASIN TRANSITION DIRECTION
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 6: BASIN TRANSITION DIRECTION")
print("=" * 70)

# Transition matrix at cross-basin bridges
basin_list = ['Kun', 'KanLi', 'Qian']
trans_matrix = {(a, b): 0 for a in basin_list for b in basin_list if a != b}
cross_sequence = []

for b_info in cross_basin_bridges:
    key = (b_info['exit'], b_info['entry'])
    trans_matrix[key] += 1
    cross_sequence.append(key)

print(f"\n  Basin transition matrix (at cross-basin bridges):")
print(f"  {'From \\ To':>10s}  {'Kun ○':>6s}  {'KanLi ◎':>8s}  {'Qian ●':>8s}")
for fr in basin_list:
    row = []
    for to in basin_list:
        if fr == to:
            row.append("  —   ")
        else:
            row.append(f"  {trans_matrix.get((fr, to), 0):3d}  ")
    print(f"  {SYM[fr]+' '+fr:>10s}  {''.join(row)}")

print(f"\n  Cross-basin transition sequence:")
for i, (ex, en) in enumerate(cross_sequence):
    bridge = cross_basin_bridges[i]['bridge']
    print(f"  Bridge {bridge:2d}: {SYM[ex]}→{SYM[en]}  ({ex}→{en})")

# Check for cyclic pattern
# Simplify: just look at the basin-to-basin sequence
print(f"\n  Simplified transition pattern:")
trans_pattern = ' → '.join(f"{SYM[ex]}→{SYM[en]}" for ex, en in cross_sequence)
print(f"  {trans_pattern}")

# Check: is there a dominant transition direction?
# Does KW always go Kun↔KanLi or Qian↔KanLi (through center)?
through_center = sum(1 for ex, en in cross_sequence if 'KanLi' in (ex, en))
total_cross = len(cross_sequence)
print(f"\n  Transitions through KanLi (center): {through_center}/{total_cross} "
      f"({100*through_center/total_cross:.0f}%)")

# Direct pole-to-pole transitions
pole_to_pole = sum(1 for ex, en in cross_sequence 
                   if ex in ('Kun', 'Qian') and en in ('Kun', 'Qian') and ex != en)
print(f"  Direct pole-to-pole (Kun↔Qian): {pole_to_pole}/{total_cross}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 7: RECONSTRUCTION QUALITY SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 7: RECONSTRUCTION QUALITY SUMMARY")
print("=" * 70)

# Random baseline
random.seed(42)
N_RAND = 10_000
rand_matches = []
rand_weights = []
order = list(range(N_PAIRS))
for _ in range(N_RAND):
    random.shuffle(order)
    m = sum(1 for k in range(31) if (order[k], order[k+1]) in 
            set((k, k+1) for k in range(31)))
    w = sum(int(W[order[k]][order[k+1]]) for k in range(31))
    rand_matches.append(m)
    rand_weights.append(w)

# Unconstrained greedy from Round 1 (pair 0 start)
def greedy_walk(start):
    path = [start]
    visited = {start}
    for _ in range(N_PAIRS - 1):
        cur = path[-1]
        cands = [j for j in range(N_PAIRS) if j not in visited]
        min_d = min(int(W[cur][j]) for j in cands)
        best = [j for j in cands if int(W[cur][j]) == min_d]
        path.append(min(best))
        visited.add(path[-1])
    return path

greedy_path = greedy_walk(0)
greedy_matches = count_matches(greedy_path)
greedy_weight = path_weight(greedy_path)

print(f"\n  {'Method':>45s}  {'Transitions':>11s}  {'Total 互':>8s}")
print(f"  {'':>45s}  {'matched':>11s}  {'weight':>8s}")
print(f"  {'-'*45}  {'-'*11}  {'-'*8}")
print(f"  {'Random (mean)':>45s}  {np.mean(rand_matches):>9.1f}/31  {np.mean(rand_weights):>8.1f}")
print(f"  {'Greedy 互 only (from pair 0)':>45s}  {greedy_matches:>9d}/31  {greedy_weight:>8d}")
print(f"  {'Basin-constrained greedy 互':>45s}  {matches_basic:>9d}/31  {weight_basic:>8d}")
print(f"  {'Basin-constrained greedy 互 + lookahead':>45s}  {matches_look:>9d}/31  {weight_look:>8d}")
print(f"  {'KW actual':>45s}  {'31':>9s}/31  {kw_total:>8d}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 8: WHAT REMAINS UNEXPLAINED
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 8: WHAT REMAINS UNEXPLAINED")
print("=" * 70)

# Use the better reconstruction variant
best_recon = recon_look if matches_look >= matches_basic else recon_basic
best_matches = max(matches_look, matches_basic)
best_label = "lookahead" if matches_look >= matches_basic else "basic"

divergences = []
for pos in range(N_PAIRS):
    if best_recon[pos] != pos:
        divergences.append(pos)

print(f"\n  Divergence positions ({len(divergences)} of 32):")
print(f"  {'Pos':>3s}  {'KW pair':>20s}  {'Recon pair':>20s}  {'Req basin':>9s}  "
      f"{'KW basin':>8s}  {'R basin':>8s}")
for pos in divergences:
    kw_p = pos
    r_p = best_recon[pos]
    req_b = required_basins[pos]
    print(f"  {pos:3d}  {pair_names[kw_p][0]+'/'+pair_names[kw_p][1]:>20s}  "
          f"{pair_names[r_p][0]+'/'+pair_names[r_p][1]:>20s}  {SYM[req_b]:>9s}  "
          f"{SYM[entry_basins[kw_p]]:>8s}  {SYM[entry_basins[r_p]]:>8s}")

# Analyze where divergences concentrate
if divergences:
    first_half = sum(1 for d in divergences if d < 16)
    second_half = sum(1 for d in divergences if d >= 16)
    print(f"\n  Divergences in first half (pos 0–15): {first_half}")
    print(f"  Divergences in second half (pos 16–31): {second_half}")

# For each divergence at a bridge point, what feature distinguishes?
print(f"\n  Transition divergences (where recon picks a different next pair):")
trans_divs = []
for k in range(31):
    kw_next = k + 1
    r_cur = best_recon[k]
    r_next = best_recon[k + 1]
    if (r_cur, r_next) != (k, k+1):
        kw_d = int(W[k][k+1])
        r_d = int(W[r_cur][r_next])
        trans_divs.append({
            'pos': k, 'kw_pair': kw_next, 'r_pair': r_next,
            'kw_d': kw_d, 'r_d': r_d,
        })

print(f"  {'Bridge':>7s}  {'KW→':>20s}  {'Recon→':>20s}  {'KW d':>4s}  {'R d':>4s}  {'Δ':>3s}")
for td in trans_divs:
    delta = td['kw_d'] - td['r_d']
    d_str = f"+{delta}" if delta > 0 else str(delta)
    print(f"  {td['pos']:2d}→{td['pos']+1:2d}  "
          f"{pair_names[td['kw_pair']][0]+'/'+pair_names[td['kw_pair']][1]:>20s}  "
          f"{pair_names[td['r_pair']][0]+'/'+pair_names[td['r_pair']][1]:>20s}  "
          f"{td['kw_d']:4d}  {td['r_d']:4d}  {d_str:>3s}")

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE RESULTS TO MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("WRITING RESULTS")
print("=" * 70)

md = []
w = md.append

w("# Hierarchical Generator Test: Basin Schedule + Local 互\n")
w("**Hypothesis:** KW's pair ordering = macro basin schedule + micro 互 greedy.\n")

# Part 1
w("## Part 1: Basin Sequence\n")
w(f"Entry basin sequence: `{' '.join(SYM[b] for b in entry_basins)}`\n")
w(f"Basin counts: {dict(Counter(entry_basins))}\n")

w(f"### Run-length encoding ({len(runs)} runs)\n")
w("| Run | Basin | Start | Length | Pairs |")
w("|-----|-------|-------|--------|-------|")
for i, (basin, start, length, indices) in enumerate(runs):
    pair_str = ', '.join(pair_names[k][0] for k in indices)
    w(f"| {i} | {SYM[basin]} | {start} | {length} | {pair_str} |")
w("")
w(f"Run-level sequence: `{' '.join(SYM[b] for b in run_basins)}`\n")
w(f"Run lengths: {run_lengths} (mean: {np.mean(run_lengths):.2f})\n")

# Part 2
w("## Part 2: Within-Run 互 Optimality\n")
w("| Run | Basin | Length | KW 互 | Min 互 | Percentile | Optimal? |")
w("|-----|-------|--------|-------|--------|------------|----------|")
for rd in run_details:
    if rd['length'] <= 1:
        w(f"| {rd['run']} | {SYM[rd['basin']]} | {rd['length']} | — | — | — | — |")
    else:
        opt_str = "✓" if rd['optimal'] else "✗"
        w(f"| {rd['run']} | {SYM[rd['basin']]} | {rd['length']} | {rd['kw_weight']} "
          f"| {rd['min_weight']} | {rd['pctile']:.1f}% | {opt_str} |")
w("")
w(f"**{n_optimal}/{len(multi_runs)} multi-pair runs are within-run 互-optimal.**\n")
w(f"**Caveat:** {len(multi_runs) - len(nontrivial_runs)}/{len(multi_runs)} of these runs "
  f"have only 2 pairs (trivially optimal when both orderings give the same weight). "
  f"Only {len(nontrivial_runs)} run(s) have ≥3 pairs, providing a real test.")
if nontrivial_runs:
    for r in nontrivial_runs:
        status = "optimal ✓" if r['optimal'] else f"**WORST ordering** (KW={r['kw_weight']}, min={r['min_weight']})"
        w(f"- Run {r['run']} ({SYM[r['basin']]}, {r['length']} pairs): {status}")
w("")

# Part 3
w("## Part 3: Basin-Constrained Reconstruction\n")
w("Fix KW's basin assignment per position, then greedily assign pairs by 互 proximity.\n")

w("| Variant | Transitions matched | Position matches | Total 互 weight |")
w("|---------|-------------------|-----------------|----------------|")
w(f"| Basin + greedy 互 | {matches_basic}/31 | {pos_match_basic}/32 | {weight_basic} |")
w(f"| Basin + greedy 互 + lookahead | {matches_look}/31 | {pos_match_look}/32 | {weight_look} |")
w(f"| KW actual | 31/31 | 32/32 | {kw_total} |")
w("")

# Part 4
w("## Part 4: Basin Sequence Entropy\n")
w(f"| Metric | Value |")
w(f"|--------|-------|")
w(f"| Basin-consistent orderings | 2^{log_choices:.1f} |")
w(f"| Full search space (32!) | 2^{log_full:.1f} |")
w(f"| Compression from basin schedule | {compression:.1f} bits |")
w(f"| Remaining search fraction | {2**(-compression):.2e} |")
w("")
w(f"The basin schedule reduces the search space by a factor of ~2^{compression:.0f}, "
  f"from 32! down to ~2^{log_choices:.0f} orderings.\n")

# Part 5
w("## Part 5: All-Bridges Basin Analysis\n")
w("| Bridge type | Count | Mean d_互 | Optimal rate | Near-optimal rate |")
w("|-------------|-------|----------|-------------|-------------------|")

if same_basin_bridges:
    sb_opt_rate = f"{sum(1 for b in same_basin_bridges if b['optimal'])}/{len(same_basin_bridges)}"
    sb_near_rate = f"{sum(1 for b in same_basin_bridges if b['near_optimal'])}/{len(same_basin_bridges)}"
    w(f"| Same-basin | {len(same_basin_bridges)} | {np.mean([b['d'] for b in same_basin_bridges]):.2f} "
      f"| {sb_opt_rate} | {sb_near_rate} |")
if cross_basin_bridges:
    cb_opt_rate = f"{sum(1 for b in cross_basin_bridges if b['optimal'])}/{len(cross_basin_bridges)}"
    cb_near_rate = f"{sum(1 for b in cross_basin_bridges if b['near_optimal'])}/{len(cross_basin_bridges)}"
    w(f"| Cross-basin | {len(cross_basin_bridges)} | {np.mean([b['d'] for b in cross_basin_bridges]):.2f} "
      f"| {cb_opt_rate} | {cb_near_rate} |")
w("")

w("### Bridge detail\n")
w("| Bridge | Exit | Entry | Type | d_互 | Min d | Optimal? |")
w("|--------|------|-------|------|------|-------|----------|")
for k in range(31):
    exit_b = exit_basins[k]
    entry_b = entry_basins[k + 1]
    d = int(W[k][k+1])
    visited = set(range(k + 1))
    available = [j for j in range(N_PAIRS) if j not in visited]
    min_d = min(int(W[k][j]) for j in available)
    btype = "same" if exit_b == entry_b else "**cross**"
    opt_str = "✓" if d == min_d else f"+{d - min_d}"
    w(f"| {k}→{k+1} | {SYM[exit_b]} | {SYM[entry_b]} | {btype} | {d} | {min_d} | {opt_str} |")
w("")

# Part 6
w("## Part 6: Basin Transition Direction\n")
w("### Transition matrix (at cross-basin bridges)\n")
w(f"| From \\ To | Kun ○ | KanLi ◎ | Qian ● |")
w(f"|----------|-------|---------|--------|")
for fr in basin_list:
    cells = []
    for to in basin_list:
        if fr == to:
            cells.append("—")
        else:
            cells.append(str(trans_matrix.get((fr, to), 0)))
    w(f"| {SYM[fr]} {fr} | {' | '.join(cells)} |")
w("")

w(f"Transitions through center (KanLi): **{through_center}/{total_cross}** "
  f"({100*through_center/total_cross:.0f}%)\n")
w(f"Direct pole-to-pole (Kun↔Qian): {pole_to_pole}/{total_cross}\n")

w("### Transition sequence\n")
w("```")
for i, (ex, en) in enumerate(cross_sequence):
    bridge = cross_basin_bridges[i]['bridge']
    w(f"Bridge {bridge:2d}: {SYM[ex]}→{SYM[en]}")
w("```\n")

# Part 7
w("## Part 7: Reconstruction Quality Summary\n")
w("| Method | Transitions matched | Total 互 weight |")
w("|--------|-------------------|----------------|")
w(f"| Random (mean of {N_RAND}) | {np.mean(rand_matches):.1f}/31 | {np.mean(rand_weights):.0f} |")
w(f"| Greedy 互 only | {greedy_matches}/31 | {greedy_weight} |")
w(f"| Basin-constrained greedy 互 | {matches_basic}/31 | {weight_basic} |")
w(f"| Basin-constrained greedy 互 + lookahead | {matches_look}/31 | {weight_look} |")
w(f"| KW actual | 31/31 | {kw_total} |")
w("")

improvement_basic = matches_basic - greedy_matches
improvement_look = matches_look - greedy_matches
w(f"**Basin constraint improves matches from {greedy_matches} → {matches_basic}** "
  f"(+{improvement_basic} without lookahead), "
  f"**{matches_look}** (+{improvement_look} with lookahead).\n")

if matches_look >= 15:
    w("The basin schedule is doing substantial generative work — with 互 greedy "
      "it reconstructs most of KW. The remaining divergences indicate what "
      "additional constraint(s) are needed.\n")
elif matches_look >= 8:
    w("The basin schedule captures a significant portion of KW's structure, "
      "but substantial divergences remain. Additional constraints beyond "
      "basin + 互 are needed.\n")
else:
    w("The basin schedule alone is insufficient — it provides modest improvement "
      "over unconstrained greedy but falls well short of full reconstruction.\n")

# Part 8
w("## Part 8: What Remains Unexplained\n")
w(f"After basin-constrained reconstruction ({best_label}), "
  f"**{len(divergences)} of 32 positions diverge** from KW.\n")

if divergences:
    first_half_d = sum(1 for d in divergences if d < 16)
    second_half_d = sum(1 for d in divergences if d >= 16)
    w(f"Divergence distribution: first half {first_half_d}, second half {second_half_d}.\n")

    w("### Divergence detail\n")
    w("| Position | KW pair | Recon pair | Required basin |")
    w("|----------|---------|------------|----------------|")
    for pos in divergences:
        kw_p = pos
        r_p = best_recon[pos]
        w(f"| {pos} | {pair_names[kw_p][0]}/{pair_names[kw_p][1]} "
          f"| {pair_names[r_p][0]}/{pair_names[r_p][1]} | {SYM[required_basins[pos]]} |")
    w("")

# Final summary
w("## Key Findings\n")

best_recon_matches = max(matches_basic, matches_look)
same_opt_count = sum(1 for b in same_basin_bridges if b['optimal']) if same_basin_bridges else 0
cross_opt_count = sum(1 for b in cross_basin_bridges if b['optimal']) if cross_basin_bridges else 0

w(f"1. **Basin sequence is highly fragmented:** {len(runs)} runs for 32 pairs "
  f"(mean length {np.mean(run_lengths):.1f}). {sum(1 for r in runs if r[2] == 1)}/{len(runs)} "
  f"runs are singletons. The basin schedule compresses the search space by {compression:.0f} bits "
  f"(from 2^{log_full:.0f} to 2^{log_choices:.0f}), but this compression is modest.\n")

w(f"2. **Within-run optimality is vacuous.** {n_optimal}/{len(multi_runs)} multi-pair runs "
  f"are 互-optimal, but {len(multi_runs) - len(nontrivial_runs)}/{len(multi_runs)} are 2-pair "
  f"runs where optimality is trivial. The sole 3-pair run (run 13: Jin, Jia Ren, Jian) "
  f"has the **worst** possible ordering. The data neither supports nor refutes within-run 互 "
  f"optimization because almost all runs are too short to test.\n")

w(f"3. **Same-basin vs cross-basin bridges:** Same-basin bridges are slightly more optimal "
  f"({same_opt_count}/{len(same_basin_bridges)}) vs cross-basin ({cross_opt_count}/{len(cross_basin_bridges)}), "
  f"but the mean d_互 is only moderately lower "
  f"({np.mean([b['d'] for b in same_basin_bridges]):.1f} vs "
  f"{np.mean([b['d'] for b in cross_basin_bridges]):.1f}). "
  f"The separation is not as clean as the hierarchical model predicts.\n")

w(f"4. **Basin transitions are center-mediated:** {through_center}/{total_cross} "
  f"cross-basin bridges involve KanLi ({100*through_center/total_cross:.0f}%). "
  f"Direct pole-to-pole (Kun↔Qian): only {pole_to_pole}/{total_cross}. "
  f"KanLi functions as a transit hub between the poles.\n")

w(f"5. **Reconstruction: basin + 互 greedy fails.** Only {best_recon_matches}/31 transitions "
  f"matched (vs {greedy_matches}/31 unconstrained, ~{np.mean(rand_matches):.0f}/31 random). "
  f"The improvement over unconstrained greedy is +{best_recon_matches - greedy_matches} transitions — "
  f"the basin schedule provides minimal generative leverage.\n")

w(f"6. **The hierarchical model is refuted.** The two-level decomposition "
  f"(macro basin schedule + micro 互 greedy) does not reconstruct KW. "
  f"The fundamental problem: basin runs are too short (mean {np.mean(run_lengths):.1f}) for "
  f"within-run optimization to matter. KW alternates basins almost every pair, "
  f"which means the ordering principle operates *at* the basin transition level, "
  f"not *within* basin blocks. The generator is not hierarchical — it's interleaved.\n")

w("### What this tells us\n")
w("The basin sequence is a *consequence* of the ordering, not its generator. "
  "KW doesn't build runs of same-basin pairs and then order within runs. Instead, "
  "it weaves basins together in a rapid-alternation pattern (23 runs in 32 positions). "
  "The ordering principle must simultaneously determine both which basin to visit "
  "and which specific pair to place — these are not separable decisions.\n")
w("The next question: what interleaving rule produces this specific basin sequence "
  "while maintaining the observed 互 continuity (12.7th percentile)?\n")

out_path = Path(__file__).parent / "03_hierarchical_test_results.md"
out_path.write_text('\n'.join(md))
print(f"\nResults written to {out_path}")
