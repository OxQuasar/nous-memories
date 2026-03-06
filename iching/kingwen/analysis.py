"""
Numerical analysis of the King Wen sequence.

Seven analyses:
1. Basic structure (weights, trigrams)
2. Transition analysis (Hamming distances, line flip frequencies)
3. Baseline comparisons (Fu Xi, Gray code, random permutations)
4. Pairing structure (inversion/complement verification)
5. Trigram grammar (transition matrices, preferred/avoided transitions)
6. Spectral / periodicity (FFT on weight sequence, per-line cycles)
7. Information content (entropy, mutual information, compressibility)
"""

import numpy as np
from collections import Counter
from itertools import product

from sequence import (
    KING_WEN, bits, name, number, all_bits,
    lower_trigram, upper_trigram, trigram_name, TRIGRAMS,
)

N = 64
LINES = 6


# ─── Utilities ───────────────────────────────────────────────────────────────

def hamming(a, b):
    """Hamming distance between two bit lists."""
    return sum(x != y for x, y in zip(a, b))


def invert(b):
    """Flip hexagram top-to-bottom (reverse line order)."""
    return list(reversed(b))


def complement(b):
    """Flip all lines (yin↔yang)."""
    return [1 - x for x in b]


def weight(b):
    """Count of yang lines."""
    return sum(b)


def to_int(b):
    """6-bit list to integer (line 1 = bit 0)."""
    return sum(v << i for i, v in enumerate(b))


# ─── 1. Basic Structure ─────────────────────────────────────────────────────

def analyze_basic():
    print("=" * 70)
    print("1. BASIC STRUCTURE")
    print("=" * 70)

    hexagrams = all_bits()
    weights = [weight(h) for h in hexagrams]

    print(f"\nWeight sequence (yang count per hexagram):")
    for row_start in range(0, N, 16):
        row = weights[row_start:row_start + 16]
        labels = [f"{row_start + i + 1:2d}:{w}" for i, w in enumerate(row)]
        print("  " + "  ".join(labels))

    print(f"\nWeight distribution:")
    wc = Counter(weights)
    for w in sorted(wc):
        print(f"  {w} yang lines: {wc[w]} hexagrams")

    print(f"\nMean weight: {np.mean(weights):.2f}")
    print(f"Weight std:  {np.std(weights):.2f}")

    # Pair weight sums
    pair_sums = [weights[i] + weights[i + 1] for i in range(0, N, 2)]
    print(f"\nPair weight sums (should all be 6): {set(pair_sums)}")

    # Trigram frequency
    print(f"\nLower trigram frequency:")
    lt = [lower_trigram(i) for i in range(N)]
    ltc = Counter(lt)
    for tri, count in sorted(ltc.items(), key=lambda x: -x[1]):
        print(f"  {tri} ({trigram_name(tri):>7s}): {count}")

    print(f"\nUpper trigram frequency:")
    ut = [upper_trigram(i) for i in range(N)]
    utc = Counter(ut)
    for tri, count in sorted(utc.items(), key=lambda x: -x[1]):
        print(f"  {tri} ({trigram_name(tri):>7s}): {count}")

    return weights


# ─── 2. Transition Analysis ─────────────────────────────────────────────────

