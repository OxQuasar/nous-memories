#!/usr/bin/env python3
"""Q1 Phase 4: King Wen path through the thematic manifold.

Traces the KW ordering through residual embedding space (algebra regressed out).
Tests whether the authored sequence has non-random geometric properties:
  1. Bridge smoothness — are between-pair transitions shorter than chance?
  2. Path shape — directional drift / oscillation in PC space
  3. Complement placement — do thematic neighbors land near each other?
  4. 上經/下經 split — is the two-book division thematically real?
"""

import numpy as np
import json
import sys
from pathlib import Path
from collections import defaultdict

from scipy.spatial.distance import cosine as cos_dist
from scipy.stats import pearsonr, spearmanr, linregress
from sklearn.decomposition import PCA

# Reuse phase1 infrastructure
from phase1_residual_structure import load_data, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
OUT_DIR = Path(__file__).resolve().parent
N_PERM = 10_000
RNG = np.random.default_rng(42)


# ═══════════════════════════════════════════════════════
# Data setup
# ═══════════════════════════════════════════════════════

def setup():
    """Load residuals, build hex centroids, KW ordering, pairs."""
    yaoci, meta, atlas = load_data()
    X, _ = build_design_matrix(meta)
    residual, r2, _ = extract_residuals(yaoci, X)
    print(f"Residual R² removed: {r2:.4f}, residual shape: {residual.shape}")

    # 64 hex centroids in residual space
    centroids = np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(64)])

    # KW ordering
    kw_map = {int(k): v['kw_number'] for k, v in atlas.items()
              if k.isdigit() and int(k) < 64}
    kw_order = sorted(range(64), key=lambda h: kw_map[h])

    # 32 pairs
    pairs = [(kw_order[2*i], kw_order[2*i+1]) for i in range(32)]

    # Classify pairs
    pair_type = []  # 'palindrome', 'anti-palindrome', 'reversal'
    for h1, h2 in pairs:
        a1 = atlas[str(h1)]
        if a1['reverse'] == h1 and a1['complement'] == h2:
            pair_type.append('palindrome')
        elif a1['reverse'] == a1['complement'] and h2 == a1['reverse']:
            pair_type.append('anti-palindrome')
        else:
            pair_type.append('reversal')

    counts = defaultdict(int)
    for t in pair_type:
        counts[t] += 1
    print(f"Pair types: {dict(counts)}")

    # Pair centroids
    pair_centroids = np.array([(centroids[h1] + centroids[h2]) / 2
                                for h1, h2 in pairs])

    # Element pairs per hex
    def elem_pair(h):
        a = atlas[str(h)]
        return (a['lower_trigram']['element'], a['upper_trigram']['element'])

    # Complement map: for pure reversal pairs, find complement pair index
    hex_to_pair = {}
    for i, (h1, h2) in enumerate(pairs):
        hex_to_pair[h1] = i
        hex_to_pair[h2] = i

    complement_pair = {}  # pair_idx → complement_pair_idx (for reversal pairs)
    for i, (h1, h2) in enumerate(pairs):
        if pair_type[i] == 'reversal':
            comp_h = atlas[str(h1)]['complement']
            complement_pair[i] = hex_to_pair[comp_h]

    return {
        'centroids': centroids,
        'pairs': pairs,
        'pair_type': pair_type,
        'pair_centroids': pair_centroids,
        'elem_pair': elem_pair,
        'complement_pair': complement_pair,
        'atlas': atlas,
        'kw_map': kw_map,
        'hex_to_pair': hex_to_pair,
    }


# ═══════════════════════════════════════════════════════
# Null model: permutations of interior pairs
# ═══════════════════════════════════════════════════════

