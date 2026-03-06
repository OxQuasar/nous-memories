"""
Pair-level analysis of the King Wen sequence.

Treat each adjacent pair (hex[2k], hex[2k+1]) as a unit.
Characterize pairs and find relationships between them.
"""

import numpy as np
from collections import Counter
from sequence import KING_WEN, all_bits, name, lower_trigram, upper_trigram, trigram_name

N = 64
DIMS = 6
N_PAIRS = 32
N_TRIALS = 10000
RNG = np.random.default_rng(42)

M = np.array(all_bits())

# Build pair structures
pairs = []
for k in range(N_PAIRS):
    a = M[2 * k]
    b = M[2 * k + 1]
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    center = (a + b) / 2.0
    pairs.append({
        'idx': k,
        'a': tuple(a), 'b': tuple(b),
        'num_a': KING_WEN[2 * k][0], 'num_b': KING_WEN[2 * k + 1][0],
        'name_a': KING_WEN[2 * k][1], 'name_b': KING_WEN[2 * k + 1][1],
        'xor': xor,
        'n_flips': sum(xor),
        'center': center,
    })


# ─── 1. Internal Masks ───────────────────────────────────────────────────────

def analyze_masks():
    print("=" * 70)
    print("1. INTERNAL PAIR MASKS (which lines flip within each pair)")
    print("=" * 70)

    print(f"\n  {'Pair':>4s}  {'Hex A':>6s} {'Hex B':>6s}  {'Mask':>6s}  Flips  Names")
    for p in pairs:
        mask_str = ''.join(map(str, p['xor']))
        print(f"  {p['idx']+1:4d}  {p['num_a']:6d} {p['num_b']:6d}  "
              f"{mask_str}  {p['n_flips']:5d}  "
              f"{p['name_a']}-{p['name_b']}")

    # Group by mask
    mask_counts = Counter(p['xor'] for p in pairs)
    print(f"\n  Unique masks: {len(mask_counts)}/32")
    print(f"\n  Mask frequency:")
    for mask, count in mask_counts.most_common():
        mask_str = ''.join(map(str, mask))
        which = [p['idx'] + 1 for p in pairs if p['xor'] == mask]
        print(f"    {mask_str} ({sum(mask)} flips): {count}x — pairs {which}")

    # Flip count distribution
    flip_counts = Counter(p['n_flips'] for p in pairs)
    print(f"\n  Flip count distribution:")
    for n in sorted(flip_counts):
        print(f"    {n} lines flip: {flip_counts[n]} pairs")

    # Which lines are most involved in pair flips?
    line_freq = np.zeros(DIMS)
    for p in pairs:
        for i in range(DIMS):
            line_freq[i] += p['xor'][i]
    print(f"\n  Per-line flip frequency across all pairs:")
    for i in range(DIMS):
        print(f"    L{i+1}: {int(line_freq[i])}/32 pairs ({line_freq[i]/N_PAIRS*100:.1f}%)")


# ─── 2. Center Geometry ──────────────────────────────────────────────────────

