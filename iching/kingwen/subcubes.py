"""
Detailed subcube occupation analysis of King Wen mask groups.
"""

import numpy as np
from collections import Counter, defaultdict
from itertools import product
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
M = np.array(all_bits())

MASK_NAMES = {
    (1,1,1,1,1,1): "OMI",
    (1,1,0,0,1,1): "OM",
    (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI",
    (0,1,0,0,1,0): "M",
    (0,0,1,1,0,0): "I",
    (1,0,0,0,0,1): "O",
}

# Build pairs with masks
pairs = []
for k in range(32):
    a = M[2 * k]
    b = M[2 * k + 1]
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    pairs.append({
        'idx': k,
        'a': tuple(a), 'b': tuple(b),
        'xor': xor,
        'name': MASK_NAMES[xor],
    })

# Group by mask
groups = defaultdict(list)
for p in pairs:
    groups[p['xor']].append(p)


def subcube_key(vertex, fixed_dims):
    """The fixed-dimension values that identify which subcube a vertex is in."""
    return tuple(vertex[d] for d in fixed_dims)


def project(vertex, flip_dims):
    """Project vertex to flip dimensions only."""
    return tuple(vertex[d] for d in flip_dims)


# ─── 1. Full Subcube Map ─────────────────────────────────────────────────────

def full_subcube_map():
    print("=" * 70)
    print("1. SUBCUBE OCCUPATION MAP")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mname = MASK_NAMES[mask]
        mask_str = ''.join(map(str, mask))
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]
        flip_dims = [i for i in range(DIMS) if mask[i] == 1]
        n_flips = sum(mask)

        print(f"\n  {mname} (mask {mask_str})")
        print(f"  Flip dims: {', '.join(f'L{d+1}' for d in flip_dims)}")
        if fixed_dims:
            print(f"  Fixed dims: {', '.join(f'L{d+1}' for d in fixed_dims)}")

        # Collect all vertices by subcube
        subcube_vertices = defaultdict(set)
        for p in g:
            key = subcube_key(p['a'], fixed_dims) if fixed_dims else ()
            subcube_vertices[key].add(project(p['a'], flip_dims))
            subcube_vertices[key].add(project(p['b'], flip_dims))

        n_vertices_per_subcube = 2 ** n_flips
        for key in sorted(subcube_vertices.keys()):
            verts = sorted(subcube_vertices[key])
            if fixed_dims:
                fixed_str = ''.join(map(str, key))
                print(f"\n    Subcube [{fixed_str}]: "
                      f"{len(verts)}/{n_vertices_per_subcube} vertices")
            else:
                print(f"\n    Full cube: {len(verts)}/{n_vertices_per_subcube} vertices")

            # Show which vertices are present and which are missing
            all_possible = list(product([0, 1], repeat=n_flips))
            present = set(verts)
            missing = [v for v in all_possible if v not in present]

            for v in all_possible:
                marker = "█" if v in present else "·"
                v_str = ''.join(map(str, v))
                # Reconstruct full hexagram
                full = [0] * DIMS
                fi = 0
                fxi = 0
                for d in range(DIMS):
                    if mask[d] == 1:
                        full[d] = v[fi]
                        fi += 1
                    else:
                        full[d] = key[fxi] if fixed_dims else 0
                        fxi += 1
                hex_str = ''.join(map(str, full))
                # Find if this hexagram exists in our pairs
                hex_tuple = tuple(full)
                found = None
                for p in g:
                    if p['a'] == hex_tuple:
                        found = f"#{KING_WEN[p['idx']*2][0]} {KING_WEN[p['idx']*2][1]}"
                    elif p['b'] == hex_tuple:
                        found = f"#{KING_WEN[p['idx']*2+1][0]} {KING_WEN[p['idx']*2+1][1]}"
                print(f"      {marker} {v_str}  ({hex_str})  {found or ''}")


# ─── 2. Pair Geometry Within Subcubes ─────────────────────────────────────────

