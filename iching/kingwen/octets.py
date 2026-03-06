"""
Octet-level analysis of the King Wen sequence.
Groups of 4 consecutive pairs (8 hexagrams). 8 octets total.
"""

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
N_PAIRS = 32
N_OCTETS = 8
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


# Build pairs
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

# Build octets
octets = []
for o in range(N_OCTETS):
    oct_pairs = pairs[4 * o: 4 * (o + 1)]
    hexes = []
    hex_indices = []
    for p in oct_pairs:
        hexes.extend([p['a'], p['b']])
        hex_indices.extend([2 * p['idx'], 2 * p['idx'] + 1])
    gen_seq = [p['name'] for p in oct_pairs]
    octets.append({
        'idx': o,
        'pairs': oct_pairs,
        'hexes': hexes,
        'hex_indices': hex_indices,
        'gen_seq': gen_seq,
    })


# ─── 1. Octet Composition ────────────────────────────────────────────────────

def composition():
    print("=" * 70)
    print("1. OCTET COMPOSITION")
    print("=" * 70)

    for o in octets:
        names = [KING_WEN[i][1] for i in o['hex_indices']]
        cn_names = []
        CN = {
            'Qian': '乾', 'Kun': '坤', 'Zhun': '屯', 'Meng': '蒙',
            'Xu': '需', 'Song': '訟', 'Shi': '師', 'Bi': '比',
            'Xiao Chu': '小畜', 'Lu': '履', 'Tai': '泰', 'Pi': '否',
            'Tong Ren': '同人', 'Da You': '大有', 'Qian': '謙', 'Yu': '豫',
            'Sui': '隨', 'Gu': '蠱', 'Lin': '臨', 'Guan': '觀',
            'Shi He': '噬嗑', 'Bo': '剝', 'Fu': '復',
            'Wu Wang': '無妄', 'Da Chu': '大畜', 'Yi': '頤', 'Da Guo': '大過',
            'Kan': '坎', 'Li': '離', 'Xian': '咸', 'Heng': '恆',
            'Dun': '遯', 'Da Zhuang': '大壯', 'Jin': '晉', 'Ming Yi': '明夷',
            'Jia Ren': '家人', 'Kui': '睽', 'Jian': '蹇', 'Xie': '解',
            'Sun': '損', 'Guai': '夬', 'Gou': '姤',
            'Cui': '萃', 'Sheng': '升', 'Jing': '井',
            'Ge': '革', 'Ding': '鼎', 'Zhen': '震', 'Gen': '艮',
            'Gui Mei': '歸妹', 'Feng': '豐',
            'Xun': '巽', 'Dui': '兌', 'Huan': '渙', 'Jie': '節',
            'Zhong Fu': '中孚', 'Xiao Guo': '小過', 'Ji Ji': '既濟', 'Wei Ji': '未濟',
        }

        gen_str = '→'.join(o['gen_seq'])
        print(f"\n  O{o['idx']+1}: pairs {4*o['idx']+1}-{4*o['idx']+4}  "
              f"(hex {o['hex_indices'][0]+1}-{o['hex_indices'][-1]+1})")
        print(f"    Generators: {gen_str}")
        print(f"    Hexagrams: {', '.join(names)}")

    # Generator vocabulary per octet
    print(f"\n  Generator vocabulary per octet:")
    for o in octets:
        vocab = set(o['gen_seq'])
        gen_bits_union = 0
        gen_bits_inter = 7
        for p in o['pairs']:
            gen_bits_union |= p['gen_bits']
            gen_bits_inter &= p['gen_bits']
        union_gens = []
        inter_gens = []
        for bit, g in [(1, 'O'), (2, 'M'), (4, 'I')]:
            if gen_bits_union & bit: union_gens.append(g)
            if gen_bits_inter & bit: inter_gens.append(g)
        print(f"    O{o['idx']+1}: types={sorted(vocab)}, "
              f"union={','.join(union_gens)}, "
              f"intersect={','.join(inter_gens) if inter_gens else '∅'}")


# ─── 2. Octet Geometry ───────────────────────────────────────────────────────

