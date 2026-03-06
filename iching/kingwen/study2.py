"""
Study 2: Ring Structure and Multi-Scale Dynamics in the King Wen Sequence

Five phases testing the timewave's implicit assumptions against
the King Wen sequence itself.
"""

import numpy as np
from collections import Counter
from sequence import all_bits, KING_WEN
from timewave import (
    first_order_differences, make_h_array, mod_64, c_div,
    exp_minus_one, generate_number_set, KELLEY_KNOWN,
)

N_HEX = 64
N_DATA = 384
N_TRIALS = 10000
RNG = np.random.default_rng(42)


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ─── Phase 1: Antipodal Coupling ────────────────────────────────────────────

def phase1():
    print("=" * 70)
    print("PHASE 1: ANTIPODAL COUPLING")
    print("=" * 70)

    h = first_order_differences()
    h = np.array(h)

    # Antipodal correlation: h[k] vs h[(k+32) mod 64]
    def offset_correlation(arr, d):
        pairs = [(arr[k], arr[(k + d) % N_HEX]) for k in range(N_HEX)]
        x, y = zip(*pairs)
        x, y = np.array(x), np.array(y)
        if np.std(x) == 0 or np.std(y) == 0:
            return 0.0
        return np.corrcoef(x, y)[0, 1]

    # Correlation at antipodal offset (d=32)
    antipodal_corr = offset_correlation(h, 32)
    print(f"\nAntipodal correlation (d=32): {antipodal_corr:.4f}")

    # Sweep all offsets
    print(f"\nCorrelation by offset:")
    offset_corrs = []
    for d in range(1, N_HEX):
        c = offset_correlation(h, d)
        offset_corrs.append((d, c))

    # Sort by absolute correlation
    offset_corrs.sort(key=lambda x: -abs(x[1]))
    print(f"  Top 10 by |correlation|:")
    for d, c in offset_corrs[:10]:
        marker = " <-- antipodal" if d == 32 else ""
        print(f"    d={d:2d}: r={c:+.4f}{marker}")

    antipodal_rank = next(i + 1 for i, (d, _) in enumerate(offset_corrs) if d == 32)
    print(f"\n  Antipodal rank among all offsets: {antipodal_rank}/63")

    # Monte Carlo: significance of antipodal correlation
    random_corrs = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(h)
        random_corrs.append(offset_correlation(perm, 32))

    random_corrs = np.array(random_corrs)
    p_value = np.mean(np.abs(random_corrs) >= abs(antipodal_corr))
    print(f"\nMonte Carlo (n={N_TRIALS}):")
    print(f"  Random antipodal |corr|: mean={np.mean(np.abs(random_corrs)):.4f}, "
          f"std={np.std(np.abs(random_corrs)):.4f}")
    print(f"  King Wen |corr|: {abs(antipodal_corr):.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  {'SIGNIFICANT' if p_value < 0.01 else 'NOT SIGNIFICANT'} at p < 0.01")

    # Also test: are adjacent pairs more coupled than antipodal?
    adj_corr = offset_correlation(h, 1)
    print(f"\n  Adjacent correlation (d=1): {adj_corr:.4f}")
    print(f"  Antipodal correlation (d=32): {antipodal_corr:.4f}")


# ─── Phase 2: Bidirectional vs Unidirectional ────────────────────────────────

