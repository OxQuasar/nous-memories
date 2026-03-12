#!/usr/bin/env python3
"""
cc_identity.py — Phase 3, Iteration 13: The Algebraic Identity

Task 1: Coherent Closure from Z₅ difference
Task 2: Difference Table + Walsh-Hadamard Spectrum
Task 3: Automorphism Orbits
Task 4a: Can the CC predict 互 dynamics?

Uses eigenstructure.py encoding convention:
  WUXING = {0:2, 1:0, 2:4, 3:3, 4:2, 5:1, 6:0, 7:3}
  Z₅: 0=Wood, 1=Fire, 2=Earth, 3=Metal, 4=Water
"""

import cmath
import math
from collections import defaultdict
from itertools import product as iterproduct

# ═══════════════════════════════════════════════════════════════
# Encoding (matching eigenstructure.py)
# ═══════════════════════════════════════════════════════════════

WUXING = {0: 2, 1: 0, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0, 7: 3}
ELEM = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}
TRIG_ZH = {0: '坤', 1: '震', 2: '坎', 3: '兌', 4: '艮', 5: '離', 6: '巽', 7: '乾'}
TRIG_EN = {0: 'Kun', 1: 'Zhen', 2: 'Kan', 3: 'Dui', 4: 'Gen', 5: 'Li', 6: 'Xun', 7: 'Qian'}

def f(x):
    """五行 map: F₂³ → Z₅"""
    return WUXING[x]

def fmt3(x):
    return format(x, '03b')

def trig_label(x):
    return f"{TRIG_ZH[x]}({fmt3(x)})"

def hamming(x, y):
    return bin(x ^ y).count('1')

# ═══════════════════════════════════════════════════════════════
# F₂ linear algebra utilities
# ═══════════════════════════════════════════════════════════════

def mat_vec_f2(A, v, n=3):
    """Matrix-vector multiplication over F₂. v is an integer (bit vector)."""
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_mul_f2(A, B, n=3):
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s ^= A[i][k] & B[k][j]
            C[i][j] = s
    return C

def mat_det_f2(A):
    a, b, c = A[0]; d, e, f_ = A[1]; g, h, k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1

def enumerate_gl3f2():
    """All 168 elements of GL(3,F₂)."""
    mats = []
    for row0 in range(1, 8):
        for row1 in range(1, 8):
            for row2 in range(1, 8):
                A = [[(row0>>j)&1 for j in range(3)],
                     [(row1>>j)&1 for j in range(3)],
                     [(row2>>j)&1 for j in range(3)]]
                if mat_det_f2(A):
                    mats.append(A)
    return mats


# ═══════════════════════════════════════════════════════════════
# TASK 1: Coherent Closure from Z₅ Difference
# ═══════════════════════════════════════════════════════════════

