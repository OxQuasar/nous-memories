#!/usr/bin/env python3
"""
design_analysis.py — The fiber partition as a combinatorial design

Analyzes whether the IC surjection's fiber partition has any design-theoretic
properties: incidence on Fano lines, group-divisible design structure,
balanced incomplete block design properties, etc.
"""

import sys, io
from collections import Counter, defaultdict
from itertools import combinations, product as iterproduct

# ═══════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════

IC = [2, 0, 4, 3, 2, 1, 0, 3]
P = 5
ELEM = {0:'Wood', 1:'Fire', 2:'Earth', 3:'Metal', 4:'Water'}
TRIG_ZH = {0:'坤', 1:'震', 2:'坎', 3:'兌', 4:'艮', 5:'離', 6:'巽', 7:'乾'}

def fmt(x): return format(x, '03b')
def complement(x): return x ^ 7
def popcount(x): return bin(x).count('1')

# ═══════════════════════════════════════════════════════════
# Fano plane
# ═══════════════════════════════════════════════════════════

def fano_lines():
    lines = []
    for mask in range(1, 8):
        pts = sorted(x for x in range(1, 8) if popcount(mask & x) % 2 == 0)
        lines.append(tuple(pts))
    return sorted(set(lines))

# ═══════════════════════════════════════════════════════════
# Fiber partition
# ═══════════════════════════════════════════════════════════

def fiber_partition(f, p=P):
    """Partition F₂³ into fibers of f."""
    fibers = defaultdict(list)
    for x in range(8):
        fibers[f[x]].append(x)
    return dict(fibers)

def fiber_partition_pg(f, p=P):
    """Partition PG(2,F₂) (nonzero points) into fibers."""
    fibers = defaultdict(list)
    for x in range(1, 8):
        fibers[f[x]].append(x)
    return dict(fibers)

# ═══════════════════════════════════════════════════════════
# Orbit infrastructure
# ═══════════════════════════════════════════════════════════

def enumerate_surjections():
    pairs = [(0,7), (1,6), (2,5), (3,4)]
    surjections = []
    for assignment in iterproduct(range(P), repeat=len(pairs)):
        fmap = {}
        for i, (rep, partner) in enumerate(pairs):
            fmap[rep] = assignment[i]
            fmap[partner] = (-assignment[i]) % P
        if len(set(fmap.values())) == P:
            surjections.append(tuple(fmap[x] for x in range(8)))
    return surjections

def mat_vec_f2(A, v):
    result = 0
    for i in range(3):
        s = 0
        for j in range(3):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_det_f2(A):
    a,b,c = A[0]; d,e,f_ = A[1]; g,h,k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1

def mat_inv_f2(A):
    M = [A[i][:] + [1 if i==j else 0 for j in range(3)] for i in range(3)]
    for col in range(3):
        pivot = None
        for row in range(col, 3):
            if M[row][col]: pivot = row; break
        if pivot is None: return None
        if pivot != col: M[col], M[pivot] = M[pivot], M[col]
        for row in range(3):
            if row != col and M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(6)]
    return [M[i][3:] for i in range(3)]

