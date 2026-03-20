#!/usr/bin/env python3
"""Probe 2a: bit₀+bit₂ union graph, pure-克 layer count, full 8-cycle scan."""

from itertools import combinations, permutations
from collections import Counter, defaultdict

# ─── Definitions (same as m1) ─────────────────────────────────────────────

XIANTIAN = [
    (1, "乾", (1,1,1)), (2, "兌", (0,1,1)), (3, "離", (1,0,1)), (4, "震", (0,0,1)),
    (5, "巽", (1,1,0)), (6, "坎", (0,1,0)), (7, "艮", (1,0,0)), (8, "坤", (0,0,0)),
]

NAMES = {v: name for _, name, v in XIANTIAN}
POS   = {v: pos  for pos, _, v in XIANTIAN}
VEC   = {pos: v  for pos, _, v in XIANTIAN}
ALL_VECS = [(b2,b1,b0) for b2 in range(2) for b1 in range(2) for b0 in range(2)]

WUXING_MAP = {
    (1,1,1): 0, (0,1,1): 0, (0,1,0): 1,
    (0,0,1): 2, (1,1,0): 2, (1,0,1): 3,
    (0,0,0): 4, (1,0,0): 4,
}
Z5_NAMES = {0: "Metal", 1: "Water", 2: "Wood", 3: "Fire", 4: "Earth"}

def wuxing_type(a, b):
    d = abs(a - b); d = min(d, 5 - d)
    return {0: "比和", 1: "生", 2: "克"}[d]

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

def bit_layer_edges(layer):
    """Return 4 undirected edges (as sorted tuples) for given bit-layer (0,1,2)."""
    idx = 2 - layer  # bit_k → tuple index
    edges = []
    for v in ALL_VECS:
        w = list(v); w[idx] = 1 - w[idx]; w = tuple(w)
        if v < w:
            edges.append((v, w))
    return edges

# Q₃ adjacency
Q3_ADJ = defaultdict(set)
for v in ALL_VECS:
    for bit in range(3):
        idx = 2 - bit
        w = list(v); w[idx] = 1 - w[idx]; w = tuple(w)
        Q3_ADJ[v].add(w)

# ─── 1. Bit₀+Bit₂ Union Graph ────────────────────────────────────────────

print("=" * 80)
print("1. BIT₀+BIT₂ UNION GRAPH")
print("=" * 80)

bit0_edges = bit_layer_edges(0)
bit1_edges = bit_layer_edges(1)
bit2_edges = bit_layer_edges(2)

union_adj = defaultdict(set)
union_edges = set()
for a, b in bit0_edges + bit2_edges:
    union_adj[a].add(b)
    union_adj[b].add(a)
    union_edges.add((a, b) if a < b else (b, a))

print(f"\nbit₀ edges: {[(NAMES[a]+'─'+NAMES[b]) for a,b in bit0_edges]}")
print(f"bit₂ edges: {[(NAMES[a]+'─'+NAMES[b]) for a,b in bit2_edges]}")
print(f"Union: {len(union_edges)} edges total")

# Find connected components via BFS
visited = set()
components = []
for v in ALL_VECS:
    if v in visited:
        continue
    comp = []
    stack = [v]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        comp.append(u)
        for nb in union_adj[u]:
            if nb not in visited:
                stack.append(nb)
    components.append(comp)

print(f"\nConnected components: {len(components)}")
for ci, comp in enumerate(components):
    b1_vals = set(v[1] for v in comp)
    names = [NAMES[v] for v in sorted(comp)]
    vecs = [f"{v[0]}{v[1]}{v[2]}" for v in sorted(comp)]
    print(f"  Component {ci+1}: {names}  vectors={vecs}  b₁={b1_vals}")

