#!/usr/bin/env python3
"""dynamics_probe.py — Five computations probing φ in I Ching dynamics.

Threads:
  1 (2A): Full pullback spectra on F₂³ and Z₅ quotient
  2 (2B): Cube-edge partition spectra
  3 (5):  E=1 family fiber partitions
  4 (3):  Hexagram transition balance
  5 (4):  互 (hugua) basin structure
"""

import numpy as np
from collections import Counter, defaultdict
from itertools import product as iprod
from math import factorial

# ════════════════════════════════════════════════════════════
# Constants
# ════════════════════════════════════════════════════════════

PHI = (1 + np.sqrt(5)) / 2
PSI = (1 - np.sqrt(5)) / 2  # = -1/φ

# Surjection f: F₂³ → Z₅
# 000→2, 001→2, 010→4, 011→0, 100→0, 101→1, 110→3, 111→3
F_MAP = [2, 2, 4, 0, 0, 1, 3, 3]

# Z₅ encoding: Wood=0, Fire=1, Earth=2, Metal=3, Water=4
ELEMENT_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}

# Fiber sizes: D = diag(2,1,2,2,1) for elements 0..4
FIBER_SIZES = {0: 2, 1: 1, 2: 2, 3: 2, 4: 1}
FIBERS = defaultdict(list)
for _x, _e in enumerate(F_MAP):
    FIBERS[_e].append(_x)

N_TRIGRAMS = 8
N_ELEMENTS = 5
N_HEXAGRAMS = 64
N_LINES = 6


# ════════════════════════════════════════════════════════════
# Utilities
# ════════════════════════════════════════════════════════════

def hamming_adjacent(x, y):
    """True if x,y differ in exactly 1 bit (3-bit)."""
    d = x ^ y
    return d != 0 and (d & (d - 1)) == 0


def detect_phi(eigenvalues, label=""):
    """Check if φ, 1/φ, -φ, or -1/φ appear among eigenvalues."""
    targets = {'φ': PHI, '1/φ': 1/PHI, '-φ': -PHI, '-1/φ': -1/PHI}
    found = {}
    for name, val in targets.items():
        for ev in eigenvalues:
            if abs(ev - val) < 1e-10:
                found[name] = val
                break
    return found


def charpoly_has_x2_minus_x_minus_1(eigenvalues):
    """Check if x²-x-1 divides the characteristic polynomial.
    Roots of x²-x-1 are φ and -1/φ = ψ."""
    has_phi = any(abs(ev - PHI) < 1e-10 for ev in eigenvalues)
    has_psi = any(abs(ev - PSI) < 1e-10 for ev in eigenvalues)
    return has_phi and has_psi


def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


def sorted_eigs(M):
    """Real eigenvalues of real matrix, sorted descending."""
    vals = np.linalg.eigvalsh(M) if np.allclose(M, M.T) else np.linalg.eigvals(M).real
    return np.sort(vals)[::-1]


# ════════════════════════════════════════════════════════════
# Computation 1: Thread 2A — Full Pullback Spectra
# ════════════════════════════════════════════════════════════

def computation_1():
    print("=" * 72)
    print("COMPUTATION 1 (Thread 2A): Full Pullback Spectra")
    print("=" * 72)

    f = F_MAP

    # ── 8×8 pullback adjacency matrices ──
    A_sheng = np.zeros((8, 8), dtype=float)
    A_ke = np.zeros((8, 8), dtype=float)

    for x in range(8):
        for y in range(8):
            if x == y:
                continue
            d = (f[y] - f[x]) % 5
            if d in (1, 4):  # 生: ±1 mod 5
                A_sheng[x, y] = 1
            if d in (2, 3):  # 克: ±2 mod 5
                A_ke[x, y] = 1

    n_sheng_edges = int(A_sheng.sum()) // 2
    n_ke_edges = int(A_ke.sum()) // 2

    eigs_sheng_8 = sorted_eigs(A_sheng)
    eigs_ke_8 = sorted_eigs(A_ke)

    print(f"\n  8×8 生-pullback: {n_sheng_edges} edges")
    print(f"    Eigenvalues: {np.round(eigs_sheng_8, 6)}")
    phi_sheng = detect_phi(eigs_sheng_8)
    print(f"    φ-related eigenvalues: {phi_sheng if phi_sheng else 'NONE'}")
    print(f"    x²−x−1 divides charpoly: {charpoly_has_x2_minus_x_minus_1(eigs_sheng_8)}")

    print(f"\n  8×8 克-pullback: {n_ke_edges} edges")
    print(f"    Eigenvalues: {np.round(eigs_ke_8, 6)}")
    phi_ke = detect_phi(eigs_ke_8)
    print(f"    φ-related eigenvalues: {phi_ke if phi_ke else 'NONE'}")
    print(f"    x²−x−1 divides charpoly: {charpoly_has_x2_minus_x_minus_1(eigs_ke_8)}")

    # ── 5×5 quotient matrices ──
    fiber_size = [FIBER_SIZES[a] for a in range(5)]

    Q_sheng = np.zeros((5, 5), dtype=float)
    Q_ke = np.zeros((5, 5), dtype=float)

    for a in range(5):
        for b in range(5):
            d = (b - a) % 5
            if d in (1, 4):
                Q_sheng[a, b] = fiber_size[b]
            if d in (2, 3):
                Q_ke[a, b] = fiber_size[b]

    eigs_sheng_5 = sorted_eigs(Q_sheng)
    eigs_ke_5 = sorted_eigs(Q_ke)

    print(f"\n  5×5 quotient Q_生:")
    print(f"    Matrix:\n{Q_sheng}")
    print(f"    Eigenvalues: {np.round(eigs_sheng_5, 6)}")

    print(f"\n  5×5 quotient Q_克:")
    print(f"    Matrix:\n{Q_ke}")
    print(f"    Eigenvalues: {np.round(eigs_ke_5, 6)}")

    # ── Verify quotient eigs are subset of 8×8 eigs ──
    for label, eigs5, eigs8 in [("生", eigs_sheng_5, eigs_sheng_8),
                                 ("克", eigs_ke_5, eigs_ke_8)]:
        remaining = list(eigs8)
        all_found = True
        for ev5 in eigs5:
            matched = False
            for i, ev8 in enumerate(remaining):
                if abs(ev5 - ev8) < 1e-8:
                    remaining.pop(i)
                    matched = True
                    break
            if not matched:
                all_found = False
        print(f"\n  Quotient eigs ⊆ pullback eigs ({label}): {all_found}")
        if all_found:
            print(f"    Remaining (fiber-only) eigenvalues: {np.round(remaining, 6)}")

    # φ detection on quotient
    for label, eigs5 in [("Q_生", eigs_sheng_5), ("Q_克", eigs_ke_5)]:
        phi5 = detect_phi(eigs5)
        has_min = charpoly_has_x2_minus_x_minus_1(eigs5)
        print(f"\n  {label} φ-detection: {phi5 if phi5 else 'NONE'}")
        print(f"  {label} x²−x−1 divides charpoly: {has_min}")

    return {
        'sheng_8': eigs_sheng_8, 'ke_8': eigs_ke_8,
        'sheng_5': eigs_sheng_5, 'ke_5': eigs_ke_5,
        'phi_sheng': bool(phi_sheng), 'phi_ke': bool(phi_ke),
    }


