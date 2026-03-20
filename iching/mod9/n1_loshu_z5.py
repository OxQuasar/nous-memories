#!/usr/bin/env python3
"""Z₅ structure of the Lo Shu compass layout.

Computes element-cycle properties of Lo Shu positions, flying star path,
後天 compass cycle, pairing systems, and magic square lines.
"""

# === Data Definitions ===

# Z₅ elements
EL = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}

# Lo Shu (後天) positions: ls_num → (trigram, binary_str|None, element_name, z5)
LS = {
    1: ('坎', '010', '水', 4),
    2: ('坤', '000', '土', 2),
    3: ('震', '001', '木', 0),
    4: ('巽', '110', '木', 0),
    5: ('中', None,  '土', 2),
    6: ('乾', '111', '金', 3),
    7: ('兌', '011', '金', 3),
    8: ('艮', '100', '土', 2),
    9: ('離', '101', '火', 1),
}

# 先天 (Fu Xi) ordering: fx_num → (trigram, element_name, z5)
FX = {
    1: ('乾', '金', 3),
    2: ('兌', '金', 3),
    3: ('離', '火', 1),
    4: ('震', '木', 0),
    5: ('巽', '木', 0),
    6: ('坎', '水', 4),
    7: ('艮', '土', 2),
    8: ('坤', '土', 2),
}

# Trigram → binary (Convention A: b₀=bottom, b₂=top)
TRIG_BIN = {'震': '001', '艮': '100', '巽': '110', '兌': '011',
            '離': '101', '坎': '010', '乾': '111', '坤': '000'}


# === Helpers ===

def z5_relation(a, b):
    """Directed Z₅ relation from element a to element b.
    Returns (distance, label)."""
    d = (b - a) % 5
    if d == 0:
        return 0, '比和'
    elif d == 1:
        return 1, f'{EL[a]}生{EL[b]}(↑)'   # a generates b, prograde
    elif d == 4:
        return 1, f'{EL[b]}生{EL[a]}(↓)'   # b generates a, retrograde 生
    elif d == 2:
        return 2, f'{EL[a]}克{EL[b]}(↑)'   # a overcomes b, prograde
    elif d == 3:
        return 2, f'{EL[b]}克{EL[a]}(↓)'   # b overcomes a, retrograde 克
    return d, '?'


def z5_type_short(a, b):
    """Short classification: 比和, 生↑, 生↓, 克↑, 克↓."""
    d = (b - a) % 5
    return {0: '比和', 1: '生↑', 4: '生↓', 2: '克↑', 3: '克↓'}[d]


def xor_mask(bin_a, bin_b):
    """XOR of two 3-bit binary strings, returns mask string and Hamming distance."""
    mask = ''.join('1' if a != b else '0' for a, b in zip(bin_a, bin_b))
    hamming = mask.count('1')
    return mask, hamming


def bit_layers(mask):
    """Which bits flip in a 3-bit mask (b₂b₁b₀ convention in string)."""
    # String index 0 = b₂, index 1 = b₁, index 2 = b₀
    layers = []
    names = ['b₂', 'b₁', 'b₀']
    for i, c in enumerate(mask):
        if c == '1':
            layers.append(names[i])
    return layers


def count_types(transitions):
    """Count 比和, 生↑, 生↓, 克↑, 克↓ from list of (z5_a, z5_b) pairs."""
    counts = {'比和': 0, '生↑': 0, '生↓': 0, '克↑': 0, '克↓': 0}
    for a, b in transitions:
        counts[z5_type_short(a, b)] += 1
    return counts


