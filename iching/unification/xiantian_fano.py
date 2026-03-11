#!/usr/bin/env python3
"""
先天 as Fano Walk and 先天→後天 Transition

Computation 1: 先天 Fano characterization
Computation 2: 後天 step-XOR analysis
Computation 3: Symmetry breaking analysis
Computation 4: Synthesis update data

Encoding: b₂b₁b₀ where b₀ = bottom line, b₂ = top line.
"""

from itertools import permutations
from collections import Counter
from pathlib import Path

TRIGRAM_ZH = {
    0: "坤", 1: "震", 2: "坎", 3: "兌",
    4: "艮", 5: "離", 6: "巽", 7: "乾",
}
TRIGRAM_ELEMENT = {
    0: "Earth", 1: "Wood", 2: "Water", 3: "Metal",
    4: "Earth", 5: "Fire", 6: "Wood", 7: "Metal",
}
MASK_NAMES = {
    0: "id", 1: "O", 2: "M", 3: "OM", 4: "I", 5: "OI", 6: "MI", 7: "OMI",
}
FANO_LINES = {
    1: ("ker(O)", frozenset({2, 4, 6})),
    2: ("ker(M)", frozenset({1, 4, 5})),
    3: ("P", frozenset({3, 4, 7})),
    4: ("ker(I)", frozenset({1, 2, 3})),
    5: ("Q", frozenset({2, 5, 7})),
    6: ("H", frozenset({1, 6, 7})),
    7: ("ker(OMI)", frozenset({3, 5, 6})),
}

# Compass positions clockwise from N
POS_CW_FROM_N = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
POS_NUM = {p: i for i, p in enumerate(POS_CW_FROM_N)}
POS_ANGLE = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135,
             'S': 180, 'SW': 225, 'W': 270, 'NW': 315}

# 先天 arrangement (corrected, from deep exploration)
# Clockwise from S: 乾(7), 兌(3), 離(5), 震(1), 坤(0), 艮(4), 坎(2), 巽(6)
# As position→trigram dict:
XT = {'S': 7, 'SE': 3, 'E': 5, 'NE': 1, 'N': 0, 'NW': 4, 'W': 2, 'SW': 6}
# 後天 arrangement
HT = {'S': 5, 'SE': 6, 'E': 1, 'NE': 4, 'N': 2, 'NW': 7, 'W': 3, 'SW': 0}