# Trace cycles within each component
print("\nCycle decomposition:")
for ci, comp in enumerate(components):
    comp_set = set(comp)
    # Each vertex has degree 2 in the union graph (restricted to component)
    # So each component is a single cycle
    degrees = {v: len(union_adj[v] & comp_set) for v in comp}
    print(f"  Component {ci+1} degrees: {dict(degrees)}")
    
    # Trace the cycle
    start = sorted(comp)[0]
    cycle = [start]
    prev = None
    curr = start
    while True:
        nbs = sorted(union_adj[curr] & comp_set)
        nxt = nbs[0] if nbs[0] != prev else nbs[1]
        if nxt == start:
            break
        cycle.append(nxt)
        prev = curr
        curr = nxt
    
    cycle_names = "→".join(NAMES[v] for v in cycle) + "→" + NAMES[cycle[0]]
    # Label each edge
    edge_labels = []
    for i in range(len(cycle)):
        a, b = cycle[i], cycle[(i+1) % len(cycle)]
        edge = (min(a,b), max(a,b))
        layer = "bit₀" if edge in set(bit0_edges) else "bit₂"
        edge_labels.append(layer)
    print(f"  Cycle: {cycle_names}")
    print(f"  Edge layers: {edge_labels}")

# ─── Q₃ Hamiltonian cycles: bit₁ edge count ──────────────────────────────

print("\n--- Bit₁ edges used by Q₃ Hamiltonian cycles ---")

def find_hamiltonian_cycles():
    start = (0,0,0)
    cycles = set()
    def backtrack(path, visited):
        if len(path) == 8:
            if start in Q3_ADJ[path[-1]]:
                fwd = path
                rev = path[:1] + list(reversed(path[1:]))
                best = None
                for seq in [fwd, rev]:
                    for rot in range(8):
                        rotated = tuple(seq[rot:] + seq[:rot])
                        if best is None or rotated < best:
                            best = rotated
                cycles.add(best)
            return
        for nb in sorted(Q3_ADJ[path[-1]]):
            if nb not in visited:
                visited.add(nb)
                path.append(nb)
                backtrack(path, visited)
                path.pop()
                visited.remove(nb)
    backtrack([start], {start})
    return sorted(cycles)

q3_cycles = find_hamiltonian_cycles()
bit1_set = set((min(a,b), max(a,b)) for a,b in bit1_edges)

for ci, cycle in enumerate(q3_cycles):
    bit1_count = 0
    for i in range(8):
        a, b = cycle[i], cycle[(i+1)%8]
        edge = (min(a,b), max(a,b))
        if edge in bit1_set:
            bit1_count += 1
    names = "→".join(NAMES[v] for v in cycle) + "→" + NAMES[cycle[0]]
    # Also get 克 count for reference
    ke = sum(1 for i in range(8) if wuxing_type(WUXING_MAP[cycle[i]], WUXING_MAP[cycle[(i+1)%8]]) == "克")
    print(f"  Cycle {ci+1}: bit₁ edges = {bit1_count}, 克 = {ke}  {names}")

print("\n  Observation: every Q₃ Ham. cycle uses ≥ ? bit₁ edges (all pure 克)")
min_bit1 = min(
    sum(1 for i in range(8) if (min(c[i],c[(i+1)%8]), max(c[i],c[(i+1)%8])) in bit1_set)
    for c in q3_cycles
)
print(f"  Minimum bit₁ edges across all 6 cycles: {min_bit1}")

# ─── 2. Pure-克 Layer Count ──────────────────────────────────────────────

print("\n" + "=" * 80)
print("2. PURE-克 LAYER COUNT ACROSS 240 SURJECTIONS")
print("=" * 80)

COMP_PAIRS = [((1,1,1),(0,0,0)), ((0,1,1),(1,0,0)), ((1,0,1),(0,1,0)), ((0,0,1),(1,1,0))]
z5_comp = lambda x: (4 - x) % 5

surjections = []
for a0 in range(5):
    for a1 in range(5):
        for a2 in range(5):
            for a3 in range(5):
                fmap = {}
                for i, (v1, v2) in enumerate(COMP_PAIRS):
                    fmap[v1] = [a0,a1,a2,a3][i]
                    fmap[v2] = z5_comp([a0,a1,a2,a3][i])
                if len(set(fmap.values())) == 5:
                    surjections.append(dict(fmap))