def print_separator(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


# === 1. Mapping Table ===

print_separator("1. LO SHU POSITION MAPPING TABLE")
print(f"{'LS#':>3} {'Trigram':>4} {'Binary':>6} {'Element':>4} {'Z₅':>3}")
print('-' * 30)
for n in range(1, 10):
    trig, bn, el, z5 = LS[n]
    bn_str = bn if bn else '  —'
    print(f"{n:>3}  {trig:>4}  {bn_str:>6}  {el:>4}  {z5:>3}")


# === 2. Lo Shu Sequential Cycle (1→2→...→9→1) ===

print_separator("2. LO SHU SEQUENTIAL CYCLE (1→2→3→...→9→1)")
print("This is label order, not a structural path.\n")

seq_cycle = list(range(1, 10)) + [1]  # wraps
transitions_seq = []
print(f"{'Step':>4}  {'From':>6}  {'To':>6}  {'Z₅':>5}  {'Relation'}")
print('-' * 55)
for i in range(len(seq_cycle) - 1):
    a, b = seq_cycle[i], seq_cycle[i + 1]
    za, zb = LS[a][3], LS[b][3]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    ta, tb = LS[a][0], LS[b][0]
    print(f"{i+1:>4}  {a}({ta}){EL[za]}  →  {b}({tb}){EL[zb]}  {typ:<5}  {rel}")
    transitions_seq.append((za, zb))

print("\nZ₅ value sequence:", [LS[n][3] for n in range(1, 10)])
print("Type counts:", count_types(transitions_seq))


# === 3. Flying Star Path (5→6→7→8→9→1→2→3→4) ===

print_separator("3. FLYING STAR PATH (5→6→7→8→9→1→2→3→4)")
print("Standard Lo Shu traversal. Center starts.\n")

fs_path = [5, 6, 7, 8, 9, 1, 2, 3, 4]
transitions_fs = []
print(f"{'Step':>4}  {'From':>10}  {'To':>10}  {'Z₅ type':>6}  {'XOR':>5}  {'Ham':>3}  {'Bits':>10}  {'Relation'}")
print('-' * 85)
for i in range(len(fs_path) - 1):
    a, b = fs_path[i], fs_path[i + 1]
    za, zb = LS[a][3], LS[b][3]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    ta, tb = LS[a][0], LS[b][0]
    ba, bb = LS[a][1], LS[b][1]

    if ba and bb:
        mask, ham = xor_mask(ba, bb)
        bits = '+'.join(bit_layers(mask))
        print(f"{i+1:>4}  {a}({ta}){ba}  →  {b}({tb}){bb}  {typ:<6}  {mask:>5}  {ham:>3}  {bits:>10}  {rel}")
    else:
        # Center involved
        center_label = f"{a}({ta})  —" if not ba else f"{a}({ta}){ba}"
        other_label = f"{b}({tb})  —" if not bb else f"{b}({tb}){bb}"
        print(f"{i+1:>4}  {center_label:>10}  →  {other_label:>10}  {typ:<6}    —    —         —  {rel}")
    transitions_fs.append((za, zb))

print("\nZ₅ value sequence:", [LS[n][3] for n in fs_path])
print("Type counts:", count_types(transitions_fs))


# === 4. 後天 Compass Cycle (clockwise from S) ===

print_separator("4. 後天 COMPASS CYCLE (clockwise from S)")
print("Spatial cycle: S→SW→W→NW→N→NE→E→SE→S")
print("Lo Shu positions: 9→2→7→6→1→8→3→4→9\n")

compass_cycle = [9, 2, 7, 6, 1, 8, 3, 4, 9]
transitions_comp = []
print(f"{'Step':>4}  {'From':>10}  {'To':>10}  {'Z₅ type':>6}  {'XOR':>5}  {'Ham':>3}  {'Bits':>10}  {'Relation'}")
print('-' * 85)
for i in range(len(compass_cycle) - 1):
    a, b = compass_cycle[i], compass_cycle[i + 1]
    za, zb = LS[a][3], LS[b][3]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    ta, tb = LS[a][0], LS[b][0]
    ba, bb = LS[a][1], LS[b][1]

    mask, ham = xor_mask(ba, bb)
    bits = '+'.join(bit_layers(mask))
    print(f"{i+1:>4}  {a}({ta}){ba}  →  {b}({tb}){bb}  {typ:<6}  {mask:>5}  {ham:>3}  {bits:>10}  {rel}")
    transitions_comp.append((za, zb))

print("\nZ₅ value sequence:", [LS[n][3] for n in compass_cycle[:-1]])
print("Type counts:", count_types(transitions_comp))


# === 5. Three Pairing Systems ===

print_separator("5. THREE PAIRING SYSTEMS COMPARED")

# 5a. 先天 pairs (n ↔ 9−n)
print("\n--- 先天 pairs (n ↔ 9−n) ---")
fx_pairs = [(1, 8), (2, 7), (3, 6), (4, 5)]
fx_transitions = []
print(f"{'Pair':>8}  {'A':>10}  {'B':>10}  {'Z₅ type':>6}  {'Relation'}")
print('-' * 55)
for a, b in fx_pairs:
    za, zb = FX[a][2], FX[b][2]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    print(f"  {a}↔{b}    {a}({FX[a][0]}){EL[za]}  ↔  {b}({FX[b][0]}){EL[zb]}  {typ:<6}  {rel}")
    fx_transitions.append((za, zb))
print("Type counts:", count_types(fx_transitions))

# 5b. Lo Shu pairs (n ↔ 10−n)
print("\n--- Lo Shu pairs (n ↔ 10−n) ---")
ls_pairs = [(1, 9), (2, 8), (3, 7), (4, 6)]
ls_transitions = []
print(f"{'Pair':>8}  {'A':>10}  {'B':>10}  {'Z₅ type':>6}  {'Relation'}")
print('-' * 55)
for a, b in ls_pairs:
    za, zb = LS[a][3], LS[b][3]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    print(f"  {a}↔{b}    {a}({LS[a][0]}){EL[za]}  ↔  {b}({LS[b][0]}){EL[zb]}  {typ:<6}  {rel}")
    ls_transitions.append((za, zb))
print("Center (5) self-paired: Z₅=2 (土), 比和")
print("Type counts:", count_types(ls_transitions))

# 5c. He Tu pairs (differ by 5)
print("\n--- He Tu pairs (differ by 5) ---")
ht_pairs = [(1, 6), (2, 7), (3, 8), (4, 9)]
ht_transitions = []
print(f"{'Pair':>8}  {'A':>10}  {'B':>10}  {'Z₅ type':>6}  {'Relation'}")
print('-' * 55)
for a, b in ht_pairs:
    za, zb = LS[a][3], LS[b][3]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    print(f"  {a}↔{b}    {a}({LS[a][0]}){EL[za]}  ↔  {b}({LS[b][0]}){EL[zb]}  {typ:<6}  {rel}")
    ht_transitions.append((za, zb))
print("Type counts:", count_types(ht_transitions))

# 5d. Summary comparison
print("\n--- Pairing Summary ---")
print(f"{'System':<15} {'比和':>4} {'生↑':>4} {'生↓':>4} {'克↑':>4} {'克↓':>4}")
print('-' * 40)
for name, trans in [('先天 (n↔9−n)', fx_transitions),
                     ('Lo Shu (n↔10−n)', ls_transitions),
                     ('He Tu (n,n+5)', ht_transitions)]:
    c = count_types(trans)
    print(f"{name:<15} {c['比和']:>4} {c['生↑']:>4} {c['生↓']:>4} {c['克↑']:>4} {c['克↓']:>4}")


# === 6. Magic Square Z₅ Grid ===

print_separator("6. MAGIC SQUARE Z₅ GRID")
print("Chinese convention: S at top.\n")

# Grid layout (S at top):
# SE(4)  S(9)  SW(2)
# E(3)   C(5)  W(7)
# NE(8)  N(1)  NW(6)
grid = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]
dir_labels = [
    ['SE', ' S', 'SW'],
    [' E', ' C', ' W'],
    ['NE', ' N', 'NW'],
]

