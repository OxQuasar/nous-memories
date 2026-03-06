"""
Phase 1b/2b: Non-Linear Structure Detection in Backward Reading

Seven tests replacing correlation with information-theoretic and structural methods.
"""

import numpy as np
from collections import Counter
from itertools import product as iterproduct
from sequence import all_bits
from timewave import first_order_differences

N_HEX = 64
N_TRIALS = 10000
RNG = np.random.default_rng(42)


def get_h():
    return np.array(first_order_differences())


# ─── Test 1: Non-Parametric Mutual Information ──────────────────────────────

def binned_mi(x, y, n_bins=3):
    """Mutual information via binned joint distribution."""
    # Bin edges from data range
    x_bins = np.digitize(x, np.linspace(min(x) - 0.5, max(x) + 0.5, n_bins + 1)[1:-1])
    y_bins = np.digitize(y, np.linspace(min(y) - 0.5, max(y) + 0.5, n_bins + 1)[1:-1])

    # Joint and marginal counts
    n = len(x)
    joint = Counter(zip(x_bins, y_bins))
    px = Counter(x_bins)
    py = Counter(y_bins)

    mi = 0.0
    for (xi, yi), nxy in joint.items():
        pxy = nxy / n
        pxi = px[xi] / n
        pyi = py[yi] / n
        if pxy > 0 and pxi > 0 and pyi > 0:
            mi += pxy * np.log2(pxy / (pxi * pyi))
    return mi


def test1():
    print("=" * 70)
    print("TEST 1: NON-PARAMETRIC MUTUAL INFORMATION")
    print("=" * 70)

    h = get_h()

    # MI at each offset
    offset_mi = []
    for d in range(1, N_HEX):
        pairs_x = h
        pairs_y = np.array([h[(k + d) % N_HEX] for k in range(N_HEX)])
        mi = binned_mi(pairs_x, pairs_y)
        offset_mi.append((d, mi))

    offset_mi.sort(key=lambda x: -x[1])
    antipodal_mi = next(mi for d, mi in offset_mi if d == 32)

    print(f"\nTop 10 offsets by MI:")
    for d, mi in offset_mi[:10]:
        marker = " <-- antipodal" if d == 32 else ""
        print(f"  d={d:2d}: MI={mi:.4f} bits{marker}")

    antipodal_rank = next(i + 1 for i, (d, _) in enumerate(offset_mi) if d == 32)
    print(f"\n  Antipodal rank: {antipodal_rank}/63")

    # Monte Carlo significance for antipodal MI
    random_mis = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(h)
        pairs_y = np.array([perm[(k + 32) % N_HEX] for k in range(N_HEX)])
        random_mis.append(binned_mi(perm, pairs_y))

    random_mis = np.array(random_mis)
    p_value = np.mean(random_mis >= antipodal_mi)
    print(f"\n  Monte Carlo (n={N_TRIALS}):")
    print(f"    Random MI: mean={np.mean(random_mis):.4f}, std={np.std(random_mis):.4f}")
    print(f"    King Wen antipodal MI: {antipodal_mi:.4f}")
    print(f"    p-value: {p_value:.4f}")


# ─── Test 2: Contingency Table (Chi-Squared) ────────────────────────────────

