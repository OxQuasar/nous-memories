"""
Hypercube representation of the King Wen sequence.

Each hexagram is a vertex of the 6-dimensional hypercube {0,1}^6.
The King Wen sequence is a path through all 64 vertices.
Test what offset 19, offset 27 symmetry, and other findings mean geometrically.
"""

import numpy as np
from collections import Counter
from itertools import combinations
from sequence import KING_WEN, bits, all_bits, name, lower_trigram, upper_trigram, trigram_name
from timewave import first_order_differences

N_HEX = 64
DIMS = 6
N_TRIALS = 10000
RNG = np.random.default_rng(42)


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ─── 1. Path Through the Hypercube ──────────────────────────────────────────

def analyze_path():
    print("=" * 70)
    print("1. PATH THROUGH THE HYPERCUBE")
    print("=" * 70)

    hexagrams = all_bits()
    vertices = np.array(hexagrams)  # 64 x 6

    # Path properties
    h = first_order_differences()

    # How much of the hypercube does the path cover?
    unique_vertices = len(set(tuple(v) for v in vertices))
    print(f"\n  Unique vertices visited: {unique_vertices}/64 (should be 64)")

    # Is the path Hamiltonian? (visits every vertex exactly once)
    print(f"  Hamiltonian path: {'YES' if unique_vertices == 64 else 'NO'}")

    # Centroid of path through time
    # Split into quarters and measure centroid drift
    quarter = N_HEX // 4
    for i, label in enumerate(["Q1 (1-16)", "Q2 (17-32)", "Q3 (33-48)", "Q4 (49-64)"]):
        start, end = i * quarter, (i + 1) * quarter
        centroid = vertices[start:end].mean(axis=0)
        print(f"  Centroid {label}: [{', '.join(f'{c:.2f}' for c in centroid)}]")

    overall_centroid = vertices.mean(axis=0)
    print(f"  Overall centroid:   [{', '.join(f'{c:.2f}' for c in overall_centroid)}]")
    print(f"  (Perfect balance = [0.50, 0.50, 0.50, 0.50, 0.50, 0.50])")

    # Per-dimension balance: does each bit appear equally as 0/1?
    print(f"\n  Per-dimension balance (fraction yang):")
    for d in range(DIMS):
        frac = vertices[:, d].mean()
        print(f"    Dim {d + 1} (line {d + 1}): {frac:.3f}")

    # Edge types used: how many of the path's transitions are along
    # single edges (Hamming 1), double edges (Hamming 2), etc.
    print(f"\n  Path step Hamming distance distribution:")
    hc = Counter(h)
    for dist in sorted(hc):
        # Total possible pairs at this distance in the hypercube
        from math import comb
        possible = comb(DIMS, dist)
        print(f"    Hamming {dist}: {hc[dist]} steps "
              f"({possible} possible {dist}-bit flips per vertex)")

    return vertices


# ─── 2. Offset 19 in Hypercube Geometry ──────────────────────────────────────

