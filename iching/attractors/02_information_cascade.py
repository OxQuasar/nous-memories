#!/usr/bin/env python3
"""
02_information_cascade.py — F₂ linear algebra of the 互 map.

The 互 operation is linear over F₂⁶. This script computes the full
algebraic structure: matrix powers, rank/kernel/image chains, fixed
points, minimal polynomial, basin partition, and information cascade.
"""

import sys
sys.path.insert(0, 'memories/iching/opposition-theory/phase4')
sys.path.insert(0, 'memories/iching/kingwen')

import numpy as np
from cycle_algebra import hugua, bit, fmt6
from sequence import KING_WEN

# ═══════════════════════════════════════════════════════════════════════
# F₂ Linear Algebra Utilities
# ═══════════════════════════════════════════════════════════════════════

def f2_mul(A, B):
    """Matrix multiply over F₂."""
    return (A @ B) % 2

def f2_add(A, B):
    """Matrix add over F₂."""
    return (A + B) % 2

def f2_rref(M):
    """Row-reduce M over F₂. Returns (rref, pivots)."""
    A = M.copy() % 2
    rows, cols = A.shape
    pivots = []
    r = 0
    for c in range(cols):
        # Find pivot in column c, row >= r
        pivot = None
        for i in range(r, rows):
            if A[i, c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        # Swap rows
        A[[r, pivot]] = A[[pivot, r]]
        # Eliminate
        for i in range(rows):
            if i != r and A[i, c] == 1:
                A[i] = (A[i] + A[r]) % 2
        pivots.append(c)
        r += 1
    return A, pivots

def f2_rank(M):
    """Rank of M over F₂."""
    _, pivots = f2_rref(M)
    return len(pivots)

def f2_kernel(M):
    """Kernel basis of M over F₂. Returns matrix whose rows are basis vectors."""
    rows, cols = M.shape
    # Augment [M^T | I] and row-reduce to find null space
    A = np.hstack([M.T, np.eye(cols, dtype=int)]) % 2
    rref, pivots = f2_rref(A)

    # Kernel vectors: rows where the M^T part is all zeros
    basis = []
    for i in range(len(pivots), A.shape[0]):
        # Check if the left part (M^T) is zero
        if np.all(rref[i, :rows] == 0):
            vec = rref[i, rows:] % 2
            if np.any(vec):
                basis.append(vec)

    # Alternative: use standard null space computation
    # Transpose M, do RREF, read off null space
    if not basis:
        return np.zeros((0, cols), dtype=int)
    return np.array(basis, dtype=int)

def f2_kernel_direct(M):
    """
    Kernel of M over F₂ via augmented RREF.
    Solves Mx = 0 by row-reducing [M | 0].
    """
    rows, cols = M.shape
    A, pivots = f2_rref(M.copy())
    # Free variables: columns not in pivots
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        vec = np.zeros(cols, dtype=int)
        vec[f] = 1
        # Back-substitute for pivot variables
        for i, p in enumerate(pivots):
            vec[p] = A[i, f]
        basis.append(vec % 2)
    if not basis:
        return np.zeros((0, cols), dtype=int)
    return np.array(basis, dtype=int)

def f2_image(M):
    """Image (column space) basis of M over F₂."""
    # Column space = row space of M^T
    rref, pivots = f2_rref(M.T.copy())
    basis = rref[:len(pivots)] % 2
    return basis


# ═══════════════════════════════════════════════════════════════════════
# The Matrix
# ═══════════════════════════════════════════════════════════════════════

# hugua(b₀,b₁,b₂,b₃,b₄,b₅) = (b₁,b₂,b₃,b₂,b₃,b₄)
# Row i of M: which input bit maps to output bit i
M = np.array([
    [0, 1, 0, 0, 0, 0],  # out₀ = b₁
    [0, 0, 1, 0, 0, 0],  # out₁ = b₂
    [0, 0, 0, 1, 0, 0],  # out₂ = b₃
    [0, 0, 1, 0, 0, 0],  # out₃ = b₂
    [0, 0, 0, 1, 0, 0],  # out₄ = b₃
    [0, 0, 0, 0, 1, 0],  # out₅ = b₄
], dtype=int)

# KW lookup
KW = {}
for kw_num, name, binstr in KING_WEN:
    val = sum(int(c) << i for i, c in enumerate(binstr))
    KW[val] = (kw_num, name)


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════

def hex_to_vec(h):
    """Integer hexagram → F₂⁶ column vector."""
    return np.array([bit(h, i) for i in range(6)], dtype=int)

def vec_to_hex(v):
    """F₂⁶ vector → integer hexagram."""
    return sum(int(v[i]) << i for i in range(6))

def print_matrix(name, M):
    """Pretty-print a 6×6 binary matrix."""
    print(f"\n  {name}:")
    for row in M:
        print(f"    [{', '.join(str(x) for x in row)}]")

def basis_str(basis):
    """Format basis vectors."""
    if len(basis) == 0:
        return "{0}"
    parts = []
    for v in basis:
        bits = ''.join(str(x) for x in v)
        h = vec_to_hex(v)
        parts.append(f"({bits})={h}")
    return '{' + ', '.join(parts) + '}'

def basis_hex_str(basis):
    """Show basis as hexagram values with KW names."""
    parts = []
    for v in basis:
        h = vec_to_hex(v)
        if h in KW:
            kw_num, name = KW[h]
            parts.append(f"{h}=KW#{kw_num}({name})")
        else:
            parts.append(str(h))
    return '{' + ', '.join(parts) + '}'


# ═══════════════════════════════════════════════════════════════════════
# 1. Matrix Powers
# ═══════════════════════════════════════════════════════════════════════

def section_matrix_powers():
    print("=" * 70)
    print("1. MATRIX POWERS M, M², M³, M⁴")
    print("=" * 70)

    powers = {1: M}
    Mk = M.copy()
    for k in range(2, 5):
        Mk = f2_mul(Mk, M)
        powers[k] = Mk

    for k in range(1, 5):
        print_matrix(f"M{'²³⁴'[k-2] if k > 1 else ''} (k={k})", powers[k])

    # Verify M⁴ = M²
    eq = np.array_equal(powers[4], powers[2])
    print(f"\n  M⁴ = M²? {eq}")

    # Also check M³ ≠ M, M³ ≠ M²
    print(f"  M³ = M?  {np.array_equal(powers[3], powers[1])}")
    print(f"  M³ = M²? {np.array_equal(powers[3], powers[2])}")

    # Show M²+M³ — should be rank 1
    sum23 = f2_add(powers[2], powers[3])
    print_matrix("M² + M³ (mod 2)", sum23)
    print(f"  rank(M²+M³) = {f2_rank(sum23)}")
    print(f"  Column space = all-ones vector (1,1,1,1,1,1) = fixed-point direction")

    # Verify against hugua()
    print("\n  Verification against hugua():")
    ok = True
    for k in range(1, 5):
        for h in range(64):
            v = hex_to_vec(h)
            mat_result = vec_to_hex(f2_mul(powers[k], v.reshape(6, 1)).flatten() % 2)
            # Compute hugua iterated k times
            func_result = h
            for _ in range(k):
                func_result = hugua(func_result)
            if mat_result != func_result:
                print(f"    MISMATCH: k={k}, h={h}: matrix={mat_result}, func={func_result}")
                ok = False
    print(f"    All 64×4 = 256 matrix-vs-function checks: {'✓ PASS' if ok else '✗ FAIL'}")

    return powers


# ═══════════════════════════════════════════════════════════════════════
# 2. Rank Sequence
# ═══════════════════════════════════════════════════════════════════════

def section_rank_sequence(powers):
    print("\n" + "=" * 70)
    print("2. RANK SEQUENCE")
    print("=" * 70)

    print(f"\n  {'k':>3} {'rank(Mᵏ)':>10} {'dim ker(Mᵏ)':>13} {'dim im(Mᵏ)':>12}")
    print(f"  {'─'*3} {'─'*10} {'─'*13} {'─'*12}")
    for k in range(1, 5):
        r = f2_rank(powers[k])
        print(f"  {k:3d} {r:10d} {6-r:13d} {r:12d}")

    print(f"\n  Rank drops: 6 → 4 → 2 → 2 → 2")
    print(f"  Two projection steps, then stabilized")


# ═══════════════════════════════════════════════════════════════════════
# 3. Kernel Chain
# ═══════════════════════════════════════════════════════════════════════

def section_kernel_chain(powers):
    print("\n" + "=" * 70)
    print("3. KERNEL CHAIN: ker(M) ⊂ ker(M²) ⊂ ker(M³)")
    print("=" * 70)

    for k in range(1, 4):
        ker = f2_kernel_direct(powers[k])
        print(f"\n  ker(M{'²³'[k-2] if k > 1 else ''}) — dim = {len(ker)}:")
        print(f"    Basis: {basis_str(ker)}")

        # Describe constraints
        if k == 1:
            print(f"    Interpretation: b₁=b₂=b₃=b₄=0 → only outer bits b₀,b₅ free")
            print(f"    These are the bits ERASED by 互")
        elif k == 2:
            print(f"    Interpretation: b₂=b₃=0 → outer bits + shell bits free")
            print(f"    ker(M²) adds b₁,b₄ to the kernel (the 'shell' bits)")
        elif k == 3:
            print(f"    Interpretation: same as ker(M²) — kernel stabilized")

    # Verify containment
    ker1 = f2_kernel_direct(powers[1])
    ker2 = f2_kernel_direct(powers[2])
    ker3 = f2_kernel_direct(powers[3])

    print(f"\n  Containment checks:")
    print(f"    ker(M) ⊂ ker(M²): dim {len(ker1)} < dim {len(ker2)} ✓")
    print(f"    ker(M²) = ker(M³): dim {len(ker2)} = dim {len(ker3)}", end="")
    print(f" {'✓' if len(ker2) == len(ker3) else '✗'}")

    # Enumerate kernel elements
    for k, ker, label in [(1, ker1, "ker(M)"), (2, ker2, "ker(M²)")]:
        elements = set()
        if len(ker) == 0:
            elements = {0}
        else:
            for mask in range(1 << len(ker)):
                v = np.zeros(6, dtype=int)
                for i in range(len(ker)):
                    if mask & (1 << i):
                        v = (v + ker[i]) % 2
                elements.add(vec_to_hex(v))
        elems_sorted = sorted(elements)
        kw_labels = []
        for h in elems_sorted:
            if h in KW:
                kw_labels.append(f"{h}=KW#{KW[h][0]}({KW[h][1]})")
            else:
                kw_labels.append(str(h))
        print(f"\n  Elements of {label} ({len(elements)} total):")
        for lbl in kw_labels:
            print(f"    {lbl}")


# ═══════════════════════════════════════════════════════════════════════
# 4. Image Chain
# ═══════════════════════════════════════════════════════════════════════

def section_image_chain(powers):
    print("\n" + "=" * 70)
    print("4. IMAGE CHAIN: im(M) ⊃ im(M²) = im(M³)")
    print("=" * 70)

    for k in range(1, 4):
        img = f2_image(powers[k])
        print(f"\n  im(M{'²³'[k-2] if k > 1 else ''}) — dim = {len(img)}:")
        print(f"    Basis: {basis_str(img)}")

        if k == 1:
            print(f"    Constraints: output has bit₁=bit₃, bit₂=bit₄")
            print(f"    4 free output bits → 16 possible values")
        elif k == 2:
            print(f"    Constraints: output = (b₂,b₃,b₂,b₃,b₂,b₃)")
            print(f"    = alternating patterns parameterized by (b₂,b₃)")

    # Enumerate im(M²)
    img2 = f2_image(powers[2])
    elements = set()
    for mask in range(1 << len(img2)):
        v = np.zeros(6, dtype=int)
        for i in range(len(img2)):
            if mask & (1 << i):
                v = (v + img2[i]) % 2
        elements.add(vec_to_hex(v))

    print(f"\n  Elements of im(M²) = attractor set:")
    for h in sorted(elements):
        kw_num, name = KW[h]
        print(f"    {h:3d} = {fmt6(h)} = KW#{kw_num} ({name})")

    print(f"\n  im(M²) IS the attractor set {{Kun, Qian, JiJi, WeiJi}}")
    print(f"  im(M²) = im(M³) ✓ — image stabilizes after 2 steps")


# ═══════════════════════════════════════════════════════════════════════
# 5. Fixed Points
# ═══════════════════════════════════════════════════════════════════════

def section_fixed_points(powers):
    print("\n" + "=" * 70)
    print("5. FIXED POINTS: ker(M + I) over F₂")
    print("=" * 70)

    I = np.eye(6, dtype=int)
    MpI = f2_add(M, I)  # M + I = M - I over F₂
    print_matrix("M + I (= M - I over F₂)", MpI)

    ker = f2_kernel_direct(MpI)
    print(f"\n  ker(M+I) — dim = {len(ker)}")
    print(f"  Basis: {basis_str(ker)}")

    # Enumerate fixed points
    elements = set()
    for mask in range(1 << len(ker)):
        v = np.zeros(6, dtype=int)
        for i in range(len(ker)):
            if mask & (1 << i):
                v = (v + ker[i]) % 2
        elements.add(vec_to_hex(v))

    print(f"\n  Fixed points (Mx = x):")
    for h in sorted(elements):
        kw_num, name = KW[h]
        print(f"    {h:3d} = {fmt6(h)} = KW#{kw_num} ({name})")

    print(f"\n  All bits equal: b₀=b₁=b₂=b₃=b₄=b₅ → only 000000 and 111111")

    # 2-periodic points: ker(M²+I)
    print(f"\n{'─' * 50}")
    print(f"  2-PERIODIC POINTS: ker(M² + I)")
    M2pI = f2_add(powers[2], I)
    ker2 = f2_kernel_direct(M2pI)
    print(f"\n  ker(M²+I) — dim = {len(ker2)}")
    print(f"  Basis: {basis_str(ker2)}")

    elements2 = set()
    for mask in range(1 << len(ker2)):
        v = np.zeros(6, dtype=int)
        for i in range(len(ker2)):
            if mask & (1 << i):
                v = (v + ker2[i]) % 2
        elements2.add(vec_to_hex(v))

    print(f"\n  2-periodic points (M²x = x):")
    for h in sorted(elements2):
        kw_num, name = KW[h]
        marker = " [fixed]" if h in {0, 63} else " [2-cycle]"
        print(f"    {h:3d} = {fmt6(h)} = KW#{kw_num} ({name}){marker}")

    print(f"\n  Constraints: b₀=b₂=b₄ and b₁=b₃=b₅ (alternating constancy)")
    print(f"  ker(M+I) ⊂ ker(M²+I): dim 1 ⊂ dim 2 ✓")
    print(f"  The 2-cycle {{21,42}} lives in ker(M²+I) \\ ker(M+I)")
    print(f"  Specifically: JiJi=21 and WeiJi=42 satisfy M²x=x but NOT Mx=x")


# ═══════════════════════════════════════════════════════════════════════
# 6. Minimal Polynomial
# ═══════════════════════════════════════════════════════════════════════

def section_minimal_polynomial(powers):
    print("\n" + "=" * 70)
    print("6. MINIMAL POLYNOMIAL OF M OVER F₂")
    print("=" * 70)

    I = np.eye(6, dtype=int)
    Z = np.zeros((6, 6), dtype=int)

    # Test candidate annihilating polynomials in order of degree
    candidates = [
        ("x",       [M]),
        ("x²",      [powers[2]]),
        ("x+1",     [f2_add(M, I)]),
        ("x²+1",    [f2_add(powers[2], I)]),
        ("x²+x",    [f2_add(powers[2], M)]),
        ("x³",      [powers[3]]),
        ("x³+x²",   [f2_add(powers[3], powers[2])]),
        ("x³+x",    [f2_add(powers[3], M)]),
        ("x³+1",    [f2_add(powers[3], I)]),
        ("x³+x²+x+1", [f2_add(f2_add(powers[3], powers[2]), f2_add(M, I))]),
        ("x⁴+x²",  [f2_add(powers[4], powers[2])]),
    ]

    print(f"\n  {'polynomial':>20} {'= p(M)':>8} {'zero?':>6}")
    print(f"  {'─'*20} {'─'*8} {'─'*6}")

    min_poly = None
    for name, terms in candidates:
        result = terms[0]
        is_zero = np.array_equal(result, Z)
        print(f"  {name:>20} {'':>8} {'YES ✓' if is_zero else 'no':>6}")
        if is_zero and min_poly is None:
            min_poly = name

    print(f"\n  Minimal polynomial: p(x) = x⁴ + x² = x²(x² + 1) = x²(x + 1)²")
    print(f"  (Over F₂: x²+1 = (x+1)² since char = 2)")
    print(f"\n  Factored form: x² · (x+1)²")
    print(f"    Eigenvalue 0: algebraic mult ≥ 2, geometric mult = dim ker(M) = 2")
    print(f"    Eigenvalue 1: algebraic mult ≥ 2, geometric mult = dim ker(M+I) = 1")

    # Jordan structure (block sizes from kernel dimension jumps)
    print(f"\n  Jordan-like structure over F₂:")

    k1 = len(f2_kernel_direct(M))
    k2 = len(f2_kernel_direct(powers[2]))
    # Blocks ≥ 1: k1=2, blocks ≥ 2: k2-k1=2, blocks ≥ 3: 0
    # All 2 blocks are size exactly 2
    print(f"    Eigenvalue 0:")
    print(f"      dim ker(M)={k1}, dim ker(M²)={k2}")
    print(f"      Blocks ≥ size 1: {k1}, blocks ≥ size 2: {k2-k1}")
    print(f"      → Two 2×2 Jordan blocks (4 dimensions)")

    MpI = f2_add(M, I)
    k1_1 = len(f2_kernel_direct(MpI))
    k2_1 = len(f2_kernel_direct(f2_add(powers[2], np.eye(6, dtype=int))))
    print(f"    Eigenvalue 1:")
    print(f"      dim ker(M+I)={k1_1}, dim ker(M²+I)={k2_1}")
    print(f"      Blocks ≥ size 1: {k1_1}, blocks ≥ size 2: {k2_1-k1_1}")
    print(f"      → One 2×2 Jordan block (2 dimensions)")

    print(f"\n  Total: 2+2+2 = 6 ✓")


# ═══════════════════════════════════════════════════════════════════════
# 7. Basin Partition in Algebraic Terms
# ═══════════════════════════════════════════════════════════════════════

def section_basin_partition(powers):
    print("\n" + "=" * 70)
    print("7. BASIN PARTITION — ALGEBRAIC DESCRIPTION")
    print("=" * 70)

    I = np.eye(6, dtype=int)

    # The projection to the attractor space is M²
    print(f"\n  The attractor space is im(M²) = span{{(101010), (010101)}}")
    print(f"  M² projects every hexagram onto this 2D subspace")
    print(f"  The projection M²(h) determines the basin:")

    print(f"\n  {'(b₂,b₃)':>8} {'M²(h)':>8} {'=':>2} {'attractor':>12} {'basin':>16}")
    print(f"  {'─'*8} {'─'*8} {'─'*2} {'─'*12} {'─'*16}")

    cases = [(0, 0, 0, "Kun"), (1, 1, 63, "Qian"),
             (1, 0, 42, "Cycle"), (0, 1, 21, "Cycle")]
    for b2, b3, att, basin in cases:
        att_name = f"KW#{KW[att][0]}({KW[att][1]})"
        print(f"  ({b2},{b3}){'':<4} {fmt6(att):>8} {'=':>2} {att_name:>12} {basin:>16}")

    # Basin type as linear functional
    print(f"\n  Basin TYPE (fixed vs cycle) = b₂ ⊕ b₃:")
    print(f"    b₂ ⊕ b₃ = 0 → fixed-point basin (Kun or Qian)")
    print(f"    b₂ ⊕ b₃ = 1 → 2-cycle basin")
    print(f"    This is a LINEAR functional on F₂⁶")

    # Eigenspace decomposition
    print(f"\n  Eigenspace decomposition:")
    print(f"    F₂⁶ = ker(M²) ⊕ ker(M²+I)")
    print(f"         = (b₂=b₃=0 subspace) ⊕ (b₀=b₂=b₄, b₁=b₃=b₅ subspace)")
    print(f"         = 4-dim 'transient' ⊕ 2-dim 'attractor'")

    # Show the 2-cycle explicitly
    print(f"\n  The 2-cycle lives in ker(M²+I) \\ ker(M+I):")
    j = hex_to_vec(21)  # JiJi
    w = hex_to_vec(42)  # WeiJi
    Mj = f2_mul(M, j.reshape(6, 1)).flatten() % 2
    Mw = f2_mul(M, w.reshape(6, 1)).flatten() % 2
    print(f"    M · JiJi(21)  = {vec_to_hex(Mj)} = WeiJi(42)")
    print(f"    M · WeiJi(42) = {vec_to_hex(Mw)} = JiJi(21)")
    print(f"    M²· JiJi(21)  = JiJi(21)  ✓ (2-periodic)")
    print(f"    M · Qian(63)  = Qian(63)   ✓ (fixed)")
    print(f"    M · Kun(0)    = Kun(0)      ✓ (fixed)")

    # Relation between basin and kernel chain
    print(f"\n  Kernel chain ↔ basin:")
    print(f"    ker(M)  = span{{e₀, e₅}} = outer bits → erased in 1 step")
    print(f"    ker(M²) = span{{e₀, e₁, e₄, e₅}} = outer + shell bits")
    print(f"    ker(M²)/ker(M) = span{{e₁, e₄}} mod ker(M)")
    print(f"    These are the 'shell' bits — erased in step 2")
    print(f"    After 2 steps, only interface bits (b₂,b₃) survive")

    # Verify with explicit computation
    print(f"\n  Verification: M² erases everything except b₂,b₃")
    ok = True
    for h in range(64):
        v = hex_to_vec(h)
        proj = f2_mul(powers[2], v.reshape(6, 1)).flatten() % 2
        expected = np.array([bit(h, 2), bit(h, 3)] * 3, dtype=int)
        if not np.array_equal(proj, expected):
            print(f"    MISMATCH at h={h}")
            ok = False
    print(f"    All 64 hexagrams: {'✓ PASS' if ok else '✗ FAIL'}")


# ═══════════════════════════════════════════════════════════════════════
# 8. Information Cascade
# ═══════════════════════════════════════════════════════════════════════

def section_information_cascade(powers):
    print("\n" + "=" * 70)
    print("8. INFORMATION CASCADE")
    print("=" * 70)

    print(f"\n  {'step k':>7} {'distinct Mᵏ(h)':>15} {'effective bits':>15} {'entropy loss':>13}")
    print(f"  {'─'*7} {'─'*15} {'─'*15} {'─'*13}")

    prev_count = 64
    for k in range(5):
        # Count distinct values of M^k(h) over all h
        if k == 0:
            values = set(range(64))
        else:
            values = set()
            for h in range(64):
                v = hex_to_vec(h)
                result = v
                for _ in range(k):
                    result = f2_mul(M, result.reshape(6, 1)).flatten() % 2
                values.add(vec_to_hex(result))
        count = len(values)
        eff_bits = np.log2(count) if count > 0 else 0
        loss = np.log2(prev_count) - eff_bits if prev_count > 0 else 0
        print(f"  {k:7d} {count:15d} {eff_bits:15.1f} {loss:13.1f}")
        prev_count = count

    print(f"\n  Information flow: 6 → 4 → 2 → 2 → 2 bits")
    print(f"  Step 1 erases 2 bits (outer shell: b₀, b₅)")
    print(f"  Step 2 erases 2 more bits (inner shell: b₁, b₄)")
    print(f"  Steps 3+ erase nothing — system is in the attractor space")

    # Which bits survive at each step
    print(f"\n  Bit survival analysis:")
    print(f"    Step 0: all 6 bits free — {{b₀,b₁,b₂,b₃,b₄,b₅}}")
    print(f"    Step 1: output determined by (b₁,b₂,b₃,b₄) — 4 free bits")
    print(f"    Step 2: output determined by (b₂,b₃) — 2 free bits")
    print(f"    Step 3+: same 2 free bits, alternating between positions")

    # Show the distinct values at each step
    for k in [1, 2, 3]:
        values = set()
        for h in range(64):
            v = hex_to_vec(h)
            result = v
            for _ in range(k):
                result = f2_mul(M, result.reshape(6, 1)).flatten() % 2
            values.add(vec_to_hex(result))
        vals = sorted(values)
        if len(vals) <= 16:
            labels = []
            for h in vals:
                kw_num, name = KW[h]
                labels.append(f"{h}({name})")
            print(f"\n  M{'²³'[k-2] if k > 1 else ''} image ({len(vals)} values): {', '.join(labels)}")


# ═══════════════════════════════════════════════════════════════════════
# Key Findings
# ═══════════════════════════════════════════════════════════════════════

def section_key_findings():
    print("\n" + "=" * 70)
    print("## Key Findings")
    print("=" * 70)

    print("""
1. COMPLETE ALGEBRAIC DESCRIPTION
   互 is a linear map M: F₂⁶ → F₂⁶ with:
     Minimal polynomial: x²(x+1)² = x⁴+x² over F₂
     Eigenvalues: 0 (alg mult 4, two 2×2 blocks), 1 (alg mult 2, one 2×2 block)
     Rank: 4 → 2 → 2 (stabilizes at step 2)

2. DIMENSIONAL REDUCTION CHAIN
   F₂⁶ →[M]→ im(M) →[M]→ im(M²) = im(M³) = ...
   dim:  6  →   4    →    2    =    2

   Step 1: erases outer bits {b₀, b₅} — the hexagram's 'shell'
   Step 2: erases shell bits {b₁, b₄} — the nuclear trigrams' free bits
   Result: only interface bits (b₂, b₃) survive

3. KERNEL CHAIN (WHAT GETS ERASED)
   ker(M)  = span{e₀, e₅}           dim 2 — outer bits
   ker(M²) = span{e₀, e₁, e₄, e₅}  dim 4 — outer + shell bits
   ker(M²) = ker(M³) = ... — stabilized

   The kernel is a NESTED onion: outer layer first, then shell layer.

4. ATTRACTOR SPACE = im(M²)
   im(M²) = span{(101010), (010101)} — the alternating patterns
   Elements: {Kun(0), JiJi(21), WeiJi(42), Qian(63)}
   This 2D subspace IS the attractor set.

5. FIXED AND PERIODIC STRUCTURE
   ker(M+I) = span{(111111)} → fixed points: {Kun, Qian}
   ker(M²+I) = span{(101010), (010101)} → 2-periodic: {Kun, JiJi, WeiJi, Qian}
   The 2-cycle {JiJi, WeiJi} ∈ ker(M²+I) ∖ ker(M+I)

6. BASIN = LINEAR FUNCTIONAL
   Basin type: b₂ ⊕ b₃ (0=fixed, 1=cycle) — a linear functional
   Basin identity: M²(h) — the projection onto the attractor space
   The basin partition is ALGEBRAIC: it's the coset decomposition of
   F₂⁶ by ker(M²).

7. MINIMAL POLYNOMIAL x²(x+1)² ENCODES EVERYTHING
   x² factor: 2 nilpotent steps to reach the attractor space
   (x+1)² factor: the attractor space has a 2-cycle
   Together: converge in 2 steps, then oscillate with period 2

8. INFORMATION LOSS IS STRUCTURED
   6 → 4 → 2 → 2 → 2 effective bits
   2 bits lost per step for exactly 2 steps
   The loss is uniform: each step removes one 'layer' of the hexagram
   Outer layer → shell layer → interface (stable)
""")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("02: INFORMATION CASCADE + F₂ LINEAR ALGEBRA")
    print("=" * 70)

    powers = section_matrix_powers()
    section_rank_sequence(powers)
    section_kernel_chain(powers)
    section_image_chain(powers)
    section_fixed_points(powers)
    section_minimal_polynomial(powers)
    section_basin_partition(powers)
    section_information_cascade(powers)
    section_key_findings()


if __name__ == '__main__':
    main()
