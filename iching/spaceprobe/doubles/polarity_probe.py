"""
The polarity partition: is it derivable or irreducible?

The blocks: {Kan,Li}, {Kun,Gen}, {Zhen,Dui}, {Xun,Qian}
P₊ = {Kan, Zhen, Dui, Li} (odd Lo Shu: 1,3,7,9)
P₋ = {Kun, Gen, Xun, Qian} (even Lo Shu: 2,8,4,6)

The question: can any structure we've identified distinguish the two
members of each block without external input?

Candidates:
1. Z₂³ binary structure (popcount, specific bits, Hamming properties)
2. Five-phase cycle direction
3. Block-internal asymmetry from the involutions themselves
4. The S₄ normal chain S₄ ⊃ A₄ ⊃ V₄ ⊃ {id}
5. Properties of the three involutions' interaction
"""

N = 8

# Trigrams as binary: bit0=bottom, bit1=middle, bit2=top
# 000=Kun, 001=Gen, 010=Kan, 011=Xun, 100=Zhen, 101=Li, 110=Dui, 111=Qian
TRIG_NAMES = {0:'Kun', 1:'Gen', 2:'Kan', 3:'Xun', 4:'Zhen', 5:'Li', 6:'Dui', 7:'Qian'}

BLOCKS = [
    (2, 5),  # Kan, Li
    (0, 1),  # Kun, Gen
    (4, 6),  # Zhen, Dui
    (3, 7),  # Xun, Qian
]

P_PLUS = {2, 4, 6, 5}   # Kan, Zhen, Dui, Li (odd Lo Shu)
P_MINUS = {0, 1, 3, 7}  # Kun, Gen, Xun, Qian (even Lo Shu)

# For each block, which member is in P₊?
for a, b in BLOCKS:
    plus = a if a in P_PLUS else b
    minus = a if a in P_MINUS else b
    print(f"  Block {{{TRIG_NAMES[a]},{TRIG_NAMES[b]}}}: "
          f"P₊={TRIG_NAMES[plus]}({plus:03b}), P₋={TRIG_NAMES[minus]}({minus:03b})")

# ══════════════════════════════════════════════════════════════════════════════
# 1. BINARY PROPERTIES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"1. BINARY (Z₂³) PROPERTIES")
print(f"{'=' * 70}")

# Popcount
print(f"\n  Popcount:")
for t in range(8):
    pc = bin(t).count('1')
    pol = "+" if t in P_PLUS else "-"
    print(f"    {TRIG_NAMES[t]:6s} ({t:03b}): popcount={pc}, polarity={pol}")

# Is polarity = popcount parity?
pop_parity_matches = all(
    (bin(t).count('1') % 2 == 1) == (t in P_PLUS) for t in range(8)
)
print(f"\n  Polarity = odd popcount? {pop_parity_matches}")

# Check: what IS the binary predicate?
print(f"\n  Checking all single-bit predicates:")
for bit_pos in range(3):
    matches = all(((t >> bit_pos) & 1 == 1) == (t in P_PLUS) for t in range(8))
    print(f"    bit {bit_pos} = 1 ↔ P₊: {matches}")

# Check popcount
pop_even = {t for t in range(8) if bin(t).count('1') % 2 == 0}
pop_odd = {t for t in range(8) if bin(t).count('1') % 2 == 1}
print(f"\n  Even popcount: {sorted(pop_even)} = {{{', '.join(TRIG_NAMES[t] for t in sorted(pop_even))}}}")
print(f"  Odd popcount:  {sorted(pop_odd)} = {{{', '.join(TRIG_NAMES[t] for t in sorted(pop_odd))}}}")
print(f"  P₊ = {sorted(P_PLUS)} = {{{', '.join(TRIG_NAMES[t] for t in sorted(P_PLUS))}}}")
print(f"  P₋ = {sorted(P_MINUS)} = {{{', '.join(TRIG_NAMES[t] for t in sorted(P_MINUS))}}}")
print(f"  P₊ = even popcount? {P_PLUS == pop_even}")
print(f"  P₊ = odd popcount? {P_PLUS == pop_odd}")