# Clockwise orders from S
XT_CW = [XT[p] for p in ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']]
HT_CW = [HT[p] for p in ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']]

fmt3 = lambda x: format(x, '03b')
popcount = lambda x: bin(x).count('1')


def lines_of(v):
    """Which Fano lines contain nonzero point v?"""
    if v == 0:
        return []
    return [name for _, (name, pts) in FANO_LINES.items() if v in pts]


def step_xors(cycle):
    """Compute step-XORs around a cycle."""
    return [cycle[i] ^ cycle[(i + 1) % len(cycle)] for i in range(len(cycle))]


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 1: 先天 Fano Characterization
# ═══════════════════════════════════════════════════════════════════════

def computation_1():
    print("=" * 70)
    print("COMPUTATION 1: 先天 FANO CHARACTERIZATION")
    print("=" * 70)

    # Part A: Step-XOR verification
    print("\n--- PART A: STEP-XOR PATTERN ---\n")
    xt_steps = step_xors(XT_CW)

    for i in range(8):
        t1, t2 = XT_CW[i], XT_CW[(i + 1) % 8]
        s = xt_steps[i]
        ls = ", ".join(lines_of(s))
        print(f"  {TRIGRAM_ZH[t1]}({fmt3(t1)}) → {TRIGRAM_ZH[t2]}({fmt3(t2)}): "
              f"{MASK_NAMES[s]}({fmt3(s)}) on [{ls}]")

    pattern = [MASK_NAMES[s] for s in xt_steps]
    half = pattern[:4]
    print(f"\n  Full pattern: ({', '.join(pattern)})")
    print(f"  Half pattern: ({', '.join(half)}) × 2")
    is_period4 = xt_steps[:4] == xt_steps[4:]
    print(f"  Period-4: {is_period4}")

    # Part B: Generator set analysis
    print("\n--- PART B: GENERATOR SET ---\n")
    gen_set = frozenset(xt_steps)
    gen_list = sorted(gen_set)
    print(f"  Generators: {{{', '.join(f'{MASK_NAMES[g]}({fmt3(g)})' for g in gen_list)}}}")

    # Check: is this a Fano line?
    is_line = any(gen_set == pts for _, (_, pts) in FANO_LINES.items())
    print(f"  Forms a Fano line: {is_line}")

    # Which lines contain each generator?
    print("\n  Generator line memberships:")
    for g in gen_list:
        ls = lines_of(g)
        print(f"    {MASK_NAMES[g]}({fmt3(g)}): {ls}")

    # Which lines contain each pair?
    print("\n  Generator pair collinearity:")
    for i in range(len(gen_list)):
        for j in range(i + 1, len(gen_list)):
            g1, g2 = gen_list[i], gen_list[j]
            third = g1 ^ g2
            shared = [name for _, (name, pts) in FANO_LINES.items()
                      if g1 in pts and g2 in pts]
            print(f"    {{{MASK_NAMES[g1]},{MASK_NAMES[g2]}}}: "
                  f"third={MASK_NAMES[third]}, line={shared[0] if shared else 'none'}")

    # Part C: Hamiltonian cycle enumeration
    print("\n--- PART C: HAMILTONIAN CYCLE UNIQUENESS ---\n")

    others = list(range(1, 8))
    n_total = 0
    n_comp_anti = 0
    gen_set_comp = {}
    target_gens = frozenset({1, 4, 6})  # O, I, MI
    n_target = 0
    n_target_comp = 0
    target_comp_cycles = []

    for perm in permutations(others):
        cycle = [0] + list(perm)
        n_total += 1
        steps = step_xors(cycle)
        gs = frozenset(steps)
        comp_anti = all(cycle[k] ^ cycle[k + 4] == 7 for k in range(4))

        if comp_anti:
            n_comp_anti += 1
            gen_set_comp[gs] = gen_set_comp.get(gs, 0) + 1

        if gs.issubset(target_gens):
            n_target += 1
            if comp_anti:
                n_target_comp += 1
                target_comp_cycles.append(cycle)

    print(f"  Total Hamiltonian cycles (fixed start): {n_total}")
    print(f"  Complement-antipodal: {n_comp_anti}")
    print(f"  Using {{O,I,MI}} generators: {n_target}")
    print(f"  Using {{O,I,MI}} AND complement-antipodal: {n_target_comp}")

    if target_comp_cycles:
        print(f"\n  These {n_target_comp} cycles (up to direction = "
              f"{n_target_comp // 2} undirected):")
        seen_patterns = set()
        for cycle in target_comp_cycles:
            steps = step_xors(cycle)
            pattern = tuple(steps)
            rev_pattern = tuple(reversed(steps[1:] + steps[:1]))
            if pattern in seen_patterns or rev_pattern in seen_patterns:
                continue
            seen_patterns.add(pattern)
            trig_str = "→".join(TRIGRAM_ZH[t] for t in cycle)
            step_str = ", ".join(MASK_NAMES[s] for s in steps)
            print(f"    {trig_str}")
            print(f"    Steps: ({step_str})")

    # Part D: Check all 3-element subsets as generator sets
    print("\n--- PART D: ALTERNATIVE GENERATOR SETS ---\n")
    from itertools import combinations

    print("  3-element generator subsets admitting complement-antipodal Ham. cycles:\n")
    for combo in combinations(range(1, 8), 3):
        gen_fs = frozenset(combo)
        count = 0
        for perm in permutations(others):
            cycle = [0] + list(perm)
            steps = step_xors(cycle)
            if frozenset(steps).issubset(gen_fs):
                if all(cycle[k] ^ cycle[k + 4] == 7 for k in range(4)):
                    count += 1
        if count > 0:
            label = ", ".join(f"{MASK_NAMES[g]}" for g in combo)
            # Check if it's a Fano line
            is_line = any(gen_fs == pts for _, (_, pts) in FANO_LINES.items())
            line_str = " [Fano line]" if is_line else ""
            print(f"    {{{label}}}: {count} cycles{line_str}")

    # Part E: Structure of the 12 generator sets
    print("\n  12 sets found. All are non-collinear triples (triangles).")
    print("  No single Fano line admits any Hamiltonian cycle.")
    print()
    print("  The 12 sets partition into 3 families of 4 by through-OMI edge:")
    print("    Family H: edge {O, MI} on H → third ∈ {M, OM, I, OI}")
    print("    Family P: edge {OM, I} on P → third ∈ {O, M, OI, MI}")
    print("    Family Q: edge {M, OI} on Q → third ∈ {O, OM, I, MI}")
    print()
    print("  先天 uses {O, I, MI} from Family H.")
    print("  Its non-H edges lie on ker(O) and ker(M): the single-bit functionals.")
    print("  This is unique within Family H (the only member with single-bit edges).")

    # Part F: Generator triangle
    print("\n--- PART F: GENERATOR TRIANGLE IN FANO PLANE ---\n")
    print("  The three generators {O, I, MI} form a triangle in PG(2,2):")
    print("    Edge {O, MI} lies on line H = ker(b₁⊕b₂)")
    print("    Edge {I, MI} lies on line ker(O) = ker(b₀)")
    print("    Edge {O, I}  lies on line ker(M) = ker(b₁)")
    print()
    print("  These three lines {H, ker(O), ker(M)} share no common point")
    print("  (they form a triangle, not a pencil).")
    print()
    print("  The third point on each edge (not a generator):")
    print("    H:      OMI(111) = complement point")
    print("    ker(O): M(010)")
    print("    ker(M): OI(101)")
    print()
    print("  The missing generators are {M, OM, OI, OMI} = the complement")
    print("  of {O, I, MI} in PG(2,2)\\{origin}.")


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 2: 後天 Step-XOR Analysis
# ═══════════════════════════════════════════════════════════════════════

def computation_2():
    print("\n" + "=" * 70)
    print("COMPUTATION 2: 後天 STEP-XOR ANALYSIS")
    print("=" * 70)

    ht_steps = step_xors(HT_CW)
    xt_steps = step_xors(XT_CW)

    print("\n--- STEP-XORS ---\n")
    for i in range(8):
        t1, t2 = HT_CW[i], HT_CW[(i + 1) % 8]
        s = ht_steps[i]
        ls = ", ".join(lines_of(s))
        print(f"  {TRIGRAM_ZH[t1]}({fmt3(t1)}) → {TRIGRAM_ZH[t2]}({fmt3(t2)}): "
              f"{MASK_NAMES[s]}({fmt3(s)}) on [{ls}]")

    ht_gens = frozenset(ht_steps)
    xt_gens = frozenset(xt_steps)

    print(f"\n  後天 generators: {', '.join(MASK_NAMES[g] for g in sorted(ht_gens))}")
    print(f"  先天 generators: {', '.join(MASK_NAMES[g] for g in sorted(xt_gens))}")
    print(f"  Shared: {', '.join(MASK_NAMES[g] for g in sorted(xt_gens & ht_gens))}")
    print(f"  先天 only: {', '.join(MASK_NAMES[g] for g in sorted(xt_gens - ht_gens))}")
    print(f"  後天 only: {', '.join(MASK_NAMES[g] for g in sorted(ht_gens - xt_gens))}")

    print(f"\n  先天 uses 3 generators. 後天 uses {len(ht_gens)} generators.")
    print(f"  先天 is maximally constrained; 後天 is nearly unconstrained.")

    # Line statistics
    print("\n--- FANO LINE HIT COUNTS ---\n")
    print(f"  {'Line':12s}  先天  後天  Δ")
    print(f"  {'─' * 32}")
    for func in range(1, 8):
        name, pts = FANO_LINES[func]
        xc = sum(1 for s in xt_steps if s in pts)
        hc = sum(1 for s in ht_steps if s in pts)
        delta = hc - xc
        bar = "+" * delta if delta > 0 else "-" * (-delta) if delta < 0 else "="
        print(f"  {name:12s}  {xc}/8   {hc}/8  {bar}")

    print("\n  Key shifts:")
    print("  - ker(O): 6→2 (先天 dominated by I∈ker(O) steps)")
    print("  - Q: 0→4 (Q is ABSENT from 先天, PRESENT in 後天)")
    print("  - H: 4→2 (H retreats)")
    print("  - ker(OMI): 2→6 (gains strongly)")
    print("  - P: 4→4 (unchanged)")


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 3: Symmetry Breaking Analysis
# ═══════════════════════════════════════════════════════════════════════

def computation_3():
    print("\n" + "=" * 70)
    print("COMPUTATION 3: SYMMETRY BREAKING ANALYSIS")
    print("=" * 70)

    # Part A: Complement-antipodal
    print("\n--- PART A: COMPLEMENT-ANTIPODAL ---\n")
    OPPOSITE = [('S', 'N'), ('SE', 'NW'), ('E', 'W'), ('NE', 'SW')]

    for name, arr in [("先天", XT), ("後天", HT)]:
        count = sum(1 for p1, p2 in OPPOSITE if arr[p1] ^ arr[p2] == 7)
        print(f"  {name}: {count}/4 complement pairs diametrically opposite")

    print()
    for p1, p2 in OPPOSITE:
        xt_comp = XT[p1] ^ XT[p2] == 7
        ht_comp = HT[p1] ^ HT[p2] == 7
        xt_pair = f"{TRIGRAM_ZH[XT[p1]]}/{TRIGRAM_ZH[XT[p2]]}"
        ht_pair = f"{TRIGRAM_ZH[HT[p1]]}/{TRIGRAM_ZH[HT[p2]]}"
        status = "PRESERVED" if ht_comp else "BROKEN"
        print(f"  {p1}-{p2}: 先天={xt_pair}({'✓' if xt_comp else '✗'}) "
              f"後天={ht_pair}({'✓' if ht_comp else '✗'}) [{status}]")

    # Part B: Symmetry groups
    print("\n--- PART B: SYMMETRY GROUPS ---\n")
    print("  先天 symmetry: complement (x→x⊕111) = 180° rotation")
    print("  This is the Z₂ generated by the complement involution.")
    print()

    # Check 後天 for any dihedral symmetries
    # D₈ has 16 elements: 8 rotations + 8 reflections
    # Test each on 後天
    ht_list = [HT[p] for p in POS_CW_FROM_N]
    symmetries = []

    for rot in range(8):
        rotated = [ht_list[(i + rot) % 8] for i in range(8)]
        if rotated == ht_list:
            symmetries.append(f"rotation by {rot * 45}°")

    for axis in range(8):
        reflected = [ht_list[(2 * axis - i) % 8] for i in range(8)]
        if reflected == ht_list:
            symmetries.append(f"reflection about axis {axis * 22.5}°")

    print(f"  後天 dihedral symmetries: {len(symmetries)}")
    for s in symmetries:
        print(f"    {s}")
    if not symmetries:
        print("    None (only identity)")

    # Part C: Transition permutation
    print("\n--- PART C: TRANSITION PERMUTATION ---\n")

    # Position permutation: where does 先天's content at pos p go in 後天?
    xt_inv = {v: k for k, v in XT.items()}
    ht_inv = {v: k for k, v in HT.items()}

    pos_perm = {}
    for pos in POS_CW_FROM_N:
        trig = XT[pos]
        pos_ht = ht_inv[trig]
        pos_perm[pos] = pos_ht

    print("  Position permutation (先天 pos → 後天 pos of same trigram):")
    for pos in POS_CW_FROM_N:
        trig = XT[pos]
        target = pos_perm[pos]
        fixed = "  FIXED" if pos == target else ""
        print(f"    {pos:3s} → {target:3s} ({TRIGRAM_ZH[trig]}){fixed}")

    # Compute cycles
    visited = set()
    cycles = []
    for start in POS_CW_FROM_N:
        if start in visited:
            continue
        cycle = [start]
        visited.add(start)
        curr = pos_perm[start]
        while curr != start:
            cycle.append(curr)
            visited.add(curr)
            curr = pos_perm[curr]
        cycles.append(cycle)

    print(f"\n  Cycle structure:")
    for c in cycles:
        if len(c) == 1:
            print(f"    Fixed: {c[0]} ({TRIGRAM_ZH[XT[c[0]]]})")
        else:
            pos_str = "→".join(c) + "→" + c[0]
            trig_str = "→".join(TRIGRAM_ZH[XT[p]] for p in c)
            print(f"    ({pos_str}) = ({trig_str})")

    # Check: are cycles related by 180° rotation?
    print(f"\n  Cycle 2 = Cycle 1 rotated by 180°:")
    if len(cycles) == 2 and len(cycles[0]) == 4 and len(cycles[1]) == 4:
        c1_nums = [POS_NUM[p] for p in cycles[0]]
        c2_nums = [POS_NUM[p] for p in cycles[1]]
        c1_rot = [(n + 4) % 8 for n in c1_nums]
        match = set(c1_rot) == set(c2_nums)
        print(f"    {match}")

    # Part D: The 0.5-bit in transition context
    print("\n--- PART D: THE 0.5-BIT IN TRANSITION ---\n")

    # Which complement pair stays on-axis?
    print("  Complement pair compass distances in 後天:")
    comp_pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    for a, b in comp_pairs:
        pa, pb = ht_inv[a], ht_inv[b]
        na, nb = POS_NUM[pa], POS_NUM[pb]
        dist = min(abs(na - nb), 8 - abs(na - nb))
        is_opp = dist == 4
        status = "OPPOSITE" if is_opp else f"dist={dist}"
        print(f"    {TRIGRAM_ZH[a]}({fmt3(a)})-{TRIGRAM_ZH[b]}({fmt3(b)}): "
              f"{pa}/{pb} [{status}]")

    print()
    print("  Only {坎,離} = Q-line pair remains diametrically opposite.")
    print("  The 先天→後天 transition preserves the Q-axis (S-N),")
    print("  which is the 互 attractor axis and the palindromic condition.")
    print()
    print("  The 0.5-bit choice between placing Wood on H or Q becomes:")
    print("    H-choice: Wood pair = {震,巽} (BROKEN axis, dist=1)")
    print("    Q-choice: Wood pair = {坎,離} (PRESERVED axis, dist=4)")
    print()
    print("  Traditional takes the H-choice: the same-element pair is on")
    print("  the broken axis, meaning Wood elements are adjacent (not opposite)")
    print("  in 後天. This breaks the 先天 symmetry maximally for Wood,")
    print("  while preserving it for the Water/Fire singletons.")


# ═══════════════════════════════════════════════════════════════════════
# COMPUTATION 4: Synthesis Addendum
# ═══════════════════════════════════════════════════════════════════════

def computation_4():
    print("\n" + "=" * 70)
    print("COMPUTATION 4: SYNTHESIS ADDENDUM")
    print("=" * 70)

    print("""
  先天 is a Fano triangle walk.
  ─────────────────────────────
  The 先天 arrangement is a Hamiltonian cycle on F₂³ using generators
  {O(001), I(100), MI(110)} with step pattern (I, MI, I, O) × 2.

  Key properties:
  1. 12 triangle generator sets (in 3 families of 4 by through-OMI edge)
     admit complement-antipodal Hamiltonian cycles. No Fano line does.
  2. 先天 uses {O, I, MI} from Family H, with edges on H, ker(O), ker(M).
  3. Exactly 2 undirected complement-antipodal cycles exist with
     these generators. They differ by swapping O↔MI in the pattern.
  4. Within Family H, {O, I, MI} is the unique member with single-bit
     edges (ker(O), ker(M)): the most "coordinate-aligned" triangle.

  後天 is 先天 + compass.
  ──────────────────────────
  The 先天→後天 transition is a permutation with cycle structure
  (two 4-cycles), related by 180° rotation, fixing no positions.

  The transition:
  - Breaks 3 of 4 complement-antipodal pairs
  - PRESERVES only the {坎,離} (Q-line) axis
  - Introduces Q-line generators (absent from 先天)
  - Shifts from ker(O)/ker(M)/H dominance to ker(OMI)/Q involvement
  - Uses 5 of 7 possible generators (vs. 先天's 3)

  The 0.5-bit acquires geometric meaning.
  ────────────────────────────────────────
  In 先天, all complement pairs are equivalent (D₂ symmetry).
  The transition breaks this equivalence by preserving one axis (Q).

  Traditional: Wood pair on H-line = BROKEN axis (elements adjacent)
  Alternative: Wood pair on Q-line = PRESERVED axis (elements opposite)

  The traditional choice says: the same-element pair belongs to the
  axis that the transition DESTROYS. This is consistent with:
  - H being the 互 kernel (internal structure line)
  - Q being the dynamic axis (attractor pair, preserved by transition)
  - The parity rotation P→H carrying 五行 information toward H
  """)


# ═══════════════════════════════════════════════════════════════════════
# MARKDOWN OUTPUT
# ═══════════════════════════════════════════════════════════════════════

def write_findings():
    xt_steps = step_xors(XT_CW)
    ht_steps = step_xors(HT_CW)
    xt_gens = frozenset(xt_steps)
    ht_gens = frozenset(ht_steps)

    L = []
    w = L.append

    w("# 先天 as Fano Walk: Findings\n")

    w("## 1. 先天 Fano Characterization\n")

    w("### Step-XOR Pattern\n")
    w("The 先天 arrangement (clockwise from S):")
    w("乾→兌→離→震→坤→艮→坎→巽→乾\n")
    w("| Step | From → To | XOR | Mask | Fano lines |")
    w("|------|-----------|-----|------|------------|")
    for i in range(8):
        t1, t2 = XT_CW[i], XT_CW[(i + 1) % 8]
        s = xt_steps[i]
        ls = ", ".join(lines_of(s))
        w(f"| {i + 1} | {TRIGRAM_ZH[t1]}→{TRIGRAM_ZH[t2]} | {fmt3(s)} | "
          f"{MASK_NAMES[s]} | {ls} |")
    w("")
    w("**Pattern: (I, MI, I, O) × 2** — period 4, using 3 generators.\n")

    w("### Generator Triangle\n")
    w("The generators {O(001), I(100), MI(110)} form a **triangle** in PG(2,2):\n")
    w("| Edge | Generators | Fano line | Third point |")
    w("|------|-----------|-----------|-------------|")
    w("| 1 | {O, MI} | **H** = ker(b₁⊕b₂) | OMI(111) |")
    w("| 2 | {I, MI} | ker(O) = ker(b₀) | M(010) |")
    w("| 3 | {O, I} | ker(M) = ker(b₁) | OI(101) |")
    w("")
    w("This triangle has one edge on the distinguished line H and two edges")
    w("on non-through-OMI lines. The generators are NOT collinear.\n")

    w("### Hamiltonian Cycle Structure\n")
    w("**Verified.** 12 three-element generator sets admit complement-antipodal")
    w("Hamiltonian cycles on F₂³. All are non-collinear triples (triangles).")
    w("No single Fano line admits any Hamiltonian cycle.\n")
    w("The 12 sets partition into **3 families of 4** by through-OMI edge:\n")
    w("| Family | Fixed edge | On line | Third generator options |")
    w("|--------|-----------|---------|------------------------|")
    w("| H | {O, MI} | H = ker(b₁⊕b₂) | M, OM, **I**, OI |")
    w("| P | {OM, I} | P = ker(b₀⊕b₁) | O, M, OI, MI |")
    w("| Q | {M, OI} | Q = ker(b₀⊕b₂) | O, OM, I, MI |")
    w("")
    w("先天 uses **{O, I, MI}** from Family H. Within Family H, it is the")
    w("unique member whose other two edges lie on the single-bit lines")
    w("ker(O) = ker(b₀) and ker(M) = ker(b₁).\n")
    w("Each generator set admits exactly 4 directed (= 2 undirected)")
    w("complement-antipodal cycles.\n")

    w("## 2. 後天 Step-XOR Analysis\n")
    w("| Step | From → To | XOR | Mask | Fano lines |")
    w("|------|-----------|-----|------|------------|")
    for i in range(8):
        t1, t2 = HT_CW[i], HT_CW[(i + 1) % 8]
        s = ht_steps[i]
        ls = ", ".join(lines_of(s))
        w(f"| {i + 1} | {TRIGRAM_ZH[t1]}→{TRIGRAM_ZH[t2]} | {fmt3(s)} | "
          f"{MASK_NAMES[s]} | {ls} |")
    w("")
    w(f"後天 uses **{len(ht_gens)} generators** "
      f"({', '.join(MASK_NAMES[g] for g in sorted(ht_gens))}) "
      f"vs. 先天's 3.\n")

    w("### Generator Comparison\n")
    w("| | 先天 | 後天 |")
    w("|---|------|------|")
    w(f"| Generators | {', '.join(MASK_NAMES[g] for g in sorted(xt_gens))} | "
      f"{', '.join(MASK_NAMES[g] for g in sorted(ht_gens))} |")
    w(f"| Count | 3 | {len(ht_gens)} |")
    w(f"| Shared | {', '.join(MASK_NAMES[g] for g in sorted(xt_gens & ht_gens))} | |")
    w(f"| Unique | {', '.join(MASK_NAMES[g] for g in sorted(xt_gens - ht_gens))} | "
      f"{', '.join(MASK_NAMES[g] for g in sorted(ht_gens - xt_gens))} |")
    w("")

    w("### Fano Line Hit Counts\n")
    w("| Line | 先天 | 後天 | Change |")
    w("|------|------|------|--------|")
    for func in range(1, 8):
        name, pts = FANO_LINES[func]
        xc = sum(1 for s in xt_steps if s in pts)
        hc = sum(1 for s in ht_steps if s in pts)
        delta = hc - xc
        arrow = "↑" if delta > 0 else "↓" if delta < 0 else "="
        w(f"| {name} | {xc}/8 | {hc}/8 | {arrow}{abs(delta)} |")
    w("")
    w("**Key shift:** Q goes from 0/8 (absent in 先天) to 4/8 (prominent in 後天).")
    w("The transition introduces Q-line structure that 先天 lacks entirely.\n")

    w("## 3. Symmetry Breaking\n")

    w("### Complement-Antipodal Pairs\n")
    w("| Pair | 先天 | 後天 | Status |")
    w("|------|------|------|--------|")
    OPPOSITE = [('S', 'N'), ('SE', 'NW'), ('E', 'W'), ('NE', 'SW')]
    for p1, p2 in OPPOSITE:
        ht_pair = f"{TRIGRAM_ZH[HT[p1]]}/{TRIGRAM_ZH[HT[p2]]}"
        xt_pair = f"{TRIGRAM_ZH[XT[p1]]}/{TRIGRAM_ZH[XT[p2]]}"
        ht_comp = HT[p1] ^ HT[p2] == 7
        status = "PRESERVED" if ht_comp else "BROKEN"
        w(f"| {p1}-{p2} | {xt_pair} ✓ | {ht_pair} {'✓' if ht_comp else '✗'} | {status} |")
    w("")
    w("Only **{坎,離}** (Q-line pair, Water/Fire) remains diametrically opposite.\n")

    w("### Transition Permutation\n")
    w("The 先天→後天 transition has cycle structure:\n")
    w("- **(S→NW→NE→E)**: carries {乾→艮→震→離}")
    w("- **(SW→SE→W→N)**: carries {巽→兌→坎→坤}")
    w("- The two 4-cycles are related by 180° rotation.\n")
    w("The transition is NOT a dihedral element (not a pure rotation or reflection).\n")

    w("### The 0.5-Bit in Transition Context\n")
    w("In 先天, all four complement pairs are equivalent (D₂ symmetry).")
    w("The transition breaks this, preserving only the Q-axis:\n")
    w("| Pair | Fano line | 後天 distance | Status |")
    w("|------|-----------|--------------|--------|")
    comp_pairs = [(0, 7, 'P'), (1, 6, 'H'), (2, 5, 'Q'), (3, 4, 'P')]
    ht_inv = {v: k for k, v in HT.items()}
    for a, b, line in comp_pairs:
        pa, pb = ht_inv[a], ht_inv[b]
        na, nb = POS_NUM[pa], POS_NUM[pb]
        dist = min(abs(na - nb), 8 - abs(na - nb))
        status = "PRESERVED" if dist == 4 else "BROKEN"
        w(f"| {TRIGRAM_ZH[a]}/{TRIGRAM_ZH[b]} | {line} | {dist} | {status} |")
    w("")
    w("The 0.5-bit chooses whether Wood (same-element pair) goes on:")
    w("- **H** (traditional): the BROKEN axis — Wood elements adjacent in 後天")
    w("- **Q** (alternative): the PRESERVED axis — Wood elements still opposite\n")
    w("Traditional = breaking the same-element pair's antipodality while")
    w("preserving the singleton elements' antipodality (Water/Fire on Q).\n")

    w("## 4. Synthesis Addendum\n")

    w("### 先天 = Fano triangle walk\n")
    w("The 先天 arrangement is characterized by:")
    w("1. Generator set {O, I, MI} from Family H (12 triangle sets exist,")
    w("   in 3 families by through-OMI edge; 先天 uses Family H)")
    w("2. Within Family H, unique member with single-bit edges (ker(O), ker(M))")
    w("3. Step pattern (I, MI, I, O) × 2: alternating I with MI/O")
    w("4. 2 undirected cycles exist; 先天 is one of them\n")

    w("### 後天 = 先天 + compass (Z₅)")
    w("The transition from 先天 to 後天:")
    w("- Breaks 3/4 complement-antipodal pairs")
    w("- Preserves only Q-axis (the dynamic/attractor axis)")
    w("- Introduces Q-line steps (absent in 先天)")
    w("- Increases generator count from 3 to 5")
    w("- Is two 4-cycles, related by 180° rotation\n")

    w("### What this means for the 0.5-bit\n")
    w("The 先天→後天 transition selects the Q-axis as the preserved")
    w("complement-antipodal axis. This creates an asymmetry between")
    w("the two odd-coset complement pairs:")
    w("- {坎,離} on Q: PRESERVED by transition, 互 attractor positions")
    w("- {震,巽} on H: BROKEN by transition, adjacent in 後天\n")
    w("The traditional assignment places Wood (same-element) on H,")
    w("the broken axis. The alternative places it on Q, the preserved axis.")
    w("While neither is forced by algebraic constraints alone,")
    w("the transition provides geometric context for the choice:\n")
    w("**The same-element pair belongs to the axis whose symmetry")
    w("the compass datum breaks.** The preserved axis carries the")
    w("dynamic singletons (Water/Fire = 互 attractors).\n")

    return '\n'.join(L)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    outdir = Path(__file__).parent

    computation_1()
    computation_2()
    computation_3()
    computation_4()

    md = write_findings()
    findings_path = outdir / "xiantian_fano_findings.md"
    findings_path.write_text(md)
    print(f"\n{'=' * 70}")
    print(f"Findings written to {findings_path}")


if __name__ == '__main__':
    main()