def analyze_centers():
    print("\n" + "=" * 70)
    print("2. PAIR CENTERS IN HYPERCUBE")
    print("=" * 70)

    centers = np.array([p['center'] for p in pairs])

    # Distance matrix between centers
    from scipy.spatial.distance import pdist, squareform
    dists = squareform(pdist(centers, 'euclidean'))

    # Nearest neighbor for each pair
    print(f"\n  Nearest neighbors (by Euclidean distance of centers):")
    for i in range(N_PAIRS):
        row = dists[i].copy()
        row[i] = np.inf
        nn = np.argmin(row)
        print(f"    Pair {i+1:2d} → Pair {nn+1:2d} (dist={dists[i, nn]:.3f})")

    # Are sequential pairs close in center space?
    sequential_dists = [dists[k, k + 1] for k in range(N_PAIRS - 1)]
    all_dists = dists[np.triu_indices(N_PAIRS, k=1)]
    print(f"\n  Sequential pair center distances:")
    print(f"    Mean sequential: {np.mean(sequential_dists):.3f}")
    print(f"    Mean all pairs:  {np.mean(all_dists):.3f}")
    print(f"    Sequential range: {min(sequential_dists):.3f} - {max(sequential_dists):.3f}")

    # Center distribution per dimension
    print(f"\n  Center values per dimension:")
    for d in range(DIMS):
        vals = centers[:, d]
        unique = sorted(set(vals))
        counts = Counter(vals)
        print(f"    Dim {d+1}: values={[f'{v:.1f}' for v in unique]}, "
              f"counts={[counts[v] for v in unique]}")

    # Do centers cluster?
    print(f"\n  Center positions (possible values: 0.0, 0.5, 1.0):")
    center_types = Counter(tuple(p['center']) for p in pairs)
    print(f"    Unique center positions: {len(center_types)}/32")
    if len(center_types) < 32:
        for ct, count in center_types.most_common(10):
            ct_str = ''.join(f'{v:.0f}' if v in (0, 1) else '½' for v in ct)
            which = [p['idx'] + 1 for p in pairs if tuple(p['center']) == ct]
            print(f"    {ct_str}: {count}x — pairs {which}")


# ─── 3. Bridge Transitions ───────────────────────────────────────────────────

def analyze_bridges():
    print("\n" + "=" * 70)
    print("3. BRIDGE TRANSITIONS (between pairs)")
    print("=" * 70)

    bridges = []
    for k in range(N_PAIRS - 1):
        exit_hex = M[2 * k + 1]      # second hex of pair k
        entry_hex = M[2 * (k + 1)]   # first hex of pair k+1
        xor = tuple(int(exit_hex[i]) ^ int(entry_hex[i]) for i in range(DIMS))
        hamming = sum(xor)
        bridges.append({
            'from_pair': k,
            'to_pair': k + 1,
            'xor': xor,
            'hamming': hamming,
        })

    # Bridge Hamming distances
    bridge_h = [b['hamming'] for b in bridges]
    intra_h = [p['n_flips'] for p in pairs]
    print(f"\n  Bridge Hamming distances (pair exit → next pair entry):")
    print(f"    Distribution: {Counter(bridge_h)}")
    print(f"    Mean: {np.mean(bridge_h):.2f}")
    print(f"\n  Intra-pair Hamming distances (for comparison):")
    print(f"    Distribution: {Counter(intra_h)}")
    print(f"    Mean: {np.mean(intra_h):.2f}")

    # Bridge masks
    bridge_masks = Counter(b['xor'] for b in bridges)
    print(f"\n  Unique bridge masks: {len(bridge_masks)}/31")
    print(f"  Most common bridge masks:")
    for mask, count in bridge_masks.most_common(10):
        mask_str = ''.join(map(str, mask))
        print(f"    {mask_str} ({sum(mask)} flips): {count}x")

    # Per-line frequency in bridges vs intra-pair
    print(f"\n  Per-line flip frequency:")
    print(f"    {'Line':>6s}  {'Intra':>6s}  {'Bridge':>6s}")
    bridge_line = np.zeros(DIMS)
    intra_line = np.zeros(DIMS)
    for b in bridges:
        for i in range(DIMS):
            bridge_line[i] += b['xor'][i]
    for p in pairs:
        for i in range(DIMS):
            intra_line[i] += p['xor'][i]
    for i in range(DIMS):
        print(f"    L{i+1}:    {int(intra_line[i]):3d}/32  {int(bridge_line[i]):3d}/31")

    # Are bridges inversions too?
    print(f"\n  Bridge structure test:")
    inversion_count = 0
    complement_count = 0
    for b in bridges:
        exit_hex = M[2 * b['from_pair'] + 1]
        entry_hex = M[2 * b['to_pair']]
        is_inv = all(exit_hex[i] == entry_hex[DIMS - 1 - i] for i in range(DIMS))
        is_comp = all(exit_hex[i] != entry_hex[i] for i in range(DIMS))
        if is_inv:
            inversion_count += 1
        if is_comp:
            complement_count += 1
    print(f"    Inversions: {inversion_count}/31")
    print(f"    Complements: {complement_count}/31")
    print(f"    Neither: {31 - inversion_count - complement_count}/31")

    return bridges