# Check XOR-based predicates
print(f"\n  Checking all XOR masks (t XOR mask → popcount parity):")
for mask in range(8):
    result = {t for t in range(8) if bin(t ^ mask).count('1') % 2 == 0}
    if result == P_PLUS:
        print(f"    mask={mask:03b}: even popcount of (t⊕mask) = P₊ ✓")
    elif result == P_MINUS:
        print(f"    mask={mask:03b}: even popcount of (t⊕mask) = P₋ (inverted) ✓")

# ══════════════════════════════════════════════════════════════════════════════
# 2. WITHIN-BLOCK BINARY RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"2. WITHIN-BLOCK BINARY RELATIONSHIPS")
print(f"{'=' * 70}")

# For each block, what's the XOR between the two members?
print(f"\n  Block XOR (difference between members):")
for a, b in BLOCKS:
    xor = a ^ b
    print(f"    {{{TRIG_NAMES[a]},{TRIG_NAMES[b]}}}: {a:03b} ⊕ {b:03b} = {xor:03b} "
          f"(popcount={bin(xor).count('1')})")

# Are the blocks defined by consistent XOR? No — distances are 3,1,1,1
# But the P₊ member: is it always the one with more/fewer yang lines?
print(f"\n  Yang count (popcount) within blocks:")
for a, b in BLOCKS:
    pa, pb = bin(a).count('1'), bin(b).count('1')
    plus = a if a in P_PLUS else b
    print(f"    {{{TRIG_NAMES[a]}({pa}),{TRIG_NAMES[b]}({pb})}}: "
          f"P₊={TRIG_NAMES[plus]}(yang={bin(plus).count('1')})")

# ══════════════════════════════════════════════════════════════════════════════
# 3. INVOLUTION-DERIVED PROPERTIES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"3. INVOLUTION-DERIVED PROPERTIES")
print(f"{'=' * 70}")

# The three involutions
iota1 = {0:7, 7:0, 1:6, 6:1, 2:5, 5:2, 3:4, 4:3}  # Fu Xi
iota2 = {2:5, 5:2, 0:1, 1:0, 4:6, 6:4, 3:7, 7:3}  # Lo Shu
iota3 = {2:7, 7:2, 0:6, 6:0, 4:1, 1:4, 3:5, 5:3}  # He Tu

def compose(p1, p2):
    return {k: p2[p1[k]] for k in p1}

# ι₂∘ι₃ is order 2 (they commute). What is it?
i23 = compose(iota2, iota3)
print(f"\n  ι₂∘ι₃ = {i23}")
print(f"  As pairs: ", end="")
seen = set()
for x in sorted(i23):
    if x not in seen:
        print(f"{TRIG_NAMES[x]}↔{TRIG_NAMES[i23[x]]}", end="  ")
        seen.add(x); seen.add(i23[x])
print()

# ι₁∘ι₂ is order 3
i12 = compose(iota1, iota2)
print(f"\n  ι₁∘ι₂ (order 3) = {i12}")
# Show cycles
seen = set()
for start in range(8):
    if start in seen:
        continue
    cycle = [start]
    seen.add(start)
    x = i12[start]
    while x != start:
        cycle.append(x)
        seen.add(x)
        x = i12[x]
    if len(cycle) > 1:
        cycle_str = '→'.join(TRIG_NAMES[c] for c in cycle)
        pols = ['+' if c in P_PLUS else '-' for c in cycle]
        print(f"    Cycle: {cycle_str} (polarities: {pols})")

# ι₁∘ι₃ is order 4
i13 = compose(iota1, iota3)
print(f"\n  ι₁∘ι₃ (order 4) = {i13}")
seen = set()
for start in range(8):
    if start in seen:
        continue
    cycle = [start]
    seen.add(start)
    x = i13[start]
    while x != start:
        cycle.append(x)
        seen.add(x)
        x = i13[x]
    if len(cycle) > 1:
        cycle_str = '→'.join(TRIG_NAMES[c] for c in cycle)
        pols = ['+' if c in P_PLUS else '-' for c in cycle]
        print(f"    Cycle: {cycle_str} (polarities: {pols})")

# Key question: does any composition of involutions map P₊ to P₊ and P₋ to P₋?
# That would mean the polarity is visible to the group.
# Actually we know Aut = Z₂, so the Z₂ element swaps within blocks.
# P₊/P₋ is what breaks this Z₂. So by definition, the non-trivial automorphism
# swaps P₊ ↔ P₋. The polarity IS the thing the automorphism flips.
# No group element can distinguish P₊ from P₋ because the automorphism that
# swaps them is a symmetry of the structure.

