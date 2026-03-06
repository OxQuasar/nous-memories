"""
Line-level analysis of the King Wen sequence.

Track each of the 6 line positions through the 64 hexagrams,
treating each as a binary signal (0=yin, 1=yang).
"""

import numpy as np
from collections import Counter
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
N_TRIALS = 10000
RNG = np.random.default_rng(42)

# 64 x 6 matrix: rows = King Wen order, columns = line positions
M = np.array(all_bits())


# ─── 1. Visualize the Six Line Signals ───────────────────────────────────────

def visualize():
    print("=" * 70)
    print("1. THE SIX LINE SIGNALS")
    print("=" * 70)

    print("\n  Hexagram sequence (yang=█, yin=·):\n")
    print("       " + "".join(f"{k+1:<2}" for k in range(0, N, 2)))
    print("       " + "".join("| " for _ in range(0, N, 2)))

    for line in range(DIMS - 1, -1, -1):  # top line first
        signal = M[:, line]
        row = "".join("█" if b else "·" for b in signal)
        print(f"  L{line+1}:  {row}")

    print()
    # Also show change points (where each line flips)
    print("  Change points (X = line flips from previous hexagram):\n")
    for line in range(DIMS - 1, -1, -1):
        signal = M[:, line]
        changes = [" "] + ["X" if signal[k] != signal[k-1] else "·"
                           for k in range(1, N)]
        print(f"  L{line+1}:  {''.join(changes)}")


# ─── 2. Run Length Analysis ──────────────────────────────────────────────────

def run_lengths():
    print("\n" + "=" * 70)
    print("2. RUN LENGTHS (consecutive same-state)")
    print("=" * 70)

    for line in range(DIMS):
        signal = M[:, line]
        runs = []
        current = signal[0]
        length = 1
        for k in range(1, N):
            if signal[k] == current:
                length += 1
            else:
                runs.append((current, length))
                current = signal[k]
                length = 1
        runs.append((current, length))

        yin_runs = [l for v, l in runs if v == 0]
        yang_runs = [l for v, l in runs if v == 1]
        n_switches = len(runs) - 1

        print(f"\n  Line {line+1}: {n_switches} switches, {len(runs)} runs")
        print(f"    Yin runs:  {yin_runs}  (mean={np.mean(yin_runs):.1f})")
        print(f"    Yang runs: {yang_runs}  (mean={np.mean(yang_runs):.1f})")
        print(f"    Run sequence: ", end="")
        for val, length in runs:
            char = "▓" if val else "░"
            print(char * length, end="")
        print()

    # Compare against random permutations
    print(f"\n  Monte Carlo (expected switches for random permutation of 32 yin + 32 yang):")
    switch_counts = np.zeros((N_TRIALS, DIMS))
    for t in range(N_TRIALS):
        perm = RNG.permutation(N)
        M_perm = M[perm]
        for line in range(DIMS):
            switches = sum(1 for k in range(1, N) if M_perm[k, line] != M_perm[k-1, line])
            switch_counts[t, line] = switches

    actual_switches = [sum(1 for k in range(1, N) if M[k, line] != M[k-1, line])
                       for line in range(DIMS)]

    for line in range(DIMS):
        mean_s = np.mean(switch_counts[:, line])
        std_s = np.std(switch_counts[:, line])
        z = (actual_switches[line] - mean_s) / std_s
        p = np.mean(switch_counts[:, line] <= actual_switches[line])
        print(f"    Line {line+1}: actual={actual_switches[line]}, "
              f"random={mean_s:.1f}±{std_s:.1f}, z={z:.2f}, p={p:.3f}")


# ─── 3. Inter-Line Correlations ──────────────────────────────────────────────

def correlations():
    print("\n" + "=" * 70)
    print("3. INTER-LINE CORRELATIONS")
    print("=" * 70)

    # Correlation between line signals
    print("\n  Pearson correlation between line signals:")
    corr = np.corrcoef(M.T)
    print("        ", end="")
    for j in range(DIMS):
        print(f"  L{j+1}   ", end="")
    print()
    for i in range(DIMS):
        print(f"    L{i+1}", end="")
        for j in range(DIMS):
            if i == j:
                print("     -  ", end="")
            else:
                print(f"  {corr[i,j]:+.3f}", end="")
        print()

    # Co-change: when line i flips, does line j also flip?
    print("\n  Co-change frequency (both lines flip at same step):")
    changes = np.zeros((N - 1, DIMS), dtype=int)
    for k in range(1, N):
        for line in range(DIMS):
            changes[k-1, line] = int(M[k, line] != M[k-1, line])

    print("        ", end="")
    for j in range(DIMS):
        print(f"  L{j+1}  ", end="")
    print()
    for i in range(DIMS):
        print(f"    L{i+1}", end="")
        for j in range(DIMS):
            if i == j:
                total_changes = changes[:, i].sum()
                print(f"   {total_changes:2d}  ", end="")
            else:
                co = np.sum(changes[:, i] & changes[:, j])
                print(f"   {co:2d}  ", end="")
        print()

    # Expected co-change under independence
    print(f"\n  Expected co-change (independent flips):")
    for i in range(DIMS):
        for j in range(i+1, DIMS):
            p_i = changes[:, i].mean()
            p_j = changes[:, j].mean()
            expected = p_i * p_j * (N - 1)
            actual = np.sum(changes[:, i] & changes[:, j])
            print(f"    L{i+1}-L{j+1}: actual={actual}, expected={expected:.1f}, "
                  f"ratio={actual/expected:.2f}")