def generate_null_perms(data, n_perm=N_PERM):
    """Permute 30 interior pairs (fix pair 0 and 31).

    Rejection sampling: reject if any bridge violates anti-clustering.
    """
    pairs = data['pairs']
    elem_pair = data['elem_pair']
    interior = list(range(1, 31))

    # Precompute element pairs for tail (h2) and head (h1) of each pair
    tail_elem = [elem_pair(pairs[i][1]) for i in range(32)]
    head_elem = [elem_pair(pairs[i][0]) for i in range(32)]

    perms = []
    n_tried = 0
    while len(perms) < n_perm:
        perm = [0] + list(RNG.permutation(interior)) + [31]
        # Check anti-clustering
        ok = True
        for j in range(31):
            if tail_elem[perm[j]] == head_elem[perm[j+1]]:
                ok = False
                break
        if ok:
            perms.append(perm)
        n_tried += 1

    accept_rate = len(perms) / n_tried
    print(f"Null model: {n_perm} permutations, acceptance rate: {accept_rate:.3f} ({n_tried} tried)")
    return perms


# ═══════════════════════════════════════════════════════
# Test 1: Bridge Smoothness
# ═══════════════════════════════════════════════════════

def compute_bridges(perm, data):
    """Compute 31 bridge distances for a given pair ordering."""
    centroids = data['centroids']
    pairs = data['pairs']
    bridges = []
    for j in range(31):
        h2_prev = pairs[perm[j]][1]
        h1_next = pairs[perm[j+1]][0]
        bridges.append(cos_dist(centroids[h2_prev], centroids[h1_next]))
    return np.array(bridges)


def test_bridge_smoothness(data, null_perms):
    """Test 1: Bridge smoothness."""
    print("\n" + "=" * 70)
    print("TEST 1: BRIDGE SMOOTHNESS")
    print("=" * 70)

    kw_perm = list(range(32))
    kw_bridges = compute_bridges(kw_perm, data)

    # KW metrics
    kw_metrics = {
        'mean': np.mean(kw_bridges),
        'median': np.median(kw_bridges),
        'max': np.max(kw_bridges),
        'std': np.std(kw_bridges),
        'lag1_autocorr': np.corrcoef(kw_bridges[:-1], kw_bridges[1:])[0, 1],
    }

    # Null metrics
    null_metrics = {k: [] for k in kw_metrics}
    for perm in null_perms:
        bridges = compute_bridges(perm, data)
        null_metrics['mean'].append(np.mean(bridges))
        null_metrics['median'].append(np.median(bridges))
        null_metrics['max'].append(np.max(bridges))
        null_metrics['std'].append(np.std(bridges))
        null_metrics['lag1_autocorr'].append(
            np.corrcoef(bridges[:-1], bridges[1:])[0, 1])

    for k in null_metrics:
        null_metrics[k] = np.array(null_metrics[k])

    results = {}
    print(f"\n{'Metric':<18} {'KW':>10} {'Null μ±σ':>16} {'%ile':>8} {'z':>8}")
    print("-" * 62)
    for name in kw_metrics:
        kw_val = kw_metrics[name]
        null_arr = null_metrics[name]
        null_mu = np.mean(null_arr)
        null_std = np.std(null_arr)
        percentile = np.mean(null_arr <= kw_val) * 100
        z = (kw_val - null_mu) / null_std if null_std > 0 else 0
        results[name] = {
            'kw': kw_val, 'null_mu': null_mu, 'null_std': null_std,
            'percentile': percentile, 'z': z,
        }
        print(f"{name:<18} {kw_val:>10.5f} {null_mu:>8.5f}±{null_std:.5f} "
              f"{percentile:>7.1f}% {z:>+7.2f}")

    print(f"\nKW bridge distances: min={kw_bridges.min():.5f}, "
          f"max={kw_bridges.max():.5f}")
    print(f"Individual bridges (sorted):")
    for i, b in enumerate(np.sort(kw_bridges)):
        print(f"  {i+1:2d}: {b:.5f}")

    return results, kw_bridges


# ═══════════════════════════════════════════════════════
# Test 2: Path Shape
# ═══════════════════════════════════════════════════════

