"""
Threads C, E, G: Meta-walk structure, generator chain dynamics, anti-generator basis.

Thread C: For sampled Eulerian paths, compute meta-hexagram sequences.
Thread E: For random pair orderings on KW's Eulerian path, compute kernel chains.
Thread G: Rewrite the KW sequence in the factored {orbit, within-orbit} basis.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import time
import math

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

VALID_MASKS = {
    (0,0,0,0,0,0): 'id', (1,0,0,0,0,1): 'O', (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I', (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI', (1,1,1,1,1,1): 'OMI',
}

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}

GEN_FLIPS = {'O': [0, 5], 'M': [1, 4], 'I': [2, 3]}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def xor_tuple(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


# ─── Build orbit multigraph from KW bridges ──────────────────────────────────

edge_count = Counter()
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    edge_count[(xor_sig(a), xor_sig(b))] += 1

# Build KW orbit walk
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))

# KW hexagram sequence as tuples
kw_hex_seq = [tuple(M[i]) for i in range(64)]


# ─── Eulerian path sampler (randomized DFS with backtracking) ─────────────────

def sample_eulerian_path(edge_count, start, end, rng):
    """Sample a random Eulerian path via randomized DFS."""
    remaining = dict(edge_count)
    total = sum(edge_count.values())
    adj = defaultdict(list)
    for (u, v) in edge_count:
        if v not in adj[u]:
            adj[u].append(v)
    for u in adj:
        adj[u].sort()

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


# ─── Meta-hexagram computation ────────────────────────────────────────────────

def orbit_walk_to_meta_hexagrams(orbit_walk):
    """
    Given a 32-element orbit walk (list of 3-bit orbit sigs),
    produce 31 meta-hexagrams by stacking consecutive signatures.

    Meta-hexagram at bridge k = (sig_k[0], sig_k[1], sig_k[2], sig_{k+1}[0], sig_{k+1}[1], sig_{k+1}[2])
    """
    metas = []
    for k in range(len(orbit_walk) - 1):
        s1 = orbit_walk[k]
        s2 = orbit_walk[k + 1]
        meta = (s1[0], s1[1], s1[2], s2[0], s2[1], s2[2])
        metas.append(meta)
    return metas


def meta_signature(meta_hex):
    """XOR signature of a 6-bit meta-hexagram: (bit0⊕bit5, bit1⊕bit4, bit2⊕bit3)."""
    return (meta_hex[0] ^ meta_hex[5], meta_hex[1] ^ meta_hex[4], meta_hex[2] ^ meta_hex[3])


def meta_walk_stats(orbit_walk):
    """Compute statistics of the meta-hexagram walk for a given orbit walk."""
    metas = orbit_walk_to_meta_hexagrams(orbit_walk)
    n_total = len(metas)
    unique = set(metas)
    n_unique = len(unique)

    freq = Counter(metas)
    most_common_hex, most_common_count = freq.most_common(1)[0]

    # Meta-signature distribution
    meta_sigs = [meta_signature(m) for m in metas]
    meta_sig_dist = Counter(meta_sigs)

    # Mean meta weight
    weights = [sum(m) for m in metas]
    mean_weight = sum(weights) / n_total

    # Meta-orbit distribution
    meta_orbits = [xor_sig(list(m)) for m in metas]  # treating meta as hex for orbit
    # Actually meta_signature IS the orbit signature of the meta-hex
    meta_orbit_dist = Counter(meta_sigs)

    return {
        'n_unique': n_unique,
        'n_total': n_total,
        'most_common': most_common_hex,
        'most_common_count': most_common_count,
        'meta_sig_dist': dict(meta_sig_dist),
        'mean_weight': mean_weight,
        'meta_orbit_dist': dict(meta_orbit_dist),
        'freq': dict(freq),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD C: META-HEXAGRAM WALK STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("THREAD C: META-HEXAGRAM WALK STRUCTURE")
print("=" * 70)

# KW meta-walk reference
kw_meta_stats = meta_walk_stats(kw_orbit_walk)
print(f"\nKW meta-walk: {kw_meta_stats['n_unique']}/31 unique meta-hexagrams")
print(f"  Most common: {kw_meta_stats['most_common']} appearing {kw_meta_stats['most_common_count']}×")

# Map meta-hex to KW number for reference
hex_to_kw = {}
for i in range(64):
    hex_to_kw[tuple(M[i])] = KING_WEN[i]
if kw_meta_stats['most_common'] in hex_to_kw:
    mc_info = hex_to_kw[kw_meta_stats['most_common']]
    print(f"  = #{mc_info[0]} {mc_info[1]}")

print(f"  Mean meta-weight: {kw_meta_stats['mean_weight']:.3f}")
print(f"  Meta-sig distribution: {kw_meta_stats['meta_sig_dist']}")

# Show full KW meta-hexagram list
kw_metas = orbit_walk_to_meta_hexagrams(kw_orbit_walk)
print(f"\n  Full KW meta-hexagram sequence:")
for k, meta in enumerate(kw_metas):
    kw_info = hex_to_kw.get(meta, (None, '???'))
    sig = meta_signature(meta)
    sig_name = KERNEL_NAMES[sig]
    freq = kw_meta_stats['freq'][meta]
    marker = f" ×{freq}" if freq > 1 else ""
    print(f"    B{k:2d}: {meta}  #{kw_info[0]:2d} {kw_info[1]:<12s}  meta-sig={sig} ({sig_name}){marker}")


# ─── Sample 10,000 Eulerian paths and compute meta-walk stats ─────────────────

N_SAMPLES = 10_000
rng = random.Random(42)

print(f"\nSampling {N_SAMPLES} Eulerian paths for meta-walk analysis...")
t0 = time.time()

unique_counts = []
max_repeat_counts = []
most_common_hexes = Counter()
mean_weights = []
meta_sig_tallies = Counter()  # across all paths, all bridges
n_valid = 0

# Track which specific meta-hexagrams appear
meta_hex_frequency = Counter()  # global frequency across all paths+bridges

for i in range(N_SAMPLES):
    path = sample_eulerian_path(edge_count, (0,0,0), (1,1,1), rng)
    if path is None:
        continue
    n_valid += 1

    stats = meta_walk_stats(path)
    unique_counts.append(stats['n_unique'])
    max_repeat_counts.append(stats['most_common_count'])
    most_common_hexes[stats['most_common']] += 1
    mean_weights.append(stats['mean_weight'])

    for sig, cnt in stats['meta_sig_dist'].items():
        meta_sig_tallies[sig] += cnt

    for meta_hex, cnt in stats['freq'].items():
        meta_hex_frequency[meta_hex] += cnt

    if (i + 1) % 2000 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{N_SAMPLES} ({n_valid} valid, {elapsed:.1f}s)")

t1 = time.time()
print(f"\nDone: {n_valid} valid paths in {t1-t0:.1f}s")

# ─── Thread C Results ─────────────────────────────────────────────────────────

print(f"\n{'─'*70}")
print("THREAD C RESULTS: META-HEXAGRAM UNIQUENESS")
print(f"{'─'*70}")

unique_counter = Counter(unique_counts)
print(f"\nDistribution of unique meta-hexagrams (out of 31):")
for u in sorted(unique_counter.keys()):
    pct = 100 * unique_counter[u] / n_valid
    bar = '█' * max(1, int(pct / 2))
    print(f"  {u:2d}/31: {unique_counter[u]:5d} ({pct:5.1f}%) {bar}")

mean_unique = sum(unique_counts) / n_valid
kw_unique = kw_meta_stats['n_unique']
above_kw = sum(1 for u in unique_counts if u >= kw_unique)
print(f"\nMean unique: {mean_unique:.2f}")
print(f"KW unique: {kw_unique}")
print(f"P(≥{kw_unique} unique) = {above_kw}/{n_valid} = {100*above_kw/n_valid:.2f}%")

# Max repeat distribution
print(f"\n{'─'*70}")
print("MAX REPEAT COUNT (most-repeated meta-hexagram)")
print(f"{'─'*70}")

repeat_counter = Counter(max_repeat_counts)
for r in sorted(repeat_counter.keys()):
    pct = 100 * repeat_counter[r] / n_valid
    print(f"  max_repeat={r}: {repeat_counter[r]:5d} ({pct:5.1f}%)")

kw_max_repeat = kw_meta_stats['most_common_count']
above_kw_repeat = sum(1 for r in max_repeat_counts if r >= kw_max_repeat)
print(f"\nKW max repeat: {kw_max_repeat}")
print(f"P(max_repeat≥{kw_max_repeat}) = {above_kw_repeat}/{n_valid} = {100*above_kw_repeat/n_valid:.2f}%")

# Which meta-hexagram is most commonly the "most repeated"?
print(f"\nMost-repeated meta-hexagram identity (top 10):")
for meta_hex, cnt in most_common_hexes.most_common(10):
    kw_info = hex_to_kw.get(meta_hex, (None, '???'))
    pct = 100 * cnt / n_valid
    kw_marker = " ★ KW" if meta_hex == kw_meta_stats['most_common'] else ""
    print(f"  {meta_hex} #{kw_info[0]:2d} {kw_info[1]:<12s}: {cnt:5d} ({pct:5.1f}%){kw_marker}")

# KW's specific most-common (#38 Kui = (1,1,0,1,0,1))
kw_mc = kw_meta_stats['most_common']
kui_count = most_common_hexes.get(kw_mc, 0)
print(f"\nKW's most-common ({hex_to_kw.get(kw_mc, (None,'?'))[1]}) as top in sample: {kui_count}/{n_valid} ({100*kui_count/n_valid:.1f}%)")

# Mean weight distribution
print(f"\n{'─'*70}")
print("META-HEXAGRAM MEAN WEIGHT")
print(f"{'─'*70}")
mean_w_overall = sum(mean_weights) / n_valid
print(f"Overall mean weight across samples: {mean_w_overall:.4f}")
print(f"KW mean meta-weight: {kw_meta_stats['mean_weight']:.4f}")
# Standard deviation
var_w = sum((w - mean_w_overall) ** 2 for w in mean_weights) / n_valid
std_w = var_w ** 0.5
print(f"Std dev: {std_w:.4f}")
kw_z = (kw_meta_stats['mean_weight'] - mean_w_overall) / std_w if std_w > 0 else 0
print(f"KW z-score: {kw_z:.2f}")

# Meta-signature distribution (aggregated over all paths)
print(f"\n{'─'*70}")
print("META-SIGNATURE DISTRIBUTION (aggregated)")
print(f"{'─'*70}")
total_meta_bridges = sum(meta_sig_tallies.values())
for sig in sorted(meta_sig_tallies.keys()):
    cnt = meta_sig_tallies[sig]
    pct = 100 * cnt / total_meta_bridges
    name = KERNEL_NAMES[sig]
    print(f"  {sig} ({name:>3s}): {cnt:7d} ({pct:5.1f}%)")

# Compare to KW
print(f"\nKW meta-sig dist (31 bridges):")
for sig in sorted(kw_meta_stats['meta_sig_dist'].keys()):
    cnt = kw_meta_stats['meta_sig_dist'][sig]
    pct = 100 * cnt / 31
    name = KERNEL_NAMES[sig]
    print(f"  {sig} ({name:>3s}): {cnt:2d} ({pct:5.1f}%)")

# Which meta-hexagrams appear most globally?
print(f"\n{'─'*70}")
print("GLOBALLY MOST FREQUENT META-HEXAGRAMS")
print(f"{'─'*70}")
for meta_hex, cnt in meta_hex_frequency.most_common(15):
    kw_info = hex_to_kw.get(meta_hex, (None, '???'))
    avg_per_path = cnt / n_valid
    kw_marker = " ★" if meta_hex in kw_meta_stats['freq'] else ""
    print(f"  {meta_hex} #{kw_info[0]:2d} {kw_info[1]:<12s}: {cnt:7d} (avg {avg_per_path:.2f}/path){kw_marker}")


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD E: GENERATOR (KERNEL) CHAIN DYNAMICS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n\n{'='*70}")
print("THREAD E: GENERATOR CHAIN DYNAMICS")
print("=" * 70)

# ─── KW kernel dressing sequence ──────────────────────────────────────────────

# Extract kernel dressing from each bridge: symmetric component of bridge mask
# kernel = (m[5], m[4], m[3]) = (m₆, m₅, m₄) in the notation where m = (m₁...m₆)
# But since kernel element is (a,b,c,c,b,a), kernel 3-bit code = (m[5], m[4], m[3])

kw_kernels_3bit = []
kw_kernels_named = []
for k in range(31):
    a = kw_hex_seq[2*k + 1]
    b = kw_hex_seq[2*k + 2]
    mask = tuple(a[d] ^ b[d] for d in range(DIMS))
    kernel_3 = (mask[5], mask[4], mask[3])
    kw_kernels_3bit.append(kernel_3)
    kw_kernels_named.append(KERNEL_NAMES[kernel_3])

print(f"\nKW kernel dressing sequence (31 bridges):")
for k in range(31):
    print(f"  B{k:2d}: {kw_kernels_named[k]:>4s}  {kw_kernels_3bit[k]}")

kw_kernel_freq = Counter(kw_kernels_named)
print(f"\nKW kernel frequency:")
for name, cnt in sorted(kw_kernel_freq.items(), key=lambda x: -x[1]):
    print(f"  {name:>4s}: {cnt}×  (expected {31/8:.1f})")


# ─── Random pair orderings on KW's Eulerian path ─────────────────────────────

# Build orbit contents with KW's uniform matching (mask=sig)
def build_kw_orbit_pairs():
    """
    For each orbit, build the 4 KW pairs.
    Returns: dict orbit_sig -> list of (first_hex, second_hex) pairs
    """
    orbit_pairs = defaultdict(list)
    for k in range(32):
        a = tuple(M[2*k])
        b = tuple(M[2*k+1])
        sig = xor_sig(a)
        orbit_pairs[sig].append((a, b))
    return orbit_pairs

kw_orbit_pairs = build_kw_orbit_pairs()

def random_completion_on_kw_path(rng):
    """
    Given KW's Eulerian orbit path and KW's matching (mask=sig),
    randomly assign pair-slots and orientations.
    Returns: 64-element hexagram sequence.
    """
    # For each orbit, shuffle pair assignment order and orientations
    orbit_queues = {}
    for sig, pairs in kw_orbit_pairs.items():
        shuffled = list(pairs)
        rng.shuffle(shuffled)
        oriented = []
        for a, b in shuffled:
            if rng.random() < 0.5:
                oriented.append((a, b))
            else:
                oriented.append((b, a))
        orbit_queues[sig] = oriented

    # Walk the KW orbit path, assigning pairs
    seq = []
    visit_count = defaultdict(int)
    for k in range(32):
        sig = kw_orbit_walk[k]
        idx = visit_count[sig]
        visit_count[sig] += 1
        pair = orbit_queues[sig][idx]
        seq.extend(pair)
    return seq


def extract_kernel_chain(seq):
    """Extract the 31-element kernel dressing chain from a 64-hex sequence."""
    kernels = []
    for k in range(31):
        a = seq[2*k + 1]
        b = seq[2*k + 2]
        mask = tuple(a[d] ^ b[d] for d in range(DIMS))
        kernel_3 = (mask[5], mask[4], mask[3])
        kernels.append(kernel_3)
    return kernels


def kernel_chain_stats(kernels):
    """Compute statistics of a kernel chain."""
    named = [KERNEL_NAMES[k] for k in kernels]
    freq = Counter(named)
    n = len(kernels)

    # Frequency uniformity (chi-squared from uniform 31/8)
    expected = n / 8
    chi2 = sum((freq.get(name, 0) - expected) ** 2 / expected
               for name in KERNEL_NAMES.values())

    # Autocorrelation at lag 1: fraction where kernel[k] == kernel[k+1]
    auto_1 = sum(1 for i in range(n-1) if kernels[i] == kernels[i+1]) / (n-1)

    # XOR autocorrelation: consecutive kernel XORs
    xor_chain = [tuple(kernels[i][d] ^ kernels[i+1][d] for d in range(3))
                 for i in range(n-1)]
    xor_freq = Counter(xor_chain)

    # Return times: for each kernel, gaps between consecutive uses
    positions = defaultdict(list)
    for i, k in enumerate(kernels):
        positions[k].append(i)
    return_times = []
    for k, poslist in positions.items():
        for i in range(len(poslist) - 1):
            return_times.append(poslist[i+1] - poslist[i])

    mean_return = sum(return_times) / len(return_times) if return_times else 0

    return {
        'freq': dict(freq),
        'chi2': chi2,
        'auto_1': auto_1,
        'xor_freq': dict(xor_freq),
        'mean_return': mean_return,
        'return_times': return_times,
    }


# KW kernel chain stats
kw_chain_stats = kernel_chain_stats(kw_kernels_3bit)
print(f"\nKW kernel chain statistics:")
print(f"  Chi² from uniform: {kw_chain_stats['chi2']:.3f}")
print(f"  Lag-1 autocorrelation (repeat rate): {kw_chain_stats['auto_1']:.3f}")
print(f"  Mean return time: {kw_chain_stats['mean_return']:.2f}")

print(f"\n  KW consecutive-kernel XOR distribution:")
for xor_val, cnt in sorted(kw_chain_stats['xor_freq'].items(), key=lambda x: -x[1]):
    name = KERNEL_NAMES[xor_val]
    print(f"    {xor_val} ({name:>3s}): {cnt}×")

# ─── Sample 10,000 random completions ─────────────────────────────────────────

N_E_SAMPLES = 10_000
rng_e = random.Random(99)

print(f"\nSampling {N_E_SAMPLES} random pair orderings (KW Eulerian path + KW matching)...")
t0 = time.time()

chi2_samples = []
auto1_samples = []
return_time_samples = []
freq_samples = []  # list of frequency dicts
xor_freq_tallies = Counter()
n_e_valid = 0

for i in range(N_E_SAMPLES):
    seq = random_completion_on_kw_path(rng_e)
    kernels = extract_kernel_chain(seq)
    stats = kernel_chain_stats(kernels)

    chi2_samples.append(stats['chi2'])
    auto1_samples.append(stats['auto_1'])
    return_time_samples.append(stats['mean_return'])
    freq_samples.append(stats['freq'])
    for xor_val, cnt in stats['xor_freq'].items():
        xor_freq_tallies[xor_val] += cnt
    n_e_valid += 1

    if (i + 1) % 2000 == 0:
        print(f"  {i+1}/{N_E_SAMPLES}")

t1 = time.time()
print(f"Done: {n_e_valid} samples in {t1-t0:.1f}s")

# ─── Thread E Results ─────────────────────────────────────────────────────────

print(f"\n{'─'*70}")
print("THREAD E RESULTS: KERNEL CHAIN UNIFORMITY")
print(f"{'─'*70}")

mean_chi2 = sum(chi2_samples) / n_e_valid
std_chi2 = (sum((c - mean_chi2)**2 for c in chi2_samples) / n_e_valid) ** 0.5
kw_chi2_pct = sum(1 for c in chi2_samples if c <= kw_chain_stats['chi2']) / n_e_valid
print(f"\nChi² from uniform (lower = more uniform):")
print(f"  KW: {kw_chain_stats['chi2']:.3f}")
print(f"  Sample mean: {mean_chi2:.3f} ± {std_chi2:.3f}")
print(f"  P(chi² ≤ KW): {kw_chi2_pct:.4f}")

print(f"\n{'─'*70}")
print("KERNEL CHAIN AUTOCORRELATION")
print(f"{'─'*70}")

mean_auto = sum(auto1_samples) / n_e_valid
std_auto = (sum((a - mean_auto)**2 for a in auto1_samples) / n_e_valid) ** 0.5
kw_auto_pct = sum(1 for a in auto1_samples if a <= kw_chain_stats['auto_1']) / n_e_valid
print(f"\nLag-1 autocorrelation (lower = less repetitive):")
print(f"  KW: {kw_chain_stats['auto_1']:.4f}")
print(f"  Sample mean: {mean_auto:.4f} ± {std_auto:.4f}")
print(f"  P(auto ≤ KW): {kw_auto_pct:.4f}")

print(f"\n{'─'*70}")
print("KERNEL CHAIN RETURN TIMES")
print(f"{'─'*70}")

mean_rt = sum(return_time_samples) / n_e_valid
std_rt = (sum((r - mean_rt)**2 for r in return_time_samples) / n_e_valid) ** 0.5
print(f"\nMean return time:")
print(f"  KW: {kw_chain_stats['mean_return']:.3f}")
print(f"  Sample mean: {mean_rt:.3f} ± {std_rt:.3f}")

# Kernel frequency distribution comparison
print(f"\n{'─'*70}")
print("KERNEL FREQUENCY DISTRIBUTIONS")
print(f"{'─'*70}")

# Compute mean frequency per generator across samples
mean_freq = {}
for name in KERNEL_NAMES.values():
    vals = [f.get(name, 0) for f in freq_samples]
    mean_freq[name] = sum(vals) / n_e_valid
    std = (sum((v - mean_freq[name])**2 for v in vals) / n_e_valid) ** 0.5
    kw_val = kw_kernel_freq.get(name, 0)
    print(f"  {name:>4s}: KW={kw_val:d}, sample mean={mean_freq[name]:.2f}±{std:.2f}")

# XOR chain frequency
print(f"\n{'─'*70}")
print("CONSECUTIVE KERNEL XOR DISTRIBUTION")
print(f"{'─'*70}")
total_xor = sum(xor_freq_tallies.values())
print(f"\nAggregate XOR distribution ({total_xor} total):")
for xor_val in sorted(xor_freq_tallies.keys()):
    cnt = xor_freq_tallies[xor_val]
    pct = 100 * cnt / total_xor
    name = KERNEL_NAMES[xor_val]
    kw_cnt = kw_chain_stats['xor_freq'].get(xor_val, 0)
    kw_pct = 100 * kw_cnt / 30 if kw_cnt > 0 else 0
    print(f"  {xor_val} ({name:>3s}): sample {pct:5.1f}%  KW {kw_pct:5.1f}% ({kw_cnt}/30)")


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD G: ANTI-GENERATOR (FACTORED) BASIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n\n{'='*70}")
print("THREAD G: ANTI-GENERATOR (FACTORED) BASIS")
print("=" * 70)

# Every hexagram h = (l₁,l₂,l₃,l₄,l₅,l₆) can be rewritten as:
#   orbit coords (ō, m̄, ī) = (l₁⊕l₆, l₂⊕l₅, l₃⊕l₄) — the asymmetric part
#   within-orbit coords (o, m, i) = (l₆, l₅, l₄) — the "base" position
#
# The original can be recovered: l_upper = ō⊕o, l_mid_upper = m̄⊕m, l_inner_upper = ī⊕i
#                                 l_inner_lower = i, l_mid_lower = m, l_lower = o
#
# Actually: l₁ = ō⊕l₆ = ō⊕o, l₂ = m̄⊕l₅ = m̄⊕m, l₃ = ī⊕l₄ = ī⊕i
#           l₄ = i, l₅ = m, l₆ = o

print(f"\nFactored basis: each hexagram (l₁,l₂,l₃,l₄,l₅,l₆) ↦ (ō,m̄,ī | o,m,i)")
print(f"  where ō=l₁⊕l₆, m̄=l₂⊕l₅, ī=l₃⊕l₄ (orbit), o=l₆, m=l₅, i=l₄ (position)")

def to_factored(h):
    """Convert hexagram to (orbit_coords, position_coords)."""
    orbit = (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])
    pos = (h[5], h[4], h[3])
    return orbit, pos

print(f"\nKW sequence in factored basis:")
print(f"  {'Pos':>3s}  {'KW#':>3s}  {'Name':<12s}  {'Hex':>6s}  {'Orbit':>5s}  {'Pos':>5s}  {'Orbit→':>7s}  {'Pos→':>5s}")
print(f"  {'─'*3}  {'─'*3}  {'─'*12}  {'─'*6}  {'─'*5}  {'─'*5}  {'─'*7}  {'─'*5}")

orbit_trajectory = []
pos_trajectory = []
for i in range(64):
    h = kw_hex_seq[i]
    orbit, pos = to_factored(h)
    orbit_trajectory.append(orbit)
    pos_trajectory.append(pos)
    kw_num = KING_WEN[i][0]
    kw_name = KING_WEN[i][1]

    # Compute deltas from previous
    if i > 0:
        prev_o, prev_p = to_factored(kw_hex_seq[i-1])
        d_orbit = tuple(orbit[d] ^ prev_o[d] for d in range(3))
        d_pos = tuple(pos[d] ^ prev_p[d] for d in range(3))
        d_orbit_s = ''.join(map(str, d_orbit))
        d_pos_s = ''.join(map(str, d_pos))
    else:
        d_orbit_s = '  —  '
        d_pos_s = '  —  '

    hex_s = ''.join(map(str, h))
    orb_s = ''.join(map(str, orbit))
    pos_s = ''.join(map(str, pos))

    # Mark pair boundaries
    is_bridge = (i > 0 and i % 2 == 0)
    marker = "│" if is_bridge else " "

    print(f"  {i+1:3d}  {kw_num:3d}  {kw_name:<12s}  {hex_s}  {orb_s}    {pos_s}   Δ{d_orbit_s}  Δ{d_pos_s}{marker}")

# ─── Analyze orbit and position trajectories separately ───────────────────────

print(f"\n{'─'*70}")
print("ORBIT TRAJECTORY (3-bit, 64 steps)")
print(f"{'─'*70}")

# Orbit changes
orbit_changes = []
for i in range(63):
    d = tuple(orbit_trajectory[i][d] ^ orbit_trajectory[i+1][d] for d in range(3))
    orbit_changes.append(d)

# Within-pair orbit changes (should always be the mask generators)
pair_orbit_changes = [orbit_changes[2*k] for k in range(32) if 2*k < 63]
bridge_orbit_changes = [orbit_changes[2*k+1] for k in range(31)]

print(f"\nWithin-pair orbit changes (should be mask = sig for KW):")
pair_oc_freq = Counter(pair_orbit_changes)
for oc, cnt in sorted(pair_oc_freq.items(), key=lambda x: -x[1]):
    name = KERNEL_NAMES[oc]
    print(f"  {oc} ({name:>3s}): {cnt}×")

print(f"\nBridge orbit changes:")
bridge_oc_freq = Counter(bridge_orbit_changes)
for oc, cnt in sorted(bridge_oc_freq.items(), key=lambda x: -x[1]):
    name = KERNEL_NAMES[oc]
    print(f"  {oc} ({name:>3s}): {cnt}×")

# ─── Position trajectory analysis ─────────────────────────────────────────────

print(f"\n{'─'*70}")
print("POSITION TRAJECTORY (3-bit within-orbit coords, 64 steps)")
print(f"{'─'*70}")

pos_changes = []
for i in range(63):
    d = tuple(pos_trajectory[i][d] ^ pos_trajectory[i+1][d] for d in range(3))
    pos_changes.append(d)

pair_pos_changes = [pos_changes[2*k] for k in range(32) if 2*k < 63]
bridge_pos_changes = [pos_changes[2*k+1] for k in range(31)]

print(f"\nWithin-pair position changes:")
pair_pc_freq = Counter(pair_pos_changes)
for pc, cnt in sorted(pair_pc_freq.items(), key=lambda x: -x[1]):
    name = KERNEL_NAMES[pc]
    print(f"  {pc} ({name:>3s}): {cnt}×")

print(f"\nBridge position changes (= kernel dressing in the standard decomposition):")
bridge_pc_freq = Counter(bridge_pos_changes)
for pc, cnt in sorted(bridge_pc_freq.items(), key=lambda x: -x[1]):
    name = KERNEL_NAMES[pc]
    print(f"  {pc} ({name:>3s}): {cnt}×")

# Verify: bridge position change = kernel dressing from Thread E
print(f"\nVerification: bridge position change matches kernel dressing?")
match_count = 0
for k in range(31):
    if bridge_pos_changes[k] == kw_kernels_3bit[k]:
        match_count += 1
print(f"  {match_count}/31 match")

# ─── Position trajectory: is it structured? ───────────────────────────────────

print(f"\n{'─'*70}")
print("POSITION TRAJECTORY: VISIT PATTERN")
print(f"{'─'*70}")

# Within each orbit visit (4 visits × 2 hexagrams = 8 hexagrams), track position coords
orbit_visit_positions = defaultdict(list)
for k in range(32):
    sig = kw_orbit_walk[k]
    for j in [2*k, 2*k+1]:
        orbit_visit_positions[sig].append(pos_trajectory[j])

print(f"\nPosition coordinates visited per orbit:")
for sig in sorted(orbit_visit_positions.keys()):
    positions = orbit_visit_positions[sig]
    unique_pos = set(positions)
    print(f"  {ORBIT_NAMES[sig]:>6s}: {len(unique_pos)}/8 unique positions → {''.join(''.join(map(str,p))+' ' for p in positions)}")

# Check: does each orbit visit all 8 positions?
all_complete = all(len(set(orbit_visit_positions[sig])) == 8 for sig in orbit_visit_positions)
print(f"\n  All orbits visit all 8 positions: {all_complete}")

# ─── Combined: orbit×position as factored walk ───────────────────────────────

print(f"\n{'─'*70}")
print("FACTORED WALK: ORBIT AND POSITION INDEPENDENCE")
print(f"{'─'*70}")

# At pair level: orbit changes by mask (forced by pairing), position changes by mask (same mask)
# At bridge level: orbit changes freely, position changes freely (kernel dressing)
# Are orbit and position changes correlated at bridges?

# For each bridge, record (orbit_change, position_change)
joint_bridge_changes = []
for k in range(31):
    joint_bridge_changes.append((bridge_orbit_changes[k], bridge_pos_changes[k]))

joint_freq = Counter(joint_bridge_changes)
print(f"\nJoint (orbit_change, position_change) at bridges:")
print(f"  {'Orbit Δ':>8s}  {'Pos Δ':>8s}  Count")
for (oc, pc), cnt in sorted(joint_freq.items(), key=lambda x: -x[1]):
    oc_name = KERNEL_NAMES[oc]
    pc_name = KERNEL_NAMES[pc]
    print(f"  {oc_name:>8s}  {pc_name:>8s}  {cnt:3d}")

# Test independence: if orbit and position changes were independent,
# P(oc, pc) = P(oc) × P(pc). Chi² test.
n_bridges = 31
expected_joint = {}
for oc in set(bridge_orbit_changes):
    for pc in set(bridge_pos_changes):
        p_oc = bridge_oc_freq[oc] / n_bridges
        p_pc = bridge_pc_freq[pc] / n_bridges
        expected_joint[(oc, pc)] = p_oc * p_pc * n_bridges

chi2_independence = 0
for key in set(list(joint_freq.keys()) + list(expected_joint.keys())):
    obs = joint_freq.get(key, 0)
    exp = expected_joint.get(key, 0)
    if exp > 0:
        chi2_independence += (obs - exp) ** 2 / exp

print(f"\nChi² test for independence of orbit and position changes:")
print(f"  Chi² = {chi2_independence:.2f}")
print(f"  (df ≈ (n_orbit_changes - 1) × (n_pos_changes - 1) = "
      f"{(len(bridge_oc_freq)-1) * (len(bridge_pc_freq)-1)})")


print(f"\n\n{'='*70}")
print("ALL THREADS COMPLETE")
print("=" * 70)