# ─── 4. Line Symmetries Under Pairing ────────────────────────────────────────

def pairing_symmetry():
    print("\n" + "=" * 70)
    print("4. LINE BEHAVIOR UNDER KING WEN PAIRING")
    print("=" * 70)

    # Adjacent pairs: does line k of hex[n] predict line k of hex[n+1]?
    print("\n  Adjacent pair line relationships (odd→even hex):")
    for line in range(DIMS):
        same = 0
        flipped = 0
        mirror = 0  # line k of hex[n] == line (6-1-k) of hex[n+1]
        for k in range(0, N, 2):
            if M[k, line] == M[k+1, line]:
                same += 1
            else:
                flipped += 1
            if M[k, line] == M[k+1, DIMS - 1 - line]:
                mirror += 1
        print(f"    Line {line+1}: same={same}/32, flipped={flipped}/32, "
              f"mirror(L{line+1}→L{DIMS-line})={mirror}/32")

    # The inversion pattern: line k of hex[n] should equal line (6-1-k) of hex[n+1]
    print(f"\n  Inversion test (L_k[n] == L_(7-k)[n+1] for paired hexagrams):")
    total_match = 0
    total_bits = 0
    for k in range(0, N, 2):
        for line in range(DIMS):
            if M[k, line] == M[k+1, DIMS - 1 - line]:
                total_match += 1
            total_bits += 1
    print(f"    Total: {total_match}/{total_bits} bits match "
          f"({total_match/total_bits*100:.1f}%)")


# ─── 5. Spectral Content ─────────────────────────────────────────────────────

def spectral():
    print("\n" + "=" * 70)
    print("5. SPECTRAL CONTENT OF LINE SIGNALS")
    print("=" * 70)

    print("\n  FFT power spectrum (top 5 frequencies per line):")
    for line in range(DIMS):
        signal = M[:, line].astype(float) - 0.5  # center at 0
        fft = np.fft.rfft(signal)
        power = np.abs(fft) ** 2
        freqs = np.fft.rfftfreq(N, d=1)

        # Skip DC (index 0)
        top_idx = np.argsort(power[1:])[::-1][:5] + 1
        print(f"\n    Line {line+1}:")
        for idx in top_idx:
            period = 1.0 / freqs[idx] if freqs[idx] > 0 else float('inf')
            print(f"      freq={freqs[idx]:.3f} (period={period:.1f}), "
                  f"power={power[idx]:.2f}")

    # Cross-spectral coherence between line pairs
    print(f"\n  Cross-spectral coherence (peak frequency of shared power):")
    for i in range(DIMS):
        for j in range(i+1, DIMS):
            si = M[:, i].astype(float) - 0.5
            sj = M[:, j].astype(float) - 0.5
            fi = np.fft.rfft(si)
            fj = np.fft.rfft(sj)
            cross = fi * np.conj(fj)
            cross_power = np.abs(cross)
            freqs = np.fft.rfftfreq(N, d=1)
            peak = np.argmax(cross_power[1:]) + 1
            period = 1.0 / freqs[peak] if freqs[peak] > 0 else float('inf')
            print(f"    L{i+1}-L{j+1}: peak at period={period:.1f}, "
                  f"power={cross_power[peak]:.2f}")


# ─── 6. Line Signals at Offset 19 and Offset 27 ─────────────────────────────