def test2():
    print("\n" + "=" * 70)
    print("TEST 2: CONTINGENCY TABLE (CHI-SQUARED)")
    print("=" * 70)

    h = get_h()

    # Bin into low (1-2), mid (3-4), high (5-6)
    def bin_h(v):
        if v <= 2:
            return 0  # low
        elif v <= 4:
            return 1  # mid
        else:
            return 2  # high

    h_binned = np.array([bin_h(v) for v in h])

    def chi_squared(h_b, d):
        """Chi-squared statistic for independence at offset d."""
        observed = np.zeros((3, 3), dtype=float)
        for k in range(N_HEX):
            i = h_b[k]
            j = h_b[(k + d) % N_HEX]
            observed[i][j] += 1

        row_sums = observed.sum(axis=1, keepdims=True)
        col_sums = observed.sum(axis=0, keepdims=True)
        total = observed.sum()
        expected = row_sums * col_sums / total

        # Avoid division by zero
        mask = expected > 0
        chi2 = np.sum((observed[mask] - expected[mask]) ** 2 / expected[mask])
        return chi2

    offset_chi2 = []
    for d in range(1, N_HEX):
        chi2 = chi_squared(h_binned, d)
        offset_chi2.append((d, chi2))

    offset_chi2.sort(key=lambda x: -x[1])

    print(f"\nTop 10 offsets by chi-squared:")
    for d, chi2 in offset_chi2[:10]:
        # df = (3-1)(3-1) = 4, critical value at p<0.05 = 9.49, p<0.01 = 13.28
        sig = "**" if chi2 > 13.28 else "*" if chi2 > 9.49 else ""
        marker = " <-- antipodal" if d == 32 else ""
        print(f"  d={d:2d}: chi²={chi2:.2f} {sig}{marker}")

    antipodal_rank = next(i + 1 for i, (d, _) in enumerate(offset_chi2) if d == 32)
    print(f"\n  Antipodal rank: {antipodal_rank}/63")
    print(f"  (Critical values: p<0.05 = 9.49, p<0.01 = 13.28, df=4)")


# ─── Test 3: Compressibility (Lempel-Ziv) ───────────────────────────────────

def lz_complexity(seq):
    """Lempel-Ziv 76 complexity: count of distinct phrases."""
    s = list(seq)
    n = len(s)
    i = 0
    phrases = 0
    while i < n:
        length = 1
        while i + length <= n:
            subseq = tuple(s[i:i + length])
            # Check if this subsequence appeared before position i
            found = False
            for j in range(i):
                if s[j:j + length] == s[i:i + length]:
                    found = True
                    break
            if not found:
                break
            length += 1
        i += length
        phrases += 1
    return phrases


def test3():
    print("\n" + "=" * 70)
    print("TEST 3: COMPRESSIBILITY (LEMPEL-ZIV)")
    print("=" * 70)

    h = list(get_h())
    h_rev = list(reversed(h))
    h_concat = h + h_rev

    lz_fwd = lz_complexity(h)
    lz_rev = lz_complexity(h_rev)
    lz_concat = lz_complexity(h_concat)
    ratio = lz_concat / lz_fwd

    print(f"\n  LZ complexity forward:      {lz_fwd}")
    print(f"  LZ complexity reversed:     {lz_rev}")
    print(f"  LZ complexity concatenated: {lz_concat}")
    print(f"  Ratio (concat/forward):     {ratio:.3f}")
    print(f"    < 2.0 → reverse is partially redundant")
    print(f"    = 2.0 → reverse is independent")
    print(f"    > 2.0 → impossible (bounded by 2x)")

    # Monte Carlo
    random_ratios = []
    for _ in range(min(N_TRIALS, 1000)):  # LZ is slow, use fewer trials
        perm = list(RNG.permutation(h))
        perm_rev = list(reversed(perm))
        lz_f = lz_complexity(perm)
        lz_c = lz_complexity(perm + perm_rev)
        if lz_f > 0:
            random_ratios.append(lz_c / lz_f)

    random_ratios = np.array(random_ratios)
    p_value = np.mean(random_ratios <= ratio)
    print(f"\n  Monte Carlo (n={len(random_ratios)}):")
    print(f"    Random ratio: mean={np.mean(random_ratios):.3f}, std={np.std(random_ratios):.3f}")
    print(f"    King Wen ratio: {ratio:.3f}")
    print(f"    p-value (lower is more redundant): {p_value:.4f}")


# ─── Test 4: Permutation Entropy and Ordinal Patterns ────────────────────────

def ordinal_patterns(seq, order=3):
    """Extract ordinal patterns of given order from sequence."""
    patterns = []
    for i in range(len(seq) - order + 1):
        window = seq[i:i + order]
        # Rank the values (0 = smallest)
        ranked = list(np.argsort(np.argsort(window)))
        patterns.append(tuple(ranked))
    return patterns