# ─── 4. Pair Offset Structure ────────────────────────────────────────────────

def analyze_pair_offsets():
    print("\n" + "=" * 70)
    print("4. PAIR-LEVEL OFFSET STRUCTURE")
    print("=" * 70)

    # Offset analysis at the pair level
    # Compare pair masks at different offsets
    masks = [p['xor'] for p in pairs]
    centers = np.array([p['center'] for p in pairs])

    print(f"\n  Mask match at each pair offset:")
    for d in range(1, N_PAIRS):
        match = sum(1 for k in range(N_PAIRS)
                    if masks[k] == masks[(k + d) % N_PAIRS])
        if match > 2:
            print(f"    offset {d:2d}: {match}/32 mask matches")

    # Center distance at each offset
    print(f"\n  Mean center distance by pair offset (top 5 closest):")
    offset_dists = []
    for d in range(1, N_PAIRS):
        dists = [np.linalg.norm(centers[k] - centers[(k + d) % N_PAIRS])
                 for k in range(N_PAIRS)]
        offset_dists.append((d, np.mean(dists)))

    offset_dists.sort(key=lambda x: x[1])
    for d, mean_d in offset_dists[:10]:
        print(f"    offset {d:2d}: mean distance={mean_d:.3f}")

    # Mutual information between pair flip counts at each offset
    print(f"\n  Flip count correlation by pair offset:")
    flips = np.array([p['n_flips'] for p in pairs], dtype=float)
    for d in range(1, N_PAIRS):
        shifted = np.array([flips[(k + d) % N_PAIRS] for k in range(N_PAIRS)])
        corr = np.corrcoef(flips, shifted)[0, 1]
        if abs(corr) > 0.25:
            print(f"    offset {d:2d}: r={corr:+.3f}")


# ─── 5. Pair Sequence as Path Through Pair Space ─────────────────────────────

def analyze_pair_path():
    print("\n" + "=" * 70)
    print("5. PAIR SEQUENCE STRUCTURE")
    print("=" * 70)

    # Each pair can be described by its mask (which lines flip)
    # The sequence of masks tells us how the "type of change" evolves

    masks = [p['xor'] for p in pairs]
    flips = [p['n_flips'] for p in pairs]

    # Transition between consecutive mask types
    print(f"\n  Flip count sequence:")
    print(f"    {' '.join(str(f) for f in flips)}")
    print(f"\n  Consecutive flip count changes:")
    changes = [flips[k + 1] - flips[k] for k in range(N_PAIRS - 1)]
    print(f"    {' '.join(f'{c:+d}' for c in changes)}")
    print(f"    Mean absolute change: {np.mean(np.abs(changes)):.2f}")

    # Mask Hamming distance between consecutive pairs
    mask_dists = []
    for k in range(N_PAIRS - 1):
        d = sum(masks[k][i] != masks[k + 1][i] for i in range(DIMS))
        mask_dists.append(d)
    print(f"\n  Mask Hamming distance (consecutive pairs):")
    print(f"    Distribution: {Counter(mask_dists)}")
    print(f"    Mean: {np.mean(mask_dists):.2f}")

    # Do masks tend to share lines? (overlap between consecutive pair masks)
    print(f"\n  Line overlap between consecutive pair masks:")
    overlaps = []
    for k in range(N_PAIRS - 1):
        shared = sum(masks[k][i] & masks[k + 1][i] for i in range(DIMS))
        union = sum(masks[k][i] | masks[k + 1][i] for i in range(DIMS))
        overlaps.append(shared / union if union > 0 else 0)
    print(f"    Mean Jaccard overlap: {np.mean(overlaps):.3f}")
    print(f"    (0 = no shared lines flip, 1 = identical masks)")

    # Monte Carlo: is mask sequence structure significant?
    print(f"\n  Monte Carlo: mask Hamming distance between consecutive pairs")
    actual_mean = np.mean(mask_dists)
    null_means = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(N_PAIRS)
        perm_masks = [masks[i] for i in perm]
        null_dists = [sum(perm_masks[k][i] != perm_masks[k + 1][i]
                         for i in range(DIMS))
                      for k in range(N_PAIRS - 1)]
        null_means.append(np.mean(null_dists))
    null_means = np.array(null_means)
    p_low = np.mean(null_means <= actual_mean)
    p_high = np.mean(null_means >= actual_mean)
    print(f"    Actual mean: {actual_mean:.3f}")
    print(f"    Random mean: {np.mean(null_means):.3f} ± {np.std(null_means):.3f}")
    print(f"    p(≤actual): {p_low:.4f}, p(≥actual): {p_high:.4f}")