def task1():
    print("=" * 72)
    print("TASK 1: COHERENT CLOSURE FROM Z₅ DIFFERENCE")
    print("=" * 72)
    
    F = list(range(8))  # F₂³
    
    # Build the 6-class seed partition
    # Class 0: diagonal
    # Class 1: d=0, off-diagonal (same fiber, x≠y)
    # Class 2: d=1, Class 3: d=2, Class 4: d=3, Class 5: d=4
    
    def seed_class(x, y):
        if x == y:
            return 0
        d = (f(y) - f(x)) % 5
        if d == 0:
            return 1
        return d + 1  # d=1→2, d=2→3, d=3→4, d=4→5
    
    # Enumerate all 64 pairs
    print("\n--- Seed partition ---")
    class_pairs = defaultdict(list)
    for x in F:
        for y in F:
            c = seed_class(x, y)
            class_pairs[c].append((x, y))
    
    for c in sorted(class_pairs.keys()):
        desc = {0: "diagonal", 1: "d=0 off-diag", 2: "d=1", 3: "d=2", 4: "d=3", 5: "d=4"}
        pairs = class_pairs[c]
        print(f"  Class {c} ({desc[c]}): {len(pairs)} pairs")
        for x, y in pairs:
            print(f"    ({trig_label(x)}, {trig_label(y)})  d={f(y)-f(x) if x!=y else '='}")
    
    # Check intersection numbers p_{ij}^k
    print("\n--- Checking intersection numbers ---")
    num_classes = 6
    
    def get_class(x, y):
        return seed_class(x, y)
    
    def check_intersection_numbers(get_cls, nc, cls_pairs):
        """Check if intersection numbers are constant for each class.
        Returns (is_cc, p_tables, violations) where p_tables[k] = matrix p_{ij}^k."""
        violations = []
        p_tables = {}
        
        for k in range(nc):
            p_values = {}  # (i,j) -> set of observed values
            for (x, y) in cls_pairs[k]:
                for i in range(nc):
                    for j in range(nc):
                        count = 0
                        for z in F:
                            if get_cls(x, z) == i and get_cls(z, y) == j:
                                count += 1
                        key = (i, j)
                        if key not in p_values:
                            p_values[key] = {}
                        if count not in p_values[key]:
                            p_values[key][count] = []
                        p_values[key][count].append((x, y))
            
            p_tables[k] = {}
            for (i, j), val_dict in p_values.items():
                if len(val_dict) > 1:
                    violations.append((k, i, j, val_dict))
                else:
                    p_tables[k][(i, j)] = list(val_dict.keys())[0]
        
        return len(violations) == 0, p_tables, violations
    
    is_cc, p_tables, violations = check_intersection_numbers(get_class, num_classes, class_pairs)
    
    if is_cc:
        print("  RESULT: Intersection numbers are CONSTANT → Coherent Configuration!")
        print("\n--- Intersection number matrices ---")
        for k in range(num_classes):
            desc = {0: "diagonal", 1: "d=0 off-diag", 2: "d=1", 3: "d=2", 4: "d=3", 5: "d=4"}
            print(f"\n  M_{k} (class {k}: {desc[k]}):")
            print(f"  {'':8s}", end="")
            for j in range(num_classes):
                print(f"  c{j}", end="")
            print()
            for i in range(num_classes):
                print(f"  c{i:1d}  ", end="")
                for j in range(num_classes):
                    val = p_tables[k].get((i, j), '?')
                    print(f"  {val:2d}" if isinstance(val, int) else f"  {val:>2s}", end="")
                print()
        
        # Check commutativity → AS?
        print("\n--- Checking commutativity (AS test) ---")
        def get_matrix(k):
            M = [[0]*num_classes for _ in range(num_classes)]
            for i in range(num_classes):
                for j in range(num_classes):
                    M[i][j] = p_tables[k].get((i, j), 0)
            return M
        
        matrices = [get_matrix(k) for k in range(num_classes)]
        is_as = True
        for a in range(num_classes):
            for b in range(a+1, num_classes):
                # Compute M_a * M_b and M_b * M_a
                Ma, Mb = matrices[a], matrices[b]
                AB = [[sum(Ma[i][k]*Mb[k][j] for k in range(num_classes)) for j in range(num_classes)] for i in range(num_classes)]
                BA = [[sum(Mb[i][k]*Ma[k][j] for k in range(num_classes)) for j in range(num_classes)] for i in range(num_classes)]
                if AB != BA:
                    is_as = False
                    print(f"  M_{a} * M_{b} ≠ M_{b} * M_{a}")
                    # Show the difference
                    for i in range(num_classes):
                        for j in range(num_classes):
                            if AB[i][j] != BA[i][j]:
                                print(f"    [{i}][{j}]: AB={AB[i][j]}, BA={BA[i][j]}")
        
        if is_as:
            print("  RESULT: All matrices commute → ASSOCIATION SCHEME!")
        else:
            print("  RESULT: Matrices do NOT all commute → CC but not AS")
    
    else:
        print(f"  RESULT: NOT a CC with 6 classes. Found {len(violations)} violations.")
        print("  Need to refine (compute coherent closure).")
        
        # Show the violations
        for (k, i, j, val_dict) in violations[:10]:
            desc = {0: "diag", 1: "d=0off", 2: "d=1", 3: "d=2", 4: "d=3", 5: "d=4"}
            print(f"\n  Violation in class {k}({desc[k]}), p_{{c{i},c{j}}}:")
            for val, pairs in val_dict.items():
                print(f"    value {val}: {len(pairs)} pairs, e.g. {pairs[0]}")
        
        # ── Coherent Closure: iterative refinement ──
        print("\n--- Computing coherent closure ---")
        
        # Start with the seed partition as a function
        partition = {(x, y): seed_class(x, y) for x in F for y in F}
        
        round_num = 0
        while True:
            round_num += 1
            # Group pairs by current class
            cls_map = defaultdict(list)
            for (x, y), c in partition.items():
                cls_map[c].append((x, y))
            
            nc = len(cls_map)
            classes = sorted(cls_map.keys())
            
            # For each class, compute the "profile" of each pair
            # Profile = tuple of (count of z for each (ci, cj) pair)
            new_partition = {}
            split_happened = False
            
            for c in classes:
                profiles = {}
                for (x, y) in cls_map[c]:
                    profile = []
                    for ci in classes:
                        for cj in classes:
                            count = 0
                            for z in F:
                                if partition[(x, z)] == ci and partition[(z, y)] == cj:
                                    count += 1
                            profile.append(count)
                    profile = tuple(profile)
                    if profile not in profiles:
                        profiles[profile] = []
                    profiles[profile].append((x, y))
                
                if len(profiles) > 1:
                    split_happened = True
                    print(f"  Round {round_num}: Splitting class {c} into {len(profiles)} subclasses")
                    for idx, (profile, pairs) in enumerate(sorted(profiles.items())):
                        sub_name = c * 100 + idx if c < 100 else c * 10 + idx
                        # Find a unique name
                        sub_name = max(new_partition.values(), default=-1) + 1
                        for (x, y) in pairs:
                            new_partition[(x, y)] = sub_name
                        print(f"    Subclass → {sub_name}: {len(pairs)} pairs, profile prefix: {profile[:6]}...")
                else:
                    # No split
                    sub_name = max(new_partition.values(), default=-1) + 1
                    for (x, y) in cls_map[c]:
                        new_partition[(x, y)] = sub_name
            
            partition = new_partition
            
            if not split_happened:
                print(f"  Stable after {round_num} rounds.")
                break
            
            if round_num > 20:
                print("  WARNING: 20 rounds reached, stopping.")
                break
        
        # Show final partition
        final_cls = defaultdict(list)
        for (x, y), c in partition.items():
            final_cls[c].append((x, y))
        
        nc_final = len(final_cls)
        print(f"\n  Final class count: {nc_final}")
        
        for c in sorted(final_cls.keys()):
            pairs = final_cls[c]
            # Characterize: check d values and Hamming distances
            d_vals = set()
            h_dists = set()
            for (x, y) in pairs:
                if x != y:
                    d_vals.add((f(y) - f(x)) % 5)
                else:
                    d_vals.add('diag')
                h_dists.add(hamming(x, y))
            
            # Check if all pairs have same XOR mask → Fano line type
            xor_masks = set(x ^ y for (x, y) in pairs)
            
            print(f"\n  Class {c}: {len(pairs)} pairs")
            print(f"    Z₅ diffs: {d_vals}")
            print(f"    Hamming distances: {h_dists}")
            print(f"    XOR masks: {set(fmt3(m) for m in xor_masks)}")
            
            # Show pairs
            for (x, y) in sorted(pairs):
                d = (f(y) - f(x)) % 5 if x != y else '-'
                print(f"      ({trig_label(x)}, {trig_label(y)})  d={d} H={hamming(x,y)} xor={fmt3(x^y)}")
        
        # Verify intersection numbers for the final partition
        print("\n--- Verifying final partition is a CC ---")
        is_cc2, p_tables2, violations2 = check_intersection_numbers(
            lambda x, y: partition[(x, y)],
            nc_final,
            {c: pairs for c, pairs in final_cls.items()}
        )
        
        if is_cc2:
            print("  CONFIRMED: Final partition is a Coherent Configuration!")
            
            classes_sorted = sorted(final_cls.keys())
            
            # Print intersection number tables
            print("\n--- Intersection number matrices ---")
            for k in classes_sorted:
                pairs = final_cls[k]
                d_vals = set()
                for (x, y) in pairs:
                    d_vals.add((f(y) - f(x)) % 5 if x != y else 'diag')
                h_dists = set(hamming(x, y) for (x, y) in pairs)
                
                print(f"\n  M_{k} ({len(pairs)} pairs, d={d_vals}, H={h_dists}):")
                print(f"  {'':8s}", end="")
                for j in classes_sorted:
                    print(f"  c{j}", end="")
                print()
                for i in classes_sorted:
                    print(f"  c{i:1d}  ", end="")
                    for j in classes_sorted:
                        val = p_tables2[k].get((i, j), '?')
                        print(f"  {val:2d}" if isinstance(val, int) else f"  {val:>2s}", end="")
                    print()
            
            # Commutativity check
            print("\n--- Commutativity check for final CC ---")
            def get_matrix2(k):
                M = [[0]*nc_final for _ in range(nc_final)]
                for i_idx, i in enumerate(classes_sorted):
                    for j_idx, j in enumerate(classes_sorted):
                        M[i_idx][j_idx] = p_tables2[k].get((i, j), 0)
                return M
            
            matrices2 = {k: get_matrix2(k) for k in classes_sorted}
            is_as2 = True
            non_commuting_pairs = []
            for a_idx, a in enumerate(classes_sorted):
                for b_idx, b in enumerate(classes_sorted):
                    if b_idx <= a_idx:
                        continue
                    Ma, Mb = matrices2[a], matrices2[b]
                    AB = [[sum(Ma[i][k]*Mb[k][j] for k in range(nc_final)) for j in range(nc_final)] for i in range(nc_final)]
                    BA = [[sum(Mb[i][k]*Ma[k][j] for k in range(nc_final)) for j in range(nc_final)] for i in range(nc_final)]
                    if AB != BA:
                        is_as2 = False
                        non_commuting_pairs.append((a, b))
            
            if is_as2:
                print("  All matrices commute → ASSOCIATION SCHEME!")
            else:
                print(f"  NOT an AS: {len(non_commuting_pairs)} non-commuting pairs found")
                for (a, b) in non_commuting_pairs[:5]:
                    print(f"    M_{a} and M_{b} do not commute")
        else:
            print(f"  NOT a CC! {len(violations2)} violations remain.")
    
    # ── Complement symmetry check ──
    print("\n--- Complement symmetry ---")
    # σ(x) = x ⊕ 111 should map classes to classes
    # And d ↦ -d mod 5 should pair classes
    
    final_cls_map = defaultdict(list)
    for (x, y), c in partition.items():
        final_cls_map[c].append((x, y))
    
    classes_sorted = sorted(final_cls_map.keys())
    
    # For each class, check what class σ maps it to
    print("  Class mapping under complement σ(x)=x⊕111:")
    comp_map = {}
    for c in classes_sorted:
        target_classes = set()
        for (x, y) in final_cls_map[c]:
            sx, sy = x ^ 7, y ^ 7
            target_classes.add(partition[(sx, sy)])
        if len(target_classes) == 1:
            target = target_classes.pop()
            comp_map[c] = target
            
            # Characterize both classes
            d_vals_c = set((f(y)-f(x))%5 if x!=y else 'diag' for (x,y) in final_cls_map[c])
            d_vals_t = set((f(y)-f(x))%5 if x!=y else 'diag' for (x,y) in final_cls_map[target])
            
            self_flag = " (SELF-PAIRED)" if target == c else ""
            print(f"    Class {c} (d={d_vals_c}) → Class {target} (d={d_vals_t}){self_flag}")
        else:
            print(f"    Class {c} → SPLITS into {target_classes} — NOT complement-closed!")
    
    return partition, final_cls_map, p_tables if is_cc else (p_tables2 if 'p_tables2' in dir() else None)