print("Position grid (Lo Shu numbers):")
for r in range(3):
    cells = []
    for c in range(3):
        n = grid[r][c]
        cells.append(f"{dir_labels[r][c]}({n})={EL[LS[n][3]]}")
    print("  " + "  ".join(cells))

print("\nZ₅ value grid:")
for r in range(3):
    vals = [str(LS[grid[r][c]][3]) for c in range(3)]
    print("  " + "  ".join(vals))

# Define all 8 lines: 3 rows, 3 cols, 2 diags
lines = {
    'Row 0 (S)':    [(0,0), (0,1), (0,2)],
    'Row 1 (C)':    [(1,0), (1,1), (1,2)],
    'Row 2 (N)':    [(2,0), (2,1), (2,2)],
    'Col 0 (E)':    [(0,0), (1,0), (2,0)],
    'Col 1 (mid)':  [(0,1), (1,1), (2,1)],
    'Col 2 (W)':    [(2,0), (2,1), (2,2)],  # WRONG — fix below
    'Diag (SE→NW)': [(0,0), (1,1), (2,2)],
    'Diag (SW→NE)': [(0,2), (1,1), (2,0)],
}
# Fix col 2
lines['Col 2 (W)'] = [(0,2), (1,2), (2,2)]

print("\n--- Lines Analysis ---")
print(f"{'Line':<16} {'Positions':>14}  {'Elements':>10}  {'Z₅ vals':>10}  {'Σ%5':>4}  {'Pairs':>30}  {'比':>2} {'生':>2} {'克':>2}")
print('-' * 110)

for name, coords in lines.items():
    positions = [grid[r][c] for r, c in coords]
    z5vals = [LS[n][3] for n in positions]
    elements = [EL[z] for z in z5vals]
    s = sum(z5vals) % 5

    # All pairwise relations (3 pairs from triple)
    pair_rels = []
    line_counts = {'比和': 0, '生': 0, '克': 0}
    for i in range(3):
        for j in range(i+1, 3):
            typ = z5_type_short(z5vals[i], z5vals[j])
            a_el, b_el = elements[i], elements[j]
            pair_rels.append(f"{a_el}→{b_el}:{typ}")
            if '比' in typ:
                line_counts['比和'] += 1
            elif '生' in typ:
                line_counts['生'] += 1
            elif '克' in typ:
                line_counts['克'] += 1

    pos_str = ','.join(str(p) for p in positions)
    el_str = ','.join(elements)
    z5_str = ','.join(str(v) for v in z5vals)
    pair_str = ' | '.join(pair_rels)
    print(f"{name:<16} {pos_str:>14}  {el_str:>10}  {z5_str:>10}  {s:>4}  {pair_str:>30}  {line_counts['比和']:>2} {line_counts['生']:>2} {line_counts['克']:>2}")