print(f"\n  The S₄ automorphism group:")
print(f"  Aut(S₄ on 4×2) = Z₂ (swap within all blocks)")
print(f"  The non-trivial automorphism: ι₂ (swaps within each block)")
print(f"  P₊ ↔ P₋ under ι₂. So the S₄ structure CANNOT distinguish P₊ from P₋.")
print(f"  Any property derived from involutions alone must be symmetric under ι₂.")

# ══════════════════════════════════════════════════════════════════════════════
# 4. CAN Z₂³ BREAK THE SYMMETRY?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"4. CAN THE BINARY STRUCTURE BREAK THE SYMMETRY?")
print(f"{'=' * 70}")

# The Z₂³ structure is independent of S₄. Does it see P₊/P₋?
# P₊ = {Kan(010), Zhen(100), Dui(110), Li(101)}
# P₋ = {Kun(000), Gen(001), Xun(011), Qian(111)}

# Check: is P₊ a coset or subgroup of Z₂³?
print(f"\n  Is P₊ a subgroup of Z₂³?")
# Closed under XOR?
for a in P_PLUS:
    for b in P_PLUS:
        if (a ^ b) not in P_PLUS:
            print(f"    No: {TRIG_NAMES[a]} ⊕ {TRIG_NAMES[b]} = {TRIG_NAMES[a^b]} ∈ P₋")
            break
    else:
        continue
    break

print(f"\n  Is P₋ a subgroup of Z₂³?")
for a in P_MINUS:
    for b in P_MINUS:
        if (a ^ b) not in P_MINUS:
            print(f"    No: {TRIG_NAMES[a]} ⊕ {TRIG_NAMES[b]} = {TRIG_NAMES[a^b]} ∈ P₊")
            break
    else:
        continue
    break

# Is P₊ a coset of some subgroup?
# P₋ contains 0 (identity), so if P₋ were a subgroup, P₊ = t + P₋ for any t ∈ P₊
print(f"\n  Is P₋ a subgroup? (Contains identity 000=Kun)")
is_subgroup = True
for a in P_MINUS:
    for b in P_MINUS:
        if (a ^ b) not in P_MINUS:
            is_subgroup = False
            print(f"    No: {TRIG_NAMES[a]} ⊕ {TRIG_NAMES[b]} = {TRIG_NAMES[a^b]} ∈ P₊")
            break
    if not is_subgroup:
        break

if is_subgroup:
    print(f"    YES! P₋ is a subgroup of Z₂³.")
    print(f"    P₊ is its coset: P₊ = t ⊕ P₋ for any t ∈ P₊")
    # Which subgroup?
    print(f"    P₋ = {{{', '.join(f'{t:03b}' for t in sorted(P_MINUS))}}} = ?")
    # Check: is it generated by some elements?
    # {000, 001, 011, 111}: 001⊕011=010∈P₊. Not closed!
    pass

# Actually let me just check closure properly
print(f"\n  Full closure check of P₋ = {{000, 001, 011, 111}}:")
for a in sorted(P_MINUS):
    for b in sorted(P_MINUS):
        r = a ^ b
        status = "∈ P₋" if r in P_MINUS else "∈ P₊ ✗"
        if r not in P_MINUS:
            print(f"    {a:03b} ⊕ {b:03b} = {r:03b} {status}")

# Not a subgroup. So Z₂³ alone can't see P₊/P₋ as a coset partition.

# ══════════════════════════════════════════════════════════════════════════════
# 5. WHAT DOES SEE THE POLARITY?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"5. WHAT STRUCTURES SEE THE POLARITY?")
print(f"{'=' * 70}")

# The polarity IS visible to:
# 1. Lo Shu numbers (odd vs even)
# 2. Popcount parity? Let's check again carefully
print(f"\n  Popcount parity check:")
for t in sorted(range(8)):
    pc = bin(t).count('1')
    pol = "+" if t in P_PLUS else "-"
    parity = "even" if pc % 2 == 0 else "odd"
    match = (pol == "+" and parity == "even") or (pol == "-" and parity == "odd")
    print(f"    {TRIG_NAMES[t]:6s} {t:03b} popcount={pc} ({parity}) polarity={pol} match={match}")