# ════════════════════════════════════════════════════════════
# Computation 2: Thread 2B — Cube-Edge Partition Spectra
# ════════════════════════════════════════════════════════════

def computation_2():
    print("\n" + "=" * 72)
    print("COMPUTATION 2 (Thread 2B): Cube-Edge Partition Spectra")
    print("=" * 72)

    f = F_MAP

    A_sheng = np.zeros((8, 8), dtype=float)
    A_ke = np.zeros((8, 8), dtype=float)
    A_bihe = np.zeros((8, 8), dtype=float)
    A_cube = np.zeros((8, 8), dtype=float)

    for x in range(8):
        for y in range(8):
            if not hamming_adjacent(x, y):
                continue
            A_cube[x, y] = 1
            d = (f[y] - f[x]) % 5
            if d in (1, 4):
                A_sheng[x, y] = 1
            elif d in (2, 3):
                A_ke[x, y] = 1
            else:  # d == 0
                A_bihe[x, y] = 1

    # Verify partition
    partition_ok = np.allclose(A_sheng + A_ke + A_bihe, A_cube)
    print(f"\n  A_生 + A_克 + A_比和 = A_cube: {partition_ok}")

    n_sheng = int(A_sheng.sum()) // 2
    n_ke = int(A_ke.sum()) // 2
    n_bihe = int(A_bihe.sum()) // 2
    n_cube = int(A_cube.sum()) // 2
    print(f"  Edge counts: 生={n_sheng}, 克={n_ke}, 比和={n_bihe}, total={n_cube} (expect 12)")

    # Eigenvalues
    eigs_cube = sorted_eigs(A_cube)
    eigs_sheng = sorted_eigs(A_sheng)
    eigs_ke = sorted_eigs(A_ke)
    eigs_bihe = sorted_eigs(A_bihe)

    print(f"\n  A_cube eigenvalues: {np.round(eigs_cube, 6)}")
    print(f"    Expected: [3, 1, 1, 1, -1, -1, -1, -3]")
    cube_ok = np.allclose(sorted(eigs_cube, reverse=True), [3, 1, 1, 1, -1, -1, -1, -3])
    print(f"    Match: {cube_ok}")

    print(f"\n  A_生 eigenvalues: {np.round(eigs_sheng, 6)}")
    phi_s = detect_phi(eigs_sheng)
    print(f"    φ-related: {phi_s if phi_s else 'NONE'}")
    print(f"    x²−x−1 divides charpoly: {charpoly_has_x2_minus_x_minus_1(eigs_sheng)}")

    print(f"\n  A_克 eigenvalues: {np.round(eigs_ke, 6)}")
    phi_k = detect_phi(eigs_ke)
    print(f"    φ-related: {phi_k if phi_k else 'NONE'}")
    print(f"    x²−x−1 divides charpoly: {charpoly_has_x2_minus_x_minus_1(eigs_ke)}")

    print(f"\n  A_比和 eigenvalues: {np.round(eigs_bihe, 6)}")
    phi_b = detect_phi(eigs_bihe)
    print(f"    φ-related: {phi_b if phi_b else 'NONE'}")
    print(f"    x²−x−1 divides charpoly: {charpoly_has_x2_minus_x_minus_1(eigs_bihe)}")

    # Show edge details
    print("\n  Edge detail (Hamming-adjacent pairs):")
    for x in range(8):
        for y in range(x+1, 8):
            if not hamming_adjacent(x, y):
                continue
            d = (f[y] - f[x]) % 5
            if d in (1, 4):
                rel = "生"
            elif d in (2, 3):
                rel = "克"
            else:
                rel = "比和"
            bit = (x ^ y).bit_length() - 1
            print(f"    {x:03b}({ELEMENT_NAMES[f[x]]:>5})—{y:03b}({ELEMENT_NAMES[f[y]]:>5})"
                  f"  bit{bit}  d={d}  {rel}")

    return {
        'phi_sheng': bool(phi_s), 'phi_ke': bool(phi_k), 'phi_bihe': bool(phi_b),
        'eigs_sheng': eigs_sheng, 'eigs_ke': eigs_ke, 'eigs_bihe': eigs_bihe,
    }


# ════════════════════════════════════════════════════════════
# Computation 3: Thread 5 — E=1 Family Partitions
# ════════════════════════════════════════════════════════════

def complement(x, n):
    return x ^ ((1 << n) - 1)


def get_complement_pairs(n):
    pairs, seen = [], set()
    for x in range(1 << n):
        if x not in seen:
            cx = complement(x, n)
            seen.add(x); seen.add(cx)
            pairs.append((min(x, cx), max(x, cx)))
    return sorted(pairs)


def enumerate_comp_surjections(n, p):
    """Complement-equivariant surjections F₂ⁿ → Z_p, as rep-value tuples."""
    pairs = get_complement_pairs(n)
    R = len(pairs)
    surjections = []
    for vals in iprod(range(p), repeat=R):
        image = set()
        for v in vals:
            image.add(v)
            image.add((-v) % p)
        if len(image) == p:
            surjections.append(vals)
    return surjections


def expand_rep_vals(rep_vals, pairs, p, N):
    f = [0] * N
    for i, (r, c) in enumerate(pairs):
        f[r] = rep_vals[i]
        f[c] = (-rep_vals[i]) % p
    return f


def fiber_partition(f_full, p):
    counts = Counter(f_full)
    return tuple(sorted(counts.values(), reverse=True))


