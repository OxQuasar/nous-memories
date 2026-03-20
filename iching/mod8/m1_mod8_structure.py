#!/usr/bin/env python3
"""Mod-8 structure investigation: trigram combinatorics on Q₃ with 五行 overlay."""

from itertools import combinations, permutations
from collections import Counter

# ─── Definitions ───────────────────────────────────────────────────────────

XIANTIAN = [  # 先天 ordering: (position 1-indexed, name, F₂³ as tuple)
    (1, "乾", (1,1,1)),
    (2, "兌", (0,1,1)),
    (3, "離", (1,0,1)),
    (4, "震", (0,0,1)),
    (5, "巽", (1,1,0)),
    (6, "坎", (0,1,0)),
    (7, "艮", (1,0,0)),
    (8, "坤", (0,0,0)),
]

NAMES = {v: name for _, name, v in XIANTIAN}
POS   = {v: pos  for pos, _, v in XIANTIAN}
VEC   = {pos: v  for pos, _, v in XIANTIAN}
NAME_BY_POS = {pos: name for pos, name, _ in XIANTIAN}

def vec_to_dec(v):
    return v[0]*4 + v[1]*2 + v[2]

def complement(v):
    return tuple(1-b for b in v)

# 五行 assignment: F₂³ → Z₅
WUXING_MAP = {
    (1,1,1): 0, (0,1,1): 0,  # Metal
    (0,1,0): 1,               # Water
    (0,0,1): 2, (1,1,0): 2,  # Wood
    (1,0,1): 3,               # Fire
    (0,0,0): 4, (1,0,0): 4,  # Earth
}

Z5_NAMES = {0: "Metal", 1: "Water", 2: "Wood", 3: "Fire", 4: "Earth"}

def wuxing_distance(a, b):
    d = abs(a - b)
    return min(d, 5 - d)

def wuxing_type(a, b):
    d = wuxing_distance(a, b)
    return {0: "比和", 1: "生", 2: "克"}[d]

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