# ═══════════════════════════════════════════════════════════════
# TASK 2: Difference Table + Walsh-Hadamard Spectrum
# ═══════════════════════════════════════════════════════════════

def task2():
    print("\n" + "=" * 72)
    print("TASK 2: DIFFERENCE TABLE + WALSH-HADAMARD SPECTRUM")
    print("=" * 72)
    
    F = list(range(8))
    masks = list(range(1, 8))  # nonzero masks
    
    # ── Difference table ──
    print("\n--- Difference table Δ_m(x) = f(x⊕m) - f(x) mod 5 ---")
    
    # Build table
    diff_table = {}
    for m in masks:
        for x in F:
            diff_table[(m, x)] = (f(x ^ m) - f(x)) % 5
    
    # Display
    print(f"\n  {'mask':>8s}", end="")
    for x in F:
        print(f"  {trig_label(x):>10s}", end="")
    print()
    
    for m in masks:
        print(f"  {fmt3(m):>8s}", end="")
        for x in F:
            print(f"  {diff_table[(m,x)]:>10d}", end="")
        print()
    
    # ── Complement equivariance check ──
    print("\n--- Complement equivariance: Δ_m(~x) = -Δ_m(x) mod 5 ---")
    all_ok = True
    for m in masks:
        for x in F:
            comp_x = x ^ 7
            lhs = diff_table[(m, comp_x)]
            rhs = (-diff_table[(m, x)]) % 5
            if lhs != rhs:
                print(f"  FAIL: m={fmt3(m)}, x={fmt3(x)}: Δ(~x)={lhs} ≠ -Δ(x)={rhs}")
                all_ok = False
    if all_ok:
        print("  VERIFIED: Δ_m(~x) = -Δ_m(x) mod 5 for all m, x")
    
    # ── Rank over Z₅ ──
    print("\n--- Rank of difference table as matrix over Z₅ ---")
    # Build as a 7×8 matrix over Z₅
    mat = [[diff_table[(m, x)] for x in F] for m in masks]
    rank = compute_rank_z5(mat, 7, 8)
    print(f"  Rank = {rank}")
    
    # ── Walsh-Hadamard spectrum ──
    print("\n--- Walsh-Hadamard spectrum ---")
    print("  W_f(ω) = Σ_{x} ζ₅^{f(x)} · (-1)^{⟨ω,x⟩}")
    
    zeta5 = cmath.exp(2j * cmath.pi / 5)
    
    print(f"\n  {'ω':>5s} {'wt(ω)':>6s} {'W_f(ω)':>30s} {'|W_f(ω)|²':>12s} {'Real?':>6s} {'Imag?':>6s}")
    
    walsh_values = {}
    for omega in F:
        W = complex(0, 0)
        for x in F:
            dot = bin(omega & x).count('1') % 2  # ⟨ω,x⟩
            W += zeta5 ** f(x) * ((-1) ** dot)
        
        walsh_values[omega] = W
        wt = bin(omega).count('1')
        is_real = abs(W.imag) < 1e-10
        is_imag = abs(W.real) < 1e-10
        
        # Parity prediction: real when wt even, imaginary when wt odd
        parity_pred = "real" if wt % 2 == 0 else "imag"
        actual = "real" if is_real else ("imag" if is_imag else "mixed")
        match = "✓" if parity_pred == actual else "✗"
        
        print(f"  {fmt3(omega):>5s} {wt:>6d} {W.real:>14.8f}+{W.imag:>13.8f}i {abs(W)**2:>12.6f} {actual:>6s} pred={parity_pred} {match}")
    
    # ── Verify parity prediction ──
    print("\n--- Parity prediction verification ---")
    parity_ok = True
    for omega in F:
        W = walsh_values[omega]
        wt = bin(omega).count('1')
        if wt % 2 == 0:
            if abs(W.imag) > 1e-10:
                print(f"  FAIL: ω={fmt3(omega)} wt={wt} (even) but W has imaginary part {W.imag}")
                parity_ok = False
        else:
            if abs(W.real) > 1e-10:
                print(f"  FAIL: ω={fmt3(omega)} wt={wt} (odd) but W has real part {W.real}")
                parity_ok = False
    if parity_ok:
        print("  VERIFIED: W_f(ω) is real for even-weight ω, purely imaginary for odd-weight ω")
    
    # ── Power spectrum ──
    print("\n--- Power spectrum |W_f(ω)|² ---")
    for omega in F:
        pw = abs(walsh_values[omega]) ** 2
        # Try to identify exact value
        # ζ₅ = e^{2πi/5}, so ζ₅ + ζ₅^4 = 2cos(2π/5) = (√5-1)/2
        # ζ₅^2 + ζ₅^3 = 2cos(4π/5) = -(√5+1)/2
        print(f"  ω={fmt3(omega)}: |W|² = {pw:.10f}")
    
    # ── Exact algebraic forms ──
    print("\n--- Exact algebraic analysis ---")
    c1 = math.cos(2 * math.pi / 5)
    c2 = math.cos(4 * math.pi / 5)
    s1 = math.sin(2 * math.pi / 5)
    s2 = math.sin(4 * math.pi / 5)
    
    print(f"  cos(2π/5) = {c1:.10f} = (√5-1)/4")
    print(f"  cos(4π/5) = {c2:.10f} = -(√5+1)/4")
    print(f"  sin(2π/5) = {s1:.10f}")
    print(f"  sin(4π/5) = {s2:.10f}")
    
    # For ω=000: W = Σ ζ₅^{f(x)} (all signs +1)
    # Count multiplicities: how many x map to each Z₅ value?
    mult = defaultdict(int)
    for x in F:
        mult[f(x)] += 1
    print(f"\n  Fiber multiplicities: {dict(mult)}")
    print(f"  (0=Wood:2, 1=Fire:1, 2=Earth:2, 3=Metal:2, 4=Water:1)")
    
    # W(000) = 2·ζ₅⁰ + 1·ζ₅¹ + 2·ζ₅² + 2·ζ₅³ + 1·ζ₅⁴
    # = 2 + ζ₅ + 2ζ₅² + 2ζ₅³ + ζ₅⁴
    # = 2 + (ζ₅+ζ₅⁴) + 2(ζ₅²+ζ₅³)
    # = 2 + 2cos(2π/5) + 2·2cos(4π/5)
    # = 2 + (√5-1)/2 - 2·(√5+1)/2  [using cos formulas... let me be more careful]
    # Actually: ζ₅+ζ₅⁴ = 2cos(2π/5), ζ₅²+ζ₅³ = 2cos(4π/5)
    # So W(000) = 2 + 2cos(2π/5) + 2·2cos(4π/5) ... wait, coefficients are 1,2 not 1,2
    # = 2 + 1·2cos(2π/5) + 2·2cos(4π/5)
    
    # Let me just compute symbolically for each ω
    for omega in F:
        # Compute the coefficient of each ζ₅^k for each sign pattern
        coeffs = [0] * 5  # coefficient of ζ₅^k
        for x in F:
            dot = bin(omega & x).count('1') % 2
            sign = (-1) ** dot
            coeffs[f(x)] += sign
        
        print(f"\n  ω={fmt3(omega)}: W = {coeffs[0]}·1 + {coeffs[1]}·ζ₅ + {coeffs[2]}·ζ₅² + {coeffs[3]}·ζ₅³ + {coeffs[4]}·ζ₅⁴")
        
        # Verify numerically
        W_check = sum(coeffs[k] * zeta5**k for k in range(5))
        W_actual = walsh_values[omega]
        assert abs(W_check - W_actual) < 1e-10, f"Mismatch at ω={fmt3(omega)}"
    
    return walsh_values