def test_path_shape(data, null_perms):
    """Test 2: PCA trajectory — drift and oscillation."""
    print("\n" + "=" * 70)
    print("TEST 2: PATH SHAPE (PCA TRAJECTORY)")
    print("=" * 70)

    pair_centroids = data['pair_centroids']

    # PCA on 32 pair centroids
    pca = PCA(n_components=5)
    coords = pca.fit_transform(pair_centroids)  # (32, 5)
    var_exp = pca.explained_variance_ratio_
    print(f"\nPCA variance explained: {[f'{v:.3f}' for v in var_exp]}")
    print(f"Cumulative: {np.cumsum(var_exp)[-1]:.3f}")

    # KW trajectory: positions 0..31
    positions = np.arange(32)

    def path_metrics(perm):
        """Compute drift and spectral features for a permutation."""
        traj = coords[perm]  # reorder pair centroids
        r2_sum = 0
        fft_amps = []
        for pc in range(5):
            y = traj[:, pc]
            slope, intercept, r, p, se = linregress(positions, y)
            r2_sum += r**2
            # FFT on detrended signal
            detrended = y - (slope * positions + intercept)
            fft = np.fft.rfft(detrended)
            amplitudes = np.abs(fft[1:])  # skip DC
            fft_amps.append(amplitudes)
        # Max spectral amplitude across PCs
        all_amps = np.array(fft_amps)
        max_amp = all_amps.max()
        # Dominant frequency per PC
        dom_freqs = [np.argmax(fa) + 1 for fa in fft_amps]
        return r2_sum, max_amp, dom_freqs

    # KW path
    kw_r2, kw_max_amp, kw_dom_freqs = path_metrics(list(range(32)))

    # Per-PC details for KW
    print(f"\nKW path per-PC regression:")
    print(f"  {'PC':<5} {'Slope':>10} {'R²':>8} {'p':>10} {'DomFreq':>8} {'DomAmp':>10}")
    print(f"  {'-'*53}")
    kw_traj = coords  # KW order is identity
    for pc in range(5):
        y = kw_traj[:, pc]
        slope, intercept, r, p, se = linregress(positions, y)
        detrended = y - (slope * positions + intercept)
        fft = np.fft.rfft(detrended)
        amps = np.abs(fft[1:])
        dom_freq = np.argmax(amps) + 1
        dom_amp = amps[dom_freq - 1]
        print(f"  PC{pc:<3} {slope:>10.5f} {r**2:>8.4f} {p:>10.4f} "
              f"{dom_freq:>8} {dom_amp:>10.4f}")

    # Null distribution
    null_r2 = []
    null_max_amp = []
    for perm in null_perms:
        r2, max_amp, _ = path_metrics(perm)
        null_r2.append(r2)
        null_max_amp.append(max_amp)
    null_r2 = np.array(null_r2)
    null_max_amp = np.array(null_max_amp)

    # Report
    for name, kw_val, null_arr in [
        ('Total R² drift', kw_r2, null_r2),
        ('Max spectral amp', kw_max_amp, null_max_amp),
    ]:
        mu, sigma = np.mean(null_arr), np.std(null_arr)
        pct = np.mean(null_arr <= kw_val) * 100
        z = (kw_val - mu) / sigma if sigma > 0 else 0
        print(f"\n{name}: KW={kw_val:.5f}, null={mu:.5f}±{sigma:.5f}, "
              f"percentile={pct:.1f}%, z={z:+.2f}")

    return {
        'kw_r2': kw_r2, 'kw_max_amp': kw_max_amp,
        'kw_dom_freqs': kw_dom_freqs,
        'null_r2_mu': np.mean(null_r2), 'null_r2_std': np.std(null_r2),
        'null_r2_pct': np.mean(null_r2 <= kw_r2) * 100,
        'null_amp_mu': np.mean(null_max_amp), 'null_amp_std': np.std(null_max_amp),
        'null_amp_pct': np.mean(null_max_amp <= kw_max_amp) * 100,
        'var_explained': var_exp.tolist(),
    }


# ═══════════════════════════════════════════════════════
# Test 3: Complement Placement
# ═══════════════════════════════════════════════════════

