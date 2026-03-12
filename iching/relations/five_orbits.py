#!/usr/bin/env python3
"""
five_orbits.py — Complete orbit decomposition at (3,5)

F₂³ → Z₅ has 240 complement-respecting surjections and 5 orbits
under Stab(111) × Aut(Z₅) (|G| = 24 × 4 = 96).

This script:
1. Enumerates all 240 surjections
2. Computes the 5 orbits explicitly
3. Characterizes each orbit: size, fiber shape, type distribution,
   representative, stabilizer, action freeness
4. Identifies which orbit is the I Ching's (Orbit C from unification)
"""

import sys
import io
from collections import Counter, defaultdict
from itertools import product as iterproduct, permutations

# ═══════════════════════════════════════════════════════════
# F₂³ utilities
# ═══════════════════════════════════════════════════════════

def complement(x, n=3):
    return x ^ ((1 << n) - 1)

def mat_vec_f2(A, v, n=3):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_det_f2(A):
    a, b, c = A[0]; d, e, f_ = A[1]; g, h, k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1

def mat_inv_f2(A, n=3):
    M = [A[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]: pivot = row; break
        if pivot is None: return None
        if pivot != col: M[col], M[pivot] = M[pivot], M[col]
        for row in range(n):
            if row != col and M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(2 * n)]
    return [M[i][n:] for i in range(n)]

def enumerate_gl3f2():
    mats = []
    for row0 in range(1, 8):
        for row1 in range(1, 8):
            for row2 in range(1, 8):
                A = [[(row0 >> j) & 1 for j in range(3)],
                     [(row1 >> j) & 1 for j in range(3)],
                     [(row2 >> j) & 1 for j in range(3)]]
                if mat_det_f2(A):
                    mats.append(A)
    return mats


# ═══════════════════════════════════════════════════════════
# Complement pairs and surjection enumeration
# ═══════════════════════════════════════════════════════════

def get_complement_pairs():
    """Complement pairs in F₂³. Returns list of (rep, partner) with rep < partner."""
    pairs = []
    seen = set()
    for x in range(8):
        if x in seen: continue
        cx = complement(x)
        seen.add(x); seen.add(cx)
        pairs.append((min(x, cx), max(x, cx)))
    return sorted(pairs)

def enumerate_surjections():
    """Enumerate all 240 complement-respecting surjections F₂³ → Z₅.
    f(~x) = -f(x) mod 5.
    Returns list of tuples (f(0), f(1), ..., f(7))."""
    pairs = get_complement_pairs()  # [(0,7), (1,6), (2,5), (3,4)]
    p = 5
    surjections = []
    
    for assignment in iterproduct(range(p), repeat=len(pairs)):
        fmap = {}
        for i, (rep, partner) in enumerate(pairs):
            fmap[rep] = assignment[i]
            fmap[partner] = (-assignment[i]) % p
        
        if len(set(fmap.values())) == p:
            s = tuple(fmap[x] for x in range(8))
            surjections.append(s)
    
    return surjections


# ═══════════════════════════════════════════════════════════
# Stab(111) computation
# ═══════════════════════════════════════════════════════════

def compute_stab111():
    """Stab(111) = {A ∈ GL(3,F₂) : A·(111) = (111)}.
    |Stab(111)| = |GL(3,F₂)| / (2³-1) = 168/7 = 24."""
    gl3 = enumerate_gl3f2()
    all_ones = 7  # 111 in binary
    stab = [A for A in gl3 if mat_vec_f2(A, all_ones) == all_ones]
    return stab


# ═══════════════════════════════════════════════════════════
# Orbit computation
# ═══════════════════════════════════════════════════════════

def compute_orbits(surjections, stab, p=5):
    """Compute orbits of surjections under Stab(111) × Aut(Z₅)."""
    aut_zp = list(range(1, p))  # {1, 2, 3, 4}
    
    # Precompute inverses
    stab_invs = [mat_inv_f2(A) for A in stab]
    
    # Union-find
    parent = {s: s for s in surjections}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    
    surj_set = set(surjections)
    
    for s in surjections:
        for A_inv in stab_invs:
            for alpha in aut_zp:
                t = tuple((alpha * s[mat_vec_f2(A_inv, x)]) % p for x in range(8))
                if t in surj_set:
                    union(s, t)
    
    # Collect orbits
    orbit_map = defaultdict(list)
    for s in surjections:
        orbit_map[find(s)].append(s)
    
    orbits = sorted(orbit_map.values(), key=lambda o: (-len(o), o[0]))
    return orbits


# ═══════════════════════════════════════════════════════════
# Orbit characterization
# ═══════════════════════════════════════════════════════════

TRIG_ZH = {0: '坤', 1: '震', 2: '坎', 3: '兌', 4: '艮', 5: '離', 6: '巽', 7: '乾'}
ELEM_NAME = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}