print(f"Total surjections: {len(surjections)}")

# For each surjection, check each layer for pure-克
pure_ke_by_layer = [0, 0, 0]  # bit₀, bit₁, bit₂
has_pure_ke = 0
results = []

for fmap in surjections:
    elem_counts = Counter(fmap.values())
    partition = tuple(sorted(elem_counts.values(), reverse=True))
    
    layer_pure_ke = [False, False, False]
    for layer in range(3):
        edges = bit_layer_edges(layer)
        all_ke = all(wuxing_type(fmap[a], fmap[b]) == "克" for a, b in edges)
        layer_pure_ke[layer] = all_ke
        if all_ke:
            pure_ke_by_layer[layer] += 1
    
    any_pure = any(layer_pure_ke)
    if any_pure:
        has_pure_ke += 1
    results.append((fmap, layer_pure_ke, partition))

print(f"\nSurjections with ≥1 pure-克 layer: {has_pure_ke} / {len(surjections)}")
print(f"\nPure-克 count by layer:")
for layer in range(3):
    print(f"  bit_{layer}: {pure_ke_by_layer[layer]} surjections")

# Breakdown by partition
by_part = defaultdict(lambda: {"total": 0, "has_pure": 0, "by_layer": [0,0,0]})
for fmap, lp, part in results:
    by_part[part]["total"] += 1
    if any(lp):
        by_part[part]["has_pure"] += 1
    for layer in range(3):
        if lp[layer]:
            by_part[part]["by_layer"][layer] += 1

print(f"\nBreakdown by partition shape:")
print(f"  {'Partition':<20} {'Total':>6} {'Has pure-克':>12} {'bit₀':>6} {'bit₁':>6} {'bit₂':>6}")
for part in sorted(by_part.keys()):
    d = by_part[part]
    print(f"  {str(part):<20} {d['total']:>6} {d['has_pure']:>12} "
          f"{d['by_layer'][0]:>6} {d['by_layer'][1]:>6} {d['by_layer'][2]:>6}")

# Check canonical
canon_fmap = {VEC[n+1]: WUXING_MAP[VEC[n+1]] for n in range(8)}
for layer in range(3):
    edges = bit_layer_edges(layer)
    all_ke = all(wuxing_type(canon_fmap[a], canon_fmap[b]) == "克" for a, b in edges)
    if all_ke:
        print(f"\n  Canonical has pure-克 at bit_{layer}")
print(f"  (Canonical bit₁ = pure 克, as established in m1)")

# ─── 3. Full 8-Cycle Scan ────────────────────────────────────────────────

print("\n" + "=" * 80)
print("3. FULL 8-CYCLE SCAN (2520 distinct cycles on 8 labeled vertices)")
print("=" * 80)

# Enumerate all 8-cycles on 8 labeled vertices, up to rotation and reflection.
# An 8-cycle is a Hamiltonian cycle on K₈. Count = 7!/2 = 2520.
# We fix vertex 0 as the start, enumerate all permutations of the other 7,
# and canonicalize by direction.

vecs = list(ALL_VECS)  # 8 vertices
fixed = vecs[0]
rest = vecs[1:]

all_8cycles = set()
for perm in permutations(rest):
    cycle = (fixed,) + perm
    # Canonicalize: compare forward vs reverse, pick lexicographically smaller
    rev = (cycle[0],) + tuple(reversed(cycle[1:]))
    canon = min(cycle, rev)
    all_8cycles.add(canon)

all_8cycles = sorted(all_8cycles)
print(f"Total distinct 8-cycles: {len(all_8cycles)}")

# Compute 五行 type counts for each
ke_hist = Counter()
bihe_hist = Counter()
sheng_hist = Counter()
full_results = []