def test_complement_placement(data, null_perms):
    """Test 3: Do complement pairs land near each other in KW sequence?"""
    print("\n" + "=" * 70)
    print("TEST 3: COMPLEMENT PLACEMENT")
    print("=" * 70)

    pairs = data['pairs']
    pair_type = data['pair_type']
    pair_centroids = data['pair_centroids']
    complement_pair = data['complement_pair']

    # 24 reversal pairs with complement mapping
    reversal_indices = [i for i in range(32) if pair_type[i] == 'reversal']
    assert len(reversal_indices) == 24

    # (a) Thematic distance between pair and its complement pair
    # (b) KW sequence distance
    thematic_dists = []
    sequence_dists = []
    for i in reversal_indices:
        j = complement_pair[i]
        td = cos_dist(pair_centroids[i], pair_centroids[j])
        sd = abs(i - j)
        thematic_dists.append(td)
        sequence_dists.append(sd)

    thematic_dists = np.array(thematic_dists)
    sequence_dists = np.array(sequence_dists)

    # Correlations
    r_pearson, p_pearson = pearsonr(thematic_dists, sequence_dists)
    r_spearman, p_spearman = spearmanr(thematic_dists, sequence_dists)

    print(f"\n24 reversal pairs — complement thematic vs sequence distance:")
    print(f"  Pearson  r={r_pearson:+.4f}, p={p_pearson:.4f}")
    print(f"  Spearman ρ={r_spearman:+.4f}, p={p_spearman:.4f}")

    # Mean complement thematic distance for KW
    kw_mean_td = np.mean(thematic_dists)
    print(f"\n  KW mean complement thematic distance: {kw_mean_td:.5f}")

    # Permutation test: under null orderings, what's the mean complement thematic distance?
    # Under permutation, pair_centroids don't change, but positions do.
    # Complement relationships are structural — they don't change.
    # The thematic distance between complement pairs is FIXED regardless of ordering.
    # What changes is the sequence distance.
    # So the permutation test for thematic distance doesn't apply here.
    #
    # Instead: test the correlation between thematic and sequence distance under null.
    null_pearson = []
    null_spearman = []
    for perm in null_perms:
        # Under this permutation, the sequence position of pair i is perm.index(i)
        inv_perm = [0] * 32
        for pos, pair_idx in enumerate(perm):
            inv_perm[pair_idx] = pos

        null_seq_dists = []
        for i in reversal_indices:
            j = complement_pair[i]
            null_seq_dists.append(abs(inv_perm[i] - inv_perm[j]))
        null_seq_dists = np.array(null_seq_dists)

        rp, _ = pearsonr(thematic_dists, null_seq_dists)
        rs, _ = spearmanr(thematic_dists, null_seq_dists)
        null_pearson.append(rp)
        null_spearman.append(rs)

    null_pearson = np.array(null_pearson)
    null_spearman = np.array(null_spearman)

    for name, kw_val, null_arr in [
        ('Pearson', r_pearson, null_pearson),
        ('Spearman', r_spearman, null_spearman),
    ]:
        mu, sigma = np.mean(null_arr), np.std(null_arr)
        pct = np.mean(null_arr <= kw_val) * 100
        z = (kw_val - mu) / sigma if sigma > 0 else 0
        print(f"  {name}: KW={kw_val:+.4f}, null={mu:+.4f}±{sigma:.4f}, "
              f"pct={pct:.1f}%, z={z:+.2f}")

    # Also report mean sequence distance for complement pairs
    kw_mean_sd = np.mean(sequence_dists)
    null_mean_sd = []
    for perm in null_perms:
        inv_perm = [0] * 32
        for pos, pair_idx in enumerate(perm):
            inv_perm[pair_idx] = pos
        sds = [abs(inv_perm[i] - inv_perm[complement_pair[i]]) for i in reversal_indices]
        null_mean_sd.append(np.mean(sds))
    null_mean_sd = np.array(null_mean_sd)
    mu_sd, std_sd = np.mean(null_mean_sd), np.std(null_mean_sd)
    pct_sd = np.mean(null_mean_sd <= kw_mean_sd) * 100
    z_sd = (kw_mean_sd - mu_sd) / std_sd if std_sd > 0 else 0
    print(f"\n  Mean complement sequence distance: KW={kw_mean_sd:.2f}, "
          f"null={mu_sd:.2f}±{std_sd:.2f}, pct={pct_sd:.1f}%, z={z_sd:+.2f}")

    # Complement-within-pair: 4 palindrome + 4 anti-palindrome
    print(f"\n  Complement-within-pair (8 pairs):")
    print(f"  {'Pair':>5} {'Type':<16} {'Within-pair dist':>16} {'Hexagrams'}")
    print(f"  {'-'*65}")
    within_dists = []
    for i in range(32):
        if pair_type[i] in ('palindrome', 'anti-palindrome'):
            h1, h2 = pairs[i]
            d = cos_dist(data['centroids'][h1], data['centroids'][h2])
            within_dists.append(d)
            a1 = data['atlas'][str(h1)]
            a2 = data['atlas'][str(h2)]
            print(f"  {i:>5} {pair_type[i]:<16} {d:>16.5f} "
                  f"{a1['kw_name']}↔{a2['kw_name']}")
    print(f"  Mean within-pair complement distance: {np.mean(within_dists):.5f}")

    # Compare to all within-pair distances for reversal pairs
    rev_within = []
    for i in reversal_indices:
        h1, h2 = pairs[i]
        rev_within.append(cos_dist(data['centroids'][h1], data['centroids'][h2]))
    print(f"  Mean within-pair reversal distance:   {np.mean(rev_within):.5f}")

    return {
        'pearson': r_pearson, 'p_pearson': p_pearson,
        'spearman': r_spearman, 'p_spearman': p_spearman,
        'kw_mean_thematic': float(kw_mean_td),
        'kw_mean_seq_dist': float(kw_mean_sd),
        'null_seq_dist_mu': float(mu_sd),
        'null_pearson_pct': float(np.mean(null_pearson <= r_pearson) * 100),
        'null_spearman_pct': float(np.mean(null_spearman <= r_spearman) * 100),
    }