def phase2():
    print("\n" + "=" * 70)
    print("PHASE 2: BIDIRECTIONAL VS UNIDIRECTIONAL")
    print("=" * 70)

    h = first_order_differences()
    h_arr = np.array(h)

    # Forward-only feature: slope at position k
    forward = []
    # Bidirectional feature: forward slope + antipodal slope
    bidirectional = []
    # Target: h[k]
    targets = []

    for k in range(N_HEX):
        fwd = h[(k - 1) % N_HEX] - h[(k - 2) % N_HEX]
        anti = h[(-k) % N_HEX] - h[(1 - k) % N_HEX]
        forward.append(fwd)
        bidirectional.append(fwd + anti)
        targets.append(h[k])

    forward = np.array(forward, dtype=float)
    bidirectional = np.array(bidirectional, dtype=float)
    targets = np.array(targets, dtype=float)

    # Mutual information approximation via correlation
    def mi_proxy(x, y):
        """Correlation-based MI proxy: -0.5 * log(1 - r^2)"""
        r = np.corrcoef(x, y)[0, 1]
        r2 = min(r ** 2, 0.9999)
        return -0.5 * np.log(1 - r2)

    corr_fwd = np.corrcoef(forward, targets)[0, 1]
    corr_bid = np.corrcoef(bidirectional, targets)[0, 1]
    mi_fwd = mi_proxy(forward, targets)
    mi_bid = mi_proxy(bidirectional, targets)

    print(f"\nPredicting h[k] (next transition):")
    print(f"  Forward-only  — r={corr_fwd:+.4f}, MI proxy={mi_fwd:.4f}")
    print(f"  Bidirectional — r={corr_bid:+.4f}, MI proxy={mi_bid:.4f}")
    print(f"  Improvement:    r delta={abs(corr_bid)-abs(corr_fwd):+.4f}, "
          f"MI delta={mi_bid-mi_fwd:+.4f}")

    # Regression: R² comparison
    def r_squared(x, y):
        r = np.corrcoef(x, y)[0, 1]
        return r ** 2

    r2_fwd = r_squared(forward, targets)
    r2_bid = r_squared(bidirectional, targets)

    print(f"\n  R² forward-only:  {r2_fwd:.4f}")
    print(f"  R² bidirectional: {r2_bid:.4f}")

    # Multi-feature regression: forward + antipodal as separate features
    anti_only = np.array([h[(-k) % N_HEX] - h[(1 - k) % N_HEX] for k in range(N_HEX)], dtype=float)
    X = np.column_stack([forward, anti_only])
    # OLS: beta = (X'X)^-1 X'y
    beta = np.linalg.lstsq(X, targets, rcond=None)[0]
    pred = X @ beta
    ss_res = np.sum((targets - pred) ** 2)
    ss_tot = np.sum((targets - np.mean(targets)) ** 2)
    r2_multi = 1 - ss_res / ss_tot

    print(f"  R² multi-feature (fwd + anti separate): {r2_multi:.4f}")
    print(f"  Regression weights: forward={beta[0]:.3f}, antipodal={beta[1]:.3f}")

    # Control: random offset instead of antipodal
    print(f"\n  Control — random pairing offsets (mean R² over offsets 1..63):")
    r2_offsets = []
    for d in range(1, N_HEX):
        anti_d = np.array([h[(k + d) % N_HEX] - h[(k + d + 1) % N_HEX]
                          for k in range(N_HEX)], dtype=float)
        Xd = np.column_stack([forward, anti_d])
        beta_d = np.linalg.lstsq(Xd, targets, rcond=None)[0]
        pred_d = Xd @ beta_d
        ss_res_d = np.sum((targets - pred_d) ** 2)
        r2_d = 1 - ss_res_d / ss_tot
        r2_offsets.append((d, r2_d))

    r2_offsets.sort(key=lambda x: -x[1])
    print(f"    Mean R²: {np.mean([r for _, r in r2_offsets]):.4f}")
    print(f"    Antipodal (d=32) R²: {r2_multi:.4f}")
    print(f"    Top 5 offsets:")
    for d, r2 in r2_offsets[:5]:
        marker = " <-- antipodal" if d == 32 else ""
        print(f"      d={d:2d}: R²={r2:.4f}{marker}")

    antipodal_rank = next(i + 1 for i, (d, _) in enumerate(r2_offsets) if d == 32)
    print(f"    Antipodal rank: {antipodal_rank}/63")


# ─── Phase 3: Multi-Scale Decomposition ──────────────────────────────────────