def analyze_offset19(vertices):
    print("\n" + "=" * 70)
    print("2. OFFSET 19 IN HYPERCUBE GEOMETRY")
    print("=" * 70)

    # For each pair (k, k+19 mod 64), compute Hamming distance in hypercube
    offset_19_dists = []
    for k in range(N_HEX):
        j = (k + 19) % N_HEX
        d = hamming(vertices[k], vertices[j])
        offset_19_dists.append(d)

    print(f"\n  Hamming distances between offset-19 pairs (in hypercube):")
    print(f"    Mean: {np.mean(offset_19_dists):.2f}")
    print(f"    Distribution: {Counter(offset_19_dists)}")

    # Compare: what's the expected Hamming distance for random offset pairs?
    all_offset_means = []
    for d in range(1, N_HEX):
        dists = [hamming(vertices[k], vertices[(k + d) % N_HEX]) for k in range(N_HEX)]
        all_offset_means.append((d, np.mean(dists)))

    all_offset_means.sort(key=lambda x: x[1])
    print(f"\n  Mean Hamming distance by offset (top 10 closest):")
    for d, mean_h in all_offset_means[:10]:
        marker = " <-- offset 19" if d == 19 else ""
        marker += " <-- offset 27" if d == 27 else ""
        marker += " <-- antipodal" if d == 32 else ""
        print(f"    d={d:2d}: mean Hamming={mean_h:.2f}{marker}")

    rank_19 = next(i + 1 for i, (d, _) in enumerate(all_offset_means) if d == 19)
    print(f"\n  Offset 19 rank (by closeness): {rank_19}/63")

    # Which bits differ most between offset-19 pairs?
    bit_diffs = np.zeros(DIMS)
    for k in range(N_HEX):
        j = (k + 19) % N_HEX
        for b in range(DIMS):
            if vertices[k][b] != vertices[j][b]:
                bit_diffs[b] += 1

    print(f"\n  Per-bit differences in offset-19 pairs:")
    for b in range(DIMS):
        print(f"    Bit {b + 1}: {int(bit_diffs[b])}/64 pairs differ")

    # XOR pattern: what's the most common XOR between offset-19 pairs?
    xor_patterns = []
    for k in range(N_HEX):
        j = (k + 19) % N_HEX
        xor = tuple(int(vertices[k][b]) ^ int(vertices[j][b]) for b in range(DIMS))
        xor_patterns.append(xor)

    xor_counts = Counter(xor_patterns)
    print(f"\n  Most common XOR patterns (offset-19 pairs):")
    for pattern, count in xor_counts.most_common(10):
        bits_str = ''.join(map(str, pattern))
        n_flips = sum(pattern)
        print(f"    {bits_str} ({n_flips} flips): {count} pairs")


# ─── 3. Offset 27 Symmetry in Hypercube ─────────────────────────────────────

def analyze_offset27(vertices):
    print("\n" + "=" * 70)
    print("3. OFFSET 27 SYMMETRY IN HYPERCUBE GEOMETRY")
    print("=" * 70)

    # The ring symmetry at offset 27 means: h[k] ≈ h_rev[(k+27) mod 64]
    # In hypercube terms: the path from vertex k to vertex k+1 has similar
    # Hamming distance as the path from vertex (64-k-27) to vertex (64-k-27-1)
    # But let's also check if offset 27 corresponds to a hypercube automorphism

    # Test: is there a fixed bit transformation T such that
    # vertex[k] ≈ T(vertex[(k+27) mod 64]) for all k?
    # Try all 2^6 = 64 possible XOR masks (bit flips)
    # and all 6! = 720 possible bit permutations (too many — try XOR only first)

    print(f"\n  Testing XOR masks: vertex[k] XOR mask ≈ vertex[(k+27) mod 64]?")
    best_mask = None
    best_matches = 0
    for mask_int in range(64):
        mask = [(mask_int >> b) & 1 for b in range(DIMS)]
        matches = 0
        for k in range(N_HEX):
            j = (k + 27) % N_HEX
            transformed = tuple(vertices[k][b] ^ mask[b] for b in range(DIMS))
            if transformed == tuple(vertices[j]):
                matches += 1
        if matches > best_matches:
            best_matches = matches
            best_mask = mask

    mask_str = ''.join(map(str, best_mask))
    print(f"    Best XOR mask: {mask_str} ({sum(best_mask)} flips)")
    print(f"    Matches: {best_matches}/64")

    # Monte Carlo: how many matches for random offsets with best XOR?
    random_matches = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(N_HEX)
        best_m = 0
        for mask_int in range(64):
            mask = [(mask_int >> b) & 1 for b in range(DIMS)]
            m = 0
            for k in range(N_HEX):
                j = perm[(k + 27) % N_HEX]
                transformed = tuple(vertices[k][b] ^ mask[b] for b in range(DIMS))
                if transformed == tuple(vertices[j]):
                    m += 1
            best_m = max(best_m, m)
        random_matches.append(best_m)

    random_matches = np.array(random_matches)
    p_value = np.mean(random_matches >= best_matches)
    print(f"\n    Monte Carlo (n={N_TRIALS}):")
    print(f"      Random best matches: mean={np.mean(random_matches):.2f}, "
          f"std={np.std(random_matches):.2f}")
    print(f"      King Wen matches: {best_matches}")
    print(f"      p-value: {p_value:.4f}")

    # Also test: does offset 27 preserve Hamming neighborhoods?
    # For each vertex k, compare its Hamming neighbors to vertex (k+27)'s neighbors
    print(f"\n  Neighborhood preservation at offset 27:")
    preserved = 0
    total = 0
    for k in range(N_HEX):
        j = (k + 27) % N_HEX
        # Neighbors of k on the path (±1, ±2 steps)
        k_neighborhood = set()
        j_neighborhood = set()
        for step in [-2, -1, 1, 2]:
            k_neighbor = (k + step) % N_HEX
            j_neighbor = (j + step) % N_HEX
            k_neighborhood.add(hamming(vertices[k], vertices[k_neighbor]))
            j_neighborhood.add(hamming(vertices[j], vertices[j_neighbor]))
        if k_neighborhood == j_neighborhood:
            preserved += 1
        total += 1

    print(f"    Positions with preserved Hamming neighborhood: {preserved}/{total}")