# ─── 6. Pair Symmetry ────────────────────────────────────────────────────────

def analyze_pair_symmetry():
    print("\n" + "=" * 70)
    print("6. PAIR-LEVEL SYMMETRY")
    print("=" * 70)

    # Upper Canon (pairs 1-15) vs Lower Canon (pairs 16-32)
    # Actually: hex 1-30 = pairs 1-15, hex 31-64 = pairs 16-32
    upper = pairs[:15]
    lower = pairs[15:]

    print(f"\n  Upper Canon (pairs 1-15) vs Lower Canon (pairs 16-32):")
    upper_flips = Counter(p['n_flips'] for p in upper)
    lower_flips = Counter(p['n_flips'] for p in lower)
    print(f"    Upper flip distribution: {dict(sorted(upper_flips.items()))}")
    print(f"    Lower flip distribution: {dict(sorted(lower_flips.items()))}")

    upper_masks = Counter(p['xor'] for p in upper)
    lower_masks = Counter(p['xor'] for p in lower)
    shared_masks = set(upper_masks.keys()) & set(lower_masks.keys())
    print(f"    Shared masks: {len(shared_masks)}")
    print(f"    Upper-only masks: {len(upper_masks) - len(shared_masks)}")
    print(f"    Lower-only masks: {len(lower_masks) - len(shared_masks)}")

    # First half vs second half (pairs 1-16 vs 17-32)
    first = pairs[:16]
    second = pairs[16:]
    print(f"\n  First half (pairs 1-16) vs second half (pairs 17-32):")
    f_flips = Counter(p['n_flips'] for p in first)
    s_flips = Counter(p['n_flips'] for p in second)
    print(f"    First flip distribution: {dict(sorted(f_flips.items()))}")
    print(f"    Second flip distribution: {dict(sorted(s_flips.items()))}")

    # Pair k vs pair (32-k): mirror symmetry?
    print(f"\n  Mirror symmetry (pair k vs pair 33-k):")
    mask_matches = 0
    flip_matches = 0
    for k in range(N_PAIRS // 2):
        mirror = N_PAIRS - 1 - k
        if pairs[k]['xor'] == pairs[mirror]['xor']:
            mask_matches += 1
        if pairs[k]['n_flips'] == pairs[mirror]['n_flips']:
            flip_matches += 1
    print(f"    Mask matches: {mask_matches}/16")
    print(f"    Flip count matches: {flip_matches}/16")

    # Monte Carlo for mirror flip matches
    null_matches = []
    for _ in range(N_TRIALS):
        perm_flips = RNG.permutation([p['n_flips'] for p in pairs])
        m = sum(1 for k in range(N_PAIRS // 2)
                if perm_flips[k] == perm_flips[N_PAIRS - 1 - k])
        null_matches.append(m)
    null_matches = np.array(null_matches)
    p = np.mean(null_matches >= flip_matches)
    print(f"    MC flip matches: mean={np.mean(null_matches):.1f}, p={p:.4f}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("PAIR-LEVEL ANALYSIS OF THE KING WEN SEQUENCE")
    print("=" * 70)

    analyze_masks()
    analyze_centers()
    bridges = analyze_bridges()
    analyze_pair_offsets()
    analyze_pair_path()
    analyze_pair_symmetry()

    print("\n" + "=" * 70)
    print("PAIR ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