# ═══════════════════════════════════════════════════════
# Test 4: 上經/下經 Split
# ═══════════════════════════════════════════════════════

def test_jing_split(data, null_perms):
    """Test 4: Is the 上經/下經 split thematically real?"""
    print("\n" + "=" * 70)
    print("TEST 4: 上經/下經 SPLIT")
    print("=" * 70)

    pairs = data['pairs']
    pair_type = data['pair_type']
    pair_centroids = data['pair_centroids']
    kw_map = data['kw_map']
    complement_pair = data['complement_pair']

    # 上經: pairs where both hexagrams have kw_number ≤ 30 (pairs 0..14)
    # 下經: remaining (pairs 15..31)
    upper_idx = list(range(15))
    lower_idx = list(range(15, 32))

    # Verify
    for i in upper_idx:
        h1, h2 = pairs[i]
        assert kw_map[h1] <= 30 and kw_map[h2] <= 30, f"Pair {i}: kw={kw_map[h1]},{kw_map[h2]}"
    for i in lower_idx:
        h1, h2 = pairs[i]
        assert kw_map[h1] > 30 or kw_map[h2] > 30, f"Pair {i}: kw={kw_map[h1]},{kw_map[h2]}"

    print(f"  上經: {len(upper_idx)} pairs (kw 1-30)")
    print(f"  下經: {len(lower_idx)} pairs (kw 31-64)")

    # Pairwise cosine distances between pair centroids
    from scipy.spatial.distance import cdist
    D = cdist(pair_centroids, pair_centroids, metric='cosine')

    def split_distances(upper, lower):
        """Mean within-upper, within-lower, cross distances."""
        within_upper = []
        for i in range(len(upper)):
            for j in range(i+1, len(upper)):
                within_upper.append(D[upper[i], upper[j]])
        within_lower = []
        for i in range(len(lower)):
            for j in range(i+1, len(lower)):
                within_lower.append(D[lower[i], lower[j]])
        cross = []
        for i in upper:
            for j in lower:
                cross.append(D[i, j])
        return np.mean(within_upper), np.mean(within_lower), np.mean(cross)

    kw_wu, kw_wl, kw_cross = split_distances(upper_idx, lower_idx)
    print(f"\n  Within-上經 mean distance:  {kw_wu:.5f}")
    print(f"  Within-下經 mean distance:  {kw_wl:.5f}")
    print(f"  Cross-split mean distance:  {kw_cross:.5f}")
    print(f"  Cross − mean(within):       {kw_cross - (kw_wu + kw_wl)/2:.5f}")

    # Permutation test: split quality = cross - mean(within)
    kw_split_quality = kw_cross - (kw_wu + kw_wl) / 2

    null_sq = []
    null_cross = []
    for perm in null_perms:
        # Under this perm, upper = first 15 of perm, lower = last 17
        u = perm[:15]
        l = perm[15:]
        wu, wl, cr = split_distances(u, l)
        null_sq.append(cr - (wu + wl) / 2)
        null_cross.append(cr)
    null_sq = np.array(null_sq)
    null_cross = np.array(null_cross)

    mu_sq, std_sq = np.mean(null_sq), np.std(null_sq)
    pct_sq = np.mean(null_sq <= kw_split_quality) * 100
    z_sq = (kw_split_quality - mu_sq) / std_sq if std_sq > 0 else 0
    print(f"\n  Split quality (cross−within): KW={kw_split_quality:.5f}, "
          f"null={mu_sq:.5f}±{std_sq:.5f}, pct={pct_sq:.1f}%, z={z_sq:+.2f}")

    # Complement pairs spanning the split
    reversal_indices = [i for i in range(32) if pair_type[i] == 'reversal']
    upper_set = set(upper_idx)
    lower_set = set(lower_idx)

    kw_cross_comps = 0
    for i in reversal_indices:
        j = complement_pair[i]
        if (i in upper_set) != (j in upper_set):
            kw_cross_comps += 1
    # Each cross-complement is counted twice (i→j and j→i within reversal_indices)
    kw_cross_comps //= 2
    # Actually, not exactly. complement_pair maps i → j. If i is reversal, j might not be.
    # Let's be more careful: count unique unordered pairs
    cross_comp_pairs = set()
    for i in reversal_indices:
        j = complement_pair[i]
        pair_key = (min(i, j), max(i, j))
        if (i in upper_set) != (j in upper_set):
            cross_comp_pairs.add(pair_key)
    kw_cross_comps = len(cross_comp_pairs)

    total_comp_pairs = len(set((min(i, complement_pair[i]), max(i, complement_pair[i]))
                               for i in reversal_indices))

    print(f"\n  Complement pairs spanning split: {kw_cross_comps}/{total_comp_pairs}")

    # Null: how many complement pairs span the 15/17 split?
    null_cc = []
    for perm in null_perms:
        u_set = set(perm[:15])
        cc = 0
        seen = set()
        for i in reversal_indices:
            j = complement_pair[i]
            key = (min(i, j), max(i, j))
            if key not in seen:
                seen.add(key)
                if (i in u_set) != (j in u_set):
                    cc += 1
        null_cc.append(cc)
    null_cc = np.array(null_cc)

    mu_cc, std_cc = np.mean(null_cc), np.std(null_cc)
    pct_cc = np.mean(null_cc <= kw_cross_comps) * 100
    z_cc = (kw_cross_comps - mu_cc) / std_cc if std_cc > 0 else 0
    print(f"  Cross-split complements: KW={kw_cross_comps}, "
          f"null={mu_cc:.2f}±{std_cc:.2f}, pct={pct_cc:.1f}%, z={z_cc:+.2f}")

    return {
        'within_upper': kw_wu, 'within_lower': kw_wl, 'cross': kw_cross,
        'split_quality': kw_split_quality, 'split_quality_pct': pct_sq,
        'split_quality_z': z_sq,
        'cross_complements': kw_cross_comps, 'total_comp_pairs': total_comp_pairs,
        'cross_comp_pct': pct_cc, 'cross_comp_z': z_cc,
    }


