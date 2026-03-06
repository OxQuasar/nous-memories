"""
Orbit analysis of the King Wen sequence under the generator group.

The 3 generators O (flip L1,L6), M (flip L2,L5), I (flip L3,L4) generate
the group Z₂³ acting on {0,1}^6. Since no generator has fixed points,
every orbit has exactly 8 elements — partitioning 64 hexagrams into 8 orbits.

Each orbit is a 3-cube (Q₃) embedded in {0,1}^6.
"""

import numpy as np
from collections import Counter, defaultdict
from itertools import combinations
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
N_PAIRS = 32
RNG = np.random.default_rng(42)
N_TRIALS = 10000

M = np.array(all_bits())

# Generator actions (bit indices to flip)
GEN_FLIPS = {
    'O': [0, 5],   # lines 1, 6
    'M': [1, 4],   # lines 2, 5
    'I': [2, 3],   # lines 3, 4
}

# All 8 group elements as subsets of {O, M, I}
GROUP = [
    frozenset(),            # identity
    frozenset({'O'}),
    frozenset({'M'}),
    frozenset({'I'}),
    frozenset({'O', 'M'}),
    frozenset({'O', 'I'}),
    frozenset({'M', 'I'}),
    frozenset({'O', 'M', 'I'}),
]

MASK_NAMES = {
    (0,0,0,0,0,0): 'id',
    (1,0,0,0,0,1): 'O',
    (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I',
    (1,1,0,0,1,1): 'OM',
    (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI',
    (1,1,1,1,1,1): 'OMI',
}


def apply_group_element(h, gens):
    """Apply a group element (set of generators) to a hexagram."""
    h = list(h)
    for g in gens:
        for idx in GEN_FLIPS[g]:
            h[idx] = 1 - h[idx]
    return tuple(h)


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ─── Build orbits ────────────────────────────────────────────────────────────

def build_orbits():
    seen = set()
    orbits = []
    for i in range(N):
        h = tuple(M[i])
        if h in seen:
            continue
        orbit = {}
        for g in GROUP:
            gh = apply_group_element(h, g)
            # Find the KW index for this hexagram
            for j in range(N):
                if tuple(M[j]) == gh:
                    label = ''.join(sorted(g)) if g else 'id'
                    orbit[gh] = {'kw_idx': j, 'kw_num': j + 1,
                                 'name': KING_WEN[j][1], 'group_el': g}
                    seen.add(gh)
                    break
        orbits.append(orbit)
    return orbits

orbits = build_orbits()

# Build pair info
pairs = []
for k in range(N_PAIRS):
    a = tuple(M[2 * k])
    b = tuple(M[2 * k + 1])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    pairs.append({'idx': k, 'a': a, 'b': b, 'mask': xor,
                  'name': MASK_NAMES[xor]})


# ─── 1. Orbit Composition ────────────────────────────────────────────────────

def orbit_composition():
    print("=" * 70)
    print("1. ORBIT COMPOSITION (8 orbits of size 8 under Z₂³)")
    print("=" * 70)

    for oi, orbit in enumerate(orbits):
        verts = sorted(orbit.keys())
        kw_nums = sorted(orbit[v]['kw_num'] for v in verts)
        names = [orbit[v]['name'] for v in sorted(orbit.keys(),
                 key=lambda v: orbit[v]['kw_num'])]

        # Orbit representative (lowest KW number)
        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        rep = orbit[rep_v]

        # Weight distribution
        weights = sorted(sum(v) for v in verts)

        print(f"\n  Orbit {oi+1} (rep: #{rep['kw_num']} {rep['name']}):")
        print(f"    KW numbers: {kw_nums}")
        print(f"    Names: {', '.join(names)}")
        print(f"    Weights: {weights}  (sum={sum(weights)})")


# ─── 2. Orbit Geometry ───────────────────────────────────────────────────────

def orbit_geometry():
    print("\n" + "=" * 70)
    print("2. ORBIT GEOMETRY (each orbit as a 3-cube in {0,1}^6)")
    print("=" * 70)

    for oi, orbit in enumerate(orbits):
        verts = np.array(sorted(orbit.keys()))
        center = verts.mean(axis=0)

        # Which dimensions vary?
        varying = [d for d in range(DIMS) if len(set(verts[:, d])) > 1]
        fixed = [d for d in range(DIMS) if d not in varying]
        fixed_vals = {d+1: int(verts[0, d]) for d in fixed}

        # Check: do varying dims match O,M,I pairs?
        # O: dims 0,5; M: dims 1,4; I: dims 2,3
        # All orbits should vary on exactly dims 0,1,2,3,4,5 since OMI flips all
        # BUT: the orbit is a 3-cube, meaning it varies on 3 "effective" dimensions
        # The 3 generators each flip 2 bits, so 6 bits vary but in pairs

        # Pairwise distances within orbit
        dists = []
        for i in range(8):
            for j in range(i + 1, 8):
                dists.append(hamming(tuple(verts[i]), tuple(verts[j])))
        dist_counter = Counter(dists)

        # Verify it's a 3-cube: should have distances {2:12, 4:12, 6:4}
        # (Q₃ has edges at dist 2, face diags at dist 4, space diags at dist 6)
        # Wait — in standard Q₃ with Hamming: dist 1:12, dist 2:12, dist 3:4
        # But here each "edge" flips 2 bits, so distances are 2,4,6

        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        rep = orbit[rep_v]

        print(f"\n  Orbit {oi+1} ({rep['name']}):")
        print(f"    Center: [{', '.join(f'{c:.2f}' for c in center)}]")
        print(f"    Fixed dims: {fixed_vals if fixed_vals else 'none (all vary)'}")
        print(f"    Pairwise Hamming: {dict(sorted(dist_counter.items()))}")

    # Verify all are isomorphic Q₃ with doubled edge weights
    expected = {2: 12, 4: 12, 6: 4}
    all_q3 = True
    for oi, orbit in enumerate(orbits):
        verts = list(orbit.keys())
        dists = Counter()
        for i in range(8):
            for j in range(i + 1, 8):
                dists[hamming(verts[i], verts[j])] += 1
        if dict(dists) != expected:
            all_q3 = False
            print(f"\n  WARNING: Orbit {oi+1} is not a standard doubled Q₃: {dict(dists)}")

    print(f"\n  All orbits are doubled Q₃ (distances {{2,4,6}}): {all_q3}")


# ─── 3. King Wen Pairs and Orbits ────────────────────────────────────────────

def pairs_and_orbits():
    print("\n" + "=" * 70)
    print("3. KING WEN PAIRS AND ORBITS")
    print("=" * 70)

    # Each pair connects two hexagrams by a generator — must be in same orbit
    # Which pairs are in which orbit?
    orbit_lookup = {}
    for oi, orbit in enumerate(orbits):
        for v in orbit:
            orbit_lookup[v] = oi

    pair_orbits = []
    for p in pairs:
        oa = orbit_lookup[p['a']]
        ob = orbit_lookup[p['b']]
        pair_orbits.append((oa, ob))
        if oa != ob:
            print(f"  WARNING: Pair {p['idx']+1} crosses orbits! {oa+1} → {ob+1}")

    # All pairs should be within orbits (since pair = generator application)
    all_intra = all(oa == ob for oa, ob in pair_orbits)
    print(f"\n  All pairs are intra-orbit: {all_intra}")

    # Pairs per orbit
    orbit_pairs = defaultdict(list)
    for pi, (oa, ob) in enumerate(pair_orbits):
        orbit_pairs[oa].append(pi)

    for oi, orbit in enumerate(orbits):
        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        plist = orbit_pairs[oi]
        pair_names = [pairs[pi]['name'] for pi in plist]
        print(f"  Orbit {oi+1} ({orbit[rep_v]['name']}): "
              f"{len(plist)} pairs — {pair_names}")

    # Each orbit has 8 vertices, 12 edges (at dist 2, i.e. single-generator).
    # 4 pairs per orbit would cover 8 vertices if each pair is a perfect matching.
    # Do the 4 pairs form a perfect matching of the orbit?
    print(f"\n  Perfect matching test (4 pairs cover 8 vertices exactly once):")
    for oi, orbit in enumerate(orbits):
        plist = orbit_pairs[oi]
        covered = set()
        for pi in plist:
            covered.add(pairs[pi]['a'])
            covered.add(pairs[pi]['b'])
        verts = set(orbit.keys())
        print(f"    Orbit {oi+1}: {len(covered)}/8 vertices covered, "
              f"missing={len(verts - covered)}")


# ─── 4. Orbit Traversal ──────────────────────────────────────────────────────

def orbit_traversal():
    print("\n" + "=" * 70)
    print("4. ORBIT TRAVERSAL (sequence of orbits visited)")
    print("=" * 70)

    orbit_lookup = {}
    for oi, orbit in enumerate(orbits):
        for v in orbit:
            orbit_lookup[v] = oi

    # Sequence of orbits
    orbit_seq = [orbit_lookup[tuple(M[i])] for i in range(N)]

    # Pairs visit orbits in this order:
    pair_orbit_seq = [orbit_lookup[pairs[k]['a']] for k in range(N_PAIRS)]

    print(f"\n  Hexagram orbit sequence (1-indexed):")
    for row in range(8):
        chunk = orbit_seq[row*8:(row+1)*8]
        hex_start = row * 8 + 1
        print(f"    Hex {hex_start:2d}-{hex_start+7:2d}: "
              f"{' '.join(str(o+1) for o in chunk)}")

    print(f"\n  Pair orbit sequence:")
    print(f"    {' → '.join(str(o+1) for o in pair_orbit_seq)}")

    # How many distinct orbits visited per octet?
    print(f"\n  Orbits per octet:")
    for oct_i in range(8):
        oct_orbits = pair_orbit_seq[oct_i*4:(oct_i+1)*4]
        unique = len(set(oct_orbits))
        print(f"    O{oct_i+1}: orbits {oct_orbits} ({unique} unique)")

    # Transition matrix: orbit_i → orbit_j at bridges
    trans = np.zeros((8, 8), dtype=int)
    for k in range(N_PAIRS - 1):
        trans[pair_orbit_seq[k], pair_orbit_seq[k + 1]] += 1

    print(f"\n  Orbit transition matrix (bridges):")
    print(f"    {'':>4s} " + ' '.join(f'O{j+1}' for j in range(8)))
    for i in range(8):
        row = ' '.join(f'{trans[i,j]:2d}' for j in range(8))
        print(f"    O{i+1}: {row}")

    # Self-transitions (staying in same orbit across bridge)
    self_trans = sum(trans[i, i] for i in range(8))
    print(f"\n  Self-transitions (bridge stays in same orbit): "
          f"{self_trans}/{N_PAIRS-1}")


# ─── 5. Orbit Centers and Inter-Orbit Geometry ──────────────────────────────

def orbit_centers():
    print("\n" + "=" * 70)
    print("5. ORBIT CENTERS AND INTER-ORBIT GEOMETRY")
    print("=" * 70)

    centers = []
    for oi, orbit in enumerate(orbits):
        verts = np.array(list(orbit.keys()))
        center = verts.mean(axis=0)
        centers.append(center)

        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        print(f"  Orbit {oi+1} ({orbit[rep_v]['name']}): "
              f"[{', '.join(f'{c:.2f}' for c in center)}]  "
              f"weight={sum(center):.1f}")

    # Center equivalence classes
    print(f"\n  Center equivalence classes:")
    center_groups = defaultdict(list)
    for oi, c in enumerate(centers):
        key = tuple(round(x, 4) for x in c)
        center_groups[key].append(oi + 1)

    for key, orbits_in_class in sorted(center_groups.items(),
                                        key=lambda x: -len(x[1])):
        print(f"    [{', '.join(f'{k:.2f}' for k in key)}]: "
              f"orbits {orbits_in_class}")

    # Inter-orbit distances
    print(f"\n  Inter-orbit center distances:")
    for i in range(8):
        for j in range(i + 1, 8):
            d = np.linalg.norm(centers[i] - centers[j])
            if d < 0.5:
                print(f"    O{i+1}↔O{j+1}: {d:.3f} (close)")

    # Do orbit centers sum to [0.5]*6 in pairs?
    print(f"\n  Complement center test (c_i + c_j = [0.5]*6):")
    target = np.array([0.5] * 6)
    for i in range(8):
        for j in range(i + 1, 8):
            avg = (centers[i] + centers[j]) / 2
            if np.allclose(avg, target, atol=0.01):
                print(f"    O{i+1}+O{j+1}: centers average to [0.50]*6")


# ─── 6. Generator Edges Within Orbits ────────────────────────────────────────

def generator_edges():
    print("\n" + "=" * 70)
    print("6. GENERATOR EDGES WITHIN ORBITS (which Q₃ edges are used?)")
    print("=" * 70)

    orbit_lookup = {}
    for oi, orbit in enumerate(orbits):
        for v in orbit:
            orbit_lookup[v] = oi

    # Each orbit is Q₃. Each edge corresponds to a single generator (O, M, or I).
    # The 4 King Wen pairs in each orbit use specific edges.
    # Q₃ has 12 edges: 4 of type O, 4 of type M, 4 of type I.
    # 4 pairs must use exactly 4 of the 12 edges.

    for oi, orbit in enumerate(orbits):
        verts = list(orbit.keys())
        # Find which pairs are in this orbit
        orbit_pairs = [p for p in pairs if p['a'] in orbit]

        # Count generator usage
        gen_usage = Counter()
        edges_used = []
        for p in orbit_pairs:
            gen_usage[p['name']] += 1
            edges_used.append((p['a'], p['b'], p['name']))

        # Which generators are missing?
        # Each generator creates 4 edges in Q₃
        all_edges = {'O': [], 'M': [], 'I': []}
        for v in verts:
            for gen_name, flips in GEN_FLIPS.items():
                w = list(v)
                for idx in flips:
                    w[idx] = 1 - w[idx]
                w = tuple(w)
                edge = (min(v, w), max(v, w))
                if edge not in all_edges[gen_name]:
                    all_edges[gen_name].append(edge)

        # Which generator-edges are used by KW pairs?
        used_edges = set()
        for p in orbit_pairs:
            edge = (min(p['a'], p['b']), max(p['a'], p['b']))
            used_edges.add(edge)

        gen_edge_usage = {}
        for gen_name, edges in all_edges.items():
            used = sum(1 for e in edges if e in used_edges)
            gen_edge_usage[gen_name] = f"{used}/{len(edges)}"

        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        print(f"\n  Orbit {oi+1} ({orbit[rep_v]['name']}):")
        print(f"    Pairs: {[p['name'] for p in orbit_pairs]}")
        print(f"    Edges used per generator: O={gen_edge_usage['O']}, "
              f"M={gen_edge_usage['M']}, I={gen_edge_usage['I']}")

    # Do the 4 pairs always form a perfect matching?
    print(f"\n  Perfect matching verification:")
    for oi, orbit in enumerate(orbits):
        orbit_pairs_list = [p for p in pairs if p['a'] in orbit]
        vertices_covered = set()
        for p in orbit_pairs_list:
            if p['a'] in vertices_covered or p['b'] in vertices_covered:
                print(f"    Orbit {oi+1}: NOT a perfect matching (vertex reuse)")
                break
            vertices_covered.add(p['a'])
            vertices_covered.add(p['b'])
        else:
            print(f"    Orbit {oi+1}: perfect matching "
                  f"(4 pairs cover 8 vertices, no overlap)")


# ─── 7. Orbit Invariants ─────────────────────────────────────────────────────

def orbit_invariants():
    print("\n" + "=" * 70)
    print("7. ORBIT INVARIANTS (what's constant within each orbit?)")
    print("=" * 70)

    for oi, orbit in enumerate(orbits):
        verts = list(orbit.keys())

        # Since O flips (b0,b5), M flips (b1,b4), I flips (b2,b3),
        # the invariants are:
        # b0 XOR b5 (preserved by O since both flip; preserved by M,I since neither flips)
        # b1 XOR b4 (preserved by M; preserved by O,I)
        # b2 XOR b3 (preserved by I; preserved by O,M)
        # Wait — O flips both b0 and b5, so b0⊕b5 is preserved (both flip → XOR unchanged)
        # M,I don't touch b0,b5, so b0⊕b5 is preserved.
        # So b0⊕b5, b1⊕b4, b2⊕b3 are orbit invariants.

        inv_05 = verts[0][0] ^ verts[0][5]
        inv_14 = verts[0][1] ^ verts[0][4]
        inv_23 = verts[0][2] ^ verts[0][3]

        # Verify
        all_same = all(
            v[0] ^ v[5] == inv_05 and
            v[1] ^ v[4] == inv_14 and
            v[2] ^ v[3] == inv_23
            for v in verts
        )

        # Also: b0+b5, b1+b4, b2+b3 sums are NOT invariants (they change)
        # But b0⊕b5 is the "line symmetry" between the mirror positions

        # Trigram relationship: within an orbit, do upper and lower trigrams
        # have a fixed relationship?
        lower_tris = set(''.join(map(str, v[:3])) for v in verts)
        upper_tris = set(''.join(map(str, v[3:])) for v in verts)

        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        rep = orbit[rep_v]

        # Signature: the 3 XOR invariants
        sig = f"({inv_05},{inv_14},{inv_23})"

        print(f"\n  Orbit {oi+1} ({rep['name']}):")
        print(f"    XOR invariants: L1⊕L6={inv_05}, L2⊕L5={inv_14}, "
              f"L3⊕L4={inv_23}  → signature {sig}")
        print(f"    Verified: {all_same}")
        print(f"    Lower trigrams: {sorted(lower_tris)}")
        print(f"    Upper trigrams: {sorted(upper_tris)}")

    # How many distinct signatures?
    sigs = set()
    for oi, orbit in enumerate(orbits):
        v = list(orbit.keys())[0]
        sigs.add((v[0]^v[5], v[1]^v[4], v[2]^v[3]))

    print(f"\n  Distinct XOR signatures: {len(sigs)}/8")
    print(f"  Signatures: {sorted(sigs)}")

    # There are 2³ = 8 possible XOR signatures, and 8 orbits.
    # Each signature should appear exactly once.
    sig_orbits = defaultdict(list)
    for oi, orbit in enumerate(orbits):
        v = list(orbit.keys())[0]
        sig = (v[0]^v[5], v[1]^v[4], v[2]^v[3])
        sig_orbits[sig].append(oi + 1)

    print(f"  Signature → Orbits:")
    for sig in sorted(sig_orbits.keys()):
        print(f"    {sig}: orbit(s) {sig_orbits[sig]}")


# ─── 8. Sequence Position Within Orbits ──────────────────────────────────────

def sequence_positions():
    print("\n" + "=" * 70)
    print("8. SEQUENCE POSITIONS WITHIN ORBITS")
    print("=" * 70)

    orbit_lookup = {}
    for oi, orbit in enumerate(orbits):
        for v in orbit:
            orbit_lookup[v] = oi

    # For each orbit, list the KW positions of its 8 hexagrams
    for oi, orbit in enumerate(orbits):
        positions = sorted(orbit[v]['kw_num'] for v in orbit)
        gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        span = positions[-1] - positions[0]

        # How spread out? Coefficient of variation
        mean_pos = np.mean(positions)
        std_pos = np.std(positions)

        # First half vs second half
        first_half = sum(1 for p in positions if p <= 32)
        second_half = sum(1 for p in positions if p > 32)

        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        print(f"\n  Orbit {oi+1} ({orbit[rep_v]['name']}):")
        print(f"    Positions: {positions}")
        print(f"    Gaps: {gaps}  span={span}")
        print(f"    Canon split: {first_half} upper / {second_half} lower")

    # Are orbits uniformly scattered or clustered?
    print(f"\n  Orbit spread (std of positions):")
    for oi, orbit in enumerate(orbits):
        positions = [orbit[v]['kw_num'] for v in orbit]
        rep_v = min(orbit.keys(), key=lambda v: orbit[v]['kw_num'])
        print(f"    Orbit {oi+1} ({orbit[rep_v]['name']}): "
              f"mean={np.mean(positions):.1f}, std={np.std(positions):.1f}")

    # Compare to random: what's the expected std for 8 of 64?
    random_stds = []
    for _ in range(N_TRIALS):
        sample = RNG.choice(64, size=8, replace=False) + 1
        random_stds.append(np.std(sample))

    actual_stds = []
    for orbit in orbits:
        positions = [orbit[v]['kw_num'] for v in orbit]
        actual_stds.append(np.std(positions))

    mean_actual = np.mean(actual_stds)
    mean_random = np.mean(random_stds)
    print(f"\n  Mean orbit spread: {mean_actual:.1f} "
          f"(random: {mean_random:.1f} ± {np.std(random_stds):.1f})")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("ORBIT ANALYSIS OF THE KING WEN SEQUENCE")
    print("Generator group Z₂³ = ⟨O, M, I⟩ acting on {0,1}^6")
    print("=" * 70)

    orbit_composition()
    orbit_geometry()
    pairs_and_orbits()
    orbit_traversal()
    orbit_centers()
    generator_edges()
    orbit_invariants()
    sequence_positions()

    print("\n" + "=" * 70)
    print("ORBIT ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