def compute_orbits():
    surjections = enumerate_surjections()
    gl3 = []
    for row0 in range(1,8):
        for row1 in range(1,8):
            for row2 in range(1,8):
                A = [[(row0>>j)&1 for j in range(3)],
                     [(row1>>j)&1 for j in range(3)],
                     [(row2>>j)&1 for j in range(3)]]
                if mat_det_f2(A): gl3.append(A)
    stab = [A for A in gl3 if mat_vec_f2(A, 7) == 7]
    stab_invs = [mat_inv_f2(A) for A in stab]
    aut = list(range(1, P))
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
            for alpha in aut:
                t = tuple((alpha * s[mat_vec_f2(A_inv, x)]) % P for x in range(8))
                if t in surj_set:
                    union(s, t)
    orbit_map = defaultdict(list)
    for s in surjections:
        orbit_map[find(s)].append(s)
    return sorted(orbit_map.values(), key=lambda o: (-len(o), sorted(o)[0]))


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    old_stdout = sys.stdout
    captured = io.StringIO()
    class Tee:
        def __init__(self, *f): self.files = f
        def write(self, d):
            for ff in self.files: ff.write(d)
        def flush(self):
            for ff in self.files: ff.flush()
    sys.stdout = Tee(old_stdout, captured)

    try:
        lines = fano_lines()
        
        print("=" * 72)
        print("  THE FIBER PARTITION AS A COMBINATORIAL DESIGN")
        print("=" * 72)
        print()
        
        # ─── 1. IC fiber partition ───
        print("  " + "=" * 68)
        print("  1. IC FIBER PARTITION")
        print("  " + "=" * 68)
        print()
        
        fibers = fiber_partition(IC)
        comp_pairs = [(0,7), (1,6), (2,5), (3,4)]
        
        for k in range(P):
            pts = fibers.get(k, [])
            labels = [f"{fmt(x)}({TRIG_ZH[x]})" for x in pts]
            print(f"  Block {k} ({ELEM[k]}): {labels} (size {len(pts)})")
        print()
        
        # Show complement pair structure
        print("  Complement pair structure:")
        for rep, partner in comp_pairs:
            print(f"    {{{fmt(rep)}, {fmt(partner)}}}: f = ({IC[rep]}, {IC[partner]}), "
                  f"blocks ({ELEM[IC[rep]]}, {ELEM[IC[partner]]})")
        print()
        
        # ─── 2. Incidence on Fano lines ───
        print("  " + "=" * 68)
        print("  2. BLOCK INCIDENCE ON FANO LINES")
        print("  " + "=" * 68)
        print()
        
        # For PG(2,F₂): only nonzero points matter
        fibers_pg = fiber_partition_pg(IC)
        
        print("  Blocks restricted to PG(2,F₂):")
        for k in range(P):
            pts = fibers_pg.get(k, [])
            labels = [f"{fmt(x)}({TRIG_ZH[x]})" for x in pts]
            print(f"    Block {k} ({ELEM[k]}): {labels} (size {len(pts)})")
        print()
        
        # Block pair intersection via lines
        print("  Block pair intersection matrix (# Fano lines touching both blocks):")
        print(f"  {'':>10}", end='')
        for j in range(P):
            print(f"  {ELEM[j]:>6}", end='')
        print()
        
        for i in range(P):
            print(f"  {ELEM[i]:>10}", end='')
            for j in range(P):
                count = 0
                for line in lines:
                    pts_i = set(fibers_pg.get(i, []))
                    pts_j = set(fibers_pg.get(j, []))
                    has_i = bool(pts_i & set(line))
                    has_j = bool(pts_j & set(line))
                    if has_i and has_j:
                        count += 1
                print(f"  {count:>6}", end='')
            print()
        print()
        
        # Lines through each block
        print("  Lines through each block:")
        for k in range(P):
            pts_k = set(fibers_pg.get(k, []))
            touching = [line for line in lines if pts_k & set(line)]
            print(f"    {ELEM[k]} (|block|={len(pts_k)}): {len(touching)} lines")
        print()
        
        # How many colors per line?
        print("  Colors per Fano line:")
        for line in lines:
            colors = set(IC[x] for x in line)
            color_names = [ELEM[c] for c in sorted(colors)]
            print(f"    {[fmt(x) for x in line]}: {len(colors)} colors: {color_names}")
        print()
        
        # ─── 3. GDD check ───
        print("  " + "=" * 68)
        print("  3. GROUP-DIVISIBLE DESIGN CHECK")
        print("  " + "=" * 68)
        print()
        print("  A GDD requires:")
        print("  - Groups (here: complement pairs)")
        print("  - Blocks (here: fibers of f)")
        print("  - Each pair of points from different groups appears in exactly λ blocks")
        print()
        
        # Groups = complement pairs
        groups = [{rep, partner} for rep, partner in comp_pairs]
        # Blocks = fibers
        blocks = [set(fibers[k]) for k in range(P)]
        
        # For each pair of points from different groups:
        # how many blocks contain both?
        lambdas = Counter()
        for i, g1 in enumerate(groups):
            for j, g2 in enumerate(groups):
                if i >= j: continue
                for x in g1:
                    for y in g2:
                        count = sum(1 for b in blocks if x in b and y in b)
                        lambdas[count] += 1
        
        print(f"  λ-values for cross-group pairs: {dict(sorted(lambdas.items()))}")
        
        if len(lambdas) == 1:
            lam = list(lambdas.keys())[0]
            print(f"  ★ All cross-group pairs have λ = {lam} → GDD property satisfied!")
        else:
            print(f"  λ is not constant → NOT a GDD in the strict sense")
        print()
        
        # Also check: pairs within groups
        print("  Within-group pair coverage:")
        for i, g in enumerate(groups):
            pts = sorted(g)
            count = sum(1 for b in blocks if pts[0] in b and pts[1] in b)
            print(f"    Group {[fmt(x) for x in pts]}: λ = {count}")
        print()
        
        # ─── 4. Cross-orbit comparison ───
        print("  " + "=" * 68)
        print("  4. CROSS-ORBIT COMPARISON")
        print("  " + "=" * 68)
        print()
        
        orbits = compute_orbits()
        ic_tuple = tuple(IC)
        
        for idx, orbit in enumerate(orbits):
            rep = sorted(orbit)[0]
            is_ic = ic_tuple in orbit
            marker = " ★" if is_ic else ""
            shape = tuple(sorted(Counter(rep).values(), reverse=True))
            
            fibers_rep = fiber_partition(list(rep))
            blocks_rep = [set(fibers_rep[k]) for k in range(P)]
            
            # GDD check
            lambdas_rep = Counter()
            for i, g1 in enumerate(groups):
                for j, g2 in enumerate(groups):
                    if i >= j: continue
                    for x in g1:
                        for y in g2:
                            count = sum(1 for b in blocks_rep if x in b and y in b)
                            lambdas_rep[count] += 1
            
            is_gdd = len(lambdas_rep) == 1
            
            # Colors per line
            line_colors = Counter()
            for line in lines:
                nc = len(set(rep[x] for x in line))
                line_colors[nc] += 1
            
            # Same-color pairs count (within blocks, restricted to PG)
            fibers_pg_rep = fiber_partition_pg(list(rep))
            same_color_on_line = 0
            for line in lines:
                for a, b in combinations(line, 2):
                    if rep[a] == rep[b]:
                        same_color_on_line += 1
            
            print(f"  Orbit {idx} (size {len(orbit)}, shape {list(shape)}){marker}:")
            print(f"    GDD: {'✓' if is_gdd else 'no'} (λ dist: {dict(sorted(lambdas_rep.items()))})")
            print(f"    Colors/line: {dict(sorted(line_colors.items()))}")
            print(f"    Same-color pairs on Fano lines: {same_color_on_line}/21")
            print()
        
        # ─── 5. Complementary balance ───
        print("  " + "=" * 68)
        print("  5. COMPLEMENTARY BALANCE")
        print("  " + "=" * 68)
        print()
        print("  For each Z₅ value k, consider block_k ∪ block_{-k mod 5}:")
        print("  These are the 'complement-related' blocks.")
        print()
        
        for k in range(P):
            neg_k = (-k) % P
            if neg_k < k: continue
            pts = sorted(set(fibers.get(k, []) + fibers.get(neg_k, [])))
            labels = [f"{fmt(x)}" for x in pts]
            if k == neg_k:
                print(f"  Block {k} (self-neg): {labels} (size {len(pts)})")
            else:
                print(f"  Blocks {k}∪{neg_k}: {labels} (size {len(pts)})")
        print()
        
        # These unions are exactly the complement pairs plus the 0-fiber
        print("  Complement constraint: f(~x) = -f(x) means")
        print("  block_k and block_{-k} are complement-related.")
        print("  {x, ~x} always maps to {k, -k}.")
        print("  For k=0: both to 0. For k≠0: one to k, one to -k.")
        
    finally:
        sys.stdout = old_stdout
    
    path = "/home/quasar/nous/memories/iching/relations/design_analysis_output.md"
    with open(path, 'w') as out:
        out.write(captured.getvalue())
    print(f"\nResults written to {path}")


if __name__ == "__main__":
    main()