# Count matches
matches = sum(1 for t in range(8) 
              if ((t in P_PLUS) == (bin(t).count('1') % 2 == 0)))
print(f"\n  Popcount parity = polarity: {matches}/8 matches")

# So popcount parity DOES match! Let me verify:
# P₊: Kan(010,pc=1,odd), Zhen(100,pc=1,odd), Dui(110,pc=2,even), Li(101,pc=2,even)
# P₋: Kun(000,pc=0,even), Gen(001,pc=1,odd), Xun(011,pc=2,even), Qian(111,pc=3,odd)
# P₊ has {odd, odd, even, even}, P₋ has {even, odd, even, odd}
# Not a clean split by popcount parity.

# What about the MIDDLE BIT specifically?
print(f"\n  Middle bit (bit 1) check:")
for t in sorted(range(8)):
    mid = (t >> 1) & 1
    pol = "+" if t in P_PLUS else "-"
    print(f"    {TRIG_NAMES[t]:6s} {t:03b} mid={mid} polarity={pol}")

mid1 = {t for t in range(8) if (t >> 1) & 1 == 1}
print(f"  Middle bit = 1: {{{', '.join(TRIG_NAMES[t] for t in sorted(mid1))}}}")
print(f"  P₊ = {{{', '.join(TRIG_NAMES[t] for t in sorted(P_PLUS))}}}")
print(f"  Match: {mid1 == P_PLUS}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. THE AUTOMORPHISM ARGUMENT
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"6. THE AUTOMORPHISM ARGUMENT (WHY IT'S IRREDUCIBLE)")
print(f"{'=' * 70}")

# The within-block swap (ι₂) is an automorphism of the full S₄ structure.
# ANY property derived purely from the involutions must be invariant under ι₂.
# But ι₂ swaps the two members of each block, which swaps P₊ ↔ P₋.
# Therefore no involution-derived property can distinguish P₊ from P₋. QED.
#
# What about properties derived from BOTH Z₂³ AND S₄?
# ι₂ is NOT an automorphism of Z₂³ (it's not even a linear map on Z₂³).
# So a property using both structures COULD break the symmetry.

print(f"""
  THEOREM: No property derived from the S₄ involution structure alone
  can distinguish P₊ from P₋.

  PROOF: ι₂ (within-block swap) is an automorphism of the S₄ structure.
  It maps P₊ → P₋ and P₋ → P₊. Any S₄-derived predicate must be
  invariant under this automorphism, hence cannot separate P₊ from P₋. □

  QUESTION: Can a property derived from BOTH Z₂³ AND S₄ break it?
  ι₂ is NOT a Z₂³ automorphism (not a linear map). So the joint
  structure could see the polarity.
""")

# Check: what is ι₂ in binary terms?
# ι₂: Kan(010)↔Li(101), Kun(000)↔Gen(001), Zhen(100)↔Dui(110), Xun(011)↔Qian(111)
# As binary: 010↔101 (XOR=111), 000↔001 (XOR=001), 100↔110 (XOR=010), 011↔111 (XOR=100)
# Different XOR for each pair! So ι₂ is NOT a uniform XOR operation.
# Is it affine? Check: ι₂(a⊕b) = ι₂(a)⊕ι₂(b)⊕ι₂(0)?
print(f"  Is ι₂ affine on Z₂³?")
iota2_fn = lambda t: iota2[t]
# Affine: f(a⊕b) = f(a)⊕f(b)⊕f(0) for all a,b
c = iota2_fn(0)  # f(0) = 1
is_affine = True
for a in range(8):
    for b in range(8):
        lhs = iota2_fn(a ^ b)
        rhs = iota2_fn(a) ^ iota2_fn(b) ^ c
        if lhs != rhs:
            is_affine = False
            print(f"    No: ι₂({a:03b}⊕{b:03b}) = ι₂({a^b:03b}) = {lhs:03b}, "
                  f"but ι₂({a:03b})⊕ι₂({b:03b})⊕ι₂(000) = {iota2_fn(a):03b}⊕{iota2_fn(b):03b}⊕{c:03b} = {rhs:03b}")
            break
    if not is_affine:
        break

if is_affine:
    print(f"    Yes — ι₂ is affine on Z₂³")
else:
    print(f"    ι₂ is NOT affine on Z₂³")
    print(f"    Therefore Z₂³ CAN distinguish what ι₂ swaps")

