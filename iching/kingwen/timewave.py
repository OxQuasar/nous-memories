"""
Reproduction of the McKenna/Kelley/Watkins Timewave Zero construction.

Three stages:
1. First-order differences from King Wen sequence (h[])
2. 384-point number set generation (w[])
3. Fractal self-similar expansion (f(x))

References:
- kl4yfd/timewave_z3r0 (C implementation)
- blasut/Timewave-Zero-JS (JS port)
- Watkins mathematical formalization
"""

import numpy as np
import math
from sequence import KING_WEN, bits, all_bits

N_HEX = 64
N_DATA = 384
WAVE_FACTOR = 64


# ─── Stage 1: First-Order Differences ───────────────────────────────────────

def hamming(a, b):
    """Hamming distance between two bit lists."""
    return sum(x != y for x, y in zip(a, b))


def first_order_differences():
    """
    h[k] = number of lines changed between hexagram k and hexagram k+1
    in King Wen order (circular: hex 64 wraps to hex 1).
    Returns array of 64 values.
    """
    hexagrams = all_bits()
    h = []
    for k in range(N_HEX):
        next_k = (k + 1) % N_HEX
        h.append(hamming(hexagrams[k], hexagrams[next_k]))
    return h


# ─── Stage 2: 384-Point Number Set Generation ───────────────────────────────

# C-compatible h[] array: 1-based indexing, h[0] = h[64] = wrap value.
# Built from our 0-based first_order_differences().
def make_h_array(fod):
    """Convert 0-based FOD to C-style 1-based h[0..64] array."""
    h = [0] * 65
    for i in range(64):
        h[i + 1] = fod[i]
    h[0] = h[64]  # wrap: h[0] = h[64] per C source
    return h


def mod_64(i):
    """C-compatible mod_64: maps to 0..63, matching C 'while (i<0) i+=64; return i%64'."""
    while i < 0:
        i += 64
    return i % 64


def c_div(a, b):
    """C-style integer division: truncates toward zero (not floor)."""
    return int(a / b) if b != 0 else 0


def exp_minus_one(i):
    """C-compatible: if i<0, i=-i; return i%2 ? -1 : 1."""
    if i < 0:
        i = -i
    return -1 if (i % 2) else 1


def generate_number_set(h_c, half_twist=True):
    """
    Generate 384-point number set from C-style h[] array (1-based, 0..64).

    Exact port of datapoints-watkins.c:
    - C integer division (truncate toward zero)
    - C mod_64 (while negative, add 64)
    - exp_minus_one: |i| % 2 ? -1 : 1

    Three resonance levels:
    - Yao (line): weight 1, period 64
    - Trigram: weight 3, period 192
    - Hexagram: weight 6, period 384

    Args:
        h_c: 65-element array (h[0]..h[64]), 1-based with h[0]=h[64]
        half_twist: if True, apply sign modulation (Kelley set);
                    if False, signs are always +1 (Watkins set)
    """
    h = h_c  # alias for readability
    w = []

    for k in range(N_DATA):
        # C integer division for scaled indices
        k3 = c_div(k, 3)
        k6 = c_div(k, 6)

        # Sign modulation (half-twist)
        if half_twist:
            sign1 = exp_minus_one(c_div(k - 1, 32))
            sign3 = exp_minus_one(c_div(k - 3, 96))
            sign6 = exp_minus_one(c_div(k - 6, 192))
        else:
            sign1 = 1
            sign3 = 1
            sign6 = 1

        # Angular term: slope differences at three scales
        a = (sign1
             * (h[mod_64(k - 1)] - h[mod_64(k - 2)]
                + h[mod_64(-k)] - h[mod_64(1 - k)])
             + 3 * sign3
             * (h[mod_64(k3 - 1)] - h[mod_64(k3 - 2)]
                + h[mod_64(-k3)] - h[mod_64(1 - k3)])
             + 6 * sign6
             * (h[mod_64(k6 - 1)] - h[mod_64(k6 - 2)]
                + h[mod_64(-k6)] - h[mod_64(1 - k6)]))

        # Linear term
        b = ((9 - h[mod_64(-k)] - h[mod_64(k - 1)])
             + 3 * (9 - h[mod_64(-k3)] - h[mod_64(k3 - 1)])
             + 6 * (9 - h[mod_64(-k6)] - h[mod_64(k6 - 1)]))

        w.append(abs(a) + abs(b))

    return w