def analyze_transitions():
    print("\n" + "=" * 70)
    print("2. TRANSITION ANALYSIS")
    print("=" * 70)

    hexagrams = all_bits()

    # Hamming distances between consecutive hexagrams
    h_dists = [hamming(hexagrams[i], hexagrams[i + 1]) for i in range(N - 1)]

    print(f"\nHamming distances (consecutive):")
    for row_start in range(0, len(h_dists), 16):
        row = h_dists[row_start:row_start + 16]
        labels = [f"{row_start + i + 1:2d}→{row_start + i + 2:2d}:{d}" for i, d in enumerate(row)]
        print("  " + "  ".join(labels))

    print(f"\nHamming distance distribution:")
    hc = Counter(h_dists)
    for d in sorted(hc):
        print(f"  distance {d}: {hc[d]} transitions")

    print(f"\nMean Hamming distance: {np.mean(h_dists):.2f}")
    print(f"Min: {min(h_dists)}, Max: {max(h_dists)}")

    # Line-by-line flip frequency
    line_flips = [0] * LINES
    for i in range(N - 1):
        for j in range(LINES):
            if hexagrams[i][j] != hexagrams[i + 1][j]:
                line_flips[j] += 1

    print(f"\nLine flip frequency (across all {N - 1} transitions):")
    for j in range(LINES):
        bar = "#" * line_flips[j]
        print(f"  Line {j + 1} ({'bottom' if j == 0 else 'top' if j == 5 else 'mid-' + str(j + 1)}): "
              f"{line_flips[j]:2d} flips  {bar}")

    # Odd vs even transitions (within-pair vs between-pair)
    within_pair = [h_dists[i] for i in range(0, len(h_dists), 2)]
    between_pair = [h_dists[i] for i in range(1, len(h_dists), 2)]

    print(f"\nWithin-pair Hamming (odd→even): mean={np.mean(within_pair):.2f}, "
          f"dist={Counter(within_pair)}")
    print(f"Between-pair Hamming (even→odd): mean={np.mean(between_pair):.2f}, "
          f"dist={Counter(between_pair)}")

    return h_dists


# ─── 3. Baseline Comparisons ────────────────────────────────────────────────

def analyze_baselines(kw_dists):
    print("\n" + "=" * 70)
    print("3. BASELINE COMPARISONS")
    print("=" * 70)

    hexagrams = all_bits()

    # Fu Xi sequence (binary counting)
    fuxi_order = sorted(range(N), key=lambda i: to_int(bits(i)))
    # Actually Fu Xi is just 0-63 in binary, need to map
    fuxi_hexagrams = []
    for val in range(N):
        b = [(val >> i) & 1 for i in range(LINES)]
        fuxi_hexagrams.append(b)

    fuxi_dists = [hamming(fuxi_hexagrams[i], fuxi_hexagrams[i + 1]) for i in range(N - 1)]

    print(f"\nFu Xi (binary counting):")
    print(f"  Mean Hamming: {np.mean(fuxi_dists):.2f}")
    print(f"  Distribution: {Counter(fuxi_dists)}")

    # Gray code (minimal transitions)
    def gray_code(n_bits, n_codes):
        codes = []
        for i in range(n_codes):
            g = i ^ (i >> 1)
            codes.append([(g >> b) & 1 for b in range(n_bits)])
        return codes

    gray_hexagrams = gray_code(LINES, N)
    gray_dists = [hamming(gray_hexagrams[i], gray_hexagrams[i + 1]) for i in range(N - 1)]

    print(f"\nGray code (minimal transitions):")
    print(f"  Mean Hamming: {np.mean(gray_dists):.2f}")
    print(f"  Distribution: {Counter(gray_dists)}")

    # Random permutations (Monte Carlo)
    n_trials = 10000
    rng = np.random.default_rng(42)
    random_means = []
    random_stds = []

    for _ in range(n_trials):
        perm = rng.permutation(N)
        perm_hexagrams = [hexagrams[p] for p in perm]
        dists = [hamming(perm_hexagrams[i], perm_hexagrams[i + 1]) for i in range(N - 1)]
        random_means.append(np.mean(dists))
        random_stds.append(np.std(dists))

    kw_mean = np.mean(kw_dists)
    percentile = np.mean([m <= kw_mean for m in random_means]) * 100

    print(f"\nRandom permutations ({n_trials} trials):")
    print(f"  Mean Hamming: {np.mean(random_means):.2f} +/- {np.std(random_means):.2f}")
    print(f"  King Wen mean: {kw_mean:.2f} (percentile: {percentile:.1f}%)")

    print(f"\nSummary comparison:")
    print(f"  Gray code:    {np.mean(gray_dists):.2f} (minimal)")
    print(f"  King Wen:     {kw_mean:.2f}")
    print(f"  Random:       {np.mean(random_means):.2f}")
    print(f"  Fu Xi:        {np.mean(fuxi_dists):.2f}")