def computation_3():
    print("\n" + "=" * 72)
    print("COMPUTATION 3 (Thread 5): E=1 Family Partitions")
    print("=" * 72)

    results = []

    for n in range(3, 9):
        p = (1 << n) - 3
        if not is_prime(p):
            print(f"\n  n={n}: p = 2^{n}-3 = {p} — NOT PRIME, skipping")
            continue

        N = 1 << n
        R = 1 << (n - 1)  # number of complement pairs
        E = R - (p + 1) // 2  # excess

        print(f"\n  n={n}: p={p}, N={N}, R={R}, E={E}")

        if n == 3:
            # Full enumeration feasible only at n=3 (5^4 = 625 candidates)
            pairs = get_complement_pairs(n)
            surjections = enumerate_comp_surjections(n, p)
            print(f"    Total surjections: {len(surjections)}")

            # Group by fiber partition
            partition_counts = Counter()
            for rv in surjections:
                ff = expand_rep_vals(rv, pairs, p, N)
                fp = fiber_partition(ff, p)
                partition_counts[fp] += 1

            for fp, cnt in sorted(partition_counts.items()):
                doubles = sum(1 for s in fp if s == 2)
                singles = sum(1 for s in fp if s == 1)
                ratio_str = f"{doubles}/{singles}" if singles > 0 else "N/A"
                print(f"    Partition {fp}: count={cnt}, "
                      f"doubletons={doubles}, singletons={singles}, ratio={ratio_str}")
                if fp == (2, 2, 2, 1, 1):
                    print(f"      ↑ (3,5) ratio = {doubles}/{singles} = {doubles/singles:.6f}")
                    print(f"        3/2 = 1.5 — compare φ = {PHI:.6f}")

            results.append({'n': n, 'p': p, 'partitions': dict(partition_counts)})
        else:
            # n≥4: p^R too large to enumerate; use analytical E=1 structure
            # Analytical: E=1 means exactly 1 pair beyond minimum
            # For E=1: (p+1)/2 negation classes, R = (p+1)/2 + 1 pairs
            # Either class 0 gets m₀=2 (Shape B, partition has one triple → no, 
            #   class 0 rep maps to 0, complement also to 0, so two extra 0-fibers)
            # Or some class j>0 gets doubled (Shape A)
            num_neg = (p - 1) // 2
            print(f"    Analytical (E=1):")
            print(f"    Shape B (class 0 doubled): partition = "
                  f"(3, 2×{num_neg-0}...) — class 0 has 4 elements, rest per negation class")
            # Actually: class 0 maps rep→0, comp→0. m₀=2 means 2 pairs map to class 0.
            # Each pair contributes 2 elements to fiber 0. So fiber(0) = 4.
            # Each other negation class {j, p-j} gets 1 pair → 2 elements total (1 in fiber j, 1 in fiber p-j).
            # So partition = (4, 2, 2, ..., 2, 1, 1, ..., 1) — wait, need to think more carefully.
            
            # Class 0: m₀=2 pairs, each contributes (0,0), so fiber(0) = 2*2 = 4
            # Negation class {j, p-j}: 1 pair → rep→j, comp→p-j, so fiber(j)=1, fiber(p-j)=1
            # Total fibers: fiber(0)=4, and for each of (p-1)/2 neg classes, two singletons
            # Partition = (4, 1, 1, ..., 1) with p-1 ones. Total = 4 + (p-1) = p+3 = 2^n
            shape_b_part = tuple([4] + [1]*(p-1))
            db = sum(1 for s in shape_b_part if s == 2)
            sb = sum(1 for s in shape_b_part if s == 1)
            print(f"      Shape B partition: {shape_b_part[:6]}... doubles={db}, singles={sb}")

            # Shape A (class j>0 doubled): 
            # m₀=1, one negation class gets 2 pairs → fiber(j)=2, fiber(p-j)=2
            # Others get 1 pair each → singletons
            # Partition = (2, 2, 2, 1, 1, ..., 1) — the doubled class gives two 2s,
            # class 0 gives fiber(0)=2, plus (p-3)/2 neg classes give singletons
            # Wait: m₀=1 → fiber(0) = 1*2 = 2
            # Doubled class j: 2 pairs → fiber(j)=2, fiber(p-j)=2
            # Other (p-1)/2 - 1 = (p-3)/2 neg classes: 1 pair each → fiber(k)=1, fiber(p-k)=1
            # Partition = (2, 2, 2, 1, 1, ..., 1) with 3 twos and (p-3) ones
            # Total = 3*2 + (p-3)*1 = 6 + p - 3 = p + 3 = 2^n ✓
            shape_a_part = tuple([2]*3 + [1]*(p-3))
            da = sum(1 for s in shape_a_part if s == 2)
            sa = sum(1 for s in shape_a_part if s == 1)
            ratio = da / sa if sa > 0 else float('inf')
            print(f"      Shape A partition: {shape_a_part[:8]}... doubles={da}, singles={sa}, ratio={da}/{sa} = {ratio:.6f}")
            print(f"      Expected ratio 3/(p-3) = 3/{p-3} = {3/(p-3):.6f}")

            results.append({'n': n, 'p': p, 'partitions': 'analytical'})

    # Summary
    print("\n  E=1 Family Ratio Summary:")
    print(f"  {'n':>3} {'p':>5} {'Shape A ratio':>20} {'= 3/(p-3)':>12}")
    print("  " + "-" * 44)
    for n in range(3, 9):
        p = (1 << n) - 3
        if not is_prime(p):
            continue
        ratio = 3 / (p - 3) if p > 3 else float('inf')
        print(f"  {n:>3} {p:>5} {ratio:>20.6f} {'= 3/2 = 1.5' if n==3 else f'= 3/{p-3}'}")

    print(f"\n  At (3,5): ratio = 3/2 = 1.5")
    print(f"  φ = {PHI:.6f}")
    print(f"  3/2 ≠ φ. The ratio 1.5 is NOT the golden ratio.")
    print(f"  Pattern: ratio → 0 as p grows. Fibonacci coincidence: NO.")

    return results


# ════════════════════════════════════════════════════════════
# Computation 4: Thread 3 — Transition Balance
# ════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 72)
    print("COMPUTATION 4 (Thread 3): Hexagram Transition Balance")
    print("=" * 72)

    f = F_MAP
    counts = Counter()  # 生, 克, 比和
    detail = defaultdict(list)

    for hex_val in range(N_HEXAGRAMS):
        lower = hex_val & 0b111
        upper = (hex_val >> 3) & 0b111

        for line in range(N_LINES):
            # Flip bit `line`
            new_hex = hex_val ^ (1 << line)
            new_lower = new_hex & 0b111
            new_upper = (new_hex >> 3) & 0b111

            if line < 3:
                # Lower trigram changes
                old_elem = f[lower]
                new_elem = f[new_lower]
            else:
                # Upper trigram changes
                old_elem = f[upper]
                new_elem = f[new_upper]

            d = (new_elem - old_elem) % 5
            if d == 0:
                rel = "比和"
            elif d in (1, 4):
                rel = "生"
            else:  # d in (2, 3)
                rel = "克"

            counts[rel] += 1
            detail[rel].append((hex_val, line, old_elem, new_elem, d))

    total = sum(counts.values())
    print(f"\n  Total transitions: {total} (expect {N_HEXAGRAMS * N_LINES} = 384)")
    print(f"  比和 (same element): {counts['比和']}")
    print(f"  生 (±1 mod 5):      {counts['生']}")
    print(f"  克 (±2 mod 5):      {counts['克']}")
    print(f"\n  Expected: 比和=64, 生=128, 克=192")
    print(f"  Match: 比和={'✓' if counts['比和']==64 else '✗'}, "
          f"生={'✓' if counts['生']==128 else '✗'}, "
          f"克={'✓' if counts['克']==192 else '✗'}")

    ratio_sheng_ke = f"{counts['生']}:{counts['克']}"
    print(f"\n  生:克 = {ratio_sheng_ke} = {counts['生']/counts['克']:.4f}")
    print(f"  = 2:3 exactly")

    # Breakdown by which bit flips
    print("\n  Breakdown by line position:")
    for line in range(N_LINES):
        c = Counter()
        trigram_part = "lower" if line < 3 else "upper"
        bit_in_trigram = line if line < 3 else line - 3
        for hex_val in range(N_HEXAGRAMS):
            new_hex = hex_val ^ (1 << line)
            if line < 3:
                old_e = f[hex_val & 0b111]
                new_e = f[new_hex & 0b111]
            else:
                old_e = f[(hex_val >> 3) & 0b111]
                new_e = f[(new_hex >> 3) & 0b111]
            d = (new_e - old_e) % 5
            if d == 0: c['比和'] += 1
            elif d in (1, 4): c['生'] += 1
            else: c['克'] += 1
        print(f"    Line {line+1} ({trigram_part} bit {bit_in_trigram}): "
              f"比和={c['比和']:>2}, 生={c['生']:>2}, 克={c['克']:>2}")

    return counts