for cycle in all_8cycles:
    types = []
    for i in range(8):
        wa = WUXING_MAP[cycle[i]]
        wb = WUXING_MAP[cycle[(i+1)%8]]
        types.append(wuxing_type(wa, wb))
    counts = Counter(types)
    ke = counts.get("克", 0)
    bihe = counts.get("比和", 0)
    sheng = counts.get("生", 0)
    ke_hist[ke] += 1
    bihe_hist[bihe] += 1
    sheng_hist[sheng] += 1
    full_results.append((cycle, ke, bihe, sheng, types))

print(f"\n--- 克 count distribution ---")
for k in sorted(ke_hist.keys()):
    bar = "█" * (ke_hist[k] // 10)
    print(f"  克={k}: {ke_hist[k]:>5}  {bar}")

print(f"\n--- 比和 count distribution ---")
for k in sorted(bihe_hist.keys()):
    bar = "█" * (bihe_hist[k] // 10)
    print(f"  比和={k}: {bihe_hist[k]:>5}  {bar}")

print(f"\n--- 生 count distribution ---")
for k in sorted(sheng_hist.keys()):
    bar = "█" * (sheng_hist[k] // 10)
    print(f"  生={k}: {sheng_hist[k]:>5}  {bar}")

print(f"\nMin 克: {min(ke_hist.keys())}, Max 克: {max(ke_hist.keys())}")

# Mod-8 cycle's position — must canonicalize to start from (0,0,0) and pick min direction
mod8_vecs = tuple(VEC[i+1] for i in range(8))
# Rotate to start from (0,0,0)
start_idx = mod8_vecs.index((0,0,0))
mod8_rotated = mod8_vecs[start_idx:] + mod8_vecs[:start_idx]
mod8_rev = (mod8_rotated[0],) + tuple(reversed(mod8_rotated[1:]))
mod8_canon = min(mod8_rotated, mod8_rev)

# Find it and get 克 count
mod8_found = False
for cycle, ke, bihe, sheng, types in full_results:
    if cycle == mod8_canon:
        print(f"\nMod-8 cycle found: 克={ke}, 比和={bihe}, 生={sheng}")
        print(f"  Types: {types}")
        mod8_found = True
        break
if not mod8_found:
    print(f"\nWARNING: Mod-8 cycle not found in enumeration!")
    print(f"  mod8_canon = {mod8_canon}")

# Percentile: how many cycles have 克 ≤ 2?
le2 = sum(c for k, c in ke_hist.items() if k <= 2)
print(f"Cycles with 克 ≤ 2: {le2} / {len(all_8cycles)} = {100*le2/len(all_8cycles):.1f}%")
print(f"Mod-8 cycle's 克=2 is at the {100*le2/len(all_8cycles):.1f}th percentile (lower = fewer 克)")

# Exact count of cycles with 克=2
eq2 = ke_hist.get(2, 0)
print(f"Cycles with 克 exactly 2: {eq2}")

# ─── Complement-palindrome filter ─────────────────────────────────────────

print("\n--- Complement-palindrome cycles ---")
print("Definition: cycle (v₁→...→v₈→v₁) where complement maps vₖ ↔ v_{9-k}")
print("Requires: type(vₖ,vₖ₊₁) = type(v_{8-k},v_{9-k}) for k=1,2,3")

def complement(v):
    return tuple(1-b for b in v)

comp_palindrome_cycles = []
for cycle, ke, bihe, sheng, types in full_results:
    # Check if complement maps v_k to v_{9-k} (1-indexed, so v[k-1] ↔ v[8-k] in 0-indexed)
    # v[0] ↔ v[7] (= complement pair), v[1] ↔ v[6], v[2] ↔ v[5], v[3] ↔ v[4]
    is_comp_paired = all(complement(cycle[k]) == cycle[7-k] for k in range(4))
    if not is_comp_paired:
        continue
    
    # Check type palindrome: type of edge k→k+1 equals type of edge (7-k)→(8-k) mod 8
    # types[k] is edge from cycle[k] to cycle[(k+1)%8]
    # The "mirror" of types[k] for k=0,1,2 is types[7-k-1] = types[6-k]
    # Actually: edge k (0-indexed) connects v_k → v_{k+1}
    # Its complement-mirror connects v_{7-k} → v_{7-(k+1)} = v_{6-k}
    # That's edge index 7-k-1 = 6-k... but direction is reversed.
    # Since 五行 type is undirected (symmetric), types[k] should equal types[6-k]
    # for k=0,1,2 (3 pairs: 0↔6, 1↔5, 2↔4, and 3↔7 wraps to edge 7→0 = types[7])
    # Edge 3: v₃→v₄. Mirror: v₄→v₃ = same edge. So types[3] is self-mirrored.
    # Edge 7: v₇→v₀. Mirror: v₀→v₇ = same edge (reversed). So types[7] is self-mirrored.
    # Pairs to check: (0,6), (1,5), (2,4). And types[3], types[7] are free.
    
    is_type_palindrome = all(types[k] == types[6-k] for k in range(3))
    
    comp_palindrome_cycles.append((cycle, ke, bihe, sheng, types, is_type_palindrome))

print(f"\nCycles with complement-pair structure (v_k ↔ v_{{9-k}} complements): {len(comp_palindrome_cycles)}")

if comp_palindrome_cycles:
    # Subset that also has type palindrome
    type_pal = [x for x in comp_palindrome_cycles if x[5]]
    print(f"  Of those, with type palindrome: {len(type_pal)}")
    
    print(f"\n  All complement-paired cycles:")
    ke_hist_cp = Counter()
    for cycle, ke, bihe, sheng, types, tp in comp_palindrome_cycles:
        ke_hist_cp[ke] += 1
        names = "→".join(NAMES[v] for v in cycle) + "→" + NAMES[cycle[0]]
        tp_mark = " [type-pal]" if tp else ""
        print(f"    克={ke} 比={bihe} 生={sheng}  {types}{tp_mark}")
        print(f"      {names}")
    
    print(f"\n  克 distribution (complement-paired):")
    for k in sorted(ke_hist_cp.keys()):
        print(f"    克={k}: {ke_hist_cp[k]}")
    
    # Check if mod-8 is among them — need to compare canonical forms
    # The comp_palindrome_cycles store the cycle as enumerated (starting from (0,0,0))
    is_mod8_comp = any(c == mod8_canon for c, *_ in comp_palindrome_cycles)
    print(f"\n  Mod-8 cycle is complement-paired? {is_mod8_comp}")
    if not is_mod8_comp:
        # Manual verification
        print(f"  Manual check: mod-8 = {[NAMES[v] for v in mod8_canon]}")
        for c, ke2, bihe2, sheng2, types2, tp2 in comp_palindrome_cycles:
            if ke2 == 2 and bihe2 == 3:
                print(f"  Candidate match: {[NAMES[v] for v in c]}, 克={ke2}")
                print(f"    Same as mod-8? {set(zip(c, c[1:]+(c[0],))) == set(zip(mod8_canon, mod8_canon[1:]+(mod8_canon[0],))) or set(zip(c, c[1:]+(c[0],))) == set(zip(reversed(mod8_canon), list(reversed(mod8_canon))[1:]+(list(reversed(mod8_canon))[0],)))}")
else:
    print("  None found.")

# ─── Summary statistics ───────────────────────────────────────────────────

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
mean_ke = sum(ke * c for ke, c in ke_hist.items()) / len(all_8cycles)
print(f"Mean 克 across all 2520 cycles: {mean_ke:.3f}")
print(f"Mod-8 cycle 克=2 vs mean={mean_ke:.3f}")

# Expected from baseline: 13 克 pairs out of 28. For 8-cycle (8 edges out of 28):
# Expected 克 per cycle = 8 * 13/28 = 3.714
print(f"Expected 克 per random 8-cycle (null model): 8 × 13/28 = {8*13/28:.3f}")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