# ═══════════════════════════════════════════════════════
# Report
# ═══════════════════════════════════════════════════════

def write_report(r1, r2, r3, r4):
    """Write markdown summary."""
    lines = [
        "# Phase 4: King Wen Path Through the Thematic Manifold",
        "",
        f"Null model: {N_PERM} permutations of 30 interior pairs "
        "(pair 0=乾坤, pair 31=既濟未濟 fixed), anti-clustering enforced.",
        "",
        "## Test 1: Bridge Smoothness",
        "",
        "31 between-pair bridge distances in residual space (cosine).",
        "",
        "| Metric | KW | Null μ±σ | %ile | z |",
        "|--------|---:|--------:|-----:|--:|",
    ]
    for name in ['mean', 'median', 'max', 'std', 'lag1_autocorr']:
        r = r1[name]
        lines.append(f"| {name} | {r['kw']:.5f} | {r['null_mu']:.5f}±{r['null_std']:.5f} "
                      f"| {r['percentile']:.1f}% | {r['z']:+.2f} |")

    lines += [
        "",
        "## Test 2: Path Shape",
        "",
        f"PCA on 32 pair centroids. Variance explained: "
        f"{', '.join(f'{v:.3f}' for v in r2['var_explained'])}",
        "",
        f"- **Total R² drift**: KW={r2['kw_r2']:.5f}, "
        f"null={r2['null_r2_mu']:.5f}±{r2['null_r2_std']:.5f}, "
        f"pct={r2['null_r2_pct']:.1f}%",
        f"- **Max spectral amp**: KW={r2['kw_max_amp']:.5f}, "
        f"null={r2['null_amp_mu']:.5f}±{r2['null_amp_std']:.5f}, "
        f"pct={r2['null_amp_pct']:.1f}%",
        f"- Dominant frequencies: {r2['kw_dom_freqs']}",
        "",
        "## Test 3: Complement Placement",
        "",
        f"24 reversal pairs with complement mapping.",
        "",
        f"- Thematic × sequence distance: Pearson r={r3['pearson']:+.4f} "
        f"(p={r3['p_pearson']:.4f}), Spearman ρ={r3['spearman']:+.4f} "
        f"(p={r3['p_spearman']:.4f})",
        f"- Pearson percentile vs null: {r3['null_pearson_pct']:.1f}%",
        f"- Spearman percentile vs null: {r3['null_spearman_pct']:.1f}%",
        f"- KW mean complement sequence distance: {r3['kw_mean_seq_dist']:.2f} "
        f"(null: {r3['null_seq_dist_mu']:.2f})",
        "",
        "## Test 4: 上經/下經 Split",
        "",
        f"- Within-上經: {r4['within_upper']:.5f}",
        f"- Within-下經: {r4['within_lower']:.5f}",
        f"- Cross-split: {r4['cross']:.5f}",
        f"- Split quality: {r4['split_quality']:.5f}, "
        f"pct={r4['split_quality_pct']:.1f}%, z={r4['split_quality_z']:+.2f}",
        f"- Cross-split complements: {r4['cross_complements']}/{r4['total_comp_pairs']}, "
        f"pct={r4['cross_comp_pct']:.1f}%, z={r4['cross_comp_z']:+.2f}",
        "",
    ]

    out_path = OUT_DIR / "phase4_kw_path_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nReport saved to {out_path}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 4: King Wen Path Through the Thematic Manifold")
    print("=" * 70)

    data = setup()
    null_perms = generate_null_perms(data)

    r1, kw_bridges = test_bridge_smoothness(data, null_perms)
    r2 = test_path_shape(data, null_perms)
    r3 = test_complement_placement(data, null_perms)
    r4 = test_jing_split(data, null_perms)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