# So: the JOINT structure (Z₂³ + S₄) can potentially see the polarity.
# But can it? We need a concrete predicate.

# ══════════════════════════════════════════════════════════════════════════════
# 7. SEARCHING FOR THE JOINT PREDICATE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"7. SEARCHING FOR A JOINT PREDICATE")
print(f"{'=' * 70}")

# For each block {a,b}, is there a Z₂³ property that consistently picks
# the P₊ member, using knowledge of the block structure?

# Candidate: within each block, which member has more yang lines?
print(f"\n  Within-block yang comparison:")
consistent_yang = True
for a, b in BLOCKS:
    pa, pb = bin(a).count('1'), bin(b).count('1')
    plus = a if a in P_PLUS else b
    plus_more = bin(plus).count('1') > bin(a if a != plus else b).count('1')
    print(f"    {{{TRIG_NAMES[a]}({pa}y),{TRIG_NAMES[b]}({pb}y)}}: "
          f"P₊={TRIG_NAMES[plus]}({bin(plus).count('1')}y) — P₊ has {'more' if plus_more else 'fewer or equal'} yang")
    if pa == pb:
        consistent_yang = False

# Candidate: the block XOR mask — does its popcount/structure predict polarity?
print(f"\n  Block XOR and polarity:")
for a, b in BLOCKS:
    xor = a ^ b
    plus = a if a in P_PLUS else b
    # Which bit does the XOR flip?
    print(f"    {{{TRIG_NAMES[a]},{TRIG_NAMES[b]}}}: XOR={xor:03b}, "
          f"P₊ has bit pattern where the differing bits are... "
          f"P₊={plus:03b}, P₋={a if a!=plus else b:03b}")

# Candidate: within each block, P₊ is the one where ι₁(P₊_member) is in a 
# "lower-numbered" block? (Using ι₁ = complement, which IS a Z₂³ map)
print(f"\n  ι₁ image of P₊ members:")
for a, b in BLOCKS:
    plus = a if a in P_PLUS else b
    minus = b if a in P_PLUS else a
    i1_plus = iota1[plus]
    i1_minus = iota1[minus]
    # Which block does ι₁(plus) land in?
    for bi, (ba, bb) in enumerate(BLOCKS):
        if i1_plus == ba or i1_plus == bb:
            i1_plus_block = bi
        if i1_minus == ba or i1_minus == bb:
            i1_minus_block = bi
    print(f"    Block {{{TRIG_NAMES[a]},{TRIG_NAMES[b]}}}: "
          f"ι₁(P₊={TRIG_NAMES[plus]})={TRIG_NAMES[i1_plus]} (block {i1_plus_block}), "
          f"ι₁(P₋={TRIG_NAMES[minus]})={TRIG_NAMES[i1_minus]} (block {i1_minus_block})")

# Candidate: P₊ member is the one where ι₁(member) is in P₊?
# ι₁ swaps blocks, so it maps each block member to a member of another block.
# Is ι₁(P₊) ⊂ P₊?
print(f"\n  Does ι₁ preserve polarity?")
for t in range(8):
    same = (t in P_PLUS) == (iota1[t] in P_PLUS)
    print(f"    ι₁({TRIG_NAMES[t]})={TRIG_NAMES[iota1[t]]}: "
          f"{'same' if same else 'flipped'} polarity")

# ι₁ = complement = XOR 111. It maps each trigram to its complement.
# Does complement preserve or flip polarity?
preserves = sum(1 for t in range(8) if (t in P_PLUS) == (iota1[t] in P_PLUS))
print(f"  ι₁ preserves polarity: {preserves}/8")

# Does ι₃ preserve polarity?
print(f"\n  Does ι₃ preserve polarity?")
preserves_3 = sum(1 for t in range(8) if (t in P_PLUS) == (iota3[t] in P_PLUS))
print(f"  ι₃ preserves polarity: {preserves_3}/8")

# ι₂ by definition flips polarity (swaps within blocks)
# What about compositions?
i12 = compose(iota1, iota2)
i13 = compose(iota1, iota3)
i23 = compose(iota2, iota3)

for name, perm in [("ι₁∘ι₂", i12), ("ι₁∘ι₃", i13), ("ι₂∘ι₃", i23)]:
    preserves = sum(1 for t in range(8) if (t in P_PLUS) == (perm[t] in P_PLUS))
    print(f"  {name} preserves polarity: {preserves}/8")