def compute_rank_z5(mat, rows, cols):
    """Compute rank of a matrix over Z₅ using Gaussian elimination."""
    # Work with a copy
    M = [row[:] for row in mat]
    
    def inv5(a):
        """Multiplicative inverse mod 5."""
        for x in range(1, 5):
            if (a * x) % 5 == 1:
                return x
        return None
    
    pivot_row = 0
    for col in range(cols):
        # Find pivot
        found = False
        for row in range(pivot_row, rows):
            if M[row][col] % 5 != 0:
                # Swap
                M[pivot_row], M[row] = M[row], M[pivot_row]
                found = True
                break
        if not found:
            continue
        
        # Scale pivot row
        inv = inv5(M[pivot_row][col] % 5)
        M[pivot_row] = [(x * inv) % 5 for x in M[pivot_row]]
        
        # Eliminate
        for row in range(rows):
            if row == pivot_row:
                continue
            if M[row][col] % 5 != 0:
                factor = M[row][col] % 5
                M[row] = [(M[row][j] - factor * M[pivot_row][j]) % 5 for j in range(cols)]
        
        pivot_row += 1
    
    return pivot_row


# ═══════════════════════════════════════════════════════════════
# TASK 3: Automorphism Orbits
# ═══════════════════════════════════════════════════════════════