# ════════════════════════════════════════════════════════════
# Computation 5: Thread 4 — Basin Structure (互 hugua)
# ════════════════════════════════════════════════════════════

def hugua(x):
    """互卦: extract lines 2-5 (0-indexed bits 1-4), overlap to form new hexagram.
    New lower = bits 1,2,3; New upper = bits 2,3,4."""
    b1 = (x >> 1) & 1
    b2 = (x >> 2) & 1
    b3 = (x >> 3) & 1
    b4 = (x >> 4) & 1
    return b1 | (b2 << 1) | (b3 << 2) | (b2 << 3) | (b3 << 4) | (b4 << 5)


def computation_5():
    print("\n" + "=" * 72)
    print("COMPUTATION 5 (Thread 4): 互 (Hugua) Basin Structure")
    print("=" * 72)

    # Compute chains for all 64 hexagrams
    chains = {}
    for x in range(N_HEXAGRAMS):
        chain = [x]
        visited = {x}
        cur = x
        while True:
            nxt = hugua(cur)
            if nxt in visited:
                chain.append(nxt)
                break
            visited.add(nxt)
            chain.append(nxt)
            cur = nxt
        chains[x] = chain

    # Find attractors
    attractors = set()
    for x, chain in chains.items():
        terminal = chain[-1]
        if hugua(terminal) == terminal:
            attractors.add((terminal,))  # fixed point
        else:
            # 2-cycle: terminal → hugua(terminal) → terminal
            a, b = terminal, hugua(terminal)
            attractors.add(tuple(sorted([a, b])))

    print(f"\n  Attractors ({len(attractors)}):")
    for att in sorted(attractors):
        if len(att) == 1:
            x = att[0]
            print(f"    Fixed point: {x:06b} (#{x}) — "
                  f"lower={x&0b111:03b}({ELEMENT_NAMES[F_MAP[x&0b111]]}), "
                  f"upper={(x>>3)&0b111:03b}({ELEMENT_NAMES[F_MAP[(x>>3)&0b111]]})")
        else:
            a, b = att
            print(f"    2-cycle: {a:06b} (#{a}) ↔ {b:06b} (#{b})")

    # Basin assignment
    def find_attractor(x):
        visited = []
        cur = x
        seen = set()
        while cur not in seen:
            seen.add(cur)
            visited.append(cur)
            cur = hugua(cur)
        # cur is in the attractor
        fp = hugua(cur)
        if fp == cur:
            return (cur,)
        return tuple(sorted([cur, fp]))

    basins = defaultdict(list)
    for x in range(N_HEXAGRAMS):
        att = find_attractor(x)
        basins[att].append(x)

    print(f"\n  Basin sizes:")
    for att in sorted(basins.keys()):
        print(f"    {att}: {len(basins[att])} hexagrams")

    # Depth distribution
    def depth(x):
        att = find_attractor(x)
        cur = x
        d = 0
        while True:
            if len(att) == 1 and cur == att[0]:
                return d
            if len(att) == 2 and cur in att:
                return d
            cur = hugua(cur)
            d += 1

    depth_dist = Counter()
    for x in range(N_HEXAGRAMS):
        depth_dist[depth(x)] += 1

    print(f"\n  Depth distribution:")
    for d in sorted(depth_dist.keys()):
        print(f"    Depth {d}: {depth_dist[d]} hexagrams")

    print(f"\n  Expected: {{0:4, 1:12, 2:48}}")
    depth_match = (depth_dist == Counter({0: 4, 1: 12, 2: 48}))
    print(f"  Match: {depth_match}")

    # Check: determined by bits 2,3 only
    print(f"\n  Bits-2,3 determination test:")
    # The hugua only depends on bits 1-4. After one iteration, it depends on bits 2-3.
    # Check: hugua(hugua(x)) depends only on bits 2,3 of x
    groups_by_bits23 = defaultdict(set)
    for x in range(N_HEXAGRAMS):
        bits23 = (x >> 2) & 0b11
        att = find_attractor(x)
        groups_by_bits23[bits23].add(att)

    all_determined = True
    for bits, atts in sorted(groups_by_bits23.items()):
        determined = len(atts) == 1
        if not determined:
            all_determined = False
        print(f"    bits[3:2]={bits:02b}: attractor(s) = {atts}, "
              f"basin_size = {sum(len(basins[a]) for a in atts)}, "
              f"determined: {determined}")

    print(f"\n  All determined by bits 2,3 only: {all_determined}")

    # Basin sizes check
    basin_sizes = sorted([len(v) for v in basins.values()], reverse=True)
    print(f"  Basin sizes (sorted): {basin_sizes}")
    expected_basins = sorted([32, 16, 16], reverse=True)
    print(f"  Expected: {expected_basins}")
    print(f"  Match: {basin_sizes == expected_basins}")

    # Show the trivial nature
    print(f"\n  Structure analysis:")
    print(f"  hugua maps 6-bit x to: lower=(b1,b2,b3), upper=(b2,b3,b4)")
    print(f"  After one step, bits 0,5 are lost. After two steps, bits 1,4 are lost.")
    print(f"  Fixed points satisfy: b1=b2, b3=b4, and lower=(b1,b2,b3), upper=(b2,b3,b4)")
    print(f"  → b0=b1=b2 and b3=b4=b5, giving 2×2 = 4 fixed points")

    return {
        'n_attractors': len(attractors),
        'basin_sizes': basin_sizes,
        'depth_dist': dict(depth_dist),
    }


# ════════════════════════════════════════════════════════════
# Shared helpers for computations 6-10
# ════════════════════════════════════════════════════════════

def _mat_vec_f2_3(rows, x):
    """3×3 F₂ matrix-vector multiply. rows = tuple of 3 row-ints."""
    r = 0
    for i, row in enumerate(rows):
        if bin(row & x).count('1') % 2:
            r |= 1 << i
    return r