def xor_vec(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

# ─── 1. Foundation Table ──────────────────────────────────────────────────

print("=" * 80)
print("1. FOUNDATION TABLE")
print("=" * 80)
print(f"{'Pos':>3} {'Name':>4} {'F₂³':>7} {'Dec':>3} {'Element':>7} {'Z₅':>2} │ {'Comp Pos':>8} {'Comp Name':>9}")
print("─" * 60)
for pos, name, v in XIANTIAN:
    c = complement(v)
    comp_pos = POS[c]
    comp_name = NAMES[c]
    wx = WUXING_MAP[v]
    print(f"{pos:>3} {name:>4} {v[0]}{v[1]}{v[2]:>5} {vec_to_dec(v):>3} {Z5_NAMES[wx]:>7} {wx:>2} │ {comp_pos:>8} {comp_name:>9}")

# ─── 2. Bit-Layer 五行 Decomposition ──────────────────────────────────────

print("\n" + "=" * 80)
print("2. BIT-LAYER 五行 DECOMPOSITION")
print("=" * 80)

ALL_VECS = [(b2,b1,b0) for b2 in range(2) for b1 in range(2) for b0 in range(2)]

for layer in range(3):
    layer_name = f"bit_{layer} (b₂b₁b₀ position {2-layer})"
    print(f"\n--- Layer: {layer_name} ---")
    edges = []
    for v in ALL_VECS:
        # flip bit at position (2-layer) from MSB, i.e. index `layer` in our (b2,b1,b0) tuple
        # Actually: bit_0 means b₀ (rightmost), bit_1 means b₁, bit_2 means b₂
        # In our tuple (b₂,b₁,b₀), index 0=b₂, index 1=b₁, index 2=b₀
        # So bit_k flips index (2-k)
        idx = 2 - layer  # bit_0 → idx 2, bit_1 → idx 1, bit_2 → idx 0
        w = list(v)
        w[idx] = 1 - w[idx]
        w = tuple(w)
        if v < w:  # avoid duplicates
            edges.append((v, w))
    
    counts = Counter()
    print(f"  {'Edge':>20} {'WX_a':>7} {'WX_b':>7} {'Type':>4}")
    for a, b in edges:
        wa, wb = WUXING_MAP[a], WUXING_MAP[b]
        t = wuxing_type(wa, wb)
        counts[t] += 1
        print(f"  {NAMES[a]}({a[0]}{a[1]}{a[2]})─{NAMES[b]}({b[0]}{b[1]}{b[2]})"
              f"  {Z5_NAMES[wa]:>7} {Z5_NAMES[wb]:>7} {t:>4}")
    print(f"  Counts: 比和={counts['比和']}, 生={counts['生']}, 克={counts['克']}")

print("\n  PREDICTION CHECK:")
print("  bit₂ = {2比和, 2生, 0克} ?")
print("  bit₁ = {0, 0, 4克} ?")
print("  bit₀ = {0, 2生, 2克} ?")

# ─── 3. Mod-8 Cycle Type Sequence ────────────────────────────────────────

print("\n" + "=" * 80)
print("3. MOD-8 CYCLE TYPE SEQUENCE (1→2→3→4→5→6→7→8→1)")
print("=" * 80)

cycle_types = []
print(f"{'Step':>4} {'Src':>4}{'→Dst':>5} {'SrcVec':>7}{'→DstVec':>8} {'XOR':>5} {'Ham':>3} {'WX_src':>7}{'→WX_dst':>8} {'Type':>4}")
print("─" * 75)
for i in range(8):
    src_pos = i + 1
    dst_pos = (i + 1) % 8 + 1  # next in cycle, wrapping 8→1
    sv, dv = VEC[src_pos], VEC[dst_pos]
    xv = xor_vec(sv, dv)
    hd = hamming(sv, dv)
    ws, wd = WUXING_MAP[sv], WUXING_MAP[dv]
    t = wuxing_type(ws, wd)
    cycle_types.append(t)
    print(f"{i+1:>4} {NAME_BY_POS[src_pos]:>4}→{NAME_BY_POS[dst_pos]:<4} "
          f"{sv[0]}{sv[1]}{sv[2]:>5}→{dv[0]}{dv[1]}{dv[2]:<5} "
          f"{xv[0]}{xv[1]}{xv[2]:>3} {hd:>3} "
          f"{Z5_NAMES[ws]:>7}→{Z5_NAMES[wd]:<7} {t:>4}")

counts = Counter(cycle_types)
print(f"\nType sequence: {cycle_types}")
print(f"Counts: 比和={counts['比和']}, 生={counts['生']}, 克={counts['克']}")
print(f"Palindromic? {cycle_types == cycle_types[::-1]}")
print(f"PREDICTION: {{比和, 克, 生, 比和, 生, 克, 比和, 生}}, counts={{3,3,2}}")

# Check: all d=1 steps
d1_steps = [(i, cycle_types[i]) for i in range(8) if hamming(VEC[i+1], VEC[(i+1)%8+1]) == 1]
print(f"\nAll d=1 steps: {d1_steps}")
d1_ke = any(t == "克" for _, t in d1_steps)
print(f"Any d=1 step is 克? {d1_ke}")
print(f"All d=1 XOR masks:")
for i in range(8):
    sv, dv = VEC[i+1], VEC[(i+1)%8+1]
    if hamming(sv, dv) == 1:
        print(f"  Step {i+1}: XOR = {xor_vec(sv, dv)}")

# ─── 4. Gray Code Comparison ─────────────────────────────────────────────

print("\n" + "=" * 80)
print("4. GRAY CODE COMPARISON")
print("=" * 80)

GRAY = [(0,0,0),(0,0,1),(0,1,1),(0,1,0),(1,1,0),(1,1,1),(1,0,1),(1,0,0)]

gray_types = []
print(f"{'Step':>4} {'Src':>4}{'→Dst':>5} {'SrcVec':>7}{'→DstVec':>8} {'Ham':>3} {'Type':>4}")
print("─" * 50)
for i in range(8):
    sv = GRAY[i]
    dv = GRAY[(i+1) % 8]
    hd = hamming(sv, dv)
    ws, wd = WUXING_MAP[sv], WUXING_MAP[dv]
    t = wuxing_type(ws, wd)
    gray_types.append(t)
    print(f"{i+1:>4} {NAMES[sv]:>4}→{NAMES[dv]:<4} "
          f"{sv[0]}{sv[1]}{sv[2]:>5}→{dv[0]}{dv[1]}{dv[2]:<5} {hd:>3} {t:>4}")

counts = Counter(gray_types)
print(f"\nType sequence: {gray_types}")
print(f"Counts: 比和={counts['比和']}, 生={counts['生']}, 克={counts['克']}")
print(f"All Hamming distances = 1? {all(hamming(GRAY[i], GRAY[(i+1)%8]) == 1 for i in range(8))}")
print(f"PREDICTION: 克-dominated (4 克 out of 8)")

# ─── 5. All Q₃ Hamiltonian Cycles ────────────────────────────────────────

print("\n" + "=" * 80)
print("5. ALL Q₃ HAMILTONIAN CYCLES")
print("=" * 80)

# Build adjacency for Q₃
adj = {v: [] for v in ALL_VECS}
for v in ALL_VECS:
    for bit in range(3):
        idx = 2 - bit  # bit_k → tuple index (2-k)
        w = list(v)
        w[idx] = 1 - w[idx]
        adj[v].append(tuple(w))

def find_hamiltonian_cycles():
    """Find all Hamiltonian cycles on Q₃, canonical form: min rotation, smaller direction."""
    start = (0,0,0)
    cycles = set()
    
    def backtrack(path, visited):
        if len(path) == 8:
            # Check if last connects to start
            if start in adj[path[-1]]:
                # Canonicalize: try all rotations and both directions
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
        
        for nb in sorted(adj[path[-1]]):
            if nb not in visited:
                visited.add(nb)
                path.append(nb)
                backtrack(path, visited)
                path.pop()
                visited.remove(nb)
    
    backtrack([start], {start})
    return sorted(cycles)

all_cycles = find_hamiltonian_cycles()
print(f"Found {len(all_cycles)} distinct Hamiltonian cycles (up to start vertex & direction)\n")

mod8_cycle_vecs = tuple(VEC[i+1] for i in range(8))
# Canonicalize mod8 cycle same way
def canonicalize(cycle):
    fwd = list(cycle)
    rev = fwd[:1] + list(reversed(fwd[1:]))
    best = None
    for seq in [fwd, rev]:
        for rot in range(len(seq)):
            rotated = tuple(seq[rot:] + seq[:rot])
            if best is None or rotated < best:
                best = rotated
    return best

mod8_canon = canonicalize(mod8_cycle_vecs)

for ci, cycle in enumerate(all_cycles):
    types = []
    for i in range(8):
        wa = WUXING_MAP[cycle[i]]
        wb = WUXING_MAP[cycle[(i+1)%8]]
        types.append(wuxing_type(wa, wb))
    
    counts = Counter(types)
    is_mod8 = (cycle == mod8_canon)
    
    names_str = "→".join(NAMES[v] for v in cycle) + "→" + NAMES[cycle[0]]
    hams = [hamming(cycle[i], cycle[(i+1)%8]) for i in range(8)]
    
    marker = " ← MOD-8 CYCLE" if is_mod8 else ""
    print(f"Cycle {ci+1}: {names_str}")
    print(f"  Hamming distances: {hams}")
    print(f"  五行 types: {types}")
    print(f"  Counts: 比和={counts['比和']}, 生={counts['生']}, 克={counts['克']}{marker}")
    print()

print("Summary: 克 counts across all cycles:")
ke_counts = []
for cycle in all_cycles:
    types = []
    for i in range(8):
        wa = WUXING_MAP[cycle[i]]
        wb = WUXING_MAP[cycle[(i+1)%8]]
        types.append(wuxing_type(wa, wb))
    ke_counts.append(Counter(types)["克"])
print(f"  克 counts: {sorted(ke_counts)}")
print(f"  All cycles have 克 ≥ 3? {all(k >= 3 for k in ke_counts)}")
print(f"  Min 克: {min(ke_counts)}, Max 克: {max(ke_counts)}")

# ─── 6. Cyclic Shift Analysis ────────────────────────────────────────────

print("\n" + "=" * 80)
print("6. CYCLIC SHIFT ANALYSIS (S_k on 0-indexed positions)")
print("=" * 80)

# S_k: position n ↦ (n+k) mod 8 (0-indexed)
# This permutes trigrams. We ask: does it preserve 五行 pair types?

# All 28 unordered pairs of trigrams
all_pairs = list(combinations(range(8), 2))  # pairs of 0-indexed positions

# Baseline: 五行 types of all 28 pairs
baseline_types = {}
for i, j in all_pairs:
    vi, vj = VEC[i+1], VEC[j+1]
    baseline_types[(i,j)] = wuxing_type(WUXING_MAP[vi], WUXING_MAP[vj])

print(f"\nBaseline pair type counts: {Counter(baseline_types.values())}")

for k in range(8):
    # S_k maps position i → (i+k) mod 8
    # So trigram at position i gets sent to position (i+k) mod 8
    # Equivalently: the trigram that WAS at position i is now "labeled" by position (i+k) mod 8
    # For pair analysis: pair (i,j) maps to pair ((i+k)%8, (j+k)%8)
    # The TRIGRAMS at positions i,j don't change — it's which positions we're looking at that changes
    # 
    # Actually the question is: S_k is a permutation of trigrams.
    # S_k sends trigram at 先天 position n to... 
    # Let me re-read: "S_k: n ↦ (n+k) mod 8 on positions {0,...,7}"
    # So S_k permutes positions. The trigram at position n gets moved to position (n+k) mod 8.
    # For pair types: we compare pairs of trigrams. The pair (trig_i, trig_j) has a 五行 type.
    # Under S_k, position i holds the trigram that USED to be at position (i-k) mod 8.
    # So the new pair at positions (i,j) is (trig_{(i-k)%8}, trig_{(j-k)%8}).
    # That's just a relabeling of positions — the SET of all 28 pairs of trigrams doesn't change!
    # 
    # I think the intent is different. S_k is a MAP on trigrams: it sends the trigram at position n
    # to the trigram at position (n+k) mod 8. So each trigram v gets mapped to some other trigram S_k(v).
    # Then for a pair (v, w), we ask: does wuxing_type(S_k(v), S_k(w)) == wuxing_type(v, w)?
    
    # Build S_k as a map on F₂³
    sk_map = {}
    for n in range(8):
        src_vec = VEC[n+1]  # 1-indexed
        dst_pos = (n + k) % 8  # 0-indexed result
        dst_vec = VEC[dst_pos + 1]  # back to 1-indexed for VEC lookup
        # Wait: S_k sends position n (0-indexed) to position (n+k) mod 8
        # The trigram at position n is VEC[n+1]. S_k sends it to... 
        # S_k is a permutation of positions. The trigram at position n is mapped to 
        # the trigram at position (n+k) mod 8.
        # So S_k(VEC[n+1]) = VEC[((n+k) % 8) + 1]
        sk_map[src_vec] = dst_vec
    
    # Count how many pairs change type
    changed = 0
    for i, j in all_pairs:
        vi, vj = VEC[i+1], VEC[j+1]
        orig_type = wuxing_type(WUXING_MAP[vi], WUXING_MAP[vj])
        new_type = wuxing_type(WUXING_MAP[sk_map[vi]], WUXING_MAP[sk_map[vj]])
        if orig_type != new_type:
            changed += 1
    
    # Induced permutation on 五行 elements
    elem_map = {}
    for n in range(8):
        sv = VEC[n+1]
        dv = sk_map[sv]
        e_src = WUXING_MAP[sv]
        e_dst = WUXING_MAP[dv]
        if e_src not in elem_map:
            elem_map[e_src] = set()
        elem_map[e_src].add(e_dst)
    
    # Check if it's a well-defined function on elements
    well_defined = all(len(v) == 1 for v in elem_map.values())
    
    elem_str = ", ".join(f"{Z5_NAMES[k2]}→{Z5_NAMES[list(v)[0]]}" if len(v)==1 
                         else f"{Z5_NAMES[k2]}→{{{','.join(Z5_NAMES[x] for x in sorted(v))}}}"
                         for k2, v in sorted(elem_map.items()))
    
    print(f"\n  S_{k}: pairs changed = {changed}/28, element map well-defined = {well_defined}")
    print(f"    Element map: {elem_str}")
    
    # Show the permutation on trigrams
    perm_str = ", ".join(f"{NAMES[VEC[n+1]]}→{NAMES[sk_map[VEC[n+1]]]}" for n in range(8))
    print(f"    Trigram perm: {perm_str}")

# ─── 7. All Complement-Respecting Surjections ────────────────────────────

print("\n" + "=" * 80)
print("7. ALL COMPLEMENT-RESPECTING SURJECTIONS F₂³ → Z₅")
print("=" * 80)

# Complement pairs in F₂³:
# {111,000}, {011,100}, {101,010}, {001,110}
COMP_PAIRS = [((1,1,1),(0,0,0)), ((0,1,1),(1,0,0)), ((1,0,1),(0,1,0)), ((0,0,1),(1,1,0))]

# NOTE: The captain's task stated x ↦ (5-x) mod 5 (fixes 0, swaps 1↔4, 2↔3).
# But the canonical 五行 assignment uses x ↦ (4-x) mod 5 (swaps 0↔4, 1↔3, fixes 2).
# Verification: canonical pairs (Metal=0,Earth=4), (Fire=3,Water=1), (Wood=2,Wood=2)
#   (4-0)%5=4 ✓, (4-3)%5=1 ✓, (4-2)%5=2 ✓
# We enumerate under BOTH involutions and compare.

def enumerate_surjections(z5_comp_fn, label):
    """Enumerate complement-respecting surjections under given Z₅ involution."""
    results = []
    for a0 in range(5):
        for a1 in range(5):
            for a2 in range(5):
                for a3 in range(5):
                    assignments = [a0, a1, a2, a3]
                    fmap = {}
                    for i, (v1, v2) in enumerate(COMP_PAIRS):
                        fmap[v1] = assignments[i]
                        fmap[v2] = z5_comp_fn(assignments[i])
                    if len(set(fmap.values())) == 5:
                        results.append(dict(fmap))
    return results

inv_neg = lambda x: (5 - x) % 5   # fixes 0, swaps 1↔4, 2↔3
inv_4mx = lambda x: (4 - x) % 5   # fixes 2, swaps 0↔4, 1↔3

surj_neg = enumerate_surjections(inv_neg, "x↦-x")
surj_4mx = enumerate_surjections(inv_4mx, "x↦4-x")

print(f"\nInvolution x ↦ (5-x)%5 [fixes 0, swaps 1↔4, 2↔3]: {len(surj_neg)} surjections")
print(f"Involution x ↦ (4-x)%5 [fixes 2, swaps 0↔4, 1↔3]: {len(surj_4mx)} surjections")

# Check which contains the canonical
canonical_tuple = tuple(WUXING_MAP[VEC[n+1]] for n in range(8))
canon_dict = {VEC[n+1]: WUXING_MAP[VEC[n+1]] for n in range(8)}
in_neg = any(all(f[v] == canon_dict[v] for v in canon_dict) for f in surj_neg)
in_4mx = any(all(f[v] == canon_dict[v] for v in canon_dict) for f in surj_4mx)
print(f"\nCanonical {canonical_tuple} in x↦(5-x)%5 set? {in_neg}")
print(f"Canonical {canonical_tuple} in x↦(4-x)%5 set? {in_4mx}")

# Use the CORRECT involution (4-x)%5 for the main analysis
valid_surjections = surj_4mx
print(f"\n>>> Using x ↦ (4-x)%5 for all analysis below (matches canonical) <<<")

print(f"Total complement-respecting surjections: {len(valid_surjections)}")

# For each, compute bit-layer decomposition
print(f"\n{'#':>3} {'Assignment (乾兌離震巽坎艮坤)':>35} {'bit₂ (比生克)':>15} {'bit₁ (比生克)':>15} {'bit₀ (比生克)':>15} {'克-free layer?':>15}")
print("─" * 105)

ke_free_count = 0
results = []

for si, fmap in enumerate(valid_surjections):
    # Assignment string
    assign_str = " ".join(f"{Z5_NAMES[fmap[VEC[n+1]]][:2]}" for n in range(8))
    
    # Partition shape: count how many trigrams map to each element
    elem_counts = Counter(fmap.values())
    partition = tuple(sorted(elem_counts.values(), reverse=True))
    
    layer_results = []
    has_ke_free = False
    for layer in range(3):
        idx = 2 - layer
        edges = []
        for v in ALL_VECS:
            w = list(v)
            w[idx] = 1 - w[idx]
            w = tuple(w)
            if v < w:
                edges.append((v, w))
        
        counts = Counter()
        for a, b in edges:
            t = wuxing_type(fmap[a], fmap[b])
            counts[t] += 1
        layer_results.append((counts.get("比和",0), counts.get("生",0), counts.get("克",0)))
        if counts.get("克", 0) == 0:
            has_ke_free = True
    
    if has_ke_free:
        ke_free_count += 1
    
    results.append((fmap, layer_results, has_ke_free, partition))

# Group by partition shape
from collections import defaultdict
by_partition = defaultdict(list)
for fmap, layers, has_kf, partition in results:
    by_partition[partition].append((fmap, layers, has_kf))

print(f"\nResults grouped by partition shape:")
for partition in sorted(by_partition.keys()):
    items = by_partition[partition]
    kf_count = sum(1 for _, _, kf in items if kf)
    print(f"\n  Partition {partition}: {len(items)} surjections, {kf_count} with ≥1 克-free layer")
    
    for fi, (fmap, layers, has_kf) in enumerate(items):
        assign = [fmap[VEC[n+1]] for n in range(8)]
        assign_names = [Z5_NAMES[a][:2] for a in assign]
        layer_strs = [f"({b},{s},{k})" for b, s, k in layers]
        kf_mark = "✓" if has_kf else " "
        print(f"    [{','.join(str(a) for a in assign)}] "
              f"bit₂={layer_strs[2]} bit₁={layer_strs[1]} bit₀={layer_strs[0]}  {kf_mark}")

print(f"\n  TOTAL with ≥1 克-free bit-layer: {ke_free_count} / {len(valid_surjections)}")

# Check: is the canonical assignment in the list?
canonical = tuple(WUXING_MAP[VEC[n+1]] for n in range(8))
print(f"\n  Canonical assignment: {canonical}")
for fmap, layers, has_kf, partition in results:
    assign = tuple(fmap[VEC[n+1]] for n in range(8))
    if assign == canonical:
        layer_strs = [f"({b},{s},{k})" for b, s, k in layers]
        print(f"  Found canonical: bit₂={layer_strs[2]} bit₁={layer_strs[1]} bit₀={layer_strs[0]}, "
              f"克-free layer: {has_kf}, partition: {partition}")
        break

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