def phase3():
    print("\n" + "=" * 70)
    print("PHASE 3: MULTI-SCALE DECOMPOSITION")
    print("=" * 70)

    fod = first_order_differences()
    h = make_h_array(fod)

    # Generate waves at individual scales
    def wave_single_scale(h, scale, weight, half_twist=True):
        """Generate 384-point wave using only one scale."""
        w = []
        for k in range(N_DATA):
            ks = c_div(k, scale)

            if half_twist:
                period = 32 * scale
                sign = exp_minus_one(c_div(k - scale, period))
            else:
                sign = 1

            a = weight * sign * (
                h[mod_64(ks - 1)] - h[mod_64(ks - 2)]
                + h[mod_64(-ks)] - h[mod_64(1 - ks)]
            )

            b = weight * (9 - h[mod_64(-ks)] - h[mod_64(ks - 1)])

            w.append(abs(a) + abs(b))
        return np.array(w)

    yao_wave = wave_single_scale(h, 1, 1)
    tri_wave = wave_single_scale(h, 3, 3)
    hex_wave = wave_single_scale(h, 6, 6)

    def wave_stats(w, label):
        entropy = -np.sum(p * np.log2(p) for p in np.bincount(w.astype(int))[1:] / len(w)
                          if p > 0)
        # Autocorrelation energy (sum of squared autocorrelation at lags 1-20)
        centered = w - np.mean(w)
        autocorr = np.correlate(centered, centered, mode='full')
        autocorr = autocorr[len(w) - 1:] / autocorr[len(w) - 1]
        ac_energy = np.sum(autocorr[1:21] ** 2)

        # Spectral concentration: fraction of power in top 5 frequencies
        fft = np.fft.rfft(centered)
        power = np.abs(fft) ** 2
        power[0] = 0  # skip DC
        total_power = np.sum(power)
        top5 = np.sum(sorted(power, reverse=True)[:5])
        spectral_conc = top5 / total_power if total_power > 0 else 0

        print(f"  {label:20s}: entropy={entropy:.2f}, "
              f"AC energy={ac_energy:.4f}, spectral_conc={spectral_conc:.3f}, "
              f"range=[{w.min()}, {w.max()}]")
        return entropy, ac_energy, spectral_conc

    print(f"\nSingle-scale waves:")
    wave_stats(yao_wave, "Yao (×1)")
    wave_stats(tri_wave, "Trigram (×3)")
    wave_stats(hex_wave, "Hexagram (×6)")

    # Combined wave (all three)
    kelley = np.array(generate_number_set(h, half_twist=True))
    wave_stats(kelley, "Combined (1+3+6)")

    # Sweep alternative scale ratios
    print(f"\nAlternative scale ratios (3 scales):")
    ratio_results = []
    ratio_candidates = [
        (1, 2, 3), (1, 2, 4), (1, 2, 6), (1, 3, 6), (1, 3, 9),
        (1, 4, 8), (1, 4, 16), (1, 6, 12), (1, 8, 32), (2, 4, 8),
        (2, 6, 12), (1, 2, 8),
    ]

    for s1, s2, s3 in ratio_candidates:
        w = np.zeros(N_DATA)
        for scale, weight in [(s1, 1), (s2, s2), (s3, s3)]:
            for k in range(N_DATA):
                ks = c_div(k, scale)
                sign = exp_minus_one(c_div(k - scale, 32 * scale))
                a = weight * sign * (
                    h[mod_64(ks - 1)] - h[mod_64(ks - 2)]
                    + h[mod_64(-ks)] - h[mod_64(1 - ks)]
                )
                b = weight * (9 - h[mod_64(-ks)] - h[mod_64(ks - 1)])
                w[k] += abs(a) + abs(b)

        centered = w - np.mean(w)
        autocorr = np.correlate(centered, centered, mode='full')
        autocorr = autocorr[len(w) - 1:] / (autocorr[len(w) - 1] + 1e-10)
        ac_energy = np.sum(autocorr[1:21] ** 2)

        fft = np.fft.rfft(centered)
        power = np.abs(fft) ** 2
        power[0] = 0
        total_power = np.sum(power)
        top5 = np.sum(sorted(power, reverse=True)[:5])
        spectral_conc = top5 / total_power if total_power > 0 else 0

        ratio_results.append(((s1, s2, s3), ac_energy, spectral_conc))

    ratio_results.sort(key=lambda x: -(x[1] + x[2]))
    print(f"  Ranked by (AC energy + spectral concentration):")
    for (s1, s2, s3), ac, sc in ratio_results:
        marker = " <-- timewave" if (s1, s2, s3) == (1, 3, 6) else ""
        print(f"    ({s1},{s2},{s3}): AC={ac:.4f}, spectral={sc:.3f}, "
              f"combined={ac + sc:.4f}{marker}")

    # FFT of raw h[] — natural frequencies
    print(f"\nRaw h[] FFT — top 5 frequencies:")
    h_arr = np.array(fod, dtype=float)
    centered = h_arr - np.mean(h_arr)
    fft = np.fft.rfft(centered)
    power = np.abs(fft) ** 2
    freqs = np.fft.rfftfreq(N_HEX)
    power[0] = 0
    top_idx = np.argsort(power)[::-1][:5]
    for idx in top_idx:
        period = 1.0 / freqs[idx] if freqs[idx] > 0 else float("inf")
        print(f"    freq={freqs[idx]:.4f}, period={period:.1f}, power={power[idx]:.1f}")


# ─── Phase 4: Level + Slope Interaction ──────────────────────────────────────