# ─── 4. Geometric Structure of Coupled Pairs ────────────────────────────────

def analyze_pair_geometry(vertices):
    print("\n" + "=" * 70)
    print("4. GEOMETRIC STRUCTURE OF COUPLED PAIRS")
    print("=" * 70)

    # The King Wen pairs (inversion/complement) — how do they sit in the hypercube?
    print(f"\n  Inversion pairs in hypercube:")
    inv_dists = []
    comp_dists = []
    for i in range(0, N_HEX, 2):
        v1 = vertices[i]
        v2 = vertices[i + 1]
        d = hamming(v1, v2)
        is_palindrome = list(v1) == list(reversed(list(v1)))

        if is_palindrome:
            comp_dists.append(d)
        else:
            inv_dists.append(d)

    print(f"    Inversion pair Hamming distances: mean={np.mean(inv_dists):.2f}, "
          f"dist={Counter(inv_dists)}")
    print(f"    Complement pair Hamming distances: mean={np.mean(comp_dists):.2f}, "
          f"dist={Counter(comp_dists)}")

    # Faces of the hypercube: which 2D faces does the path traverse?
    # A face is defined by fixing 4 bits and varying 2
    print(f"\n  2D face usage (fixing 4 bits, varying 2):")
    face_counts = Counter()
    for k in range(N_HEX):
        # For each pair of dimensions, what face is this vertex on?
        for d1, d2 in combinations(range(DIMS), 2):
            fixed = tuple(vertices[k][d] for d in range(DIMS) if d != d1 and d != d2)
            face_counts[(d1, d2, fixed)] += 1

    # How many faces have all 4 vertices visited?
    total_faces = 0
    full_faces = 0
    for (d1, d2, fixed), count in face_counts.items():
        total_faces += 1
        if count == 4:
            full_faces += 1

    # Each pair of dims has 2^4 = 16 faces, each face has 4 vertices
    n_dim_pairs = len(list(combinations(range(DIMS), 2)))
    print(f"    Total 2D faces: {total_faces} (15 dim-pairs × 16 faces = {n_dim_pairs * 16})")
    print(f"    Fully visited faces (all 4 vertices): {full_faces}")

    # Distribution of visits per face
    visit_dist = Counter(face_counts.values())
    print(f"    Visits per face distribution: {dict(sorted(visit_dist.items()))}")


# ─── 5. Subcube Residence Time ───────────────────────────────────────────────

