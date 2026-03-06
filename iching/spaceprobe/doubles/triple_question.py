"""
The 52-triple question: Is the traditional triple {ι₁, ι₂, ι₃} distinguished
among the 52 minimal FPF-generating triples within S₄?

The traditional triple has sub-pair orders {4, 6, 8} (orders of ι₁∘ι₂, ι₁∘ι₃, ι₂∘ι₃).
Is this signature unique? What signatures do the other 51 triples have?
"""

from itertools import combinations
from collections import Counter, defaultdict

N = 8

# ══════════════════════════════════════════════════════════════════════════════
# Build the traditional S₄
# ══════════════════════════════════════════════════════════════════════════════

# The traditional block system on {0,...,7}:
# We need to pick a specific S₄ on 8 elements with 4 blocks of 2.
# Use the traditional trigram encoding:
# Block 0: {Kan(010=2), Li(101=5)}
# Block 1: {Kun(000=0), Gen(001=1)}
# Block 2: {Zhen(100=4), Dui(110=6)}
# Block 3: {Xun(011=3), Qian(111=7)}

BLOCKS = [(2, 5), (0, 1), (4, 6), (3, 7)]

# Traditional involutions:
# ι₁ (Fu Xi complement): XOR with 7 → 0↔7, 1↔6, 2↔5, 3↔4
iota1 = {0: 7, 7: 0, 1: 6, 6: 1, 2: 5, 5: 2, 3: 4, 4: 3}

# ι₂ (Lo Shu diametric): swap within blocks → 2↔5, 0↔1, 4↔6, 3↔7
iota2 = {2: 5, 5: 2, 0: 1, 1: 0, 4: 6, 6: 4, 3: 7, 7: 3}

# ι₃ (He Tu): 2↔7, 0↔6, 4↔1, 3↔5
iota3 = {2: 7, 7: 2, 0: 6, 6: 0, 4: 1, 1: 4, 3: 5, 5: 3}

def compose(p1, p2):
    return {k: p2[p1[k]] for k in p1}

def to_tuple(p):
    return tuple(p[i] for i in range(N))

def perm_order(perm):
    current = dict(perm)
    identity = {k: k for k in perm}
    for i in range(1, 100):
        if current == identity:
            return i
        current = compose(current, perm)
    return -1

# Verify traditional sub-pair orders
o12 = perm_order(compose(iota1, iota2))
o13 = perm_order(compose(iota1, iota3))
o23 = perm_order(compose(iota2, iota3))
print(f"Traditional triple sub-pair orders: {{{o12}, {o13}, {o23}}}")
print(f"  ι₁∘ι₂ order: {o12}")
print(f"  ι₁∘ι₃ order: {o13}")
print(f"  ι₂∘ι₃ order: {o23}")

# ══════════════════════════════════════════════════════════════════════════════
# Generate the full S₄ group
# ══════════════════════════════════════════════════════════════════════════════

def group_generated_by(gens):
    identity = tuple(range(N))
    group = {identity}
    queue = [to_tuple(g) for g in gens]
    group.update(queue)
    while queue:
        new = []
        for g in queue:
            g_dict = {i: g[i] for i in range(N)}
            for gen in gens:
                prod = tuple(gen[g[i]] for i in range(N))
                if prod not in group:
                    group.add(prod)
                    new.append(prod)
                prod2 = tuple(g[gen[i]] for i in range(N))
                if prod2 not in group:
                    group.add(prod2)
                    new.append(prod2)
        queue = new
    return group

S4 = group_generated_by([iota1, iota2, iota3])
print(f"\n|S₄| = {len(S4)}")

# ══════════════════════════════════════════════════════════════════════════════
# Find all FPF involutions in this S₄
# ══════════════════════════════════════════════════════════════════════════════

identity = tuple(range(N))

fpf_involutions = []
for perm in S4:
    if perm == identity:
        continue
    perm_dict = {i: perm[i] for i in range(N)}
    # Check involution (order 2)
    if all(perm[perm[i]] == i for i in range(N)):
        # Check FPF
        if all(perm[i] != i for i in range(N)):
            fpf_involutions.append(perm_dict)

print(f"FPF involutions in S₄: {len(fpf_involutions)}")