def task3():
    print("\n" + "=" * 72)
    print("TASK 3: AUTOMORPHISM ORBITS")
    print("=" * 72)
    
    F = list(range(8))
    
    # ── Enumerate GL(3,F₂) ──
    all_gl = enumerate_gl3f2()
    print(f"\n  |GL(3,F₂)| = {len(all_gl)}")
    
    # ── Stab(111) ──
    stab_111 = []
    for A in all_gl:
        if mat_vec_f2(A, 7) == 7:
            stab_111.append(A)
    print(f"  |Stab(111)| = {len(stab_111)}")
    
    # ── Enumerate all 240 complement-respecting surjections ──
    print("\n--- Enumerating complement-respecting surjections ---")
    
    # Representatives of complement pairs: {0,7}, {1,6}, {2,5}, {3,4}
    # f(~x) = -f(x) mod 5
    # f(0) + f(7) ≡ 0 mod 5
    # f(1) + f(6) ≡ 0 mod 5
    # f(2) + f(5) ≡ 0 mod 5
    # f(3) + f(4) ≡ 0 mod 5
    
    # Representatives: pick from each pair. Use lower element.
    reps = [0, 1, 2, 3]  # x values; companions are 7, 6, 5, 4
    
    all_surjections = []
    for vals in iterproduct(range(5), repeat=4):
        # vals = (f(0), f(1), f(2), f(3))
        # Determine all 8 values
        fmap = {}
        fmap[0] = vals[0]
        fmap[7] = (-vals[0]) % 5
        fmap[1] = vals[1]
        fmap[6] = (-vals[1]) % 5
        fmap[2] = vals[2]
        fmap[5] = (-vals[2]) % 5
        fmap[3] = vals[3]
        fmap[4] = (-vals[3]) % 5
        
        # Check surjectivity
        image = set(fmap.values())
        if len(image) == 5:
            all_surjections.append(tuple(fmap[x] for x in range(8)))
    
    print(f"  Total complement-respecting surjections: {len(all_surjections)}")
    
    # Verify our 五行 map is among them
    wuxing_tuple = tuple(f(x) for x in range(8))
    assert wuxing_tuple in all_surjections, "五行 map not found!"
    print(f"  五行 map: {wuxing_tuple} ✓")
    
    # ── Group action: Stab(111) × Aut(Z₅) ──
    print("\n--- Orbits under Stab(111) × Aut(Z₅) ---")
    
    # Aut(Z₅) = {×1, ×2, ×3, ×4 mod 5}
    aut_z5 = [1, 2, 3, 4]
    
    def apply_action(surj, g, alpha):
        """Compute α ∘ f ∘ g: x ↦ α·f(g(x)) mod 5"""
        return tuple((alpha * surj[mat_vec_f2(g, x)]) % 5 for x in range(8))
    
    # Compute orbits on all 240
    visited = set()
    orbits_240 = []
    for s in all_surjections:
        if s in visited:
            continue
        orbit = set()
        for g in stab_111:
            for alpha in aut_z5:
                t = apply_action(s, g, alpha)
                orbit.add(t)
        orbits_240.append(orbit)
        visited |= orbit
    
    print(f"  Orbits on all {len(all_surjections)} surjections: {len(orbits_240)}")
    for idx, orb in enumerate(orbits_240):
        print(f"    Orbit {idx}: size {len(orb)}, representative: {list(orb)[0]}")
    
    # ── Classify surjections by partition shape ──
    def partition_shape(surj):
        from collections import Counter
        fiber_sizes = sorted(Counter(surj).values(), reverse=True)
        return tuple(fiber_sizes)
    
    shape_groups = defaultdict(list)
    for s in all_surjections:
        shape_groups[partition_shape(s)].append(s)
    
    print(f"\n  Partition shapes:")
    for shape, members in sorted(shape_groups.items()):
        print(f"    {shape}: {len(members)} surjections")
    
    # ── Orbits on 192 three-type surjections ──
    three_type = [s for s in all_surjections if partition_shape(s) == (2, 2, 2, 1, 1)]
    print(f"\n  Three-type surjections ({len(three_type)}):")
    
    visited3 = set()
    orbits_192 = []
    for s in three_type:
        if s in visited3:
            continue
        orbit = set()
        for g in stab_111:
            for alpha in aut_z5:
                t = apply_action(s, g, alpha)
                if t in set(three_type):
                    orbit.add(t)
                else:
                    orbit.add(t)  # Still track even if outside shape
        # Intersect with three_type
        orbit_in = orbit & set(three_type)
        orbits_192.append(orbit_in)
        visited3 |= orbit_in
    
    print(f"  Orbits on 192 three-type: {len(orbits_192)}")
    for idx, orb in enumerate(orbits_192):
        print(f"    Orbit {idx}: size {len(orb)}")
    
    # ── Orbits on I Ching's sub-assignment ──
    # I Ching: Fr=2, H=0, Q=1, P=2
    # Frame pair {0,7}: f(0)=2(Earth), f(7)=3(Metal) → Type 2 (shared doubleton)
    # H pair {1,6}: f(1)=0(Wood), f(6)=0(Wood) → Type 0 (both map to 0)
    # Q pair {2,5}: f(2)=4(Water), f(5)=1(Fire) → Type 1 (singletons)
    # P pair {3,4}: f(3)=3(Metal), f(4)=2(Earth) → Type 2 (shared doubleton)
    
    # Sub-assignment: Fr=2, H=0, Q=1, P=2
    # This means: the pair type distribution is the same
    def pair_types(surj):
        """Compute (Frame_type, H_type, Q_type, P_type)"""
        # Frame = {0,7}: values surj[0], surj[7]
        # H = {1,6}: values surj[1], surj[6]
        # Q = {2,5}: values surj[2], surj[5]
        # P = {3,4}: values surj[3], surj[4]
        
        def classify_pair(v1, v2):
            if v1 == v2 == 0:
                return 0  # Type 0: both at zero (Wood in our encoding)
            # Check if singletons
            from collections import Counter
            # Actually, type depends on fiber structure, not just the pair values
            # Type 0: both map to same value which is the self-neg element (0 mod 5)
            # Wait — in Z₅, the fixed point of negation is 0.
            # Type 0: pair maps to {a, -a} where a = 0, so both map to 0
            if v1 == 0 and v2 == 0:
                return 0
            # Type 1: the pair {v1, v2} = {a, -a} for some a≠0, and no other pair maps to {a, -a}
            # Type 2: the pair {v1, v2} = {a, -a} for some a≠0, shared with another pair
            # This requires knowing the full surjection...
            return None  # Need global context
        
        # Full classification needs counting
        from collections import Counter
        neg_pairs = {}  # negation pair in Z₅ → list of complement pairs mapping there
        # In Z₅, negation pairs are {1,4} and {2,3}. Self-neg: {0}
        
        comp_pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
        for ci, (x, y) in enumerate(comp_pairs):
            a, b = surj[x], surj[y]
            # a and b should satisfy a + b ≡ 0 mod 5
            assert (a + b) % 5 == 0
            # The Z₅ negation pair is {a, b} (which equals {a, -a})
            neg_pair = frozenset({a, b}) if a != b else frozenset({a})
            if neg_pair not in neg_pairs:
                neg_pairs[neg_pair] = []
            neg_pairs[neg_pair].append(ci)
        
        types = [None] * 4
        for neg_pair, covering in neg_pairs.items():
            if neg_pair == frozenset({0}):
                for ci in covering:
                    types[ci] = 0
            elif len(covering) == 1:
                for ci in covering:
                    types[ci] = 1
            else:
                for ci in covering:
                    types[ci] = 2
        
        return tuple(types)  # (Fr, H, Q, P)
    
    # Find all surjections with the I Ching's type pattern
    iching_types = pair_types(wuxing_tuple)
    print(f"\n  I Ching pair types: (Fr={iching_types[0]}, H={iching_types[1]}, Q={iching_types[2]}, P={iching_types[3]})")
    
    same_type = [s for s in all_surjections if pair_types(s) == iching_types]
    print(f"  Surjections with same type pattern: {len(same_type)}")
    
    # Orbits on these
    visited_ic = set()
    orbits_ic = []
    for s in same_type:
        if s in visited_ic:
            continue
        orbit = set()
        for g in stab_111:
            for alpha in aut_z5:
                t = apply_action(s, g, alpha)
                orbit.add(t)
        orbit_in = orbit & set(same_type)
        orbits_ic.append(orbit_in)
        visited_ic |= orbit_in
    
    print(f"  Orbits on {len(same_type)} same-type surjections: {len(orbits_ic)}")
    for idx, orb in enumerate(orbits_ic):
        rep = list(orb)[0]
        print(f"    Orbit {idx}: size {len(orb)}, representative: {rep}")
        # Check if our map is in this orbit
        if wuxing_tuple in orb:
            print(f"      ← Contains the I Ching's 五行 map!")
    
    # Check if the 2-orbit prediction is correct
    if len(orbits_ic) == 2:
        print(f"\n  ✓ CONFIRMED: 2 orbits on I Ching's sub-assignment → 0.5-bit!")
    else:
        print(f"\n  Prediction was 2 orbits, found {len(orbits_ic)}")
    
    return orbits_240, orbits_192, orbits_ic