def analyze_subcubes(vertices):
    print("\n" + "=" * 70)
    print("5. SUBCUBE RESIDENCE AND TRAJECTORY STRUCTURE")
    print("=" * 70)

    # Split hypercube by each dimension: how long does the path stay
    # on one side (bit=0) vs the other (bit=1)?
    print(f"\n  Run lengths per dimension (consecutive steps on same side):")
    for d in range(DIMS):
        bits_seq = [int(vertices[k][d]) for k in range(N_HEX)]
        runs = []
        current_run = 1
        for i in range(1, N_HEX):
            if bits_seq[i] == bits_seq[i - 1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)

        print(f"    Dim {d + 1}: {len(runs)} runs, "
              f"mean length={np.mean(runs):.1f}, "
              f"max={max(runs)}, "
              f"runs={runs}")

    # 3D subcube residence: split by upper/lower trigram
    print(f"\n  Upper trigram sequence (path through upper 3-cube):")
    upper_seq = [upper_trigram(k) for k in range(N_HEX)]
    upper_runs = []
    current = upper_seq[0]
    run_len = 1
    for i in range(1, N_HEX):
        if upper_seq[i] == current:
            run_len += 1
        else:
            upper_runs.append((current, trigram_name(current), run_len))
            current = upper_seq[i]
            run_len = 1
    upper_runs.append((current, trigram_name(current), run_len))

    print(f"    {len(upper_runs)} runs")
    for tri, nm, length in upper_runs:
        bar = "#" * length
        print(f"      {nm:>7s} ({tri}): {length} {bar}")

    print(f"\n  Lower trigram sequence (path through lower 3-cube):")
    lower_seq = [lower_trigram(k) for k in range(N_HEX)]
    lower_runs = []
    current = lower_seq[0]
    run_len = 1
    for i in range(1, N_HEX):
        if lower_seq[i] == current:
            run_len += 1
        else:
            lower_runs.append((current, trigram_name(current), run_len))
            current = lower_seq[i]
            run_len = 1
    lower_runs.append((current, trigram_name(current), run_len))

    print(f"    {len(lower_runs)} runs")
    for tri, nm, length in lower_runs:
        bar = "#" * length
        print(f"      {nm:>7s} ({tri}): {length} {bar}")


# ─── 6. Offset 19 and 27 as Hypercube Operations ────────────────────────────

def analyze_operations(vertices):
    print("\n" + "=" * 70)
    print("6. OFFSETS AS HYPERCUBE OPERATIONS")
    print("=" * 70)

    # For each offset, find the best-fit linear map (bit permutation + XOR)
    # that transforms vertex[k] to vertex[(k+d) mod 64]
    # Test bit permutations: does permuting dimensions + XOR explain the mapping?

    for offset in [19, 27, 32, 1]:
        print(f"\n  Offset {offset}:")

        # Collect (source, target) vertex pairs
        pairs = [(tuple(vertices[k]), tuple(vertices[(k + offset) % N_HEX]))
                 for k in range(N_HEX)]

        # Per-bit analysis: for each target bit, which source bits predict it?
        print(f"    Per-bit correlation (target bit vs each source bit):")
        src = np.array([p[0] for p in pairs])
        tgt = np.array([p[1] for p in pairs])

        for tb in range(DIMS):
            corrs = []
            for sb in range(DIMS):
                # XOR match: how often does source_bit == target_bit?
                match_rate = np.mean(src[:, sb] == tgt[:, tb])
                # Also check complement: source_bit == NOT target_bit
                comp_rate = np.mean(src[:, sb] != tgt[:, tb])
                best = max(match_rate, comp_rate)
                is_comp = comp_rate > match_rate
                corrs.append((sb, best, is_comp))

            corrs.sort(key=lambda x: -x[1])
            best_sb, best_rate, is_comp = corrs[0]
            comp_str = " (complemented)" if is_comp else ""
            print(f"      Target bit {tb + 1} ← Source bit {best_sb + 1}: "
                  f"{best_rate:.3f} match{comp_str}")

        # Overall: what fraction of bits can be predicted from a permutation+XOR?
        # Greedy assignment
        used_src = set()
        total_correct = 0
        assignments = []
        for tb in range(DIMS):
            best_rate = 0
            best_sb = -1
            best_comp = False
            for sb in range(DIMS):
                if sb in used_src:
                    continue
                match = np.mean(src[:, sb] == tgt[:, tb])
                comp = np.mean(src[:, sb] != tgt[:, tb])
                rate = max(match, comp)
                if rate > best_rate:
                    best_rate = rate
                    best_sb = sb
                    best_comp = comp > match
            used_src.add(best_sb)
            correct = int(best_rate * N_HEX)
            total_correct += correct
            assignments.append((tb, best_sb, best_comp, best_rate))

        print(f"    Greedy permutation+XOR assignment:")
        for tb, sb, comp, rate in assignments:
            op = "NOT " if comp else ""
            print(f"      Target bit {tb + 1} = {op}Source bit {sb + 1} "
                  f"({rate:.3f})")
        print(f"    Total correct bits: {total_correct}/{N_HEX * DIMS} "
              f"({total_correct / (N_HEX * DIMS) * 100:.1f}%)")