# Show them
for inv in fpf_involutions:
    pairs = []
    seen = set()
    for x in sorted(inv.keys()):
        if x not in seen:
            pairs.append(f"{x}↔{inv[x]}")
            seen.add(x)
            seen.add(inv[x])
    print(f"  {', '.join(pairs)}")

# ══════════════════════════════════════════════════════════════════════════════
# Find all minimal FPF-generating triples
# ══════════════════════════════════════════════════════════════════════════════

print(f"\nChecking all {len(fpf_involutions)}C3 = "
      f"{len(fpf_involutions)*(len(fpf_involutions)-1)*(len(fpf_involutions)-2)//6} triples...")

generating_triples = []
for i, a in enumerate(fpf_involutions):
    for j, b in enumerate(fpf_involutions):
        if j <= i:
            continue
        for k, c in enumerate(fpf_involutions):
            if k <= j:
                continue
            grp = group_generated_by([a, b, c])
            if len(grp) == 24:  # generates full S₄
                generating_triples.append((a, b, c))

print(f"FPF triples generating S₄: {len(generating_triples)}")

# Check minimality: remove any one generator and it no longer generates S₄
minimal_triples = []
for a, b, c in generating_triples:
    g_ab = group_generated_by([a, b])
    g_ac = group_generated_by([a, c])
    g_bc = group_generated_by([b, c])
    if len(g_ab) < 24 and len(g_ac) < 24 and len(g_bc) < 24:
        minimal_triples.append((a, b, c))

print(f"Minimal FPF-generating triples: {len(minimal_triples)}")

# ══════════════════════════════════════════════════════════════════════════════
# Classify by sub-pair order signature
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"SUB-PAIR ORDER SIGNATURES")
print(f"{'=' * 70}")

sig_groups = defaultdict(list)
for a, b, c in minimal_triples:
    o_ab = perm_order(compose(a, b))
    o_ac = perm_order(compose(a, c))
    o_bc = perm_order(compose(b, c))
    sig = tuple(sorted([o_ab, o_ac, o_bc]))
    sig_groups[sig].append((a, b, c))

for sig, triples in sorted(sig_groups.items()):
    print(f"\n  Signature {sig}: {len(triples)} triples")

# Check if the traditional triple's signature is unique
trad_sig = tuple(sorted([o12, o13, o23]))
print(f"\n  Traditional signature: {trad_sig}")
print(f"  Count with this signature: {len(sig_groups[trad_sig])}")
print(f"  Unique signature? {len(sig_groups) == len(minimal_triples)}")

# ══════════════════════════════════════════════════════════════════════════════
# Classify by overlap pattern
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"OVERLAP PATTERNS AMONG MINIMAL TRIPLES")
print(f"{'=' * 70}")

def overlap(inv1, inv2):
    def pairs(inv):
        return {frozenset([a, b]) for a, b in inv.items() if a < b}
    return len(pairs(inv1) & pairs(inv2))

def commutes(i1, i2):
    return compose(i1, i2) == compose(i2, i1)

overlap_groups = defaultdict(list)
for a, b, c in minimal_triples:
    ov = tuple(sorted([overlap(a, b), overlap(a, c), overlap(b, c)]))
    overlap_groups[ov].append((a, b, c))

for ov, triples in sorted(overlap_groups.items()):
    # Check commutation patterns
    comm_patterns = Counter()
    for a, b, c in triples:
        comms = sorted([
            commutes(a, b), commutes(a, c), commutes(b, c)
        ])
        comm_patterns[tuple(comms)] += 1
    
    print(f"\n  Overlap {ov}: {len(triples)} triples")
    for cp, count in sorted(comm_patterns.items()):
        print(f"    Commutation {cp}: {count}")

# ══════════════════════════════════════════════════════════════════════════════
# Cross-classify: overlap × signature
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"CROSS-CLASSIFICATION: OVERLAP × SIGNATURE")
print(f"{'=' * 70}")

cross = defaultdict(int)
for a, b, c in minimal_triples:
    ov = tuple(sorted([overlap(a, b), overlap(a, c), overlap(b, c)]))
    o_ab = perm_order(compose(a, b))
    o_ac = perm_order(compose(a, c))
    o_bc = perm_order(compose(b, c))
    sig = tuple(sorted([o_ab, o_ac, o_bc]))
    cross[(ov, sig)] += 1