# Stab(111) in GL(3,F₂): 24 matrices. Rows must have odd popcount: {1,2,4,7}.
# All 24 ordered triples of 3 distinct elements from {1,2,4,7} are invertible.
_STAB_PERMS = []
for _r0 in (1, 2, 4, 7):
    for _r1 in (1, 2, 4, 7):
        for _r2 in (1, 2, 4, 7):
            if len({_r0, _r1, _r2}) == 3:
                _STAB_PERMS.append(
                    tuple(_mat_vec_f2_3((_r0, _r1, _r2), x) for x in range(8)))


def canonical_surj(f8, p=5):
    """Lex-min image of 8-tuple f under Stab(111) × Aut(Z_p)."""
    best = f8
    for perm in _STAB_PERMS:
        g = tuple(f8[perm[x]] for x in range(8))
        for a in range(1, p):
            h = tuple((a * v) % p for v in g)
            if h < best:
                best = h
    return best


def classify_graph(adj, nv):
    """Canonical string for graph structure, e.g. 'P4+P4' or 'P3+P3+2I'."""
    vis = [False] * nv
    named = []  # (name, vertex_count)
    for s in range(nv):
        if vis[s]:
            continue
        q = [s]; vis[s] = True; vs = []
        while q:
            v = q.pop(0); vs.append(v)
            for u in range(nv):
                if adj[v, u] > 0 and not vis[u]:
                    vis[u] = True; q.append(u)
        n = len(vs)
        if n == 1:
            named.append(("I", 1)); continue
        degs = [int(sum(adj[v, u] for u in vs)) for v in vs]
        ne = sum(degs) // 2
        mx = max(degs)
        if ne == n - 1:  # tree
            name = f"P{n}" if mx <= 2 else (f"K1,{n-1}" if mx == n - 1 else f"T{n}")
        elif ne == n and all(d == 2 for d in degs):
            name = f"C{n}"
        else:
            name = f"G{n}({ne}e)"
        named.append((name, n))

    iso = sum(1 for nm, _ in named if nm == "I")
    rest = sorted([(nm, sz) for nm, sz in named if nm != "I"],
                  key=lambda t: (-t[1], t[0]))
    parts = [nm for nm, _ in rest]
    if iso > 1:
        parts.append(f"{iso}I")
    elif iso == 1:
        parts.append("I")
    return "+".join(parts) if parts else f"{nv}I"


def cube_partition(f, p=5):
    """Sub-adjacency matrices for n-cube edges by Z_p distance class."""
    N = len(f)
    A = {'生': np.zeros((N, N)), '克': np.zeros((N, N)), '比和': np.zeros((N, N))}
    for x in range(N):
        for y in range(x + 1, N):
            if not hamming_adjacent(x, y):
                continue
            d = (f[y] - f[x]) % p
            if d == 0:
                rel = '比和'
            elif d in (1, p - 1):
                rel = '生'
            elif d in (2, p - 2):
                rel = '克'
            else:
                continue  # for p > 5, other distance classes
            A[rel][x, y] = A[rel][y, x] = 1
    return A


def jac_type(f, p=5):
    """Jacobian type: sorted tuple of per-bit unsigned distance sets.
    Unsigned: min(d, p-d). Values: 0=比和, 1=生, 2=克."""
    bits = []
    for b in range(3):
        rels = set()
        for x in range(8):
            d = (f[x ^ (1 << b)] - f[x]) % p
            rels.add(min(d, p - d))
        bits.append(tuple(sorted(rels)))
    return tuple(sorted(bits))


def _get_all_240():
    """Return all 240 complement-equivariant surjections at (3,5) as 8-tuples."""
    p = 5
    pairs = get_complement_pairs(3)
    surjs = enumerate_comp_surjections(3, p)
    return [tuple(expand_rep_vals(rv, pairs, p, 8)) for rv in surjs]


# ════════════════════════════════════════════════════════════
# Computation 6: Full Orbit Taxonomy at (3,5)
# ════════════════════════════════════════════════════════════

def computation_6():
    print("\n" + "=" * 72)
    print("COMPUTATION 6: Full Orbit Taxonomy at (3,5)")
    print("=" * 72)

    p = 5
    fulls = _get_all_240()

    # 1. Classify orbits
    canons = [canonical_surj(f8, p) for f8 in fulls]
    canon_map = {}
    orbit_members = defaultdict(list)
    for i, c in enumerate(canons):
        if c not in canon_map:
            canon_map[c] = len(canon_map)
        orbit_members[canon_map[c]].append(i)

    orbit_sizes = sorted([len(m) for m in orbit_members.values()], reverse=True)
    print(f"\n  Orbits: {len(orbit_members)}, sizes: {orbit_sizes}")
    print(f"  Expected: [96, 48, 48, 24, 24]")

    # 2. For each surjection, compute cube-edge partition structures + φ detection
    surj_info = []  # (orbit_id, ke_struct, sh_struct, bh_struct, phi_ke, phi_sh)
    for i, f8 in enumerate(fulls):
        oid = canon_map[canons[i]]
        A = cube_partition(list(f8), p)
        ke_str = classify_graph(A['克'], 8)
        sh_str = classify_graph(A['生'], 8)
        bh_str = classify_graph(A['比和'], 8)
        phi_ke = bool(detect_phi(sorted_eigs(A['克'])))
        phi_sh = bool(detect_phi(sorted_eigs(A['生'])))
        surj_info.append((oid, ke_str, sh_str, bh_str, phi_ke, phi_sh))

    # 3. Structure triple cross-tabulation
    triple_counts = Counter()
    for oid, ke, sh, bh, _, _ in surj_info:
        triple_counts[(sh, ke, bh)] += 1

    print(f"\n  Distinct (生, 克, 比和) structure triples: {len(triple_counts)}")
    for (sh, ke, bh), cnt in sorted(triple_counts.items(), key=lambda x: -x[1]):
        print(f"    生={sh:<16} 克={ke:<16} 比和={bh:<16} count={cnt}")

    # 4. Per-orbit breakdown
    print(f"\n  Per-orbit breakdown:")
    for oid in sorted(orbit_members.keys()):
        members = orbit_members[oid]
        size = len(members)
        rep_f = fulls[members[0]]
        ke_strs = Counter()
        phi_ke_n = phi_sh_n = 0
        for idx in members:
            _, ke, sh, bh, pk, ps = surj_info[idx]
            ke_strs[ke] += 1
            phi_ke_n += pk
            phi_sh_n += ps
        print(f"\n    Orbit {oid} (size {size}), rep={rep_f}")
        print(f"      φ in 克: {phi_ke_n}/{size}  |  φ in 生: {phi_sh_n}/{size}")
        for ks, cnt in sorted(ke_strs.items(), key=lambda x: -x[1]):
            print(f"      克={ks}: {cnt}x")

    # Totals
    total_phi_ke = sum(1 for _, _, _, _, pk, _ in surj_info if pk)
    total_phi_sh = sum(1 for _, _, _, _, _, ps in surj_info if ps)
    total_neither = sum(1 for _, _, _, _, pk, ps in surj_info if not pk and not ps)
    print(f"\n  TOTALS: φ in 克 = {total_phi_ke}/240, "
          f"φ in 生 = {total_phi_sh}/240, neither = {total_neither}/240")

    # I Ching orbit
    iching_oid = canon_map[canonical_surj(tuple(F_MAP), p)]
    print(f"  I Ching orbit: {iching_oid} (size {len(orbit_members[iching_oid])})")

    return {
        'orbit_sizes': orbit_sizes,
        'total_phi_ke': total_phi_ke,
        'total_phi_sh': total_phi_sh,
        'total_neither': total_neither,
        'surj_info': surj_info,
        'fulls': fulls,
        'orbit_members': orbit_members,
        'canon_map': canon_map,
        'canons': canons,
    }


