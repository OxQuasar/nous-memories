"""
Quartet-level analysis of the King Wen sequence.
Groups of 2 consecutive pairs (4 hexagrams). 16 quartets total.
"""

import numpy as np
from collections import Counter, defaultdict
from itertools import combinations
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
N_PAIRS = 32
N_QUARTETS = 16
N_TRIALS = 10000
RNG = np.random.default_rng(42)

M = np.array(all_bits())

MASKS = {
    (1,1,1,1,1,1): "OMI",
    (1,1,0,0,1,1): "OM",
    (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI",
    (0,1,0,0,1,0): "M",
    (0,0,1,1,0,0): "I",
    (1,0,0,0,0,1): "O",
}

GEN_BITS = {'O': 1, 'M': 2, 'I': 4, 'OM': 3, 'OI': 5, 'MI': 6, 'OMI': 7}


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# Build pair and quartet structures
pairs = []
for k in range(N_PAIRS):
    a = M[2 * k]
    b = M[2 * k + 1]
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    pairs.append({
        'idx': k, 'a': tuple(a), 'b': tuple(b),
        'mask': xor, 'name': MASKS[xor],
        'gen_bits': GEN_BITS[MASKS[xor]],
    })

quartets = []
for q in range(N_QUARTETS):
    p1 = pairs[2 * q]
    p2 = pairs[2 * q + 1]
    hexes = [p1['a'], p1['b'], p2['a'], p2['b']]
    hex_indices = [2 * p1['idx'], 2 * p1['idx'] + 1,
                   2 * p2['idx'], 2 * p2['idx'] + 1]
    quartets.append({
        'idx': q,
        'p1': p1, 'p2': p2,
        'hexes': hexes,
        'hex_indices': hex_indices,
        'gen_pair': (p1['name'], p2['name']),
        'gen_xor': p1['gen_bits'] ^ p2['gen_bits'],
    })


# ─── 1. Quartet Composition ──────────────────────────────────────────────────

def composition():
    print("=" * 70)
    print("1. QUARTET COMPOSITION")
    print("=" * 70)

    print(f"\n  {'Q':>2s}  {'Pair1':>4s} {'Pair2':>4s}  {'Gen1':>4s} {'Gen2':>4s}  "
          f"{'ΔGEN':>4s}  Hexagrams")
    for q in quartets:
        names = [KING_WEN[i][1] for i in q['hex_indices']]
        xor = q['gen_xor']
        delta = []
        if xor & 1: delta.append('O')
        if xor & 2: delta.append('M')
        if xor & 4: delta.append('I')
        delta_str = ','.join(delta) if delta else '='
        print(f"  {q['idx']+1:2d}  {q['p1']['idx']+1:4d} {q['p2']['idx']+1:4d}  "
              f"{q['p1']['name']:>4s} {q['p2']['name']:>4s}  "
              f"{delta_str:>4s}  {', '.join(names)}")

    # Generator pair frequency
    gen_pairs = Counter(q['gen_pair'] for q in quartets)
    print(f"\n  Generator pair types:")
    for gp, count in gen_pairs.most_common():
        print(f"    {gp[0]:>4s} → {gp[1]:<4s}: {count}x")

    # Generator XOR distribution
    xor_dist = Counter(q['gen_xor'] for q in quartets)
    print(f"\n  Generator change within quartet:")
    for xor, count in sorted(xor_dist.items()):
        delta = []
        if xor & 1: delta.append('O')
        if xor & 2: delta.append('M')
        if xor & 4: delta.append('I')
        print(f"    Δ={','.join(delta) if delta else '(none)'}: {count}x")


# ─── 2. Quartet Geometry ─────────────────────────────────────────────────────

def geometry():
    print("\n" + "=" * 70)
    print("2. QUARTET GEOMETRY (4 vertices in the hypercube)")
    print("=" * 70)

    for q in quartets:
        verts = q['hexes']
        # Pairwise Hamming distances
        dists = {}
        labels = ['A1', 'B1', 'A2', 'B2']
        for i in range(4):
            for j in range(i + 1, 4):
                d = hamming(verts[i], verts[j])
                dists[(labels[i], labels[j])] = d

        # What shape? Check if it's a face (all 4 on a 2D face)
        # or a tetrahedron, or a path
        dist_vals = sorted(dists.values())

        # Center of the 4 vertices
        center = np.mean([np.array(v) for v in verts], axis=0)

        # Span: how many dimensions do the 4 vertices cover?
        v_array = np.array(verts)
        per_dim_unique = [len(set(v_array[:, d])) for d in range(DIMS)]
        span = sum(1 for u in per_dim_unique if u > 1)

        names = [KING_WEN[i][1] for i in q['hex_indices']]
        print(f"\n  Q{q['idx']+1}: {q['p1']['name']}→{q['p2']['name']}  "
              f"({', '.join(names)})")
        print(f"    Distances: A1-B1={dists[('A1','B1')]}, "
              f"B1-A2={dists[('B1','A2')]}, A2-B2={dists[('A2','B2')]}")
        print(f"    Diagonals: A1-A2={dists[('A1','A2')]}, "
              f"A1-B2={dists[('A1','B2')]}, B1-B2={dists[('B1','B2')]}")
        print(f"    Span: {span} dimensions vary")
        print(f"    Sorted distances: {dist_vals}")

        # Is it a parallelogram? (opposite sides equal)
        is_para = (dists[('A1','B1')] == dists[('A2','B2')] and
                   dists[('A1','A2')] == dists[('B1','B2')])
        if is_para:
            print(f"    Shape: parallelogram (A1B1={dists[('A1','B1')]}, "
                  f"A1A2={dists[('A1','A2')]})")

    # Summary statistics
    print(f"\n  Shape summary:")
    spans = [sum(1 for d in range(DIMS)
                 if len(set(np.array(q['hexes'])[:, d])) > 1)
             for q in quartets]
    print(f"    Span distribution: {Counter(spans)}")

    # Are any quartets contained in a face (2D subcube)?
    face_count = 0
    for q in quartets:
        v = np.array(q['hexes'])
        varying = [d for d in range(DIMS) if len(set(v[:, d])) > 1]
        if len(varying) <= 2 and len(set(map(tuple, v))) == 4:
            face_count += 1
    print(f"    Quartets contained in a 2D face: {face_count}/16")


# ─── 3. Quartet Masks ────────────────────────────────────────────────────────

def quartet_masks():
    print("\n" + "=" * 70)
    print("3. QUARTET MASKS (combined change across both pairs)")
    print("=" * 70)

    # The "quartet mask" = union of the two pair masks
    # Which lines change across the entire quartet?
    for q in quartets:
        m1 = q['p1']['mask']
        m2 = q['p2']['mask']
        union = tuple(max(m1[i], m2[i]) for i in range(DIMS))
        intersection = tuple(min(m1[i], m2[i]) for i in range(DIMS))
        only1 = tuple(m1[i] and not m2[i] for i in range(DIMS))
        only2 = tuple(m2[i] and not m1[i] for i in range(DIMS))

        union_str = ''.join(map(str, union))
        inter_str = ''.join(map(str, intersection))

        q['union_mask'] = union
        q['inter_mask'] = intersection

    # Quartet union mask distribution
    union_counts = Counter(q['union_mask'] for q in quartets)
    print(f"\n  Quartet union masks (lines that change in either pair):")
    for mask, count in union_counts.most_common():
        mask_str = ''.join(map(str, mask))
        n = sum(mask)
        which = [q['idx'] + 1 for q in quartets if q['union_mask'] == mask]
        print(f"    {mask_str} ({n} lines): {count}x — Q{which}")

    # Intersection mask distribution
    inter_counts = Counter(q['inter_mask'] for q in quartets)
    print(f"\n  Quartet intersection masks (lines that change in both pairs):")
    for mask, count in inter_counts.most_common():
        mask_str = ''.join(map(str, mask))
        n = sum(mask)
        which = [q['idx'] + 1 for q in quartets if q['inter_mask'] == mask]
        print(f"    {mask_str} ({n} lines): {count}x — Q{which}")

    # How much overlap between the two pair masks?
    print(f"\n  Mask overlap (Jaccard) per quartet:")
    for q in quartets:
        m1 = q['p1']['mask']
        m2 = q['p2']['mask']
        inter = sum(min(m1[i], m2[i]) for i in range(DIMS))
        union = sum(max(m1[i], m2[i]) for i in range(DIMS))
        jaccard = inter / union if union > 0 else 0
        print(f"    Q{q['idx']+1:2d} ({q['p1']['name']:>3s}→{q['p2']['name']:<3s}): "
              f"overlap={inter}/{union} (J={jaccard:.2f})")


# ─── 4. Quartet-Level Tiling ─────────────────────────────────────────────────

def tiling():
    print("\n" + "=" * 70)
    print("4. QUARTET-LEVEL HYPERCUBE TILING")
    print("=" * 70)

    # Each quartet has 4 vertices. How do quartets partition the 64 vertices?
    # Do quartets tile into recognizable subcube structures?

    print(f"\n  Quartet vertex uniqueness:")
    all_verts = set()
    for q in quartets:
        for v in q['hexes']:
            all_verts.add(v)
    print(f"    Total unique vertices across all quartets: {len(all_verts)}/64")

    # Per-dimension balance within each quartet
    print(f"\n  Per-quartet dimensional balance (yang fraction):")
    for q in quartets:
        v = np.array(q['hexes'])
        balance = v.mean(axis=0)
        balanced_dims = sum(1 for b in balance if b == 0.5)
        print(f"    Q{q['idx']+1:2d}: [{', '.join(f'{b:.2f}' for b in balance)}]  "
              f"({balanced_dims}/6 balanced)")

    # Quartet center distances
    centers = [np.mean(np.array(q['hexes']), axis=0) for q in quartets]

    # Sequential center distances
    seq_dists = [np.linalg.norm(centers[k+1] - centers[k])
                 for k in range(N_QUARTETS - 1)]
    all_dists = [np.linalg.norm(centers[i] - centers[j])
                 for i in range(N_QUARTETS)
                 for j in range(i+1, N_QUARTETS)]
    print(f"\n  Quartet center distances:")
    print(f"    Sequential mean: {np.mean(seq_dists):.3f}")
    print(f"    All-pairs mean:  {np.mean(all_dists):.3f}")

    # Nearest neighbor quartets
    print(f"\n  Nearest neighbor quartets (by center distance):")
    for i in range(N_QUARTETS):
        min_d = float('inf')
        nn = -1
        for j in range(N_QUARTETS):
            if i == j:
                continue
            d = np.linalg.norm(centers[i] - centers[j])
            if d < min_d:
                min_d = d
                nn = j
        print(f"    Q{i+1:2d} → Q{nn+1:2d} (dist={min_d:.3f})")


# ─── 5. Quartet Offset Structure ─────────────────────────────────────────────

def offset_structure():
    print("\n" + "=" * 70)
    print("5. QUARTET-LEVEL OFFSET STRUCTURE")
    print("=" * 70)

    centers = [np.mean(np.array(q['hexes']), axis=0) for q in quartets]
    gen_pairs = [q['gen_pair'] for q in quartets]

    # Center distance by quartet offset
    print(f"\n  Mean center distance by quartet offset:")
    offset_dists = []
    for d in range(1, N_QUARTETS):
        dists = [np.linalg.norm(centers[k] - centers[(k + d) % N_QUARTETS])
                 for k in range(N_QUARTETS)]
        offset_dists.append((d, np.mean(dists)))
    offset_dists.sort(key=lambda x: x[1])
    for d, mean_d in offset_dists[:8]:
        print(f"    offset {d:2d}: {mean_d:.3f}")

    # Generator pair match by offset
    print(f"\n  Generator pair matches by quartet offset:")
    for d in range(1, N_QUARTETS):
        matches = sum(1 for k in range(N_QUARTETS)
                      if gen_pairs[k] == gen_pairs[(k + d) % N_QUARTETS])
        if matches > 1:
            print(f"    offset {d:2d}: {matches}/16 matches")

    # At offset 8 (half the quartets = pairs 1-16 vs 17-32)
    print(f"\n  Quartet mirror (Q_k vs Q_{N_QUARTETS+1}-k):")
    for k in range(N_QUARTETS // 2):
        mirror = N_QUARTETS - 1 - k
        gp1 = quartets[k]['gen_pair']
        gp2 = quartets[mirror]['gen_pair']
        same = gp1 == gp2
        rev = gp1 == (gp2[1], gp2[0])
        print(f"    Q{k+1:2d} ({gp1[0]:>3s},{gp1[1]:<3s}) vs "
              f"Q{mirror+1:2d} ({gp2[0]:>3s},{gp2[1]:<3s})  "
              f"{'SAME' if same else 'REVERSE' if rev else '—'}")


# ─── 6. Quartet as State Transitions ─────────────────────────────────────────

def state_transitions():
    print("\n" + "=" * 70)
    print("6. QUARTETS AS STATE TRANSITIONS")
    print("=" * 70)

    # Each quartet starts at hex A1 and ends at hex B2
    # The "net change" across the quartet
    print(f"\n  Net change across each quartet (A1 → B2):")
    print(f"  {'Q':>2s}  {'A1':>7s} {'B2':>7s}  {'XOR':>7s}  {'Ham':>3s}  "
          f"{'Net weight':>10s}")

    net_hammings = []
    for q in quartets:
        a1 = q['hexes'][0]
        b2 = q['hexes'][3]
        xor = tuple(a ^ b for a, b in zip(a1, b2))
        h = sum(xor)
        w1 = sum(a1)
        w2 = sum(b2)
        net_hammings.append(h)
        xor_str = ''.join(map(str, xor))
        a1_str = ''.join(map(str, a1))
        b2_str = ''.join(map(str, b2))
        print(f"  {q['idx']+1:2d}  {a1_str} {b2_str}  {xor_str}  {h:3d}  "
              f"{w1}→{w2} (Δ={w2-w1:+d})")

    print(f"\n  Net Hamming distribution: {Counter(net_hammings)}")
    print(f"  Mean net Hamming: {np.mean(net_hammings):.2f}")

    # Weight trajectory through quartets
    print(f"\n  Weight trajectory (yang count at each position):")
    print(f"  {'Q':>2s}  A1 B1 A2 B2  Path")
    for q in quartets:
        weights = [sum(h) for h in q['hexes']]
        path = '→'.join(map(str, weights))
        print(f"  {q['idx']+1:2d}  {weights[0]:2d} {weights[1]:2d} "
              f"{weights[2]:2d} {weights[3]:2d}  {path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("QUARTET-LEVEL ANALYSIS OF THE KING WEN SEQUENCE")
    print("=" * 70)

    composition()
    geometry()
    quartet_masks()
    tiling()
    offset_structure()
    state_transitions()

    print("\n" + "=" * 70)
    print("QUARTET ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