def offset_analysis():
    print("\n" + "=" * 70)
    print("6. LINE SIGNALS AT KEY OFFSETS")
    print("=" * 70)

    for offset, label in [(19, "offset 19 (coupling)"),
                          (27, "offset 27 (ring symmetry)"),
                          (32, "offset 32 (antipodal)")]:
        print(f"\n  {label}:")
        print(f"    Per-line match rate: M[k] vs M[(k+{offset}) mod 64]")
        for line in range(DIMS):
            match = sum(1 for k in range(N)
                        if M[k, line] == M[(k + offset) % N, line])
            print(f"      Line {line+1}: {match}/64 same ({match/N*100:.1f}%)")

        # Cross-line: does line k at position p match line j at position p+offset?
        print(f"    Cross-line matches (L_i[k] vs L_j[k+{offset}]):")
        best_pairs = []
        for i in range(DIMS):
            for j in range(DIMS):
                match = sum(1 for k in range(N)
                            if M[k, i] == M[(k + offset) % N, j])
                anti = N - match
                best = max(match, anti)
                is_anti = anti > match
                best_pairs.append((i, j, best, is_anti))

        best_pairs.sort(key=lambda x: -x[2])
        for i, j, best, is_anti in best_pairs[:6]:
            op = "≠" if is_anti else "="
            print(f"      L{i+1}[k] {op} L{j+1}[k+{offset}]: "
                  f"{best}/64 ({best/N*100:.1f}%)")


# ─── 7. Line Change Coincidences ─────────────────────────────────────────────

def change_patterns():
    print("\n" + "=" * 70)
    print("7. MULTI-LINE CHANGE PATTERNS")
    print("=" * 70)

    # At each transition, which combination of lines changes?
    changes_per_step = []
    for k in range(1, N):
        changed = tuple(line for line in range(DIMS) if M[k, line] != M[k-1, line])
        changes_per_step.append(changed)

    # How many lines change per step?
    n_changed = [len(c) for c in changes_per_step]
    print(f"\n  Lines changed per step:")
    for n in sorted(set(n_changed)):
        count = n_changed.count(n)
        print(f"    {n} lines: {count} steps")

    # Most common change patterns
    pattern_counts = Counter(changes_per_step)
    print(f"\n  Most common change patterns (top 10):")
    for pattern, count in pattern_counts.most_common(10):
        lines = ", ".join(f"L{l+1}" for l in pattern)
        print(f"    ({lines}): {count} times")

    # Which lines are most/least volatile?
    print(f"\n  Per-line change frequency:")
    for line in range(DIMS):
        freq = sum(1 for c in changes_per_step if line in c)
        print(f"    Line {line+1}: changes {freq}/63 steps ({freq/63*100:.1f}%)")

    # Do inner lines (3,4) behave differently from outer lines (1,6)?
    print(f"\n  Inner (L3,L4) vs outer (L1,L6) vs middle (L2,L5) volatility:")
    inner = sum(1 for c in changes_per_step if 2 in c or 3 in c) / 2
    outer = sum(1 for c in changes_per_step if 0 in c or 5 in c) / 2
    middle = sum(1 for c in changes_per_step if 1 in c or 4 in c) / 2
    print(f"    Outer (L1,L6): {outer:.1f} avg changes")
    print(f"    Middle (L2,L5): {middle:.1f} avg changes")
    print(f"    Inner (L3,L4): {inner:.1f} avg changes")


# ─── 8. Autocorrelation of Line Signals ──────────────────────────────────────

def autocorrelation():
    print("\n" + "=" * 70)
    print("8. AUTOCORRELATION OF LINE SIGNALS")
    print("=" * 70)

    print("\n  Autocorrelation at key lags:")
    print(f"    {'':8s}", end="")
    for lag in [1, 2, 3, 4, 8, 16, 32]:
        print(f"  lag {lag:2d}", end="")
    print()

    for line in range(DIMS):
        signal = M[:, line].astype(float) - 0.5
        print(f"    Line {line+1}:", end="")
        for lag in [1, 2, 3, 4, 8, 16, 32]:
            # Circular autocorrelation
            shifted = np.roll(signal, lag)
            ac = np.corrcoef(signal, shifted)[0, 1]
            print(f"  {ac:+.3f}", end="")
        print()

    # Combined: average autocorrelation across all lines
    print(f"\n    Mean: ", end="")
    for lag in [1, 2, 3, 4, 8, 16, 32]:
        acs = []
        for line in range(DIMS):
            signal = M[:, line].astype(float) - 0.5
            shifted = np.roll(signal, lag)
            acs.append(np.corrcoef(signal, shifted)[0, 1])
        print(f"  {np.mean(acs):+.003f}", end="")
    print()


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("LINE-LEVEL ANALYSIS OF THE KING WEN SEQUENCE")
    print("=" * 70)

    visualize()
    run_lengths()
    correlations()
    pairing_symmetry()
    spectral()
    offset_analysis()
    change_patterns()
    autocorrelation()

    print("\n" + "=" * 70)
    print("LINE ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
