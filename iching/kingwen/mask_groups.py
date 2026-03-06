"""
Study hexagrams grouped by their pair mask type.
For each of the 7 masks, what relationships exist between the hexagrams?
"""

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits, name, lower_trigram, upper_trigram, trigram_name

N = 64
DIMS = 6
M = np.array(all_bits())

MASK_NAMES = {
    (1,1,1,1,1,1): "all (complement)",
    (1,1,0,0,1,1): "outer+middle",
    (1,0,1,1,0,1): "outer+inner",
    (0,1,1,1,1,0): "middle+inner",
    (0,1,0,0,1,0): "middle",
    (0,0,1,1,0,0): "inner",
    (1,0,0,0,0,1): "outer",
}

# Build mask groups
groups = defaultdict(list)
for k in range(32):
    a = M[2 * k]
    b = M[2 * k + 1]
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    groups[xor].append({
        'pair_idx': k,
        'pos_a': 2 * k, 'pos_b': 2 * k + 1,
        'a': tuple(a), 'b': tuple(b),
        'num_a': KING_WEN[2 * k][0], 'num_b': KING_WEN[2 * k + 1][0],
        'name_a': KING_WEN[2 * k][1], 'name_b': KING_WEN[2 * k + 1][1],
    })


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ─── 1. Group Composition ────────────────────────────────────────────────────

def analyze_composition():
    print("=" * 70)
    print("1. MASK GROUP COMPOSITION")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mask_str = ''.join(map(str, mask))
        mname = MASK_NAMES.get(mask, "?")
        print(f"\n  Mask {mask_str} — {mname} ({len(g)} pairs, {len(g)*2} hexagrams)")
        print(f"  {'Pair':>4s}  {'#A':>3s} {'Name A':<12s}  {'#B':>3s} {'Name B':<12s}  "
              f"{'Bits A':<7s} {'Bits B':<7s}")
        for p in g:
            bits_a = ''.join(map(str, p['a']))
            bits_b = ''.join(map(str, p['b']))
            print(f"  {p['pair_idx']+1:4d}  {p['num_a']:3d} {p['name_a']:<12s}  "
                  f"{p['num_b']:3d} {p['name_b']:<12s}  {bits_a} {bits_b}")


# ─── 2. Fixed Lines ──────────────────────────────────────────────────────────

def analyze_fixed_lines():
    print("\n" + "=" * 70)
    print("2. FIXED LINES (bits that don't flip within the pair)")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mask_str = ''.join(map(str, mask))
        mname = MASK_NAMES.get(mask, "?")
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]

        if not fixed_dims:
            print(f"\n  Mask {mask_str} — {mname}: no fixed lines (all flip)")
            continue

        print(f"\n  Mask {mask_str} — {mname}: fixed lines = "
              f"{', '.join(f'L{d+1}' for d in fixed_dims)}")

        # What values do the fixed lines take across pairs in this group?
        fixed_patterns = []
        for p in g:
            # Both hexagrams have the same value on fixed lines
            pattern = tuple(p['a'][d] for d in fixed_dims)
            fixed_patterns.append(pattern)

        pattern_counts = Counter(fixed_patterns)
        print(f"  Fixed line patterns:")
        for pattern, count in sorted(pattern_counts.items()):
            pat_str = ''.join(map(str, pattern))
            which = [p['pair_idx'] + 1 for p in g
                     if tuple(p['a'][d] for d in fixed_dims) == pattern]
            print(f"    {pat_str}: {count}x — pairs {which}")

        # Are all possible fixed patterns covered?
        n_possible = 2 ** len(fixed_dims)
        print(f"  Coverage: {len(pattern_counts)}/{n_possible} possible patterns")


# ─── 3. Intra-Group Distances ────────────────────────────────────────────────