def phase4():
    print("\n" + "=" * 70)
    print("PHASE 4: LEVEL + SLOPE INTERACTION")
    print("=" * 70)

    fod = first_order_differences()
    h = make_h_array(fod)

    # Compute angular and linear terms separately
    angular = np.zeros(N_DATA)
    linear = np.zeros(N_DATA)

    for k in range(N_DATA):
        k3 = c_div(k, 3)
        k6 = c_div(k, 6)

        sign1 = exp_minus_one(c_div(k - 1, 32))
        sign3 = exp_minus_one(c_div(k - 3, 96))
        sign6 = exp_minus_one(c_div(k - 6, 192))

        a = (sign1 * (h[mod_64(k - 1)] - h[mod_64(k - 2)]
                       + h[mod_64(-k)] - h[mod_64(1 - k)])
             + 3 * sign3 * (h[mod_64(k3 - 1)] - h[mod_64(k3 - 2)]
                             + h[mod_64(-k3)] - h[mod_64(1 - k3)])
             + 6 * sign6 * (h[mod_64(k6 - 1)] - h[mod_64(k6 - 2)]
                             + h[mod_64(-k6)] - h[mod_64(1 - k6)]))

        b = ((9 - h[mod_64(-k)] - h[mod_64(k - 1)])
             + 3 * (9 - h[mod_64(-k3)] - h[mod_64(k3 - 1)])
             + 6 * (9 - h[mod_64(-k6)] - h[mod_64(k6 - 1)]))

        angular[k] = a
        linear[k] = b

    # Correlation between angular and linear
    corr = np.corrcoef(angular, linear)[0, 1]
    print(f"\nCorrelation between angular and linear terms: {corr:.4f}")

    # Variance decomposition
    w_original = np.abs(angular) + np.abs(linear)
    var_angular = np.var(np.abs(angular))
    var_linear = np.var(np.abs(linear))
    var_combined = np.var(w_original)
    cov_term = var_combined - var_angular - var_linear

    print(f"\nVariance decomposition of w[k] = |a| + |b|:")
    print(f"  Var(|angular|):  {var_angular:.2f} ({100 * var_angular / var_combined:.1f}%)")
    print(f"  Var(|linear|):   {var_linear:.2f} ({100 * var_linear / var_combined:.1f}%)")
    print(f"  2*Cov(|a|,|b|): {cov_term:.2f} ({100 * cov_term / var_combined:.1f}%)")
    print(f"  Var(w):          {var_combined:.2f}")

    # Compare combination methods
    def structure_score(w):
        """Combined structure metric: AC energy + spectral concentration."""
        centered = w - np.mean(w)
        ac = np.correlate(centered, centered, mode='full')
        ac = ac[len(w) - 1:] / (ac[len(w) - 1] + 1e-10)
        ac_energy = np.sum(ac[1:21] ** 2)

        fft = np.fft.rfft(centered)
        power = np.abs(fft) ** 2
        power[0] = 0
        total = np.sum(power)
        top5 = np.sum(sorted(power, reverse=True)[:5])
        sc = top5 / total if total > 0 else 0

        return ac_energy + sc

    methods = {
        "|a| + |b| (original)": np.abs(angular) + np.abs(linear),
        "a + b (signed)": angular + linear,
        "a² + b² (energy)": angular ** 2 + linear ** 2,
        "|a| only": np.abs(angular),
        "|b| only": np.abs(linear),
    }

    print(f"\nCombination methods — structure score (AC energy + spectral conc):")
    scored = [(name, structure_score(w), w) for name, w in methods.items()]
    scored.sort(key=lambda x: -x[1])
    for name, score, _ in scored:
        print(f"  {name:25s}: {score:.4f}")

    # Sweep constant C in linear term
    print(f"\nConstant sweep (C - h[-k] - h[k-1]):")
    c_results = []
    for C in range(0, 13):
        lin_c = np.zeros(N_DATA)
        for k in range(N_DATA):
            k3 = c_div(k, 3)
            k6 = c_div(k, 6)
            b = ((C - h[mod_64(-k)] - h[mod_64(k - 1)])
                 + 3 * (C - h[mod_64(-k3)] - h[mod_64(k3 - 1)])
                 + 6 * (C - h[mod_64(-k6)] - h[mod_64(k6 - 1)]))
            lin_c[k] = b
        w_c = np.abs(angular) + np.abs(lin_c)
        score = structure_score(w_c)
        c_results.append((C, score))

    c_results.sort(key=lambda x: -x[1])
    for C, score in c_results:
        marker = " <-- timewave" if C == 9 else ""
        print(f"    C={C:2d}: score={score:.4f}{marker}")


