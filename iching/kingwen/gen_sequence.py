"""
Does the sequence of change generators relate to the hypercube geometry?
Track the path through generator space and subcube space simultaneously.
"""

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
N_PAIRS = 32
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

# Generator encoding: O=1, M=2, I=4 (bit flags)
GEN_BITS = {'O': 1, 'M': 2, 'I': 4, 'OM': 3, 'OI': 5, 'MI': 6, 'OMI': 7}

# Build pair sequence
pair_seq = []
for k in range(N_PAIRS):
    a = M[2 * k]
    b = M[2 * k + 1]
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    name = MASKS[xor]
    fixed_dims = [i for i in range(DIMS) if xor[i] == 0]
    fixed_key = tuple(a[d] for d in fixed_dims) if fixed_dims else ()
    pair_seq.append({
        'idx': k,
        'a': tuple(a), 'b': tuple(b),
        'mask': xor, 'name': name,
        'gen_bits': GEN_BITS[name],
        'fixed_key': fixed_key,
        'center': (a + b) / 2.0,
    })


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


# ─── 1. Generator Path in Boolean Lattice ────────────────────────────────────

def lattice_path():
    print("=" * 70)
    print("1. PATH THROUGH THE BOOLEAN LATTICE {O, M, I}")
    print("=" * 70)

    names = [p['name'] for p in pair_seq]
    bits = [p['gen_bits'] for p in pair_seq]

    # XOR between consecutive generators (which generators switch on/off)
    print(f"\n  Generator sequence and transitions:")
    print(f"  {'Pair':>4s}  {'Gen':>4s}  {'Bits':>4s}  {'XOR':>4s}  Transition")
    for k in range(N_PAIRS):
        if k == 0:
            print(f"  {k+1:4d}  {names[k]:>4s}  {bits[k]:03b}   ---  (start)")
        else:
            xor = bits[k] ^ bits[k-1]
            xor_str = []
            if xor & 1: xor_str.append('O')
            if xor & 2: xor_str.append('M')
            if xor & 4: xor_str.append('I')
            direction = '+' if bits[k] > bits[k-1] else '-' if bits[k] < bits[k-1] else '='
            print(f"  {k+1:4d}  {names[k]:>4s}  {bits[k]:03b}   {xor:03b}  "
                  f"{'±' if not xor_str else ','.join(xor_str)} "
                  f"({'add' if bin(bits[k]).count('1') > bin(bits[k-1]).count('1') else 'remove' if bin(bits[k]).count('1') < bin(bits[k-1]).count('1') else 'swap'})")

    # Lattice distance (Hamming in generator space)
    lattice_dists = []
    for k in range(N_PAIRS - 1):
        xor = bits[k] ^ bits[k + 1]
        lattice_dists.append(bin(xor).count('1'))

    print(f"\n  Lattice step distances: {lattice_dists}")
    print(f"  Distribution: {Counter(lattice_dists)}")
    print(f"  Mean: {np.mean(lattice_dists):.2f}")

    # Compare to random
    null_means = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(bits)
        null_dists = [bin(perm[k] ^ perm[k+1]).count('1') for k in range(N_PAIRS - 1)]
        null_means.append(np.mean(null_dists))
    null_means = np.array(null_means)
    p = np.mean(null_means >= np.mean(lattice_dists))
    print(f"  Random mean: {np.mean(null_means):.2f} ± {np.std(null_means):.2f}")
    print(f"  p(≥actual): {p:.4f}")


# ─── 2. Subcube Transitions ──────────────────────────────────────────────────

def subcube_transitions():
    print("\n" + "=" * 70)
    print("2. SUBCUBE TRANSITIONS")
    print("=" * 70)

    print(f"\n  Consecutive pair subcube positions:")
    print(f"  {'Pair':>4s}  {'Gen':>4s}  {'Fixed key':>10s}  {'Center dist':>11s}  "
          f"{'Hex dist':>8s}")

    for k in range(N_PAIRS):
        fk = ''.join(map(str, pair_seq[k]['fixed_key'])) if pair_seq[k]['fixed_key'] else '-'
        if k == 0:
            print(f"  {k+1:4d}  {pair_seq[k]['name']:>4s}  {fk:>10s}       ---       ---")
        else:
            cdist = np.linalg.norm(pair_seq[k]['center'] - pair_seq[k-1]['center'])
            # Hamming between exit hex and entry hex
            hdist = hamming(pair_seq[k-1]['b'], pair_seq[k]['a'])
            print(f"  {k+1:4d}  {pair_seq[k]['name']:>4s}  {fk:>10s}  "
                  f"{cdist:11.3f}  {hdist:8d}")

    # When we stay in the same generator, do we move between subcubes?
    print(f"\n  Same-generator transitions:")
    for gen_name in ['OMI', 'OM', 'OI', 'MI', 'O', 'M', 'I']:
        positions = [p['idx'] for p in pair_seq if p['name'] == gen_name]
        if len(positions) < 2:
            continue
        # Find consecutive occurrences (not necessarily adjacent in sequence)
        consecutive_in_seq = []
        for i in range(len(positions) - 1):
            if positions[i + 1] == positions[i] + 1:
                k1, k2 = positions[i], positions[i + 1]
                fk1 = pair_seq[k1]['fixed_key']
                fk2 = pair_seq[k2]['fixed_key']
                same_sub = fk1 == fk2
                consecutive_in_seq.append((k1 + 1, k2 + 1, same_sub))

        if consecutive_in_seq:
            print(f"    {gen_name}: consecutive pairs in sequence: "
                  f"{[(a, b, 'same subcube' if s else 'diff subcube') for a, b, s in consecutive_in_seq]}")


