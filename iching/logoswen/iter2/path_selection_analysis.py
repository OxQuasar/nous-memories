"""
Path Selection Analysis: How special is KW's orbit-change weight distribution?

The S-bound theorem (max_S = 3 - w(orbit_change)) shows bridges with 
w(orbit_change) >= 2 are S=2-immune. KW has 20/31 such bridges.

This script:
1. Samples 50K+ Eulerian paths through the orbit multigraph
2. For each path, computes the orbit-change weight profile
3. Determines KW's percentile for S=2-immune bridge count
4. Finds the minimum achievable S=2-susceptible bridge count
5. Checks Qian→Tai endpoint correlation
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import all_bits
import random
import time
import math

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

# ─── Build the orbit multigraph (from KW bridges) ────────────────────────────

edge_count = Counter()
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    edge_count[(xor_sig(a), xor_sig(b))] += 1

# KW orbit walk for comparison
kw_orbit_walk = [xor_sig(tuple(M[2*k])) for k in range(32)]

# KW orbit-change weights
kw_bridge_weights = []
for k in range(31):
    sig_a = kw_orbit_walk[k]
    sig_b = kw_orbit_walk[k+1]
    w = sum(sig_a[i] ^ sig_b[i] for i in range(3))
    kw_bridge_weights.append(w)

kw_w_profile = Counter(kw_bridge_weights)
kw_immune = sum(1 for w in kw_bridge_weights if w >= 2)
kw_susceptible = 31 - kw_immune

print("=" * 80)
print("KW ORBIT-CHANGE WEIGHT PROFILE")
print("=" * 80)
print(f"  Weight distribution: {dict(sorted(kw_w_profile.items()))}")
print(f"  S=2-immune (w>=2): {kw_immune}/31")
print(f"  S=2-susceptible (w<2): {kw_susceptible}/31")
print(f"    w=0 (self-loops): {kw_w_profile[0]}")
print(f"    w=1 (single-comp): {kw_w_profile[1]}")
print()

# Also compute the orbit-change weight for each edge type
print("Edge types and their orbit-change weights:")
for (u, v), cnt in sorted(edge_count.items()):
    w = sum(u[i] ^ v[i] for i in range(3))
    print(f"  {ORBIT_NAMES[u]:>6s} → {ORBIT_NAMES[v]:<6s}: mult={cnt}, w(change)={w}, "
          f"{'S=2-immune' if w >= 2 else 'S=2-SUSCEPTIBLE'}")
print()


# ─── Sampling Eulerian paths ─────────────────────────────────────────────────

def sample_eulerian_path(edge_count, start, end, rng):
    """Sample a random Eulerian path using randomized DFS with backtracking."""
    remaining = dict(edge_count)
    total = sum(edge_count.values())
    
    adj = defaultdict(list)
    for (u, v) in edge_count:
        adj[u].append(v)
    
    path = [start]
    
    def dfs(node, depth):
        if depth == total:
            return node == end
        
        available = []
        for target in adj[node]:
            edge = (node, target)
            if remaining.get(edge, 0) > 0:
                available.append(target)
        
        rng.shuffle(available)
        
        for target in available:
            edge = (node, target)
            remaining[edge] -= 1
            path.append(target)
            if dfs(target, depth + 1):
                return True
            path.pop()
            remaining[edge] += 1
        
        return False
    
    if dfs(start, 0):
        return list(path)
    return None


def compute_path_profile(path):
    """Compute orbit-change weight profile for an Eulerian path (32 nodes, 31 edges)."""
    weights = []
    for k in range(len(path) - 1):
        u, v = path[k], path[k+1]
        w = sum(u[i] ^ v[i] for i in range(3))
        weights.append(w)
    return weights


# ─── Main sampling loop ──────────────────────────────────────────────────────

N_SAMPLES = 50000
rng = random.Random(42)

print("=" * 80)
print(f"SAMPLING {N_SAMPLES} EULERIAN PATHS")
print("=" * 80)

immune_counts = []           # number of S=2-immune bridges per path
susceptible_counts = []      # number of S=2-susceptible bridges
w_profiles = []              # (w0, w1, w2, w3) counts per path
selfloop_counts = []         # w=0 count per path
w1_counts = []               # w=1 count per path
paths_found = 0

# Also track: paths that end at Tai
qian_tai_immune = []         # immune count for Qian→Tai paths

# Track full profiles for detailed analysis
profile_counter = Counter()  # (w0, w1, w2, w3) -> count

t0 = time.time()

for i in range(N_SAMPLES):
    path = sample_eulerian_path(edge_count, (0,0,0), (1,1,1), rng)
    if path is None:
        continue
    
    paths_found += 1
    weights = compute_path_profile(path)
    
    w_counts = Counter(weights)
    w0 = w_counts.get(0, 0)
    w1 = w_counts.get(1, 0)
    w2 = w_counts.get(2, 0)
    w3 = w_counts.get(3, 0)
    
    immune = w2 + w3
    susc = w0 + w1
    
    immune_counts.append(immune)
    susceptible_counts.append(susc)
    selfloop_counts.append(w0)
    w1_counts.append(w1)
    w_profiles.append((w0, w1, w2, w3))
    profile_counter[(w0, w1, w2, w3)] += 1
    
    if (i + 1) % 10000 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{N_SAMPLES} attempts, {paths_found} valid paths ({elapsed:.1f}s)")

t1 = time.time()
print(f"\nCompleted: {paths_found} valid paths from {N_SAMPLES} attempts in {t1-t0:.1f}s")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 1: S=2-immune bridge count distribution
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("1. S=2-IMMUNE BRIDGE COUNT DISTRIBUTION")
print("=" * 80)

immune_counter = Counter(immune_counts)
print(f"\n  Distribution of S=2-immune bridges (w>=2) across {paths_found} paths:")
print(f"  {'Count':>5s}  {'N_paths':>8s}  {'%':>6s}  {'Cumul%':>7s}")
cumul = 0
for count in sorted(immune_counter.keys()):
    n = immune_counter[count]
    pct = 100 * n / paths_found
    cumul += pct
    marker = " ← KW" if count == kw_immune else ""
    print(f"    {count:3d}    {n:6d}   {pct:5.1f}%   {cumul:5.1f}%{marker}")

mean_immune = sum(immune_counts) / len(immune_counts)
std_immune = (sum((x - mean_immune)**2 for x in immune_counts) / len(immune_counts)) ** 0.5

kw_pctile = 100 * sum(1 for x in immune_counts if x <= kw_immune) / len(immune_counts)
kw_above_pctile = 100 * sum(1 for x in immune_counts if x >= kw_immune) / len(immune_counts)

print(f"\n  Mean: {mean_immune:.2f}")
print(f"  Std:  {std_immune:.2f}")
print(f"  Min:  {min(immune_counts)}")
print(f"  Max:  {max(immune_counts)}")
print(f"\n  KW has {kw_immune} immune bridges")
print(f"  KW percentile: {kw_pctile:.1f}% (≤ KW)")
print(f"  Paths with ≥ {kw_immune}: {kw_above_pctile:.1f}%")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 2: S=2-susceptible bridge count (w=0 + w=1)
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("2. S=2-SUSCEPTIBLE BRIDGE COUNT DISTRIBUTION")
print("=" * 80)

susc_counter = Counter(susceptible_counts)
print(f"\n  Distribution of S=2-susceptible bridges (w<2):")
for count in sorted(susc_counter.keys()):
    n = susc_counter[count]
    pct = 100 * n / paths_found
    marker = " ← KW" if count == kw_susceptible else ""
    print(f"    {count:3d}    {n:6d}   {pct:5.1f}%{marker}")

print(f"\n  Minimum susceptible bridges: {min(susceptible_counts)}")
print(f"  Maximum susceptible bridges: {max(susceptible_counts)}")
print(f"  KW has {kw_susceptible} susceptible bridges")
print()

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 3: Self-loop count (w=0) distribution
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("3. SELF-LOOP COUNT (w=0) DISTRIBUTION")
print("=" * 80)

sl_counter = Counter(selfloop_counts)
print(f"\n  Distribution:")
for count in sorted(sl_counter.keys()):
    n = sl_counter[count]
    pct = 100 * n / paths_found
    marker = " ← KW" if count == kw_w_profile[0] else ""
    print(f"    w=0 count {count}: {n:6d}  ({pct:5.1f}%){marker}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 4: w=1 count distribution  
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("4. WEIGHT-1 BRIDGE COUNT (w=1) DISTRIBUTION")
print("=" * 80)

w1_counter = Counter(w1_counts)
print(f"\n  Distribution:")
for count in sorted(w1_counter.keys()):
    n = w1_counter[count]
    pct = 100 * n / paths_found
    marker = " ← KW" if count == kw_w_profile[1] else ""
    print(f"    w=1 count {count}: {n:6d}  ({pct:5.1f}%){marker}")

print()

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 5: Full weight profiles
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("5. FULL WEIGHT PROFILES (w0, w1, w2, w3)")
print("=" * 80)

kw_profile_tuple = tuple(kw_w_profile.get(w, 0) for w in range(4))
print(f"\n  KW profile: {kw_profile_tuple}")
print(f"\n  Top 20 most common profiles:")
for (w0, w1, w2, w3), cnt in profile_counter.most_common(20):
    pct = 100 * cnt / paths_found
    marker = " ← KW" if (w0, w1, w2, w3) == kw_profile_tuple else ""
    immune = w2 + w3
    print(f"    ({w0},{w1},{w2},{w3}): {cnt:5d} ({pct:5.2f}%)  immune={immune}{marker}")

kw_profile_cnt = profile_counter.get(kw_profile_tuple, 0)
kw_profile_pct = 100 * kw_profile_cnt / paths_found if paths_found > 0 else 0
print(f"\n  KW profile frequency: {kw_profile_cnt}/{paths_found} = {kw_profile_pct:.3f}%")
print(f"  Total distinct profiles: {len(profile_counter)}")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 6: Theoretical edge-weight structure
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("6. EDGE WEIGHT STRUCTURE — WHY IS THE PROFILE CONSTRAINED?")
print("=" * 80)

# The orbit multigraph has fixed edge multiplicities.
# Each edge has a fixed w(orbit_change).
# The weight profile of a path is determined by which edges it uses.
# But ALL Eulerian paths use ALL edges — they just differ in ORDER.
# So the MULTISET of orbit-change weights is IDENTICAL for all paths!

# Wait — is that true? An Eulerian path visits all edges exactly once.
# But our multigraph has edges with multiplicity > 1.
# Different Eulerian paths use the same multiset of edge types.
# The w-profile counts: for each w, how many edges have that w.
# Since all paths use the same multiset of edges, the w-profile is FIXED.

# Let me verify this:
edge_w_profile = Counter()
for (u, v), cnt in edge_count.items():
    w = sum(u[i] ^ v[i] for i in range(3))
    edge_w_profile[w] += cnt

print(f"\n  Edge weight profile (sum of multiplicities per weight):")
for w in sorted(edge_w_profile.keys()):
    print(f"    w={w}: {edge_w_profile[w]} edges")

print(f"\n  Total: {sum(edge_w_profile.values())} edges")
print(f"\n  THEOREM: Since ALL Eulerian paths use ALL edges exactly once,")
print(f"  the orbit-change weight profile is IDENTICAL for every Eulerian path.")
print(f"  It is: w=0:{edge_w_profile[0]}, w=1:{edge_w_profile[1]}, "
      f"w=2:{edge_w_profile[2]}, w=3:{edge_w_profile[3]}")

# Check if this matches KW
kw_total = dict(sorted(kw_w_profile.items()))
edge_total = dict(sorted(edge_w_profile.items()))
print(f"\n  KW profile: {kw_total}")
print(f"  Edge profile: {edge_total}")
match = all(kw_w_profile.get(w, 0) == edge_w_profile.get(w, 0) for w in range(4))
print(f"  Match: {'✓ YES — KW profile = unique possible profile' if match else '✗ NO'}")

# Verify from sampling
if len(profile_counter) == 1:
    print(f"\n  CONFIRMED by sampling: only 1 distinct profile seen across {paths_found} paths!")
elif len(profile_counter) <= 3:
    print(f"\n  NOTE: {len(profile_counter)} profiles seen — checking if they differ...")
    for prof, cnt in profile_counter.most_common():
        print(f"    {prof}: {cnt}")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 7: If profile is fixed, what DOES vary? — the ORDERING of weights
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("7. WHAT VARIES: THE SEQUENCE OF ORBIT-CHANGE WEIGHTS")
print("=" * 80)

# The multiset is fixed but the ORDER varies.
# KW's S=2 avoidance depends on which hexagrams appear at the 11 susceptible bridges.
# The POSITIONS of susceptible bridges in the sequence matter for:
# - Clustering effects (consecutive susceptible bridges share hexagram constraints)
# - Self-loop placement (w=0 bridges have 37.5% S=2 rate vs 25% for w=1)

# Compute the positions of susceptible bridges in KW
print(f"\n  KW susceptible bridge positions:")
for k, w in enumerate(kw_bridge_weights):
    if w < 2:
        sig_a = kw_orbit_walk[k]
        sig_b = kw_orbit_walk[k+1]
        s2_rate = 24/64 if w == 0 else 16/64  # from deep analysis
        print(f"    B{k:2d}: {ORBIT_NAMES[sig_a]:>6s}→{ORBIT_NAMES[sig_b]:<6s}  "
              f"w={w}  P(S=2)={s2_rate:.1%}")

print(f"\n  Under independence (ignoring hex correlations):")
# If each susceptible bridge independently avoids S=2, the probability of all avoiding is:
p_all_avoid = 1.0
for w in kw_bridge_weights:
    if w < 2:
        p_avoid = 1 - (24/64 if w == 0 else 16/64)
        p_all_avoid *= p_avoid

print(f"    P(all 11 avoid S=2) ≈ {p_all_avoid:.4f} = {p_all_avoid*100:.2f}%")
print(f"    Actual (from sampling): ~2.43%")
print(f"    Ratio: {2.43/100/p_all_avoid:.2f}× (correlation makes it {'harder' if p_all_avoid > 0.0243 else 'easier'})")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS 8: Sample different Eulerian paths, for each compute S=2 absence rate
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("8. S=2 ABSENCE RATE AS A FUNCTION OF EULERIAN PATH")
print("=" * 80)
print(f"\n  Since the weight profile is FIXED, all paths have the same 11 susceptible bridges.")
print(f"  But the S=2 absence rate may still vary because different paths place")
print(f"  these susceptible edges at different positions in the walk,")
print(f"  affecting hexagram correlations.")
print()

# For a proper comparison, we need to sample orderings for EACH Eulerian path.
# Sample 200 Eulerian paths, for each sample 500 orderings.

N_PATHS = 200
N_ORDERINGS = 500

GEN_BITS_6 = {
    'O': (1,0,0,0,0,1), 'M': (0,1,0,0,1,0), 'I': (0,0,1,1,0,0),
    'OM': (1,1,0,0,1,1), 'OI': (1,0,1,1,0,1), 'MI': (0,1,1,1,1,0),
    'OMI': (1,1,1,1,1,1),
}

KW_MASK = {
    (0,0,0): 'OMI', (0,0,1): 'I', (0,1,0): 'M', (0,1,1): 'MI',
    (1,0,0): 'O', (1,0,1): 'OI', (1,1,0): 'OM', (1,1,1): 'OMI',
}

ALL_SIGS = sorted(ORBIT_NAMES.keys())
orbits = defaultdict(list)
for i in range(64):
    h = tuple(M[i])
    orbits[xor_sig(h)].append(h)


def build_matching(sig, gen):
    mask = GEN_BITS_6[gen]
    hexes = orbits[sig]
    remaining = set(hexes)
    pairs = []
    while remaining:
        h = min(remaining)
        p = tuple(h[d] ^ mask[d] for d in range(DIMS))
        remaining.discard(h)
        remaining.discard(p)
        pairs.append((h, p))
    return pairs


def build_sequence_for_path(orbit_walk, mask_assignment, seed):
    """Build 64-hex sequence from an orbit walk + mask assignment."""
    rng = random.Random(seed)
    
    matchings = {sig: build_matching(sig, mask_assignment[sig]) for sig in ALL_SIGS}
    
    orbit_pair_idx = defaultdict(int)
    orbit_pair_order = {}
    for sig in ALL_SIGS:
        order = list(range(4))
        rng.shuffle(order)
        orbit_pair_order[sig] = order
    
    seq = []
    for k in range(32):
        sig = orbit_walk[k]
        idx = orbit_pair_idx[sig]
        pair_slot = orbit_pair_order[sig][idx]
        orbit_pair_idx[sig] = idx + 1
        h_a, h_b = matchings[sig][pair_slot]
        if rng.random() < 0.5:
            h_a, h_b = h_b, h_a
        seq.append(h_a)
        seq.append(h_b)
    return seq


def check_s2_absent(seq):
    for k in range(31):
        h_a = seq[2*k + 1]
        h_b = seq[2*k + 2]
        m = tuple(h_a[d] ^ h_b[d] for d in range(6))
        S = (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])
        if S == 2:
            return False
    return True


print(f"  Sampling {N_PATHS} Eulerian paths, {N_ORDERINGS} orderings each...")
print(f"  Using KW matching (mask=sig) for all.")

rng_path = random.Random(7777)
path_s2_rates = []

# Also do KW path for comparison
kw_s2_count = 0
for o_trial in range(N_ORDERINGS * 4):
    seq = build_sequence_for_path(kw_orbit_walk, KW_MASK, seed=o_trial + 800000)
    if check_s2_absent(seq):
        kw_s2_count += 1
kw_s2_rate = kw_s2_count / (N_ORDERINGS * 4)

t2 = time.time()
for p_idx in range(N_PATHS):
    path = sample_eulerian_path(edge_count, (0,0,0), (1,1,1), rng_path)
    if path is None:
        continue
    
    s2_count = 0
    for o_trial in range(N_ORDERINGS):
        seq = build_sequence_for_path(path, KW_MASK, seed=p_idx * 10000 + o_trial + 900000)
        if check_s2_absent(seq):
            s2_count += 1
    
    path_s2_rates.append(s2_count / N_ORDERINGS)
    
    if (p_idx + 1) % 50 == 0:
        elapsed = time.time() - t2
        print(f"    {p_idx+1}/{N_PATHS} paths processed ({elapsed:.1f}s)")

t3 = time.time()
print(f"  Done in {t3-t2:.1f}s")
print()

if path_s2_rates:
    mean_rate = sum(path_s2_rates) / len(path_s2_rates)
    std_rate = (sum((x - mean_rate)**2 for x in path_s2_rates) / len(path_s2_rates)) ** 0.5
    min_rate = min(path_s2_rates)
    max_rate = max(path_s2_rates)
    
    kw_pctile_rate = 100 * sum(1 for r in path_s2_rates if r <= kw_s2_rate) / len(path_s2_rates)
    
    print(f"  S=2 absence rate distribution across {len(path_s2_rates)} Eulerian paths:")
    print(f"    Mean: {mean_rate:.4f} ({mean_rate*100:.2f}%)")
    print(f"    Std:  {std_rate:.4f}")
    print(f"    Min:  {min_rate:.4f} ({min_rate*100:.2f}%)")
    print(f"    Max:  {max_rate:.4f} ({max_rate*100:.2f}%)")
    print(f"    CV:   {std_rate/mean_rate:.3f}")
    print()
    print(f"  KW Eulerian path S=2 absence rate: {kw_s2_rate:.4f} ({kw_s2_rate*100:.2f}%)")
    print(f"  KW percentile: {kw_pctile_rate:.1f}%")
    print()
    
    # Histogram
    bins = [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05, 0.10, 1.0]
    print(f"  Histogram:")
    for i in range(len(bins) - 1):
        n = sum(1 for r in path_s2_rates if bins[i] <= r < bins[i+1])
        pct = 100 * n / len(path_s2_rates)
        bar = '█' * max(0, int(pct/2))
        lo = bins[i] * 100
        hi = bins[i+1] * 100
        kw_marker = " ← KW" if bins[i] <= kw_s2_rate < bins[i+1] else ""
        print(f"    [{lo:5.1f}%,{hi:5.1f}%): {n:4d} ({pct:5.1f}%) {bar}{kw_marker}")


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()
print("1. The orbit-change weight PROFILE is INVARIANT across all Eulerian paths.")
print(f"   Every path has exactly: w=0:{edge_w_profile[0]}, w=1:{edge_w_profile[1]}, "
      f"w=2:{edge_w_profile[2]}, w=3:{edge_w_profile[3]}")
print(f"   → {edge_w_profile[0] + edge_w_profile[1]} susceptible + "
      f"{edge_w_profile[2] + edge_w_profile[3]} immune = 31 bridges")
print()
print("2. KW's 20/31 immune bridges is NOT a choice — it's the ONLY possible value.")
print("   The 'Level 2b' constraint in the hierarchy collapses:")
print("   EVERY Eulerian path has exactly the same S=2-immune bridge count.")
print()

if path_s2_rates:
    cv = std_rate / mean_rate
    if cv < 0.2:
        print(f"3. S=2 absence rate is approximately path-INDEPENDENT (CV = {cv:.3f}).")
        print(f"   All paths give ~{mean_rate*100:.1f}% S=2 absence rate.")
    else:
        print(f"3. S=2 absence rate VARIES across paths (CV = {cv:.3f}).")
        print(f"   Range: {min_rate*100:.2f}% — {max_rate*100:.2f}%")
        print(f"   KW is at the {kw_pctile_rate:.0f}th percentile.")
    print()
    print(f"4. KW path S=2 absence: {kw_s2_rate*100:.2f}% vs mean {mean_rate*100:.2f}%")

print()
print("=" * 80)
print("PATH SELECTION ANALYSIS COMPLETE")
print("=" * 80)