# The I Ching encoding (from cc_identity.py)
IC_WUXING = {0: 2, 1: 0, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0, 7: 3}

def fiber_shape(s, p=5):
    """Fiber sizes sorted descending."""
    return tuple(sorted(Counter(s).values(), reverse=True))

def type_distribution(s, p=5):
    """For each complement pair, what 'type' is it?
    Type 0: both map to 0 (pair maps to {0,0})
    Type 1: maps to a unique negation pair
    Type 2: shares a negation pair with another pair
    
    Actually, simpler: the type is determined by the value of f(rep).
    - f(rep) = 0: pair maps to {0, 0}
    - f(rep) ≠ 0: pair maps to {v, -v} for some negation pair
    
    The 'type distribution' is which negation pairs share fibers.
    """
    pairs = get_complement_pairs()
    neg_pair_assignment = {}
    for i, (rep, partner) in enumerate(pairs):
        v = s[rep]
        if v == 0:
            neg_pair_assignment[i] = 'zero'
        else:
            # Which negation pair? {v, p-v}
            slot = min(v, p - v)
            neg_pair_assignment[i] = slot
    
    # Count how many domain pairs map to each slot
    slot_counts = Counter(neg_pair_assignment.values())
    
    # Type: 0 if maps to zero, 1 if unique slot, 2 if shared slot
    types = {}
    for i, slot in neg_pair_assignment.items():
        if slot == 'zero':
            types[i] = 0
        elif slot_counts[slot] == 1:
            types[i] = 1
        else:
            types[i] = 2
    
    return tuple(types[i] for i in range(len(pairs)))

def check_freeness(orbit, stab, p=5):
    """Check if the action on this orbit is free (no non-identity element fixes any surjection)."""
    aut_zp = list(range(1, p))
    stab_invs = [mat_inv_f2(A) for A in stab]
    identity = [[1,0,0],[0,1,0],[0,0,1]]
    
    for s in orbit:
        for A, A_inv in zip(stab, stab_invs):
            for alpha in aut_zp:
                if A == identity and alpha == 1:
                    continue
                t = tuple((alpha * s[mat_vec_f2(A_inv, x)]) % p for x in range(8))
                if t == s:
                    return False, (A, alpha)
    return True, None

def is_ic_orbit(orbit):
    """Check if the I Ching surjection is in this orbit."""
    ic = tuple(IC_WUXING[x] for x in range(8))
    return ic in orbit