# ════════════════════════════════════════════════════════════
# Computation 7: Jacobian Type for All 240 Surjections
# ════════════════════════════════════════════════════════════

REL_LABELS = {0: '比和', 1: '生', 2: '克'}


def fmt_jac(jt):
    """Pretty-print a Jacobian type."""
    return str(tuple(tuple(REL_LABELS.get(d, f'd{d}') for d in bits) for bits in jt))


def computation_7():
    print("\n" + "=" * 72)
    print("COMPUTATION 7: Jacobian Type for All 240 Surjections")
    print("=" * 72)

    p = 5
    fulls = _get_all_240()
    canons = [canonical_surj(f8, p) for f8 in fulls]
    canon_map = {}
    orbit_members = defaultdict(list)
    for i, c in enumerate(canons):
        if c not in canon_map:
            canon_map[c] = len(canon_map)
        orbit_members[canon_map[c]].append(i)

    # Compute Jacobian type for each surjection
    jac_types = [jac_type(list(f8), p) for f8 in fulls]

    # Also classify 克 structure to identify P4+P4 surjections
    ke_is_p4p4 = []
    for f8 in fulls:
        A_ke = cube_partition(list(f8), p)['克']
        ke_is_p4p4.append(classify_graph(A_ke, 8) == "P4+P4")

    # Distinct Jacobian types
    all_types = Counter(jac_types)
    print(f"\n  Distinct Jacobian types: {len(all_types)}")
    for jt, cnt in sorted(all_types.items(), key=lambda x: -x[1]):
        print(f"    {fmt_jac(jt):>50}  count={cnt}")

    # Per-orbit distribution
    print(f"\n  Per-orbit Jacobian type distribution:")
    for oid in sorted(orbit_members.keys()):
        members = orbit_members[oid]
        type_counts = Counter(jac_types[i] for i in members)
        print(f"    Orbit {oid} (size {len(members)}):")
        for jt, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"      {fmt_jac(jt):>50}  {cnt}x")

    # Among surjections with 克=P₄∪P₄: is Jacobian type constant?
    p4_indices = [i for i, v in enumerate(ke_is_p4p4) if v]
    p4_types = Counter(jac_types[i] for i in p4_indices)
    print(f"\n  Surjections with 克=P₄+P₄: {len(p4_indices)}")
    print(f"    Jacobian types within this set: {len(p4_types)}")
    for jt, cnt in sorted(p4_types.items(), key=lambda x: -x[1]):
        print(f"      {fmt_jac(jt):>50}  {cnt}x")

    # I Ching specific
    iching_jt = jac_type(F_MAP, p)
    print(f"\n  I Ching Jacobian type: {fmt_jac(iching_jt)}")
    # Show per-bit detail
    for b in range(3):
        rels = set()
        for x in range(8):
            d = (F_MAP[x ^ (1 << b)] - F_MAP[x]) % p
            rels.add(min(d, p - d))
        print(f"    Bit {b}: distances = {sorted(rels)} "
              f"→ {{{', '.join(REL_LABELS[d] for d in sorted(rels))}}}")

    return {
        'n_types': len(all_types),
        'p4_types': p4_types,
        'iching_jt': iching_jt,
        'jac_types': jac_types,
        'ke_is_p4p4': ke_is_p4p4,
    }


# ════════════════════════════════════════════════════════════
# Computation 8: Nuclear Map × Jacobian Coincidence
# ════════════════════════════════════════════════════════════

def computation_8():
    print("\n" + "=" * 72)
    print("COMPUTATION 8: Nuclear Map × Jacobian Coincidence")
    print("=" * 72)

    p = 5
    fulls = _get_all_240()

    # For each surjection, find which bit positions (if any) are pure-克
    # Pure-克 at bit b: for all x, unsigned distance when flipping bit b is 2
    pure_ke_data = []  # list of (surjection_index, set_of_pure_ke_bits)
    for i, f8 in enumerate(fulls):
        pure_bits = set()
        for b in range(3):
            all_ke = True
            for x in range(8):
                d = (f8[x ^ (1 << b)] - f8[x]) % p
                if min(d, p - d) != 2:
                    all_ke = False
                    break
            if all_ke:
                pure_bits.add(b)
        pure_ke_data.append(pure_bits)

    # Also check for pure-克 in NON-basis directions
    # A direction v ∈ F₂³\{0} is pure-克 if flipping v always gives 克
    pure_ke_directions = []
    for i, f8 in enumerate(fulls):
        dirs = set()
        for v in range(1, 8):  # all nonzero vectors
            all_ke = True
            for x in range(8):
                d = (f8[x ^ v] - f8[x]) % p
                if min(d, p - d) != 2:
                    all_ke = False
                    break
            if all_ke:
                dirs.add(v)
        pure_ke_directions.append(dirs)

    n_with_pure_bit = sum(1 for bits in pure_ke_data if bits)
    n_with_pure_dir = sum(1 for dirs in pure_ke_directions if dirs)

    print(f"\n  Surjections with pure-克 at a standard basis bit: {n_with_pure_bit}/240")
    print(f"  Surjections with pure-克 at any F₂³ direction:   {n_with_pure_dir}/240")

    # Distribution of pure-克 bit positions
    bit_counts = Counter()
    for bits in pure_ke_data:
        for b in bits:
            bit_counts[b] += 1
    print(f"\n  Pure-克 bit position distribution (among those with one):")
    for b in range(3):
        print(f"    Bit {b}: {bit_counts[b]} surjections")

    # Among those with pure-克 basis bit, how many at bit 1?
    at_bit1 = sum(1 for bits in pure_ke_data if 1 in bits)
    print(f"\n  Pure-克 at bit 1 (nuclear-duplicated): {at_bit1}/{n_with_pure_bit}")
    if n_with_pure_bit > 0:
        frac = at_bit1 / n_with_pure_bit
        print(f"  Fraction: {frac:.4f} (chance = 1/3 = {1/3:.4f})")

    # Direction distribution (all 7 nonzero vectors)
    dir_counts = Counter()
    for dirs in pure_ke_directions:
        for v in dirs:
            dir_counts[v] += 1
    print(f"\n  Pure-克 direction distribution (all F₂³ directions):")
    basis = {1: 'e₀', 2: 'e₁', 4: 'e₂'}
    for v in range(1, 8):
        label = basis.get(v, f'{v:03b}')
        is_basis = "← basis" if v in (1, 2, 4) else "  non-basis"
        print(f"    v={v:03b} ({label:>3}): {dir_counts.get(v, 0):>3} surjections  {is_basis}")

    # Check if Stab(111) acts transitively on nonzero vectors
    # (would imply uniform direction distribution)
    orbit_of_e0 = set()
    for perm in _STAB_PERMS:
        orbit_of_e0.add(perm[1])  # image of e₀ = 001
    print(f"\n  Stab(111) orbit of e₀: {sorted(orbit_of_e0)}")
    print(f"  Transitive on F₂³\\{{0}}: {len(orbit_of_e0) == 7}")

    # I Ching detail
    iching_pure = pure_ke_data[fulls.index(tuple(F_MAP))]
    print(f"\n  I Ching pure-克 bits: {iching_pure}")
    print(f"  Nuclear map duplicates: bit 1 (middle line of each trigram)")
    print(f"  Coincidence: pure-克 direction IS the nuclear-duplicated bit = "
          f"{'YES' if 1 in iching_pure else 'NO'}")

    return {
        'n_with_pure_bit': n_with_pure_bit,
        'n_with_pure_dir': n_with_pure_dir,
        'at_bit1': at_bit1,
        'bit_counts': dict(bit_counts),
        'dir_counts': dict(dir_counts),
        'transitive': len(orbit_of_e0) == 7,
    }


