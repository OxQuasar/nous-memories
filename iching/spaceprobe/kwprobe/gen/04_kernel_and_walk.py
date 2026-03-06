"""
Kernel independence test + transition-walk reconstruction.

Part 1: Is H-kernel redundant with basin-crossing? (sage's independence test)
Part 2: Is the cost gradient (sub-optimal early, optimal late) artifactual?
Part 3: Score-based walk reconstruction with feature-weighted scoring.
Part 4: Divergence analysis of best reconstruction.
Part 5: Compression — how many orderings does the best rule admit?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
from itertools import product as iprod
from pathlib import Path
from math import log2
import random
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6, popcount,
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

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}
KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}

entry_basins = [get_basin(pairs[k][0]) for k in range(N_PAIRS)]
exit_basins = [get_basin(pairs[k][1]) for k in range(N_PAIRS)]

# Bridge 互 weight matrix
W = np.zeros((N_PAIRS, N_PAIRS), dtype=int)
for i in range(N_PAIRS):
    for j in range(N_PAIRS):
        W[i][j] = 99 if i == j else hamming6(pair_hu[i][1], pair_hu[j][0])

kw_total = sum(int(W[k][k+1]) for k in range(31))

# Precompute per-bridge features for score functions
def bridge_crosses_basin(k, j):
    return get_basin(pairs[k][1]) != get_basin(pairs[j][0])

def bridge_h_kernel(k, j):
    xor = pairs[k][1] ^ pairs[j][0]
    return mirror_kernel(xor) in H_KERNELS

def bridge_hex_dist(k, j):
    return hamming6(pairs[k][1], pairs[j][0])

def bridge_basin_same(k, j):
    return get_basin(pairs[k][1]) == get_basin(pairs[j][0])

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: KERNEL INDEPENDENCE FROM BASIN CROSSING
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("PART 1: KERNEL INDEPENDENCE FROM BASIN CROSSING")
print("=" * 70)

# Identify sub-optimal bridges (same definition as script 02)
sub_optimal = []
for k in range(31):
    kw_next = k + 1
    kw_d = int(W[k][kw_next])
    visited = set(range(k + 1))
    available = [j for j in range(N_PAIRS) if j not in visited]
    min_d = min(int(W[k][j]) for j in available)
    if kw_d > min_d + 1:
        alts = [j for j in available if int(W[k][j]) == min_d]
        sub_optimal.append((k, kw_next, kw_d, min_d, alts))

print(f"\n  Analyzing ALL available pairs at each of {len(sub_optimal)} sub-optimal bridges.")
print(f"  For each available pair: basin-crossing? H-kernel?")

# Global counters
total_crossers = 0
total_crossers_h = 0
total_same = 0
total_same_h = 0
per_bridge_data = []

for k, kw_next, kw_d, min_d, alts in sub_optimal:
    visited = set(range(k + 1))
    available = [j for j in range(N_PAIRS) if j not in visited]
    exit_b = get_basin(pairs[k][1])
    
    crossers = []
    same_basin = []
    for j in available:
        enter_b = get_basin(pairs[j][0])
        xor = pairs[k][1] ^ pairs[j][0]
        kernel = mirror_kernel(xor)
        is_h = kernel in H_KERNELS
        crosses = (exit_b != enter_b)
        
        if crosses:
            crossers.append((j, is_h))
        else:
            same_basin.append((j, is_h))
    
    n_cross = len(crossers)
    n_cross_h = sum(1 for _, h in crossers if h)
    n_same = len(same_basin)
    n_same_h = sum(1 for _, h in same_basin if h)
    
    total_crossers += n_cross
    total_crossers_h += n_cross_h
    total_same += n_same
    total_same_h += n_same_h
    
    # KW's choice properties
    kw_crosses = (exit_b != get_basin(pairs[kw_next][0]))
    kw_h = bridge_h_kernel(k, kw_next)
    
    per_bridge_data.append({
        'bridge': k, 'n_avail': len(available),
        'n_cross': n_cross, 'n_cross_h': n_cross_h,
        'n_same': n_same, 'n_same_h': n_same_h,
        'kw_crosses': kw_crosses, 'kw_h': kw_h,
    })
    
    cross_h_rate = n_cross_h / n_cross if n_cross > 0 else 0
    same_h_rate = n_same_h / n_same if n_same > 0 else 0
    print(f"  Bridge {k:2d}→{k+1:2d}: avail={len(available):2d}  "
          f"cross={n_cross:2d} (H:{n_cross_h:2d}, {100*cross_h_rate:4.0f}%)  "
          f"same={n_same:2d} (H:{n_same_h:2d}, {100*same_h_rate:4.0f}%)  "
          f"KW: {'cross' if kw_crosses else 'same':>5s} {'H' if kw_h else '¬H':>2s}")

overall_cross_h_rate = total_crossers_h / total_crossers if total_crossers > 0 else 0
overall_same_h_rate = total_same_h / total_same if total_same > 0 else 0
print(f"\n  Overall H-kernel rates:")
print(f"    Basin-crossing options: {total_crossers_h}/{total_crossers} = {100*overall_cross_h_rate:.1f}%")
print(f"    Same-basin options:     {total_same_h}/{total_same} = {100*overall_same_h_rate:.1f}%")

# Further test: among basin-crossing options, does KW further prefer H-kernel?
print(f"\n  Among basin-crossing options, does KW further prefer H-kernel?")
kw_chose_cross_and_h = 0
kw_chose_cross = 0
bridges_cross_multi = 0
h_further_disc = 0

for bd in per_bridge_data:
    if bd['kw_crosses']:
        kw_chose_cross += 1
        if bd['kw_h']:
            kw_chose_cross_and_h += 1
        # Does H-kernel discriminate among crossers?
        if bd['n_cross'] > 1 and bd['n_cross_h'] < bd['n_cross']:
            bridges_cross_multi += 1
            if bd['kw_h']:
                h_further_disc += 1

print(f"    KW chose basin-crossing: {kw_chose_cross}/{len(sub_optimal)}")
print(f"    Of those, KW is H-kernel: {kw_chose_cross_and_h}/{kw_chose_cross}")
print(f"    Bridges with multiple crossers, some non-H: {bridges_cross_multi}")
print(f"    Of those, KW chose H-kernel: {h_further_disc}/{bridges_cross_multi}")

if overall_cross_h_rate > 0.85:
    verdict = "REDUNDANT"
    print(f"\n  VERDICT: H-kernel is largely {verdict} with basin-crossing "
          f"({100*overall_cross_h_rate:.0f}% of crossers are H-kernel).")
else:
    verdict = "INDEPENDENT"
    print(f"\n  VERDICT: H-kernel is {verdict} from basin-crossing "
          f"({100*overall_cross_h_rate:.0f}% of crossers are H-kernel).")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: COST GRADIENT — STRUCTURAL OR ARTIFACTUAL?
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 2: COST GRADIENT — STRUCTURAL OR ARTIFACTUAL?")
print("=" * 70)

# KW's gradient
kw_dists = [int(W[k][k+1]) for k in range(31)]
kw_first = np.mean(kw_dists[:16])
kw_second = np.mean(kw_dists[16:])  # bridges 16-30 (15 bridges)
kw_gradient = kw_first - kw_second

print(f"\n  KW bridge distances: {kw_dists}")
print(f"  First half mean (bridges 0-15): {kw_first:.3f}")
print(f"  Second half mean (bridges 16-30): {kw_second:.3f}")
print(f"  Gradient (first - second): {kw_gradient:.3f}")

# Random baseline
N_RAND = 50_000
rand_gradients = np.zeros(N_RAND)
rand_first_halves = np.zeros(N_RAND)
rand_second_halves = np.zeros(N_RAND)
order = list(range(N_PAIRS))

for trial in range(N_RAND):
    random.shuffle(order)
    dists = [int(W[order[k]][order[k+1]]) for k in range(31)]
    first = np.mean(dists[:16])
    second = np.mean(dists[16:])
    rand_first_halves[trial] = first
    rand_second_halves[trial] = second
    rand_gradients[trial] = first - second

kw_grad_pctile = 100.0 * np.sum(rand_gradients <= kw_gradient) / N_RAND
mean_rand_grad = rand_gradients.mean()
std_rand_grad = rand_gradients.std()

print(f"\n  Random baseline ({N_RAND} shuffles):")
print(f"    Mean gradient: {mean_rand_grad:.3f} (std: {std_rand_grad:.3f})")
print(f"    Random first-half mean: {rand_first_halves.mean():.3f}")
print(f"    Random second-half mean: {rand_second_halves.mean():.3f}")
print(f"    KW gradient percentile: {kw_grad_pctile:.2f}%")

if abs(mean_rand_grad) > 0.05:
    print(f"\n  Random orderings DO show a systematic gradient of {mean_rand_grad:.3f}.")
    print(f"  This is a combinatorial depletion effect.")
else:
    print(f"\n  Random orderings show NO systematic gradient ({mean_rand_grad:.3f} ≈ 0).")

if kw_grad_pctile > 95:
    print(f"  KW's gradient ({kw_gradient:.2f}) is EXTREME (p={100-kw_grad_pctile:.2f}th percentile).")
    print(f"  The cost gradient is STRUCTURAL, not just depletion.")
elif kw_grad_pctile > 75:
    print(f"  KW's gradient ({kw_gradient:.2f}) is MODERATE (p={kw_grad_pctile:.1f}th percentile).")
elif kw_grad_pctile < 25:
    print(f"  KW's gradient ({kw_gradient:.2f}) is REVERSED relative to expectation.")
else:
    print(f"  KW's gradient ({kw_gradient:.2f}) is UNREMARKABLE.")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: TRANSITION-WALK RECONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 3: TRANSITION-WALK RECONSTRUCTION")
print("=" * 70)

def scored_walk(score_fn, force_last=None):
    """
    Walk starting from pair 0, at each step picking the highest-scoring
    available next pair. Ties broken by KW pair index (lowest first).
    
    force_last: if set, reserve this pair for the last position.
    """
    path = [0]
    used = {0}
    reserved = {force_last} if force_last is not None else set()
    
    for step in range(N_PAIRS - 1):
        cur = path[-1]
        
        if step == N_PAIRS - 2 and force_last is not None:
            path.append(force_last)
            used.add(force_last)
            continue
        
        cands = [j for j in range(N_PAIRS) if j not in used and j not in reserved]
        if not cands:
            if force_last is not None and force_last not in used:
                path.append(force_last)
                used.add(force_last)
            break
        
        scores = [(score_fn(cur, j), j) for j in cands]
        max_score = max(s for s, _ in scores)
        best = sorted([j for s, j in scores if s == max_score])
        
        path.append(best[0])
        used.add(best[0])
    
    return path

def count_matches(path):
    kw_trans = set((k, k+1) for k in range(31))
    path_trans = set((path[k], path[k+1]) for k in range(len(path)-1))
    return len(kw_trans & path_trans)

def pos_matches(path):
    return sum(1 for k in range(N_PAIRS) if path[k] == k)

def path_weight(path):
    return sum(int(W[path[k]][path[k+1]]) for k in range(len(path)-1))

# Score A: 互 only
def score_a(k, j):
    return -int(W[k][j])

# Score B: 互 + basin-crossing bonus
def make_score_b(alpha):
    def score(k, j):
        return -int(W[k][j]) + alpha * int(bridge_crosses_basin(k, j))
    return score

# Score C: 互 + basin-crossing + H-kernel
def make_score_c(alpha, beta):
    def score(k, j):
        return -int(W[k][j]) + alpha * int(bridge_crosses_basin(k, j)) + beta * int(bridge_h_kernel(k, j))
    return score

# Score D: 互 + hex distance bonus
def make_score_d(gamma):
    def score(k, j):
        return -int(W[k][j]) + gamma * bridge_hex_dist(k, j)
    return score

# Score E: 互 - same-basin penalty
def make_score_e(delta):
    def score(k, j):
        return -int(W[k][j]) - delta * int(bridge_basin_same(k, j))
    return score

# Score F: combined
def make_score_f(alpha, gamma, beta):
    def score(k, j):
        return (-int(W[k][j])
                + alpha * int(bridge_crosses_basin(k, j))
                + gamma * bridge_hex_dist(k, j)
                + beta * int(bridge_h_kernel(k, j)))
    return score

results = []

# Score A
path = scored_walk(score_a)
results.append(('A: 互 only', {}, path, count_matches(path), pos_matches(path), path_weight(path)))
print(f"\n  Score A (互 only): matches={results[-1][3]}/31, pos={results[-1][4]}/32, weight={results[-1][5]}")

# Score B: test α values
print(f"\n  Score B (互 + α·basin_cross):")
best_b = None
for alpha in [1, 2, 3, 5, 8, 13]:
    path = scored_walk(make_score_b(alpha))
    m = count_matches(path)
    p = pos_matches(path)
    w = path_weight(path)
    results.append((f'B: α={alpha}', {'α': alpha}, path, m, p, w))
    if best_b is None or m > best_b[3]:
        best_b = results[-1]
    print(f"    α={alpha:2d}: matches={m:2d}/31, pos={p:2d}/32, weight={w}")

# Score D: test γ values
print(f"\n  Score D (互 + γ·hex_dist):")
best_d = None
for gamma in [0.5, 1, 2, 3, 5]:
    path = scored_walk(make_score_d(gamma))
    m = count_matches(path)
    p = pos_matches(path)
    w = path_weight(path)
    results.append((f'D: γ={gamma}', {'γ': gamma}, path, m, p, w))
    if best_d is None or m > best_d[3]:
        best_d = results[-1]
    print(f"    γ={gamma}: matches={m:2d}/31, pos={p:2d}/32, weight={w}")

# Score E: test δ values
print(f"\n  Score E (互 - δ·basin_same):")
best_e = None
for delta in [1, 2, 3, 5, 8, 13]:
    path = scored_walk(make_score_e(delta))
    m = count_matches(path)
    p = pos_matches(path)
    w = path_weight(path)
    results.append((f'E: δ={delta}', {'δ': delta}, path, m, p, w))
    if best_e is None or m > best_e[3]:
        best_e = results[-1]
    print(f"    δ={delta:2d}: matches={m:2d}/31, pos={p:2d}/32, weight={w}")

# Score C: best α from B + β search
best_b_alpha = best_b[1]['α']
print(f"\n  Score C (互 + {best_b_alpha}·basin_cross + β·h_kernel):")
best_c = None
for beta in [1, 2, 3, 5, 8]:
    path = scored_walk(make_score_c(best_b_alpha, beta))
    m = count_matches(path)
    p = pos_matches(path)
    w = path_weight(path)
    results.append((f'C: α={best_b_alpha},β={beta}', {'α': best_b_alpha, 'β': beta}, path, m, p, w))
    if best_c is None or m > best_c[3]:
        best_c = results[-1]
    print(f"    β={beta:2d}: matches={m:2d}/31, pos={p:2d}/32, weight={w}")

# Score F: coarse grid search
print(f"\n  Score F (combined): grid search over (α, γ, β) ∈ {{0,1,2,4,8}}")
grid_vals = [0, 1, 2, 4, 8]
best_f = None
best_f_matches = -1
f_results = []

for alpha in grid_vals:
    for gamma in grid_vals:
        for beta in grid_vals:
            if alpha == 0 and gamma == 0 and beta == 0:
                continue  # skip pure 互 (already tested)
            path = scored_walk(make_score_f(alpha, gamma, beta))
            m = count_matches(path)
            p = pos_matches(path)
            w = path_weight(path)
            f_results.append((alpha, gamma, beta, m, p, w, path))
            if m > best_f_matches:
                best_f_matches = m
                best_f = (alpha, gamma, beta, m, p, w, path)

# Top 10 from grid
f_results.sort(key=lambda x: (-x[3], -x[4], x[5]))
print(f"  Top 15 configurations:")
print(f"  {'α':>3s}  {'γ':>3s}  {'β':>3s}  {'Match':>5s}  {'Pos':>3s}  {'Weight':>6s}")
for alpha, gamma, beta, m, p, w, _ in f_results[:15]:
    print(f"  {alpha:3d}  {gamma:3d}  {beta:3d}  {m:3d}/31  {p:3d}  {w:6d}")

print(f"\n  Best F: α={best_f[0]}, γ={best_f[1]}, β={best_f[2]} → "
      f"matches={best_f[3]}/31, pos={best_f[4]}/32, weight={best_f[5]}")

# Now add best_f to results
results.append((f'F: α={best_f[0]},γ={best_f[1]},β={best_f[2]}',
                {'α': best_f[0], 'γ': best_f[1], 'β': best_f[2]},
                best_f[6], best_f[3], best_f[4], best_f[5]))

# Also test with force_last=31
print(f"\n  Testing best configs with force_last=31 (Ji Ji/Wei Ji):")
for name, params, _, m_base, _, _ in results:
    if m_base >= best_f[3] - 2:  # only test near-best
        if 'α' in params and 'γ' in params and 'β' in params:
            fn = make_score_f(params['α'], params['γ'], params['β'])
        elif 'α' in params and 'β' in params:
            fn = make_score_c(params['α'], params['β'])
        elif 'α' in params:
            fn = make_score_b(params['α'])
        elif 'γ' in params:
            fn = make_score_d(params['γ'])
        elif 'δ' in params:
            fn = make_score_e(params['δ'])
        else:
            fn = score_a
        path_f = scored_walk(fn, force_last=31)
        m_f = count_matches(path_f)
        p_f = pos_matches(path_f)
        w_f = path_weight(path_f)
        print(f"    {name}: {m_base}/31 → {m_f}/31 (forced), weight {w_f}")
        if m_f > best_f[3]:
            best_f = (params.get('α', 0), params.get('γ', 0), params.get('β', 0),
                      m_f, p_f, w_f, path_f)
            results.append((name + ' +force31', params, path_f, m_f, p_f, w_f))

# Final summary table
results.sort(key=lambda x: (-x[3], -x[4], x[5]))
print(f"\n  === RECONSTRUCTION SUMMARY (top 20) ===")
print(f"  {'Method':>45s}  {'Match':>5s}  {'Pos':>3s}  {'Weight':>6s}")
for name, _, _, m, p, w in results[:20]:
    print(f"  {name:>45s}  {m:3d}/31  {p:3d}  {w:6d}")

# Identify overall best
best_result = results[0]
print(f"\n  Overall best: {best_result[0]} → {best_result[3]}/31 matches")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: BEST RECONSTRUCTION — DIVERGENCE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 4: DIVERGENCE ANALYSIS OF BEST RECONSTRUCTION")
print("=" * 70)

best_path = best_result[2]
best_name = best_result[0]

print(f"\n  Best method: {best_name}")
print(f"  Path: {best_path}")

divergences = []
for pos in range(N_PAIRS):
    if best_path[pos] != pos:
        divergences.append(pos)

print(f"\n  Divergence positions ({len(divergences)}/{N_PAIRS}):")
print(f"  {'Pos':>3s}  {'KW':>20s}  {'Recon':>20s}  {'Basin KW':>8s}  {'Basin R':>8s}")
for pos in divergences:
    kw_p = pos
    r_p = best_path[pos]
    print(f"  {pos:3d}  {pair_names[kw_p][0]+'/'+pair_names[kw_p][1]:>20s}  "
          f"{pair_names[r_p][0]+'/'+pair_names[r_p][1]:>20s}  "
          f"{SYM[entry_basins[kw_p]]:>8s}  {SYM[entry_basins[r_p]]:>8s}")

# Concentration analysis
if divergences:
    first_half = sum(1 for d in divergences if d < 16)
    second_half = sum(1 for d in divergences if d >= 16)
    print(f"\n  Divergences: first half={first_half}, second half={second_half}")

# Transition-level divergences
print(f"\n  Transition divergences:")
print(f"  {'Bridge':>7s}  {'KW→':>20s}  {'Recon→':>20s}  {'KW d':>4s}  {'R d':>4s}  "
      f"{'KW cross':>8s}  {'R cross':>8s}")
for k in range(31):
    r_cur = best_path[k]
    r_next = best_path[k + 1]
    if (r_cur, r_next) != (k, k + 1):
        kw_d = int(W[k][k+1])
        r_d = int(W[r_cur][r_next])
        kw_cross = "cross" if exit_basins[k] != entry_basins[k+1] else "same"
        r_cross = "cross" if exit_basins[r_cur] != entry_basins[r_next] else "same"
        print(f"  {k:2d}→{k+1:2d}  "
              f"{pair_names[k+1][0]+'/'+pair_names[k+1][1]:>20s}  "
              f"{pair_names[r_next][0]+'/'+pair_names[r_next][1]:>20s}  "
              f"{kw_d:4d}  {r_d:4d}  {kw_cross:>8s}  {r_cross:>8s}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: COMPRESSION — HOW MANY ORDERINGS DOES THE BEST RULE ADMIT?
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 5: COMPRESSION FROM BEST SCORING RULE")
print("=" * 70)

# Reconstruct the score function for the best result
bp = best_result[1]
alpha_b = bp.get('α', 0)
gamma_b = bp.get('γ', 0)
beta_b = bp.get('β', 0)
delta_b = bp.get('δ', 0)

# Use Score F if all three present, else reconstruct
if 'δ' in bp:
    best_fn = make_score_e(delta_b)
elif 'γ' in bp and 'α' in bp:
    best_fn = make_score_f(alpha_b, gamma_b, beta_b)
elif 'α' in bp and 'β' in bp:
    best_fn = make_score_c(alpha_b, beta_b)
elif 'α' in bp:
    best_fn = make_score_b(alpha_b)
elif 'γ' in bp:
    best_fn = make_score_d(gamma_b)
else:
    best_fn = score_a

# At each step, count tied candidates
log2_orderings = 0.0
ties_per_step = []
used = {0}
path = [0]

for step in range(N_PAIRS - 1):
    cur = path[-1]
    cands = [j for j in range(N_PAIRS) if j not in used]
    if not cands:
        break
    
    scores = [(best_fn(cur, j), j) for j in cands]
    max_score = max(s for s, _ in scores)
    tied = [j for s, j in scores if s == max_score]
    
    n_tied = len(tied)
    ties_per_step.append(n_tied)
    log2_orderings += log2(n_tied) if n_tied > 1 else 0
    
    # Follow the actual path (pick lowest KW index among ties)
    chosen = min(tied)
    path.append(chosen)
    used.add(chosen)

log2_full = log2(1)
for i in range(1, N_PAIRS + 1):
    log2_full += log2(i)  # log2(32!)

print(f"\n  Ties at each step: {ties_per_step}")
print(f"  Steps with ties (>1 candidate): {sum(1 for t in ties_per_step if t > 1)}/{len(ties_per_step)}")
print(f"  Max tie size: {max(ties_per_step)}")
print(f"\n  Compression:")
print(f"    log₂(orderings from scoring rule): {log2_orderings:.1f}")
print(f"    log₂(basin-consistent orderings):  75.0")
print(f"    log₂(32!):                         {log2_full:.1f}")
print(f"    Bits eliminated by scoring rule:    {log2_full - log2_orderings:.1f}")

if log2_orderings < 5:
    print(f"  The scoring rule is highly deterministic — only ~{2**log2_orderings:.0f} orderings.")
elif log2_orderings < 30:
    print(f"  The scoring rule narrows the space to ~2^{log2_orderings:.0f} orderings.")
else:
    print(f"  The scoring rule still admits a vast space of ~2^{log2_orderings:.0f} orderings.")

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE RESULTS TO MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("WRITING RESULTS")
print("=" * 70)

md = []
w = md.append

w("# Kernel Independence + Transition-Walk Reconstruction\n")

# Part 1
w("## Part 1: Kernel Independence from Basin Crossing\n")
w("**Question:** When KW chooses a basin-crossing pair at sub-optimal bridges, "
  "does H-kernel come 'for free' (redundant), or does it carry independent information?\n")

w("### H-kernel rate by crossing type\n")
w("| Category | Count | H-kernel | Rate |")
w("|----------|-------|----------|------|")
w(f"| Basin-crossing options | {total_crossers} | {total_crossers_h} | {100*overall_cross_h_rate:.1f}% |")
w(f"| Same-basin options | {total_same} | {total_same_h} | {100*overall_same_h_rate:.1f}% |")
w("")

w("### Per-bridge detail\n")
w("| Bridge | Avail | Cross (H%) | Same (H%) | KW chose |")
w("|--------|-------|-----------|----------|----------|")
for bd in per_bridge_data:
    cr = f"{bd['n_cross']} ({100*bd['n_cross_h']/bd['n_cross']:.0f}%)" if bd['n_cross'] > 0 else "0"
    sm = f"{bd['n_same']} ({100*bd['n_same_h']/bd['n_same']:.0f}%)" if bd['n_same'] > 0 else "0"
    kw_str = f"{'cross' if bd['kw_crosses'] else 'same'} {'H' if bd['kw_h'] else '¬H'}"
    w(f"| {bd['bridge']}→{bd['bridge']+1} | {bd['n_avail']} | {cr} | {sm} | {kw_str} |")
w("")

w(f"### Verdict: **{verdict}**\n")
if verdict == "REDUNDANT":
    w(f"H-kernel rate among basin-crossers is {100*overall_cross_h_rate:.0f}% — "
      f"choosing to cross basins almost automatically gives H-kernel. "
      f"The h_kernel signal in Round 2 is largely a side effect of basin-crossing.\n")
else:
    w(f"H-kernel rate among basin-crossers is only {100*overall_cross_h_rate:.0f}% "
      f"(vs {100*overall_same_h_rate:.0f}% for same-basin). "
      f"Crossing basins does NOT automatically give H-kernel. "
      f"KW's preference for H-kernel carries information beyond basin-crossing.")
    if h_further_disc > 0:
        w(f" Among {bridges_cross_multi} bridges with multiple basin-crossing options, "
          f"KW chose the H-kernel one in {h_further_disc} cases.")
    w("")

# Part 2
w("## Part 2: Cost Gradient — Structural or Artifactual?\n")
w(f"| Metric | KW | Random mean | Random std |")
w(f"|--------|-----|-----------|-----------|")
w(f"| First-half mean (bridges 0-15) | {kw_first:.2f} | {rand_first_halves.mean():.2f} | {rand_first_halves.std():.2f} |")
w(f"| Second-half mean (bridges 16-30) | {kw_second:.2f} | {rand_second_halves.mean():.2f} | {rand_second_halves.std():.2f} |")
w(f"| Gradient (first − second) | {kw_gradient:.2f} | {mean_rand_grad:.2f} | {std_rand_grad:.2f} |")
w(f"| KW gradient percentile | {kw_grad_pctile:.1f}% | — | — |")
w("")

if abs(mean_rand_grad) > 0.05:
    w(f"Random orderings show a systematic gradient of {mean_rand_grad:.2f} (depletion effect). ")
else:
    w(f"Random orderings show no systematic gradient ({mean_rand_grad:.2f} ≈ 0). ")

if kw_grad_pctile > 90:
    w(f"KW's gradient of {kw_gradient:.2f} is at the {kw_grad_pctile:.1f}th percentile — "
      f"**significantly steeper than depletion alone**. The front-loading of 互 cost is structural.\n")
elif kw_grad_pctile > 75:
    w(f"KW's gradient of {kw_gradient:.2f} is at the {kw_grad_pctile:.1f}th percentile — "
      f"**moderately above random**. Partially structural, partially depletion.\n")
else:
    w(f"KW's gradient of {kw_gradient:.2f} is at the {kw_grad_pctile:.1f}th percentile — "
      f"**within normal range** for random orderings. The apparent cost gradient is "
      f"largely a depletion artifact.\n")

w("**Important distinction:** Round 1 found 'sub-optimal early, optimal late' — meaning "
  "early bridges have more *locally sub-optimal* choices (choosing d=3 when d=0 exists). "
  "But the *absolute* d_互 values are actually lower in the first half (2.56 vs 2.93). "
  "These are compatible: early bridges pick 'bad' options from a richer pool (many d=0 "
  "alternatives exist but are skipped), while late bridges pick 'good' options from a "
  "depleted pool (fewer alternatives, so KW's choice is closer to the minimum).\n")

# Part 3
w("## Part 3: Transition-Walk Reconstruction\n")
w("Score-based greedy walk from pair 0, choosing highest-scoring available pair.\n")

w("### Results summary\n")
w("| Method | Transitions matched | Positions matched | Total 互 weight |")
w("|--------|-------------------|------------------|----------------|")
for name, _, _, m, p, wt in results[:20]:
    w(f"| {name} | {m}/31 | {p}/32 | {wt} |")
w(f"| KW actual | 31/31 | 32/32 | {kw_total} |")
w("")

# Grid search top configs
w("### Score F grid search (top 15)\n")
w("| α | γ | β | Matches | Positions | Weight |")
w("|---|---|---|---------|-----------|--------|")
for alpha, gamma, beta, m, p, wt, _ in f_results[:15]:
    w(f"| {alpha} | {gamma} | {beta} | {m}/31 | {p}/32 | {wt} |")
w("")

w(f"**Best reconstruction: {best_result[0]}** — {best_result[3]}/31 transitions, "
  f"{best_result[4]}/32 positions, weight {best_result[5]}.\n")

# Part 4
w("## Part 4: Divergence Analysis\n")
if divergences:
    first_half_d = sum(1 for d in divergences if d < 16)
    second_half_d = sum(1 for d in divergences if d >= 16)
    w(f"{len(divergences)} positions diverge (first half: {first_half_d}, second half: {second_half_d}).\n")
    
    w("| Position | KW pair | Recon pair | KW basin | Recon basin |")
    w("|----------|---------|------------|----------|-------------|")
    for pos in divergences:
        kw_p = pos
        r_p = best_path[pos]
        w(f"| {pos} | {pair_names[kw_p][0]}/{pair_names[kw_p][1]} "
          f"| {pair_names[r_p][0]}/{pair_names[r_p][1]} "
          f"| {SYM[entry_basins[kw_p]]} | {SYM[entry_basins[r_p]]} |")
    w("")
else:
    w("**No divergences — perfect reconstruction!**\n")

# Part 5
w("## Part 5: Compression\n")
w(f"| Metric | Value |")
w(f"|--------|-------|")
w(f"| log₂(orderings from scoring rule) | {log2_orderings:.1f} |")
w(f"| log₂(basin-consistent orderings) | 75.0 |")
w(f"| log₂(32!) | {log2_full:.1f} |")
w(f"| Bits eliminated | {log2_full - log2_orderings:.1f} / {log2_full:.1f} |")
w("")
w(f"Steps with ties: {sum(1 for t in ties_per_step if t > 1)}/31. "
  f"Max tie size: {max(ties_per_step)}. "
  f"The scoring rule reduces 32! to ~2^{log2_orderings:.0f} orderings.\n")

# Summary
w("## Key Findings\n")

w(f"1. **H-kernel is {verdict.lower()} from basin-crossing.** "
  f"H-kernel rate among basin-crossers: {100*overall_cross_h_rate:.0f}%, "
  f"among same-basin: {100*overall_same_h_rate:.0f}%. ")
if verdict == "REDUNDANT":
    w("Crossing basins automatically confers H-kernel — the two signals are not separable.\n")
else:
    w("Basin-crossing and H-kernel carry partially independent information.\n")

w(f"2. **Cost gradient:** KW's first-vs-second-half gradient is at "
  f"the {kw_grad_pctile:.0f}th percentile vs random. ")
if kw_grad_pctile > 80:
    w("The front-loading of 互 cost is at least partially structural.\n")
else:
    w("The apparent gradient is within normal depletion range.\n")

w(f"3. **Best reconstruction: {best_result[0]}** achieves {best_result[3]}/31 transitions "
  f"(vs 3/31 互-only, 5/31 basin-constrained). ")
if best_result[3] >= 15:
    w(f"This is a substantial improvement — the scoring function captures much of "
      f"KW's structure. The remaining {31 - best_result[3]} divergences mark "
      f"genuine exceptions to the rule.\n")
elif best_result[3] >= 8:
    w(f"This is a meaningful improvement over baselines, but far from full reconstruction. "
      f"The scoring function captures some of KW's logic but misses key constraints.\n")
else:
    w(f"The improvement is modest. No simple linear scoring of these features reconstructs KW.\n")

w(f"4. **Compression:** The best scoring rule reduces the search space to "
  f"2^{log2_orderings:.0f} orderings (from 2^{log2_full:.0f}), eliminating "
  f"{log2_full - log2_orderings:.0f} bits. ")
if log2_orderings < 10:
    w(f"This is very high compression — the rule is nearly deterministic.\n")
else:
    w(f"Substantial ambiguity remains at {sum(1 for t in ties_per_step if t > 1)} "
      f"tie-breaking steps.\n")

w("### Reconstruction progression\n")
w("| Round | Method | Matches |")
w("|-------|--------|---------|")
w("| 1 | Greedy 互 only | 3/31 |")
w("| 3 | Basin-constrained greedy | 5/31 |")
w(f"| 4 | {best_result[0]} | {best_result[3]}/31 |")
w(f"| — | KW actual | 31/31 |")
w("")

out_path = Path(__file__).parent / "04_kernel_and_walk_results.md"
out_path.write_text('\n'.join(md))
print(f"\nResults written to {out_path}")