def pair_geometry():
    print("\n" + "=" * 70)
    print("2. PAIR GEOMETRY WITHIN SUBCUBES")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        g = groups[mask]
        mname = MASK_NAMES[mask]
        flip_dims = [i for i in range(DIMS) if mask[i] == 1]
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]
        n_flips = sum(mask)

        print(f"\n  {mname}:")

        for p in g:
            proj_a = project(p['a'], flip_dims)
            proj_b = project(p['b'], flip_dims)
            # Within the subcube, what's the relationship?
            xor_proj = tuple(a ^ b for a, b in zip(proj_a, proj_b))
            hamming = sum(xor_proj)
            # Is it a diagonal (all flip) or edge (1 flip) or face diagonal etc?
            a_str = ''.join(map(str, proj_a))
            b_str = ''.join(map(str, proj_b))
            xor_str = ''.join(map(str, xor_proj))
            key = subcube_key(p['a'], fixed_dims) if fixed_dims else ()
            key_str = ''.join(map(str, key)) if key else '-'
            print(f"    Pair {p['idx']+1:2d} [{key_str}]: "
                  f"{a_str} ↔ {b_str}  (XOR={xor_str}, "
                  f"{'main diagonal' if hamming == n_flips else f'{hamming}-flip'})")


# ─── 3. Coverage Analysis ────────────────────────────────────────────────────

def coverage_analysis():
    print("\n" + "=" * 70)
    print("3. HYPERCUBE COVERAGE — HOW GROUPS TILE THE SPACE")
    print("=" * 70)

    # Every hexagram belongs to exactly one pair, hence one mask group
    # Map each vertex to its group
    vertex_to_group = {}
    for p in pairs:
        vertex_to_group[p['a']] = p['name']
        vertex_to_group[p['b']] = p['name']

    print(f"\n  Vertices per group:")
    group_counts = Counter(vertex_to_group.values())
    for name in ['OMI', 'OM', 'OI', 'MI', 'O', 'M', 'I']:
        print(f"    {name:3s}: {group_counts[name]:2d}/64")
    print(f"    Total: {sum(group_counts.values())}/64")

    # For each dimension, what fraction of vertices in each half-space
    # belong to each group?
    print(f"\n  Group distribution by half-space:")
    for d in range(DIMS):
        print(f"\n    L{d+1}=0 (yin):", end="")
        yin_groups = Counter()
        yang_groups = Counter()
        for v, g in vertex_to_group.items():
            if v[d] == 0:
                yin_groups[g] += 1
            else:
                yang_groups[g] += 1
        for name in ['OMI', 'OM', 'OI', 'MI', 'O', 'M', 'I']:
            print(f"  {name}={yin_groups.get(name,0):d}", end="")
        print(f"\n    L{d+1}=1 (yang):", end="")
        for name in ['OMI', 'OM', 'OI', 'MI', 'O', 'M', 'I']:
            print(f"  {name}={yang_groups.get(name,0):d}", end="")
        print()

    # Do groups overlap in subcube space?
    # For each pair of 4-flip groups, do they share any 4D subcubes?
    print(f"\n  4-flip group subcube overlap:")
    four_flip = [(1,1,0,0,1,1), (1,0,1,1,0,1), (0,1,1,1,1,0)]
    for i in range(3):
        for j in range(i+1, 3):
            mi, mj = four_flip[i], four_flip[j]
            # They have different fixed dims, so they partition differently
            # Check if any vertex appears in both groups' subcube spaces
            fi = [d for d in range(DIMS) if mi[d] == 0]
            fj = [d for d in range(DIMS) if mj[d] == 0]
            print(f"    {MASK_NAMES[mi]} fixed={[d+1 for d in fi]}, "
                  f"{MASK_NAMES[mj]} fixed={[d+1 for d in fj]}: "
                  f"shared fixed dims={set(fi) & set(fj)}")


# ─── 4. Subcube Adjacency ────────────────────────────────────────────────────

