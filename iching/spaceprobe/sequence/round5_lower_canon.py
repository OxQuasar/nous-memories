"""
Round 5: Two targeted tests.

1. Joint constraint tightness of f1 + H-residence (including per-canon)
2. What does the Lower Canon optimize? (trigram continuity, weight smoothness,
   raw Hamming, trigram balance)
3. Trigram-level bridge transitions: symmetry between entry/exit
4. Trigram-reverse proximity test
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
from sequence import KING_WEN, TRIGRAMS, trigram_name

import numpy as np
from collections import Counter

# ─── Constants & utilities ───────────────────────────────────────────────────

HEX_BITS = [h[2] for h in KING_WEN]
N_HEX = 64
PAIRS = [(HEX_BITS[2*k], HEX_BITS[2*k+1]) for k in range(32)]
N_PAIRS = 32
N_BRIDGES = 31

PAIR_A = np.array([[int(c) for c in PAIRS[k][0]] for k in range(N_PAIRS)], dtype=np.int8)
PAIR_B = np.array([[int(c) for c in PAIRS[k][1]] for k in range(N_PAIRS)], dtype=np.int8)

# H = {id, O, MI, OMI}: m-bit == i-bit in kernel (o,m,i)
H = frozenset([(0,0,0), (1,0,0), (0,1,1), (1,1,1)])

KERNEL_NAMES = {
    (0,0,0): "id",  (1,0,0): "O",   (0,1,0): "M",   (0,0,1): "I",
    (1,1,0): "OM",  (1,0,1): "OI",  (0,1,1): "MI",  (1,1,1): "OMI",
}

# Canon boundaries
UPPER_CANON_PAIRS = range(0, 15)   # pairs 0-14 → bridges 0-13 (B1-B14)
CROSS_BRIDGE = 14                   # bridge 14 (B15)
LOWER_CANON_PAIRS = range(15, 32)  # pairs 15-31 → bridges 15-30 (B16-B31)

def xor3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def hamming3(a, b):
    return sum(x != y for x, y in zip(a, b))

def hamming6_str(a, b):
    """Hamming distance between two 6-bit strings."""
    return sum(a[i] != b[i] for i in range(6))

def yang_count(hex_str):
    """Number of yang lines (1s) in a hexagram string."""
    return sum(int(c) for c in hex_str)

def lower_trig(hex_str):
    return hex_str[:3]

def upper_trig(hex_str):
    return hex_str[3:]

def kernel_bits(exit_h, entry_h):
    mask = tuple(int(exit_h[i]) ^ int(entry_h[i]) for i in range(6))
    return (mask[5], mask[4], mask[3])

def compute_kernels(pairs_list):
    return [kernel_bits(pairs_list[k][1], pairs_list[k+1][0])
            for k in range(len(pairs_list) - 1)]

def running_product(kernels):
    products = []
    r = (0, 0, 0)
    for k in kernels:
        r = xor3(r, k)
        products.append(r)
    return products

def h_residence_count(products):
    return sum(1 for p in products if p in H)

# ─── KW baseline ────────────────────────────────────────────────────────────

KW_KERNELS = compute_kernels(PAIRS)
KW_PRODUCTS = running_product(KW_KERNELS)
KW_DISTS = [hamming3(KW_KERNELS[i], KW_KERNELS[i+1]) for i in range(30)]
KW_F1 = np.mean(KW_DISTS)
KW_H_COUNT = h_residence_count(KW_PRODUCTS)
KW_H_RES = KW_H_COUNT / N_BRIDGES

print(f"KW baseline: f1={KW_F1:.4f}, H-residence={KW_H_COUNT}/31={KW_H_RES:.4f}")

# ─── Shared MC helper ───────────────────────────────────────────────────────

def random_trial_metrics(rng):
    """One random trial. Returns dict of metrics."""
    perm = rng.permutation(N_PAIRS)
    orient = rng.integers(0, 2, size=N_PAIRS)

    # Build ordered pairs (as string tuples for trigram analysis)
    ordered_pairs = []
    exits_np = np.empty((N_PAIRS, 6), dtype=np.int8)
    entries_np = np.empty((N_PAIRS, 6), dtype=np.int8)
    for k in range(N_PAIRS):
        pk = perm[k]
        if orient[k] == 0:
            entries_np[k] = PAIR_A[pk]; exits_np[k] = PAIR_B[pk]
            ordered_pairs.append((PAIRS[pk][0], PAIRS[pk][1]))
        else:
            entries_np[k] = PAIR_B[pk]; exits_np[k] = PAIR_A[pk]
            ordered_pairs.append((PAIRS[pk][1], PAIRS[pk][0]))

    # Full sequence kernels
    masks = np.bitwise_xor(exits_np[:N_BRIDGES], entries_np[1:N_PAIRS])
    kerns = masks[:, [5, 4, 3]]  # (31, 3)

    # f1
    diffs = np.bitwise_xor(kerns[:30], kerns[1:31])
    full_dists = diffs.sum(axis=1)
    f1 = full_dists.mean()

    # H-residence (running product)
    rp = np.cumsum(kerns, axis=0) % 2
    h_count = (rp[:, 1] == rp[:, 2]).sum()  # m-bit == i-bit

    # Repeats & types
    k_ids = kerns[:, 0] * 4 + kerns[:, 1] * 2 + kerns[:, 2]
    repeats = (full_dists == 0).sum()
    n_types = len(np.unique(k_ids))

    # OMI count
    omi_count = (full_dists == 3).sum()

    # --- Per-canon metrics ---
    # Upper canon: first 15 pairs → bridges 0..13 (14 bridges)
    upper_kerns = kerns[:14]
    if upper_kerns.shape[0] >= 2:
        upper_diffs = np.bitwise_xor(upper_kerns[:13], upper_kerns[1:14])
        upper_f1 = upper_diffs.sum(axis=1).mean()
    else:
        upper_f1 = 0.0
    upper_rp = np.cumsum(upper_kerns, axis=0) % 2
    upper_h = (upper_rp[:, 1] == upper_rp[:, 2]).sum()

    # Lower canon: last 17 pairs → bridges 15..30 (16 bridges)
    lower_kerns = kerns[15:]
    if lower_kerns.shape[0] >= 2:
        lower_diffs = np.bitwise_xor(lower_kerns[:15], lower_kerns[1:16])
        lower_f1 = lower_diffs.sum(axis=1).mean()
    else:
        lower_f1 = 0.0
    # Lower canon running product (reset)
    lower_rp = np.cumsum(lower_kerns, axis=0) % 2
    lower_h = (lower_rp[:, 1] == lower_rp[:, 2]).sum()

    # --- Lower canon hex-level metrics ---
    # Lower canon bridges: exit of pair k → entry of pair k+1, for k=15..30
    lc_trig_cont = 0  # trigram continuity: count matching trigram slots
    lc_weight_delta = 0  # sum of |w(exit) - w(entry)|
    lc_hamming = 0  # sum of raw 6-bit Hamming distance
    lc_n_bridges = 0

    # Upper canon hex-level metrics
    uc_trig_cont = 0
    uc_weight_delta = 0
    uc_hamming = 0
    uc_n_bridges = 0

    for bridge_k in range(N_BRIDGES):
        exit_hex = ordered_pairs[bridge_k][1]
        entry_hex = ordered_pairs[bridge_k + 1][0]

        tc = 0
        if lower_trig(exit_hex) == lower_trig(entry_hex): tc += 1
        if upper_trig(exit_hex) == upper_trig(entry_hex): tc += 1

        wd = abs(yang_count(exit_hex) - yang_count(entry_hex))
        hd = hamming6_str(exit_hex, entry_hex)

        if bridge_k < 14:  # Upper canon internal bridges
            uc_trig_cont += tc
            uc_weight_delta += wd
            uc_hamming += hd
            uc_n_bridges += 1
        elif bridge_k >= 15:  # Lower canon internal bridges
            lc_trig_cont += tc
            lc_weight_delta += wd
            lc_hamming += hd
            lc_n_bridges += 1

    uc_mean_tc = uc_trig_cont / uc_n_bridges if uc_n_bridges > 0 else 0
    lc_mean_tc = lc_trig_cont / lc_n_bridges if lc_n_bridges > 0 else 0
    uc_mean_wd = uc_weight_delta / uc_n_bridges if uc_n_bridges > 0 else 0
    lc_mean_wd = lc_weight_delta / lc_n_bridges if lc_n_bridges > 0 else 0
    uc_mean_hd = uc_hamming / uc_n_bridges if uc_n_bridges > 0 else 0
    lc_mean_hd = lc_hamming / lc_n_bridges if lc_n_bridges > 0 else 0

    return {
        'f1': f1, 'h_count': int(h_count), 'repeats': int(repeats),
        'n_types': int(n_types), 'omi': int(omi_count),
        'upper_f1': upper_f1, 'upper_h': int(upper_h),
        'lower_f1': lower_f1, 'lower_h': int(lower_h),
        'uc_trig_cont': uc_mean_tc, 'lc_trig_cont': lc_mean_tc,
        'uc_weight_delta': uc_mean_wd, 'lc_weight_delta': lc_mean_wd,
        'uc_hamming': uc_mean_hd, 'lc_hamming': lc_mean_hd,
    }

# ─── KW per-canon hex-level metrics ─────────────────────────────────────────

def kw_canon_metrics():
    """Compute KW hex-level metrics for both canons."""
    results = {}
    for canon_name, bridge_range in [("upper", range(0, 14)), ("lower", range(15, 31))]:
        tc = 0; wd = 0; hd = 0; n = 0
        for bk in bridge_range:
            exit_hex = PAIRS[bk][1]
            entry_hex = PAIRS[bk + 1][0]
            if lower_trig(exit_hex) == lower_trig(entry_hex): tc += 1
            if upper_trig(exit_hex) == upper_trig(entry_hex): tc += 1
            wd += abs(yang_count(exit_hex) - yang_count(entry_hex))
            hd += hamming6_str(exit_hex, entry_hex)
            n += 1
        results[canon_name] = {
            'trig_cont': tc / n, 'weight_delta': wd / n, 'hamming': hd / n, 'n': n
        }
    return results

KW_CANON = kw_canon_metrics()

# Upper canon f1 and H
upper_kernels = KW_KERNELS[:14]
upper_dists = [hamming3(upper_kernels[i], upper_kernels[i+1]) for i in range(13)]
KW_UPPER_F1 = np.mean(upper_dists)
upper_products = running_product(upper_kernels)
KW_UPPER_H = h_residence_count(upper_products)

lower_kernels = KW_KERNELS[15:]
lower_dists = [hamming3(lower_kernels[i], lower_kernels[i+1]) for i in range(15)]
KW_LOWER_F1 = np.mean(lower_dists)
lower_products = running_product(lower_kernels)
KW_LOWER_H = h_residence_count(lower_products)

print(f"Upper Canon: f1={KW_UPPER_F1:.4f}, H={KW_UPPER_H}/14, tc={KW_CANON['upper']['trig_cont']:.4f}, wd={KW_CANON['upper']['weight_delta']:.4f}, hd={KW_CANON['upper']['hamming']:.4f}")
print(f"Lower Canon: f1={KW_LOWER_F1:.4f}, H={KW_LOWER_H}/16, tc={KW_CANON['lower']['trig_cont']:.4f}, wd={KW_CANON['lower']['weight_delta']:.4f}, hd={KW_CANON['lower']['hamming']:.4f}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: JOINT CONSTRAINT TIGHTNESS
# ═══════════════════════════════════════════════════════════════════════════════

def computation_1():
    print("\n" + "=" * 80)
    print("COMPUTATION 1: JOINT CONSTRAINT TIGHTNESS (1M trials)")
    print("=" * 80)

    rng = np.random.default_rng(42)
    N = 1_000_000

    f1s = np.empty(N)
    h_counts = np.empty(N, dtype=int)
    reps = np.empty(N, dtype=int)
    types = np.empty(N, dtype=int)
    omis = np.empty(N, dtype=int)
    upper_f1s = np.empty(N)
    upper_hs = np.empty(N, dtype=int)
    lower_f1s = np.empty(N)
    lower_hs = np.empty(N, dtype=int)

    for t in range(N):
        m = random_trial_metrics(rng)
        f1s[t] = m['f1']
        h_counts[t] = m['h_count']
        reps[t] = m['repeats']
        types[t] = m['n_types']
        omis[t] = m['omi']
        upper_f1s[t] = m['upper_f1']
        upper_hs[t] = m['upper_h']
        lower_f1s[t] = m['lower_f1']
        lower_hs[t] = m['lower_h']
        if (t + 1) % 200_000 == 0:
            print(f"  ... {t+1}/{N}")

    h_res = h_counts / N_BRIDGES

    # Correlation
    corr = np.corrcoef(f1s, h_res)[0, 1]
    print(f"\n--- Correlation ---")
    print(f"  Pearson r(f1, H-residence) = {corr:.4f}")

    # Joint distribution
    c_f1 = f1s >= 1.70
    c_h = h_counts >= KW_H_COUNT
    c_rep = reps <= 2
    c_type = types >= 8
    c_omi = omis >= 8

    print(f"\n--- Individual constraints ---")
    print(f"  f1 ≥ 1.70:       {c_f1.sum():>8} ({c_f1.mean()*100:.4f}%)")
    print(f"  H-res ≥ 20/31:   {c_h.sum():>8} ({c_h.mean()*100:.4f}%)")
    print(f"  Repeats ≤ 2:     {c_rep.sum():>8} ({c_rep.mean()*100:.4f}%)")
    print(f"  Types ≥ 8:       {c_type.sum():>8} ({c_type.mean()*100:.4f}%)")

    print(f"\n--- Pairwise constraints ---")
    print(f"  f1 ∧ H-res:      {(c_f1 & c_h).sum():>8} ({(c_f1 & c_h).mean()*100:.4f}%)")
    prod = c_f1.mean() * c_h.mean()
    print(f"  Product of marginals: {prod*100:.4f}%")
    print(f"  Ratio (joint/product): {(c_f1 & c_h).mean() / prod:.4f}" if prod > 0 else "  (zero product)")

    print(f"\n--- Progressive constraints ---")
    c2 = c_f1 & c_h
    c3 = c2 & c_rep
    c4 = c3 & c_type
    c5 = c4 & c_omi
    print(f"  f1 ∧ H-res:                     {c2.sum():>8} ({c2.mean()*100:.4f}%)")
    print(f"  f1 ∧ H-res ∧ Rep≤2:             {c3.sum():>8} ({c3.mean()*100:.4f}%)")
    print(f"  f1 ∧ H-res ∧ Rep≤2 ∧ Types=8:   {c4.sum():>8} ({c4.mean()*100:.4f}%)")
    print(f"  + OMI≥8:                         {c5.sum():>8} ({c5.mean()*100:.4f}%)")

    # Per-canon analysis
    print(f"\n--- Upper Canon percentiles ---")
    print(f"  KW upper f1 = {KW_UPPER_F1:.4f}, percentile: {(upper_f1s <= KW_UPPER_F1).mean()*100:.2f}%")
    print(f"  KW upper H = {KW_UPPER_H}/14, percentile: {(upper_hs <= KW_UPPER_H).mean()*100:.2f}%")
    print(f"  Upper f1: null mean={upper_f1s.mean():.4f} ± {upper_f1s.std():.4f}")
    print(f"  Upper H:  null mean={upper_hs.mean():.2f} ± {upper_hs.std():.2f}")

    print(f"\n--- Lower Canon percentiles ---")
    print(f"  KW lower f1 = {KW_LOWER_F1:.4f}, percentile: {(lower_f1s <= KW_LOWER_F1).mean()*100:.2f}%")
    print(f"  KW lower H = {KW_LOWER_H}/16, percentile: {(lower_hs <= KW_LOWER_H).mean()*100:.2f}%")
    print(f"  Lower f1: null mean={lower_f1s.mean():.4f} ± {lower_f1s.std():.4f}")
    print(f"  Lower H:  null mean={lower_hs.mean():.2f} ± {lower_hs.std():.2f}")

    return f1s, h_counts, reps, types, omis, upper_f1s, upper_hs, lower_f1s, lower_hs

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: WHAT DOES THE LOWER CANON OPTIMIZE?
# ═══════════════════════════════════════════════════════════════════════════════

def computation_2():
    print("\n" + "=" * 80)
    print("COMPUTATION 2: WHAT DOES THE LOWER CANON OPTIMIZE?")
    print("=" * 80)

    rng = np.random.default_rng(123)
    N = 100_000

    null_uc_tc = np.empty(N)
    null_lc_tc = np.empty(N)
    null_uc_wd = np.empty(N)
    null_lc_wd = np.empty(N)
    null_uc_hd = np.empty(N)
    null_lc_hd = np.empty(N)

    for t in range(N):
        m = random_trial_metrics(rng)
        null_uc_tc[t] = m['uc_trig_cont']
        null_lc_tc[t] = m['lc_trig_cont']
        null_uc_wd[t] = m['uc_weight_delta']
        null_lc_wd[t] = m['lc_weight_delta']
        null_uc_hd[t] = m['uc_hamming']
        null_lc_hd[t] = m['lc_hamming']
        if (t + 1) % 20_000 == 0:
            print(f"  ... {t+1}/{N}")

    kw_uc = KW_CANON['upper']
    kw_lc = KW_CANON['lower']

    print(f"\n--- a. Trigram continuity (mean matching trigram slots per bridge) ---")
    print(f"  Upper Canon:")
    print(f"    KW:   {kw_uc['trig_cont']:.4f}")
    print(f"    Null: {null_uc_tc.mean():.4f} ± {null_uc_tc.std():.4f}")
    print(f"    Pctile: {(null_uc_tc <= kw_uc['trig_cont']).mean()*100:.2f}%")
    print(f"  Lower Canon:")
    print(f"    KW:   {kw_lc['trig_cont']:.4f}")
    print(f"    Null: {null_lc_tc.mean():.4f} ± {null_lc_tc.std():.4f}")
    print(f"    Pctile: {(null_lc_tc <= kw_lc['trig_cont']).mean()*100:.2f}%")

    print(f"\n--- b. Yang-line weight smoothness (mean |Δweight| per bridge) ---")
    print(f"  Upper Canon:")
    print(f"    KW:   {kw_uc['weight_delta']:.4f}")
    print(f"    Null: {null_uc_wd.mean():.4f} ± {null_uc_wd.std():.4f}")
    print(f"    Pctile: {(null_uc_wd <= kw_uc['weight_delta']).mean()*100:.2f}%")
    print(f"  Lower Canon:")
    print(f"    KW:   {kw_lc['weight_delta']:.4f}")
    print(f"    Null: {null_lc_wd.mean():.4f} ± {null_lc_wd.std():.4f}")
    print(f"    Pctile: {(null_lc_wd <= kw_lc['weight_delta']).mean()*100:.2f}%")

    print(f"\n--- c. Raw 6-bit Hamming distance (mean per bridge) ---")
    print(f"  Upper Canon:")
    print(f"    KW:   {kw_uc['hamming']:.4f}")
    print(f"    Null: {null_uc_hd.mean():.4f} ± {null_uc_hd.std():.4f}")
    print(f"    Pctile: {(null_uc_hd <= kw_uc['hamming']).mean()*100:.2f}%")
    print(f"  Lower Canon:")
    print(f"    KW:   {kw_lc['hamming']:.4f}")
    print(f"    Null: {null_lc_hd.mean():.4f} ± {null_lc_hd.std():.4f}")
    print(f"    Pctile: {(null_lc_hd <= kw_lc['hamming']).mean()*100:.2f}%")

    # d. Trigram entropy per canon
    print(f"\n--- d. Trigram distribution entropy per canon ---")
    # KW upper canon: hexagrams 0..29 (indices)
    upper_hex_indices = list(range(0, 30))
    lower_hex_indices = list(range(30, 64))

    for canon_name, indices in [("Upper", upper_hex_indices), ("Lower", lower_hex_indices)]:
        upper_trigs = [upper_trig(HEX_BITS[i]) for i in indices]
        lower_trigs = [lower_trig(HEX_BITS[i]) for i in indices]

        ut_freq = Counter(upper_trigs)
        lt_freq = Counter(lower_trigs)

        ut_probs = np.array(list(ut_freq.values())) / len(indices)
        lt_probs = np.array(list(lt_freq.values())) / len(indices)

        ut_entropy = -np.sum(ut_probs * np.log2(ut_probs))
        lt_entropy = -np.sum(lt_probs * np.log2(lt_probs))

        print(f"  {canon_name} Canon ({len(indices)} hexagrams):")
        print(f"    Upper trigram entropy: {ut_entropy:.4f} bits (max 3.000)")
        print(f"    Lower trigram entropy: {lt_entropy:.4f} bits")
        print(f"    Upper trigram distribution: {dict(sorted((trigram_name(k), v) for k, v in ut_freq.items()))}")
        print(f"    Lower trigram distribution: {dict(sorted((trigram_name(k), v) for k, v in lt_freq.items()))}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: TRIGRAM-LEVEL BRIDGE TRANSITIONS
# ═══════════════════════════════════════════════════════════════════════════════

def computation_3():
    print("\n" + "=" * 80)
    print("COMPUTATION 3: TRIGRAM-LEVEL BRIDGE TRANSITIONS")
    print("=" * 80)

    # Classify each bridge by trigram change pattern
    CHANGE_TYPES = ["neither", "lower_only", "upper_only", "both"]

    results = []
    for bk in range(N_BRIDGES):
        exit_hex = PAIRS[bk][1]
        entry_hex = PAIRS[bk + 1][0]
        lt_change = lower_trig(exit_hex) != lower_trig(entry_hex)
        ut_change = upper_trig(exit_hex) != upper_trig(entry_hex)

        if not lt_change and not ut_change:
            change_type = "neither"
        elif lt_change and not ut_change:
            change_type = "lower_only"
        elif not lt_change and ut_change:
            change_type = "upper_only"
        else:
            change_type = "both"

        kernel = KW_KERNELS[bk]
        results.append({
            'bridge': bk + 1,
            'change_type': change_type,
            'kernel': KERNEL_NAMES[kernel],
            'exit_lt': trigram_name(lower_trig(exit_hex)),
            'exit_ut': trigram_name(upper_trig(exit_hex)),
            'entry_lt': trigram_name(lower_trig(entry_hex)),
            'entry_ut': trigram_name(upper_trig(entry_hex)),
        })

    # Overall distribution
    type_counts = Counter(r['change_type'] for r in results)
    print(f"\n--- Trigram change pattern (all 31 bridges) ---")
    for ct in CHANGE_TYPES:
        print(f"  {ct:>12}: {type_counts.get(ct, 0)}")

    # Per-canon
    upper_types = Counter(r['change_type'] for r in results if r['bridge'] <= 14)
    lower_types = Counter(r['change_type'] for r in results if r['bridge'] >= 16)
    cross_type = results[14]['change_type']

    print(f"\n--- Per-canon breakdown ---")
    print(f"  {'Type':>12} {'Upper(14)':>10} {'Lower(16)':>10} {'Cross(1)':>10}")
    for ct in CHANGE_TYPES:
        u = upper_types.get(ct, 0)
        l = lower_types.get(ct, 0)
        c = 1 if cross_type == ct else 0
        print(f"  {ct:>12} {u:>10} {l:>10} {c:>10}")

    # For "lower_only" and "upper_only" bridges, show which trigram changes
    print(f"\n--- Single-trigram-change bridges ---")
    for r in results:
        if r['change_type'] in ('lower_only', 'upper_only'):
            print(f"  B{r['bridge']:>2} ({r['change_type']:>10}): "
                  f"({r['exit_lt']},{r['exit_ut']}) → ({r['entry_lt']},{r['entry_ut']})  "
                  f"kernel={r['kernel']}")

    # Compare to null
    print(f"\n--- Null comparison (100,000 trials) ---")
    rng = np.random.default_rng(42)
    N_NULL = 100_000

    null_neither = np.empty(N_NULL, dtype=int)
    null_both = np.empty(N_NULL, dtype=int)
    null_lower_only = np.empty(N_NULL, dtype=int)
    null_upper_only = np.empty(N_NULL, dtype=int)

    for t in range(N_NULL):
        perm = rng.permutation(N_PAIRS)
        orient = rng.integers(0, 2, size=N_PAIRS)
        n_ne = 0; n_bo = 0; n_lo = 0; n_uo = 0
        for bk in range(N_BRIDGES):
            pk = perm[bk]; ok = orient[bk]
            pk1 = perm[bk + 1]; ok1 = orient[bk + 1]
            exit_hex = PAIRS[pk][1] if ok == 0 else PAIRS[pk][0]
            entry_hex = PAIRS[pk1][0] if ok1 == 0 else PAIRS[pk1][1]
            lt_c = lower_trig(exit_hex) != lower_trig(entry_hex)
            ut_c = upper_trig(exit_hex) != upper_trig(entry_hex)
            if not lt_c and not ut_c: n_ne += 1
            elif lt_c and not ut_c: n_lo += 1
            elif not lt_c and ut_c: n_uo += 1
            else: n_bo += 1
        null_neither[t] = n_ne
        null_both[t] = n_bo
        null_lower_only[t] = n_lo
        null_upper_only[t] = n_uo

    kw_ne = type_counts.get("neither", 0)
    kw_bo = type_counts.get("both", 0)
    kw_lo = type_counts.get("lower_only", 0)
    kw_uo = type_counts.get("upper_only", 0)

    print(f"  {'Type':>12} {'KW':>4} {'Null mean':>10} {'Null std':>9} {'Pctile':>8}")
    for ct, kw_v, null_v in [
        ("neither", kw_ne, null_neither),
        ("lower_only", kw_lo, null_lower_only),
        ("upper_only", kw_uo, null_upper_only),
        ("both", kw_bo, null_both),
    ]:
        pctile = (null_v <= kw_v).mean() * 100
        print(f"  {ct:>12} {kw_v:>4} {null_v.mean():>10.2f} {null_v.std():>9.2f} {pctile:>7.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: TRIGRAM-REVERSE PROXIMITY
# ═══════════════════════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 80)
    print("COMPUTATION 4: TRIGRAM-REVERSE PROXIMITY")
    print("=" * 80)

    # For each hexagram, find its "trigram reverse" (swap lower and upper trigrams)
    # Hexagram with bits = abcdef → lower=abc, upper=def → reverse = defabc
    trig_reverse_map = {}  # hex_idx → hex_idx of trigram-reverse partner (if it exists)

    hex_to_idx = {}
    for i in range(N_HEX):
        hex_to_idx[HEX_BITS[i]] = i

    for i in range(N_HEX):
        bits = HEX_BITS[i]
        lt = bits[:3]
        ut = bits[3:]
        reversed_bits = ut + lt
        if reversed_bits in hex_to_idx:
            trig_reverse_map[i] = hex_to_idx[reversed_bits]

    # How many hexagrams have a trigram-reverse partner that's a DIFFERENT hexagram?
    has_partner = sum(1 for i, j in trig_reverse_map.items() if i != j)
    is_self_reverse = sum(1 for i, j in trig_reverse_map.items() if i == j)
    print(f"\n--- Trigram-reverse partners ---")
    print(f"  Hexagrams with distinct trigram-reverse partner: {has_partner}")
    print(f"  Self-trigram-reverse (lower == upper): {is_self_reverse}")
    print(f"  Total hexagrams with partner: {len(trig_reverse_map)}")

    # In the KW ordering, compute distance between each hexagram and its trigram-reverse
    kw_order = list(range(N_HEX))  # position of hex i in the sequence
    position_of = {i: i for i in range(N_HEX)}  # hex_idx → KW sequence position (trivial here)

    print(f"\n--- Trigram-reverse distances in KW sequence ---")
    distances = []
    for i in range(N_HEX):
        if i in trig_reverse_map:
            j = trig_reverse_map[i]
            if i < j:  # avoid double counting
                d = abs(i - j)
                distances.append(d)
                hex_i = KING_WEN[i]
                hex_j = KING_WEN[j]
                if d <= 8:
                    print(f"    Hex {hex_i[0]:>2} ({hex_i[1]}) ↔ Hex {hex_j[0]:>2} ({hex_j[1]}): distance {d}")

    print(f"\n  Total trigram-reverse pairs: {len(distances)}")
    print(f"  Distance distribution:")
    for k_val in [1, 2, 4, 8, 16, 32]:
        count = sum(1 for d in distances if d <= k_val)
        print(f"    Within {k_val:>2} positions: {count}/{len(distances)}")

    # Compare to null
    print(f"\n--- Null comparison (100,000 random orderings of 64 hexagrams) ---")
    rng = np.random.default_rng(42)
    N_NULL = 100_000

    # For each k, count how many pairs are within k positions
    ks = [1, 2, 4, 8, 16]
    null_within = {k: np.empty(N_NULL, dtype=int) for k in ks}

    # Build the set of trigram-reverse pairs (as frozensets of indices)
    tr_pairs = []
    for i in range(N_HEX):
        if i in trig_reverse_map:
            j = trig_reverse_map[i]
            if i < j:
                tr_pairs.append((i, j))

    for t in range(N_NULL):
        perm = rng.permutation(N_HEX)
        pos = np.empty(N_HEX, dtype=int)
        for idx in range(N_HEX):
            pos[perm[idx]] = idx

        for k_val in ks:
            count = 0
            for (i, j) in tr_pairs:
                if abs(pos[i] - pos[j]) <= k_val:
                    count += 1
            null_within[k_val][t] = count

    kw_within = {k: sum(1 for d in distances if d <= k) for k in ks}

    print(f"  {'k':>4} {'KW':>4} {'Null mean':>10} {'Null std':>9} {'Pctile':>8}")
    for k_val in ks:
        pctile = (null_within[k_val] <= kw_within[k_val]).mean() * 100
        print(f"  {k_val:>4} {kw_within[k_val]:>4} "
              f"{null_within[k_val].mean():>10.2f} {null_within[k_val].std():>9.2f} "
              f"{pctile:>7.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    results = computation_1()
    computation_2()
    computation_3()
    computation_4()

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