Bridge smoothness:
  Mean bridge: KW={r1['mean']['kw']:.5f} vs null {r1['mean']['null_mu']:.5f}±{r1['mean']['null_std']:.5f} ({r1['mean']['percentile']:.1f}%ile)
  Lag-1 autocorr: KW={r1['lag1_autocorr']['kw']:.4f} ({r1['lag1_autocorr']['percentile']:.1f}%ile)

Path shape:
  Directional drift R²: KW={r2['kw_r2']:.5f} ({r2['null_r2_pct']:.1f}%ile)
  Max spectral amp: KW={r2['kw_max_amp']:.5f} ({r2['null_amp_pct']:.1f}%ile)

Complement placement:
  Pearson(thematic, sequence): {r3['pearson']:+.4f} (p={r3['p_pearson']:.4f}, null pct={r3['null_pearson_pct']:.1f}%)
  Spearman: {r3['spearman']:+.4f} (p={r3['p_spearman']:.4f}, null pct={r3['null_spearman_pct']:.1f}%)

上經/下經 split:
  Split quality z={r4['split_quality_z']:+.2f} ({r4['split_quality_pct']:.1f}%ile)
  Cross-split complements: {r4['cross_complements']}/{r4['total_comp_pairs']} (z={r4['cross_comp_z']:+.2f})
""")

    write_report(r1, r2, r3, r4)


if __name__ == '__main__':
    main()
