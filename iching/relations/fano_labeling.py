#!/usr/bin/env python3
"""
fano_labeling.py — Z₅ labeling on the Fano plane PG(2,F₂)

Analyzes the IC surjection restricted to PG(2,F₂) (the 7 nonzero points):
1. Z₅ triples on each Fano line
2. Line sums mod 5
3. Difference patterns along lines
4. Collinear vs non-collinear difference distributions
5. Cross-orbit comparison
"""

import sys, io
from collections import Counter, defaultdict
from itertools import combinations, product as iterproduct

# ═══════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════

IC = [2, 0, 4, 3, 2, 1, 0, 3]
P = 5
TRIG_ZH = {0:'坤', 1:'震', 2:'坎', 3:'兌', 4:'艮', 5:'離', 6:'巽', 7:'乾'}
ELEM = {0:'Wood', 1:'Fire', 2:'Earth', 3:'Metal', 4:'Water'}

def fmt(x): return format(x, '03b')
def complement(x): return x ^ 7
def popcount(x): return bin(x).count('1')

# ═══════════════════════════════════════════════════════════
# Fano plane
# ═══════════════════════════════════════════════════════════

def fano_lines():
    """The 7 lines of PG(2,F₂). Each line = {a,b,c} with a⊕b⊕c = 0."""
    lines = []
    for mask in range(1, 8):
        pts = [x for x in range(1, 8) if popcount(mask & x) % 2 == 0]
        assert len(pts) == 3
        assert pts[0] ^ pts[1] ^ pts[2] == 0
        lines.append(tuple(sorted(pts)))
    # Remove duplicates
    return sorted(set(lines))

def fano_pairs():
    """All 21 unordered pairs of points in PG(2,F₂)."""
    return list(combinations(range(1, 8), 2))

def is_collinear(a, b, lines):
    """Check if points a, b are on a common line."""
    for line in lines:
        if a in line and b in line:
            return True
    return False

# ═══════════════════════════════════════════════════════════
# Line analysis
# ═══════════════════════════════════════════════════════════

def line_triple(f, line):
    """Z₅ values on a line, sorted by point."""
    return tuple(f[x] for x in line)

def line_sum(f, line, p=P):
    return sum(f[x] for x in line) % p

def line_differences(f, line, p=P):
    """Pairwise Z₅ differences on a line: (f(b)-f(a), f(c)-f(a), f(c)-f(b))."""
    a, b, c = line
    return ((f[b]-f[a])%p, (f[c]-f[a])%p, (f[c]-f[b])%p)