# ════════════════════════════════════════════════════════════
# Computation 9: hu_cell Bridge Test
# ════════════════════════════════════════════════════════════

def computation_9():
    print("\n" + "=" * 72)
    print("COMPUTATION 9: hu_cell Bridge Test")
    print("=" * 72)

    f = F_MAP

    # Precompute 克-edge set for 3-cube
    ke_edge_set = set()
    for a in range(8):
        for b in range(a + 1, 8):
            if hamming_adjacent(a, b) and (f[b] - f[a]) % 5 in (2, 3):
                ke_edge_set.add(frozenset({a, b}))

    # For each hexagram: compute hu_cell and surface 克-connectivity
    hex_data = []
    for x in range(N_HEXAGRAMS):
        lower = x & 7
        upper = (x >> 3) & 7
        nuc = hugua(x)
        nuc_l, nuc_u = nuc & 7, (nuc >> 3) & 7
        hu_cell = (f[nuc_l], f[nuc_u])
        ke_connected = frozenset({lower, upper}) in ke_edge_set
        hex_data.append((x, lower, upper, hu_cell, ke_connected))

    # Base rate
    n_ke = sum(1 for _, _, _, _, kc in hex_data if kc)
    base_rate = n_ke / N_HEXAGRAMS
    print(f"\n  Surface trigram 克-connectivity:")
    print(f"    Total 克-connected hexagrams: {n_ke}/{N_HEXAGRAMS} = {base_rate:.4f}")

    # Group by hu_cell
    hu_groups = defaultdict(list)
    for x, l, u, hc, kc in hex_data:
        hu_groups[hc].append(kc)

    print(f"\n  Distinct hu_cells: {len(hu_groups)}")
    print(f"  {'hu_cell':>18} {'size':>5} {'克-connected':>12} {'rate':>8}")
    print("  " + "-" * 50)
    group_rates = {}
    for hc in sorted(hu_groups.keys()):
        members = hu_groups[hc]
        n_kc = sum(members)
        rate = n_kc / len(members) if members else 0
        group_rates[hc] = rate
        elem_str = f"({ELEMENT_NAMES[hc[0]]},{ELEMENT_NAMES[hc[1]]})"
        print(f"  {elem_str:>18} {len(members):>5} {n_kc:>12} {rate:>8.4f}")

    # Observed between-group variance of 克-rate
    group_sizes = [len(hu_groups[hc]) for hc in hu_groups]
    group_ke_counts = [sum(hu_groups[hc]) for hc in hu_groups]
    observed_var = np.var([sum(hu_groups[hc]) / len(hu_groups[hc])
                          for hc in hu_groups], ddof=0)

    # Permutation test: shuffle 克 labels, recompute variance
    rng = np.random.default_rng(42)
    ke_labels = np.array([kc for _, _, _, _, kc in hex_data], dtype=int)
    n_perm = 10000
    n_exceed = 0
    for _ in range(n_perm):
        perm_labels = rng.permutation(ke_labels)
        # Reassign to groups (same group structure, shuffled labels)
        idx = 0
        perm_rates = []
        for hc in sorted(hu_groups.keys()):
            sz = len(hu_groups[hc])
            grp = perm_labels[idx:idx + sz]
            perm_rates.append(grp.mean())
            idx += sz
        perm_var = np.var(perm_rates, ddof=0)
        if perm_var >= observed_var:
            n_exceed += 1

    p_value = (n_exceed + 1) / (n_perm + 1)
    print(f"\n  Permutation test (10K iterations):")
    print(f"    Observed between-group variance of 克-rate: {observed_var:.6f}")
    print(f"    p-value: {p_value:.4f}")
    print(f"    Significant (p < 0.05): {'YES' if p_value < 0.05 else 'NO'}")

    return {
        'n_ke': n_ke,
        'base_rate': base_rate,
        'group_rates': group_rates,
        'p_value': p_value,
    }


# ════════════════════════════════════════════════════════════
# Computation 10: (4,13) Cube-Edge Geometry
# ════════════════════════════════════════════════════════════