# ─── Phase 5: Self-Similarity ────────────────────────────────────────────────

def phase5():
    print("\n" + "=" * 70)
    print("PHASE 5: SELF-SIMILARITY")
    print("=" * 70)

    fod = first_order_differences()
    h = make_h_array(fod)
    kelley = np.array(generate_number_set(h, half_twist=True), dtype=float)

    # Autocorrelation at multiples of 64
    centered = kelley - np.mean(kelley)
    full_ac = np.correlate(centered, centered, mode='full')
    ac = full_ac[N_DATA - 1:] / full_ac[N_DATA - 1]

    print(f"\nAutocorrelation at multiples of 64:")
    for mult in range(1, 6):
        lag = 64 * mult
        if lag < N_DATA:
            print(f"  Lag {lag:3d} ({mult}×64): r={ac[lag]:+.4f}")

    # Compare to autocorrelation at non-64 lags
    print(f"\nAutocorrelation at key lags:")
    for lag in [1, 2, 4, 8, 16, 32, 48, 64, 96, 128, 192, 256, 320]:
        if lag < N_DATA:
            print(f"  Lag {lag:3d}: r={ac[lag]:+.4f}")

    # Self-similarity: compare wave segments
    # Split 384 into 6 segments of 64 (yao cycles)
    segments = [kelley[i * 64:(i + 1) * 64] for i in range(6)]
    print(f"\nInter-segment correlations (6 yao cycles of 64):")
    corr_matrix = np.zeros((6, 6))
    for i in range(6):
        for j in range(6):
            corr_matrix[i][j] = np.corrcoef(segments[i], segments[j])[0, 1]

    for i in range(6):
        row = " ".join(f"{corr_matrix[i][j]:+.3f}" for j in range(6))
        print(f"  Seg {i}: {row}")

    mean_off_diag = (np.sum(corr_matrix) - np.trace(corr_matrix)) / (36 - 6)
    print(f"  Mean off-diagonal correlation: {mean_off_diag:+.4f}")

    # Monte Carlo: compare against random 384-point waves
    random_means = []
    for _ in range(N_TRIALS):
        random_wave = RNG.permutation(kelley)
        segs = [random_wave[i * 64:(i + 1) * 64] for i in range(6)]
        cm = np.zeros((6, 6))
        for i in range(6):
            for j in range(6):
                cm[i][j] = np.corrcoef(segs[i], segs[j])[0, 1]
        random_means.append((np.sum(cm) - np.trace(cm)) / 30)

    random_means = np.array(random_means)
    p_value = np.mean(random_means >= mean_off_diag)
    z_score = (mean_off_diag - np.mean(random_means)) / np.std(random_means)

    print(f"\n  Random mean off-diag: {np.mean(random_means):+.4f} "
          f"+/- {np.std(random_means):.4f}")
    print(f"  King Wen mean off-diag: {mean_off_diag:+.4f}")
    print(f"  Z-score: {z_score:.2f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  {'SIGNIFICANT' if p_value < 0.01 else 'NOT SIGNIFICANT'} at p < 0.01")

    # Scaling factor comparison
    print(f"\nScaling factor sweep (fractal dimension proxy):")
    print(f"  Testing self-similarity of 384-point wave at different split sizes:")

    for split_size in [2, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192]:
        if N_DATA % split_size != 0:
            continue
        n_segs = N_DATA // split_size
        if n_segs < 2:
            continue
        segs = [kelley[i * split_size:(i + 1) * split_size] for i in range(n_segs)]
        # Mean pairwise correlation
        corrs = []
        for i in range(n_segs):
            for j in range(i + 1, n_segs):
                corrs.append(np.corrcoef(segs[i], segs[j])[0, 1])
        mean_corr = np.mean(corrs) if corrs else 0
        print(f"    Split {split_size:3d} ({n_segs:3d} segments): "
              f"mean pairwise r={mean_corr:+.4f}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("STUDY 2: RING STRUCTURE AND MULTI-SCALE DYNAMICS")
    print("IN THE KING WEN SEQUENCE")
    print("=" * 70)

    phase1()
    phase2()
    phase3()
    phase4()
    phase5()

    print("\n" + "=" * 70)
    print("STUDY 2 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