def analyze_intra_group():
    print("\n" + "=" * 70)
    print("3. INTRA-GROUP RELATIONSHIPS (between pairs with same mask)")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mask_str = ''.join(map(str, mask))
        mname = MASK_NAMES.get(mask, "?")
        n = len(g)

        print(f"\n  Mask {mask_str} — {mname} ({n} pairs)")

        # Hamming distances between all 'a' hexagrams in the group
        a_hexes = [p['a'] for p in g]
        b_hexes = [p['b'] for p in g]
        all_hexes = a_hexes + b_hexes

        # Pairwise distances between the 'a' hexagrams
        if n > 1:
            a_dists = []
            for i in range(n):
                for j in range(i + 1, n):
                    a_dists.append(hamming(a_hexes[i], a_hexes[j]))
            print(f"  'A' hexagram pairwise Hamming: {Counter(a_dists)}, "
                  f"mean={np.mean(a_dists):.2f}")

        # Do different pairs in this group share any hexagrams?
        all_set = set(all_hexes)
        print(f"  Unique hexagrams: {len(all_set)}/{n*2}")

        # Cross-pair relationship: is pair i's 'a' related to pair j's 'a'?
        # Check if they're inversions, complements, or share trigrams
        if n > 1:
            inv_count = 0
            comp_count = 0
            total = 0
            for i in range(n):
                for j in range(i + 1, n):
                    total += 1
                    if all(a_hexes[i][d] == a_hexes[j][DIMS-1-d] for d in range(DIMS)):
                        inv_count += 1
                    if all(a_hexes[i][d] != a_hexes[j][d] for d in range(DIMS)):
                        comp_count += 1
            print(f"  Cross-pair 'A' relationships: "
                  f"{inv_count}/{total} inversions, "
                  f"{comp_count}/{total} complements")

        # Trigram analysis: what trigrams appear?
        upper_tris = Counter()
        lower_tris = Counter()
        for p in g:
            for hex_bits in [p['a'], p['b']]:
                lt = ''.join(map(str, hex_bits[:3]))
                ut = ''.join(map(str, hex_bits[3:]))
                lower_tris[lt] += 1
                upper_tris[ut] += 1

        print(f"  Upper trigrams: {dict(sorted(upper_tris.items(), key=lambda x: -x[1]))}")
        print(f"  Lower trigrams: {dict(sorted(lower_tris.items(), key=lambda x: -x[1]))}")


# ─── 4. Inter-Group Relationships ────────────────────────────────────────────

def analyze_inter_group():
    print("\n" + "=" * 70)
    print("4. INTER-GROUP RELATIONSHIPS (between mask types)")
    print("=" * 70)

    masks = sorted(groups.keys(), key=lambda m: (-sum(m), m))

    # XOR between mask types (how do mask groups relate to each other?)
    print(f"\n  Mask XOR matrix (Hamming between masks):")
    labels = [MASK_NAMES[m].split()[0] if m in MASK_NAMES else '?' for m in masks]
    print(f"  {'':>14s}", end="")
    for l in labels:
        print(f" {l:>7s}", end="")
    print()
    for i, mi in enumerate(masks):
        print(f"  {labels[i]:>14s}", end="")
        for j, mj in enumerate(masks):
            if i == j:
                print(f"      -", end="")
            else:
                d = hamming(mi, mj)
                print(f"      {d}", end="")
        print()

    # Complementary mask pairs
    print(f"\n  Complementary mask pairs (XOR = 111111):")
    for i, mi in enumerate(masks):
        comp = tuple(1 - b for b in mi)
        if comp in groups and comp > mi:  # avoid duplicates
            print(f"    {MASK_NAMES[mi]:>14s} ↔ {MASK_NAMES[comp]}")

    # Sequence transitions between mask groups
    print(f"\n  Transition frequency between mask groups (consecutive pairs):")
    pair_masks = []
    for k in range(32):
        a = M[2 * k]
        b = M[2 * k + 1]
        xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
        pair_masks.append(xor)

    trans = Counter()
    for k in range(31):
        from_name = MASK_NAMES[pair_masks[k]]
        to_name = MASK_NAMES[pair_masks[k + 1]]
        trans[(from_name, to_name)] += 1

    # Show as matrix
    type_order = ["all (complement)", "outer+middle", "outer+inner",
                  "middle+inner", "middle", "inner", "outer"]
    short = {"all (complement)": "all", "outer+middle": "o+m",
             "outer+inner": "o+i", "middle+inner": "m+i",
             "middle": "mid", "inner": "inn", "outer": "out"}

    print(f"\n  {'FROM →':>10s}", end="")
    for t in type_order:
        print(f" {short[t]:>4s}", end="")
    print()
    for f in type_order:
        print(f"  {short[f]:>10s}", end="")
        for t in type_order:
            c = trans.get((f, t), 0)
            print(f" {c:4d}" if c > 0 else "    ·", end="")
        print()