# ─── 4. Pairing Structure ───────────────────────────────────────────────────

def analyze_pairing():
    print("\n" + "=" * 70)
    print("4. PAIRING STRUCTURE")
    print("=" * 70)

    hexagrams = all_bits()
    inversions = 0
    complements = 0
    neither = 0

    for i in range(0, N, 2):
        a, b = hexagrams[i], hexagrams[i + 1]
        inv = invert(a)
        comp = complement(a)

        is_inv = (b == inv)
        is_comp = (b == comp)
        is_palindrome = (a == invert(a))

        rel = ""
        if is_inv and not is_palindrome:
            rel = "inversion"
            inversions += 1
        elif is_comp:
            rel = "complement"
            complements += 1
        elif is_inv and is_palindrome:
            rel = "complement (palindrome→inversion=self)"
            complements += 1
        else:
            rel = "NEITHER"
            neither += 1

        pair_num = i // 2 + 1
        print(f"  Pair {pair_num:2d}: #{i + 1:2d} {name(i):>10s} {''.join(map(str, a))} ↔ "
              f"#{i + 2:2d} {name(i + 1):>10s} {''.join(map(str, b))}  [{rel}]")

    print(f"\nSummary: {inversions} inversions, {complements} complements, {neither} neither")

    # Palindromic hexagrams (self-inverse)
    palindromes = []
    for i in range(N):
        b = hexagrams[i]
        if b == invert(b):
            palindromes.append((i + 1, name(i), "".join(map(str, b))))

    print(f"\nPalindromic (self-inverse) hexagrams:")
    for num, nm, bs in palindromes:
        print(f"  #{num:2d} {nm:>10s} {bs}")


# ─── 5. Trigram Grammar ─────────────────────────────────────────────────────

def analyze_trigram_grammar():
    print("\n" + "=" * 70)
    print("5. TRIGRAM GRAMMAR")
    print("=" * 70)

    tri_names = list(TRIGRAMS.keys())
    tri_labels = [TRIGRAMS[t] for t in tri_names]
    tri_idx = {t: i for i, t in enumerate(tri_names)}

    # Build transition matrices
    lower_trans = np.zeros((8, 8), dtype=int)
    upper_trans = np.zeros((8, 8), dtype=int)

    for i in range(N - 1):
        lt_from = lower_trigram(i)
        lt_to = lower_trigram(i + 1)
        lower_trans[tri_idx[lt_from]][tri_idx[lt_to]] += 1

        ut_from = upper_trigram(i)
        ut_to = upper_trigram(i + 1)
        upper_trans[tri_idx[ut_from]][tri_idx[ut_to]] += 1

    print("\nLower trigram transition matrix:")
    header = "         " + " ".join(f"{l[:5]:>5s}" for l in tri_labels)
    print(header)
    for i, label in enumerate(tri_labels):
        row = " ".join(f"{lower_trans[i][j]:5d}" for j in range(8))
        print(f"  {label[:5]:>5s}  {row}")

    print("\nUpper trigram transition matrix:")
    print(header)
    for i, label in enumerate(tri_labels):
        row = " ".join(f"{upper_trans[i][j]:5d}" for j in range(8))
        print(f"  {label[:5]:>5s}  {row}")

    # Self-transitions (same trigram consecutive)
    lower_self = sum(lower_trans[i][i] for i in range(8))
    upper_self = sum(upper_trans[i][i] for i in range(8))
    print(f"\nSelf-transitions: lower={lower_self}/{N - 1}, upper={upper_self}/{N - 1}")

    # Most common transitions
    print(f"\nTop 10 lower trigram transitions:")
    transitions = []
    for i in range(8):
        for j in range(8):
            if lower_trans[i][j] > 0:
                transitions.append((lower_trans[i][j], tri_labels[i], tri_labels[j]))
    transitions.sort(reverse=True)
    for count, f, t in transitions[:10]:
        print(f"  {f:>7s} → {t:<7s}: {count}")

    print(f"\nTop 10 upper trigram transitions:")
    transitions = []
    for i in range(8):
        for j in range(8):
            if upper_trans[i][j] > 0:
                transitions.append((upper_trans[i][j], tri_labels[i], tri_labels[j]))
    transitions.sort(reverse=True)
    for count, f, t in transitions[:10]:
        print(f"  {f:>7s} → {t:<7s}: {count}")

    # Zero transitions (forbidden?)
    print(f"\nZero-count lower trigram transitions (potential forbidden):")
    for i in range(8):
        for j in range(8):
            if lower_trans[i][j] == 0:
                print(f"  {tri_labels[i]:>7s} → {tri_labels[j]:<7s}")

    print(f"\nZero-count upper trigram transitions (potential forbidden):")
    for i in range(8):
        for j in range(8):
            if upper_trans[i][j] == 0:
                print(f"  {tri_labels[i]:>7s} → {tri_labels[j]:<7s}")

    return lower_trans, upper_trans


