#!/usr/bin/env python3
"""
Probe 1c: Symmetry group of the marked cube.

Find the stabilizer of the 6 marked cells under S₂ × S₃ × S₅,
and also under the algebraic subgroup Z₂ × S₃ × Aut(Z₅).
"""

from itertools import permutations, product

# ── The 6 marked cells: (polarity, line, element) ──
MARKED = frozenset([
    (0, 0, 0),  # pos H → Wood
    (1, 0, 0),  # neg H → Wood
    (0, 2, 4),  # pos Q → Water
    (1, 2, 1),  # neg Q → Fire
    (0, 1, 3),  # pos P → Metal
    (1, 1, 2),  # neg P → Earth
])

ELEM_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}
LINE_NAMES = {0: 'H', 1: 'P', 2: 'Q'}

results = []
results.append("# Probe 1c: Symmetry Group of the Marked Cube\n")

# ══════════════════════════════════════════════
# Part 1: Full ambient group S₂ × S₃ × S₅
# ══════════════════════════════════════════════

results.append("## 1. Full Ambient Group S₂ × S₃ × S₅ (order 1440)\n")

# Generate all permutations
pol_perms = list(permutations(range(2)))   # 2
line_perms = list(permutations(range(3)))  # 6
elem_perms = list(permutations(range(5)))  # 120

stabilizer = []

for pp in pol_perms:
    for lp in line_perms:
        for ep in elem_perms:
            # Apply (pp, lp, ep) to each marked cell
            image = frozenset((pp[p], lp[l], ep[e]) for p, l, e in MARKED)
            if image == MARKED:
                stabilizer.append((pp, lp, ep))

results.append(f"Stabilizer order: {len(stabilizer)}")
results.append("")

# Describe each element
results.append("### All stabilizer elements:\n")
for pp, lp, ep in stabilizer:
    pol_desc = "id" if pp == (0, 1) else "swap"
    line_desc = str(tuple(LINE_NAMES[lp[i]] for i in range(3)))
    elem_desc = str(tuple(ELEM_NAMES[ep[i]] for i in range(5)))
    
    # Show action on marked cells for verification
    image = [(pp[p], lp[l], ep[e]) for p, l, e in sorted(MARKED)]
    results.append(f"  pol={pol_desc}, lines={line_desc}, elems={elem_desc}")

results.append("")

# Analyze structure
results.append("### Structure analysis:\n")

# Check if any non-identity element permutation appears
non_id_elem = [s for s in stabilizer if s[2] != (0, 1, 2, 3, 4)]
results.append(f"Elements with non-identity element permutation: {len(non_id_elem)}")

non_id_line = [s for s in stabilizer if s[1] != (0, 1, 2)]
results.append(f"Elements with non-identity line permutation: {len(non_id_line)}")

non_id_pol = [s for s in stabilizer if s[0] != (0, 1)]
results.append(f"Elements with polarity swap: {len(non_id_pol)}")
results.append("")

# Describe the generators more carefully
results.append("### Detailed element descriptions:\n")
for i, (pp, lp, ep) in enumerate(stabilizer):
    # Describe the permutation in cycle notation
    def cycles(perm):
        seen = set()
        cycs = []
        for start in range(len(perm)):
            if start in seen:
                continue
            cyc = []
            j = start
            while j not in seen:
                seen.add(j)
                cyc.append(j)
                j = perm[j]
            if len(cyc) > 1:
                cycs.append(tuple(cyc))
        return cycs if cycs else [()]  # identity
    
    pol_cyc = cycles(pp)
    line_cyc = cycles(lp)
    elem_cyc = cycles(ep)
    
    pol_str = "id" if pol_cyc == [()] else str(pol_cyc)
    line_str = "id" if line_cyc == [()] else str([(LINE_NAMES[c] for c in cyc) for cyc in line_cyc])
    
    # Pretty line cycles
    line_parts = []
    for cyc in line_cyc:
        if len(cyc) > 1:
            line_parts.append("(" + " ".join(LINE_NAMES[c] for c in cyc) + ")")
    line_str = " ".join(line_parts) if line_parts else "id"
    
    elem_parts = []
    for cyc in elem_cyc:
        if len(cyc) > 1:
            elem_parts.append("(" + " ".join(ELEM_NAMES[c] for c in cyc) + ")")
    elem_str = " ".join(elem_parts) if elem_parts else "id"
    
    results.append(f"  g{i}: pol={'swap' if pp != (0,1) else 'id':4s}  "
                   f"lines={line_str:20s}  elems={elem_str}")

results.append("")

# Check group properties
results.append("### Is it cyclic/abelian?\n")

# Compose two group elements
def compose(g1, g2):
    pp1, lp1, ep1 = g1
    pp2, lp2, ep2 = g2
    pp = tuple(pp1[pp2[i]] for i in range(2))
    lp = tuple(lp1[lp2[i]] for i in range(3))
    ep = tuple(ep1[ep2[i]] for i in range(5))
    return (pp, lp, ep)

# Check all commutators
abelian = True
for g1 in stabilizer:
    for g2 in stabilizer:
        if compose(g1, g2) != compose(g2, g1):
            abelian = False
            break
    if not abelian:
        break

results.append(f"Abelian: {abelian}")

# Element orders
def order(g):
    current = g
    identity = ((0, 1), (0, 1, 2), (0, 1, 2, 3, 4))
    for n in range(1, 100):
        if current == identity:
            return n
        current = compose(current, g)
    return None