def line_label(line):
    return '{' + ', '.join(f"{fmt(x)}({TRIG_ZH[x]})" for x in line) + '}'

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
            for f in self.files: f.write(d)
        def flush(self):
            for f in self.files: f.flush()
    sys.stdout = Tee(old_stdout, captured)

    try:
        lines = fano_lines()
        pairs = fano_pairs()
        
        print("=" * 72)
        print("  Z₅ LABELING ON THE FANO PLANE")
        print("=" * 72)
        print()
        print(f"  f = {IC}")
        print(f"  PG(2,F₂): 7 points (nonzero F₂³), 7 lines")
        print()
        
        # ─── 1. Z₅ triples ───
        print("  " + "=" * 68)
        print("  1. Z₅ TRIPLES ON FANO LINES")
        print("  " + "=" * 68)
        print()
        
        for line in lines:
            triple = line_triple(IC, line)
            s = line_sum(IC, line)
            diffs = line_differences(IC, line)
            label = line_label(line)
            elem_triple = tuple(ELEM[IC[x]] for x in line)
            print(f"  {label}")
            print(f"    Values: {triple}, Sum mod 5 = {s}")
            print(f"    Elements: {elem_triple}")
            print(f"    Diffs: {diffs}")
            print()
        
        # ─── 2. Line sums ───
        print("  " + "=" * 68)
        print("  2. LINE SUM DISTRIBUTION")
        print("  " + "=" * 68)
        print()
        
        sums = [line_sum(IC, line) for line in lines]
        sum_dist = Counter(sums)
        print(f"  Line sums: {sums}")
        print(f"  Distribution: {dict(sorted(sum_dist.items()))}")
        print()
        
        # Check if any line is monochromatic (all same value)
        mono = [(line, line_triple(IC, line)) for line in lines 
                if len(set(IC[x] for x in line)) == 1]
        bichro = [(line, line_triple(IC, line)) for line in lines
                  if len(set(IC[x] for x in line)) == 2]
        trichro = [(line, line_triple(IC, line)) for line in lines
                   if len(set(IC[x] for x in line)) == 3]
        
        print(f"  Monochromatic lines: {len(mono)}")
        print(f"  Bichromatic lines: {len(bichro)}")
        for line, triple in bichro:
            vals = Counter(IC[x] for x in line)
            print(f"    {line_label(line)}: {triple} → {dict(vals)}")
        print(f"  Trichromatic lines: {len(trichro)}")
        print()
        
        # ─── 3. Collinear vs non-collinear differences ───
        print("  " + "=" * 68)
        print("  3. COLLINEAR VS NON-COLLINEAR DIFFERENCES")
        print("  " + "=" * 68)
        print()
        
        coll_diffs = Counter()
        noncoll_diffs = Counter()
        
        for a, b in pairs:
            d = (IC[b] - IC[a]) % P
            d_sym = min(d, P - d)  # unsigned
            if is_collinear(a, b, lines):
                coll_diffs[d_sym] += 1
            else:
                noncoll_diffs[d_sym] += 1
        
        print(f"  Collinear pairs (7 lines × 3 pairs = 21): {sum(coll_diffs.values())}")
        print(f"  Non-collinear pairs (21 total - 21 collinear = 0)...")
        
        # Actually: 7 lines × C(3,2) = 21 collinear pairs but
        # total pairs = C(7,2) = 21. So ALL pairs are collinear!
        # Every pair of points in PG(2,F₂) lies on exactly 1 line.
        total_pairs = len(pairs)
        coll_count = sum(coll_diffs.values())
        noncoll_count = sum(noncoll_diffs.values())
        
        print(f"  Total pairs: {total_pairs}")
        print(f"  Collinear: {coll_count}")
        print(f"  Non-collinear: {noncoll_count}")
        print()
        
        if noncoll_count == 0:
            print("  ★ Every pair of points in PG(2,F₂) is collinear!")
            print("  (This is a property of PG(2,F₂): every pair lies on exactly 1 line)")
            print()
        
        # Z₅ difference distribution over all 21 pairs
        all_diffs_unsigned = Counter()
        all_diffs_signed = Counter()
        for a, b in pairs:
            d = (IC[b] - IC[a]) % P
            all_diffs_unsigned[min(d, P-d)] += 1
            all_diffs_signed[d] += 1
        
        print(f"  Unsigned difference distribution (|d| = min(d, 5-d)):")
        for d in sorted(all_diffs_unsigned):
            print(f"    |d| = {d}: {all_diffs_unsigned[d]} pairs")
        
        print()
        print(f"  Signed difference distribution:")
        for d in sorted(all_diffs_signed):
            count = all_diffs_signed[d]
            rel = ""
            if d == 1 or d == 4:
                rel = " (generation ±1)"
            elif d == 2 or d == 3:
                rel = " (overcoming ±2)"
            elif d == 0:
                rel = " (same element)"
            print(f"    d = {d}: {count} pairs{rel}")
        
        print()
        
        # ─── 4. Connection to 五行 ───
        print("  " + "=" * 68)
        print("  4. 五行 RELATION ON FANO LINES")
        print("  " + "=" * 68)
        print()
        print("  Z₅ differences encode 五行 relations:")
        print("  d = ±1 (mod 5): generation (相生)")
        print("  d = ±2 (mod 5): overcoming (相克)")
        print("  d = 0: same element (同)")
        print()
        
        for line in lines:
            a, b, c = line
            dab = (IC[b] - IC[a]) % P
            dac = (IC[c] - IC[a]) % P
            dbc = (IC[c] - IC[b]) % P
            
            def rel(d):
                if d == 0: return "same"
                if d in (1, 4): return "gen"
                return "over"
            
            rels = (rel(dab), rel(dac), rel(dbc))
            label = line_label(line)
            print(f"  {label}")
            print(f"    {TRIG_ZH[a]}→{TRIG_ZH[b]}: d={dab} ({rel(dab)}), "
                  f"{TRIG_ZH[a]}→{TRIG_ZH[c]}: d={dac} ({rel(dac)}), "
                  f"{TRIG_ZH[b]}→{TRIG_ZH[c]}: d={dbc} ({rel(dbc)})")
            print(f"    Relation profile: {rels}")
            print()
        
        # ─── 5. Cross-orbit comparison ───
        print("  " + "=" * 68)
        print("  5. CROSS-ORBIT LINE SUM COMPARISON")
        print("  " + "=" * 68)
        print()
        
        orbits = compute_orbits()
        ic_tuple = tuple(IC)
        
        for idx, orbit in enumerate(orbits):
            rep = sorted(orbit)[0]
            is_ic = ic_tuple in orbit
            marker = " ★" if is_ic else ""
            
            rep_sums = tuple(sorted(line_sum(list(rep), line) for line in lines))
            
            # Check orbit invariance of line sum multiset
            sum_multisets = set()
            for s in orbit:
                ms = tuple(sorted(line_sum(list(s), line) for line in lines))
                sum_multisets.add(ms)
            
            invariant = len(sum_multisets) == 1
            
            # Count distinct relation profiles
            diff_profiles = set()
            for s in orbit:
                profile = []
                for line in lines:
                    diffs = tuple(sorted([(s[b]-s[a])%P for a,b in combinations(line, 2)]))
                    profile.append(diffs)
                diff_profiles.add(tuple(sorted(profile)))
            
            shape = tuple(sorted(Counter(rep).values(), reverse=True))
            print(f"  Orbit {idx} (size {len(orbit)}, shape {list(shape)}){marker}:")
            print(f"    Rep line sums: {rep_sums}")
            print(f"    Line sum multiset orbit-invariant: {'✓' if invariant else f'no ({len(sum_multisets)} types)'}")
            print(f"    Distinct diff profiles: {len(diff_profiles)}")
            print()
        
        # ─── 6. Fano line sum structure ───
        print("  " + "=" * 68)
        print("  6. STRUCTURAL ANALYSIS OF LINE SUMS")
        print("  " + "=" * 68)
        print()
        
        # For the IC surjection:
        print("  IC surjection line sums:")
        for line in lines:
            s = line_sum(IC, line)
            triple = line_triple(IC, line)
            # Also check: is this related to complement lines?
            comp_line = tuple(sorted(complement(x) for x in line))
            if comp_line in [tuple(sorted(l)) for l in lines]:
                cs = line_sum(IC, list(comp_line))
                print(f"    Line {[fmt(x) for x in line]}: sum={s}, "
                      f"comp line {[fmt(x) for x in sorted(comp_line)]}: sum={cs}, "
                      f"s+cs mod 5 = {(s+cs)%P}")
            else:
                print(f"    Line {[fmt(x) for x in line]}: sum={s} (no complement line in PG)")
        
        print()
        
        # Check: does the complement map act on Fano lines?
        print("  Complement action on Fano lines:")
        for line in lines:
            comp = tuple(sorted(complement(x) for x in line))
            if comp in [tuple(sorted(l)) for l in lines]:
                print(f"    {[fmt(x) for x in line]} → {[fmt(x) for x in comp]}: IS a Fano line")
            else:
                print(f"    {[fmt(x) for x in line]} → {[fmt(x) for x in comp]}: NOT a Fano line")
        
        # Check if 000 is involved
        print()
        print("  Note: complement of a nonzero point can be 000 (not in PG).")
        print("  E.g., complement(111) = 000. So complement does NOT")
        print("  preserve PG(2,F₂) as a set.")
        
    finally:
        sys.stdout = old_stdout
    
    path = "/home/quasar/nous/memories/iching/relations/fano_labeling_output.md"
    with open(path, 'w') as out:
        out.write(captured.getvalue())
    print(f"\nResults written to {path}")


if __name__ == "__main__":
    main()
