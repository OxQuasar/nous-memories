"""
Round 4: Algebraic investigation — what produces subgroup bias?

Tests:
1. Characterize H = {id,O,MI,OMI} and verify M-I lock condition
2. Bridge kernel membership in H and pair-level properties
3. Greedy construction maximizing H-residence
4. All seven order-4 subgroups — which is KW most biased toward?
5. Bridge kernel determinism from pair identity
6. Two-canon structural test (Upper Canon pairs 0-14, Lower Canon pairs 15-31)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
from sequence import KING_WEN

import numpy as np
from collections import Counter

# ─── Constants & utilities ───────────────────────────────────────────────────

HEX_BITS = [h[2] for h in KING_WEN]
PAIRS = [(HEX_BITS[2*k], HEX_BITS[2*k+1]) for k in range(32)]
N_PAIRS = 32
N_BRIDGES = 31
N_TRANS = 30

KERNEL_NAMES = {
    (0,0,0): "id",  (1,0,0): "O",   (0,1,0): "M",   (0,0,1): "I",
    (1,1,0): "OM",  (1,0,1): "OI",  (0,1,1): "MI",  (1,1,1): "OMI",
}
NAME_ORDER = ["id", "O", "M", "I", "OM", "OI", "MI", "OMI"]
KERNEL_INDEX = {v: k for k, v in KERNEL_NAMES.items()}

PAIR_A = np.array([[int(c) for c in PAIRS[k][0]] for k in range(N_PAIRS)], dtype=np.int8)
PAIR_B = np.array([[int(c) for c in PAIRS[k][1]] for k in range(N_PAIRS)], dtype=np.int8)

# Subgroup H = {id, O, MI, OMI}: m-bit == i-bit
H = frozenset([(0,0,0), (1,0,0), (0,1,1), (1,1,1)])
H_COMPLEMENT = frozenset([(0,1,0), (0,0,1), (1,1,0), (1,0,1)])  # {M, I, OM, OI}

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def hamming3(a, b):
    return sum(x != y for x, y in zip(a, b))

def kernel_from_hex_strings(exit_h, entry_h):
    """Compute 3-bit kernel from two 6-bit hex strings."""
    mask = tuple(int(exit_h[i]) ^ int(entry_h[i]) for i in range(6))
    return (mask[5], mask[4], mask[3])

def compute_kernels(pairs_list):
    """31 kernel 3-tuples from 32 string pairs."""
    return [kernel_from_hex_strings(pairs_list[k][1], pairs_list[k+1][0])
            for k in range(len(pairs_list) - 1)]

def running_product(kernels):
    """Cumulative XOR sequence."""
    products = []
    r = (0, 0, 0)
    for k in kernels:
        r = xor3(r, k)
        products.append(r)
    return products

def subgroup_residence(products, subgroup):
    """Fraction of running product positions in the given subgroup."""
    return sum(1 for p in products if p in subgroup) / len(products)

# ─── KW baseline ────────────────────────────────────────────────────────────

KW_KERNELS = compute_kernels(PAIRS)
KW_PRODUCTS = running_product(KW_KERNELS)
KW_DISTS = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(N_TRANS)]
KW_F1 = np.mean(KW_DISTS)
KW_H_RESIDENCE = subgroup_residence(KW_PRODUCTS, H)

print(f"KW baseline: f1={KW_F1:.4f}, H-residence={KW_H_RESIDENCE:.4f} ({sum(1 for p in KW_PRODUCTS if p in H)}/31)")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: CHARACTERIZE H AND VERIFY M-I LOCK
# ═══════════════════════════════════════════════════════════════════════════════

def computation_1():
    print("\n" + "=" * 80)
    print("COMPUTATION 1: CHARACTERIZE H = {id, O, MI, OMI}")
    print("=" * 80)

    # Verify M-I lock characterization
    print(f"\n--- M-I lock verification ---")
    print(f"  H = {{id, O, MI, OMI}}")
    print(f"  For z = (o, m, i): z ∈ H ⟺ m == i")
    for elem in [(0,0,0), (1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1), (1,1,1)]:
        o, m, i = elem
        in_h = elem in H
        m_eq_i = (m == i)
        name = KERNEL_NAMES[elem]
        check = "✓" if in_h == m_eq_i else "✗"
        print(f"    {name:>5} = ({o},{m},{i}): m==i? {m_eq_i}, in H? {in_h} {check}")

    # Running product M-I lock positions
    print(f"\n--- Running product M-I lock in KW ---")
    lock_count = 0
    for idx, p in enumerate(KW_PRODUCTS):
        o, m, i = p
        locked = (m == i)
        if locked:
            lock_count += 1
        marker = "H" if locked else " "
        print(f"    B{idx+1:>2}: {KERNEL_NAMES[p]:>5} ({o},{m},{i})  m==i: {locked}  [{marker}]")
    print(f"\n  M-I locked positions: {lock_count}/31 = {lock_count/31:.4f}")

    # Physical meaning
    print(f"\n--- Physical meaning of H ---")
    print(f"  O = flip outer pair (L1,L6)")
    print(f"  M = flip middle pair (L2,L5)")
    print(f"  I = flip inner pair (L3,L4)")
    print(f"  H = {{id, O, MI, OMI}}: transformations where M and I agree")
    print(f"  = outer-pair axis is distinguished; middle+inner always flip together or not at all")
    print(f"  Complement of H: {{M, I, OM, OI}} = middle and inner flip independently")

    # Null: how often does M-I lock occur in random orderings?
    print(f"\n--- Null: M-I lock frequency (100,000 trials) ---")
    rng = np.random.default_rng(42)
    N_NULL = 100_000
    null_lock_counts = np.empty(N_NULL)

    for t in range(N_NULL):
        perm = rng.permutation(N_PAIRS)
        orient = rng.integers(0, 2, size=N_PAIRS)
        exits = np.empty((N_PAIRS, 6), dtype=np.int8)
        entries = np.empty((N_PAIRS, 6), dtype=np.int8)
        for k in range(N_PAIRS):
            pk = perm[k]
            if orient[k] == 0:
                entries[k] = PAIR_A[pk]; exits[k] = PAIR_B[pk]
            else:
                entries[k] = PAIR_B[pk]; exits[k] = PAIR_A[pk]
        masks = np.bitwise_xor(exits[:N_BRIDGES], entries[1:N_PAIRS])
        kerns = masks[:, [5, 4, 3]]
        # Running product
        rp = np.zeros(3, dtype=np.int8)
        count = 0
        for j in range(N_BRIDGES):
            rp = np.bitwise_xor(rp, kerns[j])
            if rp[1] == rp[2]:  # M-bit == I-bit
                count += 1
        null_lock_counts[t] = count

    print(f"  KW: {lock_count}/31")
    print(f"  Null: mean={null_lock_counts.mean():.2f} ± {null_lock_counts.std():.2f}")
    print(f"  KW percentile: {(null_lock_counts <= lock_count).mean()*100:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: BRIDGE KERNEL MEMBERSHIP IN H
# ═══════════════════════════════════════════════════════════════════════════════

def computation_2():
    print("\n" + "=" * 80)
    print("COMPUTATION 2: BRIDGE KERNEL MEMBERSHIP IN H")
    print("=" * 80)

    # How many bridge kernels are themselves in H?
    kw_in_h = [k for k in KW_KERNELS if k in H]
    kw_not_h = [k for k in KW_KERNELS if k not in H]
    print(f"\n--- Bridge kernels in H ---")
    print(f"  In H: {len(kw_in_h)}/31")
    in_h_names = Counter(KERNEL_NAMES[k] for k in kw_in_h)
    not_h_names = Counter(KERNEL_NAMES[k] for k in kw_not_h)
    print(f"  In H breakdown: {dict(sorted(in_h_names.items()))}")
    print(f"  Not in H breakdown: {dict(sorted(not_h_names.items()))}")

    # Per-position: which bridges have kernel in H?
    print(f"\n--- Bridge kernel H-membership by position ---")
    for idx, k in enumerate(KW_KERNELS):
        in_h = k in H
        pair_nums = (KING_WEN[2*idx+1][0], KING_WEN[2*(idx+1)][0])
        marker = "H" if in_h else " "
        print(f"    B{idx+1:>2}: {KERNEL_NAMES[k]:>5}  [{marker}]  "
              f"(exit hex {pair_nums[0]} → entry hex {pair_nums[1]})")

    # Position patterns: are H-kernels clustered?
    h_positions = [i for i, k in enumerate(KW_KERNELS) if k in H]
    not_h_positions = [i for i, k in enumerate(KW_KERNELS) if k not in H]
    first_half_h = sum(1 for p in h_positions if p < 15)
    second_half_h = sum(1 for p in h_positions if p >= 15)
    print(f"\n  H-kernels in first half (B1-B15): {first_half_h}")
    print(f"  H-kernels in second half (B16-B31): {second_half_h}")

    # Null: how many bridge kernels are in H for random orderings?
    print(f"\n--- Null: kernel H-membership (100,000 trials) ---")
    rng = np.random.default_rng(42)
    N_NULL = 100_000
    null_h_counts = np.empty(N_NULL, dtype=int)

    for t in range(N_NULL):
        perm = rng.permutation(N_PAIRS)
        orient = rng.integers(0, 2, size=N_PAIRS)
        exits = np.empty((N_PAIRS, 6), dtype=np.int8)
        entries = np.empty((N_PAIRS, 6), dtype=np.int8)
        for k in range(N_PAIRS):
            pk = perm[k]
            if orient[k] == 0:
                entries[k] = PAIR_A[pk]; exits[k] = PAIR_B[pk]
            else:
                entries[k] = PAIR_B[pk]; exits[k] = PAIR_A[pk]
        masks = np.bitwise_xor(exits[:N_BRIDGES], entries[1:N_PAIRS])
        kerns = masks[:, [5, 4, 3]]
        # Count kernels in H (m-bit == i-bit)
        null_h_counts[t] = (kerns[:, 1] == kerns[:, 2]).sum()

    print(f"  KW: {len(kw_in_h)}/31")
    print(f"  Null: mean={null_h_counts.mean():.2f} ± {null_h_counts.std():.2f}")
    print(f"  KW percentile: {(null_h_counts <= len(kw_in_h)).mean()*100:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: GREEDY CONSTRUCTION MAXIMIZING H-RESIDENCE
# ═══════════════════════════════════════════════════════════════════════════════

def computation_3():
    print("\n" + "=" * 80)
    print("COMPUTATION 3: GREEDY H-MAXIMIZING CONSTRUCTION")
    print("=" * 80)

    # Precompute: for every ordered pair of pair indices (i, j) and orientations (oi, oj),
    # what is the bridge kernel?
    # kernel[i][oi][j][oj] = kernel when pair i (orientation oi) is followed by pair j (orientation oj)
    # oi=0: entry=A,exit=B; oi=1: entry=B,exit=A
    # Bridge kernel = kernel_from_hex(exit_i, entry_j)

    kernel_table = {}  # (pair_i, orient_i, pair_j, orient_j) → kernel 3-tuple
    for i in range(N_PAIRS):
        for oi in range(2):
            exit_i = PAIRS[i][1] if oi == 0 else PAIRS[i][0]
            for j in range(N_PAIRS):
                if j == i:
                    continue
                for oj in range(2):
                    entry_j = PAIRS[j][0] if oj == 0 else PAIRS[j][1]
                    k = kernel_from_hex_strings(exit_i, entry_j)
                    kernel_table[(i, oi, j, oj)] = k

    def greedy_h_maximize(start_pair, start_orient, rng):
        """Greedy: at each step pick (pair, orient) to maximize running product staying in H.
        Tie-break by maximizing distance from previous kernel (f1 contribution)."""
        sequence = [(start_pair, start_orient)]
        used = {start_pair}
        kernels = []
        running = (0, 0, 0)

        for step in range(N_BRIDGES):
            prev_pair, prev_orient = sequence[-1]
            best_score = (-1, -1)
            best_choices = []

            for j in range(N_PAIRS):
                if j in used:
                    continue
                for oj in range(2):
                    k = kernel_table[(prev_pair, prev_orient, j, oj)]
                    new_running = xor3(running, k)
                    in_h = 1 if new_running in H else 0

                    # Tie-break: distance from previous kernel
                    dist = hamming3(kernels[-1], k) if kernels else 0

                    score = (in_h, dist)
                    if score > best_score:
                        best_score = score
                        best_choices = [(j, oj, k, new_running)]
                    elif score == best_score:
                        best_choices.append((j, oj, k, new_running))

            # Pick randomly among best
            choice = best_choices[rng.integers(len(best_choices))]
            j, oj, k, new_running = choice
            sequence.append((j, oj))
            used.add(j)
            kernels.append(k)
            running = new_running

        return kernels

    rng = np.random.default_rng(42)
    N_RESTARTS = 1000

    greedy_results = []
    for trial in range(N_RESTARTS):
        start_pair = rng.integers(N_PAIRS)
        start_orient = rng.integers(2)
        kernels = greedy_h_maximize(start_pair, start_orient, rng)
        products = running_product(kernels)
        h_res = subgroup_residence(products, H)
        dists = [hamming3(kernels[i], kernels[i+1]) for i in range(len(kernels)-1)]
        f1 = np.mean(dists) if dists else 0
        omi_count = sum(1 for i in range(len(kernels)-1) if hamming3(kernels[i], kernels[i+1]) == 3)
        repeats = sum(1 for d in dists if d == 0)
        n_types = len(set(kernels))
        greedy_results.append({
            'h_res': h_res, 'f1': f1, 'omi': omi_count,
            'repeats': repeats, 'n_types': n_types
        })

    h_res_arr = np.array([r['h_res'] for r in greedy_results])
    f1_arr = np.array([r['f1'] for r in greedy_results])
    omi_arr = np.array([r['omi'] for r in greedy_results])
    rep_arr = np.array([r['repeats'] for r in greedy_results])
    types_arr = np.array([r['n_types'] for r in greedy_results])

    print(f"\n--- Greedy H-maximizing results ({N_RESTARTS} restarts) ---")
    print(f"  H-residence: mean={h_res_arr.mean():.4f} ± {h_res_arr.std():.4f}, "
          f"min={h_res_arr.min():.4f}, max={h_res_arr.max():.4f}")
    print(f"  f1:           mean={f1_arr.mean():.4f} ± {f1_arr.std():.4f}, "
          f"min={f1_arr.min():.4f}, max={f1_arr.max():.4f}")
    print(f"  OMI count:    mean={omi_arr.mean():.2f} ± {omi_arr.std():.2f}")
    print(f"  Repeats:      mean={rep_arr.mean():.2f} ± {rep_arr.std():.2f}")
    print(f"  Types:        mean={types_arr.mean():.2f} ± {types_arr.std():.2f}")

    print(f"\n  KW comparison:")
    print(f"    KW H-residence: {KW_H_RESIDENCE:.4f}")
    print(f"    KW f1:          {KW_F1:.4f}")
    print(f"    KW OMI:         {sum(1 for d in KW_DISTS if d == 3)}")
    print(f"    KW repeats:     {sum(1 for d in KW_DISTS if d == 0)}")
    print(f"    KW types:       {len(set(KW_KERNELS))}")

    # Does H-optimization naturally produce high f1?
    # Correlation within greedy results
    if len(greedy_results) > 1:
        corr_h_f1 = np.corrcoef(h_res_arr, f1_arr)[0, 1]
        print(f"\n  Correlation r(H-res, f1) in greedy results: {corr_h_f1:.4f}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: ALL SEVEN ORDER-4 SUBGROUPS
# ═══════════════════════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 80)
    print("COMPUTATION 4: ALL SEVEN ORDER-4 SUBGROUPS")
    print("=" * 80)

    # Enumerate all order-4 subgroups of Z₂³
    all_elems = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
    id_elem = (0, 0, 0)

    subgroups = []
    seen = set()
    for i, g1 in enumerate(all_elems):
        if g1 == id_elem:
            continue
        for g2 in all_elems[i+1:]:
            if g2 == id_elem or g2 == g1:
                continue
            g3 = xor3(g1, g2)
            sg = frozenset([id_elem, g1, g2, g3])
            if len(sg) == 4 and sg not in seen:
                seen.add(sg)
                subgroups.append(sg)

    print(f"\n  Found {len(subgroups)} order-4 subgroups")

    # For each subgroup: KW residence + null distribution
    rng = np.random.default_rng(42)
    N_NULL = 100_000

    # Pre-generate null running products
    null_products = []  # list of (31,3) arrays
    for t in range(N_NULL):
        perm = rng.permutation(N_PAIRS)
        orient = rng.integers(0, 2, size=N_PAIRS)
        exits = np.empty((N_PAIRS, 6), dtype=np.int8)
        entries = np.empty((N_PAIRS, 6), dtype=np.int8)
        for k in range(N_PAIRS):
            pk = perm[k]
            if orient[k] == 0:
                entries[k] = PAIR_A[pk]; exits[k] = PAIR_B[pk]
            else:
                entries[k] = PAIR_B[pk]; exits[k] = PAIR_A[pk]
        masks = np.bitwise_xor(exits[:N_BRIDGES], entries[1:N_PAIRS])
        kerns = masks[:, [5, 4, 3]]
        # Running product
        rp = np.cumsum(kerns, axis=0) % 2  # cumulative XOR
        null_products.append(rp)

    print(f"\n  {'Subgroup':>35} {'KW res':>8} {'KW/31':>6} {'Null mean':>10} {'Null std':>9} {'Pctile':>8}")
    print("  " + "-" * 80)

    results = []
    for sg in subgroups:
        # Subgroup name
        names = sorted([KERNEL_NAMES[e] for e in sg])
        sg_name = "{" + ", ".join(names) + "}"

        # KW residence
        kw_count = sum(1 for p in KW_PRODUCTS if p in sg)
        kw_res = kw_count / N_BRIDGES

        # Null: for each trial, count running product in this subgroup
        null_counts = np.empty(N_NULL)
        # Subgroup membership test: encode as a set of 3-bit tuples
        for t in range(N_NULL):
            rp = null_products[t]
            count = 0
            for j in range(N_BRIDGES):
                elem = (int(rp[j, 0]), int(rp[j, 1]), int(rp[j, 2]))
                if elem in sg:
                    count += 1
            null_counts[t] = count / N_BRIDGES

        pctile = (null_counts <= kw_res).mean() * 100
        results.append((sg_name, kw_res, kw_count, null_counts.mean(), null_counts.std(), pctile))
        print(f"  {sg_name:>35} {kw_res:>8.4f} {kw_count:>3}/31 "
              f"{null_counts.mean():>10.4f} {null_counts.std():>9.4f} {pctile:>7.2f}%")

    # Which subgroup has highest KW percentile?
    best = max(results, key=lambda x: x[5])
    print(f"\n  Most biased subgroup: {best[0]} (percentile: {best[5]:.2f}%)")

    # Which has highest absolute residence?
    best_abs = max(results, key=lambda x: x[1])
    print(f"  Highest residence: {best_abs[0]} ({best_abs[1]:.4f})")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 5: BRIDGE KERNEL DETERMINISM FROM PAIR IDENTITY
# ═══════════════════════════════════════════════════════════════════════════════

def computation_5():
    print("\n" + "=" * 80)
    print("COMPUTATION 5: BRIDGE KERNEL FROM PAIR IDENTITY")
    print("=" * 80)

    # For each pair of pair indices (i, j), what kernels are possible
    # given the 4 orientation combinations?
    h_possible_count = 0
    h_forced_count = 0
    total_pair_pairs = 0

    # Detailed table for a sample
    print(f"\n--- Kernel options per pair-pair (first 10 pair transitions) ---")
    print(f"  {'Pair i':>6} {'Pair j':>6} {'(0,0)':>6} {'(0,1)':>6} {'(1,0)':>6} {'(1,1)':>6} {'All H?':>7} {'Any H?':>7}")

    for display_idx, bridge_idx in enumerate(range(min(10, N_BRIDGES))):
        i = bridge_idx
        j = bridge_idx + 1
        kernels_4 = []
        for oi in range(2):
            for oj in range(2):
                exit_h = PAIRS[i][1] if oi == 0 else PAIRS[i][0]
                entry_h = PAIRS[j][0] if oj == 0 else PAIRS[j][1]
                k = kernel_from_hex_strings(exit_h, entry_h)
                kernels_4.append(k)
        names = [KERNEL_NAMES[k] for k in kernels_4]
        all_h = all(k in H for k in kernels_4)
        any_h = any(k in H for k in kernels_4)
        i_nums = f"({KING_WEN[2*i][0]},{KING_WEN[2*i+1][0]})"
        j_nums = f"({KING_WEN[2*j][0]},{KING_WEN[2*j+1][0]})"
        print(f"  {i_nums:>6} {j_nums:>6} {names[0]:>6} {names[1]:>6} {names[2]:>6} {names[3]:>6} "
              f"{'yes' if all_h else 'no':>7} {'yes' if any_h else 'no':>7}")

    # Full analysis: for ALL possible pair-pair combinations
    print(f"\n--- Full analysis: all 32×31 pair-pair combinations ---")

    all_h_count = 0
    any_h_count = 0
    none_h_count = 0
    total = 0

    # Distribution of how many of the 4 orientations produce H-kernel
    orient_h_dist = Counter()  # how many of 4 orientations give H-kernel

    for i in range(N_PAIRS):
        for j in range(N_PAIRS):
            if i == j:
                continue
            total += 1
            kernels_4 = []
            for oi in range(2):
                for oj in range(2):
                    exit_h = PAIRS[i][1] if oi == 0 else PAIRS[i][0]
                    entry_h = PAIRS[j][0] if oj == 0 else PAIRS[j][1]
                    k = kernel_from_hex_strings(exit_h, entry_h)
                    kernels_4.append(k)
            n_in_h = sum(1 for k in kernels_4 if k in H)
            orient_h_dist[n_in_h] += 1
            if n_in_h == 4:
                all_h_count += 1
            if n_in_h > 0:
                any_h_count += 1
            if n_in_h == 0:
                none_h_count += 1

    print(f"  Total pair-pair combinations: {total}")
    print(f"  All 4 orientations → H-kernel: {all_h_count} ({all_h_count/total*100:.1f}%)")
    print(f"  At least 1 orientation → H-kernel: {any_h_count} ({any_h_count/total*100:.1f}%)")
    print(f"  No orientation → H-kernel: {none_h_count} ({none_h_count/total*100:.1f}%)")
    print(f"\n  Distribution of H-kernel count per pair-pair (out of 4 orientations):")
    for n in sorted(orient_h_dist):
        print(f"    {n}/4: {orient_h_dist[n]:>4} ({orient_h_dist[n]/total*100:.1f}%)")

    # For the actual KW adjacent pairs: how constrained are the kernels?
    print(f"\n--- KW adjacent pair kernel constraints ---")
    print(f"  {'Bridge':>6} {'Pairs':>12} {'KW kernel':>10} {'H?':>4} {'#H options':>10} {'#options':>8}")
    kw_forced_h = 0
    for bridge_idx in range(N_BRIDGES):
        i = bridge_idx
        j = bridge_idx + 1
        # KW orientation: oi=0, oj=0 (original order)
        kw_kernel = KW_KERNELS[bridge_idx]
        kernels_4 = []
        for oi in range(2):
            for oj in range(2):
                exit_h = PAIRS[i][1] if oi == 0 else PAIRS[i][0]
                entry_h = PAIRS[j][0] if oj == 0 else PAIRS[j][1]
                k = kernel_from_hex_strings(exit_h, entry_h)
                kernels_4.append(k)
        n_in_h = sum(1 for k in kernels_4 if k in H)
        n_distinct = len(set(kernels_4))
        forced = (n_in_h == 4)
        if forced:
            kw_forced_h += 1
        i_nums = f"({KING_WEN[2*i][0]},{KING_WEN[2*i+1][0]})"
        j_nums = f"({KING_WEN[2*j][0]},{KING_WEN[2*j+1][0]})"
        print(f"  {bridge_idx+1:>6} {i_nums+'→'+j_nums:>12} "
              f"{KERNEL_NAMES[kw_kernel]:>10} {'H' if kw_kernel in H else ' ':>4} "
              f"{n_in_h:>10} {n_distinct:>8}")
    print(f"\n  Bridges where H-kernel is FORCED (all 4 orientations → H): {kw_forced_h}/31")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 6: TWO-CANON STRUCTURAL TEST
# ═══════════════════════════════════════════════════════════════════════════════

def computation_6():
    print("\n" + "=" * 80)
    print("COMPUTATION 6: TWO-CANON STRUCTURAL TEST")
    print("=" * 80)

    # Upper Canon: pairs 0-14 (hexagrams 1-30), 15 pairs, 14 internal bridges (B1-B14)
    # Bridge B15 connects the two canons
    # Lower Canon: pairs 15-31 (hexagrams 31-64), 17 pairs, 16 internal bridges (B16-B31)

    UPPER_BRIDGES = list(range(0, 14))   # bridges 0..13 (B1..B14)
    CROSS_BRIDGE = 14                     # bridge 14 (B15)
    LOWER_BRIDGES = list(range(15, 31))   # bridges 15..30 (B16..B31)

    print(f"\n--- Canon structure ---")
    print(f"  Upper Canon: pairs 0-14, bridges B1-B14 ({len(UPPER_BRIDGES)} bridges)")
    print(f"  Cross-canon bridge: B15")
    print(f"  Lower Canon: pairs 15-31, bridges B16-B31 ({len(LOWER_BRIDGES)} bridges)")

    # Kernels per canon
    upper_kernels = [KW_KERNELS[i] for i in UPPER_BRIDGES]
    lower_kernels = [KW_KERNELS[i] for i in LOWER_BRIDGES]
    cross_kernel = KW_KERNELS[CROSS_BRIDGE]

    print(f"\n  Cross-canon bridge kernel: {KERNEL_NAMES[cross_kernel]}")

    # f1 per canon
    if len(upper_kernels) >= 2:
        upper_dists = [hamming3(upper_kernels[i], upper_kernels[i+1]) for i in range(len(upper_kernels)-1)]
        upper_f1 = np.mean(upper_dists)
    else:
        upper_f1 = 0
        upper_dists = []

    if len(lower_kernels) >= 2:
        lower_dists = [hamming3(lower_kernels[i], lower_kernels[i+1]) for i in range(len(lower_kernels)-1)]
        lower_f1 = np.mean(lower_dists)
    else:
        lower_f1 = 0
        lower_dists = []

    print(f"\n--- f1 per canon ---")
    print(f"  Upper: {upper_f1:.4f} ({len(upper_dists)} transitions)")
    print(f"  Lower: {lower_f1:.4f} ({len(lower_dists)} transitions)")
    print(f"  Full:  {KW_F1:.4f} (30 transitions)")

    # OMI count per canon
    upper_omi = sum(1 for d in upper_dists if d == 3) if upper_dists else 0
    lower_omi = sum(1 for d in lower_dists if d == 3) if lower_dists else 0
    full_omi = sum(1 for d in KW_DISTS if d == 3)
    # Also count OMI deltas (which are at the transition level, not the canon-internal level)
    # OMI deltas = distance-3 consecutive kernel pairs
    print(f"\n--- OMI count per canon ---")
    print(f"  Upper (13 delta positions): {upper_omi}")
    print(f"  Lower (15 delta positions): {lower_omi}")
    print(f"  Full (30 delta positions): {full_omi}")

    # Kernel type distributions per canon
    print(f"\n--- Kernel type distribution per canon ---")
    upper_freq = Counter(KERNEL_NAMES[k] for k in upper_kernels)
    lower_freq = Counter(KERNEL_NAMES[k] for k in lower_kernels)
    full_freq = Counter(KERNEL_NAMES[k] for k in KW_KERNELS)

    print(f"  {'Type':>5} {'Upper (14)':>10} {'Lower (16)':>10} {'Cross':>6} {'Full (31)':>10}")
    for name in NAME_ORDER:
        u = upper_freq.get(name, 0)
        l = lower_freq.get(name, 0)
        c = 1 if KERNEL_NAMES[cross_kernel] == name else 0
        f = full_freq.get(name, 0)
        print(f"  {name:>5} {u:>10} {l:>10} {c:>6} {f:>10}")

    # H-membership per canon
    upper_h = sum(1 for k in upper_kernels if k in H)
    lower_h = sum(1 for k in lower_kernels if k in H)
    cross_h = 1 if cross_kernel in H else 0
    print(f"\n--- Kernel H-membership per canon ---")
    print(f"  Upper: {upper_h}/{len(upper_kernels)} ({upper_h/len(upper_kernels)*100:.1f}%)")
    print(f"  Lower: {lower_h}/{len(lower_kernels)} ({lower_h/len(lower_kernels)*100:.1f}%)")
    print(f"  Cross: {'H' if cross_h else 'not H'} ({KERNEL_NAMES[cross_kernel]})")
    print(f"  Full:  {sum(1 for k in KW_KERNELS if k in H)}/{N_BRIDGES}")

    # Subgroup residence per canon
    # Running product for upper canon only (first 14 bridges)
    upper_products = running_product(upper_kernels)
    upper_h_res = subgroup_residence(upper_products, H)

    # Running product for lower canon only (bridges 16-31, resetting running product)
    lower_products = running_product(lower_kernels)
    lower_h_res = subgroup_residence(lower_products, H)

    # Running product for lower canon CONTINUING from upper (not resetting)
    full_products = running_product(KW_KERNELS)
    lower_full_products = full_products[15:]  # after bridge 15 (cross bridge)
    lower_full_h_res = sum(1 for p in lower_full_products if p in H) / len(lower_full_products)

    print(f"\n--- Running product H-residence per canon ---")
    print(f"  Upper (reset, 14 positions): {upper_h_res:.4f} ({sum(1 for p in upper_products if p in H)}/{len(upper_products)})")
    print(f"  Lower (reset, 16 positions): {lower_h_res:.4f} ({sum(1 for p in lower_products if p in H)}/{len(lower_products)})")
    print(f"  Lower (continuing, 16 positions): {lower_full_h_res:.4f} ({sum(1 for p in lower_full_products if p in H)}/{len(lower_full_products)})")
    print(f"  Full (31 positions): {KW_H_RESIDENCE:.4f}")

    # Is the subgroup bias concentrated in one canon?
    print(f"\n--- Summary ---")
    if upper_h_res > lower_h_res + 0.1:
        print(f"  Subgroup bias concentrated in UPPER canon ({upper_h_res:.3f} vs {lower_h_res:.3f})")
    elif lower_h_res > upper_h_res + 0.1:
        print(f"  Subgroup bias concentrated in LOWER canon ({lower_h_res:.3f} vs {upper_h_res:.3f})")
    else:
        print(f"  Subgroup bias roughly balanced between canons ({upper_h_res:.3f} vs {lower_h_res:.3f})")

    if upper_omi > lower_omi + 2:
        print(f"  OMI deltas concentrated in UPPER canon ({upper_omi} vs {lower_omi})")
    elif lower_omi > upper_omi + 2:
        print(f"  OMI deltas concentrated in LOWER canon ({lower_omi} vs {upper_omi})")
    else:
        print(f"  OMI deltas roughly balanced ({upper_omi} vs {lower_omi})")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    computation_1()
    computation_2()
    computation_3()
    computation_4()
    computation_5()
    computation_6()

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