# ══════════════════════════════════════════════════════════════════════════════
# 8. THE DEFINITIVE TEST: IS POLARITY VISIBLE TO Z₂³ × S₄?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"8. DEFINITIVE TEST: ALTERNATIVE POLARITY ASSIGNMENTS")
print(f"{'=' * 70}")

# There are 2⁴ = 16 ways to choose one member from each of 4 blocks.
# The traditional polarity is one. Are there others that are equally
# compatible with both Z₂³ and S₄?
#
# "Compatible with S₄" means nothing — all choices are S₄-equivalent (that's the Z₂).
# "Compatible with Z₂³" means... what? We need a Z₂³ predicate.
#
# The question reduces to: is there a Z₂³-derived property that picks
# EXACTLY the traditional polarity and no other assignment?

# Let's enumerate all 16 possible polarity assignments and check
# which Z₂³ properties each satisfies.

from itertools import product

all_assignments = list(product(range(2), repeat=4))  # 0=first member, 1=second
print(f"\n  All 16 polarity assignments (0=first block member, 1=second):")
print(f"  Block order: {[f'{{{TRIG_NAMES[a]},{TRIG_NAMES[b]}}}' for a,b in BLOCKS]}")

# Traditional: P₊ = {Kan, Kun→no... P₊={Kan,Zhen,Dui,Li}
# Block 0: (Kan,Li) → Kan is P₊ → choice 0
# Block 1: (Kun,Gen) → Kun is P₋, Gen is P₋... wait
# Both Kun and Gen are in P₋! That means P₊ takes Li from block 0, neither from block 1...
# Wait, I'm confusing myself. Each block contributes ONE member to P₊ and ONE to P₋.
# Block 0: {Kan(2), Li(5)} → Kan ∈ P₊, Li ∈ P₊? No!
# P₊ = {2,4,6,5} = {Kan, Zhen, Dui, Li}
# Block 0 = {Kan(2), Li(5)} → BOTH in P₊?? That can't be right.

# Let me recheck.
print(f"\n  Rechecking block membership vs polarity:")
for a, b in BLOCKS:
    a_pol = "+" if a in P_PLUS else "-"
    b_pol = "+" if b in P_PLUS else "-"
    print(f"    {{{TRIG_NAMES[a]}({a_pol}), {TRIG_NAMES[b]}({b_pol})}}")

# Block 0: Kan(+), Li(+) — BOTH P₊!
# Block 1: Kun(-), Gen(-) — BOTH P₋!
# Block 2: Zhen(+), Dui(+) — BOTH P₊!
# Block 3: Xun(-), Qian(-) — BOTH P₋!
#
# Wait — the polarity partition is NOT "one from each block"!
# It's 2 BLOCKS are P₊ and 2 BLOCKS are P₋!

print(f"\n  *** THE POLARITY IS A BLOCK-LEVEL PARTITION, NOT WITHIN-BLOCK ***")
print(f"  P₊ blocks: {{{TRIG_NAMES[2]},{TRIG_NAMES[5]}}}, {{{TRIG_NAMES[4]},{TRIG_NAMES[6]}}}")
print(f"  P₋ blocks: {{{TRIG_NAMES[0]},{TRIG_NAMES[1]}}}, {{{TRIG_NAMES[3]},{TRIG_NAMES[7]}}}")
print(f"  This is a partition of 4 BLOCKS into 2+2, not a within-block choice!")

# So the automorphism that the polarity breaks is NOT the within-block swap.
# It's a permutation of blocks. Let me reconsider.

# The Aut of the S₄ structure: what permutations of 8 elements preserve
# all three involutions simultaneously?
print(f"\n  Computing Aut(ι₁, ι₂, ι₃):")
from itertools import permutations

auts = []
for perm in permutations(range(8)):
    p = {i: perm[i] for i in range(8)}
    # Check: does p commute with all three involutions?
    # p ∘ ι ∘ p⁻¹ = ι for each ι
    p_inv = {v: k for k, v in p.items()}
    
    preserves_all = True
    for iota in [iota1, iota2, iota3]:
        for x in range(8):
            # p(ι(p⁻¹(x))) should equal ι(x)
            if p[iota[p_inv[x]]] != iota[x]:
                preserves_all = False
                break
        if not preserves_all:
            break
    
    if preserves_all:
        auts.append(p)