def permutation_entropy(patterns, order=3):
    """Permutation entropy from ordinal pattern frequencies."""
    import math
    n = len(patterns)
    counts = Counter(patterns)
    max_entropy = math.log2(math.factorial(order))
    entropy = -sum((c / n) * np.log2(c / n) for c in counts.values())
    return entropy, entropy / max_entropy  # absolute, normalized


def test4():
    print("\n" + "=" * 70)
    print("TEST 4: PERMUTATION ENTROPY AND ORDINAL PATTERNS")
    print("=" * 70)

    h = list(get_h())
    h_rev = list(reversed(h))

    for order in [3, 4]:
        fwd_patterns = ordinal_patterns(h, order)
        rev_patterns = ordinal_patterns(h_rev, order)

        fwd_set = set(fwd_patterns)
        rev_set = set(rev_patterns)
        import math
        total_possible = math.factorial(order)

        shared = fwd_set & rev_set
        fwd_only = fwd_set - rev_set
        rev_only = rev_set - fwd_set
        forbidden = total_possible - len(fwd_set | rev_set)

        pe_fwd, pe_fwd_norm = permutation_entropy(fwd_patterns, order)
        pe_rev, pe_rev_norm = permutation_entropy(rev_patterns, order)

        # Combined: interleave forward and backward
        combined_patterns = fwd_patterns + rev_patterns
        pe_comb, pe_comb_norm = permutation_entropy(combined_patterns, order)

        print(f"\n  Order {order} (max {total_possible} possible patterns):")
        print(f"    Forward patterns:  {len(fwd_set)}/{total_possible}")
        print(f"    Backward patterns: {len(rev_set)}/{total_possible}")
        print(f"    Shared:            {len(shared)}")
        print(f"    Forward only:      {len(fwd_only)}")
        print(f"    Backward only:     {len(rev_only)}")
        print(f"    Forbidden (both):  {forbidden}")
        print(f"    PE forward:        {pe_fwd:.4f} (norm: {pe_fwd_norm:.4f})")
        print(f"    PE backward:       {pe_rev:.4f} (norm: {pe_rev_norm:.4f})")
        print(f"    PE combined:       {pe_comb:.4f} (norm: {pe_comb_norm:.4f})")

    # Monte Carlo: are the forbidden patterns significant?
    h_arr = np.array(h)
    order = 3
    kw_forbidden = math.factorial(order) - len(set(ordinal_patterns(h, order)) | set(ordinal_patterns(h_rev, order)))
    random_forbidden = []
    for _ in range(N_TRIALS):
        perm = list(RNG.permutation(h_arr))
        perm_rev = list(reversed(perm))
        all_pats = set(ordinal_patterns(perm, order)) | set(ordinal_patterns(perm_rev, order))
        random_forbidden.append(math.factorial(order) - len(all_pats))

    random_forbidden = np.array(random_forbidden)
    p_value = np.mean(random_forbidden >= kw_forbidden)
    print(f"\n  Forbidden pattern significance (order 3):")
    print(f"    King Wen forbidden: {kw_forbidden}")
    print(f"    Random forbidden: mean={np.mean(random_forbidden):.2f}, std={np.std(random_forbidden):.2f}")
    print(f"    p-value: {p_value:.4f}")


# ─── Test 5: Ring Symmetry ──────────────────────────────────────────────────

def edit_distance_circular(a, b):
    """Simple element-wise distance for same-length sequences."""
    return sum(x != y for x, y in zip(a, b))