# ─── 5. Subcube Structure ────────────────────────────────────────────────────

def analyze_subcubes():
    print("\n" + "=" * 70)
    print("5. MASK GROUPS AS HYPERCUBE SUBCUBES")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mask_str = ''.join(map(str, mask))
        mname = MASK_NAMES.get(mask, "?")
        n_flips = sum(mask)
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]
        flip_dims = [i for i in range(DIMS) if mask[i] == 1]

        print(f"\n  Mask {mask_str} — {mname}")

        # Each pair lives in a subcube defined by its fixed lines
        # The subcube has dimension = n_flips
        # How many distinct subcubes does this group occupy?
        subcubes = set()
        for p in g:
            fixed_vals = tuple(p['a'][d] for d in fixed_dims)
            subcubes.add(fixed_vals)

        n_possible_subcubes = 2 ** len(fixed_dims) if fixed_dims else 1
        print(f"  Occupies {len(subcubes)}/{n_possible_subcubes} possible "
              f"{n_flips}D subcubes")

        # Within each subcube, how much of it does the group cover?
        for fixed_vals in sorted(subcubes):
            members = []
            for p in g:
                if tuple(p['a'][d] for d in fixed_dims) == fixed_vals:
                    members.extend([p['a'], p['b']])

            # Project to flip dimensions only
            projected = set()
            for m in members:
                proj = tuple(m[d] for d in flip_dims)
                projected.add(proj)

            n_vertices = 2 ** n_flips
            if fixed_dims:
                fixed_str = ''.join(map(str, fixed_vals))
                print(f"    Fixed={fixed_str}: {len(projected)}/{n_vertices} "
                      f"vertices of {n_flips}D subcube")
            else:
                print(f"    {len(projected)}/{n_vertices} vertices of 6D cube")


# ─── 6. Weight and Balance ───────────────────────────────────────────────────

def analyze_weight():
    print("\n" + "=" * 70)
    print("6. HEXAGRAM WEIGHTS BY MASK GROUP")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mask_str = ''.join(map(str, mask))
        mname = MASK_NAMES.get(mask, "?")

        weights_a = [sum(p['a']) for p in g]
        weights_b = [sum(p['b']) for p in g]
        weight_sums = [wa + wb for wa, wb in zip(weights_a, weights_b)]
        weight_diffs = [abs(wa - wb) for wa, wb in zip(weights_a, weights_b)]

        print(f"\n  Mask {mask_str} — {mname}")
        print(f"    A weights: {weights_a}")
        print(f"    B weights: {weights_b}")
        print(f"    A+B sums:  {weight_sums}  (mean={np.mean(weight_sums):.1f})")
        print(f"    |A-B|:     {weight_diffs}")

        # For complement pairs, A+B should always = 6
        if sum(mask) == 6:
            print(f"    All sums = 6: {all(s == 6 for s in weight_sums)}")


# ─── 7. Sequence Position Patterns ───────────────────────────────────────────

def analyze_positions():
    print("\n" + "=" * 70)
    print("7. SEQUENCE POSITIONS BY MASK GROUP")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mask_str = ''.join(map(str, mask))
        mname = MASK_NAMES.get(mask, "?")
        positions = [p['pair_idx'] + 1 for p in g]
        gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]

        print(f"\n  Mask {mask_str} — {mname}")
        print(f"    Pair positions: {positions}")
        print(f"    Gaps: {gaps}")
        if len(gaps) > 1:
            print(f"    Mean gap: {np.mean(gaps):.1f}, regularity: "
                  f"{'regular' if len(set(gaps)) == 1 else 'irregular'}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("MASK GROUP ANALYSIS OF THE KING WEN SEQUENCE")
    print("=" * 70)

    analyze_composition()
    analyze_fixed_lines()
    analyze_intra_group()
    analyze_inter_group()
    analyze_subcubes()
    analyze_weight()
    analyze_positions()

    print("\n" + "=" * 70)
    print("MASK GROUP ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