# ─── 3. Generator Activation Pattern ─────────────────────────────────────────

def activation_pattern():
    print("\n" + "=" * 70)
    print("3. GENERATOR ACTIVATION SIGNALS")
    print("=" * 70)

    # Track O, M, I as three binary signals through the 32 pairs
    O_signal = [1 if p['gen_bits'] & 1 else 0 for p in pair_seq]
    M_signal = [1 if p['gen_bits'] & 2 else 0 for p in pair_seq]
    I_signal = [1 if p['gen_bits'] & 4 else 0 for p in pair_seq]

    signals = {'O': O_signal, 'M': M_signal, 'I': I_signal}

    print(f"\n  Generator activation through the sequence:")
    print(f"  {'Pair':>4s}  O M I  Gen")
    for k in range(N_PAIRS):
        print(f"  {k+1:4d}  {O_signal[k]} {M_signal[k]} {I_signal[k]}  {pair_seq[k]['name']}")

    # Correlation between generator signals
    print(f"\n  Generator signal correlations:")
    for g1, s1 in signals.items():
        for g2, s2 in signals.items():
            if g1 >= g2:
                continue
            corr = np.corrcoef(s1, s2)[0, 1]
            print(f"    {g1}-{g2}: r={corr:+.3f}")

    # Autocorrelation of each generator signal
    print(f"\n  Generator autocorrelation:")
    for gname, sig in signals.items():
        sig = np.array(sig, dtype=float) - np.mean(sig)
        print(f"    {gname}:", end="")
        for lag in [1, 2, 3, 4, 8, 16]:
            shifted = np.roll(sig, lag)
            ac = np.corrcoef(sig, shifted)[0, 1]
            print(f"  lag{lag}={ac:+.3f}", end="")
        print()

    # Count of each generator
    print(f"\n  Generator frequency:")
    for gname in ['O', 'M', 'I']:
        count = sum(signals[gname])
        print(f"    {gname}: active in {count}/32 pairs ({count/32*100:.1f}%)")


# ─── 4. Relationship Between Generator Path and Hypercube Path ───────────────

def generator_vs_hypercube():
    print("\n" + "=" * 70)
    print("4. GENERATOR PATH vs HYPERCUBE PATH")
    print("=" * 70)

    # For each bridge (pair k → pair k+1), measure:
    # - Lattice distance (generator change)
    # - Hypercube distance (bridge Hamming)
    # - Center distance
    # Are these correlated?

    lattice_d = []
    bridge_h = []
    center_d = []

    for k in range(N_PAIRS - 1):
        # Lattice distance
        xor = pair_seq[k]['gen_bits'] ^ pair_seq[k+1]['gen_bits']
        ld = bin(xor).count('1')
        lattice_d.append(ld)

        # Bridge Hamming
        bh = hamming(pair_seq[k]['b'], pair_seq[k+1]['a'])
        bridge_h.append(bh)

        # Center distance
        cd = np.linalg.norm(pair_seq[k+1]['center'] - pair_seq[k]['center'])
        center_d.append(cd)

    print(f"\n  Correlation between path metrics:")
    print(f"    Lattice dist ↔ Bridge Hamming: "
          f"r={np.corrcoef(lattice_d, bridge_h)[0,1]:+.3f}")
    print(f"    Lattice dist ↔ Center dist:    "
          f"r={np.corrcoef(lattice_d, center_d)[0,1]:+.3f}")
    print(f"    Bridge Hamming ↔ Center dist:   "
          f"r={np.corrcoef(bridge_h, center_d)[0,1]:+.3f}")

    # Mean bridge Hamming by lattice step type
    print(f"\n  Bridge Hamming by generator transition type:")
    by_type = defaultdict(list)
    for k in range(N_PAIRS - 1):
        by_type[lattice_d[k]].append(bridge_h[k])

    for ld in sorted(by_type):
        vals = by_type[ld]
        print(f"    Lattice step {ld}: "
              f"mean bridge Hamming={np.mean(vals):.2f}, n={len(vals)}")

    # Does changing more generators correlate with bigger jumps?
    print(f"\n  Bridge by specific generator change:")
    for k in range(N_PAIRS - 1):
        xor = pair_seq[k]['gen_bits'] ^ pair_seq[k+1]['gen_bits']
        added = []
        removed = []
        for bit, gname in [(1, 'O'), (2, 'M'), (4, 'I')]:
            if xor & bit:
                if pair_seq[k+1]['gen_bits'] & bit:
                    added.append(gname)
                else:
                    removed.append(gname)
        change_str = ""
        if added: change_str += "+" + ",".join(added)
        if removed: change_str += "-" + ",".join(removed)
        if not change_str: change_str = "(same)"
        # Only print if interesting
        if not added and not removed:
            continue


