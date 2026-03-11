#!/usr/bin/env python3
"""
Hexagram Lift: PG(2,2) × PG(2,2) Analysis

The factored basis decomposes each hexagram into:
  Position (o, m, i) = (L1, L2, L3) — lower trigram
  Orbit    (ō, m̄, ī) = (L1⊕L6, L2⊕L5, L3⊕L4) — palindromic signature

Recovery: L1=o, L2=m, L3=i, L4=i⊕ī, L5=m⊕m̄, L6=o⊕ō

Each 3-bit component lives in a copy of F₂³, giving the product
PG(2,2) × PG(2,2) as the projective geometry of the 6-bit space.
"""

import json
from collections import defaultdict, Counter
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════

TRIGRAM_ZH = {
    0b000: "坤", 0b001: "震", 0b010: "坎", 0b011: "兌",
    0b100: "艮", 0b101: "離", 0b110: "巽", 0b111: "乾",
}

TRIGRAM_ELEMENT = {
    0b000: "Earth", 0b001: "Wood", 0b010: "Water", 0b011: "Metal",
    0b100: "Earth", 0b101: "Fire", 0b110: "Wood",  0b111: "Metal",
}

# Fano line labels (from iteration 1)
FANO_LINES = {
    0b001: "ker(O)",   0b010: "ker(M)",    0b011: "P=ker(b₀⊕b₁)",
    0b100: "ker(I)",   0b101: "Q=ker(b₀⊕b₂)", 0b110: "H=ker(b₁⊕b₂)",
    0b111: "ker(OMI)",
}

ATLAS_PATH = Path("/home/quasar/nous/memories/iching/atlas/atlas.json")

fmt3 = lambda x: format(x, '03b')
fmt6 = lambda x: format(x, '06b')
popcount = lambda x: bin(x).count('1')


def load_atlas():
    with open(ATLAS_PATH) as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════
# Factored basis
# ═══════════════════════════════════════════════════════════════════════

def hex_lines(h):
    """Extract (L1..L6) from hex_val."""
    return tuple((h >> i) & 1 for i in range(6))

def factored(h):
    """Return (position, orbit) as 3-bit integers."""
    L = hex_lines(h)
    pos = L[0] | (L[1] << 1) | (L[2] << 2)
    orb = (L[0] ^ L[5]) | ((L[1] ^ L[4]) << 1) | ((L[2] ^ L[3]) << 2)
    return pos, orb

def from_factored(pos, orb):
    """Recover hex_val from (position, orbit)."""
    o, m, i_ = (pos >> 0) & 1, (pos >> 1) & 1, (pos >> 2) & 1
    ob, mb, ib = (orb >> 0) & 1, (orb >> 1) & 1, (orb >> 2) & 1
    L = (o, m, i_, i_ ^ ib, m ^ mb, o ^ ob)
    return sum(L[j] << j for j in range(6))

def hu_map(h):
    """互 map in standard encoding."""
    L = hex_lines(h)
    new_L = (L[1], L[2], L[3], L[2], L[3], L[4])
    return sum(new_L[j] << j for j in range(6))

def fano_line_of(v):
    """Which Fano line(s) contain nonzero 3-bit vector v? Returns list of masks."""
    if v == 0:
        return []  # origin is on all lines but not a point of PG(2,2)
    lines = []
    for func_mask in range(1, 8):
        # v is on line ker(func_mask) iff func_mask · v = 0 mod 2
        if popcount(func_mask & v) % 2 == 0:
            lines.append(func_mask)
    return lines

def fano_line_label(mask):
    return FANO_LINES.get(mask, f"mask={fmt3(mask)}")


# ═══════════════════════════════════════════════════════════════════════
# F₂ linear algebra
# ═══════════════════════════════════════════════════════════════════════

def mat_mul_f2(A, B, n=6):
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s ^= A[i][k] & B[k][j]
            C[i][j] = s
    return C