def subcube_adjacency():
    print("\n" + "=" * 70)
    print("4. ADJACENCY BETWEEN OCCUPIED SUBCUBES")
    print("=" * 70)

    # For 2-flip groups, each pair lives in a 2D subcube (a face)
    # How are these faces related? Adjacent? Opposite?
    for mask in sorted(groups.keys(), key=lambda m: (sum(m), m)):
        if sum(mask) != 2:
            continue
        g = groups[mask]
        mname = MASK_NAMES[mask]
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]

        print(f"\n  {mname} — 4 pairs in 4 faces (2D subcubes)")
        keys = [subcube_key(p['a'], fixed_dims) for p in g]

        print(f"    Face keys: {[''.join(map(str,k)) for k in keys]}")

        # Hamming distance between face keys
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                d = sum(a != b for a, b in zip(keys[i], keys[j]))
                print(f"    {''.join(map(str,keys[i]))} ↔ "
                      f"{''.join(map(str,keys[j]))}: Hamming={d}")

    # For 4-flip groups, 2 subcubes each
    for mask in sorted(groups.keys(), key=lambda m: (sum(m), m)):
        if sum(mask) != 4:
            continue
        g = groups[mask]
        mname = MASK_NAMES[mask]
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]

        keys = set()
        for p in g:
            keys.add(subcube_key(p['a'], fixed_dims))

        print(f"\n  {mname} — 4 pairs in 2 hypercubes (4D subcubes)")
        keys = sorted(keys)
        print(f"    Subcube keys: {[''.join(map(str,k)) for k in keys]}")
        d = sum(a != b for a, b in zip(keys[0], keys[1]))
        print(f"    Hamming distance between subcubes: {d}")
        print(f"    (keys are complements: {all(a != b for a, b in zip(keys[0], keys[1]))})")


# ─── 5. The Missing Vertices ─────────────────────────────────────────────────

def missing_vertices():
    print("\n" + "=" * 70)
    print("5. MISSING VERTICES IN EACH SUBCUBE")
    print("=" * 70)

    for mask in sorted(groups.keys(), key=lambda m: (-sum(m), m)):
        if sum(mask) == 6:
            continue  # complement uses full cube, skip

        g = groups[mask]
        mname = MASK_NAMES[mask]
        fixed_dims = [i for i in range(DIMS) if mask[i] == 0]
        flip_dims = [i for i in range(DIMS) if mask[i] == 1]
        n_flips = sum(mask)

        print(f"\n  {mname}:")

        subcube_verts = defaultdict(set)
        for p in g:
            key = subcube_key(p['a'], fixed_dims)
            subcube_verts[key].add(project(p['a'], flip_dims))
            subcube_verts[key].add(project(p['b'], flip_dims))

        for key in sorted(subcube_verts.keys()):
            present = subcube_verts[key]
            all_possible = set(product([0, 1], repeat=n_flips))
            missing = all_possible - present

            key_str = ''.join(map(str, key))
            print(f"    [{key_str}]: present={len(present)}, "
                  f"missing={len(missing)}")

            # What's the structure of the missing vertices?
            # Are they connected? Do they form a sub-subcube?
            missing_list = sorted(missing)
            if len(missing_list) > 1:
                # Pairwise Hamming
                dists = []
                for i in range(len(missing_list)):
                    for j in range(i+1, len(missing_list)):
                        d = sum(a != b for a, b in zip(missing_list[i], missing_list[j]))
                        dists.append(d)
                print(f"      Missing Hamming distances: {Counter(dists)}")

                # Do missing vertices form a subcube?
                # Check if they're closed under XOR with any basis
                is_subcube = False
                if len(missing_list) in [2, 4, 8, 16]:
                    # Check closure: for any two missing, their XOR should also be missing (mod offset)
                    origin = missing_list[0]
                    translated = set()
                    for v in missing_list:
                        translated.add(tuple(a ^ b for a, b in zip(v, origin)))
                    # A subcube's translated set should be closed under XOR
                    closed = True
                    for v1 in translated:
                        for v2 in translated:
                            xor = tuple(a ^ b for a, b in zip(v1, v2))
                            if xor not in translated:
                                closed = False
                                break
                        if not closed:
                            break
                    is_subcube = closed

                print(f"      Missing form a subcube: {is_subcube}")

            # Which group do the missing hexagrams belong to?
            missing_groups = Counter()
            for mv in missing:
                # Reconstruct full vertex
                full = [0] * DIMS
                fi = 0
                fxi = 0
                for d in range(DIMS):
                    if mask[d] == 1:
                        full[d] = mv[fi]
                        fi += 1
                    else:
                        full[d] = key[fxi]
                        fxi += 1
                full_tuple = tuple(full)
                # Find which pair this belongs to
                for p in pairs:
                    if p['a'] == full_tuple or p['b'] == full_tuple:
                        missing_groups[p['name']] += 1
                        break

            print(f"      Missing vertices belong to: {dict(missing_groups)}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("SUBCUBE OCCUPATION ANALYSIS")
    print("=" * 70)

    full_subcube_map()
    pair_geometry()
    coverage_analysis()
    subcube_adjacency()
    missing_vertices()

    print("\n" + "=" * 70)
    print("SUBCUBE ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