def computation_10():
    print("\n" + "=" * 72)
    print("COMPUTATION 10: (4,13) Cube-Edge Geometry")
    print("=" * 72)

    n, p = 4, 13
    N = 1 << n

    # Construct Shape A surjection analytically
    pairs4 = get_complement_pairs(n)
    rep_vals = (0, 1, 1, 2, 3, 4, 5, 6)
    f4 = expand_rep_vals(rep_vals, pairs4, p, N)

    print(f"\n  Surjection f: F₂⁴ → Z₁₃ (Shape A, doubled class {{1,12}})")
    print(f"    rep_vals = {rep_vals}")
    print(f"    f = {f4}")
    fp = fiber_partition(f4, p)
    print(f"    Fiber partition: {fp}")

    # 4-cube: 16 vertices, 32 edges
    # Partition edges by unsigned Z₁₃ distance
    dist_edges = defaultdict(list)  # unsigned_dist → list of (x,y) edges
    for x in range(N):
        for y in range(x + 1, N):
            if not hamming_adjacent(x, y):
                continue
            d = (f4[y] - f4[x]) % p
            d_unsigned = min(d, p - d)
            dist_edges[d_unsigned].append((x, y))

    print(f"\n  4-cube edge partition by Z₁₃ unsigned distance:")
    total_edges = sum(len(v) for v in dist_edges.values())
    print(f"    Total edges: {total_edges} (expect 32)")
    for d in sorted(dist_edges.keys()):
        label = {0: '比和', 1: '生', 2: '克'}.get(d, f'd={d}')
        print(f"    d={d} ({label:>4}): {len(dist_edges[d])} edges")

    # Focus on 克 (d=2) subgraph
    A_ke = np.zeros((N, N))
    for x, y in dist_edges.get(2, []):
        A_ke[x, y] = A_ke[y, x] = 1

    n_ke_edges = len(dist_edges.get(2, []))
    print(f"\n  克 subgraph: {n_ke_edges} edges on {N} vertices")

    if n_ke_edges > 0:
        ke_struct = classify_graph(A_ke, N)
        print(f"    Structure: {ke_struct}")

        eigs_ke = sorted_eigs(A_ke)
        print(f"    Eigenvalues: {np.round(eigs_ke, 6)}")

        phi_ke = detect_phi(eigs_ke)
        print(f"    φ detected: {'YES — ' + str(phi_ke) if phi_ke else 'NO'}")
        print(f"    x²−x−1 divides charpoly: {charpoly_has_x2_minus_x_minus_1(eigs_ke)}")
    else:
        ke_struct = "empty"
        phi_ke = {}
        print(f"    No 克 edges!")

    # Also check 生 (d=1) subgraph
    A_sh = np.zeros((N, N))
    for x, y in dist_edges.get(1, []):
        A_sh[x, y] = A_sh[y, x] = 1
    n_sh_edges = len(dist_edges.get(1, []))
    if n_sh_edges > 0:
        sh_struct = classify_graph(A_sh, N)
        eigs_sh = sorted_eigs(A_sh)
        phi_sh = detect_phi(eigs_sh)
        print(f"\n  生 subgraph: {n_sh_edges} edges, structure: {sh_struct}")
        print(f"    Eigenvalues: {np.round(eigs_sh, 6)}")
        print(f"    φ detected: {'YES' if phi_sh else 'NO'}")

    # Path analysis: what path lengths appear in 克 components?
    if n_ke_edges > 0:
        print(f"\n  Path decomposition of 克 subgraph:")
        # Extract P_n components and report n+1 (the eigenvalue denominator)
        vis = [False] * N
        for s in range(N):
            if vis[s] or sum(A_ke[s]) == 0:
                vis[s] = True
                continue
            q = [s]; vis[s] = True; vs = []
            while q:
                v = q.pop(0); vs.append(v)
                for u in range(N):
                    if A_ke[v, u] > 0 and not vis[u]:
                        vis[u] = True; q.append(u)
            nv = len(vs)
            degs = [int(sum(A_ke[v, u] for u in vs)) for v in vs]
            ne = sum(degs) // 2
            if ne == nv - 1 and max(degs) <= 2:
                denom = nv + 1
                print(f"    P{nv}: eigenvalue denominator = {denom}, "
                      f"2cos(π/{denom}) = {2*np.cos(np.pi/denom):.6f}")
            else:
                print(f"    Component: {nv} vertices, {ne} edges (not a path)")

    return {
        'ke_struct': ke_struct,
        'phi_ke': bool(phi_ke),
        'n_ke_edges': n_ke_edges,
        'dist_edges': {d: len(v) for d, v in dist_edges.items()},
    }


# ════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════

def summary(r1, r2, r3, r4, r5, r6=None, r7=None, r8=None, r9=None, r10=None):
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)

    # Iteration 7 results
    phi_2a = r1['phi_sheng'] or r1['phi_ke']
    phi_2b = r2['phi_sheng'] or r2['phi_ke'] or r2['phi_bihe']

    print(f"  Thread 2A (pullback):       φ detected = {'YES' if phi_2a else 'NO'}")
    print(f"    生-pullback eigs: {np.round(r1['sheng_8'], 4)}")
    print(f"    克-pullback eigs: {np.round(r1['ke_8'], 4)}")

    print(f"\n  Thread 2B (cube-partition):  φ detected = {'YES' if phi_2b else 'NO'}")
    print(f"    A_生 eigs: {np.round(r2['eigs_sheng'], 4)}")
    print(f"    A_克 eigs: {np.round(r2['eigs_ke'], 4)}")
    print(f"    A_比和 eigs: {np.round(r2['eigs_bihe'], 4)}")

    print(f"\n  Thread 5 (E=1 family):      Fibonacci ratio unique to (3,5) = NO")
    print(f"\n  Thread 3 (transitions):     生:克 = {r4['生']}:{r4['克']} = 2:3")

    trivial = (r5['basin_sizes'] == sorted([32, 16, 16], reverse=True)
               and r5['depth_dist'] == {0: 4, 1: 12, 2: 48})
    print(f"\n  Thread 4 (basins):          trivial = {'YES' if trivial else 'NO'}")

    # Iteration 8 results
    if r6 is not None:
        print(f"\n{'='*72}")
        print("ITERATION 8 SUMMARY")
        print(f"{'='*72}")

        print(f"  Comp 6 (orbit taxonomy):  φ in 克: {r6['total_phi_ke']}/240  |  "
              f"φ in 生: {r6['total_phi_sh']}/240  |  "
              f"neither: {r6['total_neither']}/240")
        print(f"    Orbit sizes: {r6['orbit_sizes']}")

        if r7:
            jt_str = fmt_jac(list(r7['p4_types'].keys())[0]) if len(r7['p4_types']) == 1 else 'VARIES'
            print(f"  Comp 7 (Jacobian types):  {r7['n_types']} distinct types  |  "
                  f"克=P₄ surjections type: {jt_str}")
            print(f"    I Ching type: {fmt_jac(r7['iching_jt'])}")

        if r8:
            n_pb = r8['n_with_pure_bit']
            at1 = r8['at_bit1']
            trans = r8['transitive']
            print(f"  Comp 8 (nuclear coincidence): pure-克 at any basis bit: {n_pb}/240  |  "
                  f"at bit 1: {at1}/{n_pb}")
            print(f"    Stab(111) transitive on F₂³\\{{0}}: {trans}")
            if trans:
                print(f"    → direction distribution uniform by symmetry → P(bit 1) = 1/3 exactly")

        if r9:
            print(f"  Comp 9 (hu_cell bridge):  base 克-rate: {r9['base_rate']:.4f}  |  "
                  f"permutation p-value: {r9['p_value']:.4f}")

        if r10:
            print(f"  Comp 10 ((4,13) geometry): 克 edges: {r10['n_ke_edges']}  |  "
                  f"structure: {r10['ke_struct']}  |  φ: {'YES' if r10['phi_ke'] else 'NO'}")


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════

if __name__ == '__main__':
    r1 = computation_1()
    r2 = computation_2()
    r3 = computation_3()
    r4 = computation_4()
    r5 = computation_5()
    r6 = computation_6()
    r7 = computation_7()
    r8 = computation_8()
    r9 = computation_9()
    r10 = computation_10()
    summary(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10)