def geometry():
    print("\n" + "=" * 70)
    print("2. OCTET GEOMETRY (8 vertices in the hypercube)")
    print("=" * 70)

    for o in octets:
        verts = np.array(o['hexes'])
        center = verts.mean(axis=0)
        per_dim = [verts[:, d].mean() for d in range(DIMS)]
        balanced = sum(1 for b in per_dim if b == 0.5)

        # Span
        span = sum(1 for d in range(DIMS) if len(set(verts[:, d])) > 1)

        # Pairwise distances
        dists = []
        for i in range(8):
            for j in range(i + 1, 8):
                dists.append(hamming(tuple(verts[i]), tuple(verts[j])))
        dist_counter = Counter(dists)

        # Weight distribution
        weights = [sum(v) for v in verts]

        print(f"\n  O{o['idx']+1}: {' → '.join(o['gen_seq'])}")
        print(f"    Center: [{', '.join(f'{c:.2f}' for c in center)}]  "
              f"({balanced}/6 balanced)")
        print(f"    Span: {span}/6 dimensions")
        print(f"    Pairwise Hamming: {dict(sorted(dist_counter.items()))}")
        print(f"    Mean pairwise: {np.mean(dists):.2f}")
        print(f"    Weights: {weights}")
        print(f"    Weight range: {min(weights)}-{max(weights)}")

    # Do any octets form a 3-cube (all 8 vertices of a 3D subcube)?
    print(f"\n  3-cube test (8 vertices spanning exactly 3 dimensions):")
    for o in octets:
        verts = np.array(o['hexes'])
        varying = [d for d in range(DIMS) if len(set(verts[:, d])) > 1]
        if len(varying) == 3:
            fixed = [d for d in range(DIMS) if d not in varying]
            fixed_vals = tuple(verts[0, d] for d in fixed)
            # Check if all 8 vertices of this 3-cube are present
            projected = set(tuple(verts[i, d] for d in varying) for i in range(8))
            print(f"    O{o['idx']+1}: varying={[d+1 for d in varying]}, "
                  f"projected vertices={len(projected)}/8")
        else:
            print(f"    O{o['idx']+1}: span={len(varying)} (not a 3-cube)")


# ─── 3. Octet Masks ──────────────────────────────────────────────────────────

def octet_masks():
    print("\n" + "=" * 70)
    print("3. OCTET MASKS (line coverage)")
    print("=" * 70)

    for o in octets:
        masks = [p['mask'] for p in o['pairs']]
        union = [0] * DIMS
        inter = [1] * DIMS
        for m in masks:
            for d in range(DIMS):
                union[d] = max(union[d], m[d])
                inter[d] = min(inter[d], m[d])

        union_str = ''.join(map(str, union))
        inter_str = ''.join(map(str, inter))
        n_union = sum(union)
        n_inter = sum(inter)

        # Which mask types appear?
        mask_names = [p['name'] for p in o['pairs']]
        unique_masks = len(set(p['mask'] for p in o['pairs']))

        print(f"\n  O{o['idx']+1}: {' → '.join(mask_names)}")
        print(f"    Union mask:  {union_str} ({n_union} lines)")
        print(f"    Intersection: {inter_str} ({n_inter} lines)")
        print(f"    Unique pair masks: {unique_masks}/4")

    # All octets should have union = 111111
    all_full = all(
        all(max(p['mask'][d] for p in o['pairs']) == 1 for d in range(DIMS))
        for o in octets
    )
    print(f"\n  All octets cover all 6 lines: {all_full}")


# ─── 4. Octet Generator Algebra ──────────────────────────────────────────────

def generator_algebra():
    print("\n" + "=" * 70)
    print("4. OCTET GENERATOR ALGEBRA")
    print("=" * 70)

    # Each octet has 4 generator types. What's the structure?
    for o in octets:
        gen_bits = [p['gen_bits'] for p in o['pairs']]

        # XOR of all pairs
        xor_all = 0
        for g in gen_bits:
            xor_all ^= g

        # OR of all pairs (generators used)
        or_all = 0
        for g in gen_bits:
            or_all |= g

        # AND of all pairs (generators always present)
        and_all = 7
        for g in gen_bits:
            and_all &= g

        used = [g for bit, g in [(1, 'O'), (2, 'M'), (4, 'I')] if or_all & bit]
        always = [g for bit, g in [(1, 'O'), (2, 'M'), (4, 'I')] if and_all & bit]

        # Generator count per type
        o_count = sum(1 for g in gen_bits if g & 1)
        m_count = sum(1 for g in gen_bits if g & 2)
        i_count = sum(1 for g in gen_bits if g & 4)

        print(f"\n  O{o['idx']+1}: {' → '.join(o['gen_seq'])}")
        print(f"    O={o_count}/4, M={m_count}/4, I={i_count}/4")
        print(f"    Always active: {','.join(always) if always else '∅'}")
        print(f"    XOR of all: {xor_all:03b} "
              f"({''.join(g for bit, g in [(1,'O'),(2,'M'),(4,'I')] if xor_all & bit) or '0'})")