def test5():
    print("\n" + "=" * 70)
    print("TEST 5: RING SYMMETRY")
    print("=" * 70)

    h = list(get_h())
    h_rev = list(reversed(h))

    # Direct palindrome distance
    palindrome_dist = edit_distance_circular(h, h_rev)
    print(f"\n  Palindrome distance (h vs reversed h): {palindrome_dist}/{N_HEX}")

    # Best rotation for ring symmetry
    best_rot = 0
    best_dist = N_HEX
    all_dists = []
    for r in range(N_HEX):
        rotated_rev = h_rev[r:] + h_rev[:r]
        d = edit_distance_circular(h, rotated_rev)
        all_dists.append((r, d))
        if d < best_dist:
            best_dist = d
            best_rot = r

    print(f"  Best ring symmetry: rotation={best_rot}, distance={best_dist}/{N_HEX}")

    # Show top 5 rotations
    all_dists.sort(key=lambda x: x[1])
    print(f"  Top 5 rotations:")
    for r, d in all_dists[:5]:
        print(f"    rot={r:2d}: distance={d}")

    # Monte Carlo: is the best ring symmetry better than random?
    random_best = []
    for _ in range(N_TRIALS):
        perm = list(RNG.permutation(h))
        perm_rev = list(reversed(perm))
        best = min(edit_distance_circular(perm, perm_rev[r:] + perm_rev[:r])
                   for r in range(N_HEX))
        random_best.append(best)

    random_best = np.array(random_best)
    p_value = np.mean(random_best <= best_dist)
    print(f"\n  Monte Carlo (n={N_TRIALS}):")
    print(f"    Random best ring distance: mean={np.mean(random_best):.2f}, "
          f"std={np.std(random_best):.2f}")
    print(f"    King Wen best: {best_dist}")
    print(f"    p-value (lower distance = more symmetric): {p_value:.4f}")


# ─── Test 6: Transfer Entropy ────────────────────────────────────────────────

def transfer_entropy(source, target, lag=1, n_bins=3):
    """
    Transfer entropy from source to target.
    TE = H(target_future | target_past) - H(target_future | target_past, source_past)
    Estimated via binned distributions.
    """
    n = len(target) - lag

    def bin_val(v, vals):
        edges = np.linspace(min(vals) - 0.5, max(vals) + 0.5, n_bins + 1)[1:-1]
        return int(np.digitize(v, edges))

    # Build joint distributions
    # target_past -> target_future (conditional entropy H(Y+|Y))
    ty_counts = Counter()
    ty_joint = Counter()
    # target_past + source_past -> target_future (conditional entropy H(Y+|Y,X))
    tyx_counts = Counter()
    tyx_joint = Counter()

    for i in range(lag, len(target)):
        y_past = bin_val(target[i - lag], target)
        y_future = bin_val(target[i], target)
        x_past = bin_val(source[i - lag], source)

        ty_counts[y_past] += 1
        ty_joint[(y_past, y_future)] += 1

        tyx_counts[(y_past, x_past)] += 1
        tyx_joint[(y_past, x_past, y_future)] += 1

    # H(Y+|Y) = H(Y+,Y) - H(Y)
    def cond_entropy(joint_counts, margin_counts):
        total = sum(margin_counts.values())
        ce = 0.0
        for key, count in joint_counts.items():
            margin_key = key[:-1] if len(key) > 2 else key[0]
            p_joint = count / total
            p_margin = margin_counts[margin_key] / total
            if p_joint > 0 and p_margin > 0:
                ce -= p_joint * np.log2(p_joint / p_margin)
        return ce

    h_y_given_y = cond_entropy(ty_joint, ty_counts)
    h_y_given_yx = cond_entropy(tyx_joint, tyx_counts)

    return h_y_given_y - h_y_given_yx


def test6():
    print("\n" + "=" * 70)
    print("TEST 6: TRANSFER ENTROPY")
    print("=" * 70)

    h = get_h()

    # TE from backward reading to forward, at each offset
    offset_te = []
    for d in range(1, N_HEX):
        source = np.array([h[(k + d) % N_HEX] for k in range(N_HEX)])
        te = transfer_entropy(source, h, lag=1)
        offset_te.append((d, te))

    offset_te.sort(key=lambda x: -x[1])
    antipodal_te = next(te for d, te in offset_te if d == 32)

    print(f"\nTop 10 offsets by transfer entropy (source → h[k]):")
    for d, te in offset_te[:10]:
        marker = " <-- antipodal" if d == 32 else ""
        print(f"  d={d:2d}: TE={te:.4f} bits{marker}")

    antipodal_rank = next(i + 1 for i, (d, _) in enumerate(offset_te) if d == 32)
    print(f"\n  Antipodal rank: {antipodal_rank}/63")

    # Monte Carlo
    random_tes = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(h)
        source = np.array([perm[(k + 32) % N_HEX] for k in range(N_HEX)])
        random_tes.append(transfer_entropy(source, perm, lag=1))

    random_tes = np.array(random_tes)
    p_value = np.mean(random_tes >= antipodal_te)
    print(f"\n  Monte Carlo (n={N_TRIALS}):")
    print(f"    Random TE: mean={np.mean(random_tes):.4f}, std={np.std(random_tes):.4f}")
    print(f"    King Wen antipodal TE: {antipodal_te:.4f}")
    print(f"    p-value: {p_value:.4f}")