for (ov, sig), count in sorted(cross.items()):
    trad = " ← TRADITIONAL" if ov == (0, 0, 1) and sig == trad_sig else ""
    print(f"  overlap={ov}, signature={sig}: {count}{trad}")

# ══════════════════════════════════════════════════════════════════════════════
# The traditional triple specifically
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"THE TRADITIONAL TRIPLE IN CONTEXT")
print(f"{'=' * 70}")

# Which overlap+commutation+signature class does the traditional triple sit in?
trad_ov = tuple(sorted([overlap(iota1, iota2), overlap(iota1, iota3), overlap(iota2, iota3)]))
trad_comm = tuple(sorted([commutes(iota1, iota2), commutes(iota1, iota3), commutes(iota2, iota3)]))

print(f"  Overlap pattern: {trad_ov}")
print(f"  Commutation pattern: {trad_comm}")
print(f"  Sub-pair order signature: {trad_sig}")

# How many triples share ALL three properties?
matching = 0
for a, b, c in minimal_triples:
    ov = tuple(sorted([overlap(a, b), overlap(a, c), overlap(b, c)]))
    comms = tuple(sorted([commutes(a, b), commutes(a, c), commutes(b, c)]))
    o_ab = perm_order(compose(a, b))
    o_ac = perm_order(compose(a, c))
    o_bc = perm_order(compose(b, c))
    sig = tuple(sorted([o_ab, o_ac, o_bc]))
    
    if ov == trad_ov and comms == trad_comm and sig == trad_sig:
        matching += 1

print(f"  Triples matching all three: {matching}/{len(minimal_triples)}")

# Is the traditional triple in the same conjugacy class as others with the same properties?
# Two triples are conjugate if there's a group element mapping one to the other.
# Check: among the matching triples, how many conjugacy classes?
print(f"\n  Checking conjugacy classes among matching triples...")

matching_triples = []
for a, b, c in minimal_triples:
    ov = tuple(sorted([overlap(a, b), overlap(a, c), overlap(b, c)]))
    comms = tuple(sorted([commutes(a, b), commutes(a, c), commutes(b, c)]))
    o_ab = perm_order(compose(a, b))
    o_ac = perm_order(compose(a, c))
    o_bc = perm_order(compose(b, c))
    sig = tuple(sorted([o_ab, o_ac, o_bc]))
    
    if ov == trad_ov and comms == trad_comm and sig == trad_sig:
        matching_triples.append((a, b, c))

# Two triples (a,b,c) and (a',b',c') are conjugate if exists g in S₄ such that
# g∘a∘g⁻¹ = a', g∘b∘g⁻¹ = b', g∘c∘g⁻¹ = c' (for some permutation of generators)
def conjugate(g_dict, inv):
    """Compute g ∘ inv ∘ g⁻¹"""
    g_inv = {v: k for k, v in g_dict.items()}
    result = {}
    for x in range(N):
        result[x] = g_dict[inv[g_inv[x]]]
    return result

classes = []
assigned = set()
for i, (a, b, c) in enumerate(matching_triples):
    if i in assigned:
        continue
    current_class = [i]
    assigned.add(i)
    
    a_t, b_t, c_t = to_tuple(a), to_tuple(b), to_tuple(c)
    triple_set = {a_t, b_t, c_t}
    
    for j, (a2, b2, c2) in enumerate(matching_triples):
        if j in assigned:
            continue
        # Check if any g maps {a,b,c} to {a2,b2,c2} (as unordered set)
        found = False
        for g_perm in S4:
            g_dict = {i: g_perm[i] for i in range(N)}
            ca = to_tuple(conjugate(g_dict, a))
            cb = to_tuple(conjugate(g_dict, b))
            cc = to_tuple(conjugate(g_dict, c))
            conj_set = {ca, cb, cc}
            target_set = {to_tuple(a2), to_tuple(b2), to_tuple(c2)}
            if conj_set == target_set:
                found = True
                break
        if found:
            current_class.append(j)
            assigned.add(j)
    
    classes.append(current_class)

print(f"  Conjugacy classes: {len(classes)}")
for i, cls in enumerate(classes):
    print(f"    Class {i+1}: {len(cls)} triples")

print(f"\n  If 1 class: the traditional triple is the ONLY one (up to relabeling)")
print(f"  If >1 classes: genuinely distinct alternatives exist")