# ─── 7. Forward vs Backward Path Comparison ──────────────────────────────────

def analyze_forward_backward(vertices):
    print("\n" + "=" * 70)
    print("7. FORWARD vs BACKWARD PATH COMPARISON")
    print("=" * 70)

    h_fwd = first_order_differences()  # h[k] = hamming(v[k], v[k+1])
    h_bwd = h_fwd[::-1]               # reversed = hamming(v[63-k], v[63-k-1])

    # --- 7a. Transition intensity correlation at each rotation ---
    print(f"\n  7a. Forward vs rotated-backward transition correlation:")
    best_corr = -1
    best_rot = -1
    corrs = []
    for r in range(N_HEX):
        h_rot = np.array([h_bwd[(k + r) % N_HEX] for k in range(N_HEX)])
        c = np.corrcoef(h_fwd, h_rot)[0, 1]
        corrs.append((r, c))
        if c > best_corr:
            best_corr = c
            best_rot = r

    corrs.sort(key=lambda x: -x[1])
    print(f"    Best rotation: {best_rot} (r={best_corr:.3f})")
    print(f"    Top 5 rotations:")
    for r, c in corrs[:5]:
        print(f"      rotation {r:2d}: r={c:.3f}")
    print(f"    Rotation 27: r={next(c for rot, c in corrs if rot == 27):.3f}")
    print(f"    Rotation  0: r={next(c for rot, c in corrs if rot == 0):.3f}")

    # --- 7b. Hamming distance match at rotation 27 ---
    print(f"\n  7b. Position-by-position match at rotation 27:")
    exact = 0
    off_by_1 = 0
    for k in range(N_HEX):
        fwd = h_fwd[k]
        bwd = h_bwd[(k + 27) % N_HEX]
        if fwd == bwd:
            exact += 1
        elif abs(fwd - bwd) <= 1:
            off_by_1 += 1
    print(f"    Exact matches: {exact}/64")
    print(f"    Within ±1: {exact + off_by_1}/64")
    print(f"    Expected exact (random): ~{sum(Counter(h_fwd).values()) ** 2 / N_HEX / len(set(h_fwd)):.0f}/64")

    # Monte Carlo for exact match count
    exact_null = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(h_fwd)
        e = sum(1 for k in range(N_HEX) if h_fwd[k] == perm[(k + 27) % N_HEX])
        exact_null.append(e)
    exact_null = np.array(exact_null)
    p = np.mean(exact_null >= exact)
    print(f"    Monte Carlo: mean exact={np.mean(exact_null):.1f}, p={p:.4f}")

    # --- 7c. Subcube trajectory comparison ---
    print(f"\n  7c. Trigram trajectory: forward vs backward")

    fwd_upper = [upper_trigram(k) for k in range(N_HEX)]
    bwd_upper = fwd_upper[::-1]
    fwd_lower = [lower_trigram(k) for k in range(N_HEX)]
    bwd_lower = fwd_lower[::-1]

    # Trigram match at each rotation
    best_upper_rot = -1
    best_upper_match = 0
    best_lower_rot = -1
    best_lower_match = 0
    for r in range(N_HEX):
        upper_match = sum(1 for k in range(N_HEX)
                          if fwd_upper[k] == bwd_upper[(k + r) % N_HEX])
        lower_match = sum(1 for k in range(N_HEX)
                          if fwd_lower[k] == bwd_lower[(k + r) % N_HEX])
        if upper_match > best_upper_match:
            best_upper_match = upper_match
            best_upper_rot = r
        if lower_match > best_lower_match:
            best_lower_match = lower_match
            best_lower_rot = r

    print(f"    Upper trigram: best match at rotation {best_upper_rot} "
          f"({best_upper_match}/64 positions)")
    print(f"    Lower trigram: best match at rotation {best_lower_rot} "
          f"({best_lower_match}/64 positions)")

    # Monte Carlo
    upper_null = []
    lower_null = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(N_HEX)
        um = max(sum(1 for k in range(N_HEX)
                     if fwd_upper[k] == fwd_upper[perm[(k + r) % N_HEX]])
                 for r in range(N_HEX))
        lm = max(sum(1 for k in range(N_HEX)
                     if fwd_lower[k] == fwd_lower[perm[(k + r) % N_HEX]])
                 for r in range(N_HEX))
        upper_null.append(um)
        lower_null.append(lm)

    upper_null = np.array(upper_null)
    lower_null = np.array(lower_null)
    print(f"    Upper MC: mean best match={np.mean(upper_null):.1f}, "
          f"p={np.mean(upper_null >= best_upper_match):.4f}")
    print(f"    Lower MC: mean best match={np.mean(lower_null):.1f}, "
          f"p={np.mean(lower_null >= best_lower_match):.4f}")

    # --- 7d. Centroid drift: forward vs backward ---
    print(f"\n  7d. Centroid drift symmetry:")
    print(f"    Forward cumulative centroid (8-hex windows):")
    window = 8
    for i in range(0, N_HEX, window):
        c = vertices[i:i + window].mean(axis=0)
        label = f"    [{i + 1:2d}-{i + window:2d}]"
        print(f"    {label}: [{', '.join(f'{x:.2f}' for x in c)}]")

    print(f"    Backward cumulative centroid (8-hex windows):")
    for i in range(0, N_HEX, window):
        # Backward: positions 63, 62, ..., 0
        start = N_HEX - 1 - i - window + 1
        end = N_HEX - 1 - i + 1
        c = vertices[start:end].mean(axis=0)
        label = f"    [{N_HEX - i:2d}-{N_HEX - i - window + 1:2d}]"
        print(f"    {label}: [{', '.join(f'{x:.2f}' for x in c)}]")

    # --- 7e. Path curvature: consecutive angle changes ---
    print(f"\n  7e. Path curvature (consecutive step direction changes):")
    # Direction at step k = XOR between consecutive vertices
    fwd_dirs = []
    bwd_dirs = []
    for k in range(N_HEX - 1):
        fwd_dirs.append(tuple(int(vertices[k + 1][b]) ^ int(vertices[k][b])
                               for b in range(DIMS)))
    for k in range(N_HEX - 1, 0, -1):
        bwd_dirs.append(tuple(int(vertices[k - 1][b]) ^ int(vertices[k][b])
                               for b in range(DIMS)))

    # Curvature = how much direction changes between consecutive steps
    fwd_curv = [hamming(fwd_dirs[k], fwd_dirs[k + 1])
                for k in range(len(fwd_dirs) - 1)]
    bwd_curv = [hamming(bwd_dirs[k], bwd_dirs[k + 1])
                for k in range(len(bwd_dirs) - 1)]

    print(f"    Forward curvature:  mean={np.mean(fwd_curv):.2f}, "
          f"dist={Counter(fwd_curv)}")
    print(f"    Backward curvature: mean={np.mean(bwd_curv):.2f}, "
          f"dist={Counter(bwd_curv)}")

    # Curvature correlation at each rotation
    best_curv_rot = -1
    best_curv_corr = -1
    n = len(fwd_curv)
    for r in range(n):
        bwd_rot = [bwd_curv[(k + r) % n] for k in range(n)]
        c = np.corrcoef(fwd_curv, bwd_rot)[0, 1]
        if c > best_curv_corr:
            best_curv_corr = c
            best_curv_rot = r

    print(f"    Best curvature correlation: rotation {best_curv_rot} "
          f"(r={best_curv_corr:.3f})")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("HYPERCUBE REPRESENTATION OF THE KING WEN SEQUENCE")
    print("=" * 70)

    vertices = analyze_path()
    analyze_offset19(vertices)
    analyze_offset27(vertices)
    analyze_pair_geometry(vertices)
    analyze_subcubes(vertices)
    analyze_operations(vertices)
    analyze_forward_backward(vertices)

    print("\n" + "=" * 70)
    print("HYPERCUBE ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