print(f"  |Aut| = {len(auts)}")
for aut in auts:
    if aut == {i:i for i in range(8)}:
        print(f"    identity")
    else:
        pairs = []
        seen = set()
        for x in range(8):
            if x not in seen and aut[x] != x:
                cycle = [x]
                y = aut[x]
                while y != x:
                    cycle.append(y)
                    seen.add(y)
                    y = aut[y]
                seen.add(x)
                pairs.append('→'.join(TRIG_NAMES[c] for c in cycle))
        print(f"    {', '.join(pairs)}")
        # Does this swap P₊ blocks with P₋ blocks?
        plus_blocks = {0, 2}  # block indices of P₊
        # Check where blocks go
        for bi, (a, b) in enumerate(BLOCKS):
            img_a = aut[a]
            for bj, (ba, bb) in enumerate(BLOCKS):
                if img_a == ba or img_a == bb:
                    break
            print(f"      Block {bi}({TRIG_NAMES[a]},{TRIG_NAMES[b]}) → Block {bj}({TRIG_NAMES[ba]},{TRIG_NAMES[bb]})")

# ══════════════════════════════════════════════════════════════════════════════
# 9. REVISED QUESTION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"9. THE REAL QUESTION: WHAT DISTINGUISHES THE 2+2 BLOCK PARTITION?")
print(f"{'=' * 70}")

# The polarity partitions 4 blocks into {0,2} vs {1,3}.
# That is: {Kan/Li, Zhen/Dui} vs {Kun/Gen, Xun/Qian}.
# There are C(4,2)/2 = 3 ways to split 4 blocks into 2+2.
# Which one is traditional and why?

splits = [
    ({0,2}, {1,3}, "{Kan/Li, Zhen/Dui} vs {Kun/Gen, Xun/Qian}"),
    ({0,1}, {2,3}, "{Kan/Li, Kun/Gen} vs {Zhen/Dui, Xun/Qian}"),
    ({0,3}, {1,2}, "{Kan/Li, Xun/Qian} vs {Kun/Gen, Zhen/Dui}"),
]

print(f"\n  Three possible 2+2 splits of 4 blocks:")
for s1, s2, desc in splits:
    # Get the elements in each half
    half1 = set()
    half2 = set()
    for bi in s1:
        half1.add(BLOCKS[bi][0])
        half1.add(BLOCKS[bi][1])
    for bi in s2:
        half2.add(BLOCKS[bi][0])
        half2.add(BLOCKS[bi][1])
    
    trad = " ← TRADITIONAL" if half1 == P_PLUS or half2 == P_PLUS else ""
    
    # Z₂³ properties of each half
    h1_popcounts = [bin(t).count('1') for t in half1]
    h2_popcounts = [bin(t).count('1') for t in half2]
    h1_sum = sum(h1_popcounts)
    h2_sum = sum(h2_popcounts)
    
    print(f"\n  {desc}{trad}")
    print(f"    Half 1 elements: {{{', '.join(TRIG_NAMES[t] for t in sorted(half1))}}}")
    print(f"    Half 2 elements: {{{', '.join(TRIG_NAMES[t] for t in sorted(half2))}}}")
    print(f"    Half 1 total yang: {h1_sum}, Half 2 total yang: {h2_sum}")
    
    # Is either half a subgroup or coset?
    is_h1_closed = all((a^b) in half1 for a in half1 for b in half1)
    is_h2_closed = all((a^b) in half2 for a in half2 for b in half2)
    print(f"    Half 1 closed under XOR: {is_h1_closed}")
    print(f"    Half 2 closed under XOR: {is_h2_closed}")
    
    # How does ι₁ (complement) act on this split?
    i1_preserves = all((iota1[t] in half1) == (t in half1) for t in range(8))
    print(f"    ι₁ (complement) preserves split: {i1_preserves}")
    
    # How does ι₃ act?
    i3_preserves = all((iota3[t] in half1) == (t in half1) for t in range(8))
    print(f"    ι₃ (He Tu) preserves split: {i3_preserves}")

# ══════════════════════════════════════════════════════════════════════════════
# 10. THE ANSWER
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"10. CONCLUSION")
print(f"{'=' * 70}")