# ─── Stage 3: Fractal Self-Similar Expansion ────────────────────────────────

def v(y, w):
    """
    Interpolate into the 384-point number set.
    Linear interpolation, wrapping modularly.
    """
    i = int(math.fmod(y, N_DATA))
    if i < 0:
        i += N_DATA
    j = (i + 1) % N_DATA
    z = y - math.floor(y)

    if z == 0.0:
        return float(w[i])
    return (w[j] - w[i]) * z + w[i]


def f(x, w, wave_factor=WAVE_FACTOR, precision=50):
    """
    Fractal timewave value at point x.

    Sums self-similar contributions at all scales:
    - Coarse: zoom out by powers of wave_factor
    - Fine: zoom in by powers of wave_factor

    Result normalized by wave_factor^3.
    """
    if x == 0:
        return 0.0

    total = 0.0
    powers = [wave_factor ** i for i in range(precision + 3)]

    # Coarse scales (zooming out)
    for i in range(len(powers)):
        if x < powers[i]:
            break
        total += powers[i] * v(x / powers[i], w)

    # Fine scales (zooming in)
    last_total = 0.0
    for i in range(1, precision + 3):
        last_total = total
        total += v(x * powers[i], w) / powers[i]
        if total != 0.0 and total <= last_total:
            break

    # Normalize
    return total / (wave_factor ** 3)


# ─── Known Kelley Number Set (for validation) ───────────────────────────────