orders = [order(g) for g in stabilizer]
results.append(f"Element orders: {sorted(orders)}")

# Find generators
if len(stabilizer) > 1:
    # Try each non-identity element as potential generator
    for g in stabilizer:
        if g == ((0, 1), (0, 1, 2), (0, 1, 2, 3, 4)):
            continue
        generated = set()
        current = g
        identity = ((0, 1), (0, 1, 2), (0, 1, 2, 3, 4))
        for _ in range(100):
            generated.add(current)
            if current == identity:
                break
            current = compose(current, g)
        if len(generated) == len(stabilizer):
            results.append(f"Cyclic generator found: order {order(g)}")
            break
    else:
        results.append("Not cyclic (no single generator)")
        # Try pairs
        for i, g1 in enumerate(stabilizer):
            for j, g2 in enumerate(stabilizer):
                if j <= i:
                    continue
                generated = set()
                # Generate all products of g1, g2
                queue = [g1, g2]
                identity = ((0, 1), (0, 1, 2), (0, 1, 2, 3, 4))
                generated.add(identity)
                while queue:
                    g = queue.pop()
                    if g in generated and g != identity:
                        continue
                    generated.add(g)
                    for h in list(generated):
                        for prod in [compose(g, h), compose(h, g)]:
                            if prod not in generated:
                                queue.append(prod)
                if len(generated) == len(stabilizer):
                    results.append(f"Generated by g{i} and g{j}")
                    break
            else:
                continue
            break

results.append("")

# ══════════════════════════════════════════════
# Part 2: Algebraic ambient group Z₂ × S₃ × Aut(Z₅)
# ══════════════════════════════════════════════

results.append("## 2. Algebraic Ambient Group Z₂ × S₃ × Aut(Z₅) (order 48)\n")

# Aut(Z₅) = multiplication by {1, 2, 3, 4} mod 5
aut_z5 = []
for m in [1, 2, 3, 4]:
    perm = tuple((m * e) % 5 for e in range(5))
    aut_z5.append(perm)

results.append(f"Aut(Z₅) elements (as permutations of {{0,1,2,3,4}}):")
for m, perm in zip([1,2,3,4], aut_z5):
    results.append(f"  ×{m}: {perm}")
results.append("")

alg_stabilizer = []
for pp in pol_perms:
    for lp in line_perms:
        for ep in aut_z5:
            image = frozenset((pp[p], lp[l], ep[e]) for p, l, e in MARKED)
            if image == MARKED:
                alg_stabilizer.append((pp, lp, ep))

results.append(f"Algebraic stabilizer order: {len(alg_stabilizer)}")
results.append("")

if alg_stabilizer:
    for i, (pp, lp, ep) in enumerate(alg_stabilizer):
        # Find which multiplier
        for m in [1,2,3,4]:
            if all((m*e)%5 == ep[e] for e in range(5)):
                mult = m
                break
        
        line_parts = []
        for cyc in cycles(lp):
            if len(cyc) > 1:
                line_parts.append("(" + " ".join(LINE_NAMES[c] for c in cyc) + ")")
        line_str = " ".join(line_parts) if line_parts else "id"
        
        results.append(f"  pol={'swap' if pp != (0,1) else 'id':4s}  "
                       f"lines={line_str:20s}  elems=×{mult} mod 5")
    results.append("")

    orders_alg = [order(g) for g in alg_stabilizer]
    results.append(f"Element orders: {sorted(orders_alg)}")
    
    abelian_alg = True
    for g1 in alg_stabilizer:
        for g2 in alg_stabilizer:
            if compose(g1, g2) != compose(g2, g1):
                abelian_alg = False
                break
        if not abelian_alg:
            break
    results.append(f"Abelian: {abelian_alg}")
else:
    results.append("Algebraic stabilizer is trivial (identity only)")

results.append("")

# ══════════════════════════════════════════════
# Part 3: Interpretation
# ══════════════════════════════════════════════

results.append("## 3. Interpretation\n")

# The complement + negation symmetry
# swap polarities + negate elements → should preserve marking
# Check explicitly
swap_neg = ((1, 0), (0, 1, 2), tuple((-e) % 5 for e in range(5)))
image = frozenset((swap_neg[0][p], swap_neg[1][l], swap_neg[2][e]) for p, l, e in MARKED)
results.append(f"Complement + Z₅ negation (swap pol, negate elems):")
results.append(f"  Image of marked set: {sorted(image)}")
results.append(f"  Preserves marking: {image == MARKED}")
results.append("")

# P↔Q swap + associated element permutation
for ep in elem_perms:
    pq_swap = (0, 2, 1)  # swap P and Q
    for pp in pol_perms:
        image = frozenset((pp[p], pq_swap[l], ep[e]) for p, l, e in MARKED)
        if image == MARKED:
            elem_parts = []
            for cyc in cycles(ep):
                if len(cyc) > 1:
                    elem_parts.append("(" + " ".join(ELEM_NAMES[c] for c in cyc) + ")")
            elem_str = " ".join(elem_parts) if elem_parts else "id"
            results.append(f"Found P↔Q swap symmetry: pol={'swap' if pp!=(0,1) else 'id'}, elems={elem_str}")

results.append("")

# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

output = '\n'.join(results)
print(output)

with open('memories/iching/magic/probe_1c.md', 'w') as f:
    f.write(output)

print("\n\nSaved to memories/iching/magic/probe_1c.md")