def main():
    old_stdout = sys.stdout
    captured = io.StringIO()

    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
        def flush(self):
            for f in self.files:
                f.flush()

    sys.stdout = Tee(old_stdout, captured)

    try:
        p = 5
        pairs = get_complement_pairs()
        
        print("=" * 72)
        print("  FIVE-ORBIT DECOMPOSITION AT (3,5)")
        print("=" * 72)
        print()
        print(f"  Domain: F₂³ (8 elements)")
        print(f"  Target: Z₅")
        print(f"  Complement pairs: {pairs}")
        print(f"  Negation pairs in Z₅: {{1,4}}, {{2,3}}")
        print()
        
        # Enumerate surjections
        surjections = enumerate_surjections()
        print(f"  Total surjections: {len(surjections)}")
        
        # Check fiber shapes
        shapes = Counter(fiber_shape(s) for s in surjections)
        print(f"  Fiber shapes:")
        for shape, count in sorted(shapes.items(), key=lambda x: -x[1]):
            print(f"    {list(shape)}: {count} surjections")
        print()
        
        # Compute Stab(111)
        stab = compute_stab111()
        aut_zp = list(range(1, p))
        group_size = len(stab) * len(aut_zp)
        print(f"  |Stab(111)| = {len(stab)}")
        print(f"  |Aut(Z₅)| = {len(aut_zp)}")
        print(f"  |G| = |Stab × Aut| = {group_size}")
        print()
        
        # Compute orbits
        orbits = compute_orbits(surjections, stab, p)
        print(f"  Number of orbits: {len(orbits)}")
        print(f"  Orbit sizes: {[len(o) for o in orbits]}")
        total = sum(len(o) for o in orbits)
        print(f"  Total: {total} (should be {len(surjections)})")
        assert total == len(surjections)
        print()
        
        # Characterize each orbit
        print("  " + "=" * 68)
        print("  ORBIT DETAILS")
        print("  " + "=" * 68)
        
        ic_tuple = tuple(IC_WUXING[x] for x in range(8))
        
        for idx, orbit in enumerate(orbits):
            size = len(orbit)
            rep = sorted(orbit)[0]
            shape = fiber_shape(rep)
            tdist = type_distribution(rep)
            is_ic = is_ic_orbit(orbit)
            free, nonfree_element = check_freeness(orbit, stab, p)
            stab_size = group_size // size
            
            label = "★ I CHING ORBIT" if is_ic else ""
            print(f"\n  ─── Orbit {idx} ({label}) ───" if is_ic else f"\n  ─── Orbit {idx} ───")
            print(f"    Size: {size}")
            print(f"    Fiber shape: {list(shape)}")
            print(f"    Type distribution: {tdist}")
            print(f"    Action free: {'yes' if free else 'no'}")
            print(f"    |Stabilizer|: {stab_size}")
            
            if is_ic:
                print(f"    ★ Contains the I Ching surjection")
                print(f"    IC map: {list(ic_tuple)}")
                for x in range(8):
                    print(f"      {format(x,'03b')} ({TRIG_ZH[x]}) → {ic_tuple[x]} ({ELEM_NAME[ic_tuple[x]]})")
            
            # Show representative
            print(f"    Representative: {list(rep)}")
            for x in range(8):
                cx = complement(x)
                print(f"      {format(x,'03b')} → {rep[x]},  ~{format(x,'03b')}={format(cx,'03b')} → {rep[cx]}  (sum mod 5 = {(rep[x]+rep[cx])%5})")
            
            # Verify complement constraint
            ok = all((rep[x] + rep[complement(x)]) % p == 0 for x in range(8))
            print(f"    Complement constraint verified: {ok}")
            
            # Count type distributions in orbit
            tdists = Counter(type_distribution(s) for s in orbit)
            print(f"    Type distributions in orbit: {dict(tdists)}")
            
            # Frame pair analysis: pair (0, 7)
            frame_vals = Counter()
            for s in orbit:
                frame_vals[s[0]] += 1  # f(000)
            print(f"    Frame (000) values in orbit: {dict(sorted(frame_vals.items()))}")
        
        # Summary table
        print()
        print("  " + "=" * 68)
        print("  SUMMARY TABLE")
        print("  " + "=" * 68)
        print()
        print(f"  {'Orbit':>5} {'Size':>5} {'Shape':>15} {'Type Dist':>15} {'Free':>5} {'|Stab|':>6} {'IC':>3}")
        print(f"  {'-'*55}")
        
        for idx, orbit in enumerate(orbits):
            size = len(orbit)
            shape = fiber_shape(sorted(orbit)[0])
            tdist = type_distribution(sorted(orbit)[0])
            is_ic = is_ic_orbit(orbit)
            free, _ = check_freeness(orbit, stab, p)
            stab_size = group_size // size
            
            print(f"  {idx:>5} {size:>5} {str(list(shape)):>15} {str(tdist):>15} {'yes' if free else 'no':>5} {stab_size:>6} {'★' if is_ic else '':>3}")
        
        print(f"  {'-'*55}")
        print(f"  {'Total':>5} {sum(len(o) for o in orbits):>5}")
        print()
        
        # Key finding
        ic_orbit = [o for o in orbits if is_ic_orbit(o)][0]
        ic_size = len(ic_orbit)
        ic_free, _ = check_freeness(ic_orbit, stab, p)
        
        print("  KEY FINDING:")
        if ic_free and ic_size == group_size:
            print(f"  The I Ching orbit is the UNIQUE orbit where the action is")
            print(f"  REGULAR (free + transitive): orbit size = |G| = {group_size}.")
            other_regular = sum(1 for o in orbits if len(o) == group_size and o is not ic_orbit)
            if other_regular > 0:
                print(f"  However, {other_regular} other orbit(s) also have size {group_size}.")
            else:
                print(f"  No other orbit has size {group_size}.")
        elif ic_free:
            print(f"  The I Ching orbit has free action (size {ic_size}, |Stab|=1).")
        else:
            print(f"  The I Ching orbit has non-trivial stabilizer (size {ic_size}).")
        
        # Check which orbits have maximal size
        max_size = max(len(o) for o in orbits)
        max_orbits = [i for i, o in enumerate(orbits) if len(o) == max_size]
        print(f"\n  Largest orbits: {max_orbits} (size {max_size})")
        
        # Are all orbits the same size?
        sizes = [len(o) for o in orbits]
        if len(set(sizes)) == 1:
            print(f"  All orbits have the same size: {sizes[0]}")
            print(f"  Every orbit has |stabilizer| = {group_size // sizes[0]}")
        else:
            print(f"  Orbits have different sizes: {sorted(set(sizes))}")
        
    finally:
        sys.stdout = old_stdout
    
    path = "/home/quasar/nous/memories/iching/relations/five_orbits_output.md"
    with open(path, 'w') as f:
        f.write(captured.getvalue())
    print(f"\nResults written to {path}")


if __name__ == "__main__":
    main()