# ─── 6. Spectral / Periodicity ──────────────────────────────────────────────

def analyze_spectral(weights):
    print("\n" + "=" * 70)
    print("6. SPECTRAL / PERIODICITY")
    print("=" * 70)

    weights = np.array(weights, dtype=float)

    # FFT of weight sequence
    w_centered = weights - np.mean(weights)
    fft_w = np.fft.rfft(w_centered)
    power = np.abs(fft_w) ** 2
    freqs = np.fft.rfftfreq(N)

    print(f"\nWeight sequence FFT — top 10 frequencies by power:")
    order = np.argsort(power)[::-1]
    for rank, idx in enumerate(order[:10]):
        period = 1.0 / freqs[idx] if freqs[idx] > 0 else float("inf")
        print(f"  Rank {rank + 1}: freq={freqs[idx]:.4f}, period={period:.1f}, power={power[idx]:.1f}")

    # Per-line FFT
    hexagrams = np.array(all_bits(), dtype=float)
    print(f"\nPer-line dominant periods:")
    for line in range(LINES):
        line_seq = hexagrams[:, line]
        centered = line_seq - np.mean(line_seq)
        fft_l = np.fft.rfft(centered)
        pwr = np.abs(fft_l) ** 2
        # Skip DC component
        pwr[0] = 0
        top_idx = np.argmax(pwr)
        period = 1.0 / freqs[top_idx] if freqs[top_idx] > 0 else float("inf")
        print(f"  Line {line + 1}: dominant period={period:.1f} hexagrams, power={pwr[top_idx]:.1f}")

    # Autocorrelation of weight sequence
    autocorr = np.correlate(w_centered, w_centered, mode="full")
    autocorr = autocorr[N - 1:]  # Keep positive lags
    autocorr = autocorr / autocorr[0]  # Normalize

    print(f"\nWeight sequence autocorrelation (first 16 lags):")
    for lag in range(min(16, len(autocorr))):
        bar_len = int(abs(autocorr[lag]) * 30)
        sign = "+" if autocorr[lag] >= 0 else "-"
        bar = sign * bar_len
        print(f"  Lag {lag:2d}: {autocorr[lag]:+.3f}  {bar}")


# ─── 7. Information Content ─────────────────────────────────────────────────

