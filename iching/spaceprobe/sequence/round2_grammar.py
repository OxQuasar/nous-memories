"""
Round 2: Testing whether the kernel sequence grammar is real.

Tests:
1. MI null distribution — is MI elevated just because f1 is high?
2. Second-order kernels (transition deltas in Z₂³)
3. Coset structure of the running-product path
4. Trigram-pair structure of the sequence
5. Bias-corrected MI estimate + shuffle null
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
from sequence import KING_WEN, TRIGRAMS, lower_trigram, upper_trigram, trigram_name

import numpy as np
from collections import Counter

# ─── Constants & utilities (from round1) ─────────────────────────────────────

HEX_BITS = [h[2] for h in KING_WEN]
PAIRS = [(HEX_BITS[2*k], HEX_BITS[2*k+1]) for k in range(32)]

KERNEL_NAMES = {
    (0,0,0): "id",  (1,0,0): "O",   (0,1,0): "M",   (0,0,1): "I",
    (1,1,0): "OM",  (1,0,1): "OI",  (0,1,1): "MI",  (1,1,1): "OMI",
}
NAME_ORDER = ["id", "O", "M", "I", "OM", "OI", "MI", "OMI"]

def xor6(a, b):
    return tuple(int(a[i]) ^ int(b[i]) for i in range(6))

def kernel_bits(mask6):
    return (mask6[5], mask6[4], mask6[3])

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def hamming3(a, b):
    return sum(x != y for x, y in zip(a, b))

def compute_kernels(ordered_pairs):
    """31 kernel 3-tuples from 32 ordered pairs."""
    kernels = []
    for k in range(len(ordered_pairs) - 1):
        mask = xor6(ordered_pairs[k][1], ordered_pairs[k+1][0])
        kernels.append(kernel_bits(mask))
    return kernels

def compute_mi(kernels):
    """Mutual information I(k_n; k_{n+1}) from a kernel sequence.
    Returns (H_k, H_cond, MI)."""
    n_trans = len(kernels) - 1
    if n_trans == 0:
        return 0.0, 0.0, 0.0

    # Encode to ints for speed
    ids = [k[0]*4 + k[1]*2 + k[2] for k in kernels]

    # Marginal from "from" states (first n_trans elements)
    from_counts = np.zeros(8, dtype=int)
    trans_matrix = np.zeros((8, 8), dtype=int)
    for i in range(n_trans):
        from_counts[ids[i]] += 1
        trans_matrix[ids[i]][ids[i+1]] += 1

    # H(k) from the "from" marginal
    p_from = from_counts / n_trans
    h_k = -sum(p * np.log2(p) for p in p_from if p > 0)

    # H(k_{n+1} | k_n)
    h_cond = 0.0
    for i in range(8):
        if from_counts[i] == 0:
            continue
        p_x = from_counts[i] / n_trans
        for j in range(8):
            if trans_matrix[i][j] == 0:
                continue
            p_y_given_x = trans_matrix[i][j] / from_counts[i]
            h_cond -= p_x * p_y_given_x * np.log2(p_y_given_x)

    return h_k, h_cond, h_k - h_cond

# ─── KW baseline ────────────────────────────────────────────────────────────

KW_KERNELS = compute_kernels(PAIRS)
KW_DISTS = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
KW_F1 = np.mean(KW_DISTS)
KW_H, KW_HCOND, KW_MI = compute_mi(KW_KERNELS)

print(f"KW baseline: f1={KW_F1:.4f}, H(k)={KW_H:.3f}, H(k|k_prev)={KW_HCOND:.3f}, MI={KW_MI:.3f}")

# ─── Precompute pair arrays for fast Monte Carlo ────────────────────────────

PAIR_A = np.array([[int(c) for c in PAIRS[k][0]] for k in range(32)], dtype=np.int8)
PAIR_B = np.array([[int(c) for c in PAIRS[k][1]] for k in range(32)], dtype=np.int8)

def random_trial(rng):
    """Generate one random trial. Returns (f1, mi, kernels_as_int_array)."""
    perm = rng.permutation(32)
    orient = rng.integers(0, 2, size=32)

    exits = np.empty((32, 6), dtype=np.int8)
    entries = np.empty((32, 6), dtype=np.int8)
    for k in range(32):
        pk = perm[k]
        if orient[k] == 0:
            entries[k] = PAIR_A[pk]
            exits[k] = PAIR_B[pk]
        else:
            entries[k] = PAIR_B[pk]
            exits[k] = PAIR_A[pk]

    masks = np.bitwise_xor(exits[:31], entries[1:32])
    kernels = masks[:, [5, 4, 3]]  # (31, 3)
    kernel_ids = kernels[:, 0] * 4 + kernels[:, 1] * 2 + kernels[:, 2]

    # f1
    diffs = np.bitwise_xor(kernels[:30], kernels[1:31])
    f1 = diffs.sum(axis=1).mean()

    # MI
    from_counts = np.zeros(8, dtype=int)
    trans = np.zeros((8, 8), dtype=int)
    for i in range(30):
        from_counts[kernel_ids[i]] += 1
        trans[kernel_ids[i]][kernel_ids[i+1]] += 1

    n_trans = 30
    p_from = from_counts / n_trans
    h_k = -sum(p * np.log2(p) for p in p_from if p > 0)

    h_cond = 0.0
    for i in range(8):
        if from_counts[i] == 0:
            continue
        p_x = from_counts[i] / n_trans
        for j in range(8):
            if trans[i][j] == 0:
                continue
            p_y_given_x = trans[i][j] / from_counts[i]
            h_cond -= p_x * p_y_given_x * np.log2(p_y_given_x)

    return f1, h_k - h_cond

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: MI NULL DISTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════════

def computation_1():
    print("\n" + "=" * 80)
    print("COMPUTATION 1: MI NULL DISTRIBUTION (1M random trials)")
    print("=" * 80)

    rng = np.random.default_rng(42)
    N = 1_000_000

    f1s = np.empty(N)
    mis = np.empty(N)

    for t in range(N):
        f1s[t], mis[t] = random_trial(rng)
        if (t + 1) % 200_000 == 0:
            print(f"  ... {t+1}/{N}")

    # Overall stats
    print(f"\n--- Overall distribution ---")
    print(f"  f1: mean={f1s.mean():.4f}, std={f1s.std():.4f}, min={f1s.min():.4f}, max={f1s.max():.4f}")
    print(f"  MI: mean={mis.mean():.4f}, std={mis.std():.4f}, min={mis.min():.4f}, max={mis.max():.4f}")
    print(f"  KW f1={KW_F1:.4f} (percentile: {(f1s <= KW_F1).mean()*100:.2f}%)")
    print(f"  KW MI={KW_MI:.4f} (percentile: {(mis <= KW_MI).mean()*100:.2f}%)")

    # Correlation
    corr = np.corrcoef(f1s, mis)[0, 1]
    print(f"\n--- Correlation ---")
    print(f"  Pearson r(f1, MI) = {corr:.4f}")

    # Binned: mean MI per f1 bin
    print(f"\n--- Mean MI per f1 bin ---")
    bin_edges = np.linspace(f1s.min(), f1s.max(), 21)
    print(f"  {'f1 range':>18} {'count':>8} {'mean MI':>9} {'std MI':>9}")
    for i in range(20):
        mask = (f1s >= bin_edges[i]) & (f1s < bin_edges[i+1])
        if i == 19:  # include right edge
            mask = (f1s >= bin_edges[i]) & (f1s <= bin_edges[i+1])
        n = mask.sum()
        if n > 0:
            print(f"  [{bin_edges[i]:.3f}, {bin_edges[i+1]:.3f}) {n:>8} {mis[mask].mean():>9.4f} {mis[mask].std():>9.4f}")

    # CRITICAL: conditional percentile at KW's f1 level
    print(f"\n--- Conditional analysis (f1 ≥ 1.70) ---")
    high_f1_mask = f1s >= 1.70
    n_high = high_f1_mask.sum()
    print(f"  Trials with f1 ≥ 1.70: {n_high} ({n_high/N*100:.2f}%)")

    if n_high > 0:
        mi_high = mis[high_f1_mask]
        print(f"  MI among high-f1 trials:")
        print(f"    Mean: {mi_high.mean():.4f}")
        print(f"    Std:  {mi_high.std():.4f}")
        print(f"    Min:  {mi_high.min():.4f}")
        print(f"    Max:  {mi_high.max():.4f}")
        print(f"    KW MI = {KW_MI:.4f}")
        print(f"    KW conditional percentile: {(mi_high <= KW_MI).mean()*100:.2f}%")

    # Also check f1 ≥ 1.60
    print(f"\n--- Conditional analysis (f1 ≥ 1.60) ---")
    mid_mask = f1s >= 1.60
    n_mid = mid_mask.sum()
    print(f"  Trials with f1 ≥ 1.60: {n_mid} ({n_mid/N*100:.2f}%)")
    if n_mid > 0:
        mi_mid = mis[mid_mask]
        print(f"  MI mean: {mi_mid.mean():.4f}, std: {mi_mid.std():.4f}")
        print(f"  KW MI conditional percentile: {(mi_mid <= KW_MI).mean()*100:.2f}%")

    return f1s, mis

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: SECOND-ORDER KERNELS (TRANSITION DELTAS)
# ═══════════════════════════════════════════════════════════════════════════════

def computation_2(f1s_from_mc, mis_from_mc):
    print("\n" + "=" * 80)
    print("COMPUTATION 2: SECOND-ORDER KERNELS (TRANSITION DELTAS)")
    print("=" * 80)

    # KW transition deltas
    deltas = [xor3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]

    print(f"\n--- KW transition delta sequence (30 deltas) ---")
    for i, d in enumerate(deltas):
        name = KERNEL_NAMES[d]
        prev_name = KERNEL_NAMES[KW_KERNELS[i]]
        next_name = KERNEL_NAMES[KW_KERNELS[i+1]]
        print(f"  δ{i+1:>2}: {name:>5}  ({prev_name:>5} → {next_name:<5})")

    # Frequency distribution
    delta_names = [KERNEL_NAMES[d] for d in deltas]
    freq = Counter(delta_names)

    print(f"\n--- Delta frequency distribution ---")
    for name in NAME_ORDER:
        count = freq.get(name, 0)
        bar = '█' * count
        print(f"  {name:>5}: {count:>2}  {bar}")

    # Note: delta = id means kernel repeat (distance 0)
    #        wt(delta) = consecutive distance
    print(f"\n  id (repeats): {freq.get('id', 0)}")
    absent = [n for n in NAME_ORDER if freq.get(n, 0) == 0]
    print(f"  Absent deltas: {absent if absent else 'none'}")

    # Entropy of delta distribution
    probs = np.array([freq.get(n, 0) for n in NAME_ORDER]) / 30
    probs_nz = probs[probs > 0]
    delta_entropy = -np.sum(probs_nz * np.log2(probs_nz))
    print(f"\n  Shannon entropy of deltas: {delta_entropy:.3f} bits (max 3.000)")
    print(f"  Normalized: {delta_entropy / 3:.3f}")

    # Third-order: consecutive delta distances
    delta_dists = [hamming3(deltas[i], deltas[i+1]) for i in range(29)]
    print(f"\n--- Third-order: consecutive delta distances ---")
    print(f"  Mean: {np.mean(delta_dists):.3f}")
    print(f"  Std:  {np.std(delta_dists):.3f}")
    print(f"  Distribution: {dict(sorted(Counter(delta_dists).items()))}")

    # Compare delta distribution to null model using existing MC data
    # We need to recompute deltas for random trials — run a smaller MC
    print(f"\n--- Delta statistics: null model (100,000 trials) ---")
    rng = np.random.default_rng(123)  # different seed to avoid correlation with comp1
    N_DELTA = 100_000

    delta_entropies = np.empty(N_DELTA)
    delta_id_counts = np.empty(N_DELTA, dtype=int)
    delta_mean_dists_3rd = np.empty(N_DELTA)

    # Per-delta-type counts for null
    delta_type_counts = np.zeros((N_DELTA, 8), dtype=int)

    for t in range(N_DELTA):
        perm = rng.permutation(32)
        orient = rng.integers(0, 2, size=32)

        exits = np.empty((32, 6), dtype=np.int8)
        entries = np.empty((32, 6), dtype=np.int8)
        for k in range(32):
            pk = perm[k]
            if orient[k] == 0:
                entries[k] = PAIR_A[pk]
                exits[k] = PAIR_B[pk]
            else:
                entries[k] = PAIR_B[pk]
                exits[k] = PAIR_A[pk]

        masks = np.bitwise_xor(exits[:31], entries[1:32])
        kerns = masks[:, [5, 4, 3]]  # (31, 3)

        # Deltas
        d = np.bitwise_xor(kerns[:30], kerns[1:31])  # (30, 3)
        d_ids = d[:, 0] * 4 + d[:, 1] * 2 + d[:, 2]

        # Counts per type
        for j in range(8):
            delta_type_counts[t, j] = (d_ids == j).sum()

        delta_id_counts[t] = (d_ids == 0).sum()

        # Entropy
        c = np.bincount(d_ids, minlength=8) / 30
        c_nz = c[c > 0]
        delta_entropies[t] = -np.sum(c_nz * np.log2(c_nz))

        # Third-order distance
        dd = np.bitwise_xor(d[:29], d[1:30])
        delta_mean_dists_3rd[t] = dd.sum(axis=1).mean()

    print(f"  Delta entropy: KW={delta_entropy:.3f}, null mean={delta_entropies.mean():.3f} ± {delta_entropies.std():.3f}")
    print(f"    KW percentile: {(delta_entropies <= delta_entropy).mean()*100:.2f}%")

    print(f"  Delta id-count (repeats): KW={freq.get('id', 0)}, null mean={delta_id_counts.mean():.2f} ± {delta_id_counts.std():.2f}")
    print(f"    KW percentile: {(delta_id_counts <= freq.get('id', 0)).mean()*100:.2f}%")

    print(f"  Third-order mean distance: KW={np.mean(delta_dists):.3f}, null mean={delta_mean_dists_3rd.mean():.3f} ± {delta_mean_dists_3rd.std():.3f}")
    print(f"    KW percentile: {(delta_mean_dists_3rd <= np.mean(delta_dists)).mean()*100:.2f}%")

    # Per-type comparison
    kw_type_counts = np.array([freq.get(n, 0) for n in NAME_ORDER])
    print(f"\n  Per-delta-type: KW count vs null mean ± std")
    for j, name in enumerate(NAME_ORDER):
        null_mean = delta_type_counts[:, j].mean()
        null_std = delta_type_counts[:, j].std()
        kw_val = kw_type_counts[j]
        pctile = (delta_type_counts[:, j] <= kw_val).mean() * 100
        z = (kw_val - null_mean) / null_std if null_std > 0 else 0
        print(f"    {name:>5}: KW={kw_val}, null={null_mean:.2f}±{null_std:.2f}, "
              f"pctile={pctile:.1f}%, z={z:+.2f}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: COSET STRUCTURE OF RUNNING-PRODUCT PATH
# ═══════════════════════════════════════════════════════════════════════════════

def computation_3():
    print("\n" + "=" * 80)
    print("COMPUTATION 3: RUNNING-PRODUCT PATH — COSET STRUCTURE")
    print("=" * 80)

    # Running product
    running = (0, 0, 0)
    products = []
    for k in KW_KERNELS:
        running = xor3(running, k)
        products.append(running)

    # First-return times to identity
    id_positions = [i for i, p in enumerate(products) if p == (0, 0, 0)]
    print(f"\n--- Returns to identity ---")
    print(f"  Positions (0-indexed): {id_positions}")
    print(f"  KW pair numbers: {[i+1 for i in id_positions]}")

    if len(id_positions) >= 2:
        gaps = [id_positions[i+1] - id_positions[i] for i in range(len(id_positions)-1)]
        print(f"  Gaps between returns: {gaps}")
        print(f"  Gap mean: {np.mean(gaps):.2f}, std: {np.std(gaps):.2f}")

    # First-return times for each element
    print(f"\n--- First occurrence of each element in running product ---")
    first_seen = {}
    for i, p in enumerate(products):
        name = KERNEL_NAMES[p]
        if name not in first_seen:
            first_seen[name] = i
    for name in NAME_ORDER:
        pos = first_seen.get(name, -1)
        print(f"  {name:>5}: position {pos} (bridge {pos+1})" if pos >= 0 else f"  {name:>5}: never")

    # All return times for each element
    print(f"\n--- All occurrences of each element ---")
    for name in NAME_ORDER:
        bits = [k for k, v in KERNEL_NAMES.items() if v == name][0]
        positions = [i for i, p in enumerate(products) if p == bits]
        print(f"  {name:>5}: positions {positions} (count={len(positions)})")

    # Subgroup residence analysis
    # Order-2 subgroups of Z₂³: {id, g} for each g ≠ id (7 subgroups)
    # Order-4 subgroups: kernels of projections Z₂³ → Z₂ (3 subgroups)
    #   {id, O, M, OM} = kernel of projection onto I bit
    #   {id, O, I, OI} = kernel of projection onto M bit
    #   {id, M, I, MI} = kernel of projection onto O bit
    # Also: {id, OM, OI, MI}, {id, OM, MI, OMI}... wait, let me enumerate properly.
    # Z₂³ has 7 subgroups of order 2, 7 subgroups of order 4.
    # Order-4 subgroups are Z₂² subgroups. There are C(3,2) = ... no.
    # Z₂³ has 7 elements of order 2, each generates a Z₂.
    # Order-4 subgroups: any two independent elements generate Z₂².
    # There are 7 subgroups of order 4 in Z₂³.

    print(f"\n--- Subgroup residence fractions (31 positions) ---")

    # Generate all subgroups of Z₂³
    all_elems = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
    id_elem = (0, 0, 0)

    # Order-4 subgroups: generated by any two independent elements
    order4_subgroups = []
    for i, g1 in enumerate(all_elems):
        if g1 == id_elem:
            continue
        for g2 in all_elems[i+1:]:
            if g2 == id_elem or g2 == g1:
                continue
            g3 = xor3(g1, g2)
            sg = frozenset([id_elem, g1, g2, g3])
            if len(sg) == 4 and sg not in order4_subgroups:
                order4_subgroups.append(sg)

    print(f"\n  Order-4 subgroups ({len(order4_subgroups)} total):")
    for sg in order4_subgroups:
        names = sorted([KERNEL_NAMES[e] for e in sg])
        in_count = sum(1 for p in products if p in sg)
        frac = in_count / 31
        expected = 4/8  # 50% by chance
        print(f"    {{{', '.join(names)}}}: {in_count}/31 = {frac:.3f} (expected 0.500)")

    # Check: is the path biased toward any coset?
    # The path visits id 6 times and MI 6 times. {id, MI} is the subgroup generated by MI.
    # How about {id, MI, OMI, OM} = ?
    # xor3(MI, OMI) = (0,1,1) xor (1,1,1) = (1,0,0) = O. Not OM.
    # {id, MI} ∪ coset = check what order-4 subgroup contains both id and MI
    for sg in order4_subgroups:
        if (0,0,0) in sg and (0,1,1) in sg:  # id and MI
            names = sorted([KERNEL_NAMES[e] for e in sg])
            in_count = sum(1 for p in products if p in sg)
            print(f"\n  Subgroup containing {{id, MI}}: {{{', '.join(names)}}}")
            print(f"    Residence: {in_count}/31 = {in_count/31:.3f}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: TRIGRAM-PAIR STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 80)
    print("COMPUTATION 4: TRIGRAM-PAIR STRUCTURE OF THE SEQUENCE")
    print("=" * 80)

    # For each pair, extract lower and upper trigrams of both hexagrams
    print(f"\n--- Trigram decomposition of KW pairs ---")
    print(f"  {'Pair':>4} {'Hex':>6} {'Lower1':>8} {'Upper1':>8} {'Lower2':>8} {'Upper2':>8}")
    print(f"  " + "-" * 55)

    pair_trigrams = []
    for k in range(32):
        idx_a = 2 * k
        idx_b = 2 * k + 1
        lt_a = lower_trigram(idx_a)
        ut_a = upper_trigram(idx_a)
        lt_b = lower_trigram(idx_b)
        ut_b = upper_trigram(idx_b)
        pair_trigrams.append((lt_a, ut_a, lt_b, ut_b))

        nums = f"({KING_WEN[idx_a][0]},{KING_WEN[idx_b][0]})"
        print(f"  {k:>4} {nums:>6} "
              f"{trigram_name(lt_a):>8} {trigram_name(ut_a):>8} "
              f"{trigram_name(lt_b):>8} {trigram_name(ut_b):>8}")

    # Upper trigram pair sequence
    print(f"\n--- Upper trigram pairs ---")
    upper_pairs = [(pt[1], pt[3]) for pt in pair_trigrams]
    upper_pair_names = [(trigram_name(a), trigram_name(b)) for a, b in upper_pairs]
    distinct_upper = len(set(upper_pairs))
    print(f"  Distinct upper-trigram pairs: {distinct_upper}")
    print(f"  Sequence:")
    for k, (a, b) in enumerate(upper_pair_names):
        print(f"    Pair {k:>2}: ({a}, {b})")

    # Lower trigram pair sequence
    lower_pairs = [(pt[0], pt[2]) for pt in pair_trigrams]
    lower_pair_names = [(trigram_name(a), trigram_name(b)) for a, b in lower_pairs]
    distinct_lower = len(set(lower_pairs))
    print(f"\n  Distinct lower-trigram pairs: {distinct_lower}")

    # Trigram transitions between consecutive pairs
    print(f"\n--- Trigram transitions between consecutive pairs ---")
    print(f"  (Exit hex upper trig → Entry hex upper trig)")

    upper_transitions = []
    lower_transitions = []
    for k in range(31):
        # Exit hex = pair[k]'s second member
        exit_upper = pair_trigrams[k][3]  # upper trig of hex_b
        exit_lower = pair_trigrams[k][2]  # lower trig of hex_b
        # Entry hex = pair[k+1]'s first member
        entry_upper = pair_trigrams[k+1][1]  # upper trig of hex_a
        entry_lower = pair_trigrams[k+1][0]  # lower trig of hex_a

        upper_transitions.append((exit_upper, entry_upper))
        lower_transitions.append((exit_lower, entry_lower))

    # Upper trigram transition analysis
    ut_same = sum(1 for a, b in upper_transitions if a == b)
    lt_same = sum(1 for a, b in lower_transitions if a == b)
    print(f"  Upper trigram same across bridge: {ut_same}/31 ({ut_same/31*100:.1f}%)")
    print(f"  Lower trigram same across bridge: {lt_same}/31 ({lt_same/31*100:.1f}%)")

    # Upper trigram transition matrix
    trig_list = sorted(TRIGRAMS.keys())
    trig_to_idx = {t: i for i, t in enumerate(trig_list)}
    trig_names = [trigram_name(t) for t in trig_list]

    ut_matrix = np.zeros((8, 8), dtype=int)
    for a, b in upper_transitions:
        ut_matrix[trig_to_idx[a]][trig_to_idx[b]] += 1

    print(f"\n  Upper trigram transition matrix (exit → entry):")
    header = "          " + " ".join(f"{n:>8}" for n in trig_names)
    print(header)
    for i, name in enumerate(trig_names):
        row = " ".join(f"{ut_matrix[i][j]:>8}" for j in range(8))
        print(f"  {name:>8} {row}")

    lt_matrix = np.zeros((8, 8), dtype=int)
    for a, b in lower_transitions:
        lt_matrix[trig_to_idx[a]][trig_to_idx[b]] += 1

    print(f"\n  Lower trigram transition matrix (exit → entry):")
    header = "          " + " ".join(f"{n:>8}" for n in trig_names)
    print(header)
    for i, name in enumerate(trig_names):
        row = " ".join(f"{lt_matrix[i][j]:>8}" for j in range(8))
        print(f"  {name:>8} {row}")

    # Same-trigram clustering for consecutive pairs
    print(f"\n--- Same-trigram clustering between consecutive pairs ---")
    shared_upper_entry = 0  # pair k's entry hex upper == pair k+1's entry hex upper
    shared_any = 0
    for k in range(31):
        pt_k = pair_trigrams[k]
        pt_k1 = pair_trigrams[k+1]
        # Any shared trigram between the 4 trigrams of pair k and 4 of pair k+1
        trigs_k = set([pt_k[0], pt_k[1], pt_k[2], pt_k[3]])
        trigs_k1 = set([pt_k1[0], pt_k1[1], pt_k1[2], pt_k1[3]])
        if trigs_k & trigs_k1:
            shared_any += 1
    print(f"  Consecutive pairs sharing any trigram: {shared_any}/31 ({shared_any/31*100:.1f}%)")

    # Expected from random? Each pair has 4 trigrams (some may repeat).
    # Quick null: how many trigrams does a random pair typically use?
    trigs_per_pair = [len(set([pt[0], pt[1], pt[2], pt[3]])) for pt in pair_trigrams]
    print(f"  Distinct trigrams per pair: mean={np.mean(trigs_per_pair):.2f}, "
          f"min={min(trigs_per_pair)}, max={max(trigs_per_pair)}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 5: BIAS-CORRECTED MI + SHUFFLE NULL
# ═══════════════════════════════════════════════════════════════════════════════

def computation_5():
    print("\n" + "=" * 80)
    print("COMPUTATION 5: BIAS-CORRECTED MI + SHUFFLE NULL")
    print("=" * 80)

    # Raw MI
    print(f"\n--- Raw MI ---")
    print(f"  H(k) = {KW_H:.4f}")
    print(f"  H(k|k_prev) = {KW_HCOND:.4f}")
    print(f"  MI_raw = {KW_MI:.4f}")

    # Miller-Madow correction
    # Count nonzero cells in the joint distribution (transition matrix)
    kernel_ids = [k[0]*4 + k[1]*2 + k[2] for k in KW_KERNELS]
    trans_matrix = np.zeros((8, 8), dtype=int)
    for i in range(30):
        trans_matrix[kernel_ids[i]][kernel_ids[i+1]] += 1

    m_joint = (trans_matrix > 0).sum()
    m_from = (trans_matrix.sum(axis=1) > 0).sum()
    m_to = (trans_matrix.sum(axis=0) > 0).sum()

    N = 30  # number of transitions

    # Miller-Madow bias for joint entropy ≈ (m_joint - 1) / (2N ln2)
    # Miller-Madow bias for marginal entropy ≈ (m_from - 1) / (2N ln2)
    # MI = H(X) + H(Y) - H(X,Y), bias ≈ (m_from + m_to - m_joint - 1)/(2N ln2)
    # Actually for MI: bias ≈ (m_joint - m_from - m_to + 1) / (2N ln2)
    # But simplest: just correct H(k|k_prev) directly.
    # H(k|k_prev)_corrected = H(k|k_prev)_raw + (m_joint - m_from) / (2N ln2)
    # MI_corrected = MI_raw - (m_joint - m_from) / (2N ln2)

    bias_correction = (m_joint - m_from) / (2 * N * np.log(2))

    mi_corrected = KW_MI - bias_correction

    print(f"\n--- Miller-Madow correction ---")
    print(f"  Nonzero cells in transition matrix: {m_joint}")
    print(f"  Nonzero 'from' states: {m_from}")
    print(f"  Nonzero 'to' states: {m_to}")
    print(f"  Bias estimate: {bias_correction:.4f} bits")
    print(f"  MI_corrected = {mi_corrected:.4f}")

    # Shuffle-based null: shuffle the kernel sequence, preserving marginals
    print(f"\n--- Shuffle null (100,000 shuffles) ---")
    rng = np.random.default_rng(42)
    N_SHUFFLE = 100_000

    shuffle_mis = np.empty(N_SHUFFLE)
    kw_kernel_arr = list(KW_KERNELS)  # 31 kernels

    for t in range(N_SHUFFLE):
        shuffled = list(kw_kernel_arr)
        rng.shuffle(shuffled)
        _, _, mi = compute_mi(shuffled)
        shuffle_mis[t] = mi

    print(f"  Shuffle MI: mean={shuffle_mis.mean():.4f}, std={shuffle_mis.std():.4f}")
    print(f"  Shuffle MI 95th percentile: {np.percentile(shuffle_mis, 95):.4f}")
    print(f"  Shuffle MI 99th percentile: {np.percentile(shuffle_mis, 99):.4f}")
    print(f"  KW MI_raw = {KW_MI:.4f}, percentile in shuffle null: {(shuffle_mis <= KW_MI).mean()*100:.2f}%")
    print(f"  KW MI_corrected = {mi_corrected:.4f}, percentile in shuffle null: {(shuffle_mis <= mi_corrected).mean()*100:.2f}%")

    # How much MI is expected from small-sample effects alone?
    print(f"\n--- Summary ---")
    print(f"  MI_raw:       {KW_MI:.4f}")
    print(f"  Bias:        -{bias_correction:.4f}")
    print(f"  MI_corrected: {mi_corrected:.4f}")
    print(f"  Shuffle null mean: {shuffle_mis.mean():.4f}")
    print(f"  MI excess over shuffle null: {KW_MI - shuffle_mis.mean():.4f} "
          f"({(KW_MI - shuffle_mis.mean()) / shuffle_mis.std():.2f} σ)")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    f1s, mis = computation_1()
    computation_2(f1s, mis)
    computation_3()
    computation_4()
    computation_5()

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
