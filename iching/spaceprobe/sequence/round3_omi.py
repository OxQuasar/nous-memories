"""
Round 3: Is OMI dominance the whole story?

Tests:
1. OMI dominance conditioned on f1 — independent signal or just f1's mechanism?
2. Mechanical entailment of subgroup bias from delta distribution
3. OMI spacing pattern — clustering or regularity?
4. Delta sequence autocorrelation
5. Global path properties — products, symmetry, reversal
6. Joint constraint tightness — how much of the search space is eliminated?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
from sequence import KING_WEN

import numpy as np
from collections import Counter

# ─── Constants & utilities ───────────────────────────────────────────────────

HEX_BITS = [h[2] for h in KING_WEN]
PAIRS = [(HEX_BITS[2*k], HEX_BITS[2*k+1]) for k in range(32)]

KERNEL_NAMES = {
    (0,0,0): "id",  (1,0,0): "O",   (0,1,0): "M",   (0,0,1): "I",
    (1,1,0): "OM",  (1,0,1): "OI",  (0,1,1): "MI",  (1,1,1): "OMI",
}
NAME_ORDER = ["id", "O", "M", "I", "OM", "OI", "MI", "OMI"]

PAIR_A = np.array([[int(c) for c in PAIRS[k][0]] for k in range(32)], dtype=np.int8)
PAIR_B = np.array([[int(c) for c in PAIRS[k][1]] for k in range(32)], dtype=np.int8)

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def hamming3(a, b):
    return sum(x != y for x, y in zip(a, b))

def compute_kernels_from_pairs(pairs_list):
    """31 kernel 3-tuples from 32 string pairs."""
    kernels = []
    for k in range(len(pairs_list) - 1):
        exit_h = pairs_list[k][1]
        entry_h = pairs_list[k + 1][0]
        mask = tuple(int(exit_h[i]) ^ int(entry_h[i]) for i in range(6))
        kernels.append((mask[5], mask[4], mask[3]))
    return kernels

def random_trial_full(rng):
    """One random trial. Returns (f1, omi_count, kernel_ids, delta_ids, n_repeats, n_types)."""
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
    kernel_ids = kerns[:, 0] * 4 + kerns[:, 1] * 2 + kerns[:, 2]

    # Deltas
    d = np.bitwise_xor(kerns[:30], kerns[1:31])  # (30, 3)
    delta_ids = d[:, 0] * 4 + d[:, 1] * 2 + d[:, 2]
    dists = d.sum(axis=1)

    f1 = dists.mean()
    omi_count = (delta_ids == 7).sum()  # OMI = (1,1,1) = 7
    n_repeats = (dists == 0).sum()
    n_types = len(np.unique(kernel_ids))

    return f1, int(omi_count), kernel_ids, delta_ids, int(n_repeats), int(n_types)

# ─── KW baseline ────────────────────────────────────────────────────────────

KW_KERNELS = compute_kernels_from_pairs(PAIRS)
KW_DELTAS = [xor3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
KW_DISTS = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
KW_F1 = np.mean(KW_DISTS)
KW_OMI_COUNT = sum(1 for d in KW_DELTAS if d == (1, 1, 1))
KW_REPEATS = sum(1 for d in KW_DISTS if d == 0)
KW_N_TYPES = len(set(KW_KERNELS))

KW_OMI_POSITIONS = [i for i, d in enumerate(KW_DELTAS) if d == (1, 1, 1)]

print(f"KW baseline: f1={KW_F1:.4f}, OMI count={KW_OMI_COUNT}, repeats={KW_REPEATS}, types={KW_N_TYPES}")
print(f"KW OMI positions (0-indexed): {KW_OMI_POSITIONS}")
print(f"KW delta sequence: {' '.join(KERNEL_NAMES[d] for d in KW_DELTAS)}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: OMI DOMINANCE CONDITIONED ON f1
# ═══════════════════════════════════════════════════════════════════════════════

def computation_1():
    print("\n" + "=" * 80)
    print("COMPUTATION 1: OMI DOMINANCE CONDITIONED ON f1 (1M trials)")
    print("=" * 80)

    rng = np.random.default_rng(42)
    N = 1_000_000

    f1s = np.empty(N)
    omi_counts = np.empty(N, dtype=int)
    repeats = np.empty(N, dtype=int)
    n_types = np.empty(N, dtype=int)

    for t in range(N):
        f1, omi, _, _, rep, nt = random_trial_full(rng)
        f1s[t] = f1
        omi_counts[t] = omi
        repeats[t] = rep
        n_types[t] = nt
        if (t + 1) % 200_000 == 0:
            print(f"  ... {t+1}/{N}")

    # Correlation
    corr = np.corrcoef(f1s, omi_counts)[0, 1]
    print(f"\n--- Correlation ---")
    print(f"  Pearson r(f1, OMI count) = {corr:.4f}")

    # Overall OMI distribution
    print(f"\n--- OMI count distribution ---")
    omi_dist = Counter(omi_counts)
    for v in sorted(omi_dist):
        pct = omi_dist[v] / N * 100
        print(f"  OMI={v}: {omi_dist[v]:>8} ({pct:.2f}%)")
    print(f"  KW OMI={KW_OMI_COUNT}, percentile: {(omi_counts <= KW_OMI_COUNT).mean()*100:.2f}%")

    # Conditioned on f1 ≥ 1.70
    print(f"\n--- Conditional: f1 ≥ 1.70 ---")
    mask_high = f1s >= 1.70
    n_high = mask_high.sum()
    print(f"  Trials: {n_high} ({n_high/N*100:.2f}%)")
    if n_high > 0:
        omi_high = omi_counts[mask_high]
        print(f"  OMI count: mean={omi_high.mean():.3f}, std={omi_high.std():.3f}, "
              f"min={omi_high.min()}, max={omi_high.max()}")
        pctile = (omi_high <= KW_OMI_COUNT).mean() * 100
        print(f"  KW OMI={KW_OMI_COUNT}, conditional percentile: {pctile:.2f}%")

        # Distribution within high-f1
        omi_dist_high = Counter(omi_high)
        print(f"  Distribution:")
        for v in sorted(omi_dist_high):
            print(f"    OMI={v}: {omi_dist_high[v]:>6} ({omi_dist_high[v]/n_high*100:.2f}%)")

    # Conditioned on OMI count ≥ 8
    print(f"\n--- Conditional: OMI count ≥ 8 ---")
    mask_omi = omi_counts >= KW_OMI_COUNT
    n_omi = mask_omi.sum()
    print(f"  Trials: {n_omi} ({n_omi/N*100:.2f}%)")
    if n_omi > 0:
        f1_omi = f1s[mask_omi]
        print(f"  f1: mean={f1_omi.mean():.4f}, std={f1_omi.std():.4f}")
        print(f"  KW f1={KW_F1:.4f} in this subset: percentile {(f1_omi <= KW_F1).mean()*100:.2f}%")

    # Mean OMI per f1 bin (finer at high end)
    print(f"\n--- Mean OMI count per f1 bin ---")
    bin_edges = np.array([0.7, 1.0, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.3])
    for i in range(len(bin_edges) - 1):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        mask = (f1s >= lo) & (f1s < hi)
        if i == len(bin_edges) - 2:
            mask = (f1s >= lo) & (f1s <= hi)
        n = mask.sum()
        if n > 0:
            print(f"  f1 ∈ [{lo:.1f}, {hi:.1f}): n={n:>7}, "
                  f"mean OMI={omi_counts[mask].mean():.3f} ± {omi_counts[mask].std():.3f}")

    return f1s, omi_counts, repeats, n_types

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: MECHANICAL ENTAILMENT OF SUBGROUP BIAS
# ═══════════════════════════════════════════════════════════════════════════════

def computation_2():
    print("\n" + "=" * 80)
    print("COMPUTATION 2: MECHANICAL ENTAILMENT OF SUBGROUP BIAS")
    print("=" * 80)

    # The subgroup in question: {id, O, MI, OMI} = elements where bit 1 (M-bit) = bit 2 (I-bit)
    # In our encoding: (O, M, I) → element is in subgroup iff M == I
    # id=(0,0,0)✓, O=(1,0,0)✓, M=(0,1,0)✗, I=(0,0,1)✗, OM=(1,1,0)✗, OI=(1,0,1)✗, MI=(0,1,1)✓, OMI=(1,1,1)✓
    SUBGROUP = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}
    subgroup_name = "{id, O, MI, OMI}"

    # KW running product and subgroup residence
    running = (0, 0, 0)
    kw_products = []
    for k in KW_KERNELS:
        running = xor3(running, k)
        kw_products.append(running)
    kw_in_subgroup = sum(1 for p in kw_products if p in SUBGROUP)
    kw_frac = kw_in_subgroup / 31

    print(f"\nKW subgroup {subgroup_name} residence: {kw_in_subgroup}/31 = {kw_frac:.4f}")

    # Shuffle deltas (preserve distribution, randomize order) + random start
    rng = np.random.default_rng(42)
    N_SHUFFLE = 100_000
    shuffle_fracs = np.empty(N_SHUFFLE)

    kw_delta_list = list(KW_DELTAS)  # 30 deltas

    for t in range(N_SHUFFLE):
        shuffled = list(kw_delta_list)
        rng.shuffle(shuffled)

        # Random starting element for the running product
        start_idx = rng.integers(0, 8)
        start = list(KERNEL_NAMES.keys())[start_idx]

        # Build running product: the kernels are reconstructed from deltas
        # k₁ is arbitrary, then k₂ = k₁ ⊕ δ₁, k₃ = k₂ ⊕ δ₂, etc.
        # Running product after kernel i = k₁ ⊕ k₂ ⊕ ... ⊕ kᵢ
        # With k₁ = start, kᵢ₊₁ = kᵢ ⊕ δᵢ:
        #   running after 1 kernel: k₁ = start
        #   running after 2 kernels: k₁ ⊕ k₂ = k₁ ⊕ (k₁ ⊕ δ₁) = δ₁
        #
        # Actually: KW running product = k₁ ⊕ k₂ ⊕ ... ⊕ kₙ
        # With kᵢ as the actual kernels. The running product depends on the kernels themselves.
        # The DELTA sequence determines the kernel sequence up to the initial kernel.
        # k₁ = start, k₂ = start ⊕ δ₁, k₃ = start ⊕ δ₁ ⊕ δ₂, ...
        # running product after n kernels = k₁ ⊕ k₂ ⊕ ... ⊕ kₙ
        #   = start ⊕ (start ⊕ δ₁) ⊕ (start ⊕ δ₁ ⊕ δ₂) ⊕ ...
        #
        # This gets complicated. Let me take a different approach:
        # Build the 31 kernels from the shuffled deltas, then compute running product.

        # Reconstruct kernels: k₁ = start, kᵢ₊₁ = kᵢ ⊕ δᵢ
        kernels = [start]
        for d in shuffled:
            kernels.append(xor3(kernels[-1], d))
        # kernels has 31 elements

        # Running product
        running_elem = (0, 0, 0)
        in_count = 0
        for k in kernels:
            running_elem = xor3(running_elem, k)
            if running_elem in SUBGROUP:
                in_count += 1

        shuffle_fracs[t] = in_count / 31

    print(f"\n--- Shuffle null (same delta distribution, random order, random start) ---")
    print(f"  Mean subgroup residence: {shuffle_fracs.mean():.4f} ± {shuffle_fracs.std():.4f}")
    print(f"  KW residence: {kw_frac:.4f}")
    print(f"  KW percentile: {(shuffle_fracs <= kw_frac).mean()*100:.2f}%")

    # Also: fixed start at KW's first kernel (M)
    print(f"\n--- Shuffle null with FIXED start (k₁ = M, as in KW) ---")
    shuffle_fracs_fixed = np.empty(N_SHUFFLE)
    kw_first_kernel = KW_KERNELS[0]  # M = (0, 1, 0)

    for t in range(N_SHUFFLE):
        shuffled = list(kw_delta_list)
        rng.shuffle(shuffled)
        kernels = [kw_first_kernel]
        for d in shuffled:
            kernels.append(xor3(kernels[-1], d))
        running_elem = (0, 0, 0)
        in_count = 0
        for k in kernels:
            running_elem = xor3(running_elem, k)
            if running_elem in SUBGROUP:
                in_count += 1
        shuffle_fracs_fixed[t] = in_count / 31

    print(f"  Mean subgroup residence: {shuffle_fracs_fixed.mean():.4f} ± {shuffle_fracs_fixed.std():.4f}")
    print(f"  KW percentile: {(shuffle_fracs_fixed <= kw_frac).mean()*100:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: OMI SPACING PATTERN
# ═══════════════════════════════════════════════════════════════════════════════

def computation_3():
    print("\n" + "=" * 80)
    print("COMPUTATION 3: OMI SPACING PATTERN")
    print("=" * 80)

    positions = KW_OMI_POSITIONS
    print(f"\nOMI positions (0-indexed in 30 deltas): {positions}")
    print(f"OMI count: {len(positions)}")

    # Gaps between consecutive OMI positions
    gaps = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
    print(f"Gaps between consecutive OMIs: {gaps}")
    print(f"Gap statistics: mean={np.mean(gaps):.2f}, std={np.std(gaps):.2f}, "
          f"min={min(gaps)}, max={max(gaps)}")

    # First-half vs second-half
    first_half = sum(1 for p in positions if p < 15)
    second_half = sum(1 for p in positions if p >= 15)
    print(f"\nFirst half (pos 0-14): {first_half} OMIs")
    print(f"Second half (pos 15-29): {second_half} OMIs")

    # Which pairs do OMI transitions connect?
    print(f"\n--- Pairs connected by OMI transitions ---")
    for pos in positions:
        # Delta at position pos connects kernel[pos] to kernel[pos+1]
        # kernel[pos] is bridge[pos], connecting pair[pos] exit to pair[pos+1] entry
        # kernel[pos+1] is bridge[pos+1], connecting pair[pos+1] exit to pair[pos+2] entry
        # The delta connects these two bridges
        k_before = KERNEL_NAMES[KW_KERNELS[pos]]
        k_after = KERNEL_NAMES[KW_KERNELS[pos + 1]]
        pair_before = pos  # bridge[pos] exits from pair[pos]
        pair_after = pos + 1  # bridge[pos+1] exits from pair[pos+1]
        nums_before = (KING_WEN[2*pair_before][0], KING_WEN[2*pair_before+1][0])
        nums_mid = (KING_WEN[2*(pair_before+1)][0], KING_WEN[2*(pair_before+1)+1][0])
        nums_after = (KING_WEN[2*(pair_after+1)][0], KING_WEN[2*(pair_after+1)+1][0])
        print(f"  δ{pos+1:>2}: {k_before:>5} → {k_after:<5}  "
              f"(pairs {nums_before} → {nums_mid} → {nums_after})")

    # Null model: 8 random positions out of 30
    print(f"\n--- Null model: 8 random positions in 30 slots ---")
    rng = np.random.default_rng(42)
    N_NULL = 100_000

    null_gap_vars = np.empty(N_NULL)
    null_max_gaps = np.empty(N_NULL, dtype=int)
    null_min_gaps = np.empty(N_NULL, dtype=int)
    null_first_half = np.empty(N_NULL, dtype=int)
    null_max_run = np.empty(N_NULL, dtype=int)  # max consecutive OMI positions

    for t in range(N_NULL):
        pos = sorted(rng.choice(30, size=8, replace=False))
        g = [pos[i+1] - pos[i] for i in range(7)]
        null_gap_vars[t] = np.var(g)
        null_max_gaps[t] = max(g)
        null_min_gaps[t] = min(g)
        null_first_half[t] = sum(1 for p in pos if p < 15)
        # Max consecutive: count runs of gap=1
        max_consec = 1
        current = 1
        for i in range(1, 8):
            if pos[i] == pos[i-1] + 1:
                current += 1
                max_consec = max(max_consec, current)
            else:
                current = 1
        null_max_run[t] = max_consec

    kw_gap_var = np.var(gaps)
    kw_max_gap = max(gaps)
    kw_min_gap = min(gaps)
    # Max consecutive OMI
    kw_max_consec = 1
    current = 1
    for i in range(1, len(positions)):
        if positions[i] == positions[i-1] + 1:
            current += 1
            kw_max_consec = max(kw_max_consec, current)
        else:
            current = 1

    print(f"  Gap variance:    KW={kw_gap_var:.2f}, null mean={null_gap_vars.mean():.2f} ± {null_gap_vars.std():.2f}, "
          f"pctile={( null_gap_vars <= kw_gap_var).mean()*100:.1f}%")
    print(f"  Max gap:         KW={kw_max_gap}, null mean={null_max_gaps.mean():.2f} ± {null_max_gaps.std():.2f}, "
          f"pctile={(null_max_gaps <= kw_max_gap).mean()*100:.1f}%")
    print(f"  Min gap:         KW={kw_min_gap}, null mean={null_min_gaps.mean():.2f} ± {null_min_gaps.std():.2f}, "
          f"pctile={(null_min_gaps <= kw_min_gap).mean()*100:.1f}%")
    print(f"  First-half count: KW={first_half}, null mean={null_first_half.mean():.2f} ± {null_first_half.std():.2f}, "
          f"pctile={(null_first_half <= first_half).mean()*100:.1f}%")
    print(f"  Max consecutive: KW={kw_max_consec}, null mean={null_max_run.mean():.2f} ± {null_max_run.std():.2f}, "
          f"pctile={(null_max_run <= kw_max_consec).mean()*100:.1f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: DELTA SEQUENCE AUTOCORRELATION
# ═══════════════════════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 80)
    print("COMPUTATION 4: DELTA SEQUENCE AUTOCORRELATION")
    print("=" * 80)

    # Encode deltas as 3-bit vectors
    delta_vecs = np.array([[d[0], d[1], d[2]] for d in KW_DELTAS], dtype=float)
    # Center each component
    delta_centered = delta_vecs - delta_vecs.mean(axis=0)

    # Lag-1 autocorrelation: correlation between δᵢ and δᵢ₊₁
    # Use the mean of per-component correlations
    lag1_corrs = []
    for comp in range(3):
        x = delta_centered[:29, comp]
        y = delta_centered[1:30, comp]
        denom = np.sqrt((x**2).sum() * (y**2).sum())
        if denom > 0:
            lag1_corrs.append((x * y).sum() / denom)
        else:
            lag1_corrs.append(0.0)
    
    print(f"\n--- Lag-1 autocorrelation per component ---")
    comp_names = ["O-bit", "M-bit", "I-bit"]
    for i, (name, r) in enumerate(zip(comp_names, lag1_corrs)):
        print(f"  {name}: r = {r:.4f}")
    mean_lag1 = np.mean(lag1_corrs)
    print(f"  Mean across components: {mean_lag1:.4f}")

    # Alternative: Hamming-based lag-1 correlation
    # Mean Hamming distance between δᵢ and δᵢ₊₁ (already computed in round 2 as third-order)
    lag1_hamming = [hamming3(KW_DELTAS[i], KW_DELTAS[i+1]) for i in range(29)]
    print(f"\n--- Lag-1 Hamming distance (δᵢ, δᵢ₊₁) ---")
    print(f"  Mean: {np.mean(lag1_hamming):.4f}")
    print(f"  Distribution: {dict(sorted(Counter(lag1_hamming).items()))}")

    # Run-length distribution
    print(f"\n--- Run-length distribution ---")
    runs = []
    current_delta = KW_DELTAS[0]
    current_run = 1
    for i in range(1, 30):
        if KW_DELTAS[i] == current_delta:
            current_run += 1
        else:
            runs.append((KERNEL_NAMES[current_delta], current_run))
            current_delta = KW_DELTAS[i]
            current_run = 1
    runs.append((KERNEL_NAMES[current_delta], current_run))

    print(f"  Total runs: {len(runs)}")
    run_lengths = [r[1] for r in runs]
    print(f"  Run lengths: {run_lengths}")
    print(f"  Max run: {max(run_lengths)}")
    print(f"  Mean run length: {np.mean(run_lengths):.3f}")
    print(f"  Runs of length ≥2: {sum(1 for r in run_lengths if r >= 2)}")
    print(f"  Detailed runs: {runs}")

    # Delta-delta MI (with bias correction)
    print(f"\n--- Delta-delta MI ---")
    n_trans = 29  # 29 consecutive delta pairs
    delta_ids = [d[0]*4 + d[1]*2 + d[2] for d in KW_DELTAS]

    from_counts = np.zeros(8, dtype=int)
    trans_matrix = np.zeros((8, 8), dtype=int)
    for i in range(n_trans):
        from_counts[delta_ids[i]] += 1
        trans_matrix[delta_ids[i]][delta_ids[i+1]] += 1

    p_from = from_counts / n_trans
    h_k = -sum(p * np.log2(p) for p in p_from if p > 0)

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

    mi_raw = h_k - h_cond
    m_joint = (trans_matrix > 0).sum()
    m_from = (from_counts > 0).sum()
    bias = (m_joint - m_from) / (2 * n_trans * np.log(2))
    mi_corrected = mi_raw - bias

    print(f"  H(δ) = {h_k:.4f}")
    print(f"  H(δ|δ_prev) = {h_cond:.4f}")
    print(f"  MI_raw = {mi_raw:.4f}")
    print(f"  Nonzero cells: {m_joint}, bias: {bias:.4f}")
    print(f"  MI_corrected = {mi_corrected:.4f}")

    # Compare to null
    rng = np.random.default_rng(42)
    N_NULL = 100_000
    null_lag1_means = np.empty(N_NULL)
    null_n_runs = np.empty(N_NULL, dtype=int)
    null_max_runs = np.empty(N_NULL, dtype=int)

    for t in range(N_NULL):
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
        kerns = masks[:, [5, 4, 3]]
        d = np.bitwise_xor(kerns[:30], kerns[1:31])

        # Lag-1 hamming
        dd = np.bitwise_xor(d[:29], d[1:30])
        null_lag1_means[t] = dd.sum(axis=1).mean()

        # Runs
        d_ids = d[:, 0] * 4 + d[:, 1] * 2 + d[:, 2]
        n_runs = 1
        max_run = 1
        cur_run = 1
        for i in range(1, 30):
            if d_ids[i] == d_ids[i-1]:
                cur_run += 1
                max_run = max(max_run, cur_run)
            else:
                n_runs += 1
                cur_run = 1
        null_n_runs[t] = n_runs
        null_max_runs[t] = max_run

    kw_lag1_mean = np.mean(lag1_hamming)
    kw_n_runs = len(runs)
    kw_max_run = max(run_lengths)

    print(f"\n--- Null comparison ---")
    print(f"  Lag-1 mean Hamming: KW={kw_lag1_mean:.4f}, null={null_lag1_means.mean():.4f} ± {null_lag1_means.std():.4f}, "
          f"pctile={(null_lag1_means <= kw_lag1_mean).mean()*100:.2f}%")
    print(f"  Number of runs: KW={kw_n_runs}, null={null_n_runs.mean():.2f} ± {null_n_runs.std():.2f}, "
          f"pctile={(null_n_runs <= kw_n_runs).mean()*100:.2f}%")
    print(f"  Max run length: KW={kw_max_run}, null={null_max_runs.mean():.2f} ± {null_max_runs.std():.2f}, "
          f"pctile={(null_max_runs <= kw_max_run).mean()*100:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 5: GLOBAL PATH PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

def computation_5():
    print("\n" + "=" * 80)
    print("COMPUTATION 5: GLOBAL PATH PROPERTIES")
    print("=" * 80)

    # Total delta product
    total_delta = (0, 0, 0)
    for d in KW_DELTAS:
        total_delta = xor3(total_delta, d)
    print(f"\n--- Total delta product ---")
    print(f"  XOR of all 30 deltas: {KERNEL_NAMES[total_delta]} = {total_delta}")
    print(f"  (This equals k₁ ⊕ k₃₁ = {KERNEL_NAMES[KW_KERNELS[0]]} ⊕ {KERNEL_NAMES[KW_KERNELS[30]]} "
          f"= {KERNEL_NAMES[xor3(KW_KERNELS[0], KW_KERNELS[30])]})")

    # Verify
    check = xor3(KW_KERNELS[0], KW_KERNELS[30])
    assert check == total_delta, f"Mismatch: {check} vs {total_delta}"

    # Half-sequence products
    half1_delta = (0, 0, 0)
    for d in KW_DELTAS[:15]:
        half1_delta = xor3(half1_delta, d)

    half2_delta = (0, 0, 0)
    for d in KW_DELTAS[15:]:
        half2_delta = xor3(half2_delta, d)

    print(f"\n--- Half-sequence products ---")
    print(f"  First half (δ₁..δ₁₅):  {KERNEL_NAMES[half1_delta]} = {half1_delta}")
    print(f"  Second half (δ₁₆..δ₃₀): {KERNEL_NAMES[half2_delta]} = {half2_delta}")
    print(f"  XOR of halves: {KERNEL_NAMES[xor3(half1_delta, half2_delta)]}")
    print(f"  (Should equal total: {KERNEL_NAMES[total_delta]})")

    # Also: total kernel product (from round 1, should be M)
    total_kernel = (0, 0, 0)
    for k in KW_KERNELS:
        total_kernel = xor3(total_kernel, k)
    print(f"\n--- Total kernel product ---")
    print(f"  XOR of all 31 kernels: {KERNEL_NAMES[total_kernel]} = {total_kernel}")

    # Half kernel products
    half1_kernel = (0, 0, 0)
    for k in KW_KERNELS[:16]:
        half1_kernel = xor3(half1_kernel, k)
    half2_kernel = (0, 0, 0)
    for k in KW_KERNELS[16:]:
        half2_kernel = xor3(half2_kernel, k)
    print(f"  First half (k₁..k₁₆):  {KERNEL_NAMES[half1_kernel]} = {half1_kernel}")
    print(f"  Second half (k₁₇..k₃₁): {KERNEL_NAMES[half2_kernel]} = {half2_kernel}")

    # Reversal test
    print(f"\n--- Reversal test ---")
    reversed_pairs = list(reversed(PAIRS))
    # When reversing: each pair (a, b) becomes (b, a) because the exit/entry swap
    # Actually no — reversing the pair ORDER means the same pairs in reverse.
    # But within each pair, which hex is "entry" and which is "exit" also flips.
    # In the forward sequence: entry = pair[k][0], exit = pair[k][1]
    # In reversed sequence: the k-th pair was originally pair[31-k],
    # but now its entry is the OLD exit (pair[31-k][1]) and its exit is the old entry (pair[31-k][0])
    reversed_pairs_swapped = [(PAIRS[31-k][1], PAIRS[31-k][0]) for k in range(32)]
    rev_kernels = compute_kernels_from_pairs(reversed_pairs_swapped)
    rev_deltas = [xor3(rev_kernels[i], rev_kernels[i+1]) for i in range(30)]

    print(f"  Forward kernel sequence:")
    print(f"    {' '.join(KERNEL_NAMES[k] for k in KW_KERNELS)}")
    print(f"  Reversed kernel sequence:")
    print(f"    {' '.join(KERNEL_NAMES[k] for k in rev_kernels)}")

    # Is the reversed kernel sequence the same as the forward one reversed?
    forward_rev = list(reversed(KW_KERNELS))
    same_as_reverse = (rev_kernels == forward_rev)
    print(f"\n  Reversed seq == forward seq reversed? {same_as_reverse}")

    # Delta distribution comparison
    fwd_delta_counts = Counter(KW_DELTAS)
    rev_delta_counts = Counter(rev_deltas)
    print(f"\n  Forward delta distribution: {dict(sorted((KERNEL_NAMES[k], v) for k, v in fwd_delta_counts.items()))}")
    print(f"  Reversed delta distribution: {dict(sorted((KERNEL_NAMES[k], v) for k, v in rev_delta_counts.items()))}")

    same_dist = (fwd_delta_counts == rev_delta_counts)
    print(f"  Same distribution? {same_dist}")

    # The reversed delta sequence should be the forward delta sequence reversed
    # (since δᵢ = kᵢ ⊕ kᵢ₊₁ and reversing the kernel sequence reverses the deltas)
    fwd_deltas_reversed = list(reversed(KW_DELTAS))
    print(f"\n  Forward deltas reversed:")
    print(f"    {' '.join(KERNEL_NAMES[d] for d in fwd_deltas_reversed)}")
    print(f"  Reversed sequence deltas:")
    print(f"    {' '.join(KERNEL_NAMES[d] for d in rev_deltas)}")
    match = (fwd_deltas_reversed == rev_deltas)
    print(f"  Match? {match}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 6: JOINT CONSTRAINT TIGHTNESS
# ═══════════════════════════════════════════════════════════════════════════════

def computation_6(f1s, omi_counts, repeats, n_types):
    print("\n" + "=" * 80)
    print("COMPUTATION 6: JOINT CONSTRAINT TIGHTNESS")
    print("=" * 80)

    N = len(f1s)

    # Individual constraints
    c_f1 = f1s >= 1.70
    c_omi = omi_counts >= KW_OMI_COUNT
    c_rep = repeats <= KW_REPEATS
    c_types = n_types >= KW_N_TYPES

    print(f"\n--- Individual constraint satisfaction ---")
    print(f"  f1 ≥ 1.70:         {c_f1.sum():>8} / {N} ({c_f1.mean()*100:.4f}%)")
    print(f"  OMI ≥ {KW_OMI_COUNT}:           {c_omi.sum():>8} / {N} ({c_omi.mean()*100:.4f}%)")
    print(f"  Repeats ≤ {KW_REPEATS}:        {c_rep.sum():>8} / {N} ({c_rep.mean()*100:.4f}%)")
    print(f"  Types ≥ {KW_N_TYPES}:          {c_types.sum():>8} / {N} ({c_types.mean()*100:.4f}%)")

    # Pairwise
    print(f"\n--- Pairwise constraint satisfaction ---")
    print(f"  f1 ∧ OMI:          {(c_f1 & c_omi).sum():>8} / {N} ({(c_f1 & c_omi).mean()*100:.4f}%)")
    print(f"  f1 ∧ Repeats:      {(c_f1 & c_rep).sum():>8} / {N} ({(c_f1 & c_rep).mean()*100:.4f}%)")
    print(f"  f1 ∧ Types:        {(c_f1 & c_types).sum():>8} / {N} ({(c_f1 & c_types).mean()*100:.4f}%)")
    print(f"  OMI ∧ Repeats:     {(c_omi & c_rep).sum():>8} / {N} ({(c_omi & c_rep).mean()*100:.4f}%)")

    # Triple
    print(f"\n--- Triple constraint satisfaction ---")
    c3a = c_f1 & c_omi & c_rep
    c3b = c_f1 & c_omi & c_types
    c3c = c_f1 & c_rep & c_types
    print(f"  f1 ∧ OMI ∧ Rep:    {c3a.sum():>8} / {N} ({c3a.mean()*100:.4f}%)")
    print(f"  f1 ∧ OMI ∧ Types:  {c3b.sum():>8} / {N} ({c3b.mean()*100:.4f}%)")
    print(f"  f1 ∧ Rep ∧ Types:  {c3c.sum():>8} / {N} ({c3c.mean()*100:.4f}%)")

    # All four
    c_all = c_f1 & c_omi & c_rep & c_types
    print(f"\n--- All four constraints ---")
    print(f"  f1 ∧ OMI ∧ Rep ∧ Types: {c_all.sum():>8} / {N} ({c_all.mean()*100:.4f}%)")

    # Tighter constraints
    print(f"\n--- Tighter constraints ---")
    c_f1_tight = f1s >= 1.75
    c_all_tight = c_f1_tight & c_omi & c_rep & c_types
    print(f"  f1 ≥ 1.75 ∧ OMI≥8 ∧ Rep≤2 ∧ Types=8: {c_all_tight.sum():>8} / {N} ({c_all_tight.mean()*100:.4f}%)")

    c_f1_exact = (f1s >= 1.75) & (f1s <= 1.80)
    c_exact = c_f1_exact & c_omi & c_rep & c_types
    print(f"  f1 ∈ [1.75,1.80] ∧ OMI≥8 ∧ Rep≤2 ∧ Types=8: {c_exact.sum():>8} / {N} ({c_exact.mean()*100:.4f}%)")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    f1s, omi_counts, repeats, n_types = computation_1()
    computation_2()
    computation_3()
    computation_4()
    computation_5()
    computation_6(f1s, omi_counts, repeats, n_types)

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