def analyze_information():
    print("\n" + "=" * 70)
    print("7. INFORMATION CONTENT")
    print("=" * 70)

    hexagrams = all_bits()

    # Transition entropy (how predictable is the next hexagram?)
    # Use bigram entropy on various representations

    # Weight transitions
    weight_seq = [weight(h) for h in hexagrams]
    weight_bigrams = [(weight_seq[i], weight_seq[i + 1]) for i in range(N - 1)]
    wbc = Counter(weight_bigrams)
    total = sum(wbc.values())
    weight_bigram_entropy = -sum((c / total) * np.log2(c / total) for c in wbc.values())
    print(f"\nWeight bigram entropy: {weight_bigram_entropy:.2f} bits")

    # Max possible entropy for weight bigrams
    n_unique_bigrams = len(wbc)
    max_entropy = np.log2(n_unique_bigrams)
    print(f"Max entropy ({n_unique_bigrams} unique bigrams): {max_entropy:.2f} bits")
    print(f"Efficiency: {weight_bigram_entropy / max_entropy:.2f}")

    # Lower trigram transition entropy
    lt_seq = [lower_trigram(i) for i in range(N)]
    lt_bigrams = [(lt_seq[i], lt_seq[i + 1]) for i in range(N - 1)]
    ltc = Counter(lt_bigrams)
    total = sum(ltc.values())
    lt_entropy = -sum((c / total) * np.log2(c / total) for c in ltc.values())
    print(f"\nLower trigram bigram entropy: {lt_entropy:.2f} bits")

    # Upper trigram transition entropy
    ut_seq = [upper_trigram(i) for i in range(N)]
    ut_bigrams = [(ut_seq[i], ut_seq[i + 1]) for i in range(N - 1)]
    utc = Counter(ut_bigrams)
    total = sum(utc.values())
    ut_entropy = -sum((c / total) * np.log2(c / total) for c in utc.values())
    print(f"Upper trigram bigram entropy: {ut_entropy:.2f} bits")

    # Mutual information between upper and lower trigram transitions
    # MI(lower_trans, upper_trans) = H(lower) + H(upper) - H(lower, upper)
    joint_bigrams = [
        ((lt_seq[i], lt_seq[i + 1]), (ut_seq[i], ut_seq[i + 1]))
        for i in range(N - 1)
    ]
    jc = Counter(joint_bigrams)
    total = sum(jc.values())
    joint_entropy = -sum((c / total) * np.log2(c / total) for c in jc.values())
    mi = lt_entropy + ut_entropy - joint_entropy
    print(f"\nJoint trigram transition entropy: {joint_entropy:.2f} bits")
    print(f"Mutual information (lower↔upper transitions): {mi:.2f} bits")

    # Compressibility: compare to random permutations
    # Measure total Hamming distance as a proxy
    kw_total_hamming = sum(hamming(hexagrams[i], hexagrams[i + 1]) for i in range(N - 1))

    rng = np.random.default_rng(42)
    random_totals = []
    for _ in range(10000):
        perm = rng.permutation(N)
        perm_hex = [hexagrams[p] for p in perm]
        total_h = sum(hamming(perm_hex[i], perm_hex[i + 1]) for i in range(N - 1))
        random_totals.append(total_h)

    print(f"\nTotal Hamming distance:")
    print(f"  King Wen:  {kw_total_hamming}")
    print(f"  Random:    {np.mean(random_totals):.1f} +/- {np.std(random_totals):.1f}")
    print(f"  Z-score:   {(kw_total_hamming - np.mean(random_totals)) / np.std(random_totals):.2f}")

    # Sequence uniqueness: are there repeated subsequences?
    bit_strings = ["".join(map(str, h)) for h in hexagrams]
    for length in [2, 3, 4]:
        subseqs = [tuple(bit_strings[i:i + length]) for i in range(N - length + 1)]
        sc = Counter(subseqs)
        repeats = {k: v for k, v in sc.items() if v > 1}
        print(f"\n  Repeated {length}-grams: {len(repeats)}")
        for seq, count in sorted(repeats.items(), key=lambda x: -x[1])[:5]:
            names = [f"#{bit_strings.index(s) + 1}" for s in seq]
            print(f"    {' → '.join(seq)}: {count} times")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("KING WEN SEQUENCE — NUMERICAL ANALYSIS")
    print("=" * 70)

    weights = analyze_basic()
    h_dists = analyze_transitions()
    analyze_baselines(h_dists)
    analyze_pairing()
    analyze_trigram_grammar()
    analyze_spectral(weights)
    analyze_information()

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