KELLEY_KNOWN = [
    0, 0, 0, 2, 7, 4, 3, 2, 6, 8,
    13, 5, 26, 25, 24, 15, 13, 16, 14, 19,
    17, 24, 20, 25, 63, 60, 56, 55, 47, 53,
    36, 38, 39, 43, 39, 35, 22, 24, 22, 21,
    29, 30, 27, 26, 26, 21, 23, 19, 57, 62,
    61, 55, 57, 57, 35, 50, 40, 29, 28, 26,
    50, 51, 52, 61, 60, 60, 42, 42, 43, 43,
    42, 41, 45, 41, 46, 23, 35, 34, 21, 21,
    19, 51, 40, 49, 29, 29, 31, 40, 36, 33,
    29, 26, 30, 16, 18, 14, 66, 64, 64, 56,
    53, 57, 49, 51, 47, 44, 46, 47, 56, 51,
    53, 25, 37, 30, 31, 28, 30, 36, 35, 22,
    28, 32, 27, 32, 34, 35, 52, 49, 48, 51,
    51, 53, 40, 43, 42, 26, 30, 28, 55, 41,
    53, 52, 51, 47, 61, 64, 65, 39, 41, 41,
    22, 21, 23, 43, 41, 38, 24, 22, 24, 14,
    17, 19, 52, 50, 47, 42, 40, 42, 26, 27,
    27, 34, 38, 33, 44, 44, 42, 41, 40, 37,
    33, 31, 26, 44, 34, 38, 46, 44, 44, 36,
    37, 34, 36, 36, 36, 38, 43, 38, 27, 26,
    30, 32, 37, 29, 50, 49, 48, 29, 37, 36,
    10, 19, 17, 24, 20, 25, 53, 52, 50, 53,
    57, 55, 34, 44, 45, 13, 9, 5, 34, 26,
    32, 31, 41, 42, 31, 32, 30, 21, 19, 23,
    43, 36, 31, 47, 45, 43, 47, 62, 52, 41,
    36, 38, 46, 47, 40, 43, 42, 42, 36, 38,
    43, 53, 52, 53, 47, 49, 48, 47, 41, 44,
    15, 11, 19, 51, 40, 49, 23, 23, 25, 34,
    30, 27, 7, 4, 4, 32, 22, 32, 68, 70,
    66, 68, 79, 71, 43, 45, 41, 38, 40, 41,
    24, 25, 23, 35, 33, 38, 43, 50, 48, 18,
    17, 26, 34, 38, 33, 38, 40, 41, 34, 31,
    30, 33, 33, 35, 28, 23, 22, 26, 30, 26,
    75, 77, 71, 62, 63, 63, 37, 40, 41, 49,
    47, 51, 32, 37, 33, 49, 47, 44, 32, 38,
    28, 38, 39, 37, 22, 20, 17, 44, 50, 40,
    32, 33, 33, 40, 44, 39, 32, 32, 40, 39,
    34, 41, 33, 33, 32, 32, 38, 36, 22, 20,
    20, 12, 13, 10,
]


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("TIMEWAVE ZERO — REPRODUCTION")
    print("=" * 70)

    # Stage 1: First-order differences
    fod = first_order_differences()
    h_c = make_h_array(fod)
    print(f"\nStage 1: First-order differences (h[1..64]):")
    print(f"  {h_c[1:]}")
    print(f"  h[0] (wrap) = {h_c[0]}")
    print(f"  Length: {len(fod)}, Range: [{min(fod)}, {max(fod)}]")

    # Stage 2: Generate number sets
    kelley = generate_number_set(h_c, half_twist=True)
    watkins = generate_number_set(h_c, half_twist=False)

    print(f"\nStage 2a: Kelley number set (with half-twist):")
    print(f"  Length: {len(kelley)}, Range: [{min(kelley)}, {max(kelley)}]")
    print(f"  First 20: {kelley[:20]}")
    print(f"  Last 20:  {kelley[-20:]}")

    print(f"\nStage 2b: Watkins number set (no half-twist):")
    print(f"  Length: {len(watkins)}, Range: [{min(watkins)}, {max(watkins)}]")
    print(f"  First 20: {watkins[:20]}")
    print(f"  Last 20:  {watkins[-20:]}")

    # Validate against known Kelley set
    print(f"\nValidation against known Kelley set:")
    if len(KELLEY_KNOWN) != N_DATA:
        print(f"  WARNING: Known set has {len(KELLEY_KNOWN)} values, expected {N_DATA}")
    matches = sum(1 for a, b in zip(kelley, KELLEY_KNOWN) if a == b)
    mismatches = []
    for i, (a, b) in enumerate(zip(kelley, KELLEY_KNOWN)):
        if a != b:
            mismatches.append((i, a, b))
    print(f"  Matches: {matches}/{min(len(kelley), len(KELLEY_KNOWN))}")
    if mismatches:
        print(f"  First 10 mismatches (idx, ours, known):")
        for idx, ours, known in mismatches[:10]:
            print(f"    [{idx}]: ours={ours}, known={known}")

    # Stage 3: Fractal expansion — sample points
    print(f"\nStage 3: Fractal timewave values (Kelley set):")
    sample_points = [1, 10, 50, 100, 384, 1000, 10000, 100000]
    for x in sample_points:
        val = f(x, kelley)
        print(f"  f({x:>6d}) = {val:.6f}")

    # Compare Kelley vs Watkins wave
    print(f"\nKelley vs Watkins fractal wave comparison:")
    for x in [1, 100, 1000, 10000]:
        vk = f(x, kelley)
        vw = f(x, watkins)
        print(f"  x={x:>5d}: Kelley={vk:.4f}, Watkins={vw:.4f}, diff={abs(vk-vw):.4f}")

    # Statistics of the 384-point set
    print(f"\nKelley number set statistics:")
    ka = np.array(kelley)
    print(f"  Mean:   {ka.mean():.2f}")
    print(f"  Std:    {ka.std():.2f}")
    print(f"  Median: {np.median(ka):.1f}")

    # The wave shape — print as ASCII sparkline
    print(f"\nKelley 384-point wave (ASCII, normalized):")
    max_val = max(kelley)
    cols = 76
    step = N_DATA // cols
    for row in range(8, -1, -1):
        threshold = max_val * row / 8
        line = ""
        for col in range(cols):
            idx = col * step
            if kelley[idx] >= threshold:
                line += "#"
            else:
                line += " "
        print(f"  {threshold:5.0f} |{line}|")
    print(f"        {'─' * cols}")


if __name__ == "__main__":
    main()