# === 7. Flying Star Binary Analysis ===

print_separator("7. FLYING STAR BINARY ANALYSIS")
print("Trigram-to-trigram transitions only (excluding center).\n")

# Flying star: 5→6→7→8→9→1→2→3→4
# Center is position 5, so trigram-to-trigram: 6→7, 7→8, 8→9, 9→1, 1→2, 2→3, 3→4
fs_trig_pairs = [(6,7), (7,8), (8,9), (9,1), (1,2), (2,3), (3,4)]
print(f"{'Step':>4}  {'From':>8}  {'To':>8}  {'XOR':>5}  {'Ham':>3}  {'Bits':>10}  {'Z₅ type':>6}  {'Relation'}")
print('-' * 70)
for a, b in fs_trig_pairs:
    ba, bb = LS[a][1], LS[b][1]
    mask, ham = xor_mask(ba, bb)
    bits = '+'.join(bit_layers(mask))
    za, zb = LS[a][3], LS[b][3]
    _, rel = z5_relation(za, zb)
    typ = z5_type_short(za, zb)
    ta, tb = LS[a][0], LS[b][0]
    print(f"     {a}({ta}){ba}  →  {b}({tb}){bb}  {mask:>5}  {ham:>3}  {bits:>10}  {typ:<6}  {rel}")

# Check Hamming distance pattern
print("\nHamming distances:", [xor_mask(LS[a][1], LS[b][1])[1] for a, b in fs_trig_pairs])
print("Z₅ type sequence:", [z5_type_short(LS[a][3], LS[b][3]) for a, b in fs_trig_pairs])

# Do all Hamming-2 transitions map to a fixed Z₅ type?
ham2_types = set()
for a, b in fs_trig_pairs:
    mask, ham = xor_mask(LS[a][1], LS[b][1])
    if ham == 2:
        ham2_types.add(z5_type_short(LS[a][3], LS[b][3]))
print(f"Hamming-2 transitions produce Z₅ types: {ham2_types}")
print(f"Constant Hamming-2? {all(xor_mask(LS[a][1], LS[b][1])[1] == 2 for a, b in fs_trig_pairs)}")


# === 8. Summary Comparison of All Four Cycles ===

print_separator("8. SUMMARY COMPARISON — ALL FOUR CYCLES")

# 先天 cycle: 1→2→3→4→5→6→7→8→1
fx_cycle = list(range(1, 9)) + [1]
transitions_fx_cycle = [(FX[fx_cycle[i]][2], FX[fx_cycle[i+1]][2]) for i in range(len(fx_cycle) - 1)]

cycles = {
    '先天 (1→8→1)':       transitions_fx_cycle,
    'LS sequential':       transitions_seq,
    'Flying star':         transitions_fs,
    '後天 compass':        transitions_comp,
}

print(f"\n{'Cycle':<20} {'比和':>4} {'生↑':>4} {'生↓':>4} {'克↑':>4} {'克↓':>4}  {'Steps':>5}  {'Pro:Retro':>10}  {'Palindrome?'}")
print('-' * 90)

for name, trans in cycles.items():
    c = count_types(trans)
    n = len(trans)
    prograde = c['生↑'] + c['克↑']
    retrograde = c['生↓'] + c['克↓']
    ratio = f"{prograde}:{retrograde}"

    # Palindrome check: T(k) == T(n-1-k)?
    types = [z5_type_short(a, b) for a, b in trans]
    is_palindrome = all(types[k] == types[n-1-k] for k in range(n // 2))
    pal_str = "YES" if is_palindrome else "no"

    print(f"{name:<20} {c['比和']:>4} {c['生↑']:>4} {c['生↓']:>4} {c['克↑']:>4} {c['克↓']:>4}  {n:>5}  {ratio:>10}  {pal_str}")

# Print full type sequences for comparison
print("\n--- Full Z₅ Type Sequences ---")
for name, trans in cycles.items():
    types = [z5_type_short(a, b) for a, b in trans]
    print(f"{name:<20}: {' → '.join(types)}")

# Print Z₅ value sequences
print("\n--- Z₅ Value Sequences ---")
print(f"{'先天 (1→8)':<20}: {[FX[n][2] for n in range(1, 9)]}")
print(f"{'LS sequential':<20}: {[LS[n][3] for n in range(1, 10)]}")
print(f"{'Flying star':<20}: {[LS[n][3] for n in fs_path]}")
print(f"{'後天 compass':<20}: {[LS[n][3] for n in compass_cycle[:-1]]}")

print("\n" + "=" * 70)
print("  DONE")
print("=" * 70)