# ─── 5. Fixed Key Transitions ────────────────────────────────────────────────

def fixed_key_path():
    print("\n" + "=" * 70)
    print("5. FIXED KEY TRANSITIONS (subcube identity changes)")
    print("=" * 70)

    # For 2-flip groups, track which of the 4 subcubes they visit
    # All use keys {0000, 0110, 1001, 1111}
    print(f"\n  2-flip subcube key sequence:")
    for gen_name in ['O', 'M', 'I']:
        members = [(p['idx'], p['fixed_key']) for p in pair_seq if p['name'] == gen_name]
        key_strs = [''.join(map(str, fk)) for _, fk in members]
        positions = [idx + 1 for idx, _ in members]
        print(f"    {gen_name}: positions {positions}, keys {key_strs}")

        # Are the keys ordered by weight?
        weights = [sum(fk) for _, fk in members]
        print(f"       weights: {weights}")

    # For 4-flip groups
    print(f"\n  4-flip subcube key sequence:")
    for gen_name in ['OM', 'OI', 'MI']:
        members = [(p['idx'], p['fixed_key']) for p in pair_seq if p['name'] == gen_name]
        key_strs = [''.join(map(str, fk)) for _, fk in members]
        positions = [idx + 1 for idx, _ in members]
        print(f"    {gen_name}: positions {positions}, keys {key_strs}")

    # Do the subcube keys follow a pattern across the full sequence?
    print(f"\n  Combined subcube key weight sequence (OMI has no key → weight 3):")
    weights = []
    for p in pair_seq:
        if p['name'] == 'OMI':
            weights.append(3)  # virtual "center"
        else:
            weights.append(sum(p['fixed_key']))
    print(f"    {weights}")

    # Autocorrelation of weight sequence
    w = np.array(weights, dtype=float)
    w -= w.mean()
    print(f"\n  Weight autocorrelation:")
    for lag in [1, 2, 3, 4, 8, 16]:
        shifted = np.roll(w, lag)
        ac = np.corrcoef(w, shifted)[0, 1]
        print(f"    lag {lag:2d}: r={ac:+.3f}")


# ─── 6. Generator Transitions as Hypercube Moves ─────────────────────────────

def gen_as_cube_moves():
    print("\n" + "=" * 70)
    print("6. COMPLETE PAIR-TO-PAIR PATH")
    print("=" * 70)

    # For each consecutive pair, show the full picture:
    # exit hex → bridge → entry hex → intra-pair → exit hex
    print(f"\n  {'':>4s}  {'Exit':>7s} →{'Bridge':>5s}→ {'Entry':>7s}  "
          f"{'Gen':>4s}  {'Sub':>5s}")

    for k in range(N_PAIRS):
        exit_hex = ''.join(map(str, pair_seq[k]['b']))
        entry_hex = ''.join(map(str, pair_seq[k]['a']))
        fk = ''.join(map(str, pair_seq[k]['fixed_key'])) if pair_seq[k]['fixed_key'] else '-'

        if k == 0:
            print(f"  {k+1:4d}  {' ':>7s}  {'':>5s}  {entry_hex}  "
                  f"{pair_seq[k]['name']:>4s}  {fk:>5s}")
        else:
            prev_exit = ''.join(map(str, pair_seq[k-1]['b']))
            bridge_h = hamming(pair_seq[k-1]['b'], pair_seq[k]['a'])
            print(f"  {k+1:4d}  {prev_exit} →{bridge_h:3d}  → {entry_hex}  "
                  f"{pair_seq[k]['name']:>4s}  {fk:>5s}")

    # Summary: what fraction of the total path is bridges vs intra-pair?
    bridge_total = sum(hamming(pair_seq[k]['b'], pair_seq[k+1]['a'])
                       for k in range(N_PAIRS - 1))
    intra_total = sum(hamming(pair_seq[k]['a'], pair_seq[k]['b'])
                      for k in range(N_PAIRS))
    total_path = bridge_total + intra_total

    print(f"\n  Path Hamming budget:")
    print(f"    Intra-pair (diagonal): {intra_total} ({intra_total/total_path*100:.1f}%)")
    print(f"    Bridges (free):        {bridge_total} ({bridge_total/total_path*100:.1f}%)")
    print(f"    Total path Hamming:    {total_path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("GENERATOR SEQUENCE vs HYPERCUBE GEOMETRY")
    print("=" * 70)

    lattice_path()
    subcube_transitions()
    activation_pattern()
    generator_vs_hypercube()
    fixed_key_path()
    gen_as_cube_moves()

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