def mat_inv_f2(M, n=6):
    aug = [M[i][:] + [1 if j == i else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if aug[row][col]:
                pivot = row
                break
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for row in range(n):
            if row != col and aug[row][col]:
                for j in range(2 * n):
                    aug[row][j] ^= aug[col][j]
    return [row[n:] for row in aug]

def rank_f2(M, n=6):
    A = [row[:] for row in M]
    r = 0
    for col in range(n):
        pivot = None
        for row in range(r, n):
            if A[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        for row in range(n):
            if row != r and A[row][col]:
                for j in range(n):
                    A[row][j] ^= A[r][j]
        r += 1
    return r


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 1: Product Fano Analysis
# ═══════════════════════════════════════════════════════════════════════

def computation_1():
    print("=" * 70)
    print("COMPUTATION 1: PRODUCT FANO ANALYSIS")
    print("=" * 70)

    atlas = load_atlas()

    # Define the three distinguished lines in each factor
    # H = ker(b₁⊕b₂) = mask 110: points {001, 110, 111} = {O, MI, OMI}
    # P = ker(b₀⊕b₁) = mask 011: points {011, 100, 111} = {OM, I, OMI}
    # Q = ker(b₀⊕b₂) = mask 101: points {010, 101, 111} = {M, OI, OMI}

    line_defs = {
        'H': {'mask': 0b110, 'label': 'ker(m⊕i)', 'condition': lambda t: ((t >> 1) & 1) == ((t >> 2) & 1)},
        'P': {'mask': 0b011, 'label': 'ker(o⊕m)', 'condition': lambda t: ((t >> 0) & 1) == ((t >> 1) & 1)},
        'Q': {'mask': 0b101, 'label': 'ker(o⊕i)', 'condition': lambda t: ((t >> 0) & 1) == ((t >> 2) & 1)},
    }

    # For each pair of lines (one in position, one in orbit), find hexagrams
    print("\n--- HEXAGRAM SETS FOR LINE CONDITIONS ---\n")

    for pos_name, pos_def in line_defs.items():
        for orb_name, orb_def in line_defs.items():
            pos_cond = pos_def['condition']
            orb_cond = orb_def['condition']

            matching = []
            for h in range(64):
                pos, orb = factored(h)
                if pos_cond(pos) and orb_cond(orb):
                    matching.append(h)

            if pos_name == orb_name:  # Only print diagonal and interesting cases
                entry = atlas[str(matching[0])] if matching else None
                basins = Counter()
                for h in matching:
                    basins[atlas[str(h)]['hu_attractor']] += 1

                print(f"  Pos-{pos_name} ∩ Orb-{orb_name}: {len(matching)} hexagrams")
                print(f"    Condition: pos ∈ {pos_def['label']}, orb ∈ {orb_def['label']}")
                hex_list = ", ".join(f"{h}({fmt6(h)})" for h in matching[:8])
                if len(matching) > 8:
                    hex_list += "..."
                print(f"    Hexagrams: {hex_list}")
                basin_str = ", ".join(f"{TRIGRAM_ZH.get(a, str(a))}×{c}" for a, c in sorted(basins.items()))
                print(f"    Basin distribution: {basin_str}")
                print()

    # Now the full intersection table
    print("--- INTERSECTION SIZES (Position-line × Orbit-line) ---\n")
    header = "Pos\\Orb | " + " | ".join(f"{n:>5s}" for n in line_defs) + " | total"
    print(f"  {header}")
    print(f"  {'─' * len(header)}")

    for pos_name, pos_def in line_defs.items():
        row = []
        for orb_name, orb_def in line_defs.items():
            count = sum(1 for h in range(64)
                        if pos_def['condition'](factored(h)[0])
                        and orb_def['condition'](factored(h)[1]))
            row.append(count)
        total = sum(1 for h in range(64) if pos_def['condition'](factored(h)[0]))
        print(f"  {pos_name:>7s} | " + " | ".join(f"{c:5d}" for c in row) + f" | {total:5d}")

    # Total per orbit line
    orb_totals = []
    for orb_name, orb_def in line_defs.items():
        orb_totals.append(sum(1 for h in range(64) if orb_def['condition'](factored(h)[1])))
    print(f"  {'total':>7s} | " + " | ".join(f"{c:5d}" for c in orb_totals))

    # Show which hexagrams are in PosH ∩ OrbH (the "doubly H" hexagrams)
    print("\n--- DOUBLY-H HEXAGRAMS (Pos-H ∩ Orb-H) ---\n")
    posH_cond = line_defs['H']['condition']
    orbH_cond = line_defs['H']['condition']
    doubly_H = [h for h in range(64)
                if posH_cond(factored(h)[0]) and orbH_cond(factored(h)[1])]
    for h in doubly_H:
        pos, orb = factored(h)
        entry = atlas[str(h)]
        lt = entry['lower_trigram']['name'].split()[0]
        ut = entry['upper_trigram']['name'].split()[0]
        print(f"  {entry['kw_name']:10s} ({fmt6(h)}): "
              f"pos={TRIGRAM_ZH[pos]}({fmt3(pos)}) orb={TRIGRAM_ZH[orb]}({fmt3(orb)}) "
              f"lower={lt} upper={ut} "
              f"basin={entry['basin']}")


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 2: 互 in the Factored Basis
# ═══════════════════════════════════════════════════════════════════════

def computation_2():
    print("\n" + "=" * 70)
    print("COMPUTATION 2: 互 IN THE FACTORED BASIS")
    print("=" * 70)

    labels = ['o', 'm', 'i', 'ō', 'm̄', 'ī']

    def fmt_vec(row):
        terms = [labels[j] for j in range(6) if row[j]]
        return ' ⊕ '.join(terms) if terms else '0'

    # Change of basis: P maps factored → standard
    P = [
        [1, 0, 0, 0, 0, 0],  # L1 = o
        [0, 1, 0, 0, 0, 0],  # L2 = m
        [0, 0, 1, 0, 0, 0],  # L3 = i
        [0, 0, 1, 0, 0, 1],  # L4 = i ⊕ ī
        [0, 1, 0, 0, 1, 0],  # L5 = m ⊕ m̄
        [1, 0, 0, 1, 0, 0],  # L6 = o ⊕ ō
    ]

    # 互 in standard basis
    M_std = [
        [0, 1, 0, 0, 0, 0],  # L1' = L2
        [0, 0, 1, 0, 0, 0],  # L2' = L3
        [0, 0, 0, 1, 0, 0],  # L3' = L4
        [0, 0, 1, 0, 0, 0],  # L4' = L3
        [0, 0, 0, 1, 0, 0],  # L5' = L4
        [0, 0, 0, 0, 1, 0],  # L6' = L5
    ]

    P_inv = mat_inv_f2(P)
    MP = mat_mul_f2(M_std, P)
    M = mat_mul_f2(P_inv, MP)

    print("\n--- 互 MATRIX (factored basis) ---\n")
    for i in range(6):
        print(f"  {labels[i]}' = {fmt_vec(M[i])}")

    # Check decomposition
    print("\n--- DECOMPOSITION ANALYSIS ---\n")
    pos_to_orb = any(M[i][j] for i in range(3) for j in range(3, 6))
    orb_to_pos = any(M[i][j] for i in range(3, 6) for j in range(3))
    print(f"  Position depends on orbit coords: {pos_to_orb}")
    print(f"  Orbit depends on position coords: {orb_to_pos}")

    if pos_to_orb and not orb_to_pos:
        print("\n  互 is a SHEAR: orbit acts on itself independently,")
        print("  but position gets a correction from orbit.")
        print("  Specifically: i' = i ⊕ ī (the i-coordinate gets the orbit ī mixed in)")
        print("  This is the single mixing term: position i-coord ← orbit ī-coord")
        print()
        print("  In product notation: 互 = (pos_shift) × (orb_shift) + shear(ī → i)")
        print("  The orbit factor acts as: ō' = m̄, m̄' = ī, ī' = ī  (shift + project)")
        print("  The position factor acts as: o' = m, m' = i, i' = i  (shift + project)")
        print("  Plus the shear: i gets ī added")

    # Compute powers
    M2 = mat_mul_f2(M, M)
    M3 = mat_mul_f2(M2, M)

    print("\n--- 互² (factored basis) ---\n")
    for i in range(6):
        print(f"  {labels[i]}' = {fmt_vec(M2[i])}")
    print(f"\n  Rank: {rank_f2(M2)}")

    print("\n--- 互³ (factored basis) ---\n")
    for i in range(6):
        print(f"  {labels[i]}' = {fmt_vec(M3[i])}")
    print(f"\n  Rank: {rank_f2(M3)}")

    print(f"\n  Rank sequence: M={rank_f2(M)}, M²={rank_f2(M2)}, "
          f"M³={rank_f2(M3)}")
    print(f"  Nullity sequence: {6 - rank_f2(M)}, {6 - rank_f2(M2)}, "
          f"{6 - rank_f2(M3)}")

    # Kernel chain
    print("\n--- KERNEL CHAIN ---\n")

    def kernel_vectors(mat):
        vecs = []
        for bits in range(1, 64):
            v = [(bits >> j) & 1 for j in range(6)]
            result = [0] * 6
            for i in range(6):
                for j in range(6):
                    result[i] ^= mat[i][j] & v[j]
            if all(x == 0 for x in result):
                vecs.append(v)
        return vecs

    ker1 = kernel_vectors(M)
    ker2 = kernel_vectors(M2)

    print(f"  ker(M): dim = {6 - rank_f2(M)}, basis:")
    # Find basis
    for v in ker1:
        pos_v = (v[0], v[1], v[2])
        orb_v = (v[3], v[4], v[5])
        print(f"    {fmt_vec(v):20s}  pos={pos_v}  orb={orb_v}")

    print(f"\n  ker(M²): dim = {6 - rank_f2(M2)}")
    print(f"  Spanned by coordinates that are killed after 2 applications of 互.")
    # Show which coordinates are in the kernel
    ker2_coords = set()
    for v in ker2:
        for j in range(6):
            if v[j]:
                ker2_coords.add(labels[j])
    print(f"  Coordinates appearing in ker(M²): {ker2_coords}")

    # Interpretation
    print("\n--- INTERPRETATION ---\n")
    print("  ker(M) = span{o, ō}: the 'O-coordinates' in both factors.")
    print("  These are killed first because 互 shifts o→m→i and ō→m̄→ī,")
    print("  so after one step, o information is gone from the o-slot.")
    print()
    print("  ker(M²) = span{o, m, ō, m̄}: all 'outer' coordinates.")
    print("  After two steps, only i and ī survive (the innermost positions).")
    print()
    print("  The stable image (rank 2) lives in the i,ī coordinates.")
    print("  Geometrically: 互 collapses each factor toward the i-axis,")
    print("  and the surviving 2D space is spanned by {i, ī}.")
    print()
    print("  The shear (i' = i ⊕ ī) means that in the stable image,")
    print("  M acts as: i' = i ⊕ ī, ī' = ī (i.e., i oscillates, ī is fixed).")
    print("  This gives the 2-cycle {JiJi, WeiJi} in the attractors.")

    return M


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 3: Attractor Fano Alignment
# ═══════════════════════════════════════════════════════════════════════

def computation_3():
    print("\n" + "=" * 70)
    print("COMPUTATION 3: ATTRACTOR FANO ALIGNMENT")
    print("=" * 70)

    atlas = load_atlas()

    attractors = [
        (63, "Qian 乾"),
        (0,  "Kun 坤"),
        (21, "JiJi 既濟"),
        (42, "WeiJi 未濟"),
    ]

    print("\n--- ATTRACTORS IN FACTORED BASIS ---\n")
    print(f"  {'Name':15s} {'hex':>6s} {'binary':>8s} {'pos':>5s} {'pos_trig':>8s} {'orb':>5s} {'orb_trig':>8s}")
    print(f"  {'─'*60}")

    for hval, name in attractors:
        pos, orb = factored(hval)
        print(f"  {name:15s} {hval:6d} {fmt6(hval):>8s} {fmt3(pos):>5s} "
              f"{TRIGRAM_ZH[pos]:>8s} {fmt3(orb):>5s} {TRIGRAM_ZH[orb]:>8s}")

    print("\n--- FANO LINE MEMBERSHIP ---\n")
    for hval, name in attractors:
        pos, orb = factored(hval)
        pos_lines = fano_line_of(pos)
        orb_lines = fano_line_of(orb)

        pos_str = ", ".join(fano_line_label(m) for m in pos_lines) if pos_lines else "(origin — all subgroups)"
        orb_str = ", ".join(fano_line_label(m) for m in orb_lines) if orb_lines else "(origin — all subgroups)"

        print(f"  {name}:")
        print(f"    Position {TRIGRAM_ZH[pos]}({fmt3(pos)}): {pos_str}")
        print(f"    Orbit    {TRIGRAM_ZH[orb]}({fmt3(orb)}): {orb_str}")
        print()

    # Key observations
    print("--- KEY OBSERVATIONS ---\n")
    print("  1. Qian and Kun both have orbit = 坤(000) = ORIGIN.")
    print("     They are 'palindromic': upper = lower trigram.")
    print("     Their position projections are 乾(111) and 坤(000) — the frame pair.")
    print("     The origin lies in ALL subgroups, so orbit is unconstrained.")
    print()
    print("  2. JiJi and WeiJi both have orbit = 乾(111) = OMI.")
    print("     OMI lies on exactly 3 lines: H, P, Q (all lines through OMI).")
    print("     Their positions are 離(101) and 坎(010) — the Q-line complement pair.")
    print("     坎 and 離 are the Water/Fire singletons — k₁ destination type.")
    print()
    print("  3. The 4 attractors occupy exactly 2 orbit values:")
    print("     - orbit=000 (palindromic): Qian, Kun — the frame pair")
    print("     - orbit=111 (OMI): JiJi, WeiJi — the bridge pair")
    print("     These are {origin, OMI} = the endpoints of the 'complement axis'.")
    print()
    print("  4. The position projections of JiJi/WeiJi lie on line Q = ker(o⊕i).")
    print("     This is the palindromic line! The Q-line's complement pair {坎,離}")
    print("     appears as the position-coordinates of the 2-cycle attractors.")

    # Basin structure
    print("\n--- BASIN STRUCTURE IN FACTORED BASIS ---\n")
    for att_val, att_name in attractors:
        basin_hexs = [h for h in range(64) if atlas[str(h)]['hu_attractor'] == att_val]
        pos_dist = Counter(factored(h)[0] for h in basin_hexs)
        orb_dist = Counter(factored(h)[1] for h in basin_hexs)

        print(f"  Basin of {att_name} ({len(basin_hexs)} hexagrams):")
        pos_str = ", ".join(f"{TRIGRAM_ZH[p]}×{c}" for p, c in sorted(pos_dist.items()))
        orb_str = ", ".join(f"{TRIGRAM_ZH[o]}×{c}" for o, c in sorted(orb_dist.items()))
        print(f"    Position distribution: {pos_str}")
        print(f"    Orbit distribution:    {orb_str}")
        print()


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 4: Bridge Kernels in Product Fano
# ═══════════════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 70)
    print("COMPUTATION 4: BRIDGE KERNELS IN PRODUCT FANO")
    print("=" * 70)

    atlas = load_atlas()

    # Build KW sequence
    kw_to_val = {}
    for key, entry in atlas.items():
        kw_to_val[entry['kw_number']] = entry['hex_val']
    kw_seq = [kw_to_val[i] for i in range(1, 65)]

    # Compute 63 bridges (including wrap-around #64→#1 if desired)
    bridges = []
    for idx in range(63):
        h1 = kw_seq[idx]
        h2 = kw_seq[idx + 1]
        xor = h1 ^ h2
        pos1, orb1 = factored(h1)
        pos2, orb2 = factored(h2)
        delta_pos = pos1 ^ pos2
        delta_orb = orb1 ^ orb2

        bridges.append({
            'idx': idx,
            'kw1': idx + 1, 'kw2': idx + 2,
            'h1': h1, 'h2': h2,
            'xor': xor,
            'delta_pos': delta_pos,
            'delta_orb': delta_orb,
        })

    # Wrap-around bridge
    h1, h2 = kw_seq[63], kw_seq[0]
    wrap_xor = h1 ^ h2
    p1, o1 = factored(h1)
    p2, o2 = factored(h2)
    bridges.append({
        'idx': 63,
        'kw1': 64, 'kw2': 1,
        'h1': h1, 'h2': h2,
        'xor': wrap_xor,
        'delta_pos': p1 ^ p2,
        'delta_orb': o1 ^ o2,
    })

    print(f"\nTotal bridges: {len(bridges)} (63 sequential + 1 wrap-around)")

    # For each bridge, determine Fano line membership
    print("\n--- BRIDGE FANO LINE ANALYSIS ---\n")

    pos_line_counts = Counter()
    orb_line_counts = Counter()
    pos_nonzero = 0
    orb_nonzero = 0

    for b in bridges:
        dp = b['delta_pos']
        do = b['delta_orb']

        if dp != 0:
            pos_nonzero += 1
            for line_mask in fano_line_of(dp):
                pos_line_counts[line_mask] += 1

        if do != 0:
            orb_nonzero += 1
            for line_mask in fano_line_of(do):
                orb_line_counts[line_mask] += 1

    print(f"  Bridges with nonzero position component: {pos_nonzero}/{len(bridges)}")
    print(f"  Bridges with nonzero orbit component:    {orb_nonzero}/{len(bridges)}")
    print(f"  Bridges with delta_pos = 0 (position unchanged): {len(bridges) - pos_nonzero}")
    print(f"  Bridges with delta_orb = 0 (orbit unchanged):    {len(bridges) - orb_nonzero}")

    print("\n  Position component Fano line hits (each nonzero 3-bit vector is on 3 lines):")
    for mask in sorted(FANO_LINES.keys()):
        label = fano_line_label(mask)
        count = pos_line_counts.get(mask, 0)
        pct = 100 * count / pos_nonzero if pos_nonzero > 0 else 0
        print(f"    {label:20s}: {count:3d}/{pos_nonzero} ({pct:5.1f}%)")

    print("\n  Orbit component Fano line hits:")
    for mask in sorted(FANO_LINES.keys()):
        label = fano_line_label(mask)
        count = orb_line_counts.get(mask, 0)
        pct = 100 * count / orb_nonzero if orb_nonzero > 0 else 0
        print(f"    {label:20s}: {count:3d}/{orb_nonzero} ({pct:5.1f}%)")

    # Expected: each nonzero 3-bit vector lies on exactly 3 of 7 lines.
    # If uniform over all 7 nonzero vectors, each line hit = 3/7 ≈ 42.9%.
    # Deviation from this indicates structure.

    # Within-pair vs between-pair analysis
    # KW pairs: (1,2), (3,4), ..., (63,64) — consecutive odd-even pairs
    print("\n--- WITHIN-PAIR vs BETWEEN-PAIR BRIDGES ---\n")

    within_pair = [b for b in bridges if b['kw1'] % 2 == 1 and b['kw2'] == b['kw1'] + 1]
    between_pair = [b for b in bridges if b not in within_pair]

    for category, cat_bridges, cat_name in [
        (within_pair, within_pair, "Within-pair (odd→even)"),
        (between_pair, between_pair, "Between-pair (even→odd)")
    ]:
        n = len(cat_bridges)
        dp_zero = sum(1 for b in cat_bridges if b['delta_pos'] == 0)
        do_zero = sum(1 for b in cat_bridges if b['delta_orb'] == 0)
        dp_nonz = n - dp_zero
        do_nonz = n - do_zero

        print(f"  {cat_name}: {n} bridges")
        print(f"    Δpos = 0: {dp_zero}/{n} ({100*dp_zero/n:.1f}%)")
        print(f"    Δorb = 0: {do_zero}/{n} ({100*do_zero/n:.1f}%)")

        # Fano line stats for this category
        if dp_nonz > 0:
            cat_pos_lines = Counter()
            for b in cat_bridges:
                if b['delta_pos'] != 0:
                    for lm in fano_line_of(b['delta_pos']):
                        cat_pos_lines[lm] += 1
            h_count = cat_pos_lines.get(0b110, 0)
            p_count = cat_pos_lines.get(0b011, 0)
            q_count = cat_pos_lines.get(0b101, 0)
            print(f"    Δpos on line H: {h_count}/{dp_nonz} ({100*h_count/dp_nonz:.1f}%)")
            print(f"    Δpos on line P: {p_count}/{dp_nonz} ({100*p_count/dp_nonz:.1f}%)")
            print(f"    Δpos on line Q: {q_count}/{dp_nonz} ({100*q_count/dp_nonz:.1f}%)")
        print()

    # Upper Canon vs Lower Canon
    print("--- UPPER CANON vs LOWER CANON ---\n")
    upper = [b for b in bridges if b['kw1'] <= 30]  # KW 1-30
    lower = [b for b in bridges if b['kw1'] >= 31 and b['kw1'] <= 64]

    for cat_bridges, cat_name in [(upper, "Upper Canon (KW 1-30)"),
                                   (lower, "Lower Canon (KW 31-64)")]:
        n = len(cat_bridges)
        dp_nonz = sum(1 for b in cat_bridges if b['delta_pos'] != 0)
        do_nonz = sum(1 for b in cat_bridges if b['delta_orb'] != 0)

        print(f"  {cat_name}: {n} bridges")
        for label_name, mask in [("H", 0b110), ("P", 0b011), ("Q", 0b101)]:
            pos_c = sum(1 for b in cat_bridges
                        if b['delta_pos'] != 0 and mask in fano_line_of(b['delta_pos']))
            orb_c = sum(1 for b in cat_bridges
                        if b['delta_orb'] != 0 and mask in fano_line_of(b['delta_orb']))
            print(f"    Line {label_name}: pos={pos_c}/{dp_nonz}, orb={orb_c}/{do_nonz}")
        print()

    # Kernel dressing analysis
    print("--- KERNEL DRESSING IN FACTORED BASIS ---\n")
    print("  The 'kernel dressing' from synthesis-0 is the palindromic part of")
    print("  the bridge mask: lines that are symmetric (L_k and L_{7-k} both flip).")
    print()
    print("  In the factored basis:")
    print("  - A bridge that changes only orbit (Δpos=0, Δorb≠0) is a PURE")
    print("    palindromic change: it modifies the L_k⊕L_{7-k} signature")
    print("    without changing the lower trigram.")
    print("  - A bridge that changes only position (Δpos≠0, Δorb=0) preserves")
    print("    the palindromic signature but shifts within the orbit.")
    print()

    both_zero = sum(1 for b in bridges if b['delta_pos'] == 0 and b['delta_orb'] == 0)
    pos_only = sum(1 for b in bridges if b['delta_pos'] != 0 and b['delta_orb'] == 0)
    orb_only = sum(1 for b in bridges if b['delta_pos'] == 0 and b['delta_orb'] != 0)
    both_nonz = sum(1 for b in bridges if b['delta_pos'] != 0 and b['delta_orb'] != 0)

    print(f"  Bridge decomposition:")
    print(f"    Both zero (identity):        {both_zero}")
    print(f"    Position-only (Δorb=0):      {pos_only}")
    print(f"    Orbit-only (Δpos=0):         {orb_only}")
    print(f"    Mixed (both nonzero):        {both_nonz}")
    print(f"    Total:                       {len(bridges)}")

    # What are the position-only bridges?
    if pos_only > 0:
        print(f"\n  Position-only bridges (orbit preserved):")
        for b in bridges:
            if b['delta_pos'] != 0 and b['delta_orb'] == 0:
                dp = b['delta_pos']
                lines = ", ".join(fano_line_label(m) for m in fano_line_of(dp))
                e1 = atlas[str(b['h1'])]
                e2 = atlas[str(b['h2'])]
                print(f"    KW {b['kw1']:2d}→{b['kw2']:2d}: "
                      f"Δpos={TRIGRAM_ZH[dp]}({fmt3(dp)}) on {lines}")

    # Delta_pos and delta_orb distribution
    print("\n  Position delta distribution:")
    dp_dist = Counter(b['delta_pos'] for b in bridges)
    for v, c in sorted(dp_dist.items()):
        if v == 0:
            print(f"    {TRIGRAM_ZH[v]}({fmt3(v)}) [origin]:   {c}")
        else:
            lines = ", ".join(fano_line_label(m) for m in fano_line_of(v))
            print(f"    {TRIGRAM_ZH[v]}({fmt3(v)}) [{lines}]: {c}")

    print("\n  Orbit delta distribution:")
    do_dist = Counter(b['delta_orb'] for b in bridges)
    for v, c in sorted(do_dist.items()):
        if v == 0:
            print(f"    {TRIGRAM_ZH[v]}({fmt3(v)}) [origin]:   {c}")
        else:
            lines = ", ".join(fano_line_label(m) for m in fano_line_of(v))
            print(f"    {TRIGRAM_ZH[v]}({fmt3(v)}) [{lines}]: {c}")

    return bridges


# ═══════════════════════════════════════════════════════════════════════
# MARKDOWN OUTPUT
# ═══════════════════════════════════════════════════════════════════════

def write_findings(M_fac, bridges):
    atlas = load_atlas()
    L = []
    w = L.append

    w("# Hexagram Lift: PG(2,2) × PG(2,2) Findings\n")

    labels = ['o', 'm', 'i', 'ō', 'm̄', 'ī']
    def fmt_vec(row):
        terms = [labels[j] for j in range(6) if row[j]]
        return ' ⊕ '.join(terms) if terms else '0'

    # ── Computation 1 ──
    w("## 1. Product Fano Analysis\n")
    w("Each hexagram decomposes as (position, orbit) ∈ F₂³ × F₂³:")
    w("- Position = lower trigram (o, m, i) = (L1, L2, L3)")
    w("- Orbit = palindromic signature (ō, m̄, ī) = (L1⊕L6, L2⊕L5, L3⊕L4)\n")

    w("### Line Conditions\n")
    w("In each factor, the three distinguished lines impose conditions:\n")
    w("| Line | Position condition | Orbit condition |")
    w("|---|---|---|")
    w("| H = ker(b₁⊕b₂) | L2 = L3 | L2⊕L5 = L3⊕L4 |")
    w("| P = ker(b₀⊕b₁) | L1 = L2 | L1⊕L6 = L2⊕L5 |")
    w("| Q = ker(b₀⊕b₂) | L1 = L3 | L1⊕L6 = L3⊕L4 |")
    w("")

    w("### Key Finding: Only Line H Refines Blocks\n")
    w("From Computation 3 of iteration 1: the spaceprobe block system is refined")
    w("ONLY by line H's coset partition. In the product structure, this means")
    w("the block system lives on the H-axis of each factor.\n")

    # ── Computation 2 ──
    w("## 2. 互 in the Factored Basis\n")
    w("### The Matrix\n")
    w("```")
    for i in range(6):
        w(f"  {labels[i]}' = {fmt_vec(M_fac[i])}")
    w("```\n")

    M2 = mat_mul_f2(M_fac, M_fac)
    w("### Decomposition\n")
    w("互 is NOT a product map. It is a **shear**:\n")
    w("- **Orbit factor** (independent): ō' = m̄, m̄' = ī, ī' = ī")
    w("  → shifts ō→m̄→ī then projects onto ī")
    w("- **Position factor** (almost independent): o' = m, m' = i")
    w("  → shifts o→m→i")
    w("- **Shear term**: i' = i ⊕ **ī** (position i gets orbit ī mixed in)")
    w("")
    w("The shear is a single term: the orbit's ī-coordinate leaks into position.")
    w("This is the algebraic source of the JiJi/WeiJi 2-cycle:\n")
    w("- In the stable image (after 2+ applications), only i and ī survive")
    w("- The action on {i, ī} is: i ↦ i ⊕ ī, ī ↦ ī")
    w("- If ī = 0 (palindromic): i ↦ i → fixed point (Qian or Kun)")
    w("- If ī = 1 (anti-palindromic): i ↦ i ⊕ 1 → 2-cycle\n")

    w("### Rank Sequence\n")
    M3 = mat_mul_f2(M2, M_fac)
    w(f"| Power | Rank | Nullity | Killed coordinates |")
    w(f"|---|---|---|---|")
    w(f"| M | {rank_f2(M_fac)} | {6 - rank_f2(M_fac)} | o, ō |")
    w(f"| M² | {rank_f2(M2)} | {6 - rank_f2(M2)} | o, m, ō, m̄ |")
    w(f"| M³ | {rank_f2(M3)} | {6 - rank_f2(M3)} | (stable) |")
    w("")
    w("The kernel chain kills coordinates symmetrically across factors:")
    w("first the outermost (o, ō), then the middle (m, m̄).")
    w("The surviving coordinates {i, ī} are the innermost positions in both factors.\n")

    # ── Computation 3 ──
    w("## 3. Attractor Fano Alignment\n")
    w("| Attractor | hex | Position | Orbit | Pos lines | Orb lines |")
    w("|---|---|---|---|---|---|")
    for hval, name in [(63, "Qian 乾"), (0, "Kun 坤"), (21, "JiJi 既濟"), (42, "WeiJi 未濟")]:
        pos, orb = factored(hval)
        pl = fano_line_of(pos)
        ol = fano_line_of(orb)
        pstr = ", ".join(fano_line_label(m) for m in pl) if pl else "origin"
        ostr = ", ".join(fano_line_label(m) for m in ol) if ol else "origin"
        w(f"| {name} | {fmt6(hval)} | {TRIGRAM_ZH[pos]}({fmt3(pos)}) | "
          f"{TRIGRAM_ZH[orb]}({fmt3(orb)}) | {pstr} | {ostr} |")
    w("")

    w("### Structural Pattern\n")
    w("The 4 attractors split into two complementary pairs:\n")
    w("1. **Frame pair** {Qian, Kun}: orbit = 000 (origin = palindromic)")
    w("   - Position projections = {乾, 坤} = the frame pair itself")
    w("   - These are the FIXED POINTS of 互 (ī = 0 → no oscillation)\n")
    w("2. **Bridge pair** {JiJi, WeiJi}: orbit = 111 (OMI = anti-palindromic)")
    w("   - Position projections = {離, 坎} = the Q-line complement pair")
    w("   - These form the 2-CYCLE of 互 (ī = 1 → i oscillates)")
    w("   - 坎 and 離 are the Water/Fire singletons (k₁ destination type)\n")
    w("The orbit projection {000, 111} = {origin, OMI} is the complement axis —")
    w("the unique pair that lies in ALL subgroups (origin) or ALL OMI-lines (OMI).\n")

    # ── Computation 4 ──
    w("## 4. Bridge Kernels in Product Fano\n")

    dp_zero = sum(1 for b in bridges if b['delta_pos'] == 0)
    do_zero = sum(1 for b in bridges if b['delta_orb'] == 0)
    pos_only = sum(1 for b in bridges if b['delta_pos'] != 0 and b['delta_orb'] == 0)
    orb_only = sum(1 for b in bridges if b['delta_pos'] == 0 and b['delta_orb'] != 0)
    both_nonz = sum(1 for b in bridges if b['delta_pos'] != 0 and b['delta_orb'] != 0)

    w("### Bridge Decomposition\n")
    w(f"| Category | Count |")
    w(f"|---|---|")
    w(f"| Position-only (Δorb = 0) | {pos_only} |")
    w(f"| Orbit-only (Δpos = 0) | {orb_only} |")
    w(f"| Mixed (both nonzero) | {both_nonz} |")
    w(f"| Total | {len(bridges)} |")
    w("")

    w("### Fano Line Statistics\n")
    pos_nonzero = sum(1 for b in bridges if b['delta_pos'] != 0)
    orb_nonzero = sum(1 for b in bridges if b['delta_orb'] != 0)

    pos_line_counts = Counter()
    orb_line_counts = Counter()
    for b in bridges:
        if b['delta_pos'] != 0:
            for m in fano_line_of(b['delta_pos']):
                pos_line_counts[m] += 1
        if b['delta_orb'] != 0:
            for m in fano_line_of(b['delta_orb']):
                orb_line_counts[m] += 1

    w("| Line | Pos hits | Pos % | Orb hits | Orb % | Expected % |")
    w("|---|---|---|---|---|---|")
    for mask in [0b110, 0b011, 0b101, 0b001, 0b010, 0b100, 0b111]:
        label = fano_line_label(mask)
        pc = pos_line_counts.get(mask, 0)
        oc = orb_line_counts.get(mask, 0)
        pp = 100 * pc / pos_nonzero if pos_nonzero else 0
        op = 100 * oc / orb_nonzero if orb_nonzero else 0
        w(f"| {label} | {pc} | {pp:.1f}% | {oc} | {op:.1f}% | 42.9% |")
    w("")
    w("Expected % = 3/7 ≈ 42.9% (each nonzero vector lies on 3 of 7 lines).\n")

    # Within-pair vs between-pair
    within_pair = [b for b in bridges if b['kw1'] % 2 == 1 and b['kw2'] == b['kw1'] + 1]
    between_pair = [b for b in bridges if b not in within_pair]

    w("### Within-Pair vs Between-Pair\n")
    w("KW pairs: (1,2), (3,4), ..., (63,64)")
    w("")
    w("**Key finding: All 32 within-pair bridges have Δorb = 0.**")
    w("This is a theorem, not a coincidence: KW pairs are either")
    w("reversals or complements, and both operations preserve orbit:")
    w("- Reversal swaps (L1,L2,L3) ↔ (L6,L5,L4) → symmetric XOR unchanged")
    w("- Complement flips all lines → L_k⊕L_{7-k} unchanged")
    w("")
    w("Therefore **KW pairing = orbit class**. Within-pair transitions")
    w("change only position (lower trigram), never the palindromic signature.\n")
    w("| Metric | Within-pair | Between-pair |")
    w("|---|---|---|")
    wp_dp0 = sum(1 for b in within_pair if b['delta_pos'] == 0)
    wp_do0 = sum(1 for b in within_pair if b['delta_orb'] == 0)
    bp_dp0 = sum(1 for b in between_pair if b['delta_pos'] == 0)
    bp_do0 = sum(1 for b in between_pair if b['delta_orb'] == 0)
    w(f"| Count | {len(within_pair)} | {len(between_pair)} |")
    w(f"| Δpos = 0 | {wp_dp0} ({100*wp_dp0/max(1,len(within_pair)):.0f}%) | "
      f"{bp_dp0} ({100*bp_dp0/max(1,len(between_pair)):.0f}%) |")
    w(f"| Δorb = 0 | {wp_do0} ({100*wp_do0/max(1,len(within_pair)):.0f}%) | "
      f"{bp_do0} ({100*bp_do0/max(1,len(between_pair)):.0f}%) |")
    w("")

    # ── Synthesis ──
    w("## Synthesis\n")
    w("### The Shear Structure of 互\n")
    w("The factored basis reveals 互 as a shear map on F₂³ × F₂³:")
    w("it acts independently on orbit but couples orbit→position via a single")
    w("term (ī leaks into i). This is the minimal departure from a product map.\n")
    w("The rank sequence 6→4→2→2 kills coordinates symmetrically: first the")
    w("outer O-coordinates (o,ō), then the middle M-coordinates (m,m̄), leaving")
    w("only the inner I-coordinates (i,ī). The stable image is 2-dimensional,")
    w("spanned by {i, ī}, and the dynamics on this 2D space is:\n")
    w("```")
    w("i ↦ i ⊕ ī")
    w("ī ↦ ī")
    w("```\n")
    w("This gives exactly the observed attractor structure:")
    w("- ī = 0 → i is fixed → {Qian, Kun} (position i=1,0)")
    w("- ī = 1 → i oscillates → {JiJi, WeiJi} 2-cycle\n")
    w("### Fano Alignment of Attractors\n")
    w("The attractors occupy a remarkably constrained locus in PG(2,2) × PG(2,2):")
    w("- Orbit: only {000, 111} = {origin, OMI} — the complement axis endpoints")
    w("- Position of 2-cycle: {坎, 離} = the Q-line pair = Water/Fire singletons")
    w("- Position of fixed points: {坤, 乾} = the frame pair = Earth/Metal doublets\n")
    w("The Q-line (palindromic condition ker(o⊕i)) governs which hexagrams")
    w("oscillate under 互: those with position on line Q and orbit = OMI.\n")
    w("### KW Pairing = Orbit Class\n")
    w("All 32 within-pair bridges have Δorb = 0 (100%). This is a theorem:")
    w("reversal and complement both preserve orbit (palindromic signature),")
    w("and every KW pair is related by one of these operations.")
    w("Within-pair transitions change only position; between-pair transitions")
    w("typically change both.\n")
    w("Line H is enriched in position bridges (52.5% vs 42.9% expected),")
    w("and H + P together dominate orbit bridges (53.3% each).")
    w("This suggests the KW sequence navigates preferentially along")
    w("Fano-line-aligned axes in the product geometry.\n")

    return '\n'.join(L)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    outdir = Path(__file__).parent

    computation_1()
    M_fac = computation_2()
    computation_3()
    bridges = computation_4()

    md = write_findings(M_fac, bridges)
    findings_path = outdir / "hexagram_lift_findings.md"
    findings_path.write_text(md)
    print(f"\n{'=' * 70}")
    print(f"Findings written to {findings_path}")


if __name__ == '__main__':
    main()