# ═══════════════════════════════════════════════════════════════
# TASK 4a: Can the CC Predict 互 Dynamics?
# ═══════════════════════════════════════════════════════════════

def task4a(partition):
    print("\n" + "=" * 72)
    print("TASK 4a: CAN THE CC PREDICT 互 DYNAMICS?")
    print("=" * 72)
    
    F = list(range(8))
    
    # ── Recompute T from scratch ──
    print("\n--- Recomputing 互 transition matrix ---")
    
    def nuclear(h):
        """Nuclear hexagram: take lines 2,3,4,5 as new lower/upper."""
        L = [(h >> i) & 1 for i in range(6)]
        nlo = L[1] | (L[2] << 1) | (L[3] << 2)
        nup = L[2] | (L[3] << 1) | (L[4] << 2)
        return nlo | (nup << 3)
    
    def hex_d(h):
        lower = h & 7
        upper = (h >> 3) & 7
        return (f(upper) - f(lower)) % 5
    
    # Build transition matrix
    T = [[0]*5 for _ in range(5)]
    for h in range(64):
        d_orig = hex_d(h)
        d_nuc = hex_d(nuclear(h))
        T[d_orig][d_nuc] += 1
    
    print("\n  T[d][d'] (raw counts):")
    rels = ['同', '生', '克', '被克', '被生']
    print(f"  {'d\\d→':>8s}", end="")
    for d in range(5):
        print(f" {rels[d]:>4s}", end="")
    print(f" {'total':>6s}")
    
    for d in range(5):
        print(f"  {rels[d]:>8s}", end="")
        for dp in range(5):
            print(f" {T[d][dp]:>4d}", end="")
        print(f" {sum(T[d]):>6d}")
    
    # Cross-check with synthesis-2 table
    expected = [
        [6, 2, 2, 2, 2],
        [1, 2, 3, 6, 0],
        [4, 0, 4, 5, 0],
        [4, 0, 5, 4, 0],
        [1, 0, 6, 3, 2],
    ]
    match = T == expected
    print(f"\n  Cross-check with synthesis-2: {'MATCH ✓' if match else 'MISMATCH ✗'}")
    
    # ── Analyze whether T can be derived from CC ──
    print("\n--- Analyzing CC → T relationship ---")
    
    # The key question: 互 maps hexagram h=(lower,upper) to h'=(nuc_lower, nuc_upper)
    # where nuc_lower = lines 2,3,4 of h, nuc_upper = lines 3,4,5 of h
    #
    # In our encoding (b₀=bottom):
    # h = (L₁L₂L₃, L₄L₅L₆) where lower=L₁L₂L₃, upper=L₄L₅L₆
    # nuc_lower = L₂L₃L₄, nuc_upper = L₃L₄L₅
    #
    # So: nuc_lower = (L₂, L₃, L₄) and nuc_upper = (L₃, L₄, L₅)
    # L₂ = bit 1 of lower, L₃ = bit 2 of lower, L₄ = bit 0 of upper
    # L₃ = bit 2 of lower, L₄ = bit 0 of upper, L₅ = bit 1 of upper
    
    # For each hexagram, trace the CC classes involved
    print("\n  For each hexagram h=(lo,up), nuclear h'=(nlo,nup):")
    print(f"  {'h':>4s} {'lo':>6s} {'up':>6s} {'d':>3s} {'nlo':>6s} {'nup':>6s} {'d\'':>3s} {'CC(lo,nlo)':>10s} {'CC(nlo,nup)':>10s}")
    
    # Show a sample
    for h in range(64):
        lo = h & 7
        up = (h >> 3) & 7
        hn = nuclear(h)
        nlo = hn & 7
        nup = (hn >> 3) & 7
        d = hex_d(h)
        dn = hex_d(hn)
        
        cc_lo_nlo = partition.get((lo, nlo), '?')
        cc_nlo_nup = partition.get((nlo, nup), '?')
        cc_lo_up = partition.get((lo, up), '?')
        
        if h < 16 or d != dn:  # Show first 16 and all transitions
            print(f"  {h:>4d} {trig_label(lo):>6s} {trig_label(up):>6s} {d:>3d} {trig_label(nlo):>6s} {trig_label(nup):>6s} {dn:>3d} {cc_lo_nlo:>10} {cc_nlo_nup:>10}")
    
    # ── Key analysis: decompose the transition through CC ──
    print("\n--- CC composition analysis ---")
    print("  Question: Can T[d][d'] be expressed as a sum of products of CC intersection numbers?")
    print()
    
    # The 互 map takes (lo, up) → (nlo, nup) where:
    #   nlo depends on lo and up (it uses bits from both)
    #   nup depends on lo and up (it uses bits from both)
    #
    # The CC only knows about pairwise f-differences. The transition d→d' involves:
    #   d = f(up) - f(lo) mod 5
    #   d' = f(nup) - f(nlo) mod 5
    #
    # For this to be expressible via CC, we'd need the 互 map to factor through
    # the CC relation between lo and up. But 互 uses the actual bit structure,
    # not just the Z₅ difference.
    
    # Test: within each d-class, do hexagrams with the same CC classes for
    # (lo,nlo) and (nlo,nup) always give the same d'?
    
    print("  For each d-class, checking if CC classes determine d':")
    for d in range(5):
        hexes_d = [h for h in range(64) if hex_d(h) == d]
        profile_to_d_prime = defaultdict(set)
        
        for h in hexes_d:
            lo = h & 7
            up = (h >> 3) & 7
            hn = nuclear(h)
            nlo = hn & 7
            nup = (hn >> 3) & 7
            
            cc_profile = (
                partition.get((lo, up), '?'),
                partition.get((lo, nlo), '?'),
                partition.get((lo, nup), '?'),
                partition.get((up, nlo), '?'),
                partition.get((up, nup), '?'),
                partition.get((nlo, nup), '?'),
            )
            
            dn = hex_d(hn)
            profile_to_d_prime[cc_profile].add(dn)
        
        all_determined = all(len(v) == 1 for v in profile_to_d_prime.values())
        print(f"    d={d} ({rels[d]}): {len(profile_to_d_prime)} distinct CC profiles, "
              f"{'all determine d\' uniquely ✓' if all_determined else 'SOME profiles give multiple d\' ✗'}")
        
        if not all_determined:
            for prof, d_primes in profile_to_d_prime.items():
                if len(d_primes) > 1:
                    print(f"      Profile {prof} → d' ∈ {d_primes}")
    
    # ── Alternative: check if 互 preserves CC classes ──
    print("\n--- Does 互 preserve CC classes? ---")
    print("  Check: is CC(lo,up) = CC(nlo,nup) for all hexagrams?")
    
    preserved = 0
    total = 0
    for h in range(64):
        lo = h & 7
        up = (h >> 3) & 7
        hn = nuclear(h)
        nlo = hn & 7
        nup = (hn >> 3) & 7
        
        if partition.get((lo, up)) == partition.get((nlo, nup)):
            preserved += 1
        total += 1
    
    print(f"  CC(lo,up) = CC(nlo,nup): {preserved}/{total} = {preserved/total:.1%}")
    
    # ── Finer analysis: 互 as composition of CC relations ──
    print("\n--- 互 as CC-relation composition ---")
    print("  互 maps (lo,up) → (nlo,nup) where nlo and nup are determined by")
    print("  the bit structure, not just the Z₅ relation.")
    print()
    print("  The nuclear map extracts middle lines: it's fundamentally an F₂-linear")
    print("  operation plus the ī→i shear. The CC only sees Z₅ differences.")
    print("  Can the CC algebra express this F₂ operation?")
    print()
    
    # For each d, compute all (lo,up) pairs and their nuclear (nlo,nup)
    # Group by CC class of (lo,up) → CC class of (nlo,nup)
    cc_transition = defaultdict(lambda: defaultdict(int))
    for h in range(64):
        lo = h & 7
        up = (h >> 3) & 7
        hn = nuclear(h)
        nlo = hn & 7
        nup = (hn >> 3) & 7
        
        c_in = partition.get((lo, up), '?')
        c_out = partition.get((nlo, nup), '?')
        cc_transition[c_in][c_out] += 1
    
    print("  CC class of (lo,up) → CC class of (nlo,nup) transition:")
    for c_in in sorted(cc_transition.keys()):
        outs = cc_transition[c_in]
        print(f"    Class {c_in} → {dict(outs)}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    # Redirect output to both console and file
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()
    
    output_path = "/home/quasar/nous/memories/iching/unification/cc_identity_output.txt"
    with open(output_path, 'w') as log_file:
        tee = Tee(sys.stdout, log_file)
        old_stdout = sys.stdout
        sys.stdout = tee
        
        try:
            partition, final_cls, _ = task1()
            walsh_values = task2()
            orbits_240, orbits_192, orbits_ic = task3()
            task4a(partition)
        finally:
            sys.stdout = old_stdout
    
    print(f"\nOutput saved to {output_path}")