# ─── Test 7: KNN Nonlinear Prediction ────────────────────────────────────────

def knn_predict(X_train, y_train, X_test, k=3):
    """Simple KNN regression."""
    predictions = []
    for x in X_test:
        dists = np.sqrt(np.sum((X_train - x) ** 2, axis=1))
        nearest = np.argsort(dists)[:k]
        predictions.append(np.mean(y_train[nearest]))
    return np.array(predictions)


def test7():
    print("\n" + "=" * 70)
    print("TEST 7: KNN NONLINEAR PREDICTION")
    print("=" * 70)

    h = get_h()

    # Leave-one-out cross-validation
    def loo_mse(features_func):
        """LOO-CV MSE for KNN prediction of h[k]."""
        n = N_HEX
        errors = []
        for test_k in range(n):
            # Build features and targets excluding test_k
            X_all = []
            y_all = []
            for k in range(n):
                X_all.append(features_func(k))
                y_all.append(h[k])
            X_all = np.array(X_all)
            y_all = np.array(y_all)

            X_train = np.delete(X_all, test_k, axis=0)
            y_train = np.delete(y_all, test_k)
            X_test = X_all[test_k:test_k + 1]

            pred = knn_predict(X_train, y_train, X_test, k=5)
            errors.append((h[test_k] - pred[0]) ** 2)
        return np.mean(errors)

    # Forward-only features
    def fwd_features(k):
        return np.array([h[(k - 1) % N_HEX], h[(k - 2) % N_HEX]])

    # Forward + antipodal features
    def bid_features(k):
        return np.array([h[(k - 1) % N_HEX], h[(k - 2) % N_HEX],
                         h[(-k) % N_HEX], h[(1 - k) % N_HEX]])

    mse_fwd = loo_mse(fwd_features)
    mse_bid = loo_mse(bid_features)

    # Baseline: predict mean
    mse_mean = np.var(h)

    print(f"\n  LOO-CV Mean Squared Error (KNN k=5):")
    print(f"    Mean baseline:     {mse_mean:.4f}")
    print(f"    Forward-only:      {mse_fwd:.4f}")
    print(f"    Forward+antipodal: {mse_bid:.4f}")
    print(f"    Improvement:       {(mse_fwd - mse_bid) / mse_fwd * 100:+.1f}%")

    # Sweep offsets
    print(f"\n  Offset sweep (forward + offset d features):")
    offset_mse = []
    for d in range(1, N_HEX):
        def features_d(k, d=d):
            return np.array([h[(k - 1) % N_HEX], h[(k - 2) % N_HEX],
                             h[(k + d) % N_HEX], h[(k + d + 1) % N_HEX]])
        mse_d = loo_mse(features_d)
        offset_mse.append((d, mse_d))

    offset_mse.sort(key=lambda x: x[1])
    print(f"    Top 5 offsets (lowest MSE):")
    for d, mse in offset_mse[:5]:
        marker = " <-- antipodal" if d == 32 else ""
        print(f"      d={d:2d}: MSE={mse:.4f}{marker}")

    antipodal_rank = next(i + 1 for i, (d, _) in enumerate(offset_mse) if d == 32)
    print(f"    Antipodal rank: {antipodal_rank}/63 (lower is better)")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("PHASE 1b/2b: NON-LINEAR STRUCTURE DETECTION")
    print("=" * 70)

    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()

    print("\n" + "=" * 70)
    print("PHASE 1b/2b COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