# ─── 5. Octet Trigram Coverage ────────────────────────────────────────────────

def trigram_coverage():
    print("\n" + "=" * 70)
    print("5. OCTET TRIGRAM COVERAGE")
    print("=" * 70)

    for o in octets:
        upper = Counter()
        lower = Counter()
        for h in o['hexes']:
            lt = ''.join(map(str, h[:3]))
            ut = ''.join(map(str, h[3:]))
            lower[lt] += 1
            upper[ut] += 1

        print(f"\n  O{o['idx']+1}:")
        print(f"    Upper trigrams ({len(upper)}/8): "
              f"{dict(sorted(upper.items(), key=lambda x: -x[1]))}")
        print(f"    Lower trigrams ({len(lower)}/8): "
              f"{dict(sorted(lower.items(), key=lambda x: -x[1]))}")

    # Does each octet use all 8 trigrams?
    for o in octets:
        upper = set()
        lower = set()
        for h in o['hexes']:
            lower.add(''.join(map(str, h[:3])))
            upper.add(''.join(map(str, h[3:])))
        o['full_upper'] = len(upper) == 8
        o['full_lower'] = len(lower) == 8

    full_both = sum(1 for o in octets if o['full_upper'] and o['full_lower'])
    print(f"\n  Octets with complete trigram coverage: {full_both}/8")


# ─── 6. Octet Symmetry ───────────────────────────────────────────────────────

def symmetry():
    print("\n" + "=" * 70)
    print("6. OCTET-LEVEL SYMMETRY (first half vs second half)")
    print("=" * 70)

    # O_k vs O_{9-k}
    print(f"\n  Mirror pairs (O_k vs O_{N_OCTETS+1}-k):")
    for k in range(N_OCTETS // 2):
        mirror = N_OCTETS - 1 - k
        o1 = octets[k]
        o2 = octets[mirror]

        # Center distance
        c1 = np.mean(np.array(o1['hexes']), axis=0)
        c2 = np.mean(np.array(o2['hexes']), axis=0)
        cdist = np.linalg.norm(c1 - c2)

        # Generator overlap
        g1 = set(o1['gen_seq'])
        g2 = set(o2['gen_seq'])
        shared = g1 & g2

        # Weight comparison
        w1 = sorted(sum(h) for h in o1['hexes'])
        w2 = sorted(sum(h) for h in o2['hexes'])

        print(f"\n    O{k+1} vs O{mirror+1}:")
        print(f"      Generators: {o1['gen_seq']} vs {o2['gen_seq']}")
        print(f"      Shared types: {shared}")
        print(f"      Center distance: {cdist:.3f}")
        print(f"      Weights: {w1} vs {w2}")
        print(f"      Weight sums: {sum(w1)} vs {sum(w2)}")

    # Do mirror octets sum to 24 (= 8 hexes × 3 mean weight)?
    print(f"\n  Mirror weight sum test (should be 24+24=48 if balanced):")
    for k in range(N_OCTETS // 2):
        mirror = N_OCTETS - 1 - k
        w1 = sum(sum(h) for h in octets[k]['hexes'])
        w2 = sum(sum(h) for h in octets[mirror]['hexes'])
        print(f"    O{k+1}+O{mirror+1}: {w1}+{w2}={w1+w2}")


# ─── 7. Octet as Narrative Arc ────────────────────────────────────────────────

def narrative():
    print("\n" + "=" * 70)
    print("7. OCTET WEIGHT TRAJECTORIES")
    print("=" * 70)

    for o in octets:
        weights = [sum(h) for h in o['hexes']]
        changes = [weights[k+1] - weights[k] for k in range(7)]

        # Net change
        net = weights[-1] - weights[0]

        # Trajectory shape
        ascending = sum(1 for c in changes if c > 0)
        descending = sum(1 for c in changes if c < 0)
        flat = sum(1 for c in changes if c == 0)

        print(f"\n  O{o['idx']+1}: {' → '.join(o['gen_seq'])}")
        print(f"    Weights: {' → '.join(map(str, weights))}")
        print(f"    Changes: {' '.join(f'{c:+d}' for c in changes)}")
        print(f"    Net: {weights[0]}→{weights[-1]} (Δ={net:+d})")
        print(f"    Up={ascending} Down={descending} Flat={flat}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("OCTET-LEVEL ANALYSIS OF THE KING WEN SEQUENCE")
    print("=" * 70)

    composition()
    geometry()
    octet_masks()
    generator_algebra()
    trigram_coverage()
    symmetry()
    narrative()

    print("\n" + "=" * 70)
    print("OCTET ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
